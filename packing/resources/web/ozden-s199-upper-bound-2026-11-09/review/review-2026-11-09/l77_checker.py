"""Clean-room exact checker for Witness/v2 corner files (review lane L77, #938).

Written for the stage 4 review of issue #938 before any producer code or any of this
repository's witness, verifier or promotion code was read. It imports nothing from this
repository or from the source under review.

Three parts that share only plain integers:

- ``read_witness`` / ``read_witness_json``: a strict reader that fails closed on any
  layout it does not expect, and returns every scalar as a pair of integers ``(p, q)``.
- Method A: separating axes in ``fractions.Fraction``. A square's corner list must be a
  unit square (``u.u == 1``, ``f == +-perp(u)``, ``p2 == p0 + u + f``), so its two edge
  directions are exact rational unit vectors and every projection gap is an exact length.
  Two convex polygons have disjoint interiors exactly when, on one of the four edge
  normals, their projections overlap in at most a point; the pair margin is the largest
  such gap, and a margin of exactly 0 is a contact.
- Method B: exact clipped areas in ``gmpy2.mpq``. Four unit edges whose turns share one
  sign and area 1 make a unit square. Containment is "clipping to the box keeps area 1";
  each wall is classed by clipping to the closed outside half-plane; each pair by
  clipping one square to the other: empty is clear, nonempty with area 0 is a contact,
  positive area is an overlap.

Interiors are what must be disjoint, so an exact contact (gap 0) is not an overlap.
"""

from __future__ import annotations

import hashlib
import json
import re
from fractions import Fraction
from math import gcd
from typing import Any

import gmpy2
import yaml

Q = tuple[int, int]  # (numerator, denominator), denominator > 0, lowest terms
Point = tuple[Q, Q]

_SCALAR = re.compile(r"^(-?)(0|[1-9][0-9]*)(?:/([1-9][0-9]*))?$")
_INT = re.compile(r"^[1-9][0-9]*$")

WITNESS_KEYS = {
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
}
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


class Refused(Exception):
    """The reader or a shape check refuses the input; the message says why."""


# ---------------------------------------------------------------------------- reader


def parse_scalar(text: str) -> Q:
    """An integer or p/q, q > 1, in lowest terms and canonical decimal form."""
    if not isinstance(text, str):
        raise Refused(f"scalar is not a string: {text!r}")
    m = _SCALAR.match(text)
    if m is None:
        raise Refused(f"scalar not canonical integer or p/q: {text[:60]!r}")
    sign, num, den = m.group(1), int(m.group(2)), m.group(3)
    if sign and num == 0:
        raise Refused("scalar -0")
    p = -num if sign else num
    if den is None:
        return (p, 1)
    q = int(den)
    if q == 1:
        raise Refused(f"scalar with denominator 1: {text[:60]!r}")
    if p == 0:
        raise Refused(f"scalar 0/q: {text[:60]!r}")
    if gcd(abs(p), q) != 1:
        raise Refused(f"scalar not in lowest terms: {text[:60]!r}")
    return (p, q)


def _plain_yaml(node: yaml.Node) -> Any:
    """Compose-level YAML to plain data: scalars stay strings, keys must be unique."""
    if isinstance(node, yaml.MappingNode):
        out: dict[str, Any] = {}
        for k, v in node.value:
            if not isinstance(k, yaml.ScalarNode):
                raise Refused("non-scalar mapping key")
            if k.value in out:
                raise Refused(f"duplicate key {k.value!r}")
            out[k.value] = _plain_yaml(v)
        return out
    if isinstance(node, yaml.SequenceNode):
        return [_plain_yaml(v) for v in node.value]
    if isinstance(node, yaml.ScalarNode):
        if node.tag not in ("tag:yaml.org,2002:str", "tag:yaml.org,2002:int"):
            raise Refused(f"scalar with tag {node.tag} ({node.value[:40]!r})")
        if node.tag == "tag:yaml.org,2002:int" and not (
            _INT.match(node.value) or node.value == "0"
        ):
            raise Refused(f"integer not in plain decimal form: {node.value!r}")
        return node.value
    raise Refused(f"unexpected node {type(node).__name__}")


def _no_dup_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in pairs:
        if k in out:
            raise Refused(f"duplicate key {k!r}")
        out[k] = v
    return out


def _refuse_float(text: str) -> Any:
    raise Refused(f"JSON float {text!r}")


def _refuse_const(text: str) -> Any:
    raise Refused(f"JSON constant {text!r}")


