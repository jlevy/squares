#!/usr/bin/env python3
"""Re-solve a regularized view over Q at exactly the side of the witness it was drawn from.

Usage, from `packing/`, after
`uv run --frozen --all-extras --group dev python -m devtools.regularize_same_side`:

    witnesses/known-best/n-070.yaml [--relax] [--json]
    witnesses/known-best/n-026.yaml --view-json n-026.json.gz [--relax] [--json]

Without `--view-json` the approximate view is the witness's own pose in binary64, which
re-solves the witness from its own floats. With it, the view is Evan Daniel's per-count
regularization JSON (`packing.S` and `packing.sq`, rows `x y degrees` at the view's
side, in the container orientation `orientation_g`, mapped back here into the witness's
frame).

**Why.** Evan Daniel's regularizer (`vendor/evand-regularize/search/regularize/reg.py`)
writes its view as an 80-digit point at the side `S*` of a KKT point and certifies a
copy dilated by `1 + 10^-20` at a rational side `S' > S*`. This project draws a
regularized frame only at the side of the witness it regularizes: the regularization
policy (`docs/project/policies/regularization-policy.md`) and the assessment behind it
(`docs/project/research/research-2026-10-11-evand-regularization-assessment.md`, 3.2 and
slice 3 of section 5). Where every rotation of the view is one the witness holds
exactly, or is exactly axis-aligned, the rotations can be fixed exactly and what is left
is linear in the centres, so the view's contact structure can be imposed over Q at the
witness's own side.

**Method.** All arithmetic is `fractions.Fraction`; no floating-point value takes part
in any decision. Approximate inputs are read as exact rationals first (a decimal string
as written, a binary64 value as the shortest decimal `repr` prints).

1. `snap_rotations` maps each view rotation to a target: exactly axis-aligned, or one of
   the source witness's exact rotations, each up to a quarter turn. The view rotation
   `v` and a target representative `r` (the quarter turn of the target nearest `v`) are
   compared by the exact sine of the angle between them, `|v_c r_s - v_s r_c|`; a target
   matches when that is at most `tol`. The nearest target wins, ties to the axis and
   then to the earliest source square, and the snapped rotation is `r`. A rotation
   matching nothing is refused, by square; one within `tol` of exactly 45 degrees is
   named as such, because 45 degrees has no rational pose and only a rotation the
   witness holds can stand in for it.
2. `resolve_at_side` writes every wall, and every pair whose approximate centres are
   closer than 3/2 (two unit squares can first touch at `sqrt 2`), as a constraint
   `a . z >= b` on the `2n` centre unknowns `z`, at exactly `side`. A wall is `x - e >= 0`
   or `side - x - e >= 0`, and the same in `y`, with `e = (|c| + |s|) / 2`. A pair's
   separating axis is chosen at the approximate point: of the four unit edge normals of
   the two squares, each oriented from the first centre toward the second, the one of
   largest gap `n . (C_j - C_i) - h_i(n) - h_j(n)`, where `h(n) = (|n . u| + |n . v|) / 2`
   is a square's half-width along `n`; ties go to the first square's normals, in edge
   order. With the rotations fixed this is linear and exact, and every point meeting it
   has the pair's interiors disjoint.
3. A constraint whose approximate gap is below `tight_tol` is *tight* and becomes the
   equality `a . z = b`; one whose approximate gap is `-tight_tol` or less means the view
   is not even approximately a packing at `side`, and is refused. The tight rows are
   reduced in a fixed order (near walls, `x = e` and `y = e`; then pairs, smallest
   approximate gap first; then far walls) by sparse Gaussian elimination over Q that
   carries, for every reduced row, the exact combination of original rows it is, and
   pivots on the unknown of largest coefficient. A reduced row that is nonzero but nearly
   a combination of earlier rows (two nearly parallel contacts on one square, or a loop
   closed at rotations that differ in the 36th digit) would throw the solution far from
   the view; its first-order shift, `|sum_k l_k g_k| / max|coefficient|` with `g_k` the
   approximate gaps, is computed exactly, and a row shifting more than `move_limit`
   (1e-7) is not imposed: refused (`ill-conditioned-tight-set`) under `"refuse"`, left as
   an inequality under `"relax"`. A row that reduces to `0 = r`, `r != 0`, is a
   conflict, and the combination is its
   certificate: `sum_k l_k a_k = 0` while `sum_k l_k b_k = r`, so once the other rows
   hold with equality the conflicting row's gap is forced to `-r`. The certificate is
   *Farkas* when every `l_k` has the sign of `r`: then no point meets even the
   inequalities `a_k . z >= b_k`, at these rotations, this side and these axes.
   With `on_conflict="refuse"`, the default, the first conflict is refused with its
   certificate. With `"relax"`, a conflict whose forced gap is positive is left as a
   slack inequality; one whose forced gap is negative is refused when Farkas, and
   otherwise the latest row of the certificate with a multiplier of sign opposite to
   `r` is left slack in its place (its forced gap, `-r / l_m`, is then positive) and the
   elimination restarts, at most once per tight row. The order decides where slack
   lands: on the far walls first, "gravity toward the lower-left corner", the
   convention the source regularizer draws with too.
4. Unknowns no row pivots on are free. Each is fixed at its approximate value rounded to
   the nearest multiple of `10^-d`, ties to even, for `d` on `FREE_DIGITS` (12, then 24)
   and finally at the approximate value itself; the pivots are back-substituted, and
   the first rung whose pose passes the exact check below is kept.
5. The pose is checked exactly three times. First here, completely: every corner in the
   closed `[0, side]^2`, and every pair whose centres are closer than `sqrt 2` (no other
   pair can overlap) separated, a zero gap allowed, along one of its four edge normals.
   Then by the project's two maintained routes, whose verdicts are the decision:
   `sqpack.witness.exact_verify` on the pose as a rational center-basis Witness/v2
   mapping, and `devtools.check_rational_witness_independent.check_squares` on corners
   computed here, which shares no geometry with `sqpack`. Both accept a zero sign (a
   touching pair, a corner on a wall), so a pose with its contacts closed is decidable
   here; the source's strict checkers would refuse it.

**The contract.** A `Resolved` result proves exactly this: the `n` unit squares with
the returned rational centres and rotations `(c, s)`, `c^2 + s^2 = 1` exactly, form a
packing of the square `[0, side]^2` of side exactly `side`, in the sense of
`sqpack.verify.verify_packing` (every corner in the closed square; every pair with
disjoint interiors, touching allowed), decided over Q by both maintained routes. Hence
`s(n) <= side`. Through `resolve_view`, in addition, every rotation is a rotation the
source witness holds exactly, up to a quarter turn, or is exactly axis-aligned, and
`side` is the source witness's exact side as defined below, unless the caller passes
another. The pose's certificate says which: `side_relation` is `same` exactly when
`side` equals that frame side, and `solved` for any other side (the regularization
policy's two side relations); `resolve_at_side` alone has no source and writes neither.
It does not prove that the result is the source's packing or the view's (no
combinatorial identity is claimed; `arrangement_gap` measures that elsewhere); that
every tight constraint of the view is closed (under `"relax"`, `relaxed` lists those
that are not, each with its exact gap in the pose); that the closed contacts are all of
the pose's contacts; optimality, local optimality or rigidity; or anything about the
view's `S*` or its dilated `S'`. Refusal kinds: `malformed-input` (a side, centre,
tolerance or option that is not a finite number of the declared kind, an exponent past
`EXPONENT_LIMIT`, or an empty rounding ladder with unknowns free), `count-mismatch`,
`not-a-rotation`, `unmatched-rotation`, `unsupported-scalar-kind`,
`promotion-unsupported`, `approximate-overlap`, `ill-conditioned-tight-set`,
`inconsistent-tight-set`, `tight-set-forces-overlap`, `verification-failed` (this
module's own complete check refused the pose at every rung of the ladder),
`routes-refused` (a maintained route refused a pose that check passed: a disagreement
between checkers, so a bug in one of them) and `literal-too-large` (an exact coordinate
past CPython's 4300-digit integer text limit, which no witness file could carry or a
reader re-read).

**What "same side" means.** For a rational witness, the witness's own exact side, and
its own rotations. For a decimal witness, the side of its 36-digit rational promotion at
centre dilation 1, the frame `devtools.regularize_axis_components` regularizes in
(`sqpack.witness`'s first `promote_rational` candidate: centres and `t = tan(theta/2)`
rounded to 36 significant digits, translated so the least corner coordinate on each axis
is 0, the side the larger extent), and the promotion's `(c, s)` as the rotations. That
side differs from the printed decimal by the promotion's rounding, and by any
difference, either way, between the printed pose's own extent and its printed side; it
is reported as `side_minus_printed`. Of the 106 decimal known-best witnesses on
2026-10-11, 53 differ: 24 by under 1e-30, the rounding alone, and 29 by more, the
printed pose's own excess or shortfall, as n = 69 by +1.085e-15 and n = 211 by -2.1e-14.
An exact packing at a decimal witness's side certifies a side the register may not:
where the register's verified bound for `n` is above it (for example still the grid
ceiling), a result here is a new verified upper bound, a register result and an owner
decision. `resolve_view` returns that as a flag from the `verified_bound`
its caller passes, and decides nothing.

**Where same side is impossible in principle.** A view rotation the witness does not
hold (a group merged to a new angle; exactly 45 degrees where the witness has no
rotation within `tol` of it) has no exact pose to fix. A side below the exact optimum
admits no packing at all: a decimal witness whose printed side truncates an irrational
optimum, as n = 10's `3 + sqrt(2)/2` printed to 28 places is, is refused with a Farkas
certificate. A contact loop closed at rational approximations of the optimum's
irrational rotations is generically overdetermined: `"relax"` leaves the loop open by
the rounding (1e-36 at a 36-digit promotion) where the certificate allows it, and a
Farkas certificate means the chosen axes cannot all hold. An algebraic-number-field
witness has no rational frame (`unsupported-scalar-kind`), as in the axis tool. One more
failure is not impossibility but conditioning: a tight row left open because closing it
would move the view too far keeps whatever gap the rest give it, which can be negative
by the rotations' rounding (1e-16 to 1e-36 at a 36-digit promotion); the exact check then
refuses the pose, and the refusal lists the failures and the largest moves.
"""

