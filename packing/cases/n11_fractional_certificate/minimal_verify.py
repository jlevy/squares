#!/usr/bin/env python3
"""Decide the retained ``s(11) >= 381/100`` certificate, exactly, from its own bytes.

    python3 minimal_verify.py certificate.json

One line per condition, then VERIFIED or REFUSED; the exit status is 0 only after
VERIFIED. Any CPython 3.8 or later, standard library only, nothing imported from this
repository, and no float decides anything. ``t-018-proof-card.md``, beside this file, states
the theorem with the certificate's own parameters; ``sqpack/fractional/certificate.py``
proves it and ``sqpack/fractional/sweep.py`` is the same sweep, in the project verifier.

For ``n``, a container side ``L``, a shrunken side ``B``, net half-angle tangents
``t_k = T k / K`` (net angle ``2 arctan t_k``), atoms ``(x, y, w)`` with ``w >= 0``, and
``D = max_k (t_k+1 - t_k) / (1 + t_k t_k+1)``, the largest tangent of HALF a net gap:

  Condition 1  the atoms are invariant under the eight symmetries of ``[0, L]^2``;
  Condition 2  the total weight is strictly below ``n``;
  Condition 3  the net reaches pi/4, decided exactly as ``t_K^2 + 2 t_K - 1 >= 0``;
  Condition 4  ``B (1 + D) < 1``, so a unit square at any angle contains a closed
      ``B``-square at some net angle;
  Condition 5  every closed ``B``-square at a net angle inside ``[0, L]^2`` covers
      weight at least 1.

Then ``n`` unit squares with pairwise disjoint interiors do not fit in ``[0, L]^2``:
each would contain one of ``n`` disjoint ``B``-squares of weight at least 1, and
Condition 2 forbids that total. Nonnegative weights are what makes that counting step
monotone, so they are checked here with Condition 1.

Condition 5 is the only expensive one, and the only one about a continuum. At a net
direction, covered weight is constant on the open cells the atoms' coverage rectangles
cut the plane into, so scoring every cell the centre domain reaches decides every
placement. The centre domain is the rotated square of centres keeping the ``B``-square
inside the container, not its bounding box -- the box admits placements hanging outside
and would make a sound certificate look refutable. Weights are summed as integers on
their common denominator, and each direction's minimum is re-derived by a direct sum
over the atoms at its own witness.

``verify_claim.py``, beside this file, is the unpinned counterpart: it decides any
certificate of this form, the retained ``19/5`` rung included, reads one out of a
``t-018-verifiable-claim-*.md`` document as readily as from JSON, and is embedded in
full in those documents so that each travels as one file. This program speaks only for
the bytes it pins.
"""

import hashlib
import json
import sys
import time
from bisect import bisect_left, bisect_right
from fractions import Fraction
from itertools import accumulate
from math import gcd
from pathlib import Path

#: The retained certificate's bytes, pinned once -- here, and nowhere else. Every other
#: statement of this digest (t-018-proof-card.md, the evidence entry) should read it from the
#: file, `sha256sum certificate.json`, or quote the SHA-256 line this program prints. A
#: digest copied by hand is a second thing to keep in step, and it will not be kept.
PINNED_SHA256 = "b121edbd044b6f326022d8783551efd947c95eec2738269857d039358ac6ae6a"


def refuse(message):
    """Every refusal is a ValueError: these bytes are not a proof, and this is why."""
    raise ValueError(message)


def rational(value, field):
    """Exact rationals arrive as strings; a JSON number would be a float, and is refused."""
    if not isinstance(value, str):
        refuse(f"{field} must be an exact rational written as a string, not {value!r}")
    return Fraction(value)


def load(path, *, pinned):
    raw = Path(path).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if pinned and digest != PINNED_SHA256:
        refuse(f"SHA-256 {digest} is not the pinned {PINNED_SHA256}")
    record = json.loads(raw)
    variant = record.get("variant", "unconditional")
    if variant != "unconditional":
        refuse(f"variant {variant!r} declared; only unconditional certificates are decided")
    atoms = [tuple(rational(value, "atom") for value in row) for row in record["atoms"]]
    if any(len(atom) != 3 for atom in atoms):
        refuse("every atom must be exactly [x, y, weight]")
    return digest, record, atoms


