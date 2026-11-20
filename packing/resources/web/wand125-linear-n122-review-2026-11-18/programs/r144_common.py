"""Shared readers and exact helpers for lane r144's review of mixed_n122_L1126.

Written for this review from the mathematics and the source's documents (README.md,
manifest.json, completion-audit.json and the shape of candidate.json and input.txt).
It imports nothing from jlevy/squares or from the source, and no code of either was
read before it was written.

Conventions (all exact, in fractions.Fraction):
- K = [0, L]^2; D4 acts on K by the eight maps listed in D4_NAMES.
- A primitive is (kind, geometry, mass): kind 'point' [x, y], 'segment'
  [x0, y0, x1, y1] (end points), 'rectangle' [x0, y0, x1, y1] (opposite corners).
  Its mass m is the orbit's: each of its eight D4 images carries m/8, spread
  uniformly (by length on a segment, by area on a rectangle).
- Net node j has half-angle tangent t_j = j * step; the core at node j is the closed
  square of side B centred at c with sides along u = (cos, sin), v = (-sin, cos),
  cos = (1 - t^2)/(1 + t^2), sin = 2t/(1 + t^2).
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from fractions import Fraction as F

RAT_RE = re.compile(r"^-?[0-9]+(/[0-9]+)?$")
DEC_RE = re.compile(r"^-?[0-9]+\.[0-9]+$")

D4_NAMES = ["id", "flip_x", "flip_y", "rot180", "swap", "rot90", "rot270", "antiswap"]


class ReadError(Exception):
    pass


def _no_float(token: str):
    raise ReadError(f"float token in JSON: {token!r}")


def _no_const(token: str):
    raise ReadError(f"non-finite constant in JSON: {token!r}")


def _pairs(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ReadError(f"duplicate key {k!r}")
        out[k] = v
    return out


def read_json_strict(data: bytes):
    """Parse JSON bytes, refusing float tokens, NaN/Infinity and duplicate keys."""
    text = data.decode("utf-8")
    return json.loads(text, object_pairs_hook=_pairs, parse_float=_no_float, parse_constant=_no_const)


def rat(s, *, allow_decimal: bool = False) -> F:
    """Strict rational: 'p' or 'p/q' (q > 0), optionally a plain decimal 'a.b'."""
    if not isinstance(s, str):
        raise ReadError(f"expected a string number, got {type(s).__name__}: {s!r}")
    if RAT_RE.match(s):
        if "/" in s:
            p, q = s.split("/")
            if int(q) == 0:
                raise ReadError(f"zero denominator: {s!r}")
        return F(s)
    if allow_decimal and DEC_RE.match(s):
        return F(s)
    raise ReadError(f"not a strict rational: {s!r}")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_id(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


CANDIDATE_KEYS = {"schema", "n", "L", "B", "net", "primitives", "total_mass"}
KIND_ARITY = {"point": 2, "segment": 4, "rectangle": 4}


def load_candidate(data: bytes) -> dict:
    """Read candidate.json strictly. Returns exact values; refuses anything unexpected."""
    obj = read_json_strict(data)
    if not isinstance(obj, dict) or set(obj) != CANDIDATE_KEYS:
        raise ReadError(f"candidate keys {sorted(obj) if isinstance(obj, dict) else type(obj)}")
    if obj["schema"] != "point_line_rectangle_v1":
        raise ReadError(f"schema {obj['schema']!r}")
    if not isinstance(obj["n"], int) or isinstance(obj["n"], bool):
        raise ReadError("n is not an integer")
    net = obj["net"]
    if not isinstance(net, dict) or set(net) != {"step", "last"}:
        raise ReadError(f"net keys {net!r}")
    if not isinstance(net["last"], int) or isinstance(net["last"], bool):
        raise ReadError("net.last is not an integer")
    prims = []
    for i, p in enumerate(obj["primitives"]):
        if not isinstance(p, dict) or set(p) != {"kind", "geometry", "mass"}:
            raise ReadError(f"primitive {i} keys")
        kind = p["kind"]
        if kind not in KIND_ARITY:
            raise ReadError(f"primitive {i} kind {kind!r}")
        g = p["geometry"]
        if not isinstance(g, list) or len(g) != KIND_ARITY[kind]:
            raise ReadError(f"primitive {i} geometry arity")
        prims.append((kind, tuple(rat(v) for v in g), rat(p["mass"])))
    return {
        "n": obj["n"],
        "L": rat(obj["L"], allow_decimal=True),
        "B": rat(obj["B"], allow_decimal=True),
        "step": rat(net["step"]),
        "last": net["last"],
        "primitives": prims,
        "total_mass": rat(obj["total_mass"]),
        "raw": obj,
    }


def d4_map(g: int, L: F, x: F, y: F):
    if g == 0:
        return x, y
    if g == 1:
        return L - x, y
    if g == 2:
        return x, L - y
    if g == 3:
        return L - x, L - y
    if g == 4:
        return y, x
    if g == 5:
        return L - y, x
    if g == 6:
        return y, L - x
    if g == 7:
        return L - y, L - x
    raise ValueError(g)


def image_of(kind: str, geom: tuple, g: int, L: F) -> tuple:
    """The D4 image of one primitive's geometry, canonical: a segment's end points are
    sorted, a rectangle is (x0, y0, x1, y1) with x0 < x1 and y0 < y1."""
    if kind == "point":
        return d4_map(g, L, geom[0], geom[1])
    if kind == "segment":
        a = d4_map(g, L, geom[0], geom[1])
        b = d4_map(g, L, geom[2], geom[3])
        a, b = sorted([a, b])
        return (a[0], a[1], b[0], b[1])
    if kind == "rectangle":
        a = d4_map(g, L, geom[0], geom[1])
        b = d4_map(g, L, geom[2], geom[3])
        return (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1]))
    raise ValueError(kind)


def expand_images(prims, L: F, factor: F = F(1)):
    """Every D4 image of every primitive: list of (kind, geom, mass/8 * factor, prim, g)."""
    out = []
    for i, (kind, geom, m) in enumerate(prims):
        for g in range(8):
            out.append((kind, image_of(kind, geom, g, L), m * factor / 8, i, g))
    return out


def angle_data(j: int, step: F, L: F, B: F) -> dict:
    t = step * j
    den = 1 + t * t
    c = (1 - t * t) / den
    s = 2 * t / den
    b = B / 2
    E = L / 2 - b * (c + s)
    return {"j": j, "t": t, "cos": c, "sin": s, "b": b, "E": E}


def round_down(q: F) -> float:
    """Largest binary64 value <= q (q finite, of moderate size)."""
    f = float(q)
    if F(f) > q:
        f = math.nextafter(f, -math.inf)
    return f


def round_up(q: F) -> float:
    f = float(q)
    if F(f) < q:
        f = math.nextafter(f, math.inf)
    return f


def fstr(q: F, digits: int = 17) -> str:
    """A decimal string of a fraction for reports (not used in decisions)."""
    return f"{float(q):.{digits}g}"


def frac_str(q: F) -> str:
    return f"{q.numerator}/{q.denominator}" if q.denominator != 1 else str(q.numerator)