from __future__ import annotations

import argparse
import gzip
import heapq
import json
import math
import numbers
import re
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any, Literal

from devtools import check_rational_witness_independent as independent
from devtools.regularize_axis_components import RATIONAL_DIGITS, literal
from sqpack.witness import (
    WitnessError,
    # The decimal frame is the axis tool's, built by the same private helper it uses:
    # `promote_rational`'s first candidate, dilation 1, before any verdict on it.
    _promoted_candidate,  # pyright: ignore[reportPrivateUsage]
    # The rule that promotion turns a decimal angle into a rational rotation with.
    _rational_basis,  # pyright: ignore[reportPrivateUsage]
    exact_verify,
    load_witness,
    materialize_exact_witness,
)

ROOT = Path(__file__).resolve().parent.parent
WITNESS_SCHEMA = ROOT / "witnesses" / "witness.schema.yaml"

ALGORITHM = "regularize_same_side/1"
DEFAULT_SNAP_TOLERANCE = Fraction(1, 10**9)
"""Largest `|sin|` of the angle, modulo a quarter turn, between a view rotation and the
exact rotation it snaps to: 1e-9, which is 1e-9 radians to within one part in 1e18."""
DEFAULT_TIGHT_TOLERANCE = Fraction(1, 10**9)
"""A constraint whose approximate gap is below this is tight, and is closed exactly."""
FREE_DIGITS: tuple[int | None, ...] = (12, 24, None)
"""Decimal places free unknowns are rounded to, coarsest first; `None` is the
approximate value itself. Not coarser than 12: a rounding of 1e-6 moves squares by up to
5e-7, inside the house shading rule's 2e-6 contact gap, so it could change what the
renderer shades; 1e-12 is far below both rules' gaps."""
MOVE_LIMIT = Fraction(1, 10**7)
"""Largest first-order shift one tight row may impose on the approximate point: a hundred
times the tight tolerance, and twenty times below the house shading rule's 2e-6."""
REACH_SQUARED = Fraction(9, 4)
"""Pairs whose approximate centres are within 3/2 are constrained; two unit squares can
first touch at `sqrt 2`, and 3/2 leaves 0.08 of margin for the approximate point."""
OVERLAP_REACH_SQUARED = Fraction(2)
"""Two unit squares whose centres are `sqrt 2` or more apart have disjoint interiors:
each lies in the closed disk of radius `sqrt(2)/2` about its centre."""
CELL = 2
"""Bucket width for pair enumeration; at least both reaches, so neighbours are adjacent."""
HALF = Fraction(1, 2)
EXPONENT_LIMIT = 1000
"""Largest decimal exponent, either way, an input may carry, and the most places a free
unknown may be rounded to. `Fraction` builds the whole `10^e` integer before anything
else (a billion digits for `1e999999999`); nothing in a packing of unit squares is near
`10^1000`, and a literal of that size still prints under CPython's 4300-digit limit."""
_EXPONENT = re.compile(r"[eE]\s*[-+]?([0-9_]+)\s*\Z")

type Basis = tuple[Fraction, Fraction]
"""An exact rotation `(cos theta, sin theta)`, with `c^2 + s^2 = 1`."""
type Point = tuple[Fraction, Fraction]
type Approximate = Fraction | int | str | float
type ViewSquare = tuple[Approximate, Approximate, Basis]
"""One square of a view: approximate centre `x`, `y`, and its exact rational rotation."""
ConflictPolicy = Literal["refuse", "relax"]

NEAR_WALLS = ("left", "bottom")


# --------------------------------------------------------------------------------------
# Results and refusals
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Refusal:
    """A typed refusal: what could not be done exactly, and the evidence for it."""

    kind: str
    detail: str
    items: tuple[dict[str, Any], ...] = ()

    def summary(self) -> dict[str, Any]:
        return {
            "status": "refused",
            "kind": self.kind,
            "detail": self.detail,
            "items": list(self.items),
        }


@dataclass(frozen=True)
class Snap:
    """Where one view rotation went: an exact target, the quarter turn, the deviation."""

    target: int | None
    """Index of the first source square holding the target, or `None` for the axis."""
    quarter_turns: int
    """Quarter turns applied to the target's canonical representative."""
    deviation: Fraction
    """Exact `|sin|` of the angle between the view rotation and the snapped one."""


@dataclass(frozen=True)
class Snapped:
    rotations: tuple[Basis, ...]
    snaps: tuple[Snap, ...]

    @property
    def moved(self) -> int:
        """View rotations the snap changed at all."""
        return sum(snap.deviation != 0 for snap in self.snaps)

    def summary(self) -> dict[str, Any]:
        deviations = [snap.deviation for snap in self.snaps]
        return {
            "squares": len(self.snaps),
            "to_axis": sum(snap.target is None for snap in self.snaps),
            "to_source_rotation": sum(snap.target is not None for snap in self.snaps),
            "moved": self.moved,
            "largest_deviation_sine": _e(max(deviations, default=Fraction(0))),
        }


@dataclass(frozen=True, slots=True)
class Constraint:
    """`sum(a_k z_k) >= rhs` on the centre unknowns, `z_2i = x_i` and `z_2i+1 = y_i`."""

    kind: str
    """`wall` or `pair`."""
    squares: tuple[int, ...]
    detail: str
    """The wall's name, or which of the owner's two edge normals separates the pair."""
    coefficients: tuple[tuple[int, Fraction], ...]
    rhs: Fraction
    approx_gap: Fraction
    owner: int | None = None
    """For a pair, the square whose edge normal separates it."""

    def gap(self, values: Sequence[Fraction]) -> Fraction:
        return sum((a * values[k] for k, a in self.coefficients), Fraction(0)) - self.rhs

    @property
    def group(self) -> int:
        """Elimination order: near walls, pairs, far walls."""
        if self.kind == "pair":
            return 1
        return 0 if self.detail in NEAR_WALLS else 2

    def label(self, ids: Sequence[Any] | None = None) -> str:
        def name(index: int) -> str:
            return str(ids[index]) if ids is not None else str(index)

        if self.kind == "wall" or self.owner is None:
            return f"square {name(self.squares[0])} on the {self.detail} wall"
        first, second = (name(index) for index in self.squares)
        return f"squares {first} and {second} along square {name(self.owner)}'s {self.detail}"


@dataclass(frozen=True)
class Resolved:
    """An exact pose at exactly `side`, decided by both maintained routes."""

    side: Fraction
    centres: tuple[Point, ...]
    rotations: tuple[Basis, ...]
    witness: dict[str, Any]
    """The pose as a rational center-basis Witness/v2 mapping: what `exact_verify` decided."""
    constraints: int
    """Walls and in-reach pairs written down at the approximate point."""
    tight_walls: int
    tight_pairs: int
    closed: int
    """Tight constraints imposed as equalities (pivots and consistent redundancies)."""
    redundant: int
    relaxed: tuple[dict[str, Any], ...]
    """Tight constraints left as inequalities, each with its exact gap in the pose."""
    restarts: int
    """Eliminations restarted to swap which constraint of a conflict is left slack."""
    rank: int
    unknowns: int
    free_unknowns: int
    free_rounding: str
    max_move: Fraction
    """Largest `max(|x - x~|, |y - y~|)` over squares, against the approximate centres."""
    verification: dict[str, Any]
    seconds: dict[str, float] = field(default_factory=dict[str, float])

    @property
    def tight(self) -> int:
        return self.tight_walls + self.tight_pairs

    def summary(self) -> dict[str, Any]:
        return {
            "status": "resolved",
            "algorithm": ALGORITHM,
            "side": literal(self.side),
            "side_decimal": _g(self.side),
            "n": len(self.centres),
            "constraints": self.constraints,
            "tight": self.tight,
            "tight_walls": self.tight_walls,
            "tight_pairs": self.tight_pairs,
            "closed": self.closed,
            "redundant": self.redundant,
            "relaxed": list(self.relaxed),
            "relaxed_walls": sum(item["kind"] == "wall" for item in self.relaxed),
            "relaxed_pairs": sum(item["kind"] == "pair" for item in self.relaxed),
            "restarts": self.restarts,
            "rank": self.rank,
            "unknowns": self.unknowns,
            "free_unknowns": self.free_unknowns,
            "free_rounding": self.free_rounding,
            "max_move": _e(self.max_move),
            "verification": self.verification,
            "seconds": self.seconds,
        }


