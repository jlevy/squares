"""Independent small-instance geometry checks for the standalone threshold verifier."""

from __future__ import annotations

import importlib.util
import itertools
from collections.abc import Iterator, Sequence
from fractions import Fraction
from math import lcm
from pathlib import Path
from random import Random
from typing import NamedTuple

PACKING = Path(__file__).resolve().parents[1]
VERIFIER = PACKING / "cases" / "n11_threshold_certificate" / "verify_claim.py"

Point = tuple[Fraction, Fraction]
Plane = tuple[Fraction, Fraction, Fraction]
PointAtom = tuple[Fraction, Fraction, Fraction]
ThresholdAtom = tuple[tuple[Point, ...], int, Fraction]
OracleLeaf = tuple[Fraction, int]


class OracleSlab(NamedTuple):
    u_index: int
    low_index: int
    high_index: int
    minimum: Fraction
    argmin: int
    leaves: tuple[OracleLeaf, ...]


class Fixture(NamedTuple):
    name: str
    outer_side: Fraction
    core_side: Fraction
    tangent: Fraction
    point_atoms: tuple[PointAtom, ...]
    threshold_atoms: tuple[ThresholdAtom, ...]


def load_verifier():
    spec = importlib.util.spec_from_file_location("standalone_under_review", VERIFIER)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def half_plane_vertices(planes: Sequence[Plane]) -> set[Point]:
    """Enumerate vertices of a bounded intersection without the reviewed clip code."""
    found: set[Point] = set()
    for (a, b, r), (c, d, s) in itertools.combinations(planes, 2):
        determinant = a * d - b * c
        if not determinant:
            continue
        x = (r * d - b * s) / determinant
        y = (a * s - r * c) / determinant
        if all(e * x + f * y <= g for e, f, g in planes):
            found.add((x, y))
    return found


def point_is_held(
    point: Point,
    centre: Point,
    cosine: Fraction,
    sine: Fraction,
    core_side: Fraction,
) -> bool:
    dx, dy = point[0] - centre[0], point[1] - centre[1]
    return (
        abs(cosine * dx + sine * dy) <= core_side / 2
        and abs(-sine * dx + cosine * dy) <= core_side / 2
    )


def independent_slabs(fixture: Fixture) -> list[OracleSlab]:
    """Enumerate every reachable event cell in physical-coordinate half-planes."""
    outer_side = fixture.outer_side
    core_side = fixture.core_side
    tangent = fixture.tangent
    cosine = (1 - tangent * tangent) / (1 + tangent * tangent)
    sine = 2 * tangent / (1 + tangent * tangent)
    half_extent = core_side * (cosine + sine) / 2
    sites = {(x, y) for x, y, _ in fixture.point_atoms}
    sites.update(point for points, _, _ in fixture.threshold_atoms for point in points)
    corners = tuple(itertools.product((half_extent, outer_side - half_extent), repeat=2))
    domain_u = [cosine * x + sine * y for x, y in corners]
    domain_v = [-sine * x + cosine * y for x, y in corners]
    u_events = sorted(
        {cosine * x + sine * y + sign * core_side / 2 for x, y in sites for sign in (-1, 1)}
        | {min(domain_u), max(domain_u)}
    )
    v_events = sorted(
        {-sine * x + cosine * y + sign * core_side / 2 for x, y in sites for sign in (-1, 1)}
        | {min(domain_v), max(domain_v)}
    )
    domain_planes: list[Plane] = [
        (Fraction(1), Fraction(0), outer_side - half_extent),
        (Fraction(-1), Fraction(0), -half_extent),
        (Fraction(0), Fraction(1), outer_side - half_extent),
        (Fraction(0), Fraction(-1), -half_extent),
    ]
    slabs: list[OracleSlab] = []
    for u_index, (u0, u1) in enumerate(itertools.pairwise(u_events)):
        values: list[OracleLeaf] = []
        for v_index, (v0, v1) in enumerate(itertools.pairwise(v_events)):
            planes = [
                *domain_planes,
                (cosine, sine, u1),
                (-cosine, -sine, -u0),
                (-sine, cosine, v1),
                (sine, -cosine, -v0),
            ]
            vertices = half_plane_vertices(planes)
            if not vertices:
                continue
            centre = (
                sum((point[0] for point in vertices), start=Fraction()) / len(vertices),
                sum((point[1] for point in vertices), start=Fraction()) / len(vertices),
            )
            centre_u = cosine * centre[0] + sine * centre[1]
            centre_v = -sine * centre[0] + cosine * centre[1]
            if not (u0 < centre_u < u1 and v0 < centre_v < v1):
                continue
            charge = sum(
                (
                    weight
                    for x, y, weight in fixture.point_atoms
                    if point_is_held((x, y), centre, cosine, sine, core_side)
                ),
                start=Fraction(),
            )
            charge += sum(
                (
                    weight
                    for points, threshold, weight in fixture.threshold_atoms
                    if sum(
                        point_is_held(point, centre, cosine, sine, core_side)
                        for point in points
                    )
                    >= threshold
                ),
                start=Fraction(),
            )
            values.append((charge, v_index))
        if values:
            minimum, argmin = min(values)
            slabs.append(
                OracleSlab(
                    u_index,
                    values[0][1],
                    values[-1][1],
                    minimum,
                    argmin,
                    tuple(values),
                )
            )
    return slabs


