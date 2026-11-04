"""Exact geometry of unit squares in a square box, for the stage 4 review of #893 and #894.

Written for this review from the mathematics and from the Witness/v2 schema text
(packing/witnesses/witness.schema.yaml), not from any checker's code: neither the author's
sqcheck.py nor this repository's witness verifiers were read before it was written.
It imports only the standard library and gmpy2.

A square is (x, y, a, b, s): centre (x, y), edge direction u = (a, b), side s.
Its corners are c + (s/2)(+-u +- u_perp) with u_perp = (-b, a). The schema's centre-basis
square has s = 1 and u = [cos(theta), sin(theta)], so a unit square needs a^2 + b^2 = 1
exactly; the checks test that separately and never assume it.

Two independent decision methods, each over every wall and every pair, with no distance
filter:

* Method 1, separating axes in fractions.Fraction. Two convex polygons have disjoint
  interiors exactly when some edge normal of either separates them, touching allowed:
  the facet normals of the Minkowski difference P - Q are edge normals of P or Q, and 0
  lies outside int(P - Q) = int P - int Q exactly when one facet inequality fails at 0.
  For two squares the normals are +-u_i, +-u_i_perp, +-u_j, +-u_j_perp, so the pair margin
  max over d of |(c_j - c_i).d| - w_i(d) - w_j(d) is >= 0 exactly when the interiors are
  disjoint, where w_k(d) = s_k (|u_k.d| + |u_k_perp.d|)/2 is the half-width along d. With
  unit axes the margin is a length. A wall is decided by the same half-width along e_x and
  e_y: x - w(e_x) >= 0, x + w(e_x) <= S, and the same in y.
* Method 2, clipped areas in gmpy2.mpq. The corners are formed explicitly; one square is
  clipped against the four closed half-planes of the other (Sutherland-Hodgman, exact), and
  the shoelace area of the result is the exact area of P and Q's intersection. For closed
  convex bodies int(P and Q) = int P and int Q, and a convex set has positive area exactly
  when its interior is nonempty, so area 0 is "interiors disjoint". A wall is decided by the
  corner coordinates lying in [0, S] and, again, by the clipped area of the square against
  the box equalling the square's own area.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from fractions import Fraction
from pathlib import Path

import gmpy2
from gmpy2 import mpq

RAT = re.compile(r"^(-?)(\d+)(?:/(\d+))?$")


class FormatError(ValueError):
    """The file is not in the layout this reader accepts; it fails closed."""


def sha256_file(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_rat(text: str) -> tuple[int, int]:
    """Parse '-p/q', 'p/q', '-p' or 'p' into (numerator, denominator) with q > 0."""
    m = RAT.match(text)
    if not m:
        raise FormatError(f"not a rational literal: {text!r}")
    sign, p, q = m.groups()
    num = int(p)
    den = int(q) if q is not None else 1
    if den == 0:
        raise FormatError(f"zero denominator: {text!r}")
    if sign:
        num = -num
    return num, den


def is_canonical(text: str) -> bool:
    """Lowest terms, no leading zeros, no '-0', no '/1'."""
    num, den = parse_rat(text)
    body = text.lstrip("-")
    parts = body.split("/")
    if any(len(p) > 1 and p[0] == "0" for p in parts):
        return False
    if text.startswith("-") and num == 0:
        return False
    if len(parts) == 2 and den == 1:
        return False
    return math.gcd(num, den) == 1


def unquote(token: str) -> str:
    token = token.strip()
    if len(token) >= 2 and token[0] == token[-1] == "'":
        return token[1:-1].replace("''", "'")
    if len(token) >= 2 and token[0] == token[-1] == '"':
        inner = token[1:-1]
        if "\\" in inner:
            raise FormatError(f"escaped double-quoted scalar not accepted: {token!r}")
        return inner
    if token[:1] in "&*!|>{[%@`":
        raise FormatError(f"YAML feature not accepted here: {token!r}")
    return token


HEADER_KEYS = ("id", "n", "side", "square_size", "representation")


def read_witness_yaml(path: str | Path) -> dict:
    """Read a Witness/v2 YAML file of the block layout these files use, and nothing else.

    Every line of the squares block must match the expected pattern exactly, in order;
    any other layout raises FormatError. Header fields are read from their own lines.
    Blocks after the squares (claim, source, certificate) are kept as raw text.
    """
    text = Path(path).read_text(encoding="utf-8")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    out: dict = {"path": str(path), "sha256": sha256_file(path)}
    # Top level: exactly 'softschema:' then 'witness:' at column 0.
    top = [(i, ln) for i, ln in enumerate(lines) if ln and not ln.startswith(" ")]
    top_keys = [ln for _, ln in top]
    if top_keys != ["softschema:", "witness:"]:
        raise FormatError(f"top-level keys {top_keys!r}")
    w0 = top[1][0]
    soft = {}
    for ln in lines[1:w0]:
        m = re.match(r"^  ([a-z_]+): (.+)$", ln)
        if not m:
            raise FormatError(f"softschema line {ln!r}")
        soft[m.group(1)] = unquote(m.group(2))
    out["softschema"] = soft
    i = w0 + 1
    header: dict = {}
    nested: dict = {}
    squares: list = []
    after_blocks: dict = {}
    seen_keys: list = []
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"^  ([a-z_]+):(?: (.*))?$", ln)
        if not m:
            raise FormatError(f"line {i + 1}: unexpected {ln!r}")
        key, val = m.group(1), m.group(2)
        if key in seen_keys:
            raise FormatError(f"line {i + 1}: duplicate key {key!r}")
        seen_keys.append(key)
        i += 1
        if val is not None:
            if key not in HEADER_KEYS:
                raise FormatError(f"line {i}: unexpected scalar key {key!r}")
            header[key] = unquote(val)
            continue
        if key in ("scalar", "coordinates"):
            sub = {}
            while i < len(lines) and lines[i].startswith("    "):
                mm = re.match(r"^    ([a-z_]+): (.+)$", lines[i])
                if not mm:
                    raise FormatError(f"line {i + 1}: {key} entry {lines[i]!r}")
                if mm.group(1) in sub:
                    raise FormatError(f"line {i + 1}: duplicate {key}.{mm.group(1)}")
                sub[mm.group(1)] = unquote(mm.group(2))
                i += 1
            nested[key] = sub
            continue
        if key == "squares":
            pat = [
                re.compile(r"^  - id: (\S+)$"),
                re.compile(r"^    center:$"),
                re.compile(r"^    - (\S+)$"),
                re.compile(r"^    - (\S+)$"),
                re.compile(r"^    basis:$"),
                re.compile(r"^    - (\S+)$"),
                re.compile(r"^    - (\S+)$"),
            ]
            while i < len(lines) and lines[i].startswith("  - "):
                vals = []
                for k, p in enumerate(pat):
                    if i >= len(lines):
                        raise FormatError("squares block truncated")
                    mm = p.match(lines[i])
                    if not mm:
                        raise FormatError(f"line {i + 1}: square field {k}: {lines[i]!r}")
                    if mm.groups():
                        vals.append(unquote(mm.group(1)))
                    i += 1
                sid, cx, cy, ba, bb = vals
                if not re.match(r"^[1-9]\d*$", sid):
                    raise FormatError(f"square id {sid!r}")
                squares.append({"id": int(sid), "center": [cx, cy], "basis": [ba, bb]})
            continue
        if key in ("claim", "source", "certificate"):
            raw = []
            while i < len(lines) and lines[i].startswith("    "):
                raw.append(lines[i])
                i += 1
            after_blocks[key] = "\n".join(raw)
            continue
        raise FormatError(f"line {i}: unexpected block {key!r}")
    out["header"] = header
    out["scalar"] = nested.get("scalar", {})
    out["coordinates"] = nested.get("coordinates", {})
    out["squares"] = squares
    out["after_blocks"] = after_blocks
    out["key_order"] = seen_keys
    return out


def read_witness_json(path: str | Path, gz: bool = False) -> dict:
    """Read a lab JSON export with the standard library's json module."""
    import gzip

    data = Path(path).read_bytes()
    if gz:
        data = gzip.decompress(data)
    doc = json.loads(data.decode("utf-8"))
    w = doc["witness"]
    squares = []
    for sq in w["squares"]:
        if set(sq) != {"id", "center", "basis"}:
            raise FormatError(f"json square keys {sorted(sq)}")
        squares.append(
            {"id": sq["id"], "center": list(sq["center"]), "basis": list(sq["basis"])}
        )
    return {
        "path": str(path),
        "sha256_bytes_read": sha256_bytes(data),
        "header": {k: w.get(k) for k in HEADER_KEYS},
        "scalar": w.get("scalar"),
        "coordinates": w.get("coordinates"),
        "squares": squares,
        "claim": w.get("claim"),
        "keys": sorted(w),
    }


