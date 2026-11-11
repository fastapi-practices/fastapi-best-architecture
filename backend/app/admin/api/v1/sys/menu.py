from typing import Annotated, Any

from fastapi import APIRouter, Depends, Path, Query, Request

from backend.app.admin.schema.menu import CreateMenuParam, GetMenuDetail, GetMenuTree, MenuQueryParam, UpdateMenuParam
from backend.app.admin.service.menu_service import menu_service
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession, CurrentSessionTransaction

router = APIRouter()


@router.get('/sidebar', summary='获取用户菜单侧边栏', description='已适配 vben admin v5', dependencies=[DependsJwtAuth])
async def get_user_sidebar(db: CurrentSession, request: Request) -> ResponseSchemaModel[list[dict[str, Any] | None]]:
    menu = await menu_service.get_sidebar(db=db, request=request)
    return response_base.success(data=menu)


@router.get('/{pk}', summary='获取菜单详情', dependencies=[DependsJwtAuth])
async def get_menu(
    db: CurrentSession, pk: Annotated[int, Path(description='菜单 ID')]
) -> ResponseSchemaModel[GetMenuDetail]:
    data = await menu_service.get(db=db, pk=pk)
    return response_base.success(data=data)


@router.get('', summary='获取菜单树', dependencies=[DependsJwtAuth])
async def get_menu_tree(
    db: CurrentSession,
    query: Annotated[MenuQueryParam, Query()],
) -> ResponseSchemaModel[list[GetMenuTree]]:
    menu = await menu_service.get_tree(db=db, title=query.title, status=query.status)
    return response_base.success(data=menu)


@router.post(
    '',
    summary='创建菜单',
    dependencies=[
        Depends(RequestPermission('sys:menu:add')),
        DependsRBAC,
    ],
)
async def create_menu(db: CurrentSessionTransaction, obj: CreateMenuParam) -> ResponseModel:
    await menu_service.create(db=db, obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新菜单',
    dependencies=[
        Depends(RequestPermission('sys:menu:edit')),
        DependsRBAC,
    ],
)
async def update_menu(
    db: CurrentSessionTransaction, pk: Annotated[int, Path(description='菜单 ID')], obj: UpdateMenuParam
) -> ResponseModel:
    count = await menu_service.update(db=db, pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/{pk}',
    summary='删除菜单',
    dependencies=[
        Depends(RequestPermission('sys:menu:del')),
        DependsRBAC,
    ],
)
async def delete_menu(db: CurrentSessionTransaction, pk: Annotated[int, Path(description='菜单 ID')]) -> ResponseModel:
    count = await menu_service.delete(db=db, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
