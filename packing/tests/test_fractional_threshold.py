"""Threshold atoms: the inclusion--exclusion grid is the direct count grid, cell for cell.

`threshold.charge_grid` adds a threshold atom to the sweep's difference array as signed
rectangle terms; `threshold.charge_grid_direct` thresholds one count grid per atom and
shares nothing with it past the event grid. These tests hold the two equal on random
instances, hold point atoms written as ``1-of-1`` threshold atoms to
`sweep.minimum_covered_mass` value and witness, and check the refusals and the symmetry
condition the theorem needs.
"""

from __future__ import annotations

import random
from fractions import Fraction
from math import comb

import pytest

from sqpack.fractional.certificate import Certificate, d4_images, verify
from sqpack.fractional.generate import net_half_tangents
from sqpack.fractional.model import Atom, rotation_from_half_tangent
from sqpack.fractional.sweep import minimum_covered_mass
from sqpack.fractional.threshold import (
    ThresholdAtom,
    ThresholdCertificate,
    charge_grid,
    charge_grid_direct,
    closed_form_threshold_conditions,
    exact_charge,
    expansion_terms,
    least_charged_cells,
    minimum_charge,
    rectangle_terms,
    sweep_slabs,
    threshold_weight_scale,
    verify_threshold,
)

SIDE = Fraction(3)
SQUARE = Fraction(9, 10)
NET = net_half_tangents(Fraction(207107, 500000), 6)
DIRECTIONS = tuple(rotation_from_half_tangent(str(k), t) for k, t in enumerate(NET))


def _point(rng: random.Random) -> tuple[Fraction, Fraction]:
    return Fraction(rng.randint(2, 28), 10), Fraction(rng.randint(2, 28), 10)


def _instance(seed: int) -> tuple[tuple[Atom, ...], tuple[ThresholdAtom, ...]]:
    rng = random.Random(seed)
    atoms = tuple(
        Atom(f"{k}", *_point(rng), Fraction(rng.randint(1, 9), 12)) for k in range(12)
    )
    shapes = ((3, 2), (4, 3), (5, 2), (5, 3), (5, 4), (2, 1), (4, 2), (6, 4))
    threshold_atoms = []
    for size, threshold in shapes:
        points: list[tuple[Fraction, Fraction]] = []
        while len(points) < size:
            candidate = _point(rng)
            if candidate not in points:
                points.append(candidate)
        threshold_atoms.append(
            ThresholdAtom(tuple(points), threshold, Fraction(rng.randint(1, 9), 8))
        )
    return atoms, tuple(threshold_atoms)


def test_the_expansion_identity_holds_for_every_trace_size() -> None:
    for size in range(1, 8):
        for threshold in range(1, size + 1):
            terms = expansion_terms(size, threshold)
            for m in range(size + 1):
                value = sum(coefficient * comb(m, j) for j, coefficient in terms)
                assert value == (1 if m >= threshold else 0)


@pytest.mark.parametrize("seed", [1, 2, 3])
def test_inclusion_exclusion_matches_the_direct_count_grid(seed: int) -> None:
    atoms, threshold_atoms = _instance(seed)
    scale = threshold_weight_scale(atoms, threshold_atoms)
    for direction in DIRECTIONS:
        fast = charge_grid(atoms, threshold_atoms, direction, SIDE, SQUARE, scale=scale)
        slow = charge_grid_direct(atoms, threshold_atoms, direction, SIDE, SQUARE, scale=scale)
        assert fast.reduction == slow.reduction
        assert (fast.grid == slow.grid).all()
        assert fast.grid.min() >= 0


def test_point_atoms_as_threshold_atoms_reproduce_the_sweep() -> None:
    atoms, _ = _instance(7)
    as_threshold = tuple(ThresholdAtom(((a.x, a.y),), 1, a.weight) for a in atoms)
    for direction in DIRECTIONS:
        expected = minimum_covered_mass(atoms, direction, SIDE, SQUARE)
        got = minimum_charge((), as_threshold, direction, SIDE, SQUARE)
        assert got == expected
        mixed = minimum_charge(atoms[:5], as_threshold[5:], direction, SIDE, SQUARE)
        assert mixed == expected


def test_the_minimum_cell_charge_agrees_with_an_exact_membership_count() -> None:
    atoms, threshold_atoms = _instance(11)
    direction = DIRECTIONS[3]
    minimum, (cu, cv) = minimum_charge(atoms, threshold_atoms, direction, SIDE, SQUARE)
    half = SQUARE / 2

    def contains(x: Fraction, y: Fraction) -> bool:
        u = direction.ux * x + direction.uy * y
        v = direction.vx * x + direction.vy * y
        return abs(u - cu) <= half and abs(v - cv) <= half

    assert exact_charge(atoms, threshold_atoms, contains) == minimum


def test_least_charged_cells_are_ordered_and_start_at_the_minimum() -> None:
    atoms, threshold_atoms = _instance(5)
    direction = DIRECTIONS[2]
    scale = threshold_weight_scale(atoms, threshold_atoms)
    grid = charge_grid(atoms, threshold_atoms, direction, SIDE, SQUARE, scale=scale)
    minimum, witness = minimum_charge(atoms, threshold_atoms, direction, SIDE, SQUARE)
    found = least_charged_cells(grid, direction, SIDE, SQUARE, keep=5, below=Fraction(100))
    assert len(found) == 5
    assert found[0] == (minimum, witness)
    assert [f[0] for f in found] == sorted(f[0] for f in found)
    assert least_charged_cells(grid, direction, SIDE, SQUARE, keep=5, below=minimum) == []


