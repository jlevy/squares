"""The sequential mode-A checker certifies what the simple producer proposes, and no more."""

from __future__ import annotations

import copy
import gzip
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest

from devtools import check_hull_kernel_mask0 as mask0_tool
from devtools import check_n17_subpattern as tool
from sqpack.hull_kernel import Budget, RefusalError, node, producer, sequential
from sqpack.hull_kernel.frame import Frame, make_frame
from sqpack.hull_kernel.geometry import Polygon
from sqpack.hull_kernel.rational import Q


def budget() -> Budget:
    return Budget(time.monotonic() + 60, 200_000)


def box(x0: Q, x1: Q, y0: Q, y1: Q) -> Polygon:
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


@pytest.fixture(scope="module")
def pair() -> Frame:
    """Two small cells whose union has diameter below one: two centres cannot both fit."""
    return make_frame(
        name="pair",
        cap=Q(3),
        length=Q(3),
        cells=[
            box(Q(5, 4), Q(3, 2), Q(7, 5), Q(8, 5)),
            box(Q(3, 2), Q(7, 4), Q(7, 5), Q(8, 5)),
        ],
        cell_names=["west", "east"],
        occupancy=2,
        action_names=("r0",),
    )


@pytest.fixture(scope="module")
def n17_frame() -> Frame:
    return mask0_tool.n17_unique_frame()


def certify(frame: Frame, production: producer.Production, mask: list[int], bins: int) -> Any:
    seed = node.admit_seed(
        frame, production.seed, mask=mask, bins=bins, budget=budget(), allow_empty_groups=True
    )
    return sequential.replay_sequential(
        frame,
        production.node,
        seed,
        mask=mask,
        seed_sha256=producer.content_sha256(production.seed),
        budget=budget(),
    )


def test_a_pair_closer_than_one_closes_at_its_first_update(pair: Frame) -> None:
    production = producer.produce(pair, [0, 1], bins=8, max_rounds=2, budget=budget())
    assert production.outcome == "closed"
    trace = certify(pair, production, [0, 1], 8)
    assert trace.closure == {"kind": "all_parent_poses_forbidden", "owner": 0, "step": 0}
    assert pair.states_containing([0, 1]) == [0]


def test_a_declared_closure_must_be_the_derived_one(pair: Frame) -> None:
    production = producer.produce(pair, [0, 1], bins=8, max_rounds=2, budget=budget())
    production.node["contradiction"] = {
        "kind": "all_parent_poses_forbidden",
        "owner": 1,
        "step": 0,
    }
    with pytest.raises(RefusalError, match="declared closure differs"):
        certify(pair, production, [0, 1], 8)


def test_a_removed_residual_or_a_claimed_closure_on_a_stall_is_refused(
    n17_frame: Frame,
) -> None:
    mask = sorted(n17_frame.cell_names.index(cell) for cell in tool.PATTERNS["A"])
    production = producer.produce(
        n17_frame, mask, bins=4, max_rounds=1, budget=budget(), collision=False
    )
    trace = certify(n17_frame, production, mask, 4)
    assert trace.closure is None
    live = next(
        (index, row)
        for index, row in enumerate(production.node["steps"][0]["rows"])
        if row["residual_polygons"]
    )
    cut = copy.deepcopy(production)
    cut.node["steps"][0]["rows"][live[0]]["residual_polygons"] = []
    with pytest.raises(RefusalError, match=r"uncovered|facets"):
        certify(n17_frame, cut, mask, 4)
    claimed = copy.deepcopy(production)
    claimed.node["contradiction"] = {
        "kind": "all_parent_poses_forbidden",
        "owner": mask[0],
        "step": 0,
    }
    claimed.node["closed"] = claimed.node["terminal"] = True
    with pytest.raises(RefusalError, match="declared closure differs"):
        certify(n17_frame, claimed, mask, 4)


def test_pattern_a_stalls_at_four_bins_with_its_extents(n17_frame: Frame) -> None:
    result = tool.run(
        n17_frame,
        tool.PATTERNS["A"],
        name="A",
        bins=4,
        max_rounds=2,
        max_seconds=60,
        cover="indexed",
        collision=False,
    )
    assert result["status"] == "PASS_CERTIFIED_STALL"
    assert result["excluded_orbits"] == 0
    assert len(result["final_extents"]) == 6
    assert result["seed_points"]["interior-W"] == 0
    assert result["seed_points"]["interior-SW"] > 0


