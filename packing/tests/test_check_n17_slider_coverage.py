"""Exact controls for the H-268 slider-coverage checker."""

from __future__ import annotations

import math
import random
from fractions import Fraction as Q
from functools import cache

from devtools.check_n17_endpoint_feasibility import Box
from devtools.check_n17_slider_coverage import (
    LEGACY_DESIGN,
    Rect,
    Scene,
    SixBox,
    a_floor,
    along_v_rect,
    b_cover,
    b_floor,
    build_scene,
    cell_slide_range,
    endpoint_state,
    five_rect,
    rects_overlap,
    separation_lemma,
    six_cover,
    six_overlaps,
    stack,
    trig,
    trig_radius,
    z_ceiling,
)


@cache
def scene() -> Scene:
    return build_scene()


def _float_overlap(first: list[tuple[float, float]], second: list[tuple[float, float]]) -> bool:
    for polygon in (first, second):
        for index, (x0, y0) in enumerate(polygon):
            x1, y1 = polygon[(index + 1) % len(polygon)]
            nx, ny = y1 - y0, x0 - x1
            a = [nx * x + ny * y for x, y in first]
            b = [nx * x + ny * y for x, y in second]
            if max(a) <= min(b) + 1e-12 or max(b) <= min(a) + 1e-12:
                return False
    return True


def _square(x: float, y: float, phi: float) -> list[tuple[float, float]]:
    c, s = math.cos(phi), math.sin(phi)
    return [
        (x + i * c / 2 - j * s / 2, y + i * s / 2 + j * c / 2)
        for i, j in ((1, 1), (-1, 1), (-1, -1), (1, -1))
    ]


def test_rect_overlap_is_strict() -> None:
    unit = Rect(Q(0), Q(0), Q(1), Q(0), Q(1, 2), Q(1, 2))
    touching = Rect(Q(1), Q(0), Q(1), Q(0), Q(1, 2), Q(1, 2))
    pressed = Rect(Q(99, 100), Q(0), Q(1), Q(0), Q(1, 2), Q(1, 2))
    diamond = Rect(Q(11, 10), Q(0), Q(3, 5), Q(4, 5), Q(1, 2), Q(1, 2))
    kissing = Rect(Q(6, 5), Q(0), Q(3, 5), Q(4, 5), Q(1, 2), Q(1, 2))
    assert not rects_overlap(unit, touching)
    assert rects_overlap(unit, pressed)
    # A turned square reaches 7/10 along e_x: it overlaps at 11/10 and touches at 6/5.
    assert rects_overlap(unit, diamond)
    assert not rects_overlap(unit, kissing)


def test_scene_binds_the_cell_and_the_non_sliders() -> None:
    built = scene()
    # The unique-state design's side-S2 is the tabbed one shifted left by 1/100.
    assert built.cell == (Q(4021, 1500), Q(1693, 500), Q(1, 2), Q(1411, 1000))
    legacy = build_scene(design=LEGACY_DESIGN)
    assert legacy.cell == (Q(1009, 375), Q(849, 250), Q(1, 2), Q(1411, 1000))
    assert sorted(built.fixed) == [1, 2, 3, 4, 7, 8, 9, 10, 12, 14, 15, 16, 17]
    assert built.half == Q(1, 2) - Q(2, 5000)
    # The slider rectangles keep their squeezing face: 5's left face at a1, 13's at z2.
    five = five_rect(built, (Q(1, 4), Q(3, 4)))
    assert five is not None
    assert five.p < Q(1, 4) + Q(1, 1000)
    thirteen = along_v_rect(built, 13, (Q(-1, 2), Q(0)), 1)
    assert thirteen is not None
    assert thirteen.q < Q(1, 4) + Q(1, 1000)


def test_six_overlap_is_sound_on_samples() -> None:
    rng = random.Random(268)
    obstacle = Rect(Q(0), Q(0), Q(3, 5), Q(4, 5), Q(1, 2), Q(1, 2))
    corners = [(float(x), float(y)) for x, y in obstacle.vertices()]
    corners = [corners[0], corners[1], corners[3], corners[2]]
    checked = 0
    for _ in range(300):
        t0 = Q(rng.randrange(0, 16), 16)
        x0 = Q(rng.randrange(-24, 24), 16)
        y0 = Q(rng.randrange(-24, 24), 16)
        box = SixBox((t0, t0 + Q(1, 16)), (x0, x0 + Q(1, 16)), (y0, y0 + Q(1, 16)))
        cos, sin = trig(box.t)
        if not six_overlaps(obstacle, box, cos, sin):
            continue
        checked += 1
        for _ in range(5):
            tau = rng.uniform(float(box.t[0]), float(box.t[1]))
            phi = 2 * math.atan(tau)
            x = rng.uniform(float(box.x[0]), float(box.x[1]))
            y = rng.uniform(float(box.y[0]), float(box.y[1]))
            assert _float_overlap(_square(x, y, phi), corners)
    assert checked > 20


