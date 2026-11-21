"""Lane rR2 (issue 1042 derived bounds): read a rectangle measure exactly.

A measure file lists primitives: a rectangle [x0, y0, x1, y1] and a mass. Following the
source's prose (proof/INTEGER_CHECKER.md), each of the eight images of a primitive under
the symmetries of the board [0, S]^2 carries mass m/8, spread uniformly. This module reads
the file with exact rationals, checks its arithmetic, and lists the images on an integer
grid with exact densities. Standard library only; imports nothing from the source.
"""

from __future__ import annotations

import gzip
import json
from fractions import Fraction as F
from pathlib import Path

GRID = 10**8  # coordinates are integers in units of 1e-8 (checked, not assumed)


def read_json(path: str | Path) -> object:
    raw = Path(path).read_bytes()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return json.loads(raw)


def to_grid(value: F, what: str) -> int:
    scaled = value * GRID
    if scaled.denominator != 1:
        raise ValueError(f"{what} = {value} is not on the 1e-8 grid")
    return int(scaled)


def symmetries(side: int) -> list:
    """The eight maps of [0, side]^2 acting on integer rectangles (x0, y0, x1, y1)."""

    def f0(x0, y0, x1, y1):
        return (x0, y0, x1, y1)

    def f1(x0, y0, x1, y1):
        return (side - x1, y0, side - x0, y1)

    def f2(x0, y0, x1, y1):
        return (x0, side - y1, x1, side - y0)

    def f3(x0, y0, x1, y1):
        return (side - x1, side - y1, side - x0, side - y0)

    def f4(x0, y0, x1, y1):
        return (y0, x0, y1, x1)

    def f5(x0, y0, x1, y1):
        return (side - y1, x0, side - y0, x1)

    def f6(x0, y0, x1, y1):
        return (y0, side - x1, y1, side - x0)

    def f7(x0, y0, x1, y1):
        return (side - y1, side - x1, side - y0, side - x0)

    return [f0, f1, f2, f3, f4, f5, f6, f7]


class Measure:
    """Primitives on the integer grid with exact masses; `images()` expands the symmetry."""

    def __init__(self, side: F, prims: list[tuple[int, int, int, int, F]], n: int | None):
        self.side = side
        self.S = to_grid(side, "side")
        self.prims = prims
        self.n = n

    @classmethod
    def from_file(cls, path: str | Path) -> Measure:
        data = read_json(path)
        if not isinstance(data, dict):
            raise ValueError("measure file is not an object")
        side = F(data["L"])
        if data.get("points"):
            raise ValueError("point masses present; this checker reads rectangles only")
        prims = []
        for k, rec in enumerate(data["rectangles"]):
            x0, y0, x1, y1 = (F(v) for v in rec["rectangle"])
            mass = F(rec["mass"])
            if not (x0 < x1 and y0 < y1):
                raise ValueError(f"primitive {k} is degenerate")
            if mass < 0:
                raise ValueError(f"primitive {k} has negative mass")
            if not (0 <= x0 and x1 <= side and 0 <= y0 and y1 <= side):
                raise ValueError(f"primitive {k} leaves the board")
            prims.append((
                to_grid(x0, f"x0[{k}]"),
                to_grid(y0, f"y0[{k}]"),
                to_grid(x1, f"x1[{k}]"),
                to_grid(y1, f"y1[{k}]"),
                mass,
            ))
        total = sum((p[4] for p in prims), F(0))
        if total != F(data["total_mass"]):
            raise ValueError("sum of primitive masses differs from total_mass")
        return cls(side, prims, data.get("n"))

    def total(self) -> F:
        return sum((p[4] for p in self.prims), F(0))

    def with_masses(self, masses: dict[int, F]) -> Measure:
        prims = list(self.prims)
        for k, m in masses.items():
            if m < 0:
                raise ValueError(f"modified primitive {k} has negative mass")
            x0, y0, x1, y1, _ = prims[k]
            prims[k] = (x0, y0, x1, y1, m)
        return Measure(self.side, prims, self.n)

    def images(self) -> list[tuple[int, int, int, int, F]]:
        """Every image (x0, y0, x1, y1, density), density = (m/8)/area in real units."""
        out = []
        maps = symmetries(self.S)
        g2 = GRID * GRID
        for x0, y0, x1, y1, m in self.prims:
            if m == 0:
                continue
            for g in maps:
                a, b, c, d = g(x0, y0, x1, y1)
                area = (c - a) * (d - b)
                out.append((a, b, c, d, m * g2 / (8 * area)))
        return out


def image_mass(img: tuple[int, int, int, int, F]) -> F:
    x0, y0, x1, y1, dens = img
    return dens * (x1 - x0) * (y1 - y0) / (GRID * GRID)
