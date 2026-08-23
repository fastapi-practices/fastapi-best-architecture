import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from backend.common.context import ctx
from backend.common.log import log
from backend.utils.timezone import timezone


class AccessMiddleware(BaseHTTPMiddleware):
    """访问日志中间件"""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        perf_time = time.perf_counter()
        ctx.perf_time = perf_time
        ctx.start_time = timezone.now()

        if request.method != 'OPTIONS':
            path = request.url.path if not request.url.query else f'{request.url.path}?{request.url.query}'
            log.debug(f'--> 请求开始[{path}]')

        response = await call_next(request)
        elapsed = round((time.perf_counter() - perf_time) * 1000, 3)
        log.debug(f'<-- 请求结束 [{response.status_code}] {elapsed:.3f}ms')
        return response
