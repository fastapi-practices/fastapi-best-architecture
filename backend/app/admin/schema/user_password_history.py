from pydantic import Field

from backend.common.schema import SchemaBase


class UserPasswordHistorySchemaBase(SchemaBase):
    """用户历史密码记录基础模型"""

    user_id: int = Field(description='用户 ID')
    password: str = Field(description='历史密码')


class CreateUserPasswordHistoryParam(UserPasswordHistorySchemaBase):
    """创建用户历史密码记录"""
