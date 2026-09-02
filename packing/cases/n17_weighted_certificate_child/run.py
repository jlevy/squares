"""Parent-bound child chain continuing the reviewed exp-052 prefix from ordinal 33.

This module adds no arithmetic.  It verifies the frozen exp-052 boundary, carries the
reviewed 33 parent rows verbatim into a fresh exp-056 checkpoint, and then continues the
same hash chain by calling the unchanged exp-052 accumulators through the unchanged
exp-052 checkpoint machinery.  No exp-052 path and no file under the resume package is
writable from here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from collections.abc import Callable
from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path
from typing import Any

from cases.n17_weighted_certificate.fixture import RETAINED_SHA256, load_retained_fixture
from cases.n17_weighted_certificate.model import (
    Atom,
    Direction,
    DirectionManifest,
    canonical_hash,
    canonical_json,
)
from cases.n17_weighted_certificate_resume.run import (
    FROZEN_PACKAGE_SHA256,
    FROZEN_SOURCE_SHA256,
    SCHEMA_VERSION,
    Accumulator,
    CheckpointError,
    CheckpointStore,
    DirectionSlicedDriver,
    PairedRow,
    ProgressMarker,
    ProgressStage,
    RunBinding,
    _atomic_write,  # pyright: ignore[reportPrivateUsage]
    _binding,  # pyright: ignore[reportPrivateUsage]
    _durable_unlink,  # pyright: ignore[reportPrivateUsage]
    _normalized_atoms,  # pyright: ignore[reportPrivateUsage]
    _paired_row,  # pyright: ignore[reportPrivateUsage]
    _progress_marker,  # pyright: ignore[reportPrivateUsage]
    _row_hash,  # pyright: ignore[reportPrivateUsage]
    _validate_manifest,  # pyright: ignore[reportPrivateUsage]
    accumulate_source_faithful,
    accumulate_target_independent,
    binding_hash,
    driver_sha256,
    fixture_binding_hash,
    verify_frozen_inputs,
)

PACKING_ROOT = Path(__file__).resolve().parents[2]
CHILD_DRIVER_PATH = Path(__file__)
RESUME_PACKAGE = PACKING_ROOT / "cases/n17_weighted_certificate_resume"
OUTPUT_ROOT = Path("campaign/series/series-000-smoke-and-calibration/results")
SLUG = "exp-056-h-052-n17-sequential-larger-prefix"
EXPERIMENT_ID = "exp-056"
HYPOTHESIS_ID = "H-052"
SESSION_ID = "session-079"
PARENT_EXPERIMENT_ID = "exp-052"
EXPERIMENT_RECORD_PATH = (
    "campaign/series/series-000-smoke-and-calibration/experiments/"
    "exp-056-h-052-n17-sequential-larger-prefix.md"
)
RESULT_PATH = OUTPUT_ROOT / f"{SLUG}.json"
CHECKPOINT_PATH = OUTPUT_ROOT / f"{SLUG}.checkpoint.json"
PROGRESS_PATH = OUTPUT_ROOT / f"{SLUG}.progress.json"
PARENT_CHECKPOINT = OUTPUT_ROOT / (
    "exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json"
)
PARENT_PROGRESS = OUTPUT_ROOT / (
    "exp-052-h-052-n17-resumable-certificate-agreement.progress.json"
)
PARENT_CHECKPOINT_SHA256 = "db5c156959b6de4e6f2c9be283454d01dd5f3a436e6489f5e6bb60c38559fdb8"
PARENT_PROGRESS_SHA256 = "08e301b01c7ac6eef4b03c3a4daa5f72c5f1bdbe217dbbb061b57f5c94d947af"
PARENT_BINDING_HASH = "2446fa39e154800410b9b5cc19f19aed7cc0c797d116f7ece1c97a2c7c0b4d1a"
PARENT_LAST_ROW_HASH = "9badcc57c05e328344b0ec7ae4fbf9815e8eae027a79bec1bf1a35b9871fade6"
PARENT_ROW_COUNT = 33
DIRECTION_COUNT = 181
FORBIDDEN_SLUGS = ("exp-052", "n17_weighted_certificate_resume")


class ChildError(RuntimeError):
    """A binding, path, chain, parent-verification or publication guard failed."""


class DisagreementStopError(RuntimeError):
    """The two unchanged accumulators disagreed exactly; the row is retained."""


@dataclass(frozen=True, slots=True)
class ParentSpec:
    """The frozen parent boundary a child chain descends from."""

    experiment_id: str
    checkpoint_path: Path
    progress_path: Path
    result_path: Path
    checkpoint_sha256: str
    progress_sha256: str
    binding_hash: str
    last_row_hash: str
    row_count: int


@dataclass(frozen=True, slots=True)
class ChildBinding:
    """Immutable provenance for one parent-bound child round."""

    schema_version: int
    experiment_id: str
    hypothesis_id: str
    session_id: str
    experiment_record_path: str
    parent_experiment_id: str
    parent_checkpoint_sha256: str
    parent_progress_sha256: str
    parent_binding_hash: str
    parent_last_row_hash: str
    parent_row_count: int
    package_manifest_sha256: str
    resume_driver_sha256: str
    child_driver_sha256: str
    fixture_hash: str
    direction_count: int
    direction_hash: str
    result_path: str
    checkpoint_path: str
    progress_path: str


@dataclass(frozen=True, slots=True)
class ChildCheckpoint:
    """The carried parent prefix plus every child row, in one contiguous chain."""

    binding: ChildBinding
    rows: tuple[PairedRow, ...]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def child_driver_sha256() -> str:
    """Hash this driver independently of the unchanged resume driver."""

    return _sha256(CHILD_DRIVER_PATH)


def child_binding_hash(binding: ChildBinding) -> str:
    """Return the provenance digest of a child binding block."""

    return canonical_hash({"domain": "n17-child-binding-v1", "binding": binding})


def _checkpoint_json(checkpoint: ChildCheckpoint) -> str:
    return canonical_json({"binding": checkpoint.binding, "rows": checkpoint.rows}) + "\n"


def _exact_object(value: object, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != fields:
        raise ChildError(f"malformed {label}")
    return value


def _refuse_removal(path: Path) -> None:
    raise ChildError(f"refusing to remove a parent artifact: {path}")


def _write_exclusive(path: Path, content: str) -> None:
    """Publish complete bytes atomically and never replace an existing artifact."""

    if path.exists():
        raise ChildError(f"refusing to overwrite an existing artifact: {path}")
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
        try:
            os.link(temporary, path)
        except FileExistsError as error:
            raise ChildError(f"refusing to overwrite an existing artifact: {path}") from error
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        temporary.unlink(missing_ok=True)


def require_writable(path: Path, output_root: Path, label: str) -> Path:
    """Refuse every output path outside the bound root, lexically or after resolution."""

    text = path.as_posix()
    for forbidden in FORBIDDEN_SLUGS:
        if forbidden in text:
            raise ChildError(f"{label} names a frozen parent artifact: {path}")
    if ".." in path.parts:
        raise ChildError(f"{label} escapes its bound root lexically: {path}")
    if path.is_symlink() or path.parent.is_symlink():
        raise ChildError(f"{label} is a symbolic link: {path}")
    root = output_root.resolve(strict=False)
    resolved = path.resolve(strict=False)
    if not resolved.is_relative_to(root):
        raise ChildError(f"{label} escapes its bound root: {path}")
    if resolved.is_relative_to(RESUME_PACKAGE.resolve(strict=False)):
        raise ChildError(f"{label} would write inside the resume package: {path}")
    return resolved


def verify_parent(
    spec: ParentSpec, directions: tuple[Direction, ...]
) -> tuple[RunBinding, tuple[PairedRow, ...]]:
    """Replay the frozen parent boundary through the unchanged exp-052 validator."""

    for path, expected, label in (
        (spec.checkpoint_path, spec.checkpoint_sha256, "parent checkpoint"),
        (spec.progress_path, spec.progress_sha256, "parent progress marker"),
    ):
        if not path.is_file():
            raise ChildError(f"{label} is absent: {path}")
        actual = _sha256(path)
        if actual != expected:
            raise ChildError(f"{label} digest changed: expected {expected}, got {actual}")
    try:
        raw = json.loads(spec.checkpoint_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ChildError("parent checkpoint is unreadable") from error
    parsed = _exact_object(raw, {"binding", "rows"}, "parent checkpoint")
    try:
        parent_binding = _binding(parsed["binding"])
    except CheckpointError as error:
        raise ChildError(f"parent binding is malformed: {error}") from error
    if parent_binding.experiment_id != spec.experiment_id:
        raise ChildError("parent binding names a different experiment")
    if binding_hash(parent_binding) != spec.binding_hash:
        raise ChildError("parent binding hash changed")
    store = CheckpointStore(
        binding=parent_binding,
        directions=directions,
        result_path=spec.result_path,
        checkpoint_path=spec.checkpoint_path,
        progress_path=spec.progress_path,
        progress_remover=_refuse_removal,
    )
    try:
        checkpoint = store.load()
        marker = store.read_progress(checkpoint)
    except CheckpointError as error:
        raise ChildError(
            f"parent checkpoint failed the unchanged validator: {error}"
        ) from error
    if len(checkpoint.rows) != spec.row_count:
        raise ChildError("parent prefix is not the reviewed row count")
    if not all(row.agreement for row in checkpoint.rows):
        raise ChildError("parent prefix contains a disagreement")
    if checkpoint.rows[-1].row_hash != spec.last_row_hash:
        raise ChildError("parent last row hash changed")
    if marker is None or marker.ordinal != spec.row_count:
        raise ChildError("parent progress marker does not sit at the resume ordinal")
    if marker.previous_row_hash != spec.last_row_hash:
        raise ChildError("parent progress marker is not chained to the last parent row")
    return parent_binding, checkpoint.rows


class ChildCheckpointStore:
    """Persist and validate one parent-bound child chain under a bound output root."""

    def __init__(
        self,
        *,
        binding: ChildBinding,
        directions: tuple[Direction, ...],
        parent_rows: tuple[PairedRow, ...],
        output_root: Path,
        result_path: Path,
        checkpoint_path: Path,
        progress_path: Path,
        production: bool = False,
        progress_remover: Callable[[Path], None] = _durable_unlink,
    ) -> None:
        self.binding = binding
        self.directions = directions
        self.parent_rows = parent_rows
        self.output_root = output_root
        self.result_path = result_path
        self.checkpoint_path = checkpoint_path
        self.progress_path = progress_path
        self.production = production
        self.progress_remover = progress_remover
        self._validate_binding()

    def _validate_binding(self) -> None:
        if self.binding.schema_version != SCHEMA_VERSION:
            raise ChildError("unsupported child checkpoint schema version")
        if self.binding.experiment_id != EXPERIMENT_ID:
            raise ChildError("child checkpoint is not bound to exp-056")
        if self.binding.hypothesis_id != HYPOTHESIS_ID:
            raise ChildError("child checkpoint is not bound to H-052")
        if self.binding.session_id != SESSION_ID:
            raise ChildError("child checkpoint is not bound to session-079")
        if self.binding.parent_experiment_id != PARENT_EXPERIMENT_ID:
            raise ChildError("child checkpoint is not bound to the exp-052 parent")
        if self.binding.experiment_record_path != EXPERIMENT_RECORD_PATH:
            raise ChildError("child checkpoint does not name the exp-056 record")
        if self.binding.package_manifest_sha256 != FROZEN_PACKAGE_SHA256:
            raise ChildError("child binding does not name the frozen package")
        if self.binding.resume_driver_sha256 != driver_sha256():
            raise ChildError("unchanged resume driver hash mismatch")
        if self.binding.child_driver_sha256 != child_driver_sha256():
            raise ChildError("child driver hash mismatch")
        if self.binding.direction_count != len(self.directions):
            raise ChildError("child binding direction count mismatch")
        if self.binding.direction_hash != canonical_hash(self.directions):
            raise ChildError("child binding direction hash mismatch")
        if self.binding.parent_row_count != len(self.parent_rows):
            raise ChildError("child binding parent row count mismatch")
        if not self.parent_rows:
            raise ChildError("a child chain needs a nonempty parent prefix")
        if self.binding.parent_last_row_hash != self.parent_rows[-1].row_hash:
            raise ChildError("child binding parent row hash mismatch")
        for path, declared, label in (
            (self.result_path, self.binding.result_path, "result path"),
            (self.checkpoint_path, self.binding.checkpoint_path, "checkpoint path"),
            (self.progress_path, self.binding.progress_path, "progress path"),
        ):
            if declared != str(path):
                raise ChildError(f"child binding {label} mismatch")
            require_writable(path, self.output_root, label)
        if self.production and (
            (self.result_path, self.checkpoint_path, self.progress_path)
            != (RESULT_PATH, CHECKPOINT_PATH, PROGRESS_PATH)
            or self.output_root != OUTPUT_ROOT
        ):
            raise ChildError("production paths do not match exp-056 preregistration")

    def refuse_existing_result(self) -> None:
        if self.result_path.exists():
            raise ChildError("result path already exists")

    def _validate_rows(self, rows: tuple[PairedRow, ...]) -> None:
        if len(rows) < len(self.parent_rows):
            raise ChildError("child checkpoint dropped a carried parent row")
        if len(rows) > len(self.directions):
            raise ChildError("child checkpoint contains too many rows")
        if rows[: len(self.parent_rows)] != self.parent_rows:
            raise ChildError("carried parent rows changed")
        previous = self.binding.parent_binding_hash
        for ordinal, row in enumerate(rows):
            if row.ordinal != ordinal:
                raise ChildError("child ordinals are not contiguous")
            if row.direction != self.directions[ordinal]:
                raise ChildError("child direction order changed")
            _validate_manifest(row.source, row.direction, "source")
            _validate_manifest(row.independent, row.direction, "independent")
            if row.previous_row_hash != previous:
                raise ChildError("child hash chain changed")
            if row.agreement != (row.source == row.independent):
                raise ChildError("child agreement flag changed")
            expected = _row_hash(
                ordinal=row.ordinal,
                direction=row.direction,
                source=row.source,
                independent=row.independent,
                agreement=row.agreement,
                previous_row_hash=row.previous_row_hash,
            )
            if row.row_hash != expected:
                raise ChildError("child row hash changed")
            previous = row.row_hash

    def open_chain(self) -> ChildCheckpoint:
        """Carry the parent prefix into a fresh chain, or resume a verified one."""

        self.refuse_existing_result()
        if self.checkpoint_path.exists():
            checkpoint = self.load()
            self.read_progress(checkpoint)
            return checkpoint
        if self.progress_path.exists():
            raise ChildError("progress marker exists without a child checkpoint")
        checkpoint = ChildCheckpoint(self.binding, self.parent_rows)
        self._validate_rows(checkpoint.rows)
        _atomic_write(self.checkpoint_path, _checkpoint_json(checkpoint))
        return checkpoint

    def load(self) -> ChildCheckpoint:
        self.refuse_existing_result()
        try:
            text = self.checkpoint_path.read_text(encoding="utf-8")
            value = json.loads(text)
        except (OSError, json.JSONDecodeError) as error:
            raise ChildError("child checkpoint is unreadable") from error
        raw = _exact_object(value, {"binding", "rows"}, "child checkpoint")
        parsed_binding = _child_binding(raw["binding"])
        if parsed_binding != self.binding:
            raise ChildError("child checkpoint binding changed")
        raw_rows = raw["rows"]
        if not isinstance(raw_rows, list):
            raise ChildError("malformed child checkpoint rows")
        try:
            rows = tuple(_paired_row(row) for row in raw_rows)
        except CheckpointError as error:
            raise ChildError(f"malformed child row: {error}") from error
        self._validate_rows(rows)
        checkpoint = ChildCheckpoint(parsed_binding, rows)
        if text != _checkpoint_json(checkpoint):
            raise ChildError("child checkpoint serialization is not canonical")
        return checkpoint

    def read_progress(self, checkpoint: ChildCheckpoint) -> ProgressMarker | None:
        """Validate the child progress marker; a stale marker never wins."""

        if not self.progress_path.exists():
            return None
        try:
            text = self.progress_path.read_text(encoding="utf-8")
            marker = _progress_marker(json.loads(text))
        except (OSError, json.JSONDecodeError, CheckpointError) as error:
            raise ChildError("child progress marker is unreadable") from error
        if text != canonical_json(marker) + "\n":
            raise ChildError("child progress marker serialization is not canonical")
        if marker.schema_version != SCHEMA_VERSION:
            raise ChildError("child progress marker schema changed")
        if marker.binding_hash != child_binding_hash(self.binding):
            raise ChildError("child progress marker binding changed")
        if marker.ordinal > len(checkpoint.rows):
            raise ChildError("child progress marker is ahead of the checkpoint")
        if marker.ordinal < len(self.parent_rows):
            raise ChildError("child progress marker is inside the parent prefix")
        expected = checkpoint.rows[marker.ordinal - 1].row_hash
        if marker.previous_row_hash != expected:
            raise ChildError("child progress marker chain changed")
        if marker.ordinal < len(checkpoint.rows):
            self.progress_remover(self.progress_path)
            return None
        if marker.ordinal >= len(self.directions):
            raise ChildError("child progress marker is beyond the final direction")
        return marker

    def write_progress(self, ordinal: int, stage: ProgressStage) -> ProgressMarker:
        checkpoint = self.load()
        if ordinal != len(checkpoint.rows) or ordinal >= len(self.directions):
            raise ChildError("progress ordinal is not the first incomplete direction")
        marker = ProgressMarker(
            schema_version=SCHEMA_VERSION,
            binding_hash=child_binding_hash(self.binding),
            ordinal=ordinal,
            stage=stage,
            previous_row_hash=checkpoint.rows[-1].row_hash,
        )
        _atomic_write(self.progress_path, canonical_json(marker) + "\n")
        return marker

    def append_pair(
        self,
        *,
        direction: Direction,
        source: DirectionManifest,
        independent: DirectionManifest,
    ) -> ChildCheckpoint:
        checkpoint = self.load()
        ordinal = len(checkpoint.rows)
        if ordinal >= len(self.directions) or direction != self.directions[ordinal]:
            raise ChildError("paired row is not the first incomplete direction")
        _validate_manifest(source, direction, "source")
        _validate_manifest(independent, direction, "independent")
        previous = checkpoint.rows[-1].row_hash
        agreement = source == independent
        row = PairedRow(
            ordinal=ordinal,
            direction=direction,
            source=source,
            independent=independent,
            agreement=agreement,
            previous_row_hash=previous,
            row_hash=_row_hash(
                ordinal=ordinal,
                direction=direction,
                source=source,
                independent=independent,
                agreement=agreement,
                previous_row_hash=previous,
            ),
        )
        updated = ChildCheckpoint(self.binding, (*checkpoint.rows, row))
        _atomic_write(self.checkpoint_path, _checkpoint_json(updated))
        self.progress_remover(self.progress_path)
        return updated


def _child_binding(value: object) -> ChildBinding:
    fields = {field.name for field in ChildBinding.__dataclass_fields__.values()}
    raw = _exact_object(value, fields, "child binding")
    parsed: dict[str, Any] = {}
    for name in fields:
        item = raw[name]
        if name in {"schema_version", "parent_row_count", "direction_count"}:
            if isinstance(item, bool) or not isinstance(item, int) or item < 0:
                raise ChildError(f"malformed child binding {name}")
        elif not isinstance(item, str) or not item:
            raise ChildError(f"malformed child binding {name}")
        parsed[name] = item
    return ChildBinding(**parsed)


class ChildChainDriver:
    """Continue the parent chain one direction at a time, committing complete pairs."""

    def __init__(
        self,
        store: ChildCheckpointStore,
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
    ) -> ChildCheckpoint:
        actual = fixture_binding_hash(
            atoms=atoms,
            directions=self.store.directions,
            outer_side=outer_side,
            square_side=square_side,
        )
        if actual != self.store.binding.fixture_hash:
            raise ChildError("fixture binding changed")
        checkpoint = self.store.open_chain()
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
            if not checkpoint.rows[-1].agreement:
                raise DisagreementStopError(f"exact disagreement retained at ordinal {ordinal}")
        return checkpoint


def chain_status(checkpoint_path: Path) -> dict[str, object]:
    """Report the observable chain state without loading the retained fixture."""

    try:
        text = checkpoint_path.read_text(encoding="utf-8")
        value = json.loads(text)
    except (OSError, json.JSONDecodeError) as error:
        raise ChildError("child checkpoint is unreadable") from error
    raw = _exact_object(value, {"binding", "rows"}, "child checkpoint")
    binding = _child_binding(raw["binding"])
    raw_rows = raw["rows"]
    if not isinstance(raw_rows, list) or not raw_rows:
        raise ChildError("child checkpoint has no rows")
    try:
        rows = tuple(_paired_row(row) for row in raw_rows)
    except CheckpointError as error:
        raise ChildError(f"malformed child row: {error}") from error
    previous = binding.parent_binding_hash
    first_disagreement: int | None = None
    for ordinal, row in enumerate(rows):
        if row.ordinal != ordinal or row.previous_row_hash != previous:
            raise ChildError("child chain is not contiguous")
        if row.agreement != (row.source == row.independent):
            raise ChildError("child agreement flag changed")
        if row.row_hash != _row_hash(
            ordinal=row.ordinal,
            direction=row.direction,
            source=row.source,
            independent=row.independent,
            agreement=row.agreement,
            previous_row_hash=row.previous_row_hash,
        ):
            raise ChildError("child row hash changed")
        if not row.agreement and first_disagreement is None:
            first_disagreement = ordinal
        previous = row.row_hash
    progress_path = Path(binding.progress_path)
    progress: dict[str, object] | None = None
    if progress_path.is_file():
        try:
            marker = _progress_marker(json.loads(progress_path.read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError, CheckpointError) as error:
            raise ChildError("child progress marker is unreadable") from error
        progress = {"ordinal": marker.ordinal, "stage": marker.stage}
    return {
        "schema_version": 1,
        "status": "exp-056-child-chain",
        "checkpoint_path": checkpoint_path.as_posix(),
        "checkpoint_sha256": _sha256(checkpoint_path),
        "chain_verified": True,
        "parent_row_count": binding.parent_row_count,
        "row_count": len(rows),
        "child_row_count": len(rows) - binding.parent_row_count,
        "last_ordinal": rows[-1].ordinal,
        "last_row_hash": rows[-1].row_hash,
        "direction_count": binding.direction_count,
        "complete": len(rows) == binding.direction_count,
        "all_agree": first_disagreement is None,
        "first_disagreement_ordinal": first_disagreement,
        "progress": progress,
    }


def child_result(checkpoint: ChildCheckpoint, *, retained_sha256: str) -> dict[str, object]:
    """Assemble the immutable exp-056 result from a complete verified child chain."""

    rows = checkpoint.rows
    if len(rows) != checkpoint.binding.direction_count:
        raise ChildError("cannot assemble an incomplete child chain")
    disagreements = tuple(row.ordinal for row in rows if not row.agreement)
    return {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "hypothesis_id": HYPOTHESIS_ID,
        "session_id": SESSION_ID,
        "retained_sha256": retained_sha256,
        "binding": checkpoint.binding,
        "binding_hash": child_binding_hash(checkpoint.binding),
        "rows": rows,
        "row_count": len(rows),
        "agreement": {
            "all_agree": not disagreements,
            "agreeing_rows": sum(1 for row in rows if row.agreement),
            "disagreeing_ordinals": disagreements,
            "first_disagreement_ordinal": disagreements[0] if disagreements else None,
            "contiguous_agreeing_prefix": next(
                (row.ordinal for row in rows if not row.agreement), len(rows)
            ),
        },
        "last_row_hash": rows[-1].row_hash,
        "claim_boundary": (
            "A larger contiguous agreeing prefix or all 181 pairs; agreement alone moves "
            "no bound; the first exact disagreement is a retained result."
        ),
    }


def production_binding(
    *,
    directions: tuple[Direction, ...],
    atoms: tuple[Atom, ...],
    outer_side: Fraction,
    square_side: Fraction,
) -> ChildBinding:
    """Build the exp-056 binding block from the frozen parent and fixture identities."""

    return ChildBinding(
        schema_version=SCHEMA_VERSION,
        experiment_id=EXPERIMENT_ID,
        hypothesis_id=HYPOTHESIS_ID,
        session_id=SESSION_ID,
        experiment_record_path=EXPERIMENT_RECORD_PATH,
        parent_experiment_id=PARENT_EXPERIMENT_ID,
        parent_checkpoint_sha256=PARENT_CHECKPOINT_SHA256,
        parent_progress_sha256=PARENT_PROGRESS_SHA256,
        parent_binding_hash=PARENT_BINDING_HASH,
        parent_last_row_hash=PARENT_LAST_ROW_HASH,
        parent_row_count=PARENT_ROW_COUNT,
        package_manifest_sha256=FROZEN_PACKAGE_SHA256,
        resume_driver_sha256=driver_sha256(),
        child_driver_sha256=child_driver_sha256(),
        fixture_hash=fixture_binding_hash(
            atoms=atoms,
            directions=directions,
            outer_side=outer_side,
            square_side=square_side,
        ),
        direction_count=len(directions),
        direction_hash=canonical_hash(directions),
        result_path=str(RESULT_PATH),
        checkpoint_path=str(CHECKPOINT_PATH),
        progress_path=str(PROGRESS_PATH),
    )


def _production_paths(record: Path, checkpoint: Path, progress: Path) -> None:
    if (record, checkpoint, progress) != (RESULT_PATH, CHECKPOINT_PATH, PROGRESS_PATH):
        raise ChildError("command paths do not match exp-056 preregistration")


def run_target(record: Path, checkpoint: Path, progress: Path) -> dict[str, object]:
    """Verify the parent, continue the chain to ordinal 180, and publish once."""

    _production_paths(record, checkpoint, progress)
    if record.exists():
        raise ChildError("result path already exists")
    verify_frozen_inputs()
    fixture = load_retained_fixture()
    atoms = _normalized_atoms(fixture)
    if len(fixture.directions) != DIRECTION_COUNT:
        raise ChildError("retained direction count changed")
    spec = ParentSpec(
        experiment_id=PARENT_EXPERIMENT_ID,
        checkpoint_path=PARENT_CHECKPOINT,
        progress_path=PARENT_PROGRESS,
        result_path=OUTPUT_ROOT / "exp-052-h-052-n17-resumable-certificate-agreement.json",
        checkpoint_sha256=PARENT_CHECKPOINT_SHA256,
        progress_sha256=PARENT_PROGRESS_SHA256,
        binding_hash=PARENT_BINDING_HASH,
        last_row_hash=PARENT_LAST_ROW_HASH,
        row_count=PARENT_ROW_COUNT,
    )
    _, parent_rows = verify_parent(spec, fixture.directions)
    binding = production_binding(
        directions=fixture.directions,
        atoms=atoms,
        outer_side=fixture.outer_side,
        square_side=fixture.square_side,
    )
    store = ChildCheckpointStore(
        binding=binding,
        directions=fixture.directions,
        parent_rows=parent_rows,
        output_root=OUTPUT_ROOT,
        result_path=record,
        checkpoint_path=checkpoint,
        progress_path=progress,
        production=True,
    )
    completed = ChildChainDriver(store).run(
        atoms=atoms, outer_side=fixture.outer_side, square_side=fixture.square_side
    )
    store.read_progress(completed)
    if progress.exists():
        raise ChildError("progress marker survived the final checkpoint reconciliation")
    store.refuse_existing_result()
    result = child_result(completed, retained_sha256=RETAINED_SHA256)
    _write_exclusive(record, canonical_json(result) + "\n")
    return chain_status(checkpoint)


def _require(condition: bool, guard: str) -> None:  # noqa: FBT001
    if not condition:
        raise ChildError(f"selftest guard failed: {guard}")


def _expect_refusal(action: Callable[[], object], guard: str) -> None:
    try:
        action()
    except ChildError, CheckpointError:
        return
    raise ChildError(f"selftest guard failed: {guard}")


def _synthetic() -> tuple[tuple[Atom, ...], tuple[Direction, ...], Fraction, Fraction]:
    atoms = (
        Atom("a", Fraction(1, 2), Fraction(1, 2), Fraction(1)),
        Atom("b", Fraction(1), Fraction(1), Fraction(2)),
        Atom("c", Fraction(3, 2), Fraction(3, 2), Fraction(3)),
    )
    directions = (
        Direction("axis", Fraction(1), Fraction(0), Fraction(0), Fraction(1)),
        Direction(
            "three-four", Fraction(3, 5), Fraction(4, 5), Fraction(-4, 5), Fraction(3, 5)
        ),
        Direction(
            "five-twelve",
            Fraction(5, 13),
            Fraction(12, 13),
            Fraction(-12, 13),
            Fraction(5, 13),
        ),
        Direction(
            "eight-fifteen",
            Fraction(8, 17),
            Fraction(15, 17),
            Fraction(-15, 17),
            Fraction(8, 17),
        ),
    )
    return atoms, directions, Fraction(2), Fraction(1)


def _synthetic_parent(root: Path) -> ParentSpec:
    """Build a two-row synthetic parent chain with the unchanged exp-052 machinery."""

    atoms, directions, outer_side, square_side = _synthetic()
    result = root / "parent.json"
    checkpoint = root / "parent.checkpoint.json"
    progress = root / "parent.progress.json"
    binding = RunBinding(
        schema_version=SCHEMA_VERSION,
        experiment_id="exp-052",
        hypothesis_id="H-052",
        session_id="session-068",
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
    store = CheckpointStore(
        binding=binding,
        directions=directions,
        result_path=result,
        checkpoint_path=checkpoint,
        progress_path=progress,
    )
    calls = 0

    def stop_after_two(
        call_atoms: tuple[Atom, ...],
        direction: Direction,
        call_outer: Fraction,
        call_square: Fraction,
    ) -> DirectionManifest:
        nonlocal calls
        calls += 1
        if calls == 3:
            raise RuntimeError("synthetic parent timebox")
        return accumulate_source_faithful(call_atoms, direction, call_outer, call_square)

    try:
        DirectionSlicedDriver(store, source_accumulator=stop_after_two).run(
            atoms=atoms, outer_side=outer_side, square_side=square_side
        )
    except RuntimeError:
        pass
    else:
        raise ChildError("selftest guard failed: synthetic-parent-timebox")
    parent = store.load()
    return ParentSpec(
        experiment_id="exp-052",
        checkpoint_path=checkpoint,
        progress_path=progress,
        result_path=result,
        checkpoint_sha256=_sha256(checkpoint),
        progress_sha256=_sha256(progress),
        binding_hash=binding_hash(binding),
        last_row_hash=parent.rows[-1].row_hash,
        row_count=len(parent.rows),
    )


def _synthetic_binding(
    spec: ParentSpec,
    parent_rows: tuple[PairedRow, ...],
    out: Path,
    *,
    directions: tuple[Direction, ...],
    atoms: tuple[Atom, ...],
    outer_side: Fraction,
    square_side: Fraction,
) -> ChildBinding:
    return ChildBinding(
        schema_version=SCHEMA_VERSION,
        experiment_id=EXPERIMENT_ID,
        hypothesis_id=HYPOTHESIS_ID,
        session_id=SESSION_ID,
        experiment_record_path=EXPERIMENT_RECORD_PATH,
        parent_experiment_id=PARENT_EXPERIMENT_ID,
        parent_checkpoint_sha256=spec.checkpoint_sha256,
        parent_progress_sha256=spec.progress_sha256,
        parent_binding_hash=spec.binding_hash,
        parent_last_row_hash=parent_rows[-1].row_hash,
        parent_row_count=len(parent_rows),
        package_manifest_sha256=FROZEN_PACKAGE_SHA256,
        resume_driver_sha256=driver_sha256(),
        child_driver_sha256=child_driver_sha256(),
        fixture_hash=fixture_binding_hash(
            atoms=atoms,
            directions=directions,
            outer_side=outer_side,
            square_side=square_side,
        ),
        direction_count=len(directions),
        direction_hash=canonical_hash(directions),
        result_path=str(out / "child.json"),
        checkpoint_path=str(out / "child.checkpoint.json"),
        progress_path=str(out / "child.progress.json"),
    )


def synthetic_child_store(
    root: Path,
    name: str,
    *,
    spec: ParentSpec | None = None,
    progress_remover: Callable[[Path], None] = _durable_unlink,
) -> tuple[ChildCheckpointStore, tuple[Atom, ...], Fraction, Fraction]:
    """Assemble one synthetic parent-bound child store beneath ``root/name``."""

    atoms, directions, outer_side, square_side = _synthetic()
    if spec is None:
        parent_root = root / name / "parent"
        parent_root.mkdir(parents=True, exist_ok=True)
        spec = _synthetic_parent(parent_root)
    _, parent_rows = verify_parent(spec, directions)
    out = root / name / "out"
    out.mkdir(parents=True, exist_ok=True)
    binding = _synthetic_binding(
        spec,
        parent_rows,
        out,
        directions=directions,
        atoms=atoms,
        outer_side=outer_side,
        square_side=square_side,
    )
    store = ChildCheckpointStore(
        binding=binding,
        directions=directions,
        parent_rows=parent_rows,
        output_root=out,
        result_path=Path(binding.result_path),
        checkpoint_path=Path(binding.checkpoint_path),
        progress_path=Path(binding.progress_path),
        progress_remover=progress_remover,
    )
    return store, atoms, outer_side, square_side


def _rewrite(path: Path, mutate: Callable[[dict[str, Any]], None]) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    mutate(value)
    path.write_text(canonical_json(value) + "\n", encoding="utf-8")


def run_selftest() -> dict[str, object]:
    """Exercise every named child-chain guard on synthetic directions only."""

    verify_frozen_inputs()
    receipts: dict[str, bool] = {"frozen-inputs": True}
    with tempfile.TemporaryDirectory(prefix="n17-child-selftest-") as name:
        root = Path(name)
        base_parent = root / "base/parent"
        base_parent.mkdir(parents=True, exist_ok=True)
        base_spec = _synthetic_parent(base_parent)
        store, atoms, outer_side, square_side = synthetic_child_store(
            root, "base", spec=base_spec
        )
        parent_digests = (
            _sha256(base_parent / "parent.checkpoint.json"),
            _sha256(base_parent / "parent.progress.json"),
        )
        opened = store.open_chain()
        _require(len(opened.rows) == store.binding.parent_row_count, "parent-rows-carried")
        _require(
            opened.rows[-1].row_hash == store.binding.parent_last_row_hash,
            "parent-chain-anchor",
        )
        receipts["parent-verification"] = True
        receipts["parent-rows-carried"] = True
        receipts["parent-chain-anchor"] = True

        completed = ChildChainDriver(store).run(
            atoms=atoms, outer_side=outer_side, square_side=square_side
        )
        _require(len(completed.rows) == len(store.directions), "child-chain-completes")
        _require(
            completed.rows[store.binding.parent_row_count].previous_row_hash
            == store.binding.parent_last_row_hash,
            "child-chain-continuity",
        )
        _require(all(row.agreement for row in completed.rows), "synthetic-agreement")
        _require(store.read_progress(completed) is None, "no-final-progress")
        receipts["child-chain-completes"] = True
        receipts["child-chain-continuity"] = True
        receipts["synthetic-agreement"] = True
        receipts["no-final-progress"] = True

        status = chain_status(store.checkpoint_path)
        _require(status["complete"] is True and status["all_agree"] is True, "status-report")
        _require(status["last_row_hash"] == completed.rows[-1].row_hash, "status-last-hash")
        receipts["status-report"] = True
        receipts["status-last-hash"] = True

        uninterrupted_rows = canonical_json(completed.rows)
        baseline = json.loads(store.checkpoint_path.read_text(encoding="utf-8"))
        for guard, mutate in (
            (
                "tampered-child-row-payload",
                lambda value: value["rows"][-1]["source"].__setitem__("minimum", "999/1"),
            ),
            (
                "tampered-child-row-hash",
                lambda value: value["rows"][-1].__setitem__("row_hash", "0" * 64),
            ),
            (
                "tampered-child-chain-link",
                lambda value: value["rows"][-1].__setitem__("previous_row_hash", "0" * 64),
            ),
            (
                "tampered-carried-parent-row",
                lambda value: value["rows"][0].update({"agreement": False}),
            ),
            ("child-row-reorder", lambda value: value["rows"].reverse()),
            (
                "child-row-gap",
                lambda value: value["rows"][-1].__setitem__("ordinal", 9),
            ),
        ):
            _rewrite(store.checkpoint_path, mutate)
            _expect_refusal(store.load, guard)
            receipts[guard] = True
        store.checkpoint_path.write_text(canonical_json(baseline) + "\n", encoding="utf-8")
        _require(len(store.load().rows) == len(store.directions), "restored-baseline")
        receipts["restored-baseline"] = True

        for guard, path in (
            (
                "parent-path-write-refusal",
                OUTPUT_ROOT
                / "exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json",
            ),
            (
                "resume-package-write-refusal",
                Path("cases/n17_weighted_certificate_resume/stolen.json"),
            ),
            ("lexical-escape-refusal", store.output_root / ".." / "escaped.json"),
            ("resolved-escape-refusal", root / "outside.json"),
        ):
            _expect_refusal(
                lambda path=path: require_writable(path, store.output_root, "checkpoint path"),
                guard,
            )
            receipts[guard] = True

        _expect_refusal(
            lambda: ChildCheckpointStore(
                binding=replace(
                    store.binding,
                    checkpoint_path=str(
                        OUTPUT_ROOT
                        / "exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json"
                    ),
                ),
                directions=store.directions,
                parent_rows=store.parent_rows,
                output_root=store.output_root,
                result_path=store.result_path,
                checkpoint_path=OUTPUT_ROOT
                / "exp-052-h-052-n17-resumable-certificate-agreement.checkpoint.json",
                progress_path=store.progress_path,
            ),
            "parent-bound-store-refusal",
        )
        receipts["parent-bound-store-refusal"] = True

        interrupted, interrupted_atoms, interrupted_outer, interrupted_square = (
            synthetic_child_store(root, "interrupted", spec=base_spec)
        )

        def interrupt_independent(*_args: object) -> DirectionManifest:
            raise RuntimeError("synthetic between-accumulator interruption")

        try:
            ChildChainDriver(interrupted, independent_accumulator=interrupt_independent).run(
                atoms=interrupted_atoms,
                outer_side=interrupted_outer,
                square_side=interrupted_square,
            )
        except RuntimeError:
            pass
        else:
            raise ChildError("selftest guard failed: between-accumulator-interruption")
        partial = interrupted.load()
        _require(
            len(partial.rows) == interrupted.binding.parent_row_count,
            "no-partial-row-promotion",
        )
        _require(interrupted.progress_path.is_file(), "progress-marker-written")
        resumed = ChildChainDriver(interrupted).run(
            atoms=interrupted_atoms,
            outer_side=interrupted_outer,
            square_side=interrupted_square,
        )
        _require(
            canonical_json(resumed.rows) == uninterrupted_rows,
            "interrupted-resume-equivalence",
        )
        receipts["between-accumulator-interruption"] = True
        receipts["no-partial-row-promotion"] = True
        receipts["progress-marker-written"] = True
        receipts["interrupted-resume-equivalence"] = True

        _expect_refusal(
            lambda: child_result(
                ChildCheckpoint(store.binding, completed.rows[:-1]),
                retained_sha256=RETAINED_SHA256,
            ),
            "incomplete-result-refusal",
        )
        receipts["incomplete-result-refusal"] = True

        result = child_result(completed, retained_sha256=RETAINED_SHA256)
        _write_exclusive(store.result_path, canonical_json(result) + "\n")
        _expect_refusal(
            lambda: _write_exclusive(store.result_path, canonical_json(result) + "\n"),
            "result-overwrite-refusal",
        )
        _expect_refusal(store.load, "result-blocks-further-chain-writes")
        receipts["result-overwrite-refusal"] = True
        receipts["result-blocks-further-chain-writes"] = True

        disagree, disagree_atoms, disagree_outer, disagree_square = synthetic_child_store(
            root, "disagreement", spec=base_spec
        )

        def perturbed_independent(
            call_atoms: tuple[Atom, ...],
            direction: Direction,
            call_outer: Fraction,
            call_square: Fraction,
        ) -> DirectionManifest:
            manifest = accumulate_target_independent(
                call_atoms, direction, call_outer, call_square
            )
            return replace(manifest, minimum=manifest.minimum + 1)

        try:
            ChildChainDriver(disagree, independent_accumulator=perturbed_independent).run(
                atoms=disagree_atoms,
                outer_side=disagree_outer,
                square_side=disagree_square,
            )
        except DisagreementStopError:
            pass
        else:
            raise ChildError("selftest guard failed: disagreement-stop")
        retained = disagree.load()
        _require(
            len(retained.rows) == disagree.binding.parent_row_count + 1,
            "disagreement-stops-after-one-row",
        )
        _require(retained.rows[-1].agreement is False, "disagreement-retained-as-row")
        disagree_status = chain_status(disagree.checkpoint_path)
        _require(
            disagree_status["first_disagreement_ordinal"] == disagree.binding.parent_row_count,
            "disagreement-visible-in-status",
        )
        receipts["disagreement-stop"] = True
        receipts["disagreement-stops-after-one-row"] = True
        receipts["disagreement-retained-as-row"] = True
        receipts["disagreement-visible-in-status"] = True

        spoiled, _, _, _ = synthetic_child_store(root, "spoiled")
        _rewrite(
            Path(str(spoiled.checkpoint_path)).parent.parent / "parent/parent.checkpoint.json",
            lambda value: value["rows"][0].__setitem__("row_hash", "0" * 64),
        )
        spoiled_parent = root / "spoiled/parent"
        _expect_refusal(
            lambda: verify_parent(
                ParentSpec(
                    experiment_id="exp-052",
                    checkpoint_path=spoiled_parent / "parent.checkpoint.json",
                    progress_path=spoiled_parent / "parent.progress.json",
                    result_path=spoiled_parent / "parent.json",
                    checkpoint_sha256=_sha256(spoiled_parent / "parent.checkpoint.json"),
                    progress_sha256=_sha256(spoiled_parent / "parent.progress.json"),
                    binding_hash=spoiled.binding.parent_binding_hash,
                    last_row_hash=spoiled.binding.parent_last_row_hash,
                    row_count=spoiled.binding.parent_row_count,
                ),
                spoiled.directions,
            ),
            "tampered-parent-row-refusal",
        )
        _expect_refusal(
            lambda: verify_parent(
                ParentSpec(
                    experiment_id="exp-052",
                    checkpoint_path=spoiled_parent / "parent.checkpoint.json",
                    progress_path=spoiled_parent / "parent.progress.json",
                    result_path=spoiled_parent / "parent.json",
                    checkpoint_sha256="0" * 64,
                    progress_sha256="0" * 64,
                    binding_hash=spoiled.binding.parent_binding_hash,
                    last_row_hash=spoiled.binding.parent_last_row_hash,
                    row_count=spoiled.binding.parent_row_count,
                ),
                spoiled.directions,
            ),
            "parent-digest-mismatch-refusal",
        )
        receipts["tampered-parent-row-refusal"] = True
        receipts["parent-digest-mismatch-refusal"] = True

        _require(
            parent_digests
            == (
                _sha256(root / "base/parent/parent.checkpoint.json"),
                _sha256(root / "base/parent/parent.progress.json"),
            ),
            "parent-artifacts-unchanged",
        )
        receipts["parent-artifacts-unchanged"] = True

    return {
        "schema_version": 1,
        "selftest": "exp-056-w7-child-chain-readiness",
        "passed": all(receipts.values()),
        "skipped": 0,
        "child_driver_sha256": child_driver_sha256(),
        "resume_driver_sha256": driver_sha256(),
        "frozen_package_sha256": FROZEN_PACKAGE_SHA256,
        "guard_count": len(receipts),
        "receipts": dict(sorted(receipts.items())),
        "receipt_hash": canonical_hash(dict(sorted(receipts.items()))),
    }


def selftest_json() -> str:
    return canonical_json(run_selftest())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--record", type=Path)
    action.add_argument("--selftest", action="store_true")
    action.add_argument("--status", type=Path)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--progress", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.selftest:
        if args.checkpoint is not None or args.progress is not None:
            raise ChildError("selftest does not accept output paths")
        print(selftest_json())
        return 0
    if args.status is not None:
        if args.checkpoint is not None or args.progress is not None:
            raise ChildError("status does not accept output paths")
        print(canonical_json(chain_status(args.status)))
        return 0
    if args.record is None or args.checkpoint is None or args.progress is None:
        raise ChildError("--record, --checkpoint and --progress are required")
    try:
        print(canonical_json(run_target(args.record, args.checkpoint, args.progress)))
    except DisagreementStopError as stop:
        print(
            canonical_json(
                {
                    "schema_version": 1,
                    "stopped_by": "disagreement",
                    "detail": str(stop),
                    "status": chain_status(args.checkpoint),
                }
            )
        )
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
