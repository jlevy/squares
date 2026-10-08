"""Exact whole-square envelope windows using an inherited eleven-square bound."""

from __future__ import annotations

import argparse
import copy
import hashlib
import math
import re
import subprocess
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

import yaml

from devtools import probe_n17_conditional_owned_hull as finite
from devtools.provenance import provenance
from sqpack import retained_json

SCHEMA = "n17-n11-envelope-windows/v1"
CONTEXT_SCHEMA = "n17-n11-envelope-windows-context/v1"
REPO = Path(__file__).resolve().parents[2]
U, R, H, B11 = Q(1169, 250), Q(707107, 1000000), Q(31, 8), Q(3875000000, 999999999)
INPUT_LIMIT = 10 << 20
OUTPUT_LIMIT = 64 << 20
STATE_LIMIT = 95
ROLES = ("partition", "cover", "theorem_registry", "theorem_replay")
type Box = tuple[Q, Q, Q, Q]


def require(condition: bool, message: str) -> None:  # noqa: FBT001
    if not condition:
        raise ValueError(message)


def tick(deadline: float) -> None:
    if time.monotonic() >= deadline:
        raise finite.IncompleteError("envelope wall ceiling")


def payload(value: dict[str, Any]) -> dict[str, Any]:
    return {
        k: v
        for k, v in value.items()
        if k not in {"verification_passed", "provenance", "invocation"}
    }


def scope(*, obstruction: bool = False) -> dict[str, bool]:
    return {
        "global_optimality_proved": False,
        "census_admission_proved": False,
        "ledger_admission_performed": False,
        "root_geometry_replayed": False,
        "n11_theorem_reproved": False,
        "normalized_contact_rank_used": False,
        "global_bound_proved": False,
        "ordinary_assignment_exclusion_proved": obstruction,
    }


def images(mask: int, permutations: dict[str, list[int]]) -> set[int]:
    return {
        sum(1 << permutation[i] for i in range(24) if mask & (1 << i))
        for permutation in permutations.values()
    }


def theorem(registry: Any, replay: Any) -> None:
    require(
        type(registry) is dict and type(registry.get("results")) is list,
        "theorem registry required",
    )
    registry = cast(dict[str, Any], registry)
    entries = [r for r in registry["results"] if type(r) is dict and r.get("id") == "T-061"]
    require(len(entries) == 1, "unique T-061 required")
    entry = entries[0]
    require(
        entry.get("kind") == "lower-bound"
        and entry.get("scope") == {"n_values": [11]}
        and entry.get("verification") == "V3"
        and entry.get("confirmation") == "C3"
        and type(entry.get("claim")) is str
        and entry["claim"].startswith("s(11) > 3875000000/999999999")
        and {"E-n011-wang-li-source-replay", "E-n011-wang-li-native-parent-core"}
        <= set(entry.get("evidence", [])),
        "accepted T-061 evidence differs",
    )
    require(
        replay
        == {
            "status": "PASS_FRESH_TWO_IMPLEMENTATION_FULL_REPLAY",
            "certificate_sha256": (
                "31e10ceb8368cc858e61f45ce7cfee783e8d0c7910893559164810f45439cc34"
            ),
            "rows": 12028,
            "histogram": {"1000047559": 12028},
            "surplus_units": 428125,
        },
        "accepted n11 replay premise differs",
    )


def named_row(
    row: dict[str, Any],
    names: list[str],
    permutations: dict[str, list[int]],
    endpoint_images: set[int],
) -> None:
    orbit = images(row["mask"], permutations)
    require(
        row["mask"] == min(orbit)
        and row.get("orbit_size") == len(orbit)
        and row.get("cells") == [names[i] for i in range(24) if row["mask"] & (1 << i)]
        and row["distance"] == min((row["mask"] ^ e).bit_count() for e in endpoint_images),
        "complete named orbit/distance join differs",
    )


def read_registry(document: dict[str, Any], deadline: float) -> Any:
    """Read curated theorem prose through Git; revision is provenance, not a code lock."""
    require(
        document["theorem_registry"] == "packing/frontier/results.yaml"
        and type(document["theorem_registry_git_commit"]) is str
        and re.fullmatch(r"[0-9a-f]{40}", document["theorem_registry_git_commit"]) is not None,
        "curated registry Git identity required",
    )
    object_name = document["theorem_registry_git_commit"] + ":" + document["theorem_registry"]
    tick(deadline)
    timeout = min(10.0, max(0.001, deadline - time.monotonic()))
    kind = subprocess.run(
        ["git", "cat-file", "-t", document["theorem_registry_git_commit"]],
        cwd=REPO,
        capture_output=True,
        check=True,
        timeout=timeout,
    ).stdout
    require(kind == b"commit\n", "registry revision must resolve to a Git commit")
    tick(deadline)
    size = subprocess.run(
        ["git", "cat-file", "-s", object_name],
        cwd=REPO,
        capture_output=True,
        check=True,
        timeout=min(10.0, max(0.001, deadline - time.monotonic())),
    ).stdout
    require(len(size) <= 32 and size.strip().isdigit(), "registry Git byte count required")
    if int(size) > INPUT_LIMIT:
        raise finite.IncompleteError("theorem registry byte ceiling")
    tick(deadline)
    raw = subprocess.run(
        ["git", "show", object_name],
        cwd=REPO,
        capture_output=True,
        check=True,
        timeout=min(10.0, max(0.001, deadline - time.monotonic())),
    ).stdout
    require(len(raw) == int(size), "registry Git object size differs")
    tick(deadline)
    return yaml.safe_load(raw)


