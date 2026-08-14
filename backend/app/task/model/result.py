import sqlalchemy as sa

from celery import states
from sqlalchemy.types import PickleType

from backend.common.model import MappedBase, TimeZone
from backend.utils.timezone import timezone

"""
重写 celery.backends.database.models 内部所有模型，适配 fba 创建表和 alembic 迁移
"""


class Task(MappedBase):
    """Task result/status."""

    __tablename__ = 'task_result'
    __table_args__ = {'comment': '任务结果表'}

    id = sa.Column(sa.Integer, sa.Sequence('task_id_sequence'), primary_key=True, autoincrement=True)
    task_id = sa.Column(sa.String(155), unique=True)
    status = sa.Column(sa.String(64), default=states.PENDING)
    result = sa.Column(PickleType, nullable=True)
    date_done = sa.Column(
        TimeZone,
        default=timezone.now,
        onupdate=timezone.now,
        nullable=True,
    )
    traceback = sa.Column(sa.Text, nullable=True)

    def __init__(self, task_id: str) -> None:
        self.task_id = task_id

    def to_dict(self) -> dict:
        return {
            'task_id': self.task_id,
            'status': self.status,
            'result': self.result,
            'traceback': self.traceback,
            'date_done': self.date_done,
        }

    def __repr__(self) -> str:
        return f'<Task {self.task_id} state: {self.status}>'

    @classmethod
    def configure(cls, schema=None, name=None) -> None:  # ruff:ignore[missing-type-function-argument]
        cls.__table__.schema = schema
        cls.id.default.schema = schema
        cls.__table__.name = name or cls.__tablename__


class TaskExtended(Task):
    """For the extend result."""

    __tablename__ = 'task_result'
    __table_args__ = {'extend_existing': True, 'comment': '任务结果表'}

    name = sa.Column(sa.String(155), nullable=True)
    args = sa.Column(sa.LargeBinary, nullable=True)
    kwargs = sa.Column(sa.LargeBinary, nullable=True)
    worker = sa.Column(sa.String(155), nullable=True)
    retries = sa.Column(sa.Integer, nullable=True)
    queue = sa.Column(sa.String(155), nullable=True)

    def to_dict(self) -> dict:
        task_dict = super().to_dict()
        task_dict.update({
            'name': self.name,
            'args': self.args,
            'kwargs': self.kwargs,
            'worker': self.worker,
            'retries': self.retries,
            'queue': self.queue,
        })
        return task_dict


class TaskSet(MappedBase):
    """TaskSet result."""

    __tablename__ = 'task_set_result'
    __table_args__ = {'comment': '任务集结果表'}

    id = sa.Column(sa.Integer, sa.Sequence('taskset_id_sequence'), autoincrement=True, primary_key=True)
    taskset_id = sa.Column(sa.String(155), unique=True)
    result = sa.Column(PickleType, nullable=True)
    date_done = sa.Column(TimeZone, default=timezone.now, nullable=True)

    def __init__(self, taskset_id, result) -> None:  # ruff:ignore[missing-type-function-argument]
        self.taskset_id = taskset_id
        self.result = result

    def to_dict(self) -> dict:
        return {
            'taskset_id': self.taskset_id,
            'result': self.result,
            'date_done': self.date_done,
        }

    def __repr__(self) -> str:
        return f'<TaskSet: {self.taskset_id}>'

    @classmethod
    def configure(cls, schema=None, name=None) -> None:  # ruff:ignore[missing-type-function-argument]
        cls.__table__.schema = schema
        cls.id.default.schema = schema
        cls.__table__.name = name or cls.__tablename__
