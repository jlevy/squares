"""Exact full-square SAT minima on complete accepted n17 partner domains.

The accepted parent and matched witness are inherited premises. Fresh finite
reconstruction checks every row, vertex and closed angular subinterval.
"""

from __future__ import annotations

import argparse
import copy
import math
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from devtools import check_n17_partner_pose_coupling as parent
from devtools.provenance import provenance
from sqpack import retained_json

finite, cases, standing = parent.finite, parent.cases, parent.standing
require, tick, checked = parent.require, parent.tick, parent.checked
IncompleteError = parent.IncompleteError
type Point = tuple[Q, Q]
type Polynomial = tuple[Q, Q, Q]
SCHEMA = "n17-full-square-partner-coupling/v1"
DESCRIPTOR_SCHEMA = "n17-full-square-partner-coupling-context/v1"
TAU = Q(53, 128)
C0, S0 = Q(13575, 19193), Q(13568, 19193)
L = Q(2838, 125)
QUADRATIC_LIMIT = 8000000
OUTPUT_LIMIT = 64 << 20
AXES = ("owner_u", "owner_v", "partner_u", "partner_v")


def value_at(coefficients: Polynomial, t: Q) -> Q:
    a, b, c = coefficients
    return checked(a + checked(t * checked(b + checked(c * t))))


def minimum(coefficients: Polynomial, lo: Q, hi: Q) -> tuple[Q, Q]:
    """Return the exact minimum and least rational minimizer on a closed arc."""
    require(0 <= lo <= hi <= 1, "closed quadratic interval differs")
    candidates = [(value_at(coefficients, t), t) for t in (lo, hi)]
    if coefficients[2] > 0:
        stationary = checked(-coefficients[1] / checked(2 * coefficients[2]))
        if lo < stationary < hi:
            candidates.append((value_at(coefficients, stationary), stationary))
    return min(candidates)


def split(lo: Q, hi: Q) -> list[tuple[Q, Q, int]]:
    require(0 <= lo <= hi <= 1, "full-square row interval differs")
    if hi <= TAU:
        return [(lo, hi, -1)]
    if lo >= TAU:
        return [(lo, hi, 1)]
    return [(lo, TAU, -1), (TAU, hi, 1)]


def coefficients(displacement: Point, sigma: int, axis: str, eta: int) -> Polynomial:
    require(sigma in (-1, 1) and eta in (-1, 1), "SAT projection sign differs")
    require(axis in AXES, "SAT projection axis differs")
    dx, dy = displacement
    a, b, c = Q(1) + C0 - sigma * S0, 2 * S0 + 2 * sigma * C0, Q(1) - C0 + sigma * S0
    if axis in ("owner_u", "owner_v"):
        z = finite.dot(displacement, (C0, S0) if axis == "owner_u" else (-S0, C0))
        return checked(a - 2 * eta * z), checked(b), checked(c - 2 * eta * z)
    if axis == "partner_u":
        return checked(a - 2 * eta * dx), checked(b - 4 * eta * dy), checked(c + 2 * eta * dx)
    return checked(a - 2 * eta * dy), checked(b + 4 * eta * dx), checked(c + 2 * eta * dy)


def row_domain(row: dict[str, Any], counter: list[int], deadline: float) -> dict[str, Any]:
    """Use the identical individually clipped domains without an eroded core."""
    lo, hi = map(finite.rational, row["interval"])
    if len(row["residual_polygons"]) > parent.ROW_PIECE_LIMIT:
        raise IncompleteError("full-square per-row piece ceiling")
    pieces = []
    for index, raw in enumerate(row["residual_polygons"]):
        points = parent.parse_polygon(raw, counter, deadline)
        points = parent.wall_clip(points, lo, hi, deadline)
        require(
            all(0 <= x <= cases.U and 0 <= y <= cases.U for x, y in points),
            "centre outside outer box",
        )
        pieces.append({"piece_index": index, "necessary_domain": finite.serial(points)})
    vertices = [
        (finite.rational(x), finite.rational(y))
        for piece in pieces
        for x, y in piece["necessary_domain"]
    ]
    return {
        "reference": copy.deepcopy(row["reference"]),
        "interval": list(row["interval"]),
        "pieces": pieces,
        "domain": cases.bounded_hull(vertices, parent.DOMAIN_LIMIT, deadline),
    }


