#!/usr/bin/env python3
"""Bring a regularized view to the source witness's own side, exactly, over `Q`.

Usage, from `packing/`, after
`uv run --frozen --all-extras --group dev python -m devtools.regularize_same_side`:

    WITNESS.yaml VIEW.json --output OUT.yaml [--mode relax|refuse] [--json]
    --survey 1..80 [--perturb 1e-12] [--json]

`VIEW.json` holds `{"packing": {"S": "...", "sq": [[x, y, degrees], ...]}}`, the shape
upstream's `atlas.compute_one` writes and the driver `regularize_evand.py` copies: the
view's squares as the generator printed them, centres and a rotation in degrees, in the
witness's frame.

Evan Daniel's regularizer places a view at `S*`, the 80-digit side of its KKT point, and
certifies a copy dilated by `1 + 1e-20`, so neither object is at the record's side. The
regularization policy's side relation `same` means `s_V = s_W` exactly, the witness's own
side; this module is stage 5 of the policy's automated pass and is the only way a view
earns that relation. It re-solves the view's tight contacts as exact equalities at `s_W`:

1. **The exact frame of the source.** `s_W` and an exact rational rotation `(c, s)`,
   `c^2 + s^2 = 1`, for each witness square. A rational witness is its own frame. A decimal
   centre-angle witness uses its 36-digit rational promotion at centre dilation 1, the
   first candidate `promote_rational` tries and the frame `regularize_axis_components`
   regularizes from; its side is that promotion's exact side, which the policy defines as
   `s_W` for a decimal witness. The promotion's feasibility is not checked here: the view
   is what is decided, not the source. A witness over a number field has no rational
   frame and is refused, `no-exact-frame`.
2. **Rotation matching.** Each view square's rotation, taken modulo 90 degrees, is mapped
   to an exact rotation: axis-aligned, `(1, 0)`, within a sine of `1e-9` of the axis
   (about `5.7e-8` degrees); otherwise the exact `(c, s)` of the lowest-index witness
   square whose rotation class agrees within the same tolerance, so a class the generator
   merged takes one rotation, turned by quarter turns into the quarter the view states. A
   view square that matches no class is refused, `unmatched-rotation`: a group merged to
   exactly 45 degrees, for one, has no rational pose at all, and a band the exact solve
   turned (0.0115 degrees at n = 70) matches nothing.
3. **The tight set.** At the generator's pose, in binary64 and with every rotation fixed
   at its exact match, a wall contact is a square's extent along `x` or `y` within `tight`
   of `0` or `s_W`, and a pair contact is a nearby pair whose best separating face normal,
   the one of either square's four with the largest gap as upstream's `reg.best_normal`
   chooses it, has a gap below `tight`. With rotations fixed each contact is linear in the
   `2n` centre coordinates with rational coefficients: along a normal `n`,
   `n . (c_j - c_i) = h_i(n) + h_j(n)` with `h` the support of a unit square of fixed
   rotation, rational because `(c, s)` is; a wall is `x_i = h_i(e_x)` or
   `x_i = s_W - h_i(e_x)`, and likewise for `y`.
4. **The exact solve.** Gaussian elimination over `Fraction` with the rows in one
   priority order: pair contacts, then walls toward the lower-left, then walls toward the
   upper-right, ties by square index; the pivot of a row is its lowest coordinate column.
   A dependent row is skipped. An inconsistent row refuses in `refuse` mode,
   `inconsistent-tight-set`; in `relax` mode it is skipped and left as a slack
   constraint, which the verification then has to find non-negative. Every coordinate no
   row pins is fixed at the generator's value rounded to `FREE_COORDINATE_PLACES` decimal
   places, so it is rational; the pinned ones follow exactly. Relaxing is what makes the
   side relation reachable at all: when `s_W > S*`, a chain of contacts that spans the box
   wall to wall at `S*` cannot also close at `s_W`, so one row of each such chain opens by
   `s_W - S*`, and the order above makes that row an upper-right wall. When `s_W < S*`, as
   at a decimal witness whose printed side truncates an irrational optimum, no packing
   exists at `s_W` and the verification refuses.
5. **Exact verification.** The pose is written as a rational centre-basis Witness/v2
   document at `s_W` and decided by both maintained exact routes,
   `sqpack.witness.exact_verify` and `check_rational_witness_independent`, which share no
   geometry code. Both refusing refuses the view, `overlap`; one refusing what the other
   accepts refuses it too, `routes-disagree`; both accepting is the status `same`. A pose
   whose exact coordinates are too long for Python to write as text is refused,
   `literal-too-large`.

**What decides.** The exact verification is the decision. The binary64 tight-set
detection only proposes which contacts to close, and a wrong proposal can only produce a
pose the verification refuses, never one it accepts wrongly. Nothing here shows that the
view is the same packing as the source: identity is measured elsewhere, by
`check_half_angle_area.arrangement_gap`, and the policy's decision table reads both. The
view is never written under `witnesses/` or `atlas/`, changes no side and promotes no
tier.

**The survey.** `--survey N..M` is the measurement the module was built with: each
witness's own pose, perturbed by `--perturb` so the detection has to work for it, is fed
back through `resolve`, and the outcomes are tallied by witness kind and refusal reason.
It is what says which records can reach `same` at all before any generator has run.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import time
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Literal

from strif import atomic_output_file

from devtools import check_rational_witness_independent as independent
from devtools.upper_bound_packets import RATIONAL_DIGITS
from sqpack.witness import (
    WitnessError,
    # The 36-digit rational pose at centre dilation 1, the one `promote_rational` tries
    # first and `regularize_axis_components._decimal_frame` regularizes from; built here
    # without that function's feasibility check because the view is what is decided.
    _promoted_candidate,  # pyright: ignore[reportPrivateUsage]
    exact_verify,
    load_witness,
    materialize_exact_witness,
    witness_document,
)

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
WITNESSES = ROOT / "witnesses"
WITNESS_SCHEMA = WITNESSES / "witness.schema.yaml"
KNOWN_BEST = WITNESSES / "known-best"

#: A view rotation within a sine of this of a rotation class, modulo 90, takes it: about
#: 5.7e-8 degrees, a thousand times below the policy's 1e-6 turn threshold, so a match
#: neither hides nor makes a turn, and wide enough for the drift the exact solve leaves on
#: rotations it does not turn (up to 7.5e-11 degrees at n = 146 in the full run of 12
#: October 2026, which a tolerance of 1e-12 degrees refused at 17 counts).
ROTATION_TOLERANCE_SINE = 1e-9
ROTATION_TOLERANCE_DEGREES = math.degrees(math.asin(ROTATION_TOLERANCE_SINE))
#: Decimal places a coordinate no row pins keeps of the generator's value.
FREE_COORDINATE_PLACES = 30
#: Default gap below which a contact at the generator's pose is proposed as tight.
TIGHT = 1e-9
#: Squared centre distance within which two unit squares can touch, with a margin.
REACH_SQUARED = 2.01
HALF = Fraction(1, 2)
AXIS: Rotation = (Fraction(1), Fraction(0))

type Rotation = tuple[Fraction, Fraction]
type Mode = Literal["refuse", "relax"]
type Status = Literal["same", "refused"]


@dataclass(frozen=True)
class GeneratorPose:
    """A view square as the generator printed it, in the witness's frame."""

    x: str
    """Decimal text, 50 or more digits from upstream's `mpmath.nstr`."""
    y: str
    degrees: str
    """The rotation in degrees, any representative modulo 90."""


