from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from redis_fastapi import cache, cache_evict

from backend.common.cache import http_cache_key
from backend.common.pagination import DependsPagination, PageData
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.core.conf import settings
from backend.database.db import CurrentSession, CurrentSessionTransaction
from backend.plugin.dict.schema.dict_type import (
    CreateDictTypeParam,
    DeleteDictTypeParam,
    DictTypeQueryParam,
    GetDictTypeDetail,
    UpdateDictTypeParam,
)
from backend.plugin.dict.service.dict_type_service import dict_type_service

router = APIRouter()


@router.get(
    '/all',
    summary='获取所有字典数据',
    dependencies=[
        DependsJwtAuth,
        Depends(
            cache(
                ttl=settings.HTTP_CACHE_TTL,
                eviction_group='dict',
                key_builder=http_cache_key,
                no_store=True,
            )
        ),
    ],
)
async def get_all_dict_types(db: CurrentSession) -> ResponseSchemaModel[list[GetDictTypeDetail]]:
    data = await dict_type_service.get_all(db=db)
    return response_base.success(data=data)


@router.get(
    '/{pk}',
    summary='获取字典类型详情',
    dependencies=[
        DependsJwtAuth,
        Depends(
            cache(
                ttl=settings.HTTP_CACHE_TTL,
                eviction_group='dict',
                key_builder=http_cache_key,
                no_store=True,
            )
        ),
    ],
)
async def get_dict_type(
    db: CurrentSession,
    pk: Annotated[int, Path(description='字典类型 ID')],
) -> ResponseSchemaModel[GetDictTypeDetail]:
    data = await dict_type_service.get(db=db, pk=pk)
    return response_base.success(data=data)


@router.get(
    '',
    summary='分页获取所有字典类型',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
        Depends(
            cache(
                ttl=settings.HTTP_CACHE_TTL,
                eviction_group='dict',
                key_builder=http_cache_key,
                no_store=True,
            )
        ),
    ],
)
async def get_dict_types_paginated(
    db: CurrentSession,
    query: Annotated[DictTypeQueryParam, Query()],
) -> ResponseSchemaModel[PageData[GetDictTypeDetail]]:
    page_data = await dict_type_service.get_list(db=db, name=query.name, code=query.code)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='创建字典类型',
    dependencies=[
        Depends(RequestPermission('dict:type:add')),
        DependsRBAC,
        Depends(cache_evict(eviction_group='dict'), scope='function'),
    ],
)
async def create_dict_type(db: CurrentSessionTransaction, obj: CreateDictTypeParam) -> ResponseModel:
    await dict_type_service.create(db=db, obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新字典类型',
    dependencies=[
        Depends(RequestPermission('dict:type:edit')),
        DependsRBAC,
        Depends(cache_evict(eviction_group='dict'), scope='function'),
    ],
)
async def update_dict_type(
    db: CurrentSessionTransaction,
    pk: Annotated[int, Path(description='字典类型 ID')],
    obj: UpdateDictTypeParam,
) -> ResponseModel:
    count = await dict_type_service.update(db=db, pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='批量删除字典类型',
    dependencies=[
        Depends(RequestPermission('dict:type:del')),
        DependsRBAC,
        Depends(cache_evict(eviction_group='dict'), scope='function'),
    ],
)
async def delete_dict_types(db: CurrentSessionTransaction, obj: DeleteDictTypeParam) -> ResponseModel:
    count = await dict_type_service.delete(db=db, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()
