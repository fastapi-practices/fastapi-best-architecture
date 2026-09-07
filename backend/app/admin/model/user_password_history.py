from datetime import datetime

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import DataClassBase, TenantMixin, TimeZone, id_key
from backend.utils.timezone import timezone


class UserPasswordHistory(DataClassBase, TenantMixin):
    """用户密码历史记录表"""

    __tablename__ = 'sys_user_password_history'

    id: Mapped[id_key] = mapped_column(init=False)
    user_id: Mapped[int] = mapped_column(sa.BigInteger, index=True, comment='用户 ID')
    password: Mapped[str] = mapped_column(sa.String(256), comment='历史密码')
    created_time: Mapped[datetime] = mapped_column(
        TimeZone,
        init=False,
        default_factory=timezone.now,
        comment='创建时间',
    )
