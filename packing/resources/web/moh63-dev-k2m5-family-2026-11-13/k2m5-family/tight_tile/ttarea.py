"""Lebesgue (area) term of the box cover for ttbox: density rho on the rectangle U = [X0, X1] x [Y0, Y1].

Face value (h = 0, theta = 0): rho * Ax(cx0) * Ay(cy0) with Ax(c) = |[c - 1/2, c + 1/2] cap [X0, X1]| (clamped, piecewise
affine; its kinks are face lines where the polygon is split).  If both factors vary on a polygon, the McCormick lower
bound Ax*Ay >= Ax_min*Ay + Ax*Ay_min - Ax_min*Ay_min (affine) is used (valid because (Ax-Ax_min)(Ay-Ay_min) >= 0).

Derivative (h > 0): d/dh area(Q cap U) = integral over (boundary of Q) cap U of v.n (U does not move), where for the
edge with body normal e and body point b(t) (t in [-1/2, 1/2]) the integrand is c'.n + theta' * (J b).e, linear in t.
The part of each edge inside U is t in [t_lo, t_hi], cut by the 4 lines of U: each gives t*A <= B with A, B
polynomials in (p, q, h) (times N = 1 + u^2).  All quantities are enclosed by outward-rounded float intervals over
the cell's box; then  A(h) - A(0) >= h * inf (d/dh area)  (A is Lipschitz in h; mean-value inequality)."""
from fractions import Fraction as F
from ttpoly import P, padd, pscale, pmul, pdiff_h, fpoly, feval, fdiv, fmul, fI, peval
import ttbox as _T
import math
_dn = lambda x: math.nextafter(x, -math.inf); _up = lambda x: math.nextafter(x, math.inf)
Hv = P(1, (0, 0, 1))

def iadd(a, b): return (_dn(a[0]+b[0]), _up(a[1]+b[1]))
def ineg(a): return (-a[1], -a[0])
def isq(a):
    lo, hi = a
    if lo >= 0: return (_dn(lo*lo), _up(hi*hi))
    if hi <= 0: return (_dn(hi*hi), _up(lo*lo))
    return (0.0, _up(max(lo*lo, hi*hi)))
def imax(a, b): return (max(a[0], b[0]), max(a[1], b[1]))
def imin(a, b): return (min(a[0], b[0]), min(a[1], b[1]))

