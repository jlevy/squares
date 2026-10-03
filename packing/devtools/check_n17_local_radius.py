"""The n17 local theorem at larger, per-coordinate radii: a wrapper over H-261's checker.

`check_n17_local_minimum --ratio` certifies the recipe of
`docs/project/reviews/review-2026-10-02-n17-local-theorem-recipe.md` at one uniform
radius. Its ratio `M_j / (2 (r_j - eps R))` sets a dual mass `M_j = sum_i lambda_i K_i`
against the radius, and every curvature constant `K_i` (C7, n11's per-pair bound) is a
quadratic form in the radii, so at a uniform radius the ratio grows linearly with it.
The recipe's theorem is stated for a radius vector. This module asks how far a vector
can reach, calling that module's functions unchanged:

- `scan`: at each uniform radius, the C6 option margins (exact, over the root box), the
  exp-248 certificates evaluated at that radius (exact), and an exact floor under every
  certificate of the recipe's form. At a point `w` the floor is the dual of the point
  program: a rational `z` with `A_N(w) z <= K` row by row gives
  `sum_i lambda_i K_i >= -s z_j + z . e` for every `lambda >= 0` with
  `lambda^T A_N(w) = -s e_j + e`, so a cell containing `w` whose dual has residual
  `|e|_1 <= eps` has mass at least `-s z_j - |z|_inf eps`.
- `shape`: a floating-point proposal of a radius vector with every coordinate at least
  `T` (positions at least `position_share * T` if asked), the least fixed point of
  `r = max(T, F(r) / theta)`, where `F_j(r)` is half the largest point-program mass of
  coordinate `j` over the box's vertices and centre. `F` is monotone, so the iteration
  rises to that fixed point when some vector above `T` passes the point test with
  factor `theta`, and grows without bound otherwise. The settled vector is rounded up to
  multiples of `T / 64` and tested once more; `ratio` decides it exactly.
- `ratio`: every item of `ratio_certify` at a declared radius vector, exact, with the
  certificates written beside the receipt: C1 to C4, C6 to C11, and the C12 controls
  other than the n11 replay, which no radius changes.
- `slide`: H-268's slide coverage at a uniform radius, through the unchanged `run`, with
  the module's `build_scene` held at that radius for the duration of the call.
- `bounds`: a floating-point model of finer curvature lemmas for one direction. Each
  row's exact second-order part, a corner of the other square against the owner's face,
  is `1/2 [-1/2 w_o^2 - 2|f| w_o w_p + |f| w_p^2] + w_o t_o . (dc_p - dc_o)` with
  `f = n_o . kappa`, and `1/2 |f| w^2` for a wall. The checker's per-row constants are
  set against that part bounded row by row with its sign, and against the whole
  weighted sum bounded entrywise, where rows can cancel. Third-order terms are left out,
  so it bounds nothing; it says what a finer lemma could buy.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import time
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import linprog

from devtools import check_n17_local_minimum as local
from devtools import check_n17_slider_coverage as slide
from devtools.check_n17_endpoint_feasibility import FROZEN_ROOT_REF, require_retained_path
from devtools.check_n17_endpoint_features import PARALLEL_PAIRS, option_manifest

SCHEMA = "n17-local-radius/v1"
BOX_W_PRIME: tuple[tuple[Q, Q], ...] = (
    (Q(0), Q(1, 4)),
    (Q(-1, 2500), Q(1, 12)),
    (Q(-1, 8), Q(1, 16)),
)
EXP248_CERTIFICATES = (
    local.REPO
    / "packing/campaign/series/series-000-smoke-and-calibration/results"
    / "exp-248-n17-local-half-composition/run-002/certificates.json"
)
SCAN_RADII = (Q(1, 5000), Q(1, 2500), Q(1, 1024), Q(1, 512), Q(1, 256))
FLOOR_BITS = 40
SHAPE_DENOMINATOR = 64
SHAPE_STEPS = 80
SHAPE_CAP = 64.0
SHAPE_SETTLED = 1e-4

Point = tuple[Q, Q, Q]
Box = tuple[tuple[Q, Q], ...]
SparseRow = dict[int, Q]


def _text(value: Q) -> str:
    return str(value)


@dataclass(frozen=True)
class Setting:
    """The family at the exp-237 midpoint over one slider box, with its root-box residual."""

    family: local.Family
    box: Box
    matrix: local.AffineMatrix
    enclosure: local.Enclosure
    deviation: tuple[Q, ...]
    root_audit: dict[str, Any]
    affine: dict[str, Any]
    branches: dict[str, Any]

    @property
    def names(self) -> tuple[str, ...]:
        return self.family.names


def load_point() -> tuple[tuple[Q, Q], tuple[Q, Q]]:
    """The exp-237 midpoint and inclusion radii, read from the retained certificate."""
    require_retained_path(local.ROOT_CERTIFICATE, FROZEN_ROOT_REF)
    return local.read_point(local.ROOT_CERTIFICATE.read_bytes())


def build_setting(box: Sequence[tuple[Q, Q]]) -> Setting:
    """C3, C4 and C8(i) over the box; a box leaving a tau branch is refused here."""
    (t, beta), root_radii = load_point()
    checked = local.slider_box([bound for interval in box for bound in interval])
    family = local.build_family(t, beta)
    branches = local.sign_branch_audit(family, checked)
    if not branches["passed"]:
        raise ValueError(
            "slider box leaves a declared tau branch: " + str(branches["failures"])
        )
    matrix, affine = local.affine_audit(family, checked)
    enclosure = local.root_enclosure(family, root_radii)
    deviation, root_audit = local.root_box_audit(family, enclosure, checked, matrix)
    return Setting(family, checked, matrix, enclosure, deviation, root_audit, affine, branches)


def sample_points(box: Box) -> tuple[Point, ...]:
    """The box's eight vertices and its centre."""
    centre = tuple((lo + hi) / 2 for lo, hi in box)
    return (*local.box_vertices(box), (centre[0], centre[1], centre[2]))


