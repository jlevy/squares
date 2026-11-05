"""Exact arithmetic for a check2 fine-net candidate (format M on a declared net).

Written for the stage-4 review think-1lri of wand125's mixed_n29_L582 (T-132),
from the claim's definitions in the source's SPEC.md sections 2 and 3 and the
crate's SOUNDNESS.md ("The Claim", lemma N0, lemma D).  It adapts the module of
the 4 November n = 28 and n = 30 review (think-4ul6) after re-reading it line by
line; the changes are listed in the README.  It imports nothing from the crate,
the repository's tools or the source, and uses the Python standard library only.

Everything here is exact: coordinates, masses, the net, the domains and the
capture are fractions.Fraction.  No float enters a value a function returns,
except where its docstring says the value is for display.
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

F = Fraction
ZERO = F(0)
ONE = F(1)

# The two spellings a canonical exact number may take in a candidate: a plain
# decimal or a ratio of nonnegative integers, with no sign, exponent, space or
# underscore.  Python's Fraction() accepts more than this (whitespace, exponents,
# underscores), and another reader might read those differently, so the review
# holds every number of the candidate to these forms.
CANONICAL = re.compile(r"(0|[1-9][0-9]*)(\.[0-9]+)?|(0|[1-9][0-9]*)/[1-9][0-9]*")


class DuplicateKey(ValueError):
    pass


def _no_duplicates(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise DuplicateKey(key)
        seen[key] = value
    return seen


def read_bytes(path: Path) -> bytes:
    """The candidate's JSON bytes; a .gz file must be exactly one gzip member."""
    raw = Path(path).read_bytes()
    if raw[:2] == b"\x1f\x8b":
        d = zlib.decompressobj(wbits=31)
        data = d.decompress(raw) + d.flush()
        if not d.eof or d.unused_data:
            raise ValueError("gzip input is not exactly one member")
        if data != gzip.decompress(raw):
            raise ValueError("gzip readers disagree")
        return data
    return raw


def rational(value) -> Fraction:
    """A canonical decimal or p/q string, or a JSON integer, as the rational it denotes."""
    if isinstance(value, bool):
        raise TypeError("boolean is not a number")
    if isinstance(value, int):
        return F(value)
    if isinstance(value, str):
        if not CANONICAL.fullmatch(value):
            raise ValueError(f"not a canonical exact number: {value!r}")
        return F(value)
    raise TypeError(f"not an exact number: {value!r}")


