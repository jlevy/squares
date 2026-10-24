#!/usr/bin/env python3
"""Exact finite-feasibility checker written for the stage 4 review of issue 755 (T-238).

Written on 23 October 2026 by the review lane c-review-t238-math (bead think-jdz0), from
the mathematics and the certificate's text alone, before its author read any maintained
route of this repository, any replay tool, or any program of the source or of Evan
Daniel's repository. It shares no code with any of them.

The certificate is read as: comment lines beginning with '#', then a header 'n S', then n
rows 'x y t' of rational literals ('-'? digits, optionally '/' digits). Row k is the unit
square with centre (x, y) whose edges run along u = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))
and v = (-u_y, u_x), so t = tan(theta/2) for the rotation theta. The claim decided is that
these n closed unit squares lie in the closed box [0, S]^2 with pairwise disjoint
interiors, which proves s(n) <= S whatever convention the producer intended, because it
exhibits one explicit packing.

Two routes decide it, sharing only the reader:

Route Z (CPython integers; `fractions` is never imported by this route): for t = p/q the
integers a = q^2 - p^2, b = 2pq, d = q^2 + p^2 (divided by their gcd) satisfy
a^2 + b^2 = d^2, checked per row. A square lies in the box exactly when its centre clears
each wall by the half-extent (|a| + |b|)/(2d). Two squares have disjoint interiors exactly
when one of the four edge normals u_i, v_i, u_j, v_j weakly separates them (the Minkowski
difference of two squares is a convex polygon whose edges are parallel to theirs), and
they are disjoint as closed sets exactly when one strictly separates them. Every pair is
decided, with no distance filter, by four integer inequalities with all denominators
cleared; its exact gap, the largest separation over the four axes, is recorded.

Route E (fractions.Fraction, corners): each square's four corners are built from u and v;
unit edges, right angles, positive orientation and the corner mean are checked; the box
is checked on corners. A pair whose centres are more than sqrt(2) apart (|dc|^2 > 2,
decided exactly) is disjoint, since each square lies in the closed disc of radius
sqrt(2)/2 about its centre. Every other pair is decided combinatorially: two closed convex
polygons meet exactly when an edge of one meets an edge of the other or a vertex of one
lies in the other, decided by exact orientation tests. For a disjoint close pair the exact
squared Euclidean distance is the least squared vertex-to-edge distance either way. A pair
that meets is overlapping exactly when the region its closed half-planes clip from the
other square has positive area, and touching otherwise. Route E also recomputes every
pair's separating-axis gap from corner projections, so that its arithmetic can be held to
route Z's pair by pair; that recomputation is a comparison, not route E's decision.

No route rounds, dilates or tolerates anything.

Usage:
  python3 -I review_t238_check.py CERT --route Z|E [--receipt OUT.json] [--pairs OUT.tsv]
  python3 -I review_t238_check.py --self-test

Exit status: 0 accepted, 1 refused (a wall or a pair), 2 unreadable.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import json
import math
import platform
import random
import re
import sys
import time
from pathlib import Path

_LITERAL = re.compile(r"-?[0-9]+(?:/[0-9]+)?\Z")


class ReadError(Exception):
    """The text is not a certificate in the format this checker reads."""


# ---------------------------------------------------------------------------
# The reader, shared by both routes.
# ---------------------------------------------------------------------------


def parse_literal(token: str) -> tuple[int, int]:
    """Return (p, q) in lowest terms with q > 0 for a literal '-'? digits ('/' digits)?."""
    if not _LITERAL.match(token):
        raise ReadError(f"not a rational literal: {token[:60]!r}")
    if "/" in token:
        num_text, den_text = token.split("/")
        p, q = int(num_text), int(den_text)
        if q == 0:
            raise ReadError(f"zero denominator: {token[:60]!r}")
    else:
        p, q = int(token), 1
    g = math.gcd(p, q)
    return p // g, q // g


def read_certificate(data: bytes) -> dict:
    """Read the certificate strictly. Return n, the side and the rows as integer pairs."""
    try:
        text = data.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ReadError("not ASCII") from exc
    if "\r" in text or "\t" in text:
        raise ReadError("carriage return or tab in the text")
    lines = text.split("\n")
    trailing_newline = lines[-1] == ""
    if trailing_newline:
        lines.pop()
    comments: list[str] = []
    k = 0
    while k < len(lines) and lines[k].startswith("#"):
        comments.append(lines[k])
        k += 1
    if k >= len(lines):
        raise ReadError("no header line")
    header = lines[k].split(" ")
    if len(header) != 2 or "" in header:
        raise ReadError(f"header is not 'n S': {lines[k][:80]!r}")
    n_p, n_q = parse_literal(header[0])
    if "/" in header[0] or n_q != 1 or n_p <= 0:
        raise ReadError(f"n is not a positive integer: {header[0]!r}")
    side = parse_literal(header[1])
    if side[0] <= 0:
        raise ReadError("side is not positive")
    rows = []
    body = lines[k + 1 :]
    for m, line in enumerate(body):
        if line == "":
            raise ReadError(f"blank line at line {k + 2 + m}")
        if line.startswith("#"):
            raise ReadError(f"comment after the header at line {k + 2 + m}")
        tokens = line.split(" ")
        if len(tokens) != 3 or "" in tokens:
            raise ReadError(f"row {m} is not 'x y t' at line {k + 2 + m}")
        rows.append(tuple(parse_literal(tok) for tok in tokens))
    if len(rows) != n_p:
        raise ReadError(f"{len(rows)} square rows for n = {n_p}")
    return {
        "n": n_p,
        "side": side,
        "rows": rows,
        "comments": comments,
        "header_line": k + 1,
        "trailing_newline": trailing_newline,
    }


def canon(p: int, q: int) -> str:
    """A rational in lowest terms as 'p/q' with q > 0."""
    if q < 0:
        p, q = -p, -q
    g = math.gcd(p, q)
    return f"{p // g}/{q // g}"


def less(a: tuple[int, int], b: tuple[int, int]) -> bool:
    """a < b for rationals given as (num, den) with den > 0."""
    return a[0] * b[1] < b[0] * a[1]


def below_power(num: int, den: int, k: int) -> bool:
    """num/den < 10^-k, den > 0."""
    return num * 10**k < den


def to_sci(num: int, den: int, digits: int = 15) -> str:
    """A decimal print of num/den in scientific notation, truncated toward zero, from integers."""
    if num == 0:
        return "0"
    sign = "-" if (num < 0) != (den < 0) else ""
    num, den = abs(num), abs(den)
    e = len(str(num)) - len(str(den))
    # adjust so that 1 <= num/den * 10^-e < 10
    if num * 10 ** max(0, -e) < den * 10 ** max(0, e):
        e -= 1
    scaled = num * 10 ** max(0, digits - e) // (den * 10 ** max(0, e - digits))
    s = str(scaled)
    return f"{sign}{s[0]}.{s[1:digits + 1]}e{e:+d}"


# ---------------------------------------------------------------------------
# Route Z: integers only.
# ---------------------------------------------------------------------------


def route_z(cert: dict, pairs_out=None) -> dict:
    n = cert["n"]
    side_p, side_q = cert["side"]
    rows = cert["rows"]
    lcm = side_q
    for (xp, xq), (yp, yq), _ in rows:
        lcm = lcm * xq // math.gcd(lcm, xq)
        lcm = lcm * yq // math.gcd(lcm, yq)
    big_l = lcm
    big_s = side_p * (big_l // side_q)
    cx = [xp * (big_l // xq) for (xp, xq), _, _ in rows]
    cy = [yp * (big_l // yq) for _, (yp, yq), _ in rows]
    rot = []
    for _, _, (tp, tq) in rows:
        a = tq * tq - tp * tp
        b = 2 * tp * tq
        d = tq * tq + tp * tp
        g = math.gcd(math.gcd(a, b), d)
        a, b, d = a // g, b // g, d // g
        if a * a + b * b != d * d or d <= 0:
            raise AssertionError("rotation triple off the unit circle")
        rot.append((a, b, d))

    walls = {"left": [], "right": [], "bottom": [], "top": []}
    wall_failures = []
    for k in range(n):
        a, b, d = rot[k]
        e = abs(a) + abs(b)
        den = 2 * d * big_l
        nums = {
            "left": 2 * d * cx[k] - big_l * e,
            "right": 2 * d * (big_s - cx[k]) - big_l * e,
            "bottom": 2 * d * cy[k] - big_l * e,
            "top": 2 * d * (big_s - cy[k]) - big_l * e,
        }
        for wall, num in nums.items():
            walls[wall].append((num, den))
            if num < 0:
                wall_failures.append((k, wall))

    least_wall = {}
    for wall, vals in walls.items():
        m = None
        for k in range(n):
            if m is None or less(vals[k], m):
                m = vals[k]
        at = [k for k in range(n) if vals[k][0] * m[1] == m[0] * vals[k][1]]
        least_wall[wall] = {"clearance": canon(*m), "approx": to_sci(*m), "squares": at}
    wall_digest = hashlib.sha256()
    for k in range(n):
        for wall in ("left", "right", "bottom", "top"):
            wall_digest.update(f"{k} {wall} {canon(*walls[wall][k])}\n".encode())

    pair_digest = hashlib.sha256()
    least = None
    least_at = []
    touching = []
    overlapping = []
    counts = {f"below_1e-{k}": 0 for k in (9, 10, 11, 12, 13, 15, 20)}
    npairs = 0
    tight: list[tuple[tuple[int, int], int, int, int]] = []
    for i in range(n):
        ai, bi, di = rot[i]
        xi, yi = cx[i], cy[i]
        for j in range(i + 1, n):
            aj, bj, dj = rot[j]
            dx = cx[j] - xi
            dy = cy[j] - yi
            c = ai * aj + bi * bj
            s = ai * bj - bi * aj
            r = big_l * (di * dj + abs(c) + abs(s))
            proj = (
                2 * dj * abs(dx * ai + dy * bi),
                2 * dj * abs(dy * ai - dx * bi),
                2 * di * abs(dx * aj + dy * bj),
                2 * di * abs(dy * aj - dx * bj),
            )
            m = max(proj)
            axis = proj.index(m)
            gnum = m - r
            gden = 2 * big_l * di * dj
            g = math.gcd(gnum, gden)
            gnum //= g
            gden //= g
            npairs += 1
            pair_digest.update(f"{i} {j} {gnum}/{gden}\n".encode())
            if pairs_out is not None:
                pairs_out.write(f"{i}\t{j}\t{gnum}/{gden}\t{axis}\n")
            if gnum < 0:
                overlapping.append((i, j, canon(gnum, gden)))
            elif gnum == 0:
                touching.append((i, j))
            for kk in (9, 10, 11, 12, 13, 15, 20):
                if below_power(gnum, gden, kk):
                    counts[f"below_1e-{kk}"] += 1
            val = (gnum, gden)
            if least is None or less(val, least):
                least = val
                least_at = [(i, j, axis)]
            elif val[0] * least[1] == least[0] * val[1]:
                least_at.append((i, j, axis))
            if gnum * 10**11 < gden:
                tight.append((val, i, j, axis))
    tight.sort(key=functools.cmp_to_key(lambda s, t: -1 if less(s[0], t[0]) else (1 if less(t[0], s[0]) else 0)))
    axis_names = ("u_i", "v_i", "u_j", "v_j")
    accepted = not wall_failures and not overlapping
    return {
        "route": "Z",
        "accepted": accepted,
        "n": n,
        "pairs_decided": npairs,
        "common_denominator_digits": len(str(big_l)),
        "wall_failures": wall_failures[:20],
        "overlapping_pairs": overlapping[:20],
        "overlapping_count": len(overlapping),
        "touching_pairs": touching[:50],
        "touching_count": len(touching),
        "least_wall": least_wall,
        "least_gap": None
        if least is None
        else {
            "gap": canon(*least),
            "approx": to_sci(*least),
            "pairs": [{"i": i, "j": j, "axis": axis_names[ax]} for i, j, ax in least_at],
        },
        "gap_counts": counts,
        "tightest_pairs": [
            {"i": i, "j": j, "gap": canon(*v), "approx": to_sci(*v), "axis": axis_names[ax]}
            for v, i, j, ax in tight[:40]
        ],
        "per_square_wall_digest": wall_digest.hexdigest(),
        "per_pair_gap_digest": pair_digest.hexdigest(),
        "fractions_imported_by_route": "fractions" in sys.modules,
    }


# ---------------------------------------------------------------------------
# Route E: Fraction corners, discs, orientation tests, distances, clipping.
# ---------------------------------------------------------------------------


def route_e(cert: dict, pairs_out=None) -> dict:
    from fractions import Fraction as Q  # noqa: PLC0415  (route E's own kernel)

    n = cert["n"]
    side = Q(*cert["side"])
    half = Q(1, 2)
    squares = []
    shape_failures = []
    tilt_kinds = {"t_zero": 0, "t_plus_one": 0, "t_minus_one": 0, "tilted": 0}
    for k, ((xp, xq), (yp, yq), (tp, tq)) in enumerate(cert["rows"]):
        c = (Q(xp, xq), Q(yp, yq))
        t = Q(tp, tq)
        w = 1 + t * t
        u = ((1 - t * t) / w, 2 * t / w)
        v = (-u[1], u[0])
        if t == 0:
            tilt_kinds["t_zero"] += 1
        elif t == 1:
            tilt_kinds["t_plus_one"] += 1
        elif t == -1:
            tilt_kinds["t_minus_one"] += 1
        else:
            tilt_kinds["tilted"] += 1
        hu = (u[0] * half, u[1] * half)
        hv = (v[0] * half, v[1] * half)
        corners = [
            (c[0] - hu[0] - hv[0], c[1] - hu[1] - hv[1]),
            (c[0] + hu[0] - hv[0], c[1] + hu[1] - hv[1]),
            (c[0] + hu[0] + hv[0], c[1] + hu[1] + hv[1]),
            (c[0] - hu[0] + hv[0], c[1] - hu[1] + hv[1]),
        ]
        ok = True
        for m in range(4):
            p0, p1, p2 = corners[m], corners[(m + 1) % 4], corners[(m + 2) % 4]
            e1 = (p1[0] - p0[0], p1[1] - p0[1])
            e2 = (p2[0] - p1[0], p2[1] - p1[1])
            if e1[0] * e1[0] + e1[1] * e1[1] != 1:
                ok = False
            if e1[0] * e2[0] + e1[1] * e2[1] != 0:
                ok = False
            if e1[0] * e2[1] - e1[1] * e2[0] != 1:
                ok = False
        mean = (sum(p[0] for p in corners) / 4, sum(p[1] for p in corners) / 4)
        if mean != c:
            ok = False
        if not ok:
            shape_failures.append(k)
        squares.append({"c": c, "u": u, "v": v, "k": corners})

    wall_vals = {"left": [], "right": [], "bottom": [], "top": []}
    wall_failures = []
    for k, sq in enumerate(squares):
        xs = [p[0] for p in sq["k"]]
        ys = [p[1] for p in sq["k"]]
        vals = {
            "left": min(xs),
            "right": side - max(xs),
            "bottom": min(ys),
            "top": side - max(ys),
        }
        for wall, val in vals.items():
            wall_vals[wall].append(val)
            if val < 0:
                wall_failures.append((k, wall))
    least_wall = {}
    for wall, vals in wall_vals.items():
        m = min(vals)
        least_wall[wall] = {
            "clearance": f"{m.numerator}/{m.denominator}",
            "approx": to_sci(m.numerator, m.denominator),
            "squares": [k for k in range(n) if vals[k] == m],
        }
    wall_digest = hashlib.sha256()
    for k in range(n):
        for wall in ("left", "right", "bottom", "top"):
            val = wall_vals[wall][k]
            wall_digest.update(f"{k} {wall} {val.numerator}/{val.denominator}\n".encode())

    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    def on_seg(a, b, p):
        return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])

    def segs_meet(p1, p2, q1, q2):
        d1 = orient(q1, q2, p1)
        d2 = orient(q1, q2, p2)
        d3 = orient(p1, p2, q1)
        d4 = orient(p1, p2, q2)
        if ((d1 > 0 > d2) or (d1 < 0 < d2)) and ((d3 > 0 > d4) or (d3 < 0 < d4)):
            return True
        if d1 == 0 and on_seg(q1, q2, p1):
            return True
        if d2 == 0 and on_seg(q1, q2, p2):
            return True
        if d3 == 0 and on_seg(p1, p2, q1):
            return True
        if d4 == 0 and on_seg(p1, p2, q2):
            return True
        return False

    def inside_closed(poly, p):
        return all(orient(poly[m], poly[(m + 1) % 4], p) >= 0 for m in range(4))

    def seg_dist2(p, a, b):
        ab = (b[0] - a[0], b[1] - a[1])
        ap = (p[0] - a[0], p[1] - a[1])
        ll = ab[0] * ab[0] + ab[1] * ab[1]
        t = (ap[0] * ab[0] + ap[1] * ab[1]) / ll
        if t < 0:
            t = Q(0)
        elif t > 1:
            t = Q(1)
        cx_ = a[0] + t * ab[0] - p[0]
        cy_ = a[1] + t * ab[1] - p[1]
        return cx_ * cx_ + cy_ * cy_

    def clip(subject, poly):
        out = list(subject)
        for m in range(4):
            e0, e1 = poly[m], poly[(m + 1) % 4]
            inp = out
            out = []
            if not inp:
                break
            prev = inp[-1]
            fp = orient(e0, e1, prev)
            for cur in inp:
                fc = orient(e0, e1, cur)
                if fc >= 0:
                    if fp < 0:
                        r = fp / (fp - fc)
                        out.append((prev[0] + r * (cur[0] - prev[0]), prev[1] + r * (cur[1] - prev[1])))
                    out.append(cur)
                elif fp >= 0:
                    r = fp / (fp - fc)
                    out.append((prev[0] + r * (cur[0] - prev[0]), prev[1] + r * (cur[1] - prev[1])))
                prev, fp = cur, fc
        return out

    def area2(poly):
        s = Q(0)
        for m in range(len(poly)):
            p, q = poly[m], poly[(m + 1) % len(poly)]
            s += p[0] * q[1] - p[1] * q[0]
        return s

    def proj_range(corners, w):
        vals = [p[0] * w[0] + p[1] * w[1] for p in corners]
        return min(vals), max(vals)

    pair_digest = hashlib.sha256()
    far = close = 0
    overlapping = []
    touching = []
    least_dist2 = None
    least_dist2_at = []
    clip_disagreements = []
    close_dist2 = []
    npairs = 0
    for i in range(n):
        si = squares[i]
        for j in range(i + 1, n):
            sj = squares[j]
            npairs += 1
            # the separating-axis gap again, from corner projections (a comparison, not the decision)
            best = None
            for w in (si["u"], si["v"], sj["u"], sj["v"]):
                lo_i, hi_i = proj_range(si["k"], w)
                lo_j, hi_j = proj_range(sj["k"], w)
                g = max(lo_j - hi_i, lo_i - hi_j)
                if best is None or g > best:
                    best = g
            pair_digest.update(f"{i} {j} {best.numerator}/{best.denominator}\n".encode())
            dcx = sj["c"][0] - si["c"][0]
            dcy = sj["c"][1] - si["c"][1]
            r2 = dcx * dcx + dcy * dcy
            if r2 > 2:
                far += 1
                verdict = "separated-by-discs"
                d2 = None
            else:
                close += 1
                pk, qk = si["k"], sj["k"]
                meet = False
                for a in range(4):
                    for b in range(4):
                        if segs_meet(pk[a], pk[(a + 1) % 4], qk[b], qk[(b + 1) % 4]):
                            meet = True
                            break
                    if meet:
                        break
                if not meet:
                    meet = any(inside_closed(pk, p) for p in qk) or any(inside_closed(qk, p) for p in pk)
                clipped = clip(qk, pk)
                if not meet:
                    if clipped:
                        clip_disagreements.append((i, j))
                    d2 = min(
                        min(seg_dist2(p, qk[b], qk[(b + 1) % 4]) for p in pk for b in range(4)),
                        min(seg_dist2(p, pk[a], pk[(a + 1) % 4]) for p in qk for a in range(4)),
                    )
                    verdict = "separated"
                    close_dist2.append((d2, i, j))
                    if least_dist2 is None or d2 < least_dist2:
                        least_dist2 = d2
                        least_dist2_at = [(i, j)]
                    elif d2 == least_dist2:
                        least_dist2_at.append((i, j))
                else:
                    d2 = Q(0)
                    if not clipped:
                        clip_disagreements.append((i, j))
                    a2 = area2(clipped) if len(clipped) >= 3 else Q(0)
                    if a2 > 0:
                        verdict = "overlapping"
                        overlapping.append((i, j, f"{a2 / 2}"))
                    else:
                        verdict = "touching"
                        touching.append((i, j))
            if pairs_out is not None:
                d2s = "" if d2 is None else f"{d2.numerator}/{d2.denominator}"
                pairs_out.write(f"{i}\t{j}\t{best.numerator}/{best.denominator}\t{verdict}\t{d2s}\n")
    close_dist2.sort()
    accepted = not shape_failures and not wall_failures and not overlapping
    out = {
        "route": "E",
        "accepted": accepted,
        "n": n,
        "pairs_decided": npairs,
        "pairs_by_discs": far,
        "pairs_close": close,
        "shape_failures": shape_failures[:20],
        "tilt_kinds": tilt_kinds,
        "wall_failures": wall_failures[:20],
        "overlapping_pairs": overlapping[:20],
        "overlapping_count": len(overlapping),
        "touching_pairs": touching[:50],
        "touching_count": len(touching),
        "clip_disagreements": clip_disagreements[:20],
        "least_wall": least_wall,
        "per_square_wall_digest": wall_digest.hexdigest(),
        "per_pair_gap_digest": pair_digest.hexdigest(),
    }
    if least_dist2 is not None:
        out["least_distance_squared"] = {
            "distance_squared": f"{least_dist2.numerator}/{least_dist2.denominator}",
            "distance_approx": to_sci(math.isqrt(least_dist2.numerator * 10**80 // least_dist2.denominator), 10**40),
            "pairs": least_dist2_at,
        }
        out["closest_pairs_by_distance"] = [
            {
                "i": i,
                "j": j,
                "distance_squared": f"{d2.numerator}/{d2.denominator}",
                "distance_approx": to_sci(math.isqrt(d2.numerator * 10**80 // d2.denominator), 10**40),
            }
            for d2, i, j in close_dist2[:40]
        ]
    return out


# ---------------------------------------------------------------------------
# Self-test.
# ---------------------------------------------------------------------------


def _cert_text(n_side: str, rows: list[tuple[str, str, str]]) -> bytes:
    lines = ["# self-test", f"{len(rows)} {n_side}"] + [" ".join(r) for r in rows]
    return ("\n".join(lines) + "\n").encode()


def _decide(data: bytes) -> tuple[str, str]:
    cert = read_certificate(data)
    z = route_z(cert)
    e = route_e(cert)

    def kind(res):
        if res["wall_failures"] or res.get("shape_failures"):
            return "wall"
        if res["overlapping_count"]:
            return "overlap"
        if res["touching_count"]:
            return "touch"
        return "clear"

    return kind(z), kind(e)


def self_test() -> int:
    from fractions import Fraction as Q  # noqa: PLC0415

    failures = []
    hand_cases: list[str] = []

    def expect(name, data, want):
        hand_cases.append(name)
        try:
            got = _decide(data)
        except ReadError as exc:
            got = ("read", "read")
            detail = str(exc)
        else:
            detail = ""
        if got != (want, want):
            failures.append((name, want, got, detail))
        return got

    eps = "1/1000000000000000000000000000000"
    # 1. two aligned squares side by side, touching along an edge, in a 2 x 1 box... box 2
    expect("aligned-touch", _cert_text("2", [("1/2", "1/2", "0"), ("3/2", "1/2", "0")]), "touch")
    # 2. the same pushed 1e-30 into overlap (box widened so walls are fine)
    expect(
        "aligned-overlap",
        _cert_text("3", [("1/2", "1/2", "0"), (str(Q(3, 2) - Q(eps)), "1/2", "0")]),
        "overlap",
    )
    # 3. aligned, 1e-30 apart
    expect("aligned-clear", _cert_text("3", [("1/2", "1/2", "0"), (str(Q(3, 2) + Q(eps)), "1/2", "0")]), "clear")
    # 4. identical squares
    expect("identical", _cert_text("2", [("1/2", "1/2", "0"), ("1/2", "1/2", "0")]), "overlap")
    # 5. half-offset aligned squares (collinear edges, no proper crossing)
    expect("half-offset", _cert_text("3", [("1/2", "1/2", "0"), ("1", "1/2", "0")]), "overlap")
    # 6. corner-to-corner contact of aligned squares
    expect("corner-touch", _cert_text("2", [("1/2", "1/2", "0"), ("3/2", "3/2", "0")]), "touch")
    # 7. a square 1e-30 past the left wall (exact wall contact is tested below)
    expect("wall-past", _cert_text("1", [(str(Q(1, 2) - Q(eps)), "1/2", "0")]), "wall")
    expect("wall-past-tilted", _cert_text("4", [(str(Q(7, 10) - Q(eps)), "2", "1/2")]), "wall")
    expect("wall-touch-tilted", _cert_text("4", [("7/10", "2", "1/2")]), "clear")
    # 8. quarter turn written as t = 1 is aligned
    expect("t-one-touch", _cert_text("2", [("1/2", "1/2", "1"), ("3/2", "1/2", "-1")]), "touch")
    # 9. a 45-degree square (t = tan(22.5 deg) is irrational; use t = 1/2, 53.13 deg) touching an aligned one
    #    vertex-to-edge: square at (cx, cy) with half-extent h = (|a|+|b|)/(2d); t=1/2 -> a=3,b=4,d=5, h=7/10
    expect("vertex-edge-touch", _cert_text("4", [("1/2", "1", "0"), (str(Q(1) + Q(7, 10)), "1", "1/2")]), "touch")
    expect(
        "vertex-edge-overlap",
        _cert_text("4", [("1/2", "1", "0"), (str(Q(1) + Q(7, 10) - Q(eps)), "1", "1/2")]),
        "overlap",
    )
    # 10. vertex-vertex contact: two t=1/2 squares whose rightmost and leftmost vertices meet
    #     square at (c,1): rightmost vertex x = c + 7/10, y = 1 + y-offset of that vertex
    #     u=(3/5,4/5), v=(-4/5,3/5): corners c +- u/2 +- v/2; rightmost: +u/2 - v/2 = (3/10+4/10, 4/10-3/10) = (7/10, 1/10)
    #     leftmost of the second: -u/2 + v/2 = (-7/10, -1/10). Place second centre at (c + 14/10, 1 + 2/10).
    expect(
        "vertex-vertex-touch",
        _cert_text("5", [("1", "2", "1/2"), (str(Q(1) + Q(14, 10)), str(Q(2) + Q(2, 10)), "1/2")]),
        "touch",
    )
    # malformed texts: all must be refused by the reader
    malformed = {
        "decimal": b"1 2\n0.5 0.5 0\n",
        "wrong-count": b"2 2\n1/2 1/2 0\n",
        "extra-token": b"1 2\n1/2 1/2 0 0\n",
        "double-space": b"1 2\n1/2  1/2 0\n",
        "blank-line": b"1 2\n\n1/2 1/2 0\n",
        "comment-after-header": b"1 2\n# x\n1/2 1/2 0\n",
        "zero-den": b"1 2\n1/0 1/2 0\n",
        "negative-den": b"1 2\n1/-2 1/2 0\n",
        "plus-sign": b"1 2\n+1/2 1/2 0\n",
        "non-integer-n": b"1/1 2\n1/2 1/2 0\n",
        "nonpositive-side": b"1 0\n1/2 1/2 0\n",
        "crlf": b"1 2\r\n1/2 1/2 0\r\n",
        "unicode-digit": "1 2\n١/2 1/2 0\n".encode(),
    }
    for name, data in malformed.items():
        try:
            read_certificate(data)
        except (ReadError, UnicodeDecodeError):
            pass
        else:
            failures.append((name, "read", "accepted", ""))
    # exact wall contact: both routes must accept with every clearance exactly 0
    for name, text in (
        ("wall-touch-aligned", _cert_text("1", [("1/2", "1/2", "0")])),
        ("wall-touch-tilted-all", _cert_text("7/5", [("7/10", "7/10", "1/2")])),
    ):
        cert = read_certificate(text)
        z, e = route_z(cert), route_e(cert)
        zero = all(z["least_wall"][w]["clearance"] == "0/1" == e["least_wall"][w]["clearance"] for w in z["least_wall"])
        if not (z["accepted"] and e["accepted"] and zero):
            failures.append((name, "accept at 0", (z["accepted"], e["accepted"], zero), ""))

    # random pairs: both routes must classify alike; some built to touch, half of those pushed 1e-30 in
    rng = random.Random(20261023)
    built = 0
    tallies = {}
    for trial in range(2000):
        t1 = Q(rng.randint(-60, 60), rng.randint(1, 60))
        t2 = Q(rng.randint(-60, 60), rng.randint(1, 60))
        c1 = (Q(rng.randint(3000, 5000), 1000), Q(rng.randint(3000, 5000), 1000))
        mode = trial % 5
        if mode == 0:
            c2 = (c1[0] + Q(rng.randint(-2000, 2000), 1000), c1[1] + Q(rng.randint(-2000, 2000), 1000))
        else:
            # build a contact along one of square 1's axes
            built += 1
            w1 = 1 + t1 * t1
            u1 = ((1 - t1 * t1) / w1, 2 * t1 / w1)
            v1 = (-u1[1], u1[0])
            w2 = 1 + t2 * t2
            u2 = ((1 - t2 * t2) / w2, 2 * t2 / w2)
            v2 = (-u2[1], u2[0])
            axis, perp = (u1, v1) if rng.random() < 0.5 else (v1, (-u1[0], -u1[1]))
            hw2 = (abs(u2[0] * axis[0] + u2[1] * axis[1]) + abs(v2[0] * axis[0] + v2[1] * axis[1])) / 2
            # the vertex (or edge midpoint) of square 2 nearest square 1 along axis: offset along perp
            cands = []
            for su in (-1, 1):
                for sv in (-1, 1):
                    off = (Q(su, 2) * u2[0] + Q(sv, 2) * v2[0], Q(su, 2) * u2[1] + Q(sv, 2) * v2[1])
                    cands.append((off[0] * axis[0] + off[1] * axis[1], off[0] * perp[0] + off[1] * perp[1]))
            low = min(cands)[0]
            perp_off = min(p for a_, p in cands if a_ == low)
            if mode in (1, 2):
                shift = Q(rng.randint(-400, 400), 1000) - perp_off
            else:
                # the contact point at one of square 1's corners: degenerate contacts
                shift = Q(rng.choice((-1, 1)), 2) - perp_off
            dist = Q(1, 2) + hw2
            if mode in (2, 4):
                dist -= Q(1, 10**30)
            c2 = (c1[0] + dist * axis[0] + shift * perp[0], c1[1] + dist * axis[1] + shift * perp[1])
        rows = [(str(c1[0]), str(c1[1]), str(t1)), (str(c2[0]), str(c2[1]), str(t2))]
        data = _cert_text("100", rows)
        zk, ek = _decide(data)
        tallies[(mode, zk)] = tallies.get((mode, zk), 0) + 1
        if zk != ek:
            failures.append((f"random-{trial}", "agree", (zk, ek), ""))
        if mode in (1, 3) and zk != "touch":
            failures.append((f"random-built-touch-{trial}", "touch", (zk, ek), ""))
        if mode == 2 and zk != "overlap":
            failures.append((f"random-built-overlap-{trial}", "overlap", (zk, ek), ""))
    report = {
        "hand_built_cases": len(hand_cases) + 2,
        "malformed_texts": len(malformed),
        "random_pairs": 2000,
        "random_built_contacts": built,
        "tallies": {f"mode{m}:{k}": v for (m, k), v in sorted(tallies.items())},
        "failures": failures,
    }
    print(json.dumps(report, indent=2))
    return 0 if not failures else 1


# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cert", nargs="?")
    ap.add_argument("--route", choices=("Z", "E"))
    ap.add_argument("--receipt")
    ap.add_argument("--pairs")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not args.cert or not args.route:
        ap.error("CERT and --route are required")
    data = Path(args.cert).read_bytes()
    program = Path(__file__).read_bytes()
    t0 = time.process_time()
    w0 = time.perf_counter()
    try:
        cert = read_certificate(data)
    except ReadError as exc:
        print(f"UNREADABLE: {exc}")
        if args.receipt:
            Path(args.receipt).write_text(json.dumps({"readable": False, "reason": str(exc)}, indent=2) + "\n")
        return 2
    pairs_out = open(args.pairs, "w") if args.pairs else None  # noqa: SIM115
    try:
        res = route_z(cert, pairs_out) if args.route == "Z" else route_e(cert, pairs_out)
    finally:
        if pairs_out is not None:
            pairs_out.close()
    receipt = {
        "program": "review_t238_check.py",
        "program_sha256": hashlib.sha256(program).hexdigest(),
        "input_sha256": hashlib.sha256(data).hexdigest(),
        "python": platform.python_version(),
        "n": cert["n"],
        "side": canon(*cert["side"]),
        "comments": cert["comments"],
        "trailing_newline": cert["trailing_newline"],
        "result": res,
        "cpu_seconds": round(time.process_time() - t0, 3),
        "wall_seconds": round(time.perf_counter() - w0, 3),
    }
    if args.receipt:
        Path(args.receipt).write_text(json.dumps(receipt, indent=2) + "\n")
    verdict = "ACCEPTED" if res["accepted"] else "REFUSED"
    print(f"{verdict} route {args.route}: n = {cert['n']}, S = {canon(*cert['side'])}")
    print(f"  least walls: " + ", ".join(f"{w} {v['approx']} {v['squares'][:6]}" for w, v in res["least_wall"].items()))
    if args.route == "Z":
        print(f"  least gap {res['least_gap']['approx']} at {res['least_gap']['pairs'][:4]}; pairs {res['pairs_decided']}")
    else:
        print(f"  pairs {res['pairs_decided']}: {res['pairs_by_discs']} by discs, {res['pairs_close']} close")
        if "least_distance_squared" in res:
            print(f"  least distance {res['least_distance_squared']['distance_approx']} at {res['least_distance_squared']['pairs']}")
    print(f"  touching {res['touching_count']}, overlapping {res['overlapping_count']}; cpu {receipt['cpu_seconds']} s")
    return 0 if res["accepted"] else 1


if __name__ == "__main__":
    sys.exit(main())
