from datetime import datetime
from typing import Any

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class OperaLogSchemaBase(SchemaBase):
    """操作日志基础模型"""

    trace_id: str = Field(description='追踪 ID')
    username: str | None = Field(None, description='用户名')
    method: str = Field(description='请求方法')
    title: str = Field(description='操作标题')
    path: str = Field(description='请求路径')
    ip: str = Field(description='IP 地址')
    country: str | None = Field(None, description='国家')
    region: str | None = Field(None, description='地区')
    city: str | None = Field(None, description='城市')
    user_agent: str | None = Field(description='用户代理')
    os: str | None = Field(None, description='操作系统')
    browser: str | None = Field(None, description='浏览器')
    device: str | None = Field(None, description='设备')
    args: dict[str, Any] | None = Field(None, description='请求参数')
    status: StatusType = Field(description='状态')
    code: str = Field(description='状态码')
    msg: str | None = Field(None, description='消息')
    cost_time: float = Field(description='耗时')
    opera_time: datetime = Field(description='操作时间')


class CreateOperaLogParam(OperaLogSchemaBase):
    """创建操作日志参数"""


class UpdateOperaLogParam(OperaLogSchemaBase):
    """更新操作日志参数"""


class DeleteOperaLogParam(SchemaBase):
    """删除操作日志参数"""

    pks: list[int] = Field(description='操作日志 ID 列表')


class GetOperaLogDetail(OperaLogSchemaBase):
    """操作日志详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='日志 ID')
    created_time: datetime = Field(description='创建时间')
