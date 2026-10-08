"""Guarded shared-centre geometry and exact primal reading; no LP search.

The source-specific endpoint entry point is callable only by a separately registered
round. Importing this module reads no research inputs and evaluates no endpoint.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import operator
import os
import sys
import tempfile
import time
from collections.abc import Callable
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Literal, cast

import yaml

from devtools import check_n17_incircle_projection_redundancy as projection
from devtools import probe_n17_conditional_center_cases as geometry
from devtools import verify_n17_kernel_certificate as standing
from devtools.check_n17_contact_chart import SOURCE_ROW_LABELS
from devtools.provenance import provenance
from sqpack.yamlio import load_yaml

U = Q(1169, 250)
SIDE = Q(4675530093604551, 10**15)
ENDPOINT_MASK = 1900015
BITS = 4096
CELL_LIMIT, E_LIMIT, D_LIMIT = 32, 36, 72
CLIP_LIMIT, RAW_LIMIT, H_LIMIT = 73, 584, 88
ROW_LIMIT, WITNESS_LIMIT, PACKET_LIMIT = 12580, 1 << 20, 8 << 20
DESCRIPTOR_LIMIT, OPERATION_LIMIT, PHASE_SECONDS = 10 << 20, 2_000_000, 120
CONTEXT_SCHEMA = "n17-shared-centre-endpoint-context/v1"
type Point = tuple[Q, Q]
type Plane = tuple[Q, Q, Q]
type FrameAction = Literal["r3", "f1"]
IncompleteError = projection.finite.IncompleteError
require = projection.require


@dataclass
class Budget:
    """One caller-frozen scalar-operation ceiling and cooperative monotonic deadline."""

    deadline: float
    max_operations: int
    operations: int = 0

    def __post_init__(self) -> None:
        require(
            type(self.max_operations) is int and 0 < self.max_operations <= OPERATION_LIMIT,
            "operation cap",
        )
        require(self.operations == 0, "fresh operation counter required")
        require(math.isfinite(self.deadline), "finite deadline required")

    def tick(self) -> None:
        if time.monotonic() >= self.deadline:
            raise IncompleteError("shared-centre wall ceiling")

    def charge(self) -> None:
        self.tick()
        self.operations += 1
        if self.operations > self.max_operations:
            raise IncompleteError("shared-centre operation ceiling")

    def checked(self, value: Q) -> Q:
        self.tick()
        require(type(value) is Q, "exact Fraction required")
        if max(abs(value.numerator).bit_length(), value.denominator.bit_length()) > BITS:
            raise IncompleteError("shared-centre rational bit ceiling")
        self.tick()
        return value

    def rational(self, value: object) -> Q:
        self.charge()
        require(type(value) is str, "canonical rational string required")
        assert isinstance(value, str)
        result = projection.finite.rational(value)
        return self.checked(result)


class Guarded:
    """Exact scalar seam for the existing geometry, guarding every intermediate.

    No geometry algorithm is replaced: the existing clip, hull and closed-plane
    functions operate on these scalars. Every arithmetic result and comparison
    observes the same budget. Inputs and serialized outputs remain Fractions.
    """

    def __init__(self, value: Q, budget: Budget):
        self.value = budget.checked(value)
        self.budget = budget

    @property
    def numerator(self) -> int:
        return self.value.numerator

    @property
    def denominator(self) -> int:
        return self.value.denominator

    def other(self, value: object) -> Q:
        if isinstance(value, Guarded):
            require(value.budget is self.budget, "mixed arithmetic budgets")
            return value.value
        require(type(value) in (int, Q), "nonexact arithmetic operand")
        return self.budget.checked(Q(cast(Any, value)))

    def arithmetic(self, other: object, operation: str) -> Guarded:
        self.budget.charge()
        right = self.other(other)
        if operation == "add":
            result = self.value + right
        elif operation == "sub":
            result = self.value - right
        elif operation == "mul":
            result = self.value * right
        else:
            result = self.value / right
        return Guarded(result, self.budget)

    def __add__(self, other: object) -> Guarded:
        return self.arithmetic(other, "add")

    def __radd__(self, other: object) -> Guarded:
        return self + other

    def __sub__(self, other: object) -> Guarded:
        return self.arithmetic(other, "sub")

    def __rsub__(self, other: object) -> Guarded:
        return Guarded(self.other(other), self.budget) - self

    def __mul__(self, other: object) -> Guarded:
        return self.arithmetic(other, "mul")

    def __rmul__(self, other: object) -> Guarded:
        return self * other

    def __truediv__(self, other: object) -> Guarded:
        return self.arithmetic(other, "div")

    def __rtruediv__(self, other: object) -> Guarded:
        return Guarded(self.other(other), self.budget) / self

    def __neg__(self) -> Guarded:
        self.budget.charge()
        return Guarded(-self.value, self.budget)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Guarded) and type(other) not in (int, Q):
            return False
        return self.comparison(other, operator.eq)

    def comparison(self, other: object, compare: Callable[[Q, Q], bool]) -> bool:
        self.budget.charge()
        result = compare(self.value, self.other(other))
        self.budget.tick()
        return result

    def __lt__(self, other: object) -> bool:
        return self.comparison(other, operator.lt)

    def __le__(self, other: object) -> bool:
        return self.comparison(other, operator.le)

    def __gt__(self, other: object) -> bool:
        return self.comparison(other, operator.gt)

    def __ge__(self, other: object) -> bool:
        return self.comparison(other, operator.ge)

    def __hash__(self) -> int:
        return hash(self.value)

    def __bool__(self) -> bool:
        return self.comparison(Q(0), operator.ne)


def guarded_polygon(points: list[Point], budget: Budget) -> Any:
    return [(Guarded(x, budget), Guarded(y, budget)) for x, y in points]


def unguard(value: Any, budget: Budget) -> Q:
    return budget.checked(value.value if isinstance(value, Guarded) else value)


def hull(points: list[Point], limit: int, budget: Budget) -> list[Point]:
    require(len(points) <= RAW_LIMIT, "raw geometry vertex ceiling")
    result = geometry.bounded_hull(guarded_polygon(points, budget), limit, budget.deadline)
    return [(unguard(x, budget), unguard(y, budget)) for x, y in result]


def clip(points: list[Point], plane: Plane, limit: int, budget: Budget) -> list[Point]:
    a, b, c = (Guarded(q, budget) for q in plane)
    result = geometry.clip(
        guarded_polygon(points, budget),
        cast(Any, a),
        cast(Any, b),
        cast(Any, c),
        limit,
        budget.deadline,
    )
    return [(unguard(x, budget), unguard(y, budget)) for x, y in result]


def planes(points: list[Point], budget: Budget) -> tuple[Plane, ...]:
    require(bool(points), "empty domain needs a separately reviewed disposition")
    result = standing.closed_planes(guarded_polygon(points, budget))
    return tuple(cast(Plane, tuple(unguard(q, budget) for q in plane)) for plane in result)


def centre_domain(points: list[Point], budget: Budget) -> list[Point]:
    require(0 < len(points) <= CELL_LIMIT, "original cell vertex ceiling")
    result = hull(points, CELL_LIMIT, budget)
    upper = (Guarded(U, budget) - Q(1, 2)).value
    for plane in (
        (Q(-1), Q(0), Q(-1, 2)),
        (Q(1), Q(0), upper),
        (Q(0), Q(-1), Q(-1, 2)),
        (Q(0), Q(1), upper),
    ):
        result = clip(result, plane, E_LIMIT, budget)
    require(bool(result), "empty centre domain needs separate review")
    return result


def pair_domain(left: list[Point], right: list[Point], budget: Budget) -> list[Point]:
    require(len(left) <= E_LIMIT and len(right) <= E_LIMIT, "centre domain vertex ceiling")
    differences = []
    for p, q in itertools.product(left, right):
        x = Guarded(q[0], budget) - p[0]
        y = Guarded(q[1], budget) - p[1]
        differences.append((x.value, y.value))
    # Difference proposals are bounded separately from clip-output accumulation.
    require(len(differences) <= E_LIMIT**2, "difference proposal ceiling")
    result = geometry.bounded_hull(
        guarded_polygon(differences, budget), D_LIMIT, budget.deadline
    )
    difference = [(unguard(x, budget), unguard(y, budget)) for x, y in result]
    candidates: list[Point] = []
    for nx, ny in projection.FACES:
        candidates.extend(clip(difference, (Q(-nx), Q(-ny), Q(-7)), CLIP_LIMIT, budget))
        require(len(candidates) <= RAW_LIMIT, "raw clip-output ceiling")
    require(bool(candidates), "empty pair domain needs separate review")
    return hull(candidates, H_LIMIT, budget)


@dataclass(frozen=True)
class Row:
    label: str
    coefficients: tuple[Q, ...]
    rhs: Q


@dataclass(frozen=True)
class Model:
    cells: tuple[int, ...]
    pairs: tuple[tuple[int, int], ...]
    rows: tuple[Row, ...]
    row_labels: tuple[str, ...]


def build_model(polygons: list[list[Point]], cells: tuple[int, ...], budget: Budget) -> Model:
    require(len(polygons) == 24, "original 24-cell catalogue required")
    require(
        len(cells) == 17
        and cells == tuple(sorted(set(cells)))
        and all(type(i) is int and i in range(24) for i in cells),
        "typed sorted 17 cells",
    )
    domains = {i: centre_domain(polygons[i], budget) for i in cells}
    pairs = tuple(itertools.combinations(cells, 2))
    rows: list[Row] = []
    for position, cell in enumerate(cells):
        for number, (a, b, rhs) in enumerate(planes(domains[cell], budget)):
            values = [Q(0)] * 34
            values[2 * position : 2 * position + 2] = a, b
            rows.append(Row(f"cell:{cell}:plane:{number}", tuple(values), rhs))
    for first, second in pairs:
        i, j = cells.index(first), cells.index(second)
        domain = pair_domain(domains[first], domains[second], budget)
        for number, (a, b, rhs) in enumerate(planes(domain, budget)):
            values = [Q(0)] * 34
            values[2 * i : 2 * i + 2] = (-Guarded(a, budget)).value, (-Guarded(b, budget)).value
            values[2 * j : 2 * j + 2] = a, b
            rows.append(Row(f"pair:{first}:{second}:plane:{number}", tuple(values), rhs))
            budget.charge()
    require(len(rows) <= ROW_LIMIT, "state row ceiling")
    return Model(cells, pairs, tuple(rows), tuple(row.label for row in rows))


def model_payload(model: Model, budget: Budget) -> dict[str, Any]:
    """Convert bounded rows incrementally under the packet and cooperative wall ceilings."""
    budget.tick()
    require(len(model.cells) == 17 and len(model.pairs) == 136, "endpoint model roster")
    require(len(model.rows) <= ROW_LIMIT, "state row ceiling")
    result: dict[str, Any] = {
        "cells": list(model.cells),
        "pairs": [list(p) for p in model.pairs],
        "rows": [],
    }
    size = len(packet_bytes(result, budget))

    def reserve(amount: int) -> None:
        nonlocal size
        budget.tick()
        size += amount
        if size > PACKET_LIMIT:
            raise IncompleteError("shared-centre model payload byte ceiling")

    for row in model.rows:
        budget.tick()
        require(len(row.coefficients) == 34, "primal row width")
        # Each row has fixed JSON keys/punctuation; scalar strings are ASCII rationals.
        reserve(64 + 6 * len(row.label) + 2)
        coefficients = []
        for coefficient in row.coefficients:
            text = str(budget.checked(coefficient))
            reserve(len(text) + 4)
            coefficients.append(text)
        rhs = str(budget.checked(row.rhs))
        reserve(len(rhs) + 4)
        result["rows"].append({"label": row.label, "coefficients": coefficients, "rhs": rhs})
    budget.tick()
    return result


def check_primal(model: Model, raw_point: object, budget: Budget) -> tuple[Q, ...]:
    require(
        type(raw_point) is list and len(cast(list[Any], raw_point)) == 34,
        "exact 34-coordinate primal required",
    )
    point = tuple(budget.rational(q) for q in cast(list[Any], raw_point))
    require(
        len(model.pairs) == 136
        and model.pairs == tuple(itertools.combinations(model.cells, 2)),
        "complete ordered pair roster required",
    )
    require(len({r.label for r in model.rows}) == len(model.rows), "duplicate row identities")
    require(
        tuple(row.label for row in model.rows) == model.row_labels, "missing/reordered rows"
    )
    for row in model.rows:
        require(len(row.coefficients) == 34, "primal row width")
        total = Guarded(Q(0), budget)
        for a, x in zip(row.coefficients, point, strict=True):
            coefficient = Guarded(a, budget)
            if coefficient:
                total = total + coefficient * x
        require(total <= row.rhs, f"exact primal violates {row.label}")
    return point


def check_packet(model: Model, packet: dict[str, Any], budget: Budget) -> tuple[Q, ...]:
    packet_bytes(packet, budget)
    require(
        set(packet) == {"model", "point"} and packet["model"] == model_payload(model, budget),
        "complete original row/pair payload differs",
    )
    return check_primal(model, packet["point"], budget)


def packet_bytes(packet: dict[str, Any], budget: Budget) -> bytes:
    """Bound retained output while encoding, before allocating a complete oversized JSON."""
    chunks: list[bytes] = []
    size = 0
    encoded = iter(json.JSONEncoder(sort_keys=True, allow_nan=False).iterencode(packet))
    while True:
        try:
            chunk = next(encoded)
        except StopIteration:
            break
        except RecursionError as error:
            raise ValueError("packet nesting exceeds encoder depth") from error
        budget.tick()
        raw = chunk.encode("utf-8")
        size += len(raw)
        if size > PACKET_LIMIT:
            raise IncompleteError("shared-centre packet byte ceiling")
        chunks.append(raw)
    budget.tick()
    return b"".join(chunks)


def check_held(held: dict[Path, bytes], budget: Budget) -> None:
    for path, raw in held.items():
        budget.charge()
        with path.open("rb") as stream:
            require(stream.read(len(raw) + 1) == raw, "held input bytes changed")
        budget.tick()


def frame_assignment(
    names: list[str],
    assignment: list[dict[str, Any]],
    d4: dict[str, list[int]],
    budget: Budget,
    frame_action: FrameAction = "r3",
) -> tuple[dict[int, int], tuple[int, ...]]:
    """Check the selected catalogue action before any witness or geometry evaluation."""
    budget.tick()
    require(frame_action in ("r3", "f1"), "unsupported endpoint frame action")
    require(len(names) == 24 and len(set(names)) == 24, "original named 24-cell catalogue")
    require(
        len(assignment) == 17
        and all(type(r.get("label")) is int for r in assignment)
        and {r["label"] for r in assignment} == set(range(1, 18)),
        "complete H256 candidate label assignment",
    )
    selected = d4.get(frame_action)
    require(
        type(selected) is list
        and len(selected) == 24
        and all(type(i) is int for i in selected)
        and sorted(selected) == list(range(24)),
        f"complete {frame_action} cell permutation",
    )
    permutation = tuple(cast(list[int], selected))
    assigned: dict[int, int] = {}
    transformed: set[int] = set()
    for row in assignment:
        budget.charge()
        cell = names.index(row["cell"])
        assigned[row["label"]] = cell
        require(permutation[cell] not in transformed, "duplicate transformed endpoint cell")
        transformed.add(permutation[cell])
    require(
        sum(1 << cell for cell in transformed) == ENDPOINT_MASK,
        "wrong canonical endpoint orbit",
    )
    budget.tick()
    return assigned, permutation


def frame_point(point: Point, budget: Budget, frame_action: FrameAction = "r3") -> Point:
    """Apply exactly the caller-selected action using the same guarded arithmetic seam."""
    require(frame_action in ("r3", "f1"), "unsupported endpoint frame action")
    x, y = point
    first = budget.checked(y) if frame_action == "r3" else (Guarded(U, budget) - y).value
    return first, (Guarded(U, budget) - x).value


def endpoint_coordinates(
    witness: dict[str, Any],
    names: list[str],
    assignment: list[dict[str, Any]],
    d4: dict[str, list[int]],
    polygons: list[list[Point]],
    *,
    budget: Budget,
    frame_action: FrameAction = "r3",
) -> tuple[tuple[int, ...], tuple[Q, ...]]:
    require(
        witness.get("n") == 17
        and witness.get("side") == str(SIDE)
        and witness.get("representation") == "corners"
        and witness.get("coordinates")
        == {"origin": "lower-left", "axes": "x-right-y-up", "angle_unit": "not-applicable"}
        and witness.get("scalar") == {"kind": "rational"},
        "frozen rational witness convention",
    )
    squares = witness.get("squares")
    require(
        type(squares) is list
        and len(squares) == 17
        and all(type(row) is dict for row in squares),
        "17 source squares required",
    )
    squares = cast(list[dict[str, Any]], squares)
    require([row.get("id") for row in squares] == list(range(1, 18)), "source row IDs differ")
    assigned, permutation = frame_assignment(names, assignment, d4, budget, frame_action)
    delta = (Guarded(U, budget) - SIDE) / 2
    points: dict[int, Point] = {}
    for row, label in zip(squares, SOURCE_ROW_LABELS, strict=True):
        corners = row.get("corners")
        require(
            type(corners) is list
            and len(corners) == 4
            and all(type(p) is list and len(p) == 2 for p in corners),
            "four exact corners",
        )
        corners = cast(list[list[str]], corners)
        centre = []
        for axis in range(2):
            total = Guarded(Q(0), budget)
            for corner in corners:
                total = total + budget.rational(corner[axis])
            centre.append((total / 4 + delta).value)
        cell = assigned[label]
        for a, b, rhs in planes(polygons[cell], budget):
            value = Guarded(a, budget) * centre[0] + Guarded(b, budget) * centre[1]
            require(value <= rhs, "source centre outside candidate original closed cell")
        transformed = permutation[cell]
        require(transformed not in points, "duplicate transformed endpoint cell")
        points[transformed] = frame_point((centre[0], centre[1]), budget, frame_action)
    cells = tuple(sorted(points))
    require(sum(1 << i for i in cells) == ENDPOINT_MASK, "wrong canonical endpoint orbit")
    return cells, tuple(q for i in cells for q in points[i])


def endpoint_packet(
    document: dict[str, Any],
    witness_path: Path,
    witness_sha256: str,
    budget: Budget,
    *,
    frame_action: FrameAction = "r3",
) -> dict[str, Any]:
    """Reconstruct an endpoint packet; import never evaluates source inputs.

    Accepted intake retains its existing guards. Its source-cover reconstruction is
    inherited code, not a newly claimed per-operation guarded proof execution.
    """
    roles = projection.prior.ROLES
    require(
        type(document) is dict
        and document.get("schema") == CONTEXT_SCHEMA
        and set(document)
        == {"schema", *(key for role in roles for key in (role, role + "_sha256"))},
        "endpoint descriptor shape differs",
    )
    require(
        all(type(document[key]) is str for role in roles for key in (role, role + "_sha256")),
        "endpoint descriptor role path/identity must be strings",
    )
    # The inherited descriptor contract is flat; freeze it without recursive traversal.
    frozen = document.copy()
    adapted = document | {"schema": projection.prior.CONTEXT_SCHEMA}
    polygons, names, _roster, accepted, held = projection.prior.intake(adapted, budget.deadline)
    context = accepted["accepted_inputs"]
    partition_path = Path(context["partition"])
    if not partition_path.is_absolute():
        partition_path = projection.prior.corner.old.REPO / partition_path
    partition = projection.finite.decode(held[partition_path.resolve()])
    endpoint = [r for r in partition["orbits"] if r["distance"] == 0]
    require(
        len(endpoint) == 1 and endpoint[0]["mask"] == ENDPOINT_MASK,
        "accepted partition canonical endpoint differs",
    )
    cover_path = Path(context["cover"])
    if not cover_path.is_absolute():
        cover_path = projection.prior.corner.old.REPO / cover_path
    cover = projection.finite.decode(held[cover_path.resolve()])
    family = cover["endpoint"]["family"]["h256-centroid"]
    require(family.get("one_state") is True, "accepted candidate assignment is incomplete")
    assignment = family["squares"]
    frame_assignment(names, assignment, context["d4"], budget, frame_action)
    budget.tick()
    with witness_path.open("rb") as stream:
        raw = stream.read(WITNESS_LIMIT + 1)
    if len(raw) > WITNESS_LIMIT:
        raise IncompleteError("witness byte ceiling exceeded")
    require(
        hashlib.sha256(raw).hexdigest() == witness_sha256,
        "frozen witness byte identity differs",
    )
    require(witness_path not in held or held[witness_path] == raw, "conflicting witness alias")
    held[witness_path] = raw
    source = load_yaml(raw.decode("utf-8"))
    require(
        type(source) is dict and type(source.get("witness")) is dict,
        "witness YAML envelope required",
    )
    witness = cast(dict[str, Any], source["witness"])
    cells, point = endpoint_coordinates(
        witness,
        names,
        assignment,
        context["d4"],
        polygons,
        budget=budget,
        frame_action=frame_action,
    )
    model = build_model(polygons, cells, budget)
    packet = {"model": model_payload(model, budget), "point": list(map(str, point))}
    check_packet(model, packet, budget)
    check_held(held, budget)
    require(document == frozen, "endpoint descriptor changed")
    budget.tick()
    return packet


def check_endpoint_packet(
    document: dict[str, Any],
    witness_path: Path,
    witness_sha256: str,
    packet: dict[str, Any],
    budget: Budget,
    *,
    frame_action: FrameAction = "r3",
) -> dict[str, Any]:
    """Freshly rebuild geometry and all endpoint coordinates, then compare complete payloads."""
    expected = endpoint_packet(
        document, witness_path, witness_sha256, budget, frame_action=frame_action
    )
    require(
        packet_bytes(packet, budget) == packet_bytes(expected, budget),
        "fresh endpoint mathematical payload differs",
    )
    budget.tick()
    return {
        "verification_passed": True,
        "frame_action": frame_action,
        "operations": budget.operations,
        "ordinary_assignment_exclusion_proved": False,
        "census_admission_proved": False,
        "global_bound_proved": False,
        "global_optimality_proved": False,
    }


def main(argv: list[str] | None = None) -> int:
    """Two-phase endpoint instrument; launch only after the round is registered."""
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--descriptor", type=Path, required=True)
    parser.add_argument("--witness", type=Path, required=True)
    parser.add_argument("--witness-sha256", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--check", type=Path)
    parser.add_argument("--frame-action", choices=("r3", "f1"), default="r3")
    parser.add_argument("--max-seconds", type=float, default=PHASE_SECONDS)
    parser.add_argument("--max-operations", type=int, default=OPERATION_LIMIT)
    args = parser.parse_args(argv)
    frame_action = cast(FrameAction, args.frame_action)
    try:
        require(
            math.isfinite(args.max_seconds) and 0 < args.max_seconds <= PHASE_SECONDS,
            "frozen phase wall ceiling",
        )
        budget = Budget(time.monotonic() + args.max_seconds, args.max_operations)
        try:
            descriptor_raw, document = projection.finite.read_json(
                args.descriptor, DESCRIPTOR_LIMIT
            )
        except RecursionError as error:
            raise ValueError("descriptor JSON nesting exceeds decoder depth") from error
        held = {args.descriptor: descriptor_raw}
        if args.check is None:
            mathematical = endpoint_packet(
                document, args.witness, args.witness_sha256, budget, frame_action=frame_action
            )
            result = {
                "schema": "n17-shared-centre-endpoint/v1",
                "status": "constructed",
                "frame_action": frame_action,
                "mathematical": mathematical,
                "operations": budget.operations,
                "verification_passed": False,
            }
        else:
            try:
                constructed_raw, constructed = projection.finite.read_json(
                    args.check, PACKET_LIMIT
                )
            except RecursionError as error:
                raise ValueError("construction JSON nesting exceeds decoder depth") from error
            held[args.check] = constructed_raw
            require(
                constructed.get("schema") == "n17-shared-centre-endpoint/v1"
                and constructed.get("status") == "constructed"
                and type(constructed.get("mathematical")) is dict,
                "construction envelope differs",
            )
            require(
                constructed.get("frame_action") == frame_action,
                "construction frame action differs from frozen checker choice",
            )
            result = check_endpoint_packet(
                document,
                args.witness,
                args.witness_sha256,
                constructed["mathematical"],
                budget,
                frame_action=frame_action,
            )
            result.update(schema="n17-shared-centre-endpoint/v1", status="verified")
        # Provenance's inherited subprocess timeouts remain outer-supervised work.
        source = provenance(Path(__file__), Path(geometry.__file__), Path(standing.__file__))
        check_held(held, budget)
        result.update(
            operations=budget.operations,
            provenance=source,
            invocation={
                "argv": argv if argv is not None else sys.argv[1:],
                "executable": sys.executable,
            },
        )
        output = packet_bytes(result, budget)
        publish_new(args.output, output, budget)
    except (ValueError, OSError, IncompleteError, yaml.YAMLError) as error:
        result = {
            "schema": "n17-shared-centre-endpoint/v1",
            "status": "incomplete" if isinstance(error, IncompleteError) else "refused",
            "frame_action": frame_action,
            "reason": str(error),
            "verification_passed": False,
        }
    else:
        return 0
    try:
        publish_new(args.output, json.dumps(result, sort_keys=True).encode("utf-8"))
    except (OSError, IncompleteError) as error:
        print(f"endpoint receipt publication failed: {error}", file=sys.stderr)
    return 1


def publish_new(path: Path, output: bytes, budget: Budget | None = None) -> None:
    """Atomically publish complete bytes without replacing evidence; no durability promise."""
    if len(output) > PACKET_LIMIT:
        raise IncompleteError("shared-centre publication byte ceiling")
    if budget is not None:
        budget.tick()
    descriptor, name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(output)
        if budget is not None:
            budget.tick()
        os.link(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
