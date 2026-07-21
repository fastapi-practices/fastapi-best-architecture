from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import StreamingResponse

from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC
from backend.core.conf import settings
from backend.database.db import CurrentSession, CurrentSessionTransaction
from backend.plugin.code_generator.schema.gen import ImportParam
from backend.plugin.code_generator.service.gen_service import gen_service

router = APIRouter()


@router.get('/tables', summary='获取数据库表')
async def get_all_tables(
    db: CurrentSession,
    table_schema: Annotated[str, Query(description='数据库名')] = 'fba',
) -> ResponseSchemaModel[list[dict[str, str | None]]]:
    data = await gen_service.get_tables(db=db, table_schema=table_schema)
    return response_base.success(data=data)


@router.post(
    '/imports',
    summary='导入代码生成业务和模型列（仅开发环境）',
    dependencies=[
        Depends(RequestPermission('codegen:table:import')),
        DependsRBAC,
    ],
)
async def import_table(db: CurrentSessionTransaction, obj: ImportParam) -> ResponseModel:
    await gen_service.import_business_and_model(db=db, obj=obj)
    return response_base.success()


@router.get('/{pk}/preview', summary='代码生成预览', dependencies=[DependsJwtAuth])
async def preview_code(
    db: CurrentSession, pk: Annotated[int, Path(description='业务 ID')]
) -> ResponseSchemaModel[dict[str, bytes]]:
    data = await gen_service.preview(db=db, pk=pk)
    return response_base.success(data=data)


@router.get('/{pk}/paths', summary='获取代码生成路径', dependencies=[DependsJwtAuth])
async def get_generate_paths(
    db: CurrentSession, pk: Annotated[int, Path(description='业务 ID')]
) -> ResponseSchemaModel[list[str]]:
    data = await gen_service.get_generate_path(db=db, pk=pk)
    return response_base.success(data=data)


@router.post(
    '/{pk}',
    summary='代码生成',
    description='文件磁盘写入，请谨慎操作（仅开发环境）',
    dependencies=[
        Depends(RequestPermission('codegen:local:write')),
        DependsRBAC,
    ],
)
async def generate_code(db: CurrentSession, pk: Annotated[int, Path(description='业务 ID')]) -> ResponseModel:
    await gen_service.generate(db=db, pk=pk)
    return response_base.success()


@router.get('/{pk}', summary='下载代码', dependencies=[DependsJwtAuth])
async def download_code(db: CurrentSession, pk: Annotated[int, Path(description='业务 ID')]):  # ruff:ignore[missing-return-type-undocumented-public-function]
    bio = await gen_service.download(db=db, pk=pk)
    return StreamingResponse(
        bio,
        media_type='application/x-zip-compressed',
        headers={'Content-Disposition': f'attachment; filename={settings.CODE_GENERATOR_DOWNLOAD_ZIP_FILENAME}.zip'},
    )
