"""An independent labeller for the 78,673 boxes of Lemma 4.10 of Ryu's k2-minus-c.

Sungjoon Ryu's preprint "Packing k^2 - c unit squares: s(k^2 - c) = k for all large k"
(version 1.1, retained whole in
``packing/resources/web/squarepacker-k2-minus-c-2026-10-05/``; version 1.2's Lemma 4.10
states the same model over the same 13 lists) rests its constant 0.033 on Lemma 4.10:
at an uncovered point ``p`` at most 9 Roth-Vaughan rectangles of nearly touching pairs
overlap. Its proof reduces this to a bound ``U(I) = E_II + W_I + sum_i D_i*(I) <= 9`` on a
parameter domain, and covers the domain by 78,673 boxes, each labelled ``inf`` (no
admissible configuration), ``nowall`` (with a side, no side edge is possible) or
``closed`` (the bound is at most 9). The source decides the labels with one program,
which shares the search's cell grid, float prefilter, split rule and float point count.

This module decides every label again, written from the proof of Lemma 4.10 and the disc
model of the TeX alone. None of the source's programs was read: not ``verify_leaves.py``,
``verify_leaves2.py``, ``bnb.py``, ``bnb_wall.py`` nor any other. The box lists are read
as data from the retained ``data/kw9_data.zip``.

The model, with ``d = 10^-4``, ``Lambda = d + sqrt 2``, ``rho1 = sqrt((d + sqrt2/2)^2 +
1/4)``, ``gamma0 = arccos(1 - 1/(2 Lambda^2))`` and ``p = 0``. A box gives each of the
``n <= 5`` inner centres ``c_i = r_i (cos t_i, sin t_i)`` an interval of ``r_i`` and of
``t_i``; with a side, the side is the line ``y = -h`` and ``h`` has an interval too. An
upper end of ``t_i`` at the binary64 value of ``2 pi`` is extended to the next binary64
number, which lies above ``2 pi``, as the proof extends it to the exact ``2 pi``.

- A configuration is admissible only if ``|c_i - c_j| >= 1`` for ``i != j`` and, with a
  side, ``c_iy + h >= 1/2``.
- ``E_II`` counts the pairs that may be closer than ``Lambda``.
- ``W_I`` counts the centres that may have a side edge: ``|c_ix| <= 1/2``, ``c_iy >= 0``
  and ``c_iy + h < d + sqrt2/2``.
- ``D_i*`` is the largest number of directions, pairwise at least ``gamma0`` apart, in
  which an outer centre ``x = c_i + t u`` may exist: ``1 <= t < Lambda``,
  ``|x| > rho1``, ``p`` in the rectangle ``R(c_i, x)`` (``c_i . u <= 0`` and
  ``|c_i x u| <= 1/2``), ``|x - c_j| >= 1`` for every other inner centre, and, with a
  side, ``x_y >= -h + 1/2``.

How it decides, and why each step is sound.

- **Arithmetic.** Binary64 with every basic operation rounded outward by one ulp
  (``numpy.nextafter``), which encloses the exact result because IEEE 754 rounds each
  operation correctly. Every transcendental number (``cos`` and ``sin`` of the box
  angles and of the direction grid, ``sqrt 2``, ``gamma0``, ``2 pi``) comes from
  ``mpmath``'s interval context at 200 bits and is rounded outward to binary64.
- **Directions.** For each inner centre, the circle is cut into dyadic cells of
  ``2^-L`` turn, from ``L = 5`` to at most ``L = 13``. A cell is discarded only if, for
  every configuration of the box, every direction of the cell and every ``t`` in
  ``[1, Lambda]``, some condition fails. The test is exact in ``t``: each condition is a
  quadratic or linear inequality in ``t`` whose coefficients are bounded over the box and
  the cell, so the set of ``t`` where it may hold is the complement of an open interval
  between two roots, computed with outward rounding, and the cell is discarded when those
  open intervals cover ``[1, Lambda]``.
- **The count.** ``D_i*`` is bounded by the largest number of points, pairwise at least
  ``g`` apart, in the union of the kept closed cells, where ``g`` is a rational lower
  bound of ``gamma0 / (2 pi)`` with denominator ``2^64``. This is computed exactly, in
  integers, by the greedy count from the start of each maximal run of cells with the
  closing condition, which the proof of Lemma 4.10 shows is the maximum; a full circle
  gives ``floor(1/g) = 8``.
- **Bisection.** A box whose bound does not reach its label is bisected, at the binary64
  midpoint of its widest side (an angle weighted by the largest radius), until every
  piece is decided or the budget of pieces is spent. The rule is this module's own.

A box is *certified as labelled* when every piece is decided by its own label (``inf``
pieces count for ``closed`` and ``nowall`` boxes too, since an inadmissible piece needs
no bound). Otherwise it is tried with every label, and is *certified otherwise* if that
succeeds and *not certified* if it does not.

Run from ``packing/`` with the project interpreter::

    .venv/bin/python3 -m cases.asymptotic.ryu_k2_minus_c_labels price --sample 500
    .venv/bin/python3 -m cases.asymptotic.ryu_k2_minus_c_labels run --out DIR \\
        --worker 0 --workers 2
    .venv/bin/python3 -m cases.asymptotic.ryu_k2_minus_c_labels summarize --out DIR
    .venv/bin/python3 -m cases.asymptotic.ryu_k2_minus_c_labels controls --out FILE
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
import time
import zipfile
from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

import mpmath
import numpy as np
import numpy.typing as npt

from devtools.retained_data import write_retained

#: mpmath's interval context; its functions are attached at run time.
iv: Any = mpmath.iv

FloatArray = npt.NDArray[np.float64]
IntArray = npt.NDArray[np.int64]

PACKING = Path(__file__).resolve().parents[2]
PACKET = PACKING / "resources/web/squarepacker-k2-minus-c-2026-10-05"
DATA_ZIP = PACKET / "k2-minus-c/data/kw9_data.zip"

#: The 13 box lists of Lemma 4.10, in the order the certificate names them.
LISTS = (
    "bnb_n1_T9_0of1",
    "bnb_n2_T9_0of1",
    "bnb_n3_T9_0of1",
    "bnb_n4_T9_0of2",
    "bnb_n4_T9_1of2",
    "bnb_n5_T9_0of2",
    "bnb_n5_T9_1of2",
    "bnbw_n1_T9_0of1",
    "bnbw_n2_T9_0of1",
    "bnbw_n3_T9_0of1",
    "bnbw_n4_T9_0of2",
    "bnbw_n4_T9_1of2",
    "bnbw_n5_T9_0of1",
)
LABELS = ("inf", "nowall", "closed")

#: The bound Lemma 4.10 states, and the precision of the transcendental enclosures.
THRESHOLD = 9
PREC_BITS = 200
#: The direction grid: cells of 2^-L turn, refined from FIRST_LEVEL to LAST_LEVEL; the
#: trigonometric table is held at TABLE_LEVEL.
FIRST_LEVEL = 5
LAST_LEVEL = 13
TABLE_LEVEL = 16
#: The count's unit: points on the circle are integers in units of 2^-64 turn.
TURN = 1 << 64
#: Pieces a box may be cut into before it is reported as not certified.
MAX_PIECES = 4096
#: The binary64 value of 2 pi, which every upper angle end at 2 pi in the lists carries.
TWO_PI_FLOAT = 6.283185307179586
#: The widest angle interval whose cos and sin are bounded by `arc_range`; wider ones
#: (28 intervals of inf boxes span the whole circle) get the trivial range [-1, 1]. A
#: cell adds at most 2 pi / 2^5 < 0.2, so every arc `arc_range` sees is below 3 < pi.
ARC_LIMIT = 2.8


def dn(x: Any) -> Any:
    """One ulp down: a lower bound of the exact result of the operation giving ``x``."""
    return np.nextafter(x, -np.inf)


def up(x: Any) -> Any:
    """One ulp up: an upper bound of the exact result of the operation giving ``x``."""
    return np.nextafter(x, np.inf)


def _fraction(value: Any) -> Fraction:
    """An mpmath real (an interval end point) as an exact fraction."""
    sign, man, exp, _ = value._mpf_ if hasattr(value, "_mpf_") else value
    magnitude = Fraction(int(man)) * (Fraction(2) ** int(exp))
    return -magnitude if sign else magnitude


def _ends(value: Any) -> tuple[Fraction, Fraction]:
    """The exact end points of an mpmath interval."""
    low, high = value._mpi_
    return _fraction(low), _fraction(high)


def float_down(value: Fraction) -> float:
    """The largest binary64 number at most ``value``."""
    result = float(value)
    return math.nextafter(result, -math.inf) if Fraction(result) > value else result


def float_up(value: Fraction) -> float:
    """The smallest binary64 number at least ``value``."""
    result = float(value)
    return math.nextafter(result, math.inf) if Fraction(result) < value else result


def enclose(value: Any) -> tuple[float, float]:
    """Binary64 bounds of an mpmath interval, rounded outward."""
    low, high = _ends(value)
    return float_down(low), float_up(high)


@dataclass(frozen=True)
class Constants:
    """Outward binary64 bounds of the constants of Lemma 4.10, and the count's step."""

    lam_hi: float
    lam_sq_hi: float
    rho1_sq_lo: float
    wall_hi: float
    separation: int
    gamma0_deg: tuple[float, float]
    two_pi_hi_float: float

    def describe(self) -> dict[str, Any]:
        return {
            "Lambda_hi": self.lam_hi,
            "Lambda_sq_hi": self.lam_sq_hi,
            "rho1_sq_lo": self.rho1_sq_lo,
            "d_plus_sqrt2_over_2_hi": self.wall_hi,
            "separation_turns": f"{self.separation}/2^64",
            "gamma0_degrees": list(self.gamma0_deg),
        }


