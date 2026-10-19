"""Grade-A local-minimum certificates: first-order rigid packings with strictly positive contact forces.

Claim (for the exact configuration of NAME.minpoly.json): there is eps > 0 such that every valid packing in [0, s]^2
whose centres are within eps of the record's and whose angles are within eps (mod 90 deg) has s >= S*.

Rows.  Each row is "point p (local coordinates) of closed square j lies on or beyond the line of side k of square i"
(h = n_ik . (P - c_i) - 1/2 >= 0), valid near the record whenever P projects strictly inside that side at the record
(|tau| < 1/2: then P outside the open square i forces exactly this side), or "corner of j inside the box" (wall).
Load-bearing incidences with the corner strictly inside the side are rows as they are; incidences at a side end come
in pairs on one line (aligned side-side contacts) and are replaced by the midpoint of the two corners (their average:
the midpoint projects to the middle of the side).

Coordinates Delta = (dx_i, dy_i, w_i = sin(delta_i), dS).  h_r = L_r . Delta + O(|Delta|^2) with a universal constant.
Certificate: lambda in K with sum lambda_r L_r = e_S exactly and lambda_r > 0; a rational G with ||G L - I||_inf <= 1/2
(so L is injective with |Delta| <= 2 ||G|| |L Delta|); margins 1/2 - |tau| > 0 for the point rows.  Then
s < S* near the record is impossible (rigidity lemma: |Delta| <= C |Delta|^2).

  python3 localmin.py minpoly/solve/n-11        (needs n-11.minpoly.json, n-11.contacts.json, n-11.exact.txt)
"""
import sys, json
from fractions import Fraction as F
import flint
from mpmath import mp, mpf
import numpy as np
import geom
from verify_exact import I, ev_iv, rdn, rup

Q = flint.fmpq_poly


def q(x):
    x = F(x)
    return flint.fmpq(x.numerator, x.denominator)


class Kf:
    def __init__(self, f):
        self.f = Q([q(c) for c in f])

    def red(self, p):
        return p % self.f

    def inv(self, p):
        g, a, _ = (p % self.f).xgcd(self.f)
        assert g.degree() == 0
        return self.red(a / g.coeffs()[0])

    def poly(self, coeffs):
        return self.red(Q([q(c) for c in coeffs]))


