#!/usr/bin/env python3
"""Price a target-free contact-label funnel before building a large enumerator."""

from __future__ import annotations

import argparse
import json
import math
import time
from collections import Counter
from collections.abc import Iterator
from itertools import combinations
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from strif import atomic_output_file

from sqpack.contact_assembly import (
    Axis,
    ContactEdge,
    ContactScaffold,
    enumerate_isomorph_free_scaffolds,
)
from sqpack.contact_realization import realize_local_contact_scaffolds

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "atlas/known-best/contact-enumeration-pricing.json"
SCHEMA = ROOT / "atlas/known-best/contact-enumeration-pricing.schema.yaml"
GENERATOR = "python -m devtools.price_contact_enumeration"
EDGE_COLORS: tuple[tuple[Axis, int], ...] = (
    ("u", 1),
    ("u", -1),
    ("v", 1),
    ("v", -1),
)
MAXIMUM_RAW_ORBIT_IMAGES = 10_000_000
MAXIMUM_TOPOLOGY_COLORINGS = 2_000_000
MAXIMUM_CANONICAL_PROPOSALS = 100_000
MAXIMUM_LP_SOLVES = 100_000
MINIMUM_OVERLAP = 0.25


def connected_colored_graph_count(size: int, *, edge_color_count: int = 4) -> int:
    """Count connected labeled graphs whose present edges have one of q colors."""
    if size < 1 or edge_color_count < 1:
        raise ValueError("size and edge_color_count must be positive")
    connected = [0] * (size + 1)
    connected[1] = 1
    states = edge_color_count + 1
    for vertices in range(2, size + 1):
        total = states ** math.comb(vertices, 2)
        disconnected = sum(
            math.comb(vertices - 1, component_size - 1)
            * connected[component_size]
            * states ** math.comb(vertices - component_size, 2)
            for component_size in range(1, vertices)
        )
        connected[vertices] = total - disconnected
    return connected[size]


def _is_connected(size: int, edges: list[ContactEdge]) -> bool:
    if size == 1:
        return True
    adjacent = [set() for _ in range(size)]
    for edge in edges:
        adjacent[edge.left].add(edge.right)
        adjacent[edge.right].add(edge.left)
    reached = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in adjacent[vertex] - reached:
            reached.add(neighbor)
            frontier.append(neighbor)
    return len(reached) == size


def labeled_contact_scaffolds(size: int) -> Iterator[ContactScaffold]:
    """Yield every connected uniform-color, wall-free signed-axis scaffold."""
    if not 1 <= size <= 5:
        raise ValueError("pricing scaffolds require size 1..5")
    pairs = tuple(combinations(range(size), 2))
    state_count = len(EDGE_COLORS) + 1
    for encoded in range(state_count ** len(pairs)):
        remainder = encoded
        edges: list[ContactEdge] = []
        for left, right in pairs:
            state = remainder % state_count
            remainder //= state_count
            if state:
                normal, sign = EDGE_COLORS[state - 1]
                edges.append(ContactEdge(left, right, normal, sign))
        if _is_connected(size, edges):
            yield ContactScaffold(("one-angle-class",) * size, tuple(edges), ((),) * size)


def _entry(size: int, *, decision: str) -> dict[str, Any]:
    raw = connected_colored_graph_count(size)
    group_size = 8 * math.factorial(size)
    raw_orbit_images = raw * group_size
    proposals = enumerate_isomorph_free_scaffolds(
        size,
        maximum_colorings=MAXIMUM_TOPOLOGY_COLORINGS,
        maximum_emitted_scaffolds=MAXIMUM_CANONICAL_PROPOSALS,
    )
    if proposals.status != "completed":
        raise RuntimeError(
            f"n={size} isomorph-free proposal path reached "
            f"{proposals.limit_kind} at {proposals.limit}"
        )
    entry: dict[str, Any] = {
        "n": size,
        "raw_labeled_candidates": raw,
        "d4_relabeling_group_size": group_size,
        "canonical_orbit_lower_bound": math.ceil(raw / group_size),
        "raw_orbit_image_upper_work": raw_orbit_images,
        "unlabeled_topologies": proposals.topology_count,
        "topology_coloring_candidates": proposals.required_colorings,
        "isomorph_free_orbit_actions": proposals.orbit_action_images,
        "proposal_method": "topology-automorphism-orbit-marking",
        "decision": decision,
        "canonical_orbits": len(proposals.scaffolds),
        "duplicate_candidates": None,
        "lp_solves": None,
        "outcomes": None,
    }
    if decision != "execute":
        return entry
    batch = realize_local_contact_scaffolds(
        labeled_contact_scaffolds(size),
        minimum_overlap=MINIMUM_OVERLAP,
        maximum_lp_solves=MAXIMUM_LP_SOLVES,
    )
    if batch.status != "completed":
        raise RuntimeError(f"n={size} unexpectedly reached {batch.limit_kind} at {batch.limit}")
    if batch.encountered_candidates != raw:
        raise RuntimeError(
            f"n={size} enumerated {batch.encountered_candidates}, expected {raw}"
        )
    outcomes = Counter(receipt.outcome for receipt in batch.receipts)
    if len(batch.receipts) != len(proposals.scaffolds):
        raise RuntimeError(
            f"n={size} direct quotient has {len(proposals.scaffolds)} orbits, "
            f"legacy exhaustive realization has {len(batch.receipts)}"
        )
    entry.update(
        {
            "canonical_orbits": len(batch.receipts),
            "duplicate_candidates": batch.duplicate_candidates,
            "lp_solves": batch.lp_solves,
            "outcomes": {
                name: outcomes[name]
                for name in (
                    "locally-feasible",
                    "locally-infeasible",
                    "solver-indeterminate",
                )
            },
        }
    )
    return entry


