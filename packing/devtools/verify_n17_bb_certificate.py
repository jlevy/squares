"""Standing verifier of n17 branch-and-bound certificates (schemas v1, v2), in exact rationals.

Retained from lane R4's review verifier (exp-249, `audit-A/verify_cert.py.txt`), with its
mathematics unchanged and its independence kept: it imports nothing from the branch and
bound (`pilot_n17_subpattern_bb`), from HiGHS, from `sqpack.hull_kernel` or from the
selector. The cells and the cap come from `check_n17_capacity_one_cover`'s exact polygons,
or from a JSON cells file whose SHA-256 the caller states. Everything else is recomputed:
pi by Machin's formula, sine and cosine by Taylor series with Lagrange remainders in
integer fixed point, the wall bound, the gap bound, the normal-angle pieces' coverage, the
three half-planes of an option (the chord lemma) or its one relaxed half-plane, the hull
cuts' right sides by exact clipping, the Farkas combinations and the bound tightenings.

Checks, named as in the certificate README: T1 to T3 the tree, B1 and B2 the boxes, P1 to
P4 the pairs, C1 to C5 the closures and rows. A node is verified fully: every round's
cuts that a multiplier references (C2), every bound (C4), the Farkas closure (C3), the
pair closure (C1), the tightened boxes (B2) and its inherited boxes (B1, against its
parent's final boxes).

Modes. Full, the default, checks every node and every enclosure and is what admission
requires. `--sample N` checks the deepest closed nodes, `N` random closed nodes of each
kind and all their ancestors, and `--trig-sample M` enclosures: a planning check.

Taylor certificates (schema v2, `header.settings.taylor`). The angles are LP columns
`t_s = theta_s - c_s` about recorded centres, over the exact ranges `[lo - c, hi - c]`.
Checks X1 to X5 of the README's Taylor section: the remainder constant is at least
sqrt(2)/4; every gap line is recomputed here (`h >= (s1 cos + s2 sin)/2`, Taylor at the
centre relative angle with this module's own sine and cosine); every Taylor cut's right
side is at most the exact least value of a three-variable LP per possible plane (the
largest Lagrangian bound over the multipliers that cancel a coefficient, which is the LP's
value); every wall line's constant is at most the recomputed one. The Farkas and bound
checks then run over the centre boxes and the offset ranges together.

The receipt names the certificate directory (repository-relative) and the manifest's name,
the cells' source, the pattern, the mode and the counts, this module's provenance read at
import (its Git blob id, the revision and whether it differs from it;
`devtools.provenance`), and PASS or FAIL with the failures. The certificate's files are
named by the SHA-256 of their bytes; the names are names, and a file is read whatever it
is called.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import random
import time
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from devtools.provenance import provenance, repository_path

SCHEMA = "n17-certificate-verification/v1"
KIND = "branch-and-bound"
PROVENANCE = provenance(Path(__file__))
MAX_FAILURES = 50

Point = tuple[Q, Q]
Box = tuple[Q, Q, Q, Q]
Span = tuple[Q, Q]
Plane = tuple[Q, Q, Q]
# A possible plane `(nx, ny, r, c, o)`: `nbar . d >= r`, and `>= c g - o` at the pose's gap.
FullPlane = tuple[Q, Q, Q, Q, Q]
Node = dict[str, Any]
SQRT2_OVER_4_SQUARED_TIMES_16 = 2  # K >= sqrt(2)/4 iff 16 K^2 >= 2 for K >= 0


class CertificateError(Exception):
    """A check fails: on one node, or on the certificate as a whole."""


# ---------------------------------------------------------------------------
# Exact constants and enclosures
# ---------------------------------------------------------------------------


def parse(text: str) -> Q:
    numerator, denominator = text.split("/")
    return Q(int(numerator), int(denominator))


def arctan_inv(n: int, terms: int) -> tuple[Q, Q]:
    """An enclosure of arctan(1/n): an alternating series with decreasing terms."""
    total = Q(0)
    sign = 1
    last = Q(0)
    for k in range(terms):
        term = Q(1, (2 * k + 1) * n ** (2 * k + 1))
        total += sign * term
        last = term
        sign = -sign
    # After an even number of terms the partial sum is below, the next term above.
    if terms % 2 == 0:
        return total, total + last
    return total - last, total


def pi_enclosure() -> tuple[Q, Q]:
    a_lo, a_hi = arctan_inv(5, 40)
    b_lo, b_hi = arctan_inv(239, 20)
    return 16 * a_lo - 4 * b_hi, 16 * a_hi - 4 * b_lo


PI_LO, PI_HI = pi_enclosure()
HP_LO, HP_HI = PI_LO / 2, PI_HI / 2
TWO_PI = (2 * PI_LO, 2 * PI_HI)


def constants_hold() -> bool:
    """Machin's enclosure is tight and agrees with twenty digits of pi."""
    below, above = Q("3.14159265358979323846"), Q("3.14159265358979323847")
    width = PI_HI - PI_LO
    return width < Q(1, 10**40) and below < PI_LO < PI_HI < above


def half_pi_multiple(k: int) -> Span:
    if k == 0:
        return Q(0), Q(0)
    if k > 0:
        return k * HP_LO, k * HP_HI
    return k * HP_HI, k * HP_LO


KBITS = 160
SCALE = 1 << KBITS
_TRIG: dict[Q, tuple[Q, Q, Q, Q]] = {}


def cos_sin(t: Q) -> tuple[Q, Q, Q, Q]:
    """Enclosures `[cos_lo, cos_hi, sin_lo, sin_hi]` of cos t and sin t, width about 2^-158."""
    cached = _TRIG.get(t)
    if cached is not None:
        return cached
    result = cos_sin_bits(t, KBITS)
    _TRIG[t] = result
    return result


