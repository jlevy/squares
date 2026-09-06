"""Falsify the standalone fractional sweeps with independent exact geometry.

Run from ``packing/`` with ``uv run --frozen --all-extras --group dev python -m
devtools.check_fractional_sweep --cases 20000 --seed 89213``. The bounded seeded
corpus includes rational weights, coincident events, empty supports, axes and
rotations beyond the retained net's first octant.

The oracle constructs its own coverage events, uses strict separating-axis overlap
to decide which open cells meet the admissible center domain, and sums each cell's
atoms directly. It imports neither production clipping nor strip selection nor
mass-prefix helpers. It does share the reduction both verifiers rest on: the event
lines are every atom's coverage edges plus the center domain's extremes, and the
minimum over the closed domain is taken over the open cells that meet it. A flaw in
that reduction would be invisible to all three programs. Comparing reachable-cell
counts as well as minima is what gives the corpus its power, since most seeded
minima are zero while the cell set moves under almost any reachability error. The
witness center each ``verify_claim`` sweep returns is also checked: it must admit a
square and cover exactly the reported minimum. The two standalone verifiers are
called only for comparison. This finite falsification campaign does not verify a
retained certificate or prove that either implementation is correct on every input.
"""

from __future__ import annotations

import argparse
import json
import random
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from itertools import pairwise
from math import lcm

from cases.n11_fractional_certificate import minimal_verify, verify_claim

type Point = tuple[Fraction, Fraction]
type Atom = tuple[Fraction, Fraction, Fraction]
type Cell = tuple[Fraction, Fraction, Fraction, Fraction]


@dataclass(frozen=True)
class SweepCase:
    """One finite nonnegative measure and one rational square direction."""

    outer_side: Fraction
    square_side: Fraction
    tangent: Fraction
    atoms: tuple[Atom, ...]


@dataclass(frozen=True)
class OracleResult:
    """The exact minimum and count of reachable open cells, or a singleton placement."""

    minimum: Fraction | None
    cells: int


class OracleInvariantError(RuntimeError):
    """The oracle's own reduction failed; this is not a disagreement with a verifier."""


def frame(case: SweepCase) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """The exact cosine, sine, half-side and axis-aligned reach of one case."""
    side, shrink, tangent = case.outer_side, case.square_side, case.tangent
    if side <= 0 or shrink <= 0 or any(weight < 0 for _, _, weight in case.atoms):
        raise ValueError("positive sides and nonnegative atom weights are required")
    cosine = (1 - tangent * tangent) / (1 + tangent * tangent)
    sine = 2 * tangent / (1 + tangent * tangent)
    half = shrink / 2
    return cosine, sine, half, half * (abs(cosine) + abs(sine))


def covered_mass(case: SweepCase, centre: Point) -> Fraction:
    """The mass of the closed square at a center in the original frame, summed directly."""
    cosine, sine, half, _ = frame(case)
    x, y = centre
    return sum(
        (
            weight
            for atom_x, atom_y, weight in case.atoms
            if abs(cosine * (atom_x - x) + sine * (atom_y - y)) <= half
            and abs(cosine * (atom_y - y) - sine * (atom_x - x)) <= half
        ),
        Fraction(0),
    )


def open_cell_meets_domain(cell: Cell, rotation: Point, low: Fraction, high: Fraction) -> bool:
    """Decide positive-area overlap on all four edge normals, by separating axes.

    The cell is axis-aligned in the rotated frame; the domain is ``[low, high]^2``
    in the original frame. Strict projection overlap on both pairs of edge normals
    is equivalent to intersection of their interiors. Equality admits only boundary
    contact and must not introduce an unreachable open cell.
    """
    u0, u1, v0, v1 = cell
    cosine, sine = rotation
    domain = [
        (cosine * x + sine * y, -sine * x + cosine * y)
        for x in (low, high)
        for y in (low, high)
    ]
    if not (
        u0 < max(u for u, _ in domain)
        and u1 > min(u for u, _ in domain)
        and v0 < max(v for _, v in domain)
        and v1 > min(v for _, v in domain)
    ):
        return False
    corners = [
        (cosine * u - sine * v, sine * u + cosine * v) for u in (u0, u1) for v in (v0, v1)
    ]
    return (
        min(x for x, _ in corners) < high
        and max(x for x, _ in corners) > low
        and min(y for _, y in corners) < high
        and max(y for _, y in corners) > low
    )


