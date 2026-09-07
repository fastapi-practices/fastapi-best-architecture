from datetime import datetime

from pydantic import ConfigDict, Field
from pydantic.types import JsonValue

from backend.app.task.enums import PeriodType, TaskSchedulerType
from backend.common.schema import SchemaBase


class TaskSchedulerSchemaBase(SchemaBase):
    """任务调度参数"""

    name: str = Field(description='任务名称')
    task: str = Field(description='要运行的 Celery 任务')
    args: JsonValue | None = Field(None, description='任务可接收的位置参数')
    kwargs: JsonValue | None = Field(None, description='任务可接收的关键字参数')
    queue: str | None = Field(None, description='CELERY_TASK_QUEUES 中定义的队列')
    exchange: str | None = Field(None, description='低级别 AMQP 路由的交换机')
    routing_key: str | None = Field(None, description='低级别 AMQP 路由的路由密钥')
    start_time: datetime | None = Field(None, description='任务开始触发的时间')
    expire_time: datetime | None = Field(None, description='任务不再触发的截止时间')
    expire_seconds: int | None = Field(None, description='任务不再触发的秒数时间差')
    type: TaskSchedulerType = Field(description='任务调度类型（0间隔 1定时）')
    interval_every: int | None = Field(None, description='任务再次运行前的间隔周期数')
    interval_period: PeriodType | None = Field(None, description='任务运行之间的周期类型')
    crontab: str = Field(default='* * * * *', description='Crontab 表达式')
    one_off: bool = Field(default=False, description='是否仅运行一次')
    remark: str | None = Field(None, description='备注')


class CreateTaskSchedulerParam(TaskSchedulerSchemaBase):
    """创建任务调度参数"""


class UpdateTaskSchedulerParam(TaskSchedulerSchemaBase):
    """更新任务调度参数"""


class GetTaskSchedulerDetail(TaskSchedulerSchemaBase):
    """任务调度详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='任务调度 ID')
    enabled: bool = Field(description='是否启用任务')
    total_run_count: int = Field(description='已运行总次数')
    last_run_time: datetime | None = Field(None, description='最后运行时间')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')
