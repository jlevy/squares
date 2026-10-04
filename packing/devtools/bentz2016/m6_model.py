"""The side-6 one-spare model: n = 32 against Bentz 2016 Section 3 (Theorem 9).

Reached through `python -m devtools.bentz2016.one_spare_inventory --n 32`.

## The configuration

Red rows `k = 1..6` sit at heights `y_k = c + (k-1) sqrt(3)/2` with `c = sqrt(2) - 1/2`;
odd rows carry five points at `x = 1..5`, even rows six points at `x = 0.5..5.5`. Blue
is red mirrored in `y = 3` (transcription lines 126 to 128). Both sets are unavoidable,
so every box of a packing of 33 holds one point of each colour; with 32 boxes one point
of each colour is spare.

## The moves

Theorem 9 moves whole rows *vertically* (transcription line 136) while every gap stays
in `[1/2, sqrt(3)/2]` and the two edge rows stay within `c` of their wall. A row holding
a frozen point cannot move at all. Those are difference constraints, so the feasible
heights of each row form an interval and the whole system is a shortest-path problem on
seven nodes, which `reach` solves.

A six-point row can then be shifted 0.1 sideways when it is unfrozen and both
neighbours can be brought within 0.8 (Lemma 1 at that shift needs
`sqrt(0.36 + v^2) <= 1`), and its end point can be moved to `x = 1` when both
neighbours are within `2 sqrt(2) - 2` (Lemma 6). Doing the moves at every reachable
height puts the whole rectangle `[0.4, 1] x [lo, hi]` (full) or `[0.5, 1] x [lo, hi]`
(partial) inside the end point's box, because boxes are convex. Points of five-point
rows have vertical trajectories `{x} x [lo, hi]`.

## Why the budget matters

`2c + 2(0.8) + 3 sqrt(3)/2 - 6 = 0.02650` is all the slack there is, and it is the
line the transcription printed without its leading factor 2 (`D-507`). With that
budget, a single frozen row removes the shift of every interior six-point row on its
side: red row 2 shifts only if no red row 3 to 6 is frozen, red row 4 only if no red
row 4 to 6 is frozen, red row 6 only if itself unfrozen, and mirrored for blue rows 5,
3, 1. The partial gap `2 sqrt(2) - 2` never rescues a lost shift. That is why almost
every structure here is a kill and why Theorem 9's machinery does not extend to one
spare.

## Distinctness and the finish

Two counted boxes are distinct when, for some colour, the points they are known to
hold between them are two different points: a box holds one point of each colour, so
no single box explains both. The known points of a counted box are its own end point
and every base point or vertical trajectory of the other colour meeting its rectangle,
each carried by *identity* rather than by colour alone -- sharing a colour label is
not enough, because two boxes can carry each other's end point as their only
cross-colour witness, which one box holding one point of each colour explains. The
maximum pairwise-distinct set is found by brute force over at most six candidates per
line. The finish is the `m = 5` region computation ported to mpmath and cross-checked
against the exact table to `1e-18`.

## The control

Every run first classifies the zero-spare pair, which is `n = 33`, where Theorem 9 is
a theorem: it must come out forced by six distinct full boxes on both wall lines, and
the run stops if it does not. That is what says the kills below are the spare's doing
and not the model's.

## What is not modelled

The end-point move under Lemma 3 at base spacing (`f(sqrt(3)/2) = 0.9564`, so the end
point reaches `x = 0.956` with no vertical move at all) is not modelled. It adds
partial charges only, so no kill would become forced; it could only move a kill to
needs-geometry. Nothing outside Theorem 9's own toolkit is modelled.

The merge propagation that `devtools.bentz2016.one_spare_inventory` runs at side 5 --
Theorem 8 through the boxes two meeting segments force together -- is **not** carried
here, so every count this model reports is a wall-line count alone and its kill class
is an upper bound on what survives that argument.

The two horizontal wall lines are not charged here either, for the same reason as at
side 5: a column cannot move. They are charged by the transposed configurations, whose
structures this toolkit cannot correlate with `(R, B)`, so a kill counted on the two
vertical lines is a kill on all four only for the structure paired with its own
transposed twin.

All arithmetic is mpmath at 50 digits, and the strict inequalities carry an explicit
`1e-30` guard. That the margins are of order `1e-2` is measured rather than asserted:
every guarded comparison reports how far it stood from its threshold, and `run` prints
the closest per site (`guard_margins`). Comparisons that land inside the guard are
exact ties -- a point on a rectangle's edge -- which the guard decides the same way
with or without it, and they are counted apart from the minimum.

Records: `H-227` (and `H-226` for the shared machinery); defects `D-505`, `D-507`.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Any, cast

from mpmath import mp, mpf, sqrt

from sqpack import retained_json

# 50 digits: set once, for the whole model. Every margin below is of order 1e-2.
mp.dps = 50

#: An mpmath real. `Scalar` is a binding on the active context rather than a type, so it
#: cannot be written in an annotation; this is the alias the rest of `devtools` uses.
type Scalar = Any

SIDE = mpf(6)
#: The finishing line's offset from the wall, as printed (`D-505`).
C = sqrt(2) - mpf(1) / 2
#: The base row spacing, sqrt(3)/2.
G3 = sqrt(3) / 2
HALF = mpf(1) / 2
#: Half the diagonal of a maximal box.
RHO = mpf("0.505") * sqrt(2)
STANDOFF = sqrt(2) / 2 - HALF
XL = C + STANDOFF
#: The strict-inequality guard; every real margin here is at least 1e-2.
EPS = mpf(10) ** -30
GAP_MIN = HALF
#: Lemma 1 at a 0.1 shift needs the neighbour gaps at most 0.8.
FULL_GAP = mpf("0.8")
#: Lemma 6 lets the end point move when the gaps are below 2 sqrt(2) - 2.
PART_GAP = 2 * sqrt(2) - 2
DIAG2 = (mpf("1.01") * sqrt(2)) ** 2
COLOURS = ("red", "blue")
OTHER = {"red": "blue", "blue": "red"}
SIDES = ("L", "R")

#: Significant digits in a point's identity key, kept at the value the Session 144
#: mathematical lane's scratch used because the reported orbit count is stated against
#: it. It is **not** neutral, and the tool says so on every run: a key is a decimal
#: string, so `x -> 6 - x -> x` re-rounds twice and does not return the identical
#: string for 5 of the 33 heights. The canonical form therefore splits a few true
#: orbits and the reported orbit count is an upper bound on the number of orbits.
#: `true_orbit_count` recomputes it on integer keys, where the mirror is an exact
#: involution, and `main` prints both. Nothing else depends on this: the
#: classification never compares points across a mirror, so every raw count -- which
#: is what the verdict rests on -- is independent of the key precision.
KEY_DIGITS = 25
#: Scale of the integer keys used for the exact orbit cross-check. Points of this
#: configuration are at least 0.05 apart, so 20 decimal places identify them with
#: enormous margin, and mirroring is the exact integer map `n -> 6 * 10^20 - n`.
INTEGER_KEY_SCALE = 10**20

type PointKey = tuple[str, str]
type Structure = tuple[frozenset[PointKey], tuple[frozenset[PointKey], ...]]
type FlatStructure = tuple[tuple[PointKey, ...], tuple[tuple[PointKey, ...], ...]]
#: A vertical trajectory `x` from `lo` to `hi`; a frozen point has `lo == hi`.
type Trajectory = tuple[Scalar, Scalar, Scalar]
#: A rectangle `(x0, x1), lo, hi` that the counted box must contain.
type Rect = tuple[tuple[Scalar, Scalar], Scalar, Scalar]


#: The closest any `EPS`-guarded comparison came to its threshold while still deciding
#: it, per site, and how many landed inside the guard. See `_note_margin`.
_GUARD_MARGINS: dict[str, Scalar] = {}
_GUARD_TIES: Counter[str] = Counter()


def _note_margin(site: str, margin: Scalar) -> None:
    """Record how far one `EPS`-guarded comparison was from its threshold.

    A margin at or inside the guard is an exact tie up to 50-digit round-off -- these
    quantities are algebraic and coincide exactly, a point sitting on a rectangle's
    edge being the common case -- and the guard decides none of them either way, since
    both the guarded and the unguarded comparison give the same answer on a tie. Those
    are counted. What is minimised is the closest approach of a comparison the guard
    could have flipped, which is the measurement the module docstring's "margins here
    are of order 1e-2" previously only asserted.
    """
    if margin <= EPS:
        _GUARD_TIES[site] += 1
        return
    current = _GUARD_MARGINS.get(site)
    if current is None or margin < current:
        _GUARD_MARGINS[site] = margin


def guard_margins() -> dict[str, object]:
    """The measured `EPS` margins of this process, by decision site.

    Cumulative over the process because the sites are on shared paths, which only makes
    the reported minimum more conservative. The four sites are the ones a verdict turns
    on: which point pairs are close enough to be a double (`close-pair`), whether a
    system of row moves is feasible (`reach`), whether a counted box's rectangle meets
    a trajectory (`meets-x`, `meets-y`), and whether the finish's sup drops below 1/2
    (`finish-sup`).
    """
    return {
        "eps": mp.nstr(EPS, 4),
        "closest_deciding": {
            site: mp.nstr(margin, 10) for site, margin in sorted(_GUARD_MARGINS.items())
        },
        "exact_ties_inside_the_guard": dict(sorted(_GUARD_TIES.items())),
        "min_deciding": (mp.nstr(min(_GUARD_MARGINS.values()), 10) if _GUARD_MARGINS else None),
    }


def point_key(p: tuple[Scalar, Scalar], digits: int = KEY_DIGITS) -> PointKey:
    """Identify a point by its printed coordinates, so computed heights compare."""
    return (str(mp.nstr(p[0], digits)), str(mp.nstr(p[1], digits)))


def red_heights() -> list[Scalar]:
    return [C + k * G3 for k in range(6)]


def base_config(colour: str) -> list[tuple[Scalar, list[Scalar]]]:
    """Rows as `(height, x-coordinates)`, bottom to top."""
    ys = red_heights()
    rows: list[tuple[Scalar, list[Scalar]]] = []
    for k in range(6):
        six = k % 2 == 1
        xs = [HALF + j for j in range(6)] if six else [mpf(1) + j for j in range(5)]
        rows.append((ys[k], xs))
    if colour == "blue":
        rows = [(SIDE - y, xs) for y, xs in reversed(rows)]
    return rows


def config_points(colour: str) -> list[tuple[Scalar, Scalar]]:
    return [(x, y) for y, xs in base_config(colour) for x in xs]


def structures_one_spare(pts: list[tuple[Scalar, Scalar]]) -> list[Structure]:
    """Every one-spare structure: one uncovered point, or one double."""
    out: list[Structure] = [(frozenset([point_key(p)]), ()) for p in pts]
    for a, b in combinations(pts, 2):
        d2 = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
        _note_margin("close-pair", abs(d2 - DIAG2))
        if d2 < DIAG2 - EPS:
            out.append((frozenset(), (frozenset([point_key(a), point_key(b)]),)))
    return out


def frozen_keys(st: Structure) -> set[PointKey]:
    uncovered, groups = st
    return set(uncovered) | {p for g in groups for p in g}


def reach(
    colour: str, frozen_rows: list[int], extra: tuple[tuple[int, int, Scalar], ...] = ()
) -> list[tuple[Scalar, Scalar]] | None:
    """Reachable heights per row, or `None` when the constraints are infeasible.

    Constraints: `y_{k+1} - y_k` in `[GAP_MIN, G3]`; `y_0 <= C`; `y_5 >= 6 - C`; each
    frozen row pinned at its base height; `extra` holds `(i, j, ub)` meaning
    `y_i - y_j <= ub`. Solved as difference constraints by Floyd-Warshall on seven
    nodes, node 6 being the origin.
    """
    base = [y for y, _ in base_config(colour)]
    n = 7
    inf_weight = mpf(10) ** 9
    dist = [[inf_weight] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = mpf(0)

    def add(i: int, j: int, ub: Scalar) -> None:
        # y_i - y_j <= ub is an edge j -> i of weight ub.
        dist[j][i] = min(dist[j][i], ub)

    for k in range(5):
        add(k + 1, k, G3)
        add(k, k + 1, -GAP_MIN)
    add(0, 6, C)
    add(6, 5, -(SIDE - C))
    for k in frozen_rows:
        add(k, 6, base[k])
        add(6, k, -base[k])
    for i, j, ub in extra:
        add(i, j, ub)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    for i in range(n):
        _note_margin("reach", abs(dist[i][i]))
        if dist[i][i] < -EPS:
            return None
    return [(-dist[k][6], dist[6][k]) for k in range(6)]


def neighbour_extra(i: int, gap: Scalar) -> tuple[tuple[int, int, Scalar], ...]:
    """Require row `i` to sit within `gap` of each neighbour it has."""
    extra: list[tuple[int, int, Scalar]] = []
    for j in (i - 1, i + 1):
        if 0 <= j < 6:
            extra.append((i, j, gap))
            extra.append((j, i, gap))
    return tuple(extra)


@dataclass(frozen=True)
class Charge:
    """One end point of one six-point row, on one wall line."""

    status: str
    rect: Rect | None
    end: tuple[Scalar, Scalar]


@dataclass(frozen=True)
class ColourAnalysis:
    frozen_rows: list[int]
    trajectories: dict[PointKey, Trajectory]
    charges: dict[tuple[int, str], Charge]
    six_rows: list[int]


def colour_analysis(colour: str, st: Structure) -> ColourAnalysis:
    """What one colour's structure allows: frozen rows, trajectories, and charges."""
    rows = base_config(colour)
    frozen = frozen_keys(st)
    frozen_rows = sorted(
        {k for k, (y, xs) in enumerate(rows) for x in xs if point_key((x, y)) in frozen}
    )
    base_reach = reach(colour, frozen_rows)
    if base_reach is None:
        raise AssertionError(f"the base configuration of {colour} is infeasible")
    trajectories: dict[PointKey, Trajectory] = {}
    for k, (y, xs) in enumerate(rows):
        lo, hi = base_reach[k]
        for x in xs:
            key = point_key((x, y))
            trajectories[key] = (x, y, y) if key in frozen else (x, lo, hi)
    six_rows = [k for k, (_, xs) in enumerate(rows) if len(xs) == 6]
    charges: dict[tuple[int, str], Charge] = {}
    for k in six_rows:
        y, xs = rows[k]
        for side in SIDES:
            end = (xs[0], y) if side == "L" else (xs[-1], y)
            charges[k, side] = _charge(colour, st, frozen, frozen_rows, k=k, side=side, end=end)
    return ColourAnalysis(frozen_rows, trajectories, charges, six_rows)


