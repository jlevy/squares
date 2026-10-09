"""L-blocks (Lemma L + Corollary L) for `gen_zmmtree.py`: the exact integer mirror of
`Sqpack/LBlock.lean` (`lblkOk`, `lblkVal`) and the construction of a block from zm_mixed.py's
Lemma L data.  Nothing here is trusted: the Lean kernel re-checks every block.

Data (the Lean structures, field order):
  LLine = (dir, K, a, b, du, dd, roles, sU, iU, sD, iD, up, core, dn)   iU, iD signed ints
  LBlk  = (lines, corners, lg)      corners: 4 lists (one per box corner) of (oU, sigU, oD, sigD)
Pieces (j1, lo, hi): claim index + 1, coordinates over Q.  Fine units: 1/(W Q).
"""
import math
from fractions import Fraction as F

import gen_zmtree as G


# ------------------------------------------------------------------ small helpers (mirror of the Lean)

def lx(d, K, t):
    return K if d == 0 else t


def ly(d, K, t):
    return t if d == 0 else K


def on_line(S, d, K, e):
    X0, Y0, X1, Y1, _ = e
    if d == 0:
        return X0 == X1 and X0 * S == K and Y0 < Y1
    return Y0 == Y1 and Y0 * S == K and X0 < X1


def slo(S, d, e):
    return (e[1] if d == 0 else e[0]) * S


def shi(S, d, e):
    return (e[3] if d == 0 else e[2]) * S


