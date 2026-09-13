"""The sharp dilation corollary: exact trigonometry extends the retained margin.

Section 4 of the 2026-09-05 adversarial review: dilating the retained ``s(11) >= 381/100``
certificate's atom positions, ``L`` and ``B`` by ``a = 250001/250000`` leaves the weights,
the net, the symmetry, the total mass and the coverage unchanged and keeps
``a B (1 + D) < 1``, so the same accepted data prove ``s(11) >= 95250381/25000000 =
3.81001524``. The whole strict rational family has supremum
``38100*sqrt(8100042893309449)/899996306539``. Rational density and upward embedding
prove the ordinary exact lower bound at that supremum even though no member of the
family is an endpoint certificate. The argument does not license dividing ``L`` by
``B``, assert no-fit at the endpoint, or prove a strict bound.

`devtools.dilation_corollary` recomputes every number from the file. These tests hold it
to the review's values, and check the invariance the corollary rests on where a sweep is
cheap enough to repeat.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import cast

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
from sqpack.fractional.threshold import (
    ThresholdCertificate,
    ThresholdSweepDeadlineError,
    verify_threshold,
)
from tests.test_fractional_threshold_interval import tight_certificate

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


def test_the_strict_dilation_family_proves_the_exact_lower_bound_at_its_limit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The strict family proves ``>=`` at its supremum without a certificate there."""

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
    endpoint_status = retained["proof"]["endpoint_status"]
    assert (
        f"the dilation-limit theorem establishes s(11) >= {LIMIT_BOUNDED_SIDE_EXACT}"
        in endpoint_status
    )
    assert "endpoint_certificate is false" in endpoint_status
    assert (
        f"the method does not establish s(11) > {LIMIT_BOUNDED_SIDE_EXACT}" in endpoint_status
    )
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
    assert f"theorem establishes s(11) >= {LIMIT_BOUNDED_SIDE_EXACT}" in printed
    assert f"does not establish s(11) > {LIMIT_BOUNDED_SIDE_EXACT}" in printed
    assert "COROLLARY" not in printed


# --- threshold sources --------------------------------------------------------------


def threshold_record(certificate: ThresholdCertificate) -> dict[str, object]:
    """The fixture in the shape the threshold gate freezes, declarations included."""

    return {
        "id": "C-test-threshold-limit",
        "variant": "threshold",
        "n": certificate.n,
        "claim": f"s({certificate.n}) >= {certificate.outer_side}",
        "outer_side": str(certificate.outer_side),
        "square_side": str(certificate.square_side),
        "angle_limit": "207107/500000",
        "direction_steps": len(certificate.half_tangents) - 1,
        "symmetry": certificate.symmetry,
        "total_budget": str(certificate.total_budget),
        "least_cell_charge": "1",
        "atoms": [[str(a.x), str(a.y), str(a.weight)] for a in certificate.atoms],
        "threshold_atoms": [t.to_record() for t in certificate.threshold_atoms],
    }


def write_threshold(path: Path, record: dict[str, object]) -> Path:
    path.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    return path


def test_a_threshold_source_gets_the_point_formula_from_its_own_b_and_d() -> None:
    """The dilation geometry is the point certificate's, read through the point view."""

    certificate = tight_certificate()
    point = certificate.point_certificate

    ceiling = sharp_dilation_ceiling(certificate)

    assert ceiling == sharp_dilation_ceiling(point)
    gap = point.largest_half_gap_tangent
    assert ceiling.radicand == gap.denominator**2 + gap.numerator**2
    assert ceiling.coefficient == Fraction(
        point.square_side.denominator,
        point.square_side.numerator * (gap.denominator + gap.numerator),
    )
    assert ceiling.squared * (point.square_side * (1 + gap)) ** 2 == 1 + gap * gap
    assert coarse_condition_four_ceiling(certificate) == coarse_condition_four_ceiling(point)
    assert sharp_containment_holds(certificate, Fraction(1))


def test_dilating_a_threshold_certificate_moves_its_threshold_points_too() -> None:
    """A threshold atom left behind would charge a different set of cores."""

    certificate = tight_certificate()
    factor = Fraction(41, 40)

    dilated = dilate(certificate, factor)

    assert isinstance(dilated, ThresholdCertificate)
    assert dilated.outer_side == certificate.outer_side * factor
    assert dilated.square_side == certificate.square_side * factor
    assert [t.points for t in dilated.threshold_atoms] == [
        tuple((x * factor, y * factor) for x, y in t.points)
        for t in certificate.threshold_atoms
    ]
    assert [t.weight for t in dilated.threshold_atoms] == [
        t.weight for t in certificate.threshold_atoms
    ]
    assert [t.threshold for t in dilated.threshold_atoms] == [
        t.threshold for t in certificate.threshold_atoms
    ]
    assert dilated.total_budget == certificate.total_budget
    assert verify_threshold(dilated).minimum_cell_mass == (
        verify_threshold(certificate).minimum_cell_mass
    )


