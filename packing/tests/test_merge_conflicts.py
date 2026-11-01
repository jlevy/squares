"""The merge census recomputes each retained merge and names the block that conflicted."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from devtools import merge_conflicts

BASE = 'DATA = "pin"\n\n\nRECORDS = (\n    Record(\n        name="first",\n    ),\n)\n'


def _entry(name: str, components: tuple[str, ...]) -> str:
    """A record shaped as `release.py`'s were, so two of them share most of their lines."""
    if len(components) == 1:
        listed = f"        components=({components[0]!r},),\n"
    else:
        listed = (
            "        components=(\n"
            + "".join(f"            {component!r},\n" for component in components)
            + "        ),\n"
        )
    return (
        "    Record(\n"
        + listed
        + "        outputs=(\n            'papers/survey.html',\n        ),\n"
        + f"        reason=({name!r}),\n    ),\n"
    )


def _appended(entry: str) -> str:
    return BASE.removesuffix(")\n") + entry + ")\n"


class Checkout:
    def __init__(self, root: Path) -> None:
        self.root = root
        root.mkdir(parents=True, exist_ok=True)
        self.git("init", "-q", "-b", "main")

    def git(self, *args: str) -> str:
        environment = {
            key: value for key, value in os.environ.items() if not key.startswith("GIT_")
        }
        environment.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        return subprocess.run(
            [
                "git",
                "-c",
                f"core.hooksPath={os.devnull}",
                "-c",
                "commit.gpgsign=false",
                "-c",
                "user.name=Census fixture",
                "-c",
                "user.email=fixture@example.invalid",
                *args,
            ],
            cwd=self.root,
            env=environment,
            capture_output=True,
            text=True,
            check=True,
        ).stdout

    def commit(self, path: str, text: str, message: str) -> None:
        (self.root / path).write_text(text, encoding="utf-8")
        self.git("add", path)
        self.git("commit", "-qm", message)


def _two_lanes(tmp_path: Path) -> Checkout:
    """Main, then two lanes that each append a record; lane A merges lane B's main-bound
    work by hand, keeping its own side, and lands on main as pull request #7."""
    repo = Checkout(tmp_path)
    repo.commit("release.py", BASE, "base")
    repo.git("checkout", "-qb", "lane-b")
    repo.commit("release.py", _appended(_entry("lane B", ("survey", "review"))), "lane B")
    repo.git("checkout", "-qb", "lane-a", "main")
    repo.commit("release.py", _appended(_entry("lane A", ("survey",))), "lane A")
    repo.git("merge", "-q", "-s", "ours", "--no-edit", "lane-b")
    repo.git("checkout", "-q", "main")
    repo.git(
        "merge", "-q", "--no-ff", "-m", "Merge pull request #7 from fixture/lane-a", "lane-a"
    )
    return repo


def test_a_merge_of_two_appended_records_is_charged_to_the_tuple_and_its_pr(
    tmp_path: Path,
) -> None:
    repo = _two_lanes(tmp_path)
    report = merge_conflicts.census(repo.root, ref="main", since="2000-01-01")
    assert report.merges == 2
    assert report.pull_requests == 1
    (conflict,) = report.conflicts
    assert conflict.pull_request == 7
    assert {block for _path, block, _hunks in conflict.blocks} == {"RECORDS"}
    lines = merge_conflicts.summary(report)
    assert lines[0].endswith("in 1 pull requests; 1 conflicted")
    assert lines[1].startswith("release.py :: RECORDS: 1 merges (1 conflicting nowhere else)")
    assert lines[1].endswith("(#7)")


def test_a_union_driver_interleaves_two_records_that_share_lines(tmp_path: Path) -> None:
    """Git matches the lines two appended records share and splits one conflict into
    several, so `merge=union` keeps both sides of each piece: one malformed record."""
    repo = _two_lanes(tmp_path)
    report = merge_conflicts.census(repo.root, ref="main", since="2000-01-01", union=True)
    (conflict,) = report.conflicts
    assert conflict.union == (("release.py", "broken"),)
    # Review A of #873, finding 8: the figure quoted for the tuple, the merges where it
    # was the only conflict, is one the summary prints, not one read off `--json`.
    assert merge_conflicts.summary(report)[-2:] == [
        "release.py under merge=union: broken 1",
        "release.py :: RECORDS, where it was the only conflict, under merge=union: broken 1",
    ]


def test_a_binary_conflict_is_counted_whole_and_does_not_stop_the_census(
    tmp_path: Path,
) -> None:
    """Finding 7: Git writes no markers into a conflicted binary file, and its bytes are
    not text, so the census reads git's output as bytes and counts the file whole."""
    repo = Checkout(tmp_path)
    blob = repo.root / "poster.png"
    blob.write_bytes(b"\x89PNG\x00\xff base")
    repo.git("add", "poster.png")
    repo.git("commit", "-qm", "base")
    repo.git("checkout", "-qb", "lane-b")
    blob.write_bytes(b"\x89PNG\x00\xfe lane B")
    repo.git("commit", "-qam", "lane B")
    repo.git("checkout", "-qb", "lane-a", "main")
    blob.write_bytes(b"\x89PNG\x00\xfd lane A")
    repo.git("commit", "-qam", "lane A")
    repo.git("merge", "-q", "-s", "ours", "--no-edit", "lane-b")

    report = merge_conflicts.census(repo.root, ref="lane-a", since="2000-01-01", union=True)

    (conflict,) = report.conflicts
    assert conflict.blocks == (("poster.png", "(whole file)", 1),)
    assert conflict.union == (("poster.png", "differs"),)
    filtered = merge_conflicts.census(
        repo.root, ref="lane-a", since="2000-01-01", paths=("release.py",)
    )
    assert filtered.conflicts == ()


def test_a_conflict_is_named_by_the_statement_the_hunk_starts() -> None:
    lines = ["A = 1", "", "<<<<<<< ours", "PIN = 'a'", "=======", "PIN = 'b'", ">>>>>>> b"]
    assert merge_conflicts.block_of("release.py", lines, 2) == "PIN"
    inside = ["RECORDS = (", "    'x',", "<<<<<<< ours", "    'a',", "=======", ">>>>>>> b"]
    assert merge_conflicts.block_of("release.py", inside, 2) == "RECORDS"
    assert merge_conflicts.block_of("notes.md", ["## Results", "<<<<<<< ours"], 1) == (
        "## Results"
    )
