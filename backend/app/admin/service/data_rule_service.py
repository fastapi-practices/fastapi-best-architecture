from collections.abc import Sequence
from typing import Any

from sqlalchemy import Table
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.crud.crud_data_rule import data_rule_dao
from backend.app.admin.model import DataRule
from backend.app.admin.schema.data_rule import (
    CreateDataRuleParam,
    DeleteDataRuleParam,
    GetDataRuleColumnDetail,
    GetDataRuleTemplateVariableDetail,
    UpdateDataRuleParam,
)
from backend.app.admin.utils.cache import user_cache_manager
from backend.common.exception import errors
from backend.common.i18n import t
from backend.common.pagination import paging_data
from backend.common.security.permission import get_data_permission_models
from backend.core.conf import settings


class DataRuleService:
    """数据规则服务类"""

    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> DataRule:
        """
        获取数据规则详情

        :param db: 数据库会话
        :param pk: 规则 ID
        :return:
        """

        data_rule = await data_rule_dao.get(db, pk)
        if not data_rule:
            raise errors.NotFoundError(msg=t('error.data_rule.not_found'))
        return data_rule

    @staticmethod
    async def get_models() -> list[str]:
        """获取所有数据规则可用模型"""
        model_template_variables = [var['key'] for var in settings.DATA_PERMISSION_MODEL_TEMPLATE_VARIABLES]
        models = [
            m for m in list(get_data_permission_models().keys()) if m not in settings.DATA_PERMISSION_MODEL_EXCLUDE
        ]
        return model_template_variables + models

    @staticmethod
    async def get_value_template_variables() -> list[GetDataRuleTemplateVariableDetail]:
        """获取所有数据规则值可用模板变量"""
        return [GetDataRuleTemplateVariableDetail(**var) for var in settings.DATA_PERMISSION_TEMPLATE_VARIABLES]

    @staticmethod
    async def get_columns(model: str) -> list[GetDataRuleColumnDetail]:
        """
        获取数据规则可用模型的字段列表

        :param model: 模型名称
        :return:
        """
        column_template_variables = [
            GetDataRuleColumnDetail(key=var['key'], comment=var['comment'])
            for var in settings.DATA_PERMISSION_COLUMN_TEMPLATE_VARIABLES
        ]

        model_template_variable_keys = {var['key'] for var in settings.DATA_PERMISSION_MODEL_TEMPLATE_VARIABLES}
        if model in model_template_variable_keys:
            return column_template_variables

        available_models = get_data_permission_models()
        if model not in available_models:
            raise errors.NotFoundError(msg=t('error.data_rule.model_not_found'))
        model_ins = available_models[model]

        table = model_ins if isinstance(model_ins, Table) else model_ins.__table__
        model_columns = [
            GetDataRuleColumnDetail(key=column.key, comment=column.comment)
            for column in table.columns
            if column.key not in settings.DATA_PERMISSION_COLUMN_EXCLUDE
        ]
        return model_columns + column_template_variables

    @staticmethod
    async def get_list(*, db: AsyncSession, name: str | None) -> dict[str, Any]:
        """
        获取数据规则列表

        :param db: 数据库会话
        :param name: 规则名称
        :return:
        """
        data_rule_select = await data_rule_dao.get_select(name=name)
        return await paging_data(db, data_rule_select)

    @staticmethod
    async def get_all(*, db: AsyncSession) -> Sequence[DataRule]:
        """
        获取所有数据规则

        :param db: 数据库会话
        :return:
        """

        data_rules = await data_rule_dao.get_all(db)
        return data_rules

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateDataRuleParam) -> None:
        """
        创建数据规则

        :param db: 数据库会话
        :param obj: 规则创建参数
        :return:
        """
        data_rule = await data_rule_dao.get_by_name(db, obj.name)
        if data_rule:
            raise errors.ConflictError(msg=t('error.data_rule.exists'))
        await data_rule_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateDataRuleParam) -> int:
        """
        更新数据规则

        :param db: 数据库会话
        :param pk: 规则 ID
        :param obj: 规则更新参数
        :return:
        """
        data_rule = await data_rule_dao.get(db, pk)
        if not data_rule:
            raise errors.NotFoundError(msg=t('error.data_rule.not_found'))
        if data_rule.name != obj.name and await data_rule_dao.get_by_name(db, obj.name):
            raise errors.ConflictError(msg=t('error.data_rule.exists'))
        count = await data_rule_dao.update(db, pk, obj)
        await user_cache_manager.clear_by_data_rule_id(db, [pk])
        return count

    @staticmethod
    async def delete(*, db: AsyncSession, obj: DeleteDataRuleParam) -> int:
        """
        批量删除数据规则

        :param db: 数据库会话
        :param obj: 规则 ID 列表
        :return:
        """
        count = await data_rule_dao.delete(db, obj.pks)
        await user_cache_manager.clear_by_data_rule_id(db, obj.pks)
        return count


data_rule_service: DataRuleService = DataRuleService()
