"""Exact conditional geometry predicates on a freshly replayed n17 leaf.

This adapter supports unconditional sequential nodes only. It admits no capture tree,
global coverage or census change. Original centred containment and the retained local
composition theorem are explicitly inherited premises, not proved by a descriptor.
Imports read no scientific inputs. All domains and orientation pieces are closed.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import subprocess
import sys
import tempfile
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from devtools import audit_n17_endpoint_receipt as exact
from devtools import check_n17_capacity_one_cover as cover
from devtools import check_n17_endpoint_prefix as prefix
from devtools import check_n17_subpattern as saved
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
from sqpack.hull_kernel.induction import wall_lines
from sqpack.hull_kernel.rational import Q as KernelQ

SCHEMA = "n17-capture-leaf-domain/v1"
LABELS = tuple(range(1, 18))
ACTIVE = tuple(label for label in LABELS if label != 6)
LOCAL_POSITION, LOCAL_Q = Q(1, 5000), Q(1, 10000)
SCOPE = "conditional leaf geometry only; no capture tree, global admission or census change"
COMPOSITION = "docs/project/reviews/review-2026-10-02-n17-local-half-composition.md"
SEED_DECODED_LIMIT = 10 * 1024 * 1024
NODE_DECODED_LIMIT = 64 * 1024 * 1024


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


def bounds(leaf: Leaf, *, deadline: float | None = None) -> dict[str, Any]:
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
                    if deadline is not None and time.monotonic() >= deadline:
                        raise IncompleteError("leaf geometry wall ceiling")
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
                    if label == 9:
                        values.setdefault("v9", []).append(
                            exact.dot(leaf.layout.axes["v"], delta)
                        )
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
        set(intervals) == {*names, "a", "b", "z", "v9", *(f"q{i}" for i in ACTIVE)},
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


def bounded_gzip(path: Path, limit: int, *, deadline: float, retain: bool = False) -> bytes:
    """Read at most limit decoded bytes; never expand an unbounded gzip object."""
    total, pieces = 0, []
    with gzip.open(path, "rb") as stream:
        while True:
            if time.monotonic() >= deadline:
                raise IncompleteError("saved-object loading wall ceiling")
            piece = stream.read(min(saved.STREAM_CHUNK, limit - total + 1))
            if not piece:
                break
            total += len(piece)
            exact.require(total <= limit, "saved gzip decoded byte ceiling")
            if retain:
                pieces.append(piece)
    return b"".join(pieces)


def file_digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def wall_normalization(
    frame: Frame,
    seed: dict[str, Any],
    *,
    deadline: float | None = None,
) -> dict[str, Any]:
    """Check the affine wall coefficients and every declared seed-row wall."""
    exact.require(frame.capture_cap is None, "saved prefix must retain original cap None")
    normalized = replace(frame, capture_cap=frame.cap)
    # field_centre_bounds is affine in h; agreement at 0 and 1 binds both coefficients.
    exact.require(
        all(
            frame.field_centre_bounds(h) == normalized.field_centre_bounds(h)
            for h in (KernelQ(0), KernelQ(1))
        )
        and frame.cells == normalized.cells
        and frame.scale == normalized.scale
        and frame.actions == normalized.actions,
        "normalized field wall coefficients differ",
    )
    checked = 0
    for rows in seed["cells"].values():
        for row in rows:
            if deadline is not None and time.monotonic() >= deadline:
                raise IncompleteError("seed wall normalization ceiling")
            lo, hi = (KernelQ(value) for value in row["interval"])
            exact.require(
                wall_lines(frame, lo, hi) == wall_lines(normalized, lo, hi),
                "normalized seed row walls differ",
            )
            checked += 1
    return {
        "original_capture_cap": None,
        "normalized_inner_cap": str(frame.cap),
        "affine_field_coefficients_equal": True,
        "affine_formula": "offset=0; field bounds=(B*h, B*(U-h))",
        "seed_wall_rows_checked": checked,
    }


def fresh_saved_replay(directory: Path, seconds: float) -> dict[str, Any]:
    exact.require(math.isfinite(seconds) and seconds > 0, "invalid fresh replay ceiling")
    command = [
        sys.executable,
        "-m",
        "devtools.check_n17_subpattern",
        "--check-saved",
        str(directory),
        "--cover",
        "indexed",
        "--max-seconds",
        str(seconds),
    ]
    with tempfile.TemporaryDirectory(prefix="capture-leaf-replay-") as scratch:
        output, errors = Path(scratch) / "stdout.json", Path(scratch) / "stderr.log"
        try:
            with output.open("wb") as stdout, errors.open("wb") as stderr:
                execution = subprocess.run(
                    command,
                    cwd=exact.REPO / "packing",
                    stdout=stdout,
                    stderr=stderr,
                    timeout=seconds,
                    check=False,
                )
        except subprocess.TimeoutExpired as error:
            raise IncompleteError("fresh saved replay wall ceiling") from error
        result = exact.decode(exact.read_bytes(output))
        if result.get("status") == "INCOMPLETE":
            raise IncompleteError("fresh saved replay incomplete")
        exact.require(execution.returncode == 0, "fresh saved replay refused")
    return {"command": command, "exit_code": execution.returncode, "receipt": result}


def load_saved_prefix(
    document: dict[str, Any],
    frame: Frame,
    *,
    deadline: float,
    max_nodes: int,
    replay_seconds: float,
) -> tuple[Mapping[int, Sequence[Mapping[str, Any]]], dict[str, Any]]:
    exact.require(
        frame.scale == 1
        and document["action"] == "r0"
        and type(document["expected_steps"]) is int
        and document["expected_steps"] == 1,
        "unsupported first saved-prefix frame, action or step count",
    )
    directory = retained_path(document["saved_objects"])
    seed_path, node_path = saved.saved_files(directory)
    exact.require(
        seed_path.resolve().parent == directory.resolve()
        and node_path.resolve().parent == directory.resolve()
        and seed_path.stat().st_size <= SEED_DECODED_LIMIT
        and node_path.stat().st_size <= NODE_DECODED_LIMIT,
        "saved object reference or compressed byte ceiling differs",
    )
    frozen_bytes = {str(path): file_digest(path) for path in (seed_path, node_path)}
    seed_packet = exact.decode(
        bounded_gzip(
            seed_path,
            SEED_DECODED_LIMIT,
            deadline=deadline,
            retain=True,
        )
    )
    bounded_gzip(node_path, NODE_DECODED_LIMIT, deadline=deadline)
    seed_id = producer.content_sha256(seed_packet)
    exact.require(seed_id == document["seed_sha256"], "saved seed identity differs")
    normalization = wall_normalization(frame, seed_packet, deadline=deadline)
    packet, steps = saved.stream_node(node_path)
    exact.require(
        packet.get("parent") is None
        and packet.get("guard_source") is None
        and packet.get("constraints") == [],
        "saved prefix has unsupported guard or ancestry",
    )
    budget = Budget(deadline, max_nodes)
    seed = node.admit_seed(
        frame,
        seed_packet,
        mask=document["state"],
        bins=seed_packet["bins"],
        budget=budget,
        allow_empty_groups=True,
    )
    trace = sequential.replay_sequential(
        frame,
        packet,
        seed,
        mask=document["state"],
        seed_sha256=seed_id,
        budget=budget,
        cover="indexed",
    )
    exact.require(
        steps.content_sha256 == document["node_sha256"]
        and len(trace.steps) == 1
        and trace.closure is None,
        "saved prefix identity, complete EOF or stall step count differs",
    )
    source = exact.decode(exact.read_bytes(retained_path(document["producer_receipt"])))
    exact.require(
        source["status"] == "PASS_ENDPOINT_PREFIX"
        and source["control_passed"] is True
        and source["seed_sha256"] == seed_id
        and source["node_sha256"] == steps.content_sha256
        and source["complete_owner_updates"] == 1
        and source["closure"] is None
        and exact.exact_structure(source["inputs"]["root"], document["root"]),
        "saved prefix producer receipt custody differs",
    )
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise IncompleteError("parent leaf ceiling before fresh replay")
    replay = fresh_saved_replay(directory, min(replay_seconds, remaining))
    checked = replay["receipt"]
    exact.require(
        checked["status"] == "PASS_SAVED_STALL"
        and checked["closure"] is None
        and checked["producer_imported"] is False
        and checked["steps_checked"] == 1
        and checked["seed_sha256"] == seed_id
        and checked["node_sha256"] == steps.content_sha256
        and checked["frame"] == frame.name
        and checked["mask"] == document["state"]
        and checked["cells"] == [frame.cell_names[i] for i in document["state"]]
        and checked["bins"] == seed_packet["bins"]
        and checked["cover_backend"] == "indexed",
        "fresh saved prefix receipt/source identity differs",
    )
    exact.require(
        frozen_bytes == {str(path): file_digest(path) for path in (seed_path, node_path)},
        "saved objects changed across bounded loading and fresh replay",
    )
    return trace.rows, {
        "saved_objects": document["saved_objects"],
        "seed_sha256": seed_id,
        "node_sha256": steps.content_sha256,
        "fresh_full_replay": replay,
        "wall_normalization": normalization,
        "seed_decoded_limit": SEED_DECODED_LIMIT,
        "node_decoded_limit": NODE_DECODED_LIMIT,
    }


def load_leaf(
    document: dict[str, Any],
    *,
    deadline: float,
    max_nodes: int,
    fresh_replay_seconds: float = 60,
) -> Leaf:
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
    original_inner = document["capture_cap"]
    inner = cap if original_inner is None else exact.rational(original_inner)
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
        capture_cap=None if original_inner is None else inner,
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
    saved_custody: dict[str, Any] = {}
    if "saved_objects" in document:
        exact.require(
            exact.exact_structure(document["root"], root_inputs),
            "saved descriptor accepted root differs",
        )
        rows, saved_custody = load_saved_prefix(
            document,
            frame,
            deadline=deadline,
            max_nodes=max_nodes,
            replay_seconds=fresh_replay_seconds,
        )
    else:
        seed_path, node_path, receipt_path = (
            retained_path(document[name]) for name in ("seed", "node", "producer_receipt")
        )
        seed_packet, node_packet, receipt = (
            exact.decode(exact.read_bytes(path))
            for path in (seed_path, node_path, receipt_path)
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
        rows = trace.rows
    r = root_inputs["root_inclusion_box_used"]
    endpoint = cover.endpoint(*(Box(*exact.read_interval(value)) for value in r))
    assignment = cover.family_state(cells, endpoint, cover.ENDPOINT)
    exact.require(assignment["one_state"], "endpoint assignment unavailable")
    by_name = {cell.name: i for i, cell in enumerate(cells)}
    expected = {item["label"]: by_name[item["cell"]] for item in assignment["squares"]}
    exact.require(cells[expected[6]].name == "side-S2", "square6 cell premise differs")
    if saved_custody:
        saved_custody["endpoint_retention"] = saved_endpoint_retention(
            frame,
            roles,
            expected,
            root_inputs,
            rows,
        )
    exact.require(
        document["original_container_premise"] == "centred-C(S*)"
        and document["composition_premise"] == COMPOSITION,
        "missing conditional theorem premise custody",
    )

    return Leaf(
        frame,
        layout,
        rows,
        roles,
        expected,
        document["action"],
        {
            "fresh_replay": True,
            "original_container_premise": document["original_container_premise"],
            "root": root_inputs,
            "seed": document.get("seed"),
            "node": document.get("node"),
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
            **saved_custody,
        },
    )


def saved_endpoint_retention(
    frame: Frame,
    roles: Mapping[int, int],
    expected: Mapping[int, int],
    root_inputs: dict[str, Any],
    rows: Mapping[int, Sequence[Mapping[str, Any]]],
) -> dict[str, Any]:
    endpoint_frame, poses, endpoint_inputs = prefix.load_endpoint()
    exact.require(
        frame.cap == endpoint_frame.cap
        and frame.length == endpoint_frame.length
        and frame.cells == endpoint_frame.cells
        and roles == expected
        and exact.exact_structure(root_inputs, endpoint_inputs["root"]),
        "saved prefix endpoint frame/root/label assignment differs",
    )
    checked = prefix.endpoint_check(poses, rows)
    exact.require(checked["held"] is True, "full-root endpoint not retained")
    return checked


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--leaf", type=Path, required=True)
    parser.add_argument("--features", type=Path)
    parser.add_argument("--apex", type=Path)
    parser.add_argument("--patch", type=Path)
    parser.add_argument("--max-seconds", type=float, default=30)
    parser.add_argument("--max-nodes", type=int, default=200000)
    parser.add_argument("--fresh-replay-seconds", type=float, default=60)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        exact.require(
            math.isfinite(args.max_seconds)
            and args.max_seconds > 0
            and args.max_nodes > 0
            and math.isfinite(args.fresh_replay_seconds)
            and args.fresh_replay_seconds > 0,
            "invalid replay budget",
        )
        deadline = time.monotonic() + args.max_seconds
        leaf = load_leaf(
            exact.decode(exact.read_bytes(args.leaf)),
            deadline=deadline,
            max_nodes=args.max_nodes,
            fresh_replay_seconds=args.fresh_replay_seconds,
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
        bounded = bounds(leaf, deadline=deadline)
        if leaf.custody.get("saved_objects") is not None:
            exact.require(
                bounded["status"] == "bounded"
                and all(
                    lo <= 0 <= hi
                    for lo, hi in map(exact.read_interval, bounded["intervals"].values())
                ),
                "saved endpoint coordinate intervals do not contain zero",
            )
        report = {
            "schema": SCHEMA,
            "verification_passed": True,
            "custody": dict(leaf.custody),
            "terminal_inputs": terminal_inputs,
            **predicates(bounded, apex_q0=q0, patch_box=angle_box),
        }
    except (OpenCoverage, IncompleteError) as error:
        report = {
            "schema": SCHEMA,
            "status": "incomplete",
            "verification_passed": False,
            "error": str(error),
            "scope": SCOPE,
        }
    except (ValueError, OSError, EOFError, KeyError, TypeError, IndexError) as error:
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
        Path(saved.__file__),
        Path(prefix.__file__),
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
