import json

from collections.abc import Sequence
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool

from backend.app.task.celery import celery_app
from backend.app.task.crud.crud_scheduler import task_scheduler_dao
from backend.app.task.enums import TaskSchedulerType
from backend.app.task.model import TaskScheduler
from backend.app.task.schema.scheduler import CreateTaskSchedulerParam, UpdateTaskSchedulerParam
from backend.app.task.utils.tzcrontab import crontab_verify
from backend.common.enums import StatusType
from backend.common.exception import errors
from backend.common.pagination import paging_data


class TaskSchedulerService:
    """任务调度服务类"""

    @staticmethod
    async def get(*, db: AsyncSession, pk: int) -> TaskScheduler | None:
        """
        获取任务调度详情

        :param db: 数据库会话
        :param pk: 任务调度 ID
        :return:
        """

        task_scheduler = await task_scheduler_dao.get(db, pk)
        if not task_scheduler:
            raise errors.NotFoundError(msg='任务调度不存在')
        return task_scheduler

    @staticmethod
    async def get_all(*, db: AsyncSession) -> Sequence[TaskScheduler]:
        """
        获取所有任务调度

        :param db: 数据库会话
        :return:
        """

        task_schedulers = await task_scheduler_dao.get_all(db)
        return task_schedulers

    @staticmethod
    async def get_list(*, db: AsyncSession, name: str | None, type: int | None) -> dict[str, Any]:
        """
        获取任务调度列表

        :param db: 数据库会话
        :param name: 任务调度名称
        :param type: 任务调度类型
        :return:
        """
        task_scheduler_select = await task_scheduler_dao.get_select(name=name, type=type)
        return await paging_data(db, task_scheduler_select)

    @staticmethod
    async def create(*, db: AsyncSession, obj: CreateTaskSchedulerParam) -> None:
        """
        创建任务调度

        :param db: 数据库会话
        :param obj: 任务调度创建参数
        :return:
        """

        task_scheduler = await task_scheduler_dao.get_by_name(db, obj.name)
        if task_scheduler:
            raise errors.ConflictError(msg='任务调度已存在')
        if obj.type == TaskSchedulerType.CRONTAB:
            crontab_verify(obj.crontab)
        await task_scheduler_dao.create(db, obj)

    @staticmethod
    async def update(*, db: AsyncSession, pk: int, obj: UpdateTaskSchedulerParam) -> int:
        """
        更新任务调度

        :param db: 数据库会话
        :param pk: 任务调度 ID
        :param obj: 任务调度更新参数
        :return:
        """

        task_scheduler = await task_scheduler_dao.get(db, pk)
        if not task_scheduler:
            raise errors.NotFoundError(msg='任务调度不存在')
        if task_scheduler.name != obj.name and await task_scheduler_dao.get_by_name(db, obj.name):
            raise errors.ConflictError(msg='任务调度已存在')
        if obj.type == TaskSchedulerType.CRONTAB:
            crontab_verify(obj.crontab)
        count = await task_scheduler_dao.update(db, pk, obj)
        return count

    @staticmethod
    async def update_status(*, db: AsyncSession, pk: int) -> int:
        """
        更新任务调度状态

        :param db: 数据库会话
        :param pk: 任务调度 ID
        :return:
        """

        task_scheduler = await task_scheduler_dao.get(db, pk)
        if not task_scheduler:
            raise errors.NotFoundError(msg='任务调度不存在')
        next_status = StatusType.disable if task_scheduler.status == StatusType.enable else StatusType.enable
        count = await task_scheduler_dao.set_status(db, pk, status=next_status)
        return count

    @staticmethod
    async def delete(*, db: AsyncSession, pk: int) -> int:
        """
        删除任务调度

        :param db: 数据库会话
        :param pk: 用户 ID
        :return:
        """

        task_scheduler = await task_scheduler_dao.get(db, pk)
        if not task_scheduler:
            raise errors.NotFoundError(msg='任务调度不存在')
        count = await task_scheduler_dao.delete(db, pk)
        return count

    @staticmethod
    async def execute(*, db: AsyncSession, pk: int) -> None:
        """
        执行任务

        :param db: 数据库会话
        :param pk: 任务调度 ID
        :return:
        """

        workers = await run_in_threadpool(celery_app.control.ping, timeout=0.5)
        if not workers:
            raise errors.ServerError(msg='Celery Worker 暂不可用，请稍后重试')
        task_scheduler = await task_scheduler_dao.get(db, pk)
        if not task_scheduler:
            raise errors.NotFoundError(msg='任务调度不存在')
        try:
            args = json.loads(task_scheduler.args) if task_scheduler.args else None
            kwargs = json.loads(task_scheduler.kwargs) if task_scheduler.kwargs else None
        except (TypeError, json.JSONDecodeError):
            raise errors.RequestError(msg='执行失败，任务参数非法')
        else:
            celery_app.send_task(name=task_scheduler.task, args=args, kwargs=kwargs)


task_scheduler_service: TaskSchedulerService = TaskSchedulerService()