def _plain_json(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _plain_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_plain_json(v) for v in obj]
    if isinstance(obj, bool) or obj is None:
        raise Refused(f"JSON literal {obj!r}")
    if isinstance(obj, int):
        return str(obj)
    if isinstance(obj, str):
        return obj
    raise Refused(f"JSON value of type {type(obj).__name__}")


def _str(d: dict[str, Any], key: str) -> str:
    v = d.get(key)
    if not isinstance(v, str):
        raise Refused(f"{key} missing or not a scalar")
    return v


def interpret(doc: Any) -> dict[str, Any]:
    """Validate the plain tree and return side, ids and integer corners."""
    if not isinstance(doc, dict) or set(doc) != {"softschema", "witness"}:
        raise Refused("top level must be exactly softschema + witness")
    env = doc["softschema"]
    if not isinstance(env, dict):
        raise Refused("softschema not a mapping")
    if env.get("contract") != "packing.squares:Witness/v2":
        raise Refused(f"contract {env.get('contract')!r}")
    if env.get("envelope") != "witness":
        raise Refused(f"envelope {env.get('envelope')!r}")
    w = doc["witness"]
    if not isinstance(w, dict):
        raise Refused("witness not a mapping")
    extra = set(w) - WITNESS_KEYS
    missing = WITNESS_REQUIRED - set(w)
    if extra:
        raise Refused(f"unknown witness keys {sorted(extra)}")
    if missing:
        raise Refused(f"missing witness keys {sorted(missing)}")
    if _str(w, "square_size") != "1":
        raise Refused("square_size is not '1'")
    if _str(w, "representation") != "corners":
        raise Refused(f"representation {w['representation']!r}")
    if w["scalar"] != {"kind": "rational"}:
        raise Refused(f"scalar {w['scalar']!r}")
    coords = w["coordinates"]
    if not isinstance(coords, dict) or set(coords) != {"origin", "axes", "angle_unit"}:
        raise Refused("coordinates must have exactly origin, axes, angle_unit")
    if coords["origin"] != "lower-left":
        raise Refused(f"origin {coords['origin']!r}")
    if coords["axes"] != "x-right-y-up":
        raise Refused(f"axes {coords['axes']!r}")
    if coords["angle_unit"] not in ("degrees", "radians", "not-applicable"):
        raise Refused(f"angle_unit {coords['angle_unit']!r}")
    n_text = _str(w, "n")
    if not _INT.match(n_text):
        raise Refused(f"n not a positive integer: {n_text!r}")
    n = int(n_text)
    side = parse_scalar(_str(w, "side"))
    if side[0] <= 0:
        raise Refused("side not positive")
    sq = w["squares"]
    if not isinstance(sq, list):
        raise Refused("squares not a list")
    if len(sq) != n:
        raise Refused(f"n = {n} but {len(sq)} squares")
    ids: list[int] = []
    corners: list[list[Point]] = []
    for entry in sq:
        if not isinstance(entry, dict) or set(entry) != {"id", "corners"}:
            raise Refused("square entry must have exactly id and corners")
        id_text = entry["id"]
        if not isinstance(id_text, str) or not _INT.match(id_text):
            raise Refused(f"square id not a positive integer: {id_text!r}")
        ids.append(int(id_text))
        cs = entry["corners"]
        if not isinstance(cs, list) or len(cs) != 4:
            raise Refused(f"square {id_text}: corners must be a list of 4")
        pts: list[Point] = []
        for c in cs:
            if not isinstance(c, list) or len(c) != 2:
                raise Refused(f"square {id_text}: a corner must be [x, y]")
            pts.append((parse_scalar(c[0]), parse_scalar(c[1])))
        corners.append(pts)
    if len(set(ids)) != len(ids):
        raise Refused("repeated square id")
    return {
        "n": n,
        "side": side,
        "ids": ids,
        "ids_in_order": ids == list(range(1, n + 1)),
        "corners": corners,
        "id": w.get("id"),
        "plain": doc,
    }


def read_witness_text(text: str) -> dict[str, Any]:
    try:
        node = yaml.compose(text, Loader=yaml.SafeLoader)
    except yaml.YAMLError as e:
        raise Refused(f"YAML: {e}") from None
    if node is None:
        raise Refused("empty document")
    return interpret(_plain_yaml(node))


