import asyncio
import re
import secrets
import subprocess
import sys

from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Final, Literal

import anyio
import cappa
import granian

from cappa.output import error_format
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table
from rich.text import Text
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession
from starlette.concurrency import run_in_threadpool
from watchfiles import Change, PythonFilter

from backend import __version__
from backend.common.enums import DataBaseType, PrimaryKeyType
from backend.common.exception.errors import BaseExceptionError
from backend.common.model import MappedBase
from backend.core.conf import settings
from backend.core.path_conf import (
    BASE_PATH,
    ENV_EXAMPLE_FILE_PATH,
    ENV_FILE_PATH,
    LOCALE_DIR,
    MYSQL_SCRIPT_DIR,
    PLUGIN_DIR,
    POSTGRESQL_SCRIPT_DIR,
    RELOAD_LOCK_FILE,
)
from backend.database.db import (
    async_db_session,
    create_database_async_engine,
    create_database_async_session,
    get_database_url,
)
from backend.database.redis import RedisCli, redis_client
from backend.plugin.core import (
    get_plugins,
    get_required_plugins,
)
from backend.plugin.installer import install_git_frontend_plugin, install_git_plugin, install_zip_plugin, zip_plugin
from backend.plugin.installer import remove_plugin as _remove_plugin
from backend.plugin.requirements import install_requirements_async, uninstall_requirements_async
from backend.plugin.sql import build_sql_filename, get_plugin_destroy_sql, get_plugin_sql
from backend.utils.console import console
from backend.utils.dynamic_import import import_module_cached
from backend.utils.sql_parser import parse_sql_script
from backend.utils.timezone import timezone

_OUTPUT_HELP: Final = "\n更多信息，尝试 '[cyan]--help[/]'"


class CustomReloadFilter(PythonFilter):
    """自定义重载过滤器"""

    def __init__(self) -> None:
        self.extra_extensions = ('.json', '.yaml', '.yml')
        super().__init__(extra_extensions=self.extra_extensions)

    def __call__(self, change: Change, path: str) -> bool:
        if RELOAD_LOCK_FILE.exists():
            return False

        file_path = Path(path).resolve()
        if file_path.suffix in self.extra_extensions and not file_path.is_relative_to(LOCALE_DIR.resolve()):
            return False

        return super().__call__(change, path)


def setup_env_file() -> bool:
    """交互式配置并生成 .env 环境变量文件"""
    if not ENV_EXAMPLE_FILE_PATH.exists():
        console.caution('.env.example 文件不存在')
        return False

    try:
        env_content = Path(ENV_EXAMPLE_FILE_PATH).read_text(encoding='utf-8')
        console.note('配置数据库连接信息...')
        db_type = Prompt.ask('数据库类型', choices=['mysql', 'postgresql'], default='postgresql')
        db_host = Prompt.ask('数据库主机', default='127.0.0.1')
        db_port = Prompt.ask('数据库端口', default='5432' if db_type == 'postgresql' else '3306')
        db_user = Prompt.ask('数据库用户名', default='postgres' if db_type == 'postgresql' else 'root')
        db_password = Prompt.ask('数据库密码', password=True, default='123456')

        console.note('配置 Redis 连接信息...')
        redis_host = Prompt.ask('Redis 主机', default='127.0.0.1')
        redis_port = Prompt.ask('Redis 端口', default='6379')
        redis_password = Prompt.ask('Redis 密码（留空表示无密码）', password=True, default='')
        redis_db = Prompt.ask('Redis 数据库编号', default='0')

        console.info('生成 Token 密钥...')
        token_secret = secrets.token_urlsafe(32)

        console.info('写入 .env 文件...')
        env_content = env_content.replace("DATABASE_TYPE='postgresql'", f"DATABASE_TYPE='{db_type}'")
        settings.DATABASE_TYPE = db_type
        env_content = env_content.replace("DATABASE_HOST='127.0.0.1'", f"DATABASE_HOST='{db_host}'")
        settings.DATABASE_HOST = db_host
        env_content = env_content.replace('DATABASE_PORT=5432', f'DATABASE_PORT={db_port}')
        settings.DATABASE_PORT = db_port
        env_content = env_content.replace("DATABASE_USER='postgres'", f"DATABASE_USER='{db_user}'")
        settings.DATABASE_USER = db_user
        env_content = env_content.replace("DATABASE_PASSWORD='123456'", f"DATABASE_PASSWORD='{db_password}'")
        settings.DATABASE_PASSWORD = db_password
        env_content = env_content.replace("REDIS_HOST='127.0.0.1'", f"REDIS_HOST='{redis_host}'")
        settings.REDIS_HOST = redis_host
        env_content = env_content.replace('REDIS_PORT=6379', f'REDIS_PORT={redis_port}')
        settings.REDIS_PORT = redis_port
        env_content = env_content.replace("REDIS_PASSWORD=''", f"REDIS_PASSWORD='{redis_password}'")
        settings.REDIS_PASSWORD = redis_password
        env_content = env_content.replace('REDIS_DATABASE=0', f'REDIS_DATABASE={redis_db}')
        settings.REDIS_DATABASE = redis_db
        env_content = re.sub(r"TOKEN_SECRET_KEY='[^']*'", f"TOKEN_SECRET_KEY='{token_secret}'", env_content)
        settings.TOKEN_SECRET_KEY = token_secret

        Path(ENV_FILE_PATH).write_text(env_content, encoding='utf-8')
        console.tip('.env 文件创建成功')
    except Exception as e:
        console.caution(f'.env 文件创建失败: {e}')
        return False
    else:
        return True


