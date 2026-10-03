"""The producer's second-order (octagon) core: strict, larger, and certified unchanged."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import pytest

from devtools import check_hull_kernel_mask0 as mask0_tool
from devtools import check_n17_subpattern as tool
from devtools import verify_n17_kernel_certificate as verifier
from sqpack.hull_kernel import Budget, RefusalError, producer
from sqpack.hull_kernel.frame import Frame, make_frame
from sqpack.hull_kernel.geometry import Polygon, trig
from sqpack.hull_kernel.induction import strict_core
from sqpack.hull_kernel.rational import Q

# The blind pair's node under the default (envelope) core, as the committed producer
# makes it: the octagon option must leave the default bytes alone.
ENVELOPE_BLIND_PAIR_NODE = "c02f318790c4761bb82eaa4197a0f80bf08d6abe3c98bdadc5d726751ac363b9"


def budget() -> Budget:
    return Budget(time.monotonic() + 60, 200_000)


def support(core: Polygon, lo: Q, hi: Q) -> Q:
    """The least support of the core over the body directions at the row's ends and middle."""
    least: Q | None = None
    for t in (lo, hi, (lo + hi) / 2):
        c, s = trig(t)
        for a, b in ((c, s), (-s, c), (-c, -s), (s, -c)):
            value = max(a * x + b * y for x, y in core)
            least = value if least is None else min(least, value)
    assert least is not None
    return least


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


def test_the_octagon_is_strict_and_larger_than_the_envelope_core() -> None:
    frame = mask0_tool.n17_unique_frame()
    for bins in (16, 32):
        for index in range(bins):
            lo, hi = Q(index, bins), Q(index + 1, bins)
            octagon = producer.octagon_core(frame, lo, hi)
            strict_core(frame, octagon, lo, hi)
            assert len(octagon) == 8
            assert support(octagon, lo, hi) > support(
                producer.envelope_core(frame, lo, hi), lo, hi
            )
    assert support(producer.octagon_core(frame, Q(0), Q(1, 16)), Q(0), Q(1, 16)) > Q(498, 1000)
    with pytest.raises(RefusalError, match="unknown core kind"):
        producer.CoreCache("disc")


def test_the_default_core_is_unchanged_and_the_octagon_closes_the_blind_pair(
    blind_pair: Frame, tmp_path: Path
) -> None:
    default = producer.produce(blind_pair, [0, 1], bins=16, max_rounds=2, budget=budget())
    assert producer.content_sha256(default.node) == ENVELOPE_BLIND_PAIR_NODE
    octagon = producer.produce(
        blind_pair, [0, 1], bins=16, max_rounds=2, budget=budget(), core="octagon"
    )
    assert octagon.outcome == "closed"
    assert all(
        len(row["core_vertices"]) == 8
        for step in octagon.node["steps"]
        for row in step["rows"]
        if row["core_vertices"]
    )
    tool.save_certificate(tmp_path, octagon.seed, octagon.node)
    checked = tool.check_saved(tmp_path, blind_pair, max_seconds=60, require_no_producer=False)
    assert checked["status"] == "PASS_SAVED_CLOSED"
    cells = {
        "U": "3",
        "order": list(blind_pair.cell_names),
        "cells": {
            name: [[str(x), str(y)] for x, y in polygon]
            for name, polygon in zip(blind_pair.cell_names, blind_pair.cells, strict=True)
        },
    }
    cells_path = tmp_path / "cells.json"
    cells_path.write_text(json.dumps(cells), encoding="utf-8")
    digest = hashlib.sha256(cells_path.read_bytes()).hexdigest()
    receipt = verifier.verify(tmp_path, verifier.file_cells(cells_path, digest))
    assert receipt["status"] == "PASS", receipt["failure"]
    assert receipt["closed"] is True
