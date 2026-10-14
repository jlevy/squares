"""Exact convex-polygon helpers (fractions only). Written for the review; no code of the edition is used."""
from fractions import Fraction as Fr

U = Fr(1169, 250)
C_CAP = Fr(4675531, 10**6)
R_REF = Fr(4675530093604551, 10**15)
RHO = Fr(207107, 500000)


def fr(x):
    return Fr(x)


def poly(verts):
    return [(Fr(x), Fr(y)) for x, y in verts]


def rect(x0, x1, y0, y1):
    return poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def is_ccw_convex(P):
    n = len(P)
    for i in range(n):
        if cross(P[i], P[(i + 1) % n], P[(i + 2) % n]) <= 0:
            return False
    return True


def ccw(P):
    """Return the polygon in counter-clockwise order (reverse if clockwise); checks convexity."""
    if is_ccw_convex(P):
        return list(P)
    Q = list(reversed(P))
    assert is_ccw_convex(Q), "not strictly convex"
    return Q


def mirror_x(P, cx=U / 2):
    return ccw([(2 * cx - x, y) for x, y in P])


def d4_image(P, g, c=(U / 2, U / 2)):
    """g is one of the eight signed permutation matrices ((a,b),(c,d)) acting about c."""
    out = []
    for x, y in P:
        dx, dy = x - c[0], y - c[1]
        out.append((c[0] + g[0][0] * dx + g[0][1] * dy, c[1] + g[1][0] * dx + g[1][1] * dy))
    return ccw(out)


D4 = (((1, 0), (0, 1)), ((0, -1), (1, 0)), ((-1, 0), (0, -1)), ((0, 1), (-1, 0)),
      ((1, 0), (0, -1)), ((-1, 0), (0, 1)), ((0, 1), (1, 0)), ((0, -1), (-1, 0)))


def clip_halfplane(P, a, b, c):
    """Keep the closed half-plane a x + b y + c >= 0 (Sutherland-Hodgman, exact)."""
    out = []
    n = len(P)
    for i in range(n):
        p, q = P[i], P[(i + 1) % n]
        fp = a * p[0] + b * p[1] + c
        fq = a * q[0] + b * q[1] + c
        if fp >= 0:
            out.append(p)
        if (fp > 0 and fq < 0) or (fp < 0 and fq > 0):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    # remove duplicates
    res = []
    for v in out:
        if not res or res[-1] != v:
            res.append(v)
    if len(res) > 1 and res[0] == res[-1]:
        res.pop()
    return res


def clip_box(P, x0, x1, y0, y1):
    Q = ccw(P)
    for a, b, c in ((1, 0, -x0), (-1, 0, x1), (0, 1, -y0), (0, -1, y1)):
        Q = clip_halfplane(Q, Fr(a), Fr(b), Fr(c))
        if len(Q) < 3:
            return Q
    return Q


def diam2(P):
    return max((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 for p in P for q in P)


def bbox(P):
    xs = [p[0] for p in P]
    ys = [p[1] for p in P]
    return min(xs), max(xs), min(ys), max(ys)


def strictly_separated(P, Q):
    """Two closed convex polygons are disjoint iff some edge line of one has the whole other polygon strictly
    outside (separating-axis theorem for convex polygons)."""
    for A, B in ((P, Q), (Q, P)):
        n = len(A)
        for i in range(n):
            p, q = A[i], A[(i + 1) % n]
            # inside is left of the edge for ccw A; the other polygon is strictly outside if all its vertices are strictly right
            if all(cross(p, q, v) < 0 for v in B):
                return True
    return False


def point_in(P, v):
    n = len(P)
    return all(cross(P[i], P[(i + 1) % n], v) >= 0 for i in range(n))


def contains(P, Q):
    """closed convex P contains closed convex Q"""
    return all(point_in(P, v) for v in Q)


def rot(t):
    """unit vector at angle 2 atan t"""
    t = Fr(t)
    return ((1 - t * t) / (1 + t * t), 2 * t / (1 + t * t))


def cmul(p, q):
    return (p[0] * q[0] - p[1] * q[1], p[0] * q[1] + p[1] * q[0])


def cconj(p):
    return (p[0], -p[1])


def vcross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def vdot(a, b):
    return a[0] * b[0] + a[1] * b[1]


J = (Fr(0), Fr(1))


def lift(t, m):
    """tan-half of angle + m*pi/2"""
    t = Fr(t)
    if m == 0:
        return t
    if m == 1:
        return (1 + t) / (1 - t)
    if m == -1:
        return (t - 1) / (t + 1)
    raise ValueError(m)
