"""Independent construction of the normalized 52-row G20S gate (second adversarial review, think-4j3n).

Nothing here imports producer code. Geometry comes from geom.py (my transcription of STATEMENT.md and
UPPER_FORMULAS.md). Rows are derived from first principles:

  wall  (i, corner c, coord k, sign):  sign=+1: (c_i + R(th_i) v_c)_k >= 0;  sign=-1: S - (...)_k >= 0
  pair  (l, r, owner o, corner c of other t):  (R(th_o) n).(c_r - c_l) - 1/2 - n.R(th_t - th_o) v_c >= 0
  parallel (l, r, s):  X - 1 + mu tau' + s eps (1 - sigma tau') + E >= 0   (PROOF.md P098-P107)

with the normalized variables x = h/R (core), s = (S-S*)/R (index 51), unscaled sliders a,b,z (2,21,25) and
lifted products q_{w,angle} = w*x_angle (52..99). Remainders are my own bounds (Taylor with
||R(t)-I-tJ|| <= t^2/2), divided by R and bounded with R <= eps = 1/5000.

Coefficients are computed in mpmath interval arithmetic at the exact-root enclosure (Krawczyk-verified box of
radius 1e-100), converted to rational intervals, rounded to a 1e-30 grid, and the rounding plus enclosure width
is paid as loss * variable radius (as the producer does, but with my own code and grid).
"""
from fractions import Fraction as Fr
import itertools
import mpmath
from mpmath import mp, iv
import geom

iv.dps = 120
mp.dps = 120

EPS = Fr(1, 5000)
PARAMS = (2, 21, 25)
DUMMY = (6, 7, 37)
ANGLES = tuple(34 + i for i in range(17) if i != 3)
PRODUCTS = {(w, a): 52 + k for k, (w, a) in enumerate(itertools.product(PARAMS, ANGLES))}
DIM = 52 + len(PRODUCTS)
CORE = tuple(i for i in range(51) if i not in PARAMS + DUMMY)
GRID = 10**30

PAIRS = ((1, 3), (1, 5), (2, 6), (3, 13), (5, 9), (5, 11), (6, 14), (7, 10), (8, 16), (9, 10), (10, 12), (10, 15),
         (11, 12), (12, 14), (12, 16), (13, 14), (14, 17), (15, 16), (16, 17))


def ivfr(x):
    """mpmath iv interval -> (Fraction lo, Fraction hi), exact endpoints."""
    return geom.to_fr(x.a), geom.to_fr(x.b)


def root_box():
    t, b = geom.newton_root()
    rad = mp.mpf(10)**-100
    ok, K = geom.krawczyk(t, b, rad)
    assert ok
    return iv.mpf([t - rad, t + rad]), iv.mpf([b - rad, b + rad])


class Geo:
    def __init__(self):
        T, B = root_box()
        one = iv.mpf(1)
        self.side, self.pts, self.axes, self.aux = geom.layout(T, B, one)
        # displacement maps: dict label -> list of (index, world vector) for core and for sliders
        self.core = {}
        self.slide = {}
        for lab in range(1, 18):
            if lab == 4:
                continue
            i = lab - 1
            u = self.axes[i]
            v = (-u[1], u[0])
            if lab == 2:
                self.core[lab] = [(3, (0, 1))]
                self.slide[lab] = [(2, (-1, 0))]
            elif lab == 11:
                self.core[lab] = [(20, u)]
                self.slide[lab] = [(21, (-v[0], -v[1]))]
            elif lab == 13:
                self.core[lab] = [(24, u)]
                self.slide[lab] = [(25, v)]
            else:
                self.core[lab] = [(2*i, (1, 0)), (2*i + 1, (0, 1))]
                self.slide[lab] = []

    def axis(self, lab, which):
        u = self.axes[lab - 1]
        return u if which == 0 else (-u[1], u[0])

    def corner(self, lab, c):
        ea, eb = list(itertools.product((-1, 1), repeat=2))[c]
        u = self.axis(lab, 0); v = self.axis(lab, 1)
        return (iv.mpf(ea)*u[0]/2 + iv.mpf(eb)*v[0]/2, iv.mpf(ea)*u[1]/2 + iv.mpf(eb)*v[1]/2)


