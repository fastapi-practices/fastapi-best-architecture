import asyncio
import atexit
import os
import threading
import weakref

from collections.abc import Awaitable, Callable, Coroutine
from functools import wraps
from typing import Any

_runner_context = threading.local()


class _TaskRunner:
    """在后台线程上运行 asyncio 事件循环的任务运行器"""

    def __init__(self) -> None:
        self.__loop: asyncio.AbstractEventLoop | None = None
        self.__thread: threading.Thread | None = None
        self.__pid = os.getpid()
        self.__name = f'TaskRunner-{self.__pid}-{threading.get_ident()}'
        # 同步等待期间可能发生同线程重入
        self.__lock = threading.RLock()
        atexit.register(self.close)

    def close(self) -> None:
        """关闭事件循环并清理"""
        if os.getpid() != self.__pid:
            return
        with self.__lock:
            loop = self.__loop
            thread = self.__thread
            if loop and thread and thread.is_alive() and loop.is_running():

                async def cancel_pending_tasks() -> None:
                    current_task = asyncio.current_task()
                    pending_tasks = [task for task in asyncio.all_tasks() if task is not current_task]
                    for task in pending_tasks:
                        task.cancel()
                    await asyncio.gather(*pending_tasks, return_exceptions=True)

                asyncio.run_coroutine_threadsafe(cancel_pending_tasks(), loop).result()
                loop.call_soon_threadsafe(loop.stop)
                thread.join()
            self.__loop = None
            self.__thread = None
            _runner_map.pop(self.__name, None)

    def _target(self) -> None:
        """后台线程的目标函数"""
        _runner_context.active = True
        try:
            self.__loop.run_forever()
        finally:
            _runner_context.active = False
            self.__loop.close()

    def run[T](self, coro: Awaitable[T]) -> T:
        """在后台事件循环上运行协程并返回其结果"""
        if self.__thread is threading.current_thread():
            if asyncio.iscoroutine(coro):
                coro.close()
            raise RuntimeError('run_await 不能在自身事件循环线程中同步等待')

        async def wait_for_result() -> T:
            return await coro

        with self.__lock:
            name = self.__name
            if self.__loop is None:
                self.__loop = asyncio.new_event_loop()
                self.__thread = threading.Thread(target=self._target, daemon=True, name=name)
                self.__thread.start()
            future = asyncio.run_coroutine_threadsafe(wait_for_result(), self.__loop)
            try:
                return future.result()
            except BaseException:
                future.cancel()
                raise


_runner_map = weakref.WeakValueDictionary()


def run_await[T](coro: Callable[..., Awaitable[T]] | Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., T]:
    """将协程包装在函数中，直到它执行完为止"""

    @wraps(coro)
    def wrapped(*args, **kwargs):  # ruff:ignore[missing-return-type-private-function]
        inner = coro(*args, **kwargs)
        if not asyncio.iscoroutine(inner) and not asyncio.isfuture(inner):
            raise TypeError(f'预期为协程或 Future，实际为 {type(inner)}')
        if getattr(_runner_context, 'active', False):
            if asyncio.iscoroutine(inner):
                inner.close()
            raise RuntimeError('run_await 不能在自身事件循环线程中同步等待')
        if asyncio.isfuture(inner):
            loop = inner.get_loop()
            if not loop.is_running():
                try:
                    asyncio.get_running_loop()
                except RuntimeError:
                    pass
                else:
                    raise RuntimeError('事件循环运行时不能同步等待 Future')
                return loop.run_until_complete(inner)

        # 统一在常驻的后台事件循环上执行，避免同步调用方创建的临时循环在调用结束后停止，
        # 导致循环上运行的后台任务（如雪花算法节点心跳）无法继续执行
        name = f'TaskRunner-{os.getpid()}-{threading.get_ident()}'
        if name not in _runner_map:
            _runner_map[name] = _TaskRunner()
        return _runner_map[name].run(inner)

    wrapped.__doc__ = coro.__doc__
    return wrapped
