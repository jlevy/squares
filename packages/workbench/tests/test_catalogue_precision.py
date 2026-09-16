"""The catalogue-precision tolerance is re-measured on every frame the page builder stores.

`CATALOGUE_PRECISION_TOLERANCE` exists because the builder rounds witness centres and angles
before embedding them. This test rebuilds every stored frame through the builder's own rounding
and checks the declared value against the rounding bound and the frames themselves, so the
exception stays a measurement rather than a number someone chose.
"""

from __future__ import annotations

import math
from functools import cache

import numpy as np
import pytest

from workbench_tools.build_candidate import compact_frame, load_witness
from workbench_tools.packing_contracts import (
    CATALOGUE_PRECISION_TOLERANCE,
    DEFAULT_VALIDITY_TOLERANCE,
    check_unit_square_packing,
    pair_penetrations,
    wall_penetrations,
)

CATALOGUE = range(1, 325)
POSITION_ROUNDING = 0.5e-6
ANGLE_ROUNDING = math.radians(0.5e-4)


def _rounding_bounds() -> tuple[float, float]:
    """The largest penetration the builder's rounding can add to a pair and to a wall.

    A pair's projected centre distance moves by the rounded centres (sqrt 2 per centre, two
    centres) and by the rotated axis (up to sqrt 2 sides away); the other square's projected
    radius moves with the relative angle. A wall moves by one centre and one radius.
    """
    centres = 2 * math.sqrt(2) * POSITION_ROUNDING
    axis = math.sqrt(2) * ANGLE_ROUNDING
    radius = 0.5 * math.sqrt(2) * 2 * ANGLE_ROUNDING
    wall = POSITION_ROUNDING + 0.5 * math.sqrt(2) * ANGLE_ROUNDING
    return centres + axis + radius, wall


@cache
def _stored_frame(n: int) -> tuple[np.ndarray, float]:
    witness = load_witness(n)
    rendering = [{"fill": "#000000", "contacts": 0}] * n
    frame = compact_frame(witness, rendering, list(range(1, n + 1)))
    poses = np.array(
        [(x, y, math.radians(angle)) for x, y, angle, _fill, _contacts in frame["squares"]],
        dtype=np.float64,
    )
    return poses, float(frame["side"])


def test_the_declared_tolerance_covers_the_builders_rounding_bound() -> None:
    pair_bound, wall_bound = _rounding_bounds()
    assert pair_bound == pytest.approx(3.88e-6, rel=1e-2)
    assert wall_bound < pair_bound <= CATALOGUE_PRECISION_TOLERANCE


def test_every_stored_frame_passes_at_catalogue_precision_and_some_need_it() -> None:
    pair_bound, wall_bound = _rounding_bounds()
    needing_precision: list[int] = []
    worst_pair = 0.0
    worst_wall = 0.0
    for n in CATALOGUE:
        poses, side = _stored_frame(n)
        worst_pair = max(worst_pair, float(pair_penetrations(poses, 1.0).max(initial=0.0)))
        worst_wall = max(
            worst_wall, float(wall_penetrations(poses, 1.0, (0.0, 0.0), side).max(initial=0.0))
        )
        stored = check_unit_square_packing(
            poses, side=side, expected_count=n, tolerance=CATALOGUE_PRECISION_TOLERANCE
        )
        assert stored.passed, (
            f"stored n={n} frame fails its declared precision: {stored.issues}"
        )
        contract = check_unit_square_packing(
            poses, side=side, expected_count=n, tolerance=DEFAULT_VALIDITY_TOLERANCE
        )
        if not contract.passed:
            needing_precision.append(n)
    assert worst_pair <= pair_bound, worst_pair
    assert worst_wall <= wall_bound, worst_wall
    # Without frames that fail 1e-9 the exception would be unjustified; the count is recorded
    # in `CATALOGUE_PRECISION`'s comment.
    assert len(needing_precision) == 147, (len(needing_precision), worst_pair, worst_wall)
