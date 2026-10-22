"""Evan Daniel's regularized views of 20 October: the views lane of 21 October 2026.

Four certificates of the display-regularized record lists at ``0075967``, which no issue
reports, retained under the MIT licence as the upstream gzip files they are and read by
the `evand-cert` adapter: s(204), s(227), s(229) and s(260). The general importer's checks
run on the packet through ``test_upper_bound_reports``; these hold what is particular to
it, as the stage 4 review of 19 October asked of the imports before it (RV-1 of
docs/project/reviews/review-2026-10-19-upper-bound-imports-659-664-669-674.md): how each
side was made from the solved side its JSON prints, that each is below every report at its
count and below the verified bound at the next count, that the house reader rebuilds it,
what the identity measurement found at 227, that the 227 item names #672's entry since
its registration (review A2 of #716), and that both maintained routes meet the sharp
controls at 204 (RF-3 of the 21 October review). Every test reads the retained packet and
the records only; none needs the network.
"""

from __future__ import annotations

import gzip
import json
import math
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import check_source_coverage as coverage
from devtools import evand_arrangement_reports as kernel
from devtools import select_houses
from devtools import upper_bound_reports as reports

PACKET = "evand-regularized-2026-10-20"
KEY = "[Daniel regularized lists 2026-10-20]"
CERTS = "search/regularize/lists/certs"
SIDES = {
    204: Fraction(14808642840591493923068442871459, 10**30),
    227: Fraction(7781812826162574542396221861851, 5 * 10**29),
    229: Fraction(15650161513876431064009548865321, 10**30),
    260: Fraction(4161438312629953048686574163329, 25 * 10**28),
}
#: The finder each view's JSON names, which the register credits.
FINDERS = {
    204: "Francisco Couzo (franciscouzo)",
    227: "Francisco Couzo (franciscouzo)",
    229: "Evan Daniel (evand)",
    260: "Francisco Couzo (franciscouzo)",
}
#: #672's exact side at 227 (franciscouzo/square-packing@af8cb79, certificates/n227.cert),
#: which no packet retains; the identity measurement reads it from a fetched copy.
COUZO_672 = Fraction(71427829379429597600111901507, 4589408083628500000000000000)
NOTE = "regularized display view of a certified packing at the same side; not a new bound"


def _packet() -> Path:
    return reports.packet_path(PACKET)


def _json(n: int) -> dict[str, Any]:
    folder = reports.REPO / reports.acquisition(_packet())["archived_path"] / CERTS
    return json.loads(gzip.decompress((folder / f"n-{n:03d}.json.gz").read_bytes()))


def _ceil_at(value: Fraction, places: int) -> Fraction:
    return Fraction(math.ceil(value * 10**places), 10**places)


def test_each_certificate_states_its_side_and_the_house_reader_rebuilds_it() -> None:
    certificates = reports.read_facts(_packet())
    assert {n: certificate.side for n, certificate in certificates.items()} == SIDES
    for n, side in SIDES.items():
        assert reports.house_side(KEY, n) == side


def test_each_side_is_its_solved_side_scaled_by_1e20_and_rounded_up_at_30_places() -> None:
    for n, side in SIDES.items():
        document = _json(n)
        assert Fraction(document["S_cert"]) == side
        solved = Fraction(Decimal(document["S_exact"]))
        assert side == _ceil_at(solved * (1 + Fraction(1, 10**20)), 30)
        assert document["by"] == [FINDERS[n]]
        assert document["note"] == NOTE
        assert (document["policy"], document["level"]) == ("conservative", 2)
        assert all(change[0] == "free-angle kept" for change in document["angle_changes"])


def test_each_certificate_is_below_its_case_and_every_report_it_names() -> None:
    rows = reports.check_claims(_packet())["results"]
    assert [row["n"] for row in rows] == list(SIDES)
    for row in rows:
        assert row["smallest"] == reports.THIS
        assert row["case"]["relation"] == "below"
        assert row["pending"]
        assert all(report["relation"] == "below" for report in row["pending"])
    (row229,) = (row for row in rows if row["n"] == 229)
    margin = Fraction(row229["case"]["difference"])
    assert Fraction(19122097, 10**18) < margin < Fraction(19122098, 10**18)


def test_each_side_is_below_the_verified_bound_at_the_next_count() -> None:
    for n, side in SIDES.items():
        case = coverage.parse_case(reports.ROOT / f"frontier/n-{n + 1:03d}.md")
        bound = Fraction(str(case["verified_upper_bound"]["exact_form"]))
        assert side < bound


