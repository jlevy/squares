"""Strict readers for the review of jlevy/squares#1031 (lane r1031-1118).

Written for this review; imports nothing from this repository or the source.

Three file forms are read, each into exact rationals (``fractions.Fraction``):

* form J, the source's ``n299_exact.json``: keys ``n``, ``side``, ``square_size``,
  ``format`` and ``squares``; each square a list of four scalar strings
  ``[center_x, center_y, cos, sin]``, ``(cos, sin)`` the unit direction of one edge;
* form C, a ``packing.squares:Witness/v2`` record with ``scalar.kind: rational`` and
  ``representation: corners`` (four corners per square) or ``center-basis`` (a centre
  and an exact ``[cos, sin]``), origin ``lower-left`` or ``container-center``;
* form P, a ``.cert`` file: ``#`` comment lines, a header ``n S`` and ``n`` rows
  ``x y t``, the edge at angle ``2 atan t`` counterclockwise from the x-axis.

A scalar is a string ``p`` or ``p/q``: an optional minus, no leading zero, ``q >= 1``.
Lowest terms are recorded, not required.  Anything else is refused with a reason.

A pose is ``(cx, cy, ux, uy)`` with ``ux**2 + uy**2 == 1`` exactly: the closed unit
square ``{c + a u + b v : |a| <= 1/2, |b| <= 1/2}``, ``v = (-uy, ux)``.
"""

from __future__ import annotations

import json
import re
from fractions import Fraction
from math import gcd

import yaml

SCALAR_RE = re.compile(r"-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?")
HALF = Fraction(1, 2)


class ReadError(Exception):
    """A file that this review's readers refuse, with the reason."""


def parse_scalar(text: object, where: str, notes: list[str] | None = None) -> Fraction:
    """Read one scalar string exactly; refuse every other form."""
    if not isinstance(text, str):
        raise ReadError(f"{where}: not a string scalar ({type(text).__name__})")
    if SCALAR_RE.fullmatch(text) is None:
        raise ReadError(f"{where}: not a scalar p or p/q: {text[:60]!r}")
    if "/" in text:
        p_text, q_text = text.split("/")
        p, q = int(p_text), int(q_text)
    else:
        p, q = int(text), 1
    if notes is not None:
        if gcd(p, q) != 1:
            notes.append(f"{where}: not in lowest terms")
        if q == 1 and "/" in text:
            notes.append(f"{where}: denominator 1 written")
        if p == 0 and text.startswith("-"):
            notes.append(f"{where}: negative zero")
    return Fraction(p, q)


def is_unit(ux: Fraction, uy: Fraction) -> bool:
    return ux * ux + uy * uy == 1


def pose_corners(pose: tuple[Fraction, Fraction, Fraction, Fraction]) -> list[tuple[Fraction, Fraction]]:
    """The four corners, counterclockwise: c+u/2+v/2, c-u/2+v/2, c-u/2-v/2, c+u/2-v/2."""
    cx, cy, ux, uy = pose
    hux, huy = ux * HALF, uy * HALF
    hvx, hvy = -uy * HALF, ux * HALF
    return [
        (cx + hux + hvx, cy + huy + hvy),
        (cx - hux + hvx, cy - huy + hvy),
        (cx - hux - hvx, cy - huy - hvy),
        (cx + hux - hvx, cy + huy - hvy),
    ]


def corners_pose(corners: list[tuple[Fraction, Fraction]]) -> tuple[Fraction, Fraction, Fraction, Fraction] | None:
    """The pose of four corners that are a unit square in cyclic order, else None.

    Sides of squared length 1, both diagonals of squared length 2 and the diagonals
    bisecting each other; the direction is the first edge, corner 1 minus corner 0.
    """
    if len(corners) != 4:
        return None
    for k in range(4):
        ax, ay = corners[k]
        bx, by = corners[(k + 1) % 4]
        if (bx - ax) ** 2 + (by - ay) ** 2 != 1:
            return None
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = corners
    if (x2 - x0) ** 2 + (y2 - y0) ** 2 != 2 or (x3 - x1) ** 2 + (y3 - y1) ** 2 != 2:
        return None
    if x0 + x2 != x1 + x3 or y0 + y2 != y1 + y3:
        return None
    return ((x0 + x2) * HALF, (y0 + y2) * HALF, x1 - x0, y1 - y0)


def twin_match(pose_c: list[tuple[Fraction, Fraction]], listed: list[tuple[Fraction, Fraction]]) -> tuple[int, str] | None:
    """Whether ``listed`` is a cyclic rotation of ``pose_c`` in either sense.

    Returns ``(offset, sense)``, sense ``ccw`` when listed[k] == pose_c[(k + offset) % 4]
    and ``cw`` when listed[k] == pose_c[(offset - k) % 4]; None when neither holds.
    """
    for off in range(4):
        if all(listed[k] == pose_c[(k + off) % 4] for k in range(4)):
            return off, "ccw"
    for off in range(4):
        if all(listed[k] == pose_c[(off - k) % 4] for k in range(4)):
            return off, "cw"
    return None


