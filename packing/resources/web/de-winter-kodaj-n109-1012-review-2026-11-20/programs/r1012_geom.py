"""Lane r1012's third formulation: centres and half-widths, in Python Fractions.

Clean room, written for the stage 4 review of issue 1012. It decides nothing on
its own. The self-test and the controls use it to recompute margins and
clearances a third way (control C0), to move squares exactly for the closing and
wall controls, and the check uses it to describe each pair's Euclidean gap.

For a unit square given by corners p0..p3 in cyclic order, the centre is
(p0 + p2)/2 and the edge vectors e = p1 - p0, f = p2 - p1 are perpendicular unit
vectors. On a unit axis w its projection is the interval of half-width
h(w) = (|e.w| + |f.w|)/2 about c.w, so on each of the four axes of a pair the
separation is |d.w| - h_i(w) - h_j(w), d the centre difference.
"""

from fractions import Fraction


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def add(p, q):
    return (p[0] + q[0], p[1] + q[1])


def scale(p, t):
    return (p[0] * t, p[1] * t)


def dot(p, q):
    return p[0] * q[0] + p[1] * q[1]


def centre(quad):
    return ((quad[0][0] + quad[2][0]) / 2, (quad[0][1] + quad[2][1]) / 2)


def edges(quad):
    return sub(quad[1], quad[0]), sub(quad[2], quad[1])


def half_width(quad, w):
    e, f = edges(quad)
    return (abs(dot(e, w)) + abs(dot(f, w))) / 2


def axes(qi, qj):
    ei, fi = edges(qi)
    ej, fj = edges(qj)
    return [ei, fi, ej, fj]


def margin(qi, qj):
    d = sub(centre(qj), centre(qi))
    return max(abs(dot(d, w)) - half_width(qi, w) - half_width(qj, w) for w in axes(qi, qj))


def clearances(quad, side):
    c = centre(quad)
    hx = half_width(quad, (Fraction(1), Fraction(0)))
    hy = half_width(quad, (Fraction(0), Fraction(1)))
    return (c[0] - hx, c[1] - hy, side - c[0] - hx, side - c[1] - hy)


def translate(quad, v):
    return [add(p, v) for p in quad]


def closing_time(qi, qj, target):
    """The t at which moving qj by -t * d (d = c_j - c_i) makes the margin exactly target.

    On an axis w with d.w != 0 the separation is (1 - t)|d.w| - H_w, H_w the two
    half-widths, which is decreasing in t; it equals target at
    t_w = 1 - (target + H_w)/|d.w|. The margin, the greatest separation, equals
    target at the greatest t_w, since every other separation is then at most
    target, and an axis with d.w = 0 has separation -H_w < target.
    """
    d = sub(centre(qj), centre(qi))
    best = None
    for w in axes(qi, qj):
        dw = abs(dot(d, w))
        if dw == 0:
            continue
        hw = half_width(qi, w) + half_width(qj, w)
        t = 1 - (target + hw) / dw
        if best is None or t > best:
            best = t
    return best, d


def close_pair(qi, qj, target):
    """qj moved along the centre line so that the pair's margin is exactly target."""
    t, d = closing_time(qi, qj, target)
    return translate(qj, scale(d, -t)), scale(d, -t)


def to_wall(quad, side, wall, target):
    """quad translated perpendicular to wall (0 L, 1 B, 2 R, 3 T) to clearance target."""
    c = clearances(quad, side)[wall]
    shift = c - target
    v = [(-shift, 0), (0, -shift), (shift, 0), (0, shift)][wall]
    return translate(quad, (Fraction(v[0]), Fraction(v[1]))), shift


def _seg_d2(p, a, b):
    """Squared distance from p to the segment a-b, where |b - a| = 1 exactly."""
    e = sub(b, a)
    ap = sub(p, a)
    t = dot(ap, e)
    if t <= 0:
        return dot(ap, ap)
    if t >= 1:
        bp = sub(p, b)
        return dot(bp, bp)
    return dot(ap, ap) - t * t


def gap2(qi, qj):
    """The squared Euclidean distance between two unit squares known to be apart.

    For disjoint convex polygons the least distance is attained between a vertex of
    one and an edge of the other, and each edge here has length exactly 1, so the
    squared distance is a rational.
    """
    best = None
    for p_quad, e_quad in ((qi, qj), (qj, qi)):
        for p in p_quad:
            for k in range(4):
                v = _seg_d2(p, e_quad[k], e_quad[(k + 1) % 4])
                if best is None or v < best:
                    best = v
    return best


def tilt_degrees_text(quad):
    """The edge direction's angle in degrees, folded to (-45, 45], as a 12-place string."""
    from decimal import Decimal, getcontext
    import math
    e, _ = edges(quad)
    getcontext().prec = 40
    ang = math.degrees(math.atan2(float(e[1]), float(e[0])))
    while ang > 45:
        ang -= 90
    while ang <= -45:
        ang += 90
    return f"{Decimal(ang):.12f}"