async def create_database(conn: AsyncConnection) -> bool:
    """创建或重建数据库"""
    try:
        terminate_sql = None
        if DataBaseType.mysql == settings.DATABASE_TYPE:
            check_sql = f"SHOW DATABASES LIKE '{settings.DATABASE_SCHEMA}'"
            drop_sql = f'DROP DATABASE IF EXISTS `{settings.DATABASE_SCHEMA}`'
            create_sql = (
                f'CREATE DATABASE `{settings.DATABASE_SCHEMA}` CHARACTER SET {settings.DATABASE_CHARSET} '
                f'COLLATE {settings.DATABASE_CHARSET}_unicode_ci'
            )
        else:
            check_sql = f"SELECT 1 FROM pg_database WHERE datname = '{settings.DATABASE_SCHEMA}'"
            drop_sql = f'DROP DATABASE IF EXISTS {settings.DATABASE_SCHEMA}'
            create_sql = f'CREATE DATABASE {settings.DATABASE_SCHEMA}'
            terminate_sql = (
                f'SELECT pg_terminate_backend(pid) FROM pg_stat_activity '
                f"WHERE datname = '{settings.DATABASE_SCHEMA}' AND pid <> pg_backend_pid()"
            )

        result = await conn.execute(text(check_sql))
        exists = result.fetchone() is not None
        console.note(f'重建 {settings.DATABASE_SCHEMA} 数据库...')
        if exists:
            if terminate_sql:
                await conn.execute(text(terminate_sql))
            await conn.execute(text(drop_sql))
        await conn.execute(text(create_sql))
        console.tip('数据库创建成功')
    except Exception as e:
        console.caution(f'数据库创建失败: {e}')
        return False
    else:
        return True


def _build_db_config_panel_content() -> Text:
    """构建数据库配置面板内容"""
    panel_content = Text()
    panel_content.append('【数据库配置】', style='bold green')
    panel_content.append('\n\n  • 类型: ')
    panel_content.append(f'{settings.DATABASE_TYPE}', style='yellow')
    panel_content.append('\n  • 主机：')
    panel_content.append(f'{settings.DATABASE_HOST}:{settings.DATABASE_PORT}', style='yellow')
    panel_content.append('\n  • 数据库：')
    panel_content.append(f'{settings.DATABASE_SCHEMA}', style='yellow')
    panel_content.append('\n  • 主键模式：')
    panel_content.append(f'{settings.DATABASE_PK_MODE}', style='yellow')
    return panel_content


async def auto_init() -> None:
    """自动化初始化流程"""
    console.print('\n[bold cyan]步骤 1/3:[/] 配置环境变量', style='bold')
    panel_content = Text()
    panel_content.append('【环境变量配置】', style='bold green')
    panel_content.append('\n\n  • 数据库连接信息')
    panel_content.append('\n  • Redis 连接信息')
    panel_content.append('\n  • Token 密钥（自动生成）')

    console.print(Panel(panel_content, title=f'fba (v{__version__}) - 环境变量', border_style='cyan', padding=(1, 2)))
    if not setup_env_file():
        raise cappa.Exit('.env 文件配置失败', code=1)

    console.print('\n[bold cyan]步骤 2/3:[/] 数据库创建', style='bold')
    panel_content = _build_db_config_panel_content()

    console.print(Panel(panel_content, title=f'fba (v{__version__}) - 数据库', border_style='cyan', padding=(1, 2)))
    ok = Prompt.ask('即将[red]新建/重建数据库[/red]，确认继续吗？', choices=['y', 'n'], default='n')

    if ok.lower() == 'y':
        async_init_engine = create_database_async_engine(get_database_url(with_database=False))
        async with async_init_engine.connect() as conn:
            await conn.execution_options(isolation_level='AUTOCOMMIT')
            if not await create_database(conn):
                raise cappa.Exit('数据库创建失败', code=1)
    else:
        console.warning('已取消数据库操作')

    console.print('\n[bold cyan]步骤 3/3:[/] 初始化数据库表和数据', style='bold')
    async_init_engine = create_database_async_engine(get_database_url())
    async_init_db_session = create_database_async_session(async_init_engine)
    redis_init_client = RedisCli(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=settings.REDIS_DATABASE,
    )
    await redis_init_client.init()
    async with async_init_db_session.begin() as db:
        await init(db, redis_init_client)