def intake(
    document: Any, deadline: float
) -> tuple[list[Box], list[str], list[dict[str, Any]], dict[Path, bytes]]:
    require(
        type(document) is dict
        and set(document)
        == {
            "schema",
            "outer_U",
            "radius",
            "window_side",
            "n11_lower_bound",
            "n11_premise",
            "partition",
            "partition_sha256",
            "cover",
            "cover_sha256",
            "states",
            "d4",
            "theorem_registry",
            "theorem_registry_git_commit",
            "theorem_replay",
            "theorem_replay_sha256",
            "required_squares",
        }
        and document["schema"] == CONTEXT_SCHEMA
        and document["outer_U"] == str(U)
        and document["radius"] == str(R)
        and document["window_side"] == str(H)
        and document["n11_lower_bound"] == str(B11)
        and document["n11_premise"] == "T-061",
        "frozen envelope context differs",
    )
    document = cast(dict[str, Any], document)
    held: dict[Path, bytes] = {}
    records = {}
    require(
        type(document["required_squares"]) is int and document["required_squares"] == 11,
        "eleven-square theorem arity differs",
    )
    for role in ROLES:
        tick(deadline)
        if role == "theorem_registry":
            records[role] = read_registry(document, deadline)
            continue
        require(
            type(document[role]) is str and type(document[role + "_sha256"]) is str,
            "accepted role path/identity required",
        )
        path = Path(document[role])
        path = path if path.is_absolute() else REPO / path
        raw, record = finite.read_json(path, INPUT_LIMIT)
        require(
            type(record) is dict
            and hashlib.sha256(raw).hexdigest() == document[role + "_sha256"],
            "accepted role bytes differ",
        )
        require(path not in held or held[path] == raw, "conflicting accepted role path")
        held[path] = raw
        records[role] = record
    theorem(records["theorem_registry"], records["theorem_replay"])
    from devtools.check_n17_capacity_one_cover import (  # noqa: PLC0415
        DESIGNS,
        UNIQUE_24,
        build_cover,
        cell_record,
        d4_permutations,
    )

    cells = build_cover(DESIGNS[UNIQUE_24.name])
    permutations = d4_permutations(cells)
    require(permutations is not None, "D4 catalogue absent")
    permutations = cast(dict[str, list[int]], permutations)
    cover, part = records["cover"], records["partition"]
    require(
        all(type(cover.get(k)) is dict for k in ("criterion", "design", "d4")),
        "typed cover premises required",
    )
    require(
        cover.get("schema") == "n17-capacity-one-cover/v1"
        and cover.get("criterion", {}).get("passed") is True
        and cover.get("design", {}).get("name") == UNIQUE_24.name
        and cover.get("design", {}).get("cap") == str(U)
        and cover.get("cells") == [cell_record(cell) for cell in cells]
        and cover.get("d4", {}).get("permutations") == permutations,
        "accepted full cover catalogue differs",
    )
    require(
        part.get("schema") == "n17-certified-residue-stratification/v1"
        and part.get("design") == UNIQUE_24.name
        and part.get("cap") == str(U)
        and part.get("certified")
        == {
            "admitted": 60,
            "endpoint_survives": True,
            "orbits": 4683,
            "surviving_states": 36768,
        },
        "accepted ordinary residue differs",
    )
    rows = part.get("orbits")
    require(type(rows) is list and len(rows) == 4683, "complete partition roster required")
    rows = cast(list[dict[str, Any]], rows)
    require(
        type(rows) is list
        and len(rows) == 4683
        and all(
            type(r) is dict
            and type(r.get("mask")) is int
            and 0 <= r["mask"] < 1 << 24
            and r["mask"].bit_count() == 17
            and type(r.get("distance")) is int
            for r in rows
        )
        and len({r["mask"] for r in rows}) == 4683,
        "complete typed partition required",
    )
    endpoints = [r for r in rows if r["distance"] == 0]
    require(len(endpoints) == 1, "one endpoint orbit required")
    endpoint_images = images(endpoints[0]["mask"], permutations)
    names = [c.name for c in cells]
    for row in rows:
        tick(deadline)
        named_row(row, names, permutations, endpoint_images)
    selected = sorted((r for r in rows if r["distance"] == 2), key=lambda r: r["mask"])
    require(len(selected) == STATE_LIMIT, "all95 distance-two states required")
    roster = []
    for row in selected:
        tick(deadline)
        orbit = images(row["mask"], permutations)
        named = [names[i] for i in range(24) if row["mask"] & (1 << i)]
        require(
            row["mask"] == min(orbit)
            and row.get("orbit_size") == len(orbit)
            and row.get("cells") == named
            and min((row["mask"] ^ e).bit_count() for e in endpoint_images) == 2,
            "named orbit/distance join differs",
        )
        roster.append({"mask": row["mask"], "cells": named, "orbit_size": len(orbit)})
    require(
        document["states"] == roster and document["d4"] == permutations,
        "complete descriptor roster/D4 differs",
    )
    boxes = [
        (
            min(p[0] for p in c.vertices),
            max(p[0] for p in c.vertices),
            min(p[1] for p in c.vertices),
            max(p[1] for p in c.vertices),
        )
        for c in cells
    ]
    return boxes, names, roster, held


