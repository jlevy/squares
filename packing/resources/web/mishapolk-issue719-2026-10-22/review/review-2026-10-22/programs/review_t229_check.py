#!/usr/bin/env python3
"""Exact feasibility checker of the T-229 review (lane c-review-t229-math).

Standard library only; it imports nothing from the repository. It was written from
the mathematics and from the certificate formats (the source certificate's own
format line, and the packet's derived facts and README) before its author read any
of this repository's maintained exact routes, any earlier review's checker, or any
of the source's code.

A packing of n unit squares in the closed box [0, S]^2 is feasible when every square
lies in the box and no two squares' interiors meet. Two routes decide it and share
only the reader:

route Z, integers only (the fractions module is not used):
    a Pythagorean triple (a, b, d), a^2 + b^2 = d^2, per square for its rotation
    (cos, sin) = (a/d, b/d); containment by the half-extent (|a| + |b|)/(2d) against
    each wall; and every one of the n(n-1)/2 pairs by the four separating-axis
    inequalities with every denominator cleared, giving each pair's exact gap, the
    largest separation over the four edge normals.

route C, fractions.Fraction:
    the four corners built from the rotation; unit edges, right angles, positive
    orientation and the corner mean checked on them; every corner in the box; and
    every pair decided, with no filter, by the exact area that one square's four
    closed half-planes clip from the other (positive exactly when the interiors
    meet; a non-empty clip of zero area is a contact). For every pair whose centres
    are closer than 2 it also computes the exact squared Euclidean distance between
    the two closed squares; a pair whose centres are 2 or more apart is at least
    2 - sqrt(2) > 0.585 apart.

Readers: the source's certificate text ("evand-cert": optional '#' comment lines, a
header "n S", then n rows "x y t", each a rational literal, the rotation being
(cos, sin) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))), and the packet's Witness/v2 fact
(representation center-basis, unit squares, lower-left origin, x right and y up),
read by a strict line reader for exactly that layout, gzip or plain.

Usage:
    review_t229_check.py selftest [OUT.json]
    review_t229_check.py check OUT.json LABEL=PATH [LABEL=PATH ...]
    review_t229_check.py same OUT.json LABEL=CERT_PATH=FACT_PATH [...]
"""

import gzip
import hashlib
import json
import math
import re
import sys
import time
from fractions import Fraction

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


class ReadError(Exception):
    """The input is not a certificate or fact this reader understands."""


# --------------------------------------------------------------------------------------
# The reader, shared by both routes.
# --------------------------------------------------------------------------------------

_RAT = re.compile(r"-?[0-9]+(?:/[0-9]+)?\Z")
_UINT = re.compile(r"[0-9]+\Z")


