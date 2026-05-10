from __future__ import annotations

from contextlib import nullcontext
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


try:
    import allure  # type: ignore
except ImportError:

    class _AllureFallback:
        attachment_type = type("AttachmentType", (), {"TEXT": "text/plain", "PNG": "image/png"})

        @staticmethod
        def step(title: str) -> Callable[[F], F]:
            def decorator(func: F) -> F:
                return func

            return decorator

        @staticmethod
        def attach(body: Any, name: str | None = None, attachment_type: Any = None) -> None:
            return None

    allure = _AllureFallback()  # type: ignore


def step_context(title: str):
    step = getattr(allure, "step", None)
    if callable(step):
        context = step(title)
        if hasattr(context, "__enter__"):
            return context
    return nullcontext()

