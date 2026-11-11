from datetime import datetime

from pydantic import ConfigDict, Field

from backend.app.admin.schema.data_scope import GetDataScopeWithRelationDetail
from backend.app.admin.schema.menu import GetMenuDetail
from backend.common.enums import StatusType
from backend.common.schema import SchemaBase


class RoleQueryParam(SchemaBase):
    """角色查询参数"""

    name: str | None = Field(None, description='角色名称')
    status: int | None = Field(None, description='状态')


class RoleSchemaBase(SchemaBase):
    """角色基础模型"""

    name: str = Field(description='角色名称')
    status: StatusType = Field(description='状态')
    is_filter_scopes: bool = Field(True, description='过滤数据权限')
    remark: str | None = Field(None, description='备注')


class CreateRoleParam(RoleSchemaBase):
    """创建角色参数"""


class UpdateRoleParam(RoleSchemaBase):
    """更新角色参数"""


class DeleteRoleParam(SchemaBase):
    """删除角色参数"""

    pks: list[int] = Field(description='角色 ID 列表')


class CreateRoleMenuParam(SchemaBase):
    """创建角色菜单参数"""

    role_id: int = Field(description='角色 ID')
    menu_id: int = Field(description='菜单 ID')


class UpdateRoleMenuParam(SchemaBase):
    """更新角色菜单参数"""

    menu_ids: list[int] = Field(description='菜单 ID 列表')


class CreateRoleScopeParam(SchemaBase):
    """创建角色数据范围参数"""

    role_id: int = Field(description='角色 ID')
    data_scope_id: int = Field(description='数据范围 ID')


class UpdateRoleScopeParam(SchemaBase):
    """更新角色数据范围参数"""

    scope_ids: list[int] = Field(description='数据范围 ID 列表')


class GetRoleDetail(RoleSchemaBase):
    """角色详情"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(description='角色 ID')
    created_time: datetime = Field(description='创建时间')
    updated_time: datetime | None = Field(None, description='更新时间')


class GetRoleWithRelationDetail(GetRoleDetail):
    """角色关联详情"""

    menus: list[GetMenuDetail | None] = Field([], description='菜单详情列表')
    scopes: list[GetDataScopeWithRelationDetail | None] = Field([], description='数据范围列表')
