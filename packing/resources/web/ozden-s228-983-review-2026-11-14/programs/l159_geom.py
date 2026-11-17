"""Lane L159's geometry helpers for the self-test, the controls and the description.

Clean-room code written for the stage 4 review of issue #983. It decides nothing about
the certificate: it builds squares from a centre and a frame, gives the closed-form
pair margin from centres and half-widths (not corners), the times at which a pair
closed along its centre line reaches contact and passes it, and exact decimal prints.
"""

from __future__ import annotations

from fractions import Fraction

Rational = tuple[int, int]
Point = tuple[Rational, Rational]
FPoint = tuple[Fraction, Fraction]

HALF = Fraction(1, 2)


def as_int_point(p: FPoint) -> Point:
    """A Fraction point as the reader's integer pairs."""
    return ((p[0].numerator, p[0].denominator), (p[1].numerator, p[1].denominator))


def as_fraction_points(corners: tuple[Point, ...]) -> list[FPoint]:
    """The reader's integer pairs as Fraction points."""
    return [(Fraction(xp, xq), Fraction(yp, yq)) for (xp, xq), (yp, yq) in corners]


def pythagorean(m: int, k: int) -> FPoint:
    """The rational unit vector ((m^2 - k^2), 2mk) / (m^2 + k^2)."""
    h = m * m + k * k
    return (Fraction(m * m - k * k, h), Fraction(2 * m * k, h))


def square(centre: FPoint, u: FPoint, sense: int = 1, start: int = 0) -> tuple[Point, ...]:
    """A unit square with edge direction u, listed in the given sense from a corner."""
    w = (-u[1], u[0])
    p0 = (centre[0] - HALF * u[0] - HALF * w[0], centre[1] - HALF * u[1] - HALF * w[1])
    p1 = (p0[0] + u[0], p0[1] + u[1])
    p2 = (p1[0] + w[0], p1[1] + w[1])
    p3 = (p0[0] + w[0], p0[1] + w[1])
    ring = [p0, p1, p2, p3] if sense == 1 else [p0, p3, p2, p1]
    ring = ring[start:] + ring[:start]
    return tuple(as_int_point(p) for p in ring)


def translate(corners: tuple[Point, ...], v: FPoint) -> tuple[Point, ...]:
    """The corners moved by v."""
    return tuple(as_int_point((x + v[0], y + v[1])) for x, y in as_fraction_points(corners))


def centre_frame(corners: tuple[Point, ...]) -> tuple[FPoint, FPoint, FPoint]:
    """Centre (midpoint of the diagonal P0 P2) and the edge vectors u = P1 - P0, w = P3 - P0."""
    p = as_fraction_points(corners)
    c = ((p[0][0] + p[2][0]) / 2, (p[0][1] + p[2][1]) / 2)
    u = (p[1][0] - p[0][0], p[1][1] - p[0][1])
    w = (p[3][0] - p[0][0], p[3][1] - p[0][1])
    return c, u, w


def _dot(a: FPoint, b: FPoint) -> Fraction:
    return a[0] * b[0] + a[1] * b[1]


def half_width(n: FPoint, u: FPoint, w: FPoint) -> Fraction:
    """Half the width of a unit square with frame (u, w) along the unit vector n."""
    return (abs(_dot(n, u)) + abs(_dot(n, w))) / 2


def axis_terms(
    ca: FPoint, ua: FPoint, wa: FPoint, cb: FPoint, ub: FPoint, wb: FPoint
) -> list[tuple[Fraction, Fraction]]:
    """For each of the four normals: (gap at rest, |centre offset . normal|)."""
    d = (cb[0] - ca[0], cb[1] - ca[1])
    out = []
    for n, (u, w) in ((ua, (ub, wb)), (wa, (ub, wb)), (ub, (ua, wa)), (wb, (ua, wa))):
        r = abs(_dot(d, n))
        out.append((r - HALF - half_width(n, u, w), r))
    return out


def closed_margin(
    ca: FPoint, ua: FPoint, wa: FPoint, cb: FPoint, ub: FPoint, wb: FPoint
) -> Fraction:
    """The separating-axis margin from centres and half-widths."""
    return max(g for g, _ in axis_terms(ca, ua, wa, cb, ub, wb))


def closing(
    ca: FPoint, ua: FPoint, wa: FPoint, cb: FPoint, ub: FPoint, wb: FPoint, past: Fraction
) -> tuple[Fraction, Fraction, int]:
    """Move b by t (ca - cb): the t of contact, the t of margin -past, binding axes.

    On each normal the gap is r (1 - t) - 1/2 - h for 0 <= t <= 1, so the margin reaches
    0 at t* = max g / r over normals with r > 0, and -past at max (g + past) / r.
    """
    terms = axis_terms(ca, ua, wa, cb, ub, wb)
    moving = [(g, r) for g, r in terms if r > 0]
    t_contact = max(g / r for g, r in moving)
    t_past = max((g + past) / r for g, r in moving)
    binding = sum(1 for g, r in moving if g / r == t_contact)
    if not (0 < t_contact < t_past <= 1):
        raise ValueError("closing leaves the linear range")
    if any(g > -past for g, r in terms if r == 0):
        raise ValueError("a static normal would not be passed")
    return t_contact, t_past, binding


def floor_places(x: Fraction, places: int) -> str:
    """x rounded down to the given number of decimal places, printed exactly."""
    scaled = (x.numerator * 10**places) // x.denominator
    sign = "-" if scaled < 0 else ""
    digits = str(abs(scaled)).rjust(places + 1, "0")
    return f"{sign}{digits[:-places]}.{digits[-places:]}" if places else f"{sign}{digits}"


def ceil_places(x: Fraction, places: int) -> str:
    """x rounded up to the given number of decimal places, printed exactly."""
    scaled = -((-x.numerator * 10**places) // x.denominator)
    sign = "-" if scaled < 0 else ""
    digits = str(abs(scaled)).rjust(places + 1, "0")
    return f"{sign}{digits[:-places]}.{digits[-places:]}"


def sci(x: Fraction, figures: int = 15) -> str:
    """x in scientific notation, truncated toward zero to the given significant figures."""
    if x == 0:
        return "0"
    sign = "-" if x < 0 else ""
    a = abs(x)
    e = len(str(a.numerator)) - len(str(a.denominator))
    while a >= Fraction(10) ** e:
        e += 1
    while a < Fraction(10) ** (e - 1):
        e -= 1
    e -= 1
    mant = int(a * Fraction(10) ** (figures - 1 - e))
    text = str(mant)
    return f"{sign}{text[0]}.{text[1:]}e{e:+d}"
