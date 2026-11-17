"""Lane L105's strict reader for de Winter's n132/n157 exact files.

Reads `nNNN_exact.json` and `nNNN_witness.yaml` as data and hands the deciders
integers only: the side and, per square, (x, y, cos, sin), each as a pair (p, q)
of Python integers with q >= 1. It fails closed on any layout it does not expect.

Written for this review alone. It imports nothing from this repository or from
the source repository, and was written before any of the author's code was read.

Layout expected, from the files themselves and the README:

- JSON: an object with exactly the keys n, side, square_size, format, squares.
  `n` is an integer; `side`, `square_size` and every square entry's four items
  are strings holding a rational; `format` is the one sentence the file states;
  `squares` is a list of n lists of four strings [x, y, cos, sin].
- YAML: a mapping with the one key `witness`, a mapping with exactly the keys
  id, n, side, square_size, representation, scalar, coordinates, squares, where
  representation is `center-basis`, scalar is {kind: rational}, coordinates is
  {origin: lower-left, axes: x-right-y-up, angle_unit: not-applicable}, and
  squares is a list of n mappings {id, center: [x, y], basis: [cos, sin]} with
  ids 1..n in order.

A scalar is `-?(0|[1-9][0-9]*)` or `-?[1-9][0-9]*/[1-9][0-9]*` with the
denominator above 1; `-0` is refused. Lowest terms are recorded, not required.
"""

from __future__ import annotations

import json
import re
from math import gcd
from pathlib import Path
from typing import Any

import yaml

JSON_KEYS = ("n", "side", "square_size", "format", "squares")
JSON_FORMAT = (
    "each square: [center_x, center_y, cos, sin] as exact rationals; "
    "(cos, sin) is the unit direction of one edge"
)
YAML_KEYS = (
    "id",
    "n",
    "side",
    "square_size",
    "representation",
    "scalar",
    "coordinates",
    "squares",
)
INT_RE = re.compile(r"-?(0|[1-9][0-9]*)")
FRAC_RE = re.compile(r"(-?[1-9][0-9]*)/([1-9][0-9]*)")
STR_TAG = "tag:yaml.org,2002:str"
INT_TAG = "tag:yaml.org,2002:int"
MAP_TAG = "tag:yaml.org,2002:map"
SEQ_TAG = "tag:yaml.org,2002:seq"


class ReadError(ValueError):
    """The file is not in the layout this reader accepts."""


Rat = tuple[int, int]


def parse_scalar(text: str, where: str) -> tuple[Rat, bool]:
    """Return ((p, q), lowest_terms) for a canonical rational string."""
    if not isinstance(text, str):
        raise ReadError(f"{where}: not a string")
    if INT_RE.fullmatch(text):
        if text == "-0":
            raise ReadError(f"{where}: -0")
        return (int(text), 1), True
    m = FRAC_RE.fullmatch(text)
    if m is None:
        raise ReadError(f"{where}: not a rational: {text[:40]!r}")
    p, q = int(m.group(1)), int(m.group(2))
    if q <= 1:
        raise ReadError(f"{where}: denominator 1")
    return (p, q), gcd(p, q) == 1


