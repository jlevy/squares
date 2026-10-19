"""A243 -- the SLOT-SET CENSUS at a new n (A53's Young definition, n-general), on the window [s_lo, s_hi].

A class = a 4-tuple of corner-anchored Young diagrams (corner c, cell (i, j): all (i', j') <= (i, j) present), the
slot square of cell (c, i, j) being the axis-aligned unit square at distances i, j from c's two walls, with the
union pairwise INTERIOR-disjoint, reduced by D4.  Offsets run while i + 1 <= s (s < 5 here: i <= 3).
Window stability [T]: two slot squares of opposite corners along one axis are disjoint iff i + i' + 2 <= m; the
census is computed at s_lo AND at s_hi and asserted equal, and no integer lies in [s_lo, s_hi] (asserted), so the
class table is the same at every side m of the window.  Lemma K1 (kills climb containment): a packing containing
the pins of T contains the pins of every S <= T, so a DEAD S closes every T >= S (up to D4).
Usage: python census243.py N  -> results/census243_n<N>.json (every class with k <= n: names, slots, labels)."""
import itertools
import json
import math
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
A243 = os.path.abspath(os.path.join(HERE, ".."))
HALF = Fr(1, 2)

# the windows (the Squares Project register, packing/frontier/RESULTS.md, read 2026-10-07)
#   n = 17: s_lo = 116511/25000 (T-043, R068; T-093 raises it by 2.75e-6), s_hi = an OUTWARD rational ceiling of
#           T-065's 4.6755300936045509... (Bidwell / Kleddamag's exact witness): 4675531/10^6.
#   n = 19: s_lo = 193/40 = 4.825 (T-103, superseding T-020's 24/5 and T-100), s_hi = outward ceiling of the best known
#           3 + 4 sqrt2 / 3 = 4.8856180831...: 4885619/10^6 (not a register row; register text, upper-bound runway).
#   n = 11: the lab's window [191/50, 969271/250000] (the unit test only).
WINDOWS = {17: (Fr(116511, 25000), Fr(4675531, 10 ** 6), "T-043 / T-065"),
           19: (Fr(193, 40), Fr(4885619, 10 ** 6), "T-103 / best known 3 + 4sqrt2/3"),
           11: (Fr(191, 50), Fr(969271, 250000), "lab window")}
K_REC = {17: 8, 19: 11, 11: 5}
CORNERS = ("BL", "BR", "TR", "TL")


def max_off(s):
    return int(math.floor(s)) - 1


def parts(nmax):
    return [l for l in itertools.product(range(nmax + 1), repeat=nmax) if all(l[a] >= l[a + 1] for a in range(nmax - 1))]


def cells(lam):
    return [(i, j) for j, lj in enumerate(lam) for i in range(lj)]


def centre(c, i, j, s):
    x = i + HALF if c in ("BL", "TL") else s - i - HALF
    y = j + HALF if c in ("BL", "BR") else s - j - HALF
    return (x, y)


def overlap(p, q):
    return abs(p[0] - q[0]) < 1 and abs(p[1] - q[1]) < 1


D4 = [lambda x, y, s: (x, y), lambda x, y, s: (s - x, y), lambda x, y, s: (x, s - y), lambda x, y, s: (s - x, s - y),
      lambda x, y, s: (y, x), lambda x, y, s: (s - y, x), lambda x, y, s: (y, s - x), lambda x, y, s: (s - y, s - x)]


def canon(pts, s):
    return min(tuple(sorted(f(x, y, s) for x, y in pts)) for f in D4)


def label_of(p, s):
    """position -> its (corner, i, j) label (unique: s is not an integer)."""
    x, y = p
    cx, i = ("L", x - HALF) if (x - HALF).denominator == 1 else ("R", s - HALF - x)
    cy, j = ("B", y - HALF) if (y - HALF).denominator == 1 else ("T", s - HALF - y)
    return "%s%s(%d,%d)" % (cy, cx, int(i), int(j))


def enumerate_classes(s):
    mo = max_off(s)
    P = [l for l in parts(mo + 1)]
    sm = {c: {lam: [centre(c, i, j, s) for (i, j) in cells(lam)] for lam in P} for c in CORNERS}

    def comp(A, B):
        return all(not overlap(p, q) for p in A for q in B)
    out = {}
    for lA in P:
        A = sm["BL"][lA]
        for lB in P:
            B = sm["BR"][lB]
            if not comp(A, B):
                continue
            for lC in P:
                C = sm["TR"][lC]
                if not (comp(A, C) and comp(B, C)):
                    continue
                for lD in P:
                    D = sm["TL"][lD]
                    if comp(A, D) and comp(B, D) and comp(C, D):
                        pts = A + B + C + D
                        out.setdefault(canon(pts, s), (lA, lB, lC, lD))
    return out


def build(n):
    s_lo, s_hi, src = WINDOWS[n]
    assert math.floor(s_lo) == math.floor(s_hi) and s_lo.denominator != 1, "an integer side inside the window"
    hi = enumerate_classes(s_hi)
    lo = enumerate_classes(s_lo)
    sig = lambda T, s: sorted(tuple(sorted(sum(([CORNERS[c] + str(ij) for ij in cells(l)] for c, l in enumerate(tp)), []))) for tp in T.values())
    assert sig(hi, s_hi) == sig(lo, s_lo), "census not window-stable"
    kmin = K_REC[n]
    rows = []
    for cn, tp in sorted(hi.items(), key=lambda kv: (-len(kv[0]), kv[0])):
        if len(cn) > n:
            continue
        rows.append(dict(k=len(cn), shapes=[list(l) for l in tp], slots=[[str(x), str(y)] for x, y in cn],
                         labels=sorted(label_of(p, s_hi) for p in cn)))
    byk = {}
    for r in rows:
        byk[r["k"]] = byk.get(r["k"], 0) + 1
        r["name"] = "n%d_k%02d_%04d" % (n, r["k"], byk[r["k"]] - 1)
    all_by_k = {}
    for cn in hi:
        all_by_k[len(cn)] = all_by_k.get(len(cn), 0) + 1
    return dict(n=n, s_lo=str(s_lo), s_hi=str(s_hi), source=src, max_off=max_off(s_hi), k_rec=kmin,
                census_d4_by_k={str(k): v for k, v in sorted(all_by_k.items())}, n_rows=len(rows), rows=rows)


def path(n):
    return os.path.join(A243, "results", "census243_n%d.json" % n)


def load(n):
    return json.load(open(path(n), encoding="utf-8"))


if __name__ == "__main__":
    n = int(sys.argv[1])
    d = build(n)
    json.dump(d, open(path(n), "w", encoding="utf-8"), indent=0)
    print("n=%d window [%s, %s] max_off %d; D4 classes by k %s; k_rec %d; rows %d" % (
        n, d["s_lo"], d["s_hi"], d["max_off"], d["census_d4_by_k"], d["k_rec"], d["n_rows"]))
