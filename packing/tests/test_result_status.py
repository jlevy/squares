"""A result's status is derived from the record, one word a result, and never stored.

`devtools.result_status` reads the workflow step a result has reached from its
confirmation rung, and calls it incomplete where the record holds an open defect against
it (epistemics.md, Status). These tests hold each predicate to a synthetic record, the
live register to the vocabulary, and the one hand-recorded fact, an entry's `activity`,
to its fields, its link and its age.
"""

from __future__ import annotations

import dataclasses
from collections import Counter
from typing import Any

import pytest

from devtools import (
    check_results,
    check_standing,
    render_recent_results,
    render_results,
    result_status,
)
from devtools.result_status import (
    ACTIVITY_MAX_AGE,
    CONFIRMED,
    INCOMPLETE,
    RECORDED,
    REVIEWED,
    STATUSES,
    activity_label,
    activity_problems,
    latest_review,
    open_issues,
    status,
    status_line,
)
from sqpack.yamlio import safe_load

Record = dict[str, Any]


def record(confirmation: str, *evidence: str, **more: Any) -> Record:
    return {"id": "T-999", "confirmation": confirmation, "evidence": list(evidence), **more}


def review(verdict: str, dated: str) -> Record:
    return {"path": "docs/review.md", "verdict": verdict, "date": dated}


READ = {"external_review": {"state": "informally-verified", "date": "2026-09-28"}}
DEFECT = {"external_review": {"state": "defect-found", "date": "2026-09-29"}}
PASSED = {"replay_status": "passed", "origin": "replayed-here"}
FAILED = {"replay_status": "failed", "origin": "replayed-here"}
EVIDENCE = {
    "E-report": {},
    "E-read": READ,
    "E-defect": DEFECT,
    "E-replay": PASSED,
    "E-failed": FAILED,
}


@pytest.mark.parametrize(
    ("confirmation", "expected"),
    [
        ("C0", RECORDED),
        ("C1", REVIEWED),
        ("C2", CONFIRMED),
        ("C3", CONFIRMED),
        ("C4", CONFIRMED),
        ("C5", CONFIRMED),
    ],
)
def test_a_status_is_the_confirmation_rung_in_one_word(
    confirmation: str, expected: str
) -> None:
    assert status(record(confirmation, "E-report"), EVIDENCE) == expected
    assert open_issues(record(confirmation, "E-report"), EVIDENCE) == []


def test_a_defect_a_read_found_makes_a_result_incomplete_until_a_replay_passes() -> None:
    """A read that found a defect leaves the result incomplete while it stands below
    `C2`. Once a replay here has passed, that replay is the defect's disposition."""
    for confirmation in ("C0", "C1"):
        entry = record(confirmation, "E-defect")
        (reason,) = open_issues(entry, EVIDENCE)
        assert "E-defect" in reason
        assert "2026-09-29" in reason
        assert status(entry, EVIDENCE) == INCOMPLETE
    replayed = record("C3", "E-defect", "E-replay")
    assert open_issues(replayed, EVIDENCE) == []
    assert status(replayed, EVIDENCE) == CONFIRMED
    # A read that found nothing wrong is a review and no defect.
    assert status(record("C1", "E-read"), EVIDENCE) == REVIEWED


@pytest.mark.parametrize("verdict", ["defect-open", "refuted"])
def test_an_open_review_verdict_makes_a_result_incomplete_whatever_its_rung(
    verdict: str,
) -> None:
    """The latest review decides: an earlier defect that a later review resolved is
    closed, and an accepted result that a later review reopens is incomplete again."""
    reopened = record(
        "C3",
        "E-replay",
        reviews=[review("accepted", "2026-09-20"), review(verdict, "2026-09-30")],
    )
    (reason,) = open_issues(reopened, EVIDENCE)
    assert verdict in reason
    assert status(reopened, EVIDENCE) == INCOMPLETE
    resolved = record(
        "C3",
        "E-replay",
        reviews=[review(verdict, "2026-09-20"), review("defects-resolved", "2026-09-30")],
    )
    assert status(resolved, EVIDENCE) == CONFIRMED


