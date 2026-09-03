"""Fresh H-052 successor chain and complete result assembler.

This module adds no arithmetic.  It verifies two *separate* frozen ancestries -- the
exp-056 checkpoint as the immediate parent, and the exp-052 checkpoint as the carried
chain genesis -- carries exp-056's 170 verified rows verbatim into a fresh checkpoint,
recomputes the interrupted ordinal 170 rather than promoting it, and continues to
ordinal 180.

It exists because exp-056's child assembler cannot decide H-052: it omits both
181-row ``CertificateManifest`` summaries, the global minima, the shrink-and-scaling
preconditions, the mutation map, ``all_mutations_rejected`` and ``instrument_valid``.
Two explicit terminal schemas are defined here, and both require that evidence.

Nothing under ``cases/n17_weighted_certificate``, ``cases/n17_weighted_certificate_resume``
or ``cases/n17_weighted_certificate_child`` is writable from here, and no exp-052 or
exp-056 output path is writable from here.  Importing this module performs no
measurement and does not parse the retained fixture.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path
from typing import Any

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
    scaling_preconditions,
)
from cases.n17_weighted_certificate.run import (
    CLEAN_ROOM_SHA256,
    _mutation_guards,  # pyright: ignore[reportPrivateUsage]
    _normalized_atoms,  # pyright: ignore[reportPrivateUsage]
    _preconditions,  # pyright: ignore[reportPrivateUsage]
)
from cases.n17_weighted_certificate_child.run import (
    EXPERIMENT_RECORD_PATH as CHILD_EXPERIMENT_RECORD_PATH,
)
from cases.n17_weighted_certificate_child.run import (
    ChildBinding,
    ChildChainDriver,
    ChildCheckpointStore,
    ChildError,
    ParentSpec,
    _child_binding,  # pyright: ignore[reportPrivateUsage]
    _write_exclusive,  # pyright: ignore[reportPrivateUsage]
    child_binding_hash,
    child_driver_sha256,
    verify_parent,
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
    _certificate,  # pyright: ignore[reportPrivateUsage]
    _digest,  # pyright: ignore[reportPrivateUsage]
    _durable_unlink,  # pyright: ignore[reportPrivateUsage]
    _fraction,  # pyright: ignore[reportPrivateUsage]
    _integer,  # pyright: ignore[reportPrivateUsage]
    _manifest,  # pyright: ignore[reportPrivateUsage]
    _paired_row,  # pyright: ignore[reportPrivateUsage]
    _progress_marker,  # pyright: ignore[reportPrivateUsage]
    _row_hash,  # pyright: ignore[reportPrivateUsage]
    _string,  # pyright: ignore[reportPrivateUsage]
    _validate_manifest,  # pyright: ignore[reportPrivateUsage]
    accumulate_source_faithful,
    accumulate_target_independent,
    binding_hash,
    driver_sha256,
    fixture_binding_hash,
    verify_frozen_inputs,
)

PACKING_ROOT = Path(__file__).resolve().parents[2]
SUCCESSOR_DRIVER_PATH = Path(__file__)

# Every package whose bytes this driver is bound to, and into which it may never write.
FROZEN_PACKAGES = (
    PACKING_ROOT / "cases/n17_weighted_certificate",
    PACKING_ROOT / "cases/n17_weighted_certificate_resume",
    PACKING_ROOT / "cases/n17_weighted_certificate_child",
)

# BC-147 found that the exp-056 child driver's forbidden set names only "exp-052" and
# the resume package, so it would have accepted an exp-056 output path.  The successor
# closes that gap: its own immediate parent is now protected by name as well.
FORBIDDEN_SLUGS = (
    "exp-052",
    "exp-056",
    "n17_weighted_certificate_resume",
    "n17_weighted_certificate_child",
)

OUTPUT_ROOT = Path("campaign/series/series-000-smoke-and-calibration/results")

# --- Allocated identity -------------------------------------------------------------
# These two lines are the coordinator's to confirm against the record it allocates for
# BC-148.  Changing either changes SUCCESSOR_DRIVER_SHA256 and therefore the binding, so
# both must be settled before the writer opens a chain.
EXPERIMENT_ID = "exp-058"
SESSION_ID = "session-083"

HYPOTHESIS_ID = "H-052"
SLUG = f"{EXPERIMENT_ID}-h-052-n17-fresh-successor-completion"
EXPERIMENT_RECORD_PATH = (
    f"campaign/series/series-000-smoke-and-calibration/experiments/{SLUG}.md"
)
RESULT_PATH = OUTPUT_ROOT / f"{SLUG}.json"
CHECKPOINT_PATH = OUTPUT_ROOT / f"{SLUG}.checkpoint.json"
PROGRESS_PATH = OUTPUT_ROOT / f"{SLUG}.progress.json"

# --- Immediate parent: the exp-056 checkpoint ---------------------------------------
IMMEDIATE_PARENT_ROLE = "immediate-parent-checkpoint"
IMMEDIATE_PARENT_ID = "exp-056"
IMMEDIATE_PARENT_SLUG = "exp-056-h-052-n17-sequential-larger-prefix"
IMMEDIATE_PARENT_CHECKPOINT = OUTPUT_ROOT / f"{IMMEDIATE_PARENT_SLUG}.checkpoint.json"
IMMEDIATE_PARENT_PROGRESS = OUTPUT_ROOT / f"{IMMEDIATE_PARENT_SLUG}.progress.json"
IMMEDIATE_PARENT_CHECKPOINT_SHA256 = (
    "0d39a7e734e8afc62fda914fda4ec8b5e9b2e48ea1b1d8b197dc08e27e7a35d4"
)
IMMEDIATE_PARENT_PROGRESS_SHA256 = (
    "0875f31fbf7391cfa40349812ca38a786069830a28f1c8d92ffd4ab33ecfe93c"
)
IMMEDIATE_PARENT_LAST_ROW_HASH = (
    "8947b38e0351048c3a67d914f2b8449185686d920913f5a2404898bdeca4c0b6"
)
IMMEDIATE_PARENT_ROW_COUNT = 170

# --- Carried chain genesis: the exp-052 checkpoint ----------------------------------
CHAIN_GENESIS_ROLE = "carried-chain-genesis"
CHAIN_GENESIS_ID = "exp-052"
CHAIN_GENESIS_SLUG = "exp-052-h-052-n17-resumable-certificate-agreement"
CHAIN_GENESIS_CHECKPOINT = OUTPUT_ROOT / f"{CHAIN_GENESIS_SLUG}.checkpoint.json"
CHAIN_GENESIS_PROGRESS = OUTPUT_ROOT / f"{CHAIN_GENESIS_SLUG}.progress.json"
CHAIN_GENESIS_RESULT = OUTPUT_ROOT / f"{CHAIN_GENESIS_SLUG}.json"
CHAIN_GENESIS_CHECKPOINT_SHA256 = (
    "db5c156959b6de4e6f2c9be283454d01dd5f3a436e6489f5e6bb60c38559fdb8"
)
CHAIN_GENESIS_PROGRESS_SHA256 = (
    "08e301b01c7ac6eef4b03c3a4daa5f72c5f1bdbe217dbbb061b57f5c94d947af"
)
CHAIN_GENESIS_BINDING_HASH = "2446fa39e154800410b9b5cc19f19aed7cc0c797d116f7ece1c97a2c7c0b4d1a"
CHAIN_GENESIS_LAST_ROW_HASH = "9badcc57c05e328344b0ec7ae4fbf9815e8eae027a79bec1bf1a35b9871fade6"
CHAIN_GENESIS_ROW_COUNT = 33

DIRECTION_COUNT = 181
FIRST_NEW_ORDINAL = IMMEDIATE_PARENT_ROW_COUNT
RESUME_STAGE: ProgressStage = "independent_started"

TERMINAL_COMPLETE_AGREEMENT = "complete-agreement"
TERMINAL_EARLY_DISAGREEMENT = "early-disagreement"

CLAIM_BOUNDARY = (
    "Exact agreement between two implementations on one retained certificate. It is "
    "not an independent proof method, not source adoption, and not a frontier change; "
    "a disagreement rejects the agreement claim only, at H-052's registered scope."
)


class SuccessorError(RuntimeError):
    """An ancestry, chain, schema, derivation or publication guard failed."""


class SuccessorDisagreementStopError(RuntimeError):
    """The two unchanged accumulators disagreed exactly; the row is retained."""


# Every refusal this package can legitimately raise, including the two inherited from
# the frozen packages it calls into.
REFUSALS = (SuccessorError, ChildError, CheckpointError)


@dataclass(frozen=True, slots=True)
class ImmediateParent:
    """The exp-056 boundary this round resumes from. Never the chain genesis."""

    role: str
    experiment_id: str
    checkpoint_path: str
    progress_path: str
    checkpoint_sha256: str
    progress_sha256: str
    binding_hash: str
    last_row_hash: str
    row_count: int
    resume_ordinal: int
    resume_stage: str


@dataclass(frozen=True, slots=True)
class ChainGenesis:
    """The exp-052 origin the carried chain is anchored to. Never the parent."""

    role: str
    experiment_id: str
    checkpoint_path: str
    progress_path: str
    checkpoint_sha256: str
    progress_sha256: str
    binding_hash: str
    last_row_hash: str
    row_count: int
    resume_ordinal: int
    resume_stage: str


@dataclass(frozen=True, slots=True)
class SuccessorBinding:
    """Immutable provenance for one fresh successor round, with both ancestries."""

    schema_version: int
    experiment_id: str
    hypothesis_id: str
    session_id: str
    experiment_record_path: str
    immediate_parent: ImmediateParent
    chain_genesis: ChainGenesis
    package_manifest_sha256: str
    frozen_source_sha256: tuple[tuple[str, str], ...]
    resume_driver_sha256: str
    child_driver_sha256: str
    successor_driver_sha256: str
    retained_sha256: str
    clean_room_sha256: str
    fixture_hash: str
    direction_count: int
    direction_hash: str
    first_new_ordinal: int
    result_path: str
    checkpoint_path: str
    progress_path: str


@dataclass(frozen=True, slots=True)
class SuccessorCheckpoint:
    """The carried exp-056 prefix plus every newly computed row, in one chain."""

    binding: SuccessorBinding
    rows: tuple[PairedRow, ...]


@dataclass(frozen=True, slots=True)
class FrozenExpectations:
    """The preregistered exact certificate values both summaries must reproduce."""

    atom_count: int
    direction_count: int
    total_weight: Fraction
    global_minimum: Fraction


PRODUCTION_EXPECTATIONS = FrozenExpectations(
    atom_count=168,
    direction_count=181,
    total_weight=Fraction(9744, 576),
    global_minimum=Fraction(576, 576),
)


@dataclass(frozen=True, slots=True)
class InstrumentEvidence:
    """Everything both terminal schemas require besides the chain itself."""

    preconditions: dict[str, object]
    shrink_and_scaling: dict[str, object]
    mutation_guards: dict[str, bool]
    expectations: FrozenExpectations


@dataclass(frozen=True, slots=True)
class ImmediateParentSpec:
    """What the immediate parent must be, declared before it is read."""

    experiment_id: str
    genesis_experiment_id: str
    checkpoint_path: Path
    progress_path: Path
    result_path: Path
    checkpoint_sha256: str
    progress_sha256: str
    binding_hash: str
    last_row_hash: str
    row_count: int
    genesis_binding_hash: str
    genesis_last_row_hash: str
    genesis_row_count: int
    resume_ordinal: int
    resume_stage: str


@dataclass(frozen=True, slots=True)
class AncestryReceipt:
    """Both verified ancestries and the carried rows they jointly authorize."""

    immediate_parent: ImmediateParent
    chain_genesis: ChainGenesis
    immediate_parent_binding: ChildBinding
    carried_rows: tuple[PairedRow, ...]
    genesis_rows: tuple[PairedRow, ...]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def successor_driver_sha256() -> str:
    """Hash this driver independently of the two frozen drivers it calls."""

    return _sha256(SUCCESSOR_DRIVER_PATH)


def successor_binding_hash(binding: SuccessorBinding) -> str:
    """Return the provenance digest of a successor binding block."""

    return canonical_hash({"domain": "n17-successor-binding-v1", "binding": binding})


def _checkpoint_json(checkpoint: SuccessorCheckpoint) -> str:
    return canonical_json({"binding": checkpoint.binding, "rows": checkpoint.rows}) + "\n"


def _exact_object(value: object, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != fields:
        raise SuccessorError(f"malformed {label}")
    return value


def _bool(value: object, label: str) -> bool:
    if not isinstance(value, bool):
        raise SuccessorError(f"malformed {label}")
    return value


def require_writable(path: Path, output_root: Path, label: str) -> Path:
    """Refuse every output path outside the bound root, or naming a frozen artifact."""

    text = path.as_posix()
    for forbidden in FORBIDDEN_SLUGS:
        if forbidden in text:
            raise SuccessorError(f"{label} names a frozen ancestor artifact: {path}")
    if ".." in path.parts:
        raise SuccessorError(f"{label} escapes its bound root lexically: {path}")
    if path.is_symlink() or path.parent.is_symlink():
        raise SuccessorError(f"{label} is a symbolic link: {path}")
    root = output_root.resolve(strict=False)
    resolved = path.resolve(strict=False)
    if not resolved.is_relative_to(root):
        raise SuccessorError(f"{label} escapes its bound root: {path}")
    for package in FROZEN_PACKAGES:
        if resolved.is_relative_to(package.resolve(strict=False)):
            raise SuccessorError(f"{label} would write inside a frozen package: {path}")
    return resolved


def _read_marker(path: Path, label: str) -> ProgressMarker:
    """Parse one progress marker and require canonical bytes."""

    if not path.is_file():
        raise SuccessorError(f"{label} is absent: {path}")
    try:
        text = path.read_text(encoding="utf-8")
        marker = _progress_marker(json.loads(text))
    except (OSError, json.JSONDecodeError, CheckpointError) as error:
        raise SuccessorError(f"{label} is unreadable: {error}") from error
    if text != canonical_json(marker) + "\n":
        raise SuccessorError(f"{label} serialization is not canonical")
    if marker.schema_version != SCHEMA_VERSION:
        raise SuccessorError(f"{label} schema changed")
    return marker


def verify_chain_genesis(
    spec: ParentSpec, directions: tuple[Direction, ...], *, resume_stage: str
) -> tuple[tuple[PairedRow, ...], ChainGenesis]:
    """Replay the exp-052 genesis through exp-056's already-reviewed verifier."""

    if spec.experiment_id == IMMEDIATE_PARENT_ID:
        raise SuccessorError("the chain genesis may not be the immediate parent")
    try:
        _, rows = verify_parent(spec, directions)
    except (ChildError, CheckpointError) as error:
        raise SuccessorError(f"chain genesis failed verification: {error}") from error
    marker = _read_marker(spec.progress_path, "chain genesis progress marker")
    if marker.binding_hash != spec.binding_hash:
        raise SuccessorError("chain genesis marker is not bound to its own binding")
    if marker.ordinal != spec.row_count:
        raise SuccessorError("chain genesis marker is not at its first incomplete ordinal")
    if marker.stage != resume_stage:
        raise SuccessorError(
            f"chain genesis marker stage is {marker.stage}, declared {resume_stage}"
        )
    genesis = ChainGenesis(
        role=CHAIN_GENESIS_ROLE,
        experiment_id=spec.experiment_id,
        checkpoint_path=spec.checkpoint_path.as_posix(),
        progress_path=spec.progress_path.as_posix(),
        checkpoint_sha256=spec.checkpoint_sha256,
        progress_sha256=spec.progress_sha256,
        binding_hash=spec.binding_hash,
        last_row_hash=spec.last_row_hash,
        row_count=spec.row_count,
        resume_ordinal=marker.ordinal,
        resume_stage=marker.stage,
    )
    return rows, genesis