@dataclass(frozen=True)
class SameSideOutcome:
    status: Status
    reason: str | None
    """`unmatched-rotation`, `inconsistent-tight-set`, `overlap`, `routes-disagree`,
    `literal-too-large` or `no-exact-frame`."""
    side: Fraction | None
    """`s_W` when the status is `same`."""
    witness: dict[str, Any] | None
    """The Witness/v2 record (rational centre-basis at `s_W`), for `witness_document`."""
    report: dict[str, Any]


class SameSideError(Exception):
    """A typed refusal, turned into a `SameSideOutcome` by `resolve`."""

    def __init__(self, reason: str, detail: str, **extra: Any):
        super().__init__(detail)
        self.reason = reason
        self.detail = detail
        self.extra = extra


# --------------------------------------------------------------------------------------
# Exact arithmetic helpers
# --------------------------------------------------------------------------------------


def literal(value: Fraction) -> str:
    """The witness format's rational literal."""
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def decimal_text(value: Fraction, digits: int = 40) -> str:
    """`value` to `digits` significant digits, rounded to nearest."""
    with localcontext() as context:
        context.prec = digits
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def plain_decimal(value: Fraction, places: int) -> str:
    """`value` as a plain decimal with `places` places, never in exponent form."""
    scaled = round(value * 10**places)
    sign = "-" if scaled < 0 else ""
    digits = str(abs(scaled)).rjust(places + 1, "0")
    return f"{sign}{digits[:-places]}.{digits[-places:]}" if places else f"{sign}{digits}"


def rounded_fraction(text: str, places: int = FREE_COORDINATE_PLACES) -> Fraction:
    """A decimal literal rounded to `places` decimal places, half to even."""
    return Fraction(round(Fraction(text) * 10**places), 10**places)


def turn(rotation: Rotation, quarter_turns: int) -> Rotation:
    """`rotation` turned counter-clockwise by `quarter_turns` right angles."""
    c, s = rotation
    return ((c, s), (-s, c), (-c, -s), (s, -c))[quarter_turns % 4]


def support(rotation: Rotation, normal: Rotation) -> Fraction:
    """Half-width of a unit square of this rotation along the unit direction `normal`."""
    c, s = rotation
    nx, ny = normal
    return (abs(nx * c + ny * s) + abs(-nx * s + ny * c)) / 2


def support_f(rotation: tuple[float, float], normal: tuple[float, float]) -> float:
    c, s = rotation
    nx, ny = normal
    return 0.5 * (abs(nx * c + ny * s) + abs(-nx * s + ny * c))


def degrees_of(rotation: Rotation) -> float:
    c, s = rotation
    return math.degrees(math.atan2(float(s), float(c)))


def class_distance(left: float, right: float) -> float:
    """Distance between two rotations in degrees, modulo a quarter turn."""
    difference = (left - right) % 90.0
    return min(difference, 90.0 - difference)


def circular_distance(left: float, right: float) -> float:
    """Distance between two rotations in degrees, modulo a full turn."""
    difference = (left - right) % 360.0
    return min(difference, 360.0 - difference)


def corners_of(center: tuple[Fraction, Fraction], rotation: Rotation) -> list[Point]:
    """The four corners, counter-clockwise from the lower-left: this module's own
    expansion, so the independent route decides geometry it did not receive from
    `sqpack`."""
    x, y = center
    c, s = rotation
    return [
        (x + c * a - s * b, y + s * a + c * b)
        for a, b in ((-HALF, -HALF), (HALF, -HALF), (HALF, HALF), (-HALF, HALF))
    ]


