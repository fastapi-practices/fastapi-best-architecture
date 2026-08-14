from sqlalchemy.ext.asyncio import AsyncSession

from backend.utils.dynamic_config import load_config, str_to_bool


async def load_email_config(db: AsyncSession) -> None:
    """
    获取邮箱配置

    :param db: 数据库会话
    :return:
    """
    mapping = {
        'EMAIL_HOST': str,
        'EMAIL_PORT': int,
        'EMAIL_SSL': str_to_bool,
        'EMAIL_USERNAME': str,
        'EMAIL_PASSWORD': str,
    }
    await load_config(db, 'email', mapping, 'EMAIL_CONFIG_STATUS')
