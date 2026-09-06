"""Generate a validation-efficiency report from validated experiments and raw receipts."""

from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from jsonschema import validate
from strif import atomic_write_text

from sqpack.yamlio import load_yaml

DEFAULT_ROOT = Path(__file__).with_name("validation-efficiency")
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


def main() -> int:
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
