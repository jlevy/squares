"""Strict reader for a corners/rational Witness/v2 certificate and its JSON twin.

Lane L127, stage 4 review of jlevy/squares#967. Clean room: written for this review,
importing nothing from the repository under review or from the source, and reusing no
code of any earlier review.

The reader refuses anything it does not expect and hands back integers only:

- YAML: exactly one document; no anchors, aliases or explicit tags (the bare `!` too);
  no duplicate keys; every scalar must resolve to a string or a plain decimal integer.
- Layout: the keys the schema allows, the envelope values this review expects, ids
  1..n in order, four corners of two scalars each.
- Scalars: canonical `p` or `p/q` with q > 1 and gcd(|p|, q) = 1.
- JSON twin, when given: floats, constants (NaN, Infinity) and duplicate keys refused;
  the tree must equal the YAML's exactly, with equal types.
"""

from __future__ import annotations

import json
import re
from math import gcd
from typing import Any

import yaml

INT_TAG = "tag:yaml.org,2002:int"
STR_TAG = "tag:yaml.org,2002:str"
MAP_TAG = "tag:yaml.org,2002:map"
SEQ_TAG = "tag:yaml.org,2002:seq"

PLAIN_INT = re.compile(r"(0|[1-9][0-9]*)")
RATIONAL = re.compile(r"(0|-?[1-9][0-9]*)(?:/([1-9][0-9]*))?")

TOP_KEYS = {"softschema", "witness"}
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
WITNESS_ALLOWED = WITNESS_REQUIRED | {"source", "certificate"}
CLAIM_REQUIRED = {"coordinate_provenance", "method", "limitations"}
CLAIM_ALLOWED = CLAIM_REQUIRED | {"precision", "tolerance"}
SOURCE_ALLOWED = {"key", "path", "url", "retrieved", "revision", "revision_sha256"}


class Refused(Exception):
    """The input is not a certificate this reader accepts; the message says why."""


def _refuse(why: str) -> Refused:
    return Refused(why)


# ---------------------------------------------------------------- YAML


def _scan_events(text: str) -> None:
    """Refuse anchors, aliases, explicit tags and more than one document."""
    docs = 0
    try:
        for ev in yaml.parse(text, Loader=yaml.SafeLoader):
            if isinstance(ev, yaml.AliasEvent):
                raise _refuse("yaml: alias")
            if isinstance(ev, yaml.DocumentStartEvent):
                docs += 1
                if docs > 1:
                    raise _refuse("yaml: more than one document")
            anchor = getattr(ev, "anchor", None)
            if anchor is not None:
                raise _refuse("yaml: anchor")
            tag = getattr(ev, "tag", None)
            if tag is not None:
                raise _refuse("yaml: explicit tag")
    except yaml.YAMLError as exc:
        raise _refuse(f"yaml: syntax: {type(exc).__name__}") from None
    if docs != 1:
        raise _refuse("yaml: no document")


def _build(node: yaml.Node, path: str) -> Any:
    if isinstance(node, yaml.ScalarNode):
        if node.tag == STR_TAG:
            return node.value
        if node.tag == INT_TAG:
            if node.style is not None and node.style != "":
                raise _refuse(f"yaml: quoted integer at {path}")
            if not PLAIN_INT.fullmatch(node.value):
                raise _refuse(f"yaml: integer not plain decimal at {path}")
            return int(node.value)
        raise _refuse(f"yaml: scalar type {node.tag} at {path}")
    if isinstance(node, yaml.SequenceNode):
        if node.tag != SEQ_TAG:
            raise _refuse(f"yaml: sequence tag {node.tag} at {path}")
        return [_build(item, f"{path}[{k}]") for k, item in enumerate(node.value)]
    if isinstance(node, yaml.MappingNode):
        if node.tag != MAP_TAG:
            raise _refuse(f"yaml: mapping tag {node.tag} at {path}")
        out: dict[str, Any] = {}
        for knode, vnode in node.value:
            if not isinstance(knode, yaml.ScalarNode) or knode.tag != STR_TAG:
                raise _refuse(f"yaml: non-string key at {path}")
            key = knode.value
            if key in out:
                raise _refuse(f"yaml: duplicate key {key!r} at {path}")
            out[key] = _build(vnode, f"{path}.{key}")
        return out
    raise _refuse(f"yaml: node kind at {path}")


def load_yaml_tree(text: str) -> Any:
    _scan_events(text)
    try:
        nodes = list(yaml.compose_all(text, Loader=yaml.SafeLoader))
    except yaml.YAMLError as exc:
        raise _refuse(f"yaml: syntax: {type(exc).__name__}") from None
    if len(nodes) != 1 or nodes[0] is None:
        raise _refuse("yaml: not exactly one document")
    return _build(nodes[0], "$")


# ---------------------------------------------------------------- JSON


def _no_float(_s: str) -> Any:
    raise _refuse("json: float")


def _no_constant(_s: str) -> Any:
    raise _refuse("json: constant")


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in pairs:
        if k in out:
            raise _refuse(f"json: duplicate key {k!r}")
        out[k] = v
    return out


def load_json_tree(text: str) -> Any:
    try:
        return json.loads(
            text,
            parse_float=_no_float,
            parse_constant=_no_constant,
            object_pairs_hook=_pairs,
        )
    except json.JSONDecodeError as exc:
        raise _refuse(f"json: syntax: {exc.msg}") from None


