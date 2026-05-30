from collections.abc import Sequence
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.cache.decorator import cache_invalidate, cached
from backend.common.exception import errors
from backend.common.pagination import paging_data
from backend.core.conf import settings
from backend.plugin.dict.crud.crud_dict_data import dict_data_dao
from backend.plugin.dict.crud.crud_dict_type import dict_type_dao
from backend.plugin.dict.model import DictData
from backend.plugin.dict.schema.dict_data import CreateDictDataParam, DeleteDictDataParam, UpdateDictDataParam


class DictDataService:
    """字典数据服务类"""

    @staticmethod
    @cached(settings.CACHE_DICT_REDIS_PREFIX, key='pk')
    async def get(*, db: AsyncSession, pk: int) -> DictData:
        """
        获取字典数据详情

        :param db: 数据库会话
        :param pk: 字典数据 ID
        :return:
        """
        dict_data = await dict_data_dao.get(db, pk)
        if not dict_data:
            raise errors.NotFoundError(msg='字典数据不存在')
        return dict_data

    @staticmethod
    @cached(
        settings.CACHE_DICT_REDIS_PREFIX,
        key_builder=lambda *, db, code: f'type:{code}',
    )
    async def get_by_type_code(*, db: AsyncSession, code: str) -> Sequence[DictData]:
        """
        获取字典数据详情

        :param db: 数据库会话
        :param code: 字典类型编码
        :return:
        """
        dict_datas = await dict_data_dao.get_by_type_code(db, code)
        if not dict_datas:
            raise errors.NotFoundError(msg='字典数据不存在')
        return dict_datas

    @staticmethod
    async def get_all(*, db: AsyncSession) -> Sequence[DictData]:
        """
        获取所有字典数据

        :param db: 数据库会话
        :return:
        """
        dict_datas = await dict_data_dao.get_all(db)
        return dict_datas

    @staticmethod
    async def get_list(
        *,
        db: AsyncSession,
        type_code: str | None,
        label: str | None,
        value: str | None,
        status: int | None,
        type_id: int | None,
    ) -> dict[str, Any]:
        """
        获取字典数据列表

        :param db: 数据库会话
        :param type_code: 字典类型编码
        :param label: 字典数据标签
        :param value: 字典数据键值
        :param status: 状态
        :param type_id: 字典类型 ID
        :return:
        """
        dict_data_select = await dict_data_dao.get_select(
            type_code=type_code,
            label=label,
            value=value,
            status=status,
            type_id=type_id,
        )
        return await paging_data(db, dict_data_select)

    @staticmethod
    @cache_invalidate(settings.CACHE_DICT_REDIS_PREFIX)
    async def create(*, db: AsyncSession, obj: CreateDictDataParam) -> None:
        """
        创建字典数据

        :param db: 数据库会话
        :param obj: 字典数据创建参数
        :return:
        """
        dict_type = await dict_type_dao.get(db, obj.type_id)
        if not dict_type:
            raise errors.NotFoundError(msg='字典类型不存在')
        dict_data = await dict_data_dao.get_by_label_and_type_code(db, obj.label, dict_type.code)
        if dict_data:
            raise errors.ConflictError(msg='字典数据已存在')
        await dict_data_dao.create(db, obj, dict_type.code)

    @staticmethod
    @cache_invalidate(settings.CACHE_DICT_REDIS_PREFIX)
    async def update(*, db: AsyncSession, pk: int, obj: UpdateDictDataParam) -> int:
        """
        更新字典数据

        :param db: 数据库会话
        :param pk: 字典数据 ID
        :param obj: 字典数据更新参数
        :return:
        """
        dict_data = await dict_data_dao.get(db, pk)
        if not dict_data:
            raise errors.NotFoundError(msg='字典数据不存在')
        dict_type = await dict_type_dao.get(db, obj.type_id)
        if not dict_type:
            raise errors.NotFoundError(msg='字典类型不存在')
        if dict_data.label != obj.label or dict_data.type_code != dict_type.code:
            new_dict_data = await dict_data_dao.get_by_label_and_type_code(db, obj.label, dict_type.code)
            if new_dict_data and new_dict_data.id != pk:
                raise errors.ConflictError(msg='字典数据已存在')
        count = await dict_data_dao.update(db, pk, obj, dict_type.code)
        return count

    @staticmethod
    @cache_invalidate(settings.CACHE_DICT_REDIS_PREFIX)
    async def delete(*, db: AsyncSession, obj: DeleteDictDataParam) -> int:
        """
        批量删除字典数据

        :param db: 数据库会话
        :param obj: 字典数据 ID 列表
        :return:
        """
        count = await dict_data_dao.delete(db, obj.pks)
        return count


dict_data_service: DictDataService = DictDataService()
