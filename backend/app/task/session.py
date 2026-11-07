"""重写 celery SessionManager，禁止 celery 自动创建其内部任务结果表"""

from celery.backends.database.session import SessionManager as CelerySessionManager


class SessionManager(CelerySessionManager):
    def __init__(self, engine_callback=None) -> None:  # ruff:ignore[missing-type-function-argument]
        super().__init__(engine_callback=engine_callback)

        self.prepared = True
