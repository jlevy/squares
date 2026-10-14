"""Issues #528 and #529: Daniil Ostashev's compositions and Rio Calle's n = 102 layout.

#528's three sqcert certificates are retained under the source's MIT licence and read by
the `sqcert` adapter #501 added. #529 publishes no exact certificate: its layout states
decimal centres and rotations in radians, the tree has no licence, and the packet keeps
the exact certificate the `calle-txt` adapter derives from the pinned layout. The general
importer's checks run on both packets through ``test_upper_bound_reports``; these hold
the new adapter, its radian half-angle tangent and what is particular to the packets.
Every test reads retained packets or synthetic bytes; none needs the network.
"""

from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from fractions import Fraction
from typing import Any

import mpmath as mp
import pytest

from devtools import evand_exact_certificates as legacy
from devtools import upper_bound_reports as reports

OSTASHEV_528 = "dostashev-records-2026-10-12"
CALLE = "riocalle-n102-2026-10-12"
#: The sides issue #528 prints, certified and rounded up at 38 places.
ISSUE_528 = {
    175: "13.76417431748659662942782322004234282577",
    232: "15.76417431748659662944782322004234282577",
    264: "16.77473513238783284261026458732177098083",
}
PLACES = {reports.HALF_ANGLE_PLACES: "40"}


def _rows(name: str) -> dict[int, dict[str, Any]]:
    rows = reports.check_claims(reports.packet_path(name))["results"]
    return {row["n"]: row for row in rows}


def _margin(row: Mapping[str, Any]) -> Fraction:
    return Fraction(row["difference"])


# --------------------------------------------------------------------------- the radian tangent


ANGLES = ["1e-15", "-6.32021957015244111e-15", "0.75", "-1.5", "3.1"]


@pytest.mark.parametrize("radians", ANGLES)
@pytest.mark.parametrize("places", [30, 40, 100])
def test_a_radian_half_angle_tangent_is_its_exact_value_rounded_down(
    radians: str, places: int
) -> None:
    angle = Fraction(Decimal(radians))
    tangent = reports.half_angle_tangent_radians(angle, places)
    assert 10**places % tangent.denominator == 0
    with mp.workdps(places + 60):
        exact = mp.tan(mp.mpf(angle.numerator) / angle.denominator / 2)
        assert mp.mpf(tangent.numerator) / tangent.denominator <= exact
        assert exact < mp.mpf(tangent.numerator) / tangent.denominator + mp.mpf(10) ** -places


def test_a_zero_radian_angle_has_the_exact_tangent_zero() -> None:
    assert reports.half_angle_tangent_radians(Fraction(0), 40) == 0


def test_the_degree_tangent_is_unchanged_by_the_shared_floor() -> None:
    # Both units now round through one helper; a degree angle keeps its value.
    assert reports.half_angle_tangent(Fraction(90), 30) == 1
    radians = reports.half_angle_tangent_radians(Fraction(1, 2), 40)
    with mp.workdps(100):
        degrees = Fraction(str(mp.mpf(1) / 2 * 180 / mp.pi))
    assert abs(reports.half_angle_tangent(degrees, 40) - radians) <= Fraction(1, 10**40)


# --------------------------------------------------------------------------- calle-txt

#: Rio Calle's text: two labelled comment lines and one of prose, then ``x y theta`` rows.
CALLE_TXT = (
    "# n = 2\n"
    "# s = 3.0\n"
    "# x y theta(rad) — square centres in the box [0, s]², side 1\n"
    "1.00000000000000000e+00 1.00000000000000000e+00 0.00000000000000000e+00\n"
    "2.0 2.0 7.5e-01\n"
).encode()


def test_the_calle_adapter_reads_every_decimal_exactly_and_rounds_each_tangent_down() -> None:
    certificate = reports.parse_certificate(CALLE_TXT, 2, "calle-txt", PLACES)
    assert certificate.side == 3
    assert [(pose.x, pose.y) for pose in certificate.poses] == [(1, 1), (2, 2)]
    assert certificate.poses[0].t == 0
    assert certificate.poses[1].t == reports.half_angle_tangent_radians(Fraction(3, 4), 40)
    # Prose comments are read and not believed; blank lines are skipped.
    relabelled = CALLE_TXT.replace(b"side 1", b"side 2").replace(b"\n2.0", b"\n\n2.0")
    assert reports.parse_certificate(relabelled, 2, "calle-txt", PLACES) == certificate