async def init(db: AsyncSession, redis: RedisCli) -> None:
    """交互式初始化数据库表结构和数据"""
    panel_content = _build_db_config_panel_content()
    pk_details = panel_content.from_markup(
        '[link=https://fastapi-practices.github.io/fastapi_best_architecture_docs/backend/reference/pk.html]（了解详情）[/]'
    )
    panel_content.append(pk_details)
    panel_content.append('\n\n【Redis 配置】', style='bold green')
    panel_content.append('\n\n  • 主机：')
    panel_content.append(f'{settings.REDIS_HOST}:{settings.REDIS_PORT}', style='yellow')
    panel_content.append('\n  • 数据库：')
    panel_content.append(f'{settings.REDIS_DATABASE}', style='yellow')
    plugins = get_plugins()
    panel_content.append('\n\n【已安装插件】', style='bold green')
    panel_content.append('\n\n  • ')
    if plugins:
        panel_content.append(f'{", ".join(plugins)}', style='yellow')
    else:
        panel_content.append('无', style='dim')

    console.print(Panel(panel_content, title=f'fba (v{__version__}) - 初始化', border_style='cyan', padding=(1, 2)))
    ok = Prompt.ask(
        '即将[red]新建/重建数据库表[/red]并[red]执行所有数据库脚本[/red]，确认继续吗？', choices=['y', 'n'], default='n'
    )

    if ok.lower() == 'y':
        try:
            console.note('清理 Redis 缓存')
            for prefix in [
                settings.JWT_USER_REDIS_PREFIX,
                settings.TOKEN_EXTRA_INFO_REDIS_PREFIX,
                settings.TOKEN_REDIS_PREFIX,
                settings.TOKEN_REFRESH_REDIS_PREFIX,
            ]:
                await redis.delete_prefix(prefix)

            console.note('重建数据库表')
            conn = await db.connection()
            await conn.run_sync(MappedBase.metadata.drop_all)
            await conn.run_sync(MappedBase.metadata.create_all)

            console.note('执行 SQL 脚本')
            sql_scripts = await get_sql_scripts()
            for sql_script in sql_scripts:
                console.note(f'正在执行：{sql_script}')
                await execute_sql_scripts(db, sql_script, is_init=True)

            console.tip('初始化成功')
            console.print('\n快试试 [bold cyan]fba run[/bold cyan] 启动服务吧~')
        except Exception as e:
            raise cappa.Exit(f'初始化失败：{e}', code=1)
    else:
        console.warning('已取消初始化操作')


def run(host: str, port: int, reload: bool, workers: int) -> None:  # noqa: FBT001
    """启动 API 服务"""
    url = f'http://{host}:{port}'
    docs_url = url + settings.FASTAPI_DOCS_URL
    redoc_url = url + settings.FASTAPI_REDOC_URL
    openapi_url = url + (settings.FASTAPI_OPENAPI_URL or '')

    panel_content = Text()
    panel_content.append('Python 版本：', style='bold cyan')
    panel_content.append(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}', style='white')

    panel_content.append('\nAPI 请求地址: ', style='bold cyan')
    panel_content.append(f'{url}{settings.FASTAPI_API_V1_PATH}', style='blue')

    panel_content.append('\n\n环境模式：', style='bold green')
    env_style = 'yellow' if settings.ENVIRONMENT == 'dev' else 'green'
    panel_content.append(f'{settings.ENVIRONMENT.upper()}', style=env_style)

    plugins = get_plugins()
    panel_content.append('\n已安装插件：', style='bold green')
    if plugins:
        panel_content.append(f'{", ".join(plugins)}', style='yellow')
    else:
        panel_content.append('无', style='white')

    if settings.ENVIRONMENT == 'dev':
        panel_content.append(f'\n\n📖 Swagger 文档: {docs_url}', style='bold magenta')
        panel_content.append(f'\n📚 Redoc   文档: {redoc_url}', style='bold magenta')
        panel_content.append(f'\n📡 OpenAPI JSON: {openapi_url}', style='bold magenta')

    panel_content.append('\n🌐 架构官方文档: ', style='bold magenta')
    panel_content.append('https://fastapi-practices.github.io/fastapi_best_architecture_docs/')

    console.print(Panel(panel_content, title=f'fba (v{__version__})', border_style='purple', padding=(1, 2)))
    granian.Granian(
        target='backend.main:app',
        interface='asgi',
        address=host,
        port=port,
        reload=not reload,
        reload_filter=CustomReloadFilter,
        workers=workers,
    ).serve()


