"""Strict reader for the `.cert` format of de Winter's #941/#942 certificates.

Written for the L96 stage 4 review. Imports nothing from this repository or the source.

The format, from the files' own first comment line and the source README: optional
comment lines starting with `#`, then one header line `n side`, then exactly n lines
`x y t`, where (x, y) is a square's centre and t = tan(theta/2) its rotation. Every
scalar is an integer or `p/q`. The reader fails closed on anything else and returns
integers only: each scalar as a (numerator, denominator) pair with denominator > 0.
"""

import re

SCALAR = re.compile(r"^(-?)(\d+)(?:/(\d+))?$")


class ReadError(Exception):
    pass


def _scalar(tok, where):
    m = SCALAR.match(tok)
    if not m:
        raise ReadError(f"{where}: not an integer or p/q: {tok[:40]!r}")
    sign, num, den = m.group(1), int(m.group(2)), int(m.group(3) or "1")
    if den == 0:
        raise ReadError(f"{where}: zero denominator")
    if m.group(3) is not None and m.group(3).startswith("0"):
        raise ReadError(f"{where}: denominator with a leading zero")
    if len(m.group(2)) > 1 and m.group(2).startswith("0"):
        raise ReadError(f"{where}: numerator with a leading zero")
    if sign and num == 0:
        raise ReadError(f"{where}: negative zero")
    return (-num if sign else num, den)


def _gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def read_cert(data):
    """Read a certificate from bytes. Returns a dict of integers and strings."""
    if not isinstance(data, bytes):
        raise ReadError("expected bytes")
    try:
        text = data.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ReadError("not ASCII") from exc
    if "\r" in text or "\t" in text:
        raise ReadError("carriage return or tab")
    if not text.endswith("\n"):
        raise ReadError("no final newline")
    lines = text[:-1].split("\n")
    comments = []
    i = 0
    while i < len(lines) and lines[i].startswith("#"):
        comments.append(lines[i])
        i += 1
    body = lines[i:]
    if not body:
        raise ReadError("no header line")
    for k, line in enumerate(body):
        if line != line.strip() or "  " in line or line == "":
            raise ReadError(f"line {i + k + 1}: blank, padded or double-spaced")
        if line.startswith("#"):
            raise ReadError(f"line {i + k + 1}: comment after the header")
    head = body[0].split(" ")
    if len(head) != 2:
        raise ReadError("header is not `n side`")
    n_num, n_den = _scalar(head[0], "header n")
    if n_den != 1 or n_num <= 0:
        raise ReadError("n is not a positive integer")
    side = _scalar(head[1], "header side")
    if side[0] <= 0:
        raise ReadError("side is not positive")
    rows = body[1:]
    if len(rows) != n_num:
        raise ReadError(f"{len(rows)} square lines for n = {n_num}")
    squares = []
    noncanonical = 0
    for k, line in enumerate(rows):
        toks = line.split(" ")
        if len(toks) != 3:
            raise ReadError(f"square {k + 1}: {len(toks)} fields")
        triple = tuple(_scalar(t, f"square {k + 1}") for t in toks)
        squares.append(triple)
    for num, den in [side] + [s for sq in squares for s in sq]:
        if _gcd(num, den) != 1:
            noncanonical += 1
    return {
        "n": n_num,
        "side": side,
        "squares": squares,
        "comments": comments,
        "noncanonical_scalars": noncanonical,
        "scalars": 1 + 3 * n_num,
    }
