from datetime import datetime

from pydantic import Field

from backend.app.admin.schema.user import GetUserInfoDetail
from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class OnlineSessionQueryParam(SchemaBase):
    """在线会话查询参数"""

    username: str | None = Field(None, description='用户名')


class DeleteSessionQueryParam(SchemaBase):
    """强制下线查询参数"""

    session_uuid: str = Field(description='会话 UUID')


class GetSwaggerToken(SchemaBase):
    """Swagger 认证令牌"""

    access_token: str = Field(description='访问令牌')
    token_type: str = Field('Bearer', description='令牌类型')
    user: GetUserInfoDetail = Field(description='用户信息')


class AccessTokenBase(SchemaBase):
    """访问令牌基础模型"""

    access_token: str = Field(description='访问令牌')
    access_token_expire_time: datetime = Field(description='令牌过期时间')
    session_uuid: str = Field(description='会话 UUID')


class GetNewToken(AccessTokenBase):
    """获取新令牌"""


class GetLoginToken(AccessTokenBase):
    """获取登录令牌"""

    password_expire_days_remaining: int | None = Field(None, description='密码过期剩余天数')
    user: GetUserInfoDetail = Field(description='用户信息')


class GetTokenDetail(SchemaBase):
    """令牌详情"""

    id: int = Field(description='用户 ID')
    session_uuid: str = Field(description='会话 UUID')
    username: str = Field(description='用户名')
    nickname: str = Field(description='昵称')
    ip: str = Field(description='IP 地址')
    os: str = Field(description='操作系统')
    browser: str = Field(description='浏览器')
    device: str = Field(description='设备')
    status: StatusType = Field(description='状态')
    last_login_time: str = Field(description='最后登录时间')
    expire_time: datetime = Field(description='过期时间')
