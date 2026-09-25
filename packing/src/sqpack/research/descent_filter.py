"""Descent filter: does a quench endpoint have a verified side-decreasing move?

`quench_bracket` searches the angles one orientation CLASS at a time, so it can stop at
a point where every class coordinate is stationary but a joint move of several angles
still descends. X-046 found six such endpoints within `U + 0.005` of Trump's side, all
of them on monotone paths back to Trump. This module is the filter a census needs
before it can call an endpoint a local minimum.

## What it searches

All 33 pose coordinates and the side move at once. At a pose it builds the first-order
model of the problem inside a sup-norm trust region of radius `delta`:

* containment, one row per corner and wall, each smooth in the pose;
* non-overlap, one row per corner of `B` beyond an edge line of `A`, for each way the
  pair can be separated. Two squares are disjoint exactly when one of eight such
  choices holds (an edge of either square, either orientation), so the feasible set is
  a union. Every choice that separates the pair at the current pose is kept, and a pair
  with more than one (parallel squares in edge contact, corner contacts) becomes a
  disjunction solved by a big-M MILP. That makes the first-order test exact over the
  union of active cells rather than over one arbitrarily chosen cell, which matters:
  for two parallel squares in edge contact, one choice forbids a rotation to first
  order that the other permits.

The MILP minimises the side change. A predicted decrease is followed by a line search
that moves the angles along the direction and re-optimises the centres with the stock
fixed-angle LP (`solve_to_fixed_point`), so every accepted step is a feasible pose of
the fixed-angle problem and its side is an LP value, not a linear prediction. When the
first-order model predicts no decrease, three probe families look for second-order or
missed descent: random directions in the first-order flat cone, random angle
directions, and single-angle moves, all projected the same way.

## What the verdict means

* **Rejected** means a verified decrease: a pose whose exact rational witness (below)
  has side below the reference side by more than `certify_tol`. That is a proof that
  the endpoint is not a local minimum in the neighbourhood searched, up to the
  correctness of `sqpack.verify` over the rationals.
* **Descent-stable** means only that no exact witness more than `certify_tol` below
  the reference side was found within the declared budget, while the descent itself
  continued until no step lowered the LP side by more than `step_tol`. It is empirical
  support for local minimality, not a proof: the probes are finite, the MILP is solved
  in `f64`, and a descent that needs a finite move through a higher region is invisible
  to any local method.

## Exact witnesses

A float pose is turned into a rational one by replacing each angle with the rotation
whose half-angle tangent is a nearby rational, so `cos` and `sin` are exactly rational
and the square is exactly a unit square; centres are the float values read exactly.
The centres are scaled apart about their centroid by `1 + m`, which widens every
separating gap by at least `m` (the centre distance along any separating normal is at
least 1), and the container is the exact bounding box. `verify_packing` then decides
the rational packing with exact signs, and `m` grows tenfold on a refusal. The
witness side is therefore an upper bound actually attained by a checked packing.
"""

from __future__ import annotations

import math
import random
import time
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

from sqpack.research.quench import angle_classes, solve_to_fixed_point
from sqpack.verify import verify_packing

QUARTER = math.pi / 2
SQRT2 = math.sqrt(2.0)
# Stromquist's Theorem 3 value for eleven squares at 0 and 45 degrees.
STROMQUIST_11_SIDE = 2.0 + 4.0 * SQRT2 / 3.0

_OFFSETS = ((-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5))
_NORMALS = ((1.0, 0.0), (0.0, 1.0), (-1.0, 0.0), (0.0, -1.0))

# A rational half-angle tangent with a denominator at most this is within ~1e-19 of the
# float angle it replaces, far below the smallest witness margin.
_WITNESS_DENOMINATOR = 2**32


