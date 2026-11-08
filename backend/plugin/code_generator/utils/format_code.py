import asyncio
import tempfile
import uuid

import anyio

from anyio import open_file

from backend.core.path_conf import BASE_PATH


async def format_python_code(code: str) -> str:
    """
    使用 ruff 格式化 Python 代码

    :param code: 原始代码
    :return:
    """
    temp_dir = anyio.Path(tempfile.gettempdir())
    temp_file = temp_dir / f'fba_codegen_{uuid.uuid4().hex}.py'
    config_path = BASE_PATH.parent / 'pyproject.toml'

    try:
        async with await open_file(temp_file, 'w', encoding='utf-8') as f:
            await f.write(code)

        # 优先使用项目自身的 ruff 配置，保证生成代码风格与项目一致，配置不可用时回退到 ruff 默认配置
        commands = [['ruff', 'format', str(temp_file)]]
        if await anyio.Path(config_path).is_file():
            commands.insert(0, ['ruff', 'format', '--config', str(config_path), str(temp_file)])

        for command in commands:
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await process.wait()
            if process.returncode == 0:
                async with await open_file(temp_file, encoding='utf-8') as f:
                    return await f.read()
    except (FileNotFoundError, OSError):
        return code
    finally:
        await temp_file.unlink(missing_ok=True)

    return code
