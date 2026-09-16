import asyncio
import datetime
import os
import threading
import time

from dataclasses import dataclass

from backend.common.dataclasses import SnowflakeInfo
from backend.common.exception import errors
from backend.common.log import log
from backend.core.conf import settings
from backend.database.redis import redis_client
from backend.utils.timezone import timezone


@dataclass(frozen=True)
class SnowflakeConfig:
    """雪花算法配置类，采用 Twitter 原版 Snowflake 64 位 ID 位分配配置（通用标准）"""

    # 位分配
    WORKER_ID_BITS: int = 5
    DATACENTER_ID_BITS: int = 5
    SEQUENCE_BITS: int = 12

    # 最大值
    MAX_WORKER_ID: int = (1 << WORKER_ID_BITS) - 1  # 31
    MAX_DATACENTER_ID: int = (1 << DATACENTER_ID_BITS) - 1  # 31
    SEQUENCE_MASK: int = (1 << SEQUENCE_BITS) - 1  # 4095

    # 位移偏移
    WORKER_ID_SHIFT: int = SEQUENCE_BITS
    DATACENTER_ID_SHIFT: int = SEQUENCE_BITS + WORKER_ID_BITS
    TIMESTAMP_LEFT_SHIFT: int = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

    # 元年时间戳
    EPOCH: int = 1262275200000

    # 时钟回拨容忍阈值，应对 NTP 自动同步引起的正常回跳（非标准）
    CLOCK_BACKWARD_TOLERANCE_MS: int = 10_000


class SnowflakeNodeManager:
    """雪花算法节点管理器，负责从 Redis 分配和管理节点 ID"""

    def __init__(self) -> None:
        """初始化节点管理器"""
        self.datacenter_id: int | None = None
        self.worker_id: int | None = None
        self.node_redis_prefix: str = f'{settings.SNOWFLAKE_REDIS_PREFIX}:nodes'
        self._heartbeat_task: asyncio.Task | None = None

    async def acquire_node_id(self) -> tuple[int, int]:
        """从 Redis 获取可用的 datacenter_id 和 worker_id"""
        occupied_nodes = set()
        async for key in redis_client.scan_iter(match=f'{self.node_redis_prefix}:*', count=1000):
            parts = key.split(':')
            if len(parts) >= 5:
                try:
                    datacenter_id = int(parts[-2])
                    worker_id = int(parts[-1])
                    occupied_nodes.add((datacenter_id, worker_id))
                except ValueError:
                    continue

        # 顺序查找第一个可用的 ID 组合
        for datacenter_id in range(SnowflakeConfig.MAX_DATACENTER_ID + 1):
            for worker_id in range(SnowflakeConfig.MAX_WORKER_ID + 1):
                if (datacenter_id, worker_id) not in occupied_nodes and await self._register(datacenter_id, worker_id):
                    return datacenter_id, worker_id

        raise errors.ServerError(msg='无可用的雪花算法节点，节点已耗尽')

    async def _register(self, datacenter_id: int, worker_id: int) -> bool:
        key = f'{self.node_redis_prefix}:{datacenter_id}:{worker_id}'
        value = f'pid:{os.getpid()}-ts:{timezone.now().timestamp()}'
        return await redis_client.set(key, value, nx=True, ex=settings.SNOWFLAKE_NODE_TTL_SECONDS)

    async def start_heartbeat(self, datacenter_id: int, worker_id: int) -> None:
        """启动节点心跳"""
        self.datacenter_id = datacenter_id
        self.worker_id = worker_id

        async def heartbeat() -> None:
            key = f'{self.node_redis_prefix}:{datacenter_id}:{worker_id}'
            while True:
                await asyncio.sleep(settings.SNOWFLAKE_HEARTBEAT_INTERVAL_SECONDS)
                try:
                    await redis_client.expire(key, settings.SNOWFLAKE_NODE_TTL_SECONDS)
                    log.debug(f'雪花算法节点心跳任务开始：datacenter_id={datacenter_id}, worker_id={worker_id}')
                except Exception as e:
                    log.error(f'雪花算法节点心跳任务失败：{e}')

        self._heartbeat_task = asyncio.create_task(heartbeat())

    async def release(self) -> None:
        """释放节点"""
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            try:
                await self._heartbeat_task
            except asyncio.CancelledError:
                log.debug(f'雪花算法节点心跳任务释放：datacenter_id={self.datacenter_id}, worker_id={self.worker_id}')

        if self.datacenter_id is not None and self.worker_id is not None:
            key = f'{self.node_redis_prefix}:{self.datacenter_id}:{self.worker_id}'
            await redis_client.delete(key)


