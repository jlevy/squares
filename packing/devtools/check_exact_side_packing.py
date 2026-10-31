"""Decide the packing at an exact side: non-overlap of a contact system's configuration.

Evan Daniel's exact-side reports (T-246 at ``n = 29``) export each record's contact
structure as a Julia file (``export_system.py``): variables ``t1 .. tk``, the half-angle
tangents of the record's tilted orientation classes; the ``k`` consistency polynomials
``F``; ``S = Sn / Sd``; and the contact rows, each affine in the centres and the side ``S``
with coefficients in ``Q(t)``.  A Krawczyk box proves that ``F`` has exactly one zero
``t*`` in it.  What no step of the source checks is that the configuration at ``t*`` is a
packing: that no two squares overlap and that every square lies in ``[0, S]^2``.  This
module decides that.

**The configuration.**  For every ``t`` in the box the rows of a basis of the contact
system (55 rows at ``n = 29``) are solved in interval arithmetic: an interval Krawczyk
step for the linear system proves that every system in the family has one solution and
encloses it, so the enclosure holds the exact centres and side at ``t*``.  Each square's
orientation class is read by matching its centre to a reference packing (for ``n = 29``,
T-195's exact witness, ``W-pingyou-622-n029``), and every contact row is then required to
use only the classes of the squares it names.  Squares the contact system does not
constrain (``free-20`` and ``free-21`` at ``n = 29``, free in their cells) start from
the reference packing's exact pose and are moved by small rational offsets
(``nudge_free_squares``) until they are strictly separated inside the box.

**What is decided, and how.**

- Every pair of squares and every square against each wall gets an interval enclosure of
  its separating-axis gap on each of the four edge normals.  A positive lower endpoint
  is a strict separation, certified; the least such margin is reported.  The project's
  own :func:`sqpack.promote.interval_verify.pair_verdict` is run on the same corner boxes
  as a second opinion and must agree.
- A gap whose enclosure straddles zero is a touching constraint.  No enclosure can
  certify an equality, so each is decided exactly: the gap, written symbolically as an
  affine form in the centres with coefficients in ``Q(t)`` (the absolute values in each
  square's half-width resolved by signs the enclosures decide strictly, or vanishing
  identically), must be a ``Q(t)`` multiple of one contact row.  Then the gap is zero
  wherever that row holds, so the two squares touch along that axis and do not overlap.
- A row of the basis holds at ``t*`` by construction, and so does a row proportional to
  one through a factor with no pole in the box.  Any other row holds at ``t*`` only if
  the whole system is consistent there, which ``symbolic_consistency`` decides exactly
  by elimination over ``Q(t)``: each residual vanishes identically or has a numerator
  divisible by an ``F_k``, with every pivot, every residual denominator and every
  coefficient denominator nonzero on the box.  The verdict requires that decision for
  the touching rows, for the whole system and for the rows' side against ``Sn/Sd``
  (``undecided`` names what is missing), so no Monte Carlo step enters it.

Run it from ``packing/``::

    uv run --frozen --all-extras --group dev python -m devtools.check_exact_side_packing \
        --system DATA/n29_system.jl --box DATA/n29_krawczyk.json \
        --witness resources/web/pingyou-pr622-certificate-2026-10-15/facts/n-029.yaml.gz \
        --out RECEIPTS/nonoverlap.json

Nothing here executes the system file: it is tokenized and parsed by the grammar below,
since the file is a source's data and its author's own readers ``eval`` it.
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
import sys
import time
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath as mp
from sympy import QQ
from sympy.polys.fields import FracElement, FracField
from sympy.polys.rings import PolyElement, PolyRing

from sqpack.promote.interval import decimal_string
from sqpack.promote.interval_verify import SEPARATED, pair_verdict
from sqpack.promote.krawczyk import PoseBox, certify
from sqpack.witness import validate_witness_document
from sqpack.yamlio import load_yaml

Interval = Any
#: mpmath's interval context, untyped: its stubs model neither interval arithmetic nor
#: the list form of the constructor (sqpack.promote.interval suppresses the same).
IV: Any = mp.iv
TOKEN = re.compile(
    r'\s*(?:(\d+)|([A-Za-z_][A-Za-z_0-9]*)|"([A-Za-z_0-9]+)"|(=>|//|[-+*^(),\[\]]))'
)
WALLS = ("left", "right", "bottom", "top")
TOUCH_TOLERANCE = mp.mpf("1e-30")


class SystemFormatError(ValueError):
    """The system file does not have the exported shape this parser reads."""


# --- parsing ---------------------------------------------------------------------------


def tokens(text: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    position = 0
    text = text.replace("Dict{String,Any}", "Dict")
    while position < len(text):
        match = TOKEN.match(text, position)
        if match is None or match.end() == position:
            if text[position:].strip() == "":
                break
            raise SystemFormatError(f"unexpected text at {text[position : position + 30]!r}")
        integer, name, quoted, symbol = match.groups()
        if integer is not None:
            out.append(("int", integer))
        elif name is not None:
            out.append(("name", name))
        elif quoted is not None:
            out.append(("str", quoted))
        else:
            out.append(("sym", symbol))
        position = match.end()
    return out


class Parser:
    """Recursive descent over the exported Julia subset: integers, ``big(a)//b``,
    ``t1 .. tk``, ``+ - * ^`` and parentheses, plus the row and list shapes."""

    def __init__(self, text: str, ring: PolyRing):
        self.items = tokens(text)
        self.at = 0
        self.ring = ring
        self.gens = {str(g): g for g in ring.gens}

    def peek(self) -> tuple[str, str] | None:
        return self.items[self.at] if self.at < len(self.items) else None

    def take(self, kind: str, value: str | None = None) -> str:
        item = self.peek()
        if item is None or item[0] != kind or (value is not None and item[1] != value):
            raise SystemFormatError(f"expected {value or kind}, found {item}")
        self.at += 1
        return item[1]

    def accept(self, value: str) -> bool:
        item = self.peek()
        if item is not None and item[0] == "sym" and item[1] == value:
            self.at += 1
            return True
        return False

    def expr(self) -> PolyElement:
        value = self.term()
        while True:
            if self.accept("+"):
                value = value + self.term()
            elif self.accept("-"):
                value = value - self.term()
            else:
                return value

    def term(self) -> PolyElement:
        value = self.unary()
        while self.accept("*"):
            value = value * self.unary()
        return value

    def unary(self) -> PolyElement:
        if self.accept("-"):
            return -self.unary()
        base = self.atom()
        if self.accept("^"):
            return base ** int(self.take("int"))
        return base

    def atom(self) -> PolyElement:
        item = self.peek()
        if item is None:
            raise SystemFormatError("unexpected end of expression")
        if item[0] == "int":
            self.at += 1
            return self.ring(int(item[1]))
        if item == ("name", "big"):
            self.at += 1
            self.take("sym", "(")
            numerator = int(self.take("int"))
            self.take("sym", ")")
            self.take("sym", "//")
            return self.ring(QQ(numerator, int(self.take("int"))))
        if item[0] == "name" and item[1] in self.gens:
            self.at += 1
            return self.gens[item[1]]
        if self.accept("("):
            value = self.expr()
            self.take("sym", ")")
            return value
        raise SystemFormatError(f"unexpected token {item}")

    def pair(self) -> tuple[PolyElement, PolyElement]:
        self.take("sym", "(")
        numerator = self.expr()
        self.take("sym", ",")
        denominator = self.expr()
        self.take("sym", ")")
        return numerator, denominator

    def row(self) -> Row:
        self.take("sym", "(")
        self.take("name", "Dict")
        self.take("sym", "(")
        entries: dict[str, tuple[PolyElement, PolyElement]] = {}
        while not self.accept(")"):
            name = self.take("str")
            self.take("sym", "=>")
            entries[name] = self.pair()
            self.accept(",")
        self.take("sym", ",")
        constant = self.pair()
        self.take("sym", ")")
        self.accept(",")
        return Row(entries, constant)


@dataclass
class Row:
    """One contact row: ``sum (num/den) * var + knum/kden = 0``."""

    entries: dict[str, tuple[PolyElement, PolyElement]]
    constant: tuple[PolyElement, PolyElement]


@dataclass
class ExportedSystem:
    names: list[str]
    ring: PolyRing
    field: FracField
    polynomials: list[PolyElement]
    side_numerator: PolyElement
    side_denominator: PolyElement
    unknowns: list[str]
    rows: list[Row]


def parse_system(path: Path) -> ExportedSystem:
    lines = path.read_text().splitlines()
    var_line = next(line for line in lines if line.startswith("@var "))
    names = var_line.split()[1:]
    if not names or not all(re.fullmatch(r"t\d+", n) for n in names):
        raise SystemFormatError(f"unexpected variables {names}")
    fraction_field = FracField(",".join(names), QQ)
    ring = fraction_field.ring

    def block(start: str) -> list[str]:
        first = lines.index(start)
        last = lines.index("]", first)
        return [line for line in lines[first + 1 : last] if line.strip()]

    polynomials = [Parser(line.rstrip(","), ring).expr() for line in block("F = [")]
    side = {
        key: Parser(line.split("=", 1)[1], ring).expr()
        for line in lines
        for key in ("Sn", "Sd")
        if line.startswith(f"{key} = ")
    }
    unknown_line = next(line for line in lines if line.startswith("zvars = ["))
    unknowns = re.findall(r'"([A-Za-z_0-9]+)"', unknown_line)
    rows = [Parser(line, ring).row() for line in block("rows = [")]
    if len(polynomials) != len(names):
        raise SystemFormatError(
            f"{len(polynomials)} consistency polynomials for {len(names)} variables"
        )
    return ExportedSystem(
        names, ring, fraction_field, polynomials, side["Sn"], side["Sd"], unknowns, rows
    )


# --- interval evaluation ---------------------------------------------------------------


def mid(value: Interval) -> Any:
    """The midpoint of an enclosure as an ordinary mpmath float."""
    return mp.mpf(value.mid)


def iv_fraction(value: Fraction | Any) -> Interval:
    fraction = Fraction(int(value.numerator), int(value.denominator))
    return IV.mpf(fraction.numerator) / fraction.denominator


class Evaluator:
    """Interval values of polynomials in ``t`` over one box, powers cached."""

    def __init__(self, ring: PolyRing, box: Sequence[Interval]):
        self.ring = ring
        self.box = list(box)
        self.powers: list[list[Interval]] = [[IV.mpf(1)] for _ in box]

    def power(self, index: int, exponent: int) -> Interval:
        cache = self.powers[index]
        while len(cache) <= exponent:
            cache.append(cache[-1] * self.box[index])
        return cache[exponent]

    def poly(self, value: PolyElement) -> Interval:
        total = IV.mpf(0)
        for monomial, coefficient in value.terms():
            term = iv_fraction(coefficient)
            for index, exponent in enumerate(monomial):
                if exponent:
                    term = term * self.power(index, exponent)
            total = total + term
        return total

    def ratio(self, numerator: PolyElement, denominator: PolyElement) -> Interval:
        bottom = self.poly(denominator)
        if bottom.a <= 0 <= bottom.b:
            raise ValueError("a denominator's enclosure contains zero over the box")
        return self.poly(numerator) / bottom


# --- the configuration -----------------------------------------------------------------


def choose_basis(system: ExportedSystem, centre: Sequence[Any]) -> list[int]:
    """Rows of a nonsingular square subsystem, chosen greedily at the box centre."""
    point = Evaluator(system.ring, [IV.mpf(c) for c in centre])
    column = {name: k for k, name in enumerate(system.unknowns)}
    tolerance = mp.mpf(10) ** (-mp.mp.dps // 2)
    reduced: list[tuple[int, list[Any]]] = []
    chosen: list[int] = []
    for index, row in enumerate(system.rows):
        vector = [mp.mpf(0)] * len(system.unknowns)
        for name, (numerator, denominator) in row.entries.items():
            vector[column[name]] = mid(point.ratio(numerator, denominator))
        for lead, basis_vector in reduced:
            factor = vector[lead] / basis_vector[lead]
            if factor:
                vector = [v - factor * b for v, b in zip(vector, basis_vector, strict=True)]
        # Residues of a dependent row are rounding noise: clear them, then pivot on the
        # largest entry, so no later reduction divides by noise.
        vector = [v if abs(v) > tolerance else mp.mpf(0) for v in vector]
        lead = max(range(len(vector)), key=lambda k: abs(vector[k]))
        if vector[lead] != 0:
            reduced.append((lead, vector))
            chosen.append(index)
        if len(chosen) == len(system.unknowns):
            break
    if len(chosen) != len(system.unknowns):
        raise ValueError(
            f"the rows have rank {len(chosen)} < {len(system.unknowns)} at the box centre"
        )
    return chosen


def solve_enclosure(
    system: ExportedSystem, basis: list[int], box: Sequence[Interval], centre: Sequence[Any]
) -> dict[str, Interval]:
    """Interval Krawczyk for ``A(t) z = b(t)``, ``t`` in the box: one enclosure for all."""
    size = len(system.unknowns)
    column = {name: k for k, name in enumerate(system.unknowns)}
    family = Evaluator(system.ring, box)
    point = Evaluator(system.ring, [IV.mpf(c) for c in centre])

    def assemble(evaluator: Evaluator) -> tuple[list[list[Interval]], list[Interval]]:
        matrix = [[IV.mpf(0)] * size for _ in basis]
        right = []
        for i, index in enumerate(basis):
            row = system.rows[index]
            for name, (numerator, denominator) in row.entries.items():
                matrix[i][column[name]] = evaluator.ratio(numerator, denominator)
            right.append(-evaluator.ratio(*row.constant))
        return matrix, right

    point_matrix, point_right = assemble(point)
    approximate = mp.matrix([[mid(v) for v in row] for row in point_matrix])
    inverse = approximate**-1
    middle = inverse * mp.matrix([mid(v) for v in point_right])
    matrix, right = assemble(family)
    inv = [[IV.mpf(inverse[i, j]) for j in range(size)] for i in range(size)]
    approx = [IV.mpf(middle[i]) for i in range(size)]
    residual = [
        right[i] - sum((matrix[i][j] * approx[j] for j in range(size)), IV.mpf(0))
        for i in range(size)
    ]
    correction = [
        sum((inv[i][k] * residual[k] for k in range(size)), IV.mpf(0)) for i in range(size)
    ]
    radius = mp.mpf(10) ** (-mp.mp.dps // 3)
    offsets = [IV.mpf([-radius, radius])] * size
    contraction = [
        [sum((inv[i][k] * matrix[k][j] for k in range(size)), IV.mpf(0)) for j in range(size)]
        for i in range(size)
    ]
    image = []
    for i in range(size):
        spread = sum(
            (
                ((IV.mpf(1) if i == j else IV.mpf(0)) - contraction[i][j]) * offsets[j]
                for j in range(size)
            ),
            IV.mpf(0),
        )
        image.append(correction[i] + spread)
    if not all(-radius < v.a and v.b < radius for v in image):
        raise ValueError("the linear Krawczyk image is not inside the box: no enclosure")
    return {name: approx[k] + image[k] for name, k in column.items()}


@dataclass
class Square:
    index: int
    label: str
    klass: int
    x: Interval
    y: Interval
    cos: Interval
    sin: Interval
    variables: tuple[str, str] | None
    exact_centre: tuple[Fraction, Fraction] | None = None


def reference_poses(path: Path) -> list[tuple[int, Fraction, Fraction, Fraction, Fraction]]:
    document = (
        load_yaml(gzip.decompress(path.read_bytes()).decode())
        if path.suffix == ".gz"
        else load_yaml(path.read_text())
    )
    witness = validate_witness_document(document, path=path)
    poses = []
    for square in witness["squares"]:
        cx, cy = (Fraction(v) for v in square["center"])
        ux, uy = (Fraction(v) for v in square["basis"])
        poses.append((int(square["id"]), cx, cy, ux, uy))
    return poses


def half_angle_angle(t: Any) -> Any:
    return 2 * mp.atan(t)


def reduce_quarter(angle: Any) -> Any:
    quarter = mp.pi / 2
    return angle - quarter * mp.nint(angle / quarter)


def build_squares(
    centres: dict[str, Interval],
    box: Sequence[Interval],
    tstar: Sequence[Any],
    reference: list[tuple[int, Fraction, Fraction, Fraction, Fraction]],
) -> tuple[list[Square], dict[str, Any]]:
    indices = sorted(
        {int(name[1:]) for name in centres if name[0] in "xy" and name[1:].isdigit()}
    )
    class_angles = [reduce_quarter(half_angle_angle(t)) for t in tstar]
    cos_sin = [((1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)) for t in box]
    unused = {pose[0]: pose for pose in reference}
    squares: list[Square] = []
    matches = {}
    for index in indices:
        x, y = centres[f"x{index}"], centres[f"y{index}"]
        nearest = min(
            unused.values(),
            key=lambda p: (
                abs(mp.mpf(p[1].numerator) / p[1].denominator - mid(x))
                + abs(mp.mpf(p[2].numerator) / p[2].denominator - mid(y))
            ),
        )
        distance = abs(mp.mpf(nearest[1].numerator) / nearest[1].denominator - mid(x)) + abs(
            mp.mpf(nearest[2].numerator) / nearest[2].denominator - mid(y)
        )
        if distance > mp.mpf("1e-12"):
            raise ValueError(
                f"square {index}: no reference square within 1e-12 (nearest {distance})"
            )
        del unused[nearest[0]]
        angle = reduce_quarter(
            mp.atan2(
                mp.mpf(nearest[4].numerator) / nearest[4].denominator,
                mp.mpf(nearest[3].numerator) / nearest[3].denominator,
            )
        )
        klass = 0
        if abs(angle) > mp.mpf("1e-12"):
            gaps = [abs(angle - a) for a in class_angles]
            klass = 1 + min(range(len(gaps)), key=gaps.__getitem__)
            if gaps[klass - 1] > mp.mpf("1e-12"):
                raise ValueError(f"square {index}: angle {angle} matches no class")
        cosine, sine = (IV.mpf(1), IV.mpf(0)) if klass == 0 else cos_sin[klass - 1]
        squares.append(
            Square(index, str(index), klass, x, y, cosine, sine, (f"x{index}", f"y{index}"))
        )
        matches[str(index)] = {
            "reference_id": nearest[0],
            "class": klass,
            "centre_distance": mp.nstr(distance, 3),
        }
    for ident, cx, cy, ux, uy in unused.values():
        if ux * ux + uy * uy != 1:
            raise ValueError(f"reference square {ident}: basis is not an exact unit vector")
        squares.append(
            Square(
                len(squares) + 1000,
                f"free-{ident}",
                -1,
                iv_fraction(cx),
                iv_fraction(cy),
                iv_fraction(ux),
                iv_fraction(uy),
                None,
                (cx, cy),
            )
        )
        matches[f"free-{ident}"] = {
            "reference_id": ident,
            "class": "reference pose (not in the contact system)",
        }
    return squares, matches


def clearance(square: Square, squares: list[Square], side: Interval) -> Any:
    """The least certified lower gap between `square` and everything else."""
    lows = [min(gap.a for gap in wall_gaps(square, side).values())]
    for other in squares:
        if other is not square:
            lows.append(max(gap.a for _, _, gap in pair_gaps(square, other)))  # noqa: PERF401
    return min(lows)


def nudge_free_squares(squares: list[Square], side: Interval) -> dict[str, list[str]]:
    """Translate each free square by a small exact offset that leaves it clear.

    A square the contact system does not constrain may sit anywhere in its cell, and
    the reference packing's pose can touch a neighbour at zero gap, which no enclosure
    can certify.  Each free square tries the eight unit directions at three scales and
    keeps the offset with the largest certified clearance; the offsets are exact
    rationals and the receipt records them.
    """
    offsets: dict[str, list[str]] = {}
    free = [s for s in squares if s.variables is None and s.exact_centre is not None]
    for _ in range(2):
        for square in free:
            assert square.exact_centre is not None
            cx, cy = square.exact_centre
            best = (clearance(square, squares, side), Fraction(0), Fraction(0))
            for scale in (Fraction(1, 10**9), Fraction(1, 10**6), Fraction(1, 10**4)):
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if dx == dy == 0:
                            continue
                        trial = Square(
                            square.index,
                            square.label,
                            square.klass,
                            iv_fraction(cx + dx * scale),
                            iv_fraction(cy + dy * scale),
                            square.cos,
                            square.sin,
                            None,
                            (cx + dx * scale, cy + dy * scale),
                        )
                        others = [trial if s is square else s for s in squares]
                        value = clearance(trial, others, side)
                        if value > best[0]:
                            best = (value, dx * scale, dy * scale)
            if best[1] or best[2]:
                square.exact_centre = (cx + best[1], cy + best[2])
                square.x, square.y = (
                    iv_fraction(square.exact_centre[0]),
                    iv_fraction(square.exact_centre[1]),
                )
                previous = offsets.get(square.label, ["0", "0"])
                offsets[square.label] = [
                    str(Fraction(previous[0]) + best[1]),
                    str(Fraction(previous[1]) + best[2]),
                ]
    return offsets


def check_row_classes(system: ExportedSystem, squares: list[Square]) -> list[str]:
    """Every row may use only the half-angle variables of the squares it names."""
    klass = {s.variables[0][1:]: s.klass for s in squares if s.variables}
    problems = []
    for index, row in enumerate(system.rows):
        named = {name[1:] for name in row.entries if name != "S"}
        allowed = {f"t{klass[n]}" for n in named if klass.get(n, 0) > 0}
        used = set()
        for numerator, denominator in [*row.entries.values(), row.constant]:
            for poly in (numerator, denominator):
                for monomial in poly.monoms():
                    used |= {system.names[k] for k, e in enumerate(monomial) if e}
        if not used <= allowed:
            problems.append(
                f"row {index} names squares {sorted(named)} but uses {sorted(used - allowed)}"
            )
    return problems


# --- gaps: enclosures and symbolic forms -----------------------------------------------


@dataclass
class Affine:
    """``sum coefficient * variable + constant`` with coefficients in ``Q(t)``."""

    terms: dict[str, FracElement] = field(default_factory=dict)
    constant: Any = 0

    def add(self, other: Affine, scale: Any = 1) -> Affine:
        terms = dict(self.terms)
        for name, value in other.terms.items():
            terms[name] = terms.get(name, 0) + scale * value
        return Affine(
            {k: v for k, v in terms.items() if v != 0}, self.constant + scale * other.constant
        )


class Symbolic:
    """Exact orientations and centres of the squares, in the system's ``Q(t)``."""

    def __init__(self, system: ExportedSystem):
        self.field = system.field
        self.gens = self.field.gens

    def orientation(self, square: Square) -> tuple[Any, Any]:
        if square.klass == 0:
            return self.field(1), self.field(0)
        if square.klass < 0:
            raise ValueError("a reference-pose square has no symbolic orientation")
        t = self.gens[square.klass - 1]
        return (1 - t**2) / (1 + t**2), 2 * t / (1 + t**2)

    def centre(self, square: Square) -> tuple[Affine, Affine]:
        if square.variables is None:
            raise ValueError("a reference-pose square has no symbolic centre")
        x, y = square.variables
        return Affine({x: self.field(1)}), Affine({y: self.field(1)})


