# ruff: noqa: RUF001 -- these tests read case prose, whose typography uses curly apostrophes.
"""The house adoption of 11 October 2026 and its later passes: derivation, drawing custody,
the case records, the coverage register and each pass's prior state."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import re
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
import yaml

from devtools import adopt_houses as adopt
from devtools import select_houses as select
from devtools import upper_bound_houses as houses
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
def replayed(
    selections: dict[int, select.Selection], latest: dict[int, str]
) -> list[adopt.Move]:
    """Each count's last pass planned again from the record as that pass read it."""
    cases = {
        n: select.parse_case(n, latest[n]) if n in latest else selection.case
        for n, selection in selections.items()
    }
    return adopt.plan(select.select(cases=cases), texts=latest)


def test_no_confirmed_reviewed_side_is_left_below_its_case(
    selections: dict[int, select.Selection],
) -> None:
    """After the adoption the derivation moves nothing: every case is at its house."""
    assert [n for n, selection in selections.items() if selection.moves] == []


def test_every_adopted_case_holds_the_derived_smallest_side(
    selections: dict[int, select.Selection],
) -> None:
    for n, result in houses.ADOPTED.items():
        best = selections[n].candidates[0]
        assert best.result == result
        assert selections[n].case.verified == best.side == houses.side(n)


def test_regularizations_leave_the_packing_with_its_finder(
    selections: dict[int, select.Selection],
) -> None:
    assert selections[236].candidates[0].regularizes == "T-136"
    assert selections[103].candidates[0].regularizes == "T-138"
    assert selections[70].candidates[0].regularizes == "T-125"
    assert adopt.CREDITS[236].found_by == (adopt.SQUISH,)
    assert adopt.CREDITS[70].found_by == (adopt.XU,)
    assert adopt.CREDITS[103].improved_by == ("Mishapolk", adopt.DANIEL)


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
            "replay_status": "passed",
        }
    }
    return entry, evidence


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


