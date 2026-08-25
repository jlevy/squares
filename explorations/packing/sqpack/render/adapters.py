"""Adapters from repository packing records into the rendering model."""

from __future__ import annotations

import math
from collections.abc import Sequence
from decimal import Decimal, localcontext
from fractions import Fraction

from sqpack.field import FieldElement
from sqpack.packings import gobel10, trump11
from sqpack.packings.n5_equal_side_face import build_equal_side_face, centres_at
from sqpack.render.model import (
    EvidenceTier,
    PackingFrame,
    PackingTrajectory,
    Point2,
    RigidPose,
    SquareGeometry,
    TrajectoryKind,
    VerificationSummary,
)
from sqpack.render.numbers import scalar_from_decimal, scalar_from_exact, scalar_from_float
from sqpack.verify import corners_from_poses, exact_sign, verify_packing


def _field_source(value: FieldElement) -> str:
    terms = []
    for power, coefficient in enumerate(value.coeffs):
        if coefficient:
            terms.append(f"({coefficient})*alpha^{power}")
    return " + ".join(terms) or "0"


def _field_scalar(value: FieldElement):
    value.field.refine_to(48)
    lower, upper = value.field.root_bounds()
    root = (lower + upper) / 2
    projected = Fraction(0)
    for coefficient in reversed(value.coeffs):
        projected = projected * root + coefficient
    with localcontext() as context:
        context.prec = 48
        decimal_value = Decimal(projected.numerator) / Decimal(projected.denominator)
    return scalar_from_exact(_field_source(value), decimal_value)


def _normalize_pose(values: Sequence[float | Decimal | str], label: str) -> tuple:
    scalars = []
    for index, value in enumerate(values):
        if isinstance(value, bool):
            raise TypeError(f"invalid {label}[{index}]: booleans are not numbers")
        try:
            scalars.append(
                scalar_from_float(value)
                if isinstance(value, float)
                else scalar_from_decimal(value)
            )
        except (TypeError, ValueError) as error:
            raise ValueError(f"invalid {label}[{index}]") from error
    return tuple(scalars)


def frame_from_pose_arrays(
    side: float | Decimal | str,
    x: Sequence[float | Decimal | str],
    y: Sequence[float | Decimal | str],
    theta: Sequence[float | Decimal | str],
    *,
    label: str = "final",
    logical_time: Decimal = Decimal(0),
    evidence: EvidenceTier = EvidenceTier.CANDIDATE,
    verification: VerificationSummary | None = None,
    source_id: str = "pose-arrays",
    source_url: str = "",
) -> PackingFrame:
    if not (len(x) == len(y) == len(theta)) or not x:
        raise ValueError("pose arrays must be non-empty and have equal lengths")
    xs, ys, angles = (
        _normalize_pose(x, "x"),
        _normalize_pose(y, "y"),
        _normalize_pose(theta, "theta"),
    )
    float_corners = corners_from_poses(
        [float(value.projected) for value in xs],
        [float(value.projected) for value in ys],
        [float(value.projected) for value in angles],
    )
    squares = []
    for index, corners in enumerate(float_corners):
        points = tuple(
            Point2(scalar_from_float(px), scalar_from_float(py)) for px, py in corners
        )
        squares.append(
            SquareGeometry(
                f"square-{index:02d}",
                points,
                RigidPose(Point2(xs[index], ys[index]), angles[index]),
                str(index + 1),
            )
        )
    side_scalar = (
        scalar_from_float(side) if isinstance(side, float) else scalar_from_decimal(side)
    )
    return PackingFrame(
        side_scalar,
        tuple(squares),
        evidence,
        verification,
        label,
        logical_time,
        source_id,
        source_url,
    )


def _enclosing_side(x: Sequence[float], y: Sequence[float], theta: Sequence[float]) -> float:
    corners = corners_from_poses(x, y, theta)
    values = [coordinate for square in corners for point in square for coordinate in point]
    return max(values) - min(values)