def verify_immediate_parent(
    spec: ImmediateParentSpec, directions: tuple[Direction, ...]
) -> tuple[ChildBinding, tuple[PairedRow, ...], ImmediateParent]:
    """Read-only replay of the exp-056 checkpoint, binding, chain and live marker.

    This never constructs a writable store over the frozen paths, so no code path in
    this function can publish, truncate or resume the retained artifact.
    """

    if spec.experiment_id == spec.genesis_experiment_id:
        raise SuccessorError("the immediate parent may not also be the chain genesis")
    for path, expected, label in (
        (spec.checkpoint_path, spec.checkpoint_sha256, "immediate parent checkpoint"),
        (spec.progress_path, spec.progress_sha256, "immediate parent progress marker"),
    ):
        if not path.is_file():
            raise SuccessorError(f"{label} is absent: {path}")
        actual = _sha256(path)
        if actual != expected:
            raise SuccessorError(f"{label} digest changed: expected {expected}, got {actual}")
    try:
        text = spec.checkpoint_path.read_text(encoding="utf-8")
        value = json.loads(text)
    except (OSError, json.JSONDecodeError) as error:
        raise SuccessorError("immediate parent checkpoint is unreadable") from error
    raw = _exact_object(value, {"binding", "rows"}, "immediate parent checkpoint")
    try:
        binding = _child_binding(raw["binding"])
    except (ChildError, CheckpointError) as error:
        raise SuccessorError(f"immediate parent binding is malformed: {error}") from error
    if binding.experiment_id != spec.experiment_id:
        raise SuccessorError("immediate parent binding names a different experiment")
    if binding.parent_experiment_id != spec.genesis_experiment_id:
        raise SuccessorError("immediate parent does not descend from the declared genesis")
    if child_binding_hash(binding) != spec.binding_hash:
        raise SuccessorError("immediate parent binding hash changed")
    if binding.parent_binding_hash != spec.genesis_binding_hash:
        raise SuccessorError("immediate parent is not anchored to the declared genesis")
    if binding.parent_last_row_hash != spec.genesis_last_row_hash:
        raise SuccessorError("immediate parent genesis row hash changed")
    if binding.parent_row_count != spec.genesis_row_count:
        raise SuccessorError("immediate parent genesis row count changed")
    if binding.direction_count != len(directions):
        raise SuccessorError("immediate parent direction count mismatch")
    if binding.direction_hash != canonical_hash(directions):
        raise SuccessorError("immediate parent direction hash mismatch")
    if binding.package_manifest_sha256 != FROZEN_PACKAGE_SHA256:
        raise SuccessorError("immediate parent does not name the frozen package")
    if binding.result_path != str(spec.result_path):
        raise SuccessorError("immediate parent binding names a different result path")
    if spec.result_path.exists():
        raise SuccessorError("the immediate parent published a result after it was frozen")
    raw_rows = raw["rows"]
    if not isinstance(raw_rows, list):
        raise SuccessorError("malformed immediate parent rows")
    try:
        rows = tuple(_paired_row(row) for row in raw_rows)
    except CheckpointError as error:
        raise SuccessorError(f"malformed immediate parent row: {error}") from error
    if text != canonical_json({"binding": binding, "rows": rows}) + "\n":
        raise SuccessorError("immediate parent checkpoint serialization is not canonical")
    if len(rows) != spec.row_count:
        raise SuccessorError("immediate parent is not the declared row count")
    if len(rows) > len(directions):
        raise SuccessorError("immediate parent has more rows than directions")
    previous = binding.parent_binding_hash
    for ordinal, row in enumerate(rows):
        if row.ordinal != ordinal:
            raise SuccessorError("immediate parent ordinals are not contiguous")
        if row.direction != directions[ordinal]:
            raise SuccessorError("immediate parent direction order changed")
        _validate_manifest(row.source, row.direction, "immediate parent source")
        _validate_manifest(row.independent, row.direction, "immediate parent independent")
        if row.previous_row_hash != previous:
            raise SuccessorError("immediate parent hash chain changed")
        if row.agreement != (row.source == row.independent):
            raise SuccessorError("immediate parent agreement flag changed")
        if row.row_hash != _row_hash(
            ordinal=row.ordinal,
            direction=row.direction,
            source=row.source,
            independent=row.independent,
            agreement=row.agreement,
            previous_row_hash=row.previous_row_hash,
        ):
            raise SuccessorError("immediate parent row hash changed")
        if not row.agreement:
            raise SuccessorError(f"immediate parent retains a disagreement at {ordinal}")
        previous = row.row_hash
    if rows[-1].row_hash != spec.last_row_hash:
        raise SuccessorError("immediate parent last row hash changed")
    if rows[spec.genesis_row_count - 1].row_hash != spec.genesis_last_row_hash:
        raise SuccessorError("carried genesis boundary row hash changed")
    marker = _read_marker(spec.progress_path, "immediate parent progress marker")
    if marker.binding_hash != spec.binding_hash:
        raise SuccessorError("immediate parent marker is not bound to its own binding")
    if marker.ordinal != spec.resume_ordinal or marker.ordinal != len(rows):
        raise SuccessorError("immediate parent marker is not at the first incomplete ordinal")
    if marker.ordinal >= len(directions):
        raise SuccessorError("immediate parent marker is beyond the final direction")
    if marker.stage != spec.resume_stage:
        raise SuccessorError(
            f"immediate parent marker stage is {marker.stage}, declared {spec.resume_stage}"
        )
    if marker.previous_row_hash != rows[-1].row_hash:
        raise SuccessorError("immediate parent marker is not chained to its last row")
    parent = ImmediateParent(
        role=IMMEDIATE_PARENT_ROLE,
        experiment_id=spec.experiment_id,
        checkpoint_path=spec.checkpoint_path.as_posix(),
        progress_path=spec.progress_path.as_posix(),
        checkpoint_sha256=spec.checkpoint_sha256,
        progress_sha256=spec.progress_sha256,
        binding_hash=spec.binding_hash,
        last_row_hash=spec.last_row_hash,
        row_count=len(rows),
        resume_ordinal=marker.ordinal,
        resume_stage=marker.stage,
    )
    return binding, rows, parent


def verify_ancestry(
    *,
    immediate_spec: ImmediateParentSpec,
    genesis_spec: ParentSpec,
    directions: tuple[Direction, ...],
    genesis_resume_stage: str,
) -> AncestryReceipt:
    """Verify both ancestries independently, then cross-check that one contains the other."""

    genesis_rows, genesis = verify_chain_genesis(
        genesis_spec, directions, resume_stage=genesis_resume_stage
    )
    binding, carried_rows, parent = verify_immediate_parent(immediate_spec, directions)
    if parent.role == genesis.role:
        raise SuccessorError("both ancestries claim the same role")
    if parent.experiment_id == genesis.experiment_id:
        raise SuccessorError("both ancestries name the same experiment")
    if genesis.row_count >= parent.row_count:
        raise SuccessorError("the chain genesis is not a proper prefix of its parent")
    if carried_rows[: len(genesis_rows)] != genesis_rows:
        raise SuccessorError("the carried prefix does not reproduce the genesis rows")
    if carried_rows[0].previous_row_hash != genesis.binding_hash:
        raise SuccessorError("the carried chain is not anchored at the genesis binding")
    return AncestryReceipt(
        immediate_parent=parent,
        chain_genesis=genesis,
        immediate_parent_binding=binding,
        carried_rows=carried_rows,
        genesis_rows=genesis_rows,
    )


class SuccessorCheckpointStore:
    """Persist and validate one successor chain under a bound, fresh output root."""

    def __init__(
        self,
        *,
        binding: SuccessorBinding,
        directions: tuple[Direction, ...],
        carried_rows: tuple[PairedRow, ...],
        output_root: Path,
        result_path: Path,
        checkpoint_path: Path,
        progress_path: Path,
        production: bool = False,
        progress_remover: Callable[[Path], None] = _durable_unlink,
    ) -> None:
        self.binding = binding
        self.directions = directions
        self.carried_rows = carried_rows
        self.output_root = output_root
        self.result_path = result_path
        self.checkpoint_path = checkpoint_path
        self.progress_path = progress_path
        self.production = production
        self.progress_remover = progress_remover
        self._validate_binding()

    def _validate_binding(self) -> None:
        binding = self.binding
        if binding.schema_version != SCHEMA_VERSION:
            raise SuccessorError("unsupported successor checkpoint schema version")
        if binding.hypothesis_id != HYPOTHESIS_ID:
            raise SuccessorError("successor checkpoint is not bound to H-052")
        if binding.package_manifest_sha256 != FROZEN_PACKAGE_SHA256:
            raise SuccessorError("successor binding does not name the frozen package")
        if binding.frozen_source_sha256 != FROZEN_SOURCE_SHA256:
            raise SuccessorError("successor binding does not name the frozen source set")
        if binding.resume_driver_sha256 != driver_sha256():
            raise SuccessorError("resume driver hash mismatch")
        if binding.child_driver_sha256 != child_driver_sha256():
            raise SuccessorError("child driver hash mismatch")
        if binding.successor_driver_sha256 != successor_driver_sha256():
            raise SuccessorError("successor driver hash mismatch")
        if binding.retained_sha256 != RETAINED_SHA256:
            raise SuccessorError("successor binding does not name the retained source")
        if binding.clean_room_sha256 != CLEAN_ROOM_SHA256:
            raise SuccessorError("successor binding does not name the clean-room path")
        if binding.immediate_parent.role != IMMEDIATE_PARENT_ROLE:
            raise SuccessorError("immediate parent block does not carry its own role")
        if binding.chain_genesis.role != CHAIN_GENESIS_ROLE:
            raise SuccessorError("chain genesis block does not carry its own role")
        if binding.immediate_parent.experiment_id == binding.chain_genesis.experiment_id:
            raise SuccessorError("both ancestry blocks name the same experiment")
        if binding.chain_genesis.row_count >= binding.immediate_parent.row_count:
            raise SuccessorError("the chain genesis is not a proper prefix of its parent")
        if binding.direction_count != len(self.directions):
            raise SuccessorError("successor binding direction count mismatch")
        if binding.direction_hash != canonical_hash(self.directions):
            raise SuccessorError("successor binding direction hash mismatch")
        if binding.immediate_parent.row_count != len(self.carried_rows):
            raise SuccessorError("successor binding carried row count mismatch")
        if not self.carried_rows:
            raise SuccessorError("a successor chain needs a nonempty carried prefix")
        if binding.immediate_parent.last_row_hash != self.carried_rows[-1].row_hash:
            raise SuccessorError("successor binding carried row hash mismatch")
        if binding.chain_genesis.binding_hash != self.carried_rows[0].previous_row_hash:
            raise SuccessorError("successor binding genesis anchor mismatch")
        if binding.first_new_ordinal != len(self.carried_rows):
            raise SuccessorError("first new ordinal is not the first incomplete ordinal")
        if binding.first_new_ordinal != binding.immediate_parent.resume_ordinal:
            raise SuccessorError("first new ordinal does not match the parent's marker")
        if binding.first_new_ordinal >= len(self.directions):
            raise SuccessorError("first new ordinal is beyond the final direction")
        for path, declared, label in (
            (self.result_path, binding.result_path, "result path"),
            (self.checkpoint_path, binding.checkpoint_path, "checkpoint path"),
            (self.progress_path, binding.progress_path, "progress path"),
        ):
            if declared != str(path):
                raise SuccessorError(f"successor binding {label} mismatch")
            require_writable(path, self.output_root, label)
        if self.production and (
            (self.result_path, self.checkpoint_path, self.progress_path)
            != (RESULT_PATH, CHECKPOINT_PATH, PROGRESS_PATH)
            or self.output_root != OUTPUT_ROOT
            or binding.experiment_id != EXPERIMENT_ID
            or binding.session_id != SESSION_ID
            or binding.experiment_record_path != EXPERIMENT_RECORD_PATH
        ):
            raise SuccessorError("production identity does not match the preregistration")

    def refuse_existing_result(self) -> None:
        if self.result_path.exists():
            raise SuccessorError("result path already exists")

    def _validate_rows(self, rows: tuple[PairedRow, ...]) -> None:
        if len(rows) < len(self.carried_rows):
            raise SuccessorError("successor checkpoint dropped a carried row")
        if len(rows) > len(self.directions):
            raise SuccessorError("successor checkpoint contains too many rows")
        if rows[: len(self.carried_rows)] != self.carried_rows:
            raise SuccessorError("carried rows changed")
        previous = self.binding.chain_genesis.binding_hash
        for ordinal, row in enumerate(rows):
            if row.ordinal != ordinal:
                raise SuccessorError("successor ordinals are not contiguous")
            if row.direction != self.directions[ordinal]:
                raise SuccessorError("successor direction order changed")
            _validate_manifest(row.source, row.direction, "source")
            _validate_manifest(row.independent, row.direction, "independent")
            if row.previous_row_hash != previous:
                raise SuccessorError("successor hash chain changed")
            if row.agreement != (row.source == row.independent):
                raise SuccessorError("successor agreement flag changed")
            if row.row_hash != _row_hash(
                ordinal=row.ordinal,
                direction=row.direction,
                source=row.source,
                independent=row.independent,
                agreement=row.agreement,
                previous_row_hash=row.previous_row_hash,
            ):
                raise SuccessorError("successor row hash changed")
            previous = row.row_hash

    def open_chain(self) -> SuccessorCheckpoint:
        """Carry the verified parent prefix into a fresh chain, or resume a valid one."""

        self.refuse_existing_result()
        if self.checkpoint_path.exists():
            checkpoint = self.load()
            self.read_progress(checkpoint)
            return checkpoint
        if self.progress_path.exists():
            raise SuccessorError("progress marker exists without a successor checkpoint")
        checkpoint = SuccessorCheckpoint(self.binding, self.carried_rows)
        self._validate_rows(checkpoint.rows)
        _atomic_write(self.checkpoint_path, _checkpoint_json(checkpoint))
        return checkpoint

    def load(self) -> SuccessorCheckpoint:
        self.refuse_existing_result()
        try:
            text = self.checkpoint_path.read_text(encoding="utf-8")
            value = json.loads(text)
        except (OSError, json.JSONDecodeError) as error:
            raise SuccessorError("successor checkpoint is unreadable") from error
        raw = _exact_object(value, {"binding", "rows"}, "successor checkpoint")
        parsed = parse_successor_binding(raw["binding"])
        if parsed != self.binding:
            raise SuccessorError("successor checkpoint binding changed")
        raw_rows = raw["rows"]
        if not isinstance(raw_rows, list):
            raise SuccessorError("malformed successor checkpoint rows")
        try:
            rows = tuple(_paired_row(row) for row in raw_rows)
        except CheckpointError as error:
            raise SuccessorError(f"malformed successor row: {error}") from error
        self._validate_rows(rows)
        checkpoint = SuccessorCheckpoint(parsed, rows)
        if text != _checkpoint_json(checkpoint):
            raise SuccessorError("successor checkpoint serialization is not canonical")
        return checkpoint

    def read_progress(self, checkpoint: SuccessorCheckpoint) -> ProgressMarker | None:
        """Validate this round's own marker. A stale or inherited marker never wins."""

        if not self.progress_path.exists():
            return None
        marker = _read_marker(self.progress_path, "successor progress marker")
        if marker.binding_hash != successor_binding_hash(self.binding):
            raise SuccessorError("successor progress marker binding changed")
        if marker.ordinal > len(checkpoint.rows):
            raise SuccessorError("successor progress marker is ahead of the checkpoint")
        if marker.ordinal < self.binding.first_new_ordinal:
            raise SuccessorError("successor progress marker is inside the carried prefix")
        if marker.previous_row_hash != checkpoint.rows[marker.ordinal - 1].row_hash:
            raise SuccessorError("successor progress marker chain changed")
        if marker.ordinal < len(checkpoint.rows):
            self.progress_remover(self.progress_path)
            return None
        if marker.ordinal >= len(self.directions):
            raise SuccessorError("successor progress marker is beyond the final direction")
        return marker

    def write_progress(self, ordinal: int, stage: ProgressStage) -> ProgressMarker:
        checkpoint = self.load()
        if ordinal != len(checkpoint.rows) or ordinal >= len(self.directions):
            raise SuccessorError("progress ordinal is not the first incomplete direction")
        marker = ProgressMarker(
            schema_version=SCHEMA_VERSION,
            binding_hash=successor_binding_hash(self.binding),
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
    ) -> SuccessorCheckpoint:
        checkpoint = self.load()
        ordinal = len(checkpoint.rows)
        if ordinal >= len(self.directions) or direction != self.directions[ordinal]:
            raise SuccessorError("paired row is not the first incomplete direction")
        if ordinal < self.binding.first_new_ordinal:
            raise SuccessorError("a carried ordinal may never be appended")
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
        updated = SuccessorCheckpoint(self.binding, (*checkpoint.rows, row))
        _atomic_write(self.checkpoint_path, _checkpoint_json(updated))
        self.progress_remover(self.progress_path)
        return updated


