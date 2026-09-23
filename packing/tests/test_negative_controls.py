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
from devtools.check_readme import NO_INDEX
from devtools.repo_scope import tracked_files
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
    "node_modules",
    "nested/dist",
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
    assert snapshot_source_bytes() < SNAPSHOT_MAX_BYTES


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
    repository = {name.decode() for name in names if name and (tree / name.decode()).is_file()}
    assert tracked == repository

    # The linked-back environment and cargo target are the real checkout's, not this
    # snapshot's content, which is why the index is built before they are symlinked in.
    assert not any(
        name.startswith(("packing/.venv", "packing/sqsearch/target")) for name in tracked
    )


def test_the_readme_check_reads_the_directory_inside_a_worker(
    control_snapshot: tuple[Path, set[Path]],
) -> None:
    """The README controls rehearse drift, so the check must get past "no index" here.

    `check_readme` is not green in a worker and is not expected to be: the snapshot
    carries a bounded source surface, so the layout tree draws root-level tooling the
    snapshot does not hold. What must not appear is the refusal, which is what the four
    README controls got instead of the drift they mutate for.
    """
    tree, _copied = control_snapshot
    work = tree / HERE
    completed = subprocess.run(
        [sys.executable, "-m", "devtools.check_readme"],
        cwd=work,
        env={
            **os.environ,
            "PYTHONPATH": os.pathsep.join((str(work / "src"), str(work))),
        },
        capture_output=True,
        text=True,
        check=False,
    )
    assert NO_INDEX not in completed.stdout + completed.stderr


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
