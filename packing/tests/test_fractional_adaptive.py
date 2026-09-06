"""BC-231 controls only; neither project route can retain an adaptive candidate."""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
from itertools import pairwise, product
from pathlib import Path

import pytest

from devtools.decide_certificate import load
from sqpack.fractional.adaptive import (
    AdaptiveCertificate,
    derive_cells,
    owner_cell,
    specialize_scalar,
    sweep_minima,
    validate_cells,
)
from sqpack.fractional.adaptive_interval import check_cell_geometry, interval_minima
from sqpack.fractional.certificate import Certificate, d4_images, sweep_all_directions, verify
from sqpack.fractional.model import Atom


def _control() -> AdaptiveCertificate:
    centre = Fraction(3, 5)
    sites = (
        (centre, centre, Fraction(1)),
        (Fraction(3, 10), centre, Fraction(1, 10)),
        (Fraction(9, 10), centre, Fraction(1, 10)),
        (centre, Fraction(3, 10), Fraction(1, 10)),
        (centre, Fraction(9, 10), Fraction(1, 10)),
    )
    return AdaptiveCertificate(
        n=11,
        outer_side=Fraction(6, 5),
        atoms=tuple(Atom(str(index), *site) for index, site in enumerate(sites)),
        cells=derive_cells(
            (Fraction(0), Fraction(1, 4), Fraction(9, 20)),
            (Fraction(7, 10), Fraction(3, 4), Fraction(4, 5)),
        ),
    )


def test_nonuniform_control_keeps_its_three_core_sides() -> None:
    control = _control()
    expected = (Fraction(6, 5), Fraction(13, 10), Fraction(7, 5))
    exact = sweep_minima(control)
    assert tuple(result.minimum for result in exact) == expected
    enclosed = interval_minima(control)
    assert tuple(result.label for result in enclosed.directions) == ("0", "1", "2", "1'", "2'")
    for outcome in enclosed.directions:
        index = int(outcome.label.removesuffix("'"))
        assert outcome.status == "certified"
        assert outcome.lower is not None
        assert outcome.upper is not None
        assert Fraction(outcome.lower, enclosed.scale) == expected[index]
        assert Fraction(outcome.upper, enclosed.scale) == expected[index]
        assert not outcome.stalled
        assert not outcome.budget_exhausted


def test_small_scalar_specialization_preserves_the_complete_coverage_decision() -> None:
    control = _control()
    scalar = Certificate(
        control.n,
        control.outer_side,
        Fraction(7, 10),
        control.atoms,
        tuple(cell.half_tangent for cell in control.cells),
    )
    original = verify(scalar, workers=1)
    assert original.accepted
    assert original.minimum_cell_mass == Fraction(6, 5)
    assert original.worst_direction == "0"
    adapted = specialize_scalar(scalar)
    minima = sweep_minima(adapted)
    assert tuple((row.minimum, str(row.index)) for row in minima) == sweep_all_directions(
        scalar, workers=1
    )
    enclosed = interval_minima(adapted)
    for outcome in enclosed.directions:
        index = int(outcome.label.removesuffix("'"))
        assert outcome.status == "certified"
        assert outcome.lower is not None
        assert outcome.upper is not None
        assert Fraction(outcome.lower, enclosed.scale) == minima[index].minimum
        assert Fraction(outcome.upper, enclosed.scale) == minima[index].minimum


def test_unsupported_center_domains_are_refused_instead_of_swept() -> None:
    for outer in (Fraction(7, 10), Fraction(1, 2)):
        control = AdaptiveCertificate(
            11,
            outer,
            (Atom("centre", outer / 2, outer / 2, Fraction(1)),),
            _control().cells,
        )
        with pytest.raises(ValueError, match="positive-area centre domain"):
            sweep_minima(control)
        with pytest.raises(ValueError, match="does not fit the container"):
            interval_minima(control)


