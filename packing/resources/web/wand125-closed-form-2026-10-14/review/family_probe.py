#!/usr/bin/env python3
"""Independent probes of one interval of wand125's closed-form certificate.

The release closed-form-v1 ships, per interval of delta, two family files and four region
records that this packet pins by digest and does not retain. Given one unpacked asset in
a scratch directory, this program re-derives from SPEC.md, with code of its own and no
code of the source, the parts of the argument that it can reach cheaply:

- **the family's structure** (SPEC.md sections 2.1, 3.2): the format and nonnegativity of
  F, T and V; the bottom-wall period read from T at x in [3, 4), its mass 9/5, its
  reflection symmetry and its repetition in the other six stored periods; the left wall
  of F as the transposed reflected period; the two corner remainders, nonnegative and
  inside [0, 2 + d0] x [0, 2] (F) or on the line x = 2 (T); the terminal mass m_v; the
  saving S(delta) = 99/25 + 9 delta/5 - M_C(delta) - m_v at both ends against the stored
  S_d0 and S_d1 and against the certified line alpha delta + beta of intervals.json; and
  the right-side family as T row for row;
- **the global measure** (sections 1.3, 2.1, 2.3): built here as the corner, k - 4 wall
  periods and the terminal line rotated four times, for several k and delta: its total
  segment mass equals a^2 - 4 S(delta) - (a - 18/5)^2, its support lies in [0, a]^2, and
  it equals the local family on [0, 24/5]^2 as a segment measure;
- **the records** (section 6): for each region, that every root is well formed with no
  unproved leaf, that the roots are exactly the product of four partitions of the region's
  bounds, the u-range and [d0, d1], that no root or leaf of a vertex-type test has u = 0
  inside, that the leaf kinds are the supported ones with the counts of intervals.json,
  that every root's leaves have the root's volume and lie inside it, and, for every root
  of the top region and a sample of roots of the others, that the leaves' interiors are
  pairwise disjoint, which with the volume makes an exact tiling by a route other than
  the checker's midpoint bisection;
- **the claim itself, sampled** (sections 1.2, 2.3): the mass of the global measure on
  closed unit squares, computed exactly from the pose (centre, u = tan(theta/2) rational,
  delta rational) by Cyrus-Beck clipping of every segment and exact clipping of the square
  by U, at random admissible poses in the lower-left quarter and a few elsewhere, at the
  pose families SPEC.md section 8 names as delicate, and at the poses a floating-point
  descent from many random starts finds lowest; every exact mass must be at least 1. At
  poses whose centre lies in the left, straddle or top region the local family's mass
  must equal the global one, and in the right region the right-side family's mass, in
  shifted coordinates, must not exceed it.

Run from packing/ with the project interpreter, on an asset unpacked in scratch whose
members passed sha256sum -c:

    uv run --frozen --all-extras --group dev python -I \\
        resources/web/wand125-closed-form-2026-10-14/review/family_probe.py \\
        --interval 20 --dir SCRATCH/interval_0.465_0.47 \\
        --out resources/web/wand125-closed-form-2026-10-14/review/outputs/probe-20.json

A sample decides nothing: this program can refute the claim and cannot establish it.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import random
import re
import sys
import time
from collections import Counter, defaultdict
from fractions import Fraction as Q
from itertools import pairwise
from pathlib import Path
from typing import Any

sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
INTERVALS = PACKET / "square-packing" / "problems" / "closed-form" / "intervals.json.gz"
MANIFEST = PACKET / "acquisition" / "upstream-subtree.sha256"

ALPHA = Q(9, 5)
REACH = Q(7072, 10000)
WINDOW = Q(24, 5)
HALF = Q(1, 2)
U_RANGE = (Q(-13, 32), Q(7, 16))
KINDS = {
    "EMPTY", "CORE", "B3D", "EDGE", "EX:CORE", "EX:B3D", "EY:CORE", "EY:B3D",
    "B3U:x", "B3U:y", "B3U:xy", "B3U:xyh", "B3T:x", "B3T:y", "B4U",
    "CORE1:P", "CORE1:x", "CORE1:y", "CORE1:xy", "CORE1:xyh",
    "CORE1:Tx", "CORE1:Ty", "CORE1:TxHy", "CORE1:TyHx",
}  # fmt: skip
NO_ZERO_INSIDE = KINDS - {"EMPTY", "CORE", "EDGE", "EX:CORE", "EY:CORE"}
REGIONS = ("straddle", "left", "top", "right")
_RATIONAL = re.compile(r"-?\d+(?:/[1-9]\d*)?")

# A segment measure is a list of (kind, c, lo, hi, density): kind 'v' is the vertical
# line x = c over y in [lo, hi], kind 'h' the horizontal line y = c over x in [lo, hi].
Seg = tuple[str, Q, Q, Q, Q]


def emit(line: str) -> None:
    sys.stdout.write(line + "\n")
    sys.stdout.flush()


def rational(text: object, where: str) -> Q:
    if not isinstance(text, str) or _RATIONAL.fullmatch(text) is None:
        msg = f"{where}: not an integer or p/q string: {text!r}"
        raise ValueError(msg)
    return Q(text)


# ------------------------------------------------------------------------------- inputs


def load_interval(index: int) -> dict[str, Any]:
    data = gzip.decompress(INTERVALS.read_bytes())
    want = next(
        line.split("  ")[0]
        for line in MANIFEST.read_text(encoding="utf-8").splitlines()
        if line.endswith("problems/closed-form/intervals.json")
    )
    got = hashlib.sha256(data).hexdigest()
    if got != want:
        msg = f"intervals.json: SHA-256 {got} is not the manifest's {want}"
        raise SystemExit(msg)
    rows = [r for r in json.loads(data, parse_float=str)["intervals"] if r["index"] == index]
    if len(rows) != 1:
        msg = f"interval {index} is not in intervals.json"
        raise SystemExit(msg)
    return rows[0]


class Family:
    def __init__(self, path: Path, want_sha256: str) -> None:
        data = path.read_bytes()
        self.sha256 = hashlib.sha256(data).hexdigest()
        if self.sha256 != want_sha256:
            msg = f"{path.name}: SHA-256 {self.sha256} is not intervals.json's {want_sha256}"
            raise SystemExit(msg)

        def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
            out: dict[str, Any] = {}
            for key, value in pairs:
                if key in out:
                    msg = f"duplicate key {key}"
                    raise ValueError(msg)
                out[key] = value
            return out

        doc = json.loads(data.decode("utf-8"), parse_float=str, object_pairs_hook=unique)
        self.problems: list[str] = []
        self.d0 = rational(doc["d0"], "d0")
        self.d1 = rational(doc["d1"], "d1")
        self.ua = rational(doc["UA"], "UA")
        self.s_d0 = rational(doc["S_d0"], "S_d0")
        self.s_d1 = rational(doc["S_d1"], "S_d1")
        if self.ua != ALPHA:
            self.problems.append("UA is not 9/5")
        if "U" in doc or doc.get("edge_variant"):
            self.problems.append("an explicit U or edge_variant is present")
        if not 0 <= self.d0 < self.d1 <= 1:
            self.problems.append("d0, d1 do not satisfy 0 <= d0 < d1 <= 1")
        self.rows: dict[str, list[tuple[Q, ...]]] = {"F": [], "T": [], "V": []}
        for key, width in (("F", 5), ("T", 5), ("V", 3)):
            if not isinstance(doc[key], list):
                self.problems.append(f"{key} is not an array")
                continue
            for i, raw in enumerate(doc[key]):
                label = f"{key}[{i}]"
                if not (isinstance(raw, list) and len(raw) == width):
                    self.problems.append(f"{label}: not {width} entries")
                    continue
                row = tuple(rational(v, label) for v in raw)
                if row[-1] < 0:
                    self.problems.append(f"{label}: negative mass or density")
                if key == "V":
                    xl, y, _ = row
                    if not (0 <= xl <= 2 + self.d0 and 0 <= y <= 2):
                        self.problems.append(f"{label}: V row outside the corner")
                else:
                    ax, ay, bx, by, _ = row
                    if (ax == bx) == (ay == by):
                        self.problems.append(
                            f"{label}: not an axis-parallel segment of positive length"
                        )
                self.rows[key].append(row)

    def segments(self, key: str) -> list[Seg]:
        out: list[Seg] = []
        for ax, ay, bx, by, m in self.rows[key]:
            if ax == bx:
                lo, hi = min(ay, by), max(ay, by)
                out.append(("v", ax, lo, hi, m / (hi - lo)))
            else:
                lo, hi = min(ax, bx), max(ax, bx)
                out.append(("h", ay, lo, hi, m / (hi - lo)))
        return out

    def v_segments(self, delta: Q) -> list[Seg]:
        return [("h", y, xl, 2 + delta, rho) for xl, y, rho in self.rows["V"] if xl < 2 + delta]

    def local(self, delta: Q) -> list[Seg]:
        """F + T shifted by delta + V at delta: the local family's segments."""
        return (
            self.segments("F") + shift(self.segments("T"), delta, Q(0)) + self.v_segments(delta)
        )


