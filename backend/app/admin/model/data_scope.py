import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class DataScope(Base):
    """数据范围表"""

    __tablename__ = 'sys_data_scope'
    __table_args__ = (
        sa.UniqueConstraint('name', 'deleted', name='uk_sys_data_scope_name_deleted'),
        {'comment': '数据范围表'},
    )

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(sa.String(64), comment='名称')
    status: Mapped[int] = mapped_column(default=1, comment='状态（0停用 1正常）')
