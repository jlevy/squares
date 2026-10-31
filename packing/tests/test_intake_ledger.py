"""The owner's report-order rule, on synthetic counts and every retained intake ledger."""

from __future__ import annotations

import copy
import gzip
import json
import shutil
from fractions import Fraction
from pathlib import Path
from typing import Any, cast

import pytest
import yaml

from devtools import check_standing, goebel_construction
from devtools import intake_ledger as ledger
from devtools.upper_bound_reports import exact_span

GRID_10 = ledger.beyond_side(400, {})
CLAIM_TIME = "2026-10-12T00:00:00Z"


def record(value: str = "10.5", exact_form: str = "21/2") -> ledger.Side:
    bound = {"value": value, "exact_form": exact_form, "found_by": ["A. Holder"]}
    return ledger.record_side(100, bound, ["T-001"])


def side(
    label: str, printed: str, rounding: str = "exact", when: str = CLAIM_TIME, **more: Any
) -> ledger.Side:
    claim = cast("ledger.Claim", {"n": 100, "printed": printed, "rounding": rounding, **more})
    report: ledger.Report = {
        "report": label,
        "url": f"https://github.com/jlevy/squares/issues/{label.lstrip('#')}",
        "kind": "issue",
        "holders": f"holder of {label}",
        "reported_at": when,
        "bead": "",
        "claims": [claim],
    }
    return ledger.entry_side(report, claim)


def verdicts(walk: ledger.Walk) -> list[tuple[str, str, str]]:
    return [(step.side.label, step.verdict, ledger.held_by(step)) for step in walk.steps]


def test_later_and_stronger_is_recorded() -> None:
    first = side("#1", "10.4", when="2026-10-12T01:00:00Z")
    second = side("#2", "10.3", when="2026-10-12T02:00:00Z")
    walk = ledger.walk(100, record(), [second, first])
    assert verdicts(walk) == [("#1", "recorded", "record T-001"), ("#2", "recorded", "#1")]
    assert [item.label for item in walk.standing] == ["#2"]


def test_an_earlier_stronger_report_leaves_the_later_one_unrecorded() -> None:
    stronger = side("#1", "10.3", when="2026-10-12T01:00:00Z")
    weaker = side("#2", "10.4", when="2026-10-12T02:00:00Z")
    walk = ledger.walk(100, record(), [weaker, stronger])
    assert verdicts(walk) == [("#1", "recorded", "record T-001"), ("#2", "not recorded", "#1")]
    assert walk.steps[1].reason == ledger.ABOVE


def test_an_exact_tie_is_not_recorded_and_names_the_holder() -> None:
    first = side("#1", "103/10", when="2026-10-12T01:00:00Z")
    tie = side("#2", "10.3", when="2026-10-12T02:00:00Z")
    walk = ledger.walk(100, record(), [first, tie])
    assert verdicts(walk)[1] == ("#2", "not recorded", "#1")
    assert walk.steps[1].reason == ledger.EQUAL


def test_a_tie_with_the_record_itself_is_not_recorded_and_is_an_owner_decision() -> None:
    tie = side("#1", "21/2")
    walk = ledger.walk(100, record(), [tie])
    assert verdicts(walk) == [("#1", "not recorded", "record T-001")]
    assert walk.steps[0].reason == ledger.EQUAL
    assert [item.label for item in walk.standing] == ["record T-001"]
    data = _minimal()
    data["reports"][0]["claims"] = [{"n": 100, "printed": "10.5", "rounding": "exact"}]
    decisions = ledger.evaluate(cast(ledger.Ledger, data), {100: [record()]})
    assert decisions["owner_decisions"]["exact_ties"] == [
        {
            "n": 100,
            "report": "#1",
            "holders": "A",
            "tied_with": "record T-001",
            "tied_holders": "A. Holder",
        }
    ]


def test_a_frozen_equal_in_a_walk_is_a_tie_with_the_record() -> None:
    form = "2 + (1/2)sqrt(2)"
    start = ledger.record_side(5, {"value": "2.70710678118654", "exact_form": form}, ["T-005"])
    equal: ledger.RecordRelation = {
        "lane": "reported",
        "relation": "equal",
        "value": "2.70710678118654",
        "exact_form": form,
        "read_from": "lane",
    }
    claim = side("#1", "2.7071067811865475244008443621", "unstated", record_relations=[equal])
    later = side("#2", "2.70710678118", "up", when="2026-10-12T05:00:00Z")
    walk = ledger.walk(5, start, [claim, later])
    assert verdicts(walk) == [
        ("#1", "not recorded", "record T-005"),
        ("#2", "recorded", "record T-005"),
    ]
    assert walk.steps[0].reason == ledger.EQUAL


def test_a_claim_above_an_undecided_claim_is_not_recorded() -> None:
    first = side("#1", "10.40", "up", when="2026-10-12T01:00:00Z")
    second = side("#2", "10.395", "nearest", when="2026-10-12T02:00:00Z")
    third = side("#3", "10.3956", when="2026-10-12T03:00:00Z")
    walk = ledger.walk(100, record(), [first, second, third])
    assert verdicts(walk) == [
        ("#1", "recorded", "record T-001"),
        ("#2", "undecided", "#1"),
        ("#3", "not recorded", "#2"),
    ]
    assert walk.steps[2].reason == ledger.ABOVE
    assert {item.label for item in walk.standing} == {"#1", "#2"}


def test_up_cut_and_binary64_prints_decide_as_their_spans_say() -> None:
    # An up print at the record's value may be the record: undecided. A cut print whose
    # next unit is the record excludes it: recorded.
    assert ledger.walk(100, record(), [side("#1", "10.50", "up")]).steps[0].verdict == (
        ledger.UNDECIDED
    )
    assert ledger.walk(100, record(), [side("#1", "10.49", "up")]).steps[0].verdict == (
        ledger.RECORDED
    )
    assert ledger.walk(100, record(), [side("#1", "10.49", "cut")]).steps[0].verdict == (
        ledger.RECORDED
    )
    assert ledger.walk(100, record(), [side("#1", "10.50", "cut")]).steps[0].verdict == (
        ledger.UNDECIDED
    )
    # A 16-place double read as binary64 reaches past the record that its nearest
    # reading is below.
    printed = "10.4999999999999982"
    nearest = ledger.walk(100, record(), [side("#1", printed, "nearest")])
    binary64 = ledger.walk(100, record(), [side("#1", printed, "binary64")])
    assert (nearest.steps[0].verdict, binary64.steps[0].verdict) == (
        ledger.RECORDED,
        ledger.UNDECIDED,
    )


def test_a_claim_of_unknown_time_is_kept_out_of_the_walk_and_listed() -> None:
    data = _minimal()
    data["reports"].append(
        {
            "report": "#2",
            "url": "https://github.com/jlevy/squares/issues/2",
            "kind": "issue",
            "holders": "B",
            "reported_at": ledger.UNKNOWN,
            "bead": "",
            "claims": [{"n": 100, "printed": "10.1", "rounding": "exact"}],
        }
    )
    assert ledger.problems(data) == []
    verdict = ledger.evaluate(cast(ledger.Ledger, data), {100: [record()]})
    assert [step["report"] for step in verdict["counts"][0]["steps"]] == ["#1"]
    assert verdict["owner_decisions"]["unknown_times"] == [
        {"n": 100, "report": "#2", "holders": "B"}
    ]
    assert [item["label"] for item in verdict["counts"][0]["best_now"]] == ["#1"]


def test_overlapping_prints_are_undecided_and_say_what_decides_them() -> None:
    first = side("#1", "10.40", "up", when="2026-10-12T01:00:00Z")
    second = side("#2", "10.395", "nearest", when="2026-10-12T02:00:00Z")
    walk = ledger.walk(100, record(), [first, second])
    assert verdicts(walk)[1] == ("#2", "undecided", "#1")
    assert {item.label for item in walk.standing} == {"#1", "#2"}
    assert "the exact side of #1" in ledger.decider(walk.steps[1].side, walk.steps[1].against)
    # A claim below both members of the undecided standing side is recorded.
    third = side("#3", "10.2", when="2026-10-12T03:00:00Z")
    later = ledger.walk(100, record(), [first, second, third])
    assert verdicts(later)[2] == ("#3", "recorded", "#1, #2")


def test_a_pending_adoption_bound_lowers_the_start() -> None:
    entry = {"id": "T-123", "attribution": {"source_keys": ["[Source 2026]"]}}
    stated = check_standing.Stated(Fraction("10.40"), Fraction(1, 100))
    pending = ledger.pending_side(entry, stated)
    start = ledger.minimal([record(), pending])
    assert [item.label for item in start] == ["register T-123, pending adoption"]
    # A claim at 10.45 is below the record and above the pending bound: not recorded.
    walk = ledger.walk(100, [record(), pending], [side("#1", "10.45")])
    assert verdicts(walk) == [("#1", "not recorded", "register T-123, pending adoption")]
    # A bound that is not below the record lowers nothing.
    higher = ledger.pending_side(entry, check_standing.Stated(Fraction("10.6"), Fraction(0)))
    assert [item.label for item in ledger.minimal([record(), higher])] == ["record T-001"]


def test_two_overlapping_pending_bounds_both_stay_in_the_start() -> None:
    # The review's bug_demos case: T-901 is [10.40, 10.41) and T-902 [10.405, 10.406); a
    # claim at 10.45 is above both, so it is not recorded, whatever the record says.
    first = ledger.pending_side(
        {"id": "T-901"}, check_standing.Stated(Fraction("10.40"), Fraction(1, 100))
    )
    second = ledger.pending_side(
        {"id": "T-902"}, check_standing.Stated(Fraction("10.405"), Fraction(1, 1000))
    )
    start = ledger.minimal([record(), first, second])
    assert {item.label for item in start} == {
        "register T-901, pending adoption",
        "register T-902, pending adoption",
    }
    walk = ledger.walk(100, [record(), first, second], [side("#1", "10.45")])
    assert walk.steps[0].verdict == ledger.NOT_RECORDED
    assert ledger.held_by(walk.steps[0]) == (
        "register T-901, pending adoption, register T-902, pending adoption"
    )


