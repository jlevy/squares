"""Tiny real Git histories exercise storage admission without large retained data.

Sizes are OR-18's. A blob counts as Git stores it (`devtools.git_storage`), so each
fixture states its per-blob ceiling in terms of `stored()` of its own contents. `noise()`
is incompressible, so a noise blob stores at about its checkout size, while short text
stores at a few bytes over its own; `PER` sits between the two. The total is the thin pack
of the range's new objects, which `pack_size()` asks Git for directly; a noise blob lands
in it at about its own size, and it cannot be a delta of other noise.
"""

from __future__ import annotations

import os
import random
import shutil
import signal
import subprocess
import sys
import time
import zlib
from collections.abc import Callable, Iterator, Mapping, Sequence
from pathlib import Path
from typing import Any, cast

import pytest

from devtools import check_added_blobs as tool
from devtools.git_storage import StoredSize, stored_size, stored_size_bound
from sqpack.yamlio import safe_load

MiB = 1024**2
# Over every short text fixture as Git stores it, under every 64-byte noise blob.
PER = 48
DISTINCT = (b"a" * 7, b"b" * 7, b"c" * 7)


def stored(data: bytes) -> int:
    return stored_size(data)


def noise(size: int, seed: int = 0) -> bytes:
    """Incompressible bytes, so the blob stores at about its checkout size."""
    return random.Random(seed).randbytes(size)


def git(repo: Path, *arguments: str, env: Mapping[str, str] | None = None) -> str:
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
        env=env,
    )
    return result.stdout.decode().strip()


def commit(repo: Path) -> str:
    git(repo, "commit", "-qm", "fixture")
    return git(repo, "rev-parse", "HEAD")


def add(repo: Path, name: str, data: bytes) -> None:
    (repo / name).parent.mkdir(parents=True, exist_ok=True)
    (repo / name).write_bytes(data)
    git(repo, "add", "--", name)


def pack_size(repo: Path, base: str, head: str = "HEAD", *extra: str) -> int:
    """Git's own thin pack of the range's new objects, with `extra` objects beside them."""
    revisions = "".join(f"{line}\n" for line in (head, f"^{base}", *extra))
    configuration = [option for setting in tool.PACK_CONFIG for option in ("-c", setting)]
    result = subprocess.run(
        [
            "git",
            *configuration,
            "pack-objects",
            "--revs",
            "--thin",
            "--shallow",
            "--no-sparse",
            "--delta-base-offset",
            "--non-empty",
            "--stdout",
            "-q",
        ],
        cwd=repo,
        input=revisions.encode(),
        capture_output=True,
        check=True,
        timeout=10,
    )
    return len(result.stdout)


def total_failure(added: int, total: int) -> str:
    return (
        f"the range adds {added} bytes to the repository, as a thin pack of its new objects "
        f"against the base, exceeding {total}"
    )


@pytest.fixture(autouse=True)
def isolated_git_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Inherited Git settings can override cwd for fixture writes and guard reads."""
    for name in tuple(os.environ):
        if name.startswith("GIT_"):
            monkeypatch.delenv(name)


@pytest.fixture(scope="session")
def template_repo(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, str]:
    """One seeded repository per session, built outside any inherited Git redirect.

    Review I3 of #406: initializing a repository for every test cost about 0.1 s each,
    and a copy of this one costs a few milliseconds.
    """
    environment = {
        name: value for name, value in os.environ.items() if not name.startswith("GIT_")
    }
    path = tmp_path_factory.mktemp("template") / "storage repo"
    path.mkdir()
    git(path, "init", "-qb", "main", env=environment)
    (path / "seed.txt").write_bytes(b"seed")
    git(path, "add", "--", "seed.txt", env=environment)
    git(path, "commit", "-qm", "fixture", env=environment)
    return path, git(path, "rev-parse", "HEAD", env=environment)


@pytest.fixture
def repo(tmp_path: Path, template_repo: tuple[Path, str]) -> tuple[Path, str]:
    source, base = template_repo
    path = tmp_path / "storage repo"
    shutil.copytree(source, path, symlinks=True)
    return path, base


@pytest.fixture(scope="class", params=["index", "repository"])
def foreign_git_environment(
    request: pytest.FixtureRequest, tmp_path_factory: pytest.TempPathFactory
) -> Iterator[tuple[Path, bytes, str]]:
    """Inject before function fixtures, with sentinel setup safe from caller redirects."""
    with pytest.MonkeyPatch.context() as environment:
        for name in tuple(os.environ):
            if name.startswith("GIT_"):
                environment.delenv(name)
        sentinel = tmp_path_factory.mktemp("foreign-git")
        git(sentinel, "init", "-qb", "main")
        git(sentinel, "commit", "-qm", "sentinel", "--allow-empty")
        git(sentinel, "read-tree", "--empty")
        index = (sentinel / ".git/index").read_bytes()
        refs = git(sentinel, "show-ref", "--head")
        # A redirected add can succeed, so the test detects mutation rather than setup failure.
        (sentinel / "seed.txt").write_bytes(b"foreign seed")
        if cast("str", request.param) == "index":
            environment.setenv("GIT_INDEX_FILE", str(sentinel / ".git/index"))
        else:
            environment.setenv("GIT_DIR", str(sentinel / ".git"))
            environment.setenv("GIT_WORK_TREE", str(sentinel))
        yield sentinel, index, refs


class TestGitEnvironmentIsolation:
    def test_fixture_and_guard_leave_foreign_index_and_refs_unchanged(
        self, foreign_git_environment: tuple[Path, bytes, str], repo: tuple[Path, str]
    ) -> None:
        """F1: real fixture writes and guard reads stay in the fixture."""
        sentinel, index, refs = foreign_git_environment
        path, base = repo
        assert (sentinel / ".git/index").read_bytes() == index
        assert git(sentinel, "show-ref", "--head") == refs
        assert (path / ".git/index").is_file()
        assert git(path, "ls-files") == "seed.txt"
        assert git(path, "rev-parse", "HEAD") == base
        add(path, "own.txt", b"ok")
        staged = tool.inventory(path, base, staged=True)
        assert [(blob.checkout, blob.stored, blob.paths) for blob in staged] == [
            (2, stored(b"ok"), ("own.txt",))
        ]
        head = commit(path)
        assert head != base
        assert git(path, "rev-list", f"{base}..HEAD") == head
        assert git(path, "ls-files") == "own.txt\nseed.txt"
        assert [(blob.checkout, blob.paths) for blob in tool.inventory(path, base)] == [
            (2, ("own.txt",))
        ]
        assert (sentinel / ".git/index").read_bytes() == index
        assert git(sentinel, "show-ref", "--head") == refs
        assert git(sentinel, "write-tree") == git(sentinel, "rev-parse", "HEAD^{tree}")


def test_sizes_are_counted_as_git_stores_them(repo: tuple[Path, str]) -> None:
    """H1 of #406: OR-18's unit, so text is charged a fraction of its checkout bytes."""
    path, base = repo
    text = b"register: entry\n" * 4096
    add(path, "register.yaml", text)
    commit(path)
    (blob,) = tool.inventory(path, base)
    assert blob.checkout == len(text)
    assert blob.stored == stored(text) < len(text) // 50
    # A ceiling at the stored size passes, although the checkout bytes are 50 times over it.
    assert tool.violations([blob], per_blob=stored(text), total=1, added=0) == []
    assert tool.violations([blob], per_blob=stored(text) - 1, total=1, added=0)


