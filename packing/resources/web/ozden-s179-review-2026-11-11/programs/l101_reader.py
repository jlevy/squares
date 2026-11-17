"""Strict reader for a corners / rational Witness/v2 file and its JSON twin.

Lane L101's clean-room reader. It decides the reading hypotheses only: the layout,
the count, the ids, canonical p/q scalars, and that the JSON twin holds exactly the
same tree. It hands integers to the two methods and decides no geometry.

It imports nothing from this repository or from the source repository. PyYAML is used
to compose the YAML into nodes only; every node's tag is checked here, aliases and
duplicate keys are refused, and a scalar is read from its source text.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

STR = "tag:yaml.org,2002:str"
INT = "tag:yaml.org,2002:int"
MAP = "tag:yaml.org,2002:map"
SEQ = "tag:yaml.org,2002:seq"

RATIONAL = re.compile(r"(0|-?[1-9][0-9]*)(?:/([1-9][0-9]*))?")
DECIMAL_INT = re.compile(r"0|[1-9][0-9]*")

WITNESS_REQUIRED = {
    "id", "n", "side", "square_size", "representation", "scalar", "coordinates",
    "squares", "claim",
}
WITNESS_OPTIONAL = {"source", "certificate"}


class ReadError(Exception):
    """The file is not read: the reason is the message."""


Rat = tuple[int, int]
Point = tuple[Rat, Rat]


@dataclass
class Witness:
    n: int
    side: Rat
    squares: list[list[Point]]
    ids: list[int]
    meta: dict = field(default_factory=dict)
    scalar_count: int = 0


def _refuse(message: str) -> None:
    raise ReadError(message)


def _plain(node: yaml.Node, path: str) -> object:
    """A composed node as dict / list / str / int, refusing every other tag."""
    if isinstance(node, yaml.MappingNode):
        if node.tag != MAP:
            _refuse(f"{path}: mapping tag {node.tag}")
        out: dict[str, object] = {}
        for key, value in node.value:
            if not isinstance(key, yaml.ScalarNode) or key.tag != STR:
                _refuse(f"{path}: a key that is not a plain string")
            if key.value in out:
                _refuse(f"{path}: duplicate key {key.value!r}")
            out[key.value] = _plain(value, f"{path}.{key.value}")
        return out
    if isinstance(node, yaml.SequenceNode):
        if node.tag != SEQ:
            _refuse(f"{path}: sequence tag {node.tag}")
        return [_plain(item, f"{path}[{index}]") for index, item in enumerate(node.value)]
    if isinstance(node, yaml.ScalarNode):
        if node.tag == STR:
            return node.value
        if node.tag == INT:
            if not DECIMAL_INT.fullmatch(node.value):
                _refuse(f"{path}: integer written as {node.value!r}")
            return int(node.value)
        _refuse(f"{path}: scalar tag {node.tag}")
    _refuse(f"{path}: node of kind {type(node).__name__}")
    return None


def _yaml_tree(text: str) -> object:
    for event in yaml.parse(text, Loader=yaml.SafeLoader):
        if isinstance(event, yaml.AliasEvent):
            _refuse("YAML alias")
        if isinstance(event, (yaml.ScalarEvent, yaml.MappingStartEvent, yaml.SequenceStartEvent)):
            if event.anchor is not None:
                _refuse("YAML anchor")
    try:
        node = yaml.compose(text, Loader=yaml.SafeLoader)
    except yaml.YAMLError as error:
        raise ReadError(f"YAML: {error}") from error
    if node is None:
        _refuse("empty YAML")
    return _plain(node, "$")


def _json_tree(text: str) -> object:
    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        out: dict[str, object] = {}
        for key, value in items:
            if key in out:
                _refuse(f"JSON duplicate key {key!r}")
            out[key] = value
        return out

    def no_float(token: str) -> object:
        _refuse(f"JSON float {token}")
        return None

    def no_constant(token: str) -> object:
        _refuse(f"JSON constant {token}")
        return None

    try:
        return json.loads(
            text, object_pairs_hook=pairs, parse_float=no_float, parse_constant=no_constant
        )
    except json.JSONDecodeError as error:
        raise ReadError(f"JSON: {error}") from error


def same_tree(a: object, b: object) -> bool:
    """Exact equality with exact types: bool is not int, int is not str."""
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        assert isinstance(b, dict)
        return list(a) == list(b) and all(same_tree(a[k], b[k]) for k in a)
    if isinstance(a, list):
        assert isinstance(b, list)
        return len(a) == len(b) and all(same_tree(x, y) for x, y in zip(a, b, strict=True))
    return a == b


def rational(value: object, path: str) -> Rat:
    """A canonical p/q string: q > 1 when written, gcd(p, q) = 1, no sign on 0."""
    if not isinstance(value, str):
        _refuse(f"{path}: scalar is {type(value).__name__}, not a string")
    assert isinstance(value, str)
    match = RATIONAL.fullmatch(value)
    if match is None:
        _refuse(f"{path}: {value[:40]!r} is not p or p/q")
    assert match is not None
    p = int(match[1])
    if match[2] is None:
        return (p, 1)
    q = int(match[2])
    if q == 1:
        _refuse(f"{path}: denominator 1 written")
    if math.gcd(p, q) != 1:
        _refuse(f"{path}: not in lowest terms")
    return (p, q)


def _exact(value: object, expected: object, path: str) -> None:
    if not same_tree(value, expected):
        _refuse(f"{path}: {value!r} is not {expected!r}")


def _decode(tree: object, n_expected: int) -> Witness:
    if not isinstance(tree, dict) or set(tree) != {"softschema", "witness"}:
        _refuse("top level is not exactly softschema and witness")
    assert isinstance(tree, dict)
    soft = tree["softschema"]
    if not isinstance(soft, dict) or set(soft) != {"contract", "schema", "envelope", "status"}:
        _refuse("softschema keys")
    assert isinstance(soft, dict)
    _exact(soft["contract"], "packing.squares:Witness/v2", "softschema.contract")
    _exact(soft["envelope"], "witness", "softschema.envelope")
    w = tree["witness"]
    if not isinstance(w, dict):
        _refuse("witness is not a mapping")
    assert isinstance(w, dict)
    keys = set(w)
    if not WITNESS_REQUIRED <= keys or not keys <= WITNESS_REQUIRED | WITNESS_OPTIONAL:
        _refuse(f"witness keys {sorted(keys)}")
    _exact(w["n"], n_expected, "witness.n")
    _exact(w["square_size"], "1", "witness.square_size")
    _exact(w["representation"], "corners", "witness.representation")
    _exact(w["scalar"], {"kind": "rational"}, "witness.scalar")
    _exact(
        w["coordinates"],
        {"origin": "lower-left", "axes": "x-right-y-up", "angle_unit": "not-applicable"},
        "witness.coordinates",
    )
    side = rational(w["side"], "witness.side")
    if side[0] <= 0:
        _refuse("witness.side is not positive")
    squares_raw = w["squares"]
    if not isinstance(squares_raw, list) or len(squares_raw) != n_expected:
        count = len(squares_raw) if isinstance(squares_raw, list) else "no"
        _refuse(f"witness.squares holds {count} entries, not {n_expected}")
    assert isinstance(squares_raw, list)
    squares: list[list[Point]] = []
    ids: list[int] = []
    scalars = 1
    for index, entry in enumerate(squares_raw):
        path = f"squares[{index}]"
        if not isinstance(entry, dict) or set(entry) != {"id", "corners"}:
            _refuse(f"{path}: keys are not exactly id and corners")
        assert isinstance(entry, dict)
        if type(entry["id"]) is not int or entry["id"] != index + 1:
            _refuse(f"{path}: id {entry['id']!r} is not {index + 1}")
        ids.append(entry["id"])
        corners = entry["corners"]
        if not isinstance(corners, list) or len(corners) != 4:
            _refuse(f"{path}: corners is not a list of four")
        assert isinstance(corners, list)
        square: list[Point] = []
        for k, point in enumerate(corners):
            if not isinstance(point, list) or len(point) != 2:
                _refuse(f"{path}.corners[{k}]: not a pair")
            assert isinstance(point, list)
            x = rational(point[0], f"{path}.corners[{k}][0]")
            y = rational(point[1], f"{path}.corners[{k}][1]")
            square.append((x, y))
            scalars += 2
        squares.append(square)
    meta = {
        "witness_id": w["id"],
        "softschema_schema": soft["schema"],
        "softschema_status": soft["status"],
        "claim": w["claim"],
        "source": w.get("source"),
        "certificate": w.get("certificate"),
    }
    return Witness(n=n_expected, side=side, squares=squares, ids=ids, meta=meta,
                   scalar_count=scalars)


def read_texts(yaml_text: str, json_text: str | None, n_expected: int) -> Witness:
    tree = _yaml_tree(yaml_text)
    if json_text is not None:
        twin = _json_tree(json_text)
        if not same_tree(tree, twin):
            _refuse("JSON twin does not hold the same tree as the YAML")
    return _decode(tree, n_expected)


def read_files(yaml_path: Path, json_path: Path | None, n_expected: int) -> Witness:
    yaml_text = yaml_path.read_text(encoding="utf-8")
    json_text = json_path.read_text(encoding="utf-8") if json_path is not None else None
    return read_texts(yaml_text, json_text, n_expected)
