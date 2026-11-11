from collections.abc import Sequence
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.exception import errors
from backend.common.pagination import paging_data
from backend.plugin.dict.crud.crud_dict_type import dict_type_dao
from backend.plugin.dict.model import DictType
from backend.plugin.dict.schema.dict_type import CreateDictTypeParam, DeleteDictTypeParam, UpdateDictTypeParam


class DictTypeService:
    """字典类型服务类"""

    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> DictType:
        """
        获取字典类型详情

        :param db: 数据库会话
        :param pk: 字典类型 ID
        :return:
        """
        dict_type = await dict_type_dao.get(db, pk)
        if not dict_type:
            raise errors.NotFoundError(msg='字典类型不存在')
        return dict_type

    @staticmethod
    async def get_all(*, db: AsyncSession) -> Sequence[DictType]:
        """
        获取所有字典类型

        :param db: 数据库会话
        :return:
        """
        dict_datas = await dict_type_dao.get_all(db)
        return dict_datas

    @staticmethod
    async def get_list(*, db: AsyncSession, name: str | None, code: str | None) -> dict[str, Any]:
        """
        获取字典类型列表

        :param db: 数据库会话
        :param name: 字典类型名称
        :param code: 字典类型编码
        :return:
        """
        dict_type_select = await dict_type_dao.get_select(name=name, code=code)
        return await paging_data(db, dict_type_select)

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateDictTypeParam) -> None:
        """
        创建字典类型

        :param db: 数据库会话
        :param obj: 字典类型创建参数
        :return:
        """
        dict_type = await dict_type_dao.get_by_code(db, obj.code)
        if dict_type:
            raise errors.ConflictError(msg='字典类型已存在')
        await dict_type_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateDictTypeParam) -> int:
        """
        更新字典类型

        :param db: 数据库会话
        :param pk: 字典类型 ID
        :param obj: 字典类型更新参数
        :return:
        """
        dict_type = await dict_type_dao.get(db, pk)
        if not dict_type:
            raise errors.NotFoundError(msg='字典类型不存在')
        if dict_type.code != obj.code and await dict_type_dao.get_by_code(db, obj.code):
            raise errors.ConflictError(msg='字典类型已存在')
        count = await dict_type_dao.update(db, pk, obj)
        return count

    @staticmethod
    async def delete(*, db: AsyncSession, obj: DeleteDictTypeParam) -> int:
        """
        批量删除字典类型

        :param db: 数据库会话
        :param obj: 字典类型 ID 列表
        :return:
        """
        count = await dict_type_dao.delete(db, obj.pks)
        return count


dict_type_service: DictTypeService = DictTypeService()
