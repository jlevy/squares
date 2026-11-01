#!/usr/bin/env python3
"""Independent exact check of Karimi's filled-end two-band L packings (#847, PR #870).

Stage 4 review of the filled-end lemma, 1 November 2026. Standard library only: this
program imports nothing from the repository, the checker, the maintained routes or the
author's programs, and shares no code with any of them.

For each sampled row of a deposit's ``filled_records.csv`` (read as untrusted data, every
literal matched whole before it is converted to a Fraction), it builds the packing from
the row's seven parameters (K, bV, tV, yV, bH, tH, yH) with its own code, as the lemma's
construction states it, and decides the whole construction (every square it places, not
only the last n) exactly in integer arithmetic:

- every coordinate is scaled by one common denominator D, so every corner is an integer
  pair;
- every polygon is a unit square: consecutive edges of squared length D^2, at a right
  angle, the opposite edges equal and opposite;
- every corner lies in [0, S D]^2, S the row's side_exact;
- every pair of squares whose closed bounding boxes share a unit cell is decided by the
  separating axis theorem over the four edge normals of the pair: two convex polygons
  have disjoint interiors exactly when on some edge normal of one of them their
  projections overlap in at most one point. Touching is allowed and counted. A pair whose
  interiors meet has a common interior point, which lies in a unit cell both bounding
  boxes are registered in, so no such pair escapes the broad phase;
- the construction holds at least n squares.

Mutants, each decided by the same geometry: one more layer square at every level of each
of the four band ends and at the level after the last (the checker's layer controls, as
geometry); each lift 10^-15 past its free length; the side 10^-15 lower; and the H band
written with the wrong tilt sign (each square turned by +theta about its centre instead
of reflected). A mutant is refused when a square crosses a wall or two interiors meet.

Usage, from anywhere, with the project interpreter in isolated mode::

    python -I fe_independent.py PACKET OUT.json [--rows N ...] [--random 20] [--seed S]
    python -I fe_independent.py --self-test OUT.json
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import platform
import random
import re
import sys
import time
import zipfile
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path

COLUMNS = [
    "n",
    "K",
    "side_exact",
    "side",
    "previous_best_side",
    "previous_source",
    "bV",
    "tV",
    "yV",
    "bH",
    "tH",
    "yH",
]
_INT = re.compile(r"[1-9][0-9]{0,9}")
_RAT = re.compile(r"(?:0|[1-9][0-9]{0,39})(?:/[1-9][0-9]{0,39})?")
_DEC = re.compile(r"[0-9]{1,6}\.([0-9]{1,30})")
#: The five edge rows the lane replayed on the maintained routes.
EDGE_ROWS = (1188, 5265, 7439, 8524, 9517)
EPS = Q(1, 10**15)


class Malformed(ValueError):
    """A row this reader refuses."""


# --------------------------------------------------------------------------- ingest


def _int(text: str, where: str) -> int:
    if _INT.fullmatch(text) is None:
        raise Malformed(f"{where}: {text[:40]!r} is not a positive integer literal")
    return int(text)


def _rat(text: str, where: str) -> Q:
    if _RAT.fullmatch(text) is None:
        raise Malformed(f"{where}: {text[:40]!r} is not a rational literal")
    return Q(text)


def read_rows(text: str) -> list[dict]:
    """Every row of a filled_records.csv text, its literals converted exactly."""
    lines = list(csv.reader(io.StringIO(text, newline=""), strict=True))
    if not lines or lines[0] != COLUMNS:
        raise Malformed(f"header {lines[:1]!r}")
    rows = []
    seen = set()
    for number, fields in enumerate(lines[1:], start=1):
        where = f"row {number}"
        if len(fields) != len(COLUMNS):
            raise Malformed(f"{where}: {len(fields)} fields")
        item = dict(zip(COLUMNS, fields, strict=True))
        decimal = item["side"]
        if _DEC.fullmatch(decimal) is None or _DEC.fullmatch(item["previous_best_side"]) is None:
            raise Malformed(f"{where}: a decimal column is not a decimal")
        row = {
            "n": _int(item["n"], where),
            "K": _int(item["K"], where),
            "S": _rat(item["side_exact"], where),
            "side_decimal": decimal,
            "previous_best_side": item["previous_best_side"],
            "previous_source": item["previous_source"],
            "bV": _int(item["bV"], where),
            "tV": _rat(item["tV"], where),
            "yV": _rat(item["yV"], where),
            "bH": _int(item["bH"], where),
            "tH": _rat(item["tH"], where),
            "yH": _rat(item["yH"], where),
        }
        if row["n"] in seen:
            raise Malformed(f"{where}: n = {row['n']} twice")
        seen.add(row["n"])
        rows.append(row)
    return rows


def deposit_text(packet: Path, version: str) -> tuple[str, str]:
    """The deposit's table as text, and the SHA-256 of the bytes it was read from."""
    if version == "2":
        data = (packet / "source" / "filled_records.csv").read_bytes()
        return data.decode("utf-8"), hashlib.sha256(data).hexdigest()
    with zipfile.ZipFile(packet / "source" / "karimi_filled_end_v2.zip") as archive:
        members = [m for m in archive.infolist() if m.filename == "filled_records.csv"]
        if len(members) != 1 or members[0].file_size > 8 * 1024 * 1024:
            raise Malformed("the V1.0 archive does not hold one filled_records.csv")
        data = archive.read(members[0])
    return data.decode("utf-8"), hashlib.sha256(data).hexdigest()


