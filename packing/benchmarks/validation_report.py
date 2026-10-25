"""Generate a validation-efficiency report from validated experiments and raw receipts."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import statistics
import sys
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from jsonschema import validate
from strif import atomic_write_text

from sqpack.yamlio import load_yaml

DEFAULT_ROOT = Path(__file__).with_name("validation-efficiency")
PHASE_ORDER = ("off", "on", "on", "off", "off", "on")
PHASE_FIXTURE = (
    "import pytest\n"
    "@pytest.mark.parametrize('case', range(1000), "
    "ids=[f'case::{index:04d}' for index in range(1000)])\n"
    "def test_case(case):\n    assert case >= 0\n"
)
FOOTER = """<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
"""


def completed_runs(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Reject contradictory journals; retain failed and unmatched observations."""
    starts: dict[str, dict[str, Any]] = {}
    ends: dict[str, dict[str, Any]] = {}
    for event in events:
        run_id = event["run_id"]
        if event["event"] == "start":
            if run_id in starts:
                raise ValueError(f"duplicate start: {run_id}")
            starts[run_id] = event
        elif event["event"] == "end":
            if run_id not in starts or run_id in ends:
                raise ValueError(f"unmatched or duplicate end: {run_id}")
            for field, value in starts[run_id].items():
                if field != "event" and event.get(field) != value:
                    raise ValueError(f"receipt changed {field}: {run_id}")
            for field in ("wall_seconds", "allocated_worker_seconds"):
                value = event[field]
                if (
                    isinstance(value, bool)
                    or not isinstance(value, (int, float))
                    or not math.isfinite(value)
                    or value < 0
                ):
                    raise ValueError(f"invalid {field}: {run_id}")
            if event["status"] not in {"passed", "failed", "timeout", "interrupted"}:
                raise ValueError(f"invalid status: {run_id}")
            if event["status"] == "passed" and event["returncode"] != 0:
                raise ValueError(f"nonzero pass: {run_id}")
            workers = event["allocated_workers"]
            if (
                isinstance(workers, bool)
                or not isinstance(workers, int)
                or workers < 1
                or not math.isclose(
                    event["allocated_worker_seconds"], event["wall_seconds"] * workers
                )
            ):
                raise ValueError(f"contradictory worker allocation: {run_id}")
            ends[run_id] = event
        else:
            raise ValueError(f"unknown event: {event['event']}")
    return [ends.get(key, {**start, "status": "incomplete"}) for key, start in starts.items()]


def validate_evidence(root: Path, runs: list[dict[str, Any]]) -> None:
    """Require clean, nonempty JUnit evidence for every claimed passing receipt."""
    for run in runs:
        if run["status"] != "passed":
            continue
        junit = root / "runs" / Path(run["junit_path"]).name
        if not junit.is_file():
            raise ValueError(f"passing run has no JUnit: {run['run_id']}")
        tree = ET.parse(junit)
        cases = tree.findall(".//testcase")
        if not cases or any(
            case.find(tag) is not None
            for case in cases
            for tag in ("failure", "error", "skipped")
        ):
            raise ValueError(f"passing run has unsuccessful or empty JUnit: {run['run_id']}")
        for suite in tree.iter():
            if suite.tag not in {"testsuite", "testsuites"}:
                continue
            if "tests" in suite.attrib and int(suite.attrib["tests"]) != len(
                suite.findall(".//testcase")
            ):
                raise ValueError(f"passing run has contradictory JUnit count: {run['run_id']}")
            if any(
                float(suite.get(tag, "0")) != 0 for tag in ("failures", "errors", "skipped")
            ):
                raise ValueError(f"passing run has contradictory JUnit: {run['run_id']}")
        run["test_cases"] = sorted(
            (case.get("classname", ""), case.get("name", "")) for case in cases
        )


