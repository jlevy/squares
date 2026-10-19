"""A213b -- the RECTANGLE-OBSTACLE CLIP (A171 `multibox._clip_rect_obstacle`, built on A131 pin-clip) in INTEGER
space.  Same idea as A213's polycore_int: every decision the clip makes is the SIGN of a rational expression, and the
sign of p/q with q > 0 is the sign of the integer p.  So the exact dead test `multibox.dead_poly` is re-issued as
integer sign tests over one common denominator per (obstacle, tilt bin), Fractions appear only at the boundary (the
rect the clip returns is built from the library's own rational candidates), and the float twin `_dead_poly_f` -- which
only STEERS the bisection, never decides -- is re-issued operation for operation on precompiled Python floats.
READ-ONLY use of multibox (A171) and pinclip (A131): nothing here edits them, `PIN._bisect_boundary` is reused
verbatim, so the control flow, the `stats` counters and the trace are the library's.

REPRESENTATION (all integers; W, VD, G, RD, CW > 0).
  * the obstacle K:  its vertices over one common denominator VD -- (VX_i, VY_i)/VD;  an edge normal (nx, ny) is a
    difference of vertices, so (NX, NY) = (nx VD, ny VD) are integers, and its support interval [lo, hi] is a sum of
    products of vertices, so (LO, HI) = (lo VD^2, hi VD^2) are integers.
  * the per-edge radius lower bound r_k = RN/RD comes from the library itself (`Bin.radii`, cached under obs.uid).
  * the tilt bin: cos, sin at the two endpoints as (C0, S0)/G0 and (C1, S1)/G1.
  * a query centre c = (CX, CY)/CW.

THE TWO FAMILIES (`multibox.dead_poly`), multiplied through by positive integers.
  A (K's edge normals).  p = n.c = PN/(VD CW) with PN = NX CX + NY CY.  The library's `p - r < hi and p + r > lo`,
    times VD^2 CW RD > 0, is      EL_k CW  <  PN EA_k  <  EU_k CW,
    EA = VD RD,  EU = HI RD + RN VD^2,  EL = LO RD - RN VD^2   (the triple may be divided by its gcd: both sides of
    each inequality carry EA / EU / EL exactly once).
  B (the square's own axes).  P = p_i.x - c.x = Pn/M, Q = Qn/M with M = VD CW, Pn = VX_i CW - CX VD.  A131's
    `_m_lt_half(P, Q)` is, with X = Pn C + Qn S and Y = Qn C - Pn S at each endpoint,
        if Y0 >= 0 and Y1 <= 0 and (Y0 > 0 or Y1 < 0):   4 (Pn^2 + Qn^2) < M^2        (r^2 < 1/4)
        else  max(X0/(M G0), X1/(M G1)) < 1/2, i.e. compare X0 G1 vs X1 G0 and test 2 X < M G.
    The four (swap, sign) statements the library makes per vertex are the SAME four numbers with signs:
        (0, +1): d = +Y, v = +X;  (0, -1): d = -Y, v = -X;  (1, +1): d = -X, v = +Y;  (1, -1): d = +X, v = -Y
    -- because (P, Q) -> (Q, -P) sends (X, Y) -> (Y, -X) and (P, Q) -> (-P, -Q) sends (X, Y) -> (-X, -Y).  Exactly the
    same identity holds in binary64 (negation is exact and fl(-a-b) = -fl(a+b), fl(x-y) = -fl(y-x)), so the float twin
    reuses the same four numbers and is bit-identical to the library's four `_m_lt_half_f` calls.

BIT BOUND (notes/int_clip.md s.3).  Poly obstacles live on the 1e-9 grid (VD = 10^9 < 2^30), core obstacles on
den*aden*Q; rect coordinates on 1e-9, on 1/(10^9 * 1024) (the bisection candidate) or on the container's w_min grid.
With b = log2 of the largest of VD, CW, G, RD the widest products are PN EA, 4(Pn^2 + Qn^2) vs M^2 and X G' -- all
below 2^(4b + 6).  Measured on the Y0202 run: b <= 118, every integer below 2^480.  Python ints, no overflow, and no
gcd anywhere on the hot path.
"""
import math
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
_A171 = os.path.abspath(os.path.join(HERE, "..", "..", "A171-multibox-invariant", "code"))
if _A171 not in sys.path:
    sys.path.insert(0, _A171)