@dataclass(frozen=True)
class DescentFilterConfig:
    """The declared budget and tolerances of one filter call."""

    # Sup-norm trust radius over centres (length) and angles (radians) together.
    trust_radius: float = 1e-2
    trust_max: float = 5e-2
    trust_min: float = 1e-6
    # A step is accepted when it lowers the LP side by more than this. It sets how far
    # the descent continues, near the LP's own resolution, and decides nothing: the
    # verdict on the endpoint is `certify_tol`.
    step_tol: float = 1e-11
    # The declared tolerance. A rejection needs an exact witness this far below the
    # reference side; an endpoint with no such witness is descent-stable at this scale.
    certify_tol: float = 1e-8
    # A first-order predicted side decrease (absolute) below this is solver noise.
    predicted_tol: float = 1e-12
    # A separating choice this far into overlap still counts as active at the pose.
    ambiguity_tol: float = 1e-8
    max_iterations: int = 400
    line_search_halvings: int = 12
    cone_probes: int = 8
    random_probes: int = 12
    probe_steps: tuple[float, ...] = (1e-2, 1e-3, 1e-4)
    coordinate_steps: tuple[float, ...] = (1e-3, 1e-5)
    time_budget: float = 60.0
    milp_time_limit: float = 10.0
    seed: int = 0

    def as_dict(self) -> dict[str, Any]:
        """The configuration as a plain record, for receipts."""
        return {
            "trust_radius": self.trust_radius,
            "trust_max": self.trust_max,
            "trust_min": self.trust_min,
            "step_tol": self.step_tol,
            "certify_tol": self.certify_tol,
            "predicted_tol": self.predicted_tol,
            "ambiguity_tol": self.ambiguity_tol,
            "max_iterations": self.max_iterations,
            "line_search_halvings": self.line_search_halvings,
            "cone_probes": self.cone_probes,
            "random_probes": self.random_probes,
            "probe_steps": list(self.probe_steps),
            "coordinate_steps": list(self.coordinate_steps),
            "time_budget": self.time_budget,
            "milp_time_limit": self.milp_time_limit,
            "seed": self.seed,
        }


@dataclass
class ExactWitness:
    """A rational packing built from a float pose, and what the exact check said."""

    valid: bool
    side: Fraction | None
    margin: float
    attempts: int
    touching_pairs: int = 0
    failures: list[str] = field(default_factory=list)
    x: list[Fraction] = field(default_factory=list)
    y: list[Fraction] = field(default_factory=list)
    # Rational half-angle tangents: cos = (1 - u^2) / (1 + u^2), sin = 2u / (1 + u^2).
    u: list[Fraction] = field(default_factory=list)

    def as_dict(self, *, with_pose: bool = False) -> dict[str, Any]:
        """A JSON-ready record; the rational pose only when asked for."""
        out: dict[str, Any] = {
            "valid": self.valid,
            "side": float(self.side) if self.side is not None else None,
            "side_exact": str(self.side) if self.side is not None else None,
            "margin": self.margin,
            "attempts": self.attempts,
            "touching_pairs": self.touching_pairs,
            "failures": self.failures[:5],
        }
        if with_pose:
            out["x_exact"] = [str(v) for v in self.x]
            out["y_exact"] = [str(v) for v in self.y]
            out["half_angle_tangent_exact"] = [str(v) for v in self.u]
        return out


@dataclass
class DescentFilterResult:
    """What the filter found from one endpoint."""

    status: str  # "stable" or "budget"
    rejected: bool
    reference_side: float
    start_side: float
    start_settled: bool
    terminal_side: float
    certified_decrease: float | None
    certificate: ExactWitness | None
    terminal_witness: ExactWitness | None
    x: list[float]
    y: list[float]
    theta: list[float]
    iterations: int
    accepted_steps: int
    probe_steps: int
    milp_solves: int
    fixed_point_solves: int
    seconds: float
    reason: str
    history: list[dict[str, Any]] = field(default_factory=list)

    @property
    def total_decrease(self) -> float:
        """How far the filter moved the side below the reference, in LP terms."""
        return self.reference_side - self.terminal_side

    def as_dict(self, *, with_pose: bool = True) -> dict[str, Any]:
        """A JSON-ready record of the verdict and its evidence."""
        out: dict[str, Any] = {
            "status": self.status,
            "rejected": self.rejected,
            "reference_side": self.reference_side,
            "start_side": self.start_side,
            "start_settled": self.start_settled,
            "terminal_side": self.terminal_side,
            "total_decrease": self.total_decrease,
            "certified_decrease": self.certified_decrease,
            "certificate": self.certificate.as_dict() if self.certificate else None,
            "terminal_witness": (
                self.terminal_witness.as_dict() if self.terminal_witness else None
            ),
            "iterations": self.iterations,
            "accepted_steps": self.accepted_steps,
            "probe_steps": self.probe_steps,
            "milp_solves": self.milp_solves,
            "fixed_point_solves": self.fixed_point_solves,
            "seconds": round(self.seconds, 3),
            "reason": self.reason,
        }
        if with_pose:
            out["x"] = list(self.x)
            out["y"] = list(self.y)
            out["theta"] = list(self.theta)
        return out