def run_celery_worker(log_level: Literal['info', 'debug']) -> None:
    """启动 Celery worker 服务"""
    try:
        subprocess.run(['celery', '-A', 'backend.app.task.celery', 'worker', '-l', f'{log_level}', '-P', 'gevent'])
    except KeyboardInterrupt:
        pass


def run_celery_beat(log_level: Literal['info', 'debug']) -> None:
    """启动 Celery beat 定时任务服务"""
    try:
        subprocess.run(['celery', '-A', 'backend.app.task.celery', 'beat', '-l', f'{log_level}'])
    except KeyboardInterrupt:
        pass


def run_celery_flower(port: int, basic_auth: str) -> None:
    """启动 Celery flower 监控服务"""
    try:
        subprocess.run([
            'celery',
            '-A',
            'backend.app.task.celery',
            'flower',
            f'--port={port}',
            f'--basic-auth={basic_auth}',
        ])
    except KeyboardInterrupt:
        pass


async def install_plugin(  # noqa: C901
    path: str | None,
    repo_url: str | None,
    frontend: bool,  # noqa: FBT001
    no_sql: bool,  # noqa: FBT001
    db_type: DataBaseType,
    pk_type: PrimaryKeyType,
) -> None:
    """安装插件"""
    if settings.ENVIRONMENT != 'dev':
        raise cappa.Exit('插件安装仅在开发环境可用', code=1)

    plugin_name = None
    console.note('开始安装插件...')

    try:
        if frontend:
            if repo_url is None:
                raise cappa.Exit('前端插件仅允许通过 Git 仓库地址安装', code=1)

            frontend_project_root = Prompt.ask('请输入前端项目根路径')
            plugin_name = await install_git_frontend_plugin(repo_url, frontend_project_root)
            console.tip(f'前端插件 {plugin_name} 安装成功')
            return

        if path is None and repo_url is None:
            raise cappa.Exit('path 或 repo_url 必须指定其中一项', code=1)
        if path and repo_url:
            raise cappa.Exit('path 和 repo_url 不能同时指定', code=1)

        if path:
            plugin_name = await install_zip_plugin(file=path)
        if repo_url:
            plugin_name = await install_git_plugin(repo_url=repo_url)

        console.tip(f'插件 {plugin_name} 安装成功')

        console.note(f'正在同步插件 {plugin_name} 数据库表...')
        try:
            import_module_cached(f'backend.plugin.{plugin_name}.model')
        except ModuleNotFoundError:
            pass
        else:
            async with async_db_session.begin() as db:
                conn = await db.connection()
                await conn.run_sync(MappedBase.metadata.create_all)

        if not no_sql:
            sql_file = await get_plugin_sql(plugin_name, db_type, pk_type)
            if sql_file:
                console.info(f'正在执行插件 {plugin_name} 初始化 SQL 脚本：{sql_file}')
                async with async_db_session.begin() as db:
                    await execute_sql_scripts(db, sql_file)
            else:
                console.warning(f'插件 {plugin_name} 未提供初始化 SQL 脚本，跳过数据库初始化')

    except Exception as e:
        raise cappa.Exit(e.msg if isinstance(e, BaseExceptionError) else str(e), code=1)


def should_sync_plugin_deps(plugin: str | None, *, allow_empty: bool) -> bool:
    """检查是否需要同步插件依赖"""
    plugins = get_plugins()
    if plugin is not None and plugin not in plugins:
        raise cappa.Exit(f'插件 {plugin} 不存在', code=1)
    if not plugins:
        if allow_empty:
            console.warning('当前没有已安装的插件，跳过插件依赖同步')
            return False
        raise cappa.Exit('当前没有已安装的插件', code=1)
    return True


async def sync_project_deps() -> None:
    """同步项目依赖"""
    console.note('正在同步项目依赖...')
    try:
        await run_in_threadpool(subprocess.run, ['uv', 'sync'], cwd=BASE_PATH.parent, check=True)
    except FileNotFoundError:
        raise cappa.Exit('uv 未安装，请先安装 uv', code=1)
    except subprocess.CalledProcessError as e:
        raise cappa.Exit('项目依赖同步失败', code=e.returncode)
    console.tip('项目依赖同步完成')


async def sync_plugin_deps(plugin: str | None = None) -> None:
    """同步插件依赖"""
    console.note(f'正在安装插件 {plugin} 依赖...' if plugin else '正在安装所有插件依赖...')
    try:
        await install_requirements_async(plugin)
    except Exception as e:
        raise cappa.Exit(e.msg if isinstance(e, BaseExceptionError) else str(e), code=1)
    console.tip(f'插件 {plugin} 依赖安装完成' if plugin else '所有插件依赖安装完成')


