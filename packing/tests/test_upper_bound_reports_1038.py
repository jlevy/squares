"""The upper-bound import of the intake pass's lane i1038 of 20 November 2026.

Bead think-91fu. One packet: Doğa Özden's centre-basis Witness/v2 at 228 (#1038,
``witness-center-basis``), his lab's exact conversion of jazivxt's public Kaggle packing
under one uniform clearance factor. The general importer's checks run on the packet through
``test_upper_bound_reports``; these hold what is particular to it: the digest the source
lists, the print against the exact side, the house it is compared with and the gain, the
ledger's verdict, the retained control plan and sharp controls, the identity measurement,
the option D comparison with T-301 shrunk to first contact, the held solve's side, and the
L-step scan the register's notes cite. Every test reads the packet and the ledger only; none
needs the network.
"""

from __future__ import annotations

import hashlib
import json
from decimal import ROUND_CEILING, Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import build_bound_citations as citations
from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

NAME = "ozden-s228-upper-bound-2026-11-18"
LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-1038-20261120"
#: The SHA-256 #1038 and the source's README state for the certificate.
LISTED = "1b816e2e9302ad58ca2d5bb5882f4f98b2c8fb4f9e5746a8ed3f823cfd4a3387"
#: The control plan's SHA-256, recorded on think-91fu before any control ran.
PLAN = "a8b9a8c6014168a4d750b1e1e9d98899d5abfc7e11877ec7436a2c194a8d61e1"
#: The side of the project's held solve at 228: the solved view of Evan Daniel's driver
#: on T-301's witness, 15 November 2026 (cases/regularized_drawings/think-17ex-2026-11-15,
#: its evand report at 228), accepted by both routes, held at row 3 and not retained.
HELD = Fraction(3899010779157917479945828568311, 250000000000000000000000000000)


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _packet() -> Path:
    return reports.packet_path(NAME)


def _side() -> Fraction:
    return reports.read_facts(_packet(), {228})[228].side


def test_the_packet_holds_the_certificate_whose_digest_the_source_lists() -> None:
    text = (_packet() / "acquisition/upstream-subtree.sha256").read_text("utf-8")
    manifest = {
        path.removeprefix("./"): digest
        for digest, path in (line.split(maxsplit=1) for line in text.splitlines())
    }
    assert manifest["n-228-candidate.yaml"] == LISTED


def test_the_print_is_the_exact_side_rounded_up_and_the_side_terminates() -> None:
    declaration = reports.load_declaration(_packet())
    assert declaration["issue"].endswith("/issues/1038")
    assert declaration["requested"] == declaration["replayed"] == [228]
    assert declaration["certificates"][0]["offered"] == "15.596043116632"
    side = _side()
    assert side == Fraction(389901077915794162667528670804703057, 25 * 10**33)
    with localcontext() as context:
        context.prec = 60
        exact = Decimal(side.numerator) / Decimal(side.denominator)
    assert str(exact) == "15.59604311663176650670114683218812228"
    assert str(exact.quantize(Decimal("1e-12"), rounding=ROUND_CEILING)) == "15.596043116632"


def test_the_certificate_is_below_t301_by_the_gain() -> None:
    row = reports.check_claims(_packet())["results"][0]
    case = row["case"]
    assert (row["smallest"], case["relation"], case["result"]) == (
        reports.THIS,
        "below",
        "T-301",
    )
    assert row["pending"] == []
    assert f"{float(Fraction(case['difference'])):.4e}" == "4.2890e-09"


def test_the_record_keeps_geometry_and_finder_credit_distinct() -> None:
    """The source reports geometric similarity. The record credits the certificate author."""
    ledger = _json(LEDGER / "ledger.json")
    walked = {
        count["n"]: [(step["report"], step["verdict"]) for step in count["steps"]]
        for count in ledger["counts"]
    }
    assert walked == {228: [("#1038", "recorded")]}
    assert "packing" not in ledger["counts"][0]["steps"][0]

    lane = citations.load_case(228)["reported_upper_bound"]
    assert lane["found_by"] == lane["improved_by"] == []
    row = next(entry for entry in citations.load_record()["entries"] if entry["n"] == 228)
    assert row["upper"]["text"] == "Ozden 2026, GitHub"
    assert row["upper"]["confirmed_by"] == ["T-334"]


def test_the_control_plan_is_the_one_hashed_on_the_bead() -> None:
    plan = (_packet() / "receipts/controls-plan-1038.md").read_bytes()
    assert hashlib.sha256(plan).hexdigest() == PLAN


