"""Lane r1052's reader for the two forms of an exact square-packing certificate.

Form J is one JSON object with exactly the keys ``n``, ``side``, ``square_size``,
``format`` and ``squares``; each square is a list of four exact scalars
``[x, y, cos, sin]``: the centre and the direction of one edge.

Form C is a softschema envelope around a Witness/v2 record with
``representation: corners`` and ``scalar.kind: rational``: four corners per square.

The reader decides the reading and nothing else. It hands both methods exact
``Fraction`` values; it never checks that a square is a unit square, lies in the box or
misses another square. Every refusal raises ``Refused`` with the place and the reason.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from fractions import Fraction
from typing import Any

import yaml

sys.set_int_max_str_digits(0)

RATIONAL = re.compile(r"(-?(?:0|[1-9][0-9]*))(?:/([1-9][0-9]*))?\Z")
DECIMAL = re.compile(r"-?(?:0|[1-9][0-9]*)\.[0-9]+\Z")

J_KEYS = ("n", "side", "square_size", "format", "squares")
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
WITNESS_OPTIONAL = ("source", "certificate")
CONTRACT = "packing.squares:Witness/v2"

YSTR = "tag:yaml.org,2002:str"
YINT = "tag:yaml.org,2002:int"


class Refused(ValueError):
    """The reader refuses the file: the message says where and why."""


def git_blob_id(data: bytes) -> str:
    """The git blob id of these bytes, as `git hash-object` computes it."""
    return hashlib.sha1(b"blob %d\0" % len(data) + data, usedforsecurity=False).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_scalar(text: str, where: str, *, decimal_ok: bool) -> tuple[Fraction, str, bool]:
    """One scalar: ``p``, ``p/q``, or (where allowed) a finite decimal.

    Returns the exact value, its form (integer, fraction or decimal) and whether it is
    canonical: an integer other than ``-0``, or a fraction in lowest terms with q > 1.
    A decimal is exact but never canonical.
    """
    m = RATIONAL.match(text)
    if m:
        p = int(m.group(1))
        if m.group(2) is None:
            return Fraction(p), "integer", text != "-0"
        q = int(m.group(2))
        value = Fraction(p, q)
        canonical = (
            value.numerator == p and value.denominator == q and q != 1 and not text.startswith("-0")
        )
        return value, "fraction", canonical
    if decimal_ok and DECIMAL.match(text):
        return Fraction(text), "decimal", False
    raise Refused(f"{where}: {text[:40]!r} is not an exact scalar")


class _Tally:
    def __init__(self) -> None:
        self.forms: dict[str, int] = {}
        self.noncanonical: list[str] = []

    def add(self, form: str, canonical: bool, where: str) -> None:
        self.forms[form] = self.forms.get(form, 0) + 1
        if not canonical:
            self.noncanonical.append(where)


# ----------------------------------------------------------------------------- form J


def read_form_j(data: bytes) -> dict[str, Any]:
    """Read form J exactly. Returns n, side and the poses (x, y, cos, sin)."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Refused(f"form J: not UTF-8 ({exc.reason} at byte {exc.start})") from None

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        seen: set[str] = set()
        for key, _ in items:
            if key in seen:
                raise Refused(f"form J: the key {key!r} twice in one object")
            seen.add(key)
        return dict(items)

    def no_float(token: str) -> Any:
        raise Refused(f"form J: a JSON number with a fraction or exponent ({token[:24]})")

    def no_constant(token: str) -> Any:
        raise Refused(f"form J: the non-finite constant {token}")

    try:
        obj = json.loads(
            text, object_pairs_hook=pairs, parse_float=no_float, parse_constant=no_constant
        )
    except json.JSONDecodeError as exc:
        raise Refused(f"form J: not JSON ({exc.msg} at line {exc.lineno})") from None
    if not isinstance(obj, dict):
        raise Refused("form J: the top level is not an object")
    keys = list(obj)
    if sorted(keys) != sorted(J_KEYS):
        missing = [k for k in J_KEYS if k not in obj]
        extra = [k for k in keys if k not in J_KEYS]
        raise Refused(f"form J: keys missing {missing}, unexpected {extra}")
    n = obj["n"]
    if type(n) is not int or n < 1:
        raise Refused("form J: n is not a positive integer")
    if obj["square_size"] != "1" or type(obj["square_size"]) is not str:
        raise Refused("form J: square_size is not the string '1'")
    fmt = obj["format"]
    if type(fmt) is not str:
        raise Refused("form J: format is not a string")
    tally = _Tally()
    if type(obj["side"]) is not str:
        raise Refused("form J: side is not a string")
    side, form, canon = parse_scalar(obj["side"], "form J side", decimal_ok=True)
    tally.add(form, canon, "side")
    rows = obj["squares"]
    if type(rows) is not list:
        raise Refused("form J: squares is not a list")
    if len(rows) != n:
        raise Refused(f"form J: n is {n} and {len(rows)} squares are listed")
    poses: list[tuple[Fraction, Fraction, Fraction, Fraction]] = []
    for k, row in enumerate(rows):
        if type(row) is not list or len(row) != 4:
            raise Refused(f"form J: square {k + 1} is not a list of four scalars")
        values: list[Fraction] = []
        for slot, item in zip(("x", "y", "cos", "sin"), row, strict=True):
            where = f"form J square {k + 1} {slot}"
            if type(item) is not str:
                raise Refused(f"{where}: not a string")
            value, form, canon = parse_scalar(item, where, decimal_ok=True)
            tally.add(form, canon, where)
            values.append(value)
        poses.append((values[0], values[1], values[2], values[3]))
    return {
        "form": "J",
        "n": n,
        "side": side,
        "side_text": obj["side"],
        "format": fmt,
        "poses": poses,
        "scalar_forms": tally.forms,
        "noncanonical": tally.noncanonical,
        "ascii": text.isascii(),
        "final_newline": text.endswith("\n"),
        "bytes": len(data),
        "sha256": sha256(data),
        "git_blob": git_blob_id(data),
    }


