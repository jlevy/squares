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
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from sqpack.quench import quench_bracket, solve_to_fixed_point

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
    if first and shifted and abs(first[0] - shifted[0]) > 1e-9:
        return (
            f"D-015: s(theta) moved by {abs(first[0] - shifted[0]):.2e} under a pure "
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


def main() -> int:
    checks = [check_budget_binds, check_quench_deterministic, check_angle_search_converges]
    failures = [msg for msg in (c() for c in checks) if msg]
    for msg in failures:
        print(f"  REGRESSION  {msg}", file=sys.stderr)
    if failures:
        return 1
    print(f"  {len(checks)} regression checks pass (D-002, D-015, D-016, D-019)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
