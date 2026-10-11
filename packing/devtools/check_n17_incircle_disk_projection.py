"""Exact disk-extreme diagnostic; no packing or ordinary admission."""

from __future__ import annotations

import argparse
import copy
import math
import sys
import time
from pathlib import Path
from typing import Any, cast

from devtools import check_n17_incircle_projection_redundancy as prior
from devtools.provenance import provenance
from sqpack import retained_json

finite, require, checked, tick, payload = (
    prior.finite,
    prior.require,
    prior.checked,
    prior.tick,
    prior.payload,
)
SCHEMA = "n17-incircle-disk-projection/v1"
CONTEXT_SCHEMA = "n17-incircle-disk-projection-context/v1"
OUTPUT_LIMIT = 1 << 20
NORM_LIMIT = prior.PAIR_LIMIT * prior.D_LIMIT


def disk_extremes(raw: Any, work: dict[str, int], deadline: float) -> dict[str, Any]:
    require(type(raw) is list and 0 < len(raw) <= prior.D_LIMIT, "difference vertex roster")
    points = []
    for item in raw:
        require(type(item) is list and len(item) == 2, "difference point pair")
        item = cast(list[Any], item)
        points.append((finite.rational(item[0]), finite.rational(item[1])))
    require(points == finite.hull(points), "canonical extreme difference hull")
    norms, inside = [], []
    for index, (x, y) in enumerate(points):
        tick(deadline)
        work["norms_checked"] += 1
        if work["norms_checked"] > NORM_LIMIT:
            raise finite.IncompleteError("disk norm work ceiling")
        value = checked(checked(x * x) + checked(y * y))
        norms.append(str(value))
        if value < 1:
            inside.append(index)
    return {
        "norm_squared": norms,
        "strict_disk_extreme_indices": inside,
        "disk_convexification_redundant": not inside,
        "whole_difference_in_open_disk": len(inside) == len(points),
    }


def generate(document: Any, *, deadline: float) -> dict[str, Any]:
    require(
        type(document) is dict and document.get("schema") == CONTEXT_SCHEMA,
        "disk descriptor schema",
    )
    adapted = document | {"schema": prior.prior.CONTEXT_SCHEMA}
    polygons, names, roster, _accepted, held = prior.prior.intake(adapted, deadline)
    frozen = finite.canonical(document)
    base = prior.construct(polygons, names, roster, deadline=deadline)
    require(
        base["complete_classification"] is True
        and base["states_accounted"] == 95
        and base["work"]["state_pairs_accounted"] == 12920,
        "full projection accounting",
    )
    work = {"norms_checked": 0}
    pairs, cuts, impossible = [], [], []
    for pair in base["pairs"]:
        result = disk_extremes(pair["difference_hull"], work, deadline)
        labelled = copy.deepcopy(pair)
        for key in ("convexified_pair_constraint_redundant", "strict_inside_extreme_indices"):
            if key in labelled:
                labelled["octagon_" + key] = labelled.pop(key)
        pairs.append(labelled | result)
        if not result["disk_convexification_redundant"]:
            cuts.append(pair["cells"])
        if result["whole_difference_in_open_disk"]:
            impossible.append(pair["cells"])
    states = copy.deepcopy(base.get("states", []))
    for state in states:
        state["octagon_shared_convexified_relaxation_witness_checked"] = state.pop(
            "shared_convexified_relaxation_witness_checked"
        )
        state["disk_shared_convexified_relaxation_witness_checked"] = not cuts
    base = copy.deepcopy(base)
    if "potential_cut_pairs" in base:
        base["octagon_potential_cut_pairs"] = base.pop("potential_cut_pairs")
    for p, raw in held.items():
        tick(deadline)
        with p.open("rb") as stream:
            require(stream.read(len(raw) + 1) == raw, "disk premise bytes changed")
    require(finite.canonical(document) == frozen, "disk descriptor changed")
    tick(deadline)
    return base | {
        "schema": SCHEMA,
        "status": "proper_disk_convexification_detected"
        if cuts
        else "all_disk_projection_constraints_redundant",
        "criterion_met": bool(cuts),
        "accepted_inputs": copy.deepcopy(document),
        "pairs": pairs,
        "states": states,
        "disk_cut_pairs": cuts,
        "ordinary_impossible_pair_candidates": impossible,
        "disk_work": work,
        "all95_shared_convexified_relaxations_redundant": not cuts,
        "octagon_all_redundant_diagnostic": base[
            "all95_shared_convexified_relaxations_redundant"
        ],
        "verification_passed": False,
        "accepted308_geometry_premises_inherited": True,
        "all_transitive_custody_checked_after_norm_stage": True,
        "ordinary_assignment_exclusion_proved": False,
        "census_admission_proved": False,
        "mathematical_assurance": (
            "sole Astra hand disk-extreme equivalence; independent confirmation false"
        ),
        "disk_limits": {"norms_checked": NORM_LIMIT, "output_bytes": OUTPUT_LIMIT},
    }


def check(document: Any, certificate: Any, *, deadline: float) -> dict[str, Any]:
    require(type(certificate) is dict, "disk certificate object")
    result = generate(document, deadline=deadline)
    require(payload(result) == payload(certificate), "fresh disk reconstruction differs")
    return result | {"verification_passed": True}


def failure(exc: Exception) -> dict[str, Any]:
    return prior.failure(exc) | {"schema": SCHEMA}


def main(argv: list[str] | None = None) -> int:
    # This is a separate CLI; the frozen projection CLI remains unchanged.
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
        raw, document = finite.read_json(args.descriptor, prior.prior.INPUT_LIMIT)
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
            raw == finite.read_json(args.descriptor, prior.prior.INPUT_LIMIT)[0],
            "descriptor changed",
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
        result = failure(finite.IncompleteError("disk output byte or wall ceiling"))
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        _ = stream.write(text)
    return int(result["status"] in ("incomplete", "refused"))


if __name__ == "__main__":
    raise SystemExit(main())
