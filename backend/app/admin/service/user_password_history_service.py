import math

from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.crud.crud_user_password_history import user_password_history_dao
from backend.app.admin.schema.user_password_history import CreateUserPasswordHistoryParam
from backend.common.exception import errors
from backend.core.conf import settings
from backend.database.redis import redis_client
from backend.utils.dynamic_config import load_user_security_config
from backend.utils.timezone import timezone


class UserPasswordHistoryService:
    """用户密码历史服务类"""

    @staticmethod
    async def check_status(user_id: int, user_status: int) -> None:
        """
        检查用户状态

        :param user_id: 用户 ID
        :param user_status: 用户状态
        :return:
        """
        if not user_status:
            raise errors.AuthorizationError(msg='用户已被锁定, 请联系统管理员')

        locked_until_str = await redis_client.get(f'{settings.USER_LOCK_REDIS_PREFIX}:{user_id}')

        if locked_until_str:
            locked_until = timezone.from_str(locked_until_str)
            now = timezone.now()
            if locked_until > now:
                remaining_minutes = math.ceil((locked_until - now).total_seconds() / 60)
                raise errors.AuthorizationError(msg=f'账号已被锁定，请在 {remaining_minutes} 分钟后重试')

            await redis_client.delete(f'{settings.USER_LOCK_REDIS_PREFIX}:{user_id}')
            await redis_client.delete(f'{settings.LOGIN_FAILURE_PREFIX}:{user_id}')

    @staticmethod
    async def handle_login_failure(db: AsyncSession, user_id: int) -> None:
        """
        处理登录失败

        :param db: 数据库会话
        :param user_id: 用户 ID
        :return:
        """
        await load_user_security_config(db)

        if settings.USER_LOCK_THRESHOLD == 0:
            return

        failure_count = await redis_client.get(f'{settings.LOGIN_FAILURE_PREFIX}:{user_id}')
        failure_count = int(failure_count) if failure_count else 0
        failure_count += 1
        await redis_client.set(
            f'{settings.LOGIN_FAILURE_PREFIX}:{user_id}',
            str(failure_count),
            ex=settings.USER_LOCK_SECONDS,
        )

        if failure_count >= settings.USER_LOCK_THRESHOLD:
            locked_until = timezone.now() + timedelta(seconds=settings.USER_LOCK_SECONDS)
            await redis_client.set(
                f'{settings.USER_LOCK_REDIS_PREFIX}:{user_id}',
                timezone.to_str(locked_until),
                ex=settings.USER_LOCK_SECONDS,
            )
            raise errors.AuthorizationError(msg='登录失败次数过多，账号已被锁定')

    @staticmethod
    async def check_password_expiry_status(db: AsyncSession, password_changed_time: datetime) -> int | None:
        """
        检查密码过期状态

        :param db: 数据库会话
        :param password_changed_time: 密码修改时间
        :return:
        """
        await load_user_security_config(db)

        if settings.USER_PASSWORD_EXPIRY_DAYS == 0:
            return None

        if not password_changed_time:
            raise errors.AuthorizationError(msg='密码已过期，请修改密码后重新登录')

        expiry_time = password_changed_time + timedelta(days=settings.USER_PASSWORD_EXPIRY_DAYS)
        days_remaining = (expiry_time - timezone.now()).days

        if days_remaining < 0:
            raise errors.AuthorizationError(msg='密码已过期，请修改密码后重新登录')

        if days_remaining <= settings.USER_PASSWORD_REMINDER_DAYS:
            return days_remaining

        return None

    @staticmethod
    async def handle_login_success(user_id: int) -> None:
        """
        处理登录成功

        :param user_id: 用户 ID
        :return:
        """
        await redis_client.delete(f'{settings.USER_LOCK_REDIS_PREFIX}:{user_id}')
        await redis_client.delete(f'{settings.LOGIN_FAILURE_PREFIX}:{user_id}')

    @staticmethod
    async def save_password_history(db: AsyncSession, obj: CreateUserPasswordHistoryParam) -> None:
        """
        保存密码历史记录

        :param db: 数据库会话
        :param obj: 创建密码历史记录参数
        :return:
        """
        await user_password_history_dao.create(db, obj)


password_security_service: UserPasswordHistoryService = UserPasswordHistoryService()
