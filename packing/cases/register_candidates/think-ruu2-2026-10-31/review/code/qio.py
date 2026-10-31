"""Readers for the review's inputs, which are read as data.

Written by the reviewer for this review; it imports nothing from the repository or from
any certificate's producer. A square is a tuple (cx, cy, a, b) of Fractions: centre
(cx, cy) and basis (a, b) = (cos theta, sin theta), so its corners are
c +- (a, b)/2 +- (-b, a)/2. Nothing here decides anything; the routes do.
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

RATIONAL = re.compile(r"-?\d+(/\d+)?")

type Square = tuple[Fraction, Fraction, Fraction, Fraction]


def rational(text: str) -> Fraction:
    s = text.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "'\"":
        s = s[1:-1]
    if not RATIONAL.fullmatch(s):
        raise ValueError(f"not a rational literal: {text!r}")
    return Fraction(s)


def read_view(path: str | Path) -> tuple[int, Fraction, list[Square], dict[str, str]]:
    """Read a center-basis rational witness YAML strictly, line by line."""
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    start = lines.index("witness:")
    head: dict[str, str] = {}
    squares: list[Square] = []
    ids: list[str] = []
    i = start + 1
    parent = ""
    while i < len(lines):
        line = lines[i]
        if line == "  squares:":
            i += 1
            break
        m2 = re.fullmatch(r"  ([a-z_]+):(?: (.*))?", line)
        m4 = re.fullmatch(r"    ([a-z_]+):(?: (.*))?", line)
        if m2:
            parent = m2.group(1)
            if m2.group(2) is not None:
                head[parent] = m2.group(2).strip().strip("'")
        elif m4 and m4.group(2) is not None:
            head[f"{parent}.{m4.group(1)}"] = m4.group(2).strip().strip("'")
        else:
            raise ValueError(f"unexpected header line {i + 1}: {line!r}")
        i += 1
    while i < len(lines):
        line = lines[i]
        m = re.fullmatch(r"  - id: (\S+)", line)
        if not m:
            if re.fullmatch(r"  [a-z_]+:.*", line):
                break
            raise ValueError(f"unexpected square line {i + 1}: {line!r}")
        block = lines[i + 1 : i + 7]
        if (
            len(block) != 6
            or block[0] != "    center:"
            or block[3] != "    basis:"
            or not all(b.startswith("    - ") for b in (block[1], block[2], block[4], block[5]))
        ):
            raise ValueError(f"malformed square block at line {i + 1}")
        cx, cy, a, b = (rational(block[k][6:]) for k in (1, 2, 4, 5))
        ids.append(m.group(1))
        squares.append((cx, cy, a, b))
        i += 7
    expected = {
        "square_size": "1",
        "representation": "center-basis",
        "scalar.kind": "rational",
        "coordinates.origin": "lower-left",
        "coordinates.axes": "x-right-y-up",
    }
    for key, want in expected.items():
        if head.get(key) != want:
            raise ValueError(f"{path}: {key} is {head.get(key)!r}, expected {want!r}")
    n = int(head["n"])
    if len(squares) != n or len(set(ids)) != n:
        raise ValueError(f"{path}: {len(squares)} squares, {len(set(ids))} ids, n = {n}")
    return n, rational(head["side"]), squares, head


def basis_from_t(t: Fraction) -> tuple[Fraction, Fraction]:
    """(cos theta, sin theta) from t = tan(theta/2), the half-angle form."""
    d = 1 + t * t
    return (1 - t * t) / d, 2 * t / d


def read_tcert(path: str | Path) -> tuple[int, Fraction, list[Square], list[Fraction]]:
    """Read a 'n side' then n x 'cx cy t' certificate; '#' lines are comments."""
    rows = [
        ln.split()
        for ln in Path(path).read_text(encoding="utf-8").splitlines()
        if ln.strip() and not ln.lstrip().startswith("#")
    ]
    if len(rows[0]) != 2:
        raise ValueError(f"{path}: header {rows[0]!r}")
    n, side = int(rows[0][0]), rational(rows[0][1])
    body = rows[1:]
    if len(body) != n or any(len(r) != 3 for r in body):
        raise ValueError(f"{path}: {len(body)} rows for n = {n}")
    squares: list[Square] = []
    ts: list[Fraction] = []
    for r in body:
        cx, cy, t = (rational(v) for v in r)
        a, b = basis_from_t(t)
        squares.append((cx, cy, a, b))
        ts.append(t)
    return n, side, squares, ts


def l_strip(s: Fraction, variant: str = "16+16+1") -> list[Square]:
    """33 axis-aligned unit squares in [S, S+1]x[0, S+1] U [0, S+1]x[S, S+1] for 16 < S < 17.

    '16+16+1': a column of 16 at x in [S, S+1], y in [0, 16]; a row of 16 at y in
    [S, S+1], x in [0, 16]; one corner square [S, S+1]^2.
    '17+16': a column of 17, y in [0, 17] (17 <= S + 1); a row of 16, x in [0, 16].
    """
    if not 16 < s < 17:
        raise ValueError("the L strip here is written for 16 < S < 17")
    half = Fraction(1, 2)
    one, zero = Fraction(1), Fraction(0)
    if variant == "16+16+1":
        col = [(s + half, k + half, one, zero) for k in range(16)]
        row = [(k + half, s + half, one, zero) for k in range(16)]
        return col + row + [(s + half, s + half, one, zero)]
    if variant == "17+16":
        col = [(s + half, k + half, one, zero) for k in range(17)]
        row = [(k + half, s + half, one, zero) for k in range(16)]
        return col + row
    if variant == "17top+16":
        # the placement of the 293 house's strip: a column of 17 flush with the top wall,
        # y in [S - 16, S + 1], and a row of 16 flush with the left wall, x in [0, 16]
        col = [(s + half, s + half - k, one, zero) for k in range(17)]
        row = [(k + half, s + half, one, zero) for k in range(16)]
        return col + row
    raise ValueError(variant)
