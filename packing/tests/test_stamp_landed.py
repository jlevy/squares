"""The day each register entry reached `main`, its `landed` date (`devtools.stamp_landed`).

The results page's "Added in the Last Seven Days" and its Added filter read `landed`, so
"added" means the day a reader could first see a result, not the day a lane wrote it
(#514's review A, finding A1). These tests hold the three things that keep it true: the
merge step's stamp, the one-time backfill from `main`'s first-parent history, and the
check that no entry on `main` is left without one.
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
    headline: two
  - id: T-003
    kind: optimality
    proves_kind: lower-bound
    registered: '2026-10-04'
    headline: three
"""


def test_the_stamp_follows_registration_and_touches_nothing_else() -> None:
    """The entries without `landed` are found in order, each stamp goes on the line after
    its `registered:`, an entry already dated keeps its date, and every other byte of the
    file is unchanged; stamping twice changes nothing more."""
    assert stamp_landed.unstamped(REGISTER) == ["T-002", "T-003"]
    stamped = stamp_landed.stamp(REGISTER, {"T-002": "2026-10-05", "T-001": "2026-10-09"})
    assert stamped == REGISTER.replace(
        "    registered: '2026-10-03'\n",
        "    registered: '2026-10-03'\n    landed: '2026-10-05'\n",
    )
    assert stamp_landed.unstamped(stamped) == ["T-003"]
    assert stamp_landed.stamp(stamped, {"T-002": "2026-10-06"}) == stamped


def test_the_check_holds_every_entry_on_main_and_lets_a_new_one_wait() -> None:
    """An entry `main` holds must carry a `landed` date, no earlier than its registration
    and written as a date; an entry only the branch holds may wait for the merge step."""
    register = safe_load(REGISTER)
    assert stamp_landed.problems(register, ["T-001"]) == []
    assert stamp_landed.problems(register, ["T-001", "T-002"]) == [
        "T-002 is on origin/main and carries no `landed` date"
    ]
    register["results"][0]["landed"] = "2026-09-30"
    assert stamp_landed.problems(register, []) == [
        "T-001 landed on 2026-09-30 before it was registered on 2026-10-01"
    ]
    register["results"][0]["landed"] = "October"
    assert stamp_landed.problems(register, []) == ["T-001: `landed` 'October' is not a date"]


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


def test_the_backfill_dates_an_entry_by_the_merge_that_brought_it_to_main(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """On `main`'s first-parent history an entry lands with the first commit whose
    register holds it: one committed on `main` lands that day, one written on a branch
    on 3 October lands with the merge on 5 October, and a commit's UTC day is the one
    that counts, so a merge at 23:30 in New York lands the next day. An id `main` has
    never held is not dated."""
    path = "packing/frontier/results.yaml"
    register = tmp_path / path
    register.parent.mkdir(parents=True)
    _git(tmp_path, "init", "-q", "-b", "main")
    register.write_text("results:\n  - id: T-001\n", encoding="utf-8")
    _git(tmp_path, "add", path)
    _git(tmp_path, "commit", "-q", "-m", "one", when="2026-10-01T12:00:00+00:00")
    _git(tmp_path, "checkout", "-q", "-b", "lane")
    register.write_text("results:\n  - id: T-001\n  - id: T-002\n", encoding="utf-8")
    _git(tmp_path, "commit", "-q", "-am", "two", when="2026-10-03T12:00:00+00:00")
    _git(tmp_path, "checkout", "-q", "main")
    _git(tmp_path, "merge", "-q", "--no-ff", "lane", "-m", "merge", when="2026-10-05T09:00:00Z")
    register.write_text(
        "results:\n  - id: T-001\n  - id: T-002\n  - id: T-003\n", encoding="utf-8"
    )
    _git(tmp_path, "commit", "-q", "-am", "three", when="2026-10-05T23:30:00-04:00")
    monkeypatch.setattr(stamp_landed, "REPO", tmp_path)
    assert stamp_landed.first_landings("main", path) == {
        "T-001": "2026-10-01",
        "T-002": "2026-10-05",
        "T-003": "2026-10-06",
    }


def test_every_entry_on_main_carries_the_day_it_landed() -> None:
    """The live register: every entry `origin/main` holds carries `landed`, none before
    its registration. A records pull request that merged without the merge step's stamp
    fails here on `main`, and `stamp_landed --apply` is the fix."""
    on_main = subprocess.run(
        ["git", "show", f"{stamp_landed.MAIN}:{stamp_landed.RESULTS_PATH}"],
        cwd=stamp_landed.REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    assert on_main.returncode == 0, f"{stamp_landed.MAIN} is needed: {on_main.stderr}"
    register = safe_load(stamp_landed.RESULTS.read_text(encoding="utf-8"))
    assert stamp_landed.problems(register, stamp_landed.register_ids(on_main.stdout)) == []
