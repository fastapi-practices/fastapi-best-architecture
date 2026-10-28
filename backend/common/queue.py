import asyncio
import time

from asyncio import Queue
from collections.abc import Awaitable, Callable

from backend.common.log import log
from backend.common.observability.prometheus.queue import (
    inc_queue_exception,
    observe_batch_dequeue_cost,
    observe_queue_size,
)

_STOP_CHECK_INTERVAL = 1.0


async def batch_dequeue[T](
    queue: Queue[T],
    max_items: int,
    timeout: float,
    *,
    queue_name: str = 'default',
    stop_event: asyncio.Event | None = None,
) -> list[T]:
    """
    从异步队列中获取多个项目

    :param queue: 用于获取项目的 `asyncio.Queue` 队列
    :param max_items: 从队列中获取的最大项目数量
    :param timeout: 总的等待超时时间（秒）
    :param queue_name: 队列名称，用于 Prometheus 标签
    :param stop_event: 停止信号，置位后不再等待新项目，只取走队列中已有的项目
    :return:
    """
    items = []
    start = time.perf_counter()

    async def collector() -> None:
        while len(items) < max_items:
            if stop_event is None:
                item = await queue.get()
            elif stop_event.is_set():
                if queue.empty():
                    return
                item = queue.get_nowait()
            else:
                # 周期性检查停止信号，保证停止时不必等满超时时间
                try:
                    item = await asyncio.wait_for(queue.get(), timeout=_STOP_CHECK_INTERVAL)
                except TimeoutError:
                    continue
            items.append(item)
            observe_queue_size(queue, queue_name=queue_name)

    try:
        await asyncio.wait_for(collector(), timeout=timeout)
    except TimeoutError:
        pass
    except Exception as e:
        inc_queue_exception(queue_name=queue_name)
        log.error(f'队列批量获取失败: {e}')
    finally:
        observe_batch_dequeue_cost(start, queue_name=queue_name)
        observe_queue_size(queue, queue_name=queue_name)

    return items


async def batch_consume[T](
    queue: Queue[T],
    max_items: int,
    timeout: float,
    handler: Callable[..., Awaitable[None]],
    *,
    queue_name: str = 'default',
    error_message: str = '队列批量处理失败',
    item_name: str = '数据',
    stop_event: asyncio.Event | None = None,
) -> None:
    """
    持续批量消费队列

    :param queue: 用于获取项目的 `asyncio.Queue` 队列
    :param max_items: 从队列中获取的最大项目数量
    :param timeout: 总的等待超时时间（秒）
    :param handler: 批量处理函数
    :param queue_name: 队列名称，用于 Prometheus 标签
    :param error_message: 处理失败日志消息
    :param item_name: 队列数据名称
    :param stop_event: 停止信号，置位后排空队列并退出
    :return:
    """
    while True:
        items = await batch_dequeue(
            queue, max_items=max_items, timeout=timeout, queue_name=queue_name, stop_event=stop_event
        )
        if not items:
            if stop_event is not None and stop_event.is_set():
                return
            continue

        try:
            await handler(items)
        except Exception as e:
            log.error(f'{error_message}，丢失 {len(items)} 条{item_name}: {e}')
        finally:
            for _ in items:
                queue.task_done()
                observe_queue_size(queue, queue_name=queue_name)
