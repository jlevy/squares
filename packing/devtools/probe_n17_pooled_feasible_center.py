"""A deterministic fixed-angle search satisfying walls and strict-owned strips.

Accepted union and previous witness receipts are explicit premises. This finite
construction proves only consistency of one square with owned-point facts.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import math
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from devtools import probe_n17_pooled_relaxation_witness as witness
from devtools.provenance import provenance
from sqpack import retained_json

cases, finite, standing, union = witness.cases, witness.finite, witness.standing, witness.union
require, tick, checked = witness.require, witness.tick, witness.checked
IncompleteError = witness.IncompleteError
type Point = tuple[Q, Q]
SCHEMA = "n17-pooled-feasible-center/v1"
DESCRIPTOR_SCHEMA = "n17-pooled-feasible-center-context/v1"
TAU, MARGIN = witness.TAU, Q(1, 2**20)
JSON_LIMIT, OUTPUT_LIMIT = 10 << 20, 64 << 20
POOL_LIMIT, CENTER_LIMIT, REGION_LIMIT, PIECE_LIMIT, PAIR_LIMIT = 128, 256, 132, 256, 8192
INPUTS = (*witness.INPUTS, "witness_descriptor", "witness_certificate", "witness_replay")


def intake(
    document: dict[str, Any], held: dict[Path, bytes], deadline: float
) -> dict[str, Any]:
    require(
        set(document)
        == {"schema", *(key for name in INPUTS for key in (name, name + "_sha256"))}
        and document["schema"] == DESCRIPTOR_SCHEMA,
        "feasible-center descriptor fields/schema",
    )
    values = {}
    for name in INPUTS:
        path = finite.retained_path(document[name])
        raw, value = finite.read_json(path, JSON_LIMIT)
        require(
            path not in held and hashlib.sha256(raw).hexdigest() == document[name + "_sha256"],
            "accepted input path/byte identity differs",
        )
        tick(deadline)
        held[path] = raw
        values[name] = value
    source, certificate, replay = (values[name] for name in witness.INPUTS)
    witness.union_contract(source, certificate, replay)
    previous_descriptor = values["witness_descriptor"]
    require(
        previous_descriptor
        == {
            "schema": witness.DESCRIPTOR_SCHEMA,
            **{
                key: document[key]
                for name in witness.INPUTS
                for key in (name, name + "_sha256")
            },
        },
        "previous witness union identities differ",
    )
    previous, fresh = values["witness_certificate"], values["witness_replay"]
    require(
        fresh.get("verification_passed") is True
        and witness.payload(previous) == witness.payload(fresh),
        "previous witness fresh payload differs",
    )
    require(
        previous["schema"] == witness.SCHEMA
        and previous["status"] == "criterion_missed"
        and previous["applicable"] is True
        and previous["criterion_met"] is False
        and previous["container_passed"] is False
        and previous["all_owner0_strict"] is True
        and previous["all_foreign_open_avoidance"] is True,
        "frozen containment-only witness miss required",
    )
    require(
        previous["accepted_union_inputs"] == previous_descriptor
        and previous["tau"] == str(TAU)
        and previous["guard"] == certificate["guard"]
        and previous["container"] == certificate["container"]
        and previous["mask"] == certificate["mask"]
        and previous["parent"] == certificate["custody"]["parent"],
        "previous witness parent/domain join differs",
    )
    return certificate


def target(domain: list[Point], own: list[Point], deadline: float) -> list[Point]:
    """Necessary fixed-angle walls, then sufficient strict-owned margin strips."""
    c, s = finite.trig(TAU)
    reach = checked(checked(c + s) / 2)
    lo, hi = checked(cases.OFFSET + reach), checked(cases.U - cases.OFFSET - reach)
    result = domain
    for a, b, rhs in (
        (Q(-1), Q(0), -lo),
        (Q(1), Q(0), hi),
        (Q(0), Q(-1), -lo),
        (Q(0), Q(1), hi),
    ):
        result = cases.clip(result, a, b, rhs, CENTER_LIMIT, deadline)
    for point in own:
        for nx, ny in ((c, s), (-s, c)):
            for sign in (-1, 1):
                tick(deadline)
                normal = (checked(sign * nx), checked(sign * ny))
                rhs = checked(checked(Q(1, 2) - MARGIN) + finite.dot(normal, point))
                result = cases.clip(result, *normal, rhs, CENTER_LIMIT, deadline)
    tick(deadline)
    return result


def foreign_regions(
    pools: dict[int, list[Point]], deadline: float
) -> tuple[dict[int, list[Point]], int]:
    shape = witness.square((Q(0), Q(0)), deadline)
    count, regions = 0, {}
    for owner in sorted(pools):
        if owner == 0:
            continue
        count += len(pools[owner]) * len(shape)
        if count > PAIR_LIMIT:
            raise IncompleteError("feasible-center Minkowski pair ceiling")
        points = []
        for p in pools[owner]:
            for q in shape:
                tick(deadline)
                points.append(cases.subtract(p, q))
        regions[owner] = cases.bounded_hull(points, REGION_LIMIT, deadline)
    return regions, count


def construct(certificate: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    rows: list[dict[str, Any]] = certificate["rows"]
    require(
        [r["row_index"] for r in rows] == [25, 26, 27]
        and rows[1]["interval"] == list(map(str, cases.INTERVAL)),
        "complete guard row/interval roster",
    )
    raw_pieces: list[dict[str, Any]] = rows[1]["pieces"]
    require(
        [p["piece_index"] for p in raw_pieces] == list(range(len(raw_pieces))),
        "all retained row26 pieces/order required",
    )
    if len(raw_pieces) > PIECE_LIMIT:
        raise IncompleteError("feasible-center piece ceiling")
    pool = certificate["custody"]["proof_pool"]
    pools = {
        int(o): witness.polygon(raw, POOL_LIMIT, deadline) for o, raw in pool["pools"].items()
    }
    selected = witness.polygon(pool["selected_five"], 5, deadline)
    require(len(selected) == 5, "five conditional finite points required")
    own = cases.bounded_hull(pools[0] + selected, POOL_LIMIT, deadline)
    regions, pair_count = foreign_regions(pools, deadline)
    parts = []
    chosen = None
    pose_result = None
    for piece in raw_pieces:
        tick(deadline)
        domain = witness.polygon(piece["domain"], CENTER_LIMIT, deadline)
        clipped = target(domain, own, deadline)
        record: dict[str, Any] = {
            "piece_index": piece["piece_index"],
            "target": finite.serial(clipped),
        }
        if not clipped:
            record.update(status="empty_target", covered=None, uncovered_probe=None)
            parts.append(record)
            continue
        if len(clipped) >= 3:
            covered, probe = witness.sweep(clipped, list(regions.values()), deadline)
        else:
            edges = sum(len(cases.edges(p)) for p in [clipped, *regions.values()])
            if edges > union.EDGE_LIMIT or edges * (edges - 1) // 2 > union.EDGE_PAIR_LIMIT:
                raise IncompleteError("feasible-center degenerate edge/pair ceiling")
            tick(deadline)
            covered, probe = standing.degenerate_covered(clipped, list(regions.values())), None
            tick(deadline)
        record.update(
            status="covered" if covered else "candidate",
            covered=covered,
            uncovered_probe=str(probe) if probe is not None else None,
        )
        parts.append(record)
        if covered:
            continue
        selection = witness.choose_center(
            clipped, list(regions.values()), record["uncovered_probe"], deadline
        )
        center = cast(Point, tuple(finite.rational(v) for v in selection["center"]))
        pose_result = witness.pose(center, pools, selected, deadline)
        require(
            pose_result["criterion_met"] is True,
            "constructed candidate fails independent pose calibration",
        )
        chosen = {"piece_index": piece["piece_index"], "selection": selection}
        break
    tick(deadline)
    return {
        "pieces": parts,
        "unstarted_piece_indices": [p["piece_index"] for p in raw_pieces[len(parts) :]],
        "foreign_regions": {str(o): finite.serial(p) for o, p in regions.items()},
        "closed_square_zero_centered": finite.serial(witness.square((Q(0), Q(0)), deadline)),
        "generated_pairs": pair_count,
        "conditional_owner0_hull": finite.serial(own),
        "chosen": chosen,
        "pose": pose_result,
        "criterion_met": chosen is not None,
        "status": "owned_point_relaxation_witness"
        if chosen is not None
        else "criterion_missed",
        "miss_proves_fixed_angle_infeasibility": False,
        "closed_obstacles_may_miss_boundary_contacts": True,
    }


def generate(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    frozen = finite.canonical(document)
    held: dict[Path, bytes] = {}
    certificate = intake(document, held, deadline)
    result = construct(certificate, deadline=deadline)
    for path, raw in held.items():
        require(
            finite.read_json(path, JSON_LIMIT)[0] == raw,
            "accepted inputs changed during construction",
        )
        tick(deadline)
    require(finite.canonical(document) == frozen, "feasible-center descriptor changed")
    return {
        "schema": SCHEMA,
        "tau": str(TAU),
        "margin": str(MARGIN),
        "guard": copy.deepcopy(cases.GUARD),
        "container": copy.deepcopy(certificate["container"]),
        "mask": copy.deepcopy(certificate["mask"]),
        "accepted_inputs": copy.deepcopy(document),
        "parent": copy.deepcopy(certificate["custody"]["parent"]),
        "constants": {
            "input_bytes_each": JSON_LIMIT,
            "output_bytes": OUTPUT_LIMIT,
            "normalized_rational_bits": finite.BIT_LIMIT,
            "pool_vertices": POOL_LIMIT,
            "target_vertices": CENTER_LIMIT,
            "foreign_region_vertices": REGION_LIMIT,
            "pieces": PIECE_LIMIT,
            "Minkowski_pairs": PAIR_LIMIT,
            "polygon_edges": union.EDGE_LIMIT,
            "prospective_edge_pairs": union.EDGE_PAIR_LIMIT,
        },
        "construction_assurance": (
            "closed obstacles and fixed owned-point margin; a miss is only recipe failure"
        ),
        "sweep_resource_assurance": {
            "unreduced_integer_product_bit_cap": False,
            "required": "outer wall and sampled current RSS per live owned process",
        },
        "hand_implication": (
            "Astra hand derivation; not independently mathematically reviewed "
            "or machine-checked"
        ),
        **witness.scope(),
        **result,
    }


def check(
    document: dict[str, Any], certificate: dict[str, Any], *, deadline: float
) -> dict[str, Any]:
    expected = witness.payload(certificate)
    require(
        expected == generate(document, deadline=deadline),
        "fresh feasible-center reconstruction differs",
    )
    return copy.deepcopy(expected) | {"verification_passed": True}


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
                name == prefix or name.startswith(prefix + ".")
                for name in sys.modules
                for prefix in (*finite.FORBIDDEN, "devtools.produce_n17_conditional_owned_hull")
            ),
            "producer/kernel/root import in feasible-center checker",
        )
        raw, document = finite.read_json(args.descriptor)
        if args.certificate:
            saved, certificate = finite.read_json(args.certificate, OUTPUT_LIMIT)
            result = check(document, certificate, deadline=deadline)
            require(
                finite.read_json(args.certificate, OUTPUT_LIMIT)[0] == saved,
                "feasible-center certificate bytes changed",
            )
        else:
            result = generate(document, deadline=deadline)
        require(
            finite.read_json(args.descriptor)[0] == raw,
            "feasible-center descriptor bytes changed",
        )
    except IncompleteError as exc:
        result = {
            "schema": SCHEMA,
            "status": "incomplete",
            "error": str(exc),
            "criterion_met": False,
        }
    except (
        ValueError,
        KeyError,
        TypeError,
        OSError,
        EOFError,
        standing.VerificationError,
    ) as exc:
        result = {
            "schema": SCHEMA,
            "status": "refused",
            "error": str(exc),
            "criterion_met": False,
        }
    result.update(witness.scope())
    result.update(
        provenance=provenance(
            Path(__file__),
            Path(witness.__file__),
            Path(cast(str, union.__file__)),
            Path(cast(str, cases.__file__)),
            Path(cast(str, finite.__file__)),
            Path(cases.conditional.__file__),
            Path(cast(str, standing.__file__)),
        ),
        invocation={
            "argv": argv if argv is not None else sys.argv[1:],
            "executable": sys.executable,
        },
    )
    text = retained_json.dumps(result, sort_keys=True)
    if len(text.encode()) > OUTPUT_LIMIT or time.monotonic() >= deadline:
        result = {
            "schema": SCHEMA,
            "status": "incomplete",
            "error": "feasible-center output byte or wall ceiling",
            "criterion_met": False,
            **witness.scope(),
        }
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)
    return (
        0 if result["status"] in ("owned_point_relaxation_witness", "criterion_missed") else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