def dense(rows: Sequence[SparseRow], width: int) -> np.ndarray:
    array = np.zeros((len(rows), width))
    for index, row in enumerate(rows):
        for position, value in row.items():
            array[index, position] = float(value)
    return array


def point_program(
    matrix: np.ndarray, weights: np.ndarray, coordinate: int, sign: int
) -> tuple[float, np.ndarray] | None:
    """`min K . lambda` over `lambda >= 0`, `lambda^T A = -s e_j`, and its dual `z`."""
    rows, width = matrix.shape
    target = np.zeros(width)
    target[coordinate] = -sign
    result = linprog(
        weights,
        A_eq=matrix.T,
        b_eq=target,
        bounds=[(0, None)] * rows,
        method="highs",
    )
    if result.status != 0:
        return None
    return float(result.fun), np.asarray(result.eqlin.marginals, dtype=float)


def exact_floor(
    rows: Sequence[SparseRow],
    curvature: Sequence[Q],
    dual: np.ndarray,
    coordinate: int,
    sign: int,
) -> tuple[Q, Q]:
    """`(-s z_j, |z|_inf)` for a rational `z` scaled until `A z <= K` holds exactly."""
    scale = 1 << FLOOR_BITS
    z = [Q(round(float(value) * scale), scale) for value in dual]

    def loads(vector: Sequence[Q]) -> list[Q]:
        return [sum((e * vector[c] for c, e in row.items()), Q(0)) for row in rows]

    worst = max(
        (load / bound for load, bound in zip(loads(z), curvature, strict=True)), default=Q(0)
    )
    if worst > 1:
        z = [value / worst for value in z]
    if any(load > bound for load, bound in zip(loads(z), curvature, strict=True)):
        raise ValueError("floor certificate is not dual feasible")
    return -sign * z[coordinate], max(abs(value) for value in z)


# ---------------------------------------------------------------------------
# scan: uniform radii
# ---------------------------------------------------------------------------


def certificate_ratios(
    setting: Setting, curvature: Sequence[Q], vector: Sequence[Q], documents: Sequence[Any]
) -> dict[str, Any]:
    """Every exp-248 cell dual evaluated exactly at the given radii; the largest ratio."""
    worst: tuple[Q, str] | None = None
    unbounded: list[str] = []
    failing: set[str] = set()
    for document in documents:
        label = str(document["direction"])
        name, sign = label[1:], 1 if label[0] == "+" else -1
        for item in document["cells"]:
            verdict = local.evaluate_dual(
                setting.matrix,
                curvature,
                vector,
                coordinate=setting.names.index(name),
                sign=sign,
                dual=local.read_dual(item),
                deviation=setting.deviation,
            )
            if not verdict["passed"]:
                failing.add(label)
            ratio = verdict["ratio"]
            if ratio is None:
                unbounded.append(label)
            elif worst is None or ratio > worst[0]:
                worst = (ratio, label)
    return {
        "worst_ratio_decimal": None if worst is None else local.decimal(worst[0], 12),
        "worst_direction": None if worst is None else worst[1],
        "directions_failing": len(failing),
        "unbounded": sorted(set(unbounded)),
    }


def floors(
    setting: Setting, curvature: Sequence[Q], vector: Sequence[Q]
) -> list[dict[str, Any]]:
    """Per signed coordinate, the largest exact point floor over the sample points."""
    names = setting.names
    weights = np.array([float(value) for value in curvature])
    exact_rows = [setting.matrix.at(point) for point in sample_points(setting.box)]
    arrays = [dense(rows, len(names)) for rows in exact_rows]
    records: list[dict[str, Any]] = []
    for index, name in enumerate(names):
        for sign in (1, -1):
            best: tuple[Q, Q, int] | None = None
            for place, (rows, array) in enumerate(zip(exact_rows, arrays, strict=True)):
                solved = point_program(array, weights, index, sign)
                if solved is None:
                    continue
                floor, size = exact_floor(rows, curvature, solved[1], index, sign)
                if best is None or floor > best[0]:
                    best = (floor, size, place)
            if best is None:
                raise ValueError(f"no coordinate dual for {name}:{sign}")
            records.append(
                {
                    "direction": f"{'+' if sign > 0 else '-'}{name}",
                    "floor_ratio": best[0] / (2 * vector[index]),
                    "z_size_decimal": local.decimal(best[1], 6),
                    "point": [_text(v) for v in sample_points(setting.box)[best[2]]],
                }
            )
    records.sort(key=lambda record: -record["floor_ratio"])
    return records


