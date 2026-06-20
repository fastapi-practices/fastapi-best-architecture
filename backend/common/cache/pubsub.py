import asyncio
import json

from backend.common.cache.local import local_cache_manager
from backend.common.log import log
from backend.core.conf import settings
from backend.database.redis import RedisCli, redis_client


class CachePubSubManager:
    """缓存 Pub/Sub 管理器"""

    _pubsub_task: asyncio.Task | None = None

    @staticmethod
    async def publish_invalidation(key: str, *, is_delete_prefix: bool) -> None:
        """
        发布缓存失效通知

        :param key: 缓存键
        :param is_delete_prefix: 是否删除符合前缀的所有缓存
        :return:
        """
        try:
            message = json.dumps({'key': key, 'is_delete_prefix': is_delete_prefix})
            await redis_client.publish(settings.CACHE_PUBSUB_CHANNEL, message)
        except Exception as e:
            log.warning(f'[CachePubSub] 发布通知失败: {e}')

    @staticmethod
    async def subscribe_and_listen() -> None:  # noqa: C901
        """订阅并监听缓存失效通知"""
        reconnect_attempts = 0

        while reconnect_attempts < settings.CACHE_PUBSUB_MAX_RECONNECT_ATTEMPTS:
            pubsub_client: RedisCli | None = None
            pubsub = None

            try:
                # 使用独立连接
                pubsub_client = RedisCli(socket_timeout=None)
                pubsub = pubsub_client.pubsub()
                await pubsub.subscribe(settings.CACHE_PUBSUB_CHANNEL)

                # 发布订阅成功
                reconnect_attempts = 0

                async for message in pubsub.listen():
                    if message['type'] == 'message':
                        try:
                            data = json.loads(message['data'])
                            key = data['key']
                            if not data['is_delete_prefix']:
                                local_cache_manager.delete(key)
                            else:
                                local_cache_manager.delete_prefix(key)
                        except json.JSONDecodeError as e:
                            log.warning(f'[CachePubSub] 消息格式错误 {e}')
                        except Exception as e:
                            log.error(f'[CachePubSub] 处理通知失败: {e}')

            except asyncio.CancelledError:
                break
            except Exception as e:
                reconnect_attempts += 1
                log.error(
                    f'[CachePubSub] 订阅异常 ({reconnect_attempts}/{settings.CACHE_PUBSUB_MAX_RECONNECT_ATTEMPTS}): {e}'
                )

                if reconnect_attempts >= settings.CACHE_PUBSUB_MAX_RECONNECT_ATTEMPTS:
                    log.error('[CachePubSub] 达到最大重连次数，停止订阅')
                    break

                await asyncio.sleep(settings.CACHE_PUBSUB_RECONNECT_DELAY)
            finally:
                if pubsub_client:
                    try:
                        await pubsub_client.aclose()
                    except Exception:
                        pass
                if pubsub:
                    try:
                        await pubsub.aclose()
                    except Exception:
                        pass

    @classmethod
    def start_listener(cls) -> None:
        """启动缓存 Pub/Sub 监听器"""
        if not settings.CACHE_LOCAL_ENABLED:
            return

        if cls._pubsub_task is None or cls._pubsub_task.done():
            cls._pubsub_task = asyncio.create_task(cls.subscribe_and_listen())

    @classmethod
    async def stop_listener(cls) -> None:
        """停止缓存 Pub/Sub 监听器"""
        if cls._pubsub_task is None:
            return

        if not cls._pubsub_task.done():
            cls._pubsub_task.cancel()
            try:
                await cls._pubsub_task
            except asyncio.CancelledError:
                pass

        cls._pubsub_task = None


cache_pubsub_manager = CachePubSubManager()
