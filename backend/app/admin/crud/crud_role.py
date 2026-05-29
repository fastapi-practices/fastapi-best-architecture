from collections.abc import Sequence
from typing import Any

from sqlalchemy import Select, and_, delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus, JoinConfig

from backend.app.admin.model import DataScope, Menu, Role, role_data_scope, role_menu
from backend.app.admin.schema.role import (
    CreateRoleMenuParam,
    CreateRoleParam,
    CreateRoleScopeParam,
    UpdateRoleMenuParam,
    UpdateRoleParam,
    UpdateRoleScopeParam,
)
from backend.utils.serializers import select_join_serialize
from backend.utils.timezone import timezone


class CRUDRole(CRUDPlus[Role]):
    """角色数据库操作类"""

    async def get(self, db: AsyncSession, role_id: int) -> Role | None:
        """
        获取角色详情

        :param db: 数据库会话
        :param role_id: 角色 ID
        :return:
        """
        return await self.select_model(db, role_id, deleted=0)

    @staticmethod
    async def get_menus(db: AsyncSession, role_id: int) -> Sequence[Menu] | None:
        """
        获取角色菜单

        :param db: 数据库会话
        :param role_id: 角色 ID
        :return:
        """
        menu_stmt = (
            select(Menu)
            .join(role_menu, Menu.id == role_menu.c.menu_id)
            .where(role_menu.c.role_id == role_id, Menu.deleted == 0)
        )
        result = await db.execute(menu_stmt)
        return result.scalars().all()

    async def get_join(self, db: AsyncSession, role_id: int) -> Any:
        """
        获取角色及关联数据

        :param db: 数据库会话
        :param role_id: 角色 ID
        :return:
        """
        result = await self.select_models(
            db,
            id=role_id,
            deleted=0,
            join_conditions=[
                JoinConfig(model=role_menu, join_on=role_menu.c.role_id == self.model.id),
                JoinConfig(
                    model=Menu,
                    join_on=and_(Menu.id == role_menu.c.menu_id, Menu.deleted == 0),
                    fill_result=True,
                ),
                JoinConfig(model=role_data_scope, join_on=role_data_scope.c.role_id == self.model.id),
                JoinConfig(
                    model=DataScope,
                    join_on=and_(DataScope.id == role_data_scope.c.data_scope_id, DataScope.deleted == 0),
                    fill_result=True,
                ),
            ],
        )

        return select_join_serialize(result, relationships=['Role-m2m-Menu', 'Role-m2m-DataScope:scopes'])

    async def get_all(self, db: AsyncSession) -> Sequence[Role]:
        """
        获取所有角色

        :param db: 数据库会话
        :return:
        """
        return await self.select_models(db, deleted=0)

    async def get_all_by_ids(self, db: AsyncSession, role_ids: list[int]) -> Sequence[Role]:
        """
        通过 ID 列表批量获取角色

        :param db: 数据库会话
        :param role_ids: 角色 ID 列表
        :return:
        """
        return await self.select_models(db, id__in=role_ids, deleted=0)

    async def get_select(self, name: str | None, status: int | None) -> Select:
        """
        获取角色列表查询表达式

        :param name: 角色名称
        :param status: 角色状态
        :return:
        """

        filters = {'deleted': 0}

        if name is not None:
            filters['name__like'] = f'%{name}%'
        if status is not None:
            filters['status'] = status

        return await self.select_order('id', **filters)

    async def get_by_name(self, db: AsyncSession, name: str) -> Role | None:
        """
        通过名称获取角色

        :param db: 数据库会话
        :param name: 角色名称
        :return:
        """
        return await self.select_model_by_column(db, name=name, deleted=0)

    async def create(self, db: AsyncSession, obj: CreateRoleParam) -> None:
        """
        创建角色

        :param db: 数据库会话
        :param obj: 创建角色参数
        :return:
        """
        await self.create_model(db, obj)

    async def update(self, db: AsyncSession, role_id: int, obj: UpdateRoleParam) -> int:
        """
        更新角色

        :param db: 数据库会话
        :param role_id: 角色 ID
        :param obj: 更新角色参数
        :return:
        """
        return await self.update_model_by_column(db, obj, id=role_id, deleted=0)

    @staticmethod
    async def update_menus(db: AsyncSession, role_id: int, menu_ids: UpdateRoleMenuParam) -> int:
        """
        更新角色菜单

        :param db: 数据库会话
        :param role_id: 角色 ID
        :param menu_ids: 菜单 ID 列表
        :return:
        """
        role_menu_stmt = delete(role_menu).where(role_menu.c.role_id == role_id)
        await db.execute(role_menu_stmt)

        if menu_ids.menus:
            role_menu_data = [
                CreateRoleMenuParam(role_id=role_id, menu_id=menu_id).model_dump() for menu_id in menu_ids.menus
            ]
            role_menu_stmt = insert(role_menu)
            await db.execute(role_menu_stmt, role_menu_data)

        return len(menu_ids.menus)

    @staticmethod
    async def update_scopes(db: AsyncSession, role_id: int, scope_ids: UpdateRoleScopeParam) -> int:
        """
        更新角色数据范围

        :param db: 数据库会话
        :param role_id: 角色 ID
        :param scope_ids: 权限范围 ID 列表
        :return:
        """
        role_scope_stmt = delete(role_data_scope).where(role_data_scope.c.role_id == role_id)
        await db.execute(role_scope_stmt)

        if scope_ids.scopes:
            role_scope_data = [
                CreateRoleScopeParam(role_id=role_id, data_scope_id=scope_id).model_dump()
                for scope_id in scope_ids.scopes
            ]
            role_scope_stmt = insert(role_data_scope)
            await db.execute(role_scope_stmt, role_scope_data)

        return len(scope_ids.scopes)

    async def delete(self, db: AsyncSession, role_ids: list[int]) -> int:
        """
        批量删除角色

        :param db: 数据库会话
        :param role_ids: 角色 ID 列表
        :return:
        """
        return await self.delete_model_by_column(
            db,
            allow_multiple=True,
            logical_deletion=True,
            deleted_flag_column='deleted',
            deleted_flag_value=self.model.id,
            deleted_at_column='deleted_time',
            deleted_at_factory=timezone.now(),
            id__in=role_ids,
            deleted=0,
        )


role_dao: CRUDRole = CRUDRole(Role)
