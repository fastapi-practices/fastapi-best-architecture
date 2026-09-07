from datetime import datetime

import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import DataClassBase, TenantMixin, TimeZone, UniversalText, id_key
from backend.utils.timezone import timezone


class LoginLog(DataClassBase, TenantMixin):
    """登录日志表"""

    __tablename__ = 'sys_login_log'

    id: Mapped[id_key] = mapped_column(init=False)
    user_uuid: Mapped[str] = mapped_column(sa.String(64), comment='用户UUID')
    username: Mapped[str] = mapped_column(sa.String(64), comment='用户名')
    status: Mapped[int] = mapped_column(insert_default=0, comment='登录状态(0失败 1成功)')
    ip: Mapped[str] = mapped_column(sa.String(64), comment='登录IP地址')
    country: Mapped[str | None] = mapped_column(sa.String(64), comment='国家')
    region: Mapped[str | None] = mapped_column(sa.String(64), comment='地区')
    city: Mapped[str | None] = mapped_column(sa.String(64), comment='城市')
    user_agent: Mapped[str | None] = mapped_column(sa.String(512), comment='请求头')
    os: Mapped[str | None] = mapped_column(sa.String(64), comment='操作系统')
    browser: Mapped[str | None] = mapped_column(sa.String(64), comment='浏览器')
    device: Mapped[str | None] = mapped_column(sa.String(64), comment='设备')
    msg: Mapped[str] = mapped_column(UniversalText, comment='提示消息')
    login_time: Mapped[datetime] = mapped_column(TimeZone, comment='登录时间')
    created_time: Mapped[datetime] = mapped_column(
        TimeZone,
        init=False,
        default_factory=timezone.now,
        comment='创建时间',
    )
