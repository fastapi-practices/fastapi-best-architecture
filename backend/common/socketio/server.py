import urllib.parse
import uuid

from typing import Any

import socketio

from starlette_context import request_cycle_context

from backend.common.log import log
from backend.common.security.jwt import jwt_authentication, jwt_decode
from backend.core.conf import settings
from backend.database.redis import redis_client
from backend.utils.timezone import timezone

# 创建 Socket.IO 服务器实例
sio = socketio.AsyncServer(
    client_manager=socketio.AsyncRedisManager(
        f'redis://:{urllib.parse.quote(settings.REDIS_PASSWORD)}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DATABASE}',
        redis_options={
            'socket_timeout': None,
            'socket_connect_timeout': settings.REDIS_TIMEOUT,
        },
    ),
    async_mode='asgi',
    cors_allowed_origins=settings.CORS_ALLOWED_ORIGINS,
    cors_credentials=True,
    namespaces=['/', '/ws'],
)


@sio.event(namespace='*')
async def connect(namespace: str, sid: str, _environ: dict[str, Any], auth: dict[str, Any] | None) -> bool:
    """
    Socket 连接事件

    :param namespace: 命名空间
    :param sid: 连接 ID
    :param _environ: 连接环境
    :param auth: 授权信息
    :return:
    """
    if namespace not in sio.namespaces:
        return False
    if not isinstance(auth, dict):
        log.error('WebSocket 连接失败：无授权')
        return False
    session_uuid = auth.get('session_uuid')
    token = auth.get('token')
    if not isinstance(token, str) or not token or not isinstance(session_uuid, str) or not session_uuid:
        log.error('WebSocket 连接失败：授权失败，请检查')
        return False

    # 免授权直连
    if token == settings.WS_NO_AUTH_MARKER:
        if settings.ENVIRONMENT == 'prod':
            log.error('WebSocket 连接失败：生产环境禁止免授权直连')
            return False
        expire = settings.TOKEN_EXPIRE_SECONDS
    else:
        try:
            with request_cycle_context({settings.TRACE_ID_REQUEST_HEADER_KEY: uuid.uuid4().hex}):
                await jwt_authentication(token)
            token_payload = jwt_decode(token)
        except Exception as e:
            log.info(f'WebSocket 连接失败：{e!s}')
            return False
        session_uuid = token_payload.session_uuid
        expire = int((token_payload.expire_time - timezone.now()).total_seconds())
        if expire <= 0:
            log.info('WebSocket 连接失败：Token 已过期')
            return False

    await sio.save_session(sid, {'session_uuid': session_uuid}, namespace=namespace)
    sid_key = f'{settings.TOKEN_ONLINE_REDIS_PREFIX}:sid:{sid}'
    session_key = f'{settings.TOKEN_ONLINE_REDIS_PREFIX}:session:{session_uuid}'
    await redis_client.set(sid_key, session_uuid, ex=expire)
    await redis_client.sadd(session_key, sid)
    session_ttl = await redis_client.ttl(session_key)
    # 新集合尚无 TTL 时按本次连接设置；多连接取最长剩余寿命
    new_ttl = expire if session_ttl < 0 else max(session_ttl, expire)
    await redis_client.expire(session_key, new_ttl)
    return True


@sio.event(namespace='*')
async def disconnect(namespace: str, sid: str, _reason: str | None = None) -> None:
    """
    Socket 断开连接事件

    :param namespace: 命名空间
    :param sid: 连接 ID
    :param _reason: 断开原因
    :return:
    """
    sid_key = f'{settings.TOKEN_ONLINE_REDIS_PREFIX}:sid:{sid}'
    session_uuid = await redis_client.get(sid_key)
    if not session_uuid:
        try:
            session_data = await sio.get_session(sid, namespace=namespace)
        except KeyError:
            return
        session_uuid = session_data.get('session_uuid')
    if not session_uuid:
        return

    session_key = f'{settings.TOKEN_ONLINE_REDIS_PREFIX}:session:{session_uuid}'
    await redis_client.delete(sid_key)
    await redis_client.srem(session_key, sid)
    remaining = list(await redis_client.smembers(session_key))
    if not remaining:
        return
    mappings = await redis_client.mget_batched([
        f'{settings.TOKEN_ONLINE_REDIS_PREFIX}:sid:{other_sid}' for other_sid in remaining
    ])
    stale_sids = [other_sid for other_sid, mapping in zip(remaining, mappings, strict=True) if mapping != session_uuid]
    if stale_sids:
        await redis_client.srem(session_key, *stale_sids)