def register(entries: int, seed: int = 0) -> bytes:
    """A register of distinct entries: compresses like YAML, and differs line by line."""
    generator = random.Random(seed)
    return b"".join(
        b"- id: T-%05d\n  value: %032x\n" % (index, generator.getrandbits(128))
        for index in range(entries)
    )


def test_rewriting_a_register_costs_its_edits_not_its_versions(repo: tuple[Path, str]) -> None:
    """#578 on #406: 20 rewrites of one large register pack as one copy and 19 deltas.

    Summed as standalone versions, #578's merges of main charged 59.17 MiB of register
    churn; the thin pack of the same range is 2.39 MiB. The total is the pack.
    """
    path, base = repo
    versions = [register(2000 + index) for index in range(20)]
    for content in versions:
        add(path, "frontier/results.yaml", content)
        commit(path)
    blobs = tool.inventory(path, base)
    assert len(blobs) == 20
    summed = sum(blob.stored for blob in blobs)
    assert summed == sum(map(stored, versions))
    added = tool.added_bytes(path, base)
    assert added == pack_size(path, base)
    assert 5 * added < summed
    # A total the summed versions would exceed admits the branch.
    assert tool.violations(blobs, per_blob=stored(versions[-1]), total=added, added=added) == []


def test_repository_configuration_cannot_move_the_total(repo: tuple[Path, str]) -> None:
    """K1 of #406: the pack's settings are the guard's, whatever the clone configures.

    Thirty versions of a register, each five entries from the last, so that the delta
    window, the chain depth, the window's memory and the thread count all move the pack.
    """
    path, base = repo
    generator = random.Random(0)
    entries = register(1500).splitlines(keepends=True)
    for _ in range(30):
        for _ in range(5):
            index = generator.randrange(0, len(entries), 2)
            entries[index + 1] = b"  value: %032x\n" % generator.getrandbits(128)
        add(path, "frontier/results.yaml", b"".join(entries))
        commit(path)
    pinned = tool.added_bytes(path, base)
    assert tool.added_bytes(path, base) == pinned
    # The pins are Git's own defaults, so an unconfigured clone packs the same bytes.
    default = subprocess.run(
        [
            "git",
            "pack-objects",
            "--revs",
            "--thin",
            "--shallow",
            "--no-sparse",
            "--delta-base-offset",
            "--non-empty",
            "--threads=1",
            "--stdout",
            "-q",
        ],
        cwd=path,
        input=f"HEAD\n^{base}\n".encode(),
        capture_output=True,
        check=True,
        timeout=10,
    )
    assert len(default.stdout) == pinned
    for setting, value in (
        ("pack.window", "0"),
        ("pack.depth", "1"),
        ("pack.windowMemory", "1k"),
        ("pack.threads", "4"),
        ("pack.useBitmaps", "true"),
        ("pack.compression", "0"),
        ("core.compression", "0"),
    ):
        git(path, "config", setting, value)
    assert pack_size(path, base) == pinned
    # Git itself, under the clone's settings, would have packed it differently.
    configured = subprocess.run(
        ["git", "pack-objects", "--revs", "--thin", "--stdout", "-q"],
        cwd=path,
        input=f"HEAD\n^{base}\n".encode(),
        capture_output=True,
        check=True,
        timeout=10,
    )
    assert len(configured.stdout) != pinned
    assert tool.added_bytes(path, base) == pinned


def test_a_staged_copy_of_a_base_blob_adds_nothing(repo: tuple[Path, str]) -> None:
    path, _ = repo
    add(path, "large.bin", noise(4096))
    base = commit(path)
    add(path, "copy.bin", noise(4096))
    assert tool.added_bytes(path, base, staged=True) == 0
    add(path, "fresh.bin", noise(4096, 1))
    assert tool.added_bytes(path, base, staged=True) >= 4096


def test_stack_uses_actual_lower_branch_not_main(repo: tuple[Path, str]) -> None:
    path, main = repo
    add(path, "lower.bin", noise(64))
    lower = commit(path)
    add(path, "own.txt", b"ok")
    commit(path)
    assert tool.violations(tool.inventory(path, lower), per_blob=PER, total=1, added=0) == []
    assert tool.violations(tool.inventory(path, main), per_blob=PER, total=1, added=0)
    assert tool.added_bytes(path, lower) < tool.added_bytes(path, main)


def test_add_then_delete_keeps_history_blob_in_inventory(repo: tuple[Path, str]) -> None:
    path, base = repo
    add(path, "large.bin", noise(4096))
    commit(path)
    # Remove only the index entry: keep the fixture bytes on disk.
    git(path, "update-index", "--force-remove", "large.bin")
    commit(path)
    blobs = tool.inventory(path, base)
    assert [(blob.checkout, blob.paths, blob.charged) for blob in blobs] == [
        (4096, ("large.bin",), True)
    ]
    assert tool.violations(blobs, per_blob=PER, total=1, added=0)
    # History keeps the deleted blob, so the pack carries it.
    assert tool.added_bytes(path, base) >= 4096


