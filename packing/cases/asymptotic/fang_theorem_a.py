"""Kevin Fang's Theorem A, c*(k) < 4 sqrt(2k) + 1 for every k >= 6, checked exactly.

Kevin Fang's note *Packing k^2 - ceil(sqrt(32k)) - 1 unit squares in a square of side less
than k* (v0.2, 24 October 2026, doi:10.5281/zenodo.23624565; issue #797; retained in
``packing/resources/web/fang-theorem-a-2026-10-24/``) proves that for every integer
k >= 6 the waste w(k) = k^2 - max{N : s(N) < k} is below 4 sqrt(2k) + 2, so
c*(k) = w(k) - 1 <= ceil(sqrt(32k)). The packing is Sungjoon Ryu's L: a (k - b)^2 grid and
two bands of b rows tilted at t = tan(theta/2) just above 1/b, side S = k - b + W < k, with
both ends of each band filled by axis-parallel rows (lift 0 at one end, the whole free
length F at the other) and b an odd integer with |b - sqrt(2k)| <= 1. Evan Daniel proved
a bound of the same strength first, c*(k) <= 4 ceil(sqrt(2k - 7)) - 1, in Lean.

This module was written from the note's Sections 2 to 5, not from the source's
``lband.py`` or any other program of the source, which it never reads. Everything is
exact, in integers and ``Fraction``; a square root is compared by squaring. Theorem and
lemma numbers are the note's as printed: Theorem A is its Theorem 1, Lemma 2 fills a band
end and Lemma 3 bounds a band (finding N-2 of the review of 25 October 2026). It decides:

- **the bound** (`check_bound`): for every k of a range and every odd b with
  |b - sqrt(2k)| <= 1, a rational t = 1/b + eps that is *close* (conditions (a) to (d) of
  Section 4) and has H(t) < 4 sqrt(2k) + 2, where H(t) is b(k - S) plus the two right sides
  of Lemma 3; then that the construction's count N gives w = k^2 - N < 4 sqrt(2k) + 2,
  that w < H(t) (Lemma 3 with equation (1)), and that the limit B(k) of H(t) as t -> 1/b
  is below 4 sqrt(2k) + 2;
- **the tail** (`check_identities`): what makes B(k) < 4 sqrt(2k) + 2 hold at every k, the
  identity b(b^2 + 1)^2 (kappa_b - 1/b - 1/(b^2 + 1)) = 6b^4 - b^3 - 2b^2 - b and the
  positivity of its right side for b >= 1, Lemma 3's value at t0 = 1/b, and the strict
  closeness at t0 (delta_b in (0, 1) and 2 tau_0 - b c_0 > 0 for odd b >= 3). Each identity
  is between polynomials of bounded degree in b and L, decided at more points than the
  degree; with 4kb/(b^2 + 1) < 4k/b and 4k/b + 2b = 4 sqrt(2k) + (2/b)(b - sqrt(2k))^2, they
  give B(k) < 4 sqrt(2k) + 2 for every k >= 6 (the proof of Theorem A). That some close t
  then has H(t) < 4 sqrt(2k) + 2 is the continuity of H, which `check_bound` exhibits one
  k at a time;
- **the geometry** (`check_geometry`): every square of the packing laid out in exact
  rationals, inside [0, S]^2 with S < k, every two whose bounding boxes overlap separated
  by an exact separating-axis test, and the count equal to N;
- **controls** (`check_controls`): three mutations of each packing refused (a tilted square
  pushed 1/1000 into the next row, a fill square moved 1/1000 past the corner line, and
  one fill square too many); and **sharpness** (`check_sharpness`): w = 4b exactly at
  k = (b^2 - b + 8)/2, less than 16/b below the bound, and the bound with its additive 2
  lowered to 15/8 refused at b = 127;
- **the retained certificates** (`check_certificates`): each of the 36 shipped files is the
  construction at its k, with the smaller b at a tie, its count k^2 - w and its side below
  k, and so an instance of the theorem. Their custody is the packet's
  (`devtools.acquire_source --check`), which binds each to its Git blob at the pin.

``replay`` decides those 36 certificates on this repository's two maintained exact routes,
with the filter and the six controls of `devtools.couzo_678_replay` (route ``sqpack``
through ``sqpack.verify``'s predicates, route ``independent`` through
``devtools.check_rational_witness_independent``'s, over every wall and every pair whose
centres are closer than sqrt 2), and adds the sharp controls of
`devtools.upper_bound_sharp_controls`, which decide all pairs, at the counts of the case
corpus (k <= 18, n <= 302). It writes ``receipts/certificate-replay.json`` in the packet;
``check`` reads it back against the packet. No source program runs.

Run from ``packing/``::

    uv run --frozen --all-extras --group dev python -m cases.asymptotic.fang_theorem_a \\
        construction [--bound 60000] [--geometry 40] [--out PATH]
    uv run --frozen --all-extras --group dev python -m cases.asymptotic.fang_theorem_a \\
        replay [--workers 2]
    uv run --frozen --all-extras --group dev python -m cases.asymptotic.fang_theorem_a check
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import sys
import time
from collections.abc import Callable, Iterable, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict, dataclass
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any

from cases.asymptotic.ryu_k2_minus_c_constants import Check
from sqpack import retained_json

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parent
PACKET = ROOT / "resources/web/fang-theorem-a-2026-10-24"
CERTS = PACKET / "source/theorem-a/certs"
RECEIPTS = PACKET / "receipts"
CONSTRUCTION_RECEIPT = RECEIPTS / "construction.json"
REPLAY_RECEIPT = RECEIPTS / "certificate-replay.json"
SOURCE_COMMIT = "db1ed6220731fce432fa3b1ef3b994b5ab6c3663"
#: The k of the 36 certificates the source ships.
SHIPPED = (*range(6, 41), 101)
#: The certificates whose count is in the case corpus, n <= 324, where the all-pairs sharp
#: controls are affordable (about two minutes at k = 18, n = 302).
SHARP_THROUGH = 18
#: The note's own ranges (Section 6): the bound to 60000, every inequality to 20000.
NOTE_BOUND = 60000
NOTE_INEQUALITIES = 20000
WITNESS_PREFIX = "W-fang-theorem-a-n"
CLAIM_LIMITATIONS = (
    "Complete db1ed62 rational centre/half-angle certificate of Kevin Fang's Theorem A "
    "construction, converted exactly from the retained source. Finite construction "
    "feasibility only: an instance of the theorem at one k, not the theorem, and no exact "
    "form, local minimum, rigidity, novelty, priority or global optimality claim."
)
REPLAY_FORMAT = "fang-theorem-a-certificate-replay-v1"
CONSTRUCTION_FORMAT = "fang-theorem-a-construction-v1"
HEADER = re.compile(r"# k=(\d+) b=(\d+) n=(\d+) waste=(\d+) ")

type Point = tuple[Fraction, Fraction]
type Square = tuple[Point, Point, Point, Point]


# --------------------------------------------------------------------------- the bound


def ceil_sqrt(n: int) -> int:
    """The least integer r >= 0 with r^2 >= n."""
    root = isqrt(n)
    return root if root * root == n else root + 1


def theorem_a(k: int) -> int:
    """The theorem's integer form, c*(k) <= ceil(sqrt(32k)), for every k >= 6."""
    if k < 6:
        raise ValueError(f"Theorem A is stated for k >= 6, not k = {k}")
    return ceil_sqrt(32 * k)


