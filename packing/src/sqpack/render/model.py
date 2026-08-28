"""Immutable semantic model for deterministic packing figures."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import StrEnum
from typing import Literal


class ScalarKind(StrEnum):
    BINARY64 = "binary64"
    DECIMAL = "decimal"
    RATIONAL = "rational"
    EXACT = "exact"


class EvidenceTier(StrEnum):
    """What the drawn configuration itself establishes, and nothing more.

    Every tier is a statement about the geometry in the frame: it is a candidate,
    its feasibility was checked numerically, or it is an exactly certified feasible
    packing and therefore an upper bound on s(n). None of that can reach optimality,
    which is a lower-bound statement about the mathematics rather than a property
    of any one packing. A PROVED_OPTIMUM member used to sit here; nothing in the
    render pipeline could ever produce it, because the pipeline is fed from witness
    records whose claim.coordinate_provenance describes how coordinates were
    encoded. It was removed so a renderer cannot reach for it: optimality lives in
    frontier/n-NNN.md as packing.status, and a figure that wants to say "proved"
    must read it from there.
    """

    CANDIDATE = "candidate"
    NUMERICALLY_CHECKED = "numerically-checked"
    CERTIFIED_UPPER_BOUND = "certified-upper-bound"


class CheckKind(StrEnum):
    NUMERICAL = "numerical"
    FORMAL = "formal"


class ViewLevel(StrEnum):
    OVERVIEW = "overview"
    COMPARISON = "comparison"
    TRAJECTORY = "trajectory"


class AnnotationLevel(StrEnum):
    MINIMAL = "minimal"
    NUMERIC = "numeric"
    EXACT = "exact"


class HueScheme(StrEnum):
    ANGLE = "angle"
    INDEX = "index"


class ShadeScheme(StrEnum):
    CONTACTS = "contacts"
    CONTRAST = "contrast"
    SEQUENCE = "sequence"


class Overlay(StrEnum):
    SQUARE_IDS = "square-ids"
    CONTACTS = "contacts"
    CONTACT_CENSUS = "contact-census"
    ACTIVE_FEATURES = "active-features"


class ContainerWall(StrEnum):
    LEFT = "left"
    RIGHT = "right"
    BOTTOM = "bottom"
    TOP = "top"


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
class CheckSummary:
    passed: bool
    kind: CheckKind
    method: str
    arithmetic: str = ""
    precision: str = ""
    rounding: str = ""
    tolerance: str = ""
    detail: str = ""


@dataclass(frozen=True)
class ContactFeature:
    feature_id: str
    start: Point2
    square_ids: tuple[str, ...]
    end: Point2 | None = None
    wall: ContainerWall | None = None
    label: str = "contact"


@dataclass(frozen=True)
class DetectedContactFeature:
    """A tolerance-qualified descriptive graph edge, not exact contact geometry."""

    feature_id: str
    start: Point2
    end: Point2
    square_ids: tuple[str, ...]
    angle_tolerance_radians: Decimal
    contact_tolerance: Decimal
    residual: Decimal | None = None
    normal: Literal["u-normal", "v-normal"] | None = None
    wall: ContainerWall | None = None
    label: str = "numerically detected contact"


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
    check: CheckSummary | None = None
    label: str = "final"
    logical_time: Decimal = Decimal(0)
    source_id: str = ""
    source_url: str = ""
    features: tuple[ContactFeature | DetectedContactFeature | ActiveFeature, ...] = ()


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
    overlays: frozenset[Overlay] = field(default_factory=lambda: frozenset({Overlay.CONTACTS}))
    title: str = "Square packing"
    description: str = "A square packing rendered with mathematical y coordinates upward."
    duration_seconds: Decimal = Decimal("4")
    width: int = 960
    hue_scheme: HueScheme = HueScheme.ANGLE
    shade_scheme: ShadeScheme = ShadeScheme.CONTACTS
    hue_count: int = 20
    shades_per_hue: int = 5
    shade_lightness_span: Decimal = Decimal("0.2")
    angle_tolerance_radians: Decimal = Decimal("1e-6")
    full_side_contact_tolerance: Decimal = Decimal("2e-6")


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
    check = frame.check
    check_passed = check is not None and check.passed
    formally_checked = check_passed and check is not None and check.kind is CheckKind.FORMAL
    for feature in frame.features:
        if not feature.feature_id.strip():
            raise ValueError("feature ID must be non-empty")
        if isinstance(feature, ActiveFeature):
            validate_scalar_source(feature.point.x)
            validate_scalar_source(feature.point.y)
            continue
        if isinstance(feature, DetectedContactFeature):
            if not check_passed:
                raise ValueError("detected contact features require a checked source geometry")
            for point in (feature.start, feature.end):
                validate_scalar_source(point.x)
                validate_scalar_source(point.y)
            if (feature.start.x.projected, feature.start.y.projected) == (
                feature.end.x.projected,
                feature.end.y.projected,
            ):
                raise ValueError("detected contact graph edge must be nondegenerate")
            if (
                feature.angle_tolerance_radians <= 0
                or not feature.angle_tolerance_radians.is_finite()
                or feature.contact_tolerance <= 0
                or not feature.contact_tolerance.is_finite()
            ):
                raise ValueError("detected contact tolerances must be finite and positive")
            expected_participants = 1 if feature.wall is not None else 2
            if len(feature.square_ids) != expected_participants:
                raise ValueError("detected contact participants do not match its kind")
            if (
                len(feature.square_ids) != len(set(feature.square_ids))
                or feature.square_ids != tuple(sorted(feature.square_ids))
                or any(square_id not in ids for square_id in feature.square_ids)
            ):
                raise ValueError(
                    "detected contact square IDs must be unique, known, and stable"
                )
            if feature.wall is None:
                if feature.normal is None or feature.residual is None:
                    raise ValueError("detected pair contact requires normal and residual")
                if feature.normal not in {"u-normal", "v-normal"}:
                    raise ValueError("detected pair normal must be u-normal or v-normal")
                if (
                    feature.residual < 0
                    or not feature.residual.is_finite()
                    or feature.residual > feature.contact_tolerance
                ):
                    raise ValueError("detected pair residual must lie within tolerance")
            elif feature.normal is not None or feature.residual is not None:
                raise ValueError("detected wall seating does not carry pair residual data")
            continue
        contact_points = (
            (feature.start,) if feature.end is None else (feature.start, feature.end)
        )
        for point in contact_points:
            for value in (point.x, point.y):
                validate_scalar_source(value)
                if value.kind not in (ScalarKind.RATIONAL, ScalarKind.EXACT):
                    raise ValueError("contact coordinates must have exact sources")
        if feature.end is not None and (
            feature.start.x.projected,
            feature.start.y.projected,
        ) == (feature.end.x.projected, feature.end.y.projected):
            raise ValueError("contact segment must be nondegenerate")
        if not formally_checked:
            raise ValueError("contact features require a successful formal check")
        if len(feature.square_ids) != len(set(feature.square_ids)):
            raise ValueError("contact square IDs must be unique")
        if feature.square_ids != tuple(sorted(feature.square_ids)):
            raise ValueError("contact square IDs must be stable")
        if any(square_id not in ids for square_id in feature.square_ids):
            raise ValueError("contact feature references an unknown square")
        expected_participants = 1 if feature.wall is not None else 2
        if len(feature.square_ids) != expected_participants:
            raise ValueError("contact participants do not match its geometry")
    if frame.evidence is EvidenceTier.NUMERICALLY_CHECKED and (
        not check_passed or check is None or check.kind is not CheckKind.NUMERICAL
    ):
        raise ValueError("numerically checked evidence requires a successful numerical check")
    if frame.evidence is EvidenceTier.NUMERICALLY_CHECKED and check is not None:
        missing = [
            field_name
            for field_name in ("arithmetic", "precision", "rounding", "tolerance")
            if not getattr(check, field_name).strip()
        ]
        if missing:
            raise ValueError("numerically checked evidence requires " + ", ".join(missing))
    if frame.evidence is EvidenceTier.CERTIFIED_UPPER_BOUND:
        if not formally_checked:
            raise ValueError("formal evidence requires a successful formal check")
        if check is not None and any(
            getattr(check, field_name).strip()
            for field_name in ("precision", "rounding", "tolerance")
        ):
            raise ValueError("formal evidence must not use precision or tolerance as assurance")
        formal_sources = [frame.container_side]
        formal_sources.extend(
            value
            for square in frame.squares
            for point in square.corners
            for value in (point.x, point.y)
        )
        if any(
            value.kind not in {ScalarKind.RATIONAL, ScalarKind.EXACT}
            for value in formal_sources
        ):
            raise ValueError("formal evidence requires rational or exact geometry sources")
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
    if spec.hue_count <= 0 or spec.shades_per_hue <= 0:
        raise ValueError("color hue and shade counts must be positive")
    if (
        not spec.shade_lightness_span.is_finite()
        or spec.shade_lightness_span < 0
        or spec.shade_lightness_span > Decimal("0.3")
    ):
        raise ValueError("color shade lightness span must be between 0 and 0.3")
    if not spec.angle_tolerance_radians.is_finite() or spec.angle_tolerance_radians <= 0:
        raise ValueError("color angle tolerance must be finite and positive")
    if (
        not spec.full_side_contact_tolerance.is_finite()
        or spec.full_side_contact_tolerance <= 0
    ):
        raise ValueError("full-side contact tolerance must be finite and positive")
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
        values += [
            value
            for frame in frames
            for feature in frame.features
            if isinstance(feature, ContactFeature)
            for point in (
                (feature.start,) if feature.end is None else (feature.start, feature.end)
            )
            for value in (point.x, point.y)
        ]
        if any(value.kind is ScalarKind.EXACT and not value.exact_source for value in values):
            raise ValueError("exact annotations require complete exact sources")