def test_unchanged_large_base_blob_is_grandfathered(repo: tuple[Path, str]) -> None:
    path, _ = repo
    add(path, "large.bin", noise(64))
    base = commit(path)
    add(path, "own.txt", b"ok")
    commit(path)
    blobs = tool.inventory(path, base)
    assert [blob.checkout for blob in blobs] == [2]
    assert tool.violations(blobs, per_blob=PER, total=1, added=0) == []


def test_reintroduced_base_history_blob_is_checked(repo: tuple[Path, str]) -> None:
    path, _ = repo
    add(path, "large.bin", noise(64))
    commit(path)
    git(path, "update-index", "--force-remove", "large.bin")
    base = commit(path)
    git(path, "add", "large.bin")
    commit(path)
    assert tool.violations(tool.inventory(path, base), per_blob=PER, total=1, added=0)


def test_pure_rename_of_current_base_blob_does_not_add_storage(repo: tuple[Path, str]) -> None:
    path, _ = repo
    add(path, "large.bin", noise(64))
    base = commit(path)
    (path / "large.bin").rename(path / "renamed.bin")
    git(path, "add", "-A")
    commit(path)
    assert tool.inventory(path, base) == []


def test_mode_only_change_adds_no_blob(repo: tuple[Path, str]) -> None:
    """H4 of #406 (P4): `chmod +x` stores no new blob, so nothing is charged."""
    path, _ = repo
    add(path, "tool.sh", b"x" * 7)
    base = commit(path)
    git(path, "update-index", "--chmod=+x", "tool.sh")
    commit(path)
    assert tool.inventory(path, base) == []


def test_blob_already_in_the_base_tree_is_checked_but_not_charged(
    repo: tuple[Path, str],
) -> None:
    """H4 of #406 (P5): the same bytes the newer base gained are stored already."""
    path, _ = repo
    git(path, "checkout", "-qb", "feature")
    add(path, "same.bin", noise(4096))
    commit(path)
    git(path, "checkout", "-q", "main")
    add(path, "same.bin", noise(4096))
    add(path, "other.txt", b"o")
    base = commit(path)
    (blob,) = tool.inventory(path, base, head="feature")
    assert (blob.paths, blob.charged) == (("same.bin",), False)
    # The pack holds the branch's commit and tree, not the blob the base stores already.
    assert tool.added_bytes(path, base, head="feature") < 4096
    # It is still a new path's blob, so the per-blob ceiling holds it.
    assert tool.violations([blob], per_blob=PER, total=1, added=0) == [
        (
            f"{stored(noise(4096))} bytes exceeds {PER} as Git stores them: ('same.bin',) "
            f"({blob.object_id}, 4096 bytes in a checkout)"
        )
    ]


def test_copy_of_large_base_blob_is_checked(repo: tuple[Path, str]) -> None:
    path, _ = repo
    add(path, "large.bin", noise(4096))
    base = commit(path)
    add(path, "copy.bin", noise(4096))
    commit(path)
    exempt = tool.grandfathered(path, base, per_blob=PER)
    assert exempt == {"large.bin": stored(noise(4096))}
    blobs = tool.inventory(path, base)
    failures = tool.violations(blobs, per_blob=PER, total=1, added=0, exempt=exempt)
    assert len(failures) == 1
    assert "copy.bin" in failures[0]
    # H4 of #406: a copy of a base blob stores nothing new, so the pack does not carry it.
    assert [blob.charged for blob in blobs] == [False]
    assert tool.added_bytes(path, base) < 4096


def test_a_base_blob_moved_through_a_new_path_is_judged_where_the_tip_keeps_it(
    repo: tuple[Path, str],
) -> None:
    """A base blob stores nothing new, so only the tip's paths decide its grandfathering."""
    path, _ = repo
    add(path, "atlas.svg", noise(64))
    add(path, "other.svg", noise(64, 1))
    base = commit(path)
    add(path, "scratch.svg", noise(64, 1))
    commit(path)
    git(path, "mv", "-f", "scratch.svg", "atlas.svg")
    commit(path)
    (blob,) = tool.inventory(path, base)
    assert (blob.paths, blob.charged) == (("atlas.svg",), False)
    assert tool.judge(path, base, [blob], tool.Ceilings(per_blob=PER, total=1), added=0) == (
        {"atlas.svg": stored(noise(64))},
        [],
    )


def test_unique_storage_is_deduplicated_and_distinct_objects_aggregate(
    repo: tuple[Path, str],
) -> None:
    path, base = repo
    add(path, "one.bin", noise(4096))
    add(path, "same.bin", noise(4096))
    commit(path)
    blobs = tool.inventory(path, base)
    assert len(blobs) == 1
    assert blobs[0].paths == ("one.bin", "same.bin")
    # One object, packed once, whatever the number of paths that carry it.
    once = tool.added_bytes(path, base)
    assert 4096 <= once < 2 * 4096
    ceiling = stored(noise(4096))
    assert tool.violations(blobs, per_blob=ceiling, total=once, added=once) == []
    add(path, "different.bin", noise(4096, 1))
    commit(path)
    both = tool.added_bytes(path, base)
    assert both >= 2 * 4096
    blobs = tool.inventory(path, base)
    assert tool.violations(blobs, per_blob=ceiling, total=both - 1, added=both) == [
        total_failure(both, both - 1)
    ]


@pytest.mark.parametrize("staged", [False, True])
def test_shared_history_does_not_hide_distinct_retained_blobs(
    repo: tuple[Path, str],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    *,
    staged: bool,
) -> None:
    """D1: a shared larger template cannot hide smaller distinct head/index blobs."""
    path, base = repo
    names = ("one.bin", "two.bin", "three.bin")
    for name in names:
        add(path, name, b"template")
    commit(path)
    template = pack_size(path, base)
    monkeypatch.chdir(path)
    monkeypatch.setattr(
        tool, "load_ceilings", lambda: tool.Ceilings(per_blob=PER, total=template)
    )
    arguments = ["--base", base, *(["--staged"] if staged else [])]
    # Identical retained copies pack their one object once, even at three paths.
    assert tool.main(arguments) == 0
    assert f"PASS: {template} bytes added as a thin pack" in capsys.readouterr().out
    for name, content in zip(names, DISTINCT, strict=True):
        add(path, name, content)
    if not staged:
        commit(path)
        everything = pack_size(path, base)
    else:
        # Index membership comes from the index, even if worktree bytes disagree.
        for name in names:
            (path / name).write_bytes(b"template")
        index = [git(path, "rev-parse", f":{name}") for name in names]
        everything = pack_size(path, base, "HEAD", *index)
    assert everything > template
    assert tool.main(arguments) == 1
    output = capsys.readouterr().out
    assert f"REJECT_ADDED_STORAGE: {total_failure(everything, template)}" in output


