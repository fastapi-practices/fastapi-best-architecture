from collections.abc import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.config.model import Config
from backend.plugin.config.schema.config import CreateConfigParam, UpdateConfigParam
from backend.utils.timezone import timezone


class CRUDConfig(CRUDPlus[Config]):
    """系统参数参数配置数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> Config | None:
        """
        获取参数配置详情

        :param db: 数据库会话
        :param pk: 参数配置 ID
        :return:
        """
        return await self.select_model_by_column(db, id=pk, deleted=0)

    async def get_all(self, db: AsyncSession, type: str | None) -> Sequence[Config | None]:
        """
        通过键名获取参数配置

        :param db: 数据库会话
        :param type: 参数配置类型
        :return:
        """
        filters = {'deleted': 0}

        if type is not None:
            filters['type'] = type

        return await self.select_models(db, **filters)

    async def get_all_by_ids(self, db: AsyncSession, pks: list[int]) -> Sequence[Config]:
        """
        通过 ID 列表批量获取参数配置

        :param db: 数据库会话
        :param pks: 参数配置 ID 列表
        :return:
        """
        return await self.select_models(db, id__in=pks, deleted=0)

    async def get_all_by_keys(self, db: AsyncSession, keys: list[str]) -> Sequence[Config]:
        """
        通过键名列表批量获取参数配置

        :param db: 数据库会话
        :param keys: 参数配置键名列表
        :return:
        """
        return await self.select_models(db, key__in=keys, deleted=0)

    async def get_by_key(self, db: AsyncSession, key: str) -> Config | None:
        """
        通过键名获取参数配置

        :param db: 数据库会话
        :param key: 参数配置键名
        :return:
        """
        return await self.select_model_by_column(db, key=key, deleted=0)

    async def get_select(self, name: str | None, type: str | None) -> Select:
        """
        获取参数配置列表查询表达式

        :param name: 参数配置名称
        :param type: 参数配置类型
        :return:
        """
        filters = {'deleted': 0}

        if name is not None:
            filters['name__like'] = f'%{name}%'
        if type is not None:
            filters['type__like'] = f'%{type}%'

        return await self.select_order('created_time', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateConfigParam) -> None:
        """
        创建参数配置

        :param db: 数据库会话
        :param obj: 创建参数配置参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateConfigParam) -> int:
        """
        更新参数配置

        :param db: 数据库会话
        :param pk: 参数配置 ID
        :param obj: 更新参数配置参数
        :return:
        """
        return await self.update_model_by_column(db, obj, id=pk, deleted=0)

    async def bulk_update(self, db: AsyncSession, objs: list[UpdateConfigParam]) -> int:
        """
        批量更新参数配置

        :param db: 数据库会话
        :param objs: 批量更新参数配置参数
        :return:
        """
        return await self.bulk_update_models(db, objs)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        批量删除参数配置

        :param db: 数据库会话
        :param pks: 参数配置 ID 列表
        :return:
        """
        return await self.delete_model_by_column(
            db,
            allow_multiple=True,
            logical_deletion=True,
            deleted_flag_column='deleted',
            deleted_flag_value=self.model.id,
            deleted_at_column='deleted_time',
            deleted_at_factory=timezone.now(),
            id__in=pks,
            deleted=0,
        )


config_dao: CRUDConfig = CRUDConfig(Config)
