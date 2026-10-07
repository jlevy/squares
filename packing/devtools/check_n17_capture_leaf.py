"""Exact conditional geometry predicates on a freshly replayed n17 leaf.

This adapter supports unconditional sequential nodes only. It admits no capture tree,
global coverage or census change. Original centred containment and the retained local
composition theorem are explicitly inherited premises, not proved by a descriptor.
Imports read no scientific inputs. All domains and orientation pieces are closed.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from devtools import audit_n17_endpoint_receipt as exact
from devtools import check_n17_capacity_one_cover as cover
from devtools import check_n17_widened_annulus_patch as patch
from devtools import check_n17_widened_apex as apex
from devtools import check_n17_widened_features as forcing
from devtools.check_n17_endpoint_feasibility import Box
from devtools.pilot_n17_capture import in_convex
from devtools.provenance import provenance
from sqpack import retained_json
from sqpack.hull_kernel import node, producer, sequential
from sqpack.hull_kernel.frame import (
    D4_ACTIONS,
    Frame,
    d4_matrix,
    induced_permutation,
    make_frame,
)
from sqpack.hull_kernel.geometry import Budget, IncompleteError
from sqpack.hull_kernel.rational import Q as KernelQ

SCHEMA = "n17-capture-leaf-domain/v1"
LABELS = tuple(range(1, 18))
ACTIVE = tuple(label for label in LABELS if label != 6)
LOCAL_POSITION, LOCAL_Q = Q(1, 5000), Q(1, 10000)
SCOPE = "conditional leaf geometry only; no capture tree, global admission or census change"
COMPOSITION = "docs/project/reviews/review-2026-10-02-n17-local-half-composition.md"


class OpenCoverage(exact.AuditError):
    """The descriptor does not retain a complete closed orientation cover."""


@dataclass(frozen=True)
class Leaf:
    """Geometry context produced by fresh replay; direct API callers supply that premise."""

    frame: Frame
    layout: exact.Layout
    rows: Mapping[int, Sequence[Mapping[str, Any]]]
    roles: Mapping[int, int]
    expected_roles: Mapping[int, int]
    action: str
    custody: Mapping[str, Any]


def magnitude(value: exact.Interval) -> Q:
    return max(abs(value[0]), abs(value[1]))


def matrix_vector(matrix: tuple[int, int, int, int], value: exact.Vector) -> exact.Vector:
    a, b, c, d = matrix
    return (
        exact.add(
            exact.multiply(exact.point(a), value[0]), exact.multiply(exact.point(b), value[1])
        ),
        exact.add(
            exact.multiply(exact.point(c), value[0]), exact.multiply(exact.point(d), value[1])
        ),
    )


def principal_half_angle(
    nominal: exact.Vector, interval: exact.Interval, action: str, quarter: int
) -> exact.Interval | None:
    """Enclose s/(1+c) over a full chart piece and root box, with no angle conversion."""
    lo, hi = interval
    exact.require(
        0 <= lo <= hi <= 1 and quarter in range(4), "invalid chart piece or quarter turn"
    )
    # Both chart coordinates are monotone on the producer's complete [0,1] chart.
    cosine = (Q(1) - hi * hi) / (1 + hi * hi), (Q(1) - lo * lo) / (1 + lo * lo)
    sine = 2 * lo / (1 + lo * lo), 2 * hi / (1 + hi * hi)
    axis = matrix_vector(d4_matrix(action), (cosine, sine))
    for _ in range(quarter):
        axis = exact.negate(axis[1]), axis[0]
    c = exact.dot(nominal, axis)
    s = exact.subtract(exact.multiply(nominal[0], axis[1]), exact.multiply(nominal[1], axis[0]))
    denominator = exact.add(exact.point(1), c)
    return None if denominator[0] <= 0 else exact.divide(s, denominator)


def closed_rows(rows: Sequence[Mapping[str, Any]]) -> None:
    cursor = Q(0)
    for item in rows:
        lo, hi = exact.read_interval(item["interval"])
        if cursor != lo or not lo < hi <= 1:
            raise OpenCoverage("missing, overlapping or open chart piece")
        cursor = hi
    if cursor != 1:
        raise OpenCoverage("orientation cover incomplete")


def physical_point(frame: Frame, raw: Sequence[str], action: str) -> exact.Vector:
    exact.require(len(raw) == 2, "centre vertex dimension differs")
    scale, centre = Q(str(frame.scale)), Q(str(frame.cap)) / 2
    value = tuple(exact.point(exact.rational(v) / scale - centre) for v in raw)
    transformed = matrix_vector(d4_matrix(action), (value[0], value[1]))
    return exact.add(transformed[0], exact.point(centre)), exact.add(
        transformed[1], exact.point(centre)
    )


def bounds(leaf: Leaf) -> dict[str, Any]:
    exact.require(leaf.action in D4_ACTIONS, "invalid D4 action")
    exact.require(set(leaf.roles) == set(LABELS), "missing or extra label")
    exact.require(
        all(type(owner) is int for owner in leaf.roles.values())
        and all(0 <= owner < len(leaf.frame.cells) for owner in leaf.roles.values())
        and len(set(leaf.roles.values())) == 17
        and set(leaf.roles.values()) == set(leaf.rows),
        "labels are not a complete owner bijection",
    )
    exact.require(
        leaf.custody.get("fresh_replay") is True, "missing fresh producer coverage custody"
    )
    exact.require(
        leaf.custody.get("original_container_premise") == "centred-C(S*)",
        "missing original container premise",
    )
    actions = [value for value in leaf.frame.actions if value.name == leaf.action]
    exact.require(
        len(actions) == 1 and actions[0].matrix == d4_matrix(leaf.action),
        "frame D4 identity differs",
    )
    action = actions[0]
    exact.require(
        action.permutation
        == induced_permutation(leaf.frame.cells, action.matrix, leaf.frame.cap / 2),
        "D4 cell permutation differs from exact geometry",
    )
    transported = {label: action.permutation[owner] for label, owner in leaf.roles.items()}
    if transported != dict(leaf.expected_roles):
        return {"status": "unresolved", "reason": "unsupported_assignment", "scope": SCOPE}
    sigma = exact.divide(
        exact.subtract(exact.point(Q(str(leaf.frame.cap))), leaf.layout.side), exact.point(2)
    )
    values: dict[str, list[exact.Interval]] = {}
    angle_pieces: list[dict[str, Any]] = []
    square6 = True
    any_empty = False
    for label in LABELS:
        owner = leaf.roles[label]
        closed_rows(leaf.rows[owner])
        live = [item for item in leaf.rows[owner] if item["residual_polygons"]]
        any_empty |= not live
        for index, item in enumerate(leaf.rows[owner]):
            if not item["residual_polygons"]:
                continue
            for polygon in item["residual_polygons"]:
                exact.require(bool(polygon), "empty live polygon")
                for vertex in polygon:
                    physical = physical_point(leaf.frame, vertex, leaf.action)
                    if label == 6:
                        # Closed convex-cell membership, including its boundary.
                        square6 &= in_convex(
                            leaf.frame.cell(leaf.expected_roles[6]),
                            (KernelQ(physical[0][0]), KernelQ(physical[1][0])),
                        )
                        continue
                    local = tuple(exact.subtract(value, sigma) for value in physical)
                    delta = exact.difference((local[0], local[1]), leaf.layout.centres[label])
                    if label == 5:
                        coordinates = {"eta5": delta[1], "a": exact.negate(delta[0])}
                    elif label in {11, 13}:
                        slide = exact.dot(leaf.layout.axes["v"], delta)
                        coordinates = {
                            f"u{label}": exact.dot(leaf.layout.axes["u"], delta),
                            "b" if label == 11 else "z": exact.negate(slide)
                            if label == 11
                            else slide,
                        }
                    else:
                        coordinates = {f"xi{label}": delta[0], f"eta{label}": delta[1]}
                    for name, value in coordinates.items():
                        values.setdefault(name, []).append(value)
            if label != 6:
                axis_name = "u" if 9 <= label <= 14 else "p" if label == 16 else "ex"
                candidates = [
                    (magnitude(value), quarter, value)
                    for quarter in range(4)
                    if (
                        value := principal_half_angle(
                            leaf.layout.axes[axis_name],
                            exact.read_interval(item["interval"]),
                            leaf.action,
                            quarter,
                        )
                    )
                    is not None
                ]
                if not candidates:
                    return {
                        "status": "unresolved",
                        "reason": "principal_chart_denominator",
                        "scope": SCOPE,
                    }
                _, quarter, value = min(candidates)
                angle_pieces.append(
                    {
                        "label": label,
                        "row": index,
                        "reference": item["reference"],
                        "interval": item["interval"],
                        "quarter_turn": quarter,
                        "q": forcing.encode(value),
                    }
                )
                values.setdefault(f"q{label}", []).append(value)
    if any_empty:
        return {
            "status": "unresolved",
            "reason": "empty_owner_requires_exclusion_consumer",
            "scope": SCOPE,
        }
    intervals = {
        name: (min(v[0] for v in pieces), max(v[1] for v in pieces))
        for name, pieces in values.items()
    }
    names = apex.position_names()
    exact.require(
        set(intervals) == {*names, "a", "b", "z", *(f"q{i}" for i in ACTIVE)},
        "coordinate inventory differs",
    )
    return {
        "status": "bounded",
        "intervals": {name: forcing.encode(value) for name, value in intervals.items()},
        "angle_pieces": angle_pieces,
        "square6_S2": square6,
        "a_floor_from_containment": leaf.custody.get("root_layout_x5_identity") == "x5*=S*-1/2",
        "scope": SCOPE,
    }


def predicates(
    report: dict[str, Any],
    *,
    apex_q0: Q | None = None,
    patch_box: Sequence[exact.Interval] | None = None,
) -> dict[str, Any]:
    if report["status"] != "bounded":
        return report
    intervals = {
        name: exact.read_interval(value) for name, value in report["intervals"].items()
    }
    position = max(magnitude(intervals[name]) for name in apex.position_names())
    angle = max(magnitude(intervals[f"q{i}"]) for i in ACTIVE)
    effective_a = intervals["a"]
    if report.get("a_floor_from_containment") is True:
        effective_a = max(effective_a[0], Q(0)), effective_a[1]
    direct_sliders = effective_a[0] <= effective_a[1] and all(
        low <= intervals[name][0] <= intervals[name][1] <= high
        for name, (low, high) in zip(("b", "z"), forcing.DOMAIN[1:], strict=True)
    )
    direct_sliders &= Q(0) <= effective_a[0] <= effective_a[1] <= Q(1, 4)
    local = position <= LOCAL_POSITION and angle <= LOCAL_Q and report["square6_S2"]
    wide = position <= patch.RHO and angle <= patch.OUTER and direct_sliders
    apex_terminal = wide and report["square6_S2"] and apex_q0 is not None and angle <= apex_q0
    patch_exclusion = (
        wide
        and report["square6_S2"]
        and patch_box is not None
        and len(patch_box) == 16
        and all(
            lo <= intervals[f"q{i}"][0] <= intervals[f"q{i}"][1] <= hi
            for i, (lo, hi) in zip(ACTIVE, patch_box, strict=True)
        )
    )
    status = (
        "local_terminal"
        if local
        else "apex_terminal"
        if apex_terminal
        else "patch_exclusion"
        if patch_exclusion
        else "wide_domain_only"
        if wide
        else "unresolved"
    )
    return {
        **report,
        "status": status,
        "conditional_on": ["centred-C(S*)", COMPOSITION, "fresh producer pose-cover replay"],
        "predicates": {
            "local_terminal": local,
            "wide_domain": wide,
            "apex_terminal": apex_terminal,
            "patch_exclusion": patch_exclusion,
        },
        "effective_a_interval": forcing.encode(effective_a),
        "global_admission_proved": False,
        "capture_tree_proved": False,
    }


def retained_path(value: Any) -> Path:
    exact.require(type(value) is str, "missing source reference")
    path = (exact.REPO / value).resolve()
    exact.require(
        not Path(value).is_absolute() and path.is_relative_to(exact.REPO),
        "source reference escapes repository",
    )
    return path


def load_leaf(document: dict[str, Any], *, deadline: float, max_nodes: int) -> Leaf:
    exact.require(document["schema"] == SCHEMA, "wrong leaf schema")
    exact.require(
        document["state_encoding"] == "sorted-cell-indices/v1", "unsupported mask encoding"
    )
    design = cover.DESIGNS[document["cover_design"]]
    cells = cover.build_cover(design)
    exact.require(
        document["cells"] == [cover.cell_record(cell) for cell in cells],
        "declared closed cells differ",
    )
    root_inputs, layout, _ = forcing.load_root()
    cap, length, scale = (exact.rational(document[name]) for name in ("U", "L", "B"))
    inner = exact.rational(document["capture_cap"])
    exact.require(
        cap == cover.U
        and length > 0
        and scale == length / cap
        and layout.side[1] <= inner <= cap,
        "wrong physical cap or field scale",
    )
    frame = make_frame(
        name=f"n17-{design.name}",
        cap=cap,
        length=length,
        cells=[cell.vertices for cell in cells],
        cell_names=[cell.name for cell in cells],
        occupancy=17,
        action_names=D4_ACTIONS,
        capture_cap=inner,
    )
    state: list[Any] = document["state"]
    exact.require(
        type(state) is list
        and all(type(i) is int for i in state)
        and len(state) == 17
        and state == sorted(set(state))
        and all(0 <= i < len(cells) for i in state),
        "invalid state indices",
    )
    exact.require(
        set(document["label_to_owner"]) == set(map(str, LABELS)), "noncanonical label IDs"
    )
    roles = {int(key): owner for key, owner in document["label_to_owner"].items()}
    exact.require(
        set(roles) == set(LABELS) and len(document["label_to_owner"]) == 17,
        "label identities differ",
    )
    seed_path, node_path, receipt_path = (
        retained_path(document[name]) for name in ("seed", "node", "producer_receipt")
    )
    seed_packet, node_packet, receipt = (
        exact.decode(exact.read_bytes(path)) for path in (seed_path, node_path, receipt_path)
    )
    exact.require(
        receipt["replay"]["status"] == "PASS_REPLAYED"
        and receipt["replay"]["final_state_agrees"] is True
        and receipt["node_sha256"] == producer.content_sha256(node_packet)
        and receipt["seed_sha256"] == producer.content_sha256(seed_packet),
        "producer receipt/source custody differs",
    )
    budget = Budget(deadline, max_nodes)
    seed = node.admit_seed(
        frame,
        seed_packet,
        mask=state,
        bins=seed_packet["bins"],
        budget=budget,
        allow_empty_groups=True,
    )
    trace = sequential.replay_sequential(
        frame,
        node_packet,
        seed,
        mask=state,
        seed_sha256=producer.content_sha256(seed_packet),
        budget=budget,
        cover="indexed",
    )
    r = root_inputs["root_inclusion_box_used"]
    endpoint = cover.endpoint(*(Box(*exact.read_interval(value)) for value in r))
    assignment = cover.family_state(cells, endpoint, cover.ENDPOINT)
    exact.require(assignment["one_state"], "endpoint assignment unavailable")
    by_name = {cell.name: i for i, cell in enumerate(cells)}
    expected = {item["label"]: by_name[item["cell"]] for item in assignment["squares"]}
    exact.require(cells[expected[6]].name == "side-S2", "square6 cell premise differs")
    exact.require(
        document["original_container_premise"] == "centred-C(S*)"
        and document["composition_premise"] == COMPOSITION,
        "missing conditional theorem premise custody",
    )
    return Leaf(
        frame,
        layout,
        trace.rows,
        roles,
        expected,
        document["action"],
        {
            "fresh_replay": True,
            "original_container_premise": document["original_container_premise"],
            "root": root_inputs,
            "seed": document["seed"],
            "node": document["node"],
            "producer_receipt": document["producer_receipt"],
            "composition_premise": COMPOSITION,
            "root_layout_x5_identity": "x5*=S*-1/2",
            "cover_design": design.name,
            "state": state,
            "state_encoding": document["state_encoding"],
            "U": document["U"],
            "L": document["L"],
            "B": document["B"],
            "capture_cap": document["capture_cap"],
            "action": document["action"],
            "D4_matrix": list(d4_matrix(document["action"])),
            "label_to_owner": document["label_to_owner"],
            "expected_label_to_cell": {
                str(label): cells[owner].name for label, owner in expected.items()
            },
            "unit_transform": "raw/B; D4 about U/2; subtract exact-root sigma",
            "orientation_convention": "transformed axis; second axis is positive J(axis)",
        },
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--leaf", type=Path, required=True)
    parser.add_argument("--features", type=Path)
    parser.add_argument("--apex", type=Path)
    parser.add_argument("--patch", type=Path)
    parser.add_argument("--max-seconds", type=float, default=30)
    parser.add_argument("--max-nodes", type=int, default=200000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        exact.require(
            math.isfinite(args.max_seconds) and args.max_seconds > 0 and args.max_nodes > 0,
            "invalid replay budget",
        )
        leaf = load_leaf(
            exact.decode(exact.read_bytes(args.leaf)),
            deadline=time.monotonic() + args.max_seconds,
            max_nodes=args.max_nodes,
        )
        q0, angle_box = None, None
        terminal_inputs: dict[str, Any] = {"features": None, "apex": None, "patch": None}
        if args.apex is not None:
            exact.require(args.features is not None, "apex requires features")
            accepted = exact.decode(exact.read_bytes(args.apex))
            checked_apex = apex.check(accepted, args.features)
            q0 = exact.rational(accepted["q0"])
            terminal_inputs["features"] = str(args.features.resolve().relative_to(exact.REPO))
            terminal_inputs["apex"] = {
                "path": str(args.apex.resolve().relative_to(exact.REPO)),
                "q0": str(q0),
                "checked": checked_apex,
            }
        if args.patch is not None:
            exact.require(
                args.features is not None and args.apex is not None,
                "patch requires feature and apex joins",
            )
            accepted = exact.decode(exact.read_bytes(args.patch))
            checked = patch.check(accepted, cast(Path, args.features), cast(Path, args.apex))
            exact.require(
                checked["positive_patch_certified"] is True,
                "patch lacks strict positive certificate",
            )
            angle_box = tuple(
                exact.read_interval(value) for value in accepted["attempts"][-1]["angle_box"]
            )
            terminal_inputs["patch"] = {
                "path": str(args.patch.resolve().relative_to(exact.REPO)),
                "angle_box": [forcing.encode(value) for value in angle_box],
                "checked": checked,
            }
        report = {
            "schema": SCHEMA,
            "verification_passed": True,
            "custody": dict(leaf.custody),
            "terminal_inputs": terminal_inputs,
            **predicates(bounds(leaf), apex_q0=q0, patch_box=angle_box),
        }
    except (OpenCoverage, IncompleteError) as error:
        report = {
            "schema": SCHEMA,
            "status": "incomplete",
            "verification_passed": False,
            "error": str(error),
            "scope": SCOPE,
        }
    except (ValueError, OSError, KeyError, TypeError, IndexError) as error:
        report = {
            "schema": SCHEMA,
            "status": "refused",
            "verification_passed": False,
            "error": str(error),
            "scope": SCOPE,
        }
    report["provenance"] = provenance(
        Path(__file__),
        Path(forcing.__file__),
        Path(apex.__file__),
        Path(patch.__file__),
        Path(exact.__file__),
        Path(cover.__file__),
        Path(node.__file__),
        Path(sequential.__file__),
        Path(producer.__file__),
        Path(forcing.root.__file__),
        Path(forcing.core.__file__),
        Path(apex.endpoint.__file__),
        Path(__file__).with_name("pilot_n17_capture.py"),
        Path(__file__).parents[1] / "src/sqpack/hull_kernel/frame.py",
        Path(__file__).parents[1] / "src/sqpack/hull_kernel/geometry.py",
    )
    report["global_admission_proved"] = False
    report["capture_tree_proved"] = False
    if args.output is not None:
        args.output.write_text(retained_json.dumps(report))
    print(json.dumps(report))
    return 0 if report["verification_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
