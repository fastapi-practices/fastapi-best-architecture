import asyncio
import json
import uuid

from datetime import timedelta
from typing import Any

from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param

from backend.common.dataclasses import AccessToken, NewToken, RefreshToken
from backend.common.exception import errors
from backend.common.security.jwt import jwt_encode
from backend.core.conf import settings
from backend.database.redis import redis_client
from backend.utils.timezone import timezone

_socket_disconnect_tasks: set[asyncio.Task[None]] = set()
_REDIS_BATCH_SIZE = 1000


def get_token(request: Request) -> str:
    """
    获取请求头中的 token

    :param request: FastAPI 请求对象
    :return:
    """
    authorization = request.headers.get('Authorization')
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != 'bearer':
        raise errors.TokenError(msg='Token 无效')
    return token


async def _srem_members(key: str, members: list[str] | set[str]) -> None:
    """
    分批从集合中移除成员

    :param key: 集合 key
    :param members: 要移除的成员
    :return:
    """
    ordered = list(members)
    if not ordered:
        return
    for index in range(0, len(ordered), _REDIS_BATCH_SIZE):
        await redis_client.srem(key, *ordered[index : index + _REDIS_BATCH_SIZE])


async def get_user_sessions(user_id: int) -> set[str]:
    """
    读取有效正式会话

    :param user_id: 用户 ID
    :return:
    """
    index_key = f'{settings.TOKEN_SESSION_REDIS_PREFIX}:{user_id}'
    users_key = f'{settings.TOKEN_SESSION_REDIS_PREFIX}:users'
    swagger_key = f'{settings.TOKEN_SESSION_REDIS_PREFIX}:{user_id}:swagger'
    indexed = set(await redis_client.smembers(index_key))

    live_sessions: set[str] = set()
    swagger_sessions: set[str] = set()
    if indexed:
        ordered = list(indexed)
        access_tokens, refresh_tokens, extras = await asyncio.gather(
            redis_client.mget_batched([
                f'{settings.TOKEN_REDIS_PREFIX}:{user_id}:{session_uuid}' for session_uuid in ordered
            ]),
            redis_client.mget_batched([
                f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{user_id}:{session_uuid}' for session_uuid in ordered
            ]),
            redis_client.mget_batched([
                f'{settings.TOKEN_EXTRA_INFO_REDIS_PREFIX}:{user_id}:{session_uuid}' for session_uuid in ordered
            ]),
        )
        for session_uuid, access, refresh, extra in zip(ordered, access_tokens, refresh_tokens, extras, strict=True):
            extra_info = None
            if extra:
                try:
                    extra_info = json.loads(extra)
                except (json.JSONDecodeError, TypeError):
                    extra_info = None
            if isinstance(extra_info, dict) and extra_info.get('swagger') is not None:
                swagger_sessions.add(session_uuid)
                continue
            if access or refresh:
                live_sessions.add(session_uuid)
        if swagger_sessions:
            await _srem_members(index_key, swagger_sessions)
            async with redis_client.pipeline(transaction=False) as pipe:
                pipe.sadd(swagger_key, *swagger_sessions)
                pipe.expire(swagger_key, settings.TOKEN_EXPIRE_SECONDS)
                await pipe.execute()

    drop_from_index = indexed - live_sessions
    session_ttl = max(settings.TOKEN_EXPIRE_SECONDS, settings.TOKEN_REFRESH_EXPIRE_SECONDS)
    async with redis_client.pipeline(transaction=False) as pipe:
        if drop_from_index:
            pipe.srem(index_key, *drop_from_index)
        if live_sessions:
            pipe.expire(index_key, session_ttl)
            pipe.sadd(users_key, str(user_id))
        else:
            pipe.delete(index_key)
            pipe.srem(users_key, str(user_id))
        await pipe.execute()
    return live_sessions


