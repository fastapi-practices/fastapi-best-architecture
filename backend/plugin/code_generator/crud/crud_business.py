from collections.abc import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.code_generator.model import GenBusiness
from backend.plugin.code_generator.schema.business import CreateGenBusinessParam, UpdateGenBusinessParam
from backend.utils.timezone import timezone


class CRUDGenBusiness(CRUDPlus[GenBusiness]):
    """代码生成业务 CRUD 类"""

    async def get(self, db: AsyncSession, pk: int) -> GenBusiness | None:
        """
        获取代码生成业务

        :param db: 数据库会话
        :param pk: 代码生成业务 ID
        :return:
        """
        return await self.select_model(db, pk, deleted=0)

    async def get_by_name(self, db: AsyncSession, name: str) -> GenBusiness | None:
        """
        通过 name 获取代码生成业务

        :param db: 数据库会话
        :param name: 表名
        :return:
        """
        return await self.select_model_by_column(db, table_name=name, deleted=0)

    async def get_all(self, db: AsyncSession) -> Sequence[GenBusiness]:
        """
        获取所有代码生成业务

        :param db: 数据库会话
        :return:
        """
        return await self.select_models(db, deleted=0)

    async def get_select(self, table_name: str | None) -> Select:
        """
        获取所有代码生成业务查询表达式

        :param table_name: 业务表名
        :return:
        """
        filters = {'deleted': 0}

        if table_name is not None:
            filters['table_name__like'] = f'%{table_name}%'

        return await self.select_order('id', 'desc', **filters)

    async def create(self, db: AsyncSession, obj: CreateGenBusinessParam) -> None:
        """
        创建代码生成业务

        :param db: 数据库会话
        :param obj: 创建代码生成业务参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateGenBusinessParam) -> int:
        """
        更新代码生成业务

        :param db: 数据库会话
        :param pk: 代码生成业务 ID
        :param obj: 更新代码生成业务参数
        :return:
        """
        return await self.update_model_by_column(db, obj, id=pk, deleted=0)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        """
        删除代码生成业务

        :param db: 数据库会话
        :param pk: 代码生成业务 ID
        :return:
        """
        return await self.delete_model_by_column(
            db,
            logical_deletion=True,
            deleted_flag_column='deleted',
            deleted_flag_value=self.model.id,
            deleted_at_column='deleted_time',
            deleted_at_factory=timezone.now(),
            id=pk,
            deleted=0,
        )


gen_business_dao: CRUDGenBusiness = CRUDGenBusiness(GenBusiness)