@dataclass(frozen=True)
class ViewResolution:
    """A view re-solved at its source witness's side or the caller's, and which it was."""

    resolved: Resolved
    snapped: Snapped
    side_basis: dict[str, Any]
    register: dict[str, Any]

    @property
    def side_relation(self) -> str:
        """`same` when the side is exactly the source frame's, else `solved` (policy, 2)."""
        return self.resolved.witness["certificate"]["side_relation"]

    def summary(self) -> dict[str, Any]:
        return {
            **self.resolved.summary(),
            "status": "same-side" if self.side_relation == "same" else "solved-side",
            "side_relation": self.side_relation,
            "rotations": self.snapped.summary(),
            "side_basis": self.side_basis,
            "register": self.register,
        }


# --------------------------------------------------------------------------------------
# Exact rotations
# --------------------------------------------------------------------------------------


class MalformedValueError(ValueError):
    """An approximate input that is not a finite number this module reads exactly."""


def exact_value(value: Approximate) -> Fraction:
    """An approximate input as an exact rational: as written, or as `repr` prints it.

    Raises `MalformedValueError` for a boolean, a non-finite float, text `Fraction` does not
    read (`nan`, `inf`, `1/0`), a decimal exponent past `EXPONENT_LIMIT`, or any other
    type; the public entry points turn that into a `malformed-input` refusal.
    """
    if isinstance(value, bool):
        raise MalformedValueError("a boolean is not a number here")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise MalformedValueError(f"{value!r} is not finite")
        return Fraction(repr(value))
    if isinstance(value, numbers.Rational):
        return Fraction(value)
    if not isinstance(value, str):
        raise MalformedValueError(f"a {type(value).__name__} is not a number this tool reads")
    exponent = _EXPONENT.search(value)
    if exponent is not None:
        digits = exponent.group(1).replace("_", "").lstrip("0") or "0"
        if len(digits) > len(str(EXPONENT_LIMIT)) or int(digits) > EXPONENT_LIMIT:
            raise MalformedValueError(
                f"{value[:40]!r}: a decimal exponent past 10^{EXPONENT_LIMIT} either way"
            )
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise MalformedValueError(
            f"{value[:40]!r} is not a finite rational: {error}"
        ) from error


def _read(
    value: Approximate, what: str, *, sign: Literal["any", "nonnegative", "positive"] = "any"
) -> Fraction | Refusal:
    """`exact_value`, or a `malformed-input` refusal naming `what`, as is its sign."""
    try:
        exact = exact_value(value)
    except MalformedValueError as error:
        return Refusal("malformed-input", f"{what}: {error}")
    if (sign == "nonnegative" and exact < 0) or (sign == "positive" and exact <= 0):
        return Refusal("malformed-input", f"{what} must be {sign}, not {_e(exact)}")
    return exact


def _exact_basis(basis: object) -> bool:
    """Whether `basis` is a pair of exact rationals (`int` or `Fraction`, not `bool`)."""
    return (
        isinstance(basis, tuple | list)
        and len(basis) == 2
        and all(
            isinstance(value, int | Fraction) and not isinstance(value, bool) for value in basis
        )
    )


def basis_from_half_tangent(t: Approximate) -> Basis:
    """`((1 - t^2) / (1 + t^2), 2t / (1 + t^2))`, exactly, from `t = tan(theta / 2)`."""
    value = exact_value(t)
    denominator = 1 + value * value
    return (1 - value * value) / denominator, 2 * value / denominator


def basis_from_angle(
    text: str, unit: Literal["degrees", "radians"] = "degrees", digits: int = RATIONAL_DIGITS
) -> Basis:
    """The rational rotation promotion builds from a decimal angle: `t` to `digits` places."""
    return _rational_basis(text, unit, digits)


def is_rotation(basis: Basis) -> bool:
    c, s = basis
    return c * c + s * s == 1


def quarter_turn(basis: Basis, turns: int) -> Basis:
    c, s = basis
    for _ in range(turns % 4):
        c, s = -s, c
    return c, s


def canonical(basis: Basis) -> tuple[Basis, int]:
    """The quarter turn of `basis` with `c > 0, s >= 0`, and the turns that reach it."""
    for turns in range(4):
        c, s = quarter_turn(basis, turns)
        if c > 0 and s >= 0:
            return (c, s), turns
    raise ValueError(f"{basis} is not a rotation")


def degrees(basis: Basis) -> float:
    """For reports only: the rotation in degrees, folded into `[0, 90)`."""
    (c, s), _ = canonical(basis)
    return math.degrees(math.atan2(float(s), float(c)))


def _nearest_turn(view: Basis, target: Basis) -> tuple[Fraction, Fraction, int]:
    """`(cos, |sin|, turns)` for the quarter turn of `target` nearest `view`."""
    best: tuple[Fraction, Fraction, int] | None = None
    for turns in range(4):
        c, s = quarter_turn(target, turns)
        cosine = view[0] * c + view[1] * s
        if best is None or cosine > best[0]:
            best = (cosine, abs(view[0] * s - view[1] * c), turns)
    if best is None:
        raise AssertionError("four quarter turns always yield a candidate")
    return best


def near_45(basis: Basis, tol: Fraction) -> bool:
    """Whether `basis` is within `tol` (as `|sin|`) of exactly 45 degrees, modulo 90."""
    (c, s), _ = canonical(basis)
    return (s - c) * (s - c) <= 2 * tol * tol


def snap_rotations(
    view_rotations: Sequence[Basis],
    source_rotations: Sequence[Basis],
    tol: Approximate = DEFAULT_SNAP_TOLERANCE,
) -> Snapped | Refusal:
    """Map each view rotation to an exact rotation of the source, or to the axis.

    Targets are exactly axis-aligned `(1, 0)` and every distinct source rotation, each up
    to a quarter turn. A view rotation matches a target when the exact `|sin|` of the
    angle to the target's nearest quarter turn is at most `tol` and its cosine is
    positive; the nearest match wins, ties to the axis and then to the earliest source
    square. The snapped rotation is that quarter turn of the target, so it stays next to
    the view's own representative. Refused, naming every square that matches nothing.
    """
    tolerance = exact_value(tol)
    for where, given in (("view", view_rotations), ("source", source_rotations)):
        bad = [index for index, basis in enumerate(given) if not is_rotation(basis)]
        if bad:
            return Refusal(
                "not-a-rotation",
                f"{len(bad)} {where} rotation(s) do not satisfy c^2 + s^2 = 1 exactly",
                tuple({"where": where, "square": index} for index in bad[:20]),
            )
    targets: list[tuple[Basis, int | None]] = [((Fraction(1), Fraction(0)), None)]
    seen = {targets[0][0]}
    for index, basis in enumerate(source_rotations):
        representative, _ = canonical(basis)
        if representative not in seen:
            seen.add(representative)
            targets.append((representative, index))
    rotations: list[Basis] = []
    snaps: list[Snap] = []
    unmatched: list[dict[str, Any]] = []
    for square, view in enumerate(view_rotations):
        best: tuple[Fraction, int, Basis, int | None] | None = None
        for representative, holder in targets:
            cosine, sine, turns = _nearest_turn(view, representative)
            if cosine <= 0 or sine > tolerance:
                continue
            if best is None or sine < best[0]:
                best = (sine, turns, representative, holder)
        if best is None:
            unmatched.append(
                {
                    "square": square,
                    "degrees": round(degrees(view), 12),
                    "exactly_45": near_45(view, tolerance),
                }
            )
            continue
        sine, turns, representative, holder = best
        rotations.append(quarter_turn(representative, turns))
        snaps.append(Snap(holder, turns, sine))
    if unmatched:
        forty_five = sum(item["exactly_45"] for item in unmatched)
        note = (
            f"; {forty_five} of them within the tolerance of exactly 45 degrees, which has "
            "no rational pose, and the source holds no rotation there to stand in for it"
            if forty_five
            else ""
        )
        return Refusal(
            "unmatched-rotation",
            f"{len(unmatched)} view rotation(s) are within {float(tolerance):.1e} of no "
            f"rotation the source holds exactly and of no axis{note}",
            tuple(unmatched),
        )
    return Snapped(tuple(rotations), tuple(snaps))


# --------------------------------------------------------------------------------------
# Constraints at the approximate point
# --------------------------------------------------------------------------------------


def half_width(basis: Basis, normal: Point) -> Fraction:
    """Half the extent of a unit square with rotation `basis` along the unit `normal`."""
    c, s = basis
    return (abs(normal[0] * c + normal[1] * s) + abs(-normal[0] * s + normal[1] * c)) / 2


def edge_normals(basis: Basis) -> tuple[Point, Point]:
    c, s = basis
    return (c, s), (-s, c)


def _cell(point: Point) -> tuple[int, int]:
    return math.floor(point[0] / CELL), math.floor(point[1] / CELL)