def _charge(
    colour: str,
    st: Structure,
    frozen: set[PointKey],
    frozen_rows: list[int],
    *,
    k: int,
    side: str,
    end: tuple[Scalar, Scalar],
) -> Charge:
    key = point_key(end)
    if key in st[0]:
        return Charge("uncovered", None, end)
    if key in frozen:
        return Charge("frozen", None, end)
    if k not in frozen_rows:
        full = reach(colour, frozen_rows, neighbour_extra(k, FULL_GAP))
        if full is not None:
            lo, hi = full[k]
            span = (mpf("0.4"), mpf(1)) if side == "L" else (mpf(5), mpf("5.6"))
            return Charge("full", (span, lo, hi), end)
        partial = reach(colour, frozen_rows, neighbour_extra(k, PART_GAP - EPS))
        if partial is not None:
            lo, hi = partial[k]
            span = (HALF, mpf(1)) if side == "L" else (mpf(5), mpf("5.5"))
            return Charge("partial", (span, lo, hi), end)
    return Charge("none", None, end)


def meets(rect: Rect, traj: Trajectory) -> bool:
    """Does a counted box's rectangle meet a point's vertical trajectory?"""
    (x0, x1), lo, hi = rect
    x, tlo, thi = traj
    _note_margin("meets-x", min(abs(x - x0), abs(x - x1)))
    if not x0 - EPS <= x <= x1 + EPS:
        return False
    _note_margin("meets-y", min(abs(thi - lo), abs(tlo - hi)))
    return not (thi < lo - EPS or tlo > hi + EPS)


