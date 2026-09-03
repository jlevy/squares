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
    ChildBinding,
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
    PairedRow,
    ProgressMarker,
    ProgressStage,
    _atomic_write,  # pyright: ignore[reportPrivateUsage]
    _certificate,  # pyright: ignore[reportPrivateUsage]
    _digest,  # pyright: ignore[reportPrivateUsage]
    _durable_unlink,  # pyright: ignore[reportPrivateUsage]
    _integer,  # pyright: ignore[reportPrivateUsage]
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
CHAIN_GENESIS_BINDING_HASH = (
    "2446fa39e154800410b9b5cc19f19aed7cc0c797d116f7ece1c97a2c7c0b4d1a"
)
CHAIN_GENESIS_LAST_ROW_HASH = (
    "9badcc57c05e328344b0ec7ae4fbf9815e8eae027a79bec1bf1a35b9871fade6"
)
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


class SuccessorDisagreementStop(RuntimeError):
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
