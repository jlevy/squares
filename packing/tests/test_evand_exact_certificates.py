"""Evan Daniel's exact certificates (T-098, T-101): the reader, the conversion and the receipts.

`devtools.evand_exact_certificates` reads a certificate format no checker here read
before, converts it without rounding and hands it to this repository's two exact
checkers. These tests hold the reader to the format, the conversion to the meaning the
source's own checkers give it, the deciders to refusing what must be refused, and the
committed receipts and records to the retained certificates.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import apply_exact_ceilings, apply_exact_optima, apply_upper_bound_packets
from devtools import check_rational_witness_independent as independent
from devtools import evand_exact_certificates as certificates
from devtools.check_source_coverage import load_claims
from devtools.source_supersession import superseded_counts
from devtools.upper_bound_packets import verified_value
from sqpack.assurance import bounds_agree_at_declared_precision, check_case_semantics
from sqpack.witness import exact_verify
from sqpack.yamlio import safe_load

#: Two axis-parallel unit squares side by side, 1e-20 apart, in a box 1e-20 wider than
#: they need, and a third rotated by t = 1/3 well clear of both.
SMALL = (
    "# a test certificate\n"
    "3 400000000000000000001/100000000000000000000\n"
    "1/2 1/2 0\n"
    "150000000000000000001/100000000000000000000 1/2 0\n"
    "2 5/2 1/3\n"
)


def _small() -> certificates.Certificate:
    return certificates.parse(SMALL)


def _verdicts(certificate: certificates.Certificate) -> tuple[bool, bool]:
    first, _ = exact_verify(certificates.basis_witness(certificate))
    second = independent.check_squares(
        certificates.corner_squares(certificate), certificate.side
    )
    return bool(first["verification_passed"]), bool(second["verification_passed"])


def test_the_reader_takes_the_format_and_ignores_comments() -> None:
    certificate = _small()
    assert certificate.n == 3
    assert certificate.side == Fraction(400000000000000000001, 100000000000000000000)
    assert certificate.poses[2].t == Fraction(1, 3)


@pytest.mark.parametrize(
    "text",
    [
        "2 4\n1/2 1/2 0\n",  # a row missing
        "1 4\n1/2 1/2 0\n3 3 0\n",  # a row the source's checkers would ignore
        "1 4\n1/2 1e0 0\n",  # an exponent, which Fraction reads and the format does not name
        "1 4\n1/2 1_0 0\n",  # an underscore, likewise
        "1.0 4\n1/2 1/2 0\n",  # a count that is not an integer
        "1 -4\n1/2 1/2 0\n",  # a side that is not positive
        "1 4\n1/2 1/2\n",  # a row without its tangent
    ],
)
def test_the_reader_refuses_what_the_format_does_not_state(text: str) -> None:
    with pytest.raises(certificates.CertificateError):
        certificates.parse(text)


def test_the_header_must_name_the_count_the_file_is_for() -> None:
    with pytest.raises(certificates.CertificateError, match="file name"):
        certificates.parse(SMALL, expected_n=4)


@pytest.mark.parametrize(
    "t", [Fraction(0), Fraction(1, 3), Fraction(-7, 5), Fraction(10**30, 3)]
)
def test_the_tangent_gives_a_unit_basis_exactly(t: Fraction) -> None:
    c, s = certificates.Pose(Fraction(0), Fraction(0), t).basis
    assert c * c + s * s == 1


def test_the_corners_are_the_rotation_the_source_checkers_use() -> None:
    """``(x + c a - s b, y + s a + c b)`` for ``a, b = ±1/2``, as both of the source's
    checkers build them: at t = 1, a quarter turn, the square maps onto itself."""
    pose = certificates.Pose(Fraction(3), Fraction(5), Fraction(1, 3))
    c, s = pose.basis
    assert (c, s) == (Fraction(4, 5), Fraction(3, 5))
    half = Fraction(1, 2)
    assert pose.corners()[0] == (3 + c * half - s * half, 5 + s * half + c * half)
    quarter = certificates.Pose(Fraction(0), Fraction(0), Fraction(1))
    assert sorted(quarter.corners()) == sorted(
        certificates.Pose(Fraction(0), Fraction(0), Fraction(0)).corners()
    )


def test_both_deciders_accept_a_valid_certificate() -> None:
    assert _verdicts(_small()) == (True, True)


def test_both_deciders_refuse_each_control() -> None:
    certificate = _small()
    overlapped, row = certificates.overlap_control(certificate)
    assert row["squares"] == [0, 1]
    assert _verdicts(overlapped) == (False, False)
    (past, past_row), (one, one_row) = certificates.shrink_controls(certificate)
    assert past_row["expect"] == "refused"
    assert _verdicts(past) == (False, False)
    # The box has 1e-20 to spare, far more than one unit of its denominator.
    assert one_row["expect"] == "accepted"
    assert _verdicts(one) == (True, True)


def test_the_serialized_certificate_reads_back_as_itself() -> None:
    certificate = _small()
    assert certificates.parse(certificates.serialize(certificate)) == certificate


def test_the_held_count_is_never_read(tmp_path: Path) -> None:
    (tmp_path / "n-17.cert").write_text("this is never parsed\n", encoding="utf-8")
    (tmp_path / "n-3.cert").write_text(SMALL, encoding="utf-8")
    assert certificates.certificate_counts(tmp_path) == [3]
    with pytest.raises(certificates.CertificateError, match="held"):
        certificates.check_one(str(tmp_path / "n-17.cert"))


def test_a_side_that_terminates_is_written_out_in_full() -> None:
    assert certificates.terminating_decimal(Fraction(1, 8)) == "0.125"
    assert certificates.terminating_decimal(Fraction(1, 3)) is None


def test_the_committed_receipts_agree_with_the_packet() -> None:
    assert certificates.receipt_problems() == []


def test_the_smallest_retained_certificate_is_decided_exactly() -> None:
    path = certificates.certificate_path(certificates.CERTS, 68)
    row = certificates.decide(
        certificates.parse(path.read_text(encoding="utf-8"), expected_n=68)
    )
    assert row["exact_verify"]["passed"]
    assert row["independent"]["passed"]


def test_the_claims_record_is_the_retained_certificates() -> None:
    """`check_source_coverage` reads the packet's certificate directory as its claims:
    the 48 improving counts and the 77 ceiling counts, each at the side its header gives,
    written out in full."""
    claims = load_claims(certificates.CERTS)
    assert tuple(sorted(claims)) == certificates.RETAINED
    assert len(certificates.RETAINED) == 125
    assert not set(certificates.IMPROVING) & set(certificates.CEILINGS)
    assert claims[211] == apply_exact_optima.side_text(211)
    assert claims[28] == apply_exact_ceilings.committed()[28]["certified_side_decimal"]


def test_the_earlier_evidence_is_the_packets_and_the_catalogues() -> None:
    packets = {
        identifier
        for registration in apply_upper_bound_packets.REGISTRATIONS
        for identifier in (
            registration.report,
            registration.replay,
            registration.interval_replay,
        )
    }
    assert (
        packets
        | {
            "E-kingbird-upper-register",
            "E-kingbird-grid-completeness",
        }
        == apply_exact_optima.EARLIER_UPPER
    )


@pytest.mark.parametrize("n", [68, 126, 206, 211])
def test_the_records_are_the_layer_applied_to_themselves(n: int) -> None:
    path = apply_exact_optima.FRONTIER / f"n-{n:03d}.md"
    text = path.read_text(encoding="utf-8")
    normalized = apply_upper_bound_packets.normalized
    assert normalized(apply_exact_optima.apply_case(n, text)) == normalized(text)


def test_the_coverage_record_is_the_layer_applied_to_itself() -> None:
    text = apply_exact_optima.COVERAGE.read_text(encoding="utf-8")
    assert apply_exact_optima.coverage_text(text) == text


def _conjecture_findings(conjecture: str) -> list[str]:
    case = {
        "n": 126,
        "conjectured_optimum": conjecture,
        "verified_upper_bound": {"value": "11.7747351323878328426"},
    }
    return [e for e in check_case_semantics(case, {}) if "conjectured optimum" in e]


def test_a_conjecture_above_the_certified_ceiling_is_refused() -> None:
    # The catalogue's side, which n = 126 kept until review finding EX-1.
    expected = (
        "n=126: conjectured optimum 11.77473513240654 exceeds the verified ceiling "
        "11.7747351323878328426"
    )
    assert _conjecture_findings("11.77473513240654") == [expected]


@pytest.mark.parametrize(
    "conjecture",
    [
        "11.77473513238783",
        "11.7747351323878",
        # 1.6e-16 above the ceiling, inside half a unit of its last place, 5e-16.
        "11.774735132387833",
        "integer",
    ],
)
def test_a_conjecture_at_the_ceiling_to_its_last_place_is_kept(conjecture: str) -> None:
    assert _conjecture_findings(conjecture) == []


def test_a_conjecture_past_half_a_unit_of_its_last_place_is_refused() -> None:
    # 7.2e-15 above the ceiling, outside half a unit of its last place, 5e-15.
    assert len(_conjecture_findings("11.77473513238784")) == 1


def test_the_kkt_sentence_restates_each_count_s_second_order_report() -> None:
    reports = apply_exact_optima.reports()
    assert sorted(reports) == sorted(certificates.IMPROVING)
    kkt = [n for n, (status, _) in reports.items() if status == apply_exact_optima.KKT_STATUS]
    assert len(kkt) == 44
    for n in kkt:
        assert apply_exact_optima.report_sentence(n, *reports[n]).startswith(
            "The source reports the exact point as a KKT local minimum"
        )


def test_a_kkt_count_on_another_second_order_report_is_refused() -> None:
    status = apply_exact_optima.KKT_STATUS
    with pytest.raises(ValueError, match="not positive definite"):
        apply_exact_optima.report_sentence(211, status, "PSD with 42 zero modes")
    bound_only = apply_exact_optima.report_sentence(211, "bound only", "PSD with 42 zero modes")
    assert bound_only == apply_exact_optima.BOUND_ONLY


def test_the_ceiling_counts_are_the_ones_the_survey_derives() -> None:
    """Every count whose certificate, rounded up at the printed precision, lowers the
    verified ceiling is listed, and no other: the committed survey, the live records and
    the retained certificates agree."""
    assert apply_exact_ceilings.survey_problems() == []
    assert 17 not in certificates.CEILINGS
    assert len(certificates.CEILINGS) == 77


def test_n29_trails_its_report_and_keeps_its_own_ceiling() -> None:
    """The one trailing count the certificates do not move: its interval-certified bound
    lies below the certificate's side, so a rounding of that side would only weaken it."""
    receipt = json.loads(apply_exact_ceilings.SURVEY_RECEIPT.read_text(encoding="utf-8"))
    unmoved = {row["n"]: row for row in receipt["unmoved"]}
    assert sorted(unmoved) == [29]
    assert unmoved[29]["certified_above_verified_by"] > 0
    assert 29 not in certificates.CEILINGS
    case = certificates.case_record(29)
    assert case["verified_upper_bound"]["evidence"] == ["E-n029-interval-certified-upper"]


