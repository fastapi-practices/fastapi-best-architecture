import re

from collections.abc import Sequence

from backend.core.conf import settings

REDACTED = '[REDACTED]'


class Redaction:
    """
    敏感信息脱敏策略

    核心只提供默认规则，业务插件通过 setup hook 注册自己的路径与字段规则
    """

    def __init__(self) -> None:
        self._body_paths: list[re.Pattern[str]] = []
        self._query_paths: list[re.Pattern[str]] = []
        self._opaque_fields: set[str] = set()

    def register(
        self,
        *,
        body_paths: Sequence[str] = (),
        query_paths: Sequence[str] = (),
        opaque_fields: Sequence[str] = (),
    ) -> None:
        """
        注册脱敏规则

        :param body_paths: 请求路径正则，命中后操作日志整体不记录请求参数
        :param query_paths: 请求路径正则，命中后访问日志不记录查询字符串
        :param opaque_fields: 字段名，参数校验错误中出现该字段时整体隐藏回显的输入
        :return:
        """
        self._body_paths.extend(re.compile(pattern) for pattern in body_paths)
        self._query_paths.extend(re.compile(pattern) for pattern in query_paths)
        self._opaque_fields.update(field.lower() for field in opaque_fields)

    def is_body_redacted(self, path: str) -> bool:
        """
        判断请求路径的请求参数是否需要整体脱敏

        :param path: 请求路径
        :return:
        """
        return any(pattern.search(path) for pattern in self._body_paths)

    def is_query_redacted(self, path: str) -> bool:
        """
        判断请求路径的查询字符串是否需要整体脱敏

        :param path: 请求路径
        :return:
        """
        return any(pattern.search(path) for pattern in self._query_paths)

    def redact_error_input(self, *, error_type: str, loc: Sequence[str | int], value: object) -> object:
        """
        脱敏参数校验错误回显的输入

        :param error_type: 校验错误类型
        :param loc: 校验错误位置
        :param value: 校验错误回显的输入
        :return:
        """
        sensitive_fields = {key.lower() for key in settings.OPERA_LOG_REDACT_KEYS}
        if error_type == 'json_invalid' or any(
            str(part).lower() in sensitive_fields | self._opaque_fields for part in loc
        ):
            return REDACTED
        if isinstance(value, dict):
            if any(str(key).lower() in self._opaque_fields for key in value):
                return REDACTED
            return {key: REDACTED if str(key).lower() in sensitive_fields else item for key, item in value.items()}
        return value


redaction: Redaction = Redaction()