def test_of_reviews_on_one_day_the_one_listed_last_decides() -> None:
    """A review and the check of its fixes can share a date, as T-098's did on
    2026-10-06; the list is in the order they were written, so the later one decides
    whichever way it goes."""
    same_day = "2026-10-06"
    resolved = record(
        "C3",
        "E-replay",
        reviews=[review("defect-open", same_day), review("defects-resolved", same_day)],
    )
    assert status(resolved, EVIDENCE) == CONFIRMED
    reopened = record(
        "C3",
        "E-replay",
        reviews=[review("accepted", same_day), review("defect-open", same_day)],
    )
    assert status(reopened, EVIDENCE) == INCOMPLETE
    assert latest_review([]) is None


def test_a_failed_replay_makes_a_result_incomplete() -> None:
    failed = record("C3", "E-replay", "E-failed")
    assert open_issues(failed, EVIDENCE) == ["the replay of E-failed failed"]
    assert status(failed, EVIDENCE) == INCOMPLETE


def test_incomplete_wins_and_every_reason_is_kept() -> None:
    entry = record("C1", "E-defect", "E-failed", reviews=[review("refuted", "2026-09-30")])
    assert len(open_issues(entry, EVIDENCE)) == 3
    assert status(entry, EVIDENCE) == INCOMPLETE


def test_every_registered_result_has_exactly_one_status_from_the_record() -> None:
    """The live register: each result's status is one of the four, the first three are
    exactly its confirmation rung, and an incomplete one names the fact that makes it
    so. `RESULTS.md` prints the same word, with the marks beside it."""
    records = render_recent_results.load_records()
    evidence = records.register.evidence
    held = Counter()
    rendered = render_results.render()
    for entry in records.register.results:
        word = status(entry, evidence)
        held[word] += 1
        assert word in STATUSES, entry["id"]
        rank = int(str(entry["confirmation"])[1])
        if word == INCOMPLETE:
            assert open_issues(entry, evidence), entry["id"]
        else:
            assert word == (CONFIRMED if rank >= 2 else REVIEWED if rank == 1 else RECORDED)
            assert open_issues(entry, evidence) == [], entry["id"]
        marks = render_recent_results.position_marks(
            entry, render_recent_results.standing(entry, records), records
        )
        line = status_line(
            entry, evidence, marks, how=render_results.confirmed_how(entry, evidence)
        )
        assert line.startswith(word), entry["id"]
        row = next(row for row in rendered.splitlines() if row.startswith(f"| {entry['id']} "))
        assert f"| {line} |" in row, entry["id"]
    assert sum(held.values()) == len(records.register.results)
    assert result_status.counts() == {name: held[name] for name in STATUSES}
    # Every project result is confirmed from the day it is registered.
    for entry in records.register.results:
        if not entry.get("attribution"):
            assert status(entry, evidence) == CONFIRMED, entry["id"]


def test_a_status_line_is_the_status_then_the_activity_then_the_place() -> None:
    entry = record(
        "C0",
        "E-report",
        activity={"state": "waiting", "party": "third-party"},
    )
    assert status_line(entry, EVIDENCE) == "recorded, waiting on third party"
    assert status_line(entry, EVIDENCE, ["superseded"]) == (
        "recorded, waiting on third party, superseded"
    )
    assert status_line(record("C3", "E-replay"), EVIDENCE, ["superseded"]) == (
        "confirmed, superseded"
    )
    assert activity_label({"state": "in-analysis"}) == "in analysis"
    assert activity_label({"state": "waiting", "party": "source"}) == "waiting on source"
    assert activity_label(None) == ""