def witness_key(witness: dict[str, Any]) -> tuple[Any, ...]:
    return (
        finite.rational(witness["minimum"]),
        finite.rational(witness["minimizer"]),
        witness["row_index"],
        witness["vertex_index"],
        witness["subinterval_index"],
        AXES.index(witness["axis"]),
        witness["eta"],
    )


def partner_minimum(
    rows: list[dict[str, Any]], centre: Point, work: list[int], deadline: float
) -> dict[str, Any]:
    best = None
    records = []
    start = work[0]
    for row_index, row in enumerate(rows):
        tick(deadline)
        row_best = None
        lo, hi = map(finite.rational, row["interval"])
        for sub_index, (a, b, sigma) in enumerate(split(lo, hi)):
            for vertex_index, vertex in enumerate(row["domain"]):
                displacement = cases.subtract(vertex, centre)
                for axis in AXES:
                    for eta in (-1, 1):
                        tick(deadline)
                        work[0] += 1
                        if work[0] > QUADRATIC_LIMIT:
                            raise IncompleteError("full-square quadratic minimization ceiling")
                        polynomial = coefficients(displacement, sigma, axis, eta)
                        value, t = minimum(polynomial, a, b)
                        item = {
                            "row_index": row_index,
                            "reference": copy.deepcopy(row["reference"]),
                            "vertex_index": vertex_index,
                            "vertex": list(map(str, vertex)),
                            "subinterval_index": sub_index,
                            "subinterval": [str(a), str(b)],
                            "sigma": sigma,
                            "axis": axis,
                            "eta": eta,
                            "coefficients": list(map(str, polynomial)),
                            "minimum": str(value),
                            "minimizer": str(t),
                        }
                        if row_best is None or witness_key(item) < witness_key(row_best):
                            row_best = item
                        if best is None or witness_key(item) < witness_key(best):
                            best = item
        records.append(
            {
                "row_index": row_index,
                "reference": copy.deepcopy(row["reference"]),
                "minimum_witness": row_best,
            }
        )
    require(best is not None, "endpoint calibration all-empty partner")
    best = cast(dict[str, Any], best)
    return {
        "minimum": best["minimum"],
        "minimum_witness": best,
        "strict_collision": finite.rational(best["minimum"]) > 0,
        "quadratic_minimizations": work[0] - start,
        "complete_rows_checked": len(rows),
        "row_minima": records,
    }


def lift(value: Q, centre: Point) -> dict[str, Any]:
    require(
        value > 0 and L == 4 * cases.U + 4,
        "positive full-square margin and lift constant required",
    )
    h = checked(min(Q(1, 128), checked(value / checked(8 * L))))
    lower = checked(checked(value / 4) - checked(L * h))
    require(h > 0 and lower >= value / 8 > 0, "full-square regional margin fails")
    require(Q(13, 32) <= TAU - h < TAU + h <= Q(27, 64), "regional angle guard differs")
    return {
        "half_width": str(h),
        "centre_box": [[str(checked(x - h)), str(checked(x + h))] for x in centre],
        "angle_interval": [str(TAU - h), str(TAU + h)],
        "M": str(value),
        "L": str(L),
        "gap_lower_bound": str(lower),
        "required_gap": str(checked(value / 8)),
        "positive_coordinate_widths": True,
        "endpoint_family_disjoint": True,
        "excluded_domain": (
            "declared closed position-angle box intersected with accepted parent "
            "and physical container constraints"
        ),
    }


def exact_wall_at_minimizer(witness: dict[str, Any]) -> dict[str, Any]:
    """Secondary feasibility diagnostic; it never changes the SAT criterion."""
    t = finite.rational(witness["minimizer"])
    vertex = tuple(map(finite.rational, witness["vertex"]))
    c, s = finite.trig(t)
    reach = checked((c + s) / 2)
    lower = checked(cases.OFFSET + reach)
    upper = checked(cases.U - cases.OFFSET - reach)
    margins = [
        checked(vertex[0] - lower),
        checked(upper - vertex[0]),
        checked(vertex[1] - lower),
        checked(upper - vertex[1]),
    ]
    return {
        "exact_numeric_wall_contained": all(value >= 0 for value in margins),
        "wall_interval": [str(lower), str(upper)],
        "wall_margins": list(map(str, margins)),
        "secondary_only": True,
        "seventeen_square_packing_proved": False,
    }


