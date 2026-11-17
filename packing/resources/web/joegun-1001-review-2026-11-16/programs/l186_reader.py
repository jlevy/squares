"""Lane L186: a strict reader for Witness/v2 files with rational corners.

Written clean-room for the stage 4 review of issue #1001. It imports nothing from
this repository or from the source repository. It is the one part the two
deciding methods share: it turns the file's text into exact rationals and
checks the file's form, and decides nothing about geometry.

What it accepts, and refuses otherwise:

- one YAML document, no anchors, aliases or explicit tags, no duplicate keys, no
  tab, carriage return or byte-order mark; scalars resolve only to strings and
  plain decimal integers;
- the softschema envelope `{softschema: {contract: packing.squares:Witness/v2,
  envelope: witness, ...}, witness: {...}}`;
- `witness` keys within the schema's list, the required ones present;
  `square_size: '1'`, `representation: corners`, `scalar: {kind: rational}`,
  `coordinates.origin: lower-left`, `coordinates.axes: x-right-y-up`;
- `squares`: exactly `n` entries, ids 1 to n in order, each with exactly the keys
  `id` and `corners`, four corners of two scalars each;
- every scalar (side and corners) a string `p` or `p/q`, an optional minus sign,
  digits without a leading zero, `q >= 1` without a leading zero.

Canonical form (lowest terms, `q >= 2` when written, no `-0`, no `0/q`) is
recorded, not required: the value is what is decided.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from fractions import Fraction
from math import gcd
from typing import Any

import yaml

SCALAR_RE = re.compile(r"(-?)(0|[1-9][0-9]*)(?:/([1-9][0-9]*))?\Z")
INT_RE = re.compile(r"(0|[1-9][0-9]*)\Z")

WITNESS_KEYS = {
    "id",
    "n",
    "side",
    "square_size",
    "representation",
    "scalar",
    "coordinates",
    "squares",
    "claim",
    "source",
    "certificate",
}
WITNESS_REQUIRED = {
    "id",
    "n",
    "side",
    "square_size",
    "representation",
    "scalar",
    "coordinates",
    "squares",
    "claim",
}
ENVELOPE_KEYS = {"contract", "schema", "envelope", "status"}
COORD_KEYS = {"origin", "axes", "angle_unit"}
CONTRACT = "packing.squares:Witness/v2"

Point = tuple[Fraction, Fraction]
Square = tuple[Point, Point, Point, Point]


class ReadError(Exception):
    """The file is refused by the reader."""


@dataclass
class Witness:
    n: int
    side: Fraction
    side_text: str
    squares: list[Square]
    sha256: str
    witness_id: str
    meta: dict[str, Any] = field(default_factory=dict)
    noncanonical: list[str] = field(default_factory=list)


def parse_scalar(text: object, where: str) -> tuple[Fraction, bool]:
    """Return the exact value of a scalar string and whether it is canonical."""
    if not isinstance(text, str):
        raise ReadError(f"{where}: scalar is not a string: {text!r}")
    m = SCALAR_RE.match(text)
    if m is None:
        raise ReadError(f"{where}: not a rational scalar: {text[:60]!r}")
    sign, num_s, den_s = m.group(1), m.group(2), m.group(3)
    num = int(num_s)
    den = int(den_s) if den_s is not None else 1
    value = Fraction(-num if sign else num, den)
    canonical = True
    if sign and num == 0:
        canonical = False
    if den_s is not None and (den < 2 or gcd(num, den) != 1 or num == 0):
        canonical = False
    return value, canonical


def _check_events(text: str) -> None:
    for ev in yaml.parse(text, Loader=yaml.SafeLoader):
        if isinstance(ev, yaml.AliasEvent):
            raise ReadError("alias in YAML")
        anchor = getattr(ev, "anchor", None)
        if anchor is not None:
            raise ReadError(f"anchor in YAML: {anchor}")
        tag = getattr(ev, "tag", None)
        if isinstance(ev, yaml.ScalarEvent):
            implicit = ev.implicit
            if tag is not None and not (implicit[0] or implicit[1]):
                raise ReadError(f"explicit tag in YAML: {tag}")
        elif isinstance(ev, (yaml.MappingStartEvent, yaml.SequenceStartEvent)):
            if tag is not None and not ev.implicit:
                raise ReadError(f"explicit tag in YAML: {tag}")


def _to_plain(node: yaml.Node, path: str) -> Any:
    if isinstance(node, yaml.MappingNode):
        out: dict[str, Any] = {}
        for knode, vnode in node.value:
            if not isinstance(knode, yaml.ScalarNode) or knode.tag != "tag:yaml.org,2002:str":
                raise ReadError(f"{path}: non-string key")
            key = knode.value
            if key in out:
                raise ReadError(f"{path}: duplicate key {key!r}")
            out[key] = _to_plain(vnode, f"{path}.{key}")
        return out
    if isinstance(node, yaml.SequenceNode):
        return [_to_plain(v, f"{path}[{i}]") for i, v in enumerate(node.value)]
    if isinstance(node, yaml.ScalarNode):
        if node.tag == "tag:yaml.org,2002:str":
            return node.value
        if node.tag == "tag:yaml.org,2002:int" and node.style is None:
            if INT_RE.match(node.value) is None:
                raise ReadError(f"{path}: integer not in plain decimal form: {node.value!r}")
            return int(node.value)
        raise ReadError(f"{path}: scalar of type {node.tag} refused: {node.value[:40]!r}")
    raise ReadError(f"{path}: unknown node")


def load_yaml_strict(text: str) -> Any:
    if "\t" in text or "\r" in text or text.startswith("﻿"):
        raise ReadError("tab, carriage return or byte-order mark in file")
    try:
        _check_events(text)
        node = yaml.compose(text, Loader=yaml.SafeLoader)
    except yaml.YAMLError as exc:
        raise ReadError(f"YAML error: {exc}") from exc
    if node is None:
        raise ReadError("empty document")
    return _to_plain(node, "$")


def read_witness_text(text: str, sha256: str = "") -> Witness:
    doc = load_yaml_strict(text)
    if not isinstance(doc, dict) or set(doc) != {"softschema", "witness"}:
        raise ReadError("top level must be exactly the keys softschema and witness")
    env = doc["softschema"]
    if not isinstance(env, dict) or not set(env) <= ENVELOPE_KEYS:
        raise ReadError("softschema envelope keys")
    if env.get("contract") != CONTRACT or env.get("envelope") != "witness":
        raise ReadError("softschema contract or envelope")
    w = doc["witness"]
    if not isinstance(w, dict):
        raise ReadError("witness is not a mapping")
    keys = set(w)
    if not keys <= WITNESS_KEYS:
        raise ReadError(f"unknown witness keys: {sorted(keys - WITNESS_KEYS)}")
    if not WITNESS_REQUIRED <= keys:
        raise ReadError(f"missing witness keys: {sorted(WITNESS_REQUIRED - keys)}")
    n = w["n"]
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ReadError("n is not a positive integer")
    if w["square_size"] != "1":
        raise ReadError("square_size is not '1'")
    if w["representation"] != "corners":
        raise ReadError("representation is not corners")
    if w["scalar"] != {"kind": "rational"}:
        raise ReadError("scalar is not {kind: rational}")
    coords = w["coordinates"]
    if not isinstance(coords, dict) or set(coords) != COORD_KEYS:
        raise ReadError("coordinates keys")
    if coords["origin"] != "lower-left" or coords["axes"] != "x-right-y-up":
        raise ReadError("coordinates must be origin lower-left, axes x-right-y-up")
    wid = w["id"]
    if not isinstance(wid, str):
        raise ReadError("id is not a string")
    noncanonical: list[str] = []
    side, ok = parse_scalar(w["side"], "side")
    if not ok:
        noncanonical.append("side")
    if side <= 0:
        raise ReadError("side is not positive")
    sq_list = w["squares"]
    if not isinstance(sq_list, list):
        raise ReadError("squares is not a list")
    if len(sq_list) != n:
        raise ReadError(f"n is {n}, {len(sq_list)} squares listed")
    squares: list[Square] = []
    for idx, entry in enumerate(sq_list):
        where = f"squares[{idx}]"
        if not isinstance(entry, dict) or set(entry) != {"id", "corners"}:
            raise ReadError(f"{where}: keys must be exactly id and corners")
        if entry["id"] != idx + 1 or isinstance(entry["id"], bool):
            raise ReadError(f"{where}: id {entry['id']!r}, expected {idx + 1}")
        corners = entry["corners"]
        if not isinstance(corners, list) or len(corners) != 4:
            raise ReadError(f"{where}: four corners required")
        pts: list[Point] = []
        for k, pt in enumerate(corners):
            if not isinstance(pt, list) or len(pt) != 2:
                raise ReadError(f"{where}.corners[{k}]: a point has two scalars")
            x, okx = parse_scalar(pt[0], f"{where}.corners[{k}][0]")
            y, oky = parse_scalar(pt[1], f"{where}.corners[{k}][1]")
            if not okx:
                noncanonical.append(f"{where}.corners[{k}][0]")
            if not oky:
                noncanonical.append(f"{where}.corners[{k}][1]")
            pts.append((x, y))
        squares.append((pts[0], pts[1], pts[2], pts[3]))
    meta = {
        "envelope": env,
        "claim": w["claim"],
        "source": w.get("source"),
        "certificate": w.get("certificate"),
        "angle_unit": coords["angle_unit"],
    }
    return Witness(
        n=n,
        side=side,
        side_text=w["side"],
        squares=squares,
        sha256=sha256,
        witness_id=wid,
        meta=meta,
        noncanonical=noncanonical,
    )


def read_witness_file(path: str) -> Witness:
    with open(path, "rb") as fh:
        data = fh.read()
    digest = hashlib.sha256(data).hexdigest()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ReadError("not UTF-8") from exc
    return read_witness_text(text, digest)


def frac_text(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else f"{v.numerator}/{v.denominator}"


def dump_witness_text(w: Witness, side_text: str | None = None) -> str:
    """Write a packing back as a Witness/v2 corners file (for controls and tests)."""
    lines = [
        "softschema:",
        f"  contract: {CONTRACT}",
        "  schema: witness.schema.yaml",
        "  envelope: witness",
        "  status: enforced",
        "witness:",
        f"  id: {w.witness_id}",
        f"  n: {len(w.squares)}",
        f"  side: '{side_text if side_text is not None else frac_text(w.side)}'",
        "  square_size: '1'",
        "  representation: corners",
        "  scalar:",
        "    kind: rational",
        "  coordinates:",
        "    origin: lower-left",
        "    axes: x-right-y-up",
        "    angle_unit: not-applicable",
        "  squares:",
    ]
    for i, sq in enumerate(w.squares):
        lines.append(f"  - id: {i + 1}")
        lines.append("    corners:")
        for x, y in sq:
            lines.append(f"    - - '{frac_text(x)}'")
            lines.append(f"      - '{frac_text(y)}'")
    lines += [
        "  claim:",
        "    coordinate_provenance: reported",
        "    method: exact-algebraic",
        "    limitations: written back by lane L186 for a control",
    ]
    return "\n".join(lines) + "\n"
