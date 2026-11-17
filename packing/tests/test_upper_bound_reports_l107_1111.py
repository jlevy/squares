"""The upper-bound import of the intake pass's lane L107 of 11 November 2026 (think-89i7).

One packet, read by the ``witness-corners`` adapter: Doğa Özden's #959 at 179
(kenaznia-doga/s179-upper-bound-13880960371 6ab3cfe), which the author says supersedes his
#954 (T-291, the house at 179 since that day). The witness was promoted to exact rationals
by this repository's ``packing-witness promote --strategy robust-rational`` from a decimal
pose the source retains, and the issue prints its side rounded up at 12 places. The
general importer's checks run on the packet through ``test_upper_bound_reports``; these
hold what is particular to it: the digests the issue and README print, the print against
the exact side, the house it is compared with and the improvement the issue states, the
ledger's verdict, the retained sharp controls, the identity measurement, the core and band
measurement against the registry's 70 and the side's relation to s(70) + 5, the
contraction margins and the L-step scan the register's notes cite. Every test reads the
packet and the ledger only; none needs the network.
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

LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-959-20261111"
NAME = "ozden-s179-issue959-2026-11-11"
ISSUE = 959
N = 179
#: The house the certificate is compared with (the author's own #954), its register entry,
#: the issue's 12-place print, the side rounded up at 16 places as the claim record prints
#: it, and the improvement over the house the claim record gives.
HOUSE = "[Özden s179 upper bound 2026-11-11]"
RESULT = "T-291"
PRINTED = "13.880960371559"
CEILING = "13.8809603715582251"
GAIN = "4.068e-04"
#: T-174, the house before T-291, and the improvement the issue states over it.
EARLIER = "[PingYou PR 574 certificates 2026-10-13]"
EARLIER_GAIN = "2.835e-03"
#: The SHA-256 digests the issue (the witness) and the README (both files) print: the
#: candidate YAML's, then its JSON copy's.
PRINTED_DIGESTS = (
    "77ee3dd21e35ca6abd1410ad3a7ff25b44c5bbc0fe5ebd1031ae112126bf61fc",
    "4b2509fefd303ce1379084c0a7dc67b29233a9c6f415ee0fc9773c030559ae1a",
)
#: s(70) as the registry's 70 case states it, to the 18 places its value prints; the
#: isolating interval it gives agrees to 5e-19, far below what is measured here.
S70 = Fraction(Decimal("8.880960371555579595"))


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
    packing as the YAML (the declaration's ``same_packing``, which ``read_facts`` holds)."""
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
    assert reports.house_side(declaration["source_key"], N) == side


def test_the_certificate_is_below_both_houses_by_the_improvements_stated() -> None:
    side = _side()
    difference = reports.house_side(HOUSE, N) - side
    assert difference > 0
    assert f"{float(difference):.3e}" == GAIN
    assert f"{float(reports.house_side(EARLIER, N) - side):.3e}" == EARLIER_GAIN
    (row,) = reports.check_claims(reports.packet_path(NAME))["results"]
    assert (row["n"], row["smallest"], row["case"]["relation"]) == (N, reports.THIS, "below")
    assert (row["case"]["source_key"], row["case"]["result"]) == (HOUSE, RESULT)
    assert Fraction(row["case"]["difference"]) == difference


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
    """Against T-291 first: nearest centres pair the two one to one under the identity, and
    the assignment moves 3 squares beyond a tenth, a further arrangement of the author's own
    packing. Against T-174 no symmetry pairs them, and the house witness measures as
    T-291's packet does."""
    record = _json(reports.packet_path(NAME) / "measure/identity.json")
    assert record["n"] == N
    pair, earlier = record["pairs"][:2]
    assert (pair["view"], pair["against"], earlier["against"]) == ("OZDEN-959", RESULT, "T-174")
    assert pair["nearest_centre"]["one_to_one"] is True
    assert pair["nearest_centre"]["symmetry"] == 0
    assert pair["assignment"]["moved_beyond"]["1e-1"] == 3
    assert pair["centred"]["turned_beyond_1_degree"] == 5
    assert earlier["nearest_centre"]["one_to_one"] is False
    assert earlier["assignment"]["moved_beyond"]["1e-1"] == 46
    tilts = record["tilts"]
    assert (
        tilts["OZDEN-959"]["tilted_beyond_1_degree"],
        tilts[RESULT]["tilted_beyond_1_degree"],
    ) == (35, 36)
    witness = next(other for other in record["pairs"] if other["against"] == "house-witness")
    assert witness["assignment"]["moved_beyond"] == pair["assignment"]["moved_beyond"]


def test_the_side_is_s70_plus_5_but_for_its_padding_and_no_core_with_a_border() -> None:
    """The side lies 2.645e-12 above s(70) + 5, a border five wide round the 70 holds 175
    squares there, no corner placement of the 70 keeps all of it, and the 70 laid at both
    ends of the diagonal lies within 1e-9 of 15 of the 35 tilted squares, under the identity
    of its box and no other symmetry."""
    record = _json(reports.packet_path(NAME) / "measure/core-n070.json")
    assert (record["n"], record["m"]) == (N, 70)
    excess = _side() - S70 - 5
    assert Fraction(1, 10**12) < excess < Fraction(3, 10**12)
    five = record["side"]["plus"][5]
    assert (five["plus"], five["l_border_count"]) == (5, 175)
    assert abs(float(five["excess"]) - float(excess)) < 1e-15
    assert record["core"]["best"]["1e-9"] == 48
    assert max(row["matched"]["1e-1"] for row in record["core"]["placements"]) < 70
    band = record["band"]
    assert (band["view_squares"], band["core_squares"], band["best_symmetry"]) == (
        35,
        20,
        "identity",
    )
    assert band["by_shift"]["0"]["1e-9"] + band["by_shift"]["5"]["1e-9"] == 15
    others = [row for row in band["symmetries"] if row["symmetry"] != "identity"]
    assert all(row["matched"]["1e-2"] == 0 for row in others)


def test_the_gain_is_far_above_the_house_certificate_s_contraction_margin() -> None:
    """RV-3 (think-ruu2) asks about gains inside a predecessor's padding margin. T-291's
    certificate at 179 contracts by 2.6e-12, and the gain is 1.6e8 times that, so no part
    of it is padding and the entry is not held for it. Contracted to first contact, this
    certificate's own side lands within 1e-13 of s(70) + 5."""
    record = _json(reports.packet_path(NAME) / f"measure/contraction-n{N}.json")
    assert (record["n"], record["certificate"]["packet"]) == (
        N,
        "ozden-s179-upper-bound-2026-11-11",
    )
    assert record["routes_accept"] is True
    assert record["against"]["within_margin"] is False
    gain = reports.house_side(HOUSE, N) - _side()
    assert Fraction(record["against"]["gain"]) == gain
    assert gain > 10**8 * Fraction(record["margin"])
    own = _json(reports.packet_path(NAME) / f"measure/contraction-n{N}-own.json")
    assert own["routes_accept"] is True
    contracted = Fraction(own["contracted_side"])
    assert 0 < contracted - S70 - 5 < Fraction(1, 10**13)


def test_the_l_step_scan_stands_the_side_in_and_carries_it_nowhere() -> None:
    record = _json(reports.packet_path(NAME) / "measure/l-step-scan.json")
    assert Fraction(record["with"][str(N)]) == _side()
    improved = {row["n"] for row in record["l_step"]["improves"]}
    assert all(row["from"] != N for row in record["l_step"]["improves"])
    assert N not in improved
    assert record["monotonicity"]["improves"] == []