def construct(
    cells: dict[str, Any],
    roles: dict[str, int],
    roster: Any,
    centre: Point,
    *,
    deadline: float,
    reference_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    require(
        set(roles) == set(map(str, range(1, 18)))
        and roles["1"] == 0
        and roles["6"] == 12
        and len(set(roles.values())) == 17
        and all(type(o) is int and 0 <= o < 24 for o in roles.values())
        and set(cells) == set(map(str, roles.values())),
        "complete frozen label/owner/cell roster differs",
    )
    require(all(0 <= x <= cases.U for x in centre), "fixed centre outside outer box")
    require(finite.trig(TAU) == (C0, S0), "fixed exact owner axes differ")
    counter = [0]
    domains = {}
    for owner in sorted(roles.values()):
        raw = cells[str(owner)]
        parent.closed_rows(raw, owner, 32 if owner == 12 else 64, reference_context)
        domains[owner] = [row_domain(row, counter, deadline) for row in raw]
        require(
            any(row["domain"] for row in domains[owner]),
            "endpoint calibration all-empty partner",
        )
    endpoint = parent.endpoint_control(roster, domains, roles, deadline)
    point_pieces = []
    for raw in cells["0"]:
        lo, hi = map(finite.rational, raw["interval"])
        if lo <= TAU <= hi:
            point_pieces.extend(
                parent.wall_clip(parent.parse_polygon(p, counter, deadline), TAU, TAU, deadline)
                for p in raw["residual_polygons"]
            )
    require(
        any(cases.contains(piece, centre) for piece in point_pieces),
        "fixed witness absent from individual accepted owner0 piece",
    )
    work = [0]
    partners = {
        o: partner_minimum(rows, centre, work, deadline)
        for o, rows in domains.items()
        if o != 0
    }
    for record in partners.values():
        if finite.rational(record["minimum"]) <= 0:
            record["negative_witness_exact_wall"] = exact_wall_at_minimizer(
                record["minimum_witness"]
            )
    positive = [o for o, record in partners.items() if record["strict_collision"]]
    selected = min(positive) if positive else None
    region = (
        lift(finite.rational(partners[selected]["minimum"]), centre)
        if selected is not None
        else None
    )
    tick(deadline)
    return {
        "status": "closed_region_exclusion" if region else "criterion_missed",
        "criterion_met": region is not None,
        "closed_region_exclusion_proved": region is not None,
        "fixed_witness_excluded": bool(positive),
        "selected_partner": selected,
        "positive_partners": positive,
        "partners": {str(o): record for o, record in partners.items()},
        "region": region,
        "endpoint_control": {
            "all17_retained": True,
            "witnesses": endpoint,
            "label1_charts_disjoint_from_region": True,
        },
        "all_rows_checked": sum(len(rows) for rows in domains.values()),
        "foreign_rows_checked": sum(len(rows) for o, rows in domains.items() if o != 0),
        "quadratic_minimizations": work[0],
        "input_vertices_parsed": counter[0],
        "rows": {
            str(o): [{**row, "domain": finite.serial(row["domain"])} for row in rows]
            for o, rows in domains.items()
        },
    }


def constants() -> dict[str, Any]:
    inherited = parent.constants()
    return {
        **{
            k: inherited[k]
            for k in (
                "geometry_bits",
                "endpoint_input_bits",
                "endpoint_arithmetic_bits",
                "row_pieces",
                "input_piece_vertices",
                "clipped_piece_vertices",
                "used_input_vertices",
                "row_domain_vertices",
                "input_json_bytes_each",
                "output_bytes",
                "seed_bytes",
                "compressed_node_bytes",
                "decoded_node_bytes",
                "final_slice_bytes",
            )
        },
        "tau": str(TAU),
        "c0": str(C0),
        "s0": str(S0),
        "L": str(L),
        "maximum_half_width": "1/128",
        "quadratic_minimizations": QUADRATIC_LIMIT,
        "minimum_witness_tie_order": [
            "minimum",
            "minimizer",
            "row_index",
            "vertex_index",
            "subinterval_index",
            "axis_order",
            "eta",
        ],
    }


def generate(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    fields = {k for name in parent.INPUTS for k in (name, name + "_sha256")}
    require(
        type(document) is dict
        and set(document) == {"schema", *fields}
        and document["schema"] == DESCRIPTOR_SCHEMA,
        "full-square descriptor fields/schema differs",
    )
    require(
        all(type(document[k]) is str for k in fields),
        "full-square descriptor paths and digests must be strings",
    )
    frozen = finite.canonical(document)
    adapted = document | {"schema": parent.DESCRIPTOR_SCHEMA}
    held: dict[Path, tuple[str, int]] = {}
    final, custody, roster, centre = parent.intake(adapted, held, deadline)
    gate = finite.read_json(
        finite.retained_path(document["parent_descriptor"]), parent.JSON_LIMIT
    )[1]
    result = construct(
        final["cells"],
        gate["label_to_owner"],
        roster,
        centre,
        deadline=deadline,
        reference_context=custody["typed_reference_context"],
    )
    for path, (expected, ceiling) in held.items():
        require(
            finite.digest(path, ceiling, deadline) == expected, "full-square inputs changed"
        )
    require(finite.canonical(document) == frozen, "full-square descriptor changed")
    tick(deadline)
    return {
        "schema": SCHEMA,
        "accepted_inputs": dict(document),
        "container": standing.CenteredContainer(cases.U, cases.V).record(),
        "parent_custody": {
            k: copy.deepcopy(custody[k])
            for k in (
                "h290_receipt",
                "h290_receipt_sha256",
                "seed_sha256",
                "node_sha256",
                "compressed_sha256",
                "steps",
                "accepted_parent_premises",
                "typed_reference_context",
            )
        },
        "matched_owned_point_witness": {
            "centre": list(map(str, centre)),
            "tau": str(TAU),
            "freshly_checked": True,
        },
        "constants": constants(),
        "mathematical_assurance": (
            "finite exact quadratic reconstruction; SAT geometric composition and "
            "regional Lipschitz lift are sole-Astra hand implications, not independently "
            "mathematically reviewed or machine-formalized"
        ),
        "resource_assurance": {
            "unreduced_integer_product_bit_cap": False,
            "required": "outer wall ceiling and sampled current RSS per live owned process",
        },
        **parent.scope(),
        **result,
    }


def check(
    document: dict[str, Any], certificate: dict[str, Any], *, deadline: float
) -> dict[str, Any]:
    expected = parent.feasible.witness.payload(certificate)
    require(
        expected == generate(document, deadline=deadline),
        "fresh full-square reconstruction differs",
    )
    tick(deadline)
    return copy.deepcopy(expected) | {"verification_passed": True}


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
        require(
            not any(
                name == prefix or name.startswith(prefix + ".")
                for name in sys.modules
                for prefix in (*finite.FORBIDDEN, "devtools.produce_n17_conditional_owned_hull")
            ),
            "producer/kernel/root import in full-square checker",
        )
        raw, document = finite.read_json(args.descriptor, parent.JSON_LIMIT)
        if args.certificate:
            saved, certificate = finite.read_json(args.certificate, OUTPUT_LIMIT)
            result = check(document, certificate, deadline=deadline)
            require(
                finite.read_json(args.certificate, OUTPUT_LIMIT)[0] == saved,
                "full-square certificate bytes changed",
            )
        else:
            result = generate(document, deadline=deadline)
        require(
            finite.read_json(args.descriptor, parent.JSON_LIMIT)[0] == raw,
            "full-square descriptor bytes changed",
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
    result.update(parent.scope())
    result.update(
        provenance=provenance(
            Path(__file__),
            Path(parent.__file__),
            Path(cast(str, cases.__file__)),
            Path(cast(str, finite.__file__)),
            Path(cast(str, standing.__file__)),
            Path(parent.feasible.__file__),
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
            "error": "full-square output byte or wall ceiling",
            "criterion_met": False,
            **parent.scope(),
        }
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)
    return 0 if result["status"] in ("closed_region_exclusion", "criterion_missed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
