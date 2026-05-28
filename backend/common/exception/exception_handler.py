from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from uvicorn.protocols.http.h11_impl import STATUS_PHRASES

from backend.common.context import ctx
from backend.common.exception.errors import BaseExceptionError
from backend.common.i18n import i18n, t
from backend.common.response.response_code import CustomResponseCode, StandardResponseCode
from backend.common.response.response_schema import response_base
from backend.core.conf import settings
from backend.utils.serializers import MsgSpecJSONResponse
from backend.utils.trace_id import get_request_trace_id


def _get_exception_code(status_code: int) -> int:
    """
    获取返回状态码（可用状态码基于 RFC 定义）

    `python 状态码标准支持 <https://github.com/python/cpython/blob/6e3cc72afeaee2532b4327776501eb8234ac787b/Lib/http/__init__.py#L7>`__

    `IANA 状态码注册表 <https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml>`__

    :param status_code: HTTP 状态码
    :return:
    """
    try:
        STATUS_PHRASES[status_code]
    except Exception:
        return StandardResponseCode.HTTP_400

    return status_code


async def _validation_exception_handler(exc: RequestValidationError | ValidationError):
    """
    数据验证异常处理

    :param exc: 验证异常
    :return:
    """
    errors = []
    for error in exc.errors():
        # 非 en-US 语言下，使用自定义错误信息
        if i18n.current_language != 'en-US':
            custom_message = t(f'pydantic.{error["type"]}')
            if custom_message:
                error_ctx = error.get('ctx')
                if not error_ctx:
                    error['msg'] = custom_message
                else:
                    e = error_ctx.get('error')
                    if e:
                        error['msg'] = custom_message.format(**error_ctx)
                        error['ctx']['error'] = e.__str__().replace("'", '"') if isinstance(e, Exception) else None
        errors.append(error)
    error = errors[0]
    if error.get('type') == 'json_invalid':
        message = 'json解析失败'
    else:
        error_input = error.get('input')
        field = str(error.get('loc')[-1])
        error_msg = error.get('msg')
        message = f'{field} {error_msg}，输入：{error_input}' if settings.ENVIRONMENT == 'dev' else error_msg
    msg = f'请求参数非法: {message}'
    data = {'errors': errors} if settings.ENVIRONMENT == 'dev' else None
    content = {
        'code': StandardResponseCode.HTTP_422,
        'msg': msg,
        'data': data,
    }
    ctx.__request_validation_exception__ = content  # 用于在中间件中获取异常信息
    content.update(trace_id=get_request_trace_id())
    return MsgSpecJSONResponse(status_code=StandardResponseCode.HTTP_422, content=content)