def _certified_separation(cos_gamma0: Any) -> int:
    """An integer g with g / 2^64 turn < gamma0, certified on intervals.

    A candidate comes from mpmath's real arccos and is lowered by 2^-60 turn; it is
    accepted only if cos(2 pi g / 2^64) > cos gamma0 holds on intervals, which, as cos
    decreases on [0, pi], gives 2 pi g / 2^64 < gamma0. The interval context has no
    arccos, so this check is what makes the separation rigorous."""
    mpmath.mp.prec = PREC_BITS
    _, x_hi = _ends(cos_gamma0)
    estimate = mpmath.acos(mpmath.mpf(x_hi.numerator) / x_hi.denominator) / (2 * mpmath.pi)
    candidate = int(mpmath.floor(estimate * TURN)) - (1 << 4)
    angle = 2 * iv.pi * iv.mpf(candidate) / TURN
    cos_lo, _ = _ends(iv.cos(angle))
    low_x, high_x = _ends(cos_gamma0)
    if not (cos_lo > high_x and low_x > 0 and candidate > 0):
        msg = "the separation could not be certified below gamma0"
        raise ArithmeticError(msg)
    return candidate


@cache
def constants() -> Constants:
    """The constants, from mpmath intervals at 200 bits."""
    iv.prec = PREC_BITS
    d = iv.mpf(1) / 10000
    sqrt2 = iv.sqrt(2)
    lam = d + sqrt2
    wall = d + sqrt2 / 2
    rho1_sq = wall**2 + iv.mpf(1) / 4
    cos_gamma0 = 1 - 1 / (2 * lam**2)
    separation = _certified_separation(cos_gamma0)
    _, two_pi_hi = _ends(2 * iv.pi)
    next_float = math.nextafter(TWO_PI_FLOAT, math.inf)
    if not (Fraction(TWO_PI_FLOAT) < two_pi_hi and Fraction(next_float) > two_pi_hi):
        msg = "the binary64 neighbours of 2 pi are not where the extension assumes"
        raise ArithmeticError(msg)
    deg = iv.mpf(separation) / TURN * 360
    return Constants(
        lam_hi=enclose(lam)[1],
        lam_sq_hi=enclose(lam**2)[1],
        rho1_sq_lo=enclose(rho1_sq)[0],
        wall_hi=enclose(wall)[1],
        separation=separation,
        gamma0_deg=enclose(deg),
        two_pi_hi_float=next_float,
    )


