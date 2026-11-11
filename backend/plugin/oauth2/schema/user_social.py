from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase
from backend.plugin.oauth2.enums import UserSocialType


class UserSocialQueryParam(SchemaBase):
    """用户社交查询参数"""

    source: UserSocialType


class UserSocialSchemaBase(SchemaBase):
    """用户社交基础模型"""

    sid: str = Field(description='第三方用户 ID')
    source: UserSocialType = Field(description='社交平台')


class CreateUserSocialParam(UserSocialSchemaBase):
    """创建用户社交参数"""

    user_id: int = Field(description='用户 ID')


class UpdateUserSocialParam(SchemaBase):
    """更新用户社交参数"""


class GetUserSocialDetail(CreateUserSocialParam):
    """获取用户社交详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='用户社交 ID')