def condition_1(atoms, side, symmetry):
    """D4 invariance, on distinct sites, inside the container, at nonnegative weights."""
    if symmetry != "D4":
        refuse(f"only D4 is supported, not {symmetry!r}")
    weights = {}
    for x, y, weight in atoms:
        if weight < 0 or not (0 <= x <= side and 0 <= y <= side):
            refuse(f"atom ({x}, {y}) weighs {weight} or lies outside [0, {side}]^2")
        if (x, y) in weights:
            refuse(f"two atoms share the site ({x}, {y})")
        weights[(x, y)] = weight
    for (x, y), weight in weights.items():
        far_x, far_y = side - x, side - y
        images = ((far_x, y), (x, far_y), (far_x, far_y), (y, x), (far_y, x), (y, far_x))
        for image in (*images, (far_y, far_x)):
            if weights.get(image) != weight:
                refuse(f"the D4 image {image} of ({x}, {y}) does not carry weight {weight}")
    return f"{len(atoms)} atoms, distinct, inside, nonnegative, D4-invariant about the centre"


def clip(polygon, bound, *, above):
    """Sutherland--Hodgman against one vertical line, in exact arithmetic."""
    if not polygon:
        return []
    output, previous = [], polygon[-1]
    was_in = previous[0] >= bound if above else previous[0] <= bound
    for current in polygon:
        is_in = current[0] >= bound if above else current[0] <= bound
        if is_in != was_in:
            ratio = (bound - previous[0]) / (current[0] - previous[0])
            output.append((bound, previous[1] + ratio * (current[1] - previous[1])))
        if is_in:
            output.append(current)
        previous, was_in = current, is_in
    return output


def sweep(atoms, weights, half, side, tangent):
    """Least mass a reachable placement covers at one net direction, and the cells scored."""
    square = tangent * tangent
    cosine, sine = (1 - square) / (1 + square), 2 * tangent / (1 + square)
    if cosine * cosine + sine * sine != 1 or cosine <= 0 or sine < 0:
        refuse(f"the half-tangent {tangent} is not an exact rotation into [0, pi/4]")
    us = [cosine * x + sine * y for x, y, _ in atoms]
    vs = [cosine * y - sine * x for x, y, _ in atoms]
    reach = half * (cosine + sine)
    if 2 * reach >= side:
        refuse("no placement of the B-square fits inside the container")
    low, high = reach, side - reach
    corners = ((low, low), (high, low), (high, high), (low, high))
    domain = [(cosine * x + sine * y, cosine * y - sine * x) for x, y in corners]
    # The domain's own extremes join the events, so no cell straddles the domain's edge
    # and the index clamping below can hide no reachable placement.
    ends = (min(u for u, _ in domain), max(u for u, _ in domain))
    u_events = sorted(set(ends).union(u - half for u in us).union(u + half for u in us))
    ends = (min(v for _, v in domain), max(v for _, v in domain))
    v_events = sorted(set(ends).union(v - half for v in vs).union(v + half for v in vs))
    u_at = {value: index for index, value in enumerate(u_events)}
    v_at = {value: index for index, value in enumerate(v_events)}

    # Cell (i, j) is the open rectangle between events i, i+1 and j, j+1. Sweeping the
    # columns left to right, an atom enters at u - half and leaves at u + half, so one
    # difference array over v, prefix-summed per column, is the whole grid of masses.
    changes = [[] for _ in u_events]
    for index, weight in enumerate(weights):
        span = (v_at[vs[index] - half], v_at[vs[index] + half])
        changes[u_at[us[index] - half]].append((span[0], span[1], weight))
        changes[u_at[us[index] + half]].append((span[0], span[1], -weight))

    column = [0] * len(v_events)
    ceiling = sum(weights) + 1  # no cell carries the whole mass, so this is a sentinel
    best, spot, cells = ceiling, (0, 0), 0
    for index in range(len(u_events) - 1):
        for start, stop, weight in changes[index]:
            column[start] += weight
            column[stop] -= weight
        strip = clip(
            clip(domain, u_events[index], above=True), u_events[index + 1], above=False
        )
        if len(strip) < 3:
            continue
        floor, roof = min(v for _, v in strip), max(v for _, v in strip)
        first = max(0, bisect_right(v_events, floor) - 1)
        last = min(len(v_events) - 2, bisect_left(v_events, roof) - 1)
        if last < first:
            continue
        masses = list(accumulate(column))
        cells += last - first + 1
        least = min(masses[first : last + 1])
        if least < best:
            best = least
            spot = (index, masses.index(least, first, last + 1))
    if best == ceiling:
        refuse("the centre domain reached no event cell")

    # The prefix sums are the one clever step here; a direct sum at the witness is not.
    i, j = spot
    centre = ((u_events[i] + u_events[i + 1]) / 2, (v_events[j] + v_events[j + 1]) / 2)
    direct = sum(
        weight
        for index, weight in enumerate(weights)
        if abs(us[index] - centre[0]) <= half and abs(vs[index] - centre[1]) <= half
    )
    if direct != best:
        refuse(f"the swept minimum {best} is not the direct sum {direct} at its own witness")
    return best, cells


