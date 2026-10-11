"""The browser fixture serves its origin while rejecting rebinding and foreign reads."""

from __future__ import annotations

from collections.abc import Callable
from http.client import HTTPConnection
from pathlib import Path
from urllib.parse import urlsplit

import pytest

from workbench_tools import browser_page


class _Page:
    def __init__(self) -> None:
        self.url = ""
        self.close: Callable[[], None] = lambda: None

    def on(self, event: str, callback: Callable[[], None]) -> None:
        assert event == "close"
        self.close = callback

    def goto(self, url: str, *, wait_until: str) -> None:
        assert wait_until == "load"
        self.url = url


@pytest.mark.parametrize("method", ["GET", "HEAD"])
@pytest.mark.parametrize(
    ("kind", "status"),
    [
        ("no-origin", 200),
        ("same-origin", 200),
        ("foreign-host", 403),
        ("foreign-origin", 403),
        ("null-origin", 403),
        ("missing-host", 403),
        ("duplicate-host", 403),
    ],
)
def test_local_browser_page_requires_its_bound_origin(
    tmp_path: Path, method: str, kind: str, status: int
) -> None:
    source = tmp_path / "index.html"
    source.write_text("private loopback fixture")
    page = _Page()
    browser_page.open_page(page, source, wait_ready=False)
    url = urlsplit(page.url)
    assert url.hostname is not None
    connection = HTTPConnection(url.hostname, url.port, timeout=10)
    try:
        connection.putrequest(method, url.path, skip_host=True)
        if kind != "missing-host":
            host = "attacker.example" if kind == "foreign-host" else url.netloc
            connection.putheader("Host", host)
            if kind == "duplicate-host":
                connection.putheader("Host", url.netloc)
        if kind in {"same-origin", "foreign-origin", "null-origin"}:
            origin = {
                "same-origin": f"http://{url.netloc}",
                "foreign-origin": "https://attacker.example",
                "null-origin": "null",
            }[kind]
            connection.putheader("Origin", origin)
        connection.endheaders()
        response = connection.getresponse()
        payload = response.read()
        assert response.status == status
        if method == "HEAD":
            assert payload == b""
        elif status == 200:
            assert payload == source.read_bytes()
        else:
            assert b"private loopback fixture" not in payload
    finally:
        connection.close()
        page.close()
