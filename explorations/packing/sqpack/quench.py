"""LP-in-cell quench: turn a float configuration into a named, exactly-valued basin.

The structural fact this rests on, established in the standing review (R-2) and
verified against Trump's packing to `9e-16`:

> For fixed angles, and a fixed choice of which axis separates each pair, minimising
> the enclosing side is a LINEAR PROGRAM.

Fix every angle and every pair's separating axis and sign -- together, a *cell* of
configuration space -- and each square's extent is affine in its centre, every
separating-axis condition is one linear inequality, containment is linear, and the
objective is linear. All the nonconvexity of the problem lives in the angles and in
the combinatorial choice of cell.

So a quench is: pick the cell the configuration is in, solve it exactly, step the
angles downhill, repeat. The endpoint is a genuine cell-optimum rather than wherever
an annealer happened to get tired -- which is what makes "basin" mean anything, and
what the census, the atlas and every descriptor are built on.

This module is `f64` throughout and SCREENS: the LP optimum is exact within its cell
to solver precision, not exact in the algebraic sense. Certification remains
`sqpack.verify` over the packing's own number field.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from itertools import product
from typing import Literal

import numpy as np
from scipy.optimize import linprog


class _OutOfTimeError(Exception):
    """Raised inside a line search when the quench's wall budget expires."""


class _FixedCellUnsettledError(Exception):
    """Raised when an angle evaluation did not reach its own cell fixed point."""


# How much constraint violation a returned LP solution may carry. Two orders below the
# tightened solver tolerance, and far below any quantity the campaign reports.
LP_FEASIBLE_EPS = 1e-10
MAX_ADJACENT_CELL_CLOSURE = 64


@dataclass
class QuenchResult:
    """Where a configuration landed, and what it cost to get there."""

    side: float
    x: list[float]
    y: list[float]
    theta: list[float]
    lp_solves: int
    angle_steps: int
    converged: bool
    cell_changes: int
    contacts: list[tuple[int, int]] = field(default_factory=list)
    reason: str = ""
    fixed_point_evaluations: int = 0
    fixed_point_settled: int = 0
    fixed_point_unsettled: int = 0


@dataclass
class FixedPointResult:
    """One fixed-angle cell iteration, including whether its cell actually settled."""

    side: float
    x: list[float]
    y: list[float]
    solves: int
    changes: int
    settled: bool
    reason: str


@dataclass
class CellSolveResult:
    """One LP outcome, retaining numerical failure separately from infeasibility."""

    outcome: Literal["optimal", "infeasible", "solver_failure", "postcheck_rejection"]
    side: float | None = None
    x: list[float] = field(default_factory=list)
    y: list[float] = field(default_factory=list)
    solver_status: int | None = None
    detail: str = ""
    max_violation: float | None = None
    max_violation_row: int | None = None
    max_violation_kind: Literal["containment", "pair"] | None = None
    solver_calls: int = 1
    repair_row: int | None = None
    repair_margin: float | None = None


@dataclass
class _AdjacentClosureResult:
    """A bounded, equal-objective closure of adjacent fixed-angle LP cells."""

    side: float
    x: list[float]
    y: list[float]
    cell_count: int


def _axes(theta: float) -> list[tuple[float, float]]:
    """The two edge normals of a square at this angle."""
    c, s = math.cos(theta), math.sin(theta)
    return [(c, s), (-s, c)]


def _half_extent(theta: float, ax: float, ay: float) -> float:
    """Half-width of a unit square at `theta`, projected on the axis `(ax, ay)`."""
    c, s = math.cos(theta), math.sin(theta)
    return 0.5 * (abs(ax * c + ay * s) + abs(-ax * s + ay * c))


