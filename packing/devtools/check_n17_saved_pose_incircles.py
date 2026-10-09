"""Necessary incircle test of frozen saved poses; no whole-assignment exclusion."""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import math
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from devtools import check_n17_n11_corner_cardinality as corner
from devtools.provenance import provenance
from sqpack import retained_json

finite, require, tick, checked, payload = (
    corner.finite,
    corner.require,
    corner.tick,
    corner.checked,
    corner.payload,
)
SCHEMA = "n17-saved-pose-incircles/v1"
CONTEXT_SCHEMA = "n17-saved-pose-incircles-context/v1"
ROLES = ("corner_descriptor", "corner_certificate", "corner_replay")
INPUT_LIMIT, RECEIPT_LIMIT, OUTPUT_LIMIT = 10 << 20, 64 << 20, 1 << 20
POSE_LIMIT, ROW_LIMIT, PAIR_LIMIT = 216, 9072, 12920
type Pose = tuple[Q, Q, Q]


def scope() -> dict[str, bool]:
    return dict.fromkeys(
        (
            "ordinary_assignment_exclusion_proved",
            "membership_pattern_exclusion_proved",
            "global_bound_proved",
            "global_optimality_proved",
            "census_admission_proved",
            "physical_packing_proved",
            "orientation_realization_proved",
            "corner_classification_replayed",
            "capacity_dp_replayed",
            "endpoint_saved_pose_distance_control_required",
        ),
        False,
    )


def intake(document: Any, deadline: float) -> tuple[Any, ...]:
    require(
        type(document) is dict
        and document.get("schema") == CONTEXT_SCHEMA
        and set(document) == {"schema", *(k for r in ROLES for k in (r, r + "_sha256"))},
        "saved-pose descriptor differs",
    )
    document = cast(dict[str, Any], document)
    held: dict[Path, bytes] = {}
    records = {}
    for role in ROLES:
        tick(deadline)
        require(
            type(document[role]) is str and type(document[role + "_sha256"]) is str,
            "accepted role path/identity",
        )
        p = Path(document[role])
        p = (p if p.is_absolute() else corner.old.REPO / p).resolve()
        raw, record = finite.read_json(
            p, INPUT_LIMIT if role.endswith("descriptor") else RECEIPT_LIMIT
        )
        require(type(record) is dict, "accepted role JSON object required")
        require(
            hashlib.sha256(raw).hexdigest() == document[role + "_sha256"],
            "accepted role bytes differ",
        )
        require(p not in held or held[p] == raw, "conflicting accepted artifact alias")
        held[p], records[role] = raw, record
    accepted, replay = records["corner_certificate"], records["corner_replay"]
    require(
        accepted.get("schema") == corner.SCHEMA
        and accepted.get("status") == "criterion_missed"
        and accepted.get("criterion_met") is False
        and accepted.get("complete_classification") is True
        and accepted.get("classifications_accounted") == 216
        and type(accepted.get("classifications_accounted")) is int
        and accepted.get("states_accounted") == 95
        and type(accepted.get("states_accounted")) is int
        and accepted.get("accepted_inputs") == records["corner_descriptor"]
        and replay.get("verification_passed") is True
        and payload(accepted) == payload(replay)
        and all(accepted.get(k) is False for k in corner.scope())
        and accepted.get("physical_half_extent_squared_bound_checked") is True,
        "accepted complete308 miss premise differs",
    )
    polygons, names, roster, _, transitive = corner.intake(
        records["corner_descriptor"], deadline
    )
    for source_path, raw in transitive.items():
        path = source_path.resolve()
        require(path not in held or held[path] == raw, "conflicting transitive artifact alias")
        held[path] = raw
    require(accepted.get("cell_names") == names, "accepted original cell-name roster differs")
    require(
        accepted.get("constants")
        == {"U": str(corner.U), "H": str(corner.H), "r": str(corner.R), "capacity": 10},
        "accepted corner constants differ",
    )
    return polygons, names, roster, accepted, held


