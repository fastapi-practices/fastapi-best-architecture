from __future__ import annotations

import asyncio
import json
import math

from datetime import datetime, timedelta
from multiprocessing.util import Finalize
from typing import TYPE_CHECKING, Final

from celery import current_app, schedules
from celery.beat import ScheduleEntry, Scheduler
from celery.signals import beat_init
from celery.utils.log import get_logger
from sqlalchemy import select
from sqlalchemy.exc import DatabaseError, InterfaceError

from backend.app.task.enums import PeriodType, TaskSchedulerType
from backend.app.task.model.scheduler import TaskScheduler
from backend.app.task.schema.scheduler import CreateTaskSchedulerParam
from backend.app.task.utils.tzcrontab import TzAwareCrontab, crontab_verify
from backend.common.exception import errors
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.database.redis import redis_client
from backend.utils.async_helper import run_await
from backend.utils.serializers import select_as_dict
from backend.utils.timezone import timezone

if TYPE_CHECKING:
    from redis.asyncio.lock import Lock

# 此计划程序必须比常规的 5 分钟更频繁地唤醒，因为它需要考虑对计划的外部更改
_DEFAULT_MAX_INTERVAL: Final = 5  # seconds

# 计划锁时长，避免重复创建
_DEFAULT_MAX_LOCK_TIMEOUT: Final = _DEFAULT_MAX_INTERVAL * 5  # seconds

logger = get_logger('fba.schedulers')


