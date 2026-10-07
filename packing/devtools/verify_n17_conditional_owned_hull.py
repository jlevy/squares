"""Independent replay of a parent-relative, closed-guard owned-hull continuation.

The parent is an explicitly accepted centered domain, never a fresh generic seed.
This module must remain producer, kernel and algebraic-root free.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
import time
from fractions import Fraction as Q
from pathlib import Path, PurePosixPath
from typing import Any, cast

from devtools import probe_n17_conditional_owned_hull as finite
from devtools import verify_n17_kernel_certificate as standing
from devtools.provenance import provenance
from sqpack import retained_json

CHILD_SCHEMA = "n17-parent-guard-owned-hull/v1"
DESCRIPTOR_SCHEMA = "n17-parent-guard-owned-hull-context/v1"
RECEIPT_SCHEMA = "n17-parent-guard-owned-hull-verification/v1"
INITIAL_SCHEMA = "n17-parent-guard-owned-hull-initial/v1"
GUARD = {"kind": "closed_half_angle_guard", "owner": 0, "interval": ["13/32", "27/64"]}
Point = tuple[Q, Q]
NODE_ID = "n17-conditional-owned-hull"
IncompleteError = finite.IncompleteError
read_json = finite.read_json
require = finite.require
identity = finite.identity
OUTPUT_LIMIT = 64 << 20
CHILD_COMPRESSED_LIMIT = 64 << 20
CHILD_DECODED_LIMIT = 512 << 20


class ChildStream(finite.BoundedNode):
    """Separate child decoded ceiling; the accepted parent keeps its 2GiB cap."""

    def _fill(self) -> None:
        super()._fill()
        if self.decoded > CHILD_DECODED_LIMIT:
            raise IncompleteError("conditional child decoded byte ceiling")

    def _value(self) -> Any:
        def floating(_token: str) -> Any:
            raise ValueError("floating child JSON value")

        self._decoder = json.JSONDecoder(
            object_pairs_hook=finite.unique,
            parse_int=finite.integer,
            parse_float=floating,
            parse_constant=finite.nonfinite,
        )
        return super()._value()


def _cross(a: Point, b: Point) -> Q:
    return a[0] * b[1] - a[1] * b[0]


def _subtract(a: Point, b: Point) -> Point:
    return a[0] - b[0], a[1] - b[1]


def _on_segment(p: Point, a: Point, b: Point) -> bool:
    return _cross(_subtract(b, a), _subtract(p, a)) == 0 and all(
        min(a[k], b[k]) <= p[k] <= max(a[k], b[k]) for k in (0, 1)
    )


def _contains(polygon: list[Point], point: Point) -> bool:
    if not polygon:
        return False
    if len(polygon) == 1:
        return point == polygon[0]
    if len(polygon) == 2:
        return _on_segment(point, polygon[0], polygon[1])
    return all(
        _cross(_subtract(polygon[(k + 1) % len(polygon)], p), _subtract(point, p)) >= 0
        for k, p in enumerate(polygon)
    )


def _edges(polygon: list[Point]) -> list[tuple[Point, Point]]:
    if len(polygon) < 2:
        return []
    if len(polygon) == 2:
        return [(polygon[0], polygon[1])]
    return [(p, polygon[(k + 1) % len(polygon)]) for k, p in enumerate(polygon)]


def intersection(first: list[Point], second: list[Point]) -> list[Point]:
    """Exact closed intersection, including singleton and segment hulls."""
    a, b = standing.hull(first), standing.hull(second)
    if not a or not b:
        return []
    found = [p for p in a if _contains(b, p)] + [p for p in b if _contains(a, p)]
    for p, p1 in _edges(a):
        r = _subtract(p1, p)
        for q, q1 in _edges(b):
            s, qp = _subtract(q1, q), _subtract(q, p)
            determinant = _cross(r, s)
            if determinant:
                t, u = _cross(qp, s) / determinant, _cross(qp, r) / determinant
                if 0 <= t <= 1 and 0 <= u <= 1:
                    found.append((p[0] + t * r[0], p[1] + t * r[1]))
            elif _cross(qp, r) == 0:
                found.extend(
                    v for v in (p, p1, q, q1) if _on_segment(v, p, p1) and _on_segment(v, q, q1)
                )
    return standing.hull(found)


def initial_closure(groups: dict[int, list[Point]]) -> dict[str, Any] | None:
    """First unordered intersecting owner pair, in lexicographic owner order."""
    owners = sorted(groups)
    for k, first in enumerate(owners):
        for second in owners[k + 1 :]:
            common = intersection(groups[first], groups[second])
            if common:
                return {
                    "kind": "owned_hulls_intersect",
                    "owners": [first, second],
                    "step": -1,
                    "intersection": [[str(x), str(y)] for x, y in common],
                }
    return None


def guard_closure(rows: list[Any], step: int) -> dict[str, Any] | None:
    """Every closed owner0 row meeting the guard, including endpoint-only seams."""
    lo, hi = Q(13, 32), Q(27, 64)
    require(step == 15, "guard terminal requires final owner0 update")
    witnesses = []
    details = []
    for index, row in enumerate(rows):
        interval = (
            row.interval if isinstance(row, standing.Row) else tuple(map(Q, row["interval"]))
        )
        residual = row.residual if isinstance(row, standing.Row) else row["residual_polygons"]
        if interval[0] <= hi and interval[1] >= lo:
            if any(residual):
                return None
            witnesses.append(index)
            reference = row.reference if isinstance(row, standing.Row) else row["reference"]
            details.append(
                {
                    "row_index": index,
                    "reference": copy.deepcopy(reference),
                    "intersection": [str(max(lo, interval[0])), str(min(hi, interval[1]))],
                }
            )
    require(bool(witnesses), "guard has no covering rows")
    return {
        "kind": "guarded_owner_cover_empty",
        "owner": 0,
        "step": step,
        "guard": copy.deepcopy(GUARD),
        "row_indices": witnesses,
        "witnesses": details,
    }


def prepare(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    """Freshly reconstruct the finite gate, joining accepted parent replay premises."""
    require(document["schema"] == DESCRIPTOR_SCHEMA, "conditional descriptor schema")
    frozen = finite.canonical(document)
    held: dict[str, tuple[Path, bytes]] = {}
    values: dict[str, dict[str, Any]] = {}
    for field in (
        "finite_descriptor",
        "finite_certificate",
        "finite_replay",
        "centered_parent_receipt",
    ):
        path = finite.retained_path(document[field])
        raw, value = read_json(
            path, OUTPUT_LIMIT if field == "finite_certificate" else finite.JSON_LIMIT
        )
        held[field] = path, raw
        values[field] = value
    gate, certificate, replay, centered = (
        values[k]
        for k in (
            "finite_descriptor",
            "finite_certificate",
            "finite_replay",
            "centered_parent_receipt",
        )
    )
    require(
        hashlib.sha256(held["centered_parent_receipt"][1]).hexdigest()
        == document["centered_parent_receipt_sha256"],
        "centered parent receipt bytes differ",
    )
    fresh = finite.check(gate, certificate, deadline=deadline)
    require(
        fresh["status"] == "conditional_gain_candidate"
        and replay["finite_reconstruction_verified"] is True
        and replay["status"] == fresh["status"]
        and replay["certificate_sha256"] == identity(certificate),
        "fresh finite gain/replay premise differs",
    )
    require(
        certificate["endpoint_control"]["strictly_inside"] is True
        and certificate["endpoint_control"]["nonempty"] is True,
        "endpoint calibration premise differs",
    )
    final, custody = finite.extract(gate, deadline)
    _, accepted = finite.accepted_receipt(gate)
    context = standing.CenteredContainer(finite.U, finite.V).record()
    result = centered["fresh_standing"]["receipt"]
    require(
        centered["schema"] == "n17-centered-cap-standing-context/v1"
        and centered["status"] == "centered_stall_control_checked"
        and centered["readiness_passed"] is True
        and centered["verification_passed"] is True
        and centered["fresh_standing"]["exit_code"] == 0,
        "accepted centered parent required",
    )
    require(
        result["schema"] == "n17-centered-cap-certificate-verification/v1"
        and result["mode"] == "full"
        and result["status"] == "PASS_STALL"
        and result["independent_modules"] is True
        and result["root_cap_join_checked"] is False
        and result["owned_hull_limit"] == 48
        and result["container"] == context
        and result["certificate"]
        == {"seed_sha256": gate["seed_sha256"], "node_sha256": gate["node_sha256"]}
        and result["compressed_sha256"] == parent_compressed_roles(gate)
        and result["mask"] == final["mask"]
        and result["counts"]["steps"] == 16
        and result["closed"] is False
        and result["closure"] is None,
        "centered same-object full stall premise differs",
    )
    require(
        centered["accepted_context"]["accepted_endpoint"]["sha256"]
        == gate["h290_receipt_sha256"],
        "centered/H290 accepted premise differs",
    )
    parent_order = accepted["custody"]["parent_replay"]["step_owners"]
    return initialize(
        final,
        certificate,
        frame=gate["frame"],
        roles=gate["label_to_owner"],
        parent_order=parent_order,
        custody=custody,
        document=document,
        held=held,
        frozen=frozen,
        deadline=deadline,
    )


def parent_compressed_roles(gate: dict[str, Any]) -> dict[str, str]:
    """Join exact canonical native paths to the standing receipt's two role keys."""
    directory = gate["saved_objects"]
    require(
        type(directory) is str
        and not PurePosixPath(directory).is_absolute()
        and ".." not in PurePosixPath(directory).parts,
        "invalid canonical parent directory",
    )
    paths = {
        kind: str(PurePosixPath(directory) / f"{kind}-{gate[kind + '_sha256']}.json.gz")
        for kind in ("seed", "node")
    }
    require(
        set(gate["compressed_sha256"]) == set(paths.values()),
        "canonical parent compressed path roster differs",
    )
    return {kind: gate["compressed_sha256"][path] for kind, path in paths.items()}