@pytest.mark.parametrize("n", [28, 50, 69, 83, 127, 230, 300])
def test_the_ceiling_records_are_the_layer_applied_to_themselves(n: int) -> None:
    path = apply_exact_ceilings.FRONTIER / f"n-{n:03d}.md"
    text = path.read_text(encoding="utf-8")
    normalized = apply_upper_bound_packets.normalized
    assert normalized(apply_exact_ceilings.apply_case(n, text)) == normalized(text)


def test_the_coverage_record_is_the_ceiling_layer_applied_to_itself() -> None:
    text = apply_exact_ceilings.COVERAGE.read_text(encoding="utf-8")
    assert apply_exact_ceilings.coverage_text(text) == text


def test_each_ceiling_is_the_certified_side_rounded_up_at_the_printed_precision() -> None:
    """The verified value is at least the certificate's side, one unit of the printed last
    place above the printed side, and agrees with the report exactly where the catalogue
    prints no closed form."""
    for n, row in apply_exact_ceilings.committed().items():
        case = certificates.case_record(n)
        later = superseded_counts(
            safe_load(apply_exact_ceilings.COVERAGE.read_text()),
            {apply_exact_ceilings.COVERAGE_ID},
        )
        if n in later:
            # The frozen certificate still proves its own upper bound. A later
            # packing may now own either lane; that never changes the audited side.
            assert Fraction(row["verified_value"]) >= Fraction(row["certified_side"]), n
            assert apply_exact_ceilings.EXACT_REPLAY in case["evidence"], n
            continue
        verified = case["verified_upper_bound"]
        side = Fraction(row["certified_side"])
        assert verified["value"] == verified_value(row["printed_side"], side), n
        assert Fraction(verified["exact_form"]) == Fraction(verified["value"]) >= side, n
        assert verified["evidence"] == [
            apply_exact_ceilings.EXACT_REPLAY,
            apply_exact_ceilings.SOURCE_REPLAY,
        ], n
        agrees = bounds_agree_at_declared_precision(case["reported_upper_bound"], verified)
        assert agrees == (not case["reported_upper_bound"].get("exact_form")), n
        assert agrees == row["agrees_with_report"], n
        assert any(b["kind"] == "mathematics" for b in case["blockers"]) != agrees, n