def below_bound(value: Fraction | int, k: int) -> bool:
    """Whether ``value < 4 sqrt(2k) + 2``, decided exactly: value - 2 < sqrt(32k)."""
    excess = Fraction(value) - 2
    return excess < 0 or excess * excess < 32 * k


def floor(value: Fraction) -> int:
    return value.numerator // value.denominator


def odd_widths(k: int) -> tuple[int, ...]:
    """Every odd b >= 1 with |b - sqrt(2k)| <= 1, that is (b - 1)^2 <= 2k <= (b + 1)^2."""
    root = isqrt(2 * k)
    return tuple(
        b
        for b in range(max(1, root - 3), root + 4)
        if b % 2 == 1 and (b - 1) ** 2 <= 2 * k <= (b + 1) ** 2
    )


@dataclass(frozen=True)
class Band:
    """A band of rows of b unit squares tilted at t = tan(theta/2) (Section 2)."""

    b: int
    t: Fraction

    @property
    def c(self) -> Fraction:
        return (1 - self.t * self.t) / (1 + self.t * self.t)

    @property
    def s(self) -> Fraction:
        return 2 * self.t / (1 + self.t * self.t)

    @property
    def tau(self) -> Fraction:
        return self.c / self.s

    @property
    def sec(self) -> Fraction:
        return 1 / self.c

    @property
    def width(self) -> Fraction:
        """W = bc + s."""
        return self.b * self.c + self.s

    @property
    def height(self) -> Fraction:
        """h = bs + c, a row's height."""
        return self.b * self.s + self.c

    @property
    def eta(self) -> Fraction:
        return Fraction(self.b, 2) - self.tau

    def close(self) -> dict[str, bool]:
        """Conditions (a) to (d) of Section 4."""
        b = self.b
        return {
            "a": floor(self.width - self.s - self.tau) == (b - 1) // 2,
            "b": 0 <= self.eta < Fraction(1, 2),
            "c": 2 * self.tau - b * self.c >= 0,
            "d": self.height < 3,
        }

    def corner(self, i: int, lift: Fraction) -> Fraction:
        """a_i(y) = max(0, s + (i + 1 - y) tau): where the corner line reaches height i + 1."""
        return max(Fraction(0), self.s + (i + 1 - lift) * self.tau)

    def levels(self, lift: Fraction) -> tuple[int, ...]:
        """m_i(y) = max(0, floor(W - a_i(y))) for i = 0, 1, ... while it is positive."""
        out: list[int] = []
        while (m := floor(self.width - self.corner(len(out), lift))) > 0:
            out.append(m)
        return tuple(out)

    def rows(self, length: Fraction) -> tuple[int, Fraction]:
        """R(L) = floor((L - h)/sec) + 1 rows and the free length F = L - (R - 1) sec - h."""
        count = floor((length - self.height) / self.sec) + 1
        return count, length - (count - 1) * self.sec - self.height

    def capacity(self, length: Fraction) -> int:
        """C(L) = bR + fill(0) + fill(F) (Section 2, (E3))."""
        count, free = self.rows(length)
        return self.b * count + sum(self.levels(Fraction(0))) + sum(self.levels(free))

    def lemma_three(self, length: Fraction) -> Fraction:
        """The right side of Lemma 3: bL(1 - c) + bch - 2b + 2 - 2(W - s - 2 tau) + 2 eta."""
        b, c = self.b, self.c
        return (
            b * length * (1 - c)
            + b * c * self.height
            - 2 * b
            + 2
            - 2 * (self.width - self.s - 2 * self.tau)
            + 2 * self.eta
        )


def kappa(b: int) -> Fraction:
    """kappa_b = (7b^4 + 1)/(b (b^2 + 1)^2)."""
    return Fraction(7 * b**4 + 1, b * (b * b + 1) ** 2)


def limit(k: int, b: int) -> Fraction:
    """B(k) = 4kb/(b^2 + 1) + 2b + 2 + 2/(b^2 + 1) - 2 kappa_b, the note's limit of H(t)
    as t -> 1/b; `check_bound` holds it to `lemma_bound(k, b, 1/b)` at every (k, b)."""
    d = b * b + 1
    return Fraction(4 * k * b, d) + 2 * b + 2 + Fraction(2, d) - 2 * kappa(b)


def lemma_bound(k: int, b: int, t: Fraction) -> Fraction:
    """H(t): b(k - S) plus the right sides of Lemma 3 for the bands of length S and k - b."""
    band = Band(b, t)
    side = k - b + band.width
    return b * (k - side) + band.lemma_three(side) + band.lemma_three(Fraction(k - b))


@dataclass(frozen=True)
class Construction:
    """The packing at one (k, b, t): its side, count, waste and Lemma 3's bound H(t)."""

    k: int
    b: int
    t: Fraction
    side: Fraction
    count: int
    waste: int
    lemma_bound: Fraction
    close: bool


def construct(k: int, b: int, t: Fraction) -> Construction | None:
    """The construction of Section 3, or None where k - b <= h."""
    band = Band(b, t)
    side = k - b + band.width
    if not k - b > band.height:
        return None
    count = (k - b) ** 2 + band.capacity(side) + band.capacity(Fraction(k - b))
    bound = lemma_bound(k, b, t)
    return Construction(k, b, t, side, count, k * k - count, bound, all(band.close().values()))


def witness(k: int, b: int, tries: int = 60) -> Construction:
    """A close t = 1/b + eps with S < k and H(t) < 4 sqrt(2k) + 2, eps shrunk by tens."""
    eps = Fraction(1, 1000 * k**3)
    for _ in range(tries):
        found = construct(k, b, Fraction(1, b) + eps)
        if (
            found is not None
            and found.close
            and below_bound(found.lemma_bound, k)
            and found.side < k
        ):
            return found
        eps /= 10
    raise ValueError(f"no close t below the bound at k = {k}, b = {b}")


def best(k: int) -> Construction:
    """The construction at the odd width of least waste, the smaller b at a tie."""
    return min((witness(k, b) for b in odd_widths(k)), key=lambda item: (item.waste, item.b))


