"""Clean-room exact checker for unit-square packing certificates (review bold-ritchie-rv-daniel).

Reads a certificate of the form

    # comment lines ...
    n S
    x y t        (n lines; integers or integer fractions a/b)

and decides, in exact rational arithmetic, that the n closed unit squares with centre (x, y)
and edge directions u = (c, s), v = (-s, c), c = (1 - t^2)/(1 + t^2), s = 2t/(1 + t^2), lie in
[0, S]^2 and have pairwise disjoint interiors.

Two methods, sharing only the reader and the frame construction:

  A. separating axes: corners in the box; for every pair (no distance filter), the four
     edge normals of the two squares, with the projected gap computed in closed form.
  B. clipped areas: every square clipped to the box keeps area 1; every pair whose centres are
     within sqrt(2) (squared distance <= 2) is clipped (Sutherland-Hodgman) and must have area
     0; a pair with squared centre distance > 2 is disjoint because the circumscribed discs
     (radius sqrt(2)/2 each) are disjoint.

Written from the mathematics alone; its author read no checker of the source or of the
repository. Prints a JSON receipt.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from fractions import Fraction as F

TOKEN = re.compile(r"^-?[0-9]+(/[0-9]+)?$")
HALF = F(1, 2)


def parse_token(tok: str) -> F:
    if not TOKEN.match(tok):
        raise ValueError(f"refused token {tok!r}")
    if "/" in tok:
        a, b = tok.split("/")
        if int(b) <= 0:
            raise ValueError(f"refused denominator in {tok!r}")
        return F(int(a), int(b))
    return F(int(tok))


def read_cert(path: str) -> tuple[int, F, list[tuple[F, F, F]], list[str]]:
    comments: list[str] = []
    rows: list[list[str]] = []
    with open(path, encoding="ascii") as fh:
        for line in fh:
            s = line.strip()
            if not s:
                continue
            if s.startswith("#"):
                if rows:
                    raise ValueError("comment after data refused")
                comments.append(s)
                continue
            rows.append(s.split())
    head = rows[0]
    if len(head) != 2 or not re.match(r"^[0-9]+$", head[0]):
        raise ValueError(f"bad header {head}")
    n = int(head[0])
    side = parse_token(head[1])
    body = rows[1:]
    if len(body) != n:
        raise ValueError(f"header says {n} squares, file has {len(body)} rows")
    sq = []
    for r in body:
        if len(r) != 3:
            raise ValueError(f"row with {len(r)} tokens refused")
        sq.append((parse_token(r[0]), parse_token(r[1]), parse_token(r[2])))
    return n, side, sq, comments


def frame(t: F) -> tuple[F, F]:
    d = 1 + t * t
    c = (1 - t * t) / d
    s = 2 * t / d
    assert c * c + s * s == 1
    return c, s


def corners(x: F, y: F, c: F, s: F) -> list[tuple[F, F]]:
    # counterclockwise: (+,+), (-,+), (-,-), (+,-) in (alpha, beta) with u=(c,s), v=(-s,c)
    out = []
    for a, b in ((HALF, HALF), (-HALF, HALF), (-HALF, -HALF), (HALF, -HALF)):
        out.append((x + a * c - b * s, y + a * s + b * c))
    return out


def sat_gap(p, q) -> F:
    """Largest projected gap over the four edge normals of squares p and q.

    p = (x, y, c, s). For axis w (unit), the projection of a unit square with frame (u, v)
    is centre.w +- (|u.w| + |v.w|)/2. Along an axis of p itself, p's half-width is 1/2.
    Gap >= 0 means the axis weakly separates (interiors disjoint).
    """
    best = None
    for axis_owner, other in ((p, q), (q, p)):
        ax, ay, ac, as_ = axis_owner
        bx, by, bc, bs = other
        dx, dy = bx - ax, by - ay
        for wx, wy in ((ac, as_), (-as_, ac)):
            centre = dx * wx + dy * wy
            ub = abs(bc * wx + bs * wy)
            vb = abs(-bs * wx + bc * wy)
            gap = abs(centre) - HALF - (ub + vb) / 2
            if best is None or gap > best:
                best = gap
    assert best is not None
    return best


def clip(poly, a: F, b: F, cc: F):
    """Keep the part of poly with a*x + b*y <= cc (Sutherland-Hodgman, exact)."""
    out = []
    m = len(poly)
    for i in range(m):
        P = poly[i]
        Q = poly[(i + 1) % m]
        fp = a * P[0] + b * P[1] - cc
        fq = a * Q[0] + b * Q[1] - cc
        if fp <= 0:
            out.append(P)
        if (fp < 0 < fq) or (fq < 0 < fp):
            r = fp / (fp - fq)
            out.append((P[0] + r * (Q[0] - P[0]), P[1] + r * (Q[1] - P[1])))
    return out


def area(poly) -> F:
    m = len(poly)
    if m < 3:
        return F(0)
    acc = F(0)
    for i in range(m):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % m]
        acc += x1 * y2 - x2 * y1
    return abs(acc) / 2


def halfplanes(sq):
    """The four half-planes w.p <= w.centre + 1/2 whose intersection is the square."""
    x, y, c, s = sq
    hp = []
    for wx, wy in ((c, s), (-s, c), (-c, -s), (s, -c)):
        hp.append((wx, wy, wx * x + wy * y + HALF))
    return hp


def check(path: str, method: str = "both") -> dict:
    t0 = time.process_time()
    raw = open(path, "rb").read()
    n, side, rows, comments = read_cert(path)
    sq = []
    tilted = 0
    for x, y, t in rows:
        c, s = frame(t)
        if t != 0:
            tilted += 1
        sq.append((x, y, c, s))
    corner_list = [corners(*q) for q in sq]
    rec: dict = {
        "file": path,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "comment": comments,
        "n": n,
        "side": f"{side.numerator}/{side.denominator}",
        "side_decimal_40": decimal_str(side, 40),
        "tilted": tilted,
    }
    # --- containment (method A: corners) ---
    near = []
    far = []
    for i, cs in enumerate(corner_list):
        mnx = min(p[0] for p in cs)
        mny = min(p[1] for p in cs)
        mxx = max(p[0] for p in cs)
        mxy = max(p[1] for p in cs)
        near.append((min(mnx, mny), i))
        far.append((min(side - mxx, side - mxy), i))
    min_near = min(near)
    min_far = min(far)
    rec["A_walls_ok"] = min_near[0] >= 0 and min_far[0] >= 0
    rec["least_near_wall_clearance"] = [float(min_near[0]), min_near[1]]
    rec["least_near_wall_clearance_exact"] = str(min_near[0])
    rec["least_far_wall_clearance"] = [float(min_far[0]), min_far[1]]
    rec["least_far_wall_clearance_exact"] = str(min_far[0])
    # extent of the packing
    ext = max(max(max(p[0] for p in cs), max(p[1] for p in cs)) for cs in corner_list)
    rec["extent_exact"] = str(ext)
    rec["side_minus_extent"] = float(side - ext)
    t1 = time.process_time()
    # --- pairs, method A: all pairs, no filter ---
    pairs = 0
    bad_a = []
    least = None
    near_contacts = 0
    gaps_small = []
    if method in ("both", "A"):
        for i in range(n):
            for j in range(i + 1, n):
                pairs += 1
                g = sat_gap(sq[i], sq[j])
                if g < 0:
                    bad_a.append((i, j, float(g)))
                if least is None or g < least[0]:
                    least = (g, i, j)
                if g < F(1, 10**15):
                    near_contacts += 1
                    gaps_small.append((i, j))
        rec["A_pairs"] = pairs
        rec["A_pairs_overlapping"] = len(bad_a)
        rec["A_first_overlaps"] = bad_a[:5]
        rec["A_valid"] = rec["A_walls_ok"] and not bad_a
        assert least is not None
        rec["least_pair_gap"] = [float(least[0]), least[1], least[2]]
        rec["least_pair_gap_exact"] = str(least[0])
        rec["pairs_within_1e-15"] = near_contacts
    t2 = time.process_time()
    rec["A_cpu_s"] = round(t2 - t0, 2)
    # --- method B: clipped areas ---
    if method in ("both", "B"):
        box = [(F(0), F(0)), (side, F(0)), (side, side), (F(0), side)]
        box_hp = [(F(-1), F(0), F(0)), (F(0), F(-1), F(0)), (F(1), F(0), side), (F(0), F(1), side)]
        walls_bad = []
        for i, cs in enumerate(corner_list):
            poly = list(cs)
            for a, b, cc in box_hp:
                poly = clip(poly, a, b, cc)
            if area(poly) != 1:
                walls_bad.append(i)
        del box
        clipped = 0
        far_pairs = 0
        bad_b = []
        for i in range(n):
            xi, yi = sq[i][0], sq[i][1]
            for j in range(i + 1, n):
                dx = sq[j][0] - xi
                dy = sq[j][1] - yi
                if dx * dx + dy * dy > 2:
                    far_pairs += 1
                    continue
                clipped += 1
                poly = list(corner_list[i])
                for a, b, cc in halfplanes(sq[j]):
                    poly = clip(poly, a, b, cc)
                    if not poly:
                        break
                ar = area(poly)
                if ar != 0:
                    bad_b.append((i, j, float(ar)))
        rec["B_walls_bad"] = walls_bad[:5]
        rec["B_pairs_clipped"] = clipped
        rec["B_pairs_far_by_discs"] = far_pairs
        rec["B_pairs_positive_area"] = len(bad_b)
        rec["B_first_overlaps"] = bad_b[:5]
        rec["B_valid"] = not walls_bad and not bad_b
    rec["B_cpu_s"] = round(time.process_time() - t2, 2)
    rec["total_cpu_s"] = round(time.process_time() - t0, 2)
    del t1
    return rec


def decimal_str(q: F, places: int) -> str:
    sign = "-" if q < 0 else ""
    q = abs(q)
    ip = q.numerator // q.denominator
    frac = q - ip
    digits = (frac.numerator * 10**places) // frac.denominator
    return f"{sign}{ip}.{digits:0{places}d}"


def round_up(q: F, places: int) -> str:
    scaled = q * 10**places
    up = -((-scaled.numerator) // scaled.denominator)
    ip, fp = divmod(up, 10**places)
    return f"{ip}.{fp:0{places}d}"


if __name__ == "__main__":
    method = "both"
    args = sys.argv[1:]
    if args and args[0] in ("--A", "--B"):
        method = args[0][2:]
        args = args[1:]
    for p in args:
        r = check(p, method)
        side = F(r["side"])
        r["print_up_12"] = round_up(side, 12)
        print(json.dumps(r, indent=1))
        sys.stdout.flush()
