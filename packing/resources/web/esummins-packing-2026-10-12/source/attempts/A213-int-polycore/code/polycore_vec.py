"""A213 Phase 2 -- the vertex certification VECTORISED (numpy), the integer path of polycore_int as the reference.

certify_verts(verts, boxes) decides, for every (vertex, piece box) pair, the 16 quadratic tests of polycore.vertex_ok
(4 corners x 2 orientations x 2 quadratics).  Two vectorised routes, both bit-exact:

  (a) FLOAT FILTER (`certify_verts`, the default).  Every test is the sign of a low-degree polynomial in doubles that
      are exact (the corners, t0, t1 = k/2^24) or correctly rounded (the vertex).  The polynomial is evaluated in
      binary64 together with a RIGOROUS forward error bound (per element: the propagated input error plus one
      epsilon per rounding on the magnitude sum), and the sign is taken only where |value| > bound; a (vertex, box)
      pair with any undecided test goes to the exact integer path polycore_int.vertex_ok_h.  The decisions are
      therefore the library's on every input; the filter only chooses which pairs pay for exact arithmetic.
  (b) OBJECT DTYPE (`certify_verts_obj`).  The integer formulas of polycore_int on numpy object arrays (Python ints
      inside C loops): exact, no bound, but no early exit and one bignum op per element per step.

The two-limb int64 representation the brief suggested does not fit: the endpoint value is < 2^142 and the
discriminant < 2^183 (notes/int_polycore.md), beyond 126 bits; the same bound is what a C kernel must respect
(__int128 holds the interior test only) -- see notes/int_polycore.md, Phase 3.
"""
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import polycore_int as PI                                      # noqa: E402
import numpy as np                                             # noqa: E402

EPS = 2.0 ** -53
STATS = dict(calls=0, pairs=0, exact_pairs=0, obj_calls=0)
_SIGNS = ((1, 1), (1, -1), (-1, -1), (-1, 1))                  # corners: (x0,y0),(x1,y0),(x1,y1),(x0,y1) as x/y picks


def _ge0(x, err):
    """three-valued  x >= 0  from a float value and an absolute error bound: (certainly true, certainly false)."""
    return x > err, x < -err


def _and(a, b):
    return a[0] & b[0], a[1] | b[1]


def _or(a, b):
    return a[0] | b[0], a[1] & b[1]


def _not(a):
    return a[1], a[0]


def _quad_f(A, B, C, eA, eB, eC, t, tt, ab):
    """A t^2 + B t + C >= 0 at one endpoint t (tt = t*t exact), three-valued.  ab = |A|, |B|, |C| arrays."""
    S = ab[0] * tt + ab[1] * abs(t) + ab[2]
    P = A * tt + B * t + C
    err = eA * tt + eB * abs(t) + eC + 5.0 * EPS * S
    return _ge0(P, err)


def _quad_ok_f(A, B, C, eA, eB, eC, t0, t1, tt0, tt1):
    """polycore._quad_nonneg three-valued: endpoints, and the interior minimum when A > 0 and -B/(2A) in [t0, t1]."""
    ab = (np.abs(A), np.abs(B), np.abs(C))
    ok = _and(_quad_f(A, B, C, eA, eB, eC, t0, tt0, ab), _quad_f(A, B, C, eA, eB, eC, t1, tt1, ab))
    a_pos = (A > eA, A < -eA)                                  # A > 0 ?
    A2 = 2.0 * A
    eA2 = 2.0 * eA
    L = -B - A2 * t0                                           # t0 2A <= -B
    eL = eB + eA2 * abs(t0) + 3.0 * EPS * (ab[1] + np.abs(A2) * abs(t0))
    R = A2 * t1 + B                                            # -B <= t1 2A
    eR = eB + eA2 * abs(t1) + 3.0 * EPS * (np.abs(A2) * abs(t1) + ab[1])
    inner = _and(a_pos, _and(_ge0(L, eL), _ge0(R, eR)))
    D = 4.0 * (A * C) - B * B
    eD = 4.0 * (eA * ab[2] + eC * ab[0] + eA * eC) + (2.0 * ab[1] * eB + eB * eB) + 4.0 * EPS * (4.0 * ab[0] * ab[2] + ab[1] * ab[1])
    return _and(ok, _or(_not(inner), _ge0(D, eD)))


def _compile(verts, boxes):
    vx = np.array([float(x) for (x, _y) in verts])
    vy = np.array([float(y) for (_x, y) in verts])
    bx = np.array([[b.x0, b.x1, b.x1, b.x0] for (b, _t0, _t1) in boxes])      # (nb, 4)
    by = np.array([[b.y0, b.y0, b.y1, b.y1] for (b, _t0, _t1) in boxes])
    t0 = np.array([float(a) for (_b, a, _c) in boxes])
    t1 = np.array([float(c) for (_b, _a, c) in boxes])
    exact_t = all(Fr(float(a)) == a and Fr(float(c)) == c for (_b, a, c) in boxes)
    return vx, vy, bx, by, t0, t1, exact_t


