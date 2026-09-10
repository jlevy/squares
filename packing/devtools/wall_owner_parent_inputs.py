#!/usr/bin/env python3
"""Bind source receipts and complete manifests for the unit-parent adapter.

This module prepares authoritative, target-blind inputs. It does not apply a parent
restriction, evaluate compatibility, or serialize a scientific result.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from cases.n11_five_dot_cover.independent_union import FrozenInput, load_frozen_input
from devtools.owner_footprints import (
    OUTER_SIDE,
    DirectionSource,
    OwnerBranchManifest,
    OwnerClass,
    OwnerDirectionManifest,
    Point,
    convex_hull,
    full_owner_direction_manifest,
    owner_branch_manifest,
)
from devtools.wall_owner_containment import (
    CLASS_IDS,
    CORNERS,
    AffineMap,
    WallClass,
    WallInput,
    load_wall_input,
    physical_corner_maps,
)
from devtools.wall_owner_footprints import (
    RetainedOwnerFrame,
    validate_owner_manifest,
)
from devtools.wall_owner_parent_compatibility import (
    ParentCompatibilityError,
    bound_expected_owner_frames,
    intersect_parent_box,
    validate_bound_frames,
)
from devtools.wall_owner_selected_cover import (
    SELECTED_TUPLE,
    SelectedCoverEvidence,
    load_selected_cover_evidence,
    replay_selected_cover_evidence,
)
from devtools.wall_owner_six_dot_cover import (
    augment_with_selected_escape,
    replay_six_dot_escape,
)
from devtools.wall_owner_sixth_site_screen import (
    SixDotEscapeEvidence,
    load_six_dot_escape_evidence,
)

EXPECTED_ORIENTATION_COUNT = 361
EXPECTED_CLASS_COUNT = 16
EXPECTED_FRAMES_PER_SELECTED_CLASS = 181


@dataclass(frozen=True, slots=True)
class ReceiptPin:
    """One repository-relative receipt and exact Git blob."""

    path: str
    git_blob: str


@dataclass(frozen=True, slots=True)
class ProducedReceiptPin(ReceiptPin):
    """One receipt whose schema also exposes its producer revision."""

    producer_revision: str


@dataclass(frozen=True, slots=True)
class ParentInputPins:
    """The repository root and four identities required before evaluation."""

    repository_root: Path
    checkout_revision: str
    endpoint: ReceiptPin
    wall: ProducedReceiptPin
    selected_cover: ProducedReceiptPin
    strict_escape: ProducedReceiptPin


@dataclass(frozen=True, slots=True)
class TrackedReceiptIdentity:
    """A receipt's original pin and the clean checkout revision that supplied it."""

    path: str
    git_commit: str
    git_blob: str
    producer_revision: str | None


@dataclass(frozen=True, slots=True)
class ResidualOrientationAuthority:
    """One residual orientation and its complete folded-net provenance."""

    index: int
    label: str
    ray: Point
    turned_ray: Point
    sources: tuple[DirectionSource, ...]


@dataclass(frozen=True, slots=True)
class SelectedOwnerAuthority:
    """One selected local class, physical corner map, and expected frame inventory."""

    corner_index: int
    corner: str
    class_index: int
    class_id: str
    owner_class: OwnerClass
    wall_class: WallClass
    physical_map: AffineMap
    expected_frames: tuple[RetainedOwnerFrame, ...]


@dataclass(frozen=True, slots=True)
class ParentAdapterInputs:
    """Source-bound inputs accepted for a later parent-domain comparison."""

    checkout_revision: str
    endpoint_identity: TrackedReceiptIdentity
    wall_identity: TrackedReceiptIdentity
    selected_cover_identity: TrackedReceiptIdentity
    strict_escape_identity: TrackedReceiptIdentity
    endpoint: FrozenInput
    wall: WallInput
    selected_cover: SelectedCoverEvidence
    strict_escape: SixDotEscapeEvidence
    owner_manifest: OwnerDirectionManifest
    owner_branch: OwnerBranchManifest
    residual_manifest: tuple[ResidualOrientationAuthority, ...]
    selected_owners: tuple[SelectedOwnerAuthority, ...]
    selected_residual: ResidualOrientationAuthority