def test_squeeze_closes_inside_the_cell() -> None:
    built = scene()
    five = five_rect(built, (Q(1, 4), Q(1, 2)))
    thirteen = along_v_rect(built, 13, (Q(-1, 4), Q(1, 16)), 1)
    assert five is not None
    assert thirteen is not None
    result = six_cover([*built.fixed.values(), five, thirteen], built.cell, built.outer)
    assert result.closed


def test_control_whole_box_cell_is_refused() -> None:
    built = scene()
    lo, hi = built.outer
    whole = (lo + Q(1, 2), hi - Q(1, 2), lo + Q(1, 2), hi - Q(1, 2))
    five = five_rect(built, (Q(1), Q(9, 8)))
    thirteen = along_v_rect(built, 13, (Q(-1, 4), Q(1, 16)), 1)
    assert five is not None
    assert thirteen is not None
    obstacles = [*built.fixed.values(), five, thirteen]
    assert six_cover(obstacles, built.cell, built.outer).closed
    refused = six_cover(obstacles, whole, built.outer, node_limit=20_000)
    assert not refused.closed
    assert refused.witness is not None
    assert refused.witness.x[0] > built.cell[1]


def test_b_bound_needs_the_tight_z_bound() -> None:
    built = scene()
    assert b_cover(built, Q(1, 12), Q(-1, 20)).passed
    loose = b_cover(built, Q(1, 12), Q(-1, 8))
    assert not loose.passed
    assert loose.failure is not None


def test_endpoint_state_puts_6_in_s2_and_13_in_s1() -> None:
    state = endpoint_state(scene().design)
    assert state[6].name == "side-S2"
    assert state[13].name == "side-S1"
    assert state[11].name == "interior-W"


def test_a_floor_is_the_right_wall() -> None:
    face = a_floor(scene())
    assert face.passed
    assert face.record["a_min"] == "0"


def test_separation_lemma_refuses_lateral_and_wrong_side() -> None:
    angles = trig_radius(Q(1, 5000))
    near = Box(Q(1), Q(1))
    assert separation_lemma(Box(Q(-3, 10), Q(-1, 4)), near, angles)
    # A lateral offset of 1 lets a u-type axis separate; a positive one flips the minimiser.
    assert not separation_lemma(Box(Q(-1), Q(-1)), near, angles)
    assert not separation_lemma(Box(Q(1, 4), Q(3, 10)), near, angles)
    assert not separation_lemma(Box(Q(-3, 10), Q(-1, 4)), Box(Q(-1), Q(1)), angles)


def _pose_square(
    centre: tuple[float, float], frame: float, turn: float
) -> list[tuple[float, float]]:
    return _square(centre[0], centre[1], frame + turn)


def test_b_floor_is_attained_by_touching_squares() -> None:
    built = scene()
    face, exact = b_floor(built, Q(3, 40))
    assert face.passed
    r = float(built.radius)
    b_star = float(exact.lo)
    assert -1.6850 * r < b_star < -1.6849 * r
    pair = stack(built, 9, 11)
    assert float(pair.gap.lo) == 1.0
    c, s = float(built.poses[11].ux.lo), float(built.poses[11].uy.lo)
    frame = math.atan2(s, c)
    u, v = (c, s), (-s, c)
    c11 = (float(built.poses[11].cx.lo), float(built.poses[11].cy.lo))
    c9 = (float(built.poses[9].cx.lo) - r, float(built.poses[9].cy.lo) + r)

    def eleven(b: float) -> list[tuple[float, float]]:
        centre = (c11[0] + r * u[0] - b * v[0], c11[1] + r * u[1] - b * v[1])
        return _pose_square(centre, frame, r)

    nine = _pose_square(c9, frame, r)
    assert not _float_overlap(nine, eleven(b_star + 1e-9))
    assert _float_overlap(nine, eleven(b_star - 1e-8))


def test_z_ceiling_and_the_cell_of_13() -> None:
    built = scene()
    _, exact = b_floor(built, Q(3, 40))
    face, z_star = z_ceiling(built, exact.lo, Q(3, 40), Q(-1, 20), Q(1, 32))
    assert face.passed
    assert 0.0241 < float(z_star.lo) < float(z_star.hi) < 0.02411
    state = endpoint_state(built.design)
    u = (built.poses[13].ux, built.poses[13].uy)
    span = cell_slide_range(built.poses[13], state[13], built.v, u, built.radius)
    assert span is not None
    assert Q(1, 40) < span[1] < Q(1, 16)
