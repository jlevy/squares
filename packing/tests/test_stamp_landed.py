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
