"""Lane L169 lineage (after the freeze): the certificate against Joost de Winter's 157.

Usage: l169_lineage.py N157_EXACT_JSON CERT OUT_JSON OUT_SEED_CERT

It decides nothing; everything is measured in binary64.

1. The symmetry: for each of the eight symmetries of de Winter's box, the translations
   carrying his tilted squares onto the certificate's tilted squares (angles within 6
   degrees mod 90), binned to 0.1; the peak count says which symmetry is used.
2. Copy A: the translation, refined on the certificate squares within 0.02 of an image.
3. The crop of the README: the full width, from the bottom of de Winter's box to the top
   of the band, every square wholly inside; the band's top is the top of the highest
   square below the README's 9.353384, kept exactly.
4. The pitch: the least vertical offset at which the band and a copy of it shifted
   horizontally by 0, +1 or -1 have disjoint interiors (bisection on separating axes).
5. The seed: copy A and copy B = A + (sigma, 9.019403), every square whose centre lies in
   the certificate's box; the windows of side 10 that hold exactly the squares paired
   with the certificate; the seed's overlaps and wall crossings; and the certificate's
   moves from it (nearest centres, and the optimal one-to-one assignment).
The seed is written as `.cert` text with binary64 values as exact rationals, for the
repository's identity tool.
"""

from __future__ import annotations

import json
import math
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves it off

import l169_reader as rd

Sq = tuple[float, float, float]


def amod(a: float) -> float:
    return (a + 45.0) % 90.0 - 45.0


def corners(x: float, y: float, a: float) -> list[tuple[float, float]]:
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    ux, uy, vx, vy = c / 2, s / 2, -s / 2, c / 2
    return [(x - ux - vx, y - uy - vy), (x + ux - vx, y + uy - vy), (x + ux + vx, y + uy + vy), (x - ux + vx, y - uy + vy)]


def margin(p: Sq, q: Sq) -> float:
    cp, cq = corners(*p), corners(*q)
    best = -1e9
    for a in (p[2], q[2]):
        for ang in (a, a + 90):
            nx, ny = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            pp = [nx * x + ny * y for x, y in cp]
            pq = [nx * x + ny * y for x, y in cq]
            best = max(best, min(pq) - max(pp), min(pp) - max(pq))
    return best


def sym(k: int, S: float):
    maps = [
        ("identity", lambda x, y: (x, y), 1),
        ("quarter", lambda x, y: (S - y, x), 1),
        ("half", lambda x, y: (S - x, S - y), 1),
        ("three-quarter", lambda x, y: (y, S - x), 1),
        ("mirror-x", lambda x, y: (S - x, y), -1),
        ("mirror-y", lambda x, y: (x, S - y), -1),
        ("transpose", lambda x, y: (y, x), -1),
        ("anti-transpose", lambda x, y: (S - y, S - x), -1),
    ]
    return maps[k]


def nearest_all(cert: list[Sq], seed: list) -> list[int]:
    return [min(range(len(seed)), key=lambda q, c=c: math.hypot(seed[q][0] - c[0], seed[q][1] - c[1])) for c in cert]


def assignment(a, b):
    """Optimal one-to-one assignment by centre distance (Hungarian, O(n^3))."""
    n = len(a)
    cost = [[math.hypot(a[i][0] - b[j][0], a[i][1] - b[j][1]) for j in range(n)] for i in range(n)]
    INF = float("inf")
    u = [0.0] * (n + 1)
    v = [0.0] * (n + 1)
    p = [0] * (n + 1)
    way = [0] * (n + 1)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [INF] * (n + 1)
        used = [False] * (n + 1)
        while True:
            used[j0] = True
            i0, delta, j1 = p[j0], INF, 0
            for j in range(1, n + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j], way[j] = cur, j0
                    if minv[j] < delta:
                        delta, j1 = minv[j], j
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
    res = [0] * n
    for j in range(1, n + 1):
        res[p[j] - 1] = j - 1
    return res


