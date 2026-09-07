from typing import Annotated

from fastapi import APIRouter, Depends, Path
from starlette.concurrency import run_in_threadpool

from backend.app.task import celery_app
from backend.app.task.schema.control import GetTaskRegisteredDetail
from backend.common.exception import errors
from backend.common.response.response_schema import ResponseModel, ResponseSchemaModel, response_base
from backend.common.security.jwt import DependsJwtAuth
from backend.common.security.permission import RequestPermission
from backend.common.security.rbac import DependsRBAC

router = APIRouter()


@router.get('/registered', summary='获取已注册的任务', dependencies=[DependsJwtAuth])
async def get_task_registered() -> ResponseSchemaModel[list[GetTaskRegisteredDetail]]:
    inspector = celery_app.control.inspect(timeout=0.5)
    registered = await run_in_threadpool(inspector.registered)
    if not registered:
        raise errors.ServerError(msg='Celery Worker 暂不可用，请稍后重试')
    task_registered = []
    celery_app_tasks = celery_app.tasks
    for tasks in registered.values():
        for task in tasks:
            task_ins = celery_app_tasks.get(task)
            if task_ins:
                task_registered.append(GetTaskRegisteredDetail(name=task_ins.__doc__ or task, task=task))
            else:
                task_registered.append(GetTaskRegisteredDetail(name=task, task=task))
    return response_base.success(data=task_registered)


@router.delete(
    '/{task_id}/cancel',
    summary='撤销任务',
    dependencies=[
        Depends(RequestPermission('sys:task:revoke')),
        DependsRBAC,
    ],
)
async def revoke_task(task_id: Annotated[str, Path(description='任务 UUID')]) -> ResponseModel:
    workers = await run_in_threadpool(celery_app.control.ping, timeout=0.5)
    if not workers:
        raise errors.ServerError(msg='Celery Worker 暂不可用，请稍后重试')
    celery_app.control.revoke(task_id)
    return response_base.success()
