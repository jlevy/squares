"""The upper-bound import of the intake pass's lane L160 of 14 November 2026 (think-14i2).

One packet, read by the ``witness-corners`` adapter: Doğa Özden's #983 at 228
(kenaznia-doga/s228-upper-bound 8bebf3f), below T-174, Francisco Couzo's packing as PingYou
Ltd improved it, the house at 228 since 17 October. The witness was promoted to exact
rationals by this repository's ``packing-witness promote --strategy robust-rational`` from a
decimal pose the source retains, and the issue prints its side rounded up at 12 places. The
general importer's checks run on the packet through ``test_upper_bound_reports``; these hold
what is particular to it: the digests the issue and README print, the print against the
exact side, the house it is compared with and the improvement the issue states, the
side-only leaderboard entry it discloses, the ledger's verdict, the retained sharp controls,
the identity measurement, the contraction margins and the L-step scan the register's notes
cite. Every test reads the packet and the ledger only; none needs the network.
"""

from __future__ import annotations

import json
import math
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-983-20261114"
NAME = "ozden-s228-upper-bound-2026-11-14"
ISSUE = 983
N = 228
#: The house the certificate is compared with (T-174, Francisco Couzo's packing as PingYou
#: Ltd improved it), the issue's 12-place print, the side rounded up at 16 places as the
#: claim record prints it, and the improvement the issue states, 0.00379974091792048.
HOUSE = "[PingYou PR 574 certificates 2026-10-13]"
RESULT = "T-174"
PRINTED = "15.600801734812"
CEILING = "15.6008017348117539"
GAIN = "3.79974091792048e-03"
#: The 15-place side sqcheck-228.txt prints and the 43 places the issue and README print
#: before an ellipsis, each the exact side rounded up.
PRINTED_15 = "15.600801734811754"
PRINTED_43 = "15.6008017348117538028514559173910014808630264"
#: The SHA-256 digests the issue and README print: the candidate YAML's, and the hit file's
#: independently harvested copy, which the README says is byte-identical to the filed one.
PRINTED_DIGESTS = (
    "4dc2075f5fb06bb7a1ca68aabd8eebd0d326c16c5f408151876a165d2246b747",
    "18dad468007e8fb8058104772dcfc5887c48bf0baa2789c5bcbee03f1cf2bfe5",
)
#: The side-only Kaggle leaderboard entry the issue discloses first, unpublished, and how
#: far below the certificate's side it lies, as the issue states; and the best public
#: Kaggle packing it quotes, above the side.
LEADERBOARD = "15.596043116646"
LEADERBOARD_BELOW = "4.758618166e-03"
KAGGLE_PACKING = "15.604601475744"


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _manifest() -> dict[str, str]:
    text = (reports.packet_path(NAME) / "acquisition/upstream-subtree.sha256").read_text(
        "utf-8"
    )
    return {
        path.removeprefix("./"): digest
        for digest, path in (line.split(maxsplit=1) for line in text.splitlines())
    }


def _up(side: Fraction, places: int) -> Fraction:
    return Fraction(math.ceil(side * 10**places), 10**places)


def _side() -> Fraction:
    return reports.read_facts(reports.packet_path(NAME))[N].side


def test_the_packet_holds_the_files_whose_digests_the_issue_prints() -> None:
    manifest = _manifest()
    candidate, hit = PRINTED_DIGESTS
    assert manifest[f"n-{N}-candidate.yaml"] == candidate
    assert manifest[f"hit-n{N}-114-0.txt"] == hit
    # The decimal pose the witness's source.path names, the JSON copy and the four check
    # reports are retained beside it.
    for path in (
        f"n-{N}-decimal-pose.yaml",
        f"n{N}-witness.json",
        "checks/exact.json",
        "checks/interval.json",
        "checks/promote.json",
        "checks/registry.json",
    ):
        assert path in manifest


