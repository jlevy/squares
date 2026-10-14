#!/usr/bin/env python3
"""verify_cidl.py -- exact checker for the (c-idl) saturated ideal-membership
certificate closing the identity s-hat_A22 = s-hat_octic (cidl-membership-v1).

TCB-small: Python stdlib only (fractions, json, sys).  Every decision is exact
rational arithmetic; no floats anywhere.

## What is being certified

A22 (attempts/A22-local-rigidity, notes.md headline items 1-3) proves there is a
unique contact configuration z-hat in the box N = box(z0, 5e-4), that it is a
packing at its own side s-hat_A22 := s(z-hat), and (item 2, via the second
Krawczyk system F~) that z-hat has the EXACT structure: squares 0..5 axis-
parallel with c0 = (1/2,1/2), c1 = (3/2,1/2), c2 = (S-1/2,1/2), c3 = (1/2,3/2),
c4 = (1/2, y4), c5 = (S-1/2,S-1/2), and the five tilted squares 6..10 sharing
EXACTLY one common angle theta.  Substituting that structure into the 38 curated
constraint rows (all of which vanish at z-hat, A22 section 3) and writing
t = tan(theta/2), cos = (1-t^2)/(1+t^2), sin = 2t/(1+t^2) (Weierstrass; exact at
z-hat since |theta-hat| < pi), each surviving row, multiplied by the positive
quantity (1+t^2), becomes a POLYNOMIAL G_j in the 13 variables

    t, y4, x6, y6, x7, y7, x8, y8, x9, y9, x10, y10, S

that VANISHES at the A22 point

    P-hat = (t-hat, cy4-hat, cx6-hat, ..., cy10-hat, s-hat_A22).

The 18 surviving rows collapse (flush pairs give rationally-proportional rows)
to the 13 distinct generators G_0..G_12 hard-coded below -- THE CHECKER BUILDS
THEM ITSELF from the A22 corner/edge conventions; the certificate cannot alter
them.

This checker verifies, EXACTLY over Q:

  [O] the certificate's octic is the canonical Trump octic
      x^8 - 20x^7 + 178x^6 - 842x^5 + 1923x^4 - 496x^3 - 6754x^2 + 12420x - 6865
      (the polynomial in TopLevel.lean's `trumpOctic` and
      certs/octic_root_isolation.json);
  [I] the polynomial identity in Q[t, y4, x6..y10, S]

          e(t) * Delta(t)^8 * octic(S)  =  sum_j q_j(t,S) * G_j ,

      with e, Delta univariate and the cofactors q_j bivariate in (t, S), all
      supplied by the certificate (h := e * Delta^8 is the saturation factor);
  [G] the sign gate: e and Delta have NO real root in [3/10, 2/5] (exact Sturm
      chains), hence h(t) != 0 for every t in [3/10, 2/5].

## What a PASS proves (composition)

For ANY real tuple P = (t, y4, x6..y10, S) with t in [3/10, 2/5] at which all
13 generators vanish, [I] gives e(t) Delta(t)^8 octic(S) = 0 and [G] gives
octic(S) = 0.  A22 supplies such a tuple, P-hat:
  * the generators vanish at P-hat (A22 exact structure, above);
  * t-hat = tan(theta-hat/2) is in [3/10, 2/5]: theta-hat is within 1e-50 of
    the A03 rational angle 0.70130710554614222... (A22 enclosure), so
    theta-hat/2 in [0.35, 0.351], and 0.3 < 0.35 <= x <= tan(x) and
    tan(x) <= x + x^3/(3(1-x^2)) <= 0.3672 < 0.4 on that range;
  * s-hat_A22 is within 1e-50 of the A03 rational side 3.87708359002281417...,
    hence s-hat_A22 lies in (3.877083, 3.877084).
Therefore octic(s-hat_A22) = 0 with s-hat_A22 in the isolating interval of
certs/octic_root_isolation.json, whose unique octic root there is s-hat_octic
(the SECOND of the octic's two real roots, the other lying in (-2,-1)): so

    s-hat_A22 = s-hat_octic         (TopLevel.lean axiom `shatA22_eq_shat`).

Exit 0 = PASS, 1 = FAIL, 2 = malformed certificate.

Usage:  python verify_cidl.py cidl_identity.json [--corrupt MODE]
  corruption gates (each must FAIL): qcoeff, e, rowspec, octic
"""
import json
import sys
from fractions import Fraction as F

