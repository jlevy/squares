#!/usr/bin/env python3
"""Decide a fractional unavoidable-set certificate for s(n) >= L, exactly.

Usage:  python verify_claim.py certificate.json
        python verify_claim.py t-018-verifiable-claim-19-5.md   (embeds the certificate)

Standard library only, CPython 3.10 or later. Every decision is made in
fractions.Fraction. One line is printed per condition, then VERIFIED or REFUSED,
and the exit status is 0 only when all five conditions hold.

THE THEOREM. Let s(n) be the least side of a square containing n unit squares
with pairwise disjoint interiors, rotation allowed. A certificate names an
integer n >= 1, rationals L > 0 (container side) and B > 0 (shrunken side), a
net of rationals 0 = t_0 < ... < t_K standing for the angles 2 arctan(t_k), and
atoms (x_i, y_i, w_i) with rational coordinates and weights w_i >= 0; the mass
of a set is the total weight of the atoms in it. If
  Condition 1  the weighted atoms are invariant under the eight symmetries of
               the container [0, L]^2;
  Condition 2  the total weight is strictly less than n;
  Condition 3  2 arctan(t_K) >= pi/4, decided as t_K^2 + 2 t_K - 1 >= 0;
  Condition 4  B (1 + D) < 1 for D = max_k (t_{k+1} - t_k) / (1 + t_k t_{k+1}),
               the tangent of the largest half-gap between adjacent net angles;
  Condition 5  every closed square of side B at a net angle that lies inside
               [0, L]^2 has mass at least 1;
then n unit squares with disjoint interiors do not fit in [0, L]^2, so s(n) >= L.
(Each unit square, reflected in the diagonal if its angle exceeds pi/4, contains
strictly inside it a B-square at the nearest net angle, of mass >= 1; the n such
squares are disjoint, so the total weight is at least n, against Condition 2.)

minimal_verify.py, beside this file, is the other standard-library check: it is
pinned by SHA-256 to the retained 381/100 certificate, also compares the record's
declared total and least mass with what it computes, refuses at the first failing
check instead of reporting all five, and runs on CPython 3.8. This file decides any
certificate of the form above and is the one the claim documents embed.
"""

# ruff: noqa: N803, N806  -- L, B, D, F, U, V, X, Y are the theorem's own symbols.

import json
import re
import sys
from bisect import bisect_left, bisect_right
from fractions import Fraction
from itertools import accumulate, pairwise
from math import lcm
from pathlib import Path


def load(path):
    """The certificate as (n, L, B, tangents, atoms); any other shape is refused.

    The path is the certificate's JSON file, or a Markdown document carrying it in a
    fenced json block: each verifiable-claim document embeds the certificate it
    decides, so the whole claim travels as one file."""
    text = Path(path).read_text(encoding="utf-8")
    if not text.lstrip().startswith("{"):
        fence = re.search(
            r"^`{3,}json[ \t]*\n(.*?)^`{3,}[ \t]*$", text, re.MULTILINE | re.DOTALL
        )
        if fence is None:
            message = "neither a JSON object nor a Markdown document with a fenced json block"
            raise ValueError(message)
        text = fence.group(1)
    record = json.loads(text)

    def rational(value):
        if not isinstance(value, str):  # a JSON float would be rounded: refuse it
            message = f"rationals must be strings such as '19/5', got {value!r}"
            raise TypeError(message)
        return Fraction(value)

    variant = record.get("variant", "unconditional")
    if variant != "unconditional":  # a class or conditional certificate claims something else
        message = f"variant {variant!r} declared; only unconditional certificates are decided"
        raise ValueError(message)
    n, K = record["n"], record["direction_steps"]
    if not (isinstance(n, int) and isinstance(K, int) and n >= 1 and K >= 1):
        message = "n and direction_steps must be integers, n >= 1 and direction_steps >= 1"
        raise ValueError(message)
    L, B, T = (rational(record[key]) for key in ("outer_side", "square_side", "angle_limit"))
    if not (L > 0 and B > 0 and T > 0):
        message = "outer_side, square_side and angle_limit must be positive"
        raise ValueError(message)
    atoms = []
    for atom in record["atoms"]:
        x, y, w = (rational(value) for value in atom)
        if w < 0:
            message = f"negative weight {w} at ({x}, {y})"
            raise ValueError(message)
        atoms.append((x, y, w))
    return n, L, B, [T * k / K for k in range(K + 1)], atoms


