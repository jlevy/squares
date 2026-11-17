"""Method A: separating axes in exact rationals (`fractions.Fraction`).

L96 review program. Imports nothing from this repository or the source.

A square is (x, y, t): centre (x, y), cos = (1 - t^2)/(1 + t^2), sin = 2t/(1 + t^2), edge
directions u = (cos, sin) and v = (-sin, cos). Since cos^2 + sin^2 = 1 exactly for every
rational t, each is a unit square; `unit_ok` still checks the identity.

Containment. The square's x- and y-extents are the centre +- h with h = (|cos| + |sin|)/2,
exactly. It lies in [0, L]^2 iff all four clearances are >= 0; a clearance of 0 is a
contact.

Pairs. The margin of a pair is max over the four edge normals a of |a.d| - (h_i(a) +
h_j(a)), with h_k(a) = (|a.u_k| + |a.v_k|)/2: positive is apart, 0 is contact, negative
is overlapping interiors (the separating axis theorem for two convex polygons).
A pair whose exact bounding boxes are strictly apart in x or in y is decided `clear`
without the margin, by that axis-aligned separating line; the sweep below visits every
other pair, so every pair is decided.
"""

from fractions import Fraction as F

HALF = F(1, 2)


def to_frac(pair):
    return F(pair[0], pair[1])


def square(x, y, t):
    d = 1 + t * t
    return (x, y, (1 - t * t) / d, 2 * t / d)


def unit_ok(sq):
    return sq[2] * sq[2] + sq[3] * sq[3] == 1


def h_of(sq):
    return (abs(sq[2]) + abs(sq[3])) / 2


def support(ax, ay, sq):
    c, s = sq[2], sq[3]
    return (abs(ax * c + ay * s) + abs(-ax * s + ay * c)) / 2


def margin(si, sj):
    """Exact margin of a pair and the index (0..3) of the axis that attains it."""
    dx, dy = sj[0] - si[0], sj[1] - si[1]
    axes = (
        (si[2], si[3], 0),
        (-si[3], si[2], 0),
        (sj[2], sj[3], 1),
        (-sj[3], sj[2], 1),
    )
    best, arg = None, None
    for k, (ax, ay, own) in enumerate(axes):
        proj = abs(ax * dx + ay * dy)
        other = sj if own == 0 else si
        g = proj - HALF - support(ax, ay, other)
        if best is None or g > best:
            best, arg = g, k
    return best, arg


def classify(m):
    return "clear" if m > 0 else ("contact" if m == 0 else "overlap")


def walls(sq, side):
    h = h_of(sq)
    return {
        "left": sq[0] - h,
        "bottom": sq[1] - h,
        "right": side - (sq[0] + h),
        "top": side - (sq[1] + h),
    }


def decide(side_pair, triples):
    """Decide a read certificate. Returns a dict with exact Fractions."""
    side = to_frac(side_pair)
    sqs = [square(to_frac(a), to_frac(b), to_frac(c)) for a, b, c in triples]
    n = len(sqs)
    bad_unit = [i + 1 for i, s in enumerate(sqs) if not unit_ok(s)]
    clear = {}
    for i, s in enumerate(sqs):
        clear[i + 1] = walls(s, side)
    hs = [h_of(s) for s in sqs]
    box = [(s[0] - h, s[0] + h, s[1] - h, s[1] + h) for s, h in zip(sqs, hs)]
    order = sorted(range(n), key=lambda k: box[k][0])
    margins = {}
    pruned_x = 0
    pruned_y = 0
    least_x_gap = None
    least_y_gap = None
    for a in range(n):
        i = order[a]
        xmax_i = box[i][1]
        b = a + 1
        while b < n and box[order[b]][0] <= xmax_i:
            j = order[b]
            gy = max(box[j][2] - box[i][3], box[i][2] - box[j][3])
            if gy > 0:
                pruned_y += 1
                if least_y_gap is None or gy < least_y_gap:
                    least_y_gap = gy
            else:
                key = (min(i, j) + 1, max(i, j) + 1)
                margins[key] = margin(sqs[key[0] - 1], sqs[key[1] - 1])
            b += 1
        pruned_x += n - b
        if b < n:
            gx = box[order[b]][0] - xmax_i
            if least_x_gap is None or gx < least_x_gap:
                least_x_gap = gx
    total = n * (n - 1) // 2
    assert pruned_x + pruned_y + len(margins) == total
    return {
        "n": n,
        "side": side,
        "squares": sqs,
        "bad_unit": bad_unit,
        "clearances": clear,
        "margins": margins,
        "pairs_total": total,
        "pairs_decided_by_x_line": pruned_x,
        "pairs_decided_by_y_line": pruned_y,
        "pairs_decided_by_margin": len(margins),
        "least_x_line_gap": least_x_gap,
        "least_y_line_gap": least_y_gap,
    }
