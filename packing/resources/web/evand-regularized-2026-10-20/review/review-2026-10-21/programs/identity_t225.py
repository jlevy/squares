"""Pose-by-pose identity of each T-225 view against the packing it is credited to.

A measurement for lineage and credit; it decides no bound. Standard library only, with
review_t225_check's reader for the `n S` / `x y t` text certificates and a small reader
for de Winter's centre-basis JSON.

For a view V (side S_V) and a reference R (side S_R), each of the eight symmetries of
R's box [0, S_R]^2 is applied to R. Under each, two matchings are made:

* nearest centre: each square of V to the nearest centre of R; reported one to one or not;
* an optimal assignment: the bijection of least total squared centre displacement
  (Hungarian algorithm, binary64 costs), run on the two symmetries whose nearest-centre
  totals are least, keeping the one of least assignment cost.

Under the kept symmetry, each matched pair's centre displacement is computed exactly
(Fraction) and compared with each bound exactly; the orientation difference is the angle
between the two squares' edge directions modulo 90 degrees. The same is reported with R
also rescaled by S_V / S_R about the origin after the symmetry, which removes the part of
the displacement that is only the difference of the sides.

Usage: python -I identity_t225.py DATA_DIR OUT.json
DATA_DIR holds packet/ (the copied packet), compare/ (T-223, T-199, T-196 copies) and
fetched-672/n227.cert (franciscouzo/square-packing@af8cb79, SHA-256 checked here).
"""

from __future__ import annotations

import gzip
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import review_t225_check as check  # noqa: E402

COUZO_672_SHA256 = "65b03df883e75f890eca985232252a6340b9b5da3437c41275c9201df03d8c17"
BOUNDS = ("1e-9", "1e-6", "1e-3", "1e-2", "1e-1")
NAMES = ["identity", "mirror x", "mirror y", "half turn", "transpose", "quarter turn", "quarter turn back", "anti-transpose"]


def from_text(text: str) -> tuple[Fraction, list[tuple]]:
    n = int(next(line for line in text.split("\n") if line and not line.startswith("#")).split(" ")[0])
    side, rows = check.read_certificate(text, n)
    squares = []
    for x, y, t in rows:
        x, y, t = Fraction(*x), Fraction(*y), Fraction(*t)
        squares.append((x, y, (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)))
    return Fraction(*side), squares


def from_centre_basis(raw: bytes) -> tuple[Fraction, list[tuple]]:
    document = json.loads(gzip.decompress(raw))
    squares = []
    for square in document["squares"]:
        x, y = (Fraction(v) for v in square["center"])
        c, s = (Fraction(v) for v in square["basis"])
        if c * c + s * s != 1:
            raise ValueError("basis off the unit circle")
        squares.append((x, y, c, s))
    return Fraction(document["side"]), squares


def symmetric(side: Fraction, square: tuple, k: int) -> tuple:
    """Symmetry k of the box [0, side]^2 applied to a square (centre and edge direction)."""
    x, y, c, s = square
    if k & 4:  # transpose first
        x, y, c, s = y, x, s, c
    if k & 1:  # mirror in x
        x, c = side - x, -c
    if k & 2:  # mirror in y
        y, s = side - y, -s
    return (x, y, c, s)


def hungarian(cost: list[list[float]]) -> list[int]:
    """Least-cost perfect matching of a square cost matrix: row i -> column result[i]."""
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
                    current = row[j - 1] - ui0 - v[j]
                    if current < minv[j]:
                        minv[j] = current
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
    result = [0] * n
    for j in range(1, n + 1):
        result[p[j] - 1] = j - 1
    return result


def turn_degrees(a: tuple, b: tuple) -> float:
    _x, _y, c, s = a
    _u, _v, p, q = b
    sine = abs(c * q - s * p)
    cosine = abs(c * p + s * q)
    return math.degrees(math.atan2(float(min(sine, cosine)), float(max(sine, cosine))))


def describe(view: list[tuple], mapped: list[tuple], match: list[int]) -> dict:
    squared = [(view[i][0] - mapped[j][0]) ** 2 + (view[i][1] - mapped[j][1]) ** 2 for i, j in enumerate(match)]
    turns = [turn_degrees(view[i], mapped[j]) for i, j in enumerate(match)]
    out = {
        "within_1e-6": sum(1 for d in squared if d <= Fraction(1, 10**12)),
        "beyond": {b: sum(1 for d in squared if d > Fraction(b) ** 2) for b in BOUNDS},
        "largest_move": f"{math.sqrt(float(max(squared))):.6g}",
        "largest_turn_degrees": f"{max(turns):.4g}",
        "turned_beyond_1e-6_degrees": sum(1 for t in turns if t > 1e-6),
        "turned_beyond_degrees": {b: sum(1 for t in turns if t > float(b)) for b in ("1e-6", "1e-3", "1e-2", "1e-1", "1")},
        "most_turned": [
            {
                "view_square": i,
                "turn_degrees": f"{turns[i]:.4g}",
                "move": f"{math.sqrt(float(squared[i])):.3g}",
                "view_angle_degrees": f"{angle(view[i]):.4f}",
                "reference_angle_degrees": f"{angle(mapped[match[i]]):.4f}",
            }
            for i in sorted(range(len(turns)), key=lambda k: -turns[k])[:8]
            if turns[i] > 1e-6
        ],
    }
    return out


