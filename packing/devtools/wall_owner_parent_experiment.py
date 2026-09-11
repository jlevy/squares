#!/usr/bin/env python3
"""Prospective production runner for source-bound unit-parent experiments.

The runner is an instrument. Importing it, validating its schema, or exercising it on
synthetic inputs makes no packing claim and does not run the retained BC326 target.
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import math
import subprocess
import sys
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol, cast

from jsonschema_rs import Draft202012Validator
from strif import atomic_write_text

from devtools.owner_footprints import DirectionSource, Point
from devtools.wall_owner_escape_compatibility import (
    EVALUATION_CORNER_INDICES,
    ClassCompatibility,
    FrameExtremum,
    evaluate_class,
    frame_separation_extremum,
)
from devtools.wall_owner_footprints import OwnerFrameFootprint, RetainedOwnerFrame
from devtools.wall_owner_parent_compatibility import (
    GLOBAL_PARENT_RULE,
    DerivedOwnerFrame,
    ParentClassCompatibility,
    ResidualParentCheck,
    check_residual_parent_centre,
    evaluate_parent_class,
    parent_frame_extremum,
    restrict_owner_centres,
)
from devtools.wall_owner_parent_inputs import (
    ParentAdapterInputs,
    ParentInputPins,
    ProducedReceiptPin,
    ReceiptPin,
    SelectedOwnerAuthority,
    TrackedReceiptIdentity,
    load_parent_adapter_inputs,
)
from devtools.wall_owner_selected_cover import SELECTED_TUPLE

PACKING = Path(__file__).resolve().parents[1]
RUNNING_REPOSITORY = PACKING.parent.resolve()
RUNNING_ENTRY_POINT = Path(__file__).resolve()
RESULT_SCHEMA = (
    PACKING / "cases" / "n11_five_dot_cover" / "parent-domain-experiment.schema.json"
)
RESULT_SCHEMA_PATH = "packing/cases/n11_five_dot_cover/parent-domain-experiment.schema.json"
IMPLEMENTATION_PATHS = (
    "packing/cases/__init__.py",
    "packing/cases/n11_five_dot_cover/__init__.py",
    "packing/cases/n11_five_dot_cover/independent_union.py",
    RESULT_SCHEMA_PATH,
    "packing/devtools/__init__.py",
    "packing/devtools/multi_owner_domains.py",
    "packing/devtools/owner_footprints.py",
    "packing/devtools/wall_owner_containment.py",
    "packing/devtools/wall_owner_escape_compatibility.py",
    "packing/devtools/wall_owner_fixed_pattern.py",
    "packing/devtools/wall_owner_footprints.py",
    "packing/devtools/wall_owner_parent_compatibility.py",
    "packing/devtools/wall_owner_parent_experiment.py",
    "packing/devtools/wall_owner_parent_inputs.py",
    "packing/devtools/wall_owner_selected_cover.py",
    "packing/devtools/wall_owner_six_dot_cover.py",
    "packing/devtools/wall_owner_sixth_site_screen.py",
    "packing/src/sqpack/__init__.py",
    "packing/src/sqpack/field.py",
    "packing/src/sqpack/fractional/__init__.py",
    "packing/src/sqpack/fractional/certificate.py",
    "packing/src/sqpack/fractional/generate.py",
    "packing/src/sqpack/fractional/model.py",
    "packing/src/sqpack/fractional/sweep.py",
    "packing/src/sqpack/verify.py",
    "packing/src/sqpack/workers.py",
)
ENDPOINT_PATH = (
    "packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/"
    "exp-143-four-owner-footprint-cover.json"
)
WALL_PATH = (
    "packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/"
    "exp-146-wall-owner-footprints.json"
)
SELECTED_PATH = (
    "packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/"
    "exp-149-selected-wall-tuple-cover.json"
)
STRICT_ESCAPE_PATH = (
    "packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/"
    "exp-151-selected-six-dot-cover.json"
)
ENDPOINT_BLOB = "cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19"
WALL_BLOB = "e54fa98133db5f2135cae8875188f51b7db26e12"
WALL_PRODUCER = "915758898a97c92793f51e62b7a6b17f846895ca"
SELECTED_BLOB = "83ec897738d6d1b228623c3ac4c10cd9170d5940"
SELECTED_PRODUCER = "5600c0fb4eccf9e9dcdf82b02506d3d4340651cb"
STRICT_ESCAPE_BLOB = "46d34b1e295d9f5178379b02780a8c598c1a73e5"
STRICT_ESCAPE_PRODUCER = "c8cd38dad502c78840144bcae42df4294ba7f3d0"
SCIENTIFIC_ALLOWANCE_SECONDS = 90
EXTERNAL_BOUND_SECONDS = 120
TERMINATION_GRACE_SECONDS = 2
PHYSICAL_OWNER_ORDER = tuple(
    ("BL", "BR", "TL", "TR")[index] for index in EVALUATION_CORNER_INDICES
)
CLAIM_LIMIT = (
    "fixed exp151 residual pose against individual selected owner classes under the "
    "necessary global-D parent-centre rule; no simultaneous owner feasibility, "
    "neighbourhood exclusion, or global n=11 conclusion"
)

Clock = Callable[[], float]


@dataclass(frozen=True, slots=True)
class ParentOwnerComparison:
    """One matched B-only and parent-restricted class disposition."""

    owner: SelectedOwnerAuthority
    status: Literal["complete", "partial"]
    attribution: Literal[
        "b-only-incompatible",
        "owner-domain-gain",
        "still-compatible",
        "unresolved",
    ]
    b_only: ClassCompatibility | None
    parent_restricted: ParentClassCompatibility | None
    error: str | None = None


@dataclass(frozen=True, slots=True)
class ParentExperimentEvaluation:
    """The scientific portion after authoritative source replay has completed."""

    status: Literal["complete", "partial", "invalid"]
    outcome: Literal[
        "residual-self-excluded",
        "b-only-incompatible",
        "owner-domain-gain",
        "no-owner-domain-exclusion",
        "incomplete",
        "invalid",
    ]
    residual_check: ResidualParentCheck | None
    comparisons: tuple[ParentOwnerComparison, ...]
    error: str | None = None


class ParentInputLoader(Protocol):
    def __call__(
        self,
        pins: ParentInputPins,
        *,
        replay_deadline: float,
    ) -> ParentAdapterInputs: ...


class ParentTarget(Protocol):
    def __call__(
        self,
        inputs: ParentAdapterInputs,
        *,
        deadline: float,
        clock: Clock,
        checkpoint: Callable[[ParentExperimentEvaluation], None],
    ) -> ParentExperimentEvaluation: ...


Publisher = Callable[[Path, dict[str, object]], None]


class ParentExperimentError(ValueError):
    """A result, source, replay, path, or process guard refused the experiment."""


def _local_module_path(repository: Path, module: str) -> Path | None:
    parts = module.split(".")
    roots = {
        "cases": repository / "packing" / "cases",
        "devtools": repository / "packing" / "devtools",
        "sqpack": repository / "packing" / "src" / "sqpack",
    }
    root = roots.get(parts[0])
    if root is None:
        return None
    candidate = root.joinpath(*parts[1:])
    module_path = candidate.with_suffix(".py")
    if module_path.is_file():
        return module_path
    package_path = candidate / "__init__.py"
    return package_path if package_path.is_file() else None


def _imported_local_modules(module: str, path: Path) -> set[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError) as error:
        raise ParentExperimentError(f"could not inspect dependency {path}: {error}") from error
    package = module if path.name == "__init__.py" else module.rpartition(".")[0]
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = node.module or ""
            if node.level:
                relative = f"{'.' * node.level}{base}"
                try:
                    base = importlib.util.resolve_name(relative, package)
                except ImportError as error:
                    raise ParentExperimentError(
                        f"could not resolve relative import {relative!r} in {path}"
                    ) from error
            if base:
                imported.add(base)
                imported.update(f"{base}.{alias.name}" for alias in node.names)
    return imported


def discover_parent_implementation_paths(repository: Path) -> tuple[str, ...]:
    """Return the recursive local Python import closure plus the result schema."""

    resolved = repository.resolve()
    pending = ["devtools.wall_owner_parent_experiment"]
    visited: set[str] = set()
    paths = {RESULT_SCHEMA_PATH}
    while pending:
        module = pending.pop()
        if module in visited:
            continue
        path = _local_module_path(resolved, module)
        if path is None:
            continue
        visited.add(module)
        paths.add(path.relative_to(resolved).as_posix())
        parts = module.split(".")
        for length in range(1, len(parts)):
            package = ".".join(parts[:length])
            if package not in visited and _local_module_path(resolved, package) is not None:
                pending.append(package)
        pending.extend(
            imported
            for imported in _imported_local_modules(module, path)
            if imported not in visited and _local_module_path(resolved, imported) is not None
        )
    return tuple(sorted(paths))


def _validate_running_repository(repository: Path) -> None:
    expected_packing = repository / "packing"
    expected_entry_point = expected_packing / "devtools" / RUNNING_ENTRY_POINT.name
    if (
        expected_packing != PACKING.resolve()
        or expected_entry_point != RUNNING_ENTRY_POINT
        or not RUNNING_ENTRY_POINT.is_relative_to(repository)
    ):
        raise ParentExperimentError(
            "repository must be the checkout containing the running implementation"
        )
    for relative in IMPLEMENTATION_PATHS:
        path = Path(relative)
        if path.suffix != ".py":
            continue
        parts = path.with_suffix("").parts
        if parts[-1] == "__init__":
            parts = parts[:-1]
        if parts[:3] == ("packing", "src", "sqpack"):
            module_name = ".".join(parts[2:])
        elif parts[:2] in (("packing", "devtools"), ("packing", "cases")):
            module_name = ".".join(parts[1:])
        else:
            continue
        loaded = sys.modules.get(module_name)
        if module_name == "devtools.wall_owner_parent_experiment" and loaded is None:
            loaded = sys.modules.get("__main__")
        if loaded is None:
            continue
        origin = getattr(loaded, "__file__", None)
        expected = repository / relative
        if type(origin) is not str or Path(origin).resolve() != expected:
            raise ParentExperimentError(
                f"loaded project module {module_name} comes from a different checkout"
            )


def _validate_declared_dependency_closure(repository: Path) -> None:
    discovered = discover_parent_implementation_paths(repository)
    if discovered != IMPLEMENTATION_PATHS:
        missing = sorted(set(discovered) - set(IMPLEMENTATION_PATHS))
        extra = sorted(set(IMPLEMENTATION_PATHS) - set(discovered))
        raise ParentExperimentError(
            f"declared implementation dependency closure differs from imports; "
            f"missing={missing}, extra={extra}"
        )


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ParentExperimentError(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def _reject_json_constant(value: str) -> None:
    raise ParentExperimentError(f"non-finite JSON constant {value!r}")


def _load_json(text: str) -> object:
    return json.loads(
        text,
        object_pairs_hook=_unique_object,
        parse_constant=_reject_json_constant,
    )


def _git(repository: Path, *arguments: str) -> str:
    result = subprocess.run(
        ("git", *arguments),
        cwd=repository,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or f"git {' '.join(arguments)} failed"
        raise ParentExperimentError(message)
    return result.stdout.strip()


def validate_parent_implementation_revision(
    repository: Path,
    expected_revision: str,
) -> str:
    """Bind every instrument dependency to one clean committed checkout."""

    if len(expected_revision) != 40 or any(
        character not in "0123456789abcdef" for character in expected_revision
    ):
        raise ParentExperimentError(
            "expected implementation revision must be 40 lowercase hexadecimal digits"
        )
    resolved = repository.resolve()
    if not repository.is_absolute() or not resolved.is_dir():
        raise ParentExperimentError("repository must be an existing absolute directory")
    if resolved != RUNNING_REPOSITORY:
        raise ParentExperimentError(
            "repository must be the checkout containing the running implementation"
        )
    _validate_running_repository(resolved)
    _validate_declared_dependency_closure(resolved)
    if _git(resolved, "rev-parse", "HEAD") != expected_revision:
        raise ParentExperimentError("current Git revision differs from the frozen instrument")
    if _git(resolved, "status", "--porcelain"):
        raise ParentExperimentError("instrument checkout must be clean")
    tracked = set(
        _git(
            resolved,
            "ls-tree",
            "-r",
            "--name-only",
            expected_revision,
            "--",
            *IMPLEMENTATION_PATHS,
        ).splitlines()
    )
    if tracked != set(IMPLEMENTATION_PATHS):
        missing = ", ".join(sorted(set(IMPLEMENTATION_PATHS) - tracked))
        raise ParentExperimentError(
            f"frozen implementation dependency graph is incomplete: {missing}"
        )
    return expected_revision


def validate_parent_readback_revision(
    repository: Path,
    expected_revision: str,
) -> str:
    """Rebind the committed instrument while permitting its new result artifact."""

    if len(expected_revision) != 40 or any(
        character not in "0123456789abcdef" for character in expected_revision
    ):
        raise ParentExperimentError("readback revision must be a full lowercase Git hash")
    resolved = repository.resolve()
    if not repository.is_absolute() or not resolved.is_dir():
        raise ParentExperimentError("readback repository must be an absolute directory")
    if resolved != RUNNING_REPOSITORY:
        raise ParentExperimentError(
            "readback repository must contain the running implementation"
        )
    _validate_running_repository(resolved)
    _validate_declared_dependency_closure(resolved)
    if _git(resolved, "rev-parse", "HEAD") != expected_revision:
        raise ParentExperimentError("readback checkout differs from the frozen instrument")
    changed = _git(resolved, "status", "--porcelain", "--", *IMPLEMENTATION_PATHS)
    if changed:
        raise ParentExperimentError("readback instrument dependencies are not clean")
    tracked = set(
        _git(
            resolved,
            "ls-tree",
            "-r",
            "--name-only",
            expected_revision,
            "--",
            *IMPLEMENTATION_PATHS,
        ).splitlines()
    )
    if tracked != set(IMPLEMENTATION_PATHS):
        raise ParentExperimentError("readback dependency graph is incomplete")
    return expected_revision


def retained_parent_input_pins(
    repository_root: Path,
    checkout_revision: str,
) -> ParentInputPins:
    """Return the four retained receipt pins under one prospective checkout."""

    return ParentInputPins(
        repository_root,
        checkout_revision,
        ReceiptPin(ENDPOINT_PATH, ENDPOINT_BLOB),
        ProducedReceiptPin(WALL_PATH, WALL_BLOB, WALL_PRODUCER),
        ProducedReceiptPin(SELECTED_PATH, SELECTED_BLOB, SELECTED_PRODUCER),
        ProducedReceiptPin(
            STRICT_ESCAPE_PATH,
            STRICT_ESCAPE_BLOB,
            STRICT_ESCAPE_PRODUCER,
        ),
    )


def _point_record(point: Point) -> list[str]:
    return [str(point[0]), str(point[1])]


def _source_records(sources: tuple[DirectionSource, ...]) -> list[dict[str, object]]:
    return [
        {
            "folded_index": source.folded_index,
            "reflected": source.reflected,
        }
        for source in sources
    ]


def _frame_identity_record(frame: RetainedOwnerFrame) -> dict[str, object]:
    return {
        "ray": _point_record(frame.ray),
        "orientation_index": frame.orientation_index,
        "quarter_turn": frame.quarter_turn,
        "sources": _source_records(frame.sources),
    }


def _polygon_record(polygon: tuple[Point, ...]) -> list[list[str]]:
    return [_point_record(point) for point in polygon]


def _interval_record(interval: tuple[object, object] | None) -> list[str] | None:
    if interval is None:
        return None
    return [str(interval[0]), str(interval[1])]


def _footprint_record(frame: OwnerFrameFootprint) -> dict[str, object]:
    return {
        "disposition": frame.disposition,
        "centre_dimension": frame.centre_dimension,
        "centre_set": _polygon_record(frame.centre_set),
        "support_r": _interval_record(frame.support_r),
        "support_jr": _interval_record(frame.support_jr),
        "common_rectangle": None
        if frame.common_rectangle is None
        else _polygon_record(frame.common_rectangle),
    }


def _frame_extremum_record(row: FrameExtremum) -> dict[str, object]:
    maximum = row.maximum
    return {
        "frame_index": row.frame_index,
        "frame": _frame_identity_record(row.source.frame),
        "owner_u": _point_record(row.owner_u),
        "owner_v": _point_record(row.owner_v),
        "axes_checked": row.axes_checked,
        "maximum": {
            "label": maximum.label,
            "axis": _point_record(maximum.axis),
            "minimum_owner_projection": str(maximum.minimum_owner_projection),
            "owner_radius": str(maximum.owner_radius),
            "residual_radius": str(maximum.residual_radius),
            "slack": str(maximum.slack),
            "canonical_owner_centre": _point_record(maximum.canonical_owner_centre),
            "owner_centre": _point_record(maximum.owner_centre),
        },
    }


def b_only_result_record(result: ClassCompatibility) -> dict[str, object]:
    """Serialize the matched strict-core control without changing its verdict."""

    return {
        "status": result.status,
        "expected_frames": result.expected_frames,
        "checked_frames": len(result.frame_extrema),
        "frame_extrema": [_frame_extremum_record(row) for row in result.frame_extrema],
        "observed_maximum_slack": None
        if result.observed_maximum_slack is None
        else str(result.observed_maximum_slack),
        "global_maximum_slack": None
        if result.global_maximum_slack is None
        else str(result.global_maximum_slack),
        "error": result.error,
    }


def parent_result_record(result: ParentClassCompatibility) -> dict[str, object]:
    """Serialize all derived dispositions and exact extrema, including partial rows."""

    return {
        "status": result.status,
        "expected_frames": result.expected_frames,
        "derived_frames": [
            _derived_frame_record(index, row) for index, row in enumerate(result.derived_frames)
        ],
        "frame_extrema": [_frame_extremum_record(row) for row in result.frame_extrema],
        "observed_maximum_slack": None
        if result.observed_maximum_slack is None
        else str(result.observed_maximum_slack),
        "global_maximum_slack": None
        if result.global_maximum_slack is None
        else str(result.global_maximum_slack),
        "error": result.error,
    }


def _derived_frame_record(index: int, row: DerivedOwnerFrame) -> dict[str, object]:
    return {
        "frame_index": index,
        "frame": _frame_identity_record(row.original.frame),
        "extent": str(row.extent),
        "parent_box": _polygon_record(row.parent_box),
        "original": _footprint_record(row.original),
        "restricted": _footprint_record(row.restricted),
    }


def residual_check_record(result: ResidualParentCheck) -> dict[str, object]:
    """Serialize the residual's separate necessary parent-box check."""

    return {
        "status": result.status,
        "centre": _point_record(result.centre),
        "ray": _point_record(result.ray),
        "sources": _source_records(result.sources),
        "extent": str(result.extent),
        "parent_box": _polygon_record(result.parent_box),
    }


