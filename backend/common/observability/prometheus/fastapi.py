from prometheus_client import Counter, Gauge, Histogram

from backend.core.conf import settings

_PROMETHEUS_FASTAPI_REQUEST_IN_PROGRESS_GAUGE = Gauge(
    name='fba_request_in_progress',
    documentation='按方法和路径统计当前正在处理的 FastAPI 请求数',
    labelnames=['app_name', 'method', 'path'],
)

_PROMETHEUS_FASTAPI_REQUEST_COUNTER = Counter(
    name='fba_request_total',
    documentation='按方法和路径统计 FastAPI 请求总数',
    labelnames=['app_name', 'method', 'path'],
)

_PROMETHEUS_FASTAPI_REQUEST_COST_TIME_HISTOGRAM = Histogram(
    name='fba_request_cost_time',
    documentation='按方法和路径统计 FastAPI 请求耗时直方图（ms）',
    labelnames=['app_name', 'method', 'path'],
)

_PROMETHEUS_FASTAPI_EXCEPTION_COUNTER = Counter(
    name='fba_exception_total',
    documentation='按方法、路径和异常类型统计 FastAPI 异常总数',
    labelnames=['app_name', 'method', 'path', 'exception_type'],
)

_PROMETHEUS_FASTAPI_RESPONSE_COUNTER = Counter(
    name='fba_response_total',
    documentation='按方法、路径和状态码统计 FastAPI 响应总数',
    labelnames=['app_name', 'method', 'path', 'status_code'],
)


def inc_fastapi_request_in_progress(*, method: str, path: str) -> None:
    """增加当前正在处理的 FastAPI 请求数"""
    _PROMETHEUS_FASTAPI_REQUEST_IN_PROGRESS_GAUGE.labels(
        app_name=settings.GRAFANA_PROMETHEUS_APP_NAME, method=method, path=path
    ).inc()


def dec_fastapi_request_in_progress(*, method: str, path: str) -> None:
    """减少当前正在处理的 FastAPI 请求数"""
    _PROMETHEUS_FASTAPI_REQUEST_IN_PROGRESS_GAUGE.labels(
        app_name=settings.GRAFANA_PROMETHEUS_APP_NAME, method=method, path=path
    ).dec()


def inc_fastapi_request(*, method: str, path: str) -> None:
    """记录 FastAPI 请求总数"""
    _PROMETHEUS_FASTAPI_REQUEST_COUNTER.labels(
        app_name=settings.GRAFANA_PROMETHEUS_APP_NAME, method=method, path=path
    ).inc()


def observe_fastapi_request_cost_time(*, method: str, path: str, elapsed: float, trace_id: str) -> None:
    """记录 FastAPI 请求耗时"""
    _PROMETHEUS_FASTAPI_REQUEST_COST_TIME_HISTOGRAM.labels(
        app_name=settings.GRAFANA_PROMETHEUS_APP_NAME, method=method, path=path
    ).observe(amount=elapsed, exemplar={settings.GRAFANA_PROMETHEUS_EXEMPLAR_TRACE_ID_KEY: trace_id})


def inc_fastapi_exception(*, method: str, path: str, exception_type: str) -> None:
    """记录 FastAPI 异常总数"""
    _PROMETHEUS_FASTAPI_EXCEPTION_COUNTER.labels(
        app_name=settings.GRAFANA_PROMETHEUS_APP_NAME, method=method, path=path, exception_type=exception_type
    ).inc()


def inc_fastapi_response(*, method: str, path: str, status_code: int | str) -> None:
    """记录 FastAPI 响应总数"""
    _PROMETHEUS_FASTAPI_RESPONSE_COUNTER.labels(
        app_name=settings.GRAFANA_PROMETHEUS_APP_NAME, method=method, path=path, status_code=status_code
    ).inc()