def symmetric(atoms, L):
    """Condition 1. The eight maps form a group, so checking every site of the support
    against every image is the whole of invariance."""
    weight = {}
    for x, y, w in atoms:
        weight[x, y] = weight.get((x, y), 0) + w
    for (x, y), w in weight.items():
        flips = [(p, q) for p in (x, L - x) for q in (y, L - y)]
        for p, q in flips + [(q, p) for p, q in flips]:  # the eight symmetries of [0, L]^2
            if weight.get((p, q), 0) != w:
                return (
                    f"({x}, {y}) has weight {w} but ({p}, {q}) has {weight.get((p, q), 0)}",
                    False,
                )
    return f"{len(atoms)} atoms, {len(weight)} sites, invariant under the 8 symmetries", True


def extent(polygon, axis, low, high):
    """Range of the other coordinate over the part of a convex polygon with
    low <= coordinate[axis] <= high: that part's vertices are the polygon's vertices in
    the slab and the crossings of its edges with the slab's two boundary lines."""
    points = [p for p in polygon if low <= p[axis] <= high]
    for p, q in zip(polygon, polygon[1:] + polygon[:1], strict=True):
        for bound in (low, high):
            if (p[axis] - bound) * (q[axis] - bound) < 0:  # a strict crossing
                f = (bound - p[axis]) / (q[axis] - p[axis])
                points.append((p[0] + f * (q[0] - p[0]), p[1] + f * (q[1] - p[1])))
    values = [p[1 - axis] for p in points]
    return min(values), max(values)


# Condition 5 at one direction, decided over the continuum of centers by a finite sweep.
# In the coordinates u = c x + s y, v = -s x + c y the placed square is axis-parallel:
# the closed B-square centered at (U, V) contains the atom at (u_i, v_i) iff
# |u_i - U| <= B/2 and |v_i - V| <= B/2, and it lies inside [0, L]^2 iff its center
# (X, Y) has h <= X, Y <= L - h with h = B(|c| + |s|)/2. That closed square of centers,
# F, has nonempty interior (2h < L is checked). The lines u = u_i +- B/2,
# v = v_i +- B/2 and the four lines bounding F cut the plane into open cells. The mass
# is constant on a cell (each atom's box has its edges on the lines); a point on a
# cell's boundary has at least the cell's mass (a closed box meeting the cell contains
# its closure); and every point of F is in the closure of a cell meeting F (F has
# interior points arbitrarily near it, and an open set is not covered by finitely many
# lines). So the least mass over F is the least over the cells meeting F. A cell
# (a, b) x (a', b') with [a, b] inside F's u-projection meets F iff a' < hi and lo < b',
# where [lo, hi] is the v-range of F within the closed strip a <= u <= b: the open
# strip's part of F projects onto an interval between (lo, hi) and [lo, hi].


