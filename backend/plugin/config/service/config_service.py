from collections.abc import Sequence
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.cache.decorator import cache_invalidate, cached
from backend.common.exception import errors
from backend.common.pagination import paging_data
from backend.core.conf import settings
from backend.plugin.config.crud.crud_config import config_dao
from backend.plugin.config.model import Config
from backend.plugin.config.schema.config import (
    CreateConfigParam,
    UpdateConfigParam,
    UpdateConfigsParam,
)


class ConfigService:
    """参数配置服务类"""

    @staticmethod
    @cached(settings.CACHE_CONFIG_REDIS_PREFIX, key='pk')
    async def get(*, db: AsyncSession, pk: int) -> Config:
        """
        获取参数配置详情

        :param db: 数据库会话
        :param pk: 参数配置 ID
        :return:
        """
        config = await config_dao.get(db, pk)
        if not config:
            raise errors.NotFoundError(msg='参数配置不存在')
        return config

    @staticmethod
    @cached(settings.CACHE_CONFIG_REDIS_PREFIX, key='type')
    async def get_all(*, db: AsyncSession, type: str | None) -> Sequence[Config | None]:
        """
        获取所有参数配置

        :param db: 数据库会话
        :param type: 参数配置类型
        :return:
        """
        return await config_dao.get_all(db, type)

    @staticmethod
    async def get_list(*, db: AsyncSession, name: str | None, type: str | None) -> dict[str, Any]:
        """
        获取参数配置列表

        :param db: 数据库会话
        :param name: 参数配置名称
        :param type: 参数配置类型
        :return:
        """
        config_select = await config_dao.get_select(name=name, type=type)
        return await paging_data(db, config_select)

    @staticmethod
    @cache_invalidate(settings.CACHE_CONFIG_REDIS_PREFIX)
    async def create(*, db: AsyncSession, obj: CreateConfigParam) -> None:
        """
        创建参数配置

        :param db: 数据库会话
        :param obj: 参数配置创建参数
        :return:
        """
        config = await config_dao.get_by_key(db, obj.key)
        if config:
            raise errors.ConflictError(msg=f'参数配置 {obj.key} 已存在')
        await config_dao.create(db, obj)

    @staticmethod
    @cache_invalidate(settings.CACHE_CONFIG_REDIS_PREFIX)
    async def update(*, db: AsyncSession, pk: int, obj: UpdateConfigParam) -> int:
        """
        更新参数配置

        :param db: 数据库会话
        :param pk: 参数配置 ID
        :param obj: 参数配置更新参数
        :return:
        """
        config = await config_dao.get(db, pk)
        if not config:
            raise errors.NotFoundError(msg='参数配置不存在')
        if config.key != obj.key:
            config = await config_dao.get_by_key(db, obj.key)
            if config:
                raise errors.ConflictError(msg=f'参数配置 {obj.key} 已存在')
        count = await config_dao.update(db, pk, obj)
        return count

    @staticmethod
    @cache_invalidate(settings.CACHE_CONFIG_REDIS_PREFIX)
    async def bulk_update(*, db: AsyncSession, objs: list[UpdateConfigsParam]) -> int:
        """
        批量更新参数配置

        :param db: 数据库会话
        :param objs: 参数配置批量更新参数
        :return:
        """
        configs = await config_dao.get_all_by_ids(db, list({obj.id for obj in objs}))
        config_map = {config.id: config for config in configs}
        for obj in objs:
            if obj.id not in config_map:
                raise errors.NotFoundError(msg='参数配置不存在')

        changed_keys = [obj.key for obj in objs if config_map[obj.id].key != obj.key]
        if len(changed_keys) != len(set(changed_keys)):
            raise errors.ConflictError(msg='参数配置键名重复')

        key_configs = await config_dao.get_all_by_keys(db, list(set(changed_keys)))
        key_owner = {config.key: config.id for config in key_configs}
        for obj in objs:
            if config_map[obj.id].key != obj.key and obj.key in key_owner and key_owner[obj.key] != obj.id:
                raise errors.ConflictError(msg=f'参数配置 {obj.key} 已存在')

        count = await config_dao.bulk_update(db, objs)
        return count

    @staticmethod
    @cache_invalidate(settings.CACHE_CONFIG_REDIS_PREFIX)
    async def delete(*, db: AsyncSession, pks: list[int]) -> int:
        """
        批量删除参数配置

        :param db: 数据库会话
        :param pks: 参数配置 ID 列表
        :return:
        """
        count = await config_dao.delete(db, pks)
        return count


config_service: ConfigService = ConfigService()
