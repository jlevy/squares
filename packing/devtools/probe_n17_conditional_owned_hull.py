"""Reconstruct a finite conditional-owned-hull gate from an accepted H290 domain.

The accepted receipt is a premise, not a new geometry replay. A clean fresh
checker reconstructs the three exact polygons; no propagation is performed.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import re
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from devtools import verify_n17_kernel_certificate as standing
from devtools.provenance import provenance
from sqpack import retained_json

REPO = Path(__file__).resolve().parents[2]
SCHEMA = "n17-conditional-owned-hull-gate/v1"
U = Q(1169, 250)
V = Q(935106018721, 200000000000)
GUARDS = {"all": (Q(0), Q(1)), "target": (Q(13, 32), Q(27, 64)), "endpoint": (Q(0), Q(1, 64))}
MARGIN = Q(1, 2**20)
GAIN = Q(1, 1024)
AREA = Q(1, 2**20)
DIRECTIONS = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))
CARDINAL = DIRECTIONS[::2]
JSON_LIMIT = SEED_LIMIT = 10 << 20
NODE_LIMIT = 512 << 20
DECODED_LIMIT = 2 << 30
SLICE_LIMIT = OUTPUT_LIMIT = 64 << 20
VERTEX_LIMIT = 128
BIT_LIMIT = 4096
FORBIDDEN = (
    "sqpack.hull_kernel",
    "devtools.check_n17_subpattern",
    "devtools.pilot_n17_capture",
    "devtools.check_n17_capture_checkpoint",
    "devtools.check_n17_root_certificate",
    "devtools.check_n17_capture_cap",
)
Point = tuple[Q, Q]


class IncompleteError(Exception):
    """A frozen resource ceiling prevented a finite result."""


def require(condition: bool, message: str) -> None:  # noqa: FBT001
    if not condition:
        raise ValueError(message)


def tick(deadline: float) -> None:
    if time.monotonic() >= deadline:
        raise IncompleteError("conditional gate wall ceiling")


def checked(value: Q) -> Q:
    if max(abs(value.numerator).bit_length(), value.denominator.bit_length()) > BIT_LIMIT:
        raise IncompleteError("conditional gate rational bit ceiling")
    return value


def rational(value: Any) -> Q:
    require(type(value) is str, "exact rational string required")
    if len(value) > 2600:
        raise IncompleteError("conditional gate rational string ceiling")
    rational_grammar(value)
    result = checked(Q(value))
    require(str(result) == value, "noncanonical exact rational")
    return result


def rational_grammar(value: Any) -> None:
    """Check opaque premise syntax without integer/Fraction allocation or a bit cap."""
    require(type(value) is str, "exact rational string required")
    require(
        re.fullmatch(r"-?(?:0|[1-9]\d*)(?:/[1-9]\d*)?", value) is not None,
        "canonical integer/fraction grammar required",
    )


def opaque_polygon(value: Any) -> None:
    require(type(value) is list, "opaque polygon list required")
    for p in value:
        require(type(p) is list and len(p) == 2, "opaque polygon point shape")
        rational_grammar(p[0])
        rational_grammar(p[1])


def rational_tree(value: Any) -> None:
    """Bound numeric values retained from the admitted premise as well as new geometry."""
    if type(value) is str and re.fullmatch(r"-?\d+(?:/\d+)?", value):
        if len(value) > 2600:
            raise IncompleteError("conditional gate retained rational string ceiling")
        checked(Q(value))
    elif type(value) is int:
        checked(Q(value))
    elif type(value) is float:
        require(math.isfinite(value), "nonfinite retained metadata")
    elif type(value) is dict:
        for member in value.values():
            rational_tree(member)
    elif type(value) is list:
        for member in value:
            rational_tree(member)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def identity(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON member")
        result[key] = value
    return result


def integer(value: str) -> int:
    require(len(value) <= 1234, "oversized JSON integer")
    return int(value)


def nonfinite(_value: str) -> Any:
    raise ValueError("nonfinite JSON number")


def decode(raw: bytes) -> dict[str, Any]:
    result = json.loads(
        raw, object_pairs_hook=unique, parse_int=integer, parse_constant=nonfinite
    )
    require(type(result) is dict, "JSON object required")
    return result


def read_json(path: Path, ceiling: int = JSON_LIMIT) -> tuple[bytes, dict[str, Any]]:
    with path.open("rb") as stream:
        raw = stream.read(ceiling + 1)
    if len(raw) > ceiling:
        raise IncompleteError("conditional gate receipt/input byte ceiling")
    return raw, decode(raw)


def retained_path(value: Any) -> Path:
    require(type(value) is str and not Path(value).is_absolute(), "invalid retained path")
    path = (REPO / value).resolve()
    require(path.is_relative_to(REPO), "retained path escapes repository")
    return path


def digest(path: Path, ceiling: int, deadline: float) -> str:
    result, count = hashlib.sha256(), 0
    with path.open("rb") as stream:
        while True:
            tick(deadline)
            block = stream.read(min(1 << 20, ceiling - count + 1))
            if not block:
                return result.hexdigest()
            count += len(block)
            if count > ceiling:
                raise IncompleteError("conditional gate compressed byte ceiling")
            result.update(block)


def seed_decode(path: Path, deadline: float) -> dict[str, Any]:
    with gzip.open(path, "rb") as stream:
        tick(deadline)
        raw = stream.read(SEED_LIMIT + 1)
    if len(raw) > SEED_LIMIT:
        raise IncompleteError("conditional gate decoded seed byte ceiling")
    tick(deadline)
    return decode(raw)


class BoundedNode(standing.NodeStream):
    """Use the standing canonical EOF parser with bounded decompression."""

    def __init__(self, path: Path, deadline: float) -> None:
        self.deadline, self.decoded, self.wrapped = deadline, 0, False
        self.member: str | None = None
        super().__init__(path)

    def _name(self) -> str:
        name = super()._name()
        self.member = name
        return name

    def _fill(self) -> None:
        if not self.wrapped:
            source = self._source

            def pieces() -> Any:
                for piece in source:
                    tick(self.deadline)
                    self.decoded += len(piece.encode())
                    if self.decoded > DECODED_LIMIT:
                        raise IncompleteError("conditional gate decoded node byte ceiling")
                    yield piece

            self._source = pieces()
            self.wrapped = True
        tick(self.deadline)
        super()._fill()
        if self.member == "final_state" and len(self._text[self._at :].encode()) > SLICE_LIMIT:
            raise IncompleteError("conditional gate final-state slice byte ceiling")


def polygon(value: Any) -> list[Point]:
    require(type(value) is list, "polygon list required")
    result = []
    for p in value:
        require(type(p) is list and len(p) == 2, "polygon point shape")
        result.append((rational(p[0]), rational(p[1])))
    return hull(result, bounded=False)


def cross(o: Point, a: Point, b: Point) -> Q:
    return checked(
        checked((a[0] - o[0]) * (b[1] - o[1])) - checked((a[1] - o[1]) * (b[0] - o[0]))
    )


def hull(points: list[Point], *, bounded: bool = True) -> list[Point]:
    points = sorted(set(points))
    if len(points) <= 2:
        return points
    halves: list[list[Point]] = []
    for sequence in (points, list(reversed(points))):
        half: list[Point] = []
        for p in sequence:
            while len(half) >= 2 and cross(half[-2], half[-1], p) <= 0:
                half.pop()
            half.append(p)
        halves.append(half[:-1])
    result = halves[0] + halves[1]
    if bounded and len(result) > VERTEX_LIMIT:
        raise IncompleteError("conditional gate intermediate hull vertex ceiling")
    return result


def dot(p: Point, n: tuple[int, int] | Point) -> Q:
    return checked(checked(p[0] * n[0]) + checked(p[1] * n[1]))


def clip(points: list[Point], a: Q, b: Q, c: Q, *, bounded: bool = True) -> list[Point]:
    result = []
    for i, p in enumerate(points):
        q = points[(i + 1) % len(points)]
        fp, fq = checked(dot(p, (a, b)) - c), checked(dot(q, (a, b)) - c)
        if fp <= 0:
            result.append(p)
        if fp < 0 < fq or fq < 0 < fp:
            ratio = checked(fp / checked(fp - fq))
            result.append(
                (
                    checked(p[0] + checked(ratio * checked(q[0] - p[0]))),
                    checked(p[1] + checked(ratio * checked(q[1] - p[1]))),
                )
            )
    return hull(result, bounded=bounded)


def serial(points: list[Point]) -> list[list[str]]:
    return [[str(x), str(y)] for x, y in points]


def trig(t: Q) -> Point:
    denominator = checked(1 + checked(t * t))
    return checked((1 - checked(t * t)) / denominator), checked(2 * t / denominator)


def reconstruct(
    rows: list[dict[str, Any]], guard: tuple[Q, Q], deadline: float
) -> dict[str, Any]:
    kernel = [(Q(0), Q(0)), (U, Q(0)), (U, U), (Q(0), U)]
    joins = []
    plane_count = 0
    for index, row in enumerate(rows):
        tick(deadline)
        lo, hi = map(rational, row["interval"])
        lo, hi = max(lo, guard[0]), min(hi, guard[1])
        if lo > hi:
            continue
        centres = hull(
            [p for poly in row["residual_polygons"] for p in polygon(poly)], bounded=False
        )
        clo, shi = trig(lo)
        chi, slo = trig(hi)
        half_extent = checked(min(checked(clo + shi), checked(chi + slo)) / 2)
        lower = checked((U - V) / 2 + half_extent)
        upper = checked(U - (U - V) / 2 - half_extent)
        for a, b, c in (
            (Q(1), Q(0), upper),
            (Q(-1), Q(0), -lower),
            (Q(0), Q(1), upper),
            (Q(0), Q(-1), -lower),
        ):
            centres = clip(centres, a, b, c, bounded=False)
        joins.append(
            {
                "row": index,
                "intersection": [str(lo), str(hi)],
                "numeric_wall_box": [str(lower), str(upper)],
                "centre_hull": serial(centres),
            }
        )
        for x in centres:
            for c, s in sorted({(c, s) for c in (chi, clo) for s in (slo, shi)}):
                for sign in (-1, 1):
                    tick(deadline)
                    a, b = sign * c, sign * s
                    kernel = clip(kernel, a, b, checked(Q(1, 2) - MARGIN + dot(x, (a, b))))
                    kernel = clip(kernel, -b, a, checked(Q(1, 2) - MARGIN + dot(x, (-b, a))))
                    plane_count += 2
    chosen: list[Point] = []
    if kernel:
        for direction in DIRECTIONS:
            best = max(dot(p, direction) for p in kernel)
            p = min(p for p in kernel if dot(p, direction) == best)
            if p not in chosen:
                chosen.append(p)
    return {
        "guard": [str(q) for q in guard],
        "row_intersections": joins,
        "planes": plane_count,
        "kernel": serial(kernel),
        "selected": serial(chosen),
        "selected_hull": serial(hull(chosen)),
    }


def gain(points: list[Point], baseline: list[Point]) -> dict[str, Any]:
    if not points:
        return {"passed": False, "branch": "empty_candidate"}
    if not baseline:
        area2 = checked(
            abs(
                sum(
                    (
                        checked(points[i][0] * points[(i + 1) % len(points)][1])
                        - checked(points[(i + 1) % len(points)][0] * points[i][1])
                        for i in range(len(points))
                    ),
                    Q(0),
                )
            )
        )
        return {
            "passed": area2 >= 2 * AREA,
            "branch": "empty_baseline_area",
            "area2": str(area2),
            "required_area2": str(2 * AREA),
        }
    differences = [
        checked(max(dot(p, n) for p in points) - max(dot(p, n) for p in baseline))
        for n in CARDINAL
    ]
    return {
        "passed": max(differences) >= GAIN,
        "branch": "cardinal_support",
        "directions": [list(n) for n in CARDINAL],
        "candidate_supports": [str(max(dot(p, n) for p in points)) for n in CARDINAL],
        "baseline_supports": [str(max(dot(p, n) for p in baseline)) for n in CARDINAL],
        "differences": [str(v) for v in differences],
        "required_gain": str(GAIN),
    }


def no_science_imports() -> None:
    require(not any(name in sys.modules for name in FORBIDDEN), "scientific/producer import")


def accepted_receipt(document: dict[str, Any]) -> tuple[bytes, dict[str, Any]]:
    require(document["schema"] == SCHEMA, "conditional gate descriptor schema differs")
    raw, receipt = read_json(retained_path(document["h290_receipt"]))
    require(
        hashlib.sha256(raw).hexdigest() == document["h290_receipt_sha256"],
        "accepted H290 receipt bytes differ",
    )
    require(
        receipt["schema"] == "n17-numeric-cap-checkpoint/v1"
        and receipt["readiness_passed"] is True
        and receipt["verification_passed"] is True
        and receipt["saved_checkpoint_replayed"] is True
        and receipt["root"],
        "accepted H290 readiness premise required",
    )
    custody = receipt["custody"]
    parent, frame = custody["parent_replay"], custody["parent_replay"]["frame"]
    roles = document["label_to_owner"]
    require(
        set(roles) == {str(i) for i in range(1, 18)}
        and all(type(o) is int for o in roles.values())
        and roles["1"] == 0
        and sorted(roles.values()) == parent["mask"]
        and len(set(roles.values())) == 17,
        "full17 label/owner map differs",
    )
    require(
        frame == document["frame"]
        and frame["U"] == str(U)
        and frame["L"] == str(U)
        and frame["B"] == "1"
        and frame["capture_cap"] == str(V)
        and frame["occupancy"] == 17
        and len(frame["cells"]) == 24
        and frame["cell_names"][0] == "corner-SW"
        and frame["cell_names"][roles["6"]] == "side-S2"
        and [a["name"] for a in frame["actions"]]
        == ["r0", "r1", "r2", "r3", "f0", "f1", "f2", "f3"],
        "accepted original24 numeric frame differs",
    )
    require(
        parent["status"] == "PASS_SAVED_STALL"
        and parent["closure"] is None
        and parent["steps_checked"] == 16
        and len(parent["step_owners"]) == 16
        and set(parent["step_owners"]) == set(parent["mask"]) - {roles["6"]}
        and parent["seed_sha256"] == document["seed_sha256"]
        and parent["node_sha256"] == document["node_sha256"]
        and parent["compressed_object_sha256"] == document["compressed_sha256"],
        "accepted full16 saved-object premise differs",
    )
    fresh = custody["fresh_replay"]
    replay = fresh["receipt"]
    require(
        fresh["exit_code"] == 0
        and replay["status"] == "PASS_SAVED_STALL"
        and replay["producer_imported"] is False
        and replay["frame"] == frame
        and replay["mask"] == parent["mask"]
        and replay["steps_checked"] == 16
        and replay["step_owners"] == parent["step_owners"]
        and replay["seed_sha256"] == parent["seed_sha256"]
        and replay["node_sha256"] == parent["node_sha256"]
        and replay["closure"] is None,
        "accepted fresh complete replay premise differs",
    )
    held = custody["endpoint_retention"]
    require(
        held["held"] is True
        and held["lost_labels"] == []
        and [p["label"] for p in held["owners"]] == list(range(1, 18))
        and {str(p["label"]): p["owner"] for p in held["owners"]} == roles
        and all(p["witness"] is not None for p in held["owners"]),
        "accepted all17 endpoint premise differs",
    )
    require(
        len(receipt["intervals"]) == 49
        and all(rational(lo) <= 0 <= rational(hi) for lo, hi in receipt["intervals"].values()),
        "accepted all49 zero-containing premise differs",
    )
    raw_roster = custody["input_control"]["endpoint_roster"]
    require(type(raw_roster) is list, "endpoint roster list required")
    roster = cast(list[dict[str, Any]], raw_roster)
    require(
        [p["label"] for p in roster] == list(range(1, 18))
        and {str(p["label"]): p["owner"] for p in roster} == roles,
        "accepted endpoint roster differs",
    )
    for pose in roster:
        centre = pose["centre"]
        require(
            type(centre) is list
            and len(centre) == 2
            and all(type(box) is list and len(box) == 2 for box in centre),
            "full two-axis endpoint centre shape required",
        )
        for box in cast(list[list[str]], centre):
            for endpoint in box:
                rational_grammar(endpoint)
        if pose["label"] == 1:
            require(
                all(
                    rational(box[0]) <= rational(box[1])
                    for box in cast(list[list[str]], centre)
                ),
                "used two-axis ordered endpoint centre required",
            )
    return raw, receipt


def extract(document: dict[str, Any], deadline: float) -> tuple[dict[str, Any], dict[str, Any]]:
    raw, receipt = accepted_receipt(document)
    directory = retained_path(document["saved_objects"])
    seeds, nodes = (
        list(directory.glob("seed-*.json.gz")),
        list(directory.glob("node-*.json.gz")),
    )
    require(len(seeds) == len(nodes) == 1, "exactly one saved seed/node required")
    seed_path, node_path = seeds[0], nodes[0]
    frozen = {
        str(p.relative_to(REPO)): digest(p, cap, deadline)
        for p, cap in ((seed_path, SEED_LIMIT), (node_path, NODE_LIMIT))
    }
    require(frozen == document["compressed_sha256"], "compressed saved objects differ")
    seed = seed_decode(seed_path, deadline)
    require(identity(seed) == document["seed_sha256"], "canonical seed differs")
    node = BoundedNode(node_path, deadline)
    owners = []
    for step in node.steps():
        tick(deadline)
        owners.append(step["owner"])
    require(node.sha256 == document["node_sha256"], "canonical node EOF differs")
    header, frame = node.header, document["frame"]
    mask = receipt["custody"]["parent_replay"]["mask"]
    require(
        owners == receipt["custody"]["parent_replay"]["step_owners"]
        and header["parent"] is None
        and header["guard_source"] is None
        and header["constraints"] == []
        and type(header["source"]) is dict
        and header["source"]["sha256"] == identity(seed)
        and header["closed"] is False
        and header["terminal"] is False
        and header["contradiction"] is None
        and header["mask"] == mask
        and header["U"] == str(U)
        and header["B"] == "1",
        "accepted node headers/step order differ",
    )
    final = header["final_state"]
    if len(canonical(final)) > SLICE_LIMIT:
        raise IncompleteError("conditional gate final-state slice byte ceiling")
    require(
        final["U"] == str(U)
        and final["B"] == "1"
        and final["mask"] == mask
        and final["mask_index"] == header["mask_index"]
        and final["source"] == header["source"]
        and final["world"] == frame["cells"]
        and final["constraints"] == []
        and final["guard"] == {}
        and final["guard_source"] is None
        and set(final["cells"]) == set(final["groups"]) == set(map(str, mask)),
        "accepted final-state headers/owner keys differ",
    )
    coarse = document["label_to_owner"]["6"]
    for owner in mask:
        rows = final["cells"][str(owner)]
        require(
            type(rows) is list
            and len(rows) == (32 if owner == coarse else 64)
            and type(final["groups"][str(owner)]) is list,
            "frozen final row count/group shape differs",
        )
        require(
            all(
                type(row) is dict
                and type(row["reference"]) is dict
                and type(row["interval"]) is list
                and len(row["interval"]) == 2
                and type(row["outer_domain"]) is list
                and type(row["residual_polygons"]) is list
                for row in rows
            ),
            "accepted final row/reference shape differs",
        )
        for row in cast(list[dict[str, Any]], rows):
            for endpoint in row["interval"]:
                rational_grammar(endpoint)
            opaque_polygon(row["outer_domain"])
            for poly in row["residual_polygons"]:
                opaque_polygon(poly)
        opaque_polygon(final["groups"][str(owner)])
        # H290 already admitted every owner's final geometry. Only owner0 is an
        # arithmetic input to this gate; other geometry stays canonical-ID bound.
        if owner != 0:
            continue
        rows = cast(list[dict[str, Any]], rows)
        previous = Q(0)
        for row in rows:
            lo, hi = map(rational, row["interval"])
            require(
                lo == previous and lo < hi <= 1 and type(row["reference"]) is dict,
                "closed row partition/reference differs",
            )
            previous = hi
            for poly in row["residual_polygons"]:
                polygon(poly)
        require(previous == 1, "closed rows do not cover chart")
        polygon(final["groups"][str(owner)])
    for p, cap in ((seed_path, SEED_LIMIT), (node_path, NODE_LIMIT)):
        require(
            digest(p, cap, deadline) == frozen[str(p.relative_to(REPO))],
            "saved compressed objects changed during extraction",
        )
    require(
        read_json(retained_path(document["h290_receipt"]))[0] == raw,
        "accepted H290 receipt changed during extraction",
    )
    return final, {
        "h290_receipt": document["h290_receipt"],
        "h290_receipt_sha256": document["h290_receipt_sha256"],
        "seed_sha256": document["seed_sha256"],
        "node_sha256": node.sha256,
        "compressed_sha256": frozen,
        "steps": len(owners),
        "endpoint_retention": receipt["custody"]["endpoint_retention"],
        "label1_geometry": receipt["custody"]["input_control"]["endpoint_roster"][0],
        "accepted_parent_premises": {
            name: {
                "receipt": document["h290_receipt"],
                "json_path": path,
                "content_sha256": identity(value),
            }
            for name, path, value in (
                ("root", "$.root", receipt["root"]),
                ("frame", "$.custody.parent_replay.frame", frame),
                ("all49_zero_bounds", "$.intervals", receipt["intervals"]),
                (
                    "full17_endpoint_geometry",
                    "$.custody.input_control.endpoint_roster",
                    receipt["custody"]["input_control"]["endpoint_roster"],
                ),
            )
        }
        | {
            "other_owner_final_geometry": {
                "saved_node": str(node_path.relative_to(REPO)),
                "node_sha256": node.sha256,
                "json_path": "$.final_state",
                "subset": "cells/groups excluding owner0",
                "content_sha256": identity(
                    {
                        "cells": {k: v for k, v in final["cells"].items() if k != "0"},
                        "groups": {k: v for k, v in final["groups"].items() if k != "0"},
                    }
                ),
            }
        },
        "arithmetic_scope": "owner0 residual vertices/group/closed intervals and label1 centre",
        "opaque_premise_scope": (
            "accepted H290 facts; byte/content custody, no new geometry replay"
        ),
        "root_checked_now": False,
        "parent_geometry_replayed": False,
    }


def generate(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    frozen_descriptor = canonical(document)
    final, custody = extract(document, deadline)
    rows = final["cells"]["0"]
    variants = {name: reconstruct(rows, guard, deadline) for name, guard in GUARDS.items()}
    selected = {name: polygon(value["selected_hull"]) for name, value in variants.items()}
    baseline = polygon(final["groups"]["0"])
    unconditional = gain(selected["all"], baseline)
    guarded = gain(selected["target"], hull(baseline + selected["all"]))
    pose = custody["label1_geometry"]
    require(
        pose["owner"] == 0 and ["0", "0"] in pose["charts"],
        "endpoint chart0/owner0 premise differs",
    )
    centre = [tuple(map(rational, box)) for box in pose["centre"]]
    endpoint = selected["endpoint"]
    control = {
        "nonempty": bool(endpoint),
        "strictly_inside": bool(endpoint)
        and all(
            max(abs(checked(p[k] - lo)), abs(checked(p[k] - hi))) < Q(1, 2)
            for p in endpoint
            for k, (lo, hi) in enumerate(centre)
        ),
    }
    if not endpoint:
        status = "inconclusive_control_empty"
    elif not control["strictly_inside"]:
        status = "refused_endpoint_control"
    elif unconditional["passed"]:
        status = "unconditional_refresh_candidate"
    elif guarded["passed"]:
        status = "conditional_gain_candidate"
    else:
        status = "no_gain_under_frozen_recipe"
    for path, expected in custody["compressed_sha256"].items():
        ceiling = SEED_LIMIT if Path(path).name.startswith("seed-") else NODE_LIMIT
        require(
            digest(retained_path(path), ceiling, deadline) == expected,
            "saved compressed objects changed during finite construction",
        )
    require(
        hashlib.sha256(read_json(retained_path(document["h290_receipt"]))[0]).hexdigest()
        == document["h290_receipt_sha256"],
        "accepted H290 receipt changed during finite construction",
    )
    require(
        canonical(document) == frozen_descriptor, "gate descriptor changed during construction"
    )
    tick(deadline)
    report = {
        "schema": SCHEMA,
        "status": status,
        "custody": custody,
        "recipe": {
            "guards": {k: [str(x) for x in v] for k, v in GUARDS.items()},
            "margin": str(MARGIN),
            "gain": str(GAIN),
            "area": str(AREA),
            "vertex_limit": VERTEX_LIMIT,
            "rational_bits": BIT_LIMIT,
        },
        "variants": variants,
        "baseline": serial(baseline),
        "unconditional_gain": unconditional,
        "guard_specific_gain": guarded,
        "endpoint_control": control,
        "producer_run": False,
        "conditional_owned_exclusion": False,
        "global_optimality_proved": False,
        "census_admission_proved": False,
        "assurance": (
            "exact finite reconstruction; conditional ownership implication "
            "is reviewed hand mathematics"
        ),
    }
    rational_tree({k: v for k, v in report.items() if k != "custody"})
    rational_tree(pose)
    return report


def check(
    document: dict[str, Any], certificate: dict[str, Any], *, deadline: float
) -> dict[str, Any]:
    reconstructed = generate(document, deadline=deadline)
    core = {k: v for k, v in certificate.items() if k not in {"provenance", "invocation"}}
    require(canonical(reconstructed) == canonical(core), "finite gate certificate differs")
    return {
        "schema": SCHEMA,
        "finite_reconstruction_verified": True,
        "status": reconstructed["status"],
        "certificate_sha256": identity(certificate),
        "producer_run": False,
        "root_checked_now": False,
        "parent_geometry_replayed": False,
        "conditional_owned_exclusion": False,
        "global_optimality_proved": False,
    }


def output_within(report: dict[str, Any]) -> None:
    if len(retained_json.dumps(report).encode()) > OUTPUT_LIMIT:
        raise IncompleteError("conditional gate output byte ceiling")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--descriptor", type=Path, required=True)
    parser.add_argument("--check", type=Path)
    parser.add_argument("--max-seconds", type=float, default=60)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    report: dict[str, Any]
    try:
        require(
            math.isfinite(args.max_seconds) and 0 < args.max_seconds <= 60,
            "invalid or enlarged conditional gate wall ceiling",
        )
        no_science_imports()
        deadline = time.monotonic() + args.max_seconds
        raw, document = read_json(args.descriptor)
        if args.check:
            certificate_raw, certificate = read_json(args.check, OUTPUT_LIMIT)
            report = check(document, certificate, deadline=deadline)
            require(
                read_json(args.check, OUTPUT_LIMIT)[0] == certificate_raw,
                "finite certificate changed",
            )
        else:
            report = generate(document, deadline=deadline)
        require(read_json(args.descriptor)[0] == raw, "gate descriptor changed")
        report["provenance"] = provenance(Path(__file__))
        report["invocation"] = {
            "argv": list(argv) if argv is not None else sys.argv[1:],
            "executable": sys.executable,
            "max_seconds": args.max_seconds,
        }
        tick(deadline)
        no_science_imports()
        output_within(report)
    except IncompleteError as error:
        report = {"schema": SCHEMA, "status": "incomplete", "error": str(error)}
    except (
        ValueError,
        OSError,
        EOFError,
        KeyError,
        TypeError,
        IndexError,
        standing.VerificationError,
    ) as error:
        report = {"schema": SCHEMA, "status": "refused", "error": str(error)}
    for flag in (
        "producer_run",
        "conditional_owned_exclusion",
        "global_optimality_proved",
        "census_admission_proved",
    ):
        report[flag] = False
    args.output.write_text(retained_json.dumps(report))
    print(json.dumps({k: report[k] for k in ("status", "error") if k in report}))
    return 1 if report["status"] in {"incomplete", "refused", "refused_endpoint_control"} else 0


if __name__ == "__main__":
    raise SystemExit(main())
