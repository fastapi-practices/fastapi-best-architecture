import functools

from collections.abc import Callable, Sequence
from typing import Any, ParamSpec, TypeVar

from msgspec import json

from backend.common.cache.local import local_cache_manager
from backend.common.cache.pubsub import cache_pubsub_manager
from backend.common.context import ctx
from backend.common.exception import errors
from backend.common.log import log
from backend.core.conf import settings
from backend.database.redis import redis_client
from backend.utils.serializers import select_columns_serialize, select_list_serialize

P = ParamSpec('P')
T = TypeVar('T')


def _build_cache_key(
    name: str,
    key: str | None,
    key_builder: Callable[..., str] | None,
    *args: Any,
    **kwargs: Any,
) -> str:
    """构建缓存 Key"""
    if key:
        if '.' in key:
            param, field = key.split('.', 1)
            value = kwargs.get(param)
            if value is None:
                raise errors.ServerError(msg=f'缓存键构建失败，参数 "{param}" 不存在或值为空')

            if isinstance(value, list):
                raise errors.ServerError(msg='缓存键构建失败：不支持从列表中提取字段，请使用 key_builder 处理列表参数')

            if hasattr(value, field):
                value = getattr(value, field)
            elif isinstance(value, dict) and field in value:
                value = value[field]
            else:
                raise errors.ServerError(msg=f'缓存键构建失败，对象中不存在字段 "{field}"')
        else:
            value = kwargs.get(key)
            if value is None:
                raise errors.ServerError(msg=f'缓存键构建失败，参数 "{key}" 不存在或值为空')

        return f'{name}:{value}'

    if key_builder:
        return f'{name}:{key_builder(*args, **kwargs)}'

    return name


def _serialize_result(result: Any) -> bytes:
    """
    序列化缓存结果

    :param result: 需要进行序列化的结果
    :return:
    """
    # SQLAlchemy 查询表
    if hasattr(result, '__table__'):
        return json.encode(select_columns_serialize(result))

    # SQLAlchemy 查询列表
    if (
        isinstance(result, Sequence)
        and not isinstance(result, (str, bytes))
        and len(result) > 0
        and hasattr(result[0], '__table__')
    ):
        return json.encode(select_list_serialize(result))

    # 基本类型
    return json.encode(result)


def _deserialize_result(value: bytes) -> Any:
    """
    反序列化缓存结果

    :param value: 缓存结果
    :return:
    """
    try:
        return json.decode(value)
    except Exception:
        return value


def user_key_builder() -> str:
    """基于当前用户 ID 生成缓存 Key"""
    user_id = ctx.user_id
    if user_id is None:
        raise errors.ServerError(msg='用户缓存键构建失败')
    return str(user_id)


def cached(  # noqa: C901
    name: str,
    *,
    key: str | None = None,
    key_builder: Callable[..., str] | None = None,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    缓存装饰器

    :param name: 缓存名称（通常为缓存 Key 前缀）
    :param key: 从方法参数中获取指定参数名的值作为缓存 Key，与 key_builder 互斥
    :param key_builder: 自定义 Key 生成函数，与 key 互斥
    :return:
    """
    if key is not None and key_builder is not None:
        raise errors.ServerError(msg='缓存 key 和 key_builder 不能同时使用')

    def decorator(func: Callable[P, T]) -> Callable[P, T]:  # noqa: C901
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            cache_key = _build_cache_key(name, key, key_builder, *args, **kwargs)

            # L1: 本地缓存
            if settings.CACHE_LOCAL_ENABLED:
                local_value = local_cache_manager.get(cache_key)
                if local_value is not None:
                    return local_value

            # L2: Redis 缓存
            try:
                redis_value = await redis_client.get(cache_key)
                if redis_value is not None:
                    result = _deserialize_result(redis_value)
                    # 回填 L1
                    if settings.CACHE_LOCAL_ENABLED:
                        local_cache_manager.set(cache_key, result)
                    return result
            except Exception as e:
                log.warning(f'[Cache] GET error: {e}')

            # 缓存未命中
            result = await func(*args, **kwargs)

            if result is not None:
                try:
                    serialized_result = _serialize_result(result)
                    deserialized_result = _deserialize_result(serialized_result)

                    # 回填 L1
                    if settings.CACHE_LOCAL_ENABLED:
                        local_cache_manager.set(cache_key, deserialized_result)

                    # 回填 L2
                    if settings.CACHE_REDIS_TTL:
                        await redis_client.set(cache_key, serialized_result, ex=settings.CACHE_REDIS_TTL)
                    else:
                        await redis_client.set(cache_key, serialized_result)
                except Exception as e:
                    log.warning(f'[Cache] SET error: {e}')

            return result

        return wrapper

    return decorator


def cache_invalidate(  # noqa: C901
    name: str,
    *,
    key: str | None = None,
    key_builder: Callable[..., str] | None = None,
    atomic: bool = True,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """
    缓存失效装饰器

    :param name: 缓存名称（通常为缓存 Key 前缀）
    :param key: 从方法参数中获取指定参数名的值作为缓存 Key，与 key_builder 互斥
    :param key_builder: 自定义 Key 生成函数，与 key 互斥
    :param atomic: 是否保证缓存原子性
    :return:
    """
    if key is not None and key_builder is not None:
        raise errors.ServerError(msg='缓存 key 和 key_builder 不能同时使用')

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            result = await func(*args, **kwargs)

            # 尝试失效缓存
            invalidate_success = False
            invalidate_error = None

            try:
                invalidate_key = _build_cache_key(name, key, key_builder, *args, **kwargs)

                # L1 缓存失效
                if settings.CACHE_LOCAL_ENABLED:
                    if invalidate_key == name:
                        local_cache_manager.delete_prefix(invalidate_key)
                    else:
                        local_cache_manager.delete(invalidate_key)

                # 广播失效消息（通知其他节点清除本地缓存）
                if settings.CACHE_LOCAL_ENABLED:
                    if invalidate_key == name:
                        await cache_pubsub_manager.publish_invalidation(invalidate_key, is_delete_prefix=True)
                    else:
                        await cache_pubsub_manager.publish_invalidation(invalidate_key, is_delete_prefix=False)

                # L2 缓存失效
                if invalidate_key == name:
                    await redis_client.delete_prefix(invalidate_key)
                else:
                    await redis_client.delete(invalidate_key)

            except Exception as e:
                log.error(f'[Cache] INVALIDATE error: {e}')
                invalidate_error = e
            else:
                invalidate_success = True

            # 原子性检查
            if atomic and not invalidate_success:
                raise errors.ServerError(msg='缓存失效失败，数据可能不一致', data=invalidate_error)

            return result

        return wrapper

    return decorator
