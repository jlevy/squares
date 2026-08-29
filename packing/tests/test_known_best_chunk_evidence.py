#!/usr/bin/env python3
"""Replay and mutation controls for the non-grid chunk evidence profile."""

from __future__ import annotations

import json
from copy import deepcopy

from devtools.profile_known_best_chunks import (
    COMPONENTS,
    MANIFEST,
    OUTPUT,
    PARTITION_BAND,
    PARTITIONS,
    PRIMARY_SWEEP,
    RENDERING,
    SENSITIVITY_SWEEP,
    expected_outputs,
    profile_errors,
    schema_errors,
)


def test_known_best_chunk_evidence_profile_replays_byte_for_byte() -> None:
    expected, rendering = expected_outputs()
    retained = json.loads(OUTPUT.read_text(encoding="utf-8"))

    assert retained == expected
    assert RENDERING.read_text(encoding="utf-8") == rendering
    profile = retained["profile"]
    assert profile["aggregate"] == {
        "case_count": 36,
        "contact_component_count": 169,
        "coverage_threshold_cases": {
            "at_least_50_percent": 35,
            "at_least_75_percent": 33,
            "at_least_90_percent": 27,
        },
        "fully_structured_cases": 10,
        "internal_slide_dof": 859,
        "narrow_partition_status_counts": {
            "established": 3,
            "not-established": 23,
            "not-established-search-limit": 8,
            "outside-registered-budget": 2,
        },
        "sensitivity_comparison": {
            "changed_case_count": 3,
            "changed_ns": [68, 69, 71],
            "primary_structured_square_count": 1780,
            "sensitivity_structured_square_count": 1793,
            "within_budget_flip_ns": [69],
        },
        "source_strata": [
            {
                "case_count": 34,
                "fully_structured_cases": 10,
                "sensitivity_changed_ns": [71],
                "source_kind": "kingbird-derived-facts",
                "square_count": 1723,
                "structured_fraction": "0.96691816599",
                "structured_square_count": 1666,
                "within_six_components_and_three_free_cases": 25,
            },
            {
                "case_count": 2,
                "fully_structured_cases": 0,
                "sensitivity_changed_ns": [68, 69],
                "source_kind": "unitsquare-rendering",
                "square_count": 137,
                "structured_fraction": "0.832116788321",
                "structured_square_count": 114,
                "within_six_components_and_three_free_cases": 0,
            },
        ],
        "square_count": 1860,
        "structured_fraction": "0.956989247312",
        "structured_square_count": 1780,
        "within_six_components_and_three_free_cases": 25,
    }
    assert "DESCRIPTIVE · NO VERDICT" in rendering
    assert "Connectedness is not rigidity" in rendering
    assert "No claim of global optimality" in rendering
    assert "document-table-layout; svg-y-down; no-packing-coordinates" in rendering
    assert profile["rendering"] == {
        "path": "atlas/known-best/evidence/non-grid-chunk-evidence-profile.svg",
        "semantics": "descriptive-document-table-no-packing-geometry",
    }


def test_known_best_chunk_evidence_profile_preserves_outliers_and_sensitivity() -> None:
    profile = expected_outputs()[0]["profile"]
    by_n = {row["n"]: row for row in profile["cases"]}

    assert by_n[5]["primary"]["structured_square_count"] == 0
    assert by_n[5]["primary"]["contact_component_count"] == 0
    assert by_n[28]["primary"]["structured_square_count"] == 28
    assert by_n[89]["primary"]["largest_component_size"] == 49
    assert by_n[68]["sensitivity_delta"]["structured_square_count"] == 3
    assert by_n[69]["sensitivity_delta"] == {
        "contact_component_count": 0,
        "free_square_count": -10,
        "structured_square_count": 10,
        "within_budget_changed": True,
    }
    assert by_n[71]["sensitivity_delta"]["contact_component_count"] == -1


