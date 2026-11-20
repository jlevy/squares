"""Lane r1012's reader for an exact Witness/v2 certificate with corners.

Clean room: written for the stage 4 review of issue 1012 from the schema text
(packing/witnesses/witness.schema.yaml) alone. It imports nothing from this
repository or from the source, and it is the only code the two deciding methods
share.

The reader decides the reading and hands on exact rationals: the count, the side,
the square ids, and every square's four corners in the order written, in the
lower-left frame of the box [0, S]^2. It decides nothing about the geometry.
"""

import hashlib
import re
from fractions import Fraction
from math import gcd

import yaml

CONTRACT = "packing.squares:Witness/v2"
ENVELOPE_KEYS = {"contract", "schema", "envelope", "status"}
WITNESS_REQUIRED = {
    "id", "n", "side", "square_size", "representation", "scalar",
    "coordinates", "squares", "claim",
}
WITNESS_OPTIONAL = {"source", "certificate"}
CLAIM_REQUIRED = {"coordinate_provenance", "method", "limitations"}
CLAIM_OPTIONAL = {"precision", "tolerance"}
SOURCE_KEYS = {"key", "path", "url", "retrieved", "revision", "revision_sha256"}
SQUARE_INFO_KEYS = {"center", "angle", "basis"}
ID_PATTERN = re.compile(r"W-[a-z0-9][a-z0-9-]*")

INT_FORM = re.compile(r"-?(?:0|[1-9][0-9]*)")
FRACTION_FORM = re.compile(r"(-?(?:0|[1-9][0-9]*))/([1-9][0-9]*)")
DECIMAL_FORM = re.compile(r"(-?)(0|[1-9][0-9]*)\.([0-9]+)")
STRICT_INT = re.compile(r"0|[1-9][0-9]*")

STR_TAG = "tag:yaml.org,2002:str"
INT_TAG = "tag:yaml.org,2002:int"


class ReadError(Exception):
    """The file is not a certificate this reader can hand on."""


class Other:
    """A YAML value of a type the schema never allows where it appears."""

    def __init__(self, tag, text):
        self.tag = tag
        self.text = text

    def __repr__(self):
        return f"Other({self.tag!r}, {self.text!r})"


def parse_scalar(text, where):
    """Return (value, form, canonical) for an exact rational scalar string."""
    if not isinstance(text, str):
        raise ReadError(f"{where}: a scalar must be a string, found {text!r}")
    m = INT_FORM.fullmatch(text)
    if m:
        return Fraction(int(text)), "integer", text != "-0"
    m = FRACTION_FORM.fullmatch(text)
    if m:
        p, q = int(m.group(1)), int(m.group(2))
        canonical = q != 1 and gcd(p, q) == 1 and m.group(1) != "-0" and p != 0
        return Fraction(p, q), "fraction", canonical
    m = DECIMAL_FORM.fullmatch(text)
    if m:
        sign, whole, frac = m.group(1), m.group(2), m.group(3)
        value = Fraction(int(whole + frac), 10 ** len(frac))
        if sign:
            value = -value
        canonical = not frac.endswith("0") and not (sign and value == 0)
        return value, "decimal", canonical
    raise ReadError(f"{where}: not an exact rational scalar: {text!r}")


def _check_events(text):
    documents = 0
    for event in yaml.parse(text, Loader=yaml.SafeLoader):
        if isinstance(event, yaml.AliasEvent):
            raise ReadError("an alias")
        if getattr(event, "anchor", None) is not None:
            raise ReadError("an anchor")
        if isinstance(event, (yaml.ScalarEvent, yaml.MappingStartEvent,
                              yaml.SequenceStartEvent)) and event.tag is not None:
            raise ReadError(f"an explicit tag {event.tag!r}")
        if isinstance(event, yaml.DocumentStartEvent):
            documents += 1
            if event.version is not None or event.tags:
                raise ReadError("a directive")
    if documents != 1:
        raise ReadError(f"{documents} YAML documents, expected one")


def _convert(node, path):
    if isinstance(node, yaml.MappingNode):
        out = {}
        for key_node, value_node in node.value:
            if not isinstance(key_node, yaml.ScalarNode) or key_node.tag != STR_TAG:
                raise ReadError(f"{path}: a key that is not a string")
            key = key_node.value
            if key in out:
                raise ReadError(f"{path}: the key {key!r} twice")
            out[key] = _convert(value_node, f"{path}.{key}")
        return out
    if isinstance(node, yaml.SequenceNode):
        return [_convert(item, f"{path}[{i}]") for i, item in enumerate(node.value)]
    if isinstance(node, yaml.ScalarNode):
        if node.tag == STR_TAG:
            return node.value
        if node.tag == INT_TAG and STRICT_INT.fullmatch(node.value):
            return int(node.value)
        return Other(node.tag, node.value)
    raise ReadError(f"{path}: an unknown node")


def _keys(mapping, required, optional, where):
    if not isinstance(mapping, dict):
        raise ReadError(f"{where}: not a mapping")
    missing = sorted(required - mapping.keys())
    extra = sorted(mapping.keys() - required - optional)
    if missing:
        raise ReadError(f"{where}: missing {missing}")
    if extra:
        raise ReadError(f"{where}: keys outside the schema {extra}")