# ---------------------------------------------------------------------------
# hard-coded geometry (A22 conventions: a22lib.py HALF / NHAT / eval_g)
# ---------------------------------------------------------------------------

HALF = [(F(-1, 2), F(-1, 2)), (F(1, 2), F(-1, 2)), (F(1, 2), F(1, 2)), (F(-1, 2), F(1, 2))]
NHAT = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # edge k joins corner k -> k+1

# variable order: exponent tuples over (t, y4, x6, y6, x7, y7, x8, y8, x9, y9, x10, y10, S)
VARS = ['t', 'y4', 'x6', 'y6', 'x7', 'y7', 'x8', 'y8', 'x9', 'y9', 'x10', 'y10', 'S']
NVAR = 13
IT, IY4, IS = 0, 1, 12


def vidx(name):
    return VARS.index(name)


# sparse polynomials: dict {exponent-tuple: Fraction}
def pzero():
    return {}


def pconst(c):
    return {(0,) * NVAR: F(c)} if c else {}


def pvar(i, c=1):
    e = [0] * NVAR
    e[i] = 1
    return {tuple(e): F(c)}


def padd(a, b):
    r = dict(a)
    for m, c in b.items():
        s = r.get(m, F(0)) + c
        if s:
            r[m] = s
        else:
            r.pop(m, None)
    return r


def pscale(a, c):
    c = F(c)
    if not c:
        return {}
    return {m: v * c for m, v in a.items()}


def pmul(a, b):
    r = {}
    for m1, c1 in a.items():
        for m2, c2 in b.items():
            m = tuple(x + y for x, y in zip(m1, m2))
            s = r.get(m, F(0)) + c1 * c2
            if s:
                r[m] = s
            else:
                r.pop(m, None)
    return r


# ---------------------------------------------------------------------------
# the 13 generators, built from first principles
# ---------------------------------------------------------------------------
# Pinned squares: (centre_x, centre_y) as polynomials; cos = 1, sin = 0.
# Tilted squares 6..10: centre (x_i, y_i) variables; the common angle enters via
#   C := 1 - t^2,  Sn := 2 t  (cos, sin scaled by W := 1 + t^2).
# Every corner coordinate is then (centre) + (rotation term)/W; each wall/edge
# row is multiplied by W (wall) or W (edge, one rotation) -- for edge rows both
# the corner of square i and the normal of square j carry a 1/W, so the row is
# multiplied by W once when only one of i, j is tilted and the products
# C*C, C*Sn, Sn*Sn are handled with W^2 for tilted-tilted rows, using
# C^2 + Sn^2 = W^2 exactly (a polynomial identity, no trig).
#
# Implementation: represent each square's frame as (cx, cy, cosP, sinP, w) where
# cosP/sinP/w are polynomials with cos = cosP/w exactly at the point; corners and
# normals are computed over the common denominator and each row is cleared by the
# EXACT power of w it carries.  We verify the clearing is exact (denominator-free)
# by construction: all arithmetic below is polynomial; 1/w never appears.

T = pvar(IT)
W = padd(pconst(1), pmul(T, T))          # 1 + t^2
Ct = padd(pconst(1), pscale(pmul(T, T), -1))  # 1 - t^2
Sn = pscale(T, 2)                          # 2 t
ONE = pconst(1)
S_ = pvar(IS)
Y4 = pvar(IY4)


