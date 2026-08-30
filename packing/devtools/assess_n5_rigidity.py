#!/usr/bin/env python3
"""Decide the first-order rigidity of the proved-optimal n=5 packing, exactly.

`BC-049` asks whether the three packings the source catalogue annotates "Rigid." are
actually rigid on evidence of our own. `D-354` forbids promoting the catalogue's word into
the rigidity block, and the translation-escape screen cannot supply the answer either: it
decides single-square translation in every direction and finds none at n = 5, but rotation
and coordinated multi-square motion are outside it.

This asks the first-order question directly, for all five squares at once. An
**infinitesimal motion** gives each square a velocity and an angular velocity so that to
first order no contact is violated. Those motions form the polyhedral cone `{x : Ax >= 0}`,
and the packing is infinitesimally rigid exactly when that cone is the origin.

**It is not.** The cone is a line, spanned by rotation of the middle square about its own
centre; all fourteen other coordinates are pinned, each with an exact Farkas certificate.
The contacts cannot see that rotation because each corner square's inner corner rests at
the *midpoint* of the middle square's edge -- the foot of the perpendicular from its
centre -- so the rotation term `(p - c) . n_perp` vanishes identically.

**And that is not the end of it.** The same geometry that hides the rotation at first order
condemns it at second. The resting corner is where the edge line comes closest to the
middle square's centre, so turning the line can only bring it nearer: each pair gap is
exactly `(1/2) cos(t) - 1/2` along the rotation, curving into the obstacle from both sides.
A non-negative self-stress `w` with `w . A = 0` and `w . q < 0`, verified in the field,
proves no second-order correction rescues it. So the packing is **second-order rigid**:
infinitesimally flexible in exactly one direction, and that direction obstructed.

Three things make this worth retaining over what `bc-063` recorded numerically:

- it is **exact**, over `Q(sqrt 2)`, so contacts are decided by sign rather than tolerance
  and the pinning is certified rather than observed as a rank;
- it covers **rotation and all five squares**, so "no single-square translation" becomes
  "no infinitesimal motion at all except this one";
- the obstruction is a **certificate**, not a sampled walk: `bc-063` observed the second
  order coefficient along one displayed direction, where this exhibits weights that refuse
  every correction at once.

**The pose is `cases.gobel5`, not the retained witness.** The witness's decimals put the
middle square's centre `2.4e-30` off the diagonal, which the escape screen records as a
`-6.9e-30` pair separation; a certificate built on it would certify an infeasible
configuration. Göbel's construction is exact and independently verified.

Usage:
    uv run --frozen python -m devtools.assess_n5_rigidity
    uv run --frozen python -m devtools.assess_n5_rigidity --check
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from strif import atomic_output_file

from cases.gobel5.packing import build
from sqpack.field import FieldElement, NumberField

ROOT = pathlib.Path(__file__).resolve().parent.parent
RESULTS = ROOT / "campaign" / "series" / "series-000-smoke-and-calibration" / "results"
OUT = RESULTS / "bc-049-n5-rigidity-certificates.json"

DOF = 3
"""Two of translation and one of rotation, per square."""

Point = tuple[FieldElement, FieldElement]


@dataclass(frozen=True, slots=True)
class Pose:
    """Göbel's exact n=5 packing, as corners in `Q(sqrt 2)`."""

    field: NumberField
    side: FieldElement
    squares: tuple[tuple[Point, ...], ...]

    @property
    def count(self) -> int:
        return len(self.squares)

    def centre(self, index: int) -> Point:
        quarter = self.field.rational(1) / self.field.rational(4)
        xs = [corner[0] for corner in self.squares[index]]
        ys = [corner[1] for corner in self.squares[index]]
        return (sum(xs[1:], xs[0]) * quarter, sum(ys[1:], ys[0]) * quarter)

    def edge(self, index: int, edge: int) -> tuple[Point, Point]:
        corners = self.squares[index]
        return corners[edge], corners[(edge + 1) % len(corners)]

    def normal(self, index: int, edge: int) -> Point:
        """Outward unit normal of one edge.

        Göbel's corners run counter-clockwise, so for an edge `p -> q` the outward normal
        is `(dy, -dx)`. Every edge has length one, so this is already a unit vector and
        nothing needs scaling to stay inside the field.
        """
        (px, py), (qx, qy) = self.edge(index, edge)
        return (qy - py, px - qx)


def load_pose() -> Pose:
    squares, side, field = build()
    return Pose(field, side, tuple(tuple(square) for square in squares))


@dataclass(frozen=True, slots=True)
class Contact:
    """One active contact: a corner resting on a wall, or on another square's edge."""

    kind: str
    moving: int
    corner: int
    host: int | None = None
    edge: int | None = None
    wall: str | None = None

    def describe(self) -> str:
        if self.kind == "wall":
            return f"square {self.moving} corner {self.corner} on the {self.wall} wall"
        return (
            f"square {self.moving} corner {self.corner} on square {self.host} edge {self.edge}"
        )