def test_budgets_and_refusals() -> None:
    p = tuple((Fraction(k), Fraction(1)) for k in range(5))
    assert ThresholdAtom(p[:3], 2, Fraction(3, 4)).budget == Fraction(3, 4)
    assert ThresholdAtom(p, 2, Fraction(3, 4)).budget == Fraction(3, 2)
    assert ThresholdAtom(p, 3, Fraction(3, 4)).budget == Fraction(3, 4)
    assert ThresholdAtom(p[:1], 1, Fraction(3, 4)).budget == Fraction(3, 4)
    for points, threshold, weight in (
        (p[:3], 2, Fraction(-1, 4)),
        (p[:3], 0, Fraction(1)),
        (p[:3], 4, Fraction(1)),
        ((p[0], p[0], p[1]), 2, Fraction(1)),
        ((), 1, Fraction(1)),
    ):
        try:
            ThresholdAtom(points, threshold, weight)
        except ValueError:
            continue
        raise AssertionError(f"{(points, threshold, weight)} was accepted")


def _symmetric_threshold_certificate(
    weight: Fraction, *, drop_image: bool = False
) -> ThresholdCertificate:
    centre = SIDE / 2
    seeds = (
        (Fraction(1, 2), Fraction(3, 4), Fraction(1, 3)),
        (Fraction(1), Fraction(5, 4), Fraction(1, 2)),
    )
    sites: dict[tuple[Fraction, Fraction], Fraction] = {}
    for x, y, w in seeds:
        for image in d4_images(x, y, SIDE):
            sites[image] = w
    atoms = tuple(Atom(f"{k}", x, y, w) for k, ((x, y), w) in enumerate(sorted(sites.items())))
    base = ThresholdAtom(
        ((Fraction(1, 2), Fraction(1, 2)), (Fraction(1), centre), (centre, Fraction(1))),
        2,
        weight,
    )
    orbit = list(base.orbit(SIDE))
    if drop_image:
        orbit = orbit[:-1]
    return ThresholdCertificate(
        n=12,
        outer_side=SIDE,
        square_side=SQUARE,
        atoms=atoms,
        threshold_atoms=tuple(orbit),
        half_tangents=NET,
    )


def test_symmetry_condition_detects_a_missing_image() -> None:
    whole = _symmetric_threshold_certificate(Fraction(1, 5))
    reports = closed_form_threshold_conditions(whole)
    assert [r.holds for r in reports] == [True, True, True, True, True]
    assert whole.total_budget == whole.point_mass + len(whole.threshold_atoms) * Fraction(1, 5)
    broken = _symmetric_threshold_certificate(Fraction(1, 5), drop_image=True)
    reports = closed_form_threshold_conditions(broken)
    assert not reports[1].holds
    assert "no matching image" in reports[1].detail


def test_zero_weight_threshold_atoms_leave_the_point_verdict_unchanged() -> None:
    certificate = _symmetric_threshold_certificate(Fraction(0))
    point = verify(certificate.point_certificate, workers=1)
    threshold = verify_threshold(certificate)
    assert threshold.minimum_cell_mass == point.minimum_cell_mass
    assert threshold.worst_direction == point.worst_direction
    assert threshold.accepted == point.accepted
    assert threshold.total_mass == point.total_mass


def test_duplicate_threshold_atoms_are_refused() -> None:
    whole = _symmetric_threshold_certificate(Fraction(1, 5))
    try:
        ThresholdCertificate(
            n=12,
            outer_side=SIDE,
            square_side=SQUARE,
            atoms=whole.atoms,
            threshold_atoms=(*whole.threshold_atoms, whole.threshold_atoms[0]),
            half_tangents=NET,
        )
    except ValueError:
        return
    raise AssertionError("a repeated (points, threshold) was accepted")


def test_the_record_round_trips() -> None:
    whole = _symmetric_threshold_certificate(Fraction(2, 7))
    record = whole.to_record()
    rebuilt = tuple(ThresholdAtom.from_record(r) for r in record["threshold_atoms"])
    assert rebuilt == whole.threshold_atoms
    assert Fraction(record["total_budget"]) == whole.total_budget
    assert isinstance(Certificate, type)


@pytest.mark.parametrize("seed", [4, 8])
def test_the_slab_sweep_reads_the_dense_grid_slab_for_slab(seed: int) -> None:
    atoms, threshold_atoms = _instance(seed)
    scale = threshold_weight_scale(atoms, threshold_atoms)
    for direction in DIRECTIONS:
        grid = charge_grid(atoms, threshold_atoms, direction, SIDE, SQUARE, scale=scale)
        terms = rectangle_terms(atoms, threshold_atoms, direction, SIDE, SQUARE, scale=scale)
        scores, cells = sweep_slabs(terms)
        for k, (i, j0, j1) in enumerate(grid.reduction.spans):
            column = grid.grid[i, j0 : j1 + 1]
            assert scores[k] == column.min()
            assert tuple(cells[k]) == (i, j0 + int(column.argmin()))
        dense = minimum_charge(atoms, threshold_atoms, direction, SIDE, SQUARE)
        slab = minimum_charge(
            atoms, threshold_atoms, direction, SIDE, SQUARE, dense_cell_limit=0
        )
        assert dense == slab
