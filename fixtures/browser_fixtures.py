from __future__ import annotations

import os

import pytest


@pytest.fixture(scope="session")
def live_browser():
    pytest.importorskip("playwright.sync_api")
    from playwright.sync_api import sync_playwright

    headless = os.getenv("LIVE_HEADLESS", "1") != "0"
    with sync_playwright() as playwright:
        playwright.selectors.set_test_id_attribute("data-test")
        browser = playwright.chromium.launch(headless=headless)
        try:
            yield browser
        finally:
            browser.close()


@pytest.fixture
def live_browser_page(live_browser):
    context = live_browser.new_context()
    try:
        yield context.new_page()
    finally:
        context.close()
