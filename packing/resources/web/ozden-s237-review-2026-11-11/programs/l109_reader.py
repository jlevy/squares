"""Lane L109's strict reader for a corners Witness/v2 file and its JSON twin.

Written for the blind stage 4 review of issue #960. It imports nothing from the
repository or from the source. It composes the YAML with PyYAML's parser and composer
only, never its constructor; refuses anchors, aliases, explicit tags, duplicate keys
and every resolved tag but string, integer, mapping and sequence; builds plain Python
values itself; requires the JSON twin, read with floats, constants and duplicate keys
refused, to hold the same tree with the same types; and returns the side and every
corner as exact integer pairs (numerator, denominator), each in lowest terms.

Any layout it does not expect is refused with a reason (``ReadRefused``).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from math import gcd
from typing import Any

import yaml

STR = "tag:yaml.org,2002:str"
INT = "tag:yaml.org,2002:int"
MAP = "tag:yaml.org,2002:map"
SEQ = "tag:yaml.org,2002:seq"

CANON_INT = re.compile(r"(0|[1-9][0-9]*)\Z")
CANON_RAT = re.compile(r"(0|-?[1-9][0-9]*)(?:/([1-9][0-9]*))?\Z")

ENVELOPE_KEYS = {"softschema", "witness"}
SOFTSCHEMA_KEYS = {"contract", "schema", "envelope", "status"}
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
WITNESS_OPTIONAL = {"source", "certificate"}


class ReadRefused(Exception):
    """The file or its twin is not read: the message says why."""


Rat = tuple[int, int]


@dataclass(frozen=True)
class Read:
    n: int
    side: Rat
    corners: list[list[tuple[Rat, Rat]]]  # squares in id order, four (x, y) each
    scalars: int  # how many scalars were parsed (side plus coordinates)
    integer_scalars: int  # how many of them were written as integers


def _refuse(why: str) -> None:
    raise ReadRefused(why)


def _check_events(text: str) -> None:
    for ev in yaml.parse(text, Loader=yaml.SafeLoader):
        if isinstance(ev, yaml.AliasEvent):
            _refuse(f"alias at {ev.start_mark}")
        anchor = getattr(ev, "anchor", None)
        if anchor is not None:
            _refuse(f"anchor {anchor!r} at {ev.start_mark}")
        tag = getattr(ev, "tag", None)
        if isinstance(ev, (yaml.ScalarEvent, yaml.SequenceStartEvent, yaml.MappingStartEvent)) and tag is not None:
            _refuse(f"explicit tag {tag!r} at {ev.start_mark}")


def _build(node: yaml.Node) -> Any:
    if isinstance(node, yaml.MappingNode):
        if node.tag != MAP:
            _refuse(f"mapping tag {node.tag} at {node.start_mark}")
        out: dict[str, Any] = {}
        for knode, vnode in node.value:
            if not isinstance(knode, yaml.ScalarNode) or knode.tag != STR:
                _refuse(f"non-string key at {knode.start_mark}")
            key = knode.value
            if key in out:
                _refuse(f"duplicate key {key!r} at {knode.start_mark}")
            out[key] = _build(vnode)
        return out
    if isinstance(node, yaml.SequenceNode):
        if node.tag != SEQ:
            _refuse(f"sequence tag {node.tag} at {node.start_mark}")
        return [_build(v) for v in node.value]
    if isinstance(node, yaml.ScalarNode):
        if node.tag == STR:
            return node.value
        if node.tag == INT:
            if not CANON_INT.match(node.value):
                _refuse(f"non-canonical integer {node.value!r} at {node.start_mark}")
            return int(node.value)
        _refuse(f"scalar tag {node.tag} ({node.value!r}) at {node.start_mark}")
    _refuse(f"unexpected node {type(node).__name__}")
    return None  # unreachable


def yaml_tree(text: str) -> Any:
    """The YAML document as plain values, strictly."""
    try:
        _check_events(text)
        docs = list(yaml.compose_all(text, Loader=yaml.SafeLoader))
    except yaml.YAMLError as exc:
        raise ReadRefused(f"YAML error: {exc}") from exc
    if len(docs) != 1 or docs[0] is None:
        _refuse(f"expected one document, found {len(docs)}")
    return _build(docs[0])


def _no_dupes(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in pairs:
        if k in out:
            _refuse(f"JSON duplicate key {k!r}")
        out[k] = v
    return out


def _no_float(s: str) -> Any:
    _refuse(f"JSON float {s!r}")


def _no_const(s: str) -> Any:
    _refuse(f"JSON constant {s!r}")


def json_tree(text: str) -> Any:
    try:
        return json.loads(text, object_pairs_hook=_no_dupes, parse_float=_no_float, parse_constant=_no_const)
    except json.JSONDecodeError as exc:
        raise ReadRefused(f"JSON error: {exc}") from exc


def same_tree(a: Any, b: Any, path: str = "$") -> str | None:
    """None when equal with equal types everywhere, else the first difference."""
    if type(a) is not type(b):
        return f"{path}: type {type(a).__name__} vs {type(b).__name__}"
    if isinstance(a, dict):
        if set(a) != set(b):
            return f"{path}: keys {sorted(a)} vs {sorted(b)}"
        for k in a:
            d = same_tree(a[k], b[k], f"{path}.{k}")
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return f"{path}: length {len(a)} vs {len(b)}"
        for i, (x, y) in enumerate(zip(a, b, strict=True)):
            d = same_tree(x, y, f"{path}[{i}]")
            if d:
                return d
        return None
    if a != b:
        return f"{path}: value differs"
    return None


def rational(s: Any, where: str) -> Rat:
    """A canonical p or p/q with q > 1 and gcd(p, q) = 1, as (p, q)."""
    if not isinstance(s, str):
        _refuse(f"{where}: scalar is {type(s).__name__}, not a string")
    m = CANON_RAT.match(s)
    if not m:
        _refuse(f"{where}: non-canonical scalar {s[:40]!r}")
    p = int(m.group(1))
    if m.group(2) is None:
        return (p, 1)
    q = int(m.group(2))
    if q <= 1:
        _refuse(f"{where}: denominator {q} not above 1")
    if gcd(p, q) != 1:
        _refuse(f"{where}: not in lowest terms")
    return (p, q)


def _expect(cond: bool, why: str) -> None:
    if not cond:
        _refuse(why)


def read_texts(yaml_text: str, json_text: str | None) -> Read:
    tree = yaml_tree(yaml_text)
    if json_text is not None:
        twin = json_tree(json_text)
        diff = same_tree(tree, twin)
        if diff:
            _refuse(f"the JSON twin differs: {diff}")
    _expect(isinstance(tree, dict) and set(tree) == ENVELOPE_KEYS, "envelope keys")
    ss = tree["softschema"]
    _expect(isinstance(ss, dict) and set(ss) == SOFTSCHEMA_KEYS, "softschema keys")
    _expect(ss["contract"] == "packing.squares:Witness/v2", "contract")
    _expect(ss["envelope"] == "witness", "envelope name")
    w = tree["witness"]
    _expect(isinstance(w, dict), "witness is not a mapping")
    keys = set(w)
    _expect(WITNESS_REQUIRED <= keys, f"witness lacks {sorted(WITNESS_REQUIRED - keys)}")
    _expect(keys <= WITNESS_REQUIRED | WITNESS_OPTIONAL, f"witness has {sorted(keys - WITNESS_REQUIRED - WITNESS_OPTIONAL)}")
    _expect(w["square_size"] == "1", "square_size is not '1'")
    _expect(w["representation"] == "corners", "representation is not corners")
    _expect(w["scalar"] == {"kind": "rational"}, "scalar is not {kind: rational}")
    _expect(
        w["coordinates"] == {"origin": "lower-left", "axes": "x-right-y-up", "angle_unit": "not-applicable"},
        "coordinates are not lower-left, x-right-y-up, not-applicable",
    )
    n = w["n"]
    _expect(type(n) is int and n >= 1, "n")
    side = rational(w["side"], "side")
    _expect(side[0] > 0, "side not positive")
    sq = w["squares"]
    _expect(isinstance(sq, list), "squares is not a list")
    _expect(len(sq) == n, f"{len(sq)} squares listed, n = {n}")
    corners: list[list[tuple[Rat, Rat]]] = []
    scalars, ints = 1, int(side[1] == 1)
    for i, entry in enumerate(sq, start=1):
        _expect(isinstance(entry, dict) and set(entry) == {"id", "corners"}, f"square {i}: keys")
        _expect(type(entry["id"]) is int and entry["id"] == i, f"square {i}: id {entry['id']!r}")
        cs = entry["corners"]
        _expect(isinstance(cs, list) and len(cs) == 4, f"square {i}: not four corners")
        pts: list[tuple[Rat, Rat]] = []
        for j, pt in enumerate(cs):
            _expect(isinstance(pt, list) and len(pt) == 2, f"square {i} corner {j}: not a pair")
            x = rational(pt[0], f"square {i} corner {j} x")
            y = rational(pt[1], f"square {i} corner {j} y")
            scalars += 2
            ints += int(x[1] == 1) + int(y[1] == 1)
            pts.append((x, y))
        corners.append(pts)
    return Read(n=n, side=side, corners=corners, scalars=scalars, integer_scalars=ints)


def read_files(yaml_path: str, json_path: str | None) -> Read:
    with open(yaml_path, encoding="utf-8") as f:
        yt = f.read()
    jt = None
    if json_path is not None:
        with open(json_path, encoding="utf-8") as f:
            jt = f.read()
    return read_texts(yt, jt)
