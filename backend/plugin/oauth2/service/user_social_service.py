import json
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from backend.common.exception import errors
from backend.core.conf import settings
from backend.database.redis import redis_client
from backend.plugin.oauth2.crud.crud_user_social import user_social_dao
from backend.plugin.oauth2.enums import UserSocialAuthType, UserSocialType
from backend.plugin.oauth2.schema.user_social import CreateUserSocialParam


class UserSocialService:
    @staticmethod
    async def get_bindings(*, db: AsyncSession, user_id: int) -> list[str]:
        """
        获取用户已绑定的社交账号

        :param db: 数据库会话
        :param user_id: 用户 ID
        :return: 绑定列表，每个元素包含 sid、source 等信息
        """
        bindings = await user_social_dao.get_by_user_id(db, user_id)
        return [binding.source for binding in bindings]

    @staticmethod
    async def binding_with_oauth2(
        *,
        db: AsyncSession,
        user_id: int,
        sid: str,
        source: UserSocialType,
    ) -> None:
        """
        通过 OAuth2 流程绑定用户社交账号

        :param db: 数据库会话
        :param user_id: 用户 ID
        :param sid: 社交账号唯一编码
        :param source: 绑定源
        :return:
        """
        if await user_social_dao.check_binding(db, user_id, source.value):
            raise errors.RequestError(msg=f'用户已绑定 {source.value} 账号')

        if await user_social_dao.get_by_sid(db, sid, source.value):
            raise errors.RequestError(msg=f'该 {source.value} 账号已被其他用户绑定')

        new_user_social = CreateUserSocialParam(sid=sid, source=source.value, user_id=user_id)
        await user_social_dao.create(db, new_user_social)

    @staticmethod
    async def unbinding(*, db: AsyncSession, user_id: int, source: UserSocialType) -> int:
        """
        解绑用户社交账号

        :param db: 数据库会话
        :param user_id: 用户 ID
        :param source: 解绑源
        :return:
        """
        bind = await user_social_dao.check_binding(db, user_id, source.value)
        if not bind:
            raise errors.NotFoundError(msg=f'用户未绑定 {source.value} 账号')
        return await user_social_dao.delete(db, user_id, source.value)

    @staticmethod
    async def get_binding_auth_url(*, user_id: int, source: UserSocialType) -> str:
        state = str(uuid.uuid4())

        await redis_client.set(
            f'{settings.OAUTH2_STATE_REDIS_PREFIX}:{state}',
            json.dumps({'type': UserSocialAuthType.binding.value, 'user_id': user_id}),
            ex=settings.OAUTH2_STATE_EXPIRE_SECONDS,
        )

        match source:
            case UserSocialType.github:
                from backend.plugin.oauth2.api.v1.github import github_client

                auth_url = await github_client.get_authorization_url(
                    redirect_uri=settings.OAUTH2_GITHUB_REDIRECT_URI,
                    state=state,
                )
            case UserSocialType.google:
                from backend.plugin.oauth2.api.v1.google import google_client

                auth_url = await google_client.get_authorization_url(
                    redirect_uri=settings.OAUTH2_GOOGLE_REDIRECT_URI,
                    state=state,
                )
            case _:
                raise errors.ForbiddenError(msg=f'暂不支持 {source} 绑定')

        return auth_url


user_social_service: UserSocialService = UserSocialService()
