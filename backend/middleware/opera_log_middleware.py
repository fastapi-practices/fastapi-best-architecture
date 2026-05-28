import json
import time

from asyncio import Queue
from typing import Any

from fastapi import Response
from starlette.datastructures import UploadFile
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from backend.app.admin.schema.opera_log import CreateOperaLogParam
from backend.app.admin.service.opera_log_service import opera_log_service
from backend.common.context import ctx
from backend.common.enums import StatusType
from backend.common.log import log
from backend.common.observability.prometheus.queue import observe_queue_size
from backend.common.queue import batch_consume
from backend.common.response.response_code import StandardResponseCode
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.utils.trace_id import get_request_trace_id


class OperaLogMiddleware(BaseHTTPMiddleware):
    """操作日志中间件"""

    opera_log_queue_name = 'opera_log_queue'
    opera_log_queue: Queue[CreateOperaLogParam] = Queue(maxsize=settings.OPERA_LOG_QUEUE_MAXSIZE)

    async def dispatch(self, request: Request, call_next: Any) -> Response:  # noqa: C901
        """
        处理请求并记录操作日志

        :param request: FastAPI 请求对象
        :param call_next: 下一个中间件或路由处理函数
        :return:
        """
        path = request.url.path
        method = request.method
        args = await self.get_request_args(request)
        code = 200
        msg = 'Success'
        status = StatusType.enable
        elapsed = 0

        try:
            username = request.user.username
        except AttributeError:
            username = None

        should_log_opera = path.startswith(settings.FASTAPI_API_V1_PATH) and path not in settings.OPERA_LOG_PATH_EXCLUDE

        try:
            response = await call_next(request)
        except Exception as e:
            elapsed = round((time.perf_counter() - ctx.perf_time) * 1000, 3)
            log.error(f'请求异常: {e!s}')

            if should_log_opera:
                code = getattr(e, 'code', StandardResponseCode.HTTP_500)
                msg = getattr(e, 'msg', str(e))
                status = StatusType.disable

            raise
        else:
            elapsed = round((time.perf_counter() - ctx.perf_time) * 1000, 3)

            if should_log_opera:
                # 检查上下文中的异常信息
                for exception_key in [
                    '__request_http_exception__',
                    '__request_validation_exception__',
                    '__request_assertion_error__',
                    '__request_custom_exception__',
                    '__request_unknown_exception__',
                ]:
                    exception = ctx.get(exception_key)
                    if exception:
                        code = exception.get('code')
                        msg = exception.get('msg')
                        status = StatusType.disable
                        log.error(f'请求异常: {msg}')
                        break
        finally:
            # summary 只能在请求后获取
            route = request.scope.get('route')
            summary = route.summary or '' if route else ''

            log.debug(f'接口摘要：[{summary}]')
            log.debug(f'请求地址：[{ctx.ip}]')
            log.debug(f'请求参数：{args}')

            if request.method != 'OPTIONS':
                log.debug('<-- 请求结束')

            if path.startswith(settings.FASTAPI_API_V1_PATH):
                log.info(f'{ctx.ip: <15} | {method: <8} | {code!s: <6} | {path} | {elapsed:.3f}ms')

            if should_log_opera and request.method != 'OPTIONS':
                opera_log_in = CreateOperaLogParam(
                    trace_id=get_request_trace_id(),
                    username=username,
                    method=method,
                    title=summary,
                    path=path,
                    ip=ctx.ip,
                    country=ctx.country,
                    region=ctx.region,
                    city=ctx.city,
                    user_agent=ctx.user_agent,
                    os=ctx.os,
                    browser=ctx.browser,
                    device=ctx.device,
                    args=args,
                    status=status,
                    code=str(code),
                    msg=msg,
                    cost_time=elapsed,
                    opera_time=ctx.start_time,
                )
                await self.opera_log_queue.put(opera_log_in)
                if settings.GRAFANA_METRICS_ENABLE:
                    observe_queue_size(self.opera_log_queue, queue_name=self.opera_log_queue_name)

        return response

    async def get_request_args(self, request: Request) -> dict[str, Any] | None:  # noqa: C901
        """
        获取请求参数

        :param request: FastAPI 请求对象
        :return:
        """
        args = {}

        # 查询参数
        query_params = dict(request.query_params)
        if query_params:
            args['query_params'] = self.desensitization(query_params)

        # 路径参数
        path_params = request.path_params
        if path_params:
            args['path_params'] = self.desensitization(path_params)

        # Tip: .body() 必须在 .form() 之前获取
        # https://github.com/encode/starlette/discussions/1933
        content_types = [item.strip().lower() for item in request.headers.get('Content-Type', '').split(';')]
        is_multipart = 'multipart/form-data' in content_types
        is_form = is_multipart or 'application/x-www-form-urlencoded' in content_types
        content_length = self.get_content_length(request)
        if content_length is not None and content_length > settings.OPERA_LOG_BODY_MAX_SIZE:
            args['body'] = self.build_truncated_body(content_length, settings.OPERA_LOG_BODY_MAX_SIZE)
            return args or None

        if is_multipart and content_length is None:
            args['body'] = self.build_truncated_body(None, settings.OPERA_LOG_BODY_MAX_SIZE)
            return args or None

        # 请求体
        body_data = await request.body()
        if body_data and not is_form:
            # 注意：非 json 数据默认使用 data 作为键
            if 'application/json' not in content_types:
                args['data'] = body_data.decode('utf-8', 'ignore') if isinstance(body_data, bytes) else str(body_data)
            else:
                json_data = await request.json()
                if isinstance(json_data, dict):
                    args['json'] = self.desensitization(json_data)
                else:
                    args['data'] = str(json_data)

        if is_form:
            # 表单参数
            form_data = await request.form()
            if len(form_data) > 0:
                serialized_form = {}
                for k, v in form_data.items():
                    if isinstance(v, UploadFile):
                        serialized_form[k] = {
                            'filename': v.filename,
                            'content_type': v.content_type,
                            'size': v.size,
                        }
                    else:
                        serialized_form[k] = v
                if not is_multipart:
                    args['x-www-form-urlencoded'] = self.desensitization(serialized_form)
                else:
                    args['form-data'] = self.desensitization(serialized_form)

        if args:
            try:
                args_str = json.dumps(args, ensure_ascii=False)
                args_size = len(args_str.encode('utf-8'))
                if args_size > settings.OPERA_LOG_BODY_MAX_SIZE:
                    args = self.build_truncated_body(args_size, settings.OPERA_LOG_BODY_MAX_SIZE)
            except Exception as e:
                log.error(f'请求参数截断处理失败：{e}')

        return args or None

    @staticmethod
    def get_content_length(request: Request) -> int | None:
        """
        获取请求体大小

        :param request: FastAPI 请求对象
        :return:
        """
        content_length = request.headers.get('Content-Length')
        if not content_length:
            return None
        return int(content_length)

    @staticmethod
    def build_truncated_body(original_size: int | None, max_size: int) -> dict[str, Any]:
        """
        构建请求体截断信息

        :param original_size: 原始请求体大小
        :param max_size: 最大允许记录大小
        :return:
        """
        return {
            '_truncated': True,
            '_original_size': original_size,
            '_max_size': max_size,
            '_message': '请求体过大或大小未知，已跳过操作日志请求体记录',
        }

    @staticmethod
    def desensitization(args: dict[str, Any]) -> dict[str, Any]:
        """
        脱敏处理

        :param args: 需要脱敏的参数字典
        :return:
        """
        for key in args:
            if key in settings.OPERA_LOG_REDACT_KEYS:
                args[key] = '[REDACTED]'
        return args

    @classmethod
    async def consumer(cls) -> None:
        """操作日志消费者"""

        async def bulk_create_opera_log(logs: list[CreateOperaLogParam]) -> None:
            """批量创建操作日志"""
            if settings.DATABASE_ECHO:
                log.info('自动执行【操作日志批量创建】任务...')
            async with async_db_session.begin() as db:
                await opera_log_service.bulk_create(db=db, objs=logs)

        await batch_consume(
            cls.opera_log_queue,
            max_items=settings.OPERA_LOG_QUEUE_BATCH_CONSUME_SIZE,
            timeout=settings.OPERA_LOG_QUEUE_TIMEOUT,
            handler=bulk_create_opera_log,
            queue_name=cls.opera_log_queue_name,
            error_message='操作日志入库失败',
            item_name='日志',
        )
