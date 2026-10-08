"""Exact correlated corner-window capacity relaxation; survival is not a packing."""

from __future__ import annotations

import argparse
import copy
import itertools
import json
import math
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from devtools import check_n17_n11_envelope_windows as old
from devtools.provenance import provenance
from sqpack import retained_json

finite, require, tick, payload = old.finite, old.require, old.tick, old.payload
checked = finite.checked
SCHEMA = "n17-n11-corner-cardinality/v1"
CONTEXT_SCHEMA = "n17-n11-corner-cardinality-context/v1"
U, H, R, D = old.U, old.H, old.R, old.U - old.H
ROW_LIMIT, CELL_LIMIT = 42, 32
TRIPLE_LIMIT, INEQUALITY_LIMIT = 4000000, 64000000
TRANSITION_LIMIT, STATE_TRANSITION_LIMIT = 64000000, 3000000
FRONTIER_LIMIT = 11**4
BITMAP_BYTES = (FRONTIER_LIMIT + 7) // 8
INPUT_LIMIT, OUTPUT_LIMIT = old.INPUT_LIMIT, old.OUTPUT_LIMIT
CLASSES = tuple(itertools.product(range(3), repeat=2))
type Point = tuple[Q, Q]
type Pose = tuple[Q, Q, Q]
type Row = tuple[Q, Q, Q, Q]
type Counts = tuple[int, int, int, int]


def scope(*, obstruction: bool = False) -> dict[str, bool]:
    return old.scope(obstruction=obstruction) | {
        "physical_packing_proved": False,
        "exact_membership_classification_proved": False,
        "complementary_guard_exclusion_proved": False,
    }


def new_work() -> dict[str, int]:
    return {"triple_attempts": 0, "inequality_evaluations": 0, "dp_transitions": 0}


def charge(work: dict[str, int], key: str, maximum: int) -> None:
    work[key] += 1
    if work[key] > maximum:
        raise finite.IncompleteError(key + " ceiling")


def determinant(rows: tuple[Pose, Pose, Pose]) -> Q:
    a, b, c = rows
    return checked(
        checked(a[0] * checked(b[1] * c[2] - b[2] * c[1]))
        - checked(a[1] * checked(b[0] * c[2] - b[2] * c[0]))
        + checked(a[2] * checked(b[0] * c[1] - b[1] * c[0]))
    )


def solve(rows: tuple[Row, Row, Row]) -> Pose | None:
    normals = cast(tuple[Pose, Pose, Pose], tuple(tuple(r[:3]) for r in rows))
    det = determinant(normals)
    if det == 0:
        return None
    result = []
    for column in range(3):
        replaced = cast(
            tuple[Pose, Pose, Pose],
            tuple(tuple(row[3] if j == column else row[j] for j in range(3)) for row in rows),
        )
        result.append(checked(determinant(replaced) / det))
    return cast(Pose, tuple(result))


def value(row: Row, pose: Pose) -> Q:
    return checked(sum((checked(a * b) for a, b in zip(row[:3], pose, strict=True)), Q(0)))


def physical_half_extent_squared(squared: Q) -> bool:
    """Exact closed physical reach bound; no approximate algebraic root."""
    return checked(2 * squared) <= 1


def feasible(rows: list[Row], work: dict[str, int], deadline: float) -> dict[str, Any]:
    """Exhaustive vertices of a bounded closed polytope, including lower dimension."""
    require(len(rows) <= ROW_LIMIT, "polytope row cap")
    attempts = 0
    for triple in itertools.combinations(range(len(rows)), 3):
        tick(deadline)
        charge(work, "triple_attempts", TRIPLE_LIMIT)
        attempts += 1
        point = solve(cast(tuple[Row, Row, Row], tuple(rows[i] for i in triple)))
        if point is None:
            continue
        valid = True
        for row in rows:
            charge(work, "inequality_evaluations", INEQUALITY_LIMIT)
            if value(row, point) > row[3]:
                valid = False
                break
        if valid and physical_half_extent_squared(checked(point[2] * point[2])):
            return {
                "feasible": True,
                "active_triple": list(triple),
                "pose": list(map(str, point)),
                "triples_attempted": attempts,
                "vertex_enumeration_complete": False,
            }
    tick(deadline)
    return {
        "feasible": False,
        "active_triple": None,
        "pose": None,
        "triples_attempted": attempts,
        "vertex_enumeration_complete": True,
    }


