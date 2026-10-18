"""Tiny real Git histories exercise storage admission without large retained data."""

from __future__ import annotations

import signal
import subprocess
import sys
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Any, cast

import pytest

from devtools import check_added_blobs as tool
from sqpack.yamlio import safe_load

MiB = 1024**2


def git(repo: Path, *arguments: str) -> str:
    result = subprocess.run(
        [
            "git",
            "-c",
            "user.name=Storage fixture",
            "-c",
            "user.email=fixture@example.invalid",
            *arguments,
        ],
        cwd=repo,
        capture_output=True,
        check=True,
        timeout=10,
    )
    return result.stdout.decode().strip()


def commit(repo: Path) -> str:
    git(repo, "commit", "-qm", "fixture")
    return git(repo, "rev-parse", "HEAD")


def add(repo: Path, name: str, data: bytes) -> None:
    (repo / name).parent.mkdir(parents=True, exist_ok=True)
    (repo / name).write_bytes(data)
    git(repo, "add", "--", name)


@pytest.fixture
def repo(tmp_path: Path) -> tuple[Path, str]:
    path = tmp_path / "storage repo"
    path.mkdir()
    git(path, "init", "-qb", "main")
    add(path, "seed.txt", b"seed")
    return path, commit(path)


def test_stack_uses_actual_lower_branch_not_main(repo: tuple[Path, str]) -> None:
    path, main = repo
    add(path, "lower.bin", b"x" * 16)
    lower = commit(path)
    add(path, "own.txt", b"ok")
    commit(path)
    assert tool.violations(tool.inventory(path, lower), per_blob=8, total=32) == []
    assert tool.violations(tool.inventory(path, main), per_blob=8, total=32)


def test_add_then_delete_keeps_history_blob_in_inventory(repo: tuple[Path, str]) -> None:
    path, base = repo
    add(path, "large.bin", b"x" * 16)
    commit(path)
    # Remove only the index entry: keep the fixture bytes on disk.
    git(path, "update-index", "--force-remove", "large.bin")
    commit(path)
    blobs = tool.inventory(path, base)
    assert [(blob.size, blob.paths) for blob in blobs] == [(16, ("large.bin",))]
    assert tool.violations(blobs, per_blob=8, total=32)


def test_unchanged_large_base_blob_is_grandfathered(repo: tuple[Path, str]) -> None:
    path, _ = repo
    add(path, "large.bin", b"x" * 16)
    base = commit(path)
    add(path, "own.txt", b"ok")
    commit(path)
    blobs = tool.inventory(path, base)
    assert [blob.size for blob in blobs] == [2]
    assert tool.violations(blobs, per_blob=8, total=32) == []


def test_reintroduced_base_history_blob_is_checked(repo: tuple[Path, str]) -> None:
    path, _ = repo
    add(path, "large.bin", b"x" * 16)
    commit(path)
    git(path, "update-index", "--force-remove", "large.bin")
    base = commit(path)
    git(path, "add", "large.bin")
    commit(path)
    assert tool.violations(tool.inventory(path, base), per_blob=8, total=32)


def test_pure_rename_of_current_base_blob_does_not_add_storage(repo: tuple[Path, str]) -> None:
    path, _ = repo
    add(path, "large.bin", b"x" * 16)
    base = commit(path)
    (path / "large.bin").rename(path / "renamed.bin")
    git(path, "add", "-A")
    commit(path)
    assert tool.inventory(path, base) == []


def test_copy_of_large_base_blob_is_checked(repo: tuple[Path, str]) -> None:
    path, _ = repo
    add(path, "large.bin", b"x" * 16)
    base = commit(path)
    add(path, "copy.bin", b"x" * 16)
    commit(path)
    exempt = tool.grandfathered(path, base, per_blob=8)
    assert exempt == {"large.bin": 16}
    failures = tool.violations(tool.inventory(path, base), per_blob=8, total=32, exempt=exempt)
    assert len(failures) == 1
    assert "copy.bin" in failures[0]


def test_unique_storage_is_deduplicated_and_distinct_objects_aggregate(
    repo: tuple[Path, str],
) -> None:
    path, base = repo
    add(path, "one.bin", b"x" * 12)
    add(path, "same.bin", b"x" * 12)
    commit(path)
    blobs = tool.inventory(path, base)
    assert len(blobs) == 1
    assert blobs[0].paths == ("one.bin", "same.bin")
    assert tool.violations(blobs, per_blob=20, total=12) == []
    add(path, "different.bin", b"y" * 12)
    commit(path)
    assert tool.violations(tool.inventory(path, base), per_blob=20, total=23)