def stromquist_11_pose() -> tuple[list[float], list[float], list[float]]:
    """A packing of Stromquist's 0/45-degree family at side `2 + 4 sqrt 2 / 3`.

    Six axis squares on the walls and five diamonds, every centre in `Q(sqrt 2)`. It was
    read off an X-046 probe-C endpoint after snapping its angles to exactly 0 and 45
    degrees; the fixed-angle LP at these angles returns the family value to `1e-15`,
    and square 7 touches only square 6 and the floor, so the family has rattlers.
    """
    s = STROMQUIST_11_SIDE
    r = SQRT2
    axis = [
        (0.5, 0.5),
        (s - 0.5, 0.5),
        (2.5, s - 0.5),
        (0.5, s - 0.5),
        (1.5, s - 0.5),
        (0.5, s - 1.5),
    ]
    diamonds = [
        (1.5 - r / 6, 0.5 + 2 * r / 3),
        (1 + 2 * r / 3, r / 2),
        (1 + 2 * r / 3, 1 + 5 * r / 6),
        (1 + 7 * r / 6, 1 + r / 3),
        (s - r / 2, 5 * r / 3),
    ]
    centres = axis + diamonds
    theta = [0.0] * 6 + [math.pi / 4] * 5
    return [c[0] for c in centres], [c[1] for c in centres], theta


def fold(theta: float) -> float:
    """An angle modulo the quarter turn a square is invariant under, in `[0, pi/2)`."""
    return theta % QUARTER


def class_summary(theta: list[float], tol: float = 1e-3) -> dict[str, Any]:
    """Orientation classes modulo the quarter turn, largest first."""
    groups = sorted(angle_classes(theta, tol), key=len, reverse=True)
    return {
        "classes": len(groups),
        "multiplicities": [len(g) for g in groups],
        "class_degrees": [round(math.degrees(fold(theta[g[0]])), 4) for g in groups],
        "members": [sorted(g) for g in groups],
    }


def min_pair_gap(x: list[float], y: list[float], theta: list[float]) -> float:
    """The smallest separating-axis gap over all pairs; negative means overlap."""
    n = len(x)
    cs = [(math.cos(t), math.sin(t)) for t in theta]
    worst = math.inf
    for i in range(n):
        ci, si = cs[i]
        for j in range(i + 1, n):
            cj, sj = cs[j]
            dx, dy = x[i] - x[j], y[i] - y[j]
            half = 0.5 + 0.5 * (abs(ci * cj + si * sj) + abs(si * cj - ci * sj))
            gap = max(
                abs(dx * ax + dy * ay) - half
                for ax, ay in ((ci, si), (-si, ci), (cj, sj), (-sj, cj))
            )
            worst = min(worst, gap)
    return worst


def bounding_side(x: list[float], y: list[float], theta: list[float]) -> float:
    """Side of the smallest axis-parallel square holding the pose, in floats."""
    xs, ys = [], []
    for cx, cy, t in zip(x, y, theta, strict=True):
        c, s = math.cos(t), math.sin(t)
        for a, b in _OFFSETS:
            xs.append(cx + c * a - s * b)
            ys.append(cy + s * a + c * b)
    return max(max(xs) - min(xs), max(ys) - min(ys))


def _fraction_sign(value: Fraction) -> int:
    return (value > 0) - (value < 0)


