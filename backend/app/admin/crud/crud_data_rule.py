from collections.abc import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import DataRule
from backend.app.admin.schema.data_rule import CreateDataRuleParam, UpdateDataRuleParam
from backend.utils.timezone import timezone


class CRUDDataRule(CRUDPlus[DataRule]):
    """数据规则数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> DataRule | None:
        """
        获取规则详情

        :param db: 数据库会话
        :param pk: 规则 ID
        :return:
        """
        return await self.select_model(db, pk, deleted=0)

    async def get_select(self, name: str | None) -> Select:
        """
        获取规则列表查询表达式

        :param name: 规则名称
        :return:
        """
        filters = {'deleted': 0}

        if name is not None:
            filters['name__like'] = f'%{name}%'

        return await self.select_order('id', **filters)

    async def get_by_name(self, db: AsyncSession, name: str) -> DataRule | None:
        """
        通过名称获取规则

        :param db: 数据库会话
        :param name: 规则名称
        :return:
        """
        return await self.select_model_by_column(db, name=name, deleted=0)

    async def get_all(self, db: AsyncSession) -> Sequence[DataRule]:
        """
        获取所有规则

        :param db: 数据库会话
        :return:
        """
        return await self.select_models(db, deleted=0)

    async def get_all_by_ids(self, db: AsyncSession, pks: list[int]) -> Sequence[DataRule]:
        """
        通过 ID 列表批量获取数据规则

        :param db: 数据库会话
        :param pks: 规则 ID 列表
        :return:
        """
        return await self.select_models(db, id__in=pks, deleted=0)

    async def create(self, db: AsyncSession, obj: CreateDataRuleParam) -> None:
        """
        创建规则

        :param db: 数据库会话
        :param obj: 创建规则参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateDataRuleParam) -> int:
        """
        更新规则

        :param db: 数据库会话
        :param pk: 规则 ID
        :param obj: 更新规则参数
        :return:
        """
        return await self.update_model_by_column(db, obj, id=pk, deleted=0)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        批量删除规则

        :param db: 数据库会话
        :param pks: 规则 ID 列表
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


data_rule_dao: CRUDDataRule = CRUDDataRule(DataRule)
