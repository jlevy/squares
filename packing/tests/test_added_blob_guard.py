"""Tiny real Git histories exercise storage admission without large retained data."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from devtools import check_added_blobs as tool
from sqpack.yamlio import safe_load


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
    assert tool.violations(tool.inventory(path, base), per_blob=8, total=32)


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


def test_lfs_pointer_checks_only_committed_pointer_bytes(repo: tuple[Path, str]) -> None:
    path, base = repo
    pointer = (
        b"version https://git-lfs.github.com/spec/v1\noid sha256:"
        + b"a" * 64
        + b"\nsize 999999999\n"
    )
    add(path, "external.bin", pointer)
    commit(path)
    blobs = tool.inventory(path, base)
    assert [blob.size for blob in blobs] == [len(pointer)]
    assert tool.violations(blobs, per_blob=256, total=256) == []


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
    with pytest.raises(tool.MetadataError):
        tool.inventory(path, "does-not-exist")


def test_shallow_clone_refuses_even_if_tip_exists(
    repo: tuple[Path, str], tmp_path: Path
) -> None:
    path, base = repo
    target = tmp_path / "shallow"
    git(tmp_path, "clone", "-q", "--depth=1", "--no-local", path.as_uri(), str(target))
    with pytest.raises(tool.MetadataError, match="shallow"):
        tool.inventory(target, base)


def test_exact_byte_boundaries_and_one_byte_excess() -> None:
    first = tool.Blob("a", 8, ("one",))
    second = tool.Blob("b", 8, ("two",))
    assert tool.violations([first, second], per_blob=8, total=16) == []
    assert tool.violations([tool.Blob("a", 9, ("one",))], per_blob=8, total=16)
    assert tool.violations([first, second], per_blob=8, total=15)
    assert tool.MAX_BLOB_BYTES == 5 * 1024**2
    assert tool.MAX_TOTAL_BYTES == 20 * 1024**2


def test_boolean_limits_are_not_numeric_ceilings() -> None:
    with pytest.raises(tool.MetadataError, match="integers"):
        tool.violations([], per_blob=True)


def test_failed_metadata_cli_never_reports_pass(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def refuse(*_args: object, **_kwargs: object) -> list[tool.Blob]:
        raise tool.MetadataError("incomplete object inventory")

    monkeypatch.setattr(tool, "inventory", refuse)
    assert tool.main(["--base", "HEAD"]) == 2
    assert "PASS" not in capsys.readouterr().out


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