# ------------------------------------------------------------------- segment measures


def canonical(segs: list[Seg]) -> dict[tuple[str, Q], tuple[tuple[Q, Q, Q], ...]]:
    """The density step function on every line, as a dictionary with no zero pieces."""
    events: dict[tuple[str, Q], dict[Q, Q]] = defaultdict(lambda: defaultdict(Q))
    for kind, c, lo, hi, r in segs:
        if hi > lo and r != 0:
            events[kind, c][lo] += r
            events[kind, c][hi] -= r
    out: dict[tuple[str, Q], tuple[tuple[Q, Q, Q], ...]] = {}
    for key, changes in events.items():
        points = sorted(p for p, v in changes.items() if v != 0)
        density = Q(0)
        pieces: list[tuple[Q, Q, Q]] = []
        for lo, hi in pairwise(points):
            density += changes[lo]
            if density != 0:
                pieces.append((lo, hi, density))
        if pieces:
            out[key] = tuple(pieces)
    return out


def as_segments(measure: dict[tuple[str, Q], tuple[tuple[Q, Q, Q], ...]]) -> list[Seg]:
    return [(k, c, lo, hi, r) for (k, c), pieces in measure.items() for lo, hi, r in pieces]


def mass(segs: list[Seg]) -> Q:
    return sum(((hi - lo) * r for _, _, lo, hi, r in segs), Q(0))