def scan(setting: Setting, radii: Sequence[Q]) -> list[dict[str, Any]]:
    documents = json.loads(EXP248_CERTIFICATES.read_text())
    results: list[dict[str, Any]] = []
    for radius in radii:
        started = time.monotonic()
        named = dict.fromkeys(setting.names, radius)
        curvature, detail = local.curvature_audit(
            setting.family, setting.box, named, setting.enclosure
        )
        options = local.unavailable_option_audit(
            setting.family, setting.box, named, enclosure=setting.enclosure
        )
        vector = [radius] * len(setting.names)
        replayed = certificate_ratios(setting, curvature, vector, documents)
        ranked = floors(setting, curvature, vector)
        results.append(
            {
                "radius": _text(radius),
                "c6_options_negative": options["strictly_negative"],
                "c6_passed": options["passed"],
                "c6_least_margin": options["least_negative"][0]["worst_margin_decimal"],
                "c7_largest": detail["largest"],
                "exp248_certificates": replayed,
                "floor_worst": [
                    {**record, "floor_ratio": local.decimal(record["floor_ratio"], 8)}
                    for record in ranked[:6]
                ],
                "floor_directions_at_or_above_one": sum(
                    record["floor_ratio"] >= 1 for record in ranked
                ),
                "seconds": round(time.monotonic() - started, 1),
            }
        )
    return results


# ---------------------------------------------------------------------------
# shape: a proposed radius vector
# ---------------------------------------------------------------------------


def half_masses(
    setting: Setting, arrays: Sequence[np.ndarray], radii: dict[str, Q]
) -> np.ndarray:
    """`F_j(r)`: half the largest point-program mass of coordinate `j`, both signs."""
    curvature, _ = local.curvature_audit(setting.family, setting.box, radii)
    weights = np.array([float(value) for value in curvature])
    result = np.zeros(len(setting.names))
    for index in range(len(setting.names)):
        for sign, array in itertools.product((1, -1), arrays):
            solved = point_program(array, weights, index, sign)
            result[index] = max(result[index], math.inf if solved is None else solved[0] / 2)
    return result


def _rational(value: float) -> Q:
    return Q(math.ceil(value * (1 << FLOOR_BITS)), 1 << FLOOR_BITS)


def propose(
    setting: Setting,
    floor: Q,
    theta: float,
    progress: Callable[[str], None] | None = None,
    *,
    position_share: Q = Q(1),
) -> dict[str, Any]:
    """Iterate `r = max(T, F(r)/theta)` from `r = T`, then test the rounded-up vector.

    `T` is `floor` on the 16 angles and `position_share * floor` on the 29 position
    coordinates, for a capture whose position extents settle faster than its angles.

    The iterates rise monotonically. They settle (relative step under `SHAPE_SETTLED`)
    when a fixed point exists, and grow past `SHAPE_CAP` times the floor otherwise. The
    settled vector, rounded up to multiples of `T / SHAPE_DENOMINATOR`, is evaluated
    once more: `point_ratio` is its largest `F_j(r) / r_j`, which the exact `ratio`
    mode can only meet or exceed.
    """
    names = setting.names
    arrays = [dense(setting.matrix.at(p), len(names)) for p in sample_points(setting.box)]
    low = float(floor)
    base = {name: Q(1) if name.startswith("omega") else position_share for name in names}
    lows = np.array([low * float(base[name]) for name in names])
    current = lows.copy()
    outcome = "step limit"
    steps = 0
    for steps in range(1, SHAPE_STEPS + 1):
        radii = {name: _rational(current[k]) for k, name in enumerate(names)}
        following = np.maximum(lows, half_masses(setting, arrays, radii) / theta)
        step = float(np.max(following / current)) - 1
        current = np.maximum(current, following)
        if progress is not None:
            progress(f"step {steps}: largest r/T {np.max(current / lows):.4f}, step {step:.2e}")
        if step < SHAPE_SETTLED:
            outcome = "settled"
            break
        if np.max(current / lows) > SHAPE_CAP:
            outcome = "unbounded"
            break
    multiples = {
        name: Q(math.ceil(current[k] / low * SHAPE_DENOMINATOR), SHAPE_DENOMINATOR)
        for k, name in enumerate(names)
    }
    rounded = {name: floor * value for name, value in multiples.items()}
    widths = np.array([float(rounded[name]) for name in names])
    ratios = half_masses(setting, arrays, rounded) / widths
    return {
        "floor": _text(floor),
        "position_share": _text(position_share),
        "theta": theta,
        "outcome": outcome,
        "steps": steps,
        "radii_over_floor": {name: _text(value) for name, value in multiples.items()},
        "widened": {
            name: _text(value)
            for name, value in multiples.items()
            if value > Q(math.ceil(base[name] * SHAPE_DENOMINATOR), SHAPE_DENOMINATOR)
        },
        "point_ratio": round(float(np.max(ratios)), 6),
        "passes_point_test": bool(np.max(ratios) < 1),
        "largest_point_ratios": [
            {"coordinate": names[k], "ratio": round(float(ratios[k]), 4)}
            for k in np.argsort(-ratios)[:8]
        ],
    }


