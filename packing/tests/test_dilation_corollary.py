"""The dilation corollary: Condition 4's margin is a slightly larger bound, exactly.

Section 4 of the 2026-09-05 adversarial review: dilating the retained ``s(11) >= 381/100``
certificate's atom positions, ``L`` and ``B`` by ``a = 250001/250000`` leaves the weights,
the net, the symmetry, the total mass and the coverage unchanged and keeps
``a B (1 + D) < 1``, so the same accepted data prove ``s(11) >= 95250381/25000000 =
3.81001524``. That is an algebraic corollary of the retained certificate and not a third
certificate: nothing here is registered, and the retained bound stays ``381/100``. It does
not license dividing ``L`` by ``B`` -- the ceiling is ``1 / (B (1 + D))``, a supremum
Condition 4's strictness keeps out of reach. The margin could instead be spent in the next
search by setting ``B`` nearer its Condition 4 ceiling, so that the side the search runs
at is the side the certificate proves.

`devtools.dilation_corollary` recomputes every number from the file. These tests hold it
to the review's values, and check the invariance the corollary rests on where a sweep is
cheap enough to repeat.
"""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction

import pytest

from cases.n11_fractional_certificate.replay import CERTIFICATE_PATH
from cases.n11_fractional_certificate.replay import load as load_n11
from cases.n12_fractional_certificate.replay import FIRST_RUNG_PATH as N12_RUNG_19_5
from cases.n12_fractional_certificate.replay import load as load_n12
from devtools.dilation_corollary import corollary, dilate, dilation_ceiling, main
from sqpack.fractional.certificate import Certificate, closed_form_conditions, verify

#: The review's dilation, and the numbers it reports for the retained certificate.
REVIEW_FACTOR = Fraction(250001, 250000)
REVIEW_HALF_GAP_TANGENT = Fraction(207107, 90000000)
REVIEW_CONTAINMENT = Fraction(899996306539, 900000000000)
REVIEW_DILATED_CONTAINMENT = Fraction(224999976631056539, 225000000000000000)
REVIEW_BOUNDED_SIDE = Fraction(95250381, 25000000)


def small_certificate() -> Certificate:
    """The smallest retained atom set, on a net coarse enough to sweep in milliseconds.

    Six net steps put ``D`` near ``0.069``, which the retained ``B = 9973/10000`` cannot
    absorb, so ``B`` is lowered to ``9/10``: Conditions 1 to 4 then hold with a ceiling
    above 1, which is what the dilation tests need. Whether Condition 5 still holds at
    the smaller square is beside the point; the sweep's minimum is what is compared.
    """

    retained = load_n12(N12_RUNG_19_5)
    limit = retained.half_tangents[-1]
    return replace(
        retained,
        square_side=Fraction(9, 10),
        half_tangents=tuple(limit * k / 6 for k in range(7)),
    )


def test_the_retained_n11_certificate_carries_the_margin_the_review_reports() -> None:
    """``D`` and ``B(1 + D)`` from the retained net, the way the verifier derives them."""

    certificate = load_n11(CERTIFICATE_PATH)

    assert certificate.largest_half_gap_tangent == REVIEW_HALF_GAP_TANGENT
    assert certificate.square_side * (1 + REVIEW_HALF_GAP_TANGENT) == REVIEW_CONTAINMENT
    assert dilation_ceiling(certificate) == 1 / REVIEW_CONTAINMENT
    assert dilation_ceiling(certificate) == Fraction(900000000000, 899996306539)
    assert certificate.outer_side * dilation_ceiling(certificate) == Fraction(
        3429000000000, 899996306539
    )


