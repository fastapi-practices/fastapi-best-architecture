from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import InvalidVersion, Version

from backend.common.dataclasses import CompatibilityResult
from backend.plugin.errors import PluginConfigError

# fba 版本声明遵循 PEP 440 版本声明规范
# https://packaging.python.org/en/latest/specifications/version-specifiers/


def parse_fba_specifier(plugin_name: str, specifier: str) -> SpecifierSet:
    """
    解析插件声明的 fba 版本声明

    :param plugin_name: 插件名称
    :param specifier: 版本声明，如 ">=1.17.0,<2.0.0"
    :return:
    """
    value = specifier.strip()
    if not value:
        raise PluginConfigError(f'插件 {plugin_name} 未声明 fba_version 版本要求')

    try:
        return SpecifierSet(value)
    except InvalidSpecifier as e:
        raise PluginConfigError(
            f'插件 {plugin_name} 的 fba_version 声明非法: {value}，'
            f'应为 PEP 440 版本声明，如 ">=1.17.0"、">=1.17.0,<2.0.0"、"~=1.17"、"==1.17.0"'
        ) from e


def get_fba_version() -> Version:
    """
    获取当前 fba 版本

    版本号必须在函数内延迟导入，backend 包初始化阶段会注册所有模型并导入插件模块，
    此时模块级导入 backend 会触发循环导入

    :return:
    """
    from backend import __version__

    try:
        return Version(__version__)
    except InvalidVersion as e:
        raise PluginConfigError(f'fba 版本号非法，当前值: {__version__}') from e


def check_fba_compatibility(plugin_name: str, specifier: str) -> CompatibilityResult:
    """
    检测插件与当前 fba 版本的兼容性

    预发布版本默认排除在版本声明之外，但已安装的预发布版本应当被接受

    :param plugin_name: 插件名称
    :param specifier: 版本声明，如 ">=1.17.0,<2.0.0"
    :return:
    """
    specifier_set = parse_fba_specifier(plugin_name, specifier)
    current = get_fba_version()
    prereleases = True if current.is_prerelease else None
    return CompatibilityResult(
        compatible=specifier_set.contains(current, prereleases=prereleases),
        required=specifier.strip(),
        current=str(current),
    )


def validate_fba_compatibility(plugin_name: str, specifier: str) -> None:
    """
    校验插件与当前 fba 版本的兼容性，不兼容时抛出异常

    :param plugin_name: 插件名称
    :param specifier: 版本声明，如 ">=1.17.0,<2.0.0"
    :return:
    """
    result = check_fba_compatibility(plugin_name, specifier)
    if not result.compatible:
        raise PluginConfigError(
            f'插件 {plugin_name} 与当前 fba 版本不兼容，要求 fba 版本 {result.required}，当前版本 {result.current}'
        )