class AreaTerm:
    def __init__(self, chart, U):
        self.X0, self.Y0, self.X1, self.Y1, self.rho = U
        cx = padd(chart['cx0'], pmul(Hv, chart['cx1'])); cy = padd(chart['cy0'], pmul(Hv, chart['cy1']))
        u = pmul(Hv, chart['a']); u2 = pmul(u, u)
        N = padd(P(1), u2); NC = padd(P(1), pscale(-1, u2)); NS = pscale(2, u)
        self.cx0, self.cy0 = chart['cx0'], chart['cy0']
        # c' = d/dh (c0 + h c1) and theta' = 2a/(1 + a^2 h^2); c'.n uses n = (C, S) etc = (NC, NS)/N
        dcx = pdiff_h(cx); dcy = pdiff_h(cy)
        self.fth_num = fpoly(pscale(2, chart['a'])); self.fth_den = fpoly(N)          # theta' = 2a/N  (N = 1 + a^2 h^2)
        self.edges = []
        # body normal e, body point b(t), (J b).e = k t ;  world normal n = R e ;  edge point = c + R b(t)
        for e, bfun, k in (((1, 0), lambda t: (F(1, 2), t), -1), ((-1, 0), lambda t: (-F(1, 2), t), 1),
                           ((0, 1), lambda t: (t, F(1, 2)), 1), ((0, -1), lambda t: (t, -F(1, 2)), -1)):
            # R (b0 + t b1) with b = b0 + t b1;  R(x, y) = (C x - S y, S x + C y)  -> times N: (NC x - NS y, NS x + NC y)
            b0 = bfun(F(0)); b1 = (bfun(F(1))[0] - b0[0], bfun(F(1))[1] - b0[1])
            Rx = lambda v: padd(pscale(v[0], NC), pscale(-v[1], NS)); Ry = lambda v: padd(pscale(v[0], NS), pscale(v[1], NC))
            X0n, X1n = padd(pmul(cx, N), Rx(b0)), Rx(b1)       # N * x(t) = X0n + t X1n
            Y0n, Y1n = padd(pmul(cy, N), Ry(b0)), Ry(b1)
            cons = []
            for (z0, z1, lim, sg) in ((X0n, X1n, self.X0, -1), (X0n, X1n, self.X1, 1), (Y0n, Y1n, self.Y0, -1), (Y0n, Y1n, self.Y1, 1)):
                # sg*(z0 + t z1) <= sg*lim*N   ->  t*(sg z1) <= sg*(lim N - z0)
                A = pscale(sg, z1); B = pscale(sg, padd(pscale(lim, N), pscale(-1, z0)))
                if A and B:
                    # divide out the common power of h (h > 0 on the region; same rule as for segments)
                    m = _T.pmindeg([A, B]); m = (m[0] if 'p' in chart.get('pos', '') else 0, m[1] if 'q' in chart.get('pos', '') else 0, m[2])
                    A = _T.pdivmono(A, m); B = _T.pdivmono(B, m)
                Bp, Bm = padd(B, pscale(F(1, 2), A)), padd(B, pscale(-F(1, 2), A))      # B +- A/2
                wd = {}
                if chart.get('wedge'):
                    wi = chart['wedge'][0]
                    wd['w'] = (fpoly(_T.wedge_subst(Bp, wi)), fpoly(_T.wedge_subst(Bm, wi)))
                    if chart.get('apex'): wd['x'] = (fpoly(_T.apex_subst(_T.wedge_subst(Bp, wi), wi)), fpoly(_T.apex_subst(_T.wedge_subst(Bm, wi), wi)))
                    if chart.get('apex2'): wd['y'] = (fpoly(_T.apex2_subst(_T.wedge_subst(Bp, wi), wi)), fpoly(_T.apex2_subst(_T.wedge_subst(Bm, wi), wi)))
                cons.append((fpoly(A), fpoly(B), wd))
            nx, ny = Rx(e), Ry(e)                                # N * n
            cn = padd(pmul(dcx, nx), pmul(dcy, ny))              # N * c'.n
            self.edges.append(dict(cons=cons, fcn=fpoly(cn), k=k))
        self.fN = fpoly(N); self.wedge = chart.get('wedge'); self.apex_w = chart.get('apex_w', 1)

    def face_vertex(self, v):
        cx0 = peval(self.cx0, v[0], v[1]); cy0 = peval(self.cy0, v[0], v[1])
        ax = max(F(0), min(cx0 + F(1, 2), self.X1) - max(cx0 - F(1, 2), self.X0))
        ay = max(F(0), min(cy0 + F(1, 2), self.Y1) - max(cy0 - F(1, 2), self.Y0))
        return ax, ay
    def kink_lines(self):
        """affine face lines where Ax or Ay changes slope"""
        L = []
        for c0, lims in ((self.cx0, (self.X0, self.X1)), (self.cy0, (self.Y0, self.Y1))):
            for lim in lims:
                for off in (F(1, 2), -F(1, 2)): L.append(padd(c0, P(off - lim)))   # c0 + off - lim = 0
        return L

    def deriv_lower(self, fX, fY, fH):
        """lower bound of d/dh area over the box (float intervals); None if the edge structure cannot be bounded"""
        Nn = feval(self.fN, fX, fY, fH)
        th = fdiv(feval(self.fth_num, fX, fY, fH), Nn)
        tot = (0.0, 0.0)
        for ed in self.edges:
            lo, hi = (-0.5, -0.5), (0.5, 0.5); empty = False
            for fA, fB, wd in ed['cons']:
                a = feval(fA, fX, fY, fH); b = feval(fB, fX, fY, fH)
                if a[0] > 0: hi = imin(hi, fdiv(b, a))
                elif a[1] < 0: lo = imax(lo, fdiv(b, a))
                else:
                    m = 0.5*max(abs(a[0]), abs(a[1]))
                    if b[0] >= m: continue                       # satisfied for every t in [-1/2, 1/2]
                    if b[1] < -m: empty = True; break            # violated for every t
                    # wedge charts: B +- A/2 after the exact substitution h = v x_w (and apex substitutions)
                    done = False
                    if self.wedge:
                        Vv = fI((F(0), self.wedge[1])); wi = self.wedge[0]
                        trials = [('w', fX, fY)]
                        if 'x' in wd:
                            aw = fI((F(0), F(self.apex_w)))   # x_w = w x_o, w in [0, apex_w] (chart's apex range)
                            trials.append(('x',) + ((aw, fY) if wi == 0 else (fX, aw)))
                        if 'y' in wd: trials.append(('y',) + ((fX, (-1.0, 1.0)) if wi == 0 else ((-1.0, 1.0), fY)))
                        for key, BX, BY in trials:
                            bp = feval(wd[key][0], BX, BY, Vv); bm = feval(wd[key][1], BX, BY, Vv)
                            if bp[0] >= 0 and bm[0] >= 0: done = True; break
                            if bp[1] < 0 and bm[1] < 0: empty = True; done = True; break
                    if empty: break
                    if done: continue
                    return None
            if empty or hi[1] <= lo[0]: continue                  # edge outside U on the whole cell
            cn = fdiv(feval(ed['fcn'], fX, fY, fH), Nn)           # c'.n
            ln = (_dn(hi[0] - lo[1]), _up(hi[1] - lo[0]))
            sq = (_dn(isq(hi)[0] - isq(lo)[1]), _up(isq(hi)[1] - isq(lo)[0]))
            val = iadd(fmul(ln, cn), fmul(fmul(th, (0.5*ed['k'], 0.5*ed['k'])), sq))
            if not (hi[0] >= lo[1]): val = (min(val[0], 0.0), max(val[1], 0.0))   # the edge may miss U
            tot = iadd(tot, val)
        if self.rho != 1: raise ValueError('rho != 1: use outward-rounded multiplication')
        return tot[0]