def read_daniel_cert(path: str | Path) -> dict:
    """Read Evan Daniel's .cert layout: '#' comments, 'n side', then n lines 'x y t'.

    The 299 file's header states the meaning: unit squares, centre (x, y), rotation
    (c, s) = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2)). The basis returned is (c, s) as fractions.
    """
    lines = Path(path).read_text(encoding="utf-8").split("\n")
    body = [ln for ln in lines if ln.strip() and not ln.startswith("#")]
    comments = [ln for ln in lines if ln.startswith("#")]
    first = body[0].split()
    if len(first) != 2:
        raise FormatError(f"cert first line {body[0]!r}")
    n = int(first[0])
    side = first[1]
    rows = body[1:]
    if len(rows) != n:
        raise FormatError(f"cert has {len(rows)} rows for n = {n}")
    squares = []
    for k, ln in enumerate(rows, start=1):
        parts = ln.split()
        if len(parts) != 3:
            raise FormatError(f"cert row {k}: {ln!r}")
        x, y, t = (Fraction(*parse_rat(p)) for p in parts)
        den = 1 + t * t
        c = (1 - t * t) / den
        s = 2 * t / den
        squares.append({"id": k, "x": x, "y": y, "a": c, "b": s, "t": t})
    return {"path": str(path), "sha256": sha256_file(path), "n": n, "side": side,
            "comments": comments, "squares": squares}


