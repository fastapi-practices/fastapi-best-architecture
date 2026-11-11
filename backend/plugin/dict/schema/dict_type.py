from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.schema import SchemaBase


class DictTypeQueryParam(SchemaBase):
    """字典类型查询参数"""

    name: str | None = Field(None, description='字典类型名称')
    code: str | None = Field(None, description='字典类型编码')


class DictTypeSchemaBase(SchemaBase):
    """字典类型基础模型"""

    name: str = Field(description='字典名称')
    code: str = Field(description='字典编码')
    remark: str | None = Field(None, description='备注')


class CreateDictTypeParam(DictTypeSchemaBase):
    """创建字典类型参数"""


class UpdateDictTypeParam(DictTypeSchemaBase):
    """更新字典类型参数"""


class DeleteDictTypeParam(SchemaBase):
    """删除字典类型参数"""

    pks: list[int] = Field(description='字典类型 ID 列表')


class GetDictTypeDetail(DictTypeSchemaBase):
    """字典类型详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='字典类型 ID')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')