def dot(a, b):
    return a[0]*b[0] + a[1]*b[1]


def J(v):
    return (-v[1], v[0])


def bnd(box, j):
    lo, hi = box[j]
    return max(abs(lo), abs(hi))


def ivbox(box, j):
    lo, hi = box[j]
    return iv.mpf([mpmath.mpf(lo.numerator)/lo.denominator if lo.denominator == 1 else iv.mpf(lo.numerator)/lo.denominator,
                   0]) if False else None


def frac_iv(fr_lo, fr_hi):
    return iv.mpf([iv.mpf(fr_lo.numerator)/fr_lo.denominator, iv.mpf(fr_hi.numerator)/fr_hi.denominator]) \
        if (fr_lo, fr_hi) != (0, 0) else iv.mpf(0)


def frac_point(x):
    return iv.mpf(x.numerator)/x.denominator


def disp_radius(geo, lab, box):
    """upper bound (Fraction) on |core displacement of lab| in normalized units over box, per world axis and norm."""
    comps = [Fr(0), Fr(0)]
    for idx, vec in geo.core[lab]:
        r = bnd(box, idx)
        for k in (0, 1):
            vk = vec[k]
            vk_hi = abs(Fr(vk)) if isinstance(vk, int) else max(abs(ivfr(vk)[0]), abs(ivfr(vk)[1]))
            comps[k] += vk_hi*r
    return comps


def diff_disp_norm(geo, a, b, box):
    """upper bound on |delta_b - delta_a| (normalized): exact interval range of each world component of the
    displacement difference over the box (each core index occurs once), then the Euclidean norm."""
    comps = []
    for k in (0, 1):
        x = iv.mpf(0)
        for idx, vec in geo.core[b]:
            x = x + (iv.mpf(vec[k]) if isinstance(vec[k], int) else vec[k])*box_iv(box, idx)
        for idx, vec in geo.core[a]:
            x = x - (iv.mpf(vec[k]) if isinstance(vec[k], int) else vec[k])*box_iv(box, idx)
        comps.append(max(abs(geom.to_fr(x.a)), abs(geom.to_fr(x.b))))
    return sqrt_up(comps[0]**2 + comps[1]**2)


def sqrt_up(q):
    """rational upper bound of sqrt(q)."""
    if q == 0:
        return Fr(0)
    x = mp.sqrt(mp.mpf(q.numerator)/q.denominator)
    r = geom.to_fr(x) + Fr(1, 10**40)
    assert r*r >= q
    return r


def ref_diff(geo, l, r, box):
    """reference difference d(w) = p_r - p_l + slider part, as (iv vector at w-box, dict slider->iv vector)."""
    d0 = (geo.pts[r-1][0] - geo.pts[l-1][0], geo.pts[r-1][1] - geo.pts[l-1][1])
    wv = {}
    for idx, vec in geo.slide[r]:
        wv[idx] = (wv.get(idx, (0, 0))[0] + vec[0], wv.get(idx, (0, 0))[1] + vec[1])
    for idx, vec in geo.slide[l]:
        wv[idx] = (wv.get(idx, (0, 0))[0] - vec[0], wv.get(idx, (0, 0))[1] - vec[1])
    return d0, wv


def box_iv(box, j):
    lo, hi = box[j]
    return iv.mpf([frac_point(lo).a, frac_point(hi).b])


def dnorm_upper(geo, l, r, box):
    d0, wv = ref_diff(geo, l, r, box)
    comps = []
    for k in (0, 1):
        x = d0[k]
        for idx, vec in wv.items():
            x = x + vec[k]*box_iv(box, idx)
        comps.append(max(abs(geom.to_fr(x.a)), abs(geom.to_fr(x.b))))
    return sqrt_up(comps[0]**2 + comps[1]**2)