def choose_cell(
    x,
    y,
    theta,
    preferred: list[tuple[int, int, float, float, float, float]] | None = None,
) -> list[tuple[int, int, float, float, float, float]]:
    """Pick, for each pair, the axis and sign that separates it best.

    This is what reads a cell off a configuration. The chosen axis is the one with the
    greatest separation (or least overlap), which is the standard separating-axis
    choice and the one that stays valid under small motion.

    Two things are hoisted out of the pair loop, both of them identities rather than
    approximations, because this function is the hottest thing in the quench: it runs
    once per `solve_cell` and the fixed-point loop calls it thousands of times per
    round.

    First, `theta` is FIXED for the whole LP -- that is the premise the cell rests on --
    so each square's cos/sin is computed once here rather than 4n times per pair by
    `_axes` and `_half_extent`. At n = 11 that is 22 transcendentals in place of ~1100.

    Second, the sum of half-extents is the SAME on all four axes for two unit squares:
    `1/2 + 1/2(|cos D| + |sin D|)` with `D` the angle between them. That is the identity
    `sqsearch::geom::pair_penalty` already uses and that its selftest checks against the
    naive four-axis form; the Python side was still paying for four separate
    evaluations of a quantity it could compute once. `_half_extent` is retained because
    `solve_cell` uses it for the containment rows, where the axis is a container edge
    rather than a square's own normal and the identity does not apply.

    Verified equivalent over 17k random rows at n in {5, 10, 11, 17}: identical axis and
    sign choices, `h` agreeing to 1 ulp.
    """
    n = len(x)
    cs = [(math.cos(t), math.sin(t)) for t in theta]
    cell = []
    for i in range(n):
        ci, si = cs[i]
        xi, yi = x[i], y[i]
        for j in range(i + 1, n):
            cj, sj = cs[j]
            dx, dy = xi - x[j], yi - y[j]
            h = 0.5 + 0.5 * (abs(ci * cj + si * sj) + abs(si * cj - ci * sj))
            # Four candidate axes, always: two edge normals from each square. Seeded
            # with the worst possible gap rather than None so the result is a value
            # rather than an optional the caller has to reason about.
            best = (-math.inf, 1.0, 0.0, 1.0)
            for ax, ay in ((ci, si), (-si, ci), (cj, sj), (-sj, cj)):
                d = dx * ax + dy * ay
                gap = abs(d) - h
                if gap > best[0]:
                    best = (gap, ax, ay, 1.0 if d >= 0 else -1.0)
            if preferred is not None:
                pi, pj, pax, pay, _, psign = preferred[len(cell)]
                if (pi, pj) != (i, j):
                    raise ValueError("preferred cell has a different pair order")
                preferred_gap = psign * (dx * pax + dy * pay) - h
                # At a corner contact, two SAT axes can differ only by LP-scale
                # roundoff. Flipping between them made a deterministic two-cycle on
                # the n=10 positive control. Keep the current valid cell across such a
                # tie; change only when another axis is materially better.
                if preferred_gap >= best[0] - LP_FEASIBLE_EPS:
                    best = (preferred_gap, pax, pay, psign)
            gap, ax, ay, sign = best
            cell.append((i, j, ax, ay, h, sign))
    return cell


def solve_cell(theta, cell, n: int) -> CellSolveResult:
    """Minimise one cell while preserving why a solve did not yield usable evidence.

    Variables are `[s, x_0..x_{n-1}, y_0..y_{n-1}]`. Containment is four inequalities
    per square against the variable side; separation is one per pair, because the axis
    AND the sign are both fixed by the cell -- which is exactly what removes the
    absolute value and leaves a linear program.
    """
    nv = 1 + 2 * n
    obj = np.zeros(nv)
    obj[0] = 1.0
    rows, rhs = [], []

    for k in range(n):
        e = _half_extent(theta[k], 1.0, 0.0), _half_extent(theta[k], 0.0, 1.0)
        for coord, half in ((1 + k, e[0]), (1 + n + k, e[1])):
            lo = np.zeros(nv)
            lo[coord] = -1.0
            rows.append(lo)
            rhs.append(-half)  # centre >= half
            hi = np.zeros(nv)
            hi[coord] = 1.0
            hi[0] = -1.0
            rows.append(hi)
            rhs.append(-half)  # centre <= s - half

    for i, j, ax, ay, h, sign in cell:
        row = np.zeros(nv)
        row[1 + i] = -sign * ax
        row[1 + j] = sign * ax
        row[1 + n + i] = -sign * ay
        row[1 + n + j] = sign * ay
        rows.append(row)
        rhs.append(-h)  # sign * (c_i - c_j) . a >= h

    # HiGHS defaults to a primal feasibility tolerance of 1e-7, which is LARGER than
    # the quantities this quench is measuring: a solution may violate its own
    # separation constraint by ~1e-7 and still be reported optimal, which shows up
    # downstream as a side length below the standing best -- a record "beaten" entirely
    # by solver slack. Measured, not feared: an untightened solve returned
    # s = 3.877083568 against Trump's 3.877083590, with pair (4,8) overlapping by
    # 9.876e-08. This is the same tolerance-is-a-blind-spot failure the exact verifier
    # exists to close, appearing one layer up in the refiner.
    a_ub = np.array(rows)
    b_ub = np.array(rhs)

    def run_lp(active_rhs):
        return linprog(
            obj,
            A_ub=a_ub,
            b_ub=active_rhs,
            bounds=[(0, None)] + [(None, None)] * (2 * n),
            method="highs",
            options={
                "primal_feasibility_tolerance": 1e-10,
                "dual_feasibility_tolerance": 1e-10,
            },
        )

    res = run_lp(b_ub)
    if not res.success:
        return CellSolveResult(
            outcome="infeasible" if res.status == 2 else "solver_failure",
            solver_status=int(res.status),
            detail=str(res.message),
        )
    v = res.x
    violations = a_ub @ v - b_ub
    max_row = int(np.argmax(violations))
    max_violation = max(float(violations[max_row]), 0.0)
    max_kind: Literal["containment", "pair"] = "containment" if max_row < 4 * n else "pair"
    solver_calls = 1
    repair_row = None
    repair_margin = None

    # HiGHS can report an optimum just beyond its own requested feasibility screen.
    # Retry exactly once, tightening only the offending RHS by the measured violation
    # plus the original screen. The second result is still replayed against ORIGINAL
    # rows. This changes neither the acceptance tolerance nor an infeasible/failure
    # outcome, and the one-retry bound prevents a numerical repair loop.
    if max_violation > LP_FEASIBLE_EPS:
        repair_row = max_row
        repair_margin = max_violation + LP_FEASIBLE_EPS
        repair_rhs = np.array(b_ub, copy=True)
        repair_rhs[repair_row] -= repair_margin
        repaired = run_lp(repair_rhs)
        solver_calls = 2
        if repaired.success:
            res = repaired
            v = repaired.x
            violations = a_ub @ v - b_ub
            max_row = int(np.argmax(violations))
            max_violation = max(float(violations[max_row]), 0.0)
            max_kind = "containment" if max_row < 4 * n else "pair"
        else:
            return CellSolveResult(
                outcome="postcheck_rejection",
                side=float(v[0]),
                x=list(v[1 : 1 + n]),
                y=list(v[1 + n :]),
                solver_status=int(repaired.status),
                detail=f"bounded residual retry failed: {repaired.message}",
                max_violation=max_violation,
                max_violation_row=max_row,
                max_violation_kind=max_kind,
                solver_calls=solver_calls,
                repair_row=repair_row,
                repair_margin=repair_margin,
            )
    x, y = list(v[1 : 1 + n]), list(v[1 + n :])
    if max_violation > LP_FEASIBLE_EPS:
        return CellSolveResult(
            outcome="postcheck_rejection",
            side=float(v[0]),
            x=x,
            y=y,
            solver_status=int(res.status),
            detail="optimal LP solution exceeded the declared residual screen",
            max_violation=max_violation,
            max_violation_row=max_row,
            max_violation_kind=max_kind,
            solver_calls=solver_calls,
            repair_row=repair_row,
            repair_margin=repair_margin,
        )
    return CellSolveResult(
        outcome="optimal",
        side=float(v[0]),
        x=x,
        y=y,
        solver_status=int(res.status),
        detail=str(res.message),
        max_violation=max_violation,
        max_violation_row=max_row,
        max_violation_kind=max_kind,
        solver_calls=solver_calls,
        repair_row=repair_row,
        repair_margin=repair_margin,
    )


