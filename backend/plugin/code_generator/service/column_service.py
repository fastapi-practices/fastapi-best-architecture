from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.enums import DataBaseType
from backend.common.exception import errors
from backend.core.conf import settings
from backend.plugin.code_generator.crud.crud_business import gen_business_dao
from backend.plugin.code_generator.crud.crud_column import gen_column_dao
from backend.plugin.code_generator.enums import GenMySQLColumnType, GenPostgreSQLColumnType
from backend.plugin.code_generator.model import GenColumn
from backend.plugin.code_generator.schema.column import CreateGenColumnParam, UpdateGenColumnParam
from backend.plugin.code_generator.utils.type_conversion import sql_type_to_pydantic


class GenColumnService:
    """代码生成模型列服务类"""

    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> GenColumn:
        """
        获取指定 ID 的模型列

        :param db: 数据库会话
        :param pk: 模型列 ID
        :return:
        """

        column = await gen_column_dao.get(db, pk)
        if not column:
            raise errors.NotFoundError(msg='代码生成模型列不存在')
        if not await gen_business_dao.get(db, column.gen_business_id):
            raise errors.NotFoundError(msg='代码生成业务不存在')
        return column

    @staticmethod
    async def get_types() -> list[str]:
        """获取所有列类型"""
        if DataBaseType.mysql == settings.DATABASE_TYPE:
            types = GenMySQLColumnType.get_member_keys()
        else:
            types = GenPostgreSQLColumnType.get_member_keys()
        types.sort()
        return types

    @staticmethod
    async def get_columns(*, db: AsyncSession, business_id: int) -> Sequence[GenColumn]:
        """
        获取指定业务的所有模型列

        :param db: 数据库会话
        :param business_id: 业务 ID
        :return:
        """

        if not await gen_business_dao.get(db, business_id):
            raise errors.NotFoundError(msg='代码生成业务不存在')
        return await gen_column_dao.get_all_by_business(db, business_id)

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateGenColumnParam) -> None:
        """
        创建模型列

        :param db: 数据库会话
        :param obj: 创建模型列参数
        :return:
        """

        if not await gen_business_dao.get(db, obj.gen_business_id):
            raise errors.NotFoundError(msg='代码生成业务不存在')

        gen_columns = await gen_column_dao.get_all_by_business(db, obj.gen_business_id)
        if obj.name in [gen_column.name for gen_column in gen_columns]:
            raise errors.ForbiddenError(msg='模型列已存在')

        pd_type = sql_type_to_pydantic(obj.type)
        await gen_column_dao.create(db, obj, pd_type=pd_type)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateGenColumnParam) -> int:
        """
        更新模型列

        :param db: 数据库会话
        :param pk: 模型列 ID
        :param obj: 更新模型列参数
        :return:
        """

        column = await gen_column_dao.get(db, pk)
        if not column:
            raise errors.NotFoundError(msg='代码生成模型列不存在')
        if not await gen_business_dao.get(db, column.gen_business_id):
            raise errors.NotFoundError(msg='代码生成业务不存在')
        if not await gen_business_dao.get(db, obj.gen_business_id):
            raise errors.NotFoundError(msg='代码生成业务不存在')
        if obj.name != column.name:
            gen_columns = await gen_column_dao.get_all_by_business(db, obj.gen_business_id)
            if obj.name in [gen_column.name for gen_column in gen_columns]:
                raise errors.ConflictError(msg='模型列名已存在')

        pd_type = sql_type_to_pydantic(obj.type)
        return await gen_column_dao.update(db, pk, obj, pd_type=pd_type)

    @staticmethod
    async def delete(*, db: AsyncSession, pk: int) -> int:
        """
        删除模型列

        :param db: 数据库会话
        :param pk: 模型列 ID
        :return:
        """

        column = await gen_column_dao.get(db, pk)
        if not column:
            raise errors.NotFoundError(msg='代码生成模型列不存在')
        if not await gen_business_dao.get(db, column.gen_business_id):
            raise errors.NotFoundError(msg='代码生成业务不存在')
        return await gen_column_dao.delete(db, pk)


gen_column_service: GenColumnService = GenColumnService()