def cos_sin_bits(t: Q, bits: int) -> tuple[Q, Q, Q, Q]:
    """The same enclosures in `bits`-bit integer fixed point, width about 2^(2 - bits)."""
    scale = 1 << bits
    num, den = t.numerator, t.denominator
    # Terms t^n / n! scaled by 2^bits, as integer intervals [floor, ceil].
    c_lo = c_hi = s_lo = s_hi = 0
    power_num, power_den = 1, 1
    fact = 1
    n = 0
    while True:
        value_num = power_num * scale
        value_den = power_den * fact
        lo, hi = value_num // value_den, -((-value_num) // value_den)
        if n % 2 == 0:
            if (n // 2) % 2 == 0:
                c_lo += lo
                c_hi += hi
            else:
                c_lo -= hi
                c_hi -= lo
        elif ((n - 1) // 2) % 2 == 0:
            s_lo += lo
            s_hi += hi
        else:
            s_lo -= hi
            s_hi -= lo
        n += 1
        power_num *= num
        power_den *= den
        fact *= n
        # The Lagrange remainder of the next term, |t|^n / n!, rounded up.
        tail = -((-abs(power_num) * scale) // (power_den * fact)) + 1
        if tail <= 2 and n > 2:
            break
    # The remainders for cos (next even term) and sin (next odd term) are both at most the
    # tail at the current n, since the terms decrease once |t| < n.
    return (
        Q(c_lo - tail, scale),
        Q(c_hi + tail, scale),
        Q(s_lo - tail, scale),
        Q(s_hi + tail, scale),
    )


# An enclosure narrower than the default precision can resolve (a float sine near an
# exact zero is 2^-1074 wide) is re-checked at this precision before it is refused.
PRECISE_BITS = 2400


def least_abs(lo: Q, hi: Q) -> Q:
    if lo >= 0:
        return lo
    if hi <= 0:
        return -hi
    return Q(0)


def most_abs(lo: Q, hi: Q) -> Q:
    return max(-lo, hi)


def h_at(t: Q) -> Q:
    """A lower bound of h(t) = (|cos t| + |sin t|)/2."""
    c_lo, c_hi, s_lo, s_hi = cos_sin(t)
    return (least_abs(c_lo, c_hi) + least_abs(s_lo, s_hi)) / 2


def meets_multiple(lo: Q, hi: Q) -> bool:
    """Whether `[lo, hi]` may contain a multiple of pi/2 (conservative, tight enclosure)."""
    if hi - lo >= HP_LO:
        return True
    k_min = math.floor(float(lo) / (math.pi / 2)) - 2
    k_max = math.ceil(float(hi) / (math.pi / 2)) + 2
    for k in range(k_min, k_max + 1):
        m_lo, m_hi = half_pi_multiple(k)
        if lo <= m_hi and hi >= m_lo:
            return True
    return False


def h_lower(lo: Q, hi: Q) -> Q:
    if meets_multiple(lo, hi):
        return Q(1, 2)
    return max(Q(1, 2), min(h_at(lo), h_at(hi)))


def gap_lower(ai: Q, bi: Q, aj: Q, bj: Q) -> Q:
    if aj <= bi and ai <= bj:
        return Q(1)
    lo, hi = aj - bi, bj - ai
    if meets_multiple(lo, hi):
        return Q(1)
    return max(Q(1), Q(1, 2) + min(h_at(lo), h_at(hi)))


def sqrt_upper(value: Q) -> Q:
    """An upper bound of sqrt(value) for value >= 0."""
    if value <= 0:
        return Q(0)
    scale = 10**30
    n = math.isqrt(int(value * scale * scale)) + 1
    return Q(n, scale)


# ---------------------------------------------------------------------------
# Geometry in exact rationals
# ---------------------------------------------------------------------------


def clip_polygon(polygon: list[Point], a: Q, b: Q, c: Q) -> list[Point]:
    """Keep the closed half-plane `a x + b y <= c`."""
    result: list[Point] = []
    for index, start in enumerate(polygon):
        end = polygon[(index + 1) % len(polygon)]
        f_start = a * start[0] + b * start[1] - c
        f_end = a * end[0] + b * end[1] - c
        if f_start <= 0:
            result.append(start)
        if f_start * f_end < 0:
            t = f_start / (f_start - f_end)
            result.append(
                (start[0] + t * (end[0] - start[0]), start[1] + t * (end[1] - start[1]))
            )
    return result


def clip_cell_to_box(cell: list[Point], box: Box) -> Box | None:
    xl, xh, yl, yh = box
    if xl > xh or yl > yh:
        return None
    current = list(cell)
    for a, b, c in ((Q(-1), Q(0), -xl), (Q(1), Q(0), xh), (Q(0), Q(-1), -yl), (Q(0), Q(1), yh)):
        current = clip_polygon(current, a, b, c)
        if not current:
            return None
    xs = [p[0] for p in current]
    ys = [p[1] for p in current]
    return (max(xl, min(xs)), min(xh, max(xs)), max(yl, min(ys)), min(yh, max(ys)))


def box_contains(outer: Box, inner: Box) -> bool:
    return (
        outer[0] <= inner[0]
        and inner[1] <= outer[1]
        and outer[2] <= inner[2]
        and inner[3] <= outer[3]
    )


def contract(cell: list[Point], box: Box, angle: Span, cap: Q) -> Box | None:
    h = h_lower(*angle)
    walled = (max(box[0], h), min(box[1], cap - h), max(box[2], h), min(box[3], cap - h))
    return clip_cell_to_box(cell, walled)


def box_max_linear(nx: Q, ny: Q, dx: Span, dy: Span) -> Q:
    return (nx * dx[1] if nx >= 0 else nx * dx[0]) + (ny * dy[1] if ny >= 0 else ny * dy[0])


def interval_mul(a: Span, b: Span) -> Span:
    products = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return min(products), max(products)


def enclosed_max(c: Span, s: Span, dx: Span, dy: Span) -> Q:
    """The max over the box and over normals (cos, sin) in the enclosure of `n . d`."""
    px = interval_mul(c, dx)
    py = interval_mul(s, dy)
    return px[1] + py[1]


def plane_box_min(u: Point, plane: Plane, dx: Span, dy: Span) -> Q | None:
    """The exact min of `u . d` over the box meet `{n . d >= r}`; None when empty."""
    nx, ny, r = plane
    polygon = [(dx[0], dy[0]), (dx[1], dy[0]), (dx[1], dy[1]), (dx[0], dy[1])]
    clipped = clip_polygon(polygon, -nx, -ny, -r)
    if not clipped:
        return None
    return min(u[0] * p[0] + u[1] * p[1] for p in clipped)


def cross(o: Point, a: Point, b: Point) -> Q:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def hull_vertices(points: list[Point]) -> set[Point]:
    """The vertex set of the convex hull (monotone chain)."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return set(pts)
    lower: list[Point] = []
    upper: list[Point] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return set(lower[:-1] + upper[:-1])


# ---------------------------------------------------------------------------
# The cells and the certificate's objects
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Cells:
    """The frame: cell names and exact polygons, the cap, and their source."""

    polygons: dict[str, tuple[Point, ...]]
    cap: Q
    source: dict[str, Any]


def cover_cells() -> Cells:
    """The n17 unique-state cover's exact cells, from the cover tool."""
    from devtools import check_n17_capacity_one_cover as cover  # noqa: PLC0415

    cells = cover.build_cover(cover.UNIQUE_24)
    return Cells(
        {cell.name: tuple((Q(x), Q(y)) for x, y in cell.vertices) for cell in cells},
        Q(cover.U),
        {"kind": "cover", "design": cover.UNIQUE_24.name},
    )


def file_cells(path: Path, sha256: str) -> Cells:
    """Cells from a JSON file `{"U", "order", "cells"}` whose digest must be `sha256`."""
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != sha256:
        raise ValueError(f"cells file digest {digest} is not the stated one")
    data = json.loads(raw)
    return Cells(
        {name: tuple((Q(x), Q(y)) for x, y in data["cells"][name]) for name in data["order"]},
        Q(data["U"]),
        {"kind": "file", "path": str(path), "sha256": digest},
    )


def read_named(directory: Path, name: str) -> Any:
    return json.loads(gzip.decompress((directory / f"{name}.json.gz").read_bytes()))


def manifest_from_readme(directory: Path) -> str:
    readme = (directory / "README.txt").read_text(encoding="utf-8")
    return readme.strip().splitlines()[-1].split(":")[-1].strip().removesuffix(".json.gz")


class Verifier:
    def __init__(self, directory: Path, manifest_name: str) -> None:
        self.directory = directory
        self.manifest: dict[str, Any] = read_named(directory, manifest_name)
        header = self.manifest["header"]
        self.cap = parse(header["cap"])
        self.cells: list[list[Point]] = [
            [(parse(x), parse(y)) for x, y in cell] for cell in header["cells"]
        ]
        self.k = len(self.cells)
        self.pairs: list[tuple[int, int]] = [(p[0], p[1]) for p in header["pairs"]]
        self.root_angles: list[Span] = [
            (parse(lo), parse(hi)) for lo, hi in header["root_angles"]
        ]
        self.root_boxes: list[Box] = [
            (parse(b[0]), parse(b[1]), parse(b[2]), parse(b[3])) for b in header["root_boxes"]
        ]
        self.rows_of_cell: list[list[Plane]] = []
        for cell in self.cells:
            rows: list[Plane] = []
            for e, (x0, y0) in enumerate(cell):
                x1, y1 = cell[(e + 1) % len(cell)]
                a, b = y1 - y0, x0 - x1
                rows.append((a, b, a * x0 + b * y0))
            self.rows_of_cell.append(rows)
        settings = header.get("settings", {})
        self.taylor = bool(settings.get("taylor", False))
        self.taylor_k = parse(settings["taylor_k"]) if self.taylor else Q(0)
        self.failures: list[str] = []
        self.counts: dict[str, int] = {}

    def tick(self, what: str) -> None:
        self.counts[what] = self.counts.get(what, 0) + 1

    def fail(self, what: str) -> None:
        self.failures.append(what)

    # -- header ---------------------------------------------------------------------

    def check_header(self, cells: Cells) -> None:
        header = self.manifest["header"]
        if self.cap != cells.cap:
            self.fail(f"header cap {self.cap} is not the cells' cap {cells.cap}")
        for name, cell in zip(header["pattern"], self.cells, strict=True):
            if name not in cells.polygons:
                self.fail(f"header cell {name} is not in the cells' source")
            elif hull_vertices(list(cells.polygons[name])) != set(cell):
                self.fail(f"header cell {name} differs from the cells' source")
            n = len(cell)
            for e in range(n):
                o, a, b = cell[e], cell[(e + 1) % n], cell[(e + 2) % n]
                if cross(o, a, b) <= 0:
                    self.fail(f"header cell {name} is not strictly counterclockwise")
        schema = self.manifest.get("schema")
        expected_schema = (
            "n17-subpattern-bb-certificate/v2"
            if self.taylor
            else "n17-subpattern-bb-certificate/v1"
        )
        if schema != expected_schema:
            self.fail(f"schema {schema} does not match the Taylor setting {self.taylor}")
        if self.taylor and not (
            self.taylor_k >= 0 and 16 * self.taylor_k**2 >= SQRT2_OVER_4_SQUARED_TIMES_16
        ):
            self.fail(f"taylor_k {self.taylor_k} is below sqrt(2)/4")
        expected_pairs = [(i, j) for i in range(self.k) for j in range(i + 1, self.k)]
        if self.pairs != expected_pairs:
            self.fail("header pairs are not all pairs")
        for lo, hi in self.root_angles:
            if not hi - lo > HP_HI:
                self.fail(f"root angle interval [{lo}, {hi}] narrower than pi/2")
        for cell, box in zip(self.cells, self.root_boxes, strict=True):
            xs = [p[0] for p in cell]
            ys = [p[1] for p in cell]
            if not box_contains(box, (min(xs), max(xs), min(ys), max(ys))):
                self.fail("root box misses its cell")
        for key, (lo, hi) in header["half_pi_multiples"].items():
            m_lo, m_hi = half_pi_multiple(int(key))
            if not (parse(lo) <= m_lo and m_hi <= parse(hi)):
                self.fail(f"half_pi_multiples[{key}] does not enclose k pi/2")
        self.tick("header")

    def check_trig(self, trig: dict[str, list[str]], limit: int | None, seed: int) -> None:
        keys = list(trig)
        if limit is not None and limit < len(keys):
            keys = random.Random(seed).sample(keys, limit)
        bad = 0
        for key in keys:
            t = parse(key)
            c_lo, c_hi, s_lo, s_hi, nx, ny = (parse(v) for v in trig[key])
            mine = cos_sin(t)
            ok = c_lo <= mine[0] and mine[1] <= c_hi and s_lo <= mine[2] and mine[3] <= s_hi
            if not ok:
                mine = cos_sin_bits(t, PRECISE_BITS)
                ok = c_lo <= mine[0] and mine[1] <= c_hi and s_lo <= mine[2] and mine[3] <= s_hi
            ok = ok and c_lo <= nx <= c_hi and s_lo <= ny <= s_hi
            if not ok:
                bad += 1
                if bad <= 5:
                    self.fail(f"trig enclosure at {float(t)} is not an enclosure")
        self.counts["trig_checked"] = len(keys)
        self.counts["trig_bad"] = bad

    # -- pairs ----------------------------------------------------------------------

    def planes_of_piece(
        self, piece: tuple[Q, Q, Q], g_lo: Q, dx: Span, dy: Span
    ) -> list[FullPlane]:
        """The possible half-planes of one piece, `(nx, ny, r, c, o)`: `nbar . d >= r`
        with `r = c g_lo - o`, and `nbar . d >= c g - o` at every pose's own gap (X3)."""
        lo, hi, m = piece
        if not lo <= m <= hi:
            raise CertificateError(f"piece point {m} outside [{lo}, {hi}]")
        reach = most_abs(*dx) + most_abs(*dy)
        planes: list[FullPlane] = []
        if hi - lo < HP_LO:
            x = max(m - lo, hi - m)
            factor = 1 - x * x / 2
            for angle, c in ((lo, Q(1)), (hi, Q(1)), (m, factor)):
                base = g_lo * c
                c_lo, c_hi, s_lo, s_hi = cos_sin(angle)
                if enclosed_max((c_lo, c_hi), (s_lo, s_hi), dx, dy) < base:
                    continue
                nx, ny = (c_lo + c_hi) / 2, (s_lo + s_hi) / 2
                eps = max(c_hi - c_lo, s_hi - s_lo)
                r = base - eps * reach
                if box_max_linear(nx, ny, dx, dy) < r:
                    continue
                planes.append((nx, ny, r, c, eps * reach))
        else:
            c_lo, c_hi, s_lo, s_hi = cos_sin(m)
            tau = max(m - lo, hi - m) / 2
            perp = interval_mul((-s_hi, -s_lo), dx)
            perp2 = interval_mul((c_lo, c_hi), dy)
            spread = most_abs(perp[0] + perp2[0], perp[1] + perp2[1])
            length = sqrt_upper(most_abs(*dx) ** 2 + most_abs(*dy) ** 2)
            nx, ny = (c_lo + c_hi) / 2, (s_lo + s_hi) / 2
            eps = max(c_hi - c_lo, s_hi - s_lo)
            offset = 2 * tau * (spread + tau * length) + eps * reach
            r = g_lo - offset
            if box_max_linear(nx, ny, dx, dy) >= r:
                planes.append((nx, ny, r, Q(1), offset))
        return planes

    def check_pieces_cover(
        self,
        pieces: list[tuple[Q, Q, Q]],
        angles: tuple[Span, Span],
        window: Span | None,
    ) -> bool:
        """P2: the eight normal sets, within the window modulo 2 pi, lie in the pieces."""
        merged: list[Span] = []
        for lo, hi, _ in sorted(pieces):
            if merged and lo <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], hi))
            else:
                merged.append((lo, hi))

        def covered(lo: Q, hi: Q) -> bool:
            return any(a <= lo and hi <= b for a, b in merged)

        for a, b in angles:
            for k in range(4):
                m_lo, m_hi = half_pi_multiple(k)
                s = (a + m_lo, b + m_hi)
                if window is None:
                    if not covered(*s):
                        return False
                    continue
                for turns in (-1, 0, 1):
                    if turns == 1:
                        shifted = (s[0] + TWO_PI[0], s[1] + TWO_PI[1])
                    elif turns == -1:
                        shifted = (s[0] - TWO_PI[1], s[1] - TWO_PI[0])
                    else:
                        shifted = s
                    lo, hi = max(shifted[0], window[0]), min(shifted[1], window[1])
                    if lo <= hi and not covered(lo, hi):
                        return False
        return True

    def pair_planes(
        self, node: Node, round_record: dict[str, Any], pair: int, boxes: list[Box]
    ) -> tuple[list[list[FullPlane]], list[tuple[Q, Q, Q]], Span, Span]:
        """Every possible plane of a pair in a round, after checking P2, and the d-box."""
        i, j = self.pairs[pair]
        dx = (boxes[j][0] - boxes[i][1], boxes[j][1] - boxes[i][0])
        dy = (boxes[j][2] - boxes[i][3], boxes[j][3] - boxes[i][2])
        pieces: list[tuple[Q, Q, Q]] = [
            (parse(p[0]), parse(p[1]), parse(p[2])) for p in round_record["pairs"][str(pair)]
        ]
        window = node["window_map"].get(pair)
        angles = (node["angles_q"][i], node["angles_q"][j])
        if not self.check_pieces_cover(pieces, angles, window):
            raise CertificateError(
                f"node {node['id']} pair {pair}: pieces do not cover the normals"
            )
        ai, bi = node["angles_q"][i]
        aj, bj = node["angles_q"][j]
        g_lo = gap_lower(ai, bi, aj, bj)
        per_piece = [self.planes_of_piece(piece, g_lo, dx, dy) for piece in pieces]
        return per_piece, pieces, dx, dy

    # -- rows -----------------------------------------------------------------------

    def row_of(
        self,
        ref: list[Any],
        cuts: list[tuple[Any, ...]],
        context: tuple[Node, dict[str, Any], list[Box], dict[int, Any]],
    ) -> tuple[tuple[int, ...], tuple[Q, ...], Q]:
        """`(columns, coefficients, rhs)` of a referenced row; a cut is checked by C2."""
        node, round_record, boxes, plane_cache = context
        if ref[0] == "c":
            s, e = ref[1], ref[2]
            a, b, c = self.rows_of_cell[s][e]
            return ((2 * s, 2 * s + 1), (a, b), c)
        if ref[0] == "w":
            return self.wall_row(node, round_record["walls"][ref[1]])
        t = ref[1]
        if len(cuts[t]) == 8:
            return self.taylor_cut_row(node, cuts[t], context)
        p, ux, uy, v = cuts[t]
        i, j = self.pairs[p]
        if p not in plane_cache:
            plane_cache[p] = self.pair_planes(node, round_record, p, boxes)
        per_piece, _, dx, dy = plane_cache[p]
        least: Q | None = None
        for planes in per_piece:
            for plane in planes:
                value = plane_box_min((ux, uy), plane[:3], dx, dy)
                if value is not None and (least is None or value < least):
                    least = value
        if least is None:
            # No plane is possible: the pair is infeasible, and any cut is valid.
            self.tick("vacuous_cut")
        elif v > least:
            raise CertificateError(
                f"node {node['id']} cut {t} of pair {p}: v={float(v)} > min {float(least)}"
            )
        self.tick("cut_ok")
        return ((2 * i, 2 * i + 1, 2 * j, 2 * j + 1), (ux, uy, -ux, -uy), -v)

    # -- Taylor rows (X1 to X5) ---------------------------------------------------------

    def gap_line_constant(
        self, node: Node, pair: int, s1: int, s2: int, b: Q
    ) -> tuple[Q, Span]:
        """X2: the largest valid `a` of the gap line `(s1, s2, b)`, and the offset range A."""
        i, j = self.pairs[pair]
        centres, offsets = node["centres_q"], node["offsets_q"]
        span = (offsets[j][0] - offsets[i][1], offsets[j][1] - offsets[i][0])
        rho = max(-span[0], span[1])
        constant = Q(1, 2) + self.line_constant(centres[j] - centres[i], s1, s2, b, rho)
        return constant, span

    def line_constant(self, angle: Q, s1: int, s2: int, b: Q, rho: Q) -> Q:
        """`min f - max |f' - b| rho - K rho^2` at `angle`, f = (s1 cos + s2 sin)/2."""
        if s1 not in (1, -1) or s2 not in (1, -1):
            raise CertificateError(f"line signs ({s1}, {s2}) are not +-1")
        c_lo, c_hi, s_lo, s_hi = cos_sin(angle)
        cos_part = (c_lo, c_hi) if s1 > 0 else (-c_hi, -c_lo)
        sin_part = (s_lo, s_hi) if s2 > 0 else (-s_hi, -s_lo)
        f_lo = (cos_part[0] + sin_part[0]) / 2
        # f' = (s2 cos - s1 sin)/2
        cos_d = (c_lo, c_hi) if s2 > 0 else (-c_hi, -c_lo)
        sin_d = (s_lo, s_hi) if s1 > 0 else (-s_hi, -s_lo)
        d_lo, d_hi = (cos_d[0] - sin_d[1]) / 2, (cos_d[1] - sin_d[0]) / 2
        spread = max(d_hi - b, b - d_lo)
        return f_lo - spread * rho - self.taylor_k * rho * rho

    def taylor_cut_row(
        self,
        node: Node,
        cut: tuple[Any, ...],
        context: tuple[Node, dict[str, Any], list[Box], dict[int, Any]],
    ) -> tuple[tuple[int, ...], tuple[Q, ...], Q]:
        """X4: a Taylor cut's row, after checking its right side against every plane."""
        _, round_record, boxes, plane_cache = context
        if not self.taylor:
            raise CertificateError(
                f"node {node['id']}: a Taylor cut in an interval certificate"
            )
        p, ux, uy, v, w, s1, s2, b = cut
        i, j = self.pairs[p]
        a, span = self.gap_line_constant(node, p, s1, s2, b)
        if p not in plane_cache:
            plane_cache[p] = self.pair_planes(node, round_record, p, boxes)
        per_piece, _, dx, dy = plane_cache[p]
        least: Q | None = None
        for planes in per_piece:
            for plane in planes:
                value = taylor_plane_min((ux, uy), w, plane, (a, b), (dx, dy, span))
                if least is None or value < least:
                    least = value
        if least is None:
            self.tick("vacuous_cut")
        elif v > least:
            raise CertificateError(
                f"node {node['id']} Taylor cut of pair {p}: v={float(v)} > min {float(least)}"
            )
        self.tick("taylor_cut_ok")
        k = self.k
        return (
            (2 * i, 2 * i + 1, 2 * j, 2 * j + 1, 2 * k + i, 2 * k + j),
            (ux, uy, -ux, -uy, -w, w),
            -v,
        )

    def wall_row(self, node: Node, wall: list[Any]) -> tuple[tuple[int, ...], tuple[Q, ...], Q]:
        """X5: a wall line's row, after checking its constant."""
        if not self.taylor:
            raise CertificateError(f"node {node['id']}: a wall row in an interval certificate")
        s, axis, side = wall[0], wall[1], wall[2]
        s1, s2, b, a = wall[3], wall[4], parse(wall[5]), parse(wall[6])
        if axis not in (0, 1) or side not in (1, -1):
            raise CertificateError(f"node {node['id']}: malformed wall row {wall}")
        offset = node["offsets_q"][s]
        rho = max(-offset[0], offset[1])
        if a > self.line_constant(node["centres_q"][s], s1, s2, b, rho):
            raise CertificateError(f"node {node['id']}: wall line of square {s} too high")
        self.tick("wall_ok")
        columns = (2 * s + axis, 2 * self.k + s)
        if side == 1:
            return (columns, (Q(-1), b), -a)
        return (columns, (Q(1), b), self.cap - a)

    def combination_min(
        self,
        multipliers: list[Any],
        cost: tuple[int, Q] | None,
        cuts: list[tuple[Any, ...]],
        context: tuple[Node, dict[str, Any], list[Box], dict[int, Any]],
    ) -> Q:
        """The min over the box of `(cost + sum y a_row) . z - sum y b_row`, exactly."""
        node, _, boxes, _ = context
        combined = [Q(0)] * ((3 if self.taylor else 2) * self.k)
        if cost is not None:
            combined[cost[0]] += cost[1]
        right = Q(0)
        for ref, y_text in multipliers:
            y = parse(y_text)
            if y < 0:
                raise CertificateError(f"node {node['id']}: negative multiplier")
            columns, coefficients, rhs = self.row_of(ref, cuts, context)
            for column, coefficient in zip(columns, coefficients, strict=True):
                combined[column] += y * coefficient
            right += y * rhs
        least = Q(0)
        for column, coefficient in enumerate(combined):
            if column < 2 * self.k:
                box = boxes[column // 2]
                lo, hi = (box[0], box[1]) if column % 2 == 0 else (box[2], box[3])
            else:
                lo, hi = node["offsets_q"][column - 2 * self.k]
            least += coefficient * (lo if coefficient >= 0 else hi)
        return least - right

    # -- one node -------------------------------------------------------------------

    def check_closed_pair(self, node: Node, record: dict[str, Any], boxes: list[Box]) -> None:
        p, kind = record["closed_pair"]
        i, j = self.pairs[p]
        dx = (boxes[j][0] - boxes[i][1], boxes[j][1] - boxes[i][0])
        dy = (boxes[j][2] - boxes[i][3], boxes[j][3] - boxes[i][2])
        if kind == "disc":
            far = most_abs(*dx) ** 2 + most_abs(*dy) ** 2
            if not far < 1:
                raise CertificateError(
                    f"node {node['id']}: disc closure with max |d|^2 = {float(far)}"
                )
            self.tick("closed_disc_ok")
        elif kind == "pair":
            per_piece, _, _, _ = self.pair_planes(node, record, p, boxes)
            if any(planes for planes in per_piece):
                raise CertificateError(
                    f"node {node['id']}: pair closure but a plane is possible"
                )
            self.tick("closed_pair_ok")
        else:
            raise CertificateError(f"node {node['id']}: unknown pair closure {kind}")

    def check_open(self, node: Node, previous_next: list[Box]) -> None:
        final = node["final_q"]
        for s in range(self.k):
            if not box_contains(final[s], previous_next[s]):
                raise CertificateError(f"node {node['id']}: final box of square {s} too small")
        split = node["split"]
        if "pair" in split:
            p, windows = split["pair"]
            record = node["rounds"][-1]
            boxes = [box_of(box) for box in record["boxes"]]
            per_piece, pieces, _, _ = self.pair_planes(node, record, p, boxes)
            wins = [(parse(lo), parse(hi)) for lo, hi in windows]
            for planes, (lo, hi, _) in zip(per_piece, pieces, strict=True):
                if not planes:
                    continue
                if not any(a <= lo and hi <= b for a, b in wins):
                    raise CertificateError(
                        f"node {node['id']}: pair split leaves piece [{lo},{hi}] uncovered"
                    )
            self.tick("pair_split_ok")
        else:
            self.tick("angle_split_ok")
        self.tick("open_ok")

    def check_node(self, node: Node, parent: Node | None) -> None:
        """Every round of one node, given its parent's record (None at the root)."""
        if parent is None:
            inherited = list(self.root_boxes)
            if node["angles_q"] != self.root_angles or node["windows"]:
                raise CertificateError("T1: the root's angles or windows are wrong")
        else:
            inherited = parent["final_q"]
        rounds = node["rounds"]
        if not rounds:
            if node["closed"] != "cell":
                raise CertificateError(
                    f"node {node['id']}: no rounds but closed {node['closed']}"
                )
            for s in range(self.k):
                if contract(self.cells[s], inherited[s], node["angles_q"][s], self.cap) is None:
                    self.tick("closed_cell_ok")
                    return
            raise CertificateError(
                f"node {node['id']}: closed 'cell' but every contracted box is nonempty"
            )
        previous_next: list[Box] = []
        for r, record in enumerate(rounds):
            boxes = [box_of(box) for box in record["boxes"]]
            # B1 / B2: the recorded box contains the one derived here.
            for s in range(self.k):
                if r == 0:
                    mine = contract(self.cells[s], inherited[s], node["angles_q"][s], self.cap)
                    if mine is None:
                        raise CertificateError(
                            f"node {node['id']}: round 0 box of square {s} should be empty"
                        )
                else:
                    mine = previous_next[s]
                if not box_contains(boxes[s], mine):
                    raise CertificateError(
                        f"node {node['id']}: round {r} box of square {s} too small"
                    )
            cuts = [parsed_cut(c) for c in record.get("cuts", [])]
            context = (node, record, boxes, {})
            if "closed_pair" in record:
                self.check_closed_pair(node, record, boxes)
                if r != len(rounds) - 1 or node["closed"] != record["closed_pair"][1]:
                    raise CertificateError(f"node {node['id']}: pair closure not final")
                return
            if "farkas" in record:
                value = self.combination_min(record["farkas"], None, cuts, context)
                if not value > 0:
                    raise CertificateError(
                        f"node {node['id']}: Farkas combination min {float(value)} <= 0"
                    )
                self.tick("closed_lp_ok")
                if r != len(rounds) - 1 or node["closed"] != "lp":
                    raise CertificateError(f"node {node['id']}: lp closure not final")
                return
            outcome = self.check_bounds(node, record, boxes, cuts, context)
            if outcome is None:
                return
            previous_next = outcome
        if node["closed"] is not None:
            raise CertificateError(
                f"node {node['id']}: closed {node['closed']} without a closing record"
            )
        self.check_open(node, previous_next)

    def check_bounds(
        self,
        node: Node,
        record: dict[str, Any],
        boxes: list[Box],
        cuts: list[tuple[Any, ...]],
        context: tuple[Node, dict[str, Any], list[Box], dict[int, Any]],
    ) -> list[Box] | None:
        """C4 and C5 for one round: the next round's boxes, or None when it closes."""
        current = [list(box) for box in boxes]
        for col, sign, value_text, multipliers in record.get("bounds", []):
            value = parse(value_text)
            frozen: list[Box] = [(b[0], b[1], b[2], b[3]) for b in current]
            bound = self.combination_min(
                multipliers, (col, Q(sign)), cuts, (node, record, frozen, context[3])
            )
            if value > bound:
                raise CertificateError(
                    f"node {node['id']}: bound on column {col} sign {sign}: "
                    f"{float(value)} > {float(bound)}"
                )
            s, axis = divmod(col, 2)
            slot = 2 * axis + (0 if sign > 0 else 1)
            current[s][slot] = value if sign > 0 else -value
            self.tick("bound_ok")
        if record.get("emptied") == "bounds":
            if not any(b[0] > b[1] or b[2] > b[3] for b in current):
                raise CertificateError(
                    f"node {node['id']}: emptied by bounds but no bound crossed"
                )
            if node["closed"] != "obbt":
                raise CertificateError(f"node {node['id']}: emptied but not closed obbt")
            self.tick("closed_obbt_ok")
            return None
        tightened: list[Box] = []
        for s in range(self.k):
            clipped = clip_cell_to_box(
                self.cells[s], (current[s][0], current[s][1], current[s][2], current[s][3])
            )
            if clipped is None:
                if record.get("emptied") != "cell" or node["closed"] != "obbt":
                    raise CertificateError(
                        f"node {node['id']}: box misses its cell but not closed obbt/cell"
                    )
                self.tick("closed_obbt_ok")
                return None
            tightened.append(clipped)
        if record.get("emptied") == "cell":
            raise CertificateError(
                f"node {node['id']}: emptied cell but every box meets its cell"
            )
        if "next" not in record:
            return boxes
        following = [box_of(box) for box in record["next"]]
        for s in range(self.k):
            if not box_contains(following[s], tightened[s]):
                raise CertificateError(f"node {node['id']}: next box of square {s} too small")
        return following


def parsed_cut(cut: list[Any]) -> tuple[Any, ...]:
    """An interval cut `(p, ux, uy, v)` or a Taylor cut `(p, ux, uy, v, w, s1, s2, b)`."""
    if len(cut) == 4:
        return (cut[0], parse(cut[1]), parse(cut[2]), parse(cut[3]))
    if len(cut) == 8:
        return (
            cut[0],
            parse(cut[1]),
            parse(cut[2]),
            parse(cut[3]),
            parse(cut[4]),
            cut[5],
            cut[6],
            parse(cut[7]),
        )
    raise CertificateError(f"a cut with {len(cut)} fields")


def span_min(coefficient: Q, span: Span) -> Q:
    return coefficient * (span[0] if coefficient >= 0 else span[1])


def taylor_plane_min(
    u: Point, w: Q, plane: FullPlane, line: tuple[Q, Q], boxes: tuple[Span, Span, Span]
) -> Q:
    """The least `u . d - w t` over the boxes meet `nbar . d - c b t >= c a - o` (X4).

    One general constraint: the Lagrangian bound `(u - lam nbar) . d + (lam c b - w) t +
    lam (c a - o)` is concave and piecewise linear in `lam >= 0`, so its largest value,
    the LP's value when the region is nonempty and a lower bound in any case, is at 0 or
    at a multiplier cancelling one coefficient.
    """
    nx, ny, _, c, o = plane
    a, b = line
    dx, dy, dt = boxes
    candidates = [Q(0)]
    for numerator, denominator in ((u[0], nx), (u[1], ny), (w, c * b)):
        if denominator != 0:
            lam = numerator / denominator
            if lam >= 0:
                candidates.append(lam)
    return max(
        span_min(u[0] - lam * nx, dx)
        + span_min(u[1] - lam * ny, dy)
        + span_min(lam * c * b - w, dt)
        + lam * (c * a - o)
        for lam in candidates
    )


def box_of(values: list[str]) -> Box:
    return (parse(values[0]), parse(values[1]), parse(values[2]), parse(values[3]))


# ---------------------------------------------------------------------------
# The tree and the node passes
# ---------------------------------------------------------------------------


@dataclass
class Tree:
    index: dict[int, dict[str, Any]]
    chunk_of: dict[int, int]
    children: dict[int | None, list[int]]
    depth: dict[int, int]
    closed_leaves: int
    reasons: dict[str, int]


def load_tree(verifier: Verifier) -> Tree:
    """Pass 1: a compact index of every node, and T1 to T3 over it."""
    index: dict[int, dict[str, Any]] = {}
    chunk_of: dict[int, int] = {}
    children: dict[int | None, list[int]] = {}
    for c, chunk in enumerate(verifier.manifest["chunks"]):
        for node in read_named(verifier.directory, chunk)["nodes"]:
            ident = node["id"]
            if ident in index:
                verifier.fail(f"duplicate node id {ident}")
            index[ident] = {
                "id": ident,
                "parent": node["parent"],
                "angles": node["angles"],
                "windows": node["windows"],
                "closed": node["closed"],
                "split": node.get("split"),
                "final": node.get("final"),
            }
            chunk_of[ident] = c
            children.setdefault(node["parent"], []).append(ident)
    tree = Tree(index, chunk_of, children, {}, 0, {})
    check_tree(verifier, tree)
    return tree


def expected_children(node: dict[str, Any]) -> list[tuple[str, str]]:
    split = node["split"]
    expected: list[tuple[str, str]] = []
    if "angle" in split:
        s, a_text = split["angle"]
        for part in ((node["angles"][s][0], a_text), (a_text, node["angles"][s][1])):
            angles = list(node["angles"])
            angles[s] = list(part)
            expected.append((json.dumps(angles), json.dumps(node["windows"])))
    else:
        p, windows = split["pair"]
        for lo, hi in windows:
            wins = [w for w in node["windows"] if w[0] != p] + [[p, lo, hi]]
            expected.append((json.dumps(node["angles"]), json.dumps(sorted(wins))))
    return sorted(expected)


def check_tree(verifier: Verifier, tree: Tree) -> None:
    """T1 to T3: one root, children that partition the parent, every node reached."""
    roots = tree.children.get(None, [])
    if len(roots) != 1:
        verifier.fail(f"T1: {len(roots)} roots")
    stack = [(roots[0], 0)] if roots else []
    reached = 0
    while stack:
        ident, d = stack.pop()
        tree.depth[ident] = d
        reached += 1
        node = tree.index[ident]
        kids = tree.children.get(ident, [])
        if node["closed"] is not None:
            tree.closed_leaves += 1
            tree.reasons[node["closed"]] = tree.reasons.get(node["closed"], 0) + 1
            if kids:
                verifier.fail(f"T3: closed node {ident} has children")
            continue
        split = node["split"]
        if split is None or node["final"] is None:
            verifier.fail(f"T3: open node {ident} has no split or final")
            continue
        if "angle" in split:
            s, a_text = split["angle"]
            a = parse(a_text)
            lo, hi = parse(node["angles"][s][0]), parse(node["angles"][s][1])
            if not lo <= a <= hi:
                verifier.fail(f"T2: node {ident} angle split point outside the interval")
            got = sorted(
                (json.dumps(tree.index[c]["angles"]), json.dumps(tree.index[c]["windows"]))
                for c in kids
            )
            if got != expected_children(node):
                verifier.fail(f"T2: node {ident} angle split children mismatch")
        else:
            got = sorted(
                (
                    json.dumps(tree.index[c]["angles"]),
                    json.dumps(sorted(tree.index[c]["windows"])),
                )
                for c in kids
            )
            if got != expected_children(node):
                verifier.fail(f"T2: node {ident} pair split children mismatch")
        stack.extend((c, d + 1) for c in kids)
    if reached != len(tree.index):
        verifier.fail(f"T3: {len(tree.index) - reached} nodes unreachable from the root")


def choose_nodes(tree: Tree, sample: int | None, deepest: int, seed: int) -> set[int]:
    """Every node in full mode; otherwise the deepest, a random sample and their ancestors."""
    if sample is None:
        return set(tree.index)
    closed = [i for i, n in tree.index.items() if n["closed"] is not None]
    rng = random.Random(seed)
    chosen: set[int] = set(sorted(closed, key=lambda i: -tree.depth.get(i, 0))[:deepest])
    lp = [i for i in closed if tree.index[i]["closed"] == "lp"]
    chosen.update(rng.sample(lp, min(sample, len(lp))))
    other = [i for i in closed if tree.index[i]["closed"] != "lp"]
    chosen.update(rng.sample(other, min(sample, len(other))))
    for i in list(chosen):
        p = tree.index[i]["parent"]
        while p is not None and p not in chosen:
            chosen.add(p)
            p = tree.index[p]["parent"]
    return chosen


def prepared(node: Node) -> Node:
    node["angles_q"] = [(parse(lo), parse(hi)) for lo, hi in node["angles"]]
    if "taylor" in node:
        centres = [parse(c) for c in node["taylor"]["centres"]]
        node["centres_q"] = centres
        node["offsets_q"] = [
            (lo - c, hi - c) for (lo, hi), c in zip(node["angles_q"], centres, strict=True)
        ]
    node["window_map"] = {w[0]: (parse(w[1]), parse(w[2])) for w in node["windows"]}
    if node.get("final") is not None:
        node["final_q"] = [box_of(box) for box in node["final"]]
    return node


def check_nodes(
    verifier: Verifier, tree: Tree, chosen: set[int], *, progress: bool, clock: float
) -> tuple[int, int]:
    """Pass 2: chosen nodes by chunk and ID; keep parents until their last use."""
    needed: dict[int, list[int]] = {}
    for i in chosen:
        needed.setdefault(tree.chunk_of[i], []).append(i)
    full: dict[int, Node] = {}
    pending = set(chosen)
    remaining = {i: sum(child in chosen for child in tree.children.get(i, [])) for i in chosen}

    def retire(ident: int) -> None:
        # A chunk can put every child before its parent's own scheduled check.
        if ident not in pending and remaining.get(ident) == 0:
            full.pop(ident, None)
            remaining.pop(ident, None)

    checked = failed = 0
    for c in sorted(needed):
        wanted = set(needed[c])
        for node in read_named(verifier.directory, verifier.manifest["chunks"][c])["nodes"]:
            if node["id"] in wanted:
                full[node["id"]] = prepared(node)
        for ident in sorted(needed[c]):
            node = full[ident]
            parent = full.get(node["parent"]) if node["parent"] is not None else None
            parent_id = node["parent"]
            try:
                if parent_id is not None and parent is None:
                    verifier.fail(f"node {ident}: parent {parent_id} not loaded")
                    continue
                try:
                    verifier.check_node(node, parent)
                except CertificateError as exc:
                    failed += 1
                    verifier.fail(str(exc))
                checked += 1
                if progress and checked % 2000 == 0:
                    print(
                        json.dumps(
                            {
                                "checked": checked,
                                "seconds": round(time.perf_counter() - clock, 1),
                            }
                        ),
                        flush=True,
                    )
            finally:
                pending.remove(ident)
                retire(ident)
                if parent_id in remaining:
                    remaining[parent_id] -= 1
                    retire(parent_id)
                # Eviction must also release the loop's references before the next chunk.
                del node, parent
        # T3 forbids children of closed nodes. Keep the existing missing-parent
        # refusals for malformed children in later chunks, rather than admitting
        # their inheritance merely because a selected-child count is nonzero.
        for ident in wanted:
            if ident in full and full[ident]["closed"] is not None:
                del full[ident]
                remaining.pop(ident, None)
    return checked, failed


@dataclass(frozen=True)
class Mode:
    """Full by default; any sample setting makes it a planning check."""

    sample: int | None = None
    deepest: int = 20
    trig_sample: int | None = None
    seed: int = 1

    @property
    def full(self) -> bool:
        return self.sample is None and self.trig_sample is None


def run_checks(
    directory: Path,
    name: str,
    cells: Cells,
    mode: Mode,
    receipt: dict[str, Any],
    *,
    progress: bool,
) -> tuple[Verifier, Tree, int, int]:
    """Every check in order; a whole-certificate failure raises, a node failure is kept."""
    clock = time.perf_counter()
    if not constants_hold():
        raise CertificateError("the pi enclosure does not hold")
    verifier = Verifier(directory, name)
    receipt["pattern"] = list(verifier.manifest["header"]["pattern"])
    receipt["certificate"]["chunks"] = len(verifier.manifest["chunks"])
    verifier.check_header(cells)
    trig = read_named(directory, verifier.manifest["trig"])["trig"]
    verifier.check_trig(trig, mode.trig_sample, mode.seed)
    tree = load_tree(verifier)
    if not verifier.manifest["summary"].get("complete"):
        verifier.fail("summary.complete is false")
    chosen = choose_nodes(tree, mode.sample, mode.deepest, mode.seed)
    checked, failed = check_nodes(verifier, tree, chosen, progress=progress, clock=clock)
    return verifier, tree, checked, failed


def verify_certificate(
    directory: Path,
    cells: Cells,
    *,
    manifest: str | None = None,
    mode: Mode | None = None,
    progress: bool = False,
) -> dict[str, Any]:
    """The verification receipt: PASS only for a complete tree that checks without fault."""
    clock = time.perf_counter()
    mode = mode or Mode()
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "verifier": KIND,
        "provenance": PROVENANCE,
        "directory": repository_path(directory),
        "cells_source": cells.source,
        "mode": "full" if mode.full else "sample",
        "sample": None
        if mode.full
        else {
            "nodes": mode.sample,
            "deepest": mode.deepest,
            "trig": mode.trig_sample,
            "seed": mode.seed,
        },
        "certificate": {"manifest_sha256": manifest},
    }
    try:
        name = manifest or manifest_from_readme(directory)
        receipt["certificate"]["manifest_sha256"] = name
        verifier, tree, checked, failed = run_checks(
            directory, name, cells, mode, receipt, progress=progress
        )
    except CertificateError as failure:
        receipt.update(status="FAIL", failures=[str(failure)], failure_count=1)
    except (KeyError, TypeError, ValueError, IndexError, ZeroDivisionError, OSError) as failure:
        receipt.update(
            status="FAIL", failures=[f"malformed certificate: {failure!r}"], failure_count=1
        )
    else:
        if mode.sample is None and checked != len(tree.index):
            verifier.fail(f"checked {checked} of {len(tree.index)} nodes")
        receipt.update(
            nodes=len(tree.index),
            closed_leaves=tree.closed_leaves,
            reasons=dict(sorted(tree.reasons.items())),
            max_depth=max(tree.depth.values(), default=None),
            checked_nodes=checked,
            node_failures=failed,
            counts=dict(sorted(verifier.counts.items())),
            status="FAIL" if verifier.failures else "PASS",
            failures=verifier.failures[:MAX_FAILURES],
            failure_count=len(verifier.failures),
        )
    receipt["seconds"] = round(time.perf_counter() - clock, 3)
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("directory", type=Path, help="the certificate directory")
    _ = parser.add_argument("--manifest", default=None, help="else the README's last line")
    _ = parser.add_argument("--cells", type=Path, help="a JSON cells file instead of the cover")
    _ = parser.add_argument("--cells-sha256", help="the cells file's SHA-256, required with it")
    _ = parser.add_argument("--sample", type=int, default=None, help="closed nodes per kind")
    _ = parser.add_argument("--deepest", type=int, default=20)
    _ = parser.add_argument("--trig-sample", type=int, default=None)
    _ = parser.add_argument("--seed", type=int, default=1)
    _ = parser.add_argument("--output", type=Path, required=True, help="the receipt")
    _ = parser.add_argument("--progress", action="store_true")
    arguments = parser.parse_args(argv)
    if arguments.cells is not None:
        if not arguments.cells_sha256:
            parser.error("--cells needs --cells-sha256")
        cells = file_cells(arguments.cells, arguments.cells_sha256)
    else:
        cells = cover_cells()
    receipt = verify_certificate(
        arguments.directory,
        cells,
        manifest=arguments.manifest,
        mode=Mode(arguments.sample, arguments.deepest, arguments.trig_sample, arguments.seed),
        progress=arguments.progress,
    )
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    _ = arguments.output.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    print(
        json.dumps({k: receipt.get(k) for k in ("status", "mode", "checked_nodes", "seconds")})
    )
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
