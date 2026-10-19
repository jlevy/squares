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
RECONCILIATION_SCHEMA = "registered-phase-supervision-reconciliation/v1"
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

    pending = [plan]
    while pending:
        value = pending.pop()
        if type(value) is float:
            require(math.isfinite(value), "nonfinite execution-plan number")
        elif type(value) is list:
            pending.extend(value)
        elif type(value) is dict:
            pending.extend(value.values())
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


def read_record(path: Path, limit: int) -> tuple[bytes, dict[str, Any]]:
    with path.open("rb") as stream:
        raw = stream.read(limit + 1)
    require(len(raw) <= limit, "reconciliation input byte ceiling")

    def floating(token: str) -> float:
        value = float(token)
        require(math.isfinite(value), "nonfinite reconciliation number")
        return value

    record = json.loads(
        raw, object_pairs_hook=unique, parse_constant=nonfinite, parse_float=floating
    )
    require(type(record) is dict, "reconciliation input object required")
    return raw, cast(dict[str, Any], record)


def check_journal(
    journal: dict[str, Any], phases: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    require(journal.get("schema") == SCHEMA, "phase journal schema differs")
    require(
        journal.get("scientific_result_interpreted") is False,
        "journal must not interpret science",
    )
    entries = journal.get("phases")
    require(type(entries) is list and len(entries) <= len(phases), "journal phase prefix")
    entries = cast(list[dict[str, Any]], entries)
    for index, entry in enumerate(entries):
        require(type(entry) is dict, "journal phase object required")
        require(
            entry.get("name") == phases[index]["name"]
            and entry.get("argv") == phases[index]["argv"],
            "journal phase identity/order differs",
        )
        status, code, wall = (
            entry.get("status"),
            entry.get("returncode"),
            entry.get("wall_seconds"),
        )
        require(type(entry.get("started_at")) is str, "phase start required")
        if status == "running":
            require(
                index == len(entries) - 1 and code is None and wall is None,
                "running phase must be the unresolved tail",
            )
        else:
            require(
                type(wall) in (int, float) and cast(float, wall) >= 0,
                "terminal phase wall required",
            )
            require(type(entry.get("ended_at")) is str, "phase end required")
            require(
                (status == "completed" and type(code) is int and code == 0)
                or (status == "failed" and type(code) is int and code != 0)
                or (status in ("launch_failed", "interrupted") and code is None),
                "terminal phase status/returncode differs",
            )
            require(
                status == "completed" or index == len(entries) - 1,
                "failed phase cannot have successors",
            )
    require(
        journal.get("unstarted_phase_names") == [p["name"] for p in phases[len(entries) :]],
        "unstarted phase roster differs",
    )
    require(
        journal.get("status") in ("running", "completed", "failed", "interrupted", "refused"),
        "unsupported journal status",
    )
    return entries


def reconcile(
    manifest: Path, journal: Path, supervision: Path, output: Path, execution_root: Path
) -> dict[str, Any]:
    """Derive terminal execution status without changing any original evidence.

    The supervisor establishes owned-group termination, not a child's missing
    exit code or a scientific verdict. A stale running entry remains unresolved.
    """
    paths = {"manifest": manifest, "journal": journal, "supervision": supervision}
    require(len({p.resolve() for p in paths.values()}) == 3, "distinct inputs required")
    require(
        output.resolve() not in {p.resolve() for p in paths.values()}, "output aliases input"
    )
    raw, phases = load_plan(manifest)
    journal_raw, observed = read_record(journal, OUTPUT_LIMIT)
    supervisor_raw, guard = read_record(supervision, PLAN_LIMIT)
    require(
        observed.get("manifest_sha256") == hashlib.sha256(raw).hexdigest(),
        "journal manifest byte identity differs",
    )

    def resolved(value: str) -> Path:
        path = Path(value)
        return (path if path.is_absolute() else execution_root / path).resolve()

    require(
        type(observed.get("manifest")) is str
        and resolved(observed["manifest"]) == manifest.resolve(),
        "journal manifest path differs",
    )
    entries = check_journal(observed, phases)
    argv = guard.get("argv")
    require(
        type(argv) is list
        and len(argv) == 7
        and all(type(token) is str for token in argv)
        and bool(argv[0])
        and argv[1:3] == ["-m", "devtools.run_registered_phases"]
        and set(argv[3::2]) == {"--manifest", "--output"},
        "supervisor command is not this phase runner",
    )
    argv = cast(list[str], argv)
    flags = dict(zip(argv[3::2], argv[4::2], strict=True))
    require(
        resolved(flags["--manifest"]) == manifest.resolve()
        and resolved(flags["--output"]) == journal.resolve(),
        "supervisor runner paths differ",
    )
    require(
        guard.get("schema") == "posix-bounded-command-supervision/v1"
        and guard.get("status") in ("COMPLETED", "INCOMPLETE")
        and guard.get("cleanup_complete") is True
        and type(guard.get("returncode")) is int
        and type(guard.get("pid")) is int
        and guard["pid"] > 0
        and type(guard.get("owned_pgid")) is int
        and guard["pid"] == guard["owned_pgid"],
        "terminal owned-group cleanup evidence required",
    )
    complete = (
        observed["status"] == "completed"
        and len(entries) == len(phases)
        and all(p["status"] == "completed" for p in entries)
    )
    if guard["status"] == "COMPLETED" and guard["returncode"] == 0:
        require(complete, "successful supervisor conflicts with incomplete journal")
        status = "completed"
    else:
        status = "incomplete" if guard["status"] == "INCOMPLETE" else "failed"
    derived = copy.deepcopy(entries)
    for phase in derived:
        if phase["status"] == "running":
            phase["status"] = "interrupted_by_supervisor"
    report = {
        "schema": RECONCILIATION_SCHEMA,
        "status": status,
        "reconciled_at": utc_now(),
        "inputs": {
            name: {"path": str(paths[name]), "sha256": hashlib.sha256(data).hexdigest()}
            for name, data in zip(paths, (raw, journal_raw, supervisor_raw), strict=True)
        },
        "original_journal_status": observed["status"],
        "phases": derived,
        "unstarted_phase_names": observed["unstarted_phase_names"],
        "supervisor": guard,
        "scientific_result_interpreted": False,
        "missing_child_returncodes_inferred": False,
        "raw_evidence_modified": False,
    }
    for path, data in zip(paths.values(), (raw, journal_raw, supervisor_raw), strict=True):
        with path.open("rb") as stream:
            require(stream.read(len(data) + 1) == data, "reconciliation input bytes changed")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as stream:
        write_report(stream, report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--journal", type=Path)
    parser.add_argument("--supervision", type=Path)
    parser.add_argument("--execution-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    if (args.journal is None) != (args.supervision is None):
        parser.error("report-only reconciliation requires both --journal and --supervision")
    try:
        report = (
            execute(args.manifest, args.output)
            if args.journal is None
            else reconcile(
                args.manifest, args.journal, args.supervision, args.output, args.execution_root
            )
        )
    except (OSError, ValueError, TypeError) as exc:
        print(
            retained_json.dumps({"schema": SCHEMA, "status": "refused", "error": str(exc)}),
            file=sys.stderr,
        )
        return 2
    return 0 if report["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
