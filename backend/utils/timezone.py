import zoneinfo

from datetime import datetime
from datetime import timezone as datetime_timezone
from typing import Final

from backend.core.conf import settings

# 基于 wikipedia：https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List
_UTC_IDENTIFIERS: Final = frozenset({
    'Etc/UCT',
    'Etc/Universal',
    'Etc/UTC',
    'Etc/Zulu',
    'UCT',
    'Universal',
    'UTC',
    'Zulu',
})


class TimeZone:
    def __init__(self) -> None:
        """初始化时区转换器"""
        if settings.DATETIME_TIMEZONE in _UTC_IDENTIFIERS:
            self.tz_info = datetime_timezone.utc
        else:
            self.tz_info = zoneinfo.ZoneInfo(settings.DATETIME_TIMEZONE)

    def now(self) -> datetime:
        """获取当前时区时间"""
        return datetime.now(self.tz_info)

    def from_datetime(self, t: datetime) -> datetime:
        """
        将 datetime 对象转换为当前时区时间

        :param t: 需要转换的 datetime 对象
        :return:
        """
        return t.astimezone(self.tz_info)

    def from_str(self, t_str: str, format_str: str = settings.DATETIME_FORMAT) -> datetime:
        """
        将时间字符串转换为当前时区的 datetime 对象

        :param t_str: 时间字符串
        :param format_str: 时间格式字符串，默认为 settings.DATETIME_FORMAT
        :return:
        """
        return datetime.strptime(t_str, format_str).replace(tzinfo=self.tz_info)

    @staticmethod
    def to_str(t: datetime, format_str: str = settings.DATETIME_FORMAT) -> str:
        """
        将 datetime 对象转换为指定格式的时间字符串

        :param t: datetime 对象
        :param format_str: 时间格式字符串，默认为 settings.DATETIME_FORMAT
        :return:
        """
        return t.strftime(format_str)

    @staticmethod
    def to_utc(t: datetime | int) -> datetime:
        """
        将 datetime 对象或时间戳转换为 UTC 时区时间

        :param t: 需要转换的 datetime 对象或时间戳
        :return:
        """
        if isinstance(t, datetime):
            return t.astimezone(datetime_timezone.utc)
        return datetime.fromtimestamp(t, tz=datetime_timezone.utc)


timezone: TimeZone = TimeZone()