class ModelEntry(ScheduleEntry):
    """任务调度实体"""

    def __init__(self, model: TaskScheduler, app=None) -> None:  # noqa:ANN001,C901
        super().__init__(
            app=app or current_app._get_current_object(),
            name=model.name,
            task=model.task,
        )
        try:
            if (
                model.type == TaskSchedulerType.INTERVAL
                and model.interval_every is not None
                and model.interval_period is not None
            ):
                self.schedule = schedules.schedule(timedelta(**{model.interval_period: model.interval_every}))
            elif model.type == TaskSchedulerType.CRONTAB and model.crontab is not None:
                self.schedule = TzAwareCrontab.from_string(model.crontab)
            else:
                raise errors.NotFoundError(msg=f'{self.name} 计划为空！')
            # logger.debug('Schedule: {}'.format(self.schedule))
        except Exception as e:
            logger.error(f'禁用计划为空的任务 {self.name}，详情：{e}')
            asyncio.create_task(self._disable(model))

        try:
            self.args = json.loads(model.args) if model.args else None
            self.kwargs = json.loads(model.kwargs) if model.kwargs else None
        except ValueError as exc:
            logger.error(f'禁用参数错误的任务：{self.name}；error: {exc!s}')
            asyncio.create_task(self._disable(model))

        self.options = {}
        for option in ['queue', 'exchange', 'routing_key']:
            value = getattr(model, option)
            if value is None:
                continue
            self.options[option] = value

        if model.expire_seconds is not None:
            self.options['expires'] = model.expire_seconds
        elif model.expire_time is not None:
            self.options['expires'] = timezone.from_datetime(model.expire_time)

        if not model.last_run_time:
            model.last_run_time = timezone.now()
            if model.start_time:
                model.last_run_time = timezone.from_datetime(model.start_time) - timedelta(days=365)

        self.last_run_at = timezone.from_datetime(model.last_run_time)
        self.options['periodic_task_name'] = model.name
        self.model = model

    async def _disable(self, model: TaskScheduler) -> None:
        """禁用任务"""
        model.no_changes = True
        self.model.enabled = self.enabled = model.enabled = False
        async with async_db_session.begin() as db:
            stmt = select(TaskScheduler).where(TaskScheduler.id == model.id, TaskScheduler.deleted == 0)
            query = await db.execute(stmt)
            task = query.scalars().first()
            if task:
                task.no_changes = True
                task.enabled = False

    def is_due(self) -> tuple[bool, int | float | datetime]:
        """任务到期状态"""
        if not self.model.enabled:
            # 重新启用时延迟 5 秒
            return schedules.schedstate(is_due=False, next=5)

        # 仅在 'start_time' 之后运行
        if self.model.start_time is not None:
            now = timezone.now()
            start_time = timezone.from_datetime(self.model.start_time)
            if now < start_time:
                delay = math.ceil((start_time - now).total_seconds())
                return schedules.schedstate(is_due=False, next=delay)

        # 一次性任务
        if self.model.one_off and self.model.enabled and self.model.total_run_count > 0:
            self.model.enabled = False
            self.model.total_run_count = 0
            self.model.no_changes = False
            save_fields = ('enabled',)
            run_await(self.save)(save_fields)
            return schedules.schedstate(is_due=False, next=1000000000)  # 高延迟，避免重新检查

        return self.schedule.is_due(self.last_run_at)

    def __next__(self):  # noqa: ANN204
        self.model.last_run_time = timezone.now()
        self.model.total_run_count += 1
        self.model.no_changes = True
        return self.__class__(self.model)

    next = __next__

    async def save(self, fields: tuple = ()) -> None:
        """
        保存任务状态字段

        :param fields: 要保存的其他字段
        :return:
        """
        async with async_db_session.begin() as db:
            stmt = (
                select(TaskScheduler)
                .where(TaskScheduler.id == self.model.id, TaskScheduler.deleted == 0)
                .with_for_update()
            )
            query = await db.execute(stmt)
            task = query.scalars().first()
            if task:
                for field in ['last_run_time', 'total_run_count', 'no_changes']:
                    setattr(task, field, getattr(self.model, field))
                for field in fields:
                    setattr(task, field, getattr(self.model, field))
            else:
                logger.warning(f'任务 {self.model.name} 不存在，跳过更新')

    @classmethod
    async def from_entry(cls, name, app=None, **entry) -> ModelEntry:  # noqa: ANN001
        """保存或更新本地任务调度"""
        async with async_db_session.begin() as db:
            stmt = select(TaskScheduler).where(TaskScheduler.name == name, TaskScheduler.deleted == 0)
            query = await db.execute(stmt)
            task = query.scalars().first()
            temp = await cls._unpack_fields(name, **entry)
            if not task:
                task = TaskScheduler(**temp)
                db.add(task)
            else:
                for key, value in temp.items():
                    setattr(task, key, value)
            res = cls(task, app=app)
            return res

    @staticmethod
    async def to_model_schedule(name: str, task: str, schedule: schedules.schedule | TzAwareCrontab) -> TaskScheduler:
        schedule = schedules.maybe_schedule(schedule)

        async with async_db_session() as db:
            if isinstance(schedule, schedules.schedule):
                every = max(schedule.run_every.total_seconds(), 0)
                spec = {
                    'name': name,
                    'type': TaskSchedulerType.INTERVAL.value,
                    'interval_every': every,
                    'interval_period': PeriodType.SECONDS.value,
                }
                stmt = select(TaskScheduler).filter_by(**spec, deleted=0)
                query = await db.execute(stmt)
                obj = query.scalars().first()
                if not obj:
                    obj = TaskScheduler(**CreateTaskSchedulerParam(task=task, **spec).model_dump())
            elif isinstance(schedule, schedules.crontab):
                crontab = f'{schedule._orig_minute} {schedule._orig_hour} {schedule._orig_day_of_month} {schedule._orig_month_of_year} {schedule._orig_day_of_week}'  # noqa: E501
                crontab_verify(crontab)
                spec = {
                    'name': name,
                    'type': TaskSchedulerType.CRONTAB.value,
                    'crontab': crontab,
                }
                stmt = select(TaskScheduler).filter_by(**spec, deleted=0)
                query = await db.execute(stmt)
                obj = query.scalars().first()
                if not obj:
                    obj = TaskScheduler(**CreateTaskSchedulerParam(task=task, **spec).model_dump())
            else:
                raise errors.NotFoundError(msg=f'暂不支持的计划类型：{schedule}')

            return obj

    @classmethod
    async def _unpack_fields(
        cls,
        name: str,
        task: str,
        schedule: schedules.schedule | TzAwareCrontab,
        args: tuple | None = None,
        kwargs: dict | None = None,
        options: dict | None = None,
        **entry,
    ) -> dict:
        model_schedule = await cls.to_model_schedule(name, task, schedule)
        model_dict = select_as_dict(model_schedule)
        for k in ['id', 'created_time', 'updated_time', 'deleted', 'deleted_time']:
            try:
                del model_dict[k]
            except KeyError:  # noqa:PERF203
                continue
        model_dict.update(
            args=json.dumps(args, ensure_ascii=False) if args else None,
            kwargs=json.dumps(kwargs, ensure_ascii=False) if kwargs else None,
            **cls._unpack_options(**options or {}),
            **entry,
        )
        return model_dict

    @classmethod
    def _unpack_options(
        cls,
        queue: str | None = None,
        exchange: str | None = None,
        routing_key: str | None = None,
        start_time: datetime | None = None,
        expires: datetime | None = None,
        expire_seconds: int | None = None,
        *,
        one_off: bool = False,
    ) -> dict:
        data = {
            'queue': queue,
            'exchange': exchange,
            'routing_key': routing_key,
            'start_time': start_time,
            'expire_time': None,
            'expire_seconds': expire_seconds,
            'one_off': one_off,
        }
        if expires:
            if isinstance(expires, int):
                data['expire_seconds'] = expires
            elif isinstance(expires, timedelta):
                data['expire_time'] = timezone.now() + expires
            elif isinstance(expires, datetime):
                data['expire_time'] = expires
        return data


