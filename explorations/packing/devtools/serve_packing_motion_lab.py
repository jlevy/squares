#!/usr/bin/env python3
"""Serve or replay the local numerical square-packing Motion Lab."""

from __future__ import annotations

import argparse
import json
import sys
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Never
from urllib.parse import parse_qs, urlsplit

from strif import atomic_output_file

from devtools.render_general_motion_lab import (
    DEFAULT_SEED,
    DEFAULT_SIDE,
    DEFAULT_SQUARE_COUNT,
    render_general_motion_lab,
)
from devtools.render_packing_motion_lab import render_motion_lab
from sqpack.motion_lab.contracts import (
    QuenchTrace,
    canonical_json,
    quench_request_from_record,
)
from sqpack.motion_lab.scenarios.free_quench import free_quench_scenario
from sqpack.motion_lab.trace import trace_quench_bracket

LOOPBACK_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
MAX_REQUEST_BYTES = 1_000_000
ERROR_CONTRACT = "packing.squares:MotionLabError/v1"
STATUS_CONTRACT = "packing.squares:MotionLabService/v1"
LIVE_CONTENT_SECURITY_POLICY = (
    "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; "
    "img-src data:; connect-src 'self'; object-src 'none'; base-uri 'none'; "
    "form-action 'none'; frame-ancestors 'none'"
)
EXACT_CONTENT_SECURITY_POLICY = LIVE_CONTENT_SECURITY_POLICY.replace(
    "connect-src 'self'", "connect-src 'none'"
)
DATA_CONTENT_SECURITY_POLICY = "default-src 'none'; frame-ancestors 'none'"


class HttpInputError(ValueError):
    """A permanent client error with its HTTP status and stable code."""

    def __init__(self, status: HTTPStatus, code: str, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.code = code


def _object_without_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _load_json_bytes(value: bytes) -> object:
    try:
        text = value.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError("request body must be UTF-8 JSON") from error
    return json.loads(text, object_pairs_hook=_object_without_duplicate_keys)


def _canonical_record_json(record: object) -> str:
    return (
        json.dumps(
            record,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n"
    )


def build_quench_trace(payload: object) -> QuenchTrace:
    """Validate one strict Phase 1 payload and run its declared quench exactly once."""
    request = quench_request_from_record(payload)
    return trace_quench_bracket(request)


def save_trace(path: Path, trace: QuenchTrace) -> None:
    """Atomically save the canonical trace bytes used by deterministic replay."""
    with atomic_output_file(path, make_parents=True) as temporary:
        temporary.write_text(canonical_json(trace), encoding="utf-8")


def replay_trace(path: Path) -> QuenchTrace:
    """Rerun a retained request and reject any semantic or byte-level trace drift."""
    record = _load_json_bytes(path.read_bytes())
    if not isinstance(record, dict) or record.get("contract") != QuenchTrace.CONTRACT:
        raise ValueError("retained Motion Lab trace has the wrong contract")
    request = record.get("request")
    regenerated = build_quench_trace(request)
    if _canonical_record_json(record) != canonical_json(regenerated):
        raise ValueError("retained Motion Lab trace differs from deterministic replay")
    return regenerated


def _error_record(code: str, message: str) -> dict[str, object]:
    return {
        "contract": ERROR_CONTRACT,
        "schema_version": 1,
        "error": {"code": code, "message": message},
    }


def _free_scenario_parameters(query: str) -> tuple[int, int, float]:
    parameters = parse_qs(query, keep_blank_values=True)
    unknown = sorted(set(parameters) - {"n", "seed", "side"})
    if unknown:
        raise ValueError(f"unknown scenario query field(s): {', '.join(unknown)}")
    for name, values in parameters.items():
        if len(values) != 1:
            raise ValueError(f"scenario query field {name!r} must occur exactly once")
        if not values[0]:
            raise ValueError(f"scenario query field {name!r} must not be empty")
    try:
        n = int(parameters.get("n", [str(DEFAULT_SQUARE_COUNT)])[0])
        seed = int(parameters.get("seed", [str(DEFAULT_SEED)])[0])
        side = float(parameters.get("side", [str(DEFAULT_SIDE)])[0])
    except ValueError as error:
        raise ValueError("n and seed must be integers; side must be a number") from error
    return n, seed, side


class MotionLabRequestHandler(BaseHTTPRequestHandler):
    """Same-origin HTTP adapter around the typed request and trace operations."""

    protocol_version = "HTTP/1.1"

    def _send_bytes(
        self,
        status: HTTPStatus,
        body: bytes,
        *,
        content_type: str,
        content_security_policy: str = DATA_CONTENT_SECURITY_POLICY,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", content_security_policy)
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, status: HTTPStatus, record: object) -> None:
        self._send_bytes(
            status,
            _canonical_record_json(record).encode("utf-8"),
            content_type="application/json; charset=utf-8",
        )

    def _read_json_request(self) -> object:
        if self.headers.get_content_type() != "application/json":
            raise HttpInputError(
                HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                "unsupported-media-type",
                "POST /api/quench requires Content-Type: application/json",
            )
        raw_length = self.headers.get("Content-Length")
        if raw_length is None:
            raise HttpInputError(
                HTTPStatus.LENGTH_REQUIRED,
                "length-required",
                "request must include Content-Length",
            )
        try:
            length = int(raw_length)
        except ValueError as error:
            raise HttpInputError(
                HTTPStatus.BAD_REQUEST,
                "invalid-content-length",
                "Content-Length must be a non-negative integer",
            ) from error
        if length < 0:
            raise HttpInputError(
                HTTPStatus.BAD_REQUEST,
                "invalid-content-length",
                "Content-Length must be a non-negative integer",
            )
        if length > MAX_REQUEST_BYTES:
            raise HttpInputError(
                HTTPStatus.CONTENT_TOO_LARGE,
                "request-too-large",
                f"request exceeds the {MAX_REQUEST_BYTES}-byte limit",
            )
        return _load_json_bytes(self.rfile.read(length))

    def do_GET(self) -> None:
        target = urlsplit(self.path)
        if target.path == "/api/status" and not target.query:
            self._send_json(
                HTTPStatus.OK,
                {
                    "contract": STATUS_CONTRACT,
                    "schema_version": 1,
                    "status": "ready",
                    "quench_endpoint": "/api/quench",
                    "scenario_endpoint": "/api/scenario/free-quench",
                    "network_scope": "loopback-only",
                },
            )
            return
        try:
            if target.path == "/":
                n, seed, side = _free_scenario_parameters(target.query)
                self._send_bytes(
                    HTTPStatus.OK,
                    render_general_motion_lab(n=n, seed=seed, side=side).encode(),
                    content_type="text/html; charset=utf-8",
                    content_security_policy=LIVE_CONTENT_SECURITY_POLICY,
                )
                return
            if target.path == "/exact-n5" and not target.query:
                self._send_bytes(
                    HTTPStatus.OK,
                    render_motion_lab().encode(),
                    content_type="text/html; charset=utf-8",
                    content_security_policy=EXACT_CONTENT_SECURITY_POLICY,
                )
                return
            if target.path == "/api/scenario/free-quench":
                n, seed, side = _free_scenario_parameters(target.query)
                self._send_json(
                    HTTPStatus.OK,
                    free_quench_scenario(n=n, seed=seed, side=side).to_record(),
                )
                return
        except (TypeError, ValueError) as error:
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                _error_record("invalid-scenario", str(error)),
            )
            return
        self._send_json(
            HTTPStatus.NOT_FOUND,
            _error_record("not-found", f"unknown Motion Lab route: {self.path}"),
        )

    def do_POST(self) -> None:
        if self.path != "/api/quench":
            self._send_json(
                HTTPStatus.NOT_FOUND,
                _error_record("not-found", f"unknown Motion Lab route: {self.path}"),
            )
            return
        try:
            payload = self._read_json_request()
            trace = build_quench_trace(payload)
        except HttpInputError as error:
            self._send_json(error.status, _error_record(error.code, str(error)))
            return
        except (json.JSONDecodeError, TypeError, ValueError) as error:
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                _error_record("invalid-request", str(error)),
            )
            return
        except Exception as error:
            self.log_error("numerical quench failed: %s", error)
            self._send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                _error_record(
                    "numerical-failure",
                    "numerical quench failed; inspect the local service log",
                ),
            )
            return
        self._send_json(HTTPStatus.OK, trace.to_record())


