"""Strict readers for the three file forms this review decides.

Lane r127-1118, stage 4 blind review of issues #1015, #1017 and #1020 (18 November 2026).
Written for this review; imports nothing from the repository or the sources.

Forms:

* ``centre``: a JSON object with exactly the keys ``n``, ``side``, ``square_size``,
  ``format`` and ``squares``; each square is four exact rationals
  ``[center_x, center_y, cos, sin]``, (cos, sin) the unit direction of one edge.
* ``witness``: a YAML softschema envelope around a Witness/v2 record with
  ``representation: corners`` and rational scalars; four corners per square.

Every reader returns a ``Packing``: ``n``, ``side`` (Fraction), and for each square its
four corners as Fractions in the order the file implies, plus, for a centre file, the
centre and the direction.  Corners of a centre square are listed counterclockwise as
c + (u + v)/2, c + (-u + v)/2, c - (u + v)/2, c + (u - v)/2 with u = (cos, sin) and
v = (-sin, cos).  Readers do not decide geometry: a direction that is not a unit vector
is passed on and refused by the deciding methods.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from fractions import Fraction
from math import gcd

import yaml

FORMAT_SENTENCE = (
    "each square: [center_x, center_y, cos, sin] as exact rationals; "
    "(cos, sin) is the unit direction of one edge"
)
RATIONAL = re.compile(r"(-?)(0|[1-9][0-9]*)(?:/([1-9][0-9]*))?\Z")
DECIMAL_INT = re.compile(r"-?(0|[1-9][0-9]*)\Z")
WITNESS_KEYS = {
    "id", "n", "side", "square_size", "representation", "scalar", "coordinates",
    "squares", "claim", "source", "certificate",
}
WITNESS_REQUIRED = {
    "id", "n", "side", "square_size", "representation", "scalar", "coordinates",
    "squares", "claim",
}


class ReadError(Exception):
    """The file is refused by the reader."""


@dataclass
class Packing:
    n: int
    side: Fraction
    corners: list[list[tuple[Fraction, Fraction]]]
    form: str
    centres: list[tuple[Fraction, Fraction]] | None = None
    directions: list[tuple[Fraction, Fraction]] | None = None
    not_lowest: list[str] = field(default_factory=list)
    scalars: int = 0
    ids: list[object] = field(default_factory=list)
    meta: dict[str, object] = field(default_factory=dict)


def parse_rational(text: object, where: str, flags: list[str]) -> Fraction:
    """Read p or p/q with an optional minus, no leading zero, q >= 1; record lowest terms."""
    if isinstance(text, bool):
        raise ReadError(f"{where}: boolean where a rational was expected")
    if isinstance(text, int):
        return Fraction(text)
    if not isinstance(text, str):
        raise ReadError(f"{where}: {type(text).__name__} where a rational was expected")
    m = RATIONAL.match(text)
    if not m:
        raise ReadError(f"{where}: not a rational: {text[:40]!r}")
    sign, p_text, q_text = m.groups()
    p = int(p_text)
    if sign and p == 0:
        raise ReadError(f"{where}: negative zero")
    q = int(q_text) if q_text is not None else 1
    if q_text is not None and (gcd(p, q) != 1 or (p == 0 and q != 1)):
        flags.append(where)
    return Fraction(-p if sign else p, q)


# ---------------------------------------------------------------------------- YAML


def _yaml_tree(text: str) -> object:
    """Build a tree from PyYAML's events, refusing every construct but block mappings,
    block sequences and plain or quoted scalars; scalars are resolved here."""
    if "\t" in text:
        raise ReadError("tab character")
    if "\r" in text:
        raise ReadError("carriage return")
    resolver = yaml.resolver.Resolver()
    stack: list[object] = []
    keys: list[object] = []
    root: list[object] = []
    documents = 0

    def add(value: object) -> None:
        if not stack:
            root.append(value)
            return
        top = stack[-1]
        if isinstance(top, list):
            top.append(value)
        else:
            assert isinstance(top, dict)
            pending = keys[-1]
            if pending is _NOKEY:
                if not isinstance(value, str):
                    raise ReadError("mapping key that is not a string")
                if value in top:
                    raise ReadError(f"duplicate key {value!r}")
                keys[-1] = value
            else:
                top[pending] = value
                keys[-1] = _NOKEY

    try:
        events = list(yaml.parse(text, Loader=yaml.SafeLoader))
    except yaml.YAMLError as exc:
        raise ReadError(f"YAML: {exc}") from None
    for ev in events:
        if isinstance(ev, (yaml.StreamStartEvent, yaml.StreamEndEvent)):
            continue
        if isinstance(ev, yaml.DocumentStartEvent):
            documents += 1
            if ev.explicit or ev.version or ev.tags:
                raise ReadError("explicit document start or directive")
            continue
        if isinstance(ev, yaml.DocumentEndEvent):
            if ev.explicit:
                raise ReadError("explicit document end")
            continue
        if isinstance(ev, yaml.AliasEvent):
            raise ReadError("alias")
        if isinstance(ev, (yaml.MappingStartEvent, yaml.SequenceStartEvent)):
            if ev.anchor is not None or ev.tag is not None or ev.flow_style:
                raise ReadError("anchor, tag or flow collection")
            node: object = {} if isinstance(ev, yaml.MappingStartEvent) else []
            stack.append(node)
            keys.append(_NOKEY)
            continue
        if isinstance(ev, (yaml.MappingEndEvent, yaml.SequenceEndEvent)):
            node = stack.pop()
            pending = keys.pop()
            if pending is not _NOKEY:
                raise ReadError("key without value")
            add(node)
            continue
        if isinstance(ev, yaml.ScalarEvent):
            if ev.anchor is not None or ev.tag is not None:
                raise ReadError("anchored or tagged scalar")
            if ev.style in ("'", '"'):
                add(ev.value)
                continue
            if ev.style is not None:
                raise ReadError("block scalar")
            tag = resolver.resolve(yaml.ScalarNode, ev.value, (True, False))
            if tag == "tag:yaml.org,2002:str":
                add(ev.value)
            elif tag == "tag:yaml.org,2002:int" and DECIMAL_INT.match(ev.value):
                add(int(ev.value))
            else:
                raise ReadError(f"plain scalar of implicit type {tag}: {ev.value[:30]!r}")
            continue
        raise ReadError(f"unexpected event {type(ev).__name__}")
    if documents != 1 or len(root) != 1:
        raise ReadError("not exactly one document")
    return root[0]


class _NoKey:
    pass


_NOKEY = _NoKey()


def _corner_lines(text: str) -> list[str]:
    """A second, line-based read of the corner scalars, in file order."""
    out: list[str] = []
    in_squares = False
    for line in text.split("\n"):
        if line == "  squares:":
            in_squares = True
            continue
        if not in_squares:
            continue
        if line and not line.startswith("    ") and not line.startswith("  - "):
            in_squares = False
            continue
        m = re.match(r"\s+- - (\S+)\Z", line)
        if m:
            out.append(m.group(1))
            continue
        m = re.match(r"\s+- (\S+)\Z", line)
        if m and not line.lstrip().startswith("- id:"):
            out.append(m.group(1))
    return [s[1:-1] if len(s) >= 2 and s[0] == s[-1] == "'" else s for s in out]


def read_witness(text: str) -> Packing:
    tree = _yaml_tree(text)
    if not isinstance(tree, dict) or set(tree) != {"softschema", "witness"}:
        raise ReadError("top level is not exactly softschema and witness")
    env = tree["softschema"]
    if not isinstance(env, dict) or set(env) != {"contract", "schema", "envelope", "status"}:
        raise ReadError("softschema envelope keys")
    if env["contract"] != "packing.squares:Witness/v2" or env["envelope"] != "witness":
        raise ReadError("envelope contract")
    if env["status"] != "enforced" or not isinstance(env["schema"], str):
        raise ReadError("envelope status or schema")
    w = tree["witness"]
    if not isinstance(w, dict):
        raise ReadError("witness is not a mapping")
    if not set(w) <= WITNESS_KEYS or not WITNESS_REQUIRED <= set(w):
        raise ReadError(f"witness keys {sorted(set(w) ^ WITNESS_REQUIRED)}")
    if not isinstance(w["n"], int) or isinstance(w["n"], bool) or w["n"] < 1:
        raise ReadError("n")
    if w["square_size"] != "1" or w["representation"] != "corners":
        raise ReadError("square_size or representation")
    if w["scalar"] != {"kind": "rational"}:
        raise ReadError("scalar kind")
    if w["coordinates"] != {
        "origin": "lower-left", "axes": "x-right-y-up", "angle_unit": "not-applicable"
    }:
        raise ReadError("coordinates")
    flags: list[str] = []
    side = parse_rational(w["side"], "side", flags)
    if side <= 0:
        raise ReadError("side not positive")
    squares = w["squares"]
    if not isinstance(squares, list):
        raise ReadError("squares is not a list")
    if len(squares) != w["n"]:
        raise ReadError(f"n stated {w['n']}, {len(squares)} listed")
    corners: list[list[tuple[Fraction, Fraction]]] = []
    ids: list[object] = []
    flat: list[object] = []
    for k, sq in enumerate(squares):
        if not isinstance(sq, dict) or set(sq) != {"id", "corners"}:
            raise ReadError(f"square {k + 1}: keys")
        if not isinstance(sq["id"], (str, int)) or isinstance(sq["id"], bool):
            raise ReadError(f"square {k + 1}: id")
        ids.append(sq["id"])
        cs = sq["corners"]
        if not isinstance(cs, list) or len(cs) != 4:
            raise ReadError(f"square {k + 1}: not four corners")
        pts = []
        for j, pt in enumerate(cs):
            if not isinstance(pt, list) or len(pt) != 2:
                raise ReadError(f"square {k + 1} corner {j}: not two scalars")
            x = parse_rational(pt[0], f"square {k + 1} corner {j} x", flags)
            y = parse_rational(pt[1], f"square {k + 1} corner {j} y", flags)
            flat.extend([pt[0], pt[1]])
            pts.append((x, y))
        corners.append(pts)
    if len(set(ids)) != len(ids):
        raise ReadError("ids not distinct")
    second = _corner_lines(text)
    if [str(s) for s in flat] != second:
        raise ReadError("line-based second read of the corners differs")
    meta = {k: w[k] for k in ("id", "claim", "source", "certificate") if k in w}
    meta["schema"] = env["schema"]
    return Packing(
        n=w["n"], side=side, corners=corners, form="witness", not_lowest=flags,
        scalars=1 + 8 * len(corners), ids=ids, meta=meta,
    )


# ---------------------------------------------------------------------------- JSON


def _pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
    out: dict[str, object] = {}
    for k, v in pairs:
        if k in out:
            raise ReadError(f"duplicate key {k!r}")
        out[k] = v
    return out


def _refuse_float(text: str) -> object:
    raise ReadError(f"JSON number that is not an integer: {text[:30]}")


def _refuse_constant(text: str) -> object:
    raise ReadError(f"JSON constant {text}")


def read_centre(text: str) -> Packing:
    try:
        tree = json.loads(
            text, object_pairs_hook=_pairs_hook, parse_float=_refuse_float,
            parse_constant=_refuse_constant,
        )
    except json.JSONDecodeError as exc:
        raise ReadError(f"JSON: {exc}") from None
    if not isinstance(tree, dict) or set(tree) != {"n", "side", "square_size", "format",
                                                   "squares"}:
        raise ReadError("keys")
    n = tree["n"]
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ReadError("n")
    if tree["square_size"] != "1" or tree["format"] != FORMAT_SENTENCE:
        raise ReadError("square_size or format sentence")
    flags: list[str] = []
    if not isinstance(tree["side"], str):
        raise ReadError("side is not a string")
    side = parse_rational(tree["side"], "side", flags)
    if side <= 0:
        raise ReadError("side not positive")
    sq = tree["squares"]
    if not isinstance(sq, list) or len(sq) != n:
        raise ReadError(f"n stated {n}, {len(sq) if isinstance(sq, list) else '?'} listed")
    centres, dirs, corners = [], [], []
    for k, row in enumerate(sq):
        if not isinstance(row, list) or len(row) != 4 or not all(isinstance(s, str) for s in row):
            raise ReadError(f"square {k + 1}: not four string scalars")
        cx, cy, a, b = (parse_rational(s, f"square {k + 1} [{i}]", flags) for i, s in enumerate(row))
        centres.append((cx, cy))
        dirs.append((a, b))
        corners.append(centre_corners((cx, cy), (a, b)))
    return Packing(
        n=n, side=side, corners=corners, form="centre", centres=centres, directions=dirs,
        not_lowest=flags, scalars=1 + 4 * n, ids=list(range(1, n + 1)),
    )


def centre_corners(c: tuple[Fraction, Fraction], u: tuple[Fraction, Fraction]
                   ) -> list[tuple[Fraction, Fraction]]:
    """c + (u + v)/2, c + (-u + v)/2, c - (u + v)/2, c + (u - v)/2, v = (-sin, cos)."""
    (cx, cy), (a, b) = c, u
    vx, vy = -b, a
    out = []
    for su, sv in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
        out.append((cx + (su * a + sv * vx) / 2, cy + (su * b + sv * vy) / 2))
    return out


def read_path(path: str) -> Packing:
    with open(path, "rb") as fh:
        raw = fh.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise ReadError("not UTF-8") from None
    if path.endswith(".json"):
        return read_centre(text)
    if path.endswith(".yaml"):
        return read_witness(text)
    raise ReadError("unknown file form")


# ------------------------------------------------------------------ writers (controls)


def fmt(q: Fraction) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def write_centre(n: int, side: Fraction, centres, dirs, side_text: str | None = None) -> str:
    rows = [[fmt(c[0]), fmt(c[1]), fmt(d[0]), fmt(d[1])] for c, d in zip(centres, dirs, strict=True)]
    obj = {"n": n, "side": side_text if side_text is not None else fmt(side),
           "square_size": "1", "format": FORMAT_SENTENCE, "squares": rows}
    return json.dumps(obj, indent=1) + "\n"


def write_witness(n: int, side: Fraction, corners, ids=None, side_text: str | None = None,
                  origin: str = "lower-left") -> str:
    lines = [
        "softschema:", "  contract: packing.squares:Witness/v2",
        "  schema: witness.schema.yaml", "  envelope: witness", "  status: enforced",
        "witness:", "  id: W-r127-control", f"  n: {n}",
        f"  side: {side_text if side_text is not None else fmt(side)}",
        "  square_size: '1'", "  representation: corners", "  scalar:", "    kind: rational",
        "  coordinates:", f"    origin: {origin}", "    axes: x-right-y-up",
        "    angle_unit: not-applicable", "  claim:", "    coordinate_provenance: reported",
        "    method: exact-algebraic", "    limitations: control file written by r127_controls",
        "  squares:",
    ]
    for k, pts in enumerate(corners):
        ident = ids[k] if ids is not None else f"square-{k + 1}"
        lines.append(f"  - id: {ident}")
        lines.append("    corners:")
        for x, y in pts:
            lines.append(f"    - - '{fmt(x)}'" if x.denominator == 1 else f"    - - {fmt(x)}")
            lines.append(f"      - '{fmt(y)}'" if y.denominator == 1 else f"      - {fmt(y)}")
    return "\n".join(lines) + "\n"
