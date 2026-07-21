from typing import TYPE_CHECKING, Any

from fastapi import Request
from sqlalchemy import Alias, ColumnElement, Table, and_, or_
from sqlalchemy.orm.util import AliasedClass
from sqlalchemy_crud_plus.types import Model

from backend.common.context import ctx
from backend.common.enums import RoleDataRuleExpressionType, RoleDataRuleOperatorType
from backend.common.exception import errors
from backend.core.conf import settings
from backend.utils.dynamic_import import get_all_models
from backend.utils.timezone import timezone

if TYPE_CHECKING:
    from backend.app.admin.model import DataRule


class RequestPermission:
    """
    请求权限验证器，用于角色菜单 RBAC 权限控制

    注意：
        使用此请求权限时，需要将 `Depends(RequestPermission('xxx'))` 在 `DependsRBAC` 之前设置，
        因为 FastAPI 当前版本的接口依赖注入按正序执行，意味着 RBAC 标识会在验证前被设置
    """

    def __init__(self, value: str) -> None:
        """
        初始化请求权限验证器

        :param value: 权限标识
        :return:
        """
        self.value = value

    async def __call__(self, request: Request) -> None:
        """
        验证请求权限

        :param request: FastAPI 请求对象
        :return:
        """
        if settings.RBAC_ROLE_MENU_MODE:
            if not isinstance(self.value, str):
                raise errors.ServerError

            # 设置权限标识到上下文
            ctx.permission = self.value


def get_data_permission_models() -> dict[str, object]:
    """获取所有可用于数据权限的模型"""
    return {getattr(model, '__name__', str(model)): model for model in get_all_models()}


def filter_data_permission(  # ruff:ignore[complex-structure]
    request: Request, *models: type[Model] | AliasedClass | Alias | Table
) -> ColumnElement[bool]:
    """
    过滤数据权限，控制用户可见数据范围

    使用场景：
        - 控制用户能看到哪些数据

    :param request: FastAPI 请求对象
    :param models: 需要应用数据权限的模型类
    :return:
    """
    # 超级管理员不过滤
    if request.user.is_superuser:
        return or_(1 == 1)

    # 角色未启用数据权限过滤
    for role in request.user.roles:
        if role.status and not role.is_filter_scopes:
            return or_(1 == 1)

    # 获取数据规则
    data_rules: set[DataRule] = set()
    for role in request.user.roles:
        if not role.status:
            continue
        for scope in role.scopes:
            if scope.status:
                data_rules.update(rule for rule in scope.rules if rule is not None)

    # 启用数据权限过滤，但没有已启用的数据权限
    if not data_rules:
        return or_(1 != 1)

    # 目标模型
    target_model_map = (
        {getattr(model, '__name__', str(model)): model for model in models} if models else get_data_permission_models()
    )

    # 字段模板变量映射
    column_template_resolvers = {
        var['key']: var['key'].strip('_') for var in settings.DATA_PERMISSION_COLUMN_TEMPLATE_VARIABLES
    }

    # 模板变量解析映射
    template_variable_keys = {var['key'] for var in settings.DATA_PERMISSION_TEMPLATE_VARIABLES}
    template_resolvers = {
        '${user_id}': request.user.id,
        '${dept_id}': request.user.dept_id,
        '${now}': timezone.now,
    }

    where_and_list = []
    where_or_list = []

    for data_rule in data_rules:
        if data_rule.model == '__ALL__':
            target_models = list(target_model_map.values())
        else:
            target_model = target_model_map.get(data_rule.model)
            target_models = [target_model] if target_model is not None else []

        for target_model in target_models:
            table = target_model if isinstance(target_model, Table) else target_model.__table__
            rule_column = column_template_resolvers.get(data_rule.column, data_rule.column)
            if rule_column not in table.columns.keys():
                continue
            if rule_column in settings.DATA_PERMISSION_COLUMN_EXCLUDE:
                continue

            # 构建过滤条件
            column_obj = (
                getattr(target_model, rule_column)
                if not isinstance(target_model, Table)
                else table.columns[rule_column]
            )
            column_type = table.columns[rule_column].type.python_type

            def cast_value(value: Any, _column_type: type = column_type) -> Any:
                """类型转换"""
                try:
                    if value in template_variable_keys:
                        return _column_type(template_resolvers[value])
                    return _column_type(value) if _column_type is not str else value
                except (ValueError, TypeError):
                    return value

            condition = None
            match data_rule.expression:
                case RoleDataRuleExpressionType.eq:
                    condition = column_obj == cast_value(data_rule.value)
                case RoleDataRuleExpressionType.ne:
                    condition = column_obj != cast_value(data_rule.value)
                case RoleDataRuleExpressionType.gt:
                    condition = column_obj > cast_value(data_rule.value)
                case RoleDataRuleExpressionType.ge:
                    condition = column_obj >= cast_value(data_rule.value)
                case RoleDataRuleExpressionType.lt:
                    condition = column_obj < cast_value(data_rule.value)
                case RoleDataRuleExpressionType.le:
                    condition = column_obj <= cast_value(data_rule.value)
                case RoleDataRuleExpressionType.in_:
                    values = [cast_value(v.strip()) for v in data_rule.value.split(',')]
                    condition = column_obj.in_(values)
                case RoleDataRuleExpressionType.not_in:
                    values = [cast_value(v.strip()) for v in data_rule.value.split(',')]
                    condition = column_obj.not_in(values)

            # 根据运算符添加到对应列表
            if condition is not None:
                match data_rule.operator:
                    case RoleDataRuleOperatorType.AND:
                        where_and_list.append(condition)
                    case RoleDataRuleOperatorType.OR:
                        where_or_list.append(condition)

    # 组合所有条件
    where_list = []
    if where_and_list:
        where_list.append(and_(*where_and_list))
    if where_or_list:
        where_list.append(or_(*where_or_list))

    return or_(*where_list) if where_list else or_(1 == 1)


# 此函数是为了简化调用方式，但目前无法正常工作: https://github.com/fastapi/fastapi/discussions/14438
# def DataPermissionFilter(*models: type[Model] | AliasedClass | Alias | Table) -> type[ColumnElement[bool]]:
#     """
#     指定模型的数据权限过滤器
#
#     :param models: 模型类（可选，支持多个）
#     :return:
#     """
#     return Annotated[ColumnElement[bool], Depends(partial(filter_data_permission, *models))]


class DataPermissionFilter:
    """指定模型的数据权限过滤器"""

    def __init__(self, *models: type[Model] | AliasedClass | Alias | Table) -> None:
        self.models = models

    async def __call__(self, request: Request) -> ColumnElement[bool]:
        return filter_data_permission(request, *self.models)