@dataclass(frozen=True)
class Disc:
    cx: Scalar
    cy: Scalar
    r: Scalar
    inside: bool


type NumConstraint = Scalar | Disc


def _inside_all(p: tuple[Scalar, Scalar], cons: list[NumConstraint]) -> bool:
    x, y = p
    for con in cons:
        if not isinstance(con, Disc):
            if x < con - EPS:
                return False
            continue
        slack = (x - con.cx) ** 2 + (y - con.cy) ** 2 - con.r * con.r
        if con.inside and slack > EPS:
            return False
        if not con.inside and slack < -EPS:
            return False
    return True


def _pair_candidates(cons: list[NumConstraint]) -> list[tuple[Scalar, Scalar]]:
    cands: list[tuple[Scalar, Scalar]] = []
    for a, b in combinations(cons, 2):
        if not isinstance(a, Disc) and isinstance(b, Disc):
            cands += _line_disc(a, b)
        elif isinstance(a, Disc) and not isinstance(b, Disc):
            cands += _line_disc(b, a)
        elif isinstance(a, Disc) and isinstance(b, Disc):
            cands += _disc_disc(a, b)
    return cands


def _line_disc(x0: Scalar, disc: Disc) -> list[tuple[Scalar, Scalar]]:
    s = disc.r * disc.r - (x0 - disc.cx) ** 2
    if s < -EPS:
        return []
    root = sqrt(max(s, mpf(0)))
    return [(x0, disc.cy + root), (x0, disc.cy - root)]


