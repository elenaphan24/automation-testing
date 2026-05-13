import pytest

from core.config import get, validate_required_keys


@pytest.mark.smoke
def test_config_loads_required_keys():
    missing = validate_required_keys()
    assert missing == [], f"Missing required config keys: {missing}"


@pytest.mark.smoke
def test_base_url_is_reachable_format():
    url = get("urls.base_url")
    assert url and url.startswith("https://"), f"base_url invalid: {url!r}"