def comparable(experiment: dict[str, Any], arms: list[list[dict[str, Any]]]) -> bool:
    """Keep selections and provenance stable; only source changes may differ by arm."""
    runs = [run for arm in arms for run in arm]
    common_fields = (
        "platform",
        "python",
        "interpreter",
        "available_cpus",
        "native_threads",
        "test_cases",
    )
    arm_fields = (
        "commit",
        "source_hashes",
        "root",
        "environment",
        "allocated_workers",
        "inner_workers",
        "pytest_workers",
        "timeout_seconds",
    )
    if any(
        experiment["target"] not in run.get("command", [])
        or not isinstance(run.get("dirty_diff_sha256"), str)
        or not run["dirty_diff_sha256"]
        for run in runs
    ):
        return False
    for group, fields in [(runs, common_fields), *[(arm, arm_fields) for arm in arms]]:
        if any(
            field not in run or run[field] != group[0].get(field)
            for run in group
            for field in fields
        ):
            return False
    environments = [
        {
            key: value
            for key, value in run["environment"].items()
            if key not in {"PYTHONPATH", "PACK_JOBS"}
        }
        for run in runs
    ]
    return all(run.get("test_cases") for run in runs) and all(
        environment == environments[0] for environment in environments
    )


def screen(experiment: dict[str, Any], runs: list[dict[str, Any]]) -> tuple[str, str, str]:
    arms = [
        [run for run in runs if run["label"] == experiment[field]]
        for field in ("control_label", "candidate_label")
    ]
    summaries = []
    for arm in arms:
        values = [run["wall_seconds"] for run in arm if run["status"] == "passed"]
        summaries.append(
            f"{statistics.median(values):.2f} ({min(values):.2f}-{max(values):.2f}), "
            f"n={len(values)}"
            if values
            else "No passing samples"
        )
    if any(run["status"] != "passed" for arm in arms for run in arm):
        verdict = "Incomplete or unsuccessful observation; no acceptance"
    elif any(len(arm) < experiment["minimum_samples"] for arm in arms):
        verdict = "Pending samples"
    elif not comparable(experiment, arms):
        verdict = "Incomparable selection or source/worker regime; no acceptance"
    elif any(
        not math.isfinite(run[field]) or run[field] <= 0
        for arm in arms
        for run in arm
        for field in ("wall_seconds", "allocated_worker_seconds")
    ):
        verdict = "Invalid or zero timing denominator; no acceptance"
    else:
        control, candidate = [[run["wall_seconds"] for run in arm] for arm in arms]
        reduction = 1 - statistics.median(candidate) / statistics.median(control)
        allocation_ratio = statistics.median(
            run["allocated_worker_seconds"] for run in arms[1]
        ) / statistics.median(run["allocated_worker_seconds"] for run in arms[0])
        if max(candidate) >= min(control):
            verdict = "No detectable effect: ranges overlap or candidate is slower"
        elif reduction < experiment["minimum_improvement"]:
            verdict = "Below declared improvement threshold"
        elif allocation_ratio > experiment["maximum_allocation_ratio"]:
            verdict = "Exceeds allocated-work guard"
        else:
            verdict = (
                f"Screen passes ({reduction:.1%} median reduction); "
                "correctness and complexity review required"
            )
    if any(len({run.get("dirty_diff_sha256") for run in arm}) > 1 for arm in arms):
        verdict += (
            "; whole-tree diff varied within an arm: affected-source audit required, "
            "whole-tree equivalence is not established"
        )
    return summaries[0], summaries[1], verdict


