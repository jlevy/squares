"""Shared helpers for the stage 4 review of wand125's #446 fine-net certificates.

Written on 2026-10-23 for the review lane c-review-t233-math (bead think-bwis) from the
mathematics of the net-and-shrink argument and the certificate format alone. It imports
nothing from the squares repository, from the source's verifier, or from the maintained
sqverify-fast route, and none of their code was read before it ran.

Conventions (the format M certificate, as its README and the format specification state):

- every number is an exact rational, written as a decimal or as ``p/q``;
- a row ``{"rectangle": [x1, y1, x2, y2], "mass": m}`` is an orbit representative; its
  eight images under the symmetry group D4 of the container ``K = [0, L]^2`` each carry
  ``m / 8`` spread uniformly over the image (density ``m / (8 |R|)``);
- the core at net index ``r`` is the closed square of side ``B``, centre ``c`` and angle
  ``theta_r = 2 arctan(r * step)``.

The field order of ``rectangle`` is checked, not assumed: ``premises.py`` reports which
order gives positive-area rectangles inside ``K``, and ``receipts_check.py`` recomputes the
source's own exact capture values under it.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import zlib
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

# The four certificates and the side each claims, as the issue and the register state.
CERTS: dict[int, tuple[str, Fraction]] = {
    19: ("mixed_n19_L48275", Fraction(1931, 400)),
    20: ("mixed_n20_L49125", Fraction(393, 80)),
    26: ("mixed_n26_L5555", Fraction(1111, 200)),
    27: ("mixed_n27_L5655", Fraction(1131, 200)),
}

# Exact nonnegative decimals and fractions; nothing else is a number in these files.
_DECIMAL = re.compile(r"^(0|[1-9][0-9]*)(\.[0-9]+)?$")
_FRACTION = re.compile(r"^(0|[1-9][0-9]*)/([1-9][0-9]*)$")

# Float classification slack. Every float quantity compared below is within 1e-13 of
# its exact value (inputs below 8 in magnitude, a few operations deep), so a decision
# made with this slack is the exact decision.
TOL = 1e-9


class StrictError(ValueError):
    """A file that a strict reader refuses."""


def rat(text: object) -> Fraction:
    """Read an exact rational from a JSON string, refusing anything inexact."""
    if not isinstance(text, str):
        msg = f"expected a string number, got {type(text).__name__}: {text!r}"
        raise StrictError(msg)
    if _DECIMAL.match(text) or _FRACTION.match(text):
        return Fraction(text)
    msg = f"not an exact nonnegative decimal or fraction: {text!r}"
    raise StrictError(msg)


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            msg = f"duplicate JSON key {key!r}"
            raise StrictError(msg)
        out[key] = value
    return out


def _no_float(token: str) -> float:
    msg = f"binary floating-point JSON token {token!r}"
    raise StrictError(msg)


def _no_constant(token: str) -> float:
    msg = f"non-finite JSON constant {token!r}"
    raise StrictError(msg)


def strict_json(raw: bytes) -> Any:
    """Parse JSON refusing duplicate keys, float tokens and NaN/Infinity."""
    return json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=_pairs,
        parse_float=_no_float,
        parse_constant=_no_constant,
    )


def loose_json(raw: bytes) -> Any:
    """Parse JSON that legitimately holds floats (run logs), still refusing duplicates."""
    return json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs)


def read_gzip_single(path: Path) -> tuple[bytes, bytes]:
    """Return (stored, decompressed) bytes, refusing anything but one complete member."""
    stored = path.read_bytes()
    dec = zlib.decompressobj(wbits=31)
    raw = dec.decompress(stored) + dec.flush()
    if not dec.eof or dec.unused_data:
        msg = f"{path}: not exactly one complete gzip member"
        raise StrictError(msg)
    return stored, raw


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class Row:
    """One listed orbit representative, in the file's own field order."""

    fields: tuple[Fraction, Fraction, Fraction, Fraction]
    mass: Fraction


@dataclass
class Candidate:
    name: str
    n: int
    L: Fraction
    B: Fraction
    step: Fraction
    last: int
    total_mass: Fraction
    rows: list[Row]
    points: list[Any]
    stored_sha256: str
    raw_sha256: str
    stored_bytes: int
    raw_bytes: int
    keys: list[str]
    net_keys: list[str]


