import sys

from redis.asyncio import Redis
from redis.exceptions import AuthenticationError, TimeoutError

from backend.common.log import log
from backend.core.conf import settings


class RedisCli(Redis):
    """Redis 客户端"""

    def __init__(
        self,
        host: str = settings.REDIS_HOST,
        port: int = settings.REDIS_PORT,
        password: str = settings.REDIS_PASSWORD,
        db: int = settings.REDIS_DATABASE,
        socket_timeout: int | None = settings.REDIS_TIMEOUT,
        socket_connect_timeout: int = settings.REDIS_TIMEOUT,
        *,
        socket_keepalive: bool = True,
        health_check_interval: int = 30,
        decode_responses: bool = True,
    ) -> None:
        """
        初始化 Redis 客户端

        :param host: Redis 服务器的主机地址
        :param port: Redis 服务器的端口号
        :param password: Redis 认证密码
        :param db: 使用的 Redis 逻辑数据库索引
        :param socket_timeout: Socket 读写操作的超时时间
        :param socket_connect_timeout: 建立 TCP 连接时的超时时间
        :param socket_keepalive: 是否开启 TCP Keepalive 探测
        :param health_check_interval: 健康检查间隔时间（秒）
        :param decode_responses: 是否自动将 Redis 返回的字节流（bytes）解码为字符串（utf-8）
        """
        super().__init__(
            host=host,
            port=port,
            password=password,
            db=db,
            socket_timeout=socket_timeout,
            socket_connect_timeout=socket_connect_timeout,
            socket_keepalive=socket_keepalive,
            health_check_interval=health_check_interval,
            decode_responses=decode_responses,
        )

    async def init(self) -> None:
        """初始化 Redis 服务器"""
        try:
            await self.ping()
        except TimeoutError:
            log.error('Redis 服务器连接超时')
            sys.exit()
        except AuthenticationError:
            log.error('Redis 服务器连接认证失败')
            sys.exit()
        except Exception as e:
            log.error('Redis 服务器连接异常 {}', e)
            sys.exit()

    async def delete_prefix(self, prefix: str, exclude: str | list[str] | None = None, batch_size: int = 1000) -> None:
        """
        删除指定前缀的所有 key

        :param prefix: 要删除的键前缀
        :param exclude: 要排除的键或键列表
        :param batch_size: 批量删除的大小，避免一次性删除过多键导致 Redis 阻塞
        :return:
        """
        exclude_set = set(exclude) if isinstance(exclude, list) else {exclude} if isinstance(exclude, str) else set()
        batch_keys = []

        async for key in self.scan_iter(match=f'{prefix}*'):
            if key not in exclude_set:
                batch_keys.append(key)

                if len(batch_keys) >= batch_size:
                    await self.delete(*batch_keys)
                    batch_keys.clear()

        if batch_keys:
            await self.delete(*batch_keys)

    async def get_prefix(self, prefix: str, count: int = 100) -> list[str]:
        """
        获取指定前缀的所有 key

        :param prefix: 要搜索的键前缀
        :param count: 每次扫描批次的数量，值越大扫描速度越快，但会占用更多服务器资源
        :return:
        """
        return [key async for key in self.scan_iter(match=f'{prefix}*', count=count)]


# 创建 redis 客户端单例
redis_client: RedisCli = RedisCli()
