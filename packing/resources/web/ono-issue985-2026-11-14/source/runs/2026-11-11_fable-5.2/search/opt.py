"""Local optimisation for n unit squares in a square.

penalty_min : L-BFGS on  S + mu * E(x, y, th, S)   (soft constraints, fast, used for global search)
polish      : sequential linear programming on the exact smooth constraints
              (vertex-of-one-square on the outer side of an edge line of the other; vertices inside
              the container), with an l_inf trust region and an elastic slack.  Converges to a KKT
              point of "minimise S" with violations ~1e-13, which certify.py then makes exact.
"""
import math

import numpy as np
from numba import njit
from scipy.optimize import linprog, minimize
from scipy.sparse import csr_matrix

from sqgeom import energy_grad, max_violation, normalize


# ----------------------------------------------------------------------------- penalty phase
@njit(cache=True)
def _fg(v, n, mu, wS, g):
    x = v[0:n]; y = v[n:2 * n]; th = v[2 * n:3 * n]
    S = v[3 * n]
    gx = g[0:n]; gy = g[n:2 * n]; gt = g[2 * n:3 * n]
    E, gS = energy_grad(x, y, th, S, gx, gy, gt)
    for i in range(3 * n):
        g[i] *= mu
    g[3 * n] = wS + mu * gS
    return wS * S + mu * E


def penalty_min(x, y, th, S, mu, opt_S=True, maxiter=3000, gtol=1e-10):
    """Minimise S + mu*E (opt_S) or E alone at fixed S. Returns x, y, th, S, E."""
    n = len(x)
    v0 = np.concatenate([x, y, th, [S]])
    g = np.empty(3 * n + 1)
    if opt_S:
        def fun(v):
            f = _fg(v, n, mu, 1.0, g)
            return f, g.copy()
        res = minimize(fun, v0, jac=True, method="L-BFGS-B",
                       options=dict(maxiter=maxiter, maxfun=maxiter * 2, gtol=gtol, ftol=1e-15, maxcor=20))
        v = res.x
    else:
        def fun(v):
            vv = np.concatenate([v, [S]])
            f = _fg(vv, n, 1.0, 0.0, g)
            return f, g[:3 * n].copy()
        res = minimize(fun, v0[:3 * n], jac=True, method="L-BFGS-B",
                       options=dict(maxiter=maxiter, maxfun=maxiter * 2, gtol=gtol, ftol=1e-18, maxcor=20))
        v = np.concatenate([res.x, [S]])
    x, y, th, S = v[0:n].copy(), v[n:2 * n].copy(), v[2 * n:3 * n].copy(), float(v[3 * n])
    gg = np.empty(n)
    E, _ = energy_grad(x, y, th, S, gg, gg.copy(), gg.copy())
    return x, y, th, S, E


