"""Controls for the weighted fractional unavoidable-set instrument.

The positive control is the published one: Massaccesi's retained n = 17
certificate must be accepted, and the side it bounds must be the 4.5058 the
source reports. That number is the whole point of the control -- an earlier
reading of the theorem divided by the shrunken side and would have claimed
4.51799, overstating a published result.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from cases.n17_weighted_certificate.fixture import load_retained_fixture
from sqpack.fractional.certificate import Certificate, verify
from sqpack.fractional.model import Atom, Direction, rotation_from_half_tangent

MASSACCESI_LIMIT = Fraction(207107, 500000)


def retained_certificate(steps: int | None = None) -> Certificate:
    """The retained n = 17 data, re-encoded into the first-party types."""
    fixture = load_retained_fixture()
    scale = Fraction(fixture.weight_scale)
    atoms = tuple(
        Atom(atom.label, atom.x, atom.y, atom.weight / scale) for atom in fixture.atoms
    )
    count = fixture.direction_steps if steps is None else steps
    tangents = tuple(fixture.angle_limit * k / count for k in range(count + 1))
    return Certificate(
        n=17,
        outer_side=fixture.outer_side,
        square_side=fixture.square_side,
        atoms=atoms,
        half_tangents=tangents,
    )


def test_the_retained_certificate_bounds_the_side_its_source_reports() -> None:
    certificate = retained_certificate()
    assert certificate.bounded_side == Fraction(22529, 5000)
    assert float(certificate.bounded_side) == pytest.approx(4.5058)
    assert certificate.total_mass == Fraction(203, 12)
    assert certificate.total_mass < 17


def test_a_coarse_net_still_accepts_the_retained_atoms() -> None:
    """C4 on a sub-net of the published one: the atoms cover it too."""
    verdict = verify(retained_certificate(steps=6))
    assert verdict.minimum_cell_mass is not None
    assert verdict.minimum_cell_mass >= 1


@pytest.mark.exhaustive_exact
def test_the_full_retained_certificate_is_accepted() -> None:
    verdict = verify(retained_certificate())
    assert verdict.accepted, verdict.failures
    assert verdict.minimum_cell_mass == 1


def test_mass_reaching_n_is_refused() -> None:
    """C1 is strict: a total that only reaches n proves nothing."""
    base = retained_certificate(steps=6)
    inflated = Fraction(17, len(base.atoms))
    heavy = Certificate(
        n=17,
        outer_side=base.outer_side,
        square_side=base.square_side,
        atoms=tuple(Atom(a.label, a.x, a.y, inflated) for a in base.atoms),
        half_tangents=base.half_tangents,
    )
    assert heavy.total_mass == 17
    assert "C1 total mass below n" in verify(heavy).failures


def test_a_net_short_of_an_eighth_turn_is_refused() -> None:
    """C2: the D4 reduction needs the arc to reach pi/4, and 0.41 does not."""
    base = retained_certificate(steps=6)
    short = Certificate(
        n=17,
        outer_side=base.outer_side,
        square_side=base.square_side,
        atoms=base.atoms,
        half_tangents=tuple(Fraction(41, 100) * k / 6 for k in range(7)),
    )
    assert "C2 net reaches pi/4" in verify(short).failures


def test_a_net_too_coarse_for_containment_is_refused() -> None:
    """C3: with few directions the angular gap outgrows the shrink."""
    base = retained_certificate(steps=2)
    assert "C3 containment B(1 + D) < 1" in verify(base).failures


def test_a_lightened_atom_breaks_the_covering_condition() -> None:
    """C4 is tight on the retained certificate, so any loss is visible."""
    base = retained_certificate(steps=6)
    lightened = (
        Atom(base.atoms[0].label, base.atoms[0].x, base.atoms[0].y, Fraction(0)),
        *base.atoms[1:],
    )
    thin = Certificate(
        n=17,
        outer_side=base.outer_side,
        square_side=base.square_side,
        atoms=lightened,
        half_tangents=base.half_tangents,
    )
    verdict = verify(thin)
    assert verdict.minimum_cell_mass is not None
    assert verdict.minimum_cell_mass < 1
    assert "C4 every reachable cell carries mass 1" in verdict.failures


def test_the_half_angle_parametrisation_is_exactly_unit_length() -> None:
    for k in range(13):
        direction = rotation_from_half_tangent(str(k), MASSACCESI_LIMIT * k / 12)
        assert direction.ux**2 + direction.uy**2 == 1


def test_a_direction_off_the_unit_circle_is_refused() -> None:
    with pytest.raises(ValueError, match="unit length"):
        Direction("bad", Fraction(1), Fraction(1), Fraction(-1), Fraction(1))


def test_the_largest_half_gap_tangent_is_exact_on_a_uniform_net() -> None:
    """A uniform half-tangent net has its widest angular gap at zero."""
    certificate = retained_certificate(steps=180)
    assert certificate.largest_half_gap_tangent == MASSACCESI_LIMIT / 180
