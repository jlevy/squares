"""Report disjoint blocks without removing failed attempts or inventing missing costs."""

from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import Counter
from pathlib import Path

from workbench_tools.cohort_manifest import (
    AttemptStatus,
    Cohort,
    Manifest,
    Purpose,
    read_manifest,
    strict_json,
)
from workbench_tools.trial_records import Trial, admission_reason, trial_from_row


def wilson_interval(hits: int, total: int) -> tuple[float, float] | None:
    """Descriptive 95% binomial interval; independent sampling remains a design assumption."""
    if total == 0:
        return None
    z = 1.959963984540054
    rate = hits / total
    denominator = 1 + z * z / total
    centre = (rate + z * z / (2 * total)) / denominator
    radius = (
        z * math.sqrt(rate * (1 - rate) / total + z * z / (4 * total * total)) / denominator
    )
    return max(0.0, centre - radius), min(1.0, centre + radius)


def _rate(hits: int, total: int) -> dict[str, object]:
    return {
        "hits": hits,
        "denominator": total,
        "rate": hits / total if total else None,
        "wilson_95": wilson_interval(hits, total),
    }


def _distribution(values: list[float]) -> dict[str, object]:
    return {
        "count": len(values),
        "min": min(values) if values else None,
        "median": statistics.median(values) if values else None,
        "max": max(values) if values else None,
    }


def _metrics(trial: Trial) -> dict[str, float | None]:
    absolute = trial.resolved_side - trial.record
    gap = math.ceil(math.sqrt(trial.n)) - trial.record
    return {
        "absolute_excess": absolute,
        "relative_excess_pct": absolute / trial.record * 100,
        "grid_gap_closed": 1 - absolute / gap if gap > 0 else None,
    }


def summarize_cohort(
    cohort: Cohort, trials: list[Trial], *, tolerance_pct: float
) -> dict[str, object]:
    """Join exact seed slots, checking geometry before any accepted block can rank."""
    if not math.isfinite(tolerance_pct) or tolerance_pct < 0:
        raise ValueError("success tolerance must be finite and nonnegative")
    rows: dict[int, Trial] = {}
    effective_configuration: dict[str, object] | None = None
    for trial in trials:
        if trial.seed in rows:
            raise ValueError(f"duplicate trial seed {trial.seed} in {cohort.identifier}")
        if trial.n != cohort.n or trial.style != cohort.style or trial.params != cohort.params:
            raise ValueError(f"trial configuration differs from cohort {cohort.identifier}")
        if trial.configuration is not None:
            effective = trial.configuration.row()
            del effective["seed"]
            if effective_configuration is None:
                effective_configuration = effective
            elif effective != effective_configuration:
                raise ValueError(
                    "a cohort must retain one effective configuration across seeds"
                )
        rows[trial.seed] = trial
    expected = {
        attempt.seed for attempt in cohort.attempts if attempt.status is AttemptStatus.COMPLETED
    }
    if set(rows) != expected:
        raise ValueError(f"completed trial seeds do not match manifest for {cohort.identifier}")

    rejected: Counter[str] = Counter()
    accepted: dict[int, Trial] = {}
    measured_steps = 0
    measured_ms = 0.0
    unknown_steps = 0
    unknown_ms = 0
    repair_sweeps = 0
    repair_ms = 0.0
    physics_ms = 0.0
    unknown_repair = 0
    for attempt in cohort.attempts:
        if attempt.status is AttemptStatus.NOT_STARTED:
            continue
        if attempt.status is AttemptStatus.COMPLETED:
            trial = rows[attempt.seed]
            reason = admission_reason(trial)
            if trial.steps > cohort.max_steps:
                reason = "work-budget-exceeded"
            if trial.repair is not None:
                receipt = trial.repair
                if (
                    receipt.sweeps > cohort.repair_budget
                    or receipt.sweep_limit != cohort.repair_budget
                ):
                    reason = "repair-budget-mismatch"
                if receipt.sweeps >= 0 and all(
                    math.isfinite(value) and value >= 0
                    for value in (receipt.physics_ms, receipt.repair_ms)
                ):
                    repair_sweeps += receipt.sweeps
                    physics_ms += receipt.physics_ms
                    repair_ms += receipt.repair_ms
                else:
                    unknown_repair += 1
            else:
                unknown_repair += 1
            if reason is None:
                accepted[attempt.seed] = trial
            else:
                rejected[reason] += 1
            steps = trial.steps if trial.steps >= 0 else None
            ms = trial.ms if math.isfinite(trial.ms) and trial.ms >= 0 else None
        else:
            steps, ms = attempt.steps, attempt.milliseconds
            unknown_repair += 1
        if steps is None:
            unknown_steps += 1
        else:
            measured_steps += steps
        if ms is None:
            unknown_ms += 1
        else:
            measured_ms += ms

    full_count = len(cohort.attempts) // cohort.block_size
    blocks: list[dict[str, object]] = []
    best_excesses: list[float] = []
    best_normalized: list[float] = []
    hits = 0
    started_blocks = 0
    completed_blocks = 0
    complete_hits = 0
    for index in range(full_count):
        slots = cohort.attempts[index * cohort.block_size : (index + 1) * cohort.block_size]
        valid = [accepted[slot.seed] for slot in slots if slot.seed in accepted]
        best = min(valid, key=lambda trial: trial.resolved_side) if valid else None
        metrics = _metrics(best) if best is not None else None
        hit = best is not None and (best.resolved_side / best.record - 1) * 100 <= tolerance_pct
        started = any(slot.status is not AttemptStatus.NOT_STARTED for slot in slots)
        complete = all(
            slot.status in {AttemptStatus.COMPLETED, AttemptStatus.FAILED} for slot in slots
        )
        hits += hit
        started_blocks += started
        completed_blocks += complete
        complete_hits += hit and complete
        if metrics is not None:
            excess = metrics["relative_excess_pct"]
            assert excess is not None
            best_excesses.append(excess)
            normalized = metrics["grid_gap_closed"]
            if normalized is not None:
                best_normalized.append(normalized)
        blocks.append(
            {
                "index": index,
                "seeds": [slot.seed for slot in slots],
                "statuses": [slot.status.value for slot in slots],
                "accepted": len(valid),
                "best_seed": best.seed if best else None,
                "best": metrics,
                "success": hit,
                "complete": complete,
            }
        )
    status_counts = Counter(attempt.status.value for attempt in cohort.attempts)
    attempted = len(cohort.attempts) - status_counts[AttemptStatus.NOT_STARTED.value]
    accepted_hits = sum(
        (trial.resolved_side / trial.record - 1) * 100 <= tolerance_pct
        for trial in accepted.values()
    )
    return {
        "id": cohort.identifier,
        "n": cohort.n,
        "style": cohort.style,
        "params": cohort.params,
        "effective_configuration": effective_configuration,
        "partition": cohort.partition.value,
        "tolerance_pct": tolerance_pct,
        "counts": {
            "planned": len(cohort.attempts),
            "attempted": attempted,
            **{status.value: status_counts[status.value] for status in AttemptStatus},
            "accepted": len(accepted),
            "rejected": sum(rejected.values()),
        },
        "rejection_reasons": dict(sorted(rejected.items())),
        "trial_success_per_attempt": _rate(accepted_hits, attempted),
        "trial_success_conditional_on_validity": _rate(accepted_hits, len(accepted)),
        "work": {
            "max_steps_per_attempt": cohort.max_steps,
            "repair_budget": cohort.repair_budget,
            "measured_steps": measured_steps,
            "attempts_with_unknown_steps": unknown_steps,
            "measured_milliseconds": measured_ms,
            "attempts_with_unknown_time": unknown_ms,
            "measured_repair_sweeps": repair_sweeps,
            "measured_physics_milliseconds": physics_ms,
            "measured_repair_milliseconds": repair_ms,
            "attempts_with_unknown_repair": unknown_repair,
        },
        "block_size": cohort.block_size,
        "blocks": blocks,
        "trailing_partial_block_seeds": [
            attempt.seed for attempt in cohort.attempts[full_count * cohort.block_size :]
        ],
        "block_success_per_planned_block": _rate(hits, full_count),
        "block_success_per_started_block": _rate(hits, started_blocks),
        "block_success_per_completed_block": _rate(complete_hits, completed_blocks),
        "blocks_without_valid_result": sum(block["best_seed"] is None for block in blocks),
        "best_relative_excess_pct_conditional_on_validity": _distribution(best_excesses),
        "best_grid_gap_closed_conditional_on_defined_score": _distribution(best_normalized),
    }