# ----------------------------------------------------------------------------- exact SLP polish
@njit(cache=True)
def _build(x, y, th, S, pair_cut, vert_cut, wall_cut, rows, cols, vals, rhs):
    """Assemble linearised constraints  g + G d >= 0  as  A d <= b  with A = -G, b = g.
    Variables: x(0..n-1), y(n..2n-1), th(2n..3n-1), S(3n). Returns (m, nnz)."""
    n = x.shape[0]
    m = 0
    nz = 0
    cap_r = rhs.shape[0]
    cap_z = vals.shape[0]
    c = np.cos(th)
    s = np.sin(th)
    lim = (math.sqrt(2.0) + pair_cut) ** 2
    for i in range(n):
        ci = c[i]; si = s[i]
        # ---- walls (vertex inside container)
        for a2 in (-1, 1):
            for b2 in (-1, 1):
                al = 0.5 * a2; be = 0.5 * b2
                vx = x[i] + al * ci - be * si
                vy = y[i] + al * si + be * ci
                dvx = -al * si - be * ci
                dvy = al * ci - be * si
                if m + 4 >= cap_r or nz + 12 >= cap_z:
                    return -1, -1
                if vx < wall_cut:
                    rows[nz] = m; cols[nz] = i; vals[nz] = -1.0; nz += 1
                    rows[nz] = m; cols[nz] = 2 * n + i; vals[nz] = -dvx; nz += 1
                    rhs[m] = vx; m += 1
                if S - vx < wall_cut:
                    rows[nz] = m; cols[nz] = i; vals[nz] = 1.0; nz += 1
                    rows[nz] = m; cols[nz] = 2 * n + i; vals[nz] = dvx; nz += 1
                    rows[nz] = m; cols[nz] = 3 * n; vals[nz] = -1.0; nz += 1
                    rhs[m] = S - vx; m += 1
                if vy < wall_cut:
                    rows[nz] = m; cols[nz] = n + i; vals[nz] = -1.0; nz += 1
                    rows[nz] = m; cols[nz] = 2 * n + i; vals[nz] = -dvy; nz += 1
                    rhs[m] = vy; m += 1
                if S - vy < wall_cut:
                    rows[nz] = m; cols[nz] = n + i; vals[nz] = 1.0; nz += 1
                    rows[nz] = m; cols[nz] = 2 * n + i; vals[nz] = dvy; nz += 1
                    rows[nz] = m; cols[nz] = 3 * n; vals[nz] = -1.0; nz += 1
                    rhs[m] = S - vy; m += 1
        # ---- pairs
        for j in range(i + 1, n):
            dx = x[j] - x[i]
            dy = y[j] - y[i]
            if dx * dx + dy * dy >= lim:
                continue
            cj = c[j]; sj = s[j]
            cd = cj * ci + sj * si
            sd = sj * ci - cj * si
            R = 0.5 * (1.0 + abs(cd) + abs(sd))
            p0 = dx * ci + dy * si
            p1 = -dx * si + dy * ci
            p2 = dx * cj + dy * sj
            p3 = -dx * sj + dy * cj
            best = abs(p0); k = 0
            if abs(p1) > best:
                best = abs(p1); k = 1
            if abs(p2) > best:
                best = abs(p2); k = 2
            if abs(p3) > best:
                best = abs(p3); k = 3
            if best - R > pair_cut:
                continue
            # owner o (edge line), other p (vertices)
            if k < 2:
                o = i; p = j; Dx = dx; Dy = dy
                co = ci; so = si; cp = cj; sp = sj
            else:
                o = j; p = i; Dx = -dx; Dy = -dy
                co = cj; so = sj; cp = ci; sp = si
            if k == 0 or k == 2:
                ux = co; uy = so; upx = -so; upy = co        # u = a_o, du/dth = b_o
            else:
                ux = -so; uy = co; upx = -co; upy = -so      # u = b_o, du/dth = -a_o
            proj = Dx * ux + Dy * uy
            sg = 1.0 if proj >= 0 else -1.0
            # a_p.u, b_p.u
            apu = cp * ux + sp * uy
            bpu = -sp * ux + cp * uy
            apup = cp * upx + sp * upy
            bpup = -sp * upx + cp * upy
            Dup = Dx * upx + Dy * upy
            for a2 in (-1, 1):
                for b2 in (-1, 1):
                    al = 0.5 * a2; be = 0.5 * b2
                    gval = sg * (proj + al * apu + be * bpu) - 0.5
                    if gval > vert_cut:
                        continue
                    if m + 1 >= cap_r or nz + 6 >= cap_z:
                        return -1, -1
                    # G entries (A = -G)
                    rows[nz] = m; cols[nz] = p; vals[nz] = -sg * ux; nz += 1
                    rows[nz] = m; cols[nz] = n + p; vals[nz] = -sg * uy; nz += 1
                    rows[nz] = m; cols[nz] = o; vals[nz] = sg * ux; nz += 1
                    rows[nz] = m; cols[nz] = n + o; vals[nz] = sg * uy; nz += 1
                    # d/dth_p : sg*(al*b_p - be*a_p).u
                    rows[nz] = m; cols[nz] = 2 * n + p; vals[nz] = -sg * (al * bpu - be * apu); nz += 1
                    # d/dth_o : sg*(v - c_o).u'
                    rows[nz] = m; cols[nz] = 2 * n + o; vals[nz] = -sg * (Dup + al * apup + be * bpup); nz += 1
                    rhs[m] = gval; m += 1
    return m, nz


def _viol(x, y, th, S):
    mo, mw = max_violation(x, y, th, S)
    return max(mo, mw, 0.0)


