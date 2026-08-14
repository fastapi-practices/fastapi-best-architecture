import asyncio
import atexit
import threading
import weakref

from collections.abc import Awaitable, Callable, Coroutine
from functools import wraps
from typing import Any, TypeVar

T = TypeVar('T')


class _TaskRunner:
    """在后台线程上运行 asyncio 事件循环的任务运行器"""

    def __init__(self) -> None:
        self.__loop: asyncio.AbstractEventLoop | None = None
        self.__thread: threading.Thread | None = None
        self.__lock = threading.Lock()
        atexit.register(self.close)

    def close(self) -> None:
        """关闭事件循环并清理"""
        with self.__lock:
            if self.__loop:
                self.__loop.call_soon_threadsafe(self.__loop.stop)
            if self.__thread and self.__thread.is_alive():
                self.__thread.join()
            self.__loop = None
            self.__thread = None
            name = f'TaskRunner-{threading.get_ident()}'
            _runner_map.pop(name, None)

    def _target(self) -> None:
        """后台线程的目标函数"""
        try:
            self.__loop.run_forever()
        finally:
            self.__loop.close()

    def run(self, coro: Awaitable[T]) -> T:
        """在后台事件循环上运行协程并返回其结果"""
        with self.__lock:
            name = f'TaskRunner-{threading.get_ident()}'
            if self.__loop is None:
                self.__loop = asyncio.new_event_loop()
                self.__thread = threading.Thread(target=self._target, daemon=True, name=name)
                self.__thread.start()
            future = asyncio.run_coroutine_threadsafe(coro, self.__loop)
            return future.result()


_runner_map = weakref.WeakValueDictionary()


def run_await(coro: Callable[..., Awaitable[T]] | Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., T]:
    """将协程包装在函数中，直到它执行完为止"""

    @wraps(coro)
    def wrapped(*args, **kwargs):  # ruff:ignore[missing-return-type-private-function]
        inner = coro(*args, **kwargs)
        if not asyncio.iscoroutine(inner) and not asyncio.isfuture(inner):
            raise TypeError(f'Expected coroutine or future, got {type(inner)}')

        try:
            # 如果事件循环正在运行，则使用任务调用
            asyncio.get_running_loop()
            name = f'TaskRunner-{threading.get_ident()}'
            if name not in _runner_map:
                _runner_map[name] = _TaskRunner()
            return _runner_map[name].run(inner)
        except RuntimeError:
            # 如果没有，则创建一个新的事件循环
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            return loop.run_until_complete(inner)

    wrapped.__doc__ = coro.__doc__
    return wrapped
