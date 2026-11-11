"""Exact helpers for the 11 November 2026 review of wand125's fine-net certificates
mixed_n28_L57425 and mixed_n30_L58925 (bead think-4ul6).

Written for this review from the mathematics and the source's SPEC.md section 2 (the
format) alone. It imports nothing from this repository, the source or the maintained
route: only the Python standard library, and numpy for a float prefilter that only
discards images whose bounding box misses the core's by more than 1e-6.
"""

from __future__ import annotations

import hashlib
import json
import re
import zlib
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np

#: The declared net both certificates state; premises.py checks that each file says so.
STEP = Fraction(1, 5002)
LAST = 2072
#: The certificates' core side; premises.py checks it.
CORE = Fraction(4999, 5000)

_RAT = re.compile(r"^-?[0-9]+/[0-9]+$")
_DEC = re.compile(r"^-?[0-9]+(\.[0-9]+)?$")

TOP_KEYS = {"n", "L", "B", "proof_net", "total_mass", "points", "rectangles"}


class StrictError(ValueError):
    """The candidate is not in the form this review reads."""


def rat(text: object) -> Fraction:
    """A rational from a string `p/q` or a plain decimal; anything else is refused."""
    if not isinstance(text, str):
        raise StrictError(f"expected a rational string, got {text!r}")
    if _RAT.match(text):
        p, q = text.split("/")
        if int(q) == 0:
            raise StrictError(f"zero denominator in {text!r}")
        return Fraction(int(p), int(q))
    if _DEC.match(text):
        return Fraction(text)
    raise StrictError(f"not a rational: {text!r}")


def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    keys = [k for k, _ in pairs]
    if len(set(keys)) != len(keys):
        raise StrictError(f"duplicate key among {keys}")
    return dict(pairs)


def _float_token(token: str) -> object:
    raise StrictError(f"float token {token!r}")


def _constant(token: str) -> object:
    raise StrictError(f"constant {token!r}")


def strict_json(data: bytes) -> object:
    return json.loads(
        data.decode("utf-8"),
        object_pairs_hook=_pairs,
        parse_float=_float_token,
        parse_constant=_constant,
    )


def gunzip_one(raw: bytes) -> bytes:
    """The one gzip member of `raw`; a second member or trailing bytes are refused."""
    d = zlib.decompressobj(wbits=31)
    out = d.decompress(raw) + d.flush()
    if not d.eof:
        raise StrictError("truncated gzip stream")
    if d.unused_data:
        raise StrictError("data after the first gzip member")
    return out


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass
class Cert:
    path: str
    stored_sha256: str
    sha256: str
    obj: dict
    n: int
    L: Fraction
    B: Fraction
    step: Fraction
    last: int
    total_mass: Fraction
    rows: list[tuple[Fraction, Fraction, Fraction, Fraction, Fraction]]


def parse_candidate(raw: bytes, path: str = "", field_order: str = "x0y0x1y1") -> Cert:
    data = gunzip_one(raw) if raw[:2] == b"\x1f\x8b" else raw
    obj = strict_json(data)
    if not isinstance(obj, dict) or set(obj) != TOP_KEYS:
        raise StrictError(f"top-level keys {sorted(obj) if isinstance(obj, dict) else obj!r}")
    n = obj["n"]
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise StrictError(f"n is {n!r}")
    pn = obj["proof_net"]
    if not isinstance(pn, dict) or not ({"step", "last"} <= set(pn) <= {"step", "last", "count"}):
        raise StrictError(f"proof_net is {pn!r}")
    last = pn["last"]
    if not isinstance(last, int) or isinstance(last, bool):
        raise StrictError(f"proof_net.last is {last!r}")
    if "count" in pn and pn["count"] != last + 1:
        raise StrictError("proof_net.count is not last + 1")
    if obj["points"] != []:
        raise StrictError("points is not empty")
    rows = []
    for row in obj["rectangles"]:
        if not isinstance(row, dict) or set(row) != {"rectangle", "mass"}:
            raise StrictError(f"row keys {row!r}")
        a = row["rectangle"]
        if not isinstance(a, list) or len(a) != 4:
            raise StrictError(f"rectangle {a!r}")
        v = [rat(x) for x in a]
        if field_order == "x0y0x1y1":
            x0, y0, x1, y1 = v
        elif field_order == "x0x1y0y1":
            x0, x1, y0, y1 = v
        else:
            raise ValueError(field_order)
        rows.append((x0, y0, x1, y1, rat(row["mass"])))
    return Cert(
        path=path,
        stored_sha256=sha256(raw),
        sha256=sha256(data),
        obj=obj,
        n=n,
        L=rat(obj["L"]),
        B=rat(obj["B"]),
        step=rat(pn["step"]),
        last=last,
        total_mass=rat(obj["total_mass"]),
        rows=rows,
    )


