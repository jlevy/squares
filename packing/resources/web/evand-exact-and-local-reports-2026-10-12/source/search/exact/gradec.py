"""Grade-C local-minimum certificates (strict modulo exact flat motions), exact in the number field K.

Theorem C (tasks/exact-minpoly/grade-C.md): z* is a local minimum of S among packings if
  (1) every row is valid near z* with a margin (interior incidences project strictly inside their side; side-end
      incidences come as the two corners of one side of j lying on the line of i's side: h >= -K' delta^2);
  (2) KKT along the flat family M = z* + F (F = position directions with L_pos phi = 0): multipliers
      lambda(m) >= lambda_min > 0 with sum lambda_r(m) L_r(m) = e_S for every m in M near z*;
  (3) the reduced Hessian of the Lagrangian is positive definite on W, a complement of F in null L.

Certificate for (2) (null-vector form; grade-C.md "Hypothesis 2 by null vectors"): L(phi) = L0 + sum_k phi_k A_k is
affine in phi (only the lever arms of the torque columns move).  Exhibit affine vectors w_j(phi) = w_j0 + sum phi_k w_jk
with L(phi) w_j(phi) = 0 identically and S-component 0, whose w_j0 together with F span null L0.  Then for phi near 0
null L(phi) = span(F, w_j(phi)) (rank cannot drop near 0), e_S is orthogonal to it, so e_S is in the range of
L(phi)^T with constant rank, and lambda(phi) = lambda* + L(phi)^T+ (e_S - L(phi)^T lambda*) is continuous with
lambda(0) = lambda* > 0.  The identities are checked exactly in K: L0 w_j0 = 0, L0 w_jk + A_k w_j0 = 0,
A_k w_jl + A_l w_jk = 0.  (They also make the F x W block of the Hessian vanish: lambda*^T A_k w_j0 = -(w_jk)_S = 0.)

Exact data from NAME.minpoly.json (degree-d field K = Q[t]/f; practical for small d).  Signs of K elements by interval
arithmetic at t* (verify_exact.I).

  PYTHONPATH=. ./env.sh python3 gradec.py minpoly/solve/n-10 [...]
"""
import sys, json, itertools, time
from fractions import Fraction as F
import numpy as np
import flint
from mpmath import mp, mpf
import geom
from verify_exact import I, ev_iv, rdn, rup
from localmin import Kf, q

Q = flint.fmpq_poly
ZERO = Q([0])


def setup(base):
    D = json.load(open(base + '.minpoly.json'))
    ct = json.load(open(base + '.contacts.json'))
    n = D['n']
    K = Kf(D['field']['f'])
    ta, tb = (F(x) for x in D['field']['t_interval'])
    fl = [F(c) for c in D['field']['f']]
    fv = lambda x: sum(c * x ** i for i, c in enumerate(fl))
    for _ in range(200):                                          # narrow the t interval (exact bisection)
        if ta == tb:
            break
        mid = (ta + tb) / 2
        if fv(mid) == 0:
            ta = tb = mid
            break
        if fv(ta) * fv(mid) < 0:
            tb = mid
        else:
            ta = mid
        ta, tb = rdn(ta), rup(tb)
    T = I(ta, tb)
    X, Y, C, S_ = [], [], [], []
    for sq in D['squares']:
        X.append(K.poly(sq['x'])); Y.append(K.poly(sq['y']))
        u = K.poly(sq['u'])
        di = K.inv(K.red(Q([1]) + u * u))
        c, s = K.red((Q([1]) - u * u) * di), K.red(Q([2]) * u * di)
        for _ in range(sq['m'] % 4):
            c, s = -s, c
        C.append(c); S_.append(s)
    mp.dps = 60
    tnum = mpf(D['field']['t_approx'])

    def num(p):
        return sum(mpf(int(c.p)) / int(c.q) * tnum ** i for i, c in enumerate(p.coeffs())) if not p.is_zero() else mpf(0)

    def iv(p):
        return ev_iv([F(int(c.p), int(c.q)) for c in p.coeffs()], T) if not p.is_zero() else I(0)
    return dict(D=D, ct=ct, n=n, K=K, T=T, X=X, Y=Y, C=C, S=S_, num=num, iv=iv, Sk=K.poly(D['S']['in_K']))


def sign(iv_):
    if iv_.lo > 0:
        return 1
    if iv_.hi < 0:
        return -1
    return 0