def test_superseded_is_marked_on_a_bound_and_where_a_later_result_is_declared() -> None:
    """Of a standing a table draws one mark, `superseded`, on a result whose kind is a
    bound. That a bound is only reported is the status; a second proof of a held value
    is the kind simplification; and a result that is no bound is not superseded by its
    standing, though it may cite a bound's evidence and so derive it. Such a result is
    marked only where its entry declares a later result that implies it
    (`superseded_by`): `superseded` for the whole of it, `superseded in part` for some,
    which keeps it current (think-nlo0). Every mark names what supersedes it."""
    view = render_recent_results
    bound = {"kind": "lower-bound"}
    for held in (view.HOLDS, view.HOLDS_REPORTED, view.NO_STANDING):
        assert not view.superseded(bound, held), held
    for held in (view.SECOND_CERTIFICATE, view.SECOND_CERTIFICATE_REPORTED):
        assert not view.superseded({"kind": "simplification"}, held), held
    for kind in check_results.KINDS:
        marked = view.superseded({"kind": kind}, view.SUPERSEDED)
        assert marked is (kind in check_results.BOUND_KINDS), kind
    records = view.load_records()

    def declared(extent: str) -> Record:
        later = {"result": "T-060", "extent": extent, "what": "The bound."}
        return {"kind": "case-exclusion", "superseded_by": [later]}

    for held in (view.NO_STANDING, view.SUPERSEDED):
        assert view.superseded(declared("whole"), held), held
        assert not view.superseded(declared("part"), held), held
        assert view.position_marks(declared("whole"), held, records) == ["superseded by T-060"]
        assert view.position_marks(declared("part"), held, records) == [
            "superseded in part by T-060"
        ]
    # The live register: the limit of a method derives the standing and is not marked.
    limit = records.results["T-003"]
    assert limit["kind"] == "method-limit"
    assert view.standing(limit, records) == view.SUPERSEDED
    assert view.position_marks(limit, view.SUPERSEDED, records) == []
    marked = [
        str(entry["id"])
        for entry in records.register.results
        if view.superseded(entry, view.standing(entry, records))
    ]
    derived = [
        entry for entry in marked if records.results[entry]["kind"] in check_results.BOUND_KINDS
    ]
    # Thirty since 2026-10-02, when wand125's replayed rectangle certificates (T-045,
    # T-070) superseded T-030 at n = 18, T-020 at n = 19, T-021 at n = 20 and T-047 at
    # n = 26 and 29, the last counts each of them held; thirty-one later that day, when
    # the 1 October replays (T-074) beat wand125's point certificates (T-044) at the last
    # of their counts; thirty-two since 3 October, when squarepacker's rescaling (T-078)
    # superseded Daniel's s(12) >= 15680/3951 (T-049); thirty-three since the merge of the
    # same day, when the replays recorded in parallel (T-063, T-069) beat Bašić and
    # Slivková's piercing bound (T-087) at both of its counts; thirty-four since 5 October,
    # when R071's replay (T-093) superseded R068 (T-043) at n = 17; thirty-five later that
    # day, when wand125's n = 84 certificate of 5 October (T-094), decided here by
    # sqverify-fast, superseded T-071 at the last count it held; thirty-seven with
    # wand125's mixed certificate on a declared net (T-096), which took n = 18 from both
    # of its rectangle entries, the replay T-045 and the report T-046; thirty-eight when
    # squarepacker's v1.1 (T-095) took n = 12's reported lower bound from T-078, and
    # thirty-nine when its replays took the verified one from T-079 the same day; forty
    # on 6 October, when the evening certificates of 4 October (T-091), decided the same
    # way as T-094, superseded T-072 at n = 76, its one count; forty-two when Evan
    # Daniel's exact optima (T-098) took the last counts of Couzo's first certificates
    # (T-057) and his second (T-092), the first upper bounds here to be superseded;
    # forty-three when wand125's certificate on a finer declared net (T-099) took n = 18,
    # the one count T-096 held; forty-five when Evan Daniel's exact certificates of the
    # catalogue's packings (T-101) took the verified ceilings at n = 69, 83 and 87 from the
    # certificates of their pictures (T-088, T-089); forty-six when wand125's check2
    # certificate at n = 20 (T-104) took both of that count's lanes, the last T-077 held;
    # forty-eight when the check2 certificates of n = 18 and 19 (T-102, T-103) took both
    # lanes there from T-099 and T-100, the one count each held; forty-nine when wand125's
    # mixed certificate of 3 October for n = 52 (T-082), decided here by sqverify-fast,
    # took the last count T-070 held; fifty when T-117's exact rational refinements
    # took n = 105 and 292, the last verified ceilings T-056 held.
    # T-120..T-123 report exact side forms for historical source configurations; no
    # current frontier lane relies on these unverified catalogue assertions.
    assert {"T-120", "T-121", "T-122", "T-123"} <= set(derived)
    # Gupta's confirmed fourteen-case refinement supersedes T-114's final ceiling.
    expected = {
        "T-001",
        "T-002",
        "T-010",
        "T-015",
        "T-016",
        "T-017",
        "T-018",
        "T-019",
        "T-020",
        "T-021",
        "T-022",
        "T-024",
        "T-025",
        "T-026",
        "T-027",
        "T-028",
        "T-029",
        "T-030",
        "T-032",
        "T-033",
        "T-034",
        "T-037",
        "T-038",
        "T-039",
        "T-040",
        "T-041",
        "T-042",
        "T-043",
        "T-044",
        "T-045",
        "T-046",
        "T-047",
        "T-049",
        "T-050",
        "T-056",
        "T-057",
        "T-061",
        "T-070",
        "T-071",
        "T-072",
        "T-077",
        "T-078",
        "T-079",
        "T-087",
        "T-088",
        "T-089",
        "T-092",
        "T-096",
        "T-099",
        "T-100",
        "T-114",
        "T-120",
        "T-121",
        "T-122",
        "T-123",
        "T-129",
    }
    # Couzo's eight-case source report of 8 October (T-128) holds no case lane either,
    # but every side it states is below the ceiling its case holds: nothing has replaced
    # it, so it is pending adoption and carries no mark (think-h0d1).
    assert "T-128" not in marked
    assert view.standing(records.results["T-128"], records) == view.PENDING_ADOPTION
    assert set(derived) == expected
    assert len(derived) == len(expected)
    assert {
        "T-020", "T-021", "T-030", "T-043", "T-044", "T-047", "T-049", "T-057", "T-072",
        "T-056", "T-078", "T-079", "T-087", "T-088", "T-089", "T-092",
    } <= set(derived)  # fmt: skip
    assert view.position_marks(records.results["T-088"], view.SUPERSEDED, records) == [
        "superseded by T-101"
    ]
    assert {str(records.results[entry]["kind"]) for entry in derived} == {
        "lower-bound",
        "upper-bound",
    }
    # A result of another kind is marked only where its entry declares the whole of it
    # implied, and in part where it declares a part (think-rl2b).
    assert [entry for entry in marked if entry not in derived] == ["T-031"]
    in_part = [
        str(entry["id"])
        for entry in records.register.results
        if any(item["extent"] == "part" for item in entry.get("superseded_by") or [])
    ]
    assert in_part == ["T-023", "T-036"]
    # Each superseded bound names the results its cases' bounds rest on now.
    for entry in derived:
        by = view.superseding(records.results[entry], records)
        assert by, entry
        assert entry not in by, entry
    assert view.superseding(records.results["T-037"], records) == ("T-060",)
    # T-019's counts are held now by R071's replay at n = 17 (T-093) and by wand125's
    # check2 certificates of 6 October at n = 18 and 19 (T-102, T-103), which took both
    # lanes there from T-099 and T-100 the same day.
    assert view.position_marks(records.results["T-019"], view.SUPERSEDED, records) == [
        "superseded by T-093, T-102 and T-103"
    ]
    # Only a bound supersedes: at n = 13 and 46 a correction and an audit carry the
    # lower bound's evidence beside the optimality results that hold it.
    for n, other in ((13, "T-005"), (46, "T-004")):
        assert other in view.held(n, records).lower_holders
        assert records.results[other]["kind"] not in check_results.BOUND_KINDS
    lower = {"id": "T-999", "kind": "lower-bound", "scope": {"n_values": [13, 46]}}
    assert view.superseding(lower, records) == ("T-006", "T-008")
    # An exact value is superseded by a proof, never by a construction: Trump's packing,
    # T-011, holds n = 11's upper bound and supersedes no proof of s(11).
    assert view.held(11, records).upper_holders == {"T-011"}
    exact = {"id": "T-999", "kind": "optimality", "scope": {"n_values": [11]}}
    assert view.superseding(exact, records) == ("T-060",)
    upper = {"id": "T-999", "kind": "upper-bound", "scope": {"n_values": [11]}}
    assert view.superseding(upper, records) == ("T-011",)
    # T-060 implies T-036's bound and T-112 its equality case (think-7df0, think-d1bd);
    # T-060 implies T-023's exclusion and not its count of the branch, and the whole of
    # T-031's exclusion, since no packing of eleven squares fits at side 96/25
    # (think-rl2b).
    expected = {
        "T-036": ["superseded in part by T-060 and T-112"],
        "T-023": ["superseded in part by T-060"],
        "T-031": ["superseded by T-060"],
    }
    for entry, marks in expected.items():
        record = records.results[entry]
        assert view.position_marks(record, view.standing(record, records), records) == marks


