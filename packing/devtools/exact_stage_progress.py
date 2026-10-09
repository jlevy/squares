"""Bounded, fail-closed observations for a caller's cooperative exact-work clock.

This journal never supplies a scientific verdict or an admitted proof prefix.
It has no tracing, sampling thread, or background work. Callers must include
every call in their own deadline and propagate any observer failure.
"""

from __future__ import annotations

import copy
import math
import os
import tempfile
import time
from collections.abc import Callable
from functools import partial, wraps
from pathlib import Path
from typing import Any

from sqpack import retained_json

SCHEMA = "exact-stage-progress/v1"
BYTE_LIMIT = 1 << 20
STAGE_LIMIT = 512
COUNTER_LIMIT = 64
INTERVAL = 1.0


class JournalError(RuntimeError):
    """The observer failed; scientific work must stop without a verdict."""


class JournalIncompleteError(JournalError):
    """The caller's deadline or this observer's representation cap expired."""


def require(condition: bool, message: str) -> None:  # noqa: FBT001
    if not condition:
        raise JournalError(message)


def name(value: Any) -> str:
    require(
        type(value) is str
        and 0 < len(value) <= 64
        and value.isascii()
        and all(c.isalnum() or c in "_-" for c in value),
        "journal name must be bounded ASCII identifier",
    )
    return value


def integer(value: Any) -> int:
    require(type(value) is int and 0 <= value < 2**64, "journal counter must be unsigned64")
    return value


def read_clock(clock: Callable[[], float]) -> float:
    value = clock()
    require(
        type(value) in (int, float) and math.isfinite(value) and value >= 0,
        "journal clock observation must be finite and nonnegative",
    )
    return float(value)


