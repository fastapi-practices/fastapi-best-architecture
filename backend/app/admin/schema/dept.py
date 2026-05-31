from datetime import datetime

from pydantic import ConfigDict, Field

from backend.common.enums import StatusType
from backend.common.schema import CustomEmailStr, CustomPhoneNumber, SchemaBase


class DeptSchemaBase(SchemaBase):
    """部门基础模型"""

    name: str = Field(description='部门名称')
    parent_id: int | None = Field(None, description='部门父级 ID')
    sort: int = Field(0, ge=0, description='排序')
    leader: str | None = Field(None, description='负责人')
    phone: CustomPhoneNumber | None = Field(None, description='联系电话')
    email: CustomEmailStr | None = Field(None, description='邮箱')
    status: StatusType = Field(description='状态')


class CreateDeptParam(DeptSchemaBase):
    """创建部门参数"""


class UpdateDeptParam(DeptSchemaBase):
    """更新部门参数"""


class GetDeptDetail(DeptSchemaBase):
    """部门详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='部门 ID')
    deleted: int = Field(description='是否已删除（0：否；id：是）')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')
    deleted_time: datetime | None = Field(None, description='删除时间')


class GetDeptTree(GetDeptDetail):
    """获取部门树"""

    children: list['GetDeptTree'] | None = Field(None, description='子菜单')