def check_bound(
    first: int, last: int, inequalities: int = NOTE_INEQUALITIES
) -> tuple[Check, ...]:
    """The theorem's bound, Lemma 3 and B(k) for every k in [first, last] and every b."""
    bound: list[tuple[int, int, int]] = []
    lemma: list[tuple[int, int]] = []
    limits: list[tuple[int, int]] = []
    unequal: list[tuple[int, int]] = []
    least: tuple[Fraction, int, int] | None = None
    least_note: tuple[Fraction, int, int] | None = None
    ties: list[int] = []
    pairs = 0
    for k in range(first, last + 1):
        widths = odd_widths(k)
        if len(widths) > 1:
            ties.append(k)
        for b in widths:
            pairs += 1
            found = witness(k, b)
            if not below_bound(found.waste, k):
                bound.append((k, b, found.waste))
            if not found.waste < found.lemma_bound:
                lemma.append((k, b))
            ceiling = limit(k, b)
            if ceiling != lemma_bound(k, b, Fraction(1, b)):
                unequal.append((k, b))
            if not below_bound(ceiling, k):
                limits.append((k, b))
            slack = (ceiling - found.waste, k, b)
            least = slack if least is None or slack < least else least
            if k <= inequalities:
                least_note = slack if least_note is None or slack < least_note else least_note
    span = f"{first} <= k <= {last}"
    return (
        Check(
            f"w(k) < 4 sqrt(2k) + 2 at every odd b with |b - sqrt(2k)| <= 1, {span}",
            "Theorem A",
            not bound,
            f"{pairs} (k, b) decided, failures {bound[:5] or 'none'}; "
            f"two widths at {len(ties)} k",
        ),
        Check(
            f"w < H(t) at a close t, {span}",
            "Lemma 3 and equation (1)",
            not lemma,
            f"failures {lemma[:5] or 'none'}",
        ),
        Check(
            f"B(k) = H(1/b), the value of Lemma 3's bound at t0, {span}",
            "proof of Theorem A",
            not unequal,
            f"failures {unequal[:5] or 'none'}",
        ),
        Check(
            f"B(k) < 4 sqrt(2k) + 2, {span}",
            "proof of Theorem A",
            not limits,
            f"failures {limits[:5] or 'none'}",
        ),
        Check(
            f"least B(k) - w for k <= {min(last, inequalities)}",
            "Section 6",
            least_note is not None and least_note[0] > 0,
            "none" if least_note is None else f"{least_note[0]} at k = {least_note[1]}",
        ),
        Check(
            f"least B(k) - w, {span}",
            "Section 6",
            least is not None and least[0] > 0,
            "none" if least is None else f"{least[0]} at k = {least[1]}, b = {least[2]}",
        ),
    )


# --------------------------------------------------------------------------- the tail


def identity_sides(b: int) -> tuple[Fraction, int]:
    """Both sides of b (b^2 + 1)^2 (kappa_b - 1/b - 1/(b^2 + 1)) = 6b^4 - b^3 - 2b^2 - b."""
    d = b * b + 1
    left = b * d * d * (kappa(b) - Fraction(1, b) - Fraction(1, d))
    return left, 6 * b**4 - b**3 - 2 * b * b - b


def lemma_three_at_t0(b: int, length: Fraction) -> tuple[Fraction, Fraction]:
    """Lemma 3's right side at t0 = 1/b, and the closed form 2bL/(b^2+1) + b + 2 - kappa_b."""
    return Band(b, Fraction(1, b)).lemma_three(length), (
        Fraction(2 * b, b * b + 1) * length + b + 2 - kappa(b)
    )


def check_identities(widths: Iterable[int] = range(3, 41, 2)) -> tuple[Check, ...]:
    """The algebra that carries B(k) < 4 sqrt(2k) + 2 to every k (see the docstring).

    Each identity, multiplied out by b (b^2 + 1)^2, is between polynomials in b of degree at
    most 6 (and linear in L), so agreement at more than seven values of b (and two of L)
    decides it for every b; ``widths`` must hold at least eight.
    """
    chosen = tuple(widths)
    identity = [b for b in chosen if identity_sides(b)[0] != identity_sides(b)[1]]
    values = [
        (b, length)
        for b in chosen
        for length in (Fraction(0), Fraction(7, 3))
        if lemma_three_at_t0(b, length)[0] != lemma_three_at_t0(b, length)[1]
    ]
    strict: list[int] = []
    for b in chosen:
        band = Band(b, Fraction(1, b))
        delta = band.width - band.s - band.tau - Fraction(b - 1, 2)
        expected = Fraction(1, 2) + Fraction(1, 2 * b) - Fraction(2 * b, b * b + 1)
        if not (
            delta == expected
            and 0 < delta < 1
            and band.width == b
            and band.eta == Fraction(1, 2 * b)
            and 2 * band.tau - b * band.c == Fraction(b * b - 1, b * (b * b + 1))
            and band.height < 3
            and b**3 - 3 * b * b + b + 1 > 0
        ):
            strict.append(b)
    return (
        Check(
            "b(b^2+1)^2 (kappa_b - 1/b - 1/(b^2+1)) = 6b^4 - b^3 - 2b^2 - b, at "
            f"{len(chosen)} odd b",
            "proof of Theorem A",
            len(chosen) >= 8 and not identity,
            f"failures {identity or 'none'}",
        ),
        Check(
            "6b^4 - b^3 - 2b^2 - b > 0 for every b >= 1: it is at least 6b^4 - 4b^4",
            "proof of Theorem A",
            all(6 * b**4 - b**3 - 2 * b * b - b >= 2 * b**4 > 0 for b in (1, *chosen)),
            "b^3 + 2b^2 + b <= 4b^4 for b >= 1",
        ),
        Check(
            "Lemma 3's right side at t0 is 2bL/(b^2+1) + b + 2 - kappa_b",
            "Lemma 3",
            len(chosen) >= 8 and not values,
            f"failures {values or 'none'}",
        ),
        Check(
            "(a)-(d) hold strictly at t0: delta_b in (0, 1), eta_0 = 1/(2b), "
            "2 tau_0 - b c_0 = (b^2-1)/(b(b^2+1)), h_0 < 3",
            "Section 4",
            not strict,
            f"failures {strict or 'none'}; b^3 - 3b^2 + b + 1 > 0 for b >= 3",
        ),
    )


# --------------------------------------------------------------------------- the geometry


def _axis(x: Fraction, y: Fraction) -> Square:
    return ((x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1))


@dataclass(frozen=True)
class Packing:
    """Every square of the construction at (k, b, t), with the indices the controls use."""

    k: int
    b: int
    t: Fraction
    side: Fraction
    squares: tuple[Square, ...]
    count: int
    first_tilted: int
    first_fill: int


