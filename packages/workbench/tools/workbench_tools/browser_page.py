"""Load published workbench resources through a local HTTP origin."""

from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from typing import Any, cast

from workbench_tools.probes import probe


class _QuietHandler(SimpleHTTPRequestHandler):
    def _same_origin(self) -> bool:
        """A loopback bind alone does not prevent DNS rebinding or cross-origin reads."""
        server = cast(ThreadingHTTPServer, self.server)
        authority = f"127.0.0.1:{server.server_port}"
        origins = self.headers.get_all("Origin", [])
        if self.headers.get_all("Host", []) != [authority] or (
            origins and origins != [f"http://{authority}"]
        ):
            self.send_error(403, "Foreign Host or Origin")
            return False
        return True

    def do_GET(self) -> None:
        if self._same_origin():
            super().do_GET()

    def do_HEAD(self) -> None:
        if self._same_origin():
            super().do_HEAD()

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        pass


def open_page(
    page: Any, path: Path, *, wait_until: str = "load", wait_ready: bool = True
) -> None:
    """Keep the server alive through data loading and application initialization."""
    handler = partial(_QuietHandler, directory=str(path.resolve().parent))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    closed = False

    def close_server(*_: Any) -> None:
        nonlocal closed
        if not closed:
            closed = True
            server.shutdown()
            server.server_close()
            thread.join()

    page.on("close", close_server)
    try:
        page.goto(f"http://127.0.0.1:{server.server_port}/{path.name}", wait_until=wait_until)
        if wait_ready:
            page.wait_for_function(probe("policy/api-ready"), timeout=30_000)
    except BaseException:
        close_server()
        raise
