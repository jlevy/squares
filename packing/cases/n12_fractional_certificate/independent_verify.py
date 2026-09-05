# Provenance: written by an independent reviewer from the theorem statement alone,
# with the project implementation withheld, on 2026-09-04. Retained verbatim; the
# style is the reviewer's, and the point of the file is that it shares nothing with
# sqpack.fractional. See docs/project/reviews/review-2026-09-04-t017-independent-verification.md.
# ruff: noqa
"""Independent from-scratch verifier for the Burns/Massaccesi covering theorem.

Written only from the theorem statement.  Exact rational arithmetic throughout.
Allowed imports only: fractions, itertools, numpy (+ stdlib json/sys/time/bisect).

Condition 5 is decided over the CONTINUUM of placements, not on a sampled grid:
the covered-mass function is piecewise constant on the arrangement of the
atom-square edges, so we enumerate every cell of that arrangement (open cells,
open edges and vertices, in both coordinates) and decide exactly which cells
meet the feasible set F of admissible centres.  The mass on a cell is summed
DIRECTLY over the atoms (an atoms-indexed inner product), never by prefix sums
or a difference array.
"""

from fractions import Fraction as Fr
from bisect import bisect_left, bisect_right
import json, sys, time, itertools, random
import numpy as np

# --------------------------------------------------------------------------
# certificate loading
# --------------------------------------------------------------------------

def load(path):
    d = json.load(open(path))
    n = int(d["n"])
    L = Fr(d["outer_side"])
    B = Fr(d["square_side"])
    tlim = Fr(d["angle_limit"])
    steps = int(d["direction_steps"])
    atoms = [(Fr(a[0]), Fr(a[1]), Fr(a[2])) for a in d["atoms"]]
    return dict(id=d.get("id"), n=n, L=L, B=B, tlim=tlim, steps=steps, atoms=atoms)

def net(cert):
    return [cert["tlim"] * Fr(k, cert["steps"]) for k in range(cert["steps"] + 1)]

# --------------------------------------------------------------------------
# Condition 1 : D4 invariance of the weighted atom multiset
# --------------------------------------------------------------------------

def condition_1(cert):
    L = cert["L"]
    base = {}
    for x, y, w in cert["atoms"]:
        base[(x, y)] = base.get((x, y), Fr(0)) + w
    base = {k: v for k, v in base.items() if v != 0}
    maps = [lambda x, y: (x, y),        lambda x, y: (L - x, y),
            lambda x, y: (x, L - y),    lambda x, y: (L - x, L - y),
            lambda x, y: (y, x),        lambda x, y: (L - y, x),
            lambda x, y: (y, L - x),    lambda x, y: (L - y, L - x)]
    bad = []
    for gi, g in enumerate(maps):
        img = {}
        for (x, y), w in base.items():
            k = g(x, y)
            img[k] = img.get(k, Fr(0)) + w
        img = {k: v for k, v in img.items() if v != 0}
        if img != base:
            diff = set(img) ^ set(base)
            diff |= {k for k in set(img) & set(base) if img[k] != base[k]}
            bad.append((gi, sorted(diff)[:3]))
    return (len(bad) == 0), bad

# --------------------------------------------------------------------------
# Condition 2 / Condition 3 / Condition 4
# --------------------------------------------------------------------------

def condition_2(cert):
    W = sum((w for _, _, w in cert["atoms"]), Fr(0))
    return W < cert["n"], W

def condition_3(cert):
    tK = net(cert)[-1]
    return tK * tK + 2 * tK - 1 >= 0, tK

def condition_4(cert):
    ts = net(cert)
    D = max((ts[k + 1] - ts[k]) / (1 + ts[k] * ts[k + 1]) for k in range(len(ts) - 1))
    val = cert["B"] * (1 + D)
    return val < 1, D, val

# --------------------------------------------------------------------------
# Condition 5 machinery
# --------------------------------------------------------------------------

