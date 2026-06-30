from typing import Any

import cachebox

from backend.core.conf import settings


class LocalCacheManager:
    """本地缓存管理器"""

    def __init__(self) -> None:
        self.hot_cache: cachebox.TTLCache = cachebox.TTLCache(
            settings.CACHE_LOCAL_MAXSIZE, global_ttl=settings.CACHE_LOCAL_TTL
        )

    def get(self, key: str) -> Any:
        """获取缓存"""
        try:
            return self.hot_cache[key]
        except KeyError:
            return None

    def set(self, key: str, value: Any) -> None:
        """设置缓存"""
        self.hot_cache[key] = value

    def delete(self, key: str) -> bool:
        """删除缓存"""
        try:
            del self.hot_cache[key]
        except KeyError:
            return False
        return True

    def clear(self) -> None:
        """清空缓存"""
        self.hot_cache.clear()

    def delete_by_prefix(self, key_prefix: str, exclude_keys: str | list[str] | None = None) -> None:
        """
        删除指定前缀的缓存

        :param key_prefix: 要删除的键前缀
        :param exclude_keys: 要排除的键或键列表
        :return:
        """
        exclude_set = (
            set(exclude_keys)
            if isinstance(exclude_keys, list)
            else {exclude_keys}
            if isinstance(exclude_keys, str)
            else set()
        )
        for key in list(self.hot_cache.keys()):
            if (key == key_prefix or key.startswith(f'{key_prefix}:')) and key not in exclude_set:
                try:
                    del self.hot_cache[key]
                except KeyError:
                    pass


local_cache_manager = LocalCacheManager()