def least_mass(case: SweepCase) -> OracleResult:
    """Enumerate reachable cells with separating axes and score each by a direct sum.

    Each atom's coverage is constant within an open event cell, so its midpoint
    gives that cell's mass even when the midpoint lies outside the center domain.
    The separate overlap test establishes that some point of the cell is admissible.
    Nonnegative weights and closed squares make event boundaries no lighter than
    adjacent cells. A singleton domain has no such cells and is scored directly.
    """
    side = case.outer_side
    cosine, sine, half, reach = frame(case)
    if 2 * reach > side:
        return OracleResult(None, 0)
    rotated = [
        (cosine * x + sine * y, -sine * x + cosine * y, weight) for x, y, weight in case.atoms
    ]

    def mass_at(u_center: Fraction, v_center: Fraction) -> Fraction:
        return sum(
            (
                weight
                for u, v, weight in rotated
                if abs(u - u_center) <= half and abs(v - v_center) <= half
            ),
            Fraction(0),
        )

    if 2 * reach == side:
        return OracleResult(mass_at((cosine + sine) * side / 2, (cosine - sine) * side / 2), 1)
    domain = [
        (cosine * x + sine * y, -sine * x + cosine * y)
        for x in (reach, side - reach)
        for y in (reach, side - reach)
    ]
    u_events = sorted(
        {min(u for u, _ in domain), max(u for u, _ in domain)}
        | {u + offset for u, _, _ in rotated for offset in (-half, half)}
    )
    v_events = sorted(
        {min(v for _, v in domain), max(v for _, v in domain)}
        | {v + offset for _, v, _ in rotated for offset in (-half, half)}
    )
    minimum, cells = None, 0
    for u0, u1 in pairwise(u_events):
        for v0, v1 in pairwise(v_events):
            if not open_cell_meets_domain(
                (u0, u1, v0, v1), (cosine, sine), reach, side - reach
            ):
                continue
            mass = mass_at((u0 + u1) / 2, (v0 + v1) / 2)
            minimum = mass if minimum is None else min(minimum, mass)
            cells += 1
    if minimum is None:
        raise OracleInvariantError(f"positive-area domain reached no cell: {case!r}")
    return OracleResult(minimum, cells)


def compare_case(case: SweepCase) -> tuple[OracleResult, bool]:
    """Compare minimum, cell count and witness; skip the pinned sweep's unsupported domains."""
    expected = least_mass(case)
    scale = lcm(*(weight.denominator for _, _, weight in case.atoms))
    minimum, centre, cells = verify_claim.least_mass(
        case.outer_side, case.square_side, case.tangent, case.atoms, scale
    )
    minimum = None if minimum is None else Fraction(minimum)
    if OracleResult(minimum, cells) != expected:
        raise AssertionError(
            f"verify_claim: expected {expected}, got {(minimum, cells)}; {case!r}"
        )
    if minimum is not None:
        # The verifier's witness is the one claim its own cross-check also guards;
        # deciding it here keeps the oracle independent of that self-check.
        if centre is None:
            raise AssertionError(f"verify_claim: no witness for {minimum}; {case!r}")
        witness: Point = (Fraction(centre[0]), Fraction(centre[1]))
        reach = frame(case)[3]
        if not all(reach <= coordinate <= case.outer_side - reach for coordinate in witness):
            raise AssertionError(
                f"verify_claim: witness {witness} admits no square in the container; {case!r}"
            )
        direct = covered_mass(case, witness)
        if direct != minimum:
            raise AssertionError(
                f"verify_claim: witness {witness} covers {direct}, not the reported "
                f"{minimum}; {case!r}"
            )
    # minimal_verify refuses nonpositive cosines and empty/singleton center domains.
    tangent = case.tangent
    extent = case.square_side * (1 - tangent * tangent + 2 * tangent) / (1 + tangent * tangent)
    minimal_checked = 0 <= tangent < 1 and extent < case.outer_side
    if minimal_checked:
        weights = [int(weight * scale) for _, _, weight in case.atoms]
        scaled_minimum, cells = minimal_verify.sweep(
            case.atoms, weights, case.square_side / 2, case.outer_side, tangent
        )
        minimum = Fraction(scaled_minimum, scale)
        if OracleResult(minimum, cells) != expected:
            raise AssertionError(
                f"minimal_verify: expected {expected}, got {(minimum, cells)}; {case!r}"
            )
    return expected, minimal_checked


