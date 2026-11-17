"""Lane L163 closed forms, for the self-test and the controls plan; decides no file.

Everything here is in `fractions.Fraction` and is written apart from both methods.
The margin is computed a third way: each square's four corners are projected on each
of the four unit edge normals of the pair, and the gap on a normal is the distance
between the two projection intervals. The clearances are the corners' least and
greatest coordinates against the walls.

It also builds rows (centre, t) from fractions, closes a pair along its centre line to
a stated margin, and moves a square to a wall by a stated clearance.
"""

from __future__ import annotations

from fractions import Fraction as F

Row = tuple[int, int, int, int, int, int]


def row(cx: F, cy: F, t: F) -> Row:
    cx, cy, t = F(cx), F(cy), F(t)
    return (cx.numerator, cx.denominator, cy.numerator, cy.denominator, t.numerator, t.denominator)


def parts(r: Row) -> tuple[F, F, F]:
    return F(r[0], r[1]), F(r[2], r[3]), F(r[4], r[5])


def cos_sin(t: F) -> tuple[F, F]:
    d = 1 + t * t
    return (1 - t * t) / d, 2 * t / d


def corners(r: Row) -> list[tuple[F, F]]:
    cx, cy, t = parts(r)
    c, s = cos_sin(t)
    h = F(1, 2)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in ((-h, -h), (h, -h), (h, h), (-h, h))]


def normals(r: Row) -> list[tuple[F, F]]:
    c, s = cos_sin(parts(r)[2])
    return [(c, s), (-s, c)]


def gaps(ri: Row, rj: Row) -> list[F]:
    """Projection gaps on u_i, v_i, u_j, v_j."""
    pi, pj = corners(ri), corners(rj)
    out: list[F] = []
    for w in normals(ri) + normals(rj):
        a = [p[0] * w[0] + p[1] * w[1] for p in pi]
        b = [p[0] * w[0] + p[1] * w[1] for p in pj]
        out.append(max(min(b) - max(a), min(a) - max(b)))
    return out


def margin(ri: Row, rj: Row) -> F:
    return max(gaps(ri, rj))


def clearances(r: Row, side: F) -> tuple[F, F, F, F]:
    pts = corners(r)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), min(ys), side - max(xs), side - max(ys)


def translate(r: Row, dx: F, dy: F) -> Row:
    cx, cy, t = parts(r)
    return row(cx + dx, cy + dy, t)


def closing(ri: Row, rj: Row, delta: F) -> tuple[F, list[F], list[F]]:
    """The time tau at which square j, moved by -tau (C_j - C_i), has margin -delta.

    Each gap falls linearly at the rate |d . w| for a fixed normal w while tau < 1, so
    the margin reaches -delta at max over the moving normals of (g + delta) / rate.
    Returns tau, the gaps and the rates.
    """
    cxi, cyi, _ = parts(ri)
    cxj, cyj, _ = parts(rj)
    d = (cxj - cxi, cyj - cyi)
    g = gaps(ri, rj)
    rates = [abs(d[0] * w[0] + d[1] * w[1]) for w in normals(ri) + normals(rj)]
    times = [(gk + delta) / rk for gk, rk in zip(g, rates, strict=True) if rk > 0]
    for gk, rk in zip(g, rates, strict=True):
        if rk == 0 and gk > -delta:
            raise ValueError("a normal with no rate stays above -delta")
    tau = max(times)
    if not 0 <= tau < 1:
        raise ValueError("closing time outside [0, 1)")
    return tau, g, rates


def close_pair(ri: Row, rj: Row, delta: F) -> tuple[Row, F]:
    """Square j moved along the centre line to margin -delta, and the move's squared length."""
    tau, _, _ = closing(ri, rj, delta)
    cxi, cyi, _ = parts(ri)
    cxj, cyj, _ = parts(rj)
    dx, dy = cxj - cxi, cyj - cyi
    return translate(rj, -tau * dx, -tau * dy), tau * tau * (dx * dx + dy * dy)


def to_wall(r: Row, wall: int, side: F, delta: F) -> Row:
    """Square moved toward wall 0..3 (left, bottom, right, top) to clearance -delta."""
    c = clearances(r, side)[wall]
    step = c + delta
    dx, dy = [(-step, F(0)), (F(0), -step), (step, F(0)), (F(0), step)][wall]
    return translate(r, dx, dy)


def floor_places(x: F, k: int) -> str:
    """x rounded down at k decimal places, printed."""
    q = (x.numerator * 10**k) // x.denominator
    sign = "-" if q < 0 else ""
    q = abs(q)
    ip, fp = divmod(q, 10**k)
    return f"{sign}{ip}.{fp:0{k}d}" if k else f"{sign}{ip}"


def ceil_places(x: F, k: int) -> str:
    """x rounded up at k decimal places, printed."""
    return floor_places(ceil_value(x, k), k)


def ceil_value(x: F, k: int) -> F:
    return F(-((-x.numerator * 10**k) // x.denominator), 10**k)


def floor_value(x: F, k: int) -> F:
    return F((x.numerator * 10**k) // x.denominator, 10**k)


def sci(x: F, digits: int = 6) -> str:
    """A short scientific print of an exact fraction (display only)."""
    if x == 0:
        return "0"
    sign = "-" if x < 0 else ""
    a = abs(x)
    e = 0
    while a >= 10:
        a /= 10
        e += 1
    while a < 1:
        a *= 10
        e -= 1
    m = floor_places(a, digits - 1)
    return f"{sign}{m}e{e:+d}"