@dataclass(frozen=True)
class Candidate:
    path: str
    raw: bytes
    doc: dict
    n: int
    L: Fraction
    B: Fraction
    D: Fraction
    last: int
    total_mass: Fraction
    rows: tuple  # (((x1, y1, x2, y2), mass), ...)

    @property
    def count(self) -> int:
        return self.last + 1

    @property
    def h(self) -> Fraction:
        return self.B / 2

    @property
    def file_sha256(self) -> str:
        return hashlib.sha256(self.raw).hexdigest()

    def semantic_digest(self) -> str:
        """REPRODUCE.md's candidate_digest: SHA-256 of the JSON of
        {n, L, B, rectangles, points, total_mass, proof_net}, sorted keys, no spaces
        (json.dumps defaults otherwise, as fine_net_check.sh writes it)."""
        keys = ["n", "L", "B", "rectangles", "points", "total_mass", "proof_net"]
        sub = {k: self.doc[k] for k in keys}
        text = json.dumps(sub, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(text.encode()).hexdigest()


def load_candidate(path) -> Candidate:
    raw = read_bytes(Path(path))
    doc = json.loads(raw, object_pairs_hook=_no_duplicates)
    if not isinstance(doc.get("n"), int) or isinstance(doc.get("n"), bool):
        raise ValueError("n is not a JSON integer")
    rows = []
    for row in doc["rectangles"]:
        if set(row) != {"rectangle", "mass"}:
            raise ValueError(f"row keys {sorted(row)}")
        if len(row["rectangle"]) != 4:
            raise ValueError("a rectangle is not four numbers")
        x1, y1, x2, y2 = (rational(v) for v in row["rectangle"])
        rows.append(((x1, y1, x2, y2), rational(row["mass"])))
    net = doc["proof_net"]
    if not isinstance(net["last"], int) or isinstance(net["last"], bool):
        raise ValueError("last is not a JSON integer")
    return Candidate(
        path=str(path),
        raw=raw,
        doc=doc,
        n=doc["n"],
        L=rational(doc["L"]),
        B=rational(doc["B"]),
        D=rational(net["step"]),
        last=net["last"],
        total_mass=rational(doc["total_mass"]),
        rows=tuple(rows),
    )


def scaled_copy_text(cand: Candidate, factor: Fraction) -> str:
    """The mutant file the shipped fine_net_check.sh writes for its control:
    json.load, every mass times factor written as str(Fraction), total_mass
    re-summed over rectangles and points, json.dump with its defaults."""
    d = json.loads(cand.raw)
    for row in d["rectangles"]:
        row["mass"] = str(F(row["mass"]) * factor)
    for row in d.get("points", []):
        row["mass"] = str(F(row["mass"]) * factor)
    d["total_mass"] = str(sum((F(x["mass"]) for x in d["rectangles"] + d.get("points", [])), F(0)))
    return json.dumps(d)


# ---------------------------------------------------------------------------
# The measure: the D4 average of the listed rectangles (SPEC.md section 2).


def d4_images(L, x1, y1, x2, y2):
    """The eight images of [x1, x2] x [y1, y2] under the symmetries of [0, L]^2,
    as (x1, y1, x2, y2): with or without swapping x and y, times x -> L - x,
    times y -> L - y."""
    out = []
    for swap in (False, True):
        a1, b1, a2, b2 = (y1, x1, y2, x2) if swap else (x1, y1, x2, y2)
        for fx in (False, True):
            for fy in (False, True):
                u1, u2 = (L - a2, L - a1) if fx else (a1, a2)
                v1, v2 = (L - b2, L - b1) if fy else (b1, b2)
                out.append((u1, v1, u2, v2))
    return out


def images(cand: Candidate, scale: Fraction = ONE):
    """Every image with its density scale * m / (8 |R|), unmerged: a list of
    (x1, y1, x2, y2, density).  Coincident images stay separate terms, which is
    the same density function as merging them."""
    out = []
    for (x1, y1, x2, y2), m in cand.rows:
        if m == 0:
            continue
        dens = scale * m / (8 * (x2 - x1) * (y2 - y1))
        for im in d4_images(cand.L, x1, y1, x2, y2):
            out.append((*im, dens))
    return out


# ---------------------------------------------------------------------------
# The net and the domains (lemma N0, lemma D).


def direction(D: Fraction, r: int):
    """Exact (cos theta_r, sin theta_r) for theta_r = 2 atan(r D)."""
    t = D * r
    den = 1 + t * t
    return (1 - t * t) / den, 2 * t / den


def rho(a: Fraction) -> Fraction:
    """Half-width of a unit square at half-angle tangent a:
    (cos phi + sin phi)/2 = (1 + 2a - a^2) / (2 (1 + a^2))."""
    return (1 + 2 * a - a * a) / (2 * (1 + a * a))


def bin_low(D: Fraction, r: int) -> Fraction:
    """a_r = max(0, r D - D/2), the least half-angle tangent assigned to node r."""
    return max(ZERO, D * r - D / 2)


def per_bin_domain(cand: Candidate, r: int):
    """(lo, hi) with lo = rho(a_r) and hi = L - rho(a_r): every centre of [lo, hi]^2."""
    lo = rho(bin_low(cand.D, r))
    return lo, cand.L - lo


def tokoharu_half(cand: Candidate, r: int) -> Fraction:
    c, s = direction(cand.D, r)
    return cand.B * (c + s) / 2


# ---------------------------------------------------------------------------
# The exact capture of a closed core.


def core_polygon(px, py, c, s, hu, hv=None):
    """The rectangle {q : |u.(q - p)| <= hu, |v.(q - p)| <= hv}, u = (c, s),
    v = (-s, c), as its four vertices in counterclockwise order (hv = hu: the core)."""
    if hv is None:
        hv = hu
    ux, uy = hu * c, hu * s
    vx, vy = -hv * s, hv * c
    return [
        (px + ux + vx, py + uy + vy),
        (px - ux + vx, py - uy + vy),
        (px - ux - vx, py - uy - vy),
        (px + ux - vx, py + uy - vy),
    ]


def _clip(poly, inside, cross):
    out = []
    n = len(poly)
    for i in range(n):
        p = poly[i]
        q = poly[(i + 1) % n]
        ip, iq = inside(p), inside(q)
        if ip:
            out.append(p)
            if not iq:
                out.append(cross(p, q))
        elif iq:
            out.append(cross(p, q))
    return out


def _cross_x(x0):
    def cross(p, q):
        t = (x0 - p[0]) / (q[0] - p[0])
        return (x0, p[1] + t * (q[1] - p[1]))

    return cross


def _cross_y(y0):
    def cross(p, q):
        t = (y0 - p[1]) / (q[1] - p[1])
        return (p[0] + t * (q[0] - p[0]), y0)

    return cross


def clip_area(poly, x1, y1, x2, y2) -> Fraction:
    """Exact area of a convex polygon intersected with [x1, x2] x [y1, y2]
    (Sutherland-Hodgman against the four half-planes, then the shoelace sum)."""
    for inside, cross in (
        (lambda p: p[0] >= x1, _cross_x(x1)),
        (lambda p: p[0] <= x2, _cross_x(x2)),
        (lambda p: p[1] >= y1, _cross_y(y1)),
        (lambda p: p[1] <= y2, _cross_y(y2)),
    ):
        poly = _clip(poly, inside, cross)
        if len(poly) < 3:
            return ZERO
    acc = ZERO
    n = len(poly)
    for i in range(n):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % n]
        acc += ax * by - bx * ay
    return abs(acc) / 2


