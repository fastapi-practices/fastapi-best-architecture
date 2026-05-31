from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class LoginLogSchemaBase(SchemaBase):
    """登录日志基础模型"""

    user_uuid: str = Field(description='用户 UUID')
    username: str = Field(description='用户名')
    status: int = Field(description='登录状态')
    ip: str = Field(description='IP 地址')
    country: str | None = Field(None, description='国家')
    region: str | None = Field(None, description='地区')
    city: str | None = Field(None, description='城市')
    user_agent: str | None = Field(description='用户代理')
    browser: str | None = Field(None, description='浏览器')
    os: str | None = Field(None, description='操作系统')
    device: str | None = Field(None, description='设备')
    msg: str = Field(description='消息')
    login_time: datetime = Field(description='登录时间')


class CreateLoginLogParam(LoginLogSchemaBase):
    """创建登录日志参数"""


class UpdateLoginLogParam(LoginLogSchemaBase):
    """更新登录日志参数"""


class DeleteLoginLogParam(SchemaBase):
    """删除登录日志参数"""

    pks: list[int] = Field(description='登录日志 ID 列表')


class GetLoginLogDetail(LoginLogSchemaBase):
    """登录日志详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='日志 ID')
    created_time: datetime = Field(description='创建时间')