def frames_from_basin_event(event: dict[str, object]) -> tuple[PackingFrame, PackingFrame]:
    if event.get("contract") != "packing.squares:BasinEvent/v3":
        raise ValueError("renderer accepts BasinEvent/v3 only")
    start = event.get("start")
    endpoint = event.get("endpoint")
    if not isinstance(start, dict) or not isinstance(endpoint, dict):
        raise TypeError("basin event requires start and endpoint poses")
    for pose in (start, endpoint):
        if not all(isinstance(pose.get(key), list) for key in ("x", "y", "theta")):
            raise ValueError("basin event pose arrays are malformed")
    sx, sy, st = start["x"], start["y"], start["theta"]
    ex, ey, et = endpoint["x"], endpoint["y"], endpoint["theta"]
    regime = event.get("regime")
    start_side = regime.get("start_side") if isinstance(regime, dict) else None
    if not isinstance(start_side, (int, float, Decimal)):
        start_side = _enclosing_side(sx, sy, st)
    final_side = endpoint.get("side") if isinstance(endpoint, dict) else None
    if not isinstance(final_side, (int, float, Decimal, str)):
        raise TypeError("basin endpoint requires a side")
    source_url = str(regime.get("source_url", "")) if isinstance(regime, dict) else ""
    source_id = (
        str(regime.get("source_id", "BasinEvent/v3"))
        if isinstance(regime, dict)
        else "BasinEvent/v3"
    )
    verification_record = event.get("verification")
    verification = None
    if isinstance(verification_record, dict) and verification_record.get("valid") is True:
        verification = VerificationSummary(
            valid=True,
            method=str(verification_record.get("oracle", "numerical")),
            detail="retained BasinEvent/v3 endpoint",
        )
    first = frame_from_pose_arrays(
        start_side,
        sx,
        sy,
        st,
        label="source perturbation",
        source_id=source_id,
        source_url=source_url,
    )
    last = frame_from_pose_arrays(
        final_side,
        ex,
        ey,
        et,
        label="returned endpoint",
        logical_time=Decimal(1),
        evidence=EvidenceTier.CANDIDATE,
        verification=verification,
        source_id=source_id,
        source_url=source_url,
    )
    return first, last


def frame_from_gobel10() -> PackingFrame:
    pose = gobel10.pose()
    return frame_from_pose_arrays(
        pose["side"],
        pose["x"],
        pose["y"],
        pose["theta"],
        evidence=EvidenceTier.CANDIDATE,
        label="Göbel n=10 source construction",
        source_id=gobel10.SOURCE_ID,
        source_url=gobel10.SOURCE_URL,
    )


def frame_from_trump11() -> PackingFrame:
    squares, side, _field = trump11.build()
    report = verify_packing(squares, side, sign=exact_sign)
    geometries = []
    for index, corners in enumerate(squares):
        points = tuple(Point2(_field_scalar(x), _field_scalar(y)) for x, y in corners)
        geometries.append(SquareGeometry(f"square-{index:02d}", points, label=str(index + 1)))
    return PackingFrame(
        _field_scalar(side),
        tuple(geometries),
        EvidenceTier.CERTIFIED_UPPER_BOUND,
        VerificationSummary(
            report.valid, "exact-number-field", "all pair and boundary predicates"
        ),
        "Trump n=11",
        source_id="trump11-exact-q-u",
    )


def _face_square(face, centre, *, diagonal: bool):
    q, root = face.field.rational, face.field.alpha
    if diagonal:
        u, v = (root / 2, root / 2), (-root / 2, root / 2)
    else:
        u, v = (q(1), q(0)), (q(0), q(1))
    cx, cy = centre
    return tuple(
        (cx + sx * u[0] / 2 + sy * v[0] / 2, cy + sx * u[1] / 2 + sy * v[1] / 2)
        for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))
    )


def trajectory_from_n5_equal_side_face() -> PackingTrajectory:
    face = build_equal_side_face()
    parameters = (face.field.zero, face.delta / 2, face.delta)
    frames = []
    for index, parameter in enumerate(parameters):
        centres = centres_at(face, parameter)
        exact_squares = [
            _face_square(face, centre, diagonal=square_index >= 3)
            for square_index, centre in enumerate(centres)
        ]
        report = verify_packing(exact_squares, face.side, sign=exact_sign)
        geometries = []
        for square_index, (centre, corners) in enumerate(
            zip(centres, exact_squares, strict=True)
        ):
            angle = 0.0 if square_index < 3 else math.pi / 4
            points = tuple(Point2(_field_scalar(x), _field_scalar(y)) for x, y in corners)
            geometries.append(
                SquareGeometry(
                    f"square-{square_index:02d}",
                    points,
                    RigidPose(
                        Point2(_field_scalar(centre[0]), _field_scalar(centre[1])),
                        scalar_from_exact(
                            "0" if square_index < 3 else "pi/4", Decimal(repr(angle))
                        ),
                    ),
                    str(square_index + 1),
                )
            )
        frames.append(
            PackingFrame(
                _field_scalar(face.side),
                tuple(geometries),
                EvidenceTier.CERTIFIED_UPPER_BOUND,
                VerificationSummary(report.valid, "exact-q-sqrt2", "certified equal-side face"),
                ("endpoint A", "exact midpoint", "endpoint B")[index],
                Decimal(index) / 2,
                "exp-033-h-023-equal-side-face",
            )
        )
    return PackingTrajectory(
        tuple(frames),
        TrajectoryKind.CERTIFIED,
        "Exact n=5 equal-side feasible face",
        "Every parameter in [0, 3*sqrt(2)/2-2] satisfies the retained exact cell certificate.",
    )