def read_candidate(path: str | Path, field_order: str = "x0y0x1y1") -> Cert:
    return parse_candidate(Path(path).read_bytes(), str(path), field_order)


# --- The measure (SPEC.md section 2: the D4 average) -------------------------------

Box = tuple[Fraction, Fraction, Fraction, Fraction]


def d4_images(x0: Fraction, y0: Fraction, x1: Fraction, y1: Fraction, L: Fraction) -> list[Box]:
    """The eight images of [x0, x1] x [y0, y1] under the symmetries of [0, L]^2."""
    out = []
    for a0, a1, c0, c1 in ((x0, x1, y0, y1), (y0, y1, x0, x1)):
        for X0, X1 in ((a0, a1), (L - a1, L - a0)):
            for Y0, Y1 in ((c0, c1), (L - c1, L - c0)):
                out.append((X0, Y0, X1, Y1))
    return out


def symmetries(L: Fraction):
    """The eight maps of D4 on boxes, as functions Box -> Box."""

    def mk(swap: bool, fx: bool, fy: bool):
        def g(b: Box) -> Box:
            x0, y0, x1, y1 = b
            if swap:
                x0, y0, x1, y1 = y0, x0, y1, x1
            if fx:
                x0, x1 = L - x1, L - x0
            if fy:
                y0, y1 = L - y1, L - y0
            return (x0, y0, x1, y1)

        return g

    return [mk(s, a, b) for s in (False, True) for a in (False, True) for b in (False, True)]


def expand(
    rows: list[tuple[Fraction, Fraction, Fraction, Fraction, Fraction]],
    L: Fraction,
    d4: bool = True,
) -> dict[Box, Fraction]:
    """Image -> density, coincident images merged by adding densities.

    Each row of mass m puts m/8 uniformly on each of its eight images (or, with
    d4=False, the whole m on the row itself, a wrong reading kept for the controls).
    """
    merged: dict[Box, Fraction] = {}
    for x0, y0, x1, y1, m in rows:
        area = (x1 - x0) * (y1 - y0)
        if not (x1 > x0 and y1 > y0):
            raise StrictError("a row of no positive area")
        ims = d4_images(x0, y0, x1, y1, L) if d4 else [(x0, y0, x1, y1)]
        dens = m / (len(ims) * area)
        for key in ims:
            merged[key] = merged.get(key, Fraction(0)) + dens
    return merged


class Measure:
    """A merged expansion with a float index for prefiltering."""

    def __init__(self, images: dict[Box, Fraction]):
        self.keys = list(images)
        self.dens = [images[k] for k in self.keys]
        self.mass = [d * (k[2] - k[0]) * (k[3] - k[1]) for k, d in zip(self.keys, self.dens)]
        arr = np.array([[float(v) for v in k] for k in self.keys], dtype=np.float64)
        self.fx0, self.fy0, self.fx1, self.fy1 = arr[:, 0], arr[:, 1], arr[:, 2], arr[:, 3]

    def near(self, xmin: float, xmax: float, ymin: float, ymax: float) -> np.ndarray:
        eps = 1e-6
        mask = (
            (self.fx1 > xmin - eps)
            & (self.fx0 < xmax + eps)
            & (self.fy1 > ymin - eps)
            & (self.fy0 < ymax + eps)
        )
        return np.nonzero(mask)[0]

    def scaled(self, factor: Fraction) -> Measure:
        return Measure({k: d * factor for k, d in zip(self.keys, self.dens)})


# --- The net (SPEC.md sections 3 and 4) -------------------------------------------


def node(j: int, step: Fraction = STEP) -> Fraction:
    return j * step


def cos_sin(j: int, step: Fraction = STEP) -> tuple[Fraction, Fraction]:
    t = j * step
    d = 1 + t * t
    return (1 - t * t) / d, 2 * t / d


def r_of(t: Fraction) -> Fraction:
    """(cos + sin)/2 of the angle 2 atan t: a unit square's half-extent."""
    return (1 + 2 * t - t * t) / (2 * (1 + t * t))


def a_of(j: int, step: Fraction = STEP) -> Fraction:
    return max(Fraction(0), j * step - step / 2)


def upper_end(j: int, L: Fraction, step: Fraction = STEP) -> Fraction:
    """U_j = L - r(a_j), the far end of node j's centre domain."""
    return L - r_of(a_of(j, step))


# --- The exact capture of a closed core -------------------------------------------


