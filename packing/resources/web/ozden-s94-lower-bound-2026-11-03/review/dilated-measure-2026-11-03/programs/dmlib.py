"""Shared reader, measure and capture code for the stage 4 review of #890's certificate.

Written for the review of Doğa Özden's s(94) >= 1993/200 (a format M measure on a
declared net), apart from sqverify-fast, the census tools and the author's programs: it
imports nothing from this repository and nothing from the packet's `source/`.

What it implements, from the mathematics (SOUNDNESS.md, The Claim and lemmas N0, D, C1)
and Hosono's format description (a row `{"rectangle": [x1, y1, x2, y2], "mass": m}` is an
orbit representative whose eight images under the symmetries of K = [0, L]^2 carry m/8
each, spread uniformly; coinciding images add):

- a strict reader: one gzip member and nothing after it, JSON with duplicate keys
  refused, every number kept as its exact token, rationals parsed by a strict pattern;
- the D4 expansion with exact merging;
- the net (t_r = r D, cos = (1 - t^2)/(1 + t^2), sin = 2t/(1 + t^2)) and the per-bin
  centre domain [rho(a_r), L - rho(a_r)], a_r = max(0, t_r - D/2);
- the capture F_r(c) of the closed square of side B, centre c, angle theta_r:
  exactly, by clipping each rectangle against the square's four half-planes in exact
  rationals (`capture_exact`), exactly again by integrating the vertical section length
  over its breakpoints (`capture_exact_sections`, a second method), and in binary64 by the
  section method vectorized (`FloatMeasure.capture`), for searching only.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import re
import zlib
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
from gmpy2 import mpq

RATIONAL = re.compile(r"^(-?)(\d{1,400})/(\d{1,400})$")
DECIMAL = re.compile(r"^(-?)(\d{1,400})(?:\.(\d{1,400}))?$")


class Refusal(Exception):
    """A reading or premise this review refuses."""


def rational(token: Any) -> Fraction:
    """An exact rational from a JSON string or number token, by a strict pattern."""
    if isinstance(token, bool) or token is None:
        raise Refusal(f"not a number: {token!r}")
    text = str(token)
    match = RATIONAL.match(text)
    if match:
        if int(match.group(3)) == 0:
            raise Refusal(f"zero denominator: {text}")
        value = Fraction(int(match.group(2)), int(match.group(3)))
        return -value if match.group(1) else value
    match = DECIMAL.match(text)
    if match:
        whole, frac = match.group(2), match.group(3) or ""
        value = Fraction(int(whole + frac), 10 ** len(frac))
        return -value if match.group(1) else value
    raise Refusal(f"not an exact rational token: {text!r}")


def _no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise Refusal(f"duplicate JSON key {key!r}")
        out[key] = value
    return out


def _refuse_constant(name: str) -> Any:
    raise Refusal(f"non-finite JSON constant {name}")


@dataclass
class Read:
    raw_sha256: str
    text_sha256: str
    raw_bytes: int
    text_bytes: int
    data: dict[str, Any]


def read_gzip_json(path: Path) -> Read:
    """Read one gzip member holding JSON; refuse trailing bytes or a second member."""
    raw = path.read_bytes()
    if raw[:2] == b"\x1f\x8b":
        stream = zlib.decompressobj(wbits=16 + zlib.MAX_WBITS)
        text = stream.decompress(raw, 256 * 1024 * 1024)
        if not stream.eof or stream.unused_data or stream.unconsumed_tail:
            raise Refusal(f"{path.name}: not exactly one complete gzip member")
        # The standard library's reader must see the same bytes.
        if gzip.decompress(raw) != text:
            raise Refusal(f"{path.name}: two gzip readers disagree")
    else:
        text = raw
    data = json.loads(
        text.decode("utf-8"),
        object_pairs_hook=_no_duplicates,
        parse_float=str,
        parse_int=int,
        parse_constant=_refuse_constant,
    )
    if not isinstance(data, dict):
        raise Refusal("the certificate is not a JSON object")
    return Read(
        raw_sha256=hashlib.sha256(raw).hexdigest(),
        text_sha256=hashlib.sha256(text).hexdigest(),
        raw_bytes=len(raw),
        text_bytes=len(text),
        data=data,
    )


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------------------
# The measure


@dataclass
class Certificate:
    n: int
    side: Fraction
    core: Fraction
    step: Fraction
    last: int
    rows: list[tuple[Fraction, Fraction, Fraction, Fraction, Fraction]]
    total_mass_declared: Fraction | None
    keys: list[str]

    @property
    def count(self) -> int:
        return self.last + 1

    @property
    def mass(self) -> Fraction:
        return sum((row[4] for row in self.rows), Fraction(0))


def certificate(data: dict[str, Any], *, require_net: bool = True) -> Certificate:
    """Format M as Hosono describes it: `points` empty, `rectangles` of objects."""
    if not isinstance(data.get("n"), int) or isinstance(data.get("n"), bool):
        raise Refusal("n must be a JSON integer")
    points = data.get("points")
    if points != []:
        raise Refusal("format M needs an empty points list")
    rows_in = data.get("rectangles")
    if not isinstance(rows_in, list) or not rows_in:
        raise Refusal("no rectangles")
    rows: list[tuple[Fraction, Fraction, Fraction, Fraction, Fraction]] = []
    for index, row in enumerate(rows_in):
        if not isinstance(row, dict) or set(row) != {"rectangle", "mass"}:
            raise Refusal(f"row {index} is not exactly a rectangle and a mass")
        geometry = row["rectangle"]
        if not isinstance(geometry, list) or len(geometry) != 4:
            raise Refusal(f"row {index} needs four coordinates")
        x1, y1, x2, y2 = (rational(value) for value in geometry)
        rows.append((x1, y1, x2, y2, rational(row["mass"])))
    net = data.get("proof_net")
    if net is None:
        if require_net:
            raise Refusal("no proof_net")
        step, last = Fraction(83, 40000), 200
    else:
        if not isinstance(net, dict) or not set(net) <= {"step", "last", "count"}:
            raise Refusal("proof_net must hold step and last, and at most count")
        last_value = net.get("last")
        if not isinstance(last_value, int) or isinstance(last_value, bool) or last_value < 0:
            raise Refusal("proof_net.last must be a nonnegative JSON integer")
        if "count" in net and net["count"] != last_value + 1:
            raise Refusal("proof_net.count is not last + 1")
        step, last = rational(net["step"]), last_value
    total = data.get("total_mass")
    return Certificate(
        n=data["n"],
        side=rational(data["L"]),
        core=rational(data["B"]),
        step=step,
        last=last,
        rows=rows,
        total_mass_declared=None if total is None else rational(total),
        keys=list(data),
    )


def d4_images(
    side: Fraction, x1: Fraction, y1: Fraction, x2: Fraction, y2: Fraction
) -> list[tuple[Fraction, Fraction, Fraction, Fraction]]:
    """The images of [x1, x2] x [y1, y2] under the eight symmetries of [0, L]^2, each as
    (x1, y1, x2, y2), computed by mapping both corners and sorting."""
    maps = (
        lambda x, y: (x, y),
        lambda x, y: (side - x, y),
        lambda x, y: (x, side - y),
        lambda x, y: (side - x, side - y),
        lambda x, y: (y, x),
        lambda x, y: (side - y, x),
        lambda x, y: (y, side - x),
        lambda x, y: (side - y, side - x),
    )
    out = []
    for f in maps:
        ax, ay = f(x1, y1)
        bx, by = f(x2, y2)
        out.append((min(ax, bx), min(ay, by), max(ax, bx), max(ay, by)))
    return out


@dataclass
class Image:
    x1: Fraction
    y1: Fraction
    x2: Fraction
    y2: Fraction
    density: Fraction


def expand(cert: Certificate) -> list[Image]:
    """Every distinct image with its exact merged density (mass/8 over area, summed)."""
    merged: dict[tuple[Fraction, Fraction, Fraction, Fraction], Fraction] = {}
    for x1, y1, x2, y2, mass in cert.rows:
        if mass == 0:
            continue
        density = mass / 8 / ((x2 - x1) * (y2 - y1))
        for key in d4_images(cert.side, x1, y1, x2, y2):
            merged[key] = merged.get(key, Fraction(0)) + density
    return [Image(*key, density) for key, density in merged.items()]


# ---------------------------------------------------------------------------------------
# The net and the per-bin domain


def node(step: Fraction, index: int) -> tuple[Fraction, Fraction, Fraction]:
    """Half-angle tangent, cosine and sine of net index `index`."""
    t = step * index
    return t, (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def rho(a: Fraction) -> Fraction:
    """Half the axis-parallel extent of a unit square at half-angle tangent a."""
    return (1 + 2 * a - a * a) / (2 * (1 + a * a))


def bin_low(step: Fraction, index: int) -> Fraction:
    return max(Fraction(0), step * index - step / 2)


def domain(cert: Certificate, index: int) -> tuple[Fraction, Fraction]:
    """The per-bin centre domain [rho(a_r), L - rho(a_r)] on either axis."""
    low = rho(bin_low(cert.step, index))
    return low, cert.side - low


# ---------------------------------------------------------------------------------------
# Exact capture, method 1: clip each rectangle by the square's four half-planes


def q(value: Fraction) -> mpq:
    return mpq(value.numerator, value.denominator)


@dataclass
class ExactMeasure:
    """The expanded measure in gmpy2 rationals, with binary64 boxes for prefiltering."""

    side: mpq
    core: mpq
    step: mpq
    x1: list[mpq]
    y1: list[mpq]
    x2: list[mpq]
    y2: list[mpq]
    density: list[mpq]
    box: np.ndarray  # (k, 4) binary64 x1, y1, x2, y2, for prefiltering only

    @classmethod
    def of(cls, cert: Certificate, images: list[Image], *, scale: Fraction = Fraction(1)) -> ExactMeasure:
        return cls(
            side=q(cert.side),
            core=q(cert.core),
            step=q(cert.step),
            x1=[q(i.x1) for i in images],
            y1=[q(i.y1) for i in images],
            x2=[q(i.x2) for i in images],
            y2=[q(i.y2) for i in images],
            density=[q(i.density * scale) for i in images],
            box=np.array([[float(i.x1), float(i.y1), float(i.x2), float(i.y2)] for i in images]),
        )

    def direction(self, index: int) -> tuple[mpq, mpq]:
        t = self.step * index
        return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)

    def near(self, cx: float, cy: float, reach: float) -> np.ndarray:
        """Indices of rectangles whose box comes within `reach` + 1e-6 of the centre's
        box; the margin is far above binary64 error at these magnitudes, so no rectangle
        that meets the square is dropped."""
        margin = reach + 1e-6
        b = self.box
        mask = (b[:, 2] > cx - margin) & (b[:, 0] < cx + margin)
        mask &= (b[:, 3] > cy - margin) & (b[:, 1] < cy + margin)
        return np.nonzero(mask)[0]


def _clip(poly: list[tuple[mpq, mpq]], a: mpq, b: mpq, c: mpq) -> list[tuple[mpq, mpq]]:
    """Keep the part of a convex polygon with a x + b y <= c (Sutherland-Hodgman)."""
    out: list[tuple[mpq, mpq]] = []
    count = len(poly)
    for i in range(count):
        p = poly[i]
        r = poly[(i + 1) % count]
        dp = a * p[0] + b * p[1] - c
        dr = a * r[0] + b * r[1] - c
        if dp <= 0:
            out.append(p)
        if (dp < 0 < dr) or (dr < 0 < dp):
            s = dp / (dp - dr)
            out.append((p[0] + s * (r[0] - p[0]), p[1] + s * (r[1] - p[1])))
    return out


def _area(poly: list[tuple[mpq, mpq]]) -> mpq:
    total = mpq(0)
    count = len(poly)
    for i in range(count):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % count]
        total += x0 * y1 - x1 * y0
    return abs(total) / 2


def capture_exact(m: ExactMeasure, index: int, cx: mpq, cy: mpq) -> tuple[mpq, dict[str, int]]:
    """F_r(c) exactly: the sum over images of density times |R ∩ Q_r(c)|."""
    cos, sin = m.direction(index)
    h = m.core / 2
    # The square is {p : |u.(p - c)| <= h, |v.(p - c)| <= h}, u = (cos, sin), v = (-sin, cos).
    uc = cos * cx + sin * cy
    vc = -sin * cx + cos * cy
    planes = (
        (cos, sin, uc + h),
        (-cos, -sin, -uc + h),
        (-sin, cos, vc + h),
        (sin, -cos, -vc + h),
    )
    reach = float(h * (cos + sin))
    total = mpq(0)
    stats = {"near": 0, "inside": 0, "clipped": 0, "outside": 0}
    for k in m.near(float(cx), float(cy), reach):
        stats["near"] += 1
        x1, y1, x2, y2 = m.x1[k], m.y1[k], m.x2[k], m.y2[k]
        corners = ((x1, y1), (x2, y1), (x2, y2), (x1, y2))
        inside = True
        outside = False
        for a, b, c in planes:
            values = [a * x + b * y - c for x, y in corners]
            if all(v > 0 for v in values):
                outside = True
                break
            if any(v > 0 for v in values):
                inside = False
        if outside:
            stats["outside"] += 1
            continue
        if inside:
            stats["inside"] += 1
            total += m.density[k] * (x2 - x1) * (y2 - y1)
            continue
        poly: list[tuple[mpq, mpq]] = list(corners)
        for a, b, c in planes:
            poly = _clip(poly, a, b, c)
            if len(poly) < 3:
                break
        stats["clipped"] += 1
        if len(poly) >= 3:
            total += m.density[k] * _area(poly)
    return total, stats


# ---------------------------------------------------------------------------------------
# Exact capture, method 2: integrate the vertical section length between breakpoints


def _section(
    x: mpq, y1: mpq, y2: mpq, cos: mpq, sin: mpq, h: mpq
) -> mpq:
    """Length of the vertical section of R ∩ Q at local abscissa x (sin > 0)."""
    top = min(y2, (h - cos * x) / sin, (sin * x + h) / cos)
    bottom = max(y1, (-h - cos * x) / sin, (sin * x - h) / cos)
    return max(mpq(0), top - bottom)


def capture_exact_sections(m: ExactMeasure, index: int, cx: mpq, cy: mpq) -> mpq:
    """F_r(c) exactly by the second method; needs index >= 1 (sin > 0)."""
    if index < 1:
        raise ValueError("the section method needs an oblique direction")
    cos, sin = m.direction(index)
    h = m.core / 2
    reach_exact = h * (cos + sin)
    vertices = (h * (cos + sin), h * (cos - sin), -h * (cos - sin), -h * (cos + sin))
    total = mpq(0)
    for k in m.near(float(cx), float(cy), float(reach_exact)):
        x1, x2 = m.x1[k] - cx, m.x2[k] - cx
        y1, y2 = m.y1[k] - cy, m.y2[k] - cy
        lo = max(x1, -reach_exact)
        hi = min(x2, reach_exact)
        if lo >= hi:
            continue
        candidates = {lo, hi, *vertices}
        for y in (y1, y2):
            candidates.update(
                ((h - sin * y) / cos, (cos * y - h) / sin, (-h - sin * y) / cos, (cos * y + h) / sin)
            )
        xs = sorted(x for x in candidates if lo <= x <= hi)
        lengths = [_section(x, y1, y2, cos, sin, h) for x in xs]
        area = mpq(0)
        for i in range(len(xs) - 1):
            area += (xs[i + 1] - xs[i]) * (lengths[i] + lengths[i + 1]) / 2
        total += m.density[k] * area
    return total


# ---------------------------------------------------------------------------------------
# Binary64 capture by the section method, vectorized: for searching only, decides nothing


@dataclass
class FloatMeasure:
    x1: np.ndarray
    y1: np.ndarray
    x2: np.ndarray
    y2: np.ndarray
    density: np.ndarray
    core: float
    step: Fraction

    @classmethod
    def of(cls, cert: Certificate, images: list[Image]) -> FloatMeasure:
        return cls(
            x1=np.array([float(i.x1) for i in images]),
            y1=np.array([float(i.y1) for i in images]),
            x2=np.array([float(i.x2) for i in images]),
            y2=np.array([float(i.y2) for i in images]),
            density=np.array([float(i.density) for i in images]),
            core=float(cert.core),
            step=cert.step,
        )

    def direction(self, index: int) -> tuple[float, float]:
        t = self.step * index
        return float((1 - t * t) / (1 + t * t)), float(2 * t / (1 + t * t))

    def capture(self, index: int, cx: float, cy: float) -> float:
        cos, sin = self.direction(index)
        h = self.core / 2
        reach = h * (cos + sin)
        mask = (self.x2 > cx - reach) & (self.x1 < cx + reach)
        mask &= (self.y2 > cy - reach) & (self.y1 < cy + reach)
        x1 = self.x1[mask] - cx
        x2 = self.x2[mask] - cx
        y1 = self.y1[mask] - cy
        y2 = self.y2[mask] - cy
        dens = self.density[mask]
        if sin == 0.0:
            ox = np.clip(np.minimum(x2, h) - np.maximum(x1, -h), 0.0, None)
            oy = np.clip(np.minimum(y2, h) - np.maximum(y1, -h), 0.0, None)
            return float(np.sum(dens * ox * oy))
        lo = np.maximum(x1, -reach)
        hi = np.minimum(x2, reach)
        ones = np.ones_like(x1)
        columns = [
            lo,
            hi,
            h * (cos + sin) * ones,
            h * (cos - sin) * ones,
            -h * (cos - sin) * ones,
            -h * (cos + sin) * ones,
        ]
        for y in (y1, y2):
            columns += [
                (h - sin * y) / cos,
                (cos * y - h) / sin,
                (-h - sin * y) / cos,
                (cos * y + h) / sin,
            ]
        xs = np.stack(columns, axis=1)
        xs = np.clip(xs, lo[:, None], np.maximum(hi, lo)[:, None])
        xs.sort(axis=1)
        top = np.minimum(np.minimum(y2[:, None], (h - cos * xs) / sin), (sin * xs + h) / cos)
        bottom = np.maximum(np.maximum(y1[:, None], (-h - cos * xs) / sin), (sin * xs - h) / cos)
        length = np.clip(top - bottom, 0.0, None)
        area = np.sum((xs[:, 1:] - xs[:, :-1]) * (length[:, 1:] + length[:, :-1]), axis=1) / 2
        return float(np.sum(dens * area))


def exact_of_float(value: float) -> mpq:
    """The exact rational value of a binary64 number."""
    f = Fraction(value)
    return mpq(f.numerator, f.denominator)


def fraction_of(value: mpq) -> Fraction:
    return Fraction(int(value.numerator), int(value.denominator))


def short(value: Fraction | mpq, digits: int = 15) -> str:
    """A decimal rendering for reading; the exact value is kept beside it."""
    return f"{float(value):.{digits}g}"


def dumps(obj: Any, levels: int = 2, depth: int = 0) -> str:
    """JSON indented for `levels` levels and compact below, so a receipt stays readable
    and short: each record of a list is one line."""
    if depth >= levels or not isinstance(obj, (dict, list)) or not obj:
        return json.dumps(obj, ensure_ascii=False, separators=(", ", ": "))
    pad = " " * (depth + 1)
    if isinstance(obj, dict):
        items = [f"{pad}{json.dumps(str(key))}: {dumps(value, levels, depth + 1)}" for key, value in obj.items()]
        return "{\n" + ",\n".join(items) + "\n" + " " * depth + "}"
    items = [pad + dumps(value, levels, depth + 1) for value in obj]
    return "[\n" + ",\n".join(items) + "\n" + " " * depth + "]"
