#!/usr/bin/env python3
"""Regression checks, each naming the defect it exists to prevent.

The defect log's most useful column is `regression`, and its most useful list is the one
where that column reads `none` -- fixes whose cause was removed with nothing left behind
to stop it returning. D-010 and D-017 are the same mistake made twice, six days and two
authors apart, because the first fix had none.

This file is where those checks live. Every one is labelled with the defect id it
guards, so the log's claim and the code that backs it cannot drift.

Usage: uv run --frozen python -m devtools.check_regressions
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
from types import SimpleNamespace
from unittest.mock import patch

import sqpack.research.quench as quench_module
from sqpack.research.quench import (
    CellSolveResult,
    FixedPointResult,
    _free_sweep,  # pyright: ignore[reportPrivateUsage]
    _OutOfTimeError,  # pyright: ignore[reportPrivateUsage]
    _solve_adjacent_cell_closure,  # pyright: ignore[reportPrivateUsage]
    quench_bracket,
    solve_to_fixed_point,
)
from sqpack.workers import worker_count

ROOT = Path(__file__).resolve().parent.parent
BIN = ROOT / "sqsearch/target/release/sqsearch"
TRUMP = 3.877083590022814


def seed_config() -> dict:
    return json.loads(
        subprocess.run(
            [sys.executable, "-m", "cases.trump11.export_seed"],
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


def check_cell_solve_is_not_a_quench() -> str | None:  # noqa: PLR0911
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

    closures = []
    original_fixed_point = solve_to_fixed_point

    def trace_adjacent_closures(*args, **kwargs):
        result = original_fixed_point(*args, **kwargs)
        if result is not None and result.reason.startswith("adjacent cell closure"):
            closures.append(result.reason)
        return result

    with patch.object(
        quench_module,
        "solve_to_fixed_point",
        side_effect=trace_adjacent_closures,
    ):
        r = quench_bracket(best["x"], best["y"], best["t"], time_budget=60)
    if r.side - analytic > 1e-12:
        return (
            f"D-029: quench_bracket on exp-002 seed 2 reached only {r.side - analytic:+.2e}; "
            "the angle half has regressed, and n = 10 would read as an exploration failure"
        )
    if not closures:
        return "D-168: n=10 no longer exercises the adjacent-cell closure control"
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
            side_effect=[
                CellSolveResult(outcome="optimal", side=2.0, x=[0.5], y=[0.5]),
                CellSolveResult(outcome="optimal", side=2.1, x=[0.5], y=[0.5]),
            ],
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


def check_adjacent_cell_closure_is_bounded() -> str | None:
    """D-168: equal adjacent cells settle, but unequal objectives remain a refusal."""
    row_a = (0, 1, 1.0, 0.0, 1.0, 1.0)
    row_b = (0, 1, 0.0, 1.0, 1.0, 1.0)
    cells = [[row_a], [row_b]]

    def reread(_x, _y, _theta, preferred=None):
        return [row_b] if preferred == [row_a] else [row_a]

    def equal_solve(_theta, cell, _n):
        marker = 0.0 if cell == [row_a] else 1.0
        return CellSolveResult(outcome="optimal", side=2.0, x=[marker, 1.0], y=[0.0, 0.0])

    with (
        patch.object(quench_module, "choose_cell", side_effect=reread),
        patch.object(quench_module, "solve_cell", side_effect=equal_solve),
    ):
        closure, solves, _ = _solve_adjacent_cell_closure([0.0, 0.0], cells, 2)
    if closure is None or closure.cell_count != 2 or solves != 2:
        return f"D-168: finite equal-objective closure did not settle: {closure!r}, {solves=}"

    def unequal_solve(_theta, cell, _n):
        marker = 0.0 if cell == [row_a] else 1.0
        side = 2.0 + marker * 2 * quench_module.LP_FEASIBLE_EPS
        return CellSolveResult(outcome="optimal", side=side, x=[marker, 1.0], y=[0.0, 0.0])

    with (
        patch.object(quench_module, "choose_cell", side_effect=reread),
        patch.object(quench_module, "solve_cell", side_effect=unequal_solve),
    ):
        rejected, _, _ = _solve_adjacent_cell_closure([0.0, 0.0], cells, 2)
    if rejected is not None:
        return "D-168: unequal adjacent objectives were flattened into a settlement"
    return None


def check_cell_solve_failure_is_typed() -> str | None:  # noqa: PLR0911
    """D-164: a numerical residual rejection is not mathematical infeasibility."""
    cell = [(0, 1, 1.0, 0.0, 1.0, 1.0)]
    violating = SimpleNamespace(
        success=True,
        status=0,
        message="synthetic optimum",
        x=[2.0, 1.5 - 1.2e-10, 0.5, 0.5, 0.5],
    )
    with patch.object(quench_module, "linprog", return_value=violating):
        rejected = quench_module.solve_cell([0.0, 0.0], cell, 2)
    if (
        rejected.outcome != "postcheck_rejection"
        or rejected.max_violation is None
        or rejected.max_violation_row != 8
        or rejected.max_violation_kind != "pair"
        or rejected.solver_calls != quench_module.MAX_RESIDUAL_SOLVER_CALLS
        or len(rejected.residual_receipts) != quench_module.MAX_RESIDUAL_SOLVER_CALLS
    ):
        return f"D-164: numerical residual rejection lost its cause or row: {rejected!r}"

    repaired = SimpleNamespace(
        success=True,
        status=0,
        message="synthetic repaired optimum",
        x=[2.0, 1.5, 0.5, 0.5, 0.5],
    )
    with patch.object(quench_module, "linprog", side_effect=[violating, repaired]):
        accepted = quench_module.solve_cell([0.0, 0.0], cell, 2)
    if (
        accepted.outcome != "optimal"
        or accepted.solver_calls != 2
        or accepted.repair_rows != [8]
        or len(accepted.repair_margins) != 1
        or [receipt.offending_rows for receipt in accepted.residual_receipts] != [(8,), ()]
    ):
        return f"D-164: bounded one-retry repair was not retained: {accepted!r}"

    newly_offending = SimpleNamespace(
        success=True,
        status=0,
        message="synthetic new-row optimum",
        x=[2.0, 1.5 + 1.2e-10, 0.5, 0.5, 0.5],
    )
    with patch.object(
        quench_module,
        "linprog",
        side_effect=[violating, newly_offending, repaired],
    ):
        cascaded = quench_module.solve_cell([0.0, 0.0], cell, 2)
    if (
        cascaded.outcome != "optimal"
        or cascaded.solver_calls != 3
        or [receipt.offending_rows for receipt in cascaded.residual_receipts]
        != [(8,), (1,), ()]
        or cascaded.max_violation is None
        or cascaded.max_violation > quench_module.LP_FEASIBLE_EPS
    ):
        return f"D-199: a row exposed by the first repair was not repaired: {cascaded!r}"

    infeasible = SimpleNamespace(success=False, status=2, message="synthetic infeasible")
    with patch.object(quench_module, "linprog", return_value=infeasible):
        impossible = quench_module.solve_cell([0.0, 0.0], cell, 2)
    if impossible.outcome != "infeasible":
        return f"D-164: mathematical infeasibility lost its cause: {impossible!r}"
    with patch.object(quench_module, "solve_cell", return_value=impossible):
        propagated = solve_to_fixed_point([0.0, 0.0], [0.5, 1.5], [0.5, 0.5], 2)
    if propagated.settled or "mathematically infeasible" not in propagated.reason:
        return f"D-164: fixed-point layer erased the cell-solve cause: {propagated!r}"

    failed = SimpleNamespace(success=False, status=4, message="synthetic numerical failure")
    with patch.object(quench_module, "linprog", return_value=failed):
        numerical = quench_module.solve_cell([0.0, 0.0], cell, 2)
    if numerical.outcome != "solver_failure":
        return f"D-164: solver failure lost its cause: {numerical!r}"

    containment_violation = SimpleNamespace(
        success=True,
        status=0,
        message="synthetic wall violation",
        x=[1.0, 0.5 + 2e-10, 0.5],
    )
    with patch.object(quench_module, "linprog", return_value=containment_violation):
        outside = quench_module.solve_cell([0.0], [], 1)
    if (
        outside.outcome != "postcheck_rejection"
        or outside.max_violation_kind != "containment"
        or outside.max_violation_row != 1
    ):
        return f"D-169: containment-row violation escaped the complete replay: {outside!r}"

    n3_theta = [-9.35043360154506e-10, 0.30887703227181684, 0.8953194347614593]
    n3_cell = [
        (0, 1, 9.35043360154506e-10, 1.0, 1.128332272702862, 1.0),
        (0, 2, 1.0, -9.35043360154506e-10, 1.2028392061250828, -1.0),
        (1, 2, 0.6252695585800809, 0.7804088538151465, 1.1931580404947508, -1.0),
    ]
    retained = quench_module.solve_cell(n3_theta, n3_cell, 3)
    if (
        retained.outcome != "optimal"
        or retained.solver_calls != 2
        or retained.repair_rows != [12]
        or len(retained.repair_margins) != 1
        or abs(retained.repair_margins[0] - 2.1999601312595589e-10) > 1e-15
        or retained.side is None
        or abs(retained.side - 2.405678412790218) > 1e-12
    ):
        return f"D-164: retained n=3 seed-1 failing cell did not replay: {retained!r}"

    n4_theta = [
        1.5707963263740359,
        -1.0000151967426634e-09,
        -1.0000151967426634e-09,
        1.5707963263740359,
    ]
    n4_cell = [
        (0, 1, -1.0, 4.208607408719852e-10, 1.0000000002895773, -1.0),
        (0, 2, 1.0000151967426634e-09, 1.0, 1.0000000002895773, 1.0),
        (0, 3, -1.0, 4.208607408719852e-10, 1.0, -1.0),
        (1, 2, 1.0, -1.0000151967426634e-09, 1.0, -1.0),
        (1, 3, 1.0000151967426634e-09, 1.0, 1.0000000002895773, -1.0),
        (2, 3, 4.208607408719852e-10, 1.0, 1.0000000002895773, -1.0),
    ]
    tied = quench_module.solve_cell(n4_theta, n4_cell, 4)
    if (
        tied.outcome != "optimal"
        or tied.solver_calls != 2
        or tied.repair_rows != [16, 21]
        or len(tied.repair_margins) != 2
        or tied.max_violation is None
        or tied.max_violation > quench_module.LP_FEASIBLE_EPS
    ):
        return f"D-171: tied offending rows did not share one bounded repair: {tied!r}"

    # Retained n=10 seed-14 ladder cell that exposed D-199. The first solve violates
    # rows 49 and 66; their repair shifts solver-scale residual to previously clean row
    # 61. Re-observing and tightening that row must accept under the unchanged all-row
    # screen. This direct cell replay costs milliseconds; it replaces a blind 109-second
    # deep-golden retry as the diagnostic control.
    n10_theta = [
        0.8040123494998975,
        -7.263096240823372e-10,
        -7.263096240823372e-10,
        -7.263096240823372e-10,
        -7.263096240823372e-10,
        -7.263096240823372e-10,
        -7.263096240823372e-10,
        0.7601925633609738,
        -7.263096240823372e-10,
        0.8114266576034375,
    ]
    n10_cell = [
        (0, 1, -0.720145739884132, 0.6938228256022831, 1.2069842827336483, 1.0),
        (0, 2, 1.0, -7.263096240823372e-10, 1.2069842827336483, -1.0),
        (0, 3, 7.263096240823372e-10, 1.0, 1.2069842827336483, -1.0),
        (0, 4, -0.720145739884132, 0.6938228256022831, 1.2069842827336483, 1.0),
        (0, 5, -0.720145739884132, 0.6938228256022831, 1.2069842827336483, -1.0),
        (0, 6, -0.720145739884132, 0.6938228256022831, 1.2069842827336483, -1.0),
        (0, 7, 0.7247033362741131, 0.6890610091952452, 1.0214229153373688, -1.0),
        (0, 8, 0.6938228256022831, 0.720145739884132, 1.2069842827336483, 1.0),
        (0, 9, 0.6938228256022831, 0.720145739884132, 1.0036933771587326, -1.0),
        (1, 2, 1.0, -7.263096240823372e-10, 1.0, -1.0),
        (1, 3, 7.263096240823372e-10, 1.0, 1.0, -1.0),
        (1, 4, 1.0, -7.263096240823372e-10, 1.0, -1.0),
        (1, 5, 7.263096240823372e-10, 1.0, 1.0, -1.0),
        (1, 6, 7.263096240823372e-10, 1.0, 1.0, -1.0),
        (1, 7, 7.263096240823372e-10, 1.0, 1.2068821727476227, -1.0),
        (1, 8, 1.0, -7.263096240823372e-10, 1.0, 1.0),
        (1, 9, 7.263096240823372e-10, 1.0, 1.2068672684570778, -1.0),
        (2, 3, 1.0, -7.263096240823372e-10, 1.0, 1.0),
        (2, 4, 7.263096240823372e-10, 1.0, 1.0, 1.0),
        (2, 5, 1.0, -7.263096240823372e-10, 1.0, 1.0),
        (2, 6, 1.0, -7.263096240823372e-10, 1.0, 1.0),
        (2, 7, 7.263096240823372e-10, 1.0, 1.2068821727476227, -1.0),
        (2, 8, 1.0, -7.263096240823372e-10, 1.0, 1.0),
        (2, 9, -0.7252701151288633, 0.6884644218120246, 1.2068672684570778, -1.0),
        (3, 4, 7.263096240823372e-10, 1.0, 1.0, 1.0),
        (3, 5, 1.0, -7.263096240823372e-10, 1.0, 1.0),
        (3, 6, 1.0, -7.263096240823372e-10, 1.0, 1.0),
        (3, 7, 1.0, -7.263096240823372e-10, 1.2068821727476227, -1.0),
        (3, 8, 7.263096240823372e-10, 1.0, 1.0, 1.0),
        (3, 9, -0.7252701151288633, 0.6884644218120246, 1.2068672684570778, 1.0),
        (4, 5, 1.0, -7.263096240823372e-10, 1.0, 1.0),
        (4, 6, 1.0, -7.263096240823372e-10, 1.0, 1.0),
        (4, 7, 7.263096240823372e-10, 1.0, 1.2068821727476227, -1.0),
        (4, 8, 1.0, -7.263096240823372e-10, 1.0, 1.0),
        (4, 9, -0.7252701151288633, 0.6884644218120246, 1.2068672684570778, -1.0),
        (5, 6, 7.263096240823372e-10, 1.0, 1.0, 1.0),
        (5, 7, 1.0, -7.263096240823372e-10, 1.2068821727476227, -1.0),
        (5, 8, 7.263096240823372e-10, 1.0, 1.0, 1.0),
        (5, 9, -0.7252701151288633, 0.6884644218120246, 1.2068672684570778, 1.0),
        (6, 7, 1.0, -7.263096240823372e-10, 1.2068821727476227, -1.0),
        (6, 8, 7.263096240823372e-10, 1.0, 1.0, 1.0),
        (6, 9, 1.0, -7.263096240823372e-10, 1.2068672684570778, -1.0),
        (7, 8, 0.7247033362741131, 0.6890610091952452, 1.2068821727476227, 1.0),
        (7, 9, 0.7247033362741131, 0.6890610091952452, 1.0249497518540158, 1.0),
        (8, 9, 0.6884644218120246, 0.7252701151288633, 1.2068672684570778, -1.0),
    ]
    shifted = quench_module.solve_cell(n10_theta, n10_cell, 10)
    if (
        shifted.outcome != "optimal"
        or shifted.solver_calls != 3
        or [receipt.offending_rows for receipt in shifted.residual_receipts]
        != [(49, 66), (61,), ()]
        or shifted.max_violation is None
        or shifted.max_violation > quench_module.LP_FEASIBLE_EPS
    ):
        return f"D-199: retained n=10 moving-residual cell did not settle: {shifted!r}"
    return None


# Named at module level so a process pool can pickle them by reference. The eight are
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
    "check_adjacent_cell_closure_is_bounded",
    "check_cell_solve_failure_is_typed",
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
        "(D-002, D-015, D-016, D-019, D-029, D-036, D-132, D-164, D-168, D-169, "
        "D-171, D-199)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
