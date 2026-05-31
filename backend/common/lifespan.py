from collections.abc import Callable
from contextlib import AbstractAsyncContextManager, AsyncExitStack, asynccontextmanager
from typing import Any, TypeAlias, overload

from fastapi import FastAPI

from backend.common.enums import LifespanStage

LifespanFunc: TypeAlias = Callable[[FastAPI], AbstractAsyncContextManager[dict[str, Any] | None]]


class LifespanManager:
    """FastAPI lifespan 管理器"""

    def __init__(self) -> None:
        self._lifespans: dict[LifespanStage, list[LifespanFunc]] = {
            LifespanStage.core: [],
            LifespanStage.plugin: [],
            LifespanStage.tail: [],
        }

    @overload
    def register(self, func: LifespanFunc) -> LifespanFunc: ...

    @overload
    def register(self, *, stage: LifespanStage) -> Callable[[LifespanFunc], LifespanFunc]: ...

    def register(
        self, func: LifespanFunc | None = None, *, stage: LifespanStage = LifespanStage.core
    ) -> LifespanFunc | Callable[[LifespanFunc], LifespanFunc]:
        """
        注册 lifespan hook

        :param func: lifespan hook（直接装饰时使用）
        :param stage: 执行阶段，控制粗粒度顺序，默认为 core
        :return:
        """

        def decorator(f: LifespanFunc) -> LifespanFunc:
            for hooks in self._lifespans.values():
                for fn in hooks:
                    if fn is f:
                        return f

            self._lifespans[stage].append(f)
            return f

        if func is not None:
            return decorator(func)

        return decorator

    def build(self) -> LifespanFunc:
        """
        构建组合后的 lifespan hook

        :return:
        """

        @asynccontextmanager
        async def combined_lifespan(app: FastAPI):  # noqa: ANN202
            state: dict[str, Any] = {}
            async with AsyncExitStack() as exit_stack:
                for stage in LifespanStage:
                    for lifespan_fn in self._lifespans[stage]:
                        result = await exit_stack.enter_async_context(lifespan_fn(app))
                        if isinstance(result, dict):
                            state.update(result)

                for key, value in state.items():
                    setattr(app.state, key, value)

                yield state or None

        return combined_lifespan


# 创建 lifespan_manager 单例
lifespan_manager = LifespanManager()
