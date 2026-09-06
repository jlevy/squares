#!/usr/bin/env python3
"""Freeze the covering side of a cutting-plane state as a scalar-B candidate.

`devtools.run_fractional_cutting` runs one linear program and reads it two ways.
Its dual is a fractional packing, which the loop scales to unit depth and which
``--freeze`` writes as an exact family; its primal is a covering measure on the
current sites, and that is the object a lower bound needs. The state file keeps
the sites and the snapped rows but not the primal weights, so a row-converged
covering objective below ``n`` -- the one outcome of BC-232 that is a candidate
rather than a bracket -- had no path from the state to bytes that
`devtools.decide_certificate` can decide. Agenda-025 names the gap as a
"rationalize/freeze bridge"; this is it.

The bridge reloads the state, runs row generation on the held rows until no
placement is short of mass 1 (a state's rows are only ever complete for the
site set they were generated on), re-solves the covering program, rationalises
the weights exactly as `sqpack.fractional.colgen.generate_adaptive` does -- bump,
round up to a multiple of ``1/scale``, drop the empty orbits -- and writes the
candidate in the retained on-disk shape with ``least_cell_mass`` null.

It decides nothing. The row set is the loop's own finite sample of placements,
so the objective it reports is a restricted optimum, and only the exact sweep
says whether every placement is covered: `devtools.declare_least_cell_mass`
declares the number, and `devtools.decide_certificate` decides the frozen bytes
on both routes. What it refuses: a row loop that did not converge, a program the
solver rejects, a rationalised total at or above ``n`` (no candidate, whatever
the float objective said), and an output path that already exists.

Usage, from ``packing/``::

    uv run --frozen --all-extras --group dev python -m devtools.freeze_cutting_primal \
        --n 11 --state STATE.json --freeze CANDIDATE.json --json RECEIPT.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

from devtools.run_fractional_colgen import certificate_json
from sqpack.fractional.certificate import Certificate
from sqpack.fractional.colgen import (
    DEFAULT_SCALE,
    rationalise_sites,
    site_set_from_points,
    solve_lp,
    solve_rows,
)
from sqpack.fractional.cutting import (
    ExactRow,
    load_state,
    rebuild_rows,
    rows_from_exact,
    snap_centre,
)
from sqpack.fractional.generate import direction_net, net_half_tangents

ANGLE_LIMIT = Fraction(207107, 500000)
DIRECTION_STEPS = 180
ROW_DENOMINATOR = 10**6


class RefusalError(Exception):
    """The bridge found nothing it may freeze; the message says why."""


def bridge(
    state_path: Path,
    *,
    n: int,
    half_tangents: tuple[Fraction, ...],
    scale: int = DEFAULT_SCALE,
    rows_rounds: int = 2,
    rows_per_direction: int = 3,
    deadline_seconds: float | None = None,
) -> tuple[Certificate, dict[str, object]]:
    """The rationalised covering measure on the state's sites, with its receipt.

    Raises `RefusalError` rather than returning a candidate that is not one.
    """

    if n < 1:
        raise RefusalError("n must be positive")
    started = time.perf_counter()
    outer_side, points, exact_rows = load_state(state_path)
    square_side = Fraction(json.loads(state_path.read_text())["square_side"])
    sites = site_set_from_points(outer_side, set(points))
    rows = rows_from_exact(exact_rows, sites, half_tangents, square_side)
    held = len(rows)
    deadline = None if deadline_seconds is None else started + deadline_seconds
    solution = solve_rows(
        sites,
        square_side,
        half_tangents,
        rows,
        max_rounds=rows_rounds,
        rows_per_direction=rows_per_direction,
        deadline=deadline,
    )
    # New rows are held with float centres; snap them the way the loop does so
    # the program solved is the one the state would carry.
    directions = direction_net(half_tangents)
    snapped: list[ExactRow] = list(exact_rows)
    for index in range(held, len(rows)):
        direction = rows.directions[index]
        x, y = snap_centre(
            directions[direction], rows.centres[index], outer_side, square_side, ROW_DENOMINATOR
        )
        snapped.append((direction, x, y))
    rebuild_rows(rows, snapped, sites, half_tangents, square_side)
    if not solution.converged:
        raise RefusalError(
            f"row generation did not converge ({solution.stopped}); the held rows leave "
            "placements uncovered, so no covering measure on these sites is a candidate"
        )
    solved = solve_lp(sites, rows)
    if solved is None:
        raise RefusalError("the linear program refused the snapped rows")
    weights, _duals, objective = solved
    atoms = rationalise_sites(sites, weights, scale=scale)
    if not atoms:
        raise RefusalError("every site rounded to zero weight")
    certificate = Certificate(
        n=n,
        outer_side=outer_side,
        square_side=square_side,
        atoms=atoms,
        half_tangents=half_tangents,
    )
    receipt: dict[str, object] = {
        "state": str(state_path),
        "n": n,
        "outer_side": str(outer_side),
        "square_side": str(square_side),
        "direction_steps": len(half_tangents) - 1,
        "sites": sites.size,
        "orbits": len(sites.orbits),
        "rows_held": held,
        "rows_after": len(rows),
        "row_rounds": solution.rounds,
        "rows_stopped": solution.stopped,
        "least_covered": solution.least_covered,
        "objective": objective,
        "total_mass": str(certificate.total_mass),
        "total_mass_float": float(certificate.total_mass),
        "atoms": len(atoms),
        "scale": scale,
        "seconds": time.perf_counter() - started,
    }
    if certificate.total_mass >= n:
        raise RefusalError(
            f"the rationalised total {certificate.total_mass} = "
            f"{float(certificate.total_mass):.6f} is not below {n} "
            f"(LP objective {objective:.6f}); there is no candidate to freeze"
        )
    return certificate, receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="freeze a cutting-loop state's covering side as a scalar-B candidate"
    )
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--state", type=Path, required=True, help="a cutting-loop state file")
    parser.add_argument("--angle-limit", type=Fraction, default=ANGLE_LIMIT)
    parser.add_argument("--steps", type=int, default=DIRECTION_STEPS)
    parser.add_argument("--scale", type=int, default=DEFAULT_SCALE)
    parser.add_argument("--rows-rounds", type=int, default=2)
    parser.add_argument("--rows-per-direction", type=int, default=3)
    parser.add_argument("--deadline-seconds", type=float, default=None)
    parser.add_argument("--freeze", type=Path, required=True, help="write the candidate here")
    parser.add_argument("--json", type=Path, default=None, help="write the receipt here")
    args = parser.parse_args(argv)

    for path in (args.freeze, args.json):
        if path is not None and path.exists():
            print(f"REFUSED: {path} already exists; a candidate is never overwritten")
            return 1
    half_tangents = net_half_tangents(args.angle_limit, args.steps)
    try:
        certificate, receipt = bridge(
            args.state,
            n=args.n,
            half_tangents=half_tangents,
            scale=args.scale,
            rows_rounds=args.rows_rounds,
            rows_per_direction=args.rows_per_direction,
            deadline_seconds=args.deadline_seconds,
        )
    except RefusalError as refusal:
        print(f"REFUSED: {refusal}")
        return 1
    args.freeze.parent.mkdir(parents=True, exist_ok=True)
    args.freeze.write_text(certificate_json(certificate, None))
    receipt["frozen"] = str(args.freeze)
    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(receipt, indent=1, allow_nan=False) + "\n")
    print(
        f"frozen {args.freeze}: {receipt['atoms']} atoms, total {receipt['total_mass']} = "
        f"{receipt['total_mass_float']:.6f} against LP objective {receipt['objective']:.6f} "
        f"on {receipt['sites']} sites and {receipt['rows_after']} rows; least_cell_mass is "
        "undeclared until devtools.declare_least_cell_mass sweeps it"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
