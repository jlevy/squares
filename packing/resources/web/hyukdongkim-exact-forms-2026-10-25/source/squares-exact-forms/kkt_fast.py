"""Fast high-precision KKT solve for large records.

Newton-type iteration with a FROZEN double-precision pseudo-inverse of the KKT Jacobian and residuals
evaluated in arb at the target precision (mixed-precision iterative refinement). Each sweep gains
about 16 - log10(cond) digits, at O(m) arb work per sweep instead of a dense high-precision solve.
"""
import sys, time, math, pickle
import numpy as np
from scipy.optimize import nnls
from flint import arb, ctx
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import exactform as E
import kkt as K


def residual(eqs, z, lam, n, cp, N, m):
    vals, grads, hess = K.eval_full(eqs, z, n)
    stat = [arb(0)] * N
    stat[cp[3 * n]] = arb(1)
    for k, gr in enumerate(grads):
        for v, gv in gr.items():
            stat[cp[v]] = stat[cp[v]] - lam[k] * gv
    return vals + stat, grads, hess


def jacobian_double(grads, hess, lam, cp, N, m):
    M = m + N
    Jm = np.zeros((M, N + m))
    for k, gr in enumerate(grads):
        for v, gv in gr.items():
            Jm[k, cp[v]] = float(gv.mid())
            Jm[m + cp[v], N + k] = -float(gv.mid())
    for k, H in enumerate(hess):
        lk = float(lam[k].mid())
        if lk == 0.0:
            continue
        for (u, v), hv in H.items():
            if u in cp and v in cp:
                x = lk * float(hv.mid())
                Jm[m + cp[u], cp[v]] -= x
                if u != v:
                    Jm[m + cp[v], cp[u]] -= x
    return Jm


def solve(n, c, th, s, digits=600, rcond=1e-11, max_sweeps=400, log=False, z_init=None):
    eqs = E.active_equations(c, th, s)
    ctx.dps = 40
    z0 = [arb(repr(float(v))) for v in np.concatenate([c.ravel(), th, [s]])]
    _, grads, hess = K.eval_full(eqs, z0, n)
    cols = sorted({k for gr in grads for k in gr})
    cp = {k: i for i, k in enumerate(cols)}
    N, m = len(cols), len(eqs)
    G = np.zeros((N, m))
    for k, gr in enumerate(grads):
        for v, gv in gr.items():
            G[cp[v], k] = float(gv.mid())
    e = np.zeros(N); e[cp[3 * n]] = 1
    lam0, r = nnls(G, e, maxiter=50 * m)
    t0 = time.time()
    Jm = jacobian_double(grads, hess, [arb(x) for x in lam0], cp, N, m)
    Jp = np.linalg.pinv(Jm, rcond=rcond)
    if log:
        print(f"n={n}: m={m} N={N} KKT size {Jm.shape}, pinv {time.time()-t0:.0f}s, nnls res {r:.1e}", flush=True)
    ctx.dps = digits + 40
    z = list(z_init) if z_init is not None else [arb(repr(float(v))) for v in np.concatenate([c.ravel(), th, [s]])]
    lam = [arb(repr(float(x))) for x in lam0]
    hist = []
    stall = 0
    for it in range(max_sweeps):
        F, grads, hess = residual(eqs, z, lam, n, cp, N, m)
        lr = max(E.lg(x) for x in F)
        hist.append(lr)
        if lr < -digits:
            break
        if it >= 40 and lr > -30:              # not converging: active set / KKT model off
            break
        if len(hist) > 3 and hist[-1] > hist[-2] - 1:
            stall += 1
            if stall >= 3:                    # refresh the frozen Jacobian (Newton restart)
                Jm = jacobian_double(grads, hess, lam, cp, N, m)
                Jp = np.linalg.pinv(Jm, rcond=rcond)
                stall = 0
        sc = -math.floor(lr)                  # scale residual into double range
        Fd = np.array([float((x * arb(10) ** sc).mid()) for x in F])
        d = Jp @ Fd
        inv = arb(10) ** (-sc)
        for v, i in cp.items():
            z[v] = E.mid(z[v] - arb(repr(float(d[i]))) * inv)
        for k in range(m):
            lam[k] = E.mid(lam[k] - arb(repr(float(d[N + k]))) * inv)
        if log and it % 10 == 0:
            print(f"  sweep {it}: log10 residual {lr:.1f}", flush=True)
    return z, lam, hist, dict(m=m, N=N)


def analyse(n, c, th, s, digits=600, log=False):
    t = time.time()
    z, lam, h, info = solve(n, c, th, s, digits, log=log)
    rng = np.random.default_rng(5)
    c2 = c + 1e-9 * rng.normal(size=c.shape)
    th2 = th + 1e-9 * rng.normal(size=th.shape)
    z2, _, h2, _ = solve(n, c, th, s, digits, z_init=[arb(repr(float(v))) for v in
                                                       np.concatenate([c2.ravel(), th2, [s]])])
    S1, S2 = z[3 * n], z2[3 * n]
    return dict(n=n, s=S1, res=h[-1], sweeps=len(h), agree=min(digits, -E.lg(S1 - S2)),
                sec=time.time() - t, **info)