def least_mass(L, B, t, atoms, scale):
    """The least mass over every admissible center at one net direction, with a center
    (X, Y) that attains it and the number of cells decided."""
    c, s = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)  # exact: c^2 + s^2 = 1
    half, h = B / 2, B * (abs(c) + abs(s)) / 2
    if 2 * h >= L:
        message = f"no B-square at t = {t} fits inside the container with room to spare"
        raise ValueError(message)
    rotated = [(c * x + s * y, -s * x + c * y, w) for x, y, w in atoms]
    corners = ((h, h), (L - h, h), (L - h, L - h), (h, L - h))
    F = [(c * x + s * y, -s * x + c * y) for x, y in corners]
    umin, umax = min(u for u, _ in F), max(u for u, _ in F)
    vmin, vmax = min(v for _, v in F), max(v for _, v in F)
    U = sorted({u + d for u, _, _ in rotated for d in (-half, half)} | {umin, umax})
    V = sorted({v + d for _, v, _ in rotated for d in (-half, half)} | {vmin, vmax})
    ui, vi = {u: i for i, u in enumerate(U)}, {v: j for j, v in enumerate(V)}

    # grid[i][j] becomes the scaled mass on the cell (U[i], U[i+1]) x (V[j], V[j+1]):
    # a two-dimensional difference array, then two prefix sums, all in integers.
    grid = [[0] * len(V) for _ in U]
    for u, v, w in rotated:
        i0, i1, j0, j1 = ui[u - half], ui[u + half], vi[v - half], vi[v + half]
        m = int(w * scale)
        grid[i0][j0] += m
        grid[i0][j1] -= m
        grid[i1][j0] -= m
        grid[i1][j1] += m
    grid = [list(accumulate(row)) for row in grid]  # prefix sums along v ...
    columns = [list(accumulate(column)) for column in zip(*grid, strict=True)]  # ... then u
    grid = [list(row) for row in zip(*columns, strict=True)]

    strips, cells = [], 0
    for i in range(ui[umin], ui[umax]):  # the strips within F's u-projection
        lo, hi = extent(F, 0, U[i], U[i + 1])
        j0, j1 = bisect_right(V, lo) - 1, bisect_left(V, hi) - 1
        row = grid[i][j0 : j1 + 1]
        cells += len(row)
        strips.append((min(row), i, j0 + row.index(min(row))))
    best, i, j = min(strips)

    # A center in the least cell and in F: v strictly between the cell's v-bounds and
    # F's v-range on the strip, then u strictly inside F's u-range at that v.
    lo, hi = extent(F, 0, U[i], U[i + 1])
    Vc = (max(V[j], lo) + min(V[j + 1], hi)) / 2
    left, right = extent(F, 1, Vc, Vc)
    Uc = (max(U[i], left) + min(U[i + 1], right)) / 2
    X, Y = c * Uc - s * Vc, s * Uc + c * Vc
    direct = sum(
        w
        for x, y, w in atoms
        if abs(c * (x - X) + s * (y - Y)) <= half and abs(-s * (x - X) + c * (y - Y)) <= half
    )
    if not (h <= X <= L - h and h <= Y <= L - h and direct == Fraction(best, scale)):
        message = f"center ({X}, {Y}) covers {direct}, the grid says {Fraction(best, scale)}"
        raise AssertionError(message)
    return Fraction(best, scale), (X, Y), cells


def decide(n, L, B, tangents, atoms):
    """Print every condition with its numbers; return 0 if all hold, else 1."""
    verdicts = []

    def report(number, detail, *, holds):
        verdicts.append(holds)
        print(f"Condition {number} {'holds' if holds else 'fails'}: {detail}", flush=True)

    detail, holds = symmetric(atoms, L)
    report(1, detail, holds=holds)
    total = sum(w for _, _, w in atoms)
    report(2, f"total mass {total} against n = {n}", holds=total < n)
    t, slack = tangents[-1], tangents[-1] ** 2 + 2 * tangents[-1] - 1
    report(3, f"t_K = {t}, t_K^2 + 2 t_K - 1 = {slack}", holds=slack >= 0)
    D = max((b - a) / (1 + a * b) for a, b in pairwise(tangents))
    report(4, f"D = {D}, B(1 + D) = {B * (1 + D)}", holds=B * (1 + D) < 1)
    scale = lcm(*(w.denominator for _, _, w in atoms))
    sweep, cells = [], 0
    for k, t in enumerate(tangents):
        mass, center, count = least_mass(L, B, t, atoms, scale)
        sweep.append((mass, k, t, center))
        cells += count
        print(".", end="", file=sys.stderr, flush=True)
    mass, k, t, (X, Y) = min(sweep)
    report(
        5,
        f"least covered mass {mass} at direction {k} (t = {t}), center ({X}, {Y}); "
        f"{cells} cells over {len(tangents)} directions",
        holds=mass >= 1,
    )
    print(f"VERIFIED: s({n}) >= {L}" if all(verdicts) else "REFUSED")
    return 0 if all(verdicts) else 1


if __name__ == "__main__":
    if len(sys.argv[1:]) != 1:
        sys.exit(__doc__)
    try:
        certificate = load(sys.argv[1])
    except (OSError, KeyError, TypeError, ValueError) as error:
        sys.exit(f"not a certificate of the expected shape: {error}")
    sys.exit(decide(*certificate))