def close_pairs(centres: Sequence[Point], reach_squared: Fraction) -> list[tuple[int, int]]:
    """Every pair `i < j` with squared centre distance below `reach_squared`, exactly."""
    grid: dict[tuple[int, int], list[int]] = {}
    for index, point in enumerate(centres):
        grid.setdefault(_cell(point), []).append(index)
    pairs: list[tuple[int, int]] = []
    for (gx, gy), members in grid.items():
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for j in grid.get((gx + dx, gy + dy), ()):
                    for i in members:
                        if i >= j:
                            continue
                        ddx = centres[j][0] - centres[i][0]
                        ddy = centres[j][1] - centres[i][1]
                        if ddx * ddx + ddy * ddy < reach_squared:
                            pairs.append((i, j))
    return sorted(pairs)


def wall_constraints(
    index: int, basis: Basis, centre: Point, side: Fraction
) -> list[Constraint]:
    extent = (abs(basis[0]) + abs(basis[1])) / 2
    x, y = 2 * index, 2 * index + 1
    rows = (
        ("left", x, Fraction(1), extent),
        ("right", x, Fraction(-1), extent - side),
        ("bottom", y, Fraction(1), extent),
        ("top", y, Fraction(-1), extent - side),
    )
    return [
        Constraint(
            "wall",
            (index,),
            name,
            ((unknown, sign),),
            rhs,
            sign * centre[unknown - 2 * index] - rhs,
        )
        for name, unknown, sign, rhs in rows
    ]


def pair_constraint(
    i: int, j: int, rotations: Sequence[Basis], centres: Sequence[Point]
) -> Constraint:
    """The pair's row along the edge normal of largest gap at the approximate point."""
    dx, dy = centres[j][0] - centres[i][0], centres[j][1] - centres[i][1]
    best: tuple[Fraction, Point, Fraction, int, int] | None = None
    for owner in (i, j):
        for edge, normal in enumerate(edge_normals(rotations[owner])):
            nx, ny = normal
            if nx * dx + ny * dy < 0:
                nx, ny = -nx, -ny
            reach = half_width(rotations[i], (nx, ny)) + half_width(rotations[j], (nx, ny))
            gap = nx * dx + ny * dy - reach
            if best is None or gap > best[0]:
                best = (gap, (nx, ny), reach, owner, edge)
    if best is None:
        raise AssertionError("four edge normals always yield a candidate")
    gap, (nx, ny), reach, owner, edge = best
    terms = ((2 * i, -nx), (2 * i + 1, -ny), (2 * j, nx), (2 * j + 1, ny))
    coefficients = tuple((unknown, a) for unknown, a in terms if a != 0)
    return Constraint("pair", (i, j), f"edge normal {edge}", coefficients, reach, gap, owner)


# --------------------------------------------------------------------------------------
# Exact sparse elimination with conflict certificates
# --------------------------------------------------------------------------------------


@dataclass
class _Row:
    coefficients: dict[int, Fraction]
    rhs: Fraction
    combination: dict[int, Fraction]
    """Multipliers of the original constraints this row is the combination of."""


@dataclass
class _Echelon:
    """Rows reduced against earlier pivots only, so back-substitution runs in reverse."""

    rows: dict[int, _Row] = field(default_factory=dict[int, _Row])
    created: dict[int, int] = field(default_factory=dict[int, int])
    order: list[int] = field(default_factory=list[int])

    def reduce(self, tag: int, constraint: Constraint) -> _Row:
        row = _Row(dict(constraint.coefficients), constraint.rhs, {tag: Fraction(1)})
        heap = [(self.created[v], v) for v in row.coefficients if v in self.created]
        heapq.heapify(heap)
        while heap:
            _, pivot = heapq.heappop(heap)
            a = row.coefficients.get(pivot)
            if a is None:
                continue
            other = self.rows[pivot]
            factor = a / other.coefficients[pivot]
            for unknown, b in other.coefficients.items():
                value = row.coefficients.get(unknown, Fraction(0)) - factor * b
                if value == 0:
                    row.coefficients.pop(unknown, None)
                    continue
                if unknown not in row.coefficients and unknown in self.created:
                    heapq.heappush(heap, (self.created[unknown], unknown))
                row.coefficients[unknown] = value
            row.rhs -= factor * other.rhs
            for key, multiplier in other.combination.items():
                value = row.combination.get(key, Fraction(0)) - factor * multiplier
                if value == 0:
                    row.combination.pop(key, None)
                else:
                    row.combination[key] = value
        return row

    def add(self, row: _Row) -> None:
        """Pivot on the unknown of largest coefficient, ties to the lowest index: it then
        absorbs the row's residual at the cost `predicted_shift` measured."""
        pivot = max(
            row.coefficients, key=lambda unknown: (abs(row.coefficients[unknown]), -unknown)
        )
        self.created[pivot] = len(self.order)
        self.order.append(pivot)
        self.rows[pivot] = row

    def solve(self, values: list[Fraction]) -> None:
        """Back-substitute every pivot, latest first; free unknowns are already set."""
        for pivot in reversed(self.order):
            row = self.rows[pivot]
            rest = sum(
                (a * values[k] for k, a in row.coefficients.items() if k != pivot),
                Fraction(0),
            )
            values[pivot] = (row.rhs - rest) / row.coefficients[pivot]


def _certificate(
    row: _Row, constraints: Sequence[Constraint], ids: Sequence[Any] | None
) -> tuple[dict[str, Any], ...]:
    """The conflict's combination, with every multiplier exact."""
    return tuple(
        {
            "constraint": constraints[tag].label(ids),
            "multiplier": evidence_literal(multiplier),
            "approx_gap": _e(constraints[tag].approx_gap),
        }
        for tag, multiplier in sorted(row.combination.items())
    )


def _farkas(row: _Row) -> bool:
    """Whether the combination proves the chosen inequalities themselves infeasible.

    For `g_k(z) = a_k . z - b_k >= 0` and `sum l_k a_k = 0`, `sum l_k g_k = -r` for every
    `z`; with every `l_k >= 0` and `r > 0` (or all `<= 0` and `r < 0`) no `z` meets them
    all, at these rotations, this side and these separating axes.
    """
    multipliers = list(row.combination.values())
    # The second clause cannot fire on a row `_Echelon.reduce` returns: the row starts as
    # its own constraint with multiplier +1, and every earlier row it subtracts is a
    # combination of earlier constraints only, so that +1 survives and not every
    # multiplier is `<= 0`. It is kept so the function states the lemma for any
    # combination, including one scaled by -1, rather than relying on how it was built.
    return (all(m >= 0 for m in multipliers) and row.rhs > 0) or (
        all(m <= 0 for m in multipliers) and row.rhs < 0
    )


# --------------------------------------------------------------------------------------
# Exact checks of a pose
# --------------------------------------------------------------------------------------


def corners(centre: Point, basis: Basis) -> list[Point]:
    """The four corners, counter-clockwise: the centre plus the rotated half-diagonals."""
    c, s = basis
    x, y = centre
    return [
        (x + c * a - s * b, y + s * a + c * b)
        for a, b in ((HALF, HALF), (-HALF, HALF), (-HALF, -HALF), (HALF, -HALF))
    ]


def evidence_literal(value: Fraction) -> str:
    """An exact literal for a report, or its decimal where Python will not print it.

    CPython refuses to convert an integer of more than `sys.get_int_max_str_digits()`
    digits (4300 by default) to text; a multiplier carried through a long elimination
    over 36-digit rotations can exceed that. The decision was made on the exact value.
    """
    try:
        return literal(value)
    except ValueError:
        return f"{_e(value, 7)} (exact literal beyond the interpreter's digit limit)"


def _scientific(value: Fraction, figures: int) -> str:
    """`value` to `figures` significant figures as `d.ddde+XX`, by integer arithmetic.

    For amounts binary64 cannot hold: past about 1.8e308 `float` raises, and below about
    5e-324 it reads zero. Rounds half to even, as `round` on a `Fraction` does.
    """
    if value == 0:
        return f"{0:.{figures - 1}e}"
    sign = "-" if value < 0 else ""
    magnitude = abs(value)
    # floor(log10 |value|), from the bit lengths to within one, then corrected exactly.
    bits = magnitude.numerator.bit_length() - magnitude.denominator.bit_length()
    exponent = math.floor(bits * math.log10(2))
    while magnitude >= Fraction(10) ** (exponent + 1):
        exponent += 1
    while magnitude < Fraction(10) ** exponent:
        exponent -= 1
    mantissa = round(magnitude * Fraction(10) ** (figures - 1 - exponent))
    if mantissa == 10**figures:
        mantissa, exponent = mantissa // 10, exponent + 1
    digits = str(mantissa)
    fraction = f".{digits[1:]}" if figures > 1 else ""
    return f"{sign}{digits[0]}{fraction}e{exponent:+03d}"


def _binary64(value: Fraction) -> float | None:
    """`float(value)`, or `None` where binary64 overflows or flushes a nonzero to zero."""
    try:
        approximate = float(value)
    except OverflowError:
        return None
    return None if approximate == 0 and value != 0 else approximate


def _e(value: Fraction, figures: int = 4) -> str:
    """An exact amount as a short decimal, for messages; the decision was made on `value`.

    `figures` significant figures in `e` notation, as binary64 formats it, and exactly
    where binary64 cannot hold the amount (a side of `1e400`, a gap of `1e-400`).
    """
    approximate = _binary64(value)
    if approximate is None:
        return _scientific(value, figures)
    return f"{approximate:.{figures - 1}e}"


