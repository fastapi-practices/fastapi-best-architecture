from backend.common.context import ctx
from backend.core.conf import settings


def get_request_trace_id() -> str:
    """从上下文中获取追踪 ID"""
    if ctx.exists():
        return ctx.get(settings.TRACE_ID_REQUEST_HEADER_KEY, settings.TRACE_ID_LOG_DEFAULT_VALUE)
    return settings.TRACE_ID_LOG_DEFAULT_VALUE
