from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any


class LayerTagFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        layer = getattr(record, "layer", "TAF")
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "layer": f"[{layer}]",
            "logger": record.name,
            "message": record.getMessage(),
        }
        return json.dumps(payload, sort_keys=True)


class LayerLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg: str, kwargs: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        extra = kwargs.setdefault("extra", {})
        extra.setdefault("layer", self.extra["layer"])
        return msg, kwargs


def get_logger(name: str, layer: str = "TAF") -> LayerLoggerAdapter:
    root = logging.getLogger()
    if not root.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(LayerTagFormatter())
        root.addHandler(handler)
        root.setLevel(logging.INFO)
    return LayerLoggerAdapter(logging.getLogger(name), {"layer": layer})

