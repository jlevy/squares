#!/usr/bin/env python3
"""Decide a weighted fractional unavoidable-set certificate for s(n) >= L.

Usage:
    python3 verify.py CERTIFICATE.json [--audit N] [--verbose]

Standard library only: fractions, json, bisect, itertools, operator, random,
re, sys, time. Any CPython 3.12 or later. Nothing here imports numpy or any
file from the repository this ships with, so the decision rests on Python's
arbitrary-precision integers and on the reader's check of this file against
the theorem in README.md.

Every quantity that decides anything is a fractions.Fraction. Floats appear
only inside f-strings that print approximations next to the exact value.

THE THEOREM (README.md states it in full, with the proof). A certificate
names n, a container side L, a shrunken side B, a direction net of
half-angle tangents t_k = T k / K (k = 0..K), and weighted atoms (x, y, w).
Write theta_k = 2 arctan(t_k). If

  Condition 1  the weighted atom set is invariant under the eight symmetries of the
      container [0, L]^2 (the proof uses one of them, the reflection in the
      diagonal, so this is a stronger hypothesis than needed);
  Condition 2  the total weight is strictly less than n;
  Condition 3  theta_K >= pi/4, decided as t_K^2 + 2 t_K - 1 >= 0;
  Condition 4  B (1 + D) < 1, where D = max_k (t_{k+1} - t_k) / (1 + t_k t_{k+1}) is
      the largest tangent of HALF a gap between adjacent net angles;
  Condition 5  every closed square of side B at a net angle theta_k that lies inside
      [0, L]^2 covers atoms of total weight at least 1;

then n unit squares with pairwise disjoint interiors do not fit in [0, L]^2,
and therefore s(n) >= L.

RUNTIME. Condition 5 is the only expensive condition. Measured with CPython 3.12
through 3.14 on a four-core machine with other work running: 28 to 29 s for the
n = 11 certificate (425 atoms, 181 directions, 90.5 million cells in all) and
9 s for the n = 17 control (168 atoms, 16.6 million cells); an idle core is
faster and a contended one slower. Memory stays under 100 MB.
"""

# ruff: noqa: N803, N806 -- L, B, D, X, Y, U, V, K, F are the theorem's own symbols.

import json
import random
import re
import sys
import time
from bisect import bisect_left, bisect_right
from collections.abc import Sequence
from fractions import Fraction
from itertools import accumulate, pairwise
from operator import add
from pathlib import Path

RATIONAL = re.compile(r"^-?[0-9]+(/[1-9][0-9]*)?$")


class CertificateFormatError(ValueError):
    """The JSON cannot be interpreted as an exact certificate record.

    One type for every way a file can fail to be a certificate at all, so the
    command line can promise a labelled refusal instead of a traceback without
    catching exception types it never meant to catch.
    """


# ---------------------------------------------------------------------------
# Loading. The JSON carries exact rationals as strings ("p/q" or "p"); the
# regex refuses anything else, so a decimal or a float cannot slip in and be
# silently rounded.
# ---------------------------------------------------------------------------


def rational(text):
    # fullmatch, not match: `$` also matches just before a trailing newline,
    # so `match` would accept "1/2\n" and Fraction would then read it happily.
    if not isinstance(text, str) or not RATIONAL.fullmatch(text):
        raise ValueError(f"not an exact rational string: {text!r}")
    return Fraction(text)


