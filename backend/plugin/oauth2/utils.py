from backend.common.exception import errors
from backend.core.conf import settings
from backend.plugin.oauth2.enums import UserSocialType


async def get_oauth2_authorization_url(*, source: UserSocialType, state: str) -> str:
    """
    获取 OAuth2 授权链接

    :param source: 社交平台
    :param state: OAuth2 状态值
    :return:
    """
    match source:
        case UserSocialType.github:
            from backend.plugin.oauth2.api.v1.github import github_client

            auth_url = await github_client.get_authorization_url(
                redirect_uri=settings.OAUTH2_GITHUB_REDIRECT_URI,
                state=state,
            )
        case UserSocialType.google:
            from backend.plugin.oauth2.api.v1.google import google_client

            auth_url = await google_client.get_authorization_url(
                redirect_uri=settings.OAUTH2_GOOGLE_REDIRECT_URI,
                state=state,
            )
        case _:
            raise errors.ForbiddenError(msg=f'暂不支持 {source} OAuth2 授权')

    return auth_url
