#!/usr/bin/env python3
"""Decide a fractional unavoidable-set certificate for s(n) >= L, exactly.

Usage:  python verify_claim.py certificate.json
        python verify_claim.py t-018-verifiable-claim-19-5.md   (embeds the certificate)

Standard library only, CPython 3.12 or later. Every decision is made in
fractions.Fraction. One line is printed per condition, then one comparing the file's
declared claim, total_mass and least_cell_mass with what was computed, then VERIFIED
or REFUSED; the exit status is 0 only when all five conditions hold and the
declarations match, and 1 on any refusal. Condition 5, the sweep, is evaluated only
once Conditions 1 to 4 hold, and its line says so when it was not. A file that is not
a certificate of the form below is refused by name before any condition. If the
sweep's own cross-check fails, the verifier and not the certificate is broken: one
line beginning INTERNAL ERROR replaces the verdict, and the exit status is 2, as it
is for a usage error.

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
pinned by SHA-256 to the retained 381/100 certificate, refuses at the first failing
check instead of reporting Conditions 1 to 4 in full, and shares this file's floor.
This file decides any certificate of the form above, within the size ceilings below,
and is the one the claim documents embed.
"""

# ruff: noqa: N803, N806  -- L, B, D, F, U, V, X, Y are the theorem's own symbols.

import argparse
import json
import re
import sys
from bisect import bisect_left, bisect_right
from collections.abc import Sequence
from fractions import Fraction
from itertools import accumulate, pairwise
from math import lcm
from pathlib import Path

# Ceilings on a certificate's size, so that a run stays within memory and within the hour
# on an ordinary machine. At one direction the event grid holds up to (2 atoms + 2)^2
# cells as Python integers: measured on 2026-09-05 at 450 MB and a second per direction
# for the retained 1,121 atoms, and at 1.2 GB and three seconds at the atom ceiling. A
# larger certificate is refused before any condition, by name; a reader who raises these
# knows what the run will cost. The retained certificates have 1,121 atoms and 181
# directions; the repository's retention gate accepts up to 4,096 atoms.
MAX_ATOMS = 2000
MAX_DIRECTIONS = 1000


