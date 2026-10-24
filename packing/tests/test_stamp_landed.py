"""The day each register entry reached `main`, its `landed` date (`devtools.stamp_landed`).

The results page's "Added in the Last Seven Days" and its Added filters read `landed`, so
"added" means the day a reader could first see a result, not the day a lane wrote it
(#514's review A, finding A1). Every entry carries it, as the schema requires; a lane
writes it with the entry, and the merge step re-dates a branch's new entries to the merge
day. Nothing here reads Git but the tool's own history modes, which these tests run on a
scratch repository (OR-18; #514's review B, finding B3).
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from devtools import stamp_landed
from sqpack.yamlio import safe_load

REGISTER = """\
results:
  - id: T-001
    kind: lower-bound
    registered: '2026-10-01'
    landed: '2026-10-02'
    headline: one
  - id: T-002
    kind: upper-bound
    registered: '2026-10-03'
    landed: '2026-10-03'
    headline: two
  - id: T-003
    kind: optimality
    proves_kind: lower-bound
    registered: '2026-10-04'
    headline: three
"""


def test_the_merge_step_re_dates_only_the_entries_it_names() -> None:
    """A named entry's `landed` line is rewritten in place, one without a line gains one
    after its `registered:`, an entry not named keeps its date, and every other byte of
    the file is unchanged; stamping again with another day re-dates it again (#514's
    review B, finding B2)."""
    stamped = stamp_landed.set_landed(REGISTER, {"T-002": "2026-10-05", "T-003": "2026-10-05"})
    assert stamped == REGISTER.replace(
        "    registered: '2026-10-03'\n    landed: '2026-10-03'\n",
        "    registered: '2026-10-03'\n    landed: '2026-10-05'\n",
    ).replace(
        "    registered: '2026-10-04'\n",
        "    registered: '2026-10-04'\n    landed: '2026-10-05'\n",
    )
    assert stamp_landed.recorded(stamped) == {
        "T-001": "2026-10-02",
        "T-002": "2026-10-05",
        "T-003": "2026-10-05",
    }
    later = stamp_landed.set_landed(stamped, {"T-002": "2026-10-06", "T-003": "2026-10-06"})
    assert stamp_landed.recorded(later)["T-003"] == "2026-10-06"
    assert later.count("landed:") == stamped.count("landed:") == 3


def test_a_branch_adds_the_entries_main_does_not_hold() -> None:
    """The merge step re-dates the entries the branch adds, the ones `main`'s register
    lacks, and no entry `main` already holds."""
    on_main = REGISTER.split("  - id: T-002", maxsplit=1)[0]
    assert stamp_landed.branch_entries(REGISTER, on_main) == ["T-002", "T-003"]
    assert stamp_landed.branch_entries(REGISTER, REGISTER) == []


def test_the_ids_are_the_parsed_registers_and_a_line_the_scan_misses_fails() -> None:
    """An id is read from the parsed register and a scan of its `- id:` lines must agree,
    so an entry the scan cannot see, here one written as a flow mapping, fails loudly
    instead of going unstamped. A four-digit or quoted id is seen (#514's review B,
    finding B7)."""
    wide = REGISTER.replace("id: T-002", "id: 'T-1002'")
    assert stamp_landed.register_ids(wide) == ["T-001", "T-1002", "T-003"]
    hidden = REGISTER + "  - {id: T-004, registered: '2026-10-05', landed: '2026-10-05'}\n"
    with pytest.raises(ValueError, match="T-004"):
        stamp_landed.register_ids(hidden)


def test_the_check_reads_the_tree_alone() -> None:
    """Every entry must carry `landed`, written as a date and no earlier than its
    registration; no ref is consulted."""
    register = safe_load(REGISTER)
    assert stamp_landed.problems(register) == ["T-003 carries no `landed` date"]
    register["results"][2]["landed"] = "2026-10-04"
    assert stamp_landed.problems(register) == []
    register["results"][0]["landed"] = "2026-09-30"
    register["results"][1]["landed"] = "October"
    assert stamp_landed.problems(register) == [
        "T-001 landed on 2026-09-30 before it was registered on 2026-10-01",
        "T-002: `landed` 'October' is not a date",
    ]


def _git(repo: Path, *args: str, when: str = "") -> None:
    environment = {
        **os.environ,
        "GIT_AUTHOR_NAME": "test",
        "GIT_AUTHOR_EMAIL": "test@example.com",
        "GIT_COMMITTER_NAME": "test",
        "GIT_COMMITTER_EMAIL": "test@example.com",
    }
    if when:
        environment |= {"GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when}
    subprocess.run(["git", *args], cwd=repo, env=environment, check=True, capture_output=True)


def test_history_dates_an_entry_by_the_merge_that_brought_it_to_main(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """On `main`'s first-parent history an entry lands with the first commit whose
    register holds it: one committed on `main` lands that day, one written on a branch
    on 3 October lands with the merge on 5 October, and a commit's UTC day is the one
    that counts, so a merge at 23:30 in New York lands the next day. `audit` lists the
    recorded day that differs, here a lane's registration day the merge step never
    re-dated, with the day history gives."""
    path = "packing/frontier/results.yaml"
    register = tmp_path / path
    register.parent.mkdir(parents=True)

    def entries(*ids: str) -> str:
        return "results:\n" + "".join(f"  - id: {result_id}\n" for result_id in ids)

    _git(tmp_path, "init", "-q", "-b", "main")
    register.write_text(entries("T-001"), encoding="utf-8")
    _git(tmp_path, "add", path)
    _git(tmp_path, "commit", "-q", "-m", "one", when="2026-10-01T12:00:00+00:00")
    _git(tmp_path, "checkout", "-q", "-b", "lane")
    register.write_text(entries("T-001", "T-002"), encoding="utf-8")
    _git(tmp_path, "commit", "-q", "-am", "two", when="2026-10-03T12:00:00+00:00")
    _git(tmp_path, "checkout", "-q", "main")
    _git(tmp_path, "merge", "-q", "--no-ff", "lane", "-m", "merge", when="2026-10-05T09:00:00Z")
    register.write_text(entries("T-001", "T-002", "T-003"), encoding="utf-8")
    _git(tmp_path, "commit", "-q", "-am", "three", when="2026-10-05T23:30:00-04:00")
    monkeypatch.setattr(stamp_landed, "REPO", tmp_path)
    history = stamp_landed.first_landings("main", path)
    assert history == {"T-001": "2026-10-01", "T-002": "2026-10-05", "T-003": "2026-10-06"}
    recorded = {"T-001": "2026-10-01", "T-002": "2026-10-03", "T-003": "2026-10-06"}
    assert stamp_landed.audit(recorded, history, ["T-001", "T-002", "T-003"]) == {
        "T-002": "2026-10-05"
    }


def test_every_entry_carries_the_day_it_landed() -> None:
    """The live register, read from the tree alone: every entry carries `landed`, a date
    no earlier than its registration, and the line scan the tool stamps by sees every
    entry."""
    text = stamp_landed.RESULTS.read_text(encoding="utf-8")
    assert stamp_landed.problems(safe_load(text)) == []
    assert all(day for day in stamp_landed.recorded(text).values())


# The landing record: house best packings and row sources (#736's review A, finding A2).

HOUSES = """\
from __future__ import annotations