def exact_witness(
    x: list[float],
    y: list[float],
    theta: list[float],
    *,
    margin: float | None = None,
    max_attempts: int = 6,
) -> ExactWitness:
    """Build and exactly check a rational packing next to a float pose.

    See the module docstring for the construction. The returned side is attained by the
    rational packing that `verify_packing` accepted, or `valid` is false.
    """
    n = len(x)
    gap = min_pair_gap(x, y, theta)
    m = margin if margin is not None else max(0.0, -gap) * 2.0 + 1e-12
    us = [
        Fraction(math.tan(fold(t) / 2.0)).limit_denominator(_WITNESS_DENOMINATOR) for t in theta
    ]
    rot = [((1 - u * u) / (1 + u * u), (2 * u) / (1 + u * u)) for u in us]
    fx = [Fraction(v) for v in x]
    fy = [Fraction(v) for v in y]
    cx = sum(fx, Fraction(0)) / n
    cy = sum(fy, Fraction(0)) / n
    failures: list[str] = []
    for attempt in range(1, max_attempts + 1):
        factor = 1 + Fraction(m)
        px = [cx + factor * (v - cx) for v in fx]
        py = [cy + factor * (v - cy) for v in fy]
        squares = []
        for k in range(n):
            c, s = rot[k]
            squares.append(
                [(px[k] + c * a - s * b, py[k] + s * a + c * b) for a, b in _OFFSETS_Q]
            )
        lo_x = min(p[0] for sq in squares for p in sq)
        lo_y = min(p[1] for sq in squares for p in sq)
        hi_x = max(p[0] for sq in squares for p in sq)
        hi_y = max(p[1] for sq in squares for p in sq)
        side = max(hi_x - lo_x, hi_y - lo_y)
        shifted = [[(p[0] - lo_x, p[1] - lo_y) for p in sq] for sq in squares]
        report = verify_packing(shifted, side, sign=_fraction_sign)
        if report.valid:
            return ExactWitness(
                valid=True,
                side=side,
                margin=m,
                attempts=attempt,
                touching_pairs=report.touching_pairs,
                x=[v - lo_x for v in px],
                y=[v - lo_y for v in py],
                u=us,
            )
        failures = [f"{kind}: {text}" for kind, text in report.failures]
        m *= 10.0
    return ExactWitness(
        valid=False, side=None, margin=m, attempts=max_attempts, failures=failures
    )


_OFFSETS_Q = tuple((Fraction(a), Fraction(b)) for a, b in _OFFSETS)


@dataclass
class _Model:
    """The trust-region first-order model, in units of the trust radius."""

    a: np.ndarray
    lb: np.ndarray
    group_rows: np.ndarray | None
    continuous: int
    binaries: int
    ambiguous_pairs: int


def _build_model(
    x: list[float],
    y: list[float],
    theta: list[float],
    side: float,
    *,
    delta: float,
    ambiguity: float,
) -> _Model:
    """Rows `a . u >= lb` over `u = (dS, dx, dy, dtheta) / delta`, plus disjunctions."""
    n = len(x)
    nc = 1 + 3 * n
    ix, iy, it = 1, 1 + n, 1 + 2 * n
    reach = 4.0 * delta
    frames = []
    for t in theta:
        c, s = math.cos(t), math.sin(t)
        frames.append(
            (
                [(c * a - s * b, s * a + c * b) for a, b in _OFFSETS],
                [(c * a - s * b, s * a + c * b) for a, b in _NORMALS],
            )
        )
    plain: list[tuple[dict[int, float], float]] = []
    groups: list[list[list[tuple[dict[int, float], float]]]] = []
    for i in range(n):
        for rx, ry in frames[i][0]:
            px, py = x[i] + rx, y[i] + ry
            for g, coeffs in (
                (px, {ix + i: 1.0, it + i: -ry}),
                (side - px, {0: 1.0, ix + i: -1.0, it + i: ry}),
                (py, {iy + i: 1.0, it + i: rx}),
                (side - py, {0: 1.0, iy + i: -1.0, it + i: -rx}),
            ):
                if g <= reach:
                    plain.append((coeffs, -max(g, 0.0) / delta))
    for i in range(n):
        for j in range(i + 1, n):
            choices = []
            for a_sq, b_sq in ((i, j), (j, i)):
                for nx, ny in frames[a_sq][1]:
                    corners = []
                    for rx, ry in frames[b_sq][0]:
                        wx = x[b_sq] + rx - x[a_sq]
                        wy = y[b_sq] + ry - y[a_sq]
                        corners.append((wx * nx + wy * ny - 0.5, rx, ry, wx, wy))
                    choices.append((min(c[0] for c in corners), a_sq, b_sq, nx, ny, corners))
            best = max(choices, key=lambda c: c[0])
            if best[0] > reach:
                continue
            live = [c for c in choices if c[0] >= -ambiguity] or [best]
            per_choice = []
            for _, a_sq, b_sq, nx, ny, corners in live:
                rows = []
                for g, rx, ry, wx, wy in corners:
                    if g > reach:
                        continue
                    coeffs = {
                        ix + b_sq: nx,
                        iy + b_sq: ny,
                        ix + a_sq: -nx,
                        iy + a_sq: -ny,
                        it + b_sq: -ry * nx + rx * ny,
                        it + a_sq: -wx * ny + wy * nx,
                    }
                    rows.append((coeffs, -max(g, 0.0) / delta))
                per_choice.append(rows)
            if len(per_choice) == 1:
                plain.extend(per_choice[0])
            else:
                groups.append(per_choice)
    nb = sum(len(g) for g in groups)
    total_rows = len(plain) + sum(len(rows) for g in groups for rows in g)
    a = np.zeros((total_rows, nc + nb))
    lb = np.zeros(total_rows)
    ub_abs = np.ones(nc)
    ub_abs[0] = 2.0
    r = 0
    for coeffs, rhs in plain:
        for col, v in coeffs.items():
            a[r, col] += v
        lb[r] = rhs
        r += 1
    group_rows = np.zeros((len(groups), nc + nb)) if groups else None
    b = nc
    for gi, group in enumerate(groups):
        for rows in group:
            for coeffs, rhs in rows:
                big = sum(abs(v) * ub_abs[col] for col, v in coeffs.items()) + 1e-6
                for col, v in coeffs.items():
                    a[r, col] += v
                a[r, b] = -big
                lb[r] = rhs - big
                r += 1
            assert group_rows is not None
            group_rows[gi, b] = 1.0
            b += 1
    return _Model(
        a=a,
        lb=lb,
        group_rows=group_rows,
        continuous=nc,
        binaries=nb,
        ambiguous_pairs=len(groups),
    )


