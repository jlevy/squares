"""The standing certificate verifiers pass sound certificates and refuse doctored ones."""

from __future__ import annotations

import copy
import gzip
import hashlib
import json
import math
import random
import shutil
import subprocess
import sys
import time
from collections.abc import Callable, Sequence
from fractions import Fraction as Q
from functools import cache
from itertools import combinations_with_replacement
from pathlib import Path
from typing import Any

import pytest

from devtools import check_hull_kernel_mask0 as mask0_tool
from devtools import n11_closed_interval_cover as closed_interval
from devtools import pilot_n17_subpattern_bb as bb
from devtools import verify_n17_bb_certificate as bb_verifier
from devtools import verify_n17_kernel_certificate as kernel_verifier
from devtools.check_n17_subpattern import canonical_bytes, load_certificate, save_certificate
from sqpack.hull_kernel import Budget, producer
from sqpack.hull_kernel.frame import make_frame

PACKING = Path(__file__).resolve().parents[1]
FORBIDDEN = (
    "sqpack.hull_kernel",
    "devtools.check_n17_subpattern",
    "devtools.pilot_n17_subpattern_bb",
    "devtools.select_n17_sub_patterns",
    "scipy.optimize",
)


def canonical(document: Any) -> bytes:
    return json.dumps(document, sort_keys=True, separators=(",", ":")).encode()


