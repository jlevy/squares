"""KKT refinement for NON-rigid optima (contacts alone do not pin s; s is fixed by stationarity).

Unknowns: geometry z and multipliers lam for every active equation g_k.
Equations:  g_k(z) = 0,   e_s - sum_k lam_k grad g_k(z) = 0.
Solved by minimum-norm Gauss-Newton in arb with analytic second derivatives.
"""
import math, sys, time, pickle
import numpy as np
from flint import arb, arb_mat, ctx
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import exactform as E


def eval_full(eqs, z, n):
    """values, gradients (dict), Hessians (dict of (i,j)->v, symmetric, upper incl. diag)."""
    X = lambda k: 2 * k
    Y = lambda k: 2 * k + 1
    T = lambda k: 2 * n + k
    S = 3 * n
    vals, grads, hess = [], [], []
    for e in eqs:
        H = {}
        if e[0] == "pair":
            _, i, j, o, ot, w, SG, sc, ss = e
            co, so = z[T(o)].cos(), z[T(o)].sin()
            if w == 0:
                a, da = (co, so), (-so, co)
            else:
                a, da = (-so, co), (-co, -so)
            dx, dy = z[X(i)] - z[X(j)], z[Y(i)] - z[Y(j)]
            d = z[T(ot)] - z[T(o)]
            cd, sd = d.cos(), d.sin()
            f = sc * cd + ss * sd
            fp = -sc * sd + ss * cd                      # f'(d)
            g = SG * (dx * a[0] + dy * a[1]) - arb(0.5) - f / 2
            gr = {X(i): SG * a[0], Y(i): SG * a[1], X(j): -SG * a[0], Y(j): -SG * a[1]}
            gr[T(o)] = SG * (dx * da[0] + dy * da[1]) + fp / 2
            gr[T(ot)] = -fp / 2
            # second derivatives
            H[(X(i), T(o))] = SG * da[0]; H[(Y(i), T(o))] = SG * da[1]
            H[(X(j), T(o))] = -SG * da[0]; H[(Y(j), T(o))] = -SG * da[1]
            H[(T(o), T(o))] = -SG * (dx * a[0] + dy * a[1]) + f / 2      # a'' = -a ; d2(-f/2)/dto2 = f/2
            H[(T(ot), T(ot))] = f / 2
            H[(T(o), T(ot))] = -f / 2
        else:
            _, k, side, sc, ss = e
            co, so = z[T(k)].cos(), z[T(k)].sin()
            h = (sc * co + ss * so) / 2
            hp = (-sc * so + ss * co) / 2
            if side == "L":
                g, gr = z[X(k)] - h, {X(k): arb(1), T(k): -hp}
            elif side == "R":
                g, gr = z[S] - z[X(k)] - h, {S: arb(1), X(k): arb(-1), T(k): -hp}
            elif side == "B":
                g, gr = z[Y(k)] - h, {Y(k): arb(1), T(k): -hp}
            else:
                g, gr = z[S] - z[Y(k)] - h, {S: arb(1), Y(k): arb(-1), T(k): -hp}
            H[(T(k), T(k))] = h                          # -h'' = h
        vals.append(g); grads.append(gr); hess.append(H)
    return vals, grads, hess


def kkt_solve(eqs, z0, lam0, n, digits, iters=40, log=False):
    ctx.dps = digits + 40
    z = [v if isinstance(v, arb) else arb(repr(float(v))) for v in z0]
    lam = [arb(repr(float(v))) for v in lam0]
    vals, grads, _ = eval_full(eqs, z, n)
    cols = sorted({k for gr in grads for k in gr})
    cp = {k: i for i, k in enumerate(cols)}
    m, N = len(eqs), len(cols)
    S = 3 * n
    hist = []
    for it in range(iters):
        vals, grads, hess = eval_full(eqs, z, n)
        # residuals
        stat = [arb(0)] * N
        stat[cp[S]] = arb(1)
        for k, gr in enumerate(grads):
            for v, gv in gr.items():
                stat[cp[v]] = stat[cp[v]] - lam[k] * gv
        F = vals + stat
        res = max(E.lg(x) for x in F)
        hist.append(res)
        if log:
            print(it, round(res, 1), flush=True)
        if res < -digits:
            break
        M = m + N                                        # rows
        Jm = arb_mat(M, N + m)
        for k, gr in enumerate(grads):                   # d g_k / dz
            for v, gv in gr.items():
                Jm[k, cp[v]] = E.mid(gv)
        for k, H in enumerate(hess):                     # d stat / dz = -sum lam H
            for (u, v), hv in H.items():
                if u not in cp or v not in cp:
                    continue
                Jm[m + cp[u], cp[v]] -= E.mid(lam[k] * hv)
                if u != v:
                    Jm[m + cp[v], cp[u]] -= E.mid(lam[k] * hv)
        for k, gr in enumerate(grads):                   # d stat / d lam_k = -grad g_k
            for v, gv in gr.items():
                Jm[m + cp[v], N + k] = -E.mid(gv)
        Fm = arb_mat(M, 1, [E.mid(x) for x in F])
        A = Jm * Jm.transpose()
        reg = arb(10) ** (-(digits // 2))
        for r in range(M):
            A[r, r] += reg
        y = A.solve(Fm, algorithm="approx")
        step = Jm.transpose() * y
        for v, i in cp.items():
            z[v] = E.mid(z[v] - step[i, 0])
        for k in range(m):
            lam[k] = E.mid(lam[k] - step[N + k, 0])
    return z, lam, hist


def initial_multipliers(eqs, z, n):
    """Least-squares lam >= 0 at float precision for e_s = sum lam grad g."""
    from scipy.optimize import nnls
    ctx.dps = 30
    zz = [arb(repr(float(v))) for v in z]
    _, grads, _ = eval_full(eqs, zz, n)
    cols = sorted({k for gr in grads for k in gr})
    cp = {k: i for i, k in enumerate(cols)}
    G = np.zeros((len(cols), len(eqs)))
    for k, gr in enumerate(grads):
        for v, gv in gr.items():
            G[cp[v], k] = float(gv.mid())
    e = np.zeros(len(cols)); e[cp[3 * n]] = 1
    lam, r = nnls(G, e, maxiter=50 * len(eqs))
    return lam, r


def analyse(n, c, th, s, digits=200, log=False):
    eqs = E.active_equations(c, th, s)
    z0 = list(np.concatenate([c.ravel(), th, [s]]))
    lam0, r = initial_multipliers(eqs, z0, n)
    if log:
        print(f"n={n}: {len(eqs)} active eqs, stationarity residual at float start {r:.1e}", flush=True)
    z, lam, h = kkt_solve(eqs, z0, lam0, n, digits, log=log)
    rng = np.random.default_rng(3)
    z0p = list(np.array(z0) + 1e-9 * rng.normal(size=len(z0)))
    z2, lam2, h2 = kkt_solve(eqs, z0p, lam0, n, digits)
    S1, S2 = z[3 * n], z2[3 * n]
    agree = min(digits, -E.lg(S1 - S2))
    return dict(n=n, eqs=len(eqs), r0=r, res=h[-1], iters=len(h), agree=agree, s=S1,
                lam_min=min(float(x.mid()) for x in lam))