def _check_text(raw: bytes, label: str) -> dict:
    facts: dict = {}
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ReadError(f"{label}: not ASCII ({exc})") from None
    if "\t" in text:
        raise ReadError(f"{label}: contains a tab")
    if "\r" in text:
        raise ReadError(f"{label}: contains a carriage return")
    facts["final_newline"] = text.endswith("\n")
    facts["lines"] = text.count("\n") + (0 if text.endswith("\n") else 1)
    return facts


# ----------------------------------------------------------------------------- form J


def _no_duplicates(pairs: list[tuple[str, object]]) -> dict:
    out: dict = {}
    for k, v in pairs:
        if k in out:
            raise ReadError(f"form J: duplicate key {k!r}")
        out[k] = v
    return out


def _refuse_constant(name: str) -> object:
    raise ReadError(f"form J: non-finite constant {name}")


def _refuse_float(text: str) -> object:
    raise ReadError(f"form J: a JSON number with a fraction or exponent: {text[:40]!r}")


J_KEYS = {"n", "side", "square_size", "format", "squares"}


def read_json_bytes(raw: bytes) -> dict:
    """Form J from bytes: n, side, rows, poses and reading notes."""
    facts = _check_text(raw, "form J")
    try:
        doc = json.loads(
            raw.decode("ascii"),
            object_pairs_hook=_no_duplicates,
            parse_constant=_refuse_constant,
            parse_float=_refuse_float,
        )
    except json.JSONDecodeError as exc:
        raise ReadError(f"form J: not JSON ({exc})") from None
    if not isinstance(doc, dict):
        raise ReadError("form J: top level is not an object")
    if set(doc) != J_KEYS:
        raise ReadError(f"form J: keys {sorted(doc)} are not {sorted(J_KEYS)}")
    n = doc["n"]
    if type(n) is not int or n < 1:
        raise ReadError(f"form J: n is not a positive integer: {n!r}")
    notes: list[str] = []
    side = parse_scalar(doc["side"], "form J side", notes)
    if side <= 0:
        raise ReadError("form J: side not positive")
    if doc["square_size"] != "1":
        raise ReadError(f"form J: square_size is {doc['square_size']!r}, not '1'")
    if not isinstance(doc["format"], str):
        raise ReadError("form J: format is not a string")
    squares = doc["squares"]
    if not isinstance(squares, list):
        raise ReadError("form J: squares is not a list")
    if len(squares) != n:
        raise ReadError(f"form J: n is {n} and {len(squares)} squares are listed")
    poses = []
    for k, row in enumerate(squares, start=1):
        if not isinstance(row, list) or len(row) != 4:
            raise ReadError(f"form J square {k}: not a list of four scalars")
        cx, cy, ux, uy = (parse_scalar(v, f"form J square {k}[{m}]", notes) for m, v in enumerate(row))
        if not is_unit(ux, uy):
            raise ReadError(f"form J square {k}: (cos, sin) is not a unit vector")
        poses.append((cx, cy, ux, uy))
    facts.update(n=n, side_text=doc["side"], format=doc["format"], notes=notes)
    return {"form": "J", "n": n, "side": side, "poses": poses, "facts": facts}


def read_json(path: str) -> dict:
    with open(path, "rb") as fh:
        return read_json_bytes(fh.read())


# ----------------------------------------------------------------------------- form C


class _StrictLoader(yaml.SafeLoader):
    """SafeLoader that refuses duplicate mapping keys."""


def _construct_mapping(loader: _StrictLoader, node: yaml.MappingNode, deep: bool = False) -> dict:
    loader.flatten_mapping(node)
    out: dict = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in out:
            raise ReadError(f"form C: duplicate key {key!r}")
        out[key] = loader.construct_object(value_node, deep=deep)
    return out


_StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)

WITNESS_KEYS = {
    "id", "n", "side", "square_size", "representation", "scalar", "coordinates",
    "squares", "claim", "source", "certificate",
}
WITNESS_REQUIRED = {"id", "n", "side", "square_size", "representation", "scalar", "coordinates", "squares", "claim"}
WITNESS_ID_RE = re.compile(r"W-[a-z0-9][a-z0-9-]*")


