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


class _OutOfTime(Exception):
    """Raised inside a line search when the quench's wall budget expires."""

import numpy as np
from scipy.optimize import linprog

# How much constraint violation a returned LP solution may carry. Two orders below the
# tightened solver tolerance, and far below any quantity the campaign reports.
LP_FEASIBLE_EPS = 1e-10


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


def _axes(theta: float) -> list[tuple[float, float]]:
    """The two edge normals of a square at this angle."""
    c, s = math.cos(theta), math.sin(theta)
    return [(c, s), (-s, c)]


def _half_extent(theta: float, ax: float, ay: float) -> float:
    """Half-width of a unit square at `theta`, projected on the axis `(ax, ay)`."""
    c, s = math.cos(theta), math.sin(theta)
    return 0.5 * (abs(ax * c + ay * s) + abs(-ax * s + ay * c))


def choose_cell(x, y, theta) -> list[tuple[int, int, float, float, float, float]]:
    """Pick, for each pair, the axis and sign that separates it best.

    This is what reads a cell off a configuration. The chosen axis is the one with the
    greatest separation (or least overlap), which is the standard separating-axis
    choice and the one that stays valid under small motion.
    """
    n = len(x)
    cell = []
    for i in range(n):
        for j in range(i + 1, n):
            dx, dy = x[i] - x[j], y[i] - y[j]
            best = None
            for ax, ay in _axes(theta[i]) + _axes(theta[j]):
                h = _half_extent(theta[i], ax, ay) + _half_extent(theta[j], ax, ay)
                d = dx * ax + dy * ay
                gap = abs(d) - h
                if best is None or gap > best[0]:
                    best = (gap, ax, ay, h, 1.0 if d >= 0 else -1.0)
            gap, ax, ay, h, sign = best
            cell.append((i, j, ax, ay, h, sign))
    return cell


