from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class ConfigTypeQueryParam(SchemaBase):
    """参数配置类型查询参数"""

    type: str | None = Field(None, description='参数配置类型')


class ConfigQueryParam(SchemaBase):
    """参数配置查询参数"""

    name: str | None = Field(None, description='参数配置名称')
    type: str | None = Field(None, description='参数配置类型')


class ConfigSchemaBase(SchemaBase):
    """参数配置基础模型"""

    name: str = Field(description='参数配置名称')
    type: str | None = Field(None, description='参数配置类型')
    key: str = Field(description='参数配置键名')
    value: str = Field(description='参数配置值')
    is_frontend: bool = Field(description='是否前端参数配置')
    remark: str | None = Field(None, description='备注')


class CreateConfigParam(ConfigSchemaBase):
    """创建参数配置参数"""


class UpdateConfigParam(ConfigSchemaBase):
    """更新参数配置参数"""


class UpdateConfigsParam(UpdateConfigParam):
    """批量更新参数配置参数"""

    id: int = Field(description='参数配置 ID')


class GetConfigDetail(ConfigSchemaBase):
    """参数配置详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='参数配置 ID')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')