# ----------------------------------------------------------------------------- form C


def _loader() -> type:
    return yaml.CSafeLoader if getattr(yaml, "__with_libyaml__", False) else yaml.SafeLoader


def _events_clean(text: str) -> None:
    try:
        events = list(yaml.parse(text, Loader=_loader()))
    except yaml.YAMLError as exc:
        raise Refused(f"form C: not YAML ({str(exc).splitlines()[0]})") from None
    documents = 0
    for ev in events:
        if isinstance(ev, yaml.DocumentStartEvent):
            documents += 1
            if ev.version is not None or ev.tags:
                raise Refused("form C: a YAML directive")
        elif isinstance(ev, yaml.AliasEvent):
            raise Refused("form C: an alias")
        elif isinstance(ev, (yaml.ScalarEvent, yaml.SequenceStartEvent, yaml.MappingStartEvent)):
            if ev.anchor is not None:
                raise Refused(f"form C: an anchor ({ev.anchor})")
            if ev.tag is not None:
                raise Refused(f"form C: an explicit tag ({ev.tag})")
    if documents != 1:
        raise Refused(f"form C: {documents} YAML documents")


def _mapping(
    node: Any, where: str, required: tuple[str, ...], optional: tuple[str, ...] = (), *, open_: bool = False
) -> dict[str, Any]:
    if not isinstance(node, yaml.MappingNode):
        raise Refused(f"{where}: not a mapping")
    out: dict[str, Any] = {}
    for key, value in node.value:
        if not isinstance(key, yaml.ScalarNode) or key.tag != YSTR:
            raise Refused(f"{where}: a key that is not a string")
        if key.value in out:
            raise Refused(f"{where}: the key {key.value!r} twice")
        out[key.value] = value
    missing = [k for k in required if k not in out]
    extra = [k for k in out if k not in required and k not in optional]
    if missing or (extra and not open_):
        raise Refused(f"{where}: keys missing {missing}, unexpected {extra}")
    return out


def _sequence(node: Any, where: str, length: int | None = None) -> list[Any]:
    if not isinstance(node, yaml.SequenceNode):
        raise Refused(f"{where}: not a sequence")
    if length is not None and len(node.value) != length:
        raise Refused(f"{where}: {len(node.value)} items where {length} are required")
    return list(node.value)


def _text(node: Any, where: str, *, allowed: tuple[str, ...] | None = None) -> str:
    if not isinstance(node, yaml.ScalarNode) or node.tag != YSTR:
        raise Refused(f"{where}: not a string")
    if allowed is not None and node.value not in allowed:
        raise Refused(f"{where}: {node.value!r} where {list(allowed)} is required")
    return node.value


def _number(node: Any, where: str, tally: _Tally) -> Fraction:
    if not isinstance(node, yaml.ScalarNode):
        raise Refused(f"{where}: not a scalar")
    quoted = node.style in ("'", '"')
    if node.style in ("|", ">"):
        raise Refused(f"{where}: a block scalar")
    if not quoted and node.tag not in (YSTR, YINT):
        raise Refused(f"{where}: a plain scalar YAML reads as {node.tag.rsplit(':', 1)[-1]}")
    value, form, canon = parse_scalar(node.value, where, decimal_ok=quoted)
    tally.add(form, canon, where)
    return value


