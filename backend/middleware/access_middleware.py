import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from backend.common.context import ctx
from backend.common.log import log
from backend.common.observability.prometheus.fastapi import (
    dec_fastapi_request_in_progress,
    inc_fastapi_exception,
    inc_fastapi_request,
    inc_fastapi_request_in_progress,
    inc_fastapi_response,
    observe_fastapi_request_cost_time,
)
from backend.common.redaction import REDACTED, redaction
from backend.common.response.response_code import StandardResponseCode
from backend.core.conf import settings
from backend.utils.timezone import timezone
from backend.utils.trace_id import get_request_trace_id


class AccessMiddleware(BaseHTTPMiddleware):
    """访问日志中间件"""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """
        处理请求并记录访问日志

        :param request: FastAPI 请求对象
        :param call_next: 下一个中间件或路由处理函数
        :return:
        """
        perf_time = time.perf_counter()
        ctx.perf_time = perf_time

        start_time = timezone.now()
        ctx.start_time = start_time

        path = request.url.path
        method = request.method

        if method != 'OPTIONS':
            query = request.url.query
            if query and redaction.is_query_redacted(path):
                query = REDACTED
            log.debug(f'--> 请求开始[{path if not query else path + "?" + query}]')

        should_record_metrics = settings.GRAFANA_METRICS_ENABLE and path.startswith(settings.FASTAPI_API_V1_PATH)
        if should_record_metrics:
            inc_fastapi_request_in_progress(method=method, path=path)
            inc_fastapi_request(method=method, path=path)

        try:
            response = await call_next(request)
        except Exception as e:
            elapsed = round((time.perf_counter() - perf_time) * 1000, 3)
            if should_record_metrics:
                inc_fastapi_exception(method=method, path=path, exception_type=type(e).__name__)
                observe_fastapi_request_cost_time(
                    method=method, path=path, elapsed=elapsed, trace_id=get_request_trace_id()
                )
                inc_fastapi_response(
                    method=method,
                    path=path,
                    status_code=getattr(e, 'code', StandardResponseCode.HTTP_500),
                )
            raise
        else:
            elapsed = round((time.perf_counter() - perf_time) * 1000, 3)
            if should_record_metrics:
                request_exception = ctx.request_exception
                exception_code = request_exception.code if request_exception else None
                if request_exception is not None:
                    inc_fastapi_exception(method=method, path=path, exception_type=request_exception.kind.value)
                observe_fastapi_request_cost_time(
                    method=method, path=path, elapsed=elapsed, trace_id=get_request_trace_id()
                )
                inc_fastapi_response(
                    method=method,
                    path=path,
                    status_code=exception_code or response.status_code,
                )
        finally:
            if should_record_metrics:
                dec_fastapi_request_in_progress(method=method, path=path)

        return response