WALL_NORMALS: dict[str, tuple[int, int]] = {
    "left": (1, 0),
    "bottom": (0, 1),
    "right": (-1, 0),
    "top": (0, -1),
}


def incident_contacts(pose: Pose) -> list[Contact]:
    """Every corner lying exactly on a wall or on the segment of another square's edge.

    Decided by exact sign. A tight packing is one whose squares touch exactly, so a
    tolerance test here either invents contacts or misses the ones holding it together.

    **Incidence is not contact**, and the difference is the whole of `D-390`. This is the
    raw incidence relation, exposed so the gap between the two can be counted; the
    constraint system is built from `active_contacts` below.
    """
    zero = pose.field.rational(0)
    found: list[Contact] = []
    for index in range(pose.count):
        for corner_index, (px, py) in enumerate(pose.squares[index]):
            found.extend(
                Contact("wall", index, corner_index, wall=wall)
                for wall, value in (
                    ("left", px),
                    ("bottom", py),
                    ("right", pose.side - px),
                    ("top", pose.side - py),
                )
                if (value - zero).sign() == 0
            )
            found.extend(
                Contact("pair", index, corner_index, host=host, edge=edge)
                for host in range(pose.count)
                if host != index
                for edge in range(len(pose.squares[host]))
                if _on_edge(pose, host, edge, (px, py))
            )
    return found


def _on_edge(pose: Pose, host: int, edge: int, point: Point) -> bool:
    """Is the point exactly on this edge's segment?

    Both halves are needed. Lying on the edge's supporting line is not enough, because that
    line extends past the square in both directions.
    """
    (ax, ay), (bx, by) = pose.edge(host, edge)
    nx, ny = pose.normal(host, edge)
    px, py = point
    if ((px - ax) * nx + (py - ay) * ny).sign() != 0:
        return False
    along = (px - ax) * (bx - ax) + (py - ay) * (by - ay)
    length = (bx - ax) * (bx - ax) + (by - ay) * (by - ay)
    return along.sign() >= 0 and (length - along).sign() >= 0


def separating(pose: Pose, host: int, edge: int, moving: int) -> bool:
    """Does this host edge put the *whole* moving square on its outer side?

    The test a corner incidence has to pass before it is a contact. Two convex bodies are
    disjoint exactly when some axis separates them, and a host edge is such an axis only if
    every corner of the moving square lies on its outer side -- not merely the one corner
    that happens to touch its line.

    An edge-to-edge neighbour fails this on two of its edges and passes on one. Squares at
    centres `(1/2, 1/2)` and `(3/2, 1/2)` are separated by the vertical line `x = 1` and by
    nothing else, yet the first square's corners `(1, 0)` and `(1, 1)` land on the
    *endpoints* of the second's bottom and top edges, and `_on_edge` accepts an endpoint.
    Reading those as contacts asserts that the first square may not move down, which is
    false: it may, and nothing overlaps.
    """
    (ax, ay), _ = pose.edge(host, edge)
    nx, ny = pose.normal(host, edge)
    return all(((px - ax) * nx + (py - ay) * ny).sign() >= 0 for px, py in pose.squares[moving])


def active_contacts(pose: Pose) -> list[Contact]:
    """The incidences that are genuine contacts: every wall one, and the separating pairs.

    Containment is a conjunction -- a corner on the bottom-left of the container is held by
    both walls at once -- so every wall incidence is a constraint. A pair incidence is one
    only if its edge actually separates the two squares.
    """
    return [
        contact
        for contact in incident_contacts(pose)
        if contact.kind == "wall"
        or separating(pose, contact.host, contact.edge, contact.moving)  # type: ignore[arg-type]
    ]


def contact_axes(pose: Pose, contacts: list[Contact]) -> dict[frozenset[int], set[Point]]:
    """The distinct separating directions holding each touching pair, up to sign."""
    axes: dict[frozenset[int], set[Point]] = {}
    for contact in contacts:
        if contact.kind != "pair":
            continue
        assert contact.host is not None and contact.edge is not None
        nx, ny = pose.normal(contact.host, contact.edge)
        if nx.sign() < 0 or (nx.sign() == 0 and ny.sign() < 0):
            nx, ny = -nx, -ny
        axes.setdefault(frozenset((contact.moving, contact.host)), set()).add((nx, ny))
    return axes


