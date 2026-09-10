"""Contract tests for the prospective unit-parent experiment runner."""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import cast
from unittest.mock import patch

import pytest

from devtools.owner_footprints import DirectionSource
from devtools.wall_owner_containment import AffineMap
from devtools.wall_owner_escape_compatibility import (
    AxisExtremum,
    ClassCompatibility,
    FrameExtremum,
)
from devtools.wall_owner_footprints import OwnerFrameFootprint, RetainedOwnerFrame
from devtools.wall_owner_parent_compatibility import (
    DerivedOwnerFrame,
    ParentClassCompatibility,
)
from devtools.wall_owner_parent_experiment import (
    CLAIM_LIMIT,
    IMPLEMENTATION_PATHS,
    RESULT_SCHEMA,
    ParentExperimentError,
    b_only_result_record,
    discover_parent_implementation_paths,
    main,
    parent_result_record,
    prepare_output_path,
    supervise_parent_worker,
    validate_parent_implementation_revision,
    validate_parent_readback_revision,
    validate_result_document,
    write_result_document,
)


def _minimal_invalid_document() -> dict[str, object]:
    return {
        "schema": "wall-owner-parent-experiment/v1",
        "status": "invalid",
        "outcome": "invalid",
        "claim_limit": CLAIM_LIMIT,
        "sources": None,
        "settings": None,
        "clocks": {
            "source_replay_seconds": 0.0,
            "scientific_seconds": 0.0,
            "process_seconds": 0.0,
            "scientific_started": False,
        },
        "authority": None,
        "residual_check": None,
        "comparisons": [],
        "summary": {
            "expected_residual_orientations": 361,
            "bound_residual_orientations": 0,
            "expected_selected_owners": 4,
            "bound_selected_owners": 0,
            "completed_comparisons": 0,
        },
        "error": "synthetic source refusal",
    }


def test_result_schema_is_closed_and_accepts_honest_preload_failure() -> None:
    document = _minimal_invalid_document()
    validate_result_document(document)

    document["unconsumed_typo"] = True
    with pytest.raises(ParentExperimentError, match="schema"):
        validate_result_document(document)


def test_schema_path_is_repository_owned() -> None:
    expected = (
        Path(__file__).resolve().parents[1]
        / "cases"
        / "n11_five_dot_cover"
        / "parent-domain-experiment.schema.json"
    )
    assert expected == RESULT_SCHEMA


def test_atomic_writer_validates_before_replacing_a_checkpoint(tmp_path: Path) -> None:
    output = tmp_path / "result.json"
    document = _minimal_invalid_document()
    write_result_document(output, document)
    first_bytes = output.read_bytes()
    assert json.loads(first_bytes) == document
    assert first_bytes.endswith(b"\n")

    document["unconsumed_typo"] = True
    with pytest.raises(ParentExperimentError, match="schema"):
        write_result_document(output, document)
    assert output.read_bytes() == first_bytes


def test_fresh_output_guard_keeps_results_out_of_code_and_inputs(tmp_path: Path) -> None:
    repository = Path(__file__).resolve().parents[2]
    receipt = tmp_path / "source.json"
    with pytest.raises(ParentExperimentError, match="input receipt"):
        prepare_output_path(receipt, repository=repository, inputs=(receipt,))
    with pytest.raises(ParentExperimentError, match="code or tests"):
        prepare_output_path(
            Path(__file__).resolve().parents[1] / "devtools" / "result.json",
            repository=repository,
            inputs=(receipt,),
        )
    output = tmp_path / "result.json"
    assert prepare_output_path(output, repository=repository, inputs=(receipt,)) == output


