"""Finite normalized-pattern rank certificates; never ordinary packing exclusions.

The accepted normalization, determinant expansion and moving-wall lemma are
explicit hand-proof premises. Search proposes a certificate; fresh checking only
reconstructs incidence rosters and checks exact finite ranks or independence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import time
from collections import deque
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from sqpack import retained_json

SCHEMA = "n17-normalized-contact-rank-filter/v1"
CONTEXT_SCHEMA = "n17-normalized-contact-rank-context/v1"
U = Q(1169, 250)
LOWER = Q(18641771, 4000000)
TARGET = 35
VERTICES = 38
CLONES = 374
STATE_LIMIT = 95
INPUT_LIMIT = 10 << 20
OUTPUT_LIMIT = 64 << 20
EXCHANGE_STATE = 1_000_000
EXCHANGE_TOTAL = 64_000_000
BITS = 4096
REPO = Path(__file__).resolve().parents[2]
NUMBER = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z", re.ASCII)


class IncompleteError(ValueError):
    """A finite resource ceiling stopped the proposal or verification."""


def require(condition: bool, message: str) -> None:  # noqa: FBT001
    if not condition:
        raise ValueError(message)


def tick(deadline: float) -> None:
    if time.monotonic() >= deadline:
        raise IncompleteError("rank-filter wall ceiling")


def rational(value: Any) -> Q:
    require(
        type(value) is str and len(value) <= 2600 and NUMBER.fullmatch(value) is not None,
        "bounded canonical rational required",
    )
    result = Q(value)
    if max(abs(result.numerator).bit_length(), result.denominator.bit_length()) > BITS:
        raise IncompleteError("normalized geometry bit ceiling")
    require(str(result) == value, "canonical rational required")
    return result


def bounded(value: Q) -> Q:
    if max(abs(value.numerator).bit_length(), value.denominator.bit_length()) > BITS:
        raise IncompleteError("computed geometry bit ceiling")
    return value


def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON member")
        result[key] = value
    return result


def read(path: Path, limit: int = INPUT_LIMIT) -> tuple[bytes, dict[str, Any]]:
    with path.open("rb") as stream:
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise IncompleteError("input byte ceiling")

    def forbidden(_value: str) -> Any:
        raise ValueError("nonfinite JSON number refused")

    def metadata_float(value: str) -> float:
        require(len(value) <= 64, "bounded metadata float required")
        result = float(value)
        require(math.isfinite(result), "nonfinite metadata number refused")
        return result

    record = json.loads(
        raw, object_pairs_hook=unique, parse_float=metadata_float, parse_constant=forbidden
    )
    require(type(record) is dict, "JSON object required")
    return raw, record


@dataclass(frozen=True)
class Clone:
    left: int
    right: int
    physical: str
    wall: str | None


def graphic_rank(elements: list[Clone], indices: set[int]) -> int:
    parent = list(range(VERTICES))

    def root(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    result = 0
    for index in sorted(indices):
        element = elements[index]
        left, right = root(element.left), root(element.right)
        if left != right:
            parent[left] = right
            result += 1
    return result


def capacity_rank(elements: list[Clone], indices: set[int]) -> int:
    pairs: set[str] = set()
    walls: dict[str, set[str]] = {wall: set() for wall in "LRBT"}
    for index in indices:
        element = elements[index]
        if element.wall is None:
            pairs.add(element.physical)
        else:
            walls[element.wall].add(element.physical)
    return len(pairs) + sum(min(4, len(incidences)) for incidences in walls.values())


def independent(elements: list[Clone], indices: set[int], *, graphic: bool) -> bool:
    return (graphic_rank if graphic else capacity_rank)(elements, indices) == len(indices)


@dataclass
class Work:
    deadline: float
    total: int = 0
    state: int = 0

    def charge(self) -> None:
        tick(self.deadline)
        self.total += 1
        self.state += 1
        if self.state > EXCHANGE_STATE or self.total > EXCHANGE_TOTAL:
            raise IncompleteError("exchange-test ceiling")


def search(elements: list[Clone], work: Work) -> dict[str, Any]:
    """Deterministic shortest-path proposals, checked after each augmentation."""
    require(len(elements) <= CLONES, "clone ceiling")
    work.state = 0
    selected: set[int] = set()
    universe = set(range(len(elements)))
    for augmentation in range(TARGET + 1):
        if len(selected) == TARGET:
            return {
                "kind": "survival",
                "indices": sorted(selected),
                "augmentations": augmentation,
                "exchange_tests": work.state,
            }
        outside = sorted(universe - selected)

        def allowed(indices: set[int], *, graphic: bool) -> bool:
            work.charge()
            return independent(elements, indices, graphic=graphic)

        sources = [e for e in outside if allowed(selected | {e}, graphic=True)]
        sinks = {e for e in outside if allowed(selected | {e}, graphic=False)}
        previous: dict[int, int | None] = dict.fromkeys(sources)
        queue = deque(sources)
        destination = None
        while queue:
            current = queue.popleft()
            if current in sinks:
                destination = current
                break
            if current in selected:
                neighbors = [
                    e
                    for e in outside
                    if e not in previous and allowed((selected - {current}) | {e}, graphic=True)
                ]
            else:
                neighbors = [
                    e
                    for e in sorted(selected)
                    if e not in previous
                    and allowed((selected - {e}) | {current}, graphic=False)
                ]
            for neighbor in neighbors:
                previous[neighbor] = current
                queue.append(neighbor)
        if destination is None:
            subset = universe - set(previous)
            ranks = graphic_rank(elements, subset), capacity_rank(elements, universe - subset)
            if sum(ranks) < TARGET:
                return {
                    "kind": "rank_obstruction",
                    "subset_A": sorted(subset),
                    "rank_graph": ranks[0],
                    "rank_capacity_complement": ranks[1],
                    "rank_sum": sum(ranks),
                    "exchange_tests": work.state,
                }
            return {"kind": "unresolved", "exchange_tests": work.state}
        path = set()
        while destination is not None:
            path.add(destination)
            destination = previous[destination]
        selected ^= path
        require(
            len(selected) == augmentation + 1
            and allowed(selected, graphic=True)
            and allowed(selected, graphic=False),
            "proposed augmentation fails independent checks",
        )
    raise ValueError("augmentation ceiling exceeded")


def subset(value: Any, size: int) -> set[int]:
    require(
        type(value) is list
        and len(value) <= size
        and all(type(i) is int and 0 <= i < size for i in value)
        and value == sorted(set(value)),
        "canonical clone subset required",
    )
    return set(value)


def check_certificate(elements: list[Clone], certificate: dict[str, Any]) -> str:
    """The finite checker trusts neither search nor its claimed numerical ranks."""
    require(type(certificate) is dict, "finite certificate object required")
    universe = set(range(len(elements)))
    kind = certificate.get("kind")
    if kind == "rank_obstruction":
        chosen = subset(certificate.get("subset_A"), len(elements))
        graph, capacity = (
            graphic_rank(elements, chosen),
            capacity_rank(elements, universe - chosen),
        )
        require(
            (
                certificate.get("rank_graph"),
                certificate.get("rank_capacity_complement"),
                certificate.get("rank_sum"),
            )
            == (graph, capacity, graph + capacity)
            and all(
                type(certificate.get(key)) is int
                for key in ("rank_graph", "rank_capacity_complement", "rank_sum")
            )
            and graph + capacity < TARGET,
            "rank-obstruction certificate differs",
        )
    elif kind == "survival":
        chosen = subset(certificate.get("indices"), len(elements))
        require(
            len(chosen) == TARGET
            and independent(elements, chosen, graphic=True)
            and independent(elements, chosen, graphic=False),
            "survival witness differs",
        )
    else:
        require(kind == "unresolved", "unsupported finite certificate")
    return cast(str, kind)


Box = tuple[Q, Q, Q, Q]


def pair_possible(first: Box, second: Box) -> bool:
    dx = max(Q(0), first[0] - second[1], second[0] - first[1])
    dy = max(Q(0), first[2] - second[3], second[2] - first[3])
    return bounded(bounded(dx * dx) + bounded(dy * dy)) <= 2


def meets(low: Q, high: Q, left: Q, right: Q) -> bool:
    return max(low, left) <= min(high, right)


def ground_set(boxes: list[Box]) -> list[Clone]:
    require(len(boxes) == 17, "seventeen occupied cells required")
    delta = bounded((U - LOWER) / 2)
    elements: list[Clone] = []
    for i in range(17):
        for j in range(i + 1, 17):
            if pair_possible(boxes[i], boxes[j]):
                elements.extend(
                    [Clone(i, j, f"p:{i}:{j}", None), Clone(i + 18, j + 18, f"p:{i}:{j}", None)]
                )
    for i, box in enumerate(boxes):
        for wall in "LRBT":
            low, high = box[:2] if wall in "LR" else box[2:]
            left, right = (
                (Q(1, 2), Q(3, 4) + delta)
                if wall in "LB"
                else (U - Q(3, 4) - delta, U - Q(1, 2))
            )
            if meets(low, high, left, right):
                vertex, pin = (i, 17) if wall in "LR" else (i + 18, 35)
                elements.append(Clone(vertex, pin, f"w:{wall}:{i}", wall))
                if wall in "RT":
                    elements.append(Clone(36, 37, f"w:{wall}:{i}", wall))
    require(len(elements) <= CLONES, "clone ceiling")
    return elements


def images(mask: int, permutations: dict[str, list[int]]) -> set[int]:
    return {sum(1 << p[i] for i in range(24) if mask & (1 << i)) for p in permutations.values()}


def named_row(
    row: dict[str, Any],
    names: list[str],
    permutations: dict[str, list[int]],
    endpoint_images: set[int],
) -> None:
    mask = row["mask"]
    orbit = images(mask, permutations)
    occupied = [i for i in range(24) if mask & (1 << i)]
    require(
        mask == min(orbit)
        and type(row.get("orbit_size")) is int
        and row["orbit_size"] == len(orbit)
        and row.get("cells") == [names[i] for i in occupied]
        and row["distance"] == min((mask ^ image).bit_count() for image in endpoint_images),
        "partition named distance/D4 orbit join differs",
    )


def intake(document: dict[str, Any]) -> tuple[list[tuple[int, list[Box]]], dict[str, bytes]]:
    require(
        set(document)
        == {
            "schema",
            "outer_U",
            "lower_bound",
            "lower_bound_premise",
            "partition",
            "partition_sha256",
            "cover",
            "cover_sha256",
            "states",
            "d4",
        },
        "exact rank context fields required",
    )
    require(
        document.get("schema") == CONTEXT_SCHEMA
        and document.get("outer_U") == str(U)
        and document.get("lower_bound") == str(LOWER)
        and document.get("lower_bound_premise") == "T-093",
        "frozen rank context differs",
    )
    custody: dict[str, bytes] = {}
    records = {}
    for role in ("partition", "cover"):
        require(
            type(document.get(role)) is str and type(document.get(role + "_sha256")) is str,
            "accepted input path/byte identity required",
        )
        path = Path(document[role])
        path = path if path.is_absolute() else REPO / path
        raw, record = read(path)
        require(
            hashlib.sha256(raw).hexdigest() == document[role + "_sha256"],
            "accepted input bytes differ",
        )
        custody[str(path)] = raw
        records[role] = record
    # Defer the legacy catalogue's scientific imports until frozen input custody
    # is joined. These calls never rerun its cover/root/endpoint proof.
    from devtools.check_n17_capacity_one_cover import (  # noqa: PLC0415
        DESIGNS,
        UNIQUE_24,
        build_cover,
        cell_record,
        d4_permutations,
    )

    cells = build_cover(DESIGNS[UNIQUE_24.name])
    permutations = d4_permutations(cells)
    require(permutations is not None, "exact D4 catalogue required")
    permutations = cast(dict[str, list[int]], permutations)
    cover = records["cover"]
    require(
        all(type(cover.get(key)) is dict for key in ("design", "criterion", "d4")),
        "typed accepted cover premises required",
    )
    require(
        cover.get("schema") == "n17-capacity-one-cover/v1"
        and cover.get("design", {}).get("name") == UNIQUE_24.name
        and cover.get("design", {}).get("cap") == str(U)
        and cover.get("criterion", {}).get("passed") is True
        and cover.get("cells") == [cell_record(cell) for cell in cells]
        and cover.get("d4", {}).get("permutations") == permutations,
        "accepted complete cover/cell/D4 premise differs",
    )
    partition = records["partition"]
    require(type(partition.get("certified")) is dict, "typed certified partition required")
    require(
        partition.get("schema") == "n17-certified-residue-stratification/v1"
        and partition.get("design") == UNIQUE_24.name
        and partition.get("cap") == str(U)
        and partition.get("certified", {}).get("admitted") == 60
        and partition.get("certified", {}).get("surviving_states") == 36768
        and partition.get("certified", {}).get("orbits") == 4683
        and partition.get("certified", {}).get("endpoint_survives") is True,
        "accepted ordinary residue differs",
    )
    rows = partition.get("orbits")
    require(type(rows) is list and len(rows) == 4683, "complete partition roster required")
    rows = cast(list[dict[str, Any]], rows)
    require(
        all(
            type(row) is dict
            and type(row.get("mask")) is int
            and 0 <= row["mask"] < 1 << 24
            and row["mask"].bit_count() == 17
            and type(row.get("distance")) is int
            for row in rows
        )
        and len({row["mask"] for row in rows}) == len(rows),
        "typed unique partition masks required",
    )
    endpoints = [r for r in rows if r.get("distance") == 0]
    require(len(endpoints) == 1, "one endpoint orbit required")
    endpoint_images = images(endpoints[0]["mask"], permutations)
    names = [cell.name for cell in cells]
    for row in rows:
        named_row(row, names, permutations, endpoint_images)
    selected = [r for r in rows if r.get("distance") == 2]
    selected.sort(key=lambda row: row["mask"])
    require(len(selected) == STATE_LIMIT, "all95 distance-two orbits required")
    names = [cell.name for cell in cells]
    boxes = [
        (
            min(p[0] for p in c.vertices),
            max(p[0] for p in c.vertices),
            min(p[1] for p in c.vertices),
            max(p[1] for p in c.vertices),
        )
        for c in cells
    ]
    for box in boxes:
        for coordinate in box:
            bounded(coordinate)
    roster = []
    result = []
    for row in selected:
        mask = row["mask"]
        require(
            type(mask) is int and 0 <= mask < 1 << 24 and mask.bit_count() == 17,
            "full named assignment mask required",
        )
        orbit = images(mask, permutations)
        occupied = [i for i in range(24) if mask & (1 << i)]
        require(
            mask == min(orbit)
            and row.get("orbit_size") == len(orbit)
            and row.get("cells") == [names[i] for i in occupied]
            and min((mask ^ image).bit_count() for image in endpoint_images) == 2,
            "named distance/D4 orbit join differs",
        )
        roster.append({"mask": mask, "cells": row["cells"], "orbit_size": len(orbit)})
        result.append((mask, [boxes[i] for i in occupied]))
    require(
        len({mask for mask, _ in result}) == STATE_LIMIT
        and document.get("states") == roster
        and document.get("d4") == permutations,
        "frozen complete selected roster differs",
    )
    return result, custody


def payload(record: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in record.items() if k not in ("invocation", "verification_passed")}


def generate(
    document: dict[str, Any], deadline: float, certificate: dict[str, Any] | None = None
) -> dict[str, Any]:
    states, custody = intake(document)
    tick(deadline)
    outcomes = []
    work = Work(deadline)
    if certificate is not None:
        require(
            certificate.get("schema") == SCHEMA
            and certificate.get("accepted_inputs") == document,
            "certificate input context differs",
        )
        saved = certificate.get("outcomes")
        require(
            type(saved) is list and len(saved) == len(states), "complete finite outcome roster"
        )
        saved = cast(list[dict[str, Any]], saved)
    else:
        saved = None
    for index, (mask, boxes) in enumerate(states):
        tick(deadline)
        elements = ground_set(boxes)
        if saved is None:
            proposal = search(elements, work)
        else:
            require(
                type(saved[index]) is dict and saved[index].get("mask") == mask,
                "finite outcome order differs",
            )
            proposal = saved[index]["certificate"]
        kind = check_certificate(elements, proposal)
        outcomes.append(
            {
                "mask": mask,
                "clones": len(elements),
                "certificate": proposal,
                "classification": kind,
            }
        )
    for path, raw in custody.items():
        with Path(path).open("rb") as stream:
            require(
                stream.read(len(raw) + 1) == raw, "accepted input changed during reconstruction"
            )
    counts = {
        kind: sum(r["classification"] == kind for r in outcomes)
        for kind in ("rank_obstruction", "survival", "unresolved")
    }
    result = {
        "schema": SCHEMA,
        "accepted_inputs": document,
        "outcomes": outcomes,
        "counts": counts,
        "orbits_accounted": len(states),
        "status": "unresolved"
        if counts["unresolved"]
        else "normalized_obstruction_found"
        if counts["rank_obstruction"]
        else "criterion_missed",
        "criterion_met": counts["rank_obstruction"] > 0 and counts["unresolved"] == 0,
        "complete_classification": counts["unresolved"] == 0,
        "scope": "necessary normalized-full-rank pattern relaxation only",
        "hand_dependencies_independently_verified": False,
        "ordinary_assignment_exclusion_proved": False,
        "ordinary_census_admission_proved": False,
        "global_nonexistence_proved": False,
        "side_bound_improved": False,
        "parent_geometry_replayed": False,
        "limits": {
            "clones": CLONES,
            "graph_vertices": VERTICES,
            "augmentations": TARGET,
            "exchanges_per_state": EXCHANGE_STATE,
            "exchanges_total": EXCHANGE_TOTAL,
            "geometry_bits": BITS,
            "input_bytes": INPUT_LIMIT,
            "output_bytes": OUTPUT_LIMIT,
        },
    }
    if certificate is not None:
        require(payload(certificate) == result, "fresh finite payload differs")
        result["verification_passed"] = True
    tick(deadline)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--descriptor", type=Path, required=True)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--max-seconds", type=float, default=120)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    deadline = time.monotonic() + args.max_seconds
    try:
        require(
            math.isfinite(args.max_seconds) and 0 < args.max_seconds <= 120,
            "bounded phase wall required",
        )
        raw, document = read(args.descriptor)
        certificate_raw, certificate = (
            read(args.certificate, OUTPUT_LIMIT) if args.certificate else (None, None)
        )
        result = generate(document, deadline, certificate)
        with args.descriptor.open("rb") as stream:
            require(stream.read(len(raw) + 1) == raw, "descriptor bytes changed")
        if args.certificate:
            with args.certificate.open("rb") as stream:
                require(
                    stream.read(len(certificate_raw or b"") + 1) == certificate_raw,
                    "certificate bytes changed",
                )
        result["invocation"] = {"max_seconds": args.max_seconds}
        text = retained_json.dumps(result, sort_keys=True) + "\n"
        if len(text.encode()) > OUTPUT_LIMIT:
            raise IncompleteError("output byte ceiling")
        tick(deadline)
    except (OSError, ValueError, TypeError, KeyError, OverflowError) as exc:
        result = {
            "schema": SCHEMA,
            "status": "incomplete" if isinstance(exc, IncompleteError) else "refused",
            "error": str(exc),
            "ordinary_assignment_exclusion_proved": False,
            "ordinary_census_admission_proved": False,
            "global_nonexistence_proved": False,
        }
        text = retained_json.dumps(result, sort_keys=True) + "\n"
    require(
        args.output.resolve()
        not in {p.resolve() for p in (args.descriptor, args.certificate) if p},
        "output aliases input",
    )
    with args.output.open("x", encoding="utf-8") as stream:
        stream.write(text)
    return 0 if result["status"] not in ("incomplete", "refused") else 1


if __name__ == "__main__":
    raise SystemExit(main())
