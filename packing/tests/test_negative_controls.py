"""Failure-path contracts for isolated mutation-control subprocesses."""

from __future__ import annotations

import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from devtools import run_negative_controls as controls
from devtools.check_readme import NO_INDEX
from devtools.repo_scope import tracked_files
from devtools.retained_data import read_retained_bytes
from devtools.run_negative_controls import (
    BUILD_CACHES,
    COPY_SEPARATELY,
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
from sqpack.yamlio import safe_load

MOTION_LAB_GOLDEN = ROOT / "tests/golden/motion-lab-pages.json"
COMPOSITE_VECTORS = frozenset(
    ROOT / "atlas/known-best" / name
    for name in ("known-best-1-100.svg", "known-best-1-324.svg")
)
SESSION163_PUSH_LOGS = frozenset(
    ROOT / "campaign/agent-sessions" / name
    for name in (
        "session-163-push-recovery.log",
        "session-163-push-refinement.log",
        "session-163-push-final.log",
    )
)
HISTORICAL_DIAGNOSTIC_OUTPUTS = frozenset(
    ROOT / relative
    for relative in (
        "campaign/explorations/X048-session-177-cached-collision/receipts/profile-packet.json",
        "campaign/series/series-000-smoke-and-calibration/results/bc-201-n11-tight-cell-census.json",
    )
)
#: The 2026-10-06 breach's answer (PR #382): receipt roots traced as no control's input.
RETAINED_RECEIPT_ROOTS = frozenset(
    ROOT / relative
    for relative in (
        "benchmarks/gate-cost-at-324/runs",
        "benchmarks/measure-verifier/census",
        "benchmarks/measure-verifier/census-mixed",
        "benchmarks/measure-verifier/review-2026-10-03-attack",
        "witnesses/franciscouzo-2026-10-03",
    )
)


@pytest.fixture(scope="module")
def control_snapshot(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, set[Path]]:
    """Reuse one real worker snapshot; each mutation restores its target in `finally`."""
    tree = tmp_path_factory.mktemp("control-snapshot") / "snapshot"
    retained: list[Path] = []
    select = controls.snapshot_pruned_targets

    def capture_targets() -> list[Path]:
        targets = select()
        retained.extend(targets)
        return targets

    # Keep the copier's actual selection for the workflow assertion instead of walking
    # and parsing every campaign document and results record a second time in the test.
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(controls, "snapshot_pruned_targets", capture_targets)
        clone_tree(tree)
    copied_targets = {path.relative_to(controls.REPO) for path in retained}
    return tree, copied_targets


def test_historical_validation_prunes_preserve_replay_inputs(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    """Telemetry can leave a worker; linked evidence and ordinary fixtures cannot."""
    tree, copied_targets = control_snapshot
    roots = (
        ROOT / "benchmarks/validation-efficiency/runs",
        ROOT / "benchmarks/validation-efficiency/checkpoints",
        ROOT / "campaign/agent-sessions/session-152-validation",
    )
    assert set(roots) <= PRUNE
    rescued = (
        "benchmarks/validation-efficiency/checkpoints/2026-09-06-integrated-fast.log",
        "benchmarks/validation-efficiency/checkpoints/2026-09-06-integrated-fast.manifest.json",
        "benchmarks/validation-efficiency/checkpoints/2026-09-06-integrated-fast.tar.gz",
        "benchmarks/validation-efficiency/checkpoints/2026-09-06-pre-main-integration.manifest.json",
        "benchmarks/validation-efficiency/checkpoints/2026-09-06-pre-main-integration.tar.gz",
        "benchmarks/validation-efficiency/checkpoints/VE-004-full-ed595fb6.tar.gz",
        "benchmarks/validation-efficiency/runs/instrument-v1.py.txt",
        "campaign/agent-sessions/session-152-validation/pdf-d490-run-35784981711-reference.pdf",
        "campaign/agent-sessions/session-152-validation/pdf-d490-run-35784981711-replay.pdf",
        "campaign/agent-sessions/session-152-validation/pdf-d490-run-35784981711-report.txt",
        "campaign/agent-sessions/session-152-validation/pdf-d490-run-35784981711.md",
    )
    for relative in rescued:
        source = ROOT / relative
        assert source.relative_to(controls.REPO) in copied_targets, relative
        assert (tree / HERE / relative).read_bytes() == source.read_bytes(), relative
    # The normal legacy-manifest fixture test still has both its code and the two
    # manifest/archive pairs it reads. The schema checker and current witness remain
    # on the source surface too; the telemetry exclusion cannot hide their controls.
    for relative in (
        "devtools/checkpoint_manifest.py",
        "tests/test_checkpoint_manifest.py",
        "devtools/validate_schemas.py",
        "witnesses/known-best/n-123.yaml",
    ):
        assert (tree / HERE / relative).read_bytes() == (ROOT / relative).read_bytes()
    # One unconsumed generated artifact from each root must actually leave the
    # finished worker. Merely listing the roots while copying everything back would
    # preserve the cap breach and satisfy only the structural assertion above.
    for relative in (
        "benchmarks/validation-efficiency/runs/e865612fe81c4d96a7b3713b28191045.stdout.log",
        "benchmarks/validation-efficiency/checkpoints/VE-004-control-1.tar.gz",
        "campaign/agent-sessions/session-152-validation/validation-timings-exhaustive-1.zip",
    ):
        assert (ROOT / relative).is_file(), relative
        assert not (tree / HERE / relative).exists(), relative


def test_historical_push_logs_leave_workers_but_keep_scientific_consumers(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    """Exclude only unconsumed telemetry; the finished indexed worker retains inputs."""
    tree, copied_targets = control_snapshot
    logs = (
        "session-164-push-initial.log",
        "session-153-integrated-push.log",
        "session-163-push-recovery.log",
        "session-163-push-refinement.log",
        "session-163-push-final.log",
    )
    for name in logs:
        source = ROOT / "campaign/agent-sessions" / name
        assert source in PRUNE
        assert source.is_file()
        assert source.relative_to(controls.REPO) not in copied_targets
        assert not (tree / HERE / "campaign/agent-sessions" / name).exists()
    for relative in (
        "campaign/agent-sessions/session-164-efficiency-push.log.gz",
        "campaign/agent-sessions/session-164-push-final.log.gz",
        "campaign/agent-sessions/session-153-native-full.json",
        "campaign/agent-sessions/session-153-native-full.rows.jsonl",
        "frontier/results.yaml",
        "frontier/evidence.yaml",
        "witnesses/known-best/n-263.yaml",
        "devtools/check_results.py",
        "devtools/squish_second_update_packets.py",
    ):
        source = ROOT / relative
        assert (tree / HERE / relative).read_bytes() == source.read_bytes(), relative
        assert tree / HERE / relative in (tracked_files(tree, "packing") or []), relative
        if relative.endswith(".log.gz"):
            assert read_retained_bytes(tree / HERE / relative) == read_retained_bytes(source)
            assert not (tree / HERE / relative.removesuffix(".gz")).exists()
    assert snapshot_source_bytes() < SNAPSHOT_MAX_BYTES


def test_historical_site_snapshot_outputs_leave_workers_after_dependency_rescue(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    """The bounded C8 prune removes outputs while preserving real consumer inputs."""
    tree, copied_targets = control_snapshot
    assert controls.HISTORICAL_SNAPSHOT_OUTPUTS <= PRUNE
    rescued = (
        "campaign/explorations/X049-families-data/regularized/run.txt",
        "campaign/explorations/X049-families-data/regularized/shades.txt",
        "campaign/series/series-000-smoke-and-calibration/results/agenda-030/pr127-checkpoint/README.md",
        "campaign/series/series-000-smoke-and-calibration/results/agenda-030/pr127-checkpoint/full-ef8a2e72.txt",
        "campaign/series/series-000-smoke-and-calibration/results/agenda-030/pr127-checkpoint/fast-cbe9fd76.txt",
        "campaign/series/series-000-smoke-and-calibration/results/agenda-030/pr127-checkpoint/slow-cbe9fd76.txt",
        "campaign/series/series-000-smoke-and-calibration/results/agenda-030/pr127-checkpoint/negative-cbe9fd76.txt",
    )
    for relative in rescued:
        source = ROOT / relative
        assert source.relative_to(controls.REPO) in copied_targets
        assert (tree / HERE / relative).read_bytes() == source.read_bytes()
    omitted = (
        "benchmarks/results/reachable-walker-2026-09-30/comparison.json",
        "campaign/agent-sessions/session-105-validation/fast-final-bdc28e89.json",
        "campaign/agent-sessions/session-105-validation/push-0e766bfd.json",
        "campaign/explorations/X048-session-177-cached-collision/receipts/profile-packet.json",
        "campaign/explorations/X048-session-178-full-core-ablation/receipts/endpoint-packet.json",
        "campaign/explorations/X049-families-data/regularized/n-268-regularized.yaml.gz",
        "campaign/series/series-000-smoke-and-calibration/results/agenda-030/pr127-checkpoint/slow-cbe9fd76/step-21ffbec363bd41dfa16a9e479105c249.json",
    )
    spec = safe_load((ROOT / "devtools/controls.yaml").read_text())
    for relative in omitted:
        source = ROOT / relative
        assert source.is_file(), "evidence must remain in the source checkout"
        assert source.relative_to(controls.REPO) not in copied_targets
        assert not (tree / HERE / relative).exists()
        for control in spec["controls"]:
            assert (ROOT / control["file"]).resolve() != source
            assert relative not in control["run"]
    for relative in (
        "campaign/agent-sessions/session-105-validation/fast-final-bdc28e89-source.json",
        "campaign/agent-sessions/session-105-validation/push-0e766bfd-source.json",
        "campaign/explorations/X048-session-177-cached-collision/receipts/J-fixed-tuple-certificate.json",
        "campaign/explorations/X048-session-178-full-core-ablation/receipts/B-ablation-packet.json",
        "campaign/explorations/X049-families-data/family-census.json",
        "campaign/explorations/X049-families-data/contact-shade-census.json",
        "atlas/known-best/regularized/index.json",
        "witnesses/known-best/n-268.yaml",
        "devtools/probe_n17_cached_collision.py",
        "devtools/probe_n17_full_core_ablation.py",
        "devtools/regularize_axis_components.py",
    ):
        assert (tree / HERE / relative).read_bytes() == (ROOT / relative).read_bytes()
    assert SNAPSHOT_MAX_BYTES == 192 * 1024 * 1024
    assert snapshot_source_bytes() < SNAPSHOT_MAX_BYTES


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
CORNER_DUAL_SALVAGE_RECEIPT = (
    ROOT
    / "campaign/series/series-000-smoke-and-calibration/results/agenda-032"
    / "exp-137-corner-dual-salvage.json.gz"
)
# The historical live-checkout location remains a guard: the test uses this relative
# path only inside its private worker snapshot, then asserts no concurrent test planted
# it under the real `packing/` root. Its name also makes a killed private run legible.
CACHE_PROBE_ROOT = ROOT / ".negative-control-cache-probe"
# Spelled out rather than derived from `BUILD_CACHES`, which would make the test move
# with the thing it checks: a name dropped from the set would simply stop being planted,
# and this would go on passing over an exclusion that no longer existed. Written
# literally, that same edit leaves a probe planted where the walk can see it and the
# byte assertion below fails. The other direction is covered by the containment check
# in the test, so a fourth cache kind cannot join the set unprobed.
CACHE_PROBE_DIRECTORIES = (
    "node_modules",
    "nested/dist",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "one/two/three/__pycache__",
)


def test_pruned_ancestry_matches_path_semantics(tmp_path: Path) -> None:
    roots = frozenset((tmp_path / "archive", tmp_path / "receipt.json"))
    for path in (
        tmp_path,
        tmp_path / "archive",
        tmp_path / "archive" / "nested" / "input.json",
        tmp_path / "archive-backup" / "input.json",
        tmp_path / "receipt.json",
        tmp_path / "receipt.json.backup",
    ):
        expected = any(path.is_relative_to(root) for root in roots)
        assert controls.in_pruned_roots(path, roots) == expected
        assert not controls.in_pruned_roots(path, frozenset())


def test_generator_owned_prospective_outputs_stay_out_of_mutation_snapshots() -> None:
    assert ROOT / "atlas/prospective/rendering" in PRUNE
    assert ROOT / "witnesses/prospective" in PRUNE
    assert ROOT / "atlas/known-best/rendering" in PRUNE
    assert ROOT / "atlas/known-best/contact-overlays" in PRUNE
    assert COMPOSITE_VECTORS <= PRUNE
    assert MOTION_LAB_GOLDEN in PRUNE
    assert (
        ROOT
        / "campaign/series/series-000-smoke-and-calibration/results"
        / "bc-200-state-191-50.json"
        in PRUNE
    )
    assert ROOT / "campaign/series/series-000-smoke-and-calibration/results/agenda-025" in PRUNE
    output_roots = {
        ROOT / "campaign/series/series-000-smoke-and-calibration/results" / name
        for name in (
            "agenda-031",
            "agenda-033",
            "agenda-034",
            "agenda-035",
            "agenda-041",
            "exp-201-arm-calibration",
            "exp-202-round-1",
        )
    }
    assert output_roots <= PRUNE
    assert CORNER_DUAL_SALVAGE_RECEIPT in PRUNE
    assert RETAINED_RECEIPT_ROOTS <= PRUNE
    assert controls.REGULARIZED_WITNESSES <= PRUNE
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())
    assert all(
        (ROOT / control["file"]).resolve() not in controls.REGULARIZED_WITNESSES
        for control in specification["controls"]
    )
    assert all(
        "atlas/known-best/regularized/n-" not in control["run"]
        for control in specification["controls"]
    )
    assert snapshot_source_bytes() < SNAPSHOT_MAX_BYTES


def test_n32_inventory_stays_in_repo_but_out_of_mutation_workers(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    tree, copied_targets = control_snapshot
    inventory = (
        ROOT
        / "campaign/series/series-000-smoke-and-calibration/results/agenda-040"
        / "one-spare-inventory-n32.json"
    )
    relative = inventory.relative_to(controls.REPO)
    packing_relative = inventory.relative_to(ROOT).as_posix()
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())

    assert inventory.is_file()
    assert inventory in PRUNE
    assert all(
        (ROOT / control["file"]).resolve() != inventory
        and packing_relative not in control["run"]
        for control in specification["controls"]
    )
    assert relative not in copied_targets
    assert not (tree / relative).exists()
    # The agenda is not removed wholesale; other checks use its retained files.
    family = inventory.with_name("exp-214-n13-399-100-family.json")
    assert (tree / family.relative_to(controls.REPO)).read_bytes() == family.read_bytes()


def test_motion_lab_golden_is_not_a_mutation_worker_input(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    tree, copied_targets = control_snapshot
    relative = MOTION_LAB_GOLDEN.relative_to(controls.REPO)
    packing_relative = MOTION_LAB_GOLDEN.relative_to(ROOT).as_posix()
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())

    assert MOTION_LAB_GOLDEN.is_file()
    assert all(
        (ROOT / control["file"]).resolve() != MOTION_LAB_GOLDEN
        for control in specification["controls"]
    )
    assert all(packing_relative not in control["run"] for control in specification["controls"])
    assert relative not in copied_targets
    assert not (tree / relative).exists()


def test_dual_salvage_receipt_is_not_a_mutation_worker_input(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    tree, copied_targets = control_snapshot
    relative = CORNER_DUAL_SALVAGE_RECEIPT.relative_to(controls.REPO)
    packing_relative = CORNER_DUAL_SALVAGE_RECEIPT.relative_to(ROOT).as_posix()
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())

    assert CORNER_DUAL_SALVAGE_RECEIPT.is_file()
    assert all(
        (ROOT / control["file"]).resolve() != CORNER_DUAL_SALVAGE_RECEIPT
        for control in specification["controls"]
    )
    assert all(packing_relative not in control["run"] for control in specification["controls"])
    assert relative not in copied_targets
    assert not (tree / relative).exists()


def test_retired_transition_statistics_are_not_a_mutation_worker_input(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    tree, copied_targets = control_snapshot
    source = ROOT / "atlas/known-best/video/spikes/v2-transitions/transition-stats.json"
    relative = source.relative_to(controls.REPO)
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())
    assert source.is_file()
    assert source in PRUNE
    assert all(
        (ROOT / control["file"]).resolve() != source
        and "transition-stats.json" not in control["run"]
        for control in specification["controls"]
    )
    assert relative not in copied_targets
    assert not (tree / relative).exists()
    # Both the live native audit's inputs and the linked historical narrative stay.
    for retained in (
        ROOT / "campaign/agent-sessions/session-153-native-full.json",
        ROOT / "campaign/agent-sessions/session-153-native-full.rows.jsonl",
        source.with_name("NOTES.md"),
    ):
        assert (
            tree / retained.relative_to(controls.REPO)
        ).read_bytes() == retained.read_bytes()


def test_composite_vectors_are_not_a_mutation_worker_input(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    """The 2026-10-05 breach's answer: the composite vectors really leave every worker.

    Until the root README stopped linking them, a pruned vector was copied straight back
    and the prune saved nothing; the 2026-09-22 measurement recorded at `PRUNE` found
    exactly that. So the half worth asserting is the copy-back: a checked document that
    links either vector again returns its bytes to the snapshot, and this fails rather
    than letting 8.6 MB of headroom disappear unnoticed. The other half is that no
    control reaches them, as a mutation target or by naming them in a command.
    """
    tree, copied_targets = control_snapshot
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())
    for source in sorted(COMPOSITE_VECTORS):
        relative = source.relative_to(controls.REPO)
        assert source.is_file()
        assert all(
            (ROOT / control["file"]).resolve() != source and source.name not in control["run"]
            for control in specification["controls"]
        )
        assert relative not in copied_targets
        assert not (tree / relative).exists()
    # The small records beside them that controls do reach stay, byte for byte.
    contact = ROOT / "atlas/known-best/contact-full-cell-control.json"
    assert (tree / contact.relative_to(controls.REPO)).read_bytes() == contact.read_bytes()


def test_individually_rescued_paths_reach_the_worker(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    """Every path `COPY_SEPARATELY` names arrives, byte for byte, at the same place.

    These are the files a check reads by exact path out of a directory the snapshot
    otherwise prunes, so a missing one is not a smaller worker but a checker that raises
    before any mutation is applied -- which is how `resources/bibliography.yaml` blinded
    all ten `validate_schemas` controls on 2026-09-22. The tuple is now what `clone_tree`
    copies and what `snapshot_source_bytes` counts; this asserts the copy actually lands.
    """
    tree, _copied = control_snapshot
    assert ROOT / "resources/bibliography.yaml" in COPY_SEPARATELY
    for source in COPY_SEPARATELY:
        landed = tree / source.relative_to(controls.REPO)
        assert landed.is_file(), f"rescued path missing from the worker: {source}"
        assert landed.read_bytes() == source.read_bytes()


def test_agenda_041_bulk_output_is_pruned_but_linked_receipts_survive(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    """The 2026-09-22 breach's answer, asserted from both sides rather than described.

    Agenda 041 is the largest single entry in `PRUNE` at 10,827,488 bytes, and the claim
    that earned it has two halves. No control reaches it, as a mutation target or by
    naming it in a command. And the receipts a checked document links inline still
    arrive in the worker byte for byte, which is what keeps the link scan answering
    about the record rather than about the prune -- the failure mode
    `linked_pruned_targets` exists to prevent.
    """
    tree, copied_targets = control_snapshot
    directory = ROOT / "campaign/series/series-000-smoke-and-calibration/results/agenda-041"
    packing_relative = directory.relative_to(ROOT).as_posix()
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())

    assert directory in PRUNE
    assert all(
        not (ROOT / control["file"]).resolve().is_relative_to(directory)
        for control in specification["controls"]
    )
    assert all(packing_relative not in control["run"] for control in specification["controls"])

    sources = [path for path in directory.rglob("*") if path.is_file()]
    assert sources
    for source in sources:
        relative = source.relative_to(controls.REPO)
        copied = tree / relative
        if relative in copied_targets:
            assert copied.read_bytes() == source.read_bytes()
        else:
            assert not copied.exists()

    # Named rather than left to the loop: this one journal is 7,127,269 of the prune,
    # and a future link to it would quietly return two thirds of the saving.
    journal = directory / "exp-222-n17-repricing-cells.jsonl"
    assert journal.is_file()
    assert not (tree / journal.relative_to(controls.REPO)).exists()


def test_agenda_039_bulk_is_pruned_while_record_and_w3_inputs_survive(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    """The combined native/W3 snapshot keeps every checked record and drops old bulk."""
    tree, copied_targets = control_snapshot
    directory = ROOT / "campaign/series/series-000-smoke-and-calibration/results/agenda-039"
    packing_relative = directory.relative_to(ROOT).as_posix()
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())

    assert directory in PRUNE
    assert all(
        not (ROOT / control["file"]).resolve().is_relative_to(directory)
        for control in specification["controls"]
    )
    assert all(packing_relative not in control["run"] for control in specification["controls"])

    document_map = safe_load((controls.REPO / "docs/project/document-map.yaml").read_text())
    mapped = {
        controls.REPO / row["path"]
        for row in document_map["documents"]
        if row["path"].startswith(f"packing/{packing_relative}/")
    }
    assert mapped
    for source in mapped:
        relative = source.relative_to(controls.REPO)
        assert relative in copied_targets
        assert (tree / relative).read_bytes() == source.read_bytes()

    unused_bulk = directory / "n18-4679-1000-t029-auto-windows5-certificate.json"
    assert unused_bulk.is_file()
    assert unused_bulk.relative_to(controls.REPO) not in copied_targets
    assert not (tree / unused_bulk.relative_to(controls.REPO)).exists()

    retained_w3 = [
        ROOT / "campaign/explorations/X-043-new-lower-bound-proof-directions.md",
        ROOT / "campaign/explorations/X-044-low-n-certificate-transfer.md",
        ROOT / "campaign/explorations/X-045-n11-global-capture-and-exact-optimality.md",
    ]
    cases = ROOT / "cases/w3_lower_bound_directions"
    retained_w3.extend(
        path
        for path in cases.rglob("*")
        if path.is_file() and path.suffix in {".py", ".json", ".md"}
    )
    assert len(retained_w3) > 4
    for source in retained_w3:
        relative = source.relative_to(controls.REPO)
        assert (tree / relative).read_bytes() == source.read_bytes()


def test_session_152_timing_archive_is_not_a_mutation_worker_input(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    tree, copied_targets = control_snapshot
    archive = (
        ROOT
        / "campaign/agent-sessions/session-152-validation"
        / "validation-timings-validate-1.zip"
    )
    session = ROOT / "campaign/agent-sessions/session-152-external-density-and-n11-review.md"
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())
    relative = archive.relative_to(controls.REPO)
    packing_relative = archive.relative_to(ROOT).as_posix()

    assert archive.is_file()
    assert archive in PRUNE
    assert all(
        (ROOT / control["file"]).resolve() != archive and packing_relative not in control["run"]
        for control in specification["controls"]
    )
    assert relative not in copied_targets
    assert not (tree / relative).exists()
    assert (tree / session.relative_to(controls.REPO)).read_bytes() == session.read_bytes()


def test_historical_byproducts_are_kept_in_git_but_not_workers(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    tree, copied_targets = control_snapshot
    byproducts = (
        ROOT / "campaign/agent-sessions/session-106-validation/fast-3deb90fc.tar.gz",
        ROOT / "campaign/agent-sessions/session-152-validation/full-initial-diagnostic.log",
        ROOT
        / "campaign/series/series-000-smoke-and-calibration/results/agenda-040"
        / "one-spare-inventory-n21-orbits.json.gz",
        ROOT / "campaign/agent-sessions/session-105-validation/full-48a4544f.json",
    )
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())
    for source in byproducts:
        relative = source.relative_to(controls.REPO)
        packing_relative = source.relative_to(ROOT).as_posix()
        assert source.is_file()
        assert source in PRUNE
        assert all(
            (ROOT / control["file"]).resolve() != source
            and packing_relative not in control["run"]
            for control in specification["controls"]
        )
        assert relative not in copied_targets
        assert not (tree / relative).exists()
    for session in (
        ROOT / "campaign/agent-sessions/session-106-n26-source-consistency.md",
        ROOT / "campaign/agent-sessions/session-152-external-density-and-n11-review.md",
        ROOT / "campaign/agent-sessions/session-105-stromquist-n26-verification.md",
        ROOT
        / "campaign/series/series-000-smoke-and-calibration/results/agenda-040"
        / "bentz2016-one-spare-receipt.md",
    ):
        assert (tree / session.relative_to(controls.REPO)).read_bytes() == session.read_bytes()


def test_historical_diagnostics_have_no_declared_worker_consumer() -> None:
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())
    for source in HISTORICAL_DIAGNOSTIC_OUTPUTS:
        assert source.is_file()
        assert all(
            (ROOT / control["file"]).resolve() != source and source.name not in control["run"]
            for control in specification["controls"]
        )
    assert not HISTORICAL_DIAGNOSTIC_OUTPUTS.intersection(controls.snapshot_pruned_targets())


def test_historical_diagnostics_leave_workers_but_declared_dependencies_return(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Exercise the real copier, counter and private index on a small source fixture."""
    source_repo = tmp_path / "source"
    source_root = source_repo / HERE

    def rebase(path: Path) -> Path:
        return source_repo / path.relative_to(controls.REPO)

    omitted = {rebase(path): path.read_bytes() for path in HISTORICAL_DIAGNOSTIC_OUTPUTS}
    for path, payload in omitted.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)
    reader = source_root / "devtools/check_results.py"
    reader.parent.mkdir(parents=True)
    reader.write_bytes((ROOT / "devtools/check_results.py").read_bytes())
    record = source_root / "campaign/README.md"
    record.write_text("Retained diagnostic record.\n")
    register = source_root / "frontier/results.yaml"
    register.parent.mkdir()
    register.write_text("results: []\n")

    prunes = frozenset(rebase(path) for path in PRUNE)
    linked_roots = tuple(rebase(path) for path in controls.LINKED_PRUNE_ROOTS)
    descend = frozenset(
        ancestor
        for path in prunes
        for ancestor in path.parents
        if source_root in (ancestor, *ancestor.parents)
    )
    monkeypatch.setattr(controls, "REPO", source_repo)
    monkeypatch.setattr(controls, "ROOT", source_root)
    monkeypatch.setattr(controls, "PRUNE", prunes)
    monkeypatch.setattr(controls, "DESCEND", descend)
    monkeypatch.setattr(controls, "LINKED_PRUNE_ROOTS", linked_roots)
    monkeypatch.setattr(controls, "COPY_SEPARATELY", ())
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", ())
    monkeypatch.setattr(controls, "LINK_BACK", ())

    for route in ("omitted", "linked", "registered"):
        if route == "linked":
            record.write_text(
                "\n".join(
                    f"[diagnostic]({os.path.relpath(path, record.parent)})" for path in omitted
                )
            )
            assert set(controls.linked_pruned_targets()) == set(omitted)
        elif route == "registered":
            record.write_text("Retained diagnostic record.\n")
            register.write_text(
                "results:\n- artifacts:\n"
                + "".join(
                    f"  - {path.relative_to(source_repo).as_posix()}\n" for path in omitted
                )
            )
            assert set(result_pruned_targets()) == set(omitted)
        tree = tmp_path / route
        clone_tree(tree)
        assert (tree / reader.relative_to(source_repo)).read_bytes() == reader.read_bytes()
        assert (tree / record.relative_to(source_repo)).read_bytes() == record.read_bytes()
        indexed = tracked_files(tree, ".")
        assert indexed is not None
        assert tree / reader.relative_to(source_repo) in indexed
        expected_bytes = reader.stat().st_size + record.stat().st_size + register.stat().st_size
        for path, payload in omitted.items():
            target = tree / path.relative_to(source_repo)
            assert path.read_bytes() == payload
            if route == "omitted":
                assert not target.exists()
                assert target not in indexed
            else:
                assert target.read_bytes() == payload
                assert not target.is_symlink()
                assert target in indexed
                expected_bytes += len(payload)
        assert snapshot_source_bytes() == expected_bytes


def test_session163_push_logs_are_not_control_inputs() -> None:
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())
    assert SESSION163_PUSH_LOGS <= PRUNE
    for source in SESSION163_PUSH_LOGS:
        assert source.is_file()
        assert source.stat().st_size > 0
        assert all(
            (ROOT / control["file"]).resolve() != source and source.name not in control["run"]
            for control in specification["controls"]
        )


def test_session163_push_logs_leave_workers_while_the_record_survives(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    tree, copied_targets = control_snapshot
    for source in SESSION163_PUSH_LOGS:
        relative = source.relative_to(controls.REPO)
        assert source.is_file()
        assert relative not in copied_targets
        assert not (tree / relative).exists()
    session = ROOT / "campaign/agent-sessions/session-163-native-bounds-and-census.md"
    assert (tree / session.relative_to(controls.REPO)).read_bytes() == session.read_bytes()


def test_session163_push_logs_return_when_a_checked_document_links_them(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    document = tmp_path / "linked-logs.md"
    document.write_text(
        "\n".join(
            f"[log]({os.path.relpath(source, tmp_path)})"
            for source in sorted(SESSION163_PUSH_LOGS)
        )
    )
    monkeypatch.setattr(controls, "_linked_documents", lambda: [document])
    assert set(controls.linked_pruned_targets()) >= SESSION163_PUSH_LOGS


def test_old_validation_archive_is_pruned_while_current_records_survive(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    """Old compressed bulk leaves workers; its record and current evidence stay."""
    tree, copied_targets = control_snapshot
    archive = (
        ROOT
        / "campaign/agent-sessions/session-106-validation"
        / "full-46ee41af-validate.tar.gz"
    )
    session = ROOT / "campaign/agent-sessions/session-106-n26-source-consistency.md"
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())
    packing_relative = archive.relative_to(ROOT).as_posix()

    assert archive in PRUNE
    assert archive.is_file()
    assert all(
        (ROOT / control["file"]).resolve() != archive.resolve()
        for control in specification["controls"]
    )
    assert all(packing_relative not in control["run"] for control in specification["controls"])
    relative = archive.relative_to(controls.REPO)
    assert relative not in copied_targets
    assert not (tree / relative).exists()
    assert (tree / session.relative_to(controls.REPO)).read_bytes() == session.read_bytes()

    retained = [
        ROOT / "campaign/agent-sessions/session-153-native-full.json",
        ROOT / "campaign/agent-sessions/session-153-native-full.rows.jsonl",
        ROOT / "campaign/explorations/X-043-new-lower-bound-proof-directions.md",
        ROOT / "campaign/explorations/X-044-low-n-certificate-transfer.md",
        ROOT / "campaign/explorations/X-045-n11-global-capture-and-exact-optimality.md",
    ]
    retained.extend(
        path
        for path in (ROOT / "cases/w3_lower_bound_directions").rglob("*")
        if path.is_file() and path.suffix in {".py", ".json", ".md"}
    )
    for source in retained:
        landed = tree / source.relative_to(controls.REPO)
        assert landed.read_bytes() == source.read_bytes()


def test_retained_receipts_leave_workers_but_registered_and_linked_ones_return(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    """The 2026-10-06 prune, asserted from both sides, as agenda 041's is.

    No control reaches the five roots, as a mutation target or by naming one in a
    command. Every file under them is either absent from the worker or, when a checked
    document links it or the results register lists it, present byte for byte -- the two
    census READMEs and the registered receipts among them. A folder a review links
    arrives empty rather than missing, so the link scan still finds it.
    """
    tree, copied_targets = control_snapshot
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())
    for directory in sorted(RETAINED_RECEIPT_ROOTS):
        assert directory in PRUNE
        packing_relative = directory.relative_to(ROOT).as_posix()
        assert all(
            not (ROOT / control["file"]).resolve().is_relative_to(directory)
            and packing_relative not in control["run"]
            for control in specification["controls"]
        )
        sources = [path for path in directory.rglob("*") if path.is_file()]
        assert sources
        for source in sources:
            relative = source.relative_to(controls.REPO)
            copied = tree / relative
            if relative in copied_targets:
                assert copied.read_bytes() == source.read_bytes()
            else:
                assert not copied.exists()

    census = ROOT / "benchmarks/measure-verifier"
    for returned in (
        census / "census/README.md",
        census / "census-mixed/README.md",
        census / "census/census.json",
        census / "census-mixed/census.json",
    ):
        relative = returned.relative_to(controls.REPO)
        assert relative in copied_targets
        assert (tree / relative).read_bytes() == returned.read_bytes()
    for linked in (
        census / "review-2026-10-03-attack",
        ROOT / "witnesses/franciscouzo-2026-10-03",
    ):
        landed = tree / linked.relative_to(controls.REPO)
        assert landed.is_dir()
        assert not any(landed.iterdir())


def test_math_startup_reports_are_pruned_but_record_sources_survive(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    tree, copied_targets = control_snapshot
    campaign = ROOT / "benchmarks/math-startup"
    for directory in (campaign / "runs", campaign / "fixtures"):
        assert directory in PRUNE
        sources = [path for path in directory.rglob("*") if path.is_file()]
        assert sources
        for source in sources:
            relative = source.relative_to(controls.REPO)
            copied = tree / relative
            if relative in copied_targets:
                assert copied.read_bytes() == source.read_bytes()
            else:
                assert not copied.exists()

    records = [*campaign.rglob("*.md"), *campaign.rglob("*.yaml")]
    assert records
    for source in records:
        assert (tree / source.relative_to(controls.REPO)).read_bytes() == source.read_bytes()

    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())
    for control in specification["controls"]:
        source = (ROOT / control["file"]).resolve()
        assert (tree / source.relative_to(controls.REPO)).is_file()


@pytest.mark.slow
def test_build_caches_leave_the_counted_surface_and_the_worker_trees(
    tmp_path: Path,
    control_snapshot: tuple[Path, set[Path]],
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

    source, _copied = control_snapshot
    tree = tmp_path / "snapshot"
    environment = os.environ.copy()
    environment["PYTHONPATH"] = os.pathsep.join(
        (str(source / HERE / "src"), str(source / HERE))
    )
    script = """
import shutil
import sys
from pathlib import Path

from devtools import run_negative_controls as controls

destination = Path(sys.argv[1])
probe_bytes = b"n" * int(sys.argv[2])
probe_root = controls.ROOT / ".negative-control-cache-probe"
caches = [probe_root / name / "probe.bin" for name in sys.argv[3:]]
counted = probe_root / "counted.bin"
if controls.ROOT != Path.cwd():
    raise RuntimeError(f"loaded controls from {controls.ROOT}, expected {Path.cwd()}")
shutil.rmtree(probe_root, ignore_errors=True)
before = controls.snapshot_source_bytes()
try:
    for probe in (*caches, counted):
        probe.parent.mkdir(parents=True, exist_ok=True)
        probe.write_bytes(probe_bytes)
    after = controls.snapshot_source_bytes()
    if after != before + len(probe_bytes):
        raise AssertionError((before, after, len(probe_bytes)))
    controls.clone_tree(destination)
finally:
    shutil.rmtree(probe_root, ignore_errors=True)
"""
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            script,
            str(tree),
            str(len(CACHE_PROBE_BYTES)),
            *CACHE_PROBE_DIRECTORIES,
        ],
        cwd=source / HERE,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert completed.returncode == 0, completed.stderr

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
    counted = tree / HERE / ".negative-control-cache-probe/counted.bin"
    assert counted.read_bytes() == CACHE_PROBE_BYTES
    assert not CACHE_PROBE_ROOT.exists()


def test_results_register_dependencies_survive_snapshot_pruning() -> None:
    retained = {path.relative_to(ROOT).as_posix() for path in result_pruned_targets()}
    assert "resources/papers/bentz-2010-optimal-packings-13-and-46.md" in retained
    assert "resources/papers/nagamochi-2005-packing-unit-squares-in-a-rectangle.pdf" in retained


def test_snapshot_inventory_preserves_copy_count_and_cache_exclusions(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "packing"
    root.mkdir()
    ordinary = root / "source.py"
    ordinary.write_bytes(b"source")
    omitted = root / "old.log"
    omitted.write_bytes(b"historical output")
    (root / "source-link.py").symlink_to(ordinary)
    cache = root / "nested/__pycache__"
    cache.mkdir(parents=True)
    (cache / "ignored.pyc").write_bytes(b"not source")
    docs = tmp_path / "docs"
    docs.mkdir()
    document = docs / "notes.md"
    document.write_bytes(b"notes")
    (docs / "__pycache__").mkdir()
    (docs / "__pycache__/ignored.pyc").write_bytes(b"not source")
    monkeypatch.setattr(controls, "ROOT", root)
    monkeypatch.setattr(controls, "COPY_SEPARATELY", (omitted,))
    monkeypatch.setattr(controls, "root_files", lambda: ())
    monkeypatch.setattr(controls, "snapshot_pruned_targets", lambda: [omitted])
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", (docs,))
    monkeypatch.setattr(controls, "PRUNE", frozenset((omitted,)))
    assert controls.snapshot_source_paths() == [omitted, document, ordinary]
    assert controls.snapshot_source_bytes() == omitted.stat().st_size + 11
    assert controls.snapshot_duplicate_copy_bytes() == omitted.stat().st_size


@pytest.fixture
def snapshot_audit_fixture(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, Path]:
    root = tmp_path / "packing"
    old = root / "old"
    old.mkdir(parents=True)
    generated = old / "generated.bin"
    generated.write_bytes(b"g" * 10)
    linked = old / "linked.log"
    linked.write_bytes(b"l" * 14)
    registered = old / "result.bin"
    registered.write_bytes(b"r" * 20)
    core = root / "source.py"
    core.write_bytes(b"s" * 7)
    document = tmp_path / "notes.md"
    document.write_text("[evidence](packing/old/linked.log)\n")
    register = root / "frontier/results.yaml"
    register.parent.mkdir()
    register.write_text("results:\n- artifacts: [packing/old/result.bin]\n")
    spec = root / "controls.yaml"
    spec.write_text(
        "controls:\n"
        "- name: an exact target consumer\n"
        "  file: old/generated.bin\n"
        "  run: python3 -m devtools.example\n"
        "- name: an exact command consumer\n"
        "  file: source.py\n"
        "  run: python3 -m devtools.example old/linked.log\n"
    )
    monkeypatch.setattr(controls, "ROOT", root)
    monkeypatch.setattr(controls, "REPO", tmp_path)
    monkeypatch.setattr(controls, "LINKED_PRUNE_ROOTS", ())
    monkeypatch.setattr(controls, "COPY_SEPARATELY", ())
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", (document,))
    monkeypatch.setattr(controls, "root_files", lambda: ())
    monkeypatch.setattr(controls, "_linked_documents", lambda: [document])
    monkeypatch.setattr(
        controls, "snapshot_source_paths", lambda: [generated, linked, registered, core]
    )
    return old, spec


def test_snapshot_audit_counts_rescue_and_overlapping_candidates_once(
    snapshot_audit_fixture: tuple[Path, Path],
) -> None:
    old, spec = snapshot_audit_fixture
    report = controls.snapshot_audit([old, old / "generated.bin"], spec_path=spec)
    assert report["source_bytes"] == 51
    assert report["copy_operations"] == 4
    assert report["candidate_net_saved_bytes"] == 10
    assert report["candidate_source_bytes"] == 41
    candidates = report["candidates"]
    assert isinstance(candidates, list)
    candidate = candidates[0]
    assert candidate["currently_copied_bytes"] == 44
    assert candidate["net_saved_bytes"] == 10
    assert candidate["inline_rescue"] == [{"path": "packing/old/linked.log", "bytes": 14}]
    assert candidate["result_rescue"] == [{"path": "packing/old/result.bin", "bytes": 20}]
    assert [row["name"] for row in candidate["registered_mentions"]] == [
        "an exact target consumer",
        "an exact command consumer",
    ]


def test_snapshot_audit_rejects_missing_and_escaping_candidates(
    snapshot_audit_fixture: tuple[Path, Path],
    tmp_path: Path,
) -> None:
    old, spec = snapshot_audit_fixture
    for candidate in (old / "absent.bin", tmp_path.parent):
        with pytest.raises(ValueError, match="must exist inside the repository"):
            controls.snapshot_audit([candidate], spec_path=spec)


@pytest.mark.parametrize(
    ("route", "selection"),
    [
        ("root_files", "file"),
        ("root_files", "parent"),
        ("COPY_SEPARATELY", "file"),
        ("COPY_SEPARATELY", "parent"),
        ("ROOT_DOCUMENTS", "file"),
        ("ROOT_DOCUMENTS", "parent"),
        ("ROOT_DOCUMENTS", "directory"),
        ("ROOT_DOCUMENTS", "descendant"),
    ],
)
def test_snapshot_audit_refuses_unconditional_copy_candidates(
    snapshot_audit_fixture: tuple[Path, Path],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    *,
    route: str,
    selection: str,
) -> None:
    _old, spec = snapshot_audit_fixture
    directory = tmp_path / "always-copied"
    directory.mkdir()
    copied = directory / "source.txt"
    copied.write_bytes(b"unconditional source")
    target = directory if selection in ("directory", "descendant") else copied
    candidate = directory if selection in ("directory", "parent") else copied
    monkeypatch.setattr(controls, "COPY_SEPARATELY", ())
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", ())
    monkeypatch.setattr(controls, "root_files", lambda: ())
    if route == "root_files":
        monkeypatch.setattr(controls, "root_files", lambda: (target,))
    else:
        monkeypatch.setattr(controls, route, (target,))
    # An unconditional copied destination cannot be suppressed by a tree-walk prune.
    monkeypatch.setattr(controls, "snapshot_source_paths", lambda: [copied])
    monkeypatch.setattr(
        controls, "clone_tree", lambda _tree: pytest.fail("audit copied source")
    )
    monkeypatch.setattr(
        controls, "run_control_command", lambda *_args: pytest.fail("audit ran a control")
    )
    with pytest.raises(ValueError, match="copies regardless of PRUNE") as error:
        controls.snapshot_audit([candidate], spec_path=spec)
    assert route in str(error.value)
    assert candidate.relative_to(tmp_path).as_posix() in str(error.value)
    assert target.relative_to(tmp_path).as_posix() in str(error.value)
    with pytest.raises(SystemExit, match="2"):
        controls.main([str(spec), "--audit-snapshot", "--prune-candidate", str(candidate)])
    output = capsys.readouterr()
    assert output.out == ""
    assert "copies regardless of PRUNE" in output.err
    assert route in output.err


def test_snapshot_audit_cli_never_clones_or_runs_a_control(
    snapshot_audit_fixture: tuple[Path, Path],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    old, spec = snapshot_audit_fixture
    monkeypatch.setattr(
        controls, "clone_tree", lambda _tree: pytest.fail("audit copied source")
    )
    monkeypatch.setattr(
        controls, "run_control_command", lambda *_args: pytest.fail("audit ran a control")
    )
    assert controls.main([str(spec), "--audit-snapshot", "--prune-candidate", str(old)]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["source_bytes"] == 51
    assert report["candidate_source_bytes"] == 41
    with pytest.raises(SystemExit, match="2"):
        controls.main([str(spec), "--prune-candidate", str(old)])


def test_tiny_snapshot_prune_rescues_linked_and_registered_files_as_private_copies(
    snapshot_audit_fixture: tuple[Path, Path],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    old, _spec = snapshot_audit_fixture
    monkeypatch.setattr(controls, "HERE", Path("packing"))
    monkeypatch.setattr(controls, "PRUNE", frozenset((old,)))
    monkeypatch.setattr(controls, "DESCEND", frozenset(old.parents))
    monkeypatch.setattr(controls, "LINKED_PRUNE_ROOTS", (old,))
    monkeypatch.setattr(controls, "COPY_SEPARATELY", ())
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", (tmp_path / "notes.md",))
    monkeypatch.setattr(controls, "LINK_BACK", ())
    monkeypatch.setattr(controls, "root_files", lambda: ())
    destination = tmp_path / "worker"
    controls.clone_tree(destination)
    retained = tracked_files(destination, "*")
    assert retained is not None
    for name in ("linked.log", "result.bin"):
        landing = destination / "packing/old" / name
        assert landing.read_bytes() == (old / name).read_bytes()
        assert not landing.is_symlink()
        assert landing in retained
    assert not (destination / "packing/old/generated.bin").exists()
    assert (old / "generated.bin").read_bytes() == b"g" * 10
    (destination / "packing/old/result.bin").write_bytes(b"mutated")
    assert (old / "result.bin").read_bytes() == b"r" * 20
    # A future inline citation brings an omitted output back without changing PRUNE.
    (tmp_path / "notes.md").write_text("[new evidence](packing/old/generated.bin)\n")
    assert old / "generated.bin" in controls.snapshot_pruned_targets()


def test_workflow_evidence_selection_keeps_only_existing_referenced_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    workflows = tmp_path / ".github/workflows"
    workflows.mkdir(parents=True)
    needed = workflows / "needed.yml"
    needed.write_text("name: evidence\n")
    (workflows / "unused.yml").write_text("name: unreferenced\n")
    outside = tmp_path / "outside.yml"
    outside.write_text("name: outside the workflow root\n")
    (workflows / "escape.yml").symlink_to(outside)
    document = tmp_path / "SYNOPSIS.md"
    document.write_text(
        "[needed](.github/workflows/needed.yml)\n"
        "[again](.github/workflows/needed.yml)\n"
        "[absent](.github/workflows/absent.yml)\n"
        "[escape](.github/workflows/escape.yml)\n"
    )
    monkeypatch.setattr(controls, "ROOT", tmp_path / "packing")
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", (document,))
    monkeypatch.setattr(controls, "LINKED_PRUNE_ROOTS", (workflows,))
    assert controls.linked_pruned_targets() == [needed]


def test_a_worker_snapshot_can_be_asked_what_this_repository_tracks(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    """A snapshot is a git checkout of itself, holding the tracked files it carries.

    Checks that read the directory ask `repo_scope.tracked_files` rather than walking,
    because a walk reads the reader's scratch and the other agents' worktrees too. Where
    a snapshot has no index those checks do not run the code the gate runs: they either
    refuse, which is how main went red on 2026-09-21, or they take a fallback, and a
    control over a fallback would rehearse the fallback. Only `check_readme` of the three
    callers has a registered control, so the first of those is what was seen.

    Both halves are asserted, because either one alone is satisfiable by the wrong tree.
    That the index answers at all is the regression; that it answers with exactly the
    repository's own tracked set restricted to what the snapshot carries is what keeps it
    honest -- an index built by adding whatever happens to be on disk would also answer,
    and would put a reader's `attic/` scratch in it (PR 207).
    """
    from devtools import evand_arrangement_houses as evand  # noqa: PLC0415
    from devtools import gupta_house_links as gupta  # noqa: PLC0415
    from devtools import refinement_house_links as refinements  # noqa: PLC0415
    from devtools import ryxu_house_links as ryxu  # noqa: PLC0415
    from devtools import squish_followup_packets as packet  # noqa: PLC0415
    from devtools import squish_second_update_confirmation as second  # noqa: PLC0415
    from devtools import squish_second_update_house_links as house  # noqa: PLC0415

    tree, _copied = control_snapshot
    listed = tracked_files(tree, ".")
    assert listed is not None, "the worker snapshot has no index to ask"
    tracked = {path.relative_to(tree).as_posix() for path in listed}
    assert "README.md" in tracked
    assert "packing/devtools/check_readme.py" in tracked

    names = subprocess.run(
        ("git", "-C", str(controls.REPO), "ls-files", "-z", "--cached"),
        check=True,
        capture_output=True,
    ).stdout.split(b"\0")
    linked_root = tree / "packing/witnesses/squish-401-update-2026"
    assert linked_root.is_symlink()
    linked_proofs = {
        packet.certificate_path(n).relative_to(controls.REPO).as_posix()
        for n in packet.RESULT_NUMBERS
    }
    linked_proofs.update(
        second.certificate_path(n).relative_to(controls.REPO).as_posix() for n in second.NUMBERS
    )
    linked_proofs.update(
        house.house_path(n).relative_to(controls.REPO).as_posix() for n in house.LINK_NUMBERS
    )
    linked_proofs.update(
        path.relative_to(controls.REPO).as_posix()
        for path in refinements.snapshot_house_links()
    )
    linked_proofs.update(
        path.relative_to(controls.REPO).as_posix() for path in evand.snapshot_house_links()
    )
    linked_proofs.update(
        path.relative_to(controls.REPO).as_posix() for path in ryxu.snapshot_house_links()
    )
    linked_proofs.update(
        path.relative_to(controls.REPO).as_posix() for path in gupta.snapshot_house_links()
    )
    for relative in linked_proofs:
        assert (tree / relative).is_file()
        assert (tree / relative).resolve() == (controls.REPO / relative).resolve()
    repository = {
        name.decode()
        for name in names
        if name and (tree / name.decode()).is_file() and name.decode() not in linked_proofs
    }
    assert tracked == repository
    assert not tracked & linked_proofs

    # The linked-back environment and cargo target are the real checkout's, not this
    # snapshot's content, which is why the index is built before they are symlinked in.
    assert not any(
        name.startswith(
            (
                "packing/.venv",
                "packing/sqsearch/target",
                "packing/sqverify_exact/target",
                "packing/sqverify_fast/target",
                "packing/n17bb_native/target",
            )
        )
        for name in tracked
    )


#: Control commands whose unmutated baseline is held green in a worker. A control is scored
#: "exited non-zero and printed its expected message", with no green baseline demanded, so
#: a checker already red in the worker lets its controls pass for a reason that is not
#: their mutation (think-nns5). Measured 2026-10-05 by running every distinct command in
#: `controls.yaml` unmutated in a fresh worker: these two were red there, on root files and
#: the pull-request template the snapshot did not carry, and back the 4 README and 35
#: ledger controls. Two remain red and are not listed: `validate_schemas`, on verifier
#: registry paths under the pruned `resources/web/`, and
#: `tests/test_change_scoped_selection.py`, on `vendor/kpress`, which no worker carries.
GREEN_BASELINE_COMMANDS = (
    "python3 -m devtools.check_readme",
    "python3 -m sqpack.campaign.ledger check",
)


@pytest.mark.parametrize("command", GREEN_BASELINE_COMMANDS)
def test_a_control_command_is_green_unmutated_in_a_worker(
    control_snapshot: tuple[Path, set[Path]], command: str
) -> None:
    """The registry's own command, in the environment `run_one` gives it, with no edit.

    For `check_readme` this also holds what the README controls first lost on
    2026-09-21: an exit of 0 is past the "no index" refusal (`NO_INDEX`) they read in place
    of the drift they mutate for.
    """
    spec = safe_load((ROOT / "devtools/controls.yaml").read_text(encoding="utf-8"))
    assert command in {control["run"] for control in spec["controls"]}
    tree, _copied = control_snapshot
    with tempfile.TemporaryDirectory(prefix="negctl-pycache-", dir=tree) as pycache:
        outcome = run_control_command(
            command,
            cwd=tree / HERE,
            environment=controls.control_environment(tree, Path(pycache)),
            timeout_seconds=controls.DEFAULT_CONTROL_TIMEOUT_SECONDS,
        )
    assert not outcome.timed_out
    output = outcome.stdout + outcome.stderr
    assert NO_INDEX not in output
    assert outcome.returncode == 0, output


def test_the_root_files_reach_every_worker(control_snapshot: tuple[Path, set[Path]]) -> None:
    """Every file tracked at the repository root is in the worker, byte for byte."""
    tree, _copied = control_snapshot
    root = controls.root_files()
    assert controls.REPO / "Makefile" in root
    assert controls.REPO / ".gitmodules" in root
    for path in (*root, *COPY_SEPARATELY):
        relative = path.relative_to(controls.REPO)
        assert (tree / relative).read_bytes() == path.read_bytes(), relative


@pytest.mark.slow
def test_unmutated_results_checker_is_green_inside_a_worker(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    tree, _workflows = control_snapshot
    completed = subprocess.run(
        [sys.executable, "-m", "devtools.check_results"],
        cwd=tree / "packing",
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_synopsis_snapshot_is_clean_before_its_registered_mutation(
    control_snapshot: tuple[Path, set[Path]], monkeypatch: pytest.MonkeyPatch
) -> None:
    # Main measured this call at 14.44s against the 12s quick-lane ceiling. The snapshot
    # and its selection are shared setup; the real clean check, mutation and restoration
    # remain measured here, with no relaxed ceiling or slow-lane deferral.
    tree, copied_targets = control_snapshot
    work = tree / HERE
    synopsis = tree / "SYNOPSIS.md"
    original = synopsis.read_bytes()
    environment = {
        **os.environ,
        "PYTHONPATH": os.pathsep.join((str(work / "src"), str(work))),
    }
    baseline = subprocess.run(
        [sys.executable, "-m", "devtools.check_synopsis"],
        cwd=work,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert baseline.returncode == 0, baseline.stdout + baseline.stderr

    for name in ("deep-gate.yml", "branch-mergeability.yml"):
        relative = Path(".github/workflows") / name
        assert (tree / relative).read_bytes() == (controls.REPO / relative).read_bytes()
    copied_workflows = {
        path.relative_to(tree)
        for path in (tree / ".github/workflows").rglob("*")
        if path.is_file()
    }
    assert copied_workflows == {
        path for path in copied_targets if path.is_relative_to(".github/workflows")
    }

    spec = safe_load((ROOT / "devtools/controls.yaml").read_text())
    control = next(
        item
        for item in spec["controls"]
        if item["name"] == "synopsis - dateline duplicates volatile campaign progress"
    )
    outcomes: list[controls.CommandOutcome] = []

    def capture(
        command: str, *, cwd: Path, environment: dict[str, str], timeout_seconds: float
    ) -> controls.CommandOutcome:
        outcome = run_control_command(
            command,
            cwd=cwd,
            environment=environment,
            timeout_seconds=timeout_seconds,
        )
        outcomes.append(outcome)
        return outcome

    monkeypatch.setattr(controls, "run_control_command", capture)
    assert controls.run_one(control, tree) == (True, "")
    assert len(outcomes) == 1
    assert "dead link" not in outcomes[0].stdout + outcomes[0].stderr
    assert synopsis.read_bytes() == original


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


@pytest.mark.parametrize("rule_count", [16, 17, 25])
def test_new_operating_rule_control_reaches_summary_drift_after_future_rules(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, rule_count: int
) -> None:
    spec = safe_load((ROOT / "devtools/controls.yaml").read_text())
    control = next(
        item
        for item in spec["controls"]
        if item["name"] == "operating rules - a new rule never reaches the summary"
    )
    work = tmp_path / HERE
    tools = work / "devtools"
    tools.mkdir(parents=True)
    (tools / "__init__.py").write_text("")
    shutil.copy2(ROOT / "devtools/render_operating_rules.py", tools)
    original = (
        "\n\n".join(f"## OR-{index}: Rule {index}" for index in range(1, rule_count + 1))
        + "\n\n<!-- This document follows common-doc-guidelines.md.\n-->\n"
    )
    source = tmp_path / "operating-rules.md"
    source.write_text(original)
    summary = "\n".join(
        f"- **OR-{index}:** Rule {index}." for index in range(1, rule_count + 1)
    )
    (tmp_path / "AGENTS.md").write_text(
        "<!-- BEGIN OPERATING RULES SUMMARY -->\n"
        + summary
        + "\n<!-- END OPERATING RULES SUMMARY -->\n"
    )
    monkeypatch.setenv(
        "PATH", str(Path(sys.executable).parent) + os.pathsep + os.environ["PATH"]
    )
    baseline = subprocess.run(
        [sys.executable, "-m", "devtools.render_operating_rules", "--check"],
        cwd=work,
        env={**os.environ, "PYTHONPATH": str(work)},
        capture_output=True,
        text=True,
        check=False,
    )
    assert baseline.returncode == 0, baseline.stderr
    assert f"mirrors all {rule_count} rules" in baseline.stdout
    assert controls.run_one(control, tmp_path) == (True, "")
    assert source.read_text() == original


@pytest.mark.slow
def test_squish_complete_replay_survives_worker_custody_and_private_controls(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    """Complete replay reads linked proofs and retains private admission records."""
    from devtools import squish_followup_packets as packet  # noqa: PLC0415

    tree, copied = control_snapshot
    work = tree / HERE
    root = work / "witnesses/squish-401-update-2026"
    assert root.is_symlink()
    for n in packet.RESULT_NUMBERS:
        source = packet.certificate_path(n)
        relative = source.relative_to(ROOT).as_posix()
        assert (work / relative).read_bytes() == source.read_bytes()
        with pytest.raises(ValueError, match="escapes private snapshot"):
            resolve_control_target(relative, tree=tree, work=work)
    for name in (
        "certification.json.xz",
        "negative-controls.json.xz",
        "replay-summary.json",
        "reviewed-semantic-binding.json.xz",
    ):
        source = packet.PACKET / "receipts" / name
        relative = source.relative_to(controls.REPO)
        assert relative in copied
        assert not (tree / relative).is_symlink()
        assert (tree / relative).read_bytes() == source.read_bytes()
    with tempfile.TemporaryDirectory(prefix="squish-baseline-pycache-", dir=tree) as pycache:
        env = controls.control_environment(tree, Path(pycache))
        baseline = subprocess.run(
            [sys.executable, "-m", "devtools.squish_followup_packets", "check-certification"],
            cwd=work,
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
    assert baseline.returncode == 0, baseline.stdout + baseline.stderr
    for name in ("fast-cpu4-bdc28e89", "fast-native-bdc28e89"):
        source = ROOT / f"campaign/agent-sessions/session-105-validation/{name}.json"
        assert source in PRUNE
        assert source.relative_to(controls.REPO) not in copied
        assert not (tree / source.relative_to(controls.REPO)).exists()
        identity = source.with_name(f"{name}-source.json")
        assert (
            tree / identity.relative_to(controls.REPO)
        ).read_bytes() == identity.read_bytes()
    session = ROOT / "campaign/agent-sessions/session-105-stromquist-n26-verification.md"
    assert (tree / session.relative_to(controls.REPO)).read_bytes() == session.read_bytes()


def _run_second_squish_native_program(tree: Path, program: str) -> None:
    baseline_program = (
        """
from devtools import squish_second_update_confirmation as packet
def forbidden(*args, **kwargs):
    raise AssertionError('native admission must not execute a geometric decider')
packet.decide = packet.original.decide = forbidden
packet.original.exact_verify = packet.original.independent.check = forbidden
"""
        + program
    )
    with tempfile.TemporaryDirectory(
        prefix="second-squish-baseline-pycache-", dir=tree
    ) as pycache:
        environment = controls.control_environment(tree, Path(pycache))
        baseline = subprocess.run(
            [sys.executable, "-c", baseline_program],
            cwd=tree / HERE,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
    assert baseline.returncode == 0, baseline.stdout + baseline.stderr


@pytest.mark.slow
def test_second_squish_complete_replay_survives_native_worker_boundaries(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    """Exercise the production copy, real index and every complete proof leaf."""
    from devtools import squish_second_update_confirmation as packet  # noqa: PLC0415
    from devtools import squish_second_update_house_links as house  # noqa: PLC0415

    tree, _copied = control_snapshot
    work = tree / HERE
    assert snapshot_source_bytes() <= SNAPSHOT_MAX_BYTES
    assert (tree / packet.WITNESSES.relative_to(controls.REPO)).is_symlink()
    listed = tracked_files(tree, ".")
    assert listed is not None, "the actual worker has no private index"
    tracked = {path.relative_to(tree) for path in listed}
    private_n263 = house.house_path(263).relative_to(controls.REPO)
    assert private_n263 in tracked
    assert not (tree / private_n263).is_symlink()
    for n in house.LINK_NUMBERS:
        relative = house.house_path(n).relative_to(controls.REPO)
        assert (tree / relative).is_symlink()
        assert relative not in tracked
        with pytest.raises(ValueError, match="escapes private snapshot"):
            resolve_control_target(relative.relative_to(HERE).as_posix(), tree=tree, work=work)
    for source in packet.private_input_paths():
        target = tree / source.relative_to(controls.REPO)
        assert not target.is_symlink()
        assert target.read_bytes() == source.read_bytes()
    _run_second_squish_native_program(
        tree,
        """
assert tuple(packet.check_certification()) == packet.NUMBERS
print('all 27 complete inputs and nine proof leaves admitted')
""",
    )


@pytest.mark.parametrize(
    "program",
    [
        pytest.param(
            """
from devtools import squish_second_update_house_links as house
# The current n108 house is #432 geometry and must not satisfy the old #422 receipt.
try:
    house.check_houses([108])
except packet.original.PacketError as error:
    assert 'full geometry or private metadata custody mismatch' in str(error)
else:
    raise AssertionError('new n108 geometry was accepted against historical #422 inputs')
from devtools.register_ryxu_reports import read_history
from devtools import register_gupta_reports as gupta
historical = {row['n']: row['house'] for row in read_history()}
if gupta.HISTORY.exists():
    for row in gupta.read_history():
        historical.setdefault(row['n'], row['house'])
    try:
        house.check_houses([88])
    except packet.original.PacketError as error:
        assert 'full geometry or private metadata custody mismatch' in str(error)
    else:
        raise AssertionError('new Gupta geometry was accepted against historical #422 inputs')
historical_paths = {}
for n in packet.NUMBERS:
    if n in historical:
        path = packet.PACKET / 'receipts' / f'worker-historical-n{n:03d}.yaml'
        path.write_text(historical[n])
        historical_paths[n] = path
current_house_path = house.house_path
house.house_path = lambda n: historical_paths.get(n, current_house_path(n))
assert tuple(house.check_houses()) == packet.NUMBERS
for path in historical_paths.values():
    path.unlink()
house.house_path = current_house_path
print('all nine original houses admitted from current or full retained history')
""",
            id="house-reads",
        ),
        pytest.param(
            """
from devtools import check_results
from devtools import squish_second_update_house_links as house
for path in (house.house_path(88), house.house_path(263), packet.certificate_path(88)):
    relative = path.relative_to(packet.REPO).as_posix()
    assert check_results.repository_file_problem(relative) is None
assert check_results.repository_file_problem('packing/witnesses/known-best/unrelated.yaml')
print('registry acceptance and refusal passed')
""",
            id="registry-routes",
        ),
        pytest.param(
            """
from devtools import build_known_best_atlas as atlas
for producer in (atlas.update, lambda: atlas.update_selected([88])):
    try:
        producer()
    except packet.original.PacketError as error:
        assert 'output escapes' in str(error)
    else:
        raise AssertionError('producer accepted a linked output')
print('both producer output guards passed')
""",
            id="producer-guards",
        ),
    ],
)
def test_second_squish_consumers_survive_native_worker_boundaries(
    control_snapshot: tuple[Path, set[Path]], program: str
) -> None:
    """Keep each consumer contract in its own fresh native worker."""
    tree, _copied = control_snapshot
    _run_second_squish_native_program(tree, program)


@pytest.mark.parametrize(
    ("prefix", "name"),
    [
        pytest.param(
            "SQUISH update -",
            "SQUISH update - a different source revision cannot inherit the reviewed replay",
            id="first-source-revision",
        ),
        pytest.param(
            "SQUISH update -",
            "SQUISH update - an unsafe published decimal cannot inherit the exact bound",
            id="first-unsafe-decimal",
        ),
        pytest.param(
            "SQUISH second update -",
            "SQUISH second update - a different revision cannot inherit the complete replay",
            id="second-source-revision",
        ),
        pytest.param(
            "SQUISH second update -",
            (
                "SQUISH second update - unchanged geometry with a wrong canonical "
                "witness ID is refused"
            ),
            id="second-canonical-id",
        ),
    ],
)
def test_squish_private_mutation_is_detected_and_restored_in_native_worker(
    control_snapshot: tuple[Path, set[Path]], prefix: str, name: str
) -> None:
    """Each registered fault runs in a fresh native process and restores its private target."""
    tree, _copied = control_snapshot
    work = tree / HERE
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())
    selected = [c for c in specification["controls"] if c["name"].startswith(prefix)]
    assert len(selected) == 2
    matches = [control for control in selected if control["name"] == name]
    assert len(matches) == 1
    control = matches[0]
    target = resolve_control_target(control["file"], tree=tree, work=work)
    before = target.read_bytes()
    source = ROOT / control["file"]
    source_before = source.read_bytes()
    passed, detail = controls.run_one(control, tree)
    assert passed, detail
    assert target.read_bytes() == before
    assert source.read_bytes() == source_before


def _gupta_worker_program() -> str:
    """The actual custody child; literal escapes must survive serialization."""
    return r"""
import copy
from fractions import Fraction
from devtools import build_known_best_atlas as atlas
from devtools import check_results
from devtools import gupta_house_links as house
from devtools import register_gupta_reports as register
reports = house.reports
def forbidden(*args, **kwargs):
    raise AssertionError('custody admission must not call a geometric decider')
reports.kernel.run_case = reports.run_child = forbidden
reports.legacy.exact_verify = reports.legacy.independent.check_squares = forbidden
assert tuple(reports.check_certification()) == reports.NUMBERS
assert sum(len(c.poses) for c in reports.read_facts().values()) == 3017
assert len(register.read_history()) == 14
house.check_houses()
for relative in (house.house_path(88), house.house_path(239)):
    name = relative.relative_to(house.REPO).as_posix()
    assert check_results.repository_file_problem(name) is None
for kind in ('native-verdict', 'complete-input', 'original', 'comparator'):
    deciding = kind in ('native-verdict', 'complete-input')
    target = reports.receipt_path() if deciding else reports.fact_path()
    original = target.read_bytes()
    value = copy.deepcopy(reports.kernel.read_xz(target))
    row = value['cases'][-1]
    if kind == 'native-verdict':
        assert row['exact_verify']['verification_passed'] is False
        row['exact_verify']['verification_passed'] = True
    elif kind == 'complete-input':
        x = row['checker_input']['poses'][-1][0]
        row['checker_input']['poses'][-1][0] = str(Fraction(x) + 1)
    elif kind == 'original':
        row['source_certificate'] += '\n'
    else:
        row['source_comparator'] += '\n'
    try:
        reports.save_xz(target, value)
        try:
            house.check_houses()
        except reports.kernel.ReportError:
            pass
        else:
            raise AssertionError('private deciding input mutant was admitted: ' + kind)
    finally:
        target.write_bytes(original)
    house.check_houses()
    assert target.read_bytes() == original
producers = (atlas.update, lambda: atlas.update_selected([88]),
             lambda: atlas.update_selected([239]))
for producer in producers:
    try:
        producer()
    except ValueError as error:
        assert 'output escapes' in str(error)
    else:
        raise AssertionError('producer accepted a linked Gupta output')
print('all 17 sources/3017 poses/51 jobs/four private inputs/14 houses admitted; '
      'native verdict, complete input, original and comparator mutants refused/restored; '
      'all producer guards passed without deciders')
"""


def test_gupta_worker_program_compiles() -> None:
    compile(_gupta_worker_program(), "gupta-custody-child", "exec")


@pytest.mark.slow
def test_gupta_complete_sources_survive_native_worker_boundaries(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    """Use the actual shared copier, all four private inputs and live refusal/restores."""
    from devtools import gupta_house_links as house  # noqa: PLC0415

    assert snapshot_source_bytes() <= SNAPSHOT_MAX_BYTES
    tree, _copied = control_snapshot
    inputs = house.private_input_paths()
    assert len(inputs) == 4
    original_inputs = {path: path.read_bytes() for path in inputs}
    for source, original in original_inputs.items():
        target = tree / source.relative_to(controls.REPO)
        assert target.is_file()
        assert not target.is_symlink()
        assert target.read_bytes() == original
    for source in house.snapshot_house_links():
        target = tree / source.relative_to(controls.REPO)
        assert target.is_symlink()
        assert target.resolve() == source.resolve()
        with pytest.raises(ValueError, match="escapes private snapshot"):
            resolve_control_target(
                source.relative_to(ROOT).as_posix(), tree=tree, work=tree / HERE
            )
    program = _gupta_worker_program()
    completed = subprocess.run(
        [sys.executable, "-c", program],
        cwd=tree / HERE,
        env=controls.control_environment(tree, tree / "gupta-custody-pycache"),
        capture_output=True,
        text=True,
        check=False,
        timeout=45,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "all 17 sources/3017 poses/51 jobs/four private inputs/14 houses" in completed.stdout
    for source, original in original_inputs.items():
        assert source.read_bytes() == original
        assert (tree / source.relative_to(controls.REPO)).read_bytes() == original
    assert snapshot_source_bytes() <= SNAPSHOT_MAX_BYTES


@pytest.mark.parametrize(
    ("number", "canonical"),
    [
        (136, "paired-cover"),
        (140, "owner-footprint-cover"),
        (142, "owner-footprint-cover"),
        (143, "four-owner-footprint-cover"),
        (144, "four-owner-endpoint-full-net-replay"),
    ],
)
def test_duplicate_stdout_prune_preserves_canonical_and_declared_input(
    number: int, canonical: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Historical duplicate output may leave a worker, never its required input."""
    relative = "campaign/series/series-000-smoke-and-calibration/results/agenda-032"
    extension = "json" if number == 136 else "jsonl"
    output = ROOT / relative / f"exp-{number}-stdout.{extension}"
    retained = output.with_name(f"exp-{number}-{canonical}.json")
    assert output in PRUNE
    assert not controls.in_pruned_roots(retained, PRUNE)
    source_names = [path.relative_to(controls.REPO).as_posix() for path in (output, retained)]
    blobs = [
        subprocess.run(
            ["git", "rev-parse", f"HEAD:{name}"],
            cwd=controls.REPO,
            capture_output=True,
            check=True,
            timeout=10,
        ).stdout
        for name in source_names
    ]
    assert blobs[0] == blobs[1]
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())
    for control in specification["controls"]:
        assert (ROOT / control["file"]).resolve() != output
        assert output.name not in control["run"]
    packing = tmp_path / "packing"
    receipt = packing / relative / output.name
    receipt.parent.mkdir(parents=True)
    receipt.write_text('{"duplicate":true}\n')
    scientific = receipt.with_name(retained.name)
    scientific.write_bytes(receipt.read_bytes())
    document = tmp_path / "SYNOPSIS.md"
    document.write_text(f"[declared input](packing/{relative}/{receipt.name})\n")
    monkeypatch.setattr(controls, "ROOT", packing)
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", (document,))
    monkeypatch.setattr(controls, "PRUNE", frozenset({receipt}))
    monkeypatch.setattr(controls, "LINKED_PRUNE_ROOTS", (receipt,))
    monkeypatch.setattr(controls, "COPY_SEPARATELY", ())
    monkeypatch.setattr(controls, "root_files", lambda: ())
    monkeypatch.setattr(controls, "result_pruned_targets", list)
    assert controls.snapshot_pruned_targets() == [receipt]
    assert controls.snapshot_source_bytes() == sum(
        path.stat().st_size for path in (document, receipt, scientific)
    )


@pytest.mark.parametrize("declaration", ["inline", "frontier", "none"])
@pytest.mark.parametrize("explicit", [False, True])
def test_git_projection_preserves_sparse_declared_inputs(
    declaration: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, explicit: bool
) -> None:
    """Absent sparse files still count; genuine declarations rescue exact outputs."""
    packing = tmp_path / "packing"
    output = packing / "results/duplicate.json"
    output.parent.mkdir(parents=True)
    output.write_bytes(b"diagnostic output")
    canonical = output.with_name("canonical.json")
    canonical.write_bytes(output.read_bytes())
    regularized = packing / "atlas/known-best/regularized/n-011-regularized.yaml.gz"
    regularized.parent.mkdir(parents=True)
    regularized.write_bytes(b"generated witness")
    index = regularized.with_name("index.json")
    index.write_text('{"source":true}\n')
    source = packing / "source.py"
    source.write_text("source = True\n")
    document = tmp_path / "README.md"
    document.write_text(
        "[input](packing/results/duplicate.json)\n" if declaration == "inline" else "Reader\n"
    )
    register = packing / "frontier/results.yaml"
    register.parent.mkdir()
    register.write_text(
        "results:\n- artifacts: [packing/results/duplicate.json]\n"
        if declaration == "frontier"
        else "results: []\n"
    )
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True, timeout=10)
    subprocess.run(["git", "-C", str(tmp_path), "add", "."], check=True, timeout=10)
    tree = (
        subprocess.run(
            ["git", "-C", str(tmp_path), "write-tree"],
            check=True,
            capture_output=True,
            timeout=10,
        )
        .stdout.decode()
        .strip()
    )
    expected = sum(
        path.stat().st_size for path in (canonical, source, document, register, index)
    )
    if explicit or declaration != "none":
        expected += output.stat().st_size
    output.unlink()
    canonical.unlink()
    document.unlink()
    regularized.unlink()
    index.unlink()
    monkeypatch.setattr(controls, "REPO", tmp_path)
    monkeypatch.setattr(controls, "ROOT", packing)
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", (document,))
    monkeypatch.setattr(controls, "PRUNE", frozenset({output}))
    monkeypatch.setattr(controls, "LINKED_PRUNE_ROOTS", (output,))
    monkeypatch.setattr(controls, "COPY_SEPARATELY", (output,) if explicit else ())
    assert controls.snapshot_git_source_bytes(tree) == expected


def test_snapshot_prunes_leave_native_crate_fixtures_selected() -> None:
    """The cap repair cannot drop PR410's native source, tests or data fixtures."""
    listed = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "HEAD", "packing/n17_kernel_verify"],
        cwd=controls.REPO,
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout.splitlines()
    assert listed
    for relative in listed:
        path = controls.REPO / relative
        assert not controls.in_pruned_roots(path, PRUNE)


def _couzo_worker_program() -> str:
    """All source/native mutations happen in the actual private snapshot, without decisions."""
    return r"""
import copy
from fractions import Fraction
from pathlib import Path
from devtools import couzo_refinement_reports as reports
def forbidden(*args, **kwargs):
    raise AssertionError('custody must not run a native geometric decision')
reports.kernel.run_case = reports.run_child = forbidden
reports.legacy.exact_verify = reports.legacy.independent.check_squares = forbidden
assert tuple(reports.check_certification()) == reports.NUMBERS
assert sum(len(c.poses) for c in reports.read_facts().values()) == 1340
assert len(reports.kernel.read_xz(reports.receipt_path())['cases']) == 24
for kind in ('native-verdict', 'native-limitations', 'complete-input',
             'original', 'decimal', 'map'):
    deciding = kind in ('native-verdict', 'native-limitations', 'complete-input')
    target = reports.receipt_path() if deciding else reports.fact_path()
    if kind == 'map':
        target = reports.PACKET / 'acquisition/case-inputs.json'
    original = target.read_bytes()
    try:
        if kind == 'map':
            target.write_bytes(original + b'\n')
        else:
            value = copy.deepcopy(reports.kernel.read_xz(target))
            row = value['cases'][-1]
            if kind == 'native-verdict':
                assert row['exact_verify']['verification_passed'] is False
                row['exact_verify']['verification_passed'] = True
            elif kind == 'native-limitations':
                row['independent']['limitations'] = 'Global optimality is proved.'
            elif kind == 'complete-input':
                x = row['checker_input']['poses'][-1][0]
                row['checker_input']['poses'][-1][0] = str(Fraction(x) + 1)
            elif kind == 'original':
                row['source_certificate'] += '\n'
            else:
                row['decimal_pose'] += '\n'
            reports.kernel.save_xz(target, value)
        try:
            reports.check_certification()
        except reports.kernel.ReportError:
            pass
        else:
            raise AssertionError('private deciding mutant was admitted: ' + kind)
    finally:
        target.write_bytes(original)
    assert tuple(reports.check_certification()) == reports.NUMBERS
    assert target.read_bytes() == original
outside = reports.REPO.parent / 'couzo-custody-output-target'
for target, producer in ((reports.fact_path(), reports.import_facts),
                        (reports.receipt_path(), lambda: reports.certify(Path('unused-jobs')))):
    original = target.read_bytes()
    outside.write_bytes(original)
    target.unlink()
    target.symlink_to(outside)
    try:
        try:
            producer()
        except reports.kernel.ReportError as error:
            assert 'must remain private' in str(error)
        else:
            raise AssertionError('producer accepted output outside private snapshot')
        assert outside.read_bytes() == original
    finally:
        target.unlink()
        target.write_bytes(original)
        outside.unlink()
assert tuple(reports.check_certification()) == reports.NUMBERS
print('all8 sources/1340poses/24jobs/three private inputs admitted; '
      'six late mutants refused/restored and both producer escapes refused without deciders')
"""


def test_couzo_worker_program_compiles() -> None:
    compile(_couzo_worker_program(), "couzo-custody-child", "exec")


def test_couzo_complete_sources_survive_native_worker_boundaries(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    """The production copier must carry all full deciding inputs as ordinary private files."""
    from devtools import couzo_refinement_reports as reports  # noqa: PLC0415

    assert snapshot_source_bytes() <= SNAPSHOT_MAX_BYTES
    tree, _copied = control_snapshot
    inputs = reports.private_input_paths()
    assert len(inputs) == 3
    assert set(inputs) <= set(controls.COPY_SEPARATELY)
    originals = {path: path.read_bytes() for path in inputs}
    for source, original in originals.items():
        target = tree / source.relative_to(controls.REPO)
        assert target.is_file()
        assert not target.is_symlink()
        assert target.read_bytes() == original
    program = _couzo_worker_program()
    compile(program, "couzo-custody-child", "exec")
    completed = subprocess.run(
        [sys.executable, "-c", program],
        cwd=tree / HERE,
        env=controls.control_environment(tree, tree / "couzo-custody-pycache"),
        capture_output=True,
        text=True,
        check=False,
        timeout=45,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "all8 sources/1340poses/24jobs/three private inputs admitted" in completed.stdout
    for source, original in originals.items():
        assert source.read_bytes() == original
        assert (tree / source.relative_to(controls.REPO)).read_bytes() == original
    assert snapshot_source_bytes() <= SNAPSHOT_MAX_BYTES
