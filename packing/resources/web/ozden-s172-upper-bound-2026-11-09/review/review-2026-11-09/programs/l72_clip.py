"""Method B (lane L72, bead think-qqyg): exact clipped areas in gmpy2.mpq.

Written from the mathematics alone; imports nothing from the squares repository and
nothing from method A.

- A quadrilateral with four edges of length 1 and turns all of one sign is a convex
  rhombus of side 1; with area 1 it is a unit square.
- A convex polygon lies in the closed box [0, S]^2 exactly when clipping it to the box
  keeps all of its area. Against each wall, clipping to the closed far side of the wall
  line gives the class: positive area means a part is past the wall, a nonempty set of
  zero area means it touches the wall, the empty set means it is clear of it.
- The intersection of two convex polygons is convex, and a convex set has positive area
  exactly when its interior is nonempty. Sutherland-Hodgman clipping of one polygon by the
  closed half-planes of the other's edges returns that intersection exactly, so its
  shoelace area decides the pair: area > 0 overlapping, a nonempty set of area 0 touching,
  and the empty set strictly apart.
"""

from gmpy2 import mpq

ZERO = mpq(0)


def corners_q(raw):
    """raw: four (xn, xd, yn, yd) integer tuples -> four mpq points."""
    return [(mpq(xn, xd), mpq(yn, yd)) for (xn, xd, yn, yd) in raw]


def twice_signed_area(poly):
    s = mpq(0)
    m = len(poly)
    for k in range(m):
        x1, y1 = poly[k]
        x2, y2 = poly[(k + 1) % m]
        s += x1 * y2 - x2 * y1
    return s


def area(poly):
    if len(poly) < 3:
        return mpq(0)
    a2 = twice_signed_area(poly)
    if a2 < 0:
        a2 = -a2
    return a2 / 2


def square(P):
    """Unit-square test. Returns (ok, orientation, reason); orientation +1 is counterclockwise."""
    edges = []
    for k in range(4):
        x1, y1 = P[k]
        x2, y2 = P[(k + 1) % 4]
        edges.append((x2 - x1, y2 - y1))
    for ex, ey in edges:
        if ex * ex + ey * ey != 1:
            return False, 0, "an edge is not of length 1"
    turns = []
    for k in range(4):
        ax, ay = edges[k]
        bx, by = edges[(k + 1) % 4]
        turns.append(ax * by - ay * bx)
    if all(t > 0 for t in turns):
        orient = 1
    elif all(t < 0 for t in turns):
        orient = -1
    else:
        return False, 0, "turns are not all of one sign"
    if twice_signed_area(P) != 2 * orient:
        return False, 0, "area is not 1"
    return True, orient, ""


def halfplanes(P, orient):
    """Closed half-planes A x + B y + C >= 0 whose intersection is the convex polygon P."""
    out = []
    m = len(P)
    for k in range(m):
        ax, ay = P[k]
        bx, by = P[(k + 1) % m]
        dx = bx - ax
        dy = by - ay
        # orient * cross((dx, dy), (x - ax, y - ay)) >= 0
        out.append((-dy * orient, dx * orient, (dy * ax - dx * ay) * orient))
    return out


def clip(poly, hp):
    """Sutherland-Hodgman: poly intersected with the closed half-plane A x + B y + C >= 0."""
    A, B, C = hp
    m = len(poly)
    if m == 0:
        return []
    vals = [A * x + B * y + C for (x, y) in poly]
    out = []
    for k in range(m):
        s = poly[k - 1]
        e = poly[k]
        ds = vals[k - 1]
        de = vals[k]
        if de >= 0:
            if ds < 0:
                t = ds / (ds - de)
                out.append((s[0] + (e[0] - s[0]) * t, s[1] + (e[1] - s[1]) * t))
            out.append(e)
        elif ds >= 0:
            t = ds / (ds - de)
            out.append((s[0] + (e[0] - s[0]) * t, s[1] + (e[1] - s[1]) * t))
    return out


def clip_all(poly, hps):
    for hp in hps:
        poly = clip(poly, hp)
        if not poly:
            return []
    return poly


def box_halfplanes(S):
    one = mpq(1)
    return [(one, ZERO, ZERO), (-one, ZERO, S), (ZERO, one, ZERO), (ZERO, -one, S)]


def outside_halfplanes(S):
    """The closed far sides of the left, right, bottom and top wall lines."""
    one = mpq(1)
    return [(-one, ZERO, ZERO), (one, ZERO, -S), (ZERO, -one, ZERO), (ZERO, one, -S)]


def inside_area(P, S):
    """Area of P clipped to the closed box [0, S]^2."""
    return area(clip_all(list(P), box_halfplanes(S)))


def wall_classes(P, S):
    """For each wall: 'outside' (area past it), 'contact' (touches it) or 'clear'."""
    out = []
    for hp in outside_halfplanes(S):
        part = clip(list(P), hp)
        if not part:
            out.append("clear")
        elif area(part) > 0:
            out.append("outside")
        else:
            out.append("contact")
    return out


def pair(Pi, hps_j):
    """(intersection area, intersection nonempty) of Pi with the polygon whose half-planes are hps_j."""
    inter = clip_all(list(Pi), hps_j)
    if not inter:
        return mpq(0), False
    return area(inter), True


def classify(a, nonempty):
    if a > 0:
        return "overlapping"
    if nonempty:
        return "touching"
    return "apart"