def _no_dupes(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in pairs:
        if k in out:
            raise ReadError(f"JSON duplicate key {k!r}")
        out[k] = v
    return out


def _refuse_float(text: str) -> Any:
    raise ReadError(f"JSON float {text!r}")


def _refuse_const(text: str) -> Any:
    raise ReadError(f"JSON constant {text!r}")


def read_json_text(text: str) -> dict[str, Any]:
    """Read the JSON file's text into the common packing form."""
    try:
        obj = json.loads(
            text,
            object_pairs_hook=_no_dupes,
            parse_float=_refuse_float,
            parse_constant=_refuse_const,
        )
    except json.JSONDecodeError as exc:
        raise ReadError(f"JSON syntax: {exc}") from exc
    if not isinstance(obj, dict) or tuple(obj) != JSON_KEYS:
        raise ReadError(f"JSON keys {list(obj) if isinstance(obj, dict) else type(obj)}")
    n = obj["n"]
    if type(n) is not int or n < 1:
        raise ReadError("JSON n")
    if obj["square_size"] != "1":
        raise ReadError("JSON square_size")
    if obj["format"] != JSON_FORMAT:
        raise ReadError("JSON format sentence")
    side, low = parse_scalar(obj["side"], "JSON side")
    lowest = [low]
    sq = obj["squares"]
    if not isinstance(sq, list) or len(sq) != n:
        raise ReadError(f"JSON squares: {len(sq) if isinstance(sq, list) else 'not a list'} entries for n={n}")
    squares: list[tuple[Rat, Rat, Rat, Rat]] = []
    texts: list[tuple[str, str, str, str]] = []
    for i, entry in enumerate(sq, start=1):
        if not isinstance(entry, list) or len(entry) != 4:
            raise ReadError(f"JSON square {i}: not four items")
        vals = []
        for j, t in enumerate(entry):
            r, low = parse_scalar(t, f"JSON square {i} item {j}")
            vals.append(r)
            lowest.append(low)
        squares.append((vals[0], vals[1], vals[2], vals[3]))
        texts.append((entry[0], entry[1], entry[2], entry[3]))
    return {
        "n": n,
        "side": side,
        "side_text": obj["side"],
        "squares": squares,
        "texts": texts,
        "scalars": len(lowest),
        "lowest_terms": sum(lowest),
    }


def _check_events(text: str) -> None:
    for ev in yaml.parse(text, Loader=yaml.SafeLoader):
        if isinstance(ev, yaml.AliasEvent):
            raise ReadError("YAML alias")
        anchor = getattr(ev, "anchor", None)
        if anchor is not None:
            raise ReadError("YAML anchor")
        # The parser leaves `tag` as None unless the text writes one explicitly.
        tag = getattr(ev, "tag", None)
        if tag is not None:
            raise ReadError(f"YAML explicit tag {tag}")
        if isinstance(ev, yaml.DocumentStartEvent) and (ev.explicit or ev.version or ev.tags):
            raise ReadError("YAML directives or explicit document start")


def _map(node: yaml.Node, keys: tuple[str, ...], where: str) -> dict[str, yaml.Node]:
    if not isinstance(node, yaml.MappingNode) or node.tag != MAP_TAG:
        raise ReadError(f"{where}: not a mapping")
    out: dict[str, yaml.Node] = {}
    for k, v in node.value:
        if not isinstance(k, yaml.ScalarNode) or k.tag != STR_TAG:
            raise ReadError(f"{where}: key not a string")
        if k.value in out:
            raise ReadError(f"{where}: duplicate key {k.value!r}")
        out[k.value] = v
    if tuple(out) != keys:
        raise ReadError(f"{where}: keys {list(out)}, expected {list(keys)}")
    return out


def _seq(node: yaml.Node, where: str) -> list[yaml.Node]:
    if not isinstance(node, yaml.SequenceNode) or node.tag != SEQ_TAG:
        raise ReadError(f"{where}: not a sequence")
    return list(node.value)


def _str(node: yaml.Node, where: str) -> str:
    if not isinstance(node, yaml.ScalarNode) or node.tag != STR_TAG:
        raise ReadError(f"{where}: not a string scalar")
    return node.value


def _int(node: yaml.Node, where: str) -> int:
    if not isinstance(node, yaml.ScalarNode) or node.tag != INT_TAG or node.style is not None:
        raise ReadError(f"{where}: not a plain integer")
    if not INT_RE.fullmatch(node.value) or node.value.startswith("-"):
        raise ReadError(f"{where}: integer {node.value!r}")
    return int(node.value)


def read_yaml_text(text: str) -> dict[str, Any]:
    """Read the witness YAML's text into the common packing form."""
    try:
        _check_events(text)
        root = yaml.compose(text, Loader=yaml.SafeLoader)
    except yaml.YAMLError as exc:
        raise ReadError(f"YAML syntax: {exc}") from exc
    if root is None:
        raise ReadError("YAML empty")
    top = _map(root, ("witness",), "YAML top")
    w = _map(top["witness"], YAML_KEYS, "YAML witness")
    wid = _str(w["id"], "YAML id")
    n = _int(w["n"], "YAML n")
    side_text = _str(w["side"], "YAML side")
    side, low = parse_scalar(side_text, "YAML side")
    lowest = [low]
    if _str(w["square_size"], "YAML square_size") != "1":
        raise ReadError("YAML square_size")
    if _str(w["representation"], "YAML representation") != "center-basis":
        raise ReadError("YAML representation")
    sc = _map(w["scalar"], ("kind",), "YAML scalar")
    if _str(sc["kind"], "YAML scalar.kind") != "rational":
        raise ReadError("YAML scalar.kind")
    co = _map(w["coordinates"], ("origin", "axes", "angle_unit"), "YAML coordinates")
    want = {"origin": "lower-left", "axes": "x-right-y-up", "angle_unit": "not-applicable"}
    for k, v in want.items():
        if _str(co[k], f"YAML coordinates.{k}") != v:
            raise ReadError(f"YAML coordinates.{k}")
    items = _seq(w["squares"], "YAML squares")
    if len(items) != n:
        raise ReadError(f"YAML squares: {len(items)} entries for n={n}")
    squares: list[tuple[Rat, Rat, Rat, Rat]] = []
    texts: list[tuple[str, str, str, str]] = []
    styles: dict[str, int] = {}
    for i, node in enumerate(items, start=1):
        s = _map(node, ("id", "center", "basis"), f"YAML square {i}")
        if _int(s["id"], f"YAML square {i} id") != i:
            raise ReadError(f"YAML square {i}: id out of order")
        vals: list[Rat] = []
        tx: list[str] = []
        for key in ("center", "basis"):
            pt = _seq(s[key], f"YAML square {i} {key}")
            if len(pt) != 2:
                raise ReadError(f"YAML square {i} {key}: not two items")
            for j, sn in enumerate(pt):
                t = _str(sn, f"YAML square {i} {key}[{j}]")
                style = sn.style if isinstance(sn, yaml.ScalarNode) and sn.style else "plain"
                styles[style] = styles.get(style, 0) + 1
                r, low = parse_scalar(t, f"YAML square {i} {key}[{j}]")
                vals.append(r)
                tx.append(t)
                lowest.append(low)
        squares.append((vals[0], vals[1], vals[2], vals[3]))
        texts.append((tx[0], tx[1], tx[2], tx[3]))
    return {
        "n": n,
        "id": wid,
        "side": side,
        "side_text": side_text,
        "squares": squares,
        "texts": texts,
        "scalars": len(lowest),
        "lowest_terms": sum(lowest),
        "scalar_styles": styles,
    }


def read_json(path: Path) -> dict[str, Any]:
    return read_json_text(path.read_bytes().decode("utf-8", errors="strict"))


def read_yaml(path: Path) -> dict[str, Any]:
    return read_yaml_text(path.read_bytes().decode("utf-8", errors="strict"))


def _eq(a: Rat, b: Rat) -> bool:
    """Exact rational equality of two (p, q) pairs, by cross-multiplication."""
    return a[0] * b[1] == b[0] * a[1]


def compare(js: dict[str, Any], ym: dict[str, Any]) -> dict[str, Any]:
    """Decide whether the two files hold the same packing, square by square."""
    out: dict[str, Any] = {"n_equal": js["n"] == ym["n"]}
    out["side_equal"] = _eq(js["side"], ym["side"])
    out["side_text_equal"] = js["side_text"] == ym["side_text"]
    diffs: list[dict[str, Any]] = []
    text_diffs = 0
    if out["n_equal"]:
        for i, (a, b) in enumerate(zip(js["squares"], ym["squares"], strict=True), start=1):
            for j in range(4):
                if not _eq(a[j], b[j]):
                    diffs.append({"square": i, "item": ("x", "y", "cos", "sin")[j]})
            if js["texts"][i - 1] != ym["texts"][i - 1]:
                text_diffs += 1
    out["scalar_differences"] = diffs[:20]
    out["scalar_difference_count"] = len(diffs)
    out["squares_with_text_differences"] = text_diffs
    out["same_packing"] = bool(out["n_equal"] and out["side_equal"] and not diffs)
    return out
