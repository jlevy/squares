"""Lane L159's reader for a Witness/v2 corners certificate and its JSON twin.

Clean-room code written for the stage 4 review of issue #983. It imports nothing from
this repository or from the source, and reuses no code of any earlier review.

The reader decides the first two hypotheses of the review (the reading and the count)
and hands both deciding methods integers: the side as (p, q) and each corner as
((xp, xq), (yp, yq)), every fraction in lowest terms with q >= 1.

It refuses:
- YAML aliases, anchors, explicit tags (the non-specific "!" included), directives,
  duplicate keys, non-string keys, any number of documents but one, and any resolved
  type but string, integer, mapping and sequence, with integers in plain decimal only;
- witness, claim, source, square and envelope keys outside the schema's lists, and any
  layout but representation corners with rational scalars;
- a scalar that is not a canonical p or p/q with q > 1 and gcd(|p|, q) = 1;
- a JSON twin that does not hold exactly the same tree with exactly the same types,
  read with floats, constants, non-canonical integers and duplicate keys refused.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

CANONICAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?")
PLAIN_INT = re.compile(r"-?(?:0|[1-9][0-9]*)")
WITNESS_ID = re.compile(r"W-[a-z0-9][a-z0-9-]*")
STR_TAG = "tag:yaml.org,2002:str"
INT_TAG = "tag:yaml.org,2002:int"

ENVELOPE_KEYS = frozenset({"contract", "schema", "envelope", "status"})
WITNESS_REQUIRED = frozenset(
    {
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
)
WITNESS_OPTIONAL = frozenset({"source", "certificate"})
CLAIM_REQUIRED = frozenset({"coordinate_provenance", "method", "limitations"})
CLAIM_OPTIONAL = frozenset({"precision", "tolerance"})
SOURCE_REQUIRED = frozenset({"path"})
SOURCE_OPTIONAL = frozenset({"key", "url", "retrieved", "revision", "revision_sha256"})
SQUARE_KEYS = frozenset({"id", "corners"})
PROVENANCE = frozenset({"reported", "numerically-checked", "verified"})
METHODS = frozenset(
    {"numerical-f64", "numerical-multiprecision", "interval-certified", "exact-algebraic"}
)

Rational = tuple[int, int]
Point = tuple[Rational, Rational]
Corners = tuple[Point, Point, Point, Point]


class Refused(Exception):
    """The reader refuses the file; the message names the reason."""


@dataclass
class Witness:
    """What the reader hands the deciders, with the facts it read on the way."""

    n: int
    side: Rational
    squares: list[Corners]
    witness_id: str
    claim: dict[str, object]
    source: dict[str, object] | None
    certificate: dict[str, object] | None
    scalars: int
    zero_scalars: int
    tree: dict[str, object] = field(repr=False)


def _check_events(text: str) -> None:
    documents = 0
    for event in yaml.parse(text, Loader=yaml.SafeLoader):
        if isinstance(event, yaml.AliasEvent):
            raise Refused("YAML alias")
        if getattr(event, "anchor", None) is not None:
            raise Refused("YAML anchor")
        if getattr(event, "tag", None) is not None:
            raise Refused("explicit YAML tag")
        if isinstance(event, yaml.DocumentStartEvent):
            documents += 1
            if event.version is not None or event.tags:
                raise Refused("YAML directive")
    if documents != 1:
        raise Refused(f"{documents} YAML documents")


def _value(node: yaml.Node) -> object:
    if isinstance(node, yaml.MappingNode):
        out: dict[str, object] = {}
        for key_node, value_node in node.value:
            if not isinstance(key_node, yaml.ScalarNode) or key_node.tag != STR_TAG:
                raise Refused("non-string mapping key")
            key = key_node.value
            if key in out:
                raise Refused(f"duplicate key {key!r}")
            out[key] = _value(value_node)
        return out
    if isinstance(node, yaml.SequenceNode):
        return [_value(item) for item in node.value]
    if isinstance(node, yaml.ScalarNode):
        if node.tag == STR_TAG:
            return node.value
        if node.tag == INT_TAG:
            if not PLAIN_INT.fullmatch(node.value) or node.value == "-0":
                raise Refused(f"integer not in plain decimal: {node.value!r}")
            return int(node.value)
        raise Refused(f"resolved type {node.tag}")
    raise Refused("unknown node kind")


def parse_yaml(text: str) -> dict[str, object]:
    """Read YAML text strictly into str, int, dict and list."""
    _check_events(text)
    node = yaml.compose(text, Loader=yaml.SafeLoader)
    if node is None:
        raise Refused("empty YAML")
    tree = _value(node)
    if not isinstance(tree, dict):
        raise Refused("top level is not a mapping")
    return tree


def _twin_pairs(items: list[tuple[str, object]]) -> dict[str, object]:
    out: dict[str, object] = {}
    for key, value in items:
        if key in out:
            raise Refused(f"twin duplicate key {key!r}")
        out[key] = value
    return out


def _twin_float(text: str) -> object:
    raise Refused(f"twin float {text!r}")


def _twin_constant(text: str) -> object:
    raise Refused(f"twin constant {text!r}")


def _twin_int(text: str) -> int:
    if not PLAIN_INT.fullmatch(text) or text == "-0":
        raise Refused(f"twin integer not canonical: {text!r}")
    return int(text)


def parse_json(text: str) -> object:
    """Read the JSON twin strictly."""
    return json.loads(
        text,
        object_pairs_hook=_twin_pairs,
        parse_float=_twin_float,
        parse_constant=_twin_constant,
        parse_int=_twin_int,
    )


def _same_tree(a: object, b: object, where: str) -> None:
    if type(a) is not type(b):
        raise Refused(f"twin differs at {where}: {type(a).__name__} vs {type(b).__name__}")
    if isinstance(a, dict):
        assert isinstance(b, dict)
        if set(a) != set(b):
            raise Refused(f"twin differs at {where}: keys")
        for key in a:
            _same_tree(a[key], b[key], f"{where}.{key}")
    elif isinstance(a, list):
        assert isinstance(b, list)
        if len(a) != len(b):
            raise Refused(f"twin differs at {where}: length")
        for index, (x, y) in enumerate(zip(a, b, strict=True)):
            _same_tree(x, y, f"{where}[{index}]")
    elif a != b:
        raise Refused(f"twin differs at {where}")


def scalar(text: object, what: str) -> Rational:
    """A canonical rational scalar, as (p, q) in lowest terms with q >= 1."""
    if type(text) is not str:
        raise Refused(f"{what}: not a string scalar")
    if not CANONICAL.fullmatch(text) or text == "-0" or text.startswith("-0/"):
        raise Refused(f"{what}: not a canonical rational {text[:40]!r}")
    if "/" not in text:
        return int(text), 1
    num_text, den_text = text.split("/")
    p, q = int(num_text), int(den_text)
    if q <= 1:
        raise Refused(f"{what}: denominator not above 1")
    if math.gcd(abs(p), q) != 1:
        raise Refused(f"{what}: not in lowest terms")
    return p, q


def _keys(mapping: object, required: frozenset[str], optional: frozenset[str], what: str) -> dict[str, object]:
    if not isinstance(mapping, dict):
        raise Refused(f"{what}: not a mapping")
    keys = set(mapping)
    if not required <= keys:
        raise Refused(f"{what}: missing {sorted(required - keys)}")
    if not keys <= required | optional:
        raise Refused(f"{what}: unexpected {sorted(keys - required - optional)}")
    return mapping


def interpret(tree: dict[str, object]) -> Witness:
    """Decide the layout and the count, and convert every scalar."""
    _keys(tree, frozenset({"softschema", "witness"}), frozenset(), "top level")
    envelope = _keys(tree["softschema"], ENVELOPE_KEYS, frozenset(), "softschema")
    if envelope["contract"] != "packing.squares:Witness/v2":
        raise Refused("contract is not packing.squares:Witness/v2")
    if envelope["envelope"] != "witness":
        raise Refused("envelope is not witness")
    if not all(type(v) is str for v in envelope.values()):
        raise Refused("softschema: non-string value")
    w = _keys(tree["witness"], WITNESS_REQUIRED, WITNESS_OPTIONAL, "witness")
    witness_id = w["id"]
    if type(witness_id) is not str or not WITNESS_ID.fullmatch(witness_id):
        raise Refused("witness id")
    n = w["n"]
    if type(n) is not int or n < 1:
        raise Refused("n is not a positive integer")
    if w["square_size"] != "1":
        raise Refused("square_size is not '1'")
    if w["representation"] != "corners":
        raise Refused("representation is not corners")
    if w["scalar"] != {"kind": "rational"}:
        raise Refused("scalar is not {kind: rational}")
    if w["coordinates"] != {
        "origin": "lower-left",
        "axes": "x-right-y-up",
        "angle_unit": "not-applicable",
    }:
        raise Refused("coordinates are not lower-left, x-right-y-up, not-applicable")
    side = scalar(w["side"], "side")
    if side[0] <= 0:
        raise Refused("side is not positive")
    raw_squares = w["squares"]
    if not isinstance(raw_squares, list):
        raise Refused("squares is not a sequence")
    if len(raw_squares) != n:
        raise Refused(f"{len(raw_squares)} entries for n = {n}")
    squares: list[Corners] = []
    scalars = 1
    zeros = 0
    for index, entry in enumerate(raw_squares, start=1):
        entry_map = _keys(entry, SQUARE_KEYS, frozenset(), f"square {index}")
        if type(entry_map["id"]) is not int or entry_map["id"] != index:
            raise Refused(f"square {index}: id {entry_map['id']!r}")
        corners = entry_map["corners"]
        if not isinstance(corners, list) or len(corners) != 4:
            raise Refused(f"square {index}: not four corners")
        points: list[Point] = []
        for k, point in enumerate(corners):
            if not isinstance(point, list) or len(point) != 2:
                raise Refused(f"square {index} corner {k}: not a point")
            x = scalar(point[0], f"square {index} corner {k} x")
            y = scalar(point[1], f"square {index} corner {k} y")
            zeros += (x[0] == 0) + (y[0] == 0)
            scalars += 2
            points.append((x, y))
        squares.append((points[0], points[1], points[2], points[3]))
    claim = _keys(w["claim"], CLAIM_REQUIRED, CLAIM_OPTIONAL, "claim")
    if claim["coordinate_provenance"] not in PROVENANCE:
        raise Refused("claim.coordinate_provenance")
    if claim["method"] not in METHODS:
        raise Refused("claim.method")
    source = None
    if "source" in w:
        source = _keys(w["source"], SOURCE_REQUIRED, SOURCE_OPTIONAL, "source")
    certificate = None
    if "certificate" in w:
        certificate = w["certificate"]
        if not isinstance(certificate, dict):
            raise Refused("certificate is not a mapping")
    return Witness(
        n=n,
        side=side,
        squares=squares,
        witness_id=witness_id,
        claim=claim,
        source=source,
        certificate=certificate,
        scalars=scalars,
        zero_scalars=zeros,
        tree=tree,
    )


def read_texts(yaml_text: str, json_text: str) -> Witness:
    """Read the certificate and its twin from text, refusing anything unexpected."""
    tree = parse_yaml(yaml_text)
    twin = parse_json(json_text)
    _same_tree(tree, twin, "$")
    return interpret(tree)


def read_paths(yaml_path: Path, json_path: Path) -> Witness:
    """Read the certificate and its twin from files."""
    return read_texts(
        yaml_path.read_text(encoding="utf-8"), json_path.read_text(encoding="utf-8")
    )