def register_exception(app: FastAPI) -> None:  # noqa: C901
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        全局 HTTP 异常处理

        :param request: FastAPI 请求对象
        :param exc: HTTP 异常
        :return:
        """
        if settings.ENVIRONMENT == 'dev':
            content = {
                'code': exc.status_code,
                'msg': exc.detail,
                'data': None,
            }
        else:
            res = response_base.fail(res=CustomResponseCode.HTTP_400)
            content = res.model_dump()
        ctx.__request_http_exception__ = content
        content.update(trace_id=get_request_trace_id())
        return MsgSpecJSONResponse(
            status_code=_get_exception_code(exc.status_code),
            content=content,
            headers=exc.headers,
        )

    @app.exception_handler(RequestValidationError)
    async def fastapi_validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        FastAPI 数据验证异常处理

        :param request: FastAPI 请求对象
        :param exc: 验证异常
        :return:
        """
        return await _validation_exception_handler(exc)

    @app.exception_handler(ValidationError)
    async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
        """
        Pydantic 数据验证异常处理

        :param request: 请求对象
        :param exc: 验证异常
        :return:
        """
        return await _validation_exception_handler(exc)

    @app.exception_handler(AssertionError)
    async def assertion_error_handler(request: Request, exc: AssertionError):
        """
        断言错误处理

        :param request: FastAPI 请求对象
        :param exc: 断言错误
        :return:
        """
        if settings.ENVIRONMENT == 'dev':
            content = {
                'code': StandardResponseCode.HTTP_500,
                'msg': str(''.join(exc.args) if exc.args else exc.__doc__),
                'data': None,
            }
        else:
            res = response_base.fail(res=CustomResponseCode.HTTP_500)
            content = res.model_dump()
        ctx.__request_assertion_error__ = content
        content.update(trace_id=get_request_trace_id())
        return MsgSpecJSONResponse(
            status_code=StandardResponseCode.HTTP_500,
            content=content,
        )

    @app.exception_handler(BaseExceptionError)
    async def custom_exception_handler(request: Request, exc: BaseExceptionError):
        """
        全局自定义异常处理

        :param request: FastAPI 请求对象
        :param exc: 自定义异常
        :return:
        """
        content = {
            'code': exc.code,
            'msg': str(exc.msg),
            'data': exc.data or None,
        }
        ctx.__request_custom_exception__ = content
        content.update(trace_id=get_request_trace_id())
        return MsgSpecJSONResponse(
            status_code=_get_exception_code(exc.code),
            content=content,
            background=exc.background,
        )

    @app.exception_handler(Exception)
    async def all_unknown_exception_handler(request: Request, exc: Exception):
        """
        全局未知异常处理

        :param request: FastAPI 请求对象
        :param exc: 未知异常
        :return:
        """
        if settings.ENVIRONMENT == 'dev':
            content = {
                'code': StandardResponseCode.HTTP_500,
                'msg': str(exc),
                'data': None,
            }
        else:
            res = response_base.fail(res=CustomResponseCode.HTTP_500)
            content = res.model_dump()
        ctx.__request_unknown_exception__ = content
        content.update(trace_id=get_request_trace_id())
        return MsgSpecJSONResponse(
            status_code=StandardResponseCode.HTTP_500,
            content=content,
        )

    if settings.MIDDLEWARE_CORS:

        @app.exception_handler(StandardResponseCode.HTTP_500)
        async def cors_custom_code_500_exception_handler(request: Request, exc: BaseExceptionError | Exception):
            """
            跨域自定义 500 异常处理

            :param request: FastAPI 请求对象
            :param exc: 自定义异常
            :return:
            """
            if isinstance(exc, BaseExceptionError):
                content = {
                    'code': exc.code,
                    'msg': exc.msg,
                    'data': exc.data,
                }
            else:
                if settings.ENVIRONMENT == 'dev':
                    content = {
                        'code': StandardResponseCode.HTTP_500,
                        'msg': str(exc),
                        'data': None,
                    }
                else:
                    res = response_base.fail(res=CustomResponseCode.HTTP_500)
                    content = res.model_dump()
            if isinstance(exc, BaseExceptionError):
                ctx.__request_custom_exception__ = content
            else:
                ctx.__request_unknown_exception__ = content
            content.update(trace_id=get_request_trace_id())
            response = MsgSpecJSONResponse(
                status_code=exc.code if isinstance(exc, BaseExceptionError) else StandardResponseCode.HTTP_500,
                content=content,
                background=exc.background if isinstance(exc, BaseExceptionError) else None,
            )
            origin = request.headers.get('origin')
            if origin:
                cors = CORSMiddleware(
                    app=app,
                    allow_origins=settings.CORS_ALLOWED_ORIGINS,
                    allow_credentials=True,
                    allow_methods=['*'],
                    allow_headers=['*'],
                    expose_headers=settings.CORS_EXPOSE_HEADERS,
                )
                response.headers.update(cors.simple_headers)
                has_cookie = 'cookie' in request.headers
                if cors.allow_all_origins and has_cookie:
                    response.headers['Access-Control-Allow-Origin'] = origin
                elif not cors.allow_all_origins and cors.is_allowed_origin(origin=origin):
                    response.headers['Access-Control-Allow-Origin'] = origin
                    response.headers.add_vary_header('Origin')
            return response