def test_the_review_dilation_is_a_corollary_of_the_retained_certificate() -> None:
    """``a = 250001/250000`` keeps Condition 4 and moves nothing else."""

    certificate = load_n11(CERTIFICATE_PATH)

    result = corollary(certificate, REVIEW_FACTOR)
    dilated = dilate(certificate, REVIEW_FACTOR)

    assert result.dilated_containment == REVIEW_DILATED_CONTAINMENT
    assert result.dilated_containment < 1
    assert result.bounded_side == REVIEW_BOUNDED_SIDE
    assert result.bounded_side == Fraction("3.81001524")
    assert result.closed_form_failures == ()
    assert all(condition.holds for condition in closed_form_conditions(dilated))
    assert dilated.total_mass == certificate.total_mass == Fraction(434547, 40000)
    assert dilated.half_tangents == certificate.half_tangents
    assert dilated.symmetry == certificate.symmetry
    assert [atom.weight for atom in dilated.atoms] == [
        atom.weight for atom in certificate.atoms
    ]
    assert dilated.outer_side == certificate.outer_side * REVIEW_FACTOR
    assert dilated.square_side == certificate.square_side * REVIEW_FACTOR


def test_the_ceiling_is_below_dividing_l_by_b() -> None:
    """The corollary never reaches ``L / B``: ``1 / (B (1 + D)) < 1 / B`` because ``D > 0``."""

    certificate = load_n11(CERTIFICATE_PATH)

    assert dilation_ceiling(certificate) < 1 / certificate.square_side
    assert certificate.outer_side * dilation_ceiling(certificate) < (
        certificate.outer_side / certificate.square_side
    )


@pytest.mark.parametrize("factor", [REVIEW_FACTOR, Fraction(1, 2)])
def test_dilation_preserves_the_least_covered_mass(factor: Fraction) -> None:
    """Coverage is invariant: the inverse dilation is a bijection on placements.

    Checked by the exact sweep on a certificate small enough to sweep twice, in both
    directions of scaling. Only Condition 4's number moves.
    """

    certificate = small_certificate()
    dilated = dilate(certificate, factor)

    before, after = verify(certificate), verify(dilated)

    assert all(condition.holds for condition in closed_form_conditions(certificate))
    assert all(condition.holds for condition in closed_form_conditions(dilated))
    assert before.minimum_cell_mass is not None
    assert after.minimum_cell_mass == before.minimum_cell_mass
    assert after.worst_direction == before.worst_direction
    assert after.total_mass == before.total_mass
    assert dilated.square_side * (1 + dilated.largest_half_gap_tangent) == (
        factor * certificate.square_side * (1 + certificate.largest_half_gap_tangent)
    )


def test_a_factor_at_or_above_the_ceiling_or_not_positive_is_refused() -> None:
    """The result would fail Condition 4, so it is not a corollary of anything."""

    certificate = small_certificate()
    ceiling = dilation_ceiling(certificate)

    with pytest.raises(ValueError, match="not below the ceiling"):
        dilate(certificate, ceiling)
    with pytest.raises(ValueError, match="not below the ceiling"):
        dilate(certificate, ceiling * 2)
    with pytest.raises(ValueError, match="must be positive"):
        dilate(certificate, Fraction(0))
    assert dilate(certificate, Fraction(1)) == certificate


def test_the_tool_reports_the_corollary_from_the_file(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The command line prints the exact numbers and says what it did not decide."""

    assert main([str(CERTIFICATE_PATH), "--factor", str(REVIEW_FACTOR)]) == 0
    printed = capsys.readouterr().out

    assert f"D = {REVIEW_HALF_GAP_TANGENT}" in printed
    assert f"B(1 + D) = {REVIEW_CONTAINMENT}" in printed
    assert f"a B(1 + D) = {REVIEW_DILATED_CONTAINMENT}" in printed
    assert f"COROLLARY: s(11) >= {REVIEW_BOUNDED_SIDE}" in printed
    assert "not replayed here" in printed
    assert "not a further certificate" in printed


def test_the_tool_refuses_a_factor_the_containment_inequality_rejects(
    capsys: pytest.CaptureFixture[str],
) -> None:
    certificate = load_n11(CERTIFICATE_PATH)

    assert main([str(CERTIFICATE_PATH), "--factor", str(dilation_ceiling(certificate))]) == 1
    printed = capsys.readouterr().out

    assert "REFUSED" in printed
    assert "COROLLARY" not in printed


def test_without_a_factor_the_tool_reports_only_the_ceiling(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main([str(CERTIFICATE_PATH)]) == 0
    printed = capsys.readouterr().out

    assert f"ceiling 1 / (B(1 + D)) = {Fraction(900000000000, 899996306539)}" in printed
    assert "COROLLARY" not in printed
