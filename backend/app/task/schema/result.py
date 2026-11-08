from datetime import datetime
from typing import Any

from pydantic import ConfigDict, Field, field_serializer

from backend.app.task.celery import celery_app
from backend.common.schema import SchemaBase


class TaskResultQueryParam(SchemaBase):
    """任务结果查询参数"""

    name: str | None = Field(None, description='任务名称')
    task_id: str | None = Field(None, description='任务 ID')


class TaskResultSchemaBase(SchemaBase):
    """任务结果基础模型"""

    task_id: str = Field(description='任务 ID')
    status: str = Field(description='执行状态')
    result: Any | None = Field(description='执行结果')
    date_done: datetime | None = Field(description='结束时间')
    traceback: str | None = Field(description='错误回溯')
    name: str | None = Field(description='任务名称')
    args: bytes | None = Field(description='任务位置参数')
    kwargs: bytes | None = Field(description='任务关键字参数')
    worker: str | None = Field(description='运行 Worker')
    retries: int | None = Field(description='重试次数')
    queue: str | None = Field(description='运行队列')


class DeleteTaskResultParam(SchemaBase):
    """删除任务结果参数"""

    pks: list[int] = Field(description='任务结果 ID 列表')


class GetTaskResultDetail(TaskResultSchemaBase):
    """任务结果详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='任务结果 ID')

    @field_serializer('result', 'args', 'kwargs', when_used='unless-none')
    def serialize_params(self, value: bytes | None) -> Any:
        return celery_app.backend.decode(value)