def render(root: Path) -> str:
    schema = load_yaml((root / "experiment.schema.yaml").read_text())
    experiments = []
    for path in sorted((root / "experiments").glob("*.md")):
        text = path.read_text()
        parts = text.split("---", 2)
        if not text.startswith("---") or len(parts) < 3:
            raise ValueError(f"experiment record lacks YAML frontmatter: {path}")
        frontmatter = load_yaml(parts[1])
        experiment = frontmatter["experiment"]
        validate(experiment, schema)
        experiments.append((path, experiment))
    journal = root / "runs/receipts.jsonl"
    events = (
        [json.loads(line) for line in journal.read_text().splitlines()]
        if journal.exists()
        else []
    )
    runs = completed_runs(events)
    validate_evidence(root, runs)
    labels = {
        exp[field] for _, exp in experiments for field in ("control_label", "candidate_label")
    }
    if len(labels) != 2 * len(experiments):
        raise ValueError("experiment labels must be unique")
    if any(run["label"] not in labels for run in runs):
        raise ValueError("receipt references an unregistered label")
    lines = [
        "# Validation Efficiency Results",
        "",
        "Generated by `python -m benchmarks.validation_report`. Do not edit this view.",
        "",
        "These are exploratory measurements on the recorded host and cache regime.",
        "Wall seconds include pytest startup. Allocated worker-seconds are not measured CPU.",
        (
            "Selected test hashes do not establish whole-tree equivalence. "
            "Within-arm whole-tree diff variation requires an affected-source audit "
            "before accepting an arithmetic result."
        ),
        "",
        (
            "| Experiment | Control seconds: median (range) | "
            "Candidate seconds: median (range) | Arithmetic screen |"
        ),
        "| --- | --- | --- | --- |",
    ]
    for path, experiment in experiments:
        control, candidate, verdict = screen(experiment, runs)
        lines.append(
            f"| [{experiment['id']}]({path.relative_to(root).as_posix()}) | "
            f"{control} | {candidate} | {verdict} |"
        )
    lines.extend(
        [
            "",
            "## Observations",
            "",
            "Every observation is listed, including incomplete or failed work.",
            "",
        ]
    )
    for run in runs:
        run_id = run["run_id"]
        seconds = f"{run['wall_seconds']:.2f}s" if "wall_seconds" in run else "incomplete"
        junit = root / "runs" / Path(run["junit_path"]).name
        count = "no JUnit report"
        if junit.exists():
            cases = ET.parse(junit).findall(".//testcase")
            count = f"{len(cases)} test cases"
        elif run["status"] == "passed":
            raise ValueError(f"passing run has no JUnit: {run_id}")
        lines.append(
            f"- `{run_id}`: {run['label']}, {run['status']}, {seconds}, {count}; "
            f"[output](runs/{run_id}.stdout.log), [errors](runs/{run_id}.stderr.log)."
        )
    lines.extend(
        [
            "",
            "The append-only [receipts](runs/receipts.jsonl) retain commands and provenance.",
            "",
            FOOTER.rstrip(),
            "",
        ]
    )
    return "\n".join(lines)


def _phase_file(root: Path, relative: str) -> Path:
    path = root / relative
    if (
        not path.resolve().is_relative_to(root.resolve())
        or root.is_symlink()
        or any(
            parent.is_symlink()
            for parent in (path, *path.parents)
            if parent.is_relative_to(root)
        )
    ):
        raise ValueError("phase evidence must remain in its fixed subtree without symlinks")
    return path