def report(
    manifest: Manifest, trials: dict[str, list[Trial]], *, tolerance_pct: float = 0.0001
) -> dict[str, object]:
    if set(trials) != {cohort.identifier for cohort in manifest.cohorts}:
        raise ValueError("trial cohort IDs must exactly match the manifest")
    report_source = None
    summaries: list[dict[str, object]] = []
    for cohort in manifest.cohorts:
        first_source = None
        for trial in trials[cohort.identifier]:
            source = trial.source
            if source is None or source.commit != manifest.source_commit:
                raise ValueError("trial source does not match the manifest revision")
            if source.benchmark != manifest.instrument:
                raise ValueError("trial instrument does not match the manifest")
            expected_reference = f"{manifest.reference_source}/n-{cohort.n:03d}.yaml"
            if trial.record_source != expected_reference:
                raise ValueError("trial reference does not match the manifest catalogue")
            if source.dirty and manifest.purpose is Purpose.RESEARCH:
                raise ValueError("research reporting requires a committed instrument")
            if first_source is None:
                first_source = source
            elif source != first_source:
                raise ValueError(
                    "a cohort must use one page, source, and runtime configuration"
                )
            if report_source is None:
                report_source = source
            elif source != report_source:
                raise ValueError(
                    "comparison cohorts must use the same source, page, and runtime"
                )
        summary = summarize_cohort(
            cohort, trials[cohort.identifier], tolerance_pct=tolerance_pct
        )
        summary["source"] = first_source.row() if first_source is not None else None
        summaries.append(summary)
    return {
        "schema": "squares.workbench.block-report/v1",
        "source_commit": manifest.source_commit,
        "reference_source": manifest.reference_source,
        "instrument": manifest.instrument,
        "purpose": manifest.purpose.value,
        "interval_assumption": (
            "Wilson 95%; interpretable as sampling uncertainty only for independent blocks"
        ),
        "cohorts": summaries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("trials", type=Path, help="JSONL with cohort and trial objects")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--tolerance-pct", type=float, default=0.0001)
    args = parser.parse_args()
    manifest = read_manifest(strict_json(args.manifest.read_text(encoding="utf-8")))
    trials: dict[str, list[Trial]] = {cohort.identifier: [] for cohort in manifest.cohorts}
    for number, line in enumerate(args.trials.read_text(encoding="utf-8").splitlines(), 1):
        row = strict_json(line)
        if not isinstance(row, dict) or set(row) != {"cohort", "trial"}:
            raise ValueError(f"line {number}: expected cohort and trial objects")
        key, trial = row["cohort"], row["trial"]
        if not isinstance(key, str) or key not in trials or not isinstance(trial, dict):
            raise ValueError(f"line {number}: unknown cohort or malformed trial")
        trials[key].append(trial_from_row(trial))
    args.out.write_text(
        json.dumps(
            report(manifest, trials, tolerance_pct=args.tolerance_pct),
            indent=2,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