def _parse_ancestry(value: object, label: str) -> dict[str, Any]:
    fields = {
        "role",
        "experiment_id",
        "checkpoint_path",
        "progress_path",
        "checkpoint_sha256",
        "progress_sha256",
        "binding_hash",
        "last_row_hash",
        "row_count",
        "resume_ordinal",
        "resume_stage",
    }
    raw = _exact_object(value, fields, label)
    return {
        "role": _string(raw["role"], f"{label}.role"),
        "experiment_id": _string(raw["experiment_id"], f"{label}.experiment_id"),
        "checkpoint_path": _string(raw["checkpoint_path"], f"{label}.checkpoint_path"),
        "progress_path": _string(raw["progress_path"], f"{label}.progress_path"),
        "checkpoint_sha256": _digest(raw["checkpoint_sha256"], f"{label}.checkpoint_sha256"),
        "progress_sha256": _digest(raw["progress_sha256"], f"{label}.progress_sha256"),
        "binding_hash": _digest(raw["binding_hash"], f"{label}.binding_hash"),
        "last_row_hash": _digest(raw["last_row_hash"], f"{label}.last_row_hash"),
        "row_count": _integer(raw["row_count"], f"{label}.row_count"),
        "resume_ordinal": _integer(raw["resume_ordinal"], f"{label}.resume_ordinal"),
        "resume_stage": _string(raw["resume_stage"], f"{label}.resume_stage"),
    }


def parse_successor_binding(value: object) -> SuccessorBinding:
    """Parse one successor binding block, refusing every malformed field."""

    fields = {field.name for field in SuccessorBinding.__dataclass_fields__.values()}
    raw = _exact_object(value, fields, "successor binding")
    source = raw["frozen_source_sha256"]
    if not isinstance(source, list):
        raise SuccessorError("malformed successor binding frozen_source_sha256")
    frozen: list[tuple[str, str]] = []
    for index, row in enumerate(source):
        if not isinstance(row, list) or len(row) != 2:
            raise SuccessorError(f"malformed frozen_source_sha256[{index}]")
        frozen.append(
            (
                _string(row[0], f"frozen_source_sha256[{index}].path"),
                _digest(row[1], f"frozen_source_sha256[{index}].hash"),
            )
        )
    return SuccessorBinding(
        schema_version=_integer(raw["schema_version"], "binding.schema_version"),
        experiment_id=_string(raw["experiment_id"], "binding.experiment_id"),
        hypothesis_id=_string(raw["hypothesis_id"], "binding.hypothesis_id"),
        session_id=_string(raw["session_id"], "binding.session_id"),
        experiment_record_path=_string(
            raw["experiment_record_path"], "binding.experiment_record_path"
        ),
        immediate_parent=ImmediateParent(
            **_parse_ancestry(raw["immediate_parent"], "binding.immediate_parent")
        ),
        chain_genesis=ChainGenesis(
            **_parse_ancestry(raw["chain_genesis"], "binding.chain_genesis")
        ),
        package_manifest_sha256=_digest(
            raw["package_manifest_sha256"], "binding.package_manifest_sha256"
        ),
        frozen_source_sha256=tuple(frozen),
        resume_driver_sha256=_digest(
            raw["resume_driver_sha256"], "binding.resume_driver_sha256"
        ),
        child_driver_sha256=_digest(raw["child_driver_sha256"], "binding.child_driver_sha256"),
        successor_driver_sha256=_digest(
            raw["successor_driver_sha256"], "binding.successor_driver_sha256"
        ),
        retained_sha256=_digest(raw["retained_sha256"], "binding.retained_sha256"),
        clean_room_sha256=_digest(raw["clean_room_sha256"], "binding.clean_room_sha256"),
        fixture_hash=_digest(raw["fixture_hash"], "binding.fixture_hash"),
        direction_count=_integer(raw["direction_count"], "binding.direction_count"),
        direction_hash=_digest(raw["direction_hash"], "binding.direction_hash"),
        first_new_ordinal=_integer(raw["first_new_ordinal"], "binding.first_new_ordinal"),
        result_path=_string(raw["result_path"], "binding.result_path"),
        checkpoint_path=_string(raw["checkpoint_path"], "binding.checkpoint_path"),
        progress_path=_string(raw["progress_path"], "binding.progress_path"),
    )


class SuccessorChainDriver:
    """Continue the carried chain one direction at a time, committing complete pairs."""

    def __init__(
        self,
        store: SuccessorCheckpointStore,
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
    ) -> SuccessorCheckpoint:
        actual = fixture_binding_hash(
            atoms=atoms,
            directions=self.store.directions,
            outer_side=outer_side,
            square_side=square_side,
        )
        if actual != self.store.binding.fixture_hash:
            raise SuccessorError("fixture binding changed")
        checkpoint = self.store.open_chain()
        if len(checkpoint.rows) < self.store.binding.first_new_ordinal:
            raise SuccessorError("the carried prefix is short of the first new ordinal")
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
                raise SuccessorDisagreementStopError(
                    f"exact disagreement retained at ordinal {ordinal}"
                )
        return checkpoint


def chain_status(checkpoint_path: Path) -> dict[str, object]:
    """Report the observable chain state without loading the retained fixture."""

    try:
        text = checkpoint_path.read_text(encoding="utf-8")
        value = json.loads(text)
    except (OSError, json.JSONDecodeError) as error:
        raise SuccessorError("successor checkpoint is unreadable") from error
    raw = _exact_object(value, {"binding", "rows"}, "successor checkpoint")
    binding = parse_successor_binding(raw["binding"])
    raw_rows = raw["rows"]
    if not isinstance(raw_rows, list) or not raw_rows:
        raise SuccessorError("successor checkpoint has no rows")
    try:
        rows = tuple(_paired_row(row) for row in raw_rows)
    except CheckpointError as error:
        raise SuccessorError(f"malformed successor row: {error}") from error
    previous = binding.chain_genesis.binding_hash
    first_disagreement: int | None = None
    for ordinal, row in enumerate(rows):
        if row.ordinal != ordinal or row.previous_row_hash != previous:
            raise SuccessorError("successor chain is not contiguous")
        if row.agreement != (row.source == row.independent):
            raise SuccessorError("successor agreement flag changed")
        if row.row_hash != _row_hash(
            ordinal=row.ordinal,
            direction=row.direction,
            source=row.source,
            independent=row.independent,
            agreement=row.agreement,
            previous_row_hash=row.previous_row_hash,
        ):
            raise SuccessorError("successor row hash changed")
        if not row.agreement and first_disagreement is None:
            first_disagreement = ordinal
        previous = row.row_hash
    progress_path = Path(binding.progress_path)
    progress: dict[str, object] | None = None
    if progress_path.is_file():
        marker = _read_marker(progress_path, "successor progress marker")
        progress = {"ordinal": marker.ordinal, "stage": marker.stage}
    return {
        "schema_version": 1,
        "status": f"{binding.experiment_id}-successor-chain",
        "checkpoint_path": checkpoint_path.as_posix(),
        "checkpoint_sha256": _sha256(checkpoint_path),
        "chain_verified": True,
        "immediate_parent_experiment_id": binding.immediate_parent.experiment_id,
        "chain_genesis_experiment_id": binding.chain_genesis.experiment_id,
        "carried_row_count": binding.immediate_parent.row_count,
        "first_new_ordinal": binding.first_new_ordinal,
        "row_count": len(rows),
        "new_row_count": len(rows) - binding.first_new_ordinal,
        "last_ordinal": rows[-1].ordinal,
        "last_row_hash": rows[-1].row_hash,
        "direction_count": binding.direction_count,
        "complete": len(rows) == binding.direction_count,
        "all_agree": first_disagreement is None,
        "first_disagreement_ordinal": first_disagreement,
        "progress": progress,
    }


# --- Terminal schemas ---------------------------------------------------------------
#
# Two, and only two, shapes may be published.  Both carry the shrink-and-scaling
# preconditions, every frozen mutation result, ``all_mutations_rejected`` and
# ``instrument_valid``; in both, the decision is derived from those emitted fields by
# :func:`derive_decision` rather than asserted beside them.

_COMMON_REQUIRED = frozenset(
    {
        "schema_version",
        "experiment_id",
        "hypothesis_id",
        "session_id",
        "terminal_schema",
        "binding",
        "binding_hash",
        "ancestry",
        "fixture",
        "frozen_expectations",
        "preconditions",
        "preconditions_pass",
        "shrink_and_scaling",
        "mutation_guards",
        "all_mutations_rejected",
        "frozen_invariants",
        "frozen_invariants_pass",
        "instrument_valid",
        "decision",
        "absences",
        "claim_boundary",
        "chain_spine",
        "row_count",
        "first_new_ordinal",
        "carried_boundary",
        "last_row_hash",
        "checkpoint_sha256",
    }
)
_AGREEMENT_ONLY = frozenset(
    {
        "source_faithful",
        "independent",
        "row_minimums",
        "global_minimum",
        "exact_manifest_agreement",
        "first_disagreement",
    }
)
_DISAGREEMENT_ONLY = frozenset({"verified_prefix", "discrepant_pair", "first_disagreement"})
AGREEMENT_REQUIRED = _COMMON_REQUIRED | _AGREEMENT_ONLY
DISAGREEMENT_REQUIRED = _COMMON_REQUIRED | _DISAGREEMENT_ONLY
# A disagreement result must not merely omit these: it must declare each one absent.
DISAGREEMENT_ABSENCES = frozenset(
    {
        "suffix_rows",
        "source_faithful_certificate_manifest",
        "independent_certificate_manifest",
        "row_minimums",
        "global_minimum",
        "exact_manifest_agreement",
    }
)
DISAGREEMENT_FORBIDDEN = frozenset(DISAGREEMENT_ABSENCES - {"suffix_rows"}) | frozenset(
    {"source_faithful", "independent"}
)
FROZEN_MUTATIONS = frozenset(
    {
        "atom_mutation_rejected",
        "weight_mutation_rejected",
        "direction_cell_mutation_rejected",
        "event_boundary_mutation_rejected",
        "scaling_mutation_rejected",
    }
)


def shrink_and_scaling_block(
    *,
    outer_side: Fraction,
    internal_side: Fraction,
    shrink_margin: Fraction,
    containment_left_operand: Fraction,
) -> dict[str, object]:
    """Return the exact shrink-and-scaling preconditions and their conjunction."""

    outer_positive, parts_positive, exact = scaling_preconditions(
        outer_side=outer_side, internal_side=internal_side, shrink_margin=shrink_margin
    )
    containment_strict = containment_left_operand < 1
    return {
        "outer_side": outer_side,
        "internal_side": internal_side,
        "shrink_margin": shrink_margin,
        "outer_side_positive": outer_positive,
        "internal_side_and_margin_positive": parts_positive,
        "exact_side_decomposition": exact,
        "containment_left_operand": containment_left_operand,
        "containment_strict": containment_strict,
        "all_hold": bool(outer_positive and parts_positive and exact and containment_strict),
    }


def production_evidence(
    fixture: RetainedFixture, atoms: tuple[Atom, ...]
) -> InstrumentEvidence:
    """Compute the only instrument evidence the production writer may publish."""

    preconditions, _ = _preconditions(fixture)
    left = preconditions["containment_left_operand"]
    if not isinstance(left, Fraction):
        raise SuccessorError("containment operand is not exact")
    return InstrumentEvidence(
        preconditions=preconditions,
        shrink_and_scaling=shrink_and_scaling_block(
            outer_side=fixture.outer_side,
            internal_side=fixture.outer_side - fixture.shrink_margin,
            shrink_margin=fixture.shrink_margin,
            containment_left_operand=left,
        ),
        mutation_guards=_mutation_guards(fixture, atoms),
        expectations=PRODUCTION_EXPECTATIONS,
    )


def _bool_sequence(value: object, label: str) -> list[bool]:
    if not isinstance(value, list) or not value:
        raise SuccessorError(f"malformed {label}")
    for item in value:
        if not isinstance(item, bool):
            raise SuccessorError(f"malformed {label}")
    return list(value)


def derive_preconditions_pass(preconditions: Mapping[str, object]) -> bool:
    """Re-derive the precondition conjunction from the emitted precondition fields."""

    unit = _bool_sequence(preconditions.get("direction_unit"), "preconditions.direction_unit")
    gaps = _bool_sequence(
        preconditions.get("adjacent_half_gap_bounds"),
        "preconditions.adjacent_half_gap_bounds",
    )
    decomposition = _bool_sequence(
        preconditions.get("side_decomposition"), "preconditions.side_decomposition"
    )
    brackets = _bool(
        preconditions.get("final_pair_brackets_quarter_turn"),
        "preconditions.final_pair_brackets_quarter_turn",
    )
    strict = _bool(preconditions.get("containment_strict"), "preconditions.containment_strict")
    return all(unit) and brackets and all(gaps) and strict and all(decomposition)


def derive_shrink_and_scaling_pass(block: Mapping[str, object]) -> bool:
    """Re-derive the shrink-and-scaling conjunction from its own emitted operands."""

    return (
        _bool(block.get("outer_side_positive"), "shrink_and_scaling.outer_side_positive")
        and _bool(
            block.get("internal_side_and_margin_positive"),
            "shrink_and_scaling.internal_side_and_margin_positive",
        )
        and _bool(
            block.get("exact_side_decomposition"),
            "shrink_and_scaling.exact_side_decomposition",
        )
        and _bool(block.get("containment_strict"), "shrink_and_scaling.containment_strict")
    )


def derive_instrument_valid(record: Mapping[str, object]) -> bool:
    """Re-derive instrument validity from the four emitted evidence conjunctions."""

    shrink = record.get("shrink_and_scaling")
    if not isinstance(shrink, dict):
        raise SuccessorError("missing shrink_and_scaling block")
    return (
        _bool(record.get("preconditions_pass"), "preconditions_pass")
        and _bool(shrink.get("all_hold"), "shrink_and_scaling.all_hold")
        and _bool(record.get("all_mutations_rejected"), "all_mutations_rejected")
        and _bool(record.get("frozen_invariants_pass"), "frozen_invariants_pass")
    )


