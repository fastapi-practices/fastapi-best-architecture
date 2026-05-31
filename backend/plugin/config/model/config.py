import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, UniversalText, id_key


class Config(Base):
    """参数配置表"""

    __tablename__ = 'sys_config'
    __table_args__ = (
        sa.UniqueConstraint('key', 'deleted', name='uk_sys_config_key_deleted'),
        {'comment': '参数配置表'},
    )

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(sa.String(32), comment='名称')
    type: Mapped[str | None] = mapped_column(sa.String(32), server_default=None, comment='类型')
    key: Mapped[str] = mapped_column(sa.String(64), comment='键名')
    value: Mapped[str] = mapped_column(UniversalText, comment='键值')
    is_frontend: Mapped[bool] = mapped_column(default=False, comment='是否前端')
    remark: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='备注')
