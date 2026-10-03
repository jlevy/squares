"""The n17 local-minimum checker (H-261, BC-407): point checks and the slider-box ratio test.

Two modes. The default certifies, at one rational point with fixed sliders, the kernel
of the positively weighted H-258 rows, exact coordinate duals for the 90 signed
non-slider directions, and the margins of the 135 unavailable owner alternatives.

`--ratio` implements the frozen recipe of
`docs/project/reviews/review-2026-10-02-n17-local-theorem-recipe.md` over a declared
slider box in `(a, b, z)`, by default `B_W = [0, 1/4] x [0, 1/12] x [-1/8, 1/16]`
(`--box` declares another, recorded as the receipt's `slider_box`), and a uniform
radius (1/5000): the rows rebuilt at the moving base point `x*(w)` with
`k = (1 - |tau|)/2` on the 45 non-slider columns (C4, exact and at symbolic root
parameters), the tau branches (C3), the curvature constants (C7), the 125 unavailable
options' Taylor margins (C6), per-cell affine duals with exact residual bounds on an
adaptive cell partition (C8, root-box residual folded in) and the strict ratio test
(C9), spanning (C10), the slide half of C2, the roster bound to the H-257 inventory
(C1), the H-258 stress recomputed along the family and nonnegative on the box with the
kernel re-checked at every vertex (C11), and the C12 refusal controls with the n11
replay. Its receipt is planning evidence, not an H-261 verdict: the recipe's lemmas are
hand proofs and tightness at `x*(0)` is H-257's.

Every box item reads the declared box's own vertices. A box on which some retained
face's tau leaves its declared sign branch or reaches `|tau| = 1` (for instance `a < 0`,
`b <= -tau_{11,12}(0)`, about `-0.0568`, or `z >= tau_{13,14}(0)`, about `0.0806`) is
refused before any dual is sought: the face rows use `|tau| = branch * tau`, so they
and C4's affine form are right only inside the branches. A floor `b < 0` is allowed,
since H-268's slide range reaches `b* = -1.685 r`, where square 11 has moved toward
square 9. The family point `x*(w)` then overlaps 9 and 11 by `|b|` across the dropped
9/11 face: its rows are not retained, its weights stay exactly zero (C11), its offset
`tau_{9,11}` does not depend on `b`, and C2 and C10 are identities in the sliders with
no sign on `b`. The conclusion `x = x*(w(x))` then says no packing in the
neighbourhood has `b < 0`.

Point. Everything is evaluated in `fractions.Fraction` arithmetic at the exact
rational point H-258 uses: the exp-237 root-box midpoint `(t, b)`, with the H-254
centres and the fixed H-256 centroid sliders built by `_layout`.

Model. The 58 common-core rows `A_i z >= 0` and their weights come unchanged from
`check_n17_core_stress.complete_stress`, in its frozen row order and its 52 columns
`z = (xi_1, eta_1, omega_1, ..., xi_17, eta_17, omega_17, sigma)`, with `sigma` the
side velocity. Exactly six weights vanish (5-right W-/W+, 6-bottom W-/W+, the 9/11 face
E-/E+); the other 52 rows form the positive set `P`.

Sliders and coordinates. With `u = (c, s)` and `v = (-s, c)` the frame of squares 9 to
14, the six slider generators are the unit vectors of `xi_5`, `xi_6`, `eta_6`, `omega_6`
and the vectors `v` placed on `(xi_11, eta_11)` and on `(xi_13, eta_13)`. The 45
non-slider coordinates are the remaining unit covectors, except that squares 11 and 13
contribute `u . V_11` and `u . V_13` (their component along `u`) instead of `xi` and
`eta`. The kernel claim is `rank A_P = 46` (exact elimination over Q, cross-checked mod
a prime) with every generator annihilated by every positive row, so the kernel is
exactly their span; all 58 rows have rank 50 with lineality `xi_6` and square 13 along
`v`.

Coordinate duals. For each non-slider covector `f_j` and sign `s` in {+1, -1}:

    minimise    a
    over        lambda_i >= 0 (i in P, the 52 positive rows only), a >= 0
    subject to  sum_{i in P} lambda_i A_i = a e_sigma - s f_j     (all 52 columns)

Any feasible pair gives `s f_j . z = a sigma - lambda^T A_P z <= a sigma` on the
first-order cone `A_P z >= 0`: this is the n11 focused-rectangle dual
`lambda^T A = (sign) e_j` with the side column carried by the multiple `a` and with
residual `epsilon_j = 0`. Requiring `a >= 0` loses nothing, since `z = 0` is feasible
in the primal below, so the optimum is nonnegative; and for a smaller packing
(`sigma <= 0`) the side term `a sigma` only helps. The curvature step this module does
not implement would add `M_j = sum_i lambda_i K_i` against the coordinate radius `r_j`,
reading the exact `lambda` from `solve_direction`. The six zero-weight rows are excluded
because the H-261
neighbourhood leaves the slider coordinates free, so those rows need not be active. The
kernel enters twice: `A_P k = 0`, `f_j . k = 0` and `e_sigma . k = 0` for every slider
generator `k`, so the six slider columns of the identity vanish identically and a
certificate is indifferent to the slider values; and the program is posed in the 46
quotient coordinates (45 non-slider plus `sigma`), where `A_P` has full column rank.
The Lagrangian dual is `maximise s f_j . z subject to A_P z >= 0, sigma <= 1`.

Solution and verification. HiGHS proposes an optimal vertex of that primal; the active
set seeds `sqpack.exact_lp.solve`, which re-derives the vertex in exact arithmetic and
pivots by Bland's rule to the exact optimum, restarting from the origin vertex if the
float hint is not an exact vertex. Each certificate is then verified independently of
the simplex: `lambda >= 0`, the 52-column identity exactly, and an exact primal point
`z` with `A_P z >= 0`, `sigma <= 1` and `s f_j . z = a`, so `a` is the exact optimum and
not only a bound. A direction with no nonnegative dual is reported with an exact ray
`z` (`A_P z >= 0`, `sigma <= 0`, `s f_j . z = 1`) and refuses the receipt.

Owner alternatives. Of the 168 raw separating-axis options of the 21 zero pairs (both
owners, both owner axes, both signs; `option_manifest`), 135 are unavailable. Each
margin `sign n . (r_j - r_i) - H_i(n) - H_j(n)`, with the support `H(n)` taken with exact
absolute values, must be strictly negative at the point.

Controls. `kernel-row` adds `xi_5` to the 5-bottom W- row, which must break the kernel
claim; `infeasible-dual` withholds the loaded 4-top W- row, which keeps the kernel claim
but removes every nonnegative dual of the leading direction `-omega_11`. A receipt is
accepted only if every target check passes and both controls are refused.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
import math
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass, replace
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import linprog

from devtools.check_n17_contact_chart import ANCHORS, CONTACTS
from devtools.check_n17_core_stress import (
    DIMENSION,
    FROZEN_FEATURE_REF,
    Dyadic,
    ExactField,
    _pair_rows,
    _root_intervals,
    _wall_rows,
    common_rows,
    complete_stress,
    deterministic_weights,
    force_roster,
)
from devtools.check_n17_endpoint_feasibility import (
    FROZEN_ROOT_REF,
    REPO,
    Box,
    _fraction_string,
    _layout,
    _object_unique,
    _read_limited,
    _wall_gap,
    require_retained_path,
)
from devtools.check_n17_endpoint_feasibility import _support as _axis_support
from devtools.check_n17_endpoint_features import (
    AXES,
    PARALLEL_PAIRS,
    option_manifest,
    square_class,
)
from sqpack.exact_lp import (
    ExactLP,
    ExactLPError,
    ExactSolution,
    LinearRow,
    independent_rows,
    rational_sign,
    solve,
)

SCHEMA = "n17-local-minimum-mechanical/v1"
ROOT_CERTIFICATE = (
    REPO
    / "packing/campaign/series/series-000-smoke-and-calibration/results"
    / "exp-237-n17-polynomial-root/run-001/certificate.json"
)
SOURCES = (
    "packing/devtools/check_n17_local_minimum.py",
    "packing/devtools/check_n17_core_stress.py",
    "packing/devtools/check_n17_endpoint_feasibility.py",
    "packing/devtools/check_n17_endpoint_features.py",
    "packing/devtools/check_n17_contact_chart.py",
    "packing/src/sqpack/exact_lp.py",
    "packing/devtools/check_n11_optimality_local_dual.py",
    "packing/devtools/check_n11_optimality_local_isolation.py",
    "packing/cases/trump11/isolation_radius.py",
)
HALF = Q(1, 2)
SIDE = DIMENSION - 1
COMPONENTS = {"x": 0, "y": 1, "angle": 2}
ZERO_WEIGHT_KEYS = frozenset(
    {
        ("wall", 5, "right", 0),
        ("wall", 5, "right", 1),
        ("wall", 6, "bottom", 0),
        ("wall", 6, "bottom", 1),
        ("pair", 9, 11, 0),
        ("pair", 9, 11, 1),
    }
)
SLIDERS = ("xi5", "xi6", "eta6", "omega6", "v11", "v13")
LINEALITY = ("xi6", "v13")
EXPECTED_RANK_POSITIVE = 46
EXPECTED_RANK_ALL = 50
MODULUS = (1 << 61) - 1
CONTROLS = ("kernel-row", "infeasible-dual")
CONTROL_DIRECTION = ("omega11", -1)
DECIMAL_DIGITS = 30

RowKey = tuple[Any, ...]
Vector = dict[int, Q]


def column(label: int, component: str) -> int:
    """Column of a square's `x`, `y` or `angle` velocity in the H-258 order."""
    return 3 * (label - 1) + COMPONENTS[component]


def row_label(key: RowKey) -> str:
    return ":".join(str(part) for part in key)


def decimal(value: Q, digits: int = DECIMAL_DIGITS) -> str:
    """A rounded decimal for reading; the exact rational is always reported beside it."""
    with localcontext() as context:
        context.prec = digits
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def _digits(value: Q) -> list[int]:
    """Decimal digit counts of numerator and denominator, without `str` on huge ints."""
    text = _fraction_string(abs(value))
    top, _, bottom = text.partition("/")
    return [len(top), len(bottom) if bottom else 1]


def _sha256_json(document: Any) -> str:
    return hashlib.sha256(json.dumps(document, sort_keys=True).encode()).hexdigest()


@dataclass(frozen=True)
class Model:
    """The 58 H-258 rows and weights at one exact rational point, as Fractions."""

    t: Q
    b: Q
    keys: tuple[RowKey, ...]
    rows: dict[RowKey, tuple[Q, ...]]
    weights: dict[RowKey, Q]
    stress_residuals: tuple[Q, ...]
    u: tuple[Q, Q]
    v: tuple[Q, Q]
    side: Q

    @property
    def positive_keys(self) -> tuple[RowKey, ...]:
        return tuple(key for key in self.keys if key not in ZERO_WEIGHT_KEYS)


def build_model(t: Q, b: Q) -> Model:
    """Rebuild the frozen H-258 rows and weights with exact rational inputs."""
    if type(t) is not Q or type(b) is not Q:
        raise TypeError("the model point must be exact Fractions")
    rows, weights, _, residuals = complete_stress(t, b, HALF)
    side, aux, _ = _layout(t, b, HALF)
    exact_rows = {key: tuple(Q(value) for value in row) for key, row in rows.items()}
    if len(exact_rows) != 58 or any(len(row) != DIMENSION for row in exact_rows.values()):
        raise ValueError("H-258 builder no longer emits 58 rows of 52 columns")
    return Model(
        t=t,
        b=b,
        keys=tuple(rows),
        rows=exact_rows,
        weights={key: Q(value) for key, value in weights.items()},
        stress_residuals=tuple(Q(value) for value in residuals),
        u=(Q(aux["u"][0]), Q(aux["u"][1])),
        v=(Q(aux["v"][0]), Q(aux["v"][1])),
        side=Q(side),
    )


def mutate(model: Model, control: str) -> Model:
    """Apply one synthetic control mutation; the target model is never altered."""
    if control == "kernel-row":
        key = ("wall", 5, "bottom", 0)
        row = list(model.rows[key])
        row[column(5, "x")] += Q(1, 1000)
        return replace(model, rows={**model.rows, key: tuple(row)})
    if control == "infeasible-dual":
        withheld = ("wall", 4, "top", 0)
        return replace(model, keys=tuple(key for key in model.keys if key != withheld))
    raise ValueError(f"unknown control: {control}")


def slider_generators(model: Model) -> dict[str, Vector]:
    """The six named slider motions as exact sparse vectors over the 52 columns."""
    (vx, vy) = model.v
    return {
        "xi5": {column(5, "x"): Q(1)},
        "xi6": {column(6, "x"): Q(1)},
        "eta6": {column(6, "y"): Q(1)},
        "omega6": {column(6, "angle"): Q(1)},
        "v11": {column(11, "x"): vx, column(11, "y"): vy},
        "v13": {column(13, "x"): vx, column(13, "y"): vy},
    }


def coordinates(model: Model) -> dict[str, Vector]:
    """The 45 non-slider covectors, which are also their own lifts since `u` is unit."""
    return coordinate_lifts(model.u)


def coordinate_lifts(u: tuple[Q, Q]) -> dict[str, Vector]:
    """The 45 non-slider covectors for the frame `u` of squares 9 to 14."""
    (ux, uy) = u
    result: dict[str, Vector] = {}
    for label in range(1, 18):
        if label == 6:
            continue
        if label in {11, 13}:
            result[f"u{label}"] = {column(label, "x"): ux, column(label, "y"): uy}
        elif label != 5:
            result[f"xi{label}"] = {column(label, "x"): Q(1)}
        if label not in {11, 13}:
            result[f"eta{label}"] = {column(label, "y"): Q(1)}
        result[f"omega{label}"] = {column(label, "angle"): Q(1)}
    if len(result) != 45:
        raise ValueError("non-slider coordinate roster drifted")
    return result


def directions(model: Model) -> tuple[tuple[str, int], ...]:
    return tuple((name, sign) for name in coordinates(model) for sign in (1, -1))


def _apply(row: Sequence[Q], vector: Vector) -> Q:
    return sum((row[index] * value for index, value in vector.items()), Q(0))


def exact_rank(matrix: Sequence[Sequence[Q]]) -> int:
    """Rank over Q by Gaussian elimination, choosing the sparsest pivot row."""
    work = [list(row) for row in matrix if any(row)]
    rank = 0
    width = len(work[0]) if work else 0
    for index in range(width):
        candidates = [position for position in range(rank, len(work)) if work[position][index]]
        if not candidates:
            continue
        position = min(candidates, key=lambda row: sum(value != 0 for value in work[row]))
        work[rank], work[position] = work[position], work[rank]
        pivot = work[rank]
        inverse = 1 / pivot[index]
        for other in range(rank + 1, len(work)):
            factor = work[other][index]
            if factor != 0:
                scale = factor * inverse
                work[other] = [
                    left - scale * right if right != 0 else left
                    for left, right in zip(work[other], pivot, strict=True)
                ]
        rank += 1
    return rank


def modular_rank(matrix: Sequence[Sequence[Q]], modulus: int = MODULUS) -> int:
    """Rank modulo a prime, a lower bound for the rank over Q when entries are p-integral."""
    work: list[list[int]] = []
    for row in matrix:
        reduced: list[int] = []
        for value in row:
            if value.denominator % modulus == 0:
                raise ValueError("entry is not integral at the modular-rank prime")
            reduced.append(value.numerator * pow(value.denominator, -1, modulus) % modulus)
        work.append(reduced)
    rank = 0
    width = len(work[0]) if work else 0
    for index in range(width):
        position = next((r for r in range(rank, len(work)) if work[r][index]), None)
        if position is None:
            continue
        work[rank], work[position] = work[position], work[rank]
        inverse = pow(work[rank][index], -1, modulus)
        for other in range(rank + 1, len(work)):
            factor = work[other][index] * inverse % modulus
            if factor:
                work[other] = [
                    (left - factor * right) % modulus
                    for left, right in zip(work[other], work[rank], strict=True)
                ]
        rank += 1
    return rank