# --------------------------------------------------------------------------- construction


def trig(t: Q) -> tuple[Q, Q]:
    """cos and sin of theta for t = tan(theta/2)."""
    q = t * t
    return (1 - q) / (1 + q), 2 * t / (1 + q)


def layer_counts(wide: Q, c: Q, s: Q, lift: Q) -> list[int]:
    """m_i = floor(W - a_i), a_i = max(0, s + (i + 1 - y) c/s), at levels i = 0, 1, ...
    while a_i < W (past that m_i <= 0, and a_i only grows); negative counts are kept as
    0 and trailing zeros dropped, so a zero inside the list would show."""
    counts: list[int] = []
    level = 0
    while True:
        a = max(Q(0), s + (level + 1 - lift) * c / s)
        if a >= wide:
            break
        counts.append(max(0, math.floor(wide - a)))
        level += 1
    while counts and counts[-1] == 0:
        counts.pop()
    return counts


class Band:
    """One band in its own frame, X across in [0, W] and Y along in [0, L]."""

    def __init__(self, width: int, tilt: Q, length: Q, lift: Q) -> None:
        self.width, self.tilt, self.length, self.lift = width, tilt, length, lift
        c, s = trig(tilt)
        self.c, self.s = c, s
        self.wide = width * c + s
        self.deep = width * s + c
        self.pitch = 1 / c
        if self.deep > length:
            raise Malformed("band shorter than its depth h")
        rows = math.floor((length - self.deep) / self.pitch) + 1
        # The defining property of R, checked rather than trusted.
        assert (rows - 1) * self.pitch + self.deep <= length < rows * self.pitch + self.deep
        self.rows = rows
        self.free = length - (rows - 1) * self.pitch - self.deep
        self.near = layer_counts(self.wide, c, s, lift)
        self.far = layer_counts(self.wide, c, s, self.free - lift)

    @property
    def count(self) -> int:
        return self.width * self.rows + sum(self.near) + sum(self.far)

    def layer_slack(self) -> Q | None:
        found = []
        for counts, lift in ((self.near, self.lift), (self.far, self.free - self.lift)):
            for level, held in enumerate(counts):
                if held:
                    a = max(Q(0), self.s + (level + 1 - lift) * self.c / self.s)
                    found.append(self.wide - held - a)
        return min(found) if found else None

    def row_square(self, j: int, i: int) -> list[tuple[Q, Q]]:
        """Square i of row j: P_j + u (c, s) + v (-s, c), i <= u <= i + 1, 0 <= v <= 1."""
        c, s = self.c, self.s
        px, py = s, self.lift + j * self.pitch
        return [
            (px + u * c - v * s, py + u * s + v * c)
            for u, v in ((i, 0), (i + 1, 0), (i + 1, 1), (i, 1))
        ]

    def near_square(self, level: int, x0: Q) -> list[tuple[Q, Q]]:
        return [(x0, Q(level)), (x0 + 1, Q(level)), (x0 + 1, Q(level + 1)), (x0, Q(level + 1))]

    def far_square(self, level: int, x0: Q) -> list[tuple[Q, Q]]:
        """The near-end square of the lift F - y, turned by 180 degrees about (W/2, L/2)."""
        return [(self.wide - x, self.length - y) for x, y in self.near_square(level, x0)]

    def squares(self) -> list[tuple[str, list[tuple[Q, Q]]]]:
        out = []
        for j in range(self.rows):
            for i in range(self.width):
                out.append(("row", self.row_square(j, i)))
        for level, held in enumerate(self.near):
            for q in range(held):
                out.append(("near", self.near_square(level, self.wide - held + q)))
        for level, held in enumerate(self.far):
            for q in range(held):
                out.append(("far", self.far_square(level, self.wide - held + q)))
        return out