def _disc_disc(a: Disc, b: Disc) -> list[tuple[Scalar, Scalar]]:
    dx, dy = b.cx - a.cx, b.cy - a.cy
    dd = sqrt(dx * dx + dy * dy)
    if dd == 0:
        return []
    along = (a.r * a.r - b.r * b.r + dd * dd) / (2 * dd)
    off2 = a.r * a.r - along * along
    if off2 < -EPS:
        return []
    off = sqrt(max(off2, mpf(0)))
    mx, my = a.cx + along * dx / dd, a.cy + along * dy / dd
    return [
        (mx + off * dy / dd, my - off * dx / dd),
        (mx - off * dy / dd, my + off * dx / dd),
    ]


def sup_dist_region(
    y_e: Scalar,
    denied: list[int],
    target: tuple[Scalar, Scalar],
    *,
    x_left: Scalar = XL,
    e_x: Scalar = HALF,
    rho: Scalar = RHO,
) -> Scalar | None:
    """The sup of the distance to `target` over the m = 5 midpoint region, in mpmath.

    The same region as `devtools.bentz2016.regions`, evaluated numerically because the
    heights here are irrational. `main` cross-checks three of its values against that
    module's exact table to `1e-18`.
    """
    cons: list[NumConstraint] = [x_left, Disc(e_x, y_e, rho, inside=True)]
    cons += [
        Disc(C, mpf(k), HALF, inside=False)
        for k in denied
        if not (abs(C - target[0]) < EPS and abs(mpf(k) - target[1]) < EPS)
    ]
    tx, ty = target
    cands = _pair_candidates(cons)
    for con in cons:
        if not isinstance(con, Disc):
            cands.append((con, ty))
            continue
        dd = sqrt((tx - con.cx) ** 2 + (ty - con.cy) ** 2)
        if dd == 0:
            continue
        cands.append((con.cx + con.r * (tx - con.cx) / dd, con.cy + con.r * (ty - con.cy) / dd))
        cands.append((con.cx - con.r * (tx - con.cx) / dd, con.cy - con.r * (ty - con.cy) / dd))
    best: Scalar | None = None
    for p in cands:
        if not _inside_all(p, cons):
            continue
        d = sqrt((p[0] - tx) ** 2 + (p[1] - ty) ** 2)
        if best is None or d > best:
            best = d
    return best


