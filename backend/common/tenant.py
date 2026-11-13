from typing import Any, Protocol

import sqlalchemy as sa

from sqlalchemy import BigInteger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column
from starlette_context.errors import ContextDoesNotExistError

from backend.common.context import ctx
from backend.core.conf import settings


def current_tenant_id() -> int:
    """
    当前请求所属租户 ID

    未启用租户时返回默认租户，未取到租户上下文时同样回落到默认租户，
    后台任务等没有请求上下文的场景按默认租户处理

    :return:
    """
    if not settings.TENANT_ENABLED:
        return settings.TENANT_DEFAULT_ID
    try:
        tenant_id = ctx.get('tenant_id')
    except ContextDoesNotExistError:
        tenant_id = None
    return tenant_id if tenant_id is not None else settings.TENANT_DEFAULT_ID


def inject_tenant(obj: dict[str, Any]) -> dict[str, Any]:
    """
    向待写入的数据注入租户 ID

    未启用租户时原样返回，ORM 插入由监听器兜底，本函数用于 Core 批量插入

    :param obj: 待写入的数据
    :return:
    """
    if not settings.TENANT_ENABLED:
        return obj
    if 'tenant_id' not in obj:
        obj['tenant_id'] = current_tenant_id()
    return obj


def tenant_columns() -> list[sa.Column]:
    """租户列定义，未启用租户时为空"""
    if not settings.TENANT_ENABLED:
        return []
    return [sa.Column('tenant_id', BigInteger, nullable=False, index=True, comment='租户ID')]


def tenant_unique_columns(*columns: str) -> tuple[str, ...]:
    """
    唯一约束列

    开启租户时按租户维度隔离，约束名保持不变，避免同一约束出现两套命名

    :param columns: 业务列
    :return:
    """
    if settings.TENANT_ENABLED:
        return (*columns, 'tenant_id', 'deleted')
    return (*columns, 'deleted')


class TenantMixin(MappedAsDataclass):
    """租户 Mixin 数据类"""

    if settings.TENANT_ENABLED:
        tenant_id: Mapped[int] = mapped_column(
            BigInteger,
            init=False,
            nullable=False,
            index=True,
            sort_order=997,
            comment='租户ID',
        )


class TenantChecker(Protocol):
    """租户状态校验器协议，由持有租户体系的应用实现，并在应用启动时注册"""

    async def __call__(self, *, db: AsyncSession, tenant_id: int) -> None:
        """
        校验租户状态

        :param db: 数据库会话
        :param tenant_id: 租户 ID
        :return:
        """


_tenant_checker: TenantChecker | None = None


def register_tenant_checker(checker: TenantChecker) -> None:
    """
    注册租户状态校验器

    :param checker: 租户状态校验器
    :return:
    """
    global _tenant_checker
    _tenant_checker = checker


async def check_tenant_status(*, db: AsyncSession, tenant_id: int) -> None:
    """
    校验租户状态

    未启用租户时直接返回，未注册校验器时说明应用未正确装配租户能力

    :param db: 数据库会话
    :param tenant_id: 租户 ID
    :return:
    """
    if not settings.TENANT_ENABLED:
        return
    if _tenant_checker is None:
        raise RuntimeError('租户校验器未注册，请在应用启动时调用 register_tenant_checker')
    await _tenant_checker(db=db, tenant_id=tenant_id)