def weight_audit(model: Model) -> dict[str, Any]:
    """Confirm the six prescribed zero weights and the positivity of the other 52."""
    zero = sorted(row_label(key) for key in model.keys if model.weights[key] == 0)
    negative = sorted(row_label(key) for key in model.keys if model.weights[key] < 0)
    positive = [model.weights[key] for key in model.keys if model.weights[key] > 0]
    expected_zero = sorted(row_label(key) for key in ZERO_WEIGHT_KEYS)
    smallest = min(
        (key for key in model.keys if model.weights[key] > 0), key=model.weights.__getitem__
    )
    nonzero_residuals = {
        str(index): decimal(value, 12)
        for index, value in enumerate(model.stress_residuals)
        if value != 0
    }
    return {
        "rows": len(model.keys),
        "zero_weight_rows": zero,
        "negative_weight_rows": negative,
        "positive_weight_rows": len(positive),
        "smallest_positive_weight": {
            "row": row_label(smallest),
            "value": decimal(model.weights[smallest], 12),
        },
        "stress_residual_columns_at_point": nonzero_residuals,
        "passed": zero == expected_zero and not negative and len(positive) == 52,
    }


def kernel_audit(model: Model) -> dict[str, Any]:
    """Exact rank, kernel basis and lineality of the positive rows and of all rows."""
    positive = [model.rows[key] for key in model.positive_keys]
    every = [model.rows[key] for key in model.keys]
    generators = slider_generators(model)
    rank_positive = exact_rank(positive)
    rank_all = exact_rank(every)
    modular_positive = modular_rank(positive)
    modular_all = modular_rank(every)
    dense = [
        [vector.get(index, Q(0)) for index in range(DIMENSION)]
        for vector in generators.values()
    ]
    generator_rank = exact_rank(dense)
    annihilated: dict[str, bool] = {}
    zero_row_values: dict[str, dict[str, str]] = {}
    for name, vector in generators.items():
        annihilated[name] = all(
            _apply(model.rows[key], vector) == 0 for key in model.positive_keys
        )
        zero_row_values[name] = {
            row_label(key): _fraction_string(_apply(model.rows[key], vector))
            for key in model.keys
            if key not in model.positive_keys and _apply(model.rows[key], vector) != 0
        }
    lineality = sorted(name for name, values in zero_row_values.items() if not values)
    kernel_dimension = DIMENSION - rank_positive
    equals_span = kernel_dimension == 6 and generator_rank == 6 and all(annihilated.values())
    checks = {
        "rank_positive": rank_positive == EXPECTED_RANK_POSITIVE,
        "rank_positive_mod_p": modular_positive == EXPECTED_RANK_POSITIVE,
        "kernel_equals_slider_span": equals_span,
        "rank_all": rank_all == EXPECTED_RANK_ALL,
        "rank_all_mod_p": modular_all == EXPECTED_RANK_ALL,
        "lineality": DIMENSION - rank_all == 2
        and annihilated["xi6"]
        and annihilated["v13"]
        and lineality == sorted(LINEALITY),
    }
    return {
        "positive_rows": len(positive),
        "rank_positive": rank_positive,
        "rank_positive_mod_p": modular_positive,
        "kernel_dimension": kernel_dimension,
        "generator_rank": generator_rank,
        "generators": {
            name: {str(index): _fraction_string(value) for index, value in vector.items()}
            for name, vector in generators.items()
        },
        "generators_annihilated_by_positive_rows": annihilated,
        "generator_values_on_zero_weight_rows": zero_row_values,
        "rank_all": rank_all,
        "rank_all_mod_p": modular_all,
        "lineality_dimension": DIMENSION - rank_all,
        "lineality_generators": lineality,
        "modulus": str(MODULUS),
        "checks": checks,
        "passed": all(checks.values()),
    }


@dataclass(frozen=True)
class Quotient:
    """Positive rows written in the 46 quotient coordinates (45 non-slider and sigma)."""

    names: tuple[str, ...]
    lifts: tuple[Vector, ...]
    keys: tuple[RowKey, ...]
    rows: tuple[tuple[Q, ...], ...]


def quotient(model: Model) -> Quotient:
    named = coordinates(model)
    names = (*named, "sigma")
    lifts = (*named.values(), {SIDE: Q(1)})
    keys = model.positive_keys
    rows = tuple(tuple(_apply(model.rows[key], lift) for lift in lifts) for key in keys)
    return Quotient(names=names, lifts=lifts, keys=keys, rows=rows)


def _lift(space: Quotient, point: Sequence[Q]) -> list[Q]:
    full = [Q(0)] * DIMENSION
    for value, lift in zip(point, space.lifts, strict=True):
        for index, coefficient in lift.items():
            full[index] += value * coefficient
    return full


def _exact_program(space: Quotient, objective_index: int, sign: int, *, ray: bool) -> ExactLP:
    """`min -s z_j` over `-A_P z <= 0`, `sigma <= 1`; or the bounded ray program."""
    width = len(space.names)
    unit = [Q(0)] * width
    unit[-1] = Q(1)
    rows = [
        LinearRow(row_label(key), tuple(-value for value in row))
        for key, row in zip(space.keys, space.rows, strict=True)
    ]
    rows.append(LinearRow("sigma", tuple(unit)))
    rhs = [Q(0)] * len(space.keys) + [Q(0) if ray else Q(1)]
    if ray:
        bound = [Q(0)] * width
        bound[objective_index] = Q(sign)
        rows.append(LinearRow("bound", tuple(bound)))
        rhs.append(Q(1))
    objective = [Q(0)] * width
    objective[objective_index] = Q(-sign)
    return ExactLP(tuple(objective), tuple(rows), tuple(rhs), Q(0), Q(1))


def _float_order(lp: ExactLP, space: Quotient, objective_index: int, sign: int) -> list[int]:
    """Rows ordered by their slack at a HiGHS optimum, tightest first."""
    width = len(space.names)
    matrix = np.array([[float(value) for value in row.coefficients] for row in lp.rows])
    rhs = np.array([float(value) for value in lp.rhs])
    cost = np.zeros(width)
    cost[objective_index] = -sign
    result = linprog(cost, A_ub=matrix, b_ub=rhs, bounds=[(None, None)] * width, method="highs")
    if result.status != 0:
        return list(range(len(lp.rows)))
    slack = rhs - matrix @ result.x
    return sorted(range(len(lp.rows)), key=lambda index: (abs(float(slack[index])), index))


def _exact_solve(lp: ExactLP, order: list[int], width: int) -> tuple[ExactSolution, str]:
    """Bland's rule from the float-suggested vertex, else from the origin vertex."""
    try:
        start = independent_rows(lp, order, size=width)
        return solve(lp, start, rational_sign), "float_hint"
    except ExactLPError as error:
        if error.kind == "unbounded":
            raise
    origin = independent_rows(lp, range(len(lp.rows) - 1), size=width)
    return solve(lp, origin, rational_sign), "origin"


def _verify_dual(
    model: Model, space: Quotient, name: str, sign: int, *, lam: dict[RowKey, Q], a: Q
) -> bool:
    """Replay `sum lambda_i A_i = a e_sigma - s f_j` in all 52 columns, independently."""
    if a < 0 or any(value < 0 for value in lam.values()) or not set(lam) <= set(space.keys):
        return False
    total = [Q(0)] * DIMENSION
    for key, value in lam.items():
        for index, coefficient in enumerate(model.rows[key]):
            if coefficient != 0:
                total[index] += value * coefficient
    expected = [Q(0)] * DIMENSION
    expected[SIDE] = a
    for index, coefficient in coordinates(model)[name].items():
        expected[index] -= sign * coefficient
    return total == expected


def _verify_primal(
    model: Model,
    space: Quotient,
    name: str,
    sign: int,
    *,
    point: Sequence[Q],
    value: Q,
    ray: bool,
) -> bool:
    """Replay the primal witness on the original rows: feasibility and attained value."""
    full = _lift(space, point)
    feasible = all(_apply(model.rows[key], dict(enumerate(full))) >= 0 for key in space.keys)
    side_ok = full[SIDE] <= 0 if ray else full[SIDE] <= 1
    attained = sign * _apply(full, coordinates(model)[name]) == value
    return feasible and side_ok and attained


@dataclass(frozen=True)
class DirectionSolution:
    """The exact outcome for one signed direction.

    For `certified_optimal`, `lam` and `a` are the exact dual and `point` the exact primal
    optimum in the quotient coordinates; for `no_nonnegative_dual`, `point` is the exact
    ray. A downstream curvature step reads `lam` from here rather than from a receipt.
    """

    name: str
    sign: int
    status: str
    lam: dict[RowKey, Q]
    a: Q | None
    point: tuple[Q, ...]
    active: tuple[str, ...] = ()
    pivots: int = 0
    start: str = ""
    error: str = ""

    @property
    def label(self) -> str:
        return f"{'+' if self.sign > 0 else '-'}{self.name}"


def verify_solution(model: Model, space: Quotient, solution: DirectionSolution) -> bool:
    """Replay a certificate on the original 52 columns, independently of the simplex."""
    if solution.status == "certified_optimal" and solution.a is not None:
        return _verify_dual(
            model, space, solution.name, solution.sign, lam=solution.lam, a=solution.a
        ) and _verify_primal(
            model,
            space,
            solution.name,
            solution.sign,
            point=solution.point,
            value=solution.a,
            ray=False,
        )
    if solution.status == "no_nonnegative_dual":
        return _verify_primal(
            model,
            space,
            solution.name,
            solution.sign,
            point=solution.point,
            value=Q(1),
            ray=True,
        )
    return False


def solve_direction(model: Model, space: Quotient, name: str, sign: int) -> DirectionSolution:
    """Exact optimal dual and primal certificate for one signed non-slider direction."""
    index = space.names.index(name)
    width = len(space.names)
    lp = _exact_program(space, index, sign, ray=False)
    try:
        solution, start = _exact_solve(lp, _float_order(lp, space, index, sign), width)
    except ExactLPError as error:
        if error.kind != "unbounded":
            return DirectionSolution(name, sign, "undecided", {}, None, (), error=str(error))
        return _no_dual(model, space, name, sign)
    vertex = solution.vertex
    lam: dict[RowKey, Q] = {}
    a = Q(0)
    for row_index, multiplier in zip(vertex.active, vertex.multipliers, strict=True):
        if row_index == len(space.keys):
            a = multiplier
        elif multiplier != 0:
            lam[space.keys[row_index]] = multiplier
    result = DirectionSolution(
        name,
        sign,
        "certified_optimal",
        lam,
        a,
        tuple(vertex.point),
        active=tuple(lp.rows[row].label for row in vertex.active),
        pivots=solution.pivots,
        start=start,
    )
    if a != -vertex.objective_value or not verify_solution(model, space, result):
        return replace(result, status="undecided", error="exact replay failed")
    return result


def _no_dual(model: Model, space: Quotient, name: str, sign: int) -> DirectionSolution:
    """Certify, by an exact ray, that a direction has no nonnegative dual."""
    index = space.names.index(name)
    lp = _exact_program(space, index, sign, ray=True)
    try:
        solution, start = _exact_solve(
            lp, _float_order(lp, space, index, sign), len(space.names)
        )
    except ExactLPError as error:
        return DirectionSolution(name, sign, "undecided", {}, None, (), error=str(error))
    result = DirectionSolution(
        name,
        sign,
        "no_nonnegative_dual",
        {},
        None,
        tuple(solution.vertex.point),
        pivots=solution.pivots,
        start=start,
    )
    if solution.vertex.objective_value != -1 or not verify_solution(model, space, result):
        return replace(result, status="undecided", error="ray replay failed")
    return result


def direction_record(solution: DirectionSolution) -> dict[str, Any]:
    """The receipt entry: exact optimum, readable multipliers, digests of exact vectors."""
    record: dict[str, Any] = {
        "direction": solution.label,
        "coordinate": solution.name,
        "sign": solution.sign,
        "status": solution.status,
        "pivots": solution.pivots,
        "start": solution.start,
    }
    point_digest = _sha256_json([_fraction_string(value) for value in solution.point])
    if solution.status == "certified_optimal" and solution.a is not None:
        exact = {row_label(key): _fraction_string(value) for key, value in solution.lam.items()}
        record.update(
            {
                "a": _fraction_string(solution.a),
                "a_decimal": decimal(solution.a),
                "a_digits": _digits(solution.a),
                "support": len(solution.lam),
                "lambda_sum_decimal": decimal(sum(solution.lam.values(), Q(0)), 12),
                "lambda_decimal": {
                    row_label(key): decimal(value, 10) for key, value in solution.lam.items()
                },
                "lambda_sha256": _sha256_json(exact),
                "primal_sha256": point_digest,
                "active_rows": list(solution.active),
            }
        )
    elif solution.status == "no_nonnegative_dual":
        record.update(
            {
                "ray_sha256": point_digest,
                "ray_side_velocity": _fraction_string(solution.point[-1]),
            }
        )
    else:
        record["error"] = solution.error
    return record