async def sync_deps(plugin: str | None, *, no_project: bool = False, no_plugin: bool = False) -> None:
    """同步项目和插件依赖"""
    if no_project and no_plugin:
        raise cappa.Exit('--no-project 和 --no-plugin 不能同时使用', code=1)
    if plugin is not None and no_plugin:
        raise cappa.Exit('--plugin 和 --no-plugin 不能同时使用', code=1)

    should_sync_plugins = False if no_plugin else should_sync_plugin_deps(plugin, allow_empty=not no_project)
    if not no_project:
        await sync_project_deps()
    if should_sync_plugins:
        await sync_plugin_deps(plugin)


async def remove_plugin(plugin: str | None, *, no_sql: bool = False) -> None:  # noqa: C901
    """卸载插件"""
    if settings.ENVIRONMENT != 'dev':
        raise cappa.Exit('插件卸载仅在开发环境可用', code=1)

    async def remove() -> None:
        plugin_dir = PLUGIN_DIR / plugin
        if not plugin_dir.exists():
            raise cappa.Exit(f'插件 {plugin} 不存在', code=1)

        if not no_sql:
            destroy_sql_file = await get_plugin_destroy_sql(plugin, settings.DATABASE_TYPE, settings.DATABASE_PK_MODE)
            if destroy_sql_file:
                console.note(f'正在执行插件 {plugin} 销毁 SQL 脚本：{destroy_sql_file}')
                async with async_db_session.begin() as db:
                    await execute_destroy_sql_scripts(db, destroy_sql_file)
            else:
                console.warning(f'插件 {plugin} 未提供销毁 SQL 脚本，跳过数据库清理')

        console.note(f'正在卸载插件 {plugin} 依赖...')
        await uninstall_requirements_async(plugin)

        console.note(f'正在备份插件 {plugin}...')
        backup_file = PLUGIN_DIR / f'{plugin}.{timezone.now().strftime("%Y%m%d%H%M%S")}.backup.zip'
        await run_in_threadpool(zip_plugin, plugin_dir, backup_file)
        await run_in_threadpool(_remove_plugin, plugin_dir)

        console.note(f'备份文件：{backup_file}')
        console.tip(f'插件 {plugin} 卸载成功')
        console.print()
        console.warning('请根据插件说明（README.md）移除相关配置并重启服务')

    plugins = get_plugins()
    if not plugins:
        raise cappa.Exit('当前没有已安装的插件', code=1)

    if not plugin:
        table = Table(show_header=True, header_style='bold magenta')
        table.add_column('编号', style='cyan', no_wrap=True, justify='center')
        table.add_column('插件名称', style='green', no_wrap=True)

        for idx, name in enumerate(plugins, 1):
            table.add_row(str(idx), name)

        console.print(table)
        choice = IntPrompt.ask('请选择要卸载的插件编号', choices=[str(i) for i in range(1, len(plugins) + 1)])
        plugin = plugins[choice - 1]
    else:
        if plugin not in plugins:
            raise cappa.Exit(f'插件 {plugin} 不存在', code=1)

    if plugin in get_required_plugins():
        raise cappa.Exit(f'插件 {plugin} 为必需插件，禁止卸载', code=1)

    try:
        await remove()
    except Exception as e:
        raise cappa.Exit(f'插件卸载失败：{e}', code=1)


async def get_sql_scripts() -> list[str]:
    """获取所有待执行的 SQL 脚本路径列表"""
    sql_scripts: list[str] = []
    db_script_dir = MYSQL_SCRIPT_DIR if DataBaseType.mysql == settings.DATABASE_TYPE else POSTGRESQL_SCRIPT_DIR
    main_sql_file = db_script_dir / build_sql_filename(
        'init',
        settings.DATABASE_PK_MODE,
        suffix='test_data',
    )

    if await anyio.Path(main_sql_file).exists():
        sql_scripts.append(str(main_sql_file))

    for plugin in get_plugins():
        plugin_sql = await get_plugin_sql(plugin, settings.DATABASE_TYPE, settings.DATABASE_PK_MODE)
        if plugin_sql:
            sql_scripts.append(plugin_sql)

    return sql_scripts


async def execute_sql_scripts(db: AsyncSession, sql_scripts: str, *, is_init: bool = False) -> None:
    """解析并执行 SQL 脚本"""
    try:
        stmts = await parse_sql_script(sql_scripts)
        conn = await db.connection()
        for stmt in stmts:
            await conn.exec_driver_sql(stmt)
    except Exception as e:
        raise cappa.Exit(f'SQL 脚本执行失败：{e}', code=1)

    if not is_init:
        console.tip('SQL 脚本已执行完成')


