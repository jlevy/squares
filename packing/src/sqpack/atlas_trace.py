"""Opt-in, bounded atlas diagnostics in an existing validation artifact context.

Set PACKING_ATLAS_TRACE=1 for the composite test. The validation runner supplies the
artifact directory, command stem, run ID and source identity; tracing chooses no other
destination and never reads Git. Every process owns an exclusive, immediately flushed
JSONL file. Disabled tracing performs no I/O. Stack sampling is deliberately separate:
this tool does not install process-wide signal handlers or change runtime deadlines.
"""

from __future__ import annotations

import json
import logging
import os
import re
import time
from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from functools import wraps
from pathlib import Path

ENABLED = "PACKING_ATLAS_TRACE"
MAX_EVENTS = 10_000
MAX_BYTES = 4 * 1024 * 1024
MAX_ROW_BYTES = 8192
SCHEMA = "atlas-trace-v1"
_TOKEN = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.-]{0,191}\Z")


@dataclass(frozen=True)
class TraceContext:
    """Picklable validation context explicitly installed in pool children."""

    directory: Path
    stem: str
    run_id: str
    source_commit: str


class _Writer:
    def __init__(self, context: TraceContext) -> None:
        self.pid = os.getpid()
        self.context = context
        self.events = 0
        self.bytes = 0
        self.full = False
        self.stream = (context.directory / f"{context.stem}.atlas-{self.pid}.jsonl").open("xb")

    def emit(self, row: Mapping[str, object]) -> None:
        if self.full:
            return
        data = (json.dumps(row, sort_keys=True) + "\n").encode()
        reason = (
            "row_limit"
            if len(data) > MAX_ROW_BYTES
            else "event_limit"
            if self.events + 1 >= MAX_EVENTS
            else "byte_limit"
            if self.bytes + len(data) + 128 > MAX_BYTES
            else ""
        )
        if reason:
            self.full = True
            data = (
                json.dumps({"schema": SCHEMA, "event": "truncated", "reason": reason}) + "\n"
            ).encode()
        if self.events >= MAX_EVENTS or self.bytes + len(data) > MAX_BYTES:
            return
        self.stream.write(data)
        self.stream.flush()
        self.events += 1
        self.bytes += len(data)

    def close(self) -> None:
        self.stream.close()


@dataclass
class _ProcessState:
    context: TraceContext | None = None
    writer: _Writer | None = None
    case: tuple[int, str] | None = None
    failed: bool = False


_state = _ProcessState()


def current_context() -> TraceContext | None:
    """Return the active context for explicit pool initialization, or None."""
    return _state.context


def install_context(context: TraceContext | None) -> None:
    """Install inherited context without opening a file or retaining a parent's FD."""
    if _state.writer is not None:
        try:
            _state.writer.close()
        except OSError as error:
            logging.getLogger(__name__).warning("Atlas trace close failed: %s", error)
    _state.context, _state.writer, _state.case, _state.failed = context, None, None, False


def _environment_context() -> TraceContext:
    stem = Path(os.environ["PACKING_REACHABLE_TEST_ARTIFACT_STEM"])
    # The runner strips its parent configuration from pytest, leaving this existing
    # child stem and its source/run context. Never create an alternative directory.
    directory = Path(os.environ.get("PACKING_VALIDATION_ARTIFACT_DIR", str(stem.parent)))
    if (
        not stem.is_absolute()
        or not directory.is_absolute()
        or directory.is_symlink()
        or not directory.is_dir()
        or stem.parent.resolve() != directory.resolve()
        or _TOKEN.fullmatch(stem.name) is None
    ):
        raise ValueError("atlas trace requires the existing validation artifact directory/stem")
    run_id = os.environ["PACKING_REACHABLE_TEST_RUN_ID"]
    source = os.environ["PACKING_REACHABLE_TEST_SOURCE_COMMIT"]
    if _TOKEN.fullmatch(run_id) is None or re.fullmatch(r"[0-9a-f]{40}", source) is None:
        raise ValueError("atlas trace requires the validation run and source identity")
    return TraceContext(directory.resolve(), stem.name, run_id, source)


def _emit(event: str, stage: str, **fields: object) -> None:
    if _state.context is None or _state.failed:
        return
    try:
        if _state.writer is None or _state.writer.pid != os.getpid():
            if _state.writer is not None:
                _state.writer.close()
            _state.writer = _Writer(_state.context)
        row: dict[str, object] = {
            "schema": SCHEMA,
            "event": event,
            "stage": stage,
            "pid": os.getpid(),
            "worker_id": os.environ.get("PYTEST_XDIST_WORKER", "main"),
            "run_id": _state.context.run_id,
            "source_commit": _state.context.source_commit,
            "command_id": _state.context.stem,
            "monotonic_ns": time.monotonic_ns(),
            "process_cpu_ns": time.process_time_ns(),
            **fields,
        }
        if _state.case is not None:
            row.update(n=_state.case[0], source_kind=_state.case[1])
        _state.writer.emit(row)
    except (OSError, TypeError, ValueError) as error:
        # Diagnostics must not replace the result or exception of the checked work.
        _state.failed = True
        logging.getLogger(__name__).warning("Atlas trace disabled after I/O failure: %s", error)


@contextmanager
def session() -> Iterator[None]:
    """Trace only the named composite test, and close its writer even on failure."""
    if os.environ.get(ENABLED) != "1" or _state.context is not None:
        yield
        return
    install_context(_environment_context())
    try:
        with phase("composite.test"):
            yield
    finally:
        install_context(None)


def composite_test[**P, R](function: Callable[P, R]) -> Callable[P, R]:
    """Keep pytest's original signature while scoping opt-in context to this test."""

    @wraps(function)
    def traced(*args: P.args, **kwargs: P.kwargs) -> R:
        with session():
            return function(*args, **kwargs)

    return traced


@contextmanager
def phase(
    stage: str,
    *,
    source: str = "",
    workers: int | None = None,
    n: int | None = None,
) -> Iterator[None]:
    """Record a stage without changing its returned value or propagated exception."""
    if _state.context is None:
        yield
        return
    wall, cpu = time.monotonic_ns(), time.process_time_ns()
    fields: dict[str, object] = {"source": source, "workers": workers}
    if n is not None:
        fields["n"] = n
    _emit("start", stage, **fields)
    try:
        yield
    except BaseException as error:
        _emit(
            "error",
            stage,
            error_type=type(error).__name__,
            wall_ns=time.monotonic_ns() - wall,
            cpu_ns=time.process_time_ns() - cpu,
            **fields,
        )
        raise
    else:
        _emit(
            "finish",
            stage,
            wall_ns=time.monotonic_ns() - wall,
            cpu_ns=time.process_time_ns() - cpu,
            **fields,
        )


@contextmanager
def case(n: int, source_kind: str) -> Iterator[None]:
    """Attach one pool unit's identity to its nested stage events."""
    previous = _state.case
    if _state.context is not None:
        _state.case = n, source_kind
    try:
        with phase("case"):
            yield
    finally:
        _state.case = previous


def cache_snapshot(name: str, key: object, info: Mapping[str, int | None]) -> None:
    """Observe existing cache counters without touching their keys or contents."""
    _emit("cache", name, cache_key=key, cache_info=dict(info))
