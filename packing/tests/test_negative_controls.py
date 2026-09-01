"""Failure-path contracts for isolated mutation-control subprocesses."""

from __future__ import annotations

import shlex
import subprocess
import sys
import time
from pathlib import Path

import pytest

from devtools.run_negative_controls import (
    PRUNE,
    ROOT,
    SNAPSHOT_MAX_BYTES,
    clone_tree,
    resolve_control_target,
    result_pruned_targets,
    run_control_command,
    snapshot_source_bytes,
)


def test_generator_owned_prospective_outputs_stay_out_of_mutation_snapshots() -> None:
    assert ROOT / "atlas/prospective/rendering" in PRUNE
    assert ROOT / "witnesses/prospective" in PRUNE
    assert ROOT / "atlas/known-best/rendering" in PRUNE
    assert ROOT / "atlas/known-best/contact-overlays" in PRUNE
    assert snapshot_source_bytes() < SNAPSHOT_MAX_BYTES


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
