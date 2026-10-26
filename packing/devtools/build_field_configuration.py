"""Build an exact number-field configuration from a tight rational certificate's contacts.

A rational certificate of an upper bound, such as T-174's at 297, is a packing pushed a
hair off its stationary point: every contact is opened by a margin far below the binary64
spacing (1e-91 at 297), and every other pair and wall is separated by orders of magnitude
more. Its exact stationary side is algebraic, and an author who reports it (issue 804)
can be checked here without reading the author's files: this module recovers the contact
graph from the certificate, solves the contacts at high precision, identifies the number
field the configuration lies in, rebuilds every centre and rotation exactly in that field,
and hands the result to `sqpack.witness.exact_verify`, which decides it.

**The steps**, each a subcommand that writes its own receipt:

- ``contacts``: the contact graph. Every pair whose separating gap and every corner whose
  wall clearance is below `CONTACT_FLOOR` is a contact, every other one must clear
  `STRICT_FLOOR`, and anything between is refused as undecided rather than guessed. A
  contact is typed by the features on its separating line: a corner on an edge, an edge
  on an edge (which also puts both squares in one rotation class), or a corner on a
  corner. An edge flush with a wall puts its square's class at angle zero.
- ``solve``: the contacts as equations in the centres, the side and one half-angle
  tangent per rotation class; the Jacobian's rank, measured in binary64 by a pivoted QR,
  names the free unknowns, which are pinned to dyadic rationals on a grid of
  the rationals of least denominator within
  `PIN_TOLERANCE`; the rest are refined by Gauss-Newton steps whose residual is evaluated at
  the working precision and whose step is solved in binary64, so each step gains the
  digits the Jacobian's conditioning allows. It refuses unless the residual falls below
  the target.
- ``field``: the generator's minimal polynomial, by integer relation on the refined value
  of one class's tangent, judged by `sqpack.promote.solve`'s margin rule; every other
  class's tangent is then expressed in that field, or the step refuses.
- ``build``: the exact configuration. With every rotation in the field ``K``, the contact
  equations are linear in the centres and the side; they are solved at each of the
  field's embeddings in binary64-guided multiprecision, the power-basis coefficients are
  recovered through the Vandermonde system of the conjugates and rounded to rationals by
  continued fractions, and every contact equation is then checked as an identity in
  ``K``. Nothing is accepted on the numbers: an identity that does not hold exactly is a
  refusal.
- ``decide``: `sqpack.witness.exact_verify` over ``K`` on the built witness, with its
  duplicate-square and outside-container controls refused.

The module reads only rational ``center-basis`` Witness/v2 certificates. It decides
nothing about the bound by itself: the exact verifier does.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
import time
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any, cast

import mpmath as mp
import numpy as np
import scipy.linalg
import sympy

from sqpack.field import FieldElement, NumberField
from sqpack.witness import load_witness

#: A separating gap or wall clearance below this is a contact.
CONTACT_FLOOR = Fraction(1, 10**40)
#: Every gap that is not a contact must clear this, or the extraction refuses.
STRICT_FLOOR = Fraction(1, 10**14)
#: The largest centre distance at which two unit squares can touch, with slack.
TOUCH_REACH = 1.4143
#: The dyadic grid free unknowns are pinned to.
PIN_TOLERANCE = Fraction(1, 10**14)

CORNERS = ((1, 1), (-1, 1), (-1, -1), (1, -1))


class BuildError(ValueError):
    """A step that cannot decide refuses with a kind and a detail."""

    def __init__(self, kind: str, detail: str):
        super().__init__(f"{kind}: {detail}")
        self.kind = kind
        self.detail = detail


# --------------------------------------------------------------------------- reading


@dataclass(frozen=True)
class Certificate:
    """A rational centre-basis certificate: side and each square's centre and unit basis."""

    n: int
    side: Fraction
    poses: tuple[tuple[Fraction, Fraction, Fraction, Fraction], ...]


def read_certificate(path: Path) -> Certificate:
    """Read a rational center-basis Witness/v2, refusing any other kind."""
    document = load_witness(path)
    witness = document.get("witness", document)
    if witness.get("representation") != "center-basis":
        raise BuildError("unsupported", "only a center-basis witness is read")
    if witness.get("scalar", {}).get("kind") != "rational":
        raise BuildError("unsupported", "only a rational witness is read")
    poses = []
    for square in witness["squares"]:
        x, y = (Fraction(value) for value in square["center"])
        c, s = (Fraction(value) for value in square["basis"])
        if c * c + s * s != 1:
            raise BuildError(
                "malformed", f"square {square.get('id')} has a basis off the unit circle"
            )
        poses.append((x, y, c, s))
    if len(poses) != witness["n"]:
        raise BuildError("malformed", "the square count is not the witness's n")
    return Certificate(n=witness["n"], side=Fraction(witness["side"]), poses=tuple(poses))


# --------------------------------------------------------------------------- contacts


def pivoted_qr(matrix: np.ndarray) -> tuple[Any, np.ndarray, np.ndarray]:
    """The economic QR with column pivoting: ``(q, r, pivots)``."""
    q, r, pivots = cast(
        "tuple[Any, np.ndarray, np.ndarray]",
        scipy.linalg.qr(matrix, mode="economic", pivoting=True),
    )
    return q, r, pivots


def _text(value: Any, digits: int, **options: Any) -> str:
    return str(mp.nstr(value, digits, **options))


def mpf_of(value: Fraction) -> Any:
    """A rational as an mpf at the working precision."""
    return mp.mpf(value.numerator) / value.denominator


def _mpf(value: Fraction) -> Any:
    return mp.mpf(value.numerator) / value.denominator


def canonical_rotation(c: Any, s: Any) -> tuple[Any, Any]:
    """The square's basis turned by quarter turns into the half-open range (-45, 45] degrees."""
    for _ in range(4):
        if c > 0 and -c < s <= c:
            return c, s
        c, s = s, -c
    raise BuildError("malformed", "no quarter turn puts the basis in range")


@dataclass
class Contacts:
    """The contact graph and its typed equations."""

    pair_equations: list[tuple[int, str, int, int, int, int]] = field(default_factory=list)
    wall_equations: list[tuple[int, int, int, int, int]] = field(default_factory=list)
    corner_equations: list[tuple[int, int, int, int, int, int, int]] = field(
        default_factory=list
    )
    unions: list[tuple[int, int]] = field(default_factory=list)
    flush: list[int] = field(default_factory=list)
    kinds: dict[str, int] = field(default_factory=dict)
    largest_contact: Any = None
    smallest_strict: Any = None
    pairs_read: int = 0


