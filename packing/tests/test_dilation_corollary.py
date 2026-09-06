"""The sharp dilation corollary: exact trigonometry extends the retained margin.

Section 4 of the 2026-09-05 adversarial review: dilating the retained ``s(11) >= 381/100``
certificate's atom positions, ``L`` and ``B`` by ``a = 250001/250000`` leaves the weights,
the net, the symmetry, the total mass and the coverage unchanged and keeps
``a B (1 + D) < 1``, so the same accepted data prove ``s(11) >= 95250381/25000000 =
3.81001524``. The whole strict rational family has supremum
``38100*sqrt(8100042893309449)/899996306539``. Rational density promotes that
supremum to a weak lower bound even though no member of the family is an endpoint
certificate. It does not license dividing ``L`` by ``B``, assert no-fit at the
endpoint, or prove a strict bound.

`devtools.dilation_corollary` recomputes every number from the file. These tests hold it
to the review's values, and check the invariance the corollary rests on where a sweep is
cheap enough to repeat.
"""

from __future__ import annotations

import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from cases.n11_fractional_certificate.replay import CERTIFICATE_PATH
from cases.n11_fractional_certificate.replay import load as load_n11
from cases.n12_fractional_certificate.replay import FIRST_RUNG_PATH as N12_RUNG_19_5
from cases.n12_fractional_certificate.replay import load as load_n12
from devtools import dilation_corollary as dilation
from devtools.dilation_corollary import (
    build_limit_record,
    coarse_condition_four_ceiling,
    corollary,
    dilate,
    limit_corollary,
    main,
    rational_subfactor_above,
    sharp_containment_holds,
    sharp_dilation_ceiling,
)
from sqpack.fractional.certificate import (
    Certificate,
    ConditionReport,
    Verdict,
    closed_form_conditions,
    verify,
)

#: The review's dilation, and the numbers it reports for the retained certificate.
REVIEW_FACTOR = Fraction(250001, 250000)
REVIEW_HALF_GAP_TANGENT = Fraction(207107, 90000000)
REVIEW_CONTAINMENT = Fraction(899996306539, 900000000000)
REVIEW_DILATED_CONTAINMENT = Fraction(224999976631056539, 225000000000000000)
REVIEW_BOUNDED_SIDE = Fraction(95250381, 25000000)
COARSE_FACTOR = Fraction(900000000000, 899996306539)
COARSE_BOUNDED_SIDE = Fraction(3429000000000, 899996306539)
LIMIT_RADICAND = 8100042893309449
LIMIT_FACTOR_EXACT = "10000*sqrt(8100042893309449)/899996306539"
LIMIT_FACTOR_SQUARED = Fraction(810004289330944900000000, 809993351783841654158521)
LIMIT_BOUNDED_SIDE_EXACT = "38100*sqrt(8100042893309449)/899996306539"
LIMIT_BOUNDED_SIDE_SQUARED = Fraction(11758103264356929262890000, 809993351783841654158521)
LIMIT_BOUNDED_SIDE_DECIMAL = "3.810025723614703"
SHARP_BAND_FACTOR = Fraction(500003, 500000)
SHARP_BAND_SIDE = Fraction(190501143, 50000000)
SHARP_BAND_SLACK = Fraction(
    33822158946641039188838841479,
    22500000000000000000000000000000000,
)
LIMIT_RECORD = CERTIFICATE_PATH.with_name("t-022-dilation-limit-corollary.json")
LIMIT_SOURCE = "packing/cases/n11_fractional_certificate/certificate.json"


def accepted_verdict(certificate: Certificate) -> Verdict:
    """The retained declaration as a verdict, for tests of the pure limit step."""

    least = Fraction(4001, 4000)
    return Verdict(
        (
            *closed_form_conditions(certificate),
            ConditionReport(
                "Condition 5 every reachable cell carries mass 1",
                f"least cell mass {least} at direction fixture",
                holds=True,
            ),
        ),
        certificate.total_mass,
        least,
        "fixture",
    )


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
    assert coarse_condition_four_ceiling(certificate) == 1 / REVIEW_CONTAINMENT
    assert coarse_condition_four_ceiling(certificate) == COARSE_FACTOR
    assert certificate.outer_side * coarse_condition_four_ceiling(certificate) == (
        COARSE_BOUNDED_SIDE
    )
    sharp = sharp_dilation_ceiling(certificate)
    assert sharp.coefficient == Fraction(10000, 899996306539)
    assert sharp.radicand == LIMIT_RADICAND
    assert sharp.exact == LIMIT_FACTOR_EXACT
    assert sharp.squared == LIMIT_FACTOR_SQUARED
    assert sharp.irrational
    assert sharp.squared > COARSE_FACTOR * COARSE_FACTOR