def read_witness_bytes(raw: bytes, require_claim: bool = True) -> dict:
    """Form C from bytes: n, side, squares as corners (or poses), reading notes."""
    facts = _check_text(raw, "form C")
    text = raw.decode("ascii")
    try:
        for tok in yaml.scan(text):
            if isinstance(tok, (yaml.AnchorToken, yaml.AliasToken, yaml.TagToken)):
                raise ReadError(f"form C: {type(tok).__name__} not allowed")
        docs = list(yaml.load_all(text, Loader=_StrictLoader))
    except yaml.YAMLError as exc:
        raise ReadError(f"form C: not YAML ({str(exc)[:120]})") from None
    if len(docs) != 1:
        raise ReadError(f"form C: {len(docs)} documents")
    doc = docs[0]
    if not isinstance(doc, dict) or set(doc) != {"softschema", "witness"}:
        raise ReadError("form C: top level is not {softschema, witness}")
    env = doc["softschema"]
    if not isinstance(env, dict) or env.get("contract") != "packing.squares:Witness/v2" or env.get("envelope") != "witness":
        raise ReadError("form C: the envelope is not packing.squares:Witness/v2, envelope witness")
    if not set(env) <= {"contract", "schema", "envelope", "status"}:
        raise ReadError(f"form C: envelope keys {sorted(env)}")
    w = doc["witness"]
    if not isinstance(w, dict):
        raise ReadError("form C: witness is not a mapping")
    extra = set(w) - WITNESS_KEYS
    if extra:
        raise ReadError(f"form C: keys outside the schema: {sorted(extra)}")
    required = WITNESS_REQUIRED if require_claim else WITNESS_REQUIRED - {"claim"}
    missing = required - set(w)
    if missing:
        raise ReadError(f"form C: required keys missing: {sorted(missing)}")
    if not isinstance(w["id"], str) or WITNESS_ID_RE.fullmatch(w["id"]) is None:
        raise ReadError(f"form C: id {w['id']!r} does not match the schema")
    n = w["n"]
    if type(n) is not int or n < 1:
        raise ReadError(f"form C: n is not a positive integer: {n!r}")
    notes: list[str] = []
    side = parse_scalar(w["side"], "form C side", notes)
    if side <= 0:
        raise ReadError("form C: side not positive")
    if w["square_size"] != "1":
        raise ReadError(f"form C: square_size {w['square_size']!r} is not '1'")
    if w["scalar"] != {"kind": "rational"}:
        raise ReadError(f"form C: scalar is {w['scalar']!r}, not {{kind: rational}}")
    coords = w["coordinates"]
    if not isinstance(coords, dict) or set(coords) != {"origin", "axes", "angle_unit"}:
        raise ReadError("form C: coordinates keys are not origin, axes, angle_unit")
    if coords["axes"] != "x-right-y-up":
        raise ReadError(f"form C: axes {coords['axes']!r}")
    if coords["origin"] not in ("lower-left", "container-center"):
        raise ReadError(f"form C: origin {coords['origin']!r}")
    if coords["angle_unit"] not in ("degrees", "radians", "not-applicable"):
        raise ReadError(f"form C: angle_unit {coords['angle_unit']!r}")
    shift = side * HALF if coords["origin"] == "container-center" else Fraction(0)
    rep = w["representation"]
    squares = w["squares"]
    if not isinstance(squares, list) or len(squares) != n:
        raise ReadError(f"form C: n is {n} and {len(squares) if isinstance(squares, list) else '?'} squares are listed")
    id_style = None
    corners_all: list[list[tuple[Fraction, Fraction]]] = []
    poses: list[tuple[Fraction, Fraction, Fraction, Fraction]] = []
    for k, sq in enumerate(squares, start=1):
        if not isinstance(sq, dict) or "id" not in sq:
            raise ReadError(f"form C square {k}: not a mapping with an id")
        sid = sq["id"]
        if sid == f"square-{k}":
            style = "square-k"
        elif type(sid) is int and sid == k:
            style = "integer"
        else:
            raise ReadError(f"form C square {k}: id {sid!r} out of order")
        if id_style is None:
            id_style = style
        elif style != id_style:
            raise ReadError(f"form C square {k}: id style changes")
        if rep == "corners":
            if set(sq) != {"id", "corners"}:
                raise ReadError(f"form C square {k}: keys {sorted(sq)}, not id and corners")
            cs = sq["corners"]
            if not isinstance(cs, list) or len(cs) != 4:
                raise ReadError(f"form C square {k}: not four corners")
            pts = []
            for m, pt in enumerate(cs):
                if not isinstance(pt, list) or len(pt) != 2:
                    raise ReadError(f"form C square {k} corner {m}: not a point of two scalars")
                x = parse_scalar(pt[0], f"form C square {k} corner {m} x", notes) + shift
                y = parse_scalar(pt[1], f"form C square {k} corner {m} y", notes) + shift
                pts.append((x, y))
            corners_all.append(pts)
        elif rep == "center-basis":
            if set(sq) != {"id", "center", "basis"}:
                raise ReadError(f"form C square {k}: keys {sorted(sq)}, not id, center and basis")
            c, b = sq["center"], sq["basis"]
            if not (isinstance(c, list) and len(c) == 2 and isinstance(b, list) and len(b) == 2):
                raise ReadError(f"form C square {k}: centre or basis not a pair")
            cx = parse_scalar(c[0], f"form C square {k} center x", notes) + shift
            cy = parse_scalar(c[1], f"form C square {k} center y", notes) + shift
            ux = parse_scalar(b[0], f"form C square {k} basis cos", notes)
            uy = parse_scalar(b[1], f"form C square {k} basis sin", notes)
            if not is_unit(ux, uy):
                raise ReadError(f"form C square {k}: basis is not a unit vector")
            poses.append((cx, cy, ux, uy))
        else:
            raise ReadError(f"form C: representation {rep!r} is not exact corners or center-basis")
    facts.update(
        n=n, id=w["id"], side_text=w["side"], representation=rep, origin=coords["origin"],
        id_style=id_style, envelope_status=env.get("status"), claim=w.get("claim"),
        has_source="source" in w, has_certificate="certificate" in w, notes=notes,
    )
    out = {"form": "C", "n": n, "side": side, "facts": facts, "representation": rep}
    if rep == "corners":
        out["corners"] = corners_all
    else:
        out["poses"] = poses
    return out