def pair_status(verts, boxes):
    """(certainly ok, certainly bad) boolean arrays of shape (nv, nb) from the float filter."""
    vx, vy, bx, by, t0, t1, exact_t = _compile(verts, boxes)
    nv, nb = len(vx), len(bx)
    if not exact_t or nv == 0 or nb == 0:
        z = np.zeros((nv, nb), bool)
        return z, z
    dx = vx[:, None, None] - bx[None, :, :]                    # (nv, nb, 4)
    dy = vy[:, None, None] - by[None, :, :]
    delta = EPS * (2.0 * (np.abs(vx) + np.abs(vy))[:, None, None] + 2.0 * (np.abs(dx) + np.abs(dy)))
    T0, T1 = t0[None, :, None], t1[None, :, None]
    TT0, TT1 = T0 * T0, T1 * T1
    ok = (np.ones(dx.shape, bool), np.zeros(dx.shape, bool))
    for (u, w) in ((dx, dy), (dy, -dx)):
        A, C, B = 0.5 + u, 0.5 - u, -2.0 * w
        eA, eC, eB = delta + EPS * np.abs(A), delta + EPS * np.abs(C), 2.0 * delta
        ok = _and(ok, _quad_ok_f(A, B, C, eA, eB, eC, T0, T1, TT0, TT1))
        ok = _and(ok, _quad_ok_f(C, -B, A, eC, eB, eA, T0, T1, TT0, TT1))
    return ok[0].all(axis=2), ok[1].any(axis=2)


def certify_verts(verts, boxes):
    """drop-in for multibox.certify_verts: the float filter, exact integer arithmetic where it cannot decide."""
    STATS["calls"] += 1
    nv, nb = len(verts), len(boxes)
    STATS["pairs"] += nv * nb
    good, badp = pair_status(verts, boxes)
    bad = []
    ibs = None
    for i in range(nv):
        if badp[i].any():
            bad.append(i)
            continue
        und = np.flatnonzero(~good[i])
        if len(und) == 0:
            continue
        if ibs is None:
            ibs = [PI.ibox_of(pb, pt0, pt1) for (pb, pt0, pt1) in boxes]
        X, Y, W = PI.hom(*verts[i])
        for j in und.tolist():
            STATS["exact_pairs"] += 1
            if not PI.vertex_ok_h(X, Y, W, ibs[j]):
                bad.append(i)
                break
    return bad


# ----------------------------------------------------------------------------------- (b) object dtype
def _quad_ok_obj(A, B, C, T0SQ, T0E, T1SQ, T1E, ESQ, E, TT0, TT1):
    e0 = (A * T0SQ + B * T0E + C * ESQ) >= 0
    e1 = (A * T1SQ + B * T1E + C * ESQ) >= 0
    nb = -B * E
    inner = (A > 0) & (TT0 * A <= nb) & (nb <= TT1 * A)
    return e0 & e1 & (~inner | ((4 * A * C - B * B) >= 0))


def certify_verts_obj(verts, boxes):
    """the integer formulas on numpy OBJECT arrays (exact; measured against the scalar path)."""
    STATS["obj_calls"] += 1
    ibs = [PI.ibox_of(pb, pt0, pt1) for (pb, pt0, pt1) in boxes]
    hv = [PI.hom(x, y) for (x, y) in verts]
    nv, nb = len(hv), len(ibs)
    if nv == 0 or nb == 0:
        return []
    X = np.array([p[0] for p in hv], dtype=object)[:, None, None]
    Y = np.array([p[1] for p in hv], dtype=object)[:, None, None]
    W = np.array([p[2] for p in hv], dtype=object)[:, None, None]
    CW = np.array([ib.cw for ib in ibs], dtype=object)[None, :, None]
    CX = np.array([ib.cx for ib in ibs], dtype=object)[None, :, :]
    CY = np.array([ib.cy for ib in ibs], dtype=object)[None, :, :]
    col = lambda f: np.array([f(ib) for ib in ibs], dtype=object)[None, :, None]   # noqa: E731
    T0SQ, T0E, T1SQ, T1E, ESQ, E = (col(lambda ib: ib.t0sq), col(lambda ib: ib.t0e), col(lambda ib: ib.t1sq),
                                    col(lambda ib: ib.t1e), col(lambda ib: ib.esq), col(lambda ib: ib.e))
    TT0, TT1 = col(lambda ib: ib.tt0), col(lambda ib: ib.tt1)
    S2 = W * CW
    UX = X * CW - CX * W
    UY = Y * CW - CY * W
    ok = np.ones((nv, nb, 4), bool)
    for (U, V) in ((UX, UY), (UY, -UX)):
        P, M, B4 = S2 + 2 * U, S2 - 2 * U, 4 * V
        ok &= _quad_ok_obj(P, -B4, M, T0SQ, T0E, T1SQ, T1E, ESQ, E, TT0, TT1).astype(bool)
        ok &= _quad_ok_obj(M, B4, P, T0SQ, T0E, T1SQ, T1E, ESQ, E, TT0, TT1).astype(bool)
    pair = ok.all(axis=2)
    return [i for i in range(nv) if not pair[i].all()]


def rep():
    return dict(STATS)
