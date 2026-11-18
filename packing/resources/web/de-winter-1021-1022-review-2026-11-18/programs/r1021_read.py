"""Strict readers for the certificate files of lane r1021-1118 (issues 1021 and 1022).

Reads data only and decides nothing about geometry.  Four layouts are read:

- form J, ``n2NN_exact.json``: one JSON object with exactly the keys n, side,
  square_size, format and squares, each square [center_x, center_y, cos, sin];
- form C, ``n2NN_witness.yaml``: a softschema envelope around a Witness/v2 witness with
  ``representation: corners``, rational scalars, ids ``square-1`` to ``square-n``;
- a house file: the same Witness/v2 corners form with integer ids 1 to n and the
  optional claim, source and certificate blocks (T-289's and T-283's certificates);
- a centre-basis witness (the house witness on main), read only to be compared.

Every scalar is parsed by one grammar, ``-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?``: no plus
sign, no leading zero, a denominator of at least 1 and no negative zero.  A scalar
not in lowest terms is read and flagged, not refused.  YAML is read twice: once
through PyYAML's event stream and composer (no anchor, alias, tag, directive, flow
collection, duplicate key, tab, carriage return or quoting other than single
quotes), and once line by line from the text, and the two readings must agree.
"""

from __future__ import annotations

import hashlib
import json
import re
from fractions import Fraction

import yaml