def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it() -> None:
    """Square 1 touches the bottom wall and the box is the packing's extent, so the side is
    lowered by 0, the near-wall move is 0 and the touching square grows by 0: accepted at
    contact and refused past it for the wall and its shape, the plan's branch W0. The
    least pair gap, about 3.63e-23 at squares 156 and 166, exceeds the step (branch G), so
    the enlarged pair square is refused at contact for its shape alone."""
    record = _json(sharp.receipt_path(_packet(), [228], 228))
    assert (record["n"], record["packet"], record["all_as_expected"]) == (228, NAME, True)
    assert record["epsilon"] == str(kernel.SHARP_EPSILON)
    assert {row["control"] for row in record["controls"]} == set(sharp.CONTROLS)
    assert len(record["controls"]) == 11
    for row in record["controls"]:
        assert row["as_expected"] is True
        verdicts = {
            route: (
                outcome["passed"],
                tuple(outcome["failures"]),
                outcome["wall"],
                outcome["gap"],
            )
            for route, outcome in row["routes"].items()
        }
        assert set(verdicts) == set(kernel.ROUTES)
        assert len(set(verdicts.values())) == 1
    wall = [row for row in record["controls"] if row["control"] == sharp.ENLARGED_WALL]
    assert wall[0]["detail"]["square"] == 1
    assert Fraction(wall[0]["detail"]["wall_clearance"]) == 0
    pair = next(
        row
        for row in record["controls"]
        if row["control"] == sharp.ENLARGED_PAIR and row["where"] == "at-contact"
    )
    assert (pair["detail"]["square"], pair["detail"]["partner"]) == (166, 156)
    assert Fraction(pair["detail"]["pair_gap"]) > kernel.SHARP_EPSILON
    assert pair["expected_failures"] == ["shape"]


def test_the_identity_measurement_pairs_it_one_to_one_with_t301() -> None:
    """Nearest centres pair it one to one with T-301, with five squares beyond a tenth.

    The house witness measures as T-301's packet. T-300 has no one-to-one pairing.
    """
    record = _json(_packet() / "measure/identity.json")
    pairs = {pair["against"]: pair for pair in record["pairs"]}
    t301 = pairs["T-301"]
    assert t301["nearest_centre"]["one_to_one"] is True
    assert t301["assignment"]["symmetry"] == 0
    assert t301["assignment"]["moved_beyond"]["1e-3"] == 86
    assert t301["assignment"]["moved_beyond"]["1e-1"] == 5
    assert t301["assignment"]["largest_move"] == "0.238073"
    assert pairs["house-witness"]["assignment"] == t301["assignment"]
    assert pairs["T-300"]["nearest_centre"]["one_to_one"] is False


def test_option_d_the_certificate_is_below_t301_shrunk_to_first_contact() -> None:
    """The owner's option D (think-b0w5): T-301 contracted uniformly to first contact has
    margin 3.4875e-09; the gain is 1.2298 of it, so the certificate lies below the
    contracted side, by 8.015e-10, and is a new result. Its own margin is the clearance
    factor's, below 1e-21."""
    record = _json(_packet() / "measure/contraction-n228.json")
    assert (record["certificate"]["label"], record["binding_pair"]) == ("T-301", [8, 21])
    assert record["routes_accept"] is True
    against = record["against"]
    assert against["certificate"] == {"label": "ozden-1038", "input": "packet", "packet": NAME}
    assert against["within_margin"] is False
    assert Fraction(against["side"]) == _side()
    below = Fraction(record["contracted_side"]) - _side()
    assert Fraction(8, 10**10) < below < Fraction(81, 10**11)
    assert against["gain_over_margin"] == "1.2298"
    own = _json(_packet() / "measure/contraction-n228-own.json")
    assert (own["certificate"]["label"], own["binding_pair"]) == ("ozden-1038", [156, 166])
    assert 0 < Fraction(own["margin"]) < Fraction(1, 10**21)


def test_the_projects_held_solve_lies_just_below_the_certificate() -> None:
    """The held view is 9.66e-14 below this side and below T-301 shrunk to first contact;
    it stays a register candidate (think-4z8z), and this claim keeps its status (think-frl5)."""
    gap = _side() - HELD
    assert Fraction(9, 10**14) < gap < Fraction(1, 10**13)
    contracted = Fraction(_json(_packet() / "measure/contraction-n228.json")["contracted_side"])
    assert contracted > HELD


def test_the_l_step_scan_stands_the_side_in_and_carries_it_nowhere() -> None:
    record = _json(_packet() / "measure/l-step-scan.json")
    assert {int(n): Fraction(side) for n, side in record["with"].items()} == {228: _side()}
    steps = record["l_step"]["improves"] + record["l_step"]["extensions"]
    assert not [row for row in steps if 228 in (row["n"], row["from"])]
    assert record["monotonicity"]["improves"] == []
