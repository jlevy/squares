#!/usr/bin/env python3
"""Decide a certificate file by both routes, and refuse it unless both accept.

This is the retention gate. A rung joins the record only when the bytes on disk
-- not an object in memory, not a lane's report -- are accepted by the exact
event-cell sweep and by the interval branch and bound, which share no modelling
assumption and fail differently. Reading the file back is half the point: a
generator that rewrites its own output between verification and retention has
happened here, turning 1032 atoms into 1121 under a path someone was about to
read.

The two routes are also asked to agree on the number, not merely on the verdict.
In minimisation mode the interval run encloses the least covered mass, and that
enclosure must have width zero and equal the sweep's value exactly; a verdict
that agreed while the values differed would mean one of them is deciding a
different object.

Usage:
    uv run --frozen python -m devtools.decide_certificate <path>...
    uv run --frozen python -m devtools.decide_certificate --quick <path>...

``--quick`` runs only the interval route, which is minutes faster on a large
certificate and is enough to reject a candidate. It is never enough to retain
one, and the tool says so in its own output rather than leaving the reader to
remember.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

from sqpack.fractional.certificate import (
    Certificate,
    ceiling_side,
    least_size_certified,
    verify,
)
from sqpack.fractional.interval import verify_by_intervals
from sqpack.fractional.model import Atom


def load(path: Path) -> tuple[Certificate, dict]:
    """Rebuild a certificate from a record's own bytes, trusting none of its summary."""

    record = json.loads(path.read_text())
    limit = Fraction(record["angle_limit"])
    steps = int(record["direction_steps"])
    certificate = Certificate(
        n=int(record["n"]),
        outer_side=Fraction(record["outer_side"]),
        square_side=Fraction(record["square_side"]),
        atoms=tuple(
            Atom(f"{index:04d}", Fraction(x), Fraction(y), Fraction(weight))
            for index, (x, y, weight) in enumerate(record["atoms"])
        ),
        half_tangents=tuple(limit * k / steps for k in range(steps + 1)),
        symmetry=record.get("symmetry", "D4"),
    )
    return certificate, record


def decide(path: Path, *, quick: bool) -> bool:
    certificate, record = load(path)
    mass = certificate.total_mass
    side = certificate.outer_side
    print(
        f"{path.name}: n = {certificate.n}, L = {side} = {float(side):.6f}, "
        f"{len(certificate.atoms)} atoms, mass {mass} = {float(mass):.6f}"
    )

    problems: list[str] = []
    declared_mass = record.get("total_mass")
    if declared_mass is not None and Fraction(declared_mass) != mass:
        problems.append(f"declared total_mass {declared_mass} != recomputed {mass}")
    ceiling = ceiling_side(certificate.n, certificate.square_side)
    if side > ceiling:
        problems.append(f"side {side} is above the ceiling {ceiling} = ceil(sqrt(n)) * B")
    reach = least_size_certified(mass)
    print(f"  ceiling {float(ceiling):.6f}, certifies every n >= {reach}")
    if reach > certificate.n:
        problems.append(f"mass {mass} does not fall below the declared n = {certificate.n}")

    start = time.time()
    exact = None
    if not quick:
        exact = verify(certificate)
        print(
            f"  exact    accepted={exact.accepted} least={exact.minimum_cell_mass} "
            f"({time.time() - start:.0f}s)"
        )
        if not exact.accepted:
            problems.append(f"the exact sweep refused it: {exact.failures}")

    start = time.time()
    interval = verify_by_intervals(certificate, enclose=True)
    boxes = sum(outcome.boxes for outcome in interval.directions)
    stalled = sum(outcome.stalled for outcome in interval.directions)
    enclosure = interval.enclosure
    print(
        f"  interval accepted={interval.accepted} enclosure={enclosure} "
        f"boxes={boxes} stalled={stalled} ({time.time() - start:.0f}s)"
    )
    if not interval.accepted:
        problems.append(f"the interval route refused it: {interval.failures}")
    if stalled:
        problems.append(f"{stalled} boxes stalled; the interval route decided nothing there")

    if exact is not None:
        if enclosure is None:
            problems.append("the interval route returned no enclosure to compare")
        elif enclosure[0] != enclosure[1]:
            problems.append(f"the enclosure has width: {enclosure}")
        elif enclosure[0] != exact.minimum_cell_mass:
            problems.append(
                f"the two routes disagree on the least covered mass: "
                f"{exact.minimum_cell_mass} against {enclosure[0]}"
            )
        declared_least = record.get("least_cell_mass")
        if declared_least is not None and Fraction(declared_least) != exact.minimum_cell_mass:
            problems.append(
                f"declared least_cell_mass {declared_least} != {exact.minimum_cell_mass}"
            )

    if problems:
        for problem in problems:
            print(f"  REFUSED: {problem}")
        return False
    if quick:
        print("  the interval route accepts. NOT ENOUGH TO RETAIN: run without --quick.")
        return True
    print(f"  RETAINABLE: both routes accept and agree at {exact.minimum_cell_mass}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument(
        "--quick", action="store_true", help="interval route only; cannot retain"
    )
    args = parser.parse_args()
    ok = True
    for path in args.paths:
        ok = decide(path, quick=args.quick) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
