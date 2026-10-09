"""Failure-path contracts for isolated mutation-control subprocesses."""

from __future__ import annotations

import cProfile
import hashlib
import inspect
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable
from datetime import datetime, timedelta
from pathlib import Path
from types import ModuleType
from typing import Any

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


def index_fixture_source(repository: Path) -> None:
    """Give a synthetic source the same tracked-set boundary as the real checkout."""
    environment = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    for arguments in (("init", "-q"), ("add", "--", ".")):
        subprocess.run(
            ("git", "-C", str(repository), *arguments),
            check=True,
            capture_output=True,
            env=environment,
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
    assert {
        ROOT
        / "campaign/explorations/X048-session-177-cached-collision/receipts"
        / "J-fixed-tuple-certificate.json",
        ROOT
        / "campaign/explorations/X048-session-178-full-core-ablation/receipts"
        / "B-ablation-packet.json",
    } <= set(COPY_SEPARATELY)
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


def _native_profile_inputs(tmp_path: Path) -> tuple[Path, Path, Path]:
    tree = tmp_path / "private tree"
    (tree / "packing/src").mkdir(parents=True)
    (tree / ".git").mkdir()
    (tree / ".git/index").write_bytes(b"private index")
    script = tmp_path / "native child.py"
    script.write_text("print('native child')\n")
    return script, tree, tmp_path / "diagnostic.json"


def _native_profile_arguments(script: Path, tree: Path, output: Path) -> list[str]:
    return [
        "--profile-native-script",
        str(script),
        "--profile-tree",
        str(tree),
        "--profile-output",
        str(output),
    ]


@pytest.mark.parametrize("mask", range(1, 7))
def test_native_profile_rejects_partial_flags_before_execution(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, mask: int
) -> None:
    inputs = _native_profile_inputs(tmp_path)
    flags = _native_profile_arguments(*inputs)
    selected = [
        value
        for index in range(3)
        if mask & (1 << index)
        for value in flags[index * 2 : index * 2 + 2]
    ]
    monkeypatch.setattr(
        controls, "run_control_command", lambda *_args, **_kwargs: pytest.fail("child ran")
    )
    with pytest.raises(SystemExit) as error:
        controls.main(selected)
    assert error.value.code == 2
    assert not inputs[2].exists()


@pytest.mark.parametrize("existing", ["json", "raw"])
def test_native_profile_refuses_existing_evidence_without_launch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, existing: str
) -> None:
    script, tree, output = _native_profile_inputs(tmp_path)
    destination = output if existing == "json" else output.with_suffix(".prof")
    destination.write_bytes(b"prior evidence")
    monkeypatch.setattr(
        controls, "run_control_command", lambda *_args, **_kwargs: pytest.fail("child ran")
    )
    with pytest.raises(SystemExit) as error:
        controls.main(_native_profile_arguments(script, tree, output))
    assert error.value.code == 2
    assert destination.read_bytes() == b"prior evidence"
    assert not (output.with_suffix(".prof") if existing == "json" else output).exists()


@pytest.mark.parametrize("invalid", ["script", "tree", "index"])
def test_native_profile_rejects_invalid_inputs_before_launch(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, invalid: str
) -> None:
    script, tree, output = _native_profile_inputs(tmp_path)
    if invalid == "script":
        script.unlink()
    elif invalid == "tree":
        tree = tmp_path / "missing tree"
    else:
        (tree / ".git/index").unlink()
    monkeypatch.setattr(
        controls, "run_control_command", lambda *_args, **_kwargs: pytest.fail("child ran")
    )
    with pytest.raises(SystemExit) as error:
        controls.main(_native_profile_arguments(script, tree, output))
    assert error.value.code == 2
    assert not output.exists()


