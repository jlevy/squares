"""Strict readers for the three file forms this review decides.

Lane R1 (c-review-1005-1117), stage 4 review of issues #1005, #1006 and #1007.
Clean-room: written for this review from the schema text of
packing/witnesses/witness.schema.yaml, the three issues and the shape of the files.
It imports nothing from this repository or from the sources.

Forms:

* ``witness-yaml``: a softschema envelope around a Witness/v2 record with
  ``representation: corners`` and ``scalar.kind: rational`` (YAML text).
* ``witness-json``: the same record as JSON text.
* ``centre-json``: de Winter's ``nNNN_exact.json``: ``n``, ``side``,
  ``square_size``, ``format`` and ``squares``, each square
  ``[center_x, center_y, cos, sin]``.

Every reader hands back exact rationals (``fractions.Fraction``) in the file's own
terms and derives nothing: corners stay corners, centres and directions stay centres
and directions.  A file that is not exactly what the reader analysed is refused.
"""

from __future__ import annotations

import json
import re
from fractions import Fraction
from math import gcd

import yaml

FORMAT_SENTENCE = (
    "each square: [center_x, center_y, cos, sin] as exact rationals; "
    "(cos, sin) is the unit direction of one edge"
)
CONTRACT = "packing.squares:Witness/v2"
SCALAR_RE = re.compile(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?")
PLAIN_INT_RE = re.compile(r"0|[1-9][0-9]*")
WITNESS_ID_RE = re.compile(r"W-[a-z0-9][a-z0-9-]*")
MAX_SCALAR_CHARS = 4000  # below CPython's 4300-digit conversion limit, stated not inherited

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
WITNESS_REQUIRED = WITNESS_KEYS[:9]
STR_TAG = "tag:yaml.org,2002:str"
INT_TAG = "tag:yaml.org,2002:int"


class Refusal(Exception):
    """The file is not a document this reader analysed."""


class Packing:
    """What a reader hands on: exact values in the file's own terms."""

    def __init__(self, form, n, side, squares, ids, notes):
        self.form = form  # "corners" or "centre"
        self.n = n
        self.side = side  # Fraction
        self.squares = squares  # corners: ((x, y) * 4); centre: (cx, cy, ux, uy)
        self.ids = ids
        self.notes = notes  # everything recorded and not required


def parse_scalar(text, where):
    """A rational written ``p`` or ``p/q``; returns (Fraction, written in lowest terms)."""
    if not isinstance(text, str):
        raise Refusal(f"{where}: a scalar must be a string, found {type(text).__name__}")
    if len(text) > MAX_SCALAR_CHARS:
        raise Refusal(f"{where}: scalar longer than {MAX_SCALAR_CHARS} characters")
    if SCALAR_RE.fullmatch(text) is None:
        raise Refusal(f"{where}: not a rational scalar: {text[:60]!r}")
    if text == "-0" or text.startswith("-0/"):
        raise Refusal(f"{where}: negative zero")
    if "/" in text:
        p_text, q_text = text.split("/")
        p, q = int(p_text), int(q_text)
        canonical = q != 1 and gcd(abs(p), q) == 1
    else:
        p, q = int(text), 1
        canonical = True
    return Fraction(p, q), canonical


# ---------------------------------------------------------------- YAML text


class _Plain(str):
    """A plain (unquoted) YAML scalar, kept apart from a quoted one."""


def _yaml_tree(text):
    """One block-style YAML document as dicts, lists, strings and integers.

    Built from the parser's events, not from PyYAML's constructors.  Refused: more than
    one document, directives, anchors, aliases, explicit tags, flow collections,
    scalars that are neither plain nor single-quoted, keys that are not plain
    scalars, duplicate keys, and plain scalars that YAML 1.1 resolves to anything
    but a string or a plain decimal integer.
    """
    try:
        events = list(yaml.parse(text, Loader=yaml.SafeLoader))
    except yaml.YAMLError as exc:
        raise Refusal(f"YAML syntax: {str(exc).splitlines()[0]}") from exc
    resolver = yaml.resolver.Resolver()
    spans = {}
    pos = 0

    def take():
        nonlocal pos
        ev = events[pos]
        pos += 1
        return ev

    def check_plain_meta(ev, what):
        if getattr(ev, "anchor", None) is not None:
            raise Refusal(f"line {ev.start_mark.line + 1}: anchor on {what}")
        if getattr(ev, "tag", None) is not None:
            raise Refusal(f"line {ev.start_mark.line + 1}: explicit tag on {what}")

    def node(path):
        ev = take()
        line = ev.start_mark.line + 1
        if isinstance(ev, yaml.AliasEvent):
            raise Refusal(f"line {line}: alias")
        if isinstance(ev, yaml.ScalarEvent):
            check_plain_meta(ev, "scalar")
            if ev.style is None:
                tag = resolver.resolve(yaml.ScalarNode, ev.value, (True, False))
                if tag == STR_TAG:
                    value = _Plain(ev.value)
                elif tag == INT_TAG and PLAIN_INT_RE.fullmatch(ev.value):
                    value = int(ev.value)
                else:
                    raise Refusal(
                        f"line {line}: plain scalar {ev.value[:40]!r} resolves to "
                        f"{tag.rsplit(':', 1)[-1]}, neither a string nor a plain integer"
                    )
            elif ev.style == "'":
                value = ev.value
            else:
                raise Refusal(f"line {line}: scalar style {ev.style!r} not analysed")
            spans[path] = (line, ev.end_mark.line + 1)
            return value
        if isinstance(ev, yaml.SequenceStartEvent):
            check_plain_meta(ev, "sequence")
            if ev.flow_style:
                raise Refusal(f"line {line}: flow sequence")
            items = []
            while not isinstance(events[pos], yaml.SequenceEndEvent):
                items.append(node(path + (len(items),)))
            end = take()
            spans[path] = (line, end.end_mark.line + 1)
            return items
        if isinstance(ev, yaml.MappingStartEvent):
            check_plain_meta(ev, "mapping")
            if ev.flow_style:
                raise Refusal(f"line {line}: flow mapping")
            mapping = {}
            while not isinstance(events[pos], yaml.MappingEndEvent):
                kev = take()
                kline = kev.start_mark.line + 1
                if not isinstance(kev, yaml.ScalarEvent) or kev.style is not None:
                    raise Refusal(f"line {kline}: key is not a plain scalar")
                check_plain_meta(kev, "key")
                key = kev.value
                if key in mapping:
                    raise Refusal(f"line {kline}: duplicate key {key!r}")
                mapping[key] = node(path + (key,))
            end = take()
            spans[path] = (line, end.end_mark.line + 1)
            return mapping
        raise Refusal(f"line {line}: unexpected {type(ev).__name__}")

    ev = take()
    if not isinstance(ev, yaml.StreamStartEvent):
        raise Refusal("no stream start")
    ev = take()
    if not isinstance(ev, yaml.DocumentStartEvent):
        raise Refusal("empty stream")
    if ev.version is not None or ev.tags:
        raise Refusal("YAML directives")
    tree = node(())
    ev = take()
    if not isinstance(ev, yaml.DocumentEndEvent):
        raise Refusal("document does not end where its node ends")
    ev = take()
    if not isinstance(ev, yaml.StreamEndEvent):
        raise Refusal("more than one YAML document")
    return tree, spans


def _decode(raw, where, *, yaml_text):
    if raw.startswith(b"\xef\xbb\xbf"):
        raise Refusal(f"{where}: byte-order mark")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Refusal(f"{where}: not UTF-8") from exc
    if yaml_text:
        for ch, name in (("\t", "tab"), ("\r", "carriage return"), ("\x00", "NUL")):
            if ch in text:
                raise Refusal(f"{where}: contains a {name}")
    return text


# ---------------------------------------------------------------- JSON text


def _json_tree(text):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise Refusal(f"duplicate key {key!r}")
            out[key] = value
        return out

    def no_float(token):
        raise Refusal(f"a JSON number that is not an integer: {token[:40]}")

    def no_constant(token):
        raise Refusal(f"JSON constant {token}")

    try:
        tree = json.loads(
            text, object_pairs_hook=pairs, parse_float=no_float, parse_constant=no_constant
        )
    except json.JSONDecodeError as exc:
        raise Refusal(f"JSON syntax: {exc.msg} at line {exc.lineno}") from exc
    except ValueError as exc:  # CPython's integer conversion limit
        raise Refusal(f"JSON integer not convertible: {exc}") from exc

    def walk(value, path):
        if isinstance(value, bool) or value is None:
            raise Refusal(f"{path}: JSON {value!r} where a string or integer is required")
        if isinstance(value, dict):
            for key, item in value.items():
                walk(item, f"{path}.{key}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                walk(item, f"{path}[{index}]")
        elif not isinstance(value, (str, int)):
            raise Refusal(f"{path}: unexpected {type(value).__name__}")

    walk(tree, "$")
    return tree


# ---------------------------------------------------------------- Witness/v2


def _need_dict(value, where, *, exactly=None, required=(), allowed=None):
    if not isinstance(value, dict):
        raise Refusal(f"{where}: not a mapping")
    keys = list(value)
    if exactly is not None and sorted(keys) != sorted(exactly):
        raise Refusal(f"{where}: keys {keys} are not exactly {list(exactly)}")
    for key in required:
        if key not in value:
            raise Refusal(f"{where}: required key {key!r} missing")
    if allowed is not None:
        for key in keys:
            if key not in allowed:
                raise Refusal(f"{where}: key {key!r} is not in the schema")
    return value


def _witness_from_tree(tree, form_name):
    top = _need_dict(tree, "document", exactly=("softschema", "witness"))
    soft = _need_dict(top["softschema"], "softschema", required=("contract", "envelope"))
    if soft["contract"] != CONTRACT:
        raise Refusal(f"softschema.contract is {soft['contract']!r}")
    if soft["envelope"] != "witness":
        raise Refusal(f"softschema.envelope is {soft['envelope']!r}")
    wit = _need_dict(
        top["witness"], "witness", required=WITNESS_REQUIRED, allowed=WITNESS_KEYS
    )
    notes = {
        "form": form_name,
        "softschema": {k: soft[k] for k in soft},
        "witness_id": wit["id"],
        "witness_id_matches_schema_pattern": isinstance(wit["id"], str)
        and WITNESS_ID_RE.fullmatch(wit["id"]) is not None,
    }
    n = wit["n"]
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise Refusal(f"witness.n is {n!r}, not an integer of at least 1")
    side, side_canonical = parse_scalar(wit["side"], "witness.side")
    if wit["square_size"] != "1":
        raise Refusal(f"witness.square_size is {wit['square_size']!r}, not the string '1'")
    if wit["representation"] != "corners":
        raise Refusal(f"witness.representation is {wit['representation']!r}, not corners")
    scalar = _need_dict(wit["scalar"], "witness.scalar", exactly=("kind",))
    if scalar["kind"] != "rational":
        raise Refusal(f"witness.scalar.kind is {scalar['kind']!r}, not rational")
    coords = _need_dict(
        wit["coordinates"], "witness.coordinates", exactly=("origin", "axes", "angle_unit")
    )
    if coords["origin"] != "lower-left":
        raise Refusal(f"witness.coordinates.origin is {coords['origin']!r}")
    if coords["axes"] != "x-right-y-up":
        raise Refusal(f"witness.coordinates.axes is {coords['axes']!r}")
    if coords["angle_unit"] not in ("degrees", "radians", "not-applicable"):
        raise Refusal(f"witness.coordinates.angle_unit is {coords['angle_unit']!r}")
    notes["angle_unit"] = coords["angle_unit"]
    claim = _need_dict(wit["claim"], "witness.claim")
    notes["claim"] = {k: claim[k] for k in claim}
    for key in ("source", "certificate"):
        if key in wit:
            block = _need_dict(wit[key], f"witness.{key}")
            notes[key] = {k: block[k] for k in block}
    listed = wit["squares"]
    if not isinstance(listed, list):
        raise Refusal("witness.squares: not a sequence")
    if len(listed) != n:
        raise Refusal(f"witness.n states {n} squares and {len(listed)} are listed")
    squares, ids = [], []
    canonical_scalars = int(side_canonical)
    total_scalars = 1
    integer_scalars = 0
    for index, entry in enumerate(listed, start=1):
        where = f"witness.squares[{index}]"
        entry = _need_dict(entry, where, exactly=("id", "corners"))
        ident = entry["id"]
        if isinstance(ident, bool) or not (
            (isinstance(ident, int) and ident >= 1) or (isinstance(ident, str) and ident)
        ):
            raise Refusal(f"{where}.id is {ident!r}")
        ids.append(ident)
        corners = entry["corners"]
        if not isinstance(corners, list) or len(corners) != 4:
            raise Refusal(f"{where}.corners: not a sequence of four points")
        points = []
        for cindex, point in enumerate(corners):
            if not isinstance(point, list) or len(point) != 2:
                raise Refusal(f"{where}.corners[{cindex}]: not a point of two scalars")
            pair = []
            for axis, item in zip("xy", point):
                if isinstance(item, int):
                    raise Refusal(
                        f"{where}.corners[{cindex}].{axis}: an integer where the schema "
                        "requires a string scalar"
                    )
                value, canonical = parse_scalar(item, f"{where}.corners[{cindex}].{axis}")
                total_scalars += 1
                canonical_scalars += int(canonical)
                integer_scalars += int("/" not in item)
                pair.append(value)
            points.append((pair[0], pair[1]))
        squares.append(tuple(points))
    if len(set(map(repr, ids))) != len(ids):
        raise Refusal("witness.squares: duplicate square ids")
    if ids == list(range(1, n + 1)):
        id_form = "integers 1 to n in order"
    elif ids == [f"square-{k}" for k in range(1, n + 1)]:
        id_form = "strings square-1 to square-n in order"
    else:
        id_form = "other distinct ids"
    notes.update(
        id_form=id_form,
        side_written_in_lowest_terms=side_canonical,
        scalars=total_scalars,
        scalars_in_lowest_terms=canonical_scalars,
        corner_scalars_written_as_integers=integer_scalars,
    )
    return Packing("corners", n, side, squares, ids, notes)


def _lexical_twin(text, packing):
    """A second, line-level reading of the corner scalars, compared with the first.

    Every line that is exactly a corner scalar (``- - X`` or ``  - X`` under a square's
    ``corners:``) is taken in order with a regular expression; the sequence must equal
    the composed one, 8n values.  It shares no parser with the event walk.
    """
    token = re.compile(r"    (?:- - |  - )('?)(-?[0-9]+(?:/[0-9]+)?)\1")
    found = []
    for line in text.split("\n"):
        match = token.fullmatch(line)
        if match is not None:
            text_value = match.group(2)
            if "/" in text_value:
                p_text, q_text = text_value.split("/")
                found.append(Fraction(int(p_text), int(q_text)))
            else:
                found.append(Fraction(int(text_value)))
    composed = [value for square in packing.squares for point in square for value in point]
    if found != composed:
        raise Refusal(
            f"line-level reading finds {len(found)} corner scalars that do not equal "
            f"the {len(composed)} composed ones in order"
        )
    return len(found)


def read_witness_yaml(raw, where="file"):
    text = _decode(raw, where, yaml_text=True)
    tree, spans = _yaml_tree(text)
    packing = _witness_from_tree(tree, "witness-yaml")
    packing.notes["lexical_twin_scalars"] = _lexical_twin(text, packing)
    packing.notes["ends_with_newline"] = text.endswith("\n")
    packing.spans = spans
    packing.text = text
    return packing


def read_witness_json(raw, where="file"):
    text = _decode(raw, where, yaml_text=False)
    packing = _witness_from_tree(_json_tree(text), "witness-json")
    packing.text = text
    return packing


def read_centre_json(raw, where="file"):
    text = _decode(raw, where, yaml_text=False)
    tree = _json_tree(text)
    top = _need_dict(tree, "document", exactly=("n", "side", "square_size", "format", "squares"))
    n = top["n"]
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise Refusal(f"n is {n!r}, not an integer of at least 1")
    side, side_canonical = parse_scalar(top["side"], "side")
    if top["square_size"] != "1":
        raise Refusal(f"square_size is {top['square_size']!r}, not the string '1'")
    if top["format"] != FORMAT_SENTENCE:
        raise Refusal(f"format sentence not the one analysed: {str(top['format'])[:80]!r}")
    listed = top["squares"]
    if not isinstance(listed, list):
        raise Refusal("squares: not an array")
    if len(listed) != n:
        raise Refusal(f"n states {n} squares and {len(listed)} are listed")
    squares = []
    canonical_scalars = int(side_canonical)
    total_scalars = 1
    integer_scalars = 0
    for index, entry in enumerate(listed, start=1):
        if not isinstance(entry, list) or len(entry) != 4:
            raise Refusal(f"squares[{index}]: not an array of four scalars")
        values = []
        for name, item in zip(("center_x", "center_y", "cos", "sin"), entry):
            value, canonical = parse_scalar(item, f"squares[{index}].{name}")
            total_scalars += 1
            canonical_scalars += int(canonical)
            integer_scalars += int("/" not in item)
            values.append(value)
        squares.append(tuple(values))
    notes = {
        "form": "centre-json",
        "format": top["format"],
        "id_form": "none; squares are numbered by position",
        "side_written_in_lowest_terms": side_canonical,
        "scalars": total_scalars,
        "scalars_in_lowest_terms": canonical_scalars,
        "scalars_written_as_integers": integer_scalars,
    }
    packing = Packing("centre", n, side, squares, list(range(1, n + 1)), notes)
    packing.text = text
    return packing


READERS = {
    "witness-yaml": read_witness_yaml,
    "witness-json": read_witness_json,
    "centre-json": read_centre_json,
}


def read_file(path, form):
    with open(path, "rb") as handle:
        raw = handle.read()
    return READERS[form](raw, where=str(path)), raw


# ---------------------------------------------------------------- writers


def scalar_text(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def write_witness_yaml(n, side, squares, ids=None, witness_id="W-r1-control"):
    """A corners packing as Witness/v2 YAML text, in the block style of the sources."""
    ids = list(range(1, len(squares) + 1)) if ids is None else ids
    out = [
        "softschema:",
        f"  contract: {CONTRACT}",
        "  schema: witness.schema.yaml",
        "  envelope: witness",
        "  status: enforced",
        "witness:",
        f"  id: {witness_id}",
        f"  n: {n}",
        f"  side: {_yaml_scalar(side)}",
        "  square_size: '1'",
        "  representation: corners",
        "  scalar:",
        "    kind: rational",
        "  coordinates:",
        "    origin: lower-left",
        "    axes: x-right-y-up",
        "    angle_unit: not-applicable",
        "  squares:",
    ]
    for ident, corners in zip(ids, squares):
        out.append(f"  - id: {ident}")
        out.append("    corners:")
        for x, y in corners:
            out.append(f"    - - {_yaml_scalar(x)}")
            out.append(f"      - {_yaml_scalar(y)}")
    out += [
        "  claim:",
        "    coordinate_provenance: reported",
        "    method: exact-algebraic",
        "    limitations: A control file written by lane R1; it is not a certificate.",
    ]
    return ("\n".join(out) + "\n").encode()


def _yaml_scalar(value):
    text = scalar_text(value)
    return text if "/" in text else f"'{text}'"


def write_witness_json(n, side, squares, ids=None, witness_id="W-r1-control"):
    ids = list(range(1, len(squares) + 1)) if ids is None else ids
    tree = {
        "softschema": {
            "contract": CONTRACT,
            "schema": "witness.schema.yaml",
            "envelope": "witness",
            "status": "enforced",
        },
        "witness": {
            "id": witness_id,
            "n": n,
            "side": scalar_text(side),
            "square_size": "1",
            "representation": "corners",
            "scalar": {"kind": "rational"},
            "coordinates": {
                "origin": "lower-left",
                "axes": "x-right-y-up",
                "angle_unit": "not-applicable",
            },
            "squares": [
                {
                    "id": ident,
                    "corners": [[scalar_text(x), scalar_text(y)] for x, y in corners],
                }
                for ident, corners in zip(ids, squares)
            ],
            "claim": {
                "coordinate_provenance": "reported",
                "method": "exact-algebraic",
                "limitations": "A control file written by lane R1; it is not a certificate.",
            },
        },
    }
    return (json.dumps(tree, indent=2) + "\n").encode()


def write_centre_json(n, side, squares):
    tree = {
        "n": n,
        "side": scalar_text(side),
        "square_size": "1",
        "format": FORMAT_SENTENCE,
        "squares": [[scalar_text(v) for v in square] for square in squares],
    }
    return (json.dumps(tree, indent=0) + "\n").encode()


WRITERS = {
    "witness-yaml": write_witness_yaml,
    "witness-json": write_witness_json,
    "centre-json": write_centre_json,
}
