import json

from typing import cast

from fastapi import Request

from backend.common.enums import StatusType
from backend.common.exception import errors
from backend.common.log import log
from backend.core.conf import settings
from backend.database.redis import redis_client
from backend.plugin.errors import PluginInjectError


def get_plugin_enable(plugin_info: str | None, default_status: int) -> str:
    """
    解析插件启用状态

    :param plugin_info: 插件缓存信息
    :param default_status: 默认状态值
    :return:
    """
    if not plugin_info:
        return str(default_status)

    try:
        return json.loads(plugin_info)['plugin']['enable']
    except Exception:
        return str(default_status)


class PluginStatusChecker:
    """插件状态检查器"""

    def __init__(self, plugin: str) -> None:
        """
        初始化插件状态检查器

        :param plugin: 插件名称
        :return:
        """
        self.plugin = plugin

    async def __call__(self, request: Request) -> None:
        """
        验证插件状态

        :param request: FastAPI 请求对象
        :return:
        """
        plugin_info = cast('str', await redis_client.get(f'{settings.PLUGIN_REDIS_PREFIX}:{self.plugin}'))
        if not plugin_info:
            log.error('插件状态未初始化或丢失，需重启服务自动修复')
            raise PluginInjectError('插件状态未初始化或丢失，请联系系统管理员')

        if get_plugin_enable(plugin_info, StatusType.disable.value) != str(StatusType.enable.value):
            raise errors.ServerError(msg=f'插件 {self.plugin} 未启用，请联系系统管理员')
