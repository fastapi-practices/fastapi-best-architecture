import uuid

from fast_captcha import img_captcha
from fastapi import APIRouter, Depends
from starlette.concurrency import run_in_threadpool

from backend.app.admin.schema.captcha import GetCaptchaDetail
from backend.common.limiter import rate_limit
from backend.common.response.response_schema import ResponseSchemaModel, response_base
from backend.core.conf import settings
from backend.database.db import CurrentSession
from backend.database.redis import redis_client
from backend.utils.dynamic_config import load_login_config

router = APIRouter()


@router.get(
    '/captcha',
    summary='获取登录验证码',
    dependencies=[Depends(rate_limit('5/30seconds'))],
)
async def get_captcha(db: CurrentSession) -> ResponseSchemaModel[GetCaptchaDetail]:
    await load_login_config(db)
    img, code = await run_in_threadpool(img_captcha, img_byte='base64')
    captcha_uuid = str(uuid.uuid4())
    await redis_client.set(
        f'{settings.LOGIN_CAPTCHA_REDIS_PREFIX}:{captcha_uuid}',
        code,
        ex=settings.LOGIN_CAPTCHA_EXPIRE_SECONDS,
    )
    data = GetCaptchaDetail(
        is_enabled=settings.LOGIN_CAPTCHA_ENABLED,
        expire_seconds=settings.LOGIN_CAPTCHA_EXPIRE_SECONDS,
        uuid=captcha_uuid,
        image=img,
    )
    return response_base.success(data=data)