def _corners(pose: tuple[Any, Any, Any, Any]) -> list[tuple[Any, Any]]:
    x, y, c, s = pose
    return [(x + (a * c - b * s) / 2, y + (a * s + b * c) / 2) for a, b in CORNERS]


def extract_contacts(cert: Certificate, *, digits: int = 120) -> tuple[Contacts, list]:
    """Type every contact of `cert`, refusing an undecided margin.

    Returns the contacts and each square's canonical pose at `digits`.
    """
    mp.mp.dps = digits
    floor = _mpf(CONTACT_FLOOR)
    strict = _mpf(STRICT_FLOOR)
    poses = []
    for x, y, c, s in cert.poses:
        cc, ss = canonical_rotation(_mpf(c), _mpf(s))
        poses.append((_mpf(x), _mpf(y), cc, ss))
    side = _mpf(cert.side)
    corners = [_corners(pose) for pose in poses]
    out = Contacts()

    def note(kind: str) -> None:
        out.kinds[kind] = out.kinds.get(kind, 0) + 1

    def strict_margin(value: Any) -> None:
        if value >= strict:
            if out.smallest_strict is None or value < out.smallest_strict:
                out.smallest_strict = value
        elif value > floor or value < -floor:
            raise BuildError(
                "undecided", f"a margin of {mp.nstr(value, 5)} is neither contact nor strict"
            )
        elif out.largest_contact is None or abs(value) > out.largest_contact:
            out.largest_contact = abs(value)

    for index in range(len(poses)):
        on_wall: dict[tuple[int, int], list[tuple[int, int]]] = {}
        for (a, b), (px, py) in zip(CORNERS, corners[index], strict=True):
            for axis, value in ((0, px), (1, py)):
                for at, clearance in ((0, value), (1, side - value)):
                    strict_margin(clearance)
                    if abs(clearance) < floor:
                        on_wall.setdefault((axis, at), []).append((a, b))
        for (axis, at), features in on_wall.items():
            a, b = features[0]
            out.wall_equations.append((index, a, b, axis, at))
            if len(features) == 2:
                out.flush.append(index)
                note("edge-wall")
            elif len(features) == 1:
                note("corner-wall")
            else:
                raise BuildError(
                    "malformed", f"square {index} has {len(features)} corners on a wall"
                )

    centres = [(float(p[0]), float(p[1])) for p in poses]
    for i in range(cert.n):
        for j in range(i + 1, cert.n):
            dx = centres[i][0] - centres[j][0]
            dy = centres[i][1] - centres[j][1]
            if dx * dx + dy * dy > TOUCH_REACH**2:
                continue
            out.pairs_read += 1
            _classify_pair(i, j, poses, corners, floor, strict_margin, out, note)
    return out, poses


def _touching_point(candidate, corners, floor) -> tuple[int, int] | None:
    """For two parallel edges on one line, the corners they share where they meet at a point.

    Returns the owner's and the other square's corner indices when the edges overlap in a
    single point (within `floor`), and None when they overlap along a segment.
    """
    owner, other, _selector, _sign, own_line, oth_line = candidate
    for k in own_line:
        for m in oth_line:
            (px, py), (qx, qy) = corners[owner][k], corners[other][m]
            if abs(px - qx) < floor and abs(py - qy) < floor:
                others_own = next(p for p in own_line if p != k)
                others_oth = next(p for p in oth_line if p != m)
                (ax, ay), (bx, by) = corners[owner][others_own], corners[other][others_oth]
                # The far ends lie on opposite sides of the shared point: no overlap.
                if (ax - px) * (bx - px) + (ay - py) * (by - py) < 0:
                    return k, m
    return None


def _classify_pair(i, j, poses, corners, floor, strict_margin, out, note) -> None:  # noqa: PLR0917
    """Type one pair: separated, or a contact with its equations."""
    candidates = []
    best = None
    for owner, other in ((i, j), (j, i)):
        _, _, c, s = poses[owner]
        for selector, (wx, wy) in (("u", (c, s)), ("v", (-s, c))):
            for sign in (1, -1):
                nx, ny = sign * wx, sign * wy
                own = [px * nx + py * ny for px, py in corners[owner]]
                oth = [px * nx + py * ny for px, py in corners[other]]
                gap = min(oth) - max(own)
                best = gap if best is None or gap > best else best
                if abs(gap) < floor:
                    top = max(own)
                    low = min(oth)
                    own_line = [k for k, value in enumerate(own) if value - top > -floor]
                    oth_line = [k for k, value in enumerate(oth) if value - low < floor]
                    candidates.append((owner, other, selector, sign, own_line, oth_line))
    strict_margin(best)
    if not candidates:
        return
    edge = [cand for cand in candidates if len(cand[4]) == 2]
    if edge and len(edge[0][5]) == 2 and _touching_point(edge[0], corners, floor):
        # Two parallel edges that share one end point only: a corner on a corner.
        owner, other, _selector, _sign, own_line, oth_line = edge[0]
        touching = _touching_point(edge[0], corners, floor)
        assert touching is not None  # the branch's condition
        own_corner, oth_corner = touching
        a, b = CORNERS[own_corner]
        a2, b2 = CORNERS[oth_corner]
        out.unions.append((owner, other))
        for axis in (0, 1):
            out.corner_equations.append((owner, a, b, other, a2, b2, axis))
        note("corner-corner")
        return
    if edge:
        owner, other, selector, sign, _own_line, oth_line = edge[0]
        a, b = CORNERS[oth_line[0]]
        out.pair_equations.append(
            (owner, selector + ("+" if sign > 0 else "-"), other, a, b, 0)
        )
        if len(oth_line) == 2:
            out.unions.append((owner, other))
            note("edge-edge")
        else:
            note("corner-edge")
        return
    owner, other, _selector, _sign, own_line, oth_line = candidates[0]
    if len(own_line) != 1 or len(oth_line) != 1:
        raise BuildError("malformed", f"pair {i},{j} touches on an unrecognised feature")
    a, b = CORNERS[own_line[0]]
    a2, b2 = CORNERS[oth_line[0]]
    for axis in (0, 1):
        out.corner_equations.append((owner, a, b, other, a2, b2, axis))
    note("corner-corner")


# --------------------------------------------------------------------------- classes


class Classes:
    """Rotation classes: squares joined by edge-edge contacts, and the class held at zero."""

    AXIS = -1

    def __init__(self, n: int, contacts: Contacts):
        parent = list(range(n))

        def find(k: int) -> int:
            while parent[k] != k:
                parent[k] = parent[parent[k]]
                k = parent[k]
            return k

        for left, right in contacts.unions:
            parent[find(left)] = find(right)
        roots = sorted({find(k) for k in range(n)})
        flush_roots = {find(k) for k in contacts.flush}
        index = {}
        for root in roots:
            if root not in flush_roots:
                index[root] = len(index)
        self.of = [self.AXIS if find(k) in flush_roots else index[find(k)] for k in range(n)]
        self.count = len(index)
        self.members = [[k for k in range(n) if self.of[k] == cls] for cls in range(self.count)]


