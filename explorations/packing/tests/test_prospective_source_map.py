#!/usr/bin/env python3
"""Controls for the annotation-free prospective source-availability map."""

from __future__ import annotations

import json
from collections import Counter
from copy import deepcopy
from pathlib import Path

from devtools.map_prospective_sources import (
    OUTPUT,
    availability_errors,
    expected_document,
)

ROOT = Path(__file__).resolve().parent.parent


def test_prospective_source_map_is_deterministic_and_complete() -> None:
    retained = json.loads(OUTPUT.read_text(encoding="utf-8"))
    assert retained == expected_document()
    availability = retained["availability"]
    entries = availability["entries"]

    assert [entry["n"] for entry in entries] == list(range(101, 325))
    assert Counter(entry["source_key"] for entry in entries) == {
        "catalogue-trivial-grid-rule": 97,
        "kingbird-current-catalogue": 123,
        "unitsquare-release-1": 4,
    }
    assert {
        entry["n"] for entry in entries if entry["source_key"] == "unitsquare-release-1"
    } == {103, 105, 110, 131}
    assert availability["readiness"] == {
        "acquisition": "incomplete",
        "normalization": "incomplete",
        "source_selection": "provisionally-complete",
    }
    upstream_digests = {
        entry["n"]: entry["upstream_declared_sha256"]
        for entry in entries
        if "upstream_declared_sha256" in entry
    }
    assert set(upstream_digests) == {103, 105, 110, 131}
    assert all(len(digest) == 64 for digest in upstream_digests.values())
    assert "source_sha256" not in json.dumps(entries, sort_keys=True)
    assert "evidence_sha256" not in json.dumps(availability["sources"], sort_keys=True)


def test_map_keeps_visual_sources_and_annotations_out_of_geometry() -> None:
    availability = expected_document()["availability"]
    assert all(
        source["coordinate_use"] == "prohibited"
        for source in availability["visual_only_sources"]
    )
    assert availability["claim_status"] == "source-availability-only-no-annotations"
    serialized_entries = json.dumps(availability["entries"], sort_keys=True)
    for forbidden in ("contact", "chunk", "rigidity", "grammar"):
        assert forbidden not in serialized_entries

    gaps = availability["access_audit"]["kingbird"]["adapter_gap_sources"]
    assert gaps == []


def test_cross_field_controls_reject_range_source_and_audit_mutations() -> None:
    availability = expected_document()["availability"]
    mutations = []

    duplicate_count = deepcopy(availability)
    duplicate_count["entries"][0]["n"] = 102
    mutations.append(duplicate_count)

    stale_precedence = deepcopy(availability)
    n103 = next(entry for entry in stale_precedence["entries"] if entry["n"] == 103)
    n103["source_key"] = "kingbird-current-catalogue"
    mutations.append(stale_precedence)

    wrong_grid = deepcopy(availability)
    grid = next(
        entry
        for entry in wrong_grid["entries"]
        if entry["source_key"] == "catalogue-trivial-grid-rule"
    )
    grid["trivial_grid_side"] += 1
    mutations.append(wrong_grid)

    video_coordinates = deepcopy(availability)
    video_coordinates["visual_only_sources"][0]["coordinate_use"] = "allowed"
    mutations.append(video_coordinates)

    hidden_parser_loss = deepcopy(availability)
    hidden_parser_loss["access_audit"]["kingbird"]["adapter_passed"] = 111
    mutations.append(hidden_parser_loss)

    invented_gap = deepcopy(availability)
    invented_gap["access_audit"]["kingbird"]["adapter_passed"] = 113
    invented_gap["access_audit"]["kingbird"]["adapter_gap_sources"].append(
        {"reason": "invented regression", "source_path": "square-102.svg"}
    )
    mutations.append(invented_gap)

    misplaced_upstream_digest = deepcopy(availability)
    grid = next(
        entry
        for entry in misplaced_upstream_digest["entries"]
        if entry["source_key"] == "catalogue-trivial-grid-rule"
    )
    grid["upstream_declared_sha256"] = "0" * 64
    mutations.append(misplaced_upstream_digest)

    for mutation in mutations:
        assert availability_errors(mutation)
