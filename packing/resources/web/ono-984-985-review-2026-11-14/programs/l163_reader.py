"""Lane L163 reader for Roberto Ono's centre-and-half-angle certificates (#984, #985).

The JSON form is an object with `n`, `side`, an optional `side_decimal_info_only`
string, and `squares`, each an object with exactly `cx`, `cy` and `t`, every scalar a
string `p/q`. The text form (`.cert`) is comment lines starting with `#`, then a line
`n S`, then one line `x y t` per square.

A scalar is canonical when it is `p/q` with `q >= 1`, no sign on zero, no leading zeros
and `gcd(|p|, q) = 1`. The reader hands the methods integers only:
`(side_num, side_den)` and, per square, `(xn, xd, yn, yd, tn, td)`.

It decides nothing about geometry. It refuses floats, constants, duplicate keys,
non-string scalars, keys outside the lists below, and a count other than `n`.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from math import gcd

FRACTION = re.compile(r"(-?)(0|[1-9][0-9]*)/([1-9][0-9]*)\Z")
DECIMAL_INT = re.compile(r"(0|[1-9][0-9]*)\Z")
TOP_REQUIRED = frozenset({"n", "side", "squares"})
TOP_OPTIONAL = frozenset({"side_decimal_info_only"})
SQUARE_KEYS = frozenset({"cx", "cy", "t"})


class Refused(Exception):
    """The reader refuses the file; `reason` says why."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


@dataclass(frozen=True)
class Certificate:
    """A certificate as integers: the side and, per square, centre and half-angle."""

    n: int
    side: tuple[int, int]
    squares: tuple[tuple[int, int, int, int, int, int], ...]
    info: dict[str, str] = field(default_factory=dict)  # pyright: ignore[reportUnknownVariableType]

    def tree(self) -> tuple[int, tuple[int, int], tuple[tuple[int, ...], ...]]:
        return (self.n, self.side, self.squares)


INTEGER = re.compile(r"-?(0|[1-9][0-9]*)\Z")


def scalar(text: object, where: str, lowest: bool = True, allow_int: bool = False) -> tuple[int, int]:
    """Read one canonical `p/q` string as `(p, q)`; with allow_int, also a canonical `p`."""
    if not isinstance(text, str):
        raise Refused(f"{where}: scalar is not a string")
    if allow_int and INTEGER.match(text):
        if text == "-0":
            raise Refused(f"{where}: negative zero")
        return int(text), 1
    m = FRACTION.match(text)
    if m is None:
        raise Refused(f"{where}: scalar {text[:40]!r} is not p/q")
    sign, ps, qs = m.groups()
    p, q = int(ps), int(qs)
    if sign and p == 0:
        raise Refused(f"{where}: negative zero")
    if sign:
        p = -p
    if lowest and gcd(abs(p), q) != 1:
        raise Refused(f"{where}: not in lowest terms")
    return p, q


def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    out: dict[str, object] = {}
    for k, v in pairs:
        if k in out:
            raise Refused(f"duplicate key {k!r}")
        out[k] = v
    return out


def _no_float(text: str) -> object:
    raise Refused(f"JSON float {text[:20]!r}")


def _no_constant(text: str) -> object:
    raise Refused(f"JSON constant {text!r}")


def _int(text: str) -> int:
    if not re.fullmatch(r"-?(0|[1-9][0-9]*)", text):
        raise Refused(f"JSON integer {text!r} is not canonical")
    return int(text)


