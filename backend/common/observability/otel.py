from fastapi import FastAPI
from opentelemetry import _logs, metrics, trace
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.asyncio import AsyncioInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs._internal.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from redis.observability.config import OTelConfig
from redis.observability.providers import get_observability_instance

from backend.common.log import log, request_id_filter
from backend.core.conf import settings
from backend.database.db import async_engine
from backend.database.redis import redis_client


def init_resource(service_name: str) -> Resource:
    """
    初始化资源

    :param service_name: 服务名称
    :return:
    """
    from backend import __version__

    return Resource(
        attributes={
            'service.name': service_name,
            'service.version': __version__,
            'deployment.environment': settings.ENVIRONMENT,
        },
    )


def init_tracer(resource: Resource) -> None:
    """
    初始化追踪器

    :param resource: 遥测资源
    :return:
    """
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=settings.GRAFANA_OTLP_GRPC_ENDPOINT, insecure=True)
    processor = BatchSpanProcessor(span_exporter=exporter)

    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)


def init_metrics(resource: Resource) -> None:
    """
    初始化指标

    :param resource: 遥测资源
    :return:
    """
    exporter = OTLPMetricExporter(endpoint=settings.GRAFANA_OTLP_GRPC_ENDPOINT, insecure=True)
    reader = PeriodicExportingMetricReader(exporter=exporter)
    provider = MeterProvider(resource=resource, metric_readers=[reader])

    metrics.set_meter_provider(provider)


def init_logging(resource: Resource) -> None:
    """
    初始化日志

    :param resource: 遥测资源
    :return:
    """
    provider = LoggerProvider(resource=resource)
    exporter = OTLPLogExporter(endpoint=settings.GRAFANA_OTLP_GRPC_ENDPOINT, insecure=True)
    processor = BatchLogRecordProcessor(exporter=exporter)

    provider.add_log_record_processor(processor)
    _logs.set_logger_provider(provider)

    otel_logging_handler = LoggingHandler(logger_provider=provider)
    log.add(
        otel_logging_handler,
        level=settings.LOG_STD_LEVEL,
        format=settings.LOG_FORMAT,
        filter=lambda record: request_id_filter(record),
    )


def init_otel(app: FastAPI) -> None:
    """
    初始化 OpenTelemetry

    :param app: FastAPI 应用实例
    :return:
    """
    resource = init_resource(settings.GRAFANA_PROMETHEUS_APP_NAME)
    init_tracer(resource)
    init_metrics(resource)
    init_logging(resource)

    # Redis 原生指标
    redis_otel = get_observability_instance()
    redis_otel.init(OTelConfig())

    AsyncioInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()
    LoggingInstrumentor().instrument(set_logging_format=True)
    RedisInstrumentor.instrument_client(client=redis_client)  # type: ignore
    SQLAlchemyInstrumentor().instrument(engine=async_engine.sync_engine)
    FastAPIInstrumentor.instrument_app(app)