def negate(segs: list[Seg]) -> list[Seg]:
    return [(k, c, lo, hi, -r) for k, c, lo, hi, r in segs]


def nonnegative(segs: list[Seg]) -> bool:
    return all(r >= 0 for _, _, _, _, r in as_segments(canonical(segs)))


def shift(segs: list[Seg], dx: Q, dy: Q) -> list[Seg]:
    return [
        ("v", c + dx, lo + dy, hi + dy, r) if k == "v" else ("h", c + dy, lo + dx, hi + dx, r)
        for k, c, lo, hi, r in segs
    ]


def transpose(segs: list[Seg]) -> list[Seg]:
    return [("h" if k == "v" else "v", c, lo, hi, r) for k, c, lo, hi, r in segs]


def rotate(segs: list[Seg], a: Q) -> list[Seg]:
    """The image under rho(x, y) = (a - y, x)."""
    out: list[Seg] = []
    for k, c, lo, hi, r in segs:
        if k == "v":
            out.append(("h", c, a - hi, a - lo, r))
        else:
            out.append(("v", a - c, lo, hi, r))
    return out


def clip(segs: list[Seg], x0: Q, x1: Q, y0: Q, y1: Q, *, right_open: bool = False) -> list[Seg]:
    """The restriction to the box; with right_open, lines at x = x1 (or y = y1) are left out."""
    out: list[Seg] = []
    for k, c, lo, hi, r in segs:
        across = (x0, x1) if k == "v" else (y0, y1)
        along = (y0, y1) if k == "v" else (x0, x1)
        if not across[0] <= c <= across[1] or (right_open and k == "v" and c == across[1]):
            continue
        a, b = max(lo, along[0]), min(hi, along[1])
        if b > a:
            out.append((k, c, a, b, r))
    return out


def reflect_period(profile: list[Seg]) -> list[Seg]:
    """x -> 1 - x on one period [0, 1), the line at phase 0 staying at 0 (the wrap)."""
    out: list[Seg] = []
    for k, c, lo, hi, r in profile:
        if k == "h":
            out.append(("h", c, 1 - hi, 1 - lo, r))
        else:
            out.append(("v", (-c) % 1, lo, hi, r))
    return out


# -------------------------------------------------------------------- the structure


def period(segs: list[Seg], base: Q, *, transposed: bool = False) -> list[Seg]:
    """One wall period [base, base + 1) of the bottom wall (or of the left wall when
    transposed, read along y), moved to [0, 1)."""
    if transposed:
        part = clip(transpose(segs), base, base + 1, Q(0), ALPHA, right_open=True)
    else:
        part = clip(segs, base, base + 1, Q(0), ALPHA, right_open=True)
    return shift(part, -base, Q(0))