# --------------------------------------------------------------------------- the system


@dataclass
class System:
    """The contact equations over centres, side and one tangent per class."""

    n: int
    contacts: Contacts
    classes: Classes

    @property
    def unknowns(self) -> int:
        return 2 * self.n + 1 + self.classes.count

    def names(self) -> list[str]:
        names = []
        for k in range(self.n):
            names += [f"x{k + 1}", f"y{k + 1}"]
        names.append("S")
        names += [f"t[{cls}]" for cls in range(self.classes.count)]
        return names

    @property
    def equation_count(self) -> int:
        c = self.contacts
        return len(c.pair_equations) + len(c.wall_equations) + len(c.corner_equations)


def _rotation(t: Any, one: Any) -> tuple[Any, Any]:
    denominator = one + t * t
    return (one - t * t) / denominator, 2 * t / denominator


def rotations(system: System, values: list, one: Any = 1) -> list[tuple[Any, Any]]:
    """Each square's (cos, sin) from its class's tangent; the axis class is exact (1, 0)."""
    zero = one * 0
    by_class = [
        _rotation(values[2 * system.n + 1 + cls], one) for cls in range(system.classes.count)
    ]
    return [(one, zero) if cls == Classes.AXIS else by_class[cls] for cls in system.classes.of]


def _normal(rotation: tuple[Any, Any], selector: str) -> tuple[Any, Any]:
    c, s = rotation
    nx, ny = (c, s) if selector[0] == "u" else (-s, c)
    return (nx, ny) if selector[1] == "+" else (-nx, -ny)


def residuals(system: System, values: list, one: Any = 1) -> list:
    """Every contact equation's value at `values` (centres, side, tangents), in their ring."""
    n = system.n
    rot = rotations(system, values, one)
    half = one / 2
    side = values[2 * n]
    out = []
    for owner, selector, other, a, b, _ in system.contacts.pair_equations:
        nx, ny = _normal(rot[owner], selector)
        c, s = rot[other]
        dx = values[2 * other] - values[2 * owner] + (a * c - b * s) * half
        dy = values[2 * other + 1] - values[2 * owner + 1] + (a * s + b * c) * half
        out.append(nx * dx + ny * dy - half)
    for square, a, b, axis, at in system.contacts.wall_equations:
        c, s = rot[square]
        offset = (a * c - b * s) if axis == 0 else (a * s + b * c)
        value = values[2 * square + axis] + offset * half
        out.append(value - side if at else value)
    for first, a, b, second, a2, b2, axis in system.contacts.corner_equations:
        c, s = rot[first]
        c2, s2 = rot[second]
        p = (
            values[2 * first + axis]
            + ((a * c - b * s) if axis == 0 else (a * s + b * c)) * half
        )
        q = (
            values[2 * second + axis]
            + ((a2 * c2 - b2 * s2) if axis == 0 else (a2 * s2 + b2 * c2)) * half
        )
        out.append(p - q)
    return out


def entries(system: System, values: list, one: Any = 1.0) -> list[tuple[int, int, Any]]:
    """The Jacobian of `residuals` as (row, column, value) triples, analytic, in its ring.

    A class's tangent ``t`` turns its squares by ``theta = 2 atan t``, so a derivative in
    ``theta`` is carried to ``t`` by ``d theta / d t = 2 / (1 + t^2)``.
    """
    n = system.n
    base = 2 * n + 1
    rot = rotations(system, values, one)
    half = one / 2
    cls_of = system.classes.of
    dtheta = [
        2 * one / (one + values[base + k] * values[base + k])
        for k in range(system.classes.count)
    ]
    out: list[tuple[int, int, Any]] = []
    row = 0
    for owner, selector, other, a, b, _ in system.contacts.pair_equations:
        nx, ny = _normal(rot[owner], selector)
        c, s = rot[other]
        out += [
            (row, 2 * other, nx),
            (row, 2 * other + 1, ny),
            (row, 2 * owner, -nx),
            (row, 2 * owner + 1, -ny),
        ]
        dx = values[2 * other] - values[2 * owner] + (a * c - b * s) * half
        dy = values[2 * other + 1] - values[2 * owner + 1] + (a * s + b * c) * half
        if cls_of[owner] != Classes.AXIS:
            # d n / d theta: u turns to v and v to -u.
            mx, my = (-ny, nx)
            out.append((row, base + cls_of[owner], (mx * dx + my * dy) * dtheta[cls_of[owner]]))
        if cls_of[other] != Classes.AXIS:
            ox, oy = (-a * s - b * c) * half, (a * c - b * s) * half
            out.append((row, base + cls_of[other], (nx * ox + ny * oy) * dtheta[cls_of[other]]))
        row += 1
    for square, a, b, axis, at in system.contacts.wall_equations:
        out.append((row, 2 * square + axis, one))
        if at:
            out.append((row, 2 * n, -one))
        if cls_of[square] != Classes.AXIS:
            c, s = rot[square]
            turn = (-a * s - b * c) if axis == 0 else (a * c - b * s)
            out.append((row, base + cls_of[square], turn * half * dtheta[cls_of[square]]))
        row += 1
    for first, a, b, second, a2, b2, axis in system.contacts.corner_equations:
        for square, sa, sb, sign in ((first, a, b, 1), (second, a2, b2, -1)):
            out.append((row, 2 * square + axis, sign * one))
            if cls_of[square] != Classes.AXIS:
                c, s = rot[square]
                turn = (-sa * s - sb * c) if axis == 0 else (sa * c - sb * s)
                out.append(
                    (row, base + cls_of[square], sign * turn * half * dtheta[cls_of[square]])
                )
        row += 1
    return out


def jacobian(system: System, values: list[float]) -> np.ndarray:
    """The binary64 Jacobian of `residuals`, dense."""
    matrix = np.zeros((system.equation_count, system.unknowns))
    for row, column, value in entries(system, [float(v) for v in values], 1.0):
        matrix[row, column] += float(value)
    return matrix


def initial_values(system: System, poses: list) -> list:
    """Centres, side and class tangents read from the certificate's canonical poses."""
    values: list[Any] = []
    for x, y, _, _ in poses:
        values += [x, y]
    values.append(None)
    for members in system.classes.members:
        c, s = poses[members[0]][2], poses[members[0]][3]
        values.append(s / (1 + c))
    return values


