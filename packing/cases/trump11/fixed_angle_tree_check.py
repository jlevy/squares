"""Independent reader for a fixed-angle cell tree (H-236, X-046 rung 0).

The reader does not import `fixed_angle_tree`.  From the header it takes only the family
(counts and the rational half-tangent box), the tilted core (a half-tangent and a side),
the target, the variable cap, the declared symmetry rows and the declared labelled image
(its name, quarter turns, labels and radius).  Everything else is rebuilt here:

- the core is accepted only if every vertex lies in the rotated unit square at every
  angle of the box, decided exactly;
- each pair's options are the distinct edge-normal directions of the two cores in
  counter-clockwise order from the positive x axis, and each row is rebuilt from the
  direction, scaled so its larger centre coefficient has absolute value 1;
- the tree is replayed in pre-order: every branch's children must be exactly its
  options, each once, no pair may be branched twice on a path, and there is one root;
- every leaf's multipliers are read as exact rationals and its bound is evaluated in
  `Fraction` arithmetic against the rows of *that* leaf's cell;
- for the target ``U``, the upper end the header uses must be at least ``U``, which the
  reader brackets itself from the witness field; the Trump image's centres are rebuilt
  from `cases.trump11.packing` with the declared turns and labels, the radius must be
  BC-240's ``rho``, and the box's angle half-width must be below ``rho``.

It reports ``closed`` only when no leaf is unresolved.

    uv run --frozen python -m cases.trump11.fixed_angle_tree_check TREE.jsonl.gz
"""

from __future__ import annotations

import argparse
import gzip
import json
import math
import multiprocessing
import sys
import time
from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any

from cases.trump11.packing import build

BC240_RHO = Fraction(808514697, 200000000000)
WITNESS_DIGITS = 50

type Point = tuple[Fraction, Fraction]
type Span = tuple[Fraction, Fraction]


class RejectionError(ValueError):
    """The tree or one of its certificates does not verify."""


# -- geometry, rebuilt ------------------------------------------------------------------


def unit_at(tangent: Fraction) -> Point:
    square = tangent * tangent
    return (1 - square) / (1 + square), (tangent + tangent) / (1 + square)


def quarter(vector: Point, turns: int) -> Point:
    x, y = vector
    return [(x, y), (-y, x), (-x, -y), (y, -x)][turns % 4]


def square_corners(tangent: Fraction, side: Fraction) -> list[Point]:
    cos_t, sin_t = unit_at(tangent)
    half = side / 2
    corners = []
    for turns in range(4):
        # the corner in direction theta + 45 degrees, turned
        ex, ey = quarter((cos_t, sin_t), turns)
        fx, fy = quarter((cos_t, sin_t), turns + 1)
        corners.append((half * (ex + fx), half * (ey + fy)))
    return corners


def window_contains(corners: list[Point], left: Fraction, right: Fraction) -> bool:
    """Each corner is in the unit square rotated to every angle with half-tangent in the box."""
    if not (0 <= left <= right < 1):
        return False
    start, stop = unit_at(left), unit_at(right)
    half = Fraction(1, 2)
    for px, py in corners:
        for turns in range(4):
            ax, ay = quarter(start, turns)
            bx, by = quarter(stop, turns)
            if ax * px + ay * py > half or bx * px + by * py > half:
                return False
            # |p| cos(phi - arg p) peaks inside the window only if arg p is inside it
            between = (ax * py - ay * px) >= 0 and (px * by - py * bx) >= 0
            if between and px * px + py * py > half * half:
                return False
    return True


def integer_direction(x: Fraction, y: Fraction) -> tuple[int, int]:
    common = x.denominator * y.denominator
    a, b = int(x * common), int(y * common)
    g = math.gcd(a, b)
    return a // g, b // g


