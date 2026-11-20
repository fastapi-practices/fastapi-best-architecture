import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key
from backend.common.tenant import TenantMixin


class Notice(Base, TenantMixin):
    """系统通知公告表"""

    __tablename__ = 'sys_notice'

    id: Mapped[id_key] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(sa.String(64), comment='标题')
    type: Mapped[int] = mapped_column(comment='类型（0：通知、1：公告）')
    status: Mapped[int] = mapped_column(comment='状态（0：隐藏、1：显示）')
    content: Mapped[str] = mapped_column(sa.Text, comment='内容')