# ---------------------------------------------------------------------------
# ratio: the recipe at a radius vector
# ---------------------------------------------------------------------------


def ratio_controls(
    setting: Setting,
    radii: dict[str, Q],
    worst: local.CoordinateOutcome,
) -> list[dict[str, Any]]:
    """C12 controls at the vector, as `ratio_controls` runs them at a uniform radius."""
    family, box = setting.family, setting.box
    controls: list[dict[str, Any]] = []
    flipped = local.build_family(
        family.t, family.beta, branches={**local.FACE_BRANCHES, (5, 7): 1}
    )
    branch = local.sign_branch_audit(flipped, box)
    controls.append(
        {"control": "flipped-tau-branch-5/7", "control_passed": not branch["passed"]}
    )
    _, perturbed = local.affine_audit(family, box, perturb=True)
    controls.append({"control": "perturbed-b-slope", "control_passed": not perturbed["passed"]})
    coordinate = family.names.index(worst.name)
    vector = [radii[name] for name in family.names]
    curvature, _ = local.curvature_audit(family, box, radii, setting.enclosure)
    negative = local.evaluate_dual(
        setting.matrix,
        curvature,
        vector,
        coordinate=coordinate,
        sign=worst.sign,
        dual=local.negative_vertex_control(worst.certificates[0][0]),
        deviation=setting.deviation,
    )
    controls.append(
        {
            "control": "negative-vertex-dual",
            "direction": worst.label,
            "control_passed": not negative["nonnegative"] and not negative["passed"],
        }
    )
    largest = max(verdict["ratio"] for _, verdict in worst.certificates)
    factor = max(2, math.ceil(2 / largest))
    wide = {name: value * factor for name, value in radii.items()}
    wide_curvature, _ = local.curvature_audit(family, box, wide, setting.enclosure)
    failing = sum(
        not local.evaluate_dual(
            setting.matrix,
            wide_curvature,
            [wide[name] for name in family.names],
            coordinate=coordinate,
            sign=worst.sign,
            dual=dual,
            deviation=setting.deviation,
        )["passed"]
        for dual, _ in worst.certificates
    )
    controls.append(
        {
            "control": "radius-vector-above-limit",
            "direction": worst.label,
            "factor": factor,
            "cells_failing": failing,
            "control_passed": failing > 0,
        }
    )
    restored = local.slide_invariance_audit(family, restore=frozenset({(9, 11)}))
    controls.append(
        {"control": "non-tight-row-9/11-restored", "control_passed": not restored["passed"]}
    )
    corner = local.unavailable_option_audit(family, box, radii, largest_corner=True)
    controls.append(
        {"control": "largest-corner-choice", "control_passed": not corner["passed"]}
    )
    return controls