def _cell_failure_reason(result: CellSolveResult) -> str:
    """Stable evidence label for a non-optimal cell solve."""
    if result.outcome == "postcheck_rejection":
        assert result.max_violation is not None
        return (
            f"post-check rejection ({result.max_violation_kind} row "
            f"{result.max_violation_row}, max violation {result.max_violation:.3e})"
        )
    if result.outcome == "infeasible":
        return "mathematically infeasible cell"
    return f"solver failure (status {result.solver_status}: {result.detail})"


def _incoming_side(theta, x, y) -> float:
    """Enclosing side of an input whose first LP did not yield an accepted point."""
    extents = [
        (
            _half_extent(angle, 1.0, 0.0),
            _half_extent(angle, 0.0, 1.0),
        )
        for angle in theta
    ]
    return max(
        max(a + e[0] for a, e in zip(x, extents, strict=True))
        - min(a - e[0] for a, e in zip(x, extents, strict=True)),
        max(b + e[1] for b, e in zip(y, extents, strict=True))
        - min(b - e[1] for b, e in zip(y, extents, strict=True)),
    )


def _solve_adjacent_cell_closure(  # noqa: PLR0911 - each failed obligation refuses closure
    theta,
    cycle_cells,
    n: int,
    *,
    max_cells: int = MAX_ADJACENT_CELL_CLOSURE,
) -> tuple[_AdjacentClosureResult | None, int, str]:
    """Close a finite cell cycle without claiming a global fixed-angle optimum.

    A tie locus can make the cell reread alternate even though every adjacent LP has
    the same objective.  Starting only from rows observed in the cycle, enumerate their
    Cartesian product, solve every cell, and add any row choice exposed by rereading a
    solution.  The closure is settled only when that process stops, every solve passes,
    every reread remains inside the enumerated row choices, and the full objective
    spread is within the LP screen.  The hard cap makes combinatorial growth a typed
    refusal rather than a hidden search.

    This certifies one finite adjacent-cell closure.  It does not enumerate every cell
    at these angles and therefore does not certify a global fixed-angle optimum.
    """
    if not cycle_cells:
        return None, 0, "empty cycle"
    options = [[row] for row in cycle_cells[0]]
    for cell in cycle_cells[1:]:
        if len(cell) != len(options):
            return None, 0, "cell row-count mismatch"
        for index, row in enumerate(cell):
            if row not in options[index]:
                options[index].append(row)

    solves = 0
    while True:
        cell_count = math.prod(len(rows) for rows in options)
        if cell_count > max_cells:
            return None, solves, f"closure exceeded {max_cells}-cell cap"
        outcomes = []
        expanded = False
        for selection in product(*options):
            cell = list(selection)
            solved = solve_cell(theta, cell, n)
            solves += solved.solver_calls
            if solved.outcome != "optimal":
                return None, solves, _cell_failure_reason(solved)
            assert solved.side is not None
            side, x, y = solved.side, solved.x, solved.y
            reread = choose_cell(x, y, theta, preferred=cell)
            if len(reread) != len(options):
                return None, solves, "reread row-count mismatch"
            for index, row in enumerate(reread):
                if row not in options[index]:
                    options[index].append(row)
                    expanded = True
            outcomes.append((side, x, y))
        if expanded:
            continue
        sides = [outcome[0] for outcome in outcomes]
        if max(sides) - min(sides) > LP_FEASIBLE_EPS:
            return None, solves, "adjacent objectives disagree"
        # Keep the conservative (largest-side) representative.  Differences within
        # this closure are solver-scale, but choosing the smallest would flatter it.
        side, x, y = max(outcomes, key=lambda outcome: outcome[0])
        return _AdjacentClosureResult(side, x, y, cell_count), solves, ""


