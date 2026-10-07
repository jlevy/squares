"""Run frozen argument arrays sequentially and retain partial execution evidence.

This runner does not interpret scientific results or retry a failed phase. The
external supervisor owns combined wall/RSS limits and process-group cleanup.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, TextIO, cast

from sqpack import retained_json

SCHEMA = "registered-phase-execution/v1"
PLAN_LIMIT = 10 << 20
PHASE_LIMIT = 64
OUTPUT_LIMIT = 64 << 20


def require(condition: bool, message: str) -> None:  # noqa: FBT001
    if not condition:
        raise ValueError(message)


def utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate execution-plan member")
        result[key] = value
    return result


def nonfinite(_token: str) -> Any:
    raise ValueError("nonfinite execution-plan number")


def validate(plan: Any) -> list[dict[str, Any]]:
    """Other manifest metadata is retained by its byte identity, not executed."""

    def finite_tree(value: Any) -> None:
        if type(value) is float:
            require(math.isfinite(value), "nonfinite execution-plan number")
        elif type(value) is list:
            for item in value:
                finite_tree(item)
        elif type(value) is dict:
            for item in value.values():
                finite_tree(item)

    finite_tree(plan)
    require(type(plan) is dict, "execution plan object required")
    phases = plan.get("phases")
    require(
        type(phases) is list and 1 <= len(phases) <= PHASE_LIMIT,
        "bounded nonempty phases required",
    )
    names = set()
    for phase in phases:
        require(
            type(phase) is dict and set(phase) == {"name", "argv"},
            "phase fields must be name/argv",
        )
        phase = cast(dict[str, Any], phase)
        name, argv = phase["name"], phase["argv"]
        require(
            type(name) is str and bool(name) and len(name) <= 128 and name not in names,
            "unique nonempty phase name required",
        )
        require(
            type(argv) is list
            and bool(argv)
            and all(type(token) is str and "\0" not in token for token in argv)
            and bool(argv[0]),
            "phase argv must be an explicit nonempty string array",
        )
        names.add(name)
    return copy.deepcopy(phases)


def load_plan(path: Path) -> tuple[bytes, list[dict[str, Any]]]:
    with path.open("rb") as stream:
        raw = stream.read(PLAN_LIMIT + 1)
    require(len(raw) <= PLAN_LIMIT, "execution plan byte ceiling")
    plan = json.loads(raw, object_pairs_hook=unique, parse_constant=nonfinite)
    return raw, validate(plan)


def write_report(stream: TextIO, report: dict[str, Any]) -> None:
    text = retained_json.dumps(report, sort_keys=True) + "\n"
    require(len(text.encode()) <= OUTPUT_LIMIT, "phase report byte ceiling")
    stream.seek(0)
    stream.write(text)
    stream.truncate()
    stream.flush()


def execute(manifest: Path, output: Path) -> dict[str, Any]:
    raw, phases = load_plan(manifest)
    # Reserve the output before any process is started. A retained earlier
    # attempt must never be overwritten, even after a partial failure.
    require(manifest.resolve() != output.resolve(), "manifest cannot be execution output")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as stream:
        report: dict[str, Any] = {
            "schema": SCHEMA,
            "status": "running",
            "started_at": utc_now(),
            "manifest": str(manifest),
            "manifest_sha256": hashlib.sha256(raw).hexdigest(),
            "phases": [],
            "unstarted_phase_names": [p["name"] for p in phases],
            "scientific_result_interpreted": False,
            "combined_resource_guard": "external supervisor; no internal wall/RSS guard",
        }
        start = time.perf_counter()
        write_report(stream, report)
        for phase in phases:
            entry: dict[str, Any] = {
                "name": phase["name"],
                "argv": phase["argv"],
                "started_at": utc_now(),
                "status": "running",
                "returncode": None,
                "wall_seconds": None,
            }
            report["phases"].append(entry)
            report["unstarted_phase_names"].pop(0)
            write_report(stream, report)
            phase_start = time.perf_counter()
            try:
                done = subprocess.run(phase["argv"], check=False)
                entry.update(
                    returncode=done.returncode,
                    status="completed" if done.returncode == 0 else "failed",
                )
            except KeyboardInterrupt:
                entry.update(status="interrupted", error="runner interrupted")
                report["status"] = "interrupted"
            except OSError as exc:
                entry.update(status="launch_failed", error=str(exc))
                report["status"] = "failed"
            entry.update(wall_seconds=time.perf_counter() - phase_start, ended_at=utc_now())
            try:
                current, _ = load_plan(manifest)
                require(current == raw, "execution manifest changed during phases")
            except (OSError, ValueError, TypeError) as exc:
                report.update(status="refused", error=str(exc))
            if report["status"] != "running" or entry["returncode"] != 0:
                if report["status"] == "running":
                    report["status"] = "failed"
                break
            write_report(stream, report)
        if report["status"] == "running":
            report["status"] = "completed"
        report.update(ended_at=utc_now(), wall_seconds=time.perf_counter() - start)
        write_report(stream, report)
        return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        report = execute(args.manifest, args.output)
    except (OSError, ValueError, TypeError) as exc:
        print(
            retained_json.dumps({"schema": SCHEMA, "status": "refused", "error": str(exc)}),
            file=sys.stderr,
        )
        return 2
    return 0 if report["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
