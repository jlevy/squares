# ruff: noqa: RUF001 -- these tests read case prose, whose typography uses curly apostrophes.
"""The house adoption of 11 October 2026 and its later passes: derivation, drawing custody,
the case records, the coverage register and each pass's prior state."""

from __future__ import annotations

import dataclasses
import gzip
import hashlib
import json
import re
from datetime import date
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any, cast

import pytest
import yaml

from devtools import adopt_houses as adopt
from devtools import apply_closed_form as closed_form
from devtools import default_drawings as defaults
from devtools import run_negative_controls as controls
from devtools import select_houses as select
from devtools import upper_bound_houses as houses
from sqpack.field import FieldPreconditionError
from sqpack.yamlio import safe_load


@pytest.fixture(scope="module")
def selections() -> dict[int, select.Selection]:
    return select.select()


@pytest.fixture(scope="module")
def prior() -> dict[int, str]:
    """Each moved record as it stood before the adoption first moved it."""
    return adopt.read_history()


@pytest.fixture(scope="module")
def latest() -> dict[int, str]:
    """Each adopted record as it stood before the pass that last moved it."""
    return adopt.before_last_pass()


@pytest.fixture(scope="module")
def recorded() -> dict[int, select.Selection]:
    """The selection each record was written under (`adopt_houses.recorded_days`)."""
    return select.select(recorded=adopt.recorded_days())


@pytest.fixture(scope="module")
def replayed() -> list[adopt.Move]:
    """Each count's last pass planned again from the record as that pass read it, under the
    rule that pass ran under, so it plans the house it adopted."""
    return adopt.replay_plan()


def test_every_smaller_validated_packing_is_the_house_or_staged(
    selections: dict[int, select.Selection],
) -> None:
    """The house rule: wherever a validated packing is below its case, the count is staged
    for the bead that adopts it, and nowhere else does the derivation move anything; a
    staged count the selection no longer moves fails (`select_houses.check`)."""
    moving = {n: s.house.result for n, s in selections.items() if s.house is not None}
    assert moving == {n: pending.house for n, pending in select.PENDING_ADOPTION.items()}
    assert select.check(selections) == []
    assert all(
        not selection.held and not selection.algebraic for selection in selections.values()
    )


def test_n183_original_certificate_is_read_exactly_and_adopted_with_its_runs(
    latest: dict[int, str],
) -> None:
    """The adoption of 19 October 2026 (think-jh4w) moved 183 from the trivial grid to
    Evan Daniel's original certificate (T-220), took it off the staging list, and ran
    both strong generators on its witness in the same pull request, deferring nothing."""
    entry = next(row for row in select.load_results() if row["id"] == "T-220")
    unread: list[str] = []
    selected = select.select([entry], select.load_evidence(), unread=unread)
    assert unread == []
    assert set(selected) == {183}
    selection = selected[183]
    side = Fraction(13999580178736252502081470897571, 10**30)
    assert selection.house is None
    assert selection.case.verified == side < 14
    assert [c.result for c in selection.candidates] == ["T-220"]
    assert houses.ADOPTED[183] == "T-220"
    assert houses.adopted_on(183) == "2026-10-19"
    assert houses.side(183) == side
    assert 183 not in select.PENDING_ADOPTION
    assert 183 not in defaults.PENDING_ALLOWED
    assert adopt.plan(selected) == []
    # The record the adoption read is the grid's, and replaying the writer from it
    # plans exactly this house.
    before = _front(latest[183])
    assert before["reported_upper_bound"]["exact_form"] == "14"
    assert before["verified_upper_bound"]["exact_form"] == "14"
    replayed = select.select(
        [entry],
        select.load_evidence(),
        cases={183: select.parse_case(183, latest[183])},
        recorded={183: "2026-10-19"},
    )
    house = replayed[183].house
    assert house is not None
    assert house.result == "T-220"
    assert house.side == side
    assert house.report_evidence == ("E-evand-680-n183-report",)
    assert house.confirming_evidence == ("E-evand-680-n183-primary-exact-feasibility",)
    # The credit stays Evan Daniel's, after Francisco Couzo's n = 182 packing.
    packing = _front(select.case_path(183).read_text(encoding="utf-8"))
    assert packing["reported_upper_bound"]["found_by"] == ["Evan Daniel"]
    assert packing["reported_upper_bound"]["improved_by"] == []
    assert packing["conjectured_optimum"] is None


def test_every_adopted_case_holds_the_house_its_record_was_written_for(
    selections: dict[int, select.Selection], recorded: dict[int, select.Selection]
) -> None:
    """Every adopted count holds the house its last pass derived; where the house rule
    moves it since, the move is staged, and the record keeps that pass's house, the
    smallest candidate the rule of 15 October left in, until its adoption."""
    for n, result in houses.ADOPTED.items():
        selection = recorded[n]
        best = next(
            c
            for c in selection.candidates
            if houses.adopted_on(n) >= select.RULE_PASSES_FROM or c.result not in select.LIFTED
        )
        assert best.result == result
        assert selection.case.verified == best.side == houses.side(n)
        assert all(c.side < best.side for c in selection.held)
        if n not in select.PENDING_ADOPTION:
            assert selections[n].candidates[0].result == result


#: The counts where a held certificate (T-174's) was the smallest and the next candidate
#: took the house on 15 October 2026, once a hold skipped only the held entry (reviews A
#: and B of PR 614), each with the house it moved from. The pass of 16 October 2026 moved
#: seven of the ten again (`MOVED_AGAIN`), to certificates below T-174's.
NEXT_CANDIDATES = {
    105: ("T-170", "T-130"),
    261: ("T-169", "T-150"),
    272: ("T-171", "T-151"),
}

#: The counts of the 15 October next candidates that the 16 October review's adoption
#: moved again, each with its house since then and the next candidate it replaced: T-186
#: (Mykhailo Polkovskyi) and T-187 (Evan Daniel) are below T-174 there, so the hold no
#: longer decides them.
MOVED_AGAIN = {
    129: ("T-186", "T-162"),
    146: ("T-187", "T-168"),
    156: ("T-186", "T-161"),
    176: ("T-186", "T-165"),
    204: ("T-186", "T-162"),
    303: ("T-186", "T-162"),
}
#: The count of `MOVED_AGAIN` that a later pass moved once more: the adoption of 19 October
#: 2026 took 271 from T-186 to Evan Daniel's issue-664 certificate (T-219).
MOVED_LATER = {271: ("T-219", "2026-10-19")}

#: Issue 639's exact algebraic sides (T-193), the smallest at all sixteen of its counts
#: since its stage 4 exit (#658), each staged for the writer: below T-174's held sides at
#: twelve, which think-3mry held before, and below the T-186 houses #657 adopted at four.
T193_COUNTS = (88, 102, 123, 126, 175, 199, 204, 232, 258, 259, 266, 267, 292, 295, 301, 302)
T193_BELOW_T186 = (175, 204, 232, 302)


def test_the_records_of_the_lifted_hold_keep_their_next_candidates_until_adopted(
    selections: dict[int, select.Selection],
) -> None:
    """Where T-174 is smallest, the 15 October pass adopted the next confirmed, reviewed
    candidate while the owner held T-174. The 17 October archive keeps those records,
    and that pass adopted T-174 at all three counts."""
    previous = adopt.read_pass("2026-10-17")
    cases = {
        n: select.parse_case(n, previous[n]) if n in previous else selection.case
        for n, selection in selections.items()
    }
    recorded = select.select(cases=cases, recorded=dict.fromkeys(cases, "2026-10-15"))
    for n, (result, before) in NEXT_CANDIDATES.items():
        assert houses.ADOPTED[n] == "T-174"
        assert houses.adopted_on(n) == "2026-10-17"
        assert [c.result for c in recorded[n].held] == ["T-174"]
        assert selections[n].house is None
        assert n not in select.PENDING_ADOPTION
        packing = _front(previous[n])
        assert adopt._holder(packing).endswith(f"({result})")  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
        assert Fraction(packing["verified_upper_bound"]["exact_form"]) > houses.side(n)
        if before is not None:
            earlier = _front(adopt.read_pass("2026-10-15")[n])
            assert adopt._holder(earlier).endswith(f"({before})")  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    held_counts = {n for n, s in recorded.items() if s.held}
    assert set(NEXT_CANDIDATES) < held_counts
    # 50 until the adoption of 19 October 2026 moved 155 and 236 to Evan Daniel's
    # certificates (T-197, T-218), below T-174's, so the hold decides neither; 47 since
    # the adoption of 20 October 2026 moved 308 to his issue-689 certificate (T-221).
    assert len(held_counts) == 47
    previous_t174 = {n for n in previous if houses.ADOPTED[n] == "T-174"}
    assert held_counts | {70, 153, 207} | set(T193_BELOW_T186) == (
        set(select.PENDING_ADOPTION) | previous_t174
    )
    assert {n: houses.ADOPTED[n] for n in previous if n not in previous_t174} == {
        29: "T-195",
        155: "T-197",
        308: "T-221",
    }


def test_a_house_below_the_held_entry_leaves_the_hold_deciding_nothing(
    selections: dict[int, select.Selection], latest: dict[int, str]
) -> None:
    """The 16 October adoption moved seven of the 15 October next candidates to
    certificates below T-174's, so no hold is named there and the earlier pass's house is
    the record's holder before this pass."""
    for n, (result, before) in MOVED_AGAIN.items():
        assert houses.ADOPTED[n] == result
        assert houses.adopted_on(n) == "2026-10-16"
        assert not selections[n].held
        held = [c for c in selections[n].candidates if c.result == "T-174"]
        assert all(c.side > houses.side(n) for c in held)
        assert adopt._holder(_front(latest[n])).endswith(f"({before})")  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    for n, (result, day) in MOVED_LATER.items():
        assert houses.ADOPTED[n] == result
        assert houses.adopted_on(n) == day
        assert not selections[n].held


def test_regularizations_leave_the_packing_with_its_finder(
    selections: dict[int, select.Selection],
) -> None:
    houses_at = {
        n: next(c for c in selections[n].candidates if c.result == houses.ADOPTED[n])
        for n in (70, 103, 211, 241, 292)
    }
    # T-188's 211 is another arrangement of Ostashev's design, no refinement (RT-1 of the
    # 16 October review), so it regularizes nothing.
    assert {n: house.regularizes for n, house in houses_at.items()} == {
        70: "T-125",
        103: "T-146",
        211: None,
        241: "T-181",
        292: "T-136",
    }
    assert adopt.CREDITS[292].found_by == (adopt.SQUISH,)
    assert adopt.CREDITS[70].found_by == (adopt.XU,)
    assert adopt.CREDITS[103].improved_by == ("Mishapolk", adopt.DANIEL, "PingYou Ltd")


def _candidate(result: str, side: Fraction, published: str) -> select.Candidate:
    return select.Candidate(
        result=result,
        n=7,
        side=side,
        source_key=f"[{result}]",
        published=published,
        report_evidence=(),
        confirming_evidence=(f"E-{result.lower()}",),
        regularizes=None,
    )


def test_ties_go_to_the_earlier_finder_then_the_earlier_entry() -> None:
    later = _candidate("T-200", Fraction(5, 2), "2026-10-10")
    earlier = _candidate("T-300", Fraction(5, 2), "2026-10-09")
    smaller = _candidate("T-400", Fraction(9, 4), "2026-10-11")
    assert min([later, earlier], key=select.precedence) is earlier
    assert min([later, earlier, smaller], key=select.precedence) is smaller
    first = _candidate("T-100", Fraction(5, 2), "2026-10-10")
    assert min([later, first], key=select.precedence) is first


def _confirmed_entry() -> tuple[dict[str, Any], dict[str, Any]]:
    """A synthetic V3/C3 upper bound at n = 7 with an accepted review and a passing replay."""
    entry: dict[str, Any] = {
        "id": "T-900",
        "kind": "upper-bound",
        "verification": "V3",
        "confirmation": "C3",
        "scope": {"n_values": [7]},
        "attribution": {"source_keys": ["[test]"], "published": "2026-10-10"},
        "evidence": ["E-test-replay"],
        "reviews": [{"verdict": "accepted", "covers": ["T-900"]}],
    }
    evidence = {
        "E-test-replay": {
            "claim": "upper-bound",
            "assurance": "verified",
            "origin": "replayed-here",
            "performed_by": "repository",
            "replay_status": "passed",
        }
    }
    return entry, evidence


def test_only_a_run_beyond_the_producer_confirms_a_house() -> None:
    entry, evidence = _confirmed_entry()
    assert select.confirming(entry, evidence, 7) == ("E-test-replay",)
    producer = {**evidence["E-test-replay"], "performed_by": "source-author"}
    assert select.confirming(entry, {"E-test-replay": producer}, 7) == ()