def structure(fam: Family, line: tuple[Q, Q]) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    notes: dict[str, str] = {}
    f_segs, t_segs = fam.segments("F"), fam.segments("T")
    profile = as_segments(canonical(period(t_segs, Q(3))))
    checks["bottom wall period mass 9/5"] = mass(profile) == ALPHA
    checks["period reflection symmetric"] = canonical(reflect_period(profile)) == canonical(
        profile
    )
    phases = {c for k, c, _, _, _ in profile if k == "v"}
    checks["period lines on the 1/5 grid"] = all(c * 5 == int(c * 5) for c in phases) and all(
        c * 5 == int(c * 5) and 0 < c <= ALPHA for k, c, _, _, _ in profile if k == "h"
    )
    checks["six other bottom periods equal the period"] = all(
        canonical(period(t_segs, Q(2 + n))) == canonical(profile) for n in range(1, 7)
    )
    left = transpose(reflect_period(profile))
    # Period 0 of each wall may carry corner mass on its boundary line (x = 2 for T, y = 2
    # for F), which the corner remainders below account for; periods 1 to 6 must be exact.
    checks["six other left-wall periods equal the transposed reflected period"] = all(
        canonical(period(f_segs, Q(2 + n), transposed=True))
        == canonical(reflect_period(profile))
        for n in range(1, 7)
    )
    walls_t = [s for n in range(7) for s in shift(profile, Q(2 + n), Q(0))]
    walls_f = [s for n in range(7) for s in shift(left, Q(0), Q(2 + n))]
    ct = as_segments(canonical(t_segs + negate(walls_t)))
    cf = as_segments(canonical(f_segs + negate(walls_f)))
    checks["T corner remainder nonnegative, vertical lines on x = 2 within y in [0, 2]"] = all(
        k == "v" and c == 2 and 0 <= lo < hi <= 2 and r > 0 for k, c, lo, hi, r in ct
    )
    checks["F corner remainder nonnegative inside [0, 2 + d0] x [0, 2]"] = all(
        r > 0 for *_, r in cf
    ) and canonical(cf) == canonical(clip(cf, Q(0), 2 + fam.d0, Q(0), Q(2)))
    m_v = mass([s for s in profile if s[0] == "v" and s[1] == 0])
    notes["m_v"] = str(m_v)

    def saving(delta: Q) -> Q:
        corner = (
            mass(cf)
            + mass(ct)
            + sum((rho * (2 + delta - xl) for xl, _, rho in fam.rows["V"]), Q(0))
        )
        return Q(99, 25) + Q(9, 5) * delta - corner - m_v

    s0, s1 = saving(fam.d0), saving(fam.d1)
    notes["S_d0"], notes["S_d1"] = str(float(s0)), str(float(s1))
    checks["recomputed S(d0), S(d1) equal the stored S_d0, S_d1"] = (s0, s1) == (
        fam.s_d0,
        fam.s_d1,
    )
    alpha, beta = line
    checks["certified line equals S at both ends"] = (alpha * fam.d0 + beta == s0) and (
        alpha * fam.d1 + beta == s1
    )
    checks["S above delta/2 at both ends"] = s0 > fam.d0 / 2 and s1 > fam.d1 / 2
    return {
        "checks": checks,
        "notes": notes,
        "profile": profile,
        "cf": cf,
        "ct": ct,
        "m_v": m_v,
        "saving": saving,
    }


def build_global(fam: Family, parts: dict[str, Any], k: int, delta: Q) -> list[Seg]:
    """The C4-symmetric global measure of SPEC.md section 2.1 for side a = k + delta."""
    a = k + delta
    profile: list[Seg] = parts["profile"]
    base: list[Seg] = (
        list(parts["cf"]) + shift(parts["ct"], delta, Q(0)) + fam.v_segments(delta)
    )
    for n in range(k - 4):
        base += shift(profile, 2 + delta + n, Q(0))
    terminal = [s for s in profile if s[0] == "v" and s[1] == 0]
    base += shift(terminal, 2 + delta + (k - 4), Q(0))
    out: list[Seg] = []
    part = base
    for _ in range(4):
        out.extend(part)
        part = rotate(part, a)
    return out


def global_checks(
    fam: Family, parts: dict[str, Any], ks: list[int], deltas: list[Q]
) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for k in ks:
        for delta in deltas:
            a = k + delta
            mu = build_global(fam, parts, k, delta)
            expected = a * a - 4 * parts["saving"](delta) - (a - 2 * ALPHA) ** 2
            inside = canonical(mu) == canonical(clip(mu, Q(0), a, Q(0), a))
            window = canonical(clip(mu, Q(0), WINDOW, Q(0), WINDOW)) == canonical(
                clip(fam.local(delta), Q(0), WINDOW, Q(0), WINDOW)
            )
            results[f"k={k} delta={delta}"] = {
                "total mass identity": mass(mu) == expected,
                "support inside the container": inside,
                "global equals local on [0, 24/5]^2": window and a - ALPHA >= WINDOW,
                "segments": len(mu),
            }
    return results


# ------------------------------------------------------------------------- the records


Box = tuple[Q, ...]


def parse_box(raw: Any, where: str) -> Box:
    if not (isinstance(raw, list) and len(raw) == 8):
        msg = f"{where}: box is not 8 entries"
        raise ValueError(msg)
    b = tuple(rational(v, where) for v in raw)
    if any(b[i] >= b[i + 1] for i in range(0, 8, 2)):
        msg = f"{where}: nonpositive interval"
        raise ValueError(msg)
    return b


def disjoint(b1: Box, b2: Box) -> bool:
    return any(b1[i + 1] <= b2[i] or b2[i + 1] <= b1[i] for i in range(0, 8, 2))


def volume(b: Box) -> Q:
    v = Q(1)
    for i in range(0, 8, 2):
        v *= b[i + 1] - b[i]
    return v


