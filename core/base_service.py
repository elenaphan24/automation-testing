from __future__ import annotations

from typing import Any, Protocol

from core.allure_compat import allure
from core.config import get
from core.logging_util import get_logger


class ResponseLike(Protocol):
    status_code: int

    def json(self) -> dict[str, Any]:
        ...


class Transport(Protocol):
    def request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> ResponseLike:
        ...


class BaseService:
    def __init__(self, transport: Transport, auth_token: str | None = None) -> None:
        self.transport = transport
        self.auth_token = auth_token
        self.base_url = get("urls.api_base_url")
        self.logger = get_logger(self.__class__.__name__, "API")

    def _headers(self) -> dict[str, str]:
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers

    @allure.step("API request: {method} {path}")
    def request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        self.logger.info("%s %s", method.upper(), path)
        response = self.transport.request(
            method.upper(),
            path,
            json=payload,
            headers=self._headers(),
        )
        data = response.json()
        if response.status_code >= 400:
            raise AssertionError(f"{method.upper()} {path} failed: {response.status_code} {data}")
        return data

    @allure.step("Assert API response field {field}")
    def assert_field(self, actual: dict[str, Any], field: str, expected: Any) -> None:
        self.logger.info("assert %s == %r", field, expected)
        assert actual.get(field) == expected

