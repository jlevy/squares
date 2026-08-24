#!/usr/bin/env python3
"""Regression checks, each naming the defect it exists to prevent.

The defect log's most useful column is `regression`, and its most useful list is the one
where that column reads `none` -- fixes whose cause was removed with nothing left behind
to stop it returning. D-010 and D-017 are the same mistake made twice, six days and two
authors apart, because the first fix had none.

This file is where those checks live. Every one is labelled with the defect id it
guards, so the log's claim and the code that backs it cannot drift.

Usage:  python3 tools/regression_test.py
"""

from __future__ import annotations

import json
import math
import random
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import sqpack.quench as quench_module
from sqpack.quench import (
    FixedPointResult,
    _free_sweep,  # pyright: ignore[reportPrivateUsage]
    _OutOfTimeError,  # pyright: ignore[reportPrivateUsage]
    quench_bracket,
    solve_to_fixed_point,
)
from sqpack.workers import worker_count

BIN = ROOT / "sqsearch/target/release/sqsearch"
TRUMP = 3.877083590022814


def seed_config() -> dict:
    return json.loads(
        subprocess.run(
            [sys.executable, str(ROOT / "tools/export_trump11.py")],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    )


def check_budget_binds() -> str | None:
    """D-002: a restart cap once made --budget-moves inert, so 'equal budget' was a lie.

    Doubling the declared budget must roughly double the work actually done.
    """
    if not BIN.exists():
        return None
    moves = []
    for budget in (2_000_000, 4_000_000):
        out = subprocess.run(
            [
                str(BIN),
                "--n",
                "5",
                "--seed",
                "3",
                "--chains",
                "1",
                "--budget-moves",
                str(budget),
            ],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        summary = next(json.loads(line) for line in out.splitlines() if '"summary"' in line)
        moves.append(summary["moves"])
    ratio = moves[1] / max(moves[0], 1)
    if not 1.7 < ratio < 2.3:
        return (
            f"D-002: doubling the budget changed work by {ratio:.2f}x "
            f"({moves[0]} -> {moves[1]}); the budget is not binding"
        )
    return None


def check_quench_deterministic() -> str | None:
    """D-015: the angle objective was once path-dependent, so it was not a function.

    The same input must produce the same output, exactly.
    """
    d = seed_config()
    rnd = random.Random(5)
    x = [v + 1e-3 * rnd.uniform(-1, 1) for v in d["x"]]
    y = [v + 1e-3 * rnd.uniform(-1, 1) for v in d["y"]]
    t = [v + 1e-3 * rnd.uniform(-1, 1) for v in d["t"]]
    a = quench_bracket(x, y, t)
    b = quench_bracket(x, y, t)
    if a.side != b.side or a.theta != b.theta:
        return (
            f"D-015: two quenches of one input disagree "
            f"({a.side!r} vs {b.side!r}); the objective is path-dependent again"
        )
    # And the underlying evaluation must not depend on the centres it is handed.
    first = solve_to_fixed_point(t, x, y, len(x))
    shifted = solve_to_fixed_point(t, [v + 3.0 for v in x], [v - 2.0 for v in y], len(x))
    if first and shifted and abs(first.side - shifted.side) > 1e-9:
        return (
            f"D-015: s(theta) moved by {abs(first.side - shifted.side):.2e} under a pure "
            f"translation of the centres it was handed"
        )
    return None


def check_angle_search_converges() -> str | None:
    """D-016 and D-019: the angle search once stalled early, and once could not stop.

    From a 1e-3 perturbation of a known optimum it must land on it, and quickly.
    """
    d = seed_config()
    rnd = random.Random(1)
    x = [v + 1e-3 * rnd.uniform(-1, 1) for v in d["x"]]
    y = [v + 1e-3 * rnd.uniform(-1, 1) for v in d["y"]]
    t = [v + 1e-3 * rnd.uniform(-1, 1) for v in d["t"]]
    r = quench_bracket(x, y, t, time_budget=60)
    if abs(r.side - TRUMP) > 1e-9:
        return (
            f"D-016: quench from a 1e-3 perturbation reached {r.side - TRUMP:+.2e}, "
            f"outside 1e-9; the angle search has stalled early again"
        )
    if "time budget" in r.reason:
        return "D-019: the angle search hit its wall budget on a cell that should converge"
    # D-019 specifically: angles far from zero must not defeat the line search.
    far = [v + 4 * math.pi for v in t]
    r2 = quench_bracket(x, y, far, time_budget=60)
    if "time budget" in r2.reason:
        return (
            "D-019: angles offset by four full turns defeat the line search; "
            "the folding or the tolerance scaling has regressed"
        )
    return None


def check_cell_solve_is_not_a_quench() -> str | None:
    """D-029: freezing the angles measures the cell, not the basin.

    An agent checking exp-001's polish/exploration split built a probe that did one LP
    solve at fixed angles, called it "the quench", saw it fail to reach the analytic
    optimum at `n = 10`, and retracted a correct finding. On exp-002's seed 2 the
    fixed-angle solve improves the annealer's output by *nothing at all* -- the centres
    are already optimal at those angles, and every remaining unit of gap is angular.
    That is what the RIGHT basin looks like when the residual is in the angles, and it
    was read as evidence of the wrong one.

    The check pins the discrimination rather than the story: the cell solve must stay
    put, and the quench with its angle half must reach the optimum.
    """
    archive = (
        ROOT
        / "campaign/series/series-000-smoke-and-calibration/results"
        / "exp-002-baseline-n10-positive-control.jsonl"
    )
    if not archive.exists():
        return None
    analytic = 3 + 0.5 * math.sqrt(2)  # s(10), Stromquist 2003 Theorem 1
    rows = [json.loads(line) for line in archive.read_text().splitlines() if line.strip()]
    chains = [
        r for r in rows if r.get("kind") == "chain" and r.get("n") == 10 and r.get("seed") == 2
    ]
    if not chains:
        return None
    best = min(chains, key=lambda r: r["best_side"])

    quarter = math.pi / 2
    frozen = [t % quarter for t in best["t"]]
    solved = solve_to_fixed_point(frozen, best["x"], best["y"], 10)
    if solved is None:
        return (
            "D-029: the fixed-angle solve on exp-002 seed 2 returned no solution at all; "
            "it is supposed to succeed and merely fall short, so the LP or the cell "
            "read has regressed"
        )
    cell_side = solved.side
    if cell_side - analytic < 1e-6:
        return (
            f"D-029: the fixed-angle cell solve reached {cell_side - analytic:+.2e} of the "
            "analytic optimum. It is supposed to be unable to -- if it now can, the "
            "measurement that separates a cell from a basin has stopped separating them"
        )

    r = quench_bracket(best["x"], best["y"], best["t"], time_budget=60)
    if r.side - analytic > 1e-12:
        return (
            f"D-029: quench_bracket on exp-002 seed 2 reached only {r.side - analytic:+.2e}; "
            "the angle half has regressed, and n = 10 would read as an exploration failure"
        )
    return None


def check_free_sweep_deadline_is_not_convergence() -> str | None:
    """D-036: an incomplete free sweep must not certify convergence."""
    try:
        _free_sweep(
            1.0,
            [0.5],
            [0.5],
            [0.0],
            1,
            deadline=time.monotonic() - 1.0,
        )
    except _OutOfTimeError:
        return None
    return "D-036: an already-expired free sweep returned as if every angle was checked"


def check_fixed_cell_termination_is_typed() -> str | None:
    """D-132: an incumbent is not a fixed point unless the cell actually settled."""
    settled = solve_to_fixed_point([0.0], [0.5], [0.5], 1)
    if settled is None or not settled.settled or settled.reason != "cell fixed point":
        return f"D-132: the known n=1 fixed point was not marked settled: {settled!r}"

    capped = solve_to_fixed_point([0.0], [0.5], [0.5], 1, max_iters=0)
    if capped is None or capped.settled or capped.reason != "cell iteration limit":
        return f"D-132: an iteration cap was not exposed as unsettled: {capped!r}"

    cell_a = [(0, 1, 1.0, 0.0, 1.0, 1.0)]
    cell_b = [(0, 1, 0.0, 1.0, 1.0, 1.0)]
    with (
        patch.object(quench_module, "choose_cell", side_effect=[cell_a, cell_b]),
        patch.object(
            quench_module,
            "solve_cell",
            side_effect=[(2.0, [0.5], [0.5]), (2.1, [0.5], [0.5])],
        ),
    ):
        worse = solve_to_fixed_point([0.0], [0.5], [0.5], 1)
    if worse is None or worse.settled or worse.reason != "re-read cell worse":
        return f"D-132: a worse transition was not exposed as unsettled: {worse!r}"

    with patch.object(
        quench_module,
        "solve_to_fixed_point",
        return_value=FixedPointResult(
            side=2.0,
            x=[0.5],
            y=[0.5],
            solves=1,
            changes=1,
            settled=False,
            reason="synthetic iteration limit",
        ),
    ):
        outer = quench_bracket([0.5], [0.5], [0.0], time_budget=1.0)
    if outer.converged or "fixed cell unsettled" not in outer.reason:
        return f"D-132: outer quench promoted an unsettled inner solve: {outer!r}"
    return None


# Named at module level so a process pool can pickle them by reference. The five are
# independent -- each builds its own fixture and reads nothing the others write -- and
# each is seconds of LP solving, so running them serially made this file the gate's
# second-longest step for no reason. `pool.map` preserves submission order, so the
# failure list reads the same as it did serially.
CHECKS = (
    "check_budget_binds",
    "check_quench_deterministic",
    "check_angle_search_converges",
    "check_cell_solve_is_not_a_quench",
    "check_free_sweep_deadline_is_not_convergence",
    "check_fixed_cell_termination_is_typed",
)


def _run_check(name: str) -> str | None:
    return globals()[name]()


def main() -> int:
    with ProcessPoolExecutor(max_workers=worker_count(len(CHECKS))) as pool:
        failures = [msg for msg in pool.map(_run_check, CHECKS) if msg]
    for msg in failures:
        print(f"  REGRESSION  {msg}", file=sys.stderr)
    if failures:
        return 1
    print(
        f"  {len(CHECKS)} regression checks pass "
        "(D-002, D-015, D-016, D-019, D-029, D-036, D-132)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