# ---------------------------------------------------------------- sparse linear algebra over K (exact)
def rref(rows, K, ncols):
    """rows: list of dict col -> K element.  Returns (pivots: dict col -> normalised row dict, inconsistent: bool when
    column ncols (if present) is the right-hand side)."""
    piv = {}
    order = []
    for r in rows:
        r = {c: v for c, v in r.items() if not v.is_zero()}
        # reduce by existing pivots
        changed = True
        while changed:
            changed = False
            for c in sorted(r):
                if c in piv and not r[c].is_zero():
                    f = r[c]
                    for cc, vv in piv[c].items():
                        r[cc] = K.red(r.get(cc, ZERO) - f * vv)
                    r = {c2: v for c2, v in r.items() if not v.is_zero()}
                    changed = True
                    break
        if not r:
            continue
        c0 = min(c for c in r if c < ncols) if any(c < ncols for c in r) else None
        if c0 is None:
            return piv, True                                      # 0 = nonzero rhs
        inv = K.inv(r[c0])
        r = {c: K.red(v * inv) for c, v in r.items()}
        # back-substitute into existing pivots
        for pc, pr in piv.items():
            if c0 in pr:
                f = pr[c0]
                for cc, vv in r.items():
                    pr[cc] = K.red(pr.get(cc, ZERO) - f * vv)
                for cc in [cc for cc, vv in pr.items() if vv.is_zero()]:
                    del pr[cc]
        piv[c0] = r
    return piv, False


def nullspace(rows, K, ncols):
    piv, _ = rref(rows, K, ncols)
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for fc in free:
        v = {fc: Q([1])}
        for pc, pr in piv.items():
            if fc in pr:
                v[pc] = K.red(-pr[fc])
        basis.append(v)
    return basis


def matvec(Lrows, v, K):
    out = []
    for r in Lrows:
        acc = ZERO
        for c, x in r.items():
            if c in v:
                acc = acc + x * v[c]
        out.append(K.red(acc))
    return out


