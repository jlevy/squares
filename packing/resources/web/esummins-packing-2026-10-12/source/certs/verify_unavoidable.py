"""
Exact-rational verifier for unavoidable point sets (lower bounds for square packing).

Claim certified:  every closed unit square Q contained in the closed square [0,s0]^2 (any
orientation) contains at least one point of P.  Consequently  s(|P|+1) >= s0.

Input JSON:  {"s0": "p/q", "points": [["p/q","p/q"], ...], "claim": "...", ...}
             (all numbers are exact rationals given as strings or ints)

Method: interval branch-and-bound over (cx, cy, t) with t = tan(theta/2) in [0,1]
(theta in [0, pi/2] suffices by the symmetry Q(theta) = Q(theta+pi/2)):
    cos theta = (1-t^2)/(1+t^2)   (decreasing in t on [0,1])
    sin theta = 2t/(1+t^2)        (increasing in t on [0,1])
so on a t-interval [t1,t2] the enclosures of cos and sin are exact rationals.  Everything
is computed with fractions.Fraction: no floating point, no rounding, no transcendental
functions.

A unit square Q(c,theta) is contained in [0,s0]^2 iff its centre c lies in
[w/2, s0-w/2]^2 with w = cos theta + sin theta.  A box (X,Y,T) is
  * irrelevant if it lies outside that centre domain for all t in T (test uses
    w_min = min(w(t1),w(t2)); w is unimodal in t so this is a valid lower bound), or
  * covered by point p if for all (c,theta) in the box  |u|<=1/2 and |v|<=1/2, where
    u = cos*(px-cx) + sin*(py-cy),  v = -sin*(px-cx) + cos*(py-cy)  (interval arithmetic).
Otherwise it is bisected along its widest (weighted) side.  Boxes below a minimum size that
are neither irrelevant nor covered are reported as failure witnesses.

usage:  python verify_unavoidable.py cert.json [--minsize 1/10000000] [--maxboxes N] [--float]
  --float: same algorithm with IEEE-double intervals rounded outward by math.nextafter (rigorous under
           IEEE 754, ~50x faster); default is pure Fraction arithmetic.
exit code 0 = PASS, 1 = FAIL.
"""
import sys, json, time, argparse
from fractions import Fraction as F

HALF = F(1, 2)


def cos_t(t):
    return (1 - t * t) / (1 + t * t)


def sin_t(t):
    return 2 * t / (1 + t * t)


def imul(a, b):
    """interval product [a0,a1]*[b0,b1]"""
    p = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return (min(p), max(p))


def covered_by(p, X, Y, T):
    """True if point p lies in every unit square Q(c,theta) with c in X x Y, tan(theta/2) in T."""
    C = (cos_t(T[1]), cos_t(T[0]))
    S = (sin_t(T[0]), sin_t(T[1]))
    dx = (p[0] - X[1], p[0] - X[0])
    dy = (p[1] - Y[1], p[1] - Y[0])
    a = imul(C, dx); b = imul(S, dy)
    u = (a[0] + b[0], a[1] + b[1])
    if u[1] > HALF or u[0] < -HALF:
        return False
    a = imul((-S[1], -S[0]), dx); b = imul(C, dy)
    v = (a[0] + b[0], a[1] + b[1])
    if v[1] > HALF or v[0] < -HALF:
        return False
    return True


def irrelevant(s0, X, Y, T):
    w1 = cos_t(T[0]) + sin_t(T[0])
    w2 = cos_t(T[1]) + sin_t(T[1])
    wmin = min(w1, w2)
    lo = wmin / 2
    hi = s0 - wmin / 2
    return X[1] < lo or X[0] > hi or Y[1] < lo or Y[0] > hi


