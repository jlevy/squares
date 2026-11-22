"""The optional GMP execution preserves full exact native outcomes and margins."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools import n232_rational_source as source
from sqpack.witness import exact_verify


def _boundary_certificates() -> list[legacy.Certificate]:
    epsilon = Fraction(1, 10**80)
    contact = legacy.Certificate(
        2,
        Fraction(3),
        (
            legacy.Pose(Fraction(1, 2), Fraction(1, 2), Fraction(0)),
            legacy.Pose(Fraction(3, 2), Fraction(1, 2), Fraction(0)),
        ),
    )
    # Exactly 3/5 and 4/5 edge directions; conversion must not pass through a float.
    tilted = legacy.Certificate(
        2,
        Fraction(4),
        (
            legacy.Pose(Fraction(1), Fraction(1), Fraction(1, 3)),
            legacy.Pose(Fraction(9, 5), Fraction(8, 5), Fraction(1, 3)),
        ),
    )
    return [
        contact,
        replace(
            contact,
            poses=(contact.poses[0], replace(contact.poses[1], x=contact.poses[1].x - epsilon)),
        ),
        replace(
            contact,
            poses=(contact.poses[0], replace(contact.poses[1], x=contact.poses[1].x + epsilon)),
        ),
        replace(
            contact,
            poses=(replace(contact.poses[0], x=contact.poses[0].x - epsilon), contact.poses[1]),
        ),
        tilted,
    ]


@pytest.mark.parametrize("certificate", _boundary_certificates())
@pytest.mark.parametrize("control", kernel.JOBS)
def test_gmp_preserves_every_native_result_field(
    certificate: legacy.Certificate, control: str
) -> None:
    reference = kernel.run_case(certificate, control)
    accelerated = kernel.run_case(certificate, control, rational_backend="gmp")
    assert kernel.stable_row(accelerated) == kernel.stable_row(reference)


def test_gmp_keeps_exact_contacts_and_refuses_sub_spacing_penetration() -> None:
    contact, inward, outward, wall_inward, tilted = _boundary_certificates()
    for certificate, expected in (
        (contact, True),
        (inward, False),
        (outward, True),
        (wall_inward, False),
        (tilted, True),
    ):
        native = kernel.run_case(certificate, "positive", rational_backend="gmp")
        assert native["exact_verify"]["verification_passed"] is expected
        assert native["independent"]["verification_passed"] is expected
    native = kernel.run_case(contact, "positive", rational_backend="gmp")
    assert native["exact_verify"]["minimum_best_pair_gap"] == "0"
    assert native["exact_verify"]["minimum_containment_clearance"] == "0"
    native = kernel.run_case(inward, "positive", rational_backend="gmp")
    assert Fraction(native["exact_verify"]["minimum_best_pair_gap"]) == -Fraction(1, 10**80)


def test_gmp_preserves_shape_failure_and_does_not_mutate_input() -> None:
    witness = kernel.to_witness(_boundary_certificates()[-1])
    witness["squares"][0]["basis"][0] = "3/5"
    before = deepcopy(witness)
    reference, reference_report = exact_verify(witness)
    accelerated, accelerated_report = exact_verify(witness, rational_backend="gmp")
    assert accelerated == reference
    assert accelerated_report == reference_report
    assert not accelerated_report.valid
    assert any(kind == "shape" for kind, _detail in accelerated_report.failures)
    assert witness == before


def test_gmp_standard_jobs_still_validate_against_the_exact_member() -> None:
    certificate = _boundary_certificates()[0]
    for control in kernel.JOBS:
        row = kernel.run_case(certificate, control, rational_backend="gmp")
        kernel.validate_job(row, certificate, control)
        row["checker_input"]["side"] = "4"
        with pytest.raises(kernel.ReportError, match="complete source/control"):
            kernel.validate_job(row, certificate, control)


def test_issue1062_source_admits_only_its_retained_complete_native_jobs() -> None:
    """Exercise the production source adapter without recomputing its exact proof."""
    certificate = source.certificate(232)
    jobs = source.jobs(232, certificate)
    assert set(jobs) == set(kernel.JOBS)
    for control, row in jobs.items():
        for route in ("exact_verify", "independent"):
            result = row[route]
            assert result["verification_passed"] is (control == "positive")
            assert result["pairs_tested"] == 26796
    positive = jobs["positive"]
    for route in ("exact_verify", "independent"):
        assert positive[route]["minimum_best_pair_gap"] == "0"
        assert positive[route]["minimum_containment_clearance"] == "0"
    with pytest.raises(kernel.ReportError, match="differs from original source"):
        source.jobs(232, replace(certificate, side=certificate.side + Fraction(1, 10**80)))


def test_issue1062_source_refuses_changed_original_member(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(source.reports, "REPO", tmp_path)
    for relative in (source.ACQUISITION, source.ORIGINAL):
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((source.PACKET / relative).read_bytes())
    candidate = tmp_path / source.ORIGINAL
    original = candidate.read_bytes()
    candidate.write_bytes(original[:-1] + bytes([original[-1] ^ 1]))
    with pytest.raises(kernel.ReportError, match="original acquisition manifest"):
        source.certificate(232, tmp_path)


def test_issue1062_source_refuses_a_receipt_for_changed_coordinates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    certificate = source.certificate(232)
    retained = kernel.read_xz(source.PACKET / source.RECEIPT)
    damaged = deepcopy(retained)
    damaged["cases"][0]["checker_input"]["poses"][0][0] = "0"
    monkeypatch.setattr(kernel, "read_xz", lambda _path: damaged)
    with pytest.raises(kernel.ReportError, match="complete source/control"):
        source.jobs(232, certificate)
