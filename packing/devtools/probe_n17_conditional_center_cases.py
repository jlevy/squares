"""Exact finite center-case contradictions in an accepted closed-guard domain.

Accepted full replay is an explicit premise; this instrument does not replay
parent geometry or admit a mask. Fresh verification reconstructs every finite
polygon, coefficient-corner constraint and closed-hull intersection.
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
from typing import Any

from devtools import probe_n17_conditional_owned_hull as finite
from devtools import verify_n17_conditional_owned_hull as conditional
from devtools.provenance import provenance
from sqpack import retained_json

SCHEMA = "n17-conditional-center-cases/v1"
DESCRIPTOR_SCHEMA = "n17-conditional-center-cases-context/v1"
BASE_CHILD = "accepted_complete_conditional_child"
BASE_INITIAL = "accepted_conditional_initialization"
GUARD = copy.deepcopy(conditional.GUARD)
INTERVAL = (Q(13, 32), Q(27, 64))
U, V, MARGIN = finite.U, finite.V, finite.MARGIN
OFFSET = (U - V) / 2
JSON_LIMIT = 10 << 20
OUTPUT_LIMIT = 64 << 20
INPUT_VERTICES = 16384
CENTER_LIMIT = 256
INTERSECTION_LIMIT = 384
K_LIMIT = 128
POOL_LIMIT = 128
RAW_POOL_OWNER_LIMIT = 512
RAW_POOL_LIMIT = 8192
Point = tuple[Q, Q]
IncompleteError = finite.IncompleteError
require, tick, checked = finite.require, finite.tick, finite.checked
RAW_CASES = (("--", -1, -1), ("-+", -1, 1), ("+-", 1, -1), ("++", 1, 1))


def bounded_hull(points: list[Point], limit: int, deadline: float) -> list[Point]:
    tick(deadline)
    ordered = sorted(set(points))
    halves = []
    for sequence in (ordered, list(reversed(ordered))):
        half = []
        for p in sequence:
            tick(deadline)
            while (
                len(half) >= 2
                and cross(subtract(half[-1], half[-2]), subtract(p, half[-2])) <= 0
            ):
                half.pop()
            half.append(p)
        halves.append(half[:-1])
    result = ordered if len(ordered) < 3 else halves[0] + halves[1]
    if len(result) > limit:
        raise IncompleteError("center-case polygon vertex ceiling")
    tick(deadline)
    return result


def clip(points: list[Point], a: Q, b: Q, c: Q, limit: int, deadline: float) -> list[Point]:  # noqa: PLR0917
    tick(deadline)
    a, b, c = checked(a), checked(b), checked(c)
    result = []
    for p, q in edges(points) if len(points) > 1 else [(p, p) for p in points]:
        tick(deadline)
        fp = checked(finite.dot(p, (a, b)) - c)
        fq = checked(finite.dot(q, (a, b)) - c)
        if fp <= 0:
            result.append(p)
        if fp < 0 < fq or fq < 0 < fp:
            ratio = checked(fp / checked(fp - fq))
            delta = subtract(q, p)
            result.append(
                (
                    checked(p[0] + checked(ratio * delta[0])),
                    checked(p[1] + checked(ratio * delta[1])),
                )
            )
    # A segment has one undirected edge, so explicitly retain its second endpoint.
    if len(points) == 2 and finite.dot(points[1], (a, b)) <= c:
        result.append(points[1])
    return bounded_hull(result, limit, deadline)


def subtract(a: Point, b: Point) -> Point:
    return checked(a[0] - b[0]), checked(a[1] - b[1])


def cross(a: Point, b: Point) -> Q:
    return checked(checked(a[0] * b[1]) - checked(a[1] * b[0]))


def contains(polygon: list[Point], p: Point) -> bool:
    if not polygon:
        return False
    if len(polygon) == 1:
        return polygon[0] == p
    if len(polygon) == 2:
        return cross(subtract(polygon[1], polygon[0]), subtract(p, polygon[0])) == 0 and all(
            min(a, b) <= x <= max(a, b)
            for a, b, x in zip(polygon[0], polygon[1], p, strict=True)
        )
    return all(cross(subtract(b, a), subtract(p, a)) >= 0 for a, b in edges(polygon))


def edges(polygon: list[Point]) -> list[tuple[Point, Point]]:
    if len(polygon) < 2:
        return []
    if len(polygon) == 2:
        return [(polygon[0], polygon[1])]
    return list(zip(polygon, polygon[1:] + polygon[:1], strict=True))


def intersection(first: list[Point], second: list[Point], deadline: float) -> list[Point]:
    """Closed exact intersection, including singleton and segment hulls."""
    first = bounded_hull(first, CENTER_LIMIT, deadline)
    second = bounded_hull(second, CENTER_LIMIT, deadline)
    candidates = {p for p in first if contains(second, p)} | {
        p for p in second if contains(first, p)
    }
    for a, b in edges(first):
        for c, d in edges(second):
            tick(deadline)
            ab, cd, ca = subtract(b, a), subtract(d, c), subtract(c, a)
            denominator = cross(ab, cd)
            if denominator:
                t = checked(cross(ca, cd) / denominator)
                u = checked(cross(ca, ab) / denominator)
                if 0 <= t <= 1 and 0 <= u <= 1:
                    candidates.add(
                        (checked(a[0] + checked(t * ab[0])), checked(a[1] + checked(t * ab[1])))
                    )
            elif cross(ca, ab) == 0:
                candidates.update(
                    p for p in (a, b, c, d) if contains([a, b], p) and contains([c, d], p)
                )
    return bounded_hull(list(candidates), INTERSECTION_LIMIT, deadline)


def parse_polygon(raw: Any, counter: list[int], deadline: float) -> list[Point]:
    finite.opaque_polygon(raw)
    counter[0] += len(raw)
    if counter[0] > INPUT_VERTICES:
        raise IncompleteError("center-case input vertex ceiling")
    points = [(finite.rational(p[0]), finite.rational(p[1])) for p in raw]
    return bounded_hull(points, CENTER_LIMIT, deadline)


def necessary_pieces(
    rows: list[Any], deadline: float, counter: list[int]
) -> list[dict[str, Any]]:
    result = []
    for index, row in enumerate(rows):
        tick(deadline)
        lo, hi = map(finite.rational, row["interval"])
        lo, hi = max(lo, INTERVAL[0]), min(hi, INTERVAL[1])
        if lo > hi:
            continue
        cl, sl = finite.trig(lo)
        ch, sh = finite.trig(hi)
        reach = checked(min(checked(cl + sl), checked(ch + sh)) / 2)
        lower, upper = checked(OFFSET + reach), checked(U - OFFSET - reach)
        pieces = []
        for raw in row["residual_polygons"]:
            polygon = parse_polygon(raw, counter, deadline)
            if lower > upper:
                polygon = []
            else:
                for a, b, c in (
                    (Q(-1), Q(0), -lower),
                    (Q(1), Q(0), upper),
                    (Q(0), Q(-1), -lower),
                    (Q(0), Q(1), upper),
                ):
                    polygon = clip(polygon, a, b, c, CENTER_LIMIT, deadline)
            if polygon:
                pieces.append(polygon)
        result.append(
            {
                "row_index": index,
                "reference": copy.deepcopy(row["reference"]),
                "interval": (lo, hi),
                "pieces": pieces,
            }
        )
    return result


def ownership_planes(rows: list[dict[str, Any]], deadline: float) -> Any:
    for row in rows:
        lo, hi = row["interval"]
        cl, sl = finite.trig(lo)
        ch, sh = finite.trig(hi)
        centers = bounded_hull(
            [p for piece in row["pieces"] for p in piece], CENTER_LIMIT, deadline
        )
        for center in centers:
            for c in (ch, cl):
                for s in (sl, sh):
                    for sign in (-1, 1):
                        for a, b in (
                            (checked(sign * c), checked(sign * s)),
                            (checked(-sign * s), checked(sign * c)),
                        ):
                            rhs = checked(
                                checked(Q(1, 2) - MARGIN) + finite.dot((a, b), center)
                            )
                            tick(deadline)
                            yield a, b, rhs


def ownership_kernel(rows: list[dict[str, Any]], deadline: float) -> list[Point]:
    kernel = [(Q(0), Q(0)), (U, Q(0)), (U, U), (Q(0), U)]
    for a, b, rhs in ownership_planes(rows, deadline):
        kernel = clip(kernel, a, b, rhs, K_LIMIT, deadline)
    return kernel


def case_geometry(
    rows: list[dict[str, Any]],
    groups: dict[int, list[Point]],
    deadline: float,
    selected: list[Point] | None = None,
) -> dict[str, Any]:
    vertices = [p for row in rows for piece in row["pieces"] for p in piece]
    recorded = [
        {
            "row_index": r["row_index"],
            "reference": r["reference"],
            "interval": list(map(str, r["interval"])),
            "pieces": [finite.serial(p) for p in r["pieces"]],
        }
        for r in rows
    ]
    if not vertices:
        return {
            "status": "empty_case",
            "closed": True,
            "rows": recorded,
            "K": [],
            "H": [],
            "intersection": None,
        }
    if selected is not None:
        for a, b, rhs in ownership_planes(rows, deadline):
            require(
                all(finite.dot(p, (a, b)) <= rhs for p in selected),
                "selected-five subset calibration failed",
            )
    kernel = ownership_kernel(rows, deadline)
    owned = bounded_hull(groups[0] + kernel, CENTER_LIMIT, deadline)
    witness = None
    for owner in sorted(groups):
        if owner == 0:
            continue
        common = intersection(owned, groups[owner], deadline)
        if common:
            point = min(common)
            require(
                contains(owned, point) and contains(groups[owner], point),
                "intersection membership",
            )
            witness = {
                "other_owner": owner,
                "point": list(map(str, point)),
                "polygon": finite.serial(common),
            }
            break
    return {
        "status": "shared_owned_point" if witness else "unresolved",
        "closed": witness is not None,
        "rows": recorded,
        "K": finite.serial(kernel),
        "H": finite.serial(owned),
        "intersection": witness,
    }


def construct(
    rows: list[Any],
    raw_groups: dict[str, Any],
    *,
    deadline: float,
    input_vertex_offset: int = 0,
    selected: list[Point] | None = None,
    unpooled_groups: dict[str, Any] | None = None,
) -> dict[str, Any]:
    require(
        len(raw_groups) == 17
        and "0" in raw_groups
        and all(str(int(k)) == k and 0 <= int(k) < 24 for k in raw_groups),
        "full17 owned-hull roster",
    )
    counter = [input_vertex_offset]
    groups = {int(o): parse_polygon(p, counter, deadline) for o, p in raw_groups.items()}
    unpooled = None
    if unpooled_groups is not None:
        require(set(unpooled_groups) == set(raw_groups), "matched unpooled owner roster")
        unpooled = group_closure(
            {int(o): parse_polygon(p, counter, deadline) for o, p in unpooled_groups.items()},
            deadline,
        )
    pooled_closure = None if unpooled else group_closure(groups, deadline)
    unsplit = (
        {
            "status": "conditional_unpooled_intersection",
            "closed": True,
            "intersection": unpooled,
        }
        if unpooled
        else {
            "status": "conditional_pooled_intersection",
            "closed": True,
            "intersection": pooled_closure,
        }
        if pooled_closure
        else None
    )
    if unsplit is None:
        pieces = necessary_pieces(rows, deadline, counter)
        unsplit = case_geometry(pieces, groups, deadline, selected)
    else:
        pieces = []
    alpha = beta = None
    if not unsplit["closed"]:
        vertices = [p for row in pieces for polygon in row["pieces"] for p in polygon]
        ds = [checked(p[0] + p[1]) for p in vertices]
        es = [checked(p[1] - p[0]) for p in vertices]
        alpha = checked(checked(min(ds) + max(ds)) / 2)
        beta = checked(checked(min(es) + max(es)) / 2)
    cases = []
    for name, sigma, tau in RAW_CASES:
        if unsplit["closed"]:
            cases.append({"id": name, "status": "not_needed_unsplit_proved", "closed": None})
            continue
        assert alpha is not None
        assert beta is not None
        clipped = []
        for row in pieces:
            polygons = []
            for original_piece in row["pieces"]:
                polygon = clip(
                    original_piece,
                    Q(-sigma),
                    Q(-sigma),
                    checked(-sigma * alpha),
                    CENTER_LIMIT,
                    deadline,
                )
                polygon = clip(
                    polygon, Q(tau), Q(-tau), checked(-tau * beta), CENTER_LIMIT, deadline
                )
                if polygon:
                    polygons.append(polygon)
            clipped.append(row | {"pieces": polygons})
        cases.append({"id": name} | case_geometry(clipped, groups, deadline, selected))
    proved = unsplit["closed"] or all(c["closed"] is True for c in cases)
    tick(deadline)
    return {
        "alpha": str(alpha) if alpha is not None else None,
        "beta": str(beta) if beta is not None else None,
        "unsplit": unsplit,
        "cases": cases,
        "conditional_I_exclusion_proved": proved,
        "criterion_met": proved,
        "status": "closed_I_exclusion" if proved else "criterion_missed",
        "input_vertices": counter[0],
        "matched_unpooled_intersection": unpooled,
        "conditional_pooled_intersection": pooled_closure,
        "compression_information_recovered": bool(pooled_closure and not unpooled),
    }


def group_closure(groups: dict[int, list[Point]], deadline: float) -> dict[str, Any] | None:
    for first in sorted(groups):
        for second in sorted(groups):
            if first >= second:
                continue
            common = intersection(groups[first], groups[second], deadline)
            if common:
                return {
                    "owners": [first, second],
                    "point": list(map(str, min(common))),
                    "intersection": finite.serial(common),
                }
    return None


def pool_original(
    gate: dict[str, Any], prepared: dict[str, Any], deadline: float
) -> tuple[dict[str, Any], dict[str, Any], int, list[Point]]:
    """Proof-only points from an accepted original node, never a partial child."""
    _, accepted = finite.accepted_receipt(gate)
    parent = accepted["custody"]["parent_replay"]
    mask = parent["mask"]
    directory = finite.retained_path(gate["saved_objects"])
    seed_path = directory / f"seed-{gate['seed_sha256']}.json.gz"
    node_path = directory / f"node-{gate['node_sha256']}.json.gz"
    seed = finite.seed_decode(seed_path, deadline)
    require(finite.identity(seed) == gate["seed_sha256"], "pool canonical seed differs")
    stream = finite.BoundedNode(node_path, deadline)
    header = stream.header
    require(
        set(header["initial"]["groups"]) == set(seed["groups"]) == set(map(str, mask)),
        "pool initial/seed roster differs",
    )
    origins: dict[int, dict[Point, dict[str, Any]]] = {o: {} for o in mask}
    counts = dict.fromkeys(mask, 0)
    counter = [0]

    def append(owner: int, raw: Any, source: dict[str, Any]) -> None:
        finite.opaque_polygon(raw)
        counts[owner] += len(raw)
        counter[0] += len(raw)
        if counts[owner] > RAW_POOL_OWNER_LIMIT or counter[0] > RAW_POOL_LIMIT:
            raise IncompleteError("proof-only raw pool point ceiling")
        for index, point in enumerate(raw):
            tick(deadline)
            parsed = (finite.rational(point[0]), finite.rational(point[1]))
            origins[owner].setdefault(parsed, source | {"point_index": index})

    for owner in sorted(mask):
        append(
            owner,
            header["initial"]["groups"][str(owner)],
            {"kind": "initial_group", "owner": owner, "jsonpath": f"$.initial.groups.{owner}"},
        )
    count = 0
    for si, step in enumerate(stream.steps()):
        tick(deadline)
        require(
            si < 16
            and step["index"] == si
            and step["owner"] == parent["step_owners"][si]
            and step["complete"] is True,
            "accepted original pool step/order",
        )
        append(
            step["owner"],
            step["common_owned_kernel"],
            {
                "kind": "common_owned_kernel",
                "step": si,
                "owner": step["owner"],
                "jsonpath": f"$.steps[{si}].common_owned_kernel",
            },
        )
        count += 1
    require(
        count == 16
        and stream.sha256 == gate["node_sha256"]
        and header["schema"] == "exact_generic_owned_hull_v1"
        and header["mask"] == mask
        and header["parent"] is None
        and header["guard_source"] is None
        and header["constraints"] == []
        and header["source"]["sha256"] == gate["seed_sha256"]
        and header["closed"] is False
        and header["contradiction"] is None,
        "accepted original pool canonical EOF/header",
    )
    final = header["final_state"]
    pools = {owner: bounded_hull(list(origins[owner]), POOL_LIMIT, deadline) for owner in mask}
    original = copy.deepcopy(prepared["initial_state"])
    require(
        final["groups"]["0"] == prepared["guard_source"]["point_origins"]["old"]
        and final["cells"] == original["cells"]
        and final["world"] == original["world"]
        and final["mask"] == mask
        and final["U"] == str(U)
        and final["B"] == "1"
        and all(final["groups"][str(o)] == original["groups"][str(o)] for o in mask if o != 0),
        "pool original final-state differs",
    )
    for owner in mask:
        points = parse_polygon(final["groups"][str(owner)], counter, deadline)
        require(
            all(contains(pools[owner], point) for point in points),
            "accepted final hull not contained in original pool",
        )
    for first in sorted(mask):
        for second in sorted(mask):
            if first < second:
                require(
                    not intersection(pools[first], pools[second], deadline),
                    "unconditional original pool calibration intersects",
                )
    selected_raw = prepared["guard_source"]["point_origins"]["selected"]
    require(len(selected_raw) == 5, "all five finite points required")
    selected = parse_polygon(selected_raw, counter, deadline)
    require(len(set(selected)) == 5, "five finite point identities")
    pools[0] = bounded_hull(pools[0] + selected, POOL_LIMIT, deadline)
    original["groups"] = {str(o): finite.serial(pools[o]) for o in mask}
    evidence = {
        "node_sha256": gate["node_sha256"],
        "seed_sha256": gate["seed_sha256"],
        "node_object": str(node_path.relative_to(finite.REPO)),
        "seed_object": str(seed_path.relative_to(finite.REPO)),
        "parent_geometry_replayed": False,
        "initial_seed_hull_equality": (
            "accepted full check_seed premise on these canonical objects"
        ),
        "original_final_contained": True,
        "unconditional_parent_pools_disjoint": True,
        "raw_counts": {str(o): n for o, n in counts.items()},
        "raw_total": sum(counts.values()),
        "origins": {
            str(o): [
                {"point": list(map(str, p)), "origin": origin}
                for p, origin in origins[o].items()
            ]
            for o in sorted(mask)
        },
        "pools": {
            str(o): finite.serial(bounded_hull(list(origins[o]), POOL_LIMIT, deadline))
            for o in mask
        },
        "selected_five": finite.serial(selected),
        "unpooled_conditional_groups": copy.deepcopy(prepared["initial_state"]["groups"]),
    }
    return original, evidence, counter[0], selected


def opaque_row(row: Any) -> None:
    require(type(row) is dict, "row object required")
    require(
        type(row["interval"]) is list and len(row["interval"]) == 2, "closed interval shape"
    )
    for token in row["interval"]:
        finite.rational_grammar(token)
    reference = row["reference"]
    require(
        type(reference) is dict
        and type(reference["row"]) is int
        and (
            (
                reference["kind"] == "wall_seed"
                and set(reference) == {"kind", "owner", "row"}
                and type(reference["owner"]) is int
            )
            or (
                reference["kind"] == "phase3"
                and set(reference) == {"kind", "node", "step", "row"}
                and type(reference["node"]) is str
                and type(reference["step"]) is int
            )
        ),
        "typed row reference",
    )
    finite.opaque_polygon(row["outer_domain"])
    require(type(row["residual_polygons"]) is list, "residual union shape")
    for polygon in row["residual_polygons"]:
        finite.opaque_polygon(polygon)


def validate_state(
    state: dict[str, Any], frame: dict[str, Any], mask: list[int], coarse: int
) -> None:
    require(
        state["mask"] == mask
        and state["mask_index"] is None
        and state["U"] == str(U)
        and state["B"] == "1"
        and state["world"] == frame["cells"],
        "original frame/state differs",
    )
    keys = set(map(str, mask))
    require(set(state["cells"]) == set(state["groups"]) == keys, "complete state owner keys")
    for owner in mask:
        finite.opaque_polygon(state["groups"][str(owner)])
        rows = state["cells"][str(owner)]
        count = 32 if owner == coarse else 64
        require(type(rows) is list and len(rows) == count, "complete row roster")
        for index, row in enumerate(rows):
            opaque_row(row)
            require(row["reference"]["row"] == index, "row reference index differs")
            if row["reference"]["kind"] == "wall_seed":
                require(row["reference"]["owner"] == owner, "wall seed owner differs")


def read_premise(
    value: Any, expected: str, held: dict[Path, tuple[str, int]], deadline: float
) -> dict[str, Any]:
    path = finite.retained_path(value)
    raw, data = finite.read_json(path, JSON_LIMIT)
    require(
        hashlib.sha256(raw).hexdigest() == expected, "accepted premise byte identity differs"
    )
    tick(deadline)
    held[path] = (expected, JSON_LIMIT)
    return data


def hold_initial_inputs(
    document: dict[str, Any],
    prepared: dict[str, Any],
    held: dict[Path, tuple[str, int]],
    deadline: float,
) -> None:
    for key in (
        "finite_descriptor",
        "finite_certificate",
        "finite_replay",
        "centered_parent_receipt",
    ):
        path = finite.retained_path(document[key])
        current = finite.digest(path, JSON_LIMIT, deadline)
        require(
            path not in held or held[path][0] == current, "initialization premise bytes changed"
        )
        held[path] = (current, JSON_LIMIT)
    parent = prepared["parent"]
    read_premise(parent["h290_receipt"], parent["h290_receipt_sha256"], held, deadline)
    for relative, expected in parent["compressed_sha256"].items():
        path = finite.retained_path(relative)
        ceiling = finite.SEED_LIMIT if path.name.startswith("seed-") else finite.NODE_LIMIT
        require(
            finite.digest(path, ceiling, deadline) == expected,
            "parent original object identity differs",
        )
        held[path] = (expected, ceiling)


def intake(
    document: dict[str, Any], held: dict[Path, tuple[str, int]], deadline: float
) -> tuple[dict[str, Any], dict[str, Any], int, list[Point]]:
    require(document["schema"] == DESCRIPTOR_SCHEMA, "center-case descriptor schema")
    if document["base_kind"] == BASE_INITIAL:
        require(
            set(document)
            == {
                "schema",
                "base_kind",
                "proof_pool",
                "initialization_descriptor",
                "initialization_descriptor_sha256",
            },
            "initialization base descriptor fields",
        )
        require(
            document["proof_pool"] == "accepted_original_parent_kernels",
            "frozen original-parent pool required",
        )
        source = read_premise(
            document["initialization_descriptor"],
            document["initialization_descriptor_sha256"],
            held,
            deadline,
        )
        require("child_object" not in source, "initialization base must not use child")
        for key in (
            "finite_descriptor",
            "finite_certificate",
            "finite_replay",
            "centered_parent_receipt",
        ):
            path = finite.retained_path(source[key])
            held[path] = (finite.digest(path, JSON_LIMIT, deadline), JSON_LIMIT)
        prepared = conditional.prepare(source, deadline=deadline)
        hold_initial_inputs(source, prepared, held, deadline)
        state = prepared["initial_state"]
        validate_state(
            state, prepared["frame"], state["mask"], prepared["custody"]["label_to_owner"]["6"]
        )
        gate = finite.read_json(finite.retained_path(source["finite_descriptor"]))[1]
        state, pool, offset, selected = pool_original(gate, prepared, deadline)
        return (
            state,
            {
                "base_kind": BASE_INITIAL,
                "proof_pool": pool,
                "initialization_freshly_reconstructed": True,
                "parent_geometry_replayed": False,
                "child_geometry_replayed_now": False,
                "initialization_descriptor": document["initialization_descriptor"],
                "initialization_descriptor_sha256": document[
                    "initialization_descriptor_sha256"
                ],
                "initial_sha256": finite.identity(state),
                "parent": prepared["parent"],
                "guard_source": prepared["guard_source"],
            },
            offset,
            selected,
        )
    raise ValueError(
        "unsupported center-case base; fresh initialization and original-parent pool required"
    )


def generate(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    frozen = finite.canonical(document)
    held: dict[Path, tuple[str, int]] = {}
    state, custody, offset, selected = intake(document, held, deadline)
    result = construct(
        state["cells"]["0"],
        state["groups"],
        deadline=deadline,
        input_vertex_offset=offset,
        selected=selected,
        unpooled_groups=custody["proof_pool"]["unpooled_conditional_groups"]
        if "proof_pool" in custody
        else None,
    )
    for path, (expected, ceiling) in held.items():
        require(
            finite.digest(path, ceiling, deadline) == expected,
            "center-case input changed during construction",
        )
    require(finite.canonical(document) == frozen, "center-case descriptor changed")
    return {
        "schema": SCHEMA,
        "guard": copy.deepcopy(GUARD),
        "container": conditional.standing.CenteredContainer(U, V).record(),
        "constants": {
            "margin": str(MARGIN),
            "input_vertices": INPUT_VERTICES,
            "rational_bits": finite.BIT_LIMIT,
            "center_vertices": CENTER_LIMIT,
            "H_vertices": CENTER_LIMIT,
            "intersection_vertices": INTERSECTION_LIMIT,
            "K_vertices": K_LIMIT,
            "pool_vertices": POOL_LIMIT,
            "raw_pool_per_owner": RAW_POOL_OWNER_LIMIT,
            "raw_pool_total": RAW_POOL_LIMIT,
        },
        "custody": custody,
        "mask": state["mask"],
        "unconditional_exclusion_proved": False,
        "census_admission_proved": False,
        "global_optimality_proved": False,
        "root_checked_now": False,
        "hand_implication": (
            "Astra hand derivation; not independently mathematically reviewed "
            "or machine-checked"
        ),
        **result,
    }


def check(
    document: dict[str, Any], certificate: dict[str, Any], *, deadline: float
) -> dict[str, Any]:
    core = {k: v for k, v in certificate.items() if k not in ("provenance", "invocation")}
    require(
        core == generate(document, deadline=deadline),
        "fresh center-case reconstruction differs",
    )
    return copy.deepcopy(core) | {"verification_passed": True}


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
            "producer/kernel/root import in finite checker",
        )
        raw, document = finite.read_json(args.descriptor)
        if args.certificate:
            certificate_raw, certificate = finite.read_json(args.certificate, OUTPUT_LIMIT)
            result = check(document, certificate, deadline=deadline)
            require(
                finite.read_json(args.certificate, OUTPUT_LIMIT)[0] == certificate_raw,
                "certificate changed during verification",
            )
        else:
            result = generate(document, deadline=deadline)
        require(
            finite.read_json(args.descriptor)[0] == raw,
            "descriptor changed during construction",
        )
    except IncompleteError as exc:
        result = {
            "schema": SCHEMA,
            "status": "incomplete",
            "error": str(exc),
            "conditional_I_exclusion_proved": False,
        }
    except (
        ValueError,
        KeyError,
        TypeError,
        OSError,
        EOFError,
        conditional.standing.VerificationError,
    ) as exc:
        result = {
            "schema": SCHEMA,
            "status": "refused",
            "error": str(exc),
            "conditional_I_exclusion_proved": False,
        }
    result.update(
        provenance=provenance(
            Path(__file__),
            Path(finite.__file__),
            Path(conditional.__file__),
            Path(conditional.standing.__file__),
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
            "error": "center-case output byte or wall ceiling",
            "conditional_I_exclusion_proved": False,
        }
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)
    return 0 if result["status"] in ("closed_I_exclusion", "criterion_missed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