def read_json_text(text: str, lowest: bool = True) -> Certificate:
    """Read the JSON form from its text."""
    try:
        doc = json.loads(
            text,
            object_pairs_hook=_pairs,
            parse_float=_no_float,
            parse_constant=_no_constant,
            parse_int=_int,
        )
    except json.JSONDecodeError as exc:
        raise Refused(f"not JSON: {exc.msg}") from exc
    if not isinstance(doc, dict):
        raise Refused("top level is not an object")
    keys = set(doc)  # pyright: ignore[reportUnknownArgumentType]
    if not TOP_REQUIRED <= keys:
        raise Refused(f"missing keys {sorted(TOP_REQUIRED - keys)}")
    if keys - TOP_REQUIRED - TOP_OPTIONAL:
        raise Refused(f"unknown keys {sorted(keys - TOP_REQUIRED - TOP_OPTIONAL)}")
    n = doc["n"]  # pyright: ignore[reportUnknownVariableType]
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise Refused("n is not a positive integer")
    side = scalar(doc["side"], "side", lowest)
    if side[0] <= 0:
        raise Refused("side is not positive")
    info: dict[str, str] = {}
    if "side_decimal_info_only" in doc:
        s = doc["side_decimal_info_only"]  # pyright: ignore[reportUnknownVariableType]
        if not isinstance(s, str):
            raise Refused("side_decimal_info_only is not a string")
        info["side_decimal_info_only"] = s
    rows = doc["squares"]  # pyright: ignore[reportUnknownVariableType]
    if not isinstance(rows, list):
        raise Refused("squares is not a list")
    if len(rows) != n:  # pyright: ignore[reportUnknownArgumentType]
        raise Refused(f"{len(rows)} entries for n = {n}")  # pyright: ignore[reportUnknownArgumentType]
    squares: list[tuple[int, int, int, int, int, int]] = []
    for i, row in enumerate(rows, start=1):  # pyright: ignore[reportUnknownVariableType, reportUnknownArgumentType]
        if not isinstance(row, dict):
            raise Refused(f"square {i} is not an object")
        if set(row) != SQUARE_KEYS:  # pyright: ignore[reportUnknownArgumentType]
            raise Refused(f"square {i}: keys {sorted(row)} are not cx, cy, t")  # pyright: ignore[reportUnknownArgumentType]
        xn, xd = scalar(row["cx"], f"square {i} cx", lowest)
        yn, yd = scalar(row["cy"], f"square {i} cy", lowest)
        tn, td = scalar(row["t"], f"square {i} t", lowest)
        squares.append((xn, xd, yn, yd, tn, td))
    return Certificate(n, side, tuple(squares), info)


def read_cert_text(text: str, lowest: bool = True) -> Certificate:
    """Read the text form: `#` comments first, then `n S`, then `x y t` per square."""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    k = 0
    comments: list[str] = []
    while k < len(lines) and lines[k].startswith("#"):
        comments.append(lines[k])
        k += 1
    body = lines[k:]
    if not body:
        raise Refused("no header line")
    for j, line in enumerate(body):
        if line != line.strip() or "  " in line or "\t" in line or line == "":
            raise Refused(f"line {k + j + 1}: not single-space separated")
    head = body[0].split(" ")
    if len(head) != 2 or not DECIMAL_INT.match(head[0]):
        raise Refused("header is not `n S`")
    n = int(head[0])
    if n < 1:
        raise Refused("n is not positive")
    side = scalar(head[1], "side", lowest, allow_int=True)
    if side[0] <= 0:
        raise Refused("side is not positive")
    rows = body[1:]
    if len(rows) != n:
        raise Refused(f"{len(rows)} entries for n = {n}")
    squares: list[tuple[int, int, int, int, int, int]] = []
    ints = 0
    for i, line in enumerate(rows, start=1):
        parts = line.split(" ")
        if len(parts) != 3:
            raise Refused(f"square {i}: {len(parts)} fields")
        ints += sum(1 for p in parts if "/" not in p)
        xn, xd = scalar(parts[0], f"square {i} x", lowest, allow_int=True)
        yn, yd = scalar(parts[1], f"square {i} y", lowest, allow_int=True)
        tn, td = scalar(parts[2], f"square {i} t", lowest, allow_int=True)
        squares.append((xn, xd, yn, yd, tn, td))
    return Certificate(n, side, tuple(squares), {"comments": "\n".join(comments), "integer_form_scalars": str(ints)})


def read_json(path: str, lowest: bool = True) -> Certificate:
    with open(path, encoding="utf-8") as fh:
        return read_json_text(fh.read(), lowest)


def read_cert(path: str, lowest: bool = True) -> Certificate:
    with open(path, encoding="utf-8") as fh:
        return read_cert_text(fh.read(), lowest)


def same_tree(a: Certificate, b: Certificate) -> bool:
    """Whether two readings hold exactly the same n, side and squares."""
    return a.tree() == b.tree()
