"""Describe a certificate: tilts, blocks of tilted squares, wall contacts, number forms.

Lane R1, stage 4 review of #1005, #1006 and #1007.  Clean-room.

    python -I -B r1_describe.py FILE FORM OUT.json

It decides nothing.  It is frozen with the checker, having been tried on synthetic
files only.  It reads the file through the reader and uses method A for the margins
between tilted squares.  Angles are printed from binary64 arctangents of the exact
directions; every count that says "exactly" is decided on the exact rationals.
"""

from __future__ import annotations

import math
import os
import sys
from collections import Counter
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import r1_axes  # noqa: E402
import r1_fmt  # noqa: E402
import r1_frame  # noqa: E402
import r1_read  # noqa: E402

WALLS = r1_frame.WALLS
NEAR = Fraction(1, 10**6)


def tilt_degrees(u):
    """The square's turn from upright, in (-45, 45] degrees (a square repeats every 90)."""
    angle = math.degrees(math.atan2(float(u[1]), float(u[0]))) % 90.0
    return angle - 90.0 if angle > 45.0 else angle


def exactly_upright(u):
    return (u[0] == 0 and abs(u[1]) == 1) or (u[1] == 0 and abs(u[0]) == 1)


def components(nodes, edges):
    parent = {k: k for k in nodes}

    def find(k):
        while parent[k] != k:
            parent[k] = parent[parent[k]]
            k = parent[k]
        return k

    for a, b in edges:
        parent[find(a)] = find(b)
    groups = Counter(find(k) for k in nodes)
    return sorted(groups.values(), reverse=True)


def digits(value):
    return len(str(abs(value.numerator))), len(str(value.denominator))


def decimal_places(value):
    """The number of decimal places of a terminating decimal, else None."""
    den = value.denominator
    twos = fives = 0
    while den % 2 == 0:
        den //= 2
        twos += 1
    while den % 5 == 0:
        den //= 5
        fives += 1
    return max(twos, fives) if den == 1 else None


def main(argv):
    if len(argv) != 4:
        raise SystemExit(__doc__)
    path, form, out_path = argv[1:]
    packing, _ = r1_read.read_file(path, form)
    n, side = packing.n, packing.side
    frames = r1_frame.of_packing(packing)
    sq_a = r1_axes.of_packing(packing)
    tilts = [0.0 if exactly_upright(f.u) else tilt_degrees(f.u) for f in frames]
    upright = [k for k in range(n) if exactly_upright(frames[k].u)]
    turned = [k for k in range(n) if not exactly_upright(frames[k].u)]
    bands = {
        "exactly_upright": len(upright),
        "turned_below_1e-9_degrees": sum(1 for k in turned if abs(tilts[k]) < 1e-9),
        "turned_1e-9_to_1e-6_degrees": sum(1 for k in turned if 1e-9 <= abs(tilts[k]) < 1e-6),
        "turned_1e-6_to_1e-3_degrees": sum(1 for k in turned if 1e-6 <= abs(tilts[k]) < 1e-3),
        "turned_1e-3_to_1_degree": sum(1 for k in turned if 1e-3 <= abs(tilts[k]) < 1.0),
        "turned_beyond_1_degree": sum(1 for k in turned if abs(tilts[k]) >= 1.0),
    }
    tilted = [k for k in turned if abs(tilts[k]) >= 1.0]
    histogram = Counter()
    for k in tilted:
        low = int(math.floor(tilts[k] / 5.0)) * 5
        histogram[f"{low} to {low + 5}"] += 1
    edges = []
    least_between_tilted = None
    for x, i in enumerate(tilted):
        for j in tilted[x + 1 :]:
            value = r1_axes.margin(sq_a[i], sq_a[j])
            if value < NEAR:
                edges.append((i, j))
            if least_between_tilted is None or value < least_between_tilted:
                least_between_tilted = value
    blocks = components(tilted, edges)
    # squares nearly upright but not exactly: where they sit among the tilted and upright
    directions = Counter((f.u[0], f.u[1]) for f in frames)
    orientation = Counter()
    for f in frames:
        u = f.u
        # a square's orientation is its direction up to quarter turns: take the
        # representative with cos > 0 and sin >= 0
        cands = [(u[0], u[1]), (-u[1], u[0]), (-u[0], -u[1]), (u[1], -u[0])]
        rep = next(c for c in cands if c[0] > 0 and c[1] >= 0)
        orientation[rep] += 1
    contacts = {}
    clear = [r1_axes.clearances(a, side) for a in sq_a]
    for w, wall in enumerate(WALLS):
        rows = []
        for k in range(n):
            if clear[k][w] != 0:
                continue
            a = sq_a[k]
            coords = [q[0] if w in (0, 2) else q[1] for q in a.Q]
            extreme = min(coords) if w in (0, 1) else max(coords)
            rows.append((k + 1, sum(1 for c in coords if c == extreme)))
        contacts[wall] = {
            "squares": len(rows),
            "along_an_edge": [k for k, c in rows if c == 2],
            "at_one_corner": [k for k, c in rows if c == 1],
        }
    scalars = []
    for sq in packing.squares:
        if packing.form == "corners":
            for x, y in sq:
                scalars += [x, y]
        else:
            scalars += list(sq[:2])
    places = [decimal_places(v) for v in scalars]
    num_digits = [digits(v) for v in scalars]
    dir_digits = [digits(f.u[0])[1] for f in frames if not exactly_upright(f.u)]
    receipt = {
        "program": "r1_describe.py",
        "lane": "R1 (c-review-1005-1117)",
        "decides": "nothing",
        "file": os.path.basename(path),
        "form": form,
        "n": n,
        "tilts": bands,
        "largest_tilt_degrees": round(max((abs(t) for t in tilts), default=0.0), 6),
        "least_nonzero_tilt_degrees": min((abs(tilts[k]) for k in turned), default=None),
        "tilted_beyond_1_degree_by_5_degree_bin": dict(sorted(histogram.items(), key=lambda kv: int(kv[0].split()[0]))),
        "tilted_beyond_1_degree_range": (
            [round(min(tilts[k] for k in tilted), 6), round(max(tilts[k] for k in tilted), 6)]
            if tilted else None
        ),
        "tilted_squares": [k + 1 for k in tilted],
        "blocks_of_tilted_squares_joined_below_1e-6": blocks,
        "least_margin_between_tilted_squares": (
            r1_fmt.sci(least_between_tilted) if least_between_tilted is not None else None
        ),
        "distinct_directions_as_written": len(directions),
        "distinct_orientations": len(orientation),
        "commonest_orientations": [
            {"squares": count, "tilt_degrees": round(tilt_degrees(rep), 9),
             "denominator_digits": digits(rep[0])[1]}
            for rep, count in orientation.most_common(12)
        ],
        "direction_denominator_digits": (
            [min(dir_digits), max(dir_digits)] if dir_digits else None
        ),
        "wall_contacts": contacts,
        "position_scalars": {
            "what": "corner coordinates (corners file) or centre coordinates (centre file)",
            "count": len(scalars),
            "terminating_decimals": sum(1 for p in places if p is not None),
            "most_decimal_places": max((p for p in places if p is not None), default=None),
            "numerator_digits": [min(d[0] for d in num_digits), max(d[0] for d in num_digits)],
            "denominator_digits": [min(d[1] for d in num_digits), max(d[1] for d in num_digits)],
            "negative": sum(1 for v in scalars if v < 0),
        },
    }
    r1_fmt.write_json(out_path, receipt)
    print("DESCRIBED", receipt["file"], bands, "blocks", blocks[:6])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