@pytest.mark.parametrize("ending", ["delete", "revert"])
def test_versions_the_head_deleted_or_reverted_are_charged(
    repo: tuple[Path, str], ending: str
) -> None:
    """H2 of #406 (P1, P1b): a merge commit keeps every version, whatever the head keeps."""
    path, base = repo
    names = ("one.bin", "two.bin", "three.bin")
    for name in names:
        add(path, name, noise(1024))
    commit(path)
    for seed, name in enumerate(names, start=1):
        add(path, name, noise(1024, seed))
    commit(path)
    if ending == "delete":
        git(path, "rm", "-q", "--cached", *names)
    else:
        for name in names:
            add(path, name, noise(1024))
    commit(path)
    blobs = tool.inventory(path, base)
    assert len(tool._charged(blobs)) == 4  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    everything = tool.added_bytes(path, base)
    # The template and the three versions the head no longer keeps are all in the pack.
    assert everything >= 4 * 1024
    assert everything == pack_size(path, base)
    ceiling = stored(noise(1024))
    assert tool.violations(blobs, per_blob=ceiling, total=everything, added=everything) == []
    assert tool.violations(blobs, per_blob=ceiling, total=everything - 1, added=everything) == [
        total_failure(everything, everything - 1)
    ]


def test_every_new_version_of_one_path_is_charged(repo: tuple[Path, str]) -> None:
    """H2 of #406 (P2): ten versions of one regenerated file are ten stored blobs."""
    path, base = repo
    versions = [noise(512, seed) for seed in range(10)]
    for content in versions:
        add(path, "out.bin", content)
        commit(path)
    blobs = tool.inventory(path, base)
    assert len(blobs) == 10
    # Noise has no delta against other noise, so each version is in the pack whole.
    added = tool.added_bytes(path, base)
    assert added >= 10 * 512
    assert tool.violations(blobs, per_blob=PER, total=added - 1, added=added)
    # Every version also meets the per-blob ceiling, including the ones no tree keeps.
    over = tool.violations(blobs, per_blob=stored(versions[0]) - 1, total=1, added=0)
    assert len(over) == 10


def test_grandfathered_path_rewrites_are_charged_in_full(repo: tuple[Path, str]) -> None:
    """H2 of #406 (P3): grandfathering lifts the per-blob ceiling, never the total."""
    path, _ = repo
    add(path, "atlas.svg", noise(1024))
    base = commit(path)
    rewrites = [noise(1024, seed) for seed in range(1, 6)]
    for content in rewrites:
        add(path, "atlas.svg", content)
        commit(path)
    blobs = tool.inventory(path, base)
    rewritten = tool.added_bytes(path, base)
    assert rewritten >= 5 * 1024
    ceilings = tool.Ceilings(per_blob=PER, total=rewritten)
    assert tool.judge(path, base, blobs, ceilings, added=rewritten) == (
        {"atlas.svg": stored(noise(1024))},
        [],
    )
    _, failures = tool.judge(
        path, base, blobs, tool.Ceilings(per_blob=PER, total=rewritten - 1), added=rewritten
    )
    assert failures == [total_failure(rewritten, rewritten - 1)]


def test_retained_membership_uses_the_selected_head(repo: tuple[Path, str]) -> None:
    path, base = repo
    for name in ("one", "two", "three"):
        add(path, name, noise(1024))
    shared = commit(path)
    for seed, name in enumerate(("one", "two", "three"), start=1):
        add(path, name, noise(1024, seed))
    distinct = commit(path)
    git(path, "checkout", "--detach", shared)
    assert len(tool.inventory(path, base, head=distinct)) == 4
    assert len(tool.inventory(path, base, head=shared)) == 1
    assert tool.added_bytes(path, base, head=distinct) >= 4 * 1024
    assert 1024 <= tool.added_bytes(path, base, head=shared) < 2 * 1024


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
    assert [(blob.checkout, blob.paths) for blob in blobs] == [(2, ("own.txt",))]


def test_changed_oversize_base_path_is_grandfathered_and_charged_in_full(
    repo: tuple[Path, str],
) -> None:
    """Review A2: changing a file already over the ceiling at the base is the status quo."""
    path, _ = repo
    add(path, "large.bin", noise(64))
    base = commit(path)
    add(path, "large.bin", noise(80, 1))
    commit(path)
    blobs = tool.inventory(path, base)
    exempt = tool.grandfathered(path, base, per_blob=PER)
    assert exempt == {"large.bin": stored(noise(64))}
    added = tool.added_bytes(path, base)
    assert added >= 80
    assert tool.violations(blobs, per_blob=PER, total=added, added=added) != []
    assert tool.violations(blobs, per_blob=PER, total=added, added=added, exempt=exempt) == []
    assert tool.violations(
        blobs, per_blob=PER, total=added - 1, added=added, exempt=exempt
    ) == [total_failure(added, added - 1)]


def test_new_large_path_beside_a_grandfathered_one_is_refused(
    repo: tuple[Path, str],
) -> None:
    path, _ = repo
    add(path, "large.bin", noise(64))
    base = commit(path)
    add(path, "large.bin", noise(64, 1))
    add(path, "new.bin", noise(64, 2))
    commit(path)
    exempt = tool.grandfathered(path, base, per_blob=PER)
    failures = tool.violations(
        tool.inventory(path, base), per_blob=PER, total=1, added=0, exempt=exempt
    )
    assert len(failures) == 1
    assert "('new.bin',)" in failures[0]