def test_edit_churn_is_charged_once_per_path_at_its_largest_version(
    repo: tuple[Path, str],
) -> None:
    """Review A1: three versions of one file are one retained file, not three."""
    path, base = repo
    for content in (b"a" * 10, b"b" * 10, b"c" * 12):
        add(path, "register.yaml", content)
        commit(path)
    blobs = tool.inventory(path, base)
    assert sorted(blob.size for blob in blobs) == [10, 10, 12]
    assert tool.charged_bytes(blobs) == 12
    assert tool.violations(blobs, per_blob=20, total=12) == []
    assert tool.violations(blobs, per_blob=20, total=11) == [
        "the largest version of each path totals 12 bytes, exceeding 11"
    ]
    # Every version still meets the per-blob ceiling, including the ones no tree keeps.
    assert len(tool.violations(blobs, per_blob=9, total=64)) == 3


def test_branch_behind_its_base_is_not_charged_for_the_base_newer_files(
    repo: tuple[Path, str],
) -> None:
    path, _ = repo
    add(path, "register.yaml", b"v1" * 8)
    commit(path)
    git(path, "checkout", "-qb", "feature")
    add(path, "own.txt", b"ok")
    commit(path)
    git(path, "checkout", "-q", "main")
    add(path, "register.yaml", b"v2" * 8)
    base = commit(path)
    blobs = tool.inventory(path, base, head="feature")
    assert [(blob.size, blob.paths) for blob in blobs] == [(2, ("own.txt",))]


def test_changed_oversize_base_path_is_grandfathered_and_charged_its_growth(
    repo: tuple[Path, str],
) -> None:
    """Review A2: changing a file already over the ceiling at the base is the status quo."""
    path, _ = repo
    add(path, "large.bin", b"x" * 16)
    base = commit(path)
    add(path, "large.bin", b"y" * 20)
    commit(path)
    blobs = tool.inventory(path, base)
    exempt = tool.grandfathered(path, base, per_blob=8)
    assert exempt == {"large.bin": 16}
    assert tool.violations(blobs, per_blob=8, total=32) != []
    assert tool.violations(blobs, per_blob=8, total=32, exempt=exempt) == []
    assert tool.charged_bytes(blobs, exempt) == 4
    assert tool.violations(blobs, per_blob=8, total=3, exempt=exempt) == [
        "the largest version of each path totals 4 bytes, exceeding 3"
    ]


def test_new_large_path_beside_a_grandfathered_one_is_refused(
    repo: tuple[Path, str],
) -> None:
    path, _ = repo
    add(path, "large.bin", b"x" * 16)
    base = commit(path)
    add(path, "large.bin", b"y" * 16)
    add(path, "new.bin", b"z" * 16)
    commit(path)
    exempt = tool.grandfathered(path, base, per_blob=8)
    failures = tool.violations(tool.inventory(path, base), per_blob=8, total=64, exempt=exempt)
    assert len(failures) == 1
    assert "('new.bin',)" in failures[0]


def test_rename_of_a_grandfathered_path_passes_only_unedited(repo: tuple[Path, str]) -> None:
    path, _ = repo
    add(path, "large.bin", b"x" * 16)
    base = commit(path)
    exempt = tool.grandfathered(path, base, per_blob=8)
    git(path, "mv", "large.bin", "moved.bin")
    commit(path)
    assert tool.inventory(path, base) == []
    add(path, "moved.bin", b"x" * 15 + b"y")
    commit(path)
    failures = tool.violations(tool.inventory(path, base), per_blob=8, total=64, exempt=exempt)
    assert len(failures) == 1
    assert "('moved.bin',)" in failures[0]


def test_grandfathered_paths_are_repository_relative_from_a_subdirectory(
    repo: tuple[Path, str],
) -> None:
    """The PR job runs from `packing/`; the base listing must still name whole paths."""
    path, _ = repo
    add(path, "data/large.bin", b"x" * 16)
    add(path, "tool/run.txt", b"ok")
    base = commit(path)
    assert tool.grandfathered(path / "tool", base, per_blob=8) == {"data/large.bin": 16}


def test_staged_mode_catches_new_bytes_before_commit(repo: tuple[Path, str]) -> None:
    path, base = repo
    add(path, "large.bin", b"x" * 16)
    assert tool.inventory(path, base) == []
    assert tool.violations(tool.inventory(path, base, staged=True), per_blob=8, total=32)


