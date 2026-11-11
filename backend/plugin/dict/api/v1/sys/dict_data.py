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
from backend.plugin.dict.schema.dict_data import (
    CreateDictDataParam,
    DeleteDictDataParam,
    DictDataQueryParam,
    GetDictDataDetail,
    UpdateDictDataParam,
)
from backend.plugin.dict.service.dict_data_service import dict_data_service

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
async def get_all_dict_datas(db: CurrentSession) -> ResponseSchemaModel[list[GetDictDataDetail]]:
    data = await dict_data_service.get_all(db=db)
    return response_base.success(data=data)


@router.get(
    '/{pk}',
    summary='获取字典数据详情',
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
async def get_dict_data(
    db: CurrentSession,
    pk: Annotated[int, Path(description='字典数据 ID')],
) -> ResponseSchemaModel[GetDictDataDetail]:
    data = await dict_data_service.get(db=db, pk=pk)
    return response_base.success(data=data)


@router.get(
    '/type-codes/{code}',
    summary='获取字典数据列表',
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
async def get_dict_data_by_type_code(
    db: CurrentSession,
    code: Annotated[str, Path(description='字典类型编码')],
) -> ResponseSchemaModel[list[GetDictDataDetail]]:
    data = await dict_data_service.get_by_type_code(db=db, code=code)
    return response_base.success(data=data)


@router.get(
    '',
    summary='分页获取所有字典数据',
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
async def get_dict_datas_paginated(
    db: CurrentSession,
    query: Annotated[DictDataQueryParam, Query()],
) -> ResponseSchemaModel[PageData[GetDictDataDetail]]:
    page_data = await dict_data_service.get_list(
        db=db,
        type_code=query.type_code,
        label=query.label,
        value=query.value,
        status=query.status,
        type_id=query.type_id,
    )
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='创建字典数据',
    dependencies=[
        Depends(RequestPermission('dict:data:add')),
        DependsRBAC,
        Depends(cache_evict(eviction_group='dict'), scope='function'),
    ],
)
async def create_dict_data(db: CurrentSessionTransaction, obj: CreateDictDataParam) -> ResponseModel:
    await dict_data_service.create(db=db, obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新字典数据',
    dependencies=[
        Depends(RequestPermission('dict:data:edit')),
        DependsRBAC,
        Depends(cache_evict(eviction_group='dict'), scope='function'),
    ],
)
async def update_dict_data(
    db: CurrentSessionTransaction,
    pk: Annotated[int, Path(description='字典数据 ID')],
    obj: UpdateDictDataParam,
) -> ResponseModel:
    count = await dict_data_service.update(db=db, pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='批量删除字典数据',
    dependencies=[
        Depends(RequestPermission('dict:data:del')),
        DependsRBAC,
        Depends(cache_evict(eviction_group='dict'), scope='function'),
    ],
)
async def delete_dict_datas(db: CurrentSessionTransaction, obj: DeleteDictDataParam) -> ResponseModel:
    count = await dict_data_service.delete(db=db, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()