def read_candidate(packet: Path, n: int) -> Candidate:
    """Read one retained candidate strictly."""
    name, _side = CERTS[n]
    path = packet / "release" / "certificates" / name / "candidate.json.gz"
    stored, raw = read_gzip_single(path)
    doc = strict_json(raw)
    if not isinstance(doc, dict):
        msg = "candidate is not a JSON object"
        raise StrictError(msg)
    want = {"n", "L", "B", "proof_net", "total_mass", "points", "rectangles"}
    if set(doc) != want:
        msg = f"candidate keys {sorted(doc)} != {sorted(want)}"
        raise StrictError(msg)
    if type(doc["n"]) is not int:
        msg = "n is not a JSON integer"
        raise StrictError(msg)
    net = doc["proof_net"]
    if not isinstance(net, dict) or not set(net) <= {"step", "last", "count"}:
        msg = f"proof_net {net!r} is not a uniform net declaration"
        raise StrictError(msg)
    if type(net.get("last")) is not int or net["last"] < 0:
        msg = "proof_net.last is not a nonnegative JSON integer"
        raise StrictError(msg)
    if "count" in net and (type(net["count"]) is not int or net["count"] != net["last"] + 1):
        msg = "proof_net.count is not last + 1"
        raise StrictError(msg)
    rows: list[Row] = []
    for item in doc["rectangles"]:
        if not isinstance(item, dict) or set(item) != {"rectangle", "mass"}:
            msg = f"rectangle row {item!r} is not {{rectangle, mass}}"
            raise StrictError(msg)
        geom = item["rectangle"]
        if not isinstance(geom, list) or len(geom) != 4:
            msg = f"rectangle {geom!r} is not four numbers"
            raise StrictError(msg)
        a, b, c, d = (rat(v) for v in geom)
        rows.append(Row((a, b, c, d), rat(item["mass"])))
    return Candidate(
        name=name,
        n=doc["n"],
        L=rat(doc["L"]),
        B=rat(doc["B"]),
        step=rat(net["step"]),
        last=net["last"],
        total_mass=rat(doc["total_mass"]),
        rows=rows,
        points=list(doc["points"]),
        stored_sha256=sha256(stored),
        raw_sha256=sha256(raw),
        stored_bytes=len(stored),
        raw_bytes=len(raw),
        keys=sorted(doc),
        net_keys=sorted(net),
    )


@dataclass(frozen=True)
class Rect:
    x1: Fraction
    y1: Fraction
    x2: Fraction
    y2: Fraction


def as_rect(row: Row, order: str) -> Rect:
    """Interpret a row's four numbers under a named field order."""
    a, b, c, d = row.fields
    if order == "x1y1x2y2":
        return Rect(a, b, c, d)
    if order == "x1x2y1y2":
        return Rect(a, c, b, d)
    msg = f"unknown field order {order!r}"
    raise ValueError(msg)


def d4_images(r: Rect, side: Fraction) -> list[Rect]:
    """The eight images of an axis-parallel rectangle under the symmetries of [0, L]^2.

    D4 is the group of signed permutations of the axes about the centre: an optional
    exchange of x and y, then an optional reflection of each axis.
    """
    out: list[Rect] = []
    for swap in (False, True):
        x1, x2, y1, y2 = (r.y1, r.y2, r.x1, r.x2) if swap else (r.x1, r.x2, r.y1, r.y2)
        for flip_x in (False, True):
            ax1, ax2 = (side - x2, side - x1) if flip_x else (x1, x2)
            for flip_y in (False, True):
                ay1, ay2 = (side - y2, side - y1) if flip_y else (y1, y2)
                out.append(Rect(ax1, ay1, ax2, ay2))
    return out


@dataclass
class Measure:
    """The expanded, D4-invariant density: distinct rectangles with exact densities."""

    side: Fraction
    rects: list[Rect]
    density: list[Fraction]
    mass: list[Fraction]  # density times area, exactly
    # float mirrors for classification and search
    mx: np.ndarray = field(repr=False)
    my: np.ndarray = field(repr=False)
    wx: np.ndarray = field(repr=False)
    wy: np.ndarray = field(repr=False)
    fx1: np.ndarray = field(repr=False)
    fy1: np.ndarray = field(repr=False)
    fx2: np.ndarray = field(repr=False)
    fy2: np.ndarray = field(repr=False)
    frho: np.ndarray = field(repr=False)
    fmass: np.ndarray = field(repr=False)

    @property
    def total(self) -> Fraction:
        return sum(self.mass, Fraction(0))