def to_F(text: str) -> Fraction:
    return Fraction(*parse_rat(text))


def to_Q(text: str):
    num, den = parse_rat(text)
    return mpq(num, den)


def F_to_Q(f: Fraction):
    return mpq(f.numerator, f.denominator)


def Q_to_F(q) -> Fraction:
    return Fraction(int(q.numerator), int(q.denominator))


def frac_str(f) -> str:
    f = Fraction(f) if not isinstance(f, Fraction) else f
    return f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)


def sci(f, digits: int = 14) -> str:
    """A decimal approximation of an exact rational for display only."""
    f = Fraction(f) if not isinstance(f, Fraction) else f
    if f == 0:
        return "0"
    from decimal import Decimal, getcontext

    getcontext().prec = digits + 10
    d = Decimal(f.numerator) / Decimal(f.denominator)
    return f"{d:.{digits - 1}e}"


def decimal_places(f: Fraction, places: int, mode: str) -> str:
    """f at `places` decimals, rounded 'floor', 'ceil' or 'exact' (exact needs a finite expansion)."""
    scaled = f * 10**places
    if mode == "floor":
        k = math.floor(scaled)
    elif mode == "ceil":
        k = math.ceil(scaled)
    elif mode == "exact":
        if scaled.denominator != 1:
            raise ValueError("not exact at that many places")
        k = scaled.numerator
    else:
        raise ValueError(mode)
    sign = "-" if k < 0 else ""
    k = abs(k)
    s = str(k).rjust(places + 1, "0")
    return f"{sign}{s[:-places]}.{s[-places:]}" if places else f"{sign}{s}"


def terminating_places(f: Fraction) -> int | None:
    d = f.denominator
    p = 0
    while d % 2 == 0 or d % 5 == 0:
        if d % 10 == 0:
            d //= 10
        elif d % 2 == 0:
            d //= 2
        else:
            d //= 5
        p += 1
    if d != 1:
        return None
    # minimal places: smallest k with f * 10^k integral
    k = 0
    while (f * 10**k).denominator != 1:
        k += 1
    return k


