from fastapi import APIRouter

from backend.app.admin.api.router import v1 as admin_v1

router = APIRouter()

router.include_router(admin_v1)
