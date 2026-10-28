from typing import Any

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.crud.crud_menu import menu_dao
from backend.app.admin.model import Menu
from backend.app.admin.schema.menu import CreateMenuParam, UpdateMenuParam
from backend.app.admin.utils.cache import user_cache_manager
from backend.common.enums import StatusType
from backend.common.exception import errors
from backend.common.i18n import t
from backend.utils.build_tree import get_tree_data, get_vben5_tree_data


class MenuService:
    """菜单服务类"""

    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> Menu:
        """
        获取菜单详情

        :param db: 数据库会话
        :param pk: 菜单 ID
        :return:
        """

        menu = await menu_dao.get(db, menu_id=pk)
        if not menu:
            raise errors.NotFoundError(msg=t('error.menu.not_found'))
        return menu

    @staticmethod
    async def get_tree(*, db: AsyncSession, title: str | None, status: int | None) -> list[dict[str, Any]]:
        """
        获取菜单树形结构

        :param db: 数据库会话
        :param title: 菜单标题
        :param status: 状态
        :return:
        """

        menu_data = await menu_dao.get_all(db, title=title, status=status)
        menu_tree = get_tree_data(menu_data)
        return menu_tree

    @staticmethod
    async def get_sidebar(*, db: AsyncSession, request: Request) -> list[dict[str, Any] | None]:
        """
        获取用户的菜单侧边栏

        :param db: 数据库会话
        :param request: FastAPI 请求对象
        :return:
        """
        menu_data = None
        if request.user.is_superuser:
            menu_data = await menu_dao.get_sidebar(db, None)
        else:
            roles = [role for role in request.user.roles if role.status == StatusType.enable]
            menu_ids = set()
            if roles:
                for role in roles:
                    menu_ids.update(menu.id for menu in role.menus)
                menu_data = await menu_dao.get_sidebar(db, list(menu_ids))

        if menu_data:
            return get_vben5_tree_data(menu_data)

        return []

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateMenuParam) -> None:
        """
        创建菜单

        :param db: 数据库会话
        :param obj: 菜单创建参数
        :return:
        """

        title = await menu_dao.get_by_title(db, obj.title)
        if title:
            raise errors.ConflictError(msg=t('error.menu.title_exists'))
        if obj.parent_id:
            parent_menu = await menu_dao.get(db, obj.parent_id)
            if not parent_menu:
                raise errors.NotFoundError(msg=t('error.menu.parent_not_found'))
        await menu_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateMenuParam) -> int:
        """
        更新菜单

        :param db: 数据库会话
        :param pk: 菜单 ID
        :param obj: 菜单更新参数
        :return:
        """

        menu = await menu_dao.get(db, pk)
        if not menu:
            raise errors.NotFoundError(msg=t('error.menu.not_found'))
        if menu.title != obj.title and await menu_dao.get_by_title(db, obj.title):
            raise errors.ConflictError(msg=t('error.menu.title_exists'))
        if obj.parent_id:
            parent_menu = await menu_dao.get(db, obj.parent_id)
            if not parent_menu:
                raise errors.NotFoundError(msg=t('error.menu.parent_not_found'))
        if obj.parent_id == menu.id:
            raise errors.ForbiddenError(msg=t('error.dept.parent_self'))
        count = await menu_dao.update(db, pk, obj)
        await user_cache_manager.clear_by_menu_id(db, [pk])
        return count

    @staticmethod
    async def delete(*, db: AsyncSession, pk: int) -> int:
        """
        删除菜单

        :param db: 数据库会话
        :param pk: 菜单 ID
        :return:
        """

        children = await menu_dao.get_children(db, pk)
        if children:
            raise errors.ConflictError(msg=t('error.menu.has_children'))
        count = await menu_dao.delete(db, pk)
        if count:
            await user_cache_manager.clear_by_menu_id(db, [pk])
        return count


menu_service: MenuService = MenuService()
