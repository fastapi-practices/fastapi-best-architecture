from typing import Annotated

from fastapi import APIRouter, Depends, Query

from backend.app.admin.schema.opera_log import DeleteOperaLogParam, GetOperaLogDetail, OperaLogQueryParam
from backend.app.admin.service.opera_log_service import opera_log_service
from backend.common.pagination import DependsPagination, PageData
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession, CurrentSessionTransaction

router = APIRouter()


@router.get(
    '',
    summary='分页获取操作日志',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_opera_logs_paginated(
    db: CurrentSession,
    query: Annotated[OperaLogQueryParam, Query()],
) -> ResponseSchemaModel[PageData[GetOperaLogDetail]]:
    page_data = await opera_log_service.get_list(db=db, username=query.username, status=query.status, ip=query.ip)

    return response_base.success(data=page_data)


@router.delete(
    '',
    summary='批量删除操作日志',
    dependencies=[
        Depends(RequestPermission('log:opera:del')),
        DependsRBAC,
    ],
)
async def delete_opera_logs(db: CurrentSessionTransaction, obj: DeleteOperaLogParam) -> ResponseModel:
    count = await opera_log_service.delete(db=db, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/all',
    summary='清空操作日志',
    dependencies=[
        Depends(RequestPermission('log:opera:clear')),
        DependsRBAC,
    ],
)
async def delete_all_opera_logs(db: CurrentSessionTransaction) -> ResponseModel:
    await opera_log_service.delete_all(db=db)
    return response_base.success()
