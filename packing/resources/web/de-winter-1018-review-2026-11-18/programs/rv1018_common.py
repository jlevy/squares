"""Shared readers and exact geometry for the blind review of jlevy/squares#1018.

Lane r108-1118. Written from the mathematics of the issue's argument and the format's
stated meaning (a format M file: rows [x0, y0, x1, y1] with mass m, each spread evenly
over its eight images under the symmetry group D4 of K = [0, L]^2). It imports nothing
from jlevy/squares or from the source, and reads every file it is given as data.

Exact arithmetic is gmpy2's mpq (GMP rationals) and Python's Fraction; floats appear
only in the clearly marked search helpers, which decide nothing.
"""

from __future__ import annotations

import hashlib
import json
import re
import zlib
from fractions import Fraction
from pathlib import Path

import gmpy2
import numpy as np
from gmpy2 import mpq

MEASURE_KEYS = {"n", "L", "B", "proof_net", "total_mass", "points", "rectangles"}
NET_KEYS = {"step", "last"}
ROW_KEYS = {"rectangle", "mass"}
_NUM = re.compile(r"^-?(?:\d+/\d+|\d+\.\d+|\d+)$")


class FormatError(ValueError):
    """A file that this review's strict reader refuses."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_one_member(path: str | Path) -> tuple[bytes, bytes]:
    """Return (stored bytes, payload). A gzip file must be exactly one member."""
    raw = Path(path).read_bytes()
    if raw[:2] != b"\x1f\x8b":
        return raw, raw
    d = zlib.decompressobj(wbits=31)
    out = d.decompress(raw) + d.flush()
    if not d.eof or d.unused_data:
        raise FormatError(f"{path}: not exactly one gzip member")
    return raw, out


def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    keys = [k for k, _ in pairs]
    if len(keys) != len(set(keys)):
        raise FormatError(f"duplicate key among {sorted(keys)}")
    return dict(pairs)


def _no_float(tok: str) -> object:
    raise FormatError(f"float token {tok!r}")


def _no_const(tok: str) -> object:
    raise FormatError(f"constant {tok!r}")


def loads_strict(text: bytes | str) -> object:
    """JSON with no duplicate key, no float token and no NaN or Infinity."""
    return json.loads(
        text, object_pairs_hook=_pairs, parse_float=_no_float, parse_constant=_no_const
    )


def num(v: object) -> Fraction:
    """An exact number: a JSON integer, or a string p/q, a decimal or an integer."""
    if isinstance(v, bool):
        raise FormatError(f"boolean where a number is required: {v!r}")
    if isinstance(v, int):
        return Fraction(v)
    if isinstance(v, str) and _NUM.match(v):
        return Fraction(v)
    raise FormatError(f"not an exact number: {v!r}")


def read_measure(path: str | Path) -> dict[str, object]:
    """Read a format M rectangle measure strictly. Rows keep their file order."""
    raw, payload = read_one_member(path)
    obj = loads_strict(payload)
    if not isinstance(obj, dict) or set(obj) != MEASURE_KEYS:
        got = sorted(obj) if isinstance(obj, dict) else type(obj).__name__
        raise FormatError(f"{path}: top-level keys {got}")
    n = obj["n"]
    if not isinstance(n, int) or isinstance(n, bool):
        raise FormatError("n is not a JSON integer")
    net = obj["proof_net"]
    if not isinstance(net, dict) or set(net) != NET_KEYS:
        raise FormatError(f"proof_net keys {sorted(net) if isinstance(net, dict) else net}")
    last = net["last"]
    if not isinstance(last, int) or isinstance(last, bool) or last < 0:
        raise FormatError("proof_net.last is not a nonnegative JSON integer")
    if obj["points"] != []:
        raise FormatError("points is not empty")
    rows: list[tuple[Fraction, Fraction, Fraction, Fraction, Fraction]] = []
    rects = obj["rectangles"]
    if not isinstance(rects, list):
        raise FormatError("rectangles is not a list")
    for i, r in enumerate(rects):
        if not isinstance(r, dict) or set(r) != ROW_KEYS:
            raise FormatError(f"row {i}: keys {sorted(r) if isinstance(r, dict) else r}")
        box = r["rectangle"]
        if not isinstance(box, list) or len(box) != 4:
            raise FormatError(f"row {i}: rectangle is not four numbers")
        x0, y0, x1, y1 = (num(v) for v in box)
        rows.append((x0, y0, x1, y1, num(r["mass"])))
    return {
        "n": n,
        "L": num(obj["L"]),
        "B": num(obj["B"]),
        "step": num(net["step"]),
        "last": last,
        "total_mass": num(obj["total_mass"]),
        "rows": rows,
        "raw_strings": rects,
        "stored_sha256": sha256_bytes(raw),
        "json_sha256": sha256_bytes(payload),
        "canonical_sha256": sha256_bytes(
            json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
        ),
    }


def d4_images(
    x0: Fraction, y0: Fraction, x1: Fraction, y1: Fraction, side: Fraction
) -> list[tuple[Fraction, Fraction, Fraction, Fraction]]:
    """The eight images of [x0, x1] x [y0, y1] under the symmetries of [0, side]^2."""
    s = side
    return [
        (x0, y0, x1, y1),  # identity
        (s - x1, y0, s - x0, y1),  # x -> s - x
        (x0, s - y1, x1, s - y0),  # y -> s - y
        (s - x1, s - y1, s - x0, s - y0),  # half turn
        (y0, x0, y1, x1),  # (x, y) -> (y, x)
        (s - y1, x0, s - y0, x1),  # (x, y) -> (s - y, x)
        (y0, s - x1, y1, s - x0),  # (x, y) -> (y, s - x)
        (s - y1, s - x1, s - y0, s - x0),  # (x, y) -> (s - y, s - x)
    ]


def expand(
    rows: list[tuple[Fraction, Fraction, Fraction, Fraction, Fraction]], side: Fraction
) -> list[tuple[Fraction, Fraction, Fraction, Fraction, Fraction, Fraction]]:
    """Merged D4 expansion: (x0, y0, x1, y1, mass, density), coincident images summed."""
    acc: dict[tuple[Fraction, Fraction, Fraction, Fraction], Fraction] = {}
    for x0, y0, x1, y1, m in rows:
        for img in d4_images(x0, y0, x1, y1, side):
            acc[img] = acc.get(img, Fraction(0)) + m / 8
    out = []
    for (a, b, c, d), mass in acc.items():
        area = (c - a) * (d - b)
        out.append((a, b, c, d, mass, mass / area))
    out.sort()
    return out


# ---------------------------------------------------------------- the net and domains


def w_half_width(t: Fraction) -> Fraction:
    """w(t) = (1 + 2t - t^2) / (2(1 + t^2)): half the axis extent of a unit square at
    angle 2 arctan t, which is (cos + sin) / 2 of that angle."""
    return (1 + 2 * t - t * t) / (2 * (1 + t * t))


def cos_sin(t: Fraction) -> tuple[Fraction, Fraction]:
    """Exact cos and sin of 2 arctan t."""
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def node_tangent(r: int, step: Fraction) -> Fraction:
    return r * step


def bin_low(r: int, step: Fraction) -> Fraction:
    """a_r = max(0, r D - D/2), the least half-angle tangent assigned to node r."""
    return max(Fraction(0), r * step - step / 2)


def domain_upper(r: int, step: Fraction, side: Fraction) -> Fraction:
    """U_r = L - w(a_r): the quadrant [L/2, U_r]^2 is what the argument needs at r."""
    return side - w_half_width(bin_low(r, step))


# ---------------------------------------------------------------- exact capture


def _q(v: Fraction | int) -> mpq:
    return mpq(v.numerator, v.denominator) if isinstance(v, Fraction) else mpq(v)


def to_mpq_rects(
    rects: list[tuple[Fraction, Fraction, Fraction, Fraction, Fraction, Fraction]],
    factor: Fraction = Fraction(1),
) -> list[tuple[mpq, mpq, mpq, mpq, mpq, mpq]]:
    """Rectangles as mpq with mass and density multiplied by factor."""
    f = _q(factor)
    return [
        (_q(a), _q(b), _q(c), _q(d), _q(m) * f, _q(g) * f) for (a, b, c, d, m, g) in rects
    ]


def _clip(poly: list[tuple[mpq, mpq]], nx: mpq, ny: mpq, k: mpq) -> list[tuple[mpq, mpq]]:
    """Sutherland-Hodgman: keep nx*x + ny*y <= k."""
    out: list[tuple[mpq, mpq]] = []
    m = len(poly)
    for i in range(m):
        px, py = poly[i]
        qx, qy = poly[(i + 1) % m]
        fp = nx * px + ny * py - k
        fq = nx * qx + ny * qy - k
        if fp <= 0:
            out.append((px, py))
        if (fp < 0 < fq) or (fq < 0 < fp):
            tt = fp / (fp - fq)
            out.append((px + tt * (qx - px), py + tt * (qy - py)))
    return out


def _area(poly: list[tuple[mpq, mpq]]) -> mpq:
    s = mpq(0)
    m = len(poly)
    for i in range(m):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % m]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def capture_exact_clip(
    rects: list[tuple[mpq, mpq, mpq, mpq, mpq, mpq]],
    c: mpq,
    s: mpq,
    h: mpq,
    px: mpq,
    py: mpq,
) -> mpq:
    """Exact capture of the closed square of half-side h, centre (px, py), whose sides
    have unit normals u = (c, s) and v = (-s, c), with c^2 + s^2 = 1. Each rectangle is
    clipped against the four half-planes, its area taken by the shoelace formula."""
    total = mpq(0)
    ext = h * (abs(c) + abs(s))  # half axis extent of the square
    for x0, y0, x1, y1, mass, dens in rects:
        if x1 <= px - ext or x0 >= px + ext or y1 <= py - ext or y0 >= py + ext:
            continue
        # u- and v-coordinates of the four corners relative to the centre
        cu = [c * (x - px) + s * (y - py) for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
        cv = [-s * (x - px) + c * (y - py) for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
        if max(cu) <= h and min(cu) >= -h and max(cv) <= h and min(cv) >= -h:
            total += mass
            continue
        if min(cu) >= h or max(cu) <= -h or min(cv) >= h or max(cv) <= -h:
            continue
        poly = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        for nx, ny, k in (
            (c, s, px * c + py * s + h),
            (-c, -s, -(px * c + py * s) + h),
            (-s, c, -px * s + py * c + h),
            (s, -c, px * s - py * c + h),
        ):
            poly = _clip(poly, nx, ny, k)
            if len(poly) < 3:
                break
        if len(poly) >= 3:
            total += dens * _area(poly)
    return total


def _chord_area(
    x0: mpq, y0: mpq, x1: mpq, y1: mpq, c: mpq, s: mpq, h: mpq, px: mpq, py: mpq
) -> mpq:
    """Exact area of [x0, x1] x [y0, y1] inside the square, by integrating vertical
    chords. Needs c > 0 and s > 0. The chord length is max(0, G) with
    G = min(y1', f1, f2) - max(y0', g1, g2), piecewise linear, and every breakpoint of
    max(0, G) is among the fourteen nodes below, so the trapezoid rule is exact."""
    a = b = h
    e0, e1 = x0 - px, x1 - px
    lo, hi = y0 - py, y1 - py

    def g_of(xi: mpq) -> mpq:
        f1 = (a - c * xi) / s
        f2 = (b + s * xi) / c
        g1 = (-a - c * xi) / s
        g2 = (s * xi - b) / c
        return min(hi, f1, f2) - max(lo, g1, g2)

    nodes = {
        e0,
        e1,
        (c * a - s * b),
        (s * b - c * a),
        (c * a + s * b),
        -(c * a + s * b),
        (a - s * hi) / c,
        (c * hi - b) / s,
        (-a - s * lo) / c,
        (c * lo + b) / s,
        (-a - s * hi) / c,
        (c * hi + b) / s,
        (a - s * lo) / c,
        (c * lo - b) / s,
    }
    pts = sorted(z for z in nodes if e0 <= z <= e1)
    vals = [max(mpq(0), g_of(z)) for z in pts]
    area = mpq(0)
    for i in range(len(pts) - 1):
        area += (pts[i + 1] - pts[i]) * (vals[i] + vals[i + 1]) / 2
    return area


def capture_exact_chords(
    rects: list[tuple[mpq, mpq, mpq, mpq, mpq, mpq]],
    c: mpq,
    s: mpq,
    h: mpq,
    px: mpq,
    py: mpq,
) -> mpq:
    """The same capture by a second exact method (vertical chords), for c, s > 0."""
    if not (c > 0 and s > 0):
        raise ValueError("chord method needs c > 0 and s > 0")
    total = mpq(0)
    ext = h * (c + s)
    for x0, y0, x1, y1, _mass, dens in rects:
        if x1 <= px - ext or x0 >= px + ext or y1 <= py - ext or y0 >= py + ext:
            continue
        ar = _chord_area(x0, y0, x1, y1, c, s, h, px, py)
        if ar:
            total += dens * ar
    return total


def capture_exact_axis(
    rects: list[tuple[mpq, mpq, mpq, mpq, mpq, mpq]], h: mpq, px: mpq, py: mpq
) -> mpq:
    """Exact capture of the axis-parallel square of half-side h: overlap products."""
    total = mpq(0)
    for x0, y0, x1, y1, _mass, dens in rects:
        ox = min(px + h, x1) - max(px - h, x0)
        if ox <= 0:
            continue
        oy = min(py + h, y1) - max(py - h, y0)
        if oy <= 0:
            continue
        total += dens * ox * oy
    return total


def capture_exact(
    rects: list[tuple[mpq, mpq, mpq, mpq, mpq, mpq]],
    r: int,
    step: Fraction,
    side_b: Fraction,
    px: Fraction | mpq,
    py: Fraction | mpq,
) -> mpq:
    """Capture of the core of side B at net index r, centre (px, py), exactly."""
    h = _q(side_b) / 2
    pxq = _q(px) if isinstance(px, Fraction) else px
    pyq = _q(py) if isinstance(py, Fraction) else py
    if r == 0:
        return capture_exact_axis(rects, h, pxq, pyq)
    c, s = cos_sin(r * step)
    return capture_exact_clip(rects, _q(c), _q(s), h, pxq, pyq)


def float_to_fraction(x: float) -> Fraction:
    return Fraction(x)


def mpq_to_float_str(v: mpq, digits: int = 17) -> str:
    return format(gmpy2.mpfr(v, 200), f".{digits}g")


# ---------------------------------------------------------------- float search helpers


class FloatMeasure:
    """Float copy of an expanded measure for searches that decide nothing."""

    def __init__(
        self,
        rects: list[tuple[Fraction, Fraction, Fraction, Fraction, Fraction, Fraction]],
        factor: Fraction = Fraction(1),
    ):
        arr = np.array(
            [[float(a), float(b), float(c), float(d), float(g * factor)] for a, b, c, d, _m, g in rects]
        )
        self.x0, self.y0, self.x1, self.y1, self.d = (arr[:, i].copy() for i in range(5))
        self.mass = self.d * (self.x1 - self.x0) * (self.y1 - self.y0)

    def capture(self, c: float, s: float, h: float, px: float, py: float) -> float:
        """Float capture at one centre (s > 0 rotated, or s == 0 axis)."""
        if s == 0.0:
            ox = np.clip(np.minimum(px + h, self.x1) - np.maximum(px - h, self.x0), 0, None)
            oy = np.clip(np.minimum(py + h, self.y1) - np.maximum(py - h, self.y0), 0, None)
            return float(np.dot(self.d, ox * oy))
        ext = h * (c + s)
        sel = (self.x1 > px - ext) & (self.x0 < px + ext) & (self.y1 > py - ext) & (
            self.y0 < py + ext
        )
        x0, y0, x1, y1, d = self.x0[sel], self.y0[sel], self.x1[sel], self.y1[sel], self.d[sel]
        e0, e1 = x0 - px, x1 - px
        lo, hi = y0 - py, y1 - py
        n = len(x0)
        cand = np.empty((n, 14))
        cand[:, 0] = e0
        cand[:, 1] = e1
        cand[:, 2] = c * h - s * h
        cand[:, 3] = s * h - c * h
        cand[:, 4] = c * h + s * h
        cand[:, 5] = -(c * h + s * h)
        cand[:, 6] = (h - s * hi) / c
        cand[:, 7] = (c * hi - h) / s
        cand[:, 8] = (-h - s * lo) / c
        cand[:, 9] = (c * lo + h) / s
        cand[:, 10] = (-h - s * hi) / c
        cand[:, 11] = (c * hi + h) / s
        cand[:, 12] = (h - s * lo) / c
        cand[:, 13] = (c * lo - h) / s
        cand = np.clip(cand, e0[:, None], e1[:, None])
        cand.sort(axis=1)
        f1 = (h - c * cand) / s
        f2 = (h + s * cand) / c
        g1 = (-h - c * cand) / s
        g2 = (s * cand - h) / c
        top = np.minimum(np.minimum(hi[:, None], f1), f2)
        bot = np.maximum(np.maximum(lo[:, None], g1), g2)
        val = np.clip(top - bot, 0, None)
        area = 0.5 * np.sum((cand[:, 1:] - cand[:, :-1]) * (val[:, 1:] + val[:, :-1]), axis=1)
        return float(np.dot(d, area))
