import json
import uuid

from typing import Any
from urllib.parse import urlparse

from fast_captcha import text_captcha
from fastapi import BackgroundTasks, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.crud.crud_user import user_dao
from backend.app.admin.schema.token import GetLoginToken
from backend.app.admin.schema.user import AddOAuth2UserParam
from backend.app.admin.service.login_log_service import login_log_service
from backend.common.context import ctx
from backend.common.enums import LoginLogStatusType
from backend.common.exception import errors
from backend.common.i18n import t
from backend.common.security import jwt
from backend.core.conf import settings
from backend.database.redis import redis_client
from backend.plugin.oauth2.crud.crud_user_social import user_social_dao
from backend.plugin.oauth2.enums import UserSocialAuthType, UserSocialType
from backend.plugin.oauth2.schema.user_social import CreateUserSocialParam
from backend.plugin.oauth2.service.user_social_service import user_social_service
from backend.plugin.oauth2.utils import get_oauth2_authorization_url
from backend.utils.timezone import timezone


class OAuth2Service:
    """OAuth2 认证服务类"""

    async def get_login_auth_url(self, *, db: AsyncSession, request: Request, source: UserSocialType) -> str:
        """
        获取 OAuth2 登录授权链接

        :param db: 数据库会话
        :param request: FastAPI 请求对象
        :param source: 社交平台
        :return:
        """
        tenant_id = settings.TENANT_DEFAULT_ID

        if settings.TENANT_ENABLED:
            try:
                from backend.plugin.tenant.service.tenant_service import tenant_service
            except ImportError:
                raise errors.ServerError(msg='租户插件方法导入失败，请联系系统管理员')

            tenant_domain = request.headers.get('Origin') or request.headers.get('Referer')
            if tenant_domain:
                tenant_domain = urlparse(tenant_domain).hostname
            else:
                tenant_domain = (
                    request.headers.get('X-Forwarded-Host')
                    or request.headers.get('X-Original-Host')
                    or request.url.hostname
                )

            if tenant_domain:
                tenant_domain = tenant_domain.strip().split(',')[0].strip().lower()
                tenant = await tenant_service.get_by_domain(db=db, domain=tenant_domain)
                if tenant:
                    tenant_id = tenant.id
            if tenant_id == settings.TENANT_DEFAULT_ID:
                raise errors.ForbiddenError(msg='OAuth2 登录缺少有效租户上下文')

        state = str(uuid.uuid4())
        await redis_client.setex(
            f'{settings.OAUTH2_STATE_REDIS_PREFIX}:{state}',
            settings.OAUTH2_STATE_EXPIRE_SECONDS,
            json.dumps({'type': UserSocialAuthType.login.value, 'tenant_id': tenant_id}),
        )

        return await get_oauth2_authorization_url(source=source, state=state)

    @staticmethod
    async def login(
        *,
        db: AsyncSession,
        response: Response,
        background_tasks: BackgroundTasks,
        sid: str,
        source: UserSocialType,
        username: str | None = None,
        nickname: str | None = None,
        email: str | None = None,
        avatar: str | None = None,
    ) -> GetLoginToken:
        """
        OAuth2 用户登录

        :param db: 数据库会话
        :param response: FastAPI 响应对象
        :param background_tasks: FastAPI 后台任务
        :param sid: 社交账号唯一编码
        :param source: 社交平台
        :param username: 用户名
        :param nickname: 昵称
        :param email: 邮箱
        :param avatar: 头像地址
        :return:
        """
        user_social = await user_social_dao.get_by_sid(db, ctx.tenant_id, sid, source.value)
        if user_social:
            sys_user = await user_dao.get(db, user_social.user_id)
            # 更新用户头像
            if not sys_user.avatar and avatar is not None:
                await user_dao.update_avatar(db, sys_user.id, avatar)
        else:
            sys_user = None
            # 检测系统用户是否已存在
            if email:
                sys_user = await user_dao.check_email(db, email)

            # 创建系统用户
            if not sys_user:
                base_username = username or text_captcha(5)
                username_candidates = [base_username, *[f'{base_username}_{text_captcha(5)}' for _ in range(10)]]
                existing_users = await user_dao.get_all_by_usernames(db, username_candidates)
                existing_usernames = {user.username for user in existing_users}
                username = next(
                    (candidate for candidate in username_candidates if candidate not in existing_usernames),
                    None,
                )
                if username is None:
                    raise errors.ConflictError(msg='用户名已存在，请重试')
                new_sys_user = AddOAuth2UserParam(
                    username=username,
                    password=None,
                    nickname=nickname,
                    email=email,
                    avatar=avatar,
                )
                await user_dao.add_by_oauth2(db, new_sys_user)
                await db.flush()
                sys_user = await user_dao.get_by_username(db, username)

            # 绑定社交账号
            new_user_social = CreateUserSocialParam(sid=sid, source=source.value, user_id=sys_user.id)
            await user_social_dao.create(db, new_user_social)

        # 创建 token
        access_token_data = await jwt.create_access_token(
            sys_user.id,
            ctx.tenant_id,
            multi_login=sys_user.is_multi_login,
            # extra info
            username=sys_user.username,
            nickname=sys_user.nickname,
            last_login_time=timezone.to_str(timezone.now()),
            ip=ctx.ip,
            os=ctx.os,
            browser=ctx.browser,
            device=ctx.device,
        )
        refresh_token_data = await jwt.create_refresh_token(
            access_token_data.session_uuid,
            sys_user.id,
            ctx.tenant_id,
            multi_login=sys_user.is_multi_login,
        )
        await user_dao.update_login_time(db, sys_user.username)
        await db.refresh(sys_user)
        background_tasks.add_task(
            login_log_service.create,
            user_uuid=sys_user.uuid,
            username=sys_user.username,
            login_time=timezone.now(),
            status=LoginLogStatusType.success.value,
            msg=t('success.login.oauth2_success'),
        )
        await redis_client.delete(f'{settings.LOGIN_CAPTCHA_REDIS_PREFIX}:{ctx.ip}')
        response.set_cookie(
            key=settings.COOKIE_REFRESH_TOKEN_KEY,
            value=refresh_token_data.refresh_token,
            max_age=settings.COOKIE_REFRESH_TOKEN_EXPIRE_SECONDS,
            expires=timezone.to_utc(refresh_token_data.refresh_token_expire_time),
            httponly=True,
        )
        data = GetLoginToken(
            access_token=access_token_data.access_token,
            access_token_expire_time=access_token_data.access_token_expire_time,
            session_uuid=access_token_data.session_uuid,
            user=sys_user,  # type: ignore
        )
        return data

    async def login_or_binding(
        self,
        *,
        db: AsyncSession,
        response: Response,
        background_tasks: BackgroundTasks,
        user: dict[str, Any],
        social: UserSocialType,
        state: str | None = None,
    ) -> GetLoginToken | None:
        """
        OAuth2 登录或绑定

        :param db: 数据库会话
        :param response: FastAPI 响应对象
        :param background_tasks: FastAPI 后台任务
        :param user: OAuth2 用户信息
        :param social: 社交平台类型
        :param state: OAuth2 state 参数
        :return:
        """
        sid = user.get('uuid')
        username = user.get('username')
        nickname = user.get('nickname')
        email = user.get('email')
        avatar = user.get('avatar_url')

        match social:
            case UserSocialType.github:
                sid = user.get('id')
                username = user.get('login')
                nickname = user.get('name')
            case UserSocialType.google:
                sid = user.get('id')
                username = user.get('name')
                nickname = user.get('given_name')
                avatar = user.get('picture')
            case _:
                raise errors.ForbiddenError(msg=f'暂不支持 {social} OAuth2 登录')

        if not state:
            raise errors.ForbiddenError(msg='OAuth2 状态信息缺失')

        state_data = await redis_client.get(f'{settings.OAUTH2_STATE_REDIS_PREFIX}:{state}')
        if not state_data:
            raise errors.ForbiddenError(msg='OAuth2 状态信息无效或缺失')

        state_info = json.loads(state_data)
        await redis_client.delete(f'{settings.OAUTH2_STATE_REDIS_PREFIX}:{state}')
        tenant_id = state_info.get('tenant_id')
        if tenant_id is None:
            raise errors.ForbiddenError(msg='OAuth2 状态信息缺少租户 ID')
        tenant_id = int(tenant_id)
        current_tenant_id = ctx.tenant_id
        ctx.tenant_id = tenant_id

        try:
            await jwt.check_tenant_status(db, tenant_id)

            # 绑定流程
            if state_info.get('type') == UserSocialAuthType.binding.value:
                user_id = state_info.get('user_id')
                if not user_id:
                    raise errors.ForbiddenError(msg='非法操作，OAuth2 状态信息无效')
                await user_social_service.binding_with_oauth2(
                    db=db,
                    user_id=user_id,
                    sid=str(sid),
                    source=social,
                )
                return None

            # 登录流程
            if state_info.get('type') != UserSocialAuthType.login.value:
                raise errors.ForbiddenError(msg='OAuth2 状态信息无效')

            return await self.login(
                db=db,
                response=response,
                background_tasks=background_tasks,
                sid=str(sid),
                source=social,
                username=username,
                nickname=nickname,
                email=email,
                avatar=avatar,
            )
        finally:
            ctx.tenant_id = current_tenant_id


oauth2_service: OAuth2Service = OAuth2Service()
