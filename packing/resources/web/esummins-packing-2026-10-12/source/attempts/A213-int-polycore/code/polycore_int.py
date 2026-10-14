"""A213 -- the K' build of A171/A132 in INTEGER space (PI: "convert everything to integer space, do the high cost
compute, go back to rational when the results land").  Bit-exact: every decision the library makes is the SIGN of a
rational expression; here each such sign is the sign of an integer (the same expression multiplied through by a
POSITIVE common denominator), and Fractions are rebuilt only at the boundary -- the certified vertices, the axis core
-- so the values handed back are the library's, bit for bit.  READ-ONLY use of multibox / polycore / caselp.

Representation.  A rational point is a homogeneous integer triple (X, Y, W), W > 0, meaning (X/W, Y/W); a line is
(a, b, c) meaning a x + b y + c = 0; join(p, q) = p x q, meet(l, m) = l x m (cross products), gcd-normalised.  A piece
box is compiled ONCE (`IBox`): its four corners over one common denominator CW (the corners are floats, so CW is a
power of two <= 2^53), the tilt interval [T0, T1]/E (E = 2^24, caselp.TDEN).  For a vertex (X, Y, W) against a corner:
u = (X CW - CX W)/(W CW) and the two quadratics of polycore.vertex_ok become, over the positive S = 2 W CW,
    P1: (S/2 + 2U) t^2 - 4V t + (S/2 - 2U),   P2: (S/2 - 2U) t^2 + 4V t + (S/2 + 2U)      (S/2 = W CW),
and `A t^2 + B t + C >= 0 on [t0, t1]` is decided EXACTLY as polycore._quad_nonneg does -- the two endpoint values
(times E^2), the interior test t0 2A <= -B <= t1 2A (times E) and the discriminant 4AC - B^2 -- all integers.
Bit bound (notes/int_polycore.md): W <= 2^30 (VDEN), CW <= 2^53, |U|, |V| < 2^87, T < 2^25, E = 2^24: the endpoint
value < 2^142, the interior test < 2^116, the discriminant < 2^183.  Python ints; no gcd anywhere on this path.
"""
import math
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
_A171 = os.path.abspath(os.path.join(HERE, "..", "..", "A171-multibox-invariant", "code"))
if _A171 not in sys.path:
    sys.path.insert(0, _A171)

import multibox as MB                                          # noqa: E402  READ-ONLY (A171; sets the whole path)
import polycore as PC                                          # noqa: E402  READ-ONLY (A132)
from caselp import t_lo, t_hi                                  # noqa: E402  READ-ONLY


# ------------------------------------------------------------------------------------ rationals -> integers
def _nd(x):
    """exact (numerator, denominator > 0) of a Fraction / int / float."""
    if isinstance(x, Fr):
        return x.numerator, x.denominator
    if isinstance(x, int):
        return x, 1
    f = Fr(x)
    return f.numerator, f.denominator


