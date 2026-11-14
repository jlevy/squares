#!/usr/bin/env python3
"""tt_box: rigorous certification of mu >= 1 near a tight tile, in blown-up chart coordinates.

Chart: two face coordinates (p, q) in a convex polygon, one scale coordinate h in [0, h0].  The pose is
    centre  = (cx0 + h*cx1, cy0 + h*cy1),   tan(theta/2) = h*a,
where cx0, cx1, cy0, cy1, a are affine in (p, q) (given per chart).  For h > 0 the square is tilted (a != 0 on the chart).

For every axis-parallel segment i of the cover, its clipped length is l_i = max(0, min H_i - max L_i) where
H_i = {1} u {upper bounds B/A}, L_i = {0} u {lower bounds B/A} come from the 4 half-plane constraints of the square
(A, B exact polynomials in (p, q, h) after clearing 1+u^2).  The maximal common monomial factor of (A, B) is divided
out EXACTLY.  Then:
  * if A(h=0) == 0 identically the constraint diverges as h -> 0 and must be proved INACTIVE on the prism (interval
    test: upper bound with B >= A >= 0, or lower bound with A <= 0 <= B); otherwise the prism is refused;
  * else A(h=0) must be a nonzero CONSTANT and B(h=0) AFFINE in (p, q): the face value t(0) = B0/A0 is affine.  The
    prism must keep sign(A) (interval test), so t(h) = B/A is C^1 on the closed prism, with derivative
    t' = (B_h A - B A_h)/A^2 bounded by exact interval arithmetic.
Face structure: on the polygon, for each segment, one upper bound j* is <= all others and one lower bound k* >= all
others AT EVERY VERTEX, and f = t_j* - t_k* has one sign at every vertex.  These are affine functions, so the
vertex tests hold on the whole polygon (exact).  If a test fails, the polygon is split by the offending line.
Then G(p,q) = mu at h = 0 is affine on the polygon (exact), and for 0 <= h <= h0 (mean-value inequality, Lipschitz):
    t_j(h) >= t_j(0) + h * inf t_j',   t_k(h) <= t_k(0) + h * sup t_k'
    min H(h) - t_j*(0) >= min_j ( gH_j + h inf t_j' ),   gH_j = min_vertices (t_j - t_j*)(0) >= 0
    max L(h) - t_k*(0) <= max_k ( -gL_k + h sup t_k' ),  gL_k = min_vertices (t_k* - t_k)(0) >= 0
    l_i(h) - l_i(0) >= 0 if f <= 0 on the polygon, else >= [min H(h) - t_j*(0)] - [max L(h) - t_k*(0)]
Summing w_i times these concave piecewise-linear lower bounds gives mu(h) - 1 >= Gmin + Delta(h), concave in h, so
it suffices to check h = 0 (Gmin >= 0) and h = h0.  Everything is exact Fractions.
"""
import sys, json
from fractions import Fraction as F
from ttpoly import P, padd, pscale, pmul, pdiff_h, pat_h0, pmindeg, pdivmono, pdeg_pq, peval, ieval, idiv, fpoly, fI, feval, fdiv

def load(path):
    L = open(path).read().split('\n'); i = 0
    while not L[i].split() or L[i].startswith('#') or L[i].startswith('mixed'): i += 1
    pitch = int(L[i+1]); wden = int(L[i+2]); n = int(L[i+4])
    segs = [tuple(int(t) for t in L[i+5+j].split()) for j in range(n)]
    return [((F(a, pitch), F(b, pitch)), (F(c, pitch), F(d, pitch)), F(w, wden)) for a, b, c, d, w in segs]

AFF = lambda c, cp=0, cq=0: padd(P(c), P(cp, (1, 0, 0)), P(cq, (0, 1, 0)))
Hv = P(1, (0, 0, 1))

def wedge_subst(p, widx):
    """substitute h = v * x_widx (x_0 = p, x_1 = q) and divide by the largest common power of x_widx (> 0 on the
    region), returning a polynomial in (p, q, v)"""
    r = {}
    for (i, j, k), c in p.items():
        e = (i+k, j, k) if widx == 0 else (i, j+k, k)
        r[e] = r.get(e, 0) + c
    r = {e: c for e, c in r.items() if c != 0}
    if not r: return r
    m = min(e[widx] for e in r)
    return {((e[0]-m, e[1], e[2]) if widx == 0 else (e[0], e[1]-m, e[2])): c for e, c in r.items()}

def apex_subst(p, widx):
    """after wedge_subst: on the region x_widx <= x_other, substitute x_widx = w * x_other (w in [0,1]) and divide by
    the largest power of x_other; result is a polynomial in (w, x_other, v) stored in the (p, q, h) slots with
    w in the slot of x_widx"""
    o = 1 - widx; r = {}
    for e, c in p.items():
        e = list(e); e[o] += e[widx]; e = tuple(e)
        r[e] = r.get(e, 0) + c
    r = {e: c for e, c in r.items() if c != 0}
    if not r: return r
    m = min(e[o] for e in r)
    return {tuple(x - (m if t == o else 0) for t, x in enumerate(e)): c for e, c in r.items()}

def apex2_subst(p, widx):
    """after wedge_subst (h = v x_w): on the region |x_o| <= x_w substitute x_o = w x_w (w in [-1, 1]) and divide by
    the largest power of x_w; w is stored in the slot of x_o"""
    o = 1 - widx; r = {}
    for e, c in p.items():
        e = list(e); e[widx] += e[o]; e = tuple(e)
        r[e] = r.get(e, 0) + c
    r = {e: c for e, c in r.items() if c != 0}
    if not r: return r
    m = min(e[widx] for e in r)
    return {tuple(x - (m if t == widx else 0) for t, x in enumerate(e)): c for e, c in r.items()}

class Con:
    """one half-plane constraint of one segment"""
    __slots__ = ('kind', 'A', 'B', 'a0', 'b0', 'num', 'den', 'const', 'fA', 'fB', 'fBA', 'fnum', 'fden', 'fBw', 'fBAw', 'fBx', 'fBAx', 'fBy', 'fBAy')