def frame(i):
    """Return (cx, cy, c, s, w): centre and scaled cos/sin with denominator w."""
    half = F(1, 2)
    if i == 0:
        return (pconst(half), pconst(half), ONE, pzero(), ONE)
    if i == 1:
        return (pconst(F(3, 2)), pconst(half), ONE, pzero(), ONE)
    if i == 2:
        return (padd(S_, pconst(-half)), pconst(half), ONE, pzero(), ONE)
    if i == 3:
        return (pconst(half), pconst(F(3, 2)), ONE, pzero(), ONE)
    if i == 4:
        return (pconst(half), Y4, ONE, pzero(), ONE)
    if i == 5:
        return (padd(S_, pconst(-half)), padd(S_, pconst(-half)), ONE, pzero(), ONE)
    # tilted
    return (pvar(vidx('x%d' % i)), pvar(vidx('y%d' % i)), Ct, Sn, W)


def corner_scaled(i, k):
    """Corner position as (num_x, num_y, w): corner = c_i + R(theta) HALF[k],
    returned as ((cx*w + rot_x), (cy*w + rot_y), w) so corner = num/w."""
    cx, cy, c, s, w = frame(i)
    hx, hy = HALF[k]
    rx = padd(pscale(c, hx), pscale(s, -hy))
    ry = padd(pscale(s, hx), pscale(c, hy))
    nx = padd(pmul(cx, w), rx)
    ny = padd(pmul(cy, w), ry)
    return nx, ny, w


def row_wall(i, k, wall):
    """g = corner coordinate (or S - it), cleared by w: returns w*g."""
    nx, ny, w = corner_scaled(i, k)
    if wall == 'x=0':
        return nx
    if wall == 'y=0':
        return ny
    if wall == 'x=s':
        return padd(pmul(S_, w), pscale(nx, -1))
    if wall == 'y=s':
        return padd(pmul(S_, w), pscale(ny, -1))
    raise ValueError(wall)


def row_edge(i, k, j, e):
    """g = n.(q - c_j) - 1/2 with n = R(theta_j) NHAT[e]; cleared by w_i * w_j."""
    qx, qy, wi = corner_scaled(i, k)          # corner = (qx, qy)/wi
    cjx, cjy, cj, sj, wj = frame(j)
    nhx, nhy = NHAT[e]
    nx = padd(pscale(cj, nhx), pscale(sj, -nhy))   # n * wj
    ny = padd(pscale(sj, nhx), pscale(cj, nhy))
    # w_i*w_j * g = n*wj . (q*wi - c_j*wi)  ... careful:
    # g = (n/wj).((q_num/wi) - c_j) - 1/2
    # wi*wj*g = n_num.(q_num - c_j*wi) - wi*wj/2
    dx = padd(qx, pscale(pmul(cjx, wi), -1))
    dy = padd(qy, pscale(pmul(cjy, wi), -1))
    r = padd(pmul(nx, dx), pmul(ny, dy))
    return padd(r, pscale(pmul(wi, wj), F(-1, 2)))


# the 13 distinct reduced rows (A69 derive.py; flush pairs collapse exactly)
ROWSPEC = [
    ('E1c2-8e3', 'edge', (1, 2, 8, 3)),
    ('E2c3-8e0', 'edge', (2, 3, 8, 0)),
    ('E3c2-7e3', 'edge', (3, 2, 7, 3)),
    ('E4c1-7e2', 'edge', (4, 1, 7, 2)),
    ('E4c2-6e3', 'edge', (4, 2, 6, 3)),
    ('E5c0-9e1', 'edge', (5, 0, 9, 1)),
    ('E6c1-9e2', 'edge', (6, 1, 9, 2)),      # == E9c3-6e0 up to rational factor
    ('W6c2[y=s]', 'wall', (6, 2, 'y=s')),
    ('E7c1-8e2', 'edge', (7, 1, 8, 2)),      # == E8c3-7e0
    ('E7c2-9e3', 'edge', (7, 2, 9, 3)),      # == E9c0-7e1
    ('E8c2-10e3', 'edge', (8, 2, 10, 3)),    # == E10c0-8e1
    ('E9c1-10e2', 'edge', (9, 1, 10, 2)),    # == E10c3-9e0
    ('W10c1[x=s]', 'wall', (10, 1, 'x=s')),
]