def derive_decision(record: Mapping[str, object]) -> str:
    """Derive the scientific decision from the emitted instrument and agreement fields."""

    if not _bool(record.get("instrument_valid"), "instrument_valid"):
        return "unresolved-invalid-instrument"
    schema = record.get("terminal_schema")
    if schema == TERMINAL_COMPLETE_AGREEMENT:
        agreement = _bool(record.get("exact_manifest_agreement"), "exact_manifest_agreement")
        if agreement and record.get("first_disagreement") is None:
            return "accepted"
        raise SuccessorError("a complete-agreement result cannot carry a disagreement")
    if schema == TERMINAL_EARLY_DISAGREEMENT:
        first = record.get("first_disagreement")
        if isinstance(first, dict) and first:
            return "rejected"
        raise SuccessorError("an early-disagreement result requires a first disagreement")
    raise SuccessorError(f"unknown terminal schema: {schema!r}")


def _fraction_text(value: Fraction) -> str:
    """Render a Fraction exactly as :func:`canonical_json` does, denominator included."""

    return f"{value.numerator}/{value.denominator}"


def _rebuild_direction(manifest: DirectionManifest) -> Direction:
    ux, uy, vx, vy = manifest.direction
    return Direction(manifest.label, ux, uy, vx, vy)


def _parse_summary(value: object, label: str) -> CertificateManifest:
    fields = {
        "atom_count",
        "atom_hash",
        "total_weight",
        "direction_count",
        "direction_hash",
        "rows",
        "global_minimum",
    }
    raw = _exact_object(value, fields, label)
    rows = raw["rows"]
    if not isinstance(rows, list) or not rows:
        raise SuccessorError(f"malformed {label}.rows")
    try:
        manifests = tuple(
            _manifest(row, f"{label}.rows[{index}]") for index, row in enumerate(rows)
        )
        summary = CertificateManifest(
            atom_count=_integer(raw["atom_count"], f"{label}.atom_count"),
            atom_hash=_digest(raw["atom_hash"], f"{label}.atom_hash"),
            total_weight=_fraction(raw["total_weight"], f"{label}.total_weight"),
            direction_count=_integer(raw["direction_count"], f"{label}.direction_count"),
            direction_hash=_digest(raw["direction_hash"], f"{label}.direction_hash"),
            rows=manifests,
            global_minimum=_fraction(raw["global_minimum"], f"{label}.global_minimum"),
        )
    except CheckpointError as error:
        raise SuccessorError(f"malformed {label}: {error}") from error
    if canonical_json(summary) != canonical_json(value):
        raise SuccessorError(f"{label} serialization is not canonical")
    return summary


def _spine_entry(
    *, ordinal: int, label: str, agreement: bool, previous_row_hash: str, row_hash: str
) -> dict[str, object]:
    return {
        "ordinal": ordinal,
        "direction_label": label,
        "agreement": agreement,
        "previous_row_hash": previous_row_hash,
        "row_hash": row_hash,
    }


def _spine_from_rows(rows: tuple[PairedRow, ...]) -> list[dict[str, object]]:
    return [
        _spine_entry(
            ordinal=row.ordinal,
            label=row.direction.label,
            agreement=row.agreement,
            previous_row_hash=row.previous_row_hash,
            row_hash=row.row_hash,
        )
        for row in rows
    ]


def _spine_from_summaries(
    source: CertificateManifest, independent: CertificateManifest, anchor: str
) -> list[dict[str, object]]:
    """Rebuild the whole hash chain from the two summaries alone."""

    previous = anchor
    spine: list[dict[str, object]] = []
    for ordinal, (source_row, independent_row) in enumerate(
        zip(source.rows, independent.rows, strict=True)
    ):
        direction = _rebuild_direction(source_row)
        if _rebuild_direction(independent_row) != direction:
            raise SuccessorError(f"summary rows disagree on direction {ordinal}")
        agreement = source_row == independent_row
        digest = _row_hash(
            ordinal=ordinal,
            direction=direction,
            source=source_row,
            independent=independent_row,
            agreement=agreement,
            previous_row_hash=previous,
        )
        spine.append(
            _spine_entry(
                ordinal=ordinal,
                label=direction.label,
                agreement=agreement,
                previous_row_hash=previous,
                row_hash=digest,
            )
        )
        previous = digest
    return spine


def _check_spine_contiguity(spine: object, anchor: str, label: str) -> list[dict[str, Any]]:
    if not isinstance(spine, list) or not spine:
        raise SuccessorError(f"malformed {label}")
    previous = anchor
    entries: list[dict[str, Any]] = []
    for ordinal, entry in enumerate(spine):
        parsed = _exact_object(
            entry,
            {"ordinal", "direction_label", "agreement", "previous_row_hash", "row_hash"},
            f"{label}[{ordinal}]",
        )
        if _integer(parsed["ordinal"], f"{label}[{ordinal}].ordinal") != ordinal:
            raise SuccessorError(f"{label} ordinals are not contiguous")
        _bool(parsed["agreement"], f"{label}[{ordinal}].agreement")
        if _digest(parsed["previous_row_hash"], f"{label}[{ordinal}].previous") != previous:
            raise SuccessorError(f"{label} hash chain is broken at {ordinal}")
        previous = _digest(parsed["row_hash"], f"{label}[{ordinal}].row_hash")
        entries.append(parsed)
    return entries


def _check_absences(record: Mapping[str, object], schema: str) -> None:
    absences = record.get("absences")
    if not isinstance(absences, dict):
        raise SuccessorError("missing absences block")
    if schema == TERMINAL_COMPLETE_AGREEMENT:
        if absences:
            raise SuccessorError("a complete-agreement result declares no absence")
        return
    if set(absences) != set(DISAGREEMENT_ABSENCES):
        raise SuccessorError("an early-disagreement result must declare every required absence")
    for name, declared in absences.items():
        if not isinstance(declared, dict):
            raise SuccessorError(f"malformed absence {name}")
        if declared.get("absent") is not True:
            raise SuccessorError(f"absence {name} does not declare itself absent")
        reason = declared.get("reason")
        if not isinstance(reason, str) or not reason:
            raise SuccessorError(f"absence {name} carries no reason")
        if name in record:
            raise SuccessorError(f"absence {name} is declared but the field is present")
    for forbidden in DISAGREEMENT_FORBIDDEN:
        if forbidden in record:
            raise SuccessorError(f"an early-disagreement result may not carry {forbidden}")


def _check_ancestry(record: Mapping[str, object], binding: SuccessorBinding) -> None:
    ancestry = record.get("ancestry")
    if not isinstance(ancestry, dict) or set(ancestry) != {
        "immediate_parent",
        "chain_genesis",
        "roles_distinct",
        "genesis_is_prefix_of_immediate_parent",
    }:
        raise SuccessorError("malformed ancestry block")
    parent = ancestry["immediate_parent"]
    genesis = ancestry["chain_genesis"]
    for block, expected, role in (
        (parent, binding.immediate_parent, IMMEDIATE_PARENT_ROLE),
        (genesis, binding.chain_genesis, CHAIN_GENESIS_ROLE),
    ):
        if not isinstance(block, dict):
            raise SuccessorError("malformed ancestry entry")
        if block.get("verified") is not True:
            raise SuccessorError(f"ancestry {role} is not marked verified")
        echoed = {key: value for key, value in block.items() if key != "verified"}
        if canonical_json(echoed) != canonical_json(expected):
            raise SuccessorError(f"ancestry {role} does not echo its binding block")
        if block.get("role") != role:
            raise SuccessorError(f"ancestry entry does not carry the {role} role")
    if ancestry.get("roles_distinct") is not True:
        raise SuccessorError("ancestry roles are not marked distinct")
    if ancestry.get("genesis_is_prefix_of_immediate_parent") is not True:
        raise SuccessorError("the genesis is not marked a prefix of the immediate parent")
    if binding.immediate_parent.experiment_id == binding.chain_genesis.experiment_id:
        raise SuccessorError("both ancestry blocks name the same experiment")
    if binding.chain_genesis.row_count >= binding.immediate_parent.row_count:
        raise SuccessorError("the chain genesis is not a proper prefix of its parent")


def _summary_invariants(
    summary: CertificateManifest, expectations: FrozenExpectations, prefix: str
) -> dict[str, bool]:
    return {
        f"{prefix}_atom_count": summary.atom_count == expectations.atom_count,
        f"{prefix}_direction_count": summary.direction_count == expectations.direction_count,
        f"{prefix}_row_count": len(summary.rows) == expectations.direction_count,
        f"{prefix}_total_weight": summary.total_weight == expectations.total_weight,
        f"{prefix}_global_minimum": summary.global_minimum == expectations.global_minimum,
        f"{prefix}_global_minimum_is_row_minimum": summary.global_minimum
        == min(row.minimum for row in summary.rows),
    }


def _parse_expectations(value: object) -> FrozenExpectations:
    raw = _exact_object(
        value,
        {"atom_count", "direction_count", "total_weight", "global_minimum"},
        "frozen_expectations",
    )
    try:
        return FrozenExpectations(
            atom_count=_integer(raw["atom_count"], "frozen_expectations.atom_count"),
            direction_count=_integer(
                raw["direction_count"], "frozen_expectations.direction_count"
            ),
            total_weight=_fraction(raw["total_weight"], "frozen_expectations.total_weight"),
            global_minimum=_fraction(
                raw["global_minimum"], "frozen_expectations.global_minimum"
            ),
        )
    except CheckpointError as error:
        raise SuccessorError(f"malformed frozen_expectations: {error}") from error


def _validate_agreement_body(
    record: Mapping[str, object], binding: SuccessorBinding, expectations: FrozenExpectations
) -> dict[str, bool]:
    source = _parse_summary(record["source_faithful"], "source_faithful")
    independent = _parse_summary(record["independent"], "independent")
    if len(source.rows) != expectations.direction_count:
        raise SuccessorError("the source summary is not a complete 181-row manifest")
    if len(independent.rows) != expectations.direction_count:
        raise SuccessorError("the independent summary is not a complete 181-row manifest")
    agreement = source == independent
    if _bool(record.get("exact_manifest_agreement"), "exact_manifest_agreement") != agreement:
        raise SuccessorError("exact_manifest_agreement contradicts the two summaries")
    if agreement != (record.get("first_disagreement") is None):
        raise SuccessorError("first_disagreement contradicts exact_manifest_agreement")
    minimums = record.get("row_minimums")
    if not isinstance(minimums, dict) or set(minimums) != {"source_faithful", "independent"}:
        raise SuccessorError("malformed row_minimums block")
    for name, summary in (("source_faithful", source), ("independent", independent)):
        emitted = minimums[name]
        expected = [_fraction_text(row.minimum) for row in summary.rows]
        if not isinstance(emitted, list) or emitted != expected:
            raise SuccessorError(f"row_minimums.{name} does not reproduce every row minimum")
    globals_block = record.get("global_minimum")
    if not isinstance(globals_block, dict) or set(globals_block) != {
        "source_faithful",
        "independent",
        "frozen_expected",
        "agrees",
    }:
        raise SuccessorError("malformed global_minimum block")
    if globals_block["source_faithful"] != _fraction_text(source.global_minimum):
        raise SuccessorError("global_minimum does not echo the source summary")
    if globals_block["independent"] != _fraction_text(independent.global_minimum):
        raise SuccessorError("global_minimum does not echo the independent summary")
    if globals_block["frozen_expected"] != _fraction_text(expectations.global_minimum):
        raise SuccessorError("global_minimum does not echo the frozen expectation")
    if globals_block["agrees"] is not (source.global_minimum == independent.global_minimum):
        raise SuccessorError("the global-minimum agreement flag is not derived")
    spine = _spine_from_summaries(source, independent, binding.chain_genesis.binding_hash)
    if canonical_json(record["chain_spine"]) != canonical_json(spine):
        raise SuccessorError("the chain spine is not reproduced by the two summaries")
    if record.get("row_count") != len(spine):
        raise SuccessorError("row_count does not match the chain spine")
    if record.get("last_row_hash") != spine[-1]["row_hash"]:
        raise SuccessorError("last_row_hash does not match the chain spine")
    return {
        **_summary_invariants(source, expectations, "source"),
        **_summary_invariants(independent, expectations, "independent"),
    }


def _validate_disagreement_body(
    record: Mapping[str, object], binding: SuccessorBinding
) -> None:
    prefix = record.get("verified_prefix")
    if not isinstance(prefix, dict) or set(prefix) != {
        "row_count",
        "first_new_ordinal",
        "chain_verified",
        "genesis_anchor_hash",
        "carried_last_row_hash",
        "last_row_hash",
    }:
        raise SuccessorError("malformed verified_prefix block")
    if prefix.get("chain_verified") is not True:
        raise SuccessorError("the verified prefix is not marked verified")
    if prefix.get("genesis_anchor_hash") != binding.chain_genesis.binding_hash:
        raise SuccessorError("the verified prefix is not anchored at the genesis")
    if prefix.get("carried_last_row_hash") != binding.immediate_parent.last_row_hash:
        raise SuccessorError("the verified prefix does not carry the parent boundary")
    pair = record.get("discrepant_pair")
    fields = {
        "ordinal",
        "direction_label",
        "direction",
        "source",
        "independent",
        "agreement",
        "previous_row_hash",
        "row_hash",
        "differing_fields",
    }
    raw = _exact_object(pair, fields, "discrepant_pair")
    if raw["agreement"] is not False:
        raise SuccessorError("the discrepant pair does not record a disagreement")
    try:
        source = _manifest(raw["source"], "discrepant_pair.source")
        independent = _manifest(raw["independent"], "discrepant_pair.independent")
    except CheckpointError as error:
        raise SuccessorError(f"malformed discrepant pair: {error}") from error
    if source == independent:
        raise SuccessorError("the discrepant pair's two manifests are equal")
    direction = _rebuild_direction(source)
    ordinal = _integer(raw["ordinal"], "discrepant_pair.ordinal")
    digest = _row_hash(
        ordinal=ordinal,
        direction=direction,
        source=source,
        independent=independent,
        agreement=False,
        previous_row_hash=_digest(raw["previous_row_hash"], "discrepant_pair.previous"),
    )
    if digest != raw["row_hash"]:
        raise SuccessorError("the discrepant pair's row hash is not reproduced")
    differing = [
        name
        for name in DirectionManifest.__dataclass_fields__
        if getattr(source, name) != getattr(independent, name)
    ]
    if raw["differing_fields"] != differing:
        raise SuccessorError("the discrepant pair does not name its differing fields")
    spine = _check_spine_contiguity(
        record["chain_spine"], binding.chain_genesis.binding_hash, "chain_spine"
    )
    if len(spine) != prefix["row_count"] or spine[-1]["ordinal"] != ordinal:
        raise SuccessorError("the chain spine does not end at the discrepant pair")
    if spine[-1]["row_hash"] != raw["row_hash"]:
        raise SuccessorError("the chain spine does not carry the discrepant row hash")
    if any(entry["agreement"] is False for entry in spine[:-1]):
        raise SuccessorError("the verified prefix is not contiguously agreeing")
    first = record.get("first_disagreement")
    if not isinstance(first, dict) or set(first) != {
        "ordinal",
        "direction_label",
        "source_minimum",
        "independent_minimum",
        "differing_fields",
    }:
        raise SuccessorError("malformed first_disagreement block")
    if first["ordinal"] != ordinal or first["differing_fields"] != differing:
        raise SuccessorError("first_disagreement contradicts the discrepant pair")
    if first["source_minimum"] != _fraction_text(source.minimum):
        raise SuccessorError("first_disagreement does not echo the source minimum")
    if first["independent_minimum"] != _fraction_text(independent.minimum):
        raise SuccessorError("first_disagreement does not echo the independent minimum")


