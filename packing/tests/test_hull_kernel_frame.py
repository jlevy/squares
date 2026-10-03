"""Hull-kernel frames: n11's half-turn and n17's D4, built from their covers or refused."""

from __future__ import annotations

import copy
import itertools
from collections.abc import Sequence
from typing import Any

import pytest

from devtools import check_hull_kernel_mask0 as tool
from devtools import check_n11_optimality_field_mask0 as frozen
from devtools import check_n17_capacity_one_cover as cover_tool
from sqpack.hull_kernel import Frame, RefusalError, make_frame, n11, orbit_representatives
from sqpack.hull_kernel.frame import D4_ACTIONS, apply_matrix, d4_matrix
from sqpack.hull_kernel.rational import Q, as_fraction


@pytest.fixture(scope="module")
def n11_cover() -> dict[str, Any]:
    _, _, cover = tool.load_sources()
    return cover


@pytest.fixture(scope="module")
def n17_frame() -> Frame:
    return tool.n17_unique_frame()


def test_d4_matrices_follow_the_cover_tool_convention() -> None:
    point = (Q(1, 3), Q(5, 7))
    for action in D4_ACTIONS:
        image = apply_matrix(d4_matrix(action), Q(cover_tool.CENTRE), point)
        assert image == cover_tool.d4_apply(
            action, (as_fraction(point[0]), as_fraction(point[1]))
        )


def test_the_n11_frame_is_the_frozen_checkers_geometry(n11_cover: dict[str, Any]) -> None:
    frame = n11.frame_from_cover(n11_cover)
    assert frame.cap == frozen.U
    assert frame.length == frozen.L
    assert frame.scale == frozen.B
    for owner in range(16):
        assert frame.cell(owner) == frozen.cell_vertices(n11_cover, owner)
        normalised = [frozen.point(v) for v in n11_cover["cells"][owner]["vertices"]]
        assert frame.world(owner) == [
            (frozen.B / 2 + (frozen.L - frozen.B) * x, frozen.B / 2 + (frozen.L - frozen.B) * y)
            for x, y in normalised
        ]
    assert frame.actions[1].permutation == tuple(15 - j for j in range(16))
    assert len(frame.representatives) == 2184
    assert [list(state) for state in frame.representatives] == n11_cover[
        "canonical_eleven_cell_subsets"
    ]
    assert frame.cells_reaching_diameter_one() == ()


def test_a_perturbed_n11_cover_is_refused(n11_cover: dict[str, Any]) -> None:
    moved = copy.deepcopy(n11_cover)
    x, y = moved["cells"][0]["vertices"][1]
    moved["cells"][0]["vertices"][1] = [str(Q(x) + Q(1, 10**30)), y]
    with pytest.raises(RefusalError, match="cell 0: its image is not a cell"):
        n11.frame_from_cover(moved)
    relabelled = copy.deepcopy(n11_cover)
    relabelled["symmetry_cell_involution"][0], relabelled["symmetry_cell_involution"][1] = (
        14,
        15,
    )
    with pytest.raises(RefusalError, match="involution is not the geometric half-turn"):
        n11.frame_from_cover(relabelled)


def test_the_n17_frame_builds_with_24_cells_and_43593_orbit_representatives(
    n17_frame: Frame,
) -> None:
    cells = cover_tool.build_cover(cover_tool.UNIQUE_24)
    assert len(n17_frame.cells) == 24
    assert n17_frame.cap == Q(1169, 250)
    assert n17_frame.scale == 1
    assert n17_frame.cell_names == tuple(cell.name for cell in cells)
    permutations = cover_tool.d4_permutations(cells)
    assert permutations is not None
    assert {action.name: list(action.permutation) for action in n17_frame.actions} == (
        permutations
    )
    representatives = n17_frame.representatives
    assert len(representatives) == 43593
    assert cover_tool.burnside(permutations)["orbits"] == 43593
    assert len(set(representatives)) == len(representatives)
    assert list(representatives) == sorted(representatives)
    for state in representatives[::997]:
        assert len(state) == 17
        assert state == min(n17_frame.image(action, state) for action in n17_frame.actions)