async def execute_destroy_sql_scripts(db: AsyncSession, sql_scripts: str) -> None:
    """执行插件销毁 SQL 脚本"""
    try:
        stmts = await parse_sql_script(sql_scripts, is_destroy=True)
        conn = await db.connection()
        for stmt in stmts:
            await conn.exec_driver_sql(stmt)
    except Exception as e:
        raise cappa.Exit(f'销毁 SQL 脚本执行失败：{e}', code=1)

    console.tip('销毁 SQL 脚本已执行完成')


async def import_table(
    app: str,
    table_schema: str,
    table_name: str,
) -> None:
    """导入代码生成业务和模型列"""
    if settings.ENVIRONMENT != 'dev':
        raise cappa.Exit('代码生成仅在开发环境可用', code=1)

    try:
        from backend.plugin.code_generator.schema.gen import ImportParam
        from backend.plugin.code_generator.service.gen_service import gen_service
    except ImportError:
        raise cappa.Exit('代码生成插件用法导入失败，请联系系统管理员', code=1)

    try:
        obj = ImportParam(app=app, table_schema=table_schema, table_name=table_name)
        async with async_db_session.begin() as db:
            await gen_service.import_business_and_model(db=db, obj=obj)
        console.tip('代码生成业务和模型列导入成功')
        console.log('\n快试试 [bold cyan]fba codegen[/bold cyan] 生成代码吧~')
    except Exception as e:
        raise cappa.Exit(e.msg if isinstance(e, BaseExceptionError) else str(e), code=1)


async def generate(*, preview: bool = False) -> None:
    """交互式代码生成"""
    if settings.ENVIRONMENT != 'dev':
        raise cappa.Exit('代码生成仅在开发环境可用', code=1)

    try:
        from backend.plugin.code_generator.service.business_service import gen_business_service
        from backend.plugin.code_generator.service.gen_service import gen_service
    except ImportError:
        raise cappa.Exit('代码生成插件用法导入失败，请联系系统管理员', code=1)

    try:
        ids = []
        async with async_db_session() as db:
            results = await gen_business_service.get_all(db=db)

        if not results:
            raise cappa.Exit('[red]暂无可用的代码生成业务！请先通过 import 命令导入！[/]')

        table = Table(show_header=True, header_style='bold magenta')
        table.add_column('业务编号', style='cyan', no_wrap=True, justify='center')
        table.add_column('应用名称', style='green', no_wrap=True)
        table.add_column('生成路径', style='yellow')
        table.add_column('备注', style='blue')

        for result in results:
            ids.append(result.id)
            table.add_row(
                str(result.id),
                result.app_name,
                result.gen_path or f'应用 {result.app_name} 根路径',
                result.remark or '',
            )

        console.print(table)
        business = IntPrompt.ask('请从中选择一个业务编号', choices=[str(id_) for id_ in ids])

        # 预览
        async with async_db_session() as db:
            preview_data = await gen_service.preview(db=db, pk=business)

        console.print('\n[bold yellow]将要生成以下文件：[/]')
        file_table = Table(show_header=True, header_style='bold cyan')
        file_table.add_column('文件路径', style='white')
        file_table.add_column('大小', style='green', justify='right')

        for filepath, content in sorted(preview_data.items()):
            size = len(content)
            size_str = f'{size} B' if size < 1024 else f'{size / 1024:.1f} KB'
            file_table.add_row(filepath, size_str)

        console.print(file_table)

        if preview:
            console.print('\n[bold cyan]预览模式：未执行实际生成操作[/]')
            return

        # 生成
        console.print('\n[bold red]警告：代码生成将进行磁盘文件（覆盖）写入，切勿在生产环境中使用！！！[/]')
        ok = Prompt.ask('\n确认继续生成代码吗？', choices=['y', 'n'], default='n')

        if ok.lower() == 'y':
            async with async_db_session.begin() as db:
                gen_path = await gen_service.generate(db=db, pk=business)

            console.print()
            console.tip('代码已生成完成')
            console.print(Text('\n详情请查看：'), Text(str(gen_path), style='bold white'))

    except Exception as e:
        raise cappa.Exit(e.msg if isinstance(e, BaseExceptionError) else str(e), code=1)


def run_alembic(*args: str) -> None:
    """执行 alembic 命令"""
    try:
        subprocess.run(['alembic', *args], cwd=BASE_PATH.parent, check=True)
    except subprocess.CalledProcessError as e:
        raise cappa.Exit('Alembic 命令执行失败', code=e.returncode)


@cappa.command(help='初始化 fba 项目', default_long=True)
@dataclass
class Init:
    auto: Annotated[
        bool,
        cappa.Arg(default=False, help='自动化初始化模式：自动创建 .env、安装依赖、创建数据库并初始化表结构'),
    ]

    async def __call__(self) -> None:
        if self.auto:
            await auto_init()
        else:
            async with async_db_session.begin() as db:
                await init(db, redis_client)


