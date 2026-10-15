"""Flushed per-worker progress for a reachable-tests child pytest invocation.

The controller does not write xdist events. Each worker owns one exclusive-create JSONL
file, so a terminated test leaves its last start row readable without waiting for JUnit.
"""

from __future__ import annotations

import json
import os
import re
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import TextIO

import pytest

ARTIFACT_STEM = "PACKING_REACHABLE_TEST_ARTIFACT_STEM"
RUN_ID = "PACKING_REACHABLE_TEST_RUN_ID"
SOURCE_COMMIT = "PACKING_REACHABLE_TEST_SOURCE_COMMIT"
WORKERS = "PACKING_REACHABLE_TEST_WORKERS"
SCHEMA = "reachable-progress-v1"


class ProgressWriter:
    """One serial runner or xdist worker, with one append-only progress stream."""

    def __init__(
        self,
        stem: Path,
        *,
        worker_id: str,
        run_id: str,
        source_commit: str,
        workers: int,
    ) -> None:
        if re.fullmatch(r"[A-Za-z0-9_-]+", worker_id) is None:
            raise pytest.UsageError(f"invalid pytest worker id: {worker_id!r}")
        self.worker_id = worker_id
        self.run_id = run_id
        self.source_commit = source_commit
        self.workers = workers
        self.pack_jobs = os.environ.get("PACK_JOBS", "")
        self.lane = os.environ.get("PACKING_REACHABLE_TEST_LANE", "unspecified")
        self.marker = os.environ.get("PACKING_REACHABLE_TEST_MARKER", "")
        self.exclusions = os.environ.get("PACKING_REACHABLE_TEST_EXCLUSIONS", "unspecified")
        self.command_id = stem.name
        target = Path(f"{stem}.progress-{worker_id}.jsonl")
        target.parent.mkdir(parents=True, exist_ok=True)
        self.stream: TextIO = target.open("x", encoding="utf-8")
        self.outcomes: dict[str, str] = {}
        self._emit("session_start", "")

    def _emit(
        self,
        event: str,
        nodeid: str,
        *,
        outcome: str | None = None,
        exit_status: int | None = None,
    ) -> None:
        row: dict[str, str | int] = {
            "schema": SCHEMA,
            "event": event,
            "run_id": self.run_id,
            "command_id": self.command_id,
            "source_commit": self.source_commit,
            "worker_id": self.worker_id,
            "nodeid": nodeid,
            "timestamp_utc": datetime.now(UTC).isoformat(),
            "monotonic_ns": time.monotonic_ns(),
            "pack_jobs": self.pack_jobs,
            "lane": self.lane,
            "marker": self.marker,
            "exclusions": self.exclusions,
            "xdist_workers": self.workers,
        }
        if outcome is not None:
            row["outcome"] = outcome
        if exit_status is not None:
            row["exit_status"] = exit_status
        self.stream.write(json.dumps(row, sort_keys=True) + "\n")
        self.stream.flush()

    def pytest_runtest_logstart(self, nodeid: str, location: tuple[str, int, str]) -> None:
        del location
        self.outcomes[nodeid] = "passed"
        self._emit("start", nodeid)

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        nodeid = report.nodeid
        if report.failed:
            self.outcomes[nodeid] = "failed"
        elif report.skipped and self.outcomes.get(nodeid) != "failed":
            self.outcomes[nodeid] = "skipped"
        if report.when == "teardown":
            self._emit("finish", nodeid, outcome=self.outcomes.pop(nodeid, report.outcome))

    def pytest_sessionfinish(self, exitstatus: int | pytest.ExitCode) -> None:
        self._emit("session_finish", "", exit_status=int(exitstatus))
        self.stream.close()


def pytest_configure(config: pytest.Config) -> None:
    stem_value = os.environ.get(ARTIFACT_STEM)
    if not stem_value:
        return
    worker_input = getattr(config, "workerinput", None)
    if worker_input is None and config.getoption("numprocesses", default=0):
        return  # xdist controller: workers write separate files
    worker_id = str(worker_input["workerid"]) if worker_input is not None else "main"
    stem = Path(stem_value)
    if not stem.is_absolute():
        raise pytest.UsageError(f"{ARTIFACT_STEM} must be absolute")
    run_id = os.environ.get(RUN_ID, "")
    source_commit = os.environ.get(SOURCE_COMMIT, "")
    workers_value = os.environ.get(WORKERS, "")
    if not run_id or re.fullmatch(r"[0-9a-f]{40}", source_commit) is None:
        raise pytest.UsageError("reachable progress needs a run id and 40-hex source commit")
    try:
        workers = int(workers_value)
    except ValueError as error:
        raise pytest.UsageError("reachable progress needs its worker count") from error
    if workers < 1:
        raise pytest.UsageError("reachable progress worker count must be positive")
    config.pluginmanager.register(
        ProgressWriter(
            stem,
            worker_id=worker_id,
            run_id=run_id,
            source_commit=source_commit,
            workers=workers,
        ),
        "reachable-progress-writer",
    )