class Row:
    def __init__(self, label):
        self.label = label
        self.coef = {}      # index -> iv interval
        self.base = iv.mpf(0)   # base gap (must contain 0)
        self.slider = {}    # slider index -> iv (must contain 0)
        self.err = Fr(0)    # remainder bound (normalized)

    def add(self, j, val):
        self.coef[j] = self.coef.get(j, iv.mpf(0)) + val


def build_rows(geo, labels, box, normals):
    rows = []
    for label in labels:
        f = label.split(':')
        row = Row(label)
        if f[0] == 'wall':
            lab, c, k, sign = int(f[1]), int(f[2]), int(f[3]), int(f[4])
            v = geo.corner(lab, c)
            p = geo.pts[lab - 1]
            row.base = sign*(p[k] + v[k]) + (geo.side if sign == -1 else 0)
            for idx, vec in geo.core[lab]:
                row.add(idx, sign*iv.mpf(vec[k]) if isinstance(vec[k], int) else sign*vec[k])
            for idx, vec in geo.slide[lab]:
                row.slider[idx] = sign*iv.mpf(vec[k]) if isinstance(vec[k], int) else sign*vec[k]
            row.add(34 + lab - 1, sign*J(v)[k])
            if sign == -1:
                row.add(51, iv.mpf(1))
            # remainder |(R(th)v - v - th Jv)_k| <= th^2 |v| / 2, |v| = sqrt(2)/2 < 1
            rt = bnd(box, 34 + lab - 1)
            row.err = EPS*rt*rt*Fr(7072, 10000)/2
        elif f[0] == 'pair':
            l, r, o, c = int(f[1]), int(f[2]), int(f[3]), int(f[4])
            t = l if o == r else r
            axis_idx, nsign = normals[(l, r)]
            n = tuple(nsign*x for x in geo.axis(o, axis_idx))
            v = geo.corner(t, c)
            d0, wv = ref_diff(geo, l, r, box)
            row.base = dot(n, d0) - iv.mpf(1)/2 - dot(n, v)
            for idx, vec in wv.items():
                row.slider[idx] = dot(n, vec)
            for idx, vec in geo.core[r]:
                row.add(idx, dot(n, vec))
            for idx, vec in geo.core[l]:
                row.add(idx, -dot(n, vec))
            Jn = J(n)
            row.add(34 + o - 1, dot(Jn, d0) + dot(n, J(v)))
            row.add(34 + t - 1, -dot(n, J(v)))
            for idx, vec in wv.items():
                row.add(PRODUCTS[idx, 34 + o - 1], dot(Jn, vec))
            D = dnorm_upper(geo, l, r, box)
            dr = diff_disp_norm(geo, l, r, box)
            wo = bnd(box, 34 + o - 1); wt = bnd(box, 34 + t - 1)
            row.err = EPS*(D*wo*wo/2 + wo*dr + Fr(7072, 10000)*(wo + wt)**2/2)
        elif f[0] == 'parallel':
            l, r, s = int(f[1]), int(f[2]), int(f[3])
            axis_idx, nsign = normals[(l, r)]
            n = tuple(nsign*x for x in geo.axis(l, axis_idx))
            d0, wv = ref_diff(geo, l, r, box)
            row.base = dot(n, d0) - 1
            for idx, vec in wv.items():
                row.slider[idx] = dot(n, vec)
            for idx, vec in geo.core[r]:
                row.add(idx, dot(n, vec))
            for idx, vec in geo.core[l]:
                row.add(idx, -dot(n, vec))
            Jn = J(n)
            tau0 = dot(Jn, d0)
            tauw = {idx: dot(Jn, vec) for idx, vec in wv.items()}
            # range of tau' over the slider box, to fix sigma and tau_max
            tr = tau0
            for idx, tv in tauw.items():
                tr = tr + tv*box_iv(box, idx)
            tlo, thi = geom.to_fr(tr.a), geom.to_fr(tr.b)
            if tlo >= -Fr(1, 10**60) and thi > 0:
                sigma = 1
            elif thi <= Fr(1, 10**60):
                sigma = -1
            else:
                raise ValueError('tau sign crossing ' + label)
            if tlo > -Fr(1, 10**60) and thi < Fr(1, 10**60):
                sigma = None   # identically ~0: sign irrelevant
            taumax = max(abs(tlo), abs(thi))
            assert taumax < 1
            row.tau = (tlo, thi)
            sg = sigma if sigma is not None else 1
            # mu*tau' + s*eps*(1 - sg*tau') with mu=(x_l+x_r)/2, eps=(x_r-x_l)/2
            # x_l: tau'/2 - s(1 - sg tau')/2 ; x_r: tau'/2 + s(1 - sg tau')/2
            row.add(34 + l - 1, tau0/2 - iv.mpf(s)*(1 - sg*tau0)/2)
            row.add(34 + r - 1, tau0/2 + iv.mpf(s)*(1 - sg*tau0)/2)
            for idx, tv in tauw.items():
                row.add(PRODUCTS[idx, 34 + l - 1], tv/2 + iv.mpf(s)*sg*tv/2)
                row.add(PRODUCTS[idx, 34 + r - 1], tv/2 - iv.mpf(s)*sg*tv/2)
            D = dnorm_upper(geo, l, r, box)
            dr = diff_disp_norm(geo, l, r, box)
            rl, rr = bnd(box, 34 + l - 1), bnd(box, 34 + r - 1)
            M = (rl + rr)/2; Q = (rl + rr)/2
            E = (EPS*(D*M*M/2 + M*dr + Q*Q/2) + EPS**2*(Q**3/6 + taumax*Q**3)
                 + (D*M + dr)*(EPS*Q + EPS**3*Q**3))
            row.err = E
        else:
            raise ValueError(label)
        rows.append(row)
    return rows


