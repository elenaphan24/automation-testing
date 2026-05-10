from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
ALLOWED_ENVS = {"sandbox", "staging", "production"}


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _read_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


@lru_cache(maxsize=1)
def load_config() -> dict[str, Any]:
    env = os.environ.get("ENV", "sandbox").lower()
    if env not in ALLOWED_ENVS:
        allowed = ", ".join(sorted(ALLOWED_ENVS))
        raise ValueError(f"ENV='{env}' is not valid. Must be one of: {allowed}")

    common = _read_yaml(CONFIG_DIR / "common.yaml")
    env_config = _read_yaml(CONFIG_DIR / "envs" / f"{env}.yaml")
    return _deep_merge(common, env_config)


def get(key: str, default: Any = None) -> Any:
    value: Any = load_config()
    for part in key.split("."):
        if not isinstance(value, dict) or part not in value:
            return default
        value = value[part]
    return value


def validate_required_keys(required: list[str] | None = None) -> list[str]:
    required_keys = required or [
        "env",
        "urls.base_url",
        "urls.api_base_url",
        "auth.jwt_secret_var",
        "database.schema_prefix",
        "database.connection_var",
    ]
    return [key for key in required_keys if get(key) is None]