def test_the_print_is_its_exact_side_rounded_up_and_its_reader_rebuilds_it() -> None:
    """The issue's 12-place print, sqcheck's 15-place print and the 43 places the issue
    prints before an ellipsis are the side rounded up, and the JSON states the same packing
    as the YAML (the declaration's ``same_packing``, which ``read_facts`` holds)."""
    declaration = reports.load_declaration(reports.packet_path(NAME))
    assert declaration["source_key"] == f"[Özden s{N} upper bound {NAME[-10:]}]"
    assert declaration["issue"].endswith(f"/issues/{ISSUE}")
    assert (declaration["requested"], declaration["replayed"]) == ([N], [N])
    (row,) = declaration["certificates"]
    assert (row["n"], row["format"], row["offered"]) == (N, "witness-corners", PRINTED)
    assert [other["path"] for other in row.get("same_packing", [])] == [f"n{N}-witness.json"]
    side = _side()
    assert _up(side, 12) == Fraction(Decimal(PRINTED))
    assert _up(side, 15) == Fraction(Decimal(PRINTED_15))
    assert _up(side, 16) == Fraction(Decimal(CEILING))
    assert _up(side, 43) == Fraction(Decimal(PRINTED_43))
    assert reports.house_side(declaration["source_key"], N) == side


def test_the_certificate_is_below_the_house_by_the_improvement_stated() -> None:
    side = _side()
    difference = reports.house_side(HOUSE, N) - side
    assert difference > 0
    assert f"{float(difference):.14e}" == GAIN
    (row,) = reports.check_claims(reports.packet_path(NAME))["results"]
    assert (row["n"], row["smallest"], row["case"]["relation"]) == (N, reports.THIS, "below")
    assert (row["case"]["source_key"], row["case"]["result"]) == (HOUSE, RESULT)
    assert Fraction(row["case"]["difference"]) == difference
    assert row["pending"] == []
    # The leaderboard's side-only entry is below the side, as the issue says first: it
    # states no packing, so it is context only. The public Kaggle packing is above it.
    below = side - Fraction(Decimal(LEADERBOARD))
    assert f"{float(below):.9e}" == LEADERBOARD_BELOW
    assert Fraction(Decimal(KAGGLE_PACKING)) > side


def test_the_ledger_records_the_claim_as_a_new_packing() -> None:
    ledger = _json(LEDGER / "ledger.json")
    recorded: dict[int, list[str]] = {}
    for count in ledger["counts"]:
        for claim in count["steps"]:
            if claim["verdict"] == "recorded":
                recorded.setdefault(count["n"], []).append(claim["report"])
    assert recorded == {N: [f"#{ISSUE}"]}


def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it() -> None:
    record = _json(reports.packet_path(NAME) / "receipts/sharp-controls.json")
    assert (record["n"], record["packet"], record["all_as_expected"]) == (N, NAME, True)
    assert record["epsilon"] == str(kernel.SHARP_EPSILON)
    assert {row["control"] for row in record["controls"]} == set(sharp.CONTROLS)
    assert len(record["controls"]) == 11
    for row in record["controls"]:
        assert row["as_expected"] is True
        assert set(row["routes"]) == set(kernel.ROUTES)
    # The least-gap pair is squares 118 and 119, 2.02e-13 apart, and square 63 touches its
    # wall, so its enlargement to the wall grows it by 0 and is accepted at contact.
    pair = next(
        row
        for row in record["controls"]
        if row["control"] == sharp.TIGHTEST_PAIR and row["where"] == "at-contact"
    )
    assert (pair["detail"]["square"], pair["detail"]["partner"]) == (119, 118)
    assert Fraction(pair["detail"]["moved_by"]) == Fraction(101, 500000000000000)
    wall = next(
        row
        for row in record["controls"]
        if row["control"] == sharp.ENLARGED_WALL and row["where"] == "at-contact"
    )
    assert (wall["detail"]["square"], wall["detail"]["wall_clearance"]) == (63, "0")
    assert wall["expected"] == "accepted"