def _require_hex(value: str, label: str) -> None:
    if len(value) != 40 or any(character not in "0123456789abcdef" for character in value):
        raise ParentCompatibilityError(f"{label} must be 40 lowercase hexadecimal digits")


def _validate_pin(pin: ReceiptPin, label: str) -> None:
    if not pin.path or Path(pin.path).is_absolute() or Path(pin.path).as_posix() != pin.path:
        raise ParentCompatibilityError(f"{label} path must be a repository-relative POSIX path")
    if any(part in ("", ".", "..") for part in Path(pin.path).parts):
        raise ParentCompatibilityError(f"{label} path contains an invalid component")
    _require_hex(pin.git_blob, f"{label} git blob")
    if isinstance(pin, ProducedReceiptPin):
        _require_hex(pin.producer_revision, f"{label} producer revision")


def _resolve_receipt_paths(
    pins: ParentInputPins,
) -> tuple[Path, Path, Path, Path]:
    """Resolve every validated repository-relative pin from one explicit root."""

    if not pins.repository_root.is_absolute():
        raise ParentCompatibilityError("repository root must be an absolute path")
    repository_root = pins.repository_root.resolve()
    if not repository_root.is_dir():
        raise ParentCompatibilityError("repository root must name an existing directory")

    labelled_pins = (
        ("endpoint", pins.endpoint),
        ("wall", pins.wall),
        ("selected cover", pins.selected_cover),
        ("strict escape", pins.strict_escape),
    )
    for label, pin in labelled_pins:
        _validate_pin(pin, label)
    _require_hex(pins.checkout_revision, "checkout revision")

    paths: list[Path] = []
    for label, pin in labelled_pins:
        path = (repository_root / pin.path).resolve()
        if not path.is_relative_to(repository_root):
            raise ParentCompatibilityError(f"{label} path leaves the repository root")
        paths.append(path)
    return paths[0], paths[1], paths[2], paths[3]


def _expected_physical_maps() -> tuple[AffineMap, ...]:
    zero = Fraction(0)
    return (
        AffineMap("I", 1, 0, 0, 1, zero, zero, 0, (0, 1, 2, 3)),
        AffineMap("H", -1, 0, 0, 1, OUTER_SIDE, zero, 0, (1, 0, 3, 2)),
        AffineMap("V", 1, 0, 0, -1, zero, OUTER_SIDE, 0, (2, 3, 0, 1)),
        AffineMap("R", -1, 0, 0, -1, OUTER_SIDE, OUTER_SIDE, 0, (3, 2, 1, 0)),
    )


def _transport_polygon(polygon: tuple[Point, ...], transform: AffineMap) -> tuple[Point, ...]:
    return convex_hull(tuple(transform.point(point) for point in polygon))


def validate_physical_corner_maps(maps: tuple[AffineMap, ...]) -> None:
    """Refuse a diagonal or otherwise altered map and replay intersection commutation."""

    if maps != _expected_physical_maps():
        raise ParentCompatibilityError("physical corner maps differ from BL, BR, TL, TR")

    probe = (
        (Fraction(1, 5), Fraction(2, 5)),
        (Fraction(17, 5), Fraction(2, 5)),
        (Fraction(17, 5), Fraction(16, 5)),
        (Fraction(1, 5), Fraction(16, 5)),
    )
    parent_box = (
        (Fraction(1, 2), Fraction(1, 2)),
        (OUTER_SIDE - Fraction(1, 2), Fraction(1, 2)),
        (OUTER_SIDE - Fraction(1, 2), OUTER_SIDE - Fraction(1, 2)),
        (Fraction(1, 2), OUTER_SIDE - Fraction(1, 2)),
    )
    restricted = intersect_parent_box(probe, parent_box)
    for transform in maps:
        transformed_parent = _transport_polygon(parent_box, transform)
        transformed_restricted = _transport_polygon(restricted, transform)
        restriction_after_transport = intersect_parent_box(
            _transport_polygon(probe, transform),
            transformed_parent,
        )
        if (
            transformed_parent != parent_box
            or transformed_restricted != restriction_after_transport
        ):
            raise ParentCompatibilityError(
                f"{transform.name} does not commute with the physical parent restriction"
            )


