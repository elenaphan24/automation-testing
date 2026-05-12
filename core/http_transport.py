from __future__ import annotations

import json
from dataclasses import dataclass
from json import JSONDecodeError
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen


@dataclass
class HttpResponse:
    status_code: int
    body: bytes

    def json(self) -> dict[str, Any]:
        if not self.body:
            return {}

        text = self.body.decode("utf-8")
        try:
            data = json.loads(text)
        except JSONDecodeError:
            return {"data": text}

        if isinstance(data, dict):
            return data
        return {"data": data}


class UrlLibTransport:
    def __init__(self, base_url: str, timeout_seconds: int = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        body = None
        if json is not None:
            body = json_dumps(json)

        request = Request(
            f"{self.base_url}/{path.lstrip('/')}",
            data=body,
            headers=headers or {},
            method=method.upper(),
        )

        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                return HttpResponse(response.status, response.read())
        except HTTPError as exc:
            return HttpResponse(exc.code, exc.read())


def json_dumps(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload).encode("utf-8")
