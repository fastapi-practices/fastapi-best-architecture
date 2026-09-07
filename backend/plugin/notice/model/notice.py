import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, TenantMixin, UniversalText, id_key


class Notice(Base, TenantMixin):
    """系统通知公告表"""

    __tablename__ = 'sys_notice'

    id: Mapped[id_key] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(sa.String(64), comment='标题')
    type: Mapped[int] = mapped_column(comment='类型（0：通知、1：公告）')
    status: Mapped[int] = mapped_column(comment='状态（0：隐藏、1：显示）')
    content: Mapped[str] = mapped_column(UniversalText, comment='内容')