def build_constraints(seg, chart):
    (x0, y0), (x1, y1), w = seg
    dx, dy = x1 - x0, y1 - y0
    cx = padd(chart['cx0'], pmul(Hv, chart['cx1'])); cy = padd(chart['cy0'], pmul(Hv, chart['cy1']))
    u = pmul(Hv, chart['a']); u2 = pmul(u, u)
    N = padd(P(1), u2); NC = padd(P(1), pscale(-1, u2)); NS = pscale(2, u)
    X0 = padd(P(x0), pscale(-1, cx)); Y0 = padd(P(y0), pscale(-1, cy))
    out = []
    for a, b in ((NC, NS), (pscale(-1, NS), NC)):
        s0 = padd(pmul(X0, a), pmul(Y0, b)); ds = padd(pscale(dx, a), pscale(dy, b))
        for sg in (1, -1):
            A = pscale(sg, ds); B = padd(pscale(F(1, 2), N), pscale(-sg, s0))
            c = Con(); c.A, c.B = A, B
            if not A:
                c.kind = 'const'; out.append(c); continue
            if B:
                m = pmindeg([A, B])
                # divide out h^k always (h > 0 on the region proved); p^i, q^j only for chart variables known > 0
                m = (m[0] if 'p' in chart.get('pos', '') else 0, m[1] if 'q' in chart.get('pos', '') else 0, m[2])
                A = pdivmono(A, m); B = pdivmono(B, m)
            c.A, c.B = A, B; c.fA = fpoly(A); c.fB = fpoly(B); c.fBA = fpoly(padd(B, pscale(-1, A)))
            if chart.get('wedge'):
                wi = chart['wedge'][0]; bw_ = wedge_subst(B, wi); baw_ = wedge_subst(padd(B, pscale(-1, A)), wi)
                c.fBw = fpoly(bw_); c.fBAw = fpoly(baw_)
                if chart.get('apex'): c.fBx = fpoly(apex_subst(bw_, wi)); c.fBAx = fpoly(apex_subst(baw_, wi))
                if chart.get('apex2'): c.fBy = fpoly(apex2_subst(bw_, wi)); c.fBAy = fpoly(apex2_subst(baw_, wi))
            a0 = pat_h0(A); b0 = pat_h0(B)
            if not a0:
                c.kind = 'div'
            else:
                if any(e != (0, 0, 0) for e in a0): c.kind = 'bad-nonconst-A0'; out.append(c); continue
                if pdeg_pq(b0) > 1: c.kind = 'bad-nonaffine-B0'; out.append(c); continue
                c.kind = 'reg'; c.a0 = a0[(0, 0, 0)]; c.b0 = b0
                c.num = padd(pmul(pdiff_h(B), A), pscale(-1, pmul(B, pdiff_h(A)))); c.den = pmul(A, A)
                c.fnum = fpoly(c.num); c.fden = fpoly(c.den)
            out.append(c)
    return out

def bbox(poly):
    xs = [v[0] for v in poly]; ys = [v[1] for v in poly]; return (min(xs), max(xs)), (min(ys), max(ys))

def seg_reach(seg, chart, polyg, h0):
    """cheap exact test: can the segment meet the square anywhere on the prism?  (bbox of pose centres +- 3/4)"""
    (x0, y0), (x1, y1), w = seg
    X, Y = bbox(polyg); Hh = (F(0), h0)
    cx = ieval(padd(chart['cx0'], pmul(Hv, chart['cx1'])), X, Y, Hh); cy = ieval(padd(chart['cy0'], pmul(Hv, chart['cy1'])), X, Y, Hh)
    r = F(3, 4)
    return not (max(x0, x1) < cx[0]-r or min(x0, x1) > cx[1]+r or max(y0, y1) < cy[0]-r or min(y0, y1) > cy[1]+r)

def split_poly(poly, lin):
    """split convex polygon by affine function lin(p,q) = 0; lin given as poly in p,q"""
    f = [peval(lin, v[0], v[1]) for v in poly]
    L, R = [], []
    for i in range(len(poly)):
        p, q, fp, fq = poly[i], poly[(i+1) % len(poly)], f[i], f[(i+1) % len(poly)]
        if fp <= 0: L.append(p)
        if fp >= 0: R.append(p)
        if (fp < 0 < fq) or (fq < 0 < fp):
            t = fp/(fp-fq); x = (p[0]+t*(q[0]-p[0]), p[1]+t*(q[1]-p[1])); L.append(x); R.append(x)
    return [Q for Q in (L, R) if len(Q) >= 3 and area2(Q) != 0]
def area2(Q): return sum(Q[i][0]*Q[(i+1) % len(Q)][1] - Q[(i+1) % len(Q)][0]*Q[i][1] for i in range(len(Q)))

def _sign2(fb, fba, boxes, aux, depth=8):
    """decide on the box product: 'in' if B >= 0 and B - A >= 0 everywhere, 'empty' if B < 0 and B - A < 0 everywhere,
    else None.  aux = slots (0,1,2) that are auxiliary substitution variables (v, w); on failure the widest aux interval
    is bisected (the sub-boxes cover the box, so a common verdict on all of them is a verdict on the box)."""
    b = feval(fb, *boxes); ba = feval(fba, *boxes)
    if b[0] >= 0 and ba[0] >= 0: return 'in'
    if b[1] < 0 and ba[1] < 0: return 'empty'
    if depth == 0 or not aux: return None
    k = max(aux, key=lambda t: boxes[t][1] - boxes[t][0]); lo, hi = boxes[k]; m = 0.5*(lo + hi)
    if not (lo < m < hi): return None
    r = []
    for part in ((lo, m), (m, hi)):
        bx = list(boxes); bx[k] = part
        v = _sign2(fb, fba, tuple(bx), aux, depth-1)
        if v is None or (r and v != r[0]): return None
        r.append(v)
    return r[0]

class Result(Exception): pass
DEBUG = None