def test_every_closed_form_lies_below_its_certificate_and_six_are_rational() -> None:
    """A certificate below the catalogue's closed form would be a smaller packing, not a
    ceiling, and `survey` refuses one; at every closed-form count the side lies above it.
    Six of those forms are rational, which a contact-exact rational certificate could
    reach, and the blockers say which (the review's EC-1 and EC-3)."""
    rows = apply_exact_ceilings.committed()
    closed = {n: row for n, row in rows.items() if row["printed_exact_form"]}
    assert len(closed) == 55
    assert all(row["certified_above_exact_side_by"] > 0 for row in closed.values())
    rational = sorted(n for n, row in closed.items() if row["printed_exact_form_degree"] == 1)
    assert rational == [50, 171, 198, 230, 261, 293]
    assert apply_exact_ceilings.closed_form_degree("7 + (4/7)") == 1
    assert apply_exact_ceilings.closed_form_degree("7 - (1/2)sqrt(2) + sqrt(1 + sqrt(2))") == 4
    for n, row in closed.items():
        blocker = apply_exact_ceilings.trailing_blocker(row, ["E-kingbird-upper-register"])
        irrational = "an irrational side, which no rational certificate reaches"
        assert (irrational in blocker["detail"]) == (n not in rational), n


def test_n50_certificate_is_53_over_7_on_a_rational_grid_scaled_outward() -> None:
    """At n = 50, whose catalogue side is the rational 53/7, the certificate appears to be a
    contact-exact rational packing scaled by 1 + 1e-20 (the review's EC-1, its fix check's
    FC-2 and FC-4): undone, the side is 53/7 rounded up at 30 decimals, every square the
    source does not list as free has tangent 0 or 1/3 to 1e-30, a 3-4-5 rotation, and 42 of
    those 44 have centres on a grid of 1/350 to 3e-36. Squares 24 and 25 (0-based) sit
    8e-17 off it, along their own 3-4-5 edge direction, so the snapped packing at 53/7 is a
    conjecture this test does not decide."""
    certificate = certificates.parse(
        certificates.certificate_path(certificates.CERTS, 50).read_text(encoding="utf-8"),
        expected_n=50,
    )
    free = set(certificates.reported_free()[50])
    assert sorted(free) == [5, 19, 23, 26, 32, 46]
    scale = 1 + Fraction(1, 10**20)
    assert 0 <= certificate.side / scale - Fraction(53, 7) < Fraction(1, 10**30)
    off: dict[int, tuple[Fraction, Fraction]] = {}
    for place, pose in enumerate(certificate.poses):
        if place in free:
            continue
        assert pose.t == 0 or abs(pose.t - Fraction(1, 3)) < Fraction(1, 10**30), place
        x, y = pose.x / scale * 350, pose.y / scale * 350
        dx, dy = (x - round(x)) / 350, (y - round(y)) / 350
        if max(abs(dx), abs(dy)) > Fraction(3, 10**36):
            off[place] = (dx, dy)
    assert sorted(off) == [24, 25]
    for dx, dy in off.values():
        assert abs(dx * 3 - dy * 4) < Fraction(1, 10**30)  # along (4, 3)
        assert Fraction(7, 10**17) ** 2 < dx * dx + dy * dy < Fraction(9, 10**17) ** 2
