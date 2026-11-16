"""Lane L180 reader: de Winter's center-basis JSON and its Witness/v2 corners twin.

Written for the blind stage 4 review of issue #996 as a clean-room implementation.
It imports nothing from this repository or the source, and reuses no code of any
earlier review.

The reader decides three things and hands both methods exact rationals:

1. the JSON certificate: exactly the keys ``n``, ``side``, ``square_size``, ``format``
   and ``squares``; ``n`` an integer; ``square_size`` the string ``"1"``; ``squares`` a
   list of ``n`` entries ``[center_x, center_y, cos, sin]``; every scalar a canonical
   ``p`` or ``p/q`` string (``q >= 2``, lowest terms, no sign on zero, no leading zero);
   no floats, constants or duplicate keys;
2. the Witness/v2 twin: a single YAML document with no anchors, aliases or explicit
   tags, no duplicate keys, only strings, plain decimal integers, mappings and
   sequences; the envelope and the keys the schema allows; ``representation: corners``,
   ``scalar.kind: rational``, ``origin: lower-left``, ``axes: x-right-y-up``; ``n``
   squares, ids ``square-1`` to ``square-n`` in order, each with four corners of two
   canonical scalars;
3. the twin agrees with the JSON: the same ``n``, the same side, and for every square
   the four corners ``C + (e1 u + e2 v) / 2`` of the JSON pose, listed as a cyclic
   rotation of them in either sense.

``json_corners`` is the one place a JSON pose is turned into corners; method B is
handed corners and nothing else.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import Any

import yaml

CANONICAL = re.compile(r"(0|-?[1-9][0-9]*)(?:/([1-9][0-9]*))?")
PLAIN_INT = re.compile(r"0|-?[1-9][0-9]*")

JSON_KEYS = ("n", "side", "square_size", "format", "squares")
ENVELOPE_KEYS = {"contract", "schema", "envelope", "status"}
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
PROVENANCE = {"reported", "numerically-checked", "verified"}
METHODS = {"numerical-f64", "numerical-multiprecision", "interval-certified", "exact-algebraic"}
ANGLE_UNITS = {"degrees", "radians", "not-applicable"}
WITNESS_ID = re.compile(r"W-[a-z0-9][a-z0-9-]*")

STR_TAG = "tag:yaml.org,2002:str"
INT_TAG = "tag:yaml.org,2002:int"


class ReadError(ValueError):
    """The text is not a certificate this reader accepts."""


@dataclass(frozen=True)
class Pose:
    """One square of the JSON form: centre and the unit direction of one edge."""

    x: Fraction
    y: Fraction
    c: Fraction
    s: Fraction


@dataclass(frozen=True)
class Reading:
    """A JSON certificate read strictly."""

    n: int
    side: Fraction
    side_text: str
    format_text: str
    poses: tuple[Pose, ...]


Point = tuple[Fraction, Fraction]


@dataclass(frozen=True)
class TwinReading:
    """A Witness/v2 corners file read strictly."""

    n: int
    side: Fraction
    side_text: str
    ids: tuple[str, ...]
    corners: tuple[tuple[Point, Point, Point, Point], ...]
    envelope: dict[str, str]
    header: dict[str, Any]


def scalar(text: object) -> Fraction:
    """One canonical rational scalar, or ReadError."""
    if type(text) is not str:
        raise ReadError(f"scalar is not a string: {text!r}")
    m = CANONICAL.fullmatch(text)
    if m is None:
        raise ReadError(f"scalar is not canonical p or p/q: {text!r}")
    p = int(m.group(1))
    if m.group(2) is None:
        return Fraction(p)
    q = int(m.group(2))
    if q < 2:
        raise ReadError(f"scalar has denominator 1: {text!r}")
    if p == 0:
        raise ReadError(f"zero written with a denominator: {text!r}")
    if gcd(abs(p), q) != 1:
        raise ReadError(f"scalar not in lowest terms: {text!r}")
    return Fraction(p, q)


def write_scalar(v: Fraction) -> str:
    """The canonical text of a rational, the inverse of ``scalar``."""
    if v.denominator == 1:
        return str(v.numerator)
    return f"{v.numerator}/{v.denominator}"


# ----------------------------------------------------------------------------- JSON


def _no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in pairs:
        if k in out:
            raise ReadError(f"duplicate JSON key: {k!r}")
        out[k] = v
    return out


def _refuse_float(text: str) -> Any:
    raise ReadError(f"JSON float: {text!r}")


def _refuse_constant(text: str) -> Any:
    raise ReadError(f"JSON constant: {text!r}")


def _decode(data: bytes) -> str:
    if data.startswith(b"\xef\xbb\xbf"):
        raise ReadError("byte-order mark")
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise ReadError(f"not UTF-8: {exc}") from exc
    if "\t" in text or "\r" in text:
        raise ReadError("tab or carriage return in the text")
    return text


def read_json_text(data: bytes) -> Reading:
    """Read the center-basis JSON certificate strictly."""
    text = _decode(data)
    try:
        obj = json.loads(
            text,
            object_pairs_hook=_no_duplicates,
            parse_float=_refuse_float,
            parse_constant=_refuse_constant,
        )
    except json.JSONDecodeError as exc:
        raise ReadError(f"not JSON: {exc}") from exc
    if type(obj) is not dict:
        raise ReadError("top level is not an object")
    if tuple(sorted(obj)) != tuple(sorted(JSON_KEYS)):
        raise ReadError(f"keys are {sorted(obj)}, not {sorted(JSON_KEYS)}")
    n = obj["n"]
    if type(n) is not int or n < 1:
        raise ReadError(f"n is not a positive integer: {n!r}")
    side = scalar(obj["side"])
    if side <= 0:
        raise ReadError("side is not positive")
    if obj["square_size"] != "1":
        raise ReadError(f"square_size is not '1': {obj['square_size']!r}")
    fmt = obj["format"]
    if type(fmt) is not str:
        raise ReadError("format is not a string")
    rows = obj["squares"]
    if type(rows) is not list:
        raise ReadError("squares is not a list")
    if len(rows) != n:
        raise ReadError(f"n is {n} but squares has {len(rows)} entries")
    poses: list[Pose] = []
    for k, row in enumerate(rows, start=1):
        if type(row) is not list or len(row) != 4:
            raise ReadError(f"square {k} is not a list of four scalars")
        x, y, c, s = (scalar(t) for t in row)
        poses.append(Pose(x, y, c, s))
    return Reading(n=n, side=side, side_text=obj["side"], format_text=fmt, poses=tuple(poses))


def write_json_text(r: Reading) -> bytes:
    """Write a reading back as JSON text of the same layout (for the controls)."""
    obj = {
        "n": r.n,
        "side": write_scalar(r.side),
        "square_size": "1",
        "format": r.format_text,
        "squares": [[write_scalar(p.x), write_scalar(p.y), write_scalar(p.c), write_scalar(p.s)] for p in r.poses],
    }
    return json.dumps(obj, indent=0).encode("ascii")


# ----------------------------------------------------------------------------- YAML


def _check_events(text: str) -> None:
    docs = 0
    for ev in yaml.parse(text, Loader=yaml.SafeLoader):
        if isinstance(ev, yaml.AliasEvent):
            raise ReadError("YAML alias")
        anchor = getattr(ev, "anchor", None)
        if anchor is not None:
            raise ReadError(f"YAML anchor {anchor!r}")
        tag = getattr(ev, "tag", None)
        if tag is not None:
            raise ReadError(f"explicit YAML tag {tag!r}")
        if isinstance(ev, yaml.DocumentStartEvent):
            docs += 1
    if docs != 1:
        raise ReadError(f"{docs} YAML documents, not one")


def _plain(node: yaml.Node) -> Any:
    """Convert a composed node tree, refusing every type but str, int, map and list."""
    if isinstance(node, yaml.MappingNode):
        out: dict[str, Any] = {}
        for knode, vnode in node.value:
            if not isinstance(knode, yaml.ScalarNode) or knode.tag != STR_TAG:
                raise ReadError(f"mapping key is not a string: {knode.value!r}")
            if knode.value in out:
                raise ReadError(f"duplicate YAML key: {knode.value!r}")
            out[knode.value] = _plain(vnode)
        return out
    if isinstance(node, yaml.SequenceNode):
        return [_plain(v) for v in node.value]
    if isinstance(node, yaml.ScalarNode):
        if node.tag == STR_TAG:
            return node.value
        if node.tag == INT_TAG and node.style is None and PLAIN_INT.fullmatch(node.value):
            return int(node.value)
        raise ReadError(f"YAML scalar of type {node.tag} ({node.value!r})")
    raise ReadError(f"YAML node of kind {type(node).__name__}")


def _keys(where: str, obj: object, required: set[str], allowed: set[str]) -> dict[str, Any]:
    if type(obj) is not dict:
        raise ReadError(f"{where} is not a mapping")
    keys = set(obj)
    if not required <= keys:
        raise ReadError(f"{where} lacks {sorted(required - keys)}")
    if not keys <= allowed:
        raise ReadError(f"{where} has keys outside the schema: {sorted(keys - allowed)}")
    return obj


def read_twin_text(data: bytes) -> TwinReading:
    """Read the Witness/v2 corners twin strictly."""
    text = _decode(data)
    try:
        _check_events(text)
        root = yaml.compose(text, Loader=yaml.SafeLoader)
    except yaml.YAMLError as exc:
        raise ReadError(f"not YAML: {exc}") from exc
    if root is None:
        raise ReadError("empty YAML")
    top = _keys("top level", _plain(root), {"softschema", "witness"}, {"softschema", "witness"})
    env = _keys("softschema", top["softschema"], ENVELOPE_KEYS, ENVELOPE_KEYS)
    if env["contract"] != "packing.squares:Witness/v2":
        raise ReadError(f"contract is {env['contract']!r}")
    if env["envelope"] != "witness":
        raise ReadError(f"envelope is {env['envelope']!r}")
    for k in ENVELOPE_KEYS:
        if type(env[k]) is not str:
            raise ReadError(f"softschema.{k} is not a string")
    w = _keys("witness", top["witness"], WITNESS_REQUIRED, WITNESS_ALLOWED)
    if type(w["id"]) is not str or WITNESS_ID.fullmatch(w["id"]) is None:
        raise ReadError(f"witness id {w['id']!r}")
    n = w["n"]
    if type(n) is not int or n < 1:
        raise ReadError(f"witness n is not a positive integer: {n!r}")
    side = scalar(w["side"])
    if side <= 0:
        raise ReadError("witness side is not positive")
    if w["square_size"] != "1":
        raise ReadError("witness square_size is not '1'")
    if w["representation"] != "corners":
        raise ReadError(f"representation is {w['representation']!r}, not corners")
    sc = _keys("scalar", w["scalar"], {"kind"}, {"kind"})
    if sc["kind"] != "rational":
        raise ReadError(f"scalar.kind is {sc['kind']!r}")
    co = _keys("coordinates", w["coordinates"], {"origin", "axes", "angle_unit"}, {"origin", "axes", "angle_unit"})
    if co["origin"] != "lower-left" or co["axes"] != "x-right-y-up":
        raise ReadError(f"coordinates {co!r}: not lower-left, x-right-y-up")
    if co["angle_unit"] not in ANGLE_UNITS:
        raise ReadError(f"angle_unit {co['angle_unit']!r}")
    cl = _keys("claim", w["claim"], CLAIM_REQUIRED, CLAIM_ALLOWED)
    if cl["coordinate_provenance"] not in PROVENANCE or cl["method"] not in METHODS:
        raise ReadError(f"claim {cl['coordinate_provenance']!r} {cl['method']!r}")
    if type(cl["limitations"]) is not str or not cl["limitations"]:
        raise ReadError("claim.limitations is not a non-empty string")
    sq = w["squares"]
    if type(sq) is not list or len(sq) != n:
        raise ReadError(f"witness n is {n} but squares has {len(sq) if type(sq) is list else '?'} entries")
    ids: list[str] = []
    corners: list[tuple[Point, Point, Point, Point]] = []
    for k, entry in enumerate(sq, start=1):
        e = _keys(f"square {k}", entry, {"id", "corners"}, {"id", "corners"})
        if e["id"] != f"square-{k}":
            raise ReadError(f"square {k} has id {e['id']!r}, not 'square-{k}'")
        ids.append(e["id"])
        cs = e["corners"]
        if type(cs) is not list or len(cs) != 4:
            raise ReadError(f"square {k} does not have four corners")
        pts: list[Point] = []
        for p in cs:
            if type(p) is not list or len(p) != 2:
                raise ReadError(f"square {k}: a corner is not a pair")
            pts.append((scalar(p[0]), scalar(p[1])))
        corners.append((pts[0], pts[1], pts[2], pts[3]))
    header = {k: w[k] for k in ("id", "representation", "scalar", "coordinates", "claim")}
    return TwinReading(
        n=n,
        side=side,
        side_text=w["side"],
        ids=tuple(ids),
        corners=tuple(corners),
        envelope=dict(env),
        header=header,
    )


def write_twin_text(t: TwinReading) -> bytes:
    """Write a twin reading back as YAML of the same envelope (for the controls)."""
    lines = ["softschema:"]
    lines += [f"  {k}: {t.envelope[k]}" for k in ("contract", "schema", "envelope", "status")]
    doc = {
        "id": t.header["id"],
        "n": t.n,
        "side": write_scalar(t.side),
        "square_size": "1",
        "representation": t.header["representation"],
        "scalar": t.header["scalar"],
        "coordinates": t.header["coordinates"],
        "claim": t.header["claim"],
        "squares": [
            {"id": i, "corners": [[write_scalar(px), write_scalar(py)] for px, py in cs]}
            for i, cs in zip(t.ids, t.corners, strict=True)
        ],
    }
    body = yaml.safe_dump({"witness": doc}, sort_keys=False, width=10**6, default_flow_style=False)
    return ("\n".join(lines) + "\n" + body).encode("ascii")


# ----------------------------------------------------------------------------- the twin


def json_corners(p: Pose) -> tuple[Point, Point, Point, Point]:
    """The four corners C + (e1 u + e2 v) / 2 of a JSON pose, counterclockwise when u is unit.

    Order: (+u +v), (-u +v), (-u -v), (+u -v), with v = (-s, c).
    """
    half = Fraction(1, 2)
    ux, uy = p.c * half, p.s * half
    vx, vy = -p.s * half, p.c * half
    return (
        (p.x + ux + vx, p.y + uy + vy),
        (p.x - ux + vx, p.y - uy + vy),
        (p.x - ux - vx, p.y - uy - vy),
        (p.x + ux - vx, p.y + uy - vy),
    )


def twin_listing(json_cs: tuple[Point, ...], twin_cs: tuple[Point, ...]) -> tuple[int, int] | None:
    """(start, sense) such that the twin's corners are the JSON corners from ``start``
    in sense +1 (the JSON's cyclic order) or -1 (reversed); None when they are not."""
    for sense in (1, -1):
        for start in range(4):
            if all(twin_cs[k] == json_cs[(start + sense * k) % 4] for k in range(4)):
                return start, sense
    return None


def compare_twin(r: Reading, t: TwinReading) -> dict[str, Any]:
    """Decide whether the twin holds exactly the JSON's packing."""
    problems: list[str] = []
    if r.n != t.n:
        problems.append(f"n differs: {r.n} and {t.n}")
    if r.side != t.side:
        problems.append("side differs")
    if r.side_text != t.side_text:
        problems.append("side text differs")
    listings: dict[str, int] = {}
    for k in range(min(r.n, t.n)):
        got = twin_listing(json_corners(r.poses[k]), t.corners[k])
        if got is None:
            problems.append(f"square {k + 1}: corners differ")
            continue
        key = f"start {got[0]}, sense {'+' if got[1] == 1 else '-'}"
        listings[key] = listings.get(key, 0) + 1
    return {"agree": not problems, "problems": problems[:20], "problem_count": len(problems), "listings": listings}


def read_json(path: str) -> Reading:
    with open(path, "rb") as fh:
        return read_json_text(fh.read())


def read_twin(path: str) -> TwinReading:
    with open(path, "rb") as fh:
        return read_twin_text(fh.read())
