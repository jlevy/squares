"""Supervised resident Rust area backend for the exact rectangle verifier.

The Rust child computes only exact weighted polygon integrals. Python still
admits the candidate, chooses the centre boxes, and owns every proof decision.
"""

from __future__ import annotations

import hashlib
import json
import os
import select
import signal
import subprocess
import tempfile
import time
from contextlib import suppress
from fractions import Fraction
from pathlib import Path
from types import TracebackType
from typing import TYPE_CHECKING, Any, NoReturn, Self

if TYPE_CHECKING:
    from sqpack.rectangle_density import DensityRectangle, Polygon

MAX_BINARY_BYTES = 64 * 1024 * 1024
MAX_REQUEST_BYTES = 64 * 1024 * 1024
MAX_RESPONSE_BYTES = 1024 * 1024


class RustGeometryError(ValueError):
    """The resident geometry child failed its exact protocol contract."""


class RustGeometryTimeoutError(TimeoutError):
    """The parent deadline interrupted a complete geometry response."""


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise RustGeometryError(f"duplicate Rust response key: {key}")
        result[key] = value
    return result


def _refuse_number(token: str) -> None:
    raise RustGeometryError(f"unexpected Rust response number: {token}")


def _fail(message: str) -> NoReturn:
    raise RustGeometryError(message)