async def create_access_token(
    user_id: int,
    *,
    multi_login: bool,
    session_uuid: str | None = None,
    swagger: bool = False,
    **kwargs: Any,
) -> AccessToken:
    """
    生成加密 token

    :param user_id: 用户 ID
    :param multi_login: 是否允许多端登录
    :param session_uuid: 复用已有会话 UUID，刷新令牌时保持在线状态连续
    :param swagger: 是否为 swagger 调试 token，不写入会话索引且不踢其他端
    :param kwargs: token 额外信息
    :return:
    """
    expire = timezone.now() + timedelta(seconds=settings.TOKEN_EXPIRE_SECONDS)
    session_uuid = session_uuid or str(uuid.uuid4())
    access_token = jwt_encode({
        'session_uuid': session_uuid,
        'jti': str(uuid.uuid4()),
        'exp': timezone.to_utc(expire).timestamp(),
        'sub': str(user_id),
    })

    if not swagger and not multi_login:
        await revoke_user_tokens(user_id, exclude_session_uuid=session_uuid, include_swagger=False)

    extra_info = {'swagger': True, **kwargs} if swagger else kwargs
    extra_ttl = (
        settings.TOKEN_EXPIRE_SECONDS
        if swagger
        else max(settings.TOKEN_EXPIRE_SECONDS, settings.TOKEN_REFRESH_EXPIRE_SECONDS)
    )
    session_ttl = max(settings.TOKEN_EXPIRE_SECONDS, settings.TOKEN_REFRESH_EXPIRE_SECONDS)
    async with redis_client.pipeline(transaction=False) as pipe:
        pipe.set(
            f'{settings.TOKEN_REDIS_PREFIX}:{user_id}:{session_uuid}',
            access_token,
            ex=settings.TOKEN_EXPIRE_SECONDS,
        )
        if extra_info:
            pipe.set(
                f'{settings.TOKEN_EXTRA_INFO_REDIS_PREFIX}:{user_id}:{session_uuid}',
                json.dumps(extra_info, ensure_ascii=False),
                ex=extra_ttl,
            )
        if swagger:
            swagger_key = f'{settings.TOKEN_SESSION_REDIS_PREFIX}:{user_id}:swagger'
            pipe.sadd(swagger_key, session_uuid)
            pipe.expire(swagger_key, settings.TOKEN_EXPIRE_SECONDS)
        else:
            index_key = f'{settings.TOKEN_SESSION_REDIS_PREFIX}:{user_id}'
            pipe.sadd(index_key, session_uuid)
            pipe.expire(index_key, session_ttl)
            pipe.sadd(
                f'{settings.TOKEN_SESSION_REDIS_PREFIX}:users',
                str(user_id),
            )
        await pipe.execute()

    return AccessToken(access_token=access_token, access_token_expire_time=expire, session_uuid=session_uuid)


async def create_refresh_token(session_uuid: str, user_id: int, *, multi_login: bool) -> RefreshToken:
    """
    生成加密刷新 token，仅用于创建新的 token

    :param session_uuid: 会话 UUID
    :param user_id: 用户 ID
    :param multi_login: 是否允许多端登录
    :return:
    """
    expire = timezone.now() + timedelta(seconds=settings.TOKEN_REFRESH_EXPIRE_SECONDS)
    refresh_token = jwt_encode({
        'session_uuid': session_uuid,
        'jti': str(uuid.uuid4()),
        'exp': timezone.to_utc(expire).timestamp(),
        'sub': str(user_id),
    })

    session_ttl = max(settings.TOKEN_EXPIRE_SECONDS, settings.TOKEN_REFRESH_EXPIRE_SECONDS)
    index_key = f'{settings.TOKEN_SESSION_REDIS_PREFIX}:{user_id}'
    async with redis_client.pipeline(transaction=False) as pipe:
        pipe.set(
            f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{user_id}:{session_uuid}',
            refresh_token,
            ex=settings.TOKEN_REFRESH_EXPIRE_SECONDS,
        )
        pipe.sadd(index_key, session_uuid)
        pipe.expire(index_key, session_ttl)
        pipe.sadd(f'{settings.TOKEN_SESSION_REDIS_PREFIX}:users', str(user_id))
        await pipe.execute()

    return RefreshToken(refresh_token=refresh_token, refresh_token_expire_time=expire)


