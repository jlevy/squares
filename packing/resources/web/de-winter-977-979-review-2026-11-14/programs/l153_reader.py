"""Lane L153 reader for the center-basis certificates of issues #977 and #979.

Clean-room: written for this review, importing nothing from this repository or the
source, and reusing no code of any earlier review.

It reads the author's JSON format

    {"n": N, "side": "p/q", "square_size": "1", "format": "...",
     "squares": [[center_x, center_y, cos, sin], ...]}

and, where one is given, the Witness/v2 YAML twin (representation center-basis,
scalar kind rational, origin lower-left, axes x-right-y-up), and hands the two methods
integers only: for every square four reduced pairs (p, q) with q >= 1.

It refuses: anything that is not strict UTF-8; JSON floats, constants, duplicate keys
and keys outside the expected set; a count that differs from n; any scalar that is not
a canonical rational, that is `p` or `p/q` with q > 1, gcd(|p|, q) = 1 and no sign on
zero; YAML anchors, aliases, explicit tags, duplicate keys, several documents, resolved
types other than string, integer, mapping and sequence, integers outside plain decimal
form, witness and square keys outside the schema's lists, and a twin that does not hold
exactly the same n, side and squares as the JSON file.
"""

from __future__ import annotations

import json
import math
import re
import sys

import yaml

sys.set_int_max_str_digits(0)

Pair = tuple[int, int]
Square = tuple[Pair, Pair, Pair, Pair]

_RATIONAL = re.compile(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?")
_DECIMAL_INT = re.compile(r"-?(0|[1-9][0-9]*)")

JSON_KEYS = frozenset({"n", "side", "square_size", "format", "squares"})
SOFTSCHEMA_KEYS = frozenset({"contract", "schema", "envelope", "status"})
WITNESS_KEYS = frozenset(
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
        "source",
        "certificate",
    }
)
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
CLAIM_KEYS = frozenset(
    {"coordinate_provenance", "method", "precision", "tolerance", "limitations"}
)
CLAIM_REQUIRED = frozenset({"coordinate_provenance", "method", "limitations"})
SQUARE_KEYS = frozenset({"id", "center", "basis"})


class ReadError(Exception):
    """The file is refused; the message says why."""


def rational(text: object, where: str) -> Pair:
    """A canonical rational string as a reduced pair (p, q), q >= 1."""
    if type(text) is not str:
        raise ReadError(f"{where}: not a string scalar")
    if _RATIONAL.fullmatch(text) is None:
        raise ReadError(f"{where}: not a canonical rational: {text[:40]!r}")
    if text == "-0" or text.startswith("-0/"):
        raise ReadError(f"{where}: signed zero")
    if "/" in text:
        p_text, q_text = text.split("/")
        p, q = int(p_text), int(q_text)
        if q == 1:
            raise ReadError(f"{where}: denominator 1 written out")
        if math.gcd(abs(p), q) != 1:
            raise ReadError(f"{where}: not in lowest terms")
        return p, q
    return int(text), 1


def _strict_text(path: str) -> str:
    with open(path, "rb") as handle:
        data = handle.read()
    try:
        return data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise ReadError(f"{path}: not UTF-8") from error


def _no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    out: dict[str, object] = {}
    for key, value in pairs:
        if key in out:
            raise ReadError(f"duplicate JSON key {key!r}")
        out[key] = value
    return out


def _refuse_float(text: str) -> object:
    raise ReadError(f"JSON float {text!r}")


def _refuse_constant(text: str) -> object:
    raise ReadError(f"JSON constant {text!r}")


def parse_json_text(text: str) -> tuple[int, Pair, list[Square], str]:
    """The JSON certificate from its text: n, side, squares, the format string."""
    try:
        tree = json.loads(
            text,
            object_pairs_hook=_no_duplicates,
            parse_float=_refuse_float,
            parse_constant=_refuse_constant,
        )
    except json.JSONDecodeError as error:
        raise ReadError(f"JSON does not parse: {error}") from error
    if type(tree) is not dict:
        raise ReadError("top level is not an object")
    keys = frozenset(tree)
    if keys != JSON_KEYS:
        raise ReadError(f"top-level keys {sorted(keys)} != {sorted(JSON_KEYS)}")
    n = tree["n"]
    if type(n) is not int or n < 1:
        raise ReadError("n is not a positive integer")
    side = rational(tree["side"], "side")
    if side[0] <= 0:
        raise ReadError("side is not positive")
    if tree["square_size"] != "1":
        raise ReadError("square_size is not '1'")
    fmt = tree["format"]
    if type(fmt) is not str:
        raise ReadError("format is not a string")
    rows = tree["squares"]
    if type(rows) is not list:
        raise ReadError("squares is not a list")
    if len(rows) != n:
        raise ReadError(f"{len(rows)} squares listed, n = {n}")
    squares: list[Square] = []
    for k, row in enumerate(rows, start=1):
        if type(row) is not list or len(row) != 4:
            raise ReadError(f"square {k}: not a list of four scalars")
        squares.append(
            (
                rational(row[0], f"square {k} center_x"),
                rational(row[1], f"square {k} center_y"),
                rational(row[2], f"square {k} cos"),
                rational(row[3], f"square {k} sin"),
            )
        )
    return n, side, squares, fmt


def _check_events(text: str) -> None:
    documents = 0
    for event in yaml.parse(text, Loader=yaml.SafeLoader):
        if isinstance(event, yaml.AliasEvent):
            raise ReadError("YAML alias")
        if isinstance(event, yaml.DocumentStartEvent):
            documents += 1
            if documents > 1:
                raise ReadError("several YAML documents")
        anchor = getattr(event, "anchor", None)
        if anchor is not None:
            raise ReadError("YAML anchor")
        if isinstance(event, (yaml.ScalarEvent, yaml.SequenceStartEvent, yaml.MappingStartEvent)):
            if event.tag is not None:
                raise ReadError(f"explicit YAML tag {event.tag!r}")
    if documents != 1:
        raise ReadError("not exactly one YAML document")


