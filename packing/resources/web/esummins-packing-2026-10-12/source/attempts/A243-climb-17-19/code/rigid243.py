"""A243 -- is the record RIGID?  First-order (infinitesimal) motions of the record packing at FIXED side s.

For every pair of squares and every square/wall with gap < TOL (signed separating-axis gap; the record has exact
contacts), the gap's gradient g_c in the 3n pose coordinates (x, y, theta) is taken by central differences.  A
first-order motion v keeps every contact closed or opening: g_c . v >= 0.  Reported:
  * dim ker(J): sliding modes keeping EVERY contact (equalities), translations of rattlers included;
  * rattlers: squares with no contact at all;
  * LP: max sum_i |v| over {J v >= 0, -1 <= v <= 1} restricted to non-rattlers (scipy linprog); > 1e-6 = the
    contact graph admits a first-order motion = NOT infinitesimally rigid (the ladder band of n = 19 may slide).
[M] numerical, floats -- a measurement for the brief's question, no claim in any certificate.
    python rigid243.py 17 | 19"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TOL = 1e-6


def record(n):
    for ln in open(os.path.join(ROOT, "attempts", "A226-one-flush", "results", "survey226.jsonl"), encoding="utf-8"):
        r = json.loads(ln)
        if r.get("n") == n and r["label"] == "square-%d" % n:
            return r
    raise KeyError(n)


def verts(x, y, t):
    c, s = math.cos(t), math.sin(t)
    return [(x + 0.5 * (a * c - b * s), y + 0.5 * (a * s + b * c)) for a, b in ((1, 1), (-1, 1), (-1, -1), (1, -1))]


def sat_gap(p, q):
    """signed separating-axis gap of two unit squares (> 0 separated, 0 touching, < 0 overlapping)."""
    V, W = verts(*p), verts(*q)
    best = -1e9
    for t in (p[2], q[2]):
        for ax in ((math.cos(t), math.sin(t)), (-math.sin(t), math.cos(t))):
            a = [v[0] * ax[0] + v[1] * ax[1] for v in V]
            b = [w[0] * ax[0] + w[1] * ax[1] for w in W]
            best = max(best, min(b) - max(a), min(a) - max(b))
    return best


def wall_gaps(p, s):
    V = verts(*p)
    return (min(v[0] for v in V), s - max(v[0] for v in V), min(v[1] for v in V), s - max(v[1] for v in V))


def analyse(n):
    r = record(n)
    s = r["side"]
    P = [tuple(q) for q in r["squares"]]
    N = len(P)
    X = np.array([c for q in P for c in q], dtype=float)

    def gaps(X):
        Q = [tuple(X[3 * i:3 * i + 3]) for i in range(N)]
        out = []
        for i in range(N):
            for j in range(i + 1, N):
                out.append(sat_gap(Q[i], Q[j]))
        for i in range(N):
            out.extend(wall_gaps(Q[i], s))
        return np.array(out)
    g0 = gaps(X)
    act = np.where(np.abs(g0) < TOL)[0]
    h = 1e-7
    J = np.zeros((len(act), 3 * N))
    for k in range(3 * N):
        e = np.zeros(3 * N)
        e[k] = h
        J[:, k] = (gaps(X + e)[act] - gaps(X - e)[act]) / (2 * h)
    touched = sorted({i for i in range(N) if np.any(np.abs(J[:, 3 * i:3 * i + 3]) > 1e-9)})
    rattlers = [i for i in range(N) if i not in touched]
    sv = np.linalg.svd(J, compute_uv=False) if len(act) else np.array([])
    rank = int(np.sum(sv > 1e-6 * (sv.max() if len(sv) else 1)))
    lp = None
    try:
        from scipy.optimize import linprog
        cols = [3 * i + d for i in touched for d in range(3)]
        Jt = J[:, cols]
        m = len(cols)
        # v = u - w, u, w >= 0, u, w <= 1: maximise sum(u + w) subject to J (u - w) >= 0
        c = -np.ones(2 * m)
        A = np.hstack([-Jt, Jt])
        res = linprog(c, A_ub=A, b_ub=np.zeros(len(act)), bounds=[(0, 1)] * (2 * m), method="highs")
        if res.success:
            v = res.x[:m] - res.x[m:]
            lp = dict(max_l1=round(float(np.abs(v).sum()), 6),
                      moving=sorted({touched[k // 3] for k in range(m) if abs(v[k]) > 1e-6}))
    except Exception as e:                                        # noqa: BLE001
        lp = dict(error=repr(e)[:120])
    tilted = [i for i, q in enumerate(P) if min(abs(q[2]) % (math.pi / 2), math.pi / 2 - abs(q[2]) % (math.pi / 2)) > 1e-6]
    return dict(n=n, side=s, n_squares=N, n_contacts=int(len(act)), min_gap=float(g0.min()), rank=rank,
                ker_dim=3 * N - rank, rattlers=rattlers, tilted=tilted, lp=lp,
                rigid_first_order=bool(lp and lp.get("max_l1", 1) < 1e-6 and not rattlers))


if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]] or [17, 19]:
        out = analyse(n)
        print(json.dumps(out))
        f = os.path.join(HERE, "..", "results", "rigid243_n%d.json" % n)
        json.dump(out, open(f, "w", encoding="utf-8"), indent=1)
