"""The coupled-row prototype's rows hold at every disjoint pose (fast, randomised)."""

from __future__ import annotations

import random
from fractions import Fraction as Q

from devtools import pilot_n17_subpattern_bb as bb
from devtools import prototype_n17_bb_coupled as coupled
from tests.test_pilot_n17_subpattern_bb import separated, three_in_a_row


def test_disjoint_poses_satisfy_every_coupled_row() -> None:
    rng = random.Random(6)
    checked = 0
    for _ in range(500):
        ci = (Q(rng.randint(150, 200), 100), Q(rng.randint(150, 200), 100))
        offset = (Q(rng.randint(-130, 130), 100), Q(rng.randint(-130, 130), 100))
        cj = (ci[0] + offset[0], ci[1] + offset[1])
        size = Q(rng.randint(5, 30), 100)
        polygons = tuple(
            ((x, y), (x + size, y), (x + size, y + size), (x, y + size)) for x, y in (ci, cj)
        )
        pattern = bb.Pattern(("i", "j"), polygons, bb.cover.U)
        solver = coupled.CoupledSolver(pattern, bb.Settings(taylor=True))
        width = rng.choice((0.3, 0.08, 0.02))
        angles = tuple(
            (start, start + width)
            for start in (rng.uniform(0.4, 1.9 - width), rng.uniform(0.4, 1.9 - width))
        )
        node = bb.Node(angles, solver.cell_boxes, (None,), 0)
        boxes = solver.contract(node)
        if boxes is None:
            continue
        solver.taylor = solver.taylor_context(node)
        rows = solver.coupled_rows(node, boxes, 0)
        centres = solver.taylor.centres
        for _ in range(80 if rows else 0):
            pose = [
                (rng.uniform(b[0], b[1]), rng.uniform(b[2], b[3]), rng.uniform(*a))
                for b, a in zip(boxes, angles, strict=True)
            ]
            if separated(pose[0], pose[1]) < 0:
                continue
            values = {
                0: pose[0][0],
                1: pose[0][1],
                2: pose[1][0],
                3: pose[1][1],
                4: pose[0][2] - centres[0],
                5: pose[1][2] - centres[1],
            }
            for row in rows:
                total = sum(
                    c * values[col] for col, c in zip(row.columns, row.values, strict=True)
                )
                assert total <= row.rhs + 1e-12
                checked += 1
    assert checked > 150


def test_the_coupled_solver_never_certifies_a_feasible_row() -> None:
    solver = coupled.CoupledSolver(three_in_a_row(("3.05", "3.10")), bb.Settings(taylor=True))
    stack = [solver.root()]
    for _ in range(300):
        if not stack:
            break
        node = stack.pop()
        evaluation = solver.assess(node)
        if evaluation.pruned is not None:
            continue
        outcome = solver.children(node, evaluation)
        assert outcome is not None
        stack.extend(reversed(outcome[1]))
    assert stack, "the feasible row's tree must not close"
