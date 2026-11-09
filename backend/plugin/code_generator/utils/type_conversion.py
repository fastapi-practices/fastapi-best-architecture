from functools import lru_cache

from backend.plugin.code_generator.enums import GenPostgreSQLColumnType


@lru_cache(maxsize=128)
def sql_type_to_sqlalchemy(typing: str) -> str:
    """
    将 SQL 类型转换为 SQLAlchemy 类型

    :param typing: SQL 类型字符串
    :return:
    """
    normalized_type = typing.replace(' ', '_')
    if normalized_type in GenPostgreSQLColumnType.get_member_keys():
        return typing
    return 'String'


@lru_cache(maxsize=128)
def sql_type_to_pydantic(typing: str) -> str:
    """
    将 SQL 类型转换为 Pydantic 类型

    :param typing: SQL 类型字符串
    :return:
    """
    try:
        normalized_type = typing.replace(' ', '_')
        return GenPostgreSQLColumnType[normalized_type].value
    except KeyError:
        return 'str'


@lru_cache(maxsize=128)
def sql_type_to_sqlalchemy_name(typing: str) -> str:
    """
    将 SQL 类型转换为有效的 SQLAlchemy 类型名称(用于代码生成)

    :param typing: SQL 类型字符串
    :return:
    """
    pg_type_mapping = {
        'CHARACTER VARYING': 'String',
        'CHARACTER': 'CHAR',
        'TIMESTAMP WITHOUT TIME ZONE': 'TIMESTAMP',
        'TIMESTAMP WITH TIME ZONE': 'TIMESTAMP',
        'TIME WITHOUT TIME ZONE': 'TIME',
        'TIME WITH TIME ZONE': 'TIME',
        'DOUBLE PRECISION': 'Double',
    }

    if typing in pg_type_mapping:
        return pg_type_mapping[typing]

    return typing