def build_generators():
    gens = []
    for name, kind, spec in ROWSPEC:
        if kind == 'wall':
            i, k, wall = spec
            gens.append((name, row_wall(i, k, wall)))
        else:
            i, k, j, e = spec
            gens.append((name, row_edge(i, k, j, e)))
    return gens


# ---------------------------------------------------------------------------
# canonical octic
# ---------------------------------------------------------------------------
OCTIC = [F(-6865), F(12420), F(-6754), F(-496), F(1923), F(-842), F(178), F(-20), F(1)]

# ---------------------------------------------------------------------------
# univariate helpers (exact Sturm, as in verify_sturm.py)
# ---------------------------------------------------------------------------

def upolyval(c, x):
    r = F(0)
    for coef in reversed(c):
        r = r * x + coef
    return r


def ustrip(c):
    c = list(c)
    while c and c[-1] == 0:
        c.pop()
    return c


def uderiv(c):
    return [F(k) * c[k] for k in range(1, len(c))]


def urem(a, b):
    r = [F(x) for x in a]
    db, lb = len(b) - 1, b[-1]
    while True:
        r = ustrip(r)
        if not r or len(r) - 1 < db:
            return r
        coef = r[-1] / lb
        deg = len(r) - 1 - db
        for i2 in range(len(b)):
            r[deg + i2] -= coef * b[i2]
        r.pop()


def sturm_no_root(c, a, b):
    """True iff the squarefree part of c has no root in [a, b]; requires
    c(a) != 0 != c(b).  Works for arbitrary c by dividing out gcd(c, c')."""
    p0 = ustrip([F(x) for x in c])
    if not p0:
        return False
    if upolyval(p0, a) == 0 or upolyval(p0, b) == 0:
        return False
    # gcd(c, c') via Euclid, then squarefree part
    x, y = p0, ustrip(uderiv(p0))
    while y:
        x, y = y, urem(x, y)
    g = x
    if len(g) > 1:
        # divide p0 by g exactly
        q = []
        r = list(p0)
        dg, lg = len(g) - 1, g[-1]
        while len(ustrip(r)) - 1 >= dg and ustrip(r):
            r = ustrip(r)
            coef = r[-1] / lg
            deg = len(r) - 1 - dg
            q.append((deg, coef))
            for i2 in range(len(g)):
                r[deg + i2] -= coef * g[i2]
            r.pop()
        assert not ustrip(r)
        p0 = [F(0)] * (max(d for d, _ in q) + 1)
        for d, cf in q:
            p0[d] = cf
        p0 = ustrip(p0)
        if upolyval(p0, a) == 0 or upolyval(p0, b) == 0:
            return False
    chain = [p0, ustrip(uderiv(p0))]
    while chain[-1]:
        nxt = [ -v for v in urem(chain[-2], chain[-1]) ]
        if not nxt:
            break
        chain.append(nxt)

    def variations(x0):
        signs = []
        for p in chain:
            v = upolyval(p, x0)
            if v:
                signs.append(1 if v > 0 else -1)
        return sum(1 for u, v in zip(signs, signs[1:]) if u != v)

    return variations(a) - variations(b) == 0


# ---------------------------------------------------------------------------
# certificate parsing
# ---------------------------------------------------------------------------

def parse_q(s):
    return F(s)


def parse_upoly(lst):
    return [parse_q(x) for x in lst]


def parse_biv(obj):
    """Bivariate in (t, S): list of {"spow": k, "t": [coeffs low-to-high]} ->
    sparse 13-var poly."""
    r = {}
    for term in obj:
        k = int(term['spow'])
        for tp, cs in enumerate(term['t']):
            c = parse_q(cs)
            if c:
                e = [0] * NVAR
                e[IT] = tp
                e[IS] = k
                m = tuple(e)
                s = r.get(m, F(0)) + c
                if s:
                    r[m] = s
                else:
                    r.pop(m, None)
    return r


