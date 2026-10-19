#!/usr/bin/env python3
"""Display regularization of record packings (prototype, 2026-10-09; log: REGULARIZE.md).

Not a result: a derived *drawing* of a certified packing at the same side S*.  Nothing here changes a certificate.

Pipeline per packing (input: the 80-digit KKT point of search/exact/batch/work/n-N/{witness,polished}.exact.txt):
  1. orient   pick one of the 8 symmetries of the container (scoring rule, ties reported)
  2. angles   display angle groups = classes of theta mod 90 in (-45, 45] equal to 1e-50 (theta and -theta distinct);
              free (force-free) squares are re-assigned to an existing group if a feasible placement exists
  3. place    translation LP at fixed angles and fixed S*: with the angles fixed, each non-overlap condition along a
              chosen separating face normal is linear in the centres, so every LP point is a true packing (exact, not
              linearized).  Objective = "gravity" toward a home corner; symmetry of the rigid part optionally imposed.
              Iterated with a trust region (separating normals re-chosen at each step).
  4. refine   the LP vertex is re-solved at 80 digits from its tight constraints (iterative refinement)
  5. verify   all pairs (separating-axis gap) and walls at 80 digits: min gap >= -1e-50

Usage:  reg.py N [--gravity yx|xy|sum] [--sym on|off] [--orient best|K] [--merge on|off] [--svg out.svg]
"""
import argparse, json, math, os, sys
import numpy as np
import mpmath as mpm
from mpmath import mp, mpf
from scipy.optimize import linprog

mp.dps = 80
HERE = os.path.dirname(os.path.abspath(__file__))
BATCH = os.path.join(HERE, '..', 'exact', 'batch')
H = 0.5
EQ_TOL = mpf('1e-50')
NEAR_DEG, NEAR_GAP = 1.0, 1e-8     # see place()          # angle equality / verification threshold at 80 digits (input carries ~70)


# ----------------------------------------------------------------------------------------------- input

REFRESH = os.path.join(HERE, '..', '..', 'runs', 'regularize', 'exact')


def refreshed(n):
    """Base path of a refreshed, certified input (refresh.py: best known packing from the store), or None."""
    d = os.path.join(REFRESH, f'n-{n}')
    for stem in ('input', 'polished'):
        j = os.path.join(d, stem + '.json')
        if os.path.exists(j) and os.path.exists(os.path.join(d, stem + '.exact.txt')):
            m = json.load(open(j))
            if m.get('cert_valid') and m.get('newton_converged', True):
                return os.path.join(d, stem)
    return None


def load(n, use_refresh=None):
    res = {r['n']: r for r in json.load(open(os.path.join(BATCH, 'results.json')))}
    r = res[n]
    base = os.path.join(BATCH, 'work', f'n-{n}', r['from_'])
    if use_refresh is None:
        use_refresh = os.environ.get('REG_REFRESH', '1') != '0'
    rb = refreshed(n) if use_refresh else None
    if rb:
        base = rb
        r = dict(r, status='KKT point (refreshed from store)', from_=os.path.basename(rb))
    lines = open(base + '.exact.txt').read().split('\n')
    S = mpf(lines[0].split()[1])
    sq = [tuple(mpf(v) for v in ln.split()) for ln in lines[1:] if ln.strip()]
    meta = json.load(open(base + '.json'))
    free = meta.get('free_squares_exact', meta.get('free_squares', [])) or []
    assert len(sq) == n
    return dict(n=n, S=S, X=[q[0] for q in sq], Y=[q[1] for q in sq], T=[fold(q[2]) for q in sq],
                free=sorted(free), status=r['status'], by=r.get('by') or [], register=r['register'])


def fold(th):
    """theta (degrees) mod 90 into (-45, 45]."""
    t = th - 90 * mpm.floor(th / 90)
    return t - 90 if t > 45 else t


# ----------------------------------------------------------------------------------------------- symmetries

def d4(P, g):
    """Image of the packing under container symmetry g = 0..7 (g & 3 quarter turns, then g & 4 mirror x -> S - x)."""
    S = P['S']
    X, Y, T = list(P['X']), list(P['Y']), list(P['T'])
    for _ in range(g & 3):                      # quarter turn ccw about the centre: (x, y) -> (S - y, x), theta + 90
        X, Y = [S - y for y in Y], list(X)
    if g & 4:
        X = [S - x for x in X]
        T = [-t for t in T]
    Q = dict(P); Q.update(X=X, Y=Y, T=[fold(t) for t in T]); Q['g'] = g
    return Q


def match(P, Q, idx, tol, atol=None):
    """Permutation p on idx with Q's square p[i] at P's square i (positions within tol, angles within atol degrees,
    default = tol); or None."""
    atol = tol if atol is None else atol
    p = {}
    used = set()
    for i in idx:
        best, bj = None, None
        for j in idx:
            if j in used:
                continue
            d = max(abs(P['X'][i] - Q['X'][j]), abs(P['Y'][i] - Q['Y'][j]))
            if d < tol and abs(fold(P['T'][i] - Q['T'][j])) < atol and (best is None or d < best):
                best, bj = d, j
        if bj is None:
            return None
        p[i] = bj; used.add(bj)
    return p


def symmetries(P, rigid):
    """Container symmetries g (1..7) mapping the rigid part onto itself to 1e-40 (with the permutation)."""
    out = []
    for g in range(1, 8):
        Q = d4(P, g)
        p = match(P, Q, rigid, mpf('1e-40'))
        if p is not None:
            out.append((g, p))
    return out


# ----------------------------------------------------------------------------------------------- angle groups

def angle_groups(T):
    """Display groups: lists of squares with equal theta mod 90 (to EQ_TOL), sorted axis first, then by size."""
    reps, mem = [], []
    for i, t in enumerate(T):
        for k, r in enumerate(reps):
            if abs(fold(t - r)) < EQ_TOL:
                mem[k].append(i); break
        else:
            reps.append(t); mem.append([i])
    order = sorted(range(len(reps)), key=lambda k: (abs(reps[k]) > EQ_TOL, -len(mem[k]), float(reps[k])))
    return [(reps[k], mem[k]) for k in order]


# ----------------------------------------------------------------------------------------------- geometry (float)

def frame(t_deg):
    a = math.radians(float(t_deg))
    return math.cos(a), math.sin(a)


def support(c, s, nx, ny):
    """Half-width of a unit square (cos c, sin s) along unit direction n."""
    return H * (abs(nx * c + ny * s) + abs(-nx * s + ny * c))


def best_normal(i, j, X, Y, CS):
    """Oriented separating normal for pair (i, j) maximizing n.(c_j - c_i) - r(n); returns (nx, ny, r, gap)."""
    dx, dy = X[j] - X[i], Y[j] - Y[i]
    best = None
    for own in (i, j):
        c, s = CS[own]
        for nx, ny in ((c, s), (-s, c)):
            if nx * dx + ny * dy < 0:
                nx, ny = -nx, -ny
            r = support(*CS[i], nx, ny) + support(*CS[j], nx, ny)
            g = nx * dx + ny * dy - r
            if best is None or g > best[3]:
                best = (nx, ny, r, g)
    return best