def same_tree(a: Any, b: Any) -> bool:
    """Equal values with equal types throughout (so 1 != True, '1' != 1)."""
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        if set(a) != set(b):
            return False
        return all(same_tree(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same_tree(x, y) for x, y in zip(a, b, strict=True))
    if isinstance(a, (str, int)):
        return a == b
    return False


# ---------------------------------------------------------------- layout


def parse_rational(s: Any, where: str) -> tuple[int, int]:
    """A canonical rational: returns (p, q) with q >= 1, gcd(|p|, q) == 1."""
    if not isinstance(s, str):
        raise _refuse(f"scalar not a string at {where}")
    m = RATIONAL.fullmatch(s)
    if m is None:
        raise _refuse(f"scalar not canonical at {where}")
    p = int(m.group(1))
    if m.group(2) is None:
        return p, 1
    q = int(m.group(2))
    if q <= 1:
        raise _refuse(f"denominator not above 1 at {where}")
    if gcd(abs(p), q) != 1:
        raise _refuse(f"scalar not in lowest terms at {where}")
    return p, q


def _keys(d: Any, required: set[str], allowed: set[str], where: str) -> None:
    if not isinstance(d, dict):
        raise _refuse(f"{where} not a mapping")
    missing = required - set(d)
    extra = set(d) - allowed
    if missing:
        raise _refuse(f"{where} missing {sorted(missing)}")
    if extra:
        raise _refuse(f"{where} has keys outside the schema {sorted(extra)}")


def _check_plain(v: Any, where: str) -> None:
    """Values in free-form blocks must still be strings, integers, lists or maps."""
    if isinstance(v, bool):
        raise _refuse(f"boolean at {where}")
    if isinstance(v, dict):
        for k, x in v.items():
            _check_plain(x, f"{where}.{k}")
    elif isinstance(v, list):
        for k, x in enumerate(v):
            _check_plain(x, f"{where}[{k}]")
    elif not isinstance(v, (str, int)):
        raise _refuse(f"value type at {where}")


def read_layout(tree: Any) -> dict[str, Any]:
    _keys(tree, TOP_KEYS, TOP_KEYS, "document")
    ss = tree["softschema"]
    _keys(ss, {"contract", "envelope"}, SOFTSCHEMA_KEYS, "softschema")
    if ss["contract"] != "packing.squares:Witness/v2":
        raise _refuse("softschema.contract")
    if ss["envelope"] != "witness":
        raise _refuse("softschema.envelope")
    _check_plain(ss, "softschema")
    w = tree["witness"]
    _keys(w, WITNESS_REQUIRED, WITNESS_ALLOWED, "witness")
    if not isinstance(w["id"], str) or not re.fullmatch(r"W-[a-z0-9][a-z0-9-]*", w["id"]):
        raise _refuse("witness.id")
    n = w["n"]
    if type(n) is not int or n < 1:
        raise _refuse("witness.n not a positive integer")
    if w["square_size"] != "1":
        raise _refuse("square_size")
    if w["representation"] != "corners":
        raise _refuse("representation")
    if w["scalar"] != {"kind": "rational"}:
        raise _refuse("scalar")
    if w["coordinates"] != {
        "origin": "lower-left",
        "axes": "x-right-y-up",
        "angle_unit": "not-applicable",
    }:
        raise _refuse("coordinates")
    _keys(w["claim"], CLAIM_REQUIRED, CLAIM_ALLOWED, "claim")
    _check_plain(w["claim"], "claim")
    if "source" in w:
        _keys(w["source"], {"path"}, SOURCE_ALLOWED, "source")
        _check_plain(w["source"], "source")
    if "certificate" in w:
        if not isinstance(w["certificate"], dict):
            raise _refuse("certificate not a mapping")
        _check_plain(w["certificate"], "certificate")
    side = parse_rational(w["side"], "side")
    if side[0] <= 0:
        raise _refuse("side not positive")
    sq = w["squares"]
    if not isinstance(sq, list):
        raise _refuse("squares not a list")
    if len(sq) != n:
        raise _refuse(f"squares: {len(sq)} entries for n = {n}")
    squares: list[list[tuple[tuple[int, int], tuple[int, int]]]] = []
    for k, entry in enumerate(sq):
        where = f"squares[{k}]"
        _keys(entry, {"id", "corners"}, {"id", "corners"}, where)
        if type(entry["id"]) is not int or entry["id"] != k + 1:
            raise _refuse(f"{where}: id is not {k + 1}")
        corners = entry["corners"]
        if not isinstance(corners, list) or len(corners) != 4:
            raise _refuse(f"{where}: not four corners")
        pts = []
        for c, pt in enumerate(corners):
            if not isinstance(pt, list) or len(pt) != 2:
                raise _refuse(f"{where}.corners[{c}]: not a point")
            pts.append(
                (
                    parse_rational(pt[0], f"{where}.corners[{c}][0]"),
                    parse_rational(pt[1], f"{where}.corners[{c}][1]"),
                )
            )
        squares.append(pts)
    return {"id": w["id"], "n": n, "side": side, "squares": squares}


def read_certificate(yaml_text: str, json_text: str | None) -> dict[str, Any]:
    tree = load_yaml_tree(yaml_text)
    out = read_layout(tree)
    if json_text is not None:
        twin = load_json_tree(json_text)
        if not same_tree(tree, twin):
            raise _refuse("json twin differs from the yaml")
        out["twin"] = "identical"
    else:
        out["twin"] = "not given"
    return out