def validate_result(record: Mapping[str, object]) -> dict[str, object]:
    """Re-derive every decision-bearing field of a canonical successor result.

    This is the whole admission boundary in one function, and it reads nothing but the
    record.  An independent reviewer runs it against the published bytes.
    """

    schema = record.get("terminal_schema")
    if schema == TERMINAL_COMPLETE_AGREEMENT:
        required = AGREEMENT_REQUIRED
    elif schema == TERMINAL_EARLY_DISAGREEMENT:
        required = DISAGREEMENT_REQUIRED
    else:
        raise SuccessorError(f"unknown terminal schema: {schema!r}")
    if set(record) != set(required):
        missing = sorted(set(required) - set(record))
        extra = sorted(set(record) - set(required))
        raise SuccessorError(f"result key set is wrong: missing {missing}, extra {extra}")
    if record.get("hypothesis_id") != HYPOTHESIS_ID:
        raise SuccessorError("result is not bound to H-052")
    binding = parse_successor_binding(record["binding"])
    if record.get("binding_hash") != successor_binding_hash(binding):
        raise SuccessorError("binding hash does not match the binding block")
    if record.get("experiment_id") != binding.experiment_id:
        raise SuccessorError("result experiment id does not match its binding")
    if record.get("session_id") != binding.session_id:
        raise SuccessorError("result session id does not match its binding")
    if record.get("first_new_ordinal") != binding.first_new_ordinal:
        raise SuccessorError("first_new_ordinal does not match its binding")
    _check_ancestry(record, binding)
    _check_absences(record, str(schema))
    carried = record.get("carried_boundary")
    if not isinstance(carried, dict) or set(carried) != {"ordinal", "row_hash"}:
        raise SuccessorError("malformed carried_boundary block")
    if carried["ordinal"] != binding.first_new_ordinal - 1:
        raise SuccessorError("carried_boundary is not the last carried ordinal")
    if carried["row_hash"] != binding.immediate_parent.last_row_hash:
        raise SuccessorError("carried_boundary is not the immediate parent's last row")
    expectations = _parse_expectations(record["frozen_expectations"])
    preconditions = record.get("preconditions")
    if not isinstance(preconditions, dict):
        raise SuccessorError("missing preconditions block")
    if derive_preconditions_pass(preconditions) != record.get("preconditions_pass"):
        raise SuccessorError("preconditions_pass is asserted, not derived")
    shrink = record.get("shrink_and_scaling")
    if not isinstance(shrink, dict):
        raise SuccessorError("missing shrink_and_scaling block")
    if derive_shrink_and_scaling_pass(shrink) != shrink.get("all_hold"):
        raise SuccessorError("shrink_and_scaling.all_hold is asserted, not derived")
    mutations = record.get("mutation_guards")
    if not isinstance(mutations, dict) or not mutations:
        raise SuccessorError("missing mutation_guards block")
    for name, outcome in mutations.items():
        _bool(outcome, f"mutation_guards.{name}")
    if all(mutations.values()) != record.get("all_mutations_rejected"):
        raise SuccessorError("all_mutations_rejected is asserted, not derived")
    invariants = record.get("frozen_invariants")
    if not isinstance(invariants, dict) or not invariants:
        raise SuccessorError("missing frozen_invariants block")
    for name, outcome in invariants.items():
        _bool(outcome, f"frozen_invariants.{name}")
    if schema == TERMINAL_COMPLETE_AGREEMENT:
        recomputed = _validate_agreement_body(record, binding, expectations)
    else:
        _validate_disagreement_body(record, binding)
        recomputed = _fixture_invariants(record["fixture"], expectations)
    if recomputed != invariants:
        raise SuccessorError("frozen_invariants are asserted, not derived")
    if all(invariants.values()) != record.get("frozen_invariants_pass"):
        raise SuccessorError("frozen_invariants_pass is asserted, not derived")
    if derive_instrument_valid(record) != record.get("instrument_valid"):
        raise SuccessorError("instrument_valid is asserted, not derived")
    if derive_decision(record) != record.get("decision"):
        raise SuccessorError("the decision is asserted, not derived")
    return dict(record)


def _fixture_invariants(
    fixture_block: object, expectations: FrozenExpectations
) -> dict[str, bool]:
    """Re-derive the fixture-level frozen invariants from the emitted fixture block."""

    if not isinstance(fixture_block, dict):
        raise SuccessorError("missing fixture block")
    return {
        "fixture_atom_count": fixture_block.get("atom_count") == expectations.atom_count,
        "fixture_direction_count": fixture_block.get("direction_count")
        == expectations.direction_count,
        "fixture_total_weight": fixture_block.get("total_weight")
        == _fraction_text(expectations.total_weight),
    }


def _ancestry_block(binding: SuccessorBinding) -> dict[str, object]:
    return {
        "immediate_parent": {"verified": True, **_as_mapping(binding.immediate_parent)},
        "chain_genesis": {"verified": True, **_as_mapping(binding.chain_genesis)},
        "roles_distinct": binding.immediate_parent.role != binding.chain_genesis.role,
        "genesis_is_prefix_of_immediate_parent": (
            binding.chain_genesis.row_count < binding.immediate_parent.row_count
        ),
    }


def _as_mapping(block: ImmediateParent | ChainGenesis) -> dict[str, object]:
    return {field: getattr(block, field) for field in block.__dataclass_fields__}


