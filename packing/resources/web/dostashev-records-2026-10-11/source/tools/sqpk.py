"""Shared helpers for the record pipeline: paths, the sqpk v1 writer/reader, decimals.

All numbers stay decimal strings. Arithmetic goes through `decimal.Decimal` or `mpmath` at
high precision; nothing here round-trips coordinates through `float`.

Scripts in `tools/` run as `uv run python -I tools/<script>.py`. `-I` keeps the script
directory off `sys.path`, so each script inserts `tools/` explicitly before importing this.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import dataclass, field
from decimal import Decimal, localcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
RECORDS = ROOT / "data" / "records"
CANDIDATES = RAW / "candidates"

# Digits kept when we have to compute a value (trig, sqrt, exact rationals -> decimal).
WORK_DIGITS = 60
# A literal with at least this many significant digits is presumed rounded (it sets the source
# precision); shorter ones (0.5, 45, s - 3.5 at the quoted side) are presumed exact.
ROUNDED_MIN_DIGITS = 12

_NUM_RE = re.compile(r"^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def check_decimal(s: str) -> str:
    """Return s if it is a plain decimal literal, else raise. Guards untrusted input."""
    s = s.strip()
    if not _NUM_RE.match(s):
        raise ValueError(f"not a decimal literal: {s!r}")
    return s


def sig_digits(s: str) -> int:
    """Significant digits of a decimal literal (trailing zeros after the point count)."""
    s = check_decimal(s).lstrip("+-")
    mant = re.split(r"[eE]", s)[0]
    digits = mant.replace(".", "").lstrip("0")
    return max(len(digits), 1)


def literal_digits(s: str) -> int:
    """Precision carried by a decimal literal, in significant digits.

    Normally its significant digits. A literal of <= 18 digits that equals a binary64 value to
    within half a unit of its last printed digit is a float dump (e.g. '%.17e'): printing more
    digits does not add precision, so it counts as 16 (binary64 is ~15.95 digits).
    """
    sd = sig_digits(s)
    if sd > 18 or sd <= 15:
        return sd
    with localcontext() as ctx:
        ctx.prec = 60
        x = Decimal(check_decimal(s))
        if x == 0:
            return sd
        half_ulp_printed = Decimal(10) ** (x.adjusted() - sd + 1) / 2
        if abs(Decimal(float(x)) - x) <= half_ulp_printed:
            return min(sd, 16)
    return sd


def fmt_decimal(x: Decimal, digits: int = WORK_DIGITS) -> str:
    """Format with `digits` significant digits, fixed-point, trailing zeros trimmed."""
    if x == 0:
        return "0"
    with localcontext() as ctx:
        ctx.prec = digits
        y = +x
    s = format(y, "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


def normalize_angle_deg(theta: Decimal) -> Decimal:
    """Reduce an angle in degrees to [0, 90)."""
    with localcontext() as ctx:
        ctx.prec = 400  # exact for any input we read (<= ~150 significant digits)
        r = theta % Decimal(90)
        if r < 0:
            r += Decimal(90)
        if r >= 90:
            r -= Decimal(90)
    return r


@dataclass
class Packing:
    n: int
    s: str
    squares: list[tuple[str, str, str]]  # (cx, cy, theta_deg) as decimal strings
    comments: list[str] = field(default_factory=list)

    def write(self, path: Path) -> None:
        if len(self.squares) != self.n:
            raise ValueError(f"n={self.n} but {len(self.squares)} squares")
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = ["# sqpk v1"]
        for c in self.comments:
            for part in str(c).splitlines():
                lines.append("# " + part if part else "#")
        lines.append(f"n {self.n}")
        lines.append(f"s {check_decimal(self.s)}")
        lines.append("# cx cy theta_deg")
        for cx, cy, th in self.squares:
            lines.append(f"{check_decimal(cx)} {check_decimal(cy)} {check_decimal(th)}")
        path.write_text("\n".join(lines) + "\n")


def read_sqpk(path: Path) -> Packing:
    n = None
    s = None
    sq: list[tuple[str, str, str]] = []
    comments: list[str] = []
    for line in path.read_text().splitlines():
        t = line.strip()
        if not t:
            continue
        if t.startswith("#"):
            c = t[1:].strip()
            if c not in ("sqpk v1", "cx cy theta_deg"):  # structural lines, re-emitted by write()
                comments.append(c)
            continue
        parts = t.split()
        if parts[0] == "n":
            n = int(parts[1])
        elif parts[0] == "s":
            s = check_decimal(parts[1])
        else:
            if len(parts) != 3:
                raise ValueError(f"{path}: bad data line {t!r}")
            sq.append(tuple(check_decimal(p) for p in parts))  # type: ignore[arg-type]
    if n is None or s is None or len(sq) != n:
        raise ValueError(f"{path}: header/data mismatch (n={n}, s={s}, lines={len(sq)})")
    return Packing(n, s, sq, comments)


def comment_value(p: Packing, key: str) -> str | None:
    for c in p.comments:
        if c.startswith(key + " "):
            return c[len(key) + 1 :].strip()
    return None


def trivial_grid(n: int) -> Packing:
    k = math.isqrt(n)
    if k * k < n:
        k += 1
    sq = []
    for i in range(n):
        x, y = i % k, i // k
        sq.append((f"{x}.5", f"{y}.5", "0"))
    return Packing(n, str(k), sq, [f"exact_s {k}"])


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1, ensure_ascii=False, sort_keys=False) + "\n")


def candidate_path(source: str, n: int) -> Path:
    return CANDIDATES / source / f"n{n:04d}.sqpk"
