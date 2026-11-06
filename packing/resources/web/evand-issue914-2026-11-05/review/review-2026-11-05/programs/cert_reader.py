"""Strict reader of Evan Daniel's rational certificate format, written for this review.

Written from the format as the certificates' own first line states it ("unit squares,
centre (x, y), rotation (c, s) = ((1-t^2)/(1+t^2), 2t/(1+t^2))") and from issue #914's
description ("n S", then "x y t" per square). It reads no producer code and no code of
this repository.

Accepted grammar, and nothing else:
  * the file is ASCII, lines end in LF, and the last line ends in LF;
  * lines starting with '#' are comments and may appear anywhere;
  * no blank line;
  * the first other line is "n S": a positive integer and a rational;
  * then exactly n lines "x y t", three rationals separated by single spaces;
  * a rational is an integer "-?[0-9]+" or a fraction "-?[0-9]+/[0-9]+" with a
    non-zero denominator (no sign on the denominator, no decimals, no exponents,
    no underscores, no whitespace inside).
"""

from __future__ import annotations

import hashlib
import re
from fractions import Fraction
from pathlib import Path

_INT = re.compile(r"-?[0-9]+\Z")
_FRAC = re.compile(r"(-?[0-9]+)/([0-9]+)\Z")


def rational(token: str) -> Fraction:
    """Parse one rational token exactly; raise ValueError on anything else."""
    if _INT.match(token):
        return Fraction(int(token))
    m = _FRAC.match(token)
    if m:
        q = int(m.group(2))
        if q == 0:
            raise ValueError(f"zero denominator in {token!r}")
        return Fraction(int(m.group(1)), q)
    raise ValueError(f"not a rational token: {token[:40]!r}")


def parse_text(raw: bytes) -> dict:
    """Parse certificate bytes; return n, S, the squares (x, y, t) and the comments."""
    text = raw.decode("ascii")
    if "\r" in text or "\t" in text:
        raise ValueError("CR or TAB in certificate")
    if not text.endswith("\n"):
        raise ValueError("last line does not end in LF")
    lines = text[:-1].split("\n")
    comments: list[tuple[int, str]] = []
    body: list[tuple[int, str]] = []
    for number, line in enumerate(lines, 1):
        if line.startswith("#"):
            comments.append((number, line))
            continue
        if line == "":
            raise ValueError(f"blank line {number}")
        body.append((number, line))
    if not body:
        raise ValueError("no header")
    header = body[0][1].split(" ")
    if len(header) != 2 or not re.fullmatch(r"[1-9][0-9]*", header[0]):
        raise ValueError(f"bad header {body[0][1][:60]!r}")
    n = int(header[0])
    side = rational(header[1])
    if side <= 0:
        raise ValueError("non-positive side")
    rows = body[1:]
    if len(rows) != n:
        raise ValueError(f"header says {n} squares, file has {len(rows)} rows")
    squares: list[tuple[Fraction, Fraction, Fraction]] = []
    lines_of: list[int] = []
    for number, line in rows:
        tokens = line.split(" ")
        if len(tokens) != 3:
            raise ValueError(f"line {number}: {len(tokens)} tokens")
        x, y, t = (rational(tok) for tok in tokens)
        squares.append((x, y, t))
        lines_of.append(number)
    return {
        "n": n,
        "S": side,
        "squares": squares,
        "line_of_square": lines_of,
        "header_line": body[0][0],
        "comments": comments,
    }


def read_cert(path: str | Path) -> dict:
    """Read a certificate file strictly; add its SHA-256 and byte count."""
    raw = Path(path).read_bytes()
    out = parse_text(raw)
    out["sha256"] = hashlib.sha256(raw).hexdigest()
    out["bytes"] = len(raw)
    out["path"] = str(path)
    return out