def _comparison_record(result: ParentOwnerComparison) -> dict[str, object]:
    owner = result.owner
    return {
        "corner": owner.corner,
        "corner_index": owner.corner_index,
        "class_index": owner.class_index,
        "class_id": owner.class_id,
        "status": result.status,
        "attribution": result.attribution,
        "b_only": None if result.b_only is None else b_only_result_record(result.b_only),
        "parent_restricted": None
        if result.parent_restricted is None
        else parent_result_record(result.parent_restricted),
        "error": result.error,
    }


def _result_document(
    evaluation: ParentExperimentEvaluation,
    *,
    inputs: ParentAdapterInputs,
    implementation_revision: str,
    source_replay_seconds: float,
    scientific_seconds: float,
    process_seconds: float,
    scientific_started: bool,
) -> dict[str, object]:
    authority = authority_record(inputs)
    return {
        "schema": "wall-owner-parent-experiment/v1",
        "status": evaluation.status,
        "outcome": evaluation.outcome,
        "claim_limit": CLAIM_LIMIT,
        "sources": sources_record(
            inputs,
            implementation_revision=implementation_revision,
        ),
        "settings": settings_record(),
        "clocks": {
            "source_replay_seconds": source_replay_seconds,
            "scientific_seconds": scientific_seconds,
            "process_seconds": process_seconds,
            "scientific_started": scientific_started,
        },
        "authority": authority,
        "residual_check": None
        if evaluation.residual_check is None
        else residual_check_record(evaluation.residual_check),
        "comparisons": [
            _comparison_record(comparison) for comparison in evaluation.comparisons
        ],
        "summary": {
            "expected_residual_orientations": 361,
            "bound_residual_orientations": len(inputs.residual_manifest),
            "expected_selected_owners": 4,
            "bound_selected_owners": len(inputs.selected_owners),
            "completed_comparisons": sum(
                comparison.status == "complete" for comparison in evaluation.comparisons
            ),
        },
        "error": evaluation.error,
    }