def test_the_start_is_both_lanes_and_the_verified_root_decides() -> None:
    # The reported lane prints sqrt(2) at 14 places; the verified lane names the root of
    # s^2 - 2. A rational above the root but inside the print is not recorded against it.
    reported = {"value": "1.41421356237309", "minimal_polynomial": "s^2 - 2 = 0"}
    verified = {
        "value": "1.4142135623730950488",
        "exact_form": "root(P, 1.4142135623730950488)",
    }
    lanes = ledger.merged_lanes(
        ledger.lane_member(9, "reported", reported, ["T-009"], "s^2 - 2 = 0"),
        ledger.lane_member(9, "verified", verified, ["T-009"], "s^2 - 2 = 0"),
    )
    assert [member["model"] for member in lanes] == ["print", "root"]
    start = [ledger.side_of(member) for member in lanes]
    claim = side("#1", "1414213562373096/1000000000000000")
    walk = ledger.walk(9, start, [claim])
    assert verdicts(walk) == [("#1", "not recorded", "record T-009 (verified lane)")]
    # One lane alone, the print, leaves it undecided.
    assert ledger.walk(9, start[:1], [claim]).steps[0].verdict == ledger.UNDECIDED


def test_each_lane_reads_its_own_polynomial_and_a_root_off_its_print_is_refused() -> None:
    reported = {"value": "1.41421356237309", "minimal_polynomial": "s^2 - 2 = 0"}
    verified = {
        "value": "1.7320508075688772",
        "exact_form": "root(P, 1.7320508075688772)",
        "minimal_polynomial": "s^2 - 3 = 0",
    }
    texts = ledger.lane_polynomials(reported, verified)
    assert texts == ("s^2 - 2 = 0", "s^2 - 3 = 0")
    member = ledger.lane_member(3, "verified", verified, ["T-003"], texts[1])
    span = ledger.side_of(member).span
    assert member["model"] == "root"
    assert span.low**2 < 3 < span.high**2
    # The reported lane's polynomial has no root inside the verified lane's print.
    with pytest.raises(ledger.LedgerError, match="outside that print"):
        ledger.lane_member(3, "verified", verified, ["T-003"], texts[0])
    # A verified root( form states no polynomial of its own and names the reported
    # lane's, as n = 11's P_trump11 does; any other verified lane reads none.
    named = {"value": "1.4142135623730950488", "exact_form": "root(P, 1.4142135623730950488)"}
    assert ledger.lane_polynomials(reported, named) == ("s^2 - 2 = 0", "s^2 - 2 = 0")
    assert ledger.lane_polynomials(reported, {"value": "2", "exact_form": "2"})[1] == ""


def test_a_holder_is_credited_by_the_display_name_the_intake_gives() -> None:
    bound = {
        "value": "10.5",
        "exact_form": "21/2",
        "found_by": ["ry-xu"],
        "improved_by": ["Evan Daniel"],
    }
    names = ledger.display_names({"display_names": {"ry-xu": "Ryan Xu"}})
    member = ledger.lane_member(100, "reported", bound, ["T-146"], names=names)
    assert (member["label"], member["holders"]) == (
        "record T-146",
        "Ryan Xu, improved by Evan Daniel",
    )
    assert ledger.lane_member(100, "reported", bound, ["T-146"])["holders"].startswith("ry-")
    with pytest.raises(ledger.LedgerError, match="display_names"):
        ledger.display_names({"display_names": ["ry-xu"]})


def test_the_committed_ledger_credits_ryan_xu_by_name() -> None:
    # The owner, 2026-10-14: credit Ryan Xu by name or surname, never by the handle.
    verdicts = json.loads((ledger.DEFAULT_DIRECTORY / ledger.VERDICTS).read_text("utf-8"))
    named = [report["holders"] for report in verdicts["reports"]]
    for count in verdicts["counts"]:
        named += [side["holders"] for side in (*count["start"], *count["best_now"])]
        steps = [step for step in count["steps"] if "packing" in step]
        named += [step["packing"].get("packing_of", "") for step in steps]
    assert any("Ryan Xu" in credit for credit in named)
    assert not [credit for credit in named if "ry-xu" in credit]


def test_two_lanes_with_one_side_are_one_member() -> None:
    bound = {"value": "7.6903559372884918", "exact_form": "(16+5*sqrt(2))/3"}
    lanes = ledger.merged_lanes(
        ledger.lane_member(51, "reported", bound, ["T-126"]),
        ledger.lane_member(51, "verified", bound, ["T-126"]),
    )
    assert [member["label"] for member in lanes] == ["record T-126"]
    assert len(lanes[0]["lanes"]) == 2


def test_a_sqrt_closed_form_is_a_rigorous_interval() -> None:
    span = ledger.closed_form_span("(16+5*sqrt(2))/3")
    assert span is not None
    assert span.high - span.low < Fraction(1, 10**80)
    # #593's exact side at 51 is 7.69e-20 above the radical side, decided exactly.
    above = Fraction(7690355937288491748079718099723, 10**30)
    assert ledger.below(span, exact_span(above))
    assert ledger.closed_form_span("7 + (4/7)") == exact_span(Fraction(53, 7))
    assert ledger.closed_form_span("root(P, 1.5)") is None


def test_a_root_enclosure_brackets_the_root() -> None:
    span = ledger.root_span(ledger.polynomial("4775s^{2} - 9550 = 0"), "1.41421356")
    assert span.low**2 < 2 < span.high**2
    assert span.high - span.low < Fraction(1, 10**60)
    assert ledger.polynomial("s^8 - 20s^7 + 6865 = 0")[:2] == [1, -20]


def test_the_start_beyond_the_horizon_is_the_row_or_the_grid() -> None:
    row = {"n": 400, "source_id": "row-2026-10-11", "value": "19.990000000000"}
    from_row = ledger.beyond_side(400, {400: row})
    assert from_row.label == "beyond-horizon row row-2026-10-11"
    assert ledger.walk(400, from_row, [side("#1", "19.99")]).steps[0].verdict == "undecided"
    assert GRID_10.label == "the grid"
    assert GRID_10.span == exact_span(Fraction(20))
    walk = ledger.walk(400, GRID_10, [side("#1", "19.99"), side("#2", "20")])
    assert [step.verdict for step in walk.steps] == ["recorded", "not recorded"]


def test_an_exception_is_applied_and_shown() -> None:
    stronger = side("#1", "10.3", when="2026-10-12T01:00:00Z")
    weaker = side("#2", "10.4", when="2026-10-12T02:00:00Z")
    walk = ledger.walk(100, record(), [stronger, weaker], {(100, "#2"): "first committed"})
    assert walk.steps[1].verdict == ledger.BY_EXCEPTION
    assert ledger.step_record(walk.steps[1])["exception"] == "first committed"
    # The exception moves nothing: the stronger report still holds the count.
    assert [item.label for item in walk.standing] == ["#1"]


#: Both of the owner's rulings of 23 October 2026, at every count beyond the horizon.
RULED = ledger.Rulings(restatement=ledger.NO_LIMIT, classical=ledger.NO_LIMIT)


def test_a_side_within_the_print_below_a_report_restates_it() -> None:
    """The owner's answer of 23 October 2026 (think-fwa9): beyond the horizon a side below
    an earlier report by less than one unit in the 12th place, both rounding up to one
    12-place print, restates it and is not recorded; a full unit below is recorded. The
    corpus and a ledger without the ruling walk as before."""
    earlier = side("#1", "39/2", when="2026-10-12T01:00:00Z")
    close = side("#2", "19.49999999999999999999", when="2026-10-12T02:00:00Z")
    far = side("#3", "19.499999999999", when="2026-10-12T03:00:00Z")
    walk = ledger.walk(400, GRID_10, [earlier, close, far], rulings=RULED)
    assert verdicts(walk) == [
        ("#1", "recorded", "the grid"),
        ("#2", "not recorded", "#1"),
        ("#3", "recorded", "#1"),
    ]
    assert walk.steps[1].reason == ledger.RESTATES
    assert ledger.step_record(walk.steps[1])["difference"] == (
        "restates, below by 1.00e-20 at the same 12-place print"
    )
    for plain in (
        ledger.walk(400, GRID_10, [earlier, close], rulings=ledger.Rulings()),
        ledger.walk(324, GRID_10, [earlier, close], rulings=RULED),
        ledger.walk(400, GRID_10, [earlier, close], rulings=ledger.Rulings(restatement=399)),
    ):
        assert [step.verdict for step in plain.steps] == ["recorded", "recorded"]


def test_a_claim_in_the_ruling_s_words_may_wait_on_the_owner() -> None:
    earlier = side("#1", "39/2", when="2026-10-12T01:00:00Z")
    close = side("#2", "19.49999999999999999999", when="2026-10-12T02:00:00Z")
    rulings = ledger.Rulings(restatement=ledger.NO_LIMIT, awaiting={(400, "#2"): "think-oqjd"})
    walk = ledger.walk(400, GRID_10, [earlier, close], rulings=rulings)
    assert [step.verdict for step in walk.steps] == ["recorded", "recorded"]
    assert ledger.step_record(walk.steps[1])["awaiting_owner"] == "think-oqjd"