def solve_to_fixed_point(  # noqa: PLR0911 - each termination reason is retained evidence
    theta, x, y, n: int, max_iters: int = 12
):
    """Solve, re-read the cell from the solution, and repeat until the cell settles.

    A single `solve_cell` optimises the cell suggested by the *incoming* centres, but
    its own solution may lie in a different cell -- so the value it returns is an upper
    bound on the true optimum at these angles, and it depends on where the caller
    happened to start. That path dependence makes `s(theta)` ill-defined, which in turn
    makes any angle search optimise a moving target: measured here, it is what made
    Powell and Nelder-Mead both do *worse* than plain descent.

    Iterating to a cell fixed point removes it.  The incumbent is returned even when a
    transition is infeasible, worse, or reaches the iteration cap, but ``settled`` is
    false in those cases.  Callers may use such an incumbent as exploratory data; they
    may not call an outer quench converged from it.
    """
    solves = changes = 0
    cell = choose_cell(x, y, theta)
    history = [cell]
    seen = {tuple(cell): 0}
    first = solve_cell(theta, cell, n)
    solves += first.solver_calls
    if first.outcome != "optimal":
        return FixedPointResult(
            side=first.side if first.side is not None else _incoming_side(theta, x, y),
            x=first.x or list(x),
            y=first.y or list(y),
            solves=solves,
            changes=changes,
            settled=False,
            reason=f"initial cell {_cell_failure_reason(first)}",
        )
    assert first.side is not None
    best = (first.side, first.x, first.y)
    for _ in range(max_iters):
        side, x, y = best
        nxt = choose_cell(x, y, theta, preferred=cell)
        if nxt == cell:
            return FixedPointResult(
                side=side,
                x=x,
                y=y,
                solves=solves,
                changes=changes,
                settled=True,
                reason="cell fixed point",
            )
        nxt_key = tuple(nxt)
        if nxt_key in seen:
            closure, closure_solves, closure_reason = _solve_adjacent_cell_closure(
                theta, history[seen[nxt_key] :], n
            )
            solves += closure_solves
            if closure is not None:
                return FixedPointResult(
                    side=closure.side,
                    x=closure.x,
                    y=closure.y,
                    solves=solves,
                    changes=changes,
                    settled=True,
                    reason=f"adjacent cell closure ({closure.cell_count} cells)",
                )
            return FixedPointResult(
                side=side,
                x=x,
                y=y,
                solves=solves,
                changes=changes,
                settled=False,
                reason=f"cell cycle ({closure_reason})",
            )
        seen[nxt_key] = len(history)
        history.append(nxt)
        cell = nxt
        changes += 1
        solved_trial = solve_cell(theta, cell, n)
        solves += solved_trial.solver_calls
        if solved_trial.outcome != "optimal":
            # Keep the incumbent, but preserve the cause rather than turning every LP
            # refusal into mathematical infeasibility.
            return FixedPointResult(
                side=side,
                x=x,
                y=y,
                solves=solves,
                changes=changes,
                settled=False,
                reason=f"re-read cell {_cell_failure_reason(solved_trial)}",
            )
        assert solved_trial.side is not None
        trial = (solved_trial.side, solved_trial.x, solved_trial.y)
        # HiGHS is asked for 1e-10 primal/dual feasibility. Comparing two LP
        # objectives at 1e-15 treated solver-scale roundoff as a genuinely worse cell
        # and is exactly what D-132 exposed on the n=10 positive control.
        if trial[0] > side + LP_FEASIBLE_EPS:
            return FixedPointResult(
                side=side,
                x=x,
                y=y,
                solves=solves,
                changes=changes,
                settled=False,
                reason="re-read cell worse",
            )
        best = trial
    side, x, y = best
    return FixedPointResult(
        side=side,
        x=x,
        y=y,
        solves=solves,
        changes=changes,
        settled=False,
        reason="cell iteration limit",
    )


