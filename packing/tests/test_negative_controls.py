"""Failure-path contracts for isolated mutation-control subprocesses."""

from __future__ import annotations

import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from devtools import run_negative_controls as controls
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


def test_oversized_snapshot_is_refused_before_cloning(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    spec = tmp_path / "controls.yaml"
    spec.write_text("controls:\n- name: selected\n")
    monkeypatch.setattr(
        controls, "snapshot_source_bytes", lambda: controls.SNAPSHOT_MAX_BYTES + 1
    )
    monkeypatch.setattr(
        controls, "clone_tree", lambda _tree: pytest.fail("oversized snapshot was cloned")
    )
    assert controls.main([str(spec), "-j", "1"]) == 1
    assert f"cap is {controls.SNAPSHOT_MAX_BYTES}" in capsys.readouterr().err


def test_control_timing_records_preserve_failed_detection_and_refuse_overwrite(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    spec = tmp_path / "controls.yaml"
    spec.write_text("controls:\n- name: detects mutation\n- name: misses mutation\n")
    timings = tmp_path / "timings.jsonl"
    monkeypatch.setattr(controls, "snapshot_source_bytes", lambda: 0)
    monkeypatch.setattr(controls, "clone_tree", lambda tree: tree.mkdir(parents=True))
    monkeypatch.setattr(
        controls,
        "run_one",
        lambda control, _tree: (
            control["name"] == "detects mutation",
            ""
            if control["name"] == "detects mutation"
            else "command SUCCEEDED; the check did not fire",
        ),
    )
    assert controls.main([str(spec), "-j", "1", "--timings", str(timings)]) == 1
    captured = capsys.readouterr()
    assert "CONTROL FAILED  misses mutation" in captured.err
    assert "slowest negative controls" in captured.out
    records = [json.loads(line) for line in timings.read_text().splitlines()]
    results = [record for record in records if record["event"] == "control_finished"]
    assert {record["name"]: record["status"] for record in results} == {
        "detects mutation": "passed",
        "misses mutation": "failed",
    }
    assert all(record["wall_seconds"] >= 0 for record in results)
    assert records[0]["selected_controls"] == ["detects mutation", "misses mutation"]
    assert records[-1]["status"] == "failed"
    original = timings.read_bytes()
    assert controls.main([str(spec), "-j", "1", "--timings", str(timings)]) == 1
    assert "refuses to overwrite" in capsys.readouterr().err
    assert timings.read_bytes() == original


def test_a_failed_start_record_returns_the_private_worker_tree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """One control makes a leaked tree observable without leaving another thread blocked."""
    spec = tmp_path / "controls.yaml"
    spec.write_text("controls:\n- name: journal failure\n")
    timings = tmp_path / "timings.jsonl"
    available = controls.queue.Queue()
    monkeypatch.setattr(controls.queue, "Queue", lambda: available)
    monkeypatch.setattr(controls, "snapshot_source_bytes", lambda: 0)
    monkeypatch.setattr(controls, "clone_tree", lambda tree: tree.mkdir(parents=True))
    monkeypatch.setattr(controls, "run_one", lambda *_args: pytest.fail("control was run"))
    original_open = Path.open
    writes = 0

    def fail_start_record(path, mode="r", *args, **kwargs):
        nonlocal writes
        if path == timings and mode == "a":
            writes += 1
            if writes == 3:
                raise OSError("journal storage failed")
        return original_open(path, mode, *args, **kwargs)

    monkeypatch.setattr(Path, "open", fail_start_record)
    with pytest.raises(OSError, match="journal storage failed"):
        controls.main([str(spec), "-j", "1", "--timings", str(timings)])
    assert available.qsize() == 1, "the journal failure leaked the private worker tree"


def test_artifact_directory_creates_unique_control_journals(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = tmp_path / "controls.yaml"
    spec.write_text("controls:\n- name: selected\n  run: python -m checker\n- name: omitted\n")
    artifact_directory = tmp_path / "artifacts"
    monkeypatch.setenv("PACKING_VALIDATION_ARTIFACT_DIR", str(artifact_directory))
    monkeypatch.setattr(controls, "snapshot_source_bytes", lambda: 0)
    monkeypatch.setattr(controls, "clone_tree", lambda tree: tree.mkdir(parents=True))
    monkeypatch.setattr(controls, "run_one", lambda *_args: (True, ""))
    monkeypatch.setattr(controls, "timing_provenance", lambda: {"source_revision": "control"})
    for _ in range(2):
        assert controls.main([str(spec), "-j", "1", "-k", "selected"]) == 0
    journals = list(artifact_directory.glob("negative-controls-*.jsonl"))
    assert len(journals) == 2
    for journal in journals:
        records = [json.loads(line) for line in journal.read_text().splitlines()]
        assert records[0]["selected_commands"] == [
            {"name": "selected", "run": "python -m checker"}
        ]
        assert records[0]["source_revision"] == "control"
        assert records[0]["workers"] == 1
        assert records[0]["journal"] == str(journal)
        assert records[-1]["completed"] == 1
        assert all(
            datetime.fromisoformat(record["at"]).utcoffset() == timedelta(0)
            for record in records
        )
    explicit = tmp_path / "explicit.jsonl"
    assert (
        controls.main([str(spec), "-j", "1", "-k", "selected", "--timings", str(explicit)]) == 0
    )
    assert explicit.exists()
    assert len(list(artifact_directory.glob("negative-controls-*.jsonl"))) == 2


def test_mutation_children_do_not_inherit_parent_artifact_capture(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = tmp_path / "controls.yaml"
    spec.write_text(
        "controls:\n- name: nested gate\n  file: probe.txt\n"
        "  replace: [original, mutated]\n  run: packing-validate\n  expect: refused\n"
    )
    artifacts = tmp_path / "artifacts"
    monkeypatch.setenv("PACKING_VALIDATION_ARTIFACT_DIR", str(artifacts))
    monkeypatch.setattr(controls, "snapshot_source_bytes", lambda: 0)
    monkeypatch.setattr(controls, "timing_provenance", dict)

    def clone(tree: Path) -> None:
        work = tree / HERE
        work.mkdir(parents=True)
        (work / "probe.txt").write_text("original")

    def command(_command: str, **kwargs: object) -> controls.CommandOutcome:
        environment = kwargs["environment"]
        assert isinstance(environment, dict)
        assert "PACKING_VALIDATION_ARTIFACT_DIR" not in environment
        return controls.CommandOutcome(returncode=1, stdout="refused", stderr="")

    monkeypatch.setattr(controls, "clone_tree", clone)
    monkeypatch.setattr(controls, "run_control_command", command)
    assert controls.main([str(spec), "-j", "1"]) == 0
    assert os.environ["PACKING_VALIDATION_ARTIFACT_DIR"] == str(artifacts)
    journals = list(artifacts.glob("negative-controls-*.jsonl"))
    assert len(journals) == 1
    records = [json.loads(line) for line in journals[0].read_text().splitlines()]
    assert records[-1]["completed"] == 1


def test_controltiming_provenance_binds_dirty_and_untracked_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(controls, "REPO", tmp_path)
    monkeypatch.setattr(controls, "ROOT", tmp_path)
    monkeypatch.setenv("PACK_JOBS", "2")
    (tmp_path / "uv.lock").write_bytes(b"locked toolchain")
    untracked = tmp_path / "new.py"
    untracked.write_bytes(b"first version")
    outputs = {
        ("rev-parse", "HEAD"): b"source-commit\n",
        ("diff", "--binary", "HEAD", "--"): b"tracked source delta",
        ("ls-files", "--others", "--exclude-standard", "-z"): b"new.py\0",
    }

    def git_result(command, **_kwargs):
        return subprocess.CompletedProcess(command, 0, outputs[tuple(command[1:])], b"")

    monkeypatch.setattr(controls.subprocess, "run", git_result)
    first = controls.timing_provenance()
    assert first["source_revision"] == "source-commit"
    assert first["tracked_dirty"] is True
    assert first["dirty_diff_sha256"] == hashlib.sha256(b"tracked source delta").hexdigest()
    assert first["uv_lock_sha256"] == hashlib.sha256(b"locked toolchain").hexdigest()
    environment = first["worker_environment"]
    assert isinstance(environment, dict)
    assert environment["PACK_JOBS"] == "2"
    assert first["python_executable"] == sys.executable
    untracked.write_bytes(b"changed version")
    second = controls.timing_provenance()
    assert first["untracked_sha256"] != second["untracked_sha256"]


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
    assert (
        ROOT
        / "campaign/series/series-000-smoke-and-calibration/results"
        / "bc-200-state-191-50.json"
        in PRUNE
    )
    assert ROOT / "campaign/series/series-000-smoke-and-calibration/results/agenda-025" in PRUNE
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
