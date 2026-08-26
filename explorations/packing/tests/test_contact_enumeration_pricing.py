#!/usr/bin/env python3
"""Exact-count and bounded-execution controls for contact-enumeration pricing."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import devtools.price_contact_enumeration as pricing
from devtools.price_contact_enumeration import (
    connected_colored_graph_count,
    expected_document,
    labeled_contact_scaffolds,
)
from sqpack.contact_assembly import (
    CanonicalScaffold,
    canonicalize_scaffold,
    enumerate_isomorph_free_scaffolds,
)

ROOT = Path(__file__).resolve().parent.parent


def test_connected_colored_counts_match_independent_small_cases() -> None:
    assert [connected_colored_graph_count(size) for size in range(1, 6)] == [
        1,
        4,
        112,
        15_104,
        9_684_224,
    ]
    assert [sum(1 for _ in labeled_contact_scaffolds(size)) for size in range(1, 4)] == [
        1,
        4,
        112,
    ]


def test_smoke_prices_all_orbits_and_lp_outcomes_through_three() -> None:
    original_generator = pricing.labeled_contact_scaffolds

    def reject_out_of_scope(size: int):
        if size >= 4:
            raise AssertionError("smoke run crossed its declared execution boundary")
        return original_generator(size)

    with patch.object(pricing, "labeled_contact_scaffolds", reject_out_of_scope):
        document = expected_document(execute_through=3)["pricing"]
    entries = document["entries"]

    assert [entry["decision"] for entry in entries] == [
        "execute",
        "execute",
        "execute",
        "outside-run-scope",
        "enumerate-isomorph-free",
    ]
    for entry in entries[:3]:
        assert entry["canonical_orbits"] == entry["lp_solves"]
        assert entry["raw_labeled_candidates"] == (
            entry["canonical_orbits"] + entry["duplicate_candidates"]
        )
        assert sum(entry["outcomes"].values()) == entry["lp_solves"]
        assert entry["outcomes"]["solver-indeterminate"] == 0

    assert [entry["canonical_orbits"] for entry in entries] == [1, 1, 7, 124, 11_013]
    assert [entry["unlabeled_topologies"] for entry in entries] == [1, 1, 2, 6, 21]
    assert [entry["topology_coloring_candidates"] for entry in entries] == [
        1,
        4,
        80,
        5_760,
        1_533_696,
    ]


def test_retained_price_enumerates_size_five_without_raw_orbit_or_lp_run() -> None:
    document = json.loads(
        (ROOT / "atlas/known-best/contact-enumeration-pricing.json").read_text(encoding="utf-8")
    )
    entries = document["pricing"]["entries"]
    entry = entries[4]

    for completed in entries[:4]:
        assert completed["raw_labeled_candidates"] == (
            completed["canonical_orbits"] + completed["duplicate_candidates"]
        )
        assert sum(completed["outcomes"].values()) == completed["lp_solves"]

    assert entry["raw_labeled_candidates"] == 9_684_224
    assert entry["raw_orbit_image_upper_work"] == 9_296_855_040
    assert entry["canonical_orbit_lower_bound"] == 10_088
    assert entry["unlabeled_topologies"] == 21
    assert entry["topology_coloring_candidates"] == 1_533_696
    assert entry["canonical_orbits"] == 11_013
    assert entry["decision"] == "enumerate-isomorph-free"
    assert entry["lp_solves"] is None


def test_direct_quotient_matches_legacy_labels_through_three_and_size_four_count() -> None:
    for size in range(1, 4):
        direct = enumerate_isomorph_free_scaffolds(
            size,
            maximum_colorings=100,
            maximum_emitted_scaffolds=20,
        )
        direct_labels = {
            result.canonical_label
            for scaffold in direct.scaffolds
            if isinstance((result := canonicalize_scaffold(scaffold)), CanonicalScaffold)
        }
        exhaustive_labels = {
            result.canonical_label
            for scaffold in labeled_contact_scaffolds(size)
            if isinstance((result := canonicalize_scaffold(scaffold)), CanonicalScaffold)
        }
        assert direct_labels == exhaustive_labels

    size_four = enumerate_isomorph_free_scaffolds(
        4,
        maximum_colorings=5_760,
        maximum_emitted_scaffolds=124,
    )
    labels = []
    for scaffold in size_four.scaffolds:
        result = canonicalize_scaffold(scaffold)
        assert isinstance(result, CanonicalScaffold)
        labels.append(result.canonical_label)
    assert len(labels) == len(set(labels)) == 124
