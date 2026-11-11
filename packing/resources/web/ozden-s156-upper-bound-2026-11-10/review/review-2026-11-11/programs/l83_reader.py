"""Strict reader for Witness/v2 corner certificates, written clean room for review L83.

It composes the YAML with PyYAML (no construction of Python objects), turns every
scalar into an exact (numerator, denominator) pair of integers, and fails closed on
any layout it does not expect. The JSON twin, read with the standard library, must
hold exactly the same tree. Nothing here decides geometry.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from math import gcd
from pathlib import Path
from typing import Any

import yaml

CONTRACT = "packing.squares:Witness/v2"
_SCALAR = re.compile(r"(-?)(0|[1-9][0-9]*)(?:/([1-9][0-9]*))?\Z")
_INT = re.compile(r"(0|[1-9][0-9]*)\Z")
_REQUIRED = ("id", "n", "side", "square_size", "representation", "scalar", "coordinates", "squares")
_OPTIONAL = ("claim", "source", "certificate")


class Refused(Exception):
    """The reader will not read this file."""


@dataclass
class Witness:
    n: int
    side: tuple[int, int]
    ids: list[int]
    corners: list[list[tuple[tuple[int, int], tuple[int, int]]]]
    ids_in_order: bool
    meta: dict[str, Any] = field(default_factory=dict)
    scalar_count: int = 0


def parse_scalar(text: object) -> tuple[int, int]:
    """Canonical integer or p/q with q > 1, gcd 1, no sign on zero."""
    if not isinstance(text, str):
        raise Refused(f"scalar is not a string: {text!r}")
    m = _SCALAR.match(text)
    if m is None:
        raise Refused(f"scalar not canonical: {text[:48]!r}")
    sign, p_text, q_text = m.groups()
    p = int(p_text)
    if sign and p == 0:
        raise Refused("negative zero")
    if q_text is None:
        return (-p if sign else p, 1)
    q = int(q_text)
    if q == 1:
        raise Refused("denominator 1")
    if p == 0:
        raise Refused("zero over a denominator")
    if gcd(p, q) != 1:
        raise Refused("not in lowest terms")
    return (-p if sign else p, q)


def _int(value: object, what: str) -> int:
    if isinstance(value, int) and not isinstance(value, bool):
        value = str(value)
    if not isinstance(value, str) or _INT.match(value) is None:
        raise Refused(f"{what} is not a canonical non-negative integer: {value!r}")
    return int(value)


def _plain(node: yaml.Node) -> Any:
    if not node.tag.startswith("tag:yaml.org,2002:"):
        raise Refused(f"non-standard tag {node.tag}")
    if isinstance(node, yaml.MappingNode):
        out: dict[str, Any] = {}
        for key, value in node.value:
            if not isinstance(key, yaml.ScalarNode):
                raise Refused("non-scalar key")
            if key.value in out:
                raise Refused(f"duplicate key {key.value!r}")
            out[key.value] = _plain(value)
        return out
    if isinstance(node, yaml.SequenceNode):
        return [_plain(v) for v in node.value]
    if isinstance(node, yaml.ScalarNode):
        return node.value
    raise Refused("unknown node kind")


def compose_yaml(text: str) -> Any:
    try:
        node = yaml.compose(text, Loader=yaml.SafeLoader)
    except yaml.YAMLError as exc:
        raise Refused(f"YAML does not compose: {type(exc).__name__}") from exc
    if node is None:
        raise Refused("empty document")
    return _plain(node)


def normalise_json(value: Any) -> Any:
    """JSON numbers become their decimal text, so the tree compares with composed YAML."""
    if isinstance(value, bool) or value is None or isinstance(value, float):
        raise Refused(f"JSON value of a kind the format does not use: {value!r}")
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return [normalise_json(v) for v in value]
    if isinstance(value, dict):
        return {k: normalise_json(v) for k, v in value.items()}
    raise Refused("unknown JSON value")


def witness_from_tree(tree: Any) -> Witness:
    if not isinstance(tree, dict) or set(tree) != {"softschema", "witness"}:
        raise Refused("top level is not exactly softschema and witness")
    ss = tree["softschema"]
    if not isinstance(ss, dict) or ss.get("contract") != CONTRACT or ss.get("envelope") != "witness":
        raise Refused("softschema contract or envelope")
    w = tree["witness"]
    if not isinstance(w, dict):
        raise Refused("witness is not a mapping")
    missing = [k for k in _REQUIRED if k not in w]
    extra = [k for k in w if k not in _REQUIRED and k not in _OPTIONAL]
    if missing or extra:
        raise Refused(f"witness keys: missing {missing}, unexpected {extra}")
    n = _int(w["n"], "n")
    side = parse_scalar(w["side"])
    if side[0] <= 0:
        raise Refused("side not positive")
    if w["square_size"] != "1":
        raise Refused("square_size is not '1'")
    if w["representation"] != "corners":
        raise Refused("representation is not corners")
    if w["scalar"] != {"kind": "rational"}:
        raise Refused("scalar is not exactly {kind: rational}")
    if w["coordinates"] != {"origin": "lower-left", "axes": "x-right-y-up", "angle_unit": "not-applicable"}:
        raise Refused("coordinates are not lower-left, x-right-y-up, not-applicable")
    squares = w["squares"]
    if not isinstance(squares, list) or len(squares) != n:
        raise Refused(f"squares is not a list of n = {n}")
    ids: list[int] = []
    corners: list[list[tuple[tuple[int, int], tuple[int, int]]]] = []
    count = 1
    for sq in squares:
        if not isinstance(sq, dict) or set(sq) != {"id", "corners"}:
            raise Refused("square entry is not exactly id and corners")
        sid = _int(sq["id"], "id")
        if sid < 1:
            raise Refused("id below 1")
        cs = sq["corners"]
        if not isinstance(cs, list) or len(cs) != 4:
            raise Refused(f"square {sid}: not four corners")
        pts = []
        for c in cs:
            if not isinstance(c, list) or len(c) != 2:
                raise Refused(f"square {sid}: corner is not a pair")
            pts.append((parse_scalar(c[0]), parse_scalar(c[1])))
            count += 2
        ids.append(sid)
        corners.append(pts)
    if len(set(ids)) != n:
        raise Refused("repeated id")
    if set(ids) != set(range(1, n + 1)):
        raise Refused("ids are not 1 to n")
    meta = {k: w[k] for k in _OPTIONAL if k in w}
    meta["id"] = w["id"]
    return Witness(n, side, ids, corners, ids == list(range(1, n + 1)), meta, count)


@dataclass
class Read:
    witness: Witness
    yaml_sha256: str
    yaml_bytes: int
    yaml_ends_newline: bool
    json_sha256: str | None = None
    json_equal: bool | None = None
    json_ends_newline: bool | None = None


def read_text(text: str) -> Witness:
    return witness_from_tree(compose_yaml(text))


def read_files(yaml_path: Path, json_path: Path | None = None) -> Read:
    raw = yaml_path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Refused("YAML is not UTF-8") from exc
    tree = compose_yaml(text)
    wit = witness_from_tree(tree)
    out = Read(wit, hashlib.sha256(raw).hexdigest(), len(raw), raw.endswith(b"\n"))
    if json_path is not None:
        jraw = json_path.read_bytes()
        jtree = normalise_json(json.loads(jraw.decode("utf-8")))
        out.json_sha256 = hashlib.sha256(jraw).hexdigest()
        out.json_ends_newline = jraw.endswith(b"\n")
        out.json_equal = jtree == tree
        if not out.json_equal:
            raise Refused("JSON twin does not hold the same witness tree")
    return out