def pattern_bits(horizontal: int, vertical: int) -> Counts:
    require(
        type(horizontal) is int
        and type(vertical) is int
        and horizontal in range(3)
        and vertical in range(3),
        "membership class",
    )
    h = ({0}, {0, 1}, {1})[horizontal]
    v = ({0}, {0, 1}, {1})[vertical]
    return cast(Counts, tuple(int(x in h and y in v) for y in (0, 1) for x in (0, 1)))


def pattern_rows(polygon: list[Point], horizontal: int, vertical: int) -> list[Row]:
    require(3 <= len(polygon) <= CELL_LIMIT, "positive bounded cell polygon required")
    polygon = [(checked(x), checked(y)) for x, y in polygon]
    require(
        finite.standing.hull(polygon) == polygon
        and checked(finite.standing.area2(polygon)) > 0,
        "canonical convex cell required",
    )
    require(
        2 * R < 2 * H - U
        and Q(1, 2) <= R
        and checked(2 * R * R) >= 1
        and 0 < H < U
        and H < old.B11,
        "guaranteed membership scalar inequality",
    )
    rows: list[Row] = []
    for p, q in zip(polygon, polygon[1:] + polygon[:1], strict=True):
        dx, dy = checked(q[0] - p[0]), checked(q[1] - p[1])
        rows.append((dy, -dx, Q(0), checked(dy * p[0] - dx * p[1])))
    rows.extend(
        (
            (Q(0), Q(0), Q(-1), Q(-1, 2)),
            (Q(0), Q(0), Q(1), R),
            (Q(-1), Q(0), Q(1), Q(0)),
            (Q(1), Q(0), Q(1), U),
            (Q(0), Q(-1), Q(1), Q(0)),
            (Q(0), Q(1), Q(1), U),
        )
    )
    pattern_bits(horizontal, vertical)
    for axis, cls in ((0, horizontal), (1, vertical)):

        def add(a: Q, h: Q, rhs: Q, axis: int = axis) -> None:
            rows.append((a if axis == 0 else Q(0), a if axis == 1 else Q(0), h, rhs))

        if cls == 0:
            add(Q(1), Q(-1), D)
        elif cls == 1:
            add(Q(-1), Q(1), -D)
            add(Q(1), Q(1), H)
        else:
            add(Q(-1), Q(-1), -H)
    require(len(rows) <= ROW_LIMIT, "polytope row cap")
    return rows


def classify(polygons: list[list[Point]], work: dict[str, int], deadline: float) -> list[Any]:
    require(len(polygons) == 24, "complete24 polygon roster")
    outcomes = []
    for index, polygon in enumerate(polygons):
        for pattern, (horizontal, vertical) in enumerate(CLASSES):
            rows = pattern_rows(polygon, horizontal, vertical)
            result = feasible(rows, work, deadline)
            outcomes.append(
                {
                    "cell_index": index,
                    "pattern_id": pattern,
                    "horizontal_class": horizontal,
                    "vertical_class": vertical,
                    "guaranteed_window_bits": list(pattern_bits(horizontal, vertical)),
                    "rows": [list(map(str, row)) for row in rows],
                    **result,
                }
            )
    require(len(outcomes) == 216, "complete216 classifications")
    return outcomes


