"""Lane r1038's reader: a Witness/v2 certificate in center-basis form, to exact rationals.

It decides the reading and nothing else, and hands both methods of this review the side
and, for each square, its centre and its basis as `fractions.Fraction` values. The two
methods share this module and nothing else. It imports nothing from this repository or
from the source, and it was written for this review.

What it accepts, and refuses everything else (fail closed):

- UTF-8 text with no byte-order mark, no tab and no carriage return;
- one YAML document with no anchor, alias, explicit tag or directive;
- only strings, plain decimal integers, mappings and sequences, with string keys and no
  duplicate key;
- the softschema envelope (`contract: packing.squares:Witness/v2`, `envelope: witness`);
- witness keys inside the schema's list with every required key present, the witness id
  in the schema's pattern, `square_size: '1'`, `representation: center-basis`,
  `scalar: {kind: rational}`, `origin: lower-left`, `axes: x-right-y-up`;
- `n` squares listed with ids 1 to `n` in order, each with exactly `id`, `center` and
  `basis`, each of the last two a list of two scalars;
- every scalar a YAML string `p` or `p/q`: an optional minus, no plus, no leading zero,
  `q >= 1`. Lowest terms are recorded, not required.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

import yaml

SCALAR_FORM = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?")
PLAIN_INT = re.compile(r"0|[1-9][0-9]*")
WITNESS_ID = re.compile(r"W-[a-z0-9][a-z0-9-]*")
STR_TAG = "tag:yaml.org,2002:str"
INT_TAG = "tag:yaml.org,2002:int"

ENVELOPE_KEYS = frozenset({"contract", "schema", "envelope", "status"})
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
ANGLE_UNITS = frozenset({"degrees", "radians", "not-applicable"})


class ReadRefused(Exception):
    """The text is not a certificate this reader accepts; the message says why."""


@dataclass(frozen=True)
class Certificate:
    """What the reader hands on: exact values, the scalars as written, and notes."""

    n: int
    side: Fraction
    side_text: str
    centers: list[tuple[Fraction, Fraction]]
    bases: list[tuple[Fraction, Fraction]]
    texts: list[tuple[str, str, str, str]]
    noncanonical: list[str]
    header: dict[str, Any]


def scalar_value(text: object, where: str) -> tuple[Fraction, bool]:
    """Read one scalar: its exact value, and whether it is written canonically."""
    if not isinstance(text, str):
        raise ReadRefused(f"{where}: a scalar that is not a YAML string")
    if not SCALAR_FORM.fullmatch(text):
        raise ReadRefused(f"{where}: {text!r} is not p or p/q")
    numerator_text, _, denominator_text = text.partition("/")
    value = Fraction(int(numerator_text), int(denominator_text) if denominator_text else 1)
    if value.denominator == 1:
        canonical = str(value.numerator)
    else:
        canonical = f"{value.numerator}/{value.denominator}"
    return value, text == canonical


def _check_events(text: str) -> None:
    documents = 0
    for event in yaml.parse(text, Loader=yaml.SafeLoader):
        if isinstance(event, yaml.DocumentStartEvent):
            documents += 1
            if event.version is not None or event.tags:
                raise ReadRefused("a YAML directive")
        elif isinstance(event, yaml.AliasEvent):
            raise ReadRefused("an alias")
        elif isinstance(
            event, (yaml.ScalarEvent, yaml.SequenceStartEvent, yaml.MappingStartEvent)
        ):
            if event.anchor is not None:
                raise ReadRefused("an anchor")
            if event.tag is not None:
                raise ReadRefused("an explicit tag")
    if documents != 1:
        raise ReadRefused(f"{documents} YAML documents, not one")


def _plain(node: yaml.Node, path: str) -> Any:
    if isinstance(node, yaml.MappingNode):
        result: dict[str, Any] = {}
        for key_node, value_node in node.value:
            if not isinstance(key_node, yaml.ScalarNode) or key_node.tag != STR_TAG:
                raise ReadRefused(f"{path}: a mapping key that is not a string")
            key = key_node.value
            if key in result:
                raise ReadRefused(f"{path}: the key {key!r} twice")
            result[key] = _plain(value_node, f"{path}.{key}")
        return result
    if isinstance(node, yaml.SequenceNode):
        return [_plain(item, f"{path}[{index}]") for index, item in enumerate(node.value)]
    if isinstance(node, yaml.ScalarNode):
        if node.tag == STR_TAG:
            return str(node.value)
        if node.tag == INT_TAG and node.style is None and PLAIN_INT.fullmatch(node.value):
            return int(node.value)
        raise ReadRefused(f"{path}: a scalar of type {node.tag} ({node.value!r})")
    raise ReadRefused(f"{path}: an unrecognised node")


def _mapping(value: Any, where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ReadRefused(f"{where}: not a mapping")
    return value


def _pair(value: Any, where: str) -> list[Any]:
    if not isinstance(value, list) or len(value) != 2:
        raise ReadRefused(f"{where}: not a list of two scalars")
    return value


def read_text(text: str) -> Certificate:
    """Read a certificate's text, or refuse it with the reason."""
    if text.startswith("﻿"):
        raise ReadRefused("a byte-order mark")
    if "\t" in text:
        raise ReadRefused("a tab")
    if "\r" in text:
        raise ReadRefused("a carriage return")
    _check_events(text)
    root_node = yaml.compose(text, Loader=yaml.SafeLoader)
    if root_node is None:
        raise ReadRefused("an empty document")
    root = _mapping(_plain(root_node, "$"), "$")
    if set(root) != {"softschema", "witness"}:
        raise ReadRefused(f"top-level keys {sorted(root)}, not softschema and witness")
    envelope = _mapping(root["softschema"], "softschema")
    if not set(envelope) <= ENVELOPE_KEYS:
        raise ReadRefused(f"softschema keys {sorted(set(envelope) - ENVELOPE_KEYS)}")
    if envelope.get("contract") != "packing.squares:Witness/v2":
        raise ReadRefused(f"contract {envelope.get('contract')!r}")
    if envelope.get("envelope") != "witness":
        raise ReadRefused(f"envelope {envelope.get('envelope')!r}")

    witness = _mapping(root["witness"], "witness")
    extra = set(witness) - WITNESS_KEYS
    missing = WITNESS_REQUIRED - set(witness)
    if extra or missing:
        raise ReadRefused(f"witness keys: extra {sorted(extra)}, missing {sorted(missing)}")
    witness_id = witness["id"]
    if not isinstance(witness_id, str) or not WITNESS_ID.fullmatch(witness_id):
        raise ReadRefused(f"witness id {witness_id!r}")
    if witness["square_size"] != "1":
        raise ReadRefused(f"square_size {witness['square_size']!r}, not the string '1'")
    if witness["representation"] != "center-basis":
        raise ReadRefused(f"representation {witness['representation']!r}, not center-basis")
    if witness["scalar"] != {"kind": "rational"}:
        raise ReadRefused(f"scalar {witness['scalar']!r}, not exactly kind rational")
    coordinates = _mapping(witness["coordinates"], "coordinates")
    if set(coordinates) != {"origin", "axes", "angle_unit"}:
        raise ReadRefused(f"coordinates keys {sorted(coordinates)}")
    if coordinates["origin"] != "lower-left":
        raise ReadRefused(f"origin {coordinates['origin']!r}, not lower-left")
    if coordinates["axes"] != "x-right-y-up":
        raise ReadRefused(f"axes {coordinates['axes']!r}")
    if coordinates["angle_unit"] not in ANGLE_UNITS:
        raise ReadRefused(f"angle_unit {coordinates['angle_unit']!r}")
    claim = _mapping(witness["claim"], "claim")

    n = witness["n"]
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ReadRefused(f"n {n!r}")
    noncanonical: list[str] = []
    side_text = witness["side"]
    side, side_canonical = scalar_value(side_text, "side")
    if not side_canonical:
        noncanonical.append("side")
    if side <= 0:
        raise ReadRefused("a side that is not positive")

    squares = witness["squares"]
    if not isinstance(squares, list):
        raise ReadRefused("squares: not a list")
    if len(squares) != n:
        raise ReadRefused(f"n is {n} but {len(squares)} squares are listed")
    centers: list[tuple[Fraction, Fraction]] = []
    bases: list[tuple[Fraction, Fraction]] = []
    texts: list[tuple[str, str, str, str]] = []
    for index, raw in enumerate(squares, start=1):
        square = _mapping(raw, f"squares[{index - 1}]")
        if set(square) != {"id", "center", "basis"}:
            raise ReadRefused(f"square {index}: keys {sorted(square)}")
        square_id = square["id"]
        if not isinstance(square_id, int) or isinstance(square_id, bool) or square_id != index:
            raise ReadRefused(f"square {index}: id {square_id!r} out of order")
        values: list[Fraction] = []
        written: list[str] = []
        for key in ("center", "basis"):
            for axis, text_value in zip("xy", _pair(square[key], f"square {index}.{key}")):
                where = f"square {index}.{key}.{axis}"
                value, canonical = scalar_value(text_value, where)
                if not canonical:
                    noncanonical.append(where)
                values.append(value)
                written.append(text_value)
        centers.append((values[0], values[1]))
        bases.append((values[2], values[3]))
        texts.append((written[0], written[1], written[2], written[3]))

    header = {
        "witness_id": witness_id,
        "envelope": {key: envelope[key] for key in sorted(envelope)},
        "representation": witness["representation"],
        "scalar": witness["scalar"],
        "coordinates": coordinates,
        "claim_coordinate_provenance": claim.get("coordinate_provenance"),
        "claim_method": claim.get("method"),
        "witness_keys": sorted(witness),
    }
    return Certificate(
        n=n,
        side=side,
        side_text=side_text,
        centers=centers,
        bases=bases,
        texts=texts,
        noncanonical=noncanonical,
        header=header,
    )


def read_path(path: str) -> Certificate:
    """Read a certificate from a file, decoding it as strict UTF-8."""
    with open(path, "rb") as handle:
        data = handle.read()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ReadRefused(f"not UTF-8: {error}") from error
    return read_text(text)
