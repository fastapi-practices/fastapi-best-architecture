import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, UniversalText, id_key


class Role(Base):
    """角色表"""

    __tablename__ = 'sys_role'
    __table_args__ = (
        sa.UniqueConstraint('name', 'deleted', name='uk_sys_role_name_deleted'),
        {'comment': '角色表'},
    )

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(sa.String(32), comment='角色名称')
    status: Mapped[int] = mapped_column(default=1, comment='角色状态（0停用 1正常）')
    is_filter_scopes: Mapped[bool] = mapped_column(default=True, comment='过滤数据权限(0否 1是)')
    remark: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='备注')