def _g(value: Fraction, figures: int = 17) -> str:
    """`format(float(value), ".17g")` for reports, exact where binary64 overflows."""
    approximate = _binary64(value)
    if approximate is not None:
        return f"{approximate:.{figures}g}"
    mantissa, _, exponent = _scientific(value, figures).partition("e")
    if "." in mantissa:
        mantissa = mantissa.rstrip("0").rstrip(".")
    return f"{mantissa}e{exponent}"


def pose_failures(
    side: Fraction,
    rotations: Sequence[Basis],
    centres: Sequence[Point],
    *,
    ids: Sequence[Any] | None = None,
    limit: int = 10,
) -> list[str]:
    """Every way the pose fails to be a packing at `side`, exactly; empty when it is one.

    Complete: each corner in the closed `[0, side]^2`, and each pair closer than `sqrt 2`
    (no other can overlap) separated, zero gap allowed, along one of its edge normals.
    Squares are named by `ids`, else by 0-based position; amounts are printed to four
    figures.
    """

    def name(index: int) -> str:
        return str(ids[index]) if ids is not None else str(index)

    failures: list[str] = []
    for index, (basis, centre) in enumerate(zip(rotations, centres, strict=True)):
        extent = (abs(basis[0]) + abs(basis[1])) / 2
        for axis, axis_name in ((0, "x"), (1, "y")):
            low, high = centre[axis] - extent, side - centre[axis] - extent
            if low < 0:
                failures.append(
                    f"square {name(index)} crosses the {axis_name} = 0 wall by {_e(-low)}"
                )
            if high < 0:
                failures.append(
                    f"square {name(index)} crosses the {axis_name} = side wall by {_e(-high)}"
                )
    for i, j in close_pairs(centres, OVERLAP_REACH_SQUARED):
        dx, dy = centres[j][0] - centres[i][0], centres[j][1] - centres[i][1]
        best = max(
            abs(n[0] * dx + n[1] * dy)
            - half_width(rotations[i], n)
            - half_width(rotations[j], n)
            for owner in (i, j)
            for n in edge_normals(rotations[owner])
        )
        if best < 0:
            failures.append(f"squares {name(i)} and {name(j)} overlap by {_e(-best)}")
    return failures[:limit]


def pose_witness(
    side: Fraction,
    rotations: Sequence[Basis],
    centres: Sequence[Point],
    *,
    ids: Sequence[Any] | None = None,
    witness_id: str = "W-same-side-view",
) -> dict[str, Any]:
    """The pose as a rational center-basis Witness/v2 mapping, lower-left origin."""
    names = list(ids) if ids is not None else list(range(1, len(centres) + 1))
    return {
        "id": witness_id,
        "n": len(centres),
        "side": literal(side),
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
                "id": name,
                "center": [literal(centre[0]), literal(centre[1])],
                "basis": [literal(basis[0]), literal(basis[1])],
            }
            for name, centre, basis in zip(names, centres, rotations, strict=True)
        ],
        "claim": {
            "coordinate_provenance": "reported",
            "method": "exact-algebraic",
            "limitations": (
                "A regularized view re-solved over Q at a fixed exact side, the source "
                "witness's where certificate.side_relation is same; the conversion "
                "decides nothing, exact_verify and the independent checker do."
            ),
        },
    }


def _short(text: str) -> str:
    """An exact clearance as the verifier printed it, shortened: `0` exactly, else 4 figures."""
    value = Fraction(text)
    return "0" if value == 0 else _e(value)


def verify_pose(witness: Mapping[str, Any]) -> dict[str, Any]:
    """Both maintained exact decisions of a rational center-basis pose."""
    started = time.perf_counter()
    result, _report = exact_verify(witness)
    sqpack_seconds = time.perf_counter() - started
    side = Fraction(witness["side"])
    squares = [
        corners(
            (Fraction(square["center"][0]), Fraction(square["center"][1])),
            (Fraction(square["basis"][0]), Fraction(square["basis"][1])),
        )
        for square in witness["squares"]
    ]
    started = time.perf_counter()
    second = independent.check_squares(squares, side)
    independent_seconds = time.perf_counter() - started
    return {
        "passed": bool(result["verification_passed"]) and bool(second["verification_passed"]),
        "exact_verify": {
            "passed": bool(result["verification_passed"]),
            "pairs_tested": result["pairs_tested"],
            "minimum_containment_clearance": _short(result["minimum_containment_clearance"]),
            "minimum_best_pair_gap": _short(result["minimum_best_pair_gap"]),
            "failures": [list(failure) for failure in result["failures"][:10]],
            "seconds": round(sqpack_seconds, 3),
        },
        "independent": {
            "passed": bool(second["verification_passed"]),
            "pairs_tested": second["pairs_tested"],
            "minimum_containment_clearance": _short(second["minimum_containment_clearance"]),
            "minimum_best_pair_gap": _short(second["minimum_best_pair_gap"]),
            "failures": second["failures"][:10],
            "seconds": round(independent_seconds, 3),
        },
    }


# --------------------------------------------------------------------------------------
# The exact re-solve at a fixed side
# --------------------------------------------------------------------------------------


def _round_to(value: Fraction, digits: int | None) -> Fraction:
    if digits is None:
        return value
    scale = 10**digits
    return Fraction(round(value * scale), scale)


def _rounding_name(digits: int | None, free: int) -> str:
    if free == 0:
        return "none: every unknown is determined"
    if digits is None:
        return "the approximate values themselves"
    return f"nearest multiple of 10^-{digits}, ties to even"


def _rotation_refusal(rotations: Sequence[Basis]) -> Refusal | None:
    """Why the rotations are not exact rotations, or `None` when they are."""
    inexact = [index for index, basis in enumerate(rotations) if not _exact_basis(basis)]
    if inexact:
        return Refusal(
            "malformed-input",
            f"{len(inexact)} rotation(s) are not pairs of exact rationals (int or Fraction)",
            tuple({"square": index} for index in inexact[:20]),
        )
    bad = [index for index, basis in enumerate(rotations) if not is_rotation(basis)]
    if bad:
        return Refusal(
            "not-a-rotation",
            f"{len(bad)} rotation(s) do not satisfy c^2 + s^2 = 1 exactly",
            tuple({"square": index} for index in bad[:20]),
        )
    return None


def _exact_centres(
    approx_centres: Sequence[tuple[Approximate, Approximate]],
) -> list[Point] | Refusal:
    """The approximate centres as exact rationals, or the first that is malformed."""
    approx: list[Point] = []
    for index, centre in enumerate(approx_centres):
        if not isinstance(centre, tuple | list) or len(centre) != 2:
            return Refusal("malformed-input", f"square {index}'s centre is not a pair")
        x = _read(centre[0], f"square {index}'s approximate x")
        if isinstance(x, Refusal):
            return x
        y = _read(centre[1], f"square {index}'s approximate y")
        if isinstance(y, Refusal):
            return y
        approx.append((x, y))
    return approx


def _options(
    tight_tol: Approximate,
    move_limit: Approximate,
    free_digits: Sequence[int | None],
    on_conflict: str,
) -> tuple[Fraction, Fraction] | Refusal:
    """The tight tolerance and move limit as exact rationals, and the other options
    checked, or why they cannot be used."""
    tolerance = _read(tight_tol, "the tight tolerance", sign="positive")
    if isinstance(tolerance, Refusal):
        return tolerance
    limit = _read(move_limit, "the move limit", sign="nonnegative")
    if isinstance(limit, Refusal):
        return limit
    if on_conflict not in {"refuse", "relax"}:
        return Refusal(
            "malformed-input", f"on_conflict is {on_conflict!r}, not refuse or relax"
        )
    for digits in free_digits:
        if digits is not None and (
            not isinstance(digits, int)
            or isinstance(digits, bool)
            or not 0 <= digits <= EXPONENT_LIMIT
        ):
            return Refusal(
                "malformed-input",
                f"free_digits holds {digits!r}: each rung is None or a whole number of "
                f"places from 0 to {EXPONENT_LIMIT}",
            )
    return tolerance, limit


@dataclass(frozen=True)
class _Inputs:
    """`resolve_at_side`'s inputs, read exactly."""

    side: Fraction
    approx: list[Point]
    tolerance: Fraction
    move_limit: Fraction


def _validated(
    side: Approximate,
    rotations: Sequence[Basis],
    approx_centres: Sequence[tuple[Approximate, Approximate]],
    ids: Sequence[Any] | None,
    *,
    tight_tol: Approximate,
    move_limit: Approximate,
    free_digits: Sequence[int | None],
    on_conflict: str,
) -> _Inputs | Refusal:
    """Every input as an exact rational or checked option, or why one cannot be."""
    options = _options(tight_tol, move_limit, free_digits, on_conflict)
    if isinstance(options, Refusal):
        return options
    exact_side = _read(side, "the side", sign="positive")
    if isinstance(exact_side, Refusal):
        return exact_side
    if len(rotations) != len(approx_centres) or (
        ids is not None and len(ids) != len(rotations)
    ):
        return Refusal(
            "count-mismatch",
            f"{len(rotations)} rotations, {len(approx_centres)} centres"
            + (f", {len(ids)} ids" if ids is not None else ""),
        )
    refused = _rotation_refusal(rotations)
    if refused is not None:
        return refused
    approx = _exact_centres(approx_centres)
    if isinstance(approx, Refusal):
        return approx
    return _Inputs(exact_side, approx, *options)


