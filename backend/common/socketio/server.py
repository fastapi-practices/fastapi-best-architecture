import urllib.parse
import uuid

import socketio

from starlette_context import request_cycle_context

from backend.common.log import log
from backend.common.security.jwt import jwt_authentication
from backend.core.conf import settings
from backend.database.redis import redis_client

# 创建 Socket.IO 服务器实例
sio = socketio.AsyncServer(
    client_manager=socketio.AsyncRedisManager(
        f'redis://:{urllib.parse.quote(settings.REDIS_PASSWORD)}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DATABASE}',
    ),
    async_mode='asgi',
    cors_allowed_origins=settings.CORS_ALLOWED_ORIGINS,
    cors_credentials=True,
    namespaces=['/ws'],
)


@sio.event
async def connect(sid, environ, auth) -> bool:
    """Socket 连接事件"""
    if not auth:
        log.error('WebSocket 连接失败：无授权')
        return False

    session_uuid = auth.get('session_uuid')
    token = auth.get('token')
    if not token or not session_uuid:
        log.error('WebSocket 连接失败：授权失败，请检查')
        return False

    # 免授权直连
    if token == settings.WS_NO_AUTH_MARKER:
        if settings.ENVIRONMENT == 'prod':
            log.error('WebSocket 连接失败：生产环境禁止免授权直连')
            return False
        await redis_client.set(f'{settings.TOKEN_ONLINE_REDIS_PREFIX}:sid:{sid}', session_uuid)
        await redis_client.sadd(f'{settings.TOKEN_ONLINE_REDIS_PREFIX}:session:{session_uuid}', sid)
        await redis_client.sadd(settings.TOKEN_ONLINE_REDIS_PREFIX, session_uuid)
        return True

    try:
        with request_cycle_context({settings.TRACE_ID_REQUEST_HEADER_KEY: uuid.uuid4().hex}):
            await jwt_authentication(token)
    except Exception as e:
        log.info(f'WebSocket 连接失败：{e!s}')
        return False

    await redis_client.set(f'{settings.TOKEN_ONLINE_REDIS_PREFIX}:sid:{sid}', session_uuid)
    await redis_client.sadd(f'{settings.TOKEN_ONLINE_REDIS_PREFIX}:session:{session_uuid}', sid)
    await redis_client.sadd(settings.TOKEN_ONLINE_REDIS_PREFIX, session_uuid)
    return True


@sio.event
async def disconnect(sid) -> None:
    """Socket 断开连接事件"""
    session_uuid = await redis_client.get(f'{settings.TOKEN_ONLINE_REDIS_PREFIX}:sid:{sid}')
    if not session_uuid:
        return

    session_key = f'{settings.TOKEN_ONLINE_REDIS_PREFIX}:session:{session_uuid}'
    await redis_client.delete(f'{settings.TOKEN_ONLINE_REDIS_PREFIX}:sid:{sid}')
    await redis_client.srem(session_key, sid)
    if await redis_client.scard(session_key) == 0:
        await redis_client.delete(session_key)
        await redis_client.srem(settings.TOKEN_ONLINE_REDIS_PREFIX, session_uuid)