def test_one_blob_at_a_grandfathered_and_a_new_path_is_refused(repo: tuple[Path, str]) -> None:
    """H3 of #406: grandfathering needs every path of the blob, not any one of them."""
    path, _ = repo
    add(path, "large.bin", noise(64))
    base = commit(path)
    add(path, "large.bin", noise(64, 1))
    add(path, "new.bin", noise(64, 1))
    commit(path)
    (blob,) = tool.inventory(path, base)
    exempt, failures = tool.judge(
        path, base, [blob], tool.Ceilings(per_blob=PER, total=1024), added=0
    )
    assert exempt == {"large.bin": stored(noise(64))}
    assert failures == [
        (
            f"{blob.stored} bytes exceeds {PER} as Git stores them: ('large.bin', 'new.bin') "
            f"({blob.object_id}, 64 bytes in a checkout)"
        )
    ]


def test_shrinking_a_grandfathered_path_offsets_nothing(repo: tuple[Path, str]) -> None:
    """H3 of #406: a grandfathered path that shrinks cannot pay for new data elsewhere."""
    path, _ = repo
    add(path, "large.bin", noise(64))
    base = commit(path)
    add(path, "large.bin", b"s" * 10)
    for name, content in zip(("a", "b", "c"), DISTINCT, strict=True):
        add(path, name, content)
    commit(path)
    blobs = tool.inventory(path, base)
    added = tool.added_bytes(path, base)
    ceilings = tool.Ceilings(per_blob=PER, total=added)
    assert tool.judge(path, base, blobs, ceilings, added=added) == ({}, [])
    ceilings = tool.Ceilings(per_blob=PER, total=added - 1)
    _, failures = tool.judge(path, base, blobs, ceilings, added=added)
    assert failures == [total_failure(added, added - 1)]


def test_grandfathering_needs_more_than_the_ceiling_at_the_base(
    repo: tuple[Path, str],
) -> None:
    """H3 of #406: a base blob exactly at the per-blob ceiling is not grandfathered."""
    path, _ = repo
    add(path, "big.bin", noise(64))
    base = commit(path)
    add(path, "big.bin", noise(80, 1))
    commit(path)
    at_base = stored(noise(64))
    blobs = tool.inventory(path, base)
    assert tool.grandfathered(path, base, per_blob=at_base) == {}
    assert tool.grandfathered(path, base, per_blob=at_base - 1) == {"big.bin": at_base}
    # The unit is the stored one, so a base blob at the ceiling in a checkout is over it.
    assert tool.grandfathered(path, base, per_blob=64) == {"big.bin": at_base}
    ceilings = tool.Ceilings(per_blob=at_base, total=1024)
    _, failures = tool.judge(path, base, blobs, ceilings, added=0)
    assert len(failures) == 1
    assert "('big.bin',)" in failures[0]
    ceilings = tool.Ceilings(per_blob=at_base - 1, total=1024)
    assert tool.judge(path, base, blobs, ceilings, added=0) == (
        {"big.bin": at_base},
        [],
    )


def test_rename_of_a_grandfathered_path_passes_only_unedited(repo: tuple[Path, str]) -> None:
    path, _ = repo
    add(path, "large.bin", noise(64))
    base = commit(path)
    exempt = tool.grandfathered(path, base, per_blob=PER)
    git(path, "mv", "large.bin", "moved.bin")
    commit(path)
    assert tool.inventory(path, base) == []
    add(path, "moved.bin", noise(64)[:-1] + b"y")
    commit(path)
    failures = tool.violations(
        tool.inventory(path, base), per_blob=PER, total=1, added=0, exempt=exempt
    )
    assert len(failures) == 1
    assert "('moved.bin',)" in failures[0]


def test_grandfathered_paths_are_repository_relative_from_a_subdirectory(
    repo: tuple[Path, str],
) -> None:
    """The PR job runs from `packing/`; the base listing must still name whole paths."""
    path, _ = repo
    add(path, "data/large.bin", noise(64))
    add(path, "data/other.bin", noise(64, 1))
    add(path, "tool/run.txt", b"ok")
    base = commit(path)
    assert tool.grandfathered(path / "tool", base, per_blob=PER) == {
        "data/large.bin": stored(noise(64)),
        "data/other.bin": stored(noise(64, 1)),
    }
    # A judgement asks only about the paths of blobs over the ceiling.
    assert tool.grandfathered(path, base, per_blob=PER, paths=["data/other.bin", "x"]) == {
        "data/other.bin": stored(noise(64, 1))
    }


def test_staged_mode_catches_new_bytes_before_commit(repo: tuple[Path, str]) -> None:
    path, base = repo
    add(path, "large.bin", noise(4096))
    assert tool.inventory(path, base) == []
    # Nothing is committed, so the range packs to nothing until the index joins it.
    assert tool.added_bytes(path, base) == 0
    staged = tool.inventory(path, base, staged=True)
    assert [blob.charged for blob in staged] == [True]
    assert tool.violations(staged, per_blob=PER, total=1, added=0)
    added = tool.added_bytes(path, base, staged=True)
    assert added >= 4096
    assert added == pack_size(path, base, "HEAD", git(path, "rev-parse", ":large.bin"))


def test_submodule_gitlink_does_not_fetch_or_measure_external_content(
    repo: tuple[Path, str],
) -> None:
    path, base = repo
    git(path, "update-index", "--add", "--cacheinfo", "160000," + "1" * 40 + ",vendor-example")
    commit(path)
    assert tool.inventory(path, base) == []


def lfs_pointer(size: int) -> bytes:
    pointer = b"version https://git-lfs.github.com/spec/v1\noid sha256:" + b"a" * 64 + b"\n"
    return pointer + b"x" * (size - len(pointer))


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
    failures = tool.violations(blobs, per_blob=4096, total=4096, added=0)
    assert len(failures) == 1
    assert "Git LFS pointer" in failures[0]
    assert "external.bin" in failures[0]


@pytest.mark.parametrize(("size", "pointer"), [(1024, True), (1025, False)])
def test_lfs_pointers_are_read_up_to_1024_bytes(
    repo: tuple[Path, str], size: int, *, pointer: bool
) -> None:
    """H3 of #406: git-lfs reads a blob of at most 1024 bytes as a pointer, never more."""
    path, base = repo
    add(path, "external.bin", lfs_pointer(size))
    commit(path)
    (blob,) = tool.inventory(path, base)
    assert (blob.checkout, blob.lfs_pointer) == (size, pointer)


def test_spaces_and_unicode_paths_are_preserved(repo: tuple[Path, str]) -> None:
    path, base = repo
    add(path, "面 recession.txt", b"new")
    commit(path)
    assert tool.inventory(path, base)[0].paths == ("面 recession.txt",)