def _json_object(raw: bytes) -> dict[str, Any]:
    try:
        value = json.loads(
            raw,
            object_pairs_hook=_pairs,
            parse_float=_refuse_number,
            parse_constant=_refuse_number,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RustGeometryError(f"malformed Rust response: {error}") from error
    if not isinstance(value, dict):
        raise RustGeometryError("Rust response must be a JSON object")
    return value


def _encode(value: object) -> bytes:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("ascii")
    if len(payload) > MAX_REQUEST_BYTES:
        raise RustGeometryError("Rust geometry request exceeds the byte limit")
    return payload


class RustRectangleGeometry:
    """Hold one immutable Rust process for one admitted candidate verification."""

    def __init__(
        self,
        rectangles: tuple[DensityRectangle, ...],
        binary: Path,
        *,
        deadline: float,
    ) -> None:
        self.deadline = deadline
        self._sequence = 0
        self._buffer = bytearray()
        self._process: subprocess.Popen[bytes] | None = None
        self._snapshot: tempfile.TemporaryDirectory[str] | None = None
        with binary.resolve(strict=True).open("rb") as source_file:
            source = source_file.read(MAX_BINARY_BYTES + 1)
        if not source or len(source) > MAX_BINARY_BYTES:
            raise RustGeometryError("Rust binary is empty or exceeds the byte limit")
        # The bytes read here are the bytes that run: they are written once into a
        # private snapshot and the child is started from it, so a rebuild of `binary`
        # mid-run cannot reach this verification. The binary is a build product with no
        # Git revision, so this digest is its name in the report (a cache identity,
        # OR-16), recorded and never compared.
        self.binary_sha256 = hashlib.sha256(source).hexdigest()
        opening = _encode(
            {
                "version": 1,
                "rectangles": [
                    {
                        "left": str(rectangle.left),
                        "bottom": str(rectangle.bottom),
                        "right": str(rectangle.right),
                        "top": str(rectangle.top),
                        "density": str(rectangle.density),
                    }
                    for rectangle in rectangles
                ],
            }
        )
        self.table_sha256 = hashlib.sha256(opening).hexdigest()
        try:
            self._check_deadline()
            self._snapshot = tempfile.TemporaryDirectory(prefix="sqverify-exact-")
            executable = Path(self._snapshot.name) / "sqverify-exact"
            executable.write_bytes(source)
            executable.chmod(0o700)
            self._process = subprocess.Popen(
                [str(executable), "--serve"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            if self._process.stdin is None or self._process.stdout is None:
                _fail("Rust process has no protocol pipes")
            os.set_blocking(self._process.stdin.fileno(), False)
            os.set_blocking(self._process.stdout.fileno(), False)
            self._write_line(opening)
            ready = _json_object(self._read_line())
            if (
                set(ready) != {"version", "status", "table_sha256", "rectangle_count"}
                or type(ready["version"]) is not int
                or ready["version"] != 1
                or ready["status"] != "ready"
                or ready["table_sha256"] != self.table_sha256
                or type(ready["rectangle_count"]) is not int
                or ready["rectangle_count"] != len(rectangles)
            ):
                _fail("Rust readiness did not bind the admitted table")
        except BaseException:
            self._stop(force=True)
            raise

    def _check_deadline(self) -> float:
        remaining = self.deadline - time.monotonic()
        if remaining <= 0:
            raise RustGeometryTimeoutError("Rust geometry exceeded the verifier deadline")
        return remaining

    def _write_line(self, payload: bytes) -> None:
        process = self._process
        if process is None or process.stdin is None:
            raise RustGeometryError("Rust process is unavailable")
        data = payload + b"\n"
        offset = 0
        while offset < len(data):
            _, writable, _ = select.select(
                [], [process.stdin.fileno()], [], self._check_deadline()
            )
            if not writable:
                raise RustGeometryTimeoutError(
                    "Rust geometry write exceeded the verifier deadline"
                )
            try:
                written = os.write(process.stdin.fileno(), data[offset:])
            except (BrokenPipeError, OSError) as error:
                raise RustGeometryError(f"Rust process closed its input: {error}") from error
            if written <= 0:
                raise RustGeometryError("Rust process made no input progress")
            offset += written

    def _read_line(self) -> bytes:
        process = self._process
        if process is None or process.stdout is None:
            raise RustGeometryError("Rust process is unavailable")
        while True:
            newline = self._buffer.find(b"\n")
            if newline >= 0:
                if newline > MAX_RESPONSE_BYTES:
                    raise RustGeometryError("Rust response exceeds the byte limit")
                line = bytes(self._buffer[:newline])
                del self._buffer[: newline + 1]
                self._check_deadline()
                return line
            if len(self._buffer) > MAX_RESPONSE_BYTES:
                raise RustGeometryError("Rust response exceeds the byte limit")
            readable, _, _ = select.select(
                [process.stdout.fileno()], [], [], self._check_deadline()
            )
            if not readable:
                raise RustGeometryTimeoutError("Rust response exceeded the verifier deadline")
            try:
                chunk = os.read(process.stdout.fileno(), 8192)
            except OSError as error:
                raise RustGeometryError(f"cannot read Rust response: {error}") from error
            if not chunk:
                raise RustGeometryError("Rust process ended before a complete response")
            self._buffer.extend(chunk)
            if len(self._buffer) > MAX_RESPONSE_BYTES + 1 and b"\n" not in self._buffer:
                raise RustGeometryError("Rust response exceeds the byte limit")

    def coverages(self, polygons: tuple[Polygon, ...]) -> tuple[Fraction, ...]:
        """Return all exact integrals or fail without using a partial response."""
        if not polygons:
            raise RustGeometryError("Rust query requires at least one polygon")
        request = _encode(
            {
                "version": 1,
                "sequence": self._sequence,
                "table_sha256": self.table_sha256,
                "polygons": [[[str(x), str(y)] for x, y in polygon] for polygon in polygons],
            }
        )
        self._write_line(request)
        response = _json_object(self._read_line())
        if (
            set(response) != {"version", "sequence", "table_sha256", "coverages"}
            or type(response["version"]) is not int
            or response["version"] != 1
            or type(response["sequence"]) is not int
            or response["sequence"] != self._sequence
            or response["table_sha256"] != self.table_sha256
            or not isinstance(response["coverages"], list)
            or len(response["coverages"]) != len(polygons)
            or not all(type(value) is str for value in response["coverages"])
        ):
            raise RustGeometryError("Rust response identity or result count changed")
        try:
            values = tuple(Fraction(value) for value in response["coverages"])
        except (ValueError, ZeroDivisionError) as error:
            raise RustGeometryError(
                "Rust response contains an invalid exact rational"
            ) from error
        if any(value < 0 for value in values):
            raise RustGeometryError("Rust response contains a negative area integral")
        self._check_deadline()
        self._sequence += 1
        return values

    def coverage(self, polygon: Polygon) -> Fraction:
        """Return one exact integral; an empty polygon has zero area."""
        return Fraction() if not polygon else self.coverages((polygon,))[0]

    def _stop(self, *, force: bool) -> None:
        process = self._process
        self._process = None
        try:
            if process is not None:
                if process.stdin is not None:
                    process.stdin.close()
                if force and process.poll() is None:
                    with suppress(ProcessLookupError):
                        os.killpg(process.pid, signal.SIGKILL)
                try:
                    process.wait(timeout=1 if force else self._check_deadline())
                except subprocess.TimeoutExpired:
                    if process.poll() is None:
                        with suppress(ProcessLookupError):
                            os.killpg(process.pid, signal.SIGKILL)
                    process.wait(timeout=1)
                if process.stdout is not None:
                    process.stdout.close()
                if process.stderr is not None:
                    process.stderr.close()
        finally:
            if self._snapshot is not None:
                self._snapshot.cleanup()
                self._snapshot = None

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        error_type: type[BaseException] | None,
        error: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        process = self._process
        if process is None:
            return
        if error_type is not None:
            self._stop(force=True)
            return
        try:
            self._check_deadline()
            if process.stdin is None or process.stdout is None:
                raise RustGeometryError("Rust protocol pipes disappeared")
            process.stdin.close()
            while True:
                if self._buffer:
                    raise RustGeometryError("Rust process emitted unsolicited output")
                readable, _, _ = select.select(
                    [process.stdout.fileno()], [], [], self._check_deadline()
                )
                if not readable:
                    raise RustGeometryTimeoutError(
                        "Rust shutdown exceeded the verifier deadline"
                    )
                chunk = os.read(process.stdout.fileno(), 8192)
                if not chunk:
                    break
                raise RustGeometryError("Rust process emitted unsolicited output")
            try:
                process.wait(timeout=self._check_deadline())
            except subprocess.TimeoutExpired as wait_error:
                raise RustGeometryTimeoutError(
                    "Rust shutdown exceeded the verifier deadline"
                ) from wait_error
            if process.returncode != 0:
                raise RustGeometryError("Rust process exited unsuccessfully")
            self._check_deadline()
        finally:
            self._stop(force=True)