def expand(cand: Candidate, order: str = "x1y1x2y2") -> Measure:
    """Expand every row into its D4 orbit, merging coincident images by exact key."""
    dens: dict[Rect, Fraction] = {}
    for row in cand.rows:
        rect = as_rect(row, order)
        area = (rect.x2 - rect.x1) * (rect.y2 - rect.y1)
        if area <= 0:
            msg = f"rectangle without positive area under order {order}: {rect}"
            raise StrictError(msg)
        rho = row.mass / (8 * area)
        for img in d4_images(rect, cand.L):
            dens[img] = dens.get(img, Fraction(0)) + rho
    rects = list(dens)
    density = [dens[r] for r in rects]
    mass = [dens[r] * (r.x2 - r.x1) * (r.y2 - r.y1) for r in rects]

    def arr(vals: list[Fraction]) -> np.ndarray:
        return np.array([float(v) for v in vals], dtype=np.float64)

    x1 = [r.x1 for r in rects]
    y1 = [r.y1 for r in rects]
    x2 = [r.x2 for r in rects]
    y2 = [r.y2 for r in rects]
    return Measure(
        side=cand.L,
        rects=rects,
        density=density,
        mass=mass,
        mx=arr([(a + b) / 2 for a, b in zip(x1, x2, strict=True)]),
        my=arr([(a + b) / 2 for a, b in zip(y1, y2, strict=True)]),
        wx=arr([(b - a) / 2 for a, b in zip(x1, x2, strict=True)]),
        wy=arr([(b - a) / 2 for a, b in zip(y1, y2, strict=True)]),
        fx1=arr(x1),
        fy1=arr(y1),
        fx2=arr(x2),
        fy2=arr(y2),
        frho=arr(density),
        fmass=arr(mass),
    )


# ---------------------------------------------------------------------------- the net


def cos_sin(step: Fraction, r: int) -> tuple[Fraction, Fraction]:
    """Exact cosine and sine of theta_r = 2 arctan(r * step)."""
    t = r * step
    d = 1 + t * t
    return (1 - t * t) / d, 2 * t / d


def half_width(a: Fraction) -> Fraction:
    """rho(a): half the axis extent of a unit square at half-angle tangent a."""
    return (1 + 2 * a - a * a) / (2 * (1 + a * a))


def bin_floor(step: Fraction, r: int) -> Fraction:
    """a_r = max(0, t_r - step/2), the least half-angle tangent assigned to node r."""
    return max(Fraction(0), r * step - step / 2)


def domain_upper(side: Fraction, step: Fraction, r: int) -> Fraction:
    """U_r = L - rho(a_r): the per-bin quadrant is [L/2, U_r]^2."""
    return side - half_width(bin_floor(step, r))


# ------------------------------------------------------------------ capture of a core


def square_vertices(
    cx: Fraction, cy: Fraction, c: Fraction, s: Fraction, h: Fraction
) -> list[tuple[Fraction, Fraction]]:
    """Counterclockwise vertices of the closed square of half-side h at angle (c, s)."""
    ux, uy = c * h, s * h  # h * u
    vx, vy = -s * h, c * h  # h * v
    return [
        (cx + ux + vx, cy + uy + vy),
        (cx - ux + vx, cy - uy + vy),
        (cx - ux - vx, cy - uy - vy),
        (cx + ux - vx, cy + uy - vy),
    ]