def angle(square: tuple) -> float:
    """The square's edge direction in degrees, modulo 90, in [0, 90)."""
    _x, _y, c, s = square
    return math.degrees(math.atan2(float(s), float(c))) % 90.0


def measure(view_packing: tuple, reference_packing: tuple) -> dict:
    side_v, view = view_packing
    side_r, reference = reference_packing
    fv = [(float(x), float(y)) for x, y, _c, _s in view]
    candidates = []
    for k in range(8):
        mapped = [symmetric(side_r, sq, k) for sq in reference]
        fr = [(float(x), float(y)) for x, y, _c, _s in mapped]
        nearest = []
        total = 0.0
        for vx, vy in fv:
            best = min(range(len(fr)), key=lambda j: (fr[j][0] - vx) ** 2 + (fr[j][1] - vy) ** 2)
            nearest.append(best)
            total += (fr[best][0] - vx) ** 2 + (fr[best][1] - vy) ** 2
        candidates.append((total, k, mapped, fr, nearest))
    candidates.sort(key=lambda c: c[0])
    nearest_one_to_one = [NAMES[k] for _t, k, _m, _f, near in candidates if len(set(near)) == len(near)]
    best = None
    for _total, k, mapped, fr, _near in candidates[:2]:
        cost = [[(fr[j][0] - vx) ** 2 + (fr[j][1] - vy) ** 2 for j in range(len(fr))] for vx, vy in fv]
        match = hungarian(cost)
        value = sum(cost[i][j] for i, j in enumerate(match))
        if best is None or value < best[0]:
            best = (value, k, mapped, match)
    _value, k, mapped, match = best
    scale = side_v / side_r
    rescaled = [(x * scale, y * scale, c, s) for x, y, c, s in mapped]
    return {
        "side_view": f"{side_v.numerator}/{side_v.denominator}",
        "side_reference": f"{side_r.numerator}/{side_r.denominator}",
        "view_below_reference_by": f"{float(side_r - side_v):.6e}",
        "nearest_centre_one_to_one_under": nearest_one_to_one,
        "assignment_symmetry": NAMES[k],
        "assignment": describe(view, mapped, match),
        "assignment_reference_rescaled_to_view_side": describe(view, rescaled, match),
    }


def main(argv: list[str]) -> int:
    data, out = Path(argv[1]), Path(argv[2])
    certs = data / "packet/source/search/regularize/lists/certs"
    views = {n: from_text(gzip.decompress((certs / f"n-{n:03d}.cert.gz").read_bytes()).decode("ascii")) for n in (204, 227, 229, 260)}
    raw672 = (data / "fetched-672/n227.cert").read_bytes()
    digest = hashlib.sha256(raw672).hexdigest()
    if digest != COUZO_672_SHA256:
        raise SystemExit(f"#672 n227.cert has SHA-256 {digest}")
    p672 = from_text(raw672.decode("ascii"))
    t223 = {n: from_text((data / f"compare/t223-n{n}.cert").read_text("ascii")) for n in (204, 260)}
    t199 = from_text((data / "compare/t199-s229_v2.cert").read_text("ascii"))
    t196 = {n: from_centre_basis((data / f"compare/t196-n{n}_exact.json.gz").read_bytes()) for n in (227, 260)}
    pairs = [
        (204, "view", "T-223 (#678)", views[204], t223[204]),
        (227, "view", "#672 (af8cb79)", views[227], p672),
        (227, "view", "T-196 (#668)", views[227], t196[227]),
        (227, "#672 (af8cb79)", "T-196 (#668)", p672, t196[227]),
        (229, "view", "T-199 (#674 update)", views[229], t199),
        (260, "view", "T-223 (#678)", views[260], t223[260]),
        (260, "view", "T-196 (#668)", views[260], t196[260]),
    ]
    result = {"couzo_672": {"sha256": digest, "side": f"{p672[0].numerator}/{p672[0].denominator}"}, "pairs": []}
    for n, a, b, first, second in pairs:
        row = {"n": n, "measured": a, "against": b, **measure(first, second)}
        result["pairs"].append(row)
        print(json.dumps(row), flush=True)
    out.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
