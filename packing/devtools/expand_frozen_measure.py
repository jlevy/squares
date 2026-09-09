#!/usr/bin/env python3
"""The largest container the retained measure certifies when only its walls move.

Enlarging the container from `L0` to `L = L0 + 2 delta` while translating every atom
by `delta` keeps the measure centred and D4-symmetric; in atom-fixed coordinates the
atoms stay put and the walls move out by `delta`. At a net direction with inset
`a = B (cos + sin) / 2` the admissible-centre square is then `[a - delta, L0 - a +
delta]^2`, the `L0` square `Q = [a, L0 - a]^2` grown by `delta` in every direction.

Coverage is constant on the open event cells of a direction's grid, and the sweep
reaches a cell exactly when the open cell meets the closed domain. A cell outside the
`L0` domain therefore becomes reachable for every `delta` above

    delta_c = dist_inf(closed cell, Q),

the least `delta` at which the growing square touches the cell, and not at `delta_c`
itself: first contact lies on the cell's boundary. With `tau = M / n` the atoms certify
at `L` iff every reachable cell carries mass above `tau` (rescale the weights by the
least mass), so the largest certified side is attained:

    L* = L0 + 2 min { delta_c(cell) : mass(cell) <= tau },

and every larger side fails at the cell that attains the minimum.

`delta_c` is rational and decided exactly. First contact between the growing square
and the cell is a cell vertex on the square's boundary or a square corner on a cell
edge (a parallel-edge contact has such a point at its end), every such candidate has a
point in both sets, so `delta_c` is the least of finitely many rational candidates and
no clipping is needed. A float lower bound (support gaps in the eight directions of
the L1 unit ball, less a margin) orders the cells and prunes those that cannot improve
the best exact value; it is compared only as the exact rational the float represents.
The half-planes beyond a grid's extent carry mass zero and are handled as cells.

The pass also records every cell with mass below the retained least mass whose
`delta_c` does not exceed the answer: the exact step function `m(L)` on `[L0, L*]`.
With `--confirm` the library's own sweep then decides `L*` (must pass, at the step
function's last value) and `L* + 10^-8` (must fail, at the predicted direction).

Usage, from `packing/`:

    uv run --frozen python -m devtools.expand_frozen_measure --confirm \\
        --output cases/n11_fractional_certificate/expansion-381-100.json
"""

from __future__ import annotations

import argparse
import json
import time
from collections.abc import Sequence
from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path

import numpy as np
from strif import atomic_output_file

from devtools.decide_certificate import load_frozen_bytes, read_bounded
from sqpack.fractional.certificate import (
    Certificate,
    closed_form_conditions,
    sweep_direction_minimum,
)
from sqpack.fractional.model import Direction
from sqpack.fractional.sweep import scaled_mass_grid, weight_scale

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
CASE = PACKING / "cases" / "n11_fractional_certificate"

# Subtracted from every float lower bound. The bounds are affine in coordinates of size
# a few units, so their rounding error is far below this, and a bound that errs low only
# costs an exact evaluation, never a cell.
MARGIN = 1e-9

# Cells are examined in order of their lower bound until it exceeds the best exact
# `delta` found; this is the bound to start from before any bad cell has been seen.
INITIAL_CAP = Fraction(1, 50)

CONFIRM_STEP = Fraction(1, 10**8)


def cell_distance(
    u0: Fraction,
    u1: Fraction,
    v0: Fraction,
    v1: Fraction,
    *,
    direction: Direction,
    low: Fraction,
    high: Fraction,
) -> Fraction:
    """`dist_inf` from the closed cell `[u0, u1] x [v0, v1]` to `[low, high]^2`.

    The cell is axis-parallel in the direction's frame; the square is axis-parallel in
    the container's. Candidates: each cell vertex reaching the square's boundary, and
    each square corner, travelling diagonally as `delta` grows, reaching a cell edge.
    """
    cosine, sine = direction.ux, direction.uy
    corners = ((u0, v0), (u1, v0), (u1, v1), (u0, v1))
    points = [(cosine * u - sine * v, sine * u + cosine * v) for u, v in corners]
    best = min(max(low - x, x - high, low - y, y - high, Fraction(0)) for x, y in points)
    paths = ((low, low, -1, -1), (high, low, 1, -1), (high, high, 1, 1), (low, high, -1, 1))
    for index in range(4):
        px, py = points[index]
        qx, qy = points[(index + 1) % 4]
        ex, ey = qx - px, qy - py
        for cx, cy, dx, dy in paths:
            det = dx * ey - ex * dy
            if det == 0:
                continue
            rx, ry = cx - px, cy - py
            along = (dx * ry - rx * dy) / det
            delta = (ex * ry - ey * rx) / det
            if 0 <= along <= 1 and 0 <= delta < best:
                best = delta
    return best