def finish_m6(
    y_e: Scalar, rank: int, e_x: Scalar = HALF
) -> dict[str, tuple[Scalar | None, bool]]:
    """The finish for a partial box at height `y_e`, `rank`-th among the six heights."""
    denied = [rank - 1, rank]
    targets = {
        f"(c,{rank - 1})": (C, mpf(rank - 1)),
        f"(c,{rank})": (C, mpf(rank)),
        f"({e_x + 1},y)": (e_x + 1, y_e),
    }
    out: dict[str, tuple[Scalar | None, bool]] = {}
    for name, target in targets.items():
        sup = sup_dist_region(y_e, denied, target, e_x=e_x)
        if sup is not None:
            _note_margin("finish-sup", abs(sup - HALF))
        out[name] = (sup, bool(sup is not None and sup < HALF - EPS))
    return out


def sym_key(
    key: PointKey, *, mirror_x: bool, mirror_y: bool, digits: int = KEY_DIGITS
) -> PointKey:
    x, y = mpf(key[0]), mpf(key[1])
    if mirror_x:
        x = SIDE - x
    if mirror_y:
        y = SIDE - y
    return point_key((x, y), digits)


def sym_structure(
    st: Structure, *, mirror_x: bool, mirror_y: bool, digits: int = KEY_DIGITS
) -> Structure:
    uncovered, groups = st

    def image(k: PointKey) -> PointKey:
        return sym_key(k, mirror_x=mirror_x, mirror_y=mirror_y, digits=digits)

    return (
        frozenset(image(k) for k in uncovered),
        tuple(sorted((frozenset(image(k) for k in g) for g in groups), key=sorted)),
    )


def _flat(st: Structure) -> FlatStructure:
    return (
        tuple(sorted(st[0])),
        tuple(tuple(sorted(g)) for g in sorted(st[1], key=sorted)),
    )


def canonical(
    red: Structure, blue: Structure, digits: int = KEY_DIGITS
) -> tuple[FlatStructure, FlatStructure]:
    """Canonical form under `x -> 6 - x` and `y -> 6 - y`, the latter swapping colours."""
    images: list[tuple[FlatStructure, FlatStructure]] = []
    for mirror_x in (False, True):
        for mirror_y in (False, True):
            r = sym_structure(red, mirror_x=mirror_x, mirror_y=mirror_y, digits=digits)
            b = sym_structure(blue, mirror_x=mirror_x, mirror_y=mirror_y, digits=digits)
            if mirror_y:
                r, b = b, r
            images.append((_flat(r), _flat(b)))
    return min(images)


def mirror_is_involutive(digits: int = KEY_DIGITS) -> bool:
    """Does the double mirror return the identical key for every point of the model?"""
    for colour in COLOURS:
        for p in config_points(colour):
            key = point_key(p, digits)
            once = sym_key(key, mirror_x=True, mirror_y=True, digits=digits)
            if sym_key(once, mirror_x=True, mirror_y=True, digits=digits) != key:
                return False
    return True


type IntKey = tuple[int, int]
type IntStructure = tuple[tuple[IntKey, ...], tuple[tuple[IntKey, ...], ...]]


def _int_key(key: PointKey) -> IntKey:
    scale = mpf(INTEGER_KEY_SCALE)
    return (int(mp.nint(mpf(key[0]) * scale)), int(mp.nint(mpf(key[1]) * scale)))


def _int_structure(st: Structure, *, mirror_x: bool, mirror_y: bool) -> IntStructure:
    side = 6 * INTEGER_KEY_SCALE

    def image(key: PointKey) -> IntKey:
        x, y = _int_key(key)
        return (side - x if mirror_x else x, side - y if mirror_y else y)

    return (
        tuple(sorted(image(k) for k in st[0])),
        tuple(sorted(tuple(sorted(image(k) for k in g)) for g in st[1])),
    )


def true_orbit_count(reds: list[Structure], blues: list[Structure]) -> int:
    """The orbit count on integer keys, where the mirror is an exact involution.

    The decimal-string keys the inventory reports against are not exactly involutive,
    so the reported orbit count can split a true orbit. This is the same quotient
    computed where the group really acts, and it is printed beside the reported count
    rather than replacing it, because the reported count is what the record states.
    """
    canonicals: set[tuple[IntStructure, IntStructure]] = set()
    for red in reds:
        for blue in blues:
            images: list[tuple[IntStructure, IntStructure]] = []
            for mirror_x in (False, True):
                for mirror_y in (False, True):
                    r = _int_structure(red, mirror_x=mirror_x, mirror_y=mirror_y)
                    b = _int_structure(blue, mirror_x=mirror_x, mirror_y=mirror_y)
                    if mirror_y:
                        r, b = b, r
                    images.append((r, b))
            canonicals.add(min(images))
    return len(canonicals)


@dataclass(frozen=True)
class CountedBox:
    colour: str
    row: int
    status: str
    #: The witnesses this box is known to hold, as `(colour, point key)` pairs: its own
    #: end point, and every point of the other colour whose trajectory its rectangle
    #: meets. The identity of the point is carried, not just its colour, because the
    #: colour alone does not decide distinctness (see `boxes_are_distinct`).
    known: frozenset[tuple[str, PointKey]]
    span: tuple[Scalar, Scalar]


def _witnesses(box: CountedBox, colour: str) -> frozenset[PointKey]:
    """The points of one colour this box is known to hold."""
    return frozenset(key for c, key in box.known if c == colour)