def random_case(generator: random.Random) -> SweepCase:
    """Keep the rational grid and random-call order fixed so a seed reproduces a corpus."""
    side = Fraction(generator.randrange(1, 33), 8)
    shrink = Fraction(generator.randrange(1, 33), 16)
    tangent = generator.choice(
        [
            Fraction(0),
            Fraction(1, 3),
            Fraction(1, 2),
            Fraction(1),
            Fraction(3, 2),
            Fraction(generator.randrange(1, 400), generator.randrange(1, 400)),
        ]
    )
    sites = {
        (
            side * Fraction(generator.randrange(17), 16),
            side * Fraction(generator.randrange(17), 16),
        )
        for _ in range(generator.randrange(10))
    }
    atoms = tuple(
        (x, y, Fraction(generator.randrange(20), generator.randrange(1, 13)))
        for x, y in sorted(sites)
    )
    return SweepCase(side, shrink, tangent, atoms)


def check_cases(*, cases: int, seed: int) -> dict[str, int]:
    """Run a finite campaign; a disagreement or a verifier refusal names the seed, index
    and full case, and the oracle's own invariant failures are kept apart from both."""
    if cases < 1:
        raise ValueError("cases must be positive")
    generator = random.Random(seed)
    report = {
        "cases": cases,
        "seed": seed,
        "verify_claim": 0,
        "minimal_verify": 0,
        "vacuous": 0,
        "singleton": 0,
    }
    for index in range(cases):
        case = random_case(generator)
        try:
            expected, minimal_checked = compare_case(case)
        except OracleInvariantError as error:
            raise OracleInvariantError(f"seed={seed}, case={index}: {error}") from error
        except (AssertionError, ArithmeticError, LookupError, TypeError, ValueError) as error:
            # A verifier that refuses rather than answers is still a discrepancy, and
            # the reproduction must survive it instead of dying in a traceback.
            label = "" if isinstance(error, AssertionError) else f"{type(error).__name__}: "
            raise AssertionError(f"seed={seed}, case={index}: {label}{error}") from error
        report["verify_claim"] += 1
        report["minimal_verify"] += minimal_checked
        report["vacuous"] += expected.minimum is None
        tangent = case.tangent
        extent = (
            case.square_side
            * (abs(1 - tangent * tangent) + abs(2 * tangent))
            / (1 + tangent * tangent)
        )
        report["singleton"] += extent == case.outer_side
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=int, default=200)
    parser.add_argument("--seed", type=int, default=89213)
    arguments = parser.parse_args(argv)
    if arguments.cases < 1:
        parser.error("cases must be positive")
    try:
        report = check_cases(cases=arguments.cases, seed=arguments.seed)
    except OracleInvariantError as error:
        print(json.dumps({"result": "oracle invariant failure", "detail": str(error)}))
        return 2
    except AssertionError as error:
        print(json.dumps({"result": "disagreement", "detail": str(error)}))
        return 1
    print(json.dumps({"result": "agreement on every tested minimum and cell count", **report}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
