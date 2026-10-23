#!/usr/bin/env python3
"""Pose-by-pose identity measurement of the T-229 review (lane c-review-t229-math).

Standard library only; a measurement, which decides nothing. For each pair (A, B) of
packings it applies the eight symmetries of B's box [0, S_B]^2 to B and measures how far
A lies from each image:

* whether nearest centres pair the squares one to one under that symmetry;
* the least total squared displacement over all assignments, by this program's own
  Hungarian algorithm (O(n^3), on binary64 squared distances); a symmetry is skipped only
  when the sum over A's squares of the least squared distance to any centre of B's image,
  a lower bound on every assignment's total, already exceeds the best total found;
* under the symmetry and assignment of least total: the squares within 1e-6 and beyond
  1e-3, 1e-2 and 1e-1 (each displacement compared with the threshold exactly, in
  Fraction), the largest move, and turns modulo 90 degrees (a reflection negates the
  angle), with the count beyond 1 degree;
* the tilted squares of each packing (neither cos nor sin zero, exactly).

It reads the source's certificate format (x y t rows) with review_t229_check.read_cert_text
and Witness/v2 centre-basis facts with a lenient reader of its own that accepts any other
top-level key (the house witnesses carry certificate and source blocks).

Usage: identity_t229.py OUT.json LABEL=PATH [...] -- A:B [A:B ...] [--focus A:B]
"""

import gzip
import json
import math
import os
import re
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import review_t229_check as rc  # noqa: E402

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def read_any(path):
    raw = open(path, "rb").read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    text = raw.decode("utf-8")
    if "\nwitness:" not in "\n" + text:
        pk = rc.read_cert_text(text)
        rows = []
        for r in pk["squares"]:
            t = Fraction(*r["rot"][1])
            d = 1 + t * t
            rows.append((Fraction(*r["x"]), Fraction(*r["y"]), (1 - t * t) / d, 2 * t / d))
        return Fraction(*pk["side"]), rows
    lines = text.split("\n")
    side = None
    rows = []
    i = lines.index("witness:") + 1
    while i < len(lines):
        line = lines[i]
        if line.startswith("  side: "):
            side = Fraction(rc._unquote(line[8:]))
        if line == "  squares:":
            i += 1
            while i < len(lines) and lines[i].startswith("  - id: "):
                vals = {}
                i += 1
                while i < len(lines) and lines[i].startswith("    "):
                    m = re.match(r"    (center|basis):$", lines[i])
                    if m:
                        a = Fraction(rc._unquote(lines[i + 1][6:]))
                        b = Fraction(rc._unquote(lines[i + 2][6:]))
                        vals[m.group(1)] = (a, b)
                        i += 3
                    else:
                        i += 1
                (x, y), (c, s) = vals["center"], vals["basis"]
                if c * c + s * s != 1:
                    raise ValueError("basis is not a unit vector")
                rows.append((x, y, c, s))
            continue
        if line and not line.startswith(" "):
            break
        i += 1
    return side, rows


def theta(c, s):
    """The square's orientation modulo 90 degrees, in [0, 90)."""
    return math.degrees(math.atan2(float(s), float(c))) % 90.0


SYMS = [
    ("identity", lambda x, y, S: (x, y), False),
    ("quarter turn", lambda x, y, S: (S - y, x), False),
    ("half turn", lambda x, y, S: (S - x, S - y), False),
    ("three-quarter turn", lambda x, y, S: (y, S - x), False),
    ("mirror x", lambda x, y, S: (S - x, y), True),
    ("mirror y", lambda x, y, S: (x, S - y), True),
    ("transpose", lambda x, y, S: (y, x), True),
    ("anti-transpose", lambda x, y, S: (S - y, S - x), True),
]