@cache
def angle_trig(theta: float) -> tuple[float, float, float, float]:
    """Outward bounds of (cos theta, sin theta) for a binary64 angle."""
    iv.prec = PREC_BITS
    x = iv.mpf(theta)
    c_lo, c_hi = enclose(iv.cos(x))
    s_lo, s_hi = enclose(iv.sin(x))
    return c_lo, c_hi, s_lo, s_hi


@cache
def direction_table() -> tuple[FloatArray, FloatArray, FloatArray, FloatArray]:
    """Outward bounds of cos and sin at 2 pi k / 2^16, k = 0..2^16 (the last is k = 0).

    The first octant is computed in mpmath's interval context; the rest follows by the
    exact symmetries cos(pi/2 - x) = sin x, cos(pi/2 + x) = -sin x and cos(pi + x) =
    -cos x (and their sine counterparts), which swap or negate the bounds exactly."""
    iv.prec = PREC_BITS
    total = 1 << TABLE_LEVEL
    eighth, quarter, half = total // 8, total // 4, total // 2
    cos_lo = np.empty(total + 1)
    cos_hi = np.empty(total + 1)
    sin_lo = np.empty(total + 1)
    sin_hi = np.empty(total + 1)
    step = 2 * iv.pi / total
    for k in range(eighth + 1):
        angle = step * k
        cos_lo[k], cos_hi[k] = enclose(iv.cos(angle))
        sin_lo[k], sin_hi[k] = enclose(iv.sin(angle))
    for k in range(eighth + 1, quarter + 1):
        j = quarter - k
        cos_lo[k], cos_hi[k] = sin_lo[j], sin_hi[j]
        sin_lo[k], sin_hi[k] = cos_lo[j], cos_hi[j]
    for k in range(quarter + 1, half + 1):
        j = k - quarter
        cos_lo[k], cos_hi[k] = -sin_hi[j], -sin_lo[j]
        sin_lo[k], sin_hi[k] = cos_lo[j], cos_hi[j]
    for k in range(half + 1, total):
        j = k - half
        cos_lo[k], cos_hi[k] = -cos_hi[j], -cos_lo[j]
        sin_lo[k], sin_hi[k] = -sin_hi[j], -sin_lo[j]
    cos_lo[total], cos_hi[total] = cos_lo[0], cos_hi[0]
    sin_lo[total], sin_hi[total] = sin_lo[0], sin_hi[0]
    return cos_lo, cos_hi, sin_lo, sin_hi


def imul(a_lo: Any, a_hi: Any, b_lo: Any, b_hi: Any) -> tuple[Any, Any]:
    """The product of two intervals, rounded outward."""
    p1, p2, p3, p4 = a_lo * b_lo, a_lo * b_hi, a_hi * b_lo, a_hi * b_hi
    low = np.minimum(np.minimum(p1, p2), np.minimum(p3, p4))
    high = np.maximum(np.maximum(p1, p2), np.maximum(p3, p4))
    return dn(low), up(high)


def arc_range(
    ca: tuple[Any, Any], sa: tuple[Any, Any], cb: tuple[Any, Any], sb: tuple[Any, Any]
) -> tuple[Any, Any, Any, Any]:
    """Bounds of cos and sin over the counter-clockwise arc from angle a to angle b.

    The arc must be shorter than pi. ``ca``, ``sa``, ``cb``, ``sb`` enclose cos and sin
    at its two ends. On such an arc a point of the circle lies between the ends exactly
    when the cross products from a to it and from it to b are both non-negative, so the
    arc can reach angle 0 only if sin a <= 0 <= sin b, angle pi only if sin a >= 0 >= sin
    b, angle pi/2 only if cos a >= 0 >= cos b and angle -pi/2 only if cos a <= 0 <= cos
    b; elsewhere cos and sin are monotone between the ends."""
    cos_lo = np.minimum(ca[0], cb[0])
    cos_hi = np.maximum(ca[1], cb[1])
    sin_lo = np.minimum(sa[0], sb[0])
    sin_hi = np.maximum(sa[1], sb[1])
    cos_hi = np.where((sa[0] <= 0) & (sb[1] >= 0), 1.0, cos_hi)
    cos_lo = np.where((sa[1] >= 0) & (sb[0] <= 0), -1.0, cos_lo)
    sin_hi = np.where((ca[1] >= 0) & (cb[0] <= 0), 1.0, sin_hi)
    sin_lo = np.where((ca[0] <= 0) & (cb[1] >= 0), -1.0, sin_lo)
    return cos_lo, cos_hi, sin_lo, sin_hi


def difference_ends(
    first: tuple[Any, Any, Any, Any], second: tuple[Any, Any, Any, Any]
) -> tuple[tuple[Any, Any], tuple[Any, Any]]:
    """Enclosures of cos and sin of (alpha - beta), given (cos, sin) bounds of each."""
    c1_lo, c1_hi, s1_lo, s1_hi = first
    c2_lo, c2_hi, s2_lo, s2_hi = second
    cc = imul(c1_lo, c1_hi, c2_lo, c2_hi)
    ss = imul(s1_lo, s1_hi, s2_lo, s2_hi)
    sc = imul(s1_lo, s1_hi, c2_lo, c2_hi)
    cs = imul(c1_lo, c1_hi, s2_lo, s2_hi)
    cos_d = (dn(cc[0] + ss[0]), up(cc[1] + ss[1]))
    sin_d = (dn(sc[0] - cs[1]), up(sc[1] - cs[0]))
    return cos_d, sin_d


