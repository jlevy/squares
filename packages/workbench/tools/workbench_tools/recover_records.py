"""Measure typed strategy families against retained non-grid packing records."""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from devtools.known_structure import record
from devtools.screen_jamming_targets import non_grid_cases
from workbench_tools.packing_contracts import GeometryCheck
from workbench_tools.strategy_execution import execute_strategy
from workbench_tools.strategy_records import (
    STRATEGY_CONTRACT,
    PackingStrategy,
    decode_strategy,
    strategy_to_row,
)


@dataclass(frozen=True, slots=True)
class RecoverySuccess:
    n: int
    family: str
    seed: int
    side: float
    excess_pct: float
    violation: float
    rung: str
    seconds: float
    geometry: GeometryCheck
    configuration: PackingStrategy

    @property
    def packing_valid(self) -> bool:
        return self.geometry.passed


@dataclass(frozen=True, slots=True)
class RecoveryFailure:
    n: int
    family: str
    seed: int
    error: str


type RecoveryResult = RecoverySuccess | RecoveryFailure


def strategy_for(n: int, family: str, seed: int, budget: int) -> PackingStrategy:
    """Materialize one declared family member without varying it by case."""
    if budget < 1:
        raise ValueError("strategy budget must be positive")
    phases: dict[str, list[dict[str, object]]] = {
        "bare": [
            {"mechanism": "grid"},
            {
                "mechanism": "ratchet",
                "relaxation": 0.1,
                "until": {"steps": budget},
                "schedule": {"attempts": 5, "floor": 1e-3},
            },
        ],
        "mixed": [
            {"mechanism": "grid"},
            {
                "mechanism": "ratchet",
                "relaxation": 0.1,
                "until": {"steps": budget},
                "schedule": {"attempts": 6, "floor": 1e-3, "cold": 0.5},
            },
        ],
        "built": [
            {
                "mechanism": "assemble",
                "structure": {"rung": "contact-graph-with-types"},
                "side": {"relative_to": "record", "factor": 1.12},
            },
            {
                "mechanism": "project",
                "relaxation": 0.1,
                "constraints": {"band": 0.02, "weight": 2.0},
                "until": {"steps": budget},
            },
            {
                "mechanism": "relax",
                "relaxation": 0.1,
                "until": {"steps": max(1, budget // 2)},
            },
            {
                "mechanism": "ratchet",
                "relaxation": 0.1,
                "until": {"steps": budget},
                "schedule": {"attempts": 5, "floor": 1e-3},
            },
        ],
    }
    try:
        selected = phases[family]
    except KeyError as error:
        raise ValueError(f"unknown strategy family {family!r}") from error
    return decode_strategy(
        {
            "contract": STRATEGY_CONTRACT,
            "name": family,
            "n": n,
            "seed": seed,
            "phases": selected,
        }
    )


def run_one(job: tuple[int, str, int, int]) -> RecoveryResult:
    """Run one family member and retain the independent final geometry verdict."""
    n, family, seed, budget = job
    began = time.monotonic()
    try:
        result = execute_strategy(strategy_for(n, family, seed, budget))
    except (ValueError, TypeError, KeyError, AssertionError, OverflowError) as error:
        return RecoveryFailure(n=n, family=family, seed=seed, error=str(error)[:240])
    known = record(n)[1]
    final_phase = result.phases[-1]
    return RecoverySuccess(
        n=n,
        family=family,
        seed=seed,
        side=result.side,
        excess_pct=100.0 * (result.side - known) / known,
        violation=final_phase.violation,
        rung=final_phase.rung,
        seconds=time.monotonic() - began,
        geometry=result.geometry,
        configuration=result.configuration,
    )


def recovery_to_row(result: RecoveryResult) -> dict[str, object]:
    """Encode one recovery result without replacing unsupported values with strings."""
    if isinstance(result, RecoveryFailure):
        return {
            "n": result.n,
            "family": result.family,
            "seed": result.seed,
            "error": result.error,
        }
    return {
        "n": result.n,
        "family": result.family,
        "seed": result.seed,
        "side": result.side,
        "excess_pct": result.excess_pct,
        "violation": result.violation,
        "rung": result.rung,
        "seconds": result.seconds,
        "packing_valid": result.packing_valid,
        "geometry_issues": sorted(issue.value for issue in result.geometry.issues),
        "configuration": strategy_to_row(result.configuration),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-n", type=int, default=30)
    ap.add_argument("--min-n", type=int, default=2)
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--budget", type=int, default=4000)
    ap.add_argument("--families", nargs="+", default=["bare", "mixed", "built"])
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--out", type=Path, default=None)
    options = ap.parse_args()

    if options.seeds < 1 or options.workers < 1:
        raise SystemExit("seeds and workers must be positive")
    for family in options.families:
        strategy_for(1, family, 1, options.budget)
    targets = [n for n, *_ in non_grid_cases(options.max_n) if n >= options.min_n]
    jobs = [
        (n, family, 900 + 31 * index, options.budget)
        for n in targets
        for family in options.families
        for index in range(options.seeds)
    ]
    print(f"{len(targets)} non-grid cases, {len(jobs)} runs on {options.workers} workers")
    began = time.monotonic()
    with mp.Pool(options.workers) as pool:
        rows = list(pool.imap_unordered(run_one, jobs))
    if options.out:
        options.out.write_text(
            json.dumps([recovery_to_row(row) for row in rows], allow_nan=False),
            encoding="utf-8",
        )

    good = [row for row in rows if isinstance(row, RecoverySuccess) and row.packing_valid]
    print(
        f"\n{len(good)} of {len(rows)} runs ended on an independently checked packing, "
        f"{time.monotonic() - began:.0f}s"
    )
    header = f"{'n':>4} {'grid':>5} {'record':>11}"
    for family in options.families:
        header += f" {family:>16}"
    print(header)
    for n in targets:
        line = f"{n:>4} {int(np.ceil(np.sqrt(n))):>5} {record(n)[1]:>11.6f}"
        for family in options.families:
            selected = [row for row in good if row.n == n and row.family == family]
            line += (
                f" {min(row.excess_pct for row in selected):>+15.3f}%"
                if selected
                else f" {'-':>16}"
            )
        print(line)
    for family in options.families:
        selected = [row for row in good if row.family == family]
        if selected:
            best = {
                n: min(row.excess_pct for row in selected if row.n == n)
                for n in {row.n for row in selected}
            }
            print(
                f"{family}: median excess {np.median(list(best.values())):+.3f}%, "
                f"reached {len(best)} of {len(targets)} cases, "
                f"within 1% on {sum(value < 1.0 for value in best.values())}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
