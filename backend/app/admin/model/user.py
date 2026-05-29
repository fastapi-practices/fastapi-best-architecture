from datetime import datetime

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, TimeZone, id_key
from backend.database.db import uuid4_str
from backend.utils.timezone import timezone


class User(Base):
    """用户表"""

    __tablename__ = 'sys_user'
    __table_args__ = (
        sa.UniqueConstraint('username', 'deleted', name='uk_sys_user_username_deleted'),
        sa.UniqueConstraint('email', 'deleted', name='uk_sys_user_email_deleted'),
        {'comment': '用户表'},
    )

    id: Mapped[id_key] = mapped_column(init=False)
    uuid: Mapped[str] = mapped_column(sa.String(64), init=False, default_factory=uuid4_str, unique=True)
    username: Mapped[str] = mapped_column(sa.String(64), index=True, comment='用户名')
    nickname: Mapped[str] = mapped_column(sa.String(64), comment='昵称')
    password: Mapped[str | None] = mapped_column(sa.String(256), comment='密码')
    salt: Mapped[bytes | None] = mapped_column(sa.LargeBinary(255), comment='加密盐')
    email: Mapped[str | None] = mapped_column(sa.String(256), default=None, index=True, comment='邮箱')
    phone: Mapped[str | None] = mapped_column(sa.String(11), default=None, comment='手机号')
    avatar: Mapped[str | None] = mapped_column(sa.String(256), default=None, comment='头像')
    status: Mapped[int] = mapped_column(default=1, index=True, comment='用户账号状态(0停用 1正常)')
    is_superuser: Mapped[bool] = mapped_column(default=False, comment='超级权限(0否 1是)')
    is_staff: Mapped[bool] = mapped_column(default=False, comment='后台管理登陆(0否 1是)')
    is_multi_login: Mapped[bool] = mapped_column(default=False, comment='是否重复登陆(0否 1是)')
    join_time: Mapped[datetime] = mapped_column(TimeZone, init=False, default_factory=timezone.now, comment='注册时间')
    last_login_time: Mapped[datetime | None] = mapped_column(
        TimeZone, init=False, onupdate=timezone.now, comment='上次登录时间'
    )
    last_password_changed_time: Mapped[datetime | None] = mapped_column(
        TimeZone, init=False, default_factory=timezone.now, comment='上次密码变更时间'
    )

    # 逻辑外键
    dept_id: Mapped[int | None] = mapped_column(sa.BigInteger, default=None, comment='部门关联ID')
