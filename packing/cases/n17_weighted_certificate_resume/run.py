"""Direction-sliced execution and atomic checkpoints for the frozen n = 17 kernels.

This module does not load the retained target on import.  It supplies a process wrapper
around the byte-frozen source-faithful and independent per-direction functions.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from collections.abc import Callable
from dataclasses import asdict, dataclass, replace
from fractions import Fraction
from pathlib import Path
from typing import Any, Literal

from cases.n17_weighted_certificate.fixture import (
    RETAINED_SHA256,
    RetainedFixture,
    load_retained_fixture,
)
from cases.n17_weighted_certificate.model import (
    Atom,
    CertificateManifest,
    Direction,
    DirectionManifest,
    canonical_hash,
    canonical_json,
)
from cases.n17_weighted_certificate.run import (
    CLEAN_ROOM_SHA256,
    _first_disagreement,  # pyright: ignore[reportPrivateUsage]
    _mutation_guards,  # pyright: ignore[reportPrivateUsage]
    _normalized_atoms,  # pyright: ignore[reportPrivateUsage]
    _preconditions,  # pyright: ignore[reportPrivateUsage]
)
from cases.n17_weighted_certificate.source_faithful import (
    accumulate_source_faithful,
)
from cases.n17_weighted_certificate.target_independent import (
    accumulate_target_independent,
)

PACKING_ROOT = Path(__file__).resolve().parents[2]
FROZEN_PACKAGE = PACKING_ROOT / "cases/n17_weighted_certificate"
DRIVER_PATH = Path(__file__)
FROZEN_PACKAGE_SHA256 = (
    "309ec24158f73dd2e9b837c773b1e5c1642f357de5bdf73311b73232abdb6d54"
)
FROZEN_SOURCE_SHA256 = (
    (
        "resources/web/n17-lower-bounds-2026/README.md",
        "b48c0c31cf62366d44cd12f02cf321dd38b5a23391caec95f04445938e0b3d75",
    ),
    (
        "resources/web/n17-lower-bounds-2026/massaccesi-linear-programming.html",
        "cdd27897f4f6c3b83835d59a317b3248b4f94b888f8568b740c778524a11f177",
    ),
    (
        "resources/web/n17-lower-bounds-2026/massaccesi-lower-bound-4_5058.html",
        "7dffb6e6e6cbff0ac2e887ca445b45f46c95055718219f7229d1c8cb06f84514",
    ),
    (
        (
            "resources/web/n17-lower-bounds-2026/"
            "massaccesi-verify-n17-lower-bound-4_5058.py"
        ),
        "04531a54da9a654f2318401aff43222daf721bd99e948b2491f91c05bd0b5d3f",
    ),
)
SCHEMA_VERSION = 1
EXPERIMENT_ID = "exp-052"
HYPOTHESIS_ID = "H-052"
SESSION_ID = "session-068"
RESULT_PATH = (
    "campaign/series/series-000-smoke-and-calibration/results/"
    "exp-052-h-052-n17-resumable-certificate-agreement.json"
)
CHECKPOINT_PATH = (
    "campaign/series/series-000-smoke-and-calibration/results/"
    "exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json"
)
PROGRESS_PATH = (
    "campaign/series/series-000-smoke-and-calibration/results/"
    "exp-052-h-052-n17-resumable-certificate-agreement.progress.json"
)
_FRACTION = re.compile(r"-?(?:0|[1-9][0-9]*)/[1-9][0-9]*\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_EXPERIMENT = re.compile(r"exp-[0-9]{3}\Z")

type Accumulator = Callable[
    [tuple[Atom, ...], Direction, Fraction, Fraction], DirectionManifest
]
type ProgressStage = Literal[
    "source_started", "source_complete", "independent_started"
]
_PROGRESS_STAGES: tuple[ProgressStage, ...] = (
    "source_started",
    "source_complete",
    "independent_started",
)


class CheckpointError(RuntimeError):
    """A provenance, atomicity, or resume invariant failed."""


@dataclass(frozen=True, slots=True)
class RunBinding:
    """Immutable provenance and path binding for one preregistered round."""

    schema_version: int
    experiment_id: str
    hypothesis_id: str
    session_id: str
    package_manifest_sha256: str
    source_sha256: tuple[tuple[str, str], ...]
    fixture_hash: str
    direction_count: int
    direction_hash: str
    driver_sha256: str
    result_path: str
    checkpoint_path: str
    progress_path: str


@dataclass(frozen=True, slots=True)
class PairedRow:
    """One complete source/independent direction pair and its hash-chain link."""

    ordinal: int
    direction: Direction
    source: DirectionManifest
    independent: DirectionManifest
    agreement: bool
    previous_row_hash: str
    row_hash: str


@dataclass(frozen=True, slots=True)
class Checkpoint:
    """A contiguous prefix of complete paired direction rows."""

    binding: RunBinding
    rows: tuple[PairedRow, ...]


@dataclass(frozen=True, slots=True)
class ProgressMarker:
    """Non-scientific location marker; never a completed direction row."""

    schema_version: int
    binding_hash: str
    ordinal: int
    stage: ProgressStage
    previous_row_hash: str


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_package_manifest_sha256() -> str:
    """Reproduce the frozen sorted ``sha256sum`` package-manifest digest."""

    lines = []
    for path in sorted(FROZEN_PACKAGE.rglob("*.py")):
        relative = path.relative_to(PACKING_ROOT).as_posix()
        lines.append(f"{_sha256(path)}  {relative}\n")
    return hashlib.sha256("".join(lines).encode()).hexdigest()


def driver_sha256() -> str:
    """Hash the external execution driver independently of the frozen package."""

    return _sha256(DRIVER_PATH)


def fixture_binding_hash(
    *,
    atoms: tuple[Atom, ...],
    directions: tuple[Direction, ...],
    outer_side: Fraction,
    square_side: Fraction,
) -> str:
    """Bind the exact process inputs without evaluating a target direction."""

    return canonical_hash(
        {
            "atoms": atoms,
            "directions": directions,
            "outer_side": outer_side,
            "square_side": square_side,
        }
    )


def verify_frozen_inputs() -> None:
    """Refuse a run unless every frozen source and package digest still matches."""

    package = frozen_package_manifest_sha256()
    if package != FROZEN_PACKAGE_SHA256:
        raise CheckpointError(
            f"frozen package mismatch: expected {FROZEN_PACKAGE_SHA256}, got {package}"
        )
    for relative, expected in FROZEN_SOURCE_SHA256:
        actual = _sha256(PACKING_ROOT / relative)
        if actual != expected:
            raise CheckpointError(
                f"frozen source mismatch for {relative}: expected {expected}, got {actual}"
            )


def binding_hash(binding: RunBinding) -> str:
    """Return the genesis hash for a round binding."""

    return canonical_hash({"domain": "n17-resume-binding-v1", "binding": binding})


def _row_hash(
    *,
    ordinal: int,
    direction: Direction,
    source: DirectionManifest,
    independent: DirectionManifest,
    agreement: bool,
    previous_row_hash: str,
) -> str:
    return canonical_hash(
        {
            "domain": "n17-resume-paired-row-v1",
            "ordinal": ordinal,
            "direction": direction,
            "source": source,
            "independent": independent,
            "agreement": agreement,
            "previous_row_hash": previous_row_hash,
        }
    )


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        temporary.unlink(missing_ok=True)


def _durable_unlink(path: Path) -> None:
    if not path.exists():
        return
    path.unlink()
    directory = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


def _exact_object(value: object, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != fields:
        raise CheckpointError(f"malformed {label}")
    return value


def _string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise CheckpointError(f"malformed {label}")
    return value


def _digest(value: object, label: str) -> str:
    digest = _string(value, label)
    if _SHA256.fullmatch(digest) is None:
        raise CheckpointError(f"malformed {label}")
    return digest


def _integer(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise CheckpointError(f"malformed {label}")
    return value


def _fraction(value: object, label: str) -> Fraction:
    text = _string(value, label)
    if _FRACTION.fullmatch(text) is None:
        raise CheckpointError(f"malformed {label}")
    parsed = Fraction(text)
    if text != f"{parsed.numerator}/{parsed.denominator}":
        raise CheckpointError(f"noncanonical {label}")
    return parsed


def _fraction_tuple(value: object, length: int, label: str) -> tuple[Fraction, ...]:
    if not isinstance(value, list) or len(value) != length:
        raise CheckpointError(f"malformed {label}")
    return tuple(_fraction(item, f"{label}[{index}]") for index, item in enumerate(value))


def _direction(value: object) -> Direction:
    raw = _exact_object(value, {"label", "ux", "uy", "vx", "vy"}, "direction")
    return Direction(
        _string(raw["label"], "direction.label"),
        _fraction(raw["ux"], "direction.ux"),
        _fraction(raw["uy"], "direction.uy"),
        _fraction(raw["vx"], "direction.vx"),
        _fraction(raw["vy"], "direction.vy"),
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
    x_events = _fraction_tuple(
        raw["x_events"], len(raw["x_events"]) if isinstance(raw["x_events"], list) else -1,
        f"{label}.x_events",
    )
    y_events = _fraction_tuple(
        raw["y_events"], len(raw["y_events"]) if isinstance(raw["y_events"], list) else -1,
        f"{label}.y_events",
    )
    witness = _fraction_tuple(raw["witness"], 2, f"{label}.witness")
    return DirectionManifest(
        label=_string(raw["label"], f"{label}.label"),
        direction=(direction[0], direction[1], direction[2], direction[3]),
        x_events=x_events,
        y_events=y_events,
        x_event_hash=_digest(raw["x_event_hash"], f"{label}.x_event_hash"),
        y_event_hash=_digest(raw["y_event_hash"], f"{label}.y_event_hash"),
        event_cell_count=_integer(raw["event_cell_count"], f"{label}.event_cell_count"),
        evaluated_state_count=_integer(
            raw["evaluated_state_count"], f"{label}.evaluated_state_count"
        ),
        minimum=_fraction(raw["minimum"], f"{label}.minimum"),
        witness=(witness[0], witness[1]),
    )


def _binding(value: object) -> RunBinding:
    fields = {field.name for field in RunBinding.__dataclass_fields__.values()}
    raw = _exact_object(value, fields, "binding")
    source = raw["source_sha256"]
    if not isinstance(source, list):
        raise CheckpointError("malformed binding.source_sha256")
    source_rows: list[tuple[str, str]] = []
    for index, row in enumerate(source):
        if not isinstance(row, list) or len(row) != 2:
            raise CheckpointError(f"malformed binding.source_sha256[{index}]")
        source_rows.append(
            (
                _string(row[0], f"binding.source_sha256[{index}].path"),
                _digest(row[1], f"binding.source_sha256[{index}].hash"),
            )
        )
    return RunBinding(
        schema_version=_integer(raw["schema_version"], "binding.schema_version"),
        experiment_id=_string(raw["experiment_id"], "binding.experiment_id"),
        hypothesis_id=_string(raw["hypothesis_id"], "binding.hypothesis_id"),
        session_id=_string(raw["session_id"], "binding.session_id"),
        package_manifest_sha256=_digest(
            raw["package_manifest_sha256"], "binding.package_manifest_sha256"
        ),
        source_sha256=tuple(source_rows),
        fixture_hash=_digest(raw["fixture_hash"], "binding.fixture_hash"),
        direction_count=_integer(raw["direction_count"], "binding.direction_count"),
        direction_hash=_digest(raw["direction_hash"], "binding.direction_hash"),
        driver_sha256=_digest(raw["driver_sha256"], "binding.driver_sha256"),
        result_path=_string(raw["result_path"], "binding.result_path"),
        checkpoint_path=_string(raw["checkpoint_path"], "binding.checkpoint_path"),
        progress_path=_string(raw["progress_path"], "binding.progress_path"),
    )


def _paired_row(value: object) -> PairedRow:
    fields = {
        "ordinal",
        "direction",
        "source",
        "independent",
        "agreement",
        "previous_row_hash",
        "row_hash",
    }
    raw = _exact_object(value, fields, "paired row")
    agreement = raw["agreement"]
    if not isinstance(agreement, bool):
        raise CheckpointError("malformed paired row agreement")
    return PairedRow(
        ordinal=_integer(raw["ordinal"], "paired row ordinal"),
        direction=_direction(raw["direction"]),
        source=_manifest(raw["source"], "paired row source"),
        independent=_manifest(raw["independent"], "paired row independent"),
        agreement=agreement,
        previous_row_hash=_digest(raw["previous_row_hash"], "previous row hash"),
        row_hash=_digest(raw["row_hash"], "row hash"),
    )


def _progress_marker(value: object) -> ProgressMarker:
    raw = _exact_object(
        value,
        {"schema_version", "binding_hash", "ordinal", "stage", "previous_row_hash"},
        "progress marker",
    )
    stage = _string(raw["stage"], "progress marker stage")
    if stage not in _PROGRESS_STAGES:
        raise CheckpointError("malformed progress marker stage")
    return ProgressMarker(
        schema_version=_integer(raw["schema_version"], "progress marker schema"),
        binding_hash=_digest(raw["binding_hash"], "progress marker binding hash"),
        ordinal=_integer(raw["ordinal"], "progress marker ordinal"),
        stage=stage,
        previous_row_hash=_digest(
            raw["previous_row_hash"], "progress marker previous row hash"
        ),
    )


def _validate_manifest(manifest: DirectionManifest, direction: Direction, label: str) -> None:
    expected_direction = (direction.ux, direction.uy, direction.vx, direction.vy)
    if manifest.label != direction.label or manifest.direction != expected_direction:
        raise CheckpointError(f"{label} manifest direction mismatch")
    if manifest.x_event_hash != canonical_hash(manifest.x_events):
        raise CheckpointError(f"{label} x-event hash mismatch")
    if manifest.y_event_hash != canonical_hash(manifest.y_events):
        raise CheckpointError(f"{label} y-event hash mismatch")


def _checkpoint_json(checkpoint: Checkpoint) -> str:
    return canonical_json({"binding": checkpoint.binding, "rows": checkpoint.rows}) + "\n"


class CheckpointStore:
    """Atomically persist and validate a single bound checkpoint prefix."""

    def __init__(
        self,
        *,
        binding: RunBinding,
        directions: tuple[Direction, ...],
        result_path: Path,
        checkpoint_path: Path,
        progress_path: Path,
        production: bool = False,
        progress_remover: Callable[[Path], None] = _durable_unlink,
    ) -> None:
        self.binding = binding
        self.directions = directions
        self.result_path = result_path
        self.checkpoint_path = checkpoint_path
        self.progress_path = progress_path
        self.production = production
        self.progress_remover = progress_remover
        self._validate_binding()

    def _validate_binding(self) -> None:
        if self.binding.schema_version != SCHEMA_VERSION:
            raise CheckpointError("unsupported checkpoint schema version")
        if self.binding.hypothesis_id != HYPOTHESIS_ID:
            raise CheckpointError("checkpoint is not bound to H-052")
        if self.binding.session_id != SESSION_ID:
            raise CheckpointError("checkpoint is not bound to session-068")
        if self.binding.experiment_id != EXPERIMENT_ID:
            raise CheckpointError("checkpoint is not bound to exp-052")
        if self.binding.package_manifest_sha256 != FROZEN_PACKAGE_SHA256:
            raise CheckpointError("binding does not name the frozen package")
        if self.binding.driver_sha256 != driver_sha256():
            raise CheckpointError("external driver hash mismatch")
        if self.binding.source_sha256 != FROZEN_SOURCE_SHA256:
            raise CheckpointError("binding does not name the frozen source set")
        if self.binding.direction_count != len(self.directions):
            raise CheckpointError("binding direction count mismatch")
        if self.binding.direction_hash != canonical_hash(self.directions):
            raise CheckpointError("binding direction hash mismatch")
        if self.binding.result_path != str(self.result_path):
            raise CheckpointError("binding result path mismatch")
        if self.binding.checkpoint_path != str(self.checkpoint_path):
            raise CheckpointError("binding checkpoint path mismatch")
        if self.binding.progress_path != str(self.progress_path):
            raise CheckpointError("binding progress path mismatch")
        if self.production and (
            self.binding.result_path != RESULT_PATH
            or self.binding.checkpoint_path != CHECKPOINT_PATH
            or self.binding.progress_path != PROGRESS_PATH
        ):
            raise CheckpointError("production paths do not match exp-052 preregistration")

    def refuse_existing_result(self) -> None:
        if self.result_path.exists():
            raise CheckpointError("result path already exists")

    def initialize(self) -> Checkpoint:
        self.refuse_existing_result()
        if self.checkpoint_path.exists():
            checkpoint = self.load()
            self.read_progress(checkpoint)
            return checkpoint
        if self.progress_path.exists():
            raise CheckpointError("progress marker exists without a checkpoint")
        checkpoint = Checkpoint(self.binding, ())
        _atomic_write(self.checkpoint_path, _checkpoint_json(checkpoint))
        return checkpoint

    def load(self) -> Checkpoint:
        self.refuse_existing_result()
        try:
            text = self.checkpoint_path.read_text(encoding="utf-8")
            value = json.loads(text)
        except (OSError, json.JSONDecodeError) as error:
            raise CheckpointError("checkpoint is unreadable") from error
        raw = _exact_object(value, {"binding", "rows"}, "checkpoint")
        parsed_binding = _binding(raw["binding"])
        if parsed_binding != self.binding:
            raise CheckpointError("checkpoint binding changed")
        raw_rows = raw["rows"]
        if not isinstance(raw_rows, list):
            raise CheckpointError("malformed checkpoint rows")
        rows = tuple(_paired_row(row) for row in raw_rows)
        self._validate_rows(rows)
        checkpoint = Checkpoint(parsed_binding, rows)
        if text != _checkpoint_json(checkpoint):
            raise CheckpointError("checkpoint serialization is not canonical")
        return checkpoint

    def read_progress(self, checkpoint: Checkpoint | None = None) -> ProgressMarker | None:
        """Validate progress; a valid stale marker never outranks the checkpoint."""

        if not self.progress_path.exists():
            return None
        if checkpoint is None:
            checkpoint = self.load()
        try:
            text = self.progress_path.read_text(encoding="utf-8")
            marker = _progress_marker(json.loads(text))
        except (OSError, json.JSONDecodeError) as error:
            raise CheckpointError("progress marker is unreadable") from error
        if text != canonical_json(marker) + "\n":
            raise CheckpointError("progress marker serialization is not canonical")
        if marker.schema_version != SCHEMA_VERSION:
            raise CheckpointError("progress marker schema changed")
        if marker.binding_hash != binding_hash(self.binding):
            raise CheckpointError("progress marker binding changed")
        if marker.ordinal > len(checkpoint.rows):
            raise CheckpointError("progress marker is ahead of checkpoint")
        expected_previous = (
            binding_hash(self.binding)
            if marker.ordinal == 0
            else checkpoint.rows[marker.ordinal - 1].row_hash
        )
        if marker.previous_row_hash != expected_previous:
            raise CheckpointError("progress marker chain changed")
        if marker.ordinal < len(checkpoint.rows):
            self.progress_remover(self.progress_path)
            return None
        if marker.ordinal >= len(self.directions):
            raise CheckpointError("progress marker is beyond final direction")
        return marker

    def _validate_rows(self, rows: tuple[PairedRow, ...]) -> None:
        if len(rows) > len(self.directions):
            raise CheckpointError("checkpoint contains too many rows")
        previous = binding_hash(self.binding)
        for ordinal, row in enumerate(rows):
            if row.ordinal != ordinal:
                raise CheckpointError("checkpoint ordinals are not contiguous")
            if row.direction != self.directions[ordinal]:
                raise CheckpointError("checkpoint direction order changed")
            _validate_manifest(row.source, row.direction, "source")
            _validate_manifest(row.independent, row.direction, "independent")
            if row.previous_row_hash != previous:
                raise CheckpointError("checkpoint hash chain changed")
            if row.agreement != (row.source == row.independent):
                raise CheckpointError("checkpoint agreement flag changed")
            expected = _row_hash(
                ordinal=row.ordinal,
                direction=row.direction,
                source=row.source,
                independent=row.independent,
                agreement=row.agreement,
                previous_row_hash=row.previous_row_hash,
            )
            if row.row_hash != expected:
                raise CheckpointError("checkpoint row hash changed")
            previous = row.row_hash

    def write_progress(self, ordinal: int, stage: ProgressStage) -> ProgressMarker:
        checkpoint = self.load()
        if ordinal != len(checkpoint.rows) or ordinal >= len(self.directions):
            raise CheckpointError("progress ordinal is not the first incomplete direction")
        previous = (
            checkpoint.rows[-1].row_hash
            if checkpoint.rows
            else binding_hash(self.binding)
        )
        marker = ProgressMarker(
            schema_version=SCHEMA_VERSION,
            binding_hash=binding_hash(self.binding),
            ordinal=ordinal,
            stage=stage,
            previous_row_hash=previous,
        )
        _atomic_write(self.progress_path, canonical_json(marker) + "\n")
        return marker

    def append_pair(
        self,
        *,
        direction: Direction,
        source: DirectionManifest,
        independent: DirectionManifest,
    ) -> Checkpoint:
        checkpoint = self.load()
        ordinal = len(checkpoint.rows)
        if ordinal >= len(self.directions) or direction != self.directions[ordinal]:
            raise CheckpointError("paired row is not the first incomplete direction")
        _validate_manifest(source, direction, "source")
        _validate_manifest(independent, direction, "independent")
        previous = (
            checkpoint.rows[-1].row_hash
            if checkpoint.rows
            else binding_hash(self.binding)
        )
        agreement = source == independent
        digest = _row_hash(
            ordinal=ordinal,
            direction=direction,
            source=source,
            independent=independent,
            agreement=agreement,
            previous_row_hash=previous,
        )
        row = PairedRow(
            ordinal=ordinal,
            direction=direction,
            source=source,
            independent=independent,
            agreement=agreement,
            previous_row_hash=previous,
            row_hash=digest,
        )
        updated = Checkpoint(self.binding, (*checkpoint.rows, row))
        _atomic_write(self.checkpoint_path, _checkpoint_json(updated))
        self.progress_remover(self.progress_path)
        return updated


class DirectionSlicedDriver:
    """Run each unchanged accumulator and commit only complete direction pairs."""

    def __init__(
        self,
        store: CheckpointStore,
        *,
        source_accumulator: Accumulator = accumulate_source_faithful,
        independent_accumulator: Accumulator = accumulate_target_independent,
    ) -> None:
        self.store = store
        self.source_accumulator = source_accumulator
        self.independent_accumulator = independent_accumulator

    def run(
        self,
        *,
        atoms: tuple[Atom, ...],
        outer_side: Fraction,
        square_side: Fraction,
    ) -> Checkpoint:
        verify_frozen_inputs()
        actual_fixture_hash = fixture_binding_hash(
            atoms=atoms,
            directions=self.store.directions,
            outer_side=outer_side,
            square_side=square_side,
        )
        if actual_fixture_hash != self.store.binding.fixture_hash:
            raise CheckpointError("fixture binding changed")
        checkpoint = self.store.initialize()
        for ordinal in range(len(checkpoint.rows), len(self.store.directions)):
            direction = self.store.directions[ordinal]
            self.store.write_progress(ordinal, "source_started")
            source = self.source_accumulator(atoms, direction, outer_side, square_side)
            self.store.write_progress(ordinal, "source_complete")
            self.store.write_progress(ordinal, "independent_started")
            independent = self.independent_accumulator(
                atoms, direction, outer_side, square_side
            )
            checkpoint = self.store.append_pair(
                direction=direction, source=source, independent=independent
            )
        return checkpoint


def checkpoint_asdict(checkpoint: Checkpoint) -> dict[str, object]:
    """Expose the exact structured checkpoint for tests and later assembly."""

    return asdict(checkpoint)


def _certificate(
    atoms: tuple[Atom, ...],
    directions: tuple[Direction, ...],
    rows: tuple[DirectionManifest, ...],
) -> CertificateManifest:
    if not rows or len(rows) != len(directions):
        raise CheckpointError("cannot assemble an incomplete certificate")
    return CertificateManifest(
        atom_count=len(atoms),
        atom_hash=canonical_hash(atoms),
        total_weight=sum((atom.weight for atom in atoms), start=Fraction(0)),
        direction_count=len(directions),
        direction_hash=canonical_hash(directions),
        rows=rows,
        global_minimum=min(row.minimum for row in rows),
    )


def _target_record(
    checkpoint: Checkpoint,
    fixture: RetainedFixture,
    atoms: tuple[Atom, ...],
) -> dict[str, object]:
    source = _certificate(
        atoms, fixture.directions, tuple(row.source for row in checkpoint.rows)
    )
    independent = _certificate(
        atoms, fixture.directions, tuple(row.independent for row in checkpoint.rows)
    )
    preconditions, all_preconditions = _preconditions(fixture)
    mutation_guards = _mutation_guards(fixture, atoms)
    agreement = source == independent
    frozen_values = (
        source.atom_count == 168
        and source.direction_count == 181
        and source.total_weight == Fraction(9744, 576)
        and source.global_minimum == Fraction(576, 576)
    )
    all_mutations_rejected = all(mutation_guards.values())
    instrument_valid = all_preconditions and frozen_values and all_mutations_rejected
    decision = (
        "accepted"
        if instrument_valid and agreement
        else "rejected"
        if instrument_valid
        else "unresolved-invalid-instrument"
    )
    return {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "hypothesis_id": HYPOTHESIS_ID,
        "fixture": {
            "retained_sha256": RETAINED_SHA256,
            "clean_room_sha256": CLEAN_ROOM_SHA256,
            "grid_size": fixture.grid_size,
            "weight_scale": fixture.weight_scale,
            "outer_side": fixture.outer_side,
            "square_side": fixture.square_side,
            "shrink_margin": fixture.shrink_margin,
            "angle_limit": fixture.angle_limit,
            "direction_steps": fixture.direction_steps,
        },
        "checkpoint_sha256": _sha256(Path(CHECKPOINT_PATH)),
        "source_faithful": asdict(source),
        "independent": asdict(independent),
        "preconditions": preconditions,
        "exact_manifest_agreement": agreement,
        "first_disagreement": _first_disagreement(source, independent),
        "frozen_invariants_pass": frozen_values,
        "mutation_guards": mutation_guards,
        "all_mutations_rejected": all_mutations_rejected,
        "instrument_valid": instrument_valid,
        "decision": decision,
    }


def _production_paths(record: Path, checkpoint: Path, progress: Path) -> None:
    if (str(record), str(checkpoint), str(progress)) != (
        RESULT_PATH,
        CHECKPOINT_PATH,
        PROGRESS_PATH,
    ):
        raise CheckpointError("command paths do not match exp-052 preregistration")


def _run_target(record: Path, checkpoint: Path, progress: Path) -> None:
    _production_paths(record, checkpoint, progress)
    if record.exists():
        raise CheckpointError("result path already exists")
    verify_frozen_inputs()
    fixture = load_retained_fixture()
    atoms = _normalized_atoms(fixture)
    binding = RunBinding(
        schema_version=SCHEMA_VERSION,
        experiment_id=EXPERIMENT_ID,
        hypothesis_id=HYPOTHESIS_ID,
        session_id=SESSION_ID,
        package_manifest_sha256=FROZEN_PACKAGE_SHA256,
        source_sha256=FROZEN_SOURCE_SHA256,
        fixture_hash=fixture_binding_hash(
            atoms=atoms,
            directions=fixture.directions,
            outer_side=fixture.outer_side,
            square_side=fixture.square_side,
        ),
        direction_count=len(fixture.directions),
        direction_hash=canonical_hash(fixture.directions),
        driver_sha256=driver_sha256(),
        result_path=str(record),
        checkpoint_path=str(checkpoint),
        progress_path=str(progress),
    )
    store = CheckpointStore(
        binding=binding,
        directions=fixture.directions,
        result_path=record,
        checkpoint_path=checkpoint,
        progress_path=progress,
        production=True,
    )
    completed = DirectionSlicedDriver(store).run(
        atoms=atoms,
        outer_side=fixture.outer_side,
        square_side=fixture.square_side,
    )
    store.read_progress(completed)
    if progress.exists():
        raise CheckpointError("progress marker survived final checkpoint reconciliation")
    store.refuse_existing_result()
    result = _target_record(completed, fixture, atoms)
    _atomic_write(record, canonical_json(result) + "\n")


def _require(condition: bool, guard: str) -> None:  # noqa: FBT001
    if not condition:
        raise CheckpointError(f"selftest guard failed: {guard}")


def _expect_checkpoint_error(action: Callable[[], object], guard: str) -> None:
    try:
        action()
    except CheckpointError:
        return
    raise CheckpointError(f"selftest guard failed: {guard}")


def _synthetic() -> tuple[tuple[Atom, ...], tuple[Direction, ...], Fraction, Fraction]:
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
    )
    return atoms, directions, Fraction(2), Fraction(1)


def _synthetic_store(
    root: Path,
    *,
    progress_remover: Callable[[Path], None] = _durable_unlink,
) -> tuple[CheckpointStore, tuple[Atom, ...], Fraction, Fraction]:
    atoms, directions, outer_side, square_side = _synthetic()
    result = root / "round.json"
    checkpoint = root / "round.checkpoint.json"
    progress = root / "round.progress.json"
    binding = RunBinding(
        schema_version=SCHEMA_VERSION,
        experiment_id=EXPERIMENT_ID,
        hypothesis_id=HYPOTHESIS_ID,
        session_id=SESSION_ID,
        package_manifest_sha256=FROZEN_PACKAGE_SHA256,
        source_sha256=FROZEN_SOURCE_SHA256,
        fixture_hash=fixture_binding_hash(
            atoms=atoms,
            directions=directions,
            outer_side=outer_side,
            square_side=square_side,
        ),
        direction_count=len(directions),
        direction_hash=canonical_hash(directions),
        driver_sha256=driver_sha256(),
        result_path=str(result),
        checkpoint_path=str(checkpoint),
        progress_path=str(progress),
    )
    return (
        CheckpointStore(
            binding=binding,
            directions=directions,
            result_path=result,
            checkpoint_path=checkpoint,
            progress_path=progress,
            progress_remover=progress_remover,
        ),
        atoms,
        outer_side,
        square_side,
    )


def run_selftest() -> dict[str, object]:
    """Exercise target-blind readiness with explicit guards that survive ``-O``."""

    verify_frozen_inputs()
    with tempfile.TemporaryDirectory(prefix="n17-resume-selftest-") as name:
        root = Path(name)
        store, atoms, outer_side, square_side = _synthetic_store(root)
        completed = DirectionSlicedDriver(store).run(
            atoms=atoms, outer_side=outer_side, square_side=square_side
        )
        _require(len(completed.rows) == 2, "complete-paired-prefix")
        _require(all(row.agreement for row in completed.rows), "synthetic-agreement")
        _require(store.read_progress(completed) is None, "no-final-progress")

        source = _certificate(
            atoms, store.directions, tuple(row.source for row in completed.rows)
        )
        independent = _certificate(
            atoms, store.directions, tuple(row.independent for row in completed.rows)
        )
        _require(source == independent, "final-before-assembly-equivalence")

        interrupted_store, interrupted_atoms, interrupted_outer, interrupted_square = (
            _synthetic_store(root / "between")
        )

        def interrupt_independent(*_args: object) -> DirectionManifest:
            raise RuntimeError("synthetic between-accumulator interruption")

        try:
            DirectionSlicedDriver(
                interrupted_store,
                independent_accumulator=interrupt_independent,
            ).run(
                atoms=interrupted_atoms,
                outer_side=interrupted_outer,
                square_side=interrupted_square,
            )
        except RuntimeError:
            pass
        else:
            raise CheckpointError("selftest guard failed: between-accumulator-interruption")
        _require(
            interrupted_store.load().rows == (),
            "between-accumulator-no-partial-row",
        )
        resumed = DirectionSlicedDriver(interrupted_store).run(
            atoms=interrupted_atoms,
            outer_side=interrupted_outer,
            square_side=interrupted_square,
        )
        _require(len(resumed.rows) == 2, "between-accumulator-resume")

        after_pair_store, after_pair_atoms, after_pair_outer, after_pair_square = (
            _synthetic_store(root / "after-pair")
        )
        calls = 0

        def interrupt_second_source(
            call_atoms: tuple[Atom, ...],
            direction: Direction,
            call_outer: Fraction,
            call_square: Fraction,
        ) -> DirectionManifest:
            nonlocal calls
            calls += 1
            if calls == 2:
                raise RuntimeError("synthetic after-pair interruption")
            return accumulate_source_faithful(
                call_atoms, direction, call_outer, call_square
            )

        try:
            DirectionSlicedDriver(
                after_pair_store, source_accumulator=interrupt_second_source
            ).run(
                atoms=after_pair_atoms,
                outer_side=after_pair_outer,
                square_side=after_pair_square,
            )
        except RuntimeError:
            pass
        else:
            raise CheckpointError("selftest guard failed: after-pair-interruption")
        _require(len(after_pair_store.load().rows) == 1, "after-pair-prefix-retained")
        _require(
            len(
                DirectionSlicedDriver(after_pair_store).run(
                    atoms=after_pair_atoms,
                    outer_side=after_pair_outer,
                    square_side=after_pair_square,
                ).rows
            )
            == 2,
            "after-pair-resume",
        )

        removals = 0

        def crash_before_final_unlink(path: Path) -> None:
            nonlocal removals
            removals += 1
            if removals == 2:
                raise RuntimeError("synthetic post-checkpoint pre-unlink crash")
            _durable_unlink(path)

        crash_store, crash_atoms, crash_outer, crash_square = _synthetic_store(
            root / "final-pair-crash",
            progress_remover=crash_before_final_unlink,
        )
        try:
            DirectionSlicedDriver(crash_store).run(
                atoms=crash_atoms,
                outer_side=crash_outer,
                square_side=crash_square,
            )
        except RuntimeError:
            pass
        else:
            raise CheckpointError("selftest guard failed: final-pair-crash-injection")
        _require(len(crash_store.load().rows) == 2, "final-checkpoint-survives-crash")
        _require(crash_store.progress_path.exists(), "stale-progress-survives-crash")
        resumed_store, _, _, _ = _synthetic_store(root / "final-pair-crash")
        reconciled = DirectionSlicedDriver(resumed_store).run(
            atoms=crash_atoms,
            outer_side=crash_outer,
            square_side=crash_square,
        )
        _require(len(reconciled.rows) == 2, "full-checkpoint-resume")
        _require(
            not resumed_store.progress_path.exists(),
            "stale-progress-removed-before-publication",
        )
        _atomic_write(resumed_store.result_path, '{"synthetic":true}\n')
        _require(
            resumed_store.result_path.exists() and not resumed_store.progress_path.exists(),
            "result-progress-noncoexistence",
        )

        before_store, before_atoms, before_outer, before_square = _synthetic_store(
            root / "before-row-zero"
        )

        def interrupt_first_source(*_args: object) -> DirectionManifest:
            raise RuntimeError("synthetic before-row-zero interruption")

        try:
            DirectionSlicedDriver(
                before_store, source_accumulator=interrupt_first_source
            ).run(
                atoms=before_atoms,
                outer_side=before_outer,
                square_side=before_square,
            )
        except RuntimeError:
            pass
        else:
            raise CheckpointError("selftest guard failed: before-row-zero-interruption")
        _require(before_store.load().rows == (), "before-row-zero-empty-prefix")

        _expect_checkpoint_error(
            lambda: DirectionSlicedDriver(store).run(
                atoms=atoms[1:], outer_side=outer_side, square_side=square_side
            ),
            "changed-fixture-rejection",
        )

        stale = ProgressMarker(
            SCHEMA_VERSION,
            binding_hash(store.binding),
            0,
            "source_started",
            binding_hash(store.binding),
        )
        _atomic_write(store.progress_path, canonical_json(stale) + "\n")
        _require(store.read_progress(completed) is None, "stale-progress-checkpoint-wins")

        future = ProgressMarker(
            SCHEMA_VERSION,
            binding_hash(store.binding),
            3,
            "source_started",
            completed.rows[-1].row_hash,
        )
        _atomic_write(store.progress_path, canonical_json(future) + "\n")
        _expect_checkpoint_error(
            lambda: store.read_progress(completed), "future-progress-rejection"
        )
        store.progress_path.write_text("{}\n", encoding="utf-8")
        _expect_checkpoint_error(
            lambda: store.read_progress(completed), "malformed-progress-rejection"
        )

        store.progress_path.unlink()
        baseline = json.loads(store.checkpoint_path.read_text(encoding="utf-8"))

        def corrupt(name: str, mutate: Callable[[dict[str, Any]], None]) -> None:
            candidate = json.loads(canonical_json(baseline))
            mutate(candidate)
            store.checkpoint_path.write_text(
                canonical_json(candidate) + "\n", encoding="utf-8"
            )
            _expect_checkpoint_error(store.load, name)

        corrupt("gap-rejection", lambda value: value["rows"][1].__setitem__("ordinal", 2))
        corrupt(
            "duplicate-rejection",
            lambda value: value["rows"].__setitem__(1, value["rows"][0]),
        )
        corrupt("reorder-rejection", lambda value: value["rows"].reverse())
        corrupt(
            "chain-rejection",
            lambda value: value["rows"][1].__setitem__("previous_row_hash", "0" * 64),
        )
        corrupt(
            "payload-rejection",
            lambda value: value["rows"][0]["source"].__setitem__("minimum", "999/1"),
        )
        corrupt(
            "event-hash-rejection",
            lambda value: value["rows"][0]["source"].__setitem__("x_event_hash", "0" * 64),
        )
        corrupt(
            "manifest-label-rejection",
            lambda value: value["rows"][0]["source"].__setitem__("label", "wrong"),
        )
        corrupt(
            "malformed-rational-rejection",
            lambda value: value["rows"][0]["source"]["x_events"].__setitem__(0, "0.5"),
        )
        store.checkpoint_path.write_text('{"binding":', encoding="utf-8")
        _expect_checkpoint_error(store.load, "truncation-rejection")
        store.checkpoint_path.write_text(canonical_json(baseline) + "\n", encoding="utf-8")

        wrong_binding = replace(store.binding, result_path="wrong.json")
        _expect_checkpoint_error(
            lambda: CheckpointStore(
                binding=wrong_binding,
                directions=store.directions,
                result_path=store.result_path,
                checkpoint_path=store.checkpoint_path,
                progress_path=store.progress_path,
            ),
            "path-binding-rejection",
        )
        _production_paths(Path(RESULT_PATH), Path(CHECKPOINT_PATH), Path(PROGRESS_PATH))
        _expect_checkpoint_error(
            lambda: _production_paths(
                Path("wrong.json"), Path(CHECKPOINT_PATH), Path(PROGRESS_PATH)
            ),
            "production-path-rejection",
        )

        empty_store, _, _, _ = _synthetic_store(root / "existing-empty")
        empty_store.result_path.parent.mkdir(parents=True, exist_ok=True)
        empty_store.result_path.write_text("occupied\n", encoding="utf-8")
        _expect_checkpoint_error(
            empty_store.initialize, "existing-result-without-checkpoint-rejection"
        )
        store.result_path.write_text("occupied\n", encoding="utf-8")
        _expect_checkpoint_error(
            store.initialize, "existing-result-with-checkpoint-rejection"
        )

    receipts = {
        "after-pair-resume": True,
        "before-row-zero-interruption": True,
        "between-accumulator-resume": True,
        "canonical-progress": True,
        "changed-fixture-rejection": True,
        "chain-rejection": True,
        "complete-paired-prefix": True,
        "duplicate-rejection": True,
        "event-hash-rejection": True,
        "existing-result-with-checkpoint-rejection": True,
        "existing-result-without-checkpoint-rejection": True,
        "final-before-assembly-equivalence": True,
        "final-pair-crash-reconciled-before-result": True,
        "frozen-inputs": True,
        "future-progress-rejection": True,
        "gap-rejection": True,
        "malformed-progress-rejection": True,
        "malformed-rational-rejection": True,
        "manifest-label-rejection": True,
        "no-partial-row-promotion": True,
        "path-binding-rejection": True,
        "payload-rejection": True,
        "production-path-binding": True,
        "reorder-rejection": True,
        "stale-progress-checkpoint-wins": True,
        "synthetic-agreement": True,
        "truncation-rejection": True,
    }
    return {
        "schema_version": 1,
        "selftest": "exp-052-w7-readiness",
        "passed": True,
        "driver_sha256": driver_sha256(),
        "frozen_package_sha256": FROZEN_PACKAGE_SHA256,
        "receipts": receipts,
        "receipt_hash": canonical_hash(receipts),
    }


def selftest_json() -> str:
    return canonical_json(run_selftest())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--record", type=Path)
    action.add_argument("--selftest", action="store_true")
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--progress", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.selftest:
        if args.checkpoint is not None or args.progress is not None:
            raise CheckpointError("selftest does not accept output paths")
        print(selftest_json())
        return 0
    if args.record is None or args.checkpoint is None or args.progress is None:
        raise CheckpointError("--record, --checkpoint and --progress are required")
    _run_target(args.record, args.checkpoint, args.progress)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