# ---------------------------------------------------------------- the certificate
def build(base, quiet=False):
    t00 = time.time()
    log = (lambda *a: None) if quiet else (lambda *a: print(*a, flush=True))
    P = setup(base)
    n, K, X, Y, C, S_, num, iv, Sk = (P[k] for k in ('n', 'K', 'X', 'Y', 'C', 'S', 'num', 'iv', 'Sk'))
    ct = P['ct']
    H = F(1, 2)
    MUT = __import__('os').environ.get('GRADEC_MUTATE', '')
    if MUT == 'tight':                                              # rejection test: move one square by 1e-30
        j0 = ct['load_bearing'][0][1]
        X[j0] = K.red(X[j0] + Q([q(F(1, 10 ** 30))]))
    Xn, Yn, Cn, Snn = ([float(num(p)) for p in arr] for arr in (X, Y, C, S_))
    # rows: every load-bearing incidence; side-end incidences must come as the two corners of one side of j
    A = [tuple(a) for a in ct['load_bearing']]
    rows, ends, dropped, beyond = [], {}, [], []

    def rot0(c, s_, p):
        return (c * q(p[0]) - s_ * q(p[1]), s_ * q(p[0]) + c * q(p[1]))
    for a in A:
        if a[0] == 'W':
            rows.append(a); continue
        _, j, ai, i, k = a                                        # tau exactly in K: position along i's side
        rx, ry = rot0(C[j], S_[j], (H * geom.CU[ai][0], H * geom.CU[ai][1]))
        e = geom.EK[(k + 1) % 4]
        mx, my = C[i] * e[0] - S_[i] * e[1], S_[i] * e[0] + C[i] * e[1]
        tau = K.red(mx * (X[j] + rx - X[i]) + my * (Y[j] + ry - Y[i]))
        d = K.red(tau * tau - Q([q(F(1, 4))]))
        if d.is_zero():
            ends.setdefault((j, i, k), []).append(a)              # exactly at a side end
        else:
            sg = sign(iv(d))
            assert sg != 0, f'cannot decide the side position of {a}'
            if sg < 0:
                rows.append(a)                                     # strictly inside the side
            else:
                beyond.append(a)                                   # beyond the side end: not a valid row; dropped
    end_rows = []
    for key, inc in ends.items():
        if len(inc) == 2 and (inc[0][2] - inc[1][2]) % 4 in (1, 3):
            rows += inc; end_rows += inc
        else:
            dropped += inc                                       # corner-corner touches: never rows (dropping is allowed)
    if MUT == 'droprow':                                            # rejection test: drop every right-wall row
        rows = [r for r in rows if not (r[0] == 'W' and r[3] == 'R')]
    lb = sorted({r[1] for r in rows} | {r[3] for r in rows if r[0] == 'C'})
    var = {}
    for i in lb:
        for c in range(3):
            var[3 * i + c] = len(var)
    var[3 * n] = len(var)
    N, m = len(var), len(rows)
    sv_ = N - 1
    log(f'{base}: {m} rows ({len(end_rows)} side-end, {len(dropped)} dropped corner-corner, {len(beyond)} dropped beyond a side end), {len(lb)} load-bearing '
        f'squares, {N} variables')

    def rot(c, s, p):
        return (c * q(p[0]) - s * q(p[1]), s * q(p[0]) + c * q(p[1]))

    def nrm(i, k):
        e = geom.EK[k]
        return (C[i] * e[0] - S_[i] * e[1], S_[i] * e[0] + C[i] * e[1])

    def pt(a):
        return (H * geom.CU[a][0], H * geom.CU[a][1])

    def value(r):
        if r[0] == 'W':
            _, j, a, w = r
            rx, ry = rot(C[j], S_[j], pt(a))
            return K.red({'L': X[j] + rx, 'R': Sk - X[j] - rx, 'B': Y[j] + ry, 'T': Sk - Y[j] - ry}[w])
        _, j, a, i, k = r
        nx, ny = nrm(i, k)
        rx, ry = rot(C[j], S_[j], pt(a))
        return K.red(nx * (X[j] + rx - X[i]) + ny * (Y[j] + ry - Y[i]) - Q([q(H)]))

    def lin(r, Xc=X, Yc=Y):
        if r[0] == 'W':
            _, j, a, w = r
            rx, ry = rot(C[j], S_[j], pt(a))
            jr = (-ry, rx)
            L = {'L': {3 * j: Q([1]), 3 * j + 2: jr[0]}, 'R': {3 * n: Q([1]), 3 * j: Q([-1]), 3 * j + 2: -jr[0]},
                 'B': {3 * j + 1: Q([1]), 3 * j + 2: jr[1]}, 'T': {3 * n: Q([1]), 3 * j + 1: Q([-1]), 3 * j + 2: -jr[1]}}[w]
        else:
            _, j, a, i, k = r
            nx, ny = nrm(i, k)
            rx, ry = rot(C[j], S_[j], pt(a))
            Px, Py = Xc[j] + rx - Xc[i], Yc[j] + ry - Yc[i]
            L = {3 * j: nx, 3 * j + 1: ny, 3 * i: -nx, 3 * i + 1: -ny,
                 3 * i + 2: -ny * Px + nx * Py, 3 * j + 2: nx * (-ry) + ny * rx}
        out = {}
        for v, c in L.items():
            out[var[v]] = K.red(out.get(var[v], ZERO) + c)
        return {v: c for v, c in out.items() if not c.is_zero()}

    def hess(r):                                                    # list of (v1, v2, value), unordered pairs once
        if r[0] == 'W':
            _, j, a, w = r
            ox, oy = rot(C[j], S_[j], pt(a))
            tj = var[3 * j + 2]
            return [(tj, tj, {'L': -ox, 'R': ox, 'B': -oy, 'T': oy}[w])]
        _, j, a, i, k = r
        nx, ny = nrm(i, k)
        npx, npy = -ny, nx
        ox, oy = rot(C[j], S_[j], pt(a))
        dx, dy = X[j] + ox - X[i], Y[j] + oy - Y[i]
        ppx, ppy = -oy, ox
        xi, yi, ti, xj, yj, tj = (var[3 * i], var[3 * i + 1], var[3 * i + 2], var[3 * j], var[3 * j + 1], var[3 * j + 2])
        return [(ti, ti, -(nx * dx + ny * dy)), (ti, xi, -npx), (ti, yi, -npy), (ti, xj, npx), (ti, yj, npy),
                (ti, tj, npx * ppx + npy * ppy), (tj, tj, -(nx * ox + ny * oy))]

    if __import__('os').environ.get('GRADEC_DROPZERO'):
        # Drop rows that carry zero force in every multiplier vector (numerical LP: maximise the number of rows with
        # lambda >= t, 0 <= t <= 1, in the cone L^T lambda = c e_S).  Dropping constraints only relaxes the problem,
        # so a certificate for the smaller row set is one for the record.  A side-end pair is dropped as a whole.
        from scipy.optimize import linprog
        Ln = np.zeros((m, N))
        for a, r in enumerate(rows):
            for c, v in lin(r).items():
                Ln[a, c] = float(num(v))
        es = np.zeros(N); es[sv_] = 1
        res = linprog(np.r_[np.zeros(m), -np.ones(m), 0], A_eq=np.c_[Ln.T, np.zeros((N, m)), -es], b_eq=np.zeros(N),
                      A_ub=np.c_[-np.eye(m), np.eye(m), np.zeros(m)], b_ub=np.zeros(m),
                      bounds=[(0, None)] * m + [(0, 1)] * m + [(0, None)], method='highs')
        assert res.status == 0 and res.x[-1] > 0, 'e_S is not in the cone of the rows'
        zero = {rows[a] for a in range(m) if res.x[m + a] < 1e-7}
        for key, inc in ends.items():
            if any(r in zero for r in inc):
                zero |= set(inc)
        rows = [r for r in rows if r not in zero]
        end_rows = [r for r in end_rows if r not in zero]
        lb = sorted({r[1] for r in rows} | {r[3] for r in rows if r[0] == 'C'})
        var.clear()
        for i in lb:
            for c in range(3):
                var[3 * i + c] = len(var)
        var[3 * n] = len(var)
        N, m = len(var), len(rows)
        sv_ = N - 1
        log(f'  dropped {len(zero)} zero-force rows: {sorted(zero, key=str)}; now {m} rows, {len(lb)} load-bearing '
            f'squares, {N} variables')

    # (0) every row tight at z*, exactly
    for r in rows:
        assert value(r).is_zero(), f'row {r} not tight at the record'
    L0 = [lin(r) for r in rows]
    # (1) margins: interior incidences project strictly inside their side; side-end pairs: the edge of j along i's side
    margins = []
    for r in rows:
        if r[0] == 'C' and r not in end_rows:
            _, j, a, i, k = r
            rx, ry = rot(C[j], S_[j], pt(a))
            Px, Py = K.red(X[j] + rx - X[i]), K.red(Y[j] + ry - Y[i])
            mx, my = nrm(i, (k + 1) % 4)
            tv = iv(K.red(mx * Px + my * Py))
            margins.append(F(1, 2) - max(abs(tv.lo), abs(tv.hi)))
    mu = min(margins) if margins else F(1, 2)
    assert mu > 0, 'an interior incidence does not project strictly inside its side'
    for r in end_rows:                                              # exactly at a side end (|tau| = 1/2 in K)
        _, j, a, i, k = r
        rx, ry = rot(C[j], S_[j], pt(a))
        Px, Py = K.red(X[j] + rx - X[i]), K.red(Y[j] + ry - Y[i])
        mx, my = nrm(i, (k + 1) % 4)
        tau = K.red(mx * Px + my * Py)
        assert K.red(tau * tau - Q([q(F(1, 4))])).is_zero(), f'side-end row {r} not exactly at a side end'
    log(f'  (1) rows tight exactly; interior projection margin {float(mu):.4g}; {len(end_rows) // 2} side-end pairs '
        f'exactly at side ends')
    # flat family F: null space of the position columns
    pos = sorted(var[3 * i + c] for i in lb for c in (0, 1))
    Lpos = [{c: v for c, v in r.items() if c in set(pos)} for r in L0]
    Fb = nullspace(Lpos, K, N)
    Fb = [v for v in Fb if all(c in set(pos) for c in v)]
    # position null space restricted to position columns: recompute on the position-only subproblem
    pidx = {c: k for k, c in enumerate(pos)}
    Fb = nullspace([{pidx[c]: v for c, v in r.items()} for r in Lpos], K, len(pos))
    Fb = [{pos[c]: v for c, v in b.items()} for b in Fb]
    f = len(Fb)
    moving = sorted({lb[pos.index(c) // 2] for b in Fb for c in b})
    # full null space of L0
    Nb = nullspace(L0, K, N)
    r0 = N - len(Nb)
    log(f'  rank L0 {r0}, dim null {len(Nb)}, dim F {f} (moving squares {moving})')
    # A_k: derivative of L along each F basis vector (only the torque column of i in C rows)
    Ak = []
    for b in Fb:
        Xp = [K.red(X[i] + b.get(var[3 * i], ZERO)) if i in lb else X[i] for i in range(n)]
        Yp = [K.red(Y[i] + b.get(var[3 * i + 1], ZERO)) if i in lb else Y[i] for i in range(n)]
        Ak.append([{c: K.red(v - L0[a].get(c, ZERO)) for c, v in lin(rows[a], Xp, Yp).items()
                    if not K.red(v - L0[a].get(c, ZERO)).is_zero()} for a in range(m)])
    # (2) null vectors: unknowns w0 (block 0) and w_k (block k), each length N
    nb = N * (1 + f)
    eqs = []
    for a in range(m):
        eqs.append({c: v for c, v in L0[a].items()})                                      # L0 w0 = 0
    for k in range(f):
        for a in range(m):
            e = {N * (1 + k) + c: v for c, v in L0[a].items()}                            # L0 w_k + A_k w0 = 0
            for c, v in Ak[k][a].items():
                e[c] = K.red(e.get(c, ZERO) + v)
            eqs.append(e)
    for k in range(f):
        for l in range(k, f):
            for a in range(m):
                e = {}
                for c, v in Ak[k][a].items():                                            # A_k w_l + A_l w_k = 0
                    e[N * (1 + l) + c] = K.red(e.get(N * (1 + l) + c, ZERO) + v)
                for c, v in Ak[l][a].items():
                    e[N * (1 + k) + c] = K.red(e.get(N * (1 + k) + c, ZERO) + v)
                eqs.append({c: v for c, v in e.items() if not v.is_zero()})
    t0 = time.time()
    sols = nullspace(eqs, K, nb)
    # choose solutions whose w0 parts extend F to a basis of null L0
    span = [dict(b) for b in Fb]
    chosen = []

    def rank_of(vecs):
        if not vecs:
            return 0
        piv, _ = rref([dict(v) for v in vecs], K, N)
        return len(piv)
    for s in sols:
        w0 = {c: v for c, v in s.items() if c < N}
        if not w0:
            continue
        if rank_of(span + [w0]) > len(span):
            span.append(w0); chosen.append(s)
        if len(span) == len(Nb):
            break
    dimW = len(chosen)
    assert len(span) == len(Nb), f'null vectors cover only {len(span)} of dim null {len(Nb)}'
    for s in chosen:
        for blk in range(1 + f):
            assert s.get(N * blk + sv_, ZERO).is_zero(), 'a null vector has a nonzero S component'
    # re-verify the identities directly (independent of the elimination)
    for s in chosen:
        w0 = {c: v for c, v in s.items() if c < N}
        wk = [{c - N * (1 + k): v for c, v in s.items() if N * (1 + k) <= c < N * (2 + k)} for k in range(f)]
        assert all(x.is_zero() for x in matvec(L0, w0, K))
        for k in range(f):
            assert all(K.red(x + y).is_zero() for x, y in zip(matvec(L0, wk[k], K), matvec(Ak[k], w0, K)))
            for l in range(k, f):
                assert all(K.red(x + y).is_zero() for x, y in zip(matvec(Ak[k], wk[l], K), matvec(Ak[l], wk[k], K)))
    for b in Fb:
        assert all(x.is_zero() for x in matvec(L0, b, K))
    log(f'  (2) {dimW} affine null vectors w_j(phi) (S-components 0) + F span null L0; identities exact '
        f'({time.time() - t0:.1f} s)')
    # multipliers lambda* > 0: numerical max-min, rationalised non-basis, exact basis solve
    Ln = np.zeros((m, N))
    for a, r in enumerate(L0):
        for c, v in r.items():
            Ln[a, c] = float(num(v))
    from scipy.optimize import linprog
    import scipy.linalg as sla
    es = np.zeros(N); es[sv_] = 1
    res = linprog(np.r_[np.zeros(m), -1], A_eq=np.c_[Ln.T, np.zeros(N)], b_eq=es,
                  A_ub=np.c_[-np.eye(m), np.ones(m)], b_ub=np.zeros(m), bounds=[(None, None)] * (m + 1), method='highs')
    assert res.status == 0 and res.x[-1] > 1e-9, 'no strictly positive multipliers'
    lam_n = res.x[:m]
    _, _, pv = sla.qr(Ln.T, pivoting=True)
    basis = sorted(pv[:r0])
    nonb = [a for a in range(m) if a not in basis]
    lam = {a: Q([q(F(round(lam_n[a] * 10 ** 12), 10 ** 12))]) for a in nonb}
    # equations over variables: sum_{b in basis} lam_b L_b[v] = e_S[v] - sum_nonb lam_a L_a[v]
    bidx = {b: k for k, b in enumerate(basis)}
    sys_rows = []
    for v in range(N):
        e = {}
        for b in basis:
            if v in L0[b]:
                e[bidx[b]] = L0[b][v]
        rhs = K.red((Q([1]) if v == sv_ else ZERO) - sum((lam[a] * L0[a].get(v, ZERO) for a in nonb), ZERO))
        if not rhs.is_zero():
            e[len(basis)] = rhs
        sys_rows.append(e)
    piv, bad = rref(sys_rows, K, len(basis))
    assert not bad and len(piv) == len(basis), 'KKT system for the basis multipliers is inconsistent or singular'
    for b in basis:
        lam[b] = piv[bidx[b]].get(len(basis), ZERO)
    for v in range(N):
        tot = K.red(sum((lam[a] * L0[a].get(v, ZERO) for a in range(m)), ZERO))
        assert tot == (Q([1]) if v == sv_ else ZERO), f'KKT identity fails at variable {v}'
    lam_iv = [iv(lam[a]) for a in range(m)]
    lam_min = min(x.lo for x in lam_iv)
    assert lam_min > 0, 'a multiplier is not proved positive'
    log(f'  (2) exact multipliers lambda* at z*: min {float(lam_min):.4g} (all proved > 0)')
    # (3) reduced Hessian on W = span of the chosen w_j0
    Hm = {}
    for a, r in enumerate(rows):
        for v1, v2, val in hess(r):
            for (p1, p2) in ((v1, v2), (v2, v1)) if v1 != v2 else ((v1, v2),):
                Hm[(p1, p2)] = K.red(Hm.get((p1, p2), ZERO) - lam[a] * K.red(val))
    if MUT == 'neghess':                                            # rejection test: negated Hessian
        Hm = {k_: K.red(-v) for k_, v in Hm.items()}
    W0 = [{c: v for c, v in s.items() if c < N} for s in chosen]
    Qw = [[K.red(sum((W0[i_].get(p1, ZERO) * h * W0[j_].get(p2, ZERO) for (p1, p2), h in Hm.items()), ZERO))
           for j_ in range(dimW)] for i_ in range(dimW)]
    # leading principal minors (exact in K), signs by intervals
    minors = []
    for k in range(1, dimW + 1):
        M = [row[:k] for row in Qw[:k]]
        det = ZERO
        for perm in itertools.permutations(range(k)):
            sgn = (-1) ** sum(1 for x in range(k) for y in range(x + 1, k) if perm[x] > perm[y])
            term = Q([sgn])
            for x in range(k):
                term = K.red(term * M[x][perm[x]])
            det = K.red(det + term)
        minors.append(iv(det))
    pd = all(sign(x) > 0 for x in minors)
    assert pd, f'reduced Hessian on W not proved positive definite: minors {[(float(x.lo), float(x.hi)) for x in minors]}'
    log(f'  (3) reduced Hessian on W (dim {dimW}) positive definite: leading minors '
        f'{[f"{float(x.lo):.4g}" for x in minors]}')
    log(f'  => grade C certificate VALID: local minimum, strict modulo the {f}-dim flat family ({time.time() - t00:.0f} s)')
    out = {'n': n, 'rows': [list(r) for r in rows], 'dropped_corner_corner': [list(r) for r in dropped], 'dropped_beyond_side_end': [list(r) for r in beyond],
           'load_bearing_squares': lb, 'rank_L0': r0, 'dim_F': f, 'moving_squares': moving, 'dim_W': dimW,
           'lambda_min': float(lam_min), 'margin': float(mu),
           'hessian_minors': [[float(x.lo), float(x.hi)] for x in minors], 'valid': True}
    json.dump(out, open(base + '.gradec.json', 'w'))
    return out


if __name__ == '__main__':
    for b in sys.argv[1:]:
        build(b)