@pytest.mark.parametrize(
    ("raw", "message"),
    [
        (CALLE_TXT.replace(b"# n = 2", b"# n = 3"), "`# n = 2` once"),
        (CALLE_TXT.replace(b"# n = 2\n", b""), "`# n = 2` once"),
        (CALLE_TXT.replace(b"# n = 2\n", b"# n = 2\n# n = 2\n"), "`# n = 2` once"),
        (CALLE_TXT.replace(b"# s = 3.0\n", b""), "`# s = S` once"),
        (CALLE_TXT.replace(b"# s = 3.0\n", b"# s = 3.0\n# s = 4.0\n"), "`# s = S` once"),
        (CALLE_TXT.replace(b"# s = 3.0", b"# s = 3"), "`# s = S` once"),
        (CALLE_TXT.replace(b"2.0 2.0 7.5e-01", b"2 2.0 7.5e-01"), "decimal"),
        (CALLE_TXT.replace(b"2.0 2.0 7.5e-01", b"2.0 2.0 7.5E-01"), "decimal"),
        (CALLE_TXT.replace(b"2.0 2.0 7.5e-01", b"2.0 2.0 nan"), "decimal"),
        (CALLE_TXT.replace(b"2.0 2.0 7.5e-01", b"2.0 2.0 1/2"), "decimal"),
        (CALLE_TXT.replace(b"2.0 2.0 7.5e-01", b"2.0 2.0 " + b"1" * 70 + b".0"), "decimal"),
        (CALLE_TXT.replace(b"2.0 2.0 7.5e-01", b"2.0 2.0"), "not `x y theta`"),
        (CALLE_TXT + b"0.5 0.5 0.0\n", "3 squares for n = 2"),
        (CALLE_TXT.replace(b"# s = 3.0", b"# s = 0.0"), "positive"),
        (b"\xff\xfe", "UTF-8"),
    ],
)
def test_the_calle_adapter_refuses_what_its_format_does_not_state(
    raw: bytes, message: str
) -> None:
    with pytest.raises(reports.ReportError, match=message):
        reports.parse_certificate(raw, 2, "calle-txt", PLACES)


@pytest.mark.parametrize(
    ("options", "message"),
    [
        ({}, "reads exactly"),
        ({**PLACES, reports.DILATION: "1"}, "reads exactly"),
        ({reports.HALF_ANGLE_PLACES: "29"}, "integer from 30"),
        ({reports.HALF_ANGLE_PLACES: "101"}, "integer from 30"),
        ({reports.HALF_ANGLE_PLACES: "040"}, "integer from 30"),
    ],
)
def test_the_calle_adapter_reads_exactly_its_one_declared_option(
    options: dict[str, str], message: str
) -> None:
    with pytest.raises(reports.ReportError, match=message):
        reports.parse_certificate(CALLE_TXT, 2, "calle-txt", options)


# --------------------------------------------------------------------------- #529


def test_the_calle_fact_is_the_printed_layout_with_forty_place_tangents() -> None:
    packet = reports.packet_path(CALLE)
    (certificate,) = reports.read_facts(packet).values()
    assert certificate.side == Fraction(Decimal("10.605828696455852"))
    for pose in certificate.poses:
        assert 10**40 % pose.t.denominator == 0
        for centre in (pose.x, pose.y):
            assert 0 < centre < certificate.side
            # An 18-digit decimal of the layout, as printed; no centre is below 1/2.
            assert 10**18 % centre.denominator == 0


def test_the_calle_side_is_below_t125_and_above_the_regularized_house() -> None:
    (row,) = _rows(CALLE).values()
    assert row["case"]["result"] == "T-146"
    assert row["case"]["relation"] == "above"
    assert Fraction(242, 10**13) < -_margin(row["case"]) < Fraction(243, 10**13)
    others = {other["result"]: other for other in row["pending"]}
    assert others["T-125"]["relation"] == "below"
    assert Fraction(547, 10**13) < _margin(others["T-125"]) < Fraction(548, 10**13)
    assert others["T-120"]["relation"] == "below"
    assert row["smallest"] == "case: ry-xu, regularized by Evan Daniel"


def test_the_calle_replay_clears_every_wall_and_pair_by_the_margins_the_issue_states() -> None:
    positives = reports.check_certification(reports.packet_path(CALLE))
    (margins,) = reports.margins(positives).values()
    wall = Fraction(margins["exact_verify_containment_clearance"])
    gap = Fraction(margins["exact_verify_best_pair_gap"])
    assert Fraction(2, 10**12) < wall < Fraction(201, 10**14)
    assert Fraction(193, 10**14) < gap < Fraction(194, 10**14)


# --------------------------------------------------------------------------- #528


def test_each_528_side_is_its_labelled_optimum_dilated_by_1e60_and_the_issue_print() -> None:
    packet = reports.packet_path(OSTASHEV_528)
    source = reports.REPO / reports.acquisition(packet)["archived_path"]
    certificates = reports.read_facts(packet)
    assert list(certificates) == list(ISSUE_528)
    for n, certificate in certificates.items():
        text = (source / f"records/n{n:04d}.sqcert").read_text(encoding="utf-8")
        (claimed,) = [
            line.split()[-1] for line in text.splitlines() if line.startswith("# claimed_s:")
        ]
        assert certificate.side == Fraction(claimed) * (1 + Fraction(1, 10**60))
        assert legacy.ceiling_decimal(certificate.side, 38) == ISSUE_528[n]


def test_the_528_certificates_are_smallest_at_every_count() -> None:
    rows = _rows(OSTASHEV_528)
    for row in rows.values():
        assert (row["smallest"], row["case"]["relation"]) == (reports.THIS, "below")
    expected = {175: ("T-140", 2946), 232: ("T-136", 3254), 264: ("T-101", 3439)}
    for n, (result, thousandths) in expected.items():
        case = rows[n]["case"]
        assert case["result"] == result
        assert Fraction(thousandths, 10**6) < _margin(case) < Fraction(thousandths + 1, 10**6)
    assert rows[264]["case"]["reported_relation"] == "below"
    couzo, ryxu = rows[175]["pending"]
    assert (couzo["report"], couzo["relation"]) == ("Couzo 337078c (think-9fjl)", "below")
    assert Fraction(2944, 10**6) < _margin(couzo) < Fraction(2945, 10**6)
    assert (ryxu["result"], ryxu["relation"]) == ("T-125", "below")
