from typing import Any

from fastapi import Request, Response
from fastapi.security.utils import get_authorization_scheme_param
from starlette.authentication import AuthCredentials, AuthenticationBackend
from starlette.authentication import AuthenticationError as StarletteAuthenticationError
from starlette.requests import HTTPConnection

from backend.app.admin.schema.user import GetUserInfoWithRelationDetail
from backend.common.context import ctx
from backend.common.exception.errors import TokenError
from backend.common.log import log
from backend.common.security.jwt import jwt_authentication
from backend.core.conf import settings
from backend.utils.serializers import MsgSpecJSONResponse


class AuthenticationError(StarletteAuthenticationError):
    """重写内部认证错误类"""

    def __init__(
        self,
        *,
        code: int | None = None,
        msg: str | None = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        """
        初始化认证错误类

        :param code: 错误码
        :param msg: 错误信息
        :param headers: 响应头
        :return:
        """
        self.code = code
        self.msg = msg
        self.headers = headers


class JwtAuthMiddleware(AuthenticationBackend):
    """JWT 认证中间件"""

    @staticmethod
    def auth_exception_handler(conn: HTTPConnection, exc: AuthenticationError) -> Response:
        """
        覆盖内部认证错误处理

        :param conn: HTTP 连接对象
        :param exc: 认证错误对象
        :return:
        """
        content = {'code': exc.code, 'msg': exc.msg, 'data': None}
        ctx.__request_authentication_exception__ = content
        return MsgSpecJSONResponse(content=content, status_code=exc.code)

    @staticmethod
    def extract_token(request: Request) -> str | None:
        """
        从请求中提取 Bearer Token

        :param request: FastAPI 请求对象
        :return:
        """
        authorization = request.headers.get('Authorization')
        if not authorization:
            return None

        path = request.url.path
        if path in settings.TOKEN_REQUEST_PATH_EXCLUDE:
            return None
        for pattern in settings.TOKEN_REQUEST_PATH_EXCLUDE_PATTERN:
            if pattern.match(path):
                return None

        scheme, token = get_authorization_scheme_param(authorization)
        if scheme.lower() != 'bearer':
            return None

        return token

    async def authenticate(self, request: Request) -> tuple[AuthCredentials, GetUserInfoWithRelationDetail] | None:
        """
        认证请求

        :param request: FastAPI 请求对象
        :return:
        """
        token = self.extract_token(request)
        if token is None:
            return None

        try:
            user = await jwt_authentication(token)
        except TokenError as exc:
            raise AuthenticationError(code=exc.code, msg=exc.detail, headers=exc.headers)
        except Exception as e:
            log.exception(f'JWT 授权异常：{e}')
            raise AuthenticationError(code=getattr(e, 'code', 500), msg=getattr(e, 'msg', 'Internal Server Error'))

        # 请注意，此返回使用非标准模式，所以在认证通过时，将丢失某些标准特性
        # 标准返回模式请查看：https://www.starlette.io/authentication/
        return AuthCredentials(['authenticated']), user