def initialize(
    final: dict[str, Any],
    certificate: dict[str, Any],
    *,
    frame: dict[str, Any],
    roles: dict[str, int],
    parent_order: list[int],
    custody: dict[str, Any],
    document: dict[str, Any],
    held: dict[str, tuple[Path, bytes]],
    frozen: bytes,
    deadline: float,
) -> dict[str, Any]:
    """Exact augmentation; accepted parent geometry is a named custody premise."""
    old = standing.poly(final["groups"]["0"])
    selected = standing.poly(certificate["variants"]["target"]["selected_hull"])
    require(
        len(old) == 20 and len(selected) == 5, "frozen old20/new5 initialization roster differs"
    )
    require(len(set(old)) == 20 and len(set(selected)) == 5, "duplicate initialization points")
    augmented = standing.hull(old + selected)
    require(len(augmented) <= 25 and len(augmented) <= 48, "augmented hull capacity")
    require(
        set(roles) == {str(i) for i in range(1, 18)}
        and roles["1"] == 0
        and roles["6"] == 12
        and sorted(roles.values()) == final["mask"]
        and len(set(roles.values())) == 17,
        "frozen label/owner roster",
    )
    require(
        len(parent_order) == 16
        and len(set(parent_order)) == 16
        and set(parent_order) == set(final["mask"]) - {roles["6"]},
        "complete parent owner order",
    )
    parent = {
        "schema": "accepted-centered-parent/v1",
        "seed_sha256": custody["seed_sha256"],
        "node_sha256": custody["node_sha256"],
        "compressed_sha256": copy.deepcopy(custody["compressed_sha256"]),
        "h290_receipt": custody["h290_receipt"],
        "h290_receipt_sha256": custody["h290_receipt_sha256"],
        "centered_parent_receipt": document["centered_parent_receipt"],
        "centered_parent_receipt_sha256": document["centered_parent_receipt_sha256"],
    }
    guard_source = {
        "finite_certificate": document["finite_certificate"],
        "certificate_sha256": identity(certificate),
        "finite_replay": document["finite_replay"],
        "finite_replay_sha256": hashlib.sha256(held["finite_replay"][1]).hexdigest(),
        "guard": copy.deepcopy(GUARD),
        "point_origins": {
            "old": copy.deepcopy(final["groups"]["0"]),
            "selected": copy.deepcopy(certificate["variants"]["target"]["selected_hull"]),
        },
    }
    initial = copy.deepcopy(final)
    initial.update(
        schema=INITIAL_SCHEMA,
        parent=parent,
        guard_source=guard_source,
        constraints=[copy.deepcopy(GUARD)],
        guard=copy.deepcopy(GUARD),
    )
    initial["groups"]["0"] = [[str(x), str(y)] for x, y in augmented]
    for path, raw in held.values():
        require(
            read_json(path, OUTPUT_LIMIT)[0] == raw, "conditional preparation input changed"
        )
    require(finite.canonical(document) == frozen, "conditional descriptor changed")
    finite.tick(deadline)
    return copy.deepcopy(
        {
            "initial_state": initial,
            "frame": frame,
            "parent": parent,
            "guard_source": guard_source,
            "constraints": [GUARD],
            "custody": custody
            | {
                "parent_step_owners": parent_order,
                "label_to_owner": roles,
                "parent_geometry_replayed": False,
                "finite_gate_freshly_reconstructed": True,
            },
        }
    )