def quench(  # noqa: PLR0911 - each scientific stop condition returns its evidence
    x,
    y,
    theta,
    *,
    max_rounds: int = 60,
    angle_step: float = 1e-3,
    tol: float = 1e-12,
    polish_angles: bool = True,
) -> QuenchResult:
    """Alternate cell solves with angle descent until the side stops improving.

    The angle half is finite-difference descent with a shrinking step: `s(theta)` is
    piecewise-linear-ish and non-smooth at cell boundaries, so a step that fails is
    halved rather than trusted, and the loop stops when the step can no longer buy
    anything. That is the part of H-002 that was untested -- the single-cell solve was
    already verified.
    """
    x, y, theta = list(x), list(y), list(theta)
    n = len(x)
    lp_solves = angle_steps = cell_changes = 0
    # The finite-difference probe and the line-search step are DIFFERENT quantities.
    # Sharing one (the first version of this did) makes the descent eat itself: every
    # failed step halves the probe too, and once the probe falls under LP precision the
    # gradient is noise, so the loop stops on a spurious "no improving step" long
    # before it reaches the cell optimum.
    fd_h = 1e-7

    solved = solve_to_fixed_point(theta, x, y, n)
    if solved is None:
        return QuenchResult(
            side=float("inf"),
            x=x,
            y=y,
            theta=theta,
            lp_solves=lp_solves,
            angle_steps=0,
            converged=False,
            cell_changes=0,
            reason="initial cell infeasible",
        )
    if not solved.settled:
        return QuenchResult(
            side=solved.side,
            x=solved.x,
            y=solved.y,
            theta=theta,
            lp_solves=solved.solves,
            angle_steps=0,
            converged=False,
            cell_changes=solved.changes,
            reason=f"fixed cell unsettled: {solved.reason}",
        )
    side, x, y = solved.side, solved.x, solved.y
    lp_solves += solved.solves
    cell_changes += solved.changes
    cell = choose_cell(x, y, theta)

    step = angle_step
    for _ in range(max_rounds):
        # Re-read the cell: the LP solution may have moved squares into a different
        # separating-axis regime, and solving a stale cell optimises the wrong problem.
        new_cell = choose_cell(x, y, theta)
        if new_cell != cell:
            solved = solve_to_fixed_point(theta, x, y, n)
            if solved is None:
                break
            if not solved.settled:
                return QuenchResult(
                    side=solved.side,
                    x=solved.x,
                    y=solved.y,
                    theta=theta,
                    lp_solves=lp_solves + solved.solves,
                    angle_steps=angle_steps,
                    converged=False,
                    cell_changes=cell_changes + solved.changes + 1,
                    reason=f"fixed cell unsettled: {solved.reason}",
                )
            side, x, y = solved.side, solved.x, solved.y
            lp_solves += solved.solves
            cell_changes += solved.changes + 1
            cell = choose_cell(x, y, theta)

        if not polish_angles:
            break

        # Finite-difference gradient in angle space, one LP per angle.
        grad = []
        for k in range(n):
            probe = list(theta)
            probe[k] += fd_h
            trial = solve_to_fixed_point(probe, x, y, n)
            lp_solves += trial.solves if trial else 1
            if trial is not None and not trial.settled:
                return QuenchResult(
                    side=side,
                    x=x,
                    y=y,
                    theta=theta,
                    lp_solves=lp_solves,
                    angle_steps=angle_steps,
                    converged=False,
                    cell_changes=cell_changes + trial.changes,
                    reason=f"fixed cell unsettled during angle probe: {trial.reason}",
                )
            grad.append((trial.side - side) / fd_h if trial else 0.0)

        norm = math.sqrt(sum(g * g for g in grad))
        if norm < tol:
            return QuenchResult(
                side=side,
                x=x,
                y=y,
                theta=theta,
                lp_solves=lp_solves,
                angle_steps=angle_steps,
                converged=True,
                cell_changes=cell_changes,
                reason="angle gradient vanished",
            )

        # Reset the line search each round: a step that failed against one cell says
        # nothing about the next, and carrying the shrunken step forward is what turns
        # a slow descent into a stalled one.
        step = angle_step
        moved = False
        while step > 1e-13:
            probe = [t - step * g / norm for t, g in zip(theta, grad, strict=True)]
            trial = solve_to_fixed_point(probe, x, y, n)
            lp_solves += trial.solves if trial else 1
            if trial is not None and not trial.settled:
                return QuenchResult(
                    side=side,
                    x=x,
                    y=y,
                    theta=theta,
                    lp_solves=lp_solves,
                    angle_steps=angle_steps,
                    converged=False,
                    cell_changes=cell_changes + trial.changes,
                    reason=f"fixed cell unsettled during line search: {trial.reason}",
                )
            if trial and trial.side < side - tol:
                side, x, y = trial.side, trial.x, trial.y
                theta = probe
                cell = choose_cell(x, y, theta)
                angle_steps += 1
                moved = True
                break
            step *= 0.5
        if not moved:
            return QuenchResult(
                side=side,
                x=x,
                y=y,
                theta=theta,
                lp_solves=lp_solves,
                angle_steps=angle_steps,
                converged=True,
                cell_changes=cell_changes,
                reason="no improving angle step",
            )

    return QuenchResult(
        side=side,
        x=x,
        y=y,
        theta=theta,
        lp_solves=lp_solves,
        angle_steps=angle_steps,
        converged=False,
        cell_changes=cell_changes,
        reason="round limit",
    )


def contacts(x, y, theta, tol: float = 1e-9) -> list[tuple[int, int]]:
    """Pairs touching within `tol` -- the contact structure of the quenched packing."""
    n = len(x)
    out = []
    for i in range(n):
        for j in range(i + 1, n):
            dx, dy = x[i] - x[j], y[i] - y[j]
            gap = max(
                abs(dx * ax + dy * ay)
                - (_half_extent(theta[i], ax, ay) + _half_extent(theta[j], ax, ay))
                for ax, ay in _axes(theta[i]) + _axes(theta[j])
            )
            if abs(gap) <= tol:
                out.append((i, j))
    return out


