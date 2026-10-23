"""Independent check of Theorem C's hypotheses for Evan Daniel's grade-C configurations.

Written for the stage 4 mathematical review of the #545 import (bead think-7scz) from the
mathematics of Theorem C (grade-C.md) as the review re-derives it, with the side-end
relaxation in its pair form.  It imports nothing from the source and uses Python's
standard library for every decision; numpy and scipy only propose candidates (the
multipliers' linear program, a basis order) and cross-check a rank numerically, and each
candidate is then verified exactly.

Inputs, read as data:
  MINPOLY  n-N.minpoly.json or .json.gz: the exact configuration over K = Q[t]/(f), with
           an isolating interval for the real root t*;
  CONTACTS n-N.contacts.json: candidate rows ('load_bearing'), from the release archive
           gradec-233.tar.zst, read in memory.  Every row it lists is verified; which rows
           it lists is untrusted and does not affect soundness (dropping rows relaxes).

What it decides, exactly in K, with signs at t* by interval arithmetic:
  P  the record is a packing: every corner in [0, S]^2, every pair weakly separated by
     an edge normal (so the interiors are disjoint);
  R  every kept row is tight at z* and valid near it: a wall row; an interior incidence
     (corner strictly inside the side, |tau| < 1/2); or a complete side-end pair (two
     adjacent corners of j at the two ends of side k of i, so that j's edge is i's side);
  M  multipliers lambda* > 0 with sum_r lambda*_r L_r = e_S exactly;
  N  null L0 = F + W', with F the flat family (null space of the position columns) and
     W' a complement, by exact elimination (cross-checked by a numerical SVD);
  A  hypothesis 2: affine null vectors w + sum_k phi_k v_k with L(phi)(w + sum phi_k v_k)
     = 0 identically and zero S-components, one solve per (w, k) (see lift_systems);
  H  hypothesis 3: the Lagrangian Hessian restricted to W' is positive definite (exact
     LDL^T), and its F x W' block vanishes.

Usage (from any directory; paths are arguments):
  python -I check_theorem_c.py --minpoly-dir DIR --archive gradec-233.tar.zst \
      [--dropzero N,N] [--out receipts.jsonl] N [N ...]
"""

import argparse
import gzip
import heapq
import json
import math
import os
import sys
import tarfile
import time
from fractions import Fraction as Fr

HALF = Fr(1, 2)
CORNERS = ((1, 1), (-1, 1), (-1, -1), (1, -1))      # corner a = centre + (s1 u + s2 v)/2
SIDES = ((1, 0), (0, 1), (-1, 0), (0, -1))           # side k: outward normal R(theta) e_k
INF = math.inf


# ----------------------------------------------------------------------------- the field
class RationalField:
    """K = Q[t]/(a1 t + a0): every element is its value at t* = -a0/a1, a Fraction."""

    degree = 1

    def __init__(self, f):
        a0, a1 = Fr(f[0]), Fr(f[1])
        assert a1 != 0
        self.tstar = -a0 / a1
        self.zero, self.one = Fr(0), Fr(1)

    def elem(self, coeffs):
        v, p = Fr(0), Fr(1)
        for c in coeffs:
            v += Fr(c) * p
            p *= self.tstar
        return v

    def const(self, q):
        return Fr(q)

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def sub(a, b):
        return a - b

    @staticmethod
    def mul(a, b):
        return a * b

    @staticmethod
    def neg(a):
        return -a

    @staticmethod
    def is_zero(a):
        return a == 0

    @staticmethod
    def inv(a):
        assert a != 0
        return 1 / a

    @staticmethod
    def sign(a):
        return (a > 0) - (a < 0)

    @staticmethod
    def to_float(a):
        return float(a)

    def enclosure(self, a):
        return a, a