def _solver_bound(values: np.ndarray) -> Any:
    """scipy's stubs type constraint bounds as scalars; HiGHS takes arrays."""
    return values


def _solve_model(
    model: _Model,
    *,
    objective: np.ndarray | None = None,
    side_cap: float | None = None,
    time_limit: float,
) -> np.ndarray | None:
    """Minimise `u_S` (or a supplied objective) over the model; `None` on failure."""
    nv = model.continuous + model.binaries
    c = np.zeros(nv)
    if objective is None:
        c[0] = 1.0
    else:
        c[: model.continuous] = objective
    lo = np.full(nv, -1.0)
    hi = np.full(nv, 1.0)
    lo[0], hi[0] = -2.0, 2.0
    if side_cap is not None:
        hi[0] = side_cap
    lo[model.continuous :] = 0.0
    integrality = np.zeros(nv)
    integrality[model.continuous :] = 1
    constraints = [LinearConstraint(model.a, _solver_bound(model.lb), np.inf)]
    if model.group_rows is not None:
        constraints.append(LinearConstraint(model.group_rows, 1.0, 1.0))
    res = milp(
        c,
        integrality=integrality,
        bounds=Bounds(_solver_bound(lo), _solver_bound(hi)),
        constraints=constraints,
        options={"time_limit": time_limit, "presolve": True},
    )
    if res.x is None:
        return None
    return np.asarray(res.x[: model.continuous])