def read_witness(path: str) -> dict[str, Any]:
    with open(path, "rb") as fh:
        raw = fh.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise Refused("not UTF-8") from None
    out = read_witness_text(text)
    out["sha256"] = hashlib.sha256(raw).hexdigest()
    out["bytes"] = len(raw)
    out["ends_with_newline"] = raw.endswith(b"\n")
    return out


def read_witness_json(path: str) -> dict[str, Any]:
    with open(path, "rb") as fh:
        raw = fh.read()
    try:
        obj = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_no_dup_pairs,
            parse_float=_refuse_float,
            parse_constant=_refuse_const,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise Refused(f"JSON: {e}") from None
    out = interpret(_plain_json(obj))
    out["sha256"] = hashlib.sha256(raw).hexdigest()
    out["bytes"] = len(raw)
    out["ends_with_newline"] = raw.endswith(b"\n")
    return out


def q_str(x: Fraction | Any) -> str:
    """Exact text of a Fraction or mpq."""
    if isinstance(x, Fraction):
        return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    n, d = int(x.numerator), int(x.denominator)
    return str(n) if d == 1 else f"{n}/{d}"


# ---------------------------------------------------------------------------- method A


def _fa(p: Q) -> Fraction:
    return Fraction(p[0], p[1])


class SquareA:
    """A unit square read by method A; raises Refused if the corners are not one."""

    __slots__ = ("pts", "axes", "ccw")

    def __init__(self, corners: list[Point]):
        pts = [(_fa(x), _fa(y)) for x, y in corners]
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pts
        ux, uy = x1 - x0, y1 - y0
        fx, fy = x3 - x0, y3 - y0
        if ux * ux + uy * uy != 1:
            raise Refused("A: first edge is not of length 1")
        if (fx, fy) == (-uy, ux):
            ccw = True
        elif (fx, fy) == (uy, -ux):
            ccw = False
        else:
            raise Refused("A: last edge is not the first turned by a right angle")
        if (x2, y2) != (x0 + ux + fx, y0 + uy + fy):
            raise Refused("A: third corner is not p0 + u + f")
        self.pts = pts
        self.axes = ((ux, uy), (-uy, ux))
        self.ccw = ccw


def walls_a(sq: SquareA, side: Fraction) -> dict[str, Fraction]:
    xs = [p[0] for p in sq.pts]
    ys = [p[1] for p in sq.pts]
    return {
        "left": min(xs),
        "bottom": min(ys),
        "right": side - max(xs),
        "top": side - max(ys),
    }


def margin_a(a: SquareA, b: SquareA) -> tuple[Fraction, int]:
    """Largest projection gap over the four edge normals, and which axis gives it."""
    best: Fraction | None = None
    which = -1
    for k, (ax, ay) in enumerate(a.axes + b.axes):
        pa = [ax * x + ay * y for x, y in a.pts]
        pb = [ax * x + ay * y for x, y in b.pts]
        gap = max(min(pb) - max(pa), min(pa) - max(pb))
        if best is None or gap > best:
            best, which = gap, k
    assert best is not None
    return best, which


# ---------------------------------------------------------------------------- method B

MPQ = gmpy2.mpq
ZERO = MPQ(0)


def _mb(p: Q) -> Any:
    return MPQ(p[0], p[1])


def _area2(poly: list[tuple[Any, Any]]) -> Any:
    """Twice the signed shoelace area."""
    s = ZERO
    m = len(poly)
    for i in range(m):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % m]
        s += x0 * y1 - x1 * y0
    return s


class SquareB:
    """A unit square read by method B: four unit edges, one turning sign, area 1."""

    __slots__ = ("pts", "sign")

    def __init__(self, corners: list[Point]):
        pts = [(_mb(x), _mb(y)) for x, y in corners]
        edges = []
        for i in range(4):
            x0, y0 = pts[i]
            x1, y1 = pts[(i + 1) % 4]
            ex, ey = x1 - x0, y1 - y0
            if ex * ex + ey * ey != 1:
                raise Refused(f"B: edge {i} is not of length 1")
            edges.append((ex, ey))
        turns = []
        for i in range(4):
            ax, ay = edges[i]
            bx, by = edges[(i + 1) % 4]
            turns.append(ax * by - ay * bx)
        if all(t > 0 for t in turns):
            sign = 1
        elif all(t < 0 for t in turns):
            sign = -1
        else:
            raise Refused("B: turns do not share one sign")
        a2 = _area2(pts)
        if a2 * sign != 2:
            raise Refused("B: area is not 1")
        self.pts = pts
        self.sign = sign