SCALAR = re.compile(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?\Z")
INTEGER = re.compile(r"[1-9][0-9]*\Z")
FORMAT_SENTENCE = (
    "each square: [center_x, center_y, cos, sin] as exact rationals; "
    "(cos, sin) is the unit direction of one edge"
)
FORM_J_KEYS = {"n", "side", "square_size", "format", "squares"}
WITNESS_REQUIRED = {
    "id", "n", "side", "square_size", "representation", "scalar", "coordinates",
    "squares", "claim",
}
WITNESS_ALLOWED = WITNESS_REQUIRED | {"source", "certificate"}
ENVELOPE_KEYS = {"contract", "schema", "envelope", "status"}


class ReadError(Exception):
    """A file that is not read: the message says where and why."""


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def scalar(text: object, where: str, flags: list) -> Fraction:
    """Parse one scalar by the grammar; flag one not in lowest terms."""
    if not isinstance(text, str):
        raise ReadError(f"{where}: not a string scalar ({type(text).__name__})")
    if not SCALAR.match(text):
        raise ReadError(f"{where}: scalar {text[:48]!r} is outside the grammar")
    body = text[1:] if text.startswith("-") else text
    if text.startswith("-") and body.split("/")[0] == "0":
        raise ReadError(f"{where}: negative zero")
    if "/" in body:
        p, q = body.split("/")
        value = Fraction(int(p), int(q))
        if value.denominator != int(q):
            flags.append([where, "not-lowest-terms"])
    else:
        value = Fraction(int(body))
    return -value if text.startswith("-") else value


# ---------------------------------------------------------------- form J (JSON)


def _pairs_no_duplicates(pairs):
    keys = [k for k, _ in pairs]
    if len(set(keys)) != len(keys):
        raise ReadError("form J: duplicate key")
    return dict(pairs)


def _refuse_number(text):
    raise ReadError(f"form J: non-integer JSON number {text[:32]!r}")


def _refuse_constant(text):
    raise ReadError(f"form J: JSON constant {text!r}")


def read_form_j(raw: bytes) -> dict:
    """Read a centre file strictly; return its side, rows and flags."""
    flags: list = []
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ReadError("form J: not ASCII") from exc
    if "\t" in text or "\r" in text:
        raise ReadError("form J: tab or carriage return")
    try:
        obj = json.loads(
            text,
            object_pairs_hook=_pairs_no_duplicates,
            parse_float=_refuse_number,
            parse_constant=_refuse_constant,
        )
    except json.JSONDecodeError as exc:
        raise ReadError(f"form J: not JSON ({exc.msg})") from exc
    if not isinstance(obj, dict) or set(obj) != FORM_J_KEYS:
        raise ReadError("form J: keys are not exactly n, side, square_size, format, squares")
    n = obj["n"]
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ReadError("form J: n is not a positive integer")
    side = scalar(obj["side"], "side", flags)
    if obj["square_size"] != "1":
        raise ReadError("form J: square_size is not the string 1")
    if obj["format"] != FORMAT_SENTENCE:
        raise ReadError("form J: format sentence differs")
    rows_in = obj["squares"]
    if not isinstance(rows_in, list) or len(rows_in) != n:
        raise ReadError(f"form J: squares is not a list of n = {n} rows")
    rows = []
    texts = []
    for k, row in enumerate(rows_in, start=1):
        if not isinstance(row, list) or len(row) != 4:
            raise ReadError(f"form J: row {k} is not four scalars")
        rows.append(tuple(scalar(v, f"row {k}[{m}]", flags) for m, v in enumerate(row)))
        texts.extend(row)
    # Second reading: every quoted token after "squares" in order, by a tokenizer.
    tail = text[text.index('"squares"') + len('"squares"'):]
    tokens = re.findall(r'"([^"\\]*)"', tail)
    if tokens != texts:
        raise ReadError("form J: the line reading of the squares differs from the JSON reading")
    side_tokens = re.findall(r'"side"\s*:\s*"([^"\\]*)"', text)
    if side_tokens != [obj["side"]]:
        raise ReadError("form J: the side is not stated exactly once")
    return {
        "form": "J",
        "n": n,
        "side": side,
        "side_text": obj["side"],
        "rows": rows,
        "flags": flags,
        "scalars": 1 + 4 * n,
        "sha256": sha256(raw),
    }


# ---------------------------------------------------------------- YAML


class Sc(str):
    """A YAML scalar's text, with its style (None for plain, ' for single-quoted)."""

    style: str | None = None


def _yaml_events_ok(text: str, where: str) -> None:
    docs = 0
    try:
        for ev in yaml.parse(text, Loader=yaml.SafeLoader):
            if isinstance(ev, yaml.DocumentStartEvent):
                docs += 1
                if ev.version is not None or ev.tags:
                    raise ReadError(f"{where}: YAML directive")
            elif isinstance(ev, yaml.AliasEvent):
                raise ReadError(f"{where}: YAML alias")
            elif isinstance(ev, (yaml.ScalarEvent, yaml.SequenceStartEvent, yaml.MappingStartEvent)):
                if ev.anchor is not None:
                    raise ReadError(f"{where}: YAML anchor")
                if ev.tag is not None:
                    raise ReadError(f"{where}: YAML tag")
                if isinstance(ev, yaml.ScalarEvent):
                    if ev.style not in (None, "'"):
                        raise ReadError(f"{where}: scalar style {ev.style!r}")
                elif ev.flow_style:
                    raise ReadError(f"{where}: flow collection")
    except yaml.YAMLError as exc:
        raise ReadError(f"{where}: not YAML ({type(exc).__name__})") from exc
    if docs != 1:
        raise ReadError(f"{where}: {docs} YAML documents")


def _plain(node, where: str):
    if isinstance(node, yaml.ScalarNode):
        s = Sc(node.value)
        s.style = node.style
        return s
    if isinstance(node, yaml.SequenceNode):
        return [_plain(v, where) for v in node.value]
    if isinstance(node, yaml.MappingNode):
        out: dict = {}
        for k, v in node.value:
            if not isinstance(k, yaml.ScalarNode):
                raise ReadError(f"{where}: non-scalar mapping key")
            if k.value in out:
                raise ReadError(f"{where}: duplicate key {k.value!r}")
            out[k.value] = _plain(v, where)
        return out
    raise ReadError(f"{where}: unexpected YAML node {type(node).__name__}")


def yaml_tree(raw: bytes, where: str):
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ReadError(f"{where}: not ASCII") from exc
    if "\t" in text or "\r" in text:
        raise ReadError(f"{where}: tab or carriage return")
    _yaml_events_ok(text, where)
    node = yaml.compose(text, Loader=yaml.SafeLoader)
    return text, _plain(node, where)


def _int_plain(v, where: str) -> int:
    if not isinstance(v, Sc) or v.style is not None or not INTEGER.match(v):
        raise ReadError(f"{where}: not a plain decimal integer")
    return int(v)


def _point(v, where: str, flags: list):
    if not isinstance(v, list) or len(v) != 2:
        raise ReadError(f"{where}: not a point of two scalars")
    for m, s in enumerate(v):
        if not isinstance(s, Sc) or s.style is not None:
            raise ReadError(f"{where}[{m}]: not a plain scalar")
    return (scalar(str(v[0]), f"{where}[0]", flags), scalar(str(v[1]), f"{where}[1]", flags))


def _envelope(tree, where: str) -> dict:
    if not isinstance(tree, dict) or set(tree) != {"softschema", "witness"}:
        raise ReadError(f"{where}: top level is not exactly softschema and witness")
    env = tree["softschema"]
    if not isinstance(env, dict) or set(env) != ENVELOPE_KEYS:
        raise ReadError(f"{where}: softschema keys differ")
    if env["contract"] != "packing.squares:Witness/v2" or env["envelope"] != "witness":
        raise ReadError(f"{where}: not a Witness/v2 envelope")
    w = tree["witness"]
    if not isinstance(w, dict):
        raise ReadError(f"{where}: witness is not a mapping")
    keys = set(w)
    if not WITNESS_REQUIRED <= keys or not keys <= WITNESS_ALLOWED:
        raise ReadError(f"{where}: witness keys outside the schema's list or missing")
    return w


def _common_witness(w, where: str, representation: str, flags: list):
    n = _int_plain(w["n"], f"{where} n")
    if not isinstance(w["side"], Sc) or w["side"].style is not None:
        raise ReadError(f"{where}: side is not a plain scalar")
    side = scalar(str(w["side"]), "side", flags)
    if w["square_size"] != "1":
        raise ReadError(f"{where}: square_size is not 1")
    if w["representation"] != representation:
        raise ReadError(f"{where}: representation is not {representation}")
    if w["scalar"] != {"kind": "rational"}:
        raise ReadError(f"{where}: scalar kind is not rational")
    if w["coordinates"] != {"origin": "lower-left", "axes": "x-right-y-up", "angle_unit": "not-applicable"}:
        raise ReadError(f"{where}: coordinates are not lower-left, x-right-y-up, not-applicable")
    claim = w["claim"]
    if not isinstance(claim, dict) or not {"coordinate_provenance", "method", "limitations"} <= set(claim):
        raise ReadError(f"{where}: claim block incomplete")
    sq = w["squares"]
    if not isinstance(sq, list) or len(sq) != n:
        raise ReadError(f"{where}: squares is not a list of n = {n}")
    return n, side, sq


def _id_ok(v, k: int, id_style: str) -> bool:
    if id_style == "square-k":
        return isinstance(v, Sc) and v.style is None and v == f"square-{k}"
    return isinstance(v, Sc) and v.style is None and v == str(k)


def _line_corners(text: str, n: int, id_style: str) -> list:
    lines = text.split("\n")
    try:
        i = lines.index("  squares:") + 1
    except ValueError as exc:
        raise ReadError("line reading: no '  squares:' line") from exc
    out = []
    for k in range(1, n + 1):
        ident = f"square-{k}" if id_style == "square-k" else str(k)
        if lines[i] != f"  - id: {ident}" or lines[i + 1] != "    corners:":
            raise ReadError(f"line reading: square {k} header differs")
        pts = []
        for c in range(4):
            a, b = lines[i + 2 + 2 * c], lines[i + 3 + 2 * c]
            if not a.startswith("    - - ") or not b.startswith("      - "):
                raise ReadError(f"line reading: square {k} corner {c} layout differs")
            pts.append((a[8:], b[8:]))
        out.append(pts)
        i += 10
    return out


def read_corners(raw: bytes, id_style: str = "square-k", where: str = "form C") -> dict:
    """Read a Witness/v2 corners file strictly (form C, or a house file with int ids)."""
    flags: list = []
    text, tree = yaml_tree(raw, where)
    w = _envelope(tree, where)
    n, side, sq = _common_witness(w, where, "corners", flags)
    squares = []
    texts = []
    for k, s in enumerate(sq, start=1):
        if not isinstance(s, dict) or set(s) != {"id", "corners"}:
            raise ReadError(f"{where}: square {k} keys are not exactly id and corners")
        if not _id_ok(s["id"], k, id_style):
            raise ReadError(f"{where}: square {k} id out of order or of the wrong kind")
        cs = s["corners"]
        if not isinstance(cs, list) or len(cs) != 4:
            raise ReadError(f"{where}: square {k} has not four corners")
        squares.append(tuple(_point(p, f"square {k} corner {c}", flags) for c, p in enumerate(cs)))
        texts.append([(str(p[0]), str(p[1])) for p in cs])
    if _line_corners(text, n, id_style) != texts:
        raise ReadError(f"{where}: the line reading of the corners differs from the YAML reading")
    side_lines = [ln for ln in text.split("\n") if ln.startswith("  side: ")]
    if side_lines != [f"  side: {w['side']}"]:
        raise ReadError(f"{where}: the side line is not stated exactly once")
    return {
        "form": "C",
        "n": n,
        "side": side,
        "side_text": str(w["side"]),
        "squares": squares,
        "flags": flags,
        "scalars": 1 + 8 * n,
        "claim": {k: str(v) for k, v in w["claim"].items()},
        "blocks": sorted(set(w) - WITNESS_REQUIRED),
        "witness_id": str(w["id"]),
        "envelope_schema": str(tree["softschema"]["schema"]),
        "envelope_status": str(tree["softschema"]["status"]),
        "sha256": sha256(raw),
    }


def read_center_basis(raw: bytes, where: str = "house witness") -> dict:
    """Read a centre-basis Witness/v2 file (compared with a certificate, never decided)."""
    flags: list = []
    _text, tree = yaml_tree(raw, where)
    w = _envelope(tree, where)
    n, side, sq = _common_witness(w, where, "center-basis", flags)
    poses = []
    for k, s in enumerate(sq, start=1):
        if not isinstance(s, dict) or set(s) != {"id", "center", "basis"}:
            raise ReadError(f"{where}: square {k} keys are not exactly id, center and basis")
        if not _id_ok(s["id"], k, "int"):
            raise ReadError(f"{where}: square {k} id out of order")
        c = s["center"]
        b = s["basis"]
        if not (isinstance(c, list) and len(c) == 2 and isinstance(b, list) and len(b) == 2):
            raise ReadError(f"{where}: square {k} centre or basis is not two scalars")
        x, y = (scalar(str(v), f"square {k} center", flags) for v in c)
        cc, ss = (scalar(str(v), f"square {k} basis", flags) for v in b)
        poses.append((x, y, cc, ss))
    return {"form": "center-basis", "n": n, "side": side, "poses": poses, "flags": flags, "sha256": sha256(raw)}