def analyse(segcons, chart, polyg, h0, need_reach=True, low=None, high=None):
    """cell = {(p,q) in polyg, low(p,q) <= h <= high(p,q)} (low, high affine; default 0 and h0), a convex polytope
    whose vertices are (v, low(v)), (v, high(v))."""
    low = low if low is not None else P(0); high = high if high is not None else P(h0)
    """returns ('ok', info) | ('split', lin) | ('fail', reason, info)"""
    X, Y = bbox(polyg); V = polyg
    h0 = max(peval(high, v[0], v[1]) for v in V); Hh = (F(0), h0)
    fX, fY, fH = fI(X), fI(Y), fI(Hh)
    ccx = feval(fpoly(padd(chart['cx0'], pmul(Hv, chart['cx1']))), fX, fY, fH); ccy = feval(fpoly(padd(chart['cy0'], pmul(Hv, chart['cy1']))), fX, fY, fH)
    Gv = [F(-1)]*len(V); cands = []; info = {}
    AT = chart.get('area_term'); area_m = None
    if AT is not None:
        # area kinks: split the polygon by any face line where Ax or Ay changes slope
        for lin in AT.kink_lines():
            vals = [peval(lin, v[0], v[1]) for v in V]
            if min(vals) < 0 < max(vals): return ('split', lin)
        axy = [AT.face_vertex(v) for v in V]
        ax_ = [a for a, b in axy]; ay_ = [b for a, b in axy]
        if min(ax_) == max(ax_) or min(ay_) == max(ay_): avals = [a*b for a, b in axy]
        else:   # McCormick affine lower bound of the bilinear face value
            axm, aym = min(ax_), min(ay_); avals = [axm*b + a*aym - axm*aym for a, b in axy]
        for t in range(len(V)): Gv[t] += AT.rho*avals[t]
        area_m = AT.deriv_lower(fX, fY, fH)
        if area_m is None: return ('fail', 'area derivative not bounded', {})
    for seg, cons in segcons:
        (x0_, y0_), (x1_, y1_), _w = seg
        if need_reach and (max(x0_, x1_) < ccx[0]-0.75 or min(x0_, x1_) > ccx[1]+0.75 or max(y0_, y1_) < ccy[0]-0.75 or min(y0_, y1_) > ccy[1]+0.75): continue
        w = seg[2]
        Hs = [('one', None)]; Ls = [('zero', None)]; empty = False
        for c in cons:
            if c.kind == 'const':
                b = feval(c.fB, fX, fY, fH)
                if b[0] >= 0: continue
                if b[1] < 0: empty = True; break
                return ('fail', 'const-constraint ambiguous', {})
            if c.kind == 'bad-nonaffine-B0': return ('fail', c.kind, {'seg': str(seg)})
            a = feval(c.fA, fX, fY, fH)
            if c.kind in ('div', 'bad-nonconst-A0'):
                # constraint t*A <= B for t in [0,1]:  t*A lies in [min(0,A), max(0,A)]
                b = feval(c.fB, fX, fY, fH)
                if b[0] >= max(0.0, a[1]): continue                      # satisfied for every t: inactive
                if b[1] < min(0.0, a[0]): empty = True; break            # violated for every t: segment misses Q
                if chart.get('wedge'):
                    # on a wedge chart h <= c * x_w: substitute h = v x_w (v in [0, c]) and divide by x_w^m (exact);
                    # B >= max(0, A)  <=>  B >= 0 and B - A >= 0;   B < min(0, A)  <=>  B < 0 and B - A < 0
                    V_ = (0.0, float(chart['wedge'][1])) if F(float(chart['wedge'][1])) == chart['wedge'][1] else fI((F(0), chart['wedge'][1]))
                    vd = _sign2(c.fBw, c.fBAw, (fX, fY, V_), (2,))
                    if vd == 'in': continue
                    if vd == 'empty': empty = True; break
                    if chart.get('apex'):
                        # wedge variable <= the other face variable on this chart: x_w = w x_o, w in [0, 1]
                        wi = chart['wedge'][0]; aw = F(chart.get('apex_w', 1)); Wr = (0.0, float(aw)) if F(float(aw)) == aw else fI((F(0), aw))
                        boxes = (Wr, fY) if wi == 0 else (fX, Wr)
                        vd = _sign2(c.fBx, c.fBAx, (boxes[0], boxes[1], V_), (wi, 2))
                        if vd == 'in': continue
                        if vd == 'empty': empty = True; break
                    if chart.get('apex2'):
                        # sector |x_o| <= x_w around a corner: x_o = w x_w, w in [-1, 1]
                        wi = chart['wedge'][0]; Wr = (-1.0, 1.0)
                        boxes = (fX, Wr) if wi == 0 else (Wr, fY)
                        vd = _sign2(c.fBy, c.fBAy, (boxes[0], boxes[1], V_), (1 - wi, 2))
                        if vd == 'in': continue
                        if vd == 'empty': empty = True; break
                return ('fail', 'divergent constraint not provably inactive', {'seg': str(seg)})
            if not (a[0] > 0 or a[1] < 0): return ('fail', 'A changes sign on prism', {'seg': str(seg)})
            (Hs if c.a0 > 0 else Ls).append(('reg', c))
        if empty: continue
        # face values at vertices
        def fv(item, v):
            k, c = item
            if k == 'one': return F(1)
            if k == 'zero': return F(0)
            return peval(c.b0, v[0], v[1]) / c.a0
        def flin(item):          # affine face function as polynomial in p,q
            k, c = item
            if k == 'one': return P(1)
            if k == 'zero': return P(0)
            return pscale(1/c.a0, c.b0)
        hv = [[fv(it, v) for v in V] for it in Hs]; lv = [[fv(it, v) for v in V] for it in Ls]
        nv = range(len(V))
        js = min(range(len(Hs)), key=lambda j: (hv[j][0], sum(hv[j])))
        for j in range(len(Hs)):
            d = [hv[j][t] - hv[js][t] for t in nv]
            if min(d) < 0 and max(d) > 0: return ('split', padd(flin(Hs[j]), pscale(-1, flin(Hs[js]))))
            if min(d) < 0: js = j                       # j <= js at every vertex: j is the better candidate
        for j in range(len(Hs)):
            d = [hv[j][t] - hv[js][t] for t in nv]
            if min(d) < 0: return ('split', padd(flin(Hs[j]), pscale(-1, flin(Hs[js])))) if max(d) > 0 else ('fail', 'no global min upper bound', {})
        ks = max(range(len(Ls)), key=lambda k: (lv[k][0], sum(lv[k])))
        for k in range(len(Ls)):
            d = [lv[k][t] - lv[ks][t] for t in nv]
            if min(d) < 0 and max(d) > 0: return ('split', padd(flin(Ls[k]), pscale(-1, flin(Ls[ks]))))
            if max(d) > 0: ks = k
        for k in range(len(Ls)):
            d = [lv[k][t] - lv[ks][t] for t in nv]
            if max(d) > 0: return ('split', padd(flin(Ls[k]), pscale(-1, flin(Ls[ks])))) if min(d) < 0 else ('fail', 'no global max lower bound', {})
        fvals = [hv[js][t] - lv[ks][t] for t in range(len(V))]
        if min(fvals) < 0 < max(fvals): return ('split', padd(flin(Hs[js]), pscale(-1, flin(Ls[ks]))))
        if max(fvals) > 0:
            for t in range(len(V)): Gv[t] += w*fvals[t]
        # first-order lower bound at h = h0 (concave in h; h = 0 gives 0)
        def dbound(item, lower):
            k, c = item
            if k in ('one', 'zero'): return F(0)
            r = fdiv(feval(c.fnum, fX, fY, fH), feval(c.fden, fX, fY, fH))
            return F(r[0]) if lower else F(r[1])
        # Lower bounds, as functions of the prism point (p, q, h); all gaps are affine in (p, q), all slopes are
        # constants (exact interval bounds over the prism):
        #   min H(h) - t_j*(0) >= min_a ( gapH_a(p,q) + h cH_a ),   cH_a = inf t_a'
        #   t_k*(0) - max L(h) >= min_b ( gapL_b(p,q) + h cL_b ),   cL_b = -sup t_b'
        # phi(p,q,h) := sum of the two mins is JOINTLY CONCAVE in (p,q,h).  Valid bounds on l(h) - l(0):
        #   f >= 0 on the face:  phi            (l(h) - l(0) >= f(h) - f(0))     or  -f(p,q)  (l(h) >= 0)
        #   f <= 0 on the face:  f(p,q) + phi   (l(h) >= f(h))                   or  0
        # Each option is concave or affine; one option is SELECTED per segment, so the total
        #   T(p,q,h) = G(p,q) - 1 + sum_i w_i sel_i(p,q,h)
        # is jointly concave on the prism and its minimum is attained at a vertex of polygon x {0, h0}.
        cH = [dbound(Hs[j], True) for j in range(len(Hs))]; cL = [-dbound(Ls[k], False) for k in range(len(Ls))]
        def phi(t, h):
            return min(hv[j][t] - hv[js][t] + h*cH[j] for j in range(len(Hs))) + min(lv[ks][t] - lv[k][t] + h*cL[k] for k in range(len(Ls)))
        pts = [(t, h) for t in nv for h in (peval(low, V[t][0], V[t][1]), peval(high, V[t][0], V[t][1]))]
        if max(fvals) > 0: opts = ([phi(t, h) for t, h in pts], [-fvals[t] for t, h in pts])
        else: opts = ([fvals[t] + phi(t, h) for t, h in pts], [F(0) for t, h in pts])
        cands.append((seg, [[w*v for v in o] for o in opts], [w*max(F(0), f) for f in fvals],
                      padd(flin(Hs[js]), pscale(-1, flin(Ls[ks]))), max(fvals) <= 0))
    Gmin = min(Gv)
    # option selection (any selection is valid; we look for one with min T >= 0): start from the larger sum,
    # then flip single segments while that raises the minimum over the prism vertices.
    base = [Gv[t] for t in range(len(V)) for h in (0, 1)]
    if area_m is not None:
        # area(h) - area(0) >= h * inf d(area)/dh : linear in h, added at the cell's vertices (v, low(v)), (v, high(v))
        am = F(area_m)
        base = [Gv[t] + am*(peval(low, V[t][0], V[t][1]) if hl == 0 else peval(high, V[t][0], V[t][1])) for t in range(len(V)) for hl in (0, 1)]
    sel = [max(range(2), key=lambda o: sum(c[1][o])) for c in cands]
    Tv = list(base)
    for c, o in zip(cands, sel):
        for n_, v in enumerate(c[1][o]): Tv[n_] += v
    for _ in range(3):
        improved = False
        for i, c in enumerate(cands):
            o = sel[i]; alt = [Tv[n_] - c[1][o][n_] + c[1][1-o][n_] for n_ in range(len(Tv))]
            if min(alt) > min(Tv): Tv = alt; sel[i] = 1 - o; improved = True
        if not improved: break
    lam = [F(1) if o == 1 else F(0) for o in sel]     # weight of option 1 (convex combinations are valid too)
    if min(Tv) < 0 and cands:
        # any convex combination lam*opt1 + (1-lam)*opt0 of the two concave/affine options is a valid concave lower
        # bound (it is <= the max of the two).  Find lam by a float LP, then VERIFY exactly with rational lam.
        try:
            import numpy as np
            from scipy.optimize import linprog
            nv_ = len(Tv); n = len(cands)
            d = np.array([[float(c[1][1][k] - c[1][0][k]) for c in cands] for k in range(nv_)])
            b0 = np.array([float(base[k] + sum(c[1][0][k] for c in cands)) for k in range(nv_)])
            # max t  s.t.  b0 + d lam >= t  ->  -d lam + t <= b0
            A = np.hstack([-d, np.ones((nv_, 1))]); cvec = np.zeros(n+1); cvec[-1] = -1
            res = linprog(cvec, A_ub=A, b_ub=b0, bounds=[(0, 1)]*n + [(None, None)], method='highs')
            if res.status == 0:
                lam2 = [min(F(1), max(F(0), F(x).limit_denominator(10**9))) for x in res.x[:n]]
                Tv2 = [base[k] + sum(lam2[i]*c[1][1][k] + (1-lam2[i])*c[1][0][k] for i, c in enumerate(cands)) for k in range(nv_)]
                if min(Tv2) > min(Tv): Tv, lam = Tv2, lam2
        except ImportError: pass
    if DEBUG is not None:
        for c, l in zip(cands, lam): DEBUG.append((c[0], [l*a + (1-l)*b for a, b in zip(c[1][1], c[1][0])], c[2], float(l)))
    Tmin = min(Tv)
    info = dict(Gmin=Gmin, Tmin=Tmin, val=Tmin, cands=cands, lam=lam, Tv=Tv)
    if Gmin >= 0 and Tmin >= 0: return ('ok', info)
    return ('fail', 'bound', info)

