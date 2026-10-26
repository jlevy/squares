"""Lemma K (`CapK.capOk`), exactly, and the search of its certificate.

A leaf box `(x0, x1, y0, y1)` over `Q = D S`, angles `u in [U0/R, U1/R]`.  The certificate is the
Lebesgue rectangle `e` and, per side (`x = e.1/D`, `y = e.2.1/D`), `('far',)` or
`('chain', [(p0, p1, w), ...], rho)`: contiguous pieces of the cover on the line (over `D`) with
weight per length `>= rho`, covering the chord of every square of the box.
"""
from fractions import Fraction as F


def widN(R, U0, U1): return max(0, R * R + 2 * U1 * R - U0 * U0)
def widD(R, U0): return R * R + U0 * U0
def cminQ(R, U1): return F(R * R - U1 * U1, R * R + U1 * U1)
def cmaxQ(R, U0): return F(R * R - U0 * U0, R * R + U0 * U0)
def sminQ(R, U0): return F(2 * U0 * R, R * R + U0 * U0)
def smaxQ(R, U1): return F(2 * U1 * R, R * R + U1 * U1)


def chainN(P, pcs):
    for p in pcs:
        if not (p[0] == P and p[0] < p[1]): return False
        P = p[1]
    return True


def endN(P, pcs):
    return pcs[-1][1] if pcs else P


def sideOk(D, a, cx0, cy0, cy1, w, we, cmin, cmax, smin, smax, sc):
    """`CapK.sideOk`"""
    if sc[0] == 'far':
        return a + w / 2 <= cx0
    pcs, rho = sc[1], sc[2]
    if not pcs: return False
    P = F(pcs[0][0], D); E = F(endN(pcs[0][0], pcs), D)
    dbar = a - cx0 + w / 2
    return (a <= cx0 and 0 <= rho and we * dbar <= rho and chainN(pcs[0][0], pcs)
            and all(rho * (F(q[1] - q[0], D)) <= q[2] for q in pcs)
            and (P <= cy0 - w / 2 or (0 < smin and P <= cy0 + (cmin - smax) / 2 - cmax / smin * dbar))
            and (cy1 + w / 2 <= E or (0 < cmin and cy1 + (cmax - smin) / 2 + smax / cmin * dbar <= E)))


def vSeg(A, p): return (A, p[0], A, p[1], p[2])
def hSeg(A, p): return (p[0], A, p[1], A, p[2])


def capOk(D, S, R, W, x0, x1, y0, y1, U0, U1, segs, rects, k):
    """`CapK.capOk`"""
    e, sx, sy = k
    Q = F(D * S); w = F(widN(R, U0, U1), widD(R, U0)); we = F(e[4])
    pcs = lambda sc: sc[1] if sc[0] == 'chain' else []
    segsK = [vSeg(e[0], p) for p in pcs(sx)] + [hSeg(e[1], p) for p in pcs(sy)]
    return (U1 < R and U0 <= U1 and tuple(e) in rects and W <= e[4]
            and F(x1) / Q + w / 2 <= F(e[2], D) and F(y1) / Q + w / 2 <= F(e[3], D)
            and len(set(segsK)) == len(segsK) and all(x in segs for x in segsK)
            and sideOk(D, F(e[0], D), F(x0) / Q, F(y0) / Q, F(y1) / Q, w, we,
                       cminQ(R, U1), cmaxQ(R, U0), sminQ(R, U0), smaxQ(R, U1), sx)
            and sideOk(D, F(e[1], D), F(y0) / Q, F(x0) / Q, F(x1) / Q, w, we,
                       sminQ(R, U0), smaxQ(R, U1), cminQ(R, U1), cmaxQ(R, U0), sy))


def _side(D, a, cx0, cy0, cy1, w, we, cmin, cmax, smin, smax, line):
    """a side certificate: 'far', or the shortest chain of `line` (pieces (p0, p1, w) sorted) that
    covers the needed range"""
    if a + w / 2 <= cx0:
        return ('far',)
    if a > cx0:
        return None
    dbar = a - cx0 + w / 2
    lows = [cy0 - w / 2]
    highs = [cy1 + w / 2]
    if smin > 0: lows.append(cy0 + (cmin - smax) / 2 - cmax / smin * dbar)
    if cmin > 0: highs.append(cy1 + (cmax - smin) / 2 + smax / cmin * dbar)
    lo, hi = max(lows), min(highs)
    # the pieces meeting [lo, hi]: contiguous from one with p0 <= lo to one with p1 >= hi
    sel = [p for p in line if F(p[1], D) > lo and F(p[0], D) < hi]
    if not sel or F(sel[0][0], D) > lo or F(sel[-1][1], D) < hi or not chainN(sel[0][0], sel):
        return None
    rho = min(F(p[2] * D, p[1] - p[0]) for p in sel)
    sc = ('chain', sel, rho)
    return sc if sideOk(D, a, cx0, cy0, cy1, w, we, cmin, cmax, smin, smax, sc) else None


def certify(D, S, R, W, x0, x1, y0, y1, U0, U1, segs, rects):
    """a certificate `(e, sx, sy)` passing `capOk`, or None"""
    Q = F(D * S); w = F(widN(R, U0, U1), widD(R, U0))
    for e in rects:
        we = F(e[4])
        vline = sorted((s_[1], s_[3], s_[4]) for s_ in segs if s_[0] == s_[2] == e[0])
        hline = sorted((s_[0], s_[2], s_[4]) for s_ in segs if s_[1] == s_[3] == e[1])
        sx = _side(D, F(e[0], D), F(x0) / Q, F(y0) / Q, F(y1) / Q, w, we,
                   cminQ(R, U1), cmaxQ(R, U0), sminQ(R, U0), smaxQ(R, U1), vline)
        sy = _side(D, F(e[1], D), F(y0) / Q, F(x0) / Q, F(x1) / Q, w, we,
                   sminQ(R, U0), smaxQ(R, U1), cminQ(R, U1), cmaxQ(R, U0), hline)
        if sx is None or sy is None: continue
        k = (tuple(e), sx, sy)
        if capOk(D, S, R, W, x0, x1, y0, y1, U0, U1, segs, rects, k):
            return k
    return None


def lean_side(sc):
    if sc[0] == 'far': return "CapK.SideC.far"
    pcs = ", ".join(f"({p[0]}, {p[1]}, {p[2]})" for p in sc[1])
    return f"(CapK.SideC.chain [{pcs}] ({sc[2].numerator} / {sc[2].denominator} : ℚ))"


def to_lean(k, name, D, S, R, W, box, segs="tsegs", rects="trects"):
    """the certificate and its test"""
    e, sx, sy = k
    x0, x1, y0, y1, U0, U1 = box
    return (f"def {name} : CapK.CapC := ⟨{tuple(e)}, {lean_side(sx)}, {lean_side(sy)}⟩\n\n"
            f"theorem {name}_ok : CapK.capOk {D} {S} {R} {W} {x0} {x1} {y0} {y1} {U0} {U1} {segs} {rects} "
            f"{name} = true := by decide +kernel\n")
