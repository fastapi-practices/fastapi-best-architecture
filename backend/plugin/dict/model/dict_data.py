import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, UniversalText, id_key


class DictData(Base):
    """字典数据表"""

    __tablename__ = 'sys_dict_data'
    __table_args__ = (
        sa.UniqueConstraint('type_code', 'label', 'deleted', name='uk_sys_dict_data_type_code_label_deleted'),
        {'comment': '字典数据表'},
    )

    id: Mapped[id_key] = mapped_column(init=False)
    type_code: Mapped[str] = mapped_column(sa.String(32), comment='对应的字典类型编码')
    label: Mapped[str] = mapped_column(sa.String(32), comment='字典标签')
    value: Mapped[str] = mapped_column(sa.String(32), comment='字典值')
    color: Mapped[str | None] = mapped_column(sa.String(32), default=None, comment='标签颜色')
    sort: Mapped[int] = mapped_column(default=0, comment='排序')
    status: Mapped[int] = mapped_column(default=1, comment='状态（0停用 1正常）')
    remark: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='备注')

    # 逻辑外键
    type_id: Mapped[int] = mapped_column(sa.BigInteger, default=0, comment='字典类型关联ID')
