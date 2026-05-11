from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from core.logging_util import get_logger


class JourneyFailure(AssertionError):
    def __init__(self, phase: str, layer: str, original: Exception) -> None:
        super().__init__(f"{phase} failed at layer {layer}: {original}")
        self.phase = phase
        self.layer = layer
        self.original = original


@dataclass
class Journey:
    context: dict[str, Any] = field(default_factory=dict)
    logger: Any = field(default_factory=lambda: get_logger("Journey", "TAF"))

    def given(self, actor: Any) -> "Journey":
        try:
            self.logger.info("GIVEN %s", actor.role)
            self.context["actor"] = actor
            self.context["credentials"] = actor.seed()
        except Exception as exc:
            raise JourneyFailure("GIVEN", "API", exc) from exc
        return self

    def when(self, action: Callable[..., Any], *args: Any, layer: str = "UI", **kwargs: Any) -> "Journey":
        try:
            self.logger.info("WHEN %s", action.__name__)
            self.context["last_action"] = action(*args, **kwargs)
        except Exception as exc:
            raise JourneyFailure("WHEN", layer, exc) from exc
        return self

    def then(self, assertion: Callable[..., Any], *args: Any, **kwargs: Any) -> "Journey":
        try:
            self.logger.info("THEN %s", assertion.__name__)
            assertion(*args, **kwargs)
        except Exception as exc:
            raise JourneyFailure("THEN", "API", exc) from exc
        return self
