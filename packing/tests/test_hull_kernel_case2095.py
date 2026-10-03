"""The hull kernel's mode-A checker on the n11 frame reproduces case 2095 exactly."""

# pyright: reportPrivateUsage=false
# ruff: noqa: SLF001

from __future__ import annotations

import copy
import dataclasses
import time
from collections.abc import Mapping, Sequence
from fractions import Fraction
from typing import Any

import pytest

from devtools import check_hull_kernel_case2095 as tool
from devtools import check_n11_generic_fresh as frozen
from sqpack.hull_kernel import Budget, RefusalError, node
from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.induction import hull, strict_core, wall_lines
from sqpack.hull_kernel.rational import Q, as_fraction


@pytest.fixture(scope="module")
def sources() -> tool.Sources:
    return tool.load_sources()


@pytest.fixture(scope="module")
def frame(sources: tool.Sources) -> Frame:
    return tool.library_frame(sources)


def budget() -> Budget:
    return Budget(time.monotonic() + 30, tool.MAX_EVENTS)


def fractions_of(polygon: Sequence[tuple[Q, Q]]) -> list[tuple[Fraction, Fraction]]:
    """A kernel polygon as the frozen checkers' `Fraction` points, value for value."""
    return [(as_fraction(x), as_fraction(y)) for x, y in polygon]


def prior(sources: tool.Sources) -> dict[int, list[tuple[Q, Q]]]:
    return {
        owner: hull(node.points(sources.seed["groups"][str(owner)])) for owner in frozen.MASK
    }


def test_the_sample_matches_the_frozen_checker_and_the_receipt(sources: tool.Sources) -> None:
    result = tool.sample_replay(sources, max_seconds=60)
    assert result["status"] == "PASS_PARTIAL_SAMPLE"
    assert result["geometry_verified"] is False
    assert result["row_cover"] == {"events": 87, "probes": 173, "edge_segments": 242}


def test_wall_lines_and_the_strict_core_are_the_frozen_functions(
    sources: tool.Sources, frame: Frame
) -> None:
    for index in range(tool.BINS):
        lo, hi = Q(index, tool.BINS), Q(index + 1, tool.BINS)
        assert wall_lines(frame, lo, hi) == frozen._wall_lines(as_fraction(lo), as_fraction(hi))
    row = sources.source["steps"][0]["rows"][0]
    core = node.convex(node.points(row["core_vertices"]))
    strict_core(frame, core, Q(0), Q(1, 32))
    frozen._strict_core(fractions_of(core), Fraction(0), Fraction(1, 32))
    touching = [(Q(0), Q(0)), (frame.scale / 2, Q(0)), (Q(0), frame.scale / 4)]
    with pytest.raises(RefusalError, match="strict containment"):
        strict_core(frame, touching, Q(0), Q(1, 32))
    with pytest.raises(ValueError, match="strict containment"):
        frozen._strict_core(fractions_of(touching), Fraction(0), Fraction(1, 32))


def test_the_terminal_owner_and_the_transfer(sources: tool.Sources, frame: Frame) -> None:
    assert frame.states_containing(frame.representatives[tool.MASK_INDEX]) == [2095]
    rows = {11: [{"residual_polygons": []}] * 32}
    assert node.admit_contradiction(sources.source, rows) == tool.CONTRADICTION
    with pytest.raises(RefusalError, match="not independently shown"):
        node.admit_contradiction(sources.source, {11: [{"residual_polygons": [[["0", "0"]]]}]})
    changed = copy.deepcopy(sources.source)
    changed["contradiction"]["owner"] = 14
    with pytest.raises(RefusalError, match="names no updated owner"):
        node.admit_contradiction(changed, rows)


def test_perturbed_inputs_are_refused(sources: tool.Sources, frame: Frame) -> None:
    changed = copy.deepcopy(sources.source)
    changed["steps"][0]["rows"][0]["residual_polygons"] = []
    with pytest.raises(RefusalError, match="source content differs"):
        tool.library_frame(dataclasses.replace(sources, source=changed))
    seed = node.admit_seed(
        frame, sources.seed, mask_index=2095, bins=32, budget=budget(), owners=[6]
    )
    step = changed["steps"][0]

    def row(source_step: dict[str, Any], predecessor: Mapping[str, Any]) -> node.RowResult:
        return node.check_row(
            frame,
            changed,
            source_step,
            source_step["rows"][0],
            row_index=0,
            owner=6,
            bins=32,
            prior=prior(sources),
            predecessor=predecessor,
            budget=budget(),
        )

    with pytest.raises(RefusalError, match="uncovered"):
        row(step, seed.rows[6][0])
    with pytest.raises(RefusalError, match="wrong predecessor row"):
        row(step, {**seed.rows[6][0], "reference": {"kind": "wall_seed", "owner": 6, "row": 1}})
    compression = copy.deepcopy(sources.source["steps"][0])
    compression["inner_grid_compression"]["witnesses"][0]["weights"][0] = "2"
    kernel = node.points(compression["common_owned_kernel"])
    with pytest.raises(RefusalError, match="convex-combination"):
        node.compressed(compression, prior(sources)[6], kernel)


@pytest.mark.slow
def test_the_full_replay_reproduces_case_2095(sources: tool.Sources) -> None:
    result = tool.full_replay(sources, max_seconds=600, workers=2)
    assert result["status"] == "PASS_LIBRARY_REPRODUCES_CASE2095"
    assert result["geometry_verified"] is True
    assert result["seed_points"] == 77
    assert result["seed_rows"] == 352
    assert result["step_owners"] == [6, 10, 7, 14, 11]
    assert result["step_rows"] == 160
    assert result["compressions"] == 4
    assert result["published_states_matched"] == 5
    assert result["contradiction"] == tool.CONTRADICTION
    assert result["excluded_case_ids"] == [2095]
