import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class Dept(Base):
    """部门表"""

    __tablename__ = 'sys_dept'
    __table_args__ = (
        sa.UniqueConstraint('name', 'deleted', name='uk_sys_dept_name_deleted'),
        {'comment': '部门表'},
    )

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(sa.String(64), comment='部门名称')
    sort: Mapped[int] = mapped_column(default=0, comment='排序')
    leader: Mapped[str | None] = mapped_column(sa.String(32), default=None, comment='负责人')
    phone: Mapped[str | None] = mapped_column(sa.String(11), default=None, comment='手机')
    email: Mapped[str | None] = mapped_column(sa.String(64), default=None, comment='邮箱')
    status: Mapped[int] = mapped_column(default=1, comment='部门状态(0停用 1正常)')

    # 父级部门
    parent_id: Mapped[int | None] = mapped_column(sa.BigInteger, default=None, index=True, comment='父部门ID')
