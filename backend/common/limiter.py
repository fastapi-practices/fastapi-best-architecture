from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import Request, Response
from redis_fastapi import RateLimitBackend, RateLimitResult
from redis_fastapi import rate_limit as sdk_rate_limit

from backend.common.exception import errors
from backend.common.i18n import t
from backend.common.response.response_code import StandardResponseCode
from backend.database.redis import redis_client
from backend.utils.request_parse import get_request_ip


async def get_fba_rate_limit_backend() -> RateLimitBackend:  # ruff: ignore[unused-async]
    """向 SDK 注入由 fba 管理的限流后端"""
    return RateLimitBackend(redis_client)


def rate_limit_exceeded(request: Request, result: RateLimitResult) -> Response:
    """
    限流命中回调

    抛回项目统一异常，复用全局异常处理器输出的响应体格式与 trace_id

    :param request: FastAPI 请求对象
    :param result: SDK 限流结果
    :return:
    """
    raise errors.HTTPError(
        code=StandardResponseCode.HTTP_429,
        msg=t('response.rate_limit'),
        headers={'X-RateLimit-Retry-After': str(result.retry_after)},
    )


def rate_limit(rate: str, **kwargs: Any) -> Callable[..., Awaitable[None]]:
    """
    构造路由级限流依赖

    :param rate: 限流规格，如 '5/minute'、'5/30seconds'
    :param kwargs: 透传 SDK `rate_limit` 的其余参数
    :return:
    """
    kwargs.setdefault('identifier', get_request_ip)
    kwargs.setdefault('on_limit_exceeded', rate_limit_exceeded)
    kwargs.setdefault('fail_closed', True)
    return sdk_rate_limit(rate, **kwargs)