def _invalid_document(
    error: str,
    *,
    source_replay_seconds: float,
    process_seconds: float,
) -> dict[str, object]:
    return {
        "schema": "wall-owner-parent-experiment/v1",
        "status": "invalid",
        "outcome": "invalid",
        "claim_limit": CLAIM_LIMIT,
        "sources": None,
        "settings": None,
        "clocks": {
            "source_replay_seconds": source_replay_seconds,
            "scientific_seconds": 0.0,
            "process_seconds": process_seconds,
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
        "error": error,
    }


def _expired(deadline: float, clock: Clock, message: str) -> None:
    if clock() >= deadline:
        raise ParentExperimentError(message)


def _partial_comparison(
    owner: SelectedOwnerAuthority,
    *,
    b_only: ClassCompatibility | None,
    parent: ParentClassCompatibility | None,
    error: str,
) -> ParentOwnerComparison:
    return ParentOwnerComparison(
        owner,
        "partial",
        "unresolved",
        b_only,
        parent,
        error,
    )


def run_parent_target(
    inputs: ParentAdapterInputs,
    *,
    deadline: float,
    clock: Clock = time.perf_counter,
    checkpoint: Callable[[ParentExperimentEvaluation], None] = lambda _result: None,
) -> ParentExperimentEvaluation:
    """Run the fixed comparison under a caller-started absolute scientific deadline."""

    residual = check_residual_parent_centre(
        inputs.strict_escape.escape.centre,
        inputs.selected_residual.ray,
        inputs.selected_residual.sources,
        inputs.residual_manifest[inputs.selected_residual.index].sources,
    )
    partial = ParentExperimentEvaluation(
        "partial",
        "incomplete",
        residual,
        (),
        "owner comparisons have not completed",
    )
    checkpoint(partial)
    if residual.status == "outside-parent-box":
        if clock() >= deadline:
            result = ParentExperimentEvaluation(
                "partial",
                "incomplete",
                residual,
                (),
                "scientific deadline reached before residual disposition",
            )
        else:
            result = ParentExperimentEvaluation(
                "complete",
                "residual-self-excluded",
                residual,
                (),
            )
        return result

    owners = {owner.corner_index: owner for owner in inputs.selected_owners}
    comparisons: list[ParentOwnerComparison] = []
    terminal: ParentExperimentEvaluation | None = None
    for corner_index in EVALUATION_CORNER_INDICES:
        _expired(deadline, clock, "scientific deadline reached between owner classes")
        owner = owners[corner_index]
        b_only = evaluate_class(
            owner.wall_class,
            owner_mark=owner.owner_class.mark,
            corner_index=owner.corner_index,
            class_index=owner.class_index,
            transform=owner.physical_map,
            residual_centre=inputs.strict_escape.escape.centre,
            residual_u=inputs.selected_residual.ray,
            expected_frames=len(owner.expected_frames),
            outer_side=GLOBAL_PARENT_RULE.outer_side,
            half=GLOBAL_PARENT_RULE.core_side / 2,
            deadline=deadline,
        )
        if b_only.status == "partial":
            comparison = _partial_comparison(
                owner,
                b_only=b_only,
                parent=None,
                error=b_only.error or "B-only control did not complete",
            )
            comparisons.append(comparison)
            terminal = ParentExperimentEvaluation(
                "partial",
                "incomplete",
                residual,
                tuple(comparisons),
                comparison.error,
            )
            break
        if b_only.status == "incompatible":
            if clock() >= deadline:
                terminal = ParentExperimentEvaluation(
                    "partial",
                    "incomplete",
                    residual,
                    tuple(comparisons),
                    "scientific deadline reached before B-only disposition",
                )
            else:
                comparisons.append(
                    ParentOwnerComparison(
                        owner,
                        "complete",
                        "b-only-incompatible",
                        b_only,
                        None,
                    )
                )
                terminal = ParentExperimentEvaluation(
                    "complete",
                    "b-only-incompatible",
                    residual,
                    tuple(comparisons),
                )
            break
        parent = evaluate_parent_class(
            owner.wall_class.frames,
            owner.expected_frames,
            owner_mark=owner.owner_class.mark,
            transform=owner.physical_map,
            residual_centre=inputs.strict_escape.escape.centre,
            residual_u=inputs.selected_residual.ray,
            deadline=deadline,
            clock=clock,
        )
        if parent.status == "unresolved":
            comparison = _partial_comparison(
                owner,
                b_only=b_only,
                parent=parent,
                error=parent.error or "parent-restricted comparison did not complete",
            )
            comparisons.append(comparison)
            terminal = ParentExperimentEvaluation(
                "partial",
                "incomplete",
                residual,
                tuple(comparisons),
                comparison.error,
            )
            break
        if clock() >= deadline:
            terminal = ParentExperimentEvaluation(
                "partial",
                "incomplete",
                residual,
                tuple(comparisons),
                "scientific deadline reached before parent-restricted disposition",
            )
            break
        attribution: Literal["owner-domain-gain", "still-compatible"]
        if parent.status in ("incompatible", "impossible"):
            attribution = "owner-domain-gain"
        else:
            attribution = "still-compatible"
        comparisons.append(
            ParentOwnerComparison(
                owner,
                "complete",
                attribution,
                b_only,
                parent,
            )
        )
        checkpoint(
            ParentExperimentEvaluation(
                "partial",
                "incomplete",
                residual,
                tuple(comparisons),
                "selected owner comparisons remain",
            )
        )
        if attribution == "owner-domain-gain":
            if clock() >= deadline:
                terminal = ParentExperimentEvaluation(
                    "partial",
                    "incomplete",
                    residual,
                    tuple(comparisons),
                    "scientific deadline reached after owner checkpoint publication",
                )
            else:
                terminal = ParentExperimentEvaluation(
                    "complete",
                    "owner-domain-gain",
                    residual,
                    tuple(comparisons),
                )
            break
    if terminal is not None:
        return terminal
    _expired(deadline, clock, "scientific deadline reached before final disposition")
    return ParentExperimentEvaluation(
        "complete",
        "no-owner-domain-exclusion",
        residual,
        tuple(comparisons),
    )


def execute_parent_experiment(
    pins: ParentInputPins,
    *,
    implementation_revision: str,
    output: Path,
    clock: Clock = time.perf_counter,
    loader: ParentInputLoader = load_parent_adapter_inputs,
    target: ParentTarget = run_parent_target,
    publisher: Publisher | None = None,
    process_deadline: float | None = None,
) -> dict[str, object]:
    """Load and replay sources before a target bounded by both experiment clocks."""

    process_started = clock()
    absolute_process_deadline = (
        process_started + EXTERNAL_BOUND_SECONDS
        if process_deadline is None
        else process_deadline
    )
    if absolute_process_deadline <= process_started:
        raise ParentExperimentError("process deadline must be later than process start")
    publish_result = write_result_document if publisher is None else publisher
    try:
        inputs = loader(pins, replay_deadline=absolute_process_deadline)
    except (OSError, ValueError) as error:
        finished = clock()
        document = _invalid_document(
            f"source replay refused: {error}",
            source_replay_seconds=finished - process_started,
            process_seconds=finished - process_started,
        )
        publish_result(output, document)
        return document
    source_finished = clock()
    if inputs.checkout_revision != implementation_revision:
        document = _invalid_document(
            "source replay refused: receipt checkout and implementation revision "
            "must be identical",
            source_replay_seconds=source_finished - process_started,
            process_seconds=source_finished - process_started,
        )
        publish_result(output, document)
        return document
    if source_finished >= absolute_process_deadline:
        document = _invalid_document(
            "source replay exceeded the external process bound",
            source_replay_seconds=source_finished - process_started,
            process_seconds=source_finished - process_started,
        )
        publish_result(output, document)
        return document
    scientific_started = source_finished
    source_seconds = source_finished - process_started
    scientific_deadline = min(
        scientific_started + SCIENTIFIC_ALLOWANCE_SECONDS,
        absolute_process_deadline,
    )
    latest = ParentExperimentEvaluation(
        "partial",
        "incomplete",
        None,
        (),
        "scientific evaluation has not completed",
    )

    def expire(
        evaluation: ParentExperimentEvaluation,
        now: float,
        *,
        phase: Literal["before", "during"],
    ) -> ParentExperimentEvaluation:
        if now < scientific_deadline:
            return evaluation
        if (
            evaluation.status == "partial"
            and evaluation.error
            and "deadline" in evaluation.error
        ):
            return evaluation
        if now >= absolute_process_deadline:
            error = f"external process deadline reached {phase} result publication"
        else:
            error = f"scientific deadline reached {phase} result publication"
        return ParentExperimentEvaluation(
            "partial",
            "incomplete",
            evaluation.residual_check,
            evaluation.comparisons,
            error,
        )

    def document_at(
        evaluation: ParentExperimentEvaluation,
        now: float,
    ) -> dict[str, object]:
        return _result_document(
            evaluation,
            inputs=inputs,
            implementation_revision=implementation_revision,
            source_replay_seconds=source_seconds,
            scientific_seconds=now - scientific_started,
            process_seconds=now - process_started,
            scientific_started=True,
        )

    def publish(evaluation: ParentExperimentEvaluation) -> dict[str, object]:
        nonlocal latest
        now = clock()
        evaluation = expire(evaluation, now, phase="before")
        latest = evaluation
        document = document_at(evaluation, now)
        validate_result_document(document)
        publish_result(output, document)
        published_at = clock()
        if published_at >= scientific_deadline:
            evaluation = expire(evaluation, published_at, phase="during")
            latest = evaluation
            document = document_at(evaluation, published_at)
            validate_result_document(document)
            publish_result(output, document)
        return document

    def checkpoint(evaluation: ParentExperimentEvaluation) -> None:
        document = publish(evaluation)
        clocks = _mapping(document["clocks"], "clocks")
        if (
            cast(float, clocks["process_seconds"])
            >= absolute_process_deadline - process_started
            or cast(float, clocks["scientific_seconds"]) >= SCIENTIFIC_ALLOWANCE_SECONDS
        ):
            raise ParentExperimentError(latest.error or "experiment deadline reached")

    initial = publish(latest)
    initial_clocks = _mapping(initial["clocks"], "clocks")
    if (
        cast(float, initial_clocks["process_seconds"])
        >= absolute_process_deadline - process_started
        or cast(float, initial_clocks["scientific_seconds"]) >= SCIENTIFIC_ALLOWANCE_SECONDS
    ):
        return initial
    try:
        evaluation = target(
            inputs,
            deadline=scientific_deadline,
            clock=clock,
            checkpoint=checkpoint,
        )
    except (OSError, ValueError) as error:
        evaluation = ParentExperimentEvaluation(
            "partial",
            "incomplete",
            latest.residual_check,
            latest.comparisons,
            f"scientific evaluation refused: {error}",
        )
    return publish(evaluation)


def _sequence(value: object, label: str) -> list[object]:
    if type(value) is not list:
        raise ParentExperimentError(f"{label} must be an array")
    return cast(list[object], value)


def _replay_b_only_record(
    record: dict[str, object],
    owner: SelectedOwnerAuthority,
    inputs: ParentAdapterInputs,
    *,
    deadline: float,
) -> None:
    expected_frames = len(owner.expected_frames)
    if record["expected_frames"] != expected_frames:
        raise ParentExperimentError("B-only result changed its bound frame count")
    saved_rows = _sequence(record["frame_extrema"], "b_only.frame_extrema")
    if record["checked_frames"] != len(saved_rows) or len(saved_rows) > expected_frames:
        raise ParentExperimentError("B-only result has inconsistent processed-frame counts")
    if record["status"] != "partial":
        replayed = evaluate_class(
            owner.wall_class,
            owner_mark=owner.owner_class.mark,
            corner_index=owner.corner_index,
            class_index=owner.class_index,
            transform=owner.physical_map,
            residual_centre=inputs.strict_escape.escape.centre,
            residual_u=inputs.selected_residual.ray,
            expected_frames=expected_frames,
            outer_side=GLOBAL_PARENT_RULE.outer_side,
            half=GLOBAL_PARENT_RULE.core_side / 2,
            deadline=deadline,
        )
        if b_only_result_record(replayed) != record:
            raise ParentExperimentError("B-only result differs from exact independent replay")
        return

    replayed_rows: list[FrameExtremum] = []
    for index, saved in enumerate(saved_rows):
        replayed = frame_separation_extremum(
            owner.wall_class.frames[index],
            frame_index=index,
            transform=owner.physical_map,
            residual_centre=inputs.strict_escape.escape.centre,
            residual_u=inputs.selected_residual.ray,
            half=GLOBAL_PARENT_RULE.core_side / 2,
            deadline=deadline,
        )
        if _frame_extremum_record(replayed) != saved:
            raise ParentExperimentError(
                f"B-only partial frame {index} differs from exact independent replay"
            )
        replayed_rows.append(replayed)
    observed = (
        None if not replayed_rows else str(max(row.maximum.slack for row in replayed_rows))
    )
    if (
        record["observed_maximum_slack"] != observed
        or record["global_maximum_slack"] is not None
        or not record["error"]
    ):
        raise ParentExperimentError("B-only partial result has invalid completion semantics")


def replay_parent_result_record(
    record: dict[str, object],
    owner: SelectedOwnerAuthority,
    inputs: ParentAdapterInputs,
    *,
    deadline: float,
    clock: Clock = time.perf_counter,
) -> None:
    """Recompute a saved parent row from bound source frames and exact geometry."""

    expected_frames = len(owner.expected_frames)
    if record["expected_frames"] != expected_frames:
        raise ParentExperimentError("parent result changed its bound frame count")
    if record["status"] != "unresolved":
        replayed = evaluate_parent_class(
            owner.wall_class.frames,
            owner.expected_frames,
            owner_mark=owner.owner_class.mark,
            transform=owner.physical_map,
            residual_centre=inputs.strict_escape.escape.centre,
            residual_u=inputs.selected_residual.ray,
            deadline=deadline,
            clock=clock,
        )
        if parent_result_record(replayed) != record:
            raise ParentExperimentError(
                "parent-restricted result differs from exact independent replay"
            )
        return

    saved_derived = _sequence(record["derived_frames"], "parent.derived_frames")
    saved_extrema = _sequence(record["frame_extrema"], "parent.frame_extrema")
    if len(saved_derived) > expected_frames:
        raise ParentExperimentError("parent partial result has extra derived frames")
    derived_rows: list[DerivedOwnerFrame] = []
    for index, saved in enumerate(saved_derived):
        derived = restrict_owner_centres(
            owner.wall_class.frames[index],
            owner_mark=owner.owner_class.mark,
        )
        if _derived_frame_record(index, derived) != saved:
            raise ParentExperimentError(
                f"parent partial derived frame {index} differs from independent replay"
            )
        derived_rows.append(derived)
    if saved_extrema and len(derived_rows) != expected_frames:
        raise ParentExperimentError(
            "parent partial extrema require the complete derived-frame manifest"
        )
    nonempty = [
        (index, row)
        for index, row in enumerate(derived_rows)
        if row.restricted.disposition == "allowed"
    ]
    if len(saved_extrema) > len(nonempty):
        raise ParentExperimentError("parent partial result has extra extrema")
    replayed_extrema: list[FrameExtremum] = []
    for position, saved in enumerate(saved_extrema):
        index, derived = nonempty[position]
        replayed = parent_frame_extremum(
            derived.restricted,
            frame_index=index,
            transform=owner.physical_map,
            residual_centre=inputs.strict_escape.escape.centre,
            residual_u=inputs.selected_residual.ray,
            half=GLOBAL_PARENT_RULE.core_side / 2,
            deadline=deadline,
            clock=clock,
        )
        if _frame_extremum_record(replayed) != saved:
            raise ParentExperimentError(
                f"parent partial extremum {position} differs from independent replay"
            )
        replayed_extrema.append(replayed)
    observed = (
        None
        if not replayed_extrema
        else str(max(row.maximum.slack for row in replayed_extrema))
    )
    if (
        record["observed_maximum_slack"] != observed
        or record["global_maximum_slack"] is not None
        or not record["error"]
    ):
        raise ParentExperimentError("parent partial result has invalid completion semantics")


def _replay_comparison_records(
    document: dict[str, object],
    inputs: ParentAdapterInputs,
    *,
    deadline: float,
    clock: Clock,
) -> None:
    rows = _sequence(document["comparisons"], "comparisons")
    owners = {owner.corner_index: owner for owner in inputs.selected_owners}
    expected_order = EVALUATION_CORNER_INDICES[: len(rows)]
    for position, (saved, corner_index) in enumerate(zip(rows, expected_order, strict=True)):
        row = _mapping(saved, f"comparisons[{position}]")
        owner = owners[corner_index]
        if (
            row["corner"] != owner.corner
            or row["corner_index"] != owner.corner_index
            or row["class_index"] != owner.class_index
            or row["class_id"] != owner.class_id
        ):
            raise ParentExperimentError("comparison order or selected-owner identity changed")
        b_only = _mapping(row["b_only"], f"comparisons[{position}].b_only")
        _replay_b_only_record(b_only, owner, inputs, deadline=deadline)
        b_status = b_only["status"]
        parent_value = row["parent_restricted"]
        if b_status == "partial":
            expected_status = "partial"
            expected_attribution = "unresolved"
            expected_error = b_only["error"]
            if parent_value is not None:
                raise ParentExperimentError("partial B-only result cannot have a parent row")
        elif b_status == "incompatible":
            expected_status = "complete"
            expected_attribution = "b-only-incompatible"
            expected_error = None
            if parent_value is not None:
                raise ParentExperimentError(
                    "incompatible B-only result cannot have a parent row"
                )
        else:
            parent = _mapping(
                parent_value,
                f"comparisons[{position}].parent_restricted",
            )
            replay_parent_result_record(
                parent,
                owner,
                inputs,
                deadline=deadline,
                clock=clock,
            )
            parent_status = parent["status"]
            if parent_status == "unresolved":
                expected_status = "partial"
                expected_attribution = "unresolved"
                expected_error = parent["error"]
            elif parent_status in ("incompatible", "impossible"):
                expected_status = "complete"
                expected_attribution = "owner-domain-gain"
                expected_error = None
            else:
                expected_status = "complete"
                expected_attribution = "still-compatible"
                expected_error = None
        if (
            row["status"] != expected_status
            or row["attribution"] != expected_attribution
            or row["error"] != expected_error
        ):
            raise ParentExperimentError("comparison attribution differs from replayed results")
        if position + 1 < len(rows) and expected_attribution != "still-compatible":
            raise ParentExperimentError("comparison rows continue after a terminal disposition")

    if document["status"] != "complete":
        return
    residual = _mapping(document["residual_check"], "residual_check")
    outcome = document["outcome"]
    if residual["status"] == "outside-parent-box":
        if rows or outcome != "residual-self-excluded":
            raise ParentExperimentError("residual self-exclusion completion is inconsistent")
        return
    if outcome == "b-only-incompatible":
        terminal = "b-only-incompatible"
    elif outcome == "owner-domain-gain":
        terminal = "owner-domain-gain"
    elif outcome == "no-owner-domain-exclusion":
        if len(rows) != len(EVALUATION_CORNER_INDICES):
            raise ParentExperimentError("all-compatible completion lacks four owner rows")
        terminal = "still-compatible"
    else:
        raise ParentExperimentError("complete result has no replay-supported outcome")
    if not rows or _mapping(rows[-1], "terminal comparison")["attribution"] != terminal:
        raise ParentExperimentError("complete outcome differs from its terminal comparison")


def load_parent_result(
    path: Path,
    pins: ParentInputPins,
    *,
    replay_deadline: float,
    loader: ParentInputLoader = load_parent_adapter_inputs,
    revision_validator: Callable[[Path, str], str] = validate_parent_readback_revision,
    clock: Clock = time.perf_counter,
) -> dict[str, object]:
    """Load, rebind, and exactly replay a result before returning it."""

    try:
        document = _mapping(_load_json(path.read_text(encoding="utf-8")), "result")
    except (OSError, json.JSONDecodeError) as error:
        raise ParentExperimentError(f"could not read parent result: {error}") from error
    validate_result_document(document)
    if document["status"] == "invalid":
        return document

    raw_sources = _mapping(document["sources"], "sources")
    implementation = _mapping(raw_sources["implementation"], "sources.implementation")
    revision = implementation["git_commit"]
    if type(revision) is not str:
        raise ParentExperimentError("implementation revision must be a string")
    if revision != pins.checkout_revision:
        raise ParentExperimentError("implementation and source checkout revisions differ")
    revision_validator(pins.repository_root, revision)
    inputs = loader(pins, replay_deadline=replay_deadline)
    if revision != inputs.checkout_revision:
        raise ParentExperimentError("implementation and loaded source revisions differ")
    if sources_record(inputs, implementation_revision=revision) != raw_sources:
        raise ParentExperimentError("result sources differ from independently bound receipts")
    if settings_record() != document["settings"]:
        raise ParentExperimentError("result settings differ from the frozen experiment")
    if authority_record(inputs) != document["authority"]:
        raise ParentExperimentError(
            "result authority differs from independently regenerated manifests"
        )
    expected_summary = {
        "expected_residual_orientations": 361,
        "bound_residual_orientations": len(inputs.residual_manifest),
        "expected_selected_owners": 4,
        "bound_selected_owners": len(inputs.selected_owners),
        "completed_comparisons": sum(
            _mapping(row, "comparison")["status"] == "complete"
            for row in cast(list[object], document["comparisons"])
        ),
    }
    if document["summary"] != expected_summary:
        raise ParentExperimentError("result summary differs from rebound authority and rows")
    if document["residual_check"] is not None:
        expected_residual = check_residual_parent_centre(
            inputs.strict_escape.escape.centre,
            inputs.selected_residual.ray,
            inputs.selected_residual.sources,
            inputs.residual_manifest[inputs.selected_residual.index].sources,
        )
        if residual_check_record(expected_residual) != document["residual_check"]:
            raise ParentExperimentError(
                "residual result differs from independent parent-box replay"
            )
    try:
        _replay_comparison_records(
            document,
            inputs,
            deadline=replay_deadline,
            clock=clock,
        )
    except ParentExperimentError:
        raise
    except (OSError, ValueError) as error:
        raise ParentExperimentError(
            f"comparison result could not be independently replayed: {error}"
        ) from error
    if clock() >= replay_deadline:
        raise ParentExperimentError("result readback exceeded its absolute process deadline")
    return document


def _identity_record(identity: TrackedReceiptIdentity) -> dict[str, object]:
    return {
        "path": identity.path,
        "git_commit": identity.git_commit,
        "git_blob": identity.git_blob,
        "producer_revision": identity.producer_revision,
    }


def sources_record(
    inputs: ParentAdapterInputs,
    *,
    implementation_revision: str,
) -> dict[str, object]:
    """Serialize every bound receipt identity and the instrument revision."""

    return {
        "implementation": {
            "git_commit": implementation_revision,
            "entry_point": "devtools.wall_owner_parent_experiment",
            "dependency_paths": list(IMPLEMENTATION_PATHS),
            "result_schema": RESULT_SCHEMA_PATH,
        },
        "endpoint": _identity_record(inputs.endpoint_identity),
        "wall": _identity_record(inputs.wall_identity),
        "selected_cover": _identity_record(inputs.selected_cover_identity),
        "strict_escape": _identity_record(inputs.strict_escape_identity),
    }


def settings_record() -> dict[str, object]:
    """Serialize the frozen scale, parent rule, target order, and clock budget."""

    return {
        "outer_side": str(GLOBAL_PARENT_RULE.outer_side),
        "core_side": str(GLOBAL_PARENT_RULE.core_side),
        "tangent_bound": str(GLOBAL_PARENT_RULE.tangent_bound),
        "parent_rule": GLOBAL_PARENT_RULE.mode,
        "selection_rule": GLOBAL_PARENT_RULE.selection_rule,
        "candidate": list(SELECTED_TUPLE),
        "physical_owner_order": list(PHYSICAL_OWNER_ORDER),
        "scientific_allowance_seconds": SCIENTIFIC_ALLOWANCE_SECONDS,
        "external_bound_seconds": EXTERNAL_BOUND_SECONDS,
        "termination_grace_seconds": TERMINATION_GRACE_SECONDS,
    }


def authority_record(inputs: ParentAdapterInputs) -> dict[str, object]:
    """Serialize independently regenerated residual and selected-owner authorities."""

    residual = [
        {
            "index": row.index,
            "label": row.label,
            "ray": _point_record(row.ray),
            "turned_ray": _point_record(row.turned_ray),
            "sources": _source_records(row.sources),
        }
        for row in inputs.residual_manifest
    ]
    owners = [
        {
            "corner": row.corner,
            "corner_index": row.corner_index,
            "class_index": row.class_index,
            "class_id": row.class_id,
            "owner_mark": _point_record(row.owner_class.mark),
            "physical_map": {
                "name": row.physical_map.name,
                "xx": row.physical_map.xx,
                "xy": row.physical_map.xy,
                "yx": row.physical_map.yx,
                "yy": row.physical_map.yy,
                "tx": str(row.physical_map.tx),
                "ty": str(row.physical_map.ty),
                "target_family": row.physical_map.target_family,
                "corner_permutation": list(row.physical_map.corner_permutation),
            },
            "expected_frames": [_frame_identity_record(frame) for frame in row.expected_frames],
        }
        for row in inputs.selected_owners
    ]
    return {
        "residual_manifest": residual,
        "selected_residual_index": inputs.selected_residual.index,
        "selected_owners": owners,
    }


def prepare_output_path(
    output: Path,
    *,
    repository: Path,
    inputs: tuple[Path, ...],
) -> Path:
    """Reserve a fresh JSON destination outside source, tests, and input receipts."""

    resolved = output.resolve()
    if any(resolved == path.resolve() for path in inputs):
        raise ParentExperimentError("output may not overwrite an input receipt")
    if resolved.exists() or resolved.suffix != ".json":
        raise ParentExperimentError("output must be a fresh JSON path")
    for relative in ("packing/devtools", "packing/tests", "packing/cases", "packing/src"):
        if resolved.is_relative_to(repository / relative):
            raise ParentExperimentError(
                "output may not be created inside project code or tests"
            )
    return resolved


def _mapping(value: object, label: str) -> dict[str, object]:
    if type(value) is not dict:
        raise ParentExperimentError(f"{label} must be an object")
    return cast(dict[str, object], value)


def _validate_comparison_completion(document: dict[str, object]) -> list[object]:
    rows = _sequence(document["comparisons"], "comparisons")
    terminal_seen = False
    for index, saved in enumerate(rows):
        row = _mapping(saved, f"comparisons[{index}]")
        if terminal_seen:
            raise ParentExperimentError("comparison rows continue after a terminal result")
        b_only = _mapping(row["b_only"], f"comparisons[{index}].b_only")
        parent_value = row["parent_restricted"]
        attribution = row["attribution"]
        if b_only["status"] == "partial":
            expected = ("partial", "unresolved", b_only["error"])
            terminal_seen = True
        elif b_only["status"] == "incompatible":
            expected = ("complete", "b-only-incompatible", None)
            terminal_seen = True
        else:
            parent = _mapping(
                parent_value,
                f"comparisons[{index}].parent_restricted",
            )
            if parent["status"] == "unresolved":
                expected = ("partial", "unresolved", parent["error"])
                terminal_seen = True
            elif parent["status"] in ("incompatible", "impossible"):
                expected = ("complete", "owner-domain-gain", None)
                terminal_seen = True
            else:
                expected = ("complete", "still-compatible", None)
        if parent_value is not None and b_only["status"] != "compatible":
            raise ParentExperimentError("parent result requires a compatible B-only control")
        if parent_value is None and b_only["status"] == "compatible":
            raise ParentExperimentError("compatible B-only control requires a parent result")
        if expected[0] == "partial" and not expected[2]:
            raise ParentExperimentError("partial comparison must retain its error")
        if (row["status"], attribution, row["error"]) != expected:
            raise ParentExperimentError("comparison completion fields are inconsistent")
    summary = _mapping(document["summary"], "summary")
    completed = sum(_mapping(row, "comparison")["status"] == "complete" for row in rows)
    if summary["completed_comparisons"] != completed:
        raise ParentExperimentError("summary completed count differs from comparison rows")
    return rows


def validate_result_document(document: dict[str, object]) -> None:
    """Validate the closed JSON shape and cross-field completion semantics."""

    try:
        schema = _mapping(json.loads(RESULT_SCHEMA.read_text(encoding="utf-8")), "schema")
    except (OSError, json.JSONDecodeError) as error:
        raise ParentExperimentError(f"could not read result schema: {error}") from error
    errors = list(Draft202012Validator(schema).iter_errors(document))
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.instance_path)
        suffix = f" at {location}" if location else ""
        raise ParentExperimentError(f"result schema violation{suffix}: {first.message}")

    clocks = _mapping(document["clocks"], "clocks")
    numeric_clocks: dict[str, int | float] = {}
    for field in ("source_replay_seconds", "scientific_seconds", "process_seconds"):
        value = clocks[field]
        if type(value) not in (int, float):
            raise ParentExperimentError(f"clocks.{field} must be finite and nonnegative")
        numeric = cast(int | float, value)
        if not math.isfinite(numeric) or numeric < 0:
            raise ParentExperimentError(f"clocks.{field} must be finite and nonnegative")
        numeric_clocks[field] = numeric
    if not math.isclose(
        numeric_clocks["process_seconds"],
        numeric_clocks["source_replay_seconds"] + numeric_clocks["scientific_seconds"],
        rel_tol=1e-12,
        abs_tol=1e-9,
    ):
        raise ParentExperimentError("process clock must equal replay plus scientific time")
    rows = _validate_comparison_completion(document)
    status = document["status"]
    if status == "invalid":
        summary = _mapping(document["summary"], "summary")
        if (
            document["outcome"] != "invalid"
            or not document["error"]
            or clocks["scientific_started"]
            or numeric_clocks["scientific_seconds"] != 0
            or document["sources"] is not None
            or document["settings"] is not None
            or document["authority"] is not None
            or document["residual_check"] is not None
            or rows
            or summary["bound_residual_orientations"] != 0
            or summary["bound_selected_owners"] != 0
        ):
            raise ParentExperimentError("invalid result has inconsistent preload semantics")
        return
    if document["sources"] is None or document["settings"] is None:
        raise ParentExperimentError("measured result must retain bound sources and settings")
    if document["authority"] is None:
        raise ParentExperimentError("measured result must retain independent authority")
    if not clocks["scientific_started"]:
        raise ParentExperimentError("measured result must record scientific clock start")
    if status == "partial":
        if document["outcome"] != "incomplete" or not document["error"]:
            raise ParentExperimentError("partial result must retain an incomplete reason")
        return
    if numeric_clocks["scientific_seconds"] >= SCIENTIFIC_ALLOWANCE_SECONDS:
        raise ParentExperimentError("complete result exceeds the scientific allowance")
    if numeric_clocks["process_seconds"] >= EXTERNAL_BOUND_SECONDS:
        raise ParentExperimentError("complete result exceeds the external process bound")
    if document["outcome"] in ("incomplete", "invalid") or document["error"] is not None:
        raise ParentExperimentError("complete result has an incomplete outcome or error")
    residual = _mapping(document["residual_check"], "residual_check")
    outcome = document["outcome"]
    if outcome == "residual-self-excluded":
        if residual["status"] != "outside-parent-box" or rows:
            raise ParentExperimentError("residual exclusion outcome is inconsistent")
    elif residual["status"] != "inside-parent-box":
        raise ParentExperimentError("owner comparison outcome requires an admitted residual")
    elif outcome == "b-only-incompatible":
        if not rows or _mapping(rows[-1], "comparison")["attribution"] != outcome:
            raise ParentExperimentError("B-only outcome lacks its terminal comparison")
    elif outcome == "owner-domain-gain":
        if not rows or _mapping(rows[-1], "comparison")["attribution"] != outcome:
            raise ParentExperimentError("parent gain outcome lacks its terminal comparison")
    elif outcome == "no-owner-domain-exclusion" and (
        len(rows) != len(EVALUATION_CORNER_INDICES)
        or any(_mapping(row, "comparison")["attribution"] != "still-compatible" for row in rows)
    ):
        raise ParentExperimentError("no-exclusion outcome lacks four compatible comparisons")