@cappa.command(help='运行 API 服务', default_long=True)
@dataclass
class Run:
    host: Annotated[
        str,
        cappa.Arg(
            default='127.0.0.1',
            help='提供服务的主机 IP 地址，对于本地开发，请使用 `127.0.0.1`。'
            '要启用公共访问，例如在局域网中，请使用 `0.0.0.0`',
        ),
    ]
    port: Annotated[
        int,
        cappa.Arg(default=8000, help='提供服务的主机端口号'),
    ]
    no_reload: Annotated[
        bool,
        cappa.Arg(default=False, help='禁用在（代码）文件更改时自动重新加载服务器'),
    ]
    workers: Annotated[
        int,
        cappa.Arg(default=1, help='使用多个工作进程，必须与 `--no-reload` 同时使用'),
    ]

    def __call__(self) -> None:
        run(host=self.host, port=self.port, reload=self.no_reload, workers=self.workers)


@cappa.command(help='新增插件', default_long=True)
@dataclass
class Add:
    path: Annotated[
        str | None,
        cappa.Arg(default=None, help='ZIP 插件的本地完整路径'),
    ]
    repo_url: Annotated[
        str | None,
        cappa.Arg(default=None, help='Git 插件的仓库地址'),
    ]
    frontend: Annotated[
        bool,
        cappa.Arg(short='-f', default=False, help='安装前端插件'),
    ]
    no_sql: Annotated[
        bool,
        cappa.Arg(default=False, help='禁用插件 SQL 脚本自动执行'),
    ]
    db_type: Annotated[
        DataBaseType,
        cappa.Arg(default=settings.DATABASE_TYPE, help='执行插件 SQL 脚本的数据库类型'),
    ]
    pk_type: Annotated[
        PrimaryKeyType,
        cappa.Arg(default=settings.DATABASE_PK_MODE, help='执行插件 SQL 脚本数据库主键类型'),
    ]

    async def __call__(self) -> None:
        await install_plugin(self.path, self.repo_url, self.frontend, self.no_sql, self.db_type, self.pk_type)


@cappa.command(help='移除插件')
@dataclass
class Remove:
    plugin: Annotated[
        str | None,
        cappa.Arg(default=None, help='要移除的插件名称'),
    ]
    no_sql: Annotated[
        bool,
        cappa.Arg(default=False, help='禁用插件销毁 SQL 脚本自动执行'),
    ]

    async def __call__(self) -> None:
        await remove_plugin(self.plugin, no_sql=self.no_sql)


@cappa.command(help='同步项目和插件依赖', default_long=True)
@dataclass
class Deps:
    plugin: Annotated[
        str | None,
        cappa.Arg(default=None, help='指定插件名称，不指定则同步所有插件依赖'),
    ]
    no_project: Annotated[
        bool,
        cappa.Arg(default=False, help='跳过项目依赖同步'),
    ]
    no_plugin: Annotated[
        bool,
        cappa.Arg(default=False, help='跳过插件依赖同步'),
    ]

    async def __call__(self) -> None:
        await sync_deps(self.plugin, no_project=self.no_project, no_plugin=self.no_plugin)


@cappa.command(help='格式化代码')
@dataclass
class Format:
    def __call__(self) -> None:
        try:
            subprocess.run(['prek', 'run', '--all-files'], cwd=BASE_PATH.parent, check=False)
        except FileNotFoundError:
            raise cappa.Exit('prek 未安装，请先安装项目依赖', code=1)
        except KeyboardInterrupt:
            pass


@cappa.command(help='从当前主机启动 Celery worker 服务', default_long=True)
@dataclass
class Worker:
    log_level: Annotated[
        Literal['info', 'debug'],
        cappa.Arg(short='-l', default='info', help='日志输出级别'),
    ]

    def __call__(self) -> None:
        run_celery_worker(log_level=self.log_level)


@cappa.command(help='从当前主机启动 Celery beat 服务', default_long=True)
@dataclass
class Beat:
    log_level: Annotated[
        Literal['info', 'debug'],
        cappa.Arg(short='-l', default='info', help='日志输出级别'),
    ]

    def __call__(self) -> None:
        run_celery_beat(log_level=self.log_level)


@cappa.command(help='从当前主机启动 Celery flower 服务', default_long=True)
@dataclass
class Flower:
    port: Annotated[
        int,
        cappa.Arg(default=8555, help='提供服务的主机端口号'),
    ]
    basic_auth: Annotated[
        str,
        cappa.Arg(default='admin:123456', help='页面登录的用户名和密码'),
    ]

    def __call__(self) -> None:
        run_celery_flower(port=self.port, basic_auth=self.basic_auth)


