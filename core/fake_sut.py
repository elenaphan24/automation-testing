from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Any


@dataclass
class FakeResponse:
    status_code: int
    body: dict[str, Any]

    def json(self) -> dict[str, Any]:
        return self.body


class FakeDatabase:
    def __init__(self) -> None:
        self.schemas: dict[str, dict[str, Any]] = {}

    def create_schema(self, schema: str) -> None:
        self.schemas[schema] = {"users": {}, "sessions": {}}

    def drop_schema(self, schema: str) -> None:
        self.schemas.pop(schema, None)

    def schema_exists(self, schema: str) -> bool:
        return schema in self.schemas

    def count_rows(self, schema: str, table: str) -> int:
        return len(self.schemas[schema][table])


class FakeApiTransport:
    _ids = itertools.count(1)

    def __init__(self, db: FakeDatabase, schema: str) -> None:
        self.db = db
        self.schema = schema

    def request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> FakeResponse:
        payload = json or {}
        users = self.db.schemas[self.schema]["users"]
        sessions = self.db.schemas[self.schema]["sessions"]

        if method == "POST" and path == "/users":
            user_id = str(next(self._ids))
            email = payload.get("email", f"user{user_id}@example.test")
            user = {
                "id": user_id,
                "email": email,
                "password": payload.get("password", "Password123!"),
                "type": payload.get("type", "standard"),
                "tier": payload.get("tier", "standard"),
                "balance": payload.get("balance", 500),
            }
            users[user_id] = user
            return FakeResponse(201, user)

        if method == "PATCH" and path.endswith("/promote"):
            user_id = path.split("/")[2]
            users[user_id]["tier"] = payload.get("tier", "vip")
            return FakeResponse(200, users[user_id])

        if method == "POST" and path == "/sessions":
            email = payload.get("email")
            match = next((user for user in users.values() if user["email"] == email), None)
            if not match:
                return FakeResponse(404, {"error": "user not found"})
            token = f"fake-token-{match['id']}"
            sessions[token] = {"user_id": match["id"]}
            return FakeResponse(201, {"token": token, "user_id": match["id"]})

        if method == "GET" and path.startswith("/sessions/"):
            token = path.rsplit("/", 1)[-1]
            return FakeResponse(200, {"active": token in sessions, "token": token})

        if method == "GET" and path.startswith("/users/"):
            user_id = path.rsplit("/", 1)[-1]
            return FakeResponse(200, users[user_id])

        if method == "POST" and path.endswith("/purchases"):
            user_id = path.split("/")[2]
            amount = int(payload.get("amount", 0))
            users[user_id]["balance"] -= amount
            return FakeResponse(201, {"user_id": user_id, "amount": amount, "balance": users[user_id]["balance"]})

        if method == "DELETE" and path.startswith("/users/"):
            email = path.rsplit("/", 1)[-1]
            user_id = next((uid for uid, user in users.items() if user["email"] == email), None)
            if user_id:
                users.pop(user_id)
            return FakeResponse(204, {"deleted": bool(user_id)})

        return FakeResponse(404, {"error": f"Unhandled fake route: {method} {path}"})


class FakeBrowserPage:
    def __init__(self) -> None:
        self.url = ""
        self.title_text = "Sandbox QA App"
        self.fields: dict[str, str] = {}
        self.clicked: list[str] = []
        self.purchase_handler = None

    def goto(self, url: str) -> None:
        self.url = url

    def click(self, selector: str) -> None:
        self.clicked.append(selector)

    def fill(self, selector: str, value: str) -> None:
        self.fields[selector] = value

    def title(self) -> str:
        return self.title_text

    def screenshot(self) -> bytes:
        return b"fake-png"
