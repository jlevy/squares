"""Exploration for the interval grade-C checker: structure of the rows, flat family, W, affine multipliers, Hessian.

    PYTHONPATH=. ./env.sh python3 gradec_explore.py 10 19 29
"""
import json, sys
import numpy as np
from mpmath import mp, mpf, cos, sin, radians
from scipy.optimize import linprog
import scipy.linalg as sla
import geom

mp.dps = 50


def load(n):
    Lf = [l.split() for l in open(f'minpoly/solve/n-{n}.exact.txt') if l.strip()]
    S = mpf(Lf[0][1])
    X = [mpf(l[0]) for l in Lf[1:]]; Y = [mpf(l[1]) for l in Lf[1:]]; TH = [mpf(l[2]) for l in Lf[1:]]
    C = [cos(radians(t)) for t in TH]; Sn = [sin(radians(t)) for t in TH]
    ct = json.load(open(f'minpoly/solve/n-{n}.contacts.json'))
    return S, X, Y, C, Sn, TH, ct


def rows_of(n, X, Y, C, Sn, ct):
    A = [tuple(a) for a in ct['load_bearing']]
    rows, ends = [], {}
    for a in A:
        if a[0] == 'W':
            rows.append(a); continue
        tau = geom.tangential(a, X, Y, C, Sn, mpf(1) / 2)
        if abs(abs(tau) - mpf(1) / 2) < 1e-20:
            ends.setdefault((a[1], a[3], a[4]), []).append(a)
        else:
            rows.append(a)
    lone = []
    for key, inc in ends.items():
        if len(inc) == 2:
            rows += inc
        else:
            lone += inc
    return rows, lone