def lower_bounds(
    u0: np.ndarray,
    u1: np.ndarray,
    v0: np.ndarray,
    v1: np.ndarray,
    *,
    direction: Direction,
    low: float,
    high: float,
) -> np.ndarray:
    """Float lower bounds on `cell_distance`: `<w, p - q> <= |w|_1 |p - q|_inf`."""
    c, s = float(direction.ux), float(direction.uy)
    min_x, max_x = c * u0 - s * v1, c * u1 - s * v0
    min_y, max_y = s * u0 + c * v0, s * u1 + c * v1
    min_sum, max_sum = (c + s) * u0 + (c - s) * v0, (c + s) * u1 + (c - s) * v1
    min_diff, max_diff = (c - s) * u0 - (c + s) * v1, (c - s) * u1 - (c + s) * v0
    gaps = np.stack(
        [
            min_x - high,
            low - max_x,
            min_y - high,
            low - max_y,
            (min_sum - 2 * high) / 2,
            (2 * low - max_sum) / 2,
            (min_diff - (high - low)) / 2,
            ((low - high) - max_diff) / 2,
        ]
    )
    return np.maximum(gaps.max(axis=0), 0.0) - MARGIN


def exterior_distances(
    u_events: tuple[Fraction, ...],
    v_events: tuple[Fraction, ...],
    direction: Direction,
    low: Fraction,
    high: Fraction,
) -> tuple[tuple[Fraction, str], ...]:
    """`delta` at which the grown square first touches each half-plane beyond the grid."""
    cosine, sine = direction.ux, direction.uy
    total = cosine + sine
    return (
        (u_events[-1] / total - high, "u above the grid"),
        (low - u_events[0] / total, "u below the grid"),
        ((v_events[-1] - (cosine * high - sine * low)) / total, "v above the grid"),
        (((cosine * low - sine * high) - v_events[0]) / total, "v below the grid"),
    )


@dataclass(frozen=True)
class Reached:
    """A cell of mass below the retained least mass, and the `delta` that reaches it."""

    delta: Fraction
    mass: Fraction
    direction: int
    cell: str


def reached_cells(certificate: Certificate, retained_least: Fraction) -> list[Reached]:
    """Every cell below the retained least mass with `delta_c` at most the first failure's."""
    atoms = certificate.atoms
    outer, side = certificate.outer_side, certificate.square_side
    threshold = certificate.total_mass / certificate.n
    scale = weight_scale(atoms)
    least_scaled = retained_least * scale
    if least_scaled.denominator != 1:
        raise ValueError("the retained least mass must sit on the weights' common scale")
    cap = INITIAL_CAP
    found: list[Reached] = []
    for k, direction in enumerate(certificate.directions):
        started = time.monotonic()
        low = side * (direction.ux + direction.uy) / 2
        high = outer - low
        filled = scaled_mass_grid(atoms, direction, outer, side, scale)
        grid, reduction = filled.grid, filled.reduction
        ii, jj = np.nonzero(grid[:-1, :-1] < int(least_scaled))
        u_float = np.array([float(u) for u in reduction.u_events])
        v_float = np.array([float(v) for v in reduction.v_events])
        bounds = lower_bounds(
            u_float[ii],
            u_float[ii + 1],
            v_float[jj],
            v_float[jj + 1],
            direction=direction,
            low=float(low),
            high=float(high),
        )
        evaluated = 0
        for index in np.argsort(bounds, kind="stable"):
            if Fraction(float(bounds[index])) > cap:
                break
            i, j = int(ii[index]), int(jj[index])
            delta = cell_distance(
                reduction.u_events[i],
                reduction.u_events[i + 1],
                reduction.v_events[j],
                reduction.v_events[j + 1],
                direction=direction,
                low=low,
                high=high,
            )
            evaluated += 1
            if delta > cap:
                continue
            mass = Fraction(int(grid[i, j]), scale)
            found.append(Reached(delta, mass, k, f"({i}, {j})"))
            if mass <= threshold:
                cap = min(cap, delta)
        for delta, where in exterior_distances(
            reduction.u_events, reduction.v_events, direction, low, high
        ):
            if delta <= cap:
                found.append(Reached(delta, Fraction(0), k, where))
                cap = min(cap, delta)
        print(
            f"direction {k:4d}: {len(ii)} cells below the retained least mass, {evaluated} "
            f"decided exactly, first failure so far at delta = {float(cap):.3e} "
            f"({time.monotonic() - started:.1f}s)",
            flush=True,
        )
    return [cell for cell in found if cell.delta <= cap]


def translated(certificate: Certificate, outer_side: Fraction) -> Certificate:
    """The measure centred in a container of side `outer_side`."""
    shift = (outer_side - certificate.outer_side) / 2
    return replace(
        certificate,
        outer_side=outer_side,
        atoms=tuple(replace(a, x=a.x + shift, y=a.y + shift) for a in certificate.atoms),
    )


