"""Lane L117: a strict reader for a corners, rational Witness/v2 file and its JSON twin.

Clean-room code written for the stage 4 review of jlevy/squares#962. It imports
nothing from the repository or the source. It hands both methods integers only:
every scalar becomes a pair (p, q) with q >= 1.

Refusals raise ReadRefused with a short reason string.
"""

from __future__ import annotations

import json
import math
import re

import yaml

CONTRACT = "packing.squares:Witness/v2"
WITNESS_KEYS = {
    "id", "n", "side", "square_size", "representation", "scalar",
    "coordinates", "squares", "claim", "source", "certificate",
}
WITNESS_REQUIRED = {
    "id", "n", "side", "square_size", "representation", "scalar",
    "coordinates", "squares", "claim",
}
SCALAR_RE = re.compile(r"(-?)(0|[1-9][0-9]*)(?:/([1-9][0-9]*))?")
INT_RE = re.compile(r"0|[1-9][0-9]*")
STR_TAG = "tag:yaml.org,2002:str"
INT_TAG = "tag:yaml.org,2002:int"


class ReadRefused(Exception):
    """The file is not read; the message says why."""


def _strict_yaml(text: str) -> object:
    """Compose YAML, refusing anchors, aliases, tags, duplicate keys and other types."""
    try:
        events = list(yaml.parse(text, Loader=yaml.SafeLoader))
    except yaml.YAMLError as exc:
        raise ReadRefused(f"yaml syntax: {type(exc).__name__}") from exc
    for ev in events:
        if isinstance(ev, yaml.AliasEvent):
            raise ReadRefused("yaml alias")
        if getattr(ev, "anchor", None) is not None:
            raise ReadRefused("yaml anchor")
        if isinstance(ev, (yaml.ScalarEvent, yaml.MappingStartEvent, yaml.SequenceStartEvent)):
            if ev.tag is not None:
                raise ReadRefused("yaml explicit tag")
    try:
        root = yaml.compose(text, Loader=yaml.SafeLoader)
    except yaml.YAMLError as exc:  # several documents, or a syntax error
        raise ReadRefused(f"yaml compose: {type(exc).__name__}") from exc
    if root is None:
        raise ReadRefused("empty yaml")
    return _node_value(root)


def _node_value(node: yaml.Node) -> object:
    if isinstance(node, yaml.MappingNode):
        out: dict[str, object] = {}
        for knode, vnode in node.value:
            if not isinstance(knode, yaml.ScalarNode) or knode.tag != STR_TAG:
                raise ReadRefused("mapping key not a string")
            if knode.value in out:
                raise ReadRefused(f"duplicate key {knode.value!r}")
            out[knode.value] = _node_value(vnode)
        return out
    if isinstance(node, yaml.SequenceNode):
        return [_node_value(v) for v in node.value]
    if isinstance(node, yaml.ScalarNode):
        if node.tag == STR_TAG:
            return str(node.value)
        if node.tag == INT_TAG:
            if INT_RE.fullmatch(node.value) is None:
                raise ReadRefused(f"integer not in plain decimal form: {node.value!r}")
            return int(node.value)
        raise ReadRefused(f"scalar of type {node.tag}")
    raise ReadRefused("unknown yaml node")


def _no_float(text: str) -> object:
    raise ReadRefused(f"json float {text!r}")


def _no_constant(text: str) -> object:
    raise ReadRefused(f"json constant {text!r}")


def _no_dups(pairs: list[tuple[str, object]]) -> dict[str, object]:
    out: dict[str, object] = {}
    for k, v in pairs:
        if k in out:
            raise ReadRefused(f"json duplicate key {k!r}")
        out[k] = v
    return out


def _strict_json(text: str) -> object:
    try:
        return json.loads(
            text, parse_float=_no_float, parse_constant=_no_constant, object_pairs_hook=_no_dups
        )
    except json.JSONDecodeError as exc:
        raise ReadRefused("json syntax") from exc


def same_tree(a: object, b: object) -> bool:
    """Exactly the same tree with exactly the same types (bool is not int)."""
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        assert isinstance(b, dict)
        if set(a) != set(b):
            return False
        return all(same_tree(a[k], b[k]) for k in a)
    if isinstance(a, list):
        assert isinstance(b, list)
        return len(a) == len(b) and all(same_tree(x, y) for x, y in zip(a, b, strict=True))
    return a == b


