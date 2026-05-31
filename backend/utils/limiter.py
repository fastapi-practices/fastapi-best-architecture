from collections.abc import Awaitable, Callable
from math import ceil
from typing import TypeAlias

from fastapi import Request, Response
from fastapi_pagination.utils import is_async_callable
from pyrate_limiter import AbstractBucket, Limiter, Rate
from pyrate_limiter.buckets import RedisBucket
from starlette.concurrency import run_in_threadpool

from backend.common.exception import errors
from backend.common.response.response_code import StandardResponseCode
from backend.core.conf import settings
from backend.database.redis import redis_client
from backend.utils.request_parse import get_request_ip

IdentifierCallable: TypeAlias = Callable[[Request], str] | Callable[[Request], Awaitable[str]]
CallbackCallable: TypeAlias = (
    Callable[[Request, Response, int], None] | Callable[[Request, Response, int], Awaitable[None]]
)


def default_identifier(request: Request) -> str:
    """
    默认标识符

    :param request: FastAPI 请求对象
    :return:
    """
    ip = get_request_ip(request)
    return f'{ip}:{request.scope["path"]}'


def default_callback(request: Request, response: Response, retry_after: int) -> None:
    """
    默认回调

    :param request: FastAPI 请求对象
    :param response: FastAPI 响应对象
    :param retry_after: 下次重试秒数
    :return:
    """
    raise errors.HTTPError(
        code=StandardResponseCode.HTTP_429,
        msg='请求过于频繁，请稍后重试',
        headers={'Retry-After': str(retry_after)},
    )


class RateLimiter:
    """速率限制器"""

    def __init__(
        self,
        *rates: Rate,
        identifier: IdentifierCallable = default_identifier,
        bucket: AbstractBucket | None = None,
        limiter: Limiter | None = None,
        callback: CallbackCallable = default_callback,
    ) -> None:
        """
        初始化速率限制器

        :param rates: pyrate_limiter Rate 对象，支持传入单个或多个
        :param identifier: 自定义标识符函数
        :param bucket: pyrate_limiter AbstractBucket 实例
        :param limiter: pyrate_limiter Limiter 实例
        :param callback: 自定义限流回调函数
        :return:
        """
        if not rates and bucket is None:
            raise errors.ServerError(msg='至少需要传入一个 Rate 或 bucket 实例')
        self.rates = list(rates)
        self.identifier = identifier
        self.bucket = bucket
        self.limiter = limiter
        self.callback = callback

    async def __call__(self, request: Request, response: Response) -> None:
        if self.limiter is None:
            if self.bucket is None:
                self.bucket = await RedisBucket.init(  # type: ignore
                    rates=self.rates,
                    redis=redis_client,
                    bucket_key=f'{settings.REQUEST_LIMITER_REDIS_PREFIX}',
                )
            self.limiter = Limiter(self.bucket)

        if is_async_callable(self.identifier):
            identifier = await self.identifier(request)
        else:
            identifier = await run_in_threadpool(self.identifier, request)

        acquired = await self.limiter.try_acquire_async(identifier, blocking=False)
        if not acquired:
            retry_after = ceil(self.bucket.failing_rate.interval / 1000)
            if is_async_callable(self.callback):
                await self.callback(request, response, retry_after)
            else:
                await run_in_threadpool(self.callback, request, response, retry_after)