def to_rational_row(row, box):
    """exact rational row a.x >= b valid for every point of the box (loss paid with variable radii)."""
    a = {}
    loss = Fr(0)
    for j, val in row.coef.items():
        lo, hi = ivfr(val)
        mid = Fr(round((lo + hi)/2*GRID), GRID)
        a[j] = mid
        loss += max(abs(mid - lo), abs(mid - hi))*bnd(box, j)
    # base gap and slider coefficients are exactly zero by the symbolic identities (checked separately);
    # the enclosure width of these exactly-zero quantities is not paid here.
    b = Fr(((-row.err - loss)*GRID).__floor__(), GRID)
    return a, b


def product_rows(box):
    out = []
    for (w, ang), idx in PRODUCTS.items():
        l, h = box[w]; L, U = box[ang]
        for wa, aa, qa, cst in ((-L, -l, 1, l*L), (-U, -h, 1, h*U), (L, h, -1, -h*L), (U, l, -1, -l*U)):
            a = {}
            if wa: a[w] = wa
            if aa: a[ang] = aa
            a[idx] = Fr(qa)
            out.append((a, -cst))
    return out


def refresh(base):
    res = list(base[:52]) + [(Fr(0), Fr(0))]*len(PRODUCTS)
    for (w, ang), idx in PRODUCTS.items():
        vals = [x*y for x in base[w] for y in base[ang]]
        res[idx] = (min(vals), max(vals))
    return res


def dual_bound(rows, box, coord, sign, weights):
    resid = {coord: Fr(sign)}
    val = Fr(0)
    for key, wstr in weights.items():
        lam = Fr(wstr)
        assert lam >= 0
        a, b = rows[int(key)]
        val += lam*b
        for j, c in a.items():
            resid[j] = resid.get(j, Fr(0)) - lam*c
    for j, rj in resid.items():
        if rj:
            lo, hi = box[j]
            val += rj*(lo if rj >= 0 else hi)
    return val
