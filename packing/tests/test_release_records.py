"""No-public-change records are one file each, so parallel additions never share a hunk.

They were literal entries appended to one tuple at the end of `release.py`, and every merge
of main into another open records pull request conflicted there (think-nrp6). The control
below reproduces that conflict; the test beside it shows two records added on parallel
branches merging clean.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import datetime
import os
import subprocess
from pathlib import Path

import pytest

from devtools import check_release_impact as gate
from devtools import release_records
from sqpack import release

SURVEY = "paper:square-packing-methods-survey"
OUTPUTS = (
    "papers/square-packing-methods-survey.html",
    "papers/square-packing-methods-survey.md",
)


def _record(reason: str, *paths: str) -> release.ReleaseNoPublicChange:
    return release.ReleaseNoPublicChange(
        (SURVEY,), paths or ("packing/campaign/result-requests.yaml",), OUTPUTS, reason
    )


def _literal(records: tuple[release.ReleaseNoPublicChange, ...]) -> str:
    """The tuple as release.py wrote it: one keyword call per record, appended in order."""
    lines = ["RELEASE_NO_PUBLIC_CHANGES: tuple[ReleaseNoPublicChange, ...] = ("]
    for record in records:
        lines.append("    ReleaseNoPublicChange(")
        for field in ("components", "paths", "outputs"):
            lines.append(f"        {field}=(")
            lines += [f"            {item!r}," for item in getattr(record, field)]
            lines.append("        ),")
        lines += ["        reason=(", f"            {record.reason!r}", "        ),", "    ),"]
    return "\n".join([*lines, ")", ""])


class Checkout:
    """A disposable repository whose git ignores the caller's configuration and hooks."""

    def __init__(self, root: Path) -> None:
        self.root = root
        root.mkdir(parents=True, exist_ok=True)
        self.git("init", "-q", "-b", "main")

    def git(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
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
                "user.name=Records fixture",
                "-c",
                "user.email=fixture@example.invalid",
                *args,
            ],
            cwd=self.root,
            env=environment,
            capture_output=True,
            text=True,
            check=check,
        )

    def write(self, path: str, text: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def add_record(self, name: str, record: release.ReleaseNoPublicChange) -> None:
        self.write(f"{release_records.DIRECTORY}/{name}", release_records.render(record))

    def commit(self, message: str) -> None:
        self.git("add", "-A")
        self.git("commit", "-qm", message)


def test_two_records_added_on_parallel_branches_merge_without_a_shared_hunk(
    tmp_path: Path,
) -> None:
    repo = Checkout(tmp_path)
    first = _record("The record already on main.")
    repo.add_record("0000-result-requests.yaml", first)
    repo.commit("main")
    lane_a = _record("Lane A's reviewed finding.")
    lane_b = _record("Lane B's reviewed finding, on the same input.")
    repo.git("checkout", "-qb", "lane-b")
    repo.add_record("2026-11-01-lane-b.yaml", lane_b)
    repo.commit("lane B")
    repo.git("checkout", "-qb", "lane-a", "main")
    repo.add_record("2026-11-01-lane-a.yaml", lane_a)
    repo.commit("lane A")

    merged = repo.git("merge", "--no-edit", "lane-b", check=False)

    assert merged.returncode == 0, merged.stdout + merged.stderr
    assert release_records.load(repo.root) == (first, lane_a, lane_b)


def test_control_the_same_two_records_appended_to_the_old_tuple_conflict(
    tmp_path: Path,
) -> None:
    """The fixture can see the conflict it claims to remove: appended to one tuple, the
    same two additions stop a merge, as #833, #834, #835 and #848 did on 31 October."""
    repo = Checkout(tmp_path)
    first = _record("The record already on main.")
    repo.write(gate.RELEASE_PATH, _literal((first,)))
    repo.commit("main")
    repo.git("checkout", "-qb", "lane-b")
    repo.write(gate.RELEASE_PATH, _literal((first, _record("Lane B's reviewed finding."))))
    repo.commit("lane B")
    repo.git("checkout", "-qb", "lane-a", "main")
    repo.write(gate.RELEASE_PATH, _literal((first, _record("Lane A's reviewed finding."))))
    repo.commit("lane A")

    merged = repo.git("merge", "--no-edit", "lane-b", check=False)

    assert merged.returncode != 0
    assert f"CONFLICT (content): Merge conflict in {gate.RELEASE_PATH}" in merged.stdout


def test_migration_keeps_every_record_in_order_and_removes_the_tuple(tmp_path: Path) -> None:
    records = (
        _record(
            "Rendered byte-identical: the first review.", "packing/devtools/render_changelog.py"
        ),
        _record('A reason with "quotes", a colon: here, a #hash and an é.'),
        release.ReleaseNoPublicChange(
            (SURVEY, "paper:n11-optimality-review"),
            ("packing/frontier/results.yaml", "packing/campaign/result-requests.yaml"),
            (*OUTPUTS, "papers/n11-optimality-review.html"),
            "A long reason " + "that wraps across many lines of YAML " * 12 + "and ends.",
        ),
    )
    repo = Checkout(tmp_path)
    source = "\n".join(
        [
            "class ReleaseNoPublicChange(NamedTuple):",
            '    """A record."""',
            "",
            "",
            _literal(records),
            "",
            "def component_history(component):",
            "    return ()",
            "",
        ]
    )
    repo.write(gate.RELEASE_PATH, source)

    written = release_records.migrate(repo.root)

    assert [path.name for path in written] == [
        "0000-render-changelog.yaml",
        "0001-result-requests.yaml",
        "0002-results.yaml",
    ]
    assert release_records.load(repo.root) == records
    remaining = (repo.root / gate.RELEASE_PATH).read_text(encoding="utf-8")
    assert "RELEASE_NO_PUBLIC_CHANGES" not in remaining
    assert "\n\n\ndef component_history" in remaining
    assert "\n\n\n\n" not in remaining
    # A second run finds nothing to move and leaves every file as it was.
    assert release_records.migrate(repo.root) == ()
    assert release_records.load(repo.root) == records


DAY = datetime.date(2026, 11, 2)


def _branch_from_an_older_main(
    tmp_path: Path,
) -> tuple[Checkout, tuple[release.ReleaseNoPublicChange, ...]]:
    """Main after the move holds A, B and C as files. A branch cut before it kept its own
    tuple, whose order main later changed: C before A, no B, and the lane's own record."""
    held = (_record("Record A."), _record("Record B."), _record("Record C."))
    repo = Checkout(tmp_path)
    for index, record in enumerate(held):
        repo.add_record(f"{index:04d}-result-requests.yaml", record)
    repo.write(gate.RELEASE_PATH, _literal((held[2], held[0], _record("The lane's record."))))
    return repo, held


def test_migration_on_a_tree_with_records_moves_only_what_the_files_lack(
    tmp_path: Path,
) -> None:
    """Review A of #873, finding 2: a branch whose tuple was cut from an older main, as
    #599's and #744's were, has indexes that no longer line up. Its records are matched by
    value, so the ones main holds are dropped wherever they sit, and only the lane's own is
    written, under a dated name."""
    repo, held = _branch_from_an_older_main(tmp_path)

    written = release_records.migrate(repo.root, slug="l99-think-test", day=DAY)

    assert [path.name for path in written] == ["2026-11-02-l99-think-test.yaml"]
    assert release_records.load(repo.root) == (*held, _record("The lane's record."))
    assert "RELEASE_NO_PUBLIC_CHANGES" not in (repo.root / gate.RELEASE_PATH).read_text()


def test_migration_on_a_tree_with_records_needs_a_slug_and_says_how(tmp_path: Path) -> None:
    repo, held = _branch_from_an_older_main(tmp_path)
    with pytest.raises(ValueError, match="1 of the tuple's 3 records") as refusal:
        release_records.migrate(repo.root, day=DAY)
    assert "--slug" in str(refusal.value)
    assert release_records.load(repo.root) == held
    assert "RELEASE_NO_PUBLIC_CHANGES" in (repo.root / gate.RELEASE_PATH).read_text()


def test_migration_of_a_tuple_the_files_already_hold_writes_nothing(tmp_path: Path) -> None:
    repo, held = _branch_from_an_older_main(tmp_path)
    repo.write(gate.RELEASE_PATH, _literal((held[1], held[0])))
    assert release_records.migrate(repo.root, day=DAY) == ()
    assert release_records.load(repo.root) == held
    assert "RELEASE_NO_PUBLIC_CHANGES" not in (repo.root / gate.RELEASE_PATH).read_text()


def test_migration_refuses_to_overwrite_a_different_record(tmp_path: Path) -> None:
    repo, held = _branch_from_an_older_main(tmp_path)
    repo.add_record("2026-11-02-l99-think-test.yaml", _record("Another lane's record."))
    with pytest.raises(ValueError, match="already holds a different record"):
        release_records.migrate(repo.root, slug="l99-think-test", day=DAY)
    assert "RELEASE_NO_PUBLIC_CHANGES" in (repo.root / gate.RELEASE_PATH).read_text()
    assert len(release_records.load(repo.root)) == len(held) + 1


@pytest.mark.parametrize(
    "name",
    [
        "0000-result-requests.yaml",
        "0246-result-requests.yaml",
        "2026-11-02-l17-think-nrp6.yaml",
    ],
)
def test_a_dated_or_migrated_name_is_accepted(tmp_path: Path, name: str) -> None:
    directory = tmp_path / release_records.DIRECTORY
    directory.mkdir(parents=True)
    (directory / name).write_text(release_records.render(_record("Fine.")), encoding="utf-8")
    assert release_records.load(tmp_path) == (_record("Fine."),)


@pytest.mark.parametrize(
    ("name", "text", "expected"),
    [
        ("2026-11-01-lane.yml", None, "name a record"),
        ("Lane A.yaml", None, "name a record"),
        # Review A of #873, finding 1: a lane copying the listing's last name would write
        # 0247-result-requests.yaml, and two lanes doing so collide; the numbered names are
        # the 247 records the move wrote, and every later record is dated.
        ("0247-result-requests.yaml", None, "a new record is dated"),
        ("9999-zzz.yaml", None, "a new record is dated"),
        ("2026-99-99-not-a-date.yaml", None, "not a calendar date"),
        ("2026-02-30-l17-lane.yaml", None, "not a calendar date"),
        # Finding 5: the schema refuses what the gate would refuse anyway, so `check` says so.
        (
            "2026-11-01-lane.yaml",
            "components: []\npaths: [b]\noutputs: [c]\nreason: r\n",
            "components",
        ),
        (
            "2026-11-01-lane.yaml",
            "components: [a, a]\npaths: [b]\noutputs: [c]\nreason: r\n",
            "components",
        ),
        (
            "2026-11-01-lane.yaml",
            "components: [a]\npaths: ['']\noutputs: [c]\nreason: r\n",
            "paths",
        ),
        (
            "2026-11-01-lane.yaml",
            "components: [a]\npaths: [b]\noutputs: [c]\nreason: ''\n",
            "reason",
        ),
        (
            "2026-11-01-lane.yaml",
            "components: [a]\npaths: [b]\noutputs: [c]\nreason: ' r'\n",
            "reason",
        ),
        ("2026-11-01-lane.yaml", "components: [a]\npaths: [b]\noutputs: [c]\n", "reason"),
        (
            "2026-11-01-lane.yaml",
            "components: a\npaths: [b]\noutputs: [c]\nreason: r\n",
            "not of type",
        ),
        (
            "2026-11-01-lane.yaml",
            "components: [a]\npaths: [b]\noutputs: [c]\nreason: r\nreviewer: me\n",
            "Additional properties",
        ),
        (
            "2026-11-01-lane.yaml",
            "components: [a]\npaths: [b]\noutputs: [c]\nreason: r\nreason: s\n",
            "duplicate key",
        ),
    ],
)
def test_a_misnamed_or_malformed_record_is_refused_not_skipped(
    tmp_path: Path, name: str, text: str | None, expected: str
) -> None:
    """A record the reader skipped would only ever fail closed, but silently: a lane would
    see its exemption missing with no word why. Refusing names the file and the fault."""
    directory = tmp_path / release_records.DIRECTORY
    directory.mkdir(parents=True)
    (directory / name).write_text(
        text if text is not None else release_records.render(_record("Fine.")),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match=expected) as refusal:
        release_records.load(tmp_path)
    assert name in str(refusal.value)


def test_records_read_at_a_revision_equal_the_working_tree(tmp_path: Path) -> None:
    repo = Checkout(tmp_path)
    for index in range(3):
        repo.add_record(f"000{index}-result-requests.yaml", _record(f"Record {index}."))
    repo.commit("records")
    assert release_records.load_at(repo.root, "HEAD") == release_records.load(repo.root)
    assert len(release_records.load_at(repo.root, "HEAD")) == 3
    repo.git("rm", "-rq", "packing")
    repo.commit("no records")
    assert release_records.load_at(repo.root, "HEAD") == ()


def test_a_tree_after_the_move_reads_as_the_tuple_before_it(tmp_path: Path) -> None:
    """`check --against` is the comparison the move was measured with: a revision holding
    the tuple and a working tree holding the files say the same records, in order."""
    records = (_record("First."), _record("Second."))
    repo = Checkout(tmp_path)
    repo.write(gate.RELEASE_PATH, _literal(records))
    repo.commit("the tuple")
    release_records.migrate(repo.root)
    assert release_records.retained_at(repo.root, "HEAD") == records
    assert release_records.compared(repo.root, "HEAD") == (
        "2 records; HEAD holds 2, which the working tree keeps in order; 0 fresh"
    )
    repo.add_record("2026-11-02-a-lane.yaml", _record("A lane's new finding."))
    assert release_records.compared(repo.root, "HEAD").endswith("in order; 1 fresh")


def test_the_repository_records_load_and_release_py_keeps_no_tuple() -> None:
    """The migrated records validate, keep the tuple's order as numbered names, and
    nothing appends to a tuple in `release.py` again."""
    records = release_records.load()
    directory = release_records.REPO / release_records.DIRECTORY
    names = sorted(path.name for path in directory.iterdir())
    assert len(records) == len(names) >= release_records.MIGRATED == 247
    numbered = [name for name in names if not name.startswith("20")]
    assert [name[:4] for name in numbered] == [f"{index:04d}" for index in range(247)]
    fields = gate._assignments(Path(release.__file__).read_bytes())  # noqa: SLF001
    assert "RELEASE_NO_PUBLIC_CHANGES" not in fields
    assert not hasattr(release, "RELEASE_NO_PUBLIC_CHANGES")