def _clip(poly: list[tuple[Any, Any]], a: Any, b: Any, c: Any) -> list[tuple[Any, Any]]:
    """Sutherland-Hodgman against the closed half-plane a*x + b*y + c >= 0."""
    out: list[tuple[Any, Any]] = []
    m = len(poly)
    if m == 0:
        return out
    for i in range(m):
        s = poly[i - 1]
        e = poly[i]
        ls = a * s[0] + b * s[1] + c
        le = a * e[0] + b * e[1] + c
        if le >= 0:
            if ls < 0:
                t = ls / (ls - le)
                out.append((s[0] + t * (e[0] - s[0]), s[1] + t * (e[1] - s[1])))
            out.append(e)
        elif ls >= 0:
            t = ls / (ls - le)
            out.append((s[0] + t * (e[0] - s[0]), s[1] + t * (e[1] - s[1])))
    return out


def _halfplanes(sq: SquareB) -> list[tuple[Any, Any, Any]]:
    """The square as four closed half-planes a*x + b*y + c >= 0."""
    hp = []
    for i in range(4):
        x0, y0 = sq.pts[i]
        x1, y1 = sq.pts[(i + 1) % 4]
        # inside iff sign * cross(p1 - p0, p - p0) >= 0
        ex, ey = x1 - x0, y1 - y0
        a = -ey * sq.sign
        b = ex * sq.sign
        c = (ey * x0 - ex * y0) * sq.sign
        hp.append((a, b, c))
    return hp


def classify(poly: list[tuple[Any, Any]]) -> tuple[str, Any]:
    if not poly:
        return "clear", ZERO
    area = abs(_area2(poly)) / 2
    return ("overlap" if area > 0 else "contact"), area


def pair_b(a: SquareB, b: SquareB) -> tuple[str, Any]:
    poly = list(a.pts)
    for hp in _halfplanes(b):
        poly = _clip(poly, *hp)
        if not poly:
            break
    return classify(poly)


def walls_b(sq: SquareB, side: Any) -> tuple[dict[str, tuple[str, Any]], Any]:
    """Each wall classed by clipping to its closed outside half-plane, and the area kept
    by clipping to the box."""
    outside = {
        "left": (MPQ(-1), ZERO, ZERO),  # x <= 0
        "bottom": (ZERO, MPQ(-1), ZERO),  # y <= 0
        "right": (MPQ(1), ZERO, -side),  # x >= side
        "top": (ZERO, MPQ(1), -side),  # y >= side
    }
    classes = {}
    for name, hp in outside.items():
        classes[name] = classify(_clip(list(sq.pts), *hp))
    poly = list(sq.pts)
    for hp in ((MPQ(1), ZERO, ZERO), (ZERO, MPQ(1), ZERO), (MPQ(-1), ZERO, side), (ZERO, MPQ(-1), side)):
        poly = _clip(poly, *hp)
    kept = abs(_area2(poly)) / 2 if poly else ZERO
    return classes, kept


# ---------------------------------------------------------------------------- deciding


def _class_a(m: Fraction) -> str:
    return "overlap" if m < 0 else ("contact" if m == 0 else "clear")


