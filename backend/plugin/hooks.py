import inspect

from typing import Any

from fastapi import FastAPI

from backend.common.enums import LifespanStage
from backend.common.lifespan import lifespan_manager
from backend.common.log import log
from backend.plugin.core import get_ordered_enabled_plugins
from backend.plugin.errors import PluginInjectError
from backend.utils.async_helper import run_await
from backend.utils.dynamic_import import import_module_cached


def register_plugin_lifespan_hook(plugin: str, module: Any) -> None:
    """
    注册插件 lifespan hook

    :param plugin: 插件名称
    :param module: 插件 hooks 模块
    :return:
    """
    lifespan_hook = getattr(module, 'lifespan', None)
    if lifespan_hook is None:
        return

    if not callable(lifespan_hook):
        log.warning(f'插件 {plugin} 的 lifespan 不是可调用对象，已跳过')
        return

    lifespan_manager.register(lifespan_hook, stage=LifespanStage.plugin)  # type: ignore[call-overload]
    log.info(f'插件 {plugin} lifespan hook 注册成功')


def run_plugin_setup_hook(plugin: str, module: Any, app: FastAPI) -> None:
    """
    执行插件 setup hook

    :param plugin: 插件名称
    :param module: 插件 hooks 模块
    :param app: FastAPI 应用实例
    :return:
    """
    setup_hook = getattr(module, 'setup', None)
    if setup_hook is None:
        return

    if not callable(setup_hook):
        log.warning(f'插件 {plugin} 的 setup 不是可调用对象，已跳过')
        return

    setup_result = setup_hook(app)
    if inspect.isawaitable(setup_result):
        run_await(lambda: setup_result)()  # type: ignore
    log.info(f'插件 {plugin} setup hook 执行成功')


def run_plugin_otel_hook(plugin: str, module: Any, app: FastAPI) -> None:
    """
    执行插件 OpenTelemetry hook

    :param plugin: 插件名称
    :param module: 插件 hooks 模块
    :param app: FastAPI 应用实例
    :return:
    """
    otel_hook = getattr(module, 'otel', None)
    if otel_hook is None:
        return

    if not callable(otel_hook):
        log.warning(f'插件 {plugin} 的 otel 不是可调用对象，已跳过')
        return

    otel_result = otel_hook(app)
    if inspect.isawaitable(otel_result):
        run_await(lambda: otel_result)()  # type: ignore
    log.info(f'插件 {plugin} otel hook 执行成功')


def _get_plugin_hook_modules() -> list[tuple[str, Any]]:
    """
    获取插件 hooks 模块

    :return:
    """
    plugin_hook_modules: list[tuple[str, Any]] = []

    for plugin in get_ordered_enabled_plugins():
        module_path = f'backend.plugin.{plugin.name}.hooks'
        try:
            module = import_module_cached(module_path)
        except ModuleNotFoundError as e:
            if e.name == module_path:
                continue
            log.warning(f'插件 {plugin.name} hooks 加载失败: {e}')
            continue
        except Exception as e:
            log.warning(f'插件 {plugin.name} hooks 加载失败: {e}')
            continue

        plugin_hook_modules.append((plugin.name, module))

    return plugin_hook_modules


def register_plugin_hooks(app: FastAPI) -> None:
    """
    注册并执行插件 hooks

    :param app: FastAPI 应用实例
    :return:
    """

    def run_setup_hook(plugin: str, module: Any) -> None:
        try:
            register_plugin_lifespan_hook(plugin, module)
        except Exception as e:
            log.exception(f'插件 {plugin} lifespan hooks 执行失败: {e}')
            raise PluginInjectError(f'插件 {plugin} lifespan hooks 执行失败：{e!s}') from e
        try:
            run_plugin_setup_hook(plugin, module, app)
        except Exception as e:
            log.exception(f'插件 {plugin} setup hooks 执行失败: {e}')
            raise PluginInjectError(f'插件 {plugin} setup hooks 执行失败：{e!s}') from e

    for plugin, module in _get_plugin_hook_modules():
        run_setup_hook(plugin, module)


def init_plugin_otel_hooks(app: FastAPI) -> None:
    """
    初始化插件 OpenTelemetry hooks

    :param app: FastAPI 应用实例
    :return:
    """

    def run_otel_hook(plugin: str, module: Any) -> None:
        try:
            run_plugin_otel_hook(plugin, module, app)
        except Exception as e:
            log.exception(f'插件 {plugin} otel hook 执行失败: {e}')
            raise PluginInjectError(f'插件 {plugin} otel hook 执行失败：{e!s}') from e

    for plugin, module in _get_plugin_hook_modules():
        run_otel_hook(plugin, module)
