"""A packing decided by both methods: every square, every wall, every pair.

Lane R1, stage 4 review of #1005, #1006 and #1007.  Clean-room.

There is no distance filter and no tolerance: all n(n-1)/2 pairs go through method A
(r1_axes, integers) and method B (r1_area, GMP rationals), and the verdict is
ACCEPT only when both accept every square, wall and pair with equal classes.
"""

from __future__ import annotations

from fractions import Fraction

import r1_area
import r1_axes

WALLS = ("left", "bottom", "right", "top")


def frac_text(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def from_mpq(value):
    return Fraction(int(value.numerator), int(value.denominator))


class Decision:
    """Everything both methods found, kept exact."""

    def __init__(self):
        self.n = 0
        self.side = None
        self.unit_a = []
        self.unit_b = []
        self.sense_a = []
        self.sense_b = []
        self.why_a = []
        self.clear = []  # method A: (left, bottom, right, top) per square
        self.wall_b = []  # method B: ((class, area) * 4) per square
        self.inside_b = []  # method B: area inside the box per square
        self.margin = {}  # method A: (i, j) -> Fraction, 1-based, i < j
        self.class_b = {}  # method B: (i, j) -> class
        self.area_b = {}  # method B: (i, j) -> overlap area, only where positive
        self.problems = []

    # -- summaries -------------------------------------------------------

    def disagreements(self):
        out = []
        for k in range(self.n):
            if self.unit_a[k] != self.unit_b[k]:
                out.append(("unit", k + 1))
            elif self.unit_a[k] and self.sense_a[k] != self.sense_b[k]:
                out.append(("sense", k + 1))
            if self.unit_a[k] and self.unit_b[k]:
                for w, name in enumerate(WALLS):
                    if r1_axes.classify(self.clear[k][w]) != self.wall_b[k][w][0]:
                        out.append(("wall", k + 1, name))
                contained_a = min(self.clear[k]) >= 0
                contained_b = self.inside_b[k] == 1
                if contained_a != contained_b:
                    out.append(("containment", k + 1))
        for key, value in self.margin.items():
            if r1_axes.classify(value) != self.class_b[key]:
                out.append(("pair", key[0], key[1]))
        return out

    def verdict(self):
        reasons = []
        bad_unit = [k + 1 for k in range(self.n) if not (self.unit_a[k] and self.unit_b[k])]
        if bad_unit:
            reasons.append(("not-unit", bad_unit))
        crossing = [
            (k + 1, WALLS[w])
            for k in range(self.n)
            if self.unit_a[k] and self.unit_b[k]
            for w in range(4)
            if self.clear[k][w] < 0 or self.wall_b[k][w][0] == "overlapping"
        ]
        if crossing:
            reasons.append(("crossing", crossing))
        not_inside = [
            k + 1
            for k in range(self.n)
            if self.unit_a[k] and self.unit_b[k] and self.inside_b[k] != 1
        ]
        if not_inside:
            reasons.append(("area-inside-below-1", not_inside))
        overlapping = sorted(
            key
            for key in self.margin
            if self.margin[key] < 0 or self.class_b[key] == "overlapping"
        )
        if overlapping:
            reasons.append(("overlapping", overlapping))
        disagree = self.disagreements()
        if disagree:
            reasons.append(("methods-disagree", disagree))
        return ("ACCEPT" if not reasons else "REFUSE"), reasons


def decide_squares(packing, dec, sq_a, sq_b):
    """Squares and walls by both methods (all squares)."""
    side = packing.side
    for k in range(packing.n):
        a = sq_a[k]
        dec.unit_a.append(a.unit)
        dec.sense_a.append(a.sense)
        dec.why_a.append(a.why)
        ok_b, sense_b = r1_area.unit_square(sq_b[k])
        dec.unit_b.append(ok_b)
        dec.sense_b.append(sense_b)
        dec.clear.append(r1_axes.clearances(a, side))
        if ok_b:
            ccw = r1_area.counterclockwise(sq_b[k])
            sq_b[k] = ccw
            dec.wall_b.append(
                tuple((cls, from_mpq(area)) for cls, area in r1_area.walls(ccw, side))
            )
            dec.inside_b.append(from_mpq(r1_area.area_inside_box(ccw, side)))
        else:
            dec.wall_b.append(None)
            dec.inside_b.append(None)


def decide_pair(dec, sq_a, sq_b, i, j):
    """One pair (0-based i < j) by both methods; both squares must be unit."""
    key = (i + 1, j + 1)
    dec.margin[key] = r1_axes.margin(sq_a[i], sq_a[j])
    cls, area = r1_area.pair(sq_b[i], sq_b[j])
    dec.class_b[key] = cls
    if cls == "overlapping":
        dec.area_b[key] = from_mpq(area)


def decide(packing):
    """Decide a packing the reader handed on.  Returns (Decision, sq_a, sq_b)."""
    dec = Decision()
    dec.n = packing.n
    dec.side = packing.side
    sq_a = r1_axes.of_packing(packing)
    sq_b = r1_area.of_packing(packing)
    decide_squares(packing, dec, sq_a, sq_b)
    good = [k for k in range(packing.n) if dec.unit_a[k] and dec.unit_b[k]]
    for x, i in enumerate(good):
        for j in good[x + 1 :]:
            decide_pair(dec, sq_a, sq_b, i, j)
    return dec, sq_a, sq_b


def redecide(packing, base, changed):
    """The decision of `packing`, which differs from the packing `base` decided only
    in the squares listed in `changed` (0-based) and possibly in its side.

    Pairs of two unchanged squares are taken from `base`: a pair's margin and class
    are functions of its two squares alone.  Every square and wall is decided again,
    since the walls depend on the side.
    """
    base_dec, _, _ = base
    dec = Decision()
    dec.n = packing.n
    dec.side = packing.side
    sq_a = r1_axes.of_packing(packing)
    sq_b = r1_area.of_packing(packing)
    decide_squares(packing, dec, sq_a, sq_b)
    changed = set(changed)
    good = [k for k in range(packing.n) if dec.unit_a[k] and dec.unit_b[k]]
    for x, i in enumerate(good):
        for j in good[x + 1 :]:
            key = (i + 1, j + 1)
            if i in changed or j in changed or key not in base_dec.margin:
                decide_pair(dec, sq_a, sq_b, i, j)
            else:
                dec.margin[key] = base_dec.margin[key]
                dec.class_b[key] = base_dec.class_b[key]
                if key in base_dec.area_b:
                    dec.area_b[key] = base_dec.area_b[key]
    return dec, sq_a, sq_b
