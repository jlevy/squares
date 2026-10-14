"""The owner's report-order rule, on synthetic counts, and the committed 2026-10-14 ledger."""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, cast

import pytest
import yaml

from devtools import check_standing
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


def test_check_holds_the_schema_the_prints_and_the_times() -> None:
    assert ledger.problems(_minimal()) == []
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


def test_render_check_passes_on_the_committed_ledger() -> None:
    assert ledger.problems(ledger.load_yaml(ledger.DEFAULT_DIRECTORY / ledger.LEDGER)) == []
    assert ledger.render(ledger.DEFAULT_DIRECTORY, check=True) == []


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
