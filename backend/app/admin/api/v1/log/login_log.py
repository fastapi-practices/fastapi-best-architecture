from typing import Annotated

from fastapi import APIRouter, Depends, Query

from backend.app.admin.schema.login_log import DeleteLoginLogParam, GetLoginLogDetail, LoginLogQueryParam
from backend.app.admin.service.login_log_service import login_log_service
from backend.common.pagination import DependsPagination, PageData
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession, CurrentSessionTransaction

router = APIRouter()


@router.get(
    '',
    summary='分页获取登录日志',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_login_logs_paginated(
    db: CurrentSession,
    query: Annotated[LoginLogQueryParam, Query()],
) -> ResponseSchemaModel[PageData[GetLoginLogDetail]]:
    page_data = await login_log_service.get_list(db=db, username=query.username, status=query.status, ip=query.ip)

    return response_base.success(data=page_data)


@router.delete(
    '',
    summary='批量删除登录日志',
    dependencies=[
        Depends(RequestPermission('log:login:del')),
        DependsRBAC,
    ],
)
async def delete_login_logs(db: CurrentSessionTransaction, obj: DeleteLoginLogParam) -> ResponseModel:
    count = await login_log_service.delete(db=db, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/all',
    summary='清空登录日志',
    dependencies=[
        Depends(RequestPermission('log:login:clear')),
        DependsRBAC,
    ],
)
async def delete_all_login_logs(db: CurrentSessionTransaction) -> ResponseModel:
    await login_log_service.delete_all(db=db)
    return response_base.success()