class _Search:
    """Mutable state of one filter call."""

    def __init__(
        self, x: list[float], y: list[float], theta: list[float], cfg: DescentFilterConfig
    ) -> None:
        self.cfg = cfg
        self.n = len(x)
        self.x, self.y, self.theta = list(x), list(y), list(theta)
        self.side = math.inf
        self.milp_solves = 0
        self.fixed_point_solves = 0
        self.rng = random.Random(cfg.seed)

    def project(
        self, theta: list[float], x: list[float], y: list[float]
    ) -> tuple[float, list[float], list[float]] | None:
        """The fixed-angle cell optimum at `theta`, or `None` if it did not settle."""
        self.fixed_point_solves += 1
        got = solve_to_fixed_point(theta, x, y, self.n)
        if not got.settled or not math.isfinite(got.side):
            return None
        return got.side, list(got.x), list(got.y)

    def model(self, delta: float) -> _Model:
        return _build_model(
            self.x, self.y, self.theta, self.side, delta=delta, ambiguity=self.cfg.ambiguity_tol
        )

    def solve(self, model: _Model, **kwargs: Any) -> np.ndarray | None:
        self.milp_solves += 1
        return _solve_model(model, time_limit=self.cfg.milp_time_limit, **kwargs)

    def line_search(self, u: np.ndarray, delta: float, threshold: float) -> float | None:
        """Move along `u`, halving; accept the first projected decrease over `threshold`."""
        n = self.n
        for h in range(self.cfg.line_search_halvings + 1):
            t = delta * 0.5**h
            theta = [self.theta[k] + t * float(u[1 + 2 * n + k]) for k in range(n)]
            xg = [self.x[k] + t * float(u[1 + k]) for k in range(n)]
            yg = [self.y[k] + t * float(u[1 + n + k]) for k in range(n)]
            got = self.project(theta, xg, yg)
            if got is not None and got[0] < self.side - threshold:
                self.side, self.x, self.y = got
                self.theta = theta
                return t
        return None

    def try_angle_move(self, theta: list[float], threshold: float) -> bool:
        got = self.project(theta, self.x, self.y)
        if got is not None and got[0] < self.side - threshold:
            self.side, self.x, self.y = got
            self.theta = theta
            return True
        return False

    def probe(self, deadline: float) -> str | None:
        """Look for descent the first-order model did not predict; name what found it."""
        for name, family in (
            ("flat-cone probe", self._cone_probes),
            ("random-direction probe", self._random_probes),
            ("single-angle probe", self._coordinate_probes),
        ):
            if family(deadline):
                return name
        return None

    def _cone_probes(self, deadline: float) -> bool:
        """Random directions in the first-order flat cone, projected by line search."""
        cfg, n = self.cfg, self.n
        delta = cfg.trust_radius
        base = self.solve(self.model(delta))
        cap = min((float(base[0]) if base is not None else 0.0) + 1e-7, 0.0)
        for _ in range(cfg.cone_probes):
            if time.monotonic() > deadline:
                return False
            model = self.model(delta)
            w = np.zeros(model.continuous)
            w[1 + 2 * n :] = [self.rng.gauss(0.0, 1.0) for _ in range(n)]
            w[1 : 1 + 2 * n] = [0.1 * self.rng.gauss(0.0, 1.0) for _ in range(2 * n)]
            u = self.solve(model, objective=-w, side_cap=cap)
            if u is None or float(np.max(np.abs(u[1 + 2 * n :]))) < 1e-6:
                continue
            if self.line_search(u, delta, cfg.step_tol) is not None:
                return True
        return False

    def _random_probes(self, deadline: float) -> bool:
        """Random joint angle moves at several step sizes, both signs."""
        cfg, n = self.cfg, self.n
        for _ in range(cfg.random_probes):
            if time.monotonic() > deadline:
                return False
            v = [self.rng.gauss(0.0, 1.0) for _ in range(n)]
            scale = max(abs(c) for c in v)
            v = [c / scale for c in v]
            for step in cfg.probe_steps:
                for sign in (1.0, -1.0):
                    theta = [t + sign * step * c for t, c in zip(self.theta, v, strict=True)]
                    if self.try_angle_move(theta, cfg.step_tol):
                        return True
        return False

    def _coordinate_probes(self, deadline: float) -> bool:
        """Every single angle moved alone, at each coordinate step, both signs."""
        cfg = self.cfg
        for k in range(self.n):
            if time.monotonic() > deadline:
                return False
            for step in cfg.coordinate_steps:
                for sign in (1.0, -1.0):
                    theta = list(self.theta)
                    theta[k] += sign * step
                    if self.try_angle_move(theta, cfg.step_tol):
                        return True
        return False


