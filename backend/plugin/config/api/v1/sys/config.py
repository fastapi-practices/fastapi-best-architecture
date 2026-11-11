from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path, Query
from redis_fastapi import cache, cache_evict

from backend.common.cache import http_cache_key
from backend.common.pagination import DependsPagination, PageData
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.core.conf import settings
from backend.database.db import CurrentSession, CurrentSessionTransaction
from backend.plugin.config.schema.config import (
    ConfigQueryParam,
    ConfigTypeQueryParam,
    CreateConfigParam,
    GetConfigDetail,
    UpdateConfigParam,
    UpdateConfigsParam,
)
from backend.plugin.config.service.config_service import config_service

router = APIRouter()


@router.get(
    '/all',
    summary='获取所有参数配置',
    dependencies=[
        DependsJwtAuth,
        Depends(
            cache(
                ttl=settings.HTTP_CACHE_TTL,
                eviction_group='config',
                key_builder=http_cache_key,
                no_store=True,
            )
        ),
    ],
)
async def get_all_configs(
    db: CurrentSession,
    query: Annotated[ConfigTypeQueryParam, Query()],
) -> ResponseSchemaModel[list[GetConfigDetail]]:
    configs = await config_service.get_all(db=db, type=query.type)
    return response_base.success(data=configs)


@router.get(
    '/{pk}',
    summary='获取参数配置详情',
    dependencies=[
        DependsJwtAuth,
        Depends(
            cache(
                ttl=settings.HTTP_CACHE_TTL,
                eviction_group='config',
                key_builder=http_cache_key,
                no_store=True,
            )
        ),
    ],
)
async def get_config(
    db: CurrentSession, pk: Annotated[int, Path(description='参数配置 ID')]
) -> ResponseSchemaModel[GetConfigDetail]:
    config = await config_service.get(db=db, pk=pk)
    return response_base.success(data=config)


@router.get(
    '',
    summary='分页获取所有参数配置',
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
        Depends(
            cache(
                ttl=settings.HTTP_CACHE_TTL,
                eviction_group='config',
                key_builder=http_cache_key,
                no_store=True,
            )
        ),
    ],
)
async def get_configs_paginated(
    db: CurrentSession,
    query: Annotated[ConfigQueryParam, Query()],
) -> ResponseSchemaModel[PageData[GetConfigDetail]]:
    page_data = await config_service.get_list(db=db, name=query.name, type=query.type)
    return response_base.success(data=page_data)


@router.post(
    '',
    summary='创建参数配置',
    dependencies=[
        Depends(RequestPermission('sys:config:add')),
        DependsRBAC,
        Depends(cache_evict(eviction_group='config'), scope='function'),
    ],
)
async def create_config(db: CurrentSessionTransaction, obj: CreateConfigParam) -> ResponseModel:
    await config_service.create(db=db, obj=obj)
    return response_base.success()


@router.put(
    '',
    summary='批量更新参数配置',
    dependencies=[
        Depends(RequestPermission('sys:config:edit')),
        DependsRBAC,
        Depends(cache_evict(eviction_group='config'), scope='function'),
    ],
)
async def bulk_update_config(db: CurrentSessionTransaction, objs: list[UpdateConfigsParam]) -> ResponseModel:
    count = await config_service.bulk_update(db=db, objs=objs)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put(
    '/{pk}',
    summary='更新参数配置',
    dependencies=[
        Depends(RequestPermission('sys:config:edit')),
        DependsRBAC,
        Depends(cache_evict(eviction_group='config'), scope='function'),
    ],
)
async def update_config(
    db: CurrentSessionTransaction, pk: Annotated[int, Path(description='参数配置 ID')], obj: UpdateConfigParam
) -> ResponseModel:
    count = await config_service.update(db=db, pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '',
    summary='批量删除参数配置',
    dependencies=[
        Depends(RequestPermission('sys:config:del')),
        DependsRBAC,
        Depends(cache_evict(eviction_group='config'), scope='function'),
    ],
)
async def delete_configs(
    db: CurrentSessionTransaction, pks: Annotated[list[int], Body(description='参数配置 ID 列表')]
) -> ResponseModel:
    count = await config_service.delete(db=db, pks=pks)
    if count > 0:
        return response_base.success()
    return response_base.fail()