def hungarian(cost):
    """Least-cost assignment of rows to columns, n x n, by potentials (O(n^3))."""
    n = len(cost)
    inf = float("inf")
    u = [0.0] * (n + 1)
    v = [0.0] * (n + 1)
    p = [0] * (n + 1)
    way = [0] * (n + 1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [inf] * (n + 1)
        used = [False] * (n + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            row = cost[i0 - 1]
            ui0 = u[i0]
            delta = inf
            j1 = 0
            for j in range(1, n + 1):
                if not used[j]:
                    cur = row[j - 1] - ui0 - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    out = [0] * n
    for j in range(1, n + 1):
        if p[j]:
            out[p[j] - 1] = j - 1
    return out


THRESH = [("within_1e-6", Fraction(1, 10**6)), ("beyond_1e-3", Fraction(1, 10**3)),
          ("beyond_1e-2", Fraction(1, 10**2)), ("beyond_1e-1", Fraction(1, 10))]


def compare(A, B):
    SA, ra = A
    SB, rb = B
    n = len(ra)
    fa = [(float(x), float(y)) for (x, y, c, s) in ra]
    results = []
    for name, f, refl in SYMS:
        img = [f(x, y, SB) for (x, y, c, s) in rb]
        fb = [(float(x), float(y)) for (x, y) in img]
        cost = [[(ax - bx) ** 2 + (ay - by) ** 2 for (bx, by) in fb] for (ax, ay) in fa]
        nearest = [min(range(n), key=row.__getitem__) for row in cost]
        lower = sum(row[k] for row, k in zip(cost, nearest))
        results.append({"symmetry": name, "reflection": refl, "img": img, "cost": cost,
                        "one_to_one": len(set(nearest)) == n, "lower": lower})
    best = None
    for r in sorted(results, key=lambda r: r["lower"]):
        if best is not None and r["lower"] > best["total"]:
            r["skipped"] = True
            continue
        assign = hungarian(r["cost"])
        r["assign"] = assign
        r["total"] = sum(r["cost"][i][assign[i]] for i in range(n))
        if best is None or r["total"] < best["total"]:
            best = r
    out = {"one_to_one_under": [r["symmetry"] for r in results if r["one_to_one"]],
           "best_symmetry": best["symmetry"], "best_total_squared": best["total"],
           "hungarian_runs": sum(1 for r in results if "assign" in r)}
    counts = {k: 0 for k, _ in THRESH}
    largest = Fraction(0)
    turns = []
    far = []
    for i, j in enumerate(best["assign"]):
        x, y, c, s = ra[i]
        bx, by = best["img"][j]
        d2 = (x - bx) ** 2 + (y - by) ** 2
        for k, t in THRESH:
            if k.startswith("within"):
                counts[k] += d2 <= t * t
            else:
                counts[k] += d2 > t * t
        if d2 > Fraction(1, 100):
            far.append((i + 1, j + 1, math.sqrt(float(d2))))
        largest = max(largest, d2)
        ta = theta(c, s)
        tb = theta(rb[j][2], rb[j][3])
        if best["reflection"]:
            tb = (-tb) % 90.0
        turn = (ta - tb + 45.0) % 90.0 - 45.0
        turns.append((abs(turn), i + 1, j + 1))
    turns.sort(reverse=True)
    # Squares axis-aligned (cos or sin exactly zero) in one packing and tilted in the other.
    tilted_a_only = sum(1 for i, j in enumerate(best["assign"])
                        if ra[i][2] != 0 and ra[i][3] != 0 and (rb[j][2] == 0 or rb[j][3] == 0))
    tilted_b_only = sum(1 for i, j in enumerate(best["assign"])
                        if (ra[i][2] == 0 or ra[i][3] == 0) and rb[j][2] != 0 and rb[j][3] != 0)
    out["tilted_in_a_only"] = tilted_a_only
    out["tilted_in_b_only"] = tilted_b_only
    out.update(counts)
    out["largest_move"] = math.sqrt(float(largest))
    out["largest_turn_deg"] = turns[0][0]
    out["turned_beyond_1deg"] = sum(1 for t in turns if t[0] > 1.0)
    out["largest_turns"] = [{"deg": round(t, 4), "square": a, "partner": b} for t, a, b in turns[:6]]
    out["moved_beyond_1e-1"] = [{"square": a, "partner": b, "move": round(m, 6)} for a, b, m in far]
    out["assignment"] = best["assign"]
    return out


def tilted(rows):
    return sum(1 for (x, y, c, s) in rows if c != 0 and s != 0)


def square_clearance(side, rows, k):
    """Square k's least separating-axis gap to every other square and its least wall
    clearance, exactly (Fraction): a measurement of how loose it sits."""
    x, y, c, s = rows[k]
    h = (abs(c) + abs(s)) / 2
    wall = min(x - h, y - h, side - x - h, side - y - h)
    gaps = []
    for j, (xj, yj, cj, sj) in enumerate(rows):
        if j == k:
            continue
        dx, dy = xj - x, yj - y
        C = abs(c * cj + s * sj)
        S = abs(c * sj - s * cj)
        R = Fraction(1, 2) + (C + S) / 2
        g = max(abs(c * dx + s * dy), abs(-s * dx + c * dy), abs(cj * dx + sj * dy),
                abs(-sj * dx + cj * dy)) - R
        gaps.append((g, j + 1))
    gaps.sort()
    return {"square": k + 1, "theta_deg": round(theta(c, s), 6), "least_pair_gap": float(gaps[0][0]),
            "against": gaps[0][1], "least_wall_clearance": float(wall),
            "nearest_four": [[j, float(g)] for g, j in gaps[:4]],
            "neighbours_within_1e-9": sum(1 for g, _ in gaps if g < Fraction(1, 10**9))}


def main(argv):
    out_path = argv[0]
    sep = argv.index("--")
    specs, rest = argv[1:sep], argv[sep + 1:]
    focus = []
    if "--focus" in rest:
        f = rest.index("--focus")
        focus = rest[f + 1:]
        rest = rest[:f]
    packs = {}
    for spec in specs:
        label, path = spec.split("=", 1)
        packs[label] = read_any(path)
        print(f"{label}: n={len(packs[label][1])} side={float(packs[label][0]):.16f} "
              f"tilted={tilted(packs[label][1])}")
    report = {"packings": {k: {"n": len(v[1]), "side": float(v[0]), "tilted": tilted(v[1])}
                           for k, v in packs.items()}, "comparisons": []}
    for pair in rest:
        a, b = pair.split(":")
        res = compare(packs[a], packs[b])
        res["a"], res["b"] = a, b
        print(f"{a} against {b}: one to one under {res['one_to_one_under'] or 'no symmetry'}; "
              f"best {res['best_symmetry']}; within 1e-6 {res['within_1e-6']}, beyond 1e-3 "
              f"{res['beyond_1e-3']}, 1e-2 {res['beyond_1e-2']}, 0.1 {res['beyond_1e-1']}; largest "
              f"move {res['largest_move']:.4g}; largest turn {res['largest_turn_deg']:.4g} deg; turned "
              f">1 deg {res['turned_beyond_1deg']}; turns {res['largest_turns'][:4]} "
              f"tilted only in A {res['tilted_in_a_only']}, only in B {res['tilted_in_b_only']} (Hungarian runs {res['hungarian_runs']})")
        if pair in focus:
            sq = res["largest_turns"][0]
            res["focus"] = {a: square_clearance(packs[a][0], packs[a][1], sq["square"] - 1),
                            b: square_clearance(packs[b][0], packs[b][1], sq["partner"] - 1)}
            # How far, centre to centre in A, each square moved beyond a tenth lies from it.
            fx, fy = packs[a][1][sq["square"] - 1][:2]
            res["focus"]["moved_beyond_1e-1_from_focus"] = [
                {"square": m["square"], "move": m["move"],
                 "centre_distance": round(math.hypot(float(packs[a][1][m["square"] - 1][0] - fx),
                                                     float(packs[a][1][m["square"] - 1][1] - fy)), 4)}
                for m in res["moved_beyond_1e-1"]]
            print(f"    the most-turned square: {json.dumps(res['focus'])}")
        report["comparisons"].append(res)
    with open(out_path, "w") as fh:
        json.dump(report, fh, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