def build(base, quiet=False):
    log = (lambda *a: None) if quiet else print
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
    # exact record data in K: centres, (c, s)
    X, Y, C, S_ = [], [], [], []
    for sq in D['squares']:
        X.append(K.poly(sq['x']))
        Y.append(K.poly(sq['y']))
        u = K.poly(sq['u'])
        d = K.red(Q([1]) + u * u)
        di = K.inv(d)
        c, s = K.red((Q([1]) - u * u) * di), K.red(Q([0, 2]) * u * di) if False else K.red(Q([2]) * u * di)
        for _ in range(sq['m'] % 4):
            c, s = -s, c
        C.append(c)
        S_.append(s)
    # numerical point (for row classification and G)
    mp.dps = 60
    tnum = mpf(D['field']['t_approx'])
    num = lambda p: sum(mpf(int(c.p)) / int(c.q) * tnum ** i for i, c in enumerate(p.coeffs())) if not p.is_zero() else mpf(0)
    Xn, Yn, Cn, Sn = ([float(num(p)) for p in arr] for arr in (X, Y, C, S_))
    Snum = float(num(K.poly(D['S']['in_K'])))
    H = F(1, 2)
    CU = geom.CU
    # rows from the load-bearing set
    A = [tuple(a) for a in ct['load_bearing']]
    rows, ends = [], {}
    for a in A:
        if a[0] == 'W':
            _, j, ai, w = a
            rows.append(('W', j, (H * CU[ai][0], H * CU[ai][1]), w))
            continue
        tau = geom.tangential(a, Xn, Yn, Cn, Sn, 0.5)
        if abs(abs(tau) - 0.5) < 1e-9:
            ends.setdefault((a[1], a[3], a[4]), []).append(a)
        else:
            _, j, ai, i, k = a
            rows.append(('P', j, (H * CU[ai][0], H * CU[ai][1]), i, k))
    aligned = {}
    for (j, i, k), inc in ends.items():
        if len(inc) != 2:
            raise RuntimeError(f'a lone side-end incidence {inc}: a corner-corner contact, not handled')
        p1, p2 = CU[inc[0][2]], CU[inc[1][2]]
        aligned.setdefault(frozenset((i, j)), []).append(('P', j, (H * (p1[0] + p2[0]) / 2, H * (p1[1] + p2[1]) / 2), i, k))
    for pair, rs in aligned.items():
        rows.append(rs[0])                                         # one midpoint row per aligned pair
    log(f'{base}: {len(rows)} rows ({len(aligned)} aligned pairs as midpoint rows), variables {3 * n + 1}')

    # linear parts (exact, in K): variables x_i -> 3i, y_i -> 3i+1, w_i -> 3i+2, S -> 3n
    N = 3 * n + 1
    zero = Q([0])

    def rot(c, s, p):                                              # R(c, s) p, p rational pair
        return (c * q(p[0]) - s * q(p[1]), s * q(p[0]) + c * q(p[1]))

    def nrm(i, k):
        e = geom.EK[k]
        return (C[i] * e[0] - S_[i] * e[1], S_[i] * e[0] + C[i] * e[1])

    def lin(row):
        L = {}
        if row[0] == 'W':
            _, j, p, w = row
            rx, ry = rot(C[j], S_[j], p)
            jr = (-ry, rx)                                         # J R_j p
            if w == 'L':
                L = {3 * j: Q([1]), 3 * j + 2: jr[0]}
            elif w == 'R':
                L = {N - 1: Q([1]), 3 * j: Q([-1]), 3 * j + 2: -jr[0]}
            elif w == 'B':
                L = {3 * j + 1: Q([1]), 3 * j + 2: jr[1]}
            else:
                L = {N - 1: Q([1]), 3 * j + 1: Q([-1]), 3 * j + 2: -jr[1]}
            return {v: K.red(c) for v, c in L.items()}
        _, j, p, i, k = row
        nx, ny = nrm(i, k)
        rx, ry = rot(C[j], S_[j], p)
        Px, Py = K.red(X[j] + rx - X[i]), K.red(Y[j] + ry - Y[i])
        L = {3 * j: nx, 3 * j + 1: ny, 3 * i: -nx, 3 * i + 1: -ny,
             3 * i + 2: K.red(-ny * Px + nx * Py),                 # (J n) . (P - c_i)
             3 * j + 2: K.red(nx * (-ry) + ny * rx)}               # n . (J R_j p)
        return {v: K.red(c) for v, c in L.items()}

    def value(row):                                                # h at the record (must be 0)
        if row[0] == 'W':
            _, j, p, w = row
            rx, ry = rot(C[j], S_[j], p)
            Sk = K.poly(D['S']['in_K'])
            return K.red({'L': X[j] + rx, 'R': Sk - X[j] - rx, 'B': Y[j] + ry, 'T': Sk - Y[j] - ry}[w])
        _, j, p, i, k = row
        nx, ny = nrm(i, k)
        rx, ry = rot(C[j], S_[j], p)
        return K.red(nx * (X[j] + rx - X[i]) + ny * (Y[j] + ry - Y[i]) - Q([q(H)]))

    def taus(row):                                                 # the adjacent side values at P
        _, j, p, i, k = row
        rx, ry = rot(C[j], S_[j], p)
        Px, Py = K.red(X[j] + rx - X[i]), K.red(Y[j] + ry - Y[i])
        out = []
        for kk in ((k + 1) % 4, (k + 3) % 4):
            mx, my = nrm(i, kk)
            out.append(K.red(mx * Px + my * Py))
        return out

    Ls = [lin(r) for r in rows]
    for r in rows:
        assert value(r).is_zero(), f'row {r} not tight at the record'
    # numerical L, max-min lambda, then exact lambda
    Ln = np.zeros((len(rows), N))
    for a, L in enumerate(Ls):
        for v, c in L.items():
            Ln[a, v] = float(num(c))
    from scipy.optimize import linprog
    m = len(rows)
    es = np.zeros(N)
    es[N - 1] = 1
    res = linprog(np.r_[np.zeros(m), -1], A_eq=np.c_[Ln.T, np.zeros(N)], b_eq=es,
                  A_ub=np.c_[-np.eye(m), np.ones(m)], b_ub=np.zeros(m), bounds=[(None, None)] * (m + 1), method='highs')
    if res.status != 0 or res.x[-1] <= 1e-9:
        raise RuntimeError('no strictly positive multipliers on the rows')
    lam_n = res.x[:m]
    rank = np.linalg.matrix_rank(Ln, tol=1e-9)
    if rank < N:
        raise RuntimeError(f'rows not first-order rigid: rank {rank} of {N}')
    # basis of N rows (QR with pivoting on L^T), others fixed at rationals near lam_n; solve the basis exactly in K
    import scipy.linalg as sla
    _, _, piv = sla.qr(Ln.T, pivoting=True)
    basis = sorted(piv[:N])
    nonb = [a for a in range(m) if a not in basis]
    lam = {a: Q([q(F(round(lam_n[a] * 10 ** 12), 10 ** 12))]) for a in nonb}
    # system: sum_{b in basis} lam_b L_b[v] = e_S[v] - sum_{a nonb} lam_a L_a[v]
    M = [[Ls[b].get(v, zero) for b in basis] for v in range(N)]
    rhs = [K.red((Q([1]) if v == N - 1 else zero) - sum((lam[a] * Ls[a].get(v, zero) for a in nonb), zero))
           for v in range(N)]
    # Gaussian elimination over K
    Mx = [row[:] + [rhs[v]] for v, row in enumerate(M)]
    for col in range(N):
        pr = max(range(col, N), key=lambda r_: abs(float(num(Mx[r_][col]))))
        Mx[col], Mx[pr] = Mx[pr], Mx[col]
        inv = K.inv(Mx[col][col])
        Mx[col] = [K.red(x * inv) for x in Mx[col]]
        for r_ in range(N):
            if r_ != col and not Mx[r_][col].is_zero():
                fac = Mx[r_][col]
                Mx[r_] = [K.red(x - fac * y) for x, y in zip(Mx[r_], Mx[col])]
    for idx, b in enumerate(basis):
        lam[b] = Mx[idx][N]
    # checks: exact KKT identity, positivity by intervals
    for v in range(N):
        tot = K.red(sum((lam[a] * Ls[a].get(v, zero) for a in range(m)), zero))
        assert tot == (Q([1]) if v == N - 1 else zero), f'KKT identity fails at variable {v}'

    def iv(p):
        return ev_iv([F(int(c.p), int(c.q)) for c in p.coeffs()], T) if not p.is_zero() else I(0)
    lam_iv = [iv(lam[a]) for a in range(m)]
    lam_min = min(x.lo for x in lam_iv)
    assert lam_min > 0, 'a multiplier is not proved positive'
    # G: rational approximate left inverse of L (from the numerical pseudo-inverse); ||G L - I||_inf <= 1/2
    Gn = np.linalg.pinv(Ln)
    G = [[F(round(Gn[v, a] * 10 ** 9), 10 ** 9) for a in range(m)] for v in range(N)]
    Liv = [[iv(Ls[a][v]) if v in Ls[a] else I(0) for v in range(N)] for a in range(m)]
    worst = F(0)
    for v in range(N):
        rs = F(0)
        for w_ in range(N):
            acc = I(-1 if v == w_ else 0)
            for a in range(m):
                if G[v][a] and w_ in Ls[a]:
                    acc = acc + Liv[a][w_] * G[v][a]
            rs += max(abs(acc.lo), abs(acc.hi))
        worst = max(worst, rs)
    assert worst <= F(1, 2), f'||G L - I|| = {float(worst)} > 1/2'
    Gnorm = max(sum(abs(x) for x in row) for row in G)
    # margins of the point rows
    margins = []
    for r in rows:
        if r[0] == 'P':
            for tv in taus(r):
                x = iv(tv)
                margins.append(F(1, 2) - max(abs(x.lo), abs(x.hi)))
    mu = min(margins)
    assert mu > 0, 'a point does not project strictly inside its side'
    Lam = sum(x.hi for x in lam_iv)
    out = {'n': n, 'rows': [list(r[:2]) + [[str(r[2][0]), str(r[2][1])]] + list(r[3:]) for r in rows],
           'lambda_min': float(lam_min), 'lambda_sum': float(Lam), 'G_norm': float(Gnorm),
           'GL_minus_I': float(worst), 'margin': float(mu)}
    log(f'  exact multipliers: min {float(lam_min):.4g} (sum {float(Lam):.4g}); rational left inverse ||G|| = '
        f'{float(Gnorm):.4g}, ||GL - I|| = {float(worst):.3g}; projection margin {float(mu):.4g}')
    log(f'  => grade A certificate VALID (strict local minimum in a pose-space ball)')
    json.dump(out, open(base + '.localmin.json', 'w'))
    out['_internal'] = {'rows': rows, 'lam': lam, 'C': C, 'S': S_, 'G': G, 'Ls': Ls, 'N': N, 'm': m,
                        'lam_min': lam_min, 'Lam': Lam, 'Gnorm': Gnorm, 'mu': mu, 'K': K}
    return out


if __name__ == '__main__':
    for b in sys.argv[1:]:
        build(b)