def band_squares(band: Band, length: Fraction) -> tuple[list[Square], int]:
    """A band's squares in band coordinates (X across, Y along) and its row count."""
    c, s, sec, width = band.c, band.s, band.sec, band.width
    count, free = band.rows(length)
    squares: list[Square] = []
    for j in range(count):
        lift = j * sec
        for q in range(band.b):
            corners = [
                (s + u * c - v * s, lift + u * s + v * c)
                for u, v in ((q, 0), (q + 1, 0), (q + 1, 1), (q, 1))
            ]
            squares.append((corners[0], corners[1], corners[2], corners[3]))
    for i, m in enumerate(band.levels(Fraction(0))):
        squares.extend(_axis(width - m + q, Fraction(i)) for q in range(m))
    for i, m in enumerate(band.levels(free)):
        # The square [x0, x0 + 1] x [i, i + 1] turned by pi about (W/2, L/2).
        squares.extend(_axis(Fraction(m - q - 1), length - i - 1) for q in range(m))
    return squares, count


def build(k: int, b: int, t: Fraction) -> Packing:
    """The grid and the two filled bands of Section 3, laid out exactly."""
    band = Band(b, t)
    side = k - b + band.width
    squares: list[Square] = [
        _axis(Fraction(i), Fraction(j)) for i in range(k - b) for j in range(k - b)
    ]
    first_tilted = len(squares)
    right, count = band_squares(band, side)
    squares.extend(
        (
            (k - b + p[0][0], p[0][1]),
            (k - b + p[1][0], p[1][1]),
            (k - b + p[2][0], p[2][1]),
            (k - b + p[3][0], p[3][1]),
        )
        for p in right
    )
    top, _ = band_squares(band, Fraction(k - b))
    squares.extend(
        (
            (p[0][1], k - b + p[0][0]),
            (p[1][1], k - b + p[1][0]),
            (p[2][1], k - b + p[2][0]),
            (p[3][1], k - b + p[3][0]),
        )
        for p in top
    )
    found = construct(k, b, t)
    return Packing(
        k=k,
        b=b,
        t=t,
        side=side,
        squares=tuple(squares),
        count=-1 if found is None else found.count,
        first_tilted=first_tilted,
        first_fill=first_tilted + count * b,
    )


def separated(first: Square, second: Square) -> bool:
    """Whether two convex quadrilaterals have disjoint interiors, by their edge normals."""
    for polygon in (first, second):
        for index in range(4):
            (x1, y1), (x2, y2) = polygon[index], polygon[(index + 1) % 4]
            nx, ny = y1 - y2, x2 - x1
            a = [nx * x + ny * y for x, y in first]
            b = [nx * x + ny * y for x, y in second]
            if max(a) <= min(b) or max(b) <= min(a):
                return True
    return False


def overlaps(squares: Sequence[Square], stop: int | None = None) -> list[tuple[int, int]]:
    """Every pair whose bounding boxes overlap and whose interiors meet, by a sweep in x."""
    boxes = sorted(
        (
            min(x for x, _ in sq),
            max(x for x, _ in sq),
            min(y for _, y in sq),
            max(y for _, y in sq),
            index,
        )
        for index, sq in enumerate(squares)
    )
    found: list[tuple[int, int]] = []
    active: list[tuple[Fraction, Fraction, Fraction, Fraction, int]] = []
    for box in boxes:
        active = [other for other in active if other[1] > box[0]]
        for other in active:
            if (
                other[3] > box[2]
                and box[3] > other[2]
                and not separated(squares[other[4]], squares[box[4]])
            ):
                found.append((min(other[4], box[4]), max(other[4], box[4])))
                if stop is not None and len(found) >= stop:
                    return found
        active.append(box)
    return found


def defects(packing: Packing) -> list[str]:
    """Everything that keeps the packing from being its count of squares below side k."""
    found: list[str] = []
    if not packing.side < packing.k:
        found.append("S >= k")
    if len(packing.squares) != packing.count:
        found.append(f"{len(packing.squares)} squares, the formula gives {packing.count}")
    if any(not 0 <= c <= packing.side for sq in packing.squares for p in sq for c in p):
        found.append("a vertex outside [0, S]^2")
    found.extend(f"squares {i} and {j} overlap" for i, j in overlaps(packing.squares, 1))
    return found


def shifted(square: Square, dx: Fraction, dy: Fraction) -> Square:
    a, b, c, d = ((x + dx, y + dy) for x, y in square)
    return (a, b, c, d)


def mutants(packing: Packing) -> dict[str, tuple[Square, ...]]:
    """The three controls: each must be refused."""
    band = Band(packing.b, packing.t)
    step = Fraction(1, 1000)
    squares = list(packing.squares)
    tilted = squares[packing.first_tilted]
    pushed = shifted(tilted, -step * band.s, step * band.c)
    fill = squares[packing.first_fill]
    left = min(x for x, _ in fill)
    target = packing.k - packing.b + band.corner(0, Fraction(0)) - step
    moved = shifted(fill, target - left, Fraction(0))
    extra = _axis(left - 1, Fraction(0))
    return {
        "tilted-square-pushed-into-next-row": (
            *squares[: packing.first_tilted],
            pushed,
            *squares[packing.first_tilted + 1 :],
        ),
        "fill-square-past-corner-line": (
            *squares[: packing.first_fill],
            moved,
            *squares[packing.first_fill + 1 :],
        ),
        "one-fill-square-too-many": (*squares, extra),
    }


def check_geometry(ks: Iterable[int]) -> tuple[Check, ...]:
    """Lay out and decide the packing at every k given, at each of its odd widths."""
    failures: list[str] = []
    built = 0
    for k in ks:
        for b in odd_widths(k):
            built += 1
            failures += [
                f"(k, b) = ({k}, {b}): {d}" for d in defects(build(k, b, witness(k, b).t))
            ]
    return (
        Check(
            "every square inside [0, S]^2, S < k, no two interiors meeting, count = N",
            "Sections 2 and 3",
            built > 0 and not failures,
            f"{built} packings laid out exactly; failures {failures[:5] or 'none'}",
        ),
    )


def check_controls(ks: Iterable[int]) -> tuple[Check, ...]:
    """Each of the three mutations refused at every k given, at its first odd width."""
    accepted: list[str] = []
    decided = 0
    for k in ks:
        b = odd_widths(k)[0]
        packing = build(k, b, witness(k, b).t)
        for name, squares in mutants(packing).items():
            decided += 1
            if not overlaps(squares, 1):
                accepted.append(f"k = {k}: {name}")
    return (
        Check(
            "three mutated packings refused",
            "controls",
            decided > 0 and not accepted,
            f"{decided} mutants decided; accepted {accepted[:5] or 'none'}",
        ),
    )


def sharp_k(b: int) -> int:
    """k = (b^2 - b + 8)/2, where the construction's waste is exactly 4b (the Remark)."""
    return (b * b - b + 8) // 2


#: An odd b with 31/(2b) < 1/8, where the bound with 15/8 for its additive 2 fails.
SHARP_CONTROL = 127