def test_every_profile_row_reconstructs_from_the_three_source_artifacts() -> None:
    profile = json.loads(OUTPUT.read_text(encoding="utf-8"))["profile"]
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))["atlas"]["entries"]
    components = json.loads(COMPONENTS.read_text(encoding="utf-8"))["contact_sweeps"]
    partitions = json.loads(PARTITIONS.read_text(encoding="utf-8"))["atlas"]["bands"]
    source_kind = {entry["n"]: entry["source"]["kind"] for entry in manifest}
    primary = {
        entry["n"]: entry
        for sweep in components
        if sweep["name"] == PRIMARY_SWEEP
        for entry in sweep["entries"]
    }
    sensitivity = {
        entry["n"]: entry
        for sweep in components
        if sweep["name"] == SENSITIVITY_SWEEP
        for entry in sweep["entries"]
    }
    narrow = {
        entry["n"]: entry
        for band in partitions
        if band["name"] == PARTITION_BAND
        for entry in band["entries"]
    }

    for row in profile["cases"]:
        n = row["n"]
        raw = primary[n]
        alternate = sensitivity[n]
        raw_components = [
            component for component in raw["components"] if component["size"] >= 2
        ]
        assert row["source_kind"] == source_kind[n] == narrow[n]["source_kind"]
        assert row["primary"]["structured_square_count"] == raw["structured_square_count"]
        assert row["primary"]["free_square_count"] == raw["free_square_count"]
        assert row["primary"]["contact_component_count"] == len(raw_components)
        assert row["primary"]["contact_edge_count"] == sum(
            len(component["edges"]) for component in raw_components
        )
        assert row["primary"]["largest_component_size"] == max(
            component["size"] for component in raw["components"]
        )
        assert row["primary"]["internal_slide_dof"] == raw["internal_slide_dof"]
        assert row["narrow_partition"] == {
            "selected_chunk_count": narrow[n]["selected_chunk_count"],
            "selected_free_square_count": narrow[n]["selected_free_square_count"],
            "selected_partition_minimality": narrow[n]["selected_partition_minimality"],
            "status": narrow[n]["status"],
        }
        assert row["sensitivity_delta"]["structured_square_count"] == (
            alternate["structured_square_count"] - raw["structured_square_count"]
        )


def test_known_best_chunk_evidence_profile_mutations_fail() -> None:
    profile = expected_outputs()[0]["profile"]

    duplicate_n = deepcopy(profile)
    duplicate_n["cases"][1]["n"] = duplicate_n["cases"][0]["n"]
    assert profile_errors(duplicate_n)

    wrong_sum = deepcopy(profile)
    wrong_sum["aggregate"]["structured_square_count"] -= 1
    assert profile_errors(wrong_sum)

    wrong_sensitivity = deepcopy(profile)
    wrong_sensitivity["aggregate"]["sensitivity_comparison"]["changed_ns"] = [68, 69]
    assert profile_errors(wrong_sensitivity)

    hidden_source_drift = deepcopy(profile)
    hidden_source_drift["aggregate"]["source_strata"][0]["structured_square_count"] -= 1
    assert profile_errors(hidden_source_drift)

    missing_partition_counts = deepcopy(profile)
    selected = next(
        row
        for row in missing_partition_counts["cases"]
        if row["narrow_partition"]["status"] == "established"
    )
    selected["narrow_partition"]["selected_chunk_count"] = None
    assert profile_errors(missing_partition_counts)

    partial_capped_counts = deepcopy(profile)
    capped = next(
        row
        for row in partial_capped_counts["cases"]
        if row["narrow_partition"]["status"] == "not-established-search-limit"
        and row["narrow_partition"]["selected_chunk_count"] is not None
    )
    capped["narrow_partition"]["selected_free_square_count"] = None
    assert profile_errors(partial_capped_counts)

    false_capped_minimality = deepcopy(profile)
    capped = next(
        row
        for row in false_capped_minimality["cases"]
        if row["narrow_partition"]["status"] == "not-established-search-limit"
        and row["narrow_partition"]["selected_chunk_count"] is not None
    )
    capped["narrow_partition"]["selected_partition_minimality"] = "complete"
    assert profile_errors(false_capped_minimality)

    false_outside_minimality = deepcopy(profile)
    outside = next(
        row
        for row in false_outside_minimality["cases"]
        if row["narrow_partition"]["status"] == "outside-registered-budget"
    )
    outside["narrow_partition"]["selected_partition_minimality"] = "indeterminate-search-limit"
    assert profile_errors(false_outside_minimality)

    hypothesis_channel = deepcopy(profile)
    hypothesis_channel["hypothesis"] = "supported"
    assert schema_errors(hypothesis_channel)

    geometry_channel = deepcopy(profile)
    geometry_channel["coordinates"] = [[0, 0]]
    assert schema_errors(geometry_channel)
