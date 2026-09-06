#!/usr/bin/env python3
"""Build or check the descriptive chunk-component census over the known-best atlas."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from collections.abc import Sequence
from functools import cache
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from sqpack.chunks import (
    EXACT_ADJACENCY_TOLERANCE,
    NEAR_ADJACENCY_TOLERANCE,
    REGISTERED_MAXIMUM_CHUNKS,
    component_census,
    contact_component_census,
    minimal_lattice_partition,
)
from sqpack.witness import load_witness

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "atlas/known-best/manifest.json"
OUTPUT = ROOT / "atlas/known-best/chunk-components.json"
PARTITION_OUTPUT = ROOT / "atlas/known-best/chunk-partitions.json"
WITNESS_SCHEMA = ROOT / "witnesses/witness.schema.yaml"
GENERATOR = "python -m devtools.census_known_best_chunks"
PARTITION_MAXIMUM_STATES = 10_000


@cache
def _corpus() -> tuple[tuple[dict, ...], tuple[str, ...]]:
    """The atlas witnesses and their source kinds, read once per process."""
    atlas = json.loads(MANIFEST.read_text(encoding="utf-8"))["atlas"]
    witnesses = tuple(
        load_witness(ROOT / entry["witness"]["path"], fallback_schema=WITNESS_SCHEMA)
        for entry in atlas["entries"]
    )
    return witnesses, tuple(entry["source"]["kind"] for entry in atlas["entries"])


@cache
def _component_entries(tolerance: float) -> tuple[dict[str, Any], ...]:
    """One maximal-component census per witness, built once and published twice.

    The partition atlas searches inside exactly the census the component atlas prints,
    and building it a second time was the largest single cost in this step: 200 censuses
    where 100 exist. Memoized on the band rather than passed around, because both
    documents are reachable from `--update` and from `--check`.
    """
    witnesses, _kinds = _corpus()
    return tuple(component_census(witness, tolerance=tolerance) for witness in witnesses)


def _summary(entries: list[dict]) -> dict:
    return {
        "records": len(entries),
        "established": sum(entry["status"] == "established" for entry in entries),
        "not_established": sum(entry["status"] != "established" for entry in entries),
        "angle_class_counts": dict(
            sorted(Counter(str(entry["angle_class_count"]) for entry in entries).items())
        ),
        "component_shapes": dict(
            sorted(
                Counter(
                    component["shape"]
                    for entry in entries
                    for component in entry["components"]
                    if component["size"] >= 2
                ).items()
            )
        ),
        "structured_squares": sum(entry["structured_square_count"] for entry in entries),
        "total_squares": sum(entry["n"] for entry in entries),
    }


def _contact_totals(entries: list[dict]) -> dict:
    return {
        "records": len(entries),
        "within_six_chunks_and_three_free": sum(
            entry["within_six_chunks_and_three_free"] for entry in entries
        ),
        "structured_squares": sum(entry["structured_square_count"] for entry in entries),
        "total_squares": sum(entry["n"] for entry in entries),
        "internal_slide_dof": sum(entry["internal_slide_dof"] for entry in entries),
        "wall_seated_squares": sum(entry["wall_seated_square_count"] for entry in entries),
        "topologies": dict(
            sorted(
                Counter(
                    component["topology"]
                    for entry in entries
                    for component in entry["components"]
                    if component["size"] >= 2
                ).items()
            )
        ),
        "component_slide_dof": dict(
            sorted(
                Counter(
                    str(component["internal_slide_dof"])
                    for entry in entries
                    for component in entry["components"]
                    if component["size"] >= 2
                ).items()
            )
        ),
    }


def _contact_summary(entries: list[dict], source_kinds: list[str]) -> dict:
    summary = _contact_totals(entries)
    summary["by_source_kind"] = {
        kind: _contact_totals(
            [
                entry
                for entry, source in zip(entries, source_kinds, strict=True)
                if source == kind
            ]
        )
        for kind in sorted(set(source_kinds))
    }
    summary["non_grid"] = _contact_totals(
        [
            entry
            for entry, source in zip(entries, source_kinds, strict=True)
            if source != "exact-grid"
        ]
    )
    return summary


def expected_document() -> dict:
    witnesses, source_kind_values = _corpus()
    source_kinds = list(source_kind_values)
    bands = []
    for name, tolerance in (
        ("exact", EXACT_ADJACENCY_TOLERANCE),
        ("near", NEAR_ADJACENCY_TOLERANCE),
    ):
        entries = list(_component_entries(tolerance))
        bands.append({"name": name, "summary": _summary(entries), "entries": entries})
    contact_sweeps = []
    for name, angle_tolerance, contact_tolerance in (
        ("registered-angle-contact", 1e-6, 1e-3),
        ("regularized-angle-contact", 1e-3, 1e-2),
    ):
        entries = [
            contact_component_census(
                witness,
                angle_tolerance_radians=angle_tolerance,
                contact_tolerance=contact_tolerance,
            )
            for witness in witnesses
        ]
        contact_sweeps.append(
            {
                "name": name,
                "summary": _contact_summary(entries, source_kinds),
                "entries": entries,
            }
        )
    return {
        "contract": "packing.squares:ChunkComponentCensus/v1",
        "generated_by": GENERATOR,
        "corpus": "atlas/known-best/manifest.json; descriptive n=1..100 calibration corpus",
        "claim_status": "exploratory-no-verdict",
        "detector": {
            "angle_classes": (
                "connected under 1e-6 radians modulo quarter turns, with every "
                "established class also required to fit one circular-mean angle within "
                "1e-6 radians"
            ),
            "components": "maximal same-angle components joined by unit lattice steps",
            "allowed_shapes": ["bar", "L", "rectangle"],
            "objective": "none; maximal components only",
            "known_gap": (
                "No minimal partition search. Passes are certificates for the reported "
                "decomposition; non-passes cannot refute H-044."
            ),
        },
        "contact_contract": {
            "node": "one imported square pose",
            "angle_class": "connected modulo quarter turns at the declared tolerance",
            "edge": (
                "same-angle positive-length edge contact; diagonal point contacts are excluded"
            ),
            "topology": "connected component classified as chain, tree, or patch",
            "normal_constraint_rank": (
                "sum of incidence-matrix ranks for u-normal and v-normal contact equalities"
            ),
            "internal_slide_dof": "2m - normal_constraint_rank - 2 translations",
            "wall_seating": "container walls touched within the contact tolerance",
            "grammar_cost": (
                "unfrozen; component count alone is descriptive and cannot make one "
                "giant connected assembly a zero-complexity chunk"
            ),
        },
        "bands": bands,
        "contact_sweeps": contact_sweeps,
    }


def _partition_totals(entries: list[dict]) -> dict:
    statuses = Counter(entry["status"] for entry in entries)
    return {
        "records": len(entries),
        "established": statuses["established"],
        "outside_registered_budget": statuses["outside-registered-budget"],
        "not_established": statuses["not-established"],
        "search_limit": statuses["not-established-search-limit"],
        "candidate_count": sum(entry["candidate_count"] for entry in entries),
        "selected_chunk_counts": dict(
            sorted(
                Counter(
                    str(entry["selected_chunk_count"])
                    for entry in entries
                    if entry["selected_chunk_count"] is not None
                ).items()
            )
        ),
        "selected_free_square_counts": dict(
            sorted(
                Counter(
                    str(entry["selected_free_square_count"])
                    for entry in entries
                    if entry["selected_free_square_count"] is not None
                ).items()
            )
        ),
    }


def _partition_summary(entries: list[dict], source_kinds: list[str]) -> dict:
    result = _partition_totals(entries)
    result["by_source_kind"] = {
        kind: _partition_totals(
            [
                entry
                for entry, source in zip(entries, source_kinds, strict=True)
                if source == kind
            ]
        )
        for kind in sorted(set(source_kinds))
    }
    result["non_grid"] = _partition_totals(
        [
            entry
            for entry, source in zip(entries, source_kinds, strict=True)
            if source != "exact-grid"
        ]
    )
    return result


def expected_partition_document() -> dict:
    witnesses, source_kind_values = _corpus()
    source_kinds = list(source_kind_values)
    bands = []
    for name, tolerance in (
        ("exact", EXACT_ADJACENCY_TOLERANCE),
        ("near", NEAR_ADJACENCY_TOLERANCE),
    ):
        entries = [
            {
                **minimal_lattice_partition(
                    witness,
                    tolerance=tolerance,
                    maximum_states=PARTITION_MAXIMUM_STATES,
                    component_document=component_document,
                ),
                "source_kind": source_kind,
            }
            for witness, source_kind, component_document in zip(
                witnesses, source_kinds, _component_entries(tolerance), strict=True
            )
        ]
        bands.append(
            {
                "name": name,
                "summary": _partition_summary(entries, source_kinds),
                "entries": entries,
            }
        )
    return {
        "softschema": {
            "contract": "packing.squares:ChunkPartitionAtlas/v1",
            "schema": "chunk-partition-atlas.schema.yaml",
            "envelope": "atlas",
            "status": "enforced",
        },
        "atlas": {
            "generated_by": GENERATOR,
            "corpus": "atlas/known-best/manifest.json; inspected n=1..100 calibration corpus",
            "claim_status": "calibration-no-verdict",
            "partition_contract": {
                "candidate_universe": (
                    "contiguous bars, filled rectangles, and corner Ls inside each "
                    "maximal same-angle lattice component"
                ),
                "selection_order": (
                    "evaluate every exact free-square count F; prefer partitions within "
                    "the registered chunk budget, then minimize F, chunk count C, and "
                    "maximum contact residual; ties follow deterministic MRV depth-first "
                    "traversal with candidates ordered by size, residual, and key; an "
                    "earlier capped slice leaves a later in-budget selection's "
                    "minimality indeterminate, while any capped slice leaves a retained "
                    "out-of-budget selection and budget classification indeterminate"
                ),
                "maximum_free_squares": 2,
                "maximum_chunks": REGISTERED_MAXIMUM_CHUNKS,
                "maximum_off_frame_chunks": 2,
                "maximum_search_states_per_free_count": PARTITION_MAXIMUM_STATES,
                "typed_limit": (
                    "Search-limit and candidate-universe misses are not-established, "
                    "never H-044 refutations; selected-partition minimality is typed "
                    "separately whenever a relevant free-count slice is capped."
                ),
            },
            "bands": bands,
        },
    }


def _text(document: dict) -> str:
    return json.dumps(document, indent=2, sort_keys=True) + "\n"


def update() -> None:
    component_text = _text(expected_document())
    partition_text = _text(expected_partition_document())
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(OUTPUT) as temporary:
        temporary.write_text(component_text, encoding="utf-8")
    with atomic_output_file(PARTITION_OUTPUT) as temporary:
        temporary.write_text(partition_text, encoding="utf-8")
    print(
        "chunk census updated: components, contacts, and bounded lattice partitions "
        "for 100 records"
    )


def check() -> None:
    expected = _text(expected_document())
    if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != expected:
        raise ValueError("atlas/known-best/chunk-components.json is missing or stale")
    expected_partitions = _text(expected_partition_document())
    if (
        not PARTITION_OUTPUT.is_file()
        or PARTITION_OUTPUT.read_text(encoding="utf-8") != expected_partitions
    ):
        raise ValueError("atlas/known-best/chunk-partitions.json is missing or stale")
    print(
        "chunk census check passed: components, contacts, and bounded lattice partitions "
        "for 100 records"
    )


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--update", action="store_true")
    mode.add_argument("--check", action="store_true")
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    update() if args.update else check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
