from typing import Annotated

from fastapi import APIRouter, Depends, Path

from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.database.db import CurrentSession, CurrentSessionTransaction
from backend.plugin.code_generator.schema.column import (
    CreateCodeGenColumnParam,
    GetCodeGenColumnDetail,
    UpdateCodeGenColumnParam,
)
from backend.plugin.code_generator.service.column_service import code_gen_column_service

router = APIRouter()


@router.get('/types', summary='获取代码生成模型列类型', dependencies=[DependsJwtAuth])
async def get_column_types() -> ResponseSchemaModel[list[str]]:
    column_types = await code_gen_column_service.get_types()
    return response_base.success(data=column_types)


@router.get('/{pk}', summary='获取代码生成模型列详情', dependencies=[DependsJwtAuth])
async def get_column(
    db: CurrentSession, pk: Annotated[int, Path(description='模型列 ID')]
) -> ResponseSchemaModel[GetCodeGenColumnDetail]:
    data = await code_gen_column_service.get(db=db, pk=pk)
    return response_base.success(data=data)


@router.post(
    '',
    summary='创建代码生成模型列',
    dependencies=[
        Depends(RequestPermission('codegen:column:add')),
        DependsRBAC,
    ],
)
async def create_column(db: CurrentSessionTransaction, obj: CreateCodeGenColumnParam) -> ResponseModel:
    await code_gen_column_service.create(db=db, obj=obj)
    return response_base.success()


@router.put(
    '/{pk}',
    summary='更新代码生成模型列',
    dependencies=[
        Depends(RequestPermission('codegen:column:edit')),
        DependsRBAC,
    ],
)
async def update_column(
    db: CurrentSessionTransaction, pk: Annotated[int, Path(description='模型列 ID')], obj: UpdateCodeGenColumnParam
) -> ResponseModel:
    count = await code_gen_column_service.update(db=db, pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    '/{pk}',
    summary='删除代码生成模型列',
    dependencies=[
        Depends(RequestPermission('codegen:column:del')),
        DependsRBAC,
    ],
)
async def delete_column(
    db: CurrentSessionTransaction, pk: Annotated[int, Path(description='模型列 ID')]
) -> ResponseModel:
    count = await code_gen_column_service.delete(db=db, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
