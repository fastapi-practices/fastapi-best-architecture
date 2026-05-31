from collections.abc import Sequence
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.crud.crud_data_rule import data_rule_dao
from backend.app.admin.crud.crud_data_scope import data_scope_dao
from backend.app.admin.model import DataScope
from backend.app.admin.schema.data_scope import (
    CreateDataScopeParam,
    DeleteDataScopeParam,
    UpdateDataScopeParam,
    UpdateDataScopeRuleParam,
)
from backend.app.admin.utils.cache import user_cache_manager
from backend.common.exception import errors
from backend.common.pagination import paging_data


class DataScopeService:
    """数据范围服务类"""

    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> DataScope:
        """
        获取数据范围详情

        :param db: 数据库会话
        :param pk: 范围 ID
        :return:
        """

        data_scope = await data_scope_dao.get(db, pk)
        if not data_scope:
            raise errors.NotFoundError(msg='数据范围不存在')
        return data_scope

    @staticmethod
    async def get_all(*, db: AsyncSession) -> Sequence[DataScope]:
        """
        获取所有数据范围

        :param db: 数据库会话
        :return:
        """

        data_scopes = await data_scope_dao.get_all(db)
        return data_scopes

    @staticmethod
    async def get_rules(*, db: AsyncSession, pk: int) -> DataScope:
        """
        获取数据范围规则

        :param db: 数据库会话
        :param pk: 范围 ID
        :return:
        """

        data_scope = await data_scope_dao.get_join(db, pk)
        if not data_scope:
            raise errors.NotFoundError(msg='数据范围不存在')
        return data_scope

    @staticmethod
    async def get_list(*, db: AsyncSession, name: str | None, status: int | None) -> dict[str, Any]:
        """
        获取数据范围列表

        :param db: 数据库会话
        :param name: 范围名称
        :param status: 范围状态
        :return:
        """
        data_scope_select = await data_scope_dao.get_select(name, status)
        return await paging_data(db, data_scope_select)

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateDataScopeParam) -> None:
        """
        创建数据范围

        :param db: 数据库会话
        :param obj: 数据范围参数
        :return:
        """
        data_scope = await data_scope_dao.get_by_name(db, obj.name)
        if data_scope:
            raise errors.ConflictError(msg='数据范围已存在')
        await data_scope_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateDataScopeParam) -> int:
        """
        更新数据范围

        :param db: 数据库会话
        :param pk: 范围 ID
        :param obj: 数据范围更新参数
        :return:
        """
        data_scope = await data_scope_dao.get(db, pk)
        if not data_scope:
            raise errors.NotFoundError(msg='数据范围不存在')
        if data_scope.name != obj.name and await data_scope_dao.get_by_name(db, obj.name):
            raise errors.ConflictError(msg='数据范围已存在')
        count = await data_scope_dao.update(db, pk, obj)
        await user_cache_manager.clear_by_data_scope_id(db, [pk])
        return count

    @staticmethod
    async def update_data_scope_rule(*, db: AsyncSession, pk: int, rule_ids: UpdateDataScopeRuleParam) -> int:
        """
        更新数据范围规则

        :param db: 数据库会话
        :param pk: 范围 ID
        :param rule_ids: 规则 ID 列表
        :return:
        """
        data_scope = await data_scope_dao.get(db, pk)
        if not data_scope:
            raise errors.NotFoundError(msg='数据范围不存在')
        if rule_ids.rules:
            rules = await data_rule_dao.get_all_by_ids(db, list(set(rule_ids.rules)))
            if {rule.id for rule in rules} != set(rule_ids.rules):
                raise errors.NotFoundError(msg='数据规则不存在')
        count = await data_scope_dao.update_rules(db, pk, rule_ids)
        await user_cache_manager.clear_by_data_scope_id(db, [pk])
        return count

    @staticmethod
    async def delete(*, db: AsyncSession, obj: DeleteDataScopeParam) -> int:
        """
        批量删除数据范围

        :param db: 数据库会话
        :param obj: 范围 ID 列表
        :return:
        """
        count = await data_scope_dao.delete(db, obj.pks)
        await user_cache_manager.clear_by_data_scope_id(db, obj.pks)
        return count


data_scope_service: DataScopeService = DataScopeService()
