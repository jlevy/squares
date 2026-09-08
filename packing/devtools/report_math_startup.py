"""Validate math-startup records and derive the timing ledger from raw observations."""

from __future__ import annotations

import argparse
import gzip
import json
import math
import random
import re
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

from devtools.validate_schemas import check, payload_and_meta

CAMPAIGN = Path(__file__).resolve().parents[1] / "benchmarks/math-startup"
FOOTER = """<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->"""


def interval(values: list[float]) -> tuple[float, float]:
    """Deterministic percentile bootstrap of the median paired percent change."""
    if not values or not all(math.isfinite(value) for value in values):
        raise ValueError("bootstrap needs finite observations")
    generator = random.Random(0x5EED)
    count = len(values)
    medians = sorted(
        statistics.median(values[generator.randrange(count)] for _ in values)
        for _ in range(2000)
    )
    return medians[int(0.025 * 1999)], medians[int(0.975 * 1999)]


def paired_result(runs: list[dict[str, Any]], hypothesis: dict[str, Any]) -> dict[str, Any]:
    """Reject missing or duplicated arms instead of quietly dropping bad pairs."""
    pairs: dict[int, dict[str, dict[str, Any]]] = defaultdict(dict)
    metric = hypothesis["metric"]
    regimes: set[str] = set()
    for run in runs:
        label, pair = run["label"], run["pair"]
        if label not in {"control", "candidate"} or label in pairs[pair]:
            raise ValueError("unknown or duplicate pair arm")
        if run.get("findings"):
            raise ValueError("measurement has validity findings")
        value = run["metrics"].get(metric)
        if not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise ValueError(f"missing or nonpositive {metric}")
        environment = run["environment"]
        regimes.add(
            json.dumps(
                {
                    key: environment[key]
                    for key in (
                        "browser",
                        "browser_version",
                        "viewport",
                        "browser_cache",
                        "os_cache",
                    )
                },
                sort_keys=True,
            )
        )
        pairs[pair][label] = run
    if len(regimes) != 1:
        raise ValueError("comparison mixes browser or cache regimes")
    if len(pairs) < hypothesis["minimum_pairs"]:
        raise ValueError("fewer than the registered number of pairs")
    if any(set(pair) != {"control", "candidate"} for pair in pairs.values()):
        raise ValueError("unmatched comparison pair")
    control = [pair["control"]["metrics"][metric] for pair in pairs.values()]
    candidate = [pair["candidate"]["metrics"][metric] for pair in pairs.values()]
    changes = [100 * (new - old) / old for old, new in zip(control, candidate, strict=True)]
    lower, upper = interval(changes)
    return {
        "pairs": len(pairs),
        "control": control,
        "candidate": candidate,
        "change_pct": statistics.median(changes),
        "ci95": (lower, upper),
        "passes": upper <= hypothesis["maximum_ci95_change_pct"],
    }


def spread(values: list[float]) -> str:
    """A median is always printed with the observed range."""
    return f"{statistics.median(values):.1f} ({min(values):.1f} to {max(values):.1f})"


def geometry_result(
    reports: list[dict[str, Any]], hypothesis: dict[str, Any]
) -> tuple[list[str], list[str]]:
    """Require the declared browser matrix and retain the falsification controls."""
    lines: list[str] = []
    problems: list[str] = []
    covered: set[tuple[str, int]] = set()
    controls: set[str] = set()
    tolerance = hypothesis["maximum_math_box_displacement_px"]
    for report in reports:
        browser, width = report["browser"], report["width"]
        label = f"{browser} {width}px {report['medium']}"
        problems.extend(f"{label}: {finding}" for finding in report["findings"])
        before = {box["key"]: box for box in report["before"]}
        after = {box["key"]: box for box in report["after"]}
        if not before or before.keys() != after.keys() or not report["held_fonts"]:
            problems.append(f"{label}: missing boxes or real held font requests")
            continue
        if not any(box["hidden"] for box in before.values()) or any(
            box["hidden"] for box in after.values()
        ):
            problems.append(f"{label}: no complete hidden-to-visible observation")
        movement = max(
            abs(after[key][dimension] - old[dimension])
            for key, old in before.items()
            for dimension in ("x", "y", "width", "height", "baseline")
        )
        mismatch = max(abs(box["width"] - box["intrinsic_width"]) for box in after.values())
        if not all(
            math.isfinite(value) and value <= tolerance for value in (movement, mismatch)
        ):
            problems.append(f"{label}: measured geometry exceeds {tolerance}px")
        lines.append(
            f"- {label}: {len(before)} bases; maximum movement {movement:.3f}px; "
            f"maximum final width error {mismatch:.3f}px."
        )
        if report["medium"] == "screen" and not report.get("alternate_certificate", False):
            covered.add((browser, width))
        for name, control in report.get("controls", {}).items():
            if control.get("rejected") and control.get("report", {}).get("findings"):
                controls.add(name)
    required = {
        (browser, width)
        for browser in ("chromium", "firefox", "webkit")
        for width in hypothesis["widths"]
    }
    if not required <= covered:
        problems.append(f"missing registered browser/width cells: {sorted(required - covered)}")
    if not {"removed_width", "stable_wrong_width"} <= controls:
        problems.append("missing rejected movement or stable-wrong-width control")
    return lines, problems


