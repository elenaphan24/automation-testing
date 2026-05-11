"""Pytest scaffold for the live JWT injection spike.

The fake SUT cannot answer browser storage, CSRF, token TTL, or session binding
questions. These tests are intentionally skipped until a live sandbox SUT and
real Playwright fixtures are wired.
"""

import pytest


pytest.skip("Requires live sandbox SUT", allow_module_level=True)


def test_browser_context_accepts_injected_jwt():
    """Can a Playwright BrowserContext accept a JWT from the API response?"""


def test_app_enforces_csrf_on_injected_session():
    """Does the app enforce CSRF validation on injected sessions?"""


def test_token_ttl_does_not_expire_mid_suite():
    """What is the token TTL, and can it expire mid-run on long suites?"""


def test_session_binding_blocks_cross_env_injection():
    """Does session binding prevent cross-environment injection?"""