def state_from(prepared: dict[str, Any]) -> standing.State:
    initial, frame = prepared["initial_state"], prepared["frame"]
    require(
        initial["schema"] == INITIAL_SCHEMA
        and initial["constraints"] == [GUARD]
        and initial["guard"] == GUARD,
        "conditional initialization/guard",
    )
    mask = cast(list[int], initial["mask"])
    require(type(mask) is list and len(mask) == 17 and mask == sorted(set(mask)), "full17 mask")
    require(
        set(initial["groups"]) == set(initial["cells"]) == set(map(str, mask)),
        "initial complete owner keys",
    )
    require(
        initial["world"] == frame["cells"]
        and initial["U"] == str(finite.U)
        and initial["B"] == "1"
        and frame["capture_cap"] == str(finite.V),
        "initial original frame/context",
    )
    state = standing.State(
        [standing.poly(p) for p in frame["cells"]],
        finite.U,
        64,
        list(mask),
        container=standing.CenteredContainer(finite.U, finite.V),
    )
    for owner in mask:
        state.groups[owner] = standing.hull(standing.poly(initial["groups"][str(owner)]))
        require(len(state.groups[owner]) <= 48, "initial hull limit")
        rows = initial["cells"][str(owner)]
        previous = Q(0)
        parsed = []
        for record in rows:
            lo, hi = map(Q, record["interval"])
            require(lo == previous and lo < hi <= 1, "initial closed complete partition")
            previous = hi
            parsed.append(
                standing.Row(
                    (lo, hi),
                    copy.deepcopy(record["reference"]),
                    standing.hull(standing.poly(record["outer_domain"])),
                    [standing.hull(standing.poly(p)) for p in record["residual_polygons"]],
                )
            )
        require(
            previous == 1
            and len(rows)
            == (32 if owner == prepared["custody"]["label_to_owner"]["6"] else 64),
            "initial full row count",
        )
        state.rows[owner] = parsed
    return state