def create_server(*, port: int) -> ThreadingHTTPServer:
    """Bind the service to IPv4 loopback; callers cannot supply a remote host."""
    if isinstance(port, bool) or not isinstance(port, int) or not 0 <= port <= 65_535:
        raise ValueError("port must be an integer from 0 through 65535")
    return ThreadingHTTPServer((LOOPBACK_HOST, port), MotionLabRequestHandler)


def _path_json(path: Path) -> object:
    return _load_json_bytes(path.read_bytes())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    serve = commands.add_parser("serve", help="run the loopback numerical service")
    serve.add_argument("--port", type=int, default=DEFAULT_PORT)
    serve.add_argument(
        "--open", action="store_true", help="open the lab in the default browser"
    )
    run = commands.add_parser("run", help="run a saved QuenchRequest/v1")
    run.add_argument("--request", type=Path, required=True)
    run.add_argument("--output", type=Path, required=True)
    replay = commands.add_parser("replay", help="rerun and compare a saved QuenchTrace/v1")
    replay.add_argument("trace", type=Path)
    return parser.parse_args()


def _serve(args: argparse.Namespace) -> Never:
    server = create_server(port=args.port)
    address = server.server_address
    if not isinstance(address, tuple) or len(address) < 2:
        raise RuntimeError("loopback server returned an invalid address")
    url = f"http://{address[0]}:{address[1]}/"
    print(f"Motion Lab service listening at {url}")
    if args.open and not webbrowser.open(url):
        print(f"Browser did not open automatically; navigate to {url}", file=sys.stderr)
    try:
        server.serve_forever()
    finally:
        server.server_close()
    raise AssertionError("serve_forever returned unexpectedly")


def main() -> int:
    args = parse_args()
    try:
        if args.command == "serve":
            _serve(args)
        if args.command == "run":
            trace = build_quench_trace(_path_json(args.request))
            save_trace(args.output, trace)
            print(f"wrote {args.output} ({len(canonical_json(trace).encode())} bytes)")
            return 0
        if args.command == "replay":
            trace = replay_trace(args.trace)
            print(
                f"PASS: {args.trace} replays {len(trace.events)} events to "
                f"side {trace.result.side:.12g}"
            )
            return 0
        raise AssertionError(f"unknown command: {args.command}")
    except KeyboardInterrupt:
        print("Motion Lab service stopped", file=sys.stderr)
        return 130
    except (OSError, RuntimeError, TypeError, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