def scalar(s: object) -> tuple[int, int]:
    """A canonical rational p or p/q (q > 1, gcd 1) as integers (p, q)."""
    if not isinstance(s, str):
        raise ReadRefused(f"scalar not a string: {type(s).__name__}")
    m = SCALAR_RE.fullmatch(s)
    if m is None:
        raise ReadRefused(f"scalar not canonical: {s[:40]!r}")
    sign, num, den = m.groups()
    p = int(num)
    if sign and p == 0:
        raise ReadRefused("negative zero")
    if sign:
        p = -p
    if den is None:
        return p, 1
    q = int(den)
    if q == 1:
        raise ReadRefused("denominator 1")
    if math.gcd(p, q) != 1:
        raise ReadRefused("scalar not in lowest terms")
    return p, q


def _expect(cond: bool, why: str) -> None:
    if not cond:
        raise ReadRefused(why)


def interpret(tree: object) -> dict[str, object]:
    """Check the envelope and return {'n', 'side', 'squares', 'meta'} with integer scalars."""
    _expect(isinstance(tree, dict), "top level not a mapping")
    assert isinstance(tree, dict)
    _expect(set(tree) == {"softschema", "witness"}, f"top-level keys {sorted(tree)}")
    ss = tree["softschema"]
    _expect(isinstance(ss, dict), "softschema not a mapping")
    assert isinstance(ss, dict)
    _expect(ss.get("contract") == CONTRACT, "contract")
    _expect(ss.get("envelope") == "witness", "envelope")
    w = tree["witness"]
    _expect(isinstance(w, dict), "witness not a mapping")
    assert isinstance(w, dict)
    _expect(set(w) <= WITNESS_KEYS, f"witness keys outside the schema: {sorted(set(w) - WITNESS_KEYS)}")
    _expect(WITNESS_REQUIRED <= set(w), f"witness keys missing: {sorted(WITNESS_REQUIRED - set(w))}")
    _expect(w["square_size"] == "1", "square_size")
    _expect(w["representation"] == "corners", "representation")
    _expect(w["scalar"] == {"kind": "rational"}, "scalar kind")
    _expect(
        w["coordinates"]
        == {"origin": "lower-left", "axes": "x-right-y-up", "angle_unit": "not-applicable"},
        "coordinates",
    )
    n = w["n"]
    _expect(type(n) is int and n >= 1, "n not a positive integer")
    assert isinstance(n, int)
    side = scalar(w["side"])
    _expect(side[0] > 0, "side not positive")
    sq = w["squares"]
    _expect(isinstance(sq, list), "squares not a list")
    assert isinstance(sq, list)
    _expect(len(sq) == n, f"{len(sq)} squares for n = {n}")
    squares: list[list[tuple[tuple[int, int], tuple[int, int]]]] = []
    zeros = 0
    for k, entry in enumerate(sq, start=1):
        _expect(isinstance(entry, dict), f"square {k} not a mapping")
        assert isinstance(entry, dict)
        _expect(set(entry) == {"id", "corners"}, f"square {k} keys {sorted(entry)}")
        _expect(type(entry["id"]) is int and entry["id"] == k, f"square {k} id")
        cs = entry["corners"]
        _expect(isinstance(cs, list) and len(cs) == 4, f"square {k} corners")
        assert isinstance(cs, list)
        pts: list[tuple[tuple[int, int], tuple[int, int]]] = []
        for pt in cs:
            _expect(isinstance(pt, list) and len(pt) == 2, f"square {k} point")
            assert isinstance(pt, list)
            x, y = scalar(pt[0]), scalar(pt[1])
            zeros += (x[0] == 0) + (y[0] == 0)
            pts.append((x, y))
        squares.append(pts)
    meta = {
        "id": w["id"],
        "claim": w["claim"],
        "source": w.get("source"),
        "certificate": w.get("certificate"),
        "zero_scalars": zeros,
        "scalars_read": 1 + 8 * n,
    }
    return {"n": n, "side": side, "squares": squares, "meta": meta}


def read_pair(yaml_text: str, json_text: str | None) -> dict[str, object]:
    """Read the YAML strictly; require the JSON twin to hold exactly the same tree."""
    tree = _strict_yaml(yaml_text)
    if json_text is None:
        raise ReadRefused("json twin missing")
    twin = _strict_json(json_text)
    if not same_tree(tree, twin):
        raise ReadRefused("json twin differs")
    return interpret(tree)


def read_files(yaml_path: str, json_path: str | None) -> dict[str, object]:
    with open(yaml_path, encoding="utf-8") as fh:
        ytext = fh.read()
    jtext = None
    if json_path is not None:
        with open(json_path, encoding="utf-8") as fh:
            jtext = fh.read()
    return read_pair(ytext, jtext)