def descent_filter(
    x: list[float],
    y: list[float],
    theta: list[float],
    *,
    reference_side: float | None = None,
    config: DescentFilterConfig | None = None,
) -> DescentFilterResult:
    """Search the full pose space for a verified side decrease from one endpoint.

    The search starts at the fixed-angle cell optimum at the endpoint's own angles and
    descends until neither the first-order model nor the probes find a step, or the
    budget runs out. `reference_side` is the side the endpoint was reported at (a
    quench's LP side); without it the start's own LP side is the reference. The result
    is `rejected` once an exact witness lies more than `certify_tol` below the
    reference, and its terminal pose is descent-stable when `status == "stable"`.
    """
    cfg = config or DescentFilterConfig()
    started = time.monotonic()
    deadline = started + cfg.time_budget
    search = _Search(x, y, theta, cfg)
    first = search.project(search.theta, search.x, search.y)
    start_settled = first is not None
    if first is None:
        fp = solve_to_fixed_point(search.theta, search.x, search.y, search.n)
        search.side, search.x, search.y = fp.side, list(fp.x), list(fp.y)
    else:
        search.side, search.x, search.y = first
    start_side = search.side
    reference = reference_side if reference_side is not None else start_side
    certificate: ExactWitness | None = None
    certified: float | None = None
    history: list[dict[str, Any]] = []
    iterations = accepted = probes = 0
    delta = cfg.trust_radius
    status, reason = "budget", "iteration limit"

    def maybe_certify() -> None:
        nonlocal certificate, certified
        if certificate is not None or reference - search.side <= 2.0 * cfg.certify_tol:
            return
        witness = exact_witness(search.x, search.y, search.theta)
        if witness.valid and witness.side is not None:
            drop = reference - float(witness.side)
            if drop > cfg.certify_tol:
                certificate, certified = witness, drop

    maybe_certify()
    while iterations < cfg.max_iterations:
        if time.monotonic() > deadline:
            reason = "time budget"
            break
        iterations += 1
        u = search.solve(search.model(delta))
        predicted = float(u[0]) * delta if u is not None else 0.0
        if u is not None and predicted < -cfg.predicted_tol:
            before = search.side
            t = search.line_search(u, delta, cfg.step_tol)
            if t is not None:
                accepted += 1
                history.append(
                    {
                        "kind": "first-order",
                        "delta": delta,
                        "t": t,
                        "drop": before - search.side,
                    }
                )
                delta = min(2.0 * delta, cfg.trust_max) if t >= delta else max(t, cfg.trust_min)
                maybe_certify()
                continue
            if delta > cfg.trust_min:
                delta = max(delta / 10.0, cfg.trust_min)
                continue
        before = search.side
        found = search.probe(deadline)
        if found is not None:
            probes += 1
            history.append({"kind": found, "drop": before - search.side})
            delta = cfg.trust_radius
            maybe_certify()
            continue
        if time.monotonic() > deadline:
            reason = "time budget during probes"
            break
        status = "stable"
        reason = (
            "no first-order decrease and no probe decrease"
            if predicted >= -cfg.predicted_tol
            else "first-order decrease not realised at any radius; probes clean"
        )
        break
    terminal = exact_witness(search.x, search.y, search.theta)
    return DescentFilterResult(
        status=status,
        rejected=certificate is not None,
        reference_side=reference,
        start_side=start_side,
        start_settled=start_settled,
        terminal_side=search.side,
        certified_decrease=certified,
        certificate=certificate,
        terminal_witness=terminal,
        x=search.x,
        y=search.y,
        theta=search.theta,
        iterations=iterations,
        accepted_steps=accepted,
        probe_steps=probes,
        milp_solves=search.milp_solves,
        fixed_point_solves=search.fixed_point_solves,
        seconds=time.monotonic() - started,
        reason=reason,
        history=history[-50:],
    )


def rattling_squares(
    x: list[float],
    y: list[float],
    theta: list[float],
    side: float,
    *,
    turn: float = 1e-2,
    slack: float = 1e-10,
) -> list[int]:
    """Squares that can turn by `turn` radians, alone, without raising the side.

    Each square is turned by `+turn` and by `-turn` with every other angle held, and the
    centres are re-optimised by the fixed-angle LP. A square for which either turn leaves
    the side within `slack` of `side` is a rotational rattler at that scale: its
    orientation class is not forced by the packing. A finite-move test rather than a
    first-order one, because first-order flat directions are common at degenerate
    minima (Stromquist's family has them on most squares) and say nothing about whether
    a square is actually free.
    """
    n = len(x)
    free = []
    for k in range(n):
        for sign in (1.0, -1.0):
            turned = list(theta)
            turned[k] += sign * turn
            got = solve_to_fixed_point(turned, x, y, n)
            if got.settled and got.side <= side + slack:
                free.append(k)
                break
    return free
