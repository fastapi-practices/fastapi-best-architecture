from celery.backends.database.session import SessionManager as CelerySessionManager


class SessionManager(CelerySessionManager):
    """
    重写 celery SessionManager
    """

    def __init__(self, engine_callback=None) -> None:  # ruff:ignore[missing-type-function-argument]
        super().__init__(engine_callback=engine_callback)

        # 禁止自动创建 celery 内部定义的任务结果表
        self.prepared = True
