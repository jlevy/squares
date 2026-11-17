"""Lane L169 reader: a `.cert` text certificate read strictly into Python integers.

The format (Evan Daniel's convention, as issue #989 names it): a header line `n S`, then
one line `x y t` per square, where (x, y) is the square's centre and t = tan(theta/2).
Every scalar is an exact rational written canonically: an integer as `[-]D` (no sign on
zero, no leading zeros), any other value as `[-]P/Q` with Q >= 2, no leading zeros and
gcd(|P|, Q) = 1. Tokens are separated by single spaces. Every line ends with the same
terminator, CRLF or LF, the last line included; nothing else is accepted: no blank or
comment line, no trailing space, no byte outside printable ASCII.

The reader decides only the reading and the count. It hands the two methods integers:
each scalar as a pair (p, q) with q >= 1.
"""

from __future__ import annotations

import re
from math import gcd

_INT = re.compile(r"(-?)(0|[1-9][0-9]*)\Z")
_FRAC = re.compile(r"(-?)([1-9][0-9]*)/([1-9][0-9]*)\Z")


class ReadError(ValueError):
    """The text is not a canonical certificate."""


def scalar(tok: str) -> tuple[int, int]:
    """One canonical scalar as (p, q), q >= 1, gcd(|p|, q) = 1."""
    m = _INT.match(tok)
    if m:
        sign, digits = m.group(1), m.group(2)
        if digits == "0" and sign:
            raise ReadError(f"signed zero: {tok!r}")
        return (-int(digits) if sign else int(digits), 1)
    m = _FRAC.match(tok)
    if not m:
        raise ReadError(f"not a canonical rational: {tok!r}")
    sign, ps, qs = m.group(1), m.group(2), m.group(3)
    p, q = int(ps), int(qs)
    if q == 1:
        raise ReadError(f"integer written as a fraction: {tok!r}")
    if gcd(p, q) != 1:
        raise ReadError(f"not in lowest terms: {tok!r}")
    return (-p if sign else p, q)


def read_text(raw: bytes) -> dict:
    """Read a certificate's bytes. Returns {n, side, squares, terminator}."""
    if not raw:
        raise ReadError("empty file")
    for byte in raw:
        if not (byte in (10, 13) or 32 <= byte <= 126):
            raise ReadError(f"byte outside printable ASCII: {byte}")
    text = raw.decode("ascii")
    if text.endswith("\r\n"):
        term = "\r\n"
    elif text.endswith("\n"):
        term = "\n"
    else:
        raise ReadError("last line not terminated")
    body = text[: -len(term)]
    lines = body.split(term)
    for line in lines:
        if "\r" in line or "\n" in line:
            raise ReadError("mixed line terminators")
    header = lines[0].split(" ")
    if len(header) != 2:
        raise ReadError(f"header is not `n S`: {lines[0]!r}")
    n_p, n_q = scalar(header[0])
    if n_q != 1 or n_p < 1:
        raise ReadError(f"n is not a positive integer: {header[0]!r}")
    side = scalar(header[1])
    if side[0] <= 0:
        raise ReadError("side is not positive")
    rows = lines[1:]
    if len(rows) != n_p:
        raise ReadError(f"header says {n_p} squares, the file has {len(rows)} rows")
    squares = []
    for k, line in enumerate(rows, start=1):
        toks = line.split(" ")
        if len(toks) != 3 or any(not t for t in toks):
            raise ReadError(f"row {k} is not `x y t`: {line!r}")
        squares.append((scalar(toks[0]), scalar(toks[1]), scalar(toks[2])))
    return {"n": n_p, "side": side, "squares": squares, "terminator": term}


def read_file(path: str) -> dict:
    with open(path, "rb") as fh:
        return read_text(fh.read())


def write_text(reading: dict, terminator: str = "\r\n") -> bytes:
    """The canonical text of a reading (used by the controls to write modified files)."""

    def fmt(pq: tuple[int, int]) -> str:
        p, q = pq
        return str(p) if q == 1 else f"{p}/{q}"

    lines = [f"{reading['n']} {fmt(reading['side'])}"]
    lines += [" ".join(fmt(v) for v in sq) for sq in reading["squares"]]
    return (terminator.join(lines) + terminator).encode("ascii")