def decide(side_q: Q, corners: list[list[Point]], ids: list[int] | None = None,
           pairs: list[tuple[int, int]] | None = None, near: Fraction = Fraction(1, 10**12)) -> dict[str, Any]:
    """Decide a packing by both methods. ``pairs`` (0-based) limits the pairs examined,
    for pair-level controls; by default every pair is decided."""
    n = len(corners)
    ids = ids if ids is not None else list(range(1, n + 1))
    side_a = _fa(side_q)
    side_b = _mb(side_q)
    shape_a: list[SquareA | None] = []
    shape_b: list[SquareB | None] = []
    bad_shape: dict[str, list[int]] = {"A": [], "B": []}
    for i, cs in enumerate(corners):
        try:
            shape_a.append(SquareA(cs))
        except Refused:
            shape_a.append(None)
            bad_shape["A"].append(ids[i])
        try:
            shape_b.append(SquareB(cs))
        except Refused:
            shape_b.append(None)
            bad_shape["B"].append(ids[i])
    outside_a: list[int] = []
    outside_b: list[int] = []
    contacts_a: list[list[Any]] = []
    contacts_b: list[list[Any]] = []
    least_clear: tuple[Fraction, int, str] | None = None
    wall_disagree: list[int] = []
    for i in range(n):
        sa, sb = shape_a[i], shape_b[i]
        w = cls = None
        if sa is not None:
            w = walls_a(sa, side_a)
            if any(v < 0 for v in w.values()):
                outside_a.append(ids[i])
            for name, v in w.items():
                if v == 0:
                    contacts_a.append([ids[i], name])
                elif v > 0 and (least_clear is None or v < least_clear[0]):
                    least_clear = (v, ids[i], name)
        if sb is not None:
            cls, kept = walls_b(sb, side_b)
            if kept != 1 or any(c[0] == "overlap" for c in cls.values()):
                outside_b.append(ids[i])
            for name, c in cls.items():
                if c[0] == "contact":
                    contacts_b.append([ids[i], name])
        if w is not None and cls is not None:
            # A's clearance c: c < 0 outside ("overlap"), c == 0 contact, c > 0 clear,
            # which is _class_a's mapping; B's class comes from the outside clip.
            if any(_class_a(w[name]) != cls[name][0] for name in w):
                wall_disagree.append(ids[i])
    if pairs is None:
        pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    overlap_a: list[list[Any]] = []
    overlap_b: list[list[Any]] = []
    touch_a: list[list[int]] = []
    touch_b: list[list[int]] = []
    disagree: list[list[int]] = []
    least: tuple[Fraction, int, int] | None = None
    least_pos: tuple[Fraction, int, int] | None = None
    near_pairs: list[list[Any]] = []
    area_sum = ZERO
    decided = 0
    for i, j in pairs:
        sa_i, sa_j, sb_i, sb_j = shape_a[i], shape_a[j], shape_b[i], shape_b[j]
        ca = cb = None
        if sa_i is not None and sa_j is not None:
            m, _ = margin_a(sa_i, sa_j)
            ca = _class_a(m)
            if least is None or m < least[0]:
                least = (m, ids[i], ids[j])
            if m > 0 and (least_pos is None or m < least_pos[0]):
                least_pos = (m, ids[i], ids[j])
            if 0 < m < near:
                near_pairs.append([ids[i], ids[j], q_str(m)])
            if ca == "overlap":
                overlap_a.append([ids[i], ids[j], q_str(m)])
            elif ca == "contact":
                touch_a.append([ids[i], ids[j]])
        if sb_i is not None and sb_j is not None:
            cb, area = pair_b(sb_i, sb_j)
            area_sum += area
            if cb == "overlap":
                overlap_b.append([ids[i], ids[j], q_str(area)])
            elif cb == "contact":
                touch_b.append([ids[i], ids[j]])
        if ca is not None and cb is not None and ca != cb:
            disagree.append([ids[i], ids[j]])
        decided += 1
    ok_a = not bad_shape["A"] and not outside_a and not overlap_a
    ok_b = not bad_shape["B"] and not outside_b and not overlap_b
    agree = (
        ok_a == ok_b
        and not disagree
        and not wall_disagree
        and sorted(map(tuple, contacts_a)) == sorted(map(tuple, contacts_b))
        and bad_shape["A"] == bad_shape["B"]
        and outside_a == outside_b
    )
    if ok_a and ok_b and agree:
        verdict = "ACCEPT"
    elif not ok_a and not ok_b and agree:
        verdict = "REFUSE"
    else:
        verdict = "METHODS_DISAGREE"
    return {
        "verdict": verdict,
        "n": n,
        "side": q_str(Fraction(*side_q)),
        "pairs_decided": decided,
        "not_unit_square": bad_shape,
        "outside": {"A": outside_a, "B": outside_b},
        "wall_contacts": {"A": contacts_a, "B": contacts_b},
        "wall_class_disagreements": wall_disagree,
        "least_positive_wall_clearance": None
        if least_clear is None
        else {"value": q_str(least_clear[0]), "float": float(least_clear[0]),
              "square": least_clear[1], "wall": least_clear[2]},
        "overlapping_pairs": {"A": overlap_a, "B": overlap_b},
        "touching_pairs": {"A": touch_a, "B": touch_b},
        "pair_class_disagreements": disagree,
        "least_pair_margin": None
        if least is None
        else {"value": q_str(least[0]), "float": float(least[0]), "pair": [least[1], least[2]]},
        "least_positive_pair_margin": None
        if least_pos is None
        else {"value": q_str(least_pos[0]), "float": float(least_pos[0]),
              "pair": [least_pos[1], least_pos[2]]},
        "pairs_below_1e-12_positive": len(near_pairs),
        "sum_clipped_areas": q_str(area_sum),
        "orientation_ccw": sum(1 for s in shape_a if s is not None and s.ccw),
    }