def solve_cell(theta, cell, n: int):
    """Minimise the enclosing side over one cell. Returns (side, x, y) or None.

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
    res = linprog(
        obj,
        A_ub=np.array(rows),
        b_ub=np.array(rhs),
        bounds=[(0, None)] + [(None, None)] * (2 * n),
        method="highs",
        options={
            "primal_feasibility_tolerance": 1e-10,
            "dual_feasibility_tolerance": 1e-10,
        },
    )
    if not res.success:
        return None
    v = res.x
    x, y = list(v[1 : 1 + n]), list(v[1 + n :])

    # Trust nothing: check the solution against the constraints that were imposed.
    # A violation here is a solver artifact, and returning it would let a tolerance
    # masquerade as a discovery.
    for i, j, ax, ay, h, sign in cell:
        if sign * ((x[i] - x[j]) * ax + (y[i] - y[j]) * ay) - h < -LP_FEASIBLE_EPS:
            return None
    return float(v[0]), x, y


def solve_to_fixed_point(theta, x, y, n: int, max_iters: int = 12):
    """Solve, re-read the cell from the solution, and repeat until the cell settles.

    A single `solve_cell` optimises the cell suggested by the *incoming* centres, but
    its own solution may lie in a different cell -- so the value it returns is an upper
    bound on the true optimum at these angles, and it depends on where the caller
    happened to start. That path dependence makes `s(theta)` ill-defined, which in turn
    makes any angle search optimise a moving target: measured here, it is what made
    Powell and Nelder-Mead both do *worse* than plain descent.

    Iterating to a cell fixed point removes it. Returns (side, x, y, solves, changes).
    """
    solves = changes = 0
    cell = choose_cell(x, y, theta)
    best = solve_cell(theta, cell, n)
    solves += 1
    if best is None:
        return None
    for _ in range(max_iters):
        side, x, y = best
        nxt = choose_cell(x, y, theta)
        if nxt == cell:
            return side, x, y, solves, changes
        cell = nxt
        changes += 1
        trial = solve_cell(theta, cell, n)
        solves += 1
        if trial is None or trial[0] > side + 1e-15:
            # The re-read cell is worse or infeasible: keep the incumbent rather than
            # letting the loop oscillate between two cells forever.
            return side, x, y, solves, changes
        best = trial
    side, x, y = best
    return side, x, y, solves, changes


def quench(
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
        return QuenchResult(float("inf"), x, y, theta, lp_solves, 0, False, 0,
                            reason="initial cell infeasible")
    side, x, y, used, changed = solved
    lp_solves += used
    cell_changes += changed
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
            side, x, y, used, changed = solved
            lp_solves += used
            cell_changes += changed + 1
            cell = choose_cell(x, y, theta)

        if not polish_angles:
            break

        # Finite-difference gradient in angle space, one LP per angle.
        grad = []
        for k in range(n):
            probe = list(theta)
            probe[k] += fd_h
            trial = solve_to_fixed_point(probe, x, y, n)
            lp_solves += trial[3] if trial else 1
            grad.append((trial[0] - side) / fd_h if trial else 0.0)

        norm = math.sqrt(sum(g * g for g in grad))
        if norm < tol:
            return QuenchResult(side, x, y, theta, lp_solves, angle_steps, True,
                                cell_changes, reason="angle gradient vanished")

        # Reset the line search each round: a step that failed against one cell says
        # nothing about the next, and carrying the shrunken step forward is what turns
        # a slow descent into a stalled one.
        step = angle_step
        moved = False
        while step > 1e-13:
            probe = [t - step * g / norm for t, g in zip(theta, grad)]
            trial = solve_to_fixed_point(probe, x, y, n)
            lp_solves += trial[3] if trial else 1
            if trial and trial[0] < side - tol:
                side, x, y = trial[0], trial[1], trial[2]
                theta = probe
                cell = choose_cell(x, y, theta)
                angle_steps += 1
                moved = True
                break
            step *= 0.5
        if not moved:
            return QuenchResult(side, x, y, theta, lp_solves, angle_steps, True,
                                cell_changes, reason="no improving angle step")

    return QuenchResult(side, x, y, theta, lp_solves, angle_steps, False, cell_changes,
                        reason="round limit")


def contacts(x, y, theta, tol: float = 1e-9) -> list[tuple[int, int]]:
    """Pairs touching within `tol` -- the contact structure of the quenched packing."""
    n = len(x)
    out = []
    for i in range(n):
        for j in range(i + 1, n):
            dx, dy = x[i] - x[j], y[i] - y[j]
            gap = max(
                abs(dx * ax + dy * ay) - (_half_extent(theta[i], ax, ay) + _half_extent(theta[j], ax, ay))
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


def _free_sweep(side, x, y, theta, n, deadline, span: float = 1e-3):
    """One bracketing pass over every angle individually, no classes.

    Returns (side, x, y, theta, lp_solves). Used to certify that a class-converged
    point is a genuine coordinate-wise local optimum rather than an artifact of the
    merge tolerance.
    """
    import time as _time

    lp_solves = 0
    best = (side, list(x), list(y), list(theta))
    for k in range(n):
        if _time.monotonic() > deadline:
            break
        ref_x, ref_y = list(best[1]), list(best[2])
        base = best[3][k]

        def probe(value, k=k, ref_x=ref_x, ref_y=ref_y):
            nonlocal lp_solves
            trial_theta = list(best[3])
            trial_theta[k] = value
            got = solve_to_fixed_point(trial_theta, ref_x, ref_y, n)
            lp_solves += got[3] if got else 1
            return got[0] if got else 1e3

        try:
            angle = _bracket_min(probe, base, span)
        except _OutOfTime:
            break
        trial_theta = list(best[3])
        trial_theta[k] = angle
        got = solve_to_fixed_point(trial_theta, ref_x, ref_y, n)
        lp_solves += got[3] if got else 1
        if got and got[0] < best[0] - 1e-13:
            best = (got[0], got[1], got[2], trial_theta)
    return best[0], best[1], best[2], best[3], lp_solves


def quench_bracket(
    x, y, theta, *, max_sweeps: int = 12, span: float = 0.05, tol: float = 1e-12,
    class_tol: float = 1e-2, time_budget: float = 30.0, free_pass: bool = True,
) -> QuenchResult:
    """Quench whose angle half brackets rather than descends.

    The optimum of `s(theta)` is a corner -- distinct one-sided derivatives, measured in
    exp-006 -- so a smooth local model cannot converge to it, whatever its order. This
    variant does cyclic coordinate search over the angle CLASSES, each coordinate solved
    by golden section, which needs no derivative and lands on a kink exactly.
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
    # A per-call wall budget, because a quench that does not return is worse than one
    # that returns a worse answer: it takes the whole round with it. Measured on n = 5
    # seed 4, where a cell that solves in 5 ms sent the sweep past 145 s. Hitting the
    # budget is a RESULT and is reported as one, never silently.
    deadline = time.monotonic() + time_budget

    solved = solve_to_fixed_point(theta, x, y, n)
    if solved is None:
        return QuenchResult(float("inf"), x, y, theta, 1, 0, False, 0,
                            reason="initial cell infeasible")
    side, x, y, used, changes = solved
    lp_solves += used

    # `class_tol` is the one real knob, and it is doing more than grouping. A search
    # arrives with every angle slightly different, so a tight tolerance sees eleven
    # classes where the packing has two, and searches eleven non-smooth coordinates
    # instead of one. Merging at 1e-2 rad recovers the structure and, measured, moves
    # the result four orders: 1.5e-08 at eleven classes against 1.5e-11 at two, in an
    # eighth of the LP solves. The cost is that two genuinely distinct angles closer
    # than the tolerance are forced equal -- so a packing whose record needs that is
    # out of reach until this is swept rather than fixed.
    groups = angle_classes(theta, class_tol)
    for _ in range(max_sweeps):
        improved = False
        for group in groups:
            if time.monotonic() > deadline:
                return QuenchResult(side, x, y, theta, lp_solves, angle_steps, False,
                                    changes, reason="time budget")
            ref_x, ref_y = list(x), list(y)
            base = theta[group[0]]

            def probe(value, group=group, ref_x=ref_x, ref_y=ref_y):
                nonlocal lp_solves
                if time.monotonic() > deadline:
                    raise _OutOfTime
                trial_theta = list(theta)
                for k in group:
                    trial_theta[k] = value
                got = solve_to_fixed_point(trial_theta, ref_x, ref_y, n)
                lp_solves += got[3] if got else 1
                return got[0] if got else 1e3

            try:
                best_angle = _bracket_min(probe, base, span)
            except _OutOfTime:
                return QuenchResult(side, x, y, theta, lp_solves, angle_steps, False,
                                    changes, reason="time budget")
            trial_theta = list(theta)
            for k in group:
                trial_theta[k] = best_angle
            got = solve_to_fixed_point(trial_theta, ref_x, ref_y, n)
            lp_solves += got[3] if got else 1
            if got and got[0] < side - tol:
                side, x, y = got[0], got[1], got[2]
                theta = trial_theta
                angle_steps += 1
                improved = True
        if not improved:
            if not free_pass:
                return QuenchResult(side, x, y, theta, lp_solves, angle_steps, True,
                                    changes,
                                    reason=f"bracket converged, {len(groups)} classes")
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
            free_side, free_x, free_y, free_theta, used = _free_sweep(
                side, x, y, theta, n, deadline
            )
            lp_solves += used
            if free_side < side - tol:
                side, x, y, theta = free_side, free_x, free_y, free_theta
                angle_steps += 1
                groups = angle_classes(theta, class_tol)
                continue
            return QuenchResult(side, x, y, theta, lp_solves, angle_steps, True,
                                changes,
                                reason=f"converged, {len(groups)} classes, free pass clean")
        groups = angle_classes(theta, class_tol)
        span = max(span * 0.5, 1e-9)
    return QuenchResult(side, x, y, theta, lp_solves, angle_steps, False, changes,
                        reason="sweep limit")