def check_sharpness(
    widths: Iterable[int] = (*range(5, 52, 2), SHARP_CONTROL),
) -> tuple[Check, ...]:
    """The Remark at each odd b given, the gap below the bound, and a weaker constant refused.

    At k = (b^2 - b + 8)/2, 4 sqrt(2k) + 2 - 4b < 16/b, since 16(b^2 - b + 8) <
    (4b - 2 + 16/b)^2 is 4(b - 8)^2/b^2 > 0; so no additive constant below 2 holds for this
    construction at every k, and 15/8 already fails at b = `SHARP_CONTROL`.
    """
    wrong: list[tuple[int, int]] = []
    wide: list[int] = []
    chosen = tuple(widths)
    for b in chosen:
        k = sharp_k(b)
        found = witness(k, b)
        if odd_widths(k) != (b,) or found.waste != 4 * b:
            wrong.append((k, found.waste))
        # 4 sqrt(2k) + 2 - w < 16/b  <=>  32k < (w - 2 + 16/b)^2, with w - 2 + 16/b > 0.
        if not Fraction(32 * k) < (found.waste - 2 + Fraction(16, b)) ** 2:
            wide.append(b)
    k = sharp_k(SHARP_CONTROL)
    excess = Fraction(witness(k, SHARP_CONTROL).waste) - Fraction(15, 8)
    weaker_fails = excess >= 0 and excess * excess >= 32 * k
    return (
        Check(
            f"w = 4b at k = (b^2 - b + 8)/2 for {len(chosen)} odd b from {chosen[0]}",
            "Remark (sharpness)",
            bool(chosen) and not wrong,
            f"failures {wrong or 'none'}",
        ),
        Check(
            "4 sqrt(2k) + 2 - w < 16/b at each such k",
            "Remark (sharpness)",
            bool(chosen) and not wide,
            f"failures {wide or 'none'}",
        ),
        Check(
            f"w < 4 sqrt(2k) + 15/8 fails at k = {k}, b = {SHARP_CONTROL}",
            "Remark (sharpness), as a control",
            weaker_fails,
            f"w = {4 * SHARP_CONTROL}",
        ),
    )


# --------------------------------------------------------------------------- certificates


@dataclass(frozen=True)
class Header:
    """A shipped certificate's comment line and count line, read as data."""

    k: int
    b: int
    n: int
    waste: int
    side: Fraction


def certificate_path(k: int) -> Path:
    return CERTS / f"k{k:03d}.cert"


def header(raw: bytes) -> Header:
    """The header of one retained certificate: ``# k=.. b=.. n=.. waste=..``, then ``n S``."""
    lines = raw.decode("utf-8").splitlines()
    found = HEADER.match(lines[0])
    if found is None:
        raise ValueError("a certificate opens with its # k= b= n= waste= comment")
    k, b, n, waste = (int(group) for group in found.groups())
    count, side = lines[1].split()
    if int(count) != n:
        raise ValueError(f"k = {k}: the count line states {count}, the comment {n}")
    return Header(k, b, n, waste, Fraction(side))


def check_certificates(ks: Iterable[int] = SHIPPED) -> tuple[Check, ...]:
    """Each retained certificate is this construction at its k, below side k."""
    wrong: list[str] = []
    checked = 0
    for k in ks:
        raw = certificate_path(k).read_bytes()
        stated = header(raw)
        found = best(k)
        checked += 1
        if (stated.k, stated.b, stated.waste) != (k, found.b, found.waste):
            wrong.append(
                f"k = {k}: header {stated}, construction b = {found.b}, w = {found.waste}"
            )
        if stated.n != k * k - stated.waste or not stated.side < k:
            wrong.append(f"k = {k}: count or side")
        if not stated.waste - 1 <= theorem_a(k):
            wrong.append(f"k = {k}: not an instance of Theorem A")
    return (
        Check(
            "each shipped certificate is the construction at its k (the smaller b at a tie), "
            "k^2 - w squares below side k",
            "Section 6, certs/",
            checked > 0 and not wrong,
            f"{checked} certificates; failures {wrong[:5] or 'none'}",
        ),
    )


# --------------------------------------------------------------------------- comparisons

#: The note's comparison range with Daniel's bound (Section 7), and the end of the window
#: in which Theorem A's strictly-least count is taken: below it Daniel's unregistered
#: k^{2/5} bound is not smaller at any k (`daniel_k25_crossover`, which decides each k).
COMPARE_LIMIT = 10**6
LEAST_WINDOW = (42, 702_000)
#: Where Daniel's unregistered c*(k) < 18.9 k^{2/5} + 35.7 k^{1/5} + 122 starts to hold.
DANIEL_K25_FROM = 3 * 10**5
#: Ryu's Theorem 1.6 values the register's k^{2/5} row records, by k.
RYU_THEOREM_1_6 = {10**5: 1583, 10**6: 3972, 10**7: 10039, 38_250_000: 16988, 10**8: 24790}


def daniel_tail_holds(k: int) -> bool:
    """Whether sqrt(2k) + sqrt(2k - 7) >= 28, decided exactly.

    With x = sqrt(2k), y = sqrt(2k - 7) and delta = x - y = 7/(x + y), Theorem A's
    ceil(sqrt(32k)) lies in [4x, 4x + 1) and Daniel's 4 ceil(y) - 1 in [4y - 1, 4y + 3), so
    their difference lies in (4 delta - 3, 4 delta + 2). Once x + y >= 28, 4 delta <= 1 and
    the integers differ by at most 2; x + y grows with k, so this at k decides every larger
    k. (x + y)^2 = 4k - 7 + 2 sqrt(2k(2k - 7)), compared with 28^2 by squaring.
    """
    rest = 28 * 28 - (4 * k - 7)
    return rest <= 0 or 4 * (2 * k) * (2 * k - 7) >= rest * rest


def runs(values: Iterable[int]) -> list[list[int]]:
    out: list[list[int]] = []
    for value in values:
        if out and out[-1][1] == value - 1:
            out[-1][1] = value
        else:
            out.append([value, value])
    return out


def classify(
    mine: Callable[[int], int], other: Callable[[int], int], first: int, last: int
) -> dict[str, list[list[int]]]:
    """Where ``mine(k)`` is smaller than, equal to or larger than ``other(k)``, as runs."""
    groups: dict[str, list[int]] = {"smaller": [], "tied": [], "larger": []}
    for k in range(first, last + 1):
        a, b = mine(k), other(k)
        groups["smaller" if a < b else "tied" if a == b else "larger"].append(k)
    return {key: runs(value) for key, value in groups.items()}


def _iroot_ceil(n: int, exponent: int) -> int:
    """The least m >= 0 with m^exponent >= n."""
    low, high = 0, 1
    while high**exponent < n:
        high *= 2
    while low < high:
        middle = (low + high) // 2
        if middle**exponent >= n:
            high = middle
        else:
            low = middle + 1
    return low


def _fifth_root_floor(n: int) -> int:
    """The greatest p >= 0 with p^5 <= n: a binary64 estimate, then corrected exactly."""
    p = int(n**0.2) if n < 10**300 else _iroot_ceil(n, 5)
    while p > 0 and p**5 > n:
        p -= 1
    while (p + 1) ** 5 <= n:
        p += 1
    return p


