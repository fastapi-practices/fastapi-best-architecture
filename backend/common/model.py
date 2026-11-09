from datetime import datetime
from typing import Annotated

import sqlalchemy as sa

from sqlalchemy import BigInteger
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, declared_attr, mapped_column

from backend.common.enums import PrimaryKeyType
from backend.core.conf import settings
from backend.utils.snowflake import snowflake
from backend.utils.timezone import timezone

# 通用 Mapped 类型主键, 需手动添加，参考以下使用方式
# MappedBase -> id: Mapped[id_key]
# DataClassBase && Base -> id: Mapped[id_key] = mapped_column(init=False)
id_key = Annotated[
    int,
    mapped_column(
        BigInteger,
        primary_key=True,
        unique=True,
        index=True,
        autoincrement=True,
        sort_order=-999,
        comment='主键 ID',
    )
    if PrimaryKeyType.autoincrement == settings.DATABASE_PK_MODE
    # 雪花算法 Mapped 类型主键
    # 详情：https://fastapi-practices.github.io/fastapi_best_architecture_docs/backend/reference/pk.html
    else mapped_column(
        BigInteger,
        primary_key=True,
        unique=True,
        index=True,
        default=snowflake.generate,
        sort_order=-999,
        comment='雪花算法主键 ID',
    ),
]


# Mixin: 一种面向对象编程概念, 使结构变得更加清晰, `Wiki <https://en.wikipedia.org/wiki/Mixin/>`__
class UserMixin(MappedAsDataclass):
    """用户 Mixin 数据类"""

    created_by: Mapped[int] = mapped_column(sort_order=998, comment='创建者')
    updated_by: Mapped[int | None] = mapped_column(init=False, default=None, sort_order=998, comment='修改者')


class DateTimeMixin(MappedAsDataclass):
    """日期时间 Mixin 数据类"""

    created_time: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=True),
        init=False,
        default_factory=timezone.now,
        sort_order=999,
        comment='创建时间',
    )
    updated_time: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True),
        init=False,
        onupdate=timezone.now,
        sort_order=999,
        comment='更新时间',
    )


class LogicalDeleteMixin(MappedAsDataclass):
    """逻辑删除 Mixin 数据类"""

    deleted: Mapped[int] = mapped_column(
        BigInteger,
        init=False,
        default=0,
        server_default='0',
        sort_order=999,
        comment='是否已删除（0：否；id：是）',
    )
    deleted_time: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True),
        init=False,
        default=None,
        sort_order=999,
        comment='删除时间',
    )


class MappedBase(AsyncAttrs, DeclarativeBase):
    """
    声明式基类, 作为所有基类或数据模型类的父类而存在

    `AsyncAttrs <https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncAttrs>`__

    `DeclarativeBase <https://docs.sqlalchemy.org/en/20/orm/declarative_config.html>`__

    `mapped_column() <https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column>`__
    """

    @declared_attr.directive
    def __tablename__(self) -> str:
        """生成表名"""
        return self.__name__.lower()

    @declared_attr.directive
    def __table_args__(self) -> dict:
        """表配置"""
        return {'comment': self.__doc__ or ''}


class DataClassBase(MappedAsDataclass, MappedBase):
    """
    声明性数据类基类, 带有数据类集成, 允许使用更高级配置, 但你必须注意它的一些特性, 尤其是和 DeclarativeBase 一起使用时

    `MappedAsDataclass <https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses>`__
    """

    __abstract__ = True


class Base(DataClassBase, DateTimeMixin, LogicalDeleteMixin):
    """
    声明性数据类基类, 带有数据类集成, 并包含 MiXin 数据类基础表结构
    """

    __abstract__ = True
