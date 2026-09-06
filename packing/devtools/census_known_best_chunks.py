#!/usr/bin/env python3
"""Build or check the descriptive chunk-component census over the known-best atlas.

Usage:
    uv run --frozen python -m devtools.census_known_best_chunks --update
    uv run --frozen python -m devtools.census_known_best_chunks --check
    uv run --frozen python -m devtools.census_known_best_chunks --check --jobs 4
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from collections.abc import Sequence
from concurrent.futures import ProcessPoolExecutor
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
from sqpack.workers import worker_count

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "atlas/known-best/manifest.json"
OUTPUT = ROOT / "atlas/known-best/chunk-components.json"
PARTITION_OUTPUT = ROOT / "atlas/known-best/chunk-partitions.json"
WITNESS_SCHEMA = ROOT / "witnesses/witness.schema.yaml"
GENERATOR = "python -m devtools.census_known_best_chunks"
PARTITION_MAXIMUM_STATES = 10_000

BANDS: tuple[tuple[str, float], ...] = (
    ("exact", EXACT_ADJACENCY_TOLERANCE),
    ("near", NEAR_ADJACENCY_TOLERANCE),
)
"""The two registered adjacency bands, in the order both documents publish them."""

CONTACT_SWEEPS: tuple[tuple[str, float, float], ...] = (
    ("registered-angle-contact", 1e-6, 1e-3),
    ("regularized-angle-contact", 1e-3, 1e-2),
)
"""The two contact sweeps, as `(name, angle tolerance radians, contact tolerance)`."""


@cache
def atlas_entries() -> tuple[dict[str, Any], ...]:
    """The atlas manifest entries, read once per process.

    Only the entries, no longer the witnesses they name. Each witness is now loaded by
    whichever process censuses it, which is both what keeps mpmath objects out of the
    pool protocol and what parallelizes the schema-validated load along with the work.
    """
    atlas = json.loads(MANIFEST.read_text(encoding="utf-8"))["atlas"]
    return tuple(atlas["entries"])


def _census_entry(entry: dict[str, Any]) -> dict[str, Any]:
    """Every derived census for one witness: the whole unit of parallel work.

    Six documents per witness -- a maximal-component census and a bounded partition
    search in each of the two bands, and a contact census in each of the two sweeps.
    They are grouped rather than mapped separately because the partition search reads
    exactly the census the component atlas publishes, and handing it over is what the
    per-band memo this replaced was for: 200 censuses where 100 exist. Keeping the pair
    inside one unit keeps that saving without a memo that would have to be shared across
    processes to survive.

    The process boundary is drawn here on purpose. What crosses it is JSON in both
    directions: a manifest entry going out, and plain dicts of strings, numbers and
    lists coming back, every one of them already destined for `json.dumps`. No mpmath
    object is ever pickled, so no digit can be lost to a round trip -- the witness is
    materialized in the process that censuses it.
    """
    try:
        witness = load_witness(ROOT / entry["witness"]["path"], fallback_schema=WITNESS_SCHEMA)
        components = {
            name: component_census(witness, tolerance=tolerance) for name, tolerance in BANDS
        }
        source_kind = entry["source"]["kind"]
        return {
            "components": components,
            "contacts": {
                name: contact_component_census(
                    witness,
                    angle_tolerance_radians=angle_tolerance,
                    contact_tolerance=contact_tolerance,
                )
                for name, angle_tolerance, contact_tolerance in CONTACT_SWEEPS
            },
            "partitions": {
                name: {
                    **minimal_lattice_partition(
                        witness,
                        tolerance=tolerance,
                        maximum_states=PARTITION_MAXIMUM_STATES,
                        component_document=components[name],
                    ),
                    "source_kind": source_kind,
                }
                for name, tolerance in BANDS
            },
            "source_kind": source_kind,
        }
    except Exception as error:
        # A pool reports which call raised without saying which unit it was, and the
        # messages this can surface name a square id or a component, never the record.
        # Naming it here keeps a failure attributable whichever way the corpus ran.
        message = str(error)
        prefix = f"n={entry['n']}"
        blamed = message if message.startswith(prefix) else f"{prefix}: {message}"
        raise ValueError(blamed) from error


@cache
def census_records(workers: int | None = None) -> tuple[dict[str, Any], ...]:
    """One `_census_entry` result per atlas entry, in manifest order, built once.

    Every record is independent of every other -- each loads its own witness and reads
    nothing outside it -- so this is a map, and it was a serial one. It cost 90.38s in
    the `sweeps` job of run 34018763923, which is a floor under that job's wall: no
    GitHub job finishes before its own longest step, so no rearrangement of jobs
    shortens it and the only lever is inside the step.

    `workers` is the pool size. `None` asks `sqpack.workers.worker_count`, which reads
    the `PACK_JOBS` cap the gate exports to every step -- the same contract
    `screen_translation_escape`, `check_golden_basins` and `check_regressions` use. The
    count is never taken from the machine behind the gate's back, which is the mistake
    that put nineteen ordinary tests over the quick lane's per-test ceiling on
    contention alone. `1` runs in this process rather than through a pool, because a
    one-worker pool is a subprocess and a protocol for no concurrency at all.

    Memoized on the worker count because both documents are reachable from `--update`
    and from `--check`, and the second one must not re-derive the first one's records.

    Order is the manifest's, whichever way it ran. `pool.map` yields by submission index
    rather than by completion, so both documents are built in the order the serial loop
    built them in, which is what lets `check` compare them byte for byte.

    No pool `initializer`, and that is a measured decision rather than an omission --
    see `test_a_pool_worker_censuses_at_the_same_precision_as_this_process`.
    """
    entries = atlas_entries()
    requested = worker_count(len(entries)) if workers is None else workers
    count = max(1, min(requested, len(entries)))
    if count == 1:
        return tuple(_census_entry(entry) for entry in entries)
    with ProcessPoolExecutor(max_workers=count) as pool:
        return tuple(pool.map(_census_entry, entries))


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


def expected_document(workers: int | None = None) -> dict:
    records = census_records(workers)
    source_kinds = [record["source_kind"] for record in records]
    bands = []
    for name, _tolerance in BANDS:
        entries = [record["components"][name] for record in records]
        bands.append({"name": name, "summary": _summary(entries), "entries": entries})
    contact_sweeps = []
    for name, _angle_tolerance, _contact_tolerance in CONTACT_SWEEPS:
        entries = [record["contacts"][name] for record in records]
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


def expected_partition_document(workers: int | None = None) -> dict:
    records = census_records(workers)
    source_kinds = [record["source_kind"] for record in records]
    bands = []
    for name, _tolerance in BANDS:
        entries = [record["partitions"][name] for record in records]
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


def update(workers: int | None = None) -> None:
    component_text = _text(expected_document(workers))
    partition_text = _text(expected_partition_document(workers))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(OUTPUT) as temporary:
        temporary.write_text(component_text, encoding="utf-8")
    with atomic_output_file(PARTITION_OUTPUT) as temporary:
        temporary.write_text(partition_text, encoding="utf-8")
    print(
        "chunk census updated: components, contacts, and bounded lattice partitions "
        "for 100 records"
    )


def check(workers: int | None = None) -> None:
    expected = _text(expected_document(workers))
    if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != expected:
        raise ValueError("atlas/known-best/chunk-components.json is missing or stale")
    expected_partitions = _text(expected_partition_document(workers))
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
    command.add_argument(
        "--jobs",
        type=int,
        metavar="N",
        default=None,
        help=(
            "processes to census the corpus with; the default follows the PACK_JOBS cap "
            "the gate exports, and the whole machine when there is no gate"
        ),
    )
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    workers: int | None = args.jobs
    update(workers) if args.update else check(workers)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
