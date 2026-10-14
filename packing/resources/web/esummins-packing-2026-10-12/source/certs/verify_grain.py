#!/usr/bin/env python3
"""verify_grain.py -- exact-rational checker for `grain-certificate-v1` files (A76).

TCB-small: Python stdlib only (fractions, json, sys).  Every accept decision is exact:
intervals are Fraction pairs outward-rounded to the dyadic grid 2^-PREC (rounding only
widens), and the trigonometry is RATIONAL in t = tan(theta/2):

    cosT(t) = (1 - t^2)/(1 + t^2),   sinT(t) = 2t/(1 + t^2),
    dcosT   = -4t/(1+t^2)^2,          dsinT   = 2(1-t^2)/(1+t^2)^2,

with interval enclosures by MONOTONICITY (elementary calculus, proved in the docstrings of
the four *_iv functions).  No floats, no mpmath, no Taylor series.

Configuration z in R^34: z[3i], z[3i+1], z[3i+2] = (cx_i, cy_i, t_i) of square i (i = 0..10),
z[33] = s (container side).  Corner k of square i: q_k = c_i + R(t_i) h_k with
h in {(-1/2,-1/2), (1/2,-1/2), (1/2,1/2), (-1/2,1/2)}, R(t) the rotation by theta = 2 arctan t.
Row functions (all polynomial/rational in z; gradients computed exactly):
  wall  q_k(i)_x, q_k(i)_y, s - q_k(i)_x, s - q_k(i)_y           (containment)
  edge  n_e(t_j) . (q_k(i) - c_j) - 1/2                            (corner k of i beyond edge e of j;
                                                                    n_e = outward normal of edge e)
  dist  |c_i - c_j|^2 - 1
  teq   t_i - t_j
  pinx/piny  cx_i - (alpha + beta s) / cy_i - (alpha + beta s);  pint  t_i
  es    (value 0, gradient e_s)                                    (the side direction)

The certificate names a rational centre z0 (an enclosure of Trump's contact configuration
z-hat: A22 krawczyk_cert.json converted to t = tan(theta/2) with the exact upright structure of
A22 notes sect. 3 -- the checker verifies the centre residuals of the Trump rows), a box
B = z0 +- (rc on centres, rt on tilts, rs on the side), a row universe, and three kinds of
claims, each re-verified from scratch:

 [PA]  LOCAL COMPLETENESS (Lemma G-R, docs/proofs/grain_discharge.md): the checker itself
       generates EVERY corner-wall row (11*4*4 = 176) and EVERY corner-edge row
       (11*10*4*4 = 1760).  A row is "possibly a contact on B" iff its value enclosure over B
       contains 0 and (for edge rows) the corner's tangential coordinate along the edge has an
       enclosure meeting [-1/2, 1/2] (a corner can touch an edge only on the edge SEGMENT).
       PASS iff every candidate row that is possibly a contact on B is listed in `pa.rows`.
       Hence every packing in B has all its contacts (corner-wall and corner-edge incidences)
       among the listed rows -- BY CONSTRUCTION, not by search.
 [K]   RIGID GRAIN (Krawczyk): for a listed 34-row system F (rows vanishing at z0 up to the
       residual bound) and a rational matrix Y:  K(B) = -Y F(z0) + (I - Y [J](B)) (B - z0) lies in
       the open interior of B - z0.  Then (Krawczyk/Moore/Neumaier) F has EXACTLY ONE zero in B.
       Since Trump's z-hat lies in B (|z-hat - z0| <= 1e-50, A22) and all Trump rows and pin
       rows vanish at z-hat exactly (A22 sect. 3), that zero IS z-hat: any configuration in B at
       which the listed rows are all active is Trump's packing.
 [D1]  DRAIN-FLEX (Lemma DF): for a listed independent row set A and a rational 34 x (|A|+1)
       matrix Y:  || M(B) Y - I ||_inf < 1 where M(z) = [grad g_a(z) (a in A); e_s]  (row-sum
       norm of the interval matrix, entries by magnitude).  Then M(z) Y is nonsingular for every
       z in B, so M(z) has full row rank |A|+1: the rows of J_A(z) are independent and e_s is
       NOT in their span, for every z in B.  Consequence (grain_discharge.md, Lemma DF): a
       packing in B whose active contact set has independent part A is not a minimiser of the
       container side (a feasible curve through it strictly decreases s).

Interval Krawczyk and the row-sum-norm nonsingularity test are standard (Neumaier, Interval
Methods for Systems of Equations, Thm 5.1.7 / Cor. 4.1.3); the MVT form used here allows a
different mean point per row because [J](B) encloses every row gradient over all of B.

Corruption gates (each MUST make the checker fail):
    z0       perturb one centre coordinate by 1e-3      (residuals / contraction)
    Y        negate one row (K) / column (D1) of the first preconditioner matrix
    row      tamper one row of the first K system (edge index +1)
    box      quadruple the box radii without re-deriving
    pa-drop  delete the last PA row (completeness must fail)

Usage:  python verify_grain.py cert.json [--corrupt {z0,Y,row,box,pa-drop}] [--quiet]
Exit 0 = PASS, 1 = FAIL, 2 = malformed.
"""
import json
import sys
from fractions import Fraction