def test_a_saved_run_is_checked_from_its_saved_node_with_the_same_result(
    n17_frame: Frame, tmp_path: Path
) -> None:
    """With `save_objects` the run checks the node it saved, read a step at a time, and
    lets the produced one go; its result is the one the in-memory check gives, and the
    files are what `gzip.compress` of the canonical bytes gives."""
    settings: dict[str, Any] = {
        "name": "A",
        "bins": 4,
        "max_rounds": 2,
        "max_seconds": 60,
        "cover": "indexed",
        "collision": False,
    }
    in_memory = tool.run(n17_frame, tool.PATTERNS["A"], **settings)
    saved = tool.run(n17_frame, tool.PATTERNS["A"], save_objects=tmp_path, **settings)
    timing = ("producer_seconds", "checker_seconds")
    assert {key: value for key, value in saved.items() if key not in timing} == {
        key: value for key, value in in_memory.items() if key not in timing
    }
    seed_file, node_file = tool.saved_files(tmp_path)
    assert {path.name for path in tmp_path.iterdir()} == {seed_file.name, node_file.name}
    assert node_file.name == f"node-{saved['node_sha256']}.json.gz"
    for path in (seed_file, node_file):
        document = json.loads(gzip.decompress(path.read_bytes()))
        assert path.read_bytes() == gzip.compress(tool.canonical_bytes(document), mtime=0)
        assert tool.content_sha256(document) in path.name


def test_the_endpoint_sub_pattern_stalls(n17_frame: Frame) -> None:
    result = tool.run(
        n17_frame,
        tool.PATTERNS["endpoint6"],
        name="endpoint6",
        bins=4,
        max_rounds=1,
        max_seconds=60,
        cover="indexed",
    )
    assert result["status"] == "PASS_CONTROL_STALLED"
    assert result["closure"] is None


@pytest.fixture(scope="module")
def blind_pair() -> Frame:
    """Two near-equilateral cells of side about 0.9 whose union has diameter below one.

    Each cell's least enclosing radius (about 0.52) exceeds one half, so no point is owned
    from either cell alone; two centres in them are under one apart, so the pair is
    infeasible, and only collision against the partner's pose cover can show it.
    """
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


def test_a_blind_pair_closes_through_collision_alone(blind_pair: Frame) -> None:
    production = producer.produce(blind_pair, [0, 1], bins=16, max_rounds=2, budget=budget())
    assert production.seed["groups"] == {"0": [], "1": []}
    trace = certify(blind_pair, production, [0, 1], 16)
    assert trace.closure is not None
    assert trace.closure["kind"] == "all_parent_poses_forbidden"
    assert trace.groups == {0: [], 1: []}
    assert trace.steps[-1]["collision_regions"] > 0
    without = producer.produce(
        blind_pair, [0, 1], bins=16, max_rounds=2, budget=budget(), collision=False
    )
    assert certify(blind_pair, without, [0, 1], 16).closure is None


def test_a_forged_collision_region_or_partner_cover_is_refused(blind_pair: Frame) -> None:
    production = producer.produce(blind_pair, [0, 1], bins=16, max_rounds=2, budget=budget())
    step = production.node["steps"][-1]
    index, row = next(
        (index, row) for index, row in enumerate(step["rows"]) if row["collision_regions"]
    )
    forged = copy.deepcopy(production)
    region = forged.node["steps"][-1]["rows"][index]["collision_regions"][0]
    region["vertices"] = [[str(Q(x) + Q(1, 2)), y] for x, y in region["vertices"]]
    with pytest.raises(RefusalError, match="escapes"):
        certify(blind_pair, forged, [0, 1], 16)
    partner = str(row["collision_regions"][0]["partner"])
    shrunk = copy.deepcopy(production)
    cover = shrunk.node["steps"][-1]["prior_partner_pose_covers"][partner]
    live = next(item for item in cover if item["domain"])
    live["domain"] = live["domain"][:1]
    with pytest.raises(RefusalError, match="partner cover domain differs"):
        certify(blind_pair, shrunk, [0, 1], 16)