def capture_poly(ims, poly, detail: bool = False):
    """Exact integral of the density over a convex polygon.  An image whose box
    misses the polygon's bounding box (compared exactly) contributes zero."""
    xs = [v[0] for v in poly]
    ys = [v[1] for v in poly]
    bx1, bx2, by1, by2 = min(xs), max(xs), min(ys), max(ys)
    total = ZERO
    met = 0
    for x1, y1, x2, y2, dens in ims:
        if x2 <= bx1 or x1 >= bx2 or y2 <= by1 or y1 >= by2:
            continue
        a = clip_area(poly, x1, y1, x2, y2)
        if a:
            met += 1
            total += dens * a
    if detail:
        return total, met
    return total


def capture(ims, px, py, c, s, h, detail: bool = False):
    """Exact capture of the closed core at centre (px, py), direction (c, s) and
    half-side h.  The density's support is a finite union of rectangles, so the
    closed and the open core capture the same mass."""
    return capture_poly(ims, core_polygon(px, py, c, s, h), detail)


def axis_overlap(x, h, a, b) -> Fraction:
    """|[x - h, x + h] intersected with [a, b]|."""
    return max(ZERO, min(x + h, b) - max(x - h, a))


def axis_capture(ims, px, py, h):
    """The exact capture of the axis-aligned core (direction 0), as a sum of
    products of overlaps; equal to capture(..., 1, 0, h)."""
    total = ZERO
    for x1, y1, x2, y2, dens in ims:
        ox = axis_overlap(px, h, x1, x2)
        if ox:
            oy = axis_overlap(py, h, y1, y2)
            if oy:
                total += dens * ox * oy
    return total


def fmt(q: Fraction, digits: int = 16) -> str:
    """A decimal display of a fraction, truncated toward zero (display only)."""
    sign = "-" if q < 0 else ""
    q = abs(q)
    whole = q.numerator // q.denominator
    rest = q - whole
    frac = (rest * 10**digits).numerator // (rest * 10**digits).denominator
    return f"{sign}{whole}.{frac:0{digits}d}"