type Point = tuple[Fraction, Fraction]


# --------------------------------------------------------------------------------------
# 1. The exact frame of the source
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Frame:
    """The source witness's exact rational frame: `s_W` and one rotation per square."""

    kind: str
    """`rational` or `decimal`, the witness's scalar kind."""
    side: Fraction
    """`s_W`."""
    reported_side: Fraction
    """The side the witness prints; equal to `side` for a rational witness."""
    centers: list[Point]
    rotations: list[Rotation]
    ids: list[Any]
    derivation: str


def witness_kind(witness: Mapping[str, Any]) -> str:
    """The witness's kind as the survey tallies it."""
    kind = str(witness["scalar"]["kind"])
    if kind == "rational":
        return f"rational-{witness['representation']}"
    return kind


def _rotation_of(corners: Sequence[Point]) -> Rotation:
    (ax, ay), (bx, by) = corners[0], corners[1]
    c, s = bx - ax, by - ay
    if c * c + s * s != 1:
        raise SameSideError(
            "no-exact-frame", "a source square's first edge is not an exact unit vector"
        )
    return c, s


def _center_of(corners: Sequence[Point]) -> Point:
    return sum((x for x, _ in corners), Fraction(0)) / 4, sum(
        (y for _, y in corners), Fraction(0)
    ) / 4


def exact_frame(witness: Mapping[str, Any]) -> Frame:
    """The frame the policy defines: the witness's own, or its 36-digit promotion."""
    kind = str(witness["scalar"]["kind"])
    if witness.get("square_size") != "1":
        raise SameSideError("no-exact-frame", "the frame is for unit squares only")
    reported_side = Fraction(str(witness["side"])) if isinstance(witness["side"], str) else None
    if kind == "rational" and reported_side is not None:
        expanded, side = materialize_exact_witness(witness)
        if not isinstance(side, Fraction):
            raise SameSideError(
                "no-exact-frame", "a rational witness must have a rational side"
            )
        squares: list[list[Point]] = []
        for square in expanded:
            parsed: list[Point] = []
            for x, y in square:
                if not isinstance(x, Fraction) or not isinstance(y, Fraction):
                    raise SameSideError("no-exact-frame", "rational corners expected")
                parsed.append((x, y))
            squares.append(parsed)
        derivation = (
            "the witness's own rational corners"
            if witness["representation"] == "corners"
            else "the witness's own rational centre-basis pose"
        )
    elif kind == "decimal" and reported_side is not None:
        try:
            promoted, side = _promoted_candidate(
                witness, rational_digits=RATIONAL_DIGITS, dilation=Fraction(1)
            )
        except WitnessError as error:
            raise SameSideError(
                "no-exact-frame", f"no {RATIONAL_DIGITS}-digit rational pose: {error}"
            ) from error
        squares = [list(square) for square in promoted]
        derivation = (
            f"the {RATIONAL_DIGITS}-digit rational pose at centre dilation 1, the first "
            "candidate promote_rational tries; its exact side is s_W"
        )
    else:
        raise SameSideError(
            "no-exact-frame",
            f"{kind!r} geometry has no rational frame: a field element is not a rational "
            "rotation and an enclosure proves no equality",
        )
    return Frame(
        kind=kind,
        side=side,
        reported_side=reported_side,
        centers=[_center_of(square) for square in squares],
        rotations=[_rotation_of(square) for square in squares],
        ids=[square["id"] for square in witness["squares"]],
        derivation=derivation,
    )


# --------------------------------------------------------------------------------------
# 2. Rotation matching
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Matched:
    """One view square's exact rotation and where it came from."""

    rotation: Rotation
    source: int | None
    """Index of the witness square whose rotation was taken; `None` for axis-aligned."""
    quarter_turns: int


def match_rotations(
    frame: Frame,
    view: Sequence[GeneratorPose],
    *,
    tolerance: float = ROTATION_TOLERANCE_DEGREES,
) -> list[Matched]:
    """Each view square's exact rotation from the frame, or `unmatched-rotation`."""
    classes = [degrees_of(rotation) for rotation in frame.rotations]
    matched: list[Matched] = []
    for index, pose in enumerate(view):
        degrees = float(pose.degrees)
        if class_distance(degrees, 0.0) <= tolerance:
            matched.append(Matched(AXIS, None, 0))
            continue
        candidates = sorted(
            (class_distance(degrees, angle), j)
            for j, angle in enumerate(classes)
            if class_distance(degrees, angle) <= tolerance
        )
        if not candidates:
            nearest = min(
                (class_distance(degrees, angle), j) for j, angle in enumerate(classes)
            )
            raise SameSideError(
                "unmatched-rotation",
                f"view square {index + 1} at {degrees!r} degrees matches no rotation of the "
                f"witness; the nearest class is square {frame.ids[nearest[1]]}, "
                f"{nearest[0]:.3e} degrees away",
                square=index + 1,
                degrees=degrees,
                nearest_degrees=nearest[0],
            )
        # The class representative is the lowest-index witness square in the class, so
        # a group the generator merged within the tolerance takes one rotation, as the
        # witness's own noise within a class is not a structure worth 36 distinct
        # rotations in one chain (n = 68 holds 36 tilted squares in 11 classes).
        source = min(j for _d, j in candidates)
        quarter = min(
            range(4), key=lambda k: circular_distance(degrees, classes[source] + 90.0 * k)
        )
        matched.append(Matched(turn(frame.rotations[source], quarter), source, quarter))
    return matched


