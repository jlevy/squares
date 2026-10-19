#!/usr/bin/env python3
"""Exact-contact solver: approximate jammed packing of n unit squares  ->  nearby exact KKT point (high precision),
numerical optimality checks, and an exact rational certificate of s(n) <= S'.

  exactsolve.py in.txt [--dps 80] [--eps 1e-20] [--out DIR] [--algdeg 16] [--tol 1e-8] [-q]

Pipeline (see README.md):
  1. contacts: feature incidences (corner-on-side, corner-on-wall) with |gap| < tol at the input; pure vertex-vertex
     touches are set aside (disjunctive; verified by SAT afterwards).
  2. load-bearing set A = max-support solution of the jam-LP dual  (lambda >= 0, sum lambda_k grad g_k = grad S).
     Squares with no contact in A = rattlers / free squares.
  3. KKT system on A: g_B = 0 (B = independent subset of A), grad S = sum_B lambda_b grad g_b; flat directions frozen
     (variable dropped with its stationarity row).  Chord Newton: residuals in mpmath (dps digits), f64 Jacobian.
  4. verify: A \\ B and frozen stationarity rows hold; every pair/wall SAT-separated (margins); lambda > 0 over A (LP);
     reduced Hessian of the Lagrangian on null(J_A); first-order rigidity.  Free squares re-placed with a positive margin.
  5. certificate: scale by 1 + eps, round to rationals (t = tan(theta/2)), verify exactly (verify_cert.py).
  6. optional: integer relation (mpmath.findpoly) for S.
"""
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ.setdefault(_v, '1')
import sys, math, json, time, argparse, collections
from fractions import Fraction
import numpy as np
import scipy.linalg as sla
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
import mpmath
from mpmath import mp, mpf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geom import eval_contact, tangential, sat_gap, wall_gaps, describe, offset
import verify_cert

SQ2 = math.sqrt(2)
FORCE_KKT = False                                    # --force-kkt (prototype only; see run())


def log(*a):
    print(*a, flush=True)


