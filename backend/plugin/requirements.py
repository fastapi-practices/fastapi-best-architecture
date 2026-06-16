import site
import subprocess
import sys

from importlib import invalidate_caches
from importlib.metadata import PackageNotFoundError, distribution
from pathlib import Path

from packaging.markers import default_environment
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from starlette.concurrency import run_in_threadpool

from backend.core.conf import settings
from backend.core.path_conf import PLUGIN_DIR
from backend.plugin.core import get_plugins
from backend.plugin.errors import PluginInstallError


def _is_in_virtualenv() -> bool:
    """检测当前是否在虚拟环境中运行"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)


def _requirements_installed(requirements_file: Path) -> bool:  # noqa: C901
    """检查 requirements 及其 extras 子依赖是否已安装"""
    requirements = []
    for line in requirements_file.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        try:
            requirements.append(Requirement(line))
        except Exception as e:
            raise PluginInstallError(f'依赖 {line} 格式错误: {e!s}') from e

    environment = default_environment()
    visited = set()

    def requirement_satisfied(requirement: Requirement, active_extras: frozenset[str] = frozenset({''})) -> bool:
        if requirement.marker and not any(
            requirement.marker.evaluate(environment={**environment, 'extra': extra}) for extra in active_extras
        ):
            return True

        try:
            dist = distribution(requirement.name)
        except PackageNotFoundError:
            return False

        if requirement.specifier and not requirement.specifier.contains(dist.version, prereleases=True):
            return False

        requested_extras = tuple(sorted(requirement.extras))
        state = (canonicalize_name(requirement.name), requested_extras)
        if state in visited:
            return True
        visited.add(state)

        child_active_extras = frozenset(requirement.extras) or frozenset({''})
        for dependency_line in dist.requires or []:
            try:
                dependency = Requirement(dependency_line)
            except Exception as e:
                raise PluginInstallError(f'依赖元数据 {dependency_line} 格式错误: {e!s}') from e
            if not requirement_satisfied(dependency, child_active_extras):
                return False

        return True

    return all(requirement_satisfied(requirement) for requirement in requirements)


def install_requirements(plugin: str | None) -> None:  # noqa: C901
    """
    安装插件依赖

    :param plugin: 指定插件名，否则检查所有插件
    :return:
    """
    plugins = [plugin] if plugin else get_plugins()

    for plugin in plugins:
        requirements_file = PLUGIN_DIR / plugin / 'requirements.txt'
        if not requirements_file.exists() or _requirements_installed(requirements_file):
            continue

        pip_install = ['uv', 'pip', 'install', '-r', str(requirements_file), '--prerelease=allow']
        if not _is_in_virtualenv():
            pip_install.append('--system')
        if settings.PLUGIN_PIP_CHINA:
            # 将国内源作为优先索引，同时保留 PyPI 作为回退来源
            pip_install.extend([
                '--index',
                settings.PLUGIN_PIP_INDEX_URL,
                '--index-strategy',
                'unsafe-best-match',
            ])

        max_retries = settings.PLUGIN_PIP_MAX_RETRY
        for attempt in range(max_retries):
            try:
                subprocess.check_call(pip_install)
                invalidate_caches()
                for site_dir in site.getsitepackages():
                    if site_dir.endswith('site-packages'):
                        site.addsitedir(site_dir)
                break
            except subprocess.TimeoutExpired:
                if attempt == max_retries - 1:
                    raise PluginInstallError(f'插件 {plugin} 依赖安装超时')
                continue
            except subprocess.CalledProcessError as e:
                if attempt == max_retries - 1:
                    raise PluginInstallError(f'插件 {plugin} 依赖安装失败：{e}') from e
                continue


def uninstall_requirements(plugin: str) -> None:
    """
    卸载插件依赖

    :param plugin: 插件名称
    :return:
    """
    requirements_file = PLUGIN_DIR / plugin / 'requirements.txt'
    if not requirements_file.exists():
        return

    try:
        pip_uninstall = ['uv', 'pip', 'uninstall', '-r', str(requirements_file)]
        if not _is_in_virtualenv():
            pip_uninstall.append('--system')
        subprocess.check_call(pip_uninstall, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        raise PluginInstallError(f'插件 {plugin} 依赖卸载失败：{e}') from e


async def install_requirements_async(plugin: str | None = None) -> None:
    """
    异步安装插件依赖

    由于 Windows 平台限制，无法实现完美的全异步方案，详情：
    https://stackoverflow.com/questions/44633458/why-am-i-getting-notimplementederror-with-async-and-await-on-windows
    """
    await run_in_threadpool(install_requirements, plugin)


async def uninstall_requirements_async(plugin: str) -> None:
    """
    异步卸载插件依赖

    :param plugin: 插件名称
    :return:
    """
    await run_in_threadpool(uninstall_requirements, plugin)
