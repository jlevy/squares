"""Clean-room exact checker for an `x y t` unit-square packing certificate.

Written for the stage 4 mathematical review of jlevy/squares issue 806 (Evan Daniel,
s(182) <= 13.970916436215). Its authors read the mathematics (the separating axis
theorem for convex polygons and exact convex polygon clipping) and the certificate's
one-line format statement, and nothing of the producer's code (verify_cert.py,
verify_cert2.py, exactsolve.py) or of this repository's maintained exact routes.

Certificate format, as its first line states: after comment lines starting with `#`,
a line `n S` (or the two lines `n N` and `s S`), then n lines `x y t`, each a centre
and the tangent of half the rotation angle, every token an exact integer or integer
fraction. A square's frame is (c, s) = ((1-t^2)/(1+t^2), 2t/(1+t^2)), so c^2 + s^2 = 1
exactly, and its corners are (x, y) + u (c, s) + v (-s, c) for u, v in {-1/2, 1/2}:
the rotation by the angle theta = 2 atan t, counterclockwise for t > 0 in a frame
whose x axis points right and y axis up. The container is [0, S] x [0, S].

Two methods decide the same statement, sharing only the parser and the corner
construction above:

* Method SAT. Containment: every corner lies in [0, S]^2. Pairs: for each of the
  four edge normals of the two squares, which are exact unit vectors, the two
  projection intervals overlap in at most one point. For convex polygons this holds
  for some edge normal exactly when their interiors are disjoint.
* Method AREA. Containment: the square clipped to the container keeps its whole
  area (exactly 1). Pairs: one square clipped to the other (Sutherland-Hodgman over Q)
  has area exactly 0. For closed convex bodies, zero intersection area is the same as
  disjoint interiors.

Touching is allowed by both. All arithmetic is in `fractions.Fraction`; no float
enters a decision.

Run with the project interpreter in isolated mode:

    python3 -I exact_check.py check CERT [--json OUT]
    python3 -I exact_check.py controls CERT [--json OUT]

`check` decides the certificate by both methods over every pair and wall, reports the
side, its 12-place upward print, the least slacks and the rotation-sense test.
`controls` builds the sharp mutations described in `controls()` and decides each by
both methods.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from fractions import Fraction
from itertools import combinations

TOKEN = re.compile(r"^-?[0-9]+(?:/[0-9]+)?$")
HALF = Fraction(1, 2)
TINY = Fraction(1, 10**30)
CONTACT = Fraction(1, 10**15)


def rational(token: str) -> Fraction:
    """Read one exact token; refuse decimals, exponents and anything else."""
    if not TOKEN.match(token):
        raise ValueError(f"not an exact integer or integer fraction: {token[:60]!r}")
    num, _, den = token.partition("/")
    return Fraction(int(num), int(den) if den else 1)


def read_certificate(path: str) -> tuple[int, Fraction, list[tuple[Fraction, Fraction, Fraction]], str, int]:
    raw = open(path, "rb").read()
    rows = []
    for line in raw.decode("ascii").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            rows.append(stripped.split())
    if rows[0][0] == "n" and len(rows[0]) == 2:
        n = int(rows[0][1])
        if rows[1][0] != "s" or len(rows[1]) != 2:
            raise ValueError("an `n N` line must be followed by an `s S` line")
        side, body = rational(rows[1][1]), rows[2:]
    else:
        if len(rows[0]) != 2:
            raise ValueError("the header must be `n S`")
        n, side, body = int(rows[0][0]), rational(rows[0][1]), rows[1:]
    if len(body) != n:
        raise ValueError(f"header says {n} squares, body has {len(body)}")
    poses = []
    for row in body:
        if len(row) != 3:
            raise ValueError(f"a pose line has {len(row)} tokens, not 3")
        poses.append((rational(row[0]), rational(row[1]), rational(row[2])))
    return n, side, poses, hashlib.sha256(raw).hexdigest(), len(raw)


def frame(t: Fraction, mirror: bool = False) -> tuple[Fraction, Fraction]:
    d = 1 + t * t
    c, s = (1 - t * t) / d, 2 * t / d
    return (c, -s) if mirror else (c, s)


class Square:
    """A square of side `size` centred at (x, y) with unit frame (c, s)."""

    __slots__ = ("c", "s", "size", "verts", "x", "y")

    def __init__(self, x: Fraction, y: Fraction, c: Fraction, s: Fraction, size: Fraction = Fraction(1)) -> None:
        if c * c + s * s != 1:
            raise ValueError("frame is not an exact unit vector")
        self.x, self.y, self.c, self.s, self.size = x, y, c, s, size
        h = size / 2
        # Counterclockwise: (u, v) = (-h, -h), (h, -h), (h, h), (-h, h).
        self.verts = [(x + c * u - s * v, y + s * u + c * v) for (u, v) in ((-h, -h), (h, -h), (h, h), (-h, h))]

    def axes(self) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]]:
        return (self.c, self.s), (-self.s, self.c)


def squares_from(poses: list[tuple[Fraction, Fraction, Fraction]], mirror: bool = False) -> list[Square]:
    out = []
    for x, y, t in poses:
        c, s = frame(t, mirror)
        out.append(Square(x, y, c, s))
    return out


# ---------------------------------------------------------------- method SAT


def sat_gap(a: Square, b: Square) -> tuple[Fraction, int, int]:
    """Largest signed slab gap over the four edge normals (exact, unit axes).

    Returns (gap, axis index 0..3, side) where side = +1 means b lies on the positive
    side of a along that axis. gap >= 0 exactly when the interiors are disjoint.
    """
    best: tuple[Fraction, int, int] | None = None
    for k, (ux, uy) in enumerate(a.axes() + b.axes()):
        pa = [ux * px + uy * py for (px, py) in a.verts]
        pb = [ux * px + uy * py for (px, py) in b.verts]
        forward, backward = min(pb) - max(pa), min(pa) - max(pb)
        gap, side = (forward, 1) if forward >= backward else (backward, -1)
        if best is None or gap > best[0]:
            best = (gap, k, side)
    assert best is not None
    return best


def axis_of(a: Square, b: Square, k: int) -> tuple[Fraction, Fraction]:
    return (a.axes() + b.axes())[k]


def wall_slacks(sq: Square, side: Fraction) -> tuple[Fraction, Fraction]:
    """(least distance to the left/bottom walls, least distance to the right/top walls)."""
    low = min(min(px, py) for (px, py) in sq.verts)
    high = min(min(side - px, side - py) for (px, py) in sq.verts)
    return low, high


# ---------------------------------------------------------------- method AREA


def clip(poly: list[tuple[Fraction, Fraction]], p: tuple[Fraction, Fraction], q: tuple[Fraction, Fraction]) -> list[tuple[Fraction, Fraction]]:
    """Keep the part of convex `poly` left of (or on) the directed line p -> q."""
    ex, ey = q[0] - p[0], q[1] - p[1]

    def side(z: tuple[Fraction, Fraction]) -> Fraction:
        return ex * (z[1] - p[1]) - ey * (z[0] - p[0])

    out: list[tuple[Fraction, Fraction]] = []
    for i, cur in enumerate(poly):
        prev = poly[i - 1]
        dc, dp = side(cur), side(prev)
        if dc >= 0:
            if dp < 0:
                r = dp / (dp - dc)
                out.append((prev[0] + r * (cur[0] - prev[0]), prev[1] + r * (cur[1] - prev[1])))
            out.append(cur)
        elif dp > 0:
            r = dp / (dp - dc)
            out.append((prev[0] + r * (cur[0] - prev[0]), prev[1] + r * (cur[1] - prev[1])))
    return out


def area(poly: list[tuple[Fraction, Fraction]]) -> Fraction:
    if len(poly) < 3:
        return Fraction(0)
    twice = sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))
    return abs(twice) / 2


def clipped_area(subject: list[tuple[Fraction, Fraction]], window: list[tuple[Fraction, Fraction]]) -> Fraction:
    """Exact area of subject ∩ window for convex polygons, `window` counterclockwise."""
    poly = list(subject)
    for i in range(len(window)):
        poly = clip(poly, window[i], window[(i + 1) % len(window)])
        if not poly:
            return Fraction(0)
    return area(poly)


# ---------------------------------------------------------------- deciding


def decide(squares: list[Square], side: Fraction, *, methods: tuple[str, ...] = ("sat", "area"), keep: int = 8) -> dict:
    """Decide a packing by each method over every wall and every pair."""
    n = len(squares)
    box = [(Fraction(0), Fraction(0)), (side, Fraction(0)), (side, side), (Fraction(0), side)]
    report: dict = {"n": n, "pairs": n * (n - 1) // 2}
    if "sat" in methods:
        t0 = time.process_time()
        wall_bad, pair_bad = [], []
        low_best = high_best = pair_best = None
        contacts_pairs = contacts_walls = 0
        for i, sq in enumerate(squares):
            low, high = wall_slacks(sq, side)
            if low < 0 or high < 0:
                wall_bad.append(i)
            contacts_walls += sum(1 for v in (min(px for px, _ in sq.verts), min(py for _, py in sq.verts), side - max(px for px, _ in sq.verts), side - max(py for _, py in sq.verts)) if v < CONTACT)
            if low_best is None or low < low_best[0]:
                low_best = (low, i)
            if high_best is None or high < high_best[0]:
                high_best = (high, i)
        for i, j in combinations(range(n), 2):
            gap, k, sgn = sat_gap(squares[i], squares[j])
            if gap < 0:
                pair_bad.append((i, j, gap))
            if gap < CONTACT:
                contacts_pairs += 1
            if pair_best is None or gap < pair_best[0]:
                pair_best = (gap, i, j, k, sgn)
        assert low_best is not None and high_best is not None and pair_best is not None
        report["sat"] = {
            "valid": not wall_bad and not pair_bad,
            "wall_violations": len(wall_bad),
            "pair_violations": len(pair_bad),
            "first_wall_violations": wall_bad[:keep],
            "first_pair_violations": [[i, j, float(g)] for (i, j, g) in pair_bad[:keep]],
            "least_low_wall_slack": [str(low_best[0]), float(low_best[0]), low_best[1]],
            "least_high_wall_slack": [str(high_best[0]), float(high_best[0]), high_best[1]],
            "least_pair_gap": [str(pair_best[0]), float(pair_best[0]), pair_best[1], pair_best[2], pair_best[3], pair_best[4]],
            "pairs_below_1e-15": contacts_pairs,
            "walls_below_1e-15": contacts_walls,
            "cpu_seconds": round(time.process_time() - t0, 2),
        }
    if "area" in methods:
        t0 = time.process_time()
        wall_bad, pair_bad = [], []
        for i, sq in enumerate(squares):
            own = area(sq.verts)
            if clipped_area(sq.verts, box) != own:
                wall_bad.append(i)
        for i, j in combinations(range(n), 2):
            a = clipped_area(squares[i].verts, squares[j].verts)
            if a != 0:
                pair_bad.append((i, j, a))
        report["area"] = {
            "valid": not wall_bad and not pair_bad,
            "wall_violations": len(wall_bad),
            "pair_violations": len(pair_bad),
            "first_wall_violations": wall_bad[:keep],
            "first_pair_violations": [[i, j, float(a)] for (i, j, a) in pair_bad[:keep]],
            "cpu_seconds": round(time.process_time() - t0, 2),
        }
    return report


def ceil_places(q: Fraction, places: int) -> str:
    scale = 10**places
    up = -((-q.numerator * scale) // q.denominator)
    return f"{up // scale}.{up % scale:0{places}d}"


def floor_places(q: Fraction, places: int) -> str:
    scale = 10**places
    down = (q.numerator * scale) // q.denominator
    return f"{down // scale}.{down % scale:0{places}d}"


def check(path: str) -> dict:
    n, side, poses, digest, size = read_certificate(path)
    squares = squares_from(poses)
    print(f"certificate {path}\n  sha256 {digest}  {size} bytes  n = {n}")
    up12 = ceil_places(side, 12)
    print(f"  side S = {side}\n       = {floor_places(side, 40)}... (decimal, truncated at 40 places)")
    print(f"  12-place upward print {up12}; S <= print: {side <= Fraction(up12)}; print - 1e-12 < S: {Fraction(up12) - Fraction(1, 10**12) < side}")
    tilted = sum(1 for (_, _, t) in poses if t != 0)
    print(f"  tilted squares (t != 0): {tilted}")
    result = decide(squares, side)
    for m in ("sat", "area"):
        r = result[m]
        print(f"  method {m}: valid={r['valid']} wall_violations={r['wall_violations']} pair_violations={r['pair_violations']} cpu={r['cpu_seconds']}s")
    s = result["sat"]
    print(f"  least low-wall slack  {s['least_low_wall_slack'][1]:.6e} (square {s['least_low_wall_slack'][2]})")
    print(f"  least high-wall slack {s['least_high_wall_slack'][1]:.6e} (square {s['least_high_wall_slack'][2]})")
    print(f"  least pair gap        {s['least_pair_gap'][1]:.6e} (pair {s['least_pair_gap'][2]}, {s['least_pair_gap'][3]})")
    print(f"  pairs with gap < 1e-15: {s['pairs_below_1e-15']}; square-wall incidences with slack < 1e-15: {s['walls_below_1e-15']}")
    mirrored = decide(squares_from(poses, mirror=True), side, methods=("sat",))
    print(f"  rotation sense reversed (s -> -s, same centres): SAT valid={mirrored['sat']['valid']} pair_violations={mirrored['sat']['pair_violations']} wall_violations={mirrored['sat']['wall_violations']}")
    return {
        "certificate": path,
        "sha256": digest,
        "bytes": size,
        "n": n,
        "side": str(side),
        "side_decimal_40_truncated": floor_places(side, 40),
        "print_12_up": up12,
        "tilted": tilted,
        "decision": result,
        "rotation_sense_reversed": mirrored["sat"],
    }


# ---------------------------------------------------------------- controls


def extent(squares: list[Square]) -> Fraction:
    return max(max(px, py) for sq in squares for (px, py) in sq.verts)


def low_extent(squares: list[Square]) -> tuple[Fraction, Fraction]:
    return min(px for sq in squares for (px, _) in sq.verts), min(py for sq in squares for (_, py) in sq.verts)


def moved(sq: Square, dx: Fraction, dy: Fraction) -> Square:
    return Square(sq.x + dx, sq.y + dy, sq.c, sq.s, sq.size)


def scaled(sq: Square, size: Fraction) -> Square:
    return Square(sq.x, sq.y, sq.c, sq.s, size)


def critical_size(squares: list[Square], i: int, side: Fraction, *, walls: bool = True) -> tuple[Fraction, str]:
    """Largest size of square i, about its centre, at which it still fits (exact).

    With walls=False only its pairs limit it, which finds a square to enlarge past a
    neighbour rather than past a wall.
    """
    sq = squares[i]
    best: tuple[Fraction, str] | None = None
    # Walls: a corner's offset from the centre scales with the size.
    for (px, py) in sq.verts if walls else []:
        ox, oy = px - sq.x, py - sq.y
        for off, room in ((ox, sq.x), (oy, sq.y), (-ox, side - sq.x), (-oy, side - sq.y)):
            if off < 0:  # this corner moves toward the wall at distance `room` from the centre
                cand = room / (-off) * sq.size
                if best is None or cand < best[0]:
                    best = (cand, "wall")
    # Pairs: on each fixed axis the half-width grows linearly with the size.
    for j, other in enumerate(squares):
        if j == i:
            continue
        pair_best = None
        for (ux, uy) in sq.axes() + other.axes():
            half = (abs(ux * sq.c + uy * sq.s) + abs(-ux * sq.s + uy * sq.c)) / 2  # per unit size
            centre = ux * sq.x + uy * sq.y
            po = [ux * px + uy * py for (px, py) in other.verts]
            room = max(min(po) - centre, centre - max(po))  # distance from the centre's projection to other's interval
            if room >= 0:
                cand = room / half
                if pair_best is None or cand > pair_best:
                    pair_best = cand
        if pair_best is not None and (best is None or pair_best < best[0]):
            best = (pair_best, f"pair with square {j}")
    assert best is not None
    return best


def serialise(squares_poses: list[tuple[Fraction, Fraction, Fraction]], side: Fraction) -> str:
    lines = [f"{len(squares_poses)} {side}"] + [f"{x} {y} {t}" for (x, y, t) in squares_poses]
    return "\n".join(lines) + "\n"


def controls(path: str) -> dict:
    n, side, poses, digest, _ = read_certificate(path)
    base = squares_from(poses)
    out: dict = {"certificate": path, "sha256": digest, "controls": []}

    def run(name: str, squares: list[Square], box: Fraction, expect_valid: bool, how: str, text: str | None = None) -> None:
        t0 = time.process_time()
        r = decide(squares, box)
        ok = r["sat"]["valid"] == expect_valid and r["area"]["valid"] == expect_valid
        row = {
            "control": name,
            "mutation": how,
            "expected": "accepted" if expect_valid else "refused",
            "sat": {k: r["sat"][k] for k in ("valid", "wall_violations", "pair_violations", "first_wall_violations", "first_pair_violations")},
            "area": {k: r["area"][k] for k in ("valid", "wall_violations", "pair_violations", "first_wall_violations", "first_pair_violations")},
            "as_expected": ok,
            "cpu_seconds": round(time.process_time() - t0, 2),
        }
        if text is not None:
            row["mutated_certificate_sha256"] = hashlib.sha256(text.encode()).hexdigest()
        out["controls"].append(row)
        print(f"  {name:<34} expected {row['expected']:<8} SAT valid={r['sat']['valid']!s:<5} (walls {r['sat']['wall_violations']}, pairs {r['sat']['pair_violations']})"
              f"  AREA valid={r['area']['valid']!s:<5} (walls {r['area']['wall_violations']}, pairs {r['area']['pair_violations']})  {'ok' if ok else 'UNEXPECTED'}")

    # 1. The box at the packing's extent, and 1e-30 below it.
    e = extent(base)
    out["extent"] = str(e)
    out["side_minus_extent"] = str(side - e)
    print(f"  extent E = max corner coordinate; S - E = {float(side - e):.6e}")
    run("box at extent", base, e, True, "side set to E", serialise(poses, e))
    run("box 1e-30 below extent", base, e - TINY, False, "side set to E - 1e-30", serialise(poses, e - TINY))

    # 2. Every square translated to touch the low walls, and 1e-30 past them.
    lx, ly = low_extent(base)
    out["low_extent"] = [str(lx), str(ly)]
    shifted = [(x - lx, y - ly, t) for (x, y, t) in poses]
    run("translated to low walls", [moved(q, -lx, -ly) for q in base], side, True, f"all centres moved by (-{float(lx):.3e}, -{float(ly):.3e})", serialise(shifted, side))
    past = [(x - lx - TINY, y - ly - TINY, t) for (x, y, t) in poses]
    run("translated 1e-30 past low walls", [moved(q, -lx - TINY, -ly - TINY) for q in base], side, False, "the same, 1e-30 further on each axis", serialise(past, side))

    # 3. The closest pair closed to contact along its separating axis, and 1e-30 past.
    gaps = []
    for i, j in combinations(range(n), 2):
        g, k, sgn = sat_gap(base[i], base[j])
        gaps.append((g, i, j, k, sgn))
    gaps.sort(key=lambda r: r[0])
    out["closest_pairs"] = [[float(g), i, j] for (g, i, j, _, _) in gaps[:6]]
    closed = False
    for g, i, j, k, sgn in gaps[:40]:
        ux, uy = axis_of(base[i], base[j], k)
        for mover, sign in ((j, -sgn), (i, sgn)):
            dx, dy = sign * g * ux, sign * g * uy
            trial = list(base)
            trial[mover] = moved(base[mover], dx, dy)
            # Only the moved square's pairs and walls change; the full decision follows in run().
            low, high = wall_slacks(trial[mover], side)
            if low < 0 or high < 0 or any(sat_gap(trial[mover], trial[o])[0] < 0 for o in range(n) if o != mover):
                continue
            g_after = sat_gap(trial[i], trial[j])[0]
            if g_after != 0:
                continue
            pose = list(poses)
            x, y, t = pose[mover]
            pose[mover] = (x + dx, y + dy, t)
            run("closest pair at contact", trial, side, True, f"pair ({i}, {j}), gap {float(g):.6e}; square {mover} moved by exactly the gap along the separating axis", serialise(pose, side))
            fx, fy = sign * (g + TINY) * ux, sign * (g + TINY) * uy
            trial2 = list(base)
            trial2[mover] = moved(base[mover], fx, fy)
            pose2 = list(poses)
            pose2[mover] = (x + fx, y + fy, t)
            run("closest pair 1e-30 past contact", trial2, side, False, f"the same square moved 1e-30 further along that axis", serialise(pose2, side))
            out["pair_control"] = {"pair": [i, j], "gap": str(g), "mover": mover, "axis": [str(ux), str(uy)]}
            closed = True
            break
        if closed:
            break
    if not closed:
        out["pair_control"] = "no pair among the 40 closest closes cleanly by moving one square"

    # 4. The square with the least room enlarged to its critical size, and 1e-30 past it.
    rooms = [(critical_size(base, i, side), i) for i in range(n)]
    (crit, why), i = min(rooms, key=lambda r: r[0][0])
    out["enlarge_control"] = {"square": i, "critical_size": str(crit), "critical_minus_1": float(crit - 1), "limited_by": why}
    trial = list(base)
    trial[i] = scaled(base[i], crit)
    run("least-room square at critical size", trial, side, True, f"square {i} scaled about its centre to {float(crit)!r} ({why})")
    trial = list(base)
    trial[i] = scaled(base[i], crit + TINY)
    run("least-room square 1e-30 past it", trial, side, False, f"square {i} scaled to the critical size + 1e-30")

    # 4b. The square with the least room that a neighbour, not a wall, limits.
    pair_limited = []
    for idx in range(n):
        (c_all, why_all), (c_pair, why_pair) = rooms[idx][0], critical_size(base, idx, side, walls=False)
        if c_pair == c_all:
            pair_limited.append((c_pair, why_pair, idx))
    crit2, why2, i2 = min(pair_limited, key=lambda r: r[0])
    out["enlarge_pair_control"] = {"square": i2, "critical_size": str(crit2), "critical_minus_1": float(crit2 - 1), "limited_by": why2}
    trial = list(base)
    trial[i2] = scaled(base[i2], crit2)
    run("least pair-limited square at size", trial, side, True, f"square {i2} scaled about its centre to its critical size ({why2})")
    trial = list(base)
    trial[i2] = scaled(base[i2], crit2 + TINY)
    run("least pair-limited square 1e-30 past", trial, side, False, f"square {i2} scaled to that size + 1e-30")

    # 5. A wall square enlarged past its wall: the square with the least low-wall slack.
    lows = [(wall_slacks(q, side)[0], idx) for idx, q in enumerate(base)]
    w, idx = min(lows)
    trial = list(base)
    trial[idx] = moved(base[idx], -w - TINY, Fraction(0))
    pose = list(poses)
    x, y, t = pose[idx]
    pose[idx] = (x - w - TINY, y, t)
    run("least-slack wall square 1e-30 past", trial, side, False, f"square {idx} moved left by its wall slack {float(w):.3e} + 1e-30", serialise(pose, side))

    # 6. A duplicated square.
    dup = list(base) + [base[0]]
    run("duplicated square", dup, side, False, "square 0 appended a second time (n = 183)", serialise([*poses, poses[0]], side))

    # 7. Rotation sense: reversed sense refused, the mirror image accepted.
    run("rotation sense reversed", squares_from(poses, mirror=True), side, False, "every frame (c, s) read as (c, -s), centres unchanged")
    mirror_poses = [(side - x, y, -t) for (x, y, t) in poses]
    run("mirror image (x -> S - x, t -> -t)", squares_from(mirror_poses), side, True, "the certificate reflected in the line x = S/2", serialise(mirror_poses, side))
    out["all_as_expected"] = all(c["as_expected"] for c in out["controls"])
    print(f"  all controls as expected: {out['all_as_expected']}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("mode", choices=("check", "controls"))
    ap.add_argument("certificate")
    ap.add_argument("--json", help="write the receipt here")
    args = ap.parse_args()
    t0 = time.process_time()
    result = check(args.certificate) if args.mode == "check" else controls(args.certificate)
    result["program"] = "exact_check.py"
    result["program_sha256"] = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
    result["python"] = sys.version.split()[0]
    result["cpu_seconds_total"] = round(time.process_time() - t0, 1)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(result, fh, indent=1)
            fh.write("\n")
    print(f"  total CPU {result['cpu_seconds_total']} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