def write_result_document(path: Path, document: dict[str, object]) -> None:
    """Validate and atomically publish one complete result or partial checkpoint."""

    validate_result_document(document)
    rendered = json.dumps(document, indent=2, sort_keys=True) + "\n"
    atomic_write_text(path, rendered, make_parents=True)


def _receipt_paths(pins: ParentInputPins) -> tuple[Path, ...]:
    root = pins.repository_root
    return tuple(
        root / receipt.path
        for receipt in (
            pins.endpoint,
            pins.wall,
            pins.selected_cover,
            pins.strict_escape,
        )
    )


def _downgrade_after_failed_readback(
    output: Path,
    document: dict[str, object],
    *,
    error: str,
    process_seconds: float,
) -> None:
    if document["status"] not in ("complete", "partial"):
        return
    downgraded = dict(document)
    clocks = dict(_mapping(document["clocks"], "clocks"))
    source_seconds = cast(float, clocks["source_replay_seconds"])
    recorded_process_seconds = cast(float, clocks["process_seconds"])
    process_seconds = max(process_seconds, recorded_process_seconds)
    clocks["process_seconds"] = process_seconds
    clocks["scientific_seconds"] = max(0.0, process_seconds - source_seconds)
    downgraded["status"] = "partial"
    downgraded["outcome"] = "incomplete"
    downgraded["error"] = error
    downgraded["clocks"] = clocks
    write_result_document(output, downgraded)


