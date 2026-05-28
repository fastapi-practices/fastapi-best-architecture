from typing import Any

from prometheus_client import Gauge
from sqlalchemy.pool import QueuePool

from backend.core.conf import settings

_PROMETHEUS_SQLALCHEMY_POOL_CONNECTIONS_GAUGE = Gauge(
    name='fba_sqlalchemy_pool_connections',
    documentation='SQLAlchemy 连接池状态',
    labelnames=['app_name', 'state'],
)


def observe_sqlalchemy_pool_connections(*_event_args: Any, pool: QueuePool) -> None:
    """监听 SQLAlchemy 连接池状态"""
    total_size = pool.size()
    checked_out_size = pool.checkedout()
    overflow_size = pool.overflow()
    idle_size = max(total_size + overflow_size - checked_out_size, 0)

    _PROMETHEUS_SQLALCHEMY_POOL_CONNECTIONS_GAUGE.labels(
        app_name=settings.GRAFANA_PROMETHEUS_APP_NAME, state='size'
    ).set(total_size)
    _PROMETHEUS_SQLALCHEMY_POOL_CONNECTIONS_GAUGE.labels(
        app_name=settings.GRAFANA_PROMETHEUS_APP_NAME, state='checked_out'
    ).set(checked_out_size)
    _PROMETHEUS_SQLALCHEMY_POOL_CONNECTIONS_GAUGE.labels(
        app_name=settings.GRAFANA_PROMETHEUS_APP_NAME, state='idle'
    ).set(idle_size)
    _PROMETHEUS_SQLALCHEMY_POOL_CONNECTIONS_GAUGE.labels(
        app_name=settings.GRAFANA_PROMETHEUS_APP_NAME, state='overflow'
    ).set(overflow_size)