@dataclass
class Structure:
    rank: int
    free: list[int]
    singular_gap: tuple[float, float]


def structure(system: System, values: list[float]) -> Structure:
    """The Jacobian's numerical rank and the free unknowns a pivoted QR leaves last."""
    matrix = jacobian(system, values)
    _, r, pivots = pivoted_qr(matrix)
    diagonal = np.abs(np.diag(r))
    scale = diagonal[0]
    rank = int(np.sum(diagonal > scale * 1e-10))
    above = float(diagonal[rank - 1] / scale)
    below = float(diagonal[rank] / scale) if rank < len(diagonal) else 0.0
    free = sorted(int(k) for k in pivots[rank:])
    return Structure(rank=rank, free=free, singular_gap=(above, below))


def pin(value: Any) -> Fraction:
    """A free unknown's pinned value: the rational of least denominator within `PIN_TOLERANCE`.

    Small denominators keep the field coefficients of every coordinate the pin reaches
    small, and a move below the tolerance is three decades under the certificate's
    least strict margin.
    """
    exact = Fraction(_text(value, 60, strip_zeros=False))
    bound = 1
    while True:
        candidate = exact.limit_denominator(bound)
        if abs(candidate - exact) < PIN_TOLERANCE:
            return candidate
        bound *= 10


def refine(
    system: System,
    start: list,
    free: list[int],
    pinned: dict[int, Fraction],
    *,
    digits: int,
    max_steps: int = 400,
    log=print,
) -> tuple[list, Any, int]:
    """Gauss-Newton to `digits`: residual at full precision, step solved in binary64."""
    mp.mp.dps = digits + 20
    values = [mp.mpf(v) if not isinstance(v, Fraction) else _mpf(v) for v in start]
    for k, value in pinned.items():
        values[k] = _mpf(value)
    keep = [k for k in range(system.unknowns) if k not in set(free)]
    matrix = jacobian(system, [float(v) for v in values])[:, keep]
    q, r = np.linalg.qr(matrix)
    target = mp.mpf(10) ** (-digits)
    residual = None
    for step in range(max_steps):
        res = residuals(system, values, mp.mpf(1))
        residual = max(abs(v) for v in res)
        if residual < target:
            return values, residual, step
        scale = residual
        rhs = np.array([float(v / scale) for v in res])
        delta = scipy.linalg.solve_triangular(r, q.T @ rhs)
        for k, d in zip(keep, delta, strict=True):
            values[k] -= mp.mpf(float(d)) * scale
        if step % 10 == 0:
            log(f"  step {step}: residual {mp.nstr(residual, 3)}")
    raise BuildError(
        "no-convergence", f"residual {mp.nstr(residual, 3)} after {max_steps} steps"
    )


def tangents_first(system: System, pivots: np.ndarray) -> list[int]:
    """Pin preference: class tangents, then the other columns from the QR's last pivot back.

    A free direction that turns a square is pinned at its tangent, so the square's
    rotation is rational and its position follows linearly in the field; pinning a
    coordinate instead leaves the angle to a quadratic over the field, in general outside it.
    """
    base = 2 * system.n + 1
    tangents = list(range(base, base + system.classes.count))
    rest = [int(k) for k in reversed(pivots) if int(k) not in set(tangents)]
    return tangents + rest


def choose_pins(matrix: np.ndarray, rank: int, *, preference: list[int]) -> list[int]:
    """Columns to pin, taken in `preference` order, whose removal keeps `matrix`'s rank.

    The pinned set is valid when its rows of the null space are independent, which is
    decided one candidate at a time on the null space's small matrix.
    """
    _, _singular, vt = np.linalg.svd(matrix, full_matrices=True)
    null = vt[rank:].T
    dimension = null.shape[1]
    if dimension == 0:
        return []
    chosen: list[int] = []
    for column in preference:
        trial = null[[*chosen, column]]
        if np.linalg.matrix_rank(trial, tol=1e-8) == len(chosen) + 1:
            chosen.append(column)
            if len(chosen) == dimension:
                return sorted(chosen)
    raise BuildError("degenerate", f"only {len(chosen)} of {dimension} free directions pinned")


@dataclass
class Stationary:
    """A refined stationary point: values, multipliers and what was pinned."""

    values: list
    multipliers: list
    rows: list[int]
    pinned: dict[int, Fraction]
    residual: Any
    steps: int
    kkt_rank: int
    kkt_shape: tuple[int, int]


def _stationarity(system: System, values: list, rows: list[int], multipliers: list, one: Any):
    """``J_R(z)^T lambda - e_S``: the side's gradient against the contacts' row space."""
    position = {row: k for k, row in enumerate(rows)}
    out = [one * 0] * system.unknowns
    for row, column, value in entries(system, values, one):
        k = position.get(row)
        if k is not None:
            out[column] += value * multipliers[k]
    out[2 * system.n] -= one
    return out