def hom(x, y):
    """(X, Y, W) of the rational point (x, y)."""
    xn, xd = _nd(x)
    yn, yd = _nd(y)
    if xd == yd:
        return xn, yn, xd
    W = xd * yd // math.gcd(xd, yd)
    return xn * (W // xd), yn * (W // yd), W


def _rhe(num, den):
    """round half to even of num/den (den > 0): Fraction.__round__."""
    q, r = divmod(num, den)
    r2 = 2 * r
    if r2 < den:
        return q
    if r2 > den:
        return q + 1
    return q if q % 2 == 0 else q + 1


class IBox:
    """a piece box compiled to integers: corners over CW, tilt bounds over E, and the products the tests reuse."""
    __slots__ = ("cx", "cy", "cw", "t0", "t1", "e", "t0sq", "t0e", "t1sq", "t1e", "esq", "tt0", "tt1")

    def __init__(self, box, t0, t1):
        cs = [_nd(c) for c in (box.x0, box.x1, box.y0, box.y1)]
        W = 1
        for _n, d in cs:
            W = W * d // math.gcd(W, d)
        X0, X1, Y0, Y1 = (n * (W // d) for n, d in cs)
        self.cx, self.cy, self.cw = (X0, X1, X1, X0), (Y0, Y0, Y1, Y1), W
        a, b = _nd(t0)
        c, d = _nd(t1)
        E = b * d // math.gcd(b, d)
        T0, T1 = a * (E // b), c * (E // d)
        self.t0, self.t1, self.e = T0, T1, E
        self.t0sq, self.t0e, self.t1sq, self.t1e, self.esq = T0 * T0, T0 * E, T1 * T1, T1 * E, E * E
        self.tt0, self.tt1 = 2 * T0, 2 * T1


_IBC = {}


def ibox_of(box, t0, t1):
    key = (box.x0, box.x1, box.y0, box.y1, t0, t1)
    ib = _IBC.get(key)
    if ib is None:
        if len(_IBC) >= 4096:
            _IBC.clear()
        ib = _IBC[key] = IBox(box, t0, t1)
    return ib


# ------------------------------------------------------------------------------------ vertex certification
def _quad_ok(A, B, C, ib):
    """A t^2 + B t + C >= 0 on [t0, t1]  (A, B, C the true coefficients times one positive scale)."""
    if A * ib.t0sq + B * ib.t0e + C * ib.esq < 0:
        return False
    if A * ib.t1sq + B * ib.t1e + C * ib.esq < 0:
        return False
    if A > 0:
        nb = -B * ib.e
        if ib.tt0 * A <= nb <= ib.tt1 * A:
            return 4 * A * C - B * B >= 0
    return True


def vertex_ok_h(X, Y, W, ib):
    """polycore.vertex_ok for the point (X/W, Y/W) against the compiled box, in integers."""
    CW = ib.cw
    S2 = W * CW                                                # the common denominator of u, w; S/2
    XW, YW = X * CW, Y * CW
    cx, cy = ib.cx, ib.cy
    for k in range(4):
        UX = XW - cx[k] * W
        UY = YW - cy[k] * W
        for (U, V) in ((UX, UY), (UY, -UX)):
            P, M, B4 = S2 + 2 * U, S2 - 2 * U, 4 * V
            if not _quad_ok(P, -B4, M, ib):
                return False
            if not _quad_ok(M, B4, P, ib):
                return False
    return True


def vertex_ok(vx, vy, box, t0=None, t1=None):
    """drop-in for polycore.vertex_ok (same signature, same answer)."""
    if t0 is None:
        t0, t1 = t_lo(box.th0), t_hi(box.th1)
    X, Y, W = hom(vx, vy)
    return vertex_ok_h(X, Y, W, ibox_of(box, t0, t1))


def certify_h(hv, ibs):
    """[i] of the homogeneous vertices NOT certified against every compiled box (multibox.certify_verts)."""
    bad = []
    for i, (X, Y, W) in enumerate(hv):
        for ib in ibs:
            if not vertex_ok_h(X, Y, W, ib):
                bad.append(i)
                break
    return bad


def certify_verts(verts, boxes):
    """drop-in for multibox.certify_verts."""
    ibs = [ibox_of(pb, pt0, pt1) for (pb, pt0, pt1) in boxes]
    return certify_h([hom(x, y) for (x, y) in verts], ibs)


# ------------------------------------------------------------------------------------ homogeneous polygons
def _norm(X, Y, W):
    if W < 0:
        X, Y, W = -X, -Y, -W
    g = math.gcd(X, Y, W)
    return (X // g, Y // g, W // g) if g > 1 else (X, Y, W)


def _meet_join(p, q, L):
    """the point where the line through p, q meets the line L = (a, b, c)."""
    a, b, c = p[1] * q[2] - p[2] * q[1], p[2] * q[0] - p[0] * q[2], p[0] * q[1] - p[1] * q[0]
    return _norm(b * L[2] - c * L[1], c * L[0] - a * L[2], a * L[1] - b * L[0])


def _eq(p, q):
    return p[0] * q[2] == q[0] * p[2] and p[1] * q[2] == q[1] * p[2]


def clip_h(poly, NX, NY, NB):
    """multibox._clip_frac by  NX x + NY y <= NB  (the line given as a positive multiple of the library's)."""
    if not poly:
        return poly
    m = len(poly)
    d = [NX * p[0] + NY * p[1] - NB * p[2] for p in poly]
    L = (NX, NY, -NB)
    out = []
    for i in range(m):
        j = (i + 1) % m
        dp, dq = d[i], d[j]
        if dp <= 0:
            out.append(poly[i])
        if (dp > 0) != (dq > 0):
            out.append(_meet_join(poly[i], poly[j], L))
    return out


def dedupe_h(P):
    out = []
    for p in P:
        if not out or not _eq(p, out[-1]):
            out.append(p)
    while len(out) > 1 and _eq(out[0], out[-1]):
        out.pop()
    return out


def _tri2_h(a, b, c):
    """(|2 area| numerator, denominator) of the triangle a b c."""
    det = (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0])
           + a[2] * (b[0] * c[1] - b[1] * c[0]))
    return abs(det), a[2] * b[2] * c[2]


def simplify_h(P, max_v):
    """multibox._simplify_frac: pop the FIRST minimal-area vertex while too many or the area is 0."""
    P = dedupe_h(list(P))
    while len(P) > 3:
        m = len(P)
        j, bn, bd = 0, None, None
        for i in range(m):
            n, d = _tri2_h(P[i - 1], P[i], P[(i + 1) % m])
            if bn is None or n * bd < bn * d:
                j, bn, bd = i, n, d
        if m > max_v or bn == 0:
            P.pop(j)
        else:
            break
    return P


def intersect_h(polys, max_v=16, work_v=28):
    """multibox.intersect_frac on homogeneous polygons ([] if empty or degenerate)."""
    if not polys:
        return []
    P = list(polys[0])
    for Q in polys[1:]:
        m = len(Q)
        for i in range(m):
            A, B = Q[i], Q[(i + 1) % m]
            nx1 = B[1] * A[2] - A[1] * B[2]                    # (by - ay) . AW BW
            ny1 = A[0] * B[2] - B[0] * A[2]                    # -(bx - ax) . AW BW
            if nx1 == 0 and ny1 == 0:
                continue
            P = clip_h(P, nx1 * A[2], ny1 * A[2], nx1 * A[0] + ny1 * A[1])
            if len(P) < 3:
                return []
        P = simplify_h(P, work_v)
        if len(P) < 3:
            return []
    return simplify_h(P, max_v)


def round_inward_h(P, shrink, den=MB.VDEN):
    """multibox._round_grid_inward: shrink about the centroid, round half-even to the 1/den grid, re-hull.
    -> [(X, Y)] integers over den, ccw."""
    n = len(P)
    L = 1
    for p in P:
        L = L * p[2] // math.gcd(L, p[2])
    SX = sum(p[0] * (L // p[2]) for p in P)
    SY = sum(p[1] * (L // p[2]) for p in P)
    S, Sd = _nd(shrink)
    out = []
    for (X, Y, W) in P:                                        # x' = cx sh + x (1 - sh)
        denom = n * L * Sd * W
        k, kk = S * W, (Sd - S) * n * L
        out.append((_rhe(den * (SX * k + X * kk), denom), _rhe(den * (SY * k + Y * kk), denom)))
    return PC._hull_frac(dedupe_i(out))


def dedupe_i(P):
    out = []
    for p in P:
        if not out or p != out[-1]:
            out.append(p)
    while len(out) > 1 and out[0] == out[-1]:
        out.pop()
    return out


# ------------------------------------------------------------------------------------ the two library entry points
def pieces_poly(pieces, n_grid=97, max_v=16, cache=None):
    """drop-in for multibox.pieces_poly (same protocol, same cache key, same info dict)."""
    boxes, polys = [], []
    for (bn, r) in pieces:
        pb, pt0, pt1 = MB.piece_box(bn, r)
        boxes.append((pb, pt0, pt1))
        key = (bn.t0, bn.t1, r, n_grid, max_v)
        pc = None if cache is None else cache.get(key)
        if pc is None:
            pc = PC.build(pb, n_grid=n_grid, max_v=max_v)
            if cache is not None:
                cache[key] = pc
        polys.append([hom(x, y) for (x, y) in pc.verts])
    P = intersect_h(polys, max_v=max_v)
    if len(P) < 3:
        return None, dict(reason="empty intersection", n_pieces=len(pieces)), boxes
    ibs = [ibox_of(pb, pt0, pt1) for (pb, pt0, pt1) in boxes]
    den = MB.VDEN
    for sh in MB.K_SHRINKS:
        V = round_inward_h(P, sh, den)
        if len(V) < 3:
            continue
        if not certify_h([(x, y, den) for (x, y) in V], ibs):
            Vf = [(Fr(x, den), Fr(y, den)) for (x, y) in V]
            return Vf, dict(shrink=str(sh), shrink_f=float(sh), n_pieces=len(pieces), nv=len(V),
                            area=float(MB.poly_area_frac(Vf))), boxes
    return None, dict(reason="no certified rounding", n_pieces=len(pieces)), boxes


def axis_core_pieces(V, boxes, tm, aden=MB.ADEN_DEFAULT, den=MB.VDEN):
    """drop-in for multibox.axis_core_pieces (V on the 1/den grid).  -> (kx, ky, a) Fractions or None."""
    n = len(V)
    Xs = [x.numerator * (den // x.denominator) for (x, _y) in V]
    Ys = [y.numerator * (den // y.denominator) for (_x, y) in V]
    KX, KY = _rhe(sum(Xs), n), _rhe(sum(Ys), n)
    TM, TD = _nd(tm)
    Q, CM, SM = TD * TD + TM * TM, TD * TD - TM * TM, 2 * TM * TD
    best = None                                                # a = SL Q / (den SUP)
    for i in range(n):
        AX, AY = Xs[i], Ys[i]
        j = (i + 1) % n
        NX, NY = Ys[j] - AY, AX - Xs[j]
        if NX == 0 and NY == 0:
            continue
        SL = NX * (AX - KX) + NY * (AY - KY)
        if SL <= 0:
            return None
        SUP = abs(NX * CM + NY * SM) + abs(NY * CM - NX * SM)
        if SUP <= 0:
            continue
        if best is None or SL * best[1] < best[0] * SUP:
            best = (SL, SUP)
    if best is None:
        return None
    AI = (best[0] * Q * aden) // (den * best[1])
    Wc = den * aden * Q
    kq, ibs = KX * aden * Q, [ibox_of(pb, pt0, pt1) for (pb, pt0, pt1) in boxes]
    kyq = KY * aden * Q
    for _try in range(4):
        if AI <= 0:
            return None
        ad = AI * den
        corners = [(kq + ad * (i * CM - j * SM), kyq + ad * (i * SM + j * CM), Wc)
                   for i, j in ((1, 1), (1, -1), (-1, -1), (-1, 1))]
        if not certify_h(corners, ibs):
            return Fr(KX, den), Fr(KY, den), Fr(AI, aden)
        AI = AI * 999999 // 1000000
    return None