def run(segs, chart, polys, h0, maxcells=200000, minarea=None, log=None, progress=None):
    """certify the union of polys x [0, h0]; cells are slabs (Q, low, high).  Returns (stats, failed cells)."""
    allX = [v[0] for P_ in polys for v in P_]; allY = [v[1] for P_ in polys for v in P_]
    big = [(min(allX), min(allY)), (max(allX), min(allY)), (max(allX), max(allY)), (min(allX), max(allY))]
    near = [s_ for s_ in segs if seg_reach(s_, chart, big, h0)]
    segcons = [(s_, build_constraints(s_, chart)) for s_ in near]
    todo = [(Q, P(0), chart.get('high', P(h0)), 0) for Q in polys]; ok = 0; fails = []; ncell = 0; worst = None; nsplit = dict(face=0, kink=0, bis=0, hbis=0)
    while todo:
        Q, lo, hi, depth = todo.pop(); ncell += 1
        if progress and ncell % progress == 0: print('   cells', ncell, 'ok', ok, 'todo', len(todo), 'fails', len(fails), nsplit, flush=True)
        if ncell > maxcells: fails.append((Q, 'maxcells', {})); continue
        r = analyse(segcons, chart, Q, h0, low=lo, high=hi)
        if r[0] == 'ok':
            ok += 1
            if worst is None or r[1]['val'] < worst[0]: worst = (r[1]['val'], Q)
            continue
        if r[0] == 'split':
            parts = split_poly(Q, r[1])
            if len(parts) < 2: fails.append((Q, 'split-degenerate', {})); continue
            nsplit['face'] += 1; todo += [(Pp, lo, hi, depth) for Pp in parts]; continue
        info = r[2] if len(r) > 2 else {}
        if r[1] == 'bound' and info.get('cands'):
            # kink split: for a segment that is outside the square on the face (f <= 0) and enters for h > 0, split
            # the slab by the plane h = -f(p,q)/s where its first-order gain crosses zero (s = its gain slope at h0).
            best = None
            for seg, opts, gv, flinp, outside in info['cands']:
                # option 0 is phi (inside, f >= 0) or f + phi (outside, f <= 0); the true bound is max(opt0, opt1),
                # whose kink is where f + slope*h = 0, i.e. on the plane h = -f/slope (slope from opt0 along h)
                fv = [peval(flinp, v[0], v[1]) for v in Q]
                if max(fv) == min(fv): continue
                t = min(range(len(Q)), key=lambda k: abs(fv[k]))
                hl, hh = peval(lo, *Q[t]), peval(hi, *Q[t])
                if hh <= hl: continue
                slope = (opts[0][2*t+1] - opts[0][2*t]) / (seg[2]*(hh - hl))
                if slope == 0 or (outside and slope < 0) or (not outside and slope > 0): continue
                pv = [-f/slope for f in fv]                      # plane height at the vertices
                pl_ = pscale(-1/slope, flinp)
                if pl_ == lo or pl_ == hi: continue              # this slab was already cut by that plane
                if not any(peval(lo, *Q[k]) < pv[k] < peval(hi, *Q[k]) for k in range(len(Q))) and \
                   not (min(pv[k] - peval(lo, *Q[k]) for k in range(len(Q))) < 0 < max(pv[k] - peval(lo, *Q[k]) for k in range(len(Q)))): continue
                d = sum(abs(a - b) for a, b in zip(opts[0], opts[1]))
                if best is None or d > best[0]: best = (d, seg, flinp, slope)
            if best is not None:
                d, seg, flinp, slope = best
                if True:
                    plane = pscale(-1/slope, flinp)
                    pieces = []
                    for A in split_poly(Q, padd(plane, pscale(-1, lo))):
                        for B in split_poly(A, padd(plane, pscale(-1, hi))):
                            pieces.append(B)
                    new = []
                    for B in pieces:
                        c = (sum(v[0] for v in B)/len(B), sum(v[1] for v in B)/len(B))
                        pl, l_, h_ = peval(plane, *c), peval(lo, *c), peval(hi, *c)
                        if l_ < pl < h_: new += [(B, lo, plane, depth+1), (B, plane, hi, depth+1)]
                        else: new.append((B, lo, hi, depth+1))
                    if len(new) >= 2:
                        nsplit['kink'] += 1; todo += new; continue
        (xa, xb), (ya, yb) = bbox(Q)
        if minarea is not None and max(xb-xa, yb-ya) < F(1, 2**30):
            fails.append((Q, r[1], {k: v for k, v in info.items() if k in ('Gmin', 'Tmin', 'val')}, lo, hi)); continue
        lin = padd(P(1, (1, 0, 0)), P(-(xa+xb)/2)) if xb-xa >= yb-ya else padd(P(1, (0, 1, 0)), P(-(ya+yb)/2))
        parts = split_poly(Q, lin)
        if len(parts) < 2: fails.append((Q, r[1], {})); continue
        nsplit['bis'] += 1; todo += [(Pp, lo, hi, depth+1) for Pp in parts]
    return dict(ok=ok, cells=ncell, fails=len(fails), segs=len(near), worst=worst, splits=nsplit), fails