def _direct_minimum(control: AdaptiveCertificate, index: int) -> Fraction:
    """Direct membership on every open cell, with independent separating-axis reachability.

    Neither production clipping nor its span selection or prefix sums enter this
    oracle. The midpoint scores a cell; the separating-axis test independently
    establishes that the cell contains an admissible center.
    """
    cell = control.cells[index]
    tangent = cell.half_tangent
    cosine = (1 - tangent * tangent) / (1 + tangent * tangent)
    sine = 2 * tangent / (1 + tangent * tangent)
    half = cell.square_side / 2
    low = half * (cosine + sine)
    high = control.outer_side - low
    if high <= low:
        raise ValueError("the direct control oracle needs a positive-area domain")
    domain = tuple(
        (cosine * x + sine * y, cosine * y - sine * x)
        for x, y in product((low, high), repeat=2)
    )
    rotated = tuple(
        (cosine * atom.x + sine * atom.y, cosine * atom.y - sine * atom.x, atom.weight)
        for atom in control.atoms
    )
    umin, umax = min(u for u, _ in domain), max(u for u, _ in domain)
    vmin, vmax = min(v for _, v in domain), max(v for _, v in domain)
    us = sorted({umin, umax} | {u + offset for u, _, _ in rotated for offset in (-half, half)})
    vs = sorted({vmin, vmax} | {v + offset for _, v, _ in rotated for offset in (-half, half)})
    minimum: Fraction | None = None
    for (u0, u1), (v0, v1) in product(pairwise(us), pairwise(vs)):
        if not (u0 < umax and u1 > umin and v0 < vmax and v1 > vmin):
            continue
        corners = tuple(
            (cosine * u - sine * v, sine * u + cosine * v)
            for u, v in product((u0, u1), (v0, v1))
        )
        if not (
            min(x for x, _ in corners) < high
            and max(x for x, _ in corners) > low
            and min(y for _, y in corners) < high
            and max(y for _, y in corners) > low
        ):
            continue
        u, v = (u0 + u1) / 2, (v0 + v1) / 2
        mass = sum(
            (
                weight
                for au, av, weight in rotated
                if abs(au - u) <= half and abs(av - v) <= half
            ),
            start=Fraction(0),
        )
        minimum = mass if minimum is None else min(minimum, mass)
    if minimum is None:
        raise AssertionError("the positive-area control domain reached no event cell")
    return minimum


def test_direct_membership_oracle_agrees_with_nonuniform_sweep_and_its_witnesses() -> None:
    control = _control()
    assert tuple(_direct_minimum(control, index) for index in range(3)) == (
        Fraction(6, 5),
        Fraction(13, 10),
        Fraction(7, 5),
    )
    for outcome in sweep_minima(control):
        cell = control.cells[outcome.index]
        tangent = cell.half_tangent
        cosine = (1 - tangent * tangent) / (1 + tangent * tangent)
        sine = 2 * tangent / (1 + tangent * tangent)
        u, v = outcome.centre
        x, y = cosine * u - sine * v, sine * u + cosine * v
        reach = cell.square_side * (cosine + sine) / 2
        assert reach <= x <= control.outer_side - reach
        assert reach <= y <= control.outer_side - reach
        direct = sum(
            (
                atom.weight
                for atom in control.atoms
                if abs(cosine * atom.x + sine * atom.y - u) <= cell.square_side / 2
                and abs(cosine * atom.y - sine * atom.x - v) <= cell.square_side / 2
            ),
            start=Fraction(0),
        )
        assert direct == outcome.minimum == _direct_minimum(control, outcome.index)