class DisjunctiveContactError(RuntimeError):
    """A pair held apart by two axes at once, whose tangent cone is a union.

    Two squares meeting at a single corner are separated by two independent directions, and
    non-overlap asks for **either** to keep separating -- `a_1 . x >= 0` *or* `a_2 . x >= 0`.
    The linearized feasible set is the union of two half-spaces, which is not a polyhedron
    and not what a Farkas search decides.

    Intersecting them instead is the flattering error, exactly as in `D-388`: the
    intersection is a subset of each branch, so the cone comes out too small and the pose
    reads as more rigid than it is. Squares at `(1/2, 1/2)` and `(3/2, 3/2)` touch at one
    point and may separate along `x` or along `y`; requiring both forbids a motion that
    overlaps nothing.

    Measured on 2026-08-30: `n = 5` has none of these, which is why the assessment there is
    exactly right. Goebel's `n = 40` has 42 of its 98 touching pairs, and enumerating the
    branches is `2^42` linear programs.
    """


def disjunctive_pairs(pose: Pose, contacts: list[Contact]) -> list[frozenset[int]]:
    """The touching pairs whose tangent cone is a union rather than a half-space."""
    return [pair for pair, axes in contact_axes(pose, contacts).items() if len(axes) > 1]


def require_intersection_semantics(pose: Pose, contacts: list[Contact]) -> None:
    """Refuse a pose whose tangent cone is not the intersection of its contact half-spaces.

    Called before any search runs, so the assessor stops rather than answering a question
    its linearization does not pose.
    """
    disjunctive = disjunctive_pairs(pose, contacts)
    if disjunctive:
        raise DisjunctiveContactError(
            f"{len(disjunctive)} touching pairs are held apart by two axes at once "
            f"(first: squares {sorted(disjunctive[0])}); their tangent cone is a union of "
            "half-spaces and intersecting it reports a cone smaller than the geometry has"
        )


def constraint_rows(pose: Pose, contacts: list[Contact]) -> list[list[FieldElement]]:
    """One row per contact: the first-order rate of change of that contact's gap.

    For a corner of square `i` on an edge of square `h` the gap is
    `(p - c_h) . n_h(theta_h) - 1/2`, so its rate has three parts: the corner's velocity
    through `i`, the host's translation, and -- the part the translation screen has no
    analogue for -- the host's rotation turning the normal, through `(p - c_h) . n_perp`.

    That last term is exactly zero at all four pair contacts here, and it is the finding.
    """
    q = pose.field.rational
    rows: list[list[FieldElement]] = []
    for contact in contacts:
        row = [q(0) for _ in range(pose.count * DOF)]
        px, py = pose.squares[contact.moving][contact.corner]
        cx, cy = pose.centre(contact.moving)
        rx, ry = px - cx, py - cy
        if contact.kind == "wall":
            assert contact.wall is not None
            mx, my = (q(value) for value in WALL_NORMALS[contact.wall])
            row[contact.moving * DOF] = mx
            row[contact.moving * DOF + 1] = my
            row[contact.moving * DOF + 2] = -ry * mx + rx * my
        else:
            assert contact.host is not None and contact.edge is not None
            nx, ny = pose.normal(contact.host, contact.edge)
            hx, hy = pose.centre(contact.host)
            sx, sy = px - hx, py - hy
            row[contact.moving * DOF] = nx
            row[contact.moving * DOF + 1] = ny
            row[contact.moving * DOF + 2] = -ry * nx + rx * ny
            row[contact.host * DOF] = -nx
            row[contact.host * DOF + 1] = -ny
            row[contact.host * DOF + 2] = sx * (-ny) + sy * nx
        rows.append(row)
    return rows


class MixedRowError(RuntimeError):
    """A row this scaling cannot rationalize, which the search must not be handed.

    Raised rather than worked around, because the alternative is worse than an error. A
    row with both rational and `sqrt 2` parts in it cannot be made rational by any positive
    scalar, so the rational-weight linear program below would be solving a different system
    from the one the cone is defined by -- and it would answer. It would answer "no
    certificate", which reads as "this coordinate is not pinned", which reads as a motion.
    The flattering direction, from a silent limitation.

    Measured on 2026-08-30: Goebel's `n = 40` construction, built exactly in the same field,
    has 296 mixed rows out of 608, and the assessor reported every one of its 120
    coordinates unpinned before this guard existed. `n = 5` has none, which is why the
    dichotomy held there and why nothing caught it.

    Lifting this needs a Farkas search whose weights live in the ordered field rather than
    in `Q`, which is a different instrument and not a patch to this one.
    """


