from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import HTTPBasicCredentials
from starlette.background import BackgroundTasks

from backend.app.admin.schema.token import GetLoginToken, GetNewToken, GetSwaggerToken
from backend.app.admin.schema.user import AuthLoginParam
from backend.app.admin.service.auth_service import auth_service
from backend.common.limiter import rate_limit
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.database.db import CurrentSession, CurrentSessionTransaction

router = APIRouter()


@router.post('/login/swagger', summary='swagger 调试专用', description='用于快捷获取 token 进行 swagger 认证')
async def login_swagger(
    db: CurrentSessionTransaction, obj: Annotated[HTTPBasicCredentials, Depends()]
) -> GetSwaggerToken:
    token, user = await auth_service.swagger_login(db=db, obj=obj)
    return GetSwaggerToken(access_token=token, user=user)  # type: ignore


@router.post(
    '/login',
    summary='用户登录',
    description='json 格式登录, 仅支持在第三方api工具调试, 例如: postman',
    dependencies=[Depends(rate_limit('5/minute'))],
)
async def login(
    db: CurrentSessionTransaction,
    response: Response,
    obj: AuthLoginParam,
    background_tasks: BackgroundTasks,
) -> ResponseSchemaModel[GetLoginToken]:
    data = await auth_service.login(db=db, response=response, obj=obj, background_tasks=background_tasks)
    return response_base.success(data=data)


@router.get('/codes', summary='获取所有授权码', description='适配 vben admin v5', dependencies=[DependsJwtAuth])
async def get_codes(db: CurrentSession, request: Request) -> ResponseSchemaModel[list[str]]:
    codes = await auth_service.get_codes(db=db, request=request)
    return response_base.success(data=codes)


@router.post('/refresh', summary='刷新 token')
async def refresh_token(db: CurrentSession, request: Request, response: Response) -> ResponseSchemaModel[GetNewToken]:
    data = await auth_service.refresh_token(db=db, request=request, response=response)
    return response_base.success(data=data)


@router.post('/logout', summary='用户登出')
async def logout(request: Request, response: Response) -> ResponseModel:
    await auth_service.logout(request=request, response=response)
    return response_base.success()
