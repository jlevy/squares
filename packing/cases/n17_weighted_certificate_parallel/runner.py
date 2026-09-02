"""Exact, parent-bound process profiler for three frozen n = 17 directions.

Workers write only disjoint fragments beneath a fresh exp-053 arm directory. The
parent validates and merges those fragments into a profile-only chain; no code here can
write the exp-052 checkpoint or progress files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing
import os
import shutil
import statistics
import tempfile
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass, replace
from fractions import Fraction
from pathlib import Path
from typing import Any, Literal

from cases.n17_weighted_certificate.fixture import load_retained_fixture
from cases.n17_weighted_certificate.model import (
    Atom,
    Direction,
    DirectionManifest,
    canonical_hash,
    canonical_json,
)
from cases.n17_weighted_certificate.source_faithful import accumulate_source_faithful
from cases.n17_weighted_certificate.target_independent import (
    accumulate_target_independent,
)
from cases.n17_weighted_certificate_resume.run import (
    FROZEN_PACKAGE_SHA256,
    fixture_binding_hash,
    verify_frozen_inputs,
)

type Arm = Literal["A", "B"]
type Order = Literal["AB", "BA"]

PACKING_ROOT = Path(__file__).resolve().parents[2]
RUNNER_PATH = Path(__file__)
BENCHMARK_PATH = PACKING_ROOT / "benchmarks/n17_weighted_certificate_parallel.py"
LAUNCH_REVISION = "909efafa0773fbea23b24de072ef59a03a01317a"
EXPERIMENT_ID = "exp-053"
HYPOTHESIS_ID = "H-057"
SESSION_ID = "session-073"
SELECTED_ORDINALS = (33, 107, 180)
PAIR_ORDERS: tuple[Order, ...] = ("AB", "BA", "AB")
WORKERS = 3
START_METHOD = "spawn"
SPEEDUP_THRESHOLD = 2.8
PARENT_CHECKPOINT_SHA256 = "db5c156959b6de4e6f2c9be283454d01dd5f3a436e6489f5e6bb60c38559fdb8"
PARENT_PROGRESS_SHA256 = "08e301b01c7ac6eef4b03c3a4daa5f72c5f1bdbe217dbbb061b57f5c94d947af"
PARENT_BINDING_HASH = "2446fa39e154800410b9b5cc19f19aed7cc0c797d116f7ece1c97a2c7c0b4d1a"
PARENT_ROW_HASH = "9badcc57c05e328344b0ec7ae4fbf9815e8eae027a79bec1bf1a35b9871fade6"
FIXTURE_HASH = "112fc6313def2fb05edd550e2948a1ed51bd262c581c55e52785973d31827a06"
DIRECTION_HASH = "cc789e1a16d190064a0eda2fe5e4bf0399d939362c85fb448f1162ef5cac4e79"
SOURCE_KERNEL_SHA256 = "aaccd145c61fb20bc2b83a8ded83dfdd3f2d4b6d6c730ff46df31e1f1d8ae305"
INDEPENDENT_KERNEL_SHA256 = "db86f6731180f8b82a9f54412c82713ac66ed9206458e222f8547574039a2ef0"
PARENT_CHECKPOINT = Path(
    "campaign/series/series-000-smoke-and-calibration/results/"
    "exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json"
)
PARENT_PROGRESS = Path(
    "campaign/series/series-000-smoke-and-calibration/results/"
    "exp-052-h-052-n17-resumable-certificate-agreement.progress.json"
)
RAW_ROOT = Path(
    "campaign/series/series-000-smoke-and-calibration/results/"
    "exp-053-h-057-n17-parent-bound-parallel-speedup.raw"
)
RESULT_PATH = Path(
    "campaign/series/series-000-smoke-and-calibration/results/"
    "exp-053-h-057-n17-parent-bound-parallel-speedup.json"
)
_SHA256 = frozenset("0123456789abcdef")


class ProfileError(RuntimeError):
    """A frozen-input, fragment, merge, cleanup, or timing guard failed."""


@dataclass(frozen=True, slots=True)
class ProfileBinding:
    schema_version: int
    experiment_id: str
    hypothesis_id: str
    session_id: str
    launch_revision: str
    parent_checkpoint_sha256: str
    parent_progress_sha256: str
    parent_binding_hash: str
    parent_previous_row_hash: str
    frozen_package_sha256: str
    fixture_hash: str
    direction_hash: str
    source_kernel_sha256: str
    independent_kernel_sha256: str
    runner_sha256: str
    benchmark_sha256: str
    ordinals: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class ProfileContext:
    binding: ProfileBinding
    atoms: tuple[Atom, ...]
    directions: tuple[Direction, ...]
    outer_side: Fraction
    square_side: Fraction


@dataclass(frozen=True, slots=True)
class WorkItem:
    binding_hash: str
    ordinal: int
    atoms: tuple[Atom, ...]
    direction: Direction
    outer_side: Fraction
    square_side: Fraction
    fragment_root: Path
    output_path: Path


@dataclass(frozen=True, slots=True)
class ProfileRow:
    ordinal: int
    direction: Direction
    source: DirectionManifest
    independent: DirectionManifest
    agreement: bool
    previous_row_hash: str
    row_hash: str


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_bytes(value: object) -> bytes:
    return (canonical_json(value) + "\n").encode()


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _write_exclusive(path: Path, content: bytes) -> None:
    """Publish complete bytes atomically without replacing an existing artifact."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError as error:
            raise ProfileError(f"refusing to replace existing artifact: {path}") from error
        _fsync_directory(path.parent)
    finally:
        temporary.unlink(missing_ok=True)


