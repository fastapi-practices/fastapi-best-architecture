from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.code_generator.model import GenColumn
from backend.plugin.code_generator.schema.column import (
    CreateGenColumnInternalParam,
    CreateGenColumnParam,
    UpdateGenColumnParam,
)


class CRUDGenColumn(CRUDPlus[GenColumn]):
    """代码生成模型列 CRUD 类"""

    async def get(self, db: AsyncSession, pk: int) -> GenColumn | None:
        """
        获取代码生成模型列

        :param db: 数据库会话
        :param pk: 代码生成模型 ID
        :return:
        """
        return await self.select_model(db, pk)

    async def get_all_by_business(self, db: AsyncSession, business_id: int) -> Sequence[GenColumn]:
        """
        获取所有代码生成模型列

        :param db: 数据库会话
        :param business_id: 业务 ID
        :return:
        """
        return await self.select_models_order(db, sort_columns='sort', gen_business_id=business_id)

    async def create(self, db: AsyncSession, obj: CreateGenColumnParam, pd_type: str | None) -> None:
        """
        创建代码生成模型列

        :param db: 数据库会话
        :param obj: 创建代码生成模型列参数
        :param pd_type: Pydantic 类型
        :return:
        """
        await self.create_model(db, obj, pd_type=pd_type)

    async def bulk_create(self, db: AsyncSession, objs: list[CreateGenColumnInternalParam]) -> None:
        """
        批量创建代码生成模型列

        :param db: 数据库会话
        :param objs: 创建代码生成模型列参数列表
        :return:
        """
        await self.create_models(db, objs)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateGenColumnParam, pd_type: str | None) -> int:
        """
        更新代码生成模型列

        :param db: 数据库会话
        :param pk: 代码生成模型列 ID
        :param obj: 更新代码生成模型列参数
        :param pd_type: Pydantic 类型
        :return:
        """
        return await self.update_model(db, pk, obj, pd_type=pd_type)

    async def delete(self, db: AsyncSession, pk: int) -> int:
        """
        删除代码生成模型列

        :param db: 数据库会话
        :param pk: 代码生成模型列 ID
        :return:
        """
        return await self.delete_model(db, pk)


gen_column_dao: CRUDGenColumn = CRUDGenColumn(GenColumn)
