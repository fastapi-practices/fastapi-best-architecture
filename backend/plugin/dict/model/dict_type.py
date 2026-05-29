import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, UniversalText, id_key


class DictType(Base):
    """字典类型表"""

    __tablename__ = 'sys_dict_type'
    __table_args__ = (
        sa.UniqueConstraint('code', 'deleted', name='uk_sys_dict_type_code_deleted'),
        {'comment': '字典类型表'},
    )

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(sa.String(32), comment='字典类型名称')
    code: Mapped[str] = mapped_column(sa.String(32), comment='字典类型编码')
    remark: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='备注')