def stationary_refine(
    system: System, start: list, *, digits: int, max_steps: int = 2000, log=print
) -> Stationary:
    """Refine to a stationary point of the side on the contact set (the KKT system).

    The contacts alone leave a manifold of configurations, and on it the side moves at
    second order along some free directions; the reported side is its stationary value.
    The unknowns are the configuration and one multiplier per independent contact row
    (chosen by a pivoted QR of the binary64 Jacobian, since the contact rows are
    dependent and their multipliers otherwise not unique); the equations are the contacts
    and ``J_R^T lambda = e_S``. The KKT Jacobian is built once in binary64, its
    second-order block by complex steps, and the directions it leaves free -- along which
    the side is constant -- are pinned by `pin`. Each step's residual is evaluated
    at the working precision.
    """
    n_unknowns = system.unknowns
    z0 = [float(v) for v in start]
    contact = jacobian(system, z0)
    m = contact.shape[0]
    _, r_t, pivots = pivoted_qr(contact.T)
    diagonal = np.abs(np.diag(r_t))
    rank = int(np.sum(diagonal > diagonal[0] * 1e-10))
    rows = sorted(int(k) for k in pivots[:rank])
    e_side = np.zeros(n_unknowns)
    e_side[2 * system.n] = 1.0
    lam0, *_ = np.linalg.lstsq(contact[rows].T, e_side, rcond=None)
    kkt = np.zeros((m + n_unknowns, n_unknowns + rank))
    kkt[:m, :n_unknowns] = contact
    kkt[m:, n_unknowns:] = contact[rows].T
    step = 1e-30
    for column in range(n_unknowns):
        probe = [complex(v) for v in z0]
        probe[column] += 1j * step
        gradient = _stationarity(system, probe, rows, list(lam0), 1.0 + 0j)
        kkt[m:, column] = np.array([g.imag / step for g in gradient])
    _, r_k, pivots_k = pivoted_qr(kkt)
    diagonal = np.abs(np.diag(r_k))
    kkt_rank = int(np.sum(diagonal > diagonal[0] * 1e-10))
    free = choose_pins(kkt, kkt_rank, preference=tangents_first(system, pivots_k))
    if any(k >= n_unknowns for k in free):
        raise BuildError("degenerate", "the stationarity system leaves a multiplier free")
    mp.mp.dps = digits + 20
    values = [_mpf(v) if isinstance(v, Fraction) else mp.mpf(v) for v in start]
    pinned = {k: pin(values[k]) for k in free}
    for k, value in pinned.items():
        values[k] = _mpf(value)
    multipliers = [mp.mpf(float(v)) for v in lam0]
    keep = [k for k in range(n_unknowns + rank) if k not in set(free)]
    q, r = np.linalg.qr(kkt[:, keep])
    target = mp.mpf(10) ** (-digits)
    one = mp.mpf(1)
    residual = None
    for iteration in range(max_steps):
        res = residuals(system, values, one) + _stationarity(
            system, values, rows, multipliers, one
        )
        residual = max(abs(v) for v in res)
        if residual < target:
            return Stationary(
                values, multipliers, rows, pinned, residual, iteration, kkt_rank, kkt.shape
            )
        scale = residual
        delta = scipy.linalg.solve_triangular(
            r, q.T @ np.array([float(v / scale) for v in res])
        )
        for k, d in zip(keep, delta, strict=True):
            if k < n_unknowns:
                values[k] -= mp.mpf(float(d)) * scale
            else:
                multipliers[k - n_unknowns] -= mp.mpf(float(d)) * scale
        if iteration % 25 == 0:
            log(f"  step {iteration}: residual {mp.nstr(residual, 3)}")
    raise BuildError(
        "no-convergence", f"residual {mp.nstr(residual, 3)} after {max_steps} steps"
    )


# --------------------------------------------------------------------------- building


def field_of(field_receipt: dict[str, Any], generator: Any, digits: int) -> NumberField:
    """``K = Q(g)``: the generator's relation, with an isolating interval about ``g``."""
    poly = [int(c) for c in field_receipt["generator_relation"]["high_to_low"]]
    radius = mp.mpf(10) ** (RELATION_GUARD - digits)
    low = Fraction(_text(generator - radius, digits, strip_zeros=False))
    high = Fraction(_text(generator + radius, digits, strip_zeros=False))
    return NumberField(poly, (low, high))


def class_tangents(
    system: System, field_receipt: dict[str, Any], field_: NumberField
) -> list[FieldElement]:
    """Every class's half-angle tangent in ``K``, from the field step's receipt."""
    alpha = field_.alpha
    out = []
    for cls in range(system.classes.count):
        entry = field_receipt["classes"][f"t[{cls}]"]
        kind = entry["kind"]
        if kind == "generator":
            out.append(alpha)
        elif kind == "minus generator":
            out.append(-alpha)
        elif kind == "pinned":
            out.append(field_.rational(Fraction(entry["value"])))
        elif kind == "in field":
            relation_ = [int(c) for c in entry["relation"]]
            power = field_.one
            total = field_.zero
            for c in relation_[1:]:
                total = total + power * c
                power = power * alpha
            out.append(total * Fraction(-1, relation_[0]))
        else:
            raise BuildError("not-in-field", f"class {cls} has no expression in the field")
    return out


def affine_rows(
    system: System, rot: list, field_: NumberField
) -> list[tuple[dict[int, Any], Any]]:
    """Each contact equation as ``sum coef_k z_k + const`` over the centres and the side."""
    n = system.n
    half = Fraction(1, 2)
    rows: list[tuple[dict[int, Any], Any]] = []

    def offset(rotation, a, b):
        c, s = rotation
        return (c * a - s * b) * half, (s * a + c * b) * half

    def add(coefficients: dict[int, Any], column: int, value: Any) -> None:
        coefficients[column] = coefficients[column] + value if column in coefficients else value

    for owner, selector, other, a, b, _ in system.contacts.pair_equations:
        nx, ny = _normal(rot[owner], selector)
        ox, oy = offset(rot[other], a, b)
        coefficients: dict[int, Any] = {}
        add(coefficients, 2 * other, nx)
        add(coefficients, 2 * other + 1, ny)
        add(coefficients, 2 * owner, -nx)
        add(coefficients, 2 * owner + 1, -ny)
        rows.append((coefficients, nx * ox + ny * oy - field_.rational(half)))
    for square, a, b, axis, at in system.contacts.wall_equations:
        coefficients = {2 * square + axis: field_.one}
        if at:
            coefficients[2 * n] = -field_.one
        rows.append((coefficients, offset(rot[square], a, b)[axis]))
    for first, a, b, second, a2, b2, axis in system.contacts.corner_equations:
        coefficients = {}
        add(coefficients, 2 * first + axis, field_.one)
        add(coefficients, 2 * second + axis, -field_.one)
        rows.append(
            (coefficients, offset(rot[first], a, b)[axis] - offset(rot[second], a2, b2)[axis])
        )
    # A normal along an axis gives the other coordinate a zero coefficient: no unknown.
    return [
        ({k: v for k, v in coefficients.items() if not v.is_zero()}, constant)
        for coefficients, constant in rows
    ]


def _inverse(value: Any, field_: NumberField) -> Any:
    """An inverse in ``K``, directly where the element is rational."""
    if all(c == 0 for c in value.coeffs[1:]):
        return field_.rational(1 / value.coeffs[0])
    return value.inverse()


def _affine_add(left: dict[int, Any], right: dict[int, Any], scale: Any) -> dict[int, Any]:
    out = dict(left)
    for key, value in right.items():
        term = value * scale
        out[key] = out[key] + term if key in out else term
    return out


