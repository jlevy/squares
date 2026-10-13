"""K3 independent exact check of capture rows of one #557 class certificate ("fixed" symmetry).

Written for lane K3 from the definitions in the edition's CLASS_ROW_LEMMA.md (premise
CHARGE_SEMANTICS), PROOF.md section 3 and the format note RESTRICTED_CHECKER.md sections 1.4-1.7
and 3; it imports nothing from the producers' checkers and was written without reading their
sweep code (exact_general.py, integer_sweep.py, verify_classes_wb.js).

For one row [a, b, t, B] it decides, exactly, for every cell of its own arrangement that meets the
closed centre envelope:

    charge(cell) >= Gamma * R(cell),

where charge = sum of feature weights firing on the closed core of side B and direction 2 atan(t)
centred in the open cell, evaluated by its own Moebius expansion of each Boolean feature into
"all sites of S captured" atoms; and R(cell) is the class level of PROOF.md P030: the largest
threshold of a high class (t > 1) one of whose slots meets (closed cell) x [a, b], else the least
threshold of a low class (t < 1) one of whose slots contains (closed cell) x [a, b], else 1.

Per row it prints the least charge per level and the cell count per level, for comparison with
the stored rows. Whole-certificate checks: budget recomputed from capacities, strict budget
inequality, gapless row chain on [0, 1], and the per-row geometry (strict core, envelope).

Usage: python k3_capture_row.py CERT.json CLASSES.json [--control-gamma=N] ROW [ROW ...]
(--control-gamma replaces Gamma, for a negative control.)
"""

import bisect
import json
import sys
import time
from fractions import Fraction as Q
from math import lcm


def need(cond, msg):
    if not cond:
        raise SystemExit("REFUSED: " + msg)


def rat(x):
    if isinstance(x, int):
        return Q(x)
    need(isinstance(x, str), "rational must be int or string")
    return Q(x)


def no_float(_):
    raise SystemExit("REFUSED: float token")


# ---------------------------------------------------------------- features and budget
def fires(feature, subset_mask):
    """Boolean value of a feature on the set of its positions given by subset_mask."""
    n = len(feature["sites"])
    if "winning_masks" in feature:
        return any((m & subset_mask) == m for m in feature["winning_masks"])
    coeff = feature.get("coefficients", [1] * n)
    total = sum(coeff[j] for j in range(n) if subset_mask >> j & 1)
    return total >= feature["threshold"]


def capacity(feature):
    n = len(feature["sites"])
    if "winning_masks" in feature:
        masks = feature["winning_masks"]
        need(all(m & mm for m in masks for mm in masks), "masks must pairwise intersect")
        return 1
    coeff = feature.get("coefficients", [1] * n)
    return sum(coeff) // feature["threshold"]


def moebius(feature):
    """Coefficients c_S with f(T) = sum over S subset of T of c_S (S as bit masks), nonzero only."""
    n = len(feature["sites"])
    f = [1 if fires(feature, m) else 0 for m in range(1 << n)]
    need(f[0] == 0, "a feature fires on the empty set")
    # monotone check (the lemma needs original features monotone)
    for m in range(1 << n):
        for j in range(n):
            if not m >> j & 1:
                need(f[m] <= f[m | 1 << j], "feature not monotone")
    c = f[:]
    for j in range(n):  # subset-sum Moebius inversion
        bit = 1 << j
        for m in range(1 << n):
            if m & bit:
                c[m] -= c[m ^ bit]
    return {m: v for m, v in enumerate(c) if v}


# ---------------------------------------------------------------- trig of tan-half values
def cs(x):
    return (1 - x * x) / (1 + x * x), 2 * x / (1 + x * x)


def lifts(lo, hi):
    return [(lo, hi), ((1 + lo) / (1 - lo), (1 + hi) / (1 - hi)), ((lo - 1) / (lo + 1), (hi - 1) / (hi + 1))]