def _receipt_identity(
    pin: ReceiptPin,
    *,
    source_path: str,
    git_commit: str,
    git_blob: str,
    producer_revision: str | None,
    label: str,
) -> TrackedReceiptIdentity:
    if (
        source_path != pin.path
        or git_blob != pin.git_blob
        or (isinstance(pin, ProducedReceiptPin) and producer_revision != pin.producer_revision)
    ):
        raise ParentCompatibilityError(f"{label} path, blob, or producer revision changed")
    _require_hex(git_commit, f"{label} checkout revision")
    return TrackedReceiptIdentity(
        source_path,
        git_commit,
        git_blob,
        producer_revision,
    )


def _bind_residual_manifest(
    source: FrozenInput,
    manifest: OwnerDirectionManifest,
) -> tuple[ResidualOrientationAuthority, ...]:
    if len(source.directions) != EXPECTED_ORIENTATION_COUNT:
        raise ParentCompatibilityError("endpoint lacks the complete 361 residual orientations")
    if len(manifest.orientations) != EXPECTED_ORIENTATION_COUNT:
        raise ParentCompatibilityError("owner manifest lacks 361 source-bearing orientations")

    rows: list[ResidualOrientationAuthority] = []
    for index, (source_direction, orientation) in enumerate(
        zip(source.directions, manifest.orientations, strict=True)
    ):
        expected_direction = orientation.direction
        if (
            orientation.index != index
            or source_direction.label != expected_direction.label
            or (source_direction.cosine, source_direction.sine)
            != (expected_direction.ux, expected_direction.uy)
            or (expected_direction.vx, expected_direction.vy)
            != (-expected_direction.uy, expected_direction.ux)
            or not orientation.sources
        ):
            raise ParentCompatibilityError(
                f"residual orientation {index} differs from its complete source manifest"
            )
        rows.append(
            ResidualOrientationAuthority(
                index,
                expected_direction.label,
                (expected_direction.ux, expected_direction.uy),
                (expected_direction.vx, expected_direction.vy),
                orientation.sources,
            )
        )
    return tuple(rows)


def _bind_selected_owners(
    wall: WallInput,
    branch: OwnerBranchManifest,
    manifest: OwnerDirectionManifest,
    maps: tuple[AffineMap, ...],
) -> tuple[SelectedOwnerAuthority, ...]:
    if len(wall.classes) != EXPECTED_CLASS_COUNT:
        raise ParentCompatibilityError("wall input lacks the complete sixteen-class inventory")
    for index, (wall_class, owner_class) in enumerate(
        zip(wall.classes, branch.classes, strict=True)
    ):
        if (
            wall_class.class_id != owner_class.class_id
            or wall_class.class_id != CLASS_IDS[index]
        ):
            raise ParentCompatibilityError(f"wall class {index} changes local-class identity")

    selected: list[SelectedOwnerAuthority] = []
    for corner_index, class_index in enumerate(SELECTED_TUPLE):
        owner_class = branch.classes[class_index]
        wall_class = wall.classes[class_index]
        expected_frames = bound_expected_owner_frames(owner_class, manifest)
        if len(expected_frames) != EXPECTED_FRAMES_PER_SELECTED_CLASS:
            raise ParentCompatibilityError(
                f"selected class {owner_class.class_id} has an incomplete expected "
                "frame inventory"
            )
        validate_bound_frames(wall_class.frames, expected_frames)
        selected.append(
            SelectedOwnerAuthority(
                corner_index,
                CORNERS[corner_index],
                class_index,
                owner_class.class_id,
                owner_class,
                wall_class,
                maps[corner_index],
                expected_frames,
            )
        )
    return tuple(selected)


