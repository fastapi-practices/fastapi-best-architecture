from collections.abc import Sequence
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.crud.crud_data_scope import data_scope_dao
from backend.app.admin.crud.crud_menu import menu_dao
from backend.app.admin.crud.crud_role import role_dao
from backend.app.admin.model import Role
from backend.app.admin.schema.role import (
    CreateRoleParam,
    DeleteRoleParam,
    UpdateRoleMenuParam,
    UpdateRoleParam,
    UpdateRoleScopeParam,
)
from backend.app.admin.utils.cache import user_cache_manager
from backend.common.exception import errors
from backend.common.pagination import paging_data
from backend.utils.build_tree import get_tree_data


class RoleService:
    """角色服务类"""

    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> Role:
        """
        获取角色详情

        :param db: 数据库会话
        :param pk: 角色 ID
        :return:
        """

        role = await role_dao.get_join(db, pk)
        if not role:
            raise errors.NotFoundError(msg='角色不存在')
        return role

    @staticmethod
    async def get_all(*, db: AsyncSession) -> Sequence[Role]:
        """
        获取所有角色

        :param db: 数据库会话
        :return:
        """

        roles = await role_dao.get_all(db)
        return roles

    @staticmethod
    async def get_list(*, db: AsyncSession, name: str | None, status: int | None) -> dict[str, Any]:
        """
        获取角色列表

        :param db: 数据库会话
        :param name: 角色名称
        :param status: 状态
        :return:
        """
        role_select = await role_dao.get_select(name=name, status=status)
        return await paging_data(db, role_select)

    @staticmethod
    async def get_menu_tree(*, db: AsyncSession, pk: int) -> list[dict[str, Any] | None]:
        """
        获取角色的菜单树形结构

        :param db: 数据库会话
        :param pk: 角色 ID
        :return:
        """

        role = await role_dao.get(db, pk)
        if not role:
            raise errors.NotFoundError(msg='角色不存在')
        menus = await role_dao.get_menus(db, pk)
        menu_tree = get_tree_data(menus) if menus else []
        return menu_tree

    @staticmethod
    async def get_scopes(*, db: AsyncSession, pk: int) -> list[int]:
        """
        获取角色数据范围列表

        :param db: 数据库会话
        :param pk:
        :return:
        """

        role = await role_dao.get_join(db, pk)
        if not role:
            raise errors.NotFoundError(msg='角色不存在')
        scope_ids = [scope.id for scope in role.scopes]
        return scope_ids

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateRoleParam) -> None:
        """
        创建角色

        :param db: 数据库会话
        :param obj: 角色创建参数
        :return:
        """

        role = await role_dao.get_by_name(db, obj.name)
        if role:
            raise errors.ConflictError(msg='角色已存在')
        await role_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateRoleParam) -> int:
        """
        更新角色

        :param db: 数据库会话
        :param pk: 角色 ID
        :param obj: 角色更新参数
        :return:
        """

        role = await role_dao.get(db, pk)
        if not role:
            raise errors.NotFoundError(msg='角色不存在')
        if role.name != obj.name and await role_dao.get_by_name(db, obj.name):
            raise errors.ConflictError(msg='角色已存在')
        count = await role_dao.update(db, pk, obj)
        await user_cache_manager.clear_by_role_id(db, [pk])
        return count

    @staticmethod
    async def update_role_menu(*, db: AsyncSession, pk: int, menu_ids: UpdateRoleMenuParam) -> int:
        """
        更新角色菜单

        :param db: 数据库会话
        :param pk: 角色 ID
        :param menu_ids: 菜单 ID 列表
        :return:
        """

        role = await role_dao.get(db, pk)
        if not role:
            raise errors.NotFoundError(msg='角色不存在')
        if menu_ids.menus:
            menus = await menu_dao.get_all_by_ids(db, list(set(menu_ids.menus)))
            if {menu.id for menu in menus} != set(menu_ids.menus):
                raise errors.NotFoundError(msg='菜单不存在')
        count = await role_dao.update_menus(db, pk, menu_ids)
        await user_cache_manager.clear_by_role_id(db, [pk])
        return count

    @staticmethod
    async def update_role_scope(*, db: AsyncSession, pk: int, scope_ids: UpdateRoleScopeParam) -> int:
        """
        更新角色数据范围

        :param db: 数据库会话
        :param pk: 角色 ID
        :param scope_ids: 权限规则 ID 列表
        :return:
        """

        role = await role_dao.get(db, pk)
        if not role:
            raise errors.NotFoundError(msg='角色不存在')
        if scope_ids.scopes:
            scopes = await data_scope_dao.get_all_by_ids(db, list(set(scope_ids.scopes)))
            if {scope.id for scope in scopes} != set(scope_ids.scopes):
                raise errors.NotFoundError(msg='数据范围不存在')
        count = await role_dao.update_scopes(db, pk, scope_ids)
        await user_cache_manager.clear_by_role_id(db, [pk])
        return count

    @staticmethod
    async def delete(*, db: AsyncSession, obj: DeleteRoleParam) -> int:
        """
        批量删除角色

        :param db: 数据库会话
        :param obj: 角色 ID 列表
        :return:
        """

        count = await role_dao.delete(db, obj.pks)
        await user_cache_manager.clear_by_role_id(db, obj.pks)
        return count


role_service: RoleService = RoleService()