def test_seams_have_one_owner_and_both_derivations_refuse_changed_geometry() -> None:
    cells = _control().cells
    assert tuple(cell.max_mismatch_tangent for cell in cells) == (
        Fraction(1, 4),
        Fraction(1, 4),
        Fraction(16, 89),
    )
    assert tuple(
        owner_cell(cells, tangent)
        for tangent in (Fraction(0), Fraction(1, 4), Fraction(56, 71), Fraction(1))
    ) == (0, 0, 1, 2)
    mutations = (
        (cells[0], cells[2]),
        (replace(cells[0], upper_boundary_tangent=Fraction(1, 3)), *cells[1:]),
        (replace(cells[0], max_mismatch_tangent=Fraction(1, 3)), *cells[1:]),
        (replace(cells[0], square_side=Fraction(4, 5)), *cells[1:]),
    )
    for changed in mutations:
        for check in (validate_cells, check_cell_geometry):
            with pytest.raises(ValueError, match=r"indices|derived|strict containment"):
                check(changed)


def test_boundary_membership_is_the_union_of_all_incident_open_cells() -> None:
    control = _control()
    half = control.cells[0].square_side / 2

    def members(u: Fraction, v: Fraction) -> set[int]:
        return {
            index
            for index, atom in enumerate(control.atoms)
            if abs(atom.x - u) <= half and abs(atom.y - v) <= half
        }

    for u, v, offsets in (
        (Fraction(13, 20), Fraction(3, 5), ((-1, 0), (1, 0))),
        (Fraction(13, 20), Fraction(13, 20), ((-1, -1), (-1, 1), (1, -1), (1, 1))),
    ):
        boundary = members(u, v)
        adjacent = [members(u + Fraction(du, 100), v + Fraction(dv, 100)) for du, dv in offsets]
        assert boundary == set().union(*adjacent)
        boundary_mass = sum((control.atoms[index].weight for index in boundary), Fraction(0))
        assert boundary_mass == Fraction(7, 5)
        assert boundary_mass >= max(
            sum((control.atoms[index].weight for index in group), Fraction(0))
            for group in adjacent
        )


def test_orbit_mutations_and_signed_weights_are_refused_before_coverage() -> None:
    control = _control()
    with pytest.raises(ValueError, match="complete equal-weight D4"):
        replace(control, atoms=control.atoms[:-1])
    with pytest.raises(ValueError, match="complete equal-weight D4"):
        replace(
            control,
            atoms=(*control.atoms[:-1], replace(control.atoms[-1], weight=Fraction(1, 20))),
        )
    with pytest.raises(ValueError, match="nonnegative"):
        replace(
            control, atoms=(replace(control.atoms[0], weight=Fraction(-1)), *control.atoms[1:])
        )
    zero_sites = sorted(set(d4_images(Fraction(1, 5), Fraction(3, 10), control.outer_side)))
    zeros = tuple(
        Atom(f"z{index}", x, y, Fraction(0)) for index, (x, y) in enumerate(zero_sites)
    )
    with pytest.raises(ValueError, match="complete equal-weight D4"):
        replace(control, atoms=(*control.atoms, *zeros[:-1]))
    complete = replace(control, atoms=(*control.atoms, *zeros))
    assert complete.total_mass == control.total_mass
    assert tuple(result.minimum for result in sweep_minima(complete)) == tuple(
        result.minimum for result in sweep_minima(control)
    )


@pytest.mark.parametrize(
    ("relative_path", "total"),
    [
        ("n11_fractional_certificate/certificate.json", Fraction(434547, 40000)),
        ("n12_fractional_certificate/certificate.json", Fraction(149987, 12500)),
        (
            "n11_fractional_certificate/thirdparty/control-n17-massaccesi.json",
            Fraction(203, 12),
        ),
    ],
)
def test_retained_scalar_specialization_preserves_geometry_and_bytes(
    relative_path: str, total: Fraction
) -> None:
    path = Path(__file__).resolve().parents[1] / "cases" / relative_path
    frozen = path.read_bytes()
    scalar, _ = load(path)
    control = specialize_scalar(scalar)
    assert control.total_mass == scalar.total_mass == total
    assert control.atoms is scalar.atoms
    assert all(cell.square_side == scalar.square_side for cell in control.cells)
    assert (
        max(cell.max_mismatch_tangent for cell in control.cells)
        == scalar.largest_half_gap_tangent
    )
    check_cell_geometry(control.cells)
    assert path.read_bytes() == frozen
