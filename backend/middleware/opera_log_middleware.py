import json
import time

from typing import Any

from fastapi import Response
from starlette.datastructures import UploadFile
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from backend.common.context import ctx
from backend.common.log import log
from backend.common.response.response_code import StandardResponseCode
from backend.core.conf import settings
from backend.utils.trace_id import get_request_trace_id


class OperaLogMiddleware(BaseHTTPMiddleware):
    """控制台访问日志中间件"""

    _redact_keys = {'password', 'old_password', 'new_password', 'confirm_password'}
    _max_body_size = 10240

    async def dispatch(self, request: Request, call_next: Any) -> Response:
        path = request.url.path
        method = request.method
        args = await self.get_request_args(request)
        code = StandardResponseCode.HTTP_200
        elapsed = 0.0

        try:
            response = await call_next(request)
        except Exception as exc:
            elapsed = round((time.perf_counter() - ctx.perf_time) * 1000, 3)
            code = getattr(exc, 'code', StandardResponseCode.HTTP_500)
            log.error(f'请求异常: {exc!s}')
            raise
        else:
            elapsed = round((time.perf_counter() - ctx.perf_time) * 1000, 3)
            for exception_key in (
                '__request_authentication_exception__',
                '__request_http_exception__',
                '__request_validation_exception__',
                '__request_assertion_error__',
                '__request_custom_exception__',
                '__request_unknown_exception__',
            ):
                exception = ctx.get(exception_key)
                if exception:
                    code = exception.get('code', response.status_code)
                    log.error(f'请求异常: {exception.get("msg")}')
                    break
        finally:
            route = request.scope.get('route')
            summary = route.summary or '' if route else ''
            if path.startswith(settings.FASTAPI_API_V1_PATH):
                log.info(f'{ctx.ip: <15} | {method: <8} | {code!s: <6} | {path} | {elapsed:.3f}ms')
            if args:
                log.debug(f'请求参数: {args}')
            log.debug(f'接口摘要：[{summary}] trace_id={get_request_trace_id()}')

        return response

    async def get_request_args(self, request: Request) -> dict[str, Any] | None:  # ruff:ignore[complex-structure]
        args: dict[str, Any] = {}
        query_params = dict(request.query_params)
        if query_params:
            args['query_params'] = self.desensitization(query_params)

        if request.path_params:
            args['path_params'] = self.desensitization(request.path_params)

        content_types = [item.strip().lower() for item in request.headers.get('Content-Type', '').split(';')]
        is_multipart = 'multipart/form-data' in content_types
        is_form = is_multipart or 'application/x-www-form-urlencoded' in content_types
        content_length = self.get_content_length(request)
        if content_length is not None and content_length > self._max_body_size:
            return self.build_truncated_body(content_length, self._max_body_size)
        if is_multipart and content_length is None:
            return self.build_truncated_body(None, self._max_body_size)

        body = await request.body()
        if is_form:
            form_data = await request.form()
            if form_data:
                serialized_form = {
                    key: {
                        'filename': value.filename,
                        'content_type': value.content_type,
                        'size': value.size,
                    }
                    if isinstance(value, UploadFile)
                    else value
                    for key, value in form_data.items()
                }
                args['form-data' if is_multipart else 'x-www-form-urlencoded'] = self.desensitization(serialized_form)
        elif body and 'application/json' in content_types:
            try:
                data = await request.json()
                args['json'] = self.desensitization(data) if isinstance(data, dict) else data
            except json.JSONDecodeError:
                args['data'] = body.decode('utf-8', 'ignore')
        elif body:
            args['data'] = body.decode('utf-8', 'ignore')

        if args:
            try:
                args_size = len(json.dumps(args, ensure_ascii=False).encode('utf-8'))
                if args_size > self._max_body_size:
                    return self.build_truncated_body(args_size, self._max_body_size)
            except (TypeError, ValueError) as exc:
                log.error(f'请求参数截断处理失败：{exc}')

        return args or None

    @staticmethod
    def get_content_length(request: Request) -> int | None:
        """获取请求体长度"""
        content_length = request.headers.get('Content-Length')
        return int(content_length) if content_length else None

    @staticmethod
    def build_truncated_body(original_size: int | None, max_size: int) -> dict[str, Any]:
        """构建请求体截断信息"""
        return {
            '_truncated': True,
            '_original_size': original_size,
            '_max_size': max_size,
            '_message': '请求体过大或大小未知，已跳过控制台日志请求体记录',
        }

    @classmethod
    def desensitization(cls, args: dict[str, Any]) -> dict[str, Any]:
        for key in args:
            if key in cls._redact_keys:
                args[key] = '[REDACTED]'
        return args