def test_a_candidate_below_an_algebraic_ceilings_display_is_left_to_a_human(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A display rounded up at sixteen places cannot order a side just below it."""
    assert not select.load_case(51).exact  # (16 + 5 sqrt(2)) / 3
    assert select.load_case(70).exact
    entry, evidence = _confirmed_entry()
    display = Fraction(Decimal("7.6903559372884918"))
    algebraic = select.Case(
        n=7, verified=display, reported=display, source_key="", evidence=(), exact=False
    )
    within = display - Fraction(1, 10**17)
    monkeypatch.setitem(select.reports.HOUSES, "[test]", lambda _n: within)
    monkeypatch.setattr(select, "_side", lambda _key, _n: within)
    held = select.select([entry], evidence, cases={7: algebraic})[7]
    assert held.undecided
    assert held.house is None
    rational = dataclasses.replace(algebraic, exact=True)
    assert select.select([entry], evidence, cases={7: rational})[7].moves
    monkeypatch.setattr(select, "_side", lambda _key, _n: display)
    above = select.select([entry], evidence, cases={7: algebraic})[7]
    assert not above.undecided
    assert not above.moves
    assert "undecided" in select.table({7: held}, everything=False)


def test_no_unread_eligible_entry_is_pending_adoption() -> None:
    """An eligible entry with no exact reader is never a candidate, so `--check` reads its
    standing instead: one that states a side below its case would be an adoption the
    selector cannot see."""
    unread: list[str] = []
    select.candidates(select.load_results(), select.load_evidence(), unread=unread)
    assert select.unread_pending(unread) == {}


def test_check_lists_the_unread_and_fails_on_one_pending_adoption(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def selecting(*, since: str | None, unread: list[str]) -> dict[int, select.Selection]:
        assert since is None
        unread.append("T-901")
        return {}

    monkeypatch.setattr(select, "select", selecting)
    monkeypatch.setattr(select, "unread_pending", lambda _unread: {})
    assert select.main(["--check"]) == 0
    assert "unread, eligible but with no exact reader: T-901" in capsys.readouterr().out
    monkeypatch.setattr(select, "unread_pending", lambda unread: {unread[0]: [7]})
    assert select.main(["--check"]) == 1
    assert "T-901 has no exact reader and states a side below its case at n = [7]" in (
        capsys.readouterr().out
    )


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
    assert len(receipt["mutations_refused_and_restored"]) == 2 * len(houses.source_keys())
    assert receipt["fresh_geometric_deciders"] is False


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
            # As the earlier pass left it: at that pass's house, dated that day.
            packing = _front(archives[day][n])
            assert packing["source_reviewed"] == earlier[-1]
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


#: The verifier table, which `render_case_verifiers` writes.
VERIFIER_TABLE = re.compile(
    r"<!-- BEGIN verification code.*?<!-- END verification code -->", re.DOTALL
)
#: Counts whose body the first pass, on 11 October 2026, marked as history by hand, in
#: prose no tool writes in a fixed form (`adopt_houses.historical`): the SQUISH update
#: sections and the grid prose. Their owned parts are still compared.
HAND_MARKED = frozenset({155, 258, 263, 302, 308})


def _body(text: str) -> str:
    """A record's body as the writer is answerable for it: flowmark's wrapping and escapes
    undone and the verifier table left out."""
    return _flat(VERIFIER_TABLE.sub("", text.split("---\n", 2)[2]).replace("\\+", "+"))


def test_the_writer_rebuilds_every_adopted_record_from_its_prior_state(
    replayed: list[adopt.Move],
) -> None:
    """Replaying `rewrite` on each record as its last pass read it gives the committed one.

    What the writer owns is compared: its front-matter keys, its opening paragraph and
    certificate section, and the rest of the body, which it marks as history, with
    whitespace collapsed, since flowmark rewraps it. The verifier table and the rigidity
    scope are refreshed by their own tools. A count adopted twice is replayed from the
    record the earlier pass left (`adopt_houses.before_last_pass`).
    """
    assert [move.n for move in replayed] == sorted(houses.ADOPTED)
    for move in replayed:
        assert move.house.result == houses.ADOPTED[move.n]
        committed = select.case_path(move.n).read_text(encoding="utf-8")
        written = adopt.rewrite(move)
        held, wrote = _front(committed), _front(written)
        for key in OWNED:
            assert held.get(key) == wrote.get(key), f"n={move.n}: packing.{key}"
        body = _flat(committed.split("---\n", 2)[2])
        assert _flat(adopt.opening(move)) in body, f"n={move.n}: opening paragraph"
        assert _flat(adopt.section(move)) in body, f"n={move.n}: certificate section"
        if move.n not in HAND_MARKED:
            assert _body(committed) == _body(written), f"n={move.n}: the body as history"


#: A synthetic later pass, its review and its source: n = 84 adopted again after T-130.
LATER_DAY, REVIEWED, PUBLISHED = "2026-11-03", "2026-11-02", "2025-12-31"


def _readopted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, replayed: list[adopt.Move]
) -> tuple[adopt.Move, str, adopt.Move]:
    """n = 84 as the first pass wrote it, and a move to a synthetic T-900 on a later day.

    T-900 sits a millionth below T-130 with a source of its own in a copy of the coverage
    register; the later day is a pass of its own in `upper_bound_houses.LATER_PASSES`.
    """
    first = next(move for move in replayed if move.n == 84)
    written = adopt.rewrite(first)
    monkeypatch.setitem(houses.LATER_PASSES, LATER_DAY, frozenset({84}))
    house = select.Candidate(
        result="T-900",
        n=84,
        side=first.house.side - Fraction(1, 10**6),
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
    """The second adoption of a count reads as one current house and dated history.

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
    assert body.count("**House adoption, ") == 2
    title = body.index("— open")
    assert body.index("**House adoption, 3 November 2026.**") == title + len("— open ")
    assert (
        "**House adoption, 11 October 2026.** Francisco Couzo’s refinement of Ryan Xu’s "
        "packing (T-130) was this case’s house until 3 November 2026:"
    ) in body
    assert "the verified upper bound until 3 November 2026: confirmed," in body
    assert "[review of 2 November 2026](../../docs/review-t900.md)" in body
    packing = _front(record)
    assert packing["source_reviewed"] == LATER_DAY
    assert packing["reported_upper_bound"]["found_year"] == 2025
    notes = [note["claim"] for note in packing["priority_notes"]]
    assert notes[:-1] == [note["claim"] for note in _front(written)["priority_notes"]]
    assert notes[-2].endswith(
        "the case’s ceiling until 11 October 2026; its certificate and replay remain retained."
    )
    assert notes[-1] == (
        f"Earlier house {before['value']} from {before['source_key']}, the case’s ceiling "
        "from 11 October 2026 until 3 November 2026; its certificate and replay remain "
        "retained."
    )
    path = tmp_path / "n-084.md"
    path.write_text(record, encoding="utf-8")
    assert check_case_prose.check_case_file(path) == []
    assert adopt.adopted(dataclasses.replace(again, packing=packing))
    assert not adopt.adopted(dataclasses.replace(first, packing=packing))


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
        f"The house from 2026-10-11 until {LATER_DAY}; its certificate stays retained and "
        "verified, and T-900's exact side is smaller."
    )
    assert all("T-130's exact side" not in str(row.get("reason")) for row in rows)
    results = [
        *select.load_results(),
        {"id": "T-900", "attribution": {"source_keys": ["[new]"]}},
    ]
    assert check_source_coverage.house_reason_errors(data, results) == []


def test_a_conjecture_the_house_does_not_beat_stops_the_adoption(
    selections: dict[int, select.Selection],
) -> None:
    # The first pass withdrew the catalogue's conjecture at 232, so the record its later
    # pass read (12 October, T-158) has none; the move is planned from the record the
    # first pass read.
    first = adopt.read_pass(houses.ADOPTED_ON)[232]
    cases = {n: selection.case for n, selection in selections.items()}
    cases[232] = select.parse_case(232, first)
    planned = adopt.plan(select.select(cases=cases), texts={232: first})
    move = next(move for move in planned if move.n == 232)
    conjecture = adopt.conjectured(move.packing)
    assert conjecture == Fraction(Decimal("15.77817459305202")) > move.house.side
    assert "  conjectured_optimum: null\n" in adopt.rewrite(move)
    above = dataclasses.replace(move, house=dataclasses.replace(move.house, side=conjecture))
    with pytest.raises(adopt.AdoptionError, match="does not beat the conjectured optimum"):
        adopt.rewrite(above)
    grid = {"conjectured_optimum": "integer", "reported_upper_bound": {"value": "18"}}
    assert adopt.conjectured(grid) == 18
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
    """A write stopped before its last record leaves what a rerun finishes, to the byte."""
    moved = {84, 86}
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
        if len(calls) == 4:  # the coverage register, the deferrals, n = 84, then n = 86
            raise OSError("interrupted")
        return real(path, text)

    monkeypatch.setattr(adopt, "_write", interrupted)
    with pytest.raises(OSError, match="interrupted"):
        adopt.write(moves)
    monkeypatch.setattr(adopt, "_write", real)
    rest = adopt.plan()
    assert [move.n for move in rest] == [86]
    assert adopt.write(rest) == [86]
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