from devtools import kernel

ADOPTED_ON = "2026-10-11"
ADOPTED: dict[int, str] = {
    29: "T-195",
    105: "T-229",
}
"""


def test_the_adopted_houses_are_read_without_running_the_module() -> None:
    assert stamp_landed.adopted_houses(HOUSES) == {29: "T-195", 105: "T-229"}
    with pytest.raises(ValueError, match="ADOPTED"):
        stamp_landed.adopted_houses("ADOPTED_ON = '2026-10-11'\n")


def test_the_landing_record_round_trips_and_names_what_it_lacks() -> None:
    """The record is written in one form, so the same record is the same bytes; it must
    hold one house per adopted count, under the result that houses it now, and one day
    per row source, and nothing else."""
    landings = stamp_landed.Landings(
        {29: ("T-195", "2026-10-19"), 105: ("T-229", "2026-10-23")},
        {"src-b": "2026-10-22", "src-a": "2026-10-16"},
    )
    text = stamp_landed.write_landings(landings)
    assert text.startswith(stamp_landed.LANDINGS_HEADER)
    assert stamp_landed.read_landings(text) == landings
    assert text.index("id: src-a") < text.index("id: src-b")
    adopted = {29: "T-195", 105: "T-229"}
    assert stamp_landed.landings_problems(landings, adopted, {"src-a", "src-b"}) == []
    assert stamp_landed.landings_problems(
        landings, {29: "T-195", 105: "T-174", 204: "T-225"}, {"src-a", "src-c"}
    ) == [
        "n=105: the landing names T-229, the house is T-174",
        "n=204: its house, T-225, has no landing",
        "src-b: a landing for a source with no rows",
        "src-c: its rows have no landing",
    ]


def test_the_merge_step_dates_what_a_branch_adds_and_keeps_what_main_holds() -> None:
    """A count whose house the branch changes, a new count and a new row source take the
    merge day, whatever a lane wrote; the rest keep `main`'s day. Without a day, an
    entry nothing dates is left out for the problems to name."""
    on_main = stamp_landed.Landings(
        {29: ("T-195", "2026-10-19"), 105: ("T-174", "2026-10-19")}, {"src-a": "2026-10-16"}
    )
    adopted = {29: "T-195", 105: "T-229", 204: "T-225"}
    stamped = stamp_landed.stamp_landings(adopted, {"src-a", "src-b"}, (on_main,), "2026-10-24")
    assert stamped == stamp_landed.Landings(
        {
            29: ("T-195", "2026-10-19"),
            105: ("T-229", "2026-10-24"),
            204: ("T-225", "2026-10-24"),
        },
        {"src-a": "2026-10-16", "src-b": "2026-10-24"},
    )
    lanes = stamp_landed.stamp_landings(adopted, {"src-a", "src-b"}, (on_main,), None)
    assert lanes.houses == {29: ("T-195", "2026-10-19")}
    assert lanes.sources == {"src-a": "2026-10-16"}


def test_history_dates_a_house_and_a_source_s_rows_by_the_merge_that_brought_them(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """On `main`'s first-parent history a count's house lands with the merge that moved
    it to the result that holds it now, not the day its pass ran on a branch, as the pass
    of 17 October 2026 reached `main` on the 19th; a source's rows land with the first
    merge that holds any of them, as #631's rows did with #631's results. A house moved
    back and forth is dated by its last move. `landings_audit` lists a recorded day that
    differs from history."""
    houses = tmp_path / stamp_landed.HOUSES_PATH
    coverage = tmp_path / stamp_landed.COVERAGE_PATH
    houses.parent.mkdir(parents=True)
    coverage.parent.mkdir(parents=True)

    def write(adopted: dict[int, str], sources: list[str]) -> None:
        houses.write_text(f"ADOPTED = {adopted!r}\n", encoding="utf-8")
        rows = "".join(f"  - n: 400\n    source_id: {source}\n" for source in sources)
        coverage.write_text(f"beyond_horizon_claims:\n{rows}", encoding="utf-8")

    _git(tmp_path, "init", "-q", "-b", "main")
    write({29: "T-155"}, ["src-a"])
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-q", "-m", "one", when="2026-10-15T12:00:00+00:00")
    _git(tmp_path, "checkout", "-q", "-b", "pass")
    write({29: "T-195", 68: "T-174"}, ["src-a", "src-b"])
    _git(tmp_path, "commit", "-q", "-am", "pass", when="2026-10-17T12:00:00+00:00")
    _git(tmp_path, "checkout", "-q", "main")
    _git(tmp_path, "merge", "-q", "--no-ff", "pass", "-m", "merge", when="2026-10-19T06:22:00Z")
    write({29: "T-155", 68: "T-174"}, ["src-a", "src-b"])
    _git(tmp_path, "commit", "-q", "-am", "back", when="2026-10-20T12:00:00+00:00")
    write({29: "T-195", 68: "T-174"}, ["src-a", "src-b"])
    _git(tmp_path, "commit", "-q", "-am", "again", when="2026-10-21T12:00:00+00:00")
    monkeypatch.setattr(stamp_landed, "REPO", tmp_path)
    history = stamp_landed.landing_history("main")
    assert history == stamp_landed.Landings(
        {29: ("T-195", "2026-10-21"), 68: ("T-174", "2026-10-19")},
        {"src-a": "2026-10-15", "src-b": "2026-10-19"},
    )
    recorded = stamp_landed.Landings(
        {29: ("T-195", "2026-10-21"), 68: ("T-174", "2026-10-17")},
        {"src-a": "2026-10-15", "src-b": "2026-10-19"},
    )
    assert stamp_landed.landings_audit(recorded, history, recorded) == [
        "n=68 (T-174) records 2026-10-17; history gives 2026-10-19"
    ]
    # The merge step dates only what a branch adds to `main`'s tree: here a new house at
    # 204 and a new source. Where `main` holds no record yet, the rest keep the branch's
    # days, so introducing the record re-dates nothing.
    adopted = {29: "T-195", 68: "T-174", 204: "T-225"}
    sources = {"src-a", "src-b", "src-c"}
    additions = stamp_landed.branch_additions(adopted, sources, "2026-10-24", "main")
    assert additions == stamp_landed.Landings(
        {204: ("T-225", "2026-10-24")}, {"src-c": "2026-10-24"}
    )
    stamped = stamp_landed.stamp_landings(
        adopted, sources, (additions, stamp_landed.Landings({}, {}), history), None
    )
    assert stamped == stamp_landed.Landings(
        {**history.houses, 204: ("T-225", "2026-10-24")},
        {**history.sources, "src-c": "2026-10-24"},
    )


def test_every_house_and_row_source_carries_the_day_it_landed() -> None:
    """The live landing record, read from the tree alone: one house per adopted count
    under the result that houses it now, and one day per source with rows."""
    landings = stamp_landed.read_landings(stamp_landed.LANDINGS.read_text(encoding="utf-8"))
    adopted, sources = stamp_landed.current_landings()
    problems = stamp_landed.landings_problems(landings, adopted, sources)
    assert not problems, (
        "the landing record lags the tree; run `python -m devtools.stamp_landed --apply` "
        "from packing/ after merging main, and again at the merge step (result-import.md, "
        f"stages 3 and 5): {problems}"
    )
    assert stamp_landed.LANDINGS.read_text(encoding="utf-8") == stamp_landed.write_landings(
        landings
    )
