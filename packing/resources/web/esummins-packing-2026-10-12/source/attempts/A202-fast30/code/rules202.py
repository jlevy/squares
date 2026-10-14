"""A202 -- the CLOSED-FORM geometric kill rules of stage 0 (fast30), each a SOUND necessary condition on a PIECE
(centre sub-rectangle x tilt sub-bin of a free unit square, or of H).  Lemmas in attempts/A202-fast30/notes/fast30.md:
  R  REACH   a square whose interior meets the open widened slot box has its centre within 1/sqrt2 (Euclid) of the
             closed box and within w_max(bin)/2 of it per axis;
  P  PINS    the open inscribed disc of radius 1/2 about the centre lies in the square's interior, so a centre at
             distance < 1/2 from a pin's certified core K (a closed square inside the pin) meets the pin;
  W  WALL    the centre is at least w_min(bin)/2 from every wall;
  C  CN-H    Lemma CN: centres of interior-disjoint unit squares are >= 1 apart (every alive piece of H);
  M  MK-H    the separating-axis bound with the relative tilt: on an axis of H or of F the projections are
             separated only if |d . a| >= 1/2 + w(theta_F - theta_H)/2; folded-mod-90 angular gaps;
  L  CHORD   Lemma LINE-1 (open chords): pins' + H's + the piece's min open chord on a guard line <= s.
Rects are (x0, x1, y0, y1); bins are multibox.Bin (exact endpoint cos/sin, wmin/wmax).  The disc / box rules are
evaluated in floats from outward-rounded rects with an explicit margin EPS; the chord rule is exact (guardlines_v5).
"""
import math
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
for _p in (os.path.join(ROOT, "attempts", "A198-fastprop", "code"), os.path.join(ROOT, "attempts", "A200-k516-quick", "code")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import fastprop as FP                                          # noqa: E402  READ-ONLY (A198)

MB, GV = FP.MB, FP.GV
EPS = 1e-9
SQ2H = math.sqrt(0.5)


def fr(r):
    return tuple(float(v) for v in r)


def rect_gap(a, b):
    """(dx, dy) >= 0: the per-axis gap between two closed rects (0 when they overlap on that axis)."""
    return (max(0.0, a[0] - b[1], b[0] - a[1]), max(0.0, a[2] - b[3], b[2] - a[3]))


def rect_maxdist2(a, b):
    """max squared Euclidean distance between a point of a and a point of b (attained at corners)."""
    dx = max(abs(a[1] - b[0]), abs(b[1] - a[0]))
    dy = max(abs(a[3] - b[2]), abs(b[3] - a[2]))
    return dx * dx + dy * dy


def rect_maxlinf(a, b):
    return max(abs(a[1] - b[0]), abs(b[1] - a[0]), abs(a[3] - b[2]), abs(b[3] - a[2]))


# ----------------------------------------------------------------------------- R, P, W
def reach_dead(rect, bn, wbox):
    """R: no pose of the piece meets the open widened box wbox."""
    dx, dy = rect_gap(rect, wbox)
    if dx * dx + dy * dy >= 0.5 + EPS:
        return True
    h = float(bn.wmax) / 2
    return dx >= h + EPS or dy >= h + EPS


def pin_dead(rect, cores):
    """P: every centre of the rect is at distance < 1/2 from some pin core (cores: (kx0, kx1, ky0, ky1) closed)."""
    for K in cores:
        # max over the rect's corners of dist(corner, K)^2 < 1/4
        worst = 0.0
        for x in (rect[0], rect[1]):
            for y in (rect[2], rect[3]):
                dx = max(0.0, K[0] - x, x - K[1])
                dy = max(0.0, K[2] - y, y - K[3])
                worst = max(worst, dx * dx + dy * dy)
        if worst < 0.25 - EPS:
            return True
    return False


def wall_dead(rect, bn, s):
    """W: every centre of the piece is closer than w_min/2 to a wall."""
    h = float(bn.wmin) / 2
    return rect[1] < h - EPS or rect[3] < h - EPS or rect[0] > s - h + EPS or rect[2] > s - h + EPS


# ----------------------------------------------------------------------------- C, M
def cn_dead_pair(rect1, rect2):
    """C: every centre pair is < 1 apart: no interior-disjoint pair (Lemma CN)."""
    return rect_maxdist2(rect1, rect2) < 1.0 - EPS


def _dir_interval(D):
    """angular interval [a0, a1] (degrees, width < 180) of the directions of the vectors of the closed rect D, or
    None when D contains the origin (every direction)."""
    x0, x1, y0, y1 = D
    if x0 <= 0 <= x1 and y0 <= 0 <= y1:
        return None
    if x1 < 0 or (x0 <= 0 <= x1 and y1 < 0):
        x0, x1, y0, y1 = -x1, -x0, -y1, -y0
    cs = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    if x0 > 0:
        angs = [math.degrees(math.atan2(y, x)) for x, y in cs]          # in (-90, 90)
    else:
        angs = [math.degrees(math.atan2(y, x)) for x, y in cs]          # y0 > 0 here: in (0, 180)
    return (min(angs), max(angs))


def gap90(I, J):
    """min over a in I, b in J of the distance from a - b to the nearest multiple of 90 (degrees), I, J intervals."""
    if I is None or J is None:
        return 0.0
    a0, a1 = I
    b0, b1 = J
    best = 45.0
    for k in range(-6, 7):
        c0, c1 = b0 + 90 * k, b1 + 90 * k
        if c0 <= a1 and a0 <= c1:
            return 0.0
        best = min(best, abs(a0 - c1), abs(c0 - a1))
    return min(best, 45.0)


def wmin_deg(lo, hi):
    """min of |cos| + |sin| over a degree interval (period 90; = 1 at multiples of 90, concave between)."""
    if hi - lo >= 90:
        return 1.0
    k0 = math.ceil(lo / 90.0)
    if 90 * k0 <= hi:
        return 1.0
    return min(abs(math.cos(math.radians(a))) + abs(math.sin(math.radians(a))) for a in (lo, hi))


def mk_dead(rect1, bin1, rect2, bin2):
    """M: no pose pair (F in piece 1, G in piece 2) is interior-disjoint by the separating-axis bound with the
    relative tilt.  bins = (deg_lo, deg_hi)."""
    D = (rect1[0] - rect2[1], rect1[1] - rect2[0], rect1[2] - rect2[3], rect1[3] - rect2[2])
    dmax = math.sqrt(max((x * x + y * y) for x in (D[0], D[1]) for y in (D[2], D[3])))
    lo, hi = bin1[0] - bin2[1], bin1[1] - bin2[0]
    r_lo = 0.5 + wmin_deg(lo, hi) / 2
    if dmax < r_lo - EPS:
        return True                                            # CN-like: no axis can separate
    I = _dir_interval(D)
    u1 = dmax * math.cos(math.radians(gap90(I, bin1)))
    u2 = dmax * math.cos(math.radians(gap90(I, bin2)))
    return u1 < r_lo - EPS and u2 < r_lo - EPS


def bin_deg(bn):
    return (MB.deg_of_t(bn.t0), MB.deg_of_t(bn.t1))


# ----------------------------------------------------------------------------- L (exact)
def piece_chords(rect_fr, bn, lines, near=None):
    """{line: exact min OPEN chord} for the lines within w_max/2 of the rect (others: 0, omitted)."""
    out = {}
    h = bn.wmax / 2
    for (o, off) in lines:
        lo, hi = (rect_fr[2], rect_fr[3]) if o == "h" else (rect_fr[0], rect_fr[1])
        if off < lo - h or off > hi + h:
            continue
        c = GV.minchord(FP.HALF, bn.t0, bn.t1, rect_fr[0], rect_fr[1], rect_fr[2], rect_fr[3], o, off)
        if c > 0:
            out[(o, off)] = c
    return out


def chord_dead(ch, base, s):
    """L: the fixed squares' chords plus this piece's exceed s on some line -> (line) or None."""
    for L, c in ch.items():
        if base.get(L, 0) + c > s:
            return L
    return None


# ----------------------------------------------------------------------------- the meet test (H forcing)
def may_meet(rect, bn, wbox):
    """False only when NO pose of the piece can meet the open box: the square lies in the l-inf ball of radius
    w_max/2 about its centre."""
    h = float(bn.wmax) / 2
    return rect[0] - h < wbox[1] - EPS and rect[1] + h > wbox[0] + EPS and rect[2] - h < wbox[3] - EPS and rect[3] + h > wbox[2] + EPS
