"""Strict readers for the two forms this review decides (lane r127b-1118).

Form J is de Winter's centre file, ``n127/n127_exact.json``: one JSON object with
exactly the keys ``n``, ``side``, ``square_size``, ``format`` and ``squares``, each
square ``[center_x, center_y, cos, sin]`` as exact rational strings.

Form C is a Witness/v2 file of rational corners (de Winter's ``n127_witness.yaml`` and
the house certificate of T-305, ``n-127-candidate.yaml``): a softschema envelope around
a witness with ``representation: corners``, read through PyYAML's composer only, every
node checked, and every corner scalar read a second time line by line.

Every scalar is a string ``p`` or ``p/q``: an optional minus, no plus, no leading zero,
``q >= 1``, no negative zero. Values are handed out as written, ``(p, q)``, never
reduced; whether each is in lowest terms is recorded, not required.

The module decides nothing about a packing. It imports nothing from this repository or
from the source.
"""

from __future__ import annotations

import json
import math
import re
from typing import Any

import yaml

SCALAR_RE = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?")
FORMAT_SENTENCE = (
    "each square: [center_x, center_y, cos, sin] as exact rationals; "
    "(cos, sin) is the unit direction of one edge"
)
J_KEYS = ["n", "side", "square_size", "format", "squares"]
WITNESS_REQUIRED = [
    "id", "n", "side", "square_size", "representation", "scalar", "coordinates",
    "squares", "claim",
]
WITNESS_ALLOWED = WITNESS_REQUIRED + ["source", "certificate"]
CLAIM_ALLOWED = ["coordinate_provenance", "method", "precision", "tolerance", "limitations"]
STR_TAG = "tag:yaml.org,2002:str"
INT_TAG = "tag:yaml.org,2002:int"
MAP_TAG = "tag:yaml.org,2002:map"
SEQ_TAG = "tag:yaml.org,2002:seq"


class ReadError(Exception):
    """A file this review's readers refuse."""


def parse_scalar(text: Any, where: str) -> tuple[int, int]:
    """Read one scalar string as written: ``(p, q)`` with ``q >= 1``, not reduced."""
    if not isinstance(text, str):
        raise ReadError(f"{where}: not a string scalar ({type(text).__name__})")
    if not SCALAR_RE.fullmatch(text):
        raise ReadError(f"{where}: not a scalar p or p/q: {text[:60]!r}")
    num_text, _, den_text = text.partition("/")
    if num_text == "-0":
        raise ReadError(f"{where}: negative zero")
    p = int(num_text)
    q = int(den_text) if den_text else 1
    return p, q


def lowest(pq: tuple[int, int]) -> bool:
    p, q = pq
    return math.gcd(p, q) == 1


def _hygiene(data: bytes, what: str, *, final_newline: bool) -> str:
    try:
        text = data.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ReadError(f"{what}: not ASCII ({exc})") from None
    if "\r" in text:
        raise ReadError(f"{what}: carriage return")
    if "\t" in text:
        raise ReadError(f"{what}: tab")
    if final_newline and not text.endswith("\n"):
        raise ReadError(f"{what}: no final newline")
    for k, line in enumerate(text.split("\n"), 1):
        if line.endswith(" "):
            raise ReadError(f"{what}: trailing space on line {k}")
    return text


# ----------------------------------------------------------------------------- form J


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen: dict[str, Any] = {}
    order: list[str] = []
    for k, v in pairs:
        if k in seen:
            raise ReadError(f"form J: duplicate key {k!r}")
        seen[k] = v
        order.append(k)
    seen["__order__"] = order
    return seen


def _no_float(text: str) -> Any:
    raise ReadError(f"form J: a JSON number that is not an integer: {text[:40]!r}")


def _no_constant(text: str) -> Any:
    raise ReadError(f"form J: a JSON constant {text!r}")


