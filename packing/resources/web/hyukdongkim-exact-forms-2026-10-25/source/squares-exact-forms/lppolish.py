"""Scalable polisher for large n.

(A) With all angles fixed, every SAT constraint (chosen axis + side) and every wall constraint is
    LINEAR in the centres and s, so  min s  is an exact LP (sparse, HiGHS).
(B) Angles move by sequential linear programming with a trust region; each trial is made exactly
    feasible again by (A). A step is kept only if (A) returns a smaller s.
Only pairs whose centres are within sqrt(2)+margin can touch, so constraints stay O(n).
"""
import math
import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog
from scipy.spatial import cKDTree

R2 = math.sqrt(2.0)
HIGHS = dict(primal_feasibility_tolerance=1e-10, dual_feasibility_tolerance=1e-10)


def half_ext(th_self, th_axis_owner, which):
    """Half-extent of a unit square at angle th_self on axis (owner angle, which)."""
    d = th_self - th_axis_owner
    return 0.5 * (np.abs(np.cos(d)) + np.abs(np.sin(d)))


def near_pairs(c, cut):
    tree = cKDTree(c)
    P = np.array(sorted(tree.query_pairs(cut)), dtype=int)
    return P.reshape(-1, 2)


def sat_all(c, th, P):
    """Separation on all 4 SAT axes for pairs P -> (m,4)."""
    I, J = P[:, 0], P[:, 1]
    D = c[I] - c[J]
    out = np.empty((len(P), 4))
    for k, (O, w) in enumerate([(I, 0), (I, 1), (J, 0), (J, 1)]):
        t = th[O]
        a = np.stack([np.cos(t), np.sin(t)], 1) if w == 0 else np.stack([-np.sin(t), np.cos(t)], 1)
        hi = half_ext(th[I], t, w) if True else None
        hj = half_ext(th[J], t, w)
        out[:, k] = np.abs((D * a).sum(1)) - hi - hj
    return out


def max_violation(c, th, s):
    P = near_pairs(c, R2 + 1e-6)
    v = 0.0
    if len(P):
        v = max(v, -sat_all(c, th, P).max(1).min())
    h = 0.5 * (np.abs(np.cos(th)) + np.abs(np.sin(th)))
    v = max(v, (h - c[:, 0]).max(), (c[:, 0] + h - s).max(), (h - c[:, 1]).max(), (c[:, 1] + h - s).max())
    return v


def choose(c, th, P):
    sep = sat_all(c, th, P)
    k = sep.argmax(1)
    I, J = P[:, 0], P[:, 1]
    O = np.where(k < 2, I, J)
    W = k % 2
    t = th[O]
    a = np.where(W[:, None] == 0, np.stack([np.cos(t), np.sin(t)], 1), np.stack([-np.sin(t), np.cos(t)], 1))
    SG = np.where(((c[I] - c[J]) * a).sum(1) >= 0, 1.0, -1.0)
    return I, J, O, W, SG


def lp_fixed_angles(c, th, s_hint, margin=0.25, eps=0.0, want_duals=False):
    """Exact LP over centres and s with angles fixed. Returns (c, s) or None."""
    n = len(th)
    P = near_pairs(c, R2 + margin)
    I, J, O, W, SG = choose(c, th, P)
    t = th[O]
    a = np.where(W[:, None] == 0, np.stack([np.cos(t), np.sin(t)], 1), np.stack([-np.sin(t), np.cos(t)], 1))
    ext = 0.5 + half_ext(np.where(O == I, th[J], th[I]), t, W)       # owner 0.5 + other's extent
    m = len(P)
    # variables: x(0..n-1), y(n..2n-1), s(2n)
    rows = np.repeat(np.arange(m), 4)
    cols = np.stack([I, n + I, J, n + J], 1).ravel()
    vals = np.stack([SG * a[:, 0], SG * a[:, 1], -SG * a[:, 0], -SG * a[:, 1]], 1).ravel()
    Ap = sp.csr_matrix((-vals, (rows, cols)), shape=(m, 2 * n + 1))   # -(SG a.D) <= -ext
    bp = -(ext + eps)
    h = 0.5 * (np.abs(np.cos(th)) + np.abs(np.sin(th)))
    k = np.arange(n)
    # x_k >= h_k ; x_k + h_k <= s ; same for y
    Aw = sp.vstack([
        sp.csr_matrix((-np.ones(n), (k, k)), shape=(n, 2 * n + 1)),
        sp.csr_matrix((np.r_[np.ones(n), -np.ones(n)], (np.r_[k, k], np.r_[k, np.full(n, 2 * n)])), shape=(n, 2 * n + 1)),
        sp.csr_matrix((-np.ones(n), (k, n + k)), shape=(n, 2 * n + 1)),
        sp.csr_matrix((np.r_[np.ones(n), -np.ones(n)], (np.r_[k, k], np.r_[n + k, np.full(n, 2 * n)])), shape=(n, 2 * n + 1)),
    ])
    bw = np.r_[-(h + eps), -h - eps, -(h + eps), -h - eps]
    A = sp.vstack([Ap, Aw]).tocsc()
    b = np.r_[bp, bw]
    cost = np.zeros(2 * n + 1); cost[-1] = 1
    # each centre may move at most margin/2 so no pair outside the cut can come into contact
    rmove = 0.5 * margin - 1e-6
    lo = np.r_[c[:, 0] - rmove, c[:, 1] - rmove, -np.inf]
    hi = np.r_[c[:, 0] + rmove, c[:, 1] + rmove, np.inf]
    res = linprog(cost, A_ub=A, b_ub=b, bounds=np.stack([lo, hi], 1), method="highs", options=HIGHS)
    if res.status != 0:
        return None
    z = res.x
    if want_duals:
        lam = -res.ineqlin.marginals                    # >= 0, sensitivity of s to each constraint
        load = np.zeros(n)
        np.add.at(load, I, lam[:m]); np.add.at(load, J, lam[:m])
        for w in range(4):
            load += lam[m + w * n: m + (w + 1) * n]
        return np.stack([z[:n], z[n:2 * n]], 1), z[-1], load
    return np.stack([z[:n], z[n:2 * n]], 1), z[-1]


