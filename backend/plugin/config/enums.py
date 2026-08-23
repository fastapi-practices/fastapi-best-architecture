from backend.common.enums import StrEnum


class ConfigType(StrEnum):
    """配置类型"""

    user_security = 'USER_SECURITY'
    login = 'LOGIN'