def daniel_k25_at_most(k: int, value: int) -> bool:
    """Whether D(k) = 18.9 u^2 + 35.7 u + 122, u = k^{1/5}, is at most ``value``, exactly.

    With u in [p/q, (p + 1)/q), p the integer fifth root of q^5 k, the sign of
    10 q^2 (D - value) = 189 p^2 + 357 pq + (1220 - 10 value) q^2, which increases with p,
    decides it once the bracket's two ends agree; q doubles until they do. It always ends:
    unless k is a fifth power, when u = p/q exactly, u has degree 5 over the rationals and
    is no root of the quadratic D(u) = value."""
    q = 1024
    while True:
        target = q**5 * k
        p = _fifth_root_floor(target)
        constant = (1220 - 10 * value) * q * q
        if 189 * p * p + 357 * p * q + constant > 0:
            return False
        if p**5 == target:
            return True
        if 189 * (p + 1) ** 2 + 357 * (p + 1) * q + constant <= 0:
            return True
        q *= 2


def daniel_k25_tail_holds(k: int) -> bool:
    """Whether Daniel's k^{2/5} bound stays smaller than ceil(sqrt(32k)) at every k' >= k.

    g(k) = sqrt(32k) - D(k) has g'(k) k^{4/5} = 2 sqrt 2 v^3 - 7.56 v^2 - 7.14 with
    v = k^{1/10}. From 3*10^5, v >= 7/2 (3.5^10 < 3*10^5); with 2 sqrt 2 > 2.828, the right
    side is positive at 7/2 and increasing beyond it, since 3 (2.828)(7/2) > 15.12. So g
    increases from 3*10^5, and D(k) <= isqrt(32k) <= sqrt(32k) at one such k holds at every
    larger one, where then ceil(D) - 1 < ceil(sqrt(32k))."""
    v0, a = Fraction(7, 2), Fraction(2828, 1000)
    rising = (
        v0**10 <= DANIEL_K25_FROM
        and a * a < 8
        and a * v0**3 - Fraction(756, 100) * v0**2 - Fraction(714, 100) > 0
        and 3 * a * v0 > Fraction(1512, 100)
    )
    return rising and k >= DANIEL_K25_FROM and daniel_k25_at_most(k, isqrt(32 * k))


def daniel_k25_crossover(last: int = COMPARE_LIMIT - 1) -> dict[str, Any]:
    """Where Daniel's unregistered c*(k) < 18.9 k^{2/5} + 35.7 k^{1/5} + 122 (k >= 3*10^5),
    read as the integer bound ceil(D(k)) - 1, is smaller than Theorem A's ceil(sqrt(32k)):
    exactly when D(k) <= ceil(sqrt(32k)). Decided at every k from 3*10^5 to ``last``
    (`daniel_k25_at_most`), and beyond ``last`` by `daniel_k25_tail_holds`."""
    first, last_not, count = None, None, 0
    for k in range(DANIEL_K25_FROM, last + 1):
        if daniel_k25_at_most(k, theorem_a(k)):
            count += 1
            first = k if first is None else first
        else:
            last_not = k
    return {
        "k_range": [DANIEL_K25_FROM, last],
        "smaller_at": count,
        "first_k_where_smaller": first,
        "last_k_where_not_smaller": last_not,
        "smaller_at_every_k_from": None if last_not is None else last_not + 1,
        "tail_from_next_k_holds": daniel_k25_tail_holds(last + 1),
    }


def comparisons(
    limit: int = COMPARE_LIMIT, window: tuple[int, int] = LEAST_WINDOW
) -> dict[str, Any]:
    """Theorem A's and Daniel's integer bounds against each other and the family, exactly.

    Each comparison is decided one k at a time to its stated end, and beyond it by the tail
    lemma named beside it, each decided here in integers.
    """
    # Imported here: the family module imports this one for Theorem A's value.
    from cases.asymptotic import deficiency_family as family  # noqa: PLC0415
    from cases.asymptotic import fang_excess_inventory as fang  # noqa: PLC0415

    daniel = family.daniel_layers

    ryu_1_3 = {k: family.ryu_theorem_1_3(k) for k in range(6, 601)}.__getitem__
    counts = {"A_smaller": 0, "tied": 0, "daniel_smaller": 0}
    close_below = []
    widest = 0
    for k in range(7, limit):
        a, d = theorem_a(k), daniel(k)
        counts["A_smaller" if a < d else "tied" if a == d else "daniel_smaller"] += 1
        if k < 89 and d <= a - 3:
            close_below.append([k, a - d])
        if k >= 89:
            widest = max(widest, abs(a - d))
    first, last = window
    strictly = sum(
        1
        for k in range(first, last + 1)
        if theorem_a(k) < daniel(k) and theorem_a(k) < RYU_THEOREM_1_6.get(k, theorem_a(k) + 1)
    )
    below_daniel = sum(1 for k in range(first, last + 1) if theorem_a(k) < daniel(k))
    # From k = 100 the two bounds differ by at most 2 (`daniel_tail_holds`).
    tail_100 = daniel_tail_holds(100)
    # Ryu's Theorem 1.2 for k >= 1.6*10^7, c*(k) < 20.668 k^{2/5} + 0.623: sufficient is
    # sqrt(32k) >= 20.668 m + 1.623 with m = ceil(k^{2/5}); sqrt(32k) - 20.668 k^{2/5} grows
    # for k > 4.5*10^4, so it then holds at every larger k.
    k0 = 16 * 10**6
    m = _iroot_ceil(k0 * k0, 5)
    # The three tails. Ryu's Theorem 1.4: 8 ceil(sqrt(k - 4)) - 1 > A(k) once
    # 64(k - 4) >= (sqrt(32k) + 2)^2, that is (32k - 260)^2 >= 512k, increasing from k = 9.
    # Ryu's Theorem 1.3: by his Proposition 1.5 (decided to k = 2000 by ryu_upper_l_packing)
    # it exceeds 8 sqrt(k) - 15, above A(k) once 8 sqrt(k) > A(k) + 15, which holds from
    # 47 since (8 - 4 sqrt 2) sqrt(k) > 16 there. T-163: k - 1 - F(k) >= (19k - 12)/21 >
    # A(k) once (19k - 33)^2 >= 14112k, increasing from k = 22.
    return {
        "range": [7, limit - 1],
        "A_vs_daniel": {
            **counts,
            "k_below_89_daniel_smaller_by_3_or_more": close_below,
            "largest_difference_from_89": widest,
            "tail_from_100_differs_by_at_most_2": tail_100,
        },
        "A_strictly_least_in_window": {
            "window": list(window),
            "below_daniel": below_daniel,
            "strictly_least": strictly,
            "note": "Ryu's Theorem 1.3 at its best b is larger from k = 14 and T-163 from 42; "
            "Ryu's Theorem 1.6 value 1583 at k = 10^5 is the one other statement below it",
        },
        "A_vs_ryu_theorem_1_4": classify(theorem_a, fang.ryu, 6, limit - 1),
        "A_vs_ryu_theorem_1_4_tail_from_16": 32 * 16 - 260 > 0
        and (32 * 16 - 260) ** 2 >= 16 * 32 * 16,
        "A_vs_ryu_theorem_1_3": classify(theorem_a, ryu_1_3, 6, 600),
        "A_vs_ryu_theorem_1_3_tail_from_47": all(
            64 * k > (ceil_sqrt(32 * k) + 15) ** 2 for k in range(47, 2001)
        ),
        "A_vs_t163": classify(theorem_a, fang.theorem_two, 15, 5000),
        "A_vs_t163_tail_from_43": (19 * 43 - 33) ** 2 >= 441 * 32 * 43,
        "daniel_vs_ryu_theorem_1_4": classify(daniel, fang.ryu, 7, limit - 1),
        "daniel_vs_ryu_theorem_1_3": classify(daniel, ryu_1_3, 7, 600),
        "daniel_vs_t163": classify(daniel, fang.theorem_two, 15, 5000),
        # Daniel's bound is below sqrt(32k) + 3. Ryu's Theorem 1.4 exceeds that once
        # 8 sqrt(k - 4) - 1 > sqrt(32k) + 3, that is 32k > 272 and (32k - 272)^2 > 2048k, which
        # holds from k = 14 and grows; his Theorem 1.3 once 8 sqrt(k) - 15 >= daniel(k), which
        # holds from 59 and grows; T-163 once 19k > 75 and (19k - 75)^2 > 14112k, from 47.
        "daniel_tails": {
            "ryu_theorem_1_4_from_14": 32 * 14 > 272 and (32 * 14 - 272) ** 2 > 2048 * 14,
            "ryu_theorem_1_3_from_59": all(
                64 * k > (daniel(k) + 15) ** 2 for k in range(59, 2001)
            ),
            "t163_from_47": 19 * 47 > 75 and (19 * 47 - 75) ** 2 > 14112 * 47,
        },
        "ryu_theorem_1_2_at_1.6e7": {
            "A": theorem_a(k0),
            "ryu_at_most": str(Fraction(20668 * m + 623, 1000)),
            "ryu_smaller": 1000 * isqrt(32 * k0) >= 20668 * m + 1623,
        },
        "ryu_theorem_1_6": {
            str(k): {"ryu": value, "A": theorem_a(k), "daniel": daniel(k)}
            for k, value in RYU_THEOREM_1_6.items()
        },
        "daniel_k25_crossover": daniel_k25_crossover(limit - 1),
        "case_records": case_records(),
    }