def row_scales(pose: Pose, rows: list[list[FieldElement]]) -> list[FieldElement]:
    """The positive constant each row must be multiplied by to make its entries rational.

    Returned rather than applied because the second-order test needs the *same* factors.
    Scaling row `j` scales the whole inequality `a_j . y + q_j >= 0`, so a `q` computed
    against unscaled rows and used against scaled ones is silently wrong by a factor of
    `sqrt 2` on exactly the four rows that carry the obstruction.
    """
    one = pose.field.rational(1)
    root = pose.field.alpha
    mixed = [
        index
        for index, row in enumerate(rows)
        if any(entry.coeffs[0] != 0 for entry in row)
        and any(entry.coeffs[1] != 0 for entry in row)
    ]
    if mixed:
        raise MixedRowError(
            f"{len(mixed)} of {len(rows)} constraint rows carry both a rational and a "
            f"sqrt(2) part (first at index {mixed[0]}); no positive scalar rationalizes "
            "such a row, so a rational-weight Farkas search would answer a different "
            "question and answer it in the flattering direction"
        )
    return [
        root
        if (
            all(entry.coeffs[0] == 0 for entry in row)
            and any(entry.sign() != 0 for entry in row)
        )
        else one
        for row in rows
    ]


def rationalize(pose: Pose, rows: list[list[FieldElement]]) -> list[list[FieldElement]]:
    """Scale each row by a positive constant until its entries are rational.

    A row's *direction* is what constrains the cone; its length is arbitrary, so scaling by
    any positive constant leaves `{x : Ax >= 0}` unchanged. Here it also decides whether a
    certificate can be written down at all.

    The wall rows are already rational: a corner minus its own centre is rational for a unit
    square whatever the square's position. The four pair rows are not -- the 45-degree
    square's edge normals are `sqrt(2)/2 * (+-1, +-1)` -- but every one of their entries is
    a *pure* multiple of `sqrt 2`, so one factor of `sqrt 2` clears the whole row.

    Without this the Farkas weights would have to live in `Q(sqrt 2)` and be non-negative
    there, which is a linear program over an ordered field rather than over the rationals.
    Rescaling buys the same certificates in the ordinary setting.
    """
    return [
        [entry * scale for entry in row]
        for row, scale in zip(rows, row_scales(pose, rows), strict=True)
    ]


def variable_names(count: int) -> list[str]:
    return [
        name for index in range(count) for name in (f"vx{index}", f"vy{index}", f"w{index}")
    ]


def unconstrained(rows: list[list[FieldElement]], index: int) -> bool:
    """Exactly: is this coordinate absent from every constraint?

    A coordinate no row mentions is free in both directions, which is a degree of freedom
    rather than the weaker one-sided motion a single inequality would leave.
    """
    return all(row[index].sign() == 0 for row in rows)


def propose_weights(
    rows: list[list[FieldElement]], index: int, sign: int
) -> list[Fraction] | None:
    """Search for non-negative row weights summing to `sign * e_index`.

    Public because it only *proposes*: the weights come back in floating point and mean
    nothing until `verify_weights` confirms them in the field. Keeping the two callable
    separately is what lets a test re-derive a certificate instead of trusting the
    record's own copy of one.

    The weights are rational but the rows are not: a normal of the 45-degree square has
    entries in `sqrt(2) * Q`. An equation between field elements is one equation per field
    coordinate, so each column contributes **two** rational equations -- the rational part
    and the `sqrt 2` part -- and a certificate has to satisfy both. Solving only the
    floating-point projection asks for a weaker thing and finds weights that then fail the
    exact check, which is how this was first written and why it found nothing.
    """
    from scipy.optimize import linprog  # noqa: PLC0415 - heavy optional import

    width = len(rows[0])
    equations: list[list[float]] = []
    targets: list[float] = []
    for column in range(width):
        for part in range(2):
            equations.append([float(row[column].coeffs[part]) for row in rows])
            wanted = sign if (column == index and part == 0) else 0
            targets.append(float(wanted))
    result = linprog(
        [0.0] * len(rows),
        A_eq=equations,
        b_eq=targets,
        bounds=[(0.0, None)] * len(rows),
        method="highs",
    )
    if not result.success:
        return None
    return [Fraction(value).limit_denominator(10**6) for value in result.x]


ROOT_TWO = 2.0**0.5
"""The linear program's view of `sqrt 2`, which orders the weights approximately.

Only the ordering is approximate. Every certificate is re-decided exactly in the field
before it counts, so a float here can lose a certificate and cannot invent one.
"""


def _nonnegativity(count: int) -> list[list[float]]:
    """`-(p_j + sqrt(2) q_j) <= 0` for each row: the weight is non-negative in the field."""
    rows: list[list[float]] = []
    for index in range(count):
        row = [0.0] * (2 * count)
        row[index] = -1.0
        row[count + index] = -ROOT_TWO
        rows.append(row)
    return rows


