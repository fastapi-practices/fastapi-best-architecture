from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.admin.crud.crud_user_password_history import user_password_history_dao
from backend.common.exception import errors
from backend.common.i18n import t
from backend.core.conf import settings
from backend.utils.dynamic_config import load_user_security_config
from backend.utils.pattern_validate import is_has_letter, is_has_number, is_has_special_char

password_hash = PasswordHash((BcryptHasher(),))


def get_hash_password(password: str, salt: bytes | None) -> str:
    """
    使用哈希算法加密密码

    :param password: 密码
    :param salt: 盐值
    :return:
    """
    return password_hash.hash(password, salt=salt)


def password_verify(plain_password: str, hashed_password: str) -> bool:
    """
    密码验证

    :param plain_password: 待验证的密码
    :param hashed_password: 哈希密码
    :return:
    """
    return password_hash.verify(plain_password, hashed_password)


async def validate_new_password(db: AsyncSession, user_id: int, new_password: str) -> None:
    """
    验证新密码

    :param db: 数据库会话
    :param user_id: 用户ID
    :param new_password: 新密码
    :return:
    """
    await load_user_security_config(db)

    if len(new_password) < settings.USER_PASSWORD_MIN_LENGTH:
        raise errors.RequestError(msg=t('error.password.too_short', min_length=settings.USER_PASSWORD_MIN_LENGTH))

    if len(new_password) > settings.USER_PASSWORD_MAX_LENGTH:
        raise errors.RequestError(msg=t('error.password.too_long', max_length=settings.USER_PASSWORD_MAX_LENGTH))

    if not is_has_number(new_password):
        raise errors.RequestError(msg=t('error.password.need_digit'))

    if not is_has_letter(new_password):
        raise errors.RequestError(msg=t('error.password.need_letter'))

    if settings.USER_PASSWORD_REQUIRE_SPECIAL_CHAR and not is_has_special_char(new_password):
        raise errors.RequestError(msg=t('error.password.need_special'))

    password_history = await user_password_history_dao.get_by_user_id(db, user_id)

    for hist in password_history[: settings.USER_PASSWORD_HISTORY_CHECK_COUNT]:
        if password_verify(new_password, hist.password):
            raise errors.RequestError(msg=t('error.password.reused', count=settings.USER_PASSWORD_HISTORY_CHECK_COUNT))
