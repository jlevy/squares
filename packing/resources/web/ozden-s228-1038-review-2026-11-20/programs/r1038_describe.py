"""Describe the certificate; it decides nothing. Written after the checker was frozen and
before the findings were frozen, so it is not in the checker's digest list.

Usage: python -I -B r1038_describe.py CERTIFICATE OUT_JSON

It reports the tilts (exact half-angles; degrees in binary64, for description only), the
near pairs with their exact margins, the normal that separates them, their margins as
multiples of the stated radial factor's epsilon and their exact squared Euclidean gap,
how each wall contact is made, and the stated factor's pre-image: the centres divided by
2500000000000011391221/2500000000000000000000 about the lower-left origin, bases
unchanged, with its margins and extents by method A. Floats appear only in reported
descriptions.
"""

from __future__ import annotations

import json
import math
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import r1038_decide as decide  # noqa: E402
import r1038_geom as geom  # noqa: E402
import r1038_reader as reader  # noqa: E402
import r1038_sat as sat  # noqa: E402

FACTOR = Fraction(2500000000000011391221, 2500000000000000000000)
NEAR = Fraction(1, 10**9)


def separating(ci, bi, cj, bj) -> str:
    """Which normal attains the margin: u_i, v_i, u_j or v_j."""
    pi, pj = geom.corners(ci, bi), geom.corners(cj, bj)
    best, name = None, ""
    for label, w in zip(("u_i", "v_i", "u_j", "v_j"), geom.normals(bi) + geom.normals(bj)):
        lo_i = min(p[0] * w[0] + p[1] * w[1] for p in pi)
        hi_i = max(p[0] * w[0] + p[1] * w[1] for p in pi)
        lo_j = min(p[0] * w[0] + p[1] * w[1] for p in pj)
        hi_j = max(p[0] * w[0] + p[1] * w[1] for p in pj)
        gap = max(lo_j - hi_i, lo_i - hi_j)
        if best is None or gap > best:
            best, name = gap, label
    return name


def point_segment2(p, a, b) -> Fraction:
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)
    t = min(Fraction(1), max(Fraction(0), t))
    qx, qy = a[0] + t * dx - p[0], a[1] + t * dy - p[1]
    return qx * qx + qy * qy


def gap2(ci, bi, cj, bj) -> Fraction:
    """The squared Euclidean distance between two disjoint squares: vertex to edge."""
    pi, pj = geom.corners(ci, bi), geom.corners(cj, bj)
    best = None
    for poly_a, poly_b in ((pi, pj), (pj, pi)):
        for p in poly_a:
            for k in range(4):
                value = point_segment2(p, poly_b[k], poly_b[(k + 1) % 4])
                if best is None or value < best:
                    best = value
    assert best is not None
    return best


