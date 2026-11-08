from backend.common.enums import StrEnum


class GenMySQLColumnType(StrEnum):
    """代码生成模型列类型（MySQL）"""

    # Python 类型映射
    BIGINT = 'int'
    BigInteger = 'int'  # BIGINT
    BINARY = 'bytes'
    BLOB = 'bytes'
    BOOLEAN = 'bool'  # BOOL
    Boolean = 'bool'  # BOOL
    CHAR = 'str'
    CLOB = 'str'
    DATE = 'date'
    Date = 'date'  # DATE
    DATETIME = 'datetime'
    DateTime = 'datetime'  # DATETIME
    DECIMAL = 'Decimal'
    DOUBLE = 'float'
    DOUBLE_PRECISION = 'float'
    Double = 'float'  # DOUBLE
    Enum = 'Enum'  # Enum()
    FLOAT = 'float'
    Float = 'float'  # FLOAT
    INT = 'int'  # INTEGER
    INTEGER = 'int'
    Integer = 'int'  # INTEGER
    Interval = 'timedelta'  # INTERVAL
    JSON = 'dict'
    LargeBinary = 'bytes'  # BLOB
    NCHAR = 'str'
    NUMERIC = 'Decimal'
    NVARCHAR = 'str'  # String
    Numeric = 'Decimal'  # NUMERIC
    PickleType = 'bytes'  # BLOB
    REAL = 'float'
    SMALLINT = 'int'
    SmallInteger = 'int'  # SMALLINT
    String = 'str'  # String
    TEXT = 'str'
    TIME = 'time'
    TIMESTAMP = 'datetime'
    Text = 'str'  # TEXT
    Time = 'time'  # TIME
    UUID = 'str | UUID'
    Unicode = 'str'  # String
    UnicodeText = 'str'  # TEXT
    Uuid = 'str'  # CHAR(32)
    VARBINARY = 'bytes'
    VARCHAR = 'str'  # String

    # sa.dialects.mysql 导入
    BIT = 'bool'
    ENUM = 'Enum'
    LONGBLOB = 'bytes'
    LONGTEXT = 'str'
    MEDIUMBLOB = 'bytes'
    MEDIUMINT = 'int'
    MEDIUMTEXT = 'str'
    SET = 'list[str]'
    TINYBLOB = 'bytes'
    TINYINT = 'int'
    TINYTEXT = 'str'
    YEAR = 'int'


class GenPostgreSQLColumnType(StrEnum):
    """代码生成模型列类型（PostgreSQL）"""

    # Python 类型映射
    BIGINT = 'int'
    BigInteger = 'int'  # BIGINT
    BINARY = 'bytes'
    BLOB = 'bytes'
    BOOLEAN = 'bool'
    Boolean = 'bool'  # BOOLEAN
    CHAR = 'str'
    CHARACTER = 'str'  # CHAR
    CHARACTER_VARYING = 'str'  # CHARACTER VARYING
    CLOB = 'str'
    DATE = 'date'
    Date = 'date'  # DATE
    DATETIME = 'datetime'
    DateTime = 'datetime'  # TIMESTAMP WITHOUT TIME ZONE
    DECIMAL = 'Decimal'
    DOUBLE = 'float'
    DOUBLE_PRECISION = 'float'  # DOUBLE PRECISION
    Double = 'float'  # DOUBLE PRECISION
    Enum = 'Enum'  # Enum(name='enum')
    FLOAT = 'float'
    Float = 'float'  # FLOAT
    INT = 'int'  # INTEGER
    INTEGER = 'int'
    Integer = 'int'  # INTEGER
    Interval = 'timedelta'  # INTERVAL
    JSON = 'dict'
    LargeBinary = 'bytes'  # BYTEA
    NCHAR = 'str'
    NUMERIC = 'Decimal'
    NVARCHAR = 'str'  # String
    Numeric = 'Decimal'  # NUMERIC
    PickleType = 'bytes'  # BYTEA
    REAL = 'float'
    SMALLINT = 'int'
    SmallInteger = 'int'  # SMALLINT
    String = 'str'  # String
    TEXT = 'str'
    TIME = 'time'  # TIME WITHOUT TIME ZONE
    TIME_WITHOUT_TIME_ZONE = 'time'  # TIME WITHOUT TIME ZONE
    TIME_WITH_TIME_ZONE = 'time'  # TIME WITH TIME ZONE
    TIMESTAMP = 'datetime'  # TIMESTAMP WITHOUT TIME ZONE
    TIMESTAMP_WITHOUT_TIME_ZONE = 'datetime'  # TIMESTAMP WITHOUT TIME ZONE
    TIMESTAMP_WITH_TIME_ZONE = 'datetime'  # TIMESTAMP WITH TIME ZONE
    Text = 'str'  # TEXT
    Time = 'time'  # TIME WITHOUT TIME ZONE
    UUID = 'str | UUID'
    Unicode = 'str'  # String
    UnicodeText = 'str'  # TEXT
    Uuid = 'str'
    VARBINARY = 'bytes'
    VARCHAR = 'str'  # String

    # sa.dialects.postgresql 导入
    ARRAY = 'list'
    BIT = 'bool'
    BYTEA = 'bytes'
    CIDR = 'str'
    CITEXT = 'str'
    DATEMULTIRANGE = 'list[date]'
    DATERANGE = 'tuple[date, date]'
    DOMAIN = 'str'
    ENUM = 'Enum'
    HSTORE = 'dict'
    INET = 'str'
    INT4MULTIRANGE = 'list[int]'
    INT4RANGE = 'tuple[int, int]'
    INT8MULTIRANGE = 'list[int]'
    INT8RANGE = 'tuple[int, int]'
    INTERVAL = 'timedelta'
    JSONB = 'dict'
    JSONPATH = 'str'
    MACADDR = 'str'
    MACADDR8 = 'str'
    MONEY = 'Decimal'
    NUMMULTIRANGE = 'list[Decimal]'
    NUMRANGE = 'tuple[Decimal, Decimal]'
    OID = 'int'
    REGCLASS = 'str'
    REGCONFIG = 'str'
    TSMULTIRANGE = 'list[datetime]'
    TSQUERY = 'str'
    TSRANGE = 'tuple[datetime, datetime]'
    TSTZMULTIRANGE = 'list[datetime]'
    TSTZRANGE = 'tuple[datetime, datetime]'
    TSVECTOR = 'str'


class MergeMode(StrEnum):
    """生成代码合并模式"""

    OVERWRITE = 'overwrite'  # 覆盖写入
    ROUTER = 'router'  # 路由文件追加
    MODEL_INIT = 'model_init'  # 模型包初始化文件追加
    SQL = 'sql'  # SQL 脚本追加
    INIT = 'init'  # 包初始化文件保留原有内容