def records(root: Path, directory: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in sorted((root / directory).glob("*.md")):
        errors = check(path)
        if errors:
            raise ValueError(f"{path}: {'; '.join(errors)}")
        payload, _ = payload_and_meta(path)
        identity = payload["id"]
        if identity in result or not path.name.startswith(identity + "-"):
            raise ValueError(f"duplicate or misnamed record: {identity}")
        result[identity] = payload
    return result


def render(root: Path = CAMPAIGN) -> str:
    explorations = records(root, "explorations")
    hypotheses = records(root, "hypotheses")
    experiments = records(root, "experiments")
    board = set(re.findall(r"\bH-\d{3}\b", (root / "ideas.md").read_text()))
    if board != set(hypotheses):
        raise ValueError("idea board and hypothesis registry disagree")
    for identity, hypothesis in hypotheses.items():
        for source in hypothesis["derived_from"]:
            if source not in explorations or identity not in explorations[source]["proposes"]:
                raise ValueError(f"broken exploration reference: {identity} -> {source}")
    for exploration in explorations.values():
        if not set(exploration["proposes"]) <= hypotheses.keys():
            raise ValueError("exploration names an absent hypothesis")
    lines = [
        "# Math Startup Ledger",
        "",
        "Generated by `python -m devtools.report_math_startup`; do not edit by hand.",
        "",
        "Times are milliseconds from navigation to all fourteen correct, visible parameter",
        "labels and readouts. Each arm shows median (minimum to maximum).",
        "",
    ]
    if not experiments:
        lines.extend(["No measurements have been recorded. Both hypotheses remain open.", ""])
    for identity, experiment in experiments.items():
        if not set(experiment.get("hypotheses", [])) <= hypotheses.keys():
            raise ValueError(f"{identity}: absent hypothesis")
        lines.extend([f"## {identity}: {experiment['title']}", ""])
        by_width: dict[int, list[dict[str, Any]]] = defaultdict(list)
        reports: list[dict[str, Any]] = []
        problems: list[str] = []
        for relative in experiment["measurements"]:
            path = (root / relative).resolve()
            if not path.is_relative_to(root.resolve()):
                raise ValueError("measurement path leaves campaign")
            raw = (
                gzip.decompress(path.read_bytes()).decode()
                if path.suffix == ".gz"
                else path.read_text()
            )
            report = json.loads(raw)
            reports.append(report)
            problems.extend(report["findings"])
            for run in report.get("runs", []):
                by_width[run["environment"]["viewport"]["width"]].append(run)
        passes: list[bool] = []
        if experiment["kind"] == "baseline":
            for width, runs in sorted(by_width.items()):
                values = [run["metrics"].get("parameters_ready_ms") for run in runs]
                if len(values) < 3 or any(value is None for value in values):
                    problems.append(f"{width}px: fewer than three complete baseline runs")
                else:
                    lines.append(f"- {width}px: {spread(values)}; {len(values)} runs.")
            verdict = "invalid" if problems else "baseline"
        elif experiment["kind"] == "geometry":
            detail, errors = geometry_result(reports, hypotheses["H-001"])
            lines.extend(detail)
            problems.extend(errors)
            verdict = "invalid" if problems else "accepted"
            if experiment["correctness"] != "passed":
                verdict = f"correctness {experiment['correctness']}"
        else:
            hypothesis = hypotheses["H-002"]
            if set(by_width) != set(hypothesis["widths"]):
                problems.append("comparison does not cover every registered width")
            for width, runs in sorted(by_width.items()):
                try:
                    result = paired_result(runs, hypothesis)
                except (KeyError, ValueError) as error:
                    problems.append(f"{width}px: {error}")
                    continue
                passes.append(result["passes"])
                lo, hi = result["ci95"]
                lines.append(
                    f"- {width}px: control {spread(result['control'])}, candidate "
                    f"{spread(result['candidate'])}; paired change {result['change_pct']:.1f}% "
                    f"(95% interval {lo:.1f}% to {hi:.1f}%; {result['pairs']} pairs)."
                )
            verdict = "accepted" if passes and all(passes) else "rejected"
            if experiment["correctness"] != "passed":
                verdict = f"correctness {experiment['correctness']}"
            if problems:
                verdict = "invalid"
        lines.extend(["", f"Decision: **{verdict}**. {experiment['judgment']}", ""])
        if problems:
            lines.extend([f"- {problem}" for problem in problems] + [""])
    return "\n".join([*lines, FOOTER, ""])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--campaign", type=Path, default=CAMPAIGN)
    args = parser.parse_args(argv)
    output = render(args.campaign)
    path = args.campaign / "ledger.md"
    if args.check:
        if not path.exists() or path.read_text() != output:
            print(f"stale generated ledger: {path}")
            return 1
    else:
        path.write_text(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
