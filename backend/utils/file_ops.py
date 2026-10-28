from anyio import open_file
from fastapi import UploadFile

from backend.common.exception import errors
from backend.common.i18n import t
from backend.common.log import log
from backend.core.conf import settings
from backend.core.path_conf import UPLOAD_DIR
from backend.utils.timezone import timezone


def build_filename(file: UploadFile) -> str:
    """
    构建文件名

    :param file: FastAPI 上传文件对象
    :return:
    """
    timestamp = int(timezone.now().timestamp())
    filename = file.filename
    file_ext = filename.split('.')[-1].lower()
    new_filename = f'{filename.replace(f".{file_ext}", f"_{timestamp}")}.{file_ext}'
    return new_filename


def upload_file_verify(file: UploadFile) -> None:
    """
    文件验证

    :param file: FastAPI 上传文件对象
    :return:
    """
    filename = file.filename
    file_ext = filename.split('.')[-1].lower()
    if not file_ext:
        raise errors.RequestError(msg=t('error.file.unknown_type'))

    if file_ext in settings.UPLOAD_IMAGE_EXT_INCLUDE:
        if file.size > settings.UPLOAD_IMAGE_SIZE_MAX:
            raise errors.RequestError(msg=t('error.file.image_too_large'))
    elif file_ext in settings.UPLOAD_VIDEO_EXT_INCLUDE:
        if file.size > settings.UPLOAD_VIDEO_SIZE_MAX:
            raise errors.RequestError(msg=t('error.file.video_too_large'))
    else:
        raise errors.RequestError(msg=t('error.file.unsupported_ext', file_ext=file_ext))


async def upload_file(file: UploadFile) -> str:
    """
    上传文件

    :param file: FastAPI 上传文件对象
    :return:
    """
    filename = build_filename(file)
    try:
        async with await open_file(UPLOAD_DIR / filename, mode='wb') as fb:
            while True:
                content = await file.read(settings.UPLOAD_READ_SIZE)
                if not content:
                    break
                await fb.write(content)
    except Exception as e:
        log.error(f'上传文件 {filename} 失败：{e!s}')
        raise errors.RequestError(msg=t('error.file.upload_failed'))
    await file.close()
    return filename
