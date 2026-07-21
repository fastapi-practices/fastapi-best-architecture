import asyncio
import functools
import time

from collections.abc import Callable
from typing import Any

from backend.common.log import log


def timer(func) -> Callable:  # ruff:ignore[missing-type-function-argument]
    """函数耗时计时装饰器"""

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        result = await func(*args, **kwargs)
        elapsed_seconds = time.perf_counter() - start_time
        _log_time(func, elapsed_seconds)
        return result

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_seconds = time.perf_counter() - start_time
        _log_time(func, elapsed_seconds)
        return result

    def _log_time(func, elapsed: float) -> None:  # ruff:ignore[missing-type-function-argument]
        # 智能选择单位（秒、毫秒、微秒、纳秒）
        if elapsed >= 1:
            unit, factor = 's', 1
        else:
            unit, factor = 'ms', 1e3

        log.info(f'{func.__module__}.{func.__name__} | {elapsed * factor:.3f} {unit}')

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