def git_blob_id(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def read_bytes(data):
    """Read a certificate from its bytes; raise ReadError or return the packing."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ReadError(f"not UTF-8: {exc}") from None
    try:
        _check_events(text)
        root = yaml.compose(text, Loader=yaml.SafeLoader)
    except yaml.YAMLError as exc:
        raise ReadError(f"not YAML: {exc}") from None
    top = _convert(root, "$")
    if not isinstance(top, dict):
        raise ReadError("the document is not a mapping")
    if "softschema" in top or "witness" in top:
        _keys(top, {"softschema", "witness"}, set(), "$")
        envelope = top["softschema"]
        _keys(envelope, {"contract", "envelope"}, ENVELOPE_KEYS - {"contract", "envelope"},
              "softschema")
        if envelope["contract"] != CONTRACT:
            raise ReadError(f"contract {envelope['contract']!r}")
        if envelope["envelope"] != "witness":
            raise ReadError(f"envelope {envelope['envelope']!r}")
        witness = top["witness"]
        wrapped = True
        envelope_info = {k: envelope[k] if isinstance(envelope[k], str) else repr(envelope[k])
                         for k in sorted(envelope)}
    else:
        witness = top
        wrapped = False
        envelope_info = None
    _keys(witness, WITNESS_REQUIRED, WITNESS_OPTIONAL, "witness")

    n = witness["n"]
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ReadError(f"n is not a positive integer: {n!r}")
    if witness["square_size"] != "1":
        raise ReadError(f"square_size {witness['square_size']!r}")
    if witness["representation"] != "corners":
        raise ReadError(f"representation {witness['representation']!r}")
    scalar = witness["scalar"]
    _keys(scalar, {"kind"}, set(), "scalar")
    if scalar["kind"] != "rational":
        raise ReadError(f"scalar kind {scalar['kind']!r}")
    coords = witness["coordinates"]
    _keys(coords, {"origin", "axes", "angle_unit"}, set(), "coordinates")
    if coords["axes"] != "x-right-y-up":
        raise ReadError(f"axes {coords['axes']!r}")
    if coords["origin"] not in ("lower-left", "container-center"):
        raise ReadError(f"origin {coords['origin']!r}")
    if coords["angle_unit"] not in ("degrees", "radians", "not-applicable"):
        raise ReadError(f"angle_unit {coords['angle_unit']!r}")

    forms = {"integer": 0, "fraction": 0, "decimal": 0}
    noncanonical = []

    def scalar_value(text, where):
        value, form, canonical = parse_scalar(text, where)
        forms[form] += 1
        if not canonical:
            noncanonical.append(where)
        return value

    side = scalar_value(witness["side"], "side")
    if side <= 0:
        raise ReadError("the side is not positive")

    squares = witness["squares"]
    if not isinstance(squares, list):
        raise ReadError("squares is not a sequence")
    if len(squares) != n:
        raise ReadError(f"n is {n} but {len(squares)} squares are listed")
    ids = []
    corners = []
    info_keys = {}
    shift = side / 2 if coords["origin"] == "container-center" else Fraction(0)
    for index, square in enumerate(squares):
        where = f"squares[{index}]"
        _keys(square, {"id", "corners"}, SQUARE_INFO_KEYS, where)
        sid = square["id"]
        if isinstance(sid, bool) or not (
            (isinstance(sid, int) and sid >= 1) or (isinstance(sid, str) and sid)
        ):
            raise ReadError(f"{where}: id {sid!r}")
        if sid in ids:
            raise ReadError(f"{where}: the id {sid!r} twice")
        ids.append(sid)
        for key in sorted(square.keys() & SQUARE_INFO_KEYS):
            info_keys[key] = info_keys.get(key, 0) + 1
        pts = square["corners"]
        if not isinstance(pts, list) or len(pts) != 4:
            raise ReadError(f"{where}: corners is not a list of four points")
        quad = []
        for c, point in enumerate(pts):
            if not isinstance(point, list) or len(point) != 2:
                raise ReadError(f"{where}.corners[{c}]: not a point of two scalars")
            x = scalar_value(point[0], f"{where}.corners[{c}][0]") + shift
            y = scalar_value(point[1], f"{where}.corners[{c}][1]") + shift
            quad.append((x, y))
        corners.append(quad)

    claim = witness["claim"]
    _keys(claim, CLAIM_REQUIRED, CLAIM_OPTIONAL, "claim")
    source = witness.get("source")
    if source is not None:
        _keys(source, {"path"}, SOURCE_KEYS - {"path"}, "source")
    certificate = witness.get("certificate")

    def plain(value):
        if isinstance(value, dict):
            return {k: plain(v) for k, v in value.items()}
        if isinstance(value, list):
            return [plain(v) for v in value]
        if isinstance(value, Other):
            return repr(value)
        return value

    return {
        "n": n,
        "side": side,
        "ids": ids,
        "corners": corners,
        "origin": coords["origin"],
        "angle_unit": coords["angle_unit"],
        "enveloped": wrapped,
        "envelope": envelope_info,
        "witness_id": witness["id"] if isinstance(witness["id"], str) else repr(witness["id"]),
        "witness_id_matches_schema_pattern": isinstance(witness["id"], str)
        and bool(ID_PATTERN.fullmatch(witness["id"])),
        "scalar_forms": forms,
        "scalars": sum(forms.values()),
        "noncanonical": noncanonical,
        "square_info_keys": info_keys,
        "claim": plain(claim),
        "source": plain(source),
        "certificate_keys": sorted(certificate) if isinstance(certificate, dict) else None,
        "text_facts": {
            "bytes": len(data),
            "lines": text.count("\n"),
            "carriage_returns": text.count("\r"),
            "tabs": text.count("\t"),
            "starts_with_bom": text.startswith("﻿"),
        },
    }


def read_path(path):
    with open(path, "rb") as handle:
        data = handle.read()
    packing = read_bytes(data)
    packing["sha256"] = hashlib.sha256(data).hexdigest()
    packing["git_blob"] = git_blob_id(data)
    return packing
