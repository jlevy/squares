"""Lane r1012: describe the certificate. It decides nothing.

Usage: r1012_describe.py CERTIFICATE OUT.json

Written after the checker's freeze and before the findings' freeze. It reads the
certificate through r1012_reader and reports, exactly where it can: each square's
centre and edge direction and their denominators, the tilt (from a binary64
arctangent, for display only), the rational half-angle tan(theta/2) = b/(1 + a),
the packing's extent against the side, the near pairs with their kind and
Euclidean gap, and how each wall contact is made.
"""

import json
import math
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.set_int_max_str_digits(0)

import r1012_geom as G  # noqa: E402
import r1012_reader  # noqa: E402

getcontext().prec = 60


def sci(x, d=6):
    x = F(x)
    if x == 0:
        return "0"
    return f"{Decimal(x.numerator) / Decimal(x.denominator):.{d - 1}e}"


def digits(n):
    return len(str(abs(n)))


def terminating_places(x):
    """Decimal places of x if its expansion terminates, else None."""
    den = x.denominator
    twos = fives = 0
    while den % 2 == 0:
        den //= 2
        twos += 1
    while den % 5 == 0:
        den //= 5
        fives += 1
    return max(twos, fives) if den == 1 else None


def main(argv):
    cert, out = argv[1:3]
    p = r1012_reader.read_path(cert)
    n, side, ids, quads = p["n"], p["side"], p["ids"], p["corners"]
    squares = []
    for k, q in enumerate(quads):
        c = G.centre(q)
        e, f = G.edges(q)
        a, b = e
        aligned = a == 0 or b == 0
        tilt = math.degrees(math.atan2(float(b), float(a)))
        folded = tilt
        while folded > 45:
            folded -= 90
        while folded <= -45:
            folded += 90
        half = (b / (1 + a)) if a != -1 else None
        dev = min(abs(a), abs(b))
        c0 = G.centre(quads[0])
        rel = (c[0] - c0[0], c[1] - c0[1])
        squares.append({
            "id": ids[k],
            "axis_aligned": aligned,
            "edge_direction_degrees": f"{tilt:.9f}",
            "tilt_folded_degrees": f"{folded:.9f}",
            "centre_terminating_places": [terminating_places(c[0]), terminating_places(c[1])],
            "centre_denominator_digits": [digits(c[0].denominator), digits(c[1].denominator)],
            "basis_denominator_digits": digits(F(a).denominator) if not aligned else 1,
            "half_angle_tangent": None if half is None else f"{half.numerator}/{half.denominator}",
            "half_angle_digits": None if half is None else [digits(half.numerator), digits(half.denominator)],
            "half_angle_terminating_places": None if half is None else terminating_places(half),
            "sine_of_deviation_from_nearest_axis": sci(dev, 9),
            "deviation_degrees": f"{math.degrees(math.asin(float(dev))):.6e}",
            "centre_minus_first_centre_terminating_places": [terminating_places(rel[0]), terminating_places(rel[1])],
            "corner0_terminating_places": [terminating_places(q[0][0]), terminating_places(q[0][1])],
            "corner_denominator_digits": max(digits(x.denominator) for pt in q for x in pt),
        })
    xs = [x for q in quads for x, _ in q]
    ys = [y for q in quads for _, y in q]
    extent = {
        "min_x": sci(min(xs)), "min_y": sci(min(ys)),
        "side_minus_max_x": sci(side - max(xs)), "side_minus_max_y": sci(side - max(ys)),
        "side_minus_max_x_exact": f"{(side - max(xs)).numerator}/{(side - max(xs)).denominator}",
        "side_minus_max_y_exact": f"{(side - max(ys)).numerator}/{(side - max(ys)).denominator}",
        "width": sci(max(xs) - min(xs), 25), "height": sci(max(ys) - min(ys), 25),
    }
    # near pairs: kind and gap; and the least margins above 1e-9
    near = []
    above = []
    for i in range(n):
        for j in range(i + 1, n):
            m = G.margin(quads[i], quads[j])
            if m >= F(1, 10 ** 9):
                above.append((m, ids[i], ids[j]))
            if m < F(1, 10 ** 9):
                ei, _ = G.edges(quads[i])
                ej, _ = G.edges(quads[j])
                cross = ei[0] * ej[1] - ei[1] * ej[0]
                dotp = G.dot(ei, ej)
                parallel = cross == 0 or dotp == 0
                g2 = G.gap2(quads[i], quads[j])
                ratio = (Decimal(g2.numerator) / Decimal(g2.denominator)).sqrt() / (
                    Decimal(m.numerator) / Decimal(m.denominator))
                kinds = ("aligned" if squares[i]["axis_aligned"] else "turned",
                         "aligned" if squares[j]["axis_aligned"] else "turned")
                near.append({"pair": [ids[i], ids[j]], "margin": sci(m, 9),
                             "margin_exact": f"{m.numerator}/{m.denominator}",
                             "margin_in_1e-16": f"{Decimal(m.numerator) / Decimal(m.denominator) * Decimal(10) ** 16:.4f}",
                             "edges_parallel": parallel, "kinds": "-".join(sorted(kinds)),
                             "gap_over_margin": f"{ratio:.9f}"})
    near.sort(key=lambda d: F(d["margin_exact"]))
    kinds_count = {}
    for d in near:
        kinds_count[d["kinds"]] = kinds_count.get(d["kinds"], 0) + 1
    parallel_count = sum(1 for d in near if d["edges_parallel"])
    gap_equal = sum(1 for d in near if d["gap_over_margin"] == "1.000000000")
    # wall contacts and least clearances: how made
    contacts = []
    for k, q in enumerate(quads):
        cl = G.clearances(q, side)
        for w, c in enumerate(cl):
            if c == 0:
                coord = [pt[0] if w in (0, 2) else pt[1] for pt in q]
                on_wall = sum(1 for v in coord if v == (0 if w < 2 else side))
                contacts.append({"square": ids[k], "wall": "LBRT"[w], "corners_on_wall": on_wall,
                                 "axis_aligned": squares[k]["axis_aligned"]})
    tilts = sorted(F(s["tilt_folded_degrees"]) for s in squares if not s["axis_aligned"])
    # each wall contact against the least clearance of an axis-aligned square at that wall
    for item in contacts:
        w = "LBRT".index(item["wall"])
        k = ids.index(item["square"])
        e, _ = G.edges(quads[k])
        sine = min(abs(e[0]), abs(e[1]))
        aligned_cl = min(G.clearances(q, side)[w] for j, q in enumerate(quads) if squares[j]["axis_aligned"])
        item["sine_of_deviation"] = sci(sine, 9)
        item["least_axis_aligned_clearance_at_wall"] = sci(aligned_cl, 9)
        item["that_clearance_equals_half_the_sine"] = aligned_cl == sine / 2
    small = [(F(s["sine_of_deviation_from_nearest_axis"]), s["id"]) for s in squares
             if not s["axis_aligned"] and F(s["sine_of_deviation_from_nearest_axis"]) < F(1, 10 ** 9)]
    slight = [(s["tilt_folded_degrees"], s["id"]) for s in squares if not s["axis_aligned"]
              and F(1, 10 ** 9) <= F(s["sine_of_deviation_from_nearest_axis"]) and abs(F(s["tilt_folded_degrees"])) < 1]
    receipt = {
        "program": "r1012_describe.py",
        "sha256": p["sha256"],
        "n": n,
        "side_terminating_places": terminating_places(side),
        "extent": extent,
        "axis_aligned": sum(1 for s in squares if s["axis_aligned"]),
        "turned": sum(1 for s in squares if not s["axis_aligned"]),
        "turned_positive": sum(1 for t in tilts if t > 0),
        "turned_negative": sum(1 for t in tilts if t < 0),
        "tilt_range_degrees": [str(tilts[0]) if tilts else None, str(tilts[-1]) if tilts else None],
        "centre_terminating_places_max": max(max(s["centre_terminating_places"], key=lambda v: -1 if v is None else v) or 0 for s in squares),
        "centres_all_terminating": all(None not in s["centre_terminating_places"] for s in squares),
        "half_angle_digits_max": max((max(s["half_angle_digits"]) for s in squares if s["half_angle_digits"] and not s["axis_aligned"]), default=None),
        "turned_within_sine_1e-9_of_an_axis": len(small),
        "their_sine_range": [sci(min(small)[0], 9), sci(max(small)[0], 9)] if small else None,
        "turned_by_less_than_a_degree_otherwise": slight,
        "near_pairs_below_1e-9": len(near),
        "near_pair_kinds": kinds_count,
        "near_pairs_with_parallel_edges": parallel_count,
        "near_pairs_gap_equal_margin_to_9_places": gap_equal,
        "near_pairs": near,
        "least_margins_above_1e-9": [{"pair": [a, b], "margin": sci(m, 9)} for m, a, b in sorted(above)[:6]],
        "wall_contacts": contacts,
        "squares": squares,
    }
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(receipt, handle, indent=1)
        handle.write("\n")
    print(f"described {len(near)} near pairs, {receipt['axis_aligned']} axis-aligned squares")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