class Snowflake:
    """雪花算法类"""

    def __init__(self) -> None:
        """初始化雪花算法"""
        self.datacenter_id: int | None = None
        self.worker_id: int | None = None
        self.sequence: int = 0
        self.last_timestamp: int = -1

        self._lock = threading.Lock()
        self._init_lock = asyncio.Lock()
        self._initialized = False
        self._node_manager: SnowflakeNodeManager | None = None
        self._auto_allocated = False  # 标记是否由 Redis 自动分配 ID

    async def init(self) -> None:
        """初始化雪花算法"""
        if self._initialized:
            return

        # 初始化涉及 Redis IO，必须用 asyncio.Lock，threading.Lock 会在 await 期间锁死事件循环
        async with self._init_lock:
            if self._initialized:
                return

            # 环境变量固定分配
            if settings.SNOWFLAKE_DATACENTER_ID is not None and settings.SNOWFLAKE_WORKER_ID is not None:
                self.datacenter_id = settings.SNOWFLAKE_DATACENTER_ID
                self.worker_id = settings.SNOWFLAKE_WORKER_ID
                log.debug(
                    f'雪花算法使用环境变量固定节点：datacenter_id={self.datacenter_id}, worker_id={self.worker_id}'
                )
            elif (settings.SNOWFLAKE_DATACENTER_ID is not None and settings.SNOWFLAKE_WORKER_ID is None) or (
                settings.SNOWFLAKE_DATACENTER_ID is None and settings.SNOWFLAKE_WORKER_ID is not None
            ):
                log.error('雪花算法 datacenter_id 和 worker_id 配置错误，只允许同时非 None 或同时为 None')
                raise errors.ServerError(msg='雪花算法配置失败，请联系系统管理员')
            else:
                # Redis 动态分配
                self._node_manager = SnowflakeNodeManager()
                self.datacenter_id, self.worker_id = await self._node_manager.acquire_node_id()
                self._auto_allocated = True
                await self._node_manager.start_heartbeat(self.datacenter_id, self.worker_id)
                log.debug(
                    f'雪花算法使用 Redis 动态分配节点：datacenter_id={self.datacenter_id}, worker_id={self.worker_id}'
                )

            # 严格校验范围
            if not (0 <= self.datacenter_id <= SnowflakeConfig.MAX_DATACENTER_ID):
                log.error(f'雪花算法 datacenter_id 配置失败，必须在 0~{SnowflakeConfig.MAX_DATACENTER_ID} 之间')
                raise errors.ServerError(msg='雪花算法数据中心配置失败，请联系系统管理员')
            if not (0 <= self.worker_id <= SnowflakeConfig.MAX_WORKER_ID):
                log.error(f'雪花算法 worker_id 配置失败，必须在 0~{SnowflakeConfig.MAX_WORKER_ID} 之间')
                raise errors.ServerError(msg='雪花算法工作机器配置失败，请联系系统管理员')

            self._initialized = True

    async def shutdown(self) -> None:
        """释放 Redis 节点"""
        if self._node_manager and self._auto_allocated:
            await self._node_manager.release()

    @staticmethod
    def _current_ms() -> int:
        return int(timezone.now().timestamp() * 1000)

    def _till_next_ms(self, last_timestamp: int) -> int:
        """等待直到下一毫秒"""
        ts = self._current_ms()
        while ts <= last_timestamp:
            time.sleep(0.0001)
            ts = self._current_ms()
        return ts

    def generate(self) -> int:
        """生成雪花 ID"""
        if not self._initialized:
            raise errors.ServerError(msg='雪花 ID 生成失败，雪花算法未初始化')

        with self._lock:
            timestamp = self._current_ms()

            # 时钟回拨处理
            if timestamp < self.last_timestamp:
                back_ms = self.last_timestamp - timestamp
                if back_ms <= SnowflakeConfig.CLOCK_BACKWARD_TOLERANCE_MS:
                    log.warning(f'检测到时钟回拨 {back_ms} ms，等待恢复...')
                    timestamp = self._till_next_ms(self.last_timestamp)
                else:
                    raise errors.ServerError(msg=f'雪花 ID 生成失败，时钟回拨超过 {back_ms} ms，请立即联系系统管理员')

            # 同毫秒内序列号递增
            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & SnowflakeConfig.SEQUENCE_MASK
                if self.sequence == 0:
                    timestamp = self._till_next_ms(self.last_timestamp)
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            # 组合 64 位 ID
            return (
                ((timestamp - SnowflakeConfig.EPOCH) << SnowflakeConfig.TIMESTAMP_LEFT_SHIFT)
                | (self.datacenter_id << SnowflakeConfig.DATACENTER_ID_SHIFT)
                | (self.worker_id << SnowflakeConfig.WORKER_ID_SHIFT)
                | self.sequence
            )

    @staticmethod
    def parse(snowflake_id: int) -> SnowflakeInfo:
        """
        解析雪花 ID，获取其包含的详细信息

        :param snowflake_id: 雪花ID
        :return:
        """
        timestamp = (snowflake_id >> SnowflakeConfig.TIMESTAMP_LEFT_SHIFT) + SnowflakeConfig.EPOCH
        datacenter_id = (snowflake_id >> SnowflakeConfig.DATACENTER_ID_SHIFT) & SnowflakeConfig.MAX_DATACENTER_ID
        worker_id = (snowflake_id >> SnowflakeConfig.WORKER_ID_SHIFT) & SnowflakeConfig.MAX_WORKER_ID
        sequence = snowflake_id & SnowflakeConfig.SEQUENCE_MASK

        return SnowflakeInfo(
            timestamp=timestamp,
            datetime=timezone.to_str(datetime.datetime.fromtimestamp(timestamp / 1000, timezone.tz_info)),
            datacenter_id=datacenter_id,
            worker_id=worker_id,
            sequence=sequence,
        )


snowflake = Snowflake()
