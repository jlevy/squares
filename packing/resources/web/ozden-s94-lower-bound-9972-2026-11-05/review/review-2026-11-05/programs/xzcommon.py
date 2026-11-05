"""Shared exact helpers for the think-xzxd stage 4 review of #910's certificate.

Written for this review from the mathematics (sqverify_fast/SOUNDNESS.md, "The Claim",
lemmas N0, D and C1, read as a specification) and the certificate's own JSON. It reads
no checker's source code. Every quantity here is an exact rational (gmpy2.mpq).

The certificate's measure (format M): each row is an orbit representative
R = [x1, x2] x [y1, y2], listed as [x1, y1, x2, y2], with mass w >= 0; its eight images
under the symmetry group D4 of K = [0, L]^2 each carry w/8 spread uniformly. Images that
coincide are the same set and their densities add.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import zlib
from dataclasses import dataclass
from pathlib import Path

from gmpy2 import mpq

Rect = tuple[mpq, mpq, mpq, mpq]  # (x1, y1, x2, y2)


def read_bytes(path: Path) -> bytes:
    """The decompressed bytes of a file, refusing a gzip with any byte after one member."""
    raw = path.read_bytes()
    if raw[:2] != b"\x1f\x8b":
        return raw
    d = zlib.decompressobj(wbits=31)
    out = d.decompress(raw) + d.flush()
    if not d.eof or d.unused_data:
        raise ValueError(f"{path}: not exactly one gzip member")
    if out != gzip.decompress(raw):
        raise ValueError(f"{path}: gzip readers disagree")
    return out


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strict_json(data: bytes) -> dict[str, object]:
    """Parse JSON refusing duplicate keys and any non-integer number token."""

    def no_dupes(pairs: list[tuple[str, object]]) -> dict[str, object]:
        out: dict[str, object] = {}
        for k, v in pairs:
            if k in out:
                raise ValueError(f"duplicate key {k!r}")
            out[k] = v
        return out

    def no_float(token: str) -> object:
        raise ValueError(f"non-integer number token {token!r}")

    obj = json.loads(data, object_pairs_hook=no_dupes, parse_float=no_float)
    if not isinstance(obj, dict):
        raise ValueError("top level is not an object")
    return obj


def q(text: object) -> mpq:
    """An exact rational from a JSON string 'a/b' or 'a' (never from a float)."""
    if not isinstance(text, str):
        raise ValueError(f"expected a string rational, got {text!r}")
    return mpq(text)


@dataclass(frozen=True)
class Certificate:
    n: int
    L: mpq
    B: mpq
    D: mpq
    last: int
    total_mass: mpq
    rows: list[tuple[mpq, Rect]]  # (mass, rectangle)
    raw: dict[str, object]


def load_certificate(path: Path) -> Certificate:
    obj = strict_json(read_bytes(path))
    net = obj["proof_net"]
    assert isinstance(net, dict)
    last = net["last"]
    assert isinstance(last, int) and not isinstance(last, bool)
    rows: list[tuple[mpq, Rect]] = []
    rects = obj["rectangles"]
    assert isinstance(rects, list)
    for row in rects:
        assert isinstance(row, dict) and set(row) == {"mass", "rectangle"}
        coords = row["rectangle"]
        assert isinstance(coords, list) and len(coords) == 4
        x1, y1, x2, y2 = (q(v) for v in coords)
        rows.append((q(row["mass"]), (x1, y1, x2, y2)))
    n = obj["n"]
    assert isinstance(n, int)
    return Certificate(
        n=n,
        L=q(obj["L"]),
        B=q(obj["B"]),
        D=q(net["step"]),
        last=last,
        total_mass=q(obj["total_mass"]),
        rows=rows,
        raw=obj,
    )


def d4_images(L: mpq, rect: Rect) -> list[Rect]:
    """The eight images of [x1,x2]x[y1,y2] under the symmetries of [0,L]^2."""
    x1, y1, x2, y2 = rect
    out: list[Rect] = []
    for a1, a2, b1, b2 in ((x1, x2, y1, y2), (y1, y2, x1, x2)):  # identity, then y = x
        for fx in (False, True):
            for fy in (False, True):
                X = (L - a2, L - a1) if fx else (a1, a2)
                Y = (L - b2, L - b1) if fy else (b1, b2)
                out.append((X[0], Y[0], X[1], Y[1]))
    return out


def expand(cert: Certificate, mass_factor: mpq = mpq(1)) -> dict[Rect, mpq]:
    """Distinct expanded rectangles and their exact densities (images merged)."""
    dens: dict[Rect, mpq] = {}
    for w, rect in cert.rows:
        x1, y1, x2, y2 = rect
        area = (x2 - x1) * (y2 - y1)
        if w == 0:
            continue
        per_image = mass_factor * w / 8 / area
        for im in d4_images(cert.L, rect):
            dens[im] = dens.get(im, mpq(0)) + per_image
    return dens


@dataclass(frozen=True)
class Direction:
    r: int
    t: mpq
    c: mpq  # cos(theta_r), theta_r = 2 atan(t)
    s: mpq  # sin(theta_r)
    a: mpq  # lower end of the bin's half-angle tangents, max(0, t - D/2)
    margin: mpq  # rho(a): the per-bin wall margin of lemma D
    U: mpq  # upper end of the searched quadrant, L - rho(a)


def rho_half_width(a: mpq) -> mpq:
    """Half-width (cos phi + sin phi)/2 of a unit square at half-angle tangent a."""
    return (1 + 2 * a - a * a) / (2 * (1 + a * a))


def direction(cert: Certificate, r: int) -> Direction:
    t = mpq(r) * cert.D
    c = (1 - t * t) / (1 + t * t)
    s = 2 * t / (1 + t * t)
    a = max(mpq(0), t - cert.D / 2)
    m = rho_half_width(a)
    return Direction(r=r, t=t, c=c, s=s, a=a, margin=m, U=cert.L - m)


def frac_str(x: mpq) -> str:
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else f"{x.numerator}"