def test_goebel_s_construction_is_an_earlier_report_beyond_the_horizon(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The owner's answer on #613 (think-8krd): at 369 Göbel's strip 19 + sqrt(2)/2 joins
    the start below the grid, so a side above it is not recorded and one below is. A side
    just below the construction at its 12-place print is recorded: the restatement ruling
    as written restates reports, and whether it also reaches a construction is an open
    question (think-oqjd); no case of it exists to 1024. A count whose side no build proves
    final is refused rather than read as absent: with every build capped at the retained
    program's limit of 1100, 1074 (think-llit); the module's builds read it, and 9913."""
    construction = ledger.construction_side(369)
    assert construction is not None
    assert construction.kind == ledger.CONSTRUCTION
    assert construction.shown == "19.707106781187"
    grid = ledger.beyond_side(369, {})
    above = side("#1", "19.71", when="2026-10-12T01:00:00Z")
    under = side("#2", "19.7071067811865", when="2026-10-12T02:00:00Z")
    walk = ledger.walk(369, grid, [above, under], rulings=RULED)
    assert [member.label for member in walk.start] == [ledger.GOEBEL_LABEL]
    assert verdicts(walk) == [
        ("#1", "not recorded", ledger.GOEBEL_LABEL),
        ("#2", "recorded", ledger.GOEBEL_LABEL),
    ]
    plain = ledger.walk(369, grid, [above, under])
    assert [step.verdict for step in plain.steps] == ["recorded", "recorded"]
    assert ledger.construction_side(324) is None
    assert ledger.goebel_reach() == 10_345
    for n in (1073, 1074, 9913):
        assert ledger.construction_side(n) is not None
    monkeypatch.setattr(goebel_construction, "MAX_BUILD", 1100)
    for n in (1074, 1100, 1101):
        with pytest.raises(ledger.LedgerError, match=rf"n = {n}: no build to 1100 proves"):
            ledger.construction_side(n)


def test_a_ruling_names_a_known_answer_its_day_and_its_bead() -> None:
    data = _minimal()
    data["rulings"] = [
        {"ruling": "restatement", "decided": "2026-10-23", "bead": "think-fwa9"},
        {"ruling": "classical-constructions", "decided": "2026-10-23", "bead": "think-8krd"},
    ]
    assert ledger.problems(data) == []
    assert ledger.rulings_of(data) == RULED
    data["rulings"] = [
        {"ruling": "other", "decided": "23 October", "bead": "8krd", "through": 300},
        {
            "ruling": "classical-constructions",
            "decided": "2026-10-23",
            "bead": "think-8krd",
            "awaiting_owner": [{"n": 101, "report": "#1", "bead": "think-oqjd", "reason": ""}],
        },
        {"ruling": "classical-constructions", "decided": "2026-10-23", "bead": "think-8krd"},
    ]
    assert ledger.problems(data) == [
        "ruling other: no such ruling",
        "ruling other: decided is not a date",
        "ruling other: bead is not a think-xxxx id",
        "ruling other: through is not a count beyond the horizon",
        (
            "ruling classical-constructions: only the restatement ruling keeps claims for "
            "the owner"
        ),
        "ruling classical-constructions awaiting ('#1', 101): names no claim of the ledger",
        "ruling classical-constructions awaiting ('#1', 101): states no reason",
        "ruling classical-constructions: listed twice",
    ]


def test_a_closed_form_of_integers_is_a_rational_record() -> None:
    assert ledger.record_side(
        50, {"value": "7.57142857142857", "exact_form": "7 + (4/7)"}, []
    ).exact


def test_a_frozen_relation_holds_only_while_the_lane_reads_so_and_in_both_orders() -> None:
    form = "2 + (1/2)sqrt(2)"
    start = ledger.record_side(5, {"value": "2.70710678118654", "exact_form": form}, ["T-005"])
    frozen: ledger.RecordRelation = {
        "lane": "reported",
        "relation": "equal",
        "value": "2.70710678118654",
        "exact_form": form,
        "read_from": "lane",
    }
    print_ = "2.7071067811865475244008443621048490392848"
    algebraic = side("#1", print_, "unstated", record_relations=[frozen])
    assert ledger.compare(algebraic, start) == ledger.EQUAL
    assert ledger.compare(start, algebraic) == ledger.EQUAL
    below_it = side(
        "#2", print_, "unstated", record_relations=[{**frozen, "relation": "below"}]
    )
    assert ledger.compare(start, below_it) == ledger.ABOVE
    # A record that moved, or the other lane, does not take the relation.
    moved = ledger.record_side(5, {"value": "2.707106781186547", "exact_form": form}, ["T-005"])
    assert ledger.compare(algebraic, moved) == ledger.UNDECIDED
    verified = ledger.record_side(
        5, {"value": "2.70710678118654", "exact_form": form}, ["T-005"], lane="verified"
    )
    assert ledger.compare(algebraic, verified) == ledger.UNDECIDED


BELOW_THE_RECORD: ledger.RecordRelation = {
    "lane": "reported",
    "relation": "below",
    "value": "10.5",
    "exact_form": "21/2",
    "read_from": "lane",
}


def test_a_frozen_below_survives_once_the_record_leaves_the_standing_side() -> None:
    # #1's print overlaps the record 21/2 and a lane froze it below; #2 is exactly above
    # the record and inside #1's print. #1, recorded, still holds the count against #2.
    first = side(
        "#1",
        "10.5000000000",
        "unstated",
        when="2026-10-12T01:00:00Z",
        record_relations=[BELOW_THE_RECORD],
    )
    second = side("#2", "10.50000000005", when="2026-10-12T02:00:00Z")
    assert ledger.compare(second, record()) == ledger.ABOVE
    walk = ledger.walk(100, record(), [first, second])
    assert verdicts(walk) == [("#1", "recorded", "record T-001"), ("#2", "not recorded", "#1")]
    assert [item.label for item in walk.standing] == ["#1"]
    assert walk.standing[0].span.high == Fraction(21, 2)
    assert walk.standing[0].span.open_high


def test_a_frozen_below_survives_when_the_claim_joins_an_undecided_set() -> None:
    # A pending bound overlapping the record leaves #1 undecided; #1 joins the set and the
    # record leaves it, so #2 is above #1 through the relation, not undecided against it.
    entry = {"id": "T-123"}
    pending = ledger.pending_side(
        entry, check_standing.Stated(Fraction("10.45"), Fraction(1, 10))
    )
    first = side(
        "#1",
        "10.5000000000",
        "unstated",
        when="2026-10-12T01:00:00Z",
        record_relations=[BELOW_THE_RECORD],
    )
    second = side("#2", "10.50000000005", when="2026-10-12T02:00:00Z")
    walk = ledger.walk(100, [record(), pending], [first, second])
    assert [step.verdict for step in walk.steps] == ["undecided", "not recorded"]
    assert ledger.held_by(walk.steps[1]) == "#1"
    assert {item.label for item in walk.standing} == {"register T-123, pending adoption", "#1"}


def test_a_frozen_below_an_interval_member_ends_at_its_high() -> None:
    # The relation compares with the member's exact value, which may be anywhere in its
    # enclosure, so the claim is bounded by the enclosure's high and never by its low.
    form = "2 + (1/2)sqrt(2)"
    member = ledger.record_side(5, {"value": "2.70710678118654", "exact_form": form}, [])
    relation: ledger.RecordRelation = {
        "lane": "reported",
        "relation": "below",
        "value": "2.70710678118654",
        "exact_form": form,
        "read_from": "lane",
    }
    claim = side("#1", "2.70710678118654752440", "unstated", record_relations=[relation])
    bounded = ledger.clamped(claim, [member])
    assert (bounded.span.low, bounded.span.high) == (claim.span.low, member.span.high)
    assert bounded.span.open_high
    assert ledger.clamped(claim, [record()]) is claim


def test_a_decided_relation_to_a_pending_entry_holds_while_it_states_its_value() -> None:
    # #1 lies inside T-123's stated span, so the prints leave it undecided; a receipt
    # decided it exactly above the entry's exact side, by the margin the ledger shows.
    stated = check_standing.Stated(Fraction("10.40"), Fraction(1, 100))
    pending = ledger.side_of(ledger.pending_member({"id": "T-123"}, stated))
    decided: ledger.RecordRelation = {
        "lane": "T-123",
        "relation": "above",
        "value": "52/5",
        "exact_form": "",
        "read_from": "a receipt",
        "margin": "1.25e-30",
    }
    printed = "10.400000000000000000000000000002"
    assert ledger.compare(side("#1", printed), pending) == ledger.UNDECIDED
    claim = side("#1", printed, record_relations=[decided])
    walk = ledger.walk(100, [pending], [claim])
    assert verdicts(walk) == [("#1", "not recorded", "register T-123, pending adoption")]
    assert ledger.step_record(walk.steps[0])["difference"] == "above by 1.25e-30"
    # Another entry, or the entry stating another value, does not take the relation.
    other = ledger.side_of(ledger.pending_member({"id": "T-124"}, stated))
    restated = check_standing.Stated(Fraction("10.39"), Fraction(2, 100))
    moved = ledger.side_of(ledger.pending_member({"id": "T-123"}, restated))
    assert ledger.compare(claim, other) == ledger.UNDECIDED
    assert ledger.compare(claim, moved) == ledger.UNDECIDED


def test_a_decided_relation_shows_its_margin_where_the_prints_meet() -> None:
    lane = ledger.record_side(17, {"value": "4.67553009360455"}, ["[K]"])
    relation: ledger.RecordRelation = {
        "lane": "reported",
        "relation": "above",
        "value": "4.67553009360455",
        "exact_form": "",
        "read_from": "a receipt",
        "margin": "1.28e-93",
    }
    printed = "4.675530093604550951634111270483"
    walk = ledger.walk(17, lane, [side("#1", printed, record_relations=[relation])])
    assert verdicts(walk) == [("#1", "not recorded", "record [K]")]
    assert ledger.step_record(walk.steps[0])["difference"] == "above by 1.28e-93"
    # Without a margin the difference is the prints' distance, which says only "about".
    unmeasured = {key: value for key, value in relation.items() if key != "margin"}
    walk = ledger.walk(17, lane, [side("#1", printed, record_relations=[unmeasured])])
    assert ledger.step_record(walk.steps[0])["difference"].startswith("above by about ")


def test_gather_keeps_a_lanes_relations_beside_the_transcribed_ones(tmp_path: Path) -> None:
    read_at_main = "f" * 40
    mapping = {
        "lane": "lane",
        "packet": "absent-packet-2026-10-14",
        "record": "algebraic-claims.json",
    }
    decided = {**BELOW_THE_RECORD, "read_from": "a receipt"}
    sources = {
        "format": ledger.SOURCES_FORMAT,
        "read_at_main": read_at_main,
        "read_on": "2026-10-14",
        "rule": "the owner's rule",
        "lanes": [{"name": "lane", "branch": "a-branch", "commit": "a" * 40}],
        "reports": [
            {
                "report": "owner/repo@abc1234",
                "url": "https://github.com/owner/repo/tree/abc1234",
                "reported_at": CLAIM_TIME,
                "holders": "A",
                "lanes": [{**mapping, "all": True}],
                "claims": [{"n": 100, "record_relations": [decided]}],
            }
        ],
    }
    (tmp_path / ledger.SOURCES).write_text(yaml.safe_dump(sources), encoding="utf-8")
    snapshot = {"format": ledger.SNAPSHOT_FORMAT, "items": []}
    (tmp_path / ledger.SNAPSHOT).write_text(json.dumps(snapshot), encoding="utf-8")
    member = ledger.lane_member(100, "reported", {"value": "10.5", "exact_form": "21/2"}, [])
    starts = ledger.starts_document(read_at_main, {100: [member]})
    (tmp_path / ledger.STARTS).write_text(yaml.safe_dump(starts), encoding="utf-8")
    row = {
        "n": 100,
        "side_decimal": "10.5000000000",
        "degree": 2,
        "first_committed": "2026-10-11T00:00:00Z",
        "case": {
            "verified_relation": "below",
            "verified_value": "10.51",
            "verified_exact_form": "1051/100",
        },
    }
    copy_ = tmp_path / ledger.LANE_CLAIMS / "lane" / mapping["packet"] / mapping["record"]
    copy_.parent.mkdir(parents=True)
    copy_.write_text(json.dumps({"results": [row]}), encoding="utf-8")
    assert ledger.gather(tmp_path, snapshot=True) == []
    claim = ledger.load_ledger(tmp_path)["reports"][0]["claims"][0]
    relations = claim.get("record_relations", [])
    assert [(item["lane"], item["read_from"]) for item in relations] == [
        ("verified", f"{ledger.record_path(mapping)} at a-branch@{'a' * 40}"),
        ("reported", "a receipt"),
    ]
    assert claim["printed"] == "10.5000000000"


def test_a_binary64_print_spans_one_ulp_and_a_cut_print_its_next_unit() -> None:
    span = ledger.printed_side("17.8702753825550609", "binary64")
    assert ledger.contains(span, Fraction("17.8702753825550621"))
    assert not ledger.contains(
        ledger.printed_side("17.8702753825550609", "nearest"), Fraction("17.8702753825550621")
    )
    nearest = ledger.printed_side("12.95", "nearest")
    assert ledger.contains(nearest, Fraction("12.955"))
    assert not ledger.contains(nearest, Fraction("12.9551"))
    cut = ledger.printed_side("12.95", "cut")
    assert ledger.contains(cut, Fraction("12.959"))
    assert not ledger.contains(cut, Fraction("12.96"))


def _minimal() -> dict[str, Any]:
    return {
        "format": ledger.LEDGER_FORMAT,
        "read_at_main": "f" * 40,
        "read_on": "2026-10-14",
        "rule": "the owner's rule",
        "lanes": [],
        "reports": [
            {
                "report": "#1",
                "url": "https://github.com/jlevy/squares/issues/1",
                "kind": "issue",
                "holders": "A",
                "reported_at": CLAIM_TIME,
                "bead": "think-abcd",
                "claims": [{"n": 100, "printed": "10.4", "rounding": "up", "exact": "52/5"}],
            }
        ],
        "exceptions": [],
        "other_items": [],
    }


DECIDED: ledger.RecordRelation = {
    "lane": "T-123",
    "relation": "above",
    "value": "52/5",
    "exact_form": "",
    "read_from": "a receipt",
    "margin": "1.0e-30",
}


def test_check_holds_the_schema_the_prints_and_the_times() -> None:
    assert ledger.problems(_minimal()) == []
    decided = copy.deepcopy(_minimal())
    decided["reports"][0]["claims"][0]["record_relations"] = [DECIDED]
    assert ledger.problems(decided) == []
    above_its_print = copy.deepcopy(_minimal())
    above_its_print["reports"][0]["claims"][0]["exact"] = "10401/1000"
    assert "outside its own print" in " ".join(ledger.problems(above_its_print))
    bad_time = copy.deepcopy(_minimal())
    bad_time["reports"][0]["reported_at"] = "12 October"
    assert "reported_at" in " ".join(ledger.problems(bad_time))
    duplicated = copy.deepcopy(_minimal())
    duplicated["reports"][0]["claims"].append(dict(duplicated["reports"][0]["claims"][0]))
    assert "listed twice" in " ".join(ledger.problems(duplicated))
    orphan = copy.deepcopy(_minimal())
    orphan["exceptions"] = [{"n": 7, "report": "#1", "reason": "why"}]
    assert "names no claim" in " ".join(ledger.problems(orphan))


@pytest.mark.parametrize(
    ("edit", "expected"),
    [
        (lambda data: data.pop("reports"), "missing ['reports']"),
        (lambda data: data.pop("lanes"), "missing ['lanes']"),
        (lambda data: data.update(reports="#1"), "reports is not a list"),
        (lambda data: data["reports"][0]["claims"].append("n=100"), "is not a mapping"),
        (lambda data: data["reports"][0]["claims"][0].update(n="abc"), "not a positive count"),
        (lambda data: data["reports"][0]["claims"][0].update(n=True), "not a positive count"),
        (lambda data: data["reports"][0].update(holders=["A"]), "are not strings"),
        (
            lambda data: data["reports"][0]["claims"][0].update(refines="T-001"),
            "refines is not a mapping",
        ),
        (
            lambda data: data["reports"][0]["claims"][0].update(record_relations=["below"]),
            "a record relation is not a mapping",
        ),
        (
            lambda data: data["reports"][0]["claims"][0].update(record_relations="below"),
            "record_relations is not a list",
        ),
        (
            lambda data: data["reports"][0]["claims"][0].update(
                record_relations=[{**DECIDED, "lane": "register"}]
            ),
            "names the reported or verified lane or a register entry",
        ),
        (
            lambda data: data["reports"][0]["claims"][0].update(
                record_relations=[{**DECIDED, "margin": "-1.0e-30"}]
            ),
            "a record relation above has the margin -1.0e-30",
        ),
        (
            lambda data: data["reports"][0]["claims"][0].update(
                record_relations=[{**DECIDED, "margin": "about 1e-30"}]
            ),
            "margin 'about 1e-30' is not a number",
        ),
        (
            lambda data: data["reports"][0]["claims"][0].update(
                record_relations=[DECIDED, {**DECIDED, "relation": "below", "margin": "-1"}]
            ),
            "two record relations read T-123 at 52/5",
        ),
        (
            lambda data: data.update(exceptions=[{"n": "abc", "report": "#1", "reason": "r"}]),
            "names no claim",
        ),
        (lambda data: data.update(exceptions=["#1"]), "is not a mapping"),
        (lambda data: data.update(lanes=["main"]), "is not a mapping"),
    ],
)
def test_malformed_input_is_a_problem_and_never_a_crash(edit: Any, expected: str) -> None:
    data = _minimal()
    edit(data)
    assert expected in " ".join(ledger.problems(data))


def test_claims_at_one_count_and_one_time_are_refused_rather_than_ordered_by_label() -> None:
    data = _minimal()
    second = copy.deepcopy(data["reports"][0])
    second.update(report="#2", url="https://github.com/jlevy/squares/issues/2")
    data["reports"].append(second)
    assert "#1 and #2 arrive at 2026-10-12T00:00:00Z" in " ".join(ledger.problems(data))
    # A claim with a time of its own, or at another count, is ordered by its time.
    second["claims"][0]["reported_at"] = "2026-10-12T00:00:01Z"
    assert ledger.problems(data) == []
    second["claims"][0].pop("reported_at")
    second["claims"][0]["n"] = 101
    assert ledger.problems(data) == []


def test_claims_of_one_instant_with_their_own_commit_times_are_ordered_by_them() -> None:
    """The commits of one push arrive together; each claim's ``first_committed`` orders
    them, so only a tie in both is refused (#795's review A, A1)."""
    data = _minimal()
    data["reports"][0]["claims"][0]["first_committed"] = "2026-10-11T23:00:00Z"
    second = copy.deepcopy(data["reports"][0])
    second.update(report="#0", url="https://github.com/jlevy/squares/issues/0")
    second["claims"][0]["first_committed"] = "2026-10-11T22:00:00Z"
    data["reports"].append(second)
    assert ledger.problems(data) == []
    second["claims"][0]["first_committed"] = "2026-10-11T23:00:00Z"
    assert "two first committed at 2026-10-11T23:00:00Z" in " ".join(ledger.problems(data))


def test_a_tie_in_time_with_one_unknown_commit_time_is_refused() -> None:
    """A tie in report time is ordered by commit only where every tied claim states its
    first commit: with one unknown, only the labels would order them, so the gate refuses
    it as before (#795's review B, B2)."""
    data = _minimal()
    data["reports"][0]["claims"][0]["first_committed"] = "2026-10-11T23:00:00Z"
    second = copy.deepcopy(data["reports"][0])
    second.update(report="#0", url="https://github.com/jlevy/squares/issues/0")
    del second["claims"][0]["first_committed"]
    data["reports"].append(second)
    assert "#0 and #1 arrive at 2026-10-12T00:00:00Z, so only their labels" in " ".join(
        ledger.problems(data)
    )


def test_one_instant_is_walked_in_commit_order_and_not_by_label() -> None:
    """A later commit of one push is decided against an earlier one, whatever their labels."""
    pushed = "2026-10-12T05:00:00Z"
    earlier = side("z@early", "10.4", when=pushed, first_committed="2026-10-12T01:00:00Z")
    later = side("a@late", "10.3", when=pushed, first_committed="2026-10-12T02:00:00Z")
    walk = ledger.walk(100, record(), [later, earlier])
    assert verdicts(walk) == [
        ("z@early", "recorded", "record T-001"),
        ("a@late", "recorded", "z@early"),
    ]


def test_a_malformed_start_is_refused_and_main_reports_one_line(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    data = _minimal()
    (tmp_path / ledger.LEDGER).write_text(yaml.safe_dump(data), encoding="utf-8")
    good = _starts()
    cases: list[tuple[Any, str]] = [
        ({**good, "format": "intake-ledger-starts-v1"}, "format intake-ledger-starts-v2"),
        ({**good, "counts": {"n": 100}}, "counts is not a list"),
        ({**good, "counts": [{"n": 100, "members": []}]}, "a start is never empty"),
        ({**good, "counts": [{"n": "abc", "members": []}]}, "without a positive n"),
        ({**good, "counts": [*good["counts"], good["counts"][0]]}, "listed twice"),
    ]
    missing = copy.deepcopy(good)
    missing["counts"][0]["members"][0].pop("open_low")
    cases.append((missing, "missing or mistyped ['open_low']"))
    short = copy.deepcopy(good)
    short["counts"][0]["members"][0]["lanes"][0].pop()
    cases.append((short, "a lane is [name, value, exact form, polynomial]"))
    unstated = copy.deepcopy(good)
    unstated["counts"][1]["members"][1].pop("stated")
    cases.append((unstated, "pending adoption: a pending entry states [value, slack]"))
    for starts, expected in cases:
        assert expected in " ".join(ledger.starts_problems(starts, FROZEN_AT))
    # The empty start would record the first claim against nothing; check refuses it.
    empty = {**good, "counts": [{"n": 100, "members": []}]}
    (tmp_path / ledger.STARTS).write_text(yaml.safe_dump(empty), encoding="utf-8")
    assert ledger.main(["check", str(tmp_path)]) == 1
    error = capsys.readouterr().err
    assert error.startswith("FAIL  check: starts.yaml n = 100: no members")
    assert error.count("\n") == 1
    (tmp_path / ledger.LEDGER).write_text(yaml.safe_dump({"format": "x"}), encoding="utf-8")
    assert ledger.main(["render", "--check", str(tmp_path)]) == 1
    assert "the ledger is missing" in capsys.readouterr().err


def test_a_publication_dependent_verdict_is_listed_with_its_alternative() -> None:
    data = _minimal()
    data["reports"][0]["claims"] = [{"n": 400, "printed": "19.99", "rounding": "exact"}]
    data["reports"].append(
        {
            "report": "owner/repo@abc1234",
            "url": "https://github.com/owner/repo/tree/abc1234",
            "kind": "publication",
            "holders": "B",
            "reported_at": "2026-10-11T00:00:00Z",
            "bead": "",
            "claims": [{"n": 400, "printed": "19.98", "rounding": "exact"}],
        }
    )
    verdict = ledger.evaluate(cast(ledger.Ledger, data), {400: [GRID_10]})
    changes = {
        item["report"]: item for item in verdict["owner_decisions"]["publication_dependent"]
    }
    assert changes["#1"]["with_publications"] == "not recorded"
    assert changes["#1"]["without_publications"] == "recorded"
    assert changes["owner/repo@abc1234"]["without_publications"] == ledger.NOT_IN_WALK


def test_render_reads_the_frozen_starts_and_never_the_tree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    data = _minimal()
    (tmp_path / ledger.LEDGER).write_text(yaml.safe_dump(data), encoding="utf-8")
    member = ledger.lane_member(
        100, "reported", {"value": "10.5", "exact_form": "21/2"}, ["T-1"]
    )
    starts = ledger.starts_document(data["read_at_main"], {100: [member]})
    (tmp_path / ledger.STARTS).write_text(yaml.safe_dump(starts), encoding="utf-8")

    def refuse(*_: object) -> None:
        raise AssertionError("render read the tree")

    monkeypatch.setattr(ledger, "tree_members", refuse)
    monkeypatch.setattr(ledger.view, "load_records", refuse)
    assert set(ledger.rendered(tmp_path)) == {ledger.VERDICTS, ledger.README}
    stale = {**starts, "read_at_main": "e" * 40}
    (tmp_path / ledger.STARTS).write_text(yaml.safe_dump(stale), encoding="utf-8")
    with pytest.raises(ledger.LedgerError, match="read at"):
        ledger.rendered(tmp_path)


def test_a_report_transcribing_two_claims_at_one_count_is_refused(tmp_path: Path) -> None:
    """#722's review A, A2: keyed by count, the second of two transcribed claims replaced
    the first unseen, so a commit stating two sides kept the last, not the least."""
    claims = [
        {"n": 450, "printed": "21.767428349991", "rounding": "up"},
        {"n": 451, "printed": "21.8", "rounding": "up"},
        {"n": 450, "printed": "21.767428349966", "rounding": "up"},
    ]
    sources = {
        "format": ledger.SOURCES_FORMAT,
        "read_at_main": "a" * 40,
        "read_on": "2026-10-22",
        "rule": "In order.",
        "lanes": [],
        "reports": [
            {
                "report": "owner/repo@abc1234",
                "url": "https://github.com/owner/repo/tree/abc1234",
                "reported_at": "2026-10-15T00:00:00Z",
                "holders": "Someone",
                "claims": claims,
            }
        ],
    }
    (tmp_path / ledger.SOURCES).write_text(yaml.safe_dump(sources), encoding="utf-8")
    snapshot = {"format": ledger.SNAPSHOT_FORMAT, "items": []}
    (tmp_path / ledger.SNAPSHOT).write_text(json.dumps(snapshot), encoding="utf-8")
    with pytest.raises(ledger.LedgerError, match=r"owner/repo@abc1234 .* n = \[450\]"):
        ledger.gather(tmp_path, snapshot=True)


def test_the_readme_links_lane_claims_only_where_a_copy_is_retained(
    tmp_path: Path,
) -> None:
    data = _minimal()
    (tmp_path / ledger.LEDGER).write_text(yaml.safe_dump(data), encoding="utf-8")
    member = ledger.lane_member(
        100, "reported", {"value": "10.5", "exact_form": "21/2"}, ["T-1"]
    )
    starts = ledger.starts_document(data["read_at_main"], {100: [member]})
    (tmp_path / ledger.STARTS).write_text(yaml.safe_dump(starts), encoding="utf-8")
    link = "[lane-claims/](lane-claims/README.md)"
    assert link not in ledger.rendered(tmp_path)[ledger.README]
    (tmp_path / ledger.LANE_CLAIMS).mkdir()
    assert link in ledger.rendered(tmp_path)[ledger.README]


def test_a_record_relation_that_reads_no_member_of_its_start_is_refused(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    # A relation decides only a comparison with a start member that prints what it read;
    # one naming another lane, value or register entry would decide nothing.
    member = ledger.lane_member(
        100, "reported", {"value": "10.5", "exact_form": "21/2"}, ["T-1"]
    )
    starts = ledger.starts_document(FROZEN_AT, {100: [member]})
    (tmp_path / ledger.STARTS).write_text(yaml.safe_dump(starts), encoding="utf-8")
    lane, value, form = member["lanes"][0][:3]
    live: ledger.RecordRelation = {
        "lane": lane,
        "relation": "below",
        "value": value,
        "exact_form": form,
        "read_from": "a receipt",
    }
    for relation, refused in (
        (live, False),
        (DECIDED, True),
        ({**live, "value": "10.6"}, True),
        ({**live, "lane": "verified"}, True),
    ):
        data = _minimal()
        data["reports"][0]["claims"][0]["record_relations"] = [relation]
        (tmp_path / ledger.LEDGER).write_text(yaml.safe_dump(data), encoding="utf-8")
        assert ledger.problems(data) == []
        assert ledger.main(["check", str(tmp_path)]) == int(refused)
        if not refused:
            assert set(ledger.rendered(tmp_path)) == {ledger.VERDICTS, ledger.README}
            continue
        error = capsys.readouterr().err
        assert error.startswith(
            f"FAIL  check: #1 n = 100: the record relation to {relation['lane']} at "
            f"{relation['value']!r} reads no member of the start"
        )
        with pytest.raises(ledger.LedgerError, match="reads no member of the start"):
            ledger.rendered(tmp_path)


FROZEN_AT = "f" * 40


def _starts() -> dict[str, Any]:
    """A start of every kind: a print and a root lane, an exact lane beside a pending
    entry, a beyond-horizon row and the grid."""
    reported = {"value": "1.41421356237309", "minimal_polynomial": "s^2 - 2 = 0"}
    verified = {
        "value": "1.4142135623730950488",
        "exact_form": "root(P, 1.4142135623730950488)",
    }
    texts = ledger.lane_polynomials(reported, verified)
    lanes = ledger.merged_lanes(
        ledger.lane_member(9, "reported", reported, ["T-009"], texts[0]),
        ledger.lane_member(9, "verified", verified, ["T-009"], texts[1]),
    )
    exact = ledger.lane_member(100, "reported", {"value": "10.5", "exact_form": "21/2"}, [])
    stated = check_standing.Stated(Fraction("10.40"), Fraction(1, 100))
    pending = ledger.pending_member({"id": "T-123"}, stated)
    row = {"n": 400, "source_id": "row-2026-10-11", "value": "19.990000000000"}
    members = {
        9: lanes,
        100: [exact, pending],
        400: [ledger.beyond_member(400, {400: row})],
        401: [ledger.beyond_member(401, {})],
    }
    return ledger.starts_document(FROZEN_AT, members)


def test_check_recomputes_every_start_span_and_refuses_one_edited_by_hand() -> None:
    starts = _starts()
    assert ledger.starts_problems(starts, FROZEN_AT) == []
    for n, index in ((9, 0), (9, 1), (100, 0), (100, 1), (400, 0), (401, 0)):
        edited = copy.deepcopy(starts)
        member = next(count for count in edited["counts"] if count["n"] == n)["members"][index]
        member["low"] = str(Fraction(member["low"]) - Fraction(1, 10**6))
        found = " ".join(ledger.starts_problems(edited, FROZEN_AT))
        assert f"n = {n} {member['label']}: frozen" in found
        assert "its stored inputs give" in found
    moved = copy.deepcopy(starts)
    moved["counts"][1]["members"][0]["lanes"][0][2] = "53/5"
    assert "its stored inputs give" in " ".join(ledger.starts_problems(moved, FROZEN_AT))


def test_a_beyond_horizon_start_reads_its_row_at_the_exact_side_its_source_states(
    tmp_path: Path,
) -> None:
    """A row whose source's claims record states the exact side is read at that side, kept
    as a lane the check recomputes, so a claim equal to it ties and one a fraction of the
    print's unit below it is recorded; a source that states none leaves the print."""
    side = Fraction(1999999999999993, 10**14)
    row = {"n": 400, "source_id": "row-2026-10-11", "value": "19.999999999999930"}
    record = tmp_path / "claims.json"
    record.write_text(json.dumps({"results": [{"n": 400, "exact_side": str(side)}]}), "utf-8")
    printed_only = tmp_path / "sources.json"
    printed_only.write_text(json.dumps({"sources": []}), "utf-8")
    coverage = {
        "sources": [
            {"id": "row-2026-10-11", "claims_record": str(record)},
            {"id": "row-2026-10-08", "claims_record": str(printed_only)},
        ]
    }
    rows = {400: row, 401: {"n": 401, "source_id": "row-2026-10-08", "value": "19.99"}}
    exact = ledger.beyond_exact_sides(coverage, rows)
    assert exact == {400: side}
    member = ledger.beyond_member(400, rows, exact)
    assert (member["model"], member["label"]) == ("exact", "beyond-horizon row row-2026-10-11")
    assert member["lanes"] == [[member["label"], row["value"], str(side), ""]]
    assert ledger.beyond_member(401, rows, exact)["model"] == "print"
    starts = ledger.starts_document(FROZEN_AT, {400: [member]})
    assert ledger.starts_problems(starts, FROZEN_AT) == []
    start = ledger.side_of(member)
    tie = ledger.Side("tie", "B", exact_span(side), "", side, "issue", exact=True)
    below = side - Fraction(1, 10**16)
    under = ledger.Side("under", "C", exact_span(below), "", below, "issue", exact=True)
    assert ledger.compare(tie, start) == ledger.EQUAL
    assert ledger.compare(under, start) == ledger.BELOW
    printed = ledger.side_of(ledger.beyond_member(400, rows))
    assert ledger.compare(tie, printed) == ledger.compare(under, printed) == ledger.UNDECIDED
    with pytest.raises(ledger.LedgerError, match="lies outside its print"):
        ledger.beyond_member(400, rows, {400: side + Fraction(1, 10**10)})


def test_a_row_s_exact_side_is_read_one_way_and_refused_where_its_record_is_unclear(
    tmp_path: Path,
) -> None:
    """The ledger's starts and the replay's rows read a row's exact side through one
    reader, `stated_exact_side`. A record kept as ``.gz`` reads the same, and a record
    that states no exact side at any count leaves the row to its print. A declared record
    that is missing, or that states exact sides but not exactly one at the count, is
    refused rather than read as the print (#742's review A, A3)."""
    side = Fraction(1999999999999993, 10**14)
    results = [{"n": 400, "exact_side": str(side)}, {"n": 402, "offered_side": "20"}]
    plain = tmp_path / "plain.json"
    plain.write_text(json.dumps({"results": results}), "utf-8")
    packed = gzip.compress(json.dumps({"results": results}).encode(), mtime=0)
    (tmp_path / "packed.json.gz").write_bytes(packed)
    printed_only = tmp_path / "sources.json"
    printed_only.write_text(json.dumps({"sources": []}), "utf-8")
    twice = tmp_path / "twice.json"
    twice.write_text(json.dumps({"results": [*results, results[0]]}), "utf-8")

    def source(name: str, path: Path | None) -> dict[str, str]:
        return {"id": name} if path is None else {"id": name, "claims_record": str(path)}

    assert ledger.stated_exact_side(source("plain", plain), 400) == side
    assert ledger.stated_exact_side(source("packed", tmp_path / "packed.json"), 400) == side
    assert ledger.stated_exact_side(source("printed", printed_only), 400) is None
    refused = {
        ("absent", tmp_path / "absent.json", 400): "its claims record .* does not exist",
        ("directory", tmp_path, 400): "is a directory",
        ("undeclared", None, 400): "declares no claims record",
        ("twice", twice, 400): "n=400: its claims record states no one exact side",
        ("plain", plain, 401): "n=401: its claims record states no one exact side",
        ("plain", plain, 402): "n=402: its claims record states no one exact side",
    }
    for (name, path, n), message in refused.items():
        with pytest.raises(ledger.LedgerError, match=message):
            ledger.stated_exact_side(source(name, path), n)
    coverage = {"sources": [source("plain", plain)]}
    with pytest.raises(ledger.LedgerError, match="unknown source"):
        ledger.beyond_exact_sides(coverage, {400: {"n": 400, "source_id": "gone"}})


def test_check_refuses_an_exact_beyond_horizon_start_moved_outside_its_print() -> None:
    """A start read at its row's exact side keeps that side as its lane. One whose side is
    edited to lie outside the row's print, with its span edited to match, is refused by
    ``check``, not only when ``gather`` freezes it (#742's review A, A3)."""
    side = Fraction(1999999999999993, 10**14)
    row = {"n": 400, "source_id": "row-2026-10-11", "value": "19.999999999999930"}
    member = ledger.beyond_member(400, {400: row}, {400: side})
    starts = ledger.starts_document(FROZEN_AT, {400: [member]})
    assert ledger.starts_problems(starts, FROZEN_AT) == []
    for moved_by in (Fraction(1, 10**10), -Fraction(1, 10**10)):
        moved = copy.deepcopy(starts)
        edited = moved["counts"][0]["members"][0]
        outside = side + moved_by
        edited["lanes"][0][2] = str(outside)
        edited["low"] = edited["high"] = str(outside)
        (problem,) = ledger.starts_problems(moved, FROZEN_AT)
        assert f"n = 400 {member['label']}" in problem
        assert "lies outside its print 19.999999999999930" in problem
    unreadable = copy.deepcopy(starts)
    unreadable["counts"][0]["members"][0]["lanes"][0][2] = "about 20"
    (problem,) = ledger.starts_problems(unreadable, FROZEN_AT)
    assert "not a number: 'about 20'" in problem


def test_gather_keeps_the_frozen_starts_and_reads_the_tree_only_to_refresh_them(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    read_at_main = "f" * 40
    sources = {
        "format": ledger.SOURCES_FORMAT,
        "read_at_main": read_at_main,
        "read_on": "2026-10-14",
        "rule": "the owner's rule",
        "lanes": [],
        "reports": [
            {
                "report": "owner/repo@abc1234",
                "url": "https://github.com/owner/repo/tree/abc1234",
                "reported_at": CLAIM_TIME,
                "holders": "A",
                "claims": [{"n": 100, "printed": "10.4", "rounding": "up", "exact": "52/5"}],
            }
        ],
    }
    (tmp_path / ledger.SOURCES).write_text(yaml.safe_dump(sources), encoding="utf-8")
    snapshot = {"format": ledger.SNAPSHOT_FORMAT, "items": []}
    (tmp_path / ledger.SNAPSHOT).write_text(json.dumps(snapshot), encoding="utf-8")
    member = ledger.lane_member(
        100, "reported", {"value": "10.5", "exact_form": "21/2"}, ["T-1"]
    )
    frozen = yaml.safe_dump(ledger.starts_document(read_at_main, {100: [member]}))
    (tmp_path / ledger.STARTS).write_text(frozen, encoding="utf-8")

    def refuse(*_: object, **__: object) -> None:
        raise AssertionError("gather read the tree")

    monkeypatch.setattr(ledger, "tree_members", refuse)
    assert ledger.gather(tmp_path, snapshot=True) == []
    assert (tmp_path / ledger.STARTS).read_text(encoding="utf-8") == frozen
    assert [report["report"] for report in ledger.load_ledger(tmp_path)["reports"]] == [
        "owner/repo@abc1234"
    ]
    with pytest.raises(AssertionError, match="read the tree"):
        ledger.gather(tmp_path, snapshot=True, refresh_starts=True)
    sources["reports"][0]["claims"][0]["n"] = 101
    (tmp_path / ledger.SOURCES).write_text(yaml.safe_dump(sources), encoding="utf-8")
    with pytest.raises(ledger.LedgerError, match=r"no start at n = \[101\]"):
        ledger.gather(tmp_path, snapshot=True)


def test_a_lane_print_of_unknown_rounding_is_refused() -> None:
    assert ledger.lane_rounding("binary64") == "binary64"
    with pytest.raises(ledger.LedgerError, match="unknown rounding 'None'"):
        ledger.lane_rounding("None")


def test_gather_reads_a_lane_record_by_path_and_never_a_commit(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # OR-18: the lane's commit is provenance. A packet the checkout lacks is read from the
    # copy under lane-claims/, and no git command runs.
    read_at_main = "f" * 40
    mapping = {"lane": "lane", "packet": "absent-packet-2026-10-14", "record": "claims.json"}
    sources = {
        "format": ledger.SOURCES_FORMAT,
        "read_at_main": read_at_main,
        "read_on": "2026-10-14",
        "rule": "the owner's rule",
        "lanes": [{"name": "lane", "branch": "a-branch", "commit": "a" * 40}],
        "reports": [
            {
                "report": "owner/repo@abc1234",
                "url": "https://github.com/owner/repo/tree/abc1234",
                "reported_at": CLAIM_TIME,
                "holders": "A",
                "lanes": [{**mapping, "all": True}],
            }
        ],
    }
    (tmp_path / ledger.SOURCES).write_text(yaml.safe_dump(sources), encoding="utf-8")
    snapshot = {"format": ledger.SNAPSHOT_FORMAT, "items": []}
    (tmp_path / ledger.SNAPSHOT).write_text(json.dumps(snapshot), encoding="utf-8")
    member = ledger.lane_member(
        100, "reported", {"value": "10.5", "exact_form": "21/2"}, ["T-1"]
    )
    starts = ledger.starts_document(read_at_main, {100: [member]})
    (tmp_path / ledger.STARTS).write_text(yaml.safe_dump(starts), encoding="utf-8")
    row = {
        "n": 100,
        "offered_side": "10.4",
        "exact_side": "52/5",
        "first_committed": "2026-10-11T00:00:00Z",
    }

    def refuse(*_: object, **__: object) -> None:
        raise AssertionError("gather ran a command")

    monkeypatch.setattr(ledger.subprocess, "run", refuse)
    with pytest.raises(ledger.LedgerError, match="in neither the checkout nor lane-claims"):
        ledger.gather(tmp_path, snapshot=True)
    copy_ = tmp_path / ledger.LANE_CLAIMS / "lane" / mapping["packet"] / "claims.json"
    copy_.parent.mkdir(parents=True)
    copy_.write_text(json.dumps({"results": [row]}), encoding="utf-8")
    assert ledger.gather(tmp_path, snapshot=True) == []
    claim = ledger.load_ledger(tmp_path)["reports"][0]["claims"][0]
    assert (claim.get("exact"), claim.get("exact_from")) == (
        "52/5",
        f"{ledger.record_path(mapping)} at a-branch@{'a' * 40}",
    )


def test_a_lane_row_no_report_takes_is_refused() -> None:
    taken = {"lane:packet/claims.json rows": {1, 2, 3}, "lane:packet/claims.json": {1, 3}}
    assert "rows [2]" in ledger.unclaimed_rows(taken)[0]
    taken["lane:packet/claims.json"].add(2)
    assert ledger.unclaimed_rows(taken) == []


@pytest.mark.parametrize(
    "directory",
    sorted(
        path
        for path in (ledger.ROOT / "campaign/issue-intake").glob("upper-bounds-*")
        if path.is_dir()
    ),
    ids=lambda directory: directory.name,
)
def test_render_check_passes_on_each_retained_ledger(directory: Path) -> None:
    assert ledger.problems(ledger.load_yaml(directory / ledger.LEDGER)) == []
    assert ledger.render(directory, check=True) == []


def test_16_october_ledger_records_issue_639s_sixteen_improvements() -> None:
    # Issue #639's exact sides against PR #574's rationals and the record on main e2e018f3.
    directory = ledger.ROOT / "campaign/issue-intake/upper-bounds-20261016"
    verdicts = json.loads((directory / ledger.VERDICTS).read_text("utf-8"))
    recorded = sorted(
        count["n"]
        for count in verdicts["counts"]
        for step in count["steps"]
        if step["report"] == "#639" and step["verdict"] == ledger.RECORDED
    )
    expected = "88 102 123 126 175 199 204 232 258 259 266 267 292 295 301 302"
    assert recorded == [int(n) for n in expected.split()]


def test_the_committed_ledger_decides_pr574_as_its_receipt_does() -> None:
    # The 17 comparisons decide_undecided_comparisons decided exactly are transcribed into
    # sources.yaml; each relation is the receipt's, and the verdict follows from it.
    directory = ledger.DEFAULT_DIRECTORY
    receipt = json.loads((directory / "undecided-resolved.json").read_text("utf-8"))
    (report,) = [
        item for item in ledger.load_ledger(directory)["reports"] if item["report"] == "PR #574"
    ]
    claims = {claim["n"]: claim for claim in report["claims"]}
    verdicts = json.loads((directory / ledger.VERDICTS).read_text("utf-8"))
    steps = {
        count["n"]: next(step for step in count["steps"] if step["report"] == "PR #574")
        for count in verdicts["counts"]
        if count["n"] in claims
    }
    for row in receipt["rows"]:
        n = row["n"]
        decided = [
            (item["relation"], item.get("margin"))
            for item in claims[n].get("record_relations", [])
            if "undecided-resolved.json" in item["read_from"]
        ]
        assert decided == [(row["relation"], row["margin"])], n
        assert (steps[n]["reason"], steps[n]["decided_against"]) == (
            row["relation"],
            [row["against"]],
        )
    undecided = [item["n"] for item in verdicts["owner_decisions"]["undecided"]]
    assert undecided == [item["n"] for item in receipt["gated"]] == [29, 55, 71, 83]


def test_refinements_render_with_their_packing_and_form_a_chain() -> None:
    data = _minimal()
    original: dict[str, Any] = {
        "n": 100,
        "printed": "10.4",
        "rounding": "exact",
        "refines": {"packing_of": "A. Finder", "entry": "T-001", "source": "the issue"},
    }
    data["reports"][0]["claims"] = [original]
    data["reports"].append(
        {
            "report": "#2",
            "url": "https://github.com/jlevy/squares/issues/2",
            "kind": "issue",
            "holders": "B",
            "reported_at": "2026-10-12T05:00:00Z",
            "bead": "",
            "claims": [
                {
                    "n": 100,
                    "printed": "10.39",
                    "rounding": "exact",
                    "refines": {"packing_of": "A. Finder", "entry": "#1", "source": "lane"},
                }
            ],
        }
    )
    data["reports"].append(
        {
            "report": "#3",
            "url": "https://github.com/jlevy/squares/issues/3",
            "kind": "issue",
            "holders": "C",
            "reported_at": "2026-10-12T06:00:00Z",
            "bead": "",
            "claims": [
                {
                    "n": 100,
                    "printed": "10.2",
                    "rounding": "exact",
                    "new_packing": {"source": "the issue", "continues": "B's arrangement"},
                }
            ],
        }
    )
    assert ledger.problems(data) == []
    verdict = ledger.evaluate(cast(ledger.Ledger, data), {100: [record()]})
    steps = verdict["counts"][0]["steps"]
    assert ledger.recorded_text(steps[0]) == (
        "recorded, a refinement of A. Finder's packing (T-001)"
    )
    assert ledger.recorded_text(steps[2]) == (
        "recorded (new packing, continuing B's arrangement)"
    )
    chain = verdict["owner_decisions"]["refinement_chains"]
    assert [item["report"] for item in chain[0]["refinements"]] == ["#1", "#2"]
    assert chain[0]["packing"] == "T-001"
    summary = verdict["summary"]
    assert (summary["recorded_refinement"], summary["recorded_new"]) == (2, 1)
    row = verdict["reports"][0]
    assert row["recorded_refinement"] == [
        {"n": 100, "packing_of": "A. Finder", "entry": "T-001"}
    ]
    both = copy.deepcopy(data)
    both["reports"][0]["claims"][0]["new_packing"] = {"source": "x"}
    assert "not both" in " ".join(ledger.problems(both))


#: The span a frozen start member stores, which `recomputed` gives again.
SPAN_KEYS = ("model", "low", "high", "open_low", "open_high")


def test_an_entry_that_holds_some_cases_still_joins_the_start_where_it_is_pending() -> None:
    """Pending adoption is read count by count: an entry that holds a case elsewhere, and
    so is the current best as a whole, still states a smaller bound pending adoption at
    another count, and that bound joins the count's start (T-193 at 88 and 126 on 31 October
    2026, where Polkovskyi's certificates lie above it). Every such bound on the tree is
    held to it."""
    from devtools import render_recent_results as view  # noqa: PLC0415

    records = view.load_records()
    wanted: dict[int, set[str]] = {}
    for result in records.register.results:
        if view.standing(result, records) == view.PENDING_ADOPTION:
            continue
        for finding in check_standing.improvements(result, records):
            if finding.direction == check_standing.UPPER and finding.n <= ledger.HORIZON:
                wanted.setdefault(finding.n, set()).add(
                    f"register {result['id']}, pending adoption"
                )
    # On 31 October 2026 T-193 held cases elsewhere and was pending at 88 and 126 (A11 of
    # the review of #852), so the check is not vacuous while think-ot5c stages them.
    assert {88, 126} <= set(wanted)
    members = ledger.tree_members(sorted(wanted))
    for n, labels in wanted.items():
        assert labels <= {member["label"] for member in members[n]}, n


def test_a_start_frozen_from_23_october_holds_goebel_s_construction_beyond_324(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Review A of #754, A2 (think-v022): a start `gather` freezes for a ledger read on or
    after 23 October 2026 holds Göbel's construction beside the beyond-horizon row or the
    grid, at every count whose side a build proves final, and refuses any other
    (think-llit). The member recomputes from the maintained module, reads as the walk's
    construction, and a classical ruling does not seed it twice. A start frozen earlier
    stays the grid alone."""
    (grid,) = ledger.tree_members([369], read_on="2026-10-22")[369]
    assert grid["label"] == "the grid"
    members = ledger.tree_members([369], read_on="2026-10-23")[369]
    assert [member["label"] for member in members] == ["the grid", ledger.GOEBEL_LABEL]
    goebel = members[1]
    assert goebel["kind"] == ledger.CONSTRUCTION
    assert ledger.recomputed(369, goebel) == [{key: goebel[key] for key in SPAN_KEYS}]
    assert (
        ledger.starts_problems(
            {
                "format": ledger.STARTS_FORMAT,
                "read_at_main": "x",
                "counts": [{"n": 369, "members": members}],
            },
            "x",
        )
        == []
    )
    edited = {**goebel, "high": str(Fraction(goebel["high"]) + 1)}
    assert (
        ledger.starts_problems(
            {
                "format": ledger.STARTS_FORMAT,
                "read_at_main": "x",
                "counts": [{"n": 369, "members": [grid, edited]}],
            },
            "x",
        )
        != []
    )
    side, expected = ledger.side_of(goebel), ledger.construction_side(369)
    assert expected is not None
    fields = ("label", "holders", "span", "shown", "value", "kind")
    assert [getattr(side, key) for key in fields] == [getattr(expected, key) for key in fields]
    start = [ledger.side_of(member) for member in members]
    assert [member.label for member in ledger.walk(369, start, [], rulings=RULED).start] == [
        ledger.GOEBEL_LABEL
    ]
    (_, far) = ledger.tree_members([1074], read_on="2026-10-23")[1074]
    assert ledger.recomputed(1074, far) == [{key: far[key] for key in SPAN_KEYS}]
    monkeypatch.setattr(goebel_construction, "MAX_BUILD", 1100)
    with pytest.raises(ledger.LedgerError, match="n = 1074: no build to 1100 proves"):
        ledger.tree_members([1074], read_on="2026-10-23")


def test_older_frozen_starts_recompute_their_grid_members_exactly() -> None:
    """Review A of #754, A2: every ledger read before 23 October 2026 keeps its frozen
    starts. Each grid member recomputes to its frozen span exactly, and none holds Göbel's
    construction; the history walk is the one read here."""
    directory = ledger.ROOT / "campaign/issue-intake/upper-bounds-couzo-history-20261022"
    assert str(yaml.safe_load((directory / "sources.yaml").read_text())["read_on"]) < (
        ledger.GOEBEL_FROM
    )
    starts = yaml.safe_load((directory / "starts.yaml").read_text(encoding="utf-8"))
    members = [
        (count["n"], member) for count in starts["counts"] for member in count["members"]
    ]
    grids = [(n, member) for n, member in members if member["label"] == "the grid"]
    assert len(grids) > 100
    for n, member in grids:
        assert ledger.recomputed(n, member) == [{key: member[key] for key in SPAN_KEYS}]
    assert not any(member["kind"] == ledger.CONSTRUCTION for _, member in members)


#: The owner's two rulings of 23 October 2026 as a ledger lists them (`Ruling`).
RESTATEMENT_RULING = {"ruling": "restatement", "decided": "2026-10-23", "bead": "think-fwa9"}
CLASSICAL_RULING = {
    "ruling": "classical-constructions",
    "decided": "2026-10-23",
    "bead": "think-8krd",
}
#: What a ledger that applies neither answer says instead (`NotApplied`).
NOT_APPLIED = [
    {"ruling": "restatement", "reason": "a test that walks the rule before the answer"},
    {"ruling": "classical-constructions", "reason": "a test that walks the grid alone"},
]


def _read_from_23_october() -> dict[str, Any]:
    """`_minimal`, read on the day of the owner's answers, with its claim at 369."""
    data = _minimal()
    data["read_on"] = ledger.GOEBEL_FROM
    data["reports"][0]["claims"] = [{"n": 369, "printed": "19.71", "rounding": "up"}]
    return data


def test_a_ledger_read_from_23_october_applies_both_answers_or_says_why() -> None:
    """Review B of #754, B1: from `GOEBEL_FROM` a ledger with claims beyond the horizon
    applies the restatement answer through its ruling, and Göbel's baseline through its
    ruling or a start member `gather` froze, at every such count. An answer it does not
    apply there is named under ``rulings_not_applied`` with the reason, or the check fails.
    A ledger read earlier, or with no claim beyond the horizon, is checked as before."""
    bare = _read_from_23_october()
    (restates,) = ledger.problems(bare)
    assert restates.startswith("read on 2026-10-23: the restatement answer is not applied")
    assert "at n = 369" in restates
    both = ledger.answer_problems(bare, [369], set())
    assert both[0] == restates
    assert both[1].startswith("read on 2026-10-23: Göbel's baseline is not applied")
    assert "no frozen start member" in both[1]
    # A start that holds Göbel's construction applies the baseline without the ruling.
    assert ledger.answer_problems(bare, [369], {369}) == [restates]
    ruled = {**bare, "rulings": [RESTATEMENT_RULING, CLASSICAL_RULING]}
    assert ledger.problems(ruled) == []
    assert ledger.answer_problems(ruled, [369], set()) == []
    short = {**bare, "rulings": [{**RESTATEMENT_RULING, "through": 368}, CLASSICAL_RULING]}
    (stops,) = ledger.answer_problems(short, [369], set())
    assert "restatement answer is not applied at n = 369" in stops
    said = {**bare, "rulings_not_applied": NOT_APPLIED}
    assert ledger.problems(said) == []
    assert ledger.answer_problems(said, [369], set()) == []
    malformed = {
        **bare,
        "rulings_not_applied": [
            {"ruling": "other", "reason": "why"},
            {"ruling": "restatement", "reason": " "},
            {"ruling": "restatement", "reason": "why"},
        ],
    }
    assert ledger.problems(malformed) == [
        "rulings_not_applied other: no such ruling",
        "rulings_not_applied restatement: states no reason",
        "rulings_not_applied restatement: listed twice",
    ]
    earlier = {**bare, "read_on": "2026-10-22"}
    assert ledger.answer_problems(earlier, [369], set()) == []
    inside = {**_minimal(), "read_on": ledger.GOEBEL_FROM}
    assert ledger.answer_problems(inside, [100], set()) == []


def test_check_refuses_a_ledger_read_from_23_october_that_applies_neither_answer(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Review B of #754, B1, the negative control: a ledger read on 23 October 2026 that
    lists neither ruling, over a start frozen without Göbel's construction, passed `check`
    and would have recorded a restatement and a side above Göbel's. It now fails until it
    applies both answers, its start holds the construction, or it says why not; the reasons
    then render in its README."""
    data = _read_from_23_october()
    grid = ledger.beyond_member(369, {})
    starts = ledger.starts_document(data["read_at_main"], {369: [grid]})

    def write(ledger_data: dict[str, Any], start: dict[str, Any]) -> None:
        (tmp_path / ledger.LEDGER).write_text(yaml.safe_dump(ledger_data), encoding="utf-8")
        (tmp_path / ledger.STARTS).write_text(yaml.safe_dump(start), encoding="utf-8")

    write(data, starts)
    assert ledger.main(["check", str(tmp_path)]) == 1
    assert "the restatement answer is not applied" in capsys.readouterr().err
    data["rulings"] = [RESTATEMENT_RULING]
    write(data, starts)
    assert ledger.main(["check", str(tmp_path)]) == 1
    assert "Göbel's baseline is not applied at n = 369" in capsys.readouterr().err
    with pytest.raises(ledger.LedgerError, match="Göbel's baseline is not applied"):
        ledger.rendered(tmp_path)
    held = ledger.starts_document(
        data["read_at_main"], {369: [grid, ledger.construction_member(369)]}
    )
    write(data, held)
    assert ledger.main(["check", str(tmp_path)]) == 0
    data["rulings"] = [RESTATEMENT_RULING, CLASSICAL_RULING]
    write(data, starts)
    assert ledger.main(["check", str(tmp_path)]) == 0
    data.pop("rulings")
    data["rulings_not_applied"] = NOT_APPLIED
    write(data, starts)
    assert ledger.main(["check", str(tmp_path)]) == 0
    readme = ledger.rendered(tmp_path)[ledger.README]
    for item in NOT_APPLIED:
        assert f"- **{item['ruling']}** is not applied here: {item['reason']}." in readme


def test_the_issue_732_walk_applies_goebel_s_baseline_through_its_ruling() -> None:
    """Review B of #754, B1: #732's walk, read on 23 October 2026, froze its starts before
    the rule, so none holds Göbel's construction. Its ``classical-constructions`` ruling
    through 1024 applies the baseline at every count it walks; without that ruling the
    check would fail. Every other walk was read earlier, or later with Göbel's construction
    frozen into its start at every count beyond the horizon."""
    directory = ledger.ROOT / "campaign/issue-intake/upper-bounds-issue732-20261023"
    data, starts = ledger.load_walk(directory)
    assert str(data["read_on"]) == ledger.GOEBEL_FROM
    counts = ledger.counts_of(data)
    held = ledger.construction_counts(starts)
    assert not held
    assert ledger.answer_problems(data, counts, held) == []
    without = {
        **data,
        "rulings": [
            item for item in data.get("rulings", []) if item["ruling"] != ledger.CLASSICAL
        ],
    }
    (found,) = ledger.answer_problems(without, counts, held)
    assert found.startswith("read on 2026-10-23: Göbel's baseline is not applied")
    others = [
        path
        for path in (ledger.ROOT / "campaign/issue-intake").glob("upper-bounds-*")
        if path != directory and (path / ledger.LEDGER).is_file()
    ]
    assert others
    for path in others:
        read_on = str(ledger.load_yaml(path / ledger.LEDGER)["read_on"])
        if read_on < ledger.GOEBEL_FROM:
            continue
        # A walk read later, as f1ceee4's of 24 October, froze Göbel's construction into
        # its start at every count it walks beyond the horizon.
        later, frozen = ledger.load_walk(path)
        beyond = {n for n in ledger.counts_of(later) if n > ledger.HORIZON}
        assert beyond <= ledger.construction_counts(frozen), path.name
        assert ledger.answer_problems(later, beyond, ledger.construction_counts(frozen)) == []


def test_tree_drift_reports_goebel_s_member_only_from_23_october(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Review B of #754, B2 and B3: `tree_drift` compares a frozen start with the one the
    tree gives on the ledger's day. At 369, where the tree's start is the grid, a start
    frozen as the grid has no drift for a ledger read on 22 October, and for one read on
    23 October the tree adds Göbel's construction. `check --tree` reports drift without
    failing, but fails where the tree gives no start, as at a count whose Göbel side no
    build proves final, from 23 October: 1074 with every build capped at 1100."""
    grid = ledger.beyond_member(369, {})
    starts = ledger.starts_document(FROZEN_AT, {369: [grid]})
    (tmp_path / ledger.STARTS).write_text(yaml.safe_dump(starts), encoding="utf-8")

    def read_on(day: str) -> None:
        sources = {"format": ledger.SOURCES_FORMAT, "read_at_main": FROZEN_AT, "read_on": day}
        (tmp_path / ledger.SOURCES).write_text(yaml.safe_dump(sources), encoding="utf-8")

    read_on("2026-10-22")
    assert ledger.tree_drift(tmp_path) == []
    read_on(ledger.GOEBEL_FROM)
    (drift,) = ledger.tree_drift(tmp_path)
    assert drift == (
        "n = 369: frozen the grid 20; on the tree the grid 20; "
        f"{ledger.GOEBEL_LABEL} 19.707106781187"
    )
    data = _read_from_23_october()
    data["read_at_main"] = FROZEN_AT
    data["rulings"] = [RESTATEMENT_RULING, CLASSICAL_RULING]
    (tmp_path / ledger.LEDGER).write_text(yaml.safe_dump(data), encoding="utf-8")
    assert ledger.main(["check", "--tree", str(tmp_path)]) == 0
    assert "1 counts where today's records give another start" in capsys.readouterr().out
    data["reports"][0]["claims"][0]["n"] = 1074
    (tmp_path / ledger.LEDGER).write_text(yaml.safe_dump(data), encoding="utf-8")
    beyond = ledger.starts_document(FROZEN_AT, {1074: [ledger.beyond_member(1074, {})]})
    (tmp_path / ledger.STARTS).write_text(yaml.safe_dump(beyond), encoding="utf-8")
    assert ledger.main(["check", str(tmp_path)]) == 0
    monkeypatch.setattr(goebel_construction, "MAX_BUILD", 1100)
    assert ledger.main(["check", "--tree", str(tmp_path)]) == 1
    assert "n = 1074: no build to 1100 proves" in capsys.readouterr().err


#: The walks whose ``ledger.yaml`` an offline gather does not reproduce, with the bead
#: that decides each: 14 October's read the pr574 packet's algebraic claims at a branch
#: commit whose later revision of that file gives other relations.
REGATHER_EXCEPTED = {"upper-bounds-20261014": "think-299t"}
WALK_DIRECTORIES = sorted(
    directory
    for directory in (ledger.ROOT / "campaign/issue-intake").iterdir()
    if (directory / "sources.yaml").is_file() and (directory / "github-issues.json").is_file()
)


@pytest.mark.parametrize(
    "directory",
    [
        pytest.param(
            directory,
            id=directory.name,
            marks=[pytest.mark.skip(reason=REGATHER_EXCEPTED[directory.name])]
            if directory.name in REGATHER_EXCEPTED
            else [],
        )
        for directory in WALK_DIRECTORIES
    ],
)
def test_each_walk_s_ledger_is_its_sources_gathered_offline(
    directory: Path, tmp_path: Path
) -> None:
    """``ledger.yaml`` is what ``gather --snapshot`` writes from the walk's ``sources.yaml``,
    ``starts.yaml`` and ``github-issues.json``, so an edit to a source without a regather,
    or to the ledger by hand, is refused (#789's review B, B7)."""
    copy_of = tmp_path / directory.name
    shutil.copytree(directory, copy_of)
    ledger.gather(copy_of, snapshot=True)
    assert (copy_of / "ledger.yaml").read_bytes() == (directory / "ledger.yaml").read_bytes()


def test_a_source_edited_without_a_regather_is_refused(tmp_path: Path) -> None:
    """Review B's B7 control: #763's side at 343 raised to 19, with its print, in
    ``sources.yaml`` gathers a ledger that differs from the retained one."""
    directory = ledger.ROOT / "campaign/issue-intake/upper-bounds-issue763-20261024"
    copy_of = tmp_path / directory.name
    shutil.copytree(directory, copy_of)
    sources = yaml.safe_load((copy_of / "sources.yaml").read_text(encoding="utf-8"))
    (claim,) = [
        claim
        for report in sources["reports"]
        if report["report"] == "#763"
        for claim in report["claims"]
        if claim["n"] == 343
    ]
    claim |= {"exact": "19", "printed": "19.000000000000"}
    (copy_of / "sources.yaml").write_text(
        yaml.safe_dump(sources, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )
    ledger.gather(copy_of, snapshot=True)
    assert (copy_of / "ledger.yaml").read_bytes() != (directory / "ledger.yaml").read_bytes()


def test_a_walk_past_the_summary_threshold_renders_a_summary_readme(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A walk of more than `SUMMARY_FROM` counts keeps its per-count table in ledger.json
    alone (think-llit, Gate Cost): its README keeps the tallies, each report, the rulings
    and the owner's lists. Every retained walk walks fewer counts, so each renders as it
    did; with the threshold under a walk's 23 counts, its README is the summary and its
    ledger.json is unchanged."""
    walks = sorted((ledger.ROOT / "campaign/issue-intake").glob("upper-bounds-*/ledger.json"))
    walked = [len(json.loads(path.read_text(encoding="utf-8"))["counts"]) for path in walks]
    assert max(walked) == 392 <= ledger.SUMMARY_FROM
    directory = ledger.ROOT / "campaign/issue-intake/upper-bounds-20261016"
    full = ledger.rendered(directory)
    monkeypatch.setattr(ledger, "SUMMARY_FROM", 22)
    summary = ledger.rendered(directory)
    assert summary[ledger.VERDICTS] == full[ledger.VERDICTS]
    text = summary[ledger.README]
    assert "| n | Record on main | Reports in order | Best now |" not in text
    assert "This walk reaches 23 counts, more than 22, so this README is a summary" in text
    for kept in ("## Counts", "## Per Report", "## Owner Decisions"):
        assert kept in text
    assert len(text) < len(full[ledger.README])
