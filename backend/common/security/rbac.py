from fastapi import Depends, Request

from backend.common.context import ctx
from backend.common.enums import MethodType, StatusType
from backend.common.exception import errors
from backend.common.security.jwt import DependsJwtAuth
from backend.core.conf import settings


async def rbac_verify(request: Request, _token: str = DependsJwtAuth) -> None:  # ruff:ignore[complex-structure]
    """
    RBAC 权限校验（鉴权顺序很重要，谨慎修改）

    :param request: FastAPI 请求对象
    :param _token: JWT 令牌
    :return:
    """
    path = request.url.path

    # API 鉴权白名单
    if path in settings.TOKEN_REQUEST_PATH_EXCLUDE:
        return
    for pattern in settings.TOKEN_REQUEST_PATH_EXCLUDE_PATTERN:
        if pattern.match(path):
            return

    # JWT 授权状态强制校验
    if not request.auth.scopes:
        raise errors.TokenError

    # 超级管理员免校验
    if request.user.is_superuser:
        return

    # 检测用户角色
    user_roles = request.user.roles
    enabled_roles = [role for role in user_roles if role.status == StatusType.enable]
    if not enabled_roles:
        raise errors.AuthorizationError(msg='用户所属角色已被锁定，请联系系统管理员')

    # 检测用户所属角色菜单
    if not any(len(role.menus) > 0 for role in enabled_roles):
        raise errors.AuthorizationError(msg='用户未分配菜单，请联系系统管理员')

    # 检测后台管理操作权限
    method = request.method
    if method not in {MethodType.GET, MethodType.OPTIONS} and not request.user.is_staff:
        raise errors.AuthorizationError(msg='用户已被禁止后台管理操作，请联系系统管理员')

    # RBAC 鉴权
    if settings.RBAC_ROLE_MENU_MODE:
        path_auth_perm = ctx.permission

        # 没有菜单操作权限标识不校验
        if not path_auth_perm:
            return

        # 菜单鉴权白名单
        if path_auth_perm in settings.RBAC_ROLE_MENU_EXCLUDE:
            return

        # 菜单去重
        unique_menus = {}
        for role in enabled_roles:
            for menu in role.menus:
                unique_menus[menu.id] = menu

        # 已分配菜单权限校验
        allow_perms = []
        for menu in list(unique_menus.values()):
            if menu.perms and menu.status == StatusType.enable:
                allow_perms.extend(menu.perms.split(','))
        if path_auth_perm not in allow_perms:
            raise errors.AuthorizationError
    else:
        # casbin 模式
        try:
            from backend.plugin.casbin_rbac.rbac import casbin_verify
        except ImportError:
            raise errors.ServerError(msg='Casbin RBAC 插件用法导入失败，请联系系统管理员')

        await casbin_verify(request)


# RBAC 授权依赖注入
DependsRBAC = Depends(rbac_verify)
