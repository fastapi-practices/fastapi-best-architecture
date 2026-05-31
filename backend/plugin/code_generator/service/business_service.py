from collections.abc import Sequence
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.exception import errors
from backend.common.pagination import paging_data
from backend.plugin.code_generator.crud.crud_business import gen_business_dao
from backend.plugin.code_generator.model import GenBusiness
from backend.plugin.code_generator.schema.business import CreateGenBusinessParam, UpdateGenBusinessParam


class GenBusinessService:
    """代码生成业务服务类"""

    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> GenBusiness:
        """
        获取指定 ID 的业务

        :param db: 数据库会话
        :param pk: 业务 ID
        :return:
        """

        business = await gen_business_dao.get(db, pk)
        if not business:
            raise errors.NotFoundError(msg='代码生成业务不存在')
        return business

    @staticmethod
    async def get_all(*, db: AsyncSession) -> Sequence[GenBusiness]:
        """
        获取所有业务

        :param db: 数据库会话
        :return:
        """

        return await gen_business_dao.get_all(db)

    @staticmethod
    async def get_list(*, db: AsyncSession, table_name: str) -> dict[str, Any]:
        """
        获取代码生成业务列表

        :param db: 数据库会话
        :param table_name: 业务表名
        :return:
        """
        business_select = await gen_business_dao.get_select(table_name=table_name)
        return await paging_data(db, business_select)

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateGenBusinessParam) -> None:
        """
        创建业务

        :param db: 数据库会话
        :param obj: 创建业务参数
        :return:
        """

        business = await gen_business_dao.get_by_name(db, obj.table_name)
        if business:
            raise errors.ConflictError(msg='代码生成业务已存在')
        await gen_business_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateGenBusinessParam) -> int:
        """
        更新业务

        :param db: 数据库会话
        :param pk: 业务 ID
        :param obj: 更新业务参数
        :return:
        """

        business = await gen_business_dao.get(db, pk)
        if not business:
            raise errors.NotFoundError(msg='代码生成业务不存在')
        if business.table_name != obj.table_name and await gen_business_dao.get_by_name(db, obj.table_name):
            raise errors.ConflictError(msg='代码生成业务已存在')
        return await gen_business_dao.update(db, pk, obj)

    @staticmethod
    async def delete(*, db: AsyncSession, pk: int) -> int:
        """
        删除业务

        :param db: 数据库会话
        :param pk: 业务 ID
        :return:
        """

        business = await gen_business_dao.get(db, pk)
        if not business:
            raise errors.NotFoundError(msg='代码生成业务不存在')
        return await gen_business_dao.delete(db, pk)


gen_business_service: GenBusinessService = GenBusinessService()