def _lp_step(x, y, th, S, delta, bufs, M, fix_S, cuts, margin=0.0):
    n = len(x)
    rows, cols, vals, rhs = bufs
    nv = 3 * n + 2
    pair_cut, vert_cut, wall_cut = cuts
    m, nz = _build(x, y, th, S, pair_cut + 2 * delta, vert_cut + 2 * delta, wall_cut + 2 * delta,
                   rows, cols, vals, rhs)
    if m < 0:
        raise RuntimeError("constraint buffer overflow")
    rr = np.concatenate([rows[:nz], np.arange(m)])
    cc = np.concatenate([cols[:nz], np.full(m, 3 * n + 1)])
    vv = np.concatenate([vals[:nz], -np.ones(m)])
    A = csr_matrix((vv, (rr, cc)), shape=(m, nv))
    cvec = np.zeros(nv)
    cvec[3 * n] = 1.0
    cvec[3 * n + 1] = M
    lb = np.full(nv, -delta); ub = np.full(nv, delta)
    lb[3 * n] = -4 * delta; ub[3 * n] = 4 * delta
    if fix_S:
        lb[3 * n] = 0.0; ub[3 * n] = 0.0
    lb[3 * n + 1] = 0.0; ub[3 * n + 1] = np.inf
    res = linprog(cvec, A_ub=A, b_ub=rhs[:m] - margin, bounds=np.column_stack([lb, ub]), method="highs",
                  options=dict(presolve=True, primal_feasibility_tolerance=1e-10, dual_feasibility_tolerance=1e-10))
    if res.status != 0:
        return None
    return res.x


DELTAS = (3e-2, 1e-2, 3e-3, 1e-3, 3e-4, 1e-4, 3e-5, 1e-5, 2e-6, 3e-7, 4e-8)


def polish(x, y, th, S=None, delta=0.03, max_iter=600, verbose=False,
           pair_cut=0.12, vert_cut=0.25, wall_cut=0.2, nu=1000.0, fix_S=None, slide_cap=80, safe=3e-10):
    """SLP with a decreasing trust-region schedule. Every LP step is accepted: the linearised
    constraints hold exactly, so the true violation after a step is O(delta^2) and the next LP
    removes it. A stage runs while S keeps dropping by more than 3% of delta per step (long
    "slides" are followed at the largest delta), then delta shrinks. A last LP with a tiny positive
    margin makes the result strictly feasible in floats. Returns x, y, th, S, viol, info."""
    n = len(x)
    x = x.copy(); y = y.copy(); th = th.copy()
    if S is None:
        x, y, th, S = normalize(x, y, th)
    cap_r = 40 * n + 64
    cap_z = cap_r * 7
    bufs = (np.empty(cap_z, np.int64), np.empty(cap_z, np.int64), np.empty(cap_z), np.empty(cap_r))
    cuts = (pair_cut, vert_cut, wall_cut)
    it = 0
    stages = [d for d in DELTAS if d <= delta * 1.0001]
    for si, dl in enumerate(stages):
        small = 0
        cap = slide_cap if si < 2 else (30 if si < 4 else 10)
        for k in range(cap):
            if it >= max_iter:
                break
            it += 1
            d = _lp_step(x, y, th, S, dl, bufs, nu, fix_S is not None, cuts)
            if d is None:
                break
            x = x + d[0:n]; y = y + d[n:2 * n]; th = th + d[2 * n:3 * n]
            dS = d[3 * n]
            S = S + dS
            if verbose:
                print(f"  it {it:3d} delta={dl:.1e} S={S:.14f} dS={dS:+.2e} t={d[3*n+1]:.1e} V={_viol(x, y, th, S):.2e}")
            if dS > -0.03 * dl and d[3 * n + 1] < 1e-12:
                small += 1
                if small >= 2:
                    break
            else:
                small = 0
    # final strictly-feasible step(s)
    for k in range(3):
        V = _viol(x, y, th, S)
        if V <= 0.0 and k > 0:
            break
        d = _lp_step(x, y, th, S, 1e-7 if k == 0 else 1e-6, bufs, nu, fix_S is not None, cuts, margin=safe * (1 + 3 * k))
        if d is None:
            break
        x = x + d[0:n]; y = y + d[n:2 * n]; th = th + d[2 * n:3 * n]; S = S + d[3 * n]
        it += 1
    V = _viol(x, y, th, S)
    return x, y, th, S, V, dict(iters=it, delta=stages[-1] if stages else delta)


def tighten(x, y, th, S, margin=2e-12, iters=6):
    """Make the float packing strictly feasible with a tiny positive margin (so that rational
    snapping cannot create overlaps): scale centres about the centroid, then report the bbox side."""
    V = _viol(x, y, th, S)
    lam = 1.0 + (max(V, 0.0) + margin) * 2.0
    gx, gy = x.mean(), y.mean()
    for _ in range(iters):
        xx = gx + lam * (x - gx); yy = gy + lam * (y - gy)
        xx, yy, tt, SS = normalize(xx, yy, th.copy())
        mo, mw = max_violation(xx, yy, tt, SS)
        if mo <= -margin * 0.25:
            return xx, yy, tt, SS
        lam = 1.0 + (lam - 1.0) * 2.0
    return xx, yy, tt, SS