def table(classifications: Any) -> dict[tuple[int, int], dict[str, Any]]:
    require(
        type(classifications) is list and len(classifications) == POSE_LIMIT,
        "complete216 classifications required",
    )
    classifications = cast(list[Any], classifications)
    result = {}
    for record in classifications:
        require(type(record) is dict, "classification record")
        record = cast(dict[str, Any], record)
        cell, pattern = record["cell_index"], record["pattern_id"]
        require(
            type(cell) is int
            and cell in range(24)
            and type(pattern) is int
            and pattern in range(9),
            "typed cell-pattern identity",
        )
        key = cell, pattern
        require(key not in result, "duplicate classification identity")
        horizontal, vertical = corner.CLASSES[pattern]
        require(
            record.get("horizontal_class") == horizontal
            and record.get("vertical_class") == vertical
            and type(record.get("horizontal_class")) is int
            and type(record.get("vertical_class")) is int
            and record.get("guaranteed_window_bits")
            == list(corner.pattern_bits(horizontal, vertical))
            and all(type(bit) is int for bit in record["guaranteed_window_bits"])
            and type(record.get("feasible")) is bool,
            "classification class/bits differ",
        )
        result[key] = record
    return result


def validate_pose(
    polygon: list[corner.Point],
    record: dict[str, Any],
    work: dict[str, int],
    deadline: float,
) -> Pose:
    require(
        record["feasible"] is True
        and type(record.get("pose")) is list
        and len(record["pose"]) == 3,
        "saved feasible pose required",
    )
    pose = cast(Pose, tuple(finite.rational(value) for value in record["pose"]))
    rows = corner.pattern_rows(polygon, *corner.CLASSES[record["pattern_id"]])
    require(
        record.get("rows") == [list(map(str, row)) for row in rows],
        "saved used pattern rows differ",
    )
    for row in rows:
        tick(deadline)
        work["one_square_inequalities"] += 1
        if work["one_square_inequalities"] > ROW_LIMIT:
            raise finite.IncompleteError("one-square inequality ceiling")
        require(corner.value(row, pose) <= row[3], "saved pose violates one-square row")
    require(
        pose[2] >= Q(1, 2) and checked(2 * checked(pose[2] * pose[2])) <= 1,
        "saved pose physical half-extent differs",
    )
    return pose


def distance_squared(left: Pose, right: Pose) -> Q:
    x, y = checked(left[0] - right[0]), checked(left[1] - right[1])
    return checked(checked(x * x) + checked(y * y))


def evaluate_pairs(
    cells: list[int],
    poses: list[Pose],
    names: list[str],
    work: dict[str, int],
    deadline: float,
) -> dict[str, Any]:
    require(
        len(cells) == len(poses) == 17 and cells == sorted(set(cells)), "fixed17 pair roster"
    )
    failures, first = 0, None
    for i, j in itertools.combinations(range(17), 2):
        tick(deadline)
        work["distance_pairs"] += 1
        if work["distance_pairs"] > PAIR_LIMIT:
            raise finite.IncompleteError("distance-pair ceiling")
        distance = distance_squared(poses[i], poses[j])
        if distance < 1:
            failures += 1
            if first is None:
                first = {
                    "cells": [cells[i], cells[j]],
                    "names": [names[cells[i]], names[cells[j]]],
                    "squared_distance": str(distance),
                }
    return {
        "pairs_checked": 136,
        "failing_pair_count": failures,
        "first_failing_pair": first,
        "incircle_compatible": failures == 0,
    }