class NumberField:
    """K = Q[t]/(f), deg f = d >= 2, elements as d-tuples of Fractions in the power basis.

    Signs are decided at the real root t* in the isolating interval [ta, tb]: an element
    that is not zero modulo f is evaluated on the interval exactly (Horner, Fractions),
    and the interval is bisected until the enclosure excludes 0."""

    def __init__(self, f, t_interval):
        f = [Fr(c) for c in f]
        while f and f[-1] == 0:
            f.pop()
        self.d = d = len(f) - 1
        assert d >= 2
        lc = f[-1]
        self.f = [c / lc for c in f]                       # monic
        self.degree = d
        # t^(d+i) = sum_j red[i][j] t^j, i = 0 .. d-2
        red, cur = [], [-c for c in self.f[:d]]
        for _ in range(d - 1):
            red.append(cur)
            top = cur[-1]
            nxt = [Fr(0)] + cur[:-1]
            cur = [nxt[j] + top * (-self.f[j]) for j in range(d)]
        self.red = red
        self.zero = tuple(Fr(0) for _ in range(d))
        self.one = (Fr(1),) + tuple(Fr(0) for _ in range(d - 1))
        ta, tb = (Fr(x) for x in t_interval)
        fa, fb = self.fval(ta), self.fval(tb)
        if ta == tb:
            assert fa == 0, 'the t interval is a point that is not a root of f'
        else:
            assert ta < tb and fa * fb < 0, 'f has no sign change on the t interval'
        self.ta, self.tb = ta, tb
        self.refinements = 0

    def fval(self, x):
        v = Fr(0)
        for c in reversed(self.f):
            v = v * x + c
        return v

    def bisect(self):
        if self.ta == self.tb:
            return
        mid = (self.ta + self.tb) / 2
        fm = self.fval(mid)
        if fm == 0:
            self.ta = self.tb = mid
        elif self.fval(self.ta) * fm < 0:
            self.tb = mid
        else:
            self.ta = mid
        self.refinements += 1

    def elem(self, coeffs):
        c = [Fr(x) for x in coeffs]
        d = self.d
        while len(c) > d:                               # eliminate the top coefficient
            top = c.pop()
            if top:
                s = len(c) - d
                for j in range(d):
                    c[s + j] -= top * self.f[j]
        return tuple(c + [Fr(0)] * (d - len(c)))

    def _reduce(self, c):
        d = self.d
        out = list(c[:d]) + [Fr(0)] * max(0, d - len(c))
        for i, x in enumerate(c[d:]):
            if x:
                for j, r in enumerate(self.red[i]):
                    out[j] += x * r
        return tuple(out)

    def const(self, q):
        return (Fr(q),) + tuple(Fr(0) for _ in range(self.d - 1))

    @staticmethod
    def add(a, b):
        return tuple(x + y for x, y in zip(a, b))

    @staticmethod
    def sub(a, b):
        return tuple(x - y for x, y in zip(a, b))

    @staticmethod
    def neg(a):
        return tuple(-x for x in a)

    def mul(self, a, b):
        d = self.d
        prod = [Fr(0)] * (2 * d - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    if y:
                        prod[i + j] += x * y
        return self._reduce(prod)

    @staticmethod
    def is_zero(a):
        return not any(a)

    def inv(self, a):
        """Solve M_a x = 1 for the multiplication matrix of a, then verify a x = 1."""
        assert any(a), 'inverse of zero'
        d = self.d
        cols = []
        e = list(self.one)
        for _ in range(d):
            cols.append(self.mul(a, tuple(e)))
            e = [Fr(0)] + e[:-1]                        # t^k -> t^(k+1)
        # cols[k] = a * t^k; build the d x d system  sum_k x_k cols[k] = 1
        A = [[cols[k][r] for k in range(d)] + [self.one[r]] for r in range(d)]
        for c in range(d):
            p = next(r for r in range(c, d) if A[r][c] != 0)
            A[c], A[p] = A[p], A[c]
            iv = 1 / A[c][c]
            A[c] = [x * iv for x in A[c]]
            for r in range(d):
                if r != c and A[r][c] != 0:
                    fct = A[r][c]
                    A[r] = [x - fct * y for x, y in zip(A[r], A[c])]
        x = tuple(A[r][d] for r in range(d))
        assert self.mul(a, x) == self.one, 'inverse does not verify'
        return x

    def enclosure(self, a):
        ta, tb = self.ta, self.tb
        lo = hi = a[-1]
        for c in reversed(a[:-1]):
            p = (lo * ta, lo * tb, hi * ta, hi * tb)
            lo, hi = min(p) + c, max(p) + c
        return lo, hi

    def sign(self, a):
        if not any(a):
            return 0
        for _ in range(4000):
            lo, hi = self.enclosure(a)
            if lo > 0:
                return 1
            if hi < 0:
                return -1
            self.bisect()
        raise RuntimeError('sign not decided after 4000 bisections')

    def to_float(self, a):
        lo, hi = self.enclosure(a)
        return float((lo + hi) / 2)


def make_field(D):
    f = D['field']['f']
    while len(f) > 1 and Fr(f[-1]) == 0:
        f = f[:-1]
    if len(f) == 2:
        K = RationalField(f)
        ta, tb = (Fr(x) for x in D['field']['t_interval'])
        assert ta <= K.tstar <= tb, 't* outside the stated interval'
        return K
    return NumberField(f, D['field']['t_interval'])


# ------------------------------------------------------------- rigorous float intervals
def fl_out(lo, hi):
    return (math.nextafter(float(lo), -INF), math.nextafter(float(hi), INF))


def iadd(a, b):
    return (math.nextafter(a[0] + b[0], -INF), math.nextafter(a[1] + b[1], INF))


def isub(a, b):
    return (math.nextafter(a[0] - b[1], -INF), math.nextafter(a[1] - b[0], INF))


def imul(a, b):
    p = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return (math.nextafter(min(p), -INF), math.nextafter(max(p), INF))


def iscale(a, q):                                 # q an exact small float (here +-1/2, +-1)
    return imul(a, (q, q))


def iabs(a):
    if a[0] >= 0:
        return a
    if a[1] <= 0:
        return (-a[1], -a[0])
    return (0.0, max(-a[0], a[1]))


# --------------------------------------------------------------------------- the record
class Record:
    def __init__(self, D):
        self.n = D['n']
        self.K = K = make_field(D)
        self.S = K.elem(D['S']['in_K'])
        X, Y, C, Sn = [], [], [], []
        for sq in D['squares']:
            u = K.elem(sq['u'])
            uu = K.mul(u, u)
            den = K.inv(K.add(K.one, uu))
            c = K.mul(K.sub(K.one, uu), den)
            s = K.mul(K.mul(K.const(2), u), den)
            for _ in range(sq['m'] % 4):
                c, s = K.neg(s), c
            assert K.is_zero(K.sub(K.add(K.mul(c, c), K.mul(s, s)), K.one))
            X.append(K.elem(sq['x']))
            Y.append(K.elem(sq['y']))
            C.append(c)
            Sn.append(s)
        self.X, self.Y, self.C, self.Sn = X, Y, C, Sn

    # geometry, exact in K
    def normal(self, i, k):
        K = self.K
        ex, ey = SIDES[k]
        c, s = self.C[i], self.Sn[i]
        return (K.sub(K.mul(c, K.const(ex)), K.mul(s, K.const(ey))),
                K.add(K.mul(s, K.const(ex)), K.mul(c, K.const(ey))))

    def offset(self, j, a):
        """R_j o_a with o_a = (s1, s2)/2."""
        K = self.K
        s1, s2 = CORNERS[a]
        c, s = self.C[j], self.Sn[j]
        h1, h2 = K.const(Fr(s1, 2)), K.const(Fr(s2, 2))
        return (K.sub(K.mul(c, h1), K.mul(s, h2)), K.add(K.mul(s, h1), K.mul(c, h2)))

    def corner(self, j, a, Xc=None, Yc=None):
        K = self.K
        Xc = Xc or self.X
        Yc = Yc or self.Y
        ox, oy = self.offset(j, a)
        return K.add(Xc[j], ox), K.add(Yc[j], oy)


# ------------------------------------------------------------------------------ the rows
def row_value(rec, r):
    K = rec.K
    if r[0] == 'W':
        _, j, a, w = r
        px, py = rec.corner(j, a)
        return {'L': px, 'B': py, 'R': K.sub(rec.S, px), 'T': K.sub(rec.S, py)}[w]
    _, j, a, i, k = r
    nx, ny = rec.normal(i, k)
    px, py = rec.corner(j, a)
    dx, dy = K.sub(px, rec.X[i]), K.sub(py, rec.Y[i])
    return K.sub(K.add(K.mul(nx, dx), K.mul(ny, dy)), K.const(HALF))


def row_tau(rec, r):
    """Position of corner a of j along side k of i: the value of side k+1 of i at it."""
    K = rec.K
    _, j, a, i, k = r
    mx, my = rec.normal(i, (k + 1) % 4)
    px, py = rec.corner(j, a)
    return K.add(K.mul(mx, K.sub(px, rec.X[i])), K.mul(my, K.sub(py, rec.Y[i])))


def classify_rows(rec, contacts):
    """Return kept rows, the side-end pairs, the margin and what was dropped, deciding
    each incidence's class exactly."""
    K = rec.K
    walls, interior, ends, beyond = [], [], {}, []
    for r in contacts:
        r = tuple(r)
        if r[0] == 'W':
            assert r[3] in ('L', 'R', 'B', 'T') and 0 <= r[1] < rec.n and 0 <= r[2] < 4
            assert K.is_zero(row_value(rec, r)), f'wall row {r} not tight'
            walls.append(r)
            continue
        assert r[0] == 'C' and len(r) == 5 and r[1] != r[3]
        assert K.is_zero(row_value(rec, r)), f'row {r} not tight at the record'
        tau = row_tau(rec, r)
        q = K.sub(K.mul(tau, tau), K.const(Fr(1, 4)))
        sg = K.sign(q)
        if sg == 0:
            ends.setdefault((r[1], r[3], r[4]), []).append((r, tau))
        elif sg < 0:
            interior.append((r, tau))
        else:
            beyond.append(r)
    pairs, lone = [], []
    for key, inc in ends.items():
        corners = sorted({x[0][2] for x in inc})
        if len(inc) == 2 and len(corners) == 2 and (corners[1] - corners[0]) % 4 in (1, 3) \
                and K.is_zero(K.add(inc[0][1], inc[1][1])):
            pairs.append((inc[0][0], inc[1][0]))           # the two ends: tau = +1/2 and -1/2
        else:
            lone += [x[0] for x in inc]
    margins = []
    for r, tau in interior:
        mu = K.sub(K.const(HALF), tau) if K.sign(tau) >= 0 else K.add(K.const(HALF), tau)
        assert K.sign(mu) > 0
        margins.append(K.to_float(mu))
    rows = walls + [r for r, _ in interior] + [x for p in pairs for x in p]
    return dict(rows=rows, walls=walls, interior=[r for r, _ in interior], pairs=pairs,
                lone=lone, beyond=beyond, margin=min(margins) if margins else 0.5)


# ------------------------------------------------------------ derivatives (z = x, y, theta, S)
def J(v, K):
    return (K.neg(v[1]), v[0])


def row_grad(rec, r, var, Xc=None, Yc=None):
    """Gradient of h_r at the record angles, positions Xc, Yc (default the record)."""
    K = rec.K
    Xc = Xc or rec.X
    Yc = Yc or rec.Y
    out = {}

    def put(key, val):
        c = var[key]
        out[c] = K.add(out.get(c, K.zero), val)

    if r[0] == 'W':
        _, j, a, w = r
        o = rec.offset(j, a)
        jo = J(o, K)
        if w == 'L':
            put(('x', j), K.one); put(('t', j), jo[0])
        elif w == 'R':
            put('S', K.one); put(('x', j), K.neg(K.one)); put(('t', j), K.neg(jo[0]))
        elif w == 'B':
            put(('y', j), K.one); put(('t', j), jo[1])
        else:
            put('S', K.one); put(('y', j), K.neg(K.one)); put(('t', j), K.neg(jo[1]))
    else:
        _, j, a, i, k = r
        n = rec.normal(i, k)
        jn = J(n, K)
        o = rec.offset(j, a)
        jo = J(o, K)
        px, py = K.add(Xc[j], o[0]), K.add(Yc[j], o[1])
        dx, dy = K.sub(px, Xc[i]), K.sub(py, Yc[i])
        put(('x', j), n[0]); put(('y', j), n[1])
        put(('x', i), K.neg(n[0])); put(('y', i), K.neg(n[1]))
        put(('t', j), K.add(K.mul(n[0], jo[0]), K.mul(n[1], jo[1])))
        put(('t', i), K.add(K.mul(jn[0], dx), K.mul(jn[1], dy)))
    return {c: v for c, v in out.items() if not K.is_zero(v)}


def row_hess(rec, r, var):
    """Second derivatives of h_r at the record: {(c1, c2): value} with c1 <= c2."""
    K = rec.K
    out = {}

    def put(k1, k2, val):
        a, b = sorted((var[k1], var[k2]))
        out[(a, b)] = K.add(out.get((a, b), K.zero), val)

    if r[0] == 'W':
        _, j, a, w = r
        ox, oy = rec.offset(j, a)
        put(('t', j), ('t', j), {'L': K.neg(ox), 'R': ox, 'B': K.neg(oy), 'T': oy}[w])
    else:
        _, j, a, i, k = r
        n = rec.normal(i, k)
        jn = J(n, K)
        o = rec.offset(j, a)
        jo = J(o, K)
        px, py = rec.corner(j, a)
        dx, dy = K.sub(px, rec.X[i]), K.sub(py, rec.Y[i])
        put(('t', i), ('t', i), K.neg(K.add(K.mul(n[0], dx), K.mul(n[1], dy))))
        put(('t', i), ('x', i), K.neg(jn[0]))
        put(('t', i), ('y', i), K.neg(jn[1]))
        put(('t', i), ('x', j), jn[0])
        put(('t', i), ('y', j), jn[1])
        put(('t', i), ('t', j), K.add(K.mul(jn[0], jo[0]), K.mul(jn[1], jo[1])))
        put(('t', j), ('t', j), K.neg(K.add(K.mul(n[0], o[0]), K.mul(n[1], o[1]))))
    return {c: v for c, v in out.items() if not K.is_zero(v)}


# ------------------------------------------------------------------- sparse elimination
class Echelon:
    """Row echelon form over K by sparse elimination, recording the operations so that
    any right-hand side can be carried through afterwards.

    Rows are processed in order.  A row is reduced by the existing pivot rows in the
    order they were created (a heap of pivot indices), so a reduction only ever
    introduces entries at later pivot columns or at free columns; a row that does not
    reduce to zero becomes a pivot row, normalised to 1 at its pivot column, which is
    chosen among its entries as the one occurring in the fewest original rows."""

    def __init__(self, K, rows, ncols, colcount=None):
        self.K, self.ncols = K, ncols
        self.piv = {}                 # pivot col -> row dict (normalised)
        self.pidx = {}                # pivot col -> creation index
        self.order = []               # pivot cols in creation order
        self.log = []                 # per input row: (ops [(col, mult)], pivot col or None, inv)
        if colcount is None:
            colcount = {}
            for r in rows:
                for c in r:
                    colcount[c] = colcount.get(c, 0) + 1
        zero = K.zero
        for r in rows:
            r = {c: v for c, v in r.items() if not K.is_zero(v)}
            ops = []
            heap = [(self.pidx[c], c) for c in r if c in self.piv]
            heapq.heapify(heap)
            while heap:
                _, c = heapq.heappop(heap)
                a = r.pop(c, None)
                if a is None:
                    continue
                ops.append((c, a))
                for cc, vv in self.piv[c].items():
                    if cc == c:
                        continue
                    old = r.get(cc)
                    nv = K.sub(old if old is not None else zero, K.mul(a, vv))
                    if K.is_zero(nv):
                        if old is not None:
                            del r[cc]
                    else:
                        if old is None and cc in self.piv:
                            heapq.heappush(heap, (self.pidx[cc], cc))
                        r[cc] = nv
            if not r:
                self.log.append((ops, None, None))
                continue
            c0 = min(r, key=lambda c: (colcount.get(c, 0), c))
            iv = K.inv(r[c0])
            r = {c: K.mul(v, iv) for c, v in r.items()}
            self.pidx[c0] = len(self.order)
            self.order.append(c0)
            self.piv[c0] = r
            self.log.append((ops, c0, iv))

    @property
    def rank(self):
        return len(self.order)

    def check_echelon(self):
        """Each pivot row is 1 at its pivot column and 0 at every earlier pivot column."""
        K = self.K
        for k, c in enumerate(self.order):
            row = self.piv[c]
            assert row[c] == K.one
            for cc in row:
                if cc != c and cc in self.pidx:
                    assert self.pidx[cc] > k, 'echelon property violated'

    def nullspace(self):
        """Basis of {v : row . v = 0 for all input rows}, one vector per free column."""
        K = self.K
        free = [c for c in range(self.ncols) if c not in self.piv]
        expr = {}                                   # pivot col -> {free col: coeff}
        for c in reversed(self.order):
            acc = {}
            for cc, vv in self.piv[c].items():
                if cc == c:
                    continue
                src = expr[cc] if cc in self.piv else {cc: K.one}
                for fc, fv in src.items():
                    nv = K.sub(acc.get(fc, K.zero), K.mul(vv, fv))
                    if K.is_zero(nv):
                        acc.pop(fc, None)
                    else:
                        acc[fc] = nv
            expr[c] = acc
        basis = []
        for fc in free:
            v = {fc: K.one}
            for c, e in expr.items():
                x = e.get(fc)
                if x is not None:
                    v[c] = x
            basis.append(v)
        return basis

    def solve(self, rhs):
        """Solve rows . v = rhs (rhs a list over input rows).  Returns v (free columns 0)
        or None if inconsistent."""
        K = self.K
        beta = {}
        for idx, (ops, c0, iv) in enumerate(self.log):
            b = rhs[idx]
            for c, a in ops:
                b = K.sub(b, K.mul(a, beta[c]))
            if c0 is None:
                if not K.is_zero(b):
                    return None
            else:
                beta[c0] = K.mul(b, iv)
        v = {}
        for c in reversed(self.order):
            x = beta[c]
            for cc, vv in self.piv[c].items():
                if cc != c and cc in v:
                    x = K.sub(x, K.mul(vv, v[cc]))
            if not K.is_zero(x):
                v[c] = x
        return v


def matvec(K, rows, v):
    out = []
    for r in rows:
        acc = K.zero
        for c, x in r.items():
            y = v.get(c)
            if y is not None:
                acc = K.add(acc, K.mul(x, y))
        out.append(acc)
    return out


# -------------------------------------------------------------- the packing of the record
def check_packing(rec):
    """Decide that the record is a packing in [0, S]^2: corners inside, pairs weakly
    separated along an edge normal.  Float intervals with outward rounding decide almost
    everything; exact arithmetic in K decides what they leave open."""
    K, n = rec.K, rec.n
    enc = lambda a: fl_out(*K.enclosure(a))
    X = [enc(x) for x in rec.X]
    Y = [enc(y) for y in rec.Y]
    C = [enc(c) for c in rec.C]
    Sn = [enc(s) for s in rec.Sn]
    S = enc(rec.S)
    stats = {'corners_exact': 0, 'pairs_disc': 0, 'pairs_float': 0, 'pairs_exact': 0, 'touching_axes': 0}

    def corner_iv(j, a):
        s1, s2 = CORNERS[a]
        ox = isub(iscale(C[j], s1 / 2), iscale(Sn[j], s2 / 2))
        oy = iadd(iscale(Sn[j], s1 / 2), iscale(C[j], s2 / 2))
        return iadd(X[j], ox), iadd(Y[j], oy)

    for j in range(n):
        for a in range(4):
            px, py = corner_iv(j, a)
            for g in (px, isub(S, px), py, isub(S, py)):
                if g[0] >= 0:
                    continue
                stats['corners_exact'] += 1
                ex, ey = rec.corner(j, a)
                gs = [ex, K.sub(rec.S, ex), ey, K.sub(rec.S, ey)]
                assert all(K.sign(x) >= 0 for x in gs), f'square {j} corner {a} outside the container'
                break
    # pairs
    order = sorted(range(n), key=lambda i: X[i][0])
    for p in range(n):
        i = order[p]
        for q in range(p + 1, n):
            j = order[q]
            if X[j][0] - X[i][1] > 1.5:
                break                                          # sorted by x: all later are farther
            dx, dy = isub(X[j], X[i]), isub(Y[j], Y[i])
            d2 = iadd(imul(dx, dx), imul(dy, dy))
            if d2[0] >= 2.0:
                stats['pairs_disc'] += 1
                continue
            axes = []
            for own, oth in ((i, j), (j, i)):
                u, v = (C[own], Sn[own]), ((-Sn[own][1], -Sn[own][0]), C[own])
                for nvec in (u, v):
                    proj = iabs(iadd(imul(nvec[0], isub(X[oth], X[own])), imul(nvec[1], isub(Y[oth], Y[own]))))
                    ca = iabs(iadd(imul(nvec[0], C[oth]), imul(nvec[1], Sn[oth])))
                    sa = iabs(iadd(imul(nvec[0], (-Sn[oth][1], -Sn[oth][0])), imul(nvec[1], C[oth])))
                    gap = isub(proj, iadd((0.5, 0.5), iscale(iadd(ca, sa), 0.5)))
                    axes.append((gap, own, oth, nvec is u))
            if any(g[0][0] > 0 for g in axes):
                stats['pairs_float'] += 1
                continue
            ok = False
            for gap, own, oth, is_u in sorted(axes, key=lambda z: -z[0][1]):
                if gap[1] < 0:
                    continue
                c, s = rec.C[own], rec.Sn[own]
                nx, ny = (c, s) if is_u else (K.neg(s), c)
                proj = K.add(K.mul(nx, K.sub(rec.X[oth], rec.X[own])), K.mul(ny, K.sub(rec.Y[oth], rec.Y[own])))
                ca = K.add(K.mul(nx, rec.C[oth]), K.mul(ny, rec.Sn[oth]))
                sa = K.add(K.mul(nx, K.neg(rec.Sn[oth])), K.mul(ny, rec.C[oth]))
                ab = lambda z: z if K.sign(z) >= 0 else K.neg(z)
                g = K.sub(ab(proj), K.add(K.const(HALF), K.mul(K.const(HALF), K.add(ab(ca), ab(sa)))))
                sg = K.sign(g)
                if sg >= 0:
                    ok = True
                    stats['touching_axes'] += sg == 0
                    break
            assert ok, f'pair ({i}, {j}) not proved separated'
            stats['pairs_exact'] += 1
    return stats


# ----------------------------------------------------------------------- the multipliers
def multipliers(rec, rows, L0, N, sv):
    """Exact lambda* > 0 with sum lambda_r L_r = e_S.  A linear program (scipy, HiGHS)
    proposes a max-min point; the non-basic multipliers are rounded to dyadic rationals
    and the basic ones solved exactly; the identity and the signs are then verified."""
    import numpy as np
    import scipy.linalg as sla
    from scipy.optimize import linprog
    K = rec.K
    m = len(rows)
    Ln = np.zeros((m, N))
    for a, r in enumerate(L0):
        for c, v in r.items():
            Ln[a, c] = K.to_float(v)
    es = np.zeros(N)
    es[sv] = 1.0
    res = linprog(np.r_[np.zeros(m), -1.0], A_eq=np.c_[Ln.T, np.zeros(N)], b_eq=es,
                  A_ub=np.c_[-np.eye(m), np.ones(m)], b_ub=np.zeros(m),
                  bounds=[(None, None)] * m + [(None, 1.0)], method='highs')
    if res.status != 0:
        return None, f'linear program status {res.status}', None
    tstar = float(res.x[-1])
    if tstar <= 1e-12:
        return None, f'max-min multiplier {tstar:.3g} not positive', tstar
    lam_n = res.x[:m]
    _, _, perm = sla.qr(Ln.T, pivoting=True, mode='economic')
    # exact basis: rows of L0 in QR order that are independent (exact echelon on them)
    ech = Echelon(K, [L0[a] for a in perm], N)
    basis = sorted(perm[k] for k, (_, c0, _) in enumerate(ech.log) if c0 is not None)
    bset = set(basis)
    lam = {}
    for a in range(m):
        if a not in bset:
            lam[a] = K.const(Fr(round(lam_n[a] * 2 ** 40), 2 ** 40))
    # sum_{b in B} lam_b L0[b][v] = e_S[v] - sum_{a not in B} lam_a L0[a][v]
    eqs = [{} for _ in range(N)]
    rhs = [K.one if v == sv else K.zero for v in range(N)]
    bidx = {b: k for k, b in enumerate(basis)}
    for a in range(m):
        for c, x in L0[a].items():
            if a in bset:
                eqs[c][bidx[a]] = x
            else:
                rhs[c] = K.sub(rhs[c], K.mul(lam[a], x))
    sol_ech = Echelon(K, eqs, len(basis))
    sol = sol_ech.solve(rhs)
    if sol is None or sol_ech.rank != len(basis):
        return None, 'basis system inconsistent or singular', tstar
    for b in basis:
        lam[b] = sol.get(bidx[b], K.zero)
    # verify the identity exactly, coordinate by coordinate
    tot = [K.zero] * N
    for a in range(m):
        for c, x in L0[a].items():
            tot[c] = K.add(tot[c], K.mul(lam[a], x))
    for v in range(N):
        assert tot[v] == (K.one if v == sv else K.zero), 'KKT identity fails'
    signs = [K.sign(lam[a]) for a in range(m)]
    if min(signs) <= 0:
        return None, 'a multiplier is not positive after rounding', tstar
    return lam, None, tstar


def forced_zero_rows(rec, rows, L0, N, sv):
    """Rows that carry zero force in every nonnegative multiplier vector (linear
    program; a selection only: dropping rows relaxes the problem)."""
    import numpy as np
    from scipy.optimize import linprog
    K = rec.K
    m = len(rows)
    Ln = np.zeros((m, N))
    for a, r in enumerate(L0):
        for c, v in r.items():
            Ln[a, c] = K.to_float(v)
    es = np.zeros(N)
    es[sv] = 1.0
    res = linprog(np.r_[np.zeros(m), -np.ones(m), 0.0],
                  A_eq=np.c_[Ln.T, np.zeros((N, m)), -es], b_eq=np.zeros(N),
                  A_ub=np.c_[-np.eye(m), np.eye(m), np.zeros(m)], b_ub=np.zeros(m),
                  bounds=[(0, None)] * m + [(0, 1)] * m + [(0, None)], method='highs')
    assert res.status == 0 and res.x[-1] > 0, 'e_S is not in the cone of the rows'
    return {a for a in range(m) if res.x[m + a] < 1e-7}


# --------------------------------------------------------------------------- one count
def ldl_pivots(K, Q):
    """Exact LDL^T without pivoting of a symmetric matrix; returns the pivots d_k
    (positive definite iff all are positive)."""
    k = len(Q)
    A = [row[:] for row in Q]
    piv = []
    for c in range(k):
        d = A[c][c]
        piv.append(d)
        if K.sign(d) <= 0:
            return piv, False
        di = K.inv(d)
        for r in range(c + 1, k):
            if not K.is_zero(A[r][c]):
                f = K.mul(A[r][c], di)
                for cc in range(c + 1, k):
                    A[r][cc] = K.sub(A[r][cc], K.mul(f, A[c][cc]))
    return piv, True


def check_count(n, D, contacts, dropzero=False, svd=True):
    t0 = time.process_time()
    out = {'n': n}
    rec = Record(D)
    K = rec.K
    out['field_degree'] = K.degree
    # P: the record is a packing
    out['packing'] = check_packing(rec)
    t_pack = time.process_time()
    # R: rows
    cl = classify_rows(rec, contacts['load_bearing'])
    rows = cl['rows']
    pair_of = {}
    for p in cl['pairs']:
        pair_of[p[0]] = p
        pair_of[p[1]] = p

    def build(rows):
        lb = sorted({r[1] for r in rows} | {r[3] for r in rows if r[0] == 'C'})
        var = {}
        for i in lb:
            for key in ('x', 'y', 't'):
                var[(key, i)] = len(var)
        var['S'] = len(var)
        return lb, var

    lb, var = build(rows)
    N = len(var)
    sv = var['S']
    L0 = [row_grad(rec, r, var) for r in rows]
    dropped_zero = []
    if dropzero:
        zero = forced_zero_rows(rec, rows, L0, N, sv)
        zrows = {rows[a] for a in zero}
        for r in list(zrows):
            if r in pair_of:
                zrows |= set(pair_of[r])
        dropped_zero = sorted(zrows, key=str)
        rows = [r for r in rows if r not in zrows]
        cl['pairs'] = [p for p in cl['pairs'] if p[0] not in zrows]
        lb, var = build(rows)
        N = len(var)
        sv = var['S']
        L0 = [row_grad(rec, r, var) for r in rows]
    m = len(rows)
    out.update(rows=m, walls=sum(1 for r in rows if r[0] == 'W'),
               interior=sum(1 for r in rows if r[0] == 'C') - 2 * len(cl['pairs']),
               side_end_rows=2 * len(cl['pairs']), lone_side_end=len(cl['lone']),
               beyond=len(cl['beyond']), dropped_zero=len(dropped_zero),
               load_bearing=len(lb), variables=N, margin=cl['margin'])
    out['row_set'] = sorted([list(r) for r in rows], key=str)
    # flat family F: null space of the position columns
    pos = [var[(k, i)] for i in lb for k in ('x', 'y')]
    posset = set(pos)
    pidx = {c: k for k, c in enumerate(pos)}
    Lpos = [{pidx[c]: v for c, v in r.items() if c in posset} for r in L0]
    ech_pos = Echelon(K, Lpos, len(pos))
    ech_pos.check_echelon()
    Fb = [{pos[c]: v for c, v in b.items()} for b in ech_pos.nullspace()]
    for b in Fb:
        assert all(K.is_zero(x) for x in matvec(K, L0, b)), 'a flat direction is not in null L0'
    f = len(Fb)
    moving = sorted({lb[c // 3] for b in Fb for c in b})
    # null L0
    ech = Echelon(K, L0, N)
    ech.check_echelon()
    Nb = ech.nullspace()
    for w in Nb:
        assert all(K.is_zero(x) for x in matvec(K, L0, w)), 'a null vector does not verify'
    r0 = ech.rank
    out.update(rank_L0=r0, dim_null=len(Nb), dim_F=f, moving_squares=moving)
    if svd:
        import numpy as np
        Ln = np.zeros((m, N))
        for a, r in enumerate(L0):
            for c, v in r.items():
                Ln[a, c] = K.to_float(v)
        sing = np.linalg.svd(Ln, compute_uv=False)
        sing = np.r_[sing, np.zeros(max(0, N - len(sing)))]
        tol = 1e-9 * max(1.0, sing[0])
        out['svd_nullity'] = int(np.sum(sing < tol))
        out['svd_gap'] = [float(sing[r0 - 1]) if r0 > 0 else None, float(sing[r0]) if r0 < len(sing) else 0.0]
    # W': complement of F in null L0 (null vectors independent of F and each other)
    sel = Echelon(K, [dict(b) for b in Fb] + [dict(w) for w in Nb], N)
    assert sum(1 for k in range(f) if sel.log[k][1] is not None) == f, 'F basis dependent'
    Wb = [Nb[k - f] for k in range(f, f + len(Nb)) if sel.log[k][1] is not None]
    dW = len(Wb)
    assert f + dW == len(Nb), 'F + W does not span null L0'
    out['dim_W'] = dW
    # M: multipliers
    lam, why, tstar = multipliers(rec, rows, L0, N, sv)
    out['lp_maxmin'] = tstar
    if lam is None:
        out.update(valid=False, reason=why, cpu_seconds=round(time.process_time() - t0, 2))
        return out
    out['lambda_min'] = min(K.to_float(lam[a]) for a in range(m))
    # S-components of null vectors vanish (e_S = L0^T lambda*)
    for w in Nb:
        assert K.is_zero(w.get(sv, K.zero)), 'a null vector has a nonzero S component'
    # slips: t_rk = (J n) . (b_k[j] - b_k[i]) for C rows; zero for wall rows
    slips = []
    for r in rows:
        if r[0] == 'W':
            slips.append([K.zero] * f)
            continue
        _, j, a, i, k = r
        n_ = rec.normal(i, k)
        jn = J(n_, K)
        row = []
        for b in Fb:
            dxj, dyj = b.get(var[('x', j)], K.zero), b.get(var[('y', j)], K.zero)
            dxi, dyi = b.get(var[('x', i)], K.zero), b.get(var[('y', i)], K.zero)
            rx, ry = K.sub(dxj, dxi), K.sub(dyj, dyi)
            assert K.is_zero(K.add(K.mul(n_[0], rx), K.mul(n_[1], ry))), 'flat direction moves a row normally'
            row.append(K.add(K.mul(jn[0], rx), K.mul(jn[1], ry)))
        slips.append(row)
    side_end_set = {x for p in cl['pairs'] for x in p}
    out['side_end_rows_slipping'] = sum(1 for a, r in enumerate(rows)
                                        if r in side_end_set and any(not K.is_zero(x) for x in slips[a]))
    # A_k by its definition (L at shifted centres minus L0), against the slip formula
    for k, b in enumerate(Fb[:3]):
        Xs = [K.add(rec.X[i], b.get(var[('x', i)], K.zero)) if ('x', i) in var else rec.X[i] for i in range(rec.n)]
        Ys = [K.add(rec.Y[i], b.get(var[('y', i)], K.zero)) if ('y', i) in var else rec.Y[i] for i in range(rec.n)]
        for a, r in enumerate(rows):
            g1 = row_grad(rec, r, var, Xs, Ys)
            diff = {c: K.sub(g1.get(c, K.zero), L0[a].get(c, K.zero)) for c in set(g1) | set(L0[a])}
            diff = {c: v for c, v in diff.items() if not K.is_zero(v)}
            want = {} if r[0] == 'W' or K.is_zero(slips[a][k]) else {var[('t', r[3])]: slips[a][k]}
            assert diff == want, f'A_k of row {r} disagrees with the slip formula'
    # A: hypothesis 2 lifts
    theta_slip = sorted({var[('t', r[3])] for a, r in enumerate(rows)
                         if r[0] == 'C' and any(not K.is_zero(x) for x in slips[a])})
    out['theta_slip'] = len(theta_slip)
    lifts = 0
    if dW:
        banned = set(theta_slip) | {sv}
        keep = [c for c in range(N) if c not in banned]
        kidx = {c: k for k, c in enumerate(keep)}
        Lk = [{kidx[c]: v for c, v in r.items() if c in kidx} for r in L0]
        lift_ech = Echelon(K, Lk, len(keep))
        for w in Wb:
            vks = []
            for k in range(f):
                rhs = []
                for a, r in enumerate(rows):
                    if r[0] == 'C' and not K.is_zero(slips[a][k]):
                        rhs.append(K.neg(K.mul(slips[a][k], w.get(var[('t', r[3])], K.zero))))
                    else:
                        rhs.append(K.zero)
                if all(K.is_zero(x) for x in rhs):
                    vks.append({})
                    continue
                sol = lift_ech.solve(rhs)
                if sol is None:
                    out.update(valid=False, reason='no affine lift for a null vector (hypothesis 2 certificate)',
                               cpu_seconds=round(time.process_time() - t0, 2))
                    return out
                vks.append({keep[c]: v for c, v in sol.items()})
                lifts += 1
            # verify L(phi) (w + sum phi_k v_k) = 0 identically, from the definitions
            assert all(K.is_zero(x) for x in matvec(K, L0, w))
            Aw = [[K.mul(slips[a][k], w.get(var[('t', r[3])], K.zero)) if r[0] == 'C' else K.zero
                   for a, r in enumerate(rows)] for k in range(f)]
            for k in range(f):
                lv = matvec(K, L0, vks[k])
                assert all(K.is_zero(K.add(x, y)) for x, y in zip(lv, Aw[k])), 'L0 v_k + A_k w != 0'
                assert K.is_zero(vks[k].get(sv, K.zero)), 'a lift has a nonzero S component'
            for k in range(f):
                for l in range(k, f):
                    for a, r in enumerate(rows):
                        if r[0] != 'C':
                            continue
                        ti = var[('t', r[3])]
                        x = K.add(K.mul(slips[a][k], vks[l].get(ti, K.zero)),
                                  K.mul(slips[a][l], vks[k].get(ti, K.zero)))
                        assert K.is_zero(x), 'A_k v_l + A_l v_k != 0'
    out['lifts_solved'] = lifts
    # H: Lagrangian Hessian on W', and its F x W' block
    H = {}
    for a, r in enumerate(rows):
        for (c1, c2), val in row_hess(rec, r, var).items():
            H[(c1, c2)] = K.sub(H.get((c1, c2), K.zero), K.mul(lam[a], val))
    H = {k_: v for k_, v in H.items() if not K.is_zero(v)}
    assert not any(c1 in posset and c2 in posset for (c1, c2) in H), 'a position-position Hessian entry'

    def form(u, v):
        acc = K.zero
        for (c1, c2), h in H.items():
            x1, y2 = u.get(c1), v.get(c2)
            if x1 is not None and y2 is not None:
                acc = K.add(acc, K.mul(K.mul(x1, h), y2))
            if c1 != c2:
                x2, y1 = u.get(c2), v.get(c1)
                if x2 is not None and y1 is not None:
                    acc = K.add(acc, K.mul(K.mul(x2, h), y1))
        return acc

    for b in Fb:
        for w in Wb:
            assert K.is_zero(form(b, w)), 'the F x W block of the Hessian does not vanish'
    Q = [[form(Wb[x], Wb[y]) for y in range(dW)] for x in range(dW)]
    piv, pd = ldl_pivots(K, Q)
    minors, acc = [], K.one
    for d in piv:
        acc = K.mul(acc, d)
        minors.append(K.to_float(acc))
    out['hessian_pivots'] = [K.to_float(d) for d in piv]
    out['hessian_minors_this_basis'] = minors
    if not pd:
        out.update(valid=False, reason='reduced Hessian on W not positive definite',
                   cpu_seconds=round(time.process_time() - t0, 2))
        return out
    out.update(valid=True, reason=None, dropped_zero_rows=[list(r) for r in dropped_zero],
               cpu_seconds=round(time.process_time() - t0, 2), cpu_seconds_packing=round(t_pack - t0, 2))
    if isinstance(K, NumberField):
        out['t_refinements'] = K.refinements
    return out


def canonical_sha256(obj):
    import hashlib
    return hashlib.sha256(json.dumps(obj, separators=(',', ':')).encode()).hexdigest()


def main():
    import hashlib
    import platform
    ap = argparse.ArgumentParser()
    ap.add_argument('--minpoly-dir', required=True)
    ap.add_argument('--archive', required=True)
    ap.add_argument('--dropzero', default='')
    ap.add_argument('--out', default=None)
    ap.add_argument('--no-svd', action='store_true')
    ap.add_argument('counts', nargs='+', type=int)
    a = ap.parse_args()
    dz = {int(x) for x in a.dropzero.split(',') if x}
    me = hashlib.sha256(open(os.path.abspath(__file__), 'rb').read()).hexdigest()
    import numpy
    import scipy
    env = {'python': platform.python_version(), 'numpy': numpy.__version__, 'scipy': scipy.__version__,
           'program_sha256': me}
    with tarfile.open(a.archive, 'r:zst') as tf:
        contacts, cdig = {}, {}
        for n in a.counts:
            raw = tf.extractfile(f'gradec-233/certs/n-{n}.contacts.json').read()
            contacts[n] = json.loads(raw)
            cdig[n] = hashlib.sha256(raw).hexdigest()
    fh = open(a.out, 'a') if a.out else None
    bad = 0
    for n in a.counts:
        p = os.path.join(a.minpoly_dir, f'n-{n}.minpoly.json')
        raw = open(p + '.gz', 'rb').read() if os.path.exists(p + '.gz') else open(p, 'rb').read()
        D = json.loads(gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw)
        try:
            res = check_count(n, D, contacts[n], dropzero=n in dz, svd=not a.no_svd)
        except Exception as e:                            # any failure refuses the count
            res = {'n': n, 'valid': False, 'reason': f'{type(e).__name__}: {e}'}
        res['input_sha256'] = {'minpoly': hashlib.sha256(raw).hexdigest(), 'contacts': cdig[n]}
        if 'row_set' in res:
            res['row_set_sha256'] = canonical_sha256(res.pop('row_set'))
        if 'moving_squares' in res:
            ms = res.pop('moving_squares')
            res['moving_squares_count'] = len(ms)
            res['moving_squares_sha256'] = canonical_sha256(ms)
        if res.get('dim_null') is not None and res.get('svd_nullity') is not None:
            res['svd_agrees'] = res['svd_nullity'] == res['dim_null']
        res['environment'] = env
        bad += not res.get('valid')
        print(json.dumps({k: v for k, v in res.items() if k not in ('environment', 'input_sha256', 'dropped_zero_rows')}),
              flush=True)
        if fh:
            fh.write(json.dumps(res, sort_keys=True) + '\n')
            fh.flush()
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