def read_form_j(data: bytes) -> dict[str, Any]:
    """Read a centre file strictly; return its count, side and rows as written."""
    text = _hygiene(data, "form J", final_newline=False)
    try:
        obj = json.loads(
            text,
            object_pairs_hook=_pairs_no_duplicates,
            parse_float=_no_float,
            parse_constant=_no_constant,
        )
    except json.JSONDecodeError as exc:
        raise ReadError(f"form J: not JSON ({exc})") from None
    if not isinstance(obj, dict):
        raise ReadError("form J: the document is not an object")
    order = obj.pop("__order__")
    if sorted(order) != sorted(J_KEYS) or len(order) != len(J_KEYS):
        raise ReadError(f"form J: keys {order}, expected exactly {J_KEYS}")
    n = obj["n"]
    if type(n) is not int or n < 1:
        raise ReadError(f"form J: n is not a positive integer: {n!r}")
    if obj["square_size"] != "1":
        raise ReadError(f"form J: square_size {obj['square_size']!r}, expected the string '1'")
    if obj["format"] != FORMAT_SENTENCE:
        raise ReadError("form J: the format sentence differs from the one this reader reads")
    side = parse_scalar(obj["side"], "form J side")
    squares = obj["squares"]
    if not isinstance(squares, list):
        raise ReadError("form J: squares is not a list")
    if len(squares) != n:
        raise ReadError(f"form J: n = {n} stated, {len(squares)} squares listed")
    rows: list[tuple[tuple[int, int], ...]] = []
    for k, row in enumerate(squares, 1):
        if not isinstance(row, list) or len(row) != 4:
            raise ReadError(f"form J: square {k} is not a list of four scalars")
        names = ("center_x", "center_y", "cos", "sin")
        rows.append(tuple(parse_scalar(v, f"form J square {k} {names[i]}") for i, v in enumerate(row)))
    flags = []
    if not lowest(side):
        flags.append("side not in lowest terms")
    nonlowest = sum(1 for r in rows for v in r if not lowest(v))
    if nonlowest:
        flags.append(f"{nonlowest} row scalars not in lowest terms")
    return {
        "form": "J",
        "n": n,
        "side": side,
        "rows": rows,
        "key_order": order,
        "flags": flags,
        "scalars": 1 + 4 * n,
    }


# ----------------------------------------------------------------------------- form C


def _check_nodes(node: yaml.Node, seen: set[int], path: str) -> None:
    if id(node) in seen:
        raise ReadError(f"form C: a node reached twice (an alias) at {path}")
    seen.add(id(node))
    if isinstance(node, yaml.ScalarNode):
        if node.tag not in (STR_TAG, INT_TAG):
            raise ReadError(f"form C: scalar of tag {node.tag} at {path}: {str(node.value)[:40]!r}")
        if node.tag == INT_TAG and not re.fullmatch(r"(?:0|[1-9][0-9]*)", node.value):
            raise ReadError(f"form C: integer not plain decimal at {path}: {node.value!r}")
        if node.tag == STR_TAG and node.style not in (None, "'", '"', ""):
            raise ReadError(f"form C: block scalar style {node.style!r} at {path}")
    elif isinstance(node, yaml.SequenceNode):
        if node.tag != SEQ_TAG:
            raise ReadError(f"form C: sequence tag {node.tag} at {path}")
        if node.flow_style:
            raise ReadError(f"form C: flow sequence at {path}")
        for k, child in enumerate(node.value):
            _check_nodes(child, seen, f"{path}[{k}]")
    elif isinstance(node, yaml.MappingNode):
        if node.tag != MAP_TAG:
            raise ReadError(f"form C: mapping tag {node.tag} at {path}")
        if node.flow_style:
            raise ReadError(f"form C: flow mapping at {path}")
        keys: set[str] = set()
        for key, value in node.value:
            if not isinstance(key, yaml.ScalarNode) or key.tag != STR_TAG:
                raise ReadError(f"form C: a mapping key that is not a string at {path}")
            if key.value in keys:
                raise ReadError(f"form C: duplicate key {key.value!r} at {path}")
            keys.add(key.value)
            _check_nodes(key, seen, f"{path}.{key.value}(key)")
            _check_nodes(value, seen, f"{path}.{key.value}")
    else:
        raise ReadError(f"form C: unexpected node {type(node).__name__} at {path}")


def _build(node: yaml.Node) -> Any:
    if isinstance(node, yaml.ScalarNode):
        return int(node.value) if node.tag == INT_TAG else str(node.value)
    if isinstance(node, yaml.SequenceNode):
        return [_build(c) for c in node.value]
    if isinstance(node, yaml.MappingNode):
        return {k.value: _build(v) for k, v in node.value}
    raise ReadError("form C: unbuildable node")


