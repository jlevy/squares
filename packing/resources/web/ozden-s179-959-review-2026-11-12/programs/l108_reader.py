"""Strict reader for a rational-corner Witness/v2 certificate and its JSON twin.

Lane L108, blind stage 4 review of jlevy/squares#959. Written for this review from the
schema text and the file itself; it imports nothing from the repository or the source.

The reader decides the reading (layout, count, ids, canonical scalars, the twin) and
hands the two deciding methods integers only: the side as (p, q) and each square's four
corners as ((xp, xq), (yp, yq)). Anything it does not expect, it refuses.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

TAG_STR = "tag:yaml.org,2002:str"
TAG_INT = "tag:yaml.org,2002:int"
TAG_MAP = "tag:yaml.org,2002:map"
TAG_SEQ = "tag:yaml.org,2002:seq"

RATIONAL_RE = re.compile(r"(-?)(0|[1-9][0-9]*)(?:/([1-9][0-9]*))?")
INT_RE = re.compile(r"0|[1-9][0-9]*")

# The witness keys the schema's `properties` lists (additionalProperties: false).
WITNESS_KEYS = {
    "certificate",
    "claim",
    "coordinates",
    "id",
    "n",
    "representation",
    "scalar",
    "side",
    "source",
    "square_size",
    "squares",
}
WITNESS_REQUIRED = WITNESS_KEYS - {"certificate", "source"}


class Refused(Exception):
    """The reader refuses the file; the message is the reason."""


Rat = tuple[int, int]
Point = tuple[Rat, Rat]


@dataclass(frozen=True)
class Certificate:
    """What the deciding methods receive: integers only."""

    n: int
    side: Rat
    squares: tuple[tuple[Point, Point, Point, Point], ...]
    tree: dict[str, Any]


def parse_rational(text: object, where: str) -> Rat:
    """A canonical p or p/q with q > 1 and gcd(p, q) = 1, as (p, q)."""
    if not isinstance(text, str):
        raise Refused(f"{where}: scalar is {type(text).__name__}, not a string")
    m = RATIONAL_RE.fullmatch(text)
    if m is None:
        raise Refused(f"{where}: not a canonical rational: {text[:40]!r}")
    sign, num, den = m.groups()
    p = int(num)
    if sign and p == 0:
        raise Refused(f"{where}: negative zero")
    if sign:
        p = -p
    if den is None:
        return (p, 1)
    q = int(den)
    if q == 1:
        raise Refused(f"{where}: denominator 1 written out")
    if math.gcd(p, q) != 1:
        raise Refused(f"{where}: not in lowest terms")
    return (p, q)


def _check_events(text: str) -> None:
    """Refuse anchors, aliases and explicit tags before composing."""
    for event in yaml.parse(text, Loader=yaml.SafeLoader):
        if isinstance(event, yaml.AliasEvent):
            raise Refused("YAML alias")
        anchor = getattr(event, "anchor", None)
        if anchor is not None:
            raise Refused("YAML anchor")
        tag = getattr(event, "tag", None)
        if isinstance(event, (yaml.ScalarEvent, yaml.MappingStartEvent, yaml.SequenceStartEvent)):
            if tag not in (None, "!"):
                raise Refused(f"explicit YAML tag {tag}")


def _node_to_tree(node: yaml.Node, where: str) -> Any:
    if isinstance(node, yaml.MappingNode):
        if node.tag != TAG_MAP:
            raise Refused(f"{where}: mapping tag {node.tag}")
        out: dict[str, Any] = {}
        for key_node, value_node in node.value:
            if not isinstance(key_node, yaml.ScalarNode) or key_node.tag != TAG_STR:
                raise Refused(f"{where}: non-string key")
            key = key_node.value
            if key in out:
                raise Refused(f"{where}: duplicate key {key!r}")
            out[key] = _node_to_tree(value_node, f"{where}.{key}")
        return out
    if isinstance(node, yaml.SequenceNode):
        if node.tag != TAG_SEQ:
            raise Refused(f"{where}: sequence tag {node.tag}")
        return [_node_to_tree(item, f"{where}[{i}]") for i, item in enumerate(node.value)]
    if isinstance(node, yaml.ScalarNode):
        if node.tag == TAG_STR:
            return node.value
        if node.tag == TAG_INT:
            if INT_RE.fullmatch(node.value) is None:
                raise Refused(f"{where}: non-canonical integer {node.value!r}")
            return int(node.value)
        raise Refused(f"{where}: scalar tag {node.tag}")
    raise Refused(f"{where}: unexpected node")


def load_yaml_tree(text: str) -> Any:
    _check_events(text)
    try:
        node = yaml.compose(text, Loader=yaml.SafeLoader)
    except yaml.YAMLError as exc:  # several documents, syntax errors
        raise Refused(f"YAML: {type(exc).__name__}") from exc
    if node is None:
        raise Refused("empty YAML")
    return _node_to_tree(node, "$")


def _no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise Refused(f"JSON duplicate key {key!r}")
        out[key] = value
    return out


def _refuse_float(text: str) -> Any:
    raise Refused(f"JSON float {text[:20]!r}")


def _refuse_constant(text: str) -> Any:
    raise Refused(f"JSON constant {text!r}")


def load_json_tree(text: str) -> Any:
    try:
        return json.loads(
            text,
            object_pairs_hook=_no_duplicates,
            parse_float=_refuse_float,
            parse_constant=_refuse_constant,
        )
    except json.JSONDecodeError as exc:
        raise Refused(f"JSON: {exc.msg}") from exc


def same_tree(a: Any, b: Any) -> bool:
    """Equal values with exactly equal types throughout (bool is not int)."""
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        if set(a) != set(b):
            return False
        return all(same_tree(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same_tree(x, y) for x, y in zip(a, b, strict=True))
    return a == b


def _expect(cond: bool, reason: str) -> None:
    if not cond:
        raise Refused(reason)


def read_texts(yaml_text: str, json_text: str | None) -> Certificate:
    """Read the certificate from its texts; refuse anything unexpected."""
    tree = load_yaml_tree(yaml_text)
    if json_text is not None:
        twin = load_json_tree(json_text)
        _expect(same_tree(tree, twin), "the JSON twin differs from the YAML")
    _expect(isinstance(tree, dict), "top level is not a mapping")
    _expect(set(tree) == {"softschema", "witness"}, f"top-level keys {sorted(tree)}")
    soft = tree["softschema"]
    _expect(isinstance(soft, dict), "softschema is not a mapping")
    _expect(soft.get("contract") == "packing.squares:Witness/v2", "contract")
    _expect(soft.get("envelope") == "witness", "envelope")
    w = tree["witness"]
    _expect(isinstance(w, dict), "witness is not a mapping")
    _expect(set(w) <= WITNESS_KEYS, f"unknown witness keys {sorted(set(w) - WITNESS_KEYS)}")
    _expect(WITNESS_REQUIRED <= set(w), f"missing witness keys {sorted(WITNESS_REQUIRED - set(w))}")
    _expect(w["representation"] == "corners", "representation is not corners")
    _expect(w["scalar"] == {"kind": "rational"}, "scalar kind is not rational")
    _expect(w["square_size"] == "1", "square_size is not '1'")
    _expect(
        w["coordinates"] == {"origin": "lower-left", "axes": "x-right-y-up", "angle_unit": "not-applicable"},
        "coordinates block",
    )
    n = w["n"]
    _expect(type(n) is int and n >= 1, "n is not a positive integer")
    side = parse_rational(w["side"], "side")
    _expect(side[0] > 0, "side is not positive")
    squares = w["squares"]
    _expect(isinstance(squares, list), "squares is not a list")
    _expect(len(squares) == n, f"{len(squares)} squares listed for n = {n}")
    out: list[tuple[Point, Point, Point, Point]] = []
    for index, entry in enumerate(squares, start=1):
        where = f"square {index}"
        _expect(isinstance(entry, dict), f"{where}: not a mapping")
        _expect(set(entry) == {"id", "corners"}, f"{where}: keys {sorted(entry)}")
        _expect(type(entry["id"]) is int and entry["id"] == index, f"{where}: id {entry['id']!r}")
        corners = entry["corners"]
        _expect(isinstance(corners, list) and len(corners) == 4, f"{where}: not four corners")
        pts: list[Point] = []
        for k, pt in enumerate(corners):
            _expect(isinstance(pt, list) and len(pt) == 2, f"{where} corner {k}: not a pair")
            pts.append((parse_rational(pt[0], f"{where} corner {k} x"), parse_rational(pt[1], f"{where} corner {k} y")))
        out.append((pts[0], pts[1], pts[2], pts[3]))
    return Certificate(n=n, side=side, squares=tuple(out), tree=tree)


def read_paths(yaml_path: Path, json_path: Path | None) -> Certificate:
    yaml_text = yaml_path.read_text(encoding="utf-8")
    json_text = None if json_path is None else json_path.read_text(encoding="utf-8")
    return read_texts(yaml_text, json_text)


def scalar_count(cert: Certificate) -> int:
    return 1 + 8 * len(cert.squares)
