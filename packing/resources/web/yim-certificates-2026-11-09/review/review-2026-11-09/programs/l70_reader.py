"""Strict readers for the L70 review (clean room, 9 November 2026).

Two formats, both read as untrusted data:

* ``.cert``: comment lines starting with ``#``, then a header ``n S``, then exactly
  ``n`` rows ``x y t``. Each token is an integer or ``p/q`` with ``q > 0``. Row ``k``
  is the unit square centred at ``(x, y)`` whose edge direction is
  ``u = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))``, that is ``t = tan(theta/2)``.
* Witness/v2 ``corners`` YAML: square ``i`` is four rational corners in cyclic order.

The readers return integers only (numerator, denominator pairs), so the two
geometric methods downstream share nothing but this module. Every layout the reader
does not expect is refused with a reason; nothing is repaired.

``sense='cw'`` reads the rotation the other way: a ``.cert`` row's ``t`` is negated,
and a corner square is reflected in its own horizontal centre line. Both are the
reflection of each square about the horizontal line through its centre.
"""

from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

TOKEN = re.compile(r"^(-?)(0|[1-9][0-9]*)(?:/([1-9][0-9]*))?$")
NATURAL = re.compile(r"^[1-9][0-9]*$")


class ReadError(ValueError):
    """The input is not in the layout the reader accepts."""


@dataclass(frozen=True)
class Packing:
    """A packing as integers: the side and the squares, nothing computed."""

    n: int
    side: tuple[int, int]
    kind: str  # "cert" (x, y, t rows) or "corners" (four corners per square)
    squares: tuple[tuple[int, ...], ...]
    ids: tuple[str, ...]
    meta: dict[str, Any] = field(default_factory=dict, compare=False)


def parse_rational(token: str) -> tuple[int, int, bool]:
    """Return (numerator, denominator, lowest_terms) for an integer or p/q token."""
    m = TOKEN.match(token)
    if m is None:
        raise ReadError(f"not a rational token: {token[:40]!r}")
    sign, num, den = m.group(1), m.group(2), m.group(3)
    p = int(num)
    q = int(den) if den is not None else 1
    if sign == "-":
        if p == 0:
            raise ReadError("negative zero token")
        p = -p
    lowest = math.gcd(p, q) == 1 and (den is None or q != 1)
    return p, q, lowest


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_cert(path: str | Path, sense: str = "ccw") -> Packing:
    """Read a ``.cert`` file strictly."""
    if sense not in ("ccw", "cw"):
        raise ReadError(f"unknown sense {sense!r}")
    raw = Path(path).read_bytes()
    return parse_cert_bytes(raw, sense=sense, label=str(path))


def parse_cert_bytes(raw: bytes, sense: str = "ccw", label: str = "<bytes>") -> Packing:
    if b"\r" in raw:
        raise ReadError("carriage return in file")
    if b"\t" in raw:
        raise ReadError("tab in file")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ReadError(f"not UTF-8: {exc}") from exc
    if not text.endswith("\n"):
        raise ReadError("no final newline")
    lines = text[:-1].split("\n")
    comments: list[str] = []
    k = 0
    while k < len(lines) and lines[k].startswith("#"):
        comments.append(lines[k])
        k += 1
    body = lines[k:]
    if not body:
        raise ReadError("no header")
    for idx, line in enumerate(body):
        if line.startswith("#"):
            raise ReadError(f"comment after the header at body line {idx}")
        if line == "" or line != line.strip(" ") or "  " in line:
            raise ReadError(f"blank line or irregular spacing at body line {idx}")
        if any(ord(ch) > 127 for ch in line):
            raise ReadError(f"non-ASCII data at body line {idx}")
    header = body[0].split(" ")
    if len(header) != 2:
        raise ReadError("header is not 'n S'")
    if not NATURAL.match(header[0]):
        raise ReadError("header count is not a positive integer")
    n = int(header[0])
    sp, sq, s_lowest = parse_rational(header[1])
    if sp <= 0:
        raise ReadError("side is not positive")
    rows = body[1:]
    if len(rows) != n:
        raise ReadError(f"header says {n} squares, file has {len(rows)} rows")
    squares: list[tuple[int, ...]] = []
    not_lowest = 0
    for idx, line in enumerate(rows):
        toks = line.split(" ")
        if len(toks) != 3:
            raise ReadError(f"row {idx + 1} has {len(toks)} tokens")
        vals: list[int] = []
        for tok in toks:
            p, q, lowest = parse_rational(tok)
            if not lowest:
                not_lowest += 1
            vals.extend((p, q))
        if sense == "cw":
            vals[4] = -vals[4]
        squares.append(tuple(vals))
    meta = {
        "label": label,
        "format": "cert",
        "sense": sense,
        "sha256": sha256_bytes(raw),
        "bytes": len(raw),
        "lines": len(lines),
        "comment_lines": comments,
        "final_newline": True,
        "side_lowest_terms": s_lowest,
        "row_tokens_not_lowest_terms": not_lowest,
    }
    return Packing(
        n=n,
        side=(sp, sq),
        kind="cert",
        squares=tuple(squares),
        ids=tuple(str(i + 1) for i in range(n)),
        meta=meta,
    )


