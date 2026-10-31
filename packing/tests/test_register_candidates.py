"""The register candidates of 31 October 2026 (T-261 to T-263): custody, construction, receipts.

`devtools.register_candidates` retains the regularization run's solve certificates at 130
and 307, each pinned by the SHA-256 the 31 October review decided and held to the solved
side its run's retained report records, and the review's written 293, held pose for pose
to T-257's 260 certificate plus the 293 house's L strip. This holds each certificate to
what the register states, the construction to its count, the receipts to their
certificates, and refuses a certificate whose bytes are not the pinned file's.
"""

from __future__ import annotations

import json
from fractions import Fraction

import pytest

from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools import register_candidates as candidates

BATCH = candidates.RUU2
#: Each candidate's exact side, as T-261, T-262 and T-263 state it, and its house's.
SIDES = {
    130: (
        Fraction(1487803830747751967474793359227, 125 * 10**27),
        Fraction(5951215322991132879306459820277, 5 * 10**29),
    ),
    293: (
        Fraction(8816991251060941991251052624833, 5 * 10**29),
        Fraction(8816991251061390991251052573823, 5 * 10**29),
    ),
    307: (
        Fraction(4494812820921068365908930695861, 25 * 10**28),
        Fraction(
            2707897969116659515550794271467451840032974544063449693,
            150612387934832692306604131393579915999000000000000000,
        ),
    ),
}


def test_each_side_is_the_registered_side_below_its_house() -> None:
    rows = {row["n"]: row for row in candidates.table(BATCH)}
    for n, (side, house) in SIDES.items():
        assert candidates.side(BATCH, n) == side
        assert side < house
        assert rows[n]["side"] == f"{side.numerator}/{side.denominator}"
    # 130 rounds to its house's 12-place print; 293 and 307 cross theirs. All three are
    # held for the owner (RV-3 of the 31 October review).
    assert [rows[n]["same_print"] for n in (130, 293, 307)] == [True, False, False]


def test_the_l_strip_completes_the_count_in_either_placement() -> None:
    zero = Fraction(0)
    parent = legacy.Certificate(
        1, Fraction(3, 2), (legacy.Pose(Fraction(3, 4), Fraction(3, 4), zero),)
    )
    for placement in candidates.PLACEMENTS:
        built = candidates.l_strip(parent, 4, placement)
        assert built.side == Fraction(5, 2)
        assert len(built.poses) == 4
    with pytest.raises(candidates.CandidateError):
        candidates.l_strip(parent, 5, "17top+16")
    with pytest.raises(candidates.CandidateError):
        candidates.l_strip(parent, 4, "elsewhere")


def test_the_retained_293_is_its_parent_plus_the_houses_strip() -> None:
    assert candidates.certificate(BATCH, 293) == candidates.construction(BATCH, 293)


def test_a_certificate_that_is_not_the_pinned_file_is_refused() -> None:
    raw = candidates.certificate_path(BATCH, 307).read_bytes()
    forged = raw.replace(b"\n", b"\n\n", 1)
    with pytest.raises(candidates.CandidateError, match="not the file the review decided"):
        candidates.admitted(BATCH, 307, forged)


def test_each_receipt_holds_its_certificates_three_jobs() -> None:
    for n in SIDES:
        record = candidates.check_receipt(BATCH, n)
        assert [row["control"] for row in record["cases"]] == list(kernel.JOBS)


def test_each_sharp_control_receipt_met_its_expectations() -> None:
    for n, (side, _house) in SIDES.items():
        record = json.loads(candidates.controls_path(BATCH, n).read_text(encoding="utf-8"))
        assert record["n"] == n
        assert Fraction(record["side"]) == side
        assert record["all_as_expected"] is True
        assert {row["control"] for row in record["controls"]} == set(candidates.sharp.CONTROLS)