def role(roles, k):
    return (roles // 4 ** k) % 4


def kend(d, k):
    if d == 0:
        return 1 if k % 2 == 0 else 2
    return 1 if k in (0, 3) else 2


def ktype(d, k):
    if d == 0:
        return 1 if k < 2 else 2
    return 2 if k < 2 else 1


def roles_ok(R, U0, U1, d, roles):
    for k in range(4):
        r = role(roles, k)
        if r != 0 and r != kend(d, k):
            return False
        if r != 0:
            if ktype(d, k) == 1 and not (0 < U0):
                return False
            if ktype(d, k) != 1 and not (U1 < R):
                return False
    return True


def tor(a, b):
    if a == 0:
        return b
    if b == 0:
        return a
    return a if a == b else 3


def sigq(R, f):
    return (0, 4 * R, 0) if f == 1 else (2 * R * R, 0, -2)


def tmul(f, R, n):
    n0, n1, n2 = n
    if f == 0:
        return (n0, n1, n2, 0, 0)
    if f == 1:
        k = 4 * R
        return (0, k * n0, k * n1, k * n2, 0)
    k = 2 * R * R
    return (k * n0, k * n1, k * n2 - 2 * n0, -2 * n1, -2 * n2)


def cmul(f, R, c):
    if f == 0:
        return (c, 0, 0, 0, 0)
    if f == 1:
        return (0, 4 * R * c, 0, 0, 0)
    if f == 2:
        return (2 * R * R * c, 0, -2 * c, 0, 0)
    return (0, 8 * R * R * R * c, 0, -8 * R * c, 0)


def padd(p, q):
    return tuple(a + b for a, b in zip(p, q))


def pneg(p):
    return tuple(-a for a in p)


def term(R, f, t):
    typ, n = t
    return cmul(f, R, n[0]) if typ == 0 else tmul(f - typ, R, n)


def opt_n(ctx, l, s, i, t, k, cx, cy):
    d, K = l[0], l[1]
    g = G.gq(ctx, k, lx(d, K, t) - cx, ly(d, K, t) - cy)
    sq = sigq(ctx.R, ktype(d, k))
    return tuple(i * sq[j] - s * g[j] for j in range(3))


def opt_t(ctx, l, up, cap, o, cx, cy):
    if o == 0:
        return (0, (cap, 0, 0))
    k = o - 1
    if up:
        return (ktype(l[0], k), opt_n(ctx, l, l[7], l[8], l[2], k, cx, cy))
    return (ktype(l[0], k), opt_n(ctx, l, l[9], l[10], l[3], k, cx, cy))


def is_opt(l, up, o):
    return o == 0 or (o <= 4 and role(l[6], o - 1) == (1 if up else 2))


def slack_ok(ctx, U0, U1, l, up, cap, ch, sg, cx, cy, o):
    t1 = opt_t(ctx, l, up, cap, ch, cx, cy)
    t2 = opt_t(ctx, l, up, cap, o, cx, cy)
    f = tor(t1[0], t2[0])
    P = padd(padd(term(ctx.R, f, t1), pneg(term(ctx.R, f, t2))), pneg(cmul(f, ctx.R, sg)))
    return G.bok(P, U0, U1)


def end_ok(ctx, U0, U1, l, up, cap, ch, sg, cx, cy):
    if not is_opt(l, up, ch):
        return False
    return all((not is_opt(l, up, o)) or slack_ok(ctx, U0, U1, l, up, cap, ch, sg, cx, cy, o)
               for o in range(5))


# ------------------------------------------------------------------ zones, gains

def pent(cls, p):
    j = p[0] - 1
    return cls[j][0] if 0 <= j < len(cls) else (0, 0, 0, 0, 0)


def ptag(cls, p):
    j = p[0] - 1
    return cls[j][1] if 0 <= j < len(cls) else 0


def rho(S, Q, cls, l, p):
    e = pent(cls, p)
    ln = shi(S, l[0], e) - slo(S, l[0], e)
    return (e[4] * Q) // ln if ln > 0 else 0


def cmass(S, cls, l, p):
    e = pent(cls, p)
    ln = shi(S, l[0], e) - slo(S, l[0], e)
    return (e[4] * max(p[2] - p[1], 0)) // ln if ln > 0 else 0


def ell_le(s, i, X, C):
    return s * X + i <= C


def gain_ok(s, i, D, C, L):
    for (r, o0, o1) in L:
        if not (ell_le(s, i, o0, C) and ell_le(s, i, o1, C + r * max(o1 - o0, 0))):
            return False
        C = C + r * max(o1 - o0, 0)
    return ell_le(s, i, D, C)


def gain_sum(C, L):
    for (r, o0, o1) in L:
        C += r * max(o1 - o0, 0)
    return C


def up_off(S, Q, cls, l):
    a = l[2]
    return [(rho(S, Q, cls, l, p), max(p[1] - a, 0), max(p[2] - a, 0)) for p in l[11]]


def dn_off(S, Q, cls, l):
    b = l[3]
    return list(reversed([(rho(S, Q, cls, l, p), max(b - p[2], 0), max(b - p[1], 0)) for p in l[13]]))


def cap_u(S, Q, cls, l):
    return gain_sum(0, up_off(S, Q, cls, l))


def cap_d(S, Q, cls, l):
    return gain_sum(0, dn_off(S, Q, cls, l))


def core_val(S, cls, l):
    return sum(cmass(S, cls, l, p) for p in l[12])


def lpc_ok(S, tag, cls, l, zlo, zhi, p):
    j1, lo, hi = p
    j = j1 - 1
    if not (0 <= j < len(cls)):
        return False
    e, t = cls[j]
    return (t == tag and on_line(S, l[0], l[1], e) and slo(S, l[0], e) <= lo <= hi <= shi(S, l[0], e)
            and zlo <= lo and hi <= zhi)


def psorted(L):
    return all(p[2] <= q[1] for p, q in zip(L, L[1:]))


def lcert_ok(ctx, box, l):
    d, K, a, b, du, dd, roles = l[:7]
    R = ctx.R
    U0, U1 = box[4], box[5]
    if not (b <= a and dd <= b and roles_ok(R, U0, U1, d, roles)):
        return False
    for k in range(4):
        r = role(roles, k)
        if r == 1:
            if not G.admk(ctx, k, lx(d, K, a), ly(d, K, a), box):
                return False
        elif r == 2:
            if not G.admk(ctx, k, lx(d, K, b), ly(d, K, b), box):
                return False
        else:
            if not (G.admk(ctx, k, lx(d, K, b - dd), ly(d, K, b - dd), box)
                    and G.admk(ctx, k, lx(d, K, a + du), ly(d, K, a + du), box)):
                return False
    return True


def lpcs_ok(ctx, tag, cls, l):
    S, Q = ctx.S, ctx.Q
    a, b, du, dd = l[2], l[3], l[4], l[5]
    return (all(lpc_ok(S, tag, cls, l, a, a + du, p) for p in l[11]) and psorted(l[11])
            and all(lpc_ok(S, tag, cls, l, b, a, p) for p in l[12]) and psorted(l[12])
            and all(lpc_ok(S, tag, cls, l, b - dd, b, p) for p in l[13]) and psorted(l[13])
            and gain_ok(l[7], l[8], du, 0, up_off(S, Q, cls, l))
            and gain_ok(l[9], l[10], dd, 0, dn_off(S, Q, cls, l)))


def corner_ok(ctx, box, cls, lg, cx, cy, lc):
    S, Q, R = ctx.S, ctx.Q, ctx.R
    U0, U1 = box[4], box[5]
    f = 0
    for l, c in lc:
        f = tor(tor(opt_t(ctx, l, True, cap_u(S, Q, cls, l), c[0], cx, cy)[0],
                    opt_t(ctx, l, False, cap_d(S, Q, cls, l), c[2], cx, cy)[0]), f)
    P = (0, 0, 0, 0, 0)
    sgs = 0
    for l, c in lc:
        cu, cd = cap_u(S, Q, cls, l), cap_d(S, Q, cls, l)
        if not (end_ok(ctx, U0, U1, l, True, cu, c[0], c[1], cx, cy)
                and end_ok(ctx, U0, U1, l, False, cd, c[2], c[3], cx, cy)):
            return False
        P = padd(P, padd(term(R, f, opt_t(ctx, l, True, cu, c[0], cx, cy)),
                         term(R, f, opt_t(ctx, l, False, cd, c[2], cx, cy))))
        sgs += c[1] + c[3]
    return G.bok(pneg(padd(P, pneg(cmul(f, R, sgs + lg)))), U0, U1)


def lblk_ok(ctx, box, cls, tag, B):
    lines, corners, lg = B
    x0, x1, y0, y1 = box[:4]
    for l, m in zip(lines, lines[1:]):
        if not (l[0] < m[0] or (l[0] == m[0] and l[1] < m[1])):
            return False
    for l in lines:
        if not (l[0] <= 1 and lcert_ok(ctx, box, l) and lpcs_ok(ctx, tag, cls, l)):
            return False
    if len(corners) != 4 or any(len(c) != len(lines) for c in corners):
        return False
    for (cx, cy), ch in zip(((x0, y0), (x0, y1), (x1, y0), (x1, y1)), corners):
        if not corner_ok(ctx, box, cls, lg, cx, cy, list(zip(lines, ch))):
            return False
    return True


def lblk_val(ctx, cls, B):
    lines, _, lg = B
    return sum(core_val(ctx.S, cls, l) for l in lines) + lg // ctx.Q


# ------------------------------------------------------------------ exact degree-4 Bernstein bounds

def bern4(p, U0, U1):
    """the five (scaled, positive factor 12 H^4-free) Bernstein-test combinations of G.bok, as values whose
    signs are those of the Bernstein coefficients: returns [c0..c4] with sign(c_i) = sign(beta_i)."""
    p0, p1, p2, p3, p4 = p
    H = U1 - U0
    b0 = p0 + U0 * (p1 + U0 * (p2 + U0 * (p3 + U0 * p4)))
    b1 = H * (p1 + U0 * (2 * p2 + U0 * (3 * p3 + U0 * 4 * p4)))
    b2 = H * H * (p2 + U0 * (3 * p3 + U0 * 6 * p4))
    b3 = H * H * H * (p3 + U0 * 4 * p4)
    b4 = H * H * H * H * p4
    return [b0, 4 * b0 + b1, 6 * b0 + 3 * b1 + b2, 4 * b0 + 3 * b1 + 2 * b2 + b3, b0 + b1 + b2 + b3 + b4]


def ratio_bound(P, Den, U0, U1, upper):
    """the least integer s with P - s Den <= 0 on the bin (upper) or the greatest s with P - s Den >= 0
    (lower), by the degree-4 Bernstein test (all coefficients of Den must be > 0); None otherwise.
    The combinations of bern4 are linear with positive weights, so they apply to P - s Den termwise."""
    bp = bern4(P, U0, U1)
    bd = bern4(Den, U0, U1)
    if any(v <= 0 for v in bd):
        return None
    rs = [F(a, c) for a, c in zip(bp, bd)]
    if upper:
        return math.ceil(max(rs))
    return math.floor(min(rs))


# ------------------------------------------------------------------ building a block

def lower_hull_edge(pts, xm):
    """the edge of the lower convex hull of pts (sorted by x) containing xm; (slope, intercept) Fractions."""
    H = []
    for p in pts:
        while len(H) >= 2 and (H[-1][0] - H[-2][0]) * (p[1] - H[-2][1]) - (H[-1][1] - H[-2][1]) * (p[0] - H[-2][0]) <= 0:
            H.pop()
        H.append(p)
    if len(H) == 1:
        return F(0), F(H[0][1])
    for j in range(len(H) - 1):
        if H[j + 1][0] >= xm or j == len(H) - 2:
            (x0, y0), (x1, y1) = H[j], H[j + 1]
            sl = F(y1 - y0, x1 - x0)
            return sl, F(y0) - sl * x0


def minorant(off, D, xm):
    """(s, i) integers with s >= 0 and gain_ok(s, i, D, 0, off), from the hull edge at xm; None if none."""
    pts = [(0, 0)]
    C = 0
    for (r, o0, o1) in off:
        pts.append((o0, C))
        C += r * (o1 - o0)
        pts.append((o1, C))
    pts.append((D, C))
    # dedupe x: keep the smallest value per x (the function is nondecreasing: the first occurrence)
    q = {}
    for x, y in pts:
        if x not in q or y < q[x]:
            q[x] = y
    pts = sorted(q.items())
    sl, ic = lower_hull_edge(pts, xm)
    s = max(math.floor(sl), 0)
    i = math.floor(ic)
    for _ in range(64):
        if gain_ok(s, i, D, 0, off):
            return s, i
        i -= 1 + abs(i) // 1000
    return None