def test_implementation_revision_requires_a_clean_complete_dependency_graph() -> None:
    repository = Path(__file__).resolve().parents[2]
    revision = "a" * 40

    def git(_repository: Path, *arguments: str) -> str:
        if arguments == ("rev-parse", "HEAD"):
            return revision
        if arguments == ("status", "--porcelain"):
            return ""
        if arguments[:4] == ("ls-tree", "-r", "--name-only", revision):
            return "\n".join(IMPLEMENTATION_PATHS)
        raise AssertionError(arguments)

    with patch("devtools.wall_owner_parent_experiment._git", side_effect=git):
        assert validate_parent_implementation_revision(repository, revision) == revision

    def missing_schema(_repository: Path, *arguments: str) -> str:
        value = git(_repository, *arguments)
        if arguments[:4] == ("ls-tree", "-r", "--name-only", revision):
            return "\n".join(IMPLEMENTATION_PATHS[1:])
        return value

    with (
        patch(
            "devtools.wall_owner_parent_experiment._git",
            side_effect=missing_schema,
        ),
        pytest.raises(ParentExperimentError, match="dependency graph"),
    ):
        validate_parent_implementation_revision(repository, revision)


def test_declared_dependency_graph_equals_recursive_static_import_closure() -> None:
    repository = Path(__file__).resolve().parents[2]
    discovered = discover_parent_implementation_paths(repository)
    assert discovered == IMPLEMENTATION_PATHS

    without_transitive = tuple(
        path
        for path in IMPLEMENTATION_PATHS
        if path != "packing/devtools/multi_owner_domains.py"
    )
    with (
        patch(
            "devtools.wall_owner_parent_experiment.IMPLEMENTATION_PATHS",
            without_transitive,
        ),
        pytest.raises(ParentExperimentError, match="dependency closure"),
    ):
        validate_parent_implementation_revision(repository, "a" * 40)


def test_revision_guards_refuse_to_attest_a_different_checkout(tmp_path: Path) -> None:
    other_repository = tmp_path / "clean-but-different"
    other_repository.mkdir()
    for validator in (
        validate_parent_implementation_revision,
        validate_parent_readback_revision,
    ):
        with pytest.raises(ParentExperimentError, match="running implementation"):
            validator(other_repository, "a" * 40)


def test_revision_guard_refuses_a_loaded_project_module_from_another_checkout(
    tmp_path: Path,
) -> None:
    repository = Path(__file__).resolve().parents[2]
    foreign = ModuleType("sqpack.field")
    foreign.__file__ = str(tmp_path / "foreign" / "sqpack" / "field.py")
    with (
        patch.dict(sys.modules, {"sqpack.field": foreign}),
        pytest.raises(ParentExperimentError, match="different checkout"),
    ):
        validate_parent_implementation_revision(repository, "a" * 40)


def test_result_rows_keep_exact_extrema_and_empty_derived_dispositions() -> None:
    fraction = Fraction
    identity = RetainedOwnerFrame(
        (fraction(1), fraction(0)),
        3,
        1,
        (DirectionSource(3, reflected=False),),
    )
    original = OwnerFrameFootprint(
        identity,
        ((fraction(1), fraction(1)),),
        0,
        (fraction(1), fraction(1)),
        (fraction(1), fraction(1)),
        ((fraction(1), fraction(1)),),
        "allowed",
    )
    empty = OwnerFrameFootprint(identity, (), -1, None, None, None, "empty")
    axis = AxisExtremum(
        "+owner-u",
        (fraction(1), fraction(0)),
        fraction(1),
        fraction(1, 2),
        fraction(1, 2),
        fraction(-1, 7),
        (fraction(1), fraction(1)),
        (fraction(1), fraction(1)),
    )
    extremum = FrameExtremum(
        0,
        original,
        (fraction(1), fraction(0)),
        (fraction(0), fraction(1)),
        axis,
        8,
    )
    transform = AffineMap("I", 1, 0, 0, 1, fraction(0), fraction(0), 0, (0, 1, 2, 3))
    b_only = ClassCompatibility(
        0,
        0,
        transform,
        "incompatible",
        1,
        (extremum,),
        fraction(-1, 7),
        fraction(-1, 7),
    )
    parent = ParentClassCompatibility(
        "impossible",
        1,
        (DerivedOwnerFrame(original, empty, fraction(1, 2), ()),),
        (),
        None,
        None,
    )

    b_record = b_only_result_record(b_only)
    parent_record = parent_result_record(parent)
    assert cast(dict[str, object], cast(list[object], b_record["frame_extrema"])[0])[
        "maximum"
    ] == {
        "label": "+owner-u",
        "axis": ["1", "0"],
        "minimum_owner_projection": "1",
        "owner_radius": "1/2",
        "residual_radius": "1/2",
        "slack": "-1/7",
        "canonical_owner_centre": ["1", "1"],
        "owner_centre": ["1", "1"],
    }
    derived = cast(dict[str, object], cast(list[object], parent_record["derived_frames"])[0])
    assert derived["frame_index"] == 0
    assert cast(dict[str, object], derived["restricted"])["disposition"] == "empty"
    assert parent_record["global_maximum_slack"] is None


