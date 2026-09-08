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
        if run.get("mode", "full") != hypothesis.get("required_mode", "full"):
            raise ValueError("measurement mode differs from the registered mode")
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
    sampler: dict[str, list[float]] = {}
    if "maximum_sampler_fraction" in hypothesis:
        for label, values in (("control", control), ("candidate", candidate)):
            costs = [pair[label]["metrics"].get("sampler_total_ms") for pair in pairs.values()]
            if any(
                not isinstance(cost, (int, float)) or not math.isfinite(cost) or cost < 0
                for cost in costs
            ):
                raise ValueError("missing or invalid sampler cost")
            sampler[label] = costs
            if (
                statistics.median(costs) / statistics.median(values)
                > hypothesis["maximum_sampler_fraction"]
            ):
                raise ValueError(f"{label}: sampler overhead exceeds the registered fraction")
    lower, upper = interval(changes)
    return {
        "pairs": len(pairs),
        "control": control,
        "candidate": candidate,
        "change_pct": statistics.median(changes),
        "ci95": (lower, upper),
        "passes": upper <= hypothesis["maximum_ci95_change_pct"],
        "sampler": sampler,
    }


def spread(values: list[float]) -> str:
    """A median is always printed with the observed range."""
    return f"{statistics.median(values):.1f} ({min(values):.1f} to {max(values):.1f})"


def _nonnegative(value: object) -> float | None:
    if (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
        and value >= 0
    ):
        return float(value)
    return None


def _startup_observation(run: dict[str, Any]) -> dict[str, float]:
    """Optional diagnostics never change the registered decision or drop partial samples."""
    values: dict[str, float] = {}
    runtime = _nonnegative(run.get("metrics", {}).get("runtime_available_ms"))
    if runtime is not None:
        values["runtime"] = runtime
    for key in ("katex_calls", "render_calls", "hydrate_calls"):
        count = _nonnegative(run.get("counters", {}).get(key))
        if count is not None and count.is_integer():
            values[key] = count
    fonts = run.get("fonts")
    if isinstance(fonts, list):
        values["font_calls"] = len(fonts)
        durations = []
        for font in fonts:
            if not isinstance(font, dict) or font.get("outcome") != "resolved":
                break
            start, end = _nonnegative(font.get("start_ms")), _nonnegative(font.get("end_ms"))
            if start is None or end is None or end < start:
                break
            durations.append(end - start)
        if durations and len(durations) == len(fonts):
            values["font_median"] = statistics.median(durations)
            values["font_max"] = max(durations)
    targets = run.get("targets")
    if not isinstance(targets, list) or len(targets) != 14:
        return values
    if not all(isinstance(target, dict) for target in targets):
        return values
    slug = targets[0].get("slug")
    if not isinstance(slug, str) or not slug:
        return values
    readouts = {f"s-{key}-{slug}" for key in ("phi", "theta", "d", "D", "B", "prod")}
    expected = readouts | {f"figure6-{slug}-label-{index}" for index in range(8)}
    times: dict[str, float] = {}
    for target in targets:
        identifier = target.get("id")
        time = _nonnegative(target.get("first_visible_ms"))
        if (
            not isinstance(identifier, str)
            or identifier in times
            or time is None
            or target.get("slug") != slug
            or target.get("correct") is not True
            or target.get("exposed") is not True
        ):
            return values
        times[identifier] = time
    ready = _nonnegative(run.get("metrics", {}).get("parameters_ready_ms"))
    if (
        times.keys() == expected
        and ready is not None
        and math.isclose(max(times.values()), ready, rel_tol=0, abs_tol=1e-6)
    ):
        values["readouts_ready"] = max(times[key] for key in readouts)
        values["readouts_gap"] = ready - values["readouts_ready"]
    return values


def startup_diagnostics(runs: list[dict[str, Any]]) -> list[str]:
    """Compare complete optional observations, preserving each run's weighting."""
    arms = [
        [_startup_observation(run) for run in runs if run.get("label") == label]
        for label in ("control", "candidate")
    ]
    if not all(arms):
        return []
    rows = []
    for key, label in (
        ("runtime", "Runtime available (ms)"),
        ("katex_calls", "KaTeX render calls"),
        ("render_calls", "Runtime render calls"),
        ("hydrate_calls", "Runtime hydrate calls"),
        ("font_calls", "Font load calls"),
        ("font_median", "Per-run median font promise (ms)"),
        ("font_max", "Per-run longest font promise (ms)"),
        ("readouts_ready", "All six dynamic readouts exposed (ms)"),
        ("readouts_gap", "Dynamic readouts to all fourteen (ms)"),
    ):
        if all(key in observation for arm in arms for observation in arm):
            control, candidate = [spread([value[key] for value in arm]) for arm in arms]
            rows.append(f"| {label} | {control} | {candidate} |")
    if not rows:
        return []
    lines = [
        "",
        "Startup diagnostics, median (minimum to maximum) across runs:",
        "",
        "| Observation | Control | Candidate |",
        "| --- | --- | --- |",
        *rows,
        "",
    ]
    if any("font promise" in row for row in rows):
        lines.extend(
            [
                (
                    "Font promise durations include JavaScript scheduling; "
                    "they are not isolated font-decoding measurements."
                ),
                "",
            ]
        )
    return lines


