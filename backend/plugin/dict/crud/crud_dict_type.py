from collections.abc import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.plugin.dict.crud.crud_dict_data import dict_data_dao
from backend.plugin.dict.model import DictType
from backend.plugin.dict.schema.dict_type import CreateDictTypeParam, UpdateDictTypeParam
from backend.utils.timezone import timezone


class CRUDDictType(CRUDPlus[DictType]):
    """字典类型数据库操作类"""

    async def get(self, db: AsyncSession, pk: int) -> DictType | None:
        """
        获取字典类型详情

        :param db: 数据库会话
        :param pk: 字典类型 ID
        :return:
        """
        return await self.select_model(db, pk, deleted=0)

    async def get_all(self, db: AsyncSession) -> Sequence[DictType]:
        """
        获取所有字典类型

        :param db: 数据库会话
        :return:
        """
        return await self.select_models(db, deleted=0)

    async def get_select(self, name: str | None, code: str | None) -> Select:
        """
        获取字典类型列表查询表达式

        :param name: 字典类型名称
        :param code: 字典类型编码
        :return:
        """
        filters = {'deleted': 0}

        if name is not None:
            filters['name__like'] = f'%{name}%'
        if code is not None:
            filters['code__like'] = f'%{code}%'

        return await self.select_order('id', 'desc', **filters)

    async def get_by_code(self, db: AsyncSession, code: str) -> DictType | None:
        """
        通过编码获取字典类型

        :param db: 数据库会话
        :param code: 字典编码
        :return:
        """
        return await self.select_model_by_column(db, code=code, deleted=0)

    async def create(self, db: AsyncSession, obj: CreateDictTypeParam) -> None:
        """
        创建字典类型

        :param db: 数据库会话
        :param obj: 创建字典类型参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, pk: int, obj: UpdateDictTypeParam) -> int:
        """
        更新字典类型

        :param db: 数据库会话
        :param pk: 字典类型 ID
        :param obj: 更新字典类型参数
        :return:
        """
        return await self.update_model_by_column(db, obj, id=pk, deleted=0)

    async def delete(self, db: AsyncSession, pks: list[int]) -> int:
        """
        批量删除字典类型

        :param db: 数据库会话
        :param pks: 字典类型 ID 列表
        :return:
        """
        await dict_data_dao.delete_by_type_id(db, pks)
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


dict_type_dao: CRUDDictType = CRUDDictType(DictType)