def tight_constraints(
    side: Fraction,
    rotations: Sequence[Basis],
    approx: Sequence[Point],
    tolerance: Fraction,
    ids: Sequence[Any] | None = None,
) -> tuple[list[Constraint], list[int]] | Refusal:
    """Every wall and in-reach pair at the approximate point, and the tight ones in order.

    The order is the elimination order: near walls, then pairs, then far walls, each by
    approximate gap and then by position. Refused when any approximate gap is
    `-tolerance` or less.
    """
    constraints: list[Constraint] = []
    for index, (basis, centre) in enumerate(zip(rotations, approx, strict=True)):
        constraints.extend(wall_constraints(index, basis, centre, side))
    constraints.extend(
        pair_constraint(i, j, rotations, approx) for i, j in close_pairs(approx, REACH_SQUARED)
    )
    overlapping = sorted(
        (c for c in constraints if c.approx_gap <= -tolerance), key=lambda c: c.approx_gap
    )
    if overlapping:
        return Refusal(
            "approximate-overlap",
            f"{len(overlapping)} constraint(s) fail by at least the tight tolerance at the "
            "approximate point: the view is not even approximately a packing at this side",
            tuple(
                {"constraint": c.label(ids), "approx_gap": _e(c.approx_gap)}
                for c in overlapping[:20]
            ),
        )
    tight = sorted(
        (tag for tag, c in enumerate(constraints) if c.approx_gap < tolerance),
        key=lambda tag: (constraints[tag].group, constraints[tag].approx_gap, tag),
    )
    return constraints, tight


@dataclass
class Closure:
    """The tight set reduced over Q: pivots, consistent redundancies, relaxed conflicts."""

    echelon: _Echelon
    redundant: int
    relaxed: dict[int, dict[str, Any]]
    """Tight constraints left as inequalities, by constraint index, with the evidence."""
    restarts: int = 0


def _evidence(
    tag: int, row: _Row, constraints: Sequence[Constraint], ids: Sequence[Any] | None
) -> dict[str, Any]:
    return {
        "constraint": constraints[tag].label(ids),
        "kind": constraints[tag].kind,
        "forced_gap": evidence_literal(-row.rhs),
        "forced_gap_decimal": _e(-row.rhs),
        "farkas": _farkas(row),
        "certificate": list(_certificate(row, constraints, ids)),
    }


def _swap_candidate(row: _Row, order: Mapping[int, int]) -> int:
    """The latest constraint of a forced-overlap certificate with a negative multiplier.

    With `r > 0` and the conflicting row's own multiplier 1, leaving `m` slack instead,
    with every other row of the certificate closed, gives `g_m = -r / l_m`, positive
    exactly when `l_m < 0`; such an `m` exists exactly when the certificate is not Farkas.
    """
    negative = [tag for tag, multiplier in row.combination.items() if multiplier < 0]
    return max(negative, key=lambda tag: order[tag])


def predicted_shift(row: _Row, constraints: Sequence[Constraint]) -> Fraction:
    """How far imposing a reduced row moves the approximate point, to first order, exactly.

    The row is `sum_k l_k (a_k . z - b_k) = 0`; at the approximate point its residual is
    `sum_k l_k g_k` with `g_k` the approximate gaps, and moving along the row's own
    direction removes it at the cost `|residual| / max|coefficient|`. A row that is a
    near-combination of earlier rows has tiny coefficients and a large shift.
    """
    residual = sum(
        (
            multiplier * constraints[tag].approx_gap
            for tag, multiplier in row.combination.items()
        ),
        Fraction(0),
    )
    return abs(residual) / max(map(abs, row.coefficients.values()))


def _close_once(
    constraints: Sequence[Constraint],
    tight: Sequence[int],
    excluded: Mapping[int, dict[str, Any]],
    *,
    on_conflict: ConflictPolicy,
    ids: Sequence[Any] | None,
    move_limit: Fraction,
) -> Closure | Refusal | tuple[int, dict[str, Any]]:
    """One elimination pass; a constraint to leave slack and restart, if one is needed."""
    order = {tag: position for position, tag in enumerate(tight)}
    closure = Closure(_Echelon(), 0, dict(excluded))
    for tag in tight:
        if tag in excluded:
            continue
        row = closure.echelon.reduce(tag, constraints[tag])
        if row.coefficients:
            shift = predicted_shift(row, constraints)
            if shift <= move_limit:
                closure.echelon.add(row)
                continue
            evidence = {
                "constraint": constraints[tag].label(ids),
                "kind": constraints[tag].kind,
                "predicted_shift": _e(shift),
                "largest_reduced_coefficient": _e(max(map(abs, row.coefficients.values()))),
            }
            if on_conflict == "refuse":
                return Refusal(
                    "ill-conditioned-tight-set",
                    f"closing {constraints[tag].label(ids)} would shift the view by about "
                    f"{_e(shift)}, more than {_e(move_limit)}: the tight constraints before it "
                    "nearly determine it already (nearly parallel contacts)",
                    (evidence,),
                )
            closure.relaxed[tag] = {**evidence, "relaxed": "ill-conditioned"}
            continue
        if row.rhs == 0:
            closure.redundant += 1
            continue
        evidence = _evidence(tag, row, constraints, ids)
        label = constraints[tag].label(ids)
        if on_conflict == "refuse":
            farkas = " (a Farkas certificate: these axes cannot all hold)"
            return Refusal(
                "inconsistent-tight-set",
                f"closing {label} contradicts the tight constraints before it: they force "
                f"its gap to {_e(-row.rhs)}, not 0" + (farkas if evidence["farkas"] else ""),
                (evidence,),
            )
        if row.rhs < 0:
            closure.relaxed[tag] = {**evidence, "relaxed": "slack"}
            continue
        if evidence["farkas"]:
            return Refusal(
                "tight-set-forces-overlap",
                f"the tight constraints before {label} force its gap to "
                f"{_e(-row.rhs)} < 0, and the certificate is Farkas: these "
                "separating axes cannot all hold at this side with these rotations",
                (evidence,),
            )
        swap = _swap_candidate(row, order)
        multiplier = row.combination[swap]
        forced = -row.rhs / multiplier
        return swap, {
            "constraint": constraints[swap].label(ids),
            "kind": constraints[swap].kind,
            "forced_gap": evidence_literal(forced),
            "forced_gap_decimal": _e(forced),
            "farkas": False,
            "relaxed": f"swapped for {label}",
            "certificate": evidence["certificate"],
        }
    return closure


def close_tight_set(
    constraints: Sequence[Constraint],
    tight: Sequence[int],
    *,
    on_conflict: ConflictPolicy = "refuse",
    ids: Sequence[Any] | None = None,
    move_limit: Fraction = MOVE_LIMIT,
) -> Closure | Refusal:
    """Impose the tight constraints as equalities, in order, refusing or relaxing conflicts.

    A row whose imposition would shift the approximate point by more than `move_limit`
    (`predicted_shift`) is not imposed: refused under `"refuse"`, left slack under
    `"relax"`.

    Under `"relax"`: a conflict whose forced gap `-r` is positive is left slack; one whose
    forced gap is negative is refused when its certificate is Farkas, and otherwise the
    latest constraint of the certificate with a negative multiplier is left slack in its
    place (`_swap_candidate`) and the elimination restarts. Each restart leaves one more
    constraint slack, so there are at most as many as tight constraints. Nothing here
    admits an overlap: the pose is checked exactly and completely afterwards.
    """
    excluded: dict[int, dict[str, Any]] = {}
    for restart in range(len(tight) + 1):
        outcome = _close_once(
            constraints,
            tight,
            excluded,
            on_conflict=on_conflict,
            ids=ids,
            move_limit=move_limit,
        )
        if isinstance(outcome, tuple):
            swap, evidence = outcome
            excluded[swap] = evidence
            continue
        if isinstance(outcome, Closure):
            outcome.restarts = restart
        return outcome
    raise AssertionError("each restart leaves one more tight constraint slack")