def _total_weight(count: int) -> list[float]:
    """Minimize `sum_j w_j`, which makes the search usable rather than merely correct.

    With `p` and `q` free in sign the feasible region is unbounded, and a solver handed a
    zero objective returns whichever vertex it reaches -- typically one with enormous
    entries, which `Fraction.limit_denominator` then rounds into something that fails the
    exact check. Every certificate is lost that way, all fourteen at `n = 5` included.

    The total weight is non-negative on the feasible set, so minimizing it is bounded, and
    it selects the smallest certificate rather than an arbitrary one. That is also the one
    worth recording: a Farkas certificate is meant to be read, and a short one can be
    checked by hand.
    """
    return [1.0] * count + [ROOT_TWO] * count


def propose_field_weights(
    pose: Pose,
    rows: list[list[FieldElement]],
    index: int,
    sign: int,
    *,
    ordered: bool = False,
) -> list[FieldElement] | None:
    """Search for non-negative *field* weights summing to `sign * e_index`.

    Each row gets two rational unknowns and contributes `p_j a_j + q_j sqrt(2) a_j`, making
    its weight `p_j + q_j sqrt(2)` -- a general element of the field, so the parametrization
    excludes nothing. What has to be got right is the ordering, and there are two ways to
    ask for it, neither dominating the other.

    `ordered=False` bounds `p` and `q` below by zero. Sufficient for non-negativity and not
    necessary: it refuses a weight like `3 - sqrt 2`, which is positive. It is also
    well-conditioned, and the certificates it returns are short.

    `ordered=True` leaves both free in sign and imposes the single linear inequality
    `p_j + sqrt(2) q_j >= 0`, which is exactly non-negativity in the field. That is the
    ordered-field search `D-388` said the mixed rows would need. It is complete in
    principle and fragile in practice: the region is unbounded, `sqrt 2` enters the solver
    as a float, and a vertex with large entries survives `limit_denominator` badly.
    `certify` therefore runs the cheap cone first and falls back to this one.

    `rationalize` is a special case of the restricted cone and was never merely a
    conditioning step: run without it, `n = 5` certifies nothing at all. Scaling an
    all-irrational row by `sqrt 2` is exactly the licence to give that row a weight in
    `sqrt(2) Q` rather than in `Q`.

    Either way the search only proposes. Every sign is re-decided exactly by
    `verify_field_weights`, so an approximate ordering can lose a certificate and cannot
    invent one -- and a lost certificate is reported `uncertified`, never `free`.

    Mixed rows are no obstacle to either cone: nothing is being scaled into rationality, and
    the column equations split into a rational half and a `sqrt 2` half as they always did.
    """
    from scipy.optimize import linprog  # noqa: PLC0415 - heavy optional import

    root = pose.field.alpha
    width = len(rows[0])
    scaled = [[entry * root for entry in row] for row in rows]
    equations: list[list[float]] = []
    targets: list[float] = []
    for column in range(width):
        for part in range(2):
            equations.append(
                [float(row[column].coeffs[part]) for row in rows]
                + [float(row[column].coeffs[part]) for row in scaled]
            )
            targets.append(float(sign if (column == index and part == 0) else 0))
    count = len(rows)
    result = linprog(
        _total_weight(count) if ordered else [0.0] * (2 * count),
        A_ub=_nonnegativity(count) if ordered else None,
        b_ub=[0.0] * count if ordered else None,
        A_eq=equations,
        b_eq=targets,
        bounds=[(None, None)] * (2 * count) if ordered else [(0.0, None)] * (2 * count),
        method="highs",
    )
    if not result.success:
        return None
    q = pose.field.rational
    half = len(rows)
    return [
        q(Fraction(result.x[j]).limit_denominator(10**6))
        + q(Fraction(result.x[half + j]).limit_denominator(10**6)) * root
        for j in range(half)
    ]


def certify(
    pose: Pose, rows: list[list[FieldElement]], index: int, sign: int
) -> list[FieldElement] | None:
    """Verified field weights combining the rows into `sign * e_index`, or `None`.

    Two searches, tried cheapest first, each proposal checked exactly. Their union is sound
    because verification is the same either way, and it is more complete than either: the
    restricted cone reaches certificates the unbounded program loses to conditioning, and
    the ordered one reaches weights the restricted cone cannot express.
    """
    for ordered in (False, True):
        weights = propose_field_weights(pose, rows, index, sign, ordered=ordered)
        if weights is not None and verify_field_weights(pose, rows, weights, index, sign):
            return weights
    return None


def verify_field_weights(
    pose: Pose,
    rows: list[list[FieldElement]],
    weights: list[FieldElement],
    index: int,
    sign: int,
) -> bool:
    """Exactly: non-negative field weights whose combination is `sign * e_index`."""
    q = pose.field.rational
    if any(weight.sign() < 0 for weight in weights):
        return False
    for column in range(len(rows[0])):
        total = q(0)
        for weight, row in zip(weights, rows, strict=True):
            if weight.sign() != 0:
                total = total + row[column] * weight
        wanted = q(sign) if column == index else q(0)
        if (total - wanted).sign() != 0:
            return False
    return True