@dataclass
class Box:
    """A box of the parameter domain: per centre r and angle intervals, and h with a side."""

    r_lo: FloatArray
    r_hi: FloatArray
    t_lo: FloatArray
    t_hi: FloatArray
    h: tuple[float, float] | None

    @property
    def n(self) -> int:
        return len(self.r_lo)

    @property
    def wall(self) -> bool:
        return self.h is not None

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> Box:
        rows = record["box"]
        r_lo = np.array([float(row[0]) for row in rows])
        r_hi = np.array([float(row[1]) for row in rows])
        t_lo = np.array([float(row[2]) for row in rows])
        t_hi = np.array([float(row[3]) for row in rows])
        extended = constants().two_pi_hi_float
        t_hi = np.where(t_hi == TWO_PI_FLOAT, extended, t_hi)
        h = record.get("h")
        bounds = None if h is None else (float(h[0]), float(h[1]))
        box = cls(r_lo, r_hi, t_lo, t_hi, bounds)
        box.validate()
        return box

    def validate(self) -> None:
        if not 1 <= self.n <= 5:
            msg = f"a box has 1 to 5 centres, not {self.n}"
            raise ValueError(msg)
        if np.any(self.r_lo > self.r_hi) or np.any(self.t_lo > self.t_hi):
            msg = "an interval of the box is reversed"
            raise ValueError(msg)
        if np.any(self.r_lo <= 0) or np.any(self.t_hi - self.t_lo > 6.3):
            msg = "a radius is not positive or an angle interval is wider than the circle"
            raise ValueError(msg)
        if self.h is not None and not 0 <= self.h[0] <= self.h[1]:
            msg = "the side's interval is reversed or negative"
            raise ValueError(msg)

    def widest(self) -> tuple[str, int, float]:
        """The side to bisect: the widest, with an angle weighted by its largest radius."""
        best = ("r", 0, -1.0)
        for i in range(self.n):
            width_r = float(self.r_hi[i] - self.r_lo[i])
            width_t = float((self.t_hi[i] - self.t_lo[i]) * self.r_hi[i])
            if width_r > best[2]:
                best = ("r", i, width_r)
            if width_t > best[2]:
                best = ("t", i, width_t)
        if self.h is not None and self.h[1] - self.h[0] > best[2]:
            best = ("h", 0, self.h[1] - self.h[0])
        return best

    def split(self) -> tuple[Box, Box] | None:
        """Two halves that cover this box, or None when it cannot be cut further."""
        kind, i, width = self.widest()
        if width <= 1e-13:
            return None
        if kind == "h":
            assert self.h is not None
            low, high = self.h
            middle = (low + high) / 2
            if not low < middle < high:
                return None
            return (
                Box(self.r_lo, self.r_hi, self.t_lo, self.t_hi, (low, middle)),
                Box(self.r_lo, self.r_hi, self.t_lo, self.t_hi, (middle, high)),
            )
        lo_arr, hi_arr = (self.r_lo, self.r_hi) if kind == "r" else (self.t_lo, self.t_hi)
        low, high = float(lo_arr[i]), float(hi_arr[i])
        middle = (low + high) / 2
        if not low < middle < high:
            return None
        hi_left = hi_arr.copy()
        hi_left[i] = middle
        lo_right = lo_arr.copy()
        lo_right[i] = middle
        if kind == "r":
            return (
                Box(self.r_lo, hi_left, self.t_lo, self.t_hi, self.h),
                Box(lo_right, self.r_hi, self.t_lo, self.t_hi, self.h),
            )
        return (
            Box(self.r_lo, self.r_hi, self.t_lo, hi_left, self.h),
            Box(self.r_lo, self.r_hi, lo_right, self.t_hi, self.h),
        )