class DatabaseScheduler(Scheduler):
    """数据库调度程序"""

    Entry = ModelEntry

    _schedule = None
    _last_update = None
    _initial_read = True
    _heap_invalidated = False

    lock: Lock | None = None
    lock_key = f'{settings.CELERY_REDIS_PREFIX}:beat_lock'

    def __init__(self, *args, **kwargs) -> None:
        self.app = kwargs['app']
        self._dirty = set()
        super().__init__(*args, **kwargs)
        self._finalize = Finalize(self, self.sync, exitpriority=5)
        self.max_interval = kwargs.get('max_interval') or self.app.conf.beat_max_loop_interval or _DEFAULT_MAX_INTERVAL

    def schedules_equal(self, *args, **kwargs) -> bool:
        """重写父函数"""
        if self._heap_invalidated:
            self._heap_invalidated = False
            return False
        return super().schedules_equal(*args, **kwargs)

    def reserve(self, entry):  # noqa: ANN001, ANN201
        """重写父函数"""
        new_entry = next(entry)
        # 需要按名称存储条目，因为条目可能会发生变化
        self._dirty.add(new_entry.name)
        return new_entry

    def setup_schedule(self) -> None:
        """重写父函数"""
        logger.info('setup_schedule')
        tasks = self.schedule
        self.install_default_entries(tasks)
        self.update_from_dict(self.app.conf.beat_schedule)

    def sync(self) -> None:
        """重写父函数"""
        tried = set()
        failed = set()
        try:
            while self._dirty:
                name = self._dirty.pop()
                try:
                    tasks = self.schedule
                    run_await(tasks[name].save)()
                    logger.debug(f'保存任务 {name} 最新状态到数据库')
                    tried.add(name)
                except KeyError as e:
                    logger.error(f'保存任务 {name} 最新状态失败：{e} ')
                    failed.add(name)
        except DatabaseError:
            logger.exception('同步时出现数据库错误')
        except InterfaceError as e:
            logger.warning(f'DatabaseScheduler InterfaceError：{e!s}，等待下次调用时重试...')
        finally:
            # 请稍后重试（仅针对失败的）
            self._dirty |= failed

    def tick(self, **kwargs) -> float:
        """重写父函数"""
        if self.lock:
            logger.debug('beat: Extending lock...')
            run_await(self.lock.extend)(_DEFAULT_MAX_LOCK_TIMEOUT, replace_ttl=True)

        return super().tick(**kwargs)

    def close(self) -> None:
        """重写父函数"""
        if self.lock:
            logger.info('beat: Releasing lock')
            if run_await(self.lock.owned)():
                run_await(self.lock.release)()
            self.lock = None

        super().close()

    def update_from_dict(self, beat_dict: dict) -> None:
        """重写父函数"""
        s = {}
        name = None
        try:
            for name, entry_fields in beat_dict.items():
                entry = run_await(self.Entry.from_entry)(name, app=self.app, **entry_fields)
                if entry.model.enabled:
                    s[name] = entry
        except Exception:
            logger.error(f'添加任务 {name} 到数据库失败')
            raise

        tasks = self.schedule
        tasks.update(s)

    def schedule_changed(self) -> bool | None:
        """任务调度变更状态"""
        now = timezone.now()
        last_update = run_await(redis_client.get)(f'{settings.CELERY_REDIS_PREFIX}:last_update')
        if not last_update:
            run_await(redis_client.set)(f'{settings.CELERY_REDIS_PREFIX}:last_update', timezone.to_str(now))
            return False

        last, ts = self._last_update, timezone.from_str(last_update)
        try:
            if ts and ts > (last or ts):
                return True
        finally:
            self._last_update = now

    async def get_all_task_schedulers(self) -> dict:
        """获取所有任务调度"""
        async with async_db_session() as db:
            logger.debug('DatabaseScheduler: Fetching database schedule')
            stmt = select(TaskScheduler).where(
                TaskScheduler.enabled.is_(True),
                TaskScheduler.deleted == 0,
            )
            query = await db.execute(stmt)
            schedulers = query.scalars().all()
            s = {}
            for scheduler in schedulers:
                s[scheduler.name] = self.Entry(scheduler, app=self.app)
            return s

    @property
    def schedule(self) -> dict[str, ModelEntry]:
        """获取任务调度"""
        initial = update = False
        if self._initial_read:
            logger.debug('DatabaseScheduler: initial read')
            initial = update = True
            self._initial_read = False
        elif self.schedule_changed():
            logger.info('DatabaseScheduler: Schedule changed.')
            update = True

        if update:
            logger.debug('beat: Synchronizing schedule...')
            self.sync()
            self._schedule = run_await(self.get_all_task_schedulers)()
            # 计划已更改，使 Scheduler.tick 中的堆无效
            if not initial:
                self._heap = []
                self._heap_invalidated = True
            logger.debug(
                'Current schedule:\n%s',
                '\n'.join(repr(entry) for entry in self._schedule.values()),
            )

        # logger.debug(self._schedule)
        return self._schedule


@beat_init.connect
def acquire_distributed_beat_lock(sender=None, **kwargs) -> None:  # noqa: ANN001
    """
    尝试在启动时获取锁

    :param sender: 接收方应响应的发送方
    :return:
    """
    scheduler = sender.scheduler
    if not scheduler.lock_key:
        return

    logger.debug('beat: Acquiring lock...')
    lock = redis_client.lock(
        scheduler.lock_key,
        timeout=_DEFAULT_MAX_LOCK_TIMEOUT,
        sleep=scheduler.max_interval,
    )

    run_await(lock.acquire)()
    logger.info('beat: Acquired lock')
    scheduler.lock = lock
