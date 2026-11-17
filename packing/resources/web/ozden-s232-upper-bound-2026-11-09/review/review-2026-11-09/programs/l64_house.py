"""Reader for this repository's house witnesses and regularized views (lane L64).

Not part of the frozen checker, and it decides no certificate. The house files on main
are UTF-8 (a credit key reads "Özden") and use YAML flow brackets in their `source`
blocks, which the certificate reader refuses by design. This module reads them as UTF-8
with the same duplicate-refusing BaseLoader and the same witness parser, so a house's
squares and side mean exactly what a certificate's would.

It also turns a parsed witness into exact corners, for corner and centre-basis files
alike: a centre c and basis u = (a, b) give the corners c - (u + w)/2, c + (u - w)/2,
c + (u + w)/2 and c - (u - w)/2 with w = (-b, a), counterclockwise, as the schema's
"[cos(theta), sin(theta)]" reading of the basis requires.
"""

from __future__ import annotations

import gzip
from fractions import Fraction as F
from pathlib import Path

import yaml

from l64_reader import ReadError, _parse_witness, _StrictLoader
from l64_util import sha256_file


def read_house(path: str | Path, expected_n: int | None = None) -> dict:
    path = Path(path)
    raw = path.read_bytes()
    data = gzip.decompress(raw) if path.suffix == ".gz" else raw
    text = data.decode("utf-8")
    if "\r" in text or "\t" in text:
        raise ReadError(f"{path.name}: carriage return or tab")
    doc = yaml.load(text, Loader=_StrictLoader)  # noqa: S506 - BaseLoader: strings only
    out = _parse_witness(doc, expected_n, ("corners", "center-basis"))
    out["path"] = str(path)
    out["sha256"] = sha256_file(path)
    return out


def exact_corners(sq: dict) -> list[tuple[F, F]]:
    """The square's four corners as Fractions, counterclockwise from centre and basis."""
    if "corners" in sq:
        return [(F(c[0], c[1]), F(c[2], c[3])) for c in sq["corners"]]
    cx, cy = F(sq["center"][0], sq["center"][1]), F(sq["center"][2], sq["center"][3])
    a, b = F(sq["basis"][0], sq["basis"][1]), F(sq["basis"][2], sq["basis"][3])
    ux, uy, wx, wy = a, b, -b, a
    return [
        (cx - (ux + wx) / 2, cy - (uy + wy) / 2),
        (cx + (ux - wx) / 2, cy + (uy - wy) / 2),
        (cx + (ux + wx) / 2, cy + (uy + wy) / 2),
        (cx - (ux - wx) / 2, cy - (uy - wy) / 2),
    ]


def as_int_corners(pts: list[tuple[F, F]]) -> list[tuple[int, int, int, int]]:
    return [(x.numerator, x.denominator, y.numerator, y.denominator) for x, y in pts]
