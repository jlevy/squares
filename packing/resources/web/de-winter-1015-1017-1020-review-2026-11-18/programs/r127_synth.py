"""Synthetic packings for the self-test and for pricing: none is a certificate.

Lane r127-1118.  Written for this review; imports only its own modules.
"""

from __future__ import annotations

import random
from fractions import Fraction

from r127_read import Packing, centre_corners


def pyth(m: int, k: int) -> tuple[Fraction, Fraction]:
    """The rational unit vector ((m^2 - k^2), 2mk) / (m^2 + k^2)."""
    h = m * m + k * k
    return Fraction(m * m - k * k, h), Fraction(2 * m * k, h)


def from_frames(side, centres, dirs, form="centre") -> Packing:
    corners = [centre_corners(c, u) for c, u in zip(centres, dirs, strict=True)]
    return Packing(n=len(centres), side=Fraction(side), corners=corners, form=form,
                   centres=list(centres), directions=list(dirs))


def grid(nx: int, ny: int, gap: Fraction = Fraction(0), side: Fraction | None = None) -> Packing:
    cs, us = [], []
    for j in range(ny):
        for i in range(nx):
            cs.append((Fraction(1, 2) + i * (1 + gap), Fraction(1, 2) + j * (1 + gap)))
            us.append((Fraction(1), Fraction(0)))
    if side is None:
        side = max(nx, ny) * (1 + gap) - gap
    return from_frames(side, cs, us)


def realistic(n: int = 127, seed: int = 1, digits: int = 30) -> Packing:
    """n squares on a grid of pitch 1 + 1e-3, each turned by a tiny rational angle with
    long denominators and set off-centre by a little, inside a box with 1e-12 to spare at
    the right and top.  Every pair is apart by construction (pitch less extent)."""
    rnd = random.Random(seed)
    cols = 12
    pitch = 1 + Fraction(1, 1000)
    cs, us = [], []
    for k in range(n):
        i, j = k % cols, k // cols
        m = rnd.randrange(10**digits, 10 ** (digits + 1))
        kk = rnd.randrange(1, 10 ** (digits - 4))
        u = pyth(m, kk)  # angle below 2e-4 rad
        jitter = Fraction(rnd.randrange(-10**digits, 10**digits), 10 ** (digits + 6))
        cs.append((Fraction(1, 2) + Fraction(1, 2000) + i * pitch + jitter,
                   Fraction(1, 2) + Fraction(1, 2000) + j * pitch - jitter))
        us.append(u)
    side = cols * pitch + Fraction(1, 10**12)
    return from_frames(side, cs, us)