def fix_free(
    side: Fraction,
    rotations: Sequence[Basis],
    approx: Sequence[Point],
    echelon: _Echelon,
    *,
    free_digits: Sequence[int | None] = FREE_DIGITS,
    ids: Sequence[Any] | None = None,
) -> tuple[list[Point], list[int], int | None] | Refusal:
    """Fix the free unknowns on the rounding ladder, back-substitute, and check exactly.

    Returns the first pose `pose_failures` passes, the free unknowns, and the rung used.
    An empty ladder is refused when any unknown is free, since nothing would fix it.
    """
    unknowns = 2 * len(approx)
    free = [k for k in range(unknowns) if k not in echelon.rows]
    ladder: list[int | None] = list(free_digits) if free else [None]
    if not ladder:
        return Refusal(
            "malformed-input",
            f"free_digits is empty, and {len(free)} unknown(s) are free: no rung fixes them",
        )
    approx_values = [approx[k // 2][k % 2] for k in range(unknowns)]
    failures: list[str] = []
    centres: list[Point] = []
    for digits in ladder:
        values = list(approx_values)
        for k in free:
            values[k] = _round_to(approx_values[k], digits)
        echelon.solve(values)
        centres = [(values[2 * i], values[2 * i + 1]) for i in range(len(approx))]
        failures = pose_failures(side, rotations, centres, ids=ids)
        if not failures:
            return centres, free, digits
    moves = sorted(
        (
            (max(abs(c[0] - a[0]), abs(c[1] - a[1])), index)
            for index, (c, a) in enumerate(zip(centres, approx, strict=True))
        ),
        reverse=True,
    )
    return Refusal(
        "verification-failed",
        f"the exact re-solve is not a packing at side {literal(side)} at any rounding of "
        "the free unknowns tried: the closed contacts leave no room for the rest (a large "
        "move below means an ill-conditioned tight set, two nearly parallel contacts "
        "pinning one square)",
        (
            *({"failure": failure} for failure in failures),
            *(
                {"square": ids[index] if ids is not None else index, "move": _e(move)}
                for move, index in moves[:3]
            ),
        ),
    )


def decide_pose(
    side: Fraction,
    rotations: Sequence[Basis],
    centres: Sequence[Point],
    *,
    ids: Sequence[Any] | None = None,
    witness_id: str = "W-same-side-view",
) -> tuple[dict[str, Any], dict[str, Any]] | Refusal:
    """The pose as a Witness/v2 mapping and both maintained verdicts on it, or a refusal."""
    try:
        witness = pose_witness(side, rotations, centres, ids=ids, witness_id=witness_id)
    except ValueError as error:
        return Refusal(
            "literal-too-large",
            "the exact pose has a coordinate whose literal exceeds the interpreter's "
            f"integer digit limit, so no Witness/v2 file could carry or re-read it: {error}",
        )
    verification = verify_pose(witness)
    if not verification["passed"]:
        return Refusal(
            "routes-refused",
            "a maintained exact route refused a pose this module's own complete check "
            "passed: the checkers disagree, so one of them has a bug",
            (verification,),
        )
    witness["claim"]["coordinate_provenance"] = "verified"
    # No `side_relation` here: only `resolve_view` knows the source's side to compare.
    witness["certificate"] = {
        "kind": "regularized-view",
        "label": "regularized",
        "algorithm": ALGORITHM,
        "replay": "uv run --frozen packing-witness verify <this file>",
    }
    return witness, verification


def resolve_at_side(
    side: Approximate,
    rotations: Sequence[Basis],
    approx_centres: Sequence[tuple[Approximate, Approximate]],
    *,
    tight_tol: Approximate = DEFAULT_TIGHT_TOLERANCE,
    on_conflict: ConflictPolicy = "refuse",
    free_digits: Sequence[int | None] = FREE_DIGITS,
    move_limit: Approximate = MOVE_LIMIT,
    ids: Sequence[Any] | None = None,
    witness_id: str = "W-same-side-view",
) -> Resolved | Refusal:
    """Close the view's tight contacts over Q at exactly `side`, and verify the pose.

    `rotations` are exact and fixed; `approx_centres` choose the separating axes and the
    tight set and fix free unknowns. The module docstring states the method and exactly
    what a `Resolved` result proves.
    """
    seconds: dict[str, float] = {}
    clock = time.perf_counter()
    checked = _validated(
        side,
        rotations,
        approx_centres,
        ids,
        tight_tol=tight_tol,
        move_limit=move_limit,
        free_digits=free_digits,
        on_conflict=on_conflict,
    )
    if isinstance(checked, Refusal):
        return checked
    exact_side, approx = checked.side, checked.approx
    collected = tight_constraints(exact_side, rotations, approx, checked.tolerance, ids)
    if isinstance(collected, Refusal):
        return collected
    constraints, tight = collected
    seconds["constraints"] = time.perf_counter() - clock

    clock = time.perf_counter()
    closure = close_tight_set(
        constraints,
        tight,
        on_conflict=on_conflict,
        ids=ids,
        move_limit=checked.move_limit,
    )
    if isinstance(closure, Refusal):
        return closure
    seconds["eliminate"] = time.perf_counter() - clock

    clock = time.perf_counter()
    fixed = fix_free(
        exact_side, rotations, approx, closure.echelon, free_digits=free_digits, ids=ids
    )
    if isinstance(fixed, Refusal):
        return fixed
    centres, free, chosen = fixed
    values = [coordinate for centre in centres for coordinate in centre]
    seconds["solve_and_check"] = time.perf_counter() - clock

    clock = time.perf_counter()
    decided = decide_pose(exact_side, rotations, centres, ids=ids, witness_id=witness_id)
    seconds["verify"] = time.perf_counter() - clock
    if isinstance(decided, Refusal):
        return decided
    witness, verification = decided
    tight_walls = sum(constraints[tag].kind == "wall" for tag in tight)
    return Resolved(
        side=exact_side,
        centres=tuple(centres),
        rotations=tuple(rotations),
        witness=witness,
        constraints=len(constraints),
        tight_walls=tight_walls,
        tight_pairs=len(tight) - tight_walls,
        closed=len(tight) - len(closure.relaxed),
        redundant=closure.redundant,
        relaxed=tuple(
            {
                **evidence,
                "gap_after": evidence_literal(constraints[tag].gap(values)),
                "gap_after_decimal": _e(constraints[tag].gap(values)),
            }
            for tag, evidence in sorted(closure.relaxed.items())
        ),
        restarts=closure.restarts,
        rank=len(closure.echelon.rows),
        unknowns=2 * len(centres),
        free_unknowns=len(free),
        free_rounding=_rounding_name(chosen, len(free)),
        max_move=max(
            (
                max(abs(c[0] - a[0]), abs(c[1] - a[1]))
                for c, a in zip(centres, approx, strict=True)
            ),
            default=Fraction(0),
        ),
        verification=verification,
        seconds={key: round(value, 3) for key, value in seconds.items()},
    )


# --------------------------------------------------------------------------------------
# The source witness's frame, and a view re-solved in it
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class SourceFrame:
    """The exact side and rotations a view is re-solved with, and where they came from."""

    side: Fraction
    printed_side: Fraction
    rotations: tuple[Basis, ...]
    centres: tuple[Point, ...]
    ids: tuple[Any, ...]
    scalar_kind: str
    derivation: str


def _frame_from_corners(
    squares: Sequence[Sequence[Point]],
) -> tuple[list[Basis], list[Point]] | Refusal:
    rotations: list[Basis] = []
    centres: list[Point] = []
    for index, square in enumerate(squares):
        (x0, y0), (x1, y1) = square[0], square[1]
        basis = (x1 - x0, y1 - y0)
        if not is_rotation(basis):
            return Refusal(
                "not-a-rotation",
                f"square {index}'s first edge is not an exact unit vector",
                ({"square": index},),
            )
        rotations.append(basis)
        centres.append(
            (
                sum((x for x, _ in square), Fraction(0)) / 4,
                sum((y for _, y in square), Fraction(0)) / 4,
            )
        )
    return rotations, centres


def source_frame(witness: Mapping[str, Any]) -> SourceFrame | Refusal:
    """The witness's exact side and rotations: its own, or its 36-digit promotion's."""
    kind = witness["scalar"]["kind"]
    ids = tuple(square["id"] for square in witness["squares"])
    if kind == "rational":
        try:
            expanded, side = materialize_exact_witness(witness)
        except WitnessError as error:
            return Refusal(
                "malformed-input"
                if error.kind == "malformed-scalar"
                else "promotion-unsupported",
                f"no exact rational frame can be read from this rational witness "
                f"({error.kind}): {error}; this tool promotes only decimal angles",
            )
        if not isinstance(side, Fraction):
            raise TypeError("a rational witness has a rational side")
        squares = [[(Fraction(x), Fraction(y)) for x, y in square] for square in expanded]
        derivation = "the witness's own exact side and rotations"
    elif kind == "decimal":
        try:
            promoted, side = _promoted_candidate(
                witness, rational_digits=RATIONAL_DIGITS, dilation=Fraction(1)
            )
        except WitnessError as error:
            return Refusal(
                "promotion-unsupported",
                f"no {RATIONAL_DIGITS}-digit rational frame can be built: {error}",
            )
        squares = [[(Fraction(x), Fraction(y)) for x, y in square] for square in promoted]
        derivation = (
            f"the side and rotations of the witness's {RATIONAL_DIGITS}-digit rational "
            "promotion at centre dilation 1, the frame regularize_axis_components uses: "
            f"centres and t = tan(theta/2) rounded to {RATIONAL_DIGITS} significant digits, "
            "translated onto the near walls, the side the larger extent"
        )
    else:
        return Refusal(
            "unsupported-scalar-kind",
            f"{kind!r} geometry has no exact rational frame here: an enclosure proves no "
            "equality and an algebraic field needs field arithmetic this tool lacks",
        )
    frame = _frame_from_corners(squares)
    if isinstance(frame, Refusal):
        return frame
    rotations, centres = frame
    printed_side = _read(str(witness["side"]), "the witness's printed side", sign="positive")
    if isinstance(printed_side, Refusal):
        return printed_side
    return SourceFrame(
        side=side,
        printed_side=printed_side,
        rotations=tuple(rotations),
        centres=tuple(centres),
        ids=ids,
        scalar_kind=kind,
        derivation=derivation,
    )


def self_view(frame: SourceFrame) -> list[ViewSquare]:
    """The frame's own pose as a view: binary64 centres, the exact rotations."""
    return [
        (float(x), float(y), basis)
        for (x, y), basis in zip(frame.centres, frame.rotations, strict=True)
    ]


def register_flag(
    side: Fraction, scalar_kind: str, verified_bound: Fraction | None
) -> dict[str, Any]:
    """Whether an exact packing at `side` would itself be a register result. Decides nothing."""
    if verified_bound is None:
        below = None
        note = (
            "the register's verified bound was not supplied; for a decimal witness an "
            "exact packing at this side may be a new verified upper bound, which is an "
            "owner decision"
            if scalar_kind == "decimal"
            else "the register's verified bound was not supplied"
        )
    else:
        below = side < verified_bound
        note = (
            "below the register's verified bound: an exact packing here is a new verified "
            "upper bound, a register result and an owner decision, not only a drawing"
            if below
            else "not below the register's verified bound: no register consequence"
        )
    return {
        "verified_bound": None if verified_bound is None else evidence_literal(verified_bound),
        "below_verified_bound": below,
        "note": note,
    }


def _view_options(
    tol: Approximate, side: Approximate | None, verified_bound: Approximate | None
) -> tuple[Fraction, Fraction | None, Fraction | None] | Refusal:
    """`resolve_view`'s own scalars read exactly, or the first that is malformed."""
    tolerance = _read(tol, "the snap tolerance", sign="nonnegative")
    if isinstance(tolerance, Refusal):
        return tolerance
    supplied = None if side is None else _read(side, "the side", sign="positive")
    if isinstance(supplied, Refusal):
        return supplied
    bound = None if verified_bound is None else _read(verified_bound, "the verified bound")
    if isinstance(bound, Refusal):
        return bound
    return tolerance, supplied, bound


def _view_refusal(view_squares: Sequence[ViewSquare], n: int) -> Refusal | None:
    """Why the view cannot be re-solved against an `n`-square witness, or `None`."""
    if len(view_squares) != n:
        return Refusal(
            "count-mismatch", f"the view has {len(view_squares)} squares, the witness {n}"
        )
    malformed = [
        index
        for index, square in enumerate(view_squares)
        if not isinstance(square, tuple | list)
        or len(square) != 3
        or not _exact_basis(square[2])
    ]
    if malformed:
        return Refusal(
            "malformed-input",
            f"{len(malformed)} view square(s) are not (x, y, basis) with an exact basis",
            tuple({"square": index} for index in malformed[:20]),
        )
    return None


def resolve_view(
    source_witness: Mapping[str, Any],
    view_squares: Sequence[ViewSquare],
    *,
    side: Approximate | None = None,
    tol: Approximate = DEFAULT_SNAP_TOLERANCE,
    tight_tol: Approximate = DEFAULT_TIGHT_TOLERANCE,
    on_conflict: ConflictPolicy = "refuse",
    free_digits: Sequence[int | None] = FREE_DIGITS,
    move_limit: Approximate = MOVE_LIMIT,
    verified_bound: Approximate | None = None,
) -> ViewResolution | Refusal:
    """Re-solve a view, given in the source witness's frame, at the witness's side.

    `view_squares` are `(x, y, basis)` in the witness's lower-left frame and orientation,
    square `k` labelled with the witness's `k`-th id (a label, not a correspondence).
    `side` defaults to the witness's exact side as `source_frame` defines it.
    `verified_bound`, the register's verified upper bound for `n` when the caller knows
    it, only sets the `register` flag. The pose's `certificate.side_relation` is `same`
    exactly when the side used is the frame's side, and `solved` otherwise.
    """
    options = _view_options(tol, side, verified_bound)
    if isinstance(options, Refusal):
        return options
    tolerance, supplied, bound = options
    frame = source_frame(source_witness)
    if isinstance(frame, Refusal):
        return frame
    refused = _view_refusal(view_squares, len(frame.rotations))
    if refused is not None:
        return refused
    snapped = snap_rotations(
        [basis for _, _, basis in view_squares], frame.rotations, tolerance
    )
    if isinstance(snapped, Refusal):
        return snapped
    exact_side = frame.side if supplied is None else supplied
    relation = "same" if exact_side == frame.side else "solved"
    resolved = resolve_at_side(
        exact_side,
        snapped.rotations,
        [(x, y) for x, y, _ in view_squares],
        tight_tol=tight_tol,
        on_conflict=on_conflict,
        free_digits=free_digits,
        move_limit=move_limit,
        ids=frame.ids,
        witness_id=f"{source_witness['id']}-{relation}-side",
    )
    if isinstance(resolved, Refusal):
        return resolved
    resolved.witness["certificate"]["side_relation"] = relation
    resolved.witness["certificate"]["derived_from"] = source_witness["id"]
    side_basis = {
        "scalar_kind": frame.scalar_kind,
        "derivation": frame.derivation if side is None else "supplied by the caller",
        "frame_side": literal(frame.side),
        "printed_side": literal(frame.printed_side),
        "side_minus_printed": evidence_literal(exact_side - frame.printed_side),
        "side_minus_printed_decimal": _e(exact_side - frame.printed_side),
        "fits_printed_side": exact_side <= frame.printed_side,
    }
    return ViewResolution(
        resolved, snapped, side_basis, register_flag(exact_side, frame.scalar_kind, bound)
    )


# --------------------------------------------------------------------------------------
# Evan Daniel's per-count view JSON, for the command line
# --------------------------------------------------------------------------------------


def evand_view(document: Mapping[str, Any]) -> list[ViewSquare]:
    """A regularization JSON's `packing` at its `S*`, mapped back into the source frame.

    Rows are `x y degrees`; the view was drawn in container orientation `orientation_g`
    (`reg.py` `d4`: `g & 3` quarter turns `(x, y) -> (S - y, x)`, then, if `g & 4`, the
    mirror `x -> S - x`), which is undone here: the mirror first, then the remaining
    quarter turns. Rotations go through `basis_from_angle`, the promotion's rule.
    """
    packing = document["packing"]
    side = Fraction(str(packing["S"]))
    g = int(document.get("orientation_g", 0))
    view: list[ViewSquare] = []
    for x_text, y_text, angle in packing["sq"]:
        x, y = Fraction(str(x_text)), Fraction(str(y_text))
        basis = basis_from_angle(str(angle))
        if g & 4:
            x, basis = side - x, (basis[0], -basis[1])
        for _ in range((4 - (g & 3)) % 4):
            x, y = side - y, x
            basis = quarter_turn(basis, 1)
        view.append((x, y, basis))
    return view


def _read_json(path: Path) -> Any:
    opener: Callable[..., Any] = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        prog="python -m devtools.regularize_same_side",
        description="Re-solve a view over Q at exactly its source witness's side.",
    )
    command.add_argument("witness", type=Path, help="the source Witness/v2 YAML")
    command.add_argument(
        "--view-json",
        type=Path,
        help="Evan Daniel's per-count regularization JSON (.json or .json.gz); "
        "default: the witness's own pose in binary64",
    )
    command.add_argument(
        "--relax",
        action="store_true",
        help="leave conflicting tight constraints as slack inequalities instead of refusing",
    )
    command.add_argument("--tight-tol", default=str(DEFAULT_TIGHT_TOLERANCE))
    command.add_argument("--snap-tol", default=str(DEFAULT_SNAP_TOLERANCE))
    command.add_argument(
        "--verified-bound", help="the register's verified upper bound, for the flag only"
    )
    command.add_argument("--json", action="store_true", help="print the full JSON summary")
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    witness = load_witness(args.witness, fallback_schema=WITNESS_SCHEMA)
    if args.view_json is not None:
        view = evand_view(_read_json(args.view_json))
    else:
        frame = source_frame(witness)
        if isinstance(frame, Refusal):
            print(json.dumps(frame.summary(), indent=2))
            return 1
        view = self_view(frame)
    outcome = resolve_view(
        witness,
        view,
        tol=args.snap_tol,
        tight_tol=args.tight_tol,
        on_conflict="relax" if args.relax else "refuse",
        verified_bound=args.verified_bound,
    )
    summary = outcome.summary()
    if args.json or isinstance(outcome, Refusal):
        print(json.dumps(summary, indent=2, default=str))
    else:
        resolved = outcome.resolved
        print(
            f"{outcome.side_relation.upper()} SIDE: n={len(resolved.centres)} "
            f"side={summary['side_decimal']} "
            f"tight={resolved.tight} closed={resolved.closed} relaxed={len(resolved.relaxed)} "
            f"free={resolved.free_unknowns} ({resolved.free_rounding}) "
            f"max_move={summary['max_move']} seconds={resolved.seconds}"
        )
    return 0 if isinstance(outcome, ViewResolution) else 1


if __name__ == "__main__":
    raise SystemExit(main())