PREC = 330
GRID = 1 << PREC
NV = 34
S_IDX = 33
HALF = [(Fraction(-1, 2), Fraction(-1, 2)), (Fraction(1, 2), Fraction(-1, 2)),
        (Fraction(1, 2), Fraction(1, 2)), (Fraction(-1, 2), Fraction(1, 2))]
NHAT = [(0, -1), (1, 0), (0, 1), (-1, 0)]
QUIET = False


def rdown(x):
    return Fraction((x.numerator * GRID) // x.denominator, GRID)


def rup(x):
    return Fraction(-((-x.numerator * GRID) // x.denominator), GRID)


class IV(object):
    __slots__ = ('lo', 'hi')

    def __init__(self, lo, hi, rnd=True):
        if rnd:
            lo, hi = rdown(lo), rup(hi)
        if lo > hi:
            raise ValueError('inverted interval')
        self.lo, self.hi = lo, hi

    @staticmethod
    def point(x):
        return IV(x, x)

    def __add__(self, b):
        if not isinstance(b, IV):
            b = IV.point(Fraction(b))
        return IV(self.lo + b.lo, self.hi + b.hi)

    __radd__ = __add__

    def __sub__(self, b):
        if not isinstance(b, IV):
            b = IV.point(Fraction(b))
        return IV(self.lo - b.hi, self.hi - b.lo)

    def __rsub__(self, b):
        return IV.point(Fraction(b)) - self

    def __neg__(self):
        return IV(-self.hi, -self.lo, rnd=False)

    def __mul__(self, b):
        if not isinstance(b, IV):
            b = IV.point(Fraction(b))
        ps = (self.lo * b.lo, self.lo * b.hi, self.hi * b.lo, self.hi * b.hi)
        return IV(min(ps), max(ps))

    __rmul__ = __mul__

    def mag(self):
        return max(abs(self.lo), abs(self.hi))


IZERO = IV.point(Fraction(0))
IONE = IV.point(Fraction(1))


# ---------------------------------------------------------------- rational trig
def cosT_pt(t):
    return (1 - t * t) / (1 + t * t)


def sinT_pt(t):
    return 2 * t / (1 + t * t)


def dcosT_pt(t):
    u = 1 + t * t
    return -4 * t / (u * u)


def dsinT_pt(t):
    u = 1 + t * t
    return 2 * (1 - t * t) / (u * u)


def _absmax(a, b):
    return max(abs(a), abs(b))


def _absmin(a, b):
    return Fraction(0) if a <= 0 <= b else min(abs(a), abs(b))


def cosT_iv(v):
    """cosT is even and strictly decreasing in |t| (derivative -4t/(1+t^2)^2 < 0 for t > 0)."""
    return IV(cosT_pt(_absmax(v.lo, v.hi)), cosT_pt(_absmin(v.lo, v.hi)))


def sinT_iv(v):
    """sinT is strictly increasing on [-1, 1] (derivative 2(1-t^2)/(1+t^2)^2 > 0 for |t| < 1)."""
    if not (-1 <= v.lo and v.hi <= 1):
        raise ValueError('tilt interval outside [-1,1]')
    return IV(sinT_pt(v.lo), sinT_pt(v.hi))


def dcosT_iv(v):
    """dcosT(t) = -4t/(1+t^2)^2 has derivative -4(1-3t^2)/(1+t^2)^3 < 0 on |t| < 1/sqrt3:
    strictly decreasing there, so [dcosT(hi), dcosT(lo)] encloses it."""
    if not (3 * v.lo * v.lo < 1 and 3 * v.hi * v.hi < 1):
        raise ValueError('tilt interval outside |t| < 1/sqrt3')
    return IV(dcosT_pt(v.hi), dcosT_pt(v.lo))


def dsinT_iv(v):
    """dsinT(t) = 2(1-t^2)/(1+t^2)^2 has derivative -4t(3-t^2)/(1+t^2)^3, of sign -sign(t) for
    |t| < sqrt3: even and decreasing in |t|, so [dsinT(max|t|), dsinT(min|t|)] encloses it."""
    if not (abs(v.lo) < 1 and abs(v.hi) < 1):
        raise ValueError('tilt interval outside (-1,1)')
    return IV(dsinT_pt(_absmax(v.lo, v.hi)), dsinT_pt(_absmin(v.lo, v.hi)))


def trig(t):
    if isinstance(t, IV):
        return cosT_iv(t), sinT_iv(t), dcosT_iv(t), dsinT_iv(t)
    return cosT_pt(t), sinT_pt(t), dcosT_pt(t), dsinT_pt(t)


# ---------------------------------------------------------------- rows
def corner_pos(z, i, k):
    hx, hy = HALF[k]
    co, si, _, _ = trig(z[3 * i + 2])
    return z[3 * i] + (hx * co - hy * si), z[3 * i + 1] + (hx * si + hy * co)


def dcorner_dt(z, i, k):
    hx, hy = HALF[k]
    _, _, dc, ds = trig(z[3 * i + 2])
    return hx * dc - hy * ds, hx * ds + hy * dc


def normal(z, j, e):
    nhx, nhy = NHAT[e]
    co, si, _, _ = trig(z[3 * j + 2])
    return nhx * co - nhy * si, nhx * si + nhy * co


def dnormal_dt(z, j, e):
    nhx, nhy = NHAT[e]
    _, _, dc, ds = trig(z[3 * j + 2])
    return nhx * dc - nhy * ds, nhx * ds + nhy * dc


def eval_row(z, c):
    k = c['kind']
    if k == 'wall':
        qx, qy = corner_pos(z, c['i'], c['corner'])
        w = c['wall']
        if w == 'x=0':
            return qx
        if w == 'y=0':
            return qy
        if w == 'x=s':
            return z[S_IDX] - qx
        if w == 'y=s':
            return z[S_IDX] - qy
        raise ValueError('wall ' + str(w))
    if k == 'edge':
        i, j = c['i'], c['j']
        qx, qy = corner_pos(z, i, c['corner'])
        nx, ny = normal(z, j, c['edge'])
        return nx * (qx - z[3 * j]) + ny * (qy - z[3 * j + 1]) - Fraction(1, 2)
    if k == 'dist':
        i, j = c['i'], c['j']
        dx = z[3 * i] - z[3 * j]
        dy = z[3 * i + 1] - z[3 * j + 1]
        return dx * dx + dy * dy - 1
    if k == 'teq':
        return z[3 * c['i'] + 2] - z[3 * c['j'] + 2]
    if k == 'pinx':
        return z[3 * c['i']] - (Fraction(c['alpha']) + Fraction(c['beta']) * z[S_IDX])
    if k == 'piny':
        return z[3 * c['i'] + 1] - (Fraction(c['alpha']) + Fraction(c['beta']) * z[S_IDX])
    if k == 'pint':
        return z[3 * c['i'] + 2]
    if k == 'es':
        return IZERO if isinstance(z[0], IV) else Fraction(0)
    raise ValueError('row kind ' + str(k))


def grad_row(z, c):
    k = c['kind']
    one = IONE if isinstance(z[0], IV) else Fraction(1)
    g = {}
    if k == 'wall':
        i = c['i']
        dx, dy = dcorner_dt(z, i, c['corner'])
        w = c['wall']
        if w == 'x=0':
            g[3 * i] = one
            g[3 * i + 2] = dx
        elif w == 'y=0':
            g[3 * i + 1] = one
            g[3 * i + 2] = dy
        elif w == 'x=s':
            g[3 * i] = -one
            g[3 * i + 2] = -dx
            g[S_IDX] = one
        elif w == 'y=s':
            g[3 * i + 1] = -one
            g[3 * i + 2] = -dy
            g[S_IDX] = one
        else:
            raise ValueError('wall ' + str(w))
        return g
    if k == 'edge':
        i, j = c['i'], c['j']
        nx, ny = normal(z, j, c['edge'])
        qx, qy = corner_pos(z, i, c['corner'])
        wx, wy = qx - z[3 * j], qy - z[3 * j + 1]
        dhx, dhy = dcorner_dt(z, i, c['corner'])
        dnx, dny = dnormal_dt(z, j, c['edge'])
        g[3 * i] = nx
        g[3 * i + 1] = ny
        g[3 * j] = -nx
        g[3 * j + 1] = -ny
        g[3 * i + 2] = nx * dhx + ny * dhy
        g[3 * j + 2] = dnx * wx + dny * wy
        return g
    if k == 'dist':
        i, j = c['i'], c['j']
        dx = z[3 * i] - z[3 * j]
        dy = z[3 * i + 1] - z[3 * j + 1]
        g[3 * i] = 2 * dx
        g[3 * i + 1] = 2 * dy
        g[3 * j] = -2 * dx
        g[3 * j + 1] = -2 * dy
        return g
    if k == 'teq':
        g[3 * c['i'] + 2] = one
        g[3 * c['j'] + 2] = -one
        return g
    if k in ('pinx', 'piny'):
        g[3 * c['i'] + (0 if k == 'pinx' else 1)] = one
        b = Fraction(c['beta'])
        if b != 0:
            g[S_IDX] = -b * one
        return g
    if k == 'pint':
        g[3 * c['i'] + 2] = one
        return g
    if k == 'es':
        g[S_IDX] = one
        return g
    raise ValueError('row kind ' + str(k))


def tangential(z, c):
    """tangential coordinate of the corner along the owner edge (edge rows)."""
    i, j = c['i'], c['j']
    qx, qy = corner_pos(z, i, c['corner'])
    nx, ny = normal(z, j, c['edge'])
    wx, wy = qx - z[3 * j], qy - z[3 * j + 1]
    return -ny * wx + nx * wy


def row_name(c):
    k = c['kind']
    if k == 'wall':
        return 'W%dc%d[%s]' % (c['i'], c['corner'], c['wall'])
    if k == 'edge':
        return 'E%dc%d-%de%d' % (c['i'], c['corner'], c['j'], c['edge'])
    if k == 'dist':
        return 'D%d-%d' % (c['i'], c['j'])
    if k == 'teq':
        return 'T%d-%d' % (c['i'], c['j'])
    if k == 'pinx':
        return 'PX%d' % c['i']
    if k == 'piny':
        return 'PY%d' % c['i']
    if k == 'pint':
        return 'PT%d' % c['i']
    if k == 'es':
        return 'ES'
    raise ValueError(k)


def all_candidate_rows():
    out = []
    for i in range(11):
        for k in range(4):
            for w in ('x=0', 'y=0', 'x=s', 'y=s'):
                out.append({'kind': 'wall', 'i': i, 'corner': k, 'wall': w})
    for i in range(11):
        for j in range(11):
            if i == j:
                continue
            for k in range(4):
                for e in range(4):
                    out.append({'kind': 'edge', 'i': i, 'corner': k, 'j': j, 'edge': e})
    return out


# ---------------------------------------------------------------- checks
class Check(object):
    def __init__(self):
        self.fails = []
        self.n = 0

    def __call__(self, name, ok, detail=''):
        self.n += 1
        if not QUIET or not ok:
            print('  [%s] %s %s' % ('PASS' if ok else 'FAIL', name, detail))
        if not ok:
            self.fails.append(name)


def make_box(z0, rad):
    return [IV(x - r, x + r) for x, r in zip(z0, rad)]


def check_pa(cert, z0, B, ck):
    listed = set(cert['pa']['rows'])
    missing = []
    n_out = 0
    for c in all_candidate_rows():
        v = eval_row(B, c)
        if not (v.lo <= 0 <= v.hi):
            n_out += 1
            continue
        if c['kind'] == 'edge':
            tg = tangential(B, c)
            if tg.hi < Fraction(-1, 2) or tg.lo > Fraction(1, 2):
                n_out += 1
                continue
        if row_name(c) not in listed:
            missing.append(row_name(c))
    ck('PA local completeness', not missing,
       '%d candidate rows, %d certified non-contact on B, %d listed, missing=%s'
       % (176 + 1760, n_out, len(listed), missing[:6]))


def krawczyk_check(z0, B, rad, rows, Y, ck, tag):
    n = len(rows)
    if n != NV or len(Y) != NV or any(len(r) != NV for r in Y):
        ck('K %s shape' % tag, False, 'need 34 rows and a 34x34 Y')
        return
    zc = [IV.point(x) for x in z0]
    Fc = [eval_row(zc, c) for c in rows]
    Jrows = [grad_row(B, c) for c in rows]
    cols = [[] for _ in range(NV)]
    for ri, g in enumerate(Jrows):
        for j, v in g.items():
            cols[j].append((ri, v))
    ok = True
    worst = Fraction(0)
    for i in range(NV):
        Yi = Y[i]
        acc = IZERO
        for k in range(n):
            if Yi[k] != 0:
                acc = acc + Yi[k] * Fc[k]
        Ki = -acc
        for j in range(NV):
            ssum = IZERO
            for (rr, v) in cols[j]:
                if Yi[rr] != 0:
                    ssum = ssum + Yi[rr] * v
            m = IONE if i == j else IZERO
            Ki = Ki + (m - ssum) * IV(-rad[j], rad[j])
        worst = max(worst, Ki.mag() / rad[i])
        if not (Ki.lo > -rad[i] and Ki.hi < rad[i]):
            ok = False
    ck('K %s contraction' % tag, ok, 'max|K_i|/r_i = %.4f (need < 1)' % float(worst))


def d1_check(B, rows, Y, ck, tag):
    m = len(rows) + 1
    M = list(rows) + [{'kind': 'es'}]
    if len(Y) != NV or any(len(r) != m for r in Y):
        ck('D1 %s shape' % tag, False, 'need a 34 x %d Y' % m)
        return
    Jb = [grad_row(B, c) for c in M]
    ok = True
    worst = Fraction(0)
    for i in range(m):
        rowsum = Fraction(0)
        gi = Jb[i]
        for j in range(m):
            acc = IZERO
            for col, v in gi.items():
                if Y[col][j] != 0:
                    acc = acc + v * Y[col][j]
            rowsum += (acc - (IONE if i == j else IZERO)).mag()
        worst = max(worst, rowsum)
        if rowsum >= 1:
            ok = False
    ck('D1 %s nonsingularity' % tag, ok, '||M(B)Y - I||_inf = %.4f (need < 1), |A| = %d'
       % (float(worst), m - 1))


def verify(cert, corrupt=None):
    ck = Check()
    if cert.get('format') != 'grain-certificate-v1':
        print('malformed: format')
        return 2
    z0 = [Fraction(x) for x in cert['z0']]
    if len(z0) != NV:
        print('malformed: z0')
        return 2
    rad = [Fraction(x) for x in cert['box']['radii']]
    if len(rad) != NV or any(r <= 0 for r in rad):
        print('malformed: box')
        return 2
    rows = cert['rows']
    if corrupt == 'z0':
        z0[20] = z0[20] + Fraction(1, 1000)
    if corrupt == 'box':
        rad = [4 * r for r in rad]
    if corrupt == 'pa-drop' and cert.get('pa'):
        cert['pa']['rows'] = cert['pa']['rows'][:-1]
    if corrupt == 'row' and cert.get('krawczyk'):
        for k in cert['krawczyk'][0]['rows']:
            if rows[k]['kind'] == 'edge':
                rows[k]['edge'] = (rows[k]['edge'] + 1) % 4
                break
    if corrupt == 'Y':
        if cert.get('krawczyk'):
            tgt = cert['krawczyk'][0]
            tgt['Y'][3] = [str(-Fraction(v)) for v in tgt['Y'][3]]        # negate a row of Y
        else:
            tgt = cert['d1'][0]
            for r in tgt['Y']:
                r[3] = str(-Fraction(r[3]))                                # negate a column of Y
    B = make_box(z0, rad)
    print('grain-certificate-v1: %s' % cert.get('description', ''))
    print('box radii: centres %s, tilts %s, side %s' % (rad[0], rad[2], rad[33]))
    # [G] centre residuals of the rows claimed active at z0
    act = cert.get('active_at_z0', [])
    zc = [IV.point(x) for x in z0]
    mx = Fraction(0)
    for k in act:
        mx = max(mx, eval_row(zc, rows[k]).mag())
    bound = Fraction(cert['claims']['centre_residual_max'])
    ck('G centre residuals', mx <= bound, 'max |g(z0)| = %.2e over %d rows (claim <= %.1e)'
       % (float(mx), len(act), float(bound)))
    # tilt domain sanity for the trig enclosures
    ok = all(3 * B[3 * i + 2].lo ** 2 < 1 and 3 * B[3 * i + 2].hi ** 2 < 1 for i in range(11))
    ck('T tilt domain |t| < 1/sqrt3 on B', ok)
    if cert.get('pa'):
        check_pa(cert, z0, B, ck)
    for kc in cert.get('krawczyk', []):
        Y = [[Fraction(v) for v in r] for r in kc['Y']]
        krawczyk_check(z0, B, rad, [rows[k] for k in kc['rows']], Y, ck, kc.get('id', '?'))
    for dc in cert.get('d1', []):
        Y = [[Fraction(v) for v in r] for r in dc['Y']]
        d1_check(B, [rows[k] for k in dc['rows']], Y, ck, dc.get('id', '?'))
    print('=> %s (%d checks%s)' % ('ALL CHECKS PASS' if not ck.fails else 'FAILURES: %s' % ck.fails,
                                  ck.n, '' if not corrupt else ', corruption %s' % corrupt))
    return 0 if not ck.fails else 1


def main():
    global QUIET
    argv = list(sys.argv[1:])
    corrupt = None
    if '--corrupt' in argv:
        i = argv.index('--corrupt')
        corrupt = argv[i + 1]
        del argv[i:i + 2]
    if '--quiet' in argv:
        QUIET = True
        argv.remove('--quiet')
    if not argv:
        print(__doc__)
        sys.exit(2)
    cert = json.load(open(argv[0]))
    if corrupt and corrupt not in ('z0', 'Y', 'row', 'box', 'pa-drop'):
        print('unknown corruption mode')
        sys.exit(2)
    rc = verify(cert, corrupt)
    if corrupt:
        print('corruption %s: %s' % (corrupt, 'OK (checker failed as required)' if rc else
                                     'PROBLEM: checker still passes!'))
        sys.exit(0 if rc else 2)
    sys.exit(rc)


if __name__ == '__main__':
    main()
