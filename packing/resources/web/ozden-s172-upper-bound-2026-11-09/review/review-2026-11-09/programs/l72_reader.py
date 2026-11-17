"""Strict reader for rational corner Witness/v2 certificates (lane L72, bead think-qqyg).

Written from the Witness/v2 schema text and the certificates' layout read as data. It
imports nothing from the squares repository or the source repositories.

The YAML is composed with PyYAML's BaseLoader, under which every scalar is a string, and
converted to plain Python by this module: anchors and aliases, explicit tags, non-string
keys and duplicate keys are refused. Every coordinate and the side must be an integer or
p/q in canonical decimal form with q > 0. The reader fails closed on any layout it does not
expect, and returns integers only. A JSON twin, read with the standard library's json, must
hold exactly the same witness.
"""

import json
import re

import yaml
from yaml.nodes import MappingNode, ScalarNode, SequenceNode


class ReadError(Exception):
    """The file is refused; the message says why."""


INT_RE = re.compile(r"(0|[1-9][0-9]*)\Z")
RAT_RE = re.compile(r"(0|-?[1-9][0-9]*)(?:/([1-9][0-9]*))?\Z")
ID_RE = re.compile(r"W-[a-z0-9][a-z0-9-]*\Z")

STR_TAG = "tag:yaml.org,2002:str"
SEQ_TAG = "tag:yaml.org,2002:seq"
MAP_TAG = "tag:yaml.org,2002:map"