def solve_over_field(
    rows: list[tuple[dict[int, Any], Any]],
    unknowns: int,
    pinned: dict[int, Fraction],
    field_: NumberField,
) -> tuple[list[Any], dict[str, int]]:
    """Solve the linear contact rows exactly in ``K``: propagation, with seeds where it stalls.

    A row with one unknown left fixes it. Where none is left, an unknown is made a seed
    and carried symbolically, every value an affine form in the seeds; rows whose unknowns
    are all known become constraints on the seeds, which Gaussian elimination in ``K``
    solves. Any constraint left nonzero after elimination is a refusal: the rows are not
    consistent in ``K``.
    """
    known: dict[int, dict[int, Any]] = {k: {-1: field_.rational(v)} for k, v in pinned.items()}
    open_rows = list(range(len(rows)))
    closing: list[int] = []
    seeds: list[int] = []
    while open_rows:
        progressed = False
        remaining = []
        for index in open_rows:
            coefficients, _ = rows[index]
            left = [k for k in coefficients if k not in known]
            if not left:
                closing.append(index)
                progressed = True
            elif len(left) == 1:
                target = left[0]
                coefficients, constant = rows[index]
                form: dict[int, Any] = {-1: constant}
                for k, value in coefficients.items():
                    if k != target:
                        form = _affine_add(form, known[k], value)
                inverse = _inverse(coefficients[target], field_)
                known[target] = {key: -value * inverse for key, value in form.items()}
                progressed = True
            else:
                remaining.append(index)
        open_rows = remaining
        if not progressed and open_rows:
            counts: dict[int, int] = {}
            fewest = min(sum(1 for k in rows[i][0] if k not in known) for i in open_rows)
            for i in open_rows:
                left = [k for k in rows[i][0] if k not in known]
                if len(left) == fewest:
                    for k in left:
                        counts[k] = counts.get(k, 0) + 1
            seed = max(counts, key=lambda k: (counts[k], -k))
            known[seed] = {len(seeds): field_.one}
            seeds.append(seed)
    for k in range(unknowns):
        if k not in known:
            raise BuildError("underdetermined", f"unknown {k} is in no row")
    constraints = []
    for index in closing:
        coefficients, constant = rows[index]
        form = {-1: constant}
        for k, value in coefficients.items():
            form = _affine_add(form, known[k], value)
        constraints.append(form)
    solution = _eliminate(constraints, len(seeds), field_)
    values = []
    for k in range(unknowns):
        total = known[k].get(-1, field_.zero)
        for key, value in known[k].items():
            if key >= 0:
                total = total + value * solution[key]
        values.append(total)
    return values, {"seeds": len(seeds), "constraints": len(constraints)}


def _eliminate(constraints: list[dict[int, Any]], count: int, field_: NumberField) -> list[Any]:
    """Seeds from ``sum beta_s seed_s + alpha = 0`` rows, exactly, or refuse."""
    rows = [dict(c) for c in constraints]
    pivots: list[tuple[int, dict[int, Any]]] = []
    for seed in range(count):
        chosen = next((r for r in rows if seed in r and not r[seed].is_zero()), None)
        if chosen is None:
            raise BuildError("underdetermined", f"seed {seed} is held by no constraint")
        rows.remove(chosen)
        inverse = _inverse(chosen[seed], field_)
        chosen = {key: value * inverse for key, value in chosen.items()}
        updated = []
        for r in rows:
            if seed in r and not r[seed].is_zero():
                reduced = _affine_add(
                    {k: v for k, v in r.items() if k != seed}, chosen, -r[seed]
                )
                reduced.pop(seed, None)
                updated.append(reduced)
            else:
                updated.append(r)
        rows = updated
        pivots.append((seed, chosen))
    for r in rows:
        if any(not value.is_zero() for value in r.values()):
            raise BuildError("inconsistent", "a contact row is not an identity in the field")
    solution: list[Any] = [field_.zero] * count
    for seed, row in reversed(pivots):
        total = -row.get(-1, field_.zero)
        for key, value in row.items():
            if key >= 0 and key != seed:
                total = total - value * solution[key]
        solution[seed] = total
    return solution


def _scalar(value: Any) -> list[str]:
    return [str(c) for c in value.coeffs]


def field_witness(  # noqa: PLR0917
    n: int,
    field_: NumberField,
    poly: list[int],
    side: Any,
    centres: list,
    rot: list,
    *,
    identifier: str,
) -> dict[str, Any]:
    """A centre-basis Witness/v2 over ``K``, each scalar its coefficients, low degree first."""
    low, high = field_.root_bounds()
    return {
        "id": identifier,
        "n": n,
        "side": _scalar(side),
        "square_size": "1",
        "representation": "center-basis",
        "scalar": {
            "kind": "algebraic-number-field",
            "minimal_polynomial": [str(c) for c in poly],
            "isolating_interval": [str(low), str(high)],
        },
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": [
            {"id": k + 1, "center": [_scalar(x), _scalar(y)], "basis": [_scalar(c), _scalar(s)]}
            for k, ((x, y), (c, s)) in enumerate(zip(centres, rot, strict=True))
        ],
        "claim": {
            "coordinate_provenance": "verified",
            "method": "exact-algebraic",
            "limitations": (
                "Built here by devtools.build_field_configuration from T-174's rational "
                "certificate's contacts; every contact is an identity in the field. Finite "
                "construction feasibility only, decided by exact_verify."
            ),
        },
    }


# --------------------------------------------------------------------------- commands


def _decade(value: Any) -> int | None:
    if value is None or value == 0:
        return None
    return int(mp.floor(mp.log10(abs(value))))


def run_contacts(args: argparse.Namespace) -> dict[str, Any]:
    started = time.process_time()
    cert = read_certificate(Path(args.witness))
    contacts, poses = extract_contacts(cert)
    classes = Classes(cert.n, contacts)
    system = System(cert.n, contacts, classes)
    values = [float(v) for v in initial_values(system, poses)[: 2 * cert.n]]
    values.append(float(cert.side))
    values += [float(v) for v in initial_values(system, poses)[2 * cert.n + 1 :]]
    shape = structure(system, values)
    names = system.names()
    class_angles = []
    for cls, members in enumerate(classes.members):
        c, s = poses[members[0]][2], poses[members[0]][3]
        class_angles.append(
            {
                "class": cls,
                "members": len(members),
                "degrees": float(mp.degrees(mp.atan2(s, c))),
            }
        )
    return {
        "n": cert.n,
        "pairs_read": contacts.pairs_read,
        "kinds": contacts.kinds,
        "largest_contact_decade": _decade(contacts.largest_contact),
        "smallest_strict_decade": _decade(contacts.smallest_strict),
        "axis_squares": sum(1 for k in classes.of if k == Classes.AXIS),
        "classes": class_angles,
        "equations": system.equation_count,
        "unknowns": system.unknowns,
        "rank": shape.rank,
        "free": [names[k] for k in shape.free],
        "singular_gap": shape.singular_gap,
        "cpu_seconds": round(time.process_time() - started, 1),
    }


def prepare(witness: Path) -> tuple[Certificate, System, list, Structure]:
    """Read, type and measure: the certificate, its system, start values and structure."""
    cert = read_certificate(witness)
    contacts, poses = extract_contacts(cert)
    system = System(cert.n, contacts, Classes(cert.n, contacts))
    start = initial_values(system, poses)
    start[2 * cert.n] = _mpf(cert.side)
    shape = structure(system, [float(v) for v in start])
    return cert, system, start, shape


