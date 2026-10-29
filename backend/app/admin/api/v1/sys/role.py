from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.app.admin.schema.menu import GetMenuTree
from backend.app.admin.schema.role import (
    CreateRoleParam,
    DeleteRoleParam,
    GetRoleDetail,
    GetRoleWithRelationDetail,
    RoleQueryParam,
    UpdateRoleMenuParam,
    UpdateRoleParam,
    UpdateRoleScopeParam,
)
from backend.app.admin.service.role_service import role_service
from backend.common.pagination import DependsPagination, PageData
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession, CurrentSessionTransaction

router = APIRouter()


@router.get('/all', summary='获取所有角色', dependencies=[DependsJwtAuth])
async def get_all_roles(db: CurrentSession) -> ResponseSchemaModel[list[GetRoleDetail]]:
    data = await role_service.get_all(db=db)
    return response_base.success(data=data)


@router.get('/{pk}/menus', summary='获取角色菜单树', dependencies=[DependsJwtAuth])
async def get_role_menu_tree(
    db: CurrentSession,
    pk: Annotated[int, Path(description='角色 ID')],
) -> ResponseSchemaModel[list[GetMenuTree] | None]:
    menu = await role_service.get_menu_tree(db=db, pk=pk)
    return response_base.success(data=menu)


@router.get('/{pk}/scopes', summary='获取角色所有数据范围', dependencies=[DependsJwtAuth])
async def get_role_scopes(
    db: CurrentSession, pk: Annotated[int, Path(description='角色 ID')]
) -> ResponseSchemaModel[list[int]]:
    rule = await role_service.get_scopes(db=db, pk=pk)
    return response_base.success(data=rule)


@router.get('/{pk}', summary='获取角色详情', dependencies=[DependsJwtAuth])
async def get_role(
    db: CurrentSession, pk: Annotated[int, Path(description='角色 ID')]
) -> ResponseSchemaModel[GetRoleWithRelationDetail]:
    data = await role_service.get(db=db, pk=pk)
    return response_base.success(data=data)


@router.get(
    '',
    summary='分页获取所有角色',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_roles_paginated(
    db: CurrentSession,
    query: Annotated[RoleQueryParam, Query()],
) -> ResponseSchemaModel[PageData[GetRoleDetail]]:
    page_data = await role_service.get_list(db=db, name=query.name, status=query.status)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='创建角色',
    dependencies=[
        Depends(RequestPermission('sys:role:add')),
        DependsRBAC,
    ],
)
async def create_role(db: CurrentSessionTransaction, obj: CreateRoleParam) -> ResponseModel:
    await role_service.create(db=db, obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新角色',
    dependencies=[
        Depends(RequestPermission('sys:role:edit')),
        DependsRBAC,
    ],
)
async def update_role(
    db: CurrentSessionTransaction, pk: Annotated[int, Path(description='角色 ID')], obj: UpdateRoleParam
) -> ResponseModel:
    count = await role_service.update(db=db, pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put(
    '/{pk}/menus',
    summary='更新角色菜单',
    dependencies=[
        Depends(RequestPermission('sys:role:menu:edit')),
        DependsRBAC,
    ],
)
async def update_role_menus(
    db: CurrentSessionTransaction,
    pk: Annotated[int, Path(description='角色 ID')],
    obj: UpdateRoleMenuParam,
) -> ResponseModel:
    count = await role_service.update_role_menu(db=db, pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put(
    '/{pk}/scopes',
    summary='更新角色数据范围',
    dependencies=[
        Depends(RequestPermission('sys:role:scope:edit')),
        DependsRBAC,
    ],
)
async def update_role_scopes(
    db: CurrentSessionTransaction,
    pk: Annotated[int, Path(description='角色 ID')],
    obj: UpdateRoleScopeParam,
) -> ResponseModel:
    count = await role_service.update_role_scope(db=db, pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='批量删除角色',
    dependencies=[
        Depends(RequestPermission('sys:role:del')),
        DependsRBAC,
    ],
)
async def delete_roles(db: CurrentSessionTransaction, obj: DeleteRoleParam) -> ResponseModel:
    count = await role_service.delete(db=db, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()