# ---------------------------------------------------------------- the witness model


def witness_squares(doc: dict) -> list[dict]:
    """Squares as exact values in both arithmetic kernels, side 1."""
    out = []
    for sq in doc["squares"]:
        cx, cy = sq["center"]
        ba, bb = sq["basis"]
        out.append({
            "id": sq["id"],
            "F": (to_F(cx), to_F(cy), to_F(ba), to_F(bb), Fraction(1)),
            "Q": (to_Q(cx), to_Q(cy), to_Q(ba), to_Q(bb), mpq(1)),
            "text": (cx, cy, ba, bb),
        })
    return out


# ---------------------------------------------------------------- method 1: separating axes


def halfwidth_F(sq, da, db) -> Fraction:
    _, _, a, b, s = sq
    return s * (abs(a * da + b * db) + abs(-b * da + a * db)) / 2


def sat_margin_F(P, Q) -> tuple[Fraction, int]:
    """Max over the four edge axes of |dc.d| - w_P(d) - w_Q(d); also which axis (0..3)."""
    xP, yP, aP, bP, _ = P
    xQ, yQ, aQ, bQ, _ = Q
    dx = xQ - xP
    dy = yQ - yP
    best = None
    arg = -1
    for k, (da, db) in enumerate(((aP, bP), (-bP, aP), (aQ, bQ), (-bQ, aQ))):
        m = abs(dx * da + dy * db) - halfwidth_F(P, da, db) - halfwidth_F(Q, da, db)
        if best is None or m > best:
            best, arg = m, k
    return best, arg


def wall_clearances_F(sq, S: Fraction) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """(left, right, bottom, top) clearances from the half-widths along e_x and e_y."""
    x, y, _, _, _ = sq
    wx = halfwidth_F(sq, Fraction(1), Fraction(0))
    wy = halfwidth_F(sq, Fraction(0), Fraction(1))
    return (x - wx, S - x - wx, y - wy, S - y - wy)


# ---------------------------------------------------------------- method 2: clipped areas


def corners_Q(sq):
    x, y, a, b, s = sq
    h = s / 2
    ux, uy = h * a, h * b
    vx, vy = -h * b, h * a
    return [
        (x + ux + vx, y + uy + vy),
        (x - ux + vx, y - uy + vy),
        (x - ux - vx, y - uy - vy),
        (x + ux - vx, y + uy - vy),
    ]


def clip_left(poly, A, B):
    """Sutherland-Hodgman step: keep the closed half-plane left of the directed line A->B."""
    if not poly:
        return []
    ex = B[0] - A[0]
    ey = B[1] - A[1]

    def side(P):
        return ex * (P[1] - A[1]) - ey * (P[0] - A[0])

    out = []
    S = poly[-1]
    sS = side(S)
    for E in poly:
        sE = side(E)
        if sE >= 0:
            if sS < 0:
                t = sS / (sS - sE)
                out.append((S[0] + t * (E[0] - S[0]), S[1] + t * (E[1] - S[1])))
            out.append(E)
        elif sS > 0:
            t = sS / (sS - sE)
            out.append((S[0] + t * (E[0] - S[0]), S[1] + t * (E[1] - S[1])))
        S, sS = E, sE
    return out


def area2(poly):
    """Twice the signed shoelace area."""
    n = len(poly)
    if n < 3:
        return mpq(0)
    acc = mpq(0)
    for k in range(n):
        x1, y1 = poly[k]
        x2, y2 = poly[(k + 1) % n]
        acc += x1 * y2 - x2 * y1
    return acc


def is_ccw_convex(poly) -> bool:
    n = len(poly)
    for k in range(n):
        A, B, C = poly[k], poly[(k + 1) % n], poly[(k + 2) % n]
        if (B[0] - A[0]) * (C[1] - B[1]) - (B[1] - A[1]) * (C[0] - B[0]) <= 0:
            return False
    return True


def overlap_area_Q(cornersP, cornersQ):
    """Exact area of P and Q's intersection (both CCW convex)."""
    poly = list(cornersP)
    n = len(cornersQ)
    for k in range(n):
        poly = clip_left(poly, cornersQ[k], cornersQ[(k + 1) % n])
        if len(poly) < 3:
            return mpq(0)
    return area2(poly) / 2


