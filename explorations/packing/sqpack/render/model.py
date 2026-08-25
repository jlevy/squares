"""Immutable semantic model for deterministic packing figures."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import StrEnum


class ScalarKind(StrEnum):
    BINARY64 = "binary64"
    DECIMAL = "decimal"
    RATIONAL = "rational"
    EXACT = "exact"


class EvidenceTier(StrEnum):
    CANDIDATE = "candidate"
    VERIFIED_CONSTRUCTION = "verified-construction"
    CERTIFIED_UPPER_BOUND = "certified-upper-bound"
    PROVED_OPTIMUM = "proved-optimum"


class ViewLevel(StrEnum):
    OVERVIEW = "overview"
    COMPARISON = "comparison"
    TRAJECTORY = "trajectory"


class AnnotationLevel(StrEnum):
    MINIMAL = "minimal"
    NUMERIC = "numeric"
    EXACT = "exact"


class Overlay(StrEnum):
    SQUARE_IDS = "square-ids"
    CONTACTS = "contacts"
    ACTIVE_FEATURES = "active-features"


class TrajectoryKind(StrEnum):
    RETAINED = "retained"
    CERTIFIED = "certified"
    ILLUSTRATIVE = "illustrative"


@dataclass(frozen=True)
class ScalarSource:
    kind: ScalarKind
    source: str
    projected: Decimal
    precision: int
    exact_source: str | None = None


@dataclass(frozen=True)
class Point2:
    x: ScalarSource
    y: ScalarSource


@dataclass(frozen=True)
class RigidPose:
    centre: Point2
    angle: ScalarSource


@dataclass(frozen=True)
class SquareGeometry:
    square_id: str
    corners: tuple[Point2, ...]
    pose: RigidPose | None = None
    label: str | None = None


@dataclass(frozen=True)
class VerificationSummary:
    valid: bool
    method: str
    detail: str = ""


@dataclass(frozen=True)
class ContactFeature:
    feature_id: str
    point: Point2
    square_ids: tuple[str, str]
    label: str = "contact"


@dataclass(frozen=True)
class ActiveFeature:
    feature_id: str
    point: Point2
    label: str
    square_id: str | None = None


@dataclass(frozen=True)
class PackingFrame:
    container_side: ScalarSource
    squares: tuple[SquareGeometry, ...]
    evidence: EvidenceTier = EvidenceTier.CANDIDATE
    verification: VerificationSummary | None = None
    label: str = "final"
    logical_time: Decimal = Decimal(0)
    source_id: str = ""
    source_url: str = ""
    features: tuple[ContactFeature | ActiveFeature, ...] = ()


@dataclass(frozen=True)
class PackingTrajectory:
    frames: tuple[PackingFrame, ...]
    kind: TrajectoryKind
    label: str
    certificate: str = ""


@dataclass(frozen=True)
class RenderSpec:
    view: ViewLevel = ViewLevel.OVERVIEW
    annotations: AnnotationLevel = AnnotationLevel.MINIMAL
    overlays: frozenset[Overlay] = field(default_factory=frozenset)
    title: str = "Square packing"
    description: str = "A square packing rendered with mathematical y coordinates upward."
    duration_seconds: Decimal = Decimal("4")
    width: int = 960


def validate_scalar_source(value: ScalarSource) -> None:
    if not value.source.strip():
        raise ValueError("scalar source must be non-empty")
    if not value.projected.is_finite():
        raise ValueError("scalar projection must be finite")
    if value.precision < 1:
        raise ValueError("scalar precision must be positive")
    if value.kind is ScalarKind.EXACT and not (value.exact_source or "").strip():
        raise ValueError("exact scalar requires an exact source")


def _finite_pose(pose: RigidPose) -> bool:
    return all(
        value.projected.is_finite() for value in (pose.centre.x, pose.centre.y, pose.angle)
    )


def validate_square_geometry(square: SquareGeometry) -> None:
    if not square.square_id.strip():
        raise ValueError("square ID must be non-empty")
    if len(square.corners) != 4:
        raise ValueError("a square must have four corners")
    for point in square.corners:
        validate_scalar_source(point.x)
        validate_scalar_source(point.y)
    projected = [(point.x.projected, point.y.projected) for point in square.corners]
    if any(projected[index] == projected[(index + 1) % 4] for index in range(4)):
        raise ValueError("adjacent square corners must be distinct")
    if square.pose is not None and not _finite_pose(square.pose):
        raise ValueError("square pose must be finite")


def validate_frame(frame: PackingFrame) -> None:
    validate_scalar_source(frame.container_side)
    if frame.container_side.projected <= 0:
        raise ValueError("container side must be positive")
    if not frame.squares:
        raise ValueError("packing frame must contain squares")
    ids = [square.square_id for square in frame.squares]
    if len(ids) != len(set(ids)):
        raise ValueError("square IDs must be unique")
    if ids != sorted(ids):
        raise ValueError("squares must be in stable ID order")
    for square in frame.squares:
        validate_square_geometry(square)
    feature_ids = [feature.feature_id for feature in frame.features]
    if len(feature_ids) != len(set(feature_ids)) or feature_ids != sorted(feature_ids):
        raise ValueError("feature IDs must be unique and stable")
    for feature in frame.features:
        if not feature.feature_id.strip():
            raise ValueError("feature ID must be non-empty")
        validate_scalar_source(feature.point.x)
        validate_scalar_source(feature.point.y)
        if isinstance(feature, ContactFeature) and any(
            square_id not in ids for square_id in feature.square_ids
        ):
            raise ValueError("contact feature references an unknown square")
    verified = frame.verification is not None and frame.verification.valid
    if frame.evidence is not EvidenceTier.CANDIDATE and not verified:
        raise ValueError("non-candidate evidence requires successful verification")
    if not frame.logical_time.is_finite():
        raise ValueError("logical frame time must be finite")


def validate_trajectory(trajectory: PackingTrajectory) -> None:
    if len(trajectory.frames) < 2:
        raise ValueError("trajectory requires at least two frames")
    for frame in trajectory.frames:
        validate_frame(frame)
    reference = tuple(square.square_id for square in trajectory.frames[0].squares)
    previous = trajectory.frames[0].logical_time
    for frame in trajectory.frames:
        if tuple(square.square_id for square in frame.squares) != reference:
            raise ValueError("trajectory square identity or order changed")
        if any(square.pose is None for square in frame.squares):
            raise ValueError("trajectory squares require poses")
        if frame is not trajectory.frames[0] and frame.logical_time <= previous:
            raise ValueError("trajectory times must increase")
        previous = frame.logical_time
    if trajectory.kind is TrajectoryKind.CERTIFIED:
        if not trajectory.certificate.strip():
            raise ValueError("certified trajectory requires a certificate")
        if any(frame.evidence is EvidenceTier.CANDIDATE for frame in trajectory.frames):
            raise ValueError("certified trajectory cannot contain candidate frames")


def validate_render_request(
    final: PackingFrame,
    *,
    start: PackingFrame | None,
    trajectory: PackingTrajectory | None,
    spec: RenderSpec,
) -> None:
    validate_frame(final)
    if spec.width <= 0 or not spec.duration_seconds.is_finite() or spec.duration_seconds <= 0:
        raise ValueError("render dimensions and duration must be positive")
    if spec.view is ViewLevel.COMPARISON:
        if start is None:
            raise ValueError("comparison view requires a start frame")
        validate_frame(start)
    if spec.view is ViewLevel.TRAJECTORY:
        if trajectory is None:
            raise ValueError("trajectory view requires a trajectory")
        validate_trajectory(trajectory)
    if spec.annotations is AnnotationLevel.EXACT:
        frames = (
            trajectory.frames
            if trajectory is not None
            else tuple(f for f in (start, final) if f)
        )
        values = [frame.container_side for frame in frames]
        values += [
            value
            for frame in frames
            for square in frame.squares
            for point in square.corners
            for value in (point.x, point.y)
        ]
        if any(value.kind is ScalarKind.EXACT and not value.exact_source for value in values):
            raise ValueError("exact annotations require complete exact sources")