def test_a_superseding_report_is_named_as_one() -> None:
    """A result no replay has confirmed holds a case's reported bound and never its
    verified one, so where it supersedes an entry the mark says so after its id. Until
    T-082's replays raised it to C3 on 6 October, T-044's mark named it, a report at C1,
    beside the confirmed results; no live mark names a report since, so the rule is held
    on the register with T-082 put back at C1."""
    view = render_recent_results
    records = view.load_records()
    record = records.results["T-044"]
    (mark,) = view.supersessions(record, view.standing(record, records), records)
    assert "T-082" in mark.by
    assert mark.reported == frozenset()
    assert "(reported)" not in mark.words()
    reported = {**records.results["T-082"], "confirmation": "C1"}
    before = dataclasses.replace(records, results={**records.results, "T-082": reported})
    (mark,) = view.supersessions(record, view.standing(record, before), before)
    assert mark.reported == {
        result for result in mark.by if before.results[result]["confirmation"] in ("C0", "C1")
    }
    assert mark.reported == {"T-082"}
    assert "T-082 (reported)" in mark.words()
    assert "T-070 (reported)" not in mark.words()
    for entry in ("T-019", "T-037"):
        other = records.results[entry]
        marks = view.position_marks(other, view.standing(other, records), records)
        assert marks
        assert all("(reported)" not in words for words in marks), entry


