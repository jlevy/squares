"""T-058: exact rectangle-certificate ceilings, and the mass-budget admission refusal."""

from __future__ import annotations

import gzip
import json
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import certify_rectangle_ceiling as tool
from sqpack.rectangle_ceiling import (
    ALPHA,
    CORE_SIDE,
    CeilingCertificate,
    CeilingError,
    Core,
    certificate_from_document,
    grid_certificate,
    net_orientation,
    place_cores,
    premise_checks,
    verify_ceiling,
)
from sqpack.rectangle_density import CandidateError, load_candidate, parse_candidate
from sqpack.witness import load_witness

ROOT = Path(__file__).parents[1]
RECEIPTS = ROOT / "resources/web/wand125-tools-2026-09-29/receipts"


def test_every_numeric_premise_of_the_general_ceiling_holds_exactly() -> None:
    premises = premise_checks()

    assert premises
    assert all(premises.values()), premises
    assert Fraction(399908091, 400000000) == ALPHA


def test_grid_cores_reach_exactly_b_times_ceil_sqrt_n() -> None:
    for n in range(1, 26):
        certificate = grid_certificate(n)
        k = next(k for k in range(1, 6) if k * k >= n)

        assert certificate.side == CORE_SIDE * k
        assert verify_ceiling(certificate).verified
        shrunk = replace(certificate, side=certificate.side - Fraction(1, 10**9))
        assert not verify_ceiling(shrunk).verified


def test_touching_cores_pass_and_overlapping_or_missing_cores_refuse() -> None:
    b = CORE_SIDE
    touching = CeilingCertificate(
        2,
        2 * b,
        b,
        (Core(b / 2, b / 2, 0, reflected=False), Core(3 * b / 2, b / 2, 0, reflected=False)),
    )
    assert verify_ceiling(touching).verified

    overlap = replace(
        touching,
        cores=(
            touching.cores[0],
            replace(touching.cores[1], x=3 * b / 2 - Fraction(1, 10**12)),
        ),
    )
    assert "overlap" in " ".join(verify_ceiling(overlap).reasons)

    # A net rotation of one core makes the two touching cores intersect.
    rotated = replace(touching, cores=(touching.cores[0], replace(touching.cores[1], index=1)))
    assert not verify_ceiling(rotated).verified

    assert not verify_ceiling(replace(touching, n=3)).verified


def test_malformed_ceiling_certificates_are_refused_rather_than_decided() -> None:
    core = Core(Fraction(1, 2), Fraction(1, 2), 0, reflected=False)
    with pytest.raises(CeilingError):
        net_orientation(201)
    with pytest.raises(CeilingError):
        verify_ceiling(
            CeilingCertificate(1, Fraction(1), CORE_SIDE, (replace(core, index=-1),))
        )
    with pytest.raises(CeilingError):
        verify_ceiling(CeilingCertificate(1, Fraction(1), Fraction(1), (core,)))
    with pytest.raises(CeilingError):
        verify_ceiling(CeilingCertificate(1, 1, CORE_SIDE, (core,)))  # type: ignore[arg-type]


def test_rotated_witness_needs_more_than_b_and_less_than_alpha() -> None:
    """n = 5 has a square at 45 degrees, which is not a net angle."""

    witness = load_witness(ROOT / "witnesses/known-best/n-005.yaml")
    placement = place_cores(witness.get("witness", witness))
    assert placement is not None
    assert not placement.aligned
    # 2 + sqrt(2)/2 lies strictly between these decimals.
    low, high = Fraction("2.70710678118"), Fraction("2.70710678119")

    assert CORE_SIDE * high < placement.certificate.side < ALPHA * low


def test_retained_certificates_replay_and_match_the_receipt() -> None:
    receipt = json.loads((RECEIPTS / "ceiling-certificates-2026-10-02.json").read_text())
    certificates = json.loads(
        gzip.decompress((RECEIPTS / "ceiling-certificates-2026-10-02.json.gz").read_bytes())
    )

    assert sorted(map(int, certificates)) == list(range(1, 101))
    for row in receipt["rows"]:
        certificate = certificate_from_document(certificates[str(row["n"])])
        assert certificate.n == row["n"]
        assert certificate.side == Fraction(row["ceiling"])
        assert verify_ceiling(certificate).verified
    summary = receipt["summary"]
    assert summary["verified"] == summary["proves_factor_times_ub"] == 100
    assert summary["proves_B_times_ub"] == summary["net_aligned_routes"] == 64


# The receipt keeps the witnesses of 2 October 2026, so it samples counts whose house has
# not moved since: 29 left the sample on 17 October, when its witness became PR #622's
# certificate (T-195), as 51, 68 to 70, 83 to 84 and 86 to 88 had moved before.
@pytest.mark.parametrize("n", [5, 37, 64])
def test_receipt_rows_reproduce_from_the_witnesses_and_source_table(n: int) -> None:
    receipt = json.loads((RECEIPTS / "ceiling-certificates-2026-10-02.json").read_text())
    row, _ = tool.certify(n, tool.source_table()[n])

    assert row == receipt["rows"][n - 1]


def test_rounded_table_value_is_below_its_own_exact_witness() -> None:
    """The review's n = 26 example: the float 5.62132 is below 7/2 + 3 sqrt(2)/2."""

    ub = Fraction(tool.source_table()[26]["ub"])
    # (ub - 7/2)^2 * 4/9 < 2 means ub < 7/2 + (3/2) sqrt 2.
    assert (ub - Fraction(7, 2)) ** 2 * Fraction(4, 9) < 2


# Admission: the false "s(1) >= 1.5" input must never reach coverage.

ADMISSION = RECEIPTS / "admission-scaled.json"


def _admission_data() -> dict:
    data = json.loads(ADMISSION.read_text())
    return {key: data[key] for key in ("n", "L", "B", "rectangles", "weights")}


def test_retained_false_s1_input_is_refused_on_the_mass_budget() -> None:
    with pytest.raises(CandidateError, match="strictly between zero and n"):
        load_candidate(ADMISSION, n=1, expected_side=Fraction(3, 2))


def test_admission_recomputes_mass_and_ignores_a_declared_total() -> None:
    data = _admission_data() | {"mass": 0.5}

    with pytest.raises(CandidateError, match="strictly between zero and n"):
        parse_candidate(data, n=1, expected_side=Fraction(3, 2))


@pytest.mark.parametrize("weight", ["1", "289/10"])
def test_mass_at_or_above_the_announced_count_is_refused(weight: str) -> None:
    data = _admission_data() | {"weights": [weight]}

    with pytest.raises(CandidateError, match="strictly between zero and n"):
        parse_candidate(data, n=1)


def test_budget_is_the_only_admission_defect_of_the_false_input() -> None:
    accepted = parse_candidate(_admission_data() | {"weights": ["1/2"]}, n=1)

    assert accepted.mass == Fraction(1, 2) < accepted.n


def test_announced_count_and_side_must_match_the_checked_input() -> None:
    with pytest.raises(CandidateError, match="count"):
        parse_candidate(_admission_data(), n=29)
    with pytest.raises(CandidateError, match="side"):
        parse_candidate(
            _admission_data() | {"weights": ["1/2"]}, n=1, expected_side=Fraction(8, 5)
        )
