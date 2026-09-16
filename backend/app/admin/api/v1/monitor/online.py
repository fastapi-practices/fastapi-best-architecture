import json

from typing import TYPE_CHECKING, Annotated, Any

from fastapi import APIRouter, Path, Query

from backend.app.admin.schema.token import GetTokenDetail
from backend.common.enums import StatusType
from backend.common.exception import errors
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsSuperUser, jwt_decode
from backend.common.security.token import revoke_token
from backend.core.conf import settings
from backend.database.redis import redis_client

if TYPE_CHECKING:
    from backend.common.dataclasses import TokenPayload

router = APIRouter()


@router.get('', summary='获取在线用户', dependencies=[DependsSuperUser])
async def get_sessions(  # ruff:ignore[complex-structure]
    username: Annotated[str | None, Query(description='用户名')] = None,
) -> ResponseSchemaModel[list[GetTokenDetail]]:
    users_key = f'{settings.TOKEN_SESSION_REDIS_PREFIX}:users'
    user_ids = list(await redis_client.smembers(users_key))
    if not user_ids:
        return response_base.success(data=[])

    session_sets = await redis_client.smembers_many([
        f'{settings.TOKEN_SESSION_REDIS_PREFIX}:{user_id}' for user_id in user_ids
    ])
    session_refs: list[tuple[str, str]] = []
    for user_id, members in zip(user_ids, session_sets, strict=True):
        session_refs.extend((user_id, session_uuid) for session_uuid in members)
    if not session_refs:
        await redis_client.srem(users_key, *user_ids)
        return response_base.success(data=[])

    tokens = await redis_client.mget_batched([
        f'{settings.TOKEN_REDIS_PREFIX}:{user_id}:{session_uuid}' for user_id, session_uuid in session_refs
    ])
    token_payloads: list[TokenPayload] = []
    live_user_ids: set[str] = set()
    for (user_id, _session_uuid), token in zip(session_refs, tokens, strict=True):
        if not token:
            continue
        try:
            token_payloads.append(jwt_decode(token))
        except errors.TokenError:
            continue
        live_user_ids.add(user_id)
    stale_user_ids = [user_id for user_id in user_ids if user_id not in live_user_ids]
    if stale_user_ids:
        await redis_client.srem(users_key, *stale_user_ids)
    if not token_payloads:
        return response_base.success(data=[])

    extra_infos = await redis_client.mget_batched([
        f'{settings.TOKEN_EXTRA_INFO_REDIS_PREFIX}:{item.user_id}:{item.session_uuid}' for item in token_payloads
    ])
    sid_sets = await redis_client.smembers_many([
        f'{settings.TOKEN_ONLINE_REDIS_PREFIX}:session:{item.session_uuid}' for item in token_payloads
    ])
    sid_list = [sid for members in sid_sets for sid in members]
    sid_values = await redis_client.mget_batched([
        f'{settings.TOKEN_ONLINE_REDIS_PREFIX}:sid:{sid}' for sid in sid_list
    ])
    sid_session_map = dict(zip(sid_list, sid_values, strict=True))
    online_sessions = {
        item.session_uuid
        for item, members in zip(token_payloads, sid_sets, strict=True)
        if any(sid_session_map.get(sid) == item.session_uuid for sid in members)
    }
    data: list[GetTokenDetail] = []
    for token_payload, extra_info in zip(token_payloads, extra_infos, strict=True):
        info: dict[str, Any] = {}
        if extra_info:
            try:
                parsed = json.loads(extra_info)
            except (json.JSONDecodeError, TypeError):
                parsed = None
            if isinstance(parsed, dict):
                info = parsed
        if info.get('swagger') is not None:
            continue
        if username is not None and username != info.get('username'):
            continue
        data.append(
            GetTokenDetail(
                id=token_payload.user_id,
                session_uuid=token_payload.session_uuid,
                username=info.get('username', '未知'),
                nickname=info.get('nickname', '未知'),
                ip=info.get('ip', '未知'),
                os=info.get('os', '未知'),
                browser=info.get('browser', '未知'),
                device=info.get('device', '未知'),
                status=StatusType.enable if token_payload.session_uuid in online_sessions else StatusType.disable,
                last_login_time=info.get('last_login_time', '未知'),
                expire_time=token_payload.expire_time,
            )
        )
    data.sort(key=lambda item: (item.id, item.session_uuid))
    return response_base.success(data=data)


@router.delete(
    '/{pk}',
    summary='强制下线',
    dependencies=[DependsSuperUser],
)
async def delete_session(
    pk: Annotated[int, Path(description='用户 ID')],
    session_uuid: Annotated[str, Query(description='会话 UUID')],
) -> ResponseModel:
    await revoke_token(pk, session_uuid)
    return response_base.success()