def _strict_yaml_loader() -> type:
    import yaml

    class StrictBase(yaml.BaseLoader):  # strings, lists and dicts only
        pass

    def construct_mapping(loader: Any, node: Any, deep: bool = False) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise ReadError("non-string mapping key")
            if key in out:
                raise ReadError(f"duplicate key {key!r}")
            out[key] = loader.construct_object(value_node, deep=deep)
        return out

    StrictBase.add_constructor(  # type: ignore[attr-defined]
        "tag:yaml.org,2002:map", construct_mapping
    )
    return StrictBase


def read_corners_yaml(path: str | Path, sense: str = "ccw") -> Packing:
    """Read a Witness/v2 corner witness strictly (rational scalars, lower-left origin)."""
    import yaml

    if sense not in ("ccw", "cw"):
        raise ReadError(f"unknown sense {sense!r}")
    raw = Path(path).read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ReadError(f"not UTF-8: {exc}") from exc
    doc = yaml.load(text, Loader=_strict_yaml_loader())  # noqa: S506 - BaseLoader subclass
    if not isinstance(doc, dict) or set(doc) != {"softschema", "witness"}:
        raise ReadError("top level is not {softschema, witness}")
    ss = doc["softschema"]
    if not isinstance(ss, dict) or ss.get("contract") != "packing.squares:Witness/v2":
        raise ReadError("contract is not packing.squares:Witness/v2")
    w = doc["witness"]
    if not isinstance(w, dict):
        raise ReadError("witness is not a mapping")
    expect = {
        "square_size": "1",
        "representation": "corners",
    }
    for key, val in expect.items():
        if w.get(key) != val:
            raise ReadError(f"witness.{key} is not {val!r}")
    if w.get("scalar") != {"kind": "rational"}:
        raise ReadError("scalar is not {kind: rational}")
    coords = w.get("coordinates")
    if not isinstance(coords, dict) or coords.get("origin") != "lower-left" or coords.get(
        "axes"
    ) != "x-right-y-up":
        raise ReadError("coordinates are not lower-left, x-right-y-up")
    n_tok = w.get("n")
    if not isinstance(n_tok, str) or not NATURAL.match(n_tok):
        raise ReadError("n is not a positive integer")
    n = int(n_tok)
    side_tok = w.get("side")
    if not isinstance(side_tok, str):
        raise ReadError("side is not a scalar")
    sp, sq, s_lowest = parse_rational(side_tok)
    if sp <= 0:
        raise ReadError("side is not positive")
    sqs = w.get("squares")
    if not isinstance(sqs, list) or len(sqs) != n:
        raise ReadError("squares list length differs from n")
    out: list[tuple[int, ...]] = []
    ids: list[str] = []
    not_lowest = 0
    for idx, item in enumerate(sqs):
        if not isinstance(item, dict) or set(item) != {"id", "corners"}:
            raise ReadError(f"square {idx} is not {{id, corners}}")
        sid = item["id"]
        if not isinstance(sid, str):
            raise ReadError(f"square {idx} id is not a scalar")
        corners = item["corners"]
        if not isinstance(corners, list) or len(corners) != 4:
            raise ReadError(f"square {idx} does not have four corners")
        vals: list[int] = []
        for pt in corners:
            if not isinstance(pt, list) or len(pt) != 2:
                raise ReadError(f"square {idx} corner is not a pair")
            for tok in pt:
                if not isinstance(tok, str):
                    raise ReadError(f"square {idx} coordinate is not a scalar")
                p, q, lowest = parse_rational(tok)
                if not lowest:
                    not_lowest += 1
                vals.extend((p, q))
        ids.append(sid)
        out.append(tuple(vals))
    if len(set(ids)) != n:
        raise ReadError("repeated square id")
    if sense == "cw":
        out = [reflect_corners_horizontal(v) for v in out]
    meta = {
        "label": str(path),
        "format": "corners",
        "sense": sense,
        "sha256": sha256_bytes(raw),
        "bytes": len(raw),
        "ids_are_1_to_n_in_order": ids == [str(i + 1) for i in range(n)],
        "side_lowest_terms": s_lowest,
        "scalars_not_lowest_terms": not_lowest,
        "witness_keys": sorted(w),
    }
    return Packing(
        n=n, side=(sp, sq), kind="corners", squares=tuple(out), ids=tuple(ids), meta=meta
    )


def reflect_corners_horizontal(vals: tuple[int, ...] | list[int]) -> tuple[int, ...]:
    """Reflect four corners in the horizontal line through their centre, in integers.

    The centre's ordinate is (y0 + y2)/2; each y becomes y0 + y2 - y. Done with
    integer numerators over a common denominator so that this module stays
    free of geometry libraries.
    """
    ys = [(vals[4 * k + 2], vals[4 * k + 3]) for k in range(4)]
    (a, b), (c, d) = ys[0], ys[2]
    out = list(vals)
    for k in range(4):
        e, f = ys[k]
        # a/b + c/d - e/f
        num = a * d * f + c * b * f - e * b * d
        den = b * d * f
        g = math.gcd(num, den)
        out[4 * k + 2] = num // g
        out[4 * k + 3] = den // g
    return tuple(out)