def verify(path, *, pinned=True):
    digest, record, atoms = load(path, pinned=pinned)
    print(f"SHA-256      {'PASS' if pinned else 'UNPINNED'}  {digest}")
    n, side = record["n"], rational(record["outer_side"], "outer_side")
    shrink = rational(record["square_side"], "square_side")
    claim = f"s({n}) >= {side}"
    if record["claim"] != claim:
        refuse(f"the record claims {record['claim']!r}, which is not {claim!r}")
    print(f"Condition 1  PASS  {condition_1(atoms, side, record['symmetry'])}")

    total = sum((weight for _, _, weight in atoms), Fraction(0))
    if total >= n:
        refuse(f"total mass {total} is not below n = {n}")
    if total != rational(record["total_mass"], "total_mass"):
        refuse(f"total mass {total} is not the declared {record['total_mass']}")
    print(f"Condition 2  PASS  total mass {total} = {float(total):.6f} < {n}")

    limit, steps = rational(record["angle_limit"], "angle_limit"), record["direction_steps"]
    if not isinstance(steps, int) or steps < 1 or limit <= 0:
        refuse(f"a net of {steps} steps up to {limit} is not a net")
    tangents = [limit * step / steps for step in range(steps + 1)]
    slack = limit * limit + 2 * limit - 1
    if slack < 0:
        refuse(f"the net stops short of pi/4: t^2 + 2t - 1 = {slack}")
    print(f"Condition 3  PASS  final half-tangent {limit}, t^2 + 2t - 1 = {slack} >= 0")

    gap = max(
        (tangents[k + 1] - tangents[k]) / (1 + tangents[k] * tangents[k + 1])
        for k in range(steps)
    )
    if shrink * (1 + gap) >= 1:
        refuse(f"B(1 + D) = {shrink * (1 + gap)} is not below 1")
    print(f"Condition 4  PASS  D = {gap}, B(1 + D) = {float(shrink * (1 + gap)):.12f} < 1")

    scale = 1
    for _, _, weight in atoms:
        scale = scale * weight.denominator // gcd(scale, weight.denominator)
    weights = [int(weight * scale) for _, _, weight in atoms]
    minima, cells = [], 0
    for index, tangent in enumerate(tangents):
        least, scored = sweep(atoms, weights, shrink / 2, side, tangent)
        minima.append((least, index))
        cells += scored
    worst, at = min(minima)  # ties go to the first direction attaining the minimum
    minimum = Fraction(worst, scale)
    if minimum < 1:
        refuse(f"a reachable cell at direction {at} carries only {minimum}")
    if minimum != rational(record["least_cell_mass"], "least_cell_mass"):
        refuse(f"least covered mass {minimum} is not the declared {record['least_cell_mass']}")
    print(
        f"Condition 5  PASS  least covered mass {minimum} = {float(minimum):.6f} >= 1, at "
        f"direction {at} of {len(tangents)}, over {cells} reachable cells"
    )
    print(f"VERIFIED  {claim}")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    paths = [item for item in argv if item != "--unpinned"]
    if len(paths) != 1:
        print("usage: minimal_verify.py CERTIFICATE.json [--unpinned]")
        return 2
    started = time.time()
    try:
        verify(paths[0], pinned="--unpinned" not in argv)
    except (ArithmeticError, KeyError, OSError, TypeError, ValueError) as error:
        print(f"REFUSED  {error}")
        return 1
    finally:
        print(f"elapsed {time.time() - started:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