def envelopes(boxes: list[Box], deadline: float) -> list[Box]:
    require(len(boxes) == 24 and 2 * R * R >= 1 and H < B11, "scalar premises differ")
    result: list[Box] = []
    for lx, ux, ly, uy in boxes:
        tick(deadline)
        for value in (lx, ux, ly, uy):
            finite.checked(value)
        require(0 <= lx <= ux <= U and 0 <= ly <= uy <= U, "cell AABB outside original frame")
        rectangle = (max(Q(0), lx - R), min(U, ux + R), max(Q(0), ly - R), min(U, uy + R))
        require(
            rectangle[0] <= rectangle[1] and rectangle[2] <= rectangle[3],
            "empty clipped envelope",
        )
        result.append(
            (
                finite.checked(rectangle[0]),
                finite.checked(rectangle[1]),
                finite.checked(rectangle[2]),
                finite.checked(rectangle[3]),
            )
        )
    return result


def contained(rectangle: Box, left: Q, bottom: Q) -> bool:
    lx, ux, ly, uy = rectangle
    return left <= lx and ux <= left + H and bottom <= ly and uy <= bottom + H


def window_roster(
    rectangles: list[Box], names: list[str], deadline: float
) -> list[dict[str, Any]]:
    require(
        len(rectangles) == len(names) == 24 and len(set(names)) == 24, "cell roster differs"
    )
    windows = []
    for a in range(24):
        for b in range(24):
            tick(deadline)
            left, bottom = rectangles[a][0], rectangles[b][2]
            windows.append(
                {
                    "anchor_indices": [a, b],
                    "anchor_cells": [names[a], names[b]],
                    "window": list(
                        map(
                            str,
                            (
                                left,
                                finite.checked(left + H),
                                bottom,
                                finite.checked(bottom + H),
                            ),
                        )
                    ),
                    "contained_cell_mask": sum(
                        1 << i for i, r in enumerate(rectangles) if contained(r, left, bottom)
                    ),
                }
            )
    return windows


def scan_state(
    mask: int, windows: list[dict[str, Any]], names: list[str], deadline: float
) -> dict[str, Any]:
    require(
        type(mask) is int and 0 <= mask < 1 << 24 and mask.bit_count() == 17,
        "seventeen distinct occupied cells required",
    )
    require(len(windows) == 576 and len(names) == 24, "complete window roster required")
    counts = []
    witness = None
    for window in windows:
        tick(deadline)
        inside = mask & window["contained_cell_mask"]
        count = inside.bit_count()
        counts.append(count)
        if witness is None and count >= 11:
            included = [i for i in range(24) if inside & (1 << i)]
            witness = {
                k: copy.deepcopy(window[k])
                for k in ("anchor_indices", "anchor_cells", "window")
            }
            witness.update(cell_indices=included[:11], cells=[names[i] for i in included[:11]])
    return {
        "mask": mask,
        "window_counts": counts,
        "windows_accounted": 576,
        "maximum_full_envelope_count": max(counts),
        "first_argmax_anchor_indices": windows[counts.index(max(counts))]["anchor_indices"],
        "ordinary_assignment_obstruction": witness is not None,
        "witness": witness,
    }