def fixtures() -> Iterator[Fixture]:
    grid = tuple((Fraction(x), Fraction(y)) for x in range(3) for y in range(3))
    atoms = tuple((x, y, Fraction(1)) for x, y in grid)
    thresholds: tuple[ThresholdAtom, ...] = (
        (tuple(grid[index] for index in (0, 1, 3)), 2, Fraction(1, 3)),
        (tuple(grid[index] for index in (4, 5, 7)), 2, Fraction(2, 5)),
    )
    yield Fixture("axis-seams", Fraction(2), Fraction(1), Fraction(0), atoms, thresholds)
    yield Fixture("oblique-seams", Fraction(2), Fraction(1), Fraction(1, 3), atoms, thresholds)
    central = (
        (Fraction(3, 4), Fraction(1)),
        (Fraction(1), Fraction(1)),
        (Fraction(5, 4), Fraction(1)),
    )
    yield Fixture(
        "threshold-only",
        Fraction(2),
        Fraction(1),
        Fraction(1, 3),
        (),
        ((central, 2, Fraction(7, 5)),),
    )
    random = Random(20260910)
    lattice = tuple((Fraction(x, 4), Fraction(y, 4)) for x in range(9) for y in range(9))
    for trial, tangent in enumerate(
        (Fraction(0), Fraction(1, 4), Fraction(9, 20), Fraction(4, 5))
    ):
        sites = random.sample(lattice, 8)
        atoms = tuple((x, y, Fraction(random.randrange(0, 7), 5)) for x, y in sites[:6])
        thresholds = tuple(
            (tuple(random.sample(sites, 3)), 2, Fraction(random.randrange(0, 7), 5))
            for _ in range(3)
        )
        yield Fixture(
            f"mixed-{trial}",
            Fraction(2),
            Fraction(3, 4),
            tangent,
            atoms,
            thresholds,
        )


def tracked_least_charge(verifier, fixture: Fixture, scale: int):
    """Run the reviewed sweep while recording each range query and all queried leaves."""
    original_tree = verifier.RangeMinimum
    original_query = original_tree.query
    calls: list[tuple[int, int, int, int, tuple[tuple[int, int], ...]]] = []

    class TrackedRangeMinimum(original_tree):
        def query(
            self,
            low,
            high,
            node=1,
            left=0,
            right=None,
        ):
            result = original_query(self, low, high, node, left, right)
            if node == 1:
                leaves = tuple(
                    original_query(self, index, index) for index in range(low, high + 1)
                )
                calls.append((low, high, *result, leaves))
            return result

    verifier.RangeMinimum = TrackedRangeMinimum
    try:
        result = verifier.least_charge(
            fixture.outer_side,
            fixture.core_side,
            fixture.tangent,
            fixture.point_atoms,
            fixture.threshold_atoms,
            scale,
        )
    finally:
        verifier.RangeMinimum = original_tree
    return result, calls


def test_sweep_matches_an_independent_half_plane_oracle() -> None:
    """Compare all cells on seam, oblique, and deterministic mixed fixtures."""
    verifier = load_verifier()
    total_cells = 0
    for fixture in fixtures():
        scale = lcm(
            *(weight.denominator for _, _, weight in fixture.point_atoms),
            *(weight.denominator for _, _, weight in fixture.threshold_atoms),
        )
        (value, _witness, cell_count), calls = tracked_least_charge(verifier, fixture, scale)
        slabs = independent_slabs(fixture)
        projected = [
            (
                slab.low_index,
                slab.high_index,
                int(slab.minimum * scale),
                slab.argmin,
                tuple((int(score * scale), index) for score, index in slab.leaves),
            )
            for slab in slabs
        ]
        assert calls == projected, fixture.name
        assert value == min(slab.minimum for slab in slabs), fixture.name
        expected_cells = sum(len(slab.leaves) for slab in slabs)
        assert cell_count == expected_cells, fixture.name
        total_cells += cell_count
    assert total_cells == 272
