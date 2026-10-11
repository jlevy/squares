"""Fine hull proposals remain exact-checker inputs, with all coarse fallbacks intact."""

from __future__ import annotations

import copy
from typing import Any

import pytest

from sqpack.hull_kernel import RefusalError, node, producer
from sqpack.hull_kernel.frame import Frame, make_frame
from sqpack.hull_kernel.geometry import Halfplane, Point, Polygon
from sqpack.hull_kernel.induction import encode, forbidden_regions, hull
from sqpack.hull_kernel.rational import Q

NORMALS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def box(x0: Q, x1: Q, y0: Q, y1: Q) -> Polygon:
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def fixture() -> tuple[Frame, Polygon, list[Halfplane]]:
    frame = make_frame(
        name="unit-hull-pull",
        cap=Q(2),
        length=Q(2),
        cells=[box(Q(3, 4), Q(5, 4), Q(3, 4), Q(5, 4))],
        cell_names=["centre"],
        occupancy=1,
        action_names=("r0",),
    )
    original = box(Q(1, 3), Q(4, 3), Q(1, 3), Q(4, 3))
    planes = [(Q(a), Q(b), max(a * x + b * y for x, y in original)) for a, b in NORMALS]
    return frame, original, planes


def compression_packet(original: Polygon) -> dict[str, Any]:
    points, witnesses = producer.compress(original)
    return {
        "compression_source_hull": encode(hull(original)),
        "inner_grid_compression": {
            "denominator": producer.GRID,
            "vertices": encode(points),
            "original_vertices": len(original),
            "retained_vertices": len(points),
            "witnesses": witnesses,
        },
    }


def face_recession(outer: Polygon, inner: Polygon) -> list[Q]:
    return [
        max(a * x + b * y for x, y in outer) - max(a * x + b * y for x, y in inner)
        for a, b in NORMALS
    ]


def forbidden_link(owned: Polygon) -> Polygon:
    core = box(Q(-1, 4), Q(1, 4), Q(-1, 4), Q(1, 4))
    return forbidden_regions({1: owned}, 0, core)[0]


def test_non_grid_compression_is_reconstructed_by_the_unchanged_checker() -> None:
    _, original, _ = fixture()
    packet = compression_packet(original)
    proved = node.compression_points(packet, [], original)
    assert proved == node.points(packet["inner_grid_compression"]["vertices"])
    assert len(proved) == 4
    assert all(
        (coordinate * producer.GRID).denominator == 1 for p in proved for coordinate in p
    )
    assert 0 < max(face_recession(original, hull(proved))) < Q(1, 100_000)


@pytest.mark.parametrize("field", ["weights", "point"])
def test_a_tampered_compression_is_refused(field: str) -> None:
    _, original, _ = fixture()
    packet = copy.deepcopy(compression_packet(original))
    packet["inner_grid_compression"]["witnesses"][0][field][0] = "2"
    with pytest.raises(RefusalError, match=r"convex combination|convex-combination"):
        node.compression_points(packet, [], original)


def test_already_grid_vertices_and_their_unit_witnesses_are_unchanged() -> None:
    original = box(Q(0), Q(1), Q(0), Q(1))
    points, witnesses = producer.compress(original)
    assert points == original
    assert [witness["indices"] for witness in witnesses] == [[0], [1], [2], [3]]
    assert all(witness["weights"] == ["1"] for witness in witnesses)


def test_near_boundary_rounding_rejects_fine_points_then_uses_coarse_fallbacks(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = box(Q(1, 3), Q(1, 3) + Q(1, 1000), Q(1, 3), Q(4, 3))
    fine_packet = compression_packet(original)
    fine = node.compression_points(fine_packet, [], original)
    cx = sum((x for x, _ in original), Q()) / len(original)
    cy = sum((y for _, y in original), Q()) / len(original)
    proposals: list[Point] = [
        (
            Q(round((x + (cx - x) * producer.FINE_HULL_PULL) * producer.GRID), producer.GRID),
            Q(round((y + (cy - y) * producer.FINE_HULL_PULL) * producer.GRID), producer.GRID),
        )
        for x, y in original
    ]
    assert all(point not in fine for point in proposals)
    assert all(point[0] < original[0][0] or point[0] > original[1][0] for point in proposals)
    monkeypatch.setattr(producer, "FINE_HULL_PULL", Q(1, 2**12))
    assert fine == producer.compress(original)[0]
    node.compression_points(fine_packet, [], original)


def test_kernel_retains_every_original_candidate_and_checks_planes_exactly(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    frame, original, planes = fixture()
    fine = producer.kernel_points(frame, planes)
    assert all(a * x + b * y <= c for x, y in fine for a, b, c in planes)
    monkeypatch.setattr(producer, "FINE_HULL_PULL", Q(1, 2**12))
    old = producer.kernel_points(frame, planes)
    assert set(old) <= set(fine)
    assert max(face_recession(original, hull(old))) > Q(1, 100_000)
    assert 0 < max(face_recession(original, hull(fine))) < Q(1, 100_000)
    link_gaps = face_recession(forbidden_link(original), forbidden_link(hull(fine)))
    assert link_gaps == face_recession(original, hull(fine))