def box_corners_Q(S):
    z = mpq(0)
    return [(z, z), (S, z), (S, S), (z, S)]


def wall_clearances_Q(cornersP, S):
    xs = [c[0] for c in cornersP]
    ys = [c[1] for c in cornersP]
    return (min(xs), S - max(xs), min(ys), S - max(ys))


def contained_by_area_Q(cornersP, S) -> tuple[bool, object, object]:
    own = area2(cornersP) / 2
    inside = overlap_area_Q(cornersP, box_corners_Q(S))
    return inside == own, own, inside


# ---------------------------------------------------------------- squared distance (measurement)


def seg_dist2_Q(P, A, B):
    ex = B[0] - A[0]
    ey = B[1] - A[1]
    L2 = ex * ex + ey * ey
    t = ((P[0] - A[0]) * ex + (P[1] - A[1]) * ey) / L2
    if t < 0:
        t = mpq(0)
    elif t > 1:
        t = mpq(1)
    fx = A[0] + t * ex - P[0]
    fy = A[1] + t * ey - P[1]
    return fx * fx + fy * fy


def dist2_squares_Q(cP, cQ):
    """Exact squared distance between two convex polygons with disjoint interiors."""
    best = None
    for verts, edges in ((cP, cQ), (cQ, cP)):
        n = len(edges)
        for v in verts:
            for k in range(n):
                d2 = seg_dist2_Q(v, edges[k], edges[(k + 1) % n])
                if best is None or d2 < best:
                    best = d2
    return best


# ---------------------------------------------------------------- whole-packing checks


def check_format(doc: dict, n_claimed: int, side_claimed: str) -> dict:
    """The format hypotheses the bound needs, each reported separately."""
    h = doc["header"]
    sc = doc.get("scalar") or {}
    co = doc.get("coordinates") or {}
    ids = [sq["id"] for sq in doc["squares"]]
    texts = [t for sq in doc["squares"] for t in (*sq["center"], *sq["basis"])]
    soft = doc.get("softschema") or {}
    res = {
        "softschema_contract": soft.get("contract"),
        "softschema_is_witness_v2": soft.get("contract") == "packing.squares:Witness/v2"
        and soft.get("envelope") == "witness",
        "witness_id": h.get("id"),
        "n_field": h.get("n"),
        "n_field_is_claimed": str(h.get("n")) == str(n_claimed),
        "square_count": len(doc["squares"]),
        "count_is_claimed": len(doc["squares"]) == n_claimed,
        "ids_unique": len(set(ids)) == len(ids),
        "ids_are_1_to_n": sorted(ids) == list(range(1, len(ids) + 1)),
        "side_field": h.get("side"),
        "side_is_claimed": h.get("side") == side_claimed,
        "square_size": h.get("square_size"),
        "square_size_is_1": h.get("square_size") == "1",
        "representation": h.get("representation"),
        "is_center_basis": h.get("representation") == "center-basis",
        "scalar_kind": sc.get("kind"),
        "is_rational": sc.get("kind") == "rational",
        "origin": co.get("origin"),
        "origin_lower_left": co.get("origin") == "lower-left",
        "axes": co.get("axes"),
        "axes_ok": co.get("axes") == "x-right-y-up",
        "scalars_total": len(texts),
        "scalars_non_canonical": sum(1 for t in texts if not is_canonical(t)),
    }
    res["all_hold"] = all(res[k] for k in (
        "softschema_is_witness_v2", "n_field_is_claimed", "count_is_claimed", "ids_unique", "side_is_claimed",
        "square_size_is_1", "is_center_basis", "is_rational", "origin_lower_left", "axes_ok"))
    return res