def test_the_identity_measurement_the_notes_cite() -> None:
    """Measured against T-174's packet, the regularized view and the house witness: no
    symmetry pairs any of them one to one with this packing, the optimal assignment moves 75
    squares beyond a tenth (largest 0.940075), 59 squares turn by more than a degree aligned
    by box centres, and 48 squares are tilted beyond a degree here, all one way, against
    T-174's 51 (45 and 6)."""
    record = _json(reports.packet_path(NAME) / "measure/identity.json")
    assert record["n"] == N
    pair = record["pairs"][0]
    assert (pair["view"], pair["against"]) == ("OZDEN", RESULT)
    assert pair["nearest_centre"]["one_to_one"] is False
    assert pair["assignment"]["moved_beyond"]["1e-3"] == N
    assert pair["assignment"]["moved_beyond"]["1e-1"] == 75
    assert pair["assignment"]["largest_move"] == "0.940075"
    assert pair["centred"]["turned_beyond_1_degree"] == 59
    tilts = record["tilts"]
    assert (
        tilts["OZDEN"]["tilted_beyond_1_degree"],
        tilts[RESULT]["tilted_beyond_1_degree"],
    ) == (
        48,
        51,
    )
    assert (tilts["OZDEN"]["tilted_positive"], tilts["OZDEN"]["tilted_negative"]) == (48, 0)
    assert (tilts[RESULT]["tilted_positive"], tilts[RESULT]["tilted_negative"]) == (45, 6)
    # Two near-upright squares turn by more than half a degree, so 50 are tilted beyond half
    # a degree, as the issue counts.
    half = [a for a in tilts["OZDEN"]["near_upright_beyond_1e-3_degrees"] if abs(a) > 0.5]
    assert tilts["OZDEN"]["tilted_beyond_1_degree"] + len(half) == 50
    for against in ("regularized", "house-witness"):
        other = next(row for row in record["pairs"] if row["against"] == against)
        assert other["nearest_centre"]["one_to_one"] is False
        assert other["assignment"]["moved_beyond"] == pair["assignment"]["moved_beyond"]


def test_the_gain_lies_wholly_outside_the_house_certificate_s_contraction_margin() -> None:
    """RV-3 (think-ruu2) asks about gains inside a predecessor's padding margin. T-174's
    certificate at 228 has none, a pair touching, so the entry is not held for it. This
    certificate's own margin is about 2.95e-12, and the side it would contract to is not a
    bound anyone reported."""
    gain = reports.house_side(HOUSE, N) - _side()
    record = _json(reports.packet_path(NAME) / f"measure/contraction-n{N}.json")
    assert (record["n"], record["certificate"]["label"]) == (N, RESULT)
    assert record["routes_accept"] is True
    assert Fraction(record["margin"]) == 0
    assert record["binding_pair"] == [201, 227]
    assert record["against"]["within_margin"] is False
    assert Fraction(record["against"]["gain"]) == gain
    own = _json(reports.packet_path(NAME) / f"measure/contraction-n{N}-own.json")
    assert own["routes_accept"] is True
    assert own["binding_pair"] == [118, 119]
    assert 1 - Fraction(own["lambda_star"]) == Fraction(101, 500000000000101)
    assert 0 < Fraction(own["margin"]) < Fraction(1, 10**11)
    assert gain > 10**9 * Fraction(own["margin"])


def test_the_l_step_scan_stands_the_side_in_and_carries_it_nowhere() -> None:
    record = _json(reports.packet_path(NAME) / "measure/l-step-scan.json")
    assert Fraction(record["with"][str(N)]) == _side()
    improved = {row["n"] for row in record["l_step"]["improves"]}
    assert all(row["from"] != N for row in record["l_step"]["improves"])
    assert N not in improved
    assert record["monotonicity"]["improves"] == []