def main(argv: list[str]) -> int:
    cert = reader.read_path(argv[1])
    side, centers, bases = cert.side, cert.centers, cert.bases
    result = decide.decide(side, centers, bases)
    eps = FACTOR - 1
    axis = [a * b == 0 for a, b in bases]
    tilts: dict[str, int] = {}
    half_angles = []
    for (a, b), aligned in zip(bases, axis):
        if aligned:
            continue
        degrees = math.degrees(math.atan2(float(b), float(a))) % 90.0
        key = f"{degrees:.9f}"
        tilts[key] = tilts.get(key, 0) + 1
        t = b / (1 + a) if a != -1 else None
        half_angles.append(None if t is None else len(str(t.denominator)))
    near = sorted((value, key) for key, value in result.margins.items() if value < NEAR)
    rows = []
    for value, (i, j) in near:
        ci, bi, cj, bj = centers[i - 1], bases[i - 1], centers[j - 1], bases[j - 1]
        squared = gap2(ci, bi, cj, bj)
        rows.append(
            {
                "pair": [i, j],
                "margin": decide.decimal(value),
                "margin_over_eps": decide.decimal(value / eps, 12),
                "margin_equals_eps": value == eps,
                "normal": separating(ci, bi, cj, bj),
                "both_axis_aligned": axis[i - 1] and axis[j - 1],
                "euclidean_gap": decide.decimal(Fraction(math.isqrt(squared.numerator * 10**80 // squared.denominator), 10**40)),
                "euclidean_gap_over_margin": f"{math.sqrt(float(squared / (value * value))):.12g}",
            }
        )
    contact_kinds = {"edge": 0, "corner": 0}
    contacts = []
    for k, values in enumerate(result.clear_a, start=1):
        for w, v in enumerate(values):
            if v == 0:
                kind = "edge" if axis[k - 1] else "corner"
                contact_kinds[kind] += 1
                contacts.append([k, decide.WALLS[w], kind])
    pre_centers = [(x / FACTOR, y / FACTOR) for x, y in centers]
    pre_ints = [sat.integer_square(c[0], c[1], u[0], u[1]) for c, u in zip(pre_centers, bases)]
    pre_near = []
    pre_negative = 0
    pre_zero = 0
    for value, (i, j) in near:
        m = sat.as_fraction(sat.margin(pre_ints[i - 1], pre_ints[j - 1]))
        pre_near.append({"pair": [i, j], "margin": decide.decimal(m), "margin_over_eps": decide.decimal(m / eps, 12)})
        pre_negative += m < 0
        pre_zero += m == 0
    pre_clear = [[sat.as_fraction(r) for r in sat.clearances(s, side / FACTOR)] for s in pre_ints]
    least = [min(row[w] for row in pre_clear) for w in range(4)]
    # About the box centre instead: c0 = (c - S/2)/f + S0/2 with S0 = (S + eps)/f, the side
    # for which a packing touching all four walls, scaled by f about its box centre, has
    # extent f S0 - eps = S.
    side0 = (side + eps) / FACTOR
    box_ints = [
        sat.integer_square((x - side / 2) / FACTOR + side0 / 2, (y - side / 2) / FACTOR + side0 / 2, u[0], u[1])
        for (x, y), u in zip(centers, bases)
    ]
    box_clear = [[sat.as_fraction(r) for r in sat.clearances(s, side0)] for s in box_ints]
    box_least = [min(row[w] for row in box_clear) for w in range(4)]
    box_contacts = sum(1 for row in box_clear for v in row if v == 0)
    out = {
        "program": "r1038_describe.py",
        "decides": "nothing",
        "certificate": os.path.basename(argv[1]),
        "factor": str(FACTOR),
        "factor_minus_one": str(eps),
        "factor_minus_one_decimal": decide.decimal(eps),
        "squares_axis_aligned": sum(axis),
        "squares_tilted": len(axis) - sum(axis),
        "tilt_degrees_mod_90_binary64": dict(sorted(tilts.items())),
        "half_angle_denominator_digits": sorted(h for h in half_angles if h is not None)[-5:],
        "basis_denominator_digits_max": max(len(str(max(a.denominator, b.denominator))) for a, b in bases),
        "centre_denominator_digits_max": max(len(str(max(x.denominator, y.denominator))) for x, y in centers),
        "near_pairs_below_1e-9": len(rows),
        "margins_exactly_eps": sum(1 for value in result.margins.values() if value == eps),
        "near_pairs": rows,
        "next_margin_after_near": None
        if len(near) == len(result.margins)
        else decide.decimal(min(v for v in result.margins.values() if v >= NEAR)),
        "wall_contacts": contacts,
        "wall_contact_kinds": contact_kinds,
        "extent_x": str(side - min(r[0] for r in result.clear_a) - min(r[2] for r in result.clear_a)),
        "extent_y": str(side - min(r[1] for r in result.clear_a) - min(r[3] for r in result.clear_a)),
        "pre_image": {
            "what": "centres divided by the stated factor about the lower-left origin, bases unchanged, side divided by it; method A",
            "near_pairs": pre_near,
            "near_pairs_negative": pre_negative,
            "near_pairs_zero": pre_zero,
            "least_clearance_left_bottom_right_top": [decide.decimal(v) for v in least],
        },
        "pre_image_box_centre": {
            "what": "centres scaled by 1/f about the box centre into the side S0 = (S + eps)/f; pair margins as in pre_image, since they do not depend on translation",
            "side0": str(side0),
            "side0_decimal_40": decide.fixed(side0, 40),
            "side_less_side0": decide.decimal(side - side0),
            "eps_times_side0_less_one": decide.decimal(eps * (side0 - 1)),
            "least_clearance_left_bottom_right_top": [decide.decimal(v) for v in box_least],
            "wall_contacts": box_contacts,
            "crossings": sum(1 for row in box_clear for v in row if v < 0),
        },
    }
    with open(argv[2], "w", encoding="utf-8") as handle:
        json.dump(out, handle, indent=1)
    print("described", len(rows), "near pairs,", sum(axis), "axis-aligned squares")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
