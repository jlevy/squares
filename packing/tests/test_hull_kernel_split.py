"""The producer's opt-in adaptive rows: refined rows the sequential checker admits."""

from __future__ import annotations

import copy
import time
from itertools import pairwise
from pathlib import Path

import pytest

from devtools import check_hull_kernel_mask0 as mask0_tool
from devtools import check_n17_subpattern as tool
from sqpack.hull_kernel import Budget, RefusalError, node, producer, sequential
from sqpack.hull_kernel.frame import Frame, make_frame
from sqpack.hull_kernel.rational import Q

# The blind pair at two bins under the envelope core: uniform rows stall, and bisecting
# the stuck rows closes it in round 3 with 16 rows. Pinned so a refactor that changes the
# produced bytes is seen.
SPLIT_BLIND_PAIR_NODE = "5c306769eced1a6dd95a665cfe90e68033d8baee37bf4fdcf5fb3243014510c0"


def budget() -> Budget:
    return Budget(time.monotonic() + 120, 200_000)


@pytest.fixture(scope="module")
def blind_pair() -> Frame:
    """Two near-equilateral cells, neither owning a point, with union diameter below one."""
    triangle = [(Q(1), Q(1)), (Q(19, 10), Q(1)), (Q(29, 20), Q(89, 50))]
    shifted = [(x + Q(1, 100), y) for x, y in triangle]
    return make_frame(
        name="blind-pair",
        cap=Q(3),
        length=Q(3),
        cells=[triangle, shifted],
        cell_names=["left", "right"],
        occupancy=2,
        action_names=("r0",),
    )


@pytest.fixture(scope="module")
def refined(blind_pair: Frame) -> producer.Production:
    return producer.produce(
        blind_pair,
        [0, 1],
        bins=2,
        max_rounds=12,
        budget=budget(),
        split=producer.SplitPolicy(floor=64, max_rows=200),
    )


def test_the_wall_loss_is_half_the_turn_near_an_axis_and_none_at_the_diagonal() -> None:
    frame = mask0_tool.n17_unique_frame()
    at_wall = [(frame.scale * Q(1, 2), frame.scale * Q(2))]
    inside = [(frame.scale * Q(2), frame.scale * Q(2))]
    first = producer.wall_loss(frame, Q(0), Q(1, 64), at_wall)
    assert first == pytest.approx(0.01537, abs=1e-4)
    assert producer.wall_loss(frame, Q(0), Q(1, 128), at_wall) == pytest.approx(
        first / 2, rel=0.02
    )
    assert producer.wall_loss(frame, Q(0), Q(1, 64), inside) == 0
    diagonal = Q(26, 64), Q(27, 64)
    assert producer.wall_loss(frame, *diagonal, at_wall) < first / 50
    with pytest.raises(RefusalError, match="positive floor"):
        producer.SplitPolicy(floor=0, max_rows=10)


def test_splitting_is_opt_in_and_closes_what_uniform_rows_cannot(
    blind_pair: Frame, refined: producer.Production
) -> None:
    uniform = producer.produce(blind_pair, [0, 1], bins=2, max_rounds=12, budget=budget())
    assert uniform.outcome == "stalled"
    assert all(len(step["rows"]) == 2 for step in uniform.node["steps"])
    assert all("splits" not in entry for entry in uniform.rounds)
    assert refined.outcome == "closed"
    assert [entry.get("planned_rows") for entry in refined.rounds[:3]] == [4, 8, 16]
    assert producer.content_sha256(refined.node) == SPLIT_BLIND_PAIR_NODE
    seen: dict[str, list[tuple[Q, Q]]] = {}
    for step in refined.node["steps"]:
        intervals = [(Q(row["interval"][0]), Q(row["interval"][1])) for row in step["rows"]]
        assert intervals[0][0] == 0
        assert intervals[-1][1] == 1
        assert all(a[1] == b[0] for a, b in pairwise(intervals))
        owner = str(step["owner"])
        if owner in seen:
            assert len(intervals) >= len(seen[owner])
        seen[owner] = intervals
    assert max(len(step["rows"]) for step in refined.node["steps"]) == 8


def test_the_checker_alone_certifies_refined_rows_and_refuses_a_crossed_one(
    blind_pair: Frame, refined: producer.Production, tmp_path: Path
) -> None:
    tool.save_certificate(tmp_path, refined.seed, refined.node)
    checked = tool.check_saved(tmp_path, blind_pair, max_seconds=60, require_no_producer=False)
    assert checked["status"] == "PASS_SAVED_CLOSED"
    assert checked["rows_checked"] == sum(len(step["rows"]) for step in refined.node["steps"])
    tampered = copy.deepcopy(refined.node)
    step = next(
        step
        for step in tampered["steps"]
        if len({str(row["prior_reference"]) for row in step["rows"]}) < len(step["rows"])
    )
    children = [
        index
        for index, row in enumerate(step["rows"])
        if sum(other["prior_reference"] == row["prior_reference"] for other in step["rows"]) > 1
    ]
    child = step["rows"][children[0]]
    child["prior_reference"] = next(
        row["prior_reference"]
        for row in step["rows"]
        if row["prior_reference"] != child["prior_reference"]
    )
    seed = node.admit_seed(
        blind_pair, refined.seed, mask=[0, 1], bins=2, budget=budget(), allow_empty_groups=True
    )
    with pytest.raises(RefusalError, match="refinement crossed predecessor interval"):
        sequential.replay_sequential(
            blind_pair,
            tampered,
            seed,
            mask=[0, 1],
            seed_sha256=producer.content_sha256(refined.seed),
            budget=budget(),
        )