@pytest.mark.parametrize("status", ["success", "failure", "timeout"])
def test_native_profile_uses_private_child_runner_and_preserves_outcomes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    status: str,
) -> None:
    script, tree, output = _native_profile_inputs(tmp_path)
    monkeypatch.setattr(controls, "timing_provenance", lambda: {"source_revision": "fixture"})
    monkeypatch.setenv("PACKING_VALIDATION_ARTIFACT_DIR", str(tmp_path / "parent artifacts"))
    calls = []

    def command(text: str, **kwargs: Any) -> controls.CommandOutcome:
        calls.append(text)
        arguments = shlex.split(text)
        assert arguments[:2] == [sys.executable, "-c"]
        assert arguments[3:] == [str(script), str(output.with_suffix(".prof"))]
        assert kwargs["cwd"] == tree / "packing"
        assert kwargs["timeout_seconds"] == 60.0
        environment = kwargs["environment"]
        assert environment["PYTHONDONTWRITEBYTECODE"] == "1"
        assert environment["PYTHONPATH"].split(os.pathsep)[:2] == [
            str(tree / "packing/src"),
            str(tree / "packing"),
        ]
        assert "PACKING_VALIDATION_ARTIFACT_DIR" not in environment
        native = subprocess.run(
            arguments,
            cwd=kwargs["cwd"],
            env=environment,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        assert native.returncode == 0
        assert native.stdout == "native child\n"
        assert not native.stderr
        return controls.CommandOutcome(
            0 if status == "success" else 3,
            "child stdout\n",
            "child stderr\n",
            timed_out=status == "timeout",
        )

    monkeypatch.setattr(controls, "run_control_command", command)
    assert controls.main(_native_profile_arguments(script, tree, output)) == (
        0 if status == "success" else 1
    )
    assert len(calls) == 1
    report = json.loads(output.read_text())
    assert report["complete"] == (status == "success")
    assert report["timed_out"] == (status == "timeout")
    assert report["returncode"] == (0 if status == "success" else 3)
    assert report["diagnostic_only"] is True
    assert report["gate_credit"] is False
    assert report["duration_seconds"] >= 0
    assert report["top_cumulative"]
    assert report["stdout"] == "child stdout\n"
    assert report["stderr"] == "child stderr\n"
    assert report["script"]["sha256"] == hashlib.sha256(script.read_bytes()).hexdigest()
    assert (
        report["tree"]["private_index_sha256"]
        == hashlib.sha256((tree / ".git/index").read_bytes()).hexdigest()
    )
    captured = capsys.readouterr()
    assert "child stdout" in captured.out
    assert "child stderr" in captured.err


def test_native_profile_imports_only_the_intended_private_tree(tmp_path: Path) -> None:
    script, tree, output = _native_profile_inputs(tmp_path)
    assert tree / "packing" != controls.ROOT
    package = tree / "packing/devtools"
    package.mkdir()
    (package / "__init__.py").write_text("")
    (package / "view_marker.py").write_text(
        "from pathlib import Path\nROOT = Path(__file__).resolve().parents[1]\n"
    )
    script.write_text(
        "from pathlib import Path\nfrom devtools.view_marker import ROOT\n"
        "assert ROOT == Path.cwd()\nprint('intended private tree')\n"
    )
    assert controls.main(_native_profile_arguments(script, tree, output)) == 0
    report = json.loads(output.read_text())
    assert report["complete"] is True
    assert report["returncode"] == 0
    assert "intended private tree" in report["stdout"]
    assert report["top_cumulative"]


def test_native_profile_retains_same_named_functions_at_distinct_locations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    script, tree, output = _native_profile_inputs(tmp_path)
    monkeypatch.setattr(controls, "timing_provenance", dict)

    def command(_text: str, **_kwargs: object) -> controls.CommandOutcome:
        cheap: dict[str, Any] = {}
        costly: dict[str, Any] = {}
        body = "def repeated():\n    return sum(range({count}))\n"
        exec(compile(body.format(count=100), "cheap.py", "exec"), cheap)
        exec(compile(body.format(count=100000), "costly.py", "exec"), costly)
        profile = cProfile.Profile()
        profile.runcall(cheap["repeated"])
        profile.runcall(costly["repeated"])
        profile.dump_stats(output.with_suffix(".prof"))
        return controls.CommandOutcome(0, "", "")

    monkeypatch.setattr(controls, "run_control_command", command)
    assert controls.main(_native_profile_arguments(script, tree, output)) == 0
    report = json.loads(output.read_text())
    rows = [row for row in report["top_cumulative"] if row["function"] == "repeated"]
    assert [(row["file"], row["line"]) for row in rows] == [("costly.py", 1), ("cheap.py", 1)]
    assert rows[0]["cumulative_seconds"] > rows[1]["cumulative_seconds"]
    assert all(row["calls"] == row["primitive_calls"] == 1 for row in rows)
    assert all(isinstance(row["self_seconds"], float) for row in rows)


@pytest.mark.parametrize(
    ("exception", "returncode"),
    [
        ("SystemExit(3)", 3),
        ("ValueError('native value failure')", 1),
        ("OSError('native OS failure')", 1),
    ],
)
def test_native_profile_real_child_failure_retains_profile_and_output(
    tmp_path: Path, exception: str, returncode: int
) -> None:
    script, tree, output = _native_profile_inputs(tmp_path)
    script.write_text(
        "import sys\nfrom pathlib import Path\n"
        "assert sys.argv == [__file__]\nassert sys.path[0] == str(Path.cwd())\n"
        "print('before failure')\nprint('native error', file=sys.stderr)\n"
        f"raise {exception}\n"
    )
    assert controls.main(_native_profile_arguments(script, tree, output)) == 1
    report = json.loads(output.read_text())
    assert report["returncode"] == returncode
    assert report["complete"] is False
    assert "before failure" in report["stdout"]
    assert "native error" in report["stderr"]
    if returncode == 1:
        assert "Traceback" in report["stderr"]
        assert exception.split("(", maxsplit=1)[0] in report["stderr"]
        assert "usage:" not in report["stderr"]
    assert report["top_cumulative"]
    assert output.with_suffix(".prof").stat().st_size > 0


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


def test_pruned_historical_family_copyback_keeps_bytes_and_omits_bulk(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The exact historical consumer survives a pruned agenda without its bulk."""
    source = controls.SESSION184_RESULTS / "agenda-040/exp-214-n13-399-100-family.json"
    assert source in COPY_SEPARATELY
    packing = tmp_path / "source/packing"
    agenda = packing / "campaign/results/agenda-040"
    agenda.mkdir(parents=True)
    family = agenda / source.name
    family.write_bytes(source.read_bytes())
    bulk = agenda / "unneeded-inventory.json"
    bulk.write_text("unneeded generated output\n")
    monkeypatch.setattr(controls, "ROOT", packing)
    monkeypatch.setattr(controls, "REPO", packing.parent)
    monkeypatch.setattr(controls, "PRUNE", frozenset({agenda}))
    monkeypatch.setattr(controls, "DESCEND", frozenset(agenda.parents))
    monkeypatch.setattr(controls, "COPY_SEPARATELY", (family,))
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", ())
    monkeypatch.setattr(controls, "LINK_BACK", ())
    monkeypatch.setattr(controls, "root_files", lambda: ())
    monkeypatch.setattr(controls, "snapshot_pruned_targets", list)
    monkeypatch.setattr(controls, "linked_pruned_directories", list)
    monkeypatch.setattr(controls, "index_tree", lambda _tree: None)
    tree = tmp_path / "worker"
    controls.clone_tree(tree)
    landed = tree / family.relative_to(packing.parent)
    assert landed.read_bytes() == family.read_bytes() == source.read_bytes()
    assert not (tree / bulk.relative_to(packing.parent)).exists()


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
    index_fixture_source(source_repo)

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


def test_unread_worker_outputs_leave_workers_while_declared_files_return(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    """The 2026-10-09 selection, partitioned file by file as the 2026-10-06 prune is.

    No control reaches an entry, as a mutation target or by naming one in a command.
    Every file under each entry is either absent from the worker or, when a checked
    document links it or the results register lists it, present byte for byte; and
    every entry still sends something out of the worker. The linked audit directories
    arrive even where their contents do not, so the ledger's link scan still finds them.
    """
    tree, copied_targets = control_snapshot
    assert controls.UNREAD_WORKER_OUTPUTS <= PRUNE
    spec = safe_load((ROOT / "devtools/controls.yaml").read_text(encoding="utf-8"))
    for entry in sorted(controls.UNREAD_WORKER_OUTPUTS):
        assert entry.exists(), "evidence must remain in the source checkout"
        packing_relative = entry.relative_to(ROOT).as_posix()
        for control in spec["controls"]:
            target = (ROOT / control["file"]).resolve()
            assert not controls.in_pruned_roots(target, frozenset({entry}))
            assert packing_relative not in control["run"]
        sources = [entry] if entry.is_file() else sorted(entry.rglob("*"))
        sources = [path for path in sources if path.is_file()]
        assert sources
        left = 0
        for source in sources:
            relative = source.relative_to(controls.REPO)
            copied = tree / relative
            if relative in copied_targets:
                assert copied.read_bytes() == source.read_bytes()
            else:
                assert not copied.exists(), relative
                left += 1
        assert left, f"{packing_relative}: every file returns, so the entry prunes nothing"

    results = ROOT / "campaign/series/series-000-smoke-and-calibration/results"
    for relative in (
        "exp-249-n17-first-certified-sub-patterns/census.json",
        "exp-246-n17-capacity-one-cover/audit/wall_lemma.py.txt",
        "chelokot-lean-replay/receipt.json",
    ):
        source = results / relative
        assert source.relative_to(controls.REPO) in copied_targets
        assert (tree / source.relative_to(controls.REPO)).read_bytes() == source.read_bytes()
    # exp-295 keeps its descriptor and metadata, as exp-297--314 do.
    for name in ("README.md", "descriptor.json", "mechanical-summary.json"):
        source = results / "exp-295-two-center-children" / name
        assert (tree / source.relative_to(controls.REPO)).read_bytes() == source.read_bytes()
    for relative in (
        "exp-249-n17-first-certified-sub-patterns/audit-A",
        "exp-249-n17-first-certified-sub-patterns/audit-W7",
        "exp-247-n17-unique-state-cover/audit",
    ):
        assert (tree / (results / relative).relative_to(controls.REPO)).is_dir()
    # The annealing record itself stays; only its bulk summary leaves.
    record = ROOT / "campaign/results/annealing/README.md"
    assert (tree / record.relative_to(controls.REPO)).read_bytes() == record.read_bytes()
    assert snapshot_source_bytes() < SNAPSHOT_MAX_BYTES


def test_math_startup_reports_are_pruned_but_record_sources_survive(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    tree, copied_targets = control_snapshot
    campaign = ROOT / "benchmarks/math-startup"
    # The historical review is retained, but no registered worker link checker
    # follows its outgoing links. These five primary observations stay in Git;
    # their 2,739,207 bytes no longer undo the already-declared run-output prune.
    historical_run = campaign / "runs/ci-34774787868"
    for name in (
        "index.html.gz",
        "reference.pdf",
        "replay.pdf",
        "provenance.json",
        "report.txt",
    ):
        source = historical_run / name
        assert source.is_file()
        relative = source.relative_to(controls.REPO)
        assert relative not in copied_targets
        assert not (tree / relative).exists()
    review = (
        controls.REPO / "docs/project/reviews/review-2026-09-13-explainer-pdf-comparison.md"
    )
    assert (tree / review.relative_to(controls.REPO)).read_bytes() == review.read_bytes()
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
    index_fixture_source(tmp_path)
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


@pytest.mark.parametrize(
    "selection", ["session184", "baseline", "retained", "operational", "historical_census"]
)
def test_research_outputs_are_pruned_but_linked_evidence_still_counts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, selection: str
) -> None:
    roots = (
        controls.SESSION184_RESULT_ROOTS
        if selection == "session184"
        else frozenset(
            {
                *(
                    ROOT / "campaign/explorations" / name
                    for name in (
                        "X048-session-169-pilots",
                        "X048-session-170-compatibility",
                        "X048-session-171-raw-row-support",
                        "X048-session-172-capacity-support",
                        "X048-session-174-core-refinement",
                        "X048-session-175-enhanced-support",
                        "X048-session-176-owner-priority",
                        "X048-session-177-cached-collision",
                        "X048-session-178-full-core-ablation",
                        "X048-session-179-selective-halving",
                    )
                ),
                *(
                    controls.SESSION184_RESULTS / name
                    for name in (
                        "exp-242-n17-core-stress",
                        "exp-243-n17-charge-floor-pilot",
                        "exp-244-n17-local-minimum",
                        "exp-248-n17-local-half-composition",
                    )
                ),
            }
        )
    )
    if selection == "retained":
        roots = frozenset(
            ROOT / "campaign/retained" / name
            for name in (
                "session-184-n11-readiness",
                "session-184-tail-a-dependencies",
                "session-184-n17-numeric-cap-readiness",
            )
        )
    elif selection == "operational":
        roots = frozenset(
            {
                ROOT / "benchmarks/validation-efficiency/runs",
                ROOT / "campaign/agent-sessions/session-152-validation",
            }
        )
    elif selection == "historical_census":
        roots = frozenset(
            controls.SESSION184_RESULTS / name / "census.json"
            for name in (
                "exp-253-n17-stalls-under-adaptive-rows",
                "exp-254-n17-second-tranche-flags",
                "exp-256-n17-third-tranche-flags",
                "exp-257-n17-unsampled-strata",
                "exp-258-n17-draw-31",
            )
        )
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())
    assert roots <= PRUNE
    if selection == "session184":
        assert {
            controls.SESSION184_RESULTS / name
            for name in (
                "exp-278-centered-endpoint-standing",
                "exp-279-centered-endpoint-diagnostics",
                "exp-280-centered-endpoint-hull-capacity",
                "exp-281-conditional-owned-hull-gate",
                "exp-282-conditional-owned-hull-scoped-input",
                "exp-283-parent-guard-owned-hull",
                "exp-284-parent-guard-native-custody",
                "exp-285-pooled-parent-center-cases",
                "exp-286-pooled-forbidden-cover",
                "exp-287-pooled-relaxation-witness",
                "exp-288-pooled-feasible-center",
                "exp-289-complete-partner-coupling",
                "exp-290-matched-exact-replay",
                "exp-291-complete-partner-coupling-amended",
                "exp-292-full-square-partner-coupling",
                "exp-293-guard-conditioned-ownership",
                "exp-296-collective-row-coverage",
            )
        } <= roots
    for control in specification["controls"]:
        target = (ROOT / control["file"]).resolve()
        assert not controls.in_pruned_roots(target, roots)
        assert all(root.name not in control["run"] for root in roots)
        if selection == "operational":
            assert "validation_report" not in control["run"]

    packing = tmp_path / "packing"
    output = packing / "results/exp-268"
    output.mkdir(parents=True)
    needed = output / "required.json"
    needed.write_text('{"retained":true}\n')
    (output / "unreferenced-checkpoint.json").write_text("0" * 100_000)
    document = tmp_path / "SYNOPSIS.md"
    document.write_text("[required](packing/results/exp-268/required.json)\n")
    monkeypatch.setattr(controls, "ROOT", packing)
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", (document,))
    monkeypatch.setattr(controls, "PRUNE", frozenset({output}))
    monkeypatch.setattr(controls, "LINKED_PRUNE_ROOTS", (output,))
    monkeypatch.setattr(controls, "COPY_SEPARATELY", ())
    monkeypatch.setattr(controls, "root_files", lambda: ())
    monkeypatch.setattr(controls, "result_pruned_targets", list)
    assert controls.snapshot_pruned_targets() == [needed]
    assert controls.snapshot_source_bytes() == document.stat().st_size + needed.stat().st_size


@pytest.mark.parametrize(
    "name",
    [
        "exp-292-full-square-partner-coupling",
        "exp-293-guard-conditioned-ownership",
        "exp-296-collective-row-coverage",
    ],
)
def test_session185_selected_output_prune_is_exact_and_keeps_declared_inputs(
    name: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An exact output prune keeps sibling evidence and linked proof inputs."""
    assert controls.SESSION184_RESULTS / name in PRUNE
    packing = tmp_path / "packing"
    output = packing / "results" / name
    output.mkdir(parents=True)
    needed = output / "required.json"
    needed.write_text('{"proof_input":true}\n')
    (output / "unneeded.log").write_text("unused" * 100)
    sibling = output.with_name(name + "-other")
    sibling.mkdir()
    sibling_evidence = sibling / "unique.json"
    sibling_evidence.write_text('{"unique":true}\n')
    document = tmp_path / "SYNOPSIS.md"
    document.write_text(f"[required](packing/results/{name}/required.json)\n")
    monkeypatch.setattr(controls, "ROOT", packing)
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", (document,))
    monkeypatch.setattr(controls, "PRUNE", frozenset({output}))
    monkeypatch.setattr(controls, "LINKED_PRUNE_ROOTS", (output,))
    monkeypatch.setattr(controls, "COPY_SEPARATELY", ())
    monkeypatch.setattr(controls, "root_files", lambda: ())
    monkeypatch.setattr(controls, "result_pruned_targets", list)
    assert controls.snapshot_pruned_targets() == [needed]
    assert not controls.in_pruned_roots(sibling_evidence, frozenset({output}))
    assert controls.snapshot_source_bytes() == (
        document.stat().st_size + needed.stat().st_size + sibling_evidence.stat().st_size
    )


@pytest.mark.parametrize(
    "name",
    [
        "agenda-037",
        "agenda-040",
        "bc-201-n11-tight-cell-census.json",
        "bc-241-trump-local-theorem-review.json",
        "exp-053-h-057-n17-parent-bound-parallel-speedup.raw",
    ],
)
def test_session186_historical_prune_has_no_registered_control_consumer(name: str) -> None:
    path = controls.SESSION184_RESULTS / name
    assert path in PRUNE
    assert path.exists()
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())
    relative = path.relative_to(ROOT).as_posix()
    for control in specification["controls"]:
        assert not controls.in_pruned_roots(
            (ROOT / control["file"]).resolve(), frozenset({path})
        )
        assert relative not in control["run"]
    # The selection is exact, including a file whose sibling shares its prefix.
    assert not controls.in_pruned_roots(path.with_name(name + "-other"), frozenset({path}))


@pytest.mark.parametrize(
    "result_root",
    [
        "exp-297-regional-row-coverage",
        "exp-300-one-round-direct-regional-propagation",
        "exp-301-one-round-fixed-core-regional-propagation",
        "exp-307-owned-core-guarded-clause",
        "exp-308-n11-corner-cardinality",
        "exp-309-subpattern-relevance",
        "exp-312-saved-pose-incircles",
        "exp-313-incircle-projection-redundancy",
        "exp-314-incircle-disk-projection",
    ],
)
@pytest.mark.parametrize("name", ["certificate.json", "replay.json"])
def test_session186_regional_receipt_prune_is_exact_and_copyback_survives(
    result_root: str, name: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = controls.SESSION184_RESULTS / result_root / name
    assert source in PRUNE
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())
    for control in specification["controls"]:
        assert (ROOT / control["file"]).resolve() != source
        assert source.relative_to(ROOT).as_posix() not in control["run"]
    packing = tmp_path / "packing"
    output = packing / "results" / result_root
    output.mkdir(parents=True)
    receipt = output / name
    receipt.write_text('{"exact":true}\n')
    sibling = output / (name + ".other")
    sibling.write_text("unique sibling evidence\n")
    descriptor = output / "descriptor.json"
    descriptor.write_text('{"premise":true}\n')
    document = tmp_path / "SYNOPSIS.md"
    document.write_text(f"[declared input](packing/results/{output.name}/{name})\n")
    monkeypatch.setattr(controls, "ROOT", packing)
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", (document,))
    monkeypatch.setattr(controls, "PRUNE", frozenset({receipt}))
    monkeypatch.setattr(controls, "LINKED_PRUNE_ROOTS", (receipt,))
    monkeypatch.setattr(controls, "COPY_SEPARATELY", ())
    monkeypatch.setattr(controls, "root_files", lambda: ())
    monkeypatch.setattr(controls, "result_pruned_targets", list)
    assert controls.snapshot_pruned_targets() == [receipt]
    assert not controls.in_pruned_roots(sibling, frozenset({receipt}))
    assert controls.snapshot_source_bytes() == sum(
        path.stat().st_size for path in (document, receipt, sibling, descriptor)
    )


@pytest.mark.parametrize(
    "relative",
    [
        "campaign/series/series-000-smoke-and-calibration/results/exp-005-basin-entry.jsonl",
        (
            "campaign/series/series-000-smoke-and-calibration/results/"
            "exp-126-h099-complete-graph-candidate/packet.json"
        ),
        "campaign/agent-sessions/session-105-validation/fast-final-bdc28e89.json",
        "campaign/agent-sessions/session-105-validation/push-0e766bfd.json",
        *(
            "campaign/series/series-000-smoke-and-calibration/results/agenda-032/"
            f"exp-{number}-stdout.jsonl"
            for number in (140, 142, 143, 144)
        ),
        *(
            "campaign/series/series-000-smoke-and-calibration/results/"
            "exp-204-basin-hopping/" + name
            for name in (
                "D-basin-hop.jsonl",
                "D-multistart.jsonl",
                "D-basin-hop.trace.jsonl",
                "D-multistart.trace.jsonl",
            )
        ),
    ],
)
def test_session186_diagnostic_output_prune_preserves_declared_copyback(
    relative: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = ROOT / relative
    assert source in PRUNE
    assert source.is_file()
    if "agenda-032/" in relative:
        number = source.name.split("-")[1]
        suffix = (
            "four-owner-endpoint-full-net-replay"
            if number == "144"
            else "four-owner-footprint-cover"
            if number == "143"
            else "owner-footprint-cover"
        )
        canonical = source.with_name(f"exp-{number}-{suffix}.json")
        assert canonical not in PRUNE
        assert canonical.read_bytes() == source.read_bytes()
    if "session-105-validation" in relative:
        identity = source.with_name(source.stem + "-source.json")
        assert identity.is_file()
        assert identity not in PRUNE
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())
    for control in specification["controls"]:
        assert (ROOT / control["file"]).resolve() != source
        assert relative not in control["run"]
    packing = tmp_path / "packing"
    receipt = packing / relative
    receipt.parent.mkdir(parents=True)
    receipt.write_text('{"diagnostic":true}\n')
    sibling = receipt.with_name(receipt.name + ".other")
    sibling.write_text("retained sibling\n")
    document = tmp_path / "SYNOPSIS.md"
    document.write_text(f"[declared input](packing/{relative})\n")
    monkeypatch.setattr(controls, "ROOT", packing)
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", (document,))
    monkeypatch.setattr(controls, "PRUNE", frozenset({receipt}))
    monkeypatch.setattr(controls, "LINKED_PRUNE_ROOTS", (receipt,))
    monkeypatch.setattr(controls, "COPY_SEPARATELY", ())
    monkeypatch.setattr(controls, "root_files", lambda: ())
    monkeypatch.setattr(controls, "result_pruned_targets", list)
    assert controls.snapshot_pruned_targets() == [receipt]
    assert not controls.in_pruned_roots(sibling, frozenset({receipt}))
    assert controls.snapshot_source_bytes() == sum(
        path.stat().st_size for path in (document, receipt, sibling)
    )


def test_operational_run_prune_preserves_the_reviewed_instrument_copyback() -> None:
    root = ROOT / "benchmarks/validation-efficiency/runs"
    copied = [path for path in controls.snapshot_pruned_targets() if path.is_relative_to(root)]
    assert copied == [root / "instrument-v1.py.txt"]
    # Primary CI's report-corpus test still reads the original receipts and JUnit;
    # pruning is solely a worker-copy rule, not deletion or a test exclusion.
    assert (root / "receipts.jsonl").is_file()
    assert any(root.glob("*.junit.xml"))


def test_checkpoint_archive_prune_preserves_all_declared_consumer_copyback() -> None:
    root = ROOT / "benchmarks/validation-efficiency/checkpoints"
    assert root in PRUNE
    copied = [
        path.name for path in controls.snapshot_pruned_targets() if path.is_relative_to(root)
    ]
    assert copied == sorted(
        [
            "2026-09-06-integrated-fast.log",
            "2026-09-06-integrated-fast.manifest.json",
            "2026-09-06-integrated-fast.tar.gz",
            "2026-09-06-pre-main-integration.manifest.json",
            "2026-09-06-pre-main-integration.tar.gz",
            "VE-004-full-ed595fb6.tar.gz",
        ]
    )
    # Unused operational histories stay recoverable in the primary evidence tree.
    assert (root / "VE-004-control-1.tar.gz").is_file()
    assert (root / "VE-004-candidate-1.tar.gz").is_file()


def test_session_152_operational_prune_preserves_linked_pdf_evidence() -> None:
    root = ROOT / "campaign/agent-sessions/session-152-validation"
    assert root in PRUNE
    copied = {
        path.name for path in controls.snapshot_pruned_targets() if path.is_relative_to(root)
    }
    assert copied == {
        "pdf-d490-run-35784981711-reference.pdf",
        "pdf-d490-run-35784981711-replay.pdf",
        "pdf-d490-run-35784981711-report.txt",
        "pdf-d490-run-35784981711.md",
    }
    unused = root / "push-c26afc5-initial-artifacts.tar.gz"
    assert unused.is_file()
    assert unused.name not in copied


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


def test_snapshot_index_refuses_missing_source_index_before_git_mutation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(controls, "tracked_files", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(
        controls.subprocess, "run", lambda *_args, **_kwargs: pytest.fail("worker Git write")
    )
    with pytest.raises(ValueError, match="without the source tracked set"):
        controls.index_tree(Path("uncreated-worker"))


def test_snapshot_index_keeps_source_tracking_and_snapshot_mutated_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source, tree = tmp_path / "source", tmp_path / "worker"
    source.mkdir()
    tree.mkdir()
    environment = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    (source / "tracked source.py").write_text("original")
    (source / "pruned.py").write_text("not copied")
    for arguments in (("init", "-q"), ("add", "--", "tracked source.py", "pruned.py")):
        subprocess.run(("git", "-C", str(source), *arguments), check=True, env=environment)
    (tree / "tracked source.py").write_text("changed in snapshot")
    (tree / "untracked-output.json").write_text("{}")
    monkeypatch.setattr(controls, "REPO", source)
    controls.index_tree(tree)
    assert tracked_files(tree, ".") == [tree / "tracked source.py"]
    indexed = subprocess.run(
        ("git", "-C", str(tree), "show", ":tracked source.py"),
        check=True,
        capture_output=True,
        env=environment,
    )
    assert indexed.stdout == b"changed in snapshot"


@pytest.mark.parametrize("foreign_variable", ["GIT_INDEX_FILE", "GIT_DIR"])
def test_snapshot_index_ignores_foreign_git_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, foreign_variable: str
) -> None:
    source, foreign, tree = (tmp_path / name for name in ("source", "foreign", "worker"))
    environment = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    for repository in (source, foreign):
        repository.mkdir()
        subprocess.run(
            ("git", "-C", str(repository), "init", "-q"), check=True, env=environment
        )
    (source / "tracked source.py").write_text("original")
    (source / "pruned.py").write_text("not copied")
    (foreign / "untracked-output.json").write_text("{}")
    for repository, names in (
        (source, ("tracked source.py", "pruned.py")),
        (foreign, ("untracked-output.json",)),
    ):
        subprocess.run(
            ("git", "-C", str(repository), "add", "--", *names),
            check=True,
            env=environment,
        )
    source_index = (source / ".git/index").read_bytes()
    foreign_index = (foreign / ".git/index").read_bytes()
    tree.mkdir()
    (tree / "tracked source.py").write_text("changed in snapshot")
    (tree / "untracked-output.json").write_text("{}")
    monkeypatch.setattr(controls, "REPO", source)
    foreign_path = foreign / ".git"
    if foreign_variable == "GIT_INDEX_FILE":
        foreign_path /= "index"
    monkeypatch.setenv(foreign_variable, str(foreign_path))
    controls.index_tree(tree)
    assert tracked_files(tree, ".", environment=environment) == [tree / "tracked source.py"]
    indexed = subprocess.run(
        ("git", "-C", str(tree), "show", ":tracked source.py"),
        check=True,
        capture_output=True,
        env=environment,
    )
    assert indexed.stdout == b"changed in snapshot"
    assert (source / ".git/index").read_bytes() == source_index
    assert (foreign / ".git/index").read_bytes() == foreign_index
    assert os.environ[foreign_variable] == str(foreign_path)


def test_registry_python_uses_the_harness_interpreter(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PATH", os.pathsep.join(("/usr/bin", "/bin")))
    command = "python3 -c " + shlex.quote("import sys; print(sys.executable)")
    outcome = run_control_command(
        command,
        cwd=tmp_path,
        environment=controls.control_environment(tmp_path, tmp_path / "pycache"),
    )
    assert outcome.returncode == 0, outcome.stderr
    assert Path(outcome.stdout.strip()).resolve() == Path(sys.executable).resolve()


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
    """Exercise the production copy, real index, native readers and both live mutants."""
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
    baseline_program = """
from devtools import build_known_best_atlas as atlas
from devtools import check_results
from devtools import squish_second_update_confirmation as packet
from devtools import squish_second_update_house_links as house
def forbidden(*args, **kwargs):
    raise AssertionError('native admission must not execute a geometric decider')
packet.decide = packet.original.decide = forbidden
packet.original.exact_verify = packet.original.independent.check = forbidden
assert tuple(packet.check_certification()) == packet.NUMBERS
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
for path in (house.house_path(88), house.house_path(263), packet.certificate_path(88)):
    relative = path.relative_to(packet.REPO).as_posix()
    assert check_results.repository_file_problem(relative) is None
assert check_results.repository_file_problem('packing/witnesses/known-best/unrelated.yaml')
for producer in (atlas.update, lambda: atlas.update_selected([88])):
    try:
        producer()
    except packet.original.PacketError as error:
        assert 'output escapes' in str(error)
    else:
        raise AssertionError('producer accepted a linked output')
print('all 27 complete inputs admitted; all nine original houses admitted from '
      'current or full retained history; current selected owner reads and output guards passed')
"""
    environment = controls.control_environment(tree, tree / "second-squish-baseline-pycache")
    baseline = subprocess.run(
        [sys.executable, "-c", baseline_program],
        cwd=work,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )
    assert baseline.returncode == 0, baseline.stdout + baseline.stderr
    specification = safe_load((ROOT / "devtools/controls.yaml").read_text())
    selected = [
        control
        for control in specification["controls"]
        if control["name"].startswith("SQUISH second update -")
    ]
    assert len(selected) == 2
    for control in selected:
        source = ROOT / control["file"]
        original = source.read_bytes()
        passed, detail = controls.run_one(control, tree)
        assert passed, detail
        assert source.read_bytes() == original


def _guarded_second_squish_admission(packet: ModuleType) -> Callable[[], dict[int, Any]]:
    """Reuse one actual admission in one child while every admission premise is fixed."""
    from copy import deepcopy  # noqa: PLC0415
    from pathlib import Path  # noqa: PLC0415

    repository = packet.REPO
    resolved_repository = repository.resolve()
    modules = (packet, packet.original, packet.reported, packet.shared)
    admit = packet.admit_certification

    def frozen(value: Any) -> tuple[type, Any]:
        kind = type(value)
        if isinstance(value, dict):
            return kind, tuple((frozen(key), frozen(item)) for key, item in value.items())
        if isinstance(value, (list, tuple)):
            return kind, tuple(frozen(item) for item in value)
        if isinstance(value, (set, frozenset)):
            return kind, frozenset(frozen(item) for item in value)
        if callable(value) or isinstance(value, ModuleType):
            return kind, id(value)
        return kind, value

    def namespace(module: ModuleType) -> dict[str, Any]:
        return {
            name: frozen(value)
            for name, value in vars(module).items()
            if name != "__builtins__"
            and not (module is packet and name == "admit_certification")
        }

    namespaces = tuple(namespace(module) for module in modules)
    paths = (*packet.private_input_paths(), Path(packet.original.__file__))
    assert len(paths) == len(set(paths)), "admission fixture has duplicate inputs"
    resolved = tuple(path.resolve(strict=True) for path in paths)
    ceiling = max(
        packet.original.MAX_SOURCE_BYTES,
        packet.original.MAX_RECEIPT_BYTES,
        packet.MAX_REVIEW_ROSTER_BYTES,
    )

    def read(path: Path, expected_size: int | None = None) -> bytes:
        assert path.is_relative_to(repository), "admission fixture path changed"
        assert not path.is_symlink(), "admission fixture file custody changed"
        assert path.is_file(), "admission fixture file custody changed"
        assert path.resolve(strict=True).is_relative_to(resolved_repository), (
            "admission fixture input escaped"
        )
        for parent in path.parents:
            assert not parent.is_symlink(), "admission fixture parent custody changed"
            if parent == repository:
                break
        size = path.stat().st_size
        limit = ceiling if expected_size is None else expected_size
        assert size <= limit, "admission fixture input size changed"
        assert expected_size is None or size == expected_size, (
            "admission fixture input size changed"
        )
        with path.open("rb") as stream:
            data = stream.read(limit + 1)
        assert len(data) == size, "admission fixture input changed during read"
        return data

    captured = tuple(read(path) for path in paths)

    def unchanged() -> None:
        assert repository == packet.REPO, "admission fixture repository changed"
        assert packet.REPO.resolve() == resolved_repository, (
            "admission fixture repository changed"
        )
        assert packet.admit_certification is admit or packet.admit_certification is guarded, (
            "admission fixture callback changed"
        )
        assert tuple(namespace(module) for module in modules) == namespaces, (
            "admission fixture loaded functions or constants changed"
        )
        assert (*packet.private_input_paths(), Path(packet.original.__file__)) == paths, (
            "admission fixture input roster changed"
        )
        for path, target, raw in zip(paths, resolved, captured, strict=True):
            assert path.resolve(strict=True) == target, "admission fixture input path changed"
            assert read(path, len(raw)) == raw, "admission fixture input bytes changed"

    def guarded() -> dict[int, Any]:
        unchanged()
        return deepcopy(rows)

    unchanged()
    rows = admit()
    unchanged()
    assert tuple(rows) == packet.NUMBERS, "admission fixture lost complete nine-case scope"
    return guarded


@pytest.fixture
def guarded_admission_packet(tmp_path: Path) -> Any:
    """Tiny ordinary inputs exercise the guard without creating a worker snapshot."""
    packet: Any = ModuleType("guarded_packet")
    packet.REPO = tmp_path / "repo"
    packet.REPO.mkdir()
    packet.NUMBERS = (88, 92, 108, 113, 125, 131, 263, 269, 281)
    packet.MAX_REVIEW_ROSTER_BYTES = 128
    packet.REVISION = "retained-source"
    original: Any = ModuleType("guarded_original")
    original.MAX_SOURCE_BYTES = original.MAX_RECEIPT_BYTES = 128
    packet.original = original
    packet.reported = ModuleType("guarded_reported")
    packet.shared = ModuleType("guarded_shared")
    paths = []
    for n in packet.NUMBERS:
        path = packet.REPO / str(n) / "input"
        path.parent.mkdir()
        path.write_bytes(f"complete-input-{n}".encode())
        paths.append(path)
    trusted = packet.REPO / "trusted-adapter.py"
    trusted.write_bytes(b"trusted-adapter")
    packet.original.__file__ = str(trusted)
    packet.private_input_paths = lambda: tuple(paths)
    packet.read_fact = lambda n: {"n": n}
    packet.admit_certification = lambda: {
        n: {"case": {"n": n, "premise": ["retained"]}} for n in packet.NUMBERS
    }
    return packet


@pytest.mark.parametrize(
    "mutation",
    [
        "late-bytes",
        "larger-input",
        "trusted-adapter",
        "linked-file",
        "linked-parent",
        "input-roster",
        "loaded-function",
        "loaded-constant",
        "equal-valued-type",
    ],
)
def test_guarded_admission_refuses_changed_premises_and_accepts_restoration(
    guarded_admission_packet: Any, tmp_path: Path, mutation: str
) -> None:
    packet = guarded_admission_packet
    guarded = _guarded_second_squish_admission(packet)
    packet.admit_certification = guarded
    original = guarded()
    path = packet.private_input_paths()[-1]
    if mutation == "trusted-adapter":
        path = Path(packet.original.__file__)
    raw = path.read_bytes()
    outside = tmp_path / "outside"
    previous_paths = packet.private_input_paths
    previous_fact = packet.read_fact
    revision = packet.REVISION
    source_ceiling = packet.original.MAX_SOURCE_BYTES
    if mutation in {"late-bytes", "trusted-adapter"}:
        path.write_bytes(b"!" + raw[1:])
    elif mutation == "larger-input":
        path.write_bytes(raw + b"!")
    elif mutation == "linked-file":
        outside.write_bytes(raw)
        path.unlink()
        path.symlink_to(outside)
    elif mutation == "linked-parent":
        path.parent.rename(outside)
        path.parent.symlink_to(outside, target_is_directory=True)
    elif mutation == "input-roster":
        packet.private_input_paths = lambda: previous_paths()[:-1]
    elif mutation == "loaded-function":
        packet.read_fact = lambda n: {"changed": n}
    elif mutation == "equal-valued-type":
        packet.original.MAX_SOURCE_BYTES = float(source_ceiling)
    else:
        packet.REVISION = "changed-source"
    try:
        with pytest.raises(AssertionError, match="admission fixture"):
            guarded()
    finally:
        if mutation == "linked-file":
            path.unlink()
            path.write_bytes(raw)
        elif mutation == "linked-parent":
            path.parent.unlink()
            outside.rename(path.parent)
        elif mutation in {"late-bytes", "larger-input", "trusted-adapter"}:
            path.write_bytes(raw)
        packet.private_input_paths = previous_paths
        packet.read_fact = previous_fact
        packet.REVISION = revision
        packet.original.MAX_SOURCE_BYTES = source_ceiling
    restored = guarded()
    assert restored == original
    assert restored is not original
    restored[packet.NUMBERS[-1]]["case"]["premise"].append("changed-return")
    assert guarded() == original


def test_guarded_admission_refuses_an_input_changed_during_real_admission(
    guarded_admission_packet: Any,
) -> None:
    packet = guarded_admission_packet
    path = packet.private_input_paths()[-1]
    raw = path.read_bytes()
    actual = packet.admit_certification

    def changed() -> dict[int, Any]:
        rows = actual()
        path.write_bytes(b"!" + raw[1:])
        return rows

    packet.admit_certification = changed
    try:
        with pytest.raises(AssertionError, match="admission fixture input bytes changed"):
            _guarded_second_squish_admission(packet)
    finally:
        path.write_bytes(raw)
        packet.admit_certification = actual
    guarded = _guarded_second_squish_admission(packet)
    assert tuple(guarded()) == packet.NUMBERS


@pytest.mark.parametrize(
    "program",
    [
        pytest.param(
            """
from devtools import squish_second_update_house_links as house
packet.admit_certification = _guarded_second_squish_admission(packet)
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
    gupta_module = "packing/devtools/register_gupta_reports.py"
    expected_gupta_module = (controls.REPO / gupta_module).is_file()
    program = (
        f"assert (packet.REPO / {gupta_module!r}).is_file() is {expected_gupta_module!r}\n"
        + program
    )
    program = (
        "from collections.abc import Callable\n"
        "from types import ModuleType\nfrom typing import Any\n"
        + inspect.getsource(_guarded_second_squish_admission)
        + "\n"
        + program
    )
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
