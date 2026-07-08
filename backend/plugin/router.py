import os
import warnings

from fastapi import APIRouter, Depends

from backend.common.dataclasses import PluginEntry
from backend.core.path_conf import PLUGIN_DIR
from backend.plugin.errors import PluginConfigError, PluginInjectError
from backend.plugin.status import PluginStatusChecker
from backend.utils.dynamic_import import import_module_cached


def _invalid_router_msg(plugin: str, module_path: str, level: str) -> str:
    return f'{level}插件 {plugin} 模块 {module_path} 中没有有效的 router，请检查插件文件是否完整'


def inject_extend_router(plugin: PluginEntry) -> None:
    """
    扩展级插件路由注入

    :param plugin: 插件名称
    :return:
    """
    plugin_api_path = PLUGIN_DIR / plugin.name / 'api'
    if not os.path.exists(plugin_api_path):
        raise PluginConfigError(f'插件 {plugin.name} 缺少 api 目录，请检查插件文件是否完整')

    for root, _, api_files in os.walk(plugin_api_path):
        for file in api_files:
            if not (file.endswith('.py') and file != '__init__.py'):
                continue

            # 解析插件路由配置
            file_config = plugin.api[file[:-3]]
            prefix = file_config['prefix']
            tags = file_config['tags']

            # 获取插件路由模块
            file_path = os.path.join(root, file)
            path_to_module_str = os.path.relpath(file_path, PLUGIN_DIR).replace(os.sep, '.')[:-3]
            module_path = f'backend.plugin.{path_to_module_str}'

            try:
                module = import_module_cached(module_path)
                plugin_router = getattr(module, 'router', None)
                if not plugin_router:
                    msg = _invalid_router_msg(plugin.name, module_path, '扩展级')
                    warnings.warn(
                        msg,
                        FutureWarning,
                    )
                    continue

                # 获取目标 app 路由
                relative_path = os.path.relpath(root, plugin_api_path)
                app_name = plugin.extend
                target_module_path = f'backend.app.{app_name}.api.{relative_path.replace(os.sep, ".")}'
                target_module = import_module_cached(target_module_path)
                target_router = getattr(target_module, 'router', None)

                if not target_router or not isinstance(target_router, APIRouter):
                    raise PluginInjectError(_invalid_router_msg(plugin.name, module_path, '扩展级'))

                # 将插件路由注入到目标路由中
                target_router.include_router(
                    router=plugin_router,
                    prefix=prefix,
                    tags=[tags] if tags else [],
                    dependencies=[Depends(PluginStatusChecker(plugin.name))],
                )
            except Exception as e:
                raise PluginInjectError(f'扩展级插件 {plugin.name} 路由注入失败：{e!s}') from e


def inject_app_router(plugin: PluginEntry, target_router: APIRouter) -> None:
    """
    应用级插件路由注入

    :param plugin: 插件名称
    :param target_router: FastAPI 路由器
    :return:
    """
    module_path = f'backend.plugin.{plugin.name}.api.router'
    try:
        module = import_module_cached(module_path)
        routers = plugin.routers
        if not routers or not isinstance(routers, list):
            raise PluginConfigError(f'应用级插件 {plugin.name} 配置文件存在错误，请检查')

        for router in routers:
            plugin_router = getattr(module, router, None)
            if not plugin_router or not isinstance(plugin_router, APIRouter):
                raise PluginInjectError(_invalid_router_msg(plugin.name, module_path, '应用级'))

            # 将插件路由注入到目标路由中
            target_router.include_router(plugin_router, dependencies=[Depends(PluginStatusChecker(plugin.name))])
    except Exception as e:
        raise PluginInjectError(f'应用级插件 {plugin.name} 路由注入失败：{e!s}') from e


def build_final_router() -> APIRouter:
    """构建最终路由"""
    from backend.plugin.core import parse_plugin_config, resolve_plugin_order

    extend_plugins, app_plugins = parse_plugin_config()
    plugins = extend_plugins + app_plugins
    ordered_plugins = resolve_plugin_order(plugins)

    for plugin in ordered_plugins:
        if plugin.api is not None:
            inject_extend_router(plugin)

    # 主路由，必须在扩展级插件路由注入后，应用级插件路由注入前导入
    from backend.app.router import router as main_router

    for plugin in ordered_plugins:
        if plugin.routers is not None:
            inject_app_router(plugin, main_router)

    return main_router