def test_a_saved_closure_is_certified_by_the_checker_alone(
    blind_pair: Frame, tmp_path: Path
) -> None:
    production = producer.produce(blind_pair, [0, 1], bins=16, max_rounds=2, budget=budget())
    tool.save_certificate(tmp_path, production.seed, production.node)
    result = tool.check_saved(tmp_path, blind_pair, max_seconds=60, require_no_producer=False)
    assert result["status"] == "PASS_SAVED_CLOSED"
    assert result["closure"]["kind"] == "all_parent_poses_forbidden"
    assert result["excluded_orbits"] == 1
    assert result["node_sha256"] == tool.content_sha256(production.node)
    with pytest.raises(RefusalError, match="producer is loaded"):
        tool.check_saved(tmp_path, blind_pair)
    # The file's name is a name, not a check: edited in place under its old name, the node
    # is refused for what the edit says.
    saved = next(tmp_path.glob("node-*.json.gz"))
    raw = gzip.decompress(saved.read_bytes())
    saved.write_bytes(gzip.compress(raw.replace(b'"closed":true', b'"closed":false')))
    with pytest.raises(RefusalError, match="declared closure differs"):
        tool.check_saved(tmp_path, blind_pair, require_no_producer=False)


def test_a_saved_node_is_read_a_step_at_a_time_with_the_same_content(
    blind_pair: Frame, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`stream_node` gives the node's own members, steps and content id, from the file
    `save_certificate` writes and from the same node re-spaced, with reads so short that
    values and numbers are split between them; the saved check certifies both alike."""
    production = producer.produce(blind_pair, [0, 1], bins=16, max_rounds=2, budget=budget())
    expected = json.loads(tool.canonical_bytes(production.node))
    canonical, spaced = tmp_path / "canonical", tmp_path / "spaced"
    tool.save_certificate(canonical, production.seed, production.node)
    tool.save_certificate(spaced, production.seed, production.node)
    _, node_file = tool.saved_files(spaced)
    node_file.write_bytes(
        gzip.compress(json.dumps(expected, indent=1, sort_keys=True).encode())
    )
    monkeypatch.setattr(tool, "STREAM_CHUNK", 7)
    for directory in (canonical, spaced):
        header, steps = tool.stream_node(tool.saved_files(directory)[1])
        assert steps
        assert list(steps) == expected["steps"]
        assert {**header, "steps": expected["steps"]} == expected
        assert steps.content_sha256 == tool.content_sha256(production.node)
        with pytest.raises(RefusalError, match="read once"):
            next(iter(steps))
    checked = [
        tool.check_saved(directory, blind_pair, max_seconds=60, require_no_producer=False)
        for directory in (canonical, spaced)
    ]
    trace = certify(blind_pair, production, [0, 1], 16)
    for result in checked:
        assert result["node_sha256"] == tool.content_sha256(production.node)
        assert result["closure"] == trace.closure
        assert result["rows_checked"] == sum(step["rows"] for step in trace.steps)
        assert result["events"] == sum(step["events"] for step in trace.steps)


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("[]", "is a JSON object"),
        ('{"mask":[]}', "has no steps"),
        ('{"mask":[],"mask":[],"steps":[]}', "repeats its member"),
        ('{"steps":[],"mask":[]}', "follows the steps"),
        ('{"steps":[{} {}]}', "separated by commas"),
        ('{"steps":[{}],"terminal":true} []', "data follows"),
    ],
)
def test_a_saved_node_out_of_canonical_order_or_malformed_is_refused(
    tmp_path: Path, text: str, message: str
) -> None:
    path = tmp_path / "node-0.json.gz"
    path.write_bytes(gzip.compress(text.encode()))

    def read(path: Path) -> list[dict[str, Any]]:
        return list(tool.stream_node(path)[1])

    with pytest.raises(RefusalError, match=message):
        _ = read(path)


def test_the_saved_check_path_never_imports_the_producer() -> None:
    code = (
        "import sys; import devtools.check_n17_subpattern as tool; "
        "assert tool.PRODUCER not in sys.modules, 'producer imported'"
    )
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=Path(tool.__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )
    assert completed.returncode == 0, completed.stderr