TOP_KEYS = {"softschema", "witness"}
SOFTSCHEMA_KEYS = {"contract", "schema", "envelope", "status"}
WITNESS_REQUIRED = {
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
WITNESS_ALLOWED = WITNESS_REQUIRED | {"source", "certificate"}
CLAIM_REQUIRED = {"coordinate_provenance", "method", "limitations"}
CLAIM_ALLOWED = CLAIM_REQUIRED | {"precision", "tolerance"}
SOURCE_ALLOWED = {"key", "path", "url", "retrieved", "revision", "revision_sha256"}


def _plain(node, seen):
    """Convert a composed YAML node to str / list / dict, refusing anything else."""
    if id(node) in seen:
        raise ReadError("a node appears twice (anchor and alias)")
    seen.add(id(node))
    if isinstance(node, ScalarNode):
        if node.tag != STR_TAG:
            raise ReadError(f"scalar with explicit tag {node.tag!r}")
        return node.value
    if isinstance(node, SequenceNode):
        if node.tag != SEQ_TAG:
            raise ReadError(f"sequence with explicit tag {node.tag!r}")
        return [_plain(child, seen) for child in node.value]
    if isinstance(node, MappingNode):
        if node.tag != MAP_TAG:
            raise ReadError(f"mapping with explicit tag {node.tag!r}")
        out = {}
        for key_node, value_node in node.value:
            if not isinstance(key_node, ScalarNode) or key_node.tag != STR_TAG:
                raise ReadError("a mapping key that is not a plain string")
            key = key_node.value
            if key in out:
                raise ReadError(f"duplicate key {key!r}")
            out[key] = _plain(value_node, seen)
        return out
    raise ReadError(f"unexpected YAML node {type(node).__name__}")


def yaml_tree(text):
    try:
        root = yaml.compose(text, Loader=yaml.BaseLoader)
    except yaml.YAMLError as exc:
        raise ReadError(f"YAML does not parse: {exc}") from None
    if root is None:
        raise ReadError("empty document")
    return _plain(root, set())


def _no_dup_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ReadError(f"JSON duplicate key {key!r}")
        out[key] = value
    return out


def _refuse_float(text):
    raise ReadError(f"JSON non-integer number {text!r}")


def _refuse_constant(text):
    raise ReadError(f"JSON constant {text!r}")


def _json_plain(value):
    """JSON to the YAML BaseLoader's shape: integers become their decimal strings."""
    if isinstance(value, bool) or value is None:
        raise ReadError(f"JSON value {value!r} has no YAML string twin")
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return [_json_plain(v) for v in value]
    if isinstance(value, dict):
        return {k: _json_plain(v) for k, v in value.items()}
    raise ReadError(f"JSON value of type {type(value).__name__}")


def json_tree(text):
    try:
        value = json.loads(
            text,
            object_pairs_hook=_no_dup_pairs,
            parse_float=_refuse_float,
            parse_constant=_refuse_constant,
        )
    except json.JSONDecodeError as exc:
        raise ReadError(f"JSON does not parse: {exc}") from None
    return _json_plain(value)


def _first_difference(a, b, path="$"):
    if type(a) is not type(b):
        return f"{path}: {type(a).__name__} against {type(b).__name__}"
    if isinstance(a, dict):
        if set(a) != set(b):
            return f"{path}: keys {sorted(set(a) ^ set(b))} differ"
        for k in a:
            d = _first_difference(a[k], b[k], f"{path}.{k}")
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return f"{path}: lengths {len(a)} and {len(b)}"
        for i, (x, y) in enumerate(zip(a, b)):
            d = _first_difference(x, y, f"{path}[{i}]")
            if d:
                return d
        return None
    if a != b:
        return f"{path}: {a[:40]!r} against {b[:40]!r}"
    return None


def _rational(text, what):
    if not isinstance(text, str):
        raise ReadError(f"{what}: not a scalar")
    m = RAT_RE.match(text)
    if not m:
        raise ReadError(f"{what}: {text[:60]!r} is not an integer or p/q")
    num = int(m.group(1))
    den = int(m.group(2)) if m.group(2) is not None else 1
    return num, den


def _need(cond, message):
    if not cond:
        raise ReadError(message)


def validate(tree):
    """Validate the plain tree; return the witness as integers plus metadata."""
    _need(isinstance(tree, dict), "top level is not a mapping")
    _need(set(tree) == TOP_KEYS, f"top-level keys {sorted(tree)} are not {sorted(TOP_KEYS)}")
    soft = tree["softschema"]
    _need(isinstance(soft, dict), "softschema is not a mapping")
    _need(set(soft) <= SOFTSCHEMA_KEYS, f"softschema keys {sorted(soft)}")
    _need(soft.get("contract") == "packing.squares:Witness/v2", "contract is not Witness/v2")
    _need(soft.get("envelope") == "witness", "envelope is not 'witness'")
    w = tree["witness"]
    _need(isinstance(w, dict), "witness is not a mapping")
    missing = WITNESS_REQUIRED - set(w)
    _need(not missing, f"witness lacks {sorted(missing)}")
    extra = set(w) - WITNESS_ALLOWED
    _need(not extra, f"witness has unknown keys {sorted(extra)}")
    _need(isinstance(w["id"], str) and ID_RE.match(w["id"]), "witness id is malformed")
    _need(isinstance(w["n"], str) and INT_RE.match(w["n"]), "n is not a decimal integer")
    n = int(w["n"])
    _need(n >= 1, "n < 1")
    side = _rational(w["side"], "side")
    _need(side[0] > 0, "side is not positive")
    _need(w["square_size"] == "1", "square_size is not '1'")
    _need(w["representation"] == "corners", "representation is not 'corners'")
    _need(w["scalar"] == {"kind": "rational"}, "scalar is not exactly {kind: rational}")
    coords = w["coordinates"]
    _need(isinstance(coords, dict), "coordinates is not a mapping")
    _need(set(coords) == {"origin", "axes", "angle_unit"}, f"coordinates keys {sorted(coords)}")
    _need(coords["origin"] == "lower-left", "origin is not lower-left")
    _need(coords["axes"] == "x-right-y-up", "axes are not x-right-y-up")
    _need(
        coords["angle_unit"] in ("degrees", "radians", "not-applicable"),
        "angle_unit is not in the schema's enum",
    )
    claim = w["claim"]
    _need(isinstance(claim, dict), "claim is not a mapping")
    _need(CLAIM_REQUIRED <= set(claim) <= CLAIM_ALLOWED, f"claim keys {sorted(claim)}")
    source = w.get("source")
    if source is not None:
        _need(isinstance(source, dict) and "path" in source, "source lacks path")
        _need(set(source) <= SOURCE_ALLOWED, f"source keys {sorted(source)}")
    cert = w.get("certificate")
    if cert is not None:
        _need(isinstance(cert, dict), "certificate is not a mapping")
    squares = w["squares"]
    _need(isinstance(squares, list), "squares is not a sequence")
    _need(len(squares) == n, f"{len(squares)} squares where n is {n}")
    ids = []
    corners = []
    not_lowest = 0
    from math import gcd

    if gcd(*side) != 1:
        not_lowest += 1
    for k, sq in enumerate(squares):
        where = f"squares[{k}]"
        _need(isinstance(sq, dict), f"{where} is not a mapping")
        _need(set(sq) == {"id", "corners"}, f"{where} keys {sorted(sq)} are not id, corners")
        sid = sq["id"]
        _need(isinstance(sid, str) and INT_RE.match(sid), f"{where} id is not an integer")
        sid = int(sid)
        _need(sid >= 1, f"{where} id < 1")
        ids.append(sid)
        cs = sq["corners"]
        _need(isinstance(cs, list) and len(cs) == 4, f"{where} does not have 4 corners")
        pts = []
        for j, p in enumerate(cs):
            _need(isinstance(p, list) and len(p) == 2, f"{where} corner {j} is not a pair")
            xn, xd = _rational(p[0], f"{where} corner {j} x")
            yn, yd = _rational(p[1], f"{where} corner {j} y")
            if gcd(xn, xd) != 1:
                not_lowest += 1
            if gcd(yn, yd) != 1:
                not_lowest += 1
            pts.append((xn, xd, yn, yd))
        corners.append(tuple(pts))
    _need(len(set(ids)) == n, "repeated square id")
    meta = {
        "witness_id": w["id"],
        "softschema": dict(soft),
        "angle_unit": coords["angle_unit"],
        "ids_in_order": ids == list(range(1, n + 1)),
        "scalars": 1 + 8 * n,
        "scalars_not_in_lowest_terms": not_lowest,
        "claim": dict(claim) if isinstance(claim, dict) else None,
        "source": dict(source) if isinstance(source, dict) else None,
        "certificate": dict(cert) if isinstance(cert, dict) else None,
    }
    return {"n": n, "side": side, "ids": ids, "corners": corners, "meta": meta}


def read_texts(yaml_text, json_text=None):
    """Read a certificate from its texts; the JSON twin, when given, must match exactly."""
    tree = yaml_tree(yaml_text)
    out = validate(tree)
    out["meta"]["yaml_ascii"] = yaml_text.isascii()
    if json_text is not None:
        jt = json_tree(json_text)
        diff = _first_difference(tree, jt)
        if diff:
            raise ReadError(f"JSON twin differs from the YAML: {diff}")
        out["meta"]["json_twin"] = "same witness"
        out["meta"]["json_ends_with_newline"] = json_text.endswith("\n")
    return out


def read_files(yaml_path, json_path=None):
    with open(yaml_path, "rb") as fh:
        ydata = fh.read()
    try:
        ytext = ydata.decode("utf-8")
    except UnicodeDecodeError:
        raise ReadError("YAML is not UTF-8") from None
    jtext = None
    if json_path is not None:
        with open(json_path, "rb") as fh:
            jdata = fh.read()
        try:
            jtext = jdata.decode("utf-8")
        except UnicodeDecodeError:
            raise ReadError("JSON is not UTF-8") from None
    return read_texts(ytext, jtext)