def _plain(node: yaml.Node) -> object:
    if isinstance(node, yaml.MappingNode):
        if node.tag != "tag:yaml.org,2002:map":
            raise ReadError(f"mapping tag {node.tag}")
        out: dict[str, object] = {}
        for key_node, value_node in node.value:
            key = _plain(key_node)
            if type(key) is not str:
                raise ReadError("non-string mapping key")
            if key in out:
                raise ReadError(f"duplicate YAML key {key!r}")
            out[key] = _plain(value_node)
        return out
    if isinstance(node, yaml.SequenceNode):
        if node.tag != "tag:yaml.org,2002:seq":
            raise ReadError(f"sequence tag {node.tag}")
        return [_plain(item) for item in node.value]
    if isinstance(node, yaml.ScalarNode):
        if node.tag == "tag:yaml.org,2002:str":
            return node.value
        if node.tag == "tag:yaml.org,2002:int":
            if _DECIMAL_INT.fullmatch(node.value) is None:
                raise ReadError(f"integer not in plain decimal form: {node.value!r}")
            return int(node.value)
        raise ReadError(f"scalar of type {node.tag}")
    raise ReadError("unknown YAML node")


def parse_yaml_text(text: str) -> tuple[int, Pair, list[Square], dict[str, object]]:
    """The Witness/v2 twin from its text: n, side, squares, and the witness header."""
    _check_events(text)
    root = yaml.compose(text, Loader=yaml.SafeLoader)
    if root is None:
        raise ReadError("empty YAML")
    tree = _plain(root)
    if type(tree) is not dict or frozenset(tree) != {"softschema", "witness"}:
        raise ReadError("top level is not {softschema, witness}")
    envelope = tree["softschema"]
    if type(envelope) is not dict or not frozenset(envelope) <= SOFTSCHEMA_KEYS:
        raise ReadError("softschema keys")
    if envelope.get("contract") != "packing.squares:Witness/v2":
        raise ReadError("contract is not packing.squares:Witness/v2")
    if envelope.get("envelope") != "witness":
        raise ReadError("envelope is not witness")
    witness = tree["witness"]
    if type(witness) is not dict:
        raise ReadError("witness is not a mapping")
    keys = frozenset(witness)
    if not keys <= WITNESS_KEYS:
        raise ReadError(f"witness keys outside the schema: {sorted(keys - WITNESS_KEYS)}")
    if not WITNESS_REQUIRED <= keys:
        raise ReadError(f"witness keys missing: {sorted(WITNESS_REQUIRED - keys)}")
    if witness["representation"] != "center-basis":
        raise ReadError("representation is not center-basis")
    if witness["scalar"] != {"kind": "rational"}:
        raise ReadError("scalar is not {kind: rational}")
    if witness["coordinates"] != {
        "origin": "lower-left",
        "axes": "x-right-y-up",
        "angle_unit": "not-applicable",
    }:
        raise ReadError("coordinates are not lower-left, x-right-y-up, not-applicable")
    if witness["square_size"] != "1":
        raise ReadError("square_size is not '1'")
    claim = witness["claim"]
    if type(claim) is not dict:
        raise ReadError("claim is not a mapping")
    claim_keys = frozenset(claim)
    if not claim_keys <= CLAIM_KEYS or not CLAIM_REQUIRED <= claim_keys:
        raise ReadError("claim keys")
    n = witness["n"]
    if type(n) is not int or n < 1:
        raise ReadError("n is not a positive integer")
    side = rational(witness["side"], "side")
    if side[0] <= 0:
        raise ReadError("side is not positive")
    rows = witness["squares"]
    if type(rows) is not list or len(rows) != n:
        raise ReadError("squares is not a list of n entries")
    squares: list[Square] = []
    for k, row in enumerate(rows, start=1):
        if type(row) is not dict or frozenset(row) != SQUARE_KEYS:
            raise ReadError(f"square {k}: keys are not {{id, center, basis}}")
        if type(row["id"]) is not int or row["id"] != k:
            raise ReadError(f"square {k}: id {row['id']!r}")
        center, basis = row["center"], row["basis"]
        if type(center) is not list or len(center) != 2:
            raise ReadError(f"square {k}: center is not a point")
        if type(basis) is not list or len(basis) != 2:
            raise ReadError(f"square {k}: basis is not a point")
        squares.append(
            (
                rational(center[0], f"square {k} center x"),
                rational(center[1], f"square {k} center y"),
                rational(basis[0], f"square {k} basis cos"),
                rational(basis[1], f"square {k} basis sin"),
            )
        )
    header = {k: witness[k] for k in sorted(keys) if k != "squares"}
    return n, side, squares, header


def read(json_path: str, yaml_path: str | None = None) -> dict[str, object]:
    """Read a certificate and, if given, its YAML twin, which must hold the same packing."""
    n, side, squares, fmt = parse_json_text(_strict_text(json_path))
    out: dict[str, object] = {"n": n, "side": side, "squares": squares, "format": fmt}
    if yaml_path is not None:
        yn, yside, ysquares, header = parse_yaml_text(_strict_text(yaml_path))
        if yn != n:
            raise ReadError("the twin's n differs")
        if yside != side:
            raise ReadError("the twin's side differs")
        if ysquares != squares:
            first = next(k for k in range(n) if ysquares[k] != squares[k]) + 1
            raise ReadError(f"the twin differs, first at square {first}")
        out["twin_header"] = header
    return out