def test_a_diameter_argument_refuses_every_n17_corner_and_side_cell(n17_frame: Frame) -> None:
    assert set(n17_frame.cells_reaching_diameter_one()) == {
        name for name in n17_frame.cell_names if not name.startswith("interior-")
    }
    assert len(n17_frame.cells_reaching_diameter_one()) == 16


def test_a_three_cell_pattern_has_exactly_eight_images(n17_frame: Frame) -> None:
    names = n17_frame.cell_names
    pattern = tuple(
        sorted(names.index(name) for name in ("corner-SW", "side-S0", "interior-S"))
    )
    images = {n17_frame.image(action, pattern) for action in n17_frame.actions}
    assert len(images) == 8
    # f3 reflects x and then turns three quarters: (x, y) -> (y, x), the main diagonal.
    diagonal = next(action for action in n17_frame.actions if action.name == "f3")
    assert {names[cell] for cell in n17_frame.image(diagonal, pattern)} == {
        "corner-SW",
        "side-W0",
        "interior-W",
    }


def test_orbit_representatives_agree_with_brute_force(n17_frame: Frame) -> None:
    permutations = [action.permutation for action in n17_frame.actions]
    for size in (3, 21):
        brute = sorted(
            {
                min(tuple(sorted(p[cell] for cell in state)) for p in permutations)
                for state in itertools.combinations(range(24), size)
            }
        )
        assert list(orbit_representatives(24, size, permutations)) == brute


def test_a_cell_set_that_d4_does_not_preserve_is_refused(n17_frame: Frame) -> None:
    def build(cells: Sequence[Sequence[tuple[Q, Q]]], names: Sequence[str]) -> Frame:
        return make_frame(
            name="broken",
            cap=n17_frame.cap,
            length=n17_frame.length,
            cells=cells,
            cell_names=names,
            occupancy=17,
            action_names=D4_ACTIONS,
        )

    cells, names = list(n17_frame.cells), list(n17_frame.cell_names)
    with pytest.raises(RefusalError, match="its image is not a cell"):
        build(cells[:-1], names[:-1])
    outside = [*cells[:-1], tuple((x, y - Q(3)) for x, y in cells[-1])]
    with pytest.raises(RefusalError, match="leaves the centre box"):
        build(outside, names)
    with pytest.raises(RefusalError, match="first action must be the identity"):
        make_frame(
            name="unordered",
            cap=n17_frame.cap,
            length=n17_frame.length,
            cells=cells,
            cell_names=names,
            occupancy=17,
            action_names=("r1", "r0", "r2", "r3"),
        )


def test_the_centred_box_is_n11s_wall_box_without_a_capture_cap(
    n11_cover: dict[str, Any],
) -> None:
    frame = n11.frame_from_cover(n11_cover)
    h = Q(3, 7)
    assert frame.centre_bounds(h) == (h, frozen.U - h)
    assert frame.field_centre_bounds(h) == (frozen.B * h, frozen.L - frozen.B * h)
    capped = make_frame(
        name="n11-captured",
        cap=frame.cap,
        length=frame.length,
        cells=frame.cells,
        cell_names=frame.cell_names,
        occupancy=11,
        action_names=("r0", "r2"),
        capture_cap=frame.cap - Q(1, 10),
    )
    assert capped.centre_bounds(h) == (Q(1, 20) + h, frame.cap - Q(1, 20) - h)
    with pytest.raises(RefusalError, match="capture cap"):
        make_frame(
            name="n11-overcapped",
            cap=frame.cap,
            length=frame.length,
            cells=frame.cells,
            cell_names=frame.cell_names,
            occupancy=11,
            action_names=("r0", "r2"),
            capture_cap=frame.cap + 1,
        )