def certify_vector(
    setting: Setting,
    radii: dict[str, Q],
    *,
    progress: Callable[[str], None] | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Every radius-dependent and box-dependent item of the recipe at the vector."""
    timings: dict[str, float] = {}
    started = time.monotonic()
    family, box, names = setting.family, setting.box, setting.names
    if set(radii) != set(names) or any(value <= 0 for value in radii.values()):
        raise ValueError("the radius vector must give a positive radius to all 45 coordinates")
    symbolic = local.symbolic_affine_audit(family, setting.matrix)
    slides = local.slide_invariance_audit(family)
    spanning = local.spanning_audit()
    roster = local.roster_binding_audit(family)
    stress = local.stress_audit(family, box)
    curvature, curvature_detail = local.curvature_audit(family, box, radii, setting.enclosure)
    options = local.unavailable_option_audit(family, box, radii, enclosure=setting.enclosure)
    timings["structure"] = time.monotonic() - started
    stage = time.monotonic()
    system = local.float_system(setting.matrix, len(names))
    vector = [radii[name] for name in names]
    outcomes: list[local.CoordinateOutcome] = []
    for name, sign in itertools.product(names, (1, -1)):
        outcome = local.certify_coordinate(
            setting.matrix,
            system,
            curvature,
            vector,
            names=names,
            name=name,
            sign=sign,
            box=box,
            deviation=setting.deviation,
        )
        outcomes.append(outcome)
        if progress is not None:
            record = local.outcome_record(outcome)
            progress(
                f"{record['direction']}: {record['cells']} {record.get('worst_ratio_decimal')}"
            )
    timings["c8_c9"] = time.monotonic() - stage
    stage = time.monotonic()
    certificates = [
        {
            "direction": o.label,
            "cells": [local.dual_document(dual) for dual, _ in o.certificates],
        }
        for o in outcomes
    ]
    replay = local.replay_certificates(
        setting.matrix,
        curvature,
        vector,
        names=names,
        documents=json.loads(json.dumps(certificates)),
        box=box,
        deviation=setting.deviation,
    )
    timings["replay"] = time.monotonic() - stage
    records = [local.outcome_record(outcome) for outcome in outcomes]
    passed_all = all(o.passed for o in outcomes)
    ranked = sorted(
        (o for o in outcomes if o.certificates),
        key=lambda o: -max(v["ratio"] for _, v in o.certificates),
    )
    stage = time.monotonic()
    controls = ratio_controls(setting, radii, ranked[0]) if ranked else []
    timings["controls"] = time.monotonic() - stage
    worst = local.outcome_record(ranked[0]) if ranked else None
    checks = {
        "c3_sign_branches": setting.branches["passed"],
        "c4_affine_structure": setting.affine["passed"],
        "c4_symbolic_in_root_parameters": symbolic["passed"],
        "c8i_root_box": setting.root_audit["passed"],
        "c2_slide_invariance": slides["passed"],
        "c10_spanning": spanning["passed"],
        "c1_roster_binding": roster["passed"],
        "c11_stress_on_the_box": stress["passed"],
        "c6_unavailable_options": options["passed"],
        "c8_c9_every_direction": passed_all,
        "c8_cells_tile_the_box": all(
            local.tiling_audit([dual.cell for dual, _ in o.certificates], box) for o in outcomes
        ),
        "c8_c9_replayed_from_certificates": replay["passed"]
        and replay["worst_ratio"] == (worst or {}).get("worst_ratio"),
        "c12_controls": bool(controls) and all(row["control_passed"] for row in controls),
    }
    timings["total"] = time.monotonic() - started
    body = {
        "slider_box": {
            name: [_text(lo), _text(hi)]
            for name, (lo, hi) in zip(local.SLIDER_PARAMETERS, box, strict=True)
        },
        "radii": {name: _text(radii[name]) for name in names},
        "radius_least": _text(min(vector)),
        "radius_largest": _text(max(vector)),
        "c3_sign_branches": setting.branches,
        "c6_unavailable_options": {
            key: options[key] for key in ("options", "strictly_negative", "least_negative")
        },
        "c7_largest": curvature_detail["largest"],
        "c11_stress_passed": stress["passed"],
        "c8_c9": {
            "total_cells": sum(len(o.certificates) for o in outcomes),
            "worst": worst,
            "largest_ratios": [
                {
                    "direction": o.label,
                    "ratio_decimal": local.decimal(
                        max(v["ratio"] for _, v in o.certificates), 12
                    ),
                    "cells": len(o.certificates),
                }
                for o in ranked[:12]
            ],
            "results": records,
        },
        "c8_c9_replay": replay,
        "c12_controls": controls,
        "not_rerun": (
            "the C12 n11 replay, which no radius or box changes (exp-248 run-002); the "
            "core-stress commit binding, which Git keeps"
        ),
        "checks": checks,
        "passed": all(checks.values()),
        "timing_seconds": {key: round(value, 1) for key, value in timings.items()},
    }
    return body, certificates


# ---------------------------------------------------------------------------
# slide: H-268 at a uniform radius
# ---------------------------------------------------------------------------


@contextmanager
def scene_radius(held: Q) -> Iterator[None]:
    """Hold `check_n17_slider_coverage.build_scene` at `held` while the block runs."""
    original = slide.build_scene

    def at_radius(
        radius: Q = held,
        cell: tuple[Q, Q, Q, Q] | None = None,
        design: str = slide.DEFAULT_DESIGN,
    ) -> slide.Scene:
        del radius
        return original(radius=held, cell=cell, design=design)

    slide.build_scene = at_radius
    try:
        yield
    finally:
        slide.build_scene = original


def slide_coverage(radius: Q, thresholds: Sequence[Q], tight: Sequence[Q]) -> dict[str, Any]:
    """The unchanged H-268 `run` with every non-slider coordinate within `radius`."""
    with scene_radius(radius):
        receipt = slide.run(
            thresholds[0],
            thresholds[1],
            thresholds[2],
            tight=(tight[0], tight[1], tight[2]),
        )
    if receipt["radius"] != str(radius):
        raise ValueError("slide coverage did not run at the requested radius")
    return receipt


# ---------------------------------------------------------------------------
# bounds: a model of finer curvature lemmas
# ---------------------------------------------------------------------------


def _owner(pair: tuple[int, int]) -> int:
    ordered = tuple(sorted(pair))
    return next(
        int(row["owner"])
        for row in option_manifest()
        if (row["left"], row["right"]) == ordered and row["kind"] == "identity"
    )


def second_order_forms(family: local.Family, point: Point) -> list[np.ndarray]:
    """Each retained row's exact second-order form on the 45 lifted coordinates (float)."""
    rows = local.family_rows(family, point)
    centres = [(float(x), float(y)) for x, y in local.moved_centres(family, point)]
    size = local.DIMENSION
    lift = np.zeros((size, len(family.names)))
    for k, entries in enumerate(family.lifts):
        for c, value in entries.items():
            lift[c, k] = float(value)
    forms: list[np.ndarray] = []
    for key in family.keys:
        row = [float(value) for value in rows[key]]
        form = np.zeros((size, size))
        if key[0] == "wall":
            label = int(key[1])
            angle = local.column(label, "angle")
            form[angle, angle] = math.sqrt(max(0.5 - row[angle] ** 2, 0.0))
            forms.append(lift.T @ form @ lift)
            continue
        left, right = int(key[1]), int(key[2])
        normal = (row[local.column(right, "x")], row[local.column(right, "y")])
        if (left, right) in PARALLEL_PAIRS:
            # The face endpoint is a corner of the square whose angle coefficient is
            # +-1/2 (Lemma 2); the owner is the other one. At tau = 0 both are, and the
            # variant's convention picks.
            first, second = (right, left) if key[3] == 0 else (left, right)
            other_half = abs(abs(row[local.column(second, "angle")]) - 0.5) < 1e-12
            owner = first if other_half else second
        else:
            owner = _owner((left, right))
        other = right if owner == left else left
        n_o = normal if owner == left else (-normal[0], -normal[1])
        t_o = (-n_o[1], n_o[0])
        beta = -row[local.column(other, "angle")]
        alpha = -math.sqrt(max(0.5 - beta * beta, 0.0))
        corner = (alpha * n_o[0] + beta * t_o[0], alpha * n_o[1] + beta * t_o[1])
        reach = (
            centres[other - 1][0] - centres[owner - 1][0] + corner[0],
            centres[other - 1][1] - centres[owner - 1][1] + corner[1],
        )
        tangent_arm = t_o[0] * reach[0] + t_o[1] * reach[1]
        if (
            abs(n_o[0] * reach[0] + n_o[1] * reach[1] - 0.5) > 1e-9
            or abs(tangent_arm - row[local.column(owner, "angle")]) > 1e-9
        ):
            raise ValueError(f"row geometry does not reproduce the row: {key}")
        o, p = local.column(owner, "angle"), local.column(other, "angle")
        form[o, o] -= 0.5
        form[p, p] -= alpha
        form[o, p] += alpha
        form[p, o] += alpha
        for component, value in zip(("x", "y"), t_o, strict=True):
            for label, sign in ((other, 1.0), (owner, -1.0)):
                c = local.column(label, component)
                form[o, c] += sign * value
                form[c, o] += sign * value
        forms.append(lift.T @ form @ lift)
    return forms


def entrywise_bound(form: np.ndarray, radii: np.ndarray) -> float:
    """`max h^T H h` over the box, bounded by positive diagonals and absolute off-diagonals."""
    diagonal = np.clip(np.diag(form), 0, None) @ (radii * radii)
    off = np.abs(form - np.diag(np.diag(form)))
    return float(diagonal + radii @ off @ radii)


def row_bound(form: np.ndarray, radii: np.ndarray) -> float:
    """The exact box maximum of one row's form: vertices, with a grid on a concave angle."""
    support = [k for k in range(len(radii)) if np.any(form[k] != 0)]
    if not support:
        return 0.0
    small = form[np.ix_(support, support)]
    widths = radii[support]
    concave = [i for i in range(len(support)) if small[i, i] < 0]
    free = [i for i in range(len(support)) if i not in concave]
    best = -math.inf
    for signs in itertools.product((-1.0, 1.0), repeat=len(free)):
        h = np.zeros(len(support))
        for i, value in zip(free, signs, strict=True):
            h[i] = value * widths[i]
        grid = np.linspace(-1, 1, 401) if concave else np.zeros(1)
        for g in grid:
            for i in concave:
                h[i] = g * widths[i]
            best = max(best, float(h @ small @ h))
    return best


def joint_program(
    matrix: np.ndarray, forms: Sequence[np.ndarray], radii: np.ndarray, j: int, sign: int
) -> float:
    """`min` over coordinate duals of the entrywise bound of `sum_i lambda_i H_i`."""
    rows, width = matrix.shape
    pairs = [(k, m) for k in range(width) for m in range(k, width)]
    table = np.array([[form[k, m] for k, m in pairs] for form in forms])
    active = [q for q in range(len(pairs)) if np.any(table[:, q] != 0)]
    count = rows + len(active)
    cost = np.zeros(count)
    upper: list[np.ndarray] = []
    for slot, q in enumerate(active):
        k, m = pairs[q]
        cost[rows + slot] = radii[k] ** 2 if k == m else 2 * radii[k] * radii[m]
        for direction in (1.0, -1.0) if k != m else (1.0,):
            line = np.zeros(count)
            line[:rows] = direction * table[:, q]
            line[rows + slot] = -1
            upper.append(line)
    equality = np.zeros((width, count))
    equality[:, :rows] = matrix.T
    target = np.zeros(width)
    target[j] = -sign
    result = linprog(
        cost,
        A_ub=np.array(upper),
        b_ub=np.zeros(len(upper)),
        A_eq=equality,
        b_eq=target,
        bounds=[(0, None)] * count,
        method="highs",
    )
    return float(result.fun) if result.status == 0 else math.inf


def model_bounds(setting: Setting, radii: dict[str, Q], name: str, sign: int) -> dict[str, Any]:
    """The worst sample point's ratio under the checker's constants and the two models."""
    names = setting.names
    j = names.index(name)
    widths = np.array([float(radii[n]) for n in names])
    curvature, _ = local.curvature_audit(setting.family, setting.box, radii)
    weights = np.array([float(value) for value in curvature])
    label = int(name.lstrip("abcdefghijklmnopqrstuvwxyz"))
    own_rows = [
        i
        for i, key in enumerate(setting.family.keys)
        if label in ((int(key[1]),) if key[0] == "wall" else (int(key[1]), int(key[2])))
    ]
    worst: dict[str, Any] | None = None
    for point in sample_points(setting.box):
        array = dense(setting.matrix.at(point), len(names))
        forms = second_order_forms(setting.family, point)
        checker = point_program(array, weights, j, sign)
        per_row = np.array([max(row_bound(form, widths), 1e-30) for form in forms])
        signed = point_program(array, per_row, j, sign)
        if checker is None or signed is None:
            raise ValueError(f"no coordinate dual for {name}:{sign}")
        lam = np.asarray(
            linprog(
                weights,
                A_eq=array.T,
                b_eq=-sign * np.eye(len(names))[j],
                bounds=[(0, None)] * len(forms),
                method="highs",
            ).x,
            dtype=float,
        )
        at_checker = entrywise_bound(
            sum(
                (value * form for value, form in zip(lam, forms, strict=True)),
                np.zeros_like(forms[0]),
            ),
            widths,
        )
        joint = joint_program(array, forms, widths, j, sign)
        record = {
            "point": [_text(v) for v in point],
            "checker_constants": checker[0] / (2 * widths[j]),
            "row_by_row_signed": signed[0] / (2 * widths[j]),
            "joint_at_checker_dual": at_checker / (2 * widths[j]),
            "joint_optimised": joint / (2 * widths[j]),
            "constant_over_signed_row_mean": float(np.mean(weights / per_row)),
            "dual_l1": float(np.sum(lam)),
            "largest_loads": [
                {"row": local.row_label(setting.family.keys[i]), "share": float(share)}
                for i, share in sorted(
                    enumerate(lam * weights / float(lam @ weights)), key=lambda item: -item[1]
                )[:10]
            ],
            "mass_share_on_own_square_rows": float(
                sum(lam[i] * weights[i] for i in own_rows) / float(lam @ weights)
            ),
        }
        if worst is None or record["checker_constants"] > worst["checker_constants"]:
            worst = record
    if worst is None:
        raise ValueError("no sample point")
    for load in worst["largest_loads"]:
        load["share"] = round(load["share"], 4)
    return {key: round(v, 4) if isinstance(v, float) else v for key, v in worst.items()}


# ---------------------------------------------------------------------------
# command line
# ---------------------------------------------------------------------------


def read_radii(path: Path, floor: Q | None) -> dict[str, Q]:
    """A radius vector from a `shape` receipt (`radii_over_floor` times `floor`) or a map."""
    document = json.loads(path.read_text())
    if "radii_over_floor" in document:
        base = Q(document["floor"]) if floor is None else floor
        return {name: base * Q(value) for name, value in document["radii_over_floor"].items()}
    return {name: Q(value) for name, value in document["radii"].items()}


def _box(values: Sequence[Q] | None) -> Box:
    return BOX_W_PRIME if values is None else local.slider_box(values)


def _write(path: Path | None, document: Any) -> None:
    if path is not None:
        path.write_text(json.dumps(document, sort_keys=True, indent=1, default=str) + "\n")


def _say(line: str) -> None:
    print(line, flush=True)


def _run_slide(args: argparse.Namespace) -> int:
    receipt = slide_coverage(args.radius[0], args.thresholds, args.tight)
    _write(args.output, {"schema": SCHEMA, "mode": "slide", **receipt})
    summary = {
        "passed": receipt["passed"],
        "checks": receipt["checks"],
        "certified_box": {k: v["exact"] for k, v in receipt["certified_box"].items()},
    }
    print(json.dumps(summary, sort_keys=True))
    return 0 if receipt["passed"] else 1


def _run_scan(args: argparse.Namespace, setting: Setting) -> int:
    results = scan(setting, args.radius or SCAN_RADII)
    box = [[_text(lo), _text(hi)] for lo, hi in setting.box]
    _write(args.output, {"schema": SCHEMA, "mode": "scan", "box": box, "results": results})
    for result in results:
        worst = result["floor_worst"][0]
        line = {
            "radius": result["radius"],
            "c6": result["c6_passed"],
            "exp248_worst": result["exp248_certificates"]["worst_ratio_decimal"],
            "floor_worst": [worst["direction"], worst["floor_ratio"]],
            "floor_at_or_above_one": result["floor_directions_at_or_above_one"],
        }
        print(json.dumps(line))
    return 0


def _run_shape(args: argparse.Namespace, setting: Setting) -> int:
    proposal = propose(
        setting,
        args.floor,
        args.theta,
        _say if args.progress else None,
        position_share=args.position_share,
    )
    box = [[_text(lo), _text(hi)] for lo, hi in setting.box]
    _write(args.output, {"schema": SCHEMA, "mode": "shape", "box": box, **proposal})
    keys = ("floor", "theta", "outcome", "steps", "widened", "point_ratio")
    print(json.dumps({key: proposal[key] for key in keys}))
    return 0 if proposal["passes_point_test"] else 1


def _run_bounds(args: argparse.Namespace, setting: Setting, radii: dict[str, Q]) -> int:
    name, _, sign = args.direction.partition(":")
    record = model_bounds(setting, radii, name, int(sign))
    _write(
        args.output, {"schema": SCHEMA, "mode": "bounds", "direction": args.direction, **record}
    )
    print(json.dumps(record, sort_keys=True))
    return 0


def _run_ratio(args: argparse.Namespace, setting: Setting, radii: dict[str, Q]) -> int:
    started = time.monotonic()
    body, certificates = certify_vector(
        setting, radii, progress=_say if args.progress else None
    )
    receipt = {
        "schema": SCHEMA,
        "mode": "ratio",
        "scope": (
            "H-261 recipe items C1-C4, C6-C11 and the C12 controls but the n11 replay, at a "
            "declared radius vector over a declared slider box; certificates exact at the "
            "exp-237 midpoint with the root-box residual; planning evidence"
        ),
        "root_certificate": FROZEN_ROOT_REF,
        **body,
    }
    _write(args.output, receipt)
    if args.certificates is not None:
        args.certificates.write_text(json.dumps(certificates, sort_keys=True) + "\n")
    worst = receipt["c8_c9"]["worst"] or {}
    summary = {
        "passed": receipt["passed"],
        "checks": receipt["checks"],
        "worst": {key: worst.get(key) for key in ("direction", "worst_ratio_decimal", "cells")},
        "total_cells": receipt["c8_c9"]["total_cells"],
        "seconds": round(time.monotonic() - started, 1),
    }
    print(json.dumps(summary, sort_keys=True))
    return 0 if receipt["passed"] else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or SCHEMA).splitlines()[0])
    parser.add_argument("mode", choices=("scan", "shape", "ratio", "slide", "bounds"))
    parser.add_argument(
        "--box", nargs=6, type=Q, metavar=("A_LO", "A_HI", "B_LO", "B_HI", "Z_LO", "Z_HI")
    )
    parser.add_argument("--radius", type=Q, action="append", help="uniform radius (repeatable)")
    parser.add_argument("--floor", type=Q, help="shape: least radius; ratio: scales --radii")
    parser.add_argument("--theta", type=float, default=0.95, help="shape: point-test factor")
    parser.add_argument(
        "--position-share", type=Q, default=Q(1), help="shape: position floor over angle floor"
    )
    parser.add_argument("--radii", type=Path, help="ratio, bounds: a radius vector file")
    parser.add_argument("--direction", default="omega11:-1", help="bounds: NAME:SIGN")
    parser.add_argument("--thresholds", nargs=3, type=Q, default=list(slide.THRESHOLDS))
    parser.add_argument("--tight", nargs=3, type=Q, default=list(slide.TIGHT))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--certificates", type=Path)
    parser.add_argument("--progress", action="store_true")
    args = parser.parse_args(argv)
    uniform: list[Q] = list(args.radius or [])
    single = len(uniform) == 1
    if args.mode == "slide" and not single:
        parser.error("slide takes exactly one --radius")
    if args.mode == "shape" and args.floor is None:
        parser.error("shape needs --floor")
    if args.mode in {"ratio", "bounds"} and args.radii is None and not single:
        parser.error("ratio and bounds need --radii FILE or one --radius")
    try:
        if args.mode == "slide":
            return _run_slide(args)
        setting = build_setting(_box(args.box))
        if args.mode == "scan":
            return _run_scan(args, setting)
        if args.mode == "shape":
            return _run_shape(args, setting)
        radii: dict[str, Q] = (
            read_radii(args.radii, args.floor)
            if args.radii is not None
            else dict.fromkeys(setting.names, uniform[0])
        )
        if args.mode == "bounds":
            return _run_bounds(args, setting, radii)
        return _run_ratio(args, setting, radii)
    except (ValueError, OSError, KeyError) as error:
        print(json.dumps({"schema": SCHEMA, "passed": False, "error": str(error)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