def test_the_review_dilation_is_a_corollary_of_the_retained_certificate() -> None:
    """``a = 250001/250000`` keeps Condition 4 and moves nothing else."""

    certificate = load_n11(CERTIFICATE_PATH)

    result = corollary(certificate, REVIEW_FACTOR)
    dilated = dilate(certificate, REVIEW_FACTOR)

    assert result.coarse_containment * REVIEW_FACTOR == REVIEW_DILATED_CONTAINMENT
    assert REVIEW_DILATED_CONTAINMENT < 1
    assert result.sharp_containment_left_squared < result.sharp_containment_right
    assert result.bounded_side == REVIEW_BOUNDED_SIDE
    assert result.bounded_side == Fraction("3.81001524")
    assert result.unchanged_condition_failures == ()
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
    """The sharp corollary stays below ``L / B`` because its support factor exceeds 1."""

    certificate = load_n11(CERTIFICATE_PATH)

    ceiling = sharp_dilation_ceiling(certificate)
    assert ceiling.squared < (1 / certificate.square_side) ** 2
    assert (
        certificate.outer_side**2 * ceiling.squared
        < (certificate.outer_side / certificate.square_side) ** 2
    )


def test_the_strict_dilation_family_proves_its_limit_as_a_weak_bound(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The endpoint is the supremum of certified sides, not an endpoint certificate."""

    certificate = load_n11(CERTIFICATE_PATH)
    monkeypatch.setattr(
        dilation,
        "verify",
        lambda _certificate, **_kwargs: accepted_verdict(certificate),
    )
    result = limit_corollary(certificate)

    assert result.factor_supremum.exact == LIMIT_FACTOR_EXACT
    assert result.factor_supremum.squared == LIMIT_FACTOR_SQUARED
    assert result.bounded_side.exact == LIMIT_BOUNDED_SIDE_EXACT
    assert result.bounded_side.squared == LIMIT_BOUNDED_SIDE_SQUARED
    assert result.bounded_side.squared > certificate.outer_side**2
    assert result.relation == ">="
    assert not result.endpoint_certificate
    assert result.requires_compactness is False


@pytest.mark.parametrize(
    "candidate_side",
    [
        Fraction(381, 100),
        COARSE_BOUNDED_SIDE,
        Fraction("3.8100257236147034071933954110"),
    ],
)
def test_a_rational_side_below_the_limit_has_a_strict_certificate_above_it(
    candidate_side: Fraction,
) -> None:
    """The direct rational increment gives an exact witness to the density step."""

    certificate = load_n11(CERTIFICATE_PATH)
    factor = rational_subfactor_above(certificate, candidate_side)

    assert factor > 0
    assert factor * factor < LIMIT_FACTOR_SQUARED
    rational_side = factor * certificate.outer_side
    assert candidate_side < rational_side
    assert rational_side * rational_side < LIMIT_BOUNDED_SIDE_SQUARED
    assert sharp_containment_holds(certificate, factor)


def test_a_rational_factor_between_the_coarse_and_sharp_ceilings_is_valid() -> None:
    """The new interval is real even though frozen coarse Condition 4 rejects it."""

    certificate = load_n11(CERTIFICATE_PATH)
    result = corollary(certificate, SHARP_BAND_FACTOR)
    scaled = dilate(certificate, SHARP_BAND_FACTOR)

    assert SHARP_BAND_FACTOR > COARSE_FACTOR
    assert result.bounded_side == SHARP_BAND_SIDE
    assert not all(condition.holds for condition in closed_form_conditions(scaled))
    assert result.sharp_containment_right - result.sharp_containment_left_squared == (
        SHARP_BAND_SLACK
    )
    assert sharp_containment_holds(certificate, SHARP_BAND_FACTOR)
    assert result.unchanged_condition_failures == ()


def test_the_limit_step_refuses_a_source_certificate_that_was_not_accepted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    certificate = load_n11(CERTIFICATE_PATH)
    rejected = Verdict(
        (ConditionReport("Condition 5", "deliberate control", holds=False),),
        certificate.total_mass,
        Fraction(999, 1000),
        "control",
    )

    monkeypatch.setattr(dilation, "verify", lambda _certificate, **_kwargs: rejected)

    with pytest.raises(ValueError, match="source certificate is not accepted"):
        limit_corollary(certificate)


def test_the_limit_step_refuses_a_verdict_reused_for_mutated_source_data(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Matching names and mass cannot smuggle a verdict across a changed certificate."""

    certificate = load_n11(CERTIFICATE_PATH)
    verdict = accepted_verdict(certificate)
    monkeypatch.setattr(dilation, "verify", lambda _certificate, **_kwargs: verdict)

    with pytest.raises(ValueError, match="source certificate is not accepted"):
        limit_corollary(replace(certificate, n=1))


def test_the_retained_limit_record_is_derived_from_the_frozen_certificate(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The checked-in record binds the source bytes and the exact limit theorem."""

    certificate = load_n11(CERTIFICATE_PATH)
    monkeypatch.setattr(
        dilation,
        "verify",
        lambda _certificate, **_kwargs: accepted_verdict(certificate),
    )

    built = build_limit_record(CERTIFICATE_PATH, source_name=LIMIT_SOURCE)
    retained = json.loads(LIMIT_RECORD.read_text(encoding="utf-8"))

    assert retained == built
    assert retained["conclusion"] == {
        "bounded_side": LIMIT_BOUNDED_SIDE_EXACT,
        "bounded_side_defining_polynomial": (
            "809993351783841654158521*x^2 - 11758103264356929262890000"
        ),
        "bounded_side_squared": str(LIMIT_BOUNDED_SIDE_SQUARED),
        "decimal": LIMIT_BOUNDED_SIDE_DECIMAL,
        "endpoint_certificate": False,
        "relation": ">=",
    }
    assert retained["strict_dilation_family"]["factor_supremum"] == LIMIT_FACTOR_EXACT
    assert retained["strict_dilation_family"]["factor_supremum_squared"] == str(
        LIMIT_FACTOR_SQUARED
    )
    assert retained["sharpened_containment"]["source_gap_below_one"] is True
    assert retained["proof"]["requires_compactness"] is False
    assert retained["proof"]["strict_family"] == (
        "for every rational q > 0 with q^2 below factor_supremum_squared, "
        "the sharpened containment theorem and the scaled source data rule out "
        "a packing at side q * outer_side"
    )


def test_the_record_refuses_a_source_that_changes_during_replay(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The source path must still contain the exact bytes that were parsed and hashed."""

    certificate = load_n11(CERTIFICATE_PATH)
    frozen = CERTIFICATE_PATH.read_bytes()
    reads = iter((frozen, frozen + b" "))
    monkeypatch.setattr(
        dilation,
        "verify",
        lambda _certificate, **_kwargs: accepted_verdict(certificate),
    )
    monkeypatch.setattr(dilation, "read_bounded", lambda _path: next(reads))

    with pytest.raises(ValueError, match="changed while"):
        build_limit_record(CERTIFICATE_PATH, source_name=LIMIT_SOURCE)


def test_the_record_refuses_duplicate_json_keys(
    tmp_path: Path,
) -> None:
    """The proof path reuses the certificate gate's strict JSON decoder."""

    duplicate = tmp_path / "duplicate.json"
    duplicate.write_bytes(b'{"n": 11,' + CERTIFICATE_PATH.read_bytes()[1:])

    with pytest.raises(ValueError, match="duplicate JSON object key 'n'"):
        build_limit_record(duplicate, source_name=LIMIT_SOURCE)


def test_the_limit_record_check_refuses_drift(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    certificate = load_n11(CERTIFICATE_PATH)
    monkeypatch.setattr(
        dilation,
        "verify",
        lambda _certificate, **_kwargs: accepted_verdict(certificate),
    )
    stale = tmp_path / "stale.json"
    stale.write_text("{}\n", encoding="utf-8")

    assert (
        main(
            [
                str(CERTIFICATE_PATH),
                "--source-name",
                LIMIT_SOURCE,
                "--check-limit-record",
                str(stale),
            ]
        )
        == 1
    )
    assert "stale limit record" in capsys.readouterr().err


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
    """A factor outside the sharp interval cannot inherit the no-fit proof."""

    certificate = small_certificate()

    with pytest.raises(ValueError, match="strict containment fails"):
        dilate(certificate, Fraction(2))
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
    assert "q^2 B^2(1 + D)^2" in printed
    assert LIMIT_FACTOR_EXACT in printed
    assert f"COROLLARY: s(11) >= {REVIEW_BOUNDED_SIDE}" in printed
    assert "not replayed here" in printed
    assert "not a further certificate" in printed


def test_the_tool_refuses_a_factor_the_containment_inequality_rejects(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main([str(CERTIFICATE_PATH), "--factor", "2"]) == 1
    printed = capsys.readouterr().out

    assert "REFUSED" in printed
    assert "COROLLARY" not in printed


def test_without_a_factor_the_tool_reports_only_the_ceiling(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main([str(CERTIFICATE_PATH)]) == 0
    printed = capsys.readouterr().out

    assert f"coarse Condition 4 ceiling 1 / (B(1 + D)) = {COARSE_FACTOR}" in printed
    assert f"sharp factor supremum = {LIMIT_FACTOR_EXACT}" in printed
    assert f"side supremum {LIMIT_BOUNDED_SIDE_EXACT}" in printed
    assert "COROLLARY" not in printed