def test_nul_grammar_preserves_newline_in_filename() -> None:
    before, after = b"0" * 40, b"a" * 40
    raw = b":000000 100644 " + before + b" " + after + b" A\0a\nfile\0"
    assert tool.parse_changes(raw)[0].path == "a\nfile"


@pytest.mark.parametrize(
    "raw",
    [
        b"bad\0path\0",
        b":000000 100644 x y A\0path\0",
        b":000000 100644 " + b"0" * 40 + b" " + b"a" * 40 + b" A\0",
        b":000000 100644 " + b"0" * 40 + b" " + b"a" * 40 + b" A\0\0",
        b":000000 100644 " + b"0" * 40 + b" " + b"a" * 40 + b" A\0path",
    ],
)
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
    # Room for a commit identifier, not for the one raw change the range adds.
    monkeypatch.setattr(tool, "MAX_METADATA_BYTES", 100)
    with pytest.raises(tool.MetadataError, match="too long for this gate") as refusal:
        tool.inventory(path, base)
    assert "not a commit" not in str(refusal.value)
    assert f"more than {100 / 1024**2:g} MiB" in str(refusal.value)


def test_content_past_the_gate_is_refused_before_it_is_read(
    repo: tuple[Path, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Sizing a blob means compressing it, so one check reads a bounded amount."""
    path, base = repo
    add(path, "one.bin", noise(64))
    add(path, "two.bin", noise(64, 1))
    commit(path)
    monkeypatch.setattr(tool, "MAX_CONTENT_BYTES", 127)

    def unread(*_arguments: object, **_options: object) -> object:
        raise AssertionError("content was read past the cap")

    monkeypatch.setattr(tool, "_ContentReader", unread)
    with pytest.raises(tool.MetadataError, match=r"more than the 0\.00 MiB this gate reads"):
        tool.inventory(path, base)
    monkeypatch.setattr(tool, "MAX_CONTENT_BYTES", 128)
    with pytest.raises(AssertionError, match="past the cap"):
        tool.inventory(path, base)


def test_one_deadline_bounds_the_whole_check(
    repo: tuple[Path, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """I2 of #406: grandfathering and the verdict run under the inventory's deadline."""
    path, base = repo
    add(path, "large.bin", noise(64))
    commit(path)
    blobs = tool.inventory(path, base)
    ceilings = tool.Ceilings(per_blob=PER, total=1024)
    spent = time.monotonic() - 1
    # The verdict alone needs no Git query, and it is still past the deadline.
    with pytest.raises(tool.MetadataError, match="exceeded its 30-second deadline"):
        tool.judge(path, base, [], ceilings, added=0, deadline=spent)
    with pytest.raises(tool.MetadataError, match="deadline"):
        tool.judge(path, base, blobs, ceilings, added=0, deadline=spent)
    with pytest.raises(tool.MetadataError, match="deadline"):
        tool.added_bytes(path, base, deadline=spent)
    with pytest.raises(tool.MetadataError, match="deadline"):
        tool.grandfathered(path, base, per_blob=PER, deadline=spent)
    raw = b"".join(
        b":000000 100644 " + b"0" * 40 + b" " + b"a" * 40 + b" A\0path-%d\0" % index
        for index in range(3)
    )
    monkeypatch.setattr(tool, "DEADLINE_STRIDE", 2)
    with pytest.raises(tool.MetadataError, match="deadline"):
        list(tool._changes(raw, spent))  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    seen: list[float] = []

    def record_inventory(
        *_arguments: object, deadline: float, **_options: object
    ) -> list[tool.Blob]:
        seen.append(deadline)
        return blobs

    def record_added(*_arguments: object, deadline: float, **_options: object) -> int:
        seen.append(deadline)
        return 0

    def record_judge(
        *_arguments: object, deadline: float, **_options: object
    ) -> tuple[dict[str, int], list[str]]:
        seen.append(deadline)
        return {}, []

    monkeypatch.setattr(tool, "inventory", record_inventory)
    monkeypatch.setattr(tool, "added_bytes", record_added)
    monkeypatch.setattr(tool, "judge", record_judge)
    monkeypatch.chdir(path)
    started = time.monotonic()
    assert tool.main(["--base", base]) == 0
    assert len(seen) == 3
    assert seen[0] == seen[1] == seen[2]
    assert started + tool.MAX_SECONDS <= seen[0] <= time.monotonic() + tool.MAX_SECONDS


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


def test_metadata_capture_feeds_batch_input_while_draining_output(
    repo: tuple[Path, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """C1: cat-file must drain output before its input fits in the pipe."""
    path, _ = repo
    identifier = git(path, "rev-parse", "HEAD:seed.txt").encode("ascii")
    requests = (identifier + b"\n") * 4096
    expected = (identifier + b" blob 4\nseed\n") * 4096
    monkeypatch.setattr(tool, "MAX_METADATA_BYTES", len(expected))
    assert (
        tool._git(  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
            path,
            "cat-file",
            "--batch",
            deadline=time.monotonic() + tool.MAX_SECONDS,
            data=requests,
        )
        == expected
    )


def test_a_streamed_content_read_runs_to_the_check_deadline(
    repo: tuple[Path, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """J3 of #406: only a metadata query is cut at MAX_QUERY_SECONDS.

    A content read's cost is the content it compresses, which MAX_CONTENT_BYTES bounds, so
    it runs to the check's own deadline; a long read is then rejected rather than refused.
    """
    path, _ = repo
    identifier = git(path, "rev-parse", "HEAD:seed.txt").encode("ascii")
    given: list[float] = []
    capture = tool._capture_git  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001

    def record(
        child: subprocess.Popen[bytes],
        *,
        deadline: float,
        data: bytes | None,
        sink: Callable[[bytes], None] | None = None,
    ) -> tuple[bytes, bytes]:
        given.append(deadline)
        return capture(child, deadline=deadline, data=data, sink=sink)

    monkeypatch.setattr(tool, "_capture_git", record)
    deadline = time.monotonic() + tool.MAX_QUERY_SECONDS + 600
    streamed = bytearray()
    for sink in (streamed.extend, None):
        tool._git(  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
            path,
            "cat-file",
            "--batch",
            deadline=deadline,
            data=identifier + b"\n",
            sink=sink,
        )
    assert bytes(streamed) == identifier + b" blob 4\nseed\n"
    assert given[0] == deadline
    assert given[1] <= time.monotonic() + tool.MAX_QUERY_SECONDS < deadline


@pytest.mark.parametrize(
    "data",
    [b"", b"x", noise(70_000), b"register: entry\n" * 20_000, noise(3000) * 40],
    ids=["empty", "one", "noise", "text", "repeated"],
)
def test_streamed_stored_size_is_the_unit_however_the_content_is_split(data: bytes) -> None:
    """The guard compresses each blob in read-sized pieces and must get OR-18's figure."""
    pieces = random.Random(len(data))
    for split in (1, 7, 4096, 65536, 0):
        measure = StoredSize(len(data))
        position = 0
        while position < len(data):
            step = split or pieces.randint(1, 100_000)
            measure.update(memoryview(data)[position : position + step])
            position += step
        assert measure.result() == stored(data)
    assert stored(data) <= stored_size_bound(len(data))


def mixed(size: int, seed: int) -> bytes:
    """Register-like text interleaved with incompressible runs, cut to `size` bytes."""
    draw = random.Random(seed)
    parts: list[bytes] = []
    length = 0
    while length < size:
        if draw.random() < 0.6:
            part = b"".join(
                b"- n: %d\n  side: %d\n" % (draw.randrange(10**6), draw.randrange(10**9))
                for _ in range(draw.randrange(1, 400))
            )
        else:
            part = draw.randbytes(draw.randrange(1, 3000))
        parts.append(part)
        length += len(part)
    return b"".join(parts)[:size]


# Recorded under the pinned interpreter's zlib 1.3.2. A memory level of 9 moves the three
# largest noise and mixed figures, and zlib-ng 2.2.5 moves the repeated and mixed ones.
GOLDEN_STORED = {
    "empty": 15,
    "noise-1": 16,
    "noise-4096": 4117,
    "noise-300000": 300_113,
    "repeated-16384": 88,
    "repeated-1048576": 2090,
    "mixed-65536": 33_057,
    "mixed-700000": 334_667,
}


def test_stored_size_is_pinned_to_recorded_figures() -> None:
    """J2 of #406: the figure depends on the zlib build, so a changed build fails here.

    Otherwise a different interpreter build, or a host whose zlib is zlib-ng, would move
    verdicts near a ceiling without any test failing.
    """
    corpus = {
        "empty": b"",
        "noise-1": noise(1, seed=1),
        "noise-4096": noise(4096, seed=2),
        "noise-300000": noise(300_000, seed=3),
        "repeated-16384": b"register: entry\n" * 1024,
        "repeated-1048576": b"register: entry\n" * 65536,
        "mixed-65536": mixed(65_536, seed=4),
        "mixed-700000": mixed(700_000, seed=5),
    }
    streamed: dict[str, int] = {}
    for name, data in corpus.items():
        pieces = random.Random(len(data))
        measure = StoredSize(len(data))
        position = 0
        while position < len(data):
            step = pieces.randint(1, 70_000)
            measure.update(memoryview(data)[position : position + step])
            position += step
        streamed[name] = measure.result()
    build = f"zlib {zlib.ZLIB_RUNTIME_VERSION}"
    assert {name: stored(data) for name, data in corpus.items()} == GOLDEN_STORED, build
    assert streamed == GOLDEN_STORED, build


def test_content_reader_streams_and_refuses_malformed_batch_output() -> None:
    identifier = b"a" * 40
    reader = tool._ContentReader([(identifier, 3)])  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    for byte in identifier + b" blob 3\nabc\n":
        reader.feed(bytes([byte]))
    assert reader.finish() == {identifier: (stored(b"abc"), False)}
    for output, message in [
        (identifier + b" missing\n", "missing or malformed"),
        (identifier + b" blob 4\nabcd\n", "missing or malformed"),
        (b"b" * 40 + b" blob 3\nabc\n", "missing or malformed"),
        (identifier + b" blob 3\nabcX", "truncated"),
        (identifier + b" blob 3\nabc\nextra", "unexpected trailing data"),
        (b"x" * (tool.MAX_HEADER_BYTES + 1), "missing or malformed"),
    ]:
        reader = tool._ContentReader([(identifier, 3)])  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
        with pytest.raises(tool.MetadataError, match=message):
            reader.feed(output)
    for output in (b"", identifier + b" blob 3\nab", identifier + b" blob 3\nabc"):
        reader = tool._ContentReader([(identifier, 3)])  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
        reader.feed(output)
        with pytest.raises(tool.MetadataError, match="truncated"):
            reader.finish()


def test_exact_byte_boundaries_and_one_byte_excess() -> None:
    first = tool.Blob("a", 8, ("one",), checkout=8)
    second = tool.Blob("b", 8, ("two",), checkout=8)
    assert tool.violations([first, second], per_blob=8, total=16, added=16) == []
    assert tool.violations(
        [tool.Blob("a", 9, ("one",), checkout=9)], per_blob=8, total=16, added=0
    )
    assert tool.violations([first, second], per_blob=8, total=16, added=17) == [
        total_failure(17, 16)
    ]
    # The total is the pack alone: the blobs' own sizes neither add to it nor offset it.
    assert tool.violations([first, second], per_blob=8, total=1, added=1) == []
    for added in (-1, True, 1.0):
        with pytest.raises(tool.MetadataError, match="added pack size"):
            tool.violations([], per_blob=8, total=8, added=cast("int", added))


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
        tool.violations([], per_blob=True, total=1, added=0)


def test_the_cli_measures_the_total_at_the_given_head(
    repo: tuple[Path, str],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """K3 of #406: CI checks out a synthetic merge and names the PR head with --head."""
    path, base = repo
    git(path, "checkout", "-qb", "feature")
    add(path, "dump.bin", noise(4096))
    commit(path)
    git(path, "checkout", "-q", "main")
    feature = pack_size(path, base, "feature")
    assert feature >= 4096
    assert tool.added_bytes(path, base) == 0
    monkeypatch.chdir(path)
    monkeypatch.setattr(
        tool, "load_ceilings", lambda: tool.Ceilings(per_blob=8192, total=feature - 1)
    )
    assert tool.main(["--base", base, "--head", "feature"]) == 1
    output = capsys.readouterr().out
    assert f"REJECT_ADDED_STORAGE: {total_failure(feature, feature - 1)}" in output
    monkeypatch.setattr(
        tool, "load_ceilings", lambda: tool.Ceilings(per_blob=8192, total=feature)
    )
    assert tool.main(["--base", base, "--head", "feature"]) == 0
    assert f"PASS: {feature} bytes added as a thin pack" in capsys.readouterr().out


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


def stored_just_over(limit: int, seed: int) -> bytes:
    """Incompressible content whose blob is the first size over `limit` as Git stores it.

    Over noise the compressed overhead is constant for long stretches, so one measurement
    of it places the length and two or three more confirm it.
    """
    pool = noise(limit, seed)
    length = 2 * limit - stored(pool)
    while stored(pool[:length]) > limit:
        length -= 1
    while stored(pool[:length]) <= limit:
        length += 1
    return pool[:length]


def test_production_ceiling_rejects_one_byte_over_through_the_cli(
    repo: tuple[Path, str],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Review A4: the shipped ceiling, a real blob just over it, exit 1 and the REJECT."""
    path, base = repo
    ceilings = tool.load_ceilings()
    dump = stored_just_over(ceilings.per_blob, 4)
    add(path, "dump.bin", dump)
    commit(path)
    object_id = git(path, "rev-parse", "HEAD:dump.bin")
    monkeypatch.chdir(path)
    assert tool.main(["--base", base]) == 1
    output = capsys.readouterr().out
    assert stored(dump) - ceilings.per_blob <= 5
    assert (
        f"REJECT_ADDED_STORAGE: {stored(dump)} bytes exceeds {ceilings.per_blob} as Git "
        f"stores them: ('dump.bin',) ({object_id}, {len(dump)} bytes in a checkout)"
    ) in output
    assert "PASS" not in output


def test_production_grandfathering_reports_and_passes_through_the_cli(
    repo: tuple[Path, str],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    path, _ = repo
    ceilings = tool.load_ceilings()
    add(path, "atlas.svg", noise(ceilings.per_blob, 5))
    base = commit(path)
    rewrite = noise(ceilings.per_blob, 6)
    add(path, "atlas.svg", rewrite)
    commit(path)
    monkeypatch.chdir(path)
    assert tool.main(["--base", base]) == 0
    output = capsys.readouterr().out
    assert "GRANDFATHERED:" in output
    assert "('atlas.svg',)" in output
    added = pack_size(path, base)
    assert len(rewrite) <= added < ceilings.total
    assert (
        f"PASS: {added} bytes added as a thin pack; 1 unique checked blobs, 1 new versions "
        f"({len(rewrite)} bytes in a checkout)"
    ) in output


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
    add(path, "dump.bin", noise(2048))
    commit(path)
    git(path, "checkout", "-q", "main")
    rejected = merge(path, "dump", 7)
    git(path, "checkout", "-qb", "small")
    for name in ("a.txt", "b.txt", "c.txt"):
        add(path, name, name.encode())
    commit(path)
    git(path, "checkout", "-q", "main")
    passed = merge(path, "small", 8)
    # Fewer blobs and a larger pack, so the largest pass is chosen by the pack alone.
    git(path, "checkout", "-qb", "medium")
    add(path, "medium.bin", noise(900))
    commit(path)
    git(path, "checkout", "-q", "main")
    largest = merge(path, "medium", 9)
    ceilings = tool.Ceilings(per_blob=1024, total=16384)
    rows = tool.census(path, "main", 5, ceilings=ceilings)
    assert [(row.merge, bool(row.failures), row.refusal) for row in rows] == [
        (largest, False, ""),
        (passed, False, ""),
        (rejected, True, ""),
    ]
    assert [row.added for row in rows] == [
        pack_size(path, f"{merge}^1", f"{merge}^2") for merge in (largest, passed, rejected)
    ]
    assert rows[0].added > rows[1].added
    assert len(rows[0].blobs) < len(rows[1].blobs)
    tool.print_census(rows, "main", ceilings)
    output = capsys.readouterr().out
    assert (
        f"{passed[:9]} #8 pass: 0.00 MiB added as a thin pack; 3 blobs checked, 3 new versions"
    ) in output
    assert f"{rejected[:9]} #7 REJECT: 0.00 MiB added as a thin pack; 1 blobs checked" in output
    assert (
        "SUMMARY: 1 of 3 merges rejected, 0 of them by the total alone; 0 guard refusals; "
        f"largest passing total 0.00 MiB ({largest[:9]} #9)"
    ) in output


def test_census_gives_each_replay_a_deadline_of_its_own(
    repo: tuple[Path, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """J3 of #406: each replay has a pull request's deadline, not what the census has left.

    One deadline over the whole census would refuse every replay after the first 30 s, and
    the census over all of main's merges takes minutes.
    """
    path, _ = repo
    for number in (1, 2, 3):
        git(path, "checkout", "-qb", f"pr-{number}")
        add(path, f"pr-{number}.txt", b"%d" % number)
        commit(path)
        git(path, "checkout", "-q", "main")
        merge(path, f"pr-{number}", number)
    issued: list[float] = []
    given: list[float] = []
    fresh = tool._deadline  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    inventory = tool.inventory

    def issue() -> float:
        issued.append(fresh())
        return issued[-1]

    def record(*arguments: Any, deadline: float, **options: Any) -> list[tool.Blob]:
        given.append(deadline)
        return inventory(*arguments, deadline=deadline, **options)

    monkeypatch.setattr(tool, "_deadline", issue)
    monkeypatch.setattr(tool, "inventory", record)
    rows = tool.census(path, "main", 5, ceilings=tool.Ceilings(per_blob=PER, total=1024))
    assert [row.refusal for row in rows] == ["", "", ""]
    # One for the census's own queries, then one for each replay.
    assert len(issued) == len(rows) + 1
    assert given == issued[1:]


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
    # I2 of #406 (OR-17): the step has a wall ceiling of its own, above the guard's deadline.
    assert gate["timeout-minutes"] == 1
    assert gate["timeout-minutes"] * 60 >= 2 * tool.MAX_SECONDS
    assert steps.index(gate) < next(
        index
        for index, step in enumerate(steps)
        if step.get("name") == "Run the required pull-request checks"
    )
