from __future__ import annotations

from typing import Any

from core.allure_compat import allure
from core.config import get
from core.logging_util import get_logger


class BasePage:
    """Shared page wrapper.

    Real Playwright projects should capture `page.screenshot()` in an autouse
    fixture on failure. The fake page fixture stores screenshots on the pytest
    node so the framework-level Allure failure hook can attach them.
    """

    path = "/"

    def __init__(self, page: Any) -> None:
        self.page = page
        self.base_url = get("urls.base_url")
        self.logger = get_logger(self.__class__.__name__, "UI")

    @allure.step("Navigate to page")
    def goto(self, path: str | None = None) -> None:
        target = path or self.path
        url = f"{self.base_url.rstrip('/')}/{target.lstrip('/')}"
        self.logger.info("navigate %s", url)
        self.page.goto(url)

    @allure.step("Click {selector}")
    def click(self, selector: str) -> None:
        self.logger.info("click %s", selector)
        self.page.click(selector)

    @allure.step("Fill {selector}")
    def fill(self, selector: str, value: str) -> None:
        self.logger.info("fill %s", selector)
        self.page.fill(selector, value)

    @allure.step("Take screenshot")
    def screenshot(self, name: str = "screenshot") -> bytes:
        image = self.page.screenshot()
        node = getattr(self.page, "_pytest_node", None)
        if node is not None:
            setattr(node, "_screenshot", image)
        allure.attach(image, name=name, attachment_type=getattr(allure.attachment_type, "PNG", None))
        return image

