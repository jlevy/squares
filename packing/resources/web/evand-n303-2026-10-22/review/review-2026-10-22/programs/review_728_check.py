#!/usr/bin/env python3
"""Exact feasibility checker for an n-unit-square rational certificate (review of #728).

Written for the Stage 4 mathematical review of jlevy/squares issue #728 (lane
c-review-728-math). Standard library only; it imports nothing from the repository
and nothing from the certificate's source. The format was learned from the
certificate file and the issue text alone:

    # comment lines, only before the header
    n S          n a positive integer, S a positive rational literal (the box side)
    x y t        n rows of rational literals: (x, y) the centre and t = tan(theta/2),
                 so the square's edges run along u = ((1-t^2)/(1+t^2), 2t/(1+t^2))
                 and v = (-u_y, u_x), each exactly of unit length.

A rational literal is -?[0-9]+(/[0-9]+)? with a non-zero denominator. Decimals,
exponents, '+', underscores, tabs, CR and non-ASCII bytes are refused.

Route Z decides with integers only (the fractions module is never imported on it):
the Pythagorean triple of every row, containment of every square by its half-extent
(|a| + |b|) / (2d), and every one of the n(n-1)/2 pairs by the four-axis
separating-axis test with all denominators cleared. The pair gap is the largest
separation over the four edge-normal axes, as an exact rational.

Route C decides with fractions.Fraction: the four corners built from the half-angle
map, unit edges, right angles, positive orientation and corner mean, corner
containment, and every pair by the exact area that square i's four closed
half-planes clip from square j (positive if and only if the interiors meet). For
pairs whose centres lie within distance 2 it also computes the exact squared
Euclidean distance between the two squares.

The two routes share only the reader. Neither rounds, dilates, filters or
tolerates. Exit status: 0 accepted, 1 refused (geometry), 2 refused (reader).

Usage:
    python3 -I review_728_check.py --self-test
    python3 -I review_728_check.py CERT --route Z [--expect-side P/Q] [--out FILE.json]
    python3 -I review_728_check.py CERT --route C [--expect-side P/Q] [--out FILE.json]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import time

LITERAL = re.compile(r"-?[0-9]+(?:/[0-9]+)?")
COUNT = re.compile(r"[1-9][0-9]*")
WALLS = ("x>=0", "x<=S", "y>=0", "y<=S")


class CertificateError(ValueError):
    """The reader refuses the text."""


# ---------------------------------------------------------------- the reader (shared)


def read_literal(tok: str, where: str) -> tuple[int, int]:
    if not LITERAL.fullmatch(tok):
        raise CertificateError(f"{where}: not a rational literal: {tok[:40]!r}")
    if "/" in tok:
        a, b = tok.split("/")
        num, den = int(a), int(b)
    else:
        num, den = int(tok), 1
    if den == 0:
        raise CertificateError(f"{where}: zero denominator")
    g = math.gcd(num, den)
    return num // g, den // g


def read_certificate(data: bytes) -> dict:
    if any(byte > 126 or (byte < 32 and byte != 10) for byte in data):
        raise CertificateError("a byte outside printable ASCII and LF")
    text = data.decode("ascii")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    k = 0
    comments = 0
    while k < len(lines) and lines[k].startswith("#"):
        comments += 1
        k += 1
    if k == len(lines):
        raise CertificateError("no header line")
    head = lines[k].split(" ")
    if len(head) != 2 or not COUNT.fullmatch(head[0]):
        raise CertificateError(f"header is not 'n S': {lines[k][:60]!r}")
    n = int(head[0])
    side = read_literal(head[1], "header side")
    if side[0] <= 0:
        raise CertificateError("side is not positive")
    rows = []
    for line_no in range(k + 1, len(lines)):
        toks = lines[line_no].split(" ")
        if len(toks) != 3:
            raise CertificateError(f"line {line_no + 1}: {len(toks)} fields, not 3")
        rows.append(tuple(read_literal(t, f"line {line_no + 1}") for t in toks))
    if len(rows) != n:
        raise CertificateError(f"{len(rows)} square rows for n = {n}")
    return {
        "n": n,
        "side": side,
        "rows": rows,
        "comment_lines": comments,
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
    }


# ---------------------------------------------------------------- exact printing


def frac_str(num: int, den: int) -> str:
    if den < 0:
        num, den = -num, -den
    g = math.gcd(num, den)
    num, den = num // g, den // g
    return str(num) if den == 1 else f"{num}/{den}"


def sci(num: int, den: int, digits: int = 13) -> str:
    """num/den in scientific notation, truncated toward zero at `digits` significant digits."""
    if den < 0:
        num, den = -num, -den
    if num == 0:
        return "0"
    sign = "-" if num < 0 else ""
    num = abs(num)
    e = len(str(num)) - len(str(den))
    # adjust e so that 10^e <= num/den < 10^(e+1)
    while num * 10 ** max(0, -e) < den * 10 ** max(0, e):
        e -= 1
    while num * 10 ** max(0, -(e + 1)) >= den * 10 ** max(0, e + 1):
        e += 1
    shift = digits - 1 - e
    q = (num * 10**shift) // den if shift >= 0 else num // (den * 10 ** (-shift))
    s = str(q)
    return f"{sign}{s[0]}.{s[1:]}e{e:+d}"


def less(a: tuple[int, int], b: tuple[int, int]) -> bool:
    """a < b for rationals (num, den) with positive denominators."""
    return a[0] * b[1] < b[0] * a[1]


# ---------------------------------------------------------------- route Z: integers only


def route_z(cert: dict) -> dict:
    n = cert["n"]
    sn, sd = cert["side"]
    sq = []
    for (xn, xd), (yn, yd), (p, q) in cert["rows"]:
        a, b, d = q * q - p * p, 2 * p * q, q * q + p * p
        if d <= 0 or a * a + b * b != d * d:
            raise AssertionError("not a Pythagorean triple")
        sq.append((xn, xd, yn, yd, a, b, d, abs(a) + abs(b)))

    # walls: clearance of square i from wall w, exactly, as (num, den), den > 0
    least_wall = None
    wall_contacts, wall_violations = [], []
    for i, (xn, xd, yn, yd, a, b, d, e) in enumerate(sq):
        clear = (
            (2 * d * xn - e * xd, 2 * d * xd),
            (2 * d * xd * sn - 2 * d * xn * sd - e * xd * sd, 2 * d * xd * sd),
            (2 * d * yn - e * yd, 2 * d * yd),
            (2 * d * yd * sn - 2 * d * yn * sd - e * yd * sd, 2 * d * yd * sd),
        )
        for w, c in enumerate(clear):
            if c[0] == 0:
                wall_contacts.append((i, WALLS[w]))
            elif c[0] < 0:
                wall_violations.append((i, WALLS[w], frac_str(*c)))
            if least_wall is None or less(c, least_wall[0]):
                least_wall = (c, i, WALLS[w])

    # pairs: every one of n(n-1)/2, four axes, denominators cleared
    sig = hashlib.sha256()
    pairs = 0
    near = 0
    touching, overlapping = [], []
    smallest = []  # (gap, i, j, axis) for the ten least gaps
    axis_names = ("u_i", "v_i", "u_j", "v_j")
    for i in range(n):
        xni, xdi, yni, ydi, ai, bi, di, _ = sq[i]
        for j in range(i + 1, n):
            xnj, xdj, ynj, ydj, aj, bj, dj, _ = sq[j]
            dxp = xdi * xdj
            dyp = ydi * ydj
            P = (xnj * xdi - xni * xdj) * dyp
            Q = (ynj * ydi - yni * ydj) * dxp
            L = (
                2 * dj * abs(ai * P + bi * Q),
                2 * dj * abs(-bi * P + ai * Q),
                2 * di * abs(aj * P + bj * Q),
                2 * di * abs(-bj * P + aj * Q),
            )
            C = ai * aj + bi * bj
            S = ai * bj - bi * aj
            m = dxp * dyp
            R = m * (di * dj + abs(C) + abs(S))
            k = max(range(4), key=L.__getitem__)
            G = L[k] - R
            den = 2 * di * dj * m
            pairs += 1
            if P * P + Q * Q < 2 * m * m:
                near += 1
            sign = 1 if G > 0 else (0 if G == 0 else -1)
            sig.update(f"{i},{j},{sign}\n".encode())
            if sign == 0:
                touching.append((i, j))
            elif sign < 0:
                overlapping.append((i, j, frac_str(G, den)))
            entry = ((G, den), i, j, axis_names[k])
            if len(smallest) < 10 or less(entry[0], smallest[-1][0]):
                smallest = sort_exact(smallest + [entry])[:10]

    accepted = not wall_violations and not overlapping
    lw = least_wall
    if not smallest:
        smallest = [((0, 1), None, None, None)]  # n = 1: no pairs, no gap
    out = {
        "route": "Z (integers only)",
        "n": n,
        "side": frac_str(sn, sd),
        "pythagorean_rows": n,
        "least_wall_clearance": frac_str(*lw[0]),
        "least_wall_clearance_sci": sci(*lw[0]),
        "least_wall_square": lw[1],
        "least_wall": lw[2],
        "least_clearance_by_wall": least_by_wall_z(sq, sn, sd),
        "wall_contacts": len(wall_contacts),
        "wall_contact_list": wall_contacts[:50],
        "wall_violations": wall_violations[:50],
        "wall_violation_count": len(wall_violations),
        "pairs_decided": pairs,
        "centre_pairs_within_sqrt2": near,
        "touching_pairs": touching,
        "overlapping_pair_count": len(overlapping),
        "overlapping_pairs": overlapping[:50],
        "least_gap": frac_str(*smallest[0][0]) if pairs else None,
        "least_gap_sci": sci(*smallest[0][0]),
        "least_gap_pair": [smallest[0][1], smallest[0][2]],
        "least_gap_axis": smallest[0][3],
        "ten_least_gaps": [
            {"pair": [i, j], "gap": frac_str(*g), "gap_sci": sci(*g), "axis": ax}
            for g, i, j, ax in smallest
        ],
        "pair_sign_digest": sig.hexdigest(),
        "accepted": accepted,
    }
    return out


def sort_exact(entries: list) -> list:
    """Sort (num, den)-keyed entries exactly (insertion sort; the lists are short)."""
    res: list = []
    for e in entries:
        pos = len(res)
        while pos > 0 and less(e[0], res[pos - 1][0]):
            pos -= 1
        res.insert(pos, e)
    return res


def least_by_wall_z(sq: list, sn: int, sd: int) -> dict:
    best: dict = {}
    for i, (xn, xd, yn, yd, a, b, d, e) in enumerate(sq):
        clear = (
            (2 * d * xn - e * xd, 2 * d * xd),
            (2 * d * xd * sn - 2 * d * xn * sd - e * xd * sd, 2 * d * xd * sd),
            (2 * d * yn - e * yd, 2 * d * yd),
            (2 * d * yd * sn - 2 * d * yn * sd - e * yd * sd, 2 * d * yd * sd),
        )
        for w, c in enumerate(clear):
            if WALLS[w] not in best or less(c, best[WALLS[w]][0]):
                best[WALLS[w]] = (c, i)
    return {w: {"clearance": frac_str(*c), "sci": sci(*c), "square": i} for w, (c, i) in best.items()}


# ---------------------------------------------------------------- route C: Fraction, clipping area


def route_c(cert: dict) -> dict:
    from fractions import Fraction as F

    n = cert["n"]
    S = F(*cert["side"])
    half = F(1, 2)
    squares = []
    for (xn, xd), (yn, yd), (p, q) in cert["rows"]:
        cx, cy, t = F(xn, xd), F(yn, yd), F(p, q)
        co = (1 - t * t) / (1 + t * t)
        si = 2 * t / (1 + t * t)
        ux, uy, vx, vy = co, si, -si, co
        corners = [
            (cx - half * ux - half * vx, cy - half * uy - half * vy),
            (cx + half * ux - half * vx, cy + half * uy - half * vy),
            (cx + half * ux + half * vx, cy + half * uy + half * vy),
            (cx - half * ux + half * vx, cy - half * uy + half * vy),
        ]
        for k in range(4):
            a0, a1, a2 = corners[k], corners[(k + 1) % 4], corners[(k + 2) % 4]
            e1 = (a1[0] - a0[0], a1[1] - a0[1])
            e2 = (a2[0] - a1[0], a2[1] - a1[1])
            if e1[0] * e1[0] + e1[1] * e1[1] != 1:
                raise AssertionError("edge not of unit length")
            if e1[0] * e2[0] + e1[1] * e2[1] != 0:
                raise AssertionError("corner not a right angle")
            if e1[0] * e2[1] - e1[1] * e2[0] != 1:
                raise AssertionError("corners not positively oriented")
        if sum(c[0] for c in corners) / 4 != cx or sum(c[1] for c in corners) / 4 != cy:
            raise AssertionError("corner mean is not the centre")
        squares.append(((cx, cy), corners))

    # walls: per square and wall, the least corner clearance
    least = None
    by_wall: dict = {}
    wall_contacts, wall_violations = [], []
    for i, (_, corners) in enumerate(squares):
        vals = (
            min(c[0] for c in corners),
            min(S - c[0] for c in corners),
            min(c[1] for c in corners),
            min(S - c[1] for c in corners),
        )
        for w, v in enumerate(vals):
            if v == 0:
                wall_contacts.append((i, WALLS[w]))
            elif v < 0:
                wall_violations.append((i, WALLS[w], str(v)))
            if least is None or v < least[0]:
                least = (v, i, WALLS[w])
            if WALLS[w] not in by_wall or v < by_wall[WALLS[w]][0]:
                by_wall[WALLS[w]] = (v, i)

    def clip(subject: list, clipper: list, order: list) -> list:
        poly = subject
        for k in order:
            if not poly:
                break
            A = clipper[k]
            B = clipper[(k + 1) % 4]
            ex, ey = B[0] - A[0], B[1] - A[1]
            f = [ex * (P[1] - A[1]) - ey * (P[0] - A[0]) for P in poly]
            out = []
            m = len(poly)
            for idx in range(m):
                P, Q = poly[idx], poly[(idx + 1) % m]
                fp, fq = f[idx], f[(idx + 1) % m]
                if fp >= 0:
                    out.append(P)
                if (fp > 0 and fq < 0) or (fp < 0 and fq > 0):
                    s = fp / (fp - fq)
                    out.append((P[0] + s * (Q[0] - P[0]), P[1] + s * (Q[1] - P[1])))
            poly = out
        return poly

    def twice_area(poly: list) -> F:
        m = len(poly)
        return sum(
            (poly[k][0] * poly[(k + 1) % m][1] - poly[(k + 1) % m][0] * poly[k][1] for k in range(m)),
            F(0),
        )

    def seg_d2(P: tuple, A: tuple, B: tuple) -> F:
        ex, ey = B[0] - A[0], B[1] - A[1]  # |e| = 1 exactly, checked above
        wx, wy = P[0] - A[0], P[1] - A[1]
        s = wx * ex + wy * ey
        if s < 0:
            s = F(0)
        elif s > 1:
            s = F(1)
        dx, dy = wx - s * ex, wy - s * ey
        return dx * dx + dy * dy

    sig = hashlib.sha256()
    pairs = 0
    near = 0
    within2 = 0
    touching, overlapping = [], []
    least_d2 = None
    for i in range(n):
        ci, Ki = squares[i]
        # outward normal of edge k (corner k to k+1, interior on the left) is (e_y, -e_x)
        normals = []
        for k in range(4):
            A, B = Ki[k], Ki[(k + 1) % 4]
            normals.append((B[1] - A[1], -(B[0] - A[0])))
        for j in range(i + 1, n):
            cj, Kj = squares[j]
            dx, dy = cj[0] - ci[0], cj[1] - ci[1]
            # clip first by the half-plane facing j: an ordering only, every pair is clipped
            order = sorted(range(4), key=lambda k: -(normals[k][0] * dx + normals[k][1] * dy))
            poly = clip(Kj, Ki, order)
            area2 = twice_area(poly) if poly else F(0)
            if area2 < 0:
                raise AssertionError("clipped polygon lost its orientation")
            pairs += 1
            cd2 = dx * dx + dy * dy
            if cd2 < 2:
                near += 1
            if area2 > 0:
                sign = -1
                overlapping.append((i, j, str(area2 / 2)))
            elif poly:
                sign = 0
                touching.append((i, j))
            else:
                sign = 1
            sig.update(f"{i},{j},{sign}\n".encode())
            if sign >= 0 and cd2 <= 4:
                within2 += 1
                d2 = min(
                    min(seg_d2(P, Ki[k], Ki[(k + 1) % 4]) for P in Kj for k in range(4)),
                    min(seg_d2(P, Kj[k], Kj[(k + 1) % 4]) for P in Ki for k in range(4)),
                )
                if least_d2 is None or d2 < least_d2[0]:
                    least_d2 = (d2, i, j)

    accepted = not wall_violations and not overlapping
    v, wi, ww = least
    out = {
        "route": "C (Fraction, clipping area)",
        "n": n,
        "side": str(S),
        "unit_square_rows": n,
        "least_wall_clearance": str(v),
        "least_wall_clearance_sci": sci(v.numerator, v.denominator),
        "least_wall_square": wi,
        "least_wall": ww,
        "least_clearance_by_wall": {
            w: {"clearance": str(c), "sci": sci(c.numerator, c.denominator), "square": i}
            for w, (c, i) in by_wall.items()
        },
        "wall_contacts": len(wall_contacts),
        "wall_contact_list": wall_contacts[:50],
        "wall_violations": wall_violations[:50],
        "wall_violation_count": len(wall_violations),
        "pairs_decided": pairs,
        "centre_pairs_within_sqrt2": near,
        "pairs_within_2_distance_computed": within2,
        "touching_pairs": touching,
        "overlapping_pair_count": len(overlapping),
        "overlapping_pairs": overlapping[:50],
        "least_squared_distance": None if least_d2 is None else str(least_d2[0]),
        "least_distance_sci": None
        if least_d2 is None
        else sci(math.isqrt(least_d2[0].numerator * 10**80 // least_d2[0].denominator), 10**40),
        "least_distance_pair": None if least_d2 is None else [least_d2[1], least_d2[2]],
        "pair_sign_digest": sig.hexdigest(),
        "accepted": accepted,
    }
    return out


# ---------------------------------------------------------------- self-test

E30 = 10**30


def cert_text(side: str, rows: list[str], comment: bool = True) -> bytes:
    head = "# hand-built test certificate\n" if comment else ""
    return (head + f"{len(rows)} {side}\n" + "".join(r + "\n" for r in rows)).encode()


def self_test() -> int:
    from fractions import Fraction as F  # used only to build test literals

    def lit(x: F) -> str:
        return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"

    # only-one-axis separating case: j turned by t = 2/5, (c, s) = (21/29, 20/29)
    def axis_case(g: F, swap: bool) -> bytes:
        k = F(41, 58) + F(1, 2) + g
        jx, jy = 2 + k * F(21, 29), 2 + k * F(20, 29)
        rows = ["2 2 0", f"{lit(jx)} {lit(jy)} 2/5"]
        if swap:
            rows.reverse()
        return cert_text("4", rows)

    tilted_j = F(11, 5)
    cases = [
        # name, text, expected acceptance, expected least gap (or None), expected least clearance, pair contacts
        ("feasible, apart", cert_text("4", ["1 1 0", "5/2 5/2 0"]), True, "1/2", "1/2", 0),
        ("feasible, edge contact", cert_text("2", ["1/2 1/2 0", "3/2 1/2 0"]), True, "0", "0", 1),
        ("feasible, tilted vertex on edge", cert_text("3", ["1 1 0", "11/5 1 1/2"]), True, "0", "1/10", 1),
        (
            "overlap by 1e-30, tilted vertex",
            cert_text("3", ["1 1 0", f"{lit(tilted_j - F(1, E30))} 1 1/2"]),
            False,
            f"-1/{E30}",
            lit(F(1, 10) + F(1, E30)),
            0,
        ),
        ("feasible, tilted, four wall contacts", cert_text("7/5", ["7/10 7/10 1/2"]), True, None, "0", 0),
        (
            "wall crossed by 1e-30, tilted",
            cert_text(lit(F(7, 5) - F(1, E30)), ["7/10 7/10 1/2"]),
            False,
            None,
            f"-1/{E30}",
            0,
        ),
        ("duplicated square", cert_text("3", ["1 1 1/3", "1 1 1/3"]), False, "-1", None, 0),
        ("only u_j separates, gap 1/100", axis_case(F(1, 100), False), True, "1/100", None, 0),
        ("only u_i separates (swapped), gap 1/100", axis_case(F(1, 100), True), True, "1/100", None, 0),
        ("only u_j separates, contact", axis_case(F(0), False), True, "0", None, 1),
        ("only u_j separates, past contact by 1e-30", axis_case(-F(1, E30), False), False, f"-1/{E30}", None, 0),
        ("quarter turn t = 1 equals t = 0", cert_text("2", ["1/2 1/2 1", "3/2 1/2 0"]), True, "0", "0", 1),
        ("corner to corner point contact", cert_text("2", ["1/2 1/2 0", "3/2 3/2 1"]), True, "0", "0", 1),
    ]
    reader_cases = [
        ("row count below n", b"3 4\n1 1 0\n2 2 0\n"),
        ("decimal literal", b"1 2\n0.5 1 0\n"),
        ("zero denominator", b"1 2\n1/0 1 0\n"),
        ("plus sign", b"1 2\n+1 1 0\n"),
        ("four fields", b"1 2\n1 1 0 0\n"),
        ("blank line", b"1 2\n\n1 1 0\n"),
        ("CRLF", b"1 2\r\n1 1 0\r\n"),
        ("tab separator", b"1 2\n1\t1 0\n"),
        ("comment after header", b"1 2\n# x\n1 1 0\n"),
        ("non-positive side", b"1 0\n1 1 0\n"),
        ("exponent", b"1 2\n1e0 1 0\n"),
        ("underscore digit group", b"1 2\n1_0/10 1 0\n"),
        ("Unicode digit", "1 2\n١ 1 0\n".encode()),
    ]
    failures = 0
    print("Z prints the least separating-axis gap; C prints the least squared distance (6 digits, truncated).")
    print(f"{'case':48} {'route':5} {'accepted':8} {'least gap / dist^2':>22} {'least clearance':>22} touch")
    for name, text, exp_ok, exp_gap, exp_clear, exp_touch in cases:
        cert = read_certificate(text)
        for route in (route_z, route_c):
            r = route(cert)
            tag = "Z" if route is route_z else "C"
            ok = r["accepted"] == exp_ok and len(r["touching_pairs"]) == exp_touch
            gap = r.get("least_gap") if tag == "Z" else None
            if tag == "Z" and exp_gap is not None and cert["n"] > 1:
                ok = ok and gap == exp_gap
            if exp_clear is not None:
                ok = ok and r["least_wall_clearance"] == exp_clear
            if tag == "C" and exp_gap is not None and cert["n"] > 1:
                g = F(exp_gap)
                if g < 0:
                    ok = ok and r["overlapping_pair_count"] == 1
                elif g == 0:
                    ok = ok and r["least_squared_distance"] == "0"
                elif name.startswith("only"):
                    ok = ok and F(r["least_squared_distance"]) == g * g
            failures += 0 if ok else 1
            shown = gap if tag == "Z" else r["least_squared_distance"]
            shown = "-" if shown is None else sci(F(shown).numerator, F(shown).denominator, 6)
            clear = sci(F(r["least_wall_clearance"]).numerator, F(r["least_wall_clearance"]).denominator, 6)
            print(
                f"{name:48} {tag:5} {str(r['accepted']):8} {shown:>22} "
                f"{clear:>22} {len(r['touching_pairs'])}  {'ok' if ok else 'MISMATCH'}"
            )
    for name, text in reader_cases:
        try:
            read_certificate(text)
        except CertificateError as exc:
            print(f"{name:48} {'read':5} refused: {exc}  ok")
        else:
            failures += 1
            print(f"{name:48} {'read':5} READ  MISMATCH")
    failures += random_agreement(F)
    print("self-test:", "PASS" if failures == 0 else f"FAIL ({failures})")
    return 0 if failures == 0 else 1


def random_agreement(F) -> int:
    """Route Z and route C agree on 3000 random pairs, a third of them built to touch."""
    import random

    rng = random.Random(728)
    bad = 0
    counts = {1: 0, 0: 0, -1: 0}
    for trial in range(3000):
        t1 = F(rng.randint(-40, 40), rng.randint(1, 40))
        t2 = F(rng.randint(-40, 40), rng.randint(1, 40))
        c1 = (F(4), F(4))
        ang = F(rng.randint(-60, 60), rng.randint(1, 30))
        cos_, sin_ = (1 - ang * ang) / (1 + ang * ang), 2 * ang / (1 + ang * ang)
        if trial % 3 == 0:
            # build a contact: put j along an edge normal of i (or of j) at exactly zero separation
            u = ((1 - t1 * t1) / (1 + t1 * t1), 2 * t1 / (1 + t1 * t1))
            co = ((1 - t1 * t1) * (1 - t2 * t2) + 4 * t1 * t2) / ((1 + t1 * t1) * (1 + t2 * t2))
            sn = (2 * t2 * (1 - t1 * t1) - 2 * t1 * (1 - t2 * t2)) / ((1 + t1 * t1) * (1 + t2 * t2))
            r = F(1, 2) + (abs(co) + abs(sn)) / 2
            lateral = F(rng.randint(-30, 30), 40)
            v = (-u[1], u[0])
            c2 = (c1[0] + r * u[0] + lateral * v[0], c1[1] + r * u[1] + lateral * v[1])
        else:
            rad = F(rng.randint(0, 260), 100)
            c2 = (c1[0] + rad * cos_, c1[1] + rad * sin_)

        def lit(x):
            return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"

        text = cert_text("8", [f"{lit(c1[0])} {lit(c1[1])} {lit(t1)}", f"{lit(c2[0])} {lit(c2[1])} {lit(t2)}"], False)
        cert = read_certificate(text)
        z, c = route_z(cert), route_c(cert)
        sz = 0 if z["touching_pairs"] else (-1 if z["overlapping_pair_count"] else 1)
        sc = 0 if c["touching_pairs"] else (-1 if c["overlapping_pair_count"] else 1)
        counts[sz] += 1
        if sz != sc or z["pair_sign_digest"] != c["pair_sign_digest"]:
            bad += 1
        if sz == 1 and c["least_squared_distance"] is not None:
            g = F(z["least_gap"])
            if F(c["least_squared_distance"]) < g * g:
                bad += 1  # the separating-axis gap can never exceed the distance
    print(
        f"random agreement: 3000 pairs, apart {counts[1]}, touching {counts[0]}, overlapping {counts[-1]}, "
        f"disagreements {bad}"
    )
    return bad


# ---------------------------------------------------------------- main


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cert", nargs="?")
    ap.add_argument("--route", choices=("Z", "C"))
    ap.add_argument("--expect-side")
    ap.add_argument("--out")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.cert or not args.route:
        ap.error("CERT and --route are required")
    with open(args.cert, "rb") as fh:
        data = fh.read()
    t0 = time.process_time()
    try:
        cert = read_certificate(data)
    except CertificateError as exc:
        print(json.dumps({"accepted": False, "reader": f"refused: {exc}"}))
        return 2
    if args.route == "Z":
        result = route_z(cert)
        if "fractions" in sys.modules:
            raise AssertionError("route Z must not load the fractions module")
        result["fractions_module_loaded"] = False
    else:
        result = route_c(cert)
    result["certificate_sha256"] = cert["sha256"]
    result["certificate_bytes"] = cert["bytes"]
    result["comment_lines"] = cert["comment_lines"]
    if args.expect_side is not None:
        want = read_literal(args.expect_side, "--expect-side")
        result["side_equals_claim"] = want == cert["side"]
        if not result["side_equals_claim"]:
            result["accepted"] = False
    result["cpu_seconds"] = round(time.process_time() - t0, 2)
    result["python"] = sys.version.split()[0]
    text = json.dumps(result, indent=1)
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(text + "\n")
    summary = {
        k: result[k]
        for k in (
            "route",
            "n",
            "side",
            "accepted",
            "least_wall_clearance_sci",
            "least_wall_square",
            "least_wall",
            "wall_contacts",
            "wall_violation_count",
            "pairs_decided",
            "overlapping_pair_count",
            "centre_pairs_within_sqrt2",
            "pair_sign_digest",
            "cpu_seconds",
        )
    }
    summary["touching_pairs"] = len(result["touching_pairs"])
    if args.route == "Z":
        summary["least_gap_sci"] = result["least_gap_sci"]
        summary["least_gap_pair"] = result["least_gap_pair"]
    else:
        summary["least_distance_sci"] = result["least_distance_sci"]
        summary["least_distance_pair"] = result["least_distance_pair"]
    if "side_equals_claim" in result:
        summary["side_equals_claim"] = result["side_equals_claim"]
    print(json.dumps(summary, indent=1))
    return 0 if result["accepted"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