def verify(s0, pts, minsize=F(1, 10**7), maxboxes=10**8, verbose=True, tweight=4):
    """Returns (passed, nboxes, witnesses)."""
    root = ((HALF, s0 - HALF), (HALF, s0 - HALF), (F(0), F(1)), 0)  # X, Y, T, hint
    stack = [root]
    nboxes = 0
    ncov = 0
    nirr = 0
    witnesses = []
    npts = len(pts)
    t0 = time.time()
    maxdepth = 0
    while stack:
        X, Y, T, hint = stack.pop()
        nboxes += 1
        if nboxes > maxboxes:
            witnesses.append(("maxboxes", X, Y, T))
            break
        if irrelevant(s0, X, Y, T):
            nirr += 1
            continue
        found = -1
        for j in range(npts):
            i = (hint + j) % npts
            if covered_by(pts[i], X, Y, T):
                found = i
                break
        if found >= 0:
            ncov += 1
            continue
        wx = X[1] - X[0]; wy = Y[1] - Y[0]; wt = (T[1] - T[0]) * tweight
        if max(wx, wy, wt) < minsize:
            witnesses.append(("small", X, Y, T))
            if len(witnesses) >= 20:
                break
            continue
        if wx >= wy and wx >= wt:
            m = (X[0] + X[1]) / 2
            stack.append(((X[0], m), Y, T, hint)); stack.append(((m, X[1]), Y, T, hint))
        elif wy >= wt:
            m = (Y[0] + Y[1]) / 2
            stack.append((X, (Y[0], m), T, hint)); stack.append((X, (m, Y[1]), T, hint))
        else:
            m = (T[0] + T[1]) / 2
            stack.append((X, Y, (T[0], m), hint)); stack.append((X, Y, (m, T[1]), hint))
        if verbose and nboxes % 200000 == 0:
            print(f"  ... {nboxes} boxes, {ncov} covered, {nirr} irrelevant, stack {len(stack)}, {time.time()-t0:.0f}s", flush=True)
    passed = len(witnesses) == 0
    if verbose:
        print(f"boxes={nboxes} covered={ncov} irrelevant={nirr} witnesses={len(witnesses)} time={time.time()-t0:.1f}s")
    return passed, nboxes, witnesses


# ----------------------------------------------------------------------------------------------
# Fast mode: IEEE-754 double intervals with outward rounding via math.nextafter (rigorous under
# IEEE correctly-rounded +,-,*,/; no transcendental functions are used, cos/sin are the rational
# functions of t above).  ~50x faster than Fraction mode; same branch-and-bound.
# ----------------------------------------------------------------------------------------------
import math
_INF = math.inf
_na = math.nextafter


def _dn(x):
    return _na(x, -_INF)


def _up(x):
    return _na(x, _INF)


def _fadd(a, b):
    return (_dn(a[0] + b[0]), _up(a[1] + b[1]))


def _fmul(a, b):
    p = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return (_dn(min(p)), _up(max(p)))


def _fdiv_pos(a, b):
    """a / b with b > 0"""
    lo = min(a[0] / b[0], a[0] / b[1])
    hi = max(a[1] / b[0], a[1] / b[1])
    return (_dn(lo), _up(hi))


def _fcos(T):
    """enclosure of (1-t^2)/(1+t^2) for t in T subset [0,1]  (decreasing)"""
    t2 = _fmul(T, T)
    num = (_dn(1.0 - t2[1]), _up(1.0 - t2[0]))
    den = (_dn(1.0 + t2[0]), _up(1.0 + t2[1]))
    return _fdiv_pos(num, den)


def _fsin(T):
    t2 = _fmul(T, T)
    num = (_dn(2.0 * T[0]), _up(2.0 * T[1]))
    den = (_dn(1.0 + t2[0]), _up(1.0 + t2[1]))
    return _fdiv_pos(num, den)


def covered_by_f(p, X, Y, T):
    C = _fcos(T); S = _fsin(T)
    dx = (_dn(p[0] - X[1]), _up(p[0] - X[0]))
    dy = (_dn(p[1] - Y[1]), _up(p[1] - Y[0]))
    u = _fadd(_fmul(C, dx), _fmul(S, dy))
    if u[1] > 0.5 or u[0] < -0.5:
        return False
    v = _fadd(_fmul((-S[1], -S[0]), dx), _fmul(C, dy))
    if v[1] > 0.5 or v[0] < -0.5:
        return False
    return True


def irrelevant_f(s0, X, Y, T):
    # w(t) = cos+sin is unimodal on [0,1]; lower bound of w over T is min of the two endpoint values,
    # each computed as a rigorous lower bound (degenerate interval at the endpoint).
    def wlo(t):
        c = _fcos((t, t)); s = _fsin((t, t))
        return _dn(c[0] + s[0])
    wmin = min(wlo(T[0]), wlo(T[1]))
    lo = _dn(wmin / 2)
    hi = _up(s0[1] - wmin / 2)   # s0 given as interval (s0lo, s0hi); use upper bound => conservative
    return X[1] < lo or X[0] > hi or Y[1] < lo or Y[0] > hi


