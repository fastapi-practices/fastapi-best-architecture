import asyncio
import tempfile
import uuid

import anyio

from anyio import open_file


async def format_python_code(code: str) -> str:
    """
    使用 ruff 格式化 Python 代码

    :param code: 原始代码
    :return:
    """
    temp_dir = anyio.Path(tempfile.gettempdir())
    temp_file = temp_dir / f'fba_codegen_{uuid.uuid4().hex}.py'

    try:
        async with await open_file(temp_file, 'w', encoding='utf-8') as f:
            await f.write(code)
        process = await asyncio.create_subprocess_exec(
            'ruff',
            'format',
            str(temp_file),
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await process.wait()
        if process.returncode == 0:
            async with await open_file(temp_file, encoding='utf-8') as f:
                formatted_code = await f.read()
        else:
            formatted_code = code
    except (FileNotFoundError, OSError):
        return code
    finally:
        await temp_file.unlink(missing_ok=True)

    return formatted_code