def expected_document(*, execute_through: int = 4) -> dict[str, Any]:
    if not 1 <= execute_through <= 4:
        raise ValueError("execute_through must be in 1..4")
    entries = []
    for size in range(1, 6):
        raw_work = connected_colored_graph_count(size) * 8 * math.factorial(size)
        if raw_work > MAXIMUM_RAW_ORBIT_IMAGES:
            decision = "enumerate-isomorph-free"
        elif size > execute_through:
            decision = "outside-run-scope"
        else:
            decision = "execute"
        entries.append(_entry(size, decision=decision))
    return {
        "softschema": {
            "contract": "packing.squares:ContactEnumerationPricing/v1",
            "schema": "contact-enumeration-pricing.schema.yaml",
            "envelope": "pricing",
            "status": "enforced",
        },
        "pricing": {
            "generated_by": GENERATOR,
            "scope": (
                "connected, one semantic angle color, no walls; every vertex pair is "
                "absent or carries one of signed u/v normal colors"
            ),
            "evidence_role": "target-free engineering price; no atlas geometry or verdict",
            "minimum_overlap": MINIMUM_OVERLAP,
            "caps": {
                "maximum_raw_orbit_images": MAXIMUM_RAW_ORBIT_IMAGES,
                "maximum_topology_colorings": MAXIMUM_TOPOLOGY_COLORINGS,
                "maximum_canonical_proposals": MAXIMUM_CANONICAL_PROPOSALS,
                "maximum_lp_solves": MAXIMUM_LP_SOLVES,
            },
            "decision_rule": (
                "Execute legacy labeled canonicalization and local LPs only when its exact "
                "raw orbit work is within the declared cap. Otherwise enumerate canonical "
                "proposals by connected topology and Aut(topology)-by-D4 orbit marking, "
                "without running the LP stage in this engineering-price slice."
            ),
            "runtime_policy": (
                "Wall time is platform-specific and printed by the generator, not "
                "retained in the byte-stable artifact."
            ),
            "entries": entries,
        },
    }


def _validate(document: dict[str, Any]) -> None:
    schema = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    problems = sorted(
        Draft202012Validator(schema).iter_errors(document["pricing"]),
        key=lambda problem: list(problem.path),
    )
    if problems:
        raise ValueError(f"pricing schema failure: {problems[0].message}")


def _text(document: dict[str, Any]) -> str:
    return json.dumps(document, indent=2, sort_keys=True) + "\n"


def update() -> None:
    started = time.perf_counter()
    document = expected_document()
    _validate(document)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(OUTPUT) as temporary:
        temporary.write_text(_text(document), encoding="utf-8")
    print(f"contact enumeration pricing updated in {time.perf_counter() - started:.2f}s")


def check() -> None:
    started = time.perf_counter()
    document = expected_document()
    _validate(document)
    if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != _text(document):
        raise ValueError("atlas/known-best/contact-enumeration-pricing.json is stale")
    print(f"contact enumeration pricing check passed in {time.perf_counter() - started:.2f}s")


def smoke() -> None:
    started = time.perf_counter()
    document = expected_document(execute_through=3)
    _validate(document)
    print(
        "contact enumeration pricing smoke passed through n=3 in "
        f"{time.perf_counter() - started:.2f}s"
    )


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--update", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--smoke", action="store_true")
    return command


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.update:
        update()
    elif args.check:
        check()
    else:
        smoke()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
