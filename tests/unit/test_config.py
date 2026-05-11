import pytest

from core import config


@pytest.fixture(autouse=True)
def clear_config_cache(monkeypatch):
    monkeypatch.delenv("ENV", raising=False)
    config.load_config.cache_clear()
    yield
    config.load_config.cache_clear()


def test_default_env_is_sandbox():
    assert config.load_config()["env"] == "sandbox"


@pytest.mark.parametrize("env", ["sandbox", "staging", "production"])
def test_valid_envs_load(monkeypatch, env):
    monkeypatch.setenv("ENV", env)
    config.load_config.cache_clear()

    assert config.load_config()["env"] == env


def test_invalid_env_raises_value_error(monkeypatch):
    monkeypatch.setenv("ENV", "ci")
    config.load_config.cache_clear()

    with pytest.raises(ValueError, match="ENV='ci' is not valid"):
        config.load_config()


def test_dot_notation_get_reads_nested_value():
    assert config.get("urls.base_url") == "https://sandbox.app.example.com"


def test_common_yaml_deep_merge_values_are_available():
    assert config.get("retry.max_attempts") == 3
    assert config.get("timeouts.page_load_ms") == 10000


def test_default_value_fallback_for_missing_key():
    assert config.get("missing.value", "fallback") == "fallback"


def test_validate_required_keys_returns_empty_for_sandbox():
    assert config.validate_required_keys() == []

