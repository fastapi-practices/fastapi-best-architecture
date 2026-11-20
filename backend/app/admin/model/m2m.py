import sqlalchemy as sa

from backend.common.model import MappedBase
from backend.common.tenant import tenant_columns

# 用户角色表
user_role = sa.Table(
    'sys_user_role',
    MappedBase.metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, unique=True, index=True, autoincrement=True, comment='主键ID'),
    sa.Column('user_id', sa.BigInteger, primary_key=True, comment='用户ID'),
    sa.Column('role_id', sa.BigInteger, primary_key=True, comment='角色ID'),
    *tenant_columns(),
)

# 角色菜单表
role_menu = sa.Table(
    'sys_role_menu',
    MappedBase.metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, unique=True, index=True, autoincrement=True, comment='主键ID'),
    sa.Column('role_id', sa.BigInteger, primary_key=True, comment='角色ID'),
    sa.Column('menu_id', sa.BigInteger, primary_key=True, comment='菜单ID'),
    *tenant_columns(),
)

# 角色数据范围表
role_data_scope = sa.Table(
    'sys_role_data_scope',
    MappedBase.metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, unique=True, index=True, autoincrement=True, comment='主键 ID'),
    sa.Column('role_id', sa.BigInteger, primary_key=True, comment='角色 ID'),
    sa.Column('data_scope_id', sa.BigInteger, primary_key=True, comment='数据范围 ID'),
    *tenant_columns(),
)

# 数据范围规则表
data_scope_rule = sa.Table(
    'sys_data_scope_rule',
    MappedBase.metadata,
    sa.Column('id', sa.BigInteger, primary_key=True, unique=True, index=True, autoincrement=True, comment='主键ID'),
    sa.Column('data_scope_id', sa.BigInteger, primary_key=True, comment='数据范围 ID'),
    sa.Column('data_rule_id', sa.BigInteger, primary_key=True, comment='数据规则 ID'),
)
