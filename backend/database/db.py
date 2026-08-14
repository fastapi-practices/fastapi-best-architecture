import sys

from collections.abc import AsyncGenerator, Mapping
from functools import partial
from typing import Annotated, Any, TypeAlias
from uuid import uuid4

from fastapi import Depends
from sqlalchemy import URL, Engine, event
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session

from backend.common.enums import DataBaseType
from backend.common.log import log
from backend.common.model import MappedBase
from backend.common.observability.prometheus.sqlalchemy import observe_sqlalchemy_pool_connections
from backend.core.conf import settings


def get_database_url(*, unittest: bool = False, with_database: bool = True) -> URL:
    """
    创建数据库链接

    :param unittest: 是否用于单元测试
    :param with_database: 是否包含数据库名（创建数据库时不需要）
    :return:
    """
    if with_database:
        database = settings.DATABASE_SCHEMA if not unittest else f'{settings.DATABASE_SCHEMA}_test'
    else:
        database = None if DataBaseType.mysql == settings.DATABASE_TYPE else 'postgres'

    url = URL.create(
        drivername='mysql+asyncmy' if DataBaseType.mysql == settings.DATABASE_TYPE else 'postgresql+asyncpg',
        username=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        database=database,
    )
    if DataBaseType.mysql == settings.DATABASE_TYPE and with_database:
        url = url.update_query_dict({'charset': settings.DATABASE_CHARSET})
    return url


def create_database_async_engine(url: str | URL) -> AsyncEngine:
    """
    创建数据库异步引擎

    :param url: 数据库连接地址
    :return:
    """
    try:
        return create_async_engine(
            url,
            echo=settings.DATABASE_ECHO,
            echo_pool=settings.DATABASE_POOL_ECHO,
            future=True,
            # 中等并发
            pool_size=10,  # 低：- 高：+
            max_overflow=20,  # 低：- 高：+
            pool_timeout=30,  # 低：+ 高：-
            pool_recycle=3600,  # 低：+ 高：-
            pool_pre_ping=True,  # 低：False 高：True
            pool_use_lifo=False,  # 低：False 高：True
        )
    except Exception as e:
        log.error(f'数据库连接失败 {e}')
        sys.exit()


class DatabaseSession(Session):
    """数据库数据源会话"""

    def __init__(
        self,
        *,
        source: str = 'default',
        source_binds: Mapping[str, Engine] | None = None,
        **kwargs: Any,
    ) -> None:
        source_binds = source_binds or {}
        try:
            engine = source_binds[source]
        except KeyError as e:
            raise ValueError(f'未知数据库数据源: {source}') from e

        kwargs['bind'] = engine
        kwargs['binds'] = {MappedBase: engine}
        super().__init__(**kwargs)


def create_database_async_session(
    async_engine: AsyncEngine,
    *,
    source_binds: Mapping[str, AsyncEngine] | None = None,
) -> async_sessionmaker[AsyncSession | Any]:
    """创建支持命名数据源的数据库异步会话"""
    async_binds = dict(source_binds or {})
    async_binds.setdefault('default', async_engine)
    sync_binds = {source: bind.sync_engine for source, bind in async_binds.items()}
    return async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        sync_session_class=DatabaseSession,
        source='default',
        source_binds=sync_binds,
        autoflush=False,  # 禁用自动刷新
        expire_on_commit=False,  # 禁用提交时过期
    )


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取默认数据源会话"""
    async with async_db_session(source='default') as session:
        yield session


async def get_db_transaction() -> AsyncGenerator[AsyncSession, None]:
    """获取默认数据源事务会话"""
    async with async_db_session(source='default').begin() as session:
        yield session


async def create_tables() -> None:
    """创建数据库表"""
    async with async_engine.begin() as coon:
        await coon.run_sync(MappedBase.metadata.create_all)


async def drop_tables() -> None:
    """丢弃数据库表"""
    async with async_engine.begin() as conn:
        await conn.run_sync(MappedBase.metadata.drop_all)


def uuid4_str() -> str:
    """数据库引擎 UUID 类型兼容性解决方案"""
    return str(uuid4())


# SQLA 异步引擎和会话
async_engine = create_database_async_engine(get_database_url())
_database_engines: dict[str, AsyncEngine] = {'default': async_engine}
for source, url in settings.DATABASE_SOURCES.items():
    if not source or source == 'default':
        raise ValueError('DATABASE_SOURCES 数据源名称不能为空且不能为 default')
    _database_engines[source] = create_database_async_engine(url)

async_db_session = create_database_async_session(async_engine, source_binds=_database_engines)


def get_database_engines() -> Mapping[str, AsyncEngine]:
    """获取所有数据库引擎"""
    return _database_engines


async def dispose_database() -> None:
    """释放所有数据库连接池"""
    for engine in _database_engines.values():
        await engine.dispose()


# SQLA 连接池指标监听
for source, engine in _database_engines.items():
    event.listen(
        engine.sync_engine.pool,
        'connect',
        partial(observe_sqlalchemy_pool_connections, pool=engine.sync_engine.pool, source=source),
    )
    event.listen(
        engine.sync_engine.pool,
        'checkout',
        partial(observe_sqlalchemy_pool_connections, pool=engine.sync_engine.pool, source=source),
    )
    event.listen(
        engine.sync_engine.pool,
        'checkin',
        partial(observe_sqlalchemy_pool_connections, pool=engine.sync_engine.pool, source=source),
    )

# Session 类型别名
CurrentSession: TypeAlias = Annotated[AsyncSession, Depends(get_db)]
CurrentSessionTransaction: TypeAlias = Annotated[AsyncSession, Depends(get_db_transaction)]