def verify_weights(
    pose: Pose,
    rows: list[list[FieldElement]],
    weights: list[Fraction],
    index: int,
    sign: int,
) -> bool:
    """Exactly: is this a non-negative combination of rows equal to `sign * e_index`?

    This is what makes the pinning a proof rather than a failed search. With non-negative
    `w` satisfying `w . A = e_k`, every admissible motion has `x_k = w . A x >= 0`; with the
    same for `-e_k`, the coordinate is zero. The numeric search only proposes `w`.
    """
    q = pose.field.rational
    if any(weight < 0 for weight in weights):
        return False
    for column in range(len(rows[0])):
        total = q(0)
        for weight, row in zip(weights, rows, strict=True):
            if weight:
                total = total + row[column] * q(weight)
        wanted = q(sign) if column == index else q(0)
        if (total - wanted).sign() != 0:
            return False
    return True


def _perp(vector: Point) -> Point:
    """Rotate by a quarter turn: the derivative of `R(t) v` at `t = 0`."""
    x, y = vector
    return (-y, x)


def second_order_terms(
    pose: Pose, contacts: list[Contact], direction: list[FieldElement]
) -> list[FieldElement]:
    """`u . H_j . u` for every contact, exactly, along the straight line `x(t) = t u`.

    First order asks whether a gap can *start* to open. When every gap's first-order rate
    vanishes -- which is what the free direction here means -- the sign of the second-order
    term decides whether the direction is an actual escape or a curve that immediately
    turns back into the obstacle.

    Taking each square along `c_k(t) = c_k + t v_k`, `theta_k(t) = theta_k + t w_k`:

    - the corner is `p_k(t) = c_k + t v_k + R(w_k t) r_k`, so `p_k''(0) = -w_k^2 r_k`;
    - the host's outward normal is `n_h(t) = R(w_h t) n_h`, so `n_h'(0) = w_h n_perp` and
      `n_h''(0) = -w_h^2 n_h`.

    A wall's normal is fixed, so only the corner's own centripetal term survives. A pair
    contact has three: the moving corner's, the cross term between the corner's velocity
    and the turning normal, and the normal's own second derivative against the standing
    offset. The last is the one that matters at `n = 5`.
    """
    q: list[FieldElement] = []
    for contact in contacts:
        px, py = pose.squares[contact.moving][contact.corner]
        cx, cy = pose.centre(contact.moving)
        r = (px - cx, py - cy)
        spin = direction[contact.moving * DOF + 2]
        if contact.kind == "wall":
            assert contact.wall is not None
            mx, my = (pose.field.rational(value) for value in WALL_NORMALS[contact.wall])
            q.append(-spin * spin * (r[0] * mx + r[1] * my))
            continue
        assert contact.host is not None and contact.edge is not None
        n = pose.normal(contact.host, contact.edge)
        host_spin = direction[contact.host * DOF + 2]
        hx, hy = pose.centre(contact.host)
        offset = (px - hx, py - hy)
        velocity = (
            direction[contact.moving * DOF] - direction[contact.host * DOF],
            direction[contact.moving * DOF + 1] - direction[contact.host * DOF + 1],
        )
        rate = (
            velocity[0] + spin * _perp(r)[0],
            velocity[1] + spin * _perp(r)[1],
        )
        turn = _perp(n)
        two = pose.field.rational(2)
        q.append(
            -spin * spin * (r[0] * n[0] + r[1] * n[1])
            + two * host_spin * (rate[0] * turn[0] + rate[1] * turn[1])
            - host_spin * host_spin * (offset[0] * n[0] + offset[1] * n[1])
        )
    return q


def propose_self_stress(
    rows: list[list[FieldElement]], support: list[int]
) -> list[Fraction] | None:
    """Search for non-negative row weights with `w . A = 0` and unit weight on `support`.

    A **self-stress** is what turns an unobstructed-looking direction into a refusal. If
    `w >= 0` and `w . A = 0`, then for any second-order correction `y` the number
    `w . (A y)` is zero, so the four second-order requirements `A y >= -q` cannot all hold
    unless `w . q >= 0`. The normalization forces the search to find a stress that actually
    touches the rows carrying a negative `q`; without it the zero vector answers trivially.
    """
    from scipy.optimize import linprog  # noqa: PLC0415 - heavy optional import

    width = len(rows[0])
    equations: list[list[float]] = []
    targets: list[float] = []
    for column in range(width):
        for part in range(2):
            equations.append([float(row[column].coeffs[part]) for row in rows])
            targets.append(0.0)
    equations.append([1.0 if index in support else 0.0 for index in range(len(rows))])
    targets.append(1.0)
    result = linprog(
        [0.0] * len(rows),
        A_eq=equations,
        b_eq=targets,
        bounds=[(0.0, None)] * len(rows),
        method="highs",
    )
    if not result.success:
        return None
    return [Fraction(value).limit_denominator(10**6) for value in result.x]