# ----------------------------------------------------------------------------------------------------------- state
class Pack:
    """Configuration in mp precision; angles normalised to (-45, 45] degrees (a square is invariant under 90 deg)."""

    def __init__(self, n, S, X, Y, T):
        self.n, self.S, self.X, self.Y, self.T = n, S, list(X), list(Y), list(T)

    @staticmethod
    def load(path):
        L = [l.split() for l in open(path) if l.strip() and not l.startswith('#')]
        n, S = int(L[0][0]), mpf(L[0][1])
        X, Y, T = [], [], []
        for r in L[1:n + 1]:
            d = mpf(r[2])
            d = d - 90 * mpmath.floor((d + 45) / 90)
            if d <= -45:
                d += 90
            X.append(mpf(r[0])); Y.append(mpf(r[1])); T.append(d * mp.pi / 180)
        return Pack(n, S, X, Y, T)

    def copy(self):
        return Pack(self.n, self.S, self.X, self.Y, self.T)

    def trig(self):
        return [mpmath.cos(t) for t in self.T], [mpmath.sin(t) for t in self.T]

    def flt(self):
        X = [float(v) for v in self.X]; Y = [float(v) for v in self.Y]
        return X, Y, [math.cos(float(t)) for t in self.T], [math.sin(float(t)) for t in self.T], float(self.S)

    def get(self, v):
        if v == 3 * self.n:
            return self.S
        return (self.X, self.Y, self.T)[v % 3][v // 3]

    def add(self, v, d):
        if v == 3 * self.n:
            self.S += d
        else:
            (self.X, self.Y, self.T)[v % 3][v // 3] += d

    def save(self, path, digits=None):
        digits = digits or mp.dps
        with open(path, 'w') as f:
            f.write(f'{self.n} {mpmath.nstr(self.S, digits, strip_zeros=False)}\n')
            for x, y, t in zip(self.X, self.Y, self.T):
                f.write(f'{mpmath.nstr(x, digits)} {mpmath.nstr(y, digits)} {mpmath.nstr(t * 180 / mp.pi, digits)}\n')


def near_pairs(P, extra=1e-6):
    X, Y = [float(v) for v in P.X], [float(v) for v in P.Y]
    r2 = (SQ2 + extra) ** 2
    out = []
    for i in range(P.n):
        for j in range(i + 1, P.n):
            if (X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2 < r2:
                out.append((i, j))
    return out


# ------------------------------------------------------------------------------------------------- 1. contacts
def find_contacts(P, tol=1e-8, etol=1e-7, atol=0.0, use_vv=False, reach=1e-4):
    """Candidate active contacts (feature incidences) and pure vertex-vertex touches.
    Incidence: corner with |gap| < tol on a side line that separates the pair, projecting inside the side.
    atol > 0 adds "near side-side" incidences: for a pair (or a square and a wall) that already touches, every further
    corner within atol of the same separating line (or wall) -- a nearly parallel side whose angle has not converged
    in the f64 input (a corner at distance ~ angle error)."""
    X, Y, C, Sn, S = P.flt()
    H = 0.5
    cands, vv = [], []
    for i in range(P.n):
        wg = {}
        for a in range(4):
            ox, oy = offset(C[i], Sn[i], a, H)
            px, py = X[i] + ox, Y[i] + oy
            for w, g in (('L', px), ('R', S - px), ('B', py), ('T', S - py)):
                wg[(a, w)] = g
        touching = {w for (a, w), g in wg.items() if g < tol}
        for (a, w), g in wg.items():
            if g < tol or (w in touching and g < atol):
                cands.append(('W', i, a, w))
    for i, j in near_pairs(P):
        inc = []
        for own, oth in ((i, j), (j, i)):
            for k in range(4):
                gs = [eval_contact(('C', oth, a, own, k), X, Y, C, Sn, S, H, order=1)[0] for a in range(4)]
                if min(gs) < -max(tol, atol):
                    continue                   # line of side k does not separate (e.g. collinear sides of aligned squares)
                for a in range(4):
                    ct = ('C', oth, a, own, k)
                    g = gs[a]
                    if abs(g) < max(tol, atol):
                        tau = tangential(ct, X, Y, C, Sn, H)
                        if abs(tau) <= H + reach:       # a corner just past the end of the side is a corner-corner touch
                            inc.append((ct, abs(tau) > H - etol, abs(g) < tol, abs(tau) > H + etol))
        if not any(t for _, _, t, _ in inc):
            continue
        past = {ct for ct, _, _, p in inc if p}         # corners past the side end: only for classification
        inc = [(ct, e) for ct, e, t, _ in inc]
        lines = collections.Counter((ct[3], ct[4]) for ct, _ in inc)
        if all(e for _, e in inc) and max(lines.values()) < 2:
            vv.append((i, j))
            if use_vv:
                # corner-corner touch: keep the incidences on the best separating axis only (one branch of the
                # disjunction, as in rigid.py); verified by SAT afterwards
                best = max(((ct[3], ct[4]) for ct, _ in inc),
                           key=lambda ln: min(eval_contact(('C', i if ln[0] == j else j, a, ln[0], ln[1]), X, Y, C, Sn, S,
                                                           H, order=1)[0] for a in range(4)))
                cands += [ct for ct, _ in inc if (ct[3], ct[4]) == best]
        else:
            cands += [ct for ct, _ in inc if ct not in past]
    return cands, vv


def slack_separated(P, Eq, thr):
    """Pairs whose contacts in Eq are not binding: some side line NOT carrying one of the pair's incidences in Eq
    separates the pair with clearance > thr (every corner of the other square strictly outside).  Non-overlap is a
    disjunction over separating lines, so near such a point the pair imposes no constraint at all, and treating its
    incidences as constraints (as the KKT system does) can certify a point that is not a local minimum.  Typical case:
    two nearly parallel squares, corner of j on side k of i, while side k' of j clears every corner of i by ~1e-8.
    Returns {(i, j): (clearance, (own, k))} with i < j, evaluated in mp at P."""
    C, Sn = P.trig()
    H = mpf(1) / 2
    used = collections.defaultdict(set)
    for c in Eq:
        if c[0] == 'C':
            used[tuple(sorted((c[1], c[3])))].add((c[3], c[4]))
    out = {}
    for (i, j), lines in used.items():
        best = None
        for own, oth in ((i, j), (j, i)):
            for k in range(4):
                if (own, k) in lines:
                    continue
                g = min(eval_contact(('C', oth, a, own, k), P.X, P.Y, C, Sn, P.S, H, order=1)[0] for a in range(4))
                if best is None or g > best[0]:
                    best = (g, (own, k))
        if best is not None and best[0] > thr:
            out[(i, j)] = best
    return out


def jacobian(P, cts, flt=None):
    X, Y, C, Sn, S = flt or P.flt()
    rows, cols, vals, g = [], [], [], []
    for r, ct in enumerate(cts):
        gv, gr, _ = eval_contact(ct, X, Y, C, Sn, S, 0.5, order=1)
        g.append(gv)
        for v, d in gr:
            rows.append(r); cols.append(v); vals.append(d)
    J = coo_matrix((vals, (rows, cols)), shape=(len(cts), 3 * P.n + 1)).toarray()
    return J, np.array(g)


# ------------------------------------------------------------------------------------------ 2. load-bearing set
def max_support(J, tau0=1e-6):
    """lambda >= 0 with J^T lambda = e_S (to the smallest achievable tolerance), maximising the support."""
    K, m = J.shape
    e = np.zeros(m); e[-1] = 1.0
    opts = {'primal_feasibility_tolerance': 1e-10, 'dual_feasibility_tolerance': 1e-10}
    # (a) smallest residual  min eta  s.t. |J^T lam - e| <= eta
    Aub = np.block([[J.T, -np.ones((m, 1))], [-J.T, -np.ones((m, 1))]])
    bub = np.concatenate([e, -e])
    c = np.zeros(K + 1); c[-1] = 1
    r = linprog(c, A_ub=Aub, b_ub=bub, bounds=[(0, None)] * (K + 1), method='highs', options=opts)
    eta = max(r.x[-1], 0.0)
    eta1 = max(10 * eta, 1e-11)
    # (b) max sum t,  t <= lam,  0 <= t <= tau0
    Aub = np.block([[J.T, np.zeros((m, K))], [-J.T, np.zeros((m, K))], [-np.eye(K), np.eye(K)]])
    bub = np.concatenate([e + eta1, -e + eta1, np.zeros(K)])
    c = np.concatenate([np.zeros(K), -np.ones(K)])
    for _ in range(6):
        bub = np.concatenate([e + eta1, -e + eta1, np.zeros(K)])
        r2 = linprog(c, A_ub=Aub, b_ub=bub, bounds=[(0, None)] * K + [(0, tau0)] * K, method='highs', options=opts)
        if r2.x is not None:
            break
        eta1 *= 10                                       # HiGHS tolerance trouble: relax and retry
    lam, t = r2.x[:K], r2.x[K:]
    return lam, t > 0.01 * tau0, eta


def vv_branch_test(P, cands, vv, tol):
    """First-order jamming test that treats corner-corner touches exactly, as disjunctions.

    Near a corner-corner touch the two squares are disjoint iff one of the side lines through the touching corners
    separates them, so the feasible set is a union of branches.  MILP (HiGHS):  min dS  over first-order motions z,
    |z| <= 1, every smooth contact linearised (grad g . z >= 0), and for each corner-corner pair at least one candidate
    line whose touching corners all stay outside (big-M with a binary per line).  dS* < 0 => a first-order descent
    direction exists in some branch => the input is NOT a local minimum (a fixed-separating-axis squeeze
    jammed it).  dS* = 0 => first-order jammed in every branch.
    Returns (dS*, number of VV pairs, list of (pair, chosen line) where the descent uses a different line)."""
    from scipy.optimize import milp, LinearConstraint, Bounds
    X, Y, C, Sn, S = P.flt()
    H = 0.5
    nz = 3 * P.n + 1
    J, _ = jacobian(P, cands)
    rows, lo = [J], [np.zeros(len(cands))]
    vvlines = []
    for (i, j) in vv:
        lines = []
        for own, oth in ((i, j), (j, i)):
            for k in range(4):
                gs = [eval_contact(('C', oth, a, own, k), X, Y, C, Sn, S, H, order=1) for a in range(4)]
                if min(g[0] for g in gs) < -tol:
                    continue
                touch = [a for a in range(4) if abs(gs[a][0]) < tol]
                if touch:
                    lines.append(((own, k), [('C', oth, a, own, k) for a in touch], min(g[0] for g in gs)))
        if lines:
            vvlines.append(((i, j), lines))
    nb = sum(len(l) for _, l in vvlines)
    M = 10.0
    A_rows, lb = [], []
    Jfull = np.hstack([J, np.zeros((J.shape[0], nb))])
    A_rows.append(Jfull); lb.append(np.zeros(J.shape[0]))
    bcol = nz
    one_rows = []
    for (pair, lines) in vvlines:
        cols = []
        for (ln, cts, _) in lines:
            Jl, _ = jacobian(P, cts)
            blk = np.hstack([Jl, np.zeros((len(cts), nb))])
            blk[:, bcol] = -M                     # grad.z - M b >= -M   <=>  b = 1 enforces grad.z >= 0
            A_rows.append(blk); lb.append(-M * np.ones(len(cts)))
            cols.append(bcol)
            bcol += 1
        r = np.zeros(nz + nb); r[cols] = 1.0
        one_rows.append(r)
    A = np.vstack(A_rows + ([np.array(one_rows)] if one_rows else []))
    L = np.concatenate(lb + ([np.ones(len(one_rows))] if one_rows else []))
    c = np.zeros(nz + nb); c[nz - 1] = 1.0
    integrality = np.concatenate([np.zeros(nz), np.ones(nb)])
    bounds = Bounds(np.concatenate([-np.ones(nz), np.zeros(nb)]), np.concatenate([np.ones(nz), np.ones(nb)]))
    res = milp(c, constraints=LinearConstraint(A, L, np.inf), integrality=integrality, bounds=bounds,
               options={'time_limit': 300})
    if res.x is None:
        return None, len(vvlines), []
    switched = []
    bcol = nz
    for (pair, lines) in vvlines:
        best = max(range(len(lines)), key=lambda q: lines[q][2])
        chosen = [q for q in range(len(lines)) if res.x[bcol + q] > 0.5]
        if best not in chosen:
            switched.append((pair, [lines[q][0] for q in chosen]))
        bcol += len(lines)
    return float(res.fun), len(vvlines), switched


# ------------------------------------------------------------------------------------------------- 3. KKT solve
class Degenerate(RuntimeError):
    """Newton's Jacobian turned singular near convergence: the independent subset B chosen at the f64 input became
    dependent at the exact point (e.g. two near-parallel contacts).  run() re-chooses B at the current point."""


class KKT:
    def __init__(self, P, A):
        self.P, self.A = P, list(A)
        sqs = sorted({c[1] for c in A} | {c[3] for c in A if c[0] == 'C'})
        self.squares = sqs
        self.V = [3 * i + k for i in sqs for k in range(3)] + [3 * P.n]
        self.vS = 3 * P.n

    def polish(self, log_=log, maxit=None):
        """Gauss-Newton (minimum-norm) projection of the configuration onto {g_A = 0}, residuals in mp.  Removes the
        input noise before rank decisions; stagnation means the contact equations are inconsistent.  Residuals are
        scaled by their norm before the f64 solve (no underflow below 1e-308, so any dps works)."""
        maxit = maxit or 40 + max(0, mp.dps - 300) // 10
        P = self.P
        H = mpf(1) / 2
        hist = []
        # project onto an independent subset of the contacts (rank-revealing QR): at degenerate configurations
        # (redundant contacts that agree only to second order, e.g. the (7+sqrt7)/2 family) Gauss-Newton on all of A
        # stalls at ~(input error)^2.  The other contacts are checked after the KKT solve (redundant_max_residual).
        J0, _ = jacobian(P, self.A)
        Q, Rq, piv = sla.qr(J0[:, self.V].T, pivoting=True, mode='economic')
        dg = np.abs(np.diag(Rq))
        rk = int((dg > 1e-9 * dg[0]).sum()) if len(dg) else 0
        rows = sorted(piv[:rk].tolist())
        Ab = [self.A[r] for r in rows]
        for it in range(maxit):
            C, Sn = P.trig()
            g = [eval_contact(c, P.X, P.Y, C, Sn, P.S, H, order=1)[0] for c in Ab]
            nr = max(abs(x) for x in g)
            hist.append(float(nr)); self.polish_nr = nr
            if nr < mpf(10) ** (-(mp.dps - 15)) or (it > 4 and hist[-1] > 0.5 * hist[-4] and hist[-1] > 1e-300):
                break
            J, _ = jacobian(P, Ab)
            sc = nr if nr < mpf(10) ** -200 else 1                 # scale only where f64 would underflow
            d, *_ = np.linalg.lstsq(J[:, self.V], -np.array([float(x / sc) for x in g]), rcond=1e-12)
            for k, v in enumerate(self.V):
                P.add(v, mpf(float(d[k])) * sc)
        log_(f'  projection onto {len(Ab)} independent of {len(self.A)} contact equations: max |g| {hist[0]:.1e} -> '
             f'{hist[-1]:.1e} ({len(hist)} steps)')
        self.polish_hist = hist
        return hist[-1]

    def setup(self, lam0, log_=log):
        """Choose an independent subset B of A and frozen variables so that the KKT Jacobian is nonsingular."""
        P = self.P
        self.polish(log_)
        if self.polish_nr > mpf(10) ** (-(mp.dps // 2)):
            raise RuntimeError('contact equations inconsistent (projection stalls): the contact set is not that of a '
                               'nearby exact configuration')
        J, _ = jacobian(P, self.A)
        JV = J[:, self.V]
        # independent rows, preferring large lambda
        order = np.argsort(-lam0)
        Q, R, piv = sla.qr(JV[order].T, pivoting=True, mode='economic')
        d = np.abs(np.diag(R))
        rank = int((d > 1e-9 * d[0]).sum())
        self.B = sorted(order[piv[:rank]].tolist())
        self.frozen = []
        for _ in range(500):
            self.Vf = [v for v in self.V if v not in self.frozen]
            lam = self.init_lambda()
            K = self.jac(lam)
            s = sla.svdvals(K)
            if s[-1] > 1e-9 * s[0]:
                break
            _, _, Vt = sla.svd(K)
            N = Vt[s < 1e-9 * s[0]]                               # null basis (rows)
            _, _, piv = sla.qr(N, pivoting=True)
            mz = len(self.Vf)
            pv = piv[:N.shape[0]]
            self.frozen += [self.Vf[p] for p in pv if p < mz and self.Vf[p] != self.vS]
            drop = {self.B[p - mz] for p in pv if p >= mz}
            self.B = [b for b in self.B if b not in drop]
        self.lam = lam
        self.cond = s[0] / s[-1]
        log_(f'  KKT: |A| = {len(self.A)} contacts, independent |B| = {len(self.B)}, variables {len(self.V)} '
             f'({len(self.frozen)} frozen flat), system {K.shape[0]}x{K.shape[1]}, cond ~ {self.cond:.1e}')

    def init_lambda(self):
        J, _ = jacobian(self.P, [self.A[b] for b in self.B])
        JV = J[:, self.Vf]
        e = np.array([1.0 if v == self.vS else 0.0 for v in self.Vf])
        lam, *_ = np.linalg.lstsq(JV.T, e, rcond=None)
        return lam

    def jac(self, lam, flt=None):
        P = self.P
        X, Y, C, Sn, S = flt or P.flt()
        mz, mb = len(self.Vf), len(self.B)
        idx = {v: k for k, v in enumerate(self.Vf)}
        K = np.zeros((mz + mb, mz + mb))
        for r, b in enumerate(self.B):
            g, gr, he = eval_contact(self.A[b], X, Y, C, Sn, S, 0.5, order=2)
            for v, d in gr:
                if v in idx:
                    K[idx[v], mz + r] -= d
                    K[mz + r, idx[v]] += d
            for v, w, h in he:
                if v in idx and w in idx:
                    K[idx[v], idx[w]] -= lam[r] * h
                    if v != w:
                        K[idx[w], idx[v]] -= lam[r] * h
        return K

    def residual(self, lam):
        """mp residual: stationarity rows for all variables in V (frozen ones last) and g_b, b in B."""
        P = self.P
        C, Sn = P.trig()
        H = mpf(1) / 2
        st = {v: (mpf(1) if v == self.vS else mpf(0)) for v in self.V}
        gB = []
        for r, b in enumerate(self.B):
            g, gr, _ = eval_contact(self.A[b], P.X, P.Y, C, Sn, P.S, H, order=1)
            gB.append(g)
            for v, d in gr:
                st[v] -= lam[r] * d
        return st, gB

    def newton(self, tolF, maxit=None, log_=log):
        P = self.P
        maxit = maxit or 30 + mp.dps // 6                  # chord Newton gains >= ~10 digits per step
        lam = [mpf(float(l)) for l in self.lam]
        mz = len(self.Vf)
        hist = []
        for it in range(maxit):
            st, gB = self.residual(lam)
            F = [st[v] for v in self.Vf] + gB
            nr = max(abs(f) for f in F)
            hist.append(float(nr))
            if nr < tolF:
                break
            if it > 6 and hist[-1] > 1e3 * min(hist):
                raise RuntimeError(f'Newton diverging: residual history {hist}')
            K = self.jac(np.array([float(l) for l in lam]))
            if nr < 1e-8 and np.linalg.cond(K) > 1e13:
                self.lam_mp = lam
                self.newton_hist = hist
                raise Degenerate(f'KKT Jacobian singular near convergence (residual {float(nr):.1e})')
            sc = nr if nr < mpf(10) ** -200 else 1                 # scale only where f64 would underflow
            d = sla.lu_solve(sla.lu_factor(K), -np.array([float(f / sc) for f in F]))
            # backtracking: halve the step while the residual grows by more than 10x
            base = ([P.get(v) for v in self.Vf], list(lam))
            step = 1.0
            for _ in range(12):
                for k, v in enumerate(self.Vf):
                    P.add(v, base[0][k] + mpf(float(step * d[k])) * sc - P.get(v))
                lam = [base[1][r] + mpf(float(step * d[mz + r])) * sc for r in range(len(lam))]
                st2, gB2 = self.residual(lam)
                if max(abs(f) for f in [st2[v] for v in self.Vf] + gB2) < 10 * nr:
                    break
                step /= 2
        self.lam_mp = lam
        self.newton_hist = hist
        log_(f'  Newton: {len(hist)} residual evaluations, residual {hist[0]:.1e} -> {hist[-1]:.1e}'
             f'{"" if hist[-1] < tolF else "  !! NOT CONVERGED to the requested precision"}')
        return hist[-1] < tolF


# ------------------------------------------------------------------------------------------- 4. verification
def full_lambda_lp(P, A, V):
    """max t s.t. sum_A lambda_k grad g_k = e_S (rows V), lambda_k >= t (f64 at the solution)."""
    J, _ = jacobian(P, A)
    JV = J[:, V]
    K = len(A)
    e = np.zeros(len(V)); e[-1] = 1.0
    c = np.zeros(K + 1); c[-1] = -1
    Aub = np.hstack([-np.eye(K), np.ones((K, 1))])
    r = linprog(c, A_ub=Aub, b_ub=np.zeros(K), A_eq=np.hstack([JV.T, np.zeros((len(V), 1))]), b_eq=e,
                bounds=[(0, None)] * K + [(None, 1)], method='highs',
                options={'primal_feasibility_tolerance': 1e-10, 'dual_feasibility_tolerance': 1e-10})
    if r.status != 0:
        return None, None
    return r.x[-1], r.x[:K]


def second_order(P, A, lamA, V, squares, weak=()):
    """Second-order check at a KKT point.  Hessian of the Lagrangian H = -sum_A lambda_k hess g_k with a valid multiplier
    vector (lambda >= 0 on the load-bearing set A), reduced to T = null(J_A) (variables V).  Since every lambda_k > 0
    on A, the critical cone is T intersected with {grad g_w . d >= 0} for the weakly active contacts w (lambda = 0).
    Positive definite on T => strict local minimum (second-order sufficient condition).  For each negative eigenvector
    we test whether +d or -d respects the weak contacts to first order (=> second-order descent direction)."""
    X, Y, C, Sn, S = P.flt()
    idx = {v: k for k, v in enumerate(V)}
    J, _ = jacobian(P, A)
    JV = J[:, V]
    u, s, vt = sla.svd(JV)
    rank = int((s > 1e-10 * s[0]).sum())
    Z = vt[rank:].T                                           # basis of null(J_A)
    Hm = np.zeros((len(V), len(V)))
    for ct, lam in zip(A, lamA):
        _, _, he = eval_contact(ct, X, Y, C, Sn, S, 0.5, order=2)
        for v, w, h in he:
            if v not in idx or w not in idx:
                continue
            Hm[idx[v], idx[w]] -= lam * h
            if v != w:
                Hm[idx[w], idx[v]] -= lam * h
    res = {'rank_JA': rank, 'dim_null': Z.shape[1]}
    rigid1 = [i for i in squares if np.abs(Z[[idx[3 * i], idx[3 * i + 1], idx[3 * i + 2]]]).max(initial=0) < 1e-8]
    res['first_order_rigid'] = rigid1
    if Z.shape[1] == 0:
        res.update(eig_min=None, eig_min_nonzero=None, n_zero=0, n_neg=0, flat_squares=[], descent=[], status='rigid (null(J_A) = 0)')
        return res
    M = Z.T @ Hm @ Z
    ev, evec = np.linalg.eigh((M + M.T) / 2)
    scale = max(1.0, np.abs(ev).max())
    zero = np.abs(ev) < 1e-9 * scale
    neg = ev < -1e-9 * scale
    res['eig'] = ev[:6].tolist()
    res['eig_min'] = float(ev[0])
    res['eig_min_nonzero'] = float(ev[~zero].min()) if (~zero).any() else None
    res['eig_min_positive'] = float(ev[ev > 1e-9 * scale].min()) if (ev > 1e-9 * scale).any() else None
    res['n_zero'] = int(zero.sum())
    res['n_neg'] = int(neg.sum())
    modes = Z @ evec[:, zero]
    flat = set()
    for k in range(modes.shape[1]):
        m = modes[:, k]
        for i in squares:
            if np.abs(m[[idx[3 * i], idx[3 * i + 1], idx[3 * i + 2]]]).max() > 1e-6:
                flat.add(i)
    res['flat_squares'] = sorted(flat)
    res['_zero_modes'] = modes
    # negative curvature: feasible w.r.t. the weakly active contacts?
    Gw = None
    if weak:
        Jw, _ = jacobian(P, list(weak))
        Gw = Jw[:, V]
    desc = []
    W = Gw @ Z @ evec if Gw is not None else None          # weak-contact gradients in eigen-coordinates
    for k in np.where(neg)[0]:
        d = Z @ evec[:, k]
        movers = sorted({i for i in squares if np.abs(d[[idx[3 * i], idx[3 * i + 1], idx[3 * i + 2]]]).max() > 1e-3})
        ok, best_curv = None, None
        for sg in (1, -1):
            if W is None or (sg * W[:, k] >= -1e-9).all():
                ok, best_curv = sg, float(ev[k])
                break
            # convex QP: min sum_{j != k, ev_j >= 0} ev_j c_j^2  s.t.  W c >= 0, c_k = sg, c_j = 0 for other negative j
            from scipy.optimize import minimize
            free_j = [j for j in range(len(ev)) if j != k and not neg[j]]
            wpos = np.maximum(ev[free_j], 0)
            def full(cf):
                c = np.zeros(len(ev)); c[k] = sg; c[free_j] = cf
                return c
            r = minimize(lambda cf: float(wpos @ (cf * cf)), np.zeros(len(free_j)), jac=lambda cf: 2 * wpos * cf,
                         constraints=[{'type': 'ineq', 'fun': lambda cf: W @ full(cf), 'jac': lambda cf: W[:, free_j]}],
                         method='SLSQP', options={'maxiter': 500, 'ftol': 1e-14})
            if r.success and (W @ full(r.x) >= -1e-8).all():
                curv = float(ev[k] + r.fun)
                if best_curv is None or curv < best_curv:
                    best_curv = curv
                if curv < -1e-9 * scale:
                    ok = sg
                    d = Z @ evec @ full(r.x)
                    break
        # multipliers are not unique when contacts are redundant: the second-order necessary condition asks for
        # max over all valid lambda of d^T H_lambda d >= 0.  LP over Lambda = {lambda >= 0, J_A^T lambda = e_S}.
        maxcurv = None
        if ok:
            q = np.zeros(len(A))
            for r_, ct in enumerate(A):
                _, _, he = eval_contact(ct, X, Y, C, Sn, S, 0.5, order=2)
                for v, w, h in he:
                    if v in idx and w in idx:
                        q[r_] -= h * d[idx[v]] * d[idx[w]] * (1 if v == w else 2)
            e = np.zeros(len(V)); e[idx[3 * P.n]] = 1.0
            lp = linprog(-q, A_eq=JV.T, b_eq=e, bounds=[(0, None)] * len(A), method='highs')
            if lp.status == 0:
                maxcurv = float(-lp.fun) / float(d @ d)
        desc.append({'eig': float(ev[k]), 'feasible_sign': ok, 'cone_curvature': best_curv,
                     'max_curvature_over_multipliers': maxcurv, 'squares': movers})
    res['descent'] = desc
    if res['n_neg'] and any(x['feasible_sign'] and x['max_curvature_over_multipliers'] is not None
                            and x['max_curvature_over_multipliers'] < -1e-9 for x in desc):
        res['status'] = 'NOT a local minimum: second-order descent direction (negative for every multiplier)'
    elif res['n_neg'] and any(x['feasible_sign'] for x in desc):
        res['status'] = ('inconclusive: negative curvature in the critical cone for the chosen multiplier, '
                         'but some other valid multiplier makes it nonnegative')
    elif res['n_neg']:
        res['status'] = 'inconclusive: negative curvature blocked (first order) by weakly active contacts'
    elif res['n_zero']:
        res['status'] = f'PSD with {res["n_zero"]} zero modes (degenerate; strict only modulo these)'
    else:
        res['status'] = 'PD: strict local minimum (second-order sufficient)'
    return res


def probe_flat(P, A, V, modes, t=1e-3, log_=log):
    """Are the zero modes of the reduced Hessian realised by exact motions?  For each mode d: start at z + t d and
    project back onto {g_A = 0} (Gauss-Newton, mp residuals; S may move too, so that f64 rounding of the step cannot
    leave an unrepairable inconsistency between contacts that are redundant only given S).  An exact flat family
    gives convergence (residual <= 1e-30) with |dS| <= 1e-30 (<< t^4) and a correction O(t^2).
    Returns (#modes realised, worst final residual, worst correction / t^2, worst |dS|)."""
    H = mpf(1) / 2
    nreal, worst_res, worst_corr, worst_dS = 0, 0.0, 0.0, 0.0
    for k in range(modes.shape[1]):
        d = modes[:, k] / np.abs(modes[:, k]).max()
        for sg in (1, -1):
            Q = P.copy()
            for v, dv in zip(V, d):
                if v != 3 * P.n:
                    Q.add(v, mpf(float(sg * t * dv)))
            start = [Q.get(v) for v in V]
            nr = None
            for it in range(40):
                C, Sn = Q.trig()
                g = [eval_contact(c, Q.X, Q.Y, C, Sn, Q.S, H, order=1)[0] for c in A]
                nr = max(abs(x) for x in g)
                if nr < mpf(10) ** (-(mp.dps - 20)):
                    break
                J, _ = jacobian(Q, A)
                dz, *_ = np.linalg.lstsq(J[:, V], -np.array([float(x) for x in g]), rcond=1e-10)
                for v, dv in zip(V, dz):
                    Q.add(v, mpf(float(dv)))
            corr = max(float(abs(Q.get(v) - s0)) for v, s0 in zip(V, start)) / t ** 2
            dS = float(abs(Q.S - P.S))
            worst_res = max(worst_res, float(nr)); worst_corr = max(worst_corr, corr); worst_dS = max(worst_dS, dS)
            # f64 rounding of the step (~1e-19) can leave a (1e-19)^2 inconsistency between redundant contacts that
            # meet tangentially; a genuinely curved (non-flat) mode would leave ~t^3 = 1e-9 or move S by ~t^4 = 1e-12
            if nr < 1e-30 and corr < 1e3 and dS < 1e-30:
                nreal += 0.5
    return nreal, worst_res, worst_corr, worst_dS


def free_clearance(P, free):
    """mp clearance of each free square: min over its walls and its SAT gaps to every nearby square."""
    Cm, Snm = P.trig()
    H = mpf(1) / 2
    fs = set(free)
    cl = {i: min(wall_gaps(i, P.X, P.Y, Cm, Snm, P.S, H)) for i in free}
    for i, j in near_pairs(P, 0.1):
        if i in fs or j in fs:
            g = sat_gap(i, j, P.X, P.Y, Cm, Snm, H)
            for k in (i, j):
                if k in fs:
                    cl[k] = min(cl[k], g)
    return cl


def place_free(P, free, log_=log, rounds=10, cap=1e-6, R=1e-4):
    """Move free (non-load-bearing) squares so that each gets clearance >= cap if possible (iterated LP, load-bearing
    squares fixed).  LP: max sum_i m_i, m_i <= cap, every linearised gap involving free square i >= m_i.
    Returns {square: mp clearance}."""
    if not free:
        return {}
    H = 0.5
    fidx = {i: k for k, i in enumerate(free)}
    nf = len(free)
    nv = 3 * nf + nf
    cl = free_clearance(P, free)
    for rd in range(rounds):
        if min(cl.values()) >= cap * 0.5:
            break
        X, Y, C, Sn, S = P.flt()
        rows = []                                            # (dict var->coef, gap, squares it bounds)
        for i in free:
            for a in range(4):
                for w in 'LRBT':
                    g, gr, _ = eval_contact(('W', i, a, w), X, Y, C, Sn, S, H, order=1)
                    if g < 1e-3:
                        rows.append(({fidx[i] * 3 + v % 3: d for v, d in gr if v < 3 * P.n}, g, (i,)))
        for i, j in near_pairs(P, 0.1):
            if i not in fidx and j not in fidx:
                continue
            best = None
            for own, oth in ((i, j), (j, i)):
                for k in range(4):
                    gs = [eval_contact(('C', oth, a, own, k), X, Y, C, Sn, S, H, order=1) for a in range(4)]
                    m = min(g[0] for g in gs)
                    if best is None or m > best[0]:
                        best = (m, gs)
            if best[0] > 1e-3:
                continue
            for g, gr, _ in best[1]:
                if g < best[0] + 1e-3:
                    row = {}
                    for v, d in gr:
                        if v < 3 * P.n and v // 3 in fidx:
                            key = fidx[v // 3] * 3 + v % 3
                            row[key] = row.get(key, 0) + d
                    rows.append((row, g, tuple(k for k in (i, j) if k in fidx)))
        A, b = [], []
        for row, g, sqs in rows:
            for q in sqs:
                r = np.zeros(nv)
                for v, d in row.items():
                    r[v] = -d
                r[3 * nf + fidx[q]] = 1.0
                A.append(r); b.append(g)
        c = np.zeros(nv); c[3 * nf:] = -1
        res = linprog(c, A_ub=np.array(A), b_ub=np.array(b), bounds=[(-R, R)] * (3 * nf) + [(None, cap)] * nf,
                      method='highs')
        if res.status != 0:
            break
        old = (list(P.X), list(P.Y), list(P.T))
        for k, i in enumerate(free):
            P.X[i] += mpf(float(res.x[3 * k])); P.Y[i] += mpf(float(res.x[3 * k + 1])); P.T[i] += mpf(float(res.x[3 * k + 2]))
        new = free_clearance(P, free)
        if min(new.values()) < min(cl.values()) or sum(min(v, cap) for v in new.values()) < sum(min(v, cap) for v in cl.values()):
            P.X, P.Y, P.T = old
            R /= 4
        else:
            cl = new
    log_(f'  free squares re-placed: min clearance {mpmath.nstr(min(cl.values()), 3)}; '
         f'{sum(v < 1e-12 for v in cl.values())} with clearance < 1e-12')
    return cl


def clearances(P, A, vv):
    """mp SAT gaps for all near pairs and wall clearances, classified."""
    C, Sn = P.trig()
    H = mpf(1) / 2
    inA = {(min(c[1], c[3]), max(c[1], c[3])) for c in A if c[0] == 'C'}
    wallA = {c[1] for c in A if c[0] == 'W'}
    out = {'A_pairs': [], 'other_pairs': [], 'vv': [], 'walls_A': [], 'walls_other': []}
    vvs = {tuple(p) for p in vv}
    for i, j in near_pairs(P, 0.01):
        g = sat_gap(i, j, P.X, P.Y, C, Sn, H)
        key = 'A_pairs' if (i, j) in inA else ('vv' if (i, j) in vvs else 'other_pairs')
        out[key].append((g, i, j))
    for i in range(P.n):
        for w, g in zip('LRBT', wall_gaps(i, P.X, P.Y, C, Sn, P.S, H)):
            out['walls_A' if i in wallA else 'walls_other'].append((g, i, w))
    return out


# --------------------------------------------------------------------------------------------- 5. certificate
def certificate(P, eps, path, rdig=None):
    """Scale about the origin corner by 1 + eps, round to rationals, verify exactly; write the certificate file."""
    rdig = rdig or max(30, int(-mpmath.log10(eps)) + 15)
    f = 1 + eps
    den = 10 ** rdig

    def rat(v):
        return Fraction(int(mpmath.nint(v * den)), den)
    Sp = Fraction(int(mpmath.ceil(P.S * f * 10 ** (rdig - 5))), 10 ** (rdig - 5))
    rows = []
    for x, y, t in zip(P.X, P.Y, P.T):
        rows.append((rat(x * f), rat(y * f), rat(mpmath.tan(t / 2))))
    with open(path, 'w') as fh:
        fh.write('# exact certificate: unit squares, centre (x, y), rotation (c, s) = ((1-t^2)/(1+t^2), 2t/(1+t^2));'
                 ' check with verify_cert.py\n')
        fh.write(f'{P.n} {Sp}\n')
        for x, y, t in rows:
            fh.write(f'{x} {y} {t}\n')
    n, S2, sq = verify_cert.parse(path)
    ok, wall, pair = verify_cert.verify(n, S2, sq, verbose=False)
    return ok, Sp, wall, pair


# ---------------------------------------------------------------------------------------------- 6. algebraic
def identify(S, maxdeg, log_=log):
    """Integer polynomial with S as a root, degree <= maxdeg.  findpoly (PSLQ) accepts relations at ~eps^(3/4), which
    lets spurious relations through at high degree; we accept only if the relation is far from what precision alone
    would allow: (d+1) * log10(max coefficient) <= 0.6 * dps and |P(S)| <= 10^(-0.9 dps) * max coefficient."""
    import sympy
    dps = mp.dps
    for d in range(1, maxdeg + 1):
        mc = int(10 ** min(18, max(3, int(0.6 * dps / (d + 1)))))
        try:
            p = mpmath.findpoly(S, d, maxcoeff=mc, maxsteps=20000)
        except Exception:
            p = None
        if not p:
            continue
        big = max(abs(int(c)) for c in p)
        if abs(mpmath.polyval([int(c) for c in p], S)) > mpf(10) ** (-0.9 * dps) * big:
            continue
        x = sympy.Symbol('x')
        poly = sympy.Poly([int(c) for c in p], x)
        fac = sympy.factor_list(poly)[1]
        best = min(fac, key=lambda fp: abs(mpmath.polyval([int(c) for c in fp[0].all_coeffs()], S)))
        mpoly = best[0]
        return d, str(mpoly.as_expr()), mpoly.degree()
    return None


# ------------------------------------------------------------------------------------------------------- main
def run(path, dps=80, eps='1e-20', outdir=None, algdeg=0, tol=0, quiet=False, force=(), depth=0):
    """force: pairs (i, j) whose incidences (|g| < 1e-4 at the input, projecting onto the side) are added as equations: the active-set step after a
    solve whose flat motions closed a pair that was open (by < tol_ladder) at the input."""
    mp.dps = dps
    log_ = (lambda *a: None) if quiet else log
    t0 = time.time()
    P = Pack.load(path)
    S_in = P.S
    name = os.path.splitext(os.path.basename(path))[0]
    outdir = outdir or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
    os.makedirs(outdir, exist_ok=True)
    rep = {'input': path, 'n': P.n, 'S_input': mpmath.nstr(S_in, 17), 'dps': dps}
    log_(f'== {path}: n = {P.n}, S_in = {mpmath.nstr(S_in, 17)}')

    # contact tolerance: the smallest in the ladder for which the contacts admit an equilibrium (jam-LP dual residual
    # < 1e-8); f64 inputs repaired by scaling can leave real contacts open by up to ~1e-7
    # If none works, the angles of nearly parallel touching sides have not converged: add near side-side incidences
    # (atol ladder) at tol = 1e-7.
    def not_jammed(dS, nvv, why):
        rep.update(jam_residual=float(eta), status='not jammed', vv_milp_dS=dS, n_vv=nvv, S_exact=None,
                   cert_valid=None, why=why)
        log_(f'  corner-corner branch MILP on the input: min dS over first-order motions (|z| <= 1) = {dS:.3e} '
             f'({nvv} corner-corner touches as disjunctions)')
        log_('  => NOT a local minimum: ' + why + '  No exact solve attempted.')
        with open(os.path.join(outdir, name + '.json'), 'w') as fh:
            json.dump(rep, fh, indent=1, default=str)
        return rep, P, None

    ladder = [(t, 0.0) for t in ([tol] if tol else [1e-9, 1e-8, 3e-8, 1e-7, 3e-7, 1e-6])]
    # acceptance: dual residual < 1e-8; then a second pass at < 1e-7 (n ~ 250-300: f64 round-off alone reaches
    # ~1.5e-8).  Safe: the 80-digit Newton and checks below reject a wrong contact set.
    tol0 = tol
    for thr in (1e-8, 1e-7):
        for tol, atol in ladder:
            cands, vv = find_contacts(P, tol)
            if not cands:                                # nothing within tol (far from jammed): next rung
                eta = float('inf')
                continue
            J, g = jacobian(P, cands)
            lam, supp, eta = max_support(J)
            if eta < thr:
                break
        if eta < thr:
            break
    rep['jam_threshold'] = thr
    forced_kkt = False
    if FORCE_KKT and eta >= 1e-7:
        # --force-kkt (packer finish prototype, 10-08): skip the f64 jam test; take the max-support set of the rung with
        # the smallest equilibrium residual (contact tolerance up to 1e-3) and let Newton + the checks below decide.
        best = None
        for t2 in (1e-6, 1e-5, 1e-4, 1e-3):
            c2, vv2 = find_contacts(P, t2)
            if not c2:
                continue
            J2, g2 = jacobian(P, c2)
            l2, s2, e2 = max_support(J2)
            if best is None or e2 < best[0]:
                best = (e2, t2, c2, vv2, J2, g2, l2, s2)
            if e2 < 1e-8:
                break
        if best is not None:
            eta, tol, cands, vv, J, g, lam, supp = best
            atol = 0.0
            forced_kkt = True
            rep['forced_kkt'] = dict(tol=tol, eta=float(eta))
    if forced_kkt:
        use_vv = False
    elif eta >= 1e-7:
        log_(f'  !! no contact tolerance in the ladder gives an equilibrium with smooth contacts (residual {eta:.1e})')
        c0, vv0 = find_contacts(P, 1e-6)
        dS, nvv, _ = vv_branch_test(P, c0, vv0, 1e-6)
        if dS is not None and dS < -1e-6:
            return not_jammed(dS, nvv, 'a first-order descent exists once corner-corner touches may slip along either '
                              'side (an optimizer that linearises each pair on one fixed separating axis can stall here).')
        # Jammed with corner-corner disjunctions but not with smooth contacts.  The MILP minimum over the union of
        # branches is >= 0, so every branch is jammed and (LP duality) has an equilibrium: take one branch (each
        # corner-corner touch on its best separating line) as equations.  The certificate below is checked exactly
        # whatever the branch; second-order statements are then for that branch.
        use_vv = False
        for tol in (1e-8, 1e-7, 1e-6):
            cands, vv = find_contacts(P, tol, use_vv=True)
            J, g = jacobian(P, cands)
            lam, supp, eta = max_support(J)
            if eta < 1e-8:
                use_vv = True
                atol = 0.0
                log_(f'  equilibrium with corner-corner touches on their best separating line (tol {tol:g})')
                break
        # else: "near side-side" incidences (nearly parallel touching sides whose angle has not converged in f64)
        if not use_vv:
            for atol in (1e-6, 1e-5, 1e-4, 1e-3, 3e-3):
                tol = 1e-7
                cands, vv = find_contacts(P, tol, atol=atol)
                J, g = jacobian(P, cands)
                lam, supp, eta = max_support(J)
                if eta < 1e-8:
                    break
        if eta >= 1e-8:
            return not_jammed(dS, nvv, 'no equilibrium with smooth contacts (not first-order jammed).')
    else:
        use_vv = False
    forced = []
    if force:
        fp = {tuple(sorted(p)) for p in force}
        for uv in (False, True):
            cw, _ = find_contacts(P, 1e-4, use_vv=uv)    # both ends of a near-parallel side-side contact
            forced = [c for c in cw if c[0] == 'C' and tuple(sorted((c[1], c[3]))) in fp and c not in cands]
            if {tuple(sorted((c[1], c[3]))) for c in forced} >= fp:
                break
        rep['forced_pairs'] = sorted(fp)
        log_(f'  active-set step: {len(forced)} incidences of pairs {sorted(fp)} added as equations')
    rep['contact_tol'] = tol
    rep['near_parallel_tol'] = atol
    rep['vertex_vertex_used'] = use_vv
    A = [c for c, s in zip(cands, supp) if s]
    lamA = lam[supp]
    load_sq = sorted({c[1] for c in A} | {c[3] for c in A if c[0] == 'C'})
    free = [i for i in range(P.n) if i not in load_sq]
    rep.update(n_candidates=len(cands), n_vv=len(vv), n_active=len(A), jam_residual=float(eta),
               load_bearing_squares=len(load_sq), free_squares=free)
    log_(f'  contacts: {len(cands)} candidate incidences (|gap| < {tol:g}{f", near side-side < {atol:g}" if atol else ""}{", corner-corner touches included (best axis)" if use_vv else ""}), {len(vv)} vertex-vertex touches set aside; '
         f'jam-LP dual residual {eta:.1e}; load-bearing set {len(A)} contacts on {len(load_sq)} squares; '
         f'free squares (rattlers / force-free): {free}')

    # Equations: the load-bearing set A plus "weakly active" candidates (touching within tol, force-free) among the
    # squares in the system -- kept closed (lambda solved, ~0), otherwise flat motions could open them into overlap.
    # Free squares that cannot be given a positive clearance (wedged, force-free) are promoted into the system.
    P0 = P.copy()
    promoted = []
    for attempt in range(8):
        P = P0.copy()
        ls = set(load_sq) | set(promoted)
        weakc = [c for c, s, g0 in zip(cands, supp, g) if not s and abs(g0) < tol and c[1] in ls and (c[0] == "W" or c[3] in ls)]
        Eq = A + weakc + forced
        kk = KKT(P, Eq)
        try:
            kk.setup(np.concatenate([lamA, np.zeros(len(weakc) + len(forced))]), log_)
            for resetup in range(4):
                try:
                    ok = kk.newton(mpf(10) ** (-(dps - 12)), log_=log_)
                    break
                except Degenerate as ex:
                    if resetup == 3:
                        raise
                    # re-choose the independent subset at the (now nearly exact) point, multipliers carried over
                    lam_full = np.zeros(len(Eq))
                    for r, b in enumerate(kk.B):
                        lam_full[b] = float(kk.lam_mp[r])
                    log_(f'  {ex}: re-choosing the independent contacts at the current point (round {resetup + 1})')
                    rep['kkt_resetups'] = resetup + 1
                    kk.setup(lam_full, log_)
        except (RuntimeError, ValueError, np.linalg.LinAlgError) as ex:
            log_(f'  !! KKT solve failed: {str(ex)[:200]}')
            rep.update(status='solve failed', S_exact=None, cert_valid=None, vv_milp_dS=None)
            with open(os.path.join(outdir, name + '.json'), 'w') as fh:
                json.dump(rep, fh, indent=1, default=str)
            return rep, P, None
        free = [i for i in range(P.n) if i not in ls]
        clear = place_free(P, free, log_)
        bad = [i for i in free if clear[i] < 1e-12]
        if not bad:
            break
        promoted += bad
        log_(f'  free squares {bad} cannot be given positive clearance: promoted into the KKT system; re-solving')
    rep.update(n_weak_equations=len(weakc), promoted=promoted, free_squares=free,
               free_clearance=min(clear.values()) if clear else None)
    rep['newton_converged'] = bool(ok)
    st, gB = kk.residual(kk.lam_mp)
    # checks of the dropped (redundant) contacts and frozen stationarity rows
    C, Sn = P.trig()
    H = mpf(1) / 2
    red = [abs(eval_contact(Eq[k], P.X, P.Y, C, Sn, P.S, H, order=1)[0]) for k in range(len(Eq)) if k not in kk.B]
    log_(f'  {len(weakc)} weakly active (force-free) contacts kept closed')
    fro = [abs(st[v]) for v in kk.frozen]
    rep['redundant_contacts'] = len(red)
    rep['redundant_max_residual'] = float(max(red, default=0))
    rep['frozen_vars'] = len(kk.frozen)
    rep['frozen_max_stationarity'] = float(max(fro, default=0))
    log_(f'  redundant contacts ({len(red)}): max |g| = {rep["redundant_max_residual"]:.1e}; frozen flat variables '
         f'({len(kk.frozen)}): max |dL/dv| = {rep["frozen_max_stationarity"]:.1e}')
    rep['S_exact'] = mpmath.nstr(P.S, dps - 15)
    log_(f'  S = {mpmath.nstr(P.S, min(dps - 15, 70))}   (input {mpmath.nstr(S_in, 17)}, shift {mpmath.nstr(P.S - S_in, 3)})')

    # contacts that are closed at the exact point but were not candidates at the input (e.g. a corner 1e-7 off its
    # side because of a noisy tilt): added to the closed set, so that the force and second-order analyses see them
    c2, vv2 = find_contacts(P, 1e-12)
    eqs = set(Eq)
    C, Sn = P.trig()
    newc = [c for c in c2 if c not in eqs
            and abs(eval_contact(c, P.X, P.Y, C, Sn, P.S, H, order=1)[0]) < mpf(10) ** (-(dps - 20))]
    if newc:
        log_(f'  {len(newc)} contacts closed at the exact point but not at the input: '
             f'{", ".join(describe(c) for c in newc[:6])}{" ..." if len(newc) > 6 else ""}')
        Eq = Eq + newc
    vv = sorted(set(map(tuple, vv)) | set(map(tuple, vv2)))
    rep['n_new_contacts_exact'] = len(newc)
    # pairs separated with positive clearance by a side line other than the one their incidences use: the incidences
    # are not constraints of the true (disjunctive) problem here.  Release them from every analysis below; if the rest
    # cannot hold the load, the point is not a local minimum (10-08: four "certified" s(110) census minima were such
    # branch artifacts, e.g. a corner on side 1 of square i while side 3 of square j cleared i by 1.6e-8).
    rel = slack_separated(P, Eq, mpf(10) ** (-(dps - 15)))
    rep['released_pairs'] = [[i, j, float(g), list(ln)] for (i, j), (g, ln) in sorted(rel.items())]
    if rel:
        log_(f'  {len(rel)} touching pair(s) also separated with positive clearance by another side line: '
             f'{[(p, mpmath.nstr(g, 3)) for p, (g, _) in sorted(rel.items())]}; their incidences are not binding '
             f'constraints here and are released')
        relp = set(rel)
        notrel = lambda c: c[0] != 'C' or tuple(sorted((c[1], c[3]))) not in relp
        Eq = [c for c in Eq if notrel(c)]
        c2 = [c for c in c2 if notrel(c)]
        vv2 = [p for p in vv2 if tuple(sorted(p)) not in relp]
        vv = [p for p in vv if tuple(sorted(p)) not in relp]
    # multipliers: re-identify the load-bearing set at the exact point (max support over all closed contacts)
    Jq, _ = jacobian(P, Eq)
    lamq, suppq, etaq = max_support(Jq)
    A2 = [c for c, sp in zip(Eq, suppq) if sp]
    if set(A2) != set(A):
        log_(f'  load-bearing set at the exact point: {len(A2)} contacts (was {len(A)} at the input); '
             f'{len(set(A) - set(A2))} of the input support carry no force')
    A = A2
    weak_eq = [c for c in Eq if c not in set(A)]
    load_sq = sorted({c[1] for c in A} | {c[3] for c in A if c[0] == 'C'})
    VA = [3 * i + k for i in load_sq for k in range(3)] + [3 * P.n]
    tmin, lam_full = full_lambda_lp(P, A, VA)
    rep['n_active_exact'] = len(A)
    rep['load_bearing_squares_exact'] = len(load_sq)
    rep['lambda_A_maxmin'] = tmin
    rep['equilibrium_residual_exact'] = float(etaq)
    log_(f'  multipliers: equilibrium residual {etaq:.1e}; best strictly positive choice over the {len(A)} '
         f'load-bearing contacts: min lambda = {tmin if tmin is None else f"{tmin:.3e}"}, '
         f'max {max(lam_full) if lam_full is not None else float("nan"):.3e}')
    if lam_full is None:
        lam_full = np.zeros(len(A))
        log_('  !! no multiplier lambda >= 0 balances the load at the exact point: NOT a KKT point of min S')

    so = second_order(P, A, lam_full, VA, load_sq, weak_eq)
    zm = so.pop('_zero_modes', None)
    if zm is not None and zm.shape[1]:
        nre, wr, wc, wds = probe_flat(P, A, VA, zm)
        so['zero_modes_realised'] = nre
        so['zero_mode_probe'] = {'t': 1e-3, 'worst_residual': wr, 'worst_correction_over_t2': wc, 'worst_dS': wds}
        log_(f'  zero modes: {nre:g} of {zm.shape[1]} realised by exact motions at fixed S (step 1e-3 both ways, '
             f'projection residual <= {wr:.1e}, correction <= {wc:.2g} t^2, |dS| <= {wds:.1e})')
        if so['n_neg'] == 0 and nre == zm.shape[1]:
            so['status'] = (f'local minimum of S, strict modulo {zm.shape[1]} exact flat motions (PD on the rest of '
                            f'null(J_A)); the configuration is not isolated')
    rep['second_order'] = so
    log_(f'  second order: rank J_A = {so["rank_JA"]}, dim null(J_A) = {so["dim_null"]}; reduced Hessian: #neg '
         f'{so["n_neg"]}, #zero {so["n_zero"]}, min eig {so["eig_min"]}, min positive {so.get("eig_min_positive")}')
    log_(f'    => {so["status"]}')
    for dd in so['descent'][:5]:
        log_(f'    negative mode eig {dd["eig"]:.3e}: feasible sign {dd["feasible_sign"]}, best curvature in the critical cone {dd["cone_curvature"]}, max over multipliers {dd["max_curvature_over_multipliers"]}, squares {dd["squares"]}')
    log_(f'  first-order rigid squares: {len(so["first_order_rigid"])} of {len(load_sq)} load-bearing; squares in zero '
         f'modes: {so["flat_squares"]}')
    # corner-corner touches at the exact point: first-order jamming in every branch of the disjunction?
    dS, nvv, _ = vv_branch_test(P, c2, vv2, 1e-12)
    rep['vv_milp_dS'] = dS
    rep['n_vv_exact'] = nvv
    log_(f'  corner-corner branches ({nvv} touches as disjunctions, MILP): min first-order dS = {dS:.2e} '
         f'=> {"jammed in every branch" if dS is not None and dS > -1e-9 else "DESCENT in some branch: not a local minimum"}')
    # the verdict must reflect both first-order tests (census_exact.classify reads only so['status'])
    why = []
    if etaq > 1e-8:                     # (full_lambda_lp's maxmin LP fails on some healthy points; the residual is the test)
        why.append(f'no multiplier lambda >= 0 balances the load at the exact point (residual {etaq:.1e})')
    if dS is not None and dS < -1e-9:
        why.append(f'first-order descent in the corner-corner branch MILP (dS = {dS:.2e})')
    if why:
        so['status_before_first_order'] = so.get('status')
        so['status'] = 'NOT a local minimum: ' + '; '.join(why) + (' (after releasing slack-separated pairs)' if rel else '')
        log_(f'    => {so["status"]}')
    cl = clearances(P, A, vv)
    small = mpf(10) ** (-(dps - 15))
    def mn(lst):
        return min(lst, key=lambda r: r[0]) if lst else None
    a_min = mn(cl['A_pairs']); o_min = mn(cl['other_pairs']); v_min = mn(cl['vv'])
    wA = mn(cl['walls_A']); wo = mn(cl['walls_other'])
    weak = [r for r in cl['other_pairs'] + cl['vv'] + cl['walls_other'] if abs(r[0]) < 1e-12]
    viol = [r for k in cl for r in cl[k] if r[0] < -small]
    rep['min_gap_active_pairs'] = float(a_min[0]) if a_min else None
    rep['min_gap_other_pairs'] = float(o_min[0]) if o_min else None
    rep['min_gap_vv'] = float(v_min[0]) if v_min else None
    rep['min_wall_other'] = float(wo[0]) if wo else None
    rep['weakly_active'] = [str(r[1:]) for r in weak]
    rep['violations'] = [(float(r[0]),) + tuple(r[1:]) for r in viol]
    log_(f'  feasibility (mp SAT): active pairs min gap {mpmath.nstr(a_min[0], 3) if a_min else "-"}; '
         f'non-active pairs min {mpmath.nstr(o_min[0], 3) if o_min else "-"} {o_min[1:] if o_min else ""}; '
         f'vertex-vertex min {mpmath.nstr(v_min[0], 3) if v_min else "-"}; non-active walls min {mpmath.nstr(wo[0], 3) if wo else "-"}')
    sep = [r for k in cl for r in cl[k] if r[0] >= 1e-12]
    msep = min(sep, key=lambda r: r[0]) if sep else None
    rep['margin_separated'] = float(msep[0]) if msep else None
    rep['n_touching_pairs_walls'] = sum(1 for k in cl for r in cl[k] if abs(r[0]) < 1e-12)
    log_(f'  {rep["n_touching_pairs_walls"]} pairs/walls touch (|SAT gap| < 1e-12; load-bearing, weakly active or '
         f'corner-corner); every other pair/wall is separated by >= {mpmath.nstr(msep[0], 3) if msep else "-"} '
         f'{msep[1:] if msep else ""}')
    if weak:
        log_(f'  weakly active (|gap| < 1e-12, not load-bearing): '
             f'{[(mpmath.nstr(r[0], 2),) + tuple(r[1:]) for r in weak[:12]]}{" ..." if len(weak) > 12 else ""}')
    if viol:
        log_(f'  !! VIOLATIONS (gap < -1e-{dps - 15}): {[(mpmath.nstr(r[0], 3),) + tuple(r[1:]) for r in viol[:10]]}')

    P.save(os.path.join(outdir, name + '.exact.txt'), dps - 10)
    # contact structure, for minpoly.py (exact field configuration): every closed contact used as an equation,
    # the load-bearing subset, corner-corner touches (not equations), free squares
    with open(os.path.join(outdir, name + '.contacts.json'), 'w') as fh:
        json.dump({'n': P.n, 'S': mpmath.nstr(P.S, dps - 10), 'equations': [list(c) for c in Eq],
                   'load_bearing': [list(c) for c in A], 'vv': [list(p) for p in vv], 'free': free,
                   'frozen_vars': [int(v) for v in kk.frozen], 'first_order_rigid': so.get('first_order_rigid'),
                   'dim_null': so.get('dim_null'), 'rank_JA': so.get('rank_JA')}, fh)
    okc, Sp, wall, pair = certificate(P, mpf(eps), os.path.join(outdir, name + '.cert'))
    rep['cert_valid'] = ok_c = bool(okc)
    rep['S_cert'] = str(Sp)
    rep['S_cert_decimal'] = mpmath.nstr(mpf(Sp.numerator) / Sp.denominator, 40)
    rep['cert_min_wall'] = float(wall[0]); rep['cert_min_pair'] = float(pair[0]) if pair else None
    log_(f'  certificate ({name}.cert): exact check {"VALID" if okc else "INVALID"}; S\' = {rep["S_cert_decimal"]} '
         f'(S\' - S = {mpmath.nstr(mpf(Sp.numerator) / Sp.denominator - P.S, 3)}); exact min wall {float(wall[0]):.2e}, '
         f'min pair {float(pair[0]) if pair else float("nan"):.2e}')
    if algdeg:
        r = identify(P.S, algdeg, log_)
        rep['algebraic'] = r if rep.get('newton_converged') else None
        log_(f'  algebraic: {"minimal polynomial (deg %d): %s" % (r[2], r[1]) if r else "no polynomial of degree <= %d found" % algdeg}')
    rep['seconds'] = round(time.time() - t0, 1)
    with open(os.path.join(outdir, name + '.json'), 'w') as fh:
        json.dump(rep, fh, indent=1, default=str)
    log_(f'  done in {rep["seconds"]} s')
    vp = [tuple(r[1:3]) for r in viol if len(r) >= 3 and all(isinstance(v, int) for v in r[1:3])]
    if vp and not ok_c and depth < 4:
        log_(f'  => pairs {vp} closed during the solve: re-solving with them as equations (active-set step {depth + 1})')
        return run(path, dps, eps, outdir, algdeg, tol, quiet, tuple(force) + tuple(vp), depth + 1)
    return rep, P, kk


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('input')
    ap.add_argument('--dps', type=int, default=80)
    ap.add_argument('--eps', default='1e-20')
    ap.add_argument('--out')
    ap.add_argument('--algdeg', type=int, default=0)
    ap.add_argument('--tol', type=float, default=0, help='contact tolerance (default: automatic ladder)')
    ap.add_argument('-q', action='store_true')
    ap.add_argument('--force-kkt', action='store_true', help='prototype: skip the f64 jam test, go straight to the KKT solve')
    a = ap.parse_args()
    FORCE_KKT = a.force_kkt
    run(a.input, a.dps, a.eps, a.out, a.algdeg, a.tol, a.q)
