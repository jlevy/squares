#!/usr/bin/env python3
"""Regression checks for the conservative and broad chunk-component views."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import mpmath as mp
import pytest

import sqpack.chunks as chunks_module
from devtools import census_known_best_chunks as census
from sqpack.chunks import (
    NEAR_ADJACENCY_TOLERANCE,
    component_census,
    contact_component_census,
    minimal_lattice_partition,
)
from sqpack.witness import load_witness

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "witnesses/witness.schema.yaml"


def _witness(n: int) -> dict:
    return load_witness(
        ROOT / f"witnesses/known-best/n-{n:03d}.yaml",
        fallback_schema=SCHEMA,
    )


def test_component_views_keep_strict_grammar_and_broad_assembly_separate() -> None:
    grid = component_census(_witness(100), tolerance=NEAR_ADJACENCY_TOLERANCE)
    assert grid["status"] == "established"
    assert grid["chunk_count"] == 1
    assert grid["components"][0]["shape"] == "rectangle"
    assert grid["components"][0]["maximum_lattice_residual"] == "0"

    grid_contacts = contact_component_census(
        _witness(100), angle_tolerance_radians=1e-6, contact_tolerance=1e-3
    )
    assert grid_contacts["internal_slide_dof"] == 18
    assert grid_contacts["wall_seated_square_count"] == 36
    assert grid_contacts["components"][0]["normal_constraint_rank"] == 180
    assert grid_contacts["components"][0]["contact_graph_cycle_rank"] == 81
    assert all(edge["residual"] == "0" for edge in grid_contacts["components"][0]["edges"])

    trump = contact_component_census(
        _witness(11), angle_tolerance_radians=1e-6, contact_tolerance=1e-3
    )
    assert trump["angle_class_count"] == 2
    assert trump["contact_chunk_count"] == 2
    assert trump["free_square_count"] == 3
    assert trump["structured_square_count"] == 8
    assert trump["within_six_chunks_and_three_free"] is True

    irregular_grid = component_census(_witness(7), tolerance=NEAR_ADJACENCY_TOLERANCE)
    assert irregular_grid["status"] == "not-established"
    split_grid = minimal_lattice_partition(_witness(7), tolerance=NEAR_ADJACENCY_TOLERANCE)
    assert split_grid["status"] == "established"
    assert split_grid["selected_free_square_count"] == 0
    assert split_grid["selected_chunk_count"] == 2


def test_census_trigonometry_does_not_call_the_platform_libm(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args: object) -> float:
        raise AssertionError("retained census called platform libm trigonometry")

    for name in ("atan2", "cos", "sin"):
        monkeypatch.setattr(math, name, forbidden)

    census = contact_component_census(
        _witness(11), angle_tolerance_radians=1e-6, contact_tolerance=1e-3
    )

    assert census["structured_square_count"] == 8


def test_retained_census_reports_source_stratified_coverage() -> None:
    document = json.loads(
        (ROOT / "atlas/known-best/chunk-components.json").read_text(encoding="utf-8")
    )
    registered = document["contact_sweeps"][0]
    assert registered["name"] == "registered-angle-contact"
    non_grid = registered["summary"]["non_grid"]
    assert non_grid["records"] == 36
    assert (non_grid["structured_squares"], non_grid["total_squares"]) == (1780, 1860)
    assert non_grid["within_six_chunks_and_three_free"] == 25

    relaxed = document["contact_sweeps"][1]
    strict_n68 = registered["entries"][67]
    relaxed_n68 = relaxed["entries"][67]
    assert strict_n68["structured_square_count"] == 57
    assert relaxed_n68["structured_square_count"] == 60
    assert strict_n68["angle_class_count"] == 13
    assert relaxed_n68["angle_class_count"] == 7

    partitions = json.loads(
        (ROOT / "atlas/known-best/chunk-partitions.json").read_text(encoding="utf-8")
    )
    near_partitions = partitions["atlas"]["bands"][1]
    assert near_partitions["name"] == "near"
    partitioned_non_grid = near_partitions["summary"]["non_grid"]
    assert partitioned_non_grid["records"] == 36
    assert partitioned_non_grid["established"] == 3
    assert partitioned_non_grid["outside_registered_budget"] == 2
    assert partitioned_non_grid["not_established"] == 23
    assert partitioned_non_grid["search_limit"] == 8
    assert [
        entry["n"]
        for entry in near_partitions["entries"]
        if entry["status"] == "not-established-search-limit"
    ] == [52, 65, 66, 67, 82, 84, 85, 89]
    assert [
        entry["n"]
        for entry in near_partitions["entries"]
        if entry["status"] == "outside-registered-budget"
    ] == [38, 40]


def test_partition_search_can_trade_one_more_free_square_for_budget() -> None:
    partition = minimal_lattice_partition(
        _witness(26),
        tolerance=NEAR_ADJACENCY_TOLERANCE,
        maximum_states=10_000,
    )

    assert partition["status"] == "established"
    assert partition["selected_free_square_count"] == 2
    assert partition["selected_chunk_count"] == 6
    assert partition["selected_partition_minimality"] == "complete"
    assert [option["status"] for option in partition["options"]] == [
        "no-partition",
        "partitioned",
        "partitioned",
    ]


def test_partition_search_limit_after_a_partition_remains_indeterminate() -> None:
    partition = minimal_lattice_partition(
        _witness(65),
        tolerance=NEAR_ADJACENCY_TOLERANCE,
        maximum_states=10_000,
    )

    assert partition["status"] == "not-established-search-limit"
    assert partition["selected_free_square_count"] == 0
    assert partition["selected_chunk_count"] == 9
    assert partition["selected_partition_minimality"] == "indeterminate-search-limit"
    assert "whether an in-budget partition exists" in partition["limitation"]
    assert "proves in-budget existence" not in partition["limitation"]
    assert [option["status"] for option in partition["options"]] == [
        "partitioned",
        "partitioned",
        "search-limit",
    ]


def test_earlier_search_limit_keeps_later_existence_but_types_minimality(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Fault injection must intercept the private bounded-search seam.
    original_solve = vars(chunks_module)["_solve_partition"]

    def cap_first_free_count(*args: Any, **kwargs: Any):
        if kwargs["exact_free_squares"] == 0:
            return None, int(kwargs["maximum_states"]) + 1, True
        return original_solve(*args, **kwargs)

    monkeypatch.setattr(chunks_module, "_solve_partition", cap_first_free_count)
    partition = minimal_lattice_partition(
        _witness(26),
        tolerance=NEAR_ADJACENCY_TOLERANCE,
        maximum_states=10_000,
    )

    assert partition["status"] == "established"
    assert partition["selected_free_square_count"] == 2
    assert partition["selected_chunk_count"] == 6
    assert partition["selected_partition_minimality"] == "indeterminate-search-limit"
    assert [option["status"] for option in partition["options"]] == [
        "search-limit",
        "partitioned",
        "partitioned",
    ]


def test_earlier_search_limit_does_not_promote_later_out_of_budget_partition(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_solve = vars(chunks_module)["_solve_partition"]

    def cap_first_free_count(*args: Any, **kwargs: Any):
        if kwargs["exact_free_squares"] == 0:
            return None, int(kwargs["maximum_states"]) + 1, True
        return original_solve(*args, **kwargs)

    monkeypatch.setattr(chunks_module, "_solve_partition", cap_first_free_count)
    partition = minimal_lattice_partition(
        _witness(38),
        tolerance=NEAR_ADJACENCY_TOLERANCE,
        maximum_states=10_000,
    )

    assert partition["status"] == "not-established-search-limit"
    assert partition["selected_free_square_count"] == 2
    assert partition["selected_chunk_count"] == 7
    assert partition["selected_partition_minimality"] == "indeterminate-search-limit"
    assert "whether an in-budget partition exists" in partition["limitation"]
    assert "proves in-budget existence" not in partition["limitation"]


def test_partition_bitsets_preserve_off_frame_order_and_state_cap() -> None:
    candidate_type = vars(chunks_module)["_PartitionCandidate"]
    solve = vars(chunks_module)["_solve_partition"]

    def candidate(key: str, mask: int, *, off_frame: bool = False):
        return candidate_type(
            key=key,
            mask=mask,
            members=(),
            shape="bar",
            angle_class=0,
            angle_degrees=0.0,
            off_frame=off_frame,
            maximum_contact_residual=0.0,
            contacts=(),
        )

    candidates = [
        candidate("a", 0b0011, off_frame=True),
        candidate("b", 0b1100),
        candidate("c", 0b0101),
        candidate("d", 0b1010),
    ]

    without_off_frame, states, hit_limit = solve(
        candidates,
        square_count=4,
        exact_free_squares=0,
        maximum_off_frame_chunks=0,
        maximum_states=10,
    )
    assert without_off_frame is not None
    assert (without_off_frame.candidates, states, hit_limit) == ((2, 3), 3, False)

    with_off_frame, states, hit_limit = solve(
        candidates,
        square_count=4,
        exact_free_squares=0,
        maximum_off_frame_chunks=1,
        maximum_states=10,
    )
    assert with_off_frame is not None
    assert (with_off_frame.candidates, states, hit_limit) == ((0, 1), 3, False)

    assert solve(
        candidates,
        square_count=4,
        exact_free_squares=0,
        maximum_off_frame_chunks=1,
        maximum_states=2,
    ) == (None, 3, True)


def test_connected_angle_chain_is_not_mistaken_for_one_fitted_class() -> None:
    witness = {
        "id": "W-angle-chain-control",
        "n": 4,
        "side": "5",
        "square_size": "1",
        "representation": "center-angle",
        "scalar": {"kind": "decimal"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "degrees",
        },
        "squares": [
            {"id": index + 1, "center": [str(index + 0.5), "0.5"], "angle": angle}
            for index, angle in enumerate(("0", "0.000055", "0.000110", "0.000165"))
        ],
    }
    census = component_census(witness, tolerance=NEAR_ADJACENCY_TOLERANCE)
    assert census["angle_class_count"] == 1
    assert census["angle_fit_valid"] is False
    assert census["status"] == "not-established"
    partition = minimal_lattice_partition(witness, tolerance=NEAR_ADJACENCY_TOLERANCE)
    assert partition["angle_fit_valid"] is False
    assert partition["status"] == "not-established"
    contacts = contact_component_census(
        witness,
        angle_tolerance_radians=1e-6,
        contact_tolerance=NEAR_ADJACENCY_TOLERANCE,
    )
    assert contacts["angle_fit_valid"] is True
    assert contacts["angle_class_count"] == 2
    assert max(component["size"] for component in contacts["components"]) == 3


def test_diagonal_point_contact_does_not_become_a_chunk() -> None:
    witness = {
        "id": "W-point-contact-control",
        "n": 2,
        "side": "3",
        "square_size": "1",
        "representation": "center-angle",
        "scalar": {"kind": "decimal"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "degrees",
        },
        "squares": [
            {"id": 1, "center": ["0.5", "0.5"], "angle": "0"},
            {"id": 2, "center": ["1.5", "1.5"], "angle": "0"},
        ],
    }
    partition = minimal_lattice_partition(witness, tolerance=NEAR_ADJACENCY_TOLERANCE)
    assert partition["candidate_count"] == 0
    assert partition["selected_chunk_count"] == 0
    assert partition["selected_free_square_count"] == 2
    contacts = contact_component_census(
        witness,
        angle_tolerance_radians=1e-6,
        contact_tolerance=NEAR_ADJACENCY_TOLERANCE,
    )
    assert contacts["contact_chunk_count"] == 0
    assert contacts["free_square_count"] == 2


def test_partition_ties_follow_the_declared_deterministic_traversal() -> None:
    points = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1)]
    witness = {
        "id": "W-canonical-partition-control",
        "n": len(points),
        "side": "4",
        "square_size": "1",
        "representation": "corners",
        "scalar": {"kind": "rational"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": [
            {
                "id": index,
                "corners": [
                    [str(x), str(y)],
                    [str(x + 1), str(y)],
                    [str(x + 1), str(y + 1)],
                    [str(x), str(y + 1)],
                ],
            }
            for index, (x, y) in enumerate(points, start=1)
        ],
    }

    partition = minimal_lattice_partition(
        witness,
        tolerance=NEAR_ADJACENCY_TOLERANCE,
        maximum_states=10_000,
    )

    assert partition["selected_chunk_count"] == 2
    selected = [chunk["id"] for chunk in partition["options"][0]["chunks"]]
    replay = minimal_lattice_partition(
        witness,
        tolerance=NEAR_ADJACENCY_TOLERANCE,
        maximum_states=10_000,
    )
    assert selected == [
        "a01:L:2,3,5",
        "a01:bar:1,4",
    ]
    assert [chunk["id"] for chunk in replay["options"][0]["chunks"]] == selected


def test_a_pool_worker_censuses_at_the_same_precision_as_this_process() -> None:
    """The corpus is censused across processes, and mpmath precision is per-process state.

    `mp.mp.dps` is a global that a `forkserver` child does not inherit: a worker starts
    at mpmath's default of 15 digits whatever the parent set. Where that matters it is
    silent -- arithmetic at the wrong precision does not raise, it publishes different
    decimals, and a retained census is exactly the document where a wrong number reads
    as a result rather than as a bug.

    It does not matter here, and measuring that rather than assuming it is the whole
    point of this test, because it is why `census_records` needs no pool `initializer`.
    Every mpmath entry point under `component_census`, `contact_component_census` and
    `minimal_lattice_partition` sets its own working precision instead of reading the
    ambient one: poses are materialized at 80 digits, and every trigonometric call is
    bracketed by `mp.workdps(PORTABLE_TRIG_DIGITS)`. Measured over n=5, 11, 17, 40 and
    97 entered at 15, 80 and 300 ambient digits, the six documents per witness are
    byte-identical.

    Two controls, so neither half passes vacuously. The first is the precision gap
    itself: one witness is censused twice, once from mpmath's default and once from
    whatever the first run left behind, and the assertion between them requires those to
    differ -- so the two runs demonstrably started from the different ambient states a
    pool creates, rather than from the same state twice. The second is that the two
    records in the pooled run compare unequal, so `==` over these documents is sharp
    enough to see a difference when there is one.

    The comparison then requires a real two-process run to reproduce the single-process
    result exactly, through `census_records` itself rather than around it, so what is
    checked is the path the tool takes. Two workers rather than four: two is what the
    `sweeps` job exports as `--inner-jobs`, and a test that only proved the four-worker
    path would not cover what CI runs.
    """
    selected = tuple(entry for entry in census.atlas_entries() if entry["n"] in {11, 26})
    assert [entry["n"] for entry in selected] == [11, 26]

    ambient = mp.mp.dps
    original = census.atlas_entries
    try:
        census.atlas_entries = lambda: selected[:1]
        census.census_records.cache_clear()
        mp.mp.dps = 15
        at_default_precision = census.census_records(1)
        assert mp.mp.dps != 15
        census.census_records.cache_clear()
        assert census.census_records(1) == at_default_precision

        census.atlas_entries = lambda: selected
        census.census_records.cache_clear()
        serial = census.census_records(1)
        census.census_records.cache_clear()
        pooled = census.census_records(2)
    finally:
        census.atlas_entries = original
        census.census_records.cache_clear()
        mp.mp.dps = ambient

    assert [record["components"]["exact"]["n"] for record in serial] == [11, 26]
    assert serial[0] != serial[1]
    assert serial[0] == at_default_precision[0]
    assert pooled == serial