def explore(n):
    S, X, Y, C, Sn, TH, ct = load(n)
    rows, lone = rows_of(n, X, Y, C, Sn, ct)
    lb = sorted({r[1] for r in rows} | {r[3] for r in rows if r[0] == 'C'})
    var = {}
    for i in lb:
        for c in range(3):
            var[3 * i + c] = len(var)
    var[3 * n] = len(var)
    N, m = len(var), len(rows)
    H = mpf(1) / 2

    def Lmat(X, Y):
        L = np.zeros((m, N))
        for a, r in enumerate(rows):
            for v, val in geom.eval_contact(r, X, Y, C, Sn, S, H, order=1)[1]:
                L[a, var[v]] += float(val)
        return L
    L = Lmat(X, Y)
    pos = [var[3 * i + c] for i in lb for c in (0, 1)]
    sv = np.linalg.svd(L, compute_uv=False)
    rk = int((sv > 1e-10 * sv[0]).sum())
    _, svp, Vt = np.linalg.svd(L[:, pos])
    rkp = int((svp > 1e-10 * svp[0]).sum())
    Fp = Vt[rkp:].T
    f = Fp.shape[1]
    Fb = np.zeros((N, f)); Fb[pos, :] = Fp
    N0 = sla.null_space(L, rcond=1e-10)
    # W = N0 cap F-perp
    P = N0 - Fb @ (Fb.T @ N0)
    u, sw, _ = np.linalg.svd(P, full_matrices=False)
    W = u[:, sw > 1e-8]
    moving = sorted({lb[p // 2] for p in range(len(pos)) for k in range(f) if abs(Fp[p, k]) > 1e-8})
    # max-min multipliers
    es = np.zeros(N); es[N - 1] = 1
    res = linprog(np.r_[np.zeros(m), -1], A_eq=np.c_[L.T, np.zeros(N)], b_eq=es, A_ub=np.c_[-np.eye(m), np.ones(m)],
                  b_ub=np.zeros(m), bounds=[(None, None)] * (m + 1), method='highs')
    lam = res.x[:m]
    # derivative of L along each flat direction (L is affine in the centres)
    Ak = []
    for k in range(f):
        Xm, Ym = list(X), list(Y)
        for p, col in enumerate(pos):
            i = lb[p // 2]
            if p % 2 == 0: Xm[i] += mpf(Fp[p, k])
            else: Ym[i] += mpf(Fp[p, k])
        Ak.append(Lmat(Xm, Ym) - L)
    # affine multipliers: L^T mu_k = -A_k^T lam;  A_k^T mu_l + A_l^T mu_k = 0
    nb = f * m
    blocks, rhs = [], []
    for k in range(f):
        row = np.zeros((N, nb)); row[:, k * m:(k + 1) * m] = L.T
        blocks.append(row); rhs.append(-Ak[k].T @ lam)
    for k in range(f):
        for l in range(k, f):
            row = np.zeros((N, nb))
            row[:, l * m:(l + 1) * m] += Ak[k].T
            row[:, k * m:(k + 1) * m] += Ak[l].T
            blocks.append(row); rhs.append(np.zeros(N))
    if f:
        Mx, b = np.vstack(blocks), np.concatenate(rhs)
        mu, *_ = np.linalg.lstsq(Mx, b, rcond=None)
        resid = np.linalg.norm(Mx @ mu - b)
        lin_only = np.linalg.lstsq(np.vstack(blocks[:f]), np.concatenate(rhs[:f]), rcond=None)
        resid1 = np.linalg.norm(np.vstack(blocks[:f]) @ lin_only[0] - np.concatenate(rhs[:f]))
    else:
        resid = resid1 = 0.0
    # Hessian of the Lagrangian on W
    Hs = np.zeros((N, N))
    for a, r in enumerate(rows):
        for v1, v2, val in geom.eval_contact(r, X, Y, C, Sn, S, H, order=2)[2]:
            i1, i2 = var[v1], var[v2]
            Hs[i1, i2] -= lam[a] * float(val)
            if i1 != i2:
                Hs[i2, i1] -= lam[a] * float(val)
    Qw = W.T @ Hs @ W if W.shape[1] else np.zeros((0, 0))
    ev = np.linalg.eigvalsh(Qw) if W.shape[1] else []
    print(f'n={n}: rows {m} (lone side-end {len(lone)}), load-bearing squares {len(lb)}, N {N}, rank L {rk}, '
          f'dim null {N - rk}, dim F {f} (moving squares {moving}), dim W {W.shape[1]}')
    print(f'   max-min lambda {res.x[-1]:.4g}; affine lambda(phi): first-order residual {resid1:.2e}, '
          f'with quadratic terms {resid:.2e}; Hessian on W eigenvalues {np.round(ev, 5) if len(ev) else "-"}')


for n in map(int, sys.argv[1:]):
    explore(n)


def polylam(n, d):
    """Least-squares test: lambda(phi) polynomial of degree d in the flat coordinates with L(phi)^T lambda(phi) = e_S
    identically (L(phi) = L0 + sum phi_k A_k is affine in phi)."""
    import itertools
    S, X, Y, C, Sn, TH, ct = load(n)
    rows, lone = rows_of(n, X, Y, C, Sn, ct)
    lb = sorted({r[1] for r in rows} | {r[3] for r in rows if r[0] == 'C'})
    var = {}
    for i in lb:
        for c in range(3):
            var[3 * i + c] = len(var)
    var[3 * n] = len(var)
    N, m = len(var), len(rows)
    H = mpf(1) / 2

    def Lmat(X, Y):
        L = np.zeros((m, N))
        for a, r in enumerate(rows):
            for v, val in geom.eval_contact(r, X, Y, C, Sn, S, H, order=1)[1]:
                L[a, var[v]] += float(val)
        return L
    L = Lmat(X, Y)
    pos = [var[3 * i + c] for i in lb for c in (0, 1)]
    _, svp, Vt = np.linalg.svd(L[:, pos])
    rkp = int((svp > 1e-10 * svp[0]).sum())
    Fp = Vt[rkp:].T
    f = Fp.shape[1]
    Ak = []
    for k in range(f):
        Xm, Ym = list(X), list(Y)
        for p in range(len(pos)):
            i = lb[p // 2]
            if p % 2 == 0: Xm[i] += mpf(Fp[p, k])
            else: Ym[i] += mpf(Fp[p, k])
        Ak.append(Lmat(Xm, Ym) - L)
    mons = [e for t in range(d + 1) for e in itertools.combinations_with_replacement(range(f), t)]
    idx = {e: i for i, e in enumerate(mons)}
    outm = [e for t in range(d + 2) for e in itertools.combinations_with_replacement(range(f), t)]
    oidx = {e: i for i, e in enumerate(outm)}
    Mx = np.zeros((N * len(outm), m * len(mons)))
    b = np.zeros(N * len(outm))
    b[oidx[()] * N + N - 1] = 1
    for e in mons:
        j = idx[e]
        o = oidx[e]
        Mx[o * N:(o + 1) * N, j * m:(j + 1) * m] += L.T
        for k in range(f):
            o2 = oidx[tuple(sorted(e + (k,)))]
            Mx[o2 * N:(o2 + 1) * N, j * m:(j + 1) * m] += Ak[k].T
    sol, *_ = np.linalg.lstsq(Mx, b, rcond=None)
    print(f'n={n}: f={f}, degree {d}: residual {np.linalg.norm(Mx @ sol - b):.2e} ({Mx.shape[0]} eqs, {Mx.shape[1]} unknowns)')


def polynull(n, d):
    """Dimension of the space of polynomial vectors w(phi) (degree <= d) with L(phi) w(phi) = 0 identically, and of
    those with w_S = 0; compare with dim null L(0) - dim F."""
    import itertools
    S, X, Y, C, Sn, TH, ct = load(n)
    rows, lone = rows_of(n, X, Y, C, Sn, ct)
    lb = sorted({r[1] for r in rows} | {r[3] for r in rows if r[0] == 'C'})
    var = {}
    for i in lb:
        for c in range(3):
            var[3 * i + c] = len(var)
    var[3 * n] = len(var)
    N, m = len(var), len(rows)
    H = mpf(1) / 2

    def Lmat(X, Y):
        L = np.zeros((m, N))
        for a, r in enumerate(rows):
            for v, val in geom.eval_contact(r, X, Y, C, Sn, S, H, order=1)[1]:
                L[a, var[v]] += float(val)
        return L
    L = Lmat(X, Y)
    pos = [var[3 * i + c] for i in lb for c in (0, 1)]
    _, svp, Vt = np.linalg.svd(L[:, pos])
    rkp = int((svp > 1e-10 * svp[0]).sum())
    Fp = Vt[rkp:].T
    f = Fp.shape[1]
    Ak = []
    for k in range(f):
        Xm, Ym = list(X), list(Y)
        for p in range(len(pos)):
            i = lb[p // 2]
            if p % 2 == 0: Xm[i] += mpf(Fp[p, k])
            else: Ym[i] += mpf(Fp[p, k])
        Ak.append(Lmat(Xm, Ym) - L)
    mons = [e for t in range(d + 1) for e in itertools.combinations_with_replacement(range(f), t)]
    idx = {e: i for i, e in enumerate(mons)}
    outm = [e for t in range(d + 2) for e in itertools.combinations_with_replacement(range(f), t)]
    oidx = {e: i for i, e in enumerate(outm)}
    Mx = np.zeros((m * len(outm), N * len(mons)))
    for e in mons:
        j = idx[e]
        Mx[oidx[e] * m:(oidx[e] + 1) * m, j * N:(j + 1) * N] += L
        for k in range(f):
            o2 = oidx[tuple(sorted(e + (k,)))]
            Mx[o2 * m:(o2 + 1) * m, j * N:(j + 1) * N] += Ak[k]
    ns = sla.null_space(Mx, rcond=1e-11)
    # constant part w(0) of the solutions, modulo F
    w0 = ns[:N, :]
    Fb = np.zeros((N, f)); Fb[pos, :] = Fp
    w0p = w0 - Fb @ (Fb.T @ w0)
    sv0 = np.linalg.svd(w0p, compute_uv=False) if w0p.size else []
    dimW0 = int((np.array(sv0) > 1e-8).sum())
    Sabs = np.abs(ns[[j * N + N - 1 for j in range(len(mons))], :]).max() if ns.size else 0
    nullL0 = N - int((np.linalg.svd(L, compute_uv=False) > 1e-10).sum())
    print(f'n={n}: f={f}, degree {d}: polynomial null solutions {ns.shape[1]}; their w(0) span {dimW0} dims mod F '
          f'(need {nullL0 - f}); max |w_S coefficient| {Sabs:.1e}')
