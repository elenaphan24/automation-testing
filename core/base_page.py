from __future__ import annotations

from typing import Any

from core.config import get
from core.logging_util import get_logger


class BasePage:
    """Shared page wrapper.

    Real Playwright projects should capture `page.screenshot()` in an autouse
    fixture on failure. The fake page fixture stores screenshots on the pytest
    node so the framework-level failure hook can embed them into pytest-html.
    """

    path = "/"

    def __init__(self, page: Any) -> None:
        self.page = page
        self.base_url = get("urls.base_url")
        self.logger = get_logger(self.__class__.__name__, "UI")

    def goto(self, path: str | None = None) -> None:
        target = path or self.path
        url = f"{self.base_url.rstrip('/')}/{target.lstrip('/')}"
        self.logger.info("navigate %s", url)
        self.page.goto(url)

    def click(self, selector: str) -> None:
        self.logger.info("click %s", selector)
        self.page.click(selector)

    def fill(self, selector: str, value: str) -> None:
        self.logger.info("fill %s", selector)
        self.page.fill(selector, value)

    def get_by_role(self, role: str, **kwargs) -> Any:
        self.logger.info("locate by role %s %s", role, kwargs)
        return self.page.get_by_role(role, **kwargs)

    def get_by_label(self, text: str, **kwargs) -> Any:
        self.logger.info("locate by label %s", text)
        return self.page.get_by_label(text, **kwargs)

    def get_by_placeholder(self, text: str, **kwargs) -> Any:
        self.logger.info("locate by placeholder %s", text)
        return self.page.get_by_placeholder(text, **kwargs)

    def get_by_test_id(self, test_id: str) -> Any:
        self.logger.info("locate by test-id %s", test_id)
        return self.page.get_by_test_id(test_id)

    def screenshot(self, name: str = "screenshot") -> bytes:
        image = self.page.screenshot()
        node = getattr(self.page, "_pytest_node", None)
        if node is not None:
            setattr(node, "_screenshot", image)
        self.logger.info("screenshot %s captured", name)
        return image
