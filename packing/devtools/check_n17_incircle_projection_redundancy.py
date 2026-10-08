"""Exact extreme-vertex redundancy test; no shared-centre LP or packing claim."""

from __future__ import annotations

import argparse
import copy
import itertools
import math
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from devtools import check_n17_saved_pose_incircles as prior
from devtools.provenance import provenance
from sqpack import retained_json

finite, require, checked, tick, payload = (
    prior.finite,
    prior.require,
    prior.checked,
    prior.tick,
    prior.payload,
)
SCHEMA = "n17-incircle-projection-redundancy/v1"
CONTEXT_SCHEMA = "n17-incircle-projection-redundancy-context/v1"
U = prior.corner.U
FACES = tuple(
    (a * s, b * t) for a, b in ((7, 3), (3, 7)) for s, t in itertools.product((-1, 1), repeat=2)
)
CELL_LIMIT, E_LIMIT, D_LIMIT = 32, 36, 72
PAIR_LIMIT, DIFFERENCE_LIMIT, FACE_LIMIT = 276, 357696, 158976
OUTPUT_LIMIT = 1 << 20
type Point = tuple[Q, Q]


def scope() -> dict[str, bool]:
    return dict.fromkeys(
        (
            "physical_packing_proved",
            "ordinary_assignment_exclusion_proved",
            "census_admission_proved",
            "global_bound_proved",
            "global_optimality_proved",
            "shared_center_LP_solved",
            "saved_pose_distance_replayed",
        ),
        False,
    )


def centre_projection(polygon: list[Point], deadline: float) -> list[Point]:
    require(0 < len(polygon) <= CELL_LIMIT, "original cell vertex roster")
    points = [(checked(x), checked(y)) for x, y in polygon]
    points = finite.hull(points)
    for a, b, c in (
        (Q(-1), Q(0), Q(-1, 2)),
        (Q(1), Q(0), checked(U - Q(1, 2))),
        (Q(0), Q(-1), Q(-1, 2)),
        (Q(0), Q(1), checked(U - Q(1, 2))),
    ):
        tick(deadline)
        points = finite.clip(points, a, b, c)
        if len(points) > E_LIMIT:
            raise finite.IncompleteError("centre projection vertex ceiling")
    require(bool(points), "empty unconditioned centre projection requires separate review")
    return points


def difference_hull(
    left: list[Point], right: list[Point], work: dict[str, int], deadline: float
) -> list[Point]:
    tick(deadline)
    proposals = len(left) * len(right)
    work["vertex_differences"] += proposals
    if work["vertex_differences"] > DIFFERENCE_LIMIT:
        raise finite.IncompleteError("vertex-difference ceiling")
    points = []
    for p, q in itertools.product(left, right):
        tick(deadline)
        points.append((checked(q[0] - p[0]), checked(q[1] - p[1])))
    result = finite.hull(points)
    if len(result) > D_LIMIT:
        raise finite.IncompleteError("difference hull vertex ceiling")
    tick(deadline)
    return result


def vertex_cover(
    points: list[Point], work: dict[str, int], deadline: float
) -> list[int | None]:
    """Only canonical EXTREME vertices decide equality; touching is retained."""
    require(
        points == finite.hull(points) and bool(points),
        "canonical nonempty difference hull required",
    )
    witnesses = []
    for p in points:
        first = None
        for index, normal in enumerate(FACES):
            tick(deadline)
            work["face_checks"] += 1
            if work["face_checks"] > FACE_LIMIT:
                raise finite.IncompleteError("octagon face ceiling")
            value = finite.dot(p, normal)
            if value >= 7 and first is None:
                first = index
        witnesses.append(first)
    return witnesses


