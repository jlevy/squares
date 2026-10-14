"""Geometry of unit squares with features, generic in the number type (float or mpmath.mpf).

Square i: centre (x, y), angle th (cos c, sin s).  Local frame u = (c, s), v = (-s, c).
  corner a (a = 0..3) = centre + H*(su*u + sv*v) with (su, sv) = CU[a] = (1,1), (-1,1), (-1,-1), (1,-1)
  side k (k = 0..3)   = outward normal R(th) e_k, e_k = (1,0), (0,1), (-1,0), (0,-1); corner k lies between sides k and k+1.

Contacts (constraint g >= 0, g = 0 when touching):
  ('W', i, a, w)     corner a of square i on wall w in L, R, B, T      g = Px, S-Px, Py, S-Py
  ('C', j, a, i, k)  corner a of square j on (the line of) side k of square i:   g = n_ik . (P_ja - c_i) - H

Variables: square i -> 3i (x), 3i+1 (y), 3i+2 (theta in radians); side S -> 3n.
"""

CU = ((1, 1), (-1, 1), (-1, -1), (1, -1))
EK = ((1, 0), (0, 1), (-1, 0), (0, -1))


def offset(c, s, a, H):
    su, sv = CU[a]
    return H * (c * su - s * sv), H * (s * su + c * sv)


def normal(c, s, k):
    ex, ey = EK[k]
    return c * ex - s * ey, s * ex + c * ey


def eval_contact(ct, X, Y, C, S_, side, H, order=2):
    """Return (g, grad, hess): grad = list of (var, value); hess = list of (v1, v2, value) with each unordered pair once
    (diagonal included once).  X, Y, C, S_ = per-square x, y, cos, sin; side = container side S."""
    n = len(X)
    if ct[0] == 'W':
        _, i, a, w = ct
        ox, oy = offset(C[i], S_[i], a, H)
        px, py = X[i] + ox, Y[i] + oy
        xi, yi, ti, vs = 3 * i, 3 * i + 1, 3 * i + 2, 3 * n
        if w == 'L':
            g, gr, he = px, [(xi, 1), (ti, -oy)], [(ti, ti, -ox)]
        elif w == 'R':
            g, gr, he = side - px, [(vs, 1), (xi, -1), (ti, oy)], [(ti, ti, ox)]
        elif w == 'B':
            g, gr, he = py, [(yi, 1), (ti, ox)], [(ti, ti, -oy)]
        else:
            g, gr, he = side - py, [(vs, 1), (yi, -1), (ti, -ox)], [(ti, ti, oy)]
        return g, gr, he
    _, j, a, i, k = ct
    nx, ny = normal(C[i], S_[i], k)
    npx, npy = -ny, nx                                   # d n / d th_i
    ox, oy = offset(C[j], S_[j], a, H)
    dx, dy = X[j] + ox - X[i], Y[j] + oy - Y[i]
    ppx, ppy = -oy, ox                                   # d P / d th_j
    g = nx * dx + ny * dy - H
    xi, yi, ti, xj, yj, tj = 3 * i, 3 * i + 1, 3 * i + 2, 3 * j, 3 * j + 1, 3 * j + 2
    gr = [(xi, -nx), (yi, -ny), (xj, nx), (yj, ny), (ti, npx * dx + npy * dy), (tj, nx * ppx + ny * ppy)]
    if order < 2:
        return g, gr, []
    he = [(ti, ti, -(nx * dx + ny * dy)), (ti, xi, -npx), (ti, yi, -npy), (ti, xj, npx), (ti, yj, npy),
          (ti, tj, npx * ppx + npy * ppy), (tj, tj, -(nx * ox + ny * oy))]
    return g, gr, he


def tangential(ct, X, Y, C, S_, H):
    """Position of the touching corner along the side (in (-H, H) when it projects inside the side)."""
    _, j, a, i, k = ct
    nx, ny = normal(C[i], S_[i], k)
    ox, oy = offset(C[j], S_[j], a, H)
    return -ny * (X[j] + ox - X[i]) + nx * (Y[j] + oy - Y[i])


def sat_gap(i, j, X, Y, C, S_, H, absf=abs):
    """Separating-axis gap of squares i, j (> 0: disjoint with that clearance along the best of the 4 face normals;
    = max over axes, so it is a lower bound on the Euclidean distance and > 0 iff disjoint)."""
    best = None
    dx, dy = X[j] - X[i], Y[j] - Y[i]
    for own, oth in ((i, j), (j, i)):
        for k in (0, 1):
            nx, ny = normal(C[own], S_[own], k)
            proj = absf(nx * dx + ny * dy)
            ca = nx * C[oth] + ny * S_[oth]                # n . u_oth
            sa = -nx * S_[oth] + ny * C[oth]               # n . v_oth
            g = proj - H - H * (absf(ca) + absf(sa))
            if best is None or g > best:
                best = g
    return best


def wall_gaps(i, X, Y, C, S_, side, H, absf=abs):
    e = H * (absf(C[i]) + absf(S_[i]))
    return (X[i] - e, side - X[i] - e, Y[i] - e, side - Y[i] - e)


def describe(ct):
    if ct[0] == 'W':
        return f'corner {ct[2]} of #{ct[1]} on wall {ct[3]}'
    return f'corner {ct[2]} of #{ct[1]} on side {ct[4]} of #{ct[3]}'