def run_parent_worker(repository: Path, revision: str, output: Path) -> int:
    """Produce a candidate result and admit it only after independent readback."""

    started = time.perf_counter()
    validate_parent_implementation_revision(repository, revision)
    pins = retained_parent_input_pins(repository, revision)
    destination = prepare_output_path(
        output,
        repository=repository,
        inputs=_receipt_paths(pins),
    )
    process_deadline = started + EXTERNAL_BOUND_SECONDS
    document = execute_parent_experiment(
        pins,
        implementation_revision=revision,
        output=destination,
        process_deadline=process_deadline,
    )
    if document["status"] == "invalid":
        return 2
    try:
        rebound = load_parent_result(
            destination,
            pins,
            replay_deadline=process_deadline,
        )
    except (OSError, ValueError) as error:
        _downgrade_after_failed_readback(
            destination,
            document,
            error=f"independent readback refused: {error}",
            process_seconds=time.perf_counter() - started,
        )
        return 2
    if rebound["status"] != "complete":
        return 1
    print(f"validated result written to {destination}")
    return 0


def _write_unadmitted_worker_result(
    output: Path,
    error: str,
    *,
    process_seconds: float,
    rewrite_partial: bool = False,
) -> None:
    if output.exists():
        try:
            document = _mapping(_load_json(output.read_text(encoding="utf-8")), "result")
            validate_result_document(document)
        except OSError, ValueError:
            pass
        else:
            if document["status"] == "complete" or (
                rewrite_partial and document["status"] == "partial"
            ):
                _downgrade_after_failed_readback(
                    output,
                    document,
                    error=error,
                    process_seconds=process_seconds,
                )
                return
            return
    write_result_document(
        output,
        _invalid_document(
            error,
            source_replay_seconds=max(0.0, process_seconds),
            process_seconds=max(0.0, process_seconds),
        ),
    )