def _second_reading(text: str) -> dict[str, Any]:
    """Read the side and every corner scalar again, line by line, without YAML."""
    lines = text.split("\n")
    side = None
    corners: list[list[list[str]]] = []
    ids: list[str] = []
    in_squares = False
    k = 0

    def unquote(v: str) -> str:
        if len(v) >= 2 and v[0] == "'" and v[-1] == "'":
            return v[1:-1]
        return v

    while k < len(lines):
        line = lines[k]
        if line.startswith("  side: "):
            side = unquote(line[len("  side: "):])
        if line == "  squares:":
            in_squares = True
            k += 1
            continue
        if in_squares:
            if line.startswith("  - id: "):
                ids.append(unquote(line[len("  - id: "):]))
                if lines[k + 1] != "    corners:":
                    raise ReadError(f"form C (lines): square {len(ids)} has no corners line")
                pts = []
                for c in range(4):
                    a = lines[k + 2 + 2 * c]
                    b = lines[k + 3 + 2 * c]
                    if not a.startswith("    - - ") or not b.startswith("      - "):
                        raise ReadError(f"form C (lines): square {len(ids)} corner {c + 1} malformed")
                    pts.append([unquote(a[len("    - - "):]), unquote(b[len("      - "):])])
                corners.append(pts)
                k += 10
                continue
            if line.startswith("  ") and not line.startswith("   ") and not line.startswith("  - "):
                in_squares = False
            elif line and not line.startswith(" "):
                in_squares = False
        k += 1
    return {"side": side, "ids": ids, "corners": corners}


def read_center_basis(data: bytes) -> dict[str, Any]:
    """Read a Witness/v2 file in ``center-basis`` form (the house witness on ``main``).

    Used only to compare the house witness with the certificate it stands for; it is
    read with the same node checks, without the line-by-line second reading.
    """
    text = _hygiene(data, "form CB", final_newline=True)
    try:
        docs = list(yaml.compose_all(text, Loader=yaml.SafeLoader))
    except yaml.YAMLError as exc:
        raise ReadError(f"form CB: not YAML ({str(exc)[:200]})") from None
    if len(docs) != 1 or docs[0] is None:
        raise ReadError("form CB: not one document")
    _check_nodes(docs[0], set(), "$")
    top = _build(docs[0])
    w = top["witness"]
    if w.get("representation") != "center-basis":
        raise ReadError(f"form CB: representation {w.get('representation')!r}")
    if w["coordinates"] != {"origin": "lower-left", "axes": "x-right-y-up", "angle_unit": "not-applicable"}:
        raise ReadError(f"form CB: coordinates {w['coordinates']!r}")
    n = w["n"]
    side = parse_scalar(w["side"], "form CB side")
    rows = []
    for k, sq in enumerate(w["squares"], 1):
        if sorted(sq) != ["basis", "center", "id"]:
            raise ReadError(f"form CB: square {k} keys {sorted(sq)}")
        cx, cy = (parse_scalar(v, f"form CB square {k} center") for v in sq["center"])
        c, s = (parse_scalar(v, f"form CB square {k} basis") for v in sq["basis"])
        rows.append((cx, cy, c, s))
    if len(rows) != n:
        raise ReadError(f"form CB: n = {n} stated, {len(rows)} listed")
    return {"form": "CB", "n": n, "side": side, "rows": rows, "witness_id": w.get("id"),
            "top_keys": list(top), "witness_keys": list(w)}


