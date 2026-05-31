import sqlalchemy as sa

from sqlalchemy.orm import Mapped, mapped_column

from backend.common.model import Base, id_key


class UserSocial(Base):
    """用户社交表（OAuth2）"""

    __tablename__ = 'sys_user_social'
    __table_args__ = (
        sa.UniqueConstraint('user_id', 'source', 'deleted', name='uk_sys_user_social_user_id_source_deleted'),
        sa.UniqueConstraint('sid', 'source', 'deleted', name='uk_sys_user_social_sid_source_deleted'),
        {'comment': '用户社交表（OAuth2）'},
    )

    id: Mapped[id_key] = mapped_column(init=False)
    sid: Mapped[str] = mapped_column(sa.String(256), comment='第三方用户 ID')
    source: Mapped[str] = mapped_column(sa.String(32), comment='第三方用户来源')

    # 逻辑外键
    user_id: Mapped[int] = mapped_column(sa.BigInteger, comment='用户关联ID')
