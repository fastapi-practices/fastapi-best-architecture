import os

from typing import Any

import celery
import celery_aio_pool

from celery.app.defaults import NAMESPACES
from celery.signals import worker_process_init
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from sqlalchemy import URL

from backend.app.task.tasks.beat import get_local_beat_schedule
from backend.common.enums import DataBaseType
from backend.common.observability.otel import init_resource, init_tracer
from backend.core.conf import settings
from backend.core.path_conf import BASE_PATH
from backend.database.db import get_database_url
from backend.database.redis import get_redis_url

_celery_otel_initialized = False


@worker_process_init.connect(weak=False)
def init_celery_tracing(*args, **kwargs) -> None:
    """初始化 Celery 追踪"""
    global _celery_otel_initialized

    if not settings.GRAFANA_METRICS_ENABLE or _celery_otel_initialized:
        return

    resource = init_resource(settings.GRAFANA_CELERY_OTEL_SERVICE_NAME)
    init_tracer(resource)
    CeleryInstrumentor().instrument()
    _celery_otel_initialized = True


def get_database_engine_options() -> dict[str, Any]:
    """获取数据库引擎参数，在 celery 默认值的基础上合并 echo 配置"""
    options = dict(NAMESPACES['database']['engine_options'].default or {})
    options['echo'] = settings.DATABASE_ECHO
    return options


def find_task_packages() -> list[str]:
    packages = []
    task_dir = BASE_PATH / 'app' / 'task' / 'tasks'
    for root, _dirs, files in os.walk(task_dir):
        if 'tasks.py' in files:
            package = root.replace(str(BASE_PATH.parent) + os.path.sep, '').replace(os.path.sep, '.')
            packages.append(package)
    return packages


def init_celery() -> celery.Celery:
    """初始化 Celery 应用"""

    # TODO: Update this work if celery version >= 6.0.0
    # https://github.com/fastapi-practices/fastapi-best-architecture/issues/321
    # https://github.com/celery/celery/issues/7874
    celery.app.trace.build_tracer = celery_aio_pool.build_async_tracer
    celery.app.trace.reset_worker_optimizations()

    # 使用 SQLA URL 构建，避免密码中的特殊字符破坏连接地址
    if settings.CELERY_BROKER == 'redis':
        broker_url = get_redis_url(database=settings.CELERY_BROKER_REDIS_DATABASE)
    else:
        broker_url = URL.create(
            drivername='amqp',
            username=settings.CELERY_RABBITMQ_USERNAME,
            password=settings.CELERY_RABBITMQ_PASSWORD,
            host=settings.CELERY_RABBITMQ_HOST,
            port=settings.CELERY_RABBITMQ_PORT,
            database=settings.CELERY_RABBITMQ_VHOST,
        ).render_as_string(hide_password=False)

    database_url = get_database_url()
    result_backend = database_url.set(
        drivername='mysql+pymysql' if DataBaseType.mysql == settings.DATABASE_TYPE else 'postgresql+psycopg'
    ).render_as_string(hide_password=False)
    result_backend = f'db+{result_backend}'

    # https://docs.celeryq.dev/en/stable/userguide/configuration.html
    app = celery.Celery(
        'fba_celery',
        broker_url=broker_url,
        broker_connection_retry_on_startup=True,
        result_backend=result_backend,
        result_extended=True,
        database_engine_options=get_database_engine_options(),
        # result_expires=0,
        # beat_sync_every=1,
        beat_schedule=get_local_beat_schedule(),
        beat_scheduler='backend.app.task.utils.schedulers:DatabaseScheduler',
        task_cls='backend.app.task.tasks.base:TaskBase',
        task_track_started=True,
        enable_utc=False,
        timezone=settings.DATETIME_TIMEZONE,
        worker_send_task_events=True,
        task_send_sent_event=True,
    )

    # 在 Celery 中设置此参数无效
    # 参数：https://github.com/celery/celery/issues/7270
    app.loader.override_backends = {'db': 'backend.app.task.database:DatabaseBackend'}

    # 自动发现任务
    packages = find_task_packages()
    app.autodiscover_tasks(packages)

    return app


# 创建 Celery 实例
celery_app: celery.Celery = init_celery()