def _clip(poly: list[Any], coord: int, bound: Any, keep_above: bool) -> list[Any]:  # noqa: FBT001
    """Clip a convex polygon to coord >= bound (keep_above) or coord <= bound."""
    out: list[Any] = []
    count = len(poly)
    for i in range(count):
        p = poly[i]
        q = poly[(i + 1) % count]
        fp = (p[coord] - bound) if keep_above else (bound - p[coord])
        fq = (q[coord] - bound) if keep_above else (bound - q[coord])
        if fp >= 0:
            out.append(p)
            if fq < 0:
                t = fp / (fp - fq)
                out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
        elif fq >= 0:
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def clipped_area(poly: list[Any], x1: Any, y1: Any, x2: Any, y2: Any) -> Any:
    """Area of a convex polygon intersected with [x1, x2] x [y1, y2] (shoelace)."""
    for coord, bound, above in ((0, x1, True), (0, x2, False), (1, y1, True), (1, y2, False)):
        poly = _clip(poly, coord, bound, above)
        if len(poly) < 3:
            return 0 * x1
    acc = 0 * x1
    count = len(poly)
    for i in range(count):
        p = poly[i]
        q = poly[(i + 1) % count]
        acc += p[0] * q[1] - q[0] * p[1]
    return abs(acc) / 2


def classify(
    meas: Measure, cx: float, cy: float, c: float, s: float, h: float
) -> tuple[np.ndarray, np.ndarray]:
    """Float classification of every expanded rectangle: (inside mask, boundary mask).

    Inside: inside the closed core with slack TOL. Outside (neither mask): separated
    along x, y, u or v by more than TOL, so the intersection has zero area. The slack
    makes both float decisions the exact decisions (module docstring).
    """
    dx = meas.mx - cx
    dy = meas.my - cy
    du = np.abs(c * dx + s * dy)
    dv = np.abs(-s * dx + c * dy)
    eu = c * meas.wx + s * meas.wy
    ev = s * meas.wx + c * meas.wy
    reach = h * (c + s)
    outside = (
        (du - eu > h + TOL)
        | (dv - ev > h + TOL)
        | (np.abs(dx) - meas.wx > reach + TOL)
        | (np.abs(dy) - meas.wy > reach + TOL)
    )
    inside = (du + eu < h - TOL) & (dv + ev < h - TOL)
    boundary = ~outside & ~inside
    return inside, boundary


def exact_capture(
    meas: Measure, cx: Fraction, cy: Fraction, c: Fraction, s: Fraction, h: Fraction
) -> tuple[Fraction, int, int]:
    """Exact measure of the closed core; returns (capture, inside count, boundary count)."""
    inside, boundary = classify(meas, float(cx), float(cy), float(c), float(s), float(h))
    total = Fraction(0)
    for k in np.flatnonzero(inside):
        total += meas.mass[k]
    poly = square_vertices(cx, cy, c, s, h)
    for k in np.flatnonzero(boundary):
        r = meas.rects[k]
        area = clipped_area(poly, r.x1, r.y1, r.x2, r.y2)
        if area:
            total += meas.density[k] * area
    return total, int(inside.sum()), int(boundary.sum())


def float_capture(meas: Measure, cx: float, cy: float, c: float, s: float, h: float) -> float:
    """Floating-point capture for the search only; decides nothing."""
    inside, boundary = classify(meas, cx, cy, c, s, h)
    total = float(meas.fmass[inside].sum())
    ux, uy, vx, vy = c * h, s * h, -s * h, c * h
    poly = [
        (cx + ux + vx, cy + uy + vy),
        (cx - ux + vx, cy - uy + vy),
        (cx - ux - vx, cy - uy - vy),
        (cx + ux - vx, cy + uy - vy),
    ]
    for k in np.flatnonzero(boundary):
        area = clipped_area(poly, meas.fx1[k], meas.fy1[k], meas.fx2[k], meas.fy2[k])
        total += float(meas.frho[k]) * float(area)
    return float(total)


def float_of(x: Fraction) -> float:
    """Nearest binary64 of an exact rational (Python rounds Fraction -> float correctly)."""
    return float(x)


def isqrt_frac_bounds(x: Fraction, digits: int = 40) -> tuple[Fraction, Fraction]:
    """Rational bounds lo <= sqrt(x) <= hi with hi - lo <= 10**-digits."""
    scale = 10**digits
    root = math.isqrt(x.numerator * scale * scale // x.denominator)
    lo = Fraction(root, scale)
    hi = Fraction(root + 1, scale)
    if not (lo * lo <= x <= hi * hi):
        msg = "square-root bracket failed"
        raise ArithmeticError(msg)
    return lo, hi
