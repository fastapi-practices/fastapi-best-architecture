import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, UniversalText, id_key


class GenBusiness(Base):
    """代码生成业务表"""

    __tablename__ = 'gen_business'
    __table_args__ = (
        sa.UniqueConstraint('table_name', 'deleted', name='uk_gen_business_table_name_deleted'),
        {'comment': '代码生成业务表'},
    )

    id: Mapped[id_key] = mapped_column(init=False)
    app_name: Mapped[str] = mapped_column(sa.String(64), comment='应用名称')
    table_name: Mapped[str] = mapped_column(sa.String(256), comment='表名称')
    doc_comment: Mapped[str] = mapped_column(sa.String(256), comment='文档注释')
    table_comment: Mapped[str | None] = mapped_column(sa.String(256), default=None, comment='表描述')
    class_name: Mapped[str | None] = mapped_column(sa.String(64), default=None, comment='基础类名')
    schema_name: Mapped[str | None] = mapped_column(sa.String(64), default=None, comment='Schema 名称')
    filename: Mapped[str | None] = mapped_column(sa.String(64), default=None, comment='基础文件名')
    datetime_mixin: Mapped[bool] = mapped_column(default=True, comment='是否包含时间 Mixin 列')
    api_version: Mapped[str] = mapped_column(sa.String(32), default='v1', comment='API 版本')
    tag: Mapped[str | None] = mapped_column(sa.String(64), default=None, comment='API 标签')
    gen_path: Mapped[str | None] = mapped_column(sa.String(256), default=None, comment='生成路径')
    remark: Mapped[str | None] = mapped_column(UniversalText, default=None, comment='备注')
