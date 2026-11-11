from collections.abc import Sequence

from pydantic_core import from_json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.model import data_scope_rule, role_data_scope, role_menu, user_role
from backend.app.admin.schema.user import GetUserInfoWithRelationDetail
from backend.core.conf import settings
from backend.database.redis import redis_client


class UserCacheManager:
    """用户缓存管理"""

    @staticmethod
    def get_key(user_id: int) -> str:
        """
        获取用户缓存键

        :param user_id: 用户 ID
        :return:
        """
        return f'{settings.JWT_USER_REDIS_PREFIX}:{user_id}'

    async def get(self, user_id: int) -> GetUserInfoWithRelationDetail | None:
        """
        获取用户缓存

        :param user_id: 用户 ID
        :return:
        """
        cache_user = await redis_client.get(self.get_key(user_id))
        if not cache_user:
            return None
        # TODO: 在恰当的时机，应替换为使用 model_validate_json
        # https://docs.pydantic.dev/latest/concepts/json/#partial-json-parsing
        return GetUserInfoWithRelationDetail.model_validate(from_json(cache_user, allow_partial=True))

    async def set(self, user_id: int, user: GetUserInfoWithRelationDetail) -> None:
        """
        设置用户缓存

        :param user_id: 用户 ID
        :param user: 用户信息
        :return:
        """
        await redis_client.set(self.get_key(user_id), user.model_dump_json(), ex=settings.TOKEN_EXPIRE_SECONDS)

    async def clear(self, user_ids: Sequence[int]) -> None:
        """
        清理用户缓存

        :param user_ids: 用户 ID 列表
        :return:
        """
        if user_ids:
            await redis_client.delete(*[self.get_key(user_id) for user_id in user_ids])

    async def clear_by_role_id(self, db: AsyncSession, role_ids: list[int]) -> None:
        """
        通过角色 ID 清理用户缓存

        :param db: 数据库会话
        :param role_ids: 角色 ID 列表
        :return:
        """
        stmt = select(user_role.c.user_id).where(user_role.c.role_id.in_(role_ids)).distinct()
        result = await db.execute(stmt)
        user_ids = result.scalars().all()

        await self.clear(user_ids)

    async def clear_by_menu_id(self, db: AsyncSession, menu_ids: list[int]) -> None:
        """
        通过菜单 ID 清理用户缓存

        :param db: 数据库会话
        :param menu_ids: 菜单 ID 列表
        :return:
        """
        stmt = (
            select(user_role.c.user_id)
            .join(role_menu, user_role.c.role_id == role_menu.c.role_id)
            .where(role_menu.c.menu_id.in_(menu_ids))
            .distinct()
        )
        result = await db.execute(stmt)
        user_ids = result.scalars().all()

        await self.clear(user_ids)

    async def clear_by_data_scope_id(self, db: AsyncSession, scope_ids: list[int]) -> None:
        """
        通过数据范围 ID 清理用户缓存

        :param db: 数据库会话
        :param scope_ids: 数据范围 ID 列表
        :return:
        """
        stmt = (
            select(user_role.c.user_id)
            .join(role_data_scope, user_role.c.role_id == role_data_scope.c.role_id)
            .where(role_data_scope.c.data_scope_id.in_(scope_ids))
            .distinct()
        )
        result = await db.execute(stmt)
        user_ids = result.scalars().all()

        await self.clear(user_ids)

    async def clear_by_data_rule_id(self, db: AsyncSession, rule_ids: list[int]) -> None:
        """
        通过数据规则 ID 清理用户缓存

        :param db: 数据库会话
        :param rule_ids: 数据规则 ID 列表
        :return:
        """
        stmt = (
            select(user_role.c.user_id)
            .join(role_data_scope, user_role.c.role_id == role_data_scope.c.role_id)
            .join(data_scope_rule, role_data_scope.c.data_scope_id == data_scope_rule.c.data_scope_id)
            .where(data_scope_rule.c.data_rule_id.in_(rule_ids))
            .distinct()
        )
        result = await db.execute(stmt)
        user_ids = result.scalars().all()

        await self.clear(user_ids)


user_cache_manager: UserCacheManager = UserCacheManager()