def _phase_events(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        raise ValueError("incomplete phase evidence line")
    rows = [json.loads(line) for line in text.splitlines()]
    if not rows or any(not isinstance(row, dict) for row in rows):
        raise ValueError("phase evidence needs nonempty object rows")
    return rows


def phase_command(protocol: dict[str, Any], index: int, arm: str) -> list[str]:
    """The original command is data; a maintained reader need not live at that root."""
    base, source = Path(protocol["output_root"]), protocol["source"]
    fixture = base / "fixture/test_phase_timing_work.py"
    return [
        source["interpreter"],
        "-m",
        "benchmarks.validation_timing",
        "--root",
        source["root"],
        "--label",
        arm,
        "--output-dir",
        str(base / f"observations/{index}-{arm}/runs"),
        "--repeats",
        "1",
        "--timeout",
        "30",
        "--workers",
        "2",
        "--inner-workers",
        "1",
        "--native-threads",
        "1",
        *(["--phase-timings"] if arm == "on" else []),
        "--",
        str(fixture),
        "-c",
        protocol["null_config"],
        "--noconftest",
        "--rootdir",
        str(fixture.parent),
        "--basetemp",
        str(base / f"observations/{index}-{arm}/pytest-tmp"),
        "-o",
        "junit_duration_report=total",
        "-p",
        "xdist.plugin",
    ]


def phase_observation(
    root: Path, protocol: dict[str, Any], index: int, arm: str, outer: dict[str, Any]
) -> dict[str, Any]:
    """Bind this fixed subtree's UUID, command, JUnit and worker journals together."""
    if (
        outer["command"] != phase_command(protocol, index, arm)
        or outer.get("observation") != index
        or outer.get("label") != arm
        or outer.get("status") != "passed"
        or outer.get("returncode") != 0
        or outer.get("timeout_seconds") != 45
        or outer.get("allocated_workers") != 2
        or outer.get("root") != protocol["source"]["root"]
        or outer.get("error") != ""
    ):
        raise ValueError("whole-CLI observation contradicts the declared command")
    relative = f"observations/{index}-{arm}"
    runs = completed_runs(_phase_events(_phase_file(root, f"{relative}/runs/receipts.jsonl")))
    if len(runs) != 1 or runs[0]["status"] != "passed":
        raise ValueError("observation needs exactly one successful inner receipt")
    run = runs[0]
    identifier = run["run_id"]
    if not isinstance(identifier, str) or re.fullmatch("[0-9a-f]{32}", identifier) is None:
        raise ValueError("invalid inner UUID")
    original = Path(protocol["output_root"]) / relative / "runs" / identifier
    source = protocol["source"]
    arguments = phase_command(protocol, index, arm)
    targets = arguments[arguments.index("--") + 1 :]
    expected = [
        source["interpreter"],
        "-m",
        "pytest",
        "-q",
        *targets,
        "--durations=0",
        "--durations-min=0",
        f"--junitxml={original}.junit.xml",
        "-n",
        "2",
    ]
    if arm == "on":
        expected += [
            "-p",
            "devtools.reachable_progress",
            "--reachable-phase-timings=pytest-report-duration-v1",
        ]
    if (
        run["command"] != expected
        or run.get("label") != arm
        or run.get("repeat") != 1
        or run.get("root") != source["root"]
        or run.get("commit") != source["commit"]
        or run.get("git_status") != ""
        or run.get("timeout_seconds") != 30
        or any(
            run.get(key) != value
            for key, value in {
                "pytest_workers": 2,
                "inner_workers": 1,
                "native_threads": 1,
                "allocated_workers": 2,
                "interpreter": source["interpreter"],
            }.items()
        )
    ):
        raise ValueError("inner selection or execution regime differs")
    if (
        any(run.get(key) != source[key] for key in ("python", "platform", "available_cpus"))
        or source["available_cpus"] != 2
    ):
        raise ValueError("runtime regime differs")
    expected_environment: dict[str, str] = dict.fromkeys(
        (
            "OPENBLAS_NUM_THREADS",
            "OMP_NUM_THREADS",
            "MKL_NUM_THREADS",
            "VECLIB_MAXIMUM_THREADS",
            "NUMEXPR_NUM_THREADS",
            "BLIS_NUM_THREADS",
            "PACK_JOBS",
            "UV_NO_SYNC",
        ),
        "1",
    )
    expected_environment["PYTHONPATH"] = os.pathsep.join(
        (str(Path(source["root"]) / "src"), source["root"])
    )
    if run["environment"] != expected_environment:
        raise ValueError("inner environment differs")
    if run.get("pytest_configuration") != {
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
        "PYTHONUNBUFFERED": "1",
        "PYTHONPYCACHEPREFIX": str(Path(protocol["output_root"]) / "python-cache"),
    }:
        raise ValueError("pytest configuration differs")
    for suffix, field in (
        ("stdout.log", "stdout_path"),
        ("stderr.log", "stderr_path"),
        ("junit.xml", "junit_path"),
    ):
        if run[field] != f"{original}.{suffix}":
            raise ValueError("inner artifact is not bound to its UUID")
        _phase_file(root, f"{relative}/runs/{identifier}.{suffix}").read_bytes()
    validate_evidence(_phase_file(root, relative), [run])
    names = {f"test_case[case::{number:04d}]" for number in range(1000)}
    if run["test_cases"] != sorted(("test_phase_timing_work", name) for name in names):
        raise ValueError("selected JUnit identities differ")
    junit_totals: dict[str, float] = {}
    for case in ET.parse(_phase_file(root, f"{relative}/runs/{identifier}.junit.xml")).findall(
        ".//testcase"
    ):
        raw_time = case.get("time")
        if raw_time is None:
            raise ValueError("JUnit testcase time is required")
        total = float(raw_time)
        if not math.isfinite(total) or total < 0:
            raise ValueError("JUnit testcase time must be finite and nonnegative")
        junit_totals[f"test_phase_timing_work.py::{case.get('name')}"] = total
    directory = _phase_file(root, f"{relative}/runs")
    journals = sorted(directory.glob("*.progress-*.jsonl"))
    if arm == "off":
        if journals:
            raise ValueError("phase-off observation has phase journals")
        return run
    expected_journals = [f"{identifier}.progress-gw{worker}.jsonl" for worker in range(2)]
    if [path.name for path in journals] != expected_journals:
        raise ValueError("worker journal census differs")
    if run.get("phase_timings") != {
        "capability": "pytest-report-duration-v1",
        "stem": str(original),
    }:
        raise ValueError("phase stem differs from this inner UUID")
    if run.get("phase_journals") != [
        str(original) + f".progress-gw{worker}.jsonl" for worker in range(2)
    ]:
        raise ValueError("phase paths differ from this inner UUID")
    phases: dict[tuple[str, str], float] = {}
    starts: set[str] = set()
    finishes: set[str] = set()
    for worker, path in enumerate(journals):
        rows = _phase_events(_phase_file(root, f"{relative}/runs/{path.name}"))
        if (
            rows[0]["event"] != "session_start"
            or rows[-1]["event"] != "session_finish"
            or sum(row["event"] == "session_start" for row in rows) != 1
            or sum(row["event"] == "session_finish" for row in rows) != 1
            or rows[-1].get("exit_status") != 0
            or rows[0].get("phase_timing_capability") != "pytest-report-duration-v1"
            or rows[0].get("phase_plugin_path")
            != str(Path(source["root"]) / "devtools/reachable_progress.py")
        ):
            raise ValueError("incomplete or incompatible worker session")
        owned = {row["nodeid"] for row in rows if row["event"] == "start"}
        active: set[str] = set()
        for row in rows:
            if any(
                row.get(key) != value
                for key, value in {
                    "schema": "reachable-progress-v1",
                    "run_id": identifier,
                    "command_id": identifier,
                    "source_commit": source["commit"],
                    "worker_id": f"gw{worker}",
                    "xdist_workers": 2,
                    "pack_jobs": "1",
                    "lane": "validation-timing",
                    "marker": "",
                    "exclusions": "explicit timing selection",
                }.items()
            ):
                raise ValueError("worker journal identity differs")
            node, event = row["nodeid"], row["event"]
            if event not in {"session_start", "session_finish"} and node not in owned:
                raise ValueError("node report belongs to another worker")
            if event in {"start", "finish"}:
                seen = starts if event == "start" else finishes
                if node in seen or (event == "finish" and row.get("outcome") != "passed"):
                    raise ValueError("duplicate or unsuccessful node")
                if event == "start":
                    active.add(node)
                elif node not in active or any(
                    (node, phase) not in phases for phase in ("setup", "call", "teardown")
                ):
                    raise ValueError("node finish precedes its completed phases")
                seen.add(node)
            elif event == "phase_finish":
                phase, duration = row.get("phase"), row.get("duration_seconds")
                if (
                    node not in active
                    or not isinstance(phase, str)
                    or phase not in {"setup", "call", "teardown"}
                    or row.get("outcome") != "passed"
                    or isinstance(duration, bool)
                    or not isinstance(duration, (int, float))
                    or not math.isfinite(duration)
                    or duration < 0
                ):
                    raise ValueError("invalid or duplicate quantitative phase")
                key: tuple[str, str] = (node, phase)
                if key in phases:
                    raise ValueError("invalid or duplicate quantitative phase")
                phases[key] = duration
            elif event not in {"session_start", "session_finish"}:
                raise ValueError("unexpected phase event")
    nodes = {f"test_phase_timing_work.py::{name}" for name in names}
    if (
        starts != nodes
        or finishes != nodes
        or set(phases)
        != {(node, phase) for node in nodes for phase in ("setup", "call", "teardown")}
    ):
        raise ValueError("node/phase census differs")
    for node, total in junit_totals.items():
        if (
            abs(total - sum(phases[node, phase] for phase in ("setup", "call", "teardown")))
            > 0.001
        ):
            raise ValueError("same-run JUnit and phase totals differ")
    run["phase_rows"] = len(phases)
    run["phase_bytes"] = sum(path.stat().st_size for path in journals)
    return run


def phase_overhead(root: Path) -> dict[str, Any]:
    protocol = json.loads(_phase_file(root, "protocol.json").read_text())
    if protocol.get("protocol") != "phase-overhead-v2" or protocol.get("order") != list(
        PHASE_ORDER
    ):
        raise ValueError("unknown phase overhead protocol")
    if _phase_file(root, "fixture/test_phase_timing_work.py").read_text() != PHASE_FIXTURE:
        raise ValueError("declared fixture differs")
    if json.loads(_phase_file(root, "completion.json").read_text()).get("complete") is not True:
        raise ValueError("comparison has no completed capture")
    outer = completed_runs(_phase_events(_phase_file(root, "outer/receipts.jsonl")))
    if len(outer) != len(PHASE_ORDER):
        raise ValueError("comparison is incomplete")
    for run in outer:
        identifier = run["run_id"]
        if re.fullmatch("[0-9a-f]{32}", str(identifier)) is None:
            raise ValueError("invalid whole-CLI UUID")
        original = Path(protocol["output_root"]) / "outer" / identifier
        for suffix, field in (("stdout.log", "stdout_path"), ("stderr.log", "stderr_path")):
            if run[field] != f"{original}.{suffix}":
                raise ValueError("whole-CLI artifact is not bound to its UUID")
            _phase_file(root, f"outer/{identifier}.{suffix}").read_bytes()
    inner = [
        phase_observation(root, protocol, index, arm, run)
        for index, (arm, run) in enumerate(zip(PHASE_ORDER, outer, strict=True))
    ]
    if len({run["run_id"] for run in inner}) != 6:
        raise ValueError("inner UUID was reused")
    arms = [
        [run["wall_seconds"] for run in outer if run["label"] == arm] for arm in ("off", "on")
    ]
    if any(
        type(value) not in (float, int) or not math.isfinite(value) or value <= 0
        for arm in arms
        for value in arm
    ):
        raise ValueError("invalid whole-CLI denominator")
    off, on = map(statistics.median, arms)
    return {
        "protocol": "phase-overhead-v2",
        "wall_seconds": arms,
        "ranges": [[min(arm), max(arm)] for arm in arms],
        "medians": [off, on],
        "median_ratio": on / off,
        "added_median_seconds": on - off,
        "phase_rows": [run.get("phase_rows", 0) for run in inner],
        "phase_bytes": [run.get("phase_bytes", 0) for run in inner],
        "accepted": on / off <= 1.05 and on - off <= 3.0,
    }


def main() -> int:
    if sys.argv[1:2] == ["phase-overhead"]:
        parser = argparse.ArgumentParser(description="Read retained v2 phase overhead evidence")
        parser.add_argument("--root", type=Path, required=True)
        args = parser.parse_args(sys.argv[2:])
        print(json.dumps(phase_overhead(args.root), sort_keys=True))
        return 0
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    text = render(args.root)
    destination = args.root / "report.md"
    if args.check:
        return 0 if destination.exists() and destination.read_text() == text else 1
    atomic_write_text(destination, text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