def stating(records: Any, sides: dict[int, str], **changes: Any) -> Record:
    """T-128, a source-only report at C0, stating `sides` as its claim and cut to them."""
    claim = ", ".join(f"s({n}) <= {side}" for n, side in sides.items())
    entry = {**records.results["T-128"], "claim": f"Reported {claim}."}
    return {**entry, "scope": {"n_values": list(sides)}, **changes}


def test_a_bound_better_than_its_cases_hold_is_pending_adoption_not_superseded() -> None:
    """Superseded means replaced. A bound no case bound rests on is superseded where its
    cases hold one at least as good as each it states, and named by the results that hold
    them; where one it states is strictly better, nothing has replaced it, and it is
    pending adoption, with no mark. Until 9 October T-128, eight sides below every ceiling
    its cases hold, read "superseded by T-098, T-115, T-125 and T-127" (think-h0d1)."""
    view = render_recent_results
    records = view.load_records()
    evidence = records.register.evidence
    entry = records.results["T-128"]
    assert view.standing(entry, records) == view.PENDING_ADOPTION
    assert not view.superseded(entry, view.PENDING_ADOPTION)
    assert view.position_marks(entry, view.PENDING_ADOPTION, records) == []
    assert status_line(entry, evidence) == RECORDED
    row = next(
        row for row in render_results.render().splitlines() if row.startswith("| T-128 ")
    )
    assert f"| {RECORDED} |" in row
    assert "superseded" not in row
    assert [finding.n for finding in check_standing.improvements(entry, records)] == [
        105, 108, 127, 131, 155, 180, 228, 306,
    ]  # fmt: skip
    # A dated report above the ceilings its cases hold is superseded, by their holder:
    # the earlier n = 105 source ceiling, and n = 108's one unit of the last place up.
    worse = stating(
        records,
        {105: "10.80607786551970463257490535044771520398745274", 108: "10.9048247851109050"},
    )
    assert view.standing(worse, records) == view.SUPERSEDED
    assert view.position_marks(worse, view.SUPERSEDED, records) == ["superseded by T-125"]
    # A tie is no improvement: the case holds that value under T-125's citation.
    tie = stating(records, {105: "10.7906765754107907"})
    assert view.standing(tie, records) == view.SUPERSEDED
    # Better at one count and beaten at another: pending adoption as a whole, as a result
    # that holds one case of several stands; superseded on the beaten case alone.
    mixed = stating(records, {105: "10.790618268107144505815379335866", 108: "10.95"})
    assert view.standing(mixed, records) == view.PENDING_ADOPTION
    assert view.position_marks(mixed, view.PENDING_ADOPTION, records) == []
    alone = {**mixed, "scope": {"n_values": [108]}}
    assert view.standing(alone, records) == view.SUPERSEDED
    assert view.position_marks(alone, view.SUPERSEDED, records) == ["superseded by T-125"]
    assert view.standing({**mixed, "scope": {"n_values": [105]}}, records) == (
        view.PENDING_ADOPTION
    )
    # A result a case bound rests on holds it, whatever its words state.
    held = records.results["T-125"]
    assert view.standing(held, records) == view.HOLDS
    assert view.standing({**held, "claim": "Reported s(105) <= 10.79."}, records) == view.HOLDS
    # Two lanes are never mixed: a report can hold only the reported lane, so a reported
    # ceiling below its side replaces it there, while a replayed result improves on the
    # verified ceiling it is below.
    case = records.cases[105]
    lower = {**case["reported_upper_bound"], "value": "10.79", "exact_form": "1079/100"}
    split = dataclasses.replace(
        records, cases={**records.cases, 105: {**case, "reported_upper_bound": lower}}
    )
    report = stating(records, {105: "10.790618268107144505815379335866"})
    assert view.standing(report, split) == view.SUPERSEDED
    assert view.standing({**report, "confirmation": "C3"}, split) == view.PENDING_ADOPTION