def interval_axes(square: Square) -> list[tuple[Interval, Interval]]:
    return [(square.cos, square.sin), (-square.sin, square.cos)]


def half_width(square: Square, axis: tuple[Interval, Interval]) -> Interval:
    u, w = interval_axes(square)
    return (abs(axis[0] * u[0] + axis[1] * u[1]) + abs(axis[0] * w[0] + axis[1] * w[1])) / 2


def pair_gaps(first: Square, second: Square) -> Iterator[tuple[int, int, Interval]]:
    """For each of the four axes: (axis owner 0/1, axis index, direction, gap enclosure)."""
    for owner, square in enumerate((first, second)):
        for which, axis in enumerate(interval_axes(square)):
            delta = axis[0] * (second.x - first.x) + axis[1] * (second.y - first.y)
            reach = half_width(first, axis) + half_width(second, axis)
            yield owner * 2 + which, +1, delta - reach
            yield owner * 2 + which, -1, -delta - reach


def wall_gaps(square: Square, side: Interval) -> dict[str, Interval]:
    hx = (abs(square.cos) + abs(square.sin)) / 2
    return {
        "left": square.x - hx,
        "right": side - square.x - hx,
        "bottom": square.y - hx,
        "top": side - square.y - hx,
    }


def sign_of(value: Interval) -> int:
    if value.a > 0:
        return 1
    if value.b < 0:
        return -1
    raise ValueError("an undecided sign")


