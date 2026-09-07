from pydantic import Field

from backend.common.schema import SchemaBase


class GetTaskRegisteredDetail(SchemaBase):
    """已注册任务详情"""

    name: str = Field(description='任务名称')
    task: str = Field(description='任务函数')