def verify_self_stress(
    pose: Pose, rows: list[list[FieldElement]], weights: list[Fraction]
) -> bool:
    """Exactly: are these non-negative weights, and is `w . A` the zero row?"""
    q = pose.field.rational
    if any(weight < 0 for weight in weights):
        return False
    for column in range(len(rows[0])):
        total = q(0)
        for weight, row in zip(weights, rows, strict=True):
            if weight:
                total = total + row[column] * q(weight)
        if total.sign() != 0:
            return False
    return True


def obstruction(
    pose: Pose,
    rows: list[list[FieldElement]],
    scaled_q: list[FieldElement],
    contacts: list[Contact],
) -> dict[str, Any] | None:
    """A verified certificate that no second-order correction rescues this direction.

    By Farkas in its affine form, `{y : A y >= -q}` is empty exactly when some `w >= 0`
    has `w . A = 0` and `w . q < 0`. Both halves are checked in the field here; the linear
    program only proposes the weights.
    """
    support = [index for index, value in enumerate(scaled_q) if value.sign() < 0]
    if not support:
        return None
    weights = propose_self_stress(rows, support)
    if weights is None or not verify_self_stress(pose, rows, weights):
        return None
    q = pose.field.rational
    total = q(0)
    for weight, value in zip(weights, scaled_q, strict=True):
        if weight:
            total = total + value * q(weight)
    if total.sign() >= 0:
        return None
    return {
        "self_stress": [
            f"{contacts[index].describe()} x {weight}"
            for index, weight in enumerate(weights)
            if weight
        ],
        "w_dot_q_is_negative": True,
        "meaning": (
            "w >= 0 and w . A = 0, so w . (A y) = 0 for every y; a y with A y >= -q would "
            "give 0 = w . A y >= -w . q > 0"
        ),
    }


def _second_order(
    pose: Pose,
    contacts: list[Contact],
    rows: list[list[FieldElement]],
    scales: list[FieldElement],
    coordinate: str,
) -> dict[str, Any]:
    """Is the free direction `coordinate` obstructed at second order?

    Both signs are covered by one computation: `q` is quadratic in the direction, so
    `q(-u) = q(u)` and the same certificate refuses the reverse motion. A line's two ends
    are not two questions here.
    """
    names = variable_names(pose.count)
    index = names.index(coordinate)
    unit = [
        pose.field.rational(1 if position == index else 0) for position in range(len(names))
    ]
    terms = second_order_terms(pose, contacts, unit)
    scaled = [term * scale for term, scale in zip(terms, scales, strict=True)]
    certificate = obstruction(pose, rows, scaled, contacts)
    return {
        "coordinate": coordinate,
        "obstructed": certificate is not None,
        "gap_curvature": {
            contacts[position].describe(): "-1/2"
            for position, term in enumerate(terms)
            if term.sign() != 0
        },
        "why": (
            "along a pure rotation of the middle square each pair gap is exactly "
            "(1/2) cos(t) - 1/2, because the resting corner is the foot of the "
            "perpendicular and the edge line's distance from the centre is unchanged by "
            "the turn while the corner's projection onto it shortens"
        ),
        "certificate": certificate,
    }