def confirm(certificate: Certificate, outer_side: Fraction, first: int) -> dict[str, object]:
    """The library's own sweep at one side, the named direction first, all directions."""
    candidate = translated(certificate, outer_side)
    conditions = closed_form_conditions(candidate)
    if not all(condition.holds for condition in conditions):
        raise ValueError(f"translation broke a closed-form condition at {outer_side}")
    started = time.monotonic()
    order = [first, *(k for k in range(len(candidate.directions)) if k != first)]
    least: Fraction | None = None
    argmin: int | None = None
    for k in order:
        minimum, _witness = sweep_direction_minimum(candidate, candidate.directions[k])
        if least is None or minimum < least:
            least, argmin = minimum, k
    if least is None:
        raise ValueError("the net has no direction")
    return {
        "L": str(outer_side),
        "least": str(least),
        "least_float": float(least),
        "argmin": argmin,
        "passes": least > certificate.total_mass / certificate.n,
        "seconds": round(time.monotonic() - started, 1),
    }


def measure(
    certificate: Certificate, record: dict[str, object], *, confirm_by_sweep: bool
) -> dict[str, object]:
    retained_least = Fraction(str(record["least_cell_mass"]))
    threshold = certificate.total_mass / certificate.n
    started = time.monotonic()
    cells = sorted(reached_cells(certificate, retained_least), key=lambda c: (c.delta, c.mass))
    bad = [cell for cell in cells if cell.mass <= threshold]
    if not bad:
        raise ValueError("no failing cell below the initial cap; raise INITIAL_CAP")
    first = bad[0]
    outer = certificate.outer_side
    largest = outer + 2 * first.delta
    steps: list[dict[str, object]] = []
    running = retained_least
    for cell in cells:
        if cell.mass < running:
            running = cell.mass
            steps.append(
                {
                    "L_above": str(outer + 2 * cell.delta),
                    "L_above_float": float(outer + 2 * cell.delta),
                    "least_mass": str(cell.mass),
                    "least_mass_float": float(cell.mass),
                    "passes": cell.mass > threshold,
                    "direction": cell.direction,
                    "cell": cell.cell,
                }
            )
    gap = certificate.largest_half_gap_tangent
    composed_squared = largest**2 * (1 + gap * gap) / (certificate.square_side * (1 + gap)) ** 2
    result: dict[str, object] = {
        "L0": str(outer),
        "B": str(certificate.square_side),
        "threshold_M_over_n": str(threshold),
        "delta_star": str(first.delta),
        "L_star": str(largest),
        "L_star_float": float(largest),
        "first_failure": {
            "direction": first.direction,
            "cell": first.cell,
            "mass": str(first.mass),
            "mass_float": float(first.mass),
        },
        "step_function": steps,
        "composed_dilation_supremum_squared": str(composed_squared),
        "composed_dilation_supremum_float": float(composed_squared) ** 0.5,
        "seconds": round(time.monotonic() - started, 1),
    }
    if confirm_by_sweep:
        # At L* itself only the cells with delta_c strictly below delta* are reachable;
        # the failing cell (and any tie) is reached above L*. A tie at another direction
        # is legal, so above L* the sweep must fail at a mass no larger than the
        # predicted cell's, whichever direction reports it.
        reachable = [cell for cell in cells if cell.delta < first.delta]
        expected = min((cell.mass for cell in reachable), default=retained_least)
        at_star = confirm(certificate, largest, first.direction)
        above = confirm(certificate, largest + CONFIRM_STEP, first.direction)
        if not at_star["passes"] or Fraction(str(at_star["least"])) != expected:
            raise ValueError(f"the sweep at L* disagrees with the step function: {at_star}")
        if above["passes"] or Fraction(str(above["least"])) > first.mass:
            raise ValueError(f"the sweep above L* does not fail as predicted: {above}")
        result["confirmation"] = {
            "at_L_star": at_star,
            "above_L_star": above,
            "predicted_direction_reported": above["argmin"] == first.direction,
        }
    return result


def repository_relative(path: Path, role: str) -> str:
    """The path as the record states it; refused before any sweep if outside the repo."""
    try:
        return path.relative_to(REPO).as_posix()
    except ValueError:
        raise SystemExit(f"the {role} {path} is not inside the repository") from None


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=CASE / "certificate.json")
    parser.add_argument("--output", type=Path, help="where to write the result")
    parser.add_argument(
        "--confirm", action="store_true", help="decide L* by the library sweep too"
    )
    args = parser.parse_args(argv)

    certificate_path = args.certificate.resolve()
    certificate, record = load_frozen_bytes(read_bounded(certificate_path))
    side = certificate.outer_side
    output = (
        args.output.resolve()
        if args.output
        else CASE / f"expansion-{side.numerator}-{side.denominator}.json"
    )
    payload: dict[str, object] = {
        "certificate": repository_relative(certificate_path, "certificate"),
        "certificate_id": record["id"],
    }
    output_label = repository_relative(output, "output")
    payload.update(measure(certificate, record, confirm_by_sweep=args.confirm))
    with atomic_output_file(output) as temporary:
        temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        f"L* = {payload['L_star']} = {payload['L_star_float']:.9f}; first failure "
        f"{payload['first_failure']}; wrote {output_label}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