# ---- the full chart system (TIGHT_TILE_LEMMA.md, section 0.A), version 2: the scale variable is always h = u ----
# Near a base line s = s_b, small quantities delta = cx - d0, t = cy - s_b, u = |tan(theta/2)| > 0.  With t0 = dmax = K u0
# the neighbourhood N = {0 < u <= u0, |t| <= t0, |delta| <= dmax} is covered by (case analysis on |delta| vs K u and
# |t| vs K u):
#   C_u  : |delta| <= Ku, |t| <= Ku   face (kappa = delta/u, sigma = t/u) in [-K,K]^2,  h = u in [0, u0]
#   W_t  : |delta| <= Ku < |t|         face (kappa, tau = |t|) in [-K,K] x [0,t0],      h = u in [0, tau/K]
#   W_d  : |t| <= Ku < |delta|         face (sigma, eps = |delta|) in [-K,K] x [0,dmax], h = u in [0, eps/K]
#   W_td : Ku < |delta|, Ku < |t|      face (tau, eps) in [0,t0] x [0,dmax],             h = u in [0, min(tau,eps)/K]
#          (split into tau <= eps, wedge on tau, and eps <= tau, wedge on eps)
# Strips s in [s1, s2] (|s - s_b| >= t0 for every base line):
#   S_u  : |delta| <= Ku   face (kappa, s) in [-K,K] x [s1,s2],   h = u in [0, u0]
#   S_d  : |delta| >  Ku   face (s, eps) in [s1,s2] x [0,dmax],   h = u in [0, eps/K]
# In every chart the pose is affine in h with coefficients affine in the face coordinates, tan(theta/2) = sign*h.
def chart_u(d0, sb, sign):
    return dict(cx0=P(d0), cx1=P(1, (1, 0, 0)), cy0=P(sb), cy1=P(1, (0, 1, 0)), a=P(sign), pos='')