def activity(**changes: Any) -> Record:
    entry: Record = {
        "state": "in-analysis",
        "what": "The complete replay.",
        "since": "2026-09-29",
        "link": "think-20mv",
    }
    entry.update(changes)
    return {key: value for key, value in entry.items() if value is not None}


def problems(entry: Record | None, reviewed: str = "2026-10-01") -> list[str]:
    return activity_problems({"id": "T-999", "activity": entry}, reviewed)


def test_an_activity_is_held_to_its_fields_its_link_and_its_age() -> None:
    assert problems(None) == []
    assert problems(activity()) == []
    assert problems(activity(state="waiting", party="source")) == []
    for link in (
        "https://github.com/jlevy/squares/issues/247",
        "https://github.com/jlevy/squares/pull/267",
        "https://github.com/jlevy/squares/tree/claude/replay-wand125-n50-l740-local",
        "packing/frontier/results.yaml",
    ):
        assert problems(activity(link=link)) == [], link

    def one(entry: Record, reviewed: str = "2026-10-01") -> str:
        (problem,) = problems(entry, reviewed)
        return problem

    assert "activity.state" in one(activity(state="queued"))
    assert "names who" in one(activity(state="waiting"))
    assert "names who" in one(activity(state="waiting", party="wand125"))
    assert "names no party" in one(activity(party="source"))
    assert "activity.what is required" in one(activity(what=" "))
    assert "activity.link is required" in one(activity(link=None))
    assert "is not a bead" in one(activity(link="see the notes"))
    assert "is not a bead" in one(activity(link="packing/frontier/no-such-file.yaml"))
    assert "is not a bead" in one(activity(link="../outside.md"))
    assert "not a calendar date" in one(activity(since="September"))
    assert "after the register's last_reviewed" in one(activity(since="2026-10-02"))


def test_an_activity_expires() -> None:
    """One dated more than `ACTIVITY_MAX_AGE` days before the register's last review is
    refused, so "in analysis" cannot outlive the work unremarked. The age is read from
    the register's own date and never the clock."""
    assert ACTIVITY_MAX_AGE == 30
    assert problems(activity(since="2026-09-29"), "2026-10-29") == []
    (stale,) = problems(activity(since="2026-09-29"), "2026-10-30")
    assert "31 days old" in stale
    assert "re-date it" in stale


def test_the_registers_activities_pass_and_the_schema_knows_the_field() -> None:
    register = safe_load(check_results.RESULTS.read_text(encoding="utf-8"))
    carrying = [entry for entry in register["results"] if entry.get("activity")]
    for entry in carrying:
        assert activity_problems(entry, str(register["last_reviewed"])) == [], entry["id"]
        assert entry["activity"]["state"] in result_status.ACTIVITY_STATES
    schema = safe_load(
        (check_results.FRONTIER / "results.schema.yaml").read_text(encoding="utf-8")
    )
    field = schema["$defs"]["result"]["properties"]["activity"]
    assert field["properties"]["state"]["enum"] == list(result_status.ACTIVITY_STATES)
    assert field["properties"]["party"]["enum"] == list(result_status.PARTIES)
    assert "activity" not in schema["$defs"]["result"]["required"]
    assert check_results.main() == 0
