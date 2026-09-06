"""Failure-path contracts for isolated mutation-control subprocesses."""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

from devtools.run_negative_controls import (
    BUILD_CACHES,
    HERE,
    PRUNE,
    ROOT,
    SNAPSHOT_MAX_BYTES,
    clone_tree,
    resolve_control_target,
    result_pruned_targets,
    run_control_command,
    snapshot_source_bytes,
)

# A size no accident produces, so a byte that moves the count can be attributed.
CACHE_PROBE_BYTES = b"n" * 1_000_003
# One temporary directory under `packing/`, where the walk counts it, holding a file
# the count must see and four caches it must not. Removed in `finally`, and named so a
# leftover from a killed run says what it was.
CACHE_PROBE_ROOT = ROOT / ".negative-control-cache-probe"
# Spelled out rather than derived from `BUILD_CACHES`, which would make the test move
# with the thing it checks: a name dropped from the set would simply stop being planted,
# and this would go on passing over an exclusion that no longer existed. Written
# literally, that same edit leaves a probe planted where the walk can see it and the
# byte assertion below fails. The other direction is covered by the containment check
# in the test, so a fourth cache kind cannot join the set unprobed.
CACHE_PROBE_DIRECTORIES = (
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "one/two/three/__pycache__",
)


def test_generator_owned_prospective_outputs_stay_out_of_mutation_snapshots() -> None:
    assert ROOT / "atlas/prospective/rendering" in PRUNE
    assert ROOT / "witnesses/prospective" in PRUNE
    assert ROOT / "atlas/known-best/rendering" in PRUNE
    assert ROOT / "atlas/known-best/contact-overlays" in PRUNE
    assert snapshot_source_bytes() < SNAPSHOT_MAX_BYTES


@pytest.mark.slow
def test_build_caches_leave_the_counted_surface_and_the_worker_trees(
    tmp_path: Path,
) -> None:
    """Bytecode and tool state move neither the guard's number nor a worker tree.

    The regression is D-422, and the number alone does not show its shape: the gate
    runs pytest, pytest writes `__pycache__` into the very tree the gate is measuring,
    and a later step of that same run fails the assertion above on 12 MB that no commit
    contains. Hosted CI went red on every pull request that way, on trees that pass the
    cap from a fresh clone. So what is asserted here is the property that closes it --
    the count is a fact about the commit and not about what has been run in the
    checkout -- rather than that the count happens to be small today.

    The non-cache probe is the other half, and the half that keeps this honest. An
    exclusion drawn too wide would satisfy "caches are not counted" trivially, by
    counting nothing, so the same measurement pins one ordinary file's bytes to the
    total exactly. The caches are planted at four depths for the same reason: the real
    ones sit two to five levels down, in `tests/`, `cases/`, `devtools/` and `src/`, and
    a rule that only looked at the top level would have missed almost all of them while
    still passing a shallower version of this test.
    """
    assert {Path(name).name for name in CACHE_PROBE_DIRECTORIES} >= BUILD_CACHES

    shutil.rmtree(CACHE_PROBE_ROOT, ignore_errors=True)
    caches = [CACHE_PROBE_ROOT / name / "probe.bin" for name in CACHE_PROBE_DIRECTORIES]
    counted = CACHE_PROBE_ROOT / "counted.bin"

    before = snapshot_source_bytes()
    try:
        for probe in (*caches, counted):
            probe.parent.mkdir(parents=True, exist_ok=True)
            probe.write_bytes(CACHE_PROBE_BYTES)

        assert snapshot_source_bytes() == before + len(CACHE_PROBE_BYTES)

        tree = tmp_path / "snapshot"
        clone_tree(tree)
    finally:
        shutil.rmtree(CACHE_PROBE_ROOT, ignore_errors=True)

    # The whole worker tree, not just the probe: the point of the sweep in `clone_tree`
    # is that no cache reaches a worker from any of its three copiers. `os.walk` does
    # not follow symlinks, so the linked-back `.venv` is correctly out of scope.
    surviving = [
        str(Path(parent, name).relative_to(tree))
        for parent, names, _files in os.walk(tree)
        for name in names
        if name in BUILD_CACHES
    ]
    assert surviving == []
    assert (tree / HERE / counted.relative_to(ROOT)).is_file()


def test_results_register_dependencies_survive_snapshot_pruning() -> None:
    retained = {path.relative_to(ROOT).as_posix() for path in result_pruned_targets()}
    assert "resources/papers/bentz-2010-optimal-packings-13-and-46.md" in retained
    assert "resources/papers/nagamochi-2005-packing-unit-squares-in-a-rectangle.pdf" in retained


def test_unmutated_results_checker_is_green_inside_a_worker(tmp_path: Path) -> None:
    tree = tmp_path / "snapshot"
    clone_tree(tree)
    completed = subprocess.run(
        [sys.executable, "-m", "devtools.check_results"],
        cwd=tree / "packing",
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_control_targets_cannot_escape_the_private_snapshot(tmp_path: Path) -> None:
    tree = tmp_path / "snapshot"
    work = tree / "explorations" / "packing"
    work.mkdir(parents=True)
    repository_file = tree / ".flowmarkignore"
    repository_file.write_text("inside", encoding="utf-8")
    outside = tmp_path / "outside.txt"
    outside.write_text("outside", encoding="utf-8")
    (work / "outside-link").symlink_to(outside)

    assert resolve_control_target("../../.flowmarkignore", tree=tree, work=work) == (
        repository_file
    )

    for escaped in (str(outside), "../../../outside.txt", "outside-link"):
        with pytest.raises(ValueError, match="escapes private snapshot"):
            resolve_control_target(escaped, tree=tree, work=work)

    with pytest.raises(ValueError, match="not a regular file"):
        resolve_control_target("../..", tree=tree, work=work)


def test_timeout_reaps_a_child_that_ignores_termination() -> None:
    command = shlex.join(
        [
            sys.executable,
            "-c",
            (
                "import signal, time; "
                "signal.signal(signal.SIGTERM, signal.SIG_IGN); "
                "time.sleep(60)"
            ),
        ]
    )
    started = time.monotonic()

    outcome = run_control_command(
        command,
        timeout_seconds=0.05,
        termination_grace_seconds=0.05,
    )

    assert outcome.timed_out is True
    assert outcome.returncode != 0
    assert time.monotonic() - started < 1.0
