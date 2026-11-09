"""Helpers shared by the L64 review programs: digests, exact decimal prints, receipts.

Lane L64, 2026-11-09, stage 4 review of issues 927 to 931. No geometry lives here, and
nothing here decides a certificate. Every print of a fraction is exact: a floor or a
ceiling at a stated number of places, or a truncation toward zero at a stated number of
significant digits. No binary floating point is used.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
import time
from fractions import Fraction
from pathlib import Path


def sha256_file(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def frac_str(x: Fraction) -> str:
    """Lowest terms, as p/q, or p when q is 1."""
    x = Fraction(x)
    if x.denominator == 1:
        return str(x.numerator)
    return f"{x.numerator}/{x.denominator}"


def floor_places(x: Fraction, places: int) -> Fraction:
    scale = 10**places
    return Fraction((x.numerator * scale) // x.denominator, scale)


def ceil_places(x: Fraction, places: int) -> Fraction:
    scale = 10**places
    return Fraction(-((-x.numerator * scale) // x.denominator), scale)


def fixed(x: Fraction, places: int, mode: str = "floor") -> str:
    """The exact floor (or ceiling) of x at `places` decimal places, as a string."""
    if mode == "floor":
        y = floor_places(x, places)
    elif mode == "ceil":
        y = ceil_places(x, places)
    else:
        raise ValueError(mode)
    scaled = y * 10**places
    assert scaled.denominator == 1
    v = scaled.numerator
    sign = "-" if v < 0 else ""
    v = abs(v)
    whole, frac = divmod(v, 10**places)
    if places == 0:
        return f"{sign}{whole}"
    return f"{sign}{whole}.{frac:0{places}d}"


def exp10(a: Fraction) -> int:
    """The largest e with 10**e <= a, for a > 0."""
    if a <= 0:
        raise ValueError("exp10 needs a positive number")
    e = len(str(a.numerator)) - len(str(a.denominator))
    while Fraction(10) ** e > a:
        e -= 1
    while Fraction(10) ** (e + 1) <= a:
        e += 1
    return e


def sci(x: Fraction, digits: int = 12) -> str:
    """x in scientific notation, truncated toward zero at `digits` significant digits."""
    x = Fraction(x)
    if x == 0:
        return "0"
    sign = "-" if x < 0 else ""
    a = abs(x)
    e = exp10(a)
    m = a / Fraction(10) ** e  # 1 <= m < 10
    scaled = m * 10 ** (digits - 1)
    mant = scaled.numerator // scaled.denominator
    s = str(mant)
    body = s[0] + ("." + s[1:] if len(s) > 1 else "")
    return f"{sign}{body}e{e:+d}"


def program_digests(paths: list[str | Path]) -> dict[str, str]:
    return {Path(p).name: sha256_file(p) for p in paths}


def environment() -> dict[str, str]:
    return {
        "python": sys.version.split()[0],
        "implementation": platform.python_implementation(),
        "isolated_mode": str(bool(sys.flags.isolated)),
        "nice": str(os.nice(0)),
    }


def write_receipt(path: str | Path, obj: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, indent=1, sort_keys=False, ensure_ascii=True) + "\n"
    path.write_text(text, encoding="ascii")


class Clock:
    """CPU and wall time of one program run."""

    def __init__(self) -> None:
        self.cpu0 = time.process_time()
        self.wall0 = time.perf_counter()
        self.started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def report(self) -> dict[str, str]:
        return {
            "started_utc": self.started,
            "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "cpu_seconds": f"{time.process_time() - self.cpu0:.2f}",
            "wall_seconds": f"{time.perf_counter() - self.wall0:.2f}",
        }
