import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key
from backend.common.tenant import TenantMixin, tenant_unique_columns


class Role(Base, TenantMixin):
    """角色表"""

    __tablename__ = 'sys_role'

    __table_args__ = (
        sa.UniqueConstraint(*tenant_unique_columns('name'), name='uk_sys_role_name_deleted'),
        {'comment': '角色表'},
    )

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(sa.String(32), comment='角色名称')
    status: Mapped[int] = mapped_column(default=1, comment='角色状态（0停用 1正常）')
    is_filter_scopes: Mapped[bool] = mapped_column(default=True, comment='过滤数据权限(0否 1是)')
    remark: Mapped[str | None] = mapped_column(sa.Text, default=None, comment='备注')