def test_a_threshold_record_round_trips_through_update_and_check(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The tool replays Conditions 1', 2', 3, 4 and 5' and writes the v3 record."""

    certificate = tight_certificate()
    source = write_threshold(tmp_path / "threshold.json", threshold_record(certificate))
    record_path = tmp_path / "limit.json"
    label = "packing/tests/fixture/threshold.json"

    assert (
        main([str(source), "--source-name", label, "--update-limit-record", str(record_path)])
        == 0
    )
    assert (
        main([str(source), "--source-name", label, "--check-limit-record", str(record_path)])
        == 0
    )
    assert "limit record agrees with the source certificate" in capsys.readouterr().out

    written = json.loads(record_path.read_text(encoding="utf-8"))
    ceiling = sharp_dilation_ceiling(certificate)
    assert written["schema"] == dilation.THRESHOLD_LIMIT_RECORD_SCHEMA
    assert written["source"]["variant"] == "threshold"
    assert written["source"]["total_budget"] == str(certificate.total_budget)
    assert written["source"]["minimum_cell_charge"] == "1"
    assert written["source"]["point_atoms"] == len(certificate.atoms)
    assert written["source"]["threshold_atoms"] == len(certificate.threshold_atoms)
    assert written["source"]["certificate"] == label
    assert written["source"]["sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert "total_mass" not in written["source"]
    assert (
        "Condition 5' every reachable cell is charged at least 1"
        in (written["source"]["accepted_conditions"])
    )
    assert written["strict_dilation_family"]["factor_supremum"] == ceiling.exact
    assert written["conclusion"]["bounded_side"] == (
        ceiling.scaled(certificate.outer_side).exact
    )
    assert written["conclusion"]["endpoint_certificate"] is False
    endpoint_status = written["proof"]["endpoint_status"]
    bounded_side = ceiling.scaled(certificate.outer_side).exact
    assert (
        f"the dilation-limit theorem establishes s({certificate.n}) >= {bounded_side}"
        in endpoint_status
    )
    assert (
        f"the method does not establish s({certificate.n}) > {bounded_side}" in endpoint_status
    )
    assert any(
        "Condition 5'" in invariant
        for invariant in written["strict_dilation_family"]["invariants"]
    )


def test_threshold_limit_record_reports_each_direction_and_preserves_the_record(
    tmp_path: Path,
) -> None:
    """Optional replay controls expose landed work without changing the evidence."""

    certificate = tight_certificate()
    source = write_threshold(tmp_path / "threshold.json", threshold_record(certificate))
    baseline = build_limit_record(source, workers=1)
    landed: list[tuple[int, Fraction, str]] = []

    controlled = build_limit_record(
        source,
        workers=1,
        progress=lambda index, minimum, label: landed.append((index, minimum, label)),
        deadline=float("inf"),
    )

    assert controlled == baseline
    assert [index for index, _minimum, _label in landed] == list(
        range(len(certificate.directions))
    )
    assert [label for _index, _minimum, label in landed] == [
        direction.label for direction in certificate.directions
    ]


def test_threshold_limit_record_checks_the_deadline_after_record_assembly(
    tmp_path: Path,
) -> None:
    """A replay that overruns after its final direction cannot publish a stale success."""

    certificate = tight_certificate()
    source = write_threshold(tmp_path / "threshold.json", threshold_record(certificate))
    calls = 0
    last_allowed_call = 2 * len(certificate.directions) + 2

    def clock() -> float:
        nonlocal calls
        calls += 1
        return 0.0 if calls <= last_allowed_call else 2.0

    with pytest.raises(ThresholdSweepDeadlineError, match="absolute deadline"):
        build_limit_record(source, workers=1, deadline=1.0, clock=clock)

    assert calls == last_allowed_call + 1


def test_a_point_record_still_round_trips_through_update_and_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The v2 shape a point source emits is exactly what it emitted before."""

    certificate = load_n11(CERTIFICATE_PATH)
    monkeypatch.setattr(
        dilation,
        "verify",
        lambda _certificate, **_kwargs: accepted_verdict(certificate),
    )
    record_path = tmp_path / "limit.json"

    assert (
        main(
            [
                str(CERTIFICATE_PATH),
                "--source-name",
                LIMIT_SOURCE,
                "--update-limit-record",
                str(record_path),
            ]
        )
        == 0
    )
    assert (
        main(
            [
                str(CERTIFICATE_PATH),
                "--source-name",
                LIMIT_SOURCE,
                "--check-limit-record",
                str(record_path),
            ]
        )
        == 0
    )
    capsys.readouterr()

    written = json.loads(record_path.read_text(encoding="utf-8"))
    assert written["schema"] == dilation.LIMIT_RECORD_SCHEMA
    assert "variant" not in written["source"]
    assert written["source"]["total_mass"] == str(certificate.total_mass)
    assert written == json.loads(LIMIT_RECORD.read_text(encoding="utf-8"))


def test_a_tampered_threshold_record_is_refused(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Moving one threshold-atom point breaks the source premise, and nothing is written."""

    certificate = tight_certificate()
    record = threshold_record(certificate)
    atoms = cast(list[dict[str, object]], record["threshold_atoms"])
    points = cast(list[list[str]], atoms[0]["points"])
    points[0] = [str(Fraction(points[0][0]) + Fraction(1, 8)), points[0][1]]
    source = write_threshold(tmp_path / "tampered.json", record)
    record_path = tmp_path / "limit.json"

    assert main([str(source), "--update-limit-record", str(record_path)]) == 1
    assert "REFUSED" in capsys.readouterr().err
    assert not record_path.exists()


def test_a_threshold_record_whose_declarations_disagree_is_refused(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The declared budget and least charge are held to the replayed decision."""

    certificate = tight_certificate()
    record = threshold_record(certificate)
    record["least_cell_charge"] = "1/2"
    source = write_threshold(tmp_path / "declared.json", record)

    assert main([str(source), "--update-limit-record", str(tmp_path / "limit.json")]) == 1
    assert "declared least_cell_charge does not match" in capsys.readouterr().err


def test_a_threshold_record_without_a_declared_least_charge_is_refused(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A source that declares no least charge cannot carry a limit record."""

    certificate = tight_certificate()
    record = threshold_record(certificate)
    del record["least_cell_charge"]
    source = write_threshold(tmp_path / "undeclared.json", record)

    assert main([str(source), "--update-limit-record", str(tmp_path / "limit.json")]) == 1
    assert "declared least_cell_charge does not match" in capsys.readouterr().err
