import json
import os

from copy import deepcopy
from functools import lru_cache
from typing import Any

import rtoml

from backend.common.dataclasses import PluginEntry
from backend.common.enums import PluginLevelType, StatusType
from backend.common.log import log
from backend.core.conf import settings
from backend.core.path_conf import PLUGIN_DIR
from backend.database.redis import RedisCli
from backend.plugin.errors import PluginConfigError, PluginInjectError
from backend.plugin.status import get_plugin_enable
from backend.plugin.validator import validate_plugin_config
from backend.utils.async_helper import run_await
from backend.utils.dynamic_import import get_model_objects


def check_plugin_installed(plugin_name: str) -> bool:
    """
    检查插件是否已安装

    :param plugin_name: 插件名称
    :return:
    """
    return (PLUGIN_DIR / plugin_name / '__init__.py').exists()


def get_required_plugins() -> tuple[str, ...]:
    """获取必需插件列表"""
    required_plugins = list(settings.PLUGIN_REQUIRED)
    if not settings.RBAC_ROLE_MENU_MODE and 'casbin_rbac' not in required_plugins:
        required_plugins.append('casbin_rbac')
    return tuple(required_plugins)


def check_required_plugins() -> None:
    """检查必需插件"""
    required_plugins = get_required_plugins()
    missing_plugins = [name for name in required_plugins if not check_plugin_installed(name)]
    if missing_plugins:
        raise PluginInjectError(f'当前系统缺少以下插件: {", ".join(missing_plugins)}，请先安装对应插件')


@lru_cache(maxsize=128)
def get_plugins() -> tuple[str, ...]:
    """获取插件列表"""
    plugin_packages = []

    # 遍历插件目录
    for item in os.listdir(PLUGIN_DIR):
        item_path = PLUGIN_DIR / item
        if not os.path.isdir(item_path) and item == '__pycache__':
            continue

        # 检查是否为目录且包含 __init__.py 文件
        if os.path.isdir(item_path) and '__init__.py' in os.listdir(item_path):
            plugin_packages.append(item)

    return tuple(plugin_packages)


def get_enabled_plugins(plugins: tuple[str, ...] | None = None) -> set[str]:
    """
    获取已启用的插件列表

    :param plugins: 插件名称列表
    :return:
    """
    plugin_names = plugins or get_plugins()
    enabled_plugins = set(plugin_names)

    current_redis_client = RedisCli()
    run_await(current_redis_client.init)()

    try:
        for plugin in plugin_names:
            plugin_info = run_await(current_redis_client.get)(f'{settings.PLUGIN_REDIS_PREFIX}:{plugin}')
            if get_plugin_enable(plugin_info, StatusType.enable.value) != str(StatusType.enable.value):
                enabled_plugins.discard(plugin)
    finally:
        run_await(current_redis_client.aclose)()

    return enabled_plugins


def load_plugin_config(plugin: str) -> dict[str, Any]:
    """
    加载插件配置

    :param plugin: 插件名称
    :return:
    """
    toml_path = PLUGIN_DIR / plugin / 'plugin.toml'
    if not os.path.exists(toml_path):
        raise PluginInjectError(f'插件 {plugin} 缺少 plugin.toml 配置文件，请检查插件是否合法')

    with open(toml_path, encoding='utf-8') as f:
        return rtoml.load(f)


def normalize_plugin_config(
    plugin: str,
    plugin_config: dict[str, Any],
    plugin_cache_info: str | None = None,
) -> tuple[PluginLevelType, dict[str, Any]]:
    """校验并补齐插件运行时缓存信息。"""
    plugin_type = validate_plugin_config(plugin, plugin_config)
    normalized_config = deepcopy(plugin_config)
    normalized_config['plugin']['name'] = plugin
    normalized_config['plugin']['enable'] = get_plugin_enable(plugin_cache_info, StatusType.enable.value)
    return plugin_type, normalized_config