def chart_wt(d0, sb, sign, ts, K):
    return dict(cx0=P(d0), cx1=P(1, (1, 0, 0)), cy0=padd(P(sb), P(ts, (0, 1, 0))), cy1=P(0), a=P(sign), pos='',
                high=P(1/F(K), (0, 1, 0)), wedge=(1, 1/F(K)))
def chart_wd(d0, sb, sign, ds, K):
    return dict(cx0=padd(P(d0), P(ds, (0, 1, 0))), cx1=P(0), cy0=P(sb), cy1=P(1, (1, 0, 0)), a=P(sign), pos='',
                high=P(1/F(K), (0, 1, 0)), wedge=(1, 1/F(K)))
def chart_wtd(d0, sb, sign, ts, ds, K, on):
    """face (p, q) = (tau, eps); on = 0: region tau <= eps, h <= tau/K;  on = 1: region eps <= tau, h <= eps/K"""
    e = (1, 0, 0) if on == 0 else (0, 1, 0)
    return dict(cx0=padd(P(d0), P(ds, (0, 1, 0))), cx1=P(0), cy0=padd(P(sb), P(ts, (1, 0, 0))), cy1=P(0), a=P(sign), pos='',
                high=P(1/F(K), e), wedge=(on, 1/F(K)), apex=True)
def chart_su(d0, sign):
    return dict(cx0=P(d0), cx1=P(1, (1, 0, 0)), cy0=P(1, (0, 1, 0)), cy1=P(0), a=P(sign), pos='')
def chart_sd(d0, sign, ds, K):
    return dict(cx0=padd(P(d0), P(ds, (0, 1, 0))), cx1=P(0), cy0=P(1, (1, 0, 0)), cy1=P(0), a=P(sign), pos='',
                high=P(1/F(K), (0, 1, 0)), wedge=(1, 1/F(K)))

def charts_line(d0, sb, sign, K, u0):
    K = F(K); t0 = dmax = K*u0; r = []
    sq = lambda a, b, c, d: [(a, c), (b, c), (b, d), (a, d)]
    r.append(('C_u', chart_u(d0, sb, sign), sq(-K, K, -K, K), u0))
    for ts in (1, -1): r.append((f'W_t t{ts:+d}', chart_wt(d0, sb, sign, ts, K), sq(-K, K, F(0), t0), u0))
    for ds in (1, -1): r.append((f'W_d d{ds:+d}', chart_wd(d0, sb, sign, ds, K), sq(-K, K, F(0), dmax), u0))
    for ts in (1, -1):
        for ds in (1, -1):
            r.append((f'W_td t{ts:+d} d{ds:+d} a', chart_wtd(d0, sb, sign, ts, ds, K, 0), [(F(0), F(0)), (t0, t0), (F(0), dmax)], u0))
            r.append((f'W_td t{ts:+d} d{ds:+d} b', chart_wtd(d0, sb, sign, ts, ds, K, 1), [(F(0), F(0)), (t0, F(0)), (t0, t0)], u0))
    return r
def charts_strip(d0, s1, s2, sign, K, u0):
    K = F(K); dmax = K*u0; sq = lambda a, b, c, d: [(a, c), (b, c), (b, d), (a, d)]
    r = [('S_u', chart_su(d0, sign), sq(-K, K, s1, s2), u0)]
    for ds in (1, -1): r.append((f'S_d d{ds:+d}', chart_sd(d0, sign, ds, K), sq(s1, s2, F(0), dmax), u0))
    return r


# ---- third-level zoom at a corner (kappa*, sigma*) of the C_u face where two events coincide ----
# Covers the box {|kappa - kappa*| <= rho, |sigma - sigma*| <= rho, 0 <= h <= h0} of the C_u chart by
#   CORNER : max(|kappa-kappa*|, |sigma-sigma*|) <= M h:  pose centre (d0 + h(kappa* + a h), sb + h(sigma* + b h)),
#            face (a, b) in [-M, M]^2, h in [0, h0];
#   4 SECTORS: h <= max(|kappa-kappa*|, |sigma-sigma*|)/M, split by which coordinate is larger and its sign; in each,
#            local coordinates (p, q) = signed offsets with the dominant one >= |other|, slab h <= p/M.
# (rho <= M h0 so that the sector slabs stay inside h <= h0.)
def chart_corner(d0, sb, sign, ks, ss):
    return dict(cx0=P(d0), cx1=padd(P(ks), P(1, (1, 0, 1))), cy0=P(sb), cy1=padd(P(ss), P(1, (0, 1, 1))), a=P(sign), pos='')
def chart_sector(d0, sb, sign, ks, ss, which, M):
    """which in 'EWNS': dominant offset +kappa, -kappa, +sigma, -sigma; local p = dominant offset >= 0, q = other"""
    M = F(M)
    if which == 'E': cx1, cy1 = padd(P(ks), P(1, (1, 0, 0))), padd(P(ss), P(1, (0, 1, 0)))
    if which == 'W': cx1, cy1 = padd(P(ks), P(-1, (1, 0, 0))), padd(P(ss), P(1, (0, 1, 0)))
    if which == 'N': cx1, cy1 = padd(P(ks), P(1, (0, 1, 0))), padd(P(ss), P(1, (1, 0, 0)))
    if which == 'S': cx1, cy1 = padd(P(ks), P(1, (0, 1, 0))), padd(P(ss), P(-1, (1, 0, 0)))
    return dict(cx0=P(d0), cx1=cx1, cy0=P(sb), cy1=cy1, a=P(sign), pos='', high=P(1/M, (1, 0, 0)), wedge=(0, 1/M), apex2=True)