def place_v(row: dict, pts: list[tuple[Q, Q]]) -> list[tuple[Q, Q]]:
    shift = row["K"] - row["bV"]
    return [(shift + x, y) for x, y in pts]


def place_h(row: dict, pts: list[tuple[Q, Q]]) -> list[tuple[Q, Q]]:
    """The reflection in y = x, lifted to y = K - bH: (X, Y) -> (Y, K - bH + X)."""
    shift = row["K"] - row["bH"]
    return [(y, shift + x) for x, y in pts]


def bands(row: dict, *, side: Q | None = None, lift_v: Q | None = None, lift_h: Q | None = None):
    side = row["S"] if side is None else side
    v = Band(row["bV"], row["tV"], side, row["yV"] if lift_v is None else lift_v)
    h = Band(row["bH"], row["tH"], Q(row["K"] - row["bV"]), row["yH"] if lift_h is None else lift_h)
    return v, h


def construction(
    row: dict, *, side: Q | None = None, lift_v: Q | None = None, lift_h: Q | None = None
) -> tuple[Q, list[tuple[str, list[tuple[Q, Q]]]], Band, Band]:
    """The whole construction: the grid column by column, the V band, the H band."""
    side = row["S"] if side is None else side
    v, h = bands(row, side=side, lift_v=lift_v, lift_h=lift_h)
    k = row["K"]
    polys = []
    for i in range(k - row["bV"]):
        for j in range(k - row["bH"]):
            polys.append(("grid", [(Q(i), Q(j)), (Q(i + 1), Q(j)), (Q(i + 1), Q(j + 1)), (Q(i), Q(j + 1))]))
    polys += [(f"V {part}", place_v(row, pts)) for part, pts in v.squares()]
    polys += [(f"H {part}", place_h(row, pts)) for part, pts in h.squares()]
    return side, polys, v, h


# --------------------------------------------------------------------------- the lemma's
# hypotheses, as this program reads them (for the comparison with the receipts)


def hypotheses(row: dict) -> dict:
    """The lemma's hypotheses at a row, each as a boolean, and its capacity."""
    k, side = row["K"], row["S"]
    found = {
        "K >= 2": k >= 2,
        "1 <= bV <= K - 1": 1 <= row["bV"] <= k - 1,
        "1 <= bH <= K - 1": 1 <= row["bH"] <= k - 1,
        "0 < tV < 1": 0 < row["tV"] < 1,
        "0 < tH < 1": 0 < row["tH"] < 1,
    }
    if not all(found.values()):
        return {"hypotheses": found, "holds": False}
    cv, sv = trig(row["tV"])
    ch, sh = trig(row["tH"])
    wv, wh = row["bV"] * cv + sv, row["bH"] * ch + sh
    found["V fit"] = k - row["bV"] + wv <= side
    found["H fit"] = k - row["bH"] + wh <= side
    try:
        v, h = bands(row)
    except Malformed:
        found["h <= L"] = False
        return {"hypotheses": found, "holds": False}
    found["h <= L"] = True
    found["0 <= yV <= FV"] = 0 <= row["yV"] <= v.free
    found["0 <= yH <= FH"] = 0 <= row["yH"] <= h.free
    grid = (k - row["bV"]) * (k - row["bH"])
    capacity = grid + v.count + h.count
    found["n <= capacity"] = row["n"] <= capacity
    return {
        "hypotheses": found,
        "holds": all(found.values()),
        "capacity": capacity,
        "grid": grid,
        "v_band": v.count,
        "h_band": h.count,
        "v_rows": v.rows,
        "h_rows": h.rows,
        "v_layers": [v.near, v.far],
        "h_layers": [h.near, h.far],
        "v_slack": side - (k - row["bV"]) - wv,
        "h_slack": side - (k - row["bH"]) - wh,
        "v_free": v.free,
        "h_free": h.free,
        "v_lift_room": v.free - row["yV"],
        "h_lift_room": h.free - row["yH"],
        "layer_slack": min(
            (x for x in (v.layer_slack(), h.layer_slack()) if x is not None), default=None
        ),
        "side_is_construction_side": side == k - row["bV"] + wv,
    }


