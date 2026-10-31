"""Reviewer's exact preflight of the s(44) mixed cover (bold-ritchie-rev3), written for this
review from the format statement only; it shares no code with the source's sanity.py, zmx2,
zm_mixed.py or this repository's audit tools.

Checks, in exact integer/Fraction arithmetic:
  1. format: header 'mixed 1', side 7/1, D, W, np points, ns segments, 0 polygons, no
     trailing rows; every coordinate in [0, 7D]; every weight > 0 (or >= 0); every segment
     axis-parallel with positive length;
  2. the total mass sum(w)/W and whether it is < 44;
  3. D4 invariance of the point measure (aggregated by location) under all 8 symmetries of
     [0, 7]^2, and of the line measure: for each axis-parallel line, the density as a step
     function of the coordinate along the line (mass per unit length, exact), mapped by
     each symmetry to the image line, compared as canonical step functions.
It also reports which lines carry segments, the extreme point weights and the mass split.

Usage: python -I exact_check.py COVER
"""

from __future__ import annotations

import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

N_SQUARES = 44


def parse(path: Path):
    toks_rows = []
    for line in path.read_text(encoding="ascii").splitlines():
        t = line.split("#", 1)[0].split()
        if t:
            toks_rows.append(t)
    it = iter(toks_rows)
    assert next(it) == ["mixed", "1"]
    s_num, s_den = map(int, next(it))
    (d,) = map(int, next(it))
    (w,) = map(int, next(it))
    (np_,) = map(int, next(it))
    pts = [tuple(map(int, next(it))) for _ in range(np_)]
    (ns,) = map(int, next(it))
    segs = [tuple(map(int, next(it))) for _ in range(ns)]
    (npg,) = map(int, next(it))
    rest = list(it)
    return s_num, s_den, d, w, pts, segs, npg, rest


def main(path: Path) -> int:
    s_num, s_den, d, wden, pts, segs, npg, rest = parse(path)
    ok = True
    print(f"side {s_num}/{s_den}, D {d}, W {wden}, points {len(pts)}, segments {len(segs)}, polygons {npg}, trailing rows {len(rest)}")
    assert s_den == 1 and s_num == 7 and npg == 0 and not rest
    edge = s_num * d  # container [0, edge] in 1/D units
    for p in pts:
        assert len(p) == 3
        x, y, w = p
        if not (0 <= x <= edge and 0 <= y <= edge and w > 0):
            print("bad point", p)
            ok = False
    lines_used = set()
    for sg in segs:
        assert len(sg) == 5
        x0, y0, x1, y1, w = sg
        if not all(0 <= v <= edge for v in (x0, y0, x1, y1)) or w <= 0:
            print("bad segment", sg)
            ok = False
        if x0 == x1 and y0 != y1:
            lines_used.add(("v", x0))
        elif y0 == y1 and x0 != x1:
            lines_used.add(("h", y0))
        else:
            print("segment neither axis-parallel nor of positive length", sg)
            ok = False
    pmass = sum(p[2] for p in pts)
    smass = sum(s[4] for s in segs)
    total = Fraction(pmass + smass, wden)
    print(f"point mass {Fraction(pmass, wden)} = {pmass / wden:.9f}; segment mass {Fraction(smass, wden)} = {smass / wden:.9f}")
    print(f"total {total} = {float(total):.11f}; total < {N_SQUARES}: {total < N_SQUARES}; slack {float(N_SQUARES - total):.8f}")
    ok &= total < N_SQUARES
    print("lines carrying segments:", sorted(lines_used))
    print("point weights min/max:", min(p[2] for p in pts), max(p[2] for p in pts), "segment weights min/max:", min(s[4] for s in segs), max(s[4] for s in segs))

    # ---- D4 on points
    def g_apply(k: int, x: int, y: int) -> tuple[int, int]:
        swap, fx, fy = k & 4, k & 2, k & 1
        if swap:
            x, y = y, x
        if fx:
            x = edge - x
        if fy:
            y = edge - y
        return x, y

    agg: dict[tuple[int, int], int] = defaultdict(int)
    for x, y, w in pts:
        agg[(x, y)] += w
    pt_inv = all(agg.get(g_apply(k, x, y), 0) == w for k in range(8) for (x, y), w in agg.items())
    print("point measure D4-invariant (8 symmetries, aggregated):", pt_inv)
    ok &= pt_inv

    # ---- line densities: key ('v', x) or ('h', y) -> step function on the along-coordinate.
    # density = w / (W * length) per unit (1/D) length; keep as Fraction of w/length (W common).
    events: dict[tuple[str, int], dict[int, Fraction]] = defaultdict(lambda: defaultdict(Fraction))
    for x0, y0, x1, y1, w in segs:
        if x0 == x1:
            key, a, b = ("v", x0), min(y0, y1), max(y0, y1)
        else:
            key, a, b = ("h", y0), min(x0, x1), max(x0, x1)
        dens = Fraction(w, b - a)
        events[key][a] += dens
        events[key][b] -= dens

    def canon(ev: dict[int, Fraction]) -> tuple[tuple[int, int, Fraction], ...]:
        out: list[list] = []
        cur = Fraction(0)
        pos = sorted(ev)
        for i, p in enumerate(pos):
            cur += ev[p]
            if i + 1 < len(pos) and cur != 0:
                q = pos[i + 1]
                if out and out[-1][1] == p and out[-1][2] == cur:
                    out[-1][1] = q
                else:
                    out.append([p, q, cur])
        assert cur == 0
        return tuple(tuple(v) for v in out)

    lines = {k: canon(v) for k, v in events.items()}
    lines = {k: v for k, v in lines.items() if v}

    def map_line(k: int, key: tuple[str, int], f: tuple) -> tuple[tuple[str, int], tuple]:
        """Image of the density f on line key under symmetry k."""
        orient, c = key
        # represent each interval endpoint as a point on the line, map both, re-key
        img = []
        new_key = None
        for a, b, dens in f:
            if orient == "v":
                pa, pb = (c, a), (c, b)
            else:
                pa, pb = (a, c), (b, c)
            qa, qb = g_apply(k, *pa), g_apply(k, *pb)
            if qa[0] == qb[0]:
                nk, lo, hi = ("v", qa[0]), min(qa[1], qb[1]), max(qa[1], qb[1])
            else:
                nk, lo, hi = ("h", qa[1]), min(qa[0], qb[0]), max(qa[0], qb[0])
            assert new_key in (None, nk)
            new_key = nk
            img.append((lo, hi, dens))
        img.sort()
        ev: dict[int, Fraction] = defaultdict(Fraction)
        for lo, hi, dens in img:
            ev[lo] += dens
            ev[hi] -= dens
        return new_key, canon(ev)

    ln_inv = True
    for k in range(8):
        for key, f in lines.items():
            nk, img = map_line(k, key, f)
            if lines.get(nk) != img:
                ln_inv = False
                print("line density not invariant: symmetry", k, "line", key, "->", nk)
                break
    print("line measure D4-invariant (8 symmetries, canonical step densities):", ln_inv)
    ok &= ln_inv
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1])))