def angle_classes(theta, tol: float = 1e-6) -> list[list[int]]:
    """Group squares by shared tilt, modulo the quarter turn a square is invariant under.

    Records use very few distinct angles -- Trump's `n = 11` uses two, `s(17)` two -- so
    the honest dimension of the angle search is the number of CLASSES, not `n`.
    """
    quarter = math.pi / 2
    groups: list[list[int]] = []
    reps: list[float] = []
    for k, t in enumerate(theta):
        folded = t % quarter
        for gi, rep in enumerate(reps):
            d = abs(folded - rep)
            if min(d, quarter - d) <= tol:
                groups[gi].append(k)
                break
        else:
            groups.append([k])
            reps.append(folded)
    return groups


def _bracket_min(f, x0: float, span: float, tol: float = 1e-15, max_iters: int = 120):
    """Golden section on one coordinate. Converges on a KINK, where descent cannot.

    The objective must be deterministic in its argument, which is why every evaluation
    re-solves from the same reference centres rather than threading updated ones: a
    bracketing method on a path-dependent objective loses the unimodality it needs, and
    measured here that converged to the wrong tilt by 1.2e-02.
    """
    gr = (math.sqrt(5) - 1) / 2
    lo, hi = x0 - span, x0 + span
    a, b = hi - gr * (hi - lo), lo + gr * (hi - lo)
    fa, fb = f(a), f(b)
    # The tolerance is scaled to the value being bracketed, and the iteration count is
    # capped. An ABSOLUTE tolerance is unreachable once the argument is large enough
    # that one ULP exceeds it -- measured at theta = 14.14 rad, where ULP is 1.78e-15
    # against an absolute 1e-15, so the interval could never shrink past the bound and
    # the search spun until its wall budget (defect D-019). Golden section reaches
    # machine precision in about 70 steps from any sane bracket; beyond that it is not
    # converging, it is stuck.
    bound = tol * (1.0 + abs(x0))
    iters = 0
    while hi - lo > bound and iters < max_iters:
        iters += 1
        if fa < fb:
            hi, b, fb = b, a, fa
            a = hi - gr * (hi - lo)
            fa = f(a)
        else:
            lo, a, fa = a, b, fb
            b = lo + gr * (hi - lo)
            fb = f(b)
    return (lo + hi) / 2


def _free_sweep(
    side,
    x,
    y,
    theta,
    n,
    *,
    deadline,
    span: float = 1e-3,
    solve_fixed=solve_to_fixed_point,
):
    """One bracketing pass over every angle individually, no classes.

    Returns (side, x, y, theta, lp_solves). Used to test whether a class-converged
    point is coordinate-wise stationary rather than an artifact of the merge
    tolerance. Raises `_OutOfTimeError` unless every coordinate was checked, and
    `_FixedCellUnsettledError` rather than evaluating a path-dependent incumbent.
    """
    lp_solves = 0
    best = (side, list(x), list(y), list(theta))
    for k in range(n):
        if time.monotonic() > deadline:
            raise _OutOfTimeError
        ref_x, ref_y = list(best[1]), list(best[2])
        base = best[3][k]

        def probe(value, k=k, ref_x=ref_x, ref_y=ref_y, angles=tuple(best[3])):
            nonlocal lp_solves
            if time.monotonic() > deadline:
                raise _OutOfTimeError
            trial_theta = list(angles)
            trial_theta[k] = value
            got = solve_fixed(trial_theta, ref_x, ref_y, n)
            lp_solves += got.solves
            if not got.settled:
                raise _FixedCellUnsettledError(got.reason)
            return got.side

        angle = _bracket_min(probe, base, span)
        trial_theta = list(best[3])
        trial_theta[k] = angle
        got = solve_fixed(trial_theta, ref_x, ref_y, n)
        if time.monotonic() > deadline:
            raise _OutOfTimeError
        lp_solves += got.solves
        if not got.settled:
            raise _FixedCellUnsettledError(got.reason)
        if got.side < best[0] - 1e-13:
            best = (got.side, got.x, got.y, trial_theta)
    return best[0], best[1], best[2], best[3], lp_solves