def run_solve(args: argparse.Namespace) -> dict[str, Any]:
    started = time.process_time()
    _cert, system, start, shape = prepare(Path(args.witness))
    point = stationary_refine(system, start, digits=args.digits)
    names = system.names()
    values = point.values
    if args.values:
        Path(args.values).write_text(
            json.dumps(
                {
                    "digits": args.digits,
                    "names": names,
                    "pinned": {names[k]: str(v) for k, v in point.pinned.items()},
                    "values": [mp.nstr(v, args.digits + 5, strip_zeros=False) for v in values],
                }
            )
        )
    return {
        "digits": args.digits,
        "contact_rank": shape.rank,
        "contact_free": [names[k] for k in shape.free],
        "kkt_shape": point.kkt_shape,
        "kkt_rank": point.kkt_rank,
        "multipliers": len(point.multipliers),
        "pinned": {names[k]: str(v) for k, v in point.pinned.items()},
        "steps": point.steps,
        "residual_decade": _decade(point.residual),
        "least_multiplier": mp.nstr(min(point.multipliers), 6),
        "side_digits": mp.nstr(values[2 * system.n], 301, strip_zeros=False),
        "classes_60": [
            mp.nstr(values[2 * system.n + 1 + cls], 60) for cls in range(system.classes.count)
        ],
        "cpu_seconds": round(time.process_time() - started, 1),
    }


#: The fractions of the carried digits at which an integer relation is searched.
LADDER = (0.55, 0.75, 0.97)
#: Digits below the carried precision a relation's residual must reach to be kept.
RELATION_GUARD = 60


