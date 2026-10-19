"""Tiny diagnostic protocol controls; no atlas, geometry or native work is executed."""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context
from pathlib import Path
from typing import Any

import pytest

from sqpack import atlas_trace as trace


@pytest.fixture(autouse=True)
def isolated_trace(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    trace.install_context(None)
    monkeypatch.delenv(trace.ENABLED, raising=False)
    yield
    trace.install_context(None)


def enable(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setenv(trace.ENABLED, "1")
    monkeypatch.setenv("PACKING_VALIDATION_ARTIFACT_DIR", str(tmp_path))
    monkeypatch.setenv(
        "PACKING_REACHABLE_TEST_ARTIFACT_STEM", str(tmp_path / "command-one.pytest-pool")
    )
    monkeypatch.setenv("PACKING_REACHABLE_TEST_RUN_ID", "run-one")
    monkeypatch.setenv("PACKING_REACHABLE_TEST_SOURCE_COMMIT", "a" * 40)
    return tmp_path / f"command-one.pytest-pool.atlas-{os.getpid()}.jsonl"


def rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def test_disabled_trace_does_no_io(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("disabled tracing touched the filesystem")

    monkeypatch.setattr(Path, "open", forbidden)
    monkeypatch.setattr(Path, "resolve", forbidden)

    @trace.composite_test
    def work(value: int) -> int:
        with trace.case(3, "synthetic"), trace.phase("work"):
            trace.cache_snapshot("cache", 2, {"hits": 0, "misses": 1})
            return value + 1

    assert work(4) == 5
    assert trace.current_context() is None


def test_events_flush_case_cache_and_preserve_exception(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = enable(tmp_path, monkeypatch)
    error = ValueError("original result failure")

    def failing_work() -> None:
        with trace.session(), trace.case(7, "packet-derived-facts"):
            trace.cache_snapshot("corpus", 2, {"hits": 1, "misses": 1, "maxsize": None})
            with trace.phase("native", source="T-174"):
                # The start survives an unfinished call, before any context exits.
                assert rows(path)[-1]["stage"] == "native"
                assert rows(path)[-1]["event"] == "start"
                raise error

    with pytest.raises(ValueError, match="original result failure") as caught:
        failing_work()
    assert caught.value is error
    events = rows(path)
    assert [r["event"] for r in events][-3:] == ["error", "error", "error"]
    native = next(r for r in events if r["stage"] == "native" and r["event"] == "start")
    assert (native["n"], native["source_kind"], native["source"]) == (
        7,
        "packet-derived-facts",
        "T-174",
    )
    cache = next(r for r in events if r["event"] == "cache")
    assert cache["cache_key"] == 2
    assert cache["cache_info"]["hits"] == 1
    assert all(r["pid"] == os.getpid() and r["source_commit"] == "a" * 40 for r in events)
    assert all(r["wall_ns"] >= 0 and r["cpu_ns"] >= 0 for r in events if r["event"] == "error")


@pytest.mark.pool_heavy
def test_context_is_picklable_and_explicitly_installed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = enable(tmp_path, monkeypatch)
    monkeypatch.delenv("PACKING_VALIDATION_ARTIFACT_DIR")
    with trace.session():
        context = trace.current_context()
        with ProcessPoolExecutor(
            max_workers=1,
            mp_context=get_context("spawn"),
            initializer=trace.install_context,
            initargs=(context,),
        ) as pool:
            child_pid = pool.submit(synthetic_case).result(timeout=5)
    # A child receives this value through a module-level pool initializer, including
    # when a fork server existed before the parent enabled this test's trace.
    child_path = path.with_name(f"command-one.pytest-pool.atlas-{child_pid}.jsonl")
    assert child_pid != os.getpid()
    assert rows(child_path)[0]["n"] == 9
    assert rows(child_path)[0]["event"] == "start"
    assert path.read_bytes() != child_path.read_bytes()


def synthetic_case() -> int:
    """A module-level pool unit, without importing any application geometry."""
    with trace.case(9, "synthetic"):
        pass
    return os.getpid()


def test_exclusive_writer_never_overwrites_partial_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    path = enable(tmp_path, monkeypatch)
    path.write_text("retained partial evidence\n")
    with trace.session(), trace.phase("work"):
        result = 17
    assert result == 17
    assert path.read_text() == "retained partial evidence\n"
    assert "Atlas trace disabled" in caplog.text


@pytest.mark.parametrize("limit", ["MAX_EVENTS", "MAX_BYTES", "MAX_ROW_BYTES"])
def test_trace_bounds_are_explicit_and_leave_valid_partial_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, limit: str
) -> None:
    path = enable(tmp_path, monkeypatch)
    monkeypatch.setattr(
        trace, limit, {"MAX_EVENTS": 4, "MAX_BYTES": 900, "MAX_ROW_BYTES": 100}[limit]
    )
    with trace.session():
        for _ in range(12):
            with trace.phase("synthetic"):
                pass
    events = rows(path)
    assert events[-1]["event"] == "truncated"
    assert len(events) <= trace.MAX_EVENTS
    assert path.stat().st_size <= trace.MAX_BYTES
    assert all(len(line) + 1 <= trace.MAX_ROW_BYTES for line in path.read_bytes().splitlines())


def test_destination_cannot_escape_existing_artifact_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = enable(tmp_path, monkeypatch)
    monkeypatch.setenv("PACKING_REACHABLE_TEST_ARTIFACT_STEM", str(tmp_path.parent / "escape"))
    with pytest.raises(ValueError, match="artifact directory/stem"), trace.session():
        raise AssertionError("invalid destination admitted work")
    assert not path.exists()