def fail_closed[**P, T](method: Callable[P, T]) -> Callable[P, T]:
    @wraps(method)
    def call(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return method(*args, **kwargs)
        except JournalError:
            # This decorator is used only on bound StageProgress methods.
            instance: Any = args[0]
            instance.failed = True
            raise

    return call


class StageProgress:
    """Exclusive initial claim and atomic bounded snapshots in a supplied path.

    Counter limits are observations, not enforced proof-work ceilings: an
    over-limit counter is retained so an incomplete stop is understandable.
    Owner/row/context identifiers are metadata, never geometric coordinates.
    """

    def __init__(
        self,
        output: Path,
        *,
        deadline: float,
        counter_limits: dict[str, int],
        clock: Callable[[], float] = time.monotonic,
        cpu_clock: Callable[[], float] = time.process_time,
    ) -> None:
        require(
            type(deadline) in (int, float) and math.isfinite(deadline),
            "journal deadline must be finite",
        )
        require(
            type(counter_limits) is dict and len(counter_limits) <= COUNTER_LIMIT,
            "journal counter roster exceeds representation limit",
        )
        self.output, self.deadline = output, deadline
        self.clock, self.cpu_clock = partial(read_clock, clock), partial(read_clock, cpu_clock)
        self.started, self.cpu_started = self.clock(), self.cpu_clock()
        self._tick()
        self.limits = {name(k): integer(v) for k, v in counter_limits.items()}
        self.counters = dict.fromkeys(self.limits, 0)
        self.events: list[dict[str, Any]] = []
        self.current: dict[str, Any] | None = None
        self.status, self.reason = "initialized", None
        self.last_write = self.started
        self.io_wall = self.io_cpu = 0.0
        self.writes = 0
        self.failed = self.finished = False
        self._write(initial=True)

    def _tick(self) -> None:
        if self.clock() >= self.deadline:
            raise JournalIncompleteError("journal caller wall ceiling")

    def _active(self) -> None:
        require(not self.failed and not self.finished, "journal already failed or finished")
        self._tick()

    def _counts(self, counters: dict[str, int]) -> None:
        require(type(counters) is dict, "journal counters must be a mapping")
        require(set(counters) <= set(self.limits), "journal counter roster changed")
        updates = {name(k): integer(v) for k, v in counters.items()}
        require(
            all(v >= self.counters[k] for k, v in updates.items()),
            "journal cumulative counter decreased",
        )
        self.counters.update(updates)

    def snapshot(self) -> dict[str, Any]:
        return copy.deepcopy(
            {
                "schema": SCHEMA,
                "status": self.status,
                "reason": self.reason,
                "elapsed_wall_seconds": self.clock() - self.started,
                "elapsed_cpu_seconds": self.cpu_clock() - self.cpu_started,
                "counter_limits": self.limits,
                "counters": self.counters,
                "completed_stages": self.events,
                "current_stage": self.current,
                "observer_io_through_previous_write": {
                    "writes": self.writes,
                    "wall_seconds": self.io_wall,
                    "cpu_seconds": self.io_cpu,
                },
                "observer_failure_policy": "fail_closed",
                "scientific_verdict_supplied": False,
                "proof_prefix_admitted": False,
                "rss_measured": False,
                "outer_supervisor_authoritative": True,
                "timings_in_mathematical_payload": False,
            }
        )

    def _write(self, *, initial: bool = False) -> None:
        self._tick()
        start, cpu_start = self.clock(), self.cpu_clock()
        temp: Path | None = None
        try:
            raw = retained_json.dumps(self.snapshot(), sort_keys=True).encode()
            if len(raw) > BYTE_LIMIT:
                raise JournalIncompleteError("journal byte ceiling")
            self._tick()
            if initial:
                # Parent creation is caller-owned; no implicit storage fallback.
                fd = os.open(self.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                with os.fdopen(fd, "wb") as handle:
                    handle.write(raw)
                    handle.flush()
            else:
                with tempfile.NamedTemporaryFile(
                    mode="wb", dir=self.output.parent, prefix=".stage-progress-", delete=False
                ) as handle:
                    temp = Path(handle.name)
                    handle.write(raw)
                    handle.flush()
                self._tick()
                temp.replace(self.output)
                temp = None
            self.io_wall += self.clock() - start
            self.io_cpu += self.cpu_clock() - cpu_start
            self.writes += 1
            self.last_write = self.clock()
            self._tick()
        except (JournalError, OSError) as exc:
            self.failed = True
            if isinstance(exc, JournalError):
                raise
            raise JournalError(f"journal metadata I/O failed: {exc}") from exc
        finally:
            if temp is not None:
                temp.unlink(missing_ok=True)

    @fail_closed
    def stage(self, stage: str, *, location: dict[str, int] | None = None) -> None:
        self._active()
        require(self.current is None, "finish current journal stage before starting next")
        if len(self.events) >= STAGE_LIMIT:
            raise JournalIncompleteError("journal stage ceiling")
        identifiers = {} if location is None else location
        require(
            type(identifiers) is dict and set(identifiers) <= {"owner", "row", "context"},
            "journal stage location fields differ",
        )
        self.current = {
            "name": name(stage),
            "location": {k: integer(v) for k, v in identifiers.items()},
            "started_wall_seconds": self.clock() - self.started,
            "started_cpu_seconds": self.cpu_clock() - self.cpu_started,
        }
        self.status = "running"
        self._write()

    @fail_closed
    def checkpoint(self, counters: dict[str, int]) -> bool:
        self._active()
        require(self.current is not None, "journal checkpoint needs an active stage")
        self._counts(counters)
        if self.clock() - self.last_write < INTERVAL:
            return False
        self._write()
        return True

    @fail_closed
    def end_stage(self, counters: dict[str, int]) -> None:
        self._active()
        require(self.current is not None, "journal has no active stage")
        self._counts(counters)
        event = copy.deepcopy(self.current)
        assert event is not None
        event["ended_wall_seconds"] = self.clock() - self.started
        event["ended_cpu_seconds"] = self.cpu_clock() - self.cpu_started
        event["counters"] = dict(self.counters)
        self.events.append(event)
        self.current = None
        self._write()

    @fail_closed
    def finish(self, status: str, *, reason: str | None = None) -> None:
        self._active()
        require(status in {"observations_complete", "incomplete", "refused"}, "journal status")
        require(
            reason is None or (type(reason) is str and reason.isascii() and len(reason) <= 512),
            "journal reason exceeds bounded metadata shape",
        )
        require(
            status != "observations_complete" or self.current is None,
            "unfinished stage cannot produce complete observations",
        )
        self.status, self.reason = status, reason
        self._write()
        self.finished = True