async def create_new_token(
    refresh_token: str,
    session_uuid: str,
    user_id: int,
    *,
    multi_login: bool,
    **kwargs: Any,
) -> NewToken:
    """
    生成新的 token

    :param refresh_token: 刷新 token
    :param session_uuid: 会话 UUID
    :param user_id: 用户 ID
    :param multi_login: 是否允许多端登录
    :param kwargs: token 附加信息
    :return:
    """
    redis_refresh_token = await redis_client.get(f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{user_id}:{session_uuid}')
    if not redis_refresh_token or redis_refresh_token != refresh_token:
        raise errors.TokenError(msg='Refresh Token 已过期，请重新登录')

    new_access_token = await create_access_token(
        user_id,
        multi_login=multi_login,
        session_uuid=session_uuid,
        **kwargs,
    )
    new_refresh_token = await create_refresh_token(session_uuid, user_id, multi_login=multi_login)

    return NewToken(
        new_access_token=new_access_token.access_token,
        new_access_token_expire_time=new_access_token.access_token_expire_time,
        new_refresh_token=new_refresh_token.refresh_token,
        new_refresh_token_expire_time=new_refresh_token.refresh_token_expire_time,
        session_uuid=session_uuid,
    )


async def _revoke_sessions(user_id: int, session_uuids: set[str]) -> None:
    """
    批量删除会话相关 key，并异步断开 socket

    :param user_id: 用户 ID
    :param session_uuids: 要撤销的会话 UUID
    :return:
    """
    if not session_uuids:
        return

    ordered = list(session_uuids)
    sid_sets = await redis_client.smembers_many([
        f'{settings.TOKEN_ONLINE_REDIS_PREFIX}:session:{session_uuid}' for session_uuid in ordered
    ])
    sids = [sid for members in sid_sets for sid in members]
    delete_keys: list[str] = []
    for session_uuid in ordered:
        delete_keys.extend((
            f'{settings.TOKEN_REDIS_PREFIX}:{user_id}:{session_uuid}',
            f'{settings.TOKEN_EXTRA_INFO_REDIS_PREFIX}:{user_id}:{session_uuid}',
            f'{settings.TOKEN_REFRESH_REDIS_PREFIX}:{user_id}:{session_uuid}',
            f'{settings.TOKEN_ONLINE_REDIS_PREFIX}:session:{session_uuid}',
        ))
    delete_keys.extend(f'{settings.TOKEN_ONLINE_REDIS_PREFIX}:sid:{sid}' for sid in sids)
    await redis_client.delete_batched(delete_keys)
    await asyncio.gather(
        _srem_members(
            f'{settings.TOKEN_SESSION_REDIS_PREFIX}:{user_id}',
            ordered,
        ),
        _srem_members(
            f'{settings.TOKEN_SESSION_REDIS_PREFIX}:{user_id}:swagger',
            ordered,
        ),
    )
    if not await redis_client.smembers(f'{settings.TOKEN_SESSION_REDIS_PREFIX}:{user_id}'):
        await redis_client.srem(f'{settings.TOKEN_SESSION_REDIS_PREFIX}:users', str(user_id))

    if sids:
        from backend.common.socketio.server import sio

        for sid in sids:
            for namespace in ('/', '/ws'):
                task = sio.start_background_task(sio.disconnect, sid, namespace=namespace)
                _socket_disconnect_tasks.add(task)
                task.add_done_callback(_socket_disconnect_tasks.discard)


async def revoke_token(user_id: int, session_uuid: str) -> None:
    """
    撤销 token

    :param user_id: 用户 ID
    :param session_uuid: 会话 ID
    :return:
    """
    await _revoke_sessions(user_id, {session_uuid})


async def revoke_user_tokens(
    user_id: int,
    *,
    exclude_session_uuid: str | None = None,
    include_swagger: bool = True,
) -> None:
    """
    撤销用户全部会话，可保留当前会话

    :param user_id: 用户 ID
    :param exclude_session_uuid: 需要保留的会话 UUID
    :param include_swagger: 是否同时撤销 swagger 调试 token
    :return:
    """
    session_uuids = await get_user_sessions(user_id)
    if include_swagger:
        session_uuids |= set(await redis_client.smembers(f'{settings.TOKEN_SESSION_REDIS_PREFIX}:{user_id}:swagger'))
    if exclude_session_uuid:
        session_uuids.discard(exclude_session_uuid)
    await _revoke_sessions(user_id, session_uuids)