def boxes_are_distinct(a: CountedBox, b: CountedBox) -> bool:
    """Are these two counted boxes provably different boxes?

    A box of a packing of this configuration holds one point of each colour, so two
    counted boxes are distinct as soon as some colour `c` has two *different* known
    points between them: one box cannot hold both. Sharing a colour *label* is not
    enough, and that was the bug this predicate replaced -- two boxes can each carry
    the other's end point as their only cross-colour witness, in which case a single
    box holding one point of each colour explains both and nothing is contradicted.
    """
    return any(len(_witnesses(a, colour) | _witnesses(b, colour)) >= 2 for colour in COLOURS)


def _max_distinct(boxes: list[CountedBox]) -> list[CountedBox]:
    """The largest pairwise-distinct subset, by brute force over at most six boxes."""
    for r in range(len(boxes), 0, -1):
        for sub in combinations(boxes, r):
            if all(boxes_are_distinct(a, b) for a, b in combinations(sub, 2)):
                return list(sub)
    return []


@dataclass
class M6Line:
    full_rows: list[tuple[str, int]]
    partial_rows: list[tuple[str, int]]
    max_distinct_full: int
    max_distinct_all: int
    boxes: list[CountedBox]


@dataclass
class M6Verdict:
    lines: dict[str, M6Line]
    klass: str
    reason: str


def _side_boxes(
    side: str,
    analyses: dict[str, ColourAnalysis],
    structures: dict[str, Structure],
) -> tuple[list[CountedBox], str | None]:
    boxes: list[CountedBox] = []
    immediate: str | None = None
    for colour in COLOURS:
        for (k, box_side), charge in analyses[colour].charges.items():
            if box_side != side or charge.status not in ("full", "partial"):
                continue
            rect = charge.rect
            if rect is None:
                continue
            known = {(colour, point_key(charge.end))}
            for key, traj in analyses[OTHER[colour]].trajectories.items():
                if not meets(rect, traj):
                    continue
                known.add((OTHER[colour], key))
                if key in structures[OTHER[colour]][0]:
                    immediate = (
                        f"{side}: rectangle of {colour} row {k + 1} meets the uncovered "
                        f"{OTHER[colour]} point {key}"
                    )
            boxes.append(
                CountedBox(colour, k, charge.status, frozenset(known), (rect[1], rect[2]))
            )
    return boxes, immediate


def classify(
    red_st: Structure, blue_st: Structure, cache: dict[object, ColourAnalysis]
) -> M6Verdict:
    """Classify one (red, blue) pair at side 6."""
    structures = {"red": red_st, "blue": blue_st}
    analyses: dict[str, ColourAnalysis] = {}
    for colour in COLOURS:
        cache_key = (colour, _flat(structures[colour]))
        if cache_key not in cache:
            cache[cache_key] = colour_analysis(colour, structures[colour])
        analyses[colour] = cache[cache_key]
    lines: dict[str, M6Line] = {}
    immediate: str | None = None
    for side in SIDES:
        boxes, hit = _side_boxes(side, analyses, structures)
        immediate = immediate or hit
        fulls = [b for b in boxes if b.status == "full"]
        parts = [b for b in boxes if b.status == "partial"]
        lines[side] = M6Line(
            full_rows=sorted((b.colour, b.row + 1) for b in fulls),
            partial_rows=sorted((b.colour, b.row + 1) for b in parts),
            max_distinct_full=len(_max_distinct(fulls)),
            max_distinct_all=len(_max_distinct(fulls + parts)),
            boxes=boxes,
        )
    if immediate:
        return M6Verdict(lines, "forced", "theorem8-uncovered-on-trajectory: " + immediate)
    for side in SIDES:
        if lines[side].max_distinct_full >= 6:
            return M6Verdict(lines, "forced", f"{side}: six distinct full boxes")
    for side in SIDES:
        line = lines[side]
        if line.max_distinct_full == 5 and line.max_distinct_all == 6:
            verdict = _five_plus_partial(side, line, lines)
            if verdict is not None:
                return verdict
    best = max(SIDES, key=lambda s: lines[s].max_distinct_all)
    line = lines[best]
    if line.max_distinct_all >= 6:
        return M6Verdict(
            lines,
            "needs-geometry",
            f"{best}: {line.max_distinct_full} distinct full + partial to "
            f"{line.max_distinct_all} (full rows {line.full_rows}, partial rows "
            f"{line.partial_rows}); claim needed: these cannot coexist on l",
        )
    return M6Verdict(
        lines,
        "kill",
        f"at most {line.max_distinct_all} distinct counted boxes on either line "
        f"(best {best}: full {line.full_rows}, partial {line.partial_rows})",
    )