def replay(
    prepared: dict[str, Any], stream: finite.BoundedNode, *, deadline: float
) -> dict[str, Any]:
    """Replay all child rows from the conditional admitted state, through canonical EOF."""
    state = state_from(prepared)
    finite.tick(deadline)
    node = stream.header
    expected_source = {"conditional_initial_sha256": identity(prepared["initial_state"])}
    require(
        node["schema"] == CHILD_SCHEMA
        and node["node_id"] == NODE_ID
        and node["initial"] == prepared["initial_state"]
        and node["source"] == expected_source
        and node["mask_index"] is None
        and node["mask"] == state.mask
        and node["U"] == str(finite.U)
        and node["B"] == "1",
        "conditional child initial/header differs",
    )
    for key in ("parent", "guard_source", "constraints"):
        require(node[key] == prepared[key], "child ancestry/guard differs")
    order = [o for o in prepared["custody"]["parent_step_owners"] if o != 0] + [0]
    derived = initial_closure(state.groups)
    finite.tick(deadline)
    count = 0
    for si, step in enumerate(stream.steps()):
        finite.tick(deadline)
        require(
            derived is None
            and si < 16
            and step["index"] == si
            and step["owner"] == order[si]
            and step["complete"] is True
            and step["allowed_half_angle"] == ["0", "1"],
            "conditional step/order/complete header",
        )
        owner = step["owner"]
        require(
            set(step["prior_owned_hulls"]) == set(map(str, state.mask)),
            "step prior owner roster",
        )
        for other in state.mask:
            require(
                standing.same_set(
                    standing.poly(step["prior_owned_hulls"][str(other)]), state.groups[other]
                ),
                "step prior owned hull differs",
            )
        require(
            [tuple(map(Q, r["interval"])) for r in step["rows"]]
            == [r.interval for r in state.rows[owner]],
            "conditional refinement/partition change",
        )
        before = list(state.groups[owner])
        new, planes, live = standing.check_step(
            state, step, si, NODE_ID, set(range(len(step["rows"])))
        )
        standing.compress(state, step, si, planes, any_live=live)
        state.rows[owner] = new
        standing.bound_memos(state, owner, before)
        state.tick("steps")
        count += 1
        derived = standing.derive_closure(state, owner, si)
        if derived is None and any(
            intersection(state.groups[owner], state.groups[other])
            for other in state.mask
            if other != owner
        ):
            derived = {"kind": "owned_hulls_intersect"}
        if derived is None and owner == 0:
            derived = guard_closure(state.rows[0], si)
        if derived is not None and derived["kind"] == "owned_hulls_intersect":
            declared = node["contradiction"]
            pair = cast(list[int], declared["owners"])
            require(
                type(pair) is list
                and len(pair) == 2
                and pair == sorted(set(pair))
                and owner in pair
                and all(o in state.mask for o in pair)
                and declared["kind"] == "owned_hulls_intersect"
                and declared["step"] == si,
                "poststep actual owner pair differs",
            )
            require(
                bool(intersection(state.groups[pair[0]], state.groups[pair[1]])),
                "declared pair does not intersect",
            )
            point = standing.point(declared["point"])
            require(
                all(_contains(state.groups[o], point) for o in pair),
                "closure point outside named hulls",
            )
            require(
                set(declared) == {"kind", "owners", "step", "point"}, "closure witness grammar"
            )
            derived = copy.deepcopy(declared)
        finite.tick(deadline)
    require(stream.sha256 is not None, "child canonical EOF missing")
    require(node["contradiction"] == derived, "actual conditional closure differs")
    standing.check_final(state, node, stall=derived is None)
    final = node["final_state"]
    for key in ("parent", "guard_source", "constraints"):
        require(final[key] == prepared[key], "final ancestry/guard differs")
    require(
        final["guard"] == GUARD
        and final["source"] == expected_source
        and final["world"] == prepared["frame"]["cells"]
        and final["mask_index"] is None
        and final["mask"] == state.mask
        and final["U"] == str(finite.U)
        and final["B"] == "1"
        and set(final["groups"]) == set(final["cells"]) == set(map(str, state.mask)),
        "full final context differs",
    )
    for owner in state.mask:
        require(
            [tuple(map(Q, r["interval"])) for r in final["cells"][str(owner)]]
            == [r.interval for r in state.rows[owner]],
            "final intervals differ",
        )
    require(
        node["conditional_exclusion_proved"] is False
        and node["census_admission_proved"] is False,
        "producer claims conditional admission",
    )
    complete = derived is not None or count == 16
    finite.tick(deadline)
    return {
        "schema": RECEIPT_SCHEMA,
        "status": "PASS_CONDITIONAL_CLOSED"
        if derived
        else "PASS_CONDITIONAL_STALL"
        if complete
        else "INCOMPLETE",
        "mode": "full",
        "steps_checked": count,
        "closure": derived,
        "closed": derived is not None,
        "conditional_exclusion_proved": derived is not None,
        "criterion_met": derived is not None,
        "complete_round": count == 16,
        "final_state_equal": True,
        "node_sha256": stream.sha256,
        "initial_sha256": identity(prepared["initial_state"]),
        "parent": prepared["parent"],
        "guard_source": prepared["guard_source"],
        "constraints": prepared["constraints"],
        "container": state.container.record() if state.container else None,
        "owned_hull_limit": state.hull_limit,
        "counts": dict(state.stats),
        "parent_geometry_replayed": False,
        "root_cap_join_checked": False,
        "existing_U_census_admission": False,
        "new_target_admission_proved": False,
        "mask_exclusion_proved": False,
        "global_optimality_proved": False,
        "independent_modules": True,
        "scope": (
            "conditional closed-guard contradiction only; "
            "no unconditional exclusion or admission"
        ),
    }