def bind_parent_adapter_inputs(
    pins: ParentInputPins,
    *,
    source: FrozenInput,
    wall: WallInput,
    selected_cover: SelectedCoverEvidence,
    strict_escape: SixDotEscapeEvidence,
    owner_manifest: OwnerDirectionManifest,
    maps: tuple[AffineMap, ...],
) -> ParentAdapterInputs:
    """Bind loaded receipts to independently complete manifests without deriving domains."""

    for label, pin in (
        ("endpoint", pins.endpoint),
        ("wall", pins.wall),
        ("selected cover", pins.selected_cover),
        ("strict escape", pins.strict_escape),
    ):
        _validate_pin(pin, label)
    _require_hex(pins.checkout_revision, "checkout revision")

    validate_physical_corner_maps(maps)
    branch = owner_branch_manifest(owner_manifest)
    validate_owner_manifest(owner_manifest, branch)

    endpoint_identity = _receipt_identity(
        pins.endpoint,
        source_path=source.source_path,
        git_commit=source.git_commit,
        git_blob=source.git_blob,
        producer_revision=None,
        label="endpoint",
    )
    wall_identity = _receipt_identity(
        pins.wall,
        source_path=wall.source_path,
        git_commit=wall.git_commit,
        git_blob=wall.git_blob,
        producer_revision=wall.constructor_revision,
        label="wall",
    )
    selected_identity = _receipt_identity(
        pins.selected_cover,
        source_path=selected_cover.source_path,
        git_commit=selected_cover.git_commit,
        git_blob=selected_cover.git_blob,
        producer_revision=selected_cover.implementation_revision,
        label="selected cover",
    )
    strict_identity = _receipt_identity(
        pins.strict_escape,
        source_path=strict_escape.source_path,
        git_commit=strict_escape.git_commit,
        git_blob=strict_escape.git_blob,
        producer_revision=strict_escape.implementation_revision,
        label="strict escape",
    )
    revisions = {
        endpoint_identity.git_commit,
        wall_identity.git_commit,
        selected_identity.git_commit,
        strict_identity.git_commit,
    }
    if len(revisions) != 1:
        raise ParentCompatibilityError(
            "receipts were not loaded from one clean checkout revision"
        )
    if revisions != {pins.checkout_revision}:
        raise ParentCompatibilityError("receipt checkout revision differs from the frozen pin")

    residual_manifest = _bind_residual_manifest(source, owner_manifest)
    residual_index = strict_escape.escape.orientation_index
    if not 0 <= residual_index < len(residual_manifest):
        raise ParentCompatibilityError("strict escape orientation leaves the residual manifest")
    residual = residual_manifest[residual_index]
    if (
        strict_escape.direction.index != residual_index
        or strict_escape.direction.label != residual.label
        or strict_escape.escape.orientation_label != residual.label
    ):
        raise ParentCompatibilityError(
            "strict escape changes its selected residual orientation"
        )

    selected_owners = _bind_selected_owners(wall, branch, owner_manifest, maps)
    checkout_revision = next(iter(revisions))
    return ParentAdapterInputs(
        checkout_revision,
        endpoint_identity,
        wall_identity,
        selected_identity,
        strict_identity,
        source,
        wall,
        selected_cover,
        strict_escape,
        owner_manifest,
        branch,
        residual_manifest,
        selected_owners,
        residual,
    )


def load_parent_adapter_inputs(
    pins: ParentInputPins,
    *,
    replay_deadline: float,
) -> ParentAdapterInputs:
    """Run the admitted receipt loaders and strict replays, then bind their manifests."""

    endpoint_path, wall_path, selected_path, strict_path = _resolve_receipt_paths(pins)
    source = load_frozen_input(endpoint_path, pins.endpoint.git_blob)
    wall = load_wall_input(
        wall_path,
        pins.wall.git_blob,
        expected_source=pins.wall.producer_revision,
    )
    selected = load_selected_cover_evidence(
        selected_path,
        pins.selected_cover.git_blob,
        expected_source=pins.selected_cover.producer_revision,
        source=source,
        wall=wall,
    )
    strict = load_six_dot_escape_evidence(
        strict_path,
        pins.strict_escape.git_blob,
        expected_source=pins.strict_escape.producer_revision,
        source=source,
        wall=wall,
        selected=selected,
    )
    replay_selected_cover_evidence(selected, source=source, deadline=replay_deadline)
    augmented = augment_with_selected_escape(source, wall, selected)
    replay_six_dot_escape(strict.escape, augmented, deadline=replay_deadline)
    return bind_parent_adapter_inputs(
        pins,
        source=source,
        wall=wall,
        selected_cover=selected,
        strict_escape=strict,
        owner_manifest=full_owner_direction_manifest(),
        maps=physical_corner_maps(),
    )
