from enum import Enum
from enum import IntEnum as SourceIntEnum
from typing import Any, TypeVar

T = TypeVar('T', bound=Enum)


class _EnumBase:
    """枚举基类，提供通用方法"""

    @classmethod
    def get_member_keys(cls) -> list[str]:
        """获取枚举成员名称列表"""
        return list(cls.__members__.keys())

    @classmethod
    def get_member_values(cls) -> list:
        """获取枚举成员值列表"""
        return [item.value for item in cls.__members__.values()]

    @classmethod
    def get_member_dict(cls) -> dict[str, Any]:
        """获取枚举成员字典"""
        return {name: item.value for name, item in cls.__members__.items()}


class IntEnum(_EnumBase, SourceIntEnum):
    """整型枚举基类"""


class StrEnum(_EnumBase, str, Enum):
    """字符串枚举基类"""


class MenuType(IntEnum):
    """菜单类型"""

    directory = 0
    menu = 1
    button = 2
    embedded = 3
    link = 4


class RoleDataRuleOperatorType(IntEnum):
    """数据规则运算符"""

    AND = 0
    OR = 1


class RoleDataRuleExpressionType(IntEnum):
    """数据规则表达式"""

    eq = 0  # ==
    ne = 1  # !=
    gt = 2  # >
    ge = 3  # >=
    lt = 4  # <
    le = 5  # <=
    in_ = 6
    not_in = 7


class MethodType(StrEnum):
    """HTTP 请求方法"""

    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    OPTIONS = 'OPTIONS'


class LoginLogStatusType(IntEnum):
    """登录日志状态"""

    fail = 0
    success = 1


class BuildTreeType(StrEnum):
    """构建树形结构类型"""

    traversal = 'traversal'
    recursive = 'recursive'


class OperaLogCipherType(IntEnum):
    """操作日志加密类型"""

    aes = 0
    md5 = 1
    itsdangerous = 2
    plain = 3


class StatusType(IntEnum):
    """状态类型"""

    disable = 0
    enable = 1


class FileType(StrEnum):
    """文件类型"""

    image = 'image'
    video = 'video'


class PluginLevelType(StrEnum):
    """插件级别类型"""

    app = 'app'
    capability = 'capability'
    extend = 'extend'


class PluginType(StrEnum):
    """插件类型"""

    zip = 'zip'
    git = 'git'


class UserPermissionType(StrEnum):
    """用户权限类型"""

    superuser = 'superuser'
    staff = 'staff'
    status = 'status'
    multi_login = 'multi_login'


class DataBaseType(StrEnum):
    """数据库类型"""

    mysql = 'mysql'
    postgresql = 'postgresql'


class PrimaryKeyType(StrEnum):
    """主键类型"""

    autoincrement = 'autoincrement'
    snowflake = 'snowflake'


class LifespanStage(IntEnum):
    """lifespan 执行阶段"""

    core = 0
    plugin = 1
    tail = 2