def construct(
    polygons: list[list[corner.Point]],
    names: list[str],
    roster: list[dict[str, Any]],
    accepted: dict[str, Any],
    *,
    deadline: float,
) -> dict[str, Any]:
    require(len(polygons) == len(names) == 24 and len(set(names)) == 24, "original24 cells")
    require(len(roster) == 95 and len({r["mask"] for r in roster}) == 95, "complete95 roster")
    states = accepted["states"]
    require(
        type(states) is list and len(states) == 95 and all(type(s) is dict for s in states),
        "saved95 state objects required",
    )
    states = cast(list[dict[str, Any]], states)
    require(
        all(type(s.get("mask")) is int for s in states)
        and [s["mask"] for s in states] == [r["mask"] for r in roster],
        "saved95 mask roster differs",
    )
    classified = table(accepted["classifications"])
    cache: dict[tuple[int, int], Pose] = {}
    work = {"one_square_inequalities": 0, "distance_pairs": 0}
    reports, survivors = [], []
    for state, row in zip(states, roster, strict=True):
        tick(deadline)
        mask = row["mask"]
        require(
            type(mask) is int and 0 <= mask < 1 << 24 and mask.bit_count() == 17, "typed17 mask"
        )
        chosen = state["certificate"]
        require(type(chosen) is dict, "saved capacity witness object required")
        chosen = cast(dict[str, Any], chosen)
        cells = [i for i in range(24) if mask & (1 << i)]
        require(
            chosen.get("kind") == "surviving_relaxation_assignment"
            and chosen.get("cells") == cells
            and all(type(c) is int for c in chosen["cells"])
            and type(chosen.get("pattern_ids")) is list
            and len(chosen["pattern_ids"]) == 17,
            "frozen saved17 choice differs",
        )
        counts = [0] * 4
        poses = []
        for cell, pattern in zip(cells, chosen["pattern_ids"], strict=True):
            require(type(pattern) is int and pattern in range(9), "typed saved pattern ID")
            key = cell, pattern
            record = classified[key]
            if key not in cache:
                cache[key] = validate_pose(polygons[cell], record, work, deadline)
            poses.append(cache[key])
            counts = [
                a + b for a, b in zip(counts, record["guaranteed_window_bits"], strict=True)
            ]
        require(
            chosen.get("counts") == counts
            and max(counts) <= 10
            and all(type(c) is int for c in chosen["counts"]),
            "saved guaranteed capacity differs",
        )
        result = evaluate_pairs(cells, poses, names, work, deadline)
        if result["incircle_compatible"]:
            survivors.append(mask)
        reports.append(
            {
                "mask": mask,
                "saved_choice_identity": finite.identity(chosen),
                "cells": cells,
                "pattern_ids": copy.deepcopy(chosen["pattern_ids"]),
                "guaranteed_counts": counts,
                **result,
            }
        )
    require(work["distance_pairs"] == PAIR_LIMIT, "complete12920 pair accounting")
    return {
        "status": "orientation_realization_candidates"
        if survivors
        else "all_fixed_poses_rejected",
        "criterion_met": bool(survivors),
        "complete_classification": True,
        "states_accounted": 95,
        "incircle_compatible_masks": survivors,
        "states": reports,
        "used_pose_validations": len(cache),
        "work": work,
        "used_saved_poses": [
            {
                "cell_index": cell,
                "pattern_id": pattern,
                "pose": list(map(str, cache[cell, pattern])),
            }
            for cell, pattern in sorted(cache)
        ],
        "endpoint_capacity_control_inherited": True,
        "alternate_choices_attempted": False,
        "incircle_compatibility_is_not_square_packing": True,
        **scope(),
    }


def generate(document: Any, *, deadline: float) -> dict[str, Any]:
    frozen = finite.canonical(document)
    polygons, names, roster, accepted, held = intake(document, deadline)
    result = construct(polygons, names, roster, accepted, deadline=deadline)
    for path, raw in held.items():
        tick(deadline)
        with path.open("rb") as stream:
            require(stream.read(len(raw) + 1) == raw, "saved-pose premise bytes changed")
    require(finite.canonical(document) == frozen, "saved-pose descriptor changed")
    tick(deadline)
    return {
        "schema": SCHEMA,
        **result,
        "accepted_inputs": copy.deepcopy(document),
        "verification_passed": False,
        "assurance": {
            "accepted308_full_classification_inherited": True,
            "original_cover_partition_T061_inherited": True,
            "mathematical_composition": "sole Astra hand incircle implication",
        },
        "limits": {
            "used_pose_validations": POSE_LIMIT,
            "one_square_inequalities": ROW_LIMIT,
            "distance_pairs": PAIR_LIMIT,
            "used_computed_rational_bits": finite.BIT_LIMIT,
            "descriptor_bytes": INPUT_LIMIT,
            "accepted_receipt_bytes": RECEIPT_LIMIT,
            "output_bytes": OUTPUT_LIMIT,
        },
    }


def check(document: Any, certificate: Any, *, deadline: float) -> dict[str, Any]:
    require(type(certificate) is dict, "saved-pose certificate required")
    result = generate(document, deadline=deadline)
    require(payload(certificate) == payload(result), "fresh saved-pose reconstruction differs")
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
    parser.add_argument("--max-seconds", type=float, default=60)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or not 0 < args.max_seconds <= 60:
        parser.error("max-seconds must be finite and in (0,60]")
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
    except (
        finite.IncompleteError,
        ValueError,
        KeyError,
        TypeError,
        OSError,
        EOFError,
        ArithmeticError,
    ) as exc:
        result = failure(exc)
    result.update(
        provenance=provenance(Path(__file__), Path(corner.__file__)),
        invocation={
            "argv": argv if argv is not None else sys.argv[1:],
            "executable": sys.executable,
        },
    )
    text = retained_json.dumps(result, sort_keys=True)
    if len(text.encode()) > OUTPUT_LIMIT or time.monotonic() >= deadline:
        result = failure(finite.IncompleteError("saved-pose output byte or wall ceiling"))
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        _ = stream.write(text)
    return 1 if result["status"] in ("incomplete", "refused") else 0


if __name__ == "__main__":
    raise SystemExit(main())
