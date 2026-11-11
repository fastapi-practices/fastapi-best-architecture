from pydantic import Field

from backend.common.enums import PluginType
from backend.common.schema import SchemaBase


class PluginInstallQueryParam(SchemaBase):
    """插件安装查询参数"""

    type: PluginType = Field(description='插件类型')
    repo_url: str | None = Field(None, description='插件 git 仓库地址')
