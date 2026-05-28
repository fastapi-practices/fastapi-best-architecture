import time

from asyncio import Queue

from prometheus_client import Counter, Gauge, Histogram

from backend.core.conf import settings

_PROMETHEUS_QUEUE_SIZE_GAUGE = Gauge(
    name='fba_queue_size',
    documentation='项目内部异步队列当前长度',
    labelnames=['app_name', 'queue_name'],
)

_PROMETHEUS_QUEUE_BATCH_DEQUEUE_COST_TIME_HISTOGRAM = Histogram(
    name='fba_queue_batch_dequeue_cost_time',
    documentation='项目内部异步队列批量消费耗时（ms）',
    labelnames=['app_name', 'queue_name'],
)

_PROMETHEUS_QUEUE_EXCEPTION_COUNTER = Counter(
    name='fba_queue_exception_total',
    documentation='项目内部异步队列异常总数',
    labelnames=['app_name', 'queue_name'],
)


def observe_queue_size(queue: Queue, *, queue_name: str) -> None:
    """记录队列当前长度"""
    _PROMETHEUS_QUEUE_SIZE_GAUGE.labels(app_name=settings.GRAFANA_PROMETHEUS_APP_NAME, queue_name=queue_name).set(
        queue.qsize()
    )


def observe_batch_dequeue_cost(start_time: float, *, queue_name: str) -> None:
    """记录批量消费耗时"""
    elapsed = round((time.perf_counter() - start_time) * 1000, 3)
    _PROMETHEUS_QUEUE_BATCH_DEQUEUE_COST_TIME_HISTOGRAM.labels(
        app_name=settings.GRAFANA_PROMETHEUS_APP_NAME, queue_name=queue_name
    ).observe(elapsed)


def inc_queue_exception(*, queue_name: str) -> None:
    """记录队列异常"""
    _PROMETHEUS_QUEUE_EXCEPTION_COUNTER.labels(
        app_name=settings.GRAFANA_PROMETHEUS_APP_NAME, queue_name=queue_name
    ).inc()
