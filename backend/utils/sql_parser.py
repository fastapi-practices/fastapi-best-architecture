from typing import Final

import anyio

from anyio import open_file
from sqlparse import split

from backend.common.exception import errors

# 初始化脚本允许的 SQL 语句前缀
_INIT_SQL_PREFIXES: Final = frozenset({'select', 'insert', 'set', 'do'})

# 销毁脚本允许的 SQL 语句前缀
_DESTROY_SQL_PREFIXES: Final = _INIT_SQL_PREFIXES | {'drop', 'delete', 'alter'}


async def parse_sql_script(filepath: str, *, is_destroy: bool = False) -> list[str]:
    """
    解析 SQL 脚本

    :param filepath: 脚本文件路径
    :param is_destroy: 是否为销毁脚本，将允许破坏性操作
    :return:
    """
    path = anyio.Path(filepath)
    if not await path.exists():
        raise errors.NotFoundError(msg='SQL 脚本文件不存在')

    async with await open_file(filepath, encoding='utf-8') as f:
        contents = await f.read(1024)
        while additional_contents := await f.read(1024):
            contents += additional_contents

    statements = [stmt for stmt in split(contents) if stmt.strip()]
    allowed_prefixes = _DESTROY_SQL_PREFIXES if is_destroy else _INIT_SQL_PREFIXES
    for statement in statements:
        if not any(statement.strip().lower().startswith(prefix) for prefix in allowed_prefixes):
            raise errors.RequestError(
                msg=f'SQL 脚本 {filepath} 存在非法操作，仅允许：{", ".join(item.upper() for item in sorted(allowed_prefixes))}'  # noqa: E501
            )

    return statements