def symbolic_half_width(
    symbolic: Symbolic,
    square: Square,
    axis: tuple[Any, Any],
    numeric_axis: tuple[Interval, Interval],
) -> Any:
    c, s = symbolic.orientation(square)
    total = 0
    for (ux, uy), (nx, ny) in zip(((c, s), (-s, c)), interval_axes(square), strict=True):
        dot = axis[0] * ux + axis[1] * uy
        if dot == 0:
            continue
        total = total + sign_of(numeric_axis[0] * nx + numeric_axis[1] * ny) * dot
    return total / 2


def symbolic_pair_gap(
    symbolic: Symbolic, first: Square, second: Square, axis_index: int, direction: int
) -> Affine:
    owner = (first, second)[axis_index // 2]
    c, s = symbolic.orientation(owner)
    axis = ((c, s), (-s, c))[axis_index % 2]
    numeric_axis = interval_axes(owner)[axis_index % 2]
    (fx, fy), (sx, sy) = symbolic.centre(first), symbolic.centre(second)
    delta = Affine().add(sx, axis[0]).add(sy, axis[1]).add(fx, -axis[0]).add(fy, -axis[1])
    reach = symbolic_half_width(symbolic, first, axis, numeric_axis) + symbolic_half_width(
        symbolic, second, axis, numeric_axis
    )
    gap = Affine({k: direction * v for k, v in delta.terms.items()}, direction * delta.constant)
    return Affine(gap.terms, gap.constant - reach)


def symbolic_wall_gap(symbolic: Symbolic, square: Square, wall: str) -> Affine:
    c, s = symbolic.orientation(square)
    numeric = (sign_of(square.cos) if c != 0 else 0, sign_of(square.sin) if s != 0 else 0)
    reach = (numeric[0] * c + numeric[1] * s) / 2
    x, y = symbolic.centre(square)
    side = Affine({"S": symbolic.field(1)})
    if wall == "left":
        return Affine(x.terms, -reach)
    if wall == "bottom":
        return Affine(y.terms, -reach)
    centre = x if wall == "right" else y
    return Affine(side.add(centre, -1).terms, -reach)


def row_form(system: ExportedSystem, row: Row) -> Affine:
    terms = {
        name: system.field(numerator) / system.field(denominator)
        for name, (numerator, denominator) in row.entries.items()
    }
    return Affine(
        {k: v for k, v in terms.items() if v != 0},
        system.field(row.constant[0]) / system.field(row.constant[1]),
    )


def proportional(left: Affine, right: Affine) -> Any:
    """The ``Q(t)`` factor ``lam`` with ``left == lam * right``, or ``None``."""
    if set(left.terms) != set(right.terms) or not left.terms:
        return None
    anchor = next(iter(sorted(left.terms)))
    factor = left.terms[anchor] / right.terms[anchor]
    if (
        all(left.terms[k] == factor * right.terms[k] for k in left.terms)
        and left.constant == factor * right.constant
    ):
        return factor
    return None


def symbolic_consistency(
    system: ExportedSystem,
    basis: list[int],
    forms: list[Affine],
    targets: list[int],
    *,
    box: Sequence[Interval],
    cpu_limit: float,
    extra: dict[str, Affine] | None = None,
) -> dict[str, Any]:
    """Decide exactly whether each target row holds wherever ``F`` vanishes in the box.

    The basis rows are eliminated over ``Q(t)``, so every unknown becomes a rational
    function of ``t``; each target row then reduces to a residual ``c(t)``.  A residual
    that is identically zero holds everywhere.  One whose numerator is divisible by a
    consistency polynomial ``F_k`` vanishes at ``t*``, where Krawczyk proved every
    ``F_k`` zero, provided its denominator and every pivot are nonzero over the box,
    which interval evaluation checks.  Anything else is reported undecided.
    """
    started = time.process_time()
    family = Evaluator(system.ring, box)
    pending = [Affine(dict(forms[i].terms), forms[i].constant) for i in basis]
    goals: dict[Any, Affine] = {
        j: Affine(dict(forms[j].terms), forms[j].constant) for j in targets
    }
    for name, form in (extra or {}).items():
        goals[name] = Affine(dict(form.terms), form.constant)

    def poles_excluded(form: Affine) -> bool:
        """Whether every coefficient of ``form`` has a denominator nonzero on the box, so
        the row means the same at ``t*`` as over ``Q(t)``."""
        for value in [*form.terms.values(), form.constant]:
            denominator = getattr(value, "denom", None)
            if denominator is None:
                continue
            bottom = family.poly(denominator)
            if bottom.a <= 0 <= bottom.b:
                return False
        return True

    finite_goals = {j: poles_excluded(goal) for j, goal in goals.items()}
    pivots_nonzero = True

    def weight(value: Any) -> int:
        return len(value.numer.terms()) + len(value.denom.terms())

    while pending:
        if time.process_time() - started > cpu_limit:
            return {
                "decided": False,
                "reason": f"CPU limit {cpu_limit} s reached during elimination",
            }
        row = min(
            pending, key=lambda r: (len(r.terms), min(weight(v) for v in r.terms.values()))
        )
        pending.remove(row)
        name = min(row.terms, key=lambda k: weight(row.terms[k]))
        pivot = row.terms[name]
        for part in (pivot.numer, pivot.denom):
            value = family.poly(part)
            pivots_nonzero &= not (value.a <= 0 <= value.b)
        solved = Affine(
            {k: v / pivot for k, v in row.terms.items() if k != name}, row.constant / pivot
        )
        for other in [*pending, *goals.values()]:
            factor = other.terms.pop(name, None)
            if factor is not None:
                for k, v in solved.terms.items():
                    other.terms[k] = other.terms.get(k, 0) - factor * v
                other.terms = {k: v for k, v in other.terms.items() if v != 0}
                other.constant = other.constant - factor * solved.constant
    verdicts = {}
    for j, goal in goals.items():
        if not finite_goals[j]:
            verdicts[str(j)] = "undecided"
            continue
        if goal.terms:
            verdicts[str(j)] = "unknowns left after elimination"
            continue
        residual = goal.constant
        if residual == 0:
            verdicts[str(j)] = "identically zero"
            continue
        bottom = family.poly(residual.denom)
        divisors = [
            k + 1 for k, f in enumerate(system.polynomials) if residual.numer.rem(f) == 0
        ]
        if divisors and not (bottom.a <= 0 <= bottom.b):
            verdicts[str(j)] = f"numerator divisible by F_{divisors[0]}"
        else:
            verdicts[str(j)] = "undecided"
    decided = pivots_nonzero and all(
        v != "undecided" and not v.startswith("unknowns") for v in verdicts.values()
    )
    return {
        "decided": decided,
        "pivots_nonzero_on_box": pivots_nonzero,
        "rows": verdicts,
        "cpu_seconds": round(time.process_time() - started, 1),
    }


def polynomial_system(system: ExportedSystem) -> Any:
    """``F`` as the callable :func:`sqpack.promote.krawczyk.certify` expects.

    Dual numbers in, residuals out.
    """
    terms = [
        [(monomial, iv_fraction(c)) for monomial, c in f.terms()] for f in system.polynomials
    ]
    degrees = [max(m[i] for f in terms for m, _ in f) for i in range(len(system.names))]

    def residuals(*values: Any) -> list[Any]:
        powers = []
        for value, top in zip(values, degrees, strict=True):
            cache = [value * 0 + 1, value]
            while len(cache) <= top:
                cache.append(cache[-1] * value)
            powers.append(cache)
        out = []
        for polynomial in terms:
            total = values[0] * 0
            for monomial, coefficient in polynomial:
                term = powers[0][0] * coefficient
                for index, exponent in enumerate(monomial):
                    if exponent:
                        term = term * powers[index][exponent]
                total = total + term
            out.append(total)
        return out

    return residuals


def independent_krawczyk(
    system: ExportedSystem,
    certificate: dict[str, Any],
    digits: int,
    compare: Fraction | None = None,
) -> dict[str, Any]:
    """Re-certify the source's box with the project's own operator (mpmath intervals).

    The operator contracts the box as far as its working precision allows, and ``Sn/Sd``
    over the contracted box (the elimination shows ``S = Sn/Sd`` identically) encloses
    the decided side ``S*`` that tightly; with ``compare``, ``S*`` is ordered against it.
    """
    started = time.process_time()
    box = PoseBox.around(system.names, certificate["tstar"], str(certificate["radius"]))
    root = certify(polynomial_system(system), box, digits=digits)
    previous = mp.mp.dps, IV.dps
    mp.mp.dps = IV.dps = digits + 20
    try:
        tight = [IV.mpf([lo, hi]) for lo, hi in zip(root.box.lo, root.box.hi, strict=True)]
        side = Evaluator(system.ring, tight).ratio(
            system.side_numerator, system.side_denominator
        )
        enclosure = outward(side, digits)
    finally:
        mp.mp.dps, IV.dps = previous
    result: dict[str, Any] = {
        "tool": "sqpack.promote.krawczyk.certify",
        "exists": root.exists,
        "unique": root.unique,
        "iterations": root.iterations,
        "working_digits": root.working_precision,
        "contracted_radius": root.max_radius,
        "side_enclosure": enclosure,
    }
    if compare is not None:
        low, high = Fraction(enclosure[0]), Fraction(enclosure[1])
        order = "below" if high < compare else "above" if low > compare else "undecided"
        result["against_rational"] = {
            "side_is": order,
            # Decimal, not float: the gap can lie far below binary64's range.
            "rational_minus_side": [scientific(compare - high), scientific(compare - low)],
        }
    result["cpu_seconds"] = round(time.process_time() - started, 1)
    return result


# --- the decision ----------------------------------------------------------------------


def decide(
    system_path: Path,
    box_path: Path,
    reference: list[tuple[int, Fraction, Fraction, Fraction, Fraction]],
    digits: int,
    cpu_limit: float = 900.0,
    *,
    side_digits: int = 80,
    compare: Fraction | None = None,
) -> dict[str, Any]:
    started = time.process_time()
    mp.mp.dps = digits
    IV.dps = digits
    system = parse_system(system_path)
    certificate = json.loads(box_path.read_text())
    if not certificate.get("certified"):
        raise ValueError("the box file does not record a certified box")
    radius = mp.mpf(certificate["radius"])
    tstar = [mp.mpf(v) for v in certificate["tstar"]]
    box = [IV.mpf([t - radius, t + radius]) for t in tstar]

    krawczyk = independent_krawczyk(system, certificate, digits=side_digits, compare=compare)
    mp.mp.dps = digits
    IV.dps = digits
    basis = choose_basis(system, tstar)
    centres = solve_enclosure(system, basis, box, tstar)
    side = centres["S"]
    side_check = Evaluator(system.ring, box).ratio(
        system.side_numerator, system.side_denominator
    )
    squares, matches = build_squares(centres, box, tstar, reference)
    offsets = nudge_free_squares(squares, side)
    class_problems = check_row_classes(system, squares)
    symbolic = Symbolic(system)
    forms = [row_form(system, row) for row in system.rows]
    basis_set = set(basis)

    def exactness(row_index: int) -> str:
        if row_index in basis_set:
            return "basis"
        if any(proportional(forms[row_index], forms[b]) is not None for b in basis):
            return "proportional-to-basis"
        return "consistency"

    family = Evaluator(system.ring, box)

    def finite_on_box(factor: Any) -> bool:
        """Whether ``factor`` has no pole in the box: ``gap = factor * row`` then gives
        ``gap(t*) = 0`` wherever the row holds at ``t*``."""
        bottom = family.poly(factor.denom)
        return not (bottom.a <= 0 <= bottom.b)

    def match(gap: Affine) -> tuple[int, str] | None:
        for row_index, form in enumerate(forms):
            factor = proportional(gap, form)
            if factor is not None and finite_on_box(factor):
                return row_index, exactness(row_index)
        return None

    separated_margins: list[Any] = []
    touching: list[dict[str, Any]] = []
    failures: list[str] = []
    second_opinion_disagreements: list[str] = []
    for i, first in enumerate(squares):
        for second in squares[i + 1 :]:
            gaps = list(pair_gaps(first, second))
            best = max(gap.a for _, _, gap in gaps)
            corners = [corner_box(first), corner_box(second)]
            verdict = pair_verdict(corners[0], corners[1])
            label = f"{first.label}-{second.label}"
            if best > 0:
                separated_margins.append((best, label))
                if verdict != SEPARATED:
                    second_opinion_disagreements.append(
                        f"{label}: margin {mp.nstr(best, 5)} but pair_verdict {verdict}"
                    )
                continue
            candidates = [
                (axis, direction)
                for axis, direction, gap in gaps
                if gap.a <= 0 <= gap.b and gap.b - gap.a < TOUCH_TOLERANCE
            ]
            decided = None
            if first.variables and second.variables:
                for axis, direction in candidates:
                    found = match(symbolic_pair_gap(symbolic, first, second, axis, direction))
                    if found is not None:
                        decided = {
                            "pair": label,
                            "axis": f"{'AB'[axis // 2]}{axis % 2}",
                            "row": found[0],
                            "exact_by": found[1],
                        }
                        break
            if decided is None:
                failures.append(
                    f"pair {label}: not strictly separated (best lower gap "
                    f"{mp.nstr(best, 5)}) and no exact contact row"
                )
            else:
                touching.append(decided)
    wall_margins: list[Any] = []
    for square in squares:
        for wall, gap in wall_gaps(square, side).items():
            if gap.a > 0:
                wall_margins.append((gap.a, f"{square.label}-{wall}"))
                continue
            decided = None
            if square.variables and gap.b - gap.a < TOUCH_TOLERANCE:
                found = match(symbolic_wall_gap(symbolic, square, wall))
                if found is not None:
                    decided = {
                        "pair": f"{square.label}-{wall}",
                        "axis": wall,
                        "row": found[0],
                        "exact_by": found[1],
                    }
            if decided is None:
                failures.append(
                    f"{square.label} against the {wall} wall: lower gap "
                    f"{mp.nstr(gap.a, 5)}, no exact contact row"
                )
            else:
                touching.append(decided)

    least_pair = min(separated_margins, key=lambda m: m[0], default=None)
    least_wall = min(wall_margins, key=lambda m: m[0], default=None)
    consistency_rows = sorted({t["row"] for t in touching if t["exact_by"] == "consistency"})
    consistency = (
        symbolic_consistency(
            system, basis, forms, consistency_rows, box=box, cpu_limit=cpu_limit
        )
        if consistency_rows
        else {"decided": True, "rows": {}}
    )
    # Beyond what non-overlap needs: every distinct row off the basis, and the side the
    # source's Sn/Sd gives, against the elimination's own side.
    seen: set[tuple[Any, ...]] = set()
    off_basis = []
    for index, form in enumerate(forms):
        key = (tuple(sorted((k, str(v)) for k, v in form.terms.items())), str(form.constant))
        if index not in basis_set and key not in seen:
            off_basis.append(index)
        seen.add(key)
    side_form = Affine(
        {"S": system.field(1)},
        -(system.field(system.side_numerator) / system.field(system.side_denominator)),
    )
    whole_system = symbolic_consistency(
        system,
        basis,
        forms,
        off_basis,
        box=box,
        cpu_limit=cpu_limit,
        extra={"S - Sn/Sd": side_form},
    )
    side_row = str((whole_system.get("rows") or {}).get("S - Sn/Sd", "undecided"))
    undecided = [
        reason
        for reason, holds in (
            ("the Krawczyk box's zero is not proved unique", bool(krawczyk["unique"])),
            (
                "a touching constraint's off-basis row is not decided at t*",
                bool(consistency.get("decided")),
            ),
            (
                "the whole contact system is not decided consistent at t*",
                bool(whole_system.get("decided")),
            ),
            (
                "the rows' side is not decided equal to Sn/Sd",
                side_row != "undecided" and not side_row.startswith("unknowns"),
            ),
        )
        if not holds
    ]
    decided_all = (
        not failures
        and not class_problems
        and not second_opinion_disagreements
        and not undecided
    )
    return {
        "format": "exact-side-packing/1",
        "system": {
            "variables": system.names,
            "rows": len(system.rows),
            "unknowns": len(system.unknowns),
            "basis_rows": basis,
        },
        "box": {
            "radius": certificate["radius"],
            "tstar": certificate["tstar"],
            "independent_krawczyk": krawczyk,
        },
        "working_digits": digits,
        "side_enclosure": {"from_rows": outward(side), "from_Sn_over_Sd": outward(side_check)},
        "squares": {
            "in_contact_system": sum(1 for s in squares if s.variables),
            "reference_pose": sum(1 for s in squares if not s.variables),
            "matches": matches,
        },
        "row_class_problems": class_problems,
        "pairs": {
            "tested": len(squares) * (len(squares) - 1) // 2,
            "strictly_separated": len(separated_margins),
            "least_margin": None
            if least_pair is None
            else {"pair": least_pair[1], "lower_bound": downward(least_pair[0])},
            "second_opinion": "sqpack.promote.interval_verify.pair_verdict",
            "second_opinion_disagreements": second_opinion_disagreements,
        },
        "walls": {
            "tested": 4 * len(squares),
            "strictly_inside": len(wall_margins),
            "least_margin": None
            if least_wall is None
            else {"constraint": least_wall[1], "lower_bound": downward(least_wall[0])},
        },
        "touching": {
            "count": len(touching),
            "by_exactness": {
                k: sum(1 for t in touching if t["exact_by"] == k)
                for k in ("basis", "proportional-to-basis", "consistency")
            },
            "consistency_rows": consistency_rows,
            "consistency_route": (
                "symbolic elimination over Q(t) of the basis rows (deterministic)"
            ),
            "consistency": consistency,
            "constraints": touching,
        },
        "free_square_offsets": offsets,
        "failures": failures,
        "undecided": undecided,
        "decided": decided_all,
        "contacts_exact_without_monte_carlo": bool(consistency.get("decided")),
        "whole_contact_system_at_tstar": whole_system,
        "verdict": (
            "packing: every non-touching pair and wall strictly separated; every touching "
            "constraint is a contact row"
            if decided_all
            else "not decided"
        ),
        "cpu_seconds": round(time.process_time() - started, 1),
    }


def scientific(value: Fraction, digits: int = 12) -> str:
    """A rational in scientific notation to ``digits`` places, at any exponent."""
    if value == 0:
        return "0"
    with localcontext() as context:
        context.prec = digits
        context.Emin = -(10**9)
        context.Emax = 10**9
        return f"{Decimal(value.numerator) / Decimal(value.denominator):.{digits - 1}e}"


def case_exact_form(path: Path) -> Fraction:
    """The ``packing.verified_upper_bound.exact_form`` a case record's front matter states."""
    front = path.read_text().split("---", 2)[1]
    return Fraction(str(load_yaml(front)["packing"]["verified_upper_bound"]["exact_form"]))


def outward(value: Interval, digits: int = 70) -> list[str]:
    """An enclosure's endpoints as decimals rounded outward, so the print still encloses."""
    return [
        decimal_string(mp.mpf(value.a), digits, upward=False),
        decimal_string(mp.mpf(value.b), digits, upward=True),
    ]


def downward(value: Any, digits: int = 12) -> str:
    return decimal_string(mp.mpf(value), digits, upward=False)


def corner_box(square: Square) -> list[tuple[Interval, Interval]]:
    ux, uy = square.cos / 2, square.sin / 2
    vx, vy = -square.sin / 2, square.cos / 2
    x, y = square.x, square.y
    return [
        (x - ux - vx, y - uy - vy),
        (x + ux - vx, y + uy - vy),
        (x + ux + vx, y + uy + vy),
        (x - ux + vx, y - uy + vy),
    ]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("--system", type=Path, required=True)
    parser.add_argument("--box", type=Path, required=True)
    parser.add_argument(
        "--witness", type=Path, required=True, help="the reference packing (Witness/v2)"
    )
    parser.add_argument("--digits", type=int, default=120)
    parser.add_argument(
        "--side-digits", type=int, default=80, help="precision of the re-certified box"
    )
    parser.add_argument(
        "--compare-case",
        type=Path,
        help="a case record whose verified_upper_bound.exact_form to order S* against",
    )
    parser.add_argument(
        "--cpu-limit",
        type=float,
        default=900.0,
        help="CPU seconds for the symbolic elimination",
    )
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    sys.set_int_max_str_digits(0)
    compare = case_exact_form(args.compare_case) if args.compare_case else None
    receipt = decide(
        args.system,
        args.box,
        reference_poses(args.witness),
        args.digits,
        args.cpu_limit,
        side_digits=args.side_digits,
        compare=compare,
    )
    receipt["reference_witness"] = str(args.witness)
    text = json.dumps(receipt, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text)
    summary = {
        k: receipt[k] for k in ("verdict", "failures", "row_class_problems", "cpu_seconds")
    }
    summary["pairs"] = {
        k: receipt["pairs"][k] for k in ("tested", "strictly_separated", "least_margin")
    }
    summary["walls"] = receipt["walls"]
    summary["touching"] = {
        k: receipt["touching"][k]
        for k in ("count", "by_exactness", "consistency_rows", "consistency")
    }
    summary["free_square_offsets"] = receipt["free_square_offsets"]
    summary["side_enclosure"] = receipt["side_enclosure"]
    print(json.dumps(summary, indent=1)[:3000])
    return 0 if receipt["decided"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
