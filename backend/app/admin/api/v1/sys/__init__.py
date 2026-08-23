from fastapi import APIRouter

from backend.app.admin.api.v1.sys.file import router as file_router
from backend.app.admin.api.v1.sys.plugin import router as plugin_router
from backend.app.admin.api.v1.sys.user import router as user_router

router = APIRouter(prefix='/sys')

router.include_router(user_router, prefix='/users', tags=['系统用户'])
router.include_router(file_router, prefix='/files', tags=['系统文件'])
router.include_router(plugin_router, prefix='/plugins', tags=['系统插件'])