@dataclass
class Quantities:
    """Bounds over one box, shared by the three labels."""

    box: Box
    trig_lo: list[tuple[float, float, float, float]]
    trig_hi: list[tuple[float, float, float, float]]
    cx: tuple[FloatArray, FloatArray]
    cy: tuple[FloatArray, FloatArray]
    dist_sq_lo: FloatArray
    dist_sq_hi: FloatArray

    @classmethod
    def of(cls, box: Box) -> Quantities:
        n = box.n
        trig_lo = [angle_trig(float(t)) for t in box.t_lo]
        trig_hi = [angle_trig(float(t)) for t in box.t_hi]
        cx_lo, cx_hi, cy_lo, cy_hi = (np.empty(n) for _ in range(4))
        for i in range(n):
            lo, hi = trig_lo[i], trig_hi[i]
            if box.t_lo[i] == box.t_hi[i]:
                # A point interval: the arc test would also admit the antipode.
                c_lo, c_hi, s_lo, s_hi = lo
            elif box.t_hi[i] - box.t_lo[i] >= ARC_LIMIT:
                c_lo, c_hi, s_lo, s_hi = -1.0, 1.0, -1.0, 1.0
            else:
                c_lo, c_hi, s_lo, s_hi = arc_range(lo[0:2], lo[2:4], hi[0:2], hi[2:4])
            cx_lo[i], cx_hi[i] = imul(box.r_lo[i], box.r_hi[i], c_lo, c_hi)
            cy_lo[i], cy_hi[i] = imul(box.r_lo[i], box.r_hi[i], s_lo, s_hi)
        dist_lo = np.full((n, n), np.inf)
        dist_hi = np.full((n, n), np.inf)
        for i in range(n):
            for j in range(i + 1, n):
                low, high = cls._distance_sq(box, trig_lo, trig_hi, i, j)
                dist_lo[i, j] = dist_lo[j, i] = low
                dist_hi[i, j] = dist_hi[j, i] = high
        return cls(box, trig_lo, trig_hi, (cx_lo, cx_hi), (cy_lo, cy_hi), dist_lo, dist_hi)

    @staticmethod
    def _distance_sq(
        box: Box,
        trig_lo: list[tuple[float, float, float, float]],
        trig_hi: list[tuple[float, float, float, float]],
        i: int,
        j: int,
    ) -> tuple[float, float]:
        """Bounds of |c_i - c_j|^2 = (r_i - r_j)^2 + 2 r_i r_j (1 - cos(t_i - t_j))."""
        width = (box.t_hi[i] - box.t_lo[i]) + (box.t_hi[j] - box.t_lo[j])
        if width == 0:
            # Both angles are points: the arc test would also admit the antipode.
            (c_lo, c_hi), _ = difference_ends(trig_lo[i], trig_lo[j])
        elif width < 3.0:
            ca, sa = difference_ends(trig_lo[i], trig_hi[j])
            cb, sb = difference_ends(trig_hi[i], trig_lo[j])
            c_lo, c_hi, _, _ = arc_range(ca, sa, cb, sb)
        else:
            c_lo, c_hi = -1.0, 1.0
        one_minus_lo, one_minus_hi = dn(1.0 - c_hi), up(1.0 - c_lo)
        gap_lo = max(
            0.0, float(dn(box.r_lo[i] - box.r_hi[j])), float(dn(box.r_lo[j] - box.r_hi[i]))
        )
        gap_hi = max(float(up(box.r_hi[i] - box.r_lo[j])), float(up(box.r_hi[j] - box.r_lo[i])))
        prod_lo = dn(dn(2.0 * box.r_lo[i] * box.r_lo[j]) * max(0.0, float(one_minus_lo)))
        prod_hi = up(up(2.0 * box.r_hi[i] * box.r_hi[j]) * one_minus_hi)
        low = float(dn(dn(gap_lo * gap_lo) + prod_lo))
        high = float(up(up(gap_hi * gap_hi) + prod_hi))
        return max(0.0, low), high

    def infeasible(self) -> bool:
        """Certainly inadmissible: two centres closer than 1, or a centre within 1/2 of
        the side, throughout the box."""
        n = self.box.n
        for i in range(n):
            for j in range(i + 1, n):
                if self.dist_sq_hi[i, j] < 1.0:
                    return True
        if self.box.h is not None:
            reach = up(self.cy[1] + self.box.h[1])
            if bool(np.any(reach < 0.5)):
                return True
        return False

    def side_edge_possible(self) -> FloatArray:
        """Per centre, whether it may belong to a relevant edge with the side."""
        assert self.box.h is not None
        wall_hi = constants().wall_hi
        near_axis = (self.cx[0] <= 0.5) & (self.cx[1] >= -0.5)
        above = self.cy[1] >= 0.0
        close = dn(self.cy[0] + self.box.h[0]) <= wall_hi
        return near_axis & above & close

    def no_side_edge(self) -> bool:
        return self.box.h is not None and not bool(np.any(self.side_edge_possible()))

    def e_ii(self) -> int:
        lam_sq_hi = constants().lam_sq_hi
        n = self.box.n
        return sum(
            1 for i in range(n) for j in range(i + 1, n) if self.dist_sq_lo[i, j] < lam_sq_hi
        )

    def w_i(self) -> int:
        if self.box.h is None:
            return 0
        return int(np.count_nonzero(self.side_edge_possible()))

    def kept_cells(self, i: int, level: int, cells: IntArray) -> npt.NDArray[np.bool_]:
        """Which of the given cells of 2^-level turn may hold an outer centre for c_i."""
        cos_lo, cos_hi, sin_lo, sin_hi = direction_table()
        shift = TABLE_LEVEL - level
        a = cells << shift
        b = (cells + 1) << shift
        phi_a = (cos_lo[a], cos_hi[a], sin_lo[a], sin_hi[a])
        phi_b = (cos_lo[b], cos_hi[b], sin_lo[b], sin_hi[b])
        box = self.box
        n = box.n
        # proj[j] bounds c_j . u = r_j cos(phi - t_j); cross, c_i x u = r_i sin(phi - t_i).
        proj: list[tuple[Any, Any]] = []
        sines: list[tuple[Any, Any]] = []
        for j in range(n):
            ca, sa = difference_ends(phi_a, self.trig_hi[j])
            cb, sb = difference_ends(phi_b, self.trig_lo[j])
            c_lo, c_hi, s_lo, s_hi = arc_range(ca, sa, cb, sb)
            if box.t_hi[j] - box.t_lo[j] >= ARC_LIMIT:
                low, high = np.full(len(cells), -1.0), np.full(len(cells), 1.0)
                c_lo, c_hi, s_lo, s_hi = low, high, low, high
            proj.append(imul(box.r_lo[j], box.r_hi[j], c_lo, c_hi))
            sines.append((s_lo, s_hi))
        cross = imul(box.r_lo[i], box.r_hi[i], sines[i][0], sines[i][1])
        # p lies in R(c_i, x) only if its projection is on the segment (c_i . u <= 0;
        # the far end needs -c_i . u <= t, which holds as |c_i| < 1 <= t) and it is
        # within 1/2 of the line (|c_i x u| <= 1/2).
        in_rectangle = (proj[i][0] <= 0.0) & (cross[0] <= 0.5) & (cross[1] >= -0.5)
        const = constants()
        holes_lo: list[Any] = []
        holes_hi: list[Any] = []
        coeff_c = up(up(box.r_hi[i] * box.r_hi[i]) - const.rho1_sq_lo)
        for coeff_b, c_value in [(proj[i][1], coeff_c)] + [
            (up(proj[i][1] - proj[j][0]), up(self.dist_sq_hi[i, j] - 1.0))
            for j in range(n)
            if j != i
        ]:
            low, high = _hole(coeff_b, c_value)
            holes_lo.append(low)
            holes_hi.append(high)
        start = np.full(len(cells), 1.0)
        stop = np.full(len(cells), const.lam_hi)
        if box.h is not None:
            reach = up(self.cy[1][i] + box.h[1])
            s_top = np.maximum(phi_a[3], phi_b[3])
            rising = s_top > 0
            safe = np.where(rising, s_top, 1.0)
            low_t = dn(dn(0.5 - reach) / safe)
            start = np.where(rising, np.maximum(start, low_t), start)
            falling = s_top < 0
            safe_f = np.where(falling, -s_top, 1.0)
            high_t = up(up(reach - 0.5) / safe_f)
            stop = np.where(falling, np.minimum(stop, high_t), stop)
            flat = s_top == 0
            if reach < 0.5:
                stop = np.where(flat, -np.inf, stop)
        covered = _covered(start, stop, holes_lo, holes_hi)
        return in_rectangle & ~covered