def quench_bracket(  # noqa: PLR0911 - each scientific stop condition returns its evidence
    x,
    y,
    theta,
    *,
    max_sweeps: int = 200,
    span: float = 0.05,
    span_min: float = 1e-9,
    span_shrink: float = 0.1,
    tol: float = 1e-12,
    class_tol: float = 1e-2,
    time_budget: float = 30.0,
    free_pass: bool = True,
) -> QuenchResult:
    """Quench whose angle half brackets rather than descends.

    Trump's tested shared-tilt slice has a corner -- distinct one-sided slopes measured
    in exp-006 -- so a smooth local model is misspecified at that point. This variant
    does cyclic coordinate search over the angle CLASSES, each coordinate solved by
    golden section. It needs no derivative and reached the solver floor on the proved
    controls; that evidence is empirical, not a general convergence theorem.

    ## The angle window, and why its schedule is adaptive

    `span` bounds how far one sweep may move an angle, and it narrows **only when a
    sweep fails to improve** -- the standard pattern-search rule, which gives the
    schedule a reason rather than a cadence. Narrowing it every sweep regardless was
    D-030: from annealer output that is right, because the angles arrive nearly correct,
    but from a cold start they must move O(0.1) rad and the window was down to 2.4e-05
    by sweep 12. The search then crawled instead of arriving, never converging and never
    saying so.

    So this works from both ends now, which it did not before:

    * **polishing** annealer output, unchanged in behaviour and accuracy -- exp-008's
      five archived `n = 10` seeds still reach the analytic value, median gap 8.9e-16
      against the 1.3e-15 recorded, both far below the tier's own 1e-11 floor (D-021);
    * **exploring** from a uniform random start, which previously converged on 0 of 8
      cold `n = 5` starts and now converges on 12 of 12, reaching the proved
      `s(5) = 2.707106781187` exactly.

    `max_sweeps` is a backstop rather than a budget -- the wall clock and the narrowing
    schedule bound the work -- which is why its default is 200 rather than the 12 that
    used to double as the termination condition.
    """
    # Fold every angle into [0, pi/2) first. A unit square is invariant under a quarter
    # turn, so an angle of 14.14 rad names the same square as 0.09 rad -- but at a
    # floating-point scale where one ULP is 8x coarser, which is what made the line
    # search unable to converge at all (D-019). Folding is free and removes the whole
    # regime: the annealer accumulates rotations without wrapping, so its output
    # routinely arrives many turns from zero.
    quarter = math.pi / 2
    theta = [t % quarter for t in theta]
    x, y = list(x), list(y)
    n = len(x)
    lp_solves = angle_steps = 0
    fixed_point_evaluations = fixed_point_settled = fixed_point_unsettled = 0

    def evaluate_fixed_point(eval_theta, eval_x, eval_y, eval_n):
        """The only fixed-point call path, so every outcome enters the receipt."""
        nonlocal fixed_point_evaluations, fixed_point_settled, fixed_point_unsettled
        result = solve_to_fixed_point(eval_theta, eval_x, eval_y, eval_n)
        fixed_point_evaluations += 1
        if result.settled:
            fixed_point_settled += 1
        else:
            fixed_point_unsettled += 1
        return result

    def audited_result(**fields):
        return QuenchResult(
            **fields,
            fixed_point_evaluations=fixed_point_evaluations,
            fixed_point_settled=fixed_point_settled,
            fixed_point_unsettled=fixed_point_unsettled,
        )

    # A per-call wall budget, because a quench that does not return is worse than one
    # that returns a worse answer: it takes the whole round with it. Measured on n = 5
    # seed 4, where a cell that solves in 5 ms sent the sweep past 145 s. Hitting the
    # budget is a RESULT and is reported as one, never silently.
    deadline = time.monotonic() + time_budget

    solved = evaluate_fixed_point(theta, x, y, n)
    if not solved.settled:
        return audited_result(
            side=solved.side,
            x=solved.x,
            y=solved.y,
            theta=theta,
            lp_solves=solved.solves,
            angle_steps=0,
            converged=False,
            cell_changes=solved.changes,
            reason=f"fixed cell unsettled: {solved.reason}",
        )
    side, x, y, changes = solved.side, solved.x, solved.y, solved.changes
    lp_solves += solved.solves

    # `class_tol` is the one real knob, and it is doing more than grouping. A search
    # arrives with every angle slightly different, so a tight tolerance sees eleven
    # classes where the packing has two, and searches eleven non-smooth coordinates
    # instead of one. Merging at 1e-2 rad recovers the structure and, measured, moves
    # the result four orders: 1.5e-08 at eleven classes against 1.5e-11 at two, in an
    # eighth of the LP solves. The cost is that two genuinely distinct angles closer
    # than the tolerance are forced equal -- so a packing whose record needs that is
    # out of reach until this is swept rather than fixed.
    # The angle window the class search may move within, and the schedule for narrowing
    # it. It narrows only when a sweep FAILS to improve -- see the tail of the loop.
    span0 = span
    groups = angle_classes(theta, class_tol)
    stop_reason = "sweep limit"
    for _ in range(max_sweeps):
        improved = False
        for group in groups:
            if time.monotonic() > deadline:
                return audited_result(
                    side=side,
                    x=x,
                    y=y,
                    theta=theta,
                    lp_solves=lp_solves,
                    angle_steps=angle_steps,
                    converged=False,
                    cell_changes=changes,
                    reason="time budget",
                )
            ref_x, ref_y = list(x), list(y)
            base = theta[group[0]]

            def probe(value, group=group, ref_x=ref_x, ref_y=ref_y, angles=tuple(theta)):
                nonlocal lp_solves
                if time.monotonic() > deadline:
                    raise _OutOfTimeError
                trial_theta = list(angles)
                for k in group:
                    trial_theta[k] = value
                got = evaluate_fixed_point(trial_theta, ref_x, ref_y, n)
                lp_solves += got.solves
                if not got.settled:
                    raise _FixedCellUnsettledError(got.reason)
                return got.side

            try:
                best_angle = _bracket_min(probe, base, span)
            except _OutOfTimeError:
                return audited_result(
                    side=side,
                    x=x,
                    y=y,
                    theta=theta,
                    lp_solves=lp_solves,
                    angle_steps=angle_steps,
                    converged=False,
                    cell_changes=changes,
                    reason="time budget",
                )
            except _FixedCellUnsettledError as exc:
                return audited_result(
                    side=side,
                    x=x,
                    y=y,
                    theta=theta,
                    lp_solves=lp_solves,
                    angle_steps=angle_steps,
                    converged=False,
                    cell_changes=changes,
                    reason=f"fixed cell unsettled during bracket: {exc}",
                )
            trial_theta = list(theta)
            for k in group:
                trial_theta[k] = best_angle
            got = evaluate_fixed_point(trial_theta, ref_x, ref_y, n)
            lp_solves += got.solves
            if not got.settled:
                return audited_result(
                    side=side,
                    x=x,
                    y=y,
                    theta=theta,
                    lp_solves=lp_solves,
                    angle_steps=angle_steps,
                    converged=False,
                    cell_changes=changes,
                    reason=f"fixed cell unsettled after bracket: {got.reason}",
                )
            if got.side < side - tol:
                side, x, y = got.side, got.x, got.y
                theta = trial_theta
                angle_steps += 1
                improved = True
        if improved:
            # The window is still paying for itself, so keep it. Narrowing it here --
            # unconditionally, every sweep -- is what stopped this quench arriving from
            # a cold start (D-030): `_bracket_min` may only move an angle within +-span,
            # and by sweep 12 the old schedule had span at 2.4e-05 while a random start
            # needs O(0.1) rad. It descended until the window ran out and then crawled,
            # improving by ~1e-09 a sweep, forever above `tol` and so never converged.
            groups = angle_classes(theta, class_tol)
            continue

        if span > span_min:
            # Nothing improved at this window. That is not convergence, it is evidence
            # the window is too WIDE: golden section needs a unimodal bracket, and a
            # narrower one is likelier to be. Narrow and re-sweep.
            #
            # An order of magnitude a step, not a halving. Measured 2026-08-23 on the
            # polish case (a 1e-3 perturbation of Trump's packing) and the cold case
            # (six uniform n = 5 starts), all reaching the same answer:
            #
            #   shrink   polish gap   polish wall   cold converged
            #     0.5     -2.22e-11        11.3 s        5 of 6
            #     0.1     -2.22e-11         6.6 s        6 of 6
            #    0.02     -2.22e-11         4.9 s        6 of 6
            #
            # Halving is worse on every axis, and worse at CONVERGING: from 0.05 it
            # needs 26 narrowing sweeps to reach the floor, which can exhaust the sweep
            # or wall budget before the free-sweep certificate is ever reached.
            span = max(span * span_shrink, span_min)
            continue

        # Nothing improved at the narrowest window either. This is the real test.
        if not free_pass:
            return audited_result(
                side=side,
                x=x,
                y=y,
                theta=theta,
                lp_solves=lp_solves,
                angle_steps=angle_steps,
                converged=True,
                cell_changes=changes,
                reason=f"bracket converged, {len(groups)} classes",
            )
        # The class constraint is a search device, not a property of the answer.
        # Merging angles searches one coordinate where the packing has one degree of
        # freedom -- but it also FORCES angles equal that the true optimum may want
        # apart, so a class-converged point need not be a local optimum at all. Its
        # value would then depend on class_tol, and since the cartography plan
        # defines a basin as where the quench lands, basin identity would inherit a
        # tuning parameter (defect D-020).
        #
        # One free sweep, every angle on its own, settles it: if nothing improves
        # the class-converged point IS a coordinate-wise local optimum and the
        # tolerance did not decide the answer. If something improves, the search
        # continues from there with the classes re-read.
        try:
            free_side, free_x, free_y, free_theta, used = _free_sweep(
                side,
                x,
                y,
                theta,
                n,
                deadline=deadline,
                solve_fixed=evaluate_fixed_point,
            )
        except _OutOfTimeError:
            stop_reason = "time budget during free sweep"
            break
        except _FixedCellUnsettledError as exc:
            stop_reason = f"fixed cell unsettled during free sweep: {exc}"
            break
        lp_solves += used
        if free_side < side - tol:
            # The free sweep found what the class search could not at any window, so
            # the point moved: reopen the window and let the class search work from
            # here. `side` strictly decreases on every pass through this branch, so
            # the restart cannot cycle.
            side, x, y, theta = free_side, free_x, free_y, free_theta
            angle_steps += 1
            groups = angle_classes(theta, class_tol)
            span = span0
            continue
        return audited_result(
            side=side,
            x=x,
            y=y,
            theta=theta,
            lp_solves=lp_solves,
            angle_steps=angle_steps,
            converged=True,
            cell_changes=changes,
            reason=f"converged, {len(groups)} classes, free pass clean",
        )
    return audited_result(
        side=side,
        x=x,
        y=y,
        theta=theta,
        lp_solves=lp_solves,
        angle_steps=angle_steps,
        converged=False,
        cell_changes=changes,
        reason=stop_reason,
    )
