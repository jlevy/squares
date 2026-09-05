"""The integer sweep is the Fraction sweep, cell for cell.

`minimum_covered_mass` decides in ``int64`` on the weights' common scale and
falls back to ``Fraction`` arithmetic when that scale does not fit. The
``Fraction`` route is the one that decided every retained certificate through
2026-09-04 and is kept unchanged as the reference; these tests hold the two to
the same value *and the same witness cell*, direction by direction, and hold
the parallel direction loop to the serial one. Measured on 2026-09-04: one
direction of the 2260-atom n = 20 certificate took 39.35 s by Fraction and
0.86 s by integer; the whole verify took 5378 s and 38.7 s.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from cases.n11_fractional_certificate.replay import FIRST_RUNG_PATH as N11_FIRST_RUNG
from cases.n11_fractional_certificate.replay import load as n11_load
from cases.n17_fractional_certificate.replay import declared as n17_declared
from cases.n17_fractional_certificate.replay import load as n17_load
from sqpack.fractional import sweep
from sqpack.fractional.certificate import Certificate, sweep_all_directions, verify
from sqpack.fractional.model import Atom
from sqpack.fractional.sweep import (
    minimum_covered_mass,
    minimum_covered_mass_fraction,
    minimum_covered_mass_integer,
    reduce_to_cells,
    reduce_to_spans,
    weight_scale,
)


def _small_certificate() -> Certificate:
    """A D4-closed handful of atoms at odd weights, so the scale is not a round number."""

    side = Fraction(3)
    centre = side / 2
    seeds = (
        (Fraction(1, 2), Fraction(3, 4), Fraction(3, 7)),
        (Fraction(1), Fraction(5, 4), Fraction(2, 3)),
        (Fraction(3, 2), Fraction(3, 2), Fraction(5, 11)),
    )
    atoms: dict[tuple[Fraction, Fraction], Fraction] = {}
    for x, y, w in seeds:
        dx, dy = x - centre, y - centre
        for px, py in ((dx, dy), (-dy, dx), (-dx, -dy), (dy, -dx)):
            for qx, qy in ((px, py), (-px, py)):
                atoms[(centre + qx, centre + qy)] = w
    limit, steps = Fraction(207107, 500000), 12
    return Certificate(
        n=6,
        outer_side=side,
        square_side=Fraction(9977, 10000),
        atoms=tuple(Atom(f"{k:03d}", x, y, w) for k, ((x, y), w) in enumerate(atoms.items())),
        half_tangents=tuple(limit * k / steps for k in range(steps + 1)),
        symmetry="D4",
    )


def test_the_weight_scale_is_the_common_denominator() -> None:
    certificate = _small_certificate()
    scale = weight_scale(certificate.atoms)
    assert scale == 3 * 7 * 11
    assert all((atom.weight * scale).denominator == 1 for atom in certificate.atoms)


def test_integer_and_fraction_sweeps_agree_on_every_direction_of_a_small_net() -> None:
    """Value and witness, at every direction, on a certificate whose scale is 231."""

    certificate = _small_certificate()
    scale = weight_scale(certificate.atoms)
    for direction in certificate.directions:
        reference = minimum_covered_mass_fraction(
            certificate.atoms, direction, certificate.outer_side, certificate.square_side
        )
        fast = minimum_covered_mass_integer(
            certificate.atoms, direction, certificate.outer_side, certificate.square_side, scale
        )
        assert fast == reference, direction.label


@pytest.mark.parametrize("index", [0, 1, 37, 90, 137, 180])
def test_integer_and_fraction_sweeps_agree_on_a_retained_rung(index: int) -> None:
    """The 373-atom n = 11 rung, at six directions including both ends of the net.

    All 181 directions were run once on 2026-09-04 with no mismatch in 145 s;
    six are enough to keep in the fast tier, and the ends of the net are where
    the rotated frame is furthest from the axis-aligned one.
    """

    certificate = n11_load(N11_FIRST_RUNG)
    direction = certificate.directions[index]
    reference = minimum_covered_mass_fraction(
        certificate.atoms, direction, certificate.outer_side, certificate.square_side
    )
    fast = minimum_covered_mass(
        certificate.atoms, direction, certificate.outer_side, certificate.square_side
    )
    assert fast == reference


def test_the_span_reduction_is_the_cell_reduction_folded() -> None:
    """``reduce_to_cells`` is defined as the spans expanded; check it at one direction."""

    certificate = n11_load(N11_FIRST_RUNG)
    direction = certificate.directions[53]
    spans = reduce_to_spans(
        certificate.atoms, direction, certificate.outer_side, certificate.square_side
    )
    cells = reduce_to_cells(
        certificate.atoms, direction, certificate.outer_side, certificate.square_side
    )
    assert cells.u_events == spans.u_events and cells.v_events == spans.v_events
    expanded = [(i, j) for i, j0, j1 in spans.spans for j in range(j0, j1 + 1)]
    assert list(cells.cells) == expanded
    assert all(j0 <= j1 for _, j0, j1 in spans.spans)


def test_a_scale_too_large_for_int64_falls_back_to_fractions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Past the limit the integer route declines and the Fraction route decides.

    The limit is patched down rather than a certificate built up to it: a
    certificate whose scaled mass exceeds 2**60 would not fit in the fast tier.
    """

    certificate = _small_certificate()
    direction = certificate.directions[5]
    args = (certificate.atoms, direction, certificate.outer_side, certificate.square_side)
    expected = minimum_covered_mass_fraction(*args)
    monkeypatch.setattr(sweep, "_INTEGER_MASS_LIMIT", 1)
    calls: list[str] = []
    original = sweep.minimum_covered_mass_integer

    def spy(*a: object, **k: object) -> object:
        calls.append("integer")
        return original(*a, **k)  # type: ignore[arg-type]

    monkeypatch.setattr(sweep, "minimum_covered_mass_integer", spy)
    assert minimum_covered_mass(*args) == expected
    assert calls == [], "the integer route ran past its own limit"


def test_the_parallel_direction_loop_matches_the_serial_one() -> None:
    """Same minima, same order, same first-attaining label, whatever the schedule."""

    certificate = n11_load(N11_FIRST_RUNG)
    serial = sweep_all_directions(certificate, workers=1)
    parallel = sweep_all_directions(certificate, workers=3)
    assert parallel == serial
    assert [label for _, label in serial] == [d.label for d in certificate.directions]


def test_the_n17_certificate_verifies_in_the_fast_tier_now() -> None:
    """1473 s by Fraction on 2026-09-04; 21.8 s here on a loaded four-core box.

    The exhaustive tests that decide every retained certificate still exist and
    still run in the full tier. This one is the fast tier's own proof that the
    decision the record cites is the decision the code makes today.
    """

    certificate = n17_load()
    verdict = verify(certificate)
    assert verdict.accepted, verdict.failures
    assert n17_declared()["least_cell_mass"] == str(verdict.minimum_cell_mass)