# --------------------------------------------------------------------------------------
# 3. The tight set
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Row:
    """One linear equality in the `2n` centre coordinates, with its gap orientation."""

    kind: str
    """`pair` or `wall`."""
    coefficients: dict[int, Fraction]
    """Column `2i` is `x_i`, `2i + 1` is `y_i`."""
    rhs: Fraction
    gap_sign: int
    """`+1` when the contact's gap is `lhs - rhs`, `-1` when it is `rhs - lhs`."""
    label: dict[str, Any] = field(default_factory=dict)
    priority: tuple[int, ...] = ()

    def gap(self, values: Mapping[int, Fraction]) -> Fraction:
        lhs = sum(
            (coefficient * values[column] for column, coefficient in self.coefficients.items()),
            Fraction(0),
        )
        return self.gap_sign * (lhs - self.rhs)


def _best_normal(
    i: int, j: int, x: Sequence[float], y: Sequence[float], cs: Sequence[tuple[float, float]]
) -> tuple[float, int, int, int]:
    """Upstream's `best_normal`: the face normal of either square with the largest gap.

    Returns the gap and the normal's identity: whose face, which of its two normals and
    the sign that orients it from `i` toward `j`.
    """
    dx, dy = x[j] - x[i], y[j] - y[i]
    best: tuple[float, int, int, int] | None = None
    for own in (i, j):
        c, s = cs[own]
        for face, (fx, fy) in enumerate(((c, s), (-s, c))):
            sign = -1 if fx * dx + fy * dy < 0 else 1
            normal = (sign * fx, sign * fy)
            along = normal[0] * dx + normal[1] * dy
            gap = along - support_f(cs[i], normal) - support_f(cs[j], normal)
            if best is None or gap > best[0]:
                best = (gap, own, face, sign)
    if best is None:  # Defensive: two squares always have four normals.
        raise ValueError("no normal")
    return best


def _sparse(entries: Iterable[tuple[int, Fraction]]) -> dict[int, Fraction]:
    return {column: value for column, value in entries if value != 0}


