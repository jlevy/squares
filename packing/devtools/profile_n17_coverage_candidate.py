"""Reusable exact-coverage candidate diagnostics, ABBA plan and acceptance comparison.

Replay is a full independent standing check. This tool does not launch a campaign:
root must freeze its plan and enclosing owned-group supervisor before execution.
Observation is opt-in, matched across arms, and never interpreted as a speedup.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from collections.abc import Iterator, Sequence
from contextlib import ExitStack, contextmanager
from pathlib import Path
from statistics import median
from typing import Any

from devtools import profile_n17_exact_replay as profile
from devtools import verify_n17_kernel_certificate as standing
from sqpack import retained_json

SCHEMA = "n17-coverage-candidate-profile/v1"
ORDER = ("baseline", "candidate", "candidate", "baseline") * 2
BOUNDARY_FIELDS = (
    "step",
    "owner",
    "rows_requested_in_full",
    "counter_delta",
    "memo_sizes_after_row_checks",
)


class CoverageObserver:
    """Temporary exact hooks; boundary clocks only, never per-edge clocks."""

    def __init__(self, arm: str, deadline: float, *, observe: bool = False) -> None:
        profile.require(arm in {"baseline", "candidate"}, "unknown coverage arm")
        self.arm, self.deadline, self.observe = arm, deadline, observe
        self.counts: dict[str, int] = {}
        self.stages = profile.StageRecorder(deadline)

    @contextmanager
    def installed(self) -> Iterator[None]:
        with ExitStack() as contexts:
            if self.observe:
                contexts.enter_context(self.stages.installed())
            names = (
                "sweep_events",
                "compile_edges",
                "covered_by_sweep",
                "section_covered",
                "degenerate_covered",
            )
            originals = {name: getattr(standing, name) for name in names}

            def events(*args: Any, **kwargs: Any) -> Any:
                def invoke() -> Any:
                    if self.observe:
                        return standing.sweep_events_y_filtered(
                            *args,
                            **kwargs,
                            filter_y=self.arm == "candidate",
                            counts=self.counts,
                        )
                    function = (
                        standing.sweep_events_reference
                        if self.arm == "baseline"
                        else standing.sweep_events_y_filtered
                    )
                    return function(*args, **kwargs)

                return (
                    self.stages.measure("coverage_events", invoke) if self.observe else invoke()
                )

            def wrapper(name: str) -> Any:
                original = originals[name]

                def measured(*args: Any, **kwargs: Any) -> Any:
                    return self.stages.measure(name, lambda: original(*args, **kwargs))

                return measured

            try:
                standing.sweep_events = events
                if self.observe:
                    for name in names[1:]:
                        setattr(standing, name, wrapper(name))
                yield
            finally:
                for name, original in originals.items():
                    setattr(standing, name, original)


def bounded_json(path: Path) -> dict[str, Any]:
    profile.bounded_size(path, profile.OUTPUT_LIMIT)
    raw = path.read_bytes()
    if len(raw) > profile.OUTPUT_LIMIT:
        raise profile.IncompleteError("comparison streamed byte ceiling")
    result = json.loads(raw)
    profile.require(isinstance(result, dict), "comparison receipt is not an object")
    return result


def replay(arm: str, original_argv: list[str], *, observe: bool = False) -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--max-seconds", type=float, default=180)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--compare", type=Path)
    args, _ = parser.parse_known_args(original_argv)
    profile.require(
        math.isfinite(args.max_seconds) and args.max_seconds > 0, "invalid replay lease"
    )
    deadline = time.monotonic() + args.max_seconds
    accepted_sha = (
        None
        if args.compare is None
        else profile.digest(args.compare, deadline, profile.OUTPUT_LIMIT)
    )
    observer = CoverageObserver(arm, deadline, observe=observe)
    # Every arm retains the same boundary recorder and complete standing semantics.
    with observer.installed():
        code = profile.main([*original_argv, "--instrumentation", "phases"])
    report = bounded_json(args.output)
    if args.compare is not None:
        try:
            profile.require(
                profile.digest(args.compare, deadline, profile.OUTPUT_LIMIT) == accepted_sha,
                "accepted control receipt changed",
            )
        except (profile.IncompleteError, ValueError, OSError) as error:
            report.update(
                status="INCOMPLETE"
                if isinstance(error, profile.IncompleteError)
                else "REFUSED",
                error=str(error),
            )
            code = 1
    report.update(
        {
            "schema": SCHEMA,
            "arm": arm,
            "accepted_control_receipt_sha256": accepted_sha,
            "coverage_observation": observe,
            "coverage_work": observer.counts if observe else None,
            "observer_overhead_is_not_gain": observe,
        }
    )
    report["coverage_stages"] = (
        observer.stages.report(
            report.get("replay_wall_seconds", 0), report.get("replay_cpu_seconds", 0)
        )
        if observe
        else None
    )
    if time.monotonic() >= deadline:
        report.update(status="INCOMPLETE", error="coverage final serialization lease")
        code = 1
    encoded = retained_json.dumps(report) + "\n"
    if len(encoded.encode()) > profile.OUTPUT_LIMIT or time.monotonic() >= deadline:
        report = {
            "schema": SCHEMA,
            "status": "INCOMPLETE",
            "arm": arm,
            "error": "coverage final output or wall ceiling",
            "scientific_admission_proved": False,
        }
        encoded = retained_json.dumps(report) + "\n"
        code = 1
    args.output.write_text(encoded)
    return code


def boundary_payload(report: dict[str, Any]) -> dict[str, Any]:
    return {
        "steps": [{k: row[k] for k in BOUNDARY_FIELDS} for row in report["steps"]],
        "memo_evictions": report["memo_evictions"],
    }


def compare(reports: Sequence[dict[str, Any]], supervision: dict[str, Any]) -> dict[str, Any]:
    profile.require(len(reports) == 8, "two complete ABBA blocks required")
    profile.require(tuple(r.get("arm") for r in reports) == ORDER, "ABBA order differs")
    if (
        any(r.get("status") == "INCOMPLETE" for r in reports)
        or supervision.get("status") != "COMPLETED"
    ):
        return {"schema": SCHEMA, "status": "INCOMPLETE", "gain_accepted": False}
    first = reports[0]
    profile.require(
        supervision.get("schema") == "posix-bounded-command-supervision/v1"
        and supervision.get("max_memory_mib_per_process") == 4096
        and supervision.get("max_seconds") == 1440
        and supervision.get("cleanup_seconds") == 10,
        "supervisor resource regime differs",
    )
    profile.require(
        len({r["runtime"]["pid"] for r in reports}) == 8,
        "fresh process identities differ",
    )
    for row in reports:
        profile.require(
            row.get("schema") == SCHEMA and row.get("status") == "COMPLETE",
            "noncomplete profile",
        )
        profile.require(
            row.get("matched_uninstrumented_baseline") is True
            and isinstance(row.get("accepted_control_receipt_sha256"), str)
            and len(row["accepted_control_receipt_sha256"]) == 64
            and row["accepted_control_receipt_sha256"]
            == first["accepted_control_receipt_sha256"],
            "accepted control identity differs",
        )
        result = row["verification_result"]
        profile.require(
            result.get("mode") == "full" and result.get("status") in profile.ACCEPTED,
            "full standing acceptance required",
        )
        profile.require(
            row.get("instrumentation") == "phases", "matched boundary instrumentation required"
        )
        profile.require(
            row.get("coverage_observation") == first.get("coverage_observation"),
            "observation regime differs",
        )
        profile.require(
            row["mathematical_result_sha256"]
            == profile.result_identity(result)
            == first["mathematical_result_sha256"],
            "mathematical payload differs",
        )
        profile.require(
            row["input_compressed_or_file_sha256"] == first["input_compressed_or_file_sha256"]
            and row["post_replay_input_recheck_complete"],
            "input custody differs",
        )
        profile.require(
            result.get("counts", {}).get("steps") == 16
            and len(row["steps"]) == 16
            and [step["step"] for step in row["steps"]] == list(range(16)),
            "complete sixteen-step boundary roster differs",
        )
        profile.require(
            all(
                row["runtime"][key] == first["runtime"][key]
                for key in ("python", "platform", "logical_cpus", "single_worker")
            )
            and row["runtime"]["single_worker"] is True,
            "runtime regime differs",
        )
        profile.require(
            boundary_payload(row) == boundary_payload(first),
            "standing boundary or proof counters differ",
        )
        for name in ("replay_wall_seconds", "replay_cpu_seconds"):
            value = row[name]
            profile.require(
                type(value) in {int, float} and math.isfinite(value) and value > 0,
                "invalid measured time",
            )
    profile.require(
        supervision.get("returncode") == 0 and supervision.get("cleanup_complete") is True,
        "campaign did not finish cleanly",
    )
    rss = supervision["maximum_sampled_current_rss_bytes_by_pid"]
    per_arm: dict[str, list[int]] = {"baseline": [], "candidate": []}
    for row in reports:
        value = rss[str(row["runtime"]["pid"])]
        profile.require(
            type(value) is int and 0 < value <= 4096 * (1 << 20),
            "missing or invalid sampled RSS",
        )
        per_arm[row["arm"]].append(value)
    blocks = []
    for offset in (0, 4):
        block = reports[offset : offset + 4]
        outcome = {}
        for metric in ("replay_wall_seconds", "replay_cpu_seconds"):
            a = median(r[metric] for r in block if r["arm"] == "baseline")
            b = median(r[metric] for r in block if r["arm"] == "candidate")
            outcome[metric] = {"baseline": a, "candidate": b, "candidate_strictly_lower": b < a}
        blocks.append(outcome)
    overall = {}
    for metric in ("replay_wall_seconds", "replay_cpu_seconds"):
        a = median(r[metric] for r in reports if r["arm"] == "baseline")
        b = median(r[metric] for r in reports if r["arm"] == "candidate")
        overall[metric] = {
            "baseline": a,
            "candidate": b,
            "candidate_at_least_ten_percent_lower": b <= 0.9 * a,
        }
    memory_ok = 10 * max(per_arm["candidate"]) <= 11 * max(per_arm["baseline"])
    accepted = (
        all(v["candidate_strictly_lower"] for b in blocks for v in b.values())
        and all(v["candidate_at_least_ten_percent_lower"] for v in overall.values())
        and memory_ok
    )
    return {
        "schema": SCHEMA,
        "status": "COMPLETE",
        "gain_accepted": accepted and first["coverage_observation"] is False,
        "diagnostic_observation_only": first["coverage_observation"],
        "blocks": blocks,
        "overall": overall,
        "sampled_rss": per_arm,
        "candidate_rss_no_more_than_ten_percent_above": memory_ok,
        "mathematical_and_input_parity": True,
        "standing_boundary_parity": True,
        "mathematical_result_sha256": first["mathematical_result_sha256"],
        "scientific_admission_proved": False,
        "rss_scope": "sampled current RSS per live process, not allocation-time or aggregate",
    }


def plan(common: list[str], directory: Path, *, observe: bool = False) -> dict[str, Any]:
    profile.require(
        "--instrumentation" not in common and "--output" not in common,
        "plan owns profile setting/output",
    )
    phases = []
    for index, arm in enumerate(ORDER, 1):
        argv = [
            sys.executable,
            "-m",
            "devtools.profile_n17_coverage_candidate",
            "replay",
            "--arm",
            arm,
        ]
        if observe:
            argv.append("--observe")
        argv.extend([*common, "--output", str(directory / f"{index:02}-{arm}.json")])
        phases.append({"name": f"{index:02}-{arm}", "argv": argv})
    return {"phases": phases, "comparison_order": list(ORDER), "benchmarks_launched": False}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    child = commands.add_parser("replay")
    child.add_argument("--arm", choices=("baseline", "candidate"), required=True)
    child.add_argument("--observe", action="store_true")
    proposal = commands.add_parser("plan")
    proposal.add_argument("--directory", type=Path, required=True)
    proposal.add_argument("--output", type=Path, required=True)
    proposal.add_argument("--observe", action="store_true")
    comparison = commands.add_parser("compare")
    comparison.add_argument("--receipts", type=Path, nargs=8, required=True)
    comparison.add_argument("--supervision", type=Path, required=True)
    comparison.add_argument("--output", type=Path, required=True)
    args, remainder = parser.parse_known_args(argv)
    if args.command == "replay":
        return replay(args.arm, remainder, observe=args.observe)
    try:
        if args.command == "plan":
            value = plan(
                remainder[1:] if remainder[:1] == ["--"] else remainder,
                args.directory,
                observe=args.observe,
            )
        else:
            profile.require(not remainder, "unknown comparison arguments")
            value = compare(
                [bounded_json(p) for p in args.receipts], bounded_json(args.supervision)
            )
    except (OSError, ValueError, KeyError, TypeError) as error:
        value = {
            "schema": SCHEMA,
            "status": "REFUSED",
            "error": str(error),
            "gain_accepted": False,
        }
    args.output.write_text(retained_json.dumps(value) + "\n")
    return 0 if value.get("status", "COMPLETE") == "COMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