def _print_ceiling(printed: str) -> Fraction:
    """A case's printed upper bound plus one unit in its last place: above the value it
    prints however it was rounded, so a side below k there is below k. An integer print
    is the exact value, as a grid's side is."""
    whole, point, places = printed.partition(".")
    if not point:
        return Fraction(int(whole))
    return Fraction(printed) + Fraction(1, 10 ** len(places))


def case_records(
    statements: Sequence[tuple[str, Callable[[int], int], int]] = (),
) -> dict[str, Any]:
    """Whether a statement would move a case: every n <= 324 it bounds below k, against
    the case record's reported and verified upper bounds, each read as a ceiling: its
    printed decimal plus one unit in the last place (`_print_ceiling`), never as s(n).

    A statement c*(k) <= v(k) gives s(n) < k for n <= k^2 - v(k) - 1. For each count of the
    corpus the least such k is found, and the case's two upper bounds must already lie
    below it; a count no k reaches is not bounded by the statement at all.
    """
    # Imported here: the case parser reads the frontier, which the checks above do not,
    # and the family module imports this one for Theorem A's value.
    from cases.asymptotic.deficiency_family import daniel_layers as daniel  # noqa: PLC0415
    from devtools import check_source_coverage as coverage  # noqa: PLC0415

    chosen = statements or (("theorem_a", theorem_a, 6), ("daniel", daniel, 7))
    cases = {n: coverage.parse_case(ROOT / f"frontier/n-{n:03d}.md") for n in range(1, 325)}
    out: dict[str, Any] = {}
    for name, value, least in chosen:
        reached = 0
        moved: list[int] = []
        for n, case in cases.items():
            k = next((k for k in range(least, 40) if n <= k * k - value(k) - 1), None)
            if k is None:
                continue
            reached += 1
            if any(
                not _print_ceiling(str(case[lane]["value"])) < k
                for lane in ("reported_upper_bound", "verified_upper_bound")
            ):
                moved.append(n)
        out[name] = {"counts_reached": reached, "case_bound_not_below_k": sorted(set(moved))}
    return out


# --------------------------------------------------------------------------- the report


def construction_report(bound: int, geometry: int) -> dict[str, Any]:
    """Every check above, at the note's bound range and the geometry to ``geometry``."""
    started = time.process_time()
    checks = (
        *check_bound(6, bound),
        *check_identities(),
        *check_geometry([*range(6, geometry + 1), 101]),
        *check_controls(range(6, min(geometry, 30) + 1)),
        *check_sharpness(),
        *check_certificates(),
    )
    return {
        "format": CONSTRUCTION_FORMAT,
        "module": "packing/cases/asymptotic/fang_theorem_a.py",
        "source": (
            f"TheSnakeFang/squarepack-certs {SOURCE_COMMIT}, theorem-a/note/main.tex (v0.2)"
        ),
        "bound_through": bound,
        "geometry_through": geometry,
        "passed": all(check.holds for check in checks),
        "checks": [asdict(check) for check in checks],
        "table": [
            {"k": k, "b": item.b, "waste": item.waste, "theorem_a": theorem_a(k)}
            for k in (*range(6, 41), 100, 101, 300, 600)
            for item in (best(k),)
        ],
        "python": platform.python_version(),
        "cpu_seconds": round(time.process_time() - started, 1),
    }


# --------------------------------------------------------------------------- the replay


