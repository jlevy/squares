"""The projection method's two halves, checked against what they are supposed to be.

Each test names the property the method depends on, not an arrangement that happened to
come out of a run. The first two are the ones that caught real defects while this was
being built: a divide step that separated a pair by half of what it needed, and a
pose-space formulation in which no angle ever changed.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from devtools.divide_and_concur import (
    corners_of,
    pair_separation,
    pose_of,
    project_contacts,
    project_pairs,
    violation,
)
from devtools.run_projection_ratchet import Problem, solve


def _poses(
    rng: np.random.Generator, count: int, spread: float
) -> tuple[np.ndarray, np.ndarray]:
    a = np.stack([np.zeros(count), np.zeros(count), rng.uniform(0, 1.6, count)], -1)
    b = np.stack(
        [
            rng.uniform(-spread, spread, count),
            rng.uniform(-spread, spread, count),
            rng.uniform(0, 1.6, count),
        ],
        -1,
    )
    return a, b


def test_pose_round_trip() -> None:
    """Corners and poses are the same object seen twice."""
    poses = np.array([[1.3, 2.1, 0.4], [-0.2, 0.0, -1.1]])
    assert np.allclose(pose_of(corners_of(poses)), poses)


def test_divide_step_separates_every_overlapping_pair() -> None:
    """The divide projection lands *on* the constraint set, not near it.

    This is the property that distinguishes a projection method from the penalty physics,
    and the reason to prefer one here: a penalty settles where its forces balance and
    leaves an overlap floor, measured at 0.0046 of a unit side and immovable over a
    thirteenfold budget increase. A projection has no floor.
    """
    rng = np.random.default_rng(0)
    a, b = _poses(rng, 400, 0.9)
    va, vb = corners_of(a), corners_of(b)
    assert pair_separation(va, vb).min() < -0.5, "the sample must contain deep overlaps"
    qa, qb = project_pairs(va, vb)
    assert pair_separation(qa, qb).min() >= -1e-12


def test_divide_step_leaves_separated_pairs_alone() -> None:
    """A projection fixes what violates its constraint and nothing else."""
    rng = np.random.default_rng(1)
    a, b = _poses(rng, 200, 0.0)
    b[:, 0] += 3.0
    va, vb = corners_of(a), corners_of(b)
    qa, qb = project_pairs(va, vb)
    assert np.allclose(qa, va)
    assert np.allclose(qb, vb)


def test_concur_step_can_turn_a_square() -> None:
    """Angles have to be free, or the search is a translation search with a random tilt.

    A pose-space formulation with translation-only pair projections passes every overlap
    test above and is still useless, because no angle ever changes: both projections
    preserve it exactly and the average of equal angles is that angle. Putting the corners
    in the state is what buys rotation, so the rotation is what gets asserted.
    """
    poses = np.array([[0.0, 0.0, 0.0]])
    turned = corners_of(np.array([[0.0, 0.0, 0.3]]))
    assert abs(pose_of(0.5 * (corners_of(poses) + turned))[0, 2]) > 0.05


def test_violation_is_zero_at_a_known_record() -> None:
    """The feasibility measure agrees with a packing the project has proved."""
    side = 2 + 1 / math.sqrt(2)
    poses = np.array(
        [
            [0.5, 0.5, 0.0],
            [side - 0.5, 0.5, 0.0],
            [0.5, side - 0.5, 0.0],
            [side - 0.5, side - 0.5, 0.0],
            [side / 2, side / 2, math.pi / 4],
        ]
    )
    assert violation(poses, side) <= 1e-15
    assert violation(poses, side * 0.999) > 1e-4


@pytest.mark.parametrize("beta", [0.3, 0.5])
def test_a_solved_run_reports_an_exactly_feasible_packing(beta: float) -> None:
    """Whatever the search returns as solved is a packing, at the side it claims.

    The guard the penalty calibration could not offer. It is asserted over whichever seed
    succeeds rather than over a fixed one, because the success rate is a property of the
    method -- about one run in eight at five per cent above this record -- and pinning a
    seed would assert the sample instead of the invariant.
    """
    side = (2 + 1 / math.sqrt(2)) * 1.05
    for seed in range(30):
        out = solve(5, side, np.random.default_rng(seed), beta=beta, iters=8000, monotone=2000)
        if out.solved:
            assert out.violation == 0.0 or out.violation <= 1e-9
            assert violation(out.poses, side) <= 1e-9
            return
    pytest.fail("no run in thirty succeeded five per cent above the n = 5 record")


def test_a_declared_contact_closes_from_any_distance() -> None:
    """A contact constraint has no range, which is why it is a projection and not a force.

    The 2026-09-08 measurement that shelved contact-graph guidance recorded two causes,
    and the first was reach: target pairs sat one to four units apart while the attraction
    acted over a quarter of a side, so the bias could never build the structure it named.
    This asserts the property that retires that cause, over the same span of distances.
    """
    rng = np.random.default_rng(4)
    a = np.stack([np.zeros(400), np.zeros(400), rng.uniform(0, 1.6, 400)], -1)
    b = np.stack(
        [rng.uniform(-0.8, 4.0, 400), rng.uniform(-0.8, 4.0, 400), rng.uniform(0, 1.6, 400)],
        -1,
    )
    va, vb = corners_of(a), corners_of(b)
    before = pair_separation(va, vb)
    assert before.max() > 3.0, "the sample must contain pairs several units apart"
    assert before.min() < 0.0, "and pairs that overlap"
    qa, qb = project_contacts(va, vb)
    assert np.abs(pair_separation(qa, qb)).max() < 1e-9


def test_a_declared_contact_moves_squares_rigidly() -> None:
    """The contact projection translates whole squares and never deforms one.

    It is the divide half of the iteration, where a replica is free to stop being a square
    -- but a projection that sheared the corners here would hand the concur fit a
    correction it has to undo, and the pair would never settle.
    """
    rng = np.random.default_rng(5)
    a = np.stack([np.zeros(50), np.zeros(50), rng.uniform(0, 1.6, 50)], -1)
    b = np.stack(
        [rng.uniform(1.5, 3.0, 50), rng.uniform(0, 2.0, 50), rng.uniform(0, 1.6, 50)], -1
    )
    va, vb = corners_of(a), corners_of(b)
    qa, qb = project_contacts(va, vb)
    for before, after in ((va, qa), (vb, qb)):
        shift = after - before
        assert np.allclose(shift, shift[:, :1, :]), "every corner moved by the same vector"


def test_shared_orientation_is_a_projection_not_a_pull() -> None:
    """The lowest structure rung: some squares are declared to share an angle.

    Two numbers for n = 11 -- six at one orientation, five at another -- naming neither the
    angle nor which square is which. It enters the concur set, so it is satisfied exactly
    at every step rather than approached.
    """
    p = Problem(4, 3.0, classes=[[0, 1], [2, 3]])
    x = corners_of(
        np.array([[1.0, 1.0, 0.0], [2.0, 1.0, 0.4], [1.0, 2.0, 0.9], [2.0, 2.0, 1.2]])
    )
    poses = p.poses(x[p.owner])
    assert abs(poses[0, 2] - poses[1, 2]) < 1e-12
    assert abs(poses[2, 2] - poses[3, 2]) < 1e-12
    assert abs(poses[0, 2] - poses[2, 2]) > 1e-3, "distinct classes stay distinct"
