from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import anyio

from backend.common.exception import errors
from backend.core.path_conf import RELOAD_LOCK_FILE
from backend.database.redis import redis_client


@asynccontextmanager
async def acquire_distributed_reload_lock() -> AsyncGenerator[None, Any]:
    """获取分布式热重载锁"""
    lock = redis_client.lock(
        'fba:reload_lock',
        timeout=300,  # 锁持有超时：5 分钟
        blocking_timeout=60,  # 获取锁等待超时：60 秒
    )
    if not await lock.acquire():
        raise errors.ServerError(msg='获取热重载锁超时，请稍后重试')

    # 文件锁（通知文件监控器跳过重载）
    lock_path = anyio.Path(RELOAD_LOCK_FILE)
    await lock_path.touch()

    try:
        yield
    finally:
        await lock_path.unlink(missing_ok=True)
        if await lock.owned():
            await lock.release()
