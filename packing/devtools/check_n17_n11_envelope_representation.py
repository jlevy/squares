"""Wall-coupled upper envelopes and optimistic independent-AABB lower bounds."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from devtools import check_n17_n11_envelope_windows as old
from devtools.provenance import provenance
from sqpack import retained_json

SCHEMA = "n17-n11-envelope-representation/v1"
CONTEXT_SCHEMA = "n17-n11-envelope-representation-context/v1"
ROLES = ("prior_descriptor", "prior_certificate", "prior_replay")
U, R, H, B11 = old.U, old.R, old.H, old.B11
INPUT_LIMIT, OUTPUT_LIMIT = old.INPUT_LIMIT, old.OUTPUT_LIMIT
finite = old.finite
require, tick, payload = old.require, old.tick, old.payload
type Box = tuple[Q, Q, Q, Q]


def scope(*, obstruction: bool = False, killed: bool = False) -> dict[str, bool]:
    return old.scope(obstruction=obstruction) | {
        "independent_whole_cell_aabb_architecture_killed": killed,
        "lower_envelope_physical_packing_proved": False,
    }


def representations(boxes: list[Box], deadline: float) -> tuple[list[Box], list[Box]]:
    require(len(boxes) == 24 and 2 * R * R >= 1 and H < B11, "fixed scalar/24-cell premises")
    upper, lower = [], []
    for a, b, c, d in boxes:
        tick(deadline)
        for value in (a, b, c, d):
            finite.checked(value)
        require(
            Q(1, 2) <= a <= b <= U - Q(1, 2) and Q(1, 2) <= c <= d <= U - Q(1, 2),
            "centre box outside necessary unit-square wall bounds",
        )
        mx, my = min(U / 2, b, U - a), min(U / 2, d, U - c)
        rx, ry = min(R, my), min(R, mx)
        up = (
            max(Q(0), 2 * a - U, a - rx),
            min(U, 2 * b, b + rx),
            max(Q(0), 2 * c - U, c - ry),
            min(U, 2 * d, d + ry),
        )
        lo = (a - Q(1, 2), b + Q(1, 2), c - Q(1, 2), d + Q(1, 2))
        original = (max(Q(0), a - R), min(U, b + R), max(Q(0), c - R), min(U, d + R))
        require(
            all(lo[i] >= up[i] >= original[i] for i in (0, 2))
            and all(lo[i] <= up[i] <= original[i] for i in (1, 3))
            and up[0] <= up[1]
            and up[2] <= up[3],
            "lower/upper/original envelope sandwich differs",
        )
        upper.append(tuple(finite.checked(v) for v in up))
        lower.append(tuple(finite.checked(v) for v in lo))
    return upper, lower


def read_role(
    role: str, document: dict[str, Any], held: dict[Path, tuple[bytes, int]], deadline: float
) -> Any:
    tick(deadline)
    require(
        type(document[role]) is str
        and type(document[role + "_sha256"]) is str
        and re.fullmatch(r"[0-9a-f]{64}", document[role + "_sha256"]) is not None,
        "prior role path/byte identity required",
    )
    path = Path(document[role])
    path = path if path.is_absolute() else old.REPO / path
    ceiling = INPUT_LIMIT if role.endswith("descriptor") else OUTPUT_LIMIT
    raw, value = finite.read_json(path, ceiling)
    require(type(value) is dict, "typed prior role record required")
    require(
        hashlib.sha256(raw).hexdigest() == document[role + "_sha256"], "prior role bytes differ"
    )
    require(path not in held or held[path][0] == raw, "conflicting prior role aliases")
    held[path] = (raw, min(ceiling, held.get(path, (raw, ceiling))[1]))
    return value


def intake(document: Any, deadline: float) -> tuple[Any, ...]:
    require(
        type(document) is dict
        and document.get("schema") == CONTEXT_SCHEMA
        and set(document) == {"schema", *(k for r in ROLES for k in (r, r + "_sha256"))},
        "representation descriptor differs",
    )
    held: dict[Path, tuple[bytes, int]] = {}
    values = {r: read_role(r, document, held, deadline) for r in ROLES}
    prior, replay = values["prior_certificate"], values["prior_replay"]
    require(
        prior.get("schema") == old.SCHEMA
        and prior.get("status") == "criterion_missed"
        and prior.get("criterion_met") is False
        and prior.get("accepted_inputs") == values["prior_descriptor"]
        and replay.get("verification_passed") is True
        and payload(prior) == payload(replay)
        and prior.get("states_accounted") == 95
        and prior.get("windows_per_state") == 576
        and prior.get("state_window_counts_accounted") == 54720
        and prior.get("obstructed_masks") == []
        and all(prior.get(k) is False for k in old.scope()),
        "accepted complete envelope miss/fresh premise differs",
    )
    boxes, names, roster, original_held = old.intake(values["prior_descriptor"], deadline)
    require(
        type(prior.get("states")) is list
        and len(prior["states"]) == 95
        and all(type(r) is dict for r in prior["states"])
        and [r.get("mask") for r in prior["states"]] == [r["mask"] for r in roster]
        and all(
            r.get("ordinary_assignment_obstruction") is False
            and r.get("windows_accounted") == 576
            and len(r.get("window_counts", [])) == 576
            and r.get("maximum_full_envelope_count") == max(r["window_counts"])
            and all(type(n) is int and 0 <= n <= 10 for n in r["window_counts"])
            and r.get("witness") is None
            for r in prior["states"]
        ),
        "complete inherited negative outcome roster differs",
    )
    for path, raw in original_held.items():
        require(
            path not in held or held[path][0] == raw, "conflicting transitive premise aliases"
        )
        held[path] = (raw, min(INPUT_LIMIT, held.get(path, (raw, INPUT_LIMIT))[1]))
    partition = Path(values["prior_descriptor"]["partition"])
    partition = partition if partition.is_absolute() else old.REPO / partition
    require(partition in held, "accepted partition not held")
    # old.intake freshly joined every named partition row before this adapter.
    part = json.loads(held[partition][0])
    endpoints = [r for r in part["orbits"] if r["distance"] == 0]
    require(len(endpoints) == 1, "one accepted endpoint representative required")
    endpoint = endpoints[0]
    old.named_row(
        endpoint,
        names,
        values["prior_descriptor"]["d4"],
        old.images(endpoint["mask"], values["prior_descriptor"]["d4"]),
    )
    return boxes, names, roster, endpoint["mask"], held


def lower_scan(
    mask: int, windows: list[dict[str, Any]], names: list[str], deadline: float
) -> dict[str, Any]:
    result = old.scan_state(mask, windows, names, deadline)
    result["optimistic_lower_window_possible"] = result.pop("ordinary_assignment_obstruction")
    result["nonproof_window_witness"] = result.pop("witness")
    result["ordinary_assignment_exclusion_proved"] = False
    return result


def construct(
    boxes: list[Box],
    names: list[str],
    roster: list[dict[str, Any]],
    endpoint: int,
    *,
    deadline: float,
) -> dict[str, Any]:
    require(len(roster) == 95, "complete95 roster required")
    upper, lower = representations(boxes, deadline)
    uw, lw = (
        old.window_roster(upper, names, deadline),
        old.window_roster(lower, names, deadline),
    )
    positives, lower_possible, states = [], [], []
    for row in roster:
        u = old.scan_state(row["mask"], uw, names, deadline)
        lower_result = lower_scan(row["mask"], lw, names, deadline)
        require(
            lower_result["maximum_full_envelope_count"] >= u["maximum_full_envelope_count"],
            "optimistic lower count below upper count",
        )
        if u["witness"] is not None:
            old.verify_witness(row["mask"], upper, names, u["witness"])
            positives.append(row["mask"])
        if lower_result["optimistic_lower_window_possible"]:
            lower_possible.append(row["mask"])
        states.append({"mask": row["mask"], "upper": u, "lower": lower_result})
    calibration = old.scan_state(endpoint, uw, names, deadline)
    require(
        calibration["maximum_full_envelope_count"] <= 10,
        "accepted endpoint upper-envelope positive control fails",
    )
    killed = not lower_possible
    require(
        not (positives and killed), "contradictory upper obstruction/lower architecture kill"
    )
    tick(deadline)
    return {
        "status": "ordinary_assignment_obstructions"
        if positives
        else "independent_aabb_architecture_killed"
        if killed
        else "criterion_missed",
        "criterion_met": bool(positives or killed),
        **scope(obstruction=bool(positives), killed=killed),
        "states_accounted": 95,
        "windows_per_representation": 576,
        "state_window_counts_accounted": 109440,
        "states": states,
        "upper_obstructed_masks": positives,
        "lower_possible_masks": lower_possible,
        "upper_envelopes": [list(map(str, b)) for b in upper],
        "lower_envelopes": [list(map(str, b)) for b in lower],
        "upper_window_roster": uw,
        "lower_window_roster": lw,
        "endpoint_upper_calibration": calibration,
        "endpoint_upper_window_counts_accounted": 576,
        "lower_endpoint_diagnostic_performed": False,
        "architecture_scope": (
            "Original U and entire original cells; independent all-pose axis-aligned enclosing "
            "boxes with axis-aligned side31/8 windows. No smaller V, subdivisions, relational "
            "constraints, rotated windows or different window side."
        ),
    }


def generate(document: Any, *, deadline: float) -> dict[str, Any]:
    frozen = finite.canonical(document)
    boxes, names, roster, endpoint, held = intake(document, deadline)
    result = construct(boxes, names, roster, endpoint, deadline=deadline)
    for path, (raw, ceiling) in held.items():
        tick(deadline)
        with path.open("rb") as stream:
            require(
                stream.read(ceiling + 1) == raw, "accepted representation premise bytes changed"
            )
    require(finite.canonical(document) == frozen, "representation descriptor changed")
    tick(deadline)
    return {
        "schema": SCHEMA,
        **result,
        "accepted_inputs": copy.deepcopy(document),
        "verification_passed": False,
        "assurance": {
            "accepted304_proof_inherited": True,
            "old_windows_replayed": False,
            "old_intake_freshly_rejoined_once": True,
            "n11_T061_proof_inherited": True,
            "n11_T061_proof_replayed": False,
            "whole_cell_lower_bounds_are_not_rotated_square_enclosures": True,
            "exact_envelope_sandwich_checked": True,
            "composition": "sole Astra hand derivation and fresh finite arithmetic",
        },
        "limits": {
            "role_json_bytes": INPUT_LIMIT,
            "prior_receipt_bytes": OUTPUT_LIMIT,
            "output_bytes": OUTPUT_LIMIT,
            "normalized_geometry_bits": finite.BIT_LIMIT,
        },
    }


def check(document: Any, certificate: Any, *, deadline: float) -> dict[str, Any]:
    require(type(certificate) is dict, "typed representation certificate required")
    result = generate(document, deadline=deadline)
    require(
        payload(certificate) == payload(result), "fresh representation reconstruction differs"
    )
    return result | {"verification_passed": True}


def failure(exc: Exception) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "status": "incomplete" if isinstance(exc, finite.IncompleteError) else "refused",
        "criterion_met": False,
        "verification_passed": False,
        **scope(),
        "error": str(exc),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--descriptor", type=Path, required=True)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--max-seconds", type=float, default=60)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0:
        parser.error("max-seconds must be finite and positive")
    deadline = time.monotonic() + args.max_seconds
    try:
        require(
            not any(
                n == p or n.startswith(p + ".") for n in sys.modules for p in finite.FORBIDDEN
            ),
            "producer/kernel/root import in representation checker",
        )
        raw, document = finite.read_json(args.descriptor, INPUT_LIMIT)
        if args.certificate:
            saved, certificate = finite.read_json(args.certificate, OUTPUT_LIMIT)
            result = check(document, certificate, deadline=deadline)
            require(
                saved == finite.read_json(args.certificate, OUTPUT_LIMIT)[0],
                "certificate bytes changed",
            )
        else:
            result = generate(document, deadline=deadline)
        require(
            raw == finite.read_json(args.descriptor, INPUT_LIMIT)[0], "descriptor bytes changed"
        )
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
        result = failure(finite.IncompleteError("representation output byte or wall ceiling"))
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        stream.write(text)
    return (
        0
        if result["status"]
        in (
            "ordinary_assignment_obstructions",
            "independent_aabb_architecture_killed",
            "criterion_missed",
        )
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