def check_record(
    path: Path,
    region: dict[str, Any],
    fam: Family,
    rng: random.Random,
    tiling_sample: int | None,
) -> dict[str, Any]:
    data = path.read_bytes()
    sha = hashlib.sha256(data).hexdigest()
    result: dict[str, Any] = {
        "file": path.name,
        "sha256_matches": sha == region["sha256"],
        "problems": [],
    }
    problems: list[str] = result["problems"]
    axes: list[set[tuple[Q, Q]]] = [set() for _ in range(4)]
    roots: set[Box] = set()
    kinds: Counter[str] = Counter()
    n_roots = n_leaves = 0
    tiling_checked = 0
    pending: list[tuple[Box, list[Box]]] = []
    for number, line in enumerate(data.decode("utf-8").splitlines(), 1):
        where = f"{path.name}:{number}"
        row = json.loads(line)
        if "header" in row:
            continue
        box = parse_box(row["root"], where)
        if row.get("uncert") != [] or row.get("f3d", []) != []:
            problems.append(f"{where}: uncert or f3d is not empty")
        leaves: list[tuple[Box, str]] = []
        for j, leaf in enumerate(row["leaves"]):
            lb = parse_box(leaf[0], f"{where} leaf {j}")
            kind = leaf[1]
            if kind not in KINDS:
                problems.append(f"{where} leaf {j}: unsupported kind {kind}")
            if kind in NO_ZERO_INSIDE and lb[4] < 0 < lb[5]:
                problems.append(f"{where} leaf {j}: {kind} with u = 0 inside")
            if any(lb[i] < box[i] or lb[i + 1] > box[i + 1] for i in range(0, 8, 2)):
                problems.append(f"{where} leaf {j}: outside its root")
            leaves.append((lb, kind))
            kinds[kind] += 1
        n_roots += 1
        n_leaves += len(leaves)
        if box in roots:
            problems.append(f"{where}: duplicate root")
        roots.add(box)
        for i in range(4):
            axes[i].add((box[2 * i], box[2 * i + 1]))
        if box[4] < 0 < box[5]:
            problems.append(f"{where}: root with u = 0 inside")
        if sum((volume(lb) for lb, _ in leaves), Q(0)) != volume(box):
            problems.append(f"{where}: the leaves' volume is not the root's")
        boxes = [lb for lb, _ in leaves]
        if tiling_sample is None:
            pending.append((box, boxes))
        elif rng.random() * n_roots < tiling_sample:
            pending.append((box, boxes))
            if len(pending) > tiling_sample:
                pending.pop(rng.randrange(len(pending)))
        if len(problems) > 50:
            break
    for box, boxes in pending:
        tiling_checked += 1
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                if not disjoint(boxes[i], boxes[j]):
                    problems.append(f"root {[str(v) for v in box]}: leaves {i} and {j} overlap")
                    break
    # The product grid over the region's bounds, the u-range and [d0, d1].
    bounds = [rational(v, "bounds") for v in region["bounds"]]
    expect = [(bounds[0], bounds[1]), (bounds[2], bounds[3]), U_RANGE, (fam.d0, fam.d1)]
    for i, (lo, hi) in enumerate(expect):
        ivs = sorted(axes[i])
        ok = bool(ivs) and ivs[0][0] == lo and ivs[-1][1] == hi
        ok = ok and all(a < b for a, b in ivs) and all(p[1] == q[0] for p, q in pairwise(ivs))
        if not ok:
            problems.append(f"axis {i}: the root intervals do not partition [{lo}, {hi}]")
    product = 1
    for s in axes:
        product *= len(s)
    if product != len(roots) or len(roots) != n_roots:
        problems.append(f"roots are not the product grid: {n_roots} roots, product {product}")
    a_u, b_u = -U_RANGE[0], U_RANGE[1]
    if not a_u + b_u + a_u * b_u >= 1:
        problems.append("u-range does not cover 90 degrees")
    result.update(
        {
            "roots": n_roots,
            "leaves": n_leaves,
            "roots_match_intervals_json": n_roots == region["roots"],
            "leaves_match_intervals_json": n_leaves == region["leaves"],
            "leaf_kinds_match_intervals_json": dict(kinds) == region["leaf_kinds"],
            "axis_pieces": [len(s) for s in axes],
            "tiling_disjointness_checked_roots": tiling_checked,
            "ok": not problems and sha == region["sha256"],
        }
    )
    return result


# ------------------------------------------------------------------ the mass of a square