def decide_walls(squares: list[dict], S_F: Fraction) -> dict:
    """Every wall of every square by both methods; exact clearances must agree."""
    S_Q = F_to_Q(S_F)
    least = None
    least_at = None
    per_wall_least = [None, None, None, None]
    per_wall_at = [None, None, None, None]
    m1_out = []
    m2_out = []
    disagree = []
    area_disagree = []
    touching = []
    for sq in squares:
        c1 = wall_clearances_F(sq["F"], S_F)
        cor = corners_Q(sq["Q"])
        c2 = wall_clearances_Q(cor, S_Q)
        ok1 = all(c >= 0 for c in c1)
        ok2 = all(c >= 0 for c in c2)
        inside, own, ins = contained_by_area_Q(cor, S_Q)
        if not ok1:
            m1_out.append(sq["id"])
        if not ok2 or not inside:
            m2_out.append(sq["id"])
        if any(F_to_Q(a) != b for a, b in zip(c1, c2)):
            disagree.append(sq["id"])
        if ok2 != inside:
            area_disagree.append(sq["id"])
        for w in range(4):
            if per_wall_least[w] is None or c1[w] < per_wall_least[w]:
                per_wall_least[w] = c1[w]
                per_wall_at[w] = sq["id"]
            if c1[w] == 0:
                touching.append([sq["id"], ("left", "right", "bottom", "top")[w]])
        m = min(c1)
        if least is None or m < least:
            least, least_at = m, sq["id"]
    return {
        "squares": len(squares),
        "method1_outside": m1_out,
        "method2_outside": m2_out,
        "method1_all_inside": not m1_out,
        "method2_all_inside": not m2_out,
        "clearance_disagreements": disagree,
        "corner_vs_area_disagreements": area_disagree,
        "least_clearance": frac_str(least),
        "least_clearance_approx": sci(least),
        "least_clearance_square": least_at,
        "least_per_wall": {
            name: {"clearance": frac_str(per_wall_least[w]), "approx": sci(per_wall_least[w]),
                   "square": per_wall_at[w]}
            for w, name in enumerate(("left", "right", "bottom", "top"))
        },
        "touching": touching,
        "touching_by_wall": {name: sum(1 for _, w in touching if w == name)
                             for name in ("left", "right", "bottom", "top")},
        "touching_upright": sum(
            1 for sid, _ in touching
            if next(sq for sq in squares if sq["id"] == sid)["F"][2]
            * next(sq for sq in squares if sq["id"] == sid)["F"][3] == 0),
    }


def decide_pairs(squares: list[dict], pairs=None, near_threshold=Fraction(1, 10**6)) -> dict:
    """Every pair by both methods (or the given pairs), no distance filter."""
    corners = {sq["id"]: corners_Q(sq["Q"]) for sq in squares}
    byid = {sq["id"]: sq for sq in squares}
    ids = [sq["id"] for sq in squares]
    if pairs is None:
        pairs = [(ids[p], ids[q]) for p in range(len(ids)) for q in range(p + 1, len(ids))]
    m1_overlaps = []
    m2_overlaps = []
    disagreements = []
    least = None
    least_pair = None
    touching = []
    near = []
    for i, j in pairs:
        m, axis = sat_margin_F(byid[i]["F"], byid[j]["F"])
        area = overlap_area_Q(corners[i], corners[j])
        ov1 = m < 0
        ov2 = area > 0
        if ov1:
            m1_overlaps.append([i, j, frac_str(m)])
        if ov2:
            m2_overlaps.append([i, j, str(area)])
        if ov1 != ov2:
            disagreements.append([i, j, frac_str(m), str(area)])
        if least is None or m < least:
            least, least_pair = m, (i, j, axis)
        if m == 0:
            touching.append([i, j])
        if m < near_threshold:
            near.append((m, i, j, axis))
    near.sort()
    return {
        "pairs_decided": len(pairs),
        "method1_overlapping": m1_overlaps,
        "method2_overlapping": m2_overlaps,
        "method_disagreements": disagreements,
        "method1_all_disjoint": not m1_overlaps,
        "method2_all_disjoint": not m2_overlaps,
        "least_margin": frac_str(least) if least is not None else None,
        "least_margin_approx": sci(least) if least is not None else None,
        "least_margin_pair": list(least_pair) if least_pair else None,
        "touching_pairs": touching,
        "near": near,
    }


def gmpy2_version() -> str:
    return gmpy2.version()