def build_plugin_entry(plugin: str, plugin_type: PluginLevelType, plugin_config: dict[str, Any]) -> PluginEntry:
    """从已校验配置构建插件运行入口。"""
    plugin_info = plugin_config['plugin']
    app_config = plugin_config.get('app') or {}
    return PluginEntry(
        name=plugin,
        level=plugin_type,
        depends_on=plugin_info.get('depends_on'),
        extend=app_config.get('extend') if plugin_type == PluginLevelType.extend else None,
        routers=app_config.get('router') if plugin_type == PluginLevelType.app else None,
        api=plugin_config.get('api') if plugin_type == PluginLevelType.extend else None,
    )


def parse_plugin_entries() -> list[PluginEntry]:
    """解析全部插件配置。"""
    plugins = get_plugins()
    plugin_entries: list[PluginEntry] = []

    # 使用独立连接
    current_redis_client = RedisCli()
    run_await(current_redis_client.init)()

    try:
        # 清理未知插件信息
        exclude_keys = [f'{settings.PLUGIN_REDIS_PREFIX}:{key}' for key in plugins]
        run_await(current_redis_client.delete_by_prefix)(
            settings.PLUGIN_REDIS_PREFIX,
            exclude_keys=exclude_keys,
        )

        for plugin in plugins:
            plugin_config = load_plugin_config(plugin)
            plugin_cache_key = f'{settings.PLUGIN_REDIS_PREFIX}:{plugin}'
            plugin_cache_info = run_await(current_redis_client.get)(plugin_cache_key)
            plugin_type, normalized_config = normalize_plugin_config(plugin, plugin_config, plugin_cache_info)
            plugin_entries.append(build_plugin_entry(plugin, plugin_type, normalized_config))

            # 缓存最新插件信息
            run_await(current_redis_client.set)(plugin_cache_key, json.dumps(normalized_config, ensure_ascii=False))

        # 重置插件变更状态
        run_await(current_redis_client.delete)(f'{settings.PLUGIN_REDIS_PREFIX}:changed')
    finally:
        run_await(current_redis_client.aclose)()

    return plugin_entries


def parse_plugin_config() -> tuple[list[PluginEntry], list[PluginEntry]]:
    """解析可注入路由的插件配置。"""
    plugin_entries = parse_plugin_entries()
    extend_plugins = [plugin for plugin in plugin_entries if plugin.level == PluginLevelType.extend]
    app_plugins = [plugin for plugin in plugin_entries if plugin.level == PluginLevelType.app]
    return extend_plugins, app_plugins


def resolve_plugin_order(plugins: list[PluginEntry]) -> list[PluginEntry]:
    """
    根据 depends_on 对插件排序

    :param plugins: 插件配置列表
    :return:
    """
    plugin_map = {plugin.name: plugin for plugin in plugins}
    ordered_plugins: list[PluginEntry] = []
    visited: set[str] = set()
    visiting: list[str] = []

    def visit(plugin: PluginEntry) -> None:
        if plugin.name in visited:
            return
        if plugin.name in visiting:
            cycle_start = visiting.index(plugin.name)
            cycle_path = [*visiting[cycle_start:], plugin.name]
            raise PluginConfigError(f'插件存在循环依赖: {" -> ".join(cycle_path)}')

        if plugin.depends_on is not None:
            visiting.append(plugin.name)
            for dep_name in plugin.depends_on:
                dep_plugin = plugin_map.get(dep_name)
                if dep_plugin is None:
                    raise PluginConfigError(f'插件 {plugin.name} 依赖插件 {dep_name}，但插件 {dep_name} 不存在')
                visit(dep_plugin)
            visiting.pop()

        visited.add(plugin.name)
        ordered_plugins.append(plugin)

    for plugin in plugins:
        visit(plugin)

    return ordered_plugins


def get_ordered_enabled_plugins() -> list[PluginEntry]:
    """获取按依赖排序后的已启用插件"""
    enabled_plugins = get_enabled_plugins()
    plugins = [plugin for plugin in parse_plugin_entries() if plugin.name in enabled_plugins]

    try:
        return resolve_plugin_order(plugins)
    except PluginConfigError as e:
        log.error(f'插件依赖解析失败: {e}')
        raise


def get_plugin_models() -> list[object]:
    """获取插件所有模型类"""
    objs = []

    for plugin in get_plugins():
        module_path = f'backend.plugin.{plugin}.model'
        model_objs = get_model_objects(module_path)
        if model_objs:
            objs.extend(model_objs)

    return objs
