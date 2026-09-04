#!/usr/bin/env python3
"""Decide a weighted fractional unavoidable-set certificate for s(n) >= L.

Usage:
    python3 verify.py CERTIFICATE.json [--audit N] [--verbose]

Standard library only: fractions, json, bisect, itertools, operator, random,
re, sys, time. Any CPython 3.8 or later. Nothing here imports numpy or any
file from the repository this ships with, so the decision rests on Python's
arbitrary-precision integers and on the reader's check of this file against
the theorem in README.md.

Every quantity that decides anything is a fractions.Fraction. Floats appear
only inside f-strings that print approximations next to the exact value.

THE THEOREM (README.md states it in full, with the proof). A certificate
names n, a container side L, a shrunken side B, a direction net of
half-angle tangents t_k = T k / K (k = 0..K), and weighted atoms (x, y, w).
Write theta_k = 2 arctan(t_k). If

  C0  the weighted atom set is invariant under the eight symmetries of the
      container [0, L]^2 (the proof uses one of them, the reflection in the
      diagonal, so this is a stronger hypothesis than needed);
  C1  the total weight is strictly less than n;
  C2  theta_K >= pi/4, decided as t_K^2 + 2 t_K - 1 >= 0;
  C3  B (1 + D) < 1, where D = max_k (t_{k+1} - t_k) / (1 + t_k t_{k+1}) is
      the largest tangent of HALF a gap between adjacent net angles;
  C4  every closed square of side B at a net angle theta_k that lies inside
      [0, L]^2 covers atoms of total weight at least 1;

then n unit squares with pairwise disjoint interiors do not fit in [0, L]^2,
and therefore s(n) >= L.

RUNTIME. C4 is the only expensive condition. Measured on one idle core with
CPython 3.10 through 3.14: 22 to 27 s for the n = 11 certificate (425 atoms,
181 directions, 90.5 million cells in all) and 7 to 8 s for the n = 17
control (168 atoms, 16.6 million cells); up to about twice that on a
contended machine. Memory stays under 100 MB.
"""

import json
import random
import re
import sys
import time
from bisect import bisect_left, bisect_right
from fractions import Fraction
from itertools import accumulate
from operator import add

RATIONAL = re.compile(r"^-?[0-9]+(/[1-9][0-9]*)?$")


class CertificateFormatError(ValueError):
    """The JSON cannot be interpreted as an exact certificate record."""


# ---------------------------------------------------------------------------
# Loading. The JSON carries exact rationals as strings ("p/q" or "p"); the
# regex refuses anything else, so a decimal or a float cannot slip in and be
# silently rounded.
# ---------------------------------------------------------------------------


def rational(text):
    if not isinstance(text, str) or not RATIONAL.fullmatch(text):
        raise ValueError("not an exact rational string: %r" % (text,))
    return Fraction(text)