def relation(values: list, digits: int) -> tuple[list[int] | None, list[dict[str, Any]]]:
    """An integer relation among `values`, searched at rising precision.

    A relation is kept only where its residual, re-evaluated at the full `digits`, falls
    below ``10^(RELATION_GUARD - digits)``: a relation that holds only to the precision
    it was found at is what a lattice returns for any input, and is recorded as such.
    """
    attempts = []
    for fraction in LADDER:
        working = int(digits * fraction)
        mp.mp.dps = working
        started = time.process_time()
        found = mp.pslq(
            [mp.mpf(v) for v in values], maxcoeff=10 ** (working // 25), maxsteps=4 * 10**5
        )
        took = round(time.process_time() - started, 1)
        if not found:
            attempts.append({"digits": working, "cpu_seconds": took, "found": None})
            continue
        mp.mp.dps = digits
        residual = mp.fsum(c * v for c, v in zip(found, values, strict=True))
        height = max(abs(c) for c in found)
        attempts.append(
            {
                "digits": working,
                "cpu_seconds": took,
                "height_digits": len(str(height)),
                "residual_decade": _decade(residual),
            }
        )
        if residual == 0 or abs(residual) < mp.mpf(10) ** (RELATION_GUARD - digits):
            return list(found), attempts
    return None, attempts


def _polynomial(path: Path) -> list[int]:
    """A polynomial, high to low: a JSON list or a fact's ``polynomial_high_to_low``."""
    data = json.loads(path.read_text())
    listed = data["polynomial_high_to_low"] if isinstance(data, dict) else data
    return [int(c) for c in listed]


def run_field(args: argparse.Namespace) -> dict[str, Any]:
    started = time.process_time()
    data = json.loads(Path(args.values).read_text())
    digits = int(data["digits"])
    mp.mp.dps = digits + 10
    names = data["names"]
    values = {name: mp.mpf(text) for name, text in zip(names, data["values"], strict=True)}
    tangents = [name for name in names if name.startswith("t[")]
    generator = values[args.generator]
    close = mp.mpf(10) ** (RELATION_GUARD - digits)
    powers = [generator**k for k in range(args.degree + 1)]
    minimal, attempts = relation(powers, digits)
    receipt: dict[str, Any] = {"digits": digits, "generator": args.generator}
    receipt["generator_relation"] = {
        "high_to_low": [str(c) for c in reversed(minimal)] if minimal else None,
        "attempts": attempts,
    }
    if minimal:
        x = sympy.Symbol("x")
        poly = sympy.Poly(list(reversed(minimal)), x, domain=sympy.ZZ)
        _, factors = poly.factor_list()
        receipt["generator_relation"]["irreducible"] = (
            len(factors) == 1 and factors[0][1] == 1 and factors[0][0].degree() == poly.degree()
        )
        receipt["generator_relation"]["degree"] = int(poly.degree())
    classes = {}
    for name in tangents:
        value = values[name]
        mp.mp.dps = digits + 10
        if name in data["pinned"]:
            classes[name] = {"kind": "pinned", "value": data["pinned"][name]}
        elif abs(value - generator) < close:
            classes[name] = {"kind": "generator"}
        elif abs(value + generator) < close:
            classes[name] = {"kind": "minus generator"}
        elif minimal and name in args.express:
            found, tries = relation([value, *powers[:-1]], digits)
            classes[name] = {
                "kind": "in field" if found else "not found",
                "relation": [str(c) for c in found] if found else None,
                "attempts": tries,
            }
        else:
            classes[name] = {"kind": "not searched"}
        classes[name]["decimal_40"] = mp.nstr(value, 40)
    receipt["classes"] = classes
    if args.polynomial:
        poly_high = _polynomial(Path(args.polynomial))
        side = values["S"]
        mp.mp.dps = digits + 10
        residual = mp.polyval(poly_high, side)
        scale = mp.polyval([abs(c) for c in poly_high], abs(side))
        receipt["side_against_polynomial"] = {
            "relative_residual_decade": _decade(residual / scale),
            "side_100": mp.nstr(side, 101, strip_zeros=False),
        }
    receipt["cpu_seconds"] = round(time.process_time() - started, 1)
    return receipt


def rotation_in(t: Any, field_: NumberField) -> tuple[Any, Any]:
    one = field_.one
    denominator = _inverse(one + t * t, field_)
    return (one - t * t) * denominator, t * 2 * denominator


def run_build(args: argparse.Namespace) -> dict[str, Any]:
    started = time.process_time()
    _cert, system, _start, _shape = prepare(Path(args.witness))
    data = json.loads(Path(args.values).read_text())
    field_receipt = json.loads(Path(args.field).read_text())
    digits = int(data["digits"])
    mp.mp.dps = digits + 10
    names = data["names"]
    numeric = [mp.mpf(text) for text in data["values"]]
    by_name = dict(zip(names, numeric, strict=True))
    poly = [int(c) for c in field_receipt["generator_relation"]["high_to_low"]]
    field_ = field_of(field_receipt, by_name[field_receipt["generator"]], digits)
    tangents = class_tangents(system, field_receipt, field_)
    root = mp.mpf(field_.decimal(field_.alpha, digits - 100))
    worst_tangent = max(
        (abs(_value_at(t, root) - by_name[f"t[{cls}]"]) for cls, t in enumerate(tangents)),
        default=mp.mpf(0),
    )
    if worst_tangent > mp.mpf(10) ** (200 - digits):
        raise BuildError(
            "not-in-field", f"a class tangent misses its value by {mp.nstr(worst_tangent, 3)}"
        )
    by_class = [rotation_in(t, field_) for t in tangents]
    rot = [
        (field_.one, field_.zero) if cls == Classes.AXIS else by_class[cls]
        for cls in system.classes.of
    ]
    unknowns = 2 * system.n + 1
    matrix = jacobian(system, [float(v) for v in numeric])[:, :unknowns]
    _, r_p, pivots = pivoted_qr(matrix)
    diagonal = np.abs(np.diag(r_p))
    rank = int(np.sum(diagonal > diagonal[0] * 1e-10))
    earlier = [names.index(name) for name in data["pinned"] if names.index(name) < unknowns]
    preference = earlier + [int(k) for k in reversed(pivots) if int(k) not in set(earlier)]
    free = choose_pins(matrix, rank, preference=preference)
    pinned = {
        k: Fraction(data["pinned"][names[k]]) if names[k] in data["pinned"] else pin(numeric[k])
        for k in free
    }
    rows = affine_rows(system, rot, field_)
    values, stats = solve_over_field(rows, unknowns, pinned, field_)
    identities = 0
    for coefficients, constant in rows:
        total = constant
        for k, coefficient in coefficients.items():
            total = total + coefficient * values[k]
        if not total.is_zero():
            raise BuildError("inconsistent", "a contact is not an identity in the field")
        identities += 1
    moved = max(abs(_value_at(values[k], root) - numeric[k]) for k in range(unknowns))
    side = values[2 * system.n]
    receipt: dict[str, Any] = {
        "field_degree": len(poly) - 1,
        "field_polynomial_high_to_low": [str(c) for c in poly],
        "position_rank": rank,
        "position_pins": {names[k]: str(v) for k, v in pinned.items()},
        "seeds": stats["seeds"],
        "seed_constraints": stats["constraints"],
        "contact_identities": identities,
        "largest_move_from_solve": mp.nstr(moved, 3),
        "side_100": field_.decimal(side, 100),
    }
    if args.polynomial:
        side_poly = _polynomial(Path(args.polynomial))
        total = field_.zero
        for c in side_poly:
            total = total * side + c
        receipt["side_polynomial_vanishes_in_field"] = total.is_zero()
    witness = field_witness(
        system.n,
        field_,
        poly,
        side,
        [(values[2 * k], values[2 * k + 1]) for k in range(system.n)],
        rot,
        identifier=args.identifier,
    )
    document = {
        "softschema": {
            "contract": "packing.squares:Witness/v2",
            "schema": "../witness.schema.yaml",
            "envelope": "witness",
            "status": "enforced",
        },
        "witness": witness,
    }
    raw = json.dumps(document, separators=(",", ":")).encode()
    Path(args.output).write_bytes(gzip.compress(raw, mtime=0))
    receipt["witness"] = {
        "path": args.output,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
    }
    receipt["cpu_seconds"] = round(time.process_time() - started, 1)
    return receipt


def _value_at(element: Any, root: Any) -> Any:
    total = mp.mpf(0)
    for c in reversed(element.coeffs):
        total = total * root + mp.mpf(c.numerator) / c.denominator
    return total


def run_decide(args: argparse.Namespace) -> dict[str, Any]:
    from devtools.algebraic_witness_reports import ROUTE, decide, validate_job  # noqa: PLC0415

    raw = gzip.decompress(Path(args.witness).read_bytes())
    witness = json.loads(raw)["witness"]
    row = decide(witness, args.control)
    validate_job(row, witness, args.control)
    verdict = row[ROUTE]
    return {
        "witness_sha256": hashlib.sha256(raw).hexdigest(),
        "control": args.control,
        "verification_passed": verdict.get("verification_passed"),
        "pairs_tested": verdict.get("pairs_tested"),
        "failures": [failure[0] for failure in verdict.get("failures", [])][:5],
        "row": row,
        "cpu_seconds": round(row["cpu_seconds"], 1),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    contacts = sub.add_parser("contacts", help="type the contact graph and measure its rank")
    contacts.add_argument("witness")
    contacts.add_argument("--out")
    solve = sub.add_parser("solve", help="refine the contact system at high precision")
    solve.add_argument("witness")
    solve.add_argument("--digits", type=int, default=800)
    solve.add_argument("--values", help="write the refined values here (JSON)")
    solve.add_argument("--out")
    fld = sub.add_parser(
        "field", help="the generator's minimal polynomial and the classes in it"
    )
    fld.add_argument("values", help="the values a solve wrote")
    fld.add_argument("--generator", default="t[11]")
    fld.add_argument("--degree", type=int, default=21)
    fld.add_argument("--express", nargs="*", default=[], help="class tangents to express")
    fld.add_argument("--polynomial", help="a JSON list, high to low, to evaluate at the side")
    fld.add_argument("--out")
    bld = sub.add_parser("build", help="the exact configuration in the field")
    bld.add_argument("witness")
    bld.add_argument("--values", required=True)
    bld.add_argument("--field", required=True)
    bld.add_argument("--polynomial")
    bld.add_argument("--identifier", default="W-route-a")
    bld.add_argument("--output", required=True, help="the built witness (.json.gz)")
    bld.add_argument("--out")
    dec = sub.add_parser("decide", help="exact_verify a built witness, or one of its controls")
    dec.add_argument("witness")
    dec.add_argument(
        "--control",
        default="positive",
        choices=("positive", "duplicate-square-overlap", "square-translated-outside-container"),
    )
    dec.add_argument("--out")
    args = parser.parse_args(argv)
    if args.command == "contacts":
        receipt = run_contacts(args)
    elif args.command == "solve":
        receipt = run_solve(args)
    elif args.command == "field":
        receipt = run_field(args)
    elif args.command == "build":
        receipt = run_build(args)
    elif args.command == "decide":
        receipt = run_decide(args)
    else:  # pragma: no cover - argparse refuses other commands
        return 2
    text = json.dumps(receipt, indent=2, default=str)
    if args.out:
        Path(args.out).write_text(text + "\n")
    print(text[:4000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