def verify_float(s0, pts, minsize=1e-7, maxboxes=10**8, verbose=True, tweight=4):
    """s0: Fraction; pts: list of Fraction pairs.  Points are rounded *inward*? No: a point is exact data;
    we take the float interval enclosing the rational point (both endpoints) - the point set is then a set
    of tiny boxes and 'covered' means the whole tiny box is inside, which is conservative."""
    s0f = (_dn(float(s0)), _up(float(s0)))
    ptsf = []
    for x, y in pts:
        fx, fy = float(x), float(y)
        ptsf.append(((_dn(fx), _up(fx)), (_dn(fy), _up(fy))))
    root = ((_up(0.5), _dn(s0f[0] - 0.5)), (_up(0.5), _dn(s0f[0] - 0.5)), (0.0, 1.0), 0)
    # NB the root must contain the whole centre domain: [1/2, s0-1/2]^2 x [0,1]; we round the root
    # inward here only by 1 ulp which is irrelevant since the domain boundary needs w>=1 strictly... to be
    # safe use outward rounding:
    root = ((_dn(0.5), _up(s0f[1] - 0.5)), (_dn(0.5), _up(s0f[1] - 0.5)), (0.0, 1.0), 0)
    stack = [root]
    nboxes = ncov = nirr = 0
    witnesses = []
    npts = len(ptsf)
    t0 = time.time()
    while stack:
        X, Y, T, hint = stack.pop()
        nboxes += 1
        if nboxes > maxboxes:
            witnesses.append(("maxboxes", X, Y, T)); break
        if irrelevant_f(s0f, X, Y, T):
            nirr += 1; continue
        found = -1
        for j in range(npts):
            i = (hint + j) % npts
            px, py = ptsf[i]
            # point as a tiny box: require coverage for both endpoints (linear in p => interval hull ok)
            if covered_by_f((px[0], py[0]), X, Y, T) and covered_by_f((px[1], py[1]), X, Y, T)                and covered_by_f((px[0], py[1]), X, Y, T) and covered_by_f((px[1], py[0]), X, Y, T):
                found = i; break
        if found >= 0:
            ncov += 1; continue
        wx = X[1] - X[0]; wy = Y[1] - Y[0]; wt = (T[1] - T[0]) * tweight
        if max(wx, wy, wt) < minsize:
            witnesses.append(("small", X, Y, T))
            if len(witnesses) >= 20:
                break
            continue
        if wx >= wy and wx >= wt:
            m = 0.5 * (X[0] + X[1])
            stack.append(((X[0], m), Y, T, hint)); stack.append(((m, X[1]), Y, T, hint))
        elif wy >= wt:
            m = 0.5 * (Y[0] + Y[1])
            stack.append((X, (Y[0], m), T, hint)); stack.append((X, (m, Y[1]), T, hint))
        else:
            m = 0.5 * (T[0] + T[1])
            stack.append((X, Y, (T[0], m), hint)); stack.append((X, Y, (m, T[1]), hint))
        if verbose and nboxes % 500000 == 0:
            print(f"  ... {nboxes} boxes, {ncov} covered, {nirr} irrelevant, stack {len(stack)}, {time.time()-t0:.0f}s", flush=True)
    passed = len(witnesses) == 0
    if verbose:
        print(f"[float mode] boxes={nboxes} covered={ncov} irrelevant={nirr} witnesses={len(witnesses)} time={time.time()-t0:.1f}s")
    return passed, nboxes, witnesses


def load(path):
    d = json.load(open(path))
    s0 = F(str(d["s0"]))
    pts = [(F(str(x)), F(str(y))) for x, y in d["points"]]
    return d, s0, pts


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("--minsize", type=str, default="1/10000000")
    ap.add_argument("--maxboxes", type=int, default=10**8)
    ap.add_argument("--float", action="store_true", help="fast mode: IEEE double intervals with outward rounding (nextafter)")
    a = ap.parse_args()
    d, s0, pts = load(a.cert)
    print(f"certificate: {a.cert}\n  s0 = {s0} = {float(s0):.9f}\n  {len(pts)} points; claim: s({len(pts)+1}) >= s0")
    if a.float:
        ok, nb, wit = verify_float(s0, pts, minsize=float(F(a.minsize)), maxboxes=a.maxboxes)
    else:
        ok, nb, wit = verify(s0, pts, minsize=F(a.minsize), maxboxes=a.maxboxes)
    if ok:
        print(f"PASS: the {len(pts)} points are unavoidable in [0,{float(s0):.9f}]^2  =>  s({len(pts)+1}) >= {float(s0):.9f}")
        sys.exit(0)
    else:
        print("FAIL. witnesses (X, Y, T=tan(theta/2) intervals):")
        for w in wit[:10]:
            print("  ", w[0], [float(w[1][0]), float(w[1][1])], [float(w[2][0]), float(w[2][1])], [float(w[3][0]), float(w[3][1])])
        sys.exit(1)