def read_witness(path: str, require_claim: bool = True) -> dict:
    with open(path, "rb") as fh:
        return read_witness_bytes(fh.read(), require_claim=require_claim)


# ----------------------------------------------------------------------------- form P


def tangent_direction(t: Fraction) -> tuple[Fraction, Fraction]:
    """(cos, sin) of the angle 2 atan t: ((1 - t^2), 2t) / (1 + t^2)."""
    r = 1 + t * t
    return (1 - t * t) / r, 2 * t / r


def read_cert_bytes(raw: bytes) -> dict:
    """Form P from bytes: comment lines, header ``n S``, then ``n`` rows ``x y t``."""
    facts = _check_text(raw, "form P")
    text = raw.decode("ascii")
    if not text.endswith("\n"):
        raise ReadError("form P: no final newline")
    lines = text[:-1].split("\n")
    k = 0
    comments = []
    while k < len(lines) and lines[k].startswith("#"):
        comments.append(lines[k])
        k += 1
    if k >= len(lines):
        raise ReadError("form P: no header")
    head = lines[k].split(" ")
    if len(head) != 2 or not re.fullmatch(r"[1-9][0-9]*", head[0]):
        raise ReadError(f"form P: header {lines[k][:60]!r} is not 'n S'")
    n = int(head[0])
    notes: list[str] = []
    side = parse_scalar(head[1], "form P side", notes)
    rows = lines[k + 1:]
    if len(rows) != n:
        raise ReadError(f"form P: n is {n} and {len(rows)} rows follow")
    poses = []
    for m, line in enumerate(rows, start=1):
        if line.startswith("#"):
            raise ReadError(f"form P row {m}: a comment after the header")
        parts = line.split(" ")
        if len(parts) != 3:
            raise ReadError(f"form P row {m}: not three scalars separated by single spaces")
        x, y, t = (parse_scalar(v, f"form P row {m}[{j}]", notes) for j, v in enumerate(parts))
        ux, uy = tangent_direction(t)
        poses.append((x, y, ux, uy))
    facts.update(n=n, side_text=head[1], comments=comments, notes=notes)
    return {"form": "P", "n": n, "side": side, "poses": poses, "facts": facts}


def read_cert(path: str) -> dict:
    with open(path, "rb") as fh:
        return read_cert_bytes(fh.read())


# ----------------------------------------------------------------------------- any form


def read_any(path: str, kind: str, require_claim: bool = True) -> dict:
    """Read a file of a stated kind (json, witness, cert) and give poses for every square.

    A corners witness is turned into poses by ``corners_pose``; a square whose corners
    are not a unit square is refused here.
    """
    if kind == "json":
        doc = read_json(path)
    elif kind == "cert":
        doc = read_cert(path)
    elif kind == "witness":
        doc = read_witness(path, require_claim=require_claim)
        if doc["representation"] == "corners":
            poses = []
            for k, cs in enumerate(doc["corners"], start=1):
                p = corners_pose(cs)
                if p is None:
                    raise ReadError(f"form C square {k}: corners are not a unit square")
                poses.append(p)
            doc["poses"] = poses
    else:
        raise ValueError(kind)
    return doc