class Measure:
    """A segment measure with Lebesgue measure of density 1 on the rectangle u_box, with
    floating-point bounding boxes for the prefilter and exact clipping afterwards."""

    def __init__(self, segs: list[Seg], u_box: tuple[Q, Q, Q, Q]) -> None:
        self.exact: list[tuple[Q, Q, Q, Q, Q]] = []
        self.boxes: list[tuple[float, float, float, float]] = []
        for k, c, lo, hi, r in as_segments(canonical(segs)):
            if k == "v":
                self.exact.append((c, lo, c, hi, r))
                self.boxes.append((float(c), float(lo), float(c), float(hi)))
            else:
                self.exact.append((lo, c, hi, c, r))
                self.boxes.append((float(lo), float(c), float(hi), float(c)))
        self.floats = [tuple(float(v) for v in s) for s in self.exact]
        self.u_box = u_box
        self.u_box_f = tuple(float(v) for v in u_box)

    def candidates(self, zx: float, zy: float, w: float) -> list[int]:
        x0, x1, y0, y1 = zx - w - 1e-9, zx + w + 1e-9, zy - w - 1e-9, zy + w + 1e-9
        return [
            i
            for i, (bx0, by0, bx1, by1) in enumerate(self.boxes)
            if not (bx1 < x0 or bx0 > x1 or by1 < y0 or by0 > y1)
        ]

    def mass(self, zx: Any, zy: Any, u: Any, *, exact: bool) -> Any:
        """mu(Q(z, u)) for the closed unit square with centre z and u = tan(theta/2)."""
        one = Q(1) if exact else 1.0
        half = HALF if exact else 0.5
        d = one + u * u
        c, s = (one - u * u) / d, 2 * u / d
        w = (abs(c) + abs(s)) / 2
        normals = ((c, s), (-s, c), (-c, -s), (s, -c))
        segs = self.exact if exact else self.floats
        total = 0 * one
        for i in self.candidates(float(zx), float(zy), float(w)):
            ax, ay, bx, by, r = segs[i]
            dx, dy = bx - ax, by - ay
            t0, t1 = 0 * one, one
            empty = False
            for nx, ny in normals:
                num = half - (nx * (ax - zx) + ny * (ay - zy))
                den = nx * dx + ny * dy
                if den == 0:
                    if num < 0:
                        empty = True
                        break
                elif den > 0:
                    t1 = min(t1, num / den)
                else:
                    t0 = max(t0, num / den)
                if t1 < t0:
                    empty = True
                    break
            if not empty:
                total += r * (abs(dx) + abs(dy)) * (t1 - t0)
        # The square's vertices, counterclockwise, clipped by the rectangle U.
        poly = [
            (zx + (c * ex - s * ey) / 2, zy + (s * ex + c * ey) / 2)
            for ex, ey in ((one, one), (-one, one), (-one, -one), (one, -one))
        ]
        ux0, uy0, ux1, uy1 = self.u_box if exact else self.u_box_f
        for a_, b_, bound in (
            (one, 0 * one, -ux0),
            (0 * one, one, -uy0),
            (-one, 0 * one, ux1),
            (0 * one, -one, uy1),
        ):
            # Keep a_ x + b_ y + bound >= 0 ... written as (-a_) x + (-b_) y <= bound.
            kept: list[Any] = []
            for p, q in zip(poly, poly[1:] + poly[:1], strict=True):
                fp = -(a_ * p[0] + b_ * p[1]) - bound
                fq = -(a_ * q[0] + b_ * q[1]) - bound
                if fp <= 0:
                    kept.append(p)
                if (fp < 0 < fq) or (fq < 0 < fp):
                    t = fp / (fp - fq)
                    kept.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
            poly = kept
            if not poly:
                break
        area = 0 * one
        if len(poly) >= 3:
            for p, q in zip(poly, poly[1:] + poly[:1], strict=True):
                area += p[0] * q[1] - q[0] * p[1]
            area = abs(area) / 2
        return total + area


def half_width(u: Q) -> Q:
    d = 1 + u * u
    return ((1 - u * u) / d + abs(2 * u / d)) / 2


def admissible(zx: Q, zy: Q, u: Q, a: Q) -> bool:
    w = half_width(u)
    return zx >= w and zy >= w and zx + w <= a and zy + w <= a


def region_of(zx: Q, zy: Q, delta: Q, d1: Q) -> str | None:
    if 0 <= zx <= Q(167, 100) and 0 <= zy <= Q(19, 5):
        return "left"
    if Q(167, 100) <= zx <= Q(251, 100) + d1 and 0 <= zy <= Q(272, 100):
        return "straddle"
    if Q(167, 100) <= zx <= Q(251, 100) + d1 and Q(272, 100) <= zy <= Q(19, 5):
        return "top"
    if Q(251, 100) <= zx - delta <= Q(19, 5) and 0 <= zy <= Q(19, 5):
        return "right"
    return None


def descend(
    measure: Measure, zx: float, zy: float, u: float, *, a: float, u_lo: float, u_hi: float
) -> tuple[float, float, float, float]:
    """A pattern search for a low-mass pose in floating point: a candidate, nothing more."""

    def wf(uu: float) -> float:
        d = 1 + uu * uu
        return (abs((1 - uu * uu) / d) + abs(2 * uu / d)) / 2

    def value(x: float, y: float, uu: float) -> float:
        w = wf(uu)
        if not (u_lo <= uu <= u_hi and x >= w and y >= w and x + w <= a and y + w <= a):
            return float("inf")
        return measure.mass(x, y, uu, exact=False)

    best = value(zx, zy, u)
    step = 0.05
    while step > 1e-7:
        improved = False
        for dx, dy, du in (
            (step, 0, 0),
            (-step, 0, 0),
            (0, step, 0),
            (0, -step, 0),
            (0, 0, step / 2),
            (0, 0, -step / 2),
        ):
            v = value(zx + dx, zy + dy, u + du)
            if v < best:
                best, zx, zy, u = v, zx + dx, zy + dy, u + du
                improved = True
        if not improved:
            step /= 2
    return best, zx, zy, u