def ccw_rank(direction: tuple[int, int]) -> tuple[int, Fraction]:
    """A sort key for the counter-clockwise angle in ``[0, 2 pi)``, exact."""
    x, y = direction
    # quadrant index, then the tangent-like ratio within it, both exact
    if x > 0 and y >= 0:
        return 0, Fraction(y, x)
    if x <= 0 < y:
        return 1, Fraction(-x, y)
    if x < 0 and y <= 0:
        return 2, Fraction(y, x)
    return 3, Fraction(x, -y)


@dataclass
class Shape:
    corners: list[Point]
    directions: list[tuple[int, int]]

    def reach(self, normal: Point) -> Fraction:
        return max(normal[0] * px + normal[1] * py for px, py in self.corners)


def make_shape(tangent: Fraction, side: Fraction) -> Shape:
    corners = square_corners(tangent, side)
    cos_t, sin_t = unit_at(tangent)
    directions = [integer_direction(*quarter((cos_t, sin_t), turns)) for turns in range(4)]
    return Shape(corners, directions)


# -- the witness and its image ----------------------------------------------------------


def witness_brackets() -> tuple[Span, Span, Any, Any, Any]:
    squares, side, field_ = build()
    field_.refine_to(WITNESS_DIGITS)
    u_span = field_.root_bounds()
    # U = (6u + 4)/(1 + 2u - u^2) increases on [0.36, 0.37]: the numerator of its
    # derivative is 6u^2 + 8u - 2, positive for u > 0.2153
    lo, hi = u_span
    if not (Fraction(36, 100) <= lo and hi <= Fraction(37, 100)):
        raise RejectionError("the witness root left its recorded isolating interval")

    def side_of(u: Fraction) -> Fraction:
        return (6 * u + 4) / (1 + 2 * u - u * u)

    return u_span, (side_of(lo), side_of(hi)), squares, side, field_


def trump_image(turns: int, labels: list[int]) -> tuple[list[Span], Span, Span]:
    u_span, u_side, squares, side, field_ = witness_brackets()
    if sorted(labels[:6]) != list(range(6)) or sorted(labels[6:]) != list(range(6, 11)):
        raise RejectionError("image labels must permute the six axis and five tilted squares")
    xs, ys = [], []
    for label in labels:
        corners = squares[label]
        x = (corners[0][0] + corners[1][0] + corners[2][0] + corners[3][0]) * Fraction(1, 4)
        y = (corners[0][1] + corners[1][1] + corners[2][1] + corners[3][1]) * Fraction(1, 4)
        for _ in range(turns % 4):
            x, y = side - y, x
        xs.append(field_.enclose(x))
        ys.append(field_.enclose(y))
    return xs + ys, u_span, u_side


def goebel_image() -> list[Span]:
    scale = 10**WITNESS_DIGITS
    root = math.isqrt(2 * scale * scale)
    r_lo, r_hi = Fraction(root, scale), Fraction(root + 1, scale)
    s_lo, s_hi = 2 + r_lo / 2, 2 + r_hi / 2
    half = Fraction(1, 2)
    near, far, mid = (half, half), (s_lo - half, s_hi - half), (s_lo / 2, s_hi / 2)
    # corners ordered by x + y/4: (near, near), (near, far), (far, near), (far, far)
    centres = [(near, near), (near, far), (far, near), (far, far), (mid, mid)]
    return [c[0] for c in centres] + [c[1] for c in centres]


# -- the cell program -------------------------------------------------------------------


@dataclass
class Program:
    axis_count: int
    tilted_count: int
    shapes: list[Shape]
    base: dict[str, tuple[dict[int, Fraction], Fraction]]
    target: Fraction
    cap: Fraction
    pair_cache: dict[str, tuple[dict[int, Fraction], Fraction]] = field(default_factory=dict)
    option_cache: dict[tuple[int, int], list[tuple[int, int]]] = field(default_factory=dict)

    @property
    def count(self) -> int:
        return self.axis_count + self.tilted_count

    def options(self, i: int, j: int) -> list[tuple[int, int]]:
        key = (i, j)
        if key not in self.option_cache:
            union = set(self.shapes[i].directions) | set(self.shapes[j].directions)
            self.option_cache[key] = sorted(union, key=ccw_rank)
        return self.option_cache[key]

    def pair(self, i: int, j: int, option: int) -> tuple[dict[int, Fraction], Fraction]:
        label = f"pair:{i}:{j}:{option}"
        if label not in self.pair_cache:
            a, b = self.options(i, j)[option]
            biggest = max(abs(a), abs(b))
            nx, ny = Fraction(a, biggest), Fraction(b, biggest)
            reach = self.shapes[i].reach((nx, ny)) + self.shapes[j].reach((nx, ny))
            n = self.count
            coefficients = {j: nx, n + j: ny, i: -nx, n + i: -ny}
            self.pair_cache[label] = ({k: v for k, v in coefficients.items() if v}, reach)
        return self.pair_cache[label]