@cappa.command(help='运行 Celery 服务')
@dataclass
class Celery:
    subcmd: cappa.Subcommands[Worker | Beat | Flower]


@cappa.command(help='导入代码生成业务和模型列', default_long=True)
@dataclass
class Import:
    app: Annotated[
        str,
        cappa.Arg(help='应用名称，用于代码生成到指定 app'),
    ]
    table_schema: Annotated[
        str,
        cappa.Arg(short='tc', default='fba', help='数据库名'),
    ]
    table_name: Annotated[
        str,
        cappa.Arg(short='tn', help='数据库表名'),
    ]

    async def __call__(self) -> None:
        await import_table(self.app, self.table_schema, self.table_name)


@cappa.command(name='codegen', help='代码生成（体验完整功能，请自行部署 fba vben 前端工程）', default_long=True)
@dataclass
class CodeGenerator:
    preview: Annotated[
        bool,
        cappa.Arg(short='-p', default=False, help='仅预览将要生成的文件，不执行实际生成操作'),
    ]
    subcmd: cappa.Subcommands[Import | None] = None

    async def __call__(self) -> None:
        await generate(preview=self.preview)


@cappa.command(help='生成数据库迁移文件', default_long=True)
@dataclass
class Revision:
    autogenerate: Annotated[
        bool,
        cappa.Arg(default=True, help='自动检测模型变更并生成迁移脚本'),
    ]
    message: Annotated[
        str,
        cappa.Arg(short='-m', default='', help='迁移文件的描述信息'),
    ]

    def __call__(self) -> None:
        args = ['revision']
        if self.autogenerate:
            args.append('--autogenerate')
        if self.message:
            args.extend(['-m', self.message])
        run_alembic(*args)
        console.tip('迁移文件生成成功')


@cappa.command(help='升级数据库到指定版本', default_long=True)
@dataclass
class Upgrade:
    revision: Annotated[
        str,
        cappa.Arg(default='head', help='目标版本，默认为最新版本'),
    ]

    def __call__(self) -> None:
        run_alembic('upgrade', self.revision)
        console.tip(f'数据库已升级到: {self.revision}')


@cappa.command(help='降级数据库到指定版本', default_long=True)
@dataclass
class Downgrade:
    revision: Annotated[
        str,
        cappa.Arg(default='-1', help='目标版本，默认回退一个版本'),
    ]

    def __call__(self) -> None:
        run_alembic('downgrade', self.revision)
        console.tip(f'数据库已降级到: {self.revision}')


@cappa.command(help='显示数据库当前迁移版本')
@dataclass
class Current:
    verbose: Annotated[
        bool,
        cappa.Arg(short='-v', default=False, help='显示详细信息'),
    ]

    def __call__(self) -> None:
        args = ['current']
        if self.verbose:
            args.append('-v')
        run_alembic(*args)


@cappa.command(help='显示迁移历史记录', default_long=True)
@dataclass
class History:
    verbose: Annotated[
        bool,
        cappa.Arg(short='-v', default=False, help='显示详细信息'),
    ]
    range: Annotated[
        str,
        cappa.Arg(short='-r', default='', help='显示指定范围的历史，例如 -r base:head'),
    ]

    def __call__(self) -> None:
        args = ['history']
        if self.verbose:
            args.append('-v')
        if self.range:
            args.extend(['-r', self.range])
        run_alembic(*args)


@cappa.command(help='显示所有头版本')
@dataclass
class Heads:
    verbose: Annotated[
        bool,
        cappa.Arg(short='-v', default=False, help='显示详细信息'),
    ]

    def __call__(self) -> None:
        args = ['heads']
        if self.verbose:
            args.append('-v')
        run_alembic(*args)


@cappa.command(help='数据库迁移管理')
@dataclass
class Alembic:
    subcmd: cappa.Subcommands[Revision | Upgrade | Downgrade | Current | History | Heads]


@cappa.command(help='一个高效的 fba 命令行界面', default_long=True)
@dataclass
class FbaCli:
    sql: Annotated[
        str,
        cappa.Arg(value_name='PATH', default='', show_default=False, help='在事务中执行 SQL 脚本'),
    ]
    subcmd: cappa.Subcommands[Init | Run | Add | Remove | Deps | Format | Celery | CodeGenerator | Alembic | None] = (
        None
    )

    async def __call__(self) -> None:
        if self.sql:
            async with async_db_session.begin() as db:
                await execute_sql_scripts(db, self.sql)


def main() -> None:
    output = cappa.Output(error_format=f'{error_format}\n{_OUTPUT_HELP}')
    asyncio.run(cappa.invoke_async(FbaCli, version=__version__, output=output))