def load(path):
    """The certificate as (n, L, B, tangents, atoms, declared), where declared holds the
    file's own claim, total_mass and least_cell_mass for comparison with what is
    computed; any other shape is refused. So are an atom outside [0, L]^2 and two atoms
    at one site: the theorem would tolerate both, an outside atom only adding to the
    total and a repeated site being one site of the summed weight, but neither is a
    well-formed certificate, and minimal_verify.py refuses them too.

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
    if len(record["atoms"]) > MAX_ATOMS or K + 1 > MAX_DIRECTIONS:
        message = (
            f"{len(record['atoms'])} atoms over {K + 1} directions; this verifier decides "
            f"at most {MAX_ATOMS} atoms and {MAX_DIRECTIONS} directions"
        )
        raise ValueError(message)
    atoms, sites = [], set()
    for atom in record["atoms"]:
        x, y, w = (rational(value) for value in atom)
        if w < 0:
            message = f"negative weight {w} at ({x}, {y})"
            raise ValueError(message)
        if not (0 <= x <= L and 0 <= y <= L):
            message = f"atom ({x}, {y}) lies outside the container [0, {L}]^2"
            raise ValueError(message)
        if (x, y) in sites:
            message = f"two atoms share the site ({x}, {y})"
            raise ValueError(message)
        sites.add((x, y))
        atoms.append((x, y, w))
    claim = record["claim"]
    if not isinstance(claim, str):
        message = f"claim must be a string such as 's(11) >= 19/5', got {claim!r}"
        raise TypeError(message)
    declared = {
        "claim": claim,
        "total_mass": rational(record["total_mass"]),
        "least_cell_mass": rational(record["least_cell_mass"]),
    }
    return n, L, B, [T * k / K for k in range(K + 1)], atoms, declared


def symmetric(atoms, L):
    """Condition 1. The eight maps form a group, so checking every site of the support
    against every image is the whole of invariance."""
    weight = {(x, y): w for x, y, w in atoms}  # one atom per site: load refused a repeat
    for (x, y), w in weight.items():
        flips = [(p, q) for p in (x, L - x) for q in (y, L - y)]
        for p, q in flips + [(q, p) for p, q in flips]:  # the eight symmetries of [0, L]^2
            if weight.get((p, q), 0) != w:
                return (
                    f"({x}, {y}) has weight {w} but ({p}, {q}) has {weight.get((p, q), 0)}",
                    False,
                )
    return f"{len(atoms)} atoms on distinct sites, invariant under the 8 symmetries", True


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
# F, is empty when 2h > L: no B-square at this direction fits, Condition 5 quantifies
# over nothing here and holds vacuously, and the direction is reported as deciding
# nothing. It is the single point (L/2, L/2) when 2h = L, and that one placement is
# scored directly. Otherwise F has nonempty interior. The lines u = u_i +- B/2,
# v = v_i +- B/2, with the four lines u = umin, u = umax, v = vmin, v = vmax at F's
# extreme coordinates (its bounding box: F's own edges are oblique when t > 0, and they
# are not added), cut the plane into finitely many open cells. The mass is constant on
# a cell (each atom's box has its edges on the lines); a point on a cell's boundary has
# at least the cell's mass (a closed box meeting the cell contains its closure); and
# every point of F is in the closure of a cell meeting F: F has interior points within
# every distance of it, finitely many lines do not cover an open set, so within every
# distance of the point some cell meeting F has a point, and since there are finitely
# many cells one cell does at every distance, which is to say the point is in its
# closure. So the least mass over F is the least over the cells meeting F. A cell may
# straddle F's oblique edge, and the clipping test below decides exactly which cells
# meet F: a cell (a, b) x (a', b') with [a, b] inside F's u-projection meets F iff
# a' < hi and lo < b', where [lo, hi] is the v-range of F within the closed strip
# a <= u <= b, since the open strip's part of F projects onto an interval between
# (lo, hi) and [lo, hi].


def mass_at(atoms, c, s, half, center):
    """The mass of the closed B-square with this center, in original coordinates."""
    X, Y = center
    return sum(
        w
        for x, y, w in atoms
        if abs(c * (x - X) + s * (y - Y)) <= half and abs(-s * (x - X) + c * (y - Y)) <= half
    )


def least_mass(L, B, t, atoms, scale):
    """The least mass over every admissible center at one net direction, with a center
    (X, Y) that attains it and the number of cells decided; (None, None, 0) at a
    direction where no B-square fits, and the single placement, counted as one cell,
    where exactly one does."""
    c, s = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)  # exact: c^2 + s^2 = 1
    half, h = B / 2, B * (abs(c) + abs(s)) / 2
    if 2 * h > L:
        return None, None, 0
    if 2 * h == L:
        return mass_at(atoms, c, s, half, (L / 2, L / 2)), (L / 2, L / 2), 1
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
    # The sweep's own cross-check: the witness must be admissible, and summing the atoms
    # at it directly must give the grid's minimum. A failure here is this file's bug, not
    # the certificate's, and main reports it as one, apart from either verdict.
    direct = mass_at(atoms, c, s, half, (X, Y))
    if not (h <= X <= L - h and h <= Y <= L - h):
        message = f"at t = {t} the witness center ({X}, {Y}) admits no B-square"
        raise AssertionError(message)
    if direct != Fraction(best, scale):
        message = (
            f"at t = {t} the center ({X}, {Y}) covers {direct} summed directly, "
            f"but the grid says {Fraction(best, scale)}"
        )
        raise AssertionError(message)
    return Fraction(best, scale), (X, Y), cells


def sweep(L, B, tangents, atoms):
    """Condition 5 over the whole net: its report, whether it holds, and the least mass
    found, None when no direction admitted a placement."""
    scale = lcm(*(w.denominator for _, _, w in atoms))
    found, cells, vacuous = [], 0, 0
    for k, t in enumerate(tangents):
        mass, center, count = least_mass(L, B, t, atoms, scale)
        if mass is None:
            vacuous += 1
        else:
            found.append((mass, k, t, center))
        cells += count
        print(".", end="", file=sys.stderr, flush=True)
    if not found:  # every direction vacuous: the hypothesis holds, and nothing was decided
        vacuity = f"no placement at any of the {len(tangents)} directions"
        return f"{vacuity}, so nothing was decided", True, None
    least, k, t, (X, Y) = min(found)
    detail = (
        f"least covered mass {least} at direction {k} (t = {t}), center ({X}, {Y}); "
        f"{cells} cells over {len(tangents)} directions"
    )
    if vacuous:
        detail += f", {vacuous} of them admitting no placement"
    return detail, least >= 1, least


def declarations(declared, n, L, total, least):
    """The file's own claim, total_mass and least_cell_mass against what was computed.
    The theorem never reads them, but a file that states its figures wrongly is wrong
    about itself, and success must not read as vouching for them. least is None when
    the sweep did not run or met no placement, and least_cell_mass is then not compared."""
    computed = {"claim": f"s({n}) >= {L}", "total_mass": total, "least_cell_mass": least}
    compared = [name for name, value in computed.items() if value is not None]
    wrong = [name for name in compared if declared[name] != computed[name]]

    def shown(value):
        return repr(value) if isinstance(value, str) else str(value)

    if wrong:
        detail = "; ".join(
            f"{name} declared {shown(declared[name])}, computed {shown(computed[name])}"
            for name in wrong
        )
    else:
        detail = ", ".join(f"{name} {shown(declared[name])}" for name in compared)
        detail += ", as computed"
    if least is None:
        detail += "; least_cell_mass not compared"
    return detail, not wrong


def decide(n, L, B, tangents, atoms, declared):  # noqa: PLR0917 -- the certificate, as load returns it
    """Print every condition with its numbers, then the declarations against what was
    computed; return 0 if all hold, else 1."""
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
    least = None
    if all(verdicts):
        detail, holds, least = sweep(L, B, tangents, atoms)
        report(5, detail, holds=holds)
    else:  # the sweep is the expensive step, and a refused file is not owed it
        failed = [str(k + 1) for k, holds in enumerate(verdicts) if not holds]
        which = (
            f"Condition {failed[0]} fails"
            if len(failed) == 1
            else f"Conditions {', '.join(failed)} fail"
        )
        print(
            f"Condition 5 not evaluated: {which}, and the sweep runs only when "
            "Conditions 1 to 4 hold",
            flush=True,
        )
    detail, holds = declarations(declared, n, L, total, least)
    verdicts.append(holds)
    print(f"Declarations {'hold' if holds else 'fail'}: {detail}", flush=True)
    print(f"VERIFIED: s({n}) >= {L}" if all(verdicts) else "REFUSED")
    return 0 if all(verdicts) else 1


def main(argv: Sequence[str] | None = None) -> int:
    """Verdicts go to stdout with status 0 or 1. Status 2 is no verdict: a usage error,
    which argparse reports on stderr, or the sweep's own cross-check failing, reported on
    stdout as one INTERNAL ERROR line in place of the verdict."""
    parser = argparse.ArgumentParser(
        description="Decide a fractional unavoidable-set certificate for s(n) >= L, exactly.",
        epilog=(
            "One line per condition, one comparing the file's declarations with what was "
            "computed, then VERIFIED or REFUSED; the exit status is 0 only after VERIFIED "
            "and 1 on any refusal. Status 2 is no verdict: a usage error, or an INTERNAL "
            "ERROR line saying the verifier disagreed with itself."
        ),
    )
    parser.add_argument(
        "certificate", help="a certificate.json, or a claim document that embeds one"
    )
    arguments = parser.parse_args(argv)
    try:
        certificate = load(arguments.certificate)
    except (OSError, KeyError, TypeError, ValueError) as error:
        print(f"REFUSED: not a certificate of the expected shape: {error}")
        return 1
    try:
        return decide(*certificate)
    except AssertionError as error:  # the sweep's cross-check: this file is what failed
        print(f"INTERNAL ERROR: no verdict; the verifier disagrees with itself: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