def _exact_object(value: object, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != fields:
        raise ProfileError(f"malformed {label}")
    return value


def _integer(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ProfileError(f"malformed {label}")
    return value


def _string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ProfileError(f"malformed {label}")
    return value


def _digest(value: object, label: str) -> str:
    digest = _string(value, label)
    if len(digest) != 64 or set(digest) - _SHA256:
        raise ProfileError(f"malformed {label}")
    return digest


def _fraction(value: object, label: str) -> Fraction:
    text = _string(value, label)
    try:
        parsed = Fraction(text)
    except (ValueError, ZeroDivisionError) as error:
        raise ProfileError(f"malformed {label}") from error
    if text != f"{parsed.numerator}/{parsed.denominator}":
        raise ProfileError(f"noncanonical {label}")
    return parsed


def _fraction_tuple(value: object, length: int | None, label: str) -> tuple[Fraction, ...]:
    if not isinstance(value, list) or (length is not None and len(value) != length):
        raise ProfileError(f"malformed {label}")
    return tuple(_fraction(item, f"{label}[{index}]") for index, item in enumerate(value))


def _direction(value: object, label: str = "direction") -> Direction:
    raw = _exact_object(value, {"label", "ux", "uy", "vx", "vy"}, label)
    return Direction(
        _string(raw["label"], f"{label}.label"),
        _fraction(raw["ux"], f"{label}.ux"),
        _fraction(raw["uy"], f"{label}.uy"),
        _fraction(raw["vx"], f"{label}.vx"),
        _fraction(raw["vy"], f"{label}.vy"),
    )


def _manifest(value: object, label: str) -> DirectionManifest:
    fields = {
        "label",
        "direction",
        "x_events",
        "y_events",
        "x_event_hash",
        "y_event_hash",
        "event_cell_count",
        "evaluated_state_count",
        "minimum",
        "witness",
    }
    raw = _exact_object(value, fields, label)
    direction = _fraction_tuple(raw["direction"], 4, f"{label}.direction")
    witness = _fraction_tuple(raw["witness"], 2, f"{label}.witness")
    return DirectionManifest(
        label=_string(raw["label"], f"{label}.label"),
        direction=(direction[0], direction[1], direction[2], direction[3]),
        x_events=_fraction_tuple(raw["x_events"], None, f"{label}.x_events"),
        y_events=_fraction_tuple(raw["y_events"], None, f"{label}.y_events"),
        x_event_hash=_digest(raw["x_event_hash"], f"{label}.x_event_hash"),
        y_event_hash=_digest(raw["y_event_hash"], f"{label}.y_event_hash"),
        event_cell_count=_integer(raw["event_cell_count"], f"{label}.event_cell_count"),
        evaluated_state_count=_integer(
            raw["evaluated_state_count"], f"{label}.evaluated_state_count"
        ),
        minimum=_fraction(raw["minimum"], f"{label}.minimum"),
        witness=(witness[0], witness[1]),
    )


def _validate_manifest(manifest: DirectionManifest, direction: Direction, label: str) -> None:
    expected_direction = (direction.ux, direction.uy, direction.vx, direction.vy)
    if manifest.label != direction.label or manifest.direction != expected_direction:
        raise ProfileError(f"{label} manifest direction mismatch")
    if manifest.x_event_hash != canonical_hash(manifest.x_events):
        raise ProfileError(f"{label} x-event hash mismatch")
    if manifest.y_event_hash != canonical_hash(manifest.y_events):
        raise ProfileError(f"{label} y-event hash mismatch")
    if manifest.event_cell_count != manifest.evaluated_state_count:
        raise ProfileError(f"{label} state count mismatch")


def _load_canonical(path: Path, label: str) -> object:
    try:
        content = path.read_bytes()
        value = json.loads(content)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ProfileError(f"unreadable {label}: {path}") from error
    if content != _canonical_bytes(value):
        raise ProfileError(f"noncanonical {label}: {path}")
    return value


def _normalized_atoms() -> tuple[Atom, ...]:
    fixture = load_retained_fixture()
    scale = Fraction(fixture.weight_scale)
    return tuple(
        Atom(atom.label, atom.x, atom.y, atom.weight / scale) for atom in fixture.atoms
    )


def _require_production_path(actual: Path, expected: Path, label: str) -> Path:
    if actual != expected or actual.is_absolute():
        raise ProfileError(f"{label} does not match exp-053 preregistration")
    resolved = (PACKING_ROOT / actual).resolve()
    expected_resolved = (PACKING_ROOT / expected).resolve()
    if resolved != expected_resolved or not resolved.is_relative_to(PACKING_ROOT.resolve()):
        raise ProfileError(f"{label} escapes the packing root")
    return resolved


def _validate_parent_checkpoint(value: object) -> None:
    raw = _exact_object(value, {"binding", "rows"}, "parent checkpoint")
    binding = raw["binding"]
    if not isinstance(binding, dict):
        raise ProfileError("malformed parent binding")
    expected_binding = {
        "experiment_id": "exp-052",
        "hypothesis_id": "H-052",
        "session_id": "session-068",
        "package_manifest_sha256": FROZEN_PACKAGE_SHA256,
        "fixture_hash": FIXTURE_HASH,
        "direction_hash": DIRECTION_HASH,
    }
    for key, expected in expected_binding.items():
        if binding.get(key) != expected:
            raise ProfileError(f"parent binding changed at {key}")
    rows = raw["rows"]
    if not isinstance(rows, list) or len(rows) != 33:
        raise ProfileError("parent checkpoint is not the reviewed 33-row prefix")
    previous = PARENT_BINDING_HASH
    for ordinal, value_row in enumerate(rows):
        row = _exact_object(
            value_row,
            {
                "ordinal",
                "direction",
                "source",
                "independent",
                "agreement",
                "previous_row_hash",
                "row_hash",
            },
            f"parent row {ordinal}",
        )
        if row["ordinal"] != ordinal or row["previous_row_hash"] != previous:
            raise ProfileError("parent row order or chain changed")
        if row["agreement"] is not True:
            raise ProfileError("parent checkpoint contains a disagreement")
        previous = _digest(row["row_hash"], f"parent row {ordinal} hash")
    if previous != PARENT_ROW_HASH:
        raise ProfileError("parent terminal row hash changed")


def _validate_parent_progress(value: object) -> None:
    marker = _exact_object(
        value,
        {"schema_version", "binding_hash", "ordinal", "stage", "previous_row_hash"},
        "parent progress",
    )
    expected = {
        "schema_version": 1,
        "binding_hash": PARENT_BINDING_HASH,
        "ordinal": 33,
        "stage": "independent_started",
        "previous_row_hash": PARENT_ROW_HASH,
    }
    if marker != expected:
        raise ProfileError("parent progress marker changed")


def load_parent_context(
    parent_checkpoint: Path = PARENT_CHECKPOINT,
    parent_progress: Path = PARENT_PROGRESS,
) -> ProfileContext:
    """Replay the frozen exp-052 boundary without evaluating a target direction."""

    checkpoint = _require_production_path(
        parent_checkpoint, PARENT_CHECKPOINT, "parent checkpoint path"
    )
    progress = _require_production_path(
        parent_progress, PARENT_PROGRESS, "parent progress path"
    )
    if _sha256(checkpoint) != PARENT_CHECKPOINT_SHA256:
        raise ProfileError("parent checkpoint digest changed")
    if _sha256(progress) != PARENT_PROGRESS_SHA256:
        raise ProfileError("parent progress digest changed")
    verify_frozen_inputs()
    _validate_parent_checkpoint(_load_canonical(checkpoint, "parent checkpoint"))
    _validate_parent_progress(_load_canonical(progress, "parent progress"))

    fixture = load_retained_fixture()
    atoms = _normalized_atoms()
    if canonical_hash(fixture.directions) != DIRECTION_HASH:
        raise ProfileError("retained direction hash changed")
    if (
        fixture_binding_hash(
            atoms=atoms,
            directions=fixture.directions,
            outer_side=fixture.outer_side,
            square_side=fixture.square_side,
        )
        != FIXTURE_HASH
    ):
        raise ProfileError("retained fixture binding changed")
    source_path = PACKING_ROOT / "cases/n17_weighted_certificate/source_faithful.py"
    independent_path = PACKING_ROOT / "cases/n17_weighted_certificate/target_independent.py"
    if _sha256(source_path) != SOURCE_KERNEL_SHA256:
        raise ProfileError("source-faithful kernel changed")
    if _sha256(independent_path) != INDEPENDENT_KERNEL_SHA256:
        raise ProfileError("independent kernel changed")
    binding = ProfileBinding(
        schema_version=1,
        experiment_id=EXPERIMENT_ID,
        hypothesis_id=HYPOTHESIS_ID,
        session_id=SESSION_ID,
        launch_revision=LAUNCH_REVISION,
        parent_checkpoint_sha256=PARENT_CHECKPOINT_SHA256,
        parent_progress_sha256=PARENT_PROGRESS_SHA256,
        parent_binding_hash=PARENT_BINDING_HASH,
        parent_previous_row_hash=PARENT_ROW_HASH,
        frozen_package_sha256=FROZEN_PACKAGE_SHA256,
        fixture_hash=FIXTURE_HASH,
        direction_hash=DIRECTION_HASH,
        source_kernel_sha256=SOURCE_KERNEL_SHA256,
        independent_kernel_sha256=INDEPENDENT_KERNEL_SHA256,
        runner_sha256=_sha256(RUNNER_PATH),
        benchmark_sha256=_sha256(BENCHMARK_PATH),
        ordinals=SELECTED_ORDINALS,
    )
    return ProfileContext(
        binding=binding,
        atoms=atoms,
        directions=fixture.directions,
        outer_side=fixture.outer_side,
        square_side=fixture.square_side,
    )


def profile_binding_hash(binding: ProfileBinding) -> str:
    return canonical_hash({"domain": "n17-parallel-profile-binding-v1", "binding": binding})


def _fragment_value(item: WorkItem) -> dict[str, object]:
    source = accumulate_source_faithful(
        item.atoms, item.direction, item.outer_side, item.square_side
    )
    independent = accumulate_target_independent(
        item.atoms, item.direction, item.outer_side, item.square_side
    )
    return {
        "schema_version": 1,
        "binding_hash": item.binding_hash,
        "ordinal": item.ordinal,
        "direction": item.direction,
        "source": source,
        "independent": independent,
        "agreement": source == independent,
    }


def _validate_fragment_path(item: WorkItem) -> None:
    expected_name = f"fragment-{item.ordinal:03d}.json"
    expected_path = item.fragment_root / expected_name
    if (
        item.fragment_root.is_symlink()
        or not item.fragment_root.is_dir()
        or item.output_path != expected_path
        or item.output_path.is_symlink()
    ):
        raise ProfileError("worker fragment path is not preassigned")
    try:
        resolved_root = item.fragment_root.resolve(strict=True)
        resolved_parent = item.output_path.parent.resolve(strict=True)
        resolved_output = item.output_path.resolve(strict=False)
    except OSError as error:
        raise ProfileError("worker fragment root is unreadable") from error
    if resolved_parent != resolved_root or resolved_output != resolved_root / expected_name:
        raise ProfileError("worker fragment path escapes its assigned root")


def write_fragment(item: WorkItem) -> str:
    """Compute one exact pair and publish it only at its preassigned fragment path."""

    _validate_fragment_path(item)
    _write_exclusive(item.output_path, _canonical_bytes(_fragment_value(item)))
    return item.output_path.as_posix()


def _parse_fragment(
    path: Path, *, binding_hash: str, ordinal: int, direction: Direction
) -> tuple[DirectionManifest, DirectionManifest]:
    raw = _exact_object(
        _load_canonical(path, "worker fragment"),
        {
            "schema_version",
            "binding_hash",
            "ordinal",
            "direction",
            "source",
            "independent",
            "agreement",
        },
        "worker fragment",
    )
    if raw["schema_version"] != 1 or raw["binding_hash"] != binding_hash:
        raise ProfileError("worker fragment has a foreign binding")
    if raw["ordinal"] != ordinal or _direction(raw["direction"]) != direction:
        raise ProfileError("worker fragment ordinal or direction changed")
    source = _manifest(raw["source"], "source")
    independent = _manifest(raw["independent"], "independent")
    _validate_manifest(source, direction, "source")
    _validate_manifest(independent, direction, "independent")
    agreement = raw["agreement"]
    if not isinstance(agreement, bool) or agreement != (source == independent):
        raise ProfileError("worker fragment agreement flag changed")
    if not agreement:
        raise ProfileError("unchanged exact accumulators disagree")
    return source, independent


def merge_fragments(fragment_dir: Path, context: ProfileContext) -> bytes:
    """Validate the complete selected set and derive one deterministic child chain."""

    expected_names = {f"fragment-{ordinal:03d}.json" for ordinal in context.binding.ordinals}
    try:
        entries = {path.name for path in fragment_dir.iterdir()}
    except OSError as error:
        raise ProfileError("fragment directory is unreadable") from error
    if entries != expected_names:
        raise ProfileError("fragment set has a gap, duplicate, extra, or partial file")
    binding_digest = profile_binding_hash(context.binding)
    rows: list[ProfileRow] = []
    previous = context.binding.parent_previous_row_hash
    for ordinal in context.binding.ordinals:
        direction = context.directions[ordinal]
        source, independent = _parse_fragment(
            fragment_dir / f"fragment-{ordinal:03d}.json",
            binding_hash=binding_digest,
            ordinal=ordinal,
            direction=direction,
        )
        row_hash = canonical_hash(
            {
                "domain": "n17-parallel-profile-row-v1",
                "ordinal": ordinal,
                "direction": direction,
                "source": source,
                "independent": independent,
                "agreement": True,
                "previous_row_hash": previous,
            }
        )
        rows.append(
            ProfileRow(
                ordinal=ordinal,
                direction=direction,
                source=source,
                independent=independent,
                agreement=True,
                previous_row_hash=previous,
                row_hash=row_hash,
            )
        )
        previous = row_hash
    return _canonical_bytes(
        {"schema_version": 1, "binding": context.binding, "rows": tuple(rows)}
    )


def _jobs(fragment_dir: Path, context: ProfileContext) -> list[WorkItem]:
    digest = profile_binding_hash(context.binding)
    return [
        WorkItem(
            binding_hash=digest,
            ordinal=ordinal,
            atoms=context.atoms,
            direction=context.directions[ordinal],
            outer_side=context.outer_side,
            square_side=context.square_side,
            fragment_root=fragment_dir,
            output_path=fragment_dir / f"fragment-{ordinal:03d}.json",
        )
        for ordinal in context.binding.ordinals
    ]


def _remove_partial(path: Path, pair_root: Path) -> None:
    if path.is_symlink() or path.parent.resolve() != pair_root.resolve():
        raise ProfileError("refusing unsafe partial-arm cleanup")
    if not path.name.startswith(".arm-") or ".partial-" not in path.name:
        raise ProfileError("refusing unrecognized partial-arm cleanup")
    shutil.rmtree(path)
    _fsync_directory(pair_root)


def cleanup_partial_arms(pair_root: Path, arm: Arm) -> int:
    removed = 0
    for path in pair_root.glob(f".arm-{arm}.partial-*"):
        _remove_partial(path, pair_root)
        removed += 1
    return removed


def _arm_mode(arm: Arm) -> Literal["serial", "parallel"]:
    return "serial" if arm == "A" else "parallel"


def _require_parallel_regime(workers: int, start_method: str) -> None:
    if workers != WORKERS or start_method != START_METHOD:
        raise ProfileError("parallel arm regime changed")


def _require_absent_final(final: Path) -> None:
    if final.exists() or final.is_symlink():
        raise ProfileError("durable arm appeared during exclusive publication")


def _load_arm(arm_dir: Path, arm: Arm, context: ProfileContext) -> dict[str, Any]:
    if arm_dir.is_symlink() or not arm_dir.is_dir():
        raise ProfileError("durable arm is not a real directory")
    expected = {"fragments", "merged.json", "receipt.json"}
    if {path.name for path in arm_dir.iterdir()} != expected:
        raise ProfileError("durable arm contains missing or extra artifacts")
    merged = merge_fragments(arm_dir / "fragments", context)
    if (arm_dir / "merged.json").read_bytes() != merged:
        raise ProfileError("durable arm merged bytes changed")
    receipt = _exact_object(
        _load_canonical(arm_dir / "receipt.json", "arm receipt"),
        {
            "schema_version",
            "arm",
            "mode",
            "elapsed_ns",
            "worker_count",
            "start_method",
            "cold_process_start",
            "merged_sha256",
            "fragment_sha256",
        },
        "arm receipt",
    )
    elapsed = _integer(receipt["elapsed_ns"], "arm elapsed_ns")
    if elapsed == 0 or receipt["arm"] != arm or receipt["mode"] != _arm_mode(arm):
        raise ProfileError("arm receipt identity changed")
    if receipt["merged_sha256"] != hashlib.sha256(merged).hexdigest():
        raise ProfileError("arm receipt merged digest changed")
    fragment_hashes = [
        _sha256(arm_dir / "fragments" / f"fragment-{ordinal:03d}.json")
        for ordinal in context.binding.ordinals
    ]
    if receipt["fragment_sha256"] != fragment_hashes:
        raise ProfileError("arm receipt fragment digests changed")
    expected_workers = 1 if arm == "A" else WORKERS
    expected_start = "inline" if arm == "A" else START_METHOD
    if (
        receipt["worker_count"] != expected_workers
        or receipt["start_method"] != expected_start
        or receipt["cold_process_start"] is not (arm == "B")
    ):
        raise ProfileError("arm execution regime changed")
    return receipt


def run_arm(
    pair_root: Path,
    arm: Arm,
    context: ProfileContext,
    *,
    workers: int = WORKERS,
    start_method: str = START_METHOD,
) -> dict[str, Any]:
    """Run or replay one durable arm, cleaning only its incomplete private directory."""

    final = pair_root / f"arm-{arm}"
    if final.exists() or final.is_symlink():
        return _load_arm(final, arm, context)
    cleanup_partial_arms(pair_root, arm)
    started = time.monotonic_ns()
    work = Path(tempfile.mkdtemp(dir=pair_root, prefix=f".arm-{arm}.partial-"))
    fragments = work / "fragments"
    fragments.mkdir()
    try:
        jobs = _jobs(fragments, context)
        if arm == "A":
            for job in jobs:
                write_fragment(job)
        else:
            _require_parallel_regime(workers, start_method)
            process_context = multiprocessing.get_context(start_method)
            pool = process_context.Pool(processes=workers)
            try:
                pool.map(write_fragment, jobs)
            except BaseException:
                pool.terminate()
                pool.join()
                raise
            else:
                pool.close()
                pool.join()
        merged = merge_fragments(fragments, context)
        _write_exclusive(work / "merged.json", merged)
        elapsed = time.monotonic_ns() - started
        receipt = {
            "schema_version": 1,
            "arm": arm,
            "mode": _arm_mode(arm),
            "elapsed_ns": elapsed,
            "worker_count": 1 if arm == "A" else workers,
            "start_method": "inline" if arm == "A" else start_method,
            "cold_process_start": arm == "B",
            "merged_sha256": hashlib.sha256(merged).hexdigest(),
            "fragment_sha256": [
                _sha256(fragments / f"fragment-{ordinal:03d}.json")
                for ordinal in context.binding.ordinals
            ],
        }
        _write_exclusive(work / "receipt.json", _canonical_bytes(receipt))
        _require_absent_final(final)
        work.rename(final)
        _fsync_directory(pair_root)
        return _load_arm(final, arm, context)
    except BaseException:
        if work.exists():
            _remove_partial(work, pair_root)
        raise


def _pair_root(pair_index: int, order: Order) -> Path:
    return RAW_ROOT / f"pair-{pair_index:02d}-{order.lower()}"


def _pair_binding(context: ProfileContext, pair_index: int, order: Order) -> dict[str, object]:
    return {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "session_id": SESSION_ID,
        "profile_binding_hash": profile_binding_hash(context.binding),
        "pair_index": pair_index,
        "order": order,
        "arms": {"A": "serial", "B": "parallel"},
        "workers": WORKERS,
        "start_method": START_METHOD,
    }


def _initialize_pair_root(
    output_root: Path, context: ProfileContext, pair_index: int, order: Order
) -> None:
    expected = _pair_root(pair_index, order)
    _require_production_path(output_root, expected, "pair output root")
    actual = PACKING_ROOT / output_root
    actual.parent.mkdir(parents=True, exist_ok=True)
    if not actual.exists():
        actual.mkdir()
        _fsync_directory(actual.parent)
    if actual.is_symlink() or not actual.is_dir():
        raise ProfileError("pair output root is not a real directory")
    binding_path = actual / "pair-binding.json"
    expected_bytes = _canonical_bytes(_pair_binding(context, pair_index, order))
    if binding_path.exists():
        if binding_path.read_bytes() != expected_bytes:
            raise ProfileError("pair binding changed")
    else:
        if any(actual.iterdir()):
            raise ProfileError("unbound pair root is not empty")
        _write_exclusive(binding_path, expected_bytes)


def _pair_receipt(
    pair_index: int,
    order: Order,
    serial: dict[str, Any],
    parallel: dict[str, Any],
) -> dict[str, object]:
    serial_ns = _integer(serial["elapsed_ns"], "serial elapsed_ns")
    parallel_ns = _integer(parallel["elapsed_ns"], "parallel elapsed_ns")
    return {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "session_id": SESSION_ID,
        "pair_index": pair_index,
        "order": order,
        "serial_ns": serial_ns,
        "parallel_ns": parallel_ns,
        "speedup": serial_ns / parallel_ns,
        "paired_change": (parallel_ns - serial_ns) / serial_ns,
        "merged_sha256": serial["merged_sha256"],
        "fragment_sha256": serial["fragment_sha256"],
        "exact_fragment_bytes": serial["fragment_sha256"] == parallel["fragment_sha256"],
        "exact_merged_bytes": serial["merged_sha256"] == parallel["merged_sha256"],
    }


def _load_pair(
    pair_root: Path, context: ProfileContext, pair_index: int, order: Order
) -> dict[str, Any]:
    expected_entries = {"pair-binding.json", "arm-A", "arm-B", "pair.json"}
    actual_entries = {path.name for path in pair_root.iterdir()}
    if pair_root.is_symlink() or actual_entries != expected_entries:
        raise ProfileError("pair is incomplete or contains extra artifacts")
    if (pair_root / "pair-binding.json").read_bytes() != _canonical_bytes(
        _pair_binding(context, pair_index, order)
    ):
        raise ProfileError("pair binding changed")
    serial = _load_arm(pair_root / "arm-A", "A", context)
    parallel = _load_arm(pair_root / "arm-B", "B", context)
    expected = _pair_receipt(pair_index, order, serial, parallel)
    actual = _load_canonical(pair_root / "pair.json", "pair receipt")
    if actual != expected:
        raise ProfileError("pair receipt changed")
    if not expected["exact_fragment_bytes"] or not expected["exact_merged_bytes"]:
        raise ProfileError("serial and parallel exact bytes differ")
    return expected


def validate_pair_parameters(
    *,
    experiment: str,
    session: str,
    parent_checkpoint: Path,
    parent_progress: Path,
    ordinals: tuple[int, ...],
    workers: int,
    start_method: str,
    pair_index: int,
    order: str,
    output_root: Path,
) -> Order:
    if experiment != EXPERIMENT_ID or session != SESSION_ID:
        raise ProfileError("experiment or session id changed")
    if parent_checkpoint != PARENT_CHECKPOINT or parent_progress != PARENT_PROGRESS:
        raise ProfileError("parent path changed")
    if ordinals != SELECTED_ORDINALS or workers != WORKERS or start_method != START_METHOD:
        raise ProfileError("fixed ordinal or process regime changed")
    if pair_index not in (1, 2, 3):
        raise ProfileError("pair index is outside the fixed three-pair profile")
    expected_order = PAIR_ORDERS[pair_index - 1]
    if order != expected_order:
        raise ProfileError("pair ordering changed")
    typed_order: Order = expected_order
    if output_root != _pair_root(pair_index, typed_order):
        raise ProfileError("pair output root changed")
    return typed_order


def run_pair(
    *,
    experiment: str,
    session: str,
    parent_checkpoint: Path,
    parent_progress: Path,
    ordinals: tuple[int, ...],
    workers: int,
    start_method: str,
    pair_index: int,
    order: str,
    output_root: Path,
) -> dict[str, Any]:
    typed_order = validate_pair_parameters(
        experiment=experiment,
        session=session,
        parent_checkpoint=parent_checkpoint,
        parent_progress=parent_progress,
        ordinals=ordinals,
        workers=workers,
        start_method=start_method,
        pair_index=pair_index,
        order=order,
        output_root=output_root,
    )
    context = load_parent_context(parent_checkpoint, parent_progress)
    _initialize_pair_root(output_root, context, pair_index, typed_order)
    root = PACKING_ROOT / output_root
    pair_path = root / "pair.json"
    if pair_path.exists():
        return _load_pair(root, context, pair_index, typed_order)
    receipts: dict[Arm, dict[str, Any]] = {}
    for arm_text in typed_order:
        arm: Arm = "A" if arm_text == "A" else "B"
        receipts[arm] = run_arm(root, arm, context, workers=workers, start_method=start_method)
    serial = receipts.get("A") or _load_arm(root / "arm-A", "A", context)
    parallel = receipts.get("B") or _load_arm(root / "arm-B", "B", context)
    receipt = _pair_receipt(pair_index, typed_order, serial, parallel)
    if not receipt["exact_fragment_bytes"] or not receipt["exact_merged_bytes"]:
        raise ProfileError("serial and parallel exact bytes differ")
    _write_exclusive(pair_path, _canonical_bytes(receipt))
    return _load_pair(root, context, pair_index, typed_order)


def _median(values: list[int] | list[float]) -> int | float:
    return statistics.median(values)


def validate_assemble_parameters(
    *, experiment: str, session: str, raw_root: Path, record: Path
) -> None:
    if experiment != EXPERIMENT_ID or session != SESSION_ID:
        raise ProfileError("experiment or session id changed")
    _require_production_path(raw_root, RAW_ROOT, "raw root")
    _require_production_path(record, RESULT_PATH, "result path")


def _assemble_pair_set(
    *,
    context: ProfileContext,
    raw_root: Path,
    record: Path,
    raw_root_label: str,
) -> dict[str, object]:
    if record.exists() or record.is_symlink():
        raise ProfileError("refusing to replace existing exp-053 result")
    expected_pairs = {
        f"pair-{index:02d}-{order.lower()}" for index, order in enumerate(PAIR_ORDERS, start=1)
    }
    if (
        raw_root.is_symlink()
        or not raw_root.is_dir()
        or {path.name for path in raw_root.iterdir()} != expected_pairs
    ):
        raise ProfileError("raw root does not contain exactly three fixed pairs")
    pairs = [
        _load_pair(raw_root / f"pair-{index:02d}-{order.lower()}", context, index, order)
        for index, order in enumerate(PAIR_ORDERS, start=1)
    ]
    serial = [_integer(pair["serial_ns"], "serial_ns") for pair in pairs]
    parallel = [_integer(pair["parallel_ns"], "parallel_ns") for pair in pairs]
    speedups = [float(pair["speedup"]) for pair in pairs]
    changes = [float(pair["paired_change"]) for pair in pairs]
    median_speedup = float(_median(speedups))
    minimum_speedup = min(speedups)
    change_pct = float(_median(changes)) * 100
    passes = median_speedup >= SPEEDUP_THRESHOLD and minimum_speedup > 1.0
    result = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "hypothesis_id": HYPOTHESIS_ID,
        "session_id": SESSION_ID,
        "launch_revision": LAUNCH_REVISION,
        "profile_binding": asdict(context.binding),
        "profile_binding_hash": profile_binding_hash(context.binding),
        "raw_root": raw_root_label,
        "pair_orders": PAIR_ORDERS,
        "pairs": pairs,
        "serial_ns": serial,
        "parallel_ns": parallel,
        "speedups": speedups,
        "paired_changes": changes,
        "serial_median_ns": _median(serial),
        "parallel_median_ns": _median(parallel),
        "serial_range_ns": [min(serial), max(serial)],
        "parallel_range_ns": [min(parallel), max(parallel)],
        "median_paired_change_pct": change_pct,
        "median_paired_speedup": median_speedup,
        "minimum_paired_speedup": minimum_speedup,
        "threshold": SPEEDUP_THRESHOLD,
        "exact_fragment_bytes": all(pair["exact_fragment_bytes"] for pair in pairs),
        "exact_merged_bytes": all(pair["exact_merged_bytes"] for pair in pairs),
        "passes_acceptance": passes,
        "decision": "accepted" if passes else "rejected",
        "profile_only": True,
        "needs_review": True,
        "does_not_decide": ["H-052", "exp-052"],
    }
    _write_exclusive(record, _canonical_bytes(result))
    return result


def assemble_profile(
    *, experiment: str, session: str, raw_root: Path, record: Path
) -> dict[str, object]:
    validate_assemble_parameters(
        experiment=experiment, session=session, raw_root=raw_root, record=record
    )
    context = load_parent_context()
    return _assemble_pair_set(
        context=context,
        raw_root=PACKING_ROOT / raw_root,
        record=PACKING_ROOT / record,
        raw_root_label=RAW_ROOT.as_posix(),
    )


def _synthetic_context() -> ProfileContext:
    atoms = (
        Atom("a", Fraction(1, 2), Fraction(1, 2), Fraction(1)),
        Atom("b", Fraction(1), Fraction(1), Fraction(2)),
        Atom("c", Fraction(3, 2), Fraction(3, 2), Fraction(3)),
    )
    directions = (
        Direction("axis", Fraction(1), Fraction(0), Fraction(0), Fraction(1)),
        Direction(
            "three-four",
            Fraction(3, 5),
            Fraction(4, 5),
            Fraction(-4, 5),
            Fraction(3, 5),
        ),
        Direction(
            "five-twelve",
            Fraction(5, 13),
            Fraction(12, 13),
            Fraction(-12, 13),
            Fraction(5, 13),
        ),
    )
    digest = "0" * 64
    binding = ProfileBinding(
        schema_version=1,
        experiment_id=EXPERIMENT_ID,
        hypothesis_id=HYPOTHESIS_ID,
        session_id=SESSION_ID,
        launch_revision="synthetic-selftest",
        parent_checkpoint_sha256=digest,
        parent_progress_sha256=digest,
        parent_binding_hash=digest,
        parent_previous_row_hash=digest,
        frozen_package_sha256=digest,
        fixture_hash=canonical_hash(atoms),
        direction_hash=canonical_hash(directions),
        source_kernel_sha256=digest,
        independent_kernel_sha256=digest,
        runner_sha256=_sha256(RUNNER_PATH),
        benchmark_sha256=_sha256(BENCHMARK_PATH),
        ordinals=(0, 1, 2),
    )
    return ProfileContext(
        binding=binding,
        atoms=atoms,
        directions=directions,
        outer_side=Fraction(2),
        square_side=Fraction(1),
    )


def _merge_rejects(fragment_dir: Path, context: ProfileContext) -> bool:
    try:
        merge_fragments(fragment_dir, context)
    except ProfileError:
        return True
    return False


def _copy_fragments(source: Path, root: Path, name: str) -> Path:
    destination = root / name
    shutil.copytree(source, destination)
    return destination


def _rewrite_canonical(path: Path, value: object) -> None:
    """Rewrite an intentional selftest mutation inside a disposable directory."""

    path.write_bytes(_canonical_bytes(value))


def _action_rejects(action: Callable[[], object]) -> bool:
    try:
        action()
    except ProfileError:
        return True
    return False


def _set_synthetic_elapsed(
    pair_root: Path,
    arm: Arm,
    context: ProfileContext,
    elapsed_ns: int,
) -> dict[str, Any]:
    receipt_path = pair_root / f"arm-{arm}/receipt.json"
    receipt = _load_canonical(receipt_path, "synthetic arm receipt")
    if not isinstance(receipt, dict):
        raise ProfileError("malformed synthetic arm receipt")
    receipt["elapsed_ns"] = elapsed_ns
    _rewrite_canonical(receipt_path, receipt)
    return _load_arm(pair_root / f"arm-{arm}", arm, context)


def _publish_synthetic_pair(
    *,
    raw_root: Path,
    context: ProfileContext,
    pair_index: int,
    order: Order,
    serial_ns: int,
    parallel_ns: int,
) -> dict[str, Any]:
    pair_root = raw_root / f"pair-{pair_index:02d}-{order.lower()}"
    pair_root.mkdir()
    _write_exclusive(
        pair_root / "pair-binding.json",
        _canonical_bytes(_pair_binding(context, pair_index, order)),
    )
    for arm_text in order:
        arm: Arm = "A" if arm_text == "A" else "B"
        run_arm(pair_root, arm, context)
    serial = _set_synthetic_elapsed(pair_root, "A", context, serial_ns)
    parallel = _set_synthetic_elapsed(pair_root, "B", context, parallel_ns)
    receipt = _pair_receipt(pair_index, order, serial, parallel)
    _write_exclusive(pair_root / "pair.json", _canonical_bytes(receipt))
    return _load_pair(pair_root, context, pair_index, order)


def run_selftest() -> dict[str, object]:
    """Fire every target-blind worker, merge, pair, and assembler guard."""

    guards: dict[str, bool] = {}
    children_before = {process.pid for process in multiprocessing.active_children()}
    with tempfile.TemporaryDirectory(prefix="n17-parallel-selftest-") as temporary:
        root = Path(temporary)
        context = _synthetic_context()

        assigned_root = root / "assigned-fragment-root"
        assigned_root.mkdir()
        assigned_job = _jobs(assigned_root, context)[0]
        outside_root = root / "outside-fragment-root"
        outside_root.mkdir()
        escaped_path = outside_root / assigned_job.output_path.name
        escaped_job = replace(assigned_job, output_path=escaped_path)
        guards["same_basename_outside_root_rejected"] = _action_rejects(
            lambda: write_fragment(escaped_job)
        )
        guards["same_basename_outside_root_absent"] = not escaped_path.exists()

        real_root = root / "real-fragment-root"
        real_root.mkdir()
        symlink_root = root / "symlink-fragment-root"
        symlink_root.symlink_to(real_root, target_is_directory=True)
        symlink_job = replace(
            assigned_job,
            fragment_root=symlink_root,
            output_path=symlink_root / assigned_job.output_path.name,
        )
        guards["symlink_fragment_root_rejected"] = (
            _action_rejects(lambda: write_fragment(symlink_job))
            and not (real_root / assigned_job.output_path.name).exists()
        )
        symlink_root.unlink()
        assigned_root.rmdir()
        outside_root.rmdir()
        real_root.rmdir()

        serial = run_arm(root, "A", context)
        serial_receipt = (root / "arm-A/receipt.json").read_bytes()
        guards["interrupted_pair_preserves_first_arm"] = (
            not (root / "pair.json").exists() and (root / "arm-A").is_dir()
        )
        parallel = run_arm(root, "B", context)
        source = root / "arm-A/fragments"
        parallel_receipt = (root / "arm-B/receipt.json").read_bytes()
        guards["spawn_fragment_bytes"] = (
            serial["fragment_sha256"] == parallel["fragment_sha256"]
        )
        guards["spawn_merged_bytes"] = serial["merged_sha256"] == parallel["merged_sha256"]
        guards["complete_serial_replay"] = (
            run_arm(root, "A", context) == serial
            and (root / "arm-A/receipt.json").read_bytes() == serial_receipt
        )
        guards["complete_parallel_replay"] = (
            run_arm(root, "B", context) == parallel
            and (root / "arm-B/receipt.json").read_bytes() == parallel_receipt
        )
        pair_binding = _pair_binding(context, 1, "AB")
        pair_receipt = _pair_receipt(1, "AB", serial, parallel)
        _write_exclusive(root / "pair-binding.json", _canonical_bytes(pair_binding))
        _write_exclusive(root / "pair.json", _canonical_bytes(pair_receipt))
        guards["resumed_pair_receipt"] = _load_pair(root, context, 1, "AB") == pair_receipt

        merged = json.loads(merge_fragments(source, context))
        rows = merged.get("rows") if isinstance(merged, dict) else None
        guards["deterministic_ordinal_order"] = isinstance(rows, list) and [
            row.get("ordinal") for row in rows if isinstance(row, dict)
        ] == [0, 1, 2]
        previous = context.binding.parent_previous_row_hash
        chain_valid = isinstance(rows, list)
        if isinstance(rows, list):
            for row in rows:
                if not isinstance(row, dict) or row.get("previous_row_hash") != previous:
                    chain_valid = False
                    break
                previous = str(row.get("row_hash"))
        guards["deterministic_parent_chain"] = chain_valid

        gap = _copy_fragments(source, root, "mutation-gap")
        (gap / "fragment-001.json").unlink()
        guards["gap_rejected"] = _merge_rejects(gap, context)

        extra = _copy_fragments(source, root, "mutation-duplicate")
        shutil.copy2(extra / "fragment-000.json", extra / "fragment-999.json")
        guards["duplicate_rejected"] = _merge_rejects(extra, context)

        reordered = _copy_fragments(source, root, "mutation-reorder")
        first = reordered / "fragment-000.json"
        second = reordered / "fragment-001.json"
        first_bytes, second_bytes = first.read_bytes(), second.read_bytes()
        first.write_bytes(second_bytes)
        second.write_bytes(first_bytes)
        guards["reorder_rejected"] = _merge_rejects(reordered, context)

        foreign = _copy_fragments(source, root, "mutation-foreign-parent")
        foreign_path = foreign / "fragment-000.json"
        foreign_value = json.loads(foreign_path.read_bytes())
        foreign_value["binding_hash"] = "f" * 64
        _rewrite_canonical(foreign_path, foreign_value)
        guards["foreign_parent_rejected"] = _merge_rejects(foreign, context)

        partial = _copy_fragments(source, root, "mutation-partial")
        (partial / "fragment-000.json").write_bytes(b"{")
        guards["partial_rejected"] = _merge_rejects(partial, context)

        event_hash = _copy_fragments(source, root, "mutation-event-hash")
        event_path = event_hash / "fragment-000.json"
        event_value = json.loads(event_path.read_bytes())
        event_value["source"]["x_event_hash"] = "f" * 64
        _rewrite_canonical(event_path, event_value)
        guards["event_hash_rejected"] = _merge_rejects(event_hash, context)

        flag = _copy_fragments(source, root, "mutation-agreement-flag")
        flag_path = flag / "fragment-000.json"
        flag_value = json.loads(flag_path.read_bytes())
        flag_value["agreement"] = False
        _rewrite_canonical(flag_path, flag_value)
        guards["agreement_flag_rejected"] = _merge_rejects(flag, context)

        assembly_raw = root / "assembly-raw"
        assembly_raw.mkdir()
        controlled_times = ((300, 100), (290, 100), (280, 100))
        for pair_index, (order, times) in enumerate(
            zip(PAIR_ORDERS, controlled_times, strict=True), start=1
        ):
            _publish_synthetic_pair(
                raw_root=assembly_raw,
                context=context,
                pair_index=pair_index,
                order=order,
                serial_ns=times[0],
                parallel_ns=times[1],
            )
        assembly_record = root / "assembly-result.json"
        assembled = _assemble_pair_set(
            context=context,
            raw_root=assembly_raw,
            record=assembly_record,
            raw_root_label="synthetic-selftest/assembly-raw",
        )
        pairs = assembled["pairs"]
        guards["assembler_requires_fixed_three_pairs"] = (
            isinstance(pairs, list)
            and [pair.get("pair_index") for pair in pairs if isinstance(pair, dict)]
            == [1, 2, 3]
            and assembled["pair_orders"] == PAIR_ORDERS
        )
        guards["assembler_recomputes_median"] = assembled["median_paired_speedup"] == 2.9
        guards["assembler_recomputes_minimum"] = assembled["minimum_paired_speedup"] == 2.8
        guards["assembler_recomputes_acceptance"] = (
            assembled["passes_acceptance"] is True and assembled["decision"] == "accepted"
        )
        guards["assembler_preserves_claim_boundary"] = (
            assembled["profile_only"] is True
            and assembled["needs_review"] is True
            and assembled["does_not_decide"] == ["H-052", "exp-052"]
        )
        guards["assembler_refuses_result_overwrite"] = _action_rejects(
            lambda: _assemble_pair_set(
                context=context,
                raw_root=assembly_raw,
                record=assembly_record,
                raw_root_label="synthetic-selftest/assembly-raw",
            )
        )

        missing_raw = root / "assembly-missing-pair"
        shutil.copytree(assembly_raw, missing_raw)
        shutil.rmtree(missing_raw / "pair-03-ab")
        guards["assembler_refuses_missing_pair"] = _action_rejects(
            lambda: _assemble_pair_set(
                context=context,
                raw_root=missing_raw,
                record=root / "assembly-missing-result.json",
                raw_root_label="synthetic-selftest/assembly-missing-pair",
            )
        )

        corrupt_raw = root / "assembly-corrupt-pair"
        shutil.copytree(assembly_raw, corrupt_raw)
        corrupt_receipt_path = corrupt_raw / "pair-02-ba/pair.json"
        corrupt_receipt = _load_canonical(corrupt_receipt_path, "synthetic pair receipt")
        if not isinstance(corrupt_receipt, dict):
            raise ProfileError("malformed synthetic pair receipt")
        corrupt_receipt["serial_ns"] = 291
        _rewrite_canonical(corrupt_receipt_path, corrupt_receipt)
        guards["assembler_refuses_corrupt_pair"] = _action_rejects(
            lambda: _assemble_pair_set(
                context=context,
                raw_root=corrupt_raw,
                record=root / "assembly-corrupt-result.json",
                raw_root_label="synthetic-selftest/assembly-corrupt-pair",
            )
        )

        minimum_raw = root / "assembly-minimum-guard"
        shutil.copytree(assembly_raw, minimum_raw)
        minimum_pair = minimum_raw / "pair-03-ab"
        minimum_serial = _load_arm(minimum_pair / "arm-A", "A", context)
        minimum_parallel = _set_synthetic_elapsed(minimum_pair, "B", context, 280)
        _rewrite_canonical(
            minimum_pair / "pair.json",
            _pair_receipt(3, "AB", minimum_serial, minimum_parallel),
        )
        minimum_result = _assemble_pair_set(
            context=context,
            raw_root=minimum_raw,
            record=root / "assembly-minimum-result.json",
            raw_root_label="synthetic-selftest/assembly-minimum-guard",
        )
        guards["assembler_enforces_minimum_speedup"] = (
            minimum_result["median_paired_speedup"] == 2.9
            and minimum_result["minimum_paired_speedup"] == 1.0
            and minimum_result["passes_acceptance"] is False
            and minimum_result["decision"] == "rejected"
        )

        stale = root / ".arm-B.partial-interrupted"
        stale.mkdir()
        (stale / "partial.json").write_bytes(b"{")
        guards["confined_partial_cleanup"] = cleanup_partial_arms(root, "B") == 1
        guards["no_partial_survived"] = not list(root.glob(".arm-*.partial-*"))
    guards["no_child_survived"] = {
        process.pid for process in multiprocessing.active_children()
    } == children_before
    return {
        "schema_version": 1,
        "passed": all(guards.values()),
        "guard_count": len(guards),
        "skips": 0,
        "guards": guards,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subcommands = parser.add_subparsers(dest="command", required=True)
    pair = subcommands.add_parser("pair")
    pair.add_argument("--experiment", required=True)
    pair.add_argument("--session", required=True)
    pair.add_argument("--parent-checkpoint", type=Path, required=True)
    pair.add_argument("--parent-progress", type=Path, required=True)
    pair.add_argument("--ordinals", type=int, nargs=3, required=True)
    pair.add_argument("--workers", type=int, required=True)
    pair.add_argument("--start-method", required=True)
    pair.add_argument("--pair-index", type=int, required=True)
    pair.add_argument("--order", required=True)
    pair.add_argument("--output-root", type=Path, required=True)
    assemble = subcommands.add_parser("assemble")
    assemble.add_argument("--experiment", required=True)
    assemble.add_argument("--session", required=True)
    assemble.add_argument("--raw-root", type=Path, required=True)
    assemble.add_argument("--record", type=Path, required=True)
    subcommands.add_parser("selftest")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "pair":
        receipt = run_pair(
            experiment=args.experiment,
            session=args.session,
            parent_checkpoint=args.parent_checkpoint,
            parent_progress=args.parent_progress,
            ordinals=tuple(args.ordinals),
            workers=args.workers,
            start_method=args.start_method,
            pair_index=args.pair_index,
            order=args.order,
            output_root=args.output_root,
        )
    elif args.command == "assemble":
        receipt = assemble_profile(
            experiment=args.experiment,
            session=args.session,
            raw_root=args.raw_root,
            record=args.record,
        )
    else:
        receipt = run_selftest()
    print(canonical_json(receipt))
    return 0