def test_submodule_gitlink_does_not_fetch_or_measure_external_content(
    repo: tuple[Path, str],
) -> None:
    path, base = repo
    git(path, "update-index", "--add", "--cacheinfo", "160000," + "1" * 40 + ",vendor-example")
    commit(path)
    assert tool.inventory(path, base) == []


def test_lfs_pointer_is_refused_whatever_size_it_declares(repo: tuple[Path, str]) -> None:
    """Review A7: the repository does not use LFS, so a pointer is a way around the gate."""
    path, base = repo
    pointer = (
        b"version https://git-lfs.github.com/spec/v1\noid sha256:"
        + b"a" * 64
        + b"\nsize 999999999\n"
    )
    add(path, "external.bin", pointer)
    add(path, "notes.md", b"See version https://git-lfs.github.com/spec/v1 for the format.\n")
    commit(path)
    blobs = tool.inventory(path, base)
    assert {blob.paths: blob.lfs_pointer for blob in blobs} == {
        ("external.bin",): True,
        ("notes.md",): False,
    }
    failures = tool.violations(blobs, per_blob=4096, total=4096)
    assert len(failures) == 1
    assert "Git LFS pointer" in failures[0]
    assert "external.bin" in failures[0]


def test_spaces_and_unicode_paths_are_preserved(repo: tuple[Path, str]) -> None:
    path, base = repo
    add(path, "面 recession.txt", b"new")
    commit(path)
    assert tool.inventory(path, base)[0].paths == ("面 recession.txt",)


def test_nul_grammar_preserves_newline_in_filename() -> None:
    before, after = b"0" * 40, b"a" * 40
    raw = b":000000 100644 " + before + b" " + after + b" A\0a\nfile\0"
    assert tool.parse_changes(raw)[0].path == "a\nfile"


@pytest.mark.parametrize("raw", [b"bad\0path\0", b":000000 100644 x y A\0path\0"])
def test_malformed_raw_metadata_is_refused(raw: bytes) -> None:
    with pytest.raises(tool.MetadataError):
        tool.parse_changes(raw)


def test_missing_base_is_not_a_pass(repo: tuple[Path, str]) -> None:
    path, _ = repo
    with pytest.raises(tool.MetadataError, match=r"not a commit in this clone.*fetch it"):
        tool.inventory(path, "does-not-exist")


def test_shallow_clone_refuses_even_if_tip_exists(
    repo: tuple[Path, str], tmp_path: Path
) -> None:
    path, base = repo
    target = tmp_path / "shallow"
    git(tmp_path, "clone", "-q", "--depth=1", "--no-local", path.as_uri(), str(target))
    with pytest.raises(tool.MetadataError, match="shallow history: fetch the full history"):
        tool.inventory(target, base)