def verify_witness(mask: int, rectangles: list[Box], names: list[str], witness: Any) -> None:
    require(type(witness) is dict, "eleven-cell witness required")
    anchors, indices = witness["anchor_indices"], witness["cell_indices"]
    require(
        len(anchors) == 2
        and all(type(i) is int and 0 <= i < 24 for i in anchors)
        and len(indices) == 11
        and indices == sorted(set(indices))
        and all(type(i) is int and 0 <= i < 24 and mask & (1 << i) for i in indices),
        "distinct occupied witness cells required",
    )
    left, bottom = rectangles[anchors[0]][0], rectangles[anchors[1]][2]
    require(
        witness["anchor_cells"] == [names[i] for i in anchors]
        and witness["cells"] == [names[i] for i in indices]
        and witness["window"] == list(map(str, (left, left + H, bottom, bottom + H)))
        and H < B11
        and all(contained(rectangles[i], left, bottom) for i in indices),
        "whole-square envelope containment or inherited bound differs",
    )


def generate(document: Any, *, deadline: float) -> dict[str, Any]:
    boxes, names, roster, held = intake(document, deadline)
    rectangles = envelopes(boxes, deadline)
    windows = window_roster(rectangles, names, deadline)
    require(len(roster) == STATE_LIMIT, "complete95 roster required")
    outcomes = [scan_state(row["mask"], windows, names, deadline) for row in roster]
    for outcome in outcomes:
        if outcome["witness"] is not None:
            verify_witness(outcome["mask"], rectangles, names, outcome["witness"])
    for path, raw in held.items():
        tick(deadline)
        with path.open("rb") as stream:
            current = stream.read(INPUT_LIMIT + 1)
        require(current == raw, "accepted premise bytes changed")
    positives = [r["mask"] for r in outcomes if r["ordinary_assignment_obstruction"]]
    return {
        "schema": SCHEMA,
        "status": "ordinary_assignment_obstructions" if positives else "criterion_missed",
        "criterion_met": bool(positives),
        "verification_passed": False,
        "accepted_inputs": copy.deepcopy(document),
        "states_accounted": len(outcomes),
        "windows_per_state": 576,
        "states": outcomes,
        "obstructed_masks": positives,
        "full_envelopes": [list(map(str, b)) for b in rectangles],
        "window_roster": windows,
        "state_window_counts_accounted": len(outcomes) * 576,
        "scalar_checks": {
            "two_radius_squared": str(2 * R * R),
            "window_strictly_below_n11_bound": H < B11,
            "bound_gap": str(B11 - H),
        },
        "assurance": {
            "original_full_cover_inherited": True,
            "n11_T061_inherited": True,
            "t061_proof_inherited": True,
            "t061_proof_replayed": False,
            "curated_registry_git_revision_is_provenance_not_code_lock": True,
            "composition_assurance": (
                "sole Astra hand composition, fresh finite arithmetic reconstruction"
            ),
            "full_square_envelopes_not_centre_boxes": True,
            "all576_anchors_including_aliases": True,
            "negative_scope": "this envelope criterion only",
        },
        "witness_tie_order": (
            "catalogue anchor indices(a,b), then ascending occupied catalogue indices"
        ),
        **scope(obstruction=bool(positives)),
    }


def check(document: Any, certificate: Any, *, deadline: float) -> dict[str, Any]:
    expected = generate(document, deadline=deadline)
    require(
        type(certificate) is dict and payload(certificate) == payload(expected),
        "fresh envelope payload differs",
    )
    tick(deadline)
    return copy.deepcopy(expected) | {"verification_passed": True}


def failure(exc: Exception) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": "incomplete" if isinstance(exc, finite.IncompleteError) else "refused",
        "error": str(exc),
        "criterion_met": False,
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
    if (
        not math.isfinite(args.max_seconds)
        or not 0 < args.max_seconds <= 60
        or args.output.exists()
    ):
        parser.error("finite phase ceiling at most60s and new output required")
    deadline = time.monotonic() + args.max_seconds
    try:
        raw, document = finite.read_json(args.descriptor, INPUT_LIMIT)
        if args.certificate:
            saved, certificate = finite.read_json(args.certificate, OUTPUT_LIMIT)
            result = check(document, certificate, deadline=deadline)
            require(
                saved == finite.read_json(args.certificate, OUTPUT_LIMIT)[0],
                "saved certificate changed",
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
        yaml.YAMLError,
        subprocess.SubprocessError,
    ) as exc:
        result = failure(exc)
    result.update(
        provenance=provenance(Path(__file__)),
        invocation={"argv": argv if argv is not None else sys.argv[1:]},
    )
    text = retained_json.dumps(result, sort_keys=True)
    if len(text.encode()) > OUTPUT_LIMIT or time.monotonic() >= deadline:
        result = failure(finite.IncompleteError("output byte or wall ceiling"))
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        stream.write(text)
    return (
        0 if result["status"] in ("ordinary_assignment_obstructions", "criterion_missed") else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
