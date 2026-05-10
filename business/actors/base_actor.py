from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseActor(ABC):
    def __init__(self, api_service: Any, db_schema: str) -> None:
        self.api = api_service
        self.schema = db_schema
        self.credentials: dict[str, Any] = {}
        self.user: dict[str, Any] = {}

    @abstractmethod
    def seed(self) -> dict[str, Any]:
        """Create all preconditions for this Actor via API. Returns credentials."""

    @abstractmethod
    def teardown(self) -> None:
        """Remove all test data created by this Actor."""

    @property
    @abstractmethod
    def role(self) -> str:
        """Human-readable role name used in log attribution and Allure steps."""

