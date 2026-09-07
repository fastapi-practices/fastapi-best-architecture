from fastapi import APIRouter

from backend.core.conf import settings
from backend.plugin.code_generator.api.v1.business import router as business_router
from backend.plugin.code_generator.api.v1.column import router as column_router
from backend.plugin.code_generator.api.v1.code_gen import router as code_gen_router

v1 = APIRouter(prefix=f'{settings.FASTAPI_API_V1_PATH}/code-generation', tags=['代码生成'])

v1.include_router(business_router, prefix='/businesses')
v1.include_router(column_router, prefix='/columns')
v1.include_router(code_gen_router, prefix='/generations')