def _base_envelope(
    checkpoint: SuccessorCheckpoint,
    evidence: InstrumentEvidence,
    *,
    terminal_schema: str,
    fixture_block: Mapping[str, object],
    checkpoint_sha256: str,
) -> dict[str, object]:
    binding = checkpoint.binding
    rows = checkpoint.rows
    return {
        "schema_version": 1,
        "experiment_id": binding.experiment_id,
        "hypothesis_id": binding.hypothesis_id,
        "session_id": binding.session_id,
        "terminal_schema": terminal_schema,
        "binding": binding,
        "binding_hash": successor_binding_hash(binding),
        "ancestry": _ancestry_block(binding),
        "fixture": dict(fixture_block),
        "frozen_expectations": evidence.expectations,
        "preconditions": evidence.preconditions,
        "shrink_and_scaling": evidence.shrink_and_scaling,
        "mutation_guards": evidence.mutation_guards,
        "chain_spine": _spine_from_rows(rows),
        "row_count": len(rows),
        "first_new_ordinal": binding.first_new_ordinal,
        "carried_boundary": {
            "ordinal": binding.first_new_ordinal - 1,
            "row_hash": binding.immediate_parent.last_row_hash,
        },
        "last_row_hash": rows[-1].row_hash,
        "checkpoint_sha256": checkpoint_sha256,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def _complete_agreement_body(
    checkpoint: SuccessorCheckpoint,
    evidence: InstrumentEvidence,
    *,
    atoms: tuple[Atom, ...],
    directions: tuple[Direction, ...],
    fixture_block: Mapping[str, object],
    checkpoint_sha256: str,
) -> dict[str, object]:
    rows = checkpoint.rows
    try:
        source = _certificate(atoms, directions, tuple(row.source for row in rows))
        independent = _certificate(atoms, directions, tuple(row.independent for row in rows))
    except CheckpointError as error:
        raise SuccessorError(f"cannot assemble a complete summary: {error}") from error
    envelope = _base_envelope(
        checkpoint,
        evidence,
        terminal_schema=TERMINAL_COMPLETE_AGREEMENT,
        fixture_block=fixture_block,
        checkpoint_sha256=checkpoint_sha256,
    )
    envelope.update(
        {
            "source_faithful": source,
            "independent": independent,
            "row_minimums": {
                "source_faithful": [row.minimum for row in source.rows],
                "independent": [row.minimum for row in independent.rows],
            },
            "global_minimum": {
                "source_faithful": source.global_minimum,
                "independent": independent.global_minimum,
                "frozen_expected": evidence.expectations.global_minimum,
                "agrees": source.global_minimum == independent.global_minimum,
            },
            "exact_manifest_agreement": source == independent,
            "first_disagreement": None,
            "absences": {},
        }
    )
    return envelope


def _early_disagreement_body(
    checkpoint: SuccessorCheckpoint,
    evidence: InstrumentEvidence,
    *,
    directions: tuple[Direction, ...],
    fixture_block: Mapping[str, object],
    checkpoint_sha256: str,
) -> dict[str, object]:
    rows = checkpoint.rows
    row = rows[-1]
    if row.agreement:
        raise SuccessorError("the last row of a disagreement chain must disagree")
    differing = [
        name
        for name in DirectionManifest.__dataclass_fields__
        if getattr(row.source, name) != getattr(row.independent, name)
    ]
    first_absent = row.ordinal + 1
    envelope = _base_envelope(
        checkpoint,
        evidence,
        terminal_schema=TERMINAL_EARLY_DISAGREEMENT,
        fixture_block=fixture_block,
        checkpoint_sha256=checkpoint_sha256,
    )
    envelope.update(
        {
            "verified_prefix": {
                "row_count": len(rows),
                "first_new_ordinal": checkpoint.binding.first_new_ordinal,
                "chain_verified": True,
                "genesis_anchor_hash": checkpoint.binding.chain_genesis.binding_hash,
                "carried_last_row_hash": checkpoint.binding.immediate_parent.last_row_hash,
                "last_row_hash": row.row_hash,
            },
            "discrepant_pair": {
                "ordinal": row.ordinal,
                "direction_label": row.direction.label,
                "direction": row.direction,
                "source": row.source,
                "independent": row.independent,
                "agreement": False,
                "previous_row_hash": row.previous_row_hash,
                "row_hash": row.row_hash,
                "differing_fields": differing,
            },
            "first_disagreement": {
                "ordinal": row.ordinal,
                "direction_label": row.direction.label,
                "source_minimum": row.source.minimum,
                "independent_minimum": row.independent.minimum,
                "differing_fields": differing,
            },
            "absences": {
                "suffix_rows": {
                    "absent": True,
                    "reason": (
                        "the chain stopped at the first exact disagreement, so no "
                        "direction after it was evaluated"
                    ),
                    "first_absent_ordinal": first_absent,
                    "last_absent_ordinal": len(directions) - 1,
                    "absent_count": len(directions) - first_absent,
                },
                "source_faithful_certificate_manifest": {
                    "absent": True,
                    "reason": (
                        "a 181-row CertificateManifest cannot be assembled from a chain "
                        "that stops at the first exact disagreement"
                    ),
                },
                "independent_certificate_manifest": {
                    "absent": True,
                    "reason": (
                        "a 181-row CertificateManifest cannot be assembled from a chain "
                        "that stops at the first exact disagreement"
                    ),
                },
                "row_minimums": {
                    "absent": True,
                    "reason": "row minima are reported only inside a complete summary",
                },
                "global_minimum": {
                    "absent": True,
                    "reason": "a global minimum over 181 directions is undefined here",
                },
                "exact_manifest_agreement": {
                    "absent": True,
                    "reason": (
                        "manifest-level agreement is undetermined without both complete "
                        "summaries; the row-level disagreement is what was measured"
                    ),
                },
            },
        }
    )
    return envelope


def assemble_result(
    checkpoint: SuccessorCheckpoint,
    evidence: InstrumentEvidence,
    *,
    atoms: tuple[Atom, ...],
    directions: tuple[Direction, ...],
    fixture_block: Mapping[str, object],
    checkpoint_sha256: str,
) -> dict[str, object]:
    """Route a terminal chain to its one legal schema and derive its decision."""

    rows = checkpoint.rows
    binding = checkpoint.binding
    if len(rows) <= binding.first_new_ordinal:
        raise SuccessorError("no new row was computed; a carried prefix is not a result")
    disagreeing = [row.ordinal for row in rows if not row.agreement]
    if disagreeing:
        if disagreeing[0] != rows[-1].ordinal:
            raise SuccessorError("the chain continued past its first disagreement")
        body = _early_disagreement_body(
            checkpoint,
            evidence,
            directions=directions,
            fixture_block=fixture_block,
            checkpoint_sha256=checkpoint_sha256,
        )
    elif len(rows) == len(directions):
        body = _complete_agreement_body(
            checkpoint,
            evidence,
            atoms=atoms,
            directions=directions,
            fixture_block=fixture_block,
            checkpoint_sha256=checkpoint_sha256,
        )
    else:
        raise SuccessorError(
            "a time-limited agreeing prefix is process evidence, not a terminal result"
        )
    record: dict[str, Any] = json.loads(canonical_json(body))
    record["preconditions_pass"] = derive_preconditions_pass(record["preconditions"])
    record["all_mutations_rejected"] = all(record["mutation_guards"].values())
    expectations = _parse_expectations(record["frozen_expectations"])
    if record["terminal_schema"] == TERMINAL_COMPLETE_AGREEMENT:
        record["frozen_invariants"] = {
            **_summary_invariants(
                _parse_summary(record["source_faithful"], "source_faithful"),
                expectations,
                "source",
            ),
            **_summary_invariants(
                _parse_summary(record["independent"], "independent"),
                expectations,
                "independent",
            ),
        }
    else:
        record["frozen_invariants"] = _fixture_invariants(record["fixture"], expectations)
    record["frozen_invariants_pass"] = all(record["frozen_invariants"].values())
    record["instrument_valid"] = derive_instrument_valid(record)
    record["decision"] = derive_decision(record)
    if json.loads(canonical_json(record)) != record:
        raise SuccessorError("result canonicalization is not stable")
    return validate_result(record)


IMMEDIATE_PARENT_BINDING_HASH = (
    "18ec64b477068704857dfd9dbfc4eeb92510029aa2530bdba635e99045cf32df"
)


def production_immediate_parent_spec() -> ImmediateParentSpec:
    """The exp-056 boundary, declared before it is read."""

    return ImmediateParentSpec(
        experiment_id=IMMEDIATE_PARENT_ID,
        genesis_experiment_id=CHAIN_GENESIS_ID,
        checkpoint_path=IMMEDIATE_PARENT_CHECKPOINT,
        progress_path=IMMEDIATE_PARENT_PROGRESS,
        result_path=OUTPUT_ROOT / f"{IMMEDIATE_PARENT_SLUG}.json",
        checkpoint_sha256=IMMEDIATE_PARENT_CHECKPOINT_SHA256,
        progress_sha256=IMMEDIATE_PARENT_PROGRESS_SHA256,
        binding_hash=IMMEDIATE_PARENT_BINDING_HASH,
        last_row_hash=IMMEDIATE_PARENT_LAST_ROW_HASH,
        row_count=IMMEDIATE_PARENT_ROW_COUNT,
        genesis_binding_hash=CHAIN_GENESIS_BINDING_HASH,
        genesis_last_row_hash=CHAIN_GENESIS_LAST_ROW_HASH,
        genesis_row_count=CHAIN_GENESIS_ROW_COUNT,
        resume_ordinal=FIRST_NEW_ORDINAL,
        resume_stage=RESUME_STAGE,
    )


def production_chain_genesis_spec() -> ParentSpec:
    """The exp-052 origin, declared before it is read."""

    return ParentSpec(
        experiment_id=CHAIN_GENESIS_ID,
        checkpoint_path=CHAIN_GENESIS_CHECKPOINT,
        progress_path=CHAIN_GENESIS_PROGRESS,
        result_path=CHAIN_GENESIS_RESULT,
        checkpoint_sha256=CHAIN_GENESIS_CHECKPOINT_SHA256,
        progress_sha256=CHAIN_GENESIS_PROGRESS_SHA256,
        binding_hash=CHAIN_GENESIS_BINDING_HASH,
        last_row_hash=CHAIN_GENESIS_LAST_ROW_HASH,
        row_count=CHAIN_GENESIS_ROW_COUNT,
    )


def successor_binding(
    receipt: AncestryReceipt,
    *,
    experiment_id: str,
    session_id: str,
    experiment_record_path: str,
    atoms: tuple[Atom, ...],
    directions: tuple[Direction, ...],
    outer_side: Fraction,
    square_side: Fraction,
    result_path: Path,
    checkpoint_path: Path,
    progress_path: Path,
) -> SuccessorBinding:
    """Build the binding block from two verified ancestries and the frozen fixture."""

    return SuccessorBinding(
        schema_version=SCHEMA_VERSION,
        experiment_id=experiment_id,
        hypothesis_id=HYPOTHESIS_ID,
        session_id=session_id,
        experiment_record_path=experiment_record_path,
        immediate_parent=receipt.immediate_parent,
        chain_genesis=receipt.chain_genesis,
        package_manifest_sha256=FROZEN_PACKAGE_SHA256,
        frozen_source_sha256=FROZEN_SOURCE_SHA256,
        resume_driver_sha256=driver_sha256(),
        child_driver_sha256=child_driver_sha256(),
        successor_driver_sha256=successor_driver_sha256(),
        retained_sha256=RETAINED_SHA256,
        clean_room_sha256=CLEAN_ROOM_SHA256,
        fixture_hash=fixture_binding_hash(
            atoms=atoms,
            directions=directions,
            outer_side=outer_side,
            square_side=square_side,
        ),
        direction_count=len(directions),
        direction_hash=canonical_hash(directions),
        first_new_ordinal=receipt.immediate_parent.row_count,
        result_path=str(result_path),
        checkpoint_path=str(checkpoint_path),
        progress_path=str(progress_path),
    )


def production_fixture_block(
    fixture: RetainedFixture, atoms: tuple[Atom, ...]
) -> dict[str, object]:
    return {
        "retained_sha256": RETAINED_SHA256,
        "clean_room_sha256": CLEAN_ROOM_SHA256,
        "grid_size": fixture.grid_size,
        "weight_scale": fixture.weight_scale,
        "outer_side": fixture.outer_side,
        "square_side": fixture.square_side,
        "shrink_margin": fixture.shrink_margin,
        "angle_limit": fixture.angle_limit,
        "direction_steps": fixture.direction_steps,
        "atom_count": len(atoms),
        "direction_count": len(fixture.directions),
        "total_weight": sum((atom.weight for atom in atoms), start=Fraction(0)),
    }


def verify_production_ancestry() -> tuple[AncestryReceipt, RetainedFixture, tuple[Atom, ...]]:
    """Verify both frozen ancestries. Evaluates no direction and writes nothing."""

    verify_frozen_inputs()
    fixture = load_retained_fixture()
    atoms = _normalized_atoms(fixture)
    if len(fixture.directions) != DIRECTION_COUNT:
        raise SuccessorError("retained direction count changed")
    receipt = verify_ancestry(
        immediate_spec=production_immediate_parent_spec(),
        genesis_spec=production_chain_genesis_spec(),
        directions=fixture.directions,
        genesis_resume_stage=RESUME_STAGE,
    )
    return receipt, fixture, atoms


def ancestry_report() -> dict[str, object]:
    """Readmission view: both ancestries verified, no target direction evaluated."""

    receipt, fixture, atoms = verify_production_ancestry()
    return {
        "schema_version": 1,
        "report": f"{EXPERIMENT_ID}-ancestry-verification",
        "immediate_parent": {"verified": True, **_as_mapping(receipt.immediate_parent)},
        "chain_genesis": {"verified": True, **_as_mapping(receipt.chain_genesis)},
        "roles_distinct": True,
        "genesis_is_prefix_of_immediate_parent": True,
        "carried_row_count": len(receipt.carried_rows),
        "genesis_row_count": len(receipt.genesis_rows),
        "first_new_ordinal": FIRST_NEW_ORDINAL,
        "direction_count": len(fixture.directions),
        "fixture_hash": fixture_binding_hash(
            atoms=atoms,
            directions=fixture.directions,
            outer_side=fixture.outer_side,
            square_side=fixture.square_side,
        ),
        "successor_driver_sha256": successor_driver_sha256(),
        "resume_driver_sha256": driver_sha256(),
        "child_driver_sha256": child_driver_sha256(),
        "frozen_package_sha256": FROZEN_PACKAGE_SHA256,
        "target_directions_evaluated": 0,
    }


def calibrate(ordinal: int) -> dict[str, object]:
    """Recompute one already-retained direction, time it, and project the remainder.

    Read-only: it writes nothing and it evaluates a direction whose exact answer is
    already in the immediate parent, so it can also check that this host reproduces the
    retained row hash before the writer is scheduled.
    """

    receipt, fixture, atoms = verify_production_ancestry()
    if not 0 <= ordinal < len(receipt.carried_rows):
        raise SuccessorError("calibration ordinal is not a retained row")
    retained = receipt.carried_rows[ordinal]
    direction = fixture.directions[ordinal]
    started = time.perf_counter()
    source = accumulate_source_faithful(
        atoms, direction, fixture.outer_side, fixture.square_side
    )
    midpoint = time.perf_counter()
    independent = accumulate_target_independent(
        atoms, direction, fixture.outer_side, fixture.square_side
    )
    finished = time.perf_counter()
    row_seconds = finished - started
    digest = _row_hash(
        ordinal=ordinal,
        direction=direction,
        source=source,
        independent=independent,
        agreement=source == independent,
        previous_row_hash=retained.previous_row_hash,
    )
    remaining = range(len(receipt.carried_rows), len(fixture.directions))
    reference = float(retained.independent.event_cell_count)
    proxy = sum(_cost_proxy(atoms, fixture, index) / reference for index in remaining)
    return {
        "schema_version": 1,
        "report": f"{EXPERIMENT_ID}-calibration",
        "calibration_ordinal": ordinal,
        "source_seconds": round(midpoint - started, 3),
        "independent_seconds": round(finished - midpoint, 3),
        "row_seconds": round(row_seconds, 3),
        "reproduces_retained_row_hash": digest == retained.row_hash,
        "retained_row_hash": retained.row_hash,
        "recomputed_row_hash": digest,
        "agreement": source == independent,
        "remaining_rows": len(remaining),
        "cost_proxy_vs_calibration_row": round(proxy, 4),
        "projected_accumulation_seconds": round(proxy * row_seconds, 1),
        "projected_accumulation_minutes": round(proxy * row_seconds / 60, 1),
    }


def _cost_proxy(atoms: tuple[Atom, ...], fixture: RetainedFixture, ordinal: int) -> float:
    from cases.n17_weighted_certificate.geometry import (  # noqa: PLC0415
        reduce_event_cells,
    )

    reduction = reduce_event_cells(
        atoms, fixture.directions[ordinal], fixture.outer_side, fixture.square_side
    )
    return float(len(reduction.cells))


def _production_paths(record: Path, checkpoint: Path, progress: Path) -> None:
    if (record, checkpoint, progress) != (RESULT_PATH, CHECKPOINT_PATH, PROGRESS_PATH):
        raise SuccessorError("command paths do not match the successor preregistration")


def run_target(record: Path, checkpoint: Path, progress: Path) -> dict[str, object]:
    """Verify both ancestries, recompute ordinal 170 onward, and publish once."""

    _production_paths(record, checkpoint, progress)
    for path, label in (
        (record, "result path"),
        (checkpoint, "checkpoint path"),
        (progress, "progress path"),
    ):
        require_writable(path, OUTPUT_ROOT, label)
    if record.exists():
        raise SuccessorError("result path already exists")
    receipt, fixture, atoms = verify_production_ancestry()
    binding = successor_binding(
        receipt,
        experiment_id=EXPERIMENT_ID,
        session_id=SESSION_ID,
        experiment_record_path=EXPERIMENT_RECORD_PATH,
        atoms=atoms,
        directions=fixture.directions,
        outer_side=fixture.outer_side,
        square_side=fixture.square_side,
        result_path=record,
        checkpoint_path=checkpoint,
        progress_path=progress,
    )
    store = SuccessorCheckpointStore(
        binding=binding,
        directions=fixture.directions,
        carried_rows=receipt.carried_rows,
        output_root=OUTPUT_ROOT,
        result_path=record,
        checkpoint_path=checkpoint,
        progress_path=progress,
        production=True,
    )
    completed = SuccessorChainDriver(store).run(
        atoms=atoms, outer_side=fixture.outer_side, square_side=fixture.square_side
    )
    store.read_progress(completed)
    if progress.exists():
        raise SuccessorError("progress marker survived the final checkpoint reconciliation")
    store.refuse_existing_result()
    evidence = production_evidence(fixture, atoms)
    if evidence.expectations != PRODUCTION_EXPECTATIONS:
        raise SuccessorError("production evidence does not carry the frozen expectations")
    if set(evidence.mutation_guards) != set(FROZEN_MUTATIONS):
        raise SuccessorError("production evidence does not carry the frozen mutation map")
    result = assemble_result(
        completed,
        evidence,
        atoms=atoms,
        directions=fixture.directions,
        fixture_block=production_fixture_block(fixture, atoms),
        checkpoint_sha256=_sha256(checkpoint),
    )
    _write_exclusive(record, canonical_json(result) + "\n")
    return {
        "schema_version": 1,
        "published": record.as_posix(),
        "result_sha256": _sha256(record),
        "terminal_schema": result["terminal_schema"],
        "decision": result["decision"],
        "instrument_valid": result["instrument_valid"],
        "status": chain_status(checkpoint),
    }


# --- Self-test ----------------------------------------------------------------------
#
# Every guard below runs on synthetic directions only.  No target direction is
# evaluated, and no frozen artifact is written.  The synthetic ancestry has the same
# shape as the production one: a two-row genesis, an immediate parent that carries it
# and stops mid-direction with a live marker, and a successor that recomputes that
# interrupted ordinal rather than promoting it.


def _falsify_first(items: list[Any]) -> None:
    """Flip the first entry of an emitted boolean vector, for the refusal guards."""

    items[0] = False


def _require(condition: bool, guard: str) -> None:  # noqa: FBT001
    if not condition:
        raise SuccessorError(f"selftest guard failed: {guard}")


def _expect_refusal(action: Callable[[], object], guard: str) -> None:
    try:
        action()
    except REFUSALS:
        return
    raise SuccessorError(f"selftest guard failed: {guard}")


def _rewrite(path: Path, mutate: Callable[[dict[str, Any]], None]) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    mutate(value)
    path.write_text(canonical_json(value) + "\n", encoding="utf-8")


def synthetic_inputs() -> tuple[tuple[Atom, ...], tuple[Direction, ...], Fraction, Fraction]:
    atoms = (
        Atom("a", Fraction(1, 2), Fraction(1, 2), Fraction(1)),
        Atom("b", Fraction(1), Fraction(1), Fraction(2)),
        Atom("c", Fraction(3, 2), Fraction(3, 2), Fraction(3)),
    )
    triples = (
        ("axis", 1, 0, 1),
        ("three-four", 3, 4, 5),
        ("five-twelve", 5, 12, 13),
        ("eight-fifteen", 8, 15, 17),
        ("twenty-twentyone", 20, 21, 29),
        ("seven-twentyfour", 7, 24, 25),
    )
    directions = tuple(
        Direction(
            label,
            Fraction(cosine, hypotenuse),
            Fraction(sine, hypotenuse),
            Fraction(-sine, hypotenuse),
            Fraction(cosine, hypotenuse),
        )
        for label, cosine, sine, hypotenuse in triples
    )
    return atoms, directions, Fraction(2), Fraction(1)


def _synthetic_genesis(root: Path) -> ParentSpec:
    """Build a two-row exp-052-shaped genesis with the unchanged resume machinery."""

    atoms, directions, outer_side, square_side = synthetic_inputs()
    root.mkdir(parents=True, exist_ok=True)
    result = root / "genesis.json"
    checkpoint = root / "genesis.checkpoint.json"
    progress = root / "genesis.progress.json"
    binding = RunBinding(
        schema_version=SCHEMA_VERSION,
        experiment_id="exp-052",
        hypothesis_id=HYPOTHESIS_ID,
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
            raise RuntimeError("synthetic genesis timebox")
        return accumulate_source_faithful(call_atoms, direction, call_outer, call_square)

    try:
        DirectionSlicedDriver(store, source_accumulator=stop_after_two).run(
            atoms=atoms, outer_side=outer_side, square_side=square_side
        )
    except RuntimeError:
        pass
    else:
        raise SuccessorError("selftest guard failed: synthetic-genesis-timebox")
    loaded = store.load()
    return ParentSpec(
        experiment_id="exp-052",
        checkpoint_path=checkpoint,
        progress_path=progress,
        result_path=result,
        checkpoint_sha256=_sha256(checkpoint),
        progress_sha256=_sha256(progress),
        binding_hash=binding_hash(binding),
        last_row_hash=loaded.rows[-1].row_hash,
        row_count=len(loaded.rows),
    )


def _synthetic_immediate_parent(root: Path, genesis: ParentSpec) -> ImmediateParentSpec:
    """Build a four-row exp-056-shaped parent that stops with a live marker at five."""

    atoms, directions, outer_side, square_side = synthetic_inputs()
    _, genesis_rows = verify_parent(genesis, directions)
    root.mkdir(parents=True, exist_ok=True)
    result = root / "parent.json"
    checkpoint = root / "parent.checkpoint.json"
    progress = root / "parent.progress.json"
    binding = ChildBinding(
        schema_version=SCHEMA_VERSION,
        experiment_id="exp-056",
        hypothesis_id=HYPOTHESIS_ID,
        session_id="session-079",
        experiment_record_path=CHILD_EXPERIMENT_RECORD_PATH,
        parent_experiment_id="exp-052",
        parent_checkpoint_sha256=genesis.checkpoint_sha256,
        parent_progress_sha256=genesis.progress_sha256,
        parent_binding_hash=genesis.binding_hash,
        parent_last_row_hash=genesis_rows[-1].row_hash,
        parent_row_count=len(genesis_rows),
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
        result_path=str(result),
        checkpoint_path=str(checkpoint),
        progress_path=str(progress),
    )
    store = ChildCheckpointStore(
        binding=binding,
        directions=directions,
        parent_rows=genesis_rows,
        output_root=root,
        result_path=result,
        checkpoint_path=checkpoint,
        progress_path=progress,
    )
    calls = 0

    def stop_on_third(
        call_atoms: tuple[Atom, ...],
        direction: Direction,
        call_outer: Fraction,
        call_square: Fraction,
    ) -> DirectionManifest:
        nonlocal calls
        calls += 1
        if calls == 3:
            raise RuntimeError("synthetic immediate-parent timebox")
        return accumulate_target_independent(call_atoms, direction, call_outer, call_square)

    try:
        ChildChainDriver(store, independent_accumulator=stop_on_third).run(
            atoms=atoms, outer_side=outer_side, square_side=square_side
        )
    except RuntimeError:
        pass
    else:
        raise SuccessorError("selftest guard failed: synthetic-immediate-parent-timebox")
    loaded = store.load()
    return ImmediateParentSpec(
        experiment_id="exp-056",
        genesis_experiment_id="exp-052",
        checkpoint_path=checkpoint,
        progress_path=progress,
        result_path=result,
        checkpoint_sha256=_sha256(checkpoint),
        progress_sha256=_sha256(progress),
        binding_hash=child_binding_hash(binding),
        last_row_hash=loaded.rows[-1].row_hash,
        row_count=len(loaded.rows),
        genesis_binding_hash=genesis.binding_hash,
        genesis_last_row_hash=genesis_rows[-1].row_hash,
        genesis_row_count=len(genesis_rows),
        resume_ordinal=len(loaded.rows),
        resume_stage="independent_started",
    )


def synthetic_receipt(
    root: Path, name: str
) -> tuple[AncestryReceipt, ParentSpec, ImmediateParentSpec]:
    _, directions, _, _ = synthetic_inputs()
    genesis = _synthetic_genesis(root / name / "genesis")
    immediate = _synthetic_immediate_parent(root / name / "parent", genesis)
    receipt = verify_ancestry(
        immediate_spec=immediate,
        genesis_spec=genesis,
        directions=directions,
        genesis_resume_stage="source_started",
    )
    return receipt, genesis, immediate


def synthetic_successor_store(
    root: Path,
    name: str,
    receipt: AncestryReceipt,
    *,
    progress_remover: Callable[[Path], None] = _durable_unlink,
) -> SuccessorCheckpointStore:
    atoms, directions, outer_side, square_side = synthetic_inputs()
    out = root / name / "successor"
    out.mkdir(parents=True, exist_ok=True)
    binding = successor_binding(
        receipt,
        experiment_id="exp-synthetic",
        session_id="session-synthetic",
        experiment_record_path="campaign/synthetic/record.md",
        atoms=atoms,
        directions=directions,
        outer_side=outer_side,
        square_side=square_side,
        result_path=out / "successor.json",
        checkpoint_path=out / "successor.checkpoint.json",
        progress_path=out / "successor.progress.json",
    )
    return SuccessorCheckpointStore(
        binding=binding,
        directions=directions,
        carried_rows=receipt.carried_rows,
        output_root=out,
        result_path=Path(binding.result_path),
        checkpoint_path=Path(binding.checkpoint_path),
        progress_path=Path(binding.progress_path),
        progress_remover=progress_remover,
    )


def _synthetic_evidence(
    checkpoint: SuccessorCheckpoint, *, global_minimum: Fraction
) -> InstrumentEvidence:
    atoms, directions, outer_side, _ = synthetic_inputs()
    internal_side = outer_side - Fraction(1, 2)
    containment = Fraction(9, 10)
    return InstrumentEvidence(
        preconditions={
            "direction_unit": tuple(
                direction.ux * direction.ux + direction.uy * direction.uy == 1
                for direction in directions
            ),
            "final_pair_brackets_quarter_turn": True,
            "adjacent_half_gap_bounds": tuple(True for _ in directions[:-1]),
            "angle_error_bound": Fraction(1, 10),
            "containment_left_operand": containment,
            "containment_right_operand": Fraction(1),
            "containment_strict": containment < 1,
            "side_decomposition_operands": {
                "outer_side": outer_side,
                "internal_side": internal_side,
                "shrink_margin": Fraction(1, 2),
            },
            "side_decomposition": scaling_preconditions(
                outer_side=outer_side,
                internal_side=internal_side,
                shrink_margin=Fraction(1, 2),
            ),
        },
        shrink_and_scaling=shrink_and_scaling_block(
            outer_side=outer_side,
            internal_side=internal_side,
            shrink_margin=Fraction(1, 2),
            containment_left_operand=containment,
        ),
        mutation_guards=dict.fromkeys(sorted(FROZEN_MUTATIONS), True),
        expectations=FrozenExpectations(
            atom_count=len(atoms),
            direction_count=len(directions),
            total_weight=sum((atom.weight for atom in atoms), start=Fraction(0)),
            global_minimum=global_minimum,
        ),
    )


def _synthetic_fixture_block() -> dict[str, object]:
    atoms, directions, outer_side, square_side = synthetic_inputs()
    return {
        "retained_sha256": RETAINED_SHA256,
        "clean_room_sha256": CLEAN_ROOM_SHA256,
        "grid_size": 0,
        "weight_scale": 1,
        "outer_side": outer_side,
        "square_side": square_side,
        "shrink_margin": Fraction(1, 2),
        "angle_limit": Fraction(1),
        "direction_steps": len(directions) - 1,
        "atom_count": len(atoms),
        "direction_count": len(directions),
        "total_weight": sum((atom.weight for atom in atoms), start=Fraction(0)),
    }


def assemble_synthetic_result(
    checkpoint: SuccessorCheckpoint, store: SuccessorCheckpointStore
) -> dict[str, object]:
    atoms, directions, _, _ = synthetic_inputs()
    minimum = min(row.source.minimum for row in checkpoint.rows)
    return assemble_result(
        checkpoint,
        _synthetic_evidence(checkpoint, global_minimum=minimum),
        atoms=atoms,
        directions=directions,
        fixture_block=_synthetic_fixture_block(),
        checkpoint_sha256=_sha256(store.checkpoint_path),
    )


def _ancestry_guards(
    root: Path,
    receipt: AncestryReceipt,
    genesis: ParentSpec,
    immediate: ImmediateParentSpec,
    receipts: dict[str, bool],
) -> None:
    """Guards over the two ancestries: distinctness, substitution, ordinal and stage."""

    _, directions, _, _ = synthetic_inputs()
    _require(receipt.immediate_parent.role == IMMEDIATE_PARENT_ROLE, "immediate-parent-role")
    _require(receipt.chain_genesis.role == CHAIN_GENESIS_ROLE, "chain-genesis-role")
    _require(
        receipt.carried_rows[0].previous_row_hash == receipt.chain_genesis.binding_hash,
        "carried-prefix-anchored-at-genesis",
    )
    _require(
        receipt.carried_rows[-1].row_hash == receipt.immediate_parent.last_row_hash,
        "carried-prefix-ends-at-immediate-parent",
    )
    _require(
        receipt.carried_rows[: len(receipt.genesis_rows)] == receipt.genesis_rows,
        "genesis-is-prefix-of-carried-prefix",
    )
    for guard in (
        "immediate-parent-role",
        "chain-genesis-role",
        "carried-prefix-anchored-at-genesis",
        "carried-prefix-ends-at-immediate-parent",
        "genesis-is-prefix-of-carried-prefix",
    ):
        receipts[guard] = True

    # Substitution in either direction must refuse: the two artifacts are different
    # shapes, and the declared identities are cross-checked against what is on disk.
    _expect_refusal(
        lambda: verify_immediate_parent(
            replace(
                immediate,
                checkpoint_path=genesis.checkpoint_path,
                progress_path=genesis.progress_path,
                checkpoint_sha256=genesis.checkpoint_sha256,
                progress_sha256=genesis.progress_sha256,
            ),
            directions,
        ),
        "swapped-ancestry-refusal-parent-slot",
    )
    _expect_refusal(
        lambda: verify_chain_genesis(
            replace(
                genesis,
                checkpoint_path=immediate.checkpoint_path,
                progress_path=immediate.progress_path,
                checkpoint_sha256=immediate.checkpoint_sha256,
                progress_sha256=immediate.progress_sha256,
            ),
            directions,
            resume_stage="source_started",
        ),
        "swapped-ancestry-refusal-genesis-slot",
    )
    _expect_refusal(
        lambda: verify_immediate_parent(
            replace(immediate, experiment_id="exp-052", genesis_experiment_id="exp-056"),
            directions,
        ),
        "swapped-ancestry-refusal-identities",
    )
    _expect_refusal(
        lambda: verify_chain_genesis(
            replace(genesis, experiment_id="exp-056"), directions, resume_stage="source_started"
        ),
        "genesis-may-not-be-the-parent",
    )
    _expect_refusal(
        lambda: verify_immediate_parent(replace(immediate, resume_ordinal=1), directions),
        "ancestry-wrong-ordinal-refusal",
    )
    _expect_refusal(
        lambda: verify_immediate_parent(
            replace(immediate, resume_stage="source_complete"), directions
        ),
        "ancestry-wrong-stage-refusal",
    )
    _expect_refusal(
        lambda: verify_immediate_parent(replace(immediate, binding_hash="0" * 64), directions),
        "ancestry-wrong-binding-refusal",
    )
    _expect_refusal(
        lambda: verify_immediate_parent(
            replace(immediate, checkpoint_sha256="0" * 64), directions
        ),
        "ancestry-digest-mismatch-refusal",
    )
    _expect_refusal(
        lambda: verify_immediate_parent(
            replace(immediate, genesis_binding_hash="0" * 64), directions
        ),
        "ancestry-genesis-anchor-refusal",
    )
    for guard in (
        "swapped-ancestry-refusal-parent-slot",
        "swapped-ancestry-refusal-genesis-slot",
        "swapped-ancestry-refusal-identities",
        "genesis-may-not-be-the-parent",
        "ancestry-wrong-ordinal-refusal",
        "ancestry-wrong-stage-refusal",
        "ancestry-wrong-binding-refusal",
        "ancestry-digest-mismatch-refusal",
        "ancestry-genesis-anchor-refusal",
    ):
        receipts[guard] = True

    tampered_root = root / "tampered"
    tampered_root.mkdir(parents=True, exist_ok=True)
    tampered = tampered_root / "parent.checkpoint.json"
    tampered.write_text(immediate.checkpoint_path.read_text(encoding="utf-8"), encoding="utf-8")
    _rewrite(tampered, lambda value: value["rows"][0].__setitem__("row_hash", "0" * 64))
    _expect_refusal(
        lambda: verify_immediate_parent(
            replace(immediate, checkpoint_path=tampered, checkpoint_sha256=_sha256(tampered)),
            directions,
        ),
        "changed-retained-row-refusal",
    )
    noncanonical = tampered_root / "noncanonical.checkpoint.json"
    noncanonical.write_text(
        json.dumps(json.loads(immediate.checkpoint_path.read_text(encoding="utf-8")), indent=2),
        encoding="utf-8",
    )
    _expect_refusal(
        lambda: verify_immediate_parent(
            replace(
                immediate,
                checkpoint_path=noncanonical,
                checkpoint_sha256=_sha256(noncanonical),
            ),
            directions,
        ),
        "noncanonical-checkpoint-refusal",
    )
    marker = tampered_root / "parent.progress.json"
    marker.write_text(immediate.progress_path.read_text(encoding="utf-8"), encoding="utf-8")
    _rewrite(marker, lambda value: value.__setitem__("binding_hash", "0" * 64))
    _expect_refusal(
        lambda: verify_immediate_parent(
            replace(immediate, progress_path=marker, progress_sha256=_sha256(marker)),
            directions,
        ),
        "wrong-progress-binding-refusal",
    )
    receipts["changed-retained-row-refusal"] = True
    receipts["noncanonical-checkpoint-refusal"] = True
    receipts["wrong-progress-binding-refusal"] = True


def _schema_guards(record: dict[str, Any], receipts: dict[str, bool]) -> None:
    """Guards over the complete-agreement schema and its derived decision."""

    _require(record["terminal_schema"] == TERMINAL_COMPLETE_AGREEMENT, "agreement-schema")
    _require(record["decision"] == "accepted", "agreement-decision-accepted")
    _require(record["instrument_valid"] is True, "agreement-instrument-valid")
    _require(record["absences"] == {}, "agreement-declares-no-absence")
    _require(
        set(record["source_faithful"]) == set(record["independent"]),
        "both-summaries-present",
    )
    _require(
        len(record["source_faithful"]["rows"])
        == record["frozen_expectations"]["direction_count"],
        "source-summary-is-complete",
    )
    _require(
        len(record["independent"]["rows"]) == record["frozen_expectations"]["direction_count"],
        "independent-summary-is-complete",
    )
    _require(
        record["global_minimum"]["source_faithful"]
        == record["global_minimum"]["independent"]
        == record["frozen_expectations"]["global_minimum"],
        "global-minima-agree",
    )
    for guard in (
        "agreement-schema",
        "agreement-decision-accepted",
        "agreement-instrument-valid",
        "agreement-declares-no-absence",
        "both-summaries-present",
        "source-summary-is-complete",
        "independent-summary-is-complete",
        "global-minima-agree",
    ):
        receipts[guard] = True

    for guard, mutate in (
        ("missing-summary-refusal", lambda copy: copy.pop("independent")),
        (
            "missing-source-summary-refusal",
            lambda copy: copy.pop("source_faithful"),
        ),
        (
            "wrong-global-minimum-refusal",
            lambda copy: copy["source_faithful"].__setitem__("global_minimum", "999/1"),
        ),
        (
            "wrong-global-minimum-echo-refusal",
            lambda copy: copy["global_minimum"].__setitem__("source_faithful", "999/1"),
        ),
        (
            "wrong-row-minimum-refusal",
            lambda copy: copy["row_minimums"]["independent"].__setitem__(0, "999/1"),
        ),
        (
            "tampered-summary-row-refusal",
            lambda copy: copy["independent"]["rows"][0].__setitem__("minimum", "999/1"),
        ),
        (
            "false-precondition-refusal",
            lambda copy: _falsify_first(copy["preconditions"]["direction_unit"]),
        ),
        (
            "surviving-mutation-refusal",
            lambda copy: copy["mutation_guards"].update({"scaling_mutation_rejected": False}),
        ),
        (
            "false-shrink-precondition-refusal",
            lambda copy: copy["shrink_and_scaling"].update({"exact_side_decomposition": False}),
        ),
        (
            "tampered-instrument-valid-refusal",
            lambda copy: copy.update({"instrument_valid": False}),
        ),
        (
            "tampered-decision-refusal",
            lambda copy: copy.__setitem__("decision", "rejected"),
        ),
        (
            "tampered-binding-hash-refusal",
            lambda copy: copy.__setitem__("binding_hash", "0" * 64),
        ),
        (
            "tampered-chain-spine-refusal",
            lambda copy: copy["chain_spine"][-1].__setitem__("row_hash", "0" * 64),
        ),
        (
            "tampered-carried-boundary-refusal",
            lambda copy: copy["carried_boundary"].__setitem__("row_hash", "0" * 64),
        ),
        (
            "tampered-ancestry-role-refusal",
            lambda copy: copy["ancestry"]["chain_genesis"].__setitem__(
                "role", IMMEDIATE_PARENT_ROLE
            ),
        ),
        ("extra-key-refusal", lambda copy: copy.__setitem__("extra", 1)),
        (
            "declared-absence-in-agreement-refusal",
            lambda copy: copy["absences"].__setitem__("global_minimum", {"absent": True}),
        ),
    ):
        copy = json.loads(canonical_json(record))
        mutate(copy)
        _expect_refusal(lambda copy=copy: validate_result(copy), guard)
        receipts[guard] = True

    # A consistently false precondition does not merely refuse: it must route the
    # decision away from acceptance.
    for guard, mutate in (
        (
            "false-precondition-invalidates",
            lambda copy: _falsify_first(copy["preconditions"]["direction_unit"]),
        ),
        (
            "surviving-mutation-invalidates",
            lambda copy: copy["mutation_guards"].update({"atom_mutation_rejected": False}),
        ),
        (
            "false-shrink-precondition-invalidates",
            lambda copy: copy["shrink_and_scaling"].update({"containment_strict": False}),
        ),
    ):
        copy = json.loads(canonical_json(record))
        mutate(copy)
        copy["preconditions_pass"] = derive_preconditions_pass(copy["preconditions"])
        copy["all_mutations_rejected"] = all(copy["mutation_guards"].values())
        copy["shrink_and_scaling"]["all_hold"] = derive_shrink_and_scaling_pass(
            copy["shrink_and_scaling"]
        )
        copy["instrument_valid"] = derive_instrument_valid(copy)
        copy["decision"] = derive_decision(copy)
        _require(copy["instrument_valid"] is False, guard)
        _require(copy["decision"] == "unresolved-invalid-instrument", guard)
        validate_result(copy)
        receipts[guard] = True


def _disagreement_guards(record: dict[str, Any], receipts: dict[str, bool]) -> None:
    """Guards over the early-disagreement schema and its declared absences."""

    _require(record["terminal_schema"] == TERMINAL_EARLY_DISAGREEMENT, "disagreement-schema")
    _require(record["decision"] == "rejected", "disagreement-decision-rejected")
    _require(record["instrument_valid"] is True, "disagreement-instrument-valid")
    _require(
        set(record["absences"]) == set(DISAGREEMENT_ABSENCES),
        "disagreement-declares-every-absence",
    )
    _require(
        record["absences"]["suffix_rows"]["absent_count"] >= 1,
        "disagreement-suffix-is-nonempty",
    )
    _require(
        record["verified_prefix"]["carried_last_row_hash"]
        == record["binding"]["immediate_parent"]["last_row_hash"],
        "disagreement-prefix-carries-the-parent-boundary",
    )
    _require(
        record["discrepant_pair"]["ordinal"] == record["first_disagreement"]["ordinal"],
        "disagreement-pair-matches-decision",
    )
    _require(
        bool(record["discrepant_pair"]["differing_fields"]),
        "disagreement-names-its-differing-fields",
    )
    for guard in (
        "disagreement-schema",
        "disagreement-decision-rejected",
        "disagreement-instrument-valid",
        "disagreement-declares-every-absence",
        "disagreement-suffix-is-nonempty",
        "disagreement-prefix-carries-the-parent-boundary",
        "disagreement-pair-matches-decision",
        "disagreement-names-its-differing-fields",
    ):
        receipts[guard] = True

    for guard, mutate in (
        (
            "disagreement-refuses-a-full-source-manifest",
            lambda copy: copy.__setitem__("source_faithful", {"rows": []}),
        ),
        (
            "disagreement-refuses-a-full-independent-manifest",
            lambda copy: copy.__setitem__("independent", {"rows": []}),
        ),
        (
            "disagreement-refuses-a-global-minimum",
            lambda copy: copy.__setitem__("global_minimum", "1/1"),
        ),
        (
            "disagreement-requires-the-suffix-absence",
            lambda copy: copy["absences"].pop("suffix_rows"),
        ),
        (
            "disagreement-requires-the-manifest-absences",
            lambda copy: copy["absences"].pop("source_faithful_certificate_manifest"),
        ),
        (
            "disagreement-absence-needs-a-reason",
            lambda copy: copy["absences"]["global_minimum"].__setitem__("reason", ""),
        ),
        (
            "disagreement-absence-must-declare-itself",
            lambda copy: copy["absences"]["row_minimums"].update({"absent": False}),
        ),
        (
            "disagreement-pair-hash-refusal",
            lambda copy: copy["discrepant_pair"].__setitem__("row_hash", "0" * 64),
        ),
        (
            "disagreement-pair-must-disagree",
            lambda copy: copy["discrepant_pair"].__setitem__(
                "independent", copy["discrepant_pair"]["source"]
            ),
        ),
        (
            "disagreement-prefix-anchor-refusal",
            lambda copy: copy["verified_prefix"].__setitem__("genesis_anchor_hash", "0" * 64),
        ),
    ):
        copy = json.loads(canonical_json(record))
        mutate(copy)
        _expect_refusal(lambda copy=copy: validate_result(copy), guard)
        receipts[guard] = True


def run_selftest() -> dict[str, object]:
    """Exercise every named successor guard on synthetic directions only."""

    verify_frozen_inputs()
    receipts: dict[str, bool] = {"frozen-inputs": True}
    atoms, directions, outer_side, square_side = synthetic_inputs()
    with tempfile.TemporaryDirectory(prefix="n17-successor-selftest-") as name:
        root = Path(name)
        receipt, genesis, immediate = synthetic_receipt(root, "base")
        receipts["ancestry-both-verified"] = True
        frozen_digests = tuple(
            _sha256(path)
            for path in (
                immediate.checkpoint_path,
                immediate.progress_path,
                genesis.checkpoint_path,
                genesis.progress_path,
            )
        )
        _ancestry_guards(root, receipt, genesis, immediate, receipts)

        store = synthetic_successor_store(root, "base", receipt)
        first_new = store.binding.first_new_ordinal
        opened = store.open_chain()
        _require(len(opened.rows) == receipt.immediate_parent.row_count, "carried-rows-opened")
        _require(
            first_new == len(receipt.carried_rows),
            "first-new-ordinal-is-first-incomplete",
        )
        _require(first_new < len(directions), "first-new-ordinal-is-in-range")
        receipts["carried-rows-opened"] = True
        receipts["first-new-ordinal-is-first-incomplete"] = True
        receipts["first-new-ordinal-is-in-range"] = True

        completed = SuccessorChainDriver(store).run(
            atoms=atoms, outer_side=outer_side, square_side=square_side
        )
        _require(len(completed.rows) == len(directions), "successor-completes-the-chain")
        _require(
            completed.rows[first_new].previous_row_hash
            == receipt.immediate_parent.last_row_hash,
            "recomputed-ordinal-chains-onto-the-parent",
        )
        _require(
            completed.rows[:first_new] == receipt.carried_rows,
            "carried-rows-unchanged-by-the-run",
        )
        _require(all(row.agreement for row in completed.rows), "synthetic-agreement")
        _require(store.read_progress(completed) is None, "no-final-progress")
        receipts["successor-completes-the-chain"] = True
        receipts["recomputed-ordinal-chains-onto-the-parent"] = True
        receipts["carried-rows-unchanged-by-the-run"] = True
        receipts["synthetic-agreement"] = True
        receipts["no-final-progress"] = True

        status = chain_status(store.checkpoint_path)
        _require(status["complete"] is True and status["all_agree"] is True, "status-report")
        _require(status["first_new_ordinal"] == first_new, "status-first-new-ordinal")
        _require(
            status["immediate_parent_experiment_id"] != status["chain_genesis_experiment_id"],
            "status-separates-the-two-ancestries",
        )
        receipts["status-report"] = True
        receipts["status-first-new-ordinal"] = True
        receipts["status-separates-the-two-ancestries"] = True

        baseline = store.checkpoint_path.read_text(encoding="utf-8")
        for guard, mutate in (
            (
                "changed-carried-row-refusal",
                lambda value: value["rows"][0].update({"agreement": False}),
            ),
            (
                "tampered-row-payload-refusal",
                lambda value: value["rows"][-1]["source"].__setitem__("minimum", "999/1"),
            ),
            (
                "wrong-previous-row-hash-refusal",
                lambda value: value["rows"][-1].__setitem__("previous_row_hash", "0" * 64),
            ),
            (
                "wrong-row-hash-refusal",
                lambda value: value["rows"][-1].__setitem__("row_hash", "0" * 64),
            ),
            (
                "wrong-ordinal-refusal",
                lambda value: value["rows"][-1].__setitem__("ordinal", 99),
            ),
            ("row-reorder-refusal", lambda value: value["rows"].reverse()),
            (
                "tampered-binding-refusal",
                lambda value: value["binding"]["chain_genesis"].__setitem__("row_count", 99),
            ),
            (
                "noncanonical-fraction-refusal",
                lambda value: value["rows"][-1]["source"].__setitem__("minimum", "2/4"),
            ),
        ):
            _rewrite(store.checkpoint_path, mutate)
            _expect_refusal(store.load, guard)
            store.checkpoint_path.write_text(baseline, encoding="utf-8")
            receipts[guard] = True
        indented = json.dumps(json.loads(baseline), indent=2)
        store.checkpoint_path.write_text(indented, encoding="utf-8")
        _expect_refusal(store.load, "noncanonical-successor-checkpoint-refusal")
        store.checkpoint_path.write_text(baseline, encoding="utf-8")
        _require(len(store.load().rows) == len(directions), "restored-baseline")
        receipts["noncanonical-successor-checkpoint-refusal"] = True
        receipts["restored-baseline"] = True

        for guard, path in (
            ("exp-056-path-refusal", IMMEDIATE_PARENT_CHECKPOINT),
            ("exp-056-progress-path-refusal", IMMEDIATE_PARENT_PROGRESS),
            ("exp-052-path-refusal", CHAIN_GENESIS_CHECKPOINT),
            (
                "resume-package-write-refusal",
                Path("cases/n17_weighted_certificate_resume/stolen.json"),
            ),
            (
                "child-package-write-refusal",
                Path("cases/n17_weighted_certificate_child/stolen.json"),
            ),
            ("frozen-package-write-refusal", FROZEN_PACKAGES[0] / "stolen.json"),
            ("lexical-escape-refusal", store.output_root / ".." / "escaped.json"),
            ("resolved-escape-refusal", root / "outside.json"),
        ):
            _expect_refusal(
                lambda path=path: require_writable(path, store.output_root, "checkpoint path"),
                guard,
            )
            receipts[guard] = True

        _expect_refusal(
            lambda: SuccessorCheckpointStore(
                binding=replace(
                    store.binding, checkpoint_path=str(IMMEDIATE_PARENT_CHECKPOINT)
                ),
                directions=directions,
                carried_rows=receipt.carried_rows,
                output_root=store.output_root,
                result_path=store.result_path,
                checkpoint_path=IMMEDIATE_PARENT_CHECKPOINT,
                progress_path=store.progress_path,
            ),
            "parent-bound-store-refusal",
        )
        receipts["parent-bound-store-refusal"] = True

        interrupted = synthetic_successor_store(root, "interrupted", receipt)

        def interrupt_independent(*_args: object) -> DirectionManifest:
            raise RuntimeError("synthetic between-accumulator interruption")

        try:
            SuccessorChainDriver(
                interrupted, independent_accumulator=interrupt_independent
            ).run(atoms=atoms, outer_side=outer_side, square_side=square_side)
        except RuntimeError:
            pass
        else:
            raise SuccessorError("selftest guard failed: between-accumulator-interruption")
        partial = interrupted.load()
        _require(len(partial.rows) == first_new, "no-partial-row-promotion")
        _require(interrupted.progress_path.is_file(), "progress-marker-written")
        marker = interrupted.read_progress(partial)
        _require(marker is not None and marker.ordinal == first_new, "marker-at-first-new")
        receipts["between-accumulator-interruption"] = True
        receipts["no-partial-row-promotion"] = True
        receipts["progress-marker-written"] = True
        receipts["marker-at-first-new"] = True

        marker_baseline = interrupted.progress_path.read_text(encoding="utf-8")
        for guard, mutate in (
            (
                "successor-wrong-progress-binding-refusal",
                lambda value: value.__setitem__("binding_hash", "0" * 64),
            ),
            (
                "successor-wrong-stage-refusal",
                lambda value: value.__setitem__("stage", "not_a_stage"),
            ),
            (
                "successor-progress-inside-carried-prefix-refusal",
                lambda value: value.__setitem__("ordinal", 1),
            ),
            (
                "successor-progress-ahead-of-checkpoint-refusal",
                lambda value: value.__setitem__("ordinal", len(directions)),
            ),
            (
                "successor-progress-chain-refusal",
                lambda value: value.__setitem__("previous_row_hash", "0" * 64),
            ),
        ):
            _rewrite(interrupted.progress_path, mutate)
            _expect_refusal(lambda: interrupted.read_progress(interrupted.load()), guard)
            interrupted.progress_path.write_text(marker_baseline, encoding="utf-8")
            receipts[guard] = True
        _expect_refusal(
            lambda: interrupted.write_progress(1, "source_started"),
            "successor-progress-ordinal-refusal",
        )
        receipts["successor-progress-ordinal-refusal"] = True

        resumed = SuccessorChainDriver(interrupted).run(
            atoms=atoms, outer_side=outer_side, square_side=square_side
        )
        _require(
            canonical_json(resumed.rows) == canonical_json(completed.rows),
            "interrupted-resume-equivalence",
        )
        receipts["interrupted-resume-equivalence"] = True

        _expect_refusal(
            lambda: assemble_synthetic_result(
                SuccessorCheckpoint(store.binding, completed.rows[:-1]), store
            ),
            "incomplete-chain-refusal",
        )
        _expect_refusal(
            lambda: assemble_synthetic_result(
                SuccessorCheckpoint(store.binding, completed.rows[:first_new]), store
            ),
            "carried-prefix-is-not-a-result-refusal",
        )
        receipts["incomplete-chain-refusal"] = True
        receipts["carried-prefix-is-not-a-result-refusal"] = True

        agreement = assemble_synthetic_result(completed, store)
        _schema_guards(dict(agreement), receipts)

        _write_exclusive(store.result_path, canonical_json(agreement) + "\n")
        _expect_refusal(
            lambda: _write_exclusive(store.result_path, canonical_json(agreement) + "\n"),
            "result-overwrite-refusal",
        )
        _expect_refusal(store.load, "result-blocks-further-chain-writes")
        receipts["result-overwrite-refusal"] = True
        receipts["result-blocks-further-chain-writes"] = True

        disagree = synthetic_successor_store(root, "disagreement", receipt)

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
            SuccessorChainDriver(disagree, independent_accumulator=perturbed_independent).run(
                atoms=atoms, outer_side=outer_side, square_side=square_side
            )
        except SuccessorDisagreementStopError:
            pass
        else:
            raise SuccessorError("selftest guard failed: disagreement-stop")
        retained = disagree.load()
        _require(len(retained.rows) == first_new + 1, "disagreement-stops-after-one-row")
        _require(retained.rows[-1].agreement is False, "disagreement-retained-as-row")
        disagree_status = chain_status(disagree.checkpoint_path)
        _require(
            disagree_status["first_disagreement_ordinal"] == first_new,
            "disagreement-visible-in-status",
        )
        receipts["disagreement-stop"] = True
        receipts["disagreement-stops-after-one-row"] = True
        receipts["disagreement-retained-as-row"] = True
        receipts["disagreement-visible-in-status"] = True
        _disagreement_guards(dict(assemble_synthetic_result(retained, disagree)), receipts)

        _require(
            frozen_digests
            == tuple(
                _sha256(path)
                for path in (
                    immediate.checkpoint_path,
                    immediate.progress_path,
                    genesis.checkpoint_path,
                    genesis.progress_path,
                )
            ),
            "ancestor-artifacts-unchanged",
        )
        receipts["ancestor-artifacts-unchanged"] = True

    ordered = dict(sorted(receipts.items()))
    return {
        "schema_version": 1,
        "selftest": "bc148-h052-successor-readiness",
        "passed": all(ordered.values()),
        "skipped": 0,
        "successor_driver_sha256": successor_driver_sha256(),
        "child_driver_sha256": child_driver_sha256(),
        "resume_driver_sha256": driver_sha256(),
        "frozen_package_sha256": FROZEN_PACKAGE_SHA256,
        "guard_count": len(ordered),
        "receipts": ordered,
        "receipt_hash": canonical_hash(ordered),
    }


def selftest_json() -> str:
    return canonical_json(run_selftest())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--record", type=Path)
    action.add_argument("--selftest", action="store_true")
    action.add_argument("--status", type=Path)
    action.add_argument("--verify-ancestry", action="store_true")
    action.add_argument("--calibrate", type=int, metavar="ORDINAL")
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--progress", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if (args.checkpoint is not None or args.progress is not None) and args.record is None:
        raise SuccessorError("only --record accepts output paths")
    if args.selftest:
        print(selftest_json())
        return 0
    if args.verify_ancestry:
        print(canonical_json(ancestry_report()))
        return 0
    if args.calibrate is not None:
        print(canonical_json(calibrate(args.calibrate)))
        return 0
    if args.status is not None:
        print(canonical_json(chain_status(args.status)))
        return 0
    if args.record is None or args.checkpoint is None or args.progress is None:
        raise SuccessorError("--record, --checkpoint and --progress are required")
    try:
        print(canonical_json(run_target(args.record, args.checkpoint, args.progress)))
    except SuccessorDisagreementStopError as stop:
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