def gate_meets(gate, a, b):
    return any(l <= b and a <= h for l, h in lifts(*gate))


def gate_contains(gate, a, b):
    return any(l <= a and b <= h for l, h in lifts(*gate))


# ---------------------------------------------------------------- convex polygons in sweep space
def vrange_on_slab(poly, u0, u1):
    """Exact [vmin, vmax] of the closed convex polygon over the closed slab u0 <= u <= u1, or None."""
    pts = []
    n = len(poly)
    for i in range(n):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % n]
        if u0 <= x0 <= u1:
            pts.append(y0)
        for uu in (u0, u1):
            if (x0 - uu) * (x1 - uu) < 0:
                pts.append(y0 + (y1 - y0) * (uu - x0) / (x1 - x0))
    if not pts:
        return None
    return min(pts), max(pts)


def vrange_at(poly, uu):
    return vrange_on_slab(poly, uu, uu)


def inner_vrange(poly, u0, u1):
    """[lo, hi] with (closed slab) x [lo, hi] inside the polygon, or None (convexity)."""
    r0, r1 = vrange_at(poly, u0), vrange_at(poly, u1)
    if r0 is None or r1 is None:
        return None
    lo, hi = max(r0[0], r1[0]), min(r0[1], r1[1])
    return (lo, hi) if lo <= hi else None


# ---------------------------------------------------------------- range-add / range-min tree
class Tree:
    def __init__(self, n):
        self.n = 1
        while self.n < n:
            self.n *= 2
        self.h = self.n.bit_length()
        self.t = [0] * (2 * self.n)
        self.d = [0] * self.n
        big = 1 << 62  # leaves beyond n never queried
        for i in range(n, self.n):
            self.t[self.n + i] = big
        for p in range(self.n - 1, 0, -1):
            self.t[p] = min(self.t[2 * p], self.t[2 * p + 1])

    def _apply(self, p, v):
        self.t[p] += v
        if p < self.n:
            self.d[p] += v

    def _build(self, p):
        t, d = self.t, self.d
        while p > 1:
            p >>= 1
            t[p] = min(t[2 * p], t[2 * p + 1]) + d[p]

    def _push(self, p):
        for s in range(self.h, 0, -1):
            i = p >> s
            if i and self.d[i]:
                self._apply(2 * i, self.d[i])
                self._apply(2 * i + 1, self.d[i])
                self.d[i] = 0

    def add(self, l, r, v):
        l += self.n
        r += self.n
        l0, r0 = l, r
        while l < r:
            if l & 1:
                self._apply(l, v)
                l += 1
            if r & 1:
                r -= 1
                self._apply(r, v)
            l >>= 1
            r >>= 1
        self._build(l0)
        self._build(r0 - 1)

    def min(self, l, r):
        l += self.n
        r += self.n
        self._push(l)
        self._push(r - 1)
        res = 1 << 63
        t = self.t
        while l < r:
            if l & 1:
                res = min(res, t[l])
                l += 1
            if r & 1:
                r -= 1
                res = min(res, t[r])
            l >>= 1
            r >>= 1
        return res