def test_a_case_keeps_its_own_house_where_nothing_is_below(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    entry, evidence = _confirmed_entry()
    monkeypatch.setitem(select.reports.HOUSES, "[test]", lambda _n: Fraction(3))
    monkeypatch.setattr(select, "_side", lambda _key, _n: Fraction(3))
    case = select.Case(
        n=7, verified=Fraction(3), reported=Fraction(3), source_key="", evidence=()
    )
    held = select.select([entry], evidence, cases={7: case})[7]
    assert held.house is None
    assert not held.moves
    lower = select.Case(
        n=7, verified=Fraction(4), reported=Fraction(4), source_key="", evidence=()
    )
    moved = select.select([entry], evidence, cases={7: lower})[7]
    assert moved.house is not None
    assert moved.margin == 1
    unreviewed = {**entry, "reviews": [{"verdict": "defect-open", "covers": ["T-900"]}]}
    assert select.select([unreviewed], evidence, cases={7: lower}) == {}


def test_a_candidate_is_ordered_against_a_closed_form_ceiling_exactly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A closed-form ceiling is held as the root of its minimal polynomial, so a side just
    either side of it is ordered exactly, never left to a person; only a form no reader
    holds is unordered, which `--check` fails on as a defect of the code."""
    ceiling = select.load_case(51).verified  # (16 + 5 sqrt(2)) / 3
    assert isinstance(ceiling, select.exact_sides.Algebraic)
    assert select.load_case(51).exact
    assert select.ceiling(ceiling) == "7.6903559372884918"
    entry, evidence = _confirmed_entry()
    case = select.Case(n=7, verified=ceiling, reported=Fraction(7), source_key="", evidence=())
    display = Fraction(Decimal("7.6903559372884918"))
    # The form is 7.69035593728849174800..., which its print rounds up at sixteen places.
    below, above = display - Fraction(6, 10**17), display - Fraction(4, 10**17)
    sides = {"just below": below, "just above": above}
    assert sides["just below"] < ceiling < sides["just above"]
    side = sides["just below"]
    monkeypatch.setitem(select.reports.HOUSES, "[test]", lambda _n: side)
    monkeypatch.setattr(select, "_side", lambda _key, _n: side)
    moved = select.select([entry], evidence, cases={7: case})[7]
    assert moved.house is not None
    assert Fraction(0) < moved.margin < Fraction(5, 10**17)
    side = sides["just above"]
    assert not select.select([entry], evidence, cases={7: case})[7].moves
    unread = dataclasses.replace(case, verified=display + Fraction(1, 10**16), unread="why")
    side = sides["just below"]
    unordered = select.select([entry], evidence, cases={7: unread})[7]
    assert unordered.unordered == "why"
    assert not unordered.moves
    assert "unordered: why" in select.table({7: unordered}, everything=False)
    monkeypatch.setattr(select, "PENDING_ADOPTION", {})
    assert select.check({7: unordered})[0].startswith("FAIL: a candidate is below the print")


def test_an_entry_over_two_sources_reads_each_count_where_its_replay_decided_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """T-181's replays decided 211 and 241 from issue 583's revision and 302 from issue
    586's, though both reports state all three; the replay names the source, whatever the
    order of the keys (review B of PR 614, B3)."""
    entry, evidence = _confirmed_entry()
    entry = {
        **entry,
        "scope": {"n_values": [7, 8]},
        "attribution": {"source_keys": ["[first]", "[second]"], "published": "2026-10-10"},
        "evidence": ["E-first", "E-second", "E-first-replay", "E-second-replay"],
    }
    replay = evidence["E-test-replay"]
    evidence = {
        **evidence,
        "E-first": {
            "assurance": "reported",
            "source_key": "[first]",
            "scope": {"n_values": [7, 8]},
        },
        "E-second": {
            "assurance": "reported",
            "source_key": "[second]",
            "scope": {"n_values": [7, 8]},
        },
        "E-first-replay": {**replay, "source_key": "[first]", "scope": {"n_values": [7]}},
        "E-second-replay": {**replay, "source_key": "[second]", "scope": {"n_values": [8]}},
    }
    sides = {("[first]", 7): Fraction(3), ("[second]", 8): Fraction(4)}
    monkeypatch.setitem(select.reports.HOUSES, "[first]", lambda _n: Fraction(3))
    monkeypatch.setitem(select.reports.HOUSES, "[second]", lambda _n: Fraction(4))
    monkeypatch.setattr(select, "_side", lambda key, n: sides[key, n])
    assert select.source_key_at(entry, evidence, 7) == "[first]"
    assert select.source_key_at(entry, evidence, 8) == "[second]"
    assert select.source_key_at(entry, evidence, 9) == ""
    unread: list[str] = []
    found = select.candidates([entry], evidence, unread=unread)
    assert [(c.source_key, c.side, c.report_evidence) for c in found[7]] == [
        ("[first]", Fraction(3), ("E-first",))
    ]
    assert [(c.source_key, c.side) for c in found[8]] == [("[second]", Fraction(4))]
    assert unread == []
    # The keys' order decides nothing: reversed, each count is read where it was before.
    reversed_keys = {
        **entry,
        "attribution": {**entry["attribution"], "source_keys": ["[second]", "[first]"]},
    }
    for n in (7, 8, 9):
        assert select.source_key_at(reversed_keys, evidence, n) == select.source_key_at(
            entry, evidence, n
        )
    # A count no replay of the entry decided is no candidate, and the entry is not named
    # unread either: there is nothing there for a reader to read.
    unstated = {**entry, "scope": {"n_values": [7, 9]}}
    select.candidates([unstated], evidence, unread=unread)
    assert unread == []
    # A count two replays decided from two sources is not read either.
    both = {
        **evidence,
        "E-second-replay": {**replay, "source_key": "[second]", "scope": {"n_values": [7, 8]}},
    }
    assert select.source_key_at(entry, both, 7) == ""


def test_t181_reads_the_same_sources_with_its_keys_reversed() -> None:
    """Both of T-181's reports state 211 and 241; reversed, the issue-583 replay still
    names issue 583's packet there, and 302 stays issue 586's (review B of PR 614, B3)."""
    results = select.load_results()
    evidence = select.load_evidence()
    entry = next(e for e in results if e["id"] == "T-181")
    keys = list(entry["attribution"]["source_keys"])
    flipped = {**entry, "attribution": {**entry["attribution"], "source_keys": keys[::-1]}}
    for n in (211, 241, 302):
        assert select.source_key_at(flipped, evidence, n) == select.source_key_at(
            entry, evidence, n
        )
    assert (
        select.source_key_at(entry, evidence, 211)
        == "[Couzo issue-583 certificates 2026-10-13]"
    )
    assert select.source_key_at(entry, evidence, 302) == "[Couzo certificates 2026-10-13]"
    found = select.candidates([flipped], evidence)
    sides = {n: c.side for n, cs in found.items() for c in cs}
    assert sides == {
        n: c.side for n, cs in select.candidates([entry], evidence).items() for c in cs
    }


def test_the_two_couzo_entries_from_one_packet_each_keep_their_house_source() -> None:
    """T-181 and T-182 both read issue 586's packet; keyed by result, neither is lost."""
    by_result = houses.sources()
    assert all(result == source.result for result, source in by_result.items())
    keys = [source.key for source in by_result.values()]
    for n in houses.NUMBERS:
        assert houses.source_for(n).result == houses.ADOPTED[n]
    shared = {key for key in keys if keys.count(key) > 1}
    assert all(
        len({s.result for s in by_result.values() if s.key == key}) > 1 for key in shared
    )


def test_an_algebraic_certificate_is_a_candidate_ordered_exactly(
    recorded: dict[int, select.Selection],
) -> None:
    """PR #574's sides at 70, 153, 207 and 302 are roots of integer polynomials, decided on
    one exact route, which is what stage 4 asks. Each is a candidate, held by its minimal
    polynomial and ordered exactly: below its case at 70, 153 and 207, where it is the
    house, staged, and above it at 302. The records of 15 October left them out (RP-3)."""
    key = "[PingYou PR 574 certificates 2026-10-13]"
    counts = select.algebraic_counts(key)
    assert {70, 153, 207, 302} <= counts
    assert not {68, 105, 211, 304} & counts
    assert select.algebraic_counts("[Couzo certificates 2026-10-13]") == frozenset()
    found = select.candidates(select.load_results(), select.load_evidence())
    for n, degree in ((70, 5), (153, 7), (207, 5), (302, 3)):
        (t174,) = [c for c in found[n] if c.result == "T-174"]
        assert t174.algebraic
        assert isinstance(t174.side, select.exact_sides.Algebraic)
        assert t174.side.degree == degree
        below = t174.side < select.load_case(n).verified
        assert below == (n != 302), n
        assert recorded[n].algebraic == (("T-174", key),)
        assert all(not c.algebraic for c in recorded[n].candidates)


def test_a_staged_count_passes_the_check_and_a_stale_or_unstaged_one_fails(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A validated smaller packing is the house, or staged for the bead that adopts it:
    `--check` passes a staged count, fails an unstaged one, one staged for another house,
    and a staged count where nothing moves."""
    entry, evidence = _confirmed_entry()
    other = {
        **entry,
        "id": "T-901",
        "attribution": {"source_keys": ["[other]"], "published": "2026-10-09"},
        "reviews": [{"verdict": "accepted", "covers": ["T-901"]}],
    }
    sides = {"[test]": Fraction(3), "[other]": Fraction(7, 2)}
    monkeypatch.setitem(select.reports.HOUSES, "[test]", lambda _n: Fraction(3))
    monkeypatch.setitem(select.reports.HOUSES, "[other]", lambda _n: Fraction(7, 2))
    monkeypatch.setattr(select, "_side", lambda key, _n: sides[key])
    case = select.Case(
        n=7, verified=Fraction(4), reported=Fraction(4), source_key="", evidence=()
    )
    selected = select.select([entry, other], evidence, cases={7: case})
    house = selected[7].house
    assert house is not None
    assert house.result == "T-900"
    assert [c.result for c in selected[7].candidates] == ["T-900", "T-901"]
    staged = {7: select.Pending(house="T-900", bead="think-test", why=select.NEXT_PULL_REQUEST)}
    monkeypatch.setattr(select, "PENDING_ADOPTION", staged)
    # A synthetic register owes no correction (`CORRECTIONS_OWED`, review B1 of #658).
    monkeypatch.setattr(select, "CORRECTIONS_OWED", {})
    assert select.check(selected) == []
    assert select.row(selected[7])["staged"] == "think-test"
    assert "staged (next pull request): think-test" in select.table(selected, everything=False)
    assert select.deferrals() == [("select_houses.PENDING_ADOPTION n=7 (T-900)", "think-test")]
    real = select.select
    monkeypatch.setattr(select, "select", lambda **_arguments: selected)
    monkeypatch.setattr(select, "unread_pending", lambda _unread: {})
    assert select.main(["--check"]) == 0
    shown = capsys.readouterr().out
    assert "staged adoption, T-900 under think-test (next pull request): n = [7]" in shown
    monkeypatch.setattr(
        select, "PENDING_ADOPTION", {7: dataclasses.replace(staged[7], house="T-901")}
    )
    assert "the house is T-900; stage that, or adopt it" in select.check(selected)[0]
    monkeypatch.setattr(select, "PENDING_ADOPTION", {})
    assert select.check(selected)[0].startswith("FAIL: a validated smaller packing")
    assert select.main(["--check"]) == 1
    above = dataclasses.replace(case, verified=Fraction(3), reported=Fraction(3))
    still = real([entry, other], evidence, cases={7: above})
    monkeypatch.setattr(select, "PENDING_ADOPTION", staged)
    assert "take it off PENDING_ADOPTION" in select.check(still)[0]
    # The records as written: before the house rule a lifted hold kept T-900 out, and the
    # next candidate below the case took the house; the staged house is left out after.
    monkeypatch.setitem(
        select.LIFTED, "T-900", select.Hold(whose="T-900's", why="w", since="d")
    )
    old = real([entry, other], evidence, cases={7: case}, recorded={7: "2026-10-15"})
    assert old[7].house is not None
    assert old[7].house.result == "T-901"
    assert [c.result for c in old[7].held] == ["T-900"]
    new = real([entry, other], evidence, cases={7: case}, recorded={7: "2026-10-17"})
    assert new[7].house is not None
    assert new[7].house.result == "T-901"
    assert new[7].held == ()


def test_no_result_is_held_and_the_lifted_hold_keeps_its_words() -> None:
    """The house rule holds no result: `HELD` is gone, the hold it lifted keeps only the
    words of the records written under it, and each staged count names an open bead's id."""
    assert not hasattr(select, "HELD")
    assert set(select.LIFTED) == {"T-174"}
    for hold in select.LIFTED.values():
        assert hold.why.strip()
        assert hold.reason.startswith(f"{hold.whose} houses were held for the owner, since ")
        assert adopt.words(hold.since)
        assert hold.until == select.RULE_SET_ON
    assert all(
        re.fullmatch(r"think-[a-z0-9]+", pending.bead)
        for pending in select.PENDING_ADOPTION.values()
    )


def test_every_record_names_a_smaller_held_or_algebraic_certificate(
    recorded: dict[int, select.Selection],
) -> None:
    """Under the rule of 15 October, a held certificate below a case was named in its
    record with why it waited: in the certificate section where a pass houses the count,
    in a dated note under the title elsewhere; an algebraic one below the house, which
    that rule left to the owner, in the section (reviews A and B of PR 614, A1, B2 and
    B7). The records say so until their counts are adopted, and since the house rule they
    say the waits ended, naming the bead each staged adoption waits under, and never that
    the owner decides (review A2 of #660)."""
    reason = select.LIFTED["T-174"].reason.replace("'", "’")
    for n, selection in recorded.items():
        if not selection.held:
            continue
        text = _flat(select.case_path(n).read_text(encoding="utf-8"))
        assert _flat(reason) in text, n
        assert (
            "E-pingyou-574-exact-feasibility"
            in _front(select.case_path(n).read_text())["evidence"]
        ), n
        assert "until the owner decides" not in text, n
        assert "if the owner adopts" not in text, n
        assert f"staged under {select.PENDING_ADOPTION[n].bead}," in text, n
        if n in houses.ADOPTED:
            assert adopt.HELD_OPENING not in text, n
        else:
            assert f"{adopt.HELD_OPENING}15 October 2026; lifted 16 October 2026.**" in text, n
    assert adopt.held_counts() == sorted(
        n for n, s in recorded.items() if s.held and n not in houses.ADOPTED
    )
    for n in (70, 153, 207):
        text = _flat(select.case_path(n).read_text(encoding="utf-8"))
        assert "T-174’s algebraic certificate at this count" in text, n
        assert "RP-3 of the [review of 14 October 2026]" in text, n
        assert "owner’s decision" not in text.split("algebraic certificate at this count")[1]
        assert f"staged under {select.WRITER_BEAD}," in text, n
    # At 302 T-174's algebraic side is above the house, and nothing is said of it.
    assert "algebraic certificate at this count" not in select.case_path(302).read_text()


def test_sizes_measure_a_staged_witness_as_git_stores_it(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Review C9 of #660: OR-18's stored-size unit and its measured case rested on scratch
    code, so no adoption could measure its witnesses by command before committing them.
    `upper_bound_houses sizes` builds each staged count's witness as the module builds a
    house and counts its blob, the object Git names, as zlib packs it. The adoption of 17
    October 2026 took 68 off the list, so it is staged here again: the witness it builds is
    the committed one, byte for byte."""
    import subprocess  # noqa: PLC0415
    import zlib  # noqa: PLC0415

    monkeypatch.setitem(
        select.PENDING_ADOPTION,
        68,
        select.Pending(house="T-174", bead="think-test", why=select.NEXT_PULL_REQUEST),
    )
    data = (houses.WITNESSES / "n-068.yaml").read_bytes()
    blob = b"blob %d\x00" % len(data) + data
    named = subprocess.run(
        ["git", "hash-object", "--stdin"],
        input=data,
        capture_output=True,
        check=True,
    ).stdout.decode()
    assert hashlib.sha1(blob).hexdigest() == named.strip()
    assert houses.stored_size(data) == len(zlib.compress(blob))
    (row,), skipped = houses.staged_sizes([68])
    assert skipped == []
    assert (row.n, row.house) == (68, "T-174")
    assert 0 < row.stored < row.checkout
    assert row.now_checkout == len(data) == row.checkout
    assert row.now_stored == houses.stored_size(data)
    assert houses.staged_sizes([70]) == (
        [],
        ["n=70: T-174's side is algebraic; no writer takes it yet"],
    )
    with pytest.raises(houses.HouseError, match="only counts staged"):
        houses.staged_sizes([5])
    # Review D3 of #660: history keeps the new blobs whole, the replaced ones staying in it,
    # so the stored figure is their sum, and the difference is only the tree's.
    assert houses.print_sizes([68]) == 0
    (total,) = [line for line in capsys.readouterr().out.splitlines() if "1 witness:" in line]
    stored = houses.stored_size(data)
    assert f"{row.stored / 1e6:.2f} MB as Git stores them, which history keeps" in total
    assert f"the tree's blobs by {(row.stored - stored) / 1e6:.2f} MB" in total


#: Words the records wrote while an adoption waited for the owner, and the 15 October
#: hold's size, which counted a checkout's bytes as Git's (reviews A2, C4 and C7 of #660).
OWNER_WAITS = (
    "until the owner decides, and moves",
    "if the owner adopts",
    "the owner decides their adoption",
    "adoption is the owner's decision",
    "adoption is the owner's (rp-3)",
    "18.5 mb to git",
)


def test_no_record_leaves_an_adoption_to_the_owner() -> None:
    """Review C4 of #660: the register's evidence still said the owner decides T-174's
    algebraic adoption after every case record had stopped saying it, since the A2 tests
    read case records only. Every record that can carry such words is read here, the case
    records, the register, its evidence, the coverage and requests records and the
    citation deferrals; and none counts the hold's 18.5 MB "to Git" (C7)."""
    paths = [
        *sorted(select.FRONTIER.glob("n-*.md")),
        select.RESULTS,
        select.EVIDENCE,
        select.FRONTIER / "source-coverage.yaml",
        select.ROOT / "campaign/result-requests.yaml",
        select.ROOT / "devtools/certificate-citation-deferrals.yaml",
    ]
    for path in paths:
        words = _flat(path.read_text(encoding="utf-8")).replace("\u2019", "'").lower()
        for phrase in OWNER_WAITS:
            assert phrase not in words, (path.name, phrase)


def test_a_moved_house_keeps_its_lifted_hold_as_history() -> None:
    """Review C7 of #660, and the merge of #657, which moved ten counts below T-174 on the
    day the house rule lifted the hold: a section whose house a later pass moved keeps
    when the hold held and why, and drops the clause that the case keeps the house, as
    each writer wrote it. The held sentence of a staged count puts the dates first."""
    lead = (
        "T-174 at $1$, `1e-19` below this house, is confirmed here and accepted by the "
        "[review of 14 October 2026](../../r.md)"
    )
    history = f"{lead}. {adopt.lifted_sentence('T-174')}"
    assert adopt.lifted_sentence("T-174") == (
        "From 15 October 2026 until the owner’s house rule of 16 October 2026 lifted the "
        "hold, PR #574’s houses were held for the owner, since their witnesses would add "
        "about 18.5 MB to a checkout and their custody inputs about 5.8 MB to every "
        "worker’s snapshot."
    )
    written = (
        (
            f"{lead}, but PR #574’s houses are held for the owner: their witnesses would add "
            "about 18.5 MB to Git (OR-18) and their custody inputs about 5.8 MB to every "
            "worker’s snapshot; the case keeps this house until the owner decides, and moves "
            "to T-174’s side if the owner adopts them."
        ),
        (
            f"{lead}. PR #574’s houses were held for the owner, since their witnesses would "
            "add about 18.5 MB to Git (OR-18) and their custody inputs about 5.8 MB to every "
            "worker’s snapshot, from 15 October 2026 until the owner’s house rule of 16 "
            "October 2026 lifted the hold: the case keeps this house until T-174’s adoption, "
            "staged under think-3mry, moves it to T-174’s side."
        ),
        (
            f"{history} The case keeps this house until T-174’s adoption, staged under "
            "think-3mry, moves it to T-174’s side."
        ),
    )
    for text in written:
        # The records are wrapped, so a sentence may break at any space.
        wrapped = text.replace(" until ", "\nuntil ").replace(" the hold", "\nthe hold")
        assert _flat(adopt.held_history(wrapped)) == history, text[:60]
    # The ten counts #657 moved below T-174 keep it so, and a staged count waits; three of
    # them (175, 204 and 232) wait for T-193, below #657's houses there (#658).
    for n in (129, 146, 156, 175, 176, 204, 232, 264, 271, 303):
        text = _flat(select.case_path(n).read_text(encoding="utf-8"))
        assert _flat(adopt.lifted_sentence("T-174")) in text, n
        assert "until T-174’s adoption" not in text, n
        staged = select.PENDING_ADOPTION.get(n)
        assert (staged is None) == (n not in T193_BELOW_T186), n
        assert staged is None or staged.house == "T-193", n
    # The 37 counts adopted on 17 October 2026 keep the hold's note as history, without
    # the clause that the case keeps its house.
    text = _flat(select.case_path(68).read_text(encoding="utf-8"))
    assert _flat(adopt.lifted_sentence("T-174")) in text
    assert "until T-174’s adoption" not in text
    assert "**House adoption, 17 October 2026.**" in text


#: The sentence a certificate section ends with, listing what its house was chosen over.
NOT_SELECTED = re.compile(
    r"The\s+other\s+certificates\s+confirmed\s+here\s+at\s+this\s+count,\s+(.*?),\s+stay"
    r"\s+verified\s+and\s+are\s+not\s+selected\.",
    re.DOTALL,
)


def _not_selected(text: str) -> set[str]:
    """Every result a record's sections list as confirmed there and not selected."""
    return {
        result
        for match in NOT_SELECTED.finditer(text)
        for result in re.findall(r"\bT-\d+\b", match.group(1))
    }


def test_no_section_lists_its_current_house_or_a_held_certificate_as_not_selected(
    recorded: dict[int, select.Selection],
) -> None:
    """A section's not-selected list names what its house was chosen over, so no record
    lists the count's current house there, and none lists a held certificate, which is
    no candidate. Each pass's prior state is held to the same: one that lists the house
    its own pass adopts is a record already rewritten, not the record as the pass read
    it (reviews A10 and B8 of PR 614: the 15 October archive took round 1's branch text
    at nine counts, and their earlier sections named the new house and T-174)."""
    found = []
    for n, selection in recorded.items():
        listed = _not_selected(select.case_path(n).read_text(encoding="utf-8"))
        named = listed & {houses.ADOPTED.get(n), *(c.result for c in selection.held)}
        if named:
            found.append((n, sorted(named)))
    assert found == []
    for day in adopt.passes():
        for n, text in adopt.read_pass(day).items():
            assert houses.ADOPTED[n] not in _not_selected(text), (day, n)
    # The sentence is what the writer writes, so the pattern reads it where it stands.
    assert {"T-127", "T-115", "T-113"} <= _not_selected(
        select.case_path(129).read_text(encoding="utf-8")
    )


def test_a_held_note_is_written_kept_and_dropped_by_the_held_results() -> None:
    """The note is the writer's: idempotent on the committed record, rebuilt from a record
    without it, and dropped where no held result is below the case."""
    n = adopt.held_counts()[0]
    committed = select.case_path(n).read_text(encoding="utf-8")
    assert adopt.held_note(n, committed) == committed
    assert adopt.carries_held_note(committed)
    title, parts = adopt._paragraphs(committed.split("---\n", 2)[2])  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    bare = committed.replace(
        next(part for part in parts if part.startswith(adopt.HELD_OPENING)) + "\n\n", ""
    )
    assert not adopt.carries_held_note(bare)
    assert _flat(adopt.held_note(n, bare).split("---\n", 2)[2]) == _flat(
        committed.split("---\n", 2)[2]
    )
    del title
    adopted = next(iter(houses.ADOPTED))
    text = select.case_path(adopted).read_text(encoding="utf-8")
    assert adopt.held_note(adopted, text) == text


def _register_check() -> tuple[list[str], dict[str, list[int]], dict[str, list[int]]]:
    """What `--check` fails on beside the selection, on the real register: the sides no
    reader holds, the unread entries below their cases, and the unread prints that only
    overlap their ceilings."""
    unread: list[str] = []
    unheld: list[str] = []
    select.candidates(
        select.load_results(), select.load_evidence(), unread=unread, unheld=unheld
    )
    return unheld, select.unread_pending(unread), select.unread_unordered(unread)


def test_no_unread_eligible_entry_is_pending_adoption() -> None:
    """An eligible entry with no exact reader is never a candidate, so `--check` reads its
    standing instead: one that states a side below its case would be an adoption the
    selector cannot see. Review C1 of #660: the two other failures `--check` added, a side
    no reader holds (B3) and an unread print that only overlaps its ceiling (A10), ran on
    no real register in CI; they are held empty here too."""
    assert _register_check() == ([], {}, {})


def test_every_unread_entry_reaches_the_check() -> None:
    """Review D6 of #660: the C10 guard holds `unread_pending` to every entry it is given,
    but an exemption that keeps an entry out of `unread`, in `eligible` or in `candidates`
    before the entry is listed, never reaches it. The confirmed, reviewed upper bounds
    whose one source no reader takes are found here without either, and every one is in
    `unread`, so a skip there fails this."""
    from devtools import upper_bound_reports as reports  # noqa: PLC0415

    def rank(rung: object) -> int:
        text = str(rung or "")
        return int(text[1:]) if len(text) == 2 and text[1:].isdigit() else -1

    expected = set()
    for entry in select.load_results():
        reviewed = any(
            review.get("verdict") == "accepted" and entry["id"] in (review.get("covers") or ())
            for review in entry.get("reviews") or ()
        )
        keys = list((entry.get("attribution") or {}).get("source_keys") or ())
        if (
            entry.get("kind") == "upper-bound"
            and rank(entry.get("verification")) >= 3
            and rank(entry.get("confirmation")) >= 3
            and reviewed
            and len(keys) == 1
            and keys[0] not in reports.HOUSES
            and keys[0] not in select.ALGEBRAIC_READERS
        ):
            expected.add(str(entry["id"]))
    unread: list[str] = []
    select.candidates(select.load_results(), select.load_evidence(), unread=unread)
    assert expected
    assert expected <= set(unread)


def test_a_side_the_register_cannot_hold_turns_the_register_check_red(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Review C1 of #660: forcing T-174's algebraic side at 302 to fail its reader left
    every test green while `select_houses --check` exited 1. The register check sees it."""
    real = select.exact_side

    def failing(key: str, n: int) -> select.exact_sides.Side:
        if n == 302 and n in select.algebraic_counts(key):
            raise select.exact_sides.ExactSideError("a test: the reader cannot isolate it")
        return real(key, n)

    monkeypatch.setattr(select, "exact_side", failing)
    unheld, _pending, _unordered = _register_check()
    assert unheld == ["T-174 at n = 302: a test: the reader cannot isolate it"]


def test_unread_pending_reports_every_improvement_whatever_would_defer_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Review C10 of #660: the A6 guard caught #658's exemption because it patched the
    deferral reader that exemption used, so one built on another reading would pass it.
    Here every eligible entry states a side below its case, and `unread_pending` reports
    each one: an exemption of any kind, on any record, drops one and fails this."""
    from devtools import check_standing as standing  # noqa: PLC0415

    def improving(_record: Any, _records: Any) -> list[standing.Finding]:
        stated = standing.Stated(Fraction(1), Fraction(0))
        return [standing.Finding(69, standing.UPPER, stated, standing.EXCEEDS, None)]

    from devtools import check_certificate_citations as citations  # noqa: PLC0415

    monkeypatch.setattr(standing, "improvements", improving)
    identifiers = [
        str(entry["id"]) for entry in select.load_results() if select.eligible(entry)
    ]
    deferred = {
        str(result)
        for deferral in citations.load_deferrals()
        for result in cast("list[object]", deferral["results"])
    }
    # Entries the real deferral file names are among them, as T-193 would be on #658.
    assert "T-174" in deferred & set(identifiers)
    assert select.unread_pending(identifiers) == {
        identifier: [69] for identifier in identifiers
    }


def test_check_lists_the_unread_and_fails_on_one_pending_adoption(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def selecting(
        *, since: str | None, unread: list[str], unheld: list[str]
    ) -> dict[int, select.Selection]:
        assert since is None
        assert unheld == []
        unread.append("T-901")
        return {}

    monkeypatch.setattr(select, "select", selecting)
    monkeypatch.setattr(select, "PENDING_ADOPTION", {})
    monkeypatch.setattr(select, "CORRECTIONS_OWED", {})
    monkeypatch.setattr(select, "unread_pending", lambda _unread: {})
    monkeypatch.setattr(select, "unread_unordered", lambda _unread: {})
    assert select.main(["--check"]) == 0
    assert "unread, eligible but with no exact reader: T-901" in capsys.readouterr().out
    monkeypatch.setattr(select, "unread_pending", lambda unread: {unread[0]: [7]})
    assert select.main(["--check"]) == 1
    assert "T-901 has no exact reader and states a side below its case at n = [7]" in (
        capsys.readouterr().out
    )


def test_a_citation_deferral_never_hides_a_validated_smaller_side(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Review A6 of #660: an exemption keyed on `certificate-citation-deferrals.yaml`, as
    #658 first wrote one for T-193, turned the gate green while sixteen validated smaller
    packings waited on the owner's RP-3, a wait the house rule ended. An eligible entry
    with no exact reader that states a side below its case fails `--check` whatever a
    deferral says of it, and a merged exemption turns this test red."""
    from devtools import check_certificate_citations as citations  # noqa: PLC0415
    from devtools import check_standing as standing  # noqa: PLC0415

    real = standing.improvements

    def improving(record: Any, records: Any) -> list[standing.Finding]:
        if str(record["id"]) == "T-088":
            stated = standing.Stated(Fraction(1), Fraction(0))
            return [standing.Finding(69, standing.UPPER, stated, standing.EXCEEDS, None)]
        return real(record, records)

    monkeypatch.setattr(standing, "improvements", improving)
    deferral = {
        "evidence": "E-test",
        "results": ["T-088"],
        "bead": "think-test",
        "blocked_on": "the owner's decision RP-3",
        "reason": "a test of a wait the house rule ended",
    }
    monkeypatch.setattr(citations, "load_deferrals", lambda *_path: [deferral])
    monkeypatch.setattr(select, "ALGEBRAIC_READERS", {})
    assert select.unread_pending(["T-088"]) == {"T-088": [69]}
    assert select.main(["--check"]) == 1
    assert "FAIL: T-088 has no exact reader and states a side below its case at n = [69]" in (
        capsys.readouterr().out
    )


def _below(ceiling: select.exact_sides.Side) -> select.exact_sides.Side:
    """An algebraic side a little below `ceiling`: r + sqrt(2) / 10**9 at r = ceiling less
    10**-6, the root of x^2 - 2 r x + r^2 - 2 / 10**18."""
    low, _high = select.exact_sides.enclosure(ceiling, Fraction(1, 10**12))
    r = low - Fraction(1, 10**6)
    return select.exact_sides.algebraic(
        [1, -2 * r, r * r - Fraction(2, 10**18)], (r, r + Fraction(2, 10**9))
    )


def test_t193_is_read_exactly_and_staged_as_the_house_at_all_sixteen_counts(
    selections: dict[int, select.Selection],
) -> None:
    """Review A of #658 (A2 to A5): T-193 was kept off the gate by a citation deferral,
    which the house rule allows no more. Its source now has a reader, so T-193 is a
    candidate, read exactly at each count to the 40 places its claim prints, the smallest
    at all sixteen, and staged for the writer, which cannot write an algebraic side yet."""
    key = "[Daniel exact current records 2026-10-16]"
    assert select.ALGEBRAIC_READERS[key] is select.evand_exact_side
    entry = next(entry for entry in select.load_results() if entry["id"] == "T-193")
    assert tuple(sorted(entry["scope"]["n_values"])) == T193_COUNTS
    printed = dict(
        re.findall(r"s\((\d+)\) <= (?:[^,]*? = )?(\d+\.\d{40})…", _flat(entry["claim"]))
    )
    assert sorted(int(n) for n in printed) == list(T193_COUNTS)
    unread: list[str] = []
    select.select(unread=unread)
    assert "T-193" not in unread
    for n in T193_COUNTS:
        side = select.evand_exact_side(n)
        assert isinstance(side, select.exact_sides.Algebraic), n
        cut = Fraction(printed[str(n)])
        assert cut < side < cut + Fraction(1, 10**40), n
        house = selections[n].house
        assert house is not None, n
        assert house.result == "T-193", n
        assert house.side == side, n
        assert select.PENDING_ADOPTION[n] == select.Pending(
            house="T-193", bead=select.WRITER_BEAD, why=select.NO_WRITER
        ), n


def test_the_t193_reader_refuses_a_count_it_does_not_state_or_an_interval_off_the_source(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The reader holds each tabulated interval inside the source's own and refuses a count
    the table does not state, as a reader defect `--check` names, never a side."""
    with pytest.raises(select.exact_sides.ExactSideError, match="no exact side"):
        select.evand_exact_side(5)
    row = dict(select._evand_exact_rows()[126])  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    low, high = (Fraction(end) for end in row["source_interval"])
    row["interval"] = [str(low - 1), str(high)]
    monkeypatch.setattr(select, "_evand_exact_rows", lambda: {9126: row})
    with pytest.raises(select.exact_sides.ExactSideError, match="not within the source's"):
        select.evand_exact_side(9126)


def test_a_held_count_restaged_for_a_smaller_house_names_it_and_becomes_history() -> None:
    """At the twelve counts where T-193 is below T-174's held side, the held sentence names
    the staged house, its bead and the side it passes, and a later pass's move turns it into
    history like every other held sentence (`adopt_houses.held_history`)."""
    sentence = (
        "The case keeps its house until T-193’s adoption, staged under think-ot5c, moves it "
        "to T-193’s side, below T-174’s, once the writer takes an algebraic side."
    )
    assert adopt._keeps_until(88, "T-174", "its house") == sentence  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    # A count staged for its own held house names that house's adoption: 70, under the
    # writer's bead, since the adoption of 19 October 2026 took 236, the last rational
    # count staged for T-174, to issue 659's certificate (T-218).
    assert adopt._keeps_until(70, "T-174", "its house") == (  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
        "The case keeps its house until T-174’s adoption, staged under think-ot5c, moves it "
        "to T-174’s side."
    )
    tail = sentence.split(" until ", 1)[1]
    for n in sorted(set(T193_COUNTS) - set(T193_BELOW_T186)):
        assert tail in _flat(select.case_path(n).read_text(encoding="utf-8")), n
    lead = "T-174 at $1$, `1e-19` below this house, is confirmed here"
    history = f"{lead}. {adopt.lifted_sentence('T-174')}"
    wrapped = f"{history} {sentence.replace('its house', 'this house')}".replace(
        " until ", "\nuntil "
    )
    assert _flat(adopt.held_history(wrapped)) == history


def test_every_staged_count_names_its_house_and_bead_in_its_record() -> None:
    """Every count staged for adoption says so in its record, with the house and the bead
    it waits under, and, where it waits for the writer, that it moves the case once the
    writer takes an algebraic side: the held and algebraic sentences of #660, and the
    sentences for a smaller house validated after the pass that wrote the record
    (`adopt_houses.staged_sentences`, #658). At all sixteen of T-193's counts the record
    also says what T-193 is and which review accepted it (review B3 of #658)."""
    for n, pending in select.PENDING_ADOPTION.items():
        text = _flat(select.case_path(n).read_text(encoding="utf-8"))
        assert f"staged under {pending.bead}," in text, n
        assert f"moves it to {pending.house}’s side" in text, n
        if pending.why == select.NO_WRITER:
            assert "once the writer takes an algebraic side." in text, n
    review = "../../docs/project/reviews/review-2026-10-16-evand-exact-sides-639.md"
    for n in T193_COUNTS:
        text = _flat(select.case_path(n).read_text(encoding="utf-8"))
        assert "T-193’s exact algebraic side at this count, a root of a degree-" in text, n
        assert f"accepted by the [review of 16 October 2026]({review})" in text, n


def test_an_algebraic_sentence_at_a_count_restaged_for_a_smaller_house_names_it(
    recorded: dict[int, select.Selection], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Review B3 of #658: `algebraic_sentences` closed with its own result's adoption even
    where a smaller house is staged in its place. No count reaches that today; with 70
    staged for another house, the sentence names that house's adoption and its bead."""
    staged = select.Pending(house="T-900", bead="think-test", why=select.NO_WRITER)
    monkeypatch.setitem(select.PENDING_ADOPTION, 70, staged)
    (sentence,) = adopt.algebraic_sentences(recorded[70], houses.side(70))
    assert sentence.startswith("T-174’s algebraic certificate at this count")
    assert "house rule of 16 October 2026 ended that wait." in sentence
    assert sentence.endswith(
        "The case keeps this house until T-900’s adoption, staged under think-test, moves "
        "it to T-900’s side, below T-174’s, once the writer takes an algebraic side."
    )


def test_t193s_adoption_waits_for_re1s_correction_at_nine_counts(
    selections: dict[int, select.Selection],
) -> None:
    """Review B1 of #658: at nine counts T-193's regularization item names T-174 or T-186
    as the packing the form solves, which RE-1 of its stage 4 review measured to be the
    case's own house. Each is recorded as a correction owed, under think-8ido, which
    `bead tree` holds open while it stands, and it holds the register as it is: the item
    still names the refuted `of` and the house is still T-193."""
    measured = {
        88: "T-127", 126: "T-139", 175: "T-158", 199: "T-127", 204: "T-162", 232: "T-158",
        266: "T-119", 292: "T-146", 301: "T-098",
    }  # fmt: skip
    assert {n: owed.measured for n, owed in select.CORRECTIONS_OWED.items()} == measured
    for n, owed in select.CORRECTIONS_OWED.items():
        house = selections[n].house
        assert house is not None, n
        assert (house.result, house.regularizes) == ("T-193", owed.named), n
        assert owed.named in {"T-174", "T-186"}, n
        assert (owed.bead, owed.measured_in) == ("think-8ido", select.REVIEW_639), n
        assert select.owed_correction(n, house) == owed, n
        assert (f"select_houses.CORRECTIONS_OWED n={n} (T-193 of {owed.named})", owed.bead) in (
            select.deferrals()
        ), n
    assert select.correction_problems(selections) == []


def test_the_writer_never_writes_the_uncorrected_of(
    selections: dict[int, select.Selection], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Review B1 of #658: the writer takes a house's credit from its regularization item,
    so it must refuse T-193 where the item names the refuted `of`, even once the pull
    request that adopts T-193 has taken its counts off `PENDING_ADOPTION`. This fails if
    the writer would write the uncorrected `of` at any of the nine counts; where the item
    stands (102) the writer's only refusal is its algebraic one, and once the item is
    corrected the correction no longer refuses and `--check` asks for its removal."""
    monkeypatch.setattr(
        select,
        "PENDING_ADOPTION",
        {n: p for n, p in select.PENDING_ADOPTION.items() if p.house != "T-193"},
    )
    for n, owed in select.CORRECTIONS_OWED.items():
        with pytest.raises(adopt.AdoptionError, match=f"names {owed.named} .*think-8ido"):
            adopt.plan({n: selections[n]})
    with pytest.raises(adopt.AdoptionError, match="algebraic side"):
        adopt.plan({102: selections[102]})
    house = selections[88].house
    assert house is not None
    corrected = dataclasses.replace(
        selections[88], house=dataclasses.replace(house, regularizes="T-127")
    )
    assert select.owed_correction(88, corrected.house) is None  # pyright: ignore[reportArgumentType]
    with pytest.raises(adopt.AdoptionError, match="algebraic side"):
        adopt.plan({88: corrected})
    problems = select.correction_problems({**selections, 88: corrected})
    assert problems == [
        (
            "FAIL: n=88: T-193's regularization item names T-127, not T-174, so the "
            "correction think-8ido owed has landed; take it off CORRECTIONS_OWED"
        )
    ]


def test_t193s_exact_sides_table_is_the_retained_packets() -> None:
    """Review B2 of #658: T-193's reader takes its sides from the intake's table, which no
    gate held to the packet. Every T-193 row is the packet's own: at the fourteen counts
    the packet retains, the file's digest, polynomial and isolating interval; at the two it
    pins by digest only (204 and 267), the manifest's digest."""
    packet = select.ROOT / "resources/web/evand-exact-cur-2026-10-16"
    manifest = {
        path.removeprefix("./"): digest
        for digest, path in (
            line.split(maxsplit=1)
            for line in (packet / "acquisition/upstream-subtree.sha256")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        )
    }
    rows = json.loads(select.EVAND_EXACT_SIDES.read_text(encoding="utf-8"))["rows"]
    retained = []
    for row in (row for row in rows if row["n"] in T193_COUNTS):
        name = f"search/exact/cur/data/n-{row['n']}.minpoly.json.gz"
        assert row["sha256"] == manifest[name], row["n"]
        path = packet / "source" / name
        if not path.is_file():
            assert row["n"] in (204, 267), row["n"]
            continue
        retained.append(row["n"])
        data = path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == row["sha256"], row["n"]
        side = json.loads(gzip.decompress(data))["S"]
        assert [int(c) for c in side["poly"]] == [
            int(c) for c in row["polynomial_low_to_high"]
        ], row["n"]
        assert [Fraction(end) for end in side["interval"]] == [
            Fraction(end) for end in row["source_interval"]
        ], row["n"]
        assert row["degree"] == len(side["poly"]) - 1, row["n"]
    assert len(retained) == 14


def test_a_reader_makes_an_unread_source_a_candidate_and_the_writer_waits_for_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Review A8 of #660: the route this branch gives #658, a reader in
    `ALGEBRAIC_READERS`, and the writer's refusal of an algebraic house, were untested.
    A registered reader makes the unread entry a candidate; its algebraic side below the
    case moves the house, which `--check` requires to be staged as the writer's, and
    `plan` refuses it unstaged, skips it staged, and never writes it as a fraction."""
    key = "[Ellsworth n69 2026-09-24]"
    results = [entry for entry in select.load_results() if entry["id"] == "T-088"]
    case = select.load_case(69)
    side = _below(case.verified)
    monkeypatch.setitem(select.ALGEBRAIC_READERS, key, lambda _n: side)
    unread: list[str] = []
    selected = select.select(results, select.load_evidence(), cases={69: case}, unread=unread)
    assert unread == []
    house = selected[69].house
    assert house is not None
    assert (house.result, house.algebraic, house.side) == ("T-088", True, side)
    monkeypatch.setattr(select, "PENDING_ADOPTION", {})
    assert select.check(selected)[0].startswith("FAIL: a validated smaller packing")
    with pytest.raises(adopt.AdoptionError, match="algebraic side"):
        adopt.plan(selected)
    staged = select.Pending(house="T-088", bead="think-test", why=select.NEXT_PULL_REQUEST)
    monkeypatch.setattr(select, "PENDING_ADOPTION", {69: staged})
    assert "stage it as 'no writer'" in select.check(selected)[0]
    staged = dataclasses.replace(staged, why=select.NO_WRITER)
    monkeypatch.setattr(select, "PENDING_ADOPTION", {69: staged})
    assert select.check(selected) == []
    assert adopt.plan(selected) == []
    with pytest.raises(adopt.AdoptionError, match="states rational sides"):
        adopt.rational(side)
    assert adopt.rational(Fraction(5, 2)) == Fraction(5, 2)
    shown = adopt.display(side)
    assert shown == select.ceiling(side)
    assert Fraction(shown) > side
    with pytest.raises(ValueError, match="staged for one of"):
        select.Pending(house="T-088", bead="think-test", why="until the owner decides")


def test_a_rational_house_staged_for_the_writer_fails_the_check(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The writer's gap stages an algebraic house and nothing else (review A1 of #660)."""
    entry, evidence = _confirmed_entry()
    monkeypatch.setitem(select.reports.HOUSES, "[test]", lambda _n: Fraction(3))
    monkeypatch.setattr(select, "_side", lambda _key, _n: Fraction(3))
    case = select.Case(
        n=7, verified=Fraction(4), reported=Fraction(4), source_key="", evidence=()
    )
    selected = select.select([entry], evidence, cases={7: case})
    staged = select.Pending(house="T-900", bead="think-test", why=select.NO_WRITER)
    monkeypatch.setattr(select, "PENDING_ADOPTION", {7: staged})
    (problem,) = select.check(selected)
    assert "the writer writes it, so stage it for the next pull request" in problem


def test_the_staged_adoptions_name_their_beads_and_reasons() -> None:
    """Review A1 of #660: the staged adoption sat under the policy lane's own bead, with no
    reason. T-174's rational houses wait for the adoption's bead and the next pull request,
    and its algebraic ones, and T-193's (#658), for the writer's bead and the writer.
    The adoption of 17 October 2026 (think-3mry) took 37 rational counts off; twelve
    others are staged for T-193, the adoption of 19 October 2026 took 236 to issue 659's
    certificate and 155 to issue 669's, and the adoption of 20 October 2026 took 308 to
    issue 689's."""
    for n, pending in select.PENDING_ADOPTION.items():
        assert pending.why in select.STAGING_REASONS, n
        algebraic = n in (70, 153, 207) or pending.house == "T-193"
        assert (pending.bead, pending.why) == (
            (select.WRITER_BEAD, select.NO_WRITER)
            if algebraic
            else (select.ADOPTION_BEAD, select.NEXT_PULL_REQUEST)
        ), n
    assert "think-sa5r" not in {pending.bead for pending in select.PENDING_ADOPTION.values()}
    adopted = set(houses.numbers_of("T-174"))
    assert adopted == {
        n for n in houses.LATER_PASSES["2026-10-17"] if houses.ADOPTED[n] == "T-174"
    }
    assert len(adopted) == 35
    assert not adopted & set(select.PENDING_ADOPTION)


def test_the_retained_integration_diagnostic_keeps_its_executed_bytes() -> None:
    """The archived reviewer program is parsed, never imported or rerun as assurance."""
    packet = houses.ROOT / "resources/web/t174-adoption-integration-diagnostic-2026-10-19"
    receipt = json.loads((packet / "retention.json").read_text())
    assert receipt["format"] == "retained-integration-diagnostic-v1"
    assert receipt["cited_by"] == []
    assert receipt["rerun_on_retention"] is False
    assert {row["path"] for row in receipt["files"]} == {
        "665-prospective-audit.py",
        "665-prospective-audit.json",
        "665-prospective-audit-README.md",
        "665-prospective-final-review.md",
    }
    for row in receipt["files"]:
        raw = (packet / row["path"]).read_bytes()
        assert len(raw) == row["bytes"]
        assert hashlib.sha256(raw).hexdigest() == row["sha256"]
    source = packet / "665-prospective-audit.py"
    compile(source.read_bytes(), str(source), "exec", dont_inherit=True)
    assert json.loads((packet / "665-prospective-audit.json").read_text())["failures"] == []
    for register in ("evidence.yaml", "verifiers.yaml"):
        assert (
            packet.relative_to(houses.REPO).as_posix()
            not in (houses.ROOT / "frontier" / register).read_text()
        )


def test_the_historical_custody_receipt_is_retained_separately_from_the_union() -> None:
    packet = houses.ROOT / "resources/web/t174-adoption-integration-diagnostic-2026-10-19"
    retention = json.loads((packet / "historical-65-house-custody-retention.json").read_text())
    assert retention["format"] == "historical-house-custody-retention-v1"
    assert retention["source_ref"] == "34903e701bb8a73d6a65f419525c354743bd94b7"
    assert retention["source_path"] == "packing/devtools/house-custody-2026-10-11.json"
    raw = (packet / retention["path"]).read_bytes()
    assert len(raw) == retention["bytes"] == 31822
    assert (
        hashlib.sha256(raw).hexdigest()
        == retention["sha256"]
        == ("e2366300564a93226ffd479d78883ec688e9c11fc8b3a88d8ae24191f08eb39e")
    )
    historical = json.loads(raw)
    assert historical["format"] == houses.CUSTODY_FORMAT
    assert historical["outcome"] == "PASS"
    assert len(historical["houses"]) == 65
    assert "29" not in historical["houses"]
    # The houses as the 17 October passes left them: the adoption of 19 October 2026 moved
    # 155, 236 and 271 to Evan Daniel's certificates and first adopted 229 and 183 (T-220,
    # think-jh4w), and the adoption of 20 October 2026 moved 154 and 308 to his issue-694
    # and issue-689 certificates (T-222, T-221), after this receipt was retained.
    later = {
        155: "T-197",
        183: "T-220",
        229: "T-199",
        236: "T-218",
        271: "T-219",
        154: "T-222",
        308: "T-221",
    }
    before = {
        **houses.ADOPTED,
        154: "T-186",
        155: "T-174",
        236: "T-146",
        271: "T-186",
        308: "T-174",
    }
    del before[229]
    del before[183]
    assert "183" not in historical["houses"]
    assert {n: houses.ADOPTED[n] for n in later} == later
    assert historical["houses"] == {str(n): result for n, result in before.items() if n != 29}
    assert {int(n) for n, result in historical["houses"].items() if result == "T-174"} == (
        set(houses.numbers_of("T-174")) | {155, 308}
    )


def test_check_judges_the_whole_register_and_refuses_since() -> None:
    """Review A9 of #660: narrowed to entries registered since a day, `--check` judged the
    staged counts without the entries they were staged for and advised unstaging all 63."""
    with pytest.raises(SystemExit) as refused:
        select.main(["--since", "2026-10-16", "--check"])
    assert refused.value.code == 2


def test_an_unread_print_that_only_overlaps_its_ceiling_is_unordered(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Review A10 of #660: an unread entry was compared by its print, and two spans that
    overlap read as equal, which orders nothing. `--check` fails on such an entry until a
    reader holds its side; a print that is the ceiling exactly is a tie and passes."""
    from devtools import check_standing as standing  # noqa: PLC0415
    from devtools import render_recent_results as view  # noqa: PLC0415

    assert select.unread_unordered(["T-088", "T-089", "T-114"]) == {}
    ceiling = view.load_records().cases[69]["verified_upper_bound"]
    floor, _top = view.span(ceiling)

    def meeting(slack: Fraction, value: Fraction) -> Any:
        def found(record: Any, _records: Any) -> list[standing.Finding]:
            if str(record["id"]) != "T-088":
                return []
            stated = standing.Stated(value, slack)
            return [standing.Finding(69, standing.UPPER, stated, standing.EQUAL, None)]

        return found

    monkeypatch.setattr(standing, "findings", meeting(Fraction(1, 10**4), floor))
    assert select.unread_unordered(["T-088"]) == {"T-088": [69]}
    monkeypatch.setattr(standing, "findings", meeting(Fraction(0), floor))
    exact = floor == _top
    assert select.unread_unordered(["T-088"]) == ({} if exact else {"T-088": [69]})


def test_a_side_no_route_here_holds_is_unordered_never_a_traceback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Review B3 of #660: a closed form whose minimal polynomial `sqpack.field` cannot
    decide irreducible, and a reader that cannot hold a side, crashed the selection. The
    form makes its count unordered, and the side is named for `--check` to fail on."""
    value, form = select.closed_form("5.3823323", "sqrt(2) + sqrt(3) + sqrt(5)")
    assert value is None
    assert form is not None
    assert form.startswith("the form's polynomial is not held exactly")
    entry, evidence = _confirmed_entry()

    case = select.Case(
        n=7, verified=Fraction(4), reported=Fraction(4), source_key="", evidence=()
    )
    # Review C2 of #660: a reader that builds its field from a packet, as T-193's will,
    # raises `FieldPreconditionError` where `sqpack.field` cannot certify the field.
    for error in (
        select.exact_sides.ExactSideError("a reader's side it cannot isolate"),
        FieldPreconditionError("a field sqpack.field cannot certify"),
    ):

        def unheld_side(_n: int, error: Exception = error) -> select.exact_sides.Side:
            raise error

        monkeypatch.setitem(select.ALGEBRAIC_READERS, "[test]", unheld_side)
        unheld: list[str] = []
        assert select.select([entry], evidence, cases={7: case}, unheld=unheld) == {}
        assert unheld == [f"T-900 at n = 7: {error}"]


def test_the_ceiling_rounds_up_and_the_display_ends_where_the_side_does() -> None:
    assert select.ceiling(Fraction(1, 3), 4) == "0.3334"
    assert select.ceiling(Fraction(18)) == "18.0000000000000000"
    assert adopt.display(Fraction(11986956226066, 10**12)) == "11.986956226066"
    assert adopt.display(Fraction(1, 3)) == "0.3333333333333334"


def test_every_adopted_house_rebuilds_from_its_private_inputs() -> None:
    houses.check_houses()


def test_the_house_inputs_are_ordinary_private_copies_of_every_worker() -> None:
    from devtools import run_negative_controls as controls  # noqa: PLC0415

    inputs = houses.private_input_paths()
    assert set(inputs) <= set(controls.COPY_SEPARATELY)
    assert all(path.is_file() and not path.is_symlink() for path in inputs)
    leaves = {path.relative_to(controls.ROOT) for path in houses.snapshot_house_links()}
    assert leaves <= controls.HOUSE_LINK_LEAVES


def test_a_late_verdict_in_a_receipt_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    rows = houses.receipt_cases(houses.receipt_of(70), "evand-regularized-exact-replay-v1")
    forged = [
        {**row, "exact_verify": {**row["exact_verify"], "verification_passed": True}}
        if row["n"] == 70 and row["control"] == houses.kernel.JOBS[2]
        else row
        for row in rows
    ]
    monkeypatch.setattr(houses, "receipt_cases", lambda _path, _form: tuple(forged))
    with pytest.raises(houses.kernel.ReportError):
        houses.expected_house(70)


def test_the_adopted_case_records_and_coverage_are_at_their_houses(
    selections: dict[int, select.Selection],
) -> None:
    assert adopt.check() == []
    assert adopt.plan(selections) == []


def test_the_receipt_of_the_custody_run_names_every_input_and_house() -> None:

    receipt = safe_load(houses.CUSTODY_RECEIPT.read_text(encoding="utf-8"))
    assert receipt["format"] == houses.CUSTODY_FORMAT
    assert receipt["outcome"] == "PASS"
    assert receipt["houses"] == {str(n): result for n, result in houses.ADOPTED.items()}
    recorded = {row["path"] for row in receipt["inputs"]}
    assert recorded == {
        path.relative_to(houses.REPO).as_posix() for path in houses.private_input_paths()
    }
    # Each input is still the file custody read: a changed one fails until custody runs
    # again (`python -m devtools.upper_bound_houses custody`).
    for row in receipt["inputs"]:
        raw = (houses.REPO / row["path"]).read_bytes()
        assert (row["bytes"], row["sha256"]) == (len(raw), hashlib.sha256(raw).hexdigest())
    assert len(receipt["mutations_refused_and_restored"]) == 2 * len(houses.sources())
    assert set(receipt["mutations_refused_and_restored"]) == {
        f"{result} n={min(houses.numbers_of(result))}: {kind}"
        for result in houses.sources()
        for kind in ("outside-control verdict", "certificate bytes")
    }
    assert receipt["fresh_geometric_deciders"] is False
    assert receipt["original_inputs_byte_equal"] is True
    assert receipt["restored_worker_inputs_byte_equal"] is True
    assert receipt["child_timeout_seconds"] == houses.CUSTODY_TIMEOUT == 120
    # Capacity is assessed against the current allowance. The retained operation's
    # recorded 216 MiB limit and its over-limit measurement stay raw: raising the
    # allowance does not turn them into a claim that the old run met its old limit.
    # All source inputs and every mutation/refusal above must still match this tree.
    assert receipt["snapshot_cap_bytes"] <= controls.SNAPSHOT_MAX_BYTES
    assert receipt["snapshot_source_bytes"] <= controls.SNAPSHOT_MAX_BYTES


def test_the_prior_state_keeps_every_moved_record_as_it_stood_before(
    prior: dict[int, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Each record was retained before the move: at another source, above its house."""
    assert sorted(prior) == list(houses.NUMBERS)
    for n, text in prior.items():
        packing = safe_load(text.split("---\n", 2)[1])["packing"]
        assert packing["n"] == n
        assert packing["reported_upper_bound"]["source_key"] != houses.source_for(n).key
        assert Fraction(packing["verified_upper_bound"]["exact_form"]) > houses.side(n)
    # Retaining again keeps the first text and writes only a count not yet retained; the
    # archive is never written here.
    first = houses.ADOPTED_ON
    saved: list[Any] = []
    monkeypatch.setattr(houses.kernel, "save_xz", lambda _path, value: saved.append(value))
    adopt.retain_history(first, {70: "a later text is not the prior state"})
    assert saved == []
    adopt.retain_history(first, {70: "a later text", 999: "a count not yet retained"})
    (record,) = saved
    assert record["adopted_on"] == first
    rows = {row["n"]: row["frontier"] for row in record["cases"]}
    assert rows == {**adopt.read_pass(first), 999: "a count not yet retained"}


def test_each_pass_keeps_the_records_it_moved_as_that_pass_read_them(
    prior: dict[int, str], latest: dict[int, str]
) -> None:
    """One archive per pass: a count moved twice is in both, as each pass found it.

    The earlier archive keeps the record before the adoption first moved it, and the
    later one the record as the earlier pass left it, at that pass's house and dated by
    it; the writer is replayed from the later one and the history readers read the first.
    """
    assert adopt.passes()[0] == houses.ADOPTED_ON
    archives = {day: adopt.read_pass(day) for day in adopt.passes()}
    for day, counts in houses.LATER_PASSES.items():
        assert set(archives[day]) == counts
    first = archives[houses.ADOPTED_ON]
    assert {n for n in houses.ADOPTED if houses.adopted_on(n) == houses.ADOPTED_ON} <= set(
        first
    )
    again: set[int] = set()
    for index, day in enumerate(adopt.passes()):
        for n in sorted(archives[day]):
            earlier = [d for d in adopt.passes()[:index] if n in archives[d]]
            if not earlier:
                assert prior[n] == archives[day][n]
                continue
            again.add(n)
            # As the earlier pass left it: at that pass's house, dated that day, or later
            # where the one writer that ran between the passes moved the date on,
            # `apply_closed_form`, to its intake of 14 October 2026.
            packing = _front(archives[day][n])
            assert packing["source_reviewed"] in {
                earlier[-1],
                max(earlier[-1], closed_form.INTAKE),
            }
            assert f"**House adoption, {adopt.words(earlier[-1])}.**" in archives[day][n]
            assert prior[n] == archives[earlier[0]][n] != archives[day][n]
    assert again, "no count has been adopted twice"
    assert {n for n in houses.ADOPTED if prior[n] != latest[n]} == again


#: The front-matter keys `adopt_houses.front_matter` writes; every other key is the draft's
#: or another tool's.
OWNED = (
    "source_reviewed",
    "reported_upper_bound",
    "verified_upper_bound",
    "conjectured_optimum",
    "priority_notes",
    "evidence",
    "resources",
    "blockers",
)


def _front(text: str) -> dict[str, Any]:
    return dict(safe_load(text.split("---\n", 2)[1])["packing"])


def _flat(text: str) -> str:
    return " ".join(text.split())


def _body(text: str) -> str:
    """A record's body as the writer is answerable for it (`adopt_houses.history_words`).

    The counts the first pass marked by hand (`adopt_houses.HAND_MARKED`) are compared
    only in their owned parts."""
    return adopt.history_words(text.split("---\n", 2)[2])


N108_LOWER_INTRO = r"""**Fine-net lower bound, 18 October 2026.** The certificate
`mixed_n108_L1062`, published by wand125 on 16 October, raises both lower lanes to
$s(108) \ge 531/50 = 10.62$. Its exact nonnegative rectangle measure has total mass
$10799999/100000 < 108$. The retained maintained `sqverify-fast` census verifies capture
at every centre in all 201 declared-net directions, and its whole-net control receipt
refuses the scaled mutants. The two accepted mathematical reviews check the
certificate’s implication and premises; the separate exact audits check saved points.
No native verifier was rerun during those reviews or this adoption. The producer’s
checker and the maintained replay share `sqverify_fast` components, so this is shared
component confirmation. It establishes neither independent full confirmation nor
optimality. The upper lanes remain unchanged."""

N108_CURRENT_LOWER = r"""The current verified lower bound is $s(108) \ge 531/50 = 10.62$,
from Hiroaki Hosono’s fine-net measure and the maintained replay described above. That
confirmation shares the producer’s verifier components."""


def _n108_later_lower_projection(held: dict[str, Any], wrote: dict[str, Any], body: str) -> str:
    """Check the exact later n108 lower adoption, then compare the earlier house layer."""
    assert held["source_reviewed"] == "2026-10-18"
    assert held["reported_lower_bound"]["exact_form"] == "531/50"
    assert held["verified_lower_bound"] == {
        "value": "10.62",
        "exact_form": "531/50",
        "evidence": ["E-wand125-fine-net-n108-1062-sqverify-fast-replay"],
    }
    assert held["evidence"] == [
        *wrote["evidence"],
        "E-wand125-fine-net-n108-1062-report",
        "E-wand125-fine-net-n108-1062-sqverify-fast-replay",
        "E-n108-review-max-premises",
        "E-n108-review-max-captures",
    ]
    assert held["resources"] == [
        *wrote["resources"],
        {
            "key": "[wand125 fine-net lower bounds 2026-10-16]",
            "role": "lower-bound-proof",
            "local": "packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16",
            "url": (
                "https://github.com/wand125/square-packing/tree/"
                "6af3c00991c937d40ac0fe867fe049b8e9f3bf2d/problems/"
                "square-lower-bounds/certificates/mixed_n108_L1062"
            ),
            "retrieved": True,
        },
    ]
    for key in ("source_reviewed", "evidence", "resources"):
        held[key] = wrote[key]
    for addition in (N108_LOWER_INTRO, N108_CURRENT_LOWER):
        words = _flat(addition)
        assert body.count(words) == 1
        body = body.replace(words, "", 1)
    # Only these explicit historical adjustments accompany the lower adoption.
    for current, prior in (
        ("so the reported lower bound here was", "so the reported lower bound here is now"),
        (
            "no record of it has been replayed here; it remains a historical reported bound.",
            "no record of it has been replayed here, so the verified lower bound is unchanged.",
        ),
        (
            "Karakuş’s general bound supplied the earlier verified lower bound. It applies",
            (
                "The strongest lower bound independently verified in this record is "
                "Karakuş’s general bound, which applies"
            ),
        ),
        (
            (
                "which stood above that earlier Karakuş bound and was recorded "
                "as a reported bound."
            ),
            "which is stronger at this $n$ and is now recorded as a reported bound.",
        ),
    ):
        assert body.count(current) == 1
        body = body.replace(current, prior, 1)
    return _flat(body)


#: The fine-net lower validations of 19 October 2026 at two T-174 houses: each count's
#: result, candidate, lower bound, its review, the bound it replaced, and the one phrase
#: of the earlier house paragraph the validation moved into the past tense.
FINE_NET_LOWER_19_OCTOBER: dict[int, tuple[str, str, str, str, str, str, str]] = {
    68: (
        "T-205",
        "mixed_n68_L853",
        "853/100",
        "8.53",
        "n68-fine-net-mathematics",
        "851/100",
        "the strongest verified lower bound",
    ),
    84: (
        "T-206",
        "mixed_n84_L94225",
        "3769/400",
        "9.4225",
        "n84-n85-fine-net-mathematics",
        "9411/1000",
        "and the verified lower bound",
    ),
}


def _fine_net_lower_projection(
    n: int, held: dict[str, Any], wrote: dict[str, Any], body: str
) -> str:
    """Check a 19 October fine-net lower validation, then compare the house layer below it.

    T-205 and T-206 raised both lower lanes at 68 and 84 after the T-174 adoption of 17
    October wrote those records, as n108's fine-net bound did on 18 October; the writer
    owns neither lane, so the validation is checked exactly and projected out.
    """
    result, candidate, exact, value, review, earlier, phrase = FINE_NET_LOWER_19_OCTOBER[n]
    tag = candidate.removeprefix("mixed_").replace("_L", "-").lower()
    assert held["source_reviewed"] == "2026-10-19"
    assert held["reported_lower_bound"]["exact_form"] == exact
    assert held["verified_lower_bound"] == {
        "value": value,
        "exact_form": exact,
        "evidence": [f"E-wand125-fine-net-{tag}-sqverify-fast-replay"],
    }
    assert held["evidence"] == [
        f"E-wand125-fine-net-{tag}-report",
        f"E-wand125-fine-net-{tag}-sqverify-fast-replay",
        f"E-n{n:03d}-fine-net-review-premises",
        f"E-n{n:03d}-fine-net-review-captures",
        *wrote["evidence"],
    ]
    assert held["resources"] == [
        {
            "key": "[wand125 fine-net lower bounds 2026-10-16]",
            "role": "lower-bound-proof",
            "local": "web/wand125-fine-net-lower-bounds-2026-10-16",
            "url": "https://github.com/wand125/square-packing",
            "retrieved": True,
        },
        *wrote["resources"],
    ]
    for key in ("source_reviewed", "evidence", "resources"):
        held[key] = wrote[key]
    intro = (
        f"**Fine-net validation, 19 October 2026 ({result}).** The retained candidate "
        f"`{candidate}` raises both lower lanes from ${earlier}$ to ${exact}$. The complete "
        "201-direction maintained native replay and [mathematical "
        f"review](../../docs/project/reviews/review-2026-10-19-{review}.md) confirm it by a "
        "re-implementation sharing components with the producer’s checker, wand125’s "
        "adaptation of this repository’s `sqverify_fast` crate, apart from the declared-net "
        "readers. The exact audits check premises and saved poses only. The original 18 source "
        "reports and historical native receipts remain retained."
    )
    words = _flat(intro)
    assert body.count(words) == 1, f"n={n}: fine-net introduction"
    body = body.replace(words, "", 1)
    # The one historical adjustment that accompanies each validation.
    current, prior = f"{phrase} then was", f"{phrase} is"
    assert body.count(current) == 1, f"n={n}: {current}"
    return _flat(body.replace(current, prior, 1))


def test_the_writer_rebuilds_every_adopted_record_from_its_prior_state(
    replayed: list[adopt.Move],
) -> None:
    """Replaying `rewrite` on each record as its last pass read it gives the committed one.

    What the writer owns is compared: its front-matter keys, its opening paragraph and
    certificate section, and the rest of the body, which it marks as history, with
    whitespace collapsed, since flowmark rewraps it. The verifier table and the rigidity
    scope are refreshed by their own tools. A count adopted twice is replayed from the
    record the earlier pass left (`adopt_houses.before_last_pass`). A writer that ran
    after the adoption is replayed after it: `apply_closed_form`, of 14 October 2026,
    raises the reported lower lane, adds its evidence, resource and paragraph, and moves
    `source_reviewed` no earlier. The later fine-net lower adoptions, n108's of 18 October
    and n68's and n84's of 19 October, are checked explicitly and projected out before
    this historical upper-layer comparison.
    """
    assert [move.n for move in replayed] == sorted(houses.ADOPTED)
    for move in replayed:
        assert move.house.result == houses.ADOPTED[move.n]
        committed = select.case_path(move.n).read_text(encoding="utf-8")
        # The closed-form paragraph precedes the house-adoption paragraphs; n108's
        # later fine-net introduction precedes it. Its historical replay follows each
        # pass, including 15 October, which read records it had already raised.
        written = closed_form.replay(move.n, adopt.rewrite(move))
        held, wrote = _front(committed), _front(written)
        historical_body = _body(committed)
        if move.n == 108:
            historical_body = _n108_later_lower_projection(held, wrote, historical_body)
        elif move.n in FINE_NET_LOWER_19_OCTOBER:
            historical_body = _fine_net_lower_projection(move.n, held, wrote, historical_body)
        for key in OWNED:
            assert held.get(key) == wrote.get(key), f"n={move.n}: packing.{key}"
        body = _flat(committed.split("---\n", 2)[2])
        assert _flat(adopt.opening(move)) in body, f"n={move.n}: opening paragraph"
        assert _flat(adopt.section(move)) in body, f"n={move.n}: certificate section"
        if move.n not in adopt.HAND_MARKED:
            assert historical_body == _body(written), f"n={move.n}: the body as history"


#: A synthetic later pass, its review and its source: n = 84 adopted again after T-174.
LATER_DAY, REVIEWED, PUBLISHED = "2026-11-03", "2026-11-02", "2025-12-31"


def _readopted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, replayed: list[adopt.Move]
) -> tuple[adopt.Move, str, adopt.Move]:
    """n = 84 as its latest pass wrote it, and a move to T-900 on a later day.

    T-900 sits a millionth below T-174 with a source of its own in a copy of the coverage
    register; the later day is a pass of its own in `upper_bound_houses.LATER_PASSES`.
    """
    first = next(move for move in replayed if move.n == 84)
    written = adopt.rewrite(first)
    monkeypatch.setitem(houses.LATER_PASSES, LATER_DAY, frozenset({84}))
    house = select.Candidate(
        result="T-900",
        n=84,
        side=first.side - Fraction(1, 10**6),
        source_key="[new]",
        published=PUBLISHED,
        report_evidence=("E-new",),
        confirming_evidence=("E-new-replay",),
        regularizes=None,
    )
    monkeypatch.setitem(
        adopt.RESULTS,
        "T-900",
        adopt.Prose(author="A. Finder", reported="on no issue", producer_route=False, ai=""),
    )
    review = {"path": "docs/review-t900.md", "verdict": "accepted", "date": REVIEWED}
    entry = {
        "id": "T-900",
        "scope": {"n_values": [84]},
        "evidence": ["E-new", "E-new-replay"],
        "reviews": [review],
    }
    register = (*adopt._register(), entry)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    monkeypatch.setattr(adopt, "_register", lambda: register)
    bibliography = {**adopt._bibliography(), "[new]": {"dated": PUBLISHED}}  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    monkeypatch.setattr(adopt, "_bibliography", lambda: bibliography)
    source = "- id: new\n  source_key: '[new]'\n  url: https://example.invalid/new\n"
    text = adopt.COVERAGE.read_text(encoding="utf-8").replace(
        "\nsources:\n", f"\nsources:\n{source}  scope:\n    n_values: [84]\n", 1
    )
    monkeypatch.setattr(adopt, "COVERAGE", tmp_path / "source-coverage.yaml")
    adopt.COVERAGE.write_text(text, encoding="utf-8")
    case = select.parse_case(84, written)
    selection = select.Selection(
        n=84, case=case, house=house, candidates=(house, *first.selection.candidates)
    )
    packing = _front(written)
    return first, written, adopt.Move(selection, house, packing, written)


def test_a_count_adopted_again_on_a_later_day_has_one_current_house(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, replayed: list[adopt.Move]
) -> None:
    """A third adoption of a count reads as one current house and dated history.

    The earlier pass's paragraph, section and verified statement say until when they
    held; its house becomes a note from its day until this one; the review's date, the
    found year and `source_reviewed` come from the record; and the prose check passes.
    """
    from devtools import check_case_prose  # noqa: PLC0415

    first, written, again = _readopted(tmp_path, monkeypatch, replayed)
    before = _front(written)["reported_upper_bound"]
    record = adopt.rewrite(again)
    body = _flat(record.split("---\n", 2)[2])
    assert body.count("is now this case’s house") == 1
    assert body.count("**House adoption, ") == 3
    title = body.index("— open")
    assert body.index("**House adoption, 3 November 2026.**") == title + len("— open ")
    assert (
        "**House adoption, 11 October 2026.** Francisco Couzo’s refinement of Ryan Xu’s "
        "packing (T-130) was this case’s house until 17 October 2026:"
    ) in body
    assert "packing (T-174) was this case’s house until 3 November 2026:" in body
    assert "the verified upper bound until 3 November 2026: confirmed," in body
    assert "[review of 2 November 2026](../../docs/review-t900.md)" in body
    packing = _front(record)
    assert packing["source_reviewed"] == LATER_DAY
    assert packing["reported_upper_bound"]["found_year"] == 2025
    notes = [note["claim"] for note in packing["priority_notes"]]
    assert notes[:-1] == [note["claim"] for note in _front(written)["priority_notes"]]
    assert notes[-2].endswith(
        "the case’s ceiling from 11 October 2026 until 17 October 2026; its certificate "
        "and replay remain retained."
    )
    assert notes[-1] == (
        f"Earlier house {before['value']} from {before['source_key']}, the case’s ceiling "
        "from 17 October 2026 until 3 November 2026; its certificate and replay remain "
        "retained."
    )
    path = tmp_path / "n-084.md"
    path.write_text(record, encoding="utf-8")
    assert check_case_prose.check_case_file(path) == []
    assert adopt.adopted(dataclasses.replace(again, packing=packing))
    assert not adopt.adopted(dataclasses.replace(first, packing=packing))


def test_a_house_of_an_earlier_finders_packing_keeps_the_finders_year(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, replayed: list[adopt.Move]
) -> None:
    """The reported lane's year is the packing's: the house's own year unless its credit
    names an earlier one, as at 29, where PingYou Ltd's certificate of 2026 is of Thomas
    Schadt's packing of 2025 (review A's A7 of #661). The synthetic later house at 84
    takes its own year, published in 2025, unless its credit says otherwise (review C10)."""
    assert all(c.found_year is None for n, c in adopt.CREDITS.items() if n != 29)
    _, _, again = _readopted(tmp_path, monkeypatch, replayed)
    assert adopt.reported_bound(again)["found_year"] == date.fromisoformat(PUBLISHED).year
    earlier = dataclasses.replace(adopt.CREDITS[84], found_year=2019)
    monkeypatch.setitem(adopt.CREDITS, 84, earlier)
    assert adopt.reported_bound(again)["found_year"] == 2019
    at29 = next(move for move in replayed if move.n == 29)
    assert date.fromisoformat(at29.house.published).year == 2026
    assert adopt.reported_bound(at29)["found_year"] == 2025 == adopt.CREDITS[29].found_year
    lane = _front(select.case_path(29).read_text(encoding="utf-8"))["reported_upper_bound"]
    assert lane["found_by"] == list(adopt.CREDITS[29].found_by)
    assert lane["found_year"] == 2025


def test_a_house_that_is_the_replaced_packing_keeps_what_the_record_knew_of_it(
    replayed: list[adopt.Move],
) -> None:
    """At 29 the house is the catalogue's packing measured pose for pose, no square turned
    beyond 1e-9 degrees (T-195's regularization of T-009), so the reported lane keeps the
    packing's facts: analytically optimized, found by simulated annealing, its six tilt
    angles, which the certificate reach reads for its cap. No other credit says so, and a
    house of another packing knows none of them (review C6 of #661)."""
    assert [n for n, c in adopt.CREDITS.items() if c.same_packing] == [29]
    at29 = next(move for move in replayed if move.n == 29)
    replaced = at29.packing["reported_upper_bound"]
    written = adopt.reported_bound(at29)
    for field in adopt.PACKING_FACTS:
        assert written[field] == replaced[field], field
    assert written["construction_method"] == "simulated-annealing"
    assert len(written["tilt_angles_deg"]) == 6
    (t195,) = (entry for entry in adopt._register() if entry["id"] == "T-195")  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    (item,) = t195["regularizations"]
    assert item["of"] == "T-009"
    assert item["identity"]["basis"] == "measured"
    assert float(item["identity"]["max_turn_deg"]) < 1e-9
    other = next(move for move in replayed if move.n == 84)
    assert adopt.reported_bound(other)["construction_method"] == "unknown"


@pytest.mark.parametrize(
    ("n", "printed", "prior_exact", "expected_margin"),
    [
        (
            84,
            "9.6979347990149214",
            Fraction(9697934799014921307163820128651, 10**30),
            "9.70e-20",
        ),
        (
            105,
            "10.78930378374815884",
            Fraction(
                "107893037837481588309268366600396176597362187114244213328843657546629045"
                "97598593330008796151"
            )
            / 10**90,
            "1.08e-79",
        ),
    ],
)
def test_equal_prior_displays_keep_the_exact_margin_separate_from_the_display_gap(
    replayed: list[adopt.Move],
    n: int,
    printed: str,
    prior_exact: Fraction,
    expected_margin: str,
) -> None:
    """Equal reported/verified prints still round away from the old exact certificate.

    At 84 and 105 the display gap is much larger than the genuine improvement (C1 of
    #665), so neither the new outward display nor the old print is its exact endpoint.
    """
    move = next(move for move in replayed if move.n == n)
    reported = move.packing["reported_upper_bound"]
    verified = move.packing["verified_upper_bound"]
    assert reported["value"] == verified["value"] == printed
    assert Fraction(str(reported["exact_form"])) == prior_exact
    assert Fraction(str(verified["exact_form"])) == prior_exact
    assert Fraction(printed) != prior_exact
    margin = prior_exact - move.side
    assert margin == move.selection.margin > 0
    rounded = Decimal(expected_margin)
    last_place = Fraction(Decimal(1).scaleb(int(rounded.as_tuple().exponent)))
    assert abs(Fraction(rounded) - margin) <= last_place / 2
    assert abs(Fraction(printed) - move.side - Fraction(rounded)) > last_place
    assert Fraction(str(adopt.reported_bound(move)["value"])) >= move.side
    opening = _flat(adopt.opening(move))
    assert "upper bound, rounded outward from its exact side." in opening
    assert (
        "The exact certificate side improves the previous verified exact side "
        f"by about `{expected_margin}`."
    ) in opening
    assert f"The earlier ceiling, displayed outward as ${printed}$ from" in opening
    assert f"`{expected_margin}` below the ceiling" not in opening


def test_an_opening_only_refresh_keeps_later_lower_bound_evidence_and_prose(
    replayed: list[adopt.Move], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The T216 lower adoption at 108 survives an upper-layer wording correction."""
    move = next(move for move in replayed if move.n == 108)
    committed = select.case_path(108).read_text(encoding="utf-8")
    marker = f"**House adoption, {adopt.day_words(108)}.**"
    old_before, old_after = committed.split(marker, 1)
    path = tmp_path / "n-108.md"
    path.write_text(old_before + marker + " Stale opening.\n\n" + old_after.split("\n\n", 1)[1])
    monkeypatch.setattr(adopt, "replay_plan", lambda: [move])
    monkeypatch.setattr(select, "case_path", lambda _n: path)
    assert adopt.main(["--refresh-openings"]) == 0
    refreshed = path.read_text()
    assert _front(refreshed) == _front(committed)
    new_before, new_after = refreshed.split(marker, 1)
    assert new_before == old_before
    assert new_after.split("\n\n", 1)[1] == old_after.split("\n\n", 1)[1]
    assert _flat(marker + new_after.split("\n\n", 1)[0]) == _flat(adopt.opening(move))
    _n108_later_lower_projection(
        _front(refreshed), _front(adopt.replayed_text(move)), _body(refreshed)
    )
    assert adopt.refreshed_opening(move, refreshed) == refreshed


def test_a_full_refresh_refuses_a_later_lower_layer_before_writing_any_record(
    replayed: list[adopt.Move], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An earlier pending opening cannot publish before n108's ownership check fails."""
    moves = [move for move in replayed if move.n in (29, 108)]
    assert [move.n for move in moves] == [29, 108]
    originals = {}
    for move in moves:
        text = select.case_path(move.n).read_text(encoding="utf-8")
        if move.n == 29:
            marker = f"**House adoption, {adopt.day_words(29)}.**"
            before, after = text.split(marker, 1)
            text = before + marker + " Stale opening.\n\n" + after.split("\n\n", 1)[1]
        path = tmp_path / f"n-{move.n:03d}.md"
        path.write_text(text)
        originals[path] = path.read_bytes()
    monkeypatch.setattr(adopt, "replay_plan", lambda: moves)
    monkeypatch.setattr(select, "case_path", lambda n: tmp_path / f"n-{n:03d}.md")
    assert adopt.main(["--refresh"]) == 1
    assert {path: path.read_bytes() for path in originals} == originals


def test_a_refresh_limited_to_named_counts_leaves_the_others_unread(
    replayed: list[adopt.Move], tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`--refresh --n` writes the named records and does not replay n108's later layer,
    which the full refresh refuses (review A1 of #692)."""
    moves = [move for move in replayed if move.n in (29, 108)]
    marker = f"**House adoption, {adopt.day_words(29)}.**"
    paths = {}
    for move in moves:
        text = select.case_path(move.n).read_text(encoding="utf-8")
        if move.n == 29:
            before, after = text.split(marker, 1)
            text = before + marker + " Stale opening.\n\n" + after.split("\n\n", 1)[1]
        paths[move.n] = tmp_path / f"n-{move.n:03d}.md"
        paths[move.n].write_text(text)
    untouched = paths[108].read_bytes()
    monkeypatch.setattr(adopt, "replay_plan", lambda: moves)
    monkeypatch.setattr(adopt, "held_counts", lambda: [108])
    monkeypatch.setattr(select, "case_path", lambda n: tmp_path / f"n-{n:03d}.md")
    assert adopt.main(["--refresh", "--n", "29"]) == 0
    assert "Stale opening." not in paths[29].read_text()
    assert _flat(adopt.opening(moves[0])) in _flat(paths[29].read_text())
    assert paths[108].read_bytes() == untouched
    with pytest.raises(SystemExit):
        adopt.main(["--check", "--n", "29"])


def test_an_adoption_marks_a_registration_pending_adoption_as_history() -> None:
    """The intake of 18 October 2026 wrote a fixed-form "pending adoption" paragraph for
    each report it registered at V0/C0; the adoption that moves the house marks it, and a
    sentence after it naming a report pending adoption, as history (review A1 of #692).
    155 is marked by hand (`HAND_MARKED`); 229 is the writer's, and so are 227 and 260,
    whose de Winter reports are still pending."""
    stale = (
        "Reported certificate pending adoption",
        "This V0/C0 registration leaves both case upper lanes",
        "Rigidity and arrangement notes below describe that retained house.",
    )
    history = (
        "Its V0/C0 registration left both case upper lanes, the house witness and its "
        "drawing unchanged until the house adoption of 19 October 2026, and until then the "
        "rigidity and arrangement notes below described that retained house."
    )
    for n, reported in ((155, "2026-10-17"), (229, "2026-10-18")):
        body = _flat(select.case_path(n).read_text(encoding="utf-8").split("---\n", 2)[2])
        assert not [words for words in stale if words in body], n
        opening = f"**Reported certificate, {reported}.** Evan Daniel reported a {n}-square"
        assert opening in body, n
        assert history in body, n
    body229 = _flat(select.case_path(229).read_text(encoding="utf-8"))
    assert "the latest registered report, pending adoption until 19 October 2026." in body229
    # The T-155 view's dated paragraph off T-101's side is history from the same pass.
    assert (
        "the verified upper bound until 19 October 2026 (T-155), which the record printed as "
        "$15.65685424949239$." in body229
    )
    assert "which the record still prints" not in body229
    for n in (227, 260):
        committed = select.case_path(n).read_text(encoding="utf-8")
        marked = _flat(adopt.pending_history(committed, "3 November 2026"))
        assert not [words for words in stale if words in marked], n
        assert f"Joost de Winter reported a {n}-square certificate" in marked, n
        assert "until the house adoption of 3 November 2026" in marked, n


def test_an_opening_refresh_keeps_the_following_old_bound_explicitly_historical(
    replayed: list[adopt.Move], tmp_path: Path
) -> None:
    """The earlier SQUISH upper at 258 remains history under the current house."""
    from devtools.check_case_prose import check_case_file  # noqa: PLC0415

    move = next(move for move in replayed if move.n == 258)
    committed = select.case_path(258).read_text(encoding="utf-8")
    path = tmp_path / "n-258.md"
    path.write_text(adopt.refreshed_opening(move, committed))
    assert "applied until this adoption and stays retained as history" in _flat(
        path.read_text()
    )
    assert check_case_file(path) == []


def test_where_the_replaced_lanes_differ_the_margin_is_read_from_the_verified_ceiling(
    replayed: list[adopt.Move],
) -> None:
    """The replaced displays differ at 29, 132 and 229. Their opening, section and history
    note use the exact verified baseline (reviews C3 and D1 of #661; M2/M3 of #665).
    At 29 the catalogue print orders nothing; at 132 the reported exact side agrees with
    the verified side, but its display differs from the verified display. 308's did too
    when T-174 replaced T-141 on 17 October 2026; the adoption of 20 October 2026 replays
    it from T-174's record, whose two lanes agree."""
    differing = {
        29: (
            Fraction(
                "296691673133846459484473030817600957/50000000000000000000000000000000000"
            ),
            "5.93383346267692",
            "5.93383346267692918974379895098",
            "T-155",
            "[Kingbird]",
            (
                "is a print `9.19e-15` below the new side, within one unit of its last place, "
                "so it does not order them"
            ),
        ),
        132: (
            Fraction("5992840099422904405761115982051/500000000000000000000000000000"),
            "11.985680198845808811522231964102",
            "11.9856801988458089",
            "T-141",
            "[Daniel record hunt 3 2026-10-10]",
            "lies `1.20e-19` above the new side",
        ),
        # The first adoption at 229 (19 October 2026): the catalogue's print of
        # 10 + 4 sqrt(2) above T-155's exact ceiling, both well above the new side.
        229: (
            Fraction("391421356237309504880168872421/25000000000000000000000000000"),
            "15.65685424949238",
            "15.65685424949239",
            "T-155",
            "[Kingbird]",
            "lies `6.69e-03` above the new side",
        ),
    }
    for n, (expected, printed, verified_display, result, source, relation) in differing.items():
        move = next(move for move in replayed if move.n == n)
        bound = move.packing["verified_upper_bound"]
        reported = move.packing["reported_upper_bound"]
        verified = Fraction(str(bound["exact_form"]))
        assert verified == expected
        assert reported["value"] == printed
        assert bound["value"] == verified_display
        assert adopt._lanes_differ(move.packing)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
        if n == 132:
            assert Fraction(str(reported["exact_form"])) == expected
        assert Fraction(str(bound["value"])) != verified
        margin = verified - move.side
        assert margin == move.selection.margin > 0
        opening = _flat(adopt.opening(move))
        baseline = re.search(r"The earlier exact ceiling, \$([^$]+)\$ from", opening)
        assert baseline is not None
        assert Fraction(baseline.group(1)) == verified
        stated_margin = re.search(
            r"exact certificate side improves the previous verified exact side "
            r"by about `([^`]+)`",
            opening,
        )
        assert stated_margin is not None
        rounded_margin = Decimal(stated_margin.group(1))
        last_place = Decimal(1).scaleb(int(rounded_margin.as_tuple().exponent))
        assert abs(Fraction(rounded_margin) - margin) <= Fraction(last_place) / 2
        assert f"The earlier exact ceiling, ${printed}$ from" not in opening
        assert (
            f"the reported upper bound it replaces, ${printed}$ from {source}, {relation}"
        ) in opening
        assert f"The house it replaces, ${verified}$ from" in _flat(adopt.section(move))
        note = adopt.history_note(move)["claim"]
        assert note.startswith(
            f"Earlier house {verified} from {result} (reported as {printed} from"
        )
        written = adopt.replayed_text(move)
        fence, front, body = adopt._split(written)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
        normalized = (
            fence
            + adopt._replace(front, "priority_notes", _front(written)["priority_notes"])  # pyright: ignore[reportPrivateUsage]
            + body
        )
        assert _front(normalized) == _front(written)
        assert _flat(_body(normalized)) == _flat(_body(written))
        # Corrupt only the current writer-owned spans; n308's hand-marked historical
        # certificate must retain its original exact side and is not this refresh's input.
        stale_notes = _front(normalized)["priority_notes"]
        stale_notes[-1]["claim"] = stale_notes[-1]["claim"].replace(
            str(verified), str(bound["value"])
        )
        stale = fence + adopt._replace(front, "priority_notes", stale_notes) + body  # pyright: ignore[reportPrivateUsage]
        for start, end in (
            (f"\n**House adoption, {adopt.day_words(move.n)}.**", "\n\n"),
            (f"\n## {adopt._title(move)}\n", adopt.FOOTER),  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
        ):
            a, b = adopt._span(stale, start, end)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
            stale = (
                stale[:a] + stale[a:b].replace(str(verified), str(bound["value"])) + stale[b:]
            )
        assert adopt.refreshed(move, stale) == normalized
    # Numeric agreement keeps the shared print; the margin still uses exact sides.
    for move in replayed:
        reported_number = Decimal(str(move.packing["reported_upper_bound"]["value"]))
        verified_number = Decimal(str(move.packing["verified_upper_bound"]["value"]))
        if reported_number == verified_number:
            assert not adopt._lanes_differ(move.packing), move.n  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
        else:
            assert move.n in differing


def test_the_coverage_of_a_count_adopted_again_names_the_new_house_throughout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, replayed: list[adopt.Move]
) -> None:
    """Every row at the count is re-pointed, every reason that names the house names it,
    and the house it displaced is a row of its own, dated from its adoption."""
    from devtools import check_source_coverage  # noqa: PLC0415

    _first, _written, again = _readopted(tmp_path, monkeypatch, replayed)
    text = adopt.COVERAGE.read_text(encoding="utf-8")
    held = {int(e["n"]): e for e in safe_load(text)["selected_overrides"]}[84]
    data = safe_load(adopt.coverage([again], text))
    (override,) = [entry for entry in data["selected_overrides"] if entry["n"] == 84]
    assert override["source_id"] == "new"
    assert override["reason"].endswith(f"adopted on {LATER_DAY} (T-900).")
    rows = [row for row in data["superseded_reports"] if row["n"] == 84]
    assert {row["superseded_by"] for row in rows} == {"new"}
    (displaced,) = [row for row in rows if row["source_id"] == held["source_id"]]
    assert displaced["value"] == held["value"]
    assert displaced["reason"] == (
        f"The house from 2026-10-17 until {LATER_DAY}; its certificate stays "
        "retained and verified, and T-900's exact side is smaller."
    )
    assert all("T-130's exact side" not in str(row.get("reason")) for row in rows)
    results = [
        *select.load_results(),
        {"id": "T-900", "attribution": {"source_keys": ["[new]"]}},
    ]
    assert check_source_coverage.house_reason_errors(data, results) == []


def test_a_conjecture_stands_unless_the_house_is_below_every_number_its_print_may_be(
    selections: dict[int, select.Selection],
) -> None:
    """A house below the catalogue's conjectured optimum, wherever its print rounds,
    withdraws it; any other house leaves it standing, and the adoption goes ahead either
    way: nothing here is decided by hand (result-import.md, "The House Rule")."""
    # The first pass withdrew the catalogue's conjecture at 232, so the record its later
    # pass read (12 October, T-158) has none; the move is planned from the record the
    # first pass read, under the rule that pass ran under.
    first = adopt.read_pass(houses.ADOPTED_ON)[232]
    cases = {n: selection.case for n, selection in selections.items()}
    cases[232] = select.parse_case(232, first)
    selected = select.select(cases=cases, recorded={232: houses.ADOPTED_ON})
    planned = adopt.plan(selected, texts={232: first})
    move = next(move for move in planned if move.n == 232)
    conjecture = adopt.conjectured(move.packing)
    assert conjecture is not None
    assert conjecture == Fraction(Decimal("15.77817459305202")) > move.side
    assert "  conjectured_optimum: null\n" in adopt.rewrite(move)
    unit = Fraction(1, 10**14)
    for side, stands in (
        (conjecture, True),
        (conjecture + unit, True),
        (conjecture - unit / 2, True),
        # At the print less a unit, the house is below every number the print may be
        # (review B6 of #660).
        (conjecture - unit, False),
        (conjecture - 2 * unit, False),
    ):
        assert adopt.conjecture_stands(move.packing, side) is stands, side
        moved = dataclasses.replace(move, house=dataclasses.replace(move.house, side=side))
        withdrawn = "  conjectured_optimum: null\n" in adopt.rewrite(moved)
        assert withdrawn is not stands
    assert adopt.conjecture_stands({"conjectured_optimum": None}, Fraction(1))
    grid = {"conjectured_optimum": "integer", "reported_upper_bound": {"value": "18"}}
    assert adopt.conjectured(grid) == 18
    assert adopt.conjecture_stands(grid, Fraction(18))
    assert not adopt.conjecture_stands(grid, Fraction(18) - Fraction(1, 10**30))
    assert adopt.conjectured({"conjectured_optimum": None}) is None


# ------------------------------------------------------------------- the coverage register


def _claims(directory: Path, name: str, sides: dict[int, str]) -> str:
    path = directory / f"{name}.json"
    rows = [{"n": n, "offered_side": side} for n, side in sides.items()]
    path.write_text(json.dumps({"results": rows}), encoding="utf-8")
    return path.as_posix()


def _register(directory: Path) -> str:
    """A coverage register at n = 7 before T-900 moves its house to 13/4."""
    claims = {
        "old": {7: "3.5"},
        "printed": {7: "3.3", 8: "9"},
        "below": {7: "3.2"},
        "equal": {7: "3.2500001"},
        "above": {7: "3.5000001"},
    }
    sources: list[dict[str, Any]] = [{"id": "new", "source_key": "[new]"}]
    sources += [
        {
            "id": name,
            "source_key": f"[{name}]",
            "claims_record": _claims(directory, name, sides),
        }
        for name, sides in claims.items()
    ]
    data = {
        "sources": sources,
        "selected_overrides": [
            {"n": 7, "source_id": "old", "value": "3.5", "evidence": "E-old", "reason": "Old."}
        ],
        "superseded_reports": [
            {
                "n": 7,
                "source_id": "older",
                "value": "3.75",
                "reason": (
                    "The house until 2026-10-01; its certificate stays retained and verified, "
                    "and T-800's exact side is smaller."
                ),
                "superseded_by": "old",
            },
            {
                "n": 7,
                "source_id": "grid",
                "value": "4",
                "reason": "Grid.",
                "superseded_by": "old",
            },
        ],
        "beyond_horizon_claims": [],
    }
    return yaml.safe_dump(data, sort_keys=False, width=adopt.WIDTH)


def _move(n: int = 7, side: Fraction = Fraction(13, 4)) -> adopt.Move:
    house = select.Candidate(
        result="T-900",
        n=n,
        side=side,
        source_key="[new]",
        published="2026-10-10",
        report_evidence=("E-new",),
        confirming_evidence=("E-new-replay",),
        regularizes=None,
    )
    earlier = Fraction(7, 2)
    case = select.Case(n=n, verified=earlier, reported=earlier, source_key="[old]", evidence=())
    selection = select.Selection(n=n, case=case, house=house, candidates=(house,))
    return adopt.Move(selection, house, {}, "")


def test_coverage_selects_the_new_house_and_points_every_row_at_it(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    text = _register(tmp_path)
    monkeypatch.setattr(adopt, "COVERAGE", tmp_path / "source-coverage.yaml")
    adopt.COVERAGE.write_text(text, encoding="utf-8")
    monkeypatch.setitem(select.reports.HOUSES, "[equal]", lambda _n: Fraction(13, 4))
    monkeypatch.setitem(select.reports.HOUSES, "[above]", lambda _n: Fraction(7, 2))
    # The writer dates each count by the pass that adopted it (`houses.adopted_on`), which
    # reads the adoption's table; the synthetic count is adopted by the first pass.
    monkeypatch.setitem(houses.ADOPTED, 7, "T-900")
    once = adopt.coverage([_move()], text)
    data = safe_load(once)
    (override,) = data["selected_overrides"]
    assert override["source_id"] == "new"
    assert override["value"] == "3.2500000000000000"
    assert override["evidence"] == "E-new"
    assert "adopted on 2026-10-11 (T-900)" in override["reason"]
    rows = {row["source_id"]: row for row in data["superseded_reports"]}
    assert {row["superseded_by"] for row in rows.values()} == {"new"}
    # A row an earlier adoption wrote for the house it displaced now names this house, and
    # keeps its own day; another row keeps its reason.
    assert rows["older"]["reason"] == (
        "The house until 2026-10-01; its certificate stays retained and verified, and "
        "T-900's exact side is smaller."
    )
    assert rows["grid"]["reason"] == "Grid."
    assert rows["old"]["value"] == "3.5"
    assert rows["old"]["reason"].startswith("The house until 2026-10-11;")
    assert rows["old"]["reason"].endswith("and T-900's exact side is smaller.")
    # The release's other claims at the count: compared exactly where a reader rebuilds
    # them, by the print otherwise, and a print below the house is left for
    # `check_source_coverage` to refuse.
    assert "the side it prints is above the house" in rows["printed"]["reason"]
    assert "its exact side equals the house" in rows["equal"]["reason"]
    assert "T-900's registered certificate holds" in rows["equal"]["reason"]
    assert "its exact side is above the house" in rows["above"]["reason"]
    assert "below" not in rows
    assert [row["n"] for row in data["superseded_reports"]] == [7] * 6
    assert adopt.coverage([_move()], once) == once


def test_deferrals_drop_exactly_the_entries_a_case_record_cites() -> None:
    head = "# Deferred adoptions, each with its reason.\n"
    text = (
        head + "deferrals:\n"
        "  - evidence: E-a\n    results: [T-1]\n    bead: think-a\n"
        "  - evidence: E-b\n    results: [T-2]\n    bead: think-b\n"
    )
    assert adopt.deferrals(text, set()) == text
    kept = adopt.deferrals(text, {"E-a", "E-unrelated"})
    assert kept.startswith(head + "deferrals:\n  - evidence: E-b\n")
    assert safe_load(kept)["deferrals"] == [
        {"evidence": "E-b", "results": ["T-2"], "bead": "think-b"}
    ]
    assert adopt.deferrals(text, {"E-a", "E-b"}) == head + "deferrals: []\n"


# ------------------------------------------------------------------- an interrupted write


def _unadopted(text: str, counts: set[int]) -> str:
    """The coverage register with the adoption's selection at `counts` taken back."""
    data = safe_load(text)
    rows = data["superseded_reports"]
    for n in counts:
        displaced = next(
            row for row in rows if row["n"] == n and row["reason"].startswith("The house until")
        )
        rows.remove(displaced)
        override = next(row for row in data["selected_overrides"] if row["n"] == n)
        override.update(source_id=displaced["source_id"], value=displaced["value"])
    for key in ("selected_overrides", "superseded_reports"):
        start, end = adopt._section_span(text, key)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
        dumped = yaml.safe_dump({key: data[key]}, sort_keys=False, width=adopt.WIDTH)
        text = text[:start] + dumped + text[end:]
    return text


def test_an_interrupted_write_is_finished_by_running_it_again(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    selections: dict[int, select.Selection],
    prior: dict[int, str],
) -> None:
    """A write stopped before its last record leaves what a rerun finishes, to the byte.

    The two counts are ones no staged adoption moves: 154, first adopted on 12 October
    2026, and 241, first adopted on 15 October.
    """
    moved = {154, 241}
    frontier = tmp_path / "frontier"
    frontier.mkdir()
    staged = {
        frontier / f"n-{n:03d}.md": prior[n]
        if n in moved
        else select.case_path(n).read_text(encoding="utf-8")
        for n in selections
    }
    staged[tmp_path / "source-coverage.yaml"] = _unadopted(
        adopt.COVERAGE.read_text(encoding="utf-8"), moved
    )
    staged[tmp_path / "deferrals.yaml"] = adopt.DEFERRALS.read_text(encoding="utf-8")
    monkeypatch.setattr(select, "FRONTIER", frontier)
    monkeypatch.setattr(adopt, "FRONTIER", frontier)
    monkeypatch.setattr(adopt, "COVERAGE", tmp_path / "source-coverage.yaml")
    monkeypatch.setattr(adopt, "DEFERRALS", tmp_path / "deferrals.yaml")
    retained: dict[int, str] = {}
    monkeypatch.setattr(adopt, "retain_history", lambda _day, texts: retained.update(texts))

    def stage() -> None:
        for path, text in staged.items():
            path.write_text(text, encoding="utf-8")

    def written() -> dict[Path, str]:
        return {path: path.read_text(encoding="utf-8") for path in staged}

    stage()
    moves = adopt.plan()
    assert [move.n for move in moves] == sorted(moved)
    assert adopt.write(moves) == sorted(moved)
    whole = written()
    assert retained == {n: prior[n] for n in moved}

    stage()
    real = adopt._write  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    calls: list[Path] = []

    def interrupted(path: Path, text: str) -> bool:
        calls.append(path)
        if len(calls) == 4:  # the coverage register, the deferrals, n = 154, then n = 241
            raise OSError("interrupted")
        return real(path, text)

    monkeypatch.setattr(adopt, "_write", interrupted)
    with pytest.raises(OSError, match="interrupted"):
        adopt.write(moves)
    monkeypatch.setattr(adopt, "_write", real)
    rest = adopt.plan()
    assert [move.n for move in rest] == [241]
    assert adopt.write(rest) == [241]
    assert written() == whole


def test_a_redraft_keeps_the_house_and_takes_the_drafted_lower_lanes() -> None:
    """The generator's redraft of an adopted case changes only what the draft owns."""
    record = select.case_path(70).read_text(encoding="utf-8")
    assert adopt.holds(70, record)
    assert adopt.adopt_case(70, record, record) == record
    lower = {"value": "1", "exact_form": "1", "evidence": ["E-area-lower"]}
    drafted = adopt.with_lane(record, "verified_lower_bound", lower)
    redrafted = adopt.adopt_case(70, record, drafted)
    packing = safe_load(redrafted.split("---\n", 2)[1])["packing"]
    assert packing["verified_lower_bound"] == lower
    assert redrafted == drafted
    # A record whose upper lane left the house is refused, and one at another source is
    # the draft's entirely.
    forged = adopt.with_lane(
        record,
        "verified_upper_bound",
        {"value": "9", "exact_form": "9", "evidence": ["E-basic-grid-upper"]},
    )
    with pytest.raises(adopt.AdoptionError, match="exact side"):
        adopt.adopt_case(70, forged, record)
    earlier = adopt.read_history()[70]
    assert not adopt.holds(70, earlier)
    assert adopt.adopt_case(70, earlier, record) == record


def _rehoused(tmp_path: Path) -> tuple[Path, int, int, int]:
    """The layer's index with one axis-tool record given an earlier lapse: a count a strong
    view draws, one whose strong view lapsed with an earlier house, and one only the axis
    tool has drawn."""
    document = json.loads(defaults.INDEX.read_text(encoding="utf-8"))
    entries = {int(entry["n"]): entry for entry in document["entries"]}
    strong = min(
        n for n, entry in entries.items() if entry["generator"] in defaults.STRONG_GENERATORS
    )
    lapsed, plain = sorted(
        n
        for n, entry in entries.items()
        if entry["generator"] not in defaults.STRONG_GENERATORS and defaults.LAPSED not in entry
    )[:2]
    entries[lapsed][defaults.LAPSED] = {
        "generator": "regularize_grid_slack/1",
        "run": "a-run",
        "witness_sha256": "0" * 64,
    }
    index = tmp_path / "index.json"
    index.write_text(json.dumps(document), encoding="utf-8")
    return index, strong, lapsed, plain


def test_an_adoption_names_what_each_re_housed_count_owes_the_regularized_layer(
    tmp_path: Path,
) -> None:
    """A new house is a new witness, and the count's regularized view lapses with it. The
    adoptions of #553, #598 and #614 refreshed only the axis tool's views and left twenty
    counts without a strong generator's decision, n = 176 drawn raw (think-sfas). So a
    write names every count it re-houses, one count a line for those a lapsing view or the
    allowlist makes pending for certain (review B6 of #641), the settled decision the new
    witness bears on, and the commands of the guide's "When a Witness Changes" with their
    cost, which ranges from the certain counts to all of them (review A3 of #641), and
    what the adoption's pull request owes: each count's drawing before and after (reviews
    A1 and A2 of #641; think-g3q7) and its runs, which the house rule never defers."""
    index, strong, lapsed, plain = _rehoused(tmp_path)
    regular = next(
        n
        for n, entry in sorted(defaults.index_entries(index).items())
        if n not in (strong, lapsed, plain)
        and entry["generator"] not in defaults.STRONG_GENERATORS
        and defaults.LAPSED not in entry
    )
    counts = sorted([strong, lapsed, plain, regular])
    spaced = " ".join(map(str, counts))
    why = {
        strong: f"its {defaults.index_entries(index)[strong]['generator']} view lapses",
        lapsed: "a regularize_grid_slack/1 view lapsed earlier",
        plain: (
            "PENDING_ALLOWED holds it for think-aaaa's runs, whatever the new house reads: "
            "they run here, on the new witness, and the entry comes off"
        ),
    }
    lines = adopt.regularization_owed(
        counts,
        index=index,
        allowed={plain: "think-aaaa: a test"},
        settled={lapsed: None},
        day="2026-10-16",
    )
    certain = [f"    {n}: {why[n]}" for n in counts if n in why]
    assert lines[: 2 + len(certain) + 2] == [
        f"regularization owed: 4 re-housed counts, {spaced} ({adopt.WITNESS_CHANGES})",
        "  pending until the strong generators decide the new witness:",
        *certain,
        (
            "  pending unless the new house drawing has no uneven and no near-axis square: "
            f"{regular}"
        ),
        (
            f"  n={lapsed}: SETTLED was decided on the earlier witness; decide the new one and "
            "settle it again, or take it off"
        ),
    ]
    low, high = adopt.REGULARIZE_CPU_MINUTES
    (cost,) = [line for line in lines if line.startswith("  cost: ")]
    assert cost.startswith(
        f"  cost: {low} to {high} CPU-minutes a count for both strong generators and the "
        f"selection, {3 * low} to {3 * high} for the 3 certain to be pending, up to "
        f"{4 * low} to {4 * high} for all 4; one validation item under the pass's compute cap"
    )
    assert "    RUNS=/tmp/regularize WORKERS=2" in lines
    commands = [
        line.strip().removeprefix("python -m devtools.")
        for line in lines
        if line.startswith("    python -m ")
    ]
    label = f"adopt-2026-10-16-n{counts[0]}-{counts[-1]}"
    grid = f"regularize_grid_slack --n {spaced} --run-dir $RUNS/{label}-grid"
    assert commands[:7] == [
        "build_known_best_atlas --update",
        f"regularize_axis_components --update-atlas --n {spaced}",
        "default_drawings --update",
        f"{grid}-0.5",
        f"{grid}-1 --near-axis-degrees 1",
        f"{grid}-5 --near-axis-degrees 5",
        f"regularize_evand run --run-dir $RUNS/{label}-evand --n {spaced} --workers $WORKERS",
    ]
    assert commands[7].startswith(
        f"regularize_select --evand-run $RUNS/{label}-evand --grid-run"
    )
    assert len(commands) == 8
    # The pull request shows each count's drawings before and after (reviews A1 and A2 of
    # #641), and owes every count's runs: none is deferred, and an adoption whose runs do
    # not fit under the compute cap stages the counts they do not cover (the house rule).
    assert "then the guide's step 5 (render and record)" in lines[-3]
    listing, owed = lines[-2:]
    assert listing.startswith("  List each re-housed count's drawing before and after")
    assert "`default_drawings --compare` with the base branch's record" in listing
    assert adopt.BASE_RECORD in listing
    assert listing.endswith(f": {defaults.RUNS_OWED}.")
    assert owed.startswith(f"  A re-housed count is {adopt.NEVER_DEFERRED}: ")
    assert "select_houses.PENDING_ADOPTION with the open bead that adopts them" in owed
    assert "--check-state` fails until the runs decide every re-housed count" in owed
    assert "while the list defers the runs of a witness whose house has moved since" in owed
    assert not [line for line in lines if "add each pending count" in line]
    # Nothing re-housed, nothing owed: a second run of the idempotent write prints nothing.
    assert adopt.regularization_owed([], index=index) == []


def _printed_runs(lines: list[str]) -> list[tuple[str, str]]:
    """Each strong run the printout starts, as (generator prefix of its id, directory)."""
    found = []
    for line in lines:
        words = line.split()
        if "--run-dir" not in words:
            continue
        directory = Path(words[words.index("--run-dir") + 1]).name
        prefix = (
            "grid-slack" if "devtools.regularize_grid_slack" in words else "evand-regularize"
        )
        found.append((prefix, directory))
    return found


def test_the_printed_runs_take_ids_no_run_in_the_index_has(tmp_path: Path) -> None:
    """Review B2 of #641: the layer records a run by its directory's name, and admitting a
    run whose id the index holds replaces that run's block, so every adoption that ran in
    `$RUNS/evand` would overwrite the last one's cost and decisions. The printed
    directories are named for the adoption's day, and move on where a run took the name."""
    lines = adopt.regularization_owed([176], day="2026-10-16")
    taken = {
        str(run["id"]) for run in json.loads(defaults.INDEX.read_text(encoding="utf-8"))["runs"]
    }
    ids = [f"{prefix}-{directory}" for prefix, directory in _printed_runs(lines)]
    assert ids == list(adopt.run_ids("adopt-2026-10-16-n176").values())
    assert len(set(ids)) == 4
    assert not taken & set(ids)

    document = json.loads(defaults.INDEX.read_text(encoding="utf-8"))
    document["runs"].append({"id": "grid-slack-adopt-2026-10-16-n176-grid-1"})
    index = tmp_path / "index.json"
    index.write_text(json.dumps(document), encoding="utf-8")
    assert adopt.run_label("2026-10-16", [176], index) == "adopt-2026-10-16-n176-b"
    moved = adopt.regularization_owed([176], index=index, day="2026-10-16")
    assert [directory for _prefix, directory in _printed_runs(moved)] == [
        "adopt-2026-10-16-n176-b-grid-0.5",
        "adopt-2026-10-16-n176-b-grid-1",
        "adopt-2026-10-16-n176-b-grid-5",
        "adopt-2026-10-16-n176-b-evand",
    ]


def test_two_adoptions_of_one_day_print_different_runs() -> None:
    """Review C3 of #641: the index holds only the runs merged into the branch, so two
    adoptions opened from one base on one day both read it bare, and a label of the day
    alone gave both the same ids; the second to admit its run would replace the first's
    block. The label names the re-housed counts, lowest and highest, so adoptions of other
    counts print other ids; two that re-house one count conflict on its case record."""
    first = adopt.regularization_owed([176], day="2026-10-16")
    second = adopt.regularization_owed([105, 129, 304], day="2026-10-16")
    ids = {
        tuple(f"{prefix}-{directory}" for prefix, directory in _printed_runs(lines))
        for lines in (first, second)
    }
    assert ids == {
        tuple(adopt.run_ids("adopt-2026-10-16-n176").values()),
        tuple(adopt.run_ids("adopt-2026-10-16-n105-304").values()),
    }
    with pytest.raises(ValueError, match="names the counts it re-houses"):
        adopt.run_label("2026-10-16", [])


def test_the_runbook_guide_and_printout_owe_every_re_housed_counts_runs_alike() -> None:
    """Review C4 of #641: the runbook's deferral waited "for the owner's word or for its
    runs", the guide's and the printout's only for the owner's word, and neither document
    said how to give `--compare` the base branch's record. Review D1: all three, and the
    comparison's own summary, name a lost strong view in one wording. Review D2: the
    documents name the pull request's base, which is not main for a stacked adoption, and
    the printout gives main as the example and says so. Review E1 and the house rule (16
    October 2026): the owner's rule is to adopt the smallest packing and then regularize
    it, so no adoption waits for the owner's word. Review F1: the runbook and the guide
    still deferred each pending count while the mark said a lost view's runs were not
    deferred. All three now owe every re-housed count's runs in the adoption's pull
    request, never deferred, and the documents quote the mark that says so."""
    lines = adopt.regularization_owed([176], day="2026-10-16")
    (listing,) = [line for line in lines if "drawing before and after" in line]
    command = f"--compare <(git show origin/$BASE:{defaults.RECORD_PATH})"
    assert adopt.BASE_RECORD.strip("`") == command.removeprefix("--compare ").replace(
        "$BASE", "main"
    )
    for path in (adopt.WITNESS_CHANGES, adopt.INTAKE_STEP):
        text = (houses.REPO / path.split(", ", 1)[0]).read_text(encoding="utf-8")
        words = " ".join(text.replace("\u2019", "'").split())
        assert command in words, path
        assert "`BASE` being `main` unless the pull request is stacked" in words, path
        assert defaults.STRONG_VIEW_LOST in words.lower(), path
        assert f"\u201c{defaults.RUNS_OWED}\u201d" in words, path
        assert adopt.NEVER_DEFERRED in words.replace("`", ""), path
        assert "the adoption waits for the owner's word or for its runs" not in words, path
        assert "unless the owner holds it" not in words, path
        assert "irregular house drawing" not in words, path
        assert "its runs are not deferred" not in words, path
        assert "adds each pending count to" not in words, path
    assert f"{adopt.BASE_RECORD}, {adopt.STACKED_BASE})" in listing
    assert f"where {defaults.STRONG_VIEW_LOST}, it names those goals" in listing
    assert listing.endswith(f": {defaults.RUNS_OWED}.")
    assert any(adopt.NEVER_DEFERRED in line for line in lines)
    # Review A14 of #660: the policy's gates section and the sweep's step point to the
    # house rule rather than restate it, so they cannot drift from it.
    policy = (houses.REPO / "docs/project/policies/regularization-policy.md").read_text(
        encoding="utf-8"
    )
    gates = " ".join(policy.partition("## 8. Gates")[2].partition("\n## ")[0].split())
    assert "result-import.md#the-house-rule" in gates
    assert "defers the count with its bead" not in gates
    # Review C6 of #660: each instruction for deferring a corrected witness names
    # `CORRECTED`, which `--check-state` holds every entry to.
    runbook = _flat((houses.REPO / "packing/campaign/result-import.md").read_text("utf-8"))
    step, prompt = runbook.split("3. **Import**", 1)[1], runbook.split("```text", 1)[1]
    for text in (step.split("4. **Validate**")[0], prompt.split("5. From packing/")[0]):
        assert "CORRECTED" in text
    # The sweep's step is held in test_intake_sweep.


def test_every_printed_command_parses_with_its_tools_own_parser(tmp_path: Path) -> None:
    """Review B5 of #641: each printed command, with the shell variables its first line
    sets, is one its tool's own `parser()` accepts, so a renamed flag fails here rather
    than in the next adoption's shell. As first printed, `--workers K` was refused (B3)."""
    import importlib  # noqa: PLC0415
    import shlex  # noqa: PLC0415

    lines = adopt.regularization_owed([18, 176], day="2026-10-16")
    (shell,) = [line.split() for line in lines if line.startswith("    RUNS=")]
    values = dict(word.split("=", 1) for word in shell)
    assert set(values) == {"RUNS", "WORKERS"}
    values["RUNS"] = str(tmp_path)
    commands = [line.strip() for line in lines if line.startswith("    python -m devtools.")]
    assert len(commands) == 8
    for printed in commands:
        command = printed
        for name, value in values.items():
            command = command.replace(f"${name}", value)
        assert "$" not in command, printed
        _python, _m, module, *arguments = shlex.split(command)
        parsed = importlib.import_module(module).parser().parse_args(arguments)
        assert parsed is not None, printed


@pytest.mark.parametrize("named", [adopt.WITNESS_CHANGES, adopt.INTAKE_STEP])
def test_the_printout_names_headings_that_exist(named: str) -> None:
    """Review A11 of #641: the two places the printout sends a reader are headings of the
    files it names, so renaming one fails here."""
    path, heading = named.split(", ", 1)
    text = (houses.REPO / path).read_text(encoding="utf-8")
    assert re.search(rf"^#+ {re.escape(heading.strip(chr(34)))}$", text, re.MULTILINE), named


def test_a_write_and_a_dry_run_print_what_the_moves_owe(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    move = _move(176)
    monkeypatch.setattr(adopt, "plan", lambda: [move])
    monkeypatch.setattr(adopt, "adopted", lambda _move: False)
    monkeypatch.setattr(adopt, "write", lambda moves: [moved.n for moved in moves])
    owed = adopt.regularization_owed([176])
    # One count is a count, not "1 re-housed counts" (review A8 of #641).
    assert owed[0].startswith("regularization owed: 1 re-housed count, 176 ")
    # Its runs are named for the day 176's house was adopted, not the day this test runs.
    assert f"adopt-{houses.adopted_on(176)}-n176-evand" in "\n".join(owed)
    assert adopt.main([]) == 0
    assert capsys.readouterr().out.splitlines() == ["adopted 1 houses: 176", *owed]
    assert adopt.main(["--dry-run"]) == 0
    assert capsys.readouterr().out.splitlines()[1:] == owed
    # A count already at its house is no move, and owes nothing.
    monkeypatch.setattr(adopt, "adopted", lambda _move: True)
    assert adopt.main(["--dry-run"]) == 0
    assert len(capsys.readouterr().out.splitlines()) == 1