def test_supervisor_terminates_then_kills_after_the_two_second_grace(
    tmp_path: Path,
) -> None:
    class Process:
        def __init__(self) -> None:
            self.waits: list[float | None] = []
            self.terminated = False
            self.killed = False

        def wait(self, timeout: float | None = None) -> int:
            self.waits.append(timeout)
            if len(self.waits) <= 2:
                raise subprocess.TimeoutExpired(
                    "synthetic worker",
                    0 if timeout is None else timeout,
                )
            return -9

        def terminate(self) -> None:
            self.terminated = True

        def kill(self) -> None:
            self.killed = True

    process = Process()
    output = tmp_path / "timeout.json"
    with patch(
        "devtools.wall_owner_parent_experiment.subprocess.Popen",
        return_value=process,
    ):
        status = supervise_parent_worker(("synthetic-worker",), output)

    assert status == 1
    assert process.waits == [120, 2, None]
    assert process.terminated
    assert process.killed
    document = cast(dict[str, object], json.loads(output.read_text(encoding="utf-8")))
    validate_result_document(document)
    assert document["status"] == "invalid"


def test_early_worker_failure_records_its_measured_duration(tmp_path: Path) -> None:
    class Process:
        def wait(self, timeout: float | None = None) -> int:
            assert timeout == 120
            return 3

    output = tmp_path / "early-failure.json"
    with (
        patch(
            "devtools.wall_owner_parent_experiment.subprocess.Popen",
            return_value=Process(),
        ),
        patch(
            "devtools.wall_owner_parent_experiment.time.perf_counter",
            side_effect=(100.0, 100.25),
        ),
    ):
        status = supervise_parent_worker(("synthetic-worker",), output)

    assert status == 3
    document = cast(dict[str, object], json.loads(output.read_text(encoding="utf-8")))
    validate_result_document(document)
    assert document["clocks"] == {
        "source_replay_seconds": 0.25,
        "scientific_seconds": 0.0,
        "process_seconds": 0.25,
        "scientific_started": False,
    }


def test_cli_supervises_the_pinned_worker_without_entering_the_target(
    tmp_path: Path,
) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    output = tmp_path / "result.json"
    revision = "a" * 40
    with (
        patch(
            "devtools.wall_owner_parent_experiment.validate_parent_implementation_revision",
            return_value=revision,
        ) as validate_revision,
        patch(
            "devtools.wall_owner_parent_experiment.supervise_parent_worker",
            return_value=0,
        ) as supervise,
    ):
        status = main(
            (
                "--repository",
                str(repository),
                "--expect-implementation-revision",
                revision,
                "--output",
                str(output),
            )
        )

    assert status == 0
    validate_revision.assert_called_once_with(repository, revision)
    command, destination = supervise.call_args.args
    assert command[1:4] == (
        "-m",
        "devtools.wall_owner_parent_experiment",
        "--worker",
    )
    assert command[-2:] == ("--output", str(output))
    assert destination == output