def test_the_227_view_is_measured_as_672s_packing_solved_lower() -> None:
    record = json.loads((_packet() / "measure/identity.json").read_text("utf-8"))
    assert Fraction(record["couzo_672"]["side"]) == COUZO_672
    pairs = {(pair["n"], pair["view"], pair["against"]): pair for pair in record["pairs"]}
    view = pairs[227, "evand 0075967", "#672"]
    assert Fraction(view["side_difference_exact"]) == SIDES[227] - COUZO_672
    assert SIDES[227] < COUZO_672 < SIDES[227] + Fraction(18, 10**12)
    assert view["nearest_centre"]["one_to_one"]
    assert view["assignment"]["moved_beyond"]["1e-6"] == 33
    against_668 = pairs[227, "evand 0075967", "T-196 (#668)"]
    assert against_668["assignment"]["moved_beyond"]["1e-6"] == 226
    # #672's packing moves no square beyond a tenth from de Winter's: it refines it.
    refines = pairs[227, "#672", "T-196 (#668)"]
    assert refines["assignment"]["moved_beyond"]["1e-1"] == 0


@pytest.mark.slow
@pytest.mark.parametrize("where", ["at-contact", "past-contact"])
@pytest.mark.parametrize("control", kernel.SHARP_CONTROLS)
def test_both_routes_meet_contact_and_refuse_1e30_past_it_at_204(
    control: str, where: str
) -> None:
    """RF-3 of the 21 October review: the receipt's two controls are gross (a duplicated
    square, gap -1, and a square moved outside), while every margin these certificates keep
    is about 1e-20, so a route rounding at binary64 or tolerating 1e-12 would pass the
    packet as retained. The kernel's two sharp controls on the 204 certificate: the side
    lowered by its least far-wall clearance, or its tightest pair closed along its best
    separating axis, is accepted by both maintained routes at exact contact with the margin
    exactly 0, and refused by both 1e-30 past it at exactly -1e-30, as the review's
    controls found at all four counts (review/review-2026-10-21/outputs/out-controls-n*.json).
    Each case runs both routes over 20,706 pairs, about 3 s a route, above the quick lane's
    per-test ceiling, so it runs in the deep surface."""
    certificate = reports.read_facts(_packet())[204]
    margin = "wall" if control == "side-lowered-past-wall-contact" else "gap"
    past = where == "past-contact"
    verdicts = kernel.run_sharp(certificate, control, past=past)
    for route in kernel.ROUTES:
        assert verdicts[route]["passed"] is not past, route
        assert verdicts[route][margin] == (-kernel.SHARP_EPSILON if past else 0), route


#: Francisco Couzo's #672 at 227 and 229, registered on 22 October 2026 (think-2vjc).
COUZO_672_ENTRY = "T-227"


def test_the_227_item_names_672s_entry_and_its_credit_reaches_couzo() -> None:
    """Review A2 of #716 and RF-1 of the 21 October review: the view at 227 is #672's
    packing (194 of 227 squares within 1e-6 of #672's), which refines de Winter's (T-196)
    and was unregistered when T-225 was registered, so the item named T-196 and the
    adoption at 227 waited. #672's entry now registers it, the item names that entry with
    the identity measured against it, and nothing holds 227: the house rule adopts T-225
    there with the packing credited to #672's entry, whose own item names de Winter's."""
    results = {entry["id"]: entry for entry in select_houses.load_results()}
    entry = results["T-225"]
    assert select_houses.regularized(entry, 227) == COUZO_672_ENTRY
    (item,) = (item for item in entry["regularizations"] if item["n"] == 227)
    record = json.loads((_packet() / "measure/identity.json").read_text("utf-8"))
    pairs = {(pair["n"], pair["view"], pair["against"]): pair for pair in record["pairs"]}
    measured = pairs[227, "evand 0075967", "#672"]["assignment"]
    assert item["identity"]["one_to_one"]
    assert item["identity"]["moved"] == measured["moved_beyond"]["1e-3"] == 16
    assert item["identity"]["max_move"] == round(float(measured["largest_move"]), 3)
    assert item["identity"]["max_turn_deg"] == float(measured["largest_turn_degrees"])
    couzo = results[COUZO_672_ENTRY]
    assert couzo["attribution"]["source_keys"] == ["[Couzo issue 672 2026-10-17]"]
    assert select_houses.regularized(couzo, 227) == "T-196"
    assert 227 not in select_houses.CORRECTIONS_OWED
    assert 227 not in select_houses.PENDING_ADOPTION