def core_planes(cx: Fraction, cy: Fraction, c: Fraction, s: Fraction, b: Fraction):
    """The four closed half-planes n.p <= h whose intersection is the core."""
    uc = c * cx + s * cy
    vc = -s * cx + c * cy
    return [((c, s), uc + b), ((-c, -s), b - uc), ((-s, c), vc + b), ((s, -c), b - vc)]


def clip_area(X0: Fraction, Y0: Fraction, X1: Fraction, Y1: Fraction, planes) -> Fraction | None:
    """Area of [X0, X1] x [Y0, Y1] inside the core; None when no plane cuts the box."""
    poly = [(X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1)]
    cut = False
    for (nx, ny), h in planes:
        k = len(poly)
        if k == 0:
            return Fraction(0)
        vals = [nx * p[0] + ny * p[1] - h for p in poly]
        if all(v <= 0 for v in vals):
            continue
        cut = True
        out = []
        for i in range(k):
            p, q = poly[i], poly[(i + 1) % k]
            dp, dq = vals[i], vals[(i + 1) % k]
            if dp <= 0:
                out.append(p)
            if (dp < 0 < dq) or (dq < 0 < dp):
                lam = dp / (dp - dq)
                out.append((p[0] + lam * (q[0] - p[0]), p[1] + lam * (q[1] - p[1])))
        poly = out
    if not cut:
        return None
    if len(poly) < 3:
        return Fraction(0)
    acc = Fraction(0)
    for i in range(len(poly)):
        xa, ya = poly[i]
        xb, yb = poly[(i + 1) % len(poly)]
        acc += xa * yb - xb * ya
    return acc / 2


def capture(m: Measure, j: int, cx: Fraction, cy: Fraction, B: Fraction = CORE, step: Fraction = STEP) -> Fraction:
    """The exact mass of the closed core of side B, centre (cx, cy), angle 2 atan(j step)."""
    c, s = cos_sin(j, step)
    b = B / 2
    ext = b * (c + s)
    planes = core_planes(cx, cy, c, s, b)
    lox, hix, loy, hiy = cx - ext, cx + ext, cy - ext, cy + ext
    total = Fraction(0)
    for i in m.near(float(lox), float(hix), float(loy), float(hiy)):
        X0, Y0, X1, Y1 = m.keys[i]
        if X1 <= lox or X0 >= hix or Y1 <= loy or Y0 >= hiy:
            continue
        a = clip_area(X0, Y0, X1, Y1, planes)
        if a is None:
            total += m.mass[i]
        elif a:
            total += m.dens[i] * a
    return total


def axis_capture(m: Measure, cx: Fraction, cy: Fraction, B: Fraction = CORE) -> Fraction:
    """The exact capture at direction 0 by overlap lengths, a second method."""
    b = B / 2
    total = Fraction(0)
    for i in m.near(float(cx - b), float(cx + b), float(cy - b), float(cy + b)):
        X0, Y0, X1, Y1 = m.keys[i]
        ox = min(X1, cx + b) - max(X0, cx - b)
        oy = min(Y1, cy + b) - max(Y0, cy - b)
        if ox > 0 and oy > 0:
            total += m.dens[i] * ox * oy
    return total


def chord_capture(m: Measure, j: int, cx: Fraction, cy: Fraction, B: Fraction = CORE, step: Fraction = STEP) -> Fraction:
    """The exact capture by a second method, for j >= 1: vertical chords integrated exactly.

    For 0 < theta < pi/2 the core's vertical chord at x is [lo(x), hi(x)], lo the larger
    of the two lower edge lines and hi the smaller of the two upper ones. The length of
    that chord inside [Y0, Y1] is piecewise linear in x, with kinks only at the vertices'
    abscissae and where an edge line meets Y0 or Y1, so the trapezoid rule over those
    abscissae is exact. Nothing here is shared with clip_area.
    """
    c, s = cos_sin(j, step)
    if not (s > 0 and c > 0):
        raise ValueError("chord_capture needs 0 < theta < pi/2")
    b = B / 2
    p1 = (cx + b * (c + s), cy + b * (s - c))
    p2 = (cx + b * (c - s), cy + b * (s + c))
    p3 = (cx - b * (c + s), cy + b * (c - s))
    p4 = (cx - b * (c - s), cy - b * (s + c))
    lines = [
        (p3, (p4[1] - p3[1]) / (p4[0] - p3[0])),
        (p4, (p1[1] - p4[1]) / (p1[0] - p4[0])),
        (p3, (p2[1] - p3[1]) / (p2[0] - p3[0])),
        (p2, (p1[1] - p2[1]) / (p1[0] - p2[0])),
    ]

    def at(k: int, x: Fraction) -> Fraction:
        (xr, yr), sl = lines[k]
        return yr + sl * (x - xr)

    e = p1[0] - cx
    total = Fraction(0)
    for i in m.near(float(cx - e), float(cx + e), float(cy - e), float(cy + e)):
        X0, Y0, X1, Y1 = m.keys[i]
        xa, xb = max(X0, p3[0]), min(X1, p1[0])
        if not xb > xa:
            continue
        pts = {xa, xb, p4[0], p2[0]}
        for (xr, yr), sl in lines:
            for Y in (Y0, Y1):
                pts.add(xr + (Y - yr) / sl)
        xs = sorted(p for p in pts if xa <= p <= xb)

        def g(x: Fraction) -> Fraction:
            lo = max(at(0, x), at(1, x))
            hi = min(at(2, x), at(3, x))
            return max(min(hi, Y1) - max(lo, Y0), Fraction(0))

        gs = [g(x) for x in xs]
        area = sum(((xs[k + 1] - xs[k]) * (gs[k + 1] + gs[k]) for k in range(len(xs) - 1)), Fraction(0)) / 2
        total += m.dens[i] * area
    return total