# ---------------------------------------------------------------- one row
def check_row(cert, classes, sites, atoms_by_feature, row_index):
    L, A = rat(cert["L"]), rat(cert["A"])
    D = cert["coordinate_denominator"]
    gamma = cert["minimum_units"]
    a, b, t, B = (rat(x) for x in cert["entries"][row_index])
    ct, st = cs(t)
    # row geometry, from the definitions: core inside the open parent for every direction in [a, b]
    worst = Q(0)
    for u in (a, b):
        cu, su = cs(u)
        dot = ct * cu + st * su  # cos(phi - theta)
        cross = abs(ct * su - st * cu)  # |sin(phi - theta)|
        need(dot > 0 and cross <= dot, "core direction more than pi/4 from the parent")
        worst = max(worst, dot + cross)
    need(B * worst < A, "core not strictly inside the parent")
    r = A * min(sum(cs(u)) for u in (a, b)) / 2
    need(0 < r < L / 2, "envelope")
    H = L / 2 - r
    # integer sweep coordinates: t = p/q, C = q^2 - p^2, S = 2pq; q' = point - (L/2, L/2)
    p, q = t.numerator, t.denominator
    C, S = q * q - p * p, 2 * p * q
    half = B / 2
    scale = lcm(2 * D, half.denominator)
    # U = scale * (C x' + S y'), V = scale * (-S x' + C y'); site x' = (X - L D/2)/D
    LD = L * D
    need(LD.denominator == 1, "L*D integer")
    # A site P is in the closed core centred at q iff |(P-q).(C,S)| <= Rlen*B/2 and
    # |(P-q).(-S,C)| <= Rlen*B/2, since |(C,S)| = Rlen = q^2 + p^2. With U = scale*(C x' + S y'),
    # V = scale*(-S x' + C y') this is |U(P) - U(q)| <= hw and |V(P) - V(q)| <= hw.
    Rlen = q * q + p * p
    need(C * C + S * S == Rlen * Rlen, "pythagorean")
    hw_q = Q(scale) * half * Rlen
    need(hw_q.denominator == 1, "integer half-width")
    hw = int(hw_q)

    def to_uv(x2, y2, den):
        """Point (x2/den, y2/den) in centred plain coordinates -> exact (U, V)."""
        uu = Q(scale * (C * x2 + S * y2), den)
        vv = Q(scale * (-S * x2 + C * y2), den)
        return uu, vv

    su, sv = [], []
    LDi = int(LD)
    for x, y in sites:
        # centred: (x - LD/2)/D = (2x - LD)/(2D)
        uu, vv = to_uv(2 * x - LDi, 2 * y - LDi, 2 * D)
        need(uu.denominator == 1 and vv.denominator == 1, "integer site coordinates")
        su.append(int(uu))
        sv.append(int(vv))
    # envelope square [-H, H]^2 in (U, V)
    env = [to_uv(ex * H.numerator, ey * H.numerator, H.denominator) for ex, ey in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    # atoms: rectangles [max u - hw, min u + hw] x [max v - hw, min v + hw]
    rects = []
    for feat_sites, weight, coeffs in atoms_by_feature:
        for mask, c in coeffs.items():
            idx = [feat_sites[j] for j in range(len(feat_sites)) if mask >> j & 1]
            us = [su[i] for i in idx]
            vs = [sv[i] for i in idx]
            u0, u1 = max(us) - hw, min(us) + hw
            v0, v1 = max(vs) - hw, min(vs) + hw
            if u0 <= u1 and v0 <= v1:
                rects.append((u0, u1, v0, v1, weight * c))
    # arrangement coordinates: rectangle edges and envelope vertices
    env_u = [e[0] for e in env]
    env_v = [e[1] for e in env]
    umin, umax = min(env_u), max(env_u)
    vmin, vmax = min(env_v), max(env_v)
    ucoords = sorted(set([x for r_ in rects for x in (r_[0], r_[1])] + env_u))
    vcoords = sorted(set([y for r_ in rects for y in (r_[2], r_[3])] + env_v))
    vindex = {v: i for i, v in enumerate(vcoords)}
    nv = len(vcoords) - 1  # elementary open intervals (v_j, v_{j+1}), j = 0..nv-1
    tree = Tree(nv)
    # events: rectangle [u0, u1] covers open slabs (u_k, u_{k+1}) with u0 <= u_k and u_{k+1} <= u1
    add_at, rem_at = {}, {}
    for u0, u1, v0, v1, w in rects:
        if u0 == u1 or v0 == v1:
            continue  # degenerate: covers no open cell
        add_at.setdefault(u0, []).append((vindex[v0], vindex[v1], w))
        rem_at.setdefault(u1, []).append((vindex[v0], vindex[v1], -w))
    # classes in sweep space
    ox, oy = (rat(c) for c in classes["frame"]["center"])
    regs = []  # (level index, threshold, kind, polygon in (U, V))
    for ci, cl in enumerate(classes["classes"]):
        thr = rat(cl["threshold"])
        kind = (thr > 1) - (thr < 1)
        if kind == 0:
            continue
        for slot in cl["slots"]:
            gate = tuple(rat(g) for g in slot["angle_tan_half"])
            active = gate_meets(gate, a, b) if kind > 0 else gate_contains(gate, a, b)
            if not active:
                continue
            poly = []
            for ex, ey in slot["centre"]["polygon"]:
                # frame e -> certificate point X = (L/2, L/2) + A (e - centre); centred x' = A (e - centre)
                xx, yy = A * (rat(ex) - ox), A * (rat(ey) - oy)
                poly.append((scale * (C * xx + S * yy), scale * (-S * xx + C * yy)))
            regs.append((ci, thr, kind, poly))
    nlev = len(classes["classes"]) + 1  # last level = default (threshold 1)
    thresholds = [rat(cl["threshold"]) for cl in classes["classes"]] + [Q(1)]
    lowest = [None] * nlev
    cells = [0] * nlev
    for k in range(len(ucoords) - 1):
        uk = ucoords[k]
        for item in rem_at.get(uk, ()):
            tree.add(item[0], item[1], item[2])
        for item in add_at.get(uk, ()):
            tree.add(item[0], item[1], item[2])
        uk1 = ucoords[k + 1]
        if uk1 <= umin or uk >= umax:
            continue
        er = vrange_on_slab(env, uk, uk1)
        if er is None:
            continue
        # elementary intervals j with v_{j+1} > er_lo and v_j < er_hi (open cell meets interior)

        j0 = bisect.bisect_right(vcoords, er[0]) - 1
        j1 = bisect.bisect_left(vcoords, er[1])
        j0 = max(j0, 0)
        j1 = min(j1, nv)
        if j0 >= j1:
            continue
        # level of each cell: high meets, low contains
        pieces = []  # (j_lo, j_hi, level)
        highs, lows = [], []
        for ci, thr, kind, poly in regs:
            if kind > 0:
                vr = vrange_on_slab(poly, uk, uk1)
                if vr is None:
                    continue
                # closed cell [v_j, v_{j+1}] meets [vr0, vr1]: v_{j+1} >= vr0 and v_j <= vr1
                lo = bisect.bisect_left(vcoords, vr[0]) - 1
                hi = bisect.bisect_right(vcoords, vr[1])
                lo, hi = max(lo, j0), min(hi, j1)
                if lo < hi:
                    highs.append((lo, hi, ci, thr))
            else:
                ir = inner_vrange(poly, uk, uk1)
                if ir is None:
                    continue
                # closed cell inside: v_j >= ir0 and v_{j+1} <= ir1
                lo = bisect.bisect_left(vcoords, ir[0])
                hi = bisect.bisect_right(vcoords, ir[1]) - 1
                lo, hi = max(lo, j0), min(hi, j1)
                if lo < hi:
                    lows.append((lo, hi, ci, thr))
        if not highs and not lows:
            pieces = [(j0, j1, nlev - 1)]
        else:
            cuts = sorted(set([j0, j1] + [x for h in highs + lows for x in (h[0], h[1])]))
            for x0, x1 in zip(cuts, cuts[1:]):
                hs = [(thr, ci) for lo, hi, ci, thr in highs if lo <= x0 and x1 <= hi]
                ls = [(thr, ci) for lo, hi, ci, thr in lows if lo <= x0 and x1 <= hi]
                if hs:
                    lev = max(hs, key=lambda z: (z[0], -z[1]))[1]
                elif ls:
                    lev = min(ls)[1]
                else:
                    lev = nlev - 1
                pieces.append((x0, x1, lev))
        for x0, x1, lev in pieces:
            m = tree.min(x0, x1)
            cells[lev] += x1 - x0
            if lowest[lev] is None or m < lowest[lev]:
                lowest[lev] = m
    passed = all(
        lowest[i] is None or lowest[i] * thresholds[i].denominator >= thresholds[i].numerator * gamma
        for i in range(nlev)
    )
    names = [cl["name"] for cl in classes["classes"]] + ["default"]
    return {
        "row": row_index,
        "passed": passed,
        "levels": {names[i]: {"cells": cells[i], "minimum_units": lowest[i], "threshold": str(thresholds[i])} for i in range(nlev)},
        "rectangles": len(rects),
        "slabs": len(ucoords) - 1,
        "v_intervals": nv,
    }


def main():
    t0 = time.process_time()
    cert = json.loads(open(sys.argv[1], encoding="utf-8").read(), parse_float=no_float)
    classes = json.loads(open(sys.argv[2], encoding="utf-8").read(), parse_float=no_float)
    args = sys.argv[3:]
    control = None
    if args and args[0].startswith("--control-gamma="):
        # negative control: replace Gamma (minimum_units) before any check; budget is unchanged
        control = int(args.pop(0).split("=", 1)[1])
        cert["minimum_units"] = control
    rows = [int(x) for x in args]
    need(classes["symmetry"] == "fixed", "this checker handles symmetry 'fixed' only")
    need("sites" in cert and "features" in cert, "fixed-image certificate expected")
    D = cert["coordinate_denominator"]
    L = rat(cert["L"])
    LD = L * D
    sites = [tuple(s) for s in cert["sites"]]
    need(all(isinstance(x, int) and 0 <= x <= LD for s in sites for x in s), "site range")
    need(len(set(sites)) == len(sites), "duplicate site")
    budget = 0
    atoms_by_feature = []
    for f in cert["features"]:
        w = f["weight"]
        need(isinstance(w, int) and w >= 0, "weight")
        fs = f["sites"]
        need(1 <= len(fs) <= 20 and len(set(fs)) == len(fs), "feature sites")
        if "coefficients" in f:
            co = f["coefficients"]
            need(len(co) == len(fs) and all(isinstance(x, int) and x > 0 for x in co), "coefficients")
        if "winning_masks" not in f:
            need(1 <= f["threshold"] <= sum(f.get("coefficients", [1] * len(fs))), "threshold")
        budget += w * capacity(f)
        atoms_by_feature.append((fs, w, moebius(f)))
    need(budget == cert["budget_units"], "budget differs from the recomputed capacity sum")
    beta = rat(classes["bound"])
    gamma = cert["minimum_units"]
    need(budget * beta.denominator < beta.numerator * gamma, "strict budget inequality fails")
    # gapless chain on [0, 1]
    prev = Q(0)
    for e in cert["entries"]:
        a, b = rat(e[0]), rat(e[1])
        need(a == prev and a < b <= 1, "row chain")
        prev = b
    need(prev == 1, "chain must end at 1")
    A = rat(cert["A"])
    need(rat(cert["normalized_target"]) == L / A, "normalized target")
    out = {
        "certificate_rows": len(cert["entries"]),
        "budget_units": budget,
        "minimum_units": gamma,
        "bound": str(beta),
        "surplus_units": str(beta * gamma - budget),
        "side_C": str(L / A),
        "rows": [],
    }
    for r_ in rows:
        t1 = time.process_time()
        res = check_row(cert, classes, sites, atoms_by_feature, r_)
        res["cpu_seconds"] = round(time.process_time() - t1, 1)
        out["rows"].append(res)
        print(json.dumps(res), flush=True)
    out["cpu_seconds_total"] = round(time.process_time() - t0, 1)
    out["result"] = "ALL ROWS PASS" if all(r_["passed"] for r_ in out["rows"]) else "SOME ROW FAILS"
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}))


if __name__ == "__main__":
    main()
