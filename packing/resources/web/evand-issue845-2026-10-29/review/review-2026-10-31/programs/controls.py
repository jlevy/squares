"""Sharp controls for exact_check.py (review bold-ritchie-rv-daniel).

For each certificate, writes mutated certificates to an output directory and decides each
with both methods of exact_check.py. Expected outcomes are fixed here, before any run.
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exact_check as ec  # noqa: E402

EPS = F(1, 10**30)


def tok(q: F) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def write(path: str, n: int, side: F, rows) -> None:
    with open(path, "w", encoding="ascii") as fh:
        fh.write("# control\n")
        fh.write(f"{n} {tok(side)}\n")
        for x, y, t in rows:
            fh.write(f"{tok(x)} {tok(y)} {tok(t)}\n")


def best_axis(p, q):
    """Return (gap, wx, wy, sign) for the best separating axis of p, q; sign*w points p -> q."""
    best = None
    for owner, other in ((p, q), (q, p)):
        ax, ay, ac, as_ = owner
        bx, by, bc, bs = other
        dx, dy = bx - ax, by - ay
        for wx, wy in ((ac, as_), (-as_, ac)):
            centre = dx * wx + dy * wy
            ub = abs(bc * wx + bs * wy)
            vb = abs(-bs * wx + bc * wy)
            gap = abs(centre) - ec.HALF - (ub + vb) / 2
            sign = 1 if centre >= 0 else -1
            if owner is q:
                sign = -sign  # centre measured q -> p; flip so sign*w points p -> q
            if best is None or gap > best[0]:
                best = (gap, wx, wy, sign)
    return best


def run(cert: str, outdir: str) -> list[dict]:
    n, side, rows, _ = ec.read_cert(cert)
    base = ec.check(cert, "both")
    sq = []
    for x, y, t in rows:
        c, s = ec.frame(t)
        sq.append((x, y, c, s))
    ext = F(base["extent_exact"])
    stem = os.path.join(outdir, os.path.basename(cert).replace(".cert", ""))
    controls: list[tuple[str, str, int, F, list]] = []
    controls.append(("box at extent", "accept", n, ext, rows))
    controls.append(("box 1e-30 below extent", "refuse", n, ext - EPS, rows))
    # near walls: least x and y clearance separately
    cs = [ec.corners(*q) for q in sq]
    cx = min(min(p[0] for p in c4) for c4 in cs)
    cy = min(min(p[1] for p in c4) for c4 in cs)
    moved = [(x - cx, y - cy, t) for x, y, t in rows]
    controls.append(("all squares onto the near walls", "accept", n, side, moved))
    moved2 = [(x - cx - EPS, y - cy - EPS, t) for x, y, t in rows]
    controls.append(("the same, 1e-30 further", "refuse", n, side, moved2))
    # closest pair
    i, j = base["least_pair_gap"][1], base["least_pair_gap"][2]
    gap, wx, wy, sign = best_axis(sq[i], sq[j])
    xj, yj, tj = rows[j]
    shut = list(rows)
    shut[j] = (xj - sign * gap * wx, yj - sign * gap * wy, tj)
    controls.append((f"closest pair ({i}, {j}) closed by its gap", "accept", n, side, shut))
    past = list(rows)
    past[j] = (xj - sign * (gap + EPS) * wx, yj - sign * (gap + EPS) * wy, tj)
    controls.append((f"the same, 1e-30 further", "refuse", n, side, past))
    # square 0 moved 1e-30 past its own near-wall clearance (x direction)
    x0, y0, t0 = rows[0]
    c0 = min(p[0] for p in cs[0])
    controls.append(("square 0 moved 1e-30 past its x wall clearance", "refuse", n, side,
                     [(x0 - c0 - EPS, y0, t0)] + list(rows[1:])))
    # duplicate
    controls.append(("square 0 duplicated", "refuse", n + 1, side, list(rows) + [rows[0]]))
    # rotation sense reversed
    controls.append(("rotation sense reversed (t -> -t)", "refuse" if base["tilted"] else "accept",
                     n, side, [(x, y, -t) for x, y, t in rows]))
    # mirror
    controls.append(("mirror x -> S - x, t -> -t", "accept", n, side,
                     [(side - x, y, -t) for x, y, t in rows]))
    out = []
    for k, (name, expect, nn, sd, rr) in enumerate(controls):
        path = f"{stem}.control{k:02d}.cert"
        write(path, nn, sd, rr)
        r = ec.check(path, "both")
        a = "accept" if r["A_valid"] else "refuse"
        b = "accept" if r["B_valid"] else "refuse"
        detail = {
            "A_walls_ok": r["A_walls_ok"],
            "A_pairs_overlapping": r.get("A_pairs_overlapping"),
            "A_first": r.get("A_first_overlaps", [])[:2],
            "B_walls_bad": r.get("B_walls_bad"),
            "B_pairs_positive_area": r.get("B_pairs_positive_area"),
            "B_first": r.get("B_first_overlaps", [])[:2],
        }
        row = {"control": name, "expected": expect, "A": a, "B": b,
               "as_expected": a == expect and b == expect, "detail": detail}
        out.append(row)
        print(json.dumps(row))
        sys.stdout.flush()
        os.remove(path)
    return out


if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for cert in sys.argv[2:]:
        print(f"== {cert}")
        res = run(cert, outdir)
        print(f"== {os.path.basename(cert)}: {sum(r['as_expected'] for r in res)}/{len(res)} as expected")