def dual_audit(
    model: Model,
    *,
    only: Sequence[tuple[str, int]] | None = None,
    fail_fast: bool = False,
    progress: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    """Exact coordinate duals for every requested signed non-slider direction."""
    space = quotient(model)
    wanted = tuple(only) if only is not None else directions(model)
    solutions: list[DirectionSolution] = []
    for name, sign in wanted:
        solution = solve_direction(model, space, name, sign)
        solutions.append(solution)
        if progress is not None:
            value = "" if solution.a is None else decimal(solution.a, 12)
            progress(f"{solution.label}: {solution.status} {value}")
        if fail_fast and solution.status != "certified_optimal":
            break
    optima = {
        solution.label: solution.a
        for solution in solutions
        if solution.status == "certified_optimal" and solution.a is not None
    }
    ranked = sorted(optima, key=lambda label: (-optima[label], label))
    return {
        "directions_requested": len(wanted),
        "directions_attempted": len(solutions),
        "certified_optimal": len(optima),
        "no_nonnegative_dual": [
            solution.label for solution in solutions if solution.status == "no_nonnegative_dual"
        ],
        "undecided": [
            solution.label for solution in solutions if solution.status == "undecided"
        ],
        "largest": [
            {"direction": label, "a_decimal": decimal(optima[label], 12)}
            for label in ranked[:12]
        ],
        "zero_multiple": sorted(label for label, value in optima.items() if value == 0),
        "results": [direction_record(solution) for solution in solutions],
        "passed": len(optima) == len(wanted),
    }


def _support(label: int, normal: tuple[Q, Q], aux: dict[str, Any]) -> Q:
    first, second = (aux[name] for name in AXES[square_class(label)])
    return (
        abs(normal[0] * first[0] + normal[1] * first[1])
        + abs(normal[0] * second[0] + normal[1] * second[1])
    ) / 2


def owner_alternative_audit(model: Model) -> dict[str, Any]:
    """Exact margins of the 168 raw owner-axis options; the 135 unavailable must be < 0."""
    _, aux, centres = _layout(model.t, model.b, HALF)
    strict: list[tuple[Q, dict[str, Any]]] = []
    identity: list[tuple[Q, dict[str, Any]]] = []
    for option in option_manifest():
        left, right, owner = int(option["left"]), int(option["right"]), int(option["owner"])
        normal = aux[option["axis"]]
        displacement = (
            centres[right - 1][0] - centres[left - 1][0],
            centres[right - 1][1] - centres[left - 1][1],
        )
        margin = Q(
            option["sign"] * (normal[0] * displacement[0] + normal[1] * displacement[1])
            - _support(left, normal, aux)
            - _support(right, normal, aux)
        )
        entry = {
            "pair": [left, right],
            "owner": owner,
            "axis": option["axis"],
            "sign": option["sign"],
            "margin": _fraction_string(margin),
            "margin_decimal": decimal(margin, 12),
        }
        (identity if option["kind"] == "identity" else strict).append((margin, entry))
    ranked = [entry for _, entry in sorted(strict, key=lambda item: -item[0])]
    negative = sum(margin < 0 for margin, _ in strict)
    largest_identity = max(abs(margin) for margin, _ in identity)
    return {
        "options": len(strict) + len(identity),
        "unavailable": len(strict),
        "strictly_negative": negative,
        "least_negative": [
            {key: row[key] for key in ("pair", "owner", "axis", "sign", "margin_decimal")}
            for row in ranked[:8]
        ],
        "identity_options": len(identity),
        "identity_exact_zero": sum(margin == 0 for margin, _ in identity),
        "identity_largest_abs_decimal": decimal(largest_identity, 6),
        "margins": [entry for _, entry in strict],
        "identity_margins": [entry for _, entry in identity],
        "passed": len(strict) == 135 and negative == 135 and len(identity) == 33,
    }


def run_control(model: Model, control: str) -> dict[str, Any]:
    """Run one synthetic control through the checks it targets; it must be refused."""
    mutated = mutate(model, control)
    kernel = kernel_audit(mutated)
    failed = [f"kernel.{name}" for name, ok in kernel["checks"].items() if not ok]
    detail: dict[str, Any] = {"kernel_checks": kernel["checks"]}
    if control == "infeasible-dual":
        duals = dual_audit(mutated, only=(CONTROL_DIRECTION,), fail_fast=True)
        detail["direction"] = duals["results"][0]
        if not duals["passed"]:
            failed.append(f"duals.{duals['results'][0]['direction']}")
    return {"control": control, "refused": bool(failed), "failed_checks": failed, **detail}


# ---------------------------------------------------------------------------
# The ratio test over the slider box (recipe C3, C4, C7, C8, C9, C12, C6).
#
# Recipe: docs/project/reviews/review-2026-10-02-n17-local-theorem-recipe.md. The base
# point moves with the sliders: x*(w), w = (a, b, z), is the layout with square 5 moved
# by -a e_x, square 11 by -b v and square 13 by +z v, square 6 absent. The 52 retained
# rows are built at x*(w) with k = (1 - |tau|)/2 on every parallel face and written on
# the 45 non-slider columns only (no side column, no slider column). Everything is at
# the exp-237 root-box midpoint; the root-box residual of C8(i) is not folded in.
# ---------------------------------------------------------------------------

RATIO_SCHEMA = "n17-local-minimum-ratio/v1"
CORE_STRESS_COMMIT = "2fbf8d29"
CORE_STRESS_BLOB = "4a67d5fdd6f08585d2cd1d9ffc920d8f8039e0c2"
SLIDER_PARAMETERS = ("a", "b", "z")
DECLARED_BOX: tuple[tuple[Q, Q], ...] = (
    (Q(0), Q(1, 4)),
    (Q(0), Q(1, 12)),
    (Q(-1, 8), Q(1, 16)),
)
DECLARED_RADIUS = Q(1, 5000)
INVERSE_ROOT2_UPPER = Q(7071068, 10**7)
SQRT_SCALE = 10**15
DUAL_BITS = 44
VERTEX_FLOORS = (1e-6, 1e-4)
MAX_CELLS = 2048
RETAINED_FACES = tuple(sorted(PARALLEL_PAIRS - {(9, 11)}))
FACE_BRANCHES: dict[tuple[int, int], int] = {
    pair: -1 if pair == (5, 7) else 1 for pair in sorted(PARALLEL_PAIRS)
}
STRICT_FACES = frozenset({(9, 10), (10, 12), (11, 12), (12, 14), (13, 14)})
SLIDER_SUPPORT: dict[str, tuple[frozenset[RowKey], frozenset[str]]] = {
    "a": (frozenset({("pair", 5, 7, 0), ("pair", 5, 7, 1)}), frozenset({"omega5", "omega7"})),
    "b": (
        frozenset({("pair", 3, 11, 0), ("pair", 11, 12, 0), ("pair", 11, 12, 1)}),
        frozenset({"omega11", "omega12"}),
    ),
    "z": (
        frozenset({("pair", 2, 13, 0), ("pair", 13, 14, 0), ("pair", 13, 14, 1)}),
        frozenset({"omega13", "omega14"}),
    ),
}
N11_RECEIPTS = REPO / "packing/resources/web/n11-optimality-2026-09-29/receipts"
N11_OBJECTS = {
    "weighted": "ffe9f89d40a9538ec9a10d8700999f05483d0ccfad17b84d430590da7dd65889",
    "focused": "9a9cf4e0fdcb1b1d226b9c07ec08d08cbbc572749cec9bc09cf3cd92bd4d88f3",
}

Point = tuple[Q, Q, Q]
SparseRow = dict[int, Q]


def slider_box(values: Sequence[Q]) -> tuple[tuple[Q, Q], tuple[Q, Q], tuple[Q, Q]]:
    """`(a, b, z)` bounds from `A_LO A_HI B_LO B_HI Z_LO Z_HI`, exact and nondegenerate."""
    if len(values) != 6 or any(type(value) is not Q for value in values):
        raise ValueError("slider box needs six exact rationals: A_LO A_HI B_LO B_HI Z_LO Z_HI")
    box = ((values[0], values[1]), (values[2], values[3]), (values[4], values[5]))
    if not all(lo < hi for lo, hi in box):
        raise ValueError("slider box needs LO < HI in each of a, b and z")
    return box


def box_vertices(box: Sequence[tuple[Q, Q]]) -> tuple[Point, ...]:
    """The eight vertices of a box in `(a, b, z)`, low corner first."""
    first, second, third = box
    return tuple((x, y, w) for x, y, w in itertools.product(first, second, third))


def sqrt_upper(value: Q, scale: int = SQRT_SCALE) -> Q:
    """A rational upper bound on `sqrt(value)` with denominator `scale`, checked."""
    if value < 0 or scale <= 0:
        raise ValueError("square-root bound needs a nonnegative radicand")
    scaled = math.ceil(value * scale * scale)
    root = math.isqrt(scaled)
    if root * root < scaled:
        root += 1
    upper = Q(root, scale)
    if upper * upper < value:
        raise ValueError("square-root upper bound is unsound")
    return upper


@dataclass(frozen=True)
class Family:
    """The affine slider family `x*(w)` at one exact root parameter point."""

    t: Q
    beta: Q
    side: Q
    aux: dict[str, Any]
    centres: tuple[tuple[Q, Q], ...]
    names: tuple[str, ...]
    lifts: tuple[Vector, ...]
    keys: tuple[RowKey, ...]
    branches: dict[tuple[int, int], int]


def build_family(
    t: Q, beta: Q, *, branches: dict[tuple[int, int], int] | None = None
) -> Family:
    """Layout, frame and retained-row roster; `branches` declares each face's tau sign."""
    if type(t) is not Q or type(beta) is not Q:
        raise TypeError("the family point must be exact Fractions")
    side, aux, centres = _layout(t, beta, HALF)
    named = coordinate_lifts((Q(aux["u"][0]), Q(aux["u"][1])))
    family = Family(
        t=t,
        beta=beta,
        side=Q(side),
        aux=aux,
        centres=tuple((Q(x), Q(y)) for x, y in centres),
        names=tuple(named),
        lifts=tuple(named.values()),
        keys=(),
        branches=dict(FACE_BRANCHES if branches is None else branches),
    )
    keys = tuple(
        key for key in family_rows(family, (Q(0), Q(0), Q(0))) if key not in ZERO_WEIGHT_KEYS
    )
    if len(keys) != 52:
        raise ValueError("retained roster must have 52 rows")
    return replace(family, keys=keys)


def shifted_centres(
    centres: Sequence[tuple[Any, Any]], v: tuple[Any, Any], w: Sequence[Any]
) -> tuple[tuple[Any, Any], ...]:
    """Generic `x*(w)` centres: 5 by `-a e_x`, 11 by `-b v`, 13 by `+z v` (any arithmetic)."""
    a, b, z = w
    vx, vy = v
    result = list(centres)
    result[4] = (result[4][0] - a, result[4][1])
    result[10] = (result[10][0] - b * vx, result[10][1] - b * vy)
    result[12] = (result[12][0] + z * vx, result[12][1] + z * vy)
    return tuple(result)


def moved_centres(family: Family, w: Point) -> tuple[tuple[Q, Q], ...]:
    """Exact centres of `x*(w)` at the family's rational root point."""
    shifted = shifted_centres(family.centres, family.aux["v"], w)
    return tuple((Q(x), Q(y)) for x, y in shifted)


def generic_face_offset(
    pair: tuple[int, int], axis: str, aux: dict[str, Any], centres: Sequence[tuple[Any, Any]]
) -> Any:
    """The base offset `tau` of a parallel face: tangent component of the displacement."""
    left, right = pair
    nx, ny = aux[axis]
    dx = centres[right - 1][0] - centres[left - 1][0]
    dy = centres[right - 1][1] - centres[left - 1][1]
    return -ny * dx + nx * dy


def face_offset(
    pair: tuple[int, int], axis: str, aux: dict[str, Any], centres: Sequence[tuple[Q, Q]]
) -> Q:
    return Q(generic_face_offset(pair, axis, aux, centres))


def generic_face_rows(
    pair: tuple[int, int],
    axis: str,
    aux: dict[str, Any],
    centres: Sequence[tuple[Any, Any]],
    branch: int,
) -> tuple[list[Any], list[Any]]:
    """E- and E+ of a parallel face with moment arm `k = (1 - branch * tau) / 2`."""
    left, right = pair
    translation: list[Any] = [0] * DIMENSION
    for component, value in zip(("x", "y"), aux[axis], strict=True):
        translation[column(right, component)] = translation[column(right, component)] + value
        translation[column(left, component)] = translation[column(left, component)] - value
    tau = generic_face_offset(pair, axis, aux, centres)
    k = (1 - branch * tau) / 2
    minus, plus = translation.copy(), translation.copy()
    minus[column(left, "angle")] = tau / 2 + k
    minus[column(right, "angle")] = tau / 2 - k
    plus[column(left, "angle")] = tau / 2 - k
    plus[column(right, "angle")] = tau / 2 + k
    return minus, plus


def generic_rows(
    aux: dict[str, Any],
    centres: Sequence[tuple[Any, Any]],
    branches: dict[tuple[int, int], int],
) -> dict[RowKey, list[Any]]:
    """All 58 H-258 rows at the given centres, in the frozen H-258 order (any arithmetic)."""
    rows: dict[RowKey, list[Any]] = {}
    for label, wall in ANCHORS:
        for variant, row in enumerate(_wall_rows(label, wall, aux, HALF)):
            rows["wall", label, wall, variant] = row
    for left, right, axis, _ in CONTACTS:
        pair = (left, right)
        if pair in PARALLEL_PAIRS:
            made: Sequence[list[Any]] = generic_face_rows(
                pair, axis, aux, centres, branches[pair]
            )
        else:
            made = _pair_rows(pair, axis, aux, tuple(centres), HALF)
        for variant, row in enumerate(made):
            rows["pair", left, right, variant] = row
    if len(rows) != 58:
        raise ValueError("family builder must emit 58 rows")
    return rows


def family_rows(family: Family, w: Point) -> dict[RowKey, list[Q]]:
    """All 58 H-258 rows at `x*(w)` over the 52 columns, exact."""
    rows = generic_rows(family.aux, moved_centres(family, w), family.branches)
    return {key: [Q(value) for value in row] for key, row in rows.items()}


def slider_matrix(family: Family, w: Point) -> tuple[SparseRow, ...]:
    """`A_N(w)`: the 52 retained rows on the 45 non-slider columns, sparse."""
    rows = family_rows(family, w)
    result: list[SparseRow] = []
    for key in family.keys:
        row = rows[key]
        projected: SparseRow = {}
        for index, lift in enumerate(family.lifts):
            value = _apply(row, lift)
            if value != 0:
                projected[index] = value
        result.append(projected)
    return tuple(result)


@dataclass(frozen=True)
class AffineMatrix:
    """`A_N(w) = base + a slopes[0] + b slopes[1] + z slopes[2]`, sparse and exact."""

    base: tuple[SparseRow, ...]
    slopes: tuple[tuple[SparseRow, ...], tuple[SparseRow, ...], tuple[SparseRow, ...]]

    def at(self, w: Point) -> tuple[SparseRow, ...]:
        result: list[SparseRow] = []
        for index, row in enumerate(self.base):
            total = dict(row)
            for value, slope in zip(w, self.slopes, strict=True):
                if value != 0:
                    for position, entry in slope[index].items():
                        total[position] = total.get(position, Q(0)) + value * entry
            result.append({key: entry for key, entry in total.items() if entry != 0})
        return tuple(result)


def _difference(
    left: Sequence[SparseRow], right: Sequence[SparseRow], scale: Q
) -> tuple[SparseRow, ...]:
    result: list[SparseRow] = []
    for first, second in zip(left, right, strict=True):
        row: SparseRow = {}
        for position in first.keys() | second.keys():
            value = (first.get(position, Q(0)) - second.get(position, Q(0))) * scale
            if value != 0:
                row[position] = value
        result.append(row)
    return tuple(result)


def sign_branch_audit(family: Family, box: Sequence[tuple[Q, Q]]) -> dict[str, Any]:
    """C3: every retained face's tau keeps its declared sign over the box, |tau| < 1.

    `tau` is affine in `w` (the centres are), so its range over the box is attained at
    the vertices and the eight exact vertex values decide it.
    """
    vertices = box_vertices(box)
    faces: dict[str, Any] = {}
    failures: list[str] = []
    for pair in RETAINED_FACES:
        axis = next(axis for left, right, axis, _ in CONTACTS if (left, right) == pair)
        values = [
            face_offset(pair, axis, family.aux, moved_centres(family, vertex))
            for vertex in vertices
        ]
        branch = family.branches[pair]
        signed = [branch * value for value in values]
        ok = all(0 <= value < 1 for value in signed)
        if pair in STRICT_FACES:
            ok = ok and all(value > 0 for value in signed)
        if not ok:
            failures.append(f"{pair[0]}/{pair[1]}")
        faces[f"{pair[0]}/{pair[1]}"] = {
            "branch": branch,
            "min_decimal": decimal(min(values), 12),
            "max_decimal": decimal(max(values), 12),
            "passed": ok,
        }
    origin = (Q(0), Q(0), Q(0))
    tau0 = face_offset((13, 14), "u", family.aux, moved_centres(family, origin))
    slope = (
        face_offset((13, 14), "u", family.aux, moved_centres(family, (Q(0), Q(0), Q(1)))) - tau0
    )
    crossing = -tau0 / slope
    return {
        "faces": faces,
        "tau_13_14_zero_at_z": _fraction_string(crossing),
        "tau_13_14_zero_at_z_decimal": decimal(crossing, 12),
        "tau_13_14_slope_in_z": _fraction_string(slope),
        "failures": failures,
        "passed": not failures,
    }


def affine_audit(
    family: Family, box: Sequence[tuple[Q, Q]], *, perturb: bool = False
) -> tuple[AffineMatrix, dict[str, Any]]:
    """C4: `A_N(w)` is the exact affine map pinned at four vertices, with the stated support.

    Within the C3 branches every entry is an affine function of the moved centres and
    of `tau`, so of `w`: four affinely independent points pin it. The identity is then
    re-checked exactly on fresh builds at all eight vertices, the centre and two
    interior points. `perturb` is the C12 control that adds an off-support entry to the
    `b` slope, which must be refused.
    """
    low = (box[0][0], box[1][0], box[2][0])
    corner = slider_matrix(family, low)
    slopes: list[tuple[SparseRow, ...]] = []
    for index in range(3):
        point = list(low)
        point[index] = box[index][1]
        moved = slider_matrix(family, (point[0], point[1], point[2]))
        slopes.append(_difference(moved, corner, 1 / (box[index][1] - box[index][0])))
    if perturb:
        tampered = [dict(row) for row in slopes[1]]
        tampered[0][family.names.index("omega1")] = Q(1, 10**6)
        slopes[1] = tuple(tampered)
    base = list(corner)
    for value, slope in zip(low, slopes, strict=True):
        if value != 0:
            shift = [{c: entry * value for c, entry in row.items()} for row in slope]
            base = list(_difference(base, shift, Q(1)))
    matrix = AffineMatrix(tuple(base), (slopes[0], slopes[1], slopes[2]))
    centre = tuple((lo + hi) / 2 for lo, hi in box)
    extra = (
        tuple(lo + (hi - lo) * Q(1, 3) for lo, hi in box),
        tuple(
            lo + (hi - lo) * weight
            for (lo, hi), weight in zip(box, (Q(5, 7), Q(2, 9), Q(8, 11)), strict=True)
        ),
    )
    points = (*box_vertices(box), centre, *extra)
    identity = all(
        slider_matrix(family, (p[0], p[1], p[2])) == matrix.at((p[0], p[1], p[2]))
        for p in points
    )
    support: dict[str, Any] = {}
    support_ok = True
    for name, slope in zip(SLIDER_PARAMETERS, matrix.slopes, strict=True):
        rows_expected, columns_expected = SLIDER_SUPPORT[name]
        rows_found = {family.keys[i] for i, row in enumerate(slope) if row}
        columns_found = {family.names[c] for row in slope for c in row}
        exact = rows_found == rows_expected and columns_found == columns_expected
        support_ok = support_ok and exact
        support[name] = {
            "rows": sorted(row_label(key) for key in rows_found),
            "columns": sorted(columns_found),
            "nonzero_entries": sum(len(row) for row in slope),
            "as_stated": exact,
        }
    rows_at_origin = family_rows(family, (Q(0), Q(0), Q(0)))
    frozen, _, _ = common_rows(family.t, family.beta, HALF)
    binding = set(frozen) == set(rows_at_origin) and all(
        [Q(value) for value in frozen[key]] == rows_at_origin[key] for key in frozen
    )
    dense = [[row.get(c, Q(0)) for c in range(len(family.names))] for row in matrix.base]
    rank = exact_rank(dense)
    checks = {
        "identity_at_eleven_points": identity,
        "support_as_stated": support_ok,
        "rows_at_origin_equal_frozen_h258_rows": binding,
        "rank_at_origin_45": rank == 45,
    }
    return matrix, {
        "points_checked": len(points),
        "support": support,
        "rank_at_origin": rank,
        "checks": checks,
        "passed": all(checks.values()),
    }


def _named_lift(name: str, u: tuple[Any, Any]) -> dict[int, Any]:
    """The lift of one named non-slider coordinate, for any arithmetic of `u`."""
    kind = name.rstrip("0123456789")
    label = int(name[len(kind) :])
    if kind == "u":
        return {column(label, "x"): u[0], column(label, "y"): u[1]}
    return {column(label, {"xi": "x", "eta": "y", "omega": "angle"}[kind]): 1}


def _rational_value(value: Any, field: ExactField, point: Sequence[Q]) -> Q:
    """Evaluate a constant-or-rational-function entry at `point` (t, b, S, mu, nu, rho)."""
    if isinstance(value, (int, Q)):
        return Q(value)
    numerator = Q(str(value.numerator(*point)))
    denominator = Q(1)
    for index, exponent in value.denominator.items():
        denominator *= Q(str(field.factors[index](*point))) ** exponent
    return numerator / denominator


def symbolic_affine_audit(family: Family, matrix: AffineMatrix) -> dict[str, Any]:
    """C4 at symbolic root parameters, and the three tau identities C3 relies on.

    The layout is built over QQ(t, b) with three further indeterminates standing for
    the sliders `(a, b, z)`. Every entry of `A_N(w)` must have vanishing second
    derivatives in the sliders, and slider slopes that do not depend on `(t, beta)`
    and equal the midpoint slopes `A_k`. So `A_N(w) = A_N(0) + sum_k w_k A_k` holds at
    every root in the box, with the same exact `A_k`. The structural offsets
    `tau_{1,2} = tau_{1,3} = 0` and `tau_{5,7} = -a` are identities.
    """
    field = ExactField()
    t, beta = field.generator("t"), field.generator("b")
    sliders = tuple(field.generator(name) for name in ("mu", "nu", "rho"))
    _, aux, centres = _layout(t, beta, HALF)
    moved = shifted_centres(centres, aux["v"], sliders)
    rows = generic_rows(aux, moved, family.branches)
    lifts = [_named_lift(name, aux["u"]) for name in family.names]
    point = (family.t, family.beta, Q(0), Q(0), Q(0), Q(0))
    curved = 0
    rooted = 0
    mismatched = 0
    for index, key in enumerate(family.keys):
        row = rows[key]
        for position, lift in enumerate(lifts):
            entry = field.constant(Q(0))
            for place, coefficient in lift.items():
                if not isinstance(row[place], int) or row[place] != 0:
                    entry = entry + row[place] * coefficient
            for slider, name in enumerate(("mu", "nu", "rho")):
                slope = entry.derivative(name)
                curved += sum(
                    not slope.derivative(other).is_zero for other in ("mu", "nu", "rho")
                )
                rooted += sum(not slope.derivative(other).is_zero for other in ("t", "b"))
                expected = matrix.slopes[slider][index].get(position, Q(0))
                mismatched += _rational_value(slope, field, point) != expected
    offsets: dict[str, bool] = {}
    for pair, expected in (((1, 2), 0), ((1, 3), 0), ((5, 7), -sliders[0])):
        axis = next(axis for left, right, axis, _ in CONTACTS if (left, right) == pair)
        tau = generic_face_offset(pair, axis, aux, moved)
        difference = tau - expected
        offsets[f"{pair[0]}/{pair[1]}"] = (
            difference == 0 if isinstance(difference, (int, Q)) else difference.is_zero
        )
    checks = {
        "no_second_slider_derivative": curved == 0,
        "slopes_free_of_root_parameters": rooted == 0,
        "slopes_equal_midpoint_slopes": mismatched == 0,
        "structural_offsets": all(offsets.values()),
    }
    return {
        "entries": len(family.keys) * len(lifts),
        "offsets": offsets,
        "checks": checks,
        "passed": all(checks.values()),
    }


SPANNING_ANCHORS = tuple(
    anchor for anchor in ANCHORS if anchor not in {(5, "right"), (6, "bottom")}
)


def spanning_audit() -> dict[str, Any]:
    """C10: the retained anchor wall gaps vanish identically along the family.

    Over QQ(t, beta) with indeterminate sliders `(a, b, z)`, each of the 13 retained
    anchors' wall gap at `x*(w)` is the zero rational function, and the anchors touch
    all four walls; so at every root in the box and every `w` the family spans the side
    in both coordinates. Squares 5 and 6 are not needed for this.
    """
    field = ExactField()
    t, beta = field.generator("t"), field.generator("b")
    sliders = tuple(field.generator(name) for name in ("mu", "nu", "rho"))
    side, aux, centres = _layout(t, beta, HALF)
    moved = shifted_centres(centres, aux["v"], sliders)
    gaps: dict[str, bool] = {}
    for label, wall in SPANNING_ANCHORS:
        gap = _wall_gap(label, wall, side, aux, moved, half=HALF)
        gaps[f"{label}:{wall}"] = gap == 0 if isinstance(gap, (int, Q)) else gap.is_zero
    walls = {
        wall: sorted(label for label, side_name in SPANNING_ANCHORS if side_name == wall)
        for wall in ("left", "right", "bottom", "top")
    }
    checks = {
        "anchor_gaps_identically_zero": all(gaps.values()),
        "all_four_walls_touched": all(walls.values()),
    }
    return {"anchors": gaps, "walls": walls, "checks": checks, "passed": all(checks.values())}


def slide_invariance_audit(
    family: Family, *, restore: frozenset[tuple[int, int]] = frozenset()
) -> dict[str, Any]:
    """C2, the slide half: every retained contact margin is unchanged along the family.

    For the 27 identity options of the 19 retained pairs (the tight owner features),
    the support margin `sign n.(c_right - c_left) - H_left(n) - H_right(n)` at `x*(w)`
    minus its value at `x*(0)` is the zero rational function in `(t, beta, a, b, z)`;
    the anchor wall gaps are C10. So tightness along the family reduces to tightness
    at `x*(0)`, which is H-257's at the root. At the rational midpoint those margins
    are reported exactly; nonzero ones carry the midpoint's closing residual.
    `restore` puts dropped pairs back: the C12 control restores 9/11, whose face gap
    is `b` along the family (open for `b > 0`, overlapping for `b < 0`), and must be
    refused. Nothing here depends on the sign of a slider.
    """
    field = ExactField()
    t, beta = field.generator("t"), field.generator("b")
    sliders = tuple(field.generator(name) for name in ("mu", "nu", "rho"))
    _, aux, centres = _layout(t, beta, HALF)
    moved = shifted_centres(centres, aux["v"], sliders)

    def margin(
        values: dict[str, Any], points: Sequence[tuple[Any, Any]], option: dict[str, Any]
    ) -> Any:
        left, right, axis = int(option["left"]), int(option["right"]), str(option["axis"])
        nx, ny = values[axis]
        dx = points[right - 1][0] - points[left - 1][0]
        dy = points[right - 1][1] - points[left - 1][1]
        return (
            option["sign"] * (nx * dx + ny * dy)
            - _axis_support(left, axis, values, HALF)
            - _axis_support(right, axis, values, HALF)
        )

    invariant: dict[str, bool] = {}
    midpoint: dict[str, str] = {}
    for option in option_manifest():
        pair = (int(option["left"]), int(option["right"]))
        if option["kind"] != "identity" or (pair in DROPPED_PAIRS and pair not in restore):
            continue
        label = f"{pair[0]}/{pair[1]}:{option['owner']}:{option['axis']}:{option['sign']}"
        difference = margin(aux, moved, option) - margin(aux, centres, option)
        invariant[label] = (
            difference == 0 if isinstance(difference, (int, Q)) else difference.is_zero
        )
        value = Q(margin(family.aux, family.centres, option))
        if value != 0:
            midpoint[label] = decimal(value, 6)
    return {
        "identity_options": len(invariant),
        "slide_invariant": sum(invariant.values()),
        "not_invariant": sorted(label for label, ok in invariant.items() if not ok),
        "nonzero_at_midpoint": midpoint,
        "passed": len(invariant) == 27 and all(invariant.values()),
    }


FEATURE_CERTIFICATE = (
    REPO
    / "packing/campaign/series/series-000-smoke-and-calibration/results"
    / "exp-239-n17-endpoint-features/run-001/certificate.json"
)
FEATURE_CERTIFICATE_BLOB = "d6047456ac143da0c5aaf6b25e286db75d4497ea"
FEATURE_CERTIFICATE_SHA256 = "f6ba220a66dfe13c4b6fbf1d1aaebc14fc21652b87610d13be3feb09ca09203b"


def git_blob(data: bytes) -> str:
    """Git's blob id of some bytes, computed without Git."""
    return hashlib.sha1(b"blob %d\0" % len(data) + data, usedforsecurity=False).hexdigest()


def roster_binding_audit(family: Family, raw: bytes | None = None) -> dict[str, Any]:
    """C1: the 52-row roster is the accepted H-257 inventory minus the dropped items.

    The exp-239 feature certificate (H-257) must be the frozen blob at
    `FROZEN_FEATURE_REF`, pass its criterion and carry the inventory counts the
    feature manifest reproduces. The roster's pairs must be H-257's zero pairs minus
    2/3 and 9/11, its walls the 15 active wall incidences minus 5-right and 6-bottom,
    and its rows one per wall corner pair (two, except 9's smooth left wall), two per
    face and one per nonparallel identity option.
    """
    data = FEATURE_CERTIFICATE.read_bytes() if raw is None else raw
    document = json.loads(data, object_pairs_hook=_object_unique)
    options = option_manifest()
    zero_pairs = {(int(o["left"]), int(o["right"])) for o in options if o["kind"] == "identity"}
    identity = [o for o in options if o["kind"] == "identity"]
    pairs = {(int(key[1]), int(key[2])) for key in family.keys if key[0] == "pair"}
    walls = {(int(key[1]), str(key[2])) for key in family.keys if key[0] == "wall"}
    retained_identity = [
        o for o in identity if (int(o["left"]), int(o["right"])) not in DROPPED_PAIRS
    ]
    contact_pairs = {tuple(sorted((left, right))) for left, right, _, _ in CONTACTS}
    expected_rows = (
        sum(1 if label == 9 else 2 for label, _ in walls)
        + 2 * len(pairs & PARALLEL_PAIRS)
        + len(pairs - PARALLEL_PAIRS)
    )
    counts = document.get("inventory", {}).get("counts", {})
    checks = {
        "certificate_blob_is_frozen": git_blob(data) == FEATURE_CERTIFICATE_BLOB,
        "certificate_sha256": hashlib.sha256(data).hexdigest() == FEATURE_CERTIFICATE_SHA256,
        "certificate_accepted": document.get("schema") == "n17-endpoint-feature-certificate/v1"
        and document.get("criterion_passed") is True
        and document.get("root_git_ref") == FROZEN_ROOT_REF,
        "manifest_reproduces_counts": counts.get("pairs") == len(zero_pairs) == 21
        and counts.get("pair_zero") == len(identity) == 33
        and counts.get("pair_options") == len(options) == 168
        and counts.get("active_wall_incidences") == len(ANCHORS) == 15
        and counts.get("parallel_pairs") == len(PARALLEL_PAIRS) == 9,
        "pairs_are_zero_pairs_minus_dropped": {tuple(sorted(p)) for p in pairs}
        == zero_pairs - DROPPED_PAIRS
        and zero_pairs - {(2, 3)} == contact_pairs,
        "walls_are_active_walls_minus_dropped": walls
        == set(ANCHORS) - {(5, "right"), (6, "bottom")},
        "rows_match_the_retained_options": len(family.keys) == expected_rows == 52
        and len(retained_identity) == 27,
    }
    return {
        "certificate": str(FEATURE_CERTIFICATE.relative_to(REPO)),
        "certificate_git_ref": FROZEN_FEATURE_REF,
        "certificate_blob": git_blob(data),
        "retained_pairs": len(pairs),
        "retained_walls": len(walls),
        "retained_identity_options": len(retained_identity),
        "checks": checks,
        "passed": all(checks.values()),
    }


STRESS_REBALANCED = (("wall", 5, "bottom"), ("wall", 7, "right"))


def family_stress(
    family: Family, w: Point, reference: Sequence[Q] | None = None
) -> tuple[dict[RowKey, Q], list[Q]]:
    """The H-258 stress recomputed at `x*(w)`, and its residual on the 52 columns.

    `deterministic_weights` runs unchanged on the family rows and moved centres: the
    forces do not depend on `w`, and its moment loop over squares 9 to 14 absorbs the
    `b` and `z` slides. Two changes follow the family: the 5/7 face is split with
    `k = (1 - a)/2` instead of 1/2, and, since `tau_{5,7} = -a` moves the 5/7 torque
    on squares 5 and 7, the moments of the 5-bottom and 7-right walls (each a pair of
    rows with angle coefficients -1/2, +1/2) absorb the change in the omega_5 and
    omega_7 columns relative to `reference`, the residual at `w = 0`, without changing
    any force or the side column.
    """
    rows = family_rows(family, w)
    centres = moved_centres(family, w)
    weights, scales, moments, _ = deterministic_weights(
        rows, family.side, family.aux, centres, HALF
    )
    stress = {key: Q(value) for key, value in weights.items()}
    forces, _ = force_roster(family.aux, scales)
    force, moment, scale = Q(forces[5, 7]), Q(moments[5, 7]), Q(scales["K"])
    tau = face_offset((5, 7), "ey", family.aux, centres)
    k = (1 - family.branches[5, 7] * tau) / 2
    stress["pair", 5, 7, 0] = (force + moment / k) / 2 / scale
    stress["pair", 5, 7, 1] = (force - moment / k) / 2 / scale

    def residual() -> list[Q]:
        return [
            sum((stress[key] * row[c] for key, row in rows.items()), Q(0))
            - (1 if c == SIDE else 0)
            for c in range(DIMENSION)
        ]

    if reference is not None:
        current = residual()
        for _, label, wall in STRESS_REBALANCED:
            change = current[column(label, "angle")] - reference[column(label, "angle")]
            stress["wall", label, wall, 0] += change
            stress["wall", label, wall, 1] -= change
    return stress, residual()


def _face_arm(family: Family, key: RowKey, w: Point) -> Q:
    """The positive arm `k(w)` dividing a face row's weight, 1 for other rows."""
    pair = (int(key[1]), int(key[2])) if key[0] == "pair" else None
    if pair is None or pair not in PARALLEL_PAIRS:
        return Q(1)
    axis = next(axis for left, right, axis, _ in CONTACTS if (left, right) == pair)
    tau = face_offset(pair, axis, family.aux, moved_centres(family, w))
    return (1 - family.branches[pair] * tau) / 2


def stress_audit(family: Family, box: Sequence[tuple[Q, Q]]) -> dict[str, Any]:
    """C11: the recomputed stress is a nonnegative stress on the whole slider box.

    Every column sum of `lambda(w)^T A(w)` is affine in `w` (forces are constant; a
    face pair contributes `F tau/2 +- m` to its angle columns whatever its arm `k`;
    wall moments and the 9-14 moments are affine), so equality with the `w = 0`
    residual, checked exactly at the eight vertices, the centre and two interior
    points, holds on the box. Each weight is `N(w)/k(w)` with `N` affine and `k > 0`
    (`k` the face arm, or 1): `N` is checked affine at the extra points, so its sign,
    and the least value of the weight (linear-fractional), are decided at vertices.
    At `w = 0` the stress is H-258's own, which binds it to the accepted ring proof.
    The kernel of the 52 positive rows is re-checked at every vertex: the six slider
    generators are annihilated exactly and the rank modulo a prime is 46, so the rank
    over Q is exactly 46 and the kernel is their span.
    """
    origin = (Q(0), Q(0), Q(0))
    _, frozen_weights, _, frozen_residuals = complete_stress(family.t, family.beta, HALF)
    base, reference = family_stress(family, origin)
    bound = (
        set(base) == set(frozen_weights)
        and all(base[key] == Q(frozen_weights[key]) for key in base)
        and reference == [Q(value) for value in frozen_residuals]
    )
    vertices = box_vertices(box)
    low = (box[0][0], box[1][0], box[2][0])
    pins = [low] + [
        tuple(box[k][1] if k == index else low[k] for k in range(3)) for index in range(3)
    ]
    extra = [
        tuple((lo + hi) / 2 for lo, hi in box),
        tuple(lo + (hi - lo) * Q(1, 3) for lo, hi in box),
        tuple(
            lo + (hi - lo) * f
            for (lo, hi), f in zip(box, (Q(5, 7), Q(2, 9), Q(8, 11)), strict=True)
        ),
    ]
    numerators: dict[Point, dict[RowKey, Q]] = {}
    weights_at: dict[Point, dict[RowKey, Q]] = {}
    balanced = True
    for point in [*vertices, *extra]:
        w = (point[0], point[1], point[2])
        stress, residual = family_stress(family, w, reference)
        balanced = balanced and residual == reference
        weights_at[w] = stress
        numerators[w] = {key: stress[key] * _face_arm(family, key, w) for key in stress}
    pinned = [numerators[(p[0], p[1], p[2])] for p in pins]
    affine = True
    for point in extra:
        w = (point[0], point[1], point[2])
        for key in base:
            value = pinned[0][key] + sum(
                (
                    (w[k] - low[k])
                    / (box[k][1] - box[k][0])
                    * (pinned[k + 1][key] - pinned[0][key])
                    for k in range(3)
                ),
                Q(0),
            )
            affine = affine and value == numerators[w][key]
    positive = family.keys
    least: tuple[Q, RowKey, Point] | None = None
    for vertex in vertices:
        for key in positive:
            value = weights_at[vertex][key]
            if least is None or value < least[0]:
                least = (value, key, vertex)
    if least is None:
        raise ValueError("the slider box has no vertices")
    vanishing = sorted(
        row_label(key) for key in positive if any(numerators[v][key] <= 0 for v in vertices)
    )
    zeros_exact = all(weights_at[v][key] == 0 for v in vertices for key in ZERO_WEIGHT_KEYS)
    kernel_ok = True
    ranks: list[int] = []
    for vertex in vertices:
        rows = family_rows(family, vertex)
        positive_rows = [rows[key] for key in family.keys]
        vx, vy = (Q(value) for value in family.aux["v"])
        generators = [
            {column(5, "x"): Q(1)},
            {column(6, "x"): Q(1)},
            {column(6, "y"): Q(1)},
            {column(6, "angle"): Q(1)},
            {column(11, "x"): vx, column(11, "y"): vy},
            {column(13, "x"): vx, column(13, "y"): vy},
        ]
        annihilated = all(_apply(row, g) == 0 for row in positive_rows for g in generators)
        rank = modular_rank(positive_rows)
        ranks.append(rank)
        kernel_ok = kernel_ok and annihilated and rank == EXPECTED_RANK_POSITIVE
    checks = {
        "origin_is_the_h258_stress": bound,
        "balanced_like_the_origin_at_eleven_points": balanced,
        "numerators_affine": affine,
        "positive_rows_stay_positive": not vanishing,
        "prescribed_zeros_stay_zero": zeros_exact,
        "kernel_is_the_slider_span_at_every_vertex": kernel_ok,
    }
    return {
        "rebalanced_wall_moments": [f"{label}:{wall}" for _, label, wall in STRESS_REBALANCED],
        "origin_residual_columns": {
            str(c): decimal(value, 6) for c, value in enumerate(reference) if value != 0
        },
        "least_weight_at_origin_decimal": decimal(min(base[key] for key in positive), 12),
        "least_weight": {
            "value_decimal": decimal(least[0], 12),
            "row": row_label(least[1]),
            "vertex": [_fraction_string(value) for value in least[2]],
        },
        "rows_reaching_zero": vanishing,
        "vertex_ranks_mod_p": ranks,
        "checks": checks,
        "passed": all(checks.values()),
    }


@dataclass(frozen=True)
class Enclosure:
    """The H-255 root box: outward 2^-256 interval layout, frame and lifts."""

    radii: tuple[Q, Q]
    aux: dict[str, Any]
    centres: tuple[tuple[Any, Any], ...]
    lifts: tuple[dict[int, Any], ...]


def root_enclosure(family: Family, radii: tuple[Q, Q]) -> Enclosure:
    t, beta = _root_intervals((family.t, family.beta), radii)
    _, aux, centres = _layout(t, beta, Dyadic.point(HALF))
    lifts = tuple(_named_lift(name, aux["u"]) for name in family.names)
    return Enclosure(radii, aux, tuple(centres), lifts)


def _interval(value: Any) -> Dyadic:
    return Dyadic.cast(value if isinstance(value, Box) else Q(value))


def _upper(value: Any) -> Q:
    return value.hi if isinstance(value, Box) else Q(value)


def _magnitude(value: Any) -> Any:
    return value.absolute() if isinstance(value, Box) else abs(value)


def root_box_audit(
    family: Family, enclosure: Enclosure, box: Sequence[tuple[Q, Q]], matrix: AffineMatrix
) -> tuple[tuple[Q, ...], dict[str, Any]]:
    """C8(i) and C3 over the root box.

    By the symbolic C4 the slopes do not depend on the root, so for every root in the
    box and every `w`, `|A*(w) - A_mid(w)| = |A*(0) - A_mid(0)|` entrywise, which the
    interval rows at `w = 0` bound. Returns `d_i`, the row sums of those bounds; a dual
    then carries the extra residual `sum_i lambda_i(w) d_i`. The faces other than the
    three structural ones keep their tau branch, checked on interval vertex values.
    """
    rows = generic_rows(enclosure.aux, enclosure.centres, family.branches)
    deviations: list[Q] = []
    contained = True
    for index, key in enumerate(family.keys):
        row = rows[key]
        total = Q(0)
        for position, lift in enumerate(enclosure.lifts):
            entry = Dyadic.point(Q(0))
            for place, coefficient in lift.items():
                entry = entry + _interval(row[place]) * _interval(coefficient)
            exact = matrix.base[index].get(position, Q(0))
            contained = contained and entry.lo <= exact <= entry.hi
            total += max(entry.hi - exact, exact - entry.lo)
        deviations.append(total)
    faces: dict[str, Any] = {}
    failures: list[str] = []
    for pair in RETAINED_FACES:
        if pair in {(1, 2), (1, 3), (5, 7)}:
            continue
        axis = next(axis for left, right, axis, _ in CONTACTS if (left, right) == pair)
        values = [
            _interval(
                generic_face_offset(
                    pair,
                    axis,
                    enclosure.aux,
                    shifted_centres(enclosure.centres, enclosure.aux["v"], vertex),
                )
            )
            for vertex in box_vertices(box)
        ]
        branch = family.branches[pair]
        low = min(value.lo if branch > 0 else -value.hi for value in values)
        high = max(value.hi if branch > 0 else -value.lo for value in values)
        ok = (low > 0 if pair in STRICT_FACES else low >= 0) and high < 1
        faces[f"{pair[0]}/{pair[1]}"] = {
            "signed_low_decimal": decimal(low, 12),
            "signed_high_decimal": decimal(high, 12),
            "passed": ok,
        }
        if not ok:
            failures.append(f"{pair[0]}/{pair[1]}")
    largest = max(deviations)
    return tuple(deviations), {
        "root_box_radii_decimal": [decimal(value, 6) for value in enclosure.radii],
        "grid_bits": 256,
        "midpoint_entries_contained": contained,
        "largest_row_deviation_decimal": decimal(largest, 6) if largest else "0",
        "row_deviation_sha256": _sha256_json([_fraction_string(v) for v in deviations]),
        "c3_faces": faces,
        "c3_failures": failures,
        "passed": contained and not failures,
    }


def _identity_owner(pair: tuple[int, int]) -> int:
    ordered = tuple(sorted(pair))
    return next(
        int(row["owner"])
        for row in option_manifest()
        if (row["left"], row["right"]) == ordered and row["kind"] == "identity"
    )


def position_box(
    family: Family, radii: dict[str, Q], label: int, enclosure: Enclosure | None = None
) -> tuple[Q, Q]:
    """Half-widths of a centre's perturbation: `u` only for 11 and 13, `y` only for 5.

    With an enclosure, `|u_x|` and `|u_y|` are their upper bounds over the root box.
    """
    if label in {11, 13}:
        if enclosure is None:
            ux, uy = (abs(Q(value)) for value in family.aux["u"])
        else:
            ux, uy = (_interval(value).absolute().hi for value in enclosure.aux["u"])
        return radii[f"u{label}"] * ux, radii[f"u{label}"] * uy
    if label == 5:
        return Q(0), radii["eta5"]
    return radii[f"xi{label}"], radii[f"eta{label}"]


def wall_curvature(angle: Q, inverse_root2: Q) -> Q:
    """n11's wall-gap bound `w^2 / sqrt 2`, with a rational upper bound for `1/sqrt 2`."""
    return inverse_root2 * angle * angle


def pair_curvature(separation: Q, rho: Q, owner: Q, other: Q, inverse_root2: Q) -> Q:
    """n11's pair-gap bound `D w_o^2 + 2 rho w_o + (w_o + w_p)^2 / sqrt 2` (PROOF.md s.7)."""
    return separation * owner * owner + 2 * rho * owner + inverse_root2 * (owner + other) ** 2


def _separation_squared(
    family: Family,
    enclosure: Enclosure | None,
    vertices: Sequence[Point],
    pair: tuple[int, int],
) -> Q:
    """Upper bound of `|c_p - c_o|^2` over the box (and over the root box if enclosed)."""
    left, right = pair
    values: list[Q] = []
    for vertex in vertices:
        c = moved_centres(family, vertex)
        values.append(
            (c[right - 1][0] - c[left - 1][0]) ** 2 + (c[right - 1][1] - c[left - 1][1]) ** 2
        )
        if enclosure is not None:
            e = shifted_centres(enclosure.centres, enclosure.aux["v"], vertex)
            dx = _interval(e[right - 1][0] - e[left - 1][0])
            dy = _interval(e[right - 1][1] - e[left - 1][1])
            values.append((dx * dx + dy * dy).hi)
    return max(values)


def curvature_audit(
    family: Family,
    box: Sequence[tuple[Q, Q]],
    radii: dict[str, Q],
    enclosure: Enclosure | None = None,
) -> tuple[tuple[Q, ...], dict[str, Any]]:
    """C7: an exact rational curvature constant per retained row, uniform over the box.

    `D_op` must bound the centre separation along the whole Taylor segment from
    `x*(w)` to `x*(w) + h`; it is the vertex maximum of the base separation (convex in
    `w`) rounded up, plus `rho_op`, the Euclidean bound on the relative displacement.
    A face row takes the larger of its two owners' bounds (Lemma 2).
    """
    if not 2 * INVERSE_ROOT2_UPPER * INVERSE_ROOT2_UPPER > 1:
        raise ValueError("1/sqrt 2 upper bound is unsound")
    vertices = box_vertices(box)
    constants: list[Q] = []
    detail: dict[str, Any] = {}
    for key in family.keys:
        if key[0] == "wall":
            label = int(key[1])
            constant = wall_curvature(radii[f"omega{label}"], INVERSE_ROOT2_UPPER)
            detail[row_label(key)] = {"kind": "wall", "K_decimal": decimal(constant, 8)}
        else:
            left, right = int(key[1]), int(key[2])
            squared = _separation_squared(family, enclosure, vertices, (left, right))
            (lx, ly), (rx, ry) = (
                position_box(family, radii, left, enclosure),
                position_box(family, radii, right, enclosure),
            )
            rho = sqrt_upper((lx + rx) ** 2 + (ly + ry) ** 2)
            separation = sqrt_upper(squared) + rho
            owners = (
                (left, right)
                if (left, right) in PARALLEL_PAIRS
                else (_identity_owner((left, right)),)
            )
            constant = max(
                pair_curvature(
                    separation,
                    rho,
                    radii[f"omega{owner}"],
                    radii[f"omega{right if owner == left else left}"],
                    INVERSE_ROOT2_UPPER,
                )
                for owner in owners
            )
            detail[row_label(key)] = {
                "kind": "face" if len(owners) == 2 else "cross",
                "owners": list(owners),
                "D_upper_decimal": decimal(separation, 10),
                "rho_upper_decimal": decimal(rho, 10),
                "K_decimal": decimal(constant, 8),
            }
        constants.append(constant)
    largest = max(range(len(constants)), key=constants.__getitem__)
    return tuple(constants), {
        "over_root_box": enclosure is not None,
        "inverse_root2_upper": _fraction_string(INVERSE_ROOT2_UPPER),
        "rows": detail,
        "largest": {
            "row": row_label(family.keys[largest]),
            "K_decimal": decimal(constants[largest], 10),
        },
        "sha256": _sha256_json([_fraction_string(value) for value in constants]),
    }


@dataclass(frozen=True)
class Cell:
    """A closed sub-box of the slider box in `(a, b, z)`."""

    lo: Point
    hi: Point

    @property
    def centre(self) -> Point:
        return (
            (self.lo[0] + self.hi[0]) / 2,
            (self.lo[1] + self.hi[1]) / 2,
            (self.lo[2] + self.hi[2]) / 2,
        )

    @property
    def half(self) -> Point:
        return (
            (self.hi[0] - self.lo[0]) / 2,
            (self.hi[1] - self.lo[1]) / 2,
            (self.hi[2] - self.lo[2]) / 2,
        )

    def split(self, axis: int) -> tuple[Cell, Cell]:
        middle = (self.lo[axis] + self.hi[axis]) / 2
        upper, lower = list(self.hi), list(self.lo)
        upper[axis], lower[axis] = middle, middle
        return (
            Cell(self.lo, (upper[0], upper[1], upper[2])),
            Cell((lower[0], lower[1], lower[2]), self.hi),
        )

    def record(self) -> list[list[str]]:
        return [
            [_fraction_string(lo), _fraction_string(hi)]
            for lo, hi in zip(self.lo, self.hi, strict=True)
        ]


@dataclass(frozen=True)
class AffineDual:
    """`lambda(w) = lam + sum_k (w_k - centre_k) mu[k]` on one cell, dyadic rationals."""

    cell: Cell
    lam: tuple[Q, ...]
    mu: tuple[tuple[Q, ...], tuple[Q, ...], tuple[Q, ...]]


def _transpose_apply(rows: Sequence[SparseRow], weights: Sequence[Q], width: int) -> list[Q]:
    total = [Q(0)] * width
    for weight, row in zip(weights, rows, strict=True):
        if weight != 0:
            for position, entry in row.items():
                total[position] += weight * entry
    return total


def _norm1(values: Sequence[Q]) -> Q:
    return sum((abs(value) for value in values), Q(0))


def ratio_test(radius: Q, epsilon: Q, largest: Q, mass: Q) -> tuple[bool, Q | None]:
    """C9: n11's strict `M < 2 (r_j - eps R)`, and the ratio if the right side is positive."""
    right = 2 * (radius - epsilon * largest)
    if right <= 0:
        return False, None
    return mass < right, mass / right


def evaluate_dual(
    matrix: AffineMatrix,
    curvature: Sequence[Q],
    radii: Sequence[Q],
    *,
    coordinate: int,
    sign: int,
    dual: AffineDual,
    deviation: Sequence[Q] | None = None,
) -> dict[str, Any]:
    """C8 and C9 for one cell and one signed coordinate, in exact arithmetic.

    Residual (C8 iii): with `delta = w - centre`, `|delta_k| <= W_k`,
    `lambda(w)^T A(w) + s e_j = r0 + sum_k delta_k r_k + sum_{k,l} delta_k delta_l q_kl`
    with `r0 = lam^T A_c + s e_j`, `r_k = mu_k^T A_c + lam^T A_k`, `q_kl = mu_k^T A_l`;
    `eps = |r0|_1 + sum_k W_k |r_k|_1 + sum_{k,l} W_k W_l |q_kl|_1`. Nonnegativity
    (C8 ii) and the mass `M` (C8 iv) are exact at the eight vertices, since
    `lambda(w)` is affine. With `deviation` (C8 i), the root-box term
    `max_vertices sum_i lambda_i(w) d_i` is added to `eps`. Ratio (C9):
    `M < 2 (r_j - eps R)`.
    """
    width = len(radii)
    centre, half = dual.cell.centre, dual.cell.half
    rows_c = matrix.at(centre)
    residual0 = _transpose_apply(rows_c, dual.lam, width)
    residual0[coordinate] += sign
    linear: list[Q] = []
    quadratic: list[list[Q]] = []
    for k in range(3):
        first = _transpose_apply(rows_c, dual.mu[k], width)
        second = _transpose_apply(matrix.slopes[k], dual.lam, width)
        linear.append(_norm1([x + y for x, y in zip(first, second, strict=True)]))
        quadratic.append(
            [_norm1(_transpose_apply(matrix.slopes[m], dual.mu[k], width)) for m in range(3)]
        )
    epsilon = (
        _norm1(residual0)
        + sum((half[k] * linear[k] for k in range(3)), Q(0))
        + sum((half[k] * half[m] * quadratic[k][m] for k in range(3) for m in range(3)), Q(0))
    )
    vertex_min: Q | None = None
    mass = Q(0)
    root = Q(0)
    for signs in itertools.product((-1, 1), repeat=3):
        values = [
            dual.lam[i] + sum((signs[k] * half[k] * dual.mu[k][i] for k in range(3)), Q(0))
            for i in range(len(dual.lam))
        ]
        low = min(values)
        vertex_min = low if vertex_min is None else min(vertex_min, low)
        mass = max(mass, sum((v * c for v, c in zip(values, curvature, strict=True)), Q(0)))
        if deviation is not None:
            root = max(root, sum((v * d for v, d in zip(values, deviation, strict=True)), Q(0)))
    epsilon += root
    largest = max(radii)
    below, ratio = ratio_test(radii[coordinate], epsilon, largest, mass)
    nonnegative = vertex_min is not None and vertex_min >= 0
    passed = nonnegative and below
    contributions = [
        half[k]
        * (
            2
            * largest
            * (
                linear[k]
                + sum((half[m] * (quadratic[k][m] + quadratic[m][k]) for m in range(3)), Q(0))
            )
        )
        + half[k] * abs(sum((c * u for c, u in zip(curvature, dual.mu[k], strict=True)), Q(0)))
        for k in range(3)
    ]
    return {
        "epsilon": epsilon,
        "mass": mass,
        "ratio": ratio,
        "vertex_min": vertex_min,
        "nonnegative": nonnegative,
        "passed": passed,
        "split_axis": max(range(3), key=contributions.__getitem__),
        "residual_parts": (_norm1(residual0), linear, quadratic),
        "root_box_residual": root,
    }


@dataclass(frozen=True)
class FloatSystem:
    """Float copies of `A_N` for the LP proposals (never used in a verdict)."""

    base: np.ndarray
    slopes: tuple[np.ndarray, np.ndarray, np.ndarray]
    supports: tuple[tuple[list[int], list[int]], ...]


def float_system(matrix: AffineMatrix, width: int) -> FloatSystem:
    def dense(rows: Sequence[SparseRow]) -> np.ndarray:
        array = np.zeros((len(rows), width))
        for i, row in enumerate(rows):
            for c, value in row.items():
                array[i, c] = float(value)
        return array

    slopes = tuple(dense(slope) for slope in matrix.slopes)
    supports = tuple(
        (
            sorted({i for i, row in enumerate(slope) if row}),
            sorted({c for row in slope for c in row}),
        )
        for slope in matrix.slopes
    )
    return FloatSystem(dense(matrix.base), (slopes[0], slopes[1], slopes[2]), supports)


def propose_dual(
    system: FloatSystem,
    cell: Cell,
    curvature: Sequence[float],
    *,
    largest_radius: float,
    coordinate: int,
    sign: int,
    floor: float,
) -> AffineDual | None:
    """HiGHS proposal of an affine dual minimising `M + 2 R eps_quadratic` on a cell.

    Variables: `lam` (52), `mu_a, mu_b, mu_z` (52 each), the mass bound `m`, and one
    absolute-value variable per entry of `mu_k^T A_l`. Equalities are the zeroth- and
    first-order identities about the cell centre; every vertex value is at least
    `floor`. Only the rounded output is used, and only after the exact replay.
    """
    rows, width = system.base.shape
    centre = tuple(float(value) for value in cell.centre)
    half = tuple(float(value) for value in cell.half)
    at_centre = system.base + sum(c * s for c, s in zip(centre, system.slopes, strict=True))
    quad = [(k, m, c) for k in range(3) for m in range(3) for c in system.supports[m][1]]
    count = 4 * rows + 1 + len(quad)
    mass_index = 4 * rows
    scale = largest_radius * largest_radius
    weights = np.array(curvature) / scale
    equality = np.zeros((4 * width, count))
    target = np.zeros(4 * width)
    equality[:width, :rows] = at_centre.T
    target[coordinate] = -sign
    for k in range(3):
        block = slice((k + 1) * width, (k + 2) * width)
        equality[block, (k + 1) * rows : (k + 2) * rows] = at_centre.T
        equality[block, :rows] += system.slopes[k].T
    upper: list[np.ndarray] = []
    bound: list[float] = []
    for signs in itertools.product((-1, 1), repeat=3):
        block = np.zeros((rows, count))
        block[:, :rows] = -np.eye(rows)
        for k in range(3):
            block[:, (k + 1) * rows : (k + 2) * rows] = -signs[k] * half[k] * np.eye(rows)
        upper.extend(block)
        bound.extend([-floor] * rows)
        line = np.zeros(count)
        line[:rows] = weights
        for k in range(3):
            line[(k + 1) * rows : (k + 2) * rows] = signs[k] * half[k] * weights
        line[mass_index] = -1
        upper.append(line)
        bound.append(0.0)
    objective = np.zeros(count)
    objective[mass_index] = 1
    for index, (k, m, c) in enumerate(quad):
        variable = mass_index + 1 + index
        objective[variable] = 2 / largest_radius * half[k] * half[m]
        for direction in (1, -1):
            line = np.zeros(count)
            for i in system.supports[m][0]:
                line[(k + 1) * rows + i] = direction * system.slopes[m][i, c]
            line[variable] = -1
            upper.append(line)
            bound.append(0.0)
    bounds = [(None, None)] * (mass_index + 1) + [(0, None)] * len(quad)
    result = linprog(
        objective,
        A_ub=np.array(upper),
        b_ub=np.array(bound),
        A_eq=equality,
        b_eq=target,
        bounds=bounds,
        method="highs",
    )
    if result.status != 0:
        return None
    scale_bits = 1 << DUAL_BITS

    def exact(values: np.ndarray) -> tuple[Q, ...]:
        return tuple(Q(round(float(value) * scale_bits), scale_bits) for value in values)

    x = result.x
    return AffineDual(
        cell,
        exact(x[:rows]),
        (
            exact(x[rows : 2 * rows]),
            exact(x[2 * rows : 3 * rows]),
            exact(x[3 * rows : 4 * rows]),
        ),
    )


@dataclass(frozen=True)
class CoordinateOutcome:
    name: str
    sign: int
    certificates: tuple[tuple[AffineDual, dict[str, Any]], ...]
    passed: bool
    note: str = ""

    @property
    def label(self) -> str:
        return f"{'+' if self.sign > 0 else '-'}{self.name}"


def certify_coordinate(
    matrix: AffineMatrix,
    system: FloatSystem,
    curvature: Sequence[Q],
    radii: Sequence[Q],
    *,
    names: Sequence[str],
    name: str,
    sign: int,
    box: Sequence[tuple[Q, Q]],
    max_cells: int = MAX_CELLS,
    deviation: Sequence[Q] | None = None,
) -> CoordinateOutcome:
    """Adaptive bisection of the box until every cell carries a passing exact dual."""
    coordinate = names.index(name)
    floats = [float(value) for value in curvature]
    largest = float(max(radii))
    pending = [Cell((box[0][0], box[1][0], box[2][0]), (box[0][1], box[1][1], box[2][1]))]
    accepted: list[tuple[AffineDual, dict[str, Any]]] = []
    while pending:
        if len(accepted) + len(pending) > max_cells:
            return CoordinateOutcome(
                name, sign, tuple(accepted), passed=False, note="cell limit reached"
            )
        cell = pending.pop()
        verdict: dict[str, Any] | None = None
        for floor in VERTEX_FLOORS:
            dual = propose_dual(
                system,
                cell,
                floats,
                largest_radius=largest,
                coordinate=coordinate,
                sign=sign,
                floor=floor,
            )
            if dual is None:
                continue
            verdict = evaluate_dual(
                matrix,
                curvature,
                radii,
                coordinate=coordinate,
                sign=sign,
                dual=dual,
                deviation=deviation,
            )
            if verdict["passed"]:
                accepted.append((dual, verdict))
                break
            if verdict["nonnegative"]:
                break
        if verdict is not None and verdict["passed"]:
            continue
        half = cell.half
        axis = (
            max(range(3), key=half.__getitem__)
            if verdict is None
            else int(verdict["split_axis"])
        )
        pending.extend(cell.split(axis))
    return CoordinateOutcome(name, sign, tuple(accepted), passed=True)


def outcome_record(outcome: CoordinateOutcome) -> dict[str, Any]:
    """Cells, worst exact ratio and where it occurs, and a digest of the exact duals."""
    record: dict[str, Any] = {
        "direction": outcome.label,
        "cells": len(outcome.certificates),
        "passed": outcome.passed,
    }
    if outcome.note:
        record["note"] = outcome.note
    if not outcome.certificates:
        return record
    worst_dual, worst = max(outcome.certificates, key=lambda item: item[1]["ratio"])
    record.update(
        {
            "worst_ratio": _fraction_string(worst["ratio"]),
            "worst_ratio_decimal": decimal(worst["ratio"], 12),
            "worst_cell": worst_dual.cell.record(),
            "worst_epsilon_decimal": decimal(worst["epsilon"], 6),
            "worst_mass_decimal": decimal(worst["mass"], 12),
            "largest_epsilon_decimal": decimal(
                max(v["epsilon"] for _, v in outcome.certificates), 6
            ),
            "constant_duals": sum(
                all(value == 0 for mu in dual.mu for value in mu)
                for dual, _ in outcome.certificates
            ),
            "duals_sha256": _sha256_json(
                [dual_document(dual) for dual, _ in outcome.certificates]
            ),
        }
    )
    return record


def dual_document(dual: AffineDual) -> dict[str, Any]:
    """The exact certificate of one cell, as integer numerators over `2**DUAL_BITS`."""
    scale = 1 << DUAL_BITS

    def numerators(values: Sequence[Q]) -> list[int]:
        result: list[int] = []
        for value in values:
            scaled = value * scale
            if scaled.denominator != 1:
                raise ValueError("dual entry is off the dyadic grid")
            result.append(scaled.numerator)
        return result

    return {
        "cell": dual.cell.record(),
        "lambda": numerators(dual.lam),
        "mu": [numerators(mu) for mu in dual.mu],
    }


def read_dual(document: dict[str, Any]) -> AffineDual:
    scale = 1 << DUAL_BITS
    bounds = [(Q(lo), Q(hi)) for lo, hi in document["cell"]]
    cell = Cell(
        (bounds[0][0], bounds[1][0], bounds[2][0]), (bounds[0][1], bounds[1][1], bounds[2][1])
    )
    lam = tuple(Q(value, scale) for value in document["lambda"])
    mu = [tuple(Q(value, scale) for value in values) for values in document["mu"]]
    return AffineDual(cell, lam, (mu[0], mu[1], mu[2]))


DROPPED_PAIRS = frozenset({(2, 3), (9, 11)})


def _corner_gap(
    centres: Sequence[tuple[Q, Q]],
    pair: tuple[int, int],
    corner: tuple[Q, Q],
    sign: int,
    normal: tuple[Q, Q],
) -> Q:
    """Owner-axis corner gap `sign n.(c_other + corner - c_owner) - 1/2`."""
    owner, other = pair
    dx = centres[other - 1][0] + corner[0] - centres[owner - 1][0]
    dy = centres[other - 1][1] + corner[1] - centres[owner - 1][1]
    return sign * (normal[0] * dx + normal[1] * dy) - HALF


CORNER_CHOICES: tuple[tuple[int, int], ...] = ((1, 1), (1, -1), (-1, 1), (-1, -1))


def _corner(aux: dict[str, Any], label: int, choice: tuple[int, int]) -> tuple[Any, Any]:
    """Corner offset `(s1 a1 + s2 a2) / 2` of square `label` in its own axes."""
    first, second = (aux[name] for name in AXES[square_class(label)])
    return (
        HALF * (choice[0] * first[0] + choice[1] * second[0]),
        HALF * (choice[0] * first[1] + choice[1] * second[1]),
    )


def _option_margin(
    centres: Sequence[tuple[Any, Any]],
    lifts: Sequence[dict[int, Any]],
    vector: Sequence[Q],
    pair: tuple[int, int],
    *,
    feature: tuple[int, tuple[Any, Any], tuple[Any, Any]],
    curvature: Q,
) -> Any:
    """`g + sum_j |d_j g| r_j + K/2` for one corner gap, in any arithmetic.

    `feature = (sign, normal, corner)` with `pair = (owner, other)`; the gradient is
    exact: centres move the projection, the owner angle rotates the normal and the
    other angle rotates the corner.
    """
    owner, other = pair
    sign, (nx, ny), corner = feature
    dx = centres[other - 1][0] + corner[0] - centres[owner - 1][0]
    dy = centres[other - 1][1] + corner[1] - centres[owner - 1][1]
    gradient: dict[int, Any] = {
        column(other, "x"): sign * nx,
        column(other, "y"): sign * ny,
        column(owner, "x"): -sign * nx,
        column(owner, "y"): -sign * ny,
        column(owner, "angle"): sign * (-ny * dx + nx * dy),
        column(other, "angle"): sign * (-nx * corner[1] + ny * corner[0]),
    }
    linear: Any = Q(0)
    for lift, radius in zip(lifts, vector, strict=True):
        shared = [place for place in lift if place in gradient]
        if shared:
            value: Any = Q(0)
            for place in shared:
                value = value + gradient[place] * lift[place]
            linear = linear + _magnitude(value) * radius
    gap = sign * (nx * dx + ny * dy) - HALF
    return gap + linear + curvature / 2


def unavailable_option_audit(
    family: Family,
    box: Sequence[tuple[Q, Q]],
    radii: dict[str, Q],
    *,
    largest_corner: bool = False,
    enclosure: Enclosure | None = None,
) -> dict[str, Any]:
    """C6: one corner gap of every unavailable option stays negative on the rectangle.

    For each of the 125 unavailable owner-axis options of the 19 retained pairs, the
    corner of the other square with the smallest gap at `x*(0)` is chosen, and
    `g(x*(w)) + sum_j |d_j g(x*(w))| r_j + K/2 < 0` is checked at the eight vertices:
    exactly at the midpoint, and with an enclosure also as the upper end of its
    outward interval over the root box. `g` is affine in `w` and the derivative sum is
    a sum of absolute values of affine functions, so the margin is convex in `w` and
    its maximum is at a vertex. `K` is the owner's pair bound of C7. `largest_corner` is
    the C12 control: the corner with the largest gap must be refused.
    """
    vertices = box_vertices(box)
    vector = [radii[name] for name in family.names]
    entries: list[tuple[Q, dict[str, Any]]] = []
    for option in option_manifest():
        left, right = int(option["left"]), int(option["right"])
        if option["kind"] == "identity" or (left, right) in DROPPED_PAIRS:
            continue
        owner = int(option["owner"])
        other = right if owner == left else left
        pair = (owner, other)
        # The manifest's sign orients the pair displacement right - left; seen from the
        # owner it orients other - owner, which flips when the owner is the right square.
        sign = int(option["sign"]) if owner == left else -int(option["sign"])

        normal = tuple(Q(value) for value in family.aux[option["axis"]])
        base = [
            _corner_gap(
                family.centres,
                pair,
                _corner(family.aux, other, choice),
                sign,
                (normal[0], normal[1]),
            )
            for choice in CORNER_CHOICES
        ]
        pick = (max if largest_corner else min)(range(4), key=base.__getitem__)
        (ox, oy), (px, py) = (
            position_box(family, radii, owner, enclosure),
            position_box(family, radii, other, enclosure),
        )
        rho = sqrt_upper((ox + px) ** 2 + (oy + py) ** 2)
        squared = _separation_squared(family, enclosure, vertices, pair)
        curvature = pair_curvature(
            sqrt_upper(squared) + rho,
            rho,
            radii[f"omega{owner}"],
            radii[f"omega{other}"],
            INVERSE_ROOT2_UPPER,
        )
        margins: list[Q] = []
        for vertex in vertices:
            exact = _option_margin(
                moved_centres(family, vertex),
                family.lifts,
                vector,
                pair,
                feature=(
                    sign,
                    (normal[0], normal[1]),
                    _corner(family.aux, other, CORNER_CHOICES[pick]),
                ),
                curvature=curvature,
            )
            margin = Q(exact)
            if enclosure is not None:
                outward = _option_margin(
                    shifted_centres(enclosure.centres, enclosure.aux["v"], vertex),
                    enclosure.lifts,
                    vector,
                    pair,
                    feature=(
                        sign,
                        enclosure.aux[option["axis"]],
                        _corner(enclosure.aux, other, CORNER_CHOICES[pick]),
                    ),
                    curvature=curvature,
                )
                margin = max(margin, _upper(outward))
            margins.append(margin)
        worst = max(margins)
        entries.append(
            (
                worst,
                {
                    "pair": [left, right],
                    "owner": owner,
                    "axis": option["axis"],
                    "sign": int(option["sign"]),
                    "corner": pick,
                    "base_gap_decimal": decimal(base[pick], 12),
                    "worst_margin_decimal": decimal(worst, 12),
                    "worst_vertex": [
                        _fraction_string(value) for value in vertices[margins.index(worst)]
                    ],
                },
            )
        )
    ranked = [entry for _, entry in sorted(entries, key=lambda item: -item[0])]
    negative = sum(margin < 0 for margin, _ in entries)
    return {
        "options": len(entries),
        "strictly_negative": negative,
        "over_root_box": enclosure is not None,
        "least_negative": ranked[:8],
        "margins_sha256": _sha256_json(
            [
                [
                    entry["pair"],
                    entry["owner"],
                    entry["axis"],
                    entry["sign"],
                    _fraction_string(margin),
                ]
                for margin, entry in entries
            ]
        ),
        "passed": len(entries) == 125 and negative == 125,
    }


def tiling_audit(cells: Sequence[Cell], box: Sequence[tuple[Q, Q]]) -> bool:
    """The cells lie in the box, have pairwise disjoint interiors and fill its volume."""

    def volume(lo: Point, hi: Point) -> Q:
        return (hi[0] - lo[0]) * (hi[1] - lo[1]) * (hi[2] - lo[2])

    inside = all(
        box[k][0] <= cell.lo[k] < cell.hi[k] <= box[k][1] for cell in cells for k in range(3)
    )
    disjoint = all(
        any(first.hi[k] <= second.lo[k] or second.hi[k] <= first.lo[k] for k in range(3))
        for first, second in itertools.combinations(cells, 2)
    )
    total = sum((volume(cell.lo, cell.hi) for cell in cells), Q(0))
    full = volume((box[0][0], box[1][0], box[2][0]), (box[0][1], box[1][1], box[2][1]))
    return inside and disjoint and total == full


def replay_certificates(
    matrix: AffineMatrix,
    curvature: Sequence[Q],
    radii: Sequence[Q],
    *,
    names: Sequence[str],
    documents: Sequence[dict[str, Any]],
    box: Sequence[tuple[Q, Q]],
    deviation: Sequence[Q] | None = None,
) -> dict[str, Any]:
    """C8 and C9 again from serialised certificates alone: no LP, exact throughout."""
    failures: list[str] = []
    worst: tuple[Q, str] | None = None
    seen: set[str] = set()
    for document in documents:
        label = str(document["direction"])
        name, sign = label[1:], 1 if label[0] == "+" else -1
        duals = [read_dual(item) for item in document["cells"]]
        if label in seen or not duals or not tiling_audit([d.cell for d in duals], box):
            failures.append(label)
            continue
        seen.add(label)
        for dual in duals:
            verdict = evaluate_dual(
                matrix,
                curvature,
                radii,
                coordinate=names.index(name),
                sign=sign,
                dual=dual,
                deviation=deviation,
            )
            if not verdict["passed"] or verdict["ratio"] is None:
                failures.append(label)
                break
            if worst is None or verdict["ratio"] > worst[0]:
                worst = (verdict["ratio"], label)
    expected = {f"{'+' if sign > 0 else '-'}{name}" for name in names for sign in (1, -1)}
    return {
        "directions": len(seen),
        "cells": sum(len(document["cells"]) for document in documents),
        "failures": failures,
        "complete": seen == expected,
        "worst_ratio": None if worst is None else _fraction_string(worst[0]),
        "worst_direction": None if worst is None else worst[1],
        "passed": not failures and seen == expected,
    }


def n11_ratio_replay(*, branches: Sequence[int] | None = None) -> dict[str, Any]:
    """C12: n11's focused receipt through this module's curvature and ratio routines.

    The duals, residual bounds, radii and radical bounds are n11's own (the retained
    `local-dual-residual` objects, SHA-256 checked); the separation and velocity
    bounds are computed exactly as n11's consumer does. The row curvature uses
    `pair_curvature` and `wall_curvature` and the margin uses `ratio_test`, so the
    maximum must equal the `worst_dual_ratio` of n11's `local-isolation` receipt.
    """
    from cases.trump11 import isolation_radius  # noqa: PLC0415
    from devtools import check_n11_optimality_local_dual as n11_dual  # noqa: PLC0415
    from devtools import check_n11_optimality_local_isolation as n11_local  # noqa: PLC0415

    documents: dict[str, Any] = {}
    for role, key in N11_OBJECTS.items():
        raw = gzip.decompress(
            (N11_RECEIPTS / "local-dual-residual/objects" / f"{key}.gz").read_bytes()
        )
        if hashlib.sha256(raw).hexdigest() != key:
            raise ValueError(f"n11 {role} object does not match its digest")
        documents[role] = json.loads(raw)
    proposal, focused = documents["weighted"], documents["focused"]
    radii = [Q(value) for value in focused["radii"]]
    denominator, _ = n11_dual.validate_scales(proposal)
    receipts = n11_dual.validate_branch_inventory(proposal)
    lo, hi, _ = n11_dual.root_interval()
    witness = isolation_radius.load_witness()
    functions = isolation_radius.elementary_functions(witness, Q(1, 64))
    root2, inverse_root2 = Q(proposal["sqrt2_upper"]), Q(proposal["inverse_sqrt2_upper"])
    separations: dict[tuple[int, int], tuple[Q, Q]] = {}

    def curvature(function: Any) -> Q:
        if function.kind == "wall":
            return wall_curvature(radii[3 * function.subject[0] + 2], inverse_root2)
        first, second, owner = function.subject[:3]
        other = second if owner == first else first
        if (first, second) not in separations:
            dx = witness.centres[first][0] - witness.centres[second][0]
            dy = witness.centres[first][1] - witness.centres[second][1]
            squared = n11_dual.field_interval(dx * dx + dy * dy, lo, hi)[1]
            vx = radii[3 * first] + radii[3 * second]
            vy = radii[3 * first + 1] + radii[3 * second + 1]
            separations[first, second] = (
                n11_local.radical_upper(squared) + 2 * root2 * Q(1, 64),
                n11_local.radical_upper(vx * vx + vy * vy),
            )
        separation, rho = separations[first, second]
        return pair_curvature(
            separation, rho, radii[3 * owner + 2], radii[3 * other + 2], inverse_root2
        )

    row_curvature: dict[Any, Q] = {}
    for function in functions:
        if function.value.is_zero():
            key = n11_local.signature(function.gradient)
            row_curvature[key] = max(row_curvature.get(key, Q(0)), curvature(function))
    wanted = set(range(128) if branches is None else branches)
    largest = max(radii)
    worst: tuple[Q, int, int, int] | None = None
    checked = 0
    for branch in witness.branches:
        if branch["branch"] not in wanted:
            continue
        bounds = [
            row_curvature[n11_local.signature(row.coefficients)] for row in branch["rows"]
        ]
        for item in receipts[branch["branch"]]["certificates"]:
            mass = sum(
                (
                    Q(weight, denominator) * bound
                    for weight, bound in zip(item["coefficients"], bounds, strict=True)
                ),
                Q(0),
            )
            below, ratio = ratio_test(
                radii[item["coordinate"]], Q(item["residual_upper"]), largest, mass
            )
            if not below or ratio is None:
                raise ValueError("n11 replay: a certificate fails the ratio test")
            checked += 1
            if worst is None or ratio > worst[0]:
                worst = (ratio, branch["branch"], item["coordinate"], item["sign"])
    if worst is None:
        raise ValueError("n11 replay checked no certificate")
    receipt = json.loads((N11_RECEIPTS / "local-isolation/result.json").read_text())
    expected = Q(receipt["worst_dual_ratio"])
    location = {"branch": worst[1], "coordinate": worst[2], "sign": worst[3]}
    return {
        "branches": sorted(wanted),
        "certificates_checked": checked,
        "worst_ratio": _fraction_string(worst[0]),
        "worst_ratio_decimal": decimal(worst[0], 12),
        "worst_location": location,
        "receipt_worst_ratio_decimal": decimal(expected, 12),
        "receipt_worst_location": receipt["worst_coordinate"],
        "reproduced": worst[0] == expected and location == receipt["worst_coordinate"],
    }


def negative_vertex_control(dual: AffineDual) -> AffineDual:
    """C12: lower one multiplier so that its smallest vertex value is `-1/10^6`."""
    index = max(range(len(dual.lam)), key=dual.lam.__getitem__)
    half = dual.cell.half
    spread = sum((half[k] * abs(dual.mu[k][index]) for k in range(3)), Q(0))
    lam = list(dual.lam)
    lam[index] = spread - Q(1, 10**6)
    return replace(dual, lam=tuple(lam))


def ratio_controls(
    target: Family,
    box: Sequence[tuple[Q, Q]],
    matrix: AffineMatrix,
    outcome: CoordinateOutcome,
    *,
    n11: bool,
    radius: Q = DECLARED_RADIUS,
    enclosure: Enclosure | None = None,
    deviation: Sequence[Q] | None = None,
) -> list[dict[str, Any]]:
    """C12 controls; `control_passed` means the mutation was refused, or n11 reproduced.

    Flipped tau branch (C3), perturbed slope (C4), negative vertex value (C8), a radius
    above the ratio limit (C9, on the worst direction's certificates) and the n11
    replay (C9).
    """
    controls: list[dict[str, Any]] = []
    flipped = build_family(target.t, target.beta, branches={**FACE_BRANCHES, (5, 7): 1})
    branch = sign_branch_audit(flipped, box)
    controls.append(
        {
            "control": "flipped-tau-branch-5/7",
            "check": "C3",
            "control_passed": not branch["passed"],
            "failures": branch["failures"],
        }
    )
    _, perturbed = affine_audit(target, box, perturb=True)
    controls.append(
        {
            "control": "perturbed-b-slope",
            "check": "C4",
            "control_passed": not perturbed["passed"],
            "failed_checks": [name for name, ok in perturbed["checks"].items() if not ok],
        }
    )
    coordinate = target.names.index(outcome.name)
    radii = dict.fromkeys(target.names, radius)
    curvature, _ = curvature_audit(target, box, radii, enclosure)
    vector = [radii[name] for name in target.names]
    dual = outcome.certificates[0][0]
    negative = evaluate_dual(
        matrix,
        curvature,
        vector,
        coordinate=coordinate,
        sign=outcome.sign,
        dual=negative_vertex_control(dual),
        deviation=deviation,
    )
    controls.append(
        {
            "control": "negative-vertex-dual",
            "check": "C8",
            "direction": outcome.label,
            "vertex_min_decimal": decimal(negative["vertex_min"], 12),
            "control_passed": not negative["nonnegative"] and not negative["passed"],
        }
    )
    # The ratio of a fixed certificate grows linearly with a uniform radius, so this
    # multiple puts the worst direction's ratio near two: above the limit by design.
    worst_here = max(verdict["ratio"] for _, verdict in outcome.certificates)
    control_radius = radius * max(2, math.ceil(2 / worst_here))
    wide = dict.fromkeys(target.names, control_radius)
    wide_curvature, _ = curvature_audit(target, box, wide, enclosure)
    wide_vector = [wide[name] for name in target.names]
    verdicts = [
        evaluate_dual(
            matrix,
            wide_curvature,
            wide_vector,
            coordinate=coordinate,
            sign=outcome.sign,
            dual=item,
            deviation=deviation,
        )
        for item, _ in outcome.certificates
    ]
    failing = sum(not verdict["passed"] for verdict in verdicts)
    worst = max((v["ratio"] for v in verdicts if v["ratio"] is not None), default=None)
    controls.append(
        {
            "control": "radius-above-limit",
            "check": "C9",
            "direction": outcome.label,
            "radius": _fraction_string(control_radius),
            "cells_failing": failing,
            "cells": len(verdicts),
            "worst_ratio_decimal": None if worst is None else decimal(worst, 12),
            "control_passed": failing > 0,
        }
    )
    if n11:
        replay = n11_ratio_replay()
        controls.append(
            {
                "control": "n11-focused-replay",
                "check": "C9",
                **replay,
                "control_passed": replay["reproduced"],
            }
        )
    return controls


def ratio_certify(
    t: Q,
    beta: Q,
    *,
    box: Sequence[tuple[Q, Q]] = DECLARED_BOX,
    radius: Q = DECLARED_RADIUS,
    only: Sequence[tuple[str, int]] | None = None,
    controls: bool = True,
    n11: bool = True,
    root_radii: tuple[Q, Q] | None = None,
    progress: Callable[[str], None] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """C3, C4, C6, C7, C8, C9 and the C12 controls over the slider box.

    The certificates are exact at the root-box midpoint `(t, beta)`. With `root_radii`
    (the H-255 inclusion radii) the curvature constants, C3 and C6 also hold over the
    whole root box and every dual's residual carries the root-box term of C8(i).
    A box outside the declared tau branches (C3) is refused with `ValueError` before
    the other items run. Returns the receipt body and the exact certificates (one
    document per direction).
    """
    timings: dict[str, float] = {}
    started = time.monotonic()
    box = slider_box([bound for interval in box for bound in interval])
    family = build_family(t, beta)
    branches = sign_branch_audit(family, box)
    if not branches["passed"]:
        raise ValueError(
            "slider box leaves the declared tau branch of face "
            + ", ".join(branches["failures"])
        )
    matrix, affine = affine_audit(family, box)
    enclosure = None if root_radii is None else root_enclosure(family, root_radii)
    deviation: tuple[Q, ...] | None = None
    skipped = {"passed": False, "skipped": "midpoint only: no root-box radii given"}
    root_audit: dict[str, Any] = skipped
    symbolic: dict[str, Any] = skipped
    if enclosure is not None:
        symbolic = symbolic_affine_audit(family, matrix)
        deviation, root_audit = root_box_audit(family, enclosure, box, matrix)
    slides = slide_invariance_audit(family)
    spanning = spanning_audit()
    roster = roster_binding_audit(family)
    stress = stress_audit(family, box)
    radii = dict.fromkeys(family.names, radius)
    curvature, curvature_detail = curvature_audit(family, box, radii, enclosure)
    options = unavailable_option_audit(family, box, radii, enclosure=enclosure)
    timings["c3_c4_c6_c7"] = time.monotonic() - started
    stage = time.monotonic()
    system = float_system(matrix, len(family.names))
    vector = [radii[name] for name in family.names]
    wanted = (
        tuple(only)
        if only is not None
        else tuple((name, sign) for name in family.names for sign in (1, -1))
    )
    outcomes: list[CoordinateOutcome] = []
    for name, sign in wanted:
        outcome = certify_coordinate(
            matrix,
            system,
            curvature,
            vector,
            names=family.names,
            name=name,
            sign=sign,
            box=box,
            deviation=deviation,
        )
        outcomes.append(outcome)
        if progress is not None:
            record = outcome_record(outcome)
            ratio = record.get("worst_ratio_decimal")
            progress(f"{record['direction']}: cells {record['cells']} ratio {ratio}")
    timings["c8_c9"] = time.monotonic() - stage
    stage = time.monotonic()
    certificates = [
        {"direction": o.label, "cells": [dual_document(dual) for dual, _ in o.certificates]}
        for o in outcomes
    ]
    replay = replay_certificates(
        matrix,
        curvature,
        vector,
        names=family.names,
        documents=json.loads(json.dumps(certificates)),
        box=box,
        deviation=deviation,
    )
    timings["c8_c9_replay"] = time.monotonic() - stage
    records = [outcome_record(outcome) for outcome in outcomes]
    tiled = all(tiling_audit([dual.cell for dual, _ in o.certificates], box) for o in outcomes)
    passed_all = all(o.passed for o in outcomes) and len(outcomes) == len(wanted)
    ranked = sorted(
        (o for o in outcomes if o.certificates),
        key=lambda o: -max(v["ratio"] for _, v in o.certificates),
    )
    stage = time.monotonic()
    control_rows = (
        ratio_controls(
            family,
            box,
            matrix,
            ranked[0],
            n11=n11,
            radius=radius,
            enclosure=enclosure,
            deviation=deviation,
        )
        if controls and ranked
        else []
    )
    if controls:
        restored = slide_invariance_audit(family, restore=frozenset({(9, 11)}))
        control_rows.append(
            {
                "control": "non-tight-row-9/11-restored",
                "check": "C2",
                "not_invariant": restored["not_invariant"],
                "control_passed": not restored["passed"],
            }
        )
        flipped = unavailable_option_audit(family, box, radii, largest_corner=True)
        control_rows.append(
            {
                "control": "largest-corner-choice",
                "check": "C6",
                "strictly_negative": flipped["strictly_negative"],
                "control_passed": not flipped["passed"],
            }
        )
    timings["c12_controls"] = time.monotonic() - stage
    worst = records[[o.label for o in outcomes].index(ranked[0].label)] if ranked else None
    checks = {
        "c3_sign_branches": branches["passed"],
        "c4_affine_structure": affine["passed"],
        "c4_symbolic_in_root_parameters": symbolic["passed"],
        "c2_slide_invariance": slides["passed"],
        "c10_spanning": spanning["passed"],
        "c1_roster_binding": roster["passed"],
        "c11_stress_on_the_box": stress["passed"],
        "c8i_root_box": root_audit["passed"],
        "c8_c9_every_direction": passed_all,
        "c8_cells_tile_the_box": tiled,
        "c8_c9_replayed_from_certificates": replay["passed"]
        and replay["worst_ratio"] == (worst or {}).get("worst_ratio"),
        "c6_unavailable_options": options["passed"],
        "c12_controls": bool(control_rows)
        and all(row["control_passed"] for row in control_rows),
    }
    timings["total"] = time.monotonic() - started
    body = {
        "point": {
            "t": _fraction_string(t),
            "beta": _fraction_string(beta),
            "t_decimal": decimal(t),
            "beta_decimal": decimal(beta),
        },
        "slider_box": {
            name: [_fraction_string(lo), _fraction_string(hi)]
            for name, (lo, hi) in zip(SLIDER_PARAMETERS, box, strict=True)
        },
        "radius": {"uniform": _fraction_string(radius), "coordinates": len(family.names)},
        "c3_sign_branches": branches,
        "c4_affine_structure": affine,
        "c4_symbolic": symbolic,
        "c2_slide_invariance": slides,
        "c10_spanning": spanning,
        "c1_roster_binding": roster,
        "c11_stress": stress,
        "c8i_root_box": root_audit,
        "c6_unavailable_options": options,
        "c7_curvature": curvature_detail,
        "c8_c9_replay": replay,
        "c8_c9": {
            "directions": len(wanted),
            "passed": passed_all,
            "total_cells": sum(len(o.certificates) for o in outcomes),
            "cells_per_direction": {o.label: len(o.certificates) for o in outcomes},
            "worst": worst,
            "largest_ratios": [
                {
                    "direction": o.label,
                    "ratio_decimal": decimal(max(v["ratio"] for _, v in o.certificates), 12),
                    "cells": len(o.certificates),
                }
                for o in ranked[:12]
            ],
            "results": records,
        },
        "c12_controls": control_rows,
        "open": [
            (
                "C2 at x*(0): tightness of the 27 identity options and anchors at the root "
                "is H-257's accepted result, not re-proved here (slide invariance is)"
            ),
            "C5 is implied by the C8 duals (residual below one), not checked separately",
            "Lemmas 1 to 6 are the recipe's hand proofs, not machine-checked",
        ],
        "checks": checks,
        "passed": all(checks.values()),
        "timing_seconds": timings,
    }
    return body, certificates


def source_digests() -> dict[str, str]:
    return {path: hashlib.sha256((REPO / path).read_bytes()).hexdigest() for path in SOURCES}


def certify(
    t: Q,
    b: Q,
    *,
    control: str | None = None,
    progress: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    """All mechanical checks at one point; with `control`, on the mutated model."""
    timings: dict[str, float] = {}
    started = time.monotonic()
    target = build_model(t, b)
    model = target if control is None else mutate(target, control)
    timings["build"] = time.monotonic() - started
    stage = time.monotonic()
    weights = weight_audit(target)
    kernel = kernel_audit(model)
    timings["kernel"] = time.monotonic() - stage
    stage = time.monotonic()
    duals = (
        dual_audit(model, fail_fast=control is not None, progress=progress)
        if kernel["passed"]
        else {"passed": False, "skipped": "kernel claim failed; duals not attempted"}
    )
    timings["duals"] = time.monotonic() - stage
    stage = time.monotonic()
    owners = owner_alternative_audit(target)
    timings["owner_alternatives"] = time.monotonic() - stage
    stage = time.monotonic()
    controls = [run_control(target, name) for name in CONTROLS] if control is None else []
    timings["controls"] = time.monotonic() - stage
    checks = {
        "weights": weights["passed"],
        "kernel": kernel["passed"],
        "duals": duals["passed"],
        "owner_alternatives": owners["passed"],
        "controls_refused": all(row["refused"] for row in controls) and control is None,
    }
    timings["total"] = time.monotonic() - started
    return {
        "point": {
            "t": _fraction_string(t),
            "b": _fraction_string(b),
            "t_decimal": decimal(t),
            "b_decimal": decimal(b),
            "side_decimal": decimal(target.side),
        },
        "control": control,
        "weights": weights,
        "kernel": kernel,
        "duals": duals,
        "owner_alternatives": owners,
        "controls": controls,
        "checks": checks,
        "passed": all(checks.values()),
        "timing_seconds": timings,
    }


def read_point(raw: bytes) -> tuple[tuple[Q, Q], tuple[Q, Q]]:
    """The exp-237 midpoint and inclusion radii from root-certificate bytes."""
    document = json.loads(raw, object_pairs_hook=_object_unique)
    midpoint = tuple(Q(value) for value in document["box"]["midpoint"])
    radii = tuple(Q(value) for value in document["inclusion_bounds"])
    if len(midpoint) != 2 or len(radii) != 2:
        raise ValueError("root box must have two dimensions")
    return (midpoint[0], midpoint[1]), (radii[0], radii[1])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Exact first-order parts of the n17 local-minimum checker (H-261)."
    )
    parser.add_argument("root_certificate", type=Path, nargs="?", default=ROOT_CERTIFICATE)
    parser.add_argument("--output", type=Path, help="write the JSON receipt here")
    parser.add_argument("--control", choices=CONTROLS, help="run one refusal control")
    parser.add_argument("--progress", action="store_true", help="report each direction")
    parser.add_argument(
        "--ratio",
        action="store_true",
        help="run the ratio test over the declared slider box (C3, C4, C7, C8, C9, C12)",
    )
    parser.add_argument("--radius", type=Q, default=DECLARED_RADIUS, help="uniform radius")
    parser.add_argument(
        "--box",
        nargs=6,
        type=Q,
        metavar=("A_LO", "A_HI", "B_LO", "B_HI", "Z_LO", "Z_HI"),
        help="ratio mode: the slider box in (a, b, z), rationals (default B_W)",
    )
    parser.add_argument("--certificates", type=Path, help="write the exact cell duals here")
    parser.add_argument("--no-n11", action="store_true", help="skip the n11 replay control")
    parser.add_argument(
        "--midpoint-only",
        action="store_true",
        help="ratio mode: skip the root-box items (partial run; the receipt fails)",
    )
    parser.add_argument(
        "--direction",
        action="append",
        type=_direction,
        help="ratio mode: only this signed coordinate, as NAME:SIGN (repeatable; partial run)",
    )
    args = parser.parse_args(argv)
    if args.ratio:
        return ratio_main(args)
    try:
        require_retained_path(args.root_certificate, FROZEN_ROOT_REF)
        raw = _read_limited(args.root_certificate)
        midpoint, radii = read_point(raw)
        result = certify(
            *midpoint,
            control=args.control,
            progress=(lambda line: print(line, flush=True)) if args.progress else None,
        )
    except (ValueError, OSError, KeyError, IndexError, TypeError, ExactLPError) as error:
        print(json.dumps({"schema": SCHEMA, "passed": False, "error": str(error)}))
        return 2
    receipt = {
        "schema": SCHEMA,
        "scope": (
            "mechanical parts of H-261 only: kernel, exact coordinate duals, owner "
            "alternative margins at the rational point; no curvature bound, ratio test, "
            "Taylor box check, slider-domain uniformity, or root transfer"
        ),
        "inputs": {
            "root_certificate": str(args.root_certificate),
            "root_certificate_sha256": hashlib.sha256(raw).hexdigest(),
            "root_certificate_git_ref": FROZEN_ROOT_REF,
            "root_box_radii": [_fraction_string(value) for value in radii],
            "sources_sha256": source_digests(),
        },
        **result,
    }
    encoded = json.dumps(receipt, sort_keys=True, indent=1)
    if args.output is not None:
        args.output.write_text(encoded + "\n")
    summary = {
        "schema": SCHEMA,
        "passed": receipt["passed"],
        "checks": receipt["checks"],
        "control": receipt["control"],
        "largest_dual": receipt["duals"].get("largest", [])[:1],
        "timing_seconds": receipt["timing_seconds"],
    }
    print(json.dumps(summary, sort_keys=True))
    return 0 if receipt["passed"] else 1


def core_stress_blob() -> str:
    """Git blob id of the imported core-stress source, to compare with `CORE_STRESS_BLOB`."""
    data = (REPO / "packing/devtools/check_n17_core_stress.py").read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data, usedforsecurity=False).hexdigest()


def _direction(text: str) -> tuple[str, int]:
    name, _, sign = text.partition(":")
    if sign not in {"1", "-1", "+1"}:
        raise argparse.ArgumentTypeError("direction must be NAME:1 or NAME:-1")
    return name, int(sign)


def _check_radius(radius: Q) -> None:
    if not 0 < radius < Q(1, 64):
        raise ValueError("radius must lie in (0, 1/64)")


def ratio_main(args: argparse.Namespace) -> int:
    """`--ratio`: the slider-box ratio test receipt; exit 0 only if every check passes."""
    try:
        require_retained_path(args.root_certificate, FROZEN_ROOT_REF)
        raw = _read_limited(args.root_certificate)
        midpoint, root_radii = read_point(raw)
        _check_radius(args.radius)
        box = DECLARED_BOX if args.box is None else slider_box(args.box)
        body, certificates = ratio_certify(
            *midpoint,
            box=box,
            radius=args.radius,
            n11=not args.no_n11,
            only=args.direction,
            root_radii=None if args.midpoint_only else root_radii,
            progress=(lambda line: print(line, flush=True)) if args.progress else None,
        )
    except (ValueError, OSError, KeyError, IndexError, TypeError) as error:
        print(json.dumps({"schema": RATIO_SCHEMA, "passed": False, "error": str(error)}))
        return 2
    blob = core_stress_blob()
    certificate_bytes = json.dumps(certificates, sort_keys=True).encode()
    receipt = {
        "schema": RATIO_SCHEMA,
        "scope": (
            "H-261 recipe items C1 (roster binding), C3, C4, C6, C7, C8 (with the root-box "
            "residual), C9, C10, C11, C12 and the slide half of C2 over the declared slider "
            "box, certificates exact at the exp-237 root-box midpoint; planning evidence, "
            "not an H-261 verdict"
        ),
        "inputs": {
            "root_certificate": str(args.root_certificate),
            "root_certificate_sha256": hashlib.sha256(raw).hexdigest(),
            "root_certificate_git_ref": FROZEN_ROOT_REF,
            "root_box_radii": [_fraction_string(value) for value in root_radii],
            "core_stress_commit": CORE_STRESS_COMMIT,
            "core_stress_blob": blob,
            "core_stress_matches_commit": blob == CORE_STRESS_BLOB,
            "sources_sha256": source_digests(),
            "certificates_sha256": hashlib.sha256(certificate_bytes).hexdigest(),
        },
        **body,
    }
    receipt["checks"]["core_stress_matches_commit"] = blob == CORE_STRESS_BLOB
    receipt["passed"] = all(receipt["checks"].values())
    if args.certificates is not None:
        args.certificates.write_bytes(certificate_bytes + b"\n")
    encoded = json.dumps(receipt, sort_keys=True, indent=1)
    if args.output is not None:
        args.output.write_text(encoded + "\n")
    summary = {
        "schema": RATIO_SCHEMA,
        "passed": receipt["passed"],
        "slider_box": receipt["slider_box"],
        "checks": receipt["checks"],
        "worst": {
            key: (receipt["c8_c9"]["worst"] or {}).get(key)
            for key in ("direction", "worst_ratio_decimal", "worst_cell", "cells")
        },
        "total_cells": receipt["c8_c9"]["total_cells"],
        "timing_seconds": receipt["timing_seconds"],
    }
    print(json.dumps(summary, sort_keys=True))
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