def _hole(coeff_b: Any, coeff_c: Any) -> tuple[Any, Any]:
    """An open interval of t on which t^2 + 2 B t + C < 0 for the bounds B, C, rounded
    inward, or an empty one (low >= high) when none can be certified."""
    b = np.asarray(coeff_b, dtype=np.float64)
    c = np.asarray(coeff_c, dtype=np.float64)
    disc = dn(dn(b * b) - c)
    positive = disc > 0
    root = dn(np.sqrt(np.where(positive, disc, 0.0)))
    low = np.where(positive, up(-b - root), np.inf)
    high = np.where(positive, dn(-b + root), -np.inf)
    return low, high


def _covered(start: Any, stop: Any, holes_lo: list[Any], holes_hi: list[Any]) -> Any:
    """Whether the open holes cover the closed interval [start, stop] (empty counts)."""
    current = np.array(start, dtype=np.float64, copy=True)
    for _ in range(len(holes_lo) + 1):
        best = current.copy()
        for low, high in zip(holes_lo, holes_hi, strict=True):
            inside = (low < current) & (current < high)
            best = np.where(inside & (high > best), high, best)
        if not bool(np.any(best > current)):
            break
        current = best
    return (current > stop) | (start > stop)


def circular_count(kept: IntArray, level: int) -> int:
    """The largest number of points pairwise at least g apart in the union of the kept
    closed cells of 2^-level turn, exactly, in units of 2^-64 turn."""
    g = constants().separation
    cells = 1 << level
    if len(kept) == 0:
        return 0
    if len(kept) == cells:
        return TURN // g
    unit = TURN >> level
    runs: list[tuple[int, int]] = []
    first = previous = int(kept[0])
    for value in kept[1:]:
        k = int(value)
        if k == previous + 1:
            previous = k
            continue
        runs.append((first, previous + 1))
        first = previous = k
    runs.append((first, previous + 1))
    if len(runs) > 1 and runs[0][0] == 0 and runs[-1][1] == cells:
        head = runs.pop(0)
        tail = runs.pop()
        runs.append((tail[0], cells + head[1]))
    best = 0
    count = len(runs)
    for k in range(count):
        sequence = []
        for q in range(count):
            low, high = runs[(k + q) % count]
            offset = TURN if k + q >= count else 0
            sequence.append((low * unit + offset, high * unit + offset))
        best = max(best, _greedy(sequence, g))
    return best


def _greedy(runs: list[tuple[int, int]], g: int) -> int:
    """The greedy count from the start of the first run, closing the circle."""
    point = runs[0][0]
    limit = point + TURN - g
    count = 1
    index = 0
    while True:
        target = point + g
        while index < len(runs) and runs[index][1] < target:
            index += 1
        if index == len(runs):
            return count
        candidate = max(target, runs[index][0])
        if candidate > limit:
            return count
        point = candidate
        count += 1


def bounds_by_level(q: Quantities, stop_at: int | None = None) -> list[tuple[int, int]]:
    """Upper bounds of U(I) over the box, one per level of the direction grid, as
    (level, bound), from the coarsest; with ``stop_at`` it stops at the first bound at
    most that. Each level refines the cells the previous one kept, so the bounds never
    increase."""
    fixed = q.e_ii() + q.w_i()
    n = q.box.n
    cells: list[IntArray] = [np.arange(1 << FIRST_LEVEL, dtype=np.int64) for _ in range(n)]
    found: list[tuple[int, int]] = []
    for level in range(FIRST_LEVEL, LAST_LEVEL + 1):
        total = fixed
        for i in range(n):
            mask = q.kept_cells(i, level, cells[i])
            cells[i] = cells[i][mask]
            total += circular_count(cells[i], level)
        found.append((level, total))
        if stop_at is not None and total <= stop_at:
            break
        if level < LAST_LEVEL:
            cells = [np.stack([2 * c, 2 * c + 1], axis=1).reshape(-1) for c in cells]
    return found


def closed_bound(q: Quantities, threshold: int) -> tuple[int, int] | None:
    """An upper bound of U(I) over the box that is at most ``threshold``, with the level
    of the direction grid that reached it, or None if no level does."""
    if q.e_ii() + q.w_i() > threshold:
        return None
    level, total = bounds_by_level(q, stop_at=threshold)[-1]
    return (total, level) if total <= threshold else None


@dataclass
class Verdict:
    """The outcome of certifying one box under a set of admissible leaf labels."""

    certified: bool
    leaves: Counter[str] = field(default_factory=Counter)
    max_bound: int = -1
    max_level: int = 0
    pieces: int = 0
    reason: str = ""

    def describe(self) -> dict[str, Any]:
        return {
            "certified": self.certified,
            "leaves": dict(sorted(self.leaves.items())),
            "max_bound": self.max_bound,
            "max_level": self.max_level,
            "pieces": self.pieces,
            "reason": self.reason,
        }