def replay_row(k: int) -> dict[str, Any]:
    """One shipped certificate on both maintained routes, its controls, and sharp controls."""
    # Imported here: the routes pull in the devtools kernel, which the construction
    # checks above do not need.
    from devtools import couzo_678_replay as routes  # noqa: PLC0415
    from devtools import upper_bound_reports as reports  # noqa: PLC0415
    from devtools import upper_bound_sharp_controls as sharp  # noqa: PLC0415

    raw = certificate_path(k).read_bytes()
    stated = header(raw)
    certificate = reports.parse_certificate(raw, stated.n, "evand-cert")
    started = time.process_time()
    decision = routes.decide(routes.geometry(certificate))
    controls = routes.decide_controls(certificate)
    row: dict[str, Any] = {
        "k": k,
        "b": stated.b,
        "n": stated.n,
        "waste": stated.waste,
        "certificate": certificate_path(k).relative_to(REPO).as_posix(),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "exact_side": str(certificate.side),
        "side_below_k": certificate.side < k,
        "instance_of_theorem_a": stated.waste - 1 <= theorem_a(k),
        "decision": decision,
        "controls": controls,
        "controls_refused": all(
            item["refused_by_sqpack"] and item["refused_by_independent"] for item in controls
        ),
    }
    if k <= SHARP_THROUGH:
        profile = {"witness_prefix": WITNESS_PREFIX, "claim_limitations": CLAIM_LIMITATIONS}
        rows = sharp.control_rows(certificate, profile)
        row["sharp_controls"] = rows
        row["sharp_controls_as_expected"] = all(item["as_expected"] for item in rows)
    row["cpu_seconds"] = round(time.process_time() - started, 1)
    return row


def replay(workers: int = 2) -> dict[str, Any]:
    """Every shipped certificate, after the packet's custody check, two at a time at most."""
    from devtools import acquire_source  # noqa: PLC0415

    if problems := acquire_source.check(PACKET, REPO):
        raise ValueError("packet custody: " + "; ".join(problems))
    if not 1 <= workers <= 2:
        raise ValueError("at most two workers on the shared host")
    started = time.monotonic()
    # The largest first, so the two workers finish together.
    order = sorted(SHIPPED, key=lambda k: -k)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        rows = dict(zip(order, pool.map(replay_row, order), strict=True))
    ordered = [rows[k] for k in SHIPPED]
    return {
        "format": REPLAY_FORMAT,
        "packet": PACKET.name,
        "source_commit": SOURCE_COMMIT,
        "routes": ["sqpack", "independent"],
        "filter": "pairs whose centres are closer than sqrt 2, by exact comparison "
        "(devtools.couzo_678_replay.candidate_pairs)",
        "sharp_controls_through_k": SHARP_THROUGH,
        "rows": ordered,
        "summary": summary(ordered),
        "python": platform.python_version(),
        "wall_seconds": round(time.monotonic() - started, 1),
    }


def summary(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """What the receipt shows, in the counts a reader checks first."""
    sharp = [row for row in rows if "sharp_controls" in row]
    return {
        "certificates": len(rows),
        "accepted_by_both_routes": sum(row["decision"]["passed"] for row in rows),
        "instances_of_theorem_a": sum(
            row["instance_of_theorem_a"] and row["side_below_k"] for row in rows
        ),
        "controls": sum(len(row["controls"]) for row in rows),
        "controls_refused_by_both": sum(
            item["refused_by_sqpack"] and item["refused_by_independent"]
            for row in rows
            for item in row["controls"]
        ),
        "sharp_control_certificates": len(sharp),
        "sharp_controls": sum(len(row["sharp_controls"]) for row in sharp),
        "sharp_controls_as_expected": sum(
            item["as_expected"] for row in sharp for item in row["sharp_controls"]
        ),
        "candidate_pairs": sum(row["decision"]["candidate_pairs"] for row in rows),
        "cpu_seconds": round(sum(row["cpu_seconds"] for row in rows), 1),
    }


def _untimed(value: Any) -> Any:
    """A receipt row without its measured times, which a second run does not reproduce."""
    if isinstance(value, dict):
        return {
            key: _untimed(item)
            for key, item in value.items()
            if key not in {"cpu_seconds", "wall_seconds"}
        }
    if isinstance(value, list):
        return [_untimed(item) for item in value]
    return value


def check_replay(replayed: Iterable[int] = ()) -> list[str]:
    """The retained receipt against the packet; each k of ``replayed`` decided again."""
    from devtools import acquire_source  # noqa: PLC0415

    problems = list(acquire_source.check(PACKET, REPO))
    receipt = json.loads(REPLAY_RECEIPT.read_text(encoding="utf-8"))
    rows = {row["k"]: row for row in receipt["rows"]}
    if receipt.get("format") != REPLAY_FORMAT or list(rows) != list(SHIPPED):
        problems.append("the receipt is not one row for each shipped certificate")
    for k, row in rows.items():
        stated = header(certificate_path(k).read_bytes())
        if [row["b"], row["n"], row["waste"], row["exact_side"]] != [
            stated.b,
            stated.n,
            stated.waste,
            str(stated.side),
        ]:
            problems.append(f"k = {k}: the receipt states another certificate")
        if not (
            row["decision"]["passed"]
            and row["controls_refused"]
            and row["side_below_k"]
            and row["instance_of_theorem_a"]
            and row.get("sharp_controls_as_expected", k > SHARP_THROUGH)
        ):
            problems.append(f"k = {k}: the receipt does not show it accepted with its controls")
    if receipt.get("summary") != summary(list(rows.values())):
        problems.append("the summary is not the rows'")
    problems.extend(
        f"k = {k}: decided again, it differs from the receipt"
        for k in replayed
        if _untimed(replay_row(k)) != _untimed(rows[k])
    )
    return problems


# --------------------------------------------------------------------------- command line


def _write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(retained_json.dumps(value), encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    sub = parser.add_subparsers(dest="action", required=True)
    construction = sub.add_parser("construction", help="the construction's checks")
    construction.add_argument("--bound", type=int, default=NOTE_BOUND)
    construction.add_argument("--geometry", type=int, default=40)
    construction.add_argument("--out", type=Path, help="also write the report here")
    run = sub.add_parser("replay", help="decide the 36 certificates and write the receipt")
    run.add_argument("--workers", type=int, default=2)
    compare = sub.add_parser("compare", help="the integer comparisons with the family")
    compare.add_argument("--limit", type=int, default=COMPARE_LIMIT)
    compare.add_argument("--out", type=Path, help="also write the comparisons here")
    verify = sub.add_parser("check", help="read the replay receipt back against the packet")
    verify.add_argument("--replay", type=int, nargs="*", default=[])
    args = parser.parse_args(argv)
    if args.action == "construction":
        report = construction_report(args.bound, args.geometry)
        if args.out is not None:
            _write(args.out, report)
        print(retained_json.dumps(report), end="")
        print(
            "THEOREM_A_CONSTRUCTION_HOLDS"
            if report["passed"]
            else "THEOREM_A_CONSTRUCTION_FAILS"
        )
        return 0 if report["passed"] else 1
    if args.action == "compare":
        found = comparisons(args.limit)
        if args.out is not None:
            _write(args.out, found)
        print(retained_json.dumps(found), end="")
        return 0
    if args.action == "replay":
        receipt = replay(args.workers)
        _write(REPLAY_RECEIPT, receipt)
        print(retained_json.dumps(receipt["summary"]), end="")
        return 0
    problems = check_replay(args.replay)
    for problem in problems:
        print(problem, file=sys.stderr)
    print("THEOREM_A_REPLAY_ADMITTED" if not problems else "THEOREM_A_REPLAY_REFUSED")
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