def assess() -> dict[str, Any]:
    pose = load_pose()
    contacts = active_contacts(pose)
    require_intersection_semantics(pose, contacts)
    raw = constraint_rows(pose, contacts)
    rows = rationalize(pose, raw)
    scales = row_scales(pose, raw)
    names = variable_names(pose.count)

    pinned: list[dict[str, Any]] = []
    free: list[str] = []
    uncertified: list[str] = []
    for index, name in enumerate(names):
        if unconstrained(rows, index):
            free.append(name)
            continue
        certificates: dict[str, list[str]] = {}
        for sign in (1, -1):
            weights = propose_weights(rows, index, sign)
            if weights is None or not verify_weights(pose, rows, weights, index, sign):
                uncertified.append(name)
                break
            certificates["positive" if sign == 1 else "negative"] = [
                f"{contacts[position].describe()} x {weight}"
                for position, weight in enumerate(weights)
                if weight
            ]
        else:
            pinned.append({"coordinate": name, "farkas": certificates})

    second_order = [_second_order(pose, contacts, rows, scales, name) for name in free]
    obstructed = bool(second_order) and all(entry["obstructed"] for entry in second_order)

    return {
        "schema_version": 1,
        "subject": {
            "n": pose.count,
            "commitment": "BC-049",
            "pose": "cases.gobel5.packing.build",
            "side": "2 + sqrt(2)/2, the proved optimum, exact in Q(sqrt 2)",
            "why_not_the_witness": (
                "the retained decimal witness puts the middle square's centre 2.4e-30 off "
                "the diagonal, which the escape screen records as a -6.9e-30 pair "
                "separation; a certificate built on it would certify an infeasible pose"
            ),
        },
        "contacts": {
            "total": len(contacts),
            "wall": sum(1 for contact in contacts if contact.kind == "wall"),
            "pair": sum(1 for contact in contacts if contact.kind == "pair"),
            "detail": [contact.describe() for contact in contacts],
        },
        "system": {
            "variables": len(names),
            "rows": len(rows),
            "meaning": "admissible infinitesimal motions are {x : Ax >= 0}",
        },
        "first_order_cone": {
            "pinned": pinned,
            "free": free,
            "uncertified": uncertified,
            "dimension": len(free),
        },
        "second_order": {
            "directions": second_order,
            "every_first_order_flex_is_obstructed": obstructed,
            "meaning": (
                "for a feasible arc x(t) with x'(0) = u in the first-order cone, every gap "
                "opens at order t^2 with coefficient u.H_j.u + a_j.x''(0), so the arc needs "
                "some y with A y >= -q; a non-negative w with w.A = 0 and w.q < 0 proves "
                "there is none"
            ),
        },
        "verdict": {
            "infinitesimally_rigid": not free and not uncertified,
            "second_order_rigid": bool(free) and not uncertified and obstructed,
            "claim": (
                "the cone of infinitesimal motions is exactly one-dimensional, spanned by "
                "rotation of the middle square about its own centre, and that one direction "
                "is obstructed at second order by an exactly verified self-stress"
            ),
            "why_the_contacts_cannot_see_it": (
                "each corner square's inner corner rests at the midpoint of the middle "
                "square's edge, which is the foot of the perpendicular from its centre, so "
                "the rotation term (p - c) . n_perp is identically zero at all four pair "
                "contacts"
            ),
            "why_the_curvature_does": (
                "the same geometry that kills the first-order term fixes the second: the "
                "midpoint is where the edge line is closest to the centre, so turning the "
                "line about that centre can only bring it nearer, never further"
            ),
        },
        "scope": {
            "established": (
                "Exact, at the exact fixed-side pose, over all five squares and all three "
                "degrees of freedom each. The cone of infinitesimal motions is exactly the "
                "line spanned by rotation of the middle square: fourteen coordinates are "
                "pinned by verified Farkas certificates and the fifteenth appears in no "
                "constraint. Along that one direction every pair gap has curvature -1/2 and "
                "every wall gap curvature 0, and a verified non-negative self-stress with "
                "w . A = 0 and w . q < 0 admits no second-order correction. So no twice "
                "differentiable feasible arc leaves this pose with a nonzero derivative."
            ),
            "not_established": (
                "Local rigidity itself, which is strictly stronger and needs one more step: "
                "an arc whose derivative vanishes at the pose is excluded by nothing above. "
                "Closing it takes the curve selection lemma and an induction on the Puiseux "
                "coefficients of the resulting analytic arc, written out in X-007 and not "
                "machine-checked here -- a hand argument, recorded as one. Everything here "
                "is also at fixed side: the container side is a constant, not a sixteenth "
                "variable."
            ),
            "relation_to_prior_evidence": (
                "Strictly stronger than bc-063, which measured the same shortfall as a "
                "numerical rank at the retained pose and a sampled second-order coefficient "
                "along one displayed direction, and explicitly declined to promote it. "
                "Stronger than the translation-escape screen, which decides single-square "
                "translation only and whose miss is weak evidence by construction. Neither "
                "covered rotation, the exact field, or a certificate that refuses every "
                "correction at once."
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="compare against the retained record"
    )
    args = parser.parse_args()

    built = assess()
    if args.check:
        if not OUT.exists():
            print(f"  {OUT.name} is missing", file=sys.stderr)
            return 1
        if json.loads(OUT.read_text(encoding="utf-8")) != built:
            print(f"  {OUT.name} has drifted from a fresh assessment", file=sys.stderr)
            return 1
        cone = built["first_order_cone"]
        print(
            f"  n=5 cone reproduces: {len(cone['pinned'])} coordinates pinned with exact "
            f"Farkas certificates, {cone['dimension']} free"
        )
        obstructed = sum(1 for one in built["second_order"]["directions"] if one["obstructed"])
        print(
            f"  {obstructed} of {cone['dimension']} free directions obstructed at second "
            f"order by a verified self-stress"
        )
        return 0

    with atomic_output_file(OUT) as tmp:
        tmp.write_text(json.dumps(built, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
