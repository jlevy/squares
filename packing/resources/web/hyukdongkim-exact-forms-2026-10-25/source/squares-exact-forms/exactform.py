"""Exact algebraic form of a record side length.

1. From a polished float packing, collect every geometrically active constraint (SAT contact on the
   separating axis, wall contacts), with |cos|,|sin| resolved into sign branches (both branches when
   the argument sits on a kink, which encodes parallel / axis-aligned squares).
2. Solve the contact equations to P digits with minimum-norm Gauss-Newton in arb (python-flint).
3. Rigidity check: re-solve from a perturbed start; s must agree to ~P digits.
4. Integer relation (LLL on fmpz lattice) for the minimal polynomial of s; confirm at 2P digits.
"""
import math, pickle, sys, time
import numpy as np
from flint import arb, arb_mat, fmpz_mat, fmpz, ctx
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import lppolish as L

R2 = math.sqrt(2)
KINK = 1e-9


def signs(v):
    return (1, -1) if abs(v) < KINK else ((1,) if v > 0 else (-1,))


def active_equations(c, th, s, tol=1e-9):
    """Returns list of equations; each is a tuple describing its type and fixed discrete data."""
    n = len(th)
    eqs = []
    P = L.near_pairs(c, R2 + 0.01)
    if len(P):
        sep = L.sat_all(c, th, P)
        for (i, j), row in zip(P, sep):
            if row.max() > tol:
                continue
            for k in np.where(row > -tol)[0]:          # every axis that separates (touching)
                owner, other = (i, j) if k < 2 else (j, i)
                w = k % 2
                t = th[owner]
                a = (math.cos(t), math.sin(t)) if w == 0 else (-math.sin(t), math.cos(t))
                SG = 1 if (c[i, 0] - c[j, 0]) * a[0] + (c[i, 1] - c[j, 1]) * a[1] >= 0 else -1
                d = th[other] - t
                for sc in signs(math.cos(d)):
                    for ss in signs(math.sin(d)):
                        eqs.append(("pair", int(i), int(j), int(owner), int(other), int(w), SG, sc, ss))
    for k in range(n):
        h = 0.5 * (abs(math.cos(th[k])) + abs(math.sin(th[k])))
        gaps = {"L": c[k, 0] - h, "R": s - c[k, 0] - h, "B": c[k, 1] - h, "T": s - c[k, 1] - h}
        for side, gval in gaps.items():
            if gval < tol:
                for sc in signs(math.cos(th[k])):
                    for ss in signs(math.sin(th[k])):
                        eqs.append(("wall", k, side, sc, ss))
    return eqs


def eval_eqs(eqs, z, n):
    """z: list of arb (x0,y0,...,x_{n-1},y_{n-1}, th_0..th_{n-1}, s). Returns values, sparse grads."""
    X = lambda k: 2 * k
    Y = lambda k: 2 * k + 1
    T = lambda k: 2 * n + k
    S = 3 * n
    vals, grads = [], []
    cache = {}

    def cs(k):
        if k not in cache:
            cache[k] = (z[T(k)].cos(), z[T(k)].sin())
        return cache[k]
    for e in eqs:
        if e[0] == "pair":
            _, i, j, o, ot, w, SG, sc, ss = e
            co, so = cs(o)
            if w == 0:
                a, da = (co, so), (-so, co)
            else:
                a, da = (-so, co), (-co, -so)
            dx, dy = z[X(i)] - z[X(j)], z[Y(i)] - z[Y(j)]
            d = z[T(ot)] - z[T(o)]
            cd, sd = d.cos(), d.sin()
            g = SG * (dx * a[0] + dy * a[1]) - arb(0.5) - (sc * cd + ss * sd) / 2
            dto = (sc * sd - ss * cd) / 2
            gr = {X(i): SG * a[0], Y(i): SG * a[1], X(j): -SG * a[0], Y(j): -SG * a[1]}
            gr[T(o)] = gr.get(T(o), 0) + SG * (dx * da[0] + dy * da[1]) - dto
            gr[T(ot)] = gr.get(T(ot), 0) + dto
        else:
            _, k, side, sc, ss = e
            co, so = cs(k)
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
        vals.append(g)
        grads.append(gr)
    return vals, grads


def mid(x):
    return arb(x.mid())


def lg(x):
    """log10 |x| as a float, safe far below the double-precision range."""
    a = abs(x.mid())
    if a == 0:
        return -1e9
    return float((a.log() / arb(10).log()).mid())


def solve(eqs, z0, n, digits, iters=60, log=False):
    ctx.dps = digits + 30
    z = [arb(repr(float(v))) if not isinstance(v, arb) else v for v in z0]
    cols = sorted({k for e in eval_eqs(eqs, z, n)[1] for k in e})
    colpos = {k: i for i, k in enumerate(cols)}
    m, N = len(eqs), len(cols)
    hist = []
    for it in range(iters):
        vals, grads = eval_eqs(eqs, z, n)
        res = max(lg(v) for v in vals)          # log10 of the residual
        hist.append(res)
        if log:
            print(it, res, flush=True)
        if res < -digits:
            break
        J = arb_mat(m, N)
        for r, gr in enumerate(grads):
            for k, v in gr.items():
                J[r, colpos[k]] = mid(arb(v) if not isinstance(v, arb) else v)
        g = arb_mat(m, 1, [mid(v) for v in vals])
        A = J * J.transpose()
        reg = arb(10) ** (-(digits // 2))
        for r in range(m):
            A[r, r] += reg
        y = A.solve(g, algorithm="approx")
        step = J.transpose() * y
        for k, i in colpos.items():
            z[k] = mid(z[k] - step[i, 0])
    return z, hist


def minpoly(s_arb, digits, maxdeg=40):
    """LLL integer relation on 1, s, s^2, ..., s^d."""
    ctx.dps = digits + 30
    for d in range(1, maxdeg + 1):
        K = fmpz(10) ** int(digits * 0.9)
        pw = [arb(1)]
        for _ in range(d):
            pw.append(pw[-1] * s_arb)
        rows = []
        for i in range(d + 1):
            row = [0] * (d + 1) + [int((pw[i] * arb(K)).mid().floor().unique_fmpz())]
            row[i] = 1
            rows.append(row)
        B = fmpz_mat(rows).lll()
        coeffs = [int(B[0, i]) for i in range(d + 1)]
        if coeffs[-1] == 0:
            continue
        val = sum(arb(cf) * pw[i] for i, cf in enumerate(coeffs))
        height = max(abs(cf) for cf in coeffs)
        if lg(val) < -digits * 0.6 and len(str(height)) * (d + 1) < digits * 0.7:
            return coeffs
    return None


def analyse(n, c, th, s, digits=400, log=False):
    t0 = time.time()
    eqs = active_equations(c, th, s)
    z0 = list(np.concatenate([c.ravel(), th, [s]]))
    z, h = solve(eqs, z0, n, digits)
    S1 = z[3 * n]
    rng = np.random.default_rng(1)
    z0p = list(np.array(z0) + 1e-9 * rng.normal(size=len(z0)))
    z2, h2 = solve(eqs, z0p, n, digits)
    S2 = z2[3 * n]
    agree = min(digits, -lg(S1 - S2))
    out = dict(n=n, eqs=len(eqs), res=h[-1], iters=len(h), s=S1, agree_digits=agree,
               float_s=s, sec=time.time() - t0)
    if agree > 0.8 * digits:
        out["poly"] = minpoly(S1, digits)
    return out