def overlap_free(P, tol=-1e-9):
    X, Y = [float(v) for v in P['X']], [float(v) for v in P['Y']]
    CS = [frame(t) for t in P['T']]
    n, S = P['n'], float(P['S'])
    for i in range(n):
        e = support(*CS[i], 1, 0)
        if min(X[i] - e, S - X[i] - e) < tol or min(Y[i] - support(*CS[i], 0, 1), S - Y[i] - support(*CS[i], 0, 1)) < tol:
            return False
        for j in range(i + 1, n):
            if (X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2 < 2.0001 and best_normal(i, j, X, Y, CS)[3] < tol:
                return False
    return True


# ----------------------------------------------------------------------------------------------- LP placement

def place(P, weights, sym=(), fixed=(), trust=0.5, iters=60, feas_only=False, log=None, keep=(), align=(),
          absobj=(), pins=None):
    """Translation LP at fixed angles.  weights: per-square (wx, wy) objective (minimized).  sym: list of
    (g, perm) imposed as equalities.  Returns (X, Y floats, status, info)."""
    n, S = P['n'], float(P['S'])
    X = np.array([float(v) for v in P['X']]); Y = np.array([float(v) for v in P['Y']])
    CS = [frame(t) for t in P['T']]
    E = np.array([[support(c, s, 1, 0), support(c, s, 0, 1)] for c, s in CS])
    fixed = set(fixed)
    status = 'ok'
    # Pairs with nearly equal but distinct angles that are apart in the input keep a clearance NEAR_GAP: a float LP
    # cannot see that closing a cycle of such contacts is impossible (needs equal angles); seen at n = 172, 7e-8 deg.
    X0, Y0 = X.copy(), Y.copy()
    near = set()
    if NEAR_GAP > 0:
        D20 = (X0[:, None] - X0[None, :]) ** 2 + (Y0[:, None] - Y0[None, :]) ** 2
        for i, j in zip(*[a.tolist() for a in np.nonzero(np.triu(D20 < 2.01, 1))]):
            dth = abs(fold(P['T'][i] - P['T'][j]))
            if EQ_TOL < dth < NEAR_DEG and best_normal(i, j, X0, Y0, CS)[3] > NEAR_GAP:
                near.add((i, j))
    reach = 2 * trust + math.sqrt(2) + 0.05
    for it in range(iters):
        D2 = (X[:, None] - X[None, :]) ** 2 + (Y[:, None] - Y[None, :]) ** 2
        rows, rhs = [], []
        I, J = np.nonzero(np.triu(D2 < reach ** 2, 1))
        for i, j in zip(I.tolist(), J.tolist()):
            if not (i in fixed and j in fixed):
                nx, ny, r, g = best_normal(i, j, X, Y, CS)
                rows.append({2 * i: -nx, 2 * i + 1: -ny, 2 * j: nx, 2 * j + 1: ny})
                rhs.append(r + (NEAR_GAP if (i, j) in near else 0.0))
        A = np.zeros((len(rows), 2 * n))
        for k, rw in enumerate(rows):
            for v, a in rw.items():
                A[k, v] = a
        b = np.array(rhs)
        keep_rows = []
        for (i, j), (nx, ny, r) in dict(keep).items():
            row = np.zeros(2 * n); row[2 * i] -= nx; row[2 * i + 1] -= ny; row[2 * j] += nx; row[2 * j + 1] += ny
            keep_rows.append((row, r))
        for i, j, nx, ny in align:              # face contact along n and no offset along the face: a straight chain
            for (ax, ay), r in (((nx, ny), 1.0), ((-ny, nx), 0.0)):
                row = np.zeros(2 * n); row[2 * i] -= ax; row[2 * i + 1] -= ay; row[2 * j] += ax; row[2 * j + 1] += ay
                keep_rows.append((row, r))
        lo, hi = np.empty(2 * n), np.empty(2 * n)
        for i in range(n):
            for d, Z in ((0, X), (1, Y)):
                if i in fixed:
                    lo[2 * i + d] = hi[2 * i + d] = Z[i]
                else:
                    lo[2 * i + d] = max(E[i, d], Z[i] - trust)
                    hi[2 * i + d] = min(S - E[i, d], Z[i] + trust)
                    if lo[2 * i + d] > hi[2 * i + d]:          # rounding at a wall
                        lo[2 * i + d] = hi[2 * i + d] = min(max(Z[i], E[i, d]), S - E[i, d])
                    if pins and (i, d) in pins:                 # flush on a wall (coincidence step)
                        lo[2 * i + d] = hi[2 * i + d] = pins[(i, d)]
        Aeq, beq = [], []
        for g, p in sym:
            for i in range(n):
                j, i = i, p[i]          # constraint: c_j = g(c_{p[j]}) (match: g maps p[j] onto j)
                # image of square i's centre under g must be square j's centre: affine map on (x, y)
                M, t = affine(g, S)
                for d in range(2):
                    row = np.zeros(2 * n)
                    row[2 * j + d] += 1
                    row[2 * i] -= M[d][0]; row[2 * i + 1] -= M[d][1]
                    Aeq.append(row); beq.append(t[d])
        for row, r in keep_rows:
            Aeq.append(row); beq.append(r)
        c = np.zeros(2 * n) if feas_only else np.array([w for i in range(n) for w in weights[i]])
        # absobj (i, cx, cy, w): + w (|x_i - cx| + |y_i - cy|) via auxiliary variables (pull toward a point)
        na = 2 * len(absobj)
        if na:
            A = np.hstack([A, np.zeros((A.shape[0], na))])
            extra, eb = [], []
            for k, (i, cx, cy, w) in enumerate(absobj):
                for d, cv in ((0, cx), (1, cy)):
                    for sg in (1, -1):              # t >= sg (z - c)  <=>  t - sg z >= -sg c
                        row = np.zeros(2 * n + na); row[2 * n + 2 * k + d] = 1; row[2 * i + d] = -sg
                        extra.append(row); eb.append(-sg * cv)
            A = np.vstack([A, np.array(extra)]); b = np.r_[b, eb]
            Aeq = [np.r_[row, np.zeros(na)] for row in Aeq]
            lo = np.r_[lo, np.zeros(na)]; hi = np.r_[hi, np.full(na, np.inf)]
            if not feas_only:
                c = np.r_[c, [w for (_, _, _, w) in absobj for _ in (0, 1)]]
            else:
                c = np.zeros(2 * n + na)
        res = linprog(c, A_ub=-A, b_ub=-b, A_eq=np.array(Aeq) if Aeq else None, b_eq=np.array(beq) if beq else None,
                      bounds=list(zip(lo, hi)), method='highs',
                      options=dict(primal_feasibility_tolerance=1e-10, dual_feasibility_tolerance=1e-10))
        if res.status != 0:
            return X, Y, 'infeasible', dict(iter=it, msg=res.message)
        Z = res.x[:2 * n]
        move = max(np.max(np.abs(Z[0::2] - X)), np.max(np.abs(Z[1::2] - Y)))
        X, Y = Z[0::2].copy(), Z[1::2].copy()
        if os.environ.get('REG_DEBUG'):
            print(f'  place iter {it}: move {move:.2e} obj {res.fun:.12f}', file=sys.stderr)
        if feas_only or move < 1e-11:
            break
        if it > 0 and abs(res.fun - last) < 1e-12:      # objective stalled: alternate optimal vertices
            status = 'stalled'
            break
        last = res.fun
    else:
        status = 'not converged'
    info = dict(iter=it + 1)
    if not feas_only and status != 'infeasible':
        # uniqueness probe: on the optimal face (objective <= opt + 1e-10, same constraints), min/max a fixed
        # pseudo-random direction; a spread > 1e-6 means the gravity objective does not decide the placement
        rng = np.random.default_rng(12345)
        d = np.r_[rng.standard_normal(2 * n), np.zeros(len(c) - 2 * n)]
        A_ub2 = np.vstack([-A, c[None, :]]); b_ub2 = np.r_[-b, res.fun + 1e-10]
        kw = dict(A_ub=A_ub2, b_ub=b_ub2, A_eq=np.array(Aeq) if Aeq else None, b_eq=np.array(beq) if beq else None,
                  bounds=list(zip(lo, hi)), method='highs',
                  options=dict(primal_feasibility_tolerance=1e-10, dual_feasibility_tolerance=1e-10))
        r1, r2 = linprog(d, **kw), linprog(-d, **kw)
        if r1.status == 0 and r2.status == 0:
            info['face_spread'] = float(np.max(np.abs(r1.x[:2 * n] - r2.x[:2 * n])))
    return X, Y, status, info


def affine(g, S):
    """(M, t) with image(x, y) = M (x, y) + t for container symmetry g (as in d4)."""
    M = np.eye(2); t = np.zeros(2)
    for _ in range(g & 3):
        R = np.array([[0, -1], [1, 0]]); M = R @ M; t = R @ t + np.array([S, 0])
    if g & 4:
        F = np.array([[-1, 0], [0, 1]]); M = F @ M; t = F @ t + np.array([S, 0])
    return M, t


# ----------------------------------------------------------------------------------------------- high precision

def mp_frame(t):
    a = t * mp.pi / 180
    return mp.cos(a), mp.sin(a)


def mp_support(c, s, nx, ny):
    return H * (abs(nx * c + ny * s) + abs(-nx * s + ny * c))


def refine(P, X, Y, moved, sym=(), tight_tol=1e-9):
    """Re-solve the moved squares' centres at 80 digits from the constraints tight at the float LP point.
    Unmoved squares keep their input (80-digit) coordinates.  Returns new P (mp) and a report."""
    n, S = P['n'], P['S']
    Sf = float(S)
    CSf = [frame(t) for t in P['T']]
    CSm = [mp_frame(t) for t in P['T']]
    Xm = [P['X'][i] if i not in moved else mpf(float(X[i])) for i in range(n)]
    Ym = [P['Y'][i] if i not in moved else mpf(float(Y[i])) for i in range(n)]
    # Every square is a variable: squares frozen along exact flat modes carry ~1e-17 of float noise, so equations
    # mixing them with moved squares are only consistent if they may move too (min-norm correction leaves the rest).
    mv0 = set(moved)
    moved = set(range(n))
    var = {}
    for i in sorted(moved):
        var[(i, 0)] = len(var); var[(i, 1)] = len(var)
    eqs = []                                     # (list of (var or None, coef), const) meaning sum coef*z + const = 0
    for i in moved:                              # walls
        for d, Z in ((0, X), (1, Y)):
            c, s = CSm[i]
            e = mp_support(c, s, *((1, 0) if d == 0 else (0, 1)))
            ef = float(e)
            if abs(Z[i] - ef) < tight_tol:
                eqs.append(('w', i, d, 0, e))
            if abs(Sf - ef - Z[i]) < tight_tol:
                eqs.append(('w', i, d, 1, e))
    for i in range(n):
        for j in range(i + 1, n):
            if i not in moved and j not in moved:
                continue
            if (X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2 > 2.01:
                continue
            nx, ny, r, g = best_normal(i, j, X, Y, CSf)
            if g < tight_tol:
                # recompute the same normal at 80 digits: which square's face and which of its two normals
                eqs.append(('p', i, j, nx, ny))
    if not eqs or not var:
        return P, dict(n_eq=0, n_var=len(var))

    def mp_normal(i, j, nxf, nyf):
        best, bd = None, None
        for own in (i, j):
            c, s = CSm[own]
            for nx, ny in ((c, s), (-s, c)):
                for sg in (1, -1):
                    d = abs(float(sg * nx) - nxf) + abs(float(sg * ny) - nyf)
                    if bd is None or d < bd:
                        best, bd = (sg * nx, sg * ny), d
        return best

    rows = []
    for e in eqs:
        if e[0] == 'w':
            _, i, d, side, ev = e
            rows.append(('w', i, d, side, ev))
        else:
            _, i, j, nxf, nyf = e
            nx, ny = mp_normal(i, j, nxf, nyf)
            r = mp_support(*CSm[i], nx, ny) + mp_support(*CSm[j], nx, ny)
            rows.append(('p', i, j, nx, ny, r))
    # a constraint among squares the LP did not move is kept only if it is an exact contact of the input: a true gap
    # below the float tight threshold (seen: 4.8e-11 at n = 172) would otherwise be forced shut
    def keep(rw):
        sqs = (rw[1],) if rw[0] == 'w' else (rw[1], rw[2])
        if any(q in mv0 for q in sqs):
            return True
        if rw[0] == 'w':
            _, i, d, side, ev = rw
            z = Xm[i] if d == 0 else Ym[i]
            g = z - ev if side == 0 else S - ev - z
        else:
            _, i, j, nx, ny, r = rw
            g = nx * (Xm[j] - Xm[i]) + ny * (Ym[j] - Ym[i]) - r
        return abs(g) < mpf('1e-14')
    rows = [rw for rw in rows if keep(rw)]
    symrows = []
    for g, p in sym:
        M, t = affine(g, 1.0)                    # integer M; t in units of S
        for i in range(n):
            j, i = i, p[i]          # constraint: c_j = g(c_{p[j]}) (match: g maps p[j] onto j)
            if i in moved or j in moved:
                for d in range(2):
                    symrows.append((i, j, d, M, t))

    def residuals():
        R = []
        for rw in rows:
            if rw[0] == 'w':
                _, i, d, side, ev = rw
                z = Xm[i] if d == 0 else Ym[i]
                R.append(z - ev if side == 0 else S - ev - z)
            else:
                _, i, j, nx, ny, r = rw
                R.append(nx * (Xm[j] - Xm[i]) + ny * (Ym[j] - Ym[i]) - r)
        for i, j, d, M, t in symrows:
            img = int(M[d][0]) * Xm[i] + int(M[d][1]) * Ym[i] + int(t[d]) * S
            R.append((Xm[j] if d == 0 else Ym[j]) - img)
        return R

    J = np.zeros((len(rows) + len(symrows), len(var)))
    for k, rw in enumerate(rows):
        if rw[0] == 'w':
            _, i, d, side, ev = rw
            J[k, var[(i, d)]] = 1 if side == 0 else -1
        else:
            _, i, j, nx, ny, r = rw
            for q, sg in ((i, -1), (j, 1)):
                if q in moved:
                    J[k, var[(q, 0)]] += sg * float(nx); J[k, var[(q, 1)]] += sg * float(ny)
    for k, (i, j, d, M, t) in enumerate(symrows):
        k += len(rows)
        if j in moved:
            J[k, var[(j, d)]] += 1
        if i in moved:
            J[k, var[(i, 0)]] -= M[d][0]; J[k, var[(i, 1)]] -= M[d][1]
    rank = np.linalg.matrix_rank(J, tol=1e-9)
    hist = []
    for it in range(12):
        R = residuals()
        rmax = max(abs(v) for v in R)
        hist.append(float(rmax) if rmax > 0 else 0.0)
        if rmax < mpf('1e-75'):
            break
        Rf = np.array([float(v) for v in R])
        # residual is O(1e-16) after the first step: scale to keep float precision
        scale = max(np.max(np.abs(Rf)), 1e-300)
        dz, *_ = np.linalg.lstsq(J, -Rf / scale, rcond=None)
        for (i, d), k in var.items():
            step = mpf(float(dz[k])) * mpf(scale)
            if d == 0:
                Xm[i] += step
            else:
                Ym[i] += step
    Q = dict(P); Q.update(X=Xm, Y=Ym)
    worst = []
    if hist[-1] > 1e-60:
        R = residuals()
        allrows = rows + [('s',) + tuple(r[:3]) for r in symrows]
        worst = sorted(((float(abs(v)), allrows[k][:3] if allrows[k][0] != 'p' else allrows[k][:3]) for k, v in enumerate(R)),
                       reverse=True)[:6]
    return Q, dict(n_eq=len(rows) + len(symrows), n_var=len(var), rank=int(rank), resid=hist[-1], hist=hist, worst=worst)


def verify(P):
    """80-digit check: min over pairs of the separating-axis gap and over walls; contacts counted below 1e-50."""
    n, S = P['n'], P['S']
    CS = [mp_frame(t) for t in P['T']]
    Xf, Yf = [float(v) for v in P['X']], [float(v) for v in P['Y']]
    worst = mpf(1); contacts = 0
    for i in range(n):
        c, s = CS[i]
        e = H * (abs(c) + abs(s))
        for g in (P['X'][i] - e, S - P['X'][i] - e, P['Y'][i] - e, S - P['Y'][i] - e):
            worst = min(worst, g); contacts += g < EQ_TOL
        for j in range(i + 1, n):
            if (Xf[i] - Xf[j]) ** 2 + (Yf[i] - Yf[j]) ** 2 > 2.01:
                continue
            best = None
            dx, dy = P['X'][j] - P['X'][i], P['Y'][j] - P['Y'][i]
            for own in (i, j):
                co, so = CS[own]
                for nx, ny in ((co, so), (-so, co)):
                    g = abs(nx * dx + ny * dy) - mp_support(*CS[i], nx, ny) - mp_support(*CS[j], nx, ny)
                    if best is None or g > best:
                        best = g
            worst = min(worst, best); contacts += best < EQ_TOL
    return dict(min_gap=worst, ok=worst > -EQ_TOL, contacts=contacts)


# ----------------------------------------------------------------------------------------------- orientation

def coverage_grid(P, m=120):
    """Boolean m x m grid (cell centres) of points covered by some square."""
    S = float(P['S'])
    g = (np.arange(m) + 0.5) / m * S
    GX, GY = np.meshgrid(g, g, indexing='xy')
    cov = np.zeros_like(GX, dtype=bool)
    for x, y, t in zip(P['X'], P['Y'], P['T']):
        c, s = frame(t)
        u = (GX - float(x)) * c + (GY - float(y)) * s
        v = -(GX - float(x)) * s + (GY - float(y)) * c
        cov |= (np.abs(u) <= H) & (np.abs(v) <= H)
    return GX, GY, cov


STRIP_SAG, ARC_SAG = 0.03, 0.08          # sagitta / S of the tilted squares' centre curve (see shape_of)


def shape_of(P):
    """Shape of the tilted part (centres, after the angle merge): principal axis u, quadratic fit of the normal
    offset along u.  Returns dict(sag = |sagitta| / S, cov = covariance of x, y (sign: NE vs SE), bulge = vector from
    the chord midpoint to the curve's middle (convex side), kind = strip / arc / gray / none)."""
    S = float(P['S'])
    til = [i for i, t in enumerate(P['T']) if abs(t) > EQ_TOL]
    if len(til) < 3:
        return dict(kind='none', sag=0.0, cov=0.0, bulge=(0.0, 0.0))
    Z = np.array([[float(P['X'][i]), float(P['Y'][i])] for i in til]) / S
    m = Z.mean(0)
    w, V = np.linalg.eigh(np.cov((Z - m).T))
    u, v = V[:, 1], V[:, 0]
    a, b = (Z - m) @ u, (Z - m) @ v
    c2, c1, c0 = np.polyfit(a, b, 2)
    f = lambda t: c2 * t * t + c1 * t + c0
    am = (a.max() + a.min()) / 2
    off = f(am) - (f(a.max()) + f(a.min())) / 2
    sag = abs(c2) * ((a.max() - a.min()) / 2) ** 2
    cov = float(np.mean((Z[:, 0] - m[0]) * (Z[:, 1] - m[1])))
    kind = 'strip' if sag < STRIP_SAG else 'arc' if sag > ARC_SAG else 'gray'
    # two or more separate tilted blocks of comparable size (171, 198): drawn like arcs in the sources
    sizes = sorted((len(c) for c in tilted_clusters(P)), reverse=True)
    pair = len(sizes) >= 2 and sizes[1] >= 0.25 * len(til) and sizes[1] >= 3
    if pair and kind != 'arc':
        kind = 'arc'
    return dict(kind=kind, sag=float(sag), cov=cov, bulge=(float(off * v[0]), float(off * v[1])), pair=bool(pair),
                blocks=sizes[:4])


def orient_score(P, kind=None):
    """Lexicographic key (larger = preferred), fitted to jlevy's atlas (= the source drawings; REGULARIZE.md):
      strip (or no tilted part): band runs bottom-left to top-right; empty toward the top right; toward the top;
      arc: band runs top-left to bottom-right; convex side toward the bottom left; empty toward the top right;
      gray (between): all equal -> the source drawing (final tie-break in orientations()).
    kind forces a branch ('strip', 'arc', 'source')."""
    S = float(P['S'])
    GX, GY, cov = coverage_grid(P)
    emp = ~cov
    ex, ey = (GX[emp].mean(), GY[emp].mean()) if emp.any() else (S / 2, S / 2)
    sh = shape_of(P)
    k = kind or sh['kind']
    band = float(np.sign(round(sh['cov'], 3)))
    if k in ('strip', 'none'):
        return (band, (ex + ey) / S, (ey - ex) / S)
    if k == 'arc':
        bx, by = sh['bulge']
        return (-band, round(-(bx + by), 3), (ex + ey) / S)
    return (0.0, 0.0, 0.0)


def orientations(P, kind=None):
    """All 8 images with scores, distinct images only (an image equal to an earlier one to 1e-9 is dropped)."""
    out = []
    for g in range(8):
        Q = d4(P, g)
        dup = any(match(R, Q, range(P['n']), 1e-9) is not None for _, R, _ in out)
        if not dup:
            out.append((g, Q, orient_score(Q, kind)))
    # keys compared to 1e-3 (coverage-grid noise); final tie-break: the source drawing (jlevy's orientation)
    out.sort(key=lambda z: tuple(round(v, 3) for v in z[2]) + (z[0] == 0,), reverse=True)
    return out


# ----------------------------------------------------------------------------------------------- angle merging

def merge_angles(P, free, log=print):
    """Re-assign free squares to display groups so as to have fewer groups.  Candidates for square i: the groups
    holding a force-carrying square, nearest angle first; then 0 and 45 as new groups (a new group, once used, is a
    candidate like the others).  Feasibility = the translation LP at fixed angles.  Only angles are committed;
    positions are left to place()."""
    fr = set(free)
    real = []
    for r, m in angle_groups(P['T']):
        if any(i not in fr for i in m):
            real.append(r)
    dist = lambda a, b: abs(fold(a - b))
    changes = []
    for i in free:
        t0 = P['T'][i]
        if any(dist(t0, q) < EQ_TOL for q in real):
            continue                          # already in a real group
        cands = sorted(real, key=lambda q: dist(t0, q)) + [q for q in (mpf(0), mpf(45)) if all(dist(q, r) > EQ_TOL for r in real)]
        for r in cands:
            T = list(P['T']); T[i] = fold(r)
            Q = dict(P); Q['T'] = T
            X, Y, st, _ = place(Q, None, feas_only=True, trust=0.5)
            if st == 'ok':
                changes.append((i, float(t0), float(r)))
                if all(dist(r, q) > EQ_TOL for q in real):
                    real.append(r)
                P = Q
                break
    return P, changes



# ----------------------------------------------------------------------------------------------- "pretty" rules (round 2)


ULP_DEG = 1e-12          # "equal" for angles of inexact data: a few ULPs of a double angle in degrees (45 * 2.2e-16 * ~100)
PERTURB_DEG = 1e-6       # an angle that cannot move this far either way at S* is determined by the packing


ULP_DEG = 1e-12          # "equal" for angles of inexact data: a few ULPs of a double angle in degrees (45 * 2.2e-16 * ~100)
PERTURB_DEG = 1e-6       # an angle that cannot move this far either way at S* is determined by the packing
PATH_STEP_DEG = 0.01


def path_ok(P, T_to, step=PATH_STEP_DEG, trust=0.25, radius=3.0):
    """Traversable without expansion: rotate every square from P['T'] to T_to together, linearly in angle, steps <=
    step degrees, re-solving translations at S* each step (LP from the previous positions).  Returns (ok, blocked_s,
    Q at the end or at the last feasible step).  Sufficient, not necessary (translations only, one angle path).
    NEAR_GAP is switched off: converging angles would trip it near the end."""
    global NEAR_GAP
    n = P['n']
    d = [float(fold(T_to[i] - P['T'][i])) for i in range(n)]
    big = max([abs(x) for x in d] + [0.0])
    if big < 1e-12:                            # ULP-level change: nothing to traverse, but return the new angles
        Q = dict(P); Q['T'] = list(T_to)
        return True, None, Q
    steps = max(2, int(math.ceil(big / step)))
    # only squares near the rotating ones may move (a restriction: still a sufficient test, much smaller LPs)
    mv = [i for i in range(n) if abs(d[i]) > 1e-12]
    Xf = np.array([float(v) for v in P['X']]); Yf = np.array([float(v) for v in P['Y']])
    near_mv = np.zeros(n, dtype=bool)
    for i in mv:
        near_mv |= (Xf - Xf[i]) ** 2 + (Yf - Yf[i]) ** 2 < radius ** 2
    fixed = [i for i in range(n) if not near_mv[i]]
    saved, NEAR_GAP = NEAR_GAP, 0.0
    try:
        Q = dict(P)
        for k in range(1, steps + 1):
            s_ = k / steps
            T = [fold(P['T'][i] + mpf(d[i]) * s_) if abs(d[i]) > 1e-12 else P['T'][i] for i in range(n)]
            R = dict(Q); R['T'] = T
            X, Y, st, _ = place(R, None, feas_only=True, trust=trust, fixed=fixed)
            if st != 'ok':
                X, Y, st, _ = place(R, [(0.0, 0.0)] * n, trust=trust, iters=8, fixed=fixed)
            if st == 'infeasible' and fixed:            # before giving up, let everything move
                X, Y, st, _ = place(R, [(0.0, 0.0)] * n, trust=trust, iters=8)
            if st == 'infeasible':
                return False, s_, Q
            R['X'] = [mpf(float(v)) for v in X]; R['Y'] = [mpf(float(v)) for v in Y]
            Q = R
        Q['T'] = list(T_to)
        return True, None, Q
    finally:
        NEAR_GAP = saved


def merge_determined(P, near_axis=1.0, cap=5.0, policy='free', log=print):
    """Fewer angle groups among force-carrying squares.  policy:
      'free'          (Evan 10-10: keep true rotation groups) determined angles (neither theta +- PERTURB_DEG feasible
                      at S*) are kept, merged only with a group equal to ULP_DEG; angles that are not determined are
                      reassigned to an existing group (near-axis ones straightened together first, else the nearest
                      larger group) if feasible at S*;
      'conservative'  as 'free', but every change must also be traversable without expansion from the current
                      arrangement (path_ok): the result is the same packing (level <= 2);
      'fewest'        as 'free', then determined groups too are moved to the nearest larger group within cap degrees
                      if feasible (an alternate packing at the record side may result: level 3).
    Feasible = the translation LP at S* finds a packing (refined and verified at 80 digits at the end)."""
    dist = lambda a, b: abs(fold(a - b))
    changes = []
    state = {'P': P}                       # current arrangement (positions follow accepted path moves)

    def feasible(T):
        Q = dict(state['P']); Q['T'] = T
        X, Y, st, _ = place(Q, None, feas_only=True, trust=0.5)
        return st == 'ok'

    def accept(T2, what):
        """Feasible, and (conservative) connected; on success advance the state."""
        if not feasible(T2):
            return False
        if policy == 'conservative':
            ok, sb, Q = path_ok(state['P'], T2)
            if not ok:
                changes.append(('not connected', what, round(sb, 3)))
                return False
            state['P'] = Q
        else:
            Q = dict(state['P']); Q['T'] = T2; state['P'] = Q
        return True

    def assign(T, idx, ang):
        T = list(T)
        for i in idx:
            T[i] = fold(ang)
        return T

    T = lambda: list(state['P']['T'])
    # 1. ULP-equal groups (inexact inputs): merge into the larger
    while True:
        groups = angle_groups(T())
        pair = None
        for x in range(len(groups)):
            for y in range(len(groups)):
                if x != y and dist(groups[x][0], groups[y][0]) < ULP_DEG and len(groups[x][1]) <= len(groups[y][1]):
                    pair = (groups[x], groups[y]); break
            if pair:
                break
        if not pair:
            break
        (r, m), (q, mm) = pair
        if not accept(assign(T(), m, q), ('ulp', float(r))):
            break
        changes.append(('ulp-merge', float(r), float(q), len(m)))
    # 2. groups whose angle is not determined: near-axis together first, then one by one
    movable = lambda r, m: feasible(assign(T(), m, r + PERTURB_DEG)) or feasible(assign(T(), m, r - PERTURB_DEG))
    groups = angle_groups(T())
    near = [(r, m) for r, m in groups if EQ_TOL < abs(r) < near_axis and movable(r, m)]
    if near:
        idx = [i for _, m in near for i in m]
        if accept(assign(T(), idx, 0), ('straighten', len(idx))):
            changes.append(('free-angle straighten', len(near), len(idx)))
    groups = angle_groups(T())
    for r, m in sorted([(r, m) for r, m in groups if abs(r) > EQ_TOL], key=lambda z: len(z[1])):
        if not movable(r, m):
            continue
        cur = angle_groups(T())
        targets = [q for q, mm in cur if dist(q, r) > EQ_TOL and (len(mm) >= len(m) or abs(q) < EQ_TOL)]
        targets.sort(key=lambda q: (not (abs(q) < EQ_TOL and abs(r) < near_axis), dist(q, r)))
        for q in targets:
            if accept(assign(T(), m, q), ('free-angle', float(r), float(q))):
                changes.append(('free-angle', float(r), float(q), len(m)))
                break
        else:
            changes.append(('free-angle kept', float(r), len(m)))
    # 3. 'fewest': determined groups too, within cap degrees
    if policy == 'fewest':
        while True:
            groups = angle_groups(T())
            done = False
            for r, m in sorted([(r, m) for r, m in groups if abs(r) > EQ_TOL], key=lambda z: len(z[1])):
                targets = sorted([q for q, mm in groups if len(mm) >= len(m) and EQ_TOL < dist(q, r) < cap],
                                 key=lambda q: dist(q, r))
                for q in targets:
                    if accept(assign(T(), m, q), ('determined', float(r), float(q))):
                        changes.append(('determined-merge', float(r), float(q), len(m))); done = True
                        break
                if done:
                    break
            if not done:
                break
    Q = dict(P); Q['T'] = T()
    if policy == 'conservative':
        Q['X'], Q['Y'] = state['P']['X'], state['P']['Y']
    return Q, changes


def sym_candidates(P, tol=0.75):
    """Container symmetries g with a pairing of *all* squares (nearest image, equal angles exactly, assignment
    problem): (g, perm) with perm[i] = the square of g(P) sitting near P's square i.  Whether a symmetric placement
    exists is left to the LP."""
    from scipy.optimize import linear_sum_assignment
    n = P['n']
    out = []
    X = np.array([float(v) for v in P['X']]); Y = np.array([float(v) for v in P['Y']])
    for g in range(1, 8):
        Q = d4(P, g)
        QX = np.array([float(v) for v in Q['X']]); QY = np.array([float(v) for v in Q['Y']])
        C = np.maximum(np.abs(X[:, None] - QX[None, :]), np.abs(Y[:, None] - QY[None, :]))
        for i in range(n):
            for j in range(n):
                if C[i, j] < tol and abs(fold(P['T'][i] - Q['T'][j])) > EQ_TOL:
                    C[i, j] = 1e6
        r, cidx = linear_sum_assignment(C)
        if C[r, cidx].max() < tol:
            out.append((g, {int(i): int(j) for i, j in zip(r, cidx)}))
    return out


def chain_pairs(P, tol_n=0.15, tol_t=0.25):
    """Tilted squares with equal angles, nearly face to face (centre distance along a face normal within tol_n of 1,
    offset along the face below tol_t): (i, j, nx, ny).  Imposed as straight-chain equalities."""
    n = P['n']
    X, Y = [float(v) for v in P['X']], [float(v) for v in P['Y']]
    out = []
    for i in range(n):
        if abs(P['T'][i]) < EQ_TOL:
            continue
        c, s = frame(P['T'][i])
        for j in range(i + 1, n):
            if abs(fold(P['T'][i] - P['T'][j])) > EQ_TOL:
                continue
            dx, dy = X[j] - X[i], Y[j] - Y[i]
            for nx, ny in ((c, s), (-s, c)):
                d = nx * dx + ny * dy
                if d < 0:
                    nx, ny, d = -nx, -ny, -d
                if abs(d - 1) < tol_n and abs(-ny * dx + nx * dy) < tol_t:
                    out.append((i, j, nx, ny))
    return out


def tilted_clusters(P, link=1.25):
    n = P['n']
    til = [i for i in range(n) if abs(P['T'][i]) > EQ_TOL]
    X, Y = [float(v) for v in P['X']], [float(v) for v in P['Y']]
    comp, seen = [], set()
    for i in til:
        if i in seen:
            continue
        st, cur = [i], []
        seen.add(i)
        while st:
            a = st.pop(); cur.append(a)
            for b in til:
                if b not in seen and (X[a] - X[b]) ** 2 + (Y[a] - Y[b]) ** 2 < link ** 2:
                    seen.add(b); st.append(b)
        comp.append(cur)
    return comp


def pretty_objective(P, wtilt=1.0, wgrid=1.0, eps=1e-4, grav=(1.5, 2.0)):
    """Rule 2: tilted squares pulled toward their cluster's centroid (|.| via auxiliaries).  Rule 3: axis squares
    pulled toward their nearest walls (weight wgrid; exact centre lines: no pull) *plus* gravity toward the bottom
    left (grav, stronger): without symmetry gravity wins and vacancies go to the top right; under a symmetry the
    gravity of a mirrored pair cancels and the wall pull sends both into their corners.  Tie-break: eps * gravity."""
    n, S = P['n'], float(P['S'])
    X, Y = [float(v) for v in P['X']], [float(v) for v in P['Y']]
    weights = [[eps * 1e-3, eps] for _ in range(n)]
    absobj = []
    for cl in tilted_clusters(P):
        cx = sum(X[i] for i in cl) / len(cl); cy = sum(Y[i] for i in cl) / len(cl)
        absobj += [(i, cx, cy, wtilt) for i in cl]
    for i in range(n):
        if abs(P['T'][i]) < EQ_TOL:
            for d, z in ((0, X[i]), (1, Y[i])):
                weights[i][d] += grav[d]
                if abs(z - S / 2) > 1e-9:
                    weights[i][d] += wgrid if z < S / 2 else -wgrid
    return weights, absobj


def pretty_place(P, keepc, rep):
    """Rules 1-3: largest feasible symmetry of the whole packing, straight tilted chains where feasible, pulls."""
    weights, absobj = pretty_objective(P)
    align = chain_pairs(P)
    cands = sym_candidates(P)
    rep['sym_candidates'] = [g for g, _ in cands]

    def attempt(sy, al):
        return place(P, weights, sym=sy, keep=keepc, align=al, absobj=absobj)

    # rule 1: try every candidate alone, then greedily combine (largest set first)
    ok1 = []
    for g, p in cands:
        X, Y, st, info = attempt([(g, p)], align)
        if st == 'infeasible':
            X, Y, st, info = attempt([(g, p)], [])
        if st != 'infeasible':
            ok1.append((g, p))
    chosen = []
    for gp in ok1:
        X, Y, st, info = attempt(chosen + [gp], align)
        if st == 'infeasible':
            X, Y, st, info = attempt(chosen + [gp], [])
        if st != 'infeasible':
            chosen.append(gp)
    used_align = align
    X, Y, st, info = attempt(chosen, align)
    if st == 'infeasible':
        # per chain: connected components of the alignment graph, added greedily (longest chain first)
        comp = {}
        for k, (i, j, _, _) in enumerate(align):
            ci, cj = comp.setdefault(i, {i}), comp.setdefault(j, {j})
            if ci is not cj:
                ci |= cj
                for q in cj:
                    comp[q] = ci
        chains = []
        for cset in {id(v): v for v in comp.values()}.values():
            chains.append([a for a in align if a[0] in cset])
        chains.sort(key=len, reverse=True)
        used_align = []
        for ch in chains:
            Xt, Yt, stt, _ = attempt(chosen, used_align + ch)
            if stt != 'infeasible':
                used_align += ch
            else:                                   # pair by pair (rigid lattices with real offsets)
                for a in ch:
                    Xt, Yt, stt, _ = attempt(chosen, used_align + [a])
                    if stt != 'infeasible':
                        used_align.append(a)
        X, Y, st, info = attempt(chosen, used_align)
    rep['align_pairs'] = len(used_align); rep['align_total'] = len(align)
    rep['align_dropped'] = len(align) - len(used_align)
    return X, Y, st, info, chosen



def coincidences(P, X, Y, weights, sym=(), keep=(), align=(), trust=0.75, time_limit=60):
    """Rule 2' (round 3): maximize the number of coincident faces -- equal-angle pairs flush along a face normal with
    no offset along the face, and axis squares flush on a wall -- by a MILP over translations from (X, Y) (trust
    region), tie-break = the given linear weights (scaled below one coincidence).  Returns (count, chosen pairs as
    align tuples (i, j, nx, ny), chosen walls, status)."""
    from scipy.optimize import milp, LinearConstraint, Bounds
    n, S = P['n'], float(P['S'])
    CS = [frame(t) for t in P['T']]
    E = np.array([[support(c, s, 1, 0), support(c, s, 0, 1)] for c, s in CS])
    reach = 2 * trust + math.sqrt(2) + 0.05
    rows, rhs = [], []
    for i in range(n):
        for j in range(i + 1, n):
            if (X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2 < reach ** 2:
                nx, ny, r, g = best_normal(i, j, X, Y, CS)
                rows.append(((i, -nx, -ny), (j, nx, ny))); rhs.append(r)
    cand = []                                    # (i, j, nx, ny) with n = a face normal of i pointing to j
    for i in range(n):
        c, s = CS[i]
        for j in range(n):
            if j <= i or abs(fold(P['T'][i] - P['T'][j])) > EQ_TOL:
                continue
            dx, dy = X[j] - X[i], Y[j] - Y[i]
            for nx, ny in ((c, s), (-s, c)):
                d = nx * dx + ny * dy
                if d < 0:
                    nx, ny, d = -nx, -ny, -d
                if d < 1 + 2 * trust and abs(-ny * dx + nx * dy) < 2 * trust:
                    cand.append((i, j, nx, ny))
    walls = []                                   # (i, d, side): axis square i flush on wall
    for i in range(n):
        if abs(P['T'][i]) < EQ_TOL:
            for d, z in ((0, X[i]), (1, Y[i])):
                if z - E[i, d] < 2 * trust:
                    walls.append((i, d, 0))
                if S - E[i, d] - z < 2 * trust:
                    walls.append((i, d, 1))
    nb = len(cand) + len(walls)
    nv = 2 * n + nb
    M = 4.0
    A, lb, ub = [], [], []
    def add(coefs, lo_, hi_):
        row = np.zeros(nv)
        for v, a in coefs:
            row[v] += a
        A.append(row); lb.append(lo_); ub.append(hi_)
    for ((i, ax, ay), (j, bx, by)), r in zip(rows, rhs):
        add([(2 * i, ax), (2 * i + 1, ay), (2 * j, bx), (2 * j + 1, by)], r, np.inf)
    for g, p in sym:
        Mg, t = affine(g, S)
        for jj in range(n):
            ii = p[jj]
            for d in range(2):
                add([(2 * jj + d, 1), (2 * ii, -Mg[d][0]), (2 * ii + 1, -Mg[d][1])], t[d], t[d])
    for (i, j), (nx, ny, r) in dict(keep).items():
        add([(2 * i, -nx), (2 * i + 1, -ny), (2 * j, nx), (2 * j + 1, ny)], r, r)
    for i, j, nx, ny in align:
        add([(2 * i, -nx), (2 * i + 1, -ny), (2 * j, nx), (2 * j + 1, ny)], 1.0, 1.0)
        add([(2 * i, ny), (2 * i + 1, -nx), (2 * j, -ny), (2 * j + 1, nx)], 0.0, 0.0)
    for k, (i, j, nx, ny) in enumerate(cand):
        z = 2 * n + k
        # n.(cj - ci) <= 1 + M(1 - z);  |t.(cj - ci)| <= M(1 - z)
        add([(2 * i, -nx), (2 * i + 1, -ny), (2 * j, nx), (2 * j + 1, ny), (z, M)], -np.inf, 1 + M)
        add([(2 * i, ny), (2 * i + 1, -nx), (2 * j, -ny), (2 * j + 1, nx), (z, M)], -np.inf, M)
        add([(2 * i, -ny), (2 * i + 1, nx), (2 * j, ny), (2 * j + 1, -nx), (z, M)], -np.inf, M)
    for k, (i, d, side) in enumerate(walls):
        z = 2 * n + len(cand) + k
        if side == 0:                            # z_i - e <= M(1 - zb)
            add([(2 * i + d, 1), (z, M)], -np.inf, E[i, d] + M)
        else:                                    # S - e - z_i <= M(1 - zb)
            add([(2 * i + d, -1), (z, M)], -np.inf, M - S + E[i, d])
    w = np.array([wv for i in range(n) for wv in weights[i]])
    scale = 0.5 / max(1e-12, np.sum(np.abs(w)) * S)
    c = np.r_[w * scale, -np.ones(nb)]
    lo = np.r_[[max(E[i, d], (X[i] if d == 0 else Y[i]) - trust) for i in range(n) for d in (0, 1)], np.zeros(nb)]
    hi = np.r_[[min(S - E[i, d], (X[i] if d == 0 else Y[i]) + trust) for i in range(n) for d in (0, 1)], np.ones(nb)]
    lo, hi = np.minimum(lo, hi), np.maximum(lo, hi)
    integ = np.r_[np.zeros(2 * n), np.ones(nb)]
    res = milp(c, constraints=LinearConstraint(np.array(A), np.array(lb), np.array(ub)), integrality=integ,
               bounds=Bounds(lo, hi), options=dict(time_limit=time_limit, mip_rel_gap=0))
    if res.x is None:
        return -1, [], [], res.message
    zb = res.x[2 * n:] > 0.5
    chosen = [cand[k] for k in range(len(cand)) if zb[k]]
    wch = [walls[k] for k in range(len(walls)) if zb[len(cand) + k]]
    return int(zb.sum()), chosen, wch, ('ok' if res.status == 0 else res.message)


def pretty_coincide(P, keepc, rep):
    """Round 3: pretty_place, then maximize coincident faces (dropping symmetry only if it costs coincidences),
    then re-place with the chosen coincidences as equalities."""
    X, Y, st, info, chosen = pretty_place(P, keepc, rep)
    if st == 'infeasible':
        return X, Y, st, info, chosen
    weights, absobj = pretty_objective(P)
    align0 = []
    cnt_s, pairs_s, walls_s, st_s = coincidences(P, X, Y, weights, sym=chosen, keep=keepc)
    best = (cnt_s, pairs_s, walls_s, chosen)
    if chosen:
        cnt_f, pairs_f, walls_f, st_f = coincidences(P, X, Y, weights, sym=(), keep=keepc)
        rep['coinc_nosym'] = cnt_f
        if cnt_f > cnt_s:
            best = (cnt_f, pairs_f, walls_f, [])
    rep['coinc_sym'] = cnt_s
    cnt, pairs, wls, sy = best
    rep['coincident'] = cnt; rep['sym_dropped_for_coincidence'] = [g for g, _ in chosen] if (chosen and not sy) else []
    # re-place: coincident pairs as equalities (straight chains included), walls as fixed coordinates
    S = float(P['S'])
    fixedwalls = {}
    for i, d, side in wls:
        c, s = frame(P['T'][i]); e = support(c, s, 1, 0) if d == 0 else support(c, s, 0, 1)
        fixedwalls[(i, d)] = e if side == 0 else S - e
    Xf, Yf, st2, info2 = place(P, weights, sym=sy, keep=keepc, align=pairs, absobj=absobj, pins=fixedwalls)
    if st2 == 'infeasible':                     # keep the pretty result if the re-placement fails
        rep['coinc_replace'] = 'infeasible'
        return X, Y, st, info, chosen
    return Xf, Yf, st2, info2, sy


# ----------------------------------------------------------------------------------------------- certificate

def write_cert(R, path, eps='1e-20', rdig=35):
    """Rational certificate of the regularized packing, as exactsolve.certificate: scale about the origin corner by
    1 + eps (opens every contact by ~eps * distance; squares keep their size), round centres and t = tan(theta/2) to
    10^-rdig, side S' = ceil(S (1 + eps)) at 10^-(rdig-5).  Checked by verify_cert.py (and verify_cert2.py
    separately).  Returns (ok, S' as Fraction)."""
    from fractions import Fraction
    sys.path.insert(0, os.path.join(HERE, '..', 'exact'))
    import verify_cert
    e = mpf(eps); f = 1 + e
    den = 10 ** rdig
    rat = lambda v: Fraction(int(mpm.nint(v * den)), den)
    Sp = Fraction(int(mpm.ceil(R['S'] * f * 10 ** (rdig - 5))), 10 ** (rdig - 5))
    with open(path, 'w') as fh:
        fh.write('# exact certificate (regularized display view, search/regularize): unit squares, centre (x, y), rotation '
                 '(c, s) = ((1-t^2)/(1+t^2), 2t/(1+t^2)); check with search/exact/verify_cert.py\n')
        fh.write(f"{R['n']} {Sp}\n")
        for x, y, t in zip(R['X'], R['Y'], R['T']):
            fh.write(f"{rat(x * f)} {rat(y * f)} {rat(mpm.tan(t * mp.pi / 360))}\n")
    n, S2, sq = verify_cert.parse(path)
    ok, wall, pair = verify_cert.verify(n, S2, sq, verbose=False)
    return bool(ok), Sp


# ----------------------------------------------------------------------------------------------- driver

def source_contacts(P):
    """Pairs of squares with equal angles (exact test) in face-to-face exact contact in P (gap < 1e-14 at 80 digits;
    frozen flat coordinates carry ~1e-17): (i, j) -> float (nx, ny, r) of the contact normal.  Used to keep chains
    together (a strip slides as a unit instead of breaking into pieces)."""
    n = P['n']
    X, Y = [float(v) for v in P['X']], [float(v) for v in P['Y']]
    CS = [frame(t) for t in P['T']]
    out = {}
    for i in range(n):
        for j in range(i + 1, n):
            if (X[i] - X[j]) ** 2 + (Y[i] - Y[j]) ** 2 > 1.3 or abs(fold(P['T'][i] - P['T'][j])) > EQ_TOL:
                continue
            c, s = mp_frame(P['T'][i])
            dx, dy = P['X'][j] - P['X'][i], P['Y'][j] - P['Y'][i]
            for nx, ny in ((c, s), (-s, c)):
                d = nx * dx + ny * dy
                if d < 0:
                    nx, ny, d = -nx, -ny, -d
                if abs(d - 1) < mpf('1e-14') and abs(-ny * dx + nx * dy) < 1 - mpf('1e-9'):   # faces overlap
                    out[(i, j)] = (float(nx), float(ny), 1.0)
    return out


GRAV = {'yx': (1e-3, 1.0), 'xy': (1.0, 1e-3), 'sum': (1.0, 1.0)}


def regularize(n, gravity='yx', sym='on', orient='best', merge='on', keep='off', style='gravity', orient_kind=None,
               angle_policy='free', log=print):
    P0 = load(n)
    rigid = [i for i in range(n) if i not in P0['free']]
    rep = dict(n=n, S=float(P0['S']), free=P0['free'], status=P0['status'], by=P0['by'])
    rep['groups_before'] = len(angle_groups(P0['T']))
    # angle merge first (it does not depend on the orientation; noise-tilted free squares would distort the
    # orientation score's tilted-band test)
    changes = []
    if merge == 'on' and P0['free']:
        P0, changes = merge_angles(P0, P0['free'], log)
    rep['merged'] = changes
    T_before = list(P0['T'])
    if merge == 'on':
        P0, dchanges = merge_determined(P0, policy=angle_policy, log=log)
        rep['merged_determined'] = dchanges
        changes = changes + [(i, float(T_before[i]), float(P0['T'][i])) for i in range(n)
                             if abs(fold(P0['T'][i] - T_before[i])) > EQ_TOL]
    rep['shape'] = shape_of(P0)
    ors = orientations(P0, orient_kind)
    rep['orient_scores'] = [(g, [round(x, 6) for x in sc]) for g, _, sc in ors]
    close = lambda a, b, k: all(abs(a[q] - b[q]) < 1e-3 for q in range(k))
    # true tie: the two best distinct images score alike on every key; 'top/right': only the last key
    # (emptiness toward the top rather than the right) separates them -- a convention, not geometry
    rep['orient_tie'] = len(ors) > 1 and close(ors[0][2], ors[1][2], 3)
    rep['orient_topright'] = len(ors) > 1 and close(ors[0][2], ors[1][2], 2) and not rep['orient_tie']
    rep['orient_source'] = ors[0][0] == 0          # the chosen image is the source drawing (jlevy's orientation)
    k = 0 if orient == 'best' else int(orient)
    g, P, _ = ors[k] if orient == 'best' else (k, d4(P0, k), None)
    rep['g'] = g
    rep['groups_after'] = len(angle_groups(P['T']))
    syms = symmetries(P, rigid) if sym == 'on' else []
    rep['rigid_sym'] = [s for s, _ in syms]
    imposed = []
    if syms:
        # complete the permutations on the free squares by nearest image; drop a symmetry that does not complete
        for s, p in syms:
            Q = d4(P, s)
            pf = match(P, Q, P['free'], 0.6, 90) if P['free'] else {}
            if pf is not None:
                pp = dict(p); pp.update(pf); imposed.append((s, pp))
    keepc = source_contacts(P) if keep == 'on' else {}
    rep['kept_contacts'] = len(keepc)
    wx, wy = GRAV[gravity]
    rep['style'] = style
    if style == 'pretty':
        Xf, Yf, st, info, imposed = pretty_place(P, keepc, rep)
    elif style == 'coincide':
        Xf, Yf, st, info, imposed = pretty_coincide(P, keepc, rep)
    else:
        Xf, Yf, st, info = place(P, [(wx, wy)] * n, sym=imposed, keep=keepc)
    if st == 'infeasible' and imposed:
        rep['sym_dropped'] = [s for s, _ in imposed]
        imposed = []
        Xf, Yf, st, info = place(P, [(wx, wy)] * n, keep=keepc)
    rep['sym_imposed'] = [s for s, _ in imposed]
    rep['place'] = st
    rep['face_spread'] = info.get('face_spread')
    moved = {i for i in range(n) if max(abs(Xf[i] - float(P['X'][i])), abs(Yf[i] - float(P['Y'][i]))) > 1e-9}
    moved |= {i for i, _, _ in changes}
    rep['moved'] = sorted(moved)
    rep['max_move'] = max([max(abs(Xf[i] - float(P['X'][i])), abs(Yf[i] - float(P['Y'][i]))) for i in moved], default=0.0)
    R, rr = refine(P, Xf, Yf, moved, sym=imposed)
    rep['refine'] = {k: v for k, v in rr.items() if k != 'hist'}
    v = verify(R)
    rep['verify'] = dict(ok=bool(v['ok']), min_gap=mpm.nstr(v['min_gap'], 5), contacts=v['contacts'])
    v0 = verify(P)
    rep['contacts_before'] = v0['contacts']
    return P, R, rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int)
    ap.add_argument('--gravity', default='yx', choices=list(GRAV))
    ap.add_argument('--sym', default='on')
    ap.add_argument('--orient', default='best')
    ap.add_argument('--merge', default='on')
    ap.add_argument('--keep', default='off', help='on: exact face contacts of the source stay closed')
    ap.add_argument('--style', default='gravity', choices=['gravity', 'pretty', 'coincide'])
    ap.add_argument('--orient-kind', default=None, choices=['strip', 'arc', 'source'])
    ap.add_argument('--angle-policy', default='free', choices=['free', 'conservative', 'fewest'])
    ap.add_argument('--out', default=None, help='write source + result coordinates (json)')
    a = ap.parse_args()
    P, R, rep = regularize(a.n, a.gravity, a.sym, a.orient, a.merge, a.keep, a.style, a.orient_kind, a.angle_policy)
    print(json.dumps(rep, default=str, indent=1))
    if a.out:
        dump(a.out, P, R, rep)


def dump(path, P, R, rep):
    js = lambda Q: dict(S=mpm.nstr(Q['S'], 40), sq=[[mpm.nstr(x, 40), mpm.nstr(y, 40), mpm.nstr(t, 40)]
                                                   for x, y, t in zip(Q['X'], Q['Y'], Q['T'])])
    json.dump(dict(rep=rep, source=js(P), result=js(R)), open(path, 'w'), default=str)


if __name__ == '__main__':
    main()