def slp_angle_step(c, th, s, r_th, r_x=0.02, margin=0.25):
    """Linearize all constraints in (x, y, theta, s); trust region on theta and positions."""
    n = len(th)
    P = near_pairs(c, R2 + margin)
    I, J, O, W, SG = choose(c, th, P)
    OT = np.where(O == I, J, I)
    t = th[O]
    ct, st = np.cos(t), np.sin(t)
    a = np.where(W[:, None] == 0, np.stack([ct, st], 1), np.stack([-st, ct], 1))
    da = np.where(W[:, None] == 0, np.stack([-st, ct], 1), np.stack([-ct, -st], 1))
    D = c[I] - c[J]
    dist = SG * (D * a).sum(1)
    d = th[OT] - t
    cd, sd = np.cos(d), np.sin(d)
    N = 3 * n + 1
    rows, cols, vals, rhs = [], [], [], []
    r = 0
    for sc, ss in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        g = dist - 0.5 - 0.5 * (sc * cd + ss * sd)
        dto = 0.5 * (sc * sd - ss * cd)                 # derivative wrt theta_other
        m = len(I)
        R = r + np.arange(m)
        for colset, v in ((I, SG * a[:, 0]), (n + I, SG * a[:, 1]), (J, -SG * a[:, 0]), (n + J, -SG * a[:, 1]),
                          (2 * n + O, SG * (D * da).sum(1) - dto), (2 * n + OT, dto)):
            rows.append(R); cols.append(colset); vals.append(-v)
        rhs.append(g)                                    # -(grad . delta) <= g
        r += m
    k = np.arange(n)
    for sc, ss in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        h = 0.5 * (sc * np.cos(th) + ss * np.sin(th))
        hp = 0.5 * (-sc * np.sin(th) + ss * np.cos(th))
        # x - h >= 0
        for (xcol, sgn_x, has_s, base) in ((k, 1, False, c[:, 0] - h), (k, -1, True, s - c[:, 0] - h),
                                           (n + k, 1, False, c[:, 1] - h), (n + k, -1, True, s - c[:, 1] - h)):
            R = r + k
            rows += [R, R]; cols += [xcol, 2 * n + k]; vals += [-sgn_x * np.ones(n), hp]
            if has_s:
                rows.append(R); cols.append(np.full(n, 3 * n)); vals.append(-np.ones(n))
            rhs.append(base)
            r += n
    A = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(r, N))
    b = np.concatenate(rhs)
    cost = np.zeros(N); cost[-1] = 1
    bounds = [(-r_x, r_x)] * (2 * n) + [(-r_th, r_th)] * n + [(-1, 1)]
    res = linprog(cost, A_ub=A, b_ub=b, bounds=bounds, method="highs", options=HIGHS)
    if res.status != 0:
        return None
    return th + res.x[2 * n:3 * n]


def polish(c, th, s, iters=200, r0=2e-3, tol=1e-13, log=False):
    """Returns (c, th, s, history). Input angles in radians."""
    hist = [s]
    for _ in range(50):                                   # LP with bounded moves, repeated
        out = lp_fixed_angles(c, th, s)
        if out is None:
            break
        moved = s - out[1]
        c, s = out
        hist.append(s)
        if moved < tol:
            break
    r = r0
    for it in range(iters):
        th_new = slp_angle_step(c, th, s, r)
        ok = False
        if th_new is not None:
            o = lp_fixed_angles(c, th_new, s)
            if o is not None and o[1] < s - tol:
                c, s, th = o[0], o[1], th_new
                hist.append(s); ok = True
                r = min(r * 2, 5e-2)
        if not ok:
            r /= 4
            if r < 1e-12:
                break
        if log:
            print(it, s, r, ok)
    return c, th, s, hist
