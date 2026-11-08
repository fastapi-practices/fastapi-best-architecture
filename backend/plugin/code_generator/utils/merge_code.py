import re

from backend.common.log import log
from backend.plugin.code_generator.enums import MergeMode

# 第一方模块的导入语句
BACKEND_APP_IMPORT_PATTERN = re.compile(r'^from\s+backend\.app\.[\w.]+\s+import\b')
# 路由文件中子路由的注册语句
ROUTER_INCLUDE_PATTERN = re.compile(r'^v1\.include_router\(\s*(\w+)')


def get_merge_mode(filepath: str) -> MergeMode:
    """
    获取生成文件的合并模式

    :param filepath: 生成文件相对路径
    :return:
    """
    if filepath.endswith('api/router.py'):
        return MergeMode.ROUTER
    if filepath.endswith('model/__init__.py'):
        return MergeMode.MODEL_INIT
    if filepath.endswith(('/sql/mysql/init.sql', '/sql/postgresql/init.sql')):
        return MergeMode.SQL
    if filepath.endswith('__init__.py'):
        return MergeMode.INIT
    return MergeMode.OVERWRITE


def merge_code(*, mode: MergeMode, existing: str, generated: str) -> str:
    """
    按合并模式合并已有文件与生成文件的内容

    :param mode: 合并模式
    :param existing: 已有文件内容
    :param generated: 生成文件内容
    :return:
    """
    if mode == MergeMode.ROUTER:
        return _merge_router_code(existing=existing, generated=generated)
    if mode == MergeMode.MODEL_INIT:
        return _merge_model_init_code(existing=existing, generated=generated)
    if mode == MergeMode.SQL:
        return _merge_sql_code(existing=existing, generated=generated)
    if mode == MergeMode.INIT:
        return existing if existing.strip() else generated
    return generated


def insert_import_statement(*, lines: list[str], statement: str) -> None:
    """
    按模块路径顺序插入导入语句，已导入相同模块时跳过

    :param lines: 代码行列表
    :param statement: 导入语句
    :return:
    """
    module = statement.split()[1]
    if any(line.startswith(f'from {module} import') for line in lines):
        return

    first_party_indexes = [index for index, line in enumerate(lines) if line.startswith('from backend.')]
    if not first_party_indexes:
        import_indexes = [index for index, line in enumerate(lines) if line.startswith(('import ', 'from '))]
        lines.insert(import_indexes[-1] + 1 if import_indexes else 0, statement)
        return

    for index in first_party_indexes:
        if lines[index].split()[1] > module:
            lines.insert(index, statement)
            return
    lines.insert(first_party_indexes[-1] + 1, statement)


def _merge_router_code(*, existing: str, generated: str) -> str:
    """
    将生成的子路由追加到已有路由文件中

    :param existing: 已有文件内容
    :param generated: 生成文件内容
    :return:
    """
    generated_lines = generated.splitlines()
    import_statement = _find_statement(lines=generated_lines, pattern=BACKEND_APP_IMPORT_PATTERN, contains='router as')
    include_statement = _find_statement(lines=generated_lines, pattern=ROUTER_INCLUDE_PATTERN)
    if not import_statement or not include_statement:
        log.warning('代码生成：无法解析生成的路由文件内容，已保留原有路由文件，请手动补充子路由注册')
        return existing

    lines = existing.splitlines()
    insert_import_statement(lines=lines, statement=import_statement)
    _insert_include_statement(lines=lines, statement=include_statement)

    return '\n'.join(lines) + '\n'


def _merge_model_init_code(*, existing: str, generated: str) -> str:
    """
    将生成的模型导入语句追加到已有模型包初始化文件中

    :param existing: 已有文件内容
    :param generated: 生成文件内容
    :return:
    """
    import_statement = _find_statement(
        lines=generated.splitlines(), pattern=BACKEND_APP_IMPORT_PATTERN, contains=' as '
    )
    if not import_statement:
        log.warning('代码生成：无法解析生成的模型包初始化文件内容，已保留原有文件，请手动补充模型导入')
        return existing

    lines = existing.splitlines()
    insert_import_statement(lines=lines, statement=import_statement)

    return '\n'.join(lines) + '\n'


def _merge_sql_code(*, existing: str, generated: str) -> str:
    """
    将生成的 SQL 语句追加到已有 SQL 脚本文件中

    :param existing: 已有文件内容
    :param generated: 生成文件内容
    :return:
    """
    generated_content = generated.strip()
    if not generated_content:
        return existing
    if not existing.strip():
        return generated
    if generated_content in existing:
        return existing

    return f'{existing.rstrip()}\n\n{generated_content}\n'


def _find_statement(*, lines: list[str], pattern: re.Pattern, contains: str | None = None) -> str | None:
    """
    查找符合模式的完整语句，兼容括号跨行的情况

    :param lines: 代码行列表
    :param pattern: 语句匹配模式
    :param contains: 语句中必须包含的内容
    :return:
    """
    for index, line in enumerate(lines):
        if not pattern.match(line):
            continue

        statement = line
        while statement.count('(') > statement.count(')') and index + 1 < len(lines):
            index += 1
            statement = f'{statement}\n{lines[index]}'
        if contains is None or contains in statement:
            return statement
    return None


def _insert_include_statement(*, lines: list[str], statement: str) -> None:
    """
    将子路由注册语句插入到已有注册语句之后，已注册相同子路由时跳过

    :param lines: 代码行列表
    :param statement: 注册语句
    :return:
    """
    match = ROUTER_INCLUDE_PATTERN.match(statement)
    name = match.group(1) if match else ''
    if name and re.search(rf'include_router\(\s*{name}\b', '\n'.join(lines)):
        return

    for index in range(len(lines) - 1, -1, -1):
        if lines[index].startswith('v1.include_router('):
            lines.insert(index + 1, statement)
            return

    while lines and not lines[-1].strip():
        lines.pop()
    if lines:
        lines.append('')
    lines.append(statement)