def pieces(bps, biglo, bighi):
    """Arrangement pieces of the line induced by breakpoints `bps` (sorted, distinct).

    Piece 2j   = open interval (bps[j-1], bps[j])   (unbounded at the two ends)
    Piece 2j+1 = the single point bps[j]
    Returns (rep, clo, chi) with rep strictly increasing.
    """
    M = len(bps)
    rep, clo, chi = [], [], []
    for i in range(2 * M + 1):
        if i % 2:
            p = bps[(i - 1) // 2]
            rep.append(p); clo.append(p); chi.append(p)
        else:
            j = i // 2
            lo = biglo if j == 0 else bps[j - 1]
            hi = bighi if j == M else bps[j]
            rep.append((lo + hi) / 2); clo.append(lo); chi.append(hi)
    return rep, clo, chi


def clip_v_range(poly, u0, u1):
    """v-projection of (convex polygon poly) intersect {u0 <= u <= u1}, or None."""
    def clip(pts, keep):
        out = []
        m = len(pts)
        for a in range(m):
            P, Q = pts[a], pts[(a + 1) % m]
            fp, fq = keep(P), keep(Q)
            if fp >= 0:
                out.append(P)
            if (fp > 0 and fq < 0) or (fp < 0 and fq > 0):
                s = fp / (fp - fq)
                out.append((P[0] + s * (Q[0] - P[0]), P[1] + s * (Q[1] - P[1])))
        return out
    pts = clip(poly, lambda P: P[0] - u0)
    if not pts:
        return None
    pts = clip(pts, lambda P: u1 - P[0])
    if not pts:
        return None
    vs = [p[1] for p in pts]
    return min(vs), max(vs)


def direction_min(cert, t, wint, scale, brute_check=0, rng=None):
    """Exact minimum covered mass (scaled to ints) over all admissible placements
    at half-tangent t.  Returns (m_lower, m_rep, argmin_info)."""
    L, B, atoms = cert["L"], cert["B"], cert["atoms"]
    p, q = t.numerator, t.denominator
    A = q * q - p * p          # m*cos(theta)
    Bb = 2 * p * q             # m*sin(theta)
    m = q * q + p * p
    assert A > 0 and Bb >= 0

    # Phi(x,y) = m * R(-theta) (x,y) : rotated frame, scaled by m
    Ax = [A * x + Bb * y for x, y, _ in atoms]
    Ay = [-Bb * x + A * y for x, y, _ in atoms]
    H = m * B / 2                                     # half-side in Phi units

    ubp = sorted({v for a in Ax for v in (a - H, a + H)})
    vbp = sorted({v for a in Ay for v in (a - H, a + H)})

    # feasible centres in xy: [delta, L-delta]^2 with delta = (B/2)(cos+sin)
    delta = B * (A + Bb) / (2 * m)
    corners_xy = [(delta, delta), (L - delta, delta), (L - delta, L - delta), (delta, L - delta)]
    poly = [(A * x + Bb * y, -Bb * x + A * y) for x, y in corners_xy]   # in Phi units
    feasible_nonempty = delta * 2 <= L

    allu = ubp + [c[0] for c in poly]
    allv = vbp + [c[1] for c in poly]
    biglo_u, bighi_u = min(allu) - 1, max(allu) + 1
    biglo_v, bighi_v = min(allv) - 1, max(allv) + 1

    ru, clou, chiu = pieces(ubp, biglo_u, bighi_u)
    rv, clov, chiv = pieces(vbp, biglo_v, bighi_v)
    nu, nv = len(ru), len(rv)

    # ---- membership matrices (exact: reps are sorted, endpoints compared exactly)
    na = len(atoms)
    Mu = np.zeros((na, nu), dtype=np.int64)
    Mv = np.zeros((na, nv), dtype=np.int64)
    for i in range(na):
        lo = bisect_left(ru, Ax[i] - H); hi = bisect_right(ru, Ax[i] + H)
        Mu[i, lo:hi] = 1
        lo = bisect_left(rv, Ay[i] - H); hi = bisect_right(rv, Ay[i] + H)
        Mv[i, lo:hi] = 1

    # ---- covered mass, summed DIRECTLY over atoms (no prefix sums / diff arrays)
    Fmat = (Mu * wint[:, None]).T @ Mv           # Fmat[iu,jv] = sum_i w_i [u in I_i][v in J_i]

    if brute_check:
        for _ in range(brute_check):
            iu = rng.randrange(nu); jv = rng.randrange(nv)
            s = 0
            for i in range(na):
                if abs(Ax[i] - ru[iu]) <= H and abs(Ay[i] - rv[jv]) <= H:
                    s += int(wint[i])
            assert s == int(Fmat[iu, jv]), ("brute mismatch", iu, jv)

    if not feasible_nonempty:
        return None, None, None

    Lo = delta * m * m
    Hi = (L - delta) * m * m

    # ---- lower bound: every cell whose CLOSURE meets F (superset of cells meeting F)
    m_lower = None
    for iu in range(nu):
        r = clip_v_range(poly, clou[iu], chiu[iu])
        if r is None:
            continue
        vlo, vhi = r
        j0 = bisect_left(chiv, vlo)
        j1 = bisect_right(clov, vhi) - 1
        if j0 > j1:
            continue
        cand = int(Fmat[iu, j0:j1 + 1].min())
        if m_lower is None or cand < m_lower:
            m_lower = cand

    # ---- upper bound: minimum over representative points genuinely inside F
    m_rep, arg = None, None
    for iu in range(nu):
        u = ru[iu]
        lo_v, hi_v = None, None
        if Bb > 0:
            lo_v, hi_v = (A * u - Hi) / Bb, (A * u - Lo) / Bb
        else:
            if not (Lo <= A * u <= Hi):
                continue
        a, b = (Lo - Bb * u) / A, (Hi - Bb * u) / A
        lo_v = a if lo_v is None else max(lo_v, a)
        hi_v = b if hi_v is None else min(hi_v, b)
        if lo_v > hi_v:
            continue
        j0 = bisect_left(rv, lo_v); j1 = bisect_right(rv, hi_v) - 1
        if j0 > j1:
            continue
        seg = Fmat[iu, j0:j1 + 1]
        jj = int(seg.argmin()); cand = int(seg[jj])
        if m_rep is None or cand < m_rep:
            m_rep = cand
            U, V = u, rv[j0 + jj]
            arg = (t, (A * U - Bb * V) / (m * m), (Bb * U + A * V) / (m * m))
    return m_lower, m_rep, arg


def condition_5(cert, ks=None, brute_check=0, seed=1):
    atoms = cert["atoms"]
    def _gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    den = 1
    for _, _, w in atoms:
        den = den * w.denominator // _gcd(den, w.denominator)
    scale = int(den)
    wint = np.array([int(w * scale) for _, _, w in atoms], dtype=np.int64)
    ts = net(cert)
    if ks is None:
        ks = range(len(ts))
    rng = random.Random(seed)
    best_low, best_rep, best_arg, best_k = None, None, None, None
    for k in ks:
        lo, rp, arg = direction_min(cert, ts[k], wint, scale,
                                    brute_check=brute_check, rng=rng)
        if lo is None:
            return False, dict(reason="no admissible centre at k=%d" % k), scale
        if best_low is None or lo < best_low:
            best_low = lo
        if best_rep is None or rp < best_rep:
            best_rep, best_arg, best_k = rp, arg, k
    ok = best_low >= scale
    return ok, dict(min_lower=Fr(best_low, scale), min_rep=Fr(best_rep, scale),
                    exact=(best_low == best_rep), arg=best_arg, k=best_k), scale

# --------------------------------------------------------------------------

def verify(cert, ks=None, label="", brute_check=0):
    print("=" * 74)
    print("certificate:", cert["id"], label)
    print("  n=%d  L=%s  B=%s  t_K=%s  steps=%d  atoms=%d"
          % (cert["n"], cert["L"], cert["B"], net(cert)[-1], cert["steps"], len(cert["atoms"])))
    res = {}
    ok0, bad = condition_1(cert)
    print("  Condition 1 (D4 invariance)      :", "PASS" if ok0 else "FAIL", "" if ok0 else bad[:2])
    ok1, W = condition_2(cert)
    print("  Condition 2 (total mass < n)     :", "PASS" if ok1 else "FAIL",
          " sum w = %s = %s  (n = %d)" % (W, float(W), cert["n"]))
    ok2, tK = condition_3(cert)
    print("  Condition 3 (net reaches pi/4)   :", "PASS" if ok2 else "FAIL",
          " t_K^2+2t_K-1 = %s" % (tK * tK + 2 * tK - 1))
    ok3, D, v3 = condition_4(cert)
    print("  Condition 4 (B(1+D) < 1)         :", "PASS" if ok3 else "FAIL",
          " D = %s = %.12g ; B(1+D) = %s = %.12g" % (D, float(D), v3, float(v3)))
    t0 = time.time()
    ok4, info, scale = condition_5(cert, ks=ks, brute_check=brute_check)
    dt = time.time() - t0
    if "reason" in info:
        print("  Condition 5                      : FAIL", info["reason"])
    else:
        print("  Condition 5 (min covered mass>=1):", "PASS" if ok4 else "FAIL",
              " min = %s = %s  (cell-lower = %s, exact=%s)"
              % (info["min_rep"], float(info["min_rep"]), info["min_lower"], info["exact"]))
        t, x, y = info["arg"]
        print("       attained at k=%d, t=%s, centre (x,y)=(%s, %s) ~ (%.9f, %.9f)"
              % (info["k"], t, x, y, float(x), float(y)))
    print("  Condition 5 time: %.1fs" % dt)
    allok = ok0 and ok1 and ok2 and ok3 and ok4
    print("  ==> %s : s(%d) >= %s" % ("CERTIFICATE VALID" if allok else "CERTIFICATE REJECTED",
                                      cert["n"], cert["L"]))
    return allok, dict(condition1=ok0, condition2=ok1, condition3=ok2,
                       condition4=ok3, condition5=ok4, info=info, time=dt)


if __name__ == "__main__":
    base = "/home/user/squares/packing/cases/n12_fractional_certificate/"
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    ks = None
    if len(sys.argv) > 2 and sys.argv[2] != "all":
        ks = [int(z) for z in sys.argv[2].split(",")]
    bc = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    if which in ("both", "19-5"):
        verify(load(base + "certificate-19-5.json"), ks=ks, brute_check=bc)
    if which in ("both", "77-20"):
        verify(load(base + "certificate.json"), ks=ks, brute_check=bc)
