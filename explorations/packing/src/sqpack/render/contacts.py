"""Exact contact extraction for certified square-packing constructions."""

from __future__ import annotations

from collections.abc import Callable, Sequence

from sqpack.field import FieldElement
from sqpack.render.model import (
    ContactFeature,
    ContainerWall,
    Point2,
    ScalarSource,
)
from sqpack.verify import Report, exact_sign, verify_packing

ExactPoint = tuple[FieldElement, FieldElement]
ExactSquare = Sequence[ExactPoint]
ContactGeometry = tuple[ExactPoint, ExactPoint | None]


def _same_point(first: ExactPoint, second: ExactPoint) -> bool:
    return first[0] == second[0] and first[1] == second[1]


def _cross(origin: ExactPoint, first: ExactPoint, second: ExactPoint) -> FieldElement:
    return (first[0] - origin[0]) * (second[1] - origin[1]) - (first[1] - origin[1]) * (
        second[0] - origin[0]
    )


def _point_on_segment(point: ExactPoint, start: ExactPoint, end: ExactPoint) -> bool:
    if not _cross(start, end, point).is_zero():
        return False
    dot = (point[0] - start[0]) * (point[0] - end[0]) + (point[1] - start[1]) * (
        point[1] - end[1]
    )
    return exact_sign(dot) <= 0


def _edges(square: ExactSquare):
    return tuple((square[index], square[(index + 1) % 4]) for index in range(4))


def _element_key(value: FieldElement) -> tuple[tuple[int, int], ...]:
    return tuple(
        (coefficient.numerator, coefficient.denominator) for coefficient in value.coeffs
    )


def _point_key(point: ExactPoint):
    return _element_key(point[0]), _element_key(point[1])


def _deduplicate_points(points: Sequence[ExactPoint]) -> tuple[ExactPoint, ...]:
    unique: list[ExactPoint] = []
    for point in points:
        if not any(_same_point(point, existing) for existing in unique):
            unique.append(point)
    return tuple(sorted(unique, key=_point_key))


def _pair_contact_geometry(first: ExactSquare, second: ExactSquare) -> ContactGeometry:
    intersections = []
    first_edges = _edges(first)
    second_edges = _edges(second)
    for first_start, first_end in first_edges:
        for second_start, second_end in second_edges:
            intersections.extend(
                point
                for point, start, end in (
                    (first_start, second_start, second_end),
                    (first_end, second_start, second_end),
                    (second_start, first_start, first_end),
                    (second_end, first_start, first_end),
                )
                if _point_on_segment(point, start, end)
            )
    points = _deduplicate_points(intersections)
    if not points:
        raise ValueError("touching pair has no exact boundary intersection")
    if len(points) == 1:
        return points[0], None
    if len(points) != 2:
        raise ValueError("touching pair has inconsistent contact geometry")
    if not any(
        all(_point_on_segment(point, start, end) for point in points)
        for start, end in first_edges
    ) or not any(
        all(_point_on_segment(point, start, end) for point in points)
        for start, end in second_edges
    ):
        raise ValueError("touching pair has two disjoint contact points")
    if _same_point(*points):
        raise ValueError("contact segment must be nondegenerate")
    return points[0], points[1]


def _wall_value(point: ExactPoint, side: FieldElement, wall: ContainerWall) -> FieldElement:
    return {
        ContainerWall.LEFT: point[0],
        ContainerWall.RIGHT: side - point[0],
        ContainerWall.BOTTOM: point[1],
        ContainerWall.TOP: side - point[1],
    }[wall]


def _wall_contact_geometry(
    square: ExactSquare, side: FieldElement, wall: ContainerWall
) -> ContactGeometry | None:
    indices = []
    for index, point in enumerate(square):
        value = _wall_value(point, side, wall)
        if value.is_zero():
            indices.append(index)
            continue
        sign = exact_sign(value)
        if sign < 0:
            raise ValueError("square lies outside the certified container")
    if not indices:
        return None
    if len(indices) == 1:
        return square[indices[0]], None
    if len(indices) != 2 or (indices[0] - indices[1]) % 4 not in (1, 3):
        raise ValueError("square has inconsistent wall-contact geometry")
    points = _deduplicate_points((square[indices[0]], square[indices[1]]))
    if len(points) != 2:
        raise ValueError("wall-contact segment must be nondegenerate")
    return points[0], points[1]


def _project_geometry(
    geometry: ContactGeometry, scalar: Callable[[FieldElement], ScalarSource]
) -> tuple[Point2, Point2 | None]:
    start, end = geometry
    projected_start = Point2(scalar(start[0]), scalar(start[1]))
    projected_end = None if end is None else Point2(scalar(end[0]), scalar(end[1]))
    return projected_start, projected_end


def contact_features_from_exact(
    squares: Sequence[ExactSquare],
    side: FieldElement,
    *,
    square_ids: Sequence[str],
    scalar: Callable[[FieldElement], ScalarSource],
    report: Report | None = None,
) -> tuple[ContactFeature, ...]:
    """Return stable wall and pair contacts certified in the source number field."""
    ids = tuple(square_ids)
    if len(squares) != len(ids) or not squares:
        raise ValueError("contact extraction requires one stable ID per square")
    if len(ids) != len(set(ids)) or ids != tuple(sorted(ids)):
        raise ValueError("contact extraction requires unique, stable square IDs")
    exact_report = report or verify_packing(squares, side, sign=exact_sign)
    if not exact_report.valid or exact_report.n != len(squares):
        raise ValueError("contact extraction requires a valid exact packing report")

    features = []
    wall_coordinate_count = 0
    for square_id, square in zip(ids, squares, strict=True):
        if len(square) != 4:
            raise ValueError("contact extraction requires four-corner squares")
        for wall in ContainerWall:
            geometry = _wall_contact_geometry(square, side, wall)
            if geometry is None:
                continue
            start, end = _project_geometry(geometry, scalar)
            wall_coordinate_count += 1 if end is None else 2
            features.append(
                ContactFeature(
                    f"contact-wall-{square_id}-{wall.value}",
                    start,
                    (square_id,),
                    end=end,
                    wall=wall,
                )
            )
    if wall_coordinate_count != exact_report.container_contacts:
        raise ValueError("wall contacts do not match the exact verifier report")

    touching_pairs = tuple(exact_report.touching_pair_indices)
    if (
        len(touching_pairs) != exact_report.touching_pairs
        or len(touching_pairs) != len(set(touching_pairs))
        or any(
            first < 0 or second >= len(squares) or first >= second
            for first, second in touching_pairs
        )
    ):
        raise ValueError("exact verifier report has inconsistent touching-pair indices")
    for first, second in touching_pairs:
        start, end = _project_geometry(
            _pair_contact_geometry(squares[first], squares[second]), scalar
        )
        features.append(
            ContactFeature(
                f"contact-pair-{ids[first]}-{ids[second]}",
                start,
                (ids[first], ids[second]),
                end=end,
            )
        )
    return tuple(sorted(features, key=lambda feature: feature.feature_id))
