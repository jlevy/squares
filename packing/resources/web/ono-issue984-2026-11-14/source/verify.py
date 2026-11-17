#!/usr/bin/env python3
"""
Certified verifier: n unit squares packed in a square of side S.

THIS FILE IS THE SOLE AUTHORITY. It is frozen: agents must not edit it.
Its SHA-256 is recorded in VERIFIER.sha256 (and held by the human).

Exact rational arithmetic only (fractions.Fraction). No floats anywhere in
the decision path.

Certificate format (JSON):
{
  "n": 17,
  "side": "4.6756",                 # rational: int, "p/q" or decimal string
  "squares": [
    {"cx": "1/2", "cy": "1/2", "t": "0"},          # rotation via t = tan(theta/2)
    {"cx": "...", "cy": "...", "c": "3/5", "s": "4/5"}  # or explicit (cos, sin), c^2+s^2 == 1
  ]
}
JSON floats are REJECTED (they are not exact). Use strings.

Rotation: with rational t, cos = (1-t^2)/(1+t^2), sin = 2t/(1+t^2) is an exact
rational point on the unit circle, so every vertex is rational. Rational points
are dense on the circle, so any packing with strict slack has such a certificate.

Checks:
  1. exactly n squares, all unit side (c^2 + s^2 == 1 exactly)
  2. every vertex in [0, S] x [0, S]
  3. interiors pairwise disjoint (touching allowed), via the separating axis
     theorem on the edge normals of both squares (sufficient and necessary for
     closed convex polygons whose interiors are disjoint)

Usage:
  python3 verify.py cert.json
  python3 verify.py cert.json --compare records.json
Exit code 0 = VALID (and, with --compare, regardless of record status).
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction as F

HALF = F(1, 2)


class CertError(Exception):
    pass


def q(x, what: str) -> F:
    if isinstance(x, bool):
        raise CertError(f"{what}: booleans not allowed")
    if isinstance(x, int):
        return F(x)
    if isinstance(x, str):
        try:
            return F(x.strip())
        except (ValueError, ZeroDivisionError) as e:
            raise CertError(f"{what}: cannot parse {x!r} as rational ({e})")
    raise CertError(f"{what}: must be int or string, got {type(x).__name__} "
                    f"(JSON floats are not exact and are rejected)")


def rotation(sq: dict, i: int) -> tuple[F, F]:
    has_t = "t" in sq
    has_cs = "c" in sq or "s" in sq
    if has_t and has_cs:
        raise CertError(f"square {i}: give either t or (c, s), not both")
    if has_t:
        t = q(sq["t"], f"square {i}.t")
        d = 1 + t * t
        return (1 - t * t) / d, 2 * t / d
    if "c" in sq and "s" in sq:
        c, s = q(sq["c"], f"square {i}.c"), q(sq["s"], f"square {i}.s")
        if c * c + s * s != 1:
            raise CertError(f"square {i}: c^2 + s^2 != 1 exactly (not a unit square)")
        return c, s
    return F(1), F(0)  # axis-aligned if no rotation given


class Sq:
    __slots__ = ("cx", "cy", "c", "s", "hx", "hy", "verts")

    def __init__(self, cx: F, cy: F, c: F, s: F):
        self.cx, self.cy, self.c, self.s = cx, cy, c, s
        self.hx = (c * HALF, s * HALF)      # half edge along local x
        self.hy = (-s * HALF, c * HALF)     # half edge along local y
        self.verts = [
            (cx + a * self.hx[0] + b * self.hy[0], cy + a * self.hx[1] + b * self.hy[1])
            for a in (1, -1) for b in (1, -1)
        ]

    def axes(self):
        return [(self.c, self.s), (-self.s, self.c)]

    def proj(self, ax):
        m = self.cx * ax[0] + self.cy * ax[1]
        r = abs(self.hx[0] * ax[0] + self.hx[1] * ax[1]) + abs(self.hy[0] * ax[0] + self.hy[1] * ax[1])
        return m - r, m + r


def interiors_disjoint(a: Sq, b: Sq) -> bool:
    dx, dy = a.cx - b.cx, a.cy - b.cy
    if dx * dx + dy * dy >= 2:  # circumradii sqrt(2)/2 each: cannot overlap
        return True
    for ax in a.axes() + b.axes():
        lo1, hi1 = a.proj(ax)
        lo2, hi2 = b.proj(ax)
        if hi1 <= lo2 or hi2 <= lo1:
            return True
    return False


def _reject_float(s: str):
    raise CertError(f"JSON float {s} found; write numbers as strings for exactness")


def load(path: str) -> dict:
    with open(path) as f:
        return json.load(f, parse_float=_reject_float)


def build(cert: dict) -> tuple[int, F, list[Sq]]:
    n = cert.get("n")
    if not isinstance(n, int) or n < 1:
        raise CertError("'n' must be a positive integer")
    S = q(cert.get("side"), "side")
    raw = cert.get("squares")
    if not isinstance(raw, list) or len(raw) != n:
        raise CertError(f"expected exactly n={n} squares, got {len(raw) if isinstance(raw, list) else raw!r}")
    sqs = []
    for i, sq in enumerate(raw):
        c, s = rotation(sq, i)
        sqs.append(Sq(q(sq.get("cx"), f"square {i}.cx"), q(sq.get("cy"), f"square {i}.cy"), c, s))
    return n, S, sqs


def check(n: int, S: F, sqs: list[Sq]) -> list[str]:
    errors = []
    for i, sq in enumerate(sqs):
        for (x, y) in sq.verts:
            if not (0 <= x <= S and 0 <= y <= S):
                errors.append(f"square {i}: vertex ({float(x):.9f}, {float(y):.9f}) outside [0, S]^2")
                break
    # sort by cx so the pair loop can stop early (|dx| >= sqrt(2) => disjoint)
    order = sorted(range(n), key=lambda k: sqs[k].cx)
    for a_i in range(n):
        A = sqs[order[a_i]]
        for b_i in range(a_i + 1, n):
            B = sqs[order[b_i]]
            dx = B.cx - A.cx
            if dx * dx >= 2:
                break
            if not interiors_disjoint(A, B):
                errors.append(f"squares {order[a_i]} and {order[b_i]} overlap")
    return errors


def decimal(x: F, digits: int = 15) -> str:
    sign = "-" if x < 0 else ""
    x = abs(x)
    ip = x.numerator // x.denominator
    frac = x - ip
    ds = []
    for _ in range(digits):
        frac *= 10
        d = frac.numerator // frac.denominator
        ds.append(str(d))
        frac -= d
    return f"{sign}{ip}." + "".join(ds) + ("…" if frac else "")


def compare(n: int, S: F, records_path: str) -> str:
    with open(records_path) as f:
        recs = json.load(f, parse_float=str)
    entry = next((r for r in recs.get("records", []) if r.get("n") == n), None)
    if entry is None:
        return f"no record for n={n} in {records_path}"
    if entry.get("proven_optimal"):
        return f"n={n} is marked PROVEN OPTIMAL in records; an improvement is impossible (check your certificate and the record)"
    val = str(entry.get("upper"))
    rec = F(val)
    # published decimals may be rounded: the true record is >= shown - half ulp
    if "." in val:
        k = len(val.split(".")[1])
        floor_rec = rec - F(5, 10 ** (k + 1))
    else:
        floor_rec = rec
    if entry.get("upper_truncated_down"):  # value is the record truncated toward zero (true record >= value)
        floor_rec = rec
    if S < floor_rec:
        return (f"*** CERTIFIED IMPROVEMENT *** S = {decimal(S)} < record lower edge {decimal(floor_rec)} "
                f"(published {val}, source: {entry.get('source')})")
    if S < rec:
        return (f"S = {decimal(S)} is below the published {val} but within its rounding; "
                f"obtain the record's exact value before claiming anything")
    return f"does not beat record: S = {decimal(S)} >= {val}"


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    try:
        cert = load(argv[1])
        n, S, sqs = build(cert)
        errors = check(n, S, sqs)
    except (CertError, OSError, json.JSONDecodeError) as e:
        print(f"INVALID: {e}")
        return 1
    if errors:
        print(f"INVALID: {len(errors)} problem(s)")
        for e in errors[:20]:
            print("  -", e)
        return 1
    print(f"VALID  n={n}  S={decimal(S)}  (exact: {S.numerator}/{S.denominator})")
    if len(argv) >= 4 and argv[2] == "--compare":
        print(compare(n, S, argv[3]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