def certify(
    box: Box, allowed: frozenset[str], threshold: int = THRESHOLD, budget: int = MAX_PIECES
) -> Verdict:
    """Decide the box by bisection, each piece by one of the allowed labels."""
    verdict = Verdict(certified=True)
    stack = [box]
    while stack:
        piece = stack.pop()
        verdict.pieces += 1
        q = Quantities.of(piece)
        if q.infeasible():
            verdict.leaves["inf"] += 1
            continue
        if "nowall" in allowed and q.no_side_edge():
            verdict.leaves["nowall"] += 1
            continue
        if "closed" in allowed:
            found = closed_bound(q, threshold)
            if found is not None:
                verdict.leaves["closed"] += 1
                verdict.max_bound = max(verdict.max_bound, found[0])
                verdict.max_level = max(verdict.max_level, found[1])
                continue
        if verdict.pieces + len(stack) >= budget:
            verdict.certified = False
            verdict.reason = f"budget of {budget} pieces spent"
            return verdict
        halves = piece.split()
        if halves is None:
            verdict.certified = False
            verdict.reason = "a piece too small to cut stays undecided"
            return verdict
        stack.extend(halves)
    return verdict


ALLOWED = {
    "inf": frozenset({"inf"}),
    "nowall": frozenset({"inf", "nowall"}),
    "closed": frozenset({"inf", "closed"}),
}


OUTCOMES = ("certified-as-labelled", "certified-otherwise", "not-certified")


def decide(record: dict[str, Any], threshold: int = THRESHOLD) -> dict[str, Any]:
    """Certify one recorded box under its own label, then, failing that, under any.

    The row gives the source's label and bound, the outcome, and for the run that
    decided it the pieces, the label of each leaf, the largest bound of a ``closed``
    leaf and the finest direction level that leaf needed."""
    box = Box.from_record(record)
    label = record["kind"]
    started = time.process_time()
    first = certify(box, ALLOWED[label], threshold)
    row: dict[str, Any] = {"label": label, "U": record.get("U")}
    decided = first
    if first.certified:
        row["outcome"] = OUTCOMES[0]
    else:
        anywise = (
            frozenset({"inf", "nowall", "closed"}) if box.wall else frozenset({"inf", "closed"})
        )
        second = certify(box, anywise, threshold)
        row["outcome"] = OUTCOMES[1] if second.certified else OUTCOMES[2]
        row["as_labelled"] = first.describe()
        decided = second
    row["pieces"] = decided.pieces
    row["leaves"] = dict(sorted(decided.leaves.items()))
    row["bound"] = decided.max_bound if decided.max_bound >= 0 else None
    row["level"] = decided.max_level or None
    if decided.reason:
        row["reason"] = decided.reason
    row["cpu_s"] = round(time.process_time() - started, 4)
    return row


def read_list(name: str) -> list[dict[str, Any]]:
    """The records of one box list, read as data from the retained zip."""
    with zipfile.ZipFile(DATA_ZIP) as archive:
        text = archive.read(f"{name}_final_leaves.jsonl").decode("utf-8")
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def all_boxes() -> list[tuple[str, int, dict[str, Any]]]:
    """Every box as (list, 1-based line, record)."""
    return [
        (name, line, record)
        for name in LISTS
        for line, record in enumerate(read_list(name), start=1)
    ]


def price(sample: int, seed: int) -> dict[str, Any]:
    """Time a seeded random sample of boxes and extrapolate per label class."""
    boxes = all_boxes()
    population = Counter(record["kind"] for _, _, record in boxes)
    chosen = random.Random(seed).sample(range(len(boxes)), sample)
    per_label: dict[str, list[float]] = {label: [] for label in LABELS}
    outcomes: Counter[str] = Counter()
    rows = []
    started = time.process_time()
    for index in chosen:
        name, line, record = boxes[index]
        result = decide(record)
        per_label[record["kind"]].append(result["cpu_s"])
        outcomes[f"{record['kind']}:{result['outcome']}"] += 1
        rows.append({"list": name, "line": line, **result})
    total = time.process_time() - started
    estimate = 0.0
    classes = {}
    for label in LABELS:
        times = per_label[label]
        mean = sum(times) / len(times) if times else 0.0
        classes[label] = {
            "sampled": len(times),
            "population": population[label],
            "mean_cpu_s": mean,
            "max_cpu_s": max(times) if times else 0.0,
            "extrapolated_cpu_s": mean * population[label],
        }
        estimate += mean * population[label]
    return {
        "sample": sample,
        "seed": seed,
        "cpu_s": total,
        "outcomes": dict(sorted(outcomes.items())),
        "classes": classes,
        "extrapolated_cpu_hours": estimate / 3600,
        "rows": rows,
    }


def _worker_file(out: Path, name: str, worker: int) -> Path:
    return out / f"{name}.w{worker}.jsonl"


def _done(path: Path) -> set[int]:
    """The lines a worker file already holds; a torn last line is cut off."""
    if not path.exists():
        return set()
    data = path.read_bytes()
    if data and not data.endswith(b"\n"):
        data = data[: data.rfind(b"\n") + 1]
        path.write_bytes(data)
    return {json.loads(line)["line"] for line in data.decode("utf-8").splitlines() if line}


def run(out: Path, worker: int, workers: int) -> int:
    """Decide this worker's share (every box whose global index is ``worker`` modulo
    ``workers``), appending one row per box, and skip the boxes already written."""
    out.mkdir(parents=True, exist_ok=True)
    boxes = all_boxes()
    done = {name: _done(_worker_file(out, name, worker)) for name in LISTS}
    mine = [
        (index, name, line, record)
        for index, (name, line, record) in enumerate(boxes)
        if index % workers == worker and line not in done[name]
    ]
    print(f"worker {worker} of {workers}: {len(mine)} boxes to decide", flush=True)
    tally: Counter[str] = Counter()
    started = time.process_time()
    handles = {
        name: _worker_file(out, name, worker).open("a", encoding="utf-8") for name in LISTS
    }
    try:
        for count, (_, name, line, record) in enumerate(mine, start=1):
            row = {"list": name, "line": line, **decide(record)}
            handles[name].write(json.dumps(row, sort_keys=True) + "\n")
            handles[name].flush()
            tally[f"{row['label']}:{row['outcome']}"] += 1
            if row["outcome"] != OUTCOMES[0]:
                print(f"NOT AS LABELLED {name} line {line}: {json.dumps(row)}", flush=True)
            if count % 2000 == 0 or count == len(mine):
                cpu = time.process_time() - started
                print(
                    f"{count}/{len(mine)} cpu {cpu:.1f} s {dict(sorted(tally.items()))}",
                    flush=True,
                )
    finally:
        for handle in handles.values():
            handle.close()
    return 0