# --------------------------------------------------------------------------- the geometry


def _scale(polys: list[tuple[str, list[tuple[Q, Q]]]], side: Q) -> tuple[int, int, list]:
    """One common denominator D, the side scaled, and every corner as an integer pair."""
    dens = {side.denominator}
    for _, pts in polys:
        for x, y in pts:
            dens.add(x.denominator)
            dens.add(y.denominator)
    big = math.lcm(*dens)
    scaled = [
        [(x.numerator * (big // x.denominator), y.numerator * (big // y.denominator)) for x, y in pts]
        for _, pts in polys
    ]
    return big, side.numerator * (big // side.denominator), scaled


def _normals(pts: list[tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    (x0, y0), (x1, y1), (x2, y2), _ = pts
    return (y0 - y1, x1 - x0), (y1 - y2, x2 - x1)


def separation(a: list[tuple[int, int]], b: list[tuple[int, int]], axes) -> int:
    """1 strictly separated, 0 touching (interiors disjoint), -1 interiors meet."""
    touch = False
    for ax, ay in axes:
        pa = [x * ax + y * ay for x, y in a]
        pb = [x * ax + y * ay for x, y in b]
        amin, amax, bmin, bmax = min(pa), max(pa), min(pb), max(pb)
        if amax < bmin or bmax < amin:
            return 1
        if amax == bmin or bmax == amin:
            touch = True
    return 0 if touch else -1


def _unit_square(pts: list[tuple[int, int]], d2: int) -> bool:
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pts
    e0 = (x1 - x0, y1 - y0)
    e1 = (x2 - x1, y2 - y1)
    return (
        e0[0] * e0[0] + e0[1] * e0[1] == d2
        and e1[0] * e1[0] + e1[1] * e1[1] == d2
        and e0[0] * e1[0] + e0[1] * e1[1] == 0
        and (x3 - x2, y3 - y2) == (-e0[0], -e0[1])
        and (x0 - x3, y0 - y3) == (-e1[0], -e1[1])
    )


class Verdict:
    """The geometry of one packing, decided, with what a mutant's square is checked
    against kept: the scale, the cells and the scaled squares."""

    def __init__(self, polys: list[tuple[str, list[tuple[Q, Q]]]], side: Q) -> None:
        started = time.process_time()
        self.labels = [label for label, _ in polys]
        self.side = side
        self.big, self.side_scaled, self.scaled = _scale(polys, side)
        d2 = self.big * self.big
        self.failures: list[str] = []
        self.not_unit = [k for k, pts in enumerate(self.scaled) if not _unit_square(pts, d2)]
        for k in self.not_unit[:5]:
            self.failures.append(f"square {k} ({self.labels[k]}) is not a unit square")
        least_wall = None
        self.wall_contacts = 0
        self.wall_crossings = []
        for k, pts in enumerate(self.scaled):
            crossed = False
            for x, y in pts:
                for value in (x, y, self.side_scaled - x, self.side_scaled - y):
                    least_wall = value if least_wall is None or value < least_wall else least_wall
                    if value < 0:
                        crossed = True
                    elif value == 0:
                        self.wall_contacts += 1
            if crossed:
                self.wall_crossings.append(k)
        for k in self.wall_crossings[:5]:
            self.failures.append(f"square {k} ({self.labels[k]}) crosses a wall")
        self.least_wall = Q(least_wall, self.big)
        self.cells: dict[tuple[int, int], list[int]] = defaultdict(list)
        for k, pts in enumerate(self.scaled):
            for cell in self._cells(pts):
                self.cells[cell].append(k)
        pairs = set()
        for members in self.cells.values():
            for left in range(len(members)):
                for right in range(left + 1, len(members)):
                    pairs.add((members[left], members[right]))
        self.axes = [_normals(pts) for pts in self.scaled]
        self.touching = self.strict = 0
        self.overlaps: list[tuple[int, int]] = []
        for left, right in pairs:
            verdict = separation(
                self.scaled[left], self.scaled[right], self.axes[left] + self.axes[right]
            )
            if verdict < 0:
                self.overlaps.append((left, right))
            elif verdict == 0:
                self.touching += 1
            else:
                self.strict += 1
        for left, right in sorted(self.overlaps)[:5]:
            self.failures.append(
                f"squares {left} ({self.labels[left]}) and {right} ({self.labels[right]}) overlap"
            )
        self.pairs = len(pairs)
        self.cpu = time.process_time() - started

    def _cells(self, pts: list[tuple[int, int]]):
        xs = [x for x, _ in pts]
        ys = [y for _, y in pts]
        for cx in range(min(xs) // self.big, max(xs) // self.big + 1):
            for cy in range(min(ys) // self.big, max(ys) // self.big + 1):
                yield cx, cy

    @property
    def passed(self) -> bool:
        return not self.failures

    def extra(self, label: str, pts: list[tuple[Q, Q]]) -> list[str]:
        """What one more square at ``pts`` would break: walls, then overlaps, by label.
        Its corners must share the scale (they do: a layer square's corners are a layer
        square's corners shifted by one)."""
        scaled = []
        for x, y in pts:
            sx, sy = x * self.big, y * self.big
            if sx.denominator != 1 or sy.denominator != 1:
                raise ValueError("a mutant square off the scale")
            scaled.append((int(sx), int(sy)))
        found = []
        if not _unit_square(scaled, self.big * self.big):
            found.append("not a unit square")
        if any(v < 0 for x, y in scaled for v in (x, y, self.side_scaled - x, self.side_scaled - y)):
            found.append("crosses a wall")
        axes = _normals(scaled)
        hit = set()
        for cell in self._cells(scaled):
            for k in self.cells.get(cell, ()):
                if k not in hit and separation(scaled, self.scaled[k], axes + self.axes[k]) < 0:
                    hit.add(k)
        found += sorted({f"overlaps {self.labels[k]}" for k in hit})
        return found

    def summary(self) -> dict:
        return {
            "passed": self.passed,
            "squares": len(self.scaled),
            "scale_digits": len(str(self.big)),
            "not_unit_squares": len(self.not_unit),
            "wall_crossings": len(self.wall_crossings),
            "wall_contacts": self.wall_contacts,
            "least_wall_clearance": f"{float(self.least_wall):.6e}",
            "pairs_decided": self.pairs,
            "touching_pairs": self.touching,
            "strict_pairs": self.strict,
            "overlapping_pairs": len(self.overlaps),
            "failures": self.failures,
            "cpu_seconds": round(self.cpu, 2),
        }


# --------------------------------------------------------------------------- mutants


def layer_mutants(row: dict, base: Verdict, v: Band, h: Band) -> list[dict]:
    """One more square at every level of each band end and at the level after its last:
    the square at x0 = W - m_i - 1 (near) or its 180-degree image (far), placed."""
    found = []
    for name, item, place in (("V", v, place_v), ("H", h, place_h)):
        for end, counts in (("near", item.near), ("far", item.far)):
            for level in range(len(counts) + 1):
                held = counts[level] if level < len(counts) else 0
                x0 = item.wide - held - 1
                pts = item.near_square(level, x0) if end == "near" else item.far_square(level, x0)
                broken = base.extra(f"{name} {end} +1", place(row, pts))
                found.append(
                    {"end": f"{name} {end}", "level": level, "held": held, "refused": bool(broken), "why": broken}
                )
    return found


def whole_mutant(name: str, polys, side: Q) -> dict:
    verdict = Verdict(polys, side)
    return {
        "mutant": name,
        "refused": not verdict.passed,
        "wall_crossings": len(verdict.wall_crossings),
        "overlapping_pairs": len(verdict.overlaps),
        "overlap_parts": sorted(
            {f"{verdict.labels[a]} / {verdict.labels[b]}" for a, b in verdict.overlaps}
        )[:6],
        "first_failures": verdict.failures[:3],
        "cpu_seconds": round(verdict.cpu, 2),
    }


def turned_h(row: dict, polys):
    """The H band's squares turned by +theta_H about their own centres, instead of
    reflected (the tilt sign the certificate writes, flipped)."""
    c, s = trig(row["tH"])
    half = Q(1, 2)
    out = []
    for label, pts in polys:
        if not label.startswith("H row"):
            out.append((label, pts))
            continue
        cx = sum(x for x, _ in pts) / 4
        cy = sum(y for _, y in pts) / 4
        out.append(
            (
                label,
                [(cx + c * a - s * b, cy + s * a + c * b) for a, b in ((half, half), (-half, half), (-half, -half), (half, -half))],
            )
        )
    return out


# --------------------------------------------------------------------------- one row


def literal(value: Q | None) -> str | None:
    if value is None:
        return None
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def check_row(row: dict, *, mutants: bool = True) -> dict:
    lemma = hypotheses(row)
    side, polys, v, h = construction(row)
    verdict = Verdict(polys, side)
    capacity = len(polys)
    result = {
        "n": row["n"],
        "K": row["K"],
        "side_exact": literal(side),
        "params": {key: literal(row[key]) if isinstance(row[key], Q) else row[key] for key in ("bV", "tV", "yV", "bH", "tH", "yH")},
        "side_is_K_minus_bV_plus_WV": lemma.get("side_is_construction_side"),
        "lemma_hypotheses_hold": lemma["holds"],
        "capacity": capacity,
        "lemma_capacity": lemma.get("capacity"),
        "n_at_most_capacity": row["n"] <= capacity,
        "parts": {
            "grid": sum(1 for label, _ in polys if label == "grid"),
            "V rows": sum(1 for label, _ in polys if label == "V row"),
            "V near": v.near,
            "V far": v.far,
            "H rows": sum(1 for label, _ in polys if label == "H row"),
            "H near": h.near,
            "H far": h.far,
        },
        "rows": [v.rows, h.rows],
        "free": [literal(v.free), literal(h.free)],
        "lift_room": [literal(v.free - row["yV"]), literal(h.free - row["yH"])],
        "fit_slack": [literal(lemma["v_slack"]), literal(lemma["h_slack"])],
        "layer_slack": literal(lemma["layer_slack"]),
        "geometry": verdict.summary(),
        "verified": verdict.passed and row["n"] <= capacity,
    }
    if not mutants:
        return result
    layers = layer_mutants(row, verdict, v, h)
    result["layer_plus_one"] = {
        "mutants": len(layers),
        "refused": sum(1 for item in layers if item["refused"]),
        "accepted": [item for item in layers if not item["refused"]],
        "reasons": sorted({why for item in layers for why in item["why"]}),
    }
    wholes = []
    for name, kwargs in (
        ("V lift 1e-15 past its free length", {"lift_v": v.free + EPS}),
        ("H lift 1e-15 past its free length", {"lift_h": h.free + EPS}),
        ("side 1e-15 lower", {"side": side - EPS}),
    ):
        mside, mpolys, _, _ = construction(row, **kwargs)
        wholes.append(whole_mutant(name, mpolys, mside))
    wholes.append(whole_mutant("H band turned by +theta (tilt sign flipped)", turned_h(row, polys), side))
    result["whole_mutants"] = wholes
    return result


# --------------------------------------------------------------------------- self-test


def self_test() -> dict:
    """The geometry on hand-made cases with known answers."""

    def sq(x: Q, y: Q, t: Q = Q(0)) -> list[tuple[Q, Q]]:
        c, s = trig(t)
        half = Q(1, 2)
        return [(x + c * a - s * b, y + s * a + c * b) for a, b in ((half, half), (-half, half), (-half, -half), (half, -half))]

    tiny = Q(1, 10**30)
    cases = {
        "two touching along an edge": ([sq(Q(1, 2), Q(1, 2)), sq(Q(3, 2), Q(1, 2))], Q(2), True),
        "two overlapping by 1e-30": ([sq(Q(1, 2), Q(1, 2)), sq(Q(3, 2) - tiny, Q(1, 2))], Q(2), False),
        "a square 1e-30 through the wall": ([sq(Q(1, 2) - tiny, Q(1, 2))], Q(2), False),
        "a tilted square corner-touching an axis one": (
            # t = 1/3: c = 4/5, s = 3/5; centre chosen so its lowest corner is (1, 1).
            [sq(Q(1, 2), Q(1, 2)), sq(Q(1) + Q(1, 10), Q(1) + Q(7, 10), Q(1, 3))],
            Q(3),
            True,
        ),
        "the same tilted square 1e-30 lower": (
            [sq(Q(1, 2), Q(1, 2)), sq(Q(1) + Q(1, 10), Q(1) + Q(7, 10) - tiny, Q(1, 3))],
            Q(3),
            False,
        ),
        "a polygon of side 1 + 1e-30": ([[(Q(0), Q(0)), (1 + tiny, Q(0)), (1 + tiny, 1 + tiny), (Q(0), 1 + tiny)]], Q(2), False),
    }
    found = {}
    for name, (squares, side, expected) in cases.items():
        verdict = Verdict([("case", pts) for pts in squares], side)
        found[name] = {"expected_pass": expected, "passed": verdict.passed, "failures": verdict.failures}
    return {"cases": found, "all_as_expected": all(v["expected_pass"] == v["passed"] for v in found.values())}


# --------------------------------------------------------------------------- main


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("packet", nargs="?")
    parser.add_argument("out")
    parser.add_argument("--version", default="2", choices=("1", "2"))
    parser.add_argument("--rows", type=int, nargs="*", default=list(EDGE_ROWS))
    parser.add_argument("--random", type=int, default=20)
    parser.add_argument("--seed", type=int, default=20261101)
    parser.add_argument("--no-mutants", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--all", action="store_true", help="every row, no mutants")
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args(argv)
    if args.all:
        return check_all(Path(args.packet), Path(args.out), args.version, args.workers)
    if args.self_test:
        found = self_test()
        Path(args.out).write_text(json.dumps(found, indent=1) + "\n", encoding="utf-8")
        print(json.dumps({"all_as_expected": found["all_as_expected"]}))
        return 0 if found["all_as_expected"] else 1
    packet = Path(args.packet)
    text, digest = deposit_text(packet, args.version)
    rows = read_rows(text)
    by_n = {row["n"]: row for row in rows}
    chosen = list(args.rows)
    pool = sorted(n for n in by_n if n not in set(chosen))
    drawn = sorted(random.Random(args.seed).sample(pool, args.random)) if args.random else []
    started = time.process_time()
    results = []
    for n in chosen + drawn:
        result = check_row(by_n[n], mutants=not args.no_mutants)
        results.append(result)
        print(
            json.dumps(
                {
                    "n": n,
                    "verified": result["verified"],
                    "squares": result["geometry"]["squares"],
                    "pairs": result["geometry"]["pairs_decided"],
                    "touching": result["geometry"]["touching_pairs"],
                    "cpu": result["geometry"]["cpu_seconds"],
                    "layer+1 refused": result.get("layer_plus_one", {}).get("refused"),
                    "layer+1 mutants": result.get("layer_plus_one", {}).get("mutants"),
                    "whole mutants refused": [m["refused"] for m in result.get("whole_mutants", [])],
                }
            ),
            flush=True,
        )
    receipt = {
        "program": "fe_independent.py",
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "deposit": f"V{args.version}.0",
        "table_sha256": digest,
        "rows_in_table": len(rows),
        "edge_rows": chosen,
        "random_rows": drawn,
        "seed": args.seed,
        "environment": {"python": platform.python_version(), "machine": platform.machine()},
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "cpu_seconds": round(time.process_time() - started, 1),
        "all_verified": all(r["verified"] for r in results),
        "all_layer_mutants_refused": all(r.get("layer_plus_one", {}).get("refused") == r.get("layer_plus_one", {}).get("mutants") for r in results),
        "results": results,
    }
    write_json_lines(Path(args.out), receipt, "results")
    return 0 if receipt["all_verified"] else 1


def _one(row: dict) -> list:
    """One row of the exhaustive pass, compactly: n, capacity, verified, pairs decided,
    touching pairs, wall contacts, the scale's digits and the CPU-seconds."""
    started = time.process_time()
    found = check_row(row, mutants=False)
    geometry = found["geometry"]
    return [
        row["n"],
        found["capacity"],
        found["verified"] and found["lemma_hypotheses_hold"] and found["side_is_K_minus_bV_plus_WV"],
        geometry["pairs_decided"],
        geometry["touching_pairs"],
        geometry["wall_contacts"],
        geometry["scale_digits"],
        round(time.process_time() - started, 2),
        geometry["failures"][:2],
    ]


def check_all(packet: Path, out: Path, version: str, workers: int) -> int:
    """Every row of a deposit decided by the geometry, on ``workers`` processes; the
    receipt keeps one line per K."""
    from concurrent.futures import ProcessPoolExecutor  # noqa: PLC0415

    text, digest = deposit_text(packet, version)
    rows = read_rows(text)
    started, wall = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), time.monotonic()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        found = list(pool.map(_one, rows, chunksize=16))
    by_k: dict[int, list] = defaultdict(list)
    k_of = {row["n"]: row["K"] for row in rows}
    for item in found:
        by_k[k_of[item[0]]].append(item[:-1] if not item[-1] else item)
    failed = [item for item in found if not item[2]]
    receipt = {
        "program": "fe_independent.py --all",
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "deposit": f"V{version}.0",
        "table_sha256": digest,
        "rows": len(rows),
        "verified": len(found) - len(failed),
        "failed": [item[0] for item in failed],
        "squares": sum(item[1] for item in found),
        "pairs_decided": sum(item[3] for item in found),
        "touching_pairs": sum(item[4] for item in found),
        "row_fields": [
            "n",
            "capacity",
            "verified (geometry, n <= capacity, the lemma's hypotheses, S = K - bV + WV)",
            "pairs decided",
            "touching pairs",
            "wall contacts",
            "digits of the common denominator",
            "CPU-seconds",
        ],
        "environment": {"python": platform.python_version(), "machine": platform.machine()},
        "started_utc": started,
        "wall_seconds": round(time.monotonic() - wall, 1),
        "cpu_seconds_rows": round(sum(item[7] for item in found), 1),
        "workers": workers,
        "by_K": [{"K": k, "rows": by_k[k]} for k in sorted(by_k)],
    }
    write_json_lines(out, receipt, "by_K")
    print(json.dumps({key: receipt[key] for key in ("deposit", "rows", "verified", "failed", "squares", "wall_seconds", "cpu_seconds_rows")}))
    return 0 if not failed else 1


def write_json_lines(path: Path, receipt: dict, key: str) -> None:
    """A receipt as JSON with its header indented and each item of ``key`` on one line,
    so a packet data file stays well under 1,000 lines."""
    head = {k: v for k, v in receipt.items() if k != key}
    items = receipt[key]
    text = json.dumps(head, indent=1)
    lines = [text[: text.rfind("}")].rstrip() + ",", f' "{key}": [']
    lines += [
        "  " + json.dumps(item, separators=(",", ":")) + ("," if index < len(items) - 1 else "")
        for index, item in enumerate(items)
    ]
    lines += [" ]", "}"]
    out = "\n".join(lines) + "\n"
    json.loads(out)
    path.write_text(out, encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
