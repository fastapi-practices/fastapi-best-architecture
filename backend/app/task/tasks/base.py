from typing import Any

from celery import Task
from celery_aio_pool import AsyncIOPool
from sqlalchemy.exc import SQLAlchemyError

from backend.common.socketio.actions import task_notification
from backend.core.conf import settings


class TaskBase(Task):
    """Celery 任务基类"""

    autoretry_for = (SQLAlchemyError,)
    max_retries = settings.CELERY_TASK_MAX_RETRIES

    async def before_start(self, task_id: str, args, kwargs) -> None:  # ruff:ignore[missing-type-function-argument]
        """
        任务开始前执行钩子

        :param task_id: 任务 ID
        :return:
        """
        await task_notification(msg=f'任务 {task_id} 开始执行')

    async def on_success(self, retval: Any, task_id: str, args, kwargs) -> None:  # ruff:ignore[missing-type-function-argument]
        """
        任务成功后执行钩子

        :param retval: 任务返回值
        :param task_id: 任务 ID
        :return:
        """
        await task_notification(msg=f'任务 {task_id} 执行成功')

    def on_failure(self, exc: Exception, task_id: str, args, kwargs, einfo) -> None:  # ruff:ignore[missing-type-function-argument]
        """
        任务失败后执行钩子

        :param exc: 异常对象
        :param task_id: 任务 ID
        :param einfo: 异常信息
        :return:
        """
        # on_failure 由 Celery 在执行任务的线程中同步调用，该线程没有运行中的事件循环，
        # 必须交给 worker 绑定的 AsyncIOPool 事件循环执行
        AsyncIOPool.run_in_pool(task_notification, msg=f'任务 {task_id} 执行失败')
