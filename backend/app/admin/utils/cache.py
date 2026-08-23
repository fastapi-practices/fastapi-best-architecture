from collections.abc import Sequence

from backend.core.conf import settings
from backend.database.redis import redis_client


class UserCacheManager:
    """用户缓存管理"""

    @staticmethod
    async def clear(user_ids: Sequence[int]) -> None:
        """清理用户缓存"""
        if user_ids:
            await redis_client.delete(*[f'{settings.JWT_USER_REDIS_PREFIX}:{user_id}' for user_id in user_ids])


user_cache_manager: UserCacheManager = UserCacheManager()
