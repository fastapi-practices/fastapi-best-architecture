from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from backend.common.pagination import DependsPagination, PageData
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession, CurrentSessionTransaction
from backend.plugin.notice.schema.notice import (
    CreateNoticeParam,
    DeleteNoticeParam,
    GetNoticeDetail,
    NoticeQueryParam,
    UpdateNoticeParam,
)
from backend.plugin.notice.service.notice_service import notice_service

router = APIRouter()


@router.get('/{pk}', summary='获取通知公告详情', dependencies=[DependsJwtAuth])
async def get_notice(
    db: CurrentSession, pk: Annotated[int, Path(description='通知公告 ID')]
) -> ResponseSchemaModel[GetNoticeDetail]:
    notice = await notice_service.get(db=db, pk=pk)
    return response_base.success(data=notice)


@router.get(
    '',
    summary='分页获取所有通知公告',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_notices_paginated(
    db: CurrentSession,
    query: Annotated[NoticeQueryParam, Query()],
) -> ResponseSchemaModel[PageData[GetNoticeDetail]]:
    page_data = await notice_service.get_list(db=db, title=query.title, type=query.type, status=query.status)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='创建通知公告',
    dependencies=[
        Depends(RequestPermission('sys:notice:add')),
        DependsRBAC,
    ],
)
async def create_notice(db: CurrentSessionTransaction, obj: CreateNoticeParam) -> ResponseModel:
    await notice_service.create(db=db, obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新通知公告',
    dependencies=[
        Depends(RequestPermission('sys:notice:edit')),
        DependsRBAC,
    ],
)
async def update_notice(
    db: CurrentSessionTransaction, pk: Annotated[int, Path(description='通知公告 ID')], obj: UpdateNoticeParam
) -> ResponseModel:
    count = await notice_service.update(db=db, pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='批量删除通知公告',
    dependencies=[
        Depends(RequestPermission('sys:notice:del')),
        DependsRBAC,
    ],
)
async def delete_notices(db: CurrentSessionTransaction, obj: DeleteNoticeParam) -> ResponseModel:
    count = await notice_service.delete(db=db, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()