def build_program(head: dict[str, Any]) -> Program:
    fam = head["family"]
    axis_count, tilted_count = int(fam["axis_count"]), int(fam["tilted_count"])
    left, right = Fraction(fam["left"]), Fraction(fam["right"])
    core = head["core"]
    tangent, side = Fraction(core["half_tangent"]), Fraction(core["side"])
    axis_shape = make_shape(Fraction(0), Fraction(1))
    tilted_shape = make_shape(tangent, side)
    if tilted_count and not window_contains(tilted_shape.corners, left, right):
        raise RejectionError("the declared core is not inside the unit square across the box")
    shapes = [axis_shape] * axis_count + [tilted_shape] * tilted_count
    n = axis_count + tilted_count
    one, zero = Fraction(1), Fraction(0)
    base: dict[str, tuple[dict[int, Fraction], Fraction]] = {}
    for i, shape in enumerate(shapes):
        wide = shape.reach((one, zero))
        tall = shape.reach((zero, one))
        base[f"wall:{i}:L"] = ({i: one}, wide)
        base[f"wall:{i}:R"] = ({2 * n: one, i: -one}, wide)
        base[f"wall:{i}:B"] = ({n + i: one}, tall)
        base[f"wall:{i}:T"] = ({2 * n: one, n + i: -one}, tall)
    symmetry = head["symmetry"]
    groups = [range(axis_count), range(axis_count, n)]
    if symmetry["order_epsilon"] is not None:
        eps = Fraction(symmetry["order_epsilon"])
        if eps <= 0:
            raise RejectionError("the order functional must weight y positively")
        for group in groups:
            for i in list(group)[:-1]:
                row = {i + 1: one, n + i + 1: eps, i: -one, n + i: -eps}
                base[f"order:{i}"] = (row, zero)
    if symmetry["quadrant"] != "none":
        group = {"axis": groups[0], "tilted": groups[1]}[symmetry["quadrant"]]
        if not len(group):
            raise RejectionError("the quadrant rows need a nonempty class")
        half = Fraction(len(group), 2)
        base["quad:x"] = ({**dict.fromkeys(group, one), 2 * n: -half}, zero)
        base["quad:y"] = ({**{n + i: one for i in group}, 2 * n: -half}, zero)
    cap = Fraction(head["variable_cap"])
    target = Fraction(head["target"]["upper"])
    if not 0 < target < cap:
        raise RejectionError("the target must lie inside the variable box")
    return Program(axis_count, tilted_count, shapes, base, target, cap)


def evaluate(
    program: Program,
    rows: dict[str, tuple[dict[int, Fraction], Fraction]],
    multipliers: dict[str, str],
    objective: dict[int, Fraction],
    side_top: Fraction,
) -> Fraction:
    """``b . y + sum_k min over the box of (c - A^T y)_k z_k``, every column in
    ``[0, cap]`` except the side, which is in ``[0, side_top]``."""
    residual = dict(objective)
    total = Fraction(0)
    for label, text in multipliers.items():
        if label not in rows:
            raise RejectionError(f"multiplier on {label}, which is not a row of this cell")
        weight = Fraction(text)
        if weight < 0:
            raise RejectionError("a multiplier is negative")
        coefficients, rhs = rows[label]
        total += weight * rhs
        for column, value in coefficients.items():
            residual[column] = residual.get(column, Fraction(0)) - weight * value
    side_column = 2 * program.count
    for column, value in residual.items():
        top = side_top if column == side_column else program.cap
        if value < 0:
            total += value * top
    return total


