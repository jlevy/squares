"""Replay the restricted free-square deduction and challenge its proof boundaries."""

from __future__ import annotations

import json
from dataclasses import replace
from fractions import Fraction as Q
from itertools import pairwise

import pytest

from devtools import check_n17_capacity_one_cover as cover
from devtools import check_n17_family_cell_audit as audit
from devtools.check_n17_endpoint_feasibility import Box


def test_exact_replay_and_cli_scope(capsys: pytest.CaptureFixture[str]) -> None:
    result = audit.check()
    assert result["passed"]
    assert result["forced_cell"] == "side-S2"
    assert result["worst_squared_distance"] == "409960561/423200000"
    assert result["squared_distance_margin"] == "13239439/423200000"
    assert len(result["pieces"]) == 11
    assert len(result["occupied_cells"]) == 16
    assert audit.main([]) == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed["scope"]["slider_box"] == {
        "a": ["0", "3/25"],
        "b": ["0", "3/40"],
        "z": ["-1/20", "1/40"],
    }
    assert printed["scope"]["core"] == "exact endpoint family; all labels except 6"
    assert "perturbed" in printed["limitations"]


def _section(vertices: tuple[cover.Point, ...], x: Q) -> tuple[Q, Q] | None:
    ys: list[Q] = []
    for start, end in zip(vertices, (*vertices[1:], vertices[0]), strict=True):
        if start[0] == end[0] == x:
            ys.extend((start[1], end[1]))
        elif start[0] != end[0] and min(start[0], end[0]) <= x <= max(start[0], end[0]):
            ys.append(start[1] + (x - start[0]) * (end[1] - start[1]) / (end[0] - start[0]))
    return (min(ys), max(ys)) if ys else None


def _covers_sections(cell: cover.Cell, pieces: list[audit.Piece]) -> bool:
    # Axis cuts introduce only polygon vertices as changes of vertical-section order.
    critical = sorted(
        {x for x, _ in cell.vertices} | {x for piece in pieces for x, _ in piece.vertices}
    )
    probes = sorted({*critical, *((left + right) / 2 for left, right in pairwise(critical))})
    for x in probes:
        expected = _section(cell.vertices, x)
        assert expected is not None
        intervals = sorted(
            interval
            for piece in pieces
            if (interval := _section(piece.vertices, x)) is not None
        )
        if not intervals:
            return False
        reached = expected[0]
        for low, high in intervals:
            if low > reached or low < expected[0] or high > expected[1]:
                return False
            reached = max(reached, high)
        if reached != expected[1]:
            return False
    return True


def test_piece_cover_includes_whole_cells_and_closed_cut_seams() -> None:
    cells = cover.build_cover(cover.UNIQUE_24)
    pieces = audit.closed_pieces(cells)
    for cell in cells:
        selected = [piece for piece in pieces if piece.cell == cell.name]
        if selected:
            assert _covers_sections(cell, selected)
    # Deleting the lower NE piece leaves an independently detected section gap.
    ne = next(cell for cell in cells if cell.name == "interior-NE")
    assert not _covers_sections(
        ne, [piece for piece in pieces if piece.cell == ne.name and piece.blocker == 16]
    )
    # The seams themselves belong to both adjacent branches.
    for name, axis, value in (
        ("interior-NE", 1, Q(29, 10)),
        ("side-W1", 1, Q(21, 10)),
        ("side-W1", 0, Q(1)),
        ("side-E2", 0, Q(37, 10)),
    ):
        selected = [piece for piece in pieces if piece.cell == name]
        seam_vertices = {
            vertex for piece in selected for vertex in piece.vertices if vertex[axis] == value
        }
        assert seam_vertices
        for vertex in seam_vertices:
            assert sum(audit.contains(piece.vertices, vertex) for piece in selected) >= 2


def test_rejects_changed_domain_bound_and_geometry() -> None:
    t, beta, _ = cover.load_root_box(cover.CERTIFICATE)
    point = cover.endpoint(t, beta)
    cells = cover.build_cover(cover.UNIQUE_24)
    for domain in (
        replace(cover.TRIANGLE, b=(Q(0), Q(1, 20))),
        replace(cover.TRIANGLE, z=(Q(-1, 8), Q(1, 16))),
        replace(cover.TRIANGLE, a=(Q(3, 25), Q(0))),
    ):
        with pytest.raises(ValueError, match="slider domain"):
            audit.replay(point, cells, domain=domain)
    bounds = dict(audit.PUBLISHED_BOUNDS)
    bounds["interior-NE:12"] = Q(9, 10)
    with pytest.raises(ValueError, match="published bound"):
        audit.replay(point, cells, published_bounds=bounds)
    bounds["interior-NE:12"] = Q(1)
    with pytest.raises(ValueError, match="non-strict bound"):
        audit.replay(point, cells, published_bounds=bounds)
    moved = list(point.centres)
    x, y = moved[11]
    moved[11] = x + Box.point(1), y
    with pytest.raises(ValueError, match="square 12 not contained"):
        audit.replay(replace(point, centres=tuple(moved)), cells)
    shifted = [
        replace(cell, vertices=tuple((x + 1, y) for x, y in cell.vertices))
        if cell.name == "interior-SW"
        else cell
        for cell in cells
    ]
    with pytest.raises(ValueError, match="published bound"):
        audit.replay(point, shifted)


def test_outward_centres_cover_full_slider_intervals_and_negative_rounding() -> None:
    t, beta, _ = cover.load_root_box(cover.CERTIFICATE)
    point = cover.endpoint(t, beta)
    boxes = audit.blocker_boxes(point, cover.TRIANGLE)
    # Interior and endpoint slider values are checked directly, without the interval
    # expression used to produce the centre boxes.
    for label, values, sign in ((11, cover.TRIANGLE.b, -1), (13, cover.TRIANGLE.z, 1)):
        low, high = values
        for slide in (low, (2 * low + high) / 3, (low + high) / 2, high):
            for axis in (0, 1):
                base = point.centres[label - 1][axis]
                direction = point.v[axis]
                candidates = [
                    centre + sign * vector * slide
                    for centre in (base.lo, base.hi)
                    for vector in (direction.lo, direction.hi)
                ]
                assert boxes[label][axis][0] <= min(candidates)
                assert max(candidates) <= boxes[label][axis][1]
    assert audit.round_outward(Box(Q(-10001, 100000), Q(-9999, 100000))) == (
        Q(-101, 1000),
        Q(-99, 1000),
    )