def object_without_duplicate_keys(pairs):
    """Build a JSON object while refusing duplicate member names."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise CertificateFormatError("duplicate JSON object key %r" % key)
        result[key] = value
    return result


def reject_inexact_json_number(text):
    """Reject JSON decimals and non-finite constants before they become floats."""
    raise CertificateFormatError("inexact JSON number %r; use an exact rational string" % text)


def required(record, key):
    if key not in record:
        raise CertificateFormatError("missing required field %r" % key)
    return record[key]


def exact_integer(record, key):
    value = required(record, key)
    # bool is a subclass of int, so isinstance(value, int) is deliberately
    # insufficient here.  Converting with int(...) would also accept strings
    # and truncate JSON floats.
    if type(value) is not int:
        raise CertificateFormatError("field %r must be a JSON integer, got %r" % (key, value))
    return value


def exact_rational(record, key):
    value = required(record, key)
    try:
        return rational(value)
    except ValueError as error:
        raise CertificateFormatError("field %r: %s" % (key, error)) from None


def load(path):
    try:
        with open(path, encoding="utf-8") as handle:
            record = json.load(
                handle,
                object_pairs_hook=object_without_duplicate_keys,
                parse_float=reject_inexact_json_number,
                parse_constant=reject_inexact_json_number,
            )
    except CertificateFormatError:
        raise
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
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
    for i, atom in enumerate(atoms_record):
        # Establish the tuple shape before any atom[j] access.  Besides making
        # the error useful, this prevents malformed input from escaping as an
        # IndexError later in preconditions().
        if not isinstance(atom, list) or len(atom) != 3:
            raise CertificateFormatError("atoms[%d] must be a three-element JSON array" % i)
        parsed = []
        for j, value in enumerate(atom):
            try:
                parsed.append(rational(value))
            except ValueError as error:
                raise CertificateFormatError("atoms[%d][%d]: %s" % (i, j, error)) from None
        atoms.append(tuple(parsed))

    for key in ("total_mass", "least_cell_mass"):
        if key in record:
            try:
                rational(record[key])
            except ValueError as error:
                raise CertificateFormatError("field %r: %s" % (key, error)) from None
    for key in ("id", "claim"):
        if key in record and not isinstance(record[key], str):
            raise CertificateFormatError("field %r must be a string" % key)

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
# Preconditions: the shape the theorem assumes before C0-C4 mean anything.
# ---------------------------------------------------------------------------


def preconditions(cert):
    n, L, B, tangents, atoms = cert["n"], cert["L"], cert["B"], cert["tangents"], cert["atoms"]
    checks = []
    checks.append(("P1 n >= 1, L > 0, B > 0",
                   "n = %d, L = %s, B = %s" % (n, L, B),
                   n >= 1 and L > 0 and B > 0))
    # The counting step of the proof needs every atom to contribute at most
    # its own weight to at most one square; a negative weight would let a
    # square gain mass by covering less.
    triples = all(isinstance(atom, (list, tuple)) and len(atom) == 3 for atom in atoms)
    negative = [atom for atom in atoms if atom[2] < 0] if triples else []
    checks.append(("P2 every weight is non-negative",
                   "%d atoms, %d negative%s"
                   % (len(atoms), len(negative), " (malformed tuples)" if not triples else ""),
                   triples and not negative and len(atoms) > 0))
    # The net must start at angle 0 and increase, so that every orientation
    # in [0, pi/4] lies between two adjacent net angles (with C2 closing the
    # top). Each atom triple must have exactly three entries.
    increasing = all(a < b for a, b in zip(tangents, tangents[1:]))
    checks.append(("P3 net starts at 0 and is strictly increasing",
                   "t_0 = %s, K = %d, t_K = %s" % (tangents[0], len(tangents) - 1, tangents[-1]),
                   tangents[0] == 0 and increasing and len(tangents) >= 2))
    checks.append(("P4 every atom is an (x, y, weight) triple",
                   "%d atoms" % len(atoms),
                   triples))
    # The file's own statement of what it proves must be the theorem's
    # conclusion for its n and L, so a reader cannot be misled by the label.
    expected = "s(%d) >= %s" % (n, L)
    claimed = str(cert["declared"].get("claim", ""))
    checks.append(("P5 the declared claim is the theorem's conclusion",
                   "declared %r, theorem gives %r" % (claimed, expected),
                   claimed == expected))
    return checks


# ---------------------------------------------------------------------------
# C0 - C3: closed-form conditions.
# ---------------------------------------------------------------------------


def symmetry_images(x, y, L):
    """The eight images of a point under the symmetry group of [0, L]^2."""
    fx, fy = L - x, L - y
    return [(x, y), (fx, y), (x, fy), (fx, fy), (y, x), (fy, x), (y, fx), (fy, fx)]


def condition_c0(cert):
    L = cert["L"]
    weight = {}
    for x, y, w in cert["atoms"]:
        weight[(x, y)] = weight.get((x, y), Fraction(0)) + w
    # Each map is a bijection of the plane whose inverse is also in the
    # group, so "every site's image carries the site's weight" is the whole
    # of invariance: the support maps onto itself with weights preserved.
    for site, w in weight.items():
        for image in symmetry_images(site[0], site[1], L):
            if weight.get(image) != w:
                return ("C0 atoms invariant under the container's symmetries",
                        "site %s has weight %s but its image %s has %s"
                        % (site, w, image, weight.get(image)), False)
    return ("C0 atoms invariant under the container's symmetries",
            "%d atoms on %d distinct sites, all eight maps preserve the weights"
            % (len(cert["atoms"]), len(weight)), True)


def condition_c1(cert):
    total = sum((w for _, _, w in cert["atoms"]), Fraction(0))
    return ("C1 total weight below n",
            "total %s = %.6f against n = %d" % (total, float(total), cert["n"]),
            total < cert["n"])


def condition_c2(cert):
    # tan(pi/8) = sqrt(2) - 1 is the positive root of t^2 + 2t - 1, and the
    # polynomial is increasing for t >= 0, so t_K >= tan(pi/8) is exactly
    # t_K^2 + 2 t_K - 1 >= 0. No irrational number is ever evaluated.
    last = cert["tangents"][-1]
    slack = last * last + 2 * last - 1
    return ("C2 net reaches pi/4",
            "t_K = %s, t_K^2 + 2 t_K - 1 = %s" % (last, slack),
            slack >= 0)


def largest_half_gap_tangent(tangents):
    # theta = 2 arctan t, so half the gap between adjacent net angles is
    # arctan(t2) - arctan(t1), whose tangent is (t2 - t1) / (1 + t1 t2).
    return max((b - a) / (1 + a * b) for a, b in zip(tangents, tangents[1:]))


def condition_c3(cert):
    D = largest_half_gap_tangent(cert["tangents"])
    product = cert["B"] * (1 + D)
    return ("C3 containment B(1 + D) < 1",
            "D = %s, B(1 + D) = %s = %.12f" % (D, product, float(product)),
            product < 1)


# ---------------------------------------------------------------------------
# C4: the least weight any admissible placement covers, at one direction.
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
            crossing = tuple(p + fraction * (q - p) for p, q in zip(previous, current))
            output.append(crossing)
        if current_inside:
            output.append(current)
        previous, previous_inside = current, current_inside
    return output


def clip_to_box(polygon, u_low, u_high, v_low, v_high):
    """The polygon within [u_low, u_high] x [v_low, v_high]; None means no bound."""
    for axis, bound, keep_greater in ((0, u_low, True), (0, u_high, False),
                                      (1, v_low, True), (1, v_high, False)):
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


def least_covered_weight(cert, c, s, integer_weights, scale, audit=0, rng=None):
    """Exact minimum covered weight over every admissible centre at one direction.

    Returns (minimum, witness centre (X, Y), number of regions evaluated).
    If the feasible set is empty, minimum and witness are both None.  If it
    is a singleton, the one centre is evaluated directly.  Otherwise the
    minimum is a Fraction attained at the returned witness and is recomputed
    by direct summation before it is returned.
    """
    L, B, atoms = cert["L"], cert["B"], cert["atoms"]
    half = B / 2

    # In original coordinates the feasible-centre set is
    # [h, L-h] x [h, L-h].  Separate its lower-dimensional cases before the
    # open-cell argument, which assumes a non-empty interior.  With 2h > L
    # there are no placements and the universal C4 statement is vacuous.  At
    # 2h == L there is exactly one centre, so closed-square containment must
    # be evaluated there directly (grid-cell limits cannot substitute for it).
    h = B * (abs(c) + abs(s)) / 2
    if 2 * h > L:
        return None, None, 0
    if 2 * h == L:
        centre = (L / 2, L / 2)
        return covered_weight_at(cert, c, s, *centre), centre, 1

    us = [c * x + s * y for x, y, _ in atoms]
    vs = [-s * x + c * y for x, y, _ in atoms]
    u_breaks = sorted(set(u - half for u in us) | set(u + half for u in us))
    v_breaks = sorted(set(v - half for v in vs) | set(v + half for v in vs))
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
        grid[i] = list(map(add, grid[i - 1], grid[i]))

    # The admissible centres, as a polygon in (U, V) coordinates.
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
        row_minimum = min(row[j0:j1 + 1])
        cells += j1 - j0 + 1
        feasible_rows.append((i, j0, j1))
        if best is None or row_minimum < best:
            # list.index with bounds returns the absolute position, not an
            # offset from j0.
            best, best_cell = row_minimum, (i, row.index(row_minimum, j0, j1 + 1))

    def witness(i, j):
        # A point of the open cell that is also in F: the vertex average of
        # F clipped to the cell's closure lies in the interior of that
        # clipped polygon, which is the open cell's intersection with the
        # interior of F.
        box = clip_to_box(F,
                          u_breaks[i - 1] if i > 0 else None,
                          u_breaks[i] if i < len(u_breaks) else None,
                          v_breaks[j - 1] if j > 0 else None,
                          v_breaks[j] if j < len(v_breaks) else None)
        U = sum(u for u, _ in box) / len(box)
        V = sum(v for _, v in box) / len(box)
        X, Y = c * U - s * V, s * U + c * V
        assert h <= X <= L - h and h <= Y <= L - h
        return X, Y

    X, Y = witness(*best_cell)
    direct = covered_weight_at(cert, c, s, X, Y)
    if direct != Fraction(best, scale):
        raise AssertionError("grid weight %s disagrees with direct summation %s"
                             % (Fraction(best, scale), direct))
    # Optional audit: re-sum a few random admissible cells directly.
    for _ in range(audit):
        i, j0, j1 = rng.choice(feasible_rows)
        j = rng.randint(j0, j1)
        Xa, Ya = witness(i, j)
        if covered_weight_at(cert, c, s, Xa, Ya) != Fraction(grid[i][j], scale):
            raise AssertionError("audit: cell (%d, %d) disagrees with direct summation" % (i, j))
    return Fraction(best, scale), (X, Y), cells


def condition_c4(cert, audit=0, verbose=False, log=print):
    weights = [w for _, _, w in cert["atoms"]]
    scale = 1
    for w in weights:
        scale = scale * w.denominator // gcd(scale, w.denominator)
    integer_weights = [int(w * scale) for w in weights]
    rng = random.Random(0)
    worst, total_cells, vacuous_directions, started = None, 0, 0, time.time()
    K = len(cert["tangents"]) - 1
    for k, t in enumerate(cert["tangents"]):
        c, s = direction(t)
        minimum, centre, cells = least_covered_weight(cert, c, s, integer_weights, scale, audit, rng)
        total_cells += cells
        if minimum is None:
            vacuous_directions += 1
            if verbose or k % 30 == 0 or k == K:
                running = worst[0] if worst is not None else "-"
                log("    direction %3d/%d  t = %-18s no admissible placements; C4 vacuous  running least %s"
                    % (k, K, t, running))
            continue
        if worst is None or minimum < worst[0]:
            worst = (minimum, k, t, centre)
        if verbose or k % 30 == 0 or k == K:
            log("    direction %3d/%d  t = %-18s cells %7d  least weight %s = %.6f  running least %s"
                % (k, K, t, cells, minimum, float(minimum), worst[0]))
    if worst is None:
        detail = ("no admissible placements at any of %d directions; the universal condition is "
                  "vacuous; %d regions evaluated in %.1f s"
                  % (K + 1, total_cells, time.time() - started))
        return ("C4 every admissible placement covers weight >= 1", detail, True), None
    minimum, k, t, (X, Y) = worst
    detail = ("least covered weight %s = %.6f at direction %d (t = %s), centre (%s, %s) ~ (%.6f, %.6f); "
              "%d regions over %d directions (%d vacuous) in %.1f s"
              % (minimum, float(minimum), k, t, X, Y, float(X), float(Y),
                 total_cells, K + 1, vacuous_directions, time.time() - started))
    return ("C4 every admissible placement covers weight >= 1", detail, minimum >= 1), worst


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# ---------------------------------------------------------------------------
# The verdict.
# ---------------------------------------------------------------------------


def decide(cert, audit=0, verbose=False, log=print):
    """Run every check, print each with its numbers, and return the outcome.

    Nothing short-circuits: a certificate that fails C1 still has its C4
    minimum computed and printed, so a refusal names every failing condition.
    Returns (accepted, results) where results maps a check's name to
    (detail, holds), plus the least covered weight under the key "minimum"
    and the placement that attains it, (k, t, X, Y), under "witness".
    The verdict is computed from the list of checks, never from the dict.
    """
    declared = cert["declared"]
    log("certificate %s" % cert["id"])
    log("  n = %d, L = %s = %.6f, B = %s, net t_k = %s * k / %d for k = 0..%d, %d atoms"
        % (cert["n"], cert["L"], float(cert["L"]), cert["B"],
           declared["angle_limit"], len(cert["tangents"]) - 1, len(cert["tangents"]) - 1,
           len(cert["atoms"])))
    results, verdicts = {}, []

    def record(name, detail, holds):
        verdicts.append((name, holds))
        results[name] = (detail, holds)
        log("  %s  %s | %s" % ("PASS" if holds else "FAIL", name, detail))

    for name, detail, holds in preconditions(cert):
        record(name, detail, holds)
    if not all(holds for _, holds in verdicts):
        log("REFUSED: the file is not a certificate of the expected shape")
        return False, results
    for check in (condition_c0, condition_c1, condition_c2, condition_c3):
        record(*check(cert))
    log("  C4: sweeping every net direction")
    (name, detail, holds), worst = condition_c4(cert, audit, verbose, log)
    record(name, detail, holds)
    if worst is None:
        minimum = None
        results["minimum"] = None
        results["witness"] = None
    else:
        minimum, k, t, (X, Y) = worst
        results["minimum"] = minimum
        results["witness"] = (k, t, X, Y)
    # The theorem does not use the record's bookkeeping, but an artifact that
    # declares a value must agree with its replay. Keep these failures separate
    # from C0-C4 so the mathematical and record-integrity verdicts remain clear.
    declaration_failures = []
    total = sum((w for _, _, w in cert["atoms"]), Fraction(0))
    for key, value in (("total_mass", total), ("least_cell_mass", minimum)):
        if key in declared:
            if value is None:
                agrees = False
                replay = "no finite minimum (the feasible domain is empty)"
            else:
                agrees = rational(declared[key]) == value
                replay = str(value)
            log("  %s  declared %s %s %s recomputed %s"
                % ("info" if agrees else "NOTE", key, declared[key],
                   "==" if agrees else "!=", replay))
            if not agrees:
                declaration_failures.append("declared %s disagrees with replay" % key)
    inside = all(0 <= x <= cert["L"] and 0 <= y <= cert["L"] for x, y, _ in cert["atoms"])
    log("  info  all atoms lie in [0, L]^2: %s (not a condition; an outside atom only wastes weight)"
        % ("yes" if inside else "no"))
    failures = [name for name, holds in verdicts if not holds] + declaration_failures
    if failures:
        log("REFUSED: %s" % ", ".join(failures))
        return False, results
    log("VERIFIED: s(%d) >= %s = %.6f" % (cert["n"], cert["L"], float(cert["L"])))
    return True, results


def main(argv):
    if len(argv) < 2 or argv[1].startswith("-"):
        print(__doc__)
        return 2
    audit, verbose = 0, False
    rest = argv[2:]
    while rest:
        flag = rest.pop(0)
        if flag == "--audit":
            if not rest:
                print("missing integer after --audit")
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
            print("unknown option %s" % flag)
            return 2
    print("python %s" % sys.version.split()[0])
    try:
        accepted, _ = decide(load(argv[1]), audit=audit, verbose=verbose)
    except CertificateFormatError as error:
        print("REFUSED: malformed certificate: %s" % error)
        return 1
    return 0 if accepted else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