def collect(out: Path) -> dict[str, list[dict[str, Any]]]:
    """Every row the workers wrote, per list, ordered by line."""
    rows: dict[str, list[dict[str, Any]]] = {}
    for name in LISTS:
        merged: dict[int, dict[str, Any]] = {}
        for path in sorted(out.glob(f"{name}.w*.jsonl")):
            for text in path.read_text(encoding="utf-8").splitlines():
                if text:
                    row = json.loads(text)
                    if row["line"] in merged:
                        msg = f"{name} line {row['line']} was decided twice"
                        raise ValueError(msg)
                    merged[row["line"]] = row
        rows[name] = [merged[line] for line in sorted(merged)]
    return rows


def summarize(out: Path) -> dict[str, Any]:
    """Per label class, how many boxes are certified, and every box that is not
    certified as labelled; refuses a run that missed or reordered a box."""
    rows = collect(out)
    classes = {label: Counter[str]() for label in LABELS}
    exceptions: list[dict[str, Any]] = []
    bounds: Counter[str] = Counter()
    levels: Counter[str] = Counter()
    pieces = Counter[str]()
    cpu = 0.0
    missing: list[str] = []
    for name in LISTS:
        records = read_list(name)
        found = {row["line"]: row for row in rows[name]}
        for line, record in enumerate(records, start=1):
            row = found.get(line)
            if row is None:
                missing.append(f"{name}:{line}")
                continue
            if row["label"] != record["kind"] or row.get("U") != record.get("U"):
                msg = f"{name} line {line}: the row's label differs from the list's"
                raise ValueError(msg)
            classes[row["label"]][row["outcome"]] += 1
            cpu += row["cpu_s"]
            if row["outcome"] != OUTCOMES[0]:
                exceptions.append(row)
            if row["bound"] is not None:
                bounds[str(row["bound"])] += 1
            if row["level"] is not None:
                levels[str(row["level"])] += 1
            pieces["1" if row["pieces"] == 1 else "2-16" if row["pieces"] <= 16 else ">16"] += 1
    decided = sum(sum(counter.values()) for counter in classes.values())
    return {
        "boxes": decided,
        "missing": missing,
        "classes": {label: {o: classes[label][o] for o in OUTCOMES} for label in LABELS},
        "all_certified": not missing
        and all(row["outcome"] != OUTCOMES[2] for row in exceptions),
        "all_as_labelled": not missing and not exceptions,
        "exceptions": exceptions,
        "largest_closed_bound": max((int(b) for b in bounds), default=None),
        "closed_bounds": dict(sorted(bounds.items())),
        "finest_levels": dict(sorted(levels.items(), key=lambda item: int(item[0]))),
        "pieces": dict(sorted(pieces.items())),
        "cpu_s": round(cpu, 1),
        "constants": constants().describe(),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n", 1)[0])
    commands = parser.add_subparsers(dest="command", required=True)
    pricing = commands.add_parser("price", help="time a random sample and extrapolate")
    pricing.add_argument("--sample", type=int, default=500)
    pricing.add_argument("--seed", type=int, default=20261102)
    pricing.add_argument("--receipts", type=Path, help="directory for the two receipts")
    running = commands.add_parser("run", help="decide one worker's share, resumably")
    running.add_argument("--out", type=Path, required=True)
    running.add_argument("--worker", type=int, required=True)
    running.add_argument("--workers", type=int, required=True)
    summary = commands.add_parser("summarize", help="count the outcomes of a finished run")
    summary.add_argument("--out", type=Path, required=True)
    summary.add_argument("--receipts", type=Path, help="directory for the summary and rows")
    args = parser.parse_args(argv)
    if args.command == "price":
        report = price(args.sample, args.seed)
        head = {key: value for key, value in report.items() if key != "rows"}
        print(json.dumps(head, indent=2))
        if args.receipts:
            stem = f"price-{args.sample}"
            _write(args.receipts / f"{stem}.json", json.dumps(head, indent=2) + "\n")
            _write(args.receipts / f"{stem}-rows.jsonl", _jsonl(report["rows"]))
        return 0
    if args.command == "run":
        if not 0 <= args.worker < args.workers:
            parser.error("the worker must lie in [0, workers)")
        return run(args.out, args.worker, args.workers)
    report = summarize(args.out)
    head = {key: value for key, value in report.items() if key != "exceptions"}
    print(json.dumps(head, indent=2))
    print(f"{len(report['exceptions'])} boxes not certified as labelled")
    for row in report["exceptions"]:
        print(json.dumps(row))
    if args.receipts:
        _write(args.receipts / "summary.json", json.dumps(report, indent=2) + "\n")
        for name, rows in collect(args.out).items():
            trimmed = [{k: v for k, v in row.items() if k != "list"} for row in rows]
            _write(args.receipts / "labels" / f"{name}.jsonl", _jsonl(trimmed))
    return 0 if report["all_certified"] else 1


def _jsonl(rows: list[dict[str, Any]]) -> str:
    compact = (",", ":")
    return "".join(json.dumps(row, sort_keys=True, separators=compact) + "\n" for row in rows)


def _write(path: Path, text: str) -> None:
    """Store a receipt plain, or as ``.gz`` above the packet's line threshold."""
    stored = write_retained(path, text.encode("utf-8"))
    print(f"wrote {stored}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