def rat(tok):
    """A rational literal as a reduced (numerator, denominator > 0) integer pair."""
    if not _RAT.match(tok):
        raise ReadError(f"not a rational literal: {tok[:60]!r}")
    if "/" in tok:
        a, b = tok.split("/")
        num, den = int(a), int(b)
        if den == 0:
            raise ReadError(f"zero denominator: {tok[:60]!r}")
    else:
        num, den = int(tok), 1
    g = math.gcd(num, den)
    return (num // g, den // g)


def rat_str(p):
    return f"{p[0]}/{p[1]}" if p[1] != 1 else f"{p[0]}"


def read_cert_text(text):
    header = None
    rows = []
    for lineno, raw in enumerate(text.split("\n"), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        toks = line.split()
        if header is None:
            if len(toks) != 2 or not _UINT.match(toks[0]):
                raise ReadError(f"line {lineno}: header is not 'n S'")
            n = int(toks[0])
            side = rat(toks[1])
            if side[0] <= 0:
                raise ReadError("side is not positive")
            header = (n, side)
            continue
        if len(toks) != 3:
            raise ReadError(f"line {lineno}: a row is not 'x y t'")
        x, y, t = (rat(tk) for tk in toks)
        rows.append({"id": len(rows) + 1, "x": x, "y": y, "rot": ("t", t)})
    if header is None:
        raise ReadError("no header")
    n, side = header
    if len(rows) != n:
        raise ReadError(f"{len(rows)} rows for n = {n}")
    return {"format": "evand-cert", "n": n, "side": side, "squares": rows}


def _unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
        return v[1:-1]
    return v


_TOP = re.compile(r"  ([a-z_]+):(?: (.*))?\Z")
_SUB = re.compile(r"    ([a-z_]+): (.*)\Z")
_ITEM = re.compile(r"  - id: ([0-9]+)\Z")
_VAL = re.compile(r"    - (.*)\Z")
_FACT_KEYS = {"id", "n", "side", "square_size", "representation", "scalar",
              "coordinates", "squares", "claim", "source"}


def read_fact_text(text):
    lines = text.split("\n")
    if "witness:" not in lines:
        raise ReadError("no 'witness:' block")
    start = lines.index("witness:") + 1
    block = []
    for raw in lines[start:]:
        if raw == "":
            continue
        if not raw.startswith(" "):
            break
        block.append(raw)
    top = {}
    sub = {}
    squares = []
    i = 0
    while i < len(block):
        m = _TOP.match(block[i])
        if not m:
            raise ReadError(f"unexpected line in witness: {block[i][:60]!r}")
        key, val = m.group(1), m.group(2)
        if key not in _FACT_KEYS:
            raise ReadError(f"unknown witness key {key!r}")
        if key in top:
            raise ReadError(f"duplicate witness key {key!r}")
        top[key] = val
        i += 1
        if key in ("scalar", "coordinates"):
            sub[key] = {}
            while i < len(block) and block[i].startswith("    "):
                sm = _SUB.match(block[i])
                if not sm:
                    raise ReadError(f"unexpected line under {key}: {block[i][:60]!r}")
                sub[key][sm.group(1)] = _unquote(sm.group(2))
                i += 1
        elif key == "squares":
            while i < len(block) and block[i].startswith("  - "):
                im = _ITEM.match(block[i])
                if not im:
                    raise ReadError(f"unexpected square item: {block[i][:60]!r}")
                sid = int(im.group(1))
                expect = ["    center:", None, None, "    basis:", None, None]
                vals = []
                for k, want in enumerate(expect):
                    line = block[i + 1 + k] if i + 1 + k < len(block) else ""
                    if want is not None:
                        if line != want:
                            raise ReadError(f"square {sid}: expected {want.strip()!r}")
                    else:
                        vm = _VAL.match(line)
                        if not vm:
                            raise ReadError(f"square {sid}: expected a list value")
                        vals.append(rat(_unquote(vm.group(1))))
                i += 1 + len(expect)
                if i < len(block) and block[i].startswith("    "):
                    raise ReadError(f"square {sid}: unexpected key {block[i].strip()[:40]!r}")
                squares.append({"id": sid, "x": vals[0], "y": vals[1],
                                "rot": ("basis", vals[2], vals[3])})
        else:
            while i < len(block) and block[i].startswith("   "):
                i += 1  # the nested content of id, claim and source decides nothing
    for key in ("n", "side", "square_size", "representation", "squares"):
        if key not in top:
            raise ReadError(f"missing witness key {key!r}")
    if not _UINT.match(top["n"] or ""):
        raise ReadError("n is not a count")
    n = int(top["n"])
    side = rat(_unquote(top["side"]))
    if side[0] <= 0:
        raise ReadError("side is not positive")
    if rat(_unquote(top["square_size"])) != (1, 1):
        raise ReadError("square_size is not 1")
    if _unquote(top["representation"]) != "center-basis":
        raise ReadError("representation is not center-basis")
    if sub.get("scalar", {}).get("kind") != "rational":
        raise ReadError("scalar kind is not rational")
    coords = sub.get("coordinates", {})
    if coords.get("origin") != "lower-left" or coords.get("axes") != "x-right-y-up":
        raise ReadError("coordinates are not lower-left, x right and y up")
    if len(squares) != n:
        raise ReadError(f"{len(squares)} squares for n = {n}")
    if [s["id"] for s in squares] != list(range(1, n + 1)):
        raise ReadError("square ids are not 1..n in order")
    return {"format": "witness-v2-center-basis", "n": n, "side": side, "squares": squares}


def load(path):
    raw = open(path, "rb").read()
    info = {"path": path, "file_sha256": hashlib.sha256(raw).hexdigest()}
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
        info["content_sha256"] = hashlib.sha256(raw).hexdigest()
    info["content_git_blob"] = hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ReadError("not ASCII") from exc
    if "\nwitness:" in "\n" + text:
        pk = read_fact_text(text)
    else:
        pk = read_cert_text(text)
    pk.update(info)
    return pk


# --------------------------------------------------------------------------------------
# Route Z: integers only.
# --------------------------------------------------------------------------------------

def _less(p, q):
    """p < q for rationals given as (num, den > 0)."""
    return p[0] * q[1] < q[0] * p[1]


def _reduce(num, den):
    g = math.gcd(num, den)
    return (num // g, den // g)


def route_z(pk):
    t0 = time.process_time()
    n = pk["n"]
    SN, SD = pk["side"]
    out = {"route": "Z", "rows_not_unit": [], "wall_failures": [], "overlaps": [],
           "touching": [], "wall_contacts": []}
    sq = []
    for r in pk["squares"]:
        X, DX = r["x"]
        Y, DY = r["y"]
        if r["rot"][0] == "t":
            p, q = r["rot"][1]
            a, b, d = q * q - p * p, 2 * p * q, q * q + p * p
        else:
            (cn, cd), (sn, sd) = r["rot"][1], r["rot"][2]
            d = cd * sd // math.gcd(cd, sd)
            a, b = cn * (d // cd), sn * (d // sd)
        g = math.gcd(math.gcd(a, b), d)
        a, b, d = a // g, b // g, d // g
        if d <= 0 or a * a + b * b != d * d:
            out["rows_not_unit"].append(r["id"])
        sq.append((r["id"], X, DX, Y, DY, a, b, d))
    out["rows_on_unit_circle"] = n - len(out["rows_not_unit"])
    # Containment: the centre clears each wall by the half-extent (|a| + |b|)/(2d).
    best_wall = None
    for sid, X, DX, Y, DY, a, b, d in sq:
        e = abs(a) + abs(b)
        walls = (
            ("x>=0", (2 * d * X - DX * e, 2 * d * DX)),
            ("x<=S", (2 * d * DX * SN - SD * (2 * d * X + DX * e), 2 * d * DX * SD)),
            ("y>=0", (2 * d * Y - DY * e, 2 * d * DY)),
            ("y<=S", (2 * d * DY * SN - SD * (2 * d * Y + DY * e), 2 * d * DY * SD)),
        )
        for wname, c in walls:
            if c[0] < 0:
                out["wall_failures"].append([sid, wname])
            elif c[0] == 0:
                out["wall_contacts"].append([sid, wname])
            if best_wall is None or _less(c, best_wall[0]):
                best_wall = (c, sid, wname)
    # Pairs: four separating axes, every pair, no filter.
    best_gap = None
    near = 0
    classes = bytearray()
    pairs = 0
    axis_names = ("u_i", "v_i", "u_j", "v_j")
    for ii in range(n):
        si, Xi, DXi, Yi, DYi, ai, bi, di = sq[ii]
        for jj in range(ii + 1, n):
            sj, Xj, DXj, Yj, DYj, aj, bj, dj = sq[jj]
            DXp = DXi * DXj
            DYp = DYi * DYj
            P = (Xj * DXi - Xi * DXj) * DYp
            Q = (Yj * DYi - Yi * DYj) * DXp
            M = DXp * DYp
            C = ai * aj + bi * bj
            S = ai * bj - bi * aj
            R = M * (di * dj + abs(C) + abs(S))
            Ls = (2 * dj * abs(ai * P + bi * Q), 2 * dj * abs(ai * Q - bi * P),
                  2 * di * abs(aj * P + bj * Q), 2 * di * abs(aj * Q - bj * P))
            L = max(Ls)
            num = L - R
            den = 2 * di * dj * M
            pairs += 1
            if P * P + Q * Q < 2 * M * M:
                near += 1
            if num < 0:
                classes.append(0)
                out["overlaps"].append([si, sj])
            elif num == 0:
                classes.append(1)
                out["touching"].append([si, sj])
            else:
                classes.append(2)
            if best_gap is None or num * best_gap[0][1] < best_gap[0][0] * den:
                best_gap = ((num, den), si, sj, axis_names[Ls.index(L)])
    out["pairs_decided"] = pairs
    out["near_pairs_centres_within_sqrt2"] = near
    wc = _reduce(*best_wall[0])
    out["least_wall_clearance"] = rat_str(wc)
    out["least_wall_clearance_float"] = wc[0] / wc[1]
    out["least_wall_at"] = [best_wall[1], best_wall[2]]
    if best_gap is not None:
        g = _reduce(*best_gap[0])
        out["least_gap"] = rat_str(g)
        out["least_gap_float"] = g[0] / g[1]
        out["least_gap_pair"] = [best_gap[1], best_gap[2]]
        out["least_gap_axis"] = best_gap[3]
    out["accepted"] = not (out["rows_not_unit"] or out["wall_failures"] or out["overlaps"])
    out["cpu_seconds"] = round(time.process_time() - t0, 3)
    return out, bytes(classes)


# --------------------------------------------------------------------------------------
# Route C: Fraction corners, clipping area, Euclidean distance.
# --------------------------------------------------------------------------------------

def corners_c(r):
    x = Fraction(*r["x"])
    y = Fraction(*r["y"])
    if r["rot"][0] == "t":
        t = Fraction(*r["rot"][1])
        den = 1 + t * t
        c, s = (1 - t * t) / den, 2 * t / den
    else:
        c, s = Fraction(*r["rot"][1]), Fraction(*r["rot"][2])
    ux, uy = c / 2, s / 2
    vx, vy = -s / 2, c / 2
    return (x, y), [(x - ux - vx, y - uy - vy), (x + ux - vx, y + uy - vy),
                    (x + ux + vx, y + uy + vy), (x - ux + vx, y - uy + vy)]


def _unit_square_ok(centre, P):
    e = [(P[(k + 1) % 4][0] - P[k][0], P[(k + 1) % 4][1] - P[k][1]) for k in range(4)]
    for k in range(4):
        ex, ey = e[k]
        fx, fy = e[(k + 1) % 4]
        if ex * ex + ey * ey != 1 or ex * fx + ey * fy != 0 or ex * fy - ey * fx <= 0:
            return False
    mx = sum(p[0] for p in P) / 4
    my = sum(p[1] for p in P) / 4
    return mx == centre[0] and my == centre[1]


def clip(P, Q):
    """Q (convex, counter-clockwise) clipped by the four closed half-planes of P."""
    poly = list(Q)
    for k in range(4):
        if not poly:
            break
        ax, ay = P[k]
        bx, by = P[(k + 1) % 4]
        ex, ey = bx - ax, by - ay
        f = [ex * (py - ay) - ey * (px - ax) for (px, py) in poly]
        new = []
        m = len(poly)
        for idx in range(m):
            fc, fp = f[idx], f[idx - 1]
            cur, prv = poly[idx], poly[idx - 1]
            if fc >= 0:
                if fp < 0:
                    w = fp / (fp - fc)
                    new.append((prv[0] + (cur[0] - prv[0]) * w, prv[1] + (cur[1] - prv[1]) * w))
                new.append(cur)
            elif fp >= 0:
                w = fp / (fp - fc)
                new.append((prv[0] + (cur[0] - prv[0]) * w, prv[1] + (cur[1] - prv[1]) * w))
        poly = new
    return poly


def area2(poly):
    s = Fraction(0)
    m = len(poly)
    for k in range(m):
        x0, y0 = poly[k]
        x1, y1 = poly[(k + 1) % m]
        s += x0 * y1 - x1 * y0
    return s


def _seg_dist2(p, a, b):
    ex, ey = b[0] - a[0], b[1] - a[1]
    wx, wy = p[0] - a[0], p[1] - a[1]
    t = ex * wx + ey * wy
    l2 = ex * ex + ey * ey
    if t <= 0:
        return wx * wx + wy * wy
    if t >= l2:
        dx, dy = p[0] - b[0], p[1] - b[1]
        return dx * dx + dy * dy
    cr = ex * wy - ey * wx
    return cr * cr / l2


def dist2(P, Q):
    best = None
    for A, B in ((P, Q), (Q, P)):
        for p in A:
            for k in range(4):
                d = _seg_dist2(p, B[k], B[(k + 1) % 4])
                if best is None or d < best:
                    best = d
    return best


def route_c(pk):
    t0 = time.process_time()
    n = pk["n"]
    S = Fraction(*pk["side"])
    out = {"route": "C", "not_unit_squares": [], "corners_outside": [], "overlaps": [],
           "touching": [], "wall_contacts": 0}
    cs = []
    best_wall = None
    for r in pk["squares"]:
        centre, P = corners_c(r)
        if not _unit_square_ok(centre, P):
            out["not_unit_squares"].append(r["id"])
        for k, (px, py) in enumerate(P):
            if px < 0 or py < 0 or px > S or py > S:
                out["corners_outside"].append([r["id"], k])
        xs = [p[0] for p in P]
        ys = [p[1] for p in P]
        # Each wall's clearance is its nearest corner's: one value a square and wall.
        for c in (min(xs), S - max(xs), min(ys), S - max(ys)):
            if c == 0:
                out["wall_contacts"] += 1
            if best_wall is None or c < best_wall[0]:
                best_wall = (c, r["id"])
        cs.append((r["id"], centre, P))
    out["unit_squares_checked"] = n - len(out["not_unit_squares"])
    classes = bytearray()
    best_d = None
    near2 = 0
    pairs = 0
    for ii in range(n):
        si, ci, Pi = cs[ii]
        for jj in range(ii + 1, n):
            sj, cj, Pj = cs[jj]
            pairs += 1
            poly = clip(Pi, Pj)
            if not poly:
                cls = 2
            else:
                a2 = area2(poly)
                if a2 > 0:
                    cls = 0
                    out["overlaps"].append([si, sj])
                elif a2 == 0:
                    cls = 1
                    out["touching"].append([si, sj])
                else:
                    raise AssertionError("negative clipped area")
            classes.append(cls)
            dx, dy = cj[0] - ci[0], cj[1] - ci[1]
            if dx * dx + dy * dy < 4:
                near2 += 1
                if cls == 2:
                    d2 = dist2(Pi, Pj)
                    if d2 <= 0:
                        raise AssertionError("disjoint clip with zero distance")
                elif cls == 1:
                    d2 = Fraction(0)
                else:
                    continue
                if best_d is None or d2 < best_d[0]:
                    best_d = (d2, si, sj)
    out["pairs_decided"] = pairs
    out["pairs_centres_within_2"] = near2
    out["least_wall_clearance"] = rat_str((best_wall[0].numerator, best_wall[0].denominator))
    out["least_wall_clearance_float"] = float(best_wall[0])
    if best_d is not None:
        out["least_distance_squared"] = rat_str((best_d[0].numerator, best_d[0].denominator))
        out["least_distance_float"] = math.sqrt(float(best_d[0])) if best_d[0] > 0 else 0.0
        out["least_distance_pair"] = [best_d[1], best_d[2]]
    out["accepted"] = not (out["not_unit_squares"] or out["corners_outside"] or out["overlaps"])
    out["cpu_seconds"] = round(time.process_time() - t0, 3)
    return out, bytes(classes)


# --------------------------------------------------------------------------------------
# Deciding a packing on both routes, and comparing a certificate with a fact.
# --------------------------------------------------------------------------------------

def decide(pk):
    z, zc = route_z(pk)
    c, cc = route_c(pk)
    agree = (z["accepted"] == c["accepted"]
             and z["least_wall_clearance"] == c["least_wall_clearance"]
             and zc == cc
             and len(z["wall_contacts"]) == c["wall_contacts"]
             and z["touching"] == c["touching"] and z["overlaps"] == c["overlaps"])
    # The separating-axis gap never exceeds the Euclidean distance (checked exactly).
    sat_le_dist = None
    if "least_gap" in z and "least_distance_squared" in c:
        g = Fraction(z["least_gap"])
        d2 = Fraction(c["least_distance_squared"])
        sat_le_dist = g <= 0 or g * g <= d2
    return {"route_Z": z, "route_C": c, "routes_agree": agree,
            "per_pair_classes_equal": zc == cc,
            "least_gap_at_most_least_distance": sat_le_dist,
            "accepted": z["accepted"] and c["accepted"] and agree}


def _halfangle(t):
    p, q = t
    return _reduce(q * q - p * p, q * q + p * p), _reduce(2 * p * q, q * q + p * p)


def same(cert, fact):
    """Whether the fact states exactly the certificate's squares, in order."""
    res = {"n_equal": cert["n"] == fact["n"], "side_equal": cert["side"] == fact["side"],
           "rows_exactly_equal": 0, "rows_equal_up_to_quarter_turn": 0, "rows_differing": []}
    for rc, rf in zip(cert["squares"], fact["squares"]):
        if rc["rot"][0] != "t" or rf["rot"][0] != "basis":
            raise ReadError("same() takes a certificate and a fact")
        c, s = _halfangle(rc["rot"][1])
        fc, fs = rf["rot"][1], rf["rot"][2]
        centre = rc["x"] == rf["x"] and rc["y"] == rf["y"]
        if centre and (c, s) == (fc, fs):
            res["rows_exactly_equal"] += 1
        else:
            neg = lambda p: (-p[0], p[1])  # noqa: E731
            quarter = [(c, s), (neg(s), c), (neg(c), neg(s)), (s, neg(c))]
            if centre and (fc, fs) in quarter:
                res["rows_equal_up_to_quarter_turn"] += 1
            else:
                res["rows_differing"].append(rc["id"])
    res["same_packing_exactly"] = (res["n_equal"] and res["side_equal"]
                                   and res["rows_exactly_equal"] == cert["n"] == fact["n"])
    return res


# --------------------------------------------------------------------------------------
# Self-test on hand-built cases.
# --------------------------------------------------------------------------------------

E30 = Fraction(1, 10**30)


def _cert(side, rows):
    def f(v):
        v = Fraction(v)
        return f"{v.numerator}/{v.denominator}"
    lines = ["# hand-built", f"{len(rows)} {f(side)}"]
    lines += [f"{f(x)} {f(y)} {f(t)}" for (x, y, t) in rows]
    return "\n".join(lines) + "\n"


def _fact(side, rows, n=None, extra=""):
    def f(v):
        v = Fraction(v)
        return f"{v.numerator}/{v.denominator}"
    out = ["softschema:", "  contract: packing.squares:Witness/v2", "witness:",
           "  id: W-selftest", f"  n: {len(rows) if n is None else n}", f"  side: {f(side)}",
           "  square_size: '1'", "  representation: center-basis", "  scalar:",
           "    kind: rational", "  coordinates:", "    origin: lower-left",
           "    axes: x-right-y-up", "    angle_unit: not-applicable", "  squares:"]
    for k, (x, y, c, s) in enumerate(rows, 1):
        out += [f"  - id: {k}", "    center:", f"    - {f(x)}", f"    - {f(y)}",
                "    basis:", f"    - '{f(c)}'", f"    - '{f(s)}'"]
        if extra and k == 1:
            out.append(extra)
    out += ["  claim:", "    method: exact-algebraic"]
    return "\n".join(out) + "\n"


def selftest():
    h = Fraction(1, 2)
    n_b = Fraction(6, 5)  # 7/10 + 1/2: A's half-width along (3/5, 4/5) plus B's own
    u = (Fraction(3, 5), Fraction(4, 5))
    cases = [
        # name, text, expected verdict, touching pairs, wall contacts, least gap (or None)
        ("separated", _cert(4, [(1, 1, 0), (Fraction(5, 2), 1, 0)]), True, 0, 0, h),
        ("edge contact", _cert(4, [(1, 1, 0), (2, 1, 0)]), True, 1, 0, 0),
        ("edge overlap 1e-30", _cert(4, [(1, 1, 0), (2 - E30, 1, 0)]), False, 0, 0, -E30),
        ("partial edge contact", _cert(4, [(1, 1, 0), (2, Fraction(13, 10), 0)]), True, 1, 0, 0),
        ("corner contact", _cert(4, [(1, 1, 0), (2, 2, 0)]), True, 1, 0, 0),
        ("tilted vertex on edge", _cert(6, [(2, 2, 0), (Fraction(16, 5), 2, h)]), True, 1, 0, 0),
        ("tilted vertex 1e-30 in", _cert(6, [(2, 2, 0), (Fraction(16, 5) - E30, 2, h)]),
         False, 0, 0, -E30),
        ("tilted vertex 1e-30 out", _cert(6, [(2, 2, 0), (Fraction(16, 5) + E30, 2, h)]),
         True, 0, 0, E30),
        ("separated only on B's axis, contact",
         _cert(5, [(2, 2, 0), (2 + n_b * u[0], 2 + n_b * u[1], h)]), True, 1, 0, 0),
        ("separated only on B's axis, 1e-30 in",
         _cert(5, [(2, 2, 0), (2 + (n_b - E30) * u[0], 2 + (n_b - E30) * u[1], h)]),
         False, 0, 0, -E30),
        ("separated only on B's axis, 1e-30 out",
         _cert(5, [(2, 2, 0), (2 + (n_b + E30) * u[0], 2 + (n_b + E30) * u[1], h)]),
         True, 0, 0, E30),
        ("wall contact", _cert(3, [(h, 1, 0)]), True, 0, 1, None),
        ("wall crossed by 1e-30", _cert(3, [(h - E30, 1, 0)]), False, 0, 0, None),
        ("tilted wall contact", _cert(3, [(Fraction(7, 10), 1, h)]), True, 0, 1, None),
        ("tilted wall crossed by 1e-30", _cert(3, [(Fraction(7, 10) - E30, 1, h)]),
         False, 0, 0, None),
        ("far wall contact, side lowered", _cert(Fraction(3, 2), [(1, 1, 0)]), True, 0, 2, None),
        ("duplicate square", _cert(4, [(1, 1, 0), (1, 1, 0)]), False, 0, 0, -1),
        ("tilted pair, same centre", _cert(4, [(2, 2, h), (2, 2, Fraction(2, 3))]),
         False, 0, 0, None),
        ("fact: separated", _fact(4, [(1, 1, 1, 0), (Fraction(5, 2), 1, 1, 0)]), True, 0, 0, h),
        ("fact: tilted vertex on edge",
         _fact(6, [(2, 2, 1, 0), (Fraction(16, 5), 2, u[0], u[1])]), True, 1, 0, 0),
        ("fact: basis not unit",
         _fact(6, [(2, 2, 1, 0), (4, 2, 1, Fraction(1, 10**6))]), False, 0, 0, None),
    ]
    results = []
    ok_all = True
    for name, text, verdict, touching, walls, gap in cases:
        pk = read_fact_text(text) if text.startswith("softschema") else read_cert_text(text)
        res = decide(pk)
        z, c = res["route_Z"], res["route_C"]
        ok = (res["routes_agree"] and z["accepted"] == verdict and c["accepted"] == verdict
              and len(z["touching"]) == touching and len(c["touching"]) == touching
              and len(z["wall_contacts"]) == walls and c["wall_contacts"] == walls)
        if gap is not None:
            ok = ok and Fraction(z["least_gap"]) == Fraction(gap)
        ok_all = ok_all and ok
        results.append({"case": name, "expected_accepted": verdict, "ok": ok,
                        "route_Z": z["accepted"], "route_C": c["accepted"],
                        "least_gap": z.get("least_gap"), "touching": len(z["touching"]),
                        "wall_contacts": len(z["wall_contacts"])})
    readers = [
        ("row count", _cert(4, [(1, 1, 0)]).replace("\n1 4", "\n2 4"), "rows for n"),
        ("decimal literal", _cert(4, [(1, 1, 0)]).replace("1/1 1/1 0/1", "1.0 1/1 0/1"),
         "not a rational"),
        ("fact count", _fact(4, [(1, 1, 1, 0)], n=2), "squares for n"),
        ("fact unknown key", _fact(4, [(1, 1, 1, 0)], extra="    size: 2"), "unexpected key"),
        ("fact origin", _fact(4, [(1, 1, 1, 0)]).replace("lower-left", "center"),
         "coordinates"),
    ]
    for name, text, needle in readers:
        try:
            if text.startswith("softschema"):
                read_fact_text(text)
            else:
                read_cert_text(text)
            ok = False
            msg = "accepted"
        except ReadError as exc:
            msg = str(exc)
            ok = needle in msg
        ok_all = ok_all and ok
        results.append({"case": "reader: " + name, "ok": ok, "refusal": msg})
    # The same packing as a certificate and as a fact; then one basis turned.
    cert = read_cert_text(_cert(6, [(2, 2, 0), (Fraction(16, 5), 2, h)]))
    fact = read_fact_text(_fact(6, [(2, 2, 1, 0), (Fraction(16, 5), 2, u[0], u[1])]))
    bad = read_fact_text(_fact(6, [(2, 2, 1, 0), (Fraction(16, 5), 2, u[0], -u[1])]))
    s1, s2 = same(cert, fact), same(cert, bad)
    ok = s1["same_packing_exactly"] and not s2["same_packing_exactly"] and s2["rows_differing"] == [2]
    ok_all = ok_all and ok
    results.append({"case": "same(): equal, then one basis mirrored", "ok": ok})
    return ok_all, results


# --------------------------------------------------------------------------------------

def main(argv):
    if not argv:
        print(__doc__)
        return 2
    cmd = argv[0]
    if cmd == "selftest":
        ok, results = selftest()
        for r in results:
            print(("PASS " if r["ok"] else "FAIL ") + r["case"])
        print(f"{sum(r['ok'] for r in results)} of {len(results)} as expected")
        if len(argv) > 1:
            with open(argv[1], "w") as fh:
                json.dump({"python": sys.version.split()[0], "all_as_expected": ok,
                           "cases": results}, fh, indent=1)
        return 0 if ok else 1
    if cmd == "check":
        out_path, specs = argv[1], argv[2:]
        report = {"program": "review_t229_check.py", "python": sys.version.split()[0],
                  "inputs": []}
        all_ok = True
        for spec in specs:
            label, path = spec.split("=", 1)
            pk = load(path)
            res = decide(pk)
            entry = {"label": label, "path": path, "format": pk["format"], "n": pk["n"],
                     "side": rat_str(pk["side"]), "file_sha256": pk["file_sha256"],
                     "content_git_blob": pk["content_git_blob"]}
            if "content_sha256" in pk:
                entry["content_sha256"] = pk["content_sha256"]
            entry.update(res)
            report["inputs"].append(entry)
            z, c = res["route_Z"], res["route_C"]
            print(f"{label}: n={pk['n']} {pk['format']} accepted={res['accepted']} "
                  f"agree={res['routes_agree']} pairs={z['pairs_decided']}/{c['pairs_decided']} "
                  f"wall={z['least_wall_clearance_float']:.6e} gap={z.get('least_gap_float', 0):.10e} "
                  f"pair={z.get('least_gap_pair')} dist={c.get('least_distance_float', 0):.10e} "
                  f"touch={len(z['touching'])} overlap={len(z['overlaps'])} "
                  f"Zcpu={z['cpu_seconds']} Ccpu={c['cpu_seconds']}")
            all_ok = all_ok and res["accepted"]
        with open(out_path, "w") as fh:
            json.dump(report, fh, indent=1)
        return 0 if all_ok else 1
    if cmd == "same":
        out_path, specs = argv[1], argv[2:]
        report = {"program": "review_t229_check.py same", "python": sys.version.split()[0],
                  "pairs": []}
        all_ok = True
        for spec in specs:
            label, cpath, fpath = spec.split("=", 2)
            cert, fact = load(cpath), load(fpath)
            res = same(cert, fact)
            res.update({"label": label, "certificate": cpath, "fact": fpath,
                        "certificate_sha256": cert["file_sha256"],
                        "certificate_git_blob": cert["content_git_blob"],
                        "fact_file_sha256": fact["file_sha256"],
                        "fact_content_sha256": fact.get("content_sha256"),
                        "fact_content_git_blob": fact["content_git_blob"]})
            report["pairs"].append(res)
            print(f"{label}: same_packing_exactly={res['same_packing_exactly']} "
                  f"rows={res['rows_exactly_equal']} differing={res['rows_differing'][:5]}")
            all_ok = all_ok and res["same_packing_exactly"]
        with open(out_path, "w") as fh:
            json.dump(report, fh, indent=1)
        return 0 if all_ok else 1
    print(f"unknown command {cmd!r}")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
