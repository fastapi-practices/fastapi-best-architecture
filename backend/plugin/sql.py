import anyio

from backend.common.enums import DataBaseType, PrimaryKeyType
from backend.core.path_conf import PLUGIN_DIR


def build_sql_filename(
    prefix: str,
    pk_type: PrimaryKeyType,
    *,
    suffix: str | None = None,
) -> str:
    """
    构建插件 SQL 脚本文件名

    :param prefix: SQL 脚本文件名前缀，例如 init 或 destroy
    :param pk_type: 主键类型，雪花 ID 模式会追加 snowflake 标识
    :param suffix: 可选文件名后缀，追加在主键类型标识之后
    :return:
    """
    parts = [prefix]
    if pk_type == PrimaryKeyType.snowflake:
        parts.append('snowflake')
    if suffix:
        parts.append(suffix)
    return f'{"_".join(parts)}.sql'


async def get_plugin_sql(plugin: str, db_type: DataBaseType, pk_type: PrimaryKeyType) -> str | None:
    """
    获取插件 SQL 脚本

    :param plugin: 插件名称
    :param db_type: 数据库类型
    :param pk_type: 主键类型
    :return:
    """
    sql_dir = PLUGIN_DIR / plugin / 'sql' / ('mysql' if db_type == DataBaseType.mysql else 'postgresql')
    default_filename = build_sql_filename('init', pk_type)
    default_sql_file = sql_dir / default_filename
    return str(default_sql_file) if await anyio.Path(default_sql_file).exists() else None


async def get_plugin_destroy_sql(plugin: str, db_type: DataBaseType, pk_type: PrimaryKeyType) -> str | None:
    """
    获取插件销毁 SQL 脚本

    :param plugin: 插件名称
    :param db_type: 数据库类型
    :param pk_type: 主键类型
    :return:
    """
    sql_dir = PLUGIN_DIR / plugin / 'sql' / ('mysql' if db_type == DataBaseType.mysql else 'postgresql')
    sql_file = sql_dir / build_sql_filename('destroy', pk_type)
    return str(sql_file) if await anyio.Path(sql_file).exists() else None
