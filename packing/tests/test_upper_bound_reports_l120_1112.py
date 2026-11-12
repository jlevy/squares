"""The upper-bound import of the intake pass's lane L120 of 12 November 2026 (think-s418).

One packet, read by the ``witness-corners`` adapter: Doğa Özden's #962 at 269
(kenaznia-doga/s269-upper-bound-16899469076 fdab2c0), which the author says improves his own
#947 (T-290, the house at 269 since 11 November). The witness was promoted to exact
rationals by this repository's ``packing-witness promote --strategy robust-rational`` from a
decimal pose the source retains, and the issue prints its side rounded up at 12 places. The
general importer's checks run on the packet through ``test_upper_bound_reports``; these hold
what is particular to it: the digests the issue and README print, the print against the
exact side, the house it is compared with and the improvement the issue states, the ledger's
verdict, the retained sharp controls, the identity measurement, the contraction margins and
the L-step scan the register's notes cite. Every test reads the packet and the ledger only;
none needs the network.
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

LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-962-20261112"
NAME = "ozden-s269-issue962-2026-11-11"
ISSUE = 962
N = 269
#: The house the certificate is compared with (the author's own #947), its register entry,
#: the issue's 12-place print, the side rounded up at 16 places as the claim record prints
#: it, and the improvement the issue states.
HOUSE = "[Özden s269 upper bound 2026-11-11]"
RESULT = "T-290"
PRINTED = "16.899469075856"
CEILING = "16.8994690758550466"
GAIN = "1.526e-03"
#: The 16-place side the issue and README print, the exact side truncated, below it.
PRINTED_16 = "16.8994690758550465"
#: T-174, the house before T-290, and how far below it the certificate lies.
EARLIER = "[PingYou PR 574 certificates 2026-10-13]"
EARLIER_GAIN = "2.045e-03"
#: The SHA-256 digests the issue (the witness) and the README (both files) print: the
#: candidate YAML's, then its JSON copy's.
PRINTED_DIGESTS = (
    "54b408b2f1b45fc3d0a1330767c8740f0889eecb73f5fcf7888710526dbcc26b",
    "4b7ac2a7402037b047c04e239d239042228ae6c68f09cb917e09fa128f5b9cc0",
)


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
    candidate, copy = PRINTED_DIGESTS
    assert manifest[f"n-{N}-candidate.yaml"] == candidate
    assert manifest[f"n{N}-witness.json"] == copy
    # The decimal pose the witness's source.path names is retained beside it.
    assert f"n-{N}-decimal-pose.yaml" in manifest


def test_the_print_is_its_exact_side_rounded_up_and_its_reader_rebuilds_it() -> None:
    """The issue's 12-place print is the side rounded up, and the JSON states the same
    packing as the YAML (the declaration's ``same_packing``, which ``read_facts`` holds).
    The 16-place side the issue and README also print is the side truncated, below it."""
    declaration = reports.load_declaration(reports.packet_path(NAME))
    assert declaration["source_key"] == f"[Özden s{N} issue {ISSUE} {NAME[-10:]}]"
    assert declaration["issue"].endswith(f"/issues/{ISSUE}")
    assert (declaration["requested"], declaration["replayed"]) == ([N], [N])
    (row,) = declaration["certificates"]
    assert (row["n"], row["format"], row["offered"]) == (N, "witness-corners", PRINTED)
    assert [other["path"] for other in row.get("same_packing", [])] == [f"n{N}-witness.json"]
    side = _side()
    assert _up(side, 12) == Fraction(Decimal(PRINTED))
    assert _up(side, 16) == Fraction(Decimal(CEILING))
    assert (
        Fraction(Decimal(PRINTED_16))
        < side
        < Fraction(Decimal(PRINTED_16)) + Fraction(1, 10**16)
    )
    assert reports.house_side(declaration["source_key"], N) == side


def test_the_certificate_is_below_both_houses_by_the_improvements_stated() -> None:
    side = _side()
    difference = reports.house_side(HOUSE, N) - side
    assert difference > 0
    assert f"{float(difference):.3e}" == GAIN
    earlier = reports.house_side(EARLIER, N) - side
    assert f"{float(earlier):.3e}" == EARLIER_GAIN
    (row,) = reports.check_claims(reports.packet_path(NAME))["results"]
    assert (row["n"], row["smallest"], row["case"]["relation"]) == (N, reports.THIS, "below")
    assert (row["case"]["source_key"], row["case"]["result"]) == (HOUSE, RESULT)
    assert Fraction(row["case"]["difference"]) == difference
    assert row["pending"] == []


def test_the_ledger_records_the_claim() -> None:
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


def test_the_identity_measurement_the_notes_cite() -> None:
    """Measured against T-290's packet first, then T-174's, the regularized view and the
    house witness: no symmetry pairs any of them one to one with this packing, the optimal
    assignment moves 115 squares beyond a tenth from T-290's, 116 squares turn by more than a
    degree aligned by box centres, and 45 squares are tilted beyond a degree here against
    T-290's 100 and T-174's 49."""
    record = _json(reports.packet_path(NAME) / "measure/identity.json")
    assert record["n"] == N
    pair = record["pairs"][0]
    assert (pair["view"], pair["against"]) == ("OZDEN", RESULT)
    assert pair["nearest_centre"]["one_to_one"] is False
    assert pair["assignment"]["moved_beyond"]["1e-1"] == 115
    assert pair["centred"]["turned_beyond_1_degree"] == 116
    tilts = record["tilts"]
    assert (
        tilts["OZDEN"]["tilted_beyond_1_degree"],
        tilts[RESULT]["tilted_beyond_1_degree"],
        tilts["T-174"]["tilted_beyond_1_degree"],
    ) == (45, 100, 49)
    for against in ("T-174", "regularized", "house-witness"):
        other = next(row for row in record["pairs"] if row["against"] == against)
        assert other["nearest_centre"]["one_to_one"] is False
    witness = next(row for row in record["pairs"] if row["against"] == "house-witness")
    assert witness["assignment"]["moved_beyond"] == pair["assignment"]["moved_beyond"]


def test_the_gain_is_far_above_the_house_certificate_s_contraction_margin() -> None:
    """RV-3 (think-ruu2) asks about gains inside a predecessor's padding margin. T-290's
    certificate at 269 has 3.24e-12 of padding, so the gain is about 4.7e8 times it and the
    entry is not held for it. This certificate's own margin is about the same size, and the
    side it would contract to is not a bound anyone reported."""
    gain = reports.house_side(HOUSE, N) - _side()
    record = _json(reports.packet_path(NAME) / f"measure/contraction-n{N}.json")
    assert (record["n"], record["certificate"]["label"]) == (N, RESULT)
    assert record["routes_accept"] is True
    assert 0 < Fraction(record["margin"]) < Fraction(1, 10**11)
    assert record["against"]["within_margin"] is False
    assert Fraction(record["against"]["gain"]) == gain
    assert gain > 10**8 * Fraction(record["margin"])
    own = _json(reports.packet_path(NAME) / f"measure/contraction-n{N}-own.json")
    assert own["routes_accept"] is True
    assert 0 < Fraction(own["margin"]) < Fraction(1, 10**11)
    assert gain > 10**8 * Fraction(own["margin"])


def test_the_l_step_scan_stands_the_side_in_and_carries_it_nowhere() -> None:
    record = _json(reports.packet_path(NAME) / "measure/l-step-scan.json")
    assert Fraction(record["with"][str(N)]) == _side()
    improved = {row["n"] for row in record["l_step"]["improves"]}
    assert all(row["from"] != N for row in record["l_step"]["improves"])
    assert N not in improved
    assert record["monotonicity"]["improves"] == []
