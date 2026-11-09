import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class Menu(Base):
    """菜单表"""

    __tablename__ = 'sys_menu'

    id: Mapped[id_key] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(sa.String(64), comment='菜单标题')
    name: Mapped[str] = mapped_column(sa.String(64), comment='菜单名称')
    path: Mapped[str | None] = mapped_column(sa.String(200), comment='路由地址')
    sort: Mapped[int] = mapped_column(default=0, comment='排序')
    icon: Mapped[str | None] = mapped_column(sa.String(128), default=None, comment='菜单图标')
    type: Mapped[int] = mapped_column(default=0, comment='菜单类型（0目录 1菜单 2按钮 3内嵌 4外链）')
    component: Mapped[str | None] = mapped_column(sa.String(256), default=None, comment='组件路径')
    perms: Mapped[str | None] = mapped_column(sa.String(128), default=None, comment='权限标识')
    status: Mapped[int] = mapped_column(default=1, comment='菜单状态（0停用 1正常）')
    display: Mapped[int] = mapped_column(default=1, comment='是否显示（0否 1是）')
    cache: Mapped[int] = mapped_column(default=1, comment='是否缓存（0否 1是）')
    link: Mapped[str | None] = mapped_column(sa.Text, default=None, comment='外链地址')
    remark: Mapped[str | None] = mapped_column(sa.Text, default=None, comment='备注')

    # 父级菜单
    parent_id: Mapped[int | None] = mapped_column(sa.BigInteger, default=None, index=True, comment='父菜单ID')