def read_form_c(data: bytes) -> dict[str, Any]:
    """Read form C exactly. Returns n, side, the ids and the corners in the lower-left frame."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Refused(f"form C: not UTF-8 ({exc.reason} at byte {exc.start})") from None
    _events_clean(text)
    try:
        root = yaml.compose(text, Loader=_loader())
    except yaml.YAMLError as exc:
        raise Refused(f"form C: not YAML ({str(exc).splitlines()[0]})") from None
    top = _mapping(root, "form C top level", ("softschema", "witness"))
    envelope = _mapping(top["softschema"], "softschema", ("contract", "envelope"), open_=True)
    _text(envelope["contract"], "softschema.contract", allowed=(CONTRACT,))
    _text(envelope["envelope"], "softschema.envelope", allowed=("witness",))
    envelope_keys = sorted(envelope)
    w = _mapping(top["witness"], "witness", WITNESS_REQUIRED, WITNESS_OPTIONAL)
    witness_id = _text(w["id"], "witness.id")
    n_node = w["n"]
    if (
        not isinstance(n_node, yaml.ScalarNode)
        or n_node.tag != YINT
        or n_node.style not in (None, "")
        or not re.fullmatch(r"[1-9][0-9]*", n_node.value)
    ):
        raise Refused("witness.n: not a plain positive decimal integer")
    n = int(n_node.value)
    tally = _Tally()
    side = _number(w["side"], "witness.side", tally)
    _text(w["square_size"], "witness.square_size", allowed=("1",))
    _text(w["representation"], "witness.representation", allowed=("corners",))
    scalar = _mapping(w["scalar"], "witness.scalar", ("kind",))
    _text(scalar["kind"], "witness.scalar.kind", allowed=("rational",))
    coords = _mapping(w["coordinates"], "witness.coordinates", ("origin", "axes", "angle_unit"))
    origin = _text(coords["origin"], "coordinates.origin", allowed=("lower-left", "container-center"))
    _text(coords["axes"], "coordinates.axes", allowed=("x-right-y-up",))
    angle_unit = _text(
        coords["angle_unit"], "coordinates.angle_unit", allowed=("degrees", "radians", "not-applicable")
    )
    claim = _mapping(w["claim"], "witness.claim", (), open_=True)
    rows = _sequence(w["squares"], "witness.squares")
    if len(rows) != n:
        raise Refused(f"witness: n is {n} and {len(rows)} squares are listed")
    shift = side / 2 if origin == "container-center" else Fraction(0)
    ids: list[str] = []
    seen: set[str] = set()
    corners: list[list[tuple[Fraction, Fraction]]] = []
    for k, row in enumerate(rows):
        where = f"witness square {k + 1}"
        entry = _mapping(row, where, ("id", "corners"))
        id_node = entry["id"]
        if not isinstance(id_node, yaml.ScalarNode) or id_node.tag not in (YSTR, YINT):
            raise Refused(f"{where}: the id is not a string or an integer")
        key = f"{id_node.tag.rsplit(':', 1)[-1]}:{id_node.value}"
        if key in seen:
            raise Refused(f"{where}: the id {id_node.value!r} twice")
        seen.add(key)
        ids.append(id_node.value)
        points = _sequence(entry["corners"], f"{where} corners", 4)
        square: list[tuple[Fraction, Fraction]] = []
        for c, point in enumerate(points):
            pair = _sequence(point, f"{where} corner {c + 1}", 2)
            x = _number(pair[0], f"{where} corner {c + 1} x", tally) + shift
            y = _number(pair[1], f"{where} corner {c + 1} y", tally) + shift
            square.append((x, y))
        corners.append(square)
    return {
        "form": "C",
        "n": n,
        "side": side,
        "witness_id": witness_id,
        "origin": origin,
        "angle_unit": angle_unit,
        "envelope_keys": envelope_keys,
        "witness_keys": sorted(w),
        "claim_keys": sorted(claim),
        "ids": ids,
        "corners": corners,
        "scalar_forms": tally.forms,
        "noncanonical": tally.noncanonical,
        "ascii": text.isascii(),
        "final_newline": text.endswith("\n"),
        "bytes": len(data),
        "sha256": sha256(data),
        "git_blob": git_blob_id(data),
        "yaml_loader": _loader().__name__,
    }