def bitmap(frontier: set[Counts]) -> str:
    require(len(frontier) <= FRONTIER_LIMIT, "frontier state ceiling")
    data = bytearray(BITMAP_BYTES)
    for counts in frontier:
        require(
            len(counts) == 4 and all(type(n) is int and 0 <= n <= 10 for n in counts),
            "count vector bound",
        )
        code = sum(n * 11**i for i, n in enumerate(counts))
        data[code // 8] |= 1 << (code % 8)
    return data.hex()


def decode_bitmap(text: Any) -> set[Counts]:
    require(
        type(text) is str
        and len(text) == 2 * BITMAP_BYTES
        and all(c in "0123456789abcdef" for c in text),
        "canonical frontier bitmap",
    )
    data = bytes.fromhex(text)
    require(data[-1] & 254 == 0, "unused frontier high bits")
    result = set()
    for code in range(FRONTIER_LIMIT):
        if data[code // 8] & (1 << (code % 8)):
            result.add(cast(Counts, tuple((code // 11**i) % 11 for i in range(4))))
    return result


def capacity_dp(
    cells: list[int], classifications: list[Any], work: dict[str, int], deadline: float
) -> dict[str, Any]:
    require(cells == sorted(set(cells)) and len(cells) == 17, "17 unique ascending cells")
    allowed = {
        cell: [r for r in classifications if r["cell_index"] == cell and r["feasible"]]
        for cell in cells
    }
    start = work["dp_transitions"]
    current: dict[Counts, list[int]] = {(0, 0, 0, 0): []}
    frontiers = [bitmap(set(current))]
    for cell in cells:
        next_layer: dict[Counts, list[int]] = {}
        for counts in sorted(current):
            for pattern in allowed[cell]:
                tick(deadline)
                charge(work, "dp_transitions", TRANSITION_LIMIT)
                if work["dp_transitions"] - start > STATE_TRANSITION_LIMIT:
                    raise finite.IncompleteError("per-state DP transition ceiling")
                result = cast(
                    Counts,
                    tuple(
                        a + b
                        for a, b in zip(counts, pattern["guaranteed_window_bits"], strict=True)
                    ),
                )
                if max(result) <= 10:
                    next_layer.setdefault(result, current[counts] + [pattern["pattern_id"]])
        require(len(next_layer) <= FRONTIER_LIMIT, "frontier state ceiling")
        current = next_layer
        frontiers.append(bitmap(set(current)))
    tick(deadline)
    if current:
        counts = min(current)
        return {
            "kind": "surviving_relaxation_assignment",
            "cells": cells,
            "pattern_ids": current[counts],
            "counts": list(counts),
            "transitions": work["dp_transitions"] - start,
        }
    return {
        "kind": "ordinary_assignment_obstruction",
        "cells": cells,
        "frontier_bitmaps": frontiers,
        "transitions": work["dp_transitions"] - start,
    }


def verify_state(certificate: Any, classifications: list[Any], deadline: float) -> None:
    require(
        type(certificate) is dict and type(certificate.get("cells")) is list,
        "typed capacity certificate",
    )
    certificate = cast(dict[str, Any], certificate)
    cells = certificate["cells"]
    require(cells == sorted(set(cells)) and len(cells) == 17, "17 unique ascending cells")
    table = {(r["cell_index"], r["pattern_id"]): r for r in classifications}
    if certificate["kind"] == "surviving_relaxation_assignment":
        require(len(certificate["pattern_ids"]) == 17, "full17 pattern witness")
        counts = [0] * 4
        for cell, pattern in zip(cells, certificate["pattern_ids"], strict=True):
            tick(deadline)
            require(
                type(pattern) is int
                and (cell, pattern) in table
                and table[cell, pattern]["feasible"],
                "feasible pattern witness required",
            )
            counts = [
                a + b
                for a, b in zip(
                    counts, table[cell, pattern]["guaranteed_window_bits"], strict=True
                )
            ]
        require(
            max(counts) <= 10 and certificate["counts"] == counts,
            "survivor capacity counts differ",
        )
        return
    require(
        certificate["kind"] == "ordinary_assignment_obstruction"
        and len(certificate["frontier_bitmaps"]) == 18,
        "full18 obstruction frontiers",
    )
    frontiers = [decode_bitmap(b) for b in certificate["frontier_bitmaps"]]
    require(frontiers[0] == {(0, 0, 0, 0)}, "initial reachable frontier")
    work = new_work()
    for layer, cell in enumerate(cells):
        expected = set()
        for counts in frontiers[layer]:
            for pattern in range(9):
                tick(deadline)
                record = table.get((cell, pattern))
                require(record is not None, "all9 pattern aliases required")
                record = cast(dict[str, Any], record)
                if record["feasible"]:
                    charge(work, "dp_transitions", STATE_TRANSITION_LIMIT)
                    combined = cast(
                        Counts,
                        tuple(
                            a + b
                            for a, b in zip(
                                counts, record["guaranteed_window_bits"], strict=True
                            )
                        ),
                    )
                    if max(combined) <= 10:
                        expected.add(combined)
        require(expected == frontiers[layer + 1], "complete frontier recurrence differs")
    require(not frontiers[-1], "negative certificate has a survivor")


def intake(document: Any, deadline: float) -> tuple[Any, ...]:
    require(
        type(document) is dict and document.get("schema") == CONTEXT_SCHEMA,
        "corner-cardinality context differs",
    )
    document = cast(dict[str, Any], document)
    adapted = copy.deepcopy(document) | {"schema": old.CONTEXT_SCHEMA}
    _, names, roster, held = old.intake(adapted, deadline)
    from devtools.check_n17_capacity_one_cover import (  # noqa: PLC0415
        DESIGNS,
        UNIQUE_24,
        build_cover,
    )

    polygons = [list(cell.vertices) for cell in build_cover(DESIGNS[UNIQUE_24.name])]
    path = Path(document["partition"])
    path = path if path.is_absolute() else old.REPO / path
    require(path in held, "partition held custody missing")
    partition = json.loads(held[path])
    endpoints = [r for r in partition["orbits"] if r["distance"] == 0]
    require(len(endpoints) == 1, "unique endpoint assignment")
    old.named_row(
        endpoints[0], names, document["d4"], old.images(endpoints[0]["mask"], document["d4"])
    )
    return polygons, names, roster, endpoints[0]["mask"], held


def construct(
    polygons: list[list[Point]], roster: list[dict[str, Any]], endpoint: int, *, deadline: float
) -> dict[str, Any]:
    require(
        len(roster) == 95 and len({r["mask"] for r in roster}) == 95,
        "complete95 distinct states required",
    )
    work = new_work()
    classifications = classify(polygons, work, deadline)
    endpoint_cells = [i for i in range(24) if endpoint & (1 << i)]
    control = capacity_dp(endpoint_cells, classifications, work, deadline)
    require(
        control["kind"] == "surviving_relaxation_assignment",
        "endpoint capacity calibration fails",
    )
    verify_state(control, classifications, deadline)
    states, obstructions = [], []
    for row in roster:
        tick(deadline)
        cells = [i for i in range(24) if row["mask"] & (1 << i)]
        result = capacity_dp(cells, classifications, work, deadline)
        if result["kind"] == "ordinary_assignment_obstruction":
            obstructions.append(row["mask"])
        states.append({"mask": row["mask"], "certificate": result})
    return {
        "status": "ordinary_assignment_obstructions" if obstructions else "criterion_missed",
        "criterion_met": bool(obstructions),
        **scope(obstruction=bool(obstructions)),
        "complete_classification": True,
        "classifications_accounted": 216,
        "states_accounted": 95,
        "obstructed_masks": obstructions,
        "classifications": classifications,
        "states": states,
        "endpoint_survivor": control,
        "work": work,
        "cell_geometry": "exact original closed polygons",
        "shared_half_extent": True,
        "physical_half_extent_squared_bound_checked": True,
        "closed_aliases_may_undercount_memberships": True,
        "guaranteed_window_order": ["SW", "SE", "NW", "NE"],
        "survival_is_not_physical_packing": True,
    }


def generate(document: Any, *, deadline: float) -> dict[str, Any]:
    frozen = finite.canonical(document)
    polygons, names, roster, endpoint, held = intake(document, deadline)
    result = construct(polygons, roster, endpoint, deadline=deadline)
    for path, raw in held.items():
        tick(deadline)
        with path.open("rb") as stream:
            require(
                stream.read(INPUT_LIMIT + 1) == raw, "corner-cardinality premise bytes changed"
            )
    require(finite.canonical(document) == frozen, "corner descriptor changed")
    tick(deadline)
    return {
        "schema": SCHEMA,
        **result,
        "accepted_inputs": copy.deepcopy(document),
        "verification_passed": False,
        "cell_names": names,
        "constants": {"U": str(U), "H": str(H), "r": str(R), "capacity": 10},
        "assurance": {
            "accepted_cover_partition_T061_inherited": True,
            "n11_proof_replayed": False,
            "mathematical_composition": "sole Astra hand proof",
        },
        "limits": {
            "cell_vertices": CELL_LIMIT,
            "polytope_rows": ROW_LIMIT,
            "triple_attempts": TRIPLE_LIMIT,
            "inequality_evaluations": INEQUALITY_LIMIT,
            "dp_transitions": TRANSITION_LIMIT,
            "per_state_dp_transitions": STATE_TRANSITION_LIMIT,
            "frontier_states": FRONTIER_LIMIT,
            "geometry_bits": finite.BIT_LIMIT,
            "output_bytes": OUTPUT_LIMIT,
        },
    }


def check(document: Any, certificate: Any, *, deadline: float) -> dict[str, Any]:
    require(type(certificate) is dict, "typed corner certificate")
    result = generate(document, deadline=deadline)
    require(payload(certificate) == payload(result), "fresh corner reconstruction differs")
    return result | {"verification_passed": True}


def failure(exc: Exception) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": "incomplete" if isinstance(exc, finite.IncompleteError) else "refused",
        "criterion_met": False,
        "complete_classification": False,
        "verification_passed": False,
        **scope(),
        "error": str(exc),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--descriptor", type=Path, required=True)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--max-seconds", type=float, default=120)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0:
        parser.error("max-seconds must be finite and positive")
    deadline = time.monotonic() + args.max_seconds
    try:
        raw, document = finite.read_json(args.descriptor, INPUT_LIMIT)
        if args.certificate:
            saved, certificate = finite.read_json(args.certificate, OUTPUT_LIMIT)
            result = check(document, certificate, deadline=deadline)
            require(
                saved == finite.read_json(args.certificate, OUTPUT_LIMIT)[0],
                "certificate changed",
            )
        else:
            result = generate(document, deadline=deadline)
        require(raw == finite.read_json(args.descriptor, INPUT_LIMIT)[0], "descriptor changed")
    except (finite.IncompleteError, ValueError, KeyError, TypeError, OSError, EOFError) as exc:
        result = failure(exc)
    result.update(
        provenance=provenance(Path(__file__), Path(old.__file__)),
        invocation={
            "argv": argv if argv is not None else sys.argv[1:],
            "executable": sys.executable,
        },
    )
    text = retained_json.dumps(result, sort_keys=True)
    if len(text.encode()) > OUTPUT_LIMIT or time.monotonic() >= deadline:
        result = failure(finite.IncompleteError("corner output byte or wall ceiling"))
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        stream.write(text)
    return 1 if result["status"] in ("incomplete", "refused") else 0


if __name__ == "__main__":
    raise SystemExit(main())