def _five_plus_partial(side: str, line: M6Line, lines: dict[str, M6Line]) -> M6Verdict | None:
    """Five distinct full boxes and a partial that completes the six: try the finish."""
    fulls = [b for b in line.boxes if b.status == "full"]
    for partial in [b for b in line.boxes if b.status == "partial"]:
        sub = [*fulls, partial]
        if len(sub) < 6 or not all(boxes_are_distinct(a, b) for a, b in combinations(sub, 2)):
            continue
        lo, hi = partial.span
        # Rows never cross, so ordering the six boxes by base height gives the rank
        # the finish's denied points are numbered by.
        order = sorted(sub, key=lambda b: base_config(b.colour)[b.row][0])
        rank = order.index(partial) + 1
        for y_e in (lo, (lo + hi) / 2, hi):
            finish = finish_m6(y_e, rank)
            forced = [name for name, (_, ok) in finish.items() if ok]
            if forced:
                sup = finish[forced[0]][0]
                return M6Verdict(
                    lines,
                    "forced",
                    f"{side}: five full + partial ({partial.colour} row "
                    f"{partial.row + 1}, rank {rank}, height {mp.nstr(y_e, 8)}): "
                    f"finish forces {forced[0]} (sup {mp.nstr(sup, 8)})",
                )
        return M6Verdict(
            lines,
            "needs-geometry",
            f"{side}: five full + partial ({partial.colour} row {partial.row + 1}, "
            f"rank {rank}); finish not established at heights in "
            f"[{mp.nstr(lo, 6)}, {mp.nstr(hi, 6)}]",
        )
    return None


def format_structure(st: Structure) -> str:
    uncovered, groups = st
    u = ",".join(f"({a},{b})" for a, b in sorted(uncovered))
    g = ";".join(
        "{" + ",".join(f"({a},{b})" for a, b in sorted(group)) + "}" for group in groups
    )
    return f"U[{u}] G[{g}]"


def _reason_key(verdict: M6Verdict) -> str:
    reason = verdict.reason
    if verdict.klass == "forced":
        if reason.startswith("theorem8"):
            return "forced: Theorem 8"
        if "six distinct" in reason:
            return "forced: six distinct full"
        return "forced: five full + partial finish"
    return verdict.klass + ": " + reason.split(": ", 1)[1].split(";")[0].split(" (")[0]


#: The exact m = 5 sups this model's numeric finish must reproduce, from
#: `devtools.bentz2016.regions.finish_table`.
EXACT_FINISH_CHECKS = {
    (mpf("0.9"), 1, (C, mpf(1))): "0.49732750715365940639",
    (mpf("2.5"), 3, (mpf("1.5"), mpf("2.5"))): "0.38133345358899121517",
    (mpf("1.7"), 2, (mpf("1.5"), mpf("1.7"))): "0.45097589580953922704",
}


def report_budget() -> None:
    """The Theorem 9 constants, printed so a reader can check them against the PDF."""
    for colour in COLOURS:
        reachable = reach(colour, [])
        if reachable is None:
            raise AssertionError(f"{colour} base configuration infeasible")
        print(
            f"{colour} base reachable heights: "
            f"{[(mp.nstr(lo, 6), mp.nstr(hi, 6)) for lo, hi in reachable]}"
        )
        for k in (1, 3, 5) if colour == "red" else (0, 2, 4):
            shifted = reach(colour, [], neighbour_extra(k, FULL_GAP))
            span = (
                None
                if shifted is None
                else (mp.nstr(shifted[k][0], 6), mp.nstr(shifted[k][1], 6))
            )
            print(f"   six-point row {k + 1}: full-shift heights {span}")
    budget = 2 * C + mpf("1.6") + 3 * G3 - 6
    print(
        "budget 2(sqrt2 - 1/2) + 2*0.8 + 3*sqrt3/2 - 6 = "
        f"{mp.nstr(budget, 10)} (the D-507 line; without the factor 2 it is "
        f"{mp.nstr(C + mpf('1.6') + 3 * G3, 10)} < 6, which is false)"
    )


def cross_check_finish() -> None:
    """The numeric finish must agree with the exact m = 5 table."""
    for (y_e, rank, target), exact in EXACT_FINISH_CHECKS.items():
        sup = sup_dist_region(y_e, [rank - 1, rank], target)
        if sup is None or abs(sup - mpf(exact)) >= mpf(10) ** -18:
            raise AssertionError(f"numeric finish disagrees at {y_e}: {sup} vs {exact}")
    print("numeric finish agrees with the exact m=5 table to 1e-18: OK")


def zero_spare_control() -> M6Verdict:
    """The n = 33 control: no spare in either colour, so nothing is frozen.

    Theorem 9 is a theorem at zero spares, so this pair must come out forced, and by
    the mechanism the paper uses rather than by an accident of the model: six distinct
    full boxes, on both wall lines. It is to this model what `--check` is to the side-5
    tool, and it is what says a kill at one spare is the spare's doing.
    """
    return classify((frozenset(), ()), (frozenset(), ()), {})


def report_zero_spare_control() -> dict[str, object]:
    """Print the n = 33 control, and fail the run if it is not forced."""
    verdict = zero_spare_control()
    lines = {
        side: {
            "max_distinct_full": verdict.lines[side].max_distinct_full,
            "max_distinct_all": verdict.lines[side].max_distinct_all,
            "full_rows": [list(row) for row in verdict.lines[side].full_rows],
            "partial_rows": [list(row) for row in verdict.lines[side].partial_rows],
        }
        for side in SIDES
    }
    both = all(verdict.lines[side].max_distinct_full >= 6 for side in SIDES)
    print(
        f"n=33 zero-spare control: {verdict.klass} ({verdict.reason}); "
        f"six distinct full boxes on both lines: {both}"
    )
    if verdict.klass != "forced" or not both:
        raise AssertionError(f"the zero-spare n=33 control is not forced: {verdict}")
    return {"class": verdict.klass, "reason": verdict.reason, "lines": lines}