# -- replay -----------------------------------------------------------------------------


@dataclass
class Frame:
    pair: tuple[int, int]
    size: int
    seen: set[int]


@dataclass
class Report:
    kinds: Counter[str] = field(default_factory=Counter)
    depths: Counter[int] = field(default_factory=Counter)
    unresolved: Counter[str] = field(default_factory=Counter)
    worst_margin: Fraction | None = None
    reach: Fraction = Fraction(0)


def records(path: Path) -> Iterator[dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for line in stream:
            yield json.loads(line)


def replay_subtree(
    task: tuple[Path, dict[str, Any], int, list[list[int]], int | None],
) -> Report:
    """Replay one frontier file; used directly or by a pool of reader processes."""
    top, head, index, recorded, limit = task
    program = build_program(head)
    statement = check_target_and_image(head, program)
    image, radius = statement.pop("_image"), statement.pop("_radius")
    report = Report()
    directory = top.parent / str(head["extra"]["subtree_directory"])
    sub_stream = records(directory / f"sub-{index:05d}.jsonl.gz")
    sub_head = next(sub_stream)["header"]
    for key in ("schema", "family", "core", "target", "variable_cap", "symmetry", "image"):
        if sub_head.get(key) != head.get(key):
            raise RejectionError(f"subtree {index} declares a different {key}")
    root = sub_head.get("root_path")
    if root != recorded or sub_head.get("split_depth") is not None:
        raise RejectionError(f"subtree {index} does not start at its frontier cell")
    fixed = {}
    for i, j, option in root:
        if option not in range(len(program.options(i, j))):
            raise RejectionError(f"subtree {index} has an invalid root option")
        fixed[(i, j)] = option
    walk(
        program,
        stream=sub_stream,
        fixed=fixed,
        splits=False,
        image=image,
        radius=radius,
        report=report,
        limit=limit,
    )
    return report


def merge(total: Report, part: Report) -> None:
    total.kinds.update(part.kinds)
    total.depths.update(part.depths)
    total.unresolved.update(part.unresolved)
    total.reach = max(total.reach, part.reach)
    if part.worst_margin is not None and (
        total.worst_margin is None or part.worst_margin < total.worst_margin
    ):
        total.worst_margin = part.worst_margin


def replay(path: Path, limit: int | None = None, workers: int = 0) -> dict[str, Any]:
    started = time.monotonic()
    stream = records(path)
    head = next(stream)["header"]
    if head.get("schema") != "fixed-angle-tree/v1":
        raise RejectionError("unknown schema")
    program = build_program(head)
    statement = check_target_and_image(head, program)
    image = statement.pop("_image")
    radius = statement.pop("_radius")
    report = Report()
    if head.get("root_path"):
        raise RejectionError("a top-level tree must start at the empty cell")
    frontier = walk(
        program,
        stream=stream,
        fixed={},
        splits=head.get("split_depth") is not None,
        image=image,
        radius=radius,
        report=report,
        limit=limit,
    )
    tasks = [(path, head, index, recorded, limit) for index, recorded in enumerate(frontier)]
    if workers > 1 and len(tasks) > 1:
        with multiprocessing.get_context("spawn").Pool(workers) as pool:
            for part in pool.imap_unordered(replay_subtree, tasks):
                merge(report, part)
    else:
        for task in tasks:
            merge(report, replay_subtree(task))
    unresolved = sum(report.unresolved.values())
    verdict = "closed" if unresolved == 0 else "incomplete"
    return {
        "verdict": verdict,
        "tree": str(path),
        "leaves": dict(report.kinds),
        "subtree_files": len(frontier),
        "unresolved_by_reason": dict(report.unresolved),
        "leaf_depths": {str(k): v for k, v in sorted(report.depths.items())},
        "smallest_certified_margin": None
        if report.worst_margin is None
        else float(report.worst_margin),
        "largest_enclosure_reach_beyond_image": float(report.reach),
        "statement": statement,
        "reader_seconds": round(time.monotonic() - started, 3),
    }


def check_target_and_image(head: dict[str, Any], program: Program) -> dict[str, Any]:
    label = head["target"]["label"]
    fam = head["family"]
    left, right = Fraction(fam["left"]), Fraction(fam["right"])
    statement: dict[str, Any] = {
        "family": f"{program.axis_count} axis + {program.tilted_count} tilted",
        "half_tangent_box": [str(left), str(right)],
        "target_label": label,
        "target_upper": str(program.target),
        "_image": None,
        "_radius": None,
    }
    if label == "U":
        _, (_, side_hi), _, _, _ = witness_brackets()
        if program.target < side_hi:
            raise RejectionError("the header's upper end of U is below the reader's bracket")
        statement["target_is_at_least_U"] = True
    declared = head.get("image")
    if declared is None:
        return statement
    radius = Fraction(declared["radius"])
    if declared["name"] == "trump11":
        centres, (u_lo, u_hi), _ = trump_image(int(declared["rotation"]), declared["labels"])
        if radius != BC240_RHO or not declared["theorem"]:
            raise RejectionError("a Trump-degenerate leaf must use BC-240's rho as a theorem")
        if program.axis_count != 6 or program.tilted_count != 5:
            raise RejectionError("the Trump image needs the six-plus-five family")
        # |d theta / d t| = 2 / (1 + t^2) <= 2, so the angle window is inside rho
        angle_reach = 2 * max(u_hi - left, right - u_lo)
        if angle_reach >= radius:
            raise RejectionError("the angle box is not inside rho of Trump's tilt")
        statement["angle_reach_bound"] = float(angle_reach)
        statement["local_theorem"] = "BC-240 per-row radius, labelled anchored chart"
    elif declared["name"] == "goebel5":
        centres = goebel_image()
        if declared["theorem"] or program.count != 5:
            raise RejectionError("the n = 5 image is a capture statement, not a theorem")
        statement["capture_only"] = True
    else:
        raise RejectionError("unknown image")
    statement["image"] = {
        "name": declared["name"],
        "rotation": declared["rotation"],
        "labels": declared["labels"],
        "radius": str(radius),
    }
    statement["_image"] = centres
    statement["_radius"] = radius
    return statement


def walk(
    program: Program,
    *,
    stream: Iterable[dict[str, Any]],
    fixed: dict[tuple[int, int], int],
    splits: bool,
    image: list[Span] | None,
    radius: Fraction | None,
    report: Report,
    limit: int | None,
) -> list[list[list[int]]]:
    """Replay one file from the cell ``fixed``; return the frontier paths it hands on."""
    stack: list[Frame] = []
    path: dict[tuple[int, int], int] = dict(fixed)
    frontier: list[list[list[int]]] = []
    roots = 0
    for count, node in enumerate(stream):
        if limit is not None and count >= limit:
            raise RejectionError("stopped at the replay limit before the tree ended")
        option = node.get("o")
        if stack:
            frame = stack[-1]
            if type(option) is not int or not 0 <= option < frame.size or option in frame.seen:
                raise RejectionError(f"bad option {option!r} under pair {frame.pair}")
            frame.seen.add(option)
            path[frame.pair] = option
        else:
            roots += 1
            if roots > 1 or option is not None:
                raise RejectionError("the tree must have exactly one root")
        if "b" in node:
            i, j = node["b"]
            if not (type(i) is int and type(j) is int and 0 <= i < j < program.count):
                raise RejectionError(f"bad pair {node['b']!r}")
            if (i, j) in path:
                raise RejectionError(f"pair {(i, j)} branched twice on one path")
            if node["n"] != len(program.options(i, j)):
                raise RejectionError(f"pair {(i, j)} does not list all its candidate axes")
            stack.append(Frame((i, j), node["n"], set()))
            report.kinds["b"] += 1
            continue
        if "s" in node:
            if not splits or node["s"] != len(frontier):
                raise RejectionError("a frontier leaf is out of sequence or not declared")
            frontier.append([[i, j, option] for (i, j), option in path.items()])
            report.kinds["s"] += 1
        else:
            check_leaf(program, node, path=path, image=image, radius=radius, report=report)
        report.depths[len(path)] += 1
        while stack and len(stack[-1].seen) == stack[-1].size:
            del path[stack[-1].pair]
            stack.pop()
    if stack or roots != 1:
        raise RejectionError("the tree ended before every branch listed all its children")
    return frontier


def leaf_rows(
    program: Program, path: dict[tuple[int, int], int]
) -> dict[str, tuple[dict[int, Fraction], Fraction]]:
    rows = dict(program.base)
    for (i, j), option in path.items():
        rows[f"pair:{i}:{j}:{option}"] = program.pair(i, j, option)
    return rows


def check_leaf(
    program: Program,
    node: dict[str, Any],
    *,
    path: dict[tuple[int, int], int],
    image: list[Span] | None,
    radius: Fraction | None,
    report: Report,
) -> None:
    side_column = 2 * program.count
    if "u" in node:
        report.kinds["u"] += 1
        report.unresolved[str(node["u"])] += 1
        return
    rows = leaf_rows(program, path)
    if "c" in node:
        bound = evaluate(program, rows, node["c"], {side_column: Fraction(1)}, program.cap)
        if bound <= program.target:
            raise RejectionError(f"a dual bound {float(bound)} does not exceed the target")
        margin = bound - program.target
        report.kinds["c"] += 1
    elif "f" in node:
        margin = evaluate(program, rows, node["f"], {}, program.cap)
        if margin <= 0:
            raise RejectionError("a Farkas vector does not separate")
        report.kinds["f"] += 1
    elif "t" in node:
        if image is None or radius is None:
            raise RejectionError("a degenerate leaf needs a declared image")
        margin = check_enclosure(
            program, rows, certificate=node["t"], image=image, radius=radius, report=report
        )
        report.kinds["t"] += 1
    else:
        raise RejectionError(f"unknown node {sorted(node)!r}")
    if report.worst_margin is None or margin < report.worst_margin:
        report.worst_margin = margin


def check_enclosure(
    program: Program,
    rows: dict[str, tuple[dict[int, Fraction], Fraction]],
    *,
    certificate: dict[str, Any],
    image: list[Span],
    radius: Fraction,
    report: Report,
) -> Fraction:
    lows, highs = certificate["lo"], certificate["hi"]
    columns = 2 * program.count
    if len(lows) != columns or len(highs) != columns:
        raise RejectionError("an enclosure must bound every centre coordinate both ways")
    margin: Fraction | None = None
    for column in range(columns):
        centre_lo, centre_hi = image[column]
        low = evaluate(program, rows, lows[column], {column: Fraction(1)}, program.target)
        high = -evaluate(program, rows, highs[column], {column: Fraction(-1)}, program.target)
        slack = min(low - (centre_hi - radius), (centre_lo + radius) - high)
        if slack <= 0:
            raise RejectionError(f"coordinate {column} leaves the radius of the image")
        report.reach = max(report.reach, centre_lo - low, high - centre_hi)
        margin = slack if margin is None else min(margin, slack)
    assert margin is not None
    return margin


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("tree", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--workers", type=int, default=0)
    args = parser.parse_args(argv)
    try:
        result = replay(args.tree, args.limit, args.workers)
    except RejectionError as error:
        result = {"verdict": "rejected", "tree": str(args.tree), "reason": str(error)}
    text = json.dumps(result, indent=2)
    print(text)
    if args.out is not None:
        args.out.write_text(text + "\n", encoding="utf-8")
    return 0 if result["verdict"] != "rejected" else 1


if __name__ == "__main__":
    sys.exit(main())