class FloatMeasure:
    """Float copies of a merged expansion, for the heuristic search only."""

    def __init__(self, m: Measure):
        self.x0, self.y0, self.x1, self.y1 = m.fx0, m.fy0, m.fx1, m.fy1
        self.d = np.array([float(v) for v in m.dens], dtype=np.float64)


def fcapture(fm: FloatMeasure, c: float, s: float, b: float, cx: float, cy: float) -> float:
    """A binary64 estimate of the capture of a rotated core (0 < s <= c), deciding nothing.

    The core's vertical chord at abscissa x is [lo(x), hi(x)], lo the larger of the two
    lower edge lines and hi the smaller of the two upper ones; the length of that chord
    inside [Y0, Y1] is piecewise linear in x with its kinks among the vertices' abscissae
    and the abscissae where an edge line meets Y0 or Y1, so the trapezoid rule over those
    points integrates it exactly (up to rounding).
    """
    e = b * (c + s)
    mask = (fm.x1 > cx - e) & (fm.x0 < cx + e) & (fm.y1 > cy - e) & (fm.y0 < cy + e)
    X0, X1, Y0, Y1, d = fm.x0[mask], fm.x1[mask], fm.y0[mask], fm.y1[mask], fm.d[mask]
    if X0.size == 0:
        return 0.0
    # Vertices: p3 leftmost, p4 bottom, p2 top, p1 rightmost.
    p1 = (cx + b * (c + s), cy + b * (s - c))
    p2 = (cx + b * (c - s), cy + b * (s + c))
    p3 = (cx - b * (c + s), cy + b * (c - s))
    p4 = (cx - b * (c - s), cy - b * (s + c))
    lines = [  # (x_ref, y_ref, slope)
        (p3[0], p3[1], (p4[1] - p3[1]) / (p4[0] - p3[0])),  # lower left
        (p4[0], p4[1], (p1[1] - p4[1]) / (p1[0] - p4[0])),  # lower right
        (p3[0], p3[1], (p2[1] - p3[1]) / (p2[0] - p3[0])),  # upper left
        (p2[0], p2[1], (p1[1] - p2[1]) / (p1[0] - p2[0])),  # upper right
    ]
    xa = np.maximum(X0, p3[0])
    xb = np.minimum(X1, p1[0])
    pts = [xa, xb, np.full_like(xa, p4[0]), np.full_like(xa, p2[0])]
    for xr, yr, k in lines:
        for Y in (Y0, Y1):
            pts.append(xr + (Y - yr) / k)
    P = np.stack(pts, axis=1)
    P = np.clip(P, xa[:, None], xb[:, None])
    P.sort(axis=1)

    def g(x: np.ndarray) -> np.ndarray:
        lo = np.maximum(lines[0][1] + lines[0][2] * (x - lines[0][0]), lines[1][1] + lines[1][2] * (x - lines[1][0]))
        hi = np.minimum(lines[2][1] + lines[2][2] * (x - lines[2][0]), lines[3][1] + lines[3][2] * (x - lines[3][0]))
        return np.maximum(np.minimum(hi, Y1[:, None]) - np.maximum(lo, Y0[:, None]), 0.0)

    G = g(P)
    area = 0.5 * np.sum((P[:, 1:] - P[:, :-1]) * (G[:, 1:] + G[:, :-1]), axis=1)
    area = np.where(xb > xa, area, 0.0)
    return float(np.dot(d, area))


def fstr(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}"


def write_json(path: str | Path, obj: object) -> None:
    Path(path).write_text(json.dumps(obj, indent=1, sort_keys=False) + "\n")