def geometry_result(
    reports: list[dict[str, Any]], hypothesis: dict[str, Any]
) -> tuple[list[str], list[str]]:
    """Require the declared browser matrix and retain the falsification controls."""
    lines: list[str] = []
    problems: list[str] = []
    covered: set[tuple[str, int, str]] = set()
    printed_contexts: set[str] = set()
    controls: set[str] = set()
    tolerance = hypothesis["maximum_math_box_displacement_px"]
    for report in reports:
        browser, width = report["browser"], report["width"]
        label = f"{browser} {width}px {report['medium']}"
        context = f"{report.get('font_set', 'custom')}-{report.get('prose_font', 'serif')}"
        if "font_contexts" in hypothesis:
            label += f" {context}"
        before = {box["key"]: box for box in report["before"]}
        after = {box["key"]: box for box in report["after"]}
        for stage, boxes in (("before", before), ("after", after)):
            if len(report[stage]) != len(boxes):
                problems.append(f"{label}: duplicate {stage} box keys")
        if "font_contexts" in hypothesis:
            for stage in ("before", "after"):
                coverage = report.get(f"coverage_{stage}", {})
                groups = {box.get("group") for box in report[stage]}
                if (
                    not all(
                        coverage.get(key, 0) > 0 for key in ("targets", "formulas", "bases")
                    )
                    or coverage.get("bases") != len(report[stage])
                    or coverage.get("formulas") != len(groups)
                    or None in groups
                    or coverage.get("missing", ["absent"])
                    or coverage.get("unreserved", ["absent"])
                    or coverage.get("variant_errors", ["absent"])
                    or coverage.get("duplicate_ids", ["absent"])
                ):
                    problems.append(f"{label}: incomplete {stage} formula coverage")
            if any(
                before[key].get("group") != after[key].get("group")
                for key in before.keys() & after.keys()
            ):
                problems.append(f"{label}: formula groups changed between observations")
        if report.get("alternate_certificate", False):
            label += " alternate certificate"
        problems.extend(f"{label}: {finding}" for finding in report["findings"])
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
            covered.add((browser, width, context))
        if report["medium"] == "print" and browser == "chromium":
            printed_contexts.add(context)
        for name, control in report.get("controls", {}).items():
            if control.get("rejected") and control.get("report", {}).get("findings"):
                controls.add(name)
    required = {
        (browser, width, context)
        for browser in ("chromium", "firefox", "webkit")
        for width in hypothesis["widths"]
        for context in hypothesis.get("font_contexts", ["custom-serif"])
    }
    if not required <= covered:
        problems.append(f"missing registered browser/width cells: {sorted(required - covered)}")
    if not {"removed_width", "stable_wrong_width"} <= controls:
        problems.append("missing rejected movement or stable-wrong-width control")
    if "font_contexts" in hypothesis and "missing_reservation" not in controls:
        problems.append("missing rejected pre-discovery reservation control")
    if (
        "font_contexts" in hypothesis
        and not set(hypothesis["font_contexts"]) <= printed_contexts
    ):
        problems.append("missing registered print font settings")
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
            if experiment["kind"] != "geometry":
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
            geometry = [
                hypotheses[key]
                for key in experiment.get("hypotheses", [])
                if hypotheses[key]["criterion"] == "geometry"
            ]
            if len(geometry) != 1:
                raise ValueError(
                    "geometry experiment must name exactly one geometry hypothesis"
                )
            detail, errors = geometry_result(reports, geometry[0])
            lines.extend(detail)
            problems.extend(errors)
            verdict = "invalid" if problems else "accepted"
            if experiment["correctness"] != "passed":
                verdict = f"correctness {experiment['correctness']}"
        else:
            latency = [
                hypotheses[key]
                for key in experiment["hypotheses"]
                if hypotheses[key]["criterion"] == "paired_latency"
            ]
            if len(latency) != 1:
                raise ValueError("comparison must name exactly one latency hypothesis")
            hypothesis = latency[0]
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
                if result["sampler"]:
                    lines.append(
                        "  Recorded sampler work: control "
                        f"{spread(result['sampler']['control'])}, "
                        f"candidate {spread(result['sampler']['candidate'])}."
                    )
                lines.extend(startup_diagnostics(runs))
            verdict = "accepted" if passes and all(passes) else "rejected"
            if experiment["correctness"] != "passed":
                verdict = f"correctness {experiment['correctness']}"
            if problems:
                verdict = "invalid"
        if verdict == "accepted" and experiment.get("needs_review", False):
            verdict = "needs review"
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
