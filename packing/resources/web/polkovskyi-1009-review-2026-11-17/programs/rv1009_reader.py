"""Strict readers for the two certificate forms of issue #1009.

Lane c-review-1009-1117, stage 4 blind review. Clean-room: written for this review from
the files' structure and the Witness/v2 schema text; it imports nothing from this
repository or from the source, and decides no geometry.

Form P ("poses"), a ``.cert`` text file::

    # comment lines, only before the header
    n S
    x y t          (n lines)

Form C ("corners"), a Witness/v2 YAML file with ``representation: corners`` and
``scalar.kind: rational``: four corners of two scalars for each square.

Every scalar is a string ``p`` or ``p/q`` in the grammar ``-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?``.
The readers hand out each scalar as a pair of Python integers ``(numerator, denominator)``
with a positive denominator, exactly as written and not reduced. Whether a scalar is in
canonical form (lowest terms, no ``/1``, no ``-0``) is recorded and never required.
"""

from __future__ import annotations

import math
import re

import yaml

SCALAR = re.compile(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?")
COUNT = re.compile(r"[1-9][0-9]*")
INT_PLAIN = re.compile(r"0|[1-9][0-9]*")

WITNESS_KEYS = (
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
)
WITNESS_REQUIRED = (
    "id",
    "n",
    "side",
    "square_size",
    "representation",
    "scalar",
    "coordinates",
    "squares",
    "claim",
)
CONTRACT = "packing.squares:Witness/v2"
STR_TAG = "tag:yaml.org,2002:str"
INT_TAG = "tag:yaml.org,2002:int"


class ReadError(Exception):
    """The file is not in the form this review reads."""


def parse_scalar(text: object, where: str) -> tuple[int, int, bool]:
    """Return (numerator, denominator, canonical) of one scalar string."""
    if not isinstance(text, str):
        raise ReadError(f"{where}: scalar is not a string")
    if SCALAR.fullmatch(text) is None:
        raise ReadError(f"{where}: not a scalar p or p/q: {text[:40]!r}")
    if "/" in text:
        head, tail = text.split("/")
        num, den = int(head), int(tail)
        canonical = den >= 2 and math.gcd(abs(num), den) == 1
    else:
        num, den = int(text), 1
        canonical = True
    if text.startswith("-") and num == 0:
        canonical = False
    return num, den, canonical


def _text_of(data: bytes, what: str) -> str:
    if not isinstance(data, bytes):
        raise ReadError(f"{what}: not bytes")
    try:
        text = data.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ReadError(f"{what}: not ASCII") from exc
    if "\r" in text:
        raise ReadError(f"{what}: carriage return")
    if "\t" in text:
        raise ReadError(f"{what}: tab")
    if not text.endswith("\n"):
        raise ReadError(f"{what}: no final newline")
    return text


def read_cert(data: bytes) -> dict:
    """Read form P. Raises ReadError on anything outside the form."""
    text = _text_of(data, "cert")
    lines = text.split("\n")[:-1]
    comments = []
    k = 0
    while k < len(lines) and lines[k].startswith("#"):
        comments.append(lines[k])
        k += 1
    body = lines[k:]
    if not body:
        raise ReadError("cert: no header line")
    for idx, line in enumerate(body):
        if line == "":
            raise ReadError(f"cert: blank line at body line {idx + 1}")
        if line.startswith("#"):
            raise ReadError(f"cert: comment after the header at body line {idx + 1}")
        if line != line.strip(" ") or "  " in line:
            raise ReadError(f"cert: stray space at body line {idx + 1}")
    head = body[0].split(" ")
    if len(head) != 2:
        raise ReadError("cert: header is not 'n S'")
    if COUNT.fullmatch(head[0]) is None:
        raise ReadError("cert: n is not a plain positive integer")
    n = int(head[0])
    noncanonical = []
    sn, sd, canon = parse_scalar(head[1], "cert side")
    if not canon:
        noncanonical.append("side")
    if sn <= 0:
        raise ReadError("cert: side is not positive")
    rows = body[1:]
    if len(rows) != n:
        raise ReadError(f"cert: n is {n} and {len(rows)} squares are listed")
    poses = []
    for idx, line in enumerate(rows):
        parts = line.split(" ")
        if len(parts) != 3:
            raise ReadError(f"cert: square {idx + 1} is not 'x y t'")
        triple = []
        for name, part in zip("xyt", parts, strict=True):
            num, den, canon = parse_scalar(part, f"cert square {idx + 1} {name}")
            if not canon:
                noncanonical.append(f"square {idx + 1} {name}")
            triple.append((num, den))
        poses.append(tuple(triple))
    return {
        "form": "poses",
        "n": n,
        "side": (sn, sd),
        "side_text": head[1],
        "comments": comments,
        "poses": poses,
        "scalars": 1 + 3 * n,
        "noncanonical": noncanonical,
    }


def _check_events(text: str) -> None:
    documents = 0
    try:
        events = list(yaml.parse(text, Loader=yaml.SafeLoader))
    except yaml.YAMLError as exc:
        raise ReadError(f"witness: not YAML: {type(exc).__name__}") from exc
    for event in events:
        if isinstance(event, yaml.AliasEvent):
            raise ReadError("witness: alias")
        if getattr(event, "anchor", None) is not None:
            raise ReadError("witness: anchor")
        if isinstance(event, yaml.DocumentStartEvent):
            documents += 1
            if event.explicit or event.version is not None or event.tags:
                raise ReadError("witness: document marker or directive")
        if isinstance(event, yaml.DocumentEndEvent) and event.explicit:
            raise ReadError("witness: document end marker")
        if isinstance(event, yaml.ScalarEvent | yaml.CollectionStartEvent):
            if event.tag is not None:
                raise ReadError("witness: explicit tag")
    if documents != 1:
        raise ReadError(f"witness: {documents} documents")


def _plain(node: yaml.Node, where: str) -> object:
    if isinstance(node, yaml.MappingNode):
        out: dict = {}
        for key_node, value_node in node.value:
            if not isinstance(key_node, yaml.ScalarNode) or key_node.tag != STR_TAG:
                raise ReadError(f"{where}: a key is not a string")
            key = key_node.value
            if key in out:
                raise ReadError(f"{where}: duplicate key {key!r}")
            out[key] = _plain(value_node, f"{where}.{key}")
        return out
    if isinstance(node, yaml.SequenceNode):
        return [_plain(item, f"{where}[{i}]") for i, item in enumerate(node.value)]
    if isinstance(node, yaml.ScalarNode):
        if node.tag == STR_TAG:
            return node.value
        if node.tag == INT_TAG:
            if INT_PLAIN.fullmatch(node.value) is None:
                raise ReadError(f"{where}: integer not in plain decimal form")
            return int(node.value)
        raise ReadError(f"{where}: scalar of kind {node.tag.rsplit(':', 1)[-1]}")
    raise ReadError(f"{where}: unknown node")


def _need_map(value: object, where: str, keys: tuple[str, ...]) -> dict:
    if not isinstance(value, dict):
        raise ReadError(f"{where}: not a mapping")
    if tuple(sorted(value)) != tuple(sorted(keys)):
        raise ReadError(f"{where}: keys {sorted(value)} are not {sorted(keys)}")
    return value


def read_witness(data: bytes) -> dict:
    """Read form C. Raises ReadError on anything outside the form."""
    text = _text_of(data, "witness")
    _check_events(text)
    try:
        node = yaml.compose(text, Loader=yaml.SafeLoader)
    except yaml.YAMLError as exc:
        raise ReadError(f"witness: not YAML: {type(exc).__name__}") from exc
    if node is None:
        raise ReadError("witness: empty document")
    doc = _need_map(_plain(node, "doc"), "doc", ("softschema", "witness"))
    env = _need_map(
        doc["softschema"], "softschema", ("contract", "schema", "envelope", "status")
    )
    if env["contract"] != CONTRACT:
        raise ReadError("softschema: contract is not Witness/v2")
    if env["envelope"] != "witness":
        raise ReadError("softschema: envelope is not witness")
    if not isinstance(env["schema"], str) or not isinstance(env["status"], str):
        raise ReadError("softschema: schema or status is not a string")
    wit = doc["witness"]
    if not isinstance(wit, dict):
        raise ReadError("witness: not a mapping")
    for key in wit:
        if key not in WITNESS_KEYS:
            raise ReadError(f"witness: key {key!r} is not in the schema")
    for key in WITNESS_REQUIRED:
        if key not in wit:
            raise ReadError(f"witness: required key {key!r} is missing")
    if not isinstance(wit["id"], str):
        raise ReadError("witness: id is not a string")
    n = wit["n"]
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ReadError("witness: n is not a positive integer")
    if wit["square_size"] != "1":
        raise ReadError("witness: square_size is not '1'")
    if wit["representation"] != "corners":
        raise ReadError("witness: representation is not corners")
    scalar = _need_map(wit["scalar"], "witness.scalar", ("kind",))
    if scalar["kind"] != "rational":
        raise ReadError("witness: scalar.kind is not rational")
    coords = _need_map(
        wit["coordinates"], "witness.coordinates", ("origin", "axes", "angle_unit")
    )
    if coords["origin"] != "lower-left" or coords["axes"] != "x-right-y-up":
        raise ReadError("witness: origin is not lower-left or axes not x-right-y-up")
    if coords["angle_unit"] not in ("degrees", "radians", "not-applicable"):
        raise ReadError("witness: angle_unit outside the schema")
    claim = wit["claim"]
    if not isinstance(claim, dict):
        raise ReadError("witness: claim is not a mapping")
    for key in ("coordinate_provenance", "method", "limitations"):
        if not isinstance(claim.get(key), str):
            raise ReadError(f"witness: claim.{key} is missing or not a string")
    noncanonical = []
    sn, sd, canon = parse_scalar(wit["side"], "witness side")
    if not canon:
        noncanonical.append("side")
    if sn <= 0:
        raise ReadError("witness: side is not positive")
    listed = wit["squares"]
    if not isinstance(listed, list):
        raise ReadError("witness: squares is not a sequence")
    if len(listed) != n:
        raise ReadError(f"witness: n is {n} and {len(listed)} squares are listed")
    styles = set()
    squares = []
    for idx, item in enumerate(listed):
        entry = _need_map(item, f"square {idx + 1}", ("id", "corners"))
        ident = entry["id"]
        if isinstance(ident, int) and not isinstance(ident, bool) and ident == idx + 1:
            styles.add("integer")
        elif ident == f"square-{idx + 1}":
            styles.add("square-k")
        else:
            raise ReadError(f"witness: square {idx + 1} has id {ident!r}, out of order")
        corners = entry["corners"]
        if not isinstance(corners, list) or len(corners) != 4:
            raise ReadError(f"witness: square {idx + 1} does not have four corners")
        quad = []
        for c, corner in enumerate(corners):
            if not isinstance(corner, list) or len(corner) != 2:
                raise ReadError(f"witness: square {idx + 1} corner {c + 1} is not a pair")
            point = []
            for name, part in zip("xy", corner, strict=True):
                where = f"witness square {idx + 1} corner {c + 1} {name}"
                num, den, canon = parse_scalar(part, where)
                if not canon:
                    noncanonical.append(f"square {idx + 1} corner {c + 1} {name}")
                point.append((num, den))
            quad.append(tuple(point))
        squares.append(tuple(quad))
    if len(styles) != 1:
        raise ReadError("witness: square ids of two styles")
    return {
        "form": "corners",
        "n": n,
        "side": (sn, sd),
        "side_text": wit["side"],
        "id": wit["id"],
        "id_style": styles.pop(),
        "envelope": dict(env),
        "coordinates": dict(coords),
        "claim": {key: claim[key] for key in sorted(claim)},
        "other_keys": sorted(k for k in wit if k not in WITNESS_REQUIRED),
        "squares": squares,
        "scalars": 1 + 8 * n,
        "noncanonical": noncanonical,
    }
