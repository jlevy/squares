#!/usr/bin/env python3
"""Exact, theorem-specific verifier for the retained s(11) >= 381/100 certificate.

At a fixed direction, rotate square centres to (U,V).  Each atom is then
covered on a closed axis-aligned rectangle.  Its four edge coordinates cut
the plane into open cells on which covered mass is constant.  Event-boundary
points can only gain nonnegative mass, so it is enough to score every open
cell meeting the exact feasible-centre polygon.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from bisect import bisect_left, bisect_right
from fractions import Fraction
from itertools import accumulate
from math import gcd
from operator import add
from pathlib import Path
from typing import NoReturn

Q = Fraction
SHA256 = "b121edbd044b6f326022d8783551efd947c95eec2738269857d039358ac6ae6a"
DECLARED = {
    "id": "C-n011-fractional-381-100",
    "n": 11,
    "claim": "s(11) >= 381/100",
    "outer_side": "381/100",
    "square_side": "9977/10000",
    "angle_limit": "207107/500000",
    "direction_steps": 180,
    "total_mass": "434547/40000",
    "least_cell_mass": "4001/4000",
    "symmetry": "D4",
}
RATIONAL = re.compile(r"^-?[0-9]+(?:/[1-9][0-9]*)?$")


def fail(message) -> NoReturn:
    raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            fail(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def reject_inexact(value):
    fail(f"inexact JSON number {value!r}")


def rational(value):
    if not isinstance(value, str) or not RATIONAL.fullmatch(value):
        fail(f"not a rational string: {value!r}")
    return Q(value)


def load(path):
    raw = Path(path).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != SHA256:
        fail(f"SHA-256 {digest}, expected {SHA256}")
    record = json.loads(
        raw,
        object_pairs_hook=unique_object,
        parse_float=reject_inexact,
        parse_constant=reject_inexact,
    )
    for key, expected in DECLARED.items():
        if record.get(key) != expected:
            fail(f"declaration {key!r} is {record.get(key)!r}, expected {expected!r}")
    rows = record.get("atoms")
    if not isinstance(rows, list) or len(rows) != 1121:
        fail("expected exactly 1121 atoms")
    atoms = []
    for row in rows:
        if not isinstance(row, list) or len(row) != 3:
            fail(f"malformed atom {row!r}")
        atoms.append(tuple(rational(value) for value in row))
    return record, atoms


def images(x, y, side):
    far_x, far_y = side - x, side - y
    return {
        (x, y),
        (far_x, y),
        (x, far_y),
        (far_x, far_y),
        (y, x),
        (far_y, x),
        (y, far_x),
        (far_y, far_x),
    }


def check_measure(atoms, side, expected_total=None):
    weights = {}
    for x, y, weight in atoms:
        if not (0 <= x <= side and 0 <= y <= side and weight >= 0):
            fail("atom outside the container or carrying negative weight")
        weights[x, y] = weights.get((x, y), Q(0)) + weight
    for (x, y), weight in weights.items():
        if any(weights.get(point) != weight for point in images(x, y, side)):
            fail(f"D4 invariance fails at {(x, y)}")
    total = sum(weights.values(), Q(0))
    if expected_total is not None and total != expected_total:
        fail(f"total mass {total}, declared {expected_total}")
    if total >= 11:
        fail(f"total mass {total} is not below 11")
    return total


def clip(polygon, axis, bound, keep_above):
    output = []
    previous = polygon[-1]
    previous_in = previous[axis] >= bound if keep_above else previous[axis] <= bound
    for current in polygon:
        current_in = current[axis] >= bound if keep_above else current[axis] <= bound
        if current_in != previous_in:
            ratio = (bound - previous[axis]) / (current[axis] - previous[axis])
            output.append(
                (
                    previous[0] + ratio * (current[0] - previous[0]),
                    previous[1] + ratio * (current[1] - previous[1]),
                )
            )
        if current_in:
            output.append(current)
        previous, previous_in = current, current_in
    return output


def clip_box(polygon, u_low, u_high, v_low, v_high):
    for axis, bound, keep_above in (
        (0, u_low, True),
        (0, u_high, False),
        (1, v_low, True),
        (1, v_high, False),
    ):
        if bound is not None and polygon:
            polygon = clip(polygon, axis, bound, keep_above)
    return polygon


def rotation(tangent):
    denominator = 1 + tangent * tangent
    cosine = (1 - tangent * tangent) / denominator
    sine = 2 * tangent / denominator
    if cosine * cosine + sine * sine != 1 or cosine < 0 or sine < 0:
        fail("invalid rational rotation")
    return cosine, sine


def mass_at(atoms, cosine, sine, square_side, centre):
    x_centre, y_centre = centre
    half = square_side / 2
    total = Q(0)
    for x, y, weight in atoms:
        along = cosine * (x - x_centre) + sine * (y - y_centre)
        across = -sine * (x - x_centre) + cosine * (y - y_centre)
        if -half <= along <= half and -half <= across <= half:
            total += weight
    return total


def direction_minimum(  # noqa: PLR0917 - keeping the theorem inputs explicit aids audit.
    atoms, integer_weights, scale, side, square_side, tangent
):
    cosine, sine = rotation(tangent)
    half = square_side / 2
    extent = square_side * (cosine + sine) / 2
    if 2 * extent >= side:
        fail("the concrete certificate requires a full-dimensional feasible domain")

    us = [cosine * x + sine * y for x, y, _ in atoms]
    vs = [-sine * x + cosine * y for x, y, _ in atoms]
    u_breaks = sorted({u - half for u in us} | {u + half for u in us})
    v_breaks = sorted({v - half for v in vs} | {v + half for v in vs})
    u_index = {value: index for index, value in enumerate(u_breaks)}
    v_index = {value: index for index, value in enumerate(v_breaks)}

    # Cell i lies between breakpoints i-1 and i.  Rectangle range-adds followed
    # by two prefix sums give the exact integer mass of every open cell.
    grid = [[0] * (len(v_breaks) + 1) for _ in range(len(u_breaks) + 1)]
    for index, weight in enumerate(integer_weights):
        i0 = u_index[us[index] - half] + 1
        i1 = u_index[us[index] + half] + 1
        j0 = v_index[vs[index] - half] + 1
        j1 = v_index[vs[index] + half] + 1
        grid[i0][j0] += weight
        grid[i0][j1] -= weight
        grid[i1][j0] -= weight
        grid[i1][j1] += weight
    grid = [list(accumulate(row)) for row in grid]
    for index in range(1, len(grid)):
        # Construction gives every row the same length.
        grid[index] = list(map(add, grid[index - 1], grid[index]))  # noqa: B912

    corners = (
        (extent, extent),
        (side - extent, extent),
        (side - extent, side - extent),
        (extent, side - extent),
    )
    feasible = [(cosine * x + sine * y, -sine * x + cosine * y) for x, y in corners]
    u_min = min(u for u, _ in feasible)
    u_max = max(u for u, _ in feasible)
    best = None
    best_cell = None
    cells = 0
    for i in range(len(u_breaks) + 1):
        left = u_breaks[i - 1] if i else None
        right = u_breaks[i] if i < len(u_breaks) else None
        if (left is not None and left >= u_max) or (right is not None and right <= u_min):
            continue
        strip = clip_box(feasible, left, right, None, None)
        low = min(v for _, v in strip)
        high = max(v for _, v in strip)
        if not low < high:
            fail("degenerate feasible strip")
        first = bisect_right(v_breaks, low)
        last = bisect_left(v_breaks, high)
        cells += last - first + 1
        row_best = min(grid[i][first : last + 1])
        if best is None or row_best < best:
            best = row_best
            best_cell = (i, grid[i].index(row_best, first, last + 1))

    if best is None or best_cell is None:
        fail("no feasible event cell")
    i, j = best_cell
    cell = clip_box(
        feasible,
        u_breaks[i - 1] if i else None,
        u_breaks[i] if i < len(u_breaks) else None,
        v_breaks[j - 1] if j else None,
        v_breaks[j] if j < len(v_breaks) else None,
    )
    centre_u = sum(u for u, _ in cell) / len(cell)
    centre_v = sum(v for _, v in cell) / len(cell)
    centre = (
        cosine * centre_u - sine * centre_v,
        sine * centre_u + cosine * centre_v,
    )
    exact = Q(best, scale)
    if mass_at(atoms, cosine, sine, square_side, centre) != exact:
        fail("prefix-sum minimum disagrees with direct atom summation")
    return exact, centre, cells


def verify(path):
    record, atoms = load(path)
    side = rational(record["outer_side"])
    square_side = rational(record["square_side"])
    total = check_measure(atoms, side, rational(record["total_mass"]))

    limit = rational(record["angle_limit"])
    steps = record["direction_steps"]
    tangents = [limit * index / steps for index in range(steps + 1)]
    if tangents[0] != 0 or any(
        tangents[index] >= tangents[index + 1] for index in range(steps)
    ):
        fail("direction net is not strictly increasing from zero")
    endpoint = limit * limit + 2 * limit - 1
    if endpoint < 0:
        fail("direction net does not reach pi/4")
    gaps = [
        (tangents[index + 1] - tangents[index]) / (1 + tangents[index] * tangents[index + 1])
        for index in range(steps)
    ]
    gap = max(gaps)
    containment = square_side * (1 + gap)
    if gap != Q(207107, 90000000) or containment >= 1:
        fail("direction gap does not give strict containment")

    scale = 1
    for _, _, weight in atoms:
        scale = scale * weight.denominator // gcd(scale, weight.denominator)
    integer_weights = [int(weight * scale) for _, _, weight in atoms]
    worst = None
    worst_record = None
    cell_count = 0
    for index, tangent in enumerate(tangents):
        minimum, centre, cells = direction_minimum(
            atoms, integer_weights, scale, side, square_side, tangent
        )
        cell_count += cells
        if worst is None or minimum < worst:
            worst = minimum
            worst_record = (index, centre)
    if worst is None or worst_record is None:
        fail("direction net is empty")
    declared_minimum = rational(record["least_cell_mass"])
    if worst != declared_minimum or worst < 1:
        fail(f"least cell mass {worst}, declared {declared_minimum}")

    print(f"SHA256 PASS  {SHA256}")
    print(f"C0/C1  PASS  {len(atoms)} atoms, D4 invariant, total mass {total} < 11")
    print(f"C2     PASS  endpoint slack {endpoint}")
    print(f"C3     PASS  D = {gap}; B(1+D) = {containment} < 1")
    index, centre = worst_record
    print(
        f"C4     PASS  minimum {worst} at direction {index}, "
        f"centre ({centre[0]}, {centre[1]}); {cell_count} cells"
    )
    print(f"VERIFIED {record['claim']}")
    return atoms, side, square_side, tangents, worst_record


def must_refuse(atoms, side, square_side, tangents, worst_record):
    index, centre = worst_record
    cosine, sine = rotation(tangents[index])
    # Scaling every weight keeps D4 and all geometric conditions intact, preserves
    # nonnegativity, and drives either retained certificate's tight cell below one.
    factor = Q(3999, 4001)
    mutated = [(x, y, weight * factor) for x, y, weight in atoms]
    check_measure(mutated, side)
    witness_mass = mass_at(mutated, cosine, sine, square_side, centre)
    if witness_mass >= 1:
        fail("must-refuse mutation was not refuted")
    print(
        f"MUTATION REFUSED  scaling every weight by {factor} leaves C0-C3 valid "
        f"but gives C4 witness mass {witness_mass} < 1"
    )


def main():
    if len(sys.argv) != 2:
        fail("usage: minimal_verify.py certificate.json")
    started = time.perf_counter()
    result = verify(sys.argv[1])
    must_refuse(*result)
    print(f"elapsed {time.perf_counter() - started:.3f}s")


if __name__ == "__main__":
    main()