import multibox as MB                                          # noqa: E402,F401  READ-ONLY (A171; sets the path)
import pinclip as PIN                                          # noqa: E402  READ-ONLY (A131)

CAP = 20000                                    # compiled (obstacle, bin) pairs kept
CWCAP = 96                                     # per-pair cache of the CW-only products
FILTER = os.environ.get("A213_CLIPFILTER") == "1"     # Phase 2 float filter on family A (default OFF)
_PAIRS = {}
STATS = dict(pairs=0, points=0, filt=0, fallback=0)

# (which pair of numbers carries d, sign of d, sign of v) for the library's ((0,1),(0,-1),(1,1),(1,-1))
_COMB = ((0, 1, 1), (0, -1, -1), (1, -1, 1), (1, 1, -1))


def _nd(x):
    if isinstance(x, Fr):
        return x.numerator, x.denominator
    if isinstance(x, int):
        return x, 1
    f = Fr(x)
    return f.numerator, f.denominator


def _lcm(a, b):
    return a // math.gcd(a, b) * b


def hom(x, y):
    """(X, Y, W), W > 0, with (X/W, Y/W) == (x, y) exactly."""
    xn, xd = _nd(x)
    yn, yd = _nd(y)
    if xd == yd:
        return xn, yn, xd
    W = _lcm(xd, yd)
    return xn * (W // xd), yn * (W // yd), W


def _int(q):
    n, d = _nd(q)
    assert d == 1, "pinclip_int: %r is not an integer" % (q,)
    return n


class IPair:
    """one (obstacle, tilt bin) compiled to integers (the exact test) and to floats (the search twin)."""
    __slots__ = ("nE", "nV", "vd", "VX", "VY", "NX", "NY", "EA", "EU", "EL",
                 "C0", "S0", "G0", "C1", "S1", "G1",
                 "fnx", "fny", "flo", "fhi", "fr", "fV", "fc0", "fs0", "fc1", "fs1", "cw", "obs")

    def __init__(self, obs, bn):
        self.obs = obs                                          # keeps the obstacle alive for the key
        vd = 1
        for (x, y) in obs.verts:
            vd = _lcm(_lcm(vd, _nd(x)[1]), _nd(y)[1])
        self.vd = vd
        self.VX = [_int(x * vd) for (x, _y) in obs.verts]
        self.VY = [_int(y * vd) for (_x, y) in obs.verts]
        self.nV = len(obs.verts)
        self.fV = [(float(a), float(b)) for (a, b) in obs.fV]
        vd2 = vd * vd
        R = bn.radii(obs)                                       # the library's own rational radii (cached per uid)
        self.NX, self.NY, self.EA, self.EU, self.EL = [], [], [], [], []
        self.fnx, self.fny, self.flo, self.fhi, self.fr = [], [], [], [], []
        for k, (nx, ny, lo, hi) in enumerate(obs.edges):
            self.NX.append(_int(nx * vd))
            self.NY.append(_int(ny * vd))
            rn, rd = _nd(R[k])
            ea, ern = vd * rd, rn * vd2
            eu, el = _int(hi * vd2) * rd + ern, _int(lo * vd2) * rd - ern
            g = math.gcd(math.gcd(ea, eu), el)
            if g > 1:
                ea, eu, el = ea // g, eu // g, el // g
            self.EA.append(ea)
            self.EU.append(eu)
            self.EL.append(el)
            fnx, fny = float(nx), float(ny)                     # the library's own float twin, hoisted
            u0, v0 = fnx * bn.fc0 + fny * bn.fs0, -fnx * bn.fs0 + fny * bn.fc0
            u1, v1 = fnx * bn.fc1 + fny * bn.fs1, -fnx * bn.fs1 + fny * bn.fc1
            self.fnx.append(fnx)
            self.fny.append(fny)
            self.flo.append(float(lo))
            self.fhi.append(float(hi))
            self.fr.append(min(abs(u0) + abs(v0), abs(u1) + abs(v1)) / 2.0)
        self.nE = len(self.EA)
        (c0, g0a), (s0, g0b) = _nd(bn.c0), _nd(bn.s0)
        G0 = _lcm(g0a, g0b)
        self.C0, self.S0, self.G0 = c0 * (G0 // g0a), s0 * (G0 // g0b), G0
        (c1, g1a), (s1, g1b) = _nd(bn.c1), _nd(bn.s1)
        G1 = _lcm(g1a, g1b)
        self.C1, self.S1, self.G1 = c1 * (G1 // g1a), s1 * (G1 // g1b), G1
        self.fc0, self.fs0, self.fc1, self.fs1 = bn.fc0, bn.fs0, bn.fc1, bn.fs1
        self.cw = {}

    def at(self, CW):
        """the products that depend only on the query denominator CW (the rect corners share one)."""
        e = self.cw.get(CW)
        if e is None:
            if len(self.cw) >= CWCAP:
                self.cw.clear()
            M = self.vd * CW
            e = self.cw[CW] = ([u * CW for u in self.EU], [u * CW for u in self.EL],
                               [v * CW for v in self.VX], [v * CW for v in self.VY],
                               M * M, M * self.G0, M * self.G1)
        return e


def pair(obs, bn):
    key = (obs.uid, bn.t0, bn.t1)
    p = _PAIRS.get(key)
    if p is None:
        if len(_PAIRS) >= CAP:
            _PAIRS.clear()
        p = _PAIRS[key] = IPair(obs, bn)
        STATS["pairs"] += 1
    return p


# ------------------------------------------------------------------------ family A (K's edge normals)
_U8 = 8.0 * 2.0 ** -53


def _famA(CX, CY, ic, EUc, ELc):
    """EXACT: for every edge, EL CW < PN EA < EU CW."""
    NX, NY, EA = ic.NX, ic.NY, ic.EA
    for k in range(ic.nE):
        pa = (NX[k] * CX + NY[k] * CY) * EA[k]
        if pa >= EUc[k] or pa <= ELc[k]:
            return False
    return True


def _famA_ff(CX, CY, ic, EUc, ELc, fE):
    """Phase 2: the same test in binary64 with a rigorous forward bound; the exact integers only where the
    filter cannot decide.  `fE` = (fNX, fNY, fEA, fEU, fEL) as floats, fCX / fCY the query."""
    fNX, fNY, fEA, fEU, fEL, fCX, fCY = fE
    NX, NY, EA = ic.NX, ic.NY, ic.EA
    for k in range(ic.nE):
        a, b = fNX[k] * fCX, fNY[k] * fCY
        t = (a + b) * fEA[k]
        s = (abs(a) + abs(b)) * abs(fEA[k])
        hi, lo = fEU[k], fEL[k]
        dh, dl = t - hi, t - lo
        if dh < -(_U8 * (s + abs(hi))) and dl > _U8 * (s + abs(lo)) and t == t and s != float("inf"):
            continue                                            # decided in float: strictly inside
        STATS["fallback"] += 1
        pa = (NX[k] * CX + NY[k] * CY) * EA[k]
        if pa >= EUc[k] or pa <= ELc[k]:
            return False
    STATS["filt"] += 1
    return True


# ------------------------------------------------------------------------ the exact dead test
def dead_int(CX, CY, CW, ic):
    """EXACT integer twin of `multibox.dead_poly((CX/CW, CY/CW), obs, bn)`."""
    EUc, ELc, VXc, VYc, Msq, MG0, MG1 = ic.at(CW)
    if FILTER:
        if not _famA_ff(CX, CY, ic, EUc, ELc, _ffloats(ic, CW, CX, CY)):
            return False
    elif not _famA(CX, CY, ic, EUc, ELc):
        return False
    vd, C0, S0, C1, S1 = ic.vd, ic.C0, ic.S0, ic.C1, ic.S1
    G0, G1, nV = ic.G0, ic.G1, ic.nV
    cxv, cyv = CX * vd, CY * vd
    cache = [None] * nV
    for (wch, sd, sv) in _COMB:
        ok = False
        for i in range(nV):
            e = cache[i]
            if e is None:
                pn, qn = VXc[i] - cxv, VYc[i] - cyv
                e = cache[i] = (qn * C0 - pn * S0, qn * C1 - pn * S1,
                                pn * C0 + qn * S0, pn * C1 + qn * S1, 4 * (pn * pn + qn * qn))
            if wch:
                d0, d1, v0, v1 = e[2], e[3], e[0], e[1]
            else:
                d0, d1, v0, v1 = e[0], e[1], e[2], e[3]
            if sd < 0:
                d0, d1 = -d0, -d1
            if d0 >= 0 and d1 <= 0 and (d0 > 0 or d1 < 0):
                if e[4] < Msq:                                  # 4 (Pn^2 + Qn^2) < M^2  <=>  r^2 < 1/4
                    ok = True
                    break
                continue
            if sv < 0:
                v0, v1 = -v0, -v1
            if v0 * G1 > v1 * G0:
                if 2 * v0 < MG0:
                    ok = True
                    break
            elif 2 * v1 < MG1:
                ok = True
                break
        if not ok:
            return False
    return True


def _ffloats(ic, CW, CX, CY):
    e = ic.cw.get(("f", CW))
    if e is None:
        EUc, ELc = ic.at(CW)[0], ic.at(CW)[1]
        e = ic.cw[("f", CW)] = ([float(v) for v in ic.NX], [float(v) for v in ic.NY],
                                [float(v) for v in ic.EA], [float(v) for v in EUc], [float(v) for v in ELc])
    return e + (float(CX), float(CY))


# ------------------------------------------------------------------------ the float twin (search only)
def dead_f(fx, fy, ic):
    """bit-identical re-issue of `multibox._dead_poly_f` on precompiled floats (same operations, same order)."""
    fnx, fny, flo, fhi, fr = ic.fnx, ic.fny, ic.flo, ic.fhi, ic.fr
    for k in range(ic.nE):
        p = fnx[k] * fx + fny[k] * fy
        r = fr[k]
        if not (p - r < fhi[k] and p + r > flo[k]):
            return False
    c0, s0, c1, s1, fV = ic.fc0, ic.fs0, ic.fc1, ic.fs1, ic.fV
    nV = len(fV)
    cache = [None] * nV
    for (wch, sd, sv) in _COMB:
        ok = False
        for i in range(nV):
            e = cache[i]
            if e is None:
                px, py = fV[i]
                P, Q = px - fx, py - fy
                e = cache[i] = (Q * c0 - P * s0, Q * c1 - P * s1,
                                P * c0 + Q * s0, P * c1 + Q * s1, P * P + Q * Q)
            if wch:
                d0, d1, v0, v1 = e[2], e[3], e[0], e[1]
            else:
                d0, d1, v0, v1 = e[0], e[1], e[2], e[3]
            if sd < 0:
                d0, d1 = -d0, -d1
            if d0 >= 0.0 and d1 <= 0.0 and (d0 > 0.0 or d1 < 0.0):
                if e[4] < 0.25:
                    ok = True
                    break
                continue
            if sv < 0:
                v0, v1 = -v0, -v1
            if (v0 if v0 > v1 else v1) < 0.5:
                ok = True
                break
        if not ok:
            return False
    return True


# ------------------------------------------------------------------------ the clip (drop-in)
def clip_rect_obstacle(rect, obs, bn, stats, trace=None, tag=""):
    """drop-in for `multibox._clip_rect_obstacle`: the SAME control flow, the same `PIN._bisect_boundary`, the same
    `stats` increments and the same trace -- only the two predicates are re-issued (exact integers / hoisted floats).

    `dq` also memoises its ANSWER within the call (the library asks about the same corner up to four times); the
    counter is still incremented on every ask, so `stats` is bit-identical to the library's."""
    ic = pair(obs, bn)
    x0, x1, y0, y1 = rect
    res = {}

    def dq(px, py):
        stats["exact_calls"] += 1
        k = (px, py)
        v = res.get(k)
        if v is None:
            X, Y, W = hom(px, py)
            v = res[k] = dead_int(X, Y, W, ic)
        return v

    def rec(side, frm, to):
        if trace is not None and to != frm:
            trace.append(dict(op="slab", obs=tag, side=side,
                              **{"from": str(frm)}, to=str(to)))

    if dq(x0, y0) and dq(x1, y0) and dq(x0, y1) and dq(x1, y1):
        if trace is not None:
            trace.append(dict(op="empty", obs=tag, rect=[str(v) for v in rect]))
        return None
    fx0, fx1, fy0, fy1 = float(x0), float(x1), float(y0), float(y1)
    if dq(x0, y0) and dq(x0, y1):
        nx = PIN._bisect_boundary(True, x0, x1,
                                  lambda v: dead_f(v, fy0, ic) and dead_f(v, fy1, ic),
                                  lambda v: dq(v, y0) and dq(v, y1), stats)
        rec("x0", x0, nx)
        x0 = nx
        fx0 = float(x0)
    if dq(x1, y0) and dq(x1, y1):
        neg = PIN._bisect_boundary(True, -x1, -x0,
                                   lambda v: dead_f(-v, fy0, ic) and dead_f(-v, fy1, ic),
                                   lambda v: dq(-v, y0) and dq(-v, y1), stats)
        rec("x1", x1, -neg)
        x1 = -neg
        fx1 = float(x1)
    if x1 <= x0:
        if trace is not None:
            trace.append(dict(op="collapse", obs=tag, axis="x"))
        return None
    if dq(x0, y0) and dq(x1, y0):
        ny = PIN._bisect_boundary(True, y0, y1,
                                  lambda v: dead_f(fx0, v, ic) and dead_f(fx1, v, ic),
                                  lambda v: dq(x0, v) and dq(x1, v), stats)
        rec("y0", y0, ny)
        y0 = ny
    if dq(x0, y1) and dq(x1, y1):
        neg = PIN._bisect_boundary(True, -y1, -y0,
                                   lambda v: dead_f(fx0, -v, ic) and dead_f(fx1, -v, ic),
                                   lambda v: dq(x0, -v) and dq(x1, -v), stats)
        rec("y1", y1, -neg)
        y1 = -neg
    if x1 <= x0 or y1 <= y0:
        if trace is not None:
            trace.append(dict(op="collapse", obs=tag, axis="y"))
        return None
    return (x0, x1, y0, y1)


def dead_poly(cx, cy, obs, bn):
    """drop-in for `multibox.dead_poly` (the differential tests and any other caller)."""
    X, Y, W = hom(cx, cy)
    return dead_int(X, Y, W, pair(obs, bn))


def dead_poly_f(cx, cy, obs, bn):
    """drop-in for `multibox._dead_poly_f`."""
    return dead_f(cx, cy, pair(obs, bn))


def rep():
    return dict(STATS, cached=len(_PAIRS), filter=FILTER)