def fail(msg):
    print('FAIL:', msg)
    sys.exit(1)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    corrupt = None
    for a in sys.argv[1:]:
        if a.startswith('--corrupt'):
            corrupt = a.split('=', 1)[1] if '=' in a else None
    if '--corrupt' in sys.argv:
        i = sys.argv.index('--corrupt')
        corrupt = sys.argv[i + 1] if i + 1 < len(sys.argv) else None
    if not args:
        print('usage: verify_cidl.py CERT.json [--corrupt qcoeff|e|rowspec|octic]')
        sys.exit(2)
    try:
        cert = json.load(open(args[0]))
    except Exception as ex:  # noqa
        print('malformed:', ex)
        sys.exit(2)

    try:
        oct_c = parse_upoly(cert['octic']['coefficients_low_to_high'])
        e_c = parse_upoly(cert['e']['coefficients_low_to_high'])
        delta_c = parse_upoly(cert['Delta']['coefficients_low_to_high'])
        cof = {k: parse_biv(v) for k, v in cert['cofactors'].items()}
        ga = parse_q(cert['gate_interval']['a'])
        gb = parse_q(cert['gate_interval']['b'])
    except Exception as ex:  # noqa
        print('malformed:', ex)
        sys.exit(2)

    # --- corruption gates -------------------------------------------------
    global ROWSPEC
    if corrupt == 'qcoeff':
        name = sorted(cof)[0]
        m = next(iter(cof[name]))
        cof[name][m] += 1
    elif corrupt == 'e':
        e_c[0] += F(1, 7)
    elif corrupt == 'octic':
        oct_c[3] += 1
    elif corrupt == 'rowspec':
        nm, kd, sp = ROWSPEC[2]
        ROWSPEC = list(ROWSPEC)
        ROWSPEC[2] = (nm, kd, (3, 2, 7, 2))  # wrong edge index
    elif corrupt is not None:
        print('unknown corruption mode', corrupt)
        sys.exit(2)

    # --- [O] canonical octic ---------------------------------------------
    if oct_c != OCTIC:
        fail('[O] octic is not the canonical Trump octic')
    print('[O] octic == canonical Trump octic: OK')

    # --- gate interval sanity: must contain [3/10, 2/5] --------------------
    if not (ga <= F(3, 10) and gb >= F(2, 5)):
        fail('[G] gate interval does not contain [3/10, 2/5]')

    # --- [G] sign gate -----------------------------------------------------
    if not sturm_no_root(e_c, ga, gb):
        fail('[G] e(t) has a root (or endpoint zero) in the gate interval')
    if not sturm_no_root(delta_c, ga, gb):
        fail('[G] Delta(t) has a root (or endpoint zero) in the gate interval')
    print('[G] e, Delta have no root in [%s, %s]: OK' % (ga, gb))

    # --- [I] the identity --------------------------------------------------
    gens = build_generators()
    names = [n for n, _ in gens]
    if sorted(cof) != sorted(names):
        fail('[I] cofactor keys do not match the 13 generator names')

    lhs = pzero()
    for n, g in gens:
        lhs = padd(lhs, pmul(cof[n], g))

    # rhs = e * Delta^8 * octic(S)
    def uni_to_p(c, var):
        r = {}
        for k, v in enumerate(c):
            if v:
                ee = [0] * NVAR
                ee[var] = k
                r[tuple(ee)] = v
        return r

    ep = uni_to_p(e_c, IT)
    dp = uni_to_p(delta_c, IT)
    d8 = ONE
    for _ in range(8):
        d8 = pmul(d8, dp)
    rhs = pmul(pmul(ep, d8), uni_to_p(OCTIC, IS))

    diff = padd(lhs, pscale(rhs, -1))
    if diff:
        fail('[I] identity does not hold: %d residual monomials, e.g. %s' %
             (len(diff), sorted(diff.items())[0],))
    print('[I] e*Delta^8*octic(S) == sum q_j G_j  (exact, %d generators): OK' % len(gens))

    print('PASS: cidl-membership-v1 certificate verified')
    sys.exit(0)


if __name__ == '__main__':
    main()