def cells_file(directory: Path, cap: Q, names: list[str], polygons: list[Any]) -> Path:
    path = directory / "cells.json"
    document = {
        "U": str(cap),
        "order": names,
        "cells": {
            name: [[str(x), str(y)] for x, y in polygon]
            for name, polygon in zip(names, polygons, strict=True)
        },
    }
    _ = path.write_text(json.dumps(document), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# The kernel verifier, on the blind pair of test_hull_kernel_sequential
# ---------------------------------------------------------------------------

TRIANGLE = [(Q(1), Q(1)), (Q(19, 10), Q(1)), (Q(29, 20), Q(89, 50))]
SHIFTED = [(x + Q(1, 100), y) for x, y in TRIANGLE]


@cache
def blind_pair_objects() -> tuple[dict[str, Any], dict[str, Any]]:
    """The two near-equilateral cells whose closure needs collision alone, produced once."""
    frame = make_frame(
        name="blind-pair",
        cap=Q(3),
        length=Q(3),
        cells=[TRIANGLE, SHIFTED],
        cell_names=["left", "right"],
        occupancy=2,
        action_names=("r0",),
    )
    budget = Budget(time.monotonic() + 60, 200_000)
    production = producer.produce(frame, [0, 1], bins=16, max_rounds=2, budget=budget)
    return production.seed, production.node


def blind_pair(tmp_path: Path, edit: Callable[[dict[str, Any]], None] | None = None) -> Path:
    """The saved closure under `tmp_path/cert`, its node edited and re-named if asked."""
    seed, node = blind_pair_objects()
    if edit is not None:
        node = copy.deepcopy(node)
        edit(node)
    save_certificate(tmp_path / "cert", seed, node)
    return tmp_path / "cert"


def blind_cells(tmp_path: Path) -> kernel_verifier.Cells:
    path = cells_file(tmp_path, Q(3), ["left", "right"], [TRIANGLE, SHIFTED])
    return kernel_verifier.file_cells(path, hashlib.sha256(path.read_bytes()).hexdigest())


def test_the_kernel_verifier_passes_the_blind_pair(tmp_path: Path) -> None:
    receipt = kernel_verifier.verify(blind_pair(tmp_path), blind_cells(tmp_path))
    assert receipt["status"] == "PASS", receipt["failure"]
    assert receipt["mode"] == "full"
    assert receipt["closure"]["kind"] == "all_parent_poses_forbidden"
    assert receipt["counts"]["collision_regions"] > 0
    seed, node = blind_pair_objects()
    assert receipt["certificate"] == {
        "seed_sha256": hashlib.sha256(canonical(seed)).hexdigest(),
        "node_sha256": hashlib.sha256(canonical(node)).hexdigest(),
    }
    sampled = kernel_verifier.verify(blind_pair(tmp_path), blind_cells(tmp_path), sample=1)
    assert sampled["status"] == "PASS"
    assert sampled["mode"] == "sample"


def collision_row(node: dict[str, Any]) -> dict[str, Any]:
    return next(row for row in node["steps"][-1]["rows"] if row["collision_regions"])


def shift_region(node: dict[str, Any]) -> None:
    region = collision_row(node)["collision_regions"][0]
    region["vertices"] = [[str(Q(x) + Q(1, 2)), y] for x, y in region["vertices"]]


def shrink_partner_domain(node: dict[str, Any]) -> None:
    covers = node["steps"][-1]["prior_partner_pose_covers"]
    live = next(item for items in covers.values() for item in items if item["domain"])
    live["domain"] = live["domain"][:1]


def drop_residual_claim(node: dict[str, Any]) -> None:
    node["closed"] = False


def drop_collision_region(node: dict[str, Any]) -> None:
    collision_row(node)["collision_regions"] = []


Point = tuple[Q, Q]


def decode(polygon: Any) -> list[Point]:
    return [(Q(x), Q(y)) for x, y in polygon]


def replayed_state(
    seed: dict[str, Any], node: dict[str, Any], cells: kernel_verifier.Cells, upto: int
) -> kernel_verifier.State:
    """The verifier's own state just before step `upto`, replayed without the full-row
    checks."""
    state = kernel_verifier.State(
        [list(polygon) for polygon in cells.polygons],
        cells.cap,
        seed["bins"],
        list(seed["mask"]),
    )
    kernel_verifier.check_seed(state, seed, node)
    for si, step in enumerate(node["steps"][:upto]):
        rows, planes, any_live = kernel_verifier.check_step(
            state, step, si, node["node_id"], set()
        )
        kernel_verifier.compress(state, step, si, planes, any_live=any_live)
        state.rows[step["owner"]] = rows
    return state


def facet_bounds(cover: kernel_verifier.CoverRow, core: list[Point]) -> list[tuple[Q, Q, Q]]:
    """`(a, b, bound)` per facet of partner core minus core, with the row's domain minimum
    added, by the reviewed hull form rather than the verifier's edge merge."""
    partner_core = [(Q(x, z), Q(y, z)) for x, y, z in cover.core]
    domain = [(Q(x, z), Q(y, z)) for x, y, z in cover.domain]
    difference = kernel_verifier.minkowski_diff(partner_core, core)
    return [
        (a, b, c + min(a * y[0] + b * y[1] for y in domain))
        for a, b, c in kernel_verifier.planes_of(difference)
    ]


def add_point_colliding_in_the_first_row_alone(
    node: dict[str, Any], seed: dict[str, Any], cells: kernel_verifier.Cells
) -> None:
    """A point of a row's required domain that collides with the partner in its first
    live row (every facet of that row's collision set holds) but not in some later row
    (a facet of that row's set fails), appended to a collision region so that the row's
    cover is untouched: only the collision check can refuse it, and a verifier that
    checked the first live partner row alone would accept it. The point is a vertex of
    the required domain cut by the first row's facets, so one exists exactly when that
    cut is not inside every later row's set."""
    for si in range(len(node["steps"]) - 1, -1, -1):
        step = node["steps"][si]
        state = replayed_state(seed, node, cells, si)
        partners = kernel_verifier.check_partners(state, step, si)
        for ri, row in enumerate(step["rows"]):
            if not row["collision_regions"]:
                continue
            core = kernel_verifier.hull(decode(row["core_vertices"]))
            prior = state.rows[step["owner"]][ri]
            lo, hi = Q(row["interval"][0]), Q(row["interval"][1])
            required = kernel_verifier.intersect_convex(
                list(prior.outer), kernel_verifier.wall_box(lo, hi, cells.cap)
            )
            for item in row["collision_regions"]:
                covers = partners[item["partner"]]
                if len(covers) < 2:
                    continue
                per_cover = [facet_bounds(cover, core) for cover in covers]
                first = list(required)
                for a, b, bound in per_cover[0]:
                    first = kernel_verifier.clip_closed(first, a, b, bound)
                for px, py in kernel_verifier.hull(first):
                    if any(
                        a * px + b * py > bound
                        for facets in per_cover[1:]
                        for a, b, bound in facets
                    ):
                        item["vertices"] = [*item["vertices"], [str(px), str(py)]]
                        return
    raise AssertionError("every first-row collision set lies inside the later rows' sets")


W7 = ("corner-SW", "side-N0", "side-W0", "side-W1", "side-W2", "interior-SW", "interior-W")


W7_BINS8 = (
    PACKING
    / "campaign/explorations/X048-session-168-pilots/audit-verifier-rewrites/fixture-w7-bins8"
)


@cache
def w7_stall_objects() -> tuple[dict[str, Any], dict[str, Any]]:
    """W7 at 8 bins: a stall of 14 steps and 257 collision regions in which a later live
    partner row cuts a region the first live row does not. On the blind pair the first
    live row's collision set is the tightest in all 16 regions, so a verifier that stopped
    at the first row would be equivalent to the full one there and no doctored blind-pair
    closure can tell them apart.

    The objects are the committed fixture, read rather than produced: the production is
    the test's whole cost, and the verifier's obligation is what a valid certificate holds,
    not what a fresh one holds. `test_the_w7_fixture_is_what_the_producer_writes` checks
    the seed and scientific context match, and independently replays both witnesses."""
    seed, node, _, _ = load_certificate(W7_BINS8)
    return seed, node


@pytest.mark.slow
def test_the_w7_fixture_is_what_the_producer_writes(tmp_path: Path) -> None:
    frame = mask0_tool.n17_unique_frame()
    mask = sorted(frame.cell_names.index(cell) for cell in W7)
    budget = Budget(time.monotonic() + 600, 5_000_000)
    production = producer.produce(
        frame, mask, bins=8, max_rounds=6, budget=budget, node_id="n17-W7-audit-fixture"
    )
    seed, node = w7_stall_objects()
    assert canonical_bytes(production.seed) == canonical_bytes(seed)
    # Compression may choose a different valid witness. The historical certificate
    # remains immutable; the newly proposed witness must pass its own full replay.
    for key in (
        "node_id",
        "mask",
        "U",
        "B",
        "parent",
        "constraints",
        "guard_source",
        "closed",
        "terminal",
        "contradiction",
    ):
        assert production.node[key] == node[key], key
    assert production.node["initial"] == node["initial"]
    assert production.node["final_state"]["world"] == node["final_state"]["world"]
    saved = tmp_path / "fresh-w7"
    save_certificate(saved, production.seed, production.node)
    saved_seed, saved_node, seed_id, node_id = load_certificate(saved)
    assert canonical_bytes(saved_seed) == canonical_bytes(production.seed)
    assert canonical_bytes(saved_node) == canonical_bytes(production.node)
    replay = kernel_verifier.verify_objects(saved, kernel_verifier.cover_cells())
    assert replay["certificate"] == {"seed_sha256": seed_id, "node_sha256": node_id}
    assert replay["closed"] is False
    assert replay["closure"] is None
    assert replay["mask"] == mask
    assert replay["bins"] == 8
    assert replay["counts"]["steps"] == len(production.node["steps"])
    # The control for the partner-row test below: the undoctored fixture verifies, as a
    # stall. It lives here, beside the build, so the fast test pays for one replay.
    assert (
        kernel_verifier.verify_objects(W7_BINS8, kernel_verifier.cover_cells())["closed"]
        is False
    )


def test_the_kernel_verifier_checks_every_live_partner_row(tmp_path: Path) -> None:
    """A point that collides with the first live partner row alone is refused at the
    collision check of the step it was added to; the undoctored fixture's own passing
    replay is asserted in `test_the_w7_fixture_is_what_the_producer_writes`."""
    seed, node = w7_stall_objects()
    cells = kernel_verifier.cover_cells()
    doctored = copy.deepcopy(node)
    add_point_colliding_in_the_first_row_alone(doctored, seed, cells)
    save_certificate(tmp_path / "doctored", seed, doctored)
    with pytest.raises(kernel_verifier.VerificationError, match="escapes the collision set"):
        _ = kernel_verifier.verify_objects(tmp_path / "doctored", cells)


@pytest.mark.parametrize(
    ("edit", "message"),
    [
        (shift_region, "escapes"),
        (shrink_partner_domain, "domain"),
        (drop_residual_claim, "closed flags"),
        (drop_collision_region, "NOT covered"),
    ],
)
def test_the_kernel_verifier_refuses_a_doctored_closure(
    tmp_path: Path, edit: Callable[[dict[str, Any]], None], message: str
) -> None:
    receipt = kernel_verifier.verify(blind_pair(tmp_path, edit), blind_cells(tmp_path))
    assert receipt["status"] == "FAIL"
    assert message in receipt["failure"]


def test_a_saved_object_is_judged_by_what_it_says_not_by_its_name(tmp_path: Path) -> None:
    """The saver names files by content id, and the name is not read back: the closure
    re-spaced under another name verifies, and edited in place it is refused for what the
    edit says."""
    directory = blind_pair(tmp_path)
    saved = next(directory.glob("node-*.json.gz"))
    raw = gzip.decompress(saved.read_bytes())
    saved.unlink()
    renamed = directory / "node-renamed.json.gz"
    _ = renamed.write_bytes(gzip.compress(json.dumps(json.loads(raw), indent=1).encode()))
    passed = kernel_verifier.verify(directory, blind_cells(tmp_path))
    assert passed["status"] == "PASS", passed["failure"]
    assert passed["certificate"]["node_sha256"] == hashlib.sha256(raw).hexdigest()
    _ = renamed.write_bytes(gzip.compress(raw.replace(b'"closed":true', b'"closed":false')))
    receipt = kernel_verifier.verify(directory, blind_cells(tmp_path))
    assert receipt["status"] == "FAIL"
    assert "closed flags" in receipt["failure"]
    with pytest.raises(kernel_verifier.VerificationError, match="digest"):
        _ = kernel_verifier.file_cells(tmp_path / "cells.json", "0" * 64)


def test_the_kernel_verifier_reads_a_node_a_step_at_a_time(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The node stream gives the node's own members, steps and content id, from the saved
    file and from the same node re-spaced, with reads so short that values and numbers
    are split between them."""
    _, node = blind_pair_objects()
    expected = json.loads(canonical(node))
    directory = blind_pair(tmp_path)
    saved = next(directory.glob("node-*.json.gz"))
    spaced = tmp_path / "spaced.json.gz"
    _ = spaced.write_bytes(gzip.compress(json.dumps(expected, indent=2).encode()))
    monkeypatch.setattr(kernel_verifier, "READ_BYTES", 5)
    for path in (saved, spaced):
        stream = kernel_verifier.NodeStream(path)
        steps = stream.steps()
        assert list(steps) == expected["steps"]
        assert {**stream.header, "steps": expected["steps"]} == expected
        assert stream.sha256 == hashlib.sha256(canonical(node)).hexdigest()
        with pytest.raises(kernel_verifier.VerificationError, match="read once"):
            _ = next(stream.steps())


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ('"node"', "not a JSON object"),
        ('{"mask":[]}', "has no steps"),
        ('{"mask":[],"mask":[],"steps":[]}', "repeats its member"),
        ('{"steps":[],"mask":[]}', "follows its steps"),
        ('{"steps":[{} {}]}', "not comma-separated"),
        ('{"steps":[],"terminal":true}{}', "data follows"),
    ],
)
def test_the_kernel_verifier_refuses_a_node_out_of_canonical_order(
    tmp_path: Path, text: str, message: str
) -> None:
    path = tmp_path / "node.json.gz"
    _ = path.write_bytes(gzip.compress(text.encode()))

    def read(path: Path) -> list[dict[str, Any]]:
        return list(kernel_verifier.NodeStream(path).steps())

    with pytest.raises(kernel_verifier.VerificationError, match=message):
        _ = read(path)


# ---------------------------------------------------------------------------
# The kernel verifier on refined rows, from the producer's split policy
# ---------------------------------------------------------------------------

# The blind pair moved onto both walls: its cells reach x = 1/2 and y = 1/2, so a
# bisected row's legal box is narrower than its predecessor's wherever the turn is off the
# axes, and the rows' covers reach only their own boxes.
WALL_TRIANGLE = [(x - Q(1, 2), y - Q(1, 2)) for x, y in TRIANGLE]
WALL_SHIFTED = [(x + Q(1, 100), y) for x, y in WALL_TRIANGLE]
PAIRS = {"blind": (TRIANGLE, SHIFTED), "wall": (WALL_TRIANGLE, WALL_SHIFTED)}


@cache
def split_objects(pair: str) -> tuple[dict[str, Any], dict[str, Any]]:
    """A closure whose rows the producer's split policy refined, made once per pair.

    Both pairs stall on two uniform rows. With `SplitPolicy(64, 200)` the blind pair
    closes at step 6 with rows per step 2, 2, 2, 2, 4, 4, 8 (lane K2's
    `test_hull_kernel_split`), and the wall pair at step 8 with 2, 2, 2, 2, 4, 4, 4, 4, 5.
    """
    frame = make_frame(
        name=f"{pair}-pair",
        cap=Q(3),
        length=Q(3),
        cells=list(PAIRS[pair]),
        cell_names=["left", "right"],
        occupancy=2,
        action_names=("r0",),
    )
    production = producer.produce(
        frame,
        [0, 1],
        bins=2,
        max_rounds=12,
        budget=Budget(time.monotonic() + 60, 200_000),
        split=producer.SplitPolicy(floor=64, max_rows=200),
    )
    assert production.outcome == "closed"
    return production.seed, production.node


def split_certificate(
    tmp_path: Path, pair: str, edit: Callable[[dict[str, Any]], None] | None = None
) -> Path:
    seed, node = split_objects(pair)
    if edit is not None:
        node = copy.deepcopy(node)
        edit(node)
    save_certificate(tmp_path / pair, seed, node)
    return tmp_path / pair


def pair_cells(tmp_path: Path, pair: str) -> kernel_verifier.Cells:
    path = cells_file(tmp_path, Q(3), ["left", "right"], list(PAIRS[pair]))
    return kernel_verifier.file_cells(path, hashlib.sha256(path.read_bytes()).hexdigest())


def children(step: dict[str, Any]) -> list[int]:
    """Each row index whose row shares its predecessor with the next row: a split."""
    rows = step["rows"]
    return [
        index
        for index in range(len(rows) - 1)
        if rows[index]["prior_reference"] == rows[index + 1]["prior_reference"]
    ]


@pytest.mark.parametrize("pair", ["blind", "wall"])
def test_the_kernel_verifier_passes_refined_rows(tmp_path: Path, pair: str) -> None:
    seed, node = split_objects(pair)
    counts = [len(step["rows"]) for step in node["steps"]]
    assert max(counts) > seed["bins"]
    assert any(children(step) for step in node["steps"])
    cells = pair_cells(tmp_path, pair)
    receipt = kernel_verifier.verify(split_certificate(tmp_path, pair), cells)
    assert receipt["status"] == "PASS", receipt["failure"]
    assert receipt["closure"] == node["contradiction"]
    assert receipt["counts"]["steps"] == len(counts)
    assert receipt["counts"]["rows_full"] > seed["bins"] * len(counts)
    sampled = kernel_verifier.verify(split_certificate(tmp_path, pair), cells, sample=1)
    assert sampled["status"] == "PASS", sampled["failure"]


@pytest.mark.parametrize("pair", ["blind", "wall"])
def test_the_kernel_verifier_bounds_its_memos_without_changing_a_count(
    tmp_path: Path, pair: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """With the facet bound at zero the facets are dropped after every step, as the
    forbidden regions of every replaced hull always are, and the receipt is the same."""
    cells = pair_cells(tmp_path, pair)
    bounded = kernel_verifier.verify(split_certificate(tmp_path, pair), cells)
    monkeypatch.setattr(kernel_verifier, "MEMO_PAIRS", 0)
    emptied = kernel_verifier.verify(split_certificate(tmp_path, pair), cells)
    assert bounded["status"] == "PASS", bounded["failure"]
    assert {**emptied, "seconds": None} == {**bounded, "seconds": None}


def test_a_refined_row_is_held_to_its_own_legal_box(tmp_path: Path) -> None:
    """Some bisected row of the wall pair has a cover that reaches only its own legal box:
    cut by its predecessor's wider box instead, its required domain is not covered. So the
    pass above depends on the verifier cutting by the box of the row's own interval, and a
    verifier that kept the predecessor's box would refuse a sound certificate."""
    seed, node = split_objects("wall")
    cells = pair_cells(tmp_path, "wall")
    own_only = 0
    for si, step in enumerate(node["steps"]):
        state = replayed_state(seed, node, cells, si)
        owner = step["owner"]
        cited = kernel_verifier.predecessors(state.rows[owner], step["rows"], si)
        for row, prior in zip(step["rows"], cited, strict=True):
            lo, hi = Q(row["interval"][0]), Q(row["interval"][1])
            if (lo, hi) == prior.interval or not prior.outer:
                continue
            own = kernel_verifier.intersect_convex(
                list(prior.outer), kernel_verifier.wall_box(lo, hi, cells.cap)
            )
            wide = kernel_verifier.intersect_convex(
                list(prior.outer), kernel_verifier.wall_box(*prior.interval, cells.cap)
            )
            if kernel_verifier.area2(own) == 0:
                continue
            core = kernel_verifier.hull(decode(row["core_vertices"]))
            regions = [
                state.forbidden_region(state.groups[other], core)
                for other in state.mask
                if other != owner and state.groups[other]
            ]
            regions.extend(
                kernel_verifier.hull(decode(item["vertices"]))
                for item in row["collision_regions"]
            )
            regions.extend(kernel_verifier.hull(decode(p)) for p in row["residual_polygons"])
            assert kernel_verifier.covered_by_sweep(kernel_verifier.hull(own), regions)[0]
            if not kernel_verifier.covered_by_sweep(kernel_verifier.hull(wide), regions)[0]:
                own_only += 1
    assert own_only > 0


def first_split(node: dict[str, Any]) -> tuple[dict[str, Any], int]:
    step = next(step for step in node["steps"] if children(step))
    return step, children(step)[0]


def leave_gap(node: dict[str, Any]) -> None:
    step, index = first_split(node)
    end = step["rows"][index]["interval"]
    end[1] = str(Q(end[1]) - Q(1, 2**20))


def overlap(node: dict[str, Any]) -> None:
    step, index = first_split(node)
    end = step["rows"][index]["interval"]
    end[1] = str(Q(end[1]) + Q(1, 2**20))


def stop_short(node: dict[str, Any]) -> None:
    step, _ = first_split(node)
    step["rows"].pop()


def cite_the_next_parent(node: dict[str, Any]) -> None:
    """The first split's first child cites the accepted row after its parent, which starts
    above it: the predecessor's lower end refuses it."""
    step, index = first_split(node)
    child = step["rows"][index]
    child["prior_reference"] = next(
        row["prior_reference"]
        for row in step["rows"][index:]
        if row["prior_reference"] != child["prior_reference"]
    )


def cite_the_previous_parent(node: dict[str, Any]) -> None:
    """The last child in the first step with a split cites the accepted row before its
    parent, which ends below it: the predecessor's upper end refuses it."""
    step = next(step for step in node["steps"] if children(step))
    index = children(step)[-1] + 1
    child = step["rows"][index]
    child["prior_reference"] = next(
        row["prior_reference"]
        for row in reversed(step["rows"][:index])
        if row["prior_reference"] != child["prior_reference"]
    )


def insert_an_empty_row(node: dict[str, Any]) -> None:
    """The closing step's first row is preceded by a copy of itself over the single angle
    0, an empty interval that the partition refuses."""
    rows = node["steps"][-1]["rows"]
    empty = copy.deepcopy(rows[0])
    empty["interval"] = ["0", "0"]
    rows.insert(0, empty)


def cite_the_grandparent(node: dict[str, Any]) -> None:
    """A row of the closing step cites its predecessor's own predecessor, which contains it
    but was replaced at the owner's previous step: only acceptance can refuse it."""
    last = node["steps"][-1]
    earlier = [step for step in node["steps"][:-1] if step["owner"] == last["owner"]][-1]
    row = last["rows"][0]
    parent = next(r for r in earlier["rows"] if r["reference"] == row["prior_reference"])
    row["prior_reference"] = parent["prior_reference"]


def cite_the_partner(node: dict[str, Any]) -> None:
    """A row cites the partner's accepted row with its interval, not one of its own."""
    step = node["steps"][-1]
    items = next(iter(step["prior_partner_pose_covers"].values()))
    step["rows"][0]["prior_reference"] = items[0]["reference"]


def unchecked_beyond_the_seed_grid(node: dict[str, Any]) -> None:
    """The closure step's last row, past the seed's two bins, loses its collision regions."""
    rows = node["steps"][-1]["rows"]
    assert len(rows) > 2
    rows[-1]["collision_regions"] = []


def start_above_zero(node: dict[str, Any]) -> None:
    """The closing step's first row starts at 2^-20: the half-angles below it are no row's."""
    node["steps"][-1]["rows"][0]["interval"][0] = str(Q(1, 2**20))


def point_strict_on_one_half(lo: Q, hi: Q, which: str) -> Point:
    """A point strictly inside the unit square at every half-angle of one half of
    `[lo, hi]` but not at every half-angle of the whole row, by a search over directions
    and radii near the square's boundary (the search of lane R6's
    `audit-verifier-rewrites/refinement/mutate_refined.py.txt`)."""
    mid = (lo + hi) / 2
    half = (lo, mid) if which == "lower" else (mid, hi)
    for k in range(720):
        phi = math.pi * k / 360
        direction = (
            Q(round(math.cos(phi) * 2**16), 2**16),
            Q(round(math.sin(phi) * 2**16), 2**16),
        )
        for step in range(160):
            r = Q(45, 100) + Q(step, 512)
            p = (r * direction[0], r * direction[1])
            if kernel_verifier.core_strict([p], *half) and not kernel_verifier.core_strict(
                [p], lo, hi
            ):
                return p
    raise AssertionError(f"no point is strict over the {which} half of [{lo}, {hi}] alone")


def grow_core_by_a_half_strict_point(which: str) -> Callable[[dict[str, Any]], None]:
    """The closing step's first row's core grown by a point strict over one half of the
    row only, with its common-core planes recomputed: the core still contains the old
    one, so every other obligation of the row holds and only strictness over the whole
    row can refuse it. A verifier proving the core over that half alone accepts it."""

    def edit(node: dict[str, Any]) -> None:
        row = node["steps"][-1]["rows"][0]
        lo, hi = Q(row["interval"][0]), Q(row["interval"][1])
        core = kernel_verifier.hull(decode(row["core_vertices"]))
        grown = kernel_verifier.hull([*core, point_strict_on_one_half(lo, hi, which)])
        row["core_vertices"] = encode(grown)
        vertices = [v for polygon in row["residual_polygons"] for v in decode(polygon)]
        row["common_core_halfplanes"] = common_core_planes(grown, vertices) if vertices else []

    return edit


def grow_partner_core_by_a_half_strict_point(which: str) -> Callable[[dict[str, Any]], None]:
    """A refined partner row's published core in the closing step grown likewise."""

    def edit(node: dict[str, Any]) -> None:
        covers = node["steps"][-1]["prior_partner_pose_covers"]
        items = next(items for items in covers.values() if len(items) > 2)
        item = next(item for item in items if item["core"])
        lo, hi = Q(item["interval"][0]), Q(item["interval"][1])
        core = kernel_verifier.hull(decode(item["core"]))
        item["core"] = encode(
            kernel_verifier.hull([*core, point_strict_on_one_half(lo, hi, which)])
        )

    return edit


@pytest.mark.parametrize(
    ("edit", "message"),
    [
        (leave_gap, "interval gap"),
        (overlap, "interval overlap"),
        (stop_short, "do not reach the end"),
        (cite_the_next_parent, "escapes its predecessor"),
        (cite_the_previous_parent, "escapes its predecessor"),
        (insert_an_empty_row, "row 0: interval is empty"),
        (cite_the_grandparent, "not an accepted row"),
        (cite_the_partner, "not an accepted row"),
        (unchecked_beyond_the_seed_grid, "NOT covered"),
        (start_above_zero, "interval gap"),
        pytest.param(
            grow_core_by_a_half_strict_point("lower"),
            "core not strict",
            id="grow_core_lower_half-core not strict",
        ),
        pytest.param(
            grow_core_by_a_half_strict_point("upper"),
            "core not strict",
            id="grow_core_upper_half-core not strict",
        ),
        pytest.param(
            grow_partner_core_by_a_half_strict_point("lower"),
            "core not strict",
            id="grow_partner_core_lower_half-core not strict",
        ),
        pytest.param(
            grow_partner_core_by_a_half_strict_point("upper"),
            "core not strict",
            id="grow_partner_core_upper_half-core not strict",
        ),
    ],
)
def test_the_kernel_verifier_refuses_a_doctored_refinement(
    tmp_path: Path, edit: Callable[[dict[str, Any]], None], message: str
) -> None:
    receipt = kernel_verifier.verify(
        split_certificate(tmp_path, "blind", edit), pair_cells(tmp_path, "blind")
    )
    assert receipt["status"] == "FAIL"
    assert message in receipt["failure"]


def drop_a_late_collision(node: dict[str, Any]) -> None:
    """The last row of the first step with more rows than the seed's two loses its
    collision regions; that step is not the closure, so only a sample can reach it."""
    step = next(step for step in node["steps"][:-1] if len(step["rows"]) > 2)
    step["rows"][-1]["collision_regions"] = []


def test_a_sample_draws_from_the_steps_own_rows(tmp_path: Path) -> None:
    receipt = kernel_verifier.verify(
        split_certificate(tmp_path, "blind", drop_a_late_collision),
        pair_cells(tmp_path, "blind"),
        sample=8,
    )
    assert receipt["status"] == "FAIL"
    assert "NOT covered" in receipt["failure"]


def common_core_planes(core: list[Point], vertices: list[Point]) -> list[dict[str, Any]]:
    """The published form of each core edge's plane moved out to the least vertex."""
    planes: list[dict[str, Any]] = []
    for k in range(len(core)):
        p, q = core[k], core[(k + 1) % len(core)]
        a, b = q[1] - p[1], p[0] - q[0]
        least = min(a * v[0] + b * v[1] for v in vertices)
        planes.append({"normal": [str(a), str(b)], "upper": str(a * p[0] + b * p[1] + least)})
    return planes


def cut_to_the_upper_half(node: dict[str, Any]) -> None:
    """The first live child row keeps only the residual that the legal box of its upper
    half admits, dropping poses that its own, wider box admits. Its common-core planes are
    recomputed, and its bounds dropped when nothing is left, so that only the cover can
    refuse it: a verifier that cut a row by a box narrower than its own would accept it."""
    for step in node["steps"]:
        for index in sorted({i + k for i in children(step) for k in (0, 1)}):
            row = step["rows"][index]
            lo, hi = Q(row["interval"][0]), Q(row["interval"][1])
            box = kernel_verifier.wall_box((lo + hi) / 2, hi, Q(3))
            given = [kernel_verifier.hull(decode(p)) for p in row["residual_polygons"]]
            cut = [
                kernel_verifier.hull(kernel_verifier.intersect_convex(p, box)) for p in given
            ]
            cut = [p for p in cut if len(p) >= 3]
            if not given or cut == given:
                continue
            row["residual_polygons"] = [encode(p) for p in cut]
            vertices = [v for p in cut for v in p]
            core = kernel_verifier.hull(decode(row["core_vertices"]))
            row["common_core_halfplanes"] = common_core_planes(core, vertices) if cut else []
            if not cut:
                row["outer_bounds"], row["outer_domain"] = [], []
            return
    raise AssertionError("no child row's residual reaches past its upper half's box")


def test_the_kernel_verifier_refuses_a_row_cut_to_a_narrower_box(tmp_path: Path) -> None:
    receipt = kernel_verifier.verify(
        split_certificate(tmp_path, "wall", cut_to_the_upper_half), pair_cells(tmp_path, "wall")
    )
    assert receipt["status"] == "FAIL"
    assert "NOT covered" in receipt["failure"]


# ---------------------------------------------------------------------------
# Forged one-row closures: the cover of a segment, and of a one-point section
# ---------------------------------------------------------------------------


def tiny_square(centre: Point) -> list[Point]:
    x, y = centre
    r = Q(1, 100)
    return [(x - r, y - r), (x + r, y - r), (x + r, y + r), (x - r, y + r)]


def forged_closure(
    directory: Path, claimed: list[Point], owned: list[Point], half: Q
) -> tuple[Path, kernel_verifier.Cells]:
    """A closure of owner 0 in one step of one row, every pose claimed forbidden.

    Owner 0's cell is `claimed` and owns nothing; each point of `owned` is the one owned
    point of another owner, whose cell is a square of side 1/50 about it. The seed has
    one half-angle row, `[0, 1]`, so the legal box is `[1/2, 5/2]^2` and the row's
    required domain is `claimed` cut by it. The row's core is the square of half-side
    `half` about the origin, so each forbidden region is the square of half-side `half`
    about an owned point. The row publishes no residual and no collision region, so its
    cover alone decides whether the closure stands.
    """
    directory.mkdir(parents=True)
    cap = Q(3)
    cells = [claimed, *(tiny_square(p) for p in owned)]
    mask = list(range(len(cells)))
    box = kernel_verifier.wall_box(Q(0), Q(1), cap)
    domains = [kernel_verifier.hull(kernel_verifier.intersect_convex(c, box)) for c in cells]
    groups = {"0": [], **{str(k): encode([p]) for k, p in enumerate(owned, start=1)}}
    seeded = [{"kind": "wall_seed", "owner": o, "row": 0} for o in mask]
    seed = {
        "schema": "generic_wall_seed_v1",
        "mask_index": None,
        "mask": mask,
        "U": str(cap),
        "B": "1",
        "bins": 1,
        "groups": groups,
        "cells": {
            str(o): [
                {
                    "interval": ["0", "1"],
                    "residual_polygons": [encode(domains[o])],
                    "outer_domain": encode(domains[o]),
                    "outer_bounds": [],
                    "reference": seeded[o],
                }
            ]
            for o in mask
        },
        "world": [encode(c) for c in cells],
    }
    reference = {"kind": "phase3", "node": "forged", "step": 0, "row": 0}
    core = [(-half, -half), (half, -half), (half, half), (-half, half)]
    row = {
        "interval": ["0", "1"],
        "prior_reference": seeded[0],
        "reference": reference,
        "core_vertices": encode(core),
        "collision_regions": [],
        "residual_polygons": [],
        "common_core_halfplanes": [],
        "outer_bounds": [],
        "outer_domain": [],
    }
    final = {"0": [{"reference": reference, "outer_domain": [], "residual_polygons": []}]}
    for o in mask[1:]:
        final[str(o)] = [
            {
                "reference": seeded[o],
                "outer_domain": encode(domains[o]),
                "residual_polygons": [encode(domains[o])],
            }
        ]
    node = {
        "schema": "exact_generic_owned_hull_v1",
        "node_id": "forged",
        "U": str(cap),
        "B": "1",
        "mask": mask,
        "parent": None,
        "constraints": [],
        "guard_source": None,
        "source": {"sha256": hashlib.sha256(canonical(seed)).hexdigest()},
        "initial": {
            "groups": groups,
            "cell_references": {str(o): [seeded[o]] for o in mask},
        },
        "steps": [
            {
                "index": 0,
                "owner": 0,
                "complete": True,
                "allowed_half_angle": ["0", "1"],
                "prior_owned_hulls": groups,
                "prior_partner_pose_covers": {},
                "rows": [row],
                "common_owned_kernel": [],
            }
        ],
        "contradiction": {"kind": "all_parent_poses_forbidden", "owner": 0, "step": 0},
        "final_state": {"groups": groups, "cells": final},
        "closed": True,
        "terminal": True,
        "mask_exclusion_proved": False,
        "global_optimality_proved": False,
    }
    save_certificate(directory / "cert", seed, node)
    names = [f"cell-{o}" for o in mask]
    path = cells_file(directory, cap, names, cells)
    cells_object = kernel_verifier.file_cells(
        path, hashlib.sha256(path.read_bytes()).hexdigest()
    )
    return directory / "cert", cells_object


# Owner 0's cell meets the legal box `[1/2, 5/2]^2` in the segment from (1/2, 3/4) to
# (1/2, 5/4) alone, so the row's required domain has zero area.
SEGMENT_CELL = [(Q(1, 4), Q(1)), (Q(1, 2), Q(3, 4)), (Q(1, 2), Q(5, 4))]
SEGMENT_MARKS = [(Q(1, 2), Q(3, 4)), (Q(1, 2), Q(1)), (Q(1, 2), Q(5, 4))]


def test_a_segment_row_is_covered_as_a_whole_not_at_its_ends_and_midpoint(
    tmp_path: Path,
) -> None:
    """Forbidden squares of half-side 1/16 about the segment's ends and midpoint leave
    `(13/16, 15/16)` and `(17/16, 19/16)` of it uncovered; a check of those three points
    alone accepted the closure. At half-side 1/8 the squares meet at closed seams."""
    gaps, cells = forged_closure(tmp_path / "gaps", SEGMENT_CELL, SEGMENT_MARKS, Q(1, 16))
    receipt = kernel_verifier.verify(gaps, cells)
    assert receipt["status"] == "FAIL"
    assert receipt["failure"] == "step 0 row 0: degenerate row uncovered"
    seams, cells = forged_closure(tmp_path / "seams", SEGMENT_CELL, SEGMENT_MARKS, Q(1, 8))
    receipt = kernel_verifier.verify(seams, cells)
    assert receipt["status"] == "PASS", receipt["failure"]
    assert receipt["counts"]["degenerate_cover_checks"] == 1


# Owner 0's cell is a wedge inside the legal box whose leftmost point, the vertex (1, 1),
# is the whole of its section at x = 1.
WEDGE_CELL = [(Q(1), Q(1)), (Q(13, 10), Q(9, 10)), (Q(13, 10), Q(11, 10))]
BELOW_THE_VERTEX = (Q(1), Q(1, 2))


def test_a_one_point_section_needs_a_span_that_contains_it(tmp_path: Path) -> None:
    """The square about (13/10, 1) covers the wedge from x = 21/20 on; at x = 1 the only
    span is the square about (1, 1/2), `[1/4, 3/4]`, wholly below the vertex. The sweep
    must refuse at the vertex itself, where a merge that let a one-point section through
    reported the open slab beside it instead; with the square moved to (5/4, 1) its edge
    at x = 1 holds the vertex and the closure stands."""
    short, cells = forged_closure(
        tmp_path / "short", WEDGE_CELL, [(Q(13, 10), Q(1)), BELOW_THE_VERTEX], Q(1, 4)
    )
    receipt = kernel_verifier.verify(short, cells)
    assert receipt["status"] == "FAIL"
    assert receipt["failure"] == "step 0 row 0: required domain NOT covered (uncovered at x=1)"
    flush, cells = forged_closure(
        tmp_path / "flush", WEDGE_CELL, [(Q(5, 4), Q(1)), BELOW_THE_VERTEX], Q(1, 4)
    )
    receipt = kernel_verifier.verify(flush, cells)
    assert receipt["status"] == "PASS", receipt["failure"]


# ---------------------------------------------------------------------------
# The kernel verifier's integer forms, against its Fraction forms
# ---------------------------------------------------------------------------


def convex_polygon(rng: random.Random, vertices: int) -> list[Point]:
    """A random convex polygon with at least three hull vertices, on a coarse grid."""
    while True:
        points = [
            (Q(rng.randint(-20, 20), 64), Q(rng.randint(-20, 20), 64)) for _ in range(vertices)
        ]
        found = kernel_verifier.hull(points)
        if len(found) >= 3:
            return found


def encode(polygon: list[Point]) -> list[list[str]]:
    return [[str(x), str(y)] for x, y in polygon]


def homogeneous(polygon: list[Point]) -> tuple[kernel_verifier.HPoint, ...]:
    return tuple(kernel_verifier.homogeneous(v) for v in polygon)


def canonical_plane(a: Q, b: Q, c: Q) -> tuple[int, int, Q]:
    """`a x + b y <= c` with an integer normal in lowest terms, for comparing facet sets."""
    scale = math.lcm(a.denominator, b.denominator)
    ai, bi = int(a * scale), int(b * scale)
    g = math.gcd(ai, bi)
    return ai // g, bi // g, c * scale / g


SQUARE = [(Q(-1, 4), Q(-1, 4)), (Q(1, 4), Q(-1, 4)), (Q(1, 4), Q(1, 4)), (Q(-1, 4), Q(1, 4))]


def test_difference_facets_are_the_hull_facets() -> None:
    rng = random.Random(7)
    pairs = [(SQUARE, [(x / 2, y / 2) for x, y in SQUARE])]
    pairs.extend(
        (convex_polygon(rng, 3 + rng.randrange(5)), convex_polygon(rng, 3 + rng.randrange(4)))
        for _ in range(40)
    )
    for partner, core in pairs:
        difference = kernel_verifier.minkowski_diff(partner, core)
        reference = {
            canonical_plane(a, b, c) for a, b, c in kernel_verifier.planes_of(difference)
        }
        facets = kernel_verifier.difference_facets(homogeneous(partner), homogeneous(core))
        assert {(nx, ny, Q(hn, hd)) for nx, ny, hn, hd in facets} == reference
        assert len(facets) == len(reference)


def tiling(rng: random.Random, domain: list[Point], cuts: int) -> list[list[Point]]:
    """The domain cut by random lines into convex pieces that cover it exactly."""
    pieces = [domain]
    for _ in range(cuts):
        a, b = Q(rng.randint(-5, 5)), Q(rng.randint(-5, 5))
        if a == 0 and b == 0:
            continue
        inside = rng.choice(domain)
        c = a * inside[0] + b * inside[1] + Q(rng.randint(-3, 3), 128)
        out: list[list[Point]] = []
        for piece in pieces:
            for sign in (1, -1):
                part = kernel_verifier.clip_closed(piece, sign * a, sign * b, sign * c)
                if len(part) >= 3 and kernel_verifier.area2(part) > 0:
                    out.append(kernel_verifier.hull(part))
        pieces = out
    return pieces


def shifted(polygon: list[Point], dx: Q) -> list[Point]:
    return kernel_verifier.hull([(x + dx, y) for x, y in polygon])


def test_the_sweep_agrees_with_the_area_cover() -> None:
    rng = random.Random(11)
    verdicts: set[bool] = set()
    rectangle = [(Q(0), Q(0)), (Q(2), Q(0)), (Q(2), Q(1)), (Q(0), Q(1))]
    for trial in range(48):
        domain = rectangle if trial % 6 == 0 else convex_polygon(rng, 4 + rng.randrange(4))
        regions = tiling(rng, domain, 1 + rng.randrange(4))
        kind = trial % 4
        if kind == 1 and len(regions) > 1:
            regions.pop(rng.randrange(len(regions)))
        elif kind == 2:
            index = rng.randrange(len(regions))
            regions[index] = shifted(regions[index], Q(1, 2**30))
        elif kind == 3:
            regions.extend(convex_polygon(rng, 3 + rng.randrange(3)) for _ in range(2))
            regions.append([(Q(0), Q(0)), (Q(1), Q(0))])
        rng.shuffle(regions)
        by_area = kernel_verifier.covered_by_area(domain, regions)[0]
        by_sweep, probe = kernel_verifier.covered_by_sweep(domain, regions)
        assert by_sweep == by_area, (trial, probe)
        assert (probe is None) == by_sweep
        verdicts.add(by_area)
    assert verdicts == {True, False}


def lens_regions(eps: Q) -> tuple[list[Point], list[list[Point]]]:
    """A square domain under four regions that cover it except for a sliver hidden
    strictly between two sweep events.

    The left block's vertical edge covers the whole section at x = 1 and the right block's
    at x = 3. Between them a region whose roof rises from (1, 2) to (2, 9/4) sits under a
    region whose V-shaped floor starts `2 eps` above the roof at x = 1 and crosses it at
    x = 1 + 4 eps. The gap over (1, 1 + 4 eps) is invisible at every event abscissa (the
    vertex abscissae and the crossing, where the two sections touch) and visible only on
    the open slab between them, so a sweep that probed events alone, or that did not
    treat crossings as events, would pass it. With eps = 0 the four regions cover exactly.
    """
    big = [(Q(0), Q(0)), (Q(4), Q(0)), (Q(4), Q(4)), (Q(0), Q(4))]
    left = [(Q(0), Q(0)), (Q(1), Q(0)), (Q(1), Q(4)), (Q(0), Q(4))]
    right = [(Q(3), Q(0)), (Q(4), Q(0)), (Q(4), Q(4)), (Q(3), Q(4))]
    below = kernel_verifier.hull(
        [(Q(1), Q(0)), (Q(3), Q(0)), (Q(3), Q(2)), (Q(2), Q(9, 4)), (Q(1), Q(2))]
    )
    top = 2 + 2 * eps
    above = kernel_verifier.hull(
        [(Q(1), Q(4)), (Q(3), Q(4)), (Q(3), top), (Q(2), top - Q(1, 4)), (Q(1), top)]
    )
    return big, [left, right, below, above]


def test_the_sweep_sees_a_gap_hidden_between_events() -> None:
    for eps in (Q(1, 2**40), Q(1, 2**60), Q(1, 8)):
        domain, regions = lens_regions(eps)
        assert kernel_verifier.covered_by_area(domain, regions)[0] is False
        covered, probe = kernel_verifier.covered_by_sweep(domain, regions)
        assert covered is False
        assert probe is not None
        assert 1 < probe < 1 + 4 * eps
    domain, regions = lens_regions(Q(0))
    assert kernel_verifier.covered_by_area(domain, regions)[0] is True
    assert kernel_verifier.covered_by_sweep(domain, regions) == (True, None)


def test_between_lies_strictly_inside_with_small_terms() -> None:
    rng = random.Random(3)
    pairs: list[tuple[tuple[int, int], tuple[int, int]]] = [
        ((10**60, 3 * 10**60 + 1), (10**60 + 1, 3 * 10**60 + 1)),
        ((-7, 2), (-3, 1)),
        ((0, 1), (1, 10**9)),
    ]
    while len(pairs) < 200:
        a = (rng.randint(-(10**6), 10**6), rng.randint(1, 10**6))
        b = (rng.randint(-(10**6), 10**6), rng.randint(1, 10**6))
        if kernel_verifier.ratio_lt(a, b):
            pairs.append((a, b))
    for a, b in pairs:
        n, d = kernel_verifier.between(a, b)
        assert d > 0
        assert kernel_verifier.ratio_lt(a, (n, d))
        assert kernel_verifier.ratio_lt((n, d), b)
        assert d <= a[1] + b[1]


# ---------------------------------------------------------------------------
# The closed-interval merge and the degenerate cover, held to the n11 review's contract
# (finding C2: a one-point target is covered only by a span containing it)
# ---------------------------------------------------------------------------

ENDPOINTS = [Q(value) for value in range(-3, 4)]
INTERVALS = [(lo, hi) for lo in ENDPOINTS for hi in ENDPOINTS if lo <= hi]
FAMILIES: list[tuple[tuple[Q, Q], ...]] = [
    (),
    *((interval,) for interval in INTERVALS),
    *combinations_with_replacement(INTERVALS, 2),
]


def section(interval: tuple[Q, Q]) -> kernel_verifier.Section:
    lo, hi = interval
    return (lo.numerator, lo.denominator), (hi.numerator, hi.denominator)


def merged(target: tuple[Q, Q], spans: Sequence[tuple[Q, Q]]) -> bool:
    return kernel_verifier.section_covered(section(target), [section(s) for s in spans])


def test_the_merge_is_the_corrected_cover_on_the_reviewed_12180_cases() -> None:
    """Every target and every family of at most two of the 28 closed intervals with
    integer ends in -3..3, against the review's corrected reference."""
    assert len(INTERVALS) * len(FAMILIES) == 12_180
    wrong = [
        (target, spans)
        for target in INTERVALS
        for spans in FAMILIES
        if merged(target, spans) is not closed_interval.covers_closed_interval(target, spans)
    ]
    assert wrong == []


def test_the_merge_meets_the_reviews_acceptance_cases() -> None:
    one, half, gap = Q(1), Q(1, 2), Q(1, 10**50)
    assert merged((one, one), [(Q(0), Q(0))]) is False
    assert merged((one, one), []) is False
    assert merged((one, one), [(Q(-2), Q(-1)), (Q(0), Q(0))]) is False
    assert merged((one, one), [(Q(0), Q(0)), (half, one)]) is True
    assert merged((one, one), [(one, one)]) is True
    assert merged((one, one), [(one, Q(3))]) is True
    assert merged((Q(0), one), [(half, one), (Q(0), half)]) is True
    assert merged((Q(0), one), [(Q(0), half), (half + gap, one)]) is False
    assert merged((Q(0), one), [(Q(0), half - gap), (half, one)]) is False
    assert merged((Q(0), one), [(gap, one)]) is False
    assert merged((Q(0), one), [(Q(0), one - gap)]) is False


@pytest.mark.parametrize(
    ("target", "spans"),
    [
        (((1, 1), (0, 1)), []),
        (((0, 1), (1, 1)), [((1, 1), (0, 1))]),
        (((0, 1), (1, 1)), [((0, 1), (1, 0))]),
        (((0, 1), (1, 1)), [((-2, -1), (3, 1))]),
        (((0.0, 1), (1, 1)), []),
        (((0, 1), (1, 1)), [((0, 1), (math.nan, 1))]),
        (((False, 1), (True, 1)), [((0, 1), (1, 1))]),
        ((("0", 1), (1, 1)), [((0, 1), (1, 1))]),
        (((0, 1), None), [((0, 1), (1, 1))]),
        (((0, 1), (1, 1), (2, 1)), [((0, 1), (2, 1))]),
        (((0, 1), (1, 1)), [((0, 1),)]),
        ((0, 1), [((0, 1), (1, 1))]),
    ],
)
def test_the_merge_refuses_a_malformed_interval(target: Any, spans: Any) -> None:
    with pytest.raises(kernel_verifier.VerificationError, match="malformed coverage interval"):
        kernel_verifier.section_covered(target, spans)


def box(x0: Q, x1: Q) -> list[Point]:
    return [(x0, Q(-1)), (x1, Q(-1)), (x1, Q(2)), (x0, Q(2))]


def test_a_degenerate_domain_is_covered_only_as_a_whole() -> None:
    """The segment from (0, 0) to (2, 1), and the point (1, 1), against polygons,
    segments and points: closed seams join, a positive gap refuses however small, and
    regions holding the segment's ends and midpoint do not cover the rest of it."""
    segment = [(Q(0), Q(0)), (Q(1), Q(1, 2)), (Q(2), Q(1))]
    gap = Q(1, 2**50)
    covered = kernel_verifier.degenerate_covered
    assert covered(segment, [box(Q(-1), Q(1)), box(Q(1), Q(3))])
    assert not covered(segment, [box(Q(-1), Q(1)), box(Q(1) + gap, Q(3))])
    assert not covered(segment, [box(Q(-1), Q(1) - gap), box(Q(1), Q(3))])
    marks = [box(x - Q(1, 4), x + Q(1, 4)) for x in (Q(0), Q(1), Q(2))]
    assert all(
        any(kernel_verifier.inside(r, p) for r in marks)
        for p in [(Q(0), Q(0)), (Q(1), Q(1, 2)), (Q(2), Q(1))]
    )
    assert not covered(segment, marks)
    halves = [[(Q(0), Q(0)), (Q(1), Q(1, 2))], [(Q(2), Q(1)), (Q(1), Q(1, 2))]]
    assert covered(segment, halves)
    assert not covered(segment, [halves[0], [(Q(2), Q(1)), (Q(1) + gap, Q(1, 2) + gap / 2)]])
    assert not covered(segment, [halves[0], [(Q(1), Q(1, 2))], [(Q(1), Q(1, 2)), (Q(2), Q(2))]])
    assert not covered(segment, [])
    point = [(Q(1), Q(1))]
    assert covered(point, [[(Q(1), Q(1))]])
    assert covered(point, [[(Q(0), Q(0)), (Q(2), Q(2))]])
    assert covered(point, [box(Q(1), Q(3))])
    assert not covered(point, [[(Q(0), Q(0)), (Q(2), Q(2) + gap)]])
    assert not covered(point, [box(Q(1) + gap, Q(3))])
    assert not covered(point, [])


def unit_cell() -> list[Point]:
    return [(Q(1), Q(1)), (Q(2), Q(1)), (Q(2), Q(2)), (Q(1), Q(2))]


def cover_state() -> tuple[kernel_verifier.State, kernel_verifier.Row, dict[str, Any]]:
    """A state with one partner row whose published cover is sound."""
    state = kernel_verifier.State(
        cells=[unit_cell(), unit_cell()], cap=Q(3), bins=1, mask=[0, 1]
    )
    residual = kernel_verifier.hull(
        [(Q(1), Q(1)), (Q(3, 2), Q(1)), (Q(3, 2), Q(3, 2)), (Q(1), Q(3, 2))]
    )
    row = kernel_verifier.Row(
        (Q(0), Q(1)), {"kind": "wall_seed", "owner": 1, "row": 0}, residual, [residual]
    )
    state.rows[1] = [row]
    item = {
        "reference": row.reference,
        "interval": ["0", "1"],
        "domain": encode(residual),
        "core": encode(SQUARE),
    }
    return state, row, item


def step_with(item: dict[str, Any]) -> dict[str, Any]:
    return {"owner": 0, "prior_partner_pose_covers": {"1": [item]}}


def test_a_republished_partner_cover_is_reused_only_when_identical() -> None:
    state, row, item = cover_state()
    partners = kernel_verifier.check_partners(state, step_with(item), 0)
    admitted = partners[1][0]
    assert row.cover is admitted
    again = kernel_verifier.check_partners(state, step_with(copy.deepcopy(item)), 1)
    assert again[1][0] is admitted
    assert state.stats["partner_rows"] == 2
    shrunk = copy.deepcopy(item)
    shrunk["domain"] = shrunk["domain"][:3]
    with pytest.raises(kernel_verifier.VerificationError, match="domain"):
        _ = kernel_verifier.check_partners(state, step_with(shrunk), 2)
    wide = copy.deepcopy(item)
    wide["core"] = encode([(2 * x, 2 * y) for x, y in SQUARE])
    with pytest.raises(kernel_verifier.VerificationError, match="core not strict"):
        _ = kernel_verifier.check_partners(state, step_with(wide), 3)
    assert row.cover is admitted
    replaced = kernel_verifier.hull(
        [(Q(1), Q(1)), (Q(5, 4), Q(1)), (Q(5, 4), Q(5, 4)), (Q(1), Q(5, 4))]
    )
    state.rows[1] = [kernel_verifier.Row(row.interval, row.reference, replaced, [replaced])]
    with pytest.raises(kernel_verifier.VerificationError, match="domain"):
        _ = kernel_verifier.check_partners(state, step_with(item), 4)
    assert state.rows[1][0].cover is None


def test_the_facet_cache_keys_on_the_exact_cores() -> None:
    state = kernel_verifier.State(cells=[], cap=Q(3), bins=1, mask=[])
    partner = homogeneous(unit_cell())
    core = homogeneous(SQUARE)
    moved = homogeneous([(x + Q(1, 2**40), y) if x > 0 else (x, y) for x, y in SQUARE])
    first = state.difference(partner, core)
    second = state.difference(partner, moved)
    assert state.difference(partner, core) is first
    assert second == kernel_verifier.difference_facets(partner, moved)
    assert first != second
    assert len(state.facets) == 2


def test_the_forbidden_region_cache_keys_on_the_exact_core() -> None:
    state = kernel_verifier.State(cells=[], cap=Q(3), bins=1, mask=[])
    group = unit_cell()
    moved = [(x + Q(1, 2**40), y) if x > 0 else (x, y) for x, y in SQUARE]
    first = state.forbidden_region(group, SQUARE)
    second = state.forbidden_region(group, moved)
    assert state.forbidden_region(group, SQUARE) is first
    assert second == kernel_verifier.minkowski_diff(group, moved)
    assert first != second
    assert len(state.forbidden) == 2


def test_the_row_minimum_memo_keys_on_the_whole_direction() -> None:
    domain = homogeneous(unit_cell())
    cover = kernel_verifier.CoverRow([], [], domain, homogeneous(SQUARE))
    for nx, ny in ((0, 1), (0, -1), (1, 0), (1, 2), (-1, 2)):
        assert cover.minimum(nx, ny) == kernel_verifier.support(domain, nx, ny, largest=False)
    assert cover.minimum(0, 1) != cover.minimum(0, -1)
    assert cover.minimum(1, 0) != cover.minimum(1, 2)
    assert len(cover.minima) == 5


# ---------------------------------------------------------------------------
# The branch-and-bound verifier, on the three-in-a-row round trip of P2's tests
# ---------------------------------------------------------------------------


def rectangle(x0: str, x1: str) -> tuple[tuple[Q, Q], ...]:
    a, b, c, d = Q(x0), Q(x1), Q("2.00"), Q("2.05")
    return ((a, c), (b, c), (b, d), (a, d))


ROW = ("left", "middle", "right")
ROW_CELLS = (rectangle("1.00", "1.05"), rectangle("1.40", "2.40"), rectangle("2.80", "2.85"))


@pytest.fixture(scope="module")
def row_certificates(tmp_path_factory: pytest.TempPathFactory) -> dict[int, Path]:
    """The crowded row's certificates without and with bound tightening, made once."""
    made: dict[int, Path] = {}
    pattern = bb.Pattern(ROW, ROW_CELLS, bb.cover.U)
    for obbt_rounds in (0, 3):
        directory = tmp_path_factory.mktemp(f"row-obbt{obbt_rounds}")
        settings = bb.Settings(obbt_rounds=obbt_rounds)
        result = bb.search(pattern, settings, certificate=directory)
        assert result["verdict"] == "certified-infeasible"
        made[obbt_rounds] = directory
    return made


def row_cells(tmp_path: Path) -> bb_verifier.Cells:
    path = cells_file(tmp_path, bb.cover.U, list(ROW), list(ROW_CELLS))
    return bb_verifier.file_cells(path, hashlib.sha256(path.read_bytes()).hexdigest())


@pytest.mark.parametrize("obbt_rounds", [0, 3])
def test_the_bb_verifier_passes_the_round_trip_certificate(
    tmp_path: Path, row_certificates: dict[int, Path], obbt_rounds: int
) -> None:
    receipt = bb_verifier.verify_certificate(row_certificates[obbt_rounds], row_cells(tmp_path))
    assert receipt["status"] == "PASS", receipt["failures"]
    assert receipt["mode"] == "full"
    assert receipt["checked_nodes"] == receipt["nodes"] > 1
    assert receipt["pattern"] == list(ROW)


def read_named(directory: Path, name: str) -> Any:
    return json.loads(gzip.decompress((directory / f"{name}.json.gz").read_bytes()))


def write_named(directory: Path, document: Any) -> str:
    data = json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    name = hashlib.sha256(data.encode()).hexdigest()
    (directory / f"{name}.json.gz").write_bytes(gzip.compress(data.encode(), mtime=0))
    return name


def rational(q: Q) -> str:
    return f"{q.numerator}/{q.denominator}"


def first_round(nodes: list[dict[str, Any]], key: str) -> dict[str, Any] | None:
    return next((r for n in nodes for r in n["rounds"] if r.get(key)), None)


def corrupt(directory: Path, kind: str) -> str | None:
    """R4's corruptions (`audit-A/corrupt_cert.py.txt`): one change, re-hashed; the manifest.

    None when the certificate has no record of the kind.
    """
    manifest = read_named(directory, bb_verifier.manifest_from_readme(directory))
    chunks = [read_named(directory, c)["nodes"] for c in manifest["chunks"]]
    nodes = [n for chunk in chunks for n in chunk]
    nudge = Q(1, 10**9)
    if kind == "cut_v":
        record = next(
            (
                r
                for n in nodes
                for r in n["rounds"]
                if any(f[0][0] == "u" for f in r.get("farkas", []))
            ),
            None,
        )
        if record is None:
            return None
        ref = next(f[0] for f in record["farkas"] if f[0][0] == "u")
        cut = record["cuts"][ref[1]]
        cut[3] = rational(Q(cut[3]) + nudge)
    elif kind == "farkas_y":
        record = first_round(nodes, "farkas")
        if record is None:
            return None
        record["farkas"][0][1] = rational(-Q(record["farkas"][0][1]))
    elif kind == "bound":
        record = first_round(nodes, "bounds")
        if record is None:
            return None
        record["bounds"][0][2] = rational(Q(record["bounds"][0][2]) + nudge)
    elif kind == "box":
        node = next(n for n in nodes if n["rounds"])
        node["rounds"][0]["boxes"][0][0] = rational(Q(node["rounds"][0]["boxes"][0][0]) + nudge)
    elif kind == "lost_child":
        leaf = next(n for n in nodes if n["closed"] is not None and n["parent"] is not None)
        for chunk in chunks:
            if leaf in chunk:
                chunk.remove(leaf)
    elif kind == "disc":
        node = next((n for n in nodes if n["closed"] == "disc"), None)
        if node is None:
            return None
        record = node["rounds"][-1]
        _, j = manifest["header"]["pairs"][record["closed_pair"][0]]
        record["boxes"][j][1] = rational(Q(record["boxes"][j][1]) + 1)
    elif kind == "split_point":
        node = next(n for n in nodes if n.get("split") and "angle" in n["split"])
        s, _ = node["split"]["angle"]
        node["split"]["angle"][1] = rational(Q(node["angles"][s][1]) + Q(1, 10**6))
    elif kind == "piece":
        found = False
        for record in (r for n in nodes for r in n["rounds"]):
            for pieces in record.get("pairs", {}).values():
                lows = sorted(Q(piece[0]) for piece in pieces)
                if len(lows) >= 2 and lows[0] < lows[1]:
                    piece = min(pieces, key=lambda p: Q(p[0]))
                    if Q(piece[0]) + nudge <= Q(piece[2]):
                        piece[0] = rational(Q(piece[0]) + nudge)
                        found = True
                        break
            if found:
                break
        if not found:
            return None
    else:
        raise ValueError(kind)
    manifest["chunks"] = [write_named(directory, {"nodes": chunk}) for chunk in chunks]
    return write_named(directory, manifest)


KINDS = ("cut_v", "farkas_y", "bound", "box", "lost_child", "disc", "split_point", "piece")


@pytest.mark.parametrize("kind", KINDS)
def test_the_bb_verifier_refuses_each_doctored_kind(
    tmp_path: Path, row_certificates: dict[int, Path], kind: str
) -> None:
    refused = 0
    for obbt_rounds, certificate in row_certificates.items():
        directory = tmp_path / f"obbt{obbt_rounds}"
        _ = shutil.copytree(certificate, directory)
        manifest = corrupt(directory, kind)
        if manifest is None:
            continue
        receipt = bb_verifier.verify_certificate(
            directory, row_cells(tmp_path), manifest=manifest
        )
        assert receipt["status"] == "FAIL", (kind, obbt_rounds)
        refused += 1
    assert refused > 0, f"no certificate carries a {kind} record"


# ---------------------------------------------------------------------------
# Independence
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "module", ["devtools.verify_n17_kernel_certificate", "devtools.verify_n17_bb_certificate"]
)
def test_a_verifier_imports_no_producer_checker_or_solver(module: str) -> None:
    code = (
        "import sys, importlib\n"
        f"verifier = importlib.import_module({module!r})\n"
        "verifier.cover_cells()\n"
        f"forbidden = {FORBIDDEN!r}\n"
        "loaded = [m for m in sys.modules if m.startswith(forbidden) or 'highs' in m.lower()]\n"
        "assert not loaded, loaded\n"
    )
    completed = subprocess.run(
        [sys.executable, "-c", code],
        cwd=PACKING,
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    assert completed.returncode == 0, completed.stderr