def supervise_parent_worker(command: Sequence[str], output: Path) -> int:
    """Enforce the external wall and two-second termination grace."""

    started = time.perf_counter()
    process = subprocess.Popen(command)
    try:
        status = process.wait(timeout=EXTERNAL_BOUND_SECONDS)
    except subprocess.TimeoutExpired:
        process.terminate()
        try:
            process.wait(timeout=TERMINATION_GRACE_SECONDS)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        _write_unadmitted_worker_result(
            output,
            "worker exceeded the 120-second external bound",
            process_seconds=max(
                EXTERNAL_BOUND_SECONDS,
                time.perf_counter() - started,
            ),
            rewrite_partial=True,
        )
        print(
            "unresolved: parent experiment reached its external process bound",
            file=sys.stderr,
        )
        return 1
    if status != 0:
        _write_unadmitted_worker_result(
            output,
            "worker exited before independent readback admission",
            process_seconds=time.perf_counter() - started,
        )
    return status


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--expect-implementation-revision", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the source-bound experiment in one externally supervised worker."""

    options = _parser().parse_args(argv)
    repository = options.repository.resolve()
    output = options.output.resolve()
    revision = cast(str, options.expect_implementation_revision)
    try:
        if options.worker:
            return run_parent_worker(repository, revision, output)
        validate_parent_implementation_revision(repository, revision)
        pins = retained_parent_input_pins(repository, revision)
        prepare_output_path(output, repository=repository, inputs=_receipt_paths(pins))
        command = (
            sys.executable,
            "-m",
            "devtools.wall_owner_parent_experiment",
            "--worker",
            "--repository",
            str(repository),
            "--expect-implementation-revision",
            revision,
            "--output",
            str(output),
        )
        return supervise_parent_worker(command, output)
    except (OSError, ValueError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