def charts_corner(d0, sb, sign, ks, ss, rho, M, h0):
    M = F(M); r = [('CORNER', chart_corner(d0, sb, sign, ks, ss), [(-M, -M), (M, -M), (M, M), (-M, M)], h0)]
    tri = [(F(0), F(0)), (rho, -rho), (rho, rho)]
    for wch in 'EWNS': r.append((f'SECTOR {wch}', chart_sector(d0, sb, sign, ks, ss, wch, M), tri, h0))
    return r

# sector charts, version 2 (scale = distance to the corner): sector E is {kappa - kappa* = r in [0, rho],
# |sigma - sigma*| <= r, 0 <= h <= r/M}; coordinates (w, v, r) with sigma - sigma* = w r, h = v r: a box
# w in [-1,1], v in [0, 1/M], r in [0, rho].  Pose: centre (d0 + v r (kappa* + r), sb + v r (sigma* + w r)), tan = sign v r.
def chart_sector2(d0, sb, sign, ks, ss, which):
    vr = P(1, (0, 1, 0))                       # v (times the scale r = engine h)
    if which in 'EW':
        e = 1 if which == 'E' else -1
        cx1 = padd(P(ks, (0, 1, 0)), P(e, (0, 1, 1)))          # v*ks + e*v*r
        cy1 = padd(P(ss, (0, 1, 0)), P(1, (1, 1, 1)))          # v*ss + w*v*r
    else:
        e = 1 if which == 'N' else -1
        cx1 = padd(P(ks, (0, 1, 0)), P(1, (1, 1, 1)))
        cy1 = padd(P(ss, (0, 1, 0)), P(e, (0, 1, 1)))
    return dict(cx0=P(d0), cx1=cx1, cy0=P(sb), cy1=cy1, a=P(sign, (0, 1, 0)), pos='q')
def charts_corner2(d0, sb, sign, ks, ss, rho, M, h0):
    M = F(M); r = [('CORNER', chart_corner(d0, sb, sign, ks, ss), [(-M, -M), (M, -M), (M, M), (-M, M)], h0)]
    box = [(F(-1), F(0)), (F(1), F(0)), (F(1), 1/M), (F(-1), 1/M)]
    for wch in 'EWNS': r.append((f'SECTOR2 {wch}', chart_sector2(d0, sb, sign, ks, ss, wch), box, rho))
    return r

# ---- corner charts, version 3: the same four-zone blow-up as at a base line, one level down ----
# Around a C_u corner (kappa*, sigma*), with X = |kappa - kappa*|, Y = |sigma - sigma*| (both <= rho) and h <= h0:
#   CORNER : X <= M h, Y <= M h       face (a, b) in [-M,M]^2,  centre offsets h(kappa* + a h), h(sigma* + b h)
#   KFAR   : X > M h, Y <= M h        face (p = X, b) in [0,rho] x [-M,M], offsets h(kappa* +- p), h(sigma* + b h), h <= p/M
#   SFAR   : Y > M h, X <= M h        face (a, p = Y) in [-M,M] x [0,rho], offsets h(kappa* + a h), h(sigma* +- p), h <= p/M
#   BOTH   : X > M h, Y > M h         face (X, Y) in [0,rho]^2 split by X <= Y (h <= X/M) and Y <= X (h <= Y/M)
# These cover the box exactly (case analysis on X vs Mh and Y vs Mh); rho <= M h0 keeps every slab inside h <= h0.
def charts_corner3(d0, sb, sign, ks, ss, rho, M, h0):
    M = F(M); r = []; sq = lambda a, b, c, d: [(a, c), (b, c), (b, d), (a, d)]
    base = dict(cx0=P(d0), cy0=P(sb), a=P(sign), pos='')
    r.append(('CORNER', dict(base, cx1=padd(P(ks), P(1, (1, 0, 1))), cy1=padd(P(ss), P(1, (0, 1, 1)))), sq(-M, M, -M, M), h0))
    for e in (1, -1):
        r.append((f'KFAR {e:+d}', dict(base, cx1=padd(P(ks), P(e, (1, 0, 0))), cy1=padd(P(ss), P(1, (0, 1, 1))),
                                       high=P(1/M, (1, 0, 0)), wedge=(0, 1/M)), sq(F(0), rho, -M, M), h0))
        r.append((f'SFAR {e:+d}', dict(base, cx1=padd(P(ks), P(1, (1, 0, 1))), cy1=padd(P(ss), P(e, (0, 1, 0))),
                                       high=P(1/M, (0, 1, 0)), wedge=(1, 1/M)), sq(-M, M, F(0), rho), h0))
    for ex in (1, -1):
        for ey in (1, -1):
            c1 = dict(base, cx1=padd(P(ks), P(ex, (1, 0, 0))), cy1=padd(P(ss), P(ey, (0, 1, 0))))
            r.append((f'BOTH {ex:+d}{ey:+d} a', dict(c1, high=P(1/M, (1, 0, 0)), wedge=(0, 1/M), apex=True), [(F(0), F(0)), (rho, rho), (F(0), rho)], h0))
            r.append((f'BOTH {ex:+d}{ey:+d} b', dict(c1, high=P(1/M, (0, 1, 0)), wedge=(1, 1/M), apex=True), [(F(0), F(0)), (rho, F(0)), (rho, rho)], h0))
    return r


# ---- corners on the edge q = 0 of a wedge chart (h <= q/K, e.g. W_t, W_d): points (p*, 0) where two events coincide ----
# Box |p - p*| <= rho, 0 <= q <= rho of the chart, with X = |p - p*|:
#   WCORNER : X <= M h        p = p* + a h,  face (a, q) in [-M, M] x [0, rho],  h <= q/K (wedge on q)
#   WFAR +-a: X > M h, X <= q (M = K): face (X, q), p = p* +- X, h <= X/M   (wedge on X, apex X <= q)
#   WFAR +-b: X > M h, q <= X        : face (X, q), p = p* +- X, h <= q/K   (wedge on q, apex q <= X)
# Cover: X <= M h  ->  WCORNER;  else h < X/M and h <= q/K, split by X <= q or q <= X (with M = K).
def _subst_p(poly, ps, mode):
    """p -> ps + p*h (mode 'c') or p -> ps + e*p (mode e = +1/-1) in a polynomial in (p, q, h)"""
    lin = padd(P(ps), P(1, (1, 0, 1))) if mode == 'c' else padd(P(ps), P(mode, (1, 0, 0)))
    out = {}
    for (i, j, k), c in poly.items():
        term = P(c, (0, j, k))
        for _ in range(i): term = pmul(term, lin)
        out = padd(out, term)
    return out