def least_pitch(band: list[Sq], dx: float) -> float:
    def ok(pitch: float) -> bool:
        for a in band:
            for b in band:
                q = (b[0] + dx, b[1] + pitch, b[2])
                if abs(q[1] - a[1]) < 1.5 and abs(q[0] - a[0]) < 1.5 and margin(a, q) < 0:
                    return False
        return True

    lo, hi = 0.0, 12.0
    for _ in range(50):
        mid = (lo + hi) / 2
        if ok(mid):
            hi = mid
        else:
            lo = mid
    return hi


def main(argv: list[str]) -> int:
    d = json.load(open(argv[1]))
    S157 = float(F(d["side"]))
    src0: list[Sq] = []
    for cx, cy, c, s in d["squares"]:
        src0.append((float(F(cx)), float(F(cy)), amod(math.degrees(math.atan2(float(F(s)), float(F(c)))))))
    rdg = rd.read_file(argv[2])
    S = float(F(*rdg["side"]))
    cert: list[Sq] = []
    for x, y, t in rdg["squares"]:
        cert.append((float(F(*x)), float(F(*y)), math.degrees(2 * math.atan(float(F(*t))))))
    out: dict = {"program": "l169_lineage.py", "source_157_side": S157,
                 "source_157_tilts": sorted({round(a, 2) for _, _, a in src0 if abs(a) > 0.5}),
                 "source_157_tilted": sum(1 for s in src0 if abs(s[2]) > 0.5)}
    # 1. The symmetry.
    tc = [c for c in cert if abs(c[2]) > 0.5]
    hist = {}
    for k in range(8):
        name, f, sg = sym(k, S157)
        src = [(*f(x, y), amod(sg * a)) for x, y, a in src0 if abs(a) > 0.5]
        H: dict = {}
        for c in tc:
            for s in src:
                if abs(amod(s[2] - c[2])) < 6:
                    key = (round(c[0] - s[0], 1), round(c[1] - s[1], 1))
                    H[key] = H.get(key, 0) + 1
        hist[name] = [[list(k_), v] for k_, v in sorted(H.items(), key=lambda kv: -kv[1])[:3]]
    out["tilted_translation_peaks"] = hist
    # 2. Copy A.
    T = tuple(hist["identity"][0][0])
    for _ in range(2):
        near = nearest_all(cert, [(x + T[0], y + T[1], a) for x, y, a in src0])
        tight = [(i, j) for i, j in enumerate(near)
                 if math.hypot(src0[j][0] + T[0] - cert[i][0], src0[j][1] + T[1] - cert[i][1]) < 0.02
                 and abs(amod(src0[j][2] - cert[i][2])) < 0.5]
        T = (sum(cert[i][0] - src0[j][0] for i, j in tight) / len(tight),
             sum(cert[i][1] - src0[j][1] for i, j in tight) / len(tight))
    out["copy_A_translation"] = T
    out["copy_A_tight_matches"] = len(tight)
    # 3. The crop.
    tops = sorted((max(q[1] for q in corners(*s)), j) for j, s in enumerate(src0))
    h_readme = 9.353384
    h = max(t for t, _ in tops if t <= h_readme + 5e-7)
    top_sq = [j for t, j in tops if t == h][0]
    band_idx = [j for j, s in enumerate(src0) if min(q[1] for q in corners(*s)) >= -1e-9 and max(q[1] for q in corners(*s)) <= h + 1e-12]
    band = [src0[j] for j in band_idx]
    nxt = min(t for t, _ in tops if t > h + 1e-12)
    out["crop"] = {"height": h, "readme_height": h_readme, "top_square_index_0_based": top_sq,
                   "top_square": src0[top_sq], "next_top_above": nxt, "squares": len(band),
                   "tilted": sum(1 for s in band if abs(s[2]) > 0.5)}
    # 4. The pitch.
    out["least_pitch"] = {str(dx): least_pitch(band, dx) for dx in (0.0, 1.0, -1.0)}
    # 5. The seed.
    p = 9.019403
    seeds = {}
    for sigma in (1, -1):
        seed = []
        for m in (-1, 0, 1):
            for j, s in zip(band_idx, band, strict=True):
                X, Y = s[0] + T[0] + m * sigma, s[1] + T[1] + m * p
                if 0 <= X <= S and 0 <= Y <= S:
                    seed.append((X, Y, s[2], m, j))
        near = nearest_all(cert, seed)
        seeds[sigma] = (seed, near)
        out[f"seed_sigma_{sigma:+d}"] = {
            "centres_in_box": len(seed),
            "by_copy": {str(m): sum(1 for s in seed if s[3] == m) for m in (-1, 0, 1)},
            "certificate_squares_with_a_distinct_nearest": len(set(near)),
            "largest_nearest_distance": max(math.hypot(seed[near[i]][0] - cert[i][0], seed[near[i]][1] - cert[i][1]) for i in range(90)),
            "seed_squares_nearest_to_none": [[k, seed[k][0], seed[k][1], seed[k][2]] for k in range(len(seed)) if k not in set(near)],
        }
    seed, near = seeds[1]
    keep = sorted(set(near))
    dropped = [k for k in range(len(seed)) if k not in set(near)]
    # Windows of side 10, bottom edge at 0, whose centres-inside set is exactly `keep`.
    ws = []
    for i in range(-600, 601):
        w = i / 1000
        inside = [k for k, s in enumerate(seed) if w <= s[0] <= w + 10 and 0 <= s[1] <= 10]
        if inside == keep:
            ws.append(w)
    seed90 = [seed[k] for k in keep]
    ov = []
    for i in range(90):
        for j in range(i + 1, 90):
            g = margin(seed90[i][:3], seed90[j][:3])
            if g < -1e-9:
                ov.append((g, i, j))
    ov.sort()
    wall = []
    for i, (x, y, a, _m, _j) in enumerate(seed90):
        cs = corners(x, y, a)
        c = min(min(q[0] for q in cs), min(q[1] for q in cs), S - max(q[0] for q in cs), S - max(q[1] for q in cs))
        if c < -1e-9:
            wall.append((c, i))
    perm = assignment([c[:2] for c in cert], [s[:2] for s in seed90])
    moves = [math.hypot(cert[i][0] - seed90[perm[i]][0], cert[i][1] - seed90[perm[i]][1]) for i in range(90)]
    turns = [abs(amod(cert[i][2] - seed90[perm[i]][2])) for i in range(90)]
    near90 = nearest_all(cert, seed90)
    out["seed"] = {
        "sigma": 1,
        "dropped": [[seed[k][0], seed[k][1], seed[k][2], seed[k][3]] for k in dropped],
        "dropped_wall_crossing": [min(min(q[0] for q in corners(*seed[k][:3])), min(q[1] for q in corners(*seed[k][:3]))) for k in dropped],
        "side_10_windows_holding_exactly_the_90": [min(ws), max(ws)] if ws else None,
        "squares": len(seed90),
        "by_copy": {str(m): sum(1 for s in seed90 if s[3] == m) for m in (-1, 0, 1)},
        "tilted": sum(1 for s in seed90 if abs(s[2]) > 0.5),
        "overlapping_pairs": len(ov),
        "deepest_overlap": ov[0][0] if ov else 0.0,
        "squares_crossing_a_wall": len(wall),
        "deepest_wall_crossing": min(wall)[0] if wall else 0.0,
        "nearest_centres_one_to_one": len(set(near90)) == 90 and perm == near90,
        "assignment_moves_beyond": {t: sum(1 for x in moves if x > float(t)) for t in ("1e-3", "1e-2", "1e-1")},
        "largest_move": max(moves),
        "largest_move_square": moves.index(max(moves)) + 1,
        "largest_turn_deg": max(turns),
        "turned_beyond_1_deg": sum(1 for x in turns if x > 1),
        "copy_B_squares_of_the_certificate": [i + 1 for i in range(90) if seed90[perm[i]][3] != 0],
    }
    with open(argv[4], "w") as fh:
        fh.write(f"90 {F(*rdg['side'])}\n")
        for x, y, a, _m, _j in seed90:
            fh.write(f"{F(x)} {F(y)} {F(math.tan(math.radians(a) / 2))}\n")
    with open(argv[3], "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    for k, v in out.items():
        if k not in ("seed", "tilted_translation_peaks"):
            print(k, v)
    print("peaks", {k: v[:1] for k, v in hist.items()})
    for k, v in out["seed"].items():
        print("seed", k, v)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