def read_form_c(data: bytes) -> dict[str, Any]:
    """Read a Witness/v2 corner file strictly; return its count, side and corners."""
    text = _hygiene(data, "form C", final_newline=True)
    try:
        docs = list(yaml.compose_all(text, Loader=yaml.SafeLoader))
    except yaml.YAMLError as exc:
        raise ReadError(f"form C: not YAML ({str(exc)[:200]})") from None
    if len(docs) != 1 or docs[0] is None:
        raise ReadError(f"form C: {len(docs)} documents, expected one")
    for token in yaml.scan(text, Loader=yaml.SafeLoader):
        if isinstance(token, (yaml.AnchorToken, yaml.AliasToken, yaml.TagToken, yaml.DirectiveToken)):
            raise ReadError(f"form C: {type(token).__name__} in the file")
    _check_nodes(docs[0], set(), "$")
    top = _build(docs[0])
    if not isinstance(top, dict) or list(top) != ["softschema", "witness"]:
        raise ReadError(f"form C: top-level keys {list(top) if isinstance(top, dict) else top!r}")
    env = top["softschema"]
    if not isinstance(env, dict):
        raise ReadError("form C: softschema is not a mapping")
    if env.get("contract") != "packing.squares:Witness/v2":
        raise ReadError(f"form C: contract {env.get('contract')!r}")
    if env.get("envelope") != "witness":
        raise ReadError(f"form C: envelope {env.get('envelope')!r}")
    if env.get("status") != "enforced":
        raise ReadError(f"form C: status {env.get('status')!r}")
    if sorted(env) != sorted(["contract", "schema", "envelope", "status"]):
        raise ReadError(f"form C: softschema keys {sorted(env)}")
    w = top["witness"]
    if not isinstance(w, dict):
        raise ReadError("form C: witness is not a mapping")
    missing = [k for k in WITNESS_REQUIRED if k not in w]
    extra = [k for k in w if k not in WITNESS_ALLOWED]
    if missing or extra:
        raise ReadError(f"form C: witness keys missing {missing}, not allowed {extra}")
    n = w["n"]
    if type(n) is not int or n < 1:
        raise ReadError(f"form C: n is not a positive integer: {n!r}")
    if w["square_size"] != "1":
        raise ReadError(f"form C: square_size {w['square_size']!r}")
    if w["representation"] != "corners":
        raise ReadError(f"form C: representation {w['representation']!r}")
    if w["scalar"] != {"kind": "rational"}:
        raise ReadError(f"form C: scalar {w['scalar']!r}")
    if w["coordinates"] != {"origin": "lower-left", "axes": "x-right-y-up", "angle_unit": "not-applicable"}:
        raise ReadError(f"form C: coordinates {w['coordinates']!r}")
    claim = w["claim"]
    if not isinstance(claim, dict) or any(k not in CLAIM_ALLOWED for k in claim):
        raise ReadError(f"form C: claim keys {list(claim) if isinstance(claim, dict) else claim!r}")
    for k in ("coordinate_provenance", "method", "limitations"):
        if not isinstance(claim.get(k), str):
            raise ReadError(f"form C: claim.{k} missing or not a string")
    side = parse_scalar(w["side"], "form C side")
    squares = w["squares"]
    if not isinstance(squares, list):
        raise ReadError("form C: squares is not a list")
    if len(squares) != n:
        raise ReadError(f"form C: n = {n} stated, {len(squares)} squares listed")
    id_style = None
    corners: list[tuple[tuple[tuple[int, int], tuple[int, int]], ...]] = []
    raw: list[list[list[str]]] = []
    for k, sq in enumerate(squares, 1):
        if not isinstance(sq, dict) or list(sq) != ["id", "corners"]:
            raise ReadError(f"form C: square {k} keys {list(sq) if isinstance(sq, dict) else sq!r}")
        sid = sq["id"]
        if sid == f"square-{k}":
            style = "square-k"
        elif type(sid) is int and sid == k:
            style = "integer"
        else:
            raise ReadError(f"form C: square {k} has id {sid!r}, out of order")
        if id_style is None:
            id_style = style
        elif style != id_style:
            raise ReadError(f"form C: square {k} id style {style} differs from {id_style}")
        pts = sq["corners"]
        if not isinstance(pts, list) or len(pts) != 4:
            raise ReadError(f"form C: square {k} does not have four corners")
        row = []
        rawrow = []
        for c, pt in enumerate(pts, 1):
            if not isinstance(pt, list) or len(pt) != 2:
                raise ReadError(f"form C: square {k} corner {c} is not a point")
            row.append(tuple(parse_scalar(v, f"form C square {k} corner {c} {'xy'[i]}") for i, v in enumerate(pt)))
            rawrow.append(list(pt))
        corners.append(tuple(row))  # type: ignore[arg-type]
        raw.append(rawrow)
    second = _second_reading(text)
    if second["side"] != w["side"]:
        raise ReadError("form C: the line reading of the side differs from the YAML reading")
    if len(second["corners"]) != n or second["corners"] != raw:
        raise ReadError("form C: the line reading of the corners differs from the YAML reading")
    flags = []
    if not lowest(side):
        flags.append("side not in lowest terms")
    nonlowest = sum(1 for sq in corners for pt in sq for v in pt if not lowest(v))
    if nonlowest:
        flags.append(f"{nonlowest} corner scalars not in lowest terms")
    return {
        "form": "C",
        "n": n,
        "side": side,
        "corners": corners,
        "id_style": id_style,
        "witness_id": w["id"],
        "schema": env.get("schema"),
        "claim": claim,
        "has_source": "source" in w,
        "has_certificate": "certificate" in w,
        "certificate_block": w.get("certificate"),
        "source_block": w.get("source"),
        "flags": flags,
        "scalars": 1 + 8 * n,
    }
