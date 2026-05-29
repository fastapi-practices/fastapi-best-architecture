import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class DataRule(Base):
    """数据规则表"""

    __tablename__ = 'sys_data_rule'
    __table_args__ = (
        sa.UniqueConstraint('name', 'deleted', name='uk_sys_data_rule_name_deleted'),
        {'comment': '数据规则表'},
    )

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(sa.String(512), comment='名称')
    model: Mapped[str] = mapped_column(sa.String(64), comment='模型名称')
    column: Mapped[str] = mapped_column(sa.String(32), comment='模型字段名')
    operator: Mapped[int] = mapped_column(comment='运算符（0：and、1：or）')
    expression: Mapped[int] = mapped_column(
        comment='表达式（0：==、1：!=、2：>、3：>=、4：<、5：<=、6：in、7：not_in）',
    )
    value: Mapped[str] = mapped_column(sa.String(256), comment='规则值')
