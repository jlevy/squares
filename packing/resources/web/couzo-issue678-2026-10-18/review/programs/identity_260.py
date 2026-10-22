"""Compare three n = 260 packings: T-196 (de Winter, center-basis JSON), the evand 14a9af8
seed (x y t text) and #678's n260.cert (x y t text), under the box's eight symmetries.

Counts, for the best symmetry, how many squares of one packing have a square of the other
within `tol` in centre (Euclidean, float) with the same axis set (angle mod 90 degrees).
Usage: python -I identity_260.py T196.json.gz SEED.cert.gz N260.cert
"""

from __future__ import annotations

import gzip
import json
import math
import sys
from fractions import Fraction
from pathlib import Path


def read_cert(text: str):
    rows = [ln.split() for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
    n, side = int(rows[0][0]), Fraction(rows[0][1])
    sq = []
    for x, y, t in rows[1:]:
        t = Fraction(t)
        d = 1 + t * t
        sq.append((Fraction(x), Fraction(y), (1 - t * t) / d, 2 * t / d))
    assert len(sq) == n
    return side, sq


def read_json(text: str):
    doc = json.loads(text)
    side = Fraction(doc["side"])
    sq = [(Fraction(s["center"][0]), Fraction(s["center"][1]), Fraction(s["basis"][0]), Fraction(s["basis"][1])) for s in doc["squares"]]
    assert len(sq) == doc["n"]
    return side, sq


def symmetries(side):
    S = side
    return {
        "id": lambda x, y: (x, y),
        "rot90": lambda x, y: (S - y, x),
        "rot180": lambda x, y: (S - x, S - y),
        "rot270": lambda x, y: (y, S - x),
        "flipx": lambda x, y: (S - x, y),
        "flipy": lambda x, y: (x, S - y),
        "diag": lambda x, y: (y, x),
        "anti": lambda x, y: (S - y, S - x),
    }


def angle_mod90(c, s):
    return math.degrees(math.atan2(float(s), float(c))) % 90.0


def compare(name_a, a, name_b, b, tol=1e-8):
    side_a, sq_a = a
    side_b, sq_b = b
    best = None
    for sym_name, f in symmetries(side_a).items():
        moved = [(*f(x, y), c, s) for x, y, c, s in sq_a]
        pts_b = [(float(x), float(y), angle_mod90(c, s)) for x, y, c, s in sq_b]
        matched, dists = 0, []
        for x, y, c, s in moved:
            fx, fy, fa = float(x), float(y), angle_mod90(c, s)
            d, da = min(((math.hypot(fx - bx, fy - by), abs(((fa - ba) + 45) % 90 - 45)) for bx, by, ba in pts_b))
            dists.append((d, da))
            if d <= tol and da <= 1e-6:
                matched += 1
        far = sorted(dists, reverse=True)
        if best is None or matched > best[1]:
            best = (sym_name, matched, far)
    sym_name, matched, far = best
    print(f"{name_a} vs {name_b}: side diff {float(side_a - side_b):+.3e}; best symmetry {sym_name}: {matched}/{len(sq_a)} within {tol} (centre) and 1e-6 deg (axes)")
    print("   largest centre displacements:", ", ".join(f"{d:.2e}" for d, _ in far[:8]))
    print("   displacement buckets: <1e-8:", sum(1 for d, _ in far if d <= 1e-8), " 1e-8..1e-4:", sum(1 for d, _ in far if 1e-8 < d <= 1e-4), " 1e-4..1e-2:", sum(1 for d, _ in far if 1e-4 < d <= 1e-2), " >1e-2:", sum(1 for d, _ in far if d > 1e-2))
    return sym_name, matched


def main():
    t196 = read_json(gzip.decompress(Path(sys.argv[1]).read_bytes()).decode())
    seed = read_cert(gzip.decompress(Path(sys.argv[2]).read_bytes()).decode())
    new = read_cert(Path(sys.argv[3]).read_text())
    print("sides: T-196", float(t196[0]), "seed", float(seed[0]), "#678", float(new[0]))
    print("axis-aligned counts: T-196", sum(1 for *_, c, s in t196[1] if s == 0 or c == 0), "seed", sum(1 for *_, c, s in seed[1] if s == 0 or c == 0), "#678", sum(1 for *_, c, s in new[1] if s == 0 or c == 0))
    compare("seed(14a9af8)", seed, "T-196", t196)
    compare("seed(14a9af8)", seed, "T-196", t196, tol=2e-8)
    compare("seed(14a9af8)", seed, "T-196", t196, tol=1e-7)
    compare("#678 n260", new, "seed(14a9af8)", seed)
    compare("#678 n260", new, "seed(14a9af8)", seed, tol=1e-4)
    compare("#678 n260", new, "T-196", t196, tol=1e-4)


main()