def tight_rows(
    frame: Frame,
    view: Sequence[GeneratorPose],
    matched: Sequence[Matched],
    *,
    tight: float = TIGHT,
) -> list[Row]:
    """The contacts tight at the generator's pose, as exact rows in priority order."""
    n = len(view)
    x = [float(pose.x) for pose in view]
    y = [float(pose.y) for pose in view]
    cs = [(float(m.rotation[0]), float(m.rotation[1])) for m in matched]
    side = float(frame.side)
    pairs: list[Row] = []
    low: list[Row] = []
    high: list[Row] = []
    for i in range(n):
        for axis, (z, normal) in enumerate(((x, AXIS), (y, turn(AXIS, 1)))):
            extent = support(matched[i].rotation, normal)
            extent_f = float(extent)
            column = 2 * i + axis
            if abs(z[i] - extent_f) < tight:
                low.append(
                    Row(
                        "wall",
                        {column: Fraction(1)},
                        extent,
                        1,
                        {"square": i + 1, "axis": "xy"[axis], "wall": "low"},
                        (1, i, axis),
                    )
                )
            if abs(side - extent_f - z[i]) < tight:
                high.append(
                    Row(
                        "wall",
                        {column: Fraction(1)},
                        frame.side - extent,
                        -1,
                        {"square": i + 1, "axis": "xy"[axis], "wall": "high"},
                        (2, i, axis),
                    )
                )
    for i in range(n):
        for j in range(i + 1, n):
            if (x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2 > REACH_SQUARED:
                continue
            gap, own, face, sign = _best_normal(i, j, x, y, cs)
            if gap >= tight:
                continue
            nx, ny = turn(matched[own].rotation, face)
            nx, ny = sign * nx, sign * ny
            normal: Rotation = (nx, ny)
            rhs = support(matched[i].rotation, normal) + support(matched[j].rotation, normal)
            pairs.append(
                Row(
                    "pair",
                    _sparse([(2 * i, -nx), (2 * i + 1, -ny), (2 * j, nx), (2 * j + 1, ny)]),
                    rhs,
                    1,
                    {
                        "squares": [i + 1, j + 1],
                        "normal": {"of": own + 1, "face": face, "sign": sign},
                        "gap_at_generator": gap,
                    },
                    (0, i, j),
                )
            )
    return sorted(pairs + low + high, key=lambda row: row.priority)


# --------------------------------------------------------------------------------------
# 4. The exact solve
# --------------------------------------------------------------------------------------


@dataclass
class Solution:
    values: dict[int, Fraction]
    used: list[Row]
    dependent: list[Row]
    relaxed: list[Row]
    free_columns: list[int]


def solve_rows(
    rows: Sequence[Row], n: int, generator: Sequence[tuple[Fraction, Fraction]], *, mode: Mode
) -> Solution:
    """Exact elimination in row order; free coordinates take the generator's values."""
    pivots: list[tuple[int, dict[int, Fraction], Fraction]] = []
    used: list[Row] = []
    dependent: list[Row] = []
    relaxed: list[Row] = []
    for row in rows:
        reduced = dict(row.coefficients)
        rhs = row.rhs
        for column, coefficients, pivot_rhs in pivots:
            factor = reduced.get(column)
            if factor is None:
                continue
            factor /= coefficients[column]
            for other, value in coefficients.items():
                remaining = reduced.get(other, Fraction(0)) - factor * value
                if remaining == 0:
                    reduced.pop(other, None)
                else:
                    reduced[other] = remaining
            rhs -= factor * pivot_rhs
        if not reduced:
            if rhs == 0:
                dependent.append(row)
            elif mode == "refuse":
                raise SameSideError(
                    "inconsistent-tight-set",
                    f"a tight {row.kind} contact cannot close exactly at s_W with the "
                    f"others, by {decimal_text(rhs, 6)}: {row.label}",
                    row=row.label,
                    residual=decimal_text(rhs, 20),
                )
            else:
                relaxed.append(row)
            continue
        pivots.append((min(reduced), reduced, rhs))
        used.append(row)
    pinned = {column for column, _c, _r in pivots}
    values: dict[int, Fraction] = {}
    free_columns: list[int] = []
    for i in range(n):
        for axis in range(2):
            column = 2 * i + axis
            if column not in pinned:
                values[column] = generator[i][axis]
                free_columns.append(column)
    for column, coefficients, rhs in reversed(pivots):
        total = rhs
        for other, value in coefficients.items():
            if other != column:
                total -= value * values[other]
        values[column] = total / coefficients[column]
    return Solution(values, used, dependent, relaxed, free_columns)


#: Rounds the promotion loop may take; an infeasible chain would otherwise walk them all.
MAX_PROMOTION_ROUNDS = 16


def settle(
    rows: Sequence[Row],
    n: int,
    generator: Sequence[tuple[Fraction, Fraction]],
    *,
    mode: Mode,
    max_rounds: int = MAX_PROMOTION_ROUNDS,
) -> tuple[Solution, list[Row], int]:
    """`solve_rows`, repeated in `relax` mode until no relaxed row would be penetrated.

    A relaxed row's slack has a sign, and the priority order does not know it: at a
    decimal witness with squares at 45 degrees the 36-digit rotation has `c != s`, so of
    the corners that touch one tilted edge at `S*` only one can touch it exactly, and the
    order can close the wrong one, leaving the other `1e-36` inside the square. A relaxed
    row with negative slack is therefore promoted ahead of every other row and the solve
    repeated, so that one of the rows it conflicted with opens instead; the loop ends when
    every relaxed row has non-negative slack, when a promotion would repeat, or after
    `max_rounds`. Returns the solution, the promoted rows and the rounds taken. In
    `refuse` mode there is one round.
    """
    promoted: list[Row] = []
    rounds = 0
    while True:
        rounds += 1
        keys = {row.priority for row in promoted}
        order = [*promoted, *(row for row in rows if row.priority not in keys)]
        solution = solve_rows(order, n, generator, mode=mode)
        negative = [row for row in solution.relaxed if row.gap(solution.values) < 0]
        repeated = any(row.priority in keys for row in negative)
        if mode == "refuse" or not negative or repeated or rounds >= max_rounds:
            return solution, promoted, rounds
        promoted = [*negative, *promoted]


# --------------------------------------------------------------------------------------
# 5. The witness and its verification
# --------------------------------------------------------------------------------------


def same_side_witness(
    source: Mapping[str, Any],
    frame: Frame,
    centers: Sequence[Point],
    matched: Sequence[Matched],
    *,
    view_id: str,
) -> dict[str, Any]:
    """The re-solved view as a rational centre-basis Witness/v2 record at `s_W`."""
    retained = source.get("source") or {}
    origin = {"path": str(retained.get("path") or "unrecorded")}
    for key in ("key", "url", "retrieved"):
        value = retained.get(key)
        if isinstance(value, str) and value:
            origin[key] = value
    return {
        "id": view_id,
        "n": len(centers),
        "side": literal(frame.side),
        "square_size": "1",
        "representation": "center-basis",
        "scalar": {"kind": "rational"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": [
            {
                "id": frame.ids[index] if index < len(frame.ids) else index + 1,
                "center": [literal(x), literal(y)],
                "basis": [literal(m.rotation[0]), literal(m.rotation[1])],
            }
            for index, ((x, y), m) in enumerate(zip(centers, matched, strict=True))
        ],
        "claim": {
            "coordinate_provenance": "reported",
            "method": "exact-algebraic",
            "limitations": (
                "A regularized view brought to the source witness's side exactly over Q: "
                "every rotation is the witness's own exact rational rotation or "
                "axis-aligned, the contacts closed at the generator's pose are re-solved as "
                "exact equalities at the witness's side, and the pose is decided by two "
                "exact routes. A drawing frame at the record's side, not a new bound; "
                "whether it is the same packing as the source is measured elsewhere."
            ),
        },
        "source": origin,
    }


def verify_both(
    witness: Mapping[str, Any],
    centers: Sequence[Point],
    matched: Sequence[Matched],
    side: Fraction,
) -> dict[str, Any]:
    """Both exact decisions of the pose, each on its own geometry."""
    started = time.perf_counter()
    result, report = exact_verify(witness)
    first_seconds = time.perf_counter() - started
    started = time.perf_counter()
    corners = [
        corners_of(center, m.rotation) for center, m in zip(centers, matched, strict=True)
    ]
    second = independent.check_squares(corners, side)
    second_seconds = time.perf_counter() - started
    return {
        "exact_verify": {
            "passed": bool(report.valid),
            "pairs_tested": report.pairs_tested,
            "touching_pairs": report.touching_pairs,
            "container_contacts": report.container_contacts,
            "minimum_best_pair_gap": str(result["minimum_best_pair_gap"]),
            "failures": [list(failure) for failure in report.failures[:8]],
            "seconds": round(first_seconds, 3),
        },
        "independent": {
            "passed": bool(second["verification_passed"]),
            "pairs_tested": second["pairs_tested"],
            "minimum_best_pair_gap": second["minimum_best_pair_gap"],
            "minimum_containment_clearance": second["minimum_containment_clearance"],
            "failures": list(second["failures"])[:8],
            "seconds": round(second_seconds, 3),
        },
    }


# --------------------------------------------------------------------------------------
# The whole: resolve
# --------------------------------------------------------------------------------------


def _row_record(row: Row, values: Mapping[int, Fraction] | None = None) -> dict[str, Any]:
    record: dict[str, Any] = {"kind": row.kind, **row.label}
    if values is not None:
        gap = row.gap(values)
        record["slack"] = literal(gap)
        record["slack_decimal"] = decimal_text(gap, 6)
    return record


def resolve(
    source_witness: Mapping[str, Any],
    view: Sequence[GeneratorPose],
    *,
    mode: Mode = "relax",
    tight: float = TIGHT,
    view_id: str | None = None,
) -> SameSideOutcome:
    """Bring `view` to the source witness's side exactly, or say why it cannot be."""
    try:
        return _resolve(source_witness, view, mode=mode, tight=tight, view_id=view_id)
    except ValueError as error:
        # Python refuses to write an integer longer than its digit limit as text; a pose
        # whose exact coordinates need that many digits is no drawing frame (n = 270 and
        # 272 in the full run of 12 October 2026).
        if "integer string conversion" not in str(error):
            raise
        detail = f"an exact coordinate is too long to write: {error}"
        report = {
            "n": len(view),
            "mode": mode,
            "tight": tight,
            "refusal": {"reason": "literal-too-large", "detail": detail},
        }
        return SameSideOutcome("refused", "literal-too-large", None, None, report)


def _resolve(
    source_witness: Mapping[str, Any],
    view: Sequence[GeneratorPose],
    *,
    mode: Mode,
    tight: float,
    view_id: str | None,
) -> SameSideOutcome:
    started = time.perf_counter()
    seconds: dict[str, float] = {}
    report: dict[str, Any] = {
        "n": len(view),
        "mode": mode,
        "tight": tight,
        "rotation_tolerance_degrees": ROTATION_TOLERANCE_DEGREES,
        "free_coordinate_places": FREE_COORDINATE_PLACES,
        "seconds": seconds,
    }
    if view_id is None:
        view_id = f"{source_witness['id']}-regularized"

    def refused(error: SameSideError) -> SameSideOutcome:
        report["refusal"] = {"reason": error.reason, "detail": error.detail, **error.extra}
        seconds["total"] = round(time.perf_counter() - started, 3)
        return SameSideOutcome("refused", error.reason, None, None, report)

    try:
        frame = exact_frame(source_witness)
    except SameSideError as error:
        report["source"] = {
            "id": source_witness.get("id"),
            "kind": witness_kind(source_witness),
        }
        return refused(error)
    seconds["frame"] = round(time.perf_counter() - started, 3)
    if len(view) != len(frame.rotations):
        raise ValueError(
            f"the view has {len(view)} squares, the witness {len(frame.rotations)}"
        )
    n = len(view)
    generator = [(rounded_fraction(pose.x), rounded_fraction(pose.y)) for pose in view]
    # The generator's own box, from each view square's own angle: before matching, the
    # view's rotations need not be the witness's, nor in the witness's square order.
    box = max(
        max(
            abs(float(pose.x)) + support_f(own, (1.0, 0.0)),
            abs(float(pose.y)) + support_f(own, (0.0, 1.0)),
        )
        for pose in view
        for own in [
            (
                math.cos(math.radians(float(pose.degrees))),
                math.sin(math.radians(float(pose.degrees))),
            )
        ]
    )
    report["source"] = {
        "id": source_witness.get("id"),
        "kind": witness_kind(source_witness),
        "frame": frame.derivation,
    }
    report["side"] = {
        "exact": literal(frame.side),
        "decimal": decimal_text(frame.side),
        "reported": literal(frame.reported_side),
        "side_minus_reported": decimal_text(frame.side - frame.reported_side, 6),
        "generator_box": box,
        "side_minus_generator_box": float(frame.side) - box,
    }

    phase = time.perf_counter()
    try:
        matched = match_rotations(frame, view)
    except SameSideError as error:
        return refused(error)
    seconds["match"] = round(time.perf_counter() - phase, 3)
    report["rotations"] = {
        "axis": sum(1 for m in matched if m.source is None),
        "matched": sum(1 for m in matched if m.source is not None),
        "classes": [None if m.source is None else frame.ids[m.source] for m in matched],
        "quarter_turns": [m.quarter_turns for m in matched],
    }

    phase = time.perf_counter()
    rows = tight_rows(frame, view, matched, tight=tight)
    seconds["tight_set"] = round(time.perf_counter() - phase, 3)
    phase = time.perf_counter()
    try:
        solution, promoted, rounds = settle(rows, n, generator, mode=mode)
    except SameSideError as error:
        report["rows"] = {
            "candidates": len(rows),
            "pairs": sum(1 for row in rows if row.kind == "pair"),
            "walls": sum(1 for row in rows if row.kind == "wall"),
        }
        return refused(error)
    seconds["solve"] = round(time.perf_counter() - phase, 3)
    centers = [(solution.values[2 * i], solution.values[2 * i + 1]) for i in range(n)]
    displacements = [
        math.hypot(float(x) - float(pose.x), float(y) - float(pose.y))
        for (x, y), pose in zip(centers, view, strict=True)
    ]
    report["rows"] = {
        "candidates": len(rows),
        "pairs": sum(1 for row in rows if row.kind == "pair"),
        "walls": sum(1 for row in rows if row.kind == "wall"),
        "used": len(solution.used),
        "dependent": len(solution.dependent),
        "relaxed": [_row_record(row, solution.values) for row in solution.relaxed],
        "promoted": [_row_record(row) for row in promoted],
        "rounds": rounds,
        "free_coordinates": len(solution.free_columns),
    }
    report["displacement"] = {
        "max": max(displacements, default=0.0),
        "moved_beyond_1e-6": sum(1 for d in displacements if d > 1e-6),
        "max_literal_digits": max(
            (
                len(str(abs(v.numerator))) + len(str(v.denominator))
                for v in solution.values.values()
            ),
            default=0,
        ),
    }

    phase = time.perf_counter()
    witness = same_side_witness(source_witness, frame, centers, matched, view_id=view_id)
    verdicts = verify_both(witness, centers, matched, frame.side)
    seconds["verify"] = round(time.perf_counter() - phase, 3)
    report["verdicts"] = verdicts
    seconds["total"] = round(time.perf_counter() - started, 3)
    passed = (verdicts["exact_verify"]["passed"], verdicts["independent"]["passed"])
    if not all(passed):
        failures = verdicts["exact_verify"]["failures"] or verdicts["independent"]["failures"]
        # One route accepting what the other refuses is a disagreement between checkers
        # that share no geometry code, worth naming apart from a plain overlap.
        reason = "routes-disagree" if any(passed) else "overlap"
        report["refusal"] = {
            "reason": reason,
            "detail": f"the re-solved pose is not a packing at s_W: {failures[:3]}",
        }
        return SameSideOutcome("refused", reason, None, None, report)
    witness["claim"]["coordinate_provenance"] = "verified"
    witness["certificate"] = {
        "kind": "same-side-view",
        "side_relation": "same",
        "derived_from": source_witness["id"],
        "exact_frame": {"kind": frame.kind, "derivation": frame.derivation},
        "resolve": {
            "tool": "devtools.regularize_same_side",
            "mode": mode,
            "tight": tight,
            "rows_used": len(solution.used),
            "rows_relaxed": len(solution.relaxed),
            "rows_promoted": len(promoted),
            "free_coordinates": len(solution.free_columns),
            "free_coordinate_places": FREE_COORDINATE_PLACES,
        },
        "replay": "uv run --frozen packing-witness verify <this file>",
    }
    return SameSideOutcome("same", None, frame.side, witness, report)


# --------------------------------------------------------------------------------------
# Poses from a witness or a view file, for the survey and the driver
# --------------------------------------------------------------------------------------


def witness_poses(witness: Mapping[str, Any]) -> list[GeneratorPose]:
    """The witness's own pose in its exact frame, printed as a generator would print it."""
    frame = exact_frame(witness)
    return [
        GeneratorPose(plain_decimal(x, 50), plain_decimal(y, 50), repr(degrees_of(rotation)))
        for (x, y), rotation in zip(frame.centers, frame.rotations, strict=True)
    ]


def perturbed(
    poses: Sequence[GeneratorPose],
    amount: float,
    *,
    seed: int = 0,
    squares: Mapping[int, tuple[float, float]] | None = None,
) -> list[GeneratorPose]:
    """`poses` with each centre moved by up to `amount` in each coordinate, pseudo-randomly
    from `seed`, and the squares in `squares` (zero-based) by their own `(x, y)` amounts."""
    generator = random.Random(seed)
    result: list[GeneratorPose] = []
    for index, pose in enumerate(poses):
        scale_x, scale_y = (squares or {}).get(index, (amount, amount))
        dx = Fraction(generator.uniform(-scale_x, scale_x))
        dy = Fraction(generator.uniform(-scale_y, scale_y))
        result.append(
            GeneratorPose(
                plain_decimal(Fraction(pose.x) + dx, 50),
                plain_decimal(Fraction(pose.y) + dy, 50),
                pose.degrees,
            )
        )
    return result


def view_from_json(data: Mapping[str, Any]) -> list[GeneratorPose]:
    """The poses in upstream's `atlas.compute_one` JSON shape."""
    packing = data.get("packing", data)
    squares = packing["sq"]
    return [GeneratorPose(str(x), str(y), str(degrees)) for x, y, degrees in squares]


# --------------------------------------------------------------------------------------
# The survey
# --------------------------------------------------------------------------------------


def survey(
    counts: Iterable[int],
    *,
    witnesses: Path = KNOWN_BEST,
    perturb: float = 1e-12,
    mode: Mode = "relax",
) -> dict[str, Any]:
    """Each witness's own pose, perturbed, through `resolve`; outcomes by kind and reason."""
    rows: list[dict[str, Any]] = []
    tally: dict[str, dict[str, int]] = {}
    for n in counts:
        path = witnesses / f"n-{n:03d}.yaml"
        witness = load_witness(path, fallback_schema=WITNESS_SCHEMA)
        kind = witness_kind(witness)
        try:
            poses = perturbed(witness_poses(witness), perturb, seed=n)
        except SameSideError as error:
            refusal = {"reason": error.reason, "detail": error.detail}
            outcome = SameSideOutcome("refused", error.reason, None, None, {"refusal": refusal})
        else:
            outcome = resolve(witness, poses, mode=mode)
        label = outcome.status if outcome.reason is None else f"refused/{outcome.reason}"
        tally.setdefault(kind, {})[label] = tally.setdefault(kind, {}).get(label, 0) + 1
        report = outcome.report
        rows.append(
            {
                "n": n,
                "kind": kind,
                "outcome": label,
                "relaxed": len((report.get("rows") or {}).get("relaxed", [])),
                "max_displacement": (report.get("displacement") or {}).get("max"),
                "seconds": (report.get("seconds") or {}).get("total"),
                "detail": (report.get("refusal") or {}).get("detail"),
            }
        )
    return {"perturb": perturb, "mode": mode, "tally": tally, "rows": rows}


def survey_text(result: Mapping[str, Any]) -> str:
    lines = [f"survey: perturb {result['perturb']}, mode {result['mode']}"]
    for kind, outcomes in sorted(result["tally"].items()):
        lines.append(f"  {kind}:")
        lines.extend(f"    {label}: {count}" for label, count in sorted(outcomes.items()))
    for row in result["rows"]:
        detail = f"  {row['detail']}" if row["detail"] else ""
        lines.append(
            f"  n={row['n']:3d} {row['kind']:22s} {row['outcome']:32s} "
            f"relaxed {row['relaxed']:2d} max move {row['max_displacement']!s:10s} "
            f"{row['seconds']} s{detail}"
        )
    return "\n".join(lines)


# --------------------------------------------------------------------------------------
# Command line
# --------------------------------------------------------------------------------------


def _parse_range(text: str) -> list[int]:
    if ".." in text:
        first, last = text.split("..", 1)
        return list(range(int(first), int(last) + 1))
    return [int(text)]


def parser() -> argparse.ArgumentParser:
    description = "Bring a regularized view to the source witness's side exactly over Q."
    result = argparse.ArgumentParser(description=description)
    result.add_argument("witness", nargs="?", type=Path, help="the source Witness/v2 file")
    result.add_argument("view", nargs="?", type=Path, help="the view, atlas.compute_one JSON")
    result.add_argument("--output", type=Path, help="where to write the same-side view")
    result.add_argument("--mode", choices=("relax", "refuse"), default="relax")
    result.add_argument("--tight", type=float, default=TIGHT)
    result.add_argument("--view-id", help="the view's id; default <witness id>-regularized")
    result.add_argument("--json", action="store_true", help="print the report as JSON")
    result.add_argument("--survey", metavar="N..M", help="survey the witnesses' own poses")
    result.add_argument("--perturb", type=float, default=1e-12, help="survey perturbation")
    result.add_argument("--witnesses", type=Path, default=KNOWN_BEST)
    return result


def _guard_output(path: Path) -> Path:
    resolved = path.resolve()
    for forbidden in (WITNESSES, ROOT / "atlas"):
        if resolved == forbidden.resolve() or forbidden.resolve() in resolved.parents:
            raise ValueError(f"a same-side view may not be written under {forbidden}")
    return resolved


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.survey:
        result = survey(
            _parse_range(args.survey),
            witnesses=args.witnesses,
            perturb=args.perturb,
            mode=args.mode,
        )
        print(json.dumps(result, indent=2) if args.json else survey_text(result))
        return 0
    if args.witness is None or args.view is None:
        parser().error("WITNESS.yaml and VIEW.json are required without --survey")
    witness = load_witness(args.witness, fallback_schema=WITNESS_SCHEMA)
    view = view_from_json(json.loads(args.view.read_text(encoding="utf-8")))
    outcome = resolve(witness, view, mode=args.mode, tight=args.tight, view_id=args.view_id)
    if outcome.witness is not None and args.output is not None:
        output = _guard_output(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        schema = WITNESS_SCHEMA.relative_to(output.parent, walk_up=True).as_posix()
        with atomic_output_file(output) as temporary:
            temporary.write_text(
                witness_document(outcome.witness, schema=schema), encoding="utf-8"
            )
        outcome.report["output"] = str(output)
    if args.json:
        record = {"status": outcome.status, "reason": outcome.reason, **outcome.report}
        print(json.dumps(record, indent=2, default=str))
    else:
        print(summary(outcome))
    return 0 if outcome.status == "same" else 1


def summary(outcome: SameSideOutcome) -> str:
    """One paragraph of an outcome for a terminal."""
    report = outcome.report
    status = (
        outcome.status if outcome.reason is None else f"{outcome.status} ({outcome.reason})"
    )
    lines = [f"{status}: n = {report['n']}, side {(report.get('side') or {}).get('decimal')}"]
    rows = report.get("rows")
    if rows and "used" in rows:
        lines.append(
            f"  rows: {rows['used']} used, {rows['dependent']} dependent, "
            f"{len(rows['relaxed'])} relaxed, {len(rows['promoted'])} promoted, "
            f"{rows['free_coordinates']} free coordinates"
        )
        lines.append(f"  largest centre displacement {report['displacement']['max']:.3e}")
    if "refusal" in report:
        lines.append(f"  {report['refusal']['detail']}")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