def consume(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    held = {
        field: read_json(finite.retained_path(document[field]), OUTPUT_LIMIT)[0]
        for field in (
            "finite_descriptor",
            "finite_certificate",
            "finite_replay",
            "centered_parent_receipt",
        )
    }
    prepared = prepare(document, deadline=deadline)
    child = document["child_object"]
    path = finite.retained_path(child["path"])
    frozen = finite.digest(path, CHILD_COMPRESSED_LIMIT, deadline)
    require(frozen == child["compressed_sha256"], "child compressed identity differs")
    result = replay(prepared, ChildStream(path, deadline), deadline=deadline)
    require(
        result["node_sha256"] == child["canonical_sha256"], "child canonical identity differs"
    )
    require(
        finite.digest(path, CHILD_COMPRESSED_LIMIT, deadline) == frozen,
        "child bytes changed during replay",
    )
    for field, raw in held.items():
        require(
            read_json(finite.retained_path(document[field]), OUTPUT_LIMIT)[0] == raw,
            "conditional premise changed across replay",
        )
    parent = prepared["parent"]
    require(
        hashlib.sha256(read_json(finite.retained_path(parent["h290_receipt"]))[0]).hexdigest()
        == parent["h290_receipt_sha256"],
        "H290 premise changed across replay",
    )
    for relative, expected in parent["compressed_sha256"].items():
        ceiling = (
            finite.SEED_LIMIT if Path(relative).name.startswith("seed-") else finite.NODE_LIMIT
        )
        require(
            finite.digest(finite.retained_path(relative), ceiling, deadline) == expected,
            "parent original bytes changed across child replay",
        )
    result["compressed_sha256"] = frozen
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--descriptor", type=Path, required=True)
    parser.add_argument("--max-seconds", type=float, default=300)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0:
        parser.error("max-seconds must be finite and positive")
    deadline = time.monotonic() + args.max_seconds
    try:
        require(
            not any(
                name == forbidden or name.startswith(forbidden + ".")
                for name in sys.modules
                for forbidden in (
                    *finite.FORBIDDEN,
                    "devtools.produce_n17_conditional_owned_hull",
                )
            ),
            "producer/kernel/root import in independent checker",
        )
        raw, document = read_json(args.descriptor)
        result = consume(document, deadline=deadline)
        require(read_json(args.descriptor)[0] == raw, "descriptor changed during replay")
    except IncompleteError as exc:
        result = {
            "schema": RECEIPT_SCHEMA,
            "status": "INCOMPLETE",
            "error": str(exc),
            "conditional_exclusion_proved": False,
        }
    except (ValueError, KeyError, TypeError, OSError, standing.VerificationError) as exc:
        result = {
            "schema": RECEIPT_SCHEMA,
            "status": "REFUSED",
            "error": str(exc),
            "conditional_exclusion_proved": False,
        }
    result.update(
        provenance=provenance(Path(__file__), Path(standing.__file__), Path(finite.__file__)),
        invocation={
            "argv": list(sys.argv if argv is None else argv),
            "interpreter": sys.executable,
        },
    )
    encoded = retained_json.dumps(result)
    if len(encoded.encode()) > OUTPUT_LIMIT:
        result = {
            "schema": RECEIPT_SCHEMA,
            "status": "INCOMPLETE",
            "error": "conditional report byte ceiling",
            "conditional_exclusion_proved": False,
        }
        encoded = retained_json.dumps(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(encoded + "\n")
    print(json.dumps({k: result.get(k) for k in ("schema", "status", "error")}))
    return 0 if result["status"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())
