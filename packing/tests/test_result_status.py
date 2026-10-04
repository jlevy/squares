"""A result's status is derived from the record, one word a result, and never stored.

`devtools.result_status` reads the workflow step a result has reached from its
confirmation rung, and calls it incomplete where the record holds an open defect against
it (epistemics.md, Status). These tests hold each predicate to a synthetic record, the
live register to the vocabulary, and the one hand-recorded fact, an entry's `activity`,
to its fields, its link and its age.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

import pytest

from devtools import check_results, render_recent_results, render_results, result_status
from devtools.result_status import (
    ACTIVITY_MAX_AGE,
    CONFIRMED,
    INCOMPLETE,
    RECORDED,
    REVIEWED,
    STATUSES,
    activity_label,
    activity_problems,
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
            entry, render_recent_results.standing(entry, records)
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


def test_superseded_is_marked_on_a_bound_and_on_nothing_else() -> None:
    """Of a standing a table draws one mark, `superseded`, and only on a result whose
    kind is a bound. That a bound is only reported is the status; a second proof of a
    held value is the kind simplification; and a result that is no bound is never
    superseded, though it may cite a bound's evidence and so derive the standing."""
    view = render_recent_results
    bound = {"kind": "lower-bound"}
    for held in (view.HOLDS, view.HOLDS_REPORTED, view.NO_STANDING):
        assert view.position_marks(bound, held) == [], held
    for held in (view.SECOND_CERTIFICATE, view.SECOND_CERTIFICATE_REPORTED):
        assert view.position_marks({"kind": "simplification"}, held) == [], held
    for kind in check_results.KINDS:
        marked = view.position_marks({"kind": kind}, view.SUPERSEDED)
        assert marked == (["superseded"] if kind in check_results.BOUND_KINDS else []), kind
        assert view.superseded({"kind": kind}, view.SUPERSEDED) is bool(marked), kind
    # The live register: the limit of a method derives the standing and is not marked.
    records = view.load_records()
    limit = records.results["T-003"]
    assert limit["kind"] == "method-limit"
    assert view.standing(limit, records) == view.SUPERSEDED
    assert view.position_marks(limit, view.SUPERSEDED) == []
    marked = [
        str(entry["id"])
        for entry in records.register.results
        if view.superseded(entry, view.standing(entry, records))
    ]
    # Thirty since 2026-10-02, when wand125's replayed rectangle certificates (T-045,
    # T-070) superseded T-030 at n = 18, T-020 at n = 19, T-021 at n = 20 and T-047 at
    # n = 26 and 29, the last counts each of them held; thirty-one later that day, when
    # the 1 October replays (T-074) beat wand125's point certificates (T-044) at the last
    # of their counts; thirty-two since 3 October, when squarepacker's rescaling (T-078)
    # superseded Daniel's s(12) >= 15680/3951 (T-049); thirty-three since the merge of the
    # same day, when the replays recorded in parallel (T-063, T-069) beat Bašić and
    # Slivková's piercing bound (T-087) at both of its counts.
    assert len(marked) == 33
    assert {"T-020", "T-021", "T-030", "T-044", "T-047", "T-049", "T-087"} <= set(marked)
    assert {str(records.results[entry]["kind"]) for entry in marked} == {"lower-bound"}


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