def construct(
    polygons: list[list[Point]],
    names: list[str],
    roster: list[dict[str, Any]],
    *,
    deadline: float,
) -> dict[str, Any]:
    require(
        len(polygons) == len(names) == 24 and len(set(names)) == 24, "original24 cell roster"
    )
    require(
        len(roster) == 95 and len({r["mask"] for r in roster}) == 95, "complete95 mask roster"
    )
    cells = []
    pairs = set()
    for record in roster:
        mask = record["mask"]
        require(
            type(mask) is int and 0 <= mask < 1 << 24 and mask.bit_count() == 17, "typed17 mask"
        )
        occupied = [i for i in range(24) if mask & (1 << i)]
        cells.append(occupied)
        pairs.update(itertools.combinations(occupied, 2))
    require(len(pairs) <= PAIR_LIMIT, "relevant pair roster")
    domains = [centre_projection(p, deadline) for p in polygons]
    work = {"vertex_differences": 0, "face_checks": 0, "state_pairs_accounted": 0}
    reports = []
    potential = []
    for i, j in sorted(pairs):
        d = difference_hull(domains[i], domains[j], work, deadline)
        witnesses = vertex_cover(d, work, deadline)
        inside = [k for k, face in enumerate(witnesses) if face is None]
        if inside:
            potential.append([i, j])
        reports.append(
            {
                "cells": [i, j],
                "difference_hull": finite.serial(d),
                "retained_outside_face_indices": witnesses,
                "strict_inside_extreme_indices": inside,
                "convexified_pair_constraint_redundant": not inside,
            }
        )
    states = []
    redundant = not potential
    for record, occupied in zip(roster, cells, strict=True):
        tick(deadline)
        work["state_pairs_accounted"] += len(list(itertools.combinations(occupied, 2)))
        states.append(
            {
                "mask": record["mask"],
                "cells": occupied,
                "pairs_accounted": 136,
                "uncoupled_centre_vertices": finite.serial([domains[i][0] for i in occupied]),
                "shared_convexified_relaxation_witness_checked": redundant,
            }
        )
    require(work["state_pairs_accounted"] == 12920, "full95 pair accounting")
    return {
        "schema": SCHEMA,
        "status": "strict_difference_cuts_detected"
        if potential
        else "all_pair_projection_constraints_redundant",
        "criterion_met": bool(potential),
        "complete_classification": True,
        "cell_names": names,
        "states_accounted": 95,
        "relevant_pairs_accounted": len(pairs),
        "faces": [[*n, 7] for n in FACES],
        "U": str(U),
        "centre_projections": [finite.serial(p) for p in domains],
        "pairs": reports,
        "potential_cut_pairs": potential,
        "states": states,
        "work": work,
        "all95_shared_convexified_relaxations_redundant": redundant,
        "mathematical_assurance": (
            "sole Astra hand extreme-vertex equivalence; "
            "no independent mathematical confirmation"
        ),
        **scope(),
    }


def generate(document: Any, *, deadline: float) -> dict[str, Any]:
    require(
        type(document) is dict and document.get("schema") == CONTEXT_SCHEMA,
        "projection descriptor schema",
    )
    frozen = finite.canonical(document)
    adapted = copy.deepcopy(document) | {"schema": prior.CONTEXT_SCHEMA}
    polygons, names, roster, _accepted, held = prior.intake(adapted, deadline)
    result = construct(polygons, names, roster, deadline=deadline)
    for p, raw in held.items():
        tick(deadline)
        with p.open("rb") as stream:
            require(stream.read(len(raw) + 1) == raw, "projection premise bytes changed")
    require(finite.canonical(document) == frozen, "projection descriptor changed")
    tick(deadline)
    return result | {
        "accepted_inputs": copy.deepcopy(document),
        "verification_passed": False,
        "accepted308_geometry_premises_inherited": True,
        "limits": {
            "output_bytes": OUTPUT_LIMIT,
            "descriptor_bytes": prior.INPUT_LIMIT,
            "accepted_receipt_bytes": prior.RECEIPT_LIMIT,
            "rational_bits": finite.BIT_LIMIT,
            "cell_vertices": CELL_LIMIT,
            "projection_vertices": E_LIMIT,
            "difference_vertices": D_LIMIT,
            "relevant_pairs": PAIR_LIMIT,
            "vertex_differences": DIFFERENCE_LIMIT,
            "face_checks": FACE_LIMIT,
        },
    }


def check(document: Any, certificate: Any, *, deadline: float) -> dict[str, Any]:
    require(type(certificate) is dict, "projection certificate object")
    result = generate(document, deadline=deadline)
    require(payload(certificate) == payload(result), "fresh projection reconstruction differs")
    return result | {"verification_passed": True}


def failure(exc: Exception) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": "incomplete" if isinstance(exc, finite.IncompleteError) else "refused",
        "error": str(exc),
        "criterion_met": False,
        "complete_classification": False,
        "verification_passed": False,
        **scope(),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--descriptor", type=Path, required=True)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-seconds", type=float, default=60)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or not 0 < args.max_seconds <= 60:
        parser.error("max-seconds must be finite in(0,60]")
    deadline = time.monotonic() + args.max_seconds
    try:
        raw, document = finite.read_json(args.descriptor, prior.INPUT_LIMIT)
        if args.certificate:
            saved, certificate = finite.read_json(args.certificate, OUTPUT_LIMIT)
            result = check(document, certificate, deadline=deadline)
            require(
                saved == finite.read_json(args.certificate, OUTPUT_LIMIT)[0],
                "certificate changed",
            )
        else:
            result = generate(document, deadline=deadline)
        require(
            raw == finite.read_json(args.descriptor, prior.INPUT_LIMIT)[0], "descriptor changed"
        )
    except (
        ValueError,
        TypeError,
        KeyError,
        OSError,
        EOFError,
        ArithmeticError,
        finite.IncompleteError,
    ) as exc:
        result = failure(exc)
    result.update(
        provenance=provenance(Path(__file__), Path(prior.__file__)),
        invocation={
            "argv": argv if argv is not None else sys.argv[1:],
            "executable": sys.executable,
        },
    )
    text = retained_json.dumps(result, sort_keys=True)
    if len(text.encode()) > OUTPUT_LIMIT or time.monotonic() >= deadline:
        result = failure(finite.IncompleteError("projection output byte or wall ceiling"))
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        _ = stream.write(text)
    return int(result["status"] in ("incomplete", "refused"))


if __name__ == "__main__":
    raise SystemExit(main())
