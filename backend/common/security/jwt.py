from typing import Annotated, Any, Protocol

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt
from starlette.authentication import UnauthenticatedUser

from backend.common.context import ctx
from backend.common.dataclasses import TokenPayload
from backend.common.exception import errors
from backend.core.conf import settings
from backend.database.redis import redis_client
from backend.utils.timezone import timezone


class JwtUser(Protocol):
    """JWT 认证用户协议，只约定通用安全模块需要读取的字段"""

    is_superuser: bool


class JwtUserProvider(Protocol):
    """JWT 用户提供者协议，由持有用户体系的应用实现，并在应用启动时注册"""

    async def __call__(self, *, user_id: int) -> JwtUser:
        """
        获取 JWT 认证用户

        :param user_id: 用户 ID
        :return:
        """


_jwt_user_provider: JwtUserProvider | None = None


def register_jwt_user_provider(provider: JwtUserProvider) -> None:
    """
    注册 JWT 用户提供者

    :param provider: JWT 用户提供者
    :return:
    """
    global _jwt_user_provider
    _jwt_user_provider = provider


def jwt_encode(payload: dict[str, Any]) -> str:
    """
    生成 JWT token

    :param payload: 载荷
    :return:
    """
    return jwt.encode(payload, settings.TOKEN_SECRET_KEY, settings.TOKEN_ALGORITHM)


def jwt_decode(token: str) -> TokenPayload:
    """
    解析 JWT token

    :param token: JWT token
    :return:
    """
    try:
        payload = jwt.decode(
            token,
            settings.TOKEN_SECRET_KEY,
            algorithms=[settings.TOKEN_ALGORITHM],
            options={'verify_exp': True},
        )
        session_uuid = payload.get('session_uuid')
        user_id = payload.get('sub')
        expire = payload.get('exp')
        if not session_uuid or not user_id or not expire:
            raise errors.TokenError(msg='Token 无效')
    except ExpiredSignatureError:
        raise errors.TokenError(msg='Token 已过期')
    except (JWTError, Exception):
        raise errors.TokenError(msg='Token 无效')
    return TokenPayload(
        user_id=int(user_id),
        session_uuid=session_uuid,
        expire_time=timezone.from_datetime(timezone.to_utc(expire)),
    )


async def jwt_authentication(token: str) -> JwtUser:
    """
    JWT 认证

    :param token: JWT token
    :return:
    """
    token_payload = jwt_decode(token)
    ctx.user_id = token_payload.user_id
    redis_token = await redis_client.get(f'{settings.TOKEN_REDIS_PREFIX}:{ctx.user_id}:{token_payload.session_uuid}')
    if not redis_token:
        raise errors.TokenError(msg='Token 已过期')
    if token != redis_token:
        raise errors.TokenError(msg='Token 已失效')
    if _jwt_user_provider is None:
        raise RuntimeError('JWT 用户提供者未注册，请在应用启动时调用 register_jwt_user_provider')

    user = await _jwt_user_provider(user_id=ctx.user_id)
    ctx.is_superuser = user.is_superuser

    return user


def jwt_authentication_verify(
    request: Request,
    token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
) -> str:
    """
    JWT 认证依赖

    :param request: FastAPI 请求对象
    :param token: HTTP Bearer 认证信息
    :return:
    """
    if isinstance(request.user, UnauthenticatedUser):
        if token_exception := ctx.get('__request_jwt_authentication_exception__'):
            raise token_exception
        raise errors.TokenError
    return token.credentials


# JWT 依赖注入
DependsJwtAuth = Depends(jwt_authentication_verify)


def superuser_verify(request: Request, _token: str = DependsJwtAuth) -> bool:
    """
    验证当前用户超级管理员权限

    :param request: FastAPI 请求对象
    :param _token: JWT 令牌
    :return:
    """
    if isinstance(request.user, UnauthenticatedUser):
        raise errors.TokenError
    superuser = request.user.is_superuser
    if not superuser or not request.user.is_staff:
        raise errors.AuthorizationError
    return superuser


# 超级管理员鉴权依赖注入
DependsSuperUser = Depends(superuser_verify)