def snap(x: float, denominator: int = 10**6) -> Q:
    return Q(round(x * denominator), denominator)


def pose_probe(
    fam: Family,
    right: Family,
    parts: dict[str, Any],
    *,
    ks: list[int],
    deltas: list[Q],
    rng: random.Random,
    poses: int,
    descents: int,
) -> dict[str, Any]:
    out: dict[str, Any] = {"violations": [], "local_mismatch": [], "right_above_global": []}
    violations: list[str] = out["violations"]
    minimum: tuple[Q, str] | None = None
    checked = 0
    local_compared = right_compared = 0
    delicate = [  # SPEC.md section 8 (3), rounded to rationals; (ii) is the 45 degree pose.
        (Q(11, 2500) * -1, None, Q(2899, 1000)),
        (Q(41421, 100000), Q(240711, 100000), Q(27, 10)),
        (Q(43451, 100000), Q(256990, 100000), Q(230716, 100000)),
        (Q(-150472, 1000000), Q(24, 10), Q(1)),
    ]
    for k in ks:
        for delta in deltas:
            a = k + delta
            mu = Measure(
                build_global(fam, parts, k, delta), (ALPHA, ALPHA, a - ALPHA, a - ALPHA)
            )
            big = Q(1000)
            loc = Measure(fam.local(delta), (ALPHA, ALPHA, big, big))
            rgt = Measure(right.segments("F"), (ALPHA, ALPHA, big, big))
            samples: list[tuple[Q, Q, Q, str]] = []
            for _ in range(poses):
                u = Q(rng.randint(-13 * 128, 14 * 128), 4096)
                w = half_width(u)
                zx = w + (a / 2 + Q(1, 2) - w) * Q(rng.randint(0, 10**4), 10**4)
                zy = w + (a / 2 + Q(1, 2) - w) * Q(rng.randint(0, 10**4), 10**4)
                samples.append((zx, zy, u, "random"))
            for _ in range(max(1, poses // 20)):
                u = Q(rng.randint(-13 * 128, 14 * 128), 4096)
                w = half_width(u)
                zx = w + (a - 2 * w) * Q(rng.randint(0, 10**4), 10**4)
                zy = w + (a - 2 * w) * Q(rng.randint(0, 10**4), 10**4)
                samples.append((zx, zy, u, "anywhere"))
            for u, zx, zy in delicate:
                samples.append((half_width(u) if zx is None else zx, zy, u, "delicate"))
                samples.append(
                    (zy, half_width(u) if zx is None else zx, u, "delicate transposed")
                )
            for _ in range(descents):
                u0 = rng.uniform(float(U_RANGE[0]), float(U_RANGE[1]))
                x0 = rng.uniform(0.5, float(a) / 2 + 0.5)
                y0 = rng.uniform(0.5, float(a) / 2 + 0.5)
                _, x, y, uu = descend(
                    mu, x0, y0, u0, a=float(a), u_lo=float(U_RANGE[0]), u_hi=float(U_RANGE[1])
                )
                samples.append((snap(x), snap(y), snap(uu), "descent"))
            for zx, zy, u, how in samples:
                if not admissible(zx, zy, u, a):
                    continue
                value = mu.mass(zx, zy, u, exact=True)
                checked += 1
                label = f"k={k} delta={delta} z=({zx}, {zy}) u={u} [{how}]"
                if value < 1:
                    violations.append(f"{label}: mass {value} = {float(value)}")
                if minimum is None or value < minimum[0]:
                    minimum = (value, label)
                region = region_of(zx, zy, delta, fam.d1)
                if region in ("left", "straddle", "top"):
                    local_compared += 1
                    if loc.mass(zx, zy, u, exact=True) != value:
                        out["local_mismatch"].append(label)
                elif region == "right":
                    right_compared += 1
                    if rgt.mass(zx - delta, zy, u, exact=True) > value:
                        out["right_above_global"].append(label)
    out.update(
        {
            "poses_checked": checked,
            "minimum_mass": None
            if minimum is None
            else {"value": float(minimum[0]), "exact": str(minimum[0]), "at": minimum[1]},
            "local_compared": local_compared,
            "right_compared": right_compared,
        }
    )
    return out


# ------------------------------------------------------------------------------- driver


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--interval", type=int, required=True)
    parser.add_argument("--dir", type=Path, required=True, help="the unpacked asset directory")
    parser.add_argument(
        "--ks", default="7,8,11", help="container integer parts for the global checks"
    )
    parser.add_argument("--poses", type=int, default=400, help="random poses per (k, delta)")
    parser.add_argument(
        "--descents", type=int, default=12, help="floating-point descents per (k, delta)"
    )
    parser.add_argument(
        "--tiling-sample", type=int, default=400, help="roots per region (all for top)"
    )
    parser.add_argument("--skip-records", action="store_true")
    parser.add_argument("--seed", type=int, default=20261014)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    started = time.time()
    rng = random.Random(args.seed)
    iv = load_interval(args.interval)
    d0, d1 = Q(iv["d0"]), Q(iv["d1"])
    line = (Q(iv["certified_line"]["alpha"]), Q(iv["certified_line"]["beta"]))
    fam = Family(args.dir / "family.json", iv["family_sha256"])
    right = Family(args.dir / "family_right.json", iv["family_right_sha256"])
    emit(f"interval {args.interval}: [{d0}, {d1}], family {fam.sha256[:12]}")
    receipt: dict[str, Any] = {
        "schema": "closed-form-review-family-probe/v1",
        "program": "review/family_probe.py",
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "interval": args.interval,
        "d0": str(d0),
        "d1": str(d1),
        "family_sha256": fam.sha256,
        "family_right_sha256": right.sha256,
        "seed": args.seed,
    }
    problems = fam.problems + [f"right: {p}" for p in right.problems]
    if (fam.d0, fam.d1) != (d0, d1):
        problems.append("the family's interval is not intervals.json's")
    right_ok = right.rows["F"] == fam.rows["T"] and not right.rows["T"] and not right.rows["V"]
    right_ok = right_ok and (right.d0, right.d1, right.ua) == (fam.d0, fam.d1, fam.ua)
    receipt["format"] = {"problems": problems, "right_side_is_T_row_for_row": right_ok}
    emit(f"format problems: {problems or 'none'}; right side = T row for row: {right_ok}")

    parts = structure(fam, line)
    receipt["structure"] = {"checks": parts["checks"], "notes": parts["notes"]}
    for name, ok in parts["checks"].items():
        emit(f"{'OK ' if ok else 'NG '}structure: {name}")
    emit(f"S(d0) = {parts['notes']['S_d0']}, S(d1) = {parts['notes']['S_d1']}")

    ks = [int(k) for k in args.ks.split(",")]
    deltas = sorted({d0, d1, (d0 + d1) / 2, d0 + (d1 - d0) * Q(rng.randint(1, 999), 1000)})
    receipt["global"] = global_checks(fam, parts, ks, deltas)
    for key, res in receipt["global"].items():
        bad = [name for name, ok in res.items() if ok is False]
        failed = f"; failed {bad}" if bad else ""
        emit(f"{'OK ' if not bad else 'NG '}global {key}: {res['segments']} segments{failed}")

    if not args.skip_records:
        receipt["records"] = {}
        for name in REGIONS:
            region = iv["regions"][name]
            which = right if name == "right" else fam
            sample = None if name == "top" else args.tiling_sample
            res = check_record(args.dir / region["file"], region, which, rng, sample)
            receipt["records"][name] = res
            trouble = f"; problems {res['problems'][:3]}" if res["problems"] else ""
            emit(
                f"{'OK ' if res['ok'] else 'NG '}record {name}: {res['roots']} roots, "
                f"{res['leaves']} leaves, axis pieces {res['axis_pieces']}, disjointness on "
                f"{res['tiling_disjointness_checked_roots']} roots{trouble}"
            )

    receipt["poses"] = pose_probe(
        fam,
        right,
        parts,
        ks=ks[:2],
        deltas=deltas,
        rng=rng,
        poses=args.poses,
        descents=args.descents,
    )
    p = receipt["poses"]
    least = p["minimum_mass"] or {"value": None, "at": "-"}
    emit(
        f"poses: {p['poses_checked']} checked exactly, minimum mass {least['value']} at "
        f"{least['at']}; violations {len(p['violations'])}; local = global at "
        f"{p['local_compared']} poses with {len(p['local_mismatch'])} mismatches; right <= "
        f"global at {p['right_compared']} poses with {len(p['right_above_global'])} failures"
    )
    ok = (
        not problems
        and right_ok
        and all(parts["checks"].values())
        and all(v is not False for res in receipt["global"].values() for v in res.values())
        and all(r["ok"] for r in receipt.get("records", {}).values())
        and not p["violations"]
        and not p["local_mismatch"]
        and not p["right_above_global"]
    )
    receipt["ok"] = ok
    receipt["seconds"] = round(time.time() - started, 1)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    emit(f"{receipt['seconds']} s")
    emit("FAMILY PROBE OK" if ok else "FAMILY PROBE NG")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