def test_a_range_too_long_says_so_rather_than_asking_for_a_fetch(
    repo: tuple[Path, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Review A5: nothing is missing, so the remedy must not be a fetch."""
    path, base = repo
    add(path, "own.txt", b"ok")
    commit(path)
    # Room for one commit identifier, not for the three objects the range adds.
    monkeypatch.setattr(tool, "MAX_METADATA_BYTES", 100)
    with pytest.raises(tool.MetadataError, match="too long for this gate") as refusal:
        tool.inventory(path, base)
    assert "not a commit" not in str(refusal.value)
    assert f"more than {100 / 1024**2:g} MiB" in str(refusal.value)


@pytest.mark.pool_heavy
@pytest.mark.parametrize(("descriptor", "output_size"), [(1, 65), (2, 65), (1, 0)])
def test_metadata_capture_kills_and_reaps_on_excess_or_timeout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, descriptor: int, output_size: int
) -> None:
    """C1: a tiny byte cap or deadline stops a child before its final output."""
    real_popen = subprocess.Popen
    children: list[subprocess.Popen[bytes]] = []
    code = (
        "import os, signal, sys\n"
        "descriptor = int(sys.argv[1])\n"
        "os.write(3 - descriptor, b'ok')\n"
        "os.write(descriptor, b'x' * int(sys.argv[2]))\n"
        "signal.pause()\n"
        "os.write(descriptor, b'finished')\n"
    )

    def start_git(_arguments: Sequence[str], **kwargs: Any) -> subprocess.Popen[bytes]:
        child = cast(
            "subprocess.Popen[bytes]",
            real_popen(
                [sys.executable, "-c", code, str(descriptor), str(output_size)],
                text=False,
                **kwargs,
            ),
        )
        children.append(child)
        return child

    monkeypatch.setattr(tool.subprocess, "Popen", start_git)
    monkeypatch.setattr(tool, "MAX_METADATA_BYTES", 64)
    monkeypatch.setattr(tool, "MAX_QUERY_SECONDS", 5 if output_size else 0.1)
    message = "too long for this gate" if output_size else "query exceeded"
    with pytest.raises(tool.MetadataError, match=message):
        # A child that does not read its input must not block output enforcement.
        tool._git(  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
            tmp_path, "fixture", deadline=time.monotonic() + 10, data=bytes(256 * 1024)
        )
    assert len(children) == 1
    assert children[0].returncode == -signal.SIGKILL
    assert all(
        pipe is not None and pipe.closed
        for pipe in (children[0].stdin, children[0].stdout, children[0].stderr)
    )


def test_exact_byte_boundaries_and_one_byte_excess() -> None:
    first = tool.Blob("a", 8, ("one",))
    second = tool.Blob("b", 8, ("two",))
    assert tool.violations([first, second], per_blob=8, total=16) == []
    assert tool.violations([tool.Blob("a", 9, ("one",))], per_blob=8, total=16)
    assert tool.violations([first, second], per_blob=8, total=15)


def test_ceilings_are_the_reviewed_policy_file() -> None:
    """Review A8: the ceilings are data; this pins what the policy file declares."""
    assert tool.load_ceilings() == tool.Ceilings(per_blob=5 * MiB, total=48 * MiB)


@pytest.mark.parametrize(
    "text",
    [
        "per_blob_bytes: true\ntotal_bytes: 10\n",
        "per_blob_bytes: 10\n",
        "per_blob_bytes: 10\ntotal_bytes: 10\nallowlist: []\n",
        "per_blob_bytes: 10\ntotal_bytes: 0\n",
        "per_blob_bytes: 10\nper_blob_bytes: 11\ntotal_bytes: 10\n",
        "- 10\n",
        "per_blob_bytes: [\n",
    ],
)
def test_a_malformed_policy_file_refuses_rather_than_defaults(
    tmp_path: Path, text: str
) -> None:
    policy = tmp_path / "added-blobs.yaml"
    policy.write_text(text, encoding="utf-8")
    with pytest.raises(tool.MetadataError):
        tool.load_ceilings(policy)
    with pytest.raises(tool.MetadataError, match="cannot read"):
        tool.load_ceilings(tmp_path / "absent.yaml")


def test_boolean_limits_are_not_numeric_ceilings() -> None:
    with pytest.raises(tool.MetadataError, match="integers"):
        tool.violations([], per_blob=True, total=1)


def test_failed_metadata_cli_never_reports_pass(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def refuse(*_args: object, **_kwargs: object) -> list[tool.Blob]:
        raise tool.MetadataError("incomplete object inventory")

    monkeypatch.setattr(tool, "inventory", refuse)
    assert tool.main(["--base", "HEAD"]) == 2
    assert "PASS" not in capsys.readouterr().out


def test_unreadable_policy_cli_refuses(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(tool, "POLICY", tmp_path / "absent.yaml")
    assert tool.main(["--base", "HEAD"]) == 2
    captured = capsys.readouterr()
    assert "PASS" not in captured.out
    assert "GUARD_REFUSED: cannot read the ceilings" in captured.err


def test_production_ceiling_rejects_one_byte_over_through_the_cli(
    repo: tuple[Path, str],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Review A4: the shipped ceiling, a real blob one byte over it, exit 1 and the REJECT."""
    path, base = repo
    ceilings = tool.load_ceilings()
    add(path, "dump.bin", bytes(ceilings.per_blob + 1))
    commit(path)
    object_id = git(path, "rev-parse", "HEAD:dump.bin")
    monkeypatch.chdir(path)
    assert tool.main(["--base", base]) == 1
    output = capsys.readouterr().out
    assert (
        f"REJECT_ADDED_STORAGE: {ceilings.per_blob + 1} bytes exceeds {ceilings.per_blob}: "
        f"('dump.bin',) ({object_id})"
    ) in output
    assert "PASS" not in output


def test_production_grandfathering_reports_and_passes_through_the_cli(
    repo: tuple[Path, str],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    path, _ = repo
    ceilings = tool.load_ceilings()
    add(path, "atlas.svg", bytes(ceilings.per_blob + 1))
    base = commit(path)
    add(path, "atlas.svg", bytes(ceilings.per_blob) + b"x")
    commit(path)
    monkeypatch.chdir(path)
    assert tool.main(["--base", base]) == 0
    output = capsys.readouterr().out
    assert "GRANDFATHERED:" in output
    assert "('atlas.svg',)" in output
    assert "PASS: 1 unique checked blobs, 0 bytes charged" in output


def merge(repo: Path, branch: str, number: int) -> str:
    git(
        repo,
        "merge",
        "-q",
        "--no-ff",
        "-m",
        f"Merge pull request #{number} from x/{branch}",
        branch,
    )
    return git(repo, "rev-parse", "HEAD")


def test_census_replays_merges_with_their_verdicts(
    repo: tuple[Path, str], capsys: pytest.CaptureFixture[str]
) -> None:
    """Review A1: the measurement behind the ceilings is a mode of the tool."""
    path, _ = repo
    git(path, "checkout", "-qb", "dump")
    add(path, "dump.bin", b"x" * 16)
    commit(path)
    git(path, "checkout", "-q", "main")
    rejected = merge(path, "dump", 7)
    git(path, "checkout", "-qb", "small")
    add(path, "small.txt", b"ok")
    commit(path)
    git(path, "checkout", "-q", "main")
    passed = merge(path, "small", 8)
    ceilings = tool.Ceilings(per_blob=8, total=64)
    rows = tool.census(path, "main", 5, ceilings=ceilings)
    assert [(row.merge, bool(row.failures), row.refusal) for row in rows] == [
        (passed, False, ""),
        (rejected, True, ""),
    ]
    tool.print_census(rows, "main", ceilings)
    output = capsys.readouterr().out
    assert f"{passed[:9]} #8 pass: 1 blobs" in output
    assert f"{rejected[:9]} #7 REJECT: 1 blobs" in output
    assert "SUMMARY: 1 of 2 merges rejected, 0 of them by the total alone" in output


def test_census_cli_uses_the_policy_and_reports(
    repo: tuple[Path, str],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    path, _ = repo
    git(path, "checkout", "-qb", "small")
    add(path, "small.txt", b"ok")
    commit(path)
    git(path, "checkout", "-q", "main")
    merge(path, "small", 9)
    monkeypatch.chdir(path)
    assert tool.main(["--census", "3", "--census-ref", "main"]) == 0
    output = capsys.readouterr().out
    assert "CENSUS: 1 first-parent merges into main; ceilings 5242880/blob" in output
    assert "#9 pass" in output


@pytest.mark.parametrize(
    "arguments",
    [[], ["--base", "HEAD", "--census", "2"], ["--census", "0"], ["--census", "2", "--staged"]],
)
def test_cli_needs_exactly_one_mode(arguments: list[str]) -> None:
    with pytest.raises(SystemExit) as exit_:
        tool.main(arguments)
    assert exit_.value.code == 2


def test_index_conflict_metadata_is_refused() -> None:
    raw = b":000000 000000 " + b"0" * 40 + b" " + b"0" * 40 + b" U\0conflict\0"
    with pytest.raises(tool.MetadataError, match="unmerged"):
        tool.parse_changes(raw)


@pytest.mark.parametrize("status", [b"Z", b"R101", b"C"])
def test_unknown_raw_status_is_refused(status: bytes) -> None:
    raw = b":100644 100644 " + b"a" * 40 + b" " + b"b" * 40 + b" " + status + b"\0a\0b\0"
    with pytest.raises(tool.MetadataError):
        tool.parse_changes(raw)


def test_pr_gate_uses_full_history_and_actual_base_head() -> None:
    workflow = Path(__file__).resolve().parents[2] / ".github/workflows/packing-validation.yml"
    value = safe_load(workflow.read_text(encoding="utf-8"))
    steps = value["jobs"]["validate"]["steps"]
    assert steps[0]["with"]["fetch-depth"] == 0
    gate = next(step for step in steps if step["name"] == "Refuse added bulk Git blobs")
    assert gate["if"] == "github.event_name == 'pull_request'"
    assert gate["env"]["PR_STORAGE_BASE"] == "${{ github.event.pull_request.base.sha }}"
    assert gate["env"]["PR_STORAGE_HEAD"] == "${{ github.event.pull_request.head.sha }}"
    assert '--base "$PR_STORAGE_BASE" --head "$PR_STORAGE_HEAD"' in gate["run"]
    assert steps.index(gate) < next(
        index
        for index, step in enumerate(steps)
        if step.get("name") == "Record the tree this pull-request run validates"
    )