def object_without_duplicate_keys(pairs):
    """Build a JSON object while refusing duplicate member names.

    JSON permits a repeated key and Python's decoder keeps the last one, so a
    file could carry two values for `n` and be read as whichever was written
    second. A checker must not have a hidden second answer.
    """
    result = {}
    for key, value in pairs:
        if key in result:
            raise CertificateFormatError(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def reject_inexact_json_number(text):
    """Refuse JSON decimals and non-finite constants before they become floats."""
    raise CertificateFormatError(f"inexact JSON number {text!r}; use an exact rational string")


def required(record, key):
    if key not in record:
        raise CertificateFormatError(f"missing required field {key!r}")
    return record[key]


def exact_integer(record, key):
    """`int()` truncates, and a truncated n or K would decide a different theorem.

    A file saying `"n": 11.9` must be refused, not quietly read as eleven, and
    bool is a subclass of int, so `isinstance(value, int)` is deliberately not
    the test used here: `true` is not a direction count.
    """
    value = required(record, key)
    if type(value) is not int:
        raise CertificateFormatError(f"field {key!r} must be a JSON integer, got {value!r}")
    return value


def exact_rational(record, key):
    value = required(record, key)
    try:
        return rational(value)
    except ValueError as error:
        raise CertificateFormatError(f"field {key!r}: {error}") from None


def load(path):
    try:
        with Path(path).open(encoding="utf-8") as handle:
            record = json.load(
                handle,
                object_pairs_hook=object_without_duplicate_keys,
                parse_float=reject_inexact_json_number,
                parse_constant=reject_inexact_json_number,
            )
    except CertificateFormatError:
        raise
    except (UnicodeError, ValueError, RecursionError) as error:
        raise CertificateFormatError(str(error)) from None
    if not isinstance(record, dict):
        raise CertificateFormatError("top-level JSON value must be an object")

    n = exact_integer(record, "n")
    steps = exact_integer(record, "direction_steps")
    if steps < 1:
        raise CertificateFormatError("field 'direction_steps' must be at least 1")
    limit = exact_rational(record, "angle_limit")

    atoms_record = required(record, "atoms")
    if not isinstance(atoms_record, list):
        raise CertificateFormatError("field 'atoms' must be a JSON array")
    atoms = []
    for index, atom in enumerate(atoms_record):
        # The row's shape is settled before any atom[j] access, so a short row
        # is refused by name here rather than escaping as an IndexError from
        # inside a condition.
        if not isinstance(atom, list) or len(atom) != 3:
            raise CertificateFormatError(f"atoms[{index}] must be a three-element JSON array")
        parsed = []
        for position, value in enumerate(atom):
            try:
                parsed.append(rational(value))
            except ValueError as error:
                raise CertificateFormatError(f"atoms[{index}][{position}]: {error}") from None
        atoms.append(tuple(parsed))

    # The bookkeeping fields are optional, but a file that declares one must
    # write it in the exact form everything else is written in; `decide`
    # recomputes it and refuses a disagreement.
    for key in ("total_mass", "least_cell_mass"):
        if key in record:
            try:
                rational(record[key])
            except ValueError as error:
                raise CertificateFormatError(f"field {key!r}: {error}") from None
    for key in ("id", "claim"):
        if key in record and not isinstance(record[key], str):
            raise CertificateFormatError(f"field {key!r} must be a string")

    return {
        "id": record.get("id", "?"),
        "n": n,
        "L": exact_rational(record, "outer_side"),
        "B": exact_rational(record, "square_side"),
        # The net is fixed by two numbers, T and K: t_k = T k / K. That is
        # Massaccesi's parametrisation, and it keeps every direction rational.
        "tangents": [limit * k / steps for k in range(steps + 1)],
        "atoms": atoms,
        "declared": record,
    }


# ---------------------------------------------------------------------------
# Preconditions: the shape the theorem assumes before Condition 1 to Condition 5
# mean anything.
# ---------------------------------------------------------------------------


def preconditions(cert):
    n, L, B, tangents, atoms = cert["n"], cert["L"], cert["B"], cert["tangents"], cert["atoms"]
    checks = []
    checks.append(
        (
            "P1 n >= 1, L > 0, B > 0",
            f"n = {n}, L = {L}, B = {B}",
            n >= 1 and L > 0 and B > 0,
        )
    )
    # The counting step of the proof needs every atom to contribute at most
    # its own weight to at most one square; a negative weight would let a
    # square gain mass by covering less.
    # `load` refuses a malformed row, but `decide` is also called on objects
    # built in code, so P2 must not index a row whose shape it has not checked.
    triples = all(isinstance(atom, (list, tuple)) and len(atom) == 3 for atom in atoms)
    negative = [atom for atom in atoms if atom[2] < 0] if triples else []
    checks.append(
        (
            "P2 every weight is non-negative",
            f"{len(atoms)} atoms, {len(negative)} negative"
            + ("" if triples else " (malformed rows)"),
            triples and not negative and len(atoms) > 0,
        )
    )
    # The net must start at angle 0 and increase, so that every orientation
    # in [0, pi/4] lies between two adjacent net angles (with Condition 3 closing the
    # top). Each atom triple must have exactly three entries.
    increasing = all(a < b for a, b in pairwise(tangents))
    checks.append(
        (
            "P3 net starts at 0 and is strictly increasing",
            f"t_0 = {tangents[0]}, K = {len(tangents) - 1}, t_K = {tangents[-1]}",
            tangents[0] == 0 and increasing and len(tangents) >= 2,
        )
    )
    checks.append(("P4 every atom is an (x, y, weight) triple", f"{len(atoms)} atoms", triples))
    # The file's own statement of what it proves must be the theorem's
    # conclusion for its n and L, so a reader cannot be misled by the label.
    expected = f"s({n}) >= {L}"
    claimed = str(cert["declared"].get("claim", ""))
    checks.append(
        (
            "P5 the declared claim is the theorem's conclusion",
            f"declared {claimed!r}, theorem gives {expected!r}",
            claimed == expected,
        )
    )
    # These are certificate-format requirements shared with the other standalone
    # verifiers. The theorem would allow repeated sites and outside atoms, but a
    # well-formed record lists each site once and keeps its support in the container.
    sites = {(x, y) for x, y, _w in atoms} if triples else set()
    checks.append(
        (
            "P6 every atom has a distinct site",
            f"{len(atoms)} atoms on {len(sites)} distinct sites",
            triples and len(sites) == len(atoms),
        )
    )
    outside = [site for site in sites if not (0 <= site[0] <= L and 0 <= site[1] <= L)]
    checks.append(
        (
            "P7 every atom lies in [0, L]^2",
            f"{len(outside)} sites outside the container",
            triples and not outside,
        )
    )
    return checks


# ---------------------------------------------------------------------------
# Condition 1 - Condition 4: closed-form conditions.
# ---------------------------------------------------------------------------


def symmetry_images(x, y, L):
    """The eight images of a point under the symmetry group of [0, L]^2."""
    fx, fy = L - x, L - y
    return [(x, y), (fx, y), (x, fy), (fx, fy), (y, x), (fy, x), (y, fx), (fy, fx)]


def condition_1(cert):
    L = cert["L"]
    weight = {(x, y): w for x, y, w in cert["atoms"]}  # P6 refuses repeated sites
    # Each map is a bijection of the plane whose inverse is also in the
    # group, so "every site's image carries the site's weight" is the whole
    # of invariance: the support maps onto itself with weights preserved.
    for site, w in weight.items():
        for image in symmetry_images(site[0], site[1], L):
            if weight.get(image) != w:
                return (
                    "Condition 1 atoms invariant under the container's symmetries",
                    f"site {site} has weight {w} but its image {image} has {weight.get(image)}",
                    False,
                )
    return (
        "Condition 1 atoms invariant under the container's symmetries",
        (
            f"{len(cert['atoms'])} atoms on {len(weight)} distinct sites, "
            "all eight maps preserve the weights"
        ),
        True,
    )


def condition_2(cert):
    total = sum((w for _, _, w in cert["atoms"]), Fraction(0))
    return (
        "Condition 2 total weight below n",
        f"total {total} = {float(total):.6f} against n = {cert['n']}",
        total < cert["n"],
    )


def condition_3(cert):
    # tan(pi/8) = sqrt(2) - 1 is the positive root of t^2 + 2t - 1, and the
    # polynomial is increasing for t >= 0, so t_K >= tan(pi/8) is exactly
    # t_K^2 + 2 t_K - 1 >= 0. No irrational number is ever evaluated.
    last = cert["tangents"][-1]
    slack = last * last + 2 * last - 1
    return (
        "Condition 3 net reaches pi/4",
        f"t_K = {last}, t_K^2 + 2 t_K - 1 = {slack}",
        slack >= 0,
    )


def largest_half_gap_tangent(tangents):
    # theta = 2 arctan t, so half the gap between adjacent net angles is
    # arctan(t2) - arctan(t1), whose tangent is (t2 - t1) / (1 + t1 t2).
    return max((b - a) / (1 + a * b) for a, b in pairwise(tangents))


def condition_4(cert):
    D = largest_half_gap_tangent(cert["tangents"])
    product = cert["B"] * (1 + D)
    return (
        "Condition 4 containment B(1 + D) < 1",
        f"D = {D}, B(1 + D) = {product} = {float(product):.12f}",
        product < 1,
    )


# ---------------------------------------------------------------------------
# Condition 5: the least weight any admissible placement covers, at one direction.
#
# Fix a net direction with exact cosine c and sine s (c^2 + s^2 = 1). Rotate
# the plane so the placed square is axis-parallel: u = c x + s y and
# v = -s x + c y. A closed B-square centred at (U, V) covers the atom at
# (u_k, v_k) iff |u_k - U| <= B/2 and |v_k - V| <= B/2. So the covered
# weight, as a function of the centre (U, V), is a sum of indicator
# functions of closed axis-parallel boxes, one per atom.
#
# The square lies inside [0, L]^2 iff its centre (X, Y) satisfies
# h <= X <= L - h and h <= Y <= L - h with h = B (|c| + |s|) / 2, because
# the square's extent along each axis is exactly h on either side of its
# centre. Call that closed square of centres F; in (U, V) coordinates it is
# a rotated square with four exactly known corners.
#
# WHY A FINITE ENUMERATION DECIDES THE CONTINUUM. Let the "breakpoints" be
# the values u_k +- B/2 (sorted, distinct) and v_k +- B/2 likewise. They cut
# the plane into a grid; call the open rectangles between consecutive
# breakpoints the open cells (the outermost ones are unbounded).
#   (a) On an open cell the covered weight is constant: each atom's box has
#       its edges on breakpoint lines, so it either contains the whole cell
#       or misses it.
#   (b) A point q on the boundary of an open cell C covers at least what C
#       covers: every atom box containing a point of C is closed and has
#       edges on breakpoint lines, so it contains the closure of C, hence q.
#   (c) F is a closed square of positive side (checked: 2h < L), so every
#       point q of F has interior points of F arbitrarily near. A small
#       enough ball around q meets only cells whose closure contains q, and
#       its intersection with the interior of F is a non-empty open set,
#       which cannot lie inside finitely many lines; so some open cell C
#       adjacent to q meets F, and by (b) mass(q) >= mass(C).
#   (d) Hence the minimum of the covered weight over F equals the minimum of
#       mass(C) over the open cells C that meet F, and it is attained at
#       every point of C's intersection with F. Boundary points of cells,
#       where the closed-square convention counts the most, never need to be
#       visited: they can only carry more.
#   (e) Whether an open cell (a, b) x (c', d) meets F is decided exactly:
#       the open strip a < U < b meets F iff a < U_max and U_min < b, where
#       [U_min, U_max] is F's projection on the U axis; then F within the
#       closed strip a <= U <= b projects on the V axis to a closed interval
#       [lo, hi] with lo < hi (the strip contains interior points of F), the
#       open strip's projection is squeezed between (lo, hi) and [lo, hi],
#       and an open interval (c', d) meets it iff c' < hi and lo < d.
#       [lo, hi] comes from clipping the polygon F to the strip, which is
#       exact in rationals.
# Every open cell that meets F is scored, none is sampled, and the weight on
# a cell is computed exactly by a two-dimensional prefix sum over integer
# weights (the rational weights multiplied by their common denominator).
# ---------------------------------------------------------------------------


def clip(polygon, axis, bound, keep_greater):
    """Sutherland-Hodgman: the part of a convex polygon on one side of a line.

    Keeps the points with coordinate[axis] >= bound (or <= bound). Exact: the
    crossing point of an edge with the line is a rational combination of the
    edge's ends. The result may repeat a vertex; nothing below minds.
    """
    output = []
    previous = polygon[-1]
    previous_inside = previous[axis] >= bound if keep_greater else previous[axis] <= bound
    for current in polygon:
        current_inside = current[axis] >= bound if keep_greater else current[axis] <= bound
        if current_inside != previous_inside:
            # Exactly one end is on the kept side, so the coordinates differ
            # along `axis` and the division is safe.
            fraction = (bound - previous[axis]) / (current[axis] - previous[axis])
            crossing = tuple(
                p + fraction * (q - p) for p, q in zip(previous, current, strict=True)
            )
            output.append(crossing)
        if current_inside:
            output.append(current)
        previous, previous_inside = current, current_inside
    return output


def clip_to_box(polygon, u_low, u_high, v_low, v_high):
    """The polygon within [u_low, u_high] x [v_low, v_high]; None means no bound."""
    for axis, bound, keep_greater in (
        (0, u_low, True),
        (0, u_high, False),
        (1, v_low, True),
        (1, v_high, False),
    ):
        if bound is not None and polygon:
            polygon = clip(polygon, axis, bound, keep_greater)
    return polygon


def direction(t):
    """The exact rotation by 2 arctan(t): cosine and sine with c^2 + s^2 = 1."""
    denominator = 1 + t * t
    c, s = (1 - t * t) / denominator, 2 * t / denominator
    assert c * c + s * s == 1
    return c, s


def covered_weight_at(cert, c, s, X, Y):
    """Direct summation: the weight inside the closed B-square centred at (X, Y).

    Independent of the grid machinery below, so a witness cell's weight is
    confirmed atom by atom, in the original coordinates.
    """
    half = cert["B"] / 2
    total = Fraction(0)
    for x, y, w in cert["atoms"]:
        along = c * (x - X) + s * (y - Y)
        across = -s * (x - X) + c * (y - Y)
        if -half <= along <= half and -half <= across <= half:
            total += w
    return total


def least_covered_weight(cert, c, s, integer_weights, scale, *, audit=0, rng=None):
    """Exact minimum covered weight over every admissible centre at one direction.

    Returns (minimum as a Fraction, witness centre (X, Y), number of cells).
    The witness is a point of the container at which a B-square at this
    direction fits and covers exactly the minimum; its weight is recomputed
    by direct summation before it is returned.

    If no B-square at this direction fits inside the container, there is
    nothing to minimise over: the minimum and the witness are both None and
    the caller reports Condition 5 vacuously satisfied here. See the note on
    the empty case below for why that is sound rather than convenient.
    """
    L, B, atoms = cert["L"], cert["B"], cert["atoms"]
    half = B / 2

    # The feasible centres in original coordinates are [h, L-h]^2, where 2h is
    # the width of the B-square's bounding box at this direction. The open-cell
    # argument below assumes that set has an interior, so its two degenerate
    # shapes are settled first.
    #
    # 2h > L: the set is empty and Condition 5 here quantifies over nothing, so
    # it holds vacuously. That is an acceptance, and it is worth saying why it
    # is sound and not merely convenient. Condition 5 is a hypothesis of the
    # theorem, and the theorem's proof only ever applies it to a B-square that
    # it has already placed strictly inside a unit square inside the container;
    # if no B-square at this direction fits in the container at all, then no
    # unit square containing one fits either, and the proof never reaches this
    # direction. Vacuous truth of the hypothesis is therefore the honest
    # reading, and the resulting bound is still proved. The cost of saying so
    # is real all the same: this checker's value is that it refuses what it
    # cannot handle, and a direction it accepts on vacuity is a direction where
    # it decided nothing. `condition_5` counts those and says how many, and a
    # certificate whose every direction is vacuous is reported as such rather
    # than as a decision.
    #
    # 2h == L: exactly one admissible centre. Closed-square containment must be
    # evaluated at that point directly, because the open-cell argument has no
    # open cell to reason about.
    h = B * (abs(c) + abs(s)) / 2
    if 2 * h > L:
        return None, None, 0
    if 2 * h == L:
        centre = (L / 2, L / 2)
        return covered_weight_at(cert, c, s, *centre), centre, 1

    us = [c * x + s * y for x, y, _ in atoms]
    vs = [-s * x + c * y for x, y, _ in atoms]
    u_breaks = sorted({u - half for u in us} | {u + half for u in us})
    v_breaks = sorted({v - half for v in vs} | {v + half for v in vs})
    u_index = {value: i for i, value in enumerate(u_breaks)}
    v_index = {value: j for j, value in enumerate(v_breaks)}

    # Open cell (i, j) is (u_breaks[i-1], u_breaks[i]) x (v_breaks[j-1], v_breaks[j]),
    # with i = 0 and i = len(u_breaks) the unbounded pieces (likewise j).
    # Atom k covers the cells i in [u_index(u_k - B/2) + 1, u_index(u_k + B/2)]
    # and j likewise: a rectangle of cells, entered into a difference array
    # and turned into weights by two prefix-sum passes.
    rows, columns = len(u_breaks) + 2, len(v_breaks) + 2
    grid = [[0] * columns for _ in range(rows)]
    for k in range(len(atoms)):
        w = integer_weights[k]
        r0, r1 = u_index[us[k] - half] + 1, u_index[us[k] + half] + 1
        c0, c1 = v_index[vs[k] - half] + 1, v_index[vs[k] + half] + 1
        grid[r0][c0] += w
        grid[r0][c1] -= w
        grid[r1][c0] -= w
        grid[r1][c1] += w
    for i in range(rows):
        grid[i] = list(accumulate(grid[i]))
    for i in range(1, rows):
        grid[i] = list(map(add, grid[i - 1], grid[i]))  # noqa: B912 - map(strict=) is 3.14-only; rows are equal by construction

    # The admissible centres, as a polygon in (U, V) coordinates. Both
    # degenerate shapes were returned above, so this polygon has an interior.
    corners = [(h, h), (L - h, h), (L - h, L - h), (h, L - h)]
    F = [(c * x + s * y, -s * x + c * y) for x, y in corners]
    u_min, u_max = min(u for u, _ in F), max(u for u, _ in F)

    best, best_cell, cells, feasible_rows = None, None, 0, []
    for i in range(len(u_breaks) + 1):
        a = u_breaks[i - 1] if i > 0 else None
        b = u_breaks[i] if i < len(u_breaks) else None
        if (a is not None and a >= u_max) or (b is not None and b <= u_min):
            continue
        strip = clip_to_box(F, a, b, None, None)
        lo, hi = min(v for _, v in strip), max(v for _, v in strip)
        assert lo < hi
        j0, j1 = bisect_right(v_breaks, lo), bisect_left(v_breaks, hi)
        assert j0 <= j1
        row = grid[i]
        row_minimum = min(row[j0 : j1 + 1])
        cells += j1 - j0 + 1
        feasible_rows.append((i, j0, j1))
        if best is None or row_minimum < best:
            # list.index with bounds returns the absolute position, not an
            # offset from j0.
            best, best_cell = row_minimum, (i, row.index(row_minimum, j0, j1 + 1))
    if best is None or best_cell is None:
        raise AssertionError("an admissible region was found but no cell was scored")

    def witness(i, j):
        # A point of the open cell that is also in F: the vertex average of
        # F clipped to the cell's closure lies in the interior of that
        # clipped polygon, which is the open cell's intersection with the
        # interior of F.
        box = clip_to_box(
            F,
            u_breaks[i - 1] if i > 0 else None,
            u_breaks[i] if i < len(u_breaks) else None,
            v_breaks[j - 1] if j > 0 else None,
            v_breaks[j] if j < len(v_breaks) else None,
        )
        U = sum(u for u, _ in box) / len(box)
        V = sum(v for _, v in box) / len(box)
        # Both halves of that claim are checked, not only the second. The cell's
        # midpoint would not do here: a cell can meet F while its midpoint lies
        # outside F, and a sum taken there confirms the cell's constant weight
        # without exhibiting a placement that attains it.
        assert i == 0 or u_breaks[i - 1] < U
        assert i == len(u_breaks) or u_breaks[i] > U
        assert j == 0 or v_breaks[j - 1] < V
        assert j == len(v_breaks) or v_breaks[j] > V
        X, Y = c * U - s * V, s * U + c * V
        assert h <= X <= L - h
        assert h <= Y <= L - h
        return X, Y

    X, Y = witness(*best_cell)
    direct = covered_weight_at(cert, c, s, X, Y)
    if direct != Fraction(best, scale):
        raise AssertionError(
            f"grid weight {Fraction(best, scale)} disagrees with direct summation {direct}"
        )
    # Optional audit: re-sum a few random admissible cells directly.
    if audit:
        if rng is None:
            raise AssertionError("an audit needs the caller's random source")
        for _ in range(audit):
            i, j0, j1 = rng.choice(feasible_rows)
            j = rng.randint(j0, j1)
            Xa, Ya = witness(i, j)
            if covered_weight_at(cert, c, s, Xa, Ya) != Fraction(grid[i][j], scale):
                raise AssertionError(f"audit: cell ({i}, {j}) disagrees with direct summation")
    return Fraction(best, scale), (X, Y), cells


def condition_5(cert, *, audit=0, verbose=False, log=print):
    weights = [w for _, _, w in cert["atoms"]]
    scale = 1
    for w in weights:
        scale = scale * w.denominator // gcd(scale, w.denominator)
    integer_weights = [int(w * scale) for w in weights]
    rng = random.Random(0)
    worst, total_cells, vacuous, started = None, 0, 0, time.time()
    K = len(cert["tangents"]) - 1
    for k, t in enumerate(cert["tangents"]):
        c, s = direction(t)
        minimum, centre, cells = least_covered_weight(
            cert, c, s, integer_weights, scale, audit=audit, rng=rng
        )
        total_cells += cells
        if minimum is None or centre is None:
            # No B-square fits here, so there is nothing to minimise over.
            vacuous += 1
            if verbose or k % 30 == 0 or k == K:
                log(
                    f"    direction {k:3d}/{K}  t = {t!s:<18} no admissible placement;"
                    f" nothing decided  running least {'-' if worst is None else worst[0]}"
                )
            continue
        if worst is None or minimum < worst[0]:
            worst = (minimum, k, t, centre)
        if verbose or k % 30 == 0 or k == K:
            log(
                f"    direction {k:3d}/{K}  t = {t!s:<18} cells {cells:7d}  "
                f"least weight {minimum} = {float(minimum):.6f}  running least {worst[0]}"
            )
    if worst is None:
        # Every direction was vacuous. The condition holds, and the honest
        # report is that nothing was decided rather than that something passed.
        detail = (
            f"no admissible placement at any of {K + 1} directions, so the condition is"
            f" vacuous and nothing was decided; {time.time() - started:.1f} s"
        )
        return ("Condition 5 every admissible placement covers weight >= 1", detail, True), None
    minimum, k, t, (X, Y) = worst
    detail = (
        f"least covered weight {minimum} = {float(minimum):.6f} at direction {k} (t = {t}), "
        f"centre ({X}, {Y}) ~ ({float(X):.6f}, {float(Y):.6f}); "
        f"{total_cells} cells over {K + 1} directions in {time.time() - started:.1f} s"
    )
    if vacuous:
        detail += f"; {vacuous} of those directions admitted no placement and decided nothing"
    return (
        "Condition 5 every admissible placement covers weight >= 1",
        detail,
        minimum >= 1,
    ), worst


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# ---------------------------------------------------------------------------
# The verdict.
# ---------------------------------------------------------------------------


def decide(cert, *, audit=0, verbose=False, log=print):
    """Run every check, print each with its numbers, and return the outcome.

    Nothing short-circuits: a certificate that fails Condition 2 still has its
    Condition 5 minimum computed and printed, so a refusal names every failing
    condition.
    Returns (accepted, results) where results maps a check's name to
    (detail, holds), plus the least covered weight under the key "minimum"
    and the placement that attains it, (k, t, X, Y), under "witness".
    The verdict is computed from the list of checks, never from the dict.
    """
    declared = cert["declared"]
    log("certificate {}".format(cert["id"]))
    log(
        f"  n = {cert['n']}, L = {cert['L']} = {float(cert['L']):.6f}, B = {cert['B']}, "
        f"net t_k = {declared['angle_limit']} * k / {len(cert['tangents']) - 1} "
        f"for k = 0..{len(cert['tangents']) - 1}, {len(cert['atoms'])} atoms"
    )
    results, verdicts = {}, []

    def record(name, detail, holds):
        verdicts.append((name, holds))
        results[name] = (detail, holds)
        log("  {}  {} | {}".format("PASS" if holds else "FAIL", name, detail))

    for name, detail, holds in preconditions(cert):
        record(name, detail, holds)
    if not all(holds for _, holds in verdicts):
        log("REFUSED: the file is not a certificate of the expected shape")
        return False, results
    for check in (condition_1, condition_2, condition_3, condition_4):
        record(*check(cert))
    log("  Condition 5: sweeping every net direction")
    (name, detail, holds), worst = condition_5(cert, audit=audit, verbose=verbose, log=log)
    record(name, detail, holds)
    if worst is None:
        minimum = None
        results["minimum"] = None
        results["witness"] = None
    else:
        minimum, k, t, (X, Y) = worst
        results["minimum"] = minimum
        results["witness"] = (k, t, X, Y)
    # The theorem does not use the record's own bookkeeping, but an artifact
    # that declares a value has to agree with its replay: a file whose stated
    # least covered mass is not the one recomputed here is wrong about itself,
    # whatever the conditions say. These failures are kept in their own list so
    # that the mathematical verdict and the record-integrity verdict stay
    # legible, and both are counted before anything is accepted.
    declaration_failures = []
    total = sum((w for _, _, w in cert["atoms"]), Fraction(0))
    for key, value in (("total_mass", total), ("least_cell_mass", minimum)):
        if key in declared:
            if value is None:
                agrees, replay = False, "nothing (no direction admitted a placement)"
            else:
                agrees, replay = rational(declared[key]) == value, str(value)
            log(
                "  {}  declared {} {} {} recomputed {}".format(
                    "info" if agrees else "FAIL",
                    key,
                    declared[key],
                    "==" if agrees else "!=",
                    replay,
                )
            )
            if not agrees:
                declaration_failures.append(f"declared {key} disagrees with the replay")
    failures = [name for name, holds in verdicts if not holds] + declaration_failures
    if failures:
        log("REFUSED: {}".format(", ".join(failures)))
        return False, results
    log(f"VERIFIED: s({cert['n']}) >= {cert['L']} = {float(cert['L']):.6f}")
    return True, results


def main(argv: Sequence[str] | None = None) -> int:  # noqa: PLR0911 - each usage error returns 2 where it is found
    arguments = list(sys.argv[1:] if argv is None else argv)
    if not arguments or arguments[0].startswith("-"):
        print(__doc__)
        return 2
    path = arguments[0]
    audit, verbose = 0, False
    rest = arguments[1:]
    while rest:
        flag = rest.pop(0)
        if flag == "--audit":
            if not rest:
                print("--audit requires a non-negative integer")
                return 2
            try:
                audit = int(rest.pop(0))
            except ValueError:
                print("--audit requires a non-negative integer")
                return 2
            if audit < 0:
                print("--audit requires a non-negative integer")
                return 2
        elif flag == "--verbose":
            verbose = True
        else:
            print(f"unknown option {flag}")
            return 2
    print(f"python {sys.version.split()[0]}")
    try:
        cert = load(path)
    except OSError as error:
        # Not a refusal: the file was never read. Usage status, not verdict status.
        print(f"could not open {path}: {error}")
        return 2
    except CertificateFormatError as error:
        # A malformed rational, a zero `direction_steps`, a duplicate key and a
        # short atom row all arrive here, and all as one type. This file promises
        # a labelled refusal for any form other than the one the theorem assumes,
        # and a traceback is not one.
        print(f"REFUSED: not a certificate of the expected shape: {error}")
        return 1
    accepted, _ = decide(cert, audit=audit, verbose=verbose)
    return 0 if accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