def run() -> dict[str, object]:
    """Run the n = 32 inventory and return its payload, printing the report as it goes.

    The payload is what `--json` writes and what the record's counts are read from, so
    a test can pin those counts without going through the file.
    """
    report_budget()
    cross_check_finish()
    control = report_zero_spare_control()
    reds = structures_one_spare(config_points("red"))
    blues = structures_one_spare(config_points("blue"))
    print(
        f"n=32 (red k=1, blue k=1): red structures {len(reds)} "
        f"(uncovered {sum(1 for u, _ in reds if u)}, doubles {sum(1 for _, g in reds if g)}); "
        f"blue {len(blues)}; pairs {len(reds) * len(blues)}"
    )
    cache: dict[object, ColourAnalysis] = {}
    orbits: dict[tuple[FlatStructure, FlatStructure], dict[str, object]] = {}
    classes: Counter[str] = Counter()
    reasons: Counter[str] = Counter()
    invariance_ok = True
    for red in reds:
        for blue in blues:
            verdict = classify(red, blue, cache)
            classes[verdict.klass] += 1
            reasons[_reason_key(verdict)] += 1
            key = canonical(red, blue)
            seen = orbits.get(key)
            if seen is not None:
                seen["size"] = int(seen["size"]) + 1  # pyright: ignore[reportArgumentType]
                if seen["class"] != verdict.klass:
                    invariance_ok = False
                continue
            orbits[key] = {
                "red": format_structure(red),
                "blue": format_structure(blue),
                "size": 1,
                "class": verdict.klass,
                "reason": verdict.reason,
                "lines": {
                    side: {
                        "full_rows": verdict.lines[side].full_rows,
                        "partial_rows": verdict.lines[side].partial_rows,
                        "max_distinct_full": verdict.lines[side].max_distinct_full,
                        "max_distinct_all": verdict.lines[side].max_distinct_all,
                    }
                    for side in SIDES
                },
            }
    orbit_classes = Counter(str(v["class"]) for v in orbits.values())
    exact_orbits = true_orbit_count(reds, blues)
    print(f"  raw pairs: {sum(classes.values())} -> {dict(classes)}")
    print(
        f"  orbits (x-mirror, y-mirror with colour swap): {len(orbits)} -> "
        f"{dict(orbit_classes)}  invariant: {invariance_ok}"
    )
    print(
        f"  orbit-count cross-check: {len(orbits)} reported at {KEY_DIGITS}-digit "
        f"decimal keys (double mirror exact: {mirror_is_involutive()}), "
        f"{exact_orbits} on exact integer keys; the raw counts above, and every "
        "verdict, are independent of the key precision"
    )
    for reason, count in sorted(reasons.items(), key=lambda kv: -kv[1]):
        print(f"    {count:6d}  {reason}")
    patterns: Counter[str] = Counter()
    for orbit in orbits.values():
        if orbit["class"] == "forced":
            continue
        lines = cast("dict[str, dict[str, int]]", orbit["lines"])
        shape = ", ".join(
            f"({side}: {lines[side]['max_distinct_full']} distinct full, "
            f"{lines[side]['max_distinct_all']} with partial)"
            for side in SIDES
        )
        patterns[f"{orbit['class']} {shape}"] += int(orbit["size"])  # pyright: ignore[reportArgumentType]
    if patterns:
        print("  non-forced patterns -> raw count:")
        for shape, count in sorted(patterns.items(), key=lambda kv: -kv[1]):
            print(f"    {count:6d}  {shape}")
    margins = guard_margins()
    print(
        f"  EPS-guarded decisions: closest deciding margin per site "
        f"{margins['closest_deciding']}, exact ties inside the guard "
        f"{margins['exact_ties_inside_the_guard']}, guard {margins['eps']}"
    )
    return {
        "tool": "devtools.bentz2016.one_spare_inventory --n 32",
        "label": "n=32 (red k=1, blue k=1) at side 6",
        "counts": {
            "red_structures": len(reds),
            "blue_structures": len(blues),
            "raw_pairs": len(reds) * len(blues),
            "orbits": len(orbits),
        },
        "classes_raw": dict(classes),
        "classes_orbits": dict(orbit_classes),
        "key_digits": KEY_DIGITS,
        "mirror_involutive_on_decimal_keys": mirror_is_involutive(),
        "orbits_on_exact_integer_keys": exact_orbits,
        "reasons_raw": dict(reasons),
        "non_forced_patterns_raw": dict(patterns),
        "invariance_ok": invariance_ok,
        "guard_margins": guard_margins(),
        "zero_spare_n33_control": control,
        "orbits": list(orbits.values()),
    }


def main(out_path: str | None = None) -> int:
    """Run the n = 32 inventory and, with a path, write it."""
    inventory = run()
    if out_path:
        out = Path(out_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(retained_json.dumps(inventory, default=str), encoding="utf-8")
        print(f"  inventory written to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