def charts_wcorner(chart, ps, rho, M, h0):
    M = F(M); K = 1/chart['wedge'][1]
    if not (chart['wedge'][0] == 1 and M == K): raise ValueError('charts_wcorner needs wedge index 1 and M == K')
    keys = ('cx0', 'cx1', 'cy0', 'cy1', 'a')
    r = []
    c = {k: _subst_p(chart[k], ps, 'c') for k in keys}
    r.append(('WCORNER', dict(c, pos='', high=P(1/K, (0, 1, 0)), wedge=(1, 1/K)), [(-M, F(0)), (M, F(0)), (M, rho), (-M, rho)], h0))
    for e in (1, -1):
        c = {k: _subst_p(chart[k], ps, e) for k in keys}
        r.append((f'WFAR {e:+d} a', dict(c, pos='', high=P(1/M, (1, 0, 0)), wedge=(0, 1/M), apex=True), [(F(0), F(0)), (rho, rho), (F(0), rho)], h0))
        r.append((f'WFAR {e:+d} b', dict(c, pos='', high=P(1/K, (0, 1, 0)), wedge=(1, 1/K), apex=True), [(F(0), F(0)), (rho, F(0)), (rho, rho)], h0))
    return r


# ---- generic face substitution and the "ray zoom" inside a wedge-corner zone ----
def _subst(poly, sp, sq):
    """substitute p -> sp(p', q', h), q -> sq(p', q', h) in a polynomial in (p, q, h)"""
    out = {}
    for (i, j, k), c in poly.items():
        term = P(c, (0, 0, k))
        for _ in range(i): term = pmul(term, sp)
        for _ in range(j): term = pmul(term, sq)
        out = padd(out, term)
    return out
def _rechart(chart, sp, sq, **extra):
    """new chart with face (p', q'): full pose polynomials, re-split into c0 + h c1"""
    cx = padd(chart['cx0'], pmul(Hv, chart['cx1'])); cy = padd(chart['cy0'], pmul(Hv, chart['cy1']))
    cx, cy = _subst(cx, sp, sq), _subst(cy, sp, sq); a = _subst(chart['a'], sp, sq)
    def split(pl):
        c0 = {e: v for e, v in pl.items() if e[2] == 0}; c1 = {(e[0], e[1], e[2]-1): v for e, v in pl.items() if e[2] > 0}
        return c0, c1
    cx0, cx1 = split(cx); cy0, cy1 = split(cy)
    if not all(e[2] == 0 for e in a): raise ValueError('tilt coefficient must not depend on h')
    d = dict(cx0=cx0, cx1=cx1, cy0=cy0, cy1=cy1, a=a, pos='')
    d.update(extra); return d
def charts_rayzoom(chart, lam, rho, Mr=F(1)):
    """Inside a wedge chart with face (X, q), region 0 <= q <= X, h <= q/K (e.g. WFAR b), zoom along the face line
    q = lam X through the apex.  Zones (D = q - lam X):
      NEAR : |D| <= Mr h        q = lam X + z h, face (X, z) in [0, rho] x [-Mr, Mr];  slab h <= lam X/(K - Mr)  (a superset
                                of the exact h <= q/K when |z| <= Mr: proving more poses is allowed)
      ABOVE: D > Mr h, D <= (1-lam) X   face (X, D): slab h <= min(D/Mr, (lam X + D)/K), split where the two agree
      BELOW: -D = E > Mr h, E <= lam X  face (X, E): slab h <= min(E/Mr, (lam X - E)/K), split likewise
    Every zone has h <= c X; the wedge tests use h = v X (and, where the other face variable is <= X, x_o = w X)."""
    K = 1/chart['wedge'][1]; lam = F(lam); Mr = F(Mr); r = []
    X = P(1, (1, 0, 0)); Z = P(1, (0, 1, 0))
    # NEAR
    sq = padd(pscale(lam, X), pmul(Z, Hv))
    r.append(('RAY NEAR', _rechart(chart, X, sq, high=pscale(lam/(K-Mr), X), wedge=(0, lam/(K-Mr))),
              [(F(0), -Mr), (rho, -Mr), (rho, Mr), (F(0), Mr)]))
    # ABOVE 1: D = q - lam X in [0, Dc X], slab h <= D/Mr (wedge on D, apex D <= X)
    sq = padd(pscale(lam, X), Z); Dc = Mr*lam/(K-Mr)            # D = Dc X is where D/Mr = (lam X + D)/K
    r.append(('RAY ABOVE 1', _rechart(chart, X, sq, high=pscale(1/Mr, Z), wedge=(1, 1/Mr), apex=True, apex_w=Dc),
              [(F(0), F(0)), (rho, F(0)), (rho, Dc*rho)]))
    # ABOVE 2: q in [(lam + Dc) X, X], slab h <= q/K (original coordinates; wedge on q, apex q <= X)
    r.append(('RAY ABOVE 2', _rechart(chart, X, Z, high=pscale(1/K, Z), wedge=(1, 1/K), apex=True),
              [(F(0), F(0)), (rho, (lam+Dc)*rho), (rho, rho)]))
    # BELOW 1: E = lam X - q in [0, Ec X], slab h <= E/Mr (wedge on E, apex E <= X)
    sq = padd(pscale(lam, X), pscale(-1, Z)); Ec = Mr*lam/(K+Mr)
    r.append(('RAY BELOW 1', _rechart(chart, X, sq, high=pscale(1/Mr, Z), wedge=(1, 1/Mr), apex=True, apex_w=Ec),
              [(F(0), F(0)), (rho, F(0)), (rho, Ec*rho)]))
    # BELOW 2: q in [0, (lam - Ec) X], slab h <= q/K (wedge on q, apex q <= X)
    r.append(('RAY BELOW 2', _rechart(chart, X, Z, high=pscale(1/K, Z), wedge=(1, 1/K), apex=True),
              [(F(0), F(0)), (rho, F(0)), (rho, (lam-Ec)*rho)]))
    return r
