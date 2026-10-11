"""Deterministic common-core first-order stress certificate for n17 (H-258).

Exact identities are proved with explicit-denominator rational functions over
QQ[t, b, ...] using polynomial-ring arithmetic: a value is zero exactly when its
numerator polynomial is zero. Signs over the accepted H-255 root box use a fixed
2^-256 outward dyadic interval grid. Target-free synthetic controls run, and must
pass, before any target input is read.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import time
from collections.abc import Mapping
from dataclasses import dataclass
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from typing import Any

from sympy import QQ
from sympy.polys.rings import ring

from devtools.bounded_diagnostics import same_content
from devtools.check_n17_contact_chart import ANCHORS, CONTACTS, SOURCE
from devtools.check_n17_endpoint_feasibility import (
    FROZEN_ROOT_REF,
    Box,
    _dot,
    _encode_receipt,
    _fraction_string,
    _layout,
    _object_unique,
    _read_limited,
    interval_geometry,
    require_retained_path,
    symbolic_identities,
)
from devtools.check_n17_endpoint_features import (
    AXES,
    FROZEN_ENDPOINT_REF,
    PARALLEL_PAIRS,
    interval_inventory,
    option_manifest,
    square_class,
    symbolic_zero_proofs,
)
from devtools.check_n17_root_certificate import CertificateError, n17_polynomials
from devtools.check_n17_root_certificate import check as check_root
from devtools.provenance import provenance

DIMENSION = 52
FACE_PAIRS = tuple(sorted(PARALLEL_PAIRS))
CROSS_PAIRS = tuple(
    (left, right)
    for left, right, _, _ in CONTACTS
    if tuple(sorted((left, right))) not in PARALLEL_PAIRS
)
ZERO_FORCE_PAIRS = frozenset({(9, 11)})
ZERO_FORCE_WALLS = frozenset({(6, "bottom"), (5, "right")})
FROZEN_FEATURE_REF = (
    "feafdae49:packing/campaign/series/series-000-smoke-and-calibration/"
    "results/exp-239-n17-endpoint-features/run-001/certificate.json"
)
INSTRUMENT_READY = True
AXIS_FACES = frozenset({(1, 2), (1, 3), (5, 7)})
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
GRID_BITS = 256
GRID = 1 << GRID_BITS
PROOF_GENERATORS = ("t", "b", "S", "mu", "nu", "rho")


class ExactField:
    """Rational functions with explicit factored denominators over QQ[t,b,S,mu,nu,rho].

    Every denominator is a product of registered monic irreducible polynomials, so a
    value is identically zero exactly when its numerator is the zero polynomial. No
    expression tree is expanded and no gcd is taken; denominators are cleared by ring
    multiplication only.
    """

    def __init__(self) -> None:
        polynomial_ring, *generators = ring(",".join(PROOF_GENERATORS), QQ)
        self.ring: Any = polynomial_ring
        self.generators: dict[str, Any] = dict(zip(PROOF_GENERATORS, generators, strict=True))
        self.factors: list[Any] = []

    def constant(self, value: int | Q) -> RationalFunction:
        if type(value) not in (int, Q):
            raise TypeError("exact constants must be int or Fraction")
        fraction = Q(value)
        return RationalFunction(
            self, self.ring(QQ(fraction.numerator, fraction.denominator)), {}
        )

    def generator(self, name: str) -> RationalFunction:
        return RationalFunction(self, self.generators[name], {})

    def register(self, numerator: Any) -> tuple[Any, dict[int, int]]:
        """Split a nonzero polynomial into a constant and registered monic factors."""
        coefficient, items = numerator.factor_list()
        product = self.ring(coefficient)
        exponents: dict[int, int] = {}
        for factor, multiplicity in items:
            product = product * factor**multiplicity
            leading = factor.LC
            monic = factor.quo_ground(leading)
            coefficient = coefficient * leading**multiplicity
            for index, known in enumerate(self.factors):
                if known == monic:
                    exponents[index] = exponents.get(index, 0) + multiplicity
                    break
            else:
                self.factors.append(monic)
                exponents[len(self.factors) - 1] = multiplicity
        if product != numerator:
            raise ValueError("denominator factorization does not reproduce its polynomial")
        return coefficient, exponents


class RationalFunction:
    """numerator / prod(factor_i ** exponent_i) with registered factors."""

    __slots__ = ("denominator", "field", "numerator")

    def __init__(self, field: ExactField, numerator: Any, denominator: dict[int, int]) -> None:
        self.field = field
        self.numerator = numerator
        self.denominator = {key: value for key, value in denominator.items() if value}

    def _lift(self, value: Any) -> RationalFunction:
        if isinstance(value, RationalFunction):
            if value.field is not self.field:
                raise ValueError("values from different exact fields were mixed")
            return value
        return self.field.constant(value)

    @property
    def is_zero(self) -> bool:
        return not self.numerator

    def reduced(self) -> RationalFunction:
        if not self.numerator:
            return RationalFunction(self.field, self.numerator, {})
        numerator, denominator = self.numerator, dict(self.denominator)
        for key, original in self.denominator.items():
            factor = self.field.factors[key]
            remaining = original
            while remaining:
                quotient, remainder = divmod(numerator, factor)
                if remainder:
                    break
                numerator, remaining = quotient, remaining - 1
            denominator[key] = remaining
        return RationalFunction(self.field, numerator, denominator)

    def __add__(self, other: Any) -> RationalFunction:
        rhs = self._lift(other)
        if not rhs.numerator:
            return self
        if not self.numerator:
            return rhs
        keys = self.denominator.keys() | rhs.denominator.keys()
        common = {
            key: max(self.denominator.get(key, 0), rhs.denominator.get(key, 0)) for key in keys
        }
        left, right = self.numerator, rhs.numerator
        for key, exponent in common.items():
            factor = self.field.factors[key]
            if exponent > self.denominator.get(key, 0):
                left = left * factor ** (exponent - self.denominator.get(key, 0))
            if exponent > rhs.denominator.get(key, 0):
                right = right * factor ** (exponent - rhs.denominator.get(key, 0))
        return RationalFunction(self.field, left + right, common).reduced()

    def __radd__(self, other: Any) -> RationalFunction:
        return self + other

    def __neg__(self) -> RationalFunction:
        return RationalFunction(self.field, -self.numerator, self.denominator)

    def __sub__(self, other: Any) -> RationalFunction:
        return self + -self._lift(other)

    def __rsub__(self, other: Any) -> RationalFunction:
        return self._lift(other) + -self

    def __mul__(self, other: Any) -> RationalFunction:
        rhs = self._lift(other)
        if not self.numerator or not rhs.numerator:
            return RationalFunction(self.field, self.field.ring.zero, {})
        keys = self.denominator.keys() | rhs.denominator.keys()
        combined = {
            key: self.denominator.get(key, 0) + rhs.denominator.get(key, 0) for key in keys
        }
        return RationalFunction(self.field, self.numerator * rhs.numerator, combined).reduced()

    def __rmul__(self, other: Any) -> RationalFunction:
        return self * other

    def inverse(self) -> RationalFunction:
        if not self.numerator:
            raise ZeroDivisionError("exact division by the zero rational function")
        coefficient, exponents = self.field.register(self.numerator)
        numerator = self.field.ring.one.quo_ground(coefficient)
        for key, exponent in self.denominator.items():
            numerator = numerator * self.field.factors[key] ** exponent
        return RationalFunction(self.field, numerator, exponents).reduced()

    def __truediv__(self, other: Any) -> RationalFunction:
        rhs = self._lift(other)
        if not self.numerator:
            return RationalFunction(self.field, self.field.ring.zero, {})
        return self * rhs.inverse()

    def __rtruediv__(self, other: Any) -> RationalFunction:
        return self._lift(other) / self

    def derivative(self, name: str) -> RationalFunction:
        """Exact partial derivative, all other generators held fixed."""
        variable = self.field.generators[name]
        result = RationalFunction(self.field, self.numerator.diff(variable), self.denominator)
        for key, exponent in self.denominator.items():
            factor = self.field.factors[key]
            result = result - self * RationalFunction(
                self.field, factor.diff(variable) * exponent, {key: 1}
            )
        return result


@dataclass(frozen=True)
class Dyadic(Box):
    """Closed interval on the fixed 2^-256 grid; every result is rounded outward."""

    def __post_init__(self) -> None:
        super().__post_init__()
        if (self.lo * GRID).denominator != 1 or (self.hi * GRID).denominator != 1:
            raise ValueError("interval endpoint is off the fixed 2^-256 grid")

    @classmethod
    def enclose(cls, lo: Q, hi: Q) -> Dyadic:
        """Round the lower endpoint down and the upper endpoint up, exactly."""
        return cls(Q(math.floor(lo * GRID), GRID), Q(math.ceil(hi * GRID), GRID))

    @classmethod
    def point(cls, value: int | Q) -> Dyadic:
        if type(value) not in (int, Q):
            raise ValueError("interval point must be exact integer or Fraction")
        return cls.enclose(Q(value), Q(value))

    @staticmethod
    def cast(value: Box | int | Q) -> Dyadic:
        if isinstance(value, Dyadic):
            return value
        if isinstance(value, Box):
            return Dyadic.enclose(value.lo, value.hi)
        return Dyadic.point(value)

    def __add__(self, other: Box | int | Q) -> Dyadic:
        rhs = self.cast(other)
        return Dyadic.enclose(self.lo + rhs.lo, self.hi + rhs.hi)

    def __neg__(self) -> Dyadic:
        return Dyadic(-self.hi, -self.lo)

    def __mul__(self, other: Box | int | Q) -> Dyadic:
        rhs = self.cast(other)
        values = (self.lo * rhs.lo, self.lo * rhs.hi, self.hi * rhs.lo, self.hi * rhs.hi)
        return Dyadic.enclose(min(values), max(values))

    def reciprocal(self) -> Dyadic:
        if self.lo <= 0 <= self.hi:
            raise ValueError("interval denominator includes zero")
        return Dyadic.enclose(1 / self.hi, 1 / self.lo)

    def absolute(self) -> Dyadic:
        if self.lo <= 0 <= self.hi:
            return Dyadic(Q(0), max(-self.lo, self.hi))
        return Dyadic(min(abs(self.lo), abs(self.hi)), max(abs(self.lo), abs(self.hi)))


def _coordinate(label: int, component: str) -> int:
    return 3 * (label - 1) + {"x": 0, "y": 1, "angle": 2}[component]


def _add(row: list[Any], label: int, component: str, value: Any) -> None:
    index = _coordinate(label, component)
    row[index] = row[index] + value


OMEGA_12 = _coordinate(12, "angle")
OMEGA_16 = _coordinate(16, "angle")
SIGMA = DIMENSION - 1


CORNER_SIGNS: dict[tuple[int, int], tuple[int, int]] = {
    (3, 9): (1, 1),
    (4, 10): (1, -1),
    (3, 11): (1, 1),
    (2, 13): (1, 1),
    (10, 15): (1, 1),
    (14, 17): (1, 1),
    (15, 16): (1, -1),
    (16, 8): (1, 1),
    (14, 7): (1, -1),
    (16, 17): (1, -1),
    (12, 16): (1, 1),
}


def _corner_offset(
    pair: tuple[int, int], normal: tuple[Any, Any], aux: dict[str, Any], half: Any
) -> tuple[Any, Any]:
    left, right = pair
    sorted_pair = tuple(sorted(pair))
    owner = next(
        row["owner"]
        for row in option_manifest()
        if (row["left"], row["right"]) == sorted_pair and row["kind"] == "identity"
    )
    other = right if owner == left else left
    first, second = (aux[name] for name in AXES[square_class(other)])
    a, b = CORNER_SIGNS[pair]
    for vector, expected in ((first, a), (second, b)):
        projection = _dot(normal, vector)
        if isinstance(projection, Box) and not (
            projection.lo > 0 if expected > 0 else projection.hi < 0
        ):
            raise ValueError(f"unsupported cross-contact support branch: {pair}")
    return (
        half * (a * first[0] + b * second[0]),
        half * (a * first[1] + b * second[1]),
    )


def _wall_rows(label: int, wall: str, aux: dict[str, Any], half: Any) -> tuple[list[Any], ...]:
    if (label, wall) not in ANCHORS:
        raise ValueError("wall is not active")
    if label == 9:
        if wall != "left":
            raise ValueError("unexpected oblique wall")
        row = [0] * DIMENSION
        _add(row, label, "x", 1)
        _add(row, label, "angle", -(aux["c"] - aux["s"]) / 2)
        return (row,)
    result: list[list[Any]] = []
    for angle_sign in (-1, 1):
        row = [0] * DIMENSION
        component = "x" if wall in ("left", "right") else "y"
        _add(row, label, component, 1 if wall in ("left", "bottom") else -1)
        _add(row, label, "angle", angle_sign * half)
        if wall in ("right", "top"):
            row[-1] = 1
        result.append(row)
    return tuple(result)


def _pair_rows(
    pair: tuple[int, int],
    axis: str,
    aux: dict[str, Any],
    centres: tuple[tuple[Any, Any], ...],
    half: Any,
) -> tuple[list[Any], ...]:
    left, right = pair
    normal = aux[axis]
    tangent = (-normal[1], normal[0])
    displacement = (
        centres[right - 1][0] - centres[left - 1][0],
        centres[right - 1][1] - centres[left - 1][1],
    )
    translation = [0] * DIMENSION
    for component, value in zip(("x", "y"), normal, strict=True):
        _add(translation, right, component, value)
        _add(translation, left, component, -value)
    if pair in PARALLEL_PAIRS:
        tau = _dot(tangent, displacement)
        # All nonzero declared offsets have a strictly positive root branch.
        k = (1 - tau) / 2
        if pair in {(1, 2), (1, 3), (5, 7)}:
            k = half
        minus, plus = translation.copy(), translation.copy()
        _add(minus, left, "angle", tau / 2 + k)
        _add(minus, right, "angle", tau / 2 - k)
        _add(plus, left, "angle", tau / 2 - k)
        _add(plus, right, "angle", tau / 2 + k)
        return minus, plus
    sorted_pair = tuple(sorted(pair))
    owner = next(
        row["owner"]
        for row in option_manifest()
        if (row["left"], row["right"]) == sorted_pair and row["kind"] == "identity"
    )
    other = right if owner == left else left
    corner = _corner_offset(pair, normal, aux, half)
    hprime = _dot(tangent, corner)
    _add(translation, owner, "angle", _dot(tangent, displacement) - hprime)
    _add(translation, other, "angle", hprime)
    return (translation,)


def common_rows(
    t: Any, b: Any, half: Any
) -> tuple[dict[tuple[Any, ...], list[Any]], Any, dict[str, Any]]:
    side, aux, centres = _layout(t, b, half)
    rows: dict[tuple[Any, ...], list[Any]] = {}
    for label, wall in ANCHORS:
        for variant, row in enumerate(_wall_rows(label, wall, aux, half)):
            rows["wall", label, wall, variant] = row
    for left, right, axis, _ in CONTACTS:
        for variant, row in enumerate(_pair_rows((left, right), axis, aux, centres, half)):
            rows["pair", left, right, variant] = row
    if len(rows) != 58:
        raise ValueError(f"common core requires 58 rows, got {len(rows)}")
    return rows, side, aux


def load_scales(
    side: Any, aux: dict[str, Any], formal: tuple[Any, Any, Any] | None = None
) -> dict[str, Any]:
    """Frozen partial-angle derivatives, evaluated only after fixing the side."""
    c, s, d, e = (aux[name] for name in ("c", "s", "d", "e"))
    alpha, gamma = aux["alpha"], aux["gamma"]
    p = side - 2 - s + (s * (side - 3) - 2) / c
    q = side - 3 + (c * (side - 3) - 2) / s
    p_theta = (side - 3 - 2 * s) / (c * c) - c
    q_theta = (2 * c - side + 3) / (s * s)
    f1_theta = -s * (side - 3) + c * (side - 2)
    f2_theta = d * p_theta + e * q_theta
    f2_beta = -e * p + d * q
    g3_theta = (
        c * (side - 3) - s * (side - 2) + e * alpha * q_theta - e * gamma * q + gamma - alpha
    )
    g3_beta = gamma - alpha + q * (alpha * d - gamma * e)
    nu, rho = g3_beta, -f2_beta
    mu = -(nu * f2_theta + rho * g3_theta) / f1_theta
    if formal is not None:
        mu, nu, rho = formal
    z = nu + alpha * rho
    ell = nu * d / c
    r = z * e / s
    k = (c + s) * mu + gamma * nu / c + gamma * z / s + gamma * rho * (d + e)
    return {
        "P": p,
        "Q": q,
        "F1_theta": f1_theta,
        "F2_theta": f2_theta,
        "F2_beta": f2_beta,
        "G3_theta": g3_theta,
        "G3_beta": g3_beta,
        "mu": mu,
        "nu": nu,
        "rho": rho,
        "Z": z,
        "L": ell,
        "R": r,
        "K": k,
    }


def force_roster(
    aux: dict[str, Any], scales: dict[str, Any]
) -> tuple[dict[tuple[int, int], Any], dict[tuple[int, str], Any]]:
    c, s, d, e = (aux[name] for name in ("c", "s", "d", "e"))
    gamma = aux["gamma"]
    mu, nu, rho = (scales[name] for name in ("mu", "nu", "rho"))
    z, ell, r = (scales[name] for name in ("Z", "L", "R"))
    pair = {
        (1, 2): c * r,
        (1, 3): s * (ell + rho),
        (5, 7): c * mu,
        (3, 9): s * ell,
        (9, 10): ell,
        (4, 10): mu,
        (3, 11): rho,
        (11, 12): rho,
        (10, 12): mu,
        (2, 13): r,
        (13, 14): r,
        (12, 14): mu,
        (10, 15): ell,
        (14, 17): r,
        (15, 16): nu,
        (16, 8): gamma * rho,
        (14, 7): mu,
        (16, 17): z,
        (12, 16): rho,
        (9, 11): 0,
    }
    wall = {
        (1, "left"): c * r,
        (1, "bottom"): s * (ell + rho),
        (2, "bottom"): s * r,
        (3, "left"): c * rho,
        (4, "left"): s * mu,
        (4, "top"): c * mu,
        (5, "bottom"): c * mu,
        (5, "right"): 0,
        (6, "bottom"): 0,
        (7, "right"): s * mu,
        (8, "right"): e * gamma * rho,
        (8, "top"): d * gamma * rho,
        (9, "left"): c * ell,
        (15, "top"): gamma * nu / c,
        (17, "right"): gamma * z / s,
    }
    if set(pair) != {(left, right) for left, right, _, _ in CONTACTS} or len(wall) != 15:
        raise ValueError("incomplete normal-force roster")
    return pair, wall


def deterministic_weights(
    rows: dict[tuple[Any, ...], list[Any]],
    side: Any,
    aux: dict[str, Any],
    centres: tuple[tuple[Any, Any], ...],
    half: Any,
    *,
    formal: tuple[Any, Any, Any] | None = None,
    normalize: bool = True,
) -> tuple[
    dict[tuple[Any, ...], Any],
    dict[str, Any],
    dict[tuple[int, int], Any],
    dict[tuple[int, str], Any],
]:
    """Assemble the immutable force/moment recipe, including six zero rows."""
    scales = load_scales(side, aux, formal)
    pair_forces, wall_forces = force_roster(aux, scales)
    c, s, d, e, gamma = (aux[name] for name in ("c", "s", "d", "e", "gamma"))
    mu, nu, rho = (scales[name] for name in ("mu", "nu", "rho"))
    z, ell, r = (scales[name] for name in ("Z", "L", "R"))
    b2 = r * (c - s) / 2
    b3 = s * ell * (half - s) + rho * (c - s) / 2
    b7 = mu * (c - s) / 2
    wall_moments = {
        (1, "left"): -b2,
        (1, "bottom"): -b3,
        (2, "bottom"): 0,
        (3, "left"): 0,
        (4, "left"): 0,
        (4, "top"): -b7,
        (5, "bottom"): -b7,
        (5, "right"): 0,
        (6, "bottom"): 0,
        (7, "right"): 0,
        (8, "right"): 0,
        (8, "top"): gamma * rho * (d - e) / 2,
        (15, "top"): nu * (d * s / c - e) / 2,
        (17, "right"): z * (d - e * c / s) / 2,
    }
    moments: dict[tuple[int, int], Any] = {
        (1, 2): b2,
        (1, 3): b3,
        (5, 7): b7,
        (9, 11): 0,
    }

    def assembled(moment_map: dict[tuple[int, int], Any]) -> dict[tuple[Any, ...], Any]:
        weights: dict[tuple[Any, ...], Any] = {}
        for (label, wall), force in wall_forces.items():
            if label == 9:
                weights["wall", label, wall, 0] = force
            else:
                moment = wall_moments[label, wall]
                weights["wall", label, wall, 0] = force * half - moment
                weights["wall", label, wall, 1] = force * half + moment
        for pair, force in pair_forces.items():
            if pair in PARALLEL_PAIRS:
                axis = next(axis for left, right, axis, _ in CONTACTS if (left, right) == pair)
                n = aux[axis]
                tangent = (-n[1], n[0])
                tau = _dot(
                    tangent,
                    (
                        centres[pair[1] - 1][0] - centres[pair[0] - 1][0],
                        centres[pair[1] - 1][1] - centres[pair[0] - 1][1],
                    ),
                )
                k = half if pair in {(1, 2), (1, 3), (5, 7)} else (1 - tau) / 2
                moment = moment_map.get(pair, 0)
                weights["pair", *pair, 0] = (force + moment / k) * half
                weights["pair", *pair, 1] = (force - moment / k) * half
            else:
                weights["pair", *pair, 0] = force
        if set(weights) != set(rows):
            raise ValueError("weight roster does not cover every common row")
        return weights

    baseline = assembled(moments)
    angular_residual = {
        label: sum(
            (
                weight * rows[key][_coordinate(label, "angle")]
                for key, weight in baseline.items()
            ),
            0,
        )
        for label in range(9, 15)
    }
    moments.update(
        {
            (9, 10): -angular_residual[9],
            (10, 12): -angular_residual[9] - angular_residual[10],
            (11, 12): -angular_residual[11],
            (13, 14): -angular_residual[13],
            (12, 14): angular_residual[13] + angular_residual[14],
        }
    )
    if set(moments) != set(PARALLEL_PAIRS):
        raise ValueError("incomplete parallel-face moment roster")
    weights = assembled(moments)
    final_weights = (
        {key: weight / scales["K"] for key, weight in weights.items()} if normalize else weights
    )
    return final_weights, scales, moments, wall_moments


def complete_stress(
    t: Any,
    b: Any,
    half: Any,
    *,
    formal: tuple[Any, Any, Any] | None = None,
    normalize: bool = True,
) -> tuple[
    dict[tuple[Any, ...], list[Any]], dict[tuple[Any, ...], Any], dict[str, Any], list[Any]
]:
    side, aux, centres = _layout(t, b, half)
    rows, _, _ = common_rows(t, b, half)
    weights, scales, _, _ = deterministic_weights(
        rows, side, aux, centres, half, formal=formal, normalize=normalize
    )
    residuals = [
        sum((weights[key] * row[column] for key, row in rows.items()), 0)
        - ((1 if normalize else scales["K"]) if column == DIMENSION - 1 else 0)
        for column in range(DIMENSION)
    ]
    return rows, weights, scales, residuals


def _block_residuals(
    rows: dict[tuple[Any, ...], list[Any]],
    aux: dict[str, Any],
    centres: tuple[tuple[Any, Any], ...],
    scales: dict[str, Any],
    *,
    face_moments: dict[tuple[int, int], Any],
    wall_moments: dict[tuple[int, str], Any],
) -> list[Any]:
    """Cancel each tied two-row block algebraically before column summation."""
    pair_forces, wall_forces = force_roster(aux, scales)
    residuals = [0] * DIMENSION
    for (label, wall), force in wall_forces.items():
        if label == 9:
            row = rows["wall", label, wall, 0]
            for column, coefficient in enumerate(row):
                residuals[column] += force * coefficient
            continue
        component = "x" if wall in ("left", "right") else "y"
        position = _coordinate(label, component)
        residuals[position] += force if wall in ("left", "bottom") else -force
        if wall in ("right", "top"):
            residuals[-1] += force
        residuals[_coordinate(label, "angle")] += wall_moments[label, wall]
    for left, right, axis, _ in CONTACTS:
        pair = (left, right)
        force = pair_forces[pair]
        if pair not in PARALLEL_PAIRS:
            row = rows["pair", left, right, 0]
            for column, coefficient in enumerate(row):
                residuals[column] += force * coefficient
            continue
        normal = aux[axis]
        for component, value in zip(("x", "y"), normal, strict=True):
            residuals[_coordinate(left, component)] -= force * value
            residuals[_coordinate(right, component)] += force * value
        tangent = (-normal[1], normal[0])
        tau = _dot(
            tangent,
            (
                centres[right - 1][0] - centres[left - 1][0],
                centres[right - 1][1] - centres[left - 1][1],
            ),
        )
        moment = face_moments[pair]
        residuals[_coordinate(left, "angle")] += force * tau / 2 + moment
        residuals[_coordinate(right, "angle")] += force * tau / 2 - moment
    residuals[-1] -= scales["K"]
    return residuals


def _vanishes(value: Any) -> bool:
    """Exact zero test: a ring value by its numerator, a literal by equality."""
    if isinstance(value, RationalFunction):
        return value.is_zero
    if type(value) in (int, Q):
        return value == 0
    raise TypeError(f"identity check requires an exact ring value, got {type(value)}")


def _verify_tied_row_shapes(
    rows: dict[tuple[Any, ...], list[Any]],
    aux: dict[str, Any],
    centres: tuple[tuple[Any, Any], ...],
) -> int:
    """Bind the block cancellation to each retained physical row."""
    checked = 0
    for label, wall in ANCHORS:
        if label == 9:
            continue
        minus, plus = rows["wall", label, wall, 0], rows["wall", label, wall, 1]
        component = "x" if wall in ("left", "right") else "y"
        expected = [0] * DIMENSION
        expected[_coordinate(label, component)] = 2 if wall in ("left", "bottom") else -2
        expected[-1] = 2 if wall in ("right", "top") else 0
        for column in range(DIMENSION):
            if not _vanishes(minus[column] + plus[column] - expected[column]):
                raise ValueError(f"wall row sum changed: {(label, wall, column)}")
            difference = -1 if column == _coordinate(label, "angle") else 0
            if not _vanishes(minus[column] - plus[column] - difference):
                raise ValueError(f"wall row difference changed: {(label, wall, column)}")
        checked += 1
    for left, right, axis, _ in CONTACTS:
        if (left, right) not in PARALLEL_PAIRS:
            continue
        minus, plus = rows["pair", left, right, 0], rows["pair", left, right, 1]
        normal = aux[axis]
        tangent = (-normal[1], normal[0])
        tau = _dot(
            tangent,
            (
                centres[right - 1][0] - centres[left - 1][0],
                centres[right - 1][1] - centres[left - 1][1],
            ),
        )
        k = Q(1, 2) if (left, right) in AXIS_FACES else (1 - tau) / 2
        expected_sum: list[Any] = [0] * DIMENSION
        expected_diff: list[Any] = [0] * DIMENSION
        for component, value in zip(("x", "y"), normal, strict=True):
            expected_sum[_coordinate(left, component)] = -2 * value
            expected_sum[_coordinate(right, component)] = 2 * value
        expected_sum[_coordinate(left, "angle")] = tau
        expected_sum[_coordinate(right, "angle")] = tau
        expected_diff[_coordinate(left, "angle")] = 2 * k
        expected_diff[_coordinate(right, "angle")] = -2 * k
        for column in range(DIMENSION):
            if not _vanishes(minus[column] + plus[column] - expected_sum[column]):
                raise ValueError(f"face row sum changed: {(left, right, column)}")
            if not _vanishes(minus[column] - plus[column] - expected_diff[column]):
                raise ValueError(f"face row difference changed: {(left, right, column)}")
        checked += 1
    if checked != 23:
        raise ValueError("tied-row shape coverage incomplete")
    return checked


def _generic_block_identities() -> int:
    """The two tied-row cancellations as polynomial identities, k cleared explicitly."""
    _, f, q, k, ell, dw, m, a, omega = ring("f,q,k,ell,dw,m,a,omega", QQ)
    face = (
        (f * k + q) * (ell - k * dw) + (f * k - q) * (ell + k * dw) - 2 * k * (f * ell - q * dw)
    )
    wall = (
        (f - 2 * m) * (2 * a - omega) + (f + 2 * m) * (2 * a + omega) - 4 * (f * a + m * omega)
    )
    if face or wall:
        raise ValueError("generic two-row block cancellation failed")
    return 2


def _closing_f2(side: Any, aux: dict[str, Any]) -> Any:
    return aux["d"] * (side - aux["X"] - Q(3, 2)) - aux["e"] * (aux["Y"] - side + Q(3, 2)) - 1


def identity_failures(
    rows: dict[tuple[Any, ...], list[Any]],
    weights: dict[tuple[Any, ...], Any],
    side_coefficient: Any,
    expected_twelve: Any,
    expected_sixteen: Any,
) -> list[int]:
    """Columns where the full-matrix sum of weight times row misses its prescription."""
    failures: list[int] = []
    for column in range(DIMENSION):
        total = sum((weights[key] * row[column] for key, row in rows.items()), 0)
        expected = (
            side_coefficient
            if column == SIGMA
            else expected_twelve
            if column == OMEGA_12
            else expected_sixteen
            if column == OMEGA_16
            else 0
        )
        if not _vanishes(total - expected):
            failures.append(column)
    return failures


def _formal_model(
    field: ExactField,
) -> tuple[Any, dict[str, Any], tuple[tuple[Any, Any], ...], dict[tuple[Any, ...], list[Any]]]:
    half = field.constant(Q(1, 2))
    t, b = field.generator("t"), field.generator("b")
    side, aux, centres = _layout(t, b, half)
    rows, _, _ = common_rows(t, b, half)
    return side, aux, centres, rows


def _formal_loads(field: ExactField) -> tuple[Any, Any, Any]:
    return field.generator("mu"), field.generator("nu"), field.generator("rho")


def _formal_expectations(
    loads: tuple[Any, Any, Any], side: Any, aux: dict[str, Any], scales: dict[str, Any]
) -> tuple[Any, Any]:
    mu, nu, rho = loads
    f2 = _closing_f2(side, aux)
    twelve = (
        mu * scales["F1_theta"]
        + nu * scales["F2_theta"]
        + rho * scales["G3_theta"]
        + aux["gamma"] * rho * f2
    )
    sixteen = -(nu * scales["F2_beta"] + rho * scales["G3_beta"] + aux["gamma"] * rho * f2)
    return twelve, sixteen


@dataclass(frozen=True)
class RingProof:
    summary: dict[str, Any]
    denominators: tuple[Any, ...]


@lru_cache(maxsize=2)
def ring_residual_proofs(*, substituted: bool = True) -> RingProof:
    """Prove every H-258 identity in Q[t, b, mu, nu, rho] with explicit denominators.

    The formal stage keeps mu, nu, rho as ring generators, as the frozen derivation's
    short proof does. The substituted stage replaces them by the fixed loads and checks
    the normalized 52-column identity directly. A failed identity raises.
    """
    stages: dict[str, float] = {}
    started = time.monotonic()
    field = ExactField()
    side, aux, centres, rows = _formal_model(field)
    half = field.constant(Q(1, 2))
    stages["model"] = time.monotonic() - started
    mark = time.monotonic()
    tied_row_shapes = _verify_tied_row_shapes(rows, aux, centres)
    generic = _generic_block_identities()
    stages["row_shapes"] = time.monotonic() - mark
    mark = time.monotonic()
    loads = _formal_loads(field)
    weights, scales, face_moments, wall_moments = deterministic_weights(
        rows, side, aux, centres, half, formal=loads, normalize=False
    )
    twelve, sixteen = _formal_expectations(loads, side, aux, scales)
    block = _block_residuals(
        rows, aux, centres, scales, face_moments=face_moments, wall_moments=wall_moments
    )
    block_failures = [
        column
        for column, value in enumerate(block)
        if not _vanishes(
            value - (twelve if column == OMEGA_12 else sixteen if column == OMEGA_16 else 0)
        )
    ]
    formal_failures = identity_failures(rows, weights, scales["K"], twelve, sixteen)
    formal_zero = [key for key in ZERO_WEIGHT_KEYS if not _vanishes(weights[key])]
    stages["formal_identities"] = time.monotonic() - mark
    mark = time.monotonic()
    fixed = load_scales(side, aux)
    load_balance = [
        _vanishes(fixed["nu"] * fixed["F2_beta"] + fixed["rho"] * fixed["G3_beta"]),
        _vanishes(
            fixed["mu"] * fixed["F1_theta"]
            + fixed["nu"] * fixed["F2_theta"]
            + fixed["rho"] * fixed["G3_theta"]
        ),
    ]
    t, b = field.generator("t"), field.generator("b")
    pi2 = sum(
        (
            coefficient * _power(t, i) * _power(b, j)
            for (i, j), coefficient in n17_polynomials()[0].items()
        ),
        field.constant(0),
    )
    f2 = _closing_f2(side, aux)
    f2_binding = _vanishes(f2 * t * (1 + t) * (1 + t * t) * (1 + b * b) - pi2)
    stages["load_balance"] = time.monotonic() - mark
    substituted_failures: list[int] | None = None
    substituted_zero: list[tuple[Any, ...]] | None = None
    if substituted:
        mark = time.monotonic()
        normalized, fixed_scales, _, _ = deterministic_weights(rows, side, aux, centres, half)
        exceptional = aux["gamma"] * fixed_scales["rho"] * f2 / fixed_scales["K"]
        substituted_failures = identity_failures(rows, normalized, 1, exceptional, -exceptional)
        substituted_zero = [key for key in ZERO_WEIGHT_KEYS if not _vanishes(normalized[key])]
        stages["substituted_identities"] = time.monotonic() - mark
    denominators = tuple(field.factors)
    foreign = [
        str(factor)
        for factor in denominators
        if any(any(monomial[2:]) for monomial in factor.monoms())
    ]
    passed = (
        not block_failures
        and not formal_failures
        and not formal_zero
        and all(load_balance)
        and f2_binding
        and not substituted_failures
        and not substituted_zero
        and not foreign
    )
    summary = {
        "method": "explicit-denominator rational functions over QQ[t,b,S,mu,nu,rho]; "
        "identity iff numerator polynomial is zero",
        "rows": len(rows),
        "columns": DIMENSION,
        "tied_row_shapes": tied_row_shapes,
        "generic_block_identities": generic,
        "block_residual_failures": block_failures,
        "formal_full_matrix_failures": formal_failures,
        "formal_zero_weight_failures": [list(key) for key in formal_zero],
        "load_balance_identities": load_balance,
        "f2_to_h255_pi2_binding": f2_binding,
        "substituted_normalized": substituted,
        "substituted_full_matrix_failures": substituted_failures,
        "substituted_zero_weight_failures": None
        if substituted_zero is None
        else [list(key) for key in substituted_zero],
        "zero_residual_identities": DIMENSION - 2,
        "exceptional_F2_identities": 2,
        "prescribed_zero_weights": len(ZERO_WEIGHT_KEYS),
        "denominator_factors": [
            {"degree_t": factor.degree(0), "degree_b": factor.degree(1), "terms": len(factor)}
            for factor in denominators
        ],
        "denominators_outside_t_b": foreign,
        "stage_seconds": stages,
        "seconds": time.monotonic() - started,
        "passed": passed,
    }
    if not passed:
        raise ValueError(f"common-core stationarity identity failed: {summary}")
    return RingProof(summary, denominators)


def _power(value: Any, exponent: int) -> Any:
    result: Any = 1
    for _ in range(exponent):
        result = result * value
    return result


@lru_cache(maxsize=1)
def symbolic_residual_proofs() -> dict[str, Any]:
    """Prove the full coefficient identity as rational functions before root use."""
    foundation_started = time.monotonic()
    foundation = symbolic_identities()
    foundation_seconds = time.monotonic() - foundation_started
    proof = ring_residual_proofs()
    return {
        "foundation": foundation,
        "foundation_seconds": foundation_seconds,
        "rows": 58,
        "columns": DIMENSION,
        "zero_residual_identities": 50,
        "exceptional_F2_identities": 2,
        "prescribed_zero_weights": len(ZERO_WEIGHT_KEYS),
        "tied_row_shapes": proof.summary["tied_row_shapes"],
        "ring": proof.summary,
    }


def _polynomial_interval(polynomial: Any, t: Box, b: Box) -> Box:
    total: Box = Dyadic.point(0)
    for monomial, coefficient in polynomial.terms():
        if any(monomial[2:]):
            raise ValueError("denominator factor depends on a load or side generator")
        term: Box = Dyadic.point(Q(int(coefficient.numerator), int(coefficient.denominator)))
        term = term * _power(t, monomial[0]) * _power(b, monomial[1])
        total = total + term
    return total


def _root_intervals(midpoint: tuple[Q, Q], radii: tuple[Q, Q]) -> tuple[Box, Box]:
    if len(midpoint) != 2 or len(radii) != 2:
        raise ValueError("root enclosure must have two dimensions")
    if any(type(value) is not Q for value in (*midpoint, *radii)) or any(
        radius <= 0 for radius in radii
    ):
        raise ValueError("invalid exact root enclosure")
    t, b = (
        Dyadic.enclose(value - radius, value + radius)
        for value, radius in zip(midpoint, radii, strict=True)
    )
    return t, b


def denominator_guards(
    factors: tuple[Any, ...], midpoint: tuple[Q, Q], radii: tuple[Q, Q]
) -> dict[str, Any]:
    """Every ring-proof denominator factor keeps one strict sign on the root box."""
    t, b = _root_intervals(midpoint, radii)
    signs: list[int] = []
    for index, factor in enumerate(factors):
        bound = _polynomial_interval(factor, t, b)
        if bound.lo <= 0 <= bound.hi:
            raise ValueError(
                f"ring-proof denominator factor {index} may vanish on the root box"
            )
        signs.append(1 if bound.lo > 0 else -1)
    return {"factors": len(factors), "signs": signs, "passed": True}


def classify_signs(bounds: Mapping[str, Box]) -> tuple[str, list[str]]:
    """Frozen disposition: certified negative rejects; straddling zero is unresolved."""
    failures = [key for key, bound in bounds.items() if bound.lo < 0]
    negative = any(bound.hi < 0 for bound in bounds.values())
    disposition = (
        "confirmed_fixed_stress"
        if not failures
        else "rejected_fixed_candidate"
        if negative
        else "unresolved_interval_sign"
    )
    return disposition, failures


def interval_sign_audit(midpoint: tuple[Q, Q], radii: tuple[Q, Q]) -> dict[str, Any]:
    """Check the fixed stress on the entire accepted root enclosure, 2^-256 outward."""
    t, b = _root_intervals(midpoint, radii)
    half = Dyadic.point(Q(1, 2))
    side, aux, centres = _layout(t, b, half)
    rows, _, _ = common_rows(t, b, half)
    weights, scales, moments, _ = deterministic_weights(rows, side, aux, centres, half)
    guards = {key: aux[key] for key in ("c", "s", "d", "e", "alpha", "gamma", "T")}
    guards.update(
        {key: scales[key] for key in ("F1_theta", "mu", "nu", "rho", "Z", "L", "R", "K")}
    )
    for key, bound in guards.items():
        if bound.lo <= 0:
            raise ValueError(f"strict stress denominator/force guard failed: {key}")
    tau_bounds: dict[tuple[int, int], Box] = {}
    capacities: dict[tuple[int, int], tuple[Box, Box]] = {}
    pair_forces, _ = force_roster(aux, scales)
    for left, right, axis, _ in CONTACTS:
        pair = (left, right)
        if pair not in PARALLEL_PAIRS:
            continue
        n = aux[axis]
        tau = _dot(
            (-n[1], n[0]),
            (
                centres[right - 1][0] - centres[left - 1][0],
                centres[right - 1][1] - centres[left - 1][1],
            ),
        )
        if pair not in AXIS_FACES and tau.lo <= 0:
            raise ValueError(f"positive parallel offset branch failed: {pair}")
        if tau.lo <= -1 or tau.hi >= 1:
            raise ValueError(f"parallel face offset escaped interior: {pair}")
        tau_bounds[pair] = tau
        k = half if pair in AXIS_FACES else (1 - tau) / 2
        force, moment = pair_forces[pair], moments[pair]
        capacities[pair] = (k * force + moment, k * force - moment)
    if len(tau_bounds) != 9:
        raise ValueError("parallel offset coverage incomplete")
    for key in ZERO_WEIGHT_KEYS:
        if (weights[key].lo, weights[key].hi) != (0, 0):
            raise ValueError(f"prescribed zero weight is not an exact zero interval: {key}")
    signed: dict[str, Box] = {f"weight.{key}": bound for key, bound in weights.items()}
    signed.update(
        {
            f"capacity.{pair}.{sign}": bound
            for pair, bounds in capacities.items()
            for sign, bound in zip(("plus", "minus"), bounds, strict=True)
        }
    )
    disposition, failures = classify_signs(signed)
    positive = [bound for key, bound in weights.items() if key not in ZERO_WEIGHT_KEYS]
    return {
        "grid_bits": GRID_BITS,
        "row_order": [list(key) for key in rows],
        "weight_bounds": {str(key): weights[key].as_json() for key in rows},
        "guard_bounds": {key: bound.as_json() for key, bound in guards.items()},
        "parallel_offsets": {str(key): bound.as_json() for key, bound in tau_bounds.items()},
        "moment_capacities": {
            str(key): [bound.as_json() for bound in bounds]
            for key, bounds in capacities.items()
        },
        "weights": len(weights),
        "nonnegative_weights": sum(bound.lo >= 0 for bound in weights.values()),
        "strictly_positive_weights": sum(bound.lo > 0 for bound in positive),
        "minimum_positive_weight_lower_bound": float(min(bound.lo for bound in positive)),
        "minimum_capacity_lower_bound": float(
            min(bound.lo for bounds in capacities.values() for bound in bounds)
        ),
        "passed": not failures,
        "disposition": disposition,
        "failures": failures,
    }


@dataclass(frozen=True)
class _Jet:
    """First-order one-sided jet value + slope*epsilon with exact rational parts."""

    value: Q
    slope: Q

    def __add__(self, other: _Jet) -> _Jet:
        return _Jet(self.value + other.value, self.slope + other.slope)

    def __sub__(self, other: _Jet) -> _Jet:
        return _Jet(self.value - other.value, self.slope - other.slope)

    def __mul__(self, other: _Jet) -> _Jet:
        return _Jet(
            self.value * other.value, self.value * other.slope + self.slope * other.value
        )

    def magnitude(self) -> _Jet:
        if self.value:
            return self if self.value > 0 else _Jet(-self.value, -self.slope)
        return _Jet(Q(0), abs(self.slope))


def _jet_max(first: _Jet, second: _Jet) -> _Jet:
    if first.value != second.value:
        return first if first.value > second.value else second
    return _Jet(first.value, max(first.slope, second.slope))


def _rotating(vector: tuple[Q, Q], omega: Q) -> tuple[_Jet, _Jet]:
    return _Jet(vector[0], -omega * vector[1]), _Jet(vector[1], omega * vector[0])


def _owner_gap(
    normal: tuple[Q, Q],
    owner_omega: Q,
    displacement: tuple[_Jet, _Jet],
    other_axes: tuple[tuple[Q, Q], tuple[Q, Q]],
    other_omega: Q,
) -> _Jet:
    """Exact owner-axis gap: rotating owner normal, rotating nonowner support."""
    n = _rotating(normal, owner_omega)
    projection = n[0] * displacement[0] + n[1] * displacement[1]
    support = _Jet(Q(0), Q(0))
    for axis in other_axes:
        turned = _rotating(axis, other_omega)
        support = support + (n[0] * turned[0] + n[1] * turned[1]).magnitude()
    return projection - _Jet(Q(1, 2), Q(0)) - support * _Jet(Q(1, 2), Q(0))


def _velocity(labels: tuple[int, int], values: tuple[tuple[Q, Q, Q], ...]) -> list[Q]:
    vector = [Q(0)] * DIMENSION
    for label, (x, y, angle) in zip(labels, values, strict=True):
        vector[_coordinate(label, "x")] = x
        vector[_coordinate(label, "y")] = y
        vector[_coordinate(label, "angle")] = angle
    return vector


def _row_value(row: list[Any], velocity: list[Q]) -> Q:
    return sum((Q(entry) * value for entry, value in zip(row, velocity, strict=True)), Q(0))


VELOCITY_CASES: tuple[tuple[tuple[Q, Q, Q], tuple[Q, Q, Q]], ...] = (
    ((Q(1, 7), Q(-2, 9), Q(1, 3)), (Q(3, 11), Q(1, 5), Q(5, 4))),
    ((Q(-1, 7), Q(2, 9), Q(5, 4)), (Q(3, 11), Q(-1, 5), Q(-1, 3))),
    ((Q(1, 13), Q(1, 17), Q(2, 7)), (Q(-1, 19), Q(1, 23), Q(2, 7))),
)


def _row_derivative_controls() -> dict[str, Any]:
    """Exact first-order owner gaps against the tool's reduced rows."""
    half = Q(1, 2)
    unit = (Q(3, 5), Q(4, 5))
    results: dict[str, Any] = {}
    parallel = [((9, 10), "u", unit, offset) for offset in (Q(1, 3), Q(7, 8), Q(1))]
    parallel.append(((1, 3), "ey", (Q(0), Q(1)), Q(0)))
    for pair, axis, normal, offset in parallel:
        tangent = (-normal[1], normal[0])
        centres: list[Any] = [(Q(0), Q(0))] * 17
        centres[pair[1] - 1] = (
            normal[0] + offset * tangent[0],
            normal[1] + offset * tangent[1],
        )
        rows = _pair_rows(pair, axis, {axis: normal}, tuple(centres), half)
        if len(rows) != 2:
            raise ValueError("parallel control produced the wrong row count")
        for index, (first, second) in enumerate(VELOCITY_CASES):
            velocity = _velocity(pair, (first, second))
            displacement = (
                _Jet(centres[pair[1] - 1][0], second[0] - first[0]),
                _Jet(centres[pair[1] - 1][1], second[1] - first[1]),
            )
            owner_i = _owner_gap(normal, first[2], displacement, (normal, tangent), second[2])
            owner_j = _owner_gap(normal, second[2], displacement, (normal, tangent), first[2])
            exact = _jet_max(owner_i, owner_j)
            reduced = min(_row_value(row, velocity) for row in rows)
            results[f"parallel.{pair}.tau={offset}.case{index}"] = (
                exact.value == 0 and exact.slope == reduced
            )
    smooth = (
        ((3, 9), (Q(0), Q(1)), {"ey": (Q(0), Q(1)), "u": unit[::-1], "v": (Q(-3, 5), Q(4, 5))}),
        (
            (4, 10),
            (Q(3, 5), Q(-4, 5)),
            {"w": (Q(3, 5), Q(-4, 5)), "ex": (Q(1), Q(0)), "ey": (Q(0), Q(1))},
        ),
    )
    for pair, normal, aux in smooth:
        axis = next(axis for left, right, axis, _ in CONTACTS if (left, right) == pair)
        centres = [(Q(0), Q(0))] * 17
        centres[pair[1] - 1] = (Q(1, 5), Q(2)) if pair == (3, 9) else (Q(1), Q(-1, 3))
        rows = _pair_rows(pair, axis, aux, tuple(centres), half)
        owner = next(
            row["owner"]
            for row in option_manifest()
            if (row["left"], row["right"]) == pair and row["kind"] == "identity"
        )
        other = pair[1] if owner == pair[0] else pair[0]
        other_axes = tuple(aux[name] for name in AXES[square_class(other)])
        for index, (first, second) in enumerate(VELOCITY_CASES):
            velocity = _velocity(pair, (first, second))
            omegas = {pair[0]: first[2], pair[1]: second[2]}
            displacement = (
                _Jet(centres[pair[1] - 1][0], second[0] - first[0]),
                _Jet(centres[pair[1] - 1][1], second[1] - first[1]),
            )
            exact = _owner_gap(
                normal,
                omegas[owner],
                displacement,
                (other_axes[0], other_axes[1]),
                omegas[other],
            )
            results[f"smooth.{pair}.owner{owner}.case{index}"] = exact.slope == _row_value(
                rows[0], velocity
            )
    return {"checks": len(results), "passed": all(results.values()), "results": results}


def _closing_functions(aux: dict[str, Any], side: Any, half: Any) -> dict[str, Any]:
    """H254 closing functions with the side as an independent argument."""
    c, s, d, e = (aux[name] for name in ("c", "s", "d", "e"))
    alpha, gamma = c * d - s * e, c * e + s * d
    x = half + (2 + c * s + 3 * s - s * side) / c
    y = 3 * half + (2 + 3 * c - c * side) / s
    aa = d * (x + half) - e * (side - 1) + half
    bb = (d + e) * (side - 1) - half
    f1 = c * (side - 3) + s * (side - 2) - 3
    f2 = d * (side - x - 3 * half) - e * (y - side + 3 * half) - 1
    f3 = alpha * (aa - half) + gamma * (bb - half) - (c + 2 * s + 2)
    return {"X": x, "Y": y, "A": aa, "B": bb, "F1": f1, "F2": f2, "G3": f3 + alpha * f2}


def _load_derivative_controls() -> dict[str, Any]:
    """Partial angle derivatives at fixed S, and refusal after substituting S(t)."""
    field = ExactField()
    half = field.constant(Q(1, 2))
    t, b, independent = field.generator("t"), field.generator("b"), field.generator("S")
    side, aux, _ = _layout(t, b, half)
    bound = _closing_functions(aux, side, half)
    binding = {name: _vanishes(bound[name] - aux[name]) for name in ("X", "Y", "A", "B")}
    binding["F1_vanishes_on_S(t)"] = _vanishes(bound["F1"])
    binding["F2_matches_layout"] = _vanishes(bound["F2"] - _closing_f2(side, aux))
    free = _closing_functions(aux, independent, half)
    scales = load_scales(independent, aux)
    theta, beta = (1 + t * t) / 2, (1 + b * b) / 2
    derivatives = {
        "F1_theta": theta * free["F1"].derivative("t"),
        "F2_theta": theta * free["F2"].derivative("t"),
        "F2_beta": beta * free["F2"].derivative("b"),
        "G3_theta": theta * free["G3"].derivative("t"),
        "G3_beta": beta * free["G3"].derivative("b"),
    }
    partials = {name: _vanishes(value - scales[name]) for name, value in derivatives.items()}
    substituted = load_scales(side, aux)
    after = {
        "F1_theta": theta * bound["F1"].derivative("t"),
        "F2_theta": theta * bound["F2"].derivative("t"),
    }
    refused = {name: not _vanishes(value - substituted[name]) for name, value in after.items()}
    return {
        "binding": binding,
        "fixed_side_partials": partials,
        "differentiate_after_substitution_refused": refused,
        "passed": all(binding.values()) and all(partials.values()) and all(refused.values()),
    }


def _mutation_controls() -> dict[str, Any]:
    """Each frozen adversarial mutation must break the exact formal identity."""
    field = ExactField()
    side, aux, centres, rows = _formal_model(field)
    half = field.constant(Q(1, 2))
    loads = _formal_loads(field)
    weights, scales, _, _ = deterministic_weights(
        rows, side, aux, centres, half, formal=loads, normalize=False
    )
    twelve, sixteen = _formal_expectations(loads, side, aux, scales)
    side_coefficient = scales["K"]
    baseline = identity_failures(rows, weights, side_coefficient, twelve, sixteen)
    if baseline:
        raise ValueError(f"unmutated formal identity failed in columns {baseline}")
    rho = loads[2]

    def swapped(pair: tuple[int, int]) -> dict[tuple[Any, ...], Any]:
        altered = dict(weights)
        minus, plus = ("pair", *pair, 0), ("pair", *pair, 1)
        altered[minus], altered[plus] = weights[plus], weights[minus]
        return altered

    def replaced(key: tuple[Any, ...], value: Any) -> dict[tuple[Any, ...], Any]:
        altered = dict(weights)
        altered[key] = value
        return altered

    flipped = {
        key: [-value if column == OMEGA_16 else value for column, value in enumerate(row)]
        for key, row in rows.items()
    }
    dropped = {key: row for key, row in rows.items() if key != ("wall", 8, "top", 1)}
    gamma, d, e = aux["gamma"], aux["d"], aux["e"]
    cases: dict[str, list[int]] = {
        "tree_edge_moment_sign_12_14": identity_failures(
            rows, swapped((12, 14)), side_coefficient, twelve, sixteen
        ),
        "interchange_face_rows_1_3": identity_failures(
            rows, swapped((1, 3)), side_coefficient, twelve, sixteen
        ),
        "square16_physical_angle_sign": identity_failures(
            flipped, weights, side_coefficient, twelve, sixteen
        ),
        "omit_exceptional_omega12": identity_failures(
            rows, weights, side_coefficient, 0, sixteen
        ),
        "exceptional_residual_sign": identity_failures(
            rows, weights, side_coefficient, -twelve, -sixteen
        ),
        "force_15_16": identity_failures(
            rows,
            replaced(("pair", 15, 16, 0), weights["pair", 15, 16, 0] + rho),
            side_coefficient,
            twelve,
            sixteen,
        ),
        "normalization_drops_8_wall_term": identity_failures(
            rows, weights, side_coefficient - gamma * rho * (d + e), twelve, sixteen
        ),
        "row_dropped_8_top_plus": identity_failures(
            dropped, weights, side_coefficient, twelve, sixteen
        ),
        "zero_weight_9_11": identity_failures(
            rows, replaced(("pair", 9, 11, 0), rho), side_coefficient, twelve, sixteen
        ),
    }
    return {
        "baseline_failures": len(baseline),
        "mutations": {
            name: {"refused": bool(columns), "failing_columns": columns}
            for name, columns in cases.items()
        },
        "passed": all(cases.values()),
    }


def _interval_controls() -> dict[str, Any]:
    """Outward 2^-256 containment, including negatives, division and refusal."""
    checks: dict[str, bool] = {}
    third = Dyadic.point(Q(1, 3))
    checks["inexact_point_strictly_outward"] = third.lo < Q(1, 3) < third.hi
    checks["dyadic_point_exact"] = Dyadic.point(Q(-3, 8)) == Dyadic(Q(-3, 8), Q(-3, 8))
    left = Dyadic.enclose(Q(-2, 3), Q(5, 7))
    right = Dyadic.enclose(Q(3, 11), Q(9, 13))
    samples = [(Q(-2, 3), Q(3, 11)), (Q(1, 9), Q(9, 13)), (Q(5, 7), Q(1, 2)), (Q(0), Q(2, 5))]
    for name, operation in (
        ("add", lambda x, y: x + y),
        ("sub", lambda x, y: x - y),
        ("mul", lambda x, y: x * y),
        ("div", lambda x, y: x / y),
    ):
        bound = operation(left, right)
        checks[f"{name}.on_grid"] = (
            (bound.lo * GRID).denominator == 1 == (bound.hi * GRID).denominator
        )
        checks[f"{name}.contains"] = all(
            bound.lo <= operation(x, y) <= bound.hi for x, y in samples
        )
    negative = -Dyadic.enclose(Q(1, 3), Q(2, 3))
    checks["negation"] = negative.lo <= Q(-2, 3) and Q(-1, 3) <= negative.hi
    try:
        _ = left / Dyadic.enclose(Q(-1, 5), Q(1, 5))
        checks["zero_straddling_division_refused"] = False
    except ValueError:
        checks["zero_straddling_division_refused"] = True
    try:
        _ = Dyadic(Q(1, 3), Q(1, 2))
        checks["off_grid_endpoint_refused"] = False
    except ValueError:
        checks["off_grid_endpoint_refused"] = True
    return {"checks": len(checks), "passed": all(checks.values()), "results": checks}


def _disposition_controls() -> dict[str, Any]:
    positive = Dyadic.enclose(Q(1, 10), Q(1, 5))
    straddle = Dyadic.enclose(Q(-1, 10), Q(1, 5))
    negative = Dyadic.enclose(Q(-1, 5), Q(-1, 10))
    expected = {
        "confirmed_fixed_stress": {"a": positive, "b": Dyadic.point(0)},
        "unresolved_interval_sign": {"a": positive, "b": straddle},
        "rejected_fixed_candidate": {"a": straddle, "b": negative},
    }
    results = {name: classify_signs(bounds)[0] == name for name, bounds in expected.items()}
    return {"checks": len(results), "passed": all(results.values()), "results": results}


def synthetic_controls() -> dict[str, Any]:
    """Target-free controls; any control that misbehaves refuses the instrument."""
    started = time.monotonic()
    sections: dict[str, Any] = {}
    for name, control in (
        ("interval_arithmetic", _interval_controls),
        ("sign_disposition", _disposition_controls),
        ("row_derivatives", _row_derivative_controls),
        ("load_derivatives", _load_derivative_controls),
        ("mutations", _mutation_controls),
    ):
        mark = time.monotonic()
        sections[name] = control()
        sections[name]["seconds"] = time.monotonic() - mark
    failed = [name for name, section in sections.items() if section["passed"] is not True]
    if failed:
        raise ValueError(f"synthetic controls failed: {failed}")
    return {"sections": sections, "passed": True, "seconds": time.monotonic() - started}


def _require_prerequisites(
    root: dict[str, Any], endpoint: dict[str, Any], feature: dict[str, Any], source: bytes
) -> dict[str, Any]:
    """Replay the complete prerequisite semantics without historical Git objects.

    The root proof alone does not prove the zero rows: symbolic_zero_proofs checks
    those identities, including the endpoint foundation, before interval rows are
    rebuilt. Outer Git references, timings and prior root-verification summaries
    are provenance only. The later stress proof reuses the foundation's cache.
    """
    verified_root = check_root(root, source)
    for document, schema in (
        (endpoint, "n17-endpoint-feasibility/v1"),
        (feature, "n17-endpoint-feature-certificate/v1"),
    ):
        if (
            type(document) is not dict
            or document.get("schema") != schema
            or document.get("criterion_passed") is not True
            or document.get("source_sha256") != hashlib.sha256(source).hexdigest()
        ):
            raise ValueError("prerequisite schema, verdict or source is not accepted")
    identities = symbolic_zero_proofs()
    if not same_content(endpoint.get("identities"), identities["foundation"]) or not (
        same_content(feature.get("identities"), identities)
    ):
        raise ValueError("prerequisite symbolic identities differ from the exact replay")
    midpoint, radii = _root_box(root)
    geometry = interval_geometry(midpoint, radii)
    inventory = interval_inventory(midpoint, radii)
    if (
        geometry["geometry_passed"] is not True
        or inventory["feature_passed"] is not True
        or not same_content(endpoint.get("geometry"), geometry)
        or not same_content(feature.get("inventory"), inventory)
    ):
        raise ValueError("prerequisite geometry or inventory differs from the exact replay")
    return verified_root


def _root_box(root: dict[str, Any]) -> tuple[tuple[Q, Q], tuple[Q, Q]]:
    midpoint = tuple(Q(value) for value in root["box"]["midpoint"])
    radii = tuple(Q(value) for value in root["inclusion_bounds"])
    if len(midpoint) != 2 or len(radii) != 2:
        raise ValueError("root box must have two dimensions")
    return (midpoint[0], midpoint[1]), (radii[0], radii[1])


REFUSALS = (
    CertificateError,
    ValueError,
    OSError,
    KeyError,
    IndexError,
    TypeError,
    ZeroDivisionError,
    RecursionError,
    subprocess.TimeoutExpired,
)


def _refuse(error: object) -> int:
    print(
        json.dumps(
            {
                "schema": "n17-core-stress-certificate/v1",
                "criterion_passed": False,
                "error": str(error),
            },
            sort_keys=True,
        )
    )
    return 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root_certificate", type=Path, nargs="?")
    parser.add_argument("endpoint_certificate", type=Path, nargs="?")
    parser.add_argument("feature_certificate", type=Path, nargs="?")
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument(
        "--controls-only",
        action="store_true",
        help="run the target-free synthetic controls and read no certificate",
    )
    args = parser.parse_args(argv)
    if not INSTRUMENT_READY:
        return _refuse("instrument_unready")
    started = time.monotonic()
    instrument = provenance(Path(__file__))
    try:
        controls = synthetic_controls()
    except REFUSALS as error:
        return _refuse(error)
    if args.controls_only:
        print(
            _encode_receipt(
                {
                    "schema": "n17-core-stress-controls/v1",
                    "instrument_provenance": instrument,
                    "controls": controls,
                    "passed": True,
                }
            )
        )
        return 0
    inputs = (args.root_certificate, args.endpoint_certificate, args.feature_certificate)
    if any(path is None for path in inputs):
        return _refuse("root, endpoint and feature certificates are all required")
    root_path, endpoint_path, feature_path = (Path(str(path)) for path in inputs)
    try:
        for path, reference in zip(
            (root_path, endpoint_path, feature_path),
            (FROZEN_ROOT_REF, FROZEN_ENDPOINT_REF, FROZEN_FEATURE_REF),
            strict=True,
        ):
            require_retained_path(path, reference)
        source = _read_limited(args.source)
        root_raw = _read_limited(root_path)
        endpoint_raw = _read_limited(endpoint_path)
        feature_raw = _read_limited(feature_path)
        root = json.loads(root_raw, object_pairs_hook=_object_unique)
        endpoint = json.loads(endpoint_raw, object_pairs_hook=_object_unique)
        feature = json.loads(feature_raw, object_pairs_hook=_object_unique)
        root_verification = _require_prerequisites(root, endpoint, feature, source)
        midpoint, radii = _root_box(root)
        symbolic_started = time.monotonic()
        identities = symbolic_residual_proofs()
        symbolic_seconds = time.monotonic() - symbolic_started
        guard_started = time.monotonic()
        denominators = denominator_guards(ring_residual_proofs().denominators, midpoint, radii)
        guard_seconds = time.monotonic() - guard_started
        interval_started = time.monotonic()
        interval = interval_sign_audit(midpoint, radii)
        interval_seconds = time.monotonic() - interval_started
        result = {
            "schema": "n17-core-stress-certificate/v1",
            "instrument_provenance": instrument,
            "root_git_ref": FROZEN_ROOT_REF,
            "endpoint_git_ref": FROZEN_ENDPOINT_REF,
            "feature_git_ref": FROZEN_FEATURE_REF,
            "source_sha256": hashlib.sha256(source).hexdigest(),
            "root_verification": root_verification,
            "box": {
                "midpoint": [_fraction_string(value) for value in midpoint],
                "inclusion_bounds": [_fraction_string(value) for value in radii],
            },
            "controls": controls,
            "identities": identities,
            "denominator_guards": denominators,
            "interval": interval,
            "criterion_passed": interval["passed"],
            "timing_seconds": {
                "total": time.monotonic() - started,
                "controls": controls["seconds"],
                "symbolic": symbolic_seconds,
                "symbolic_foundation": identities["foundation_seconds"],
                "ring_proof": identities["ring"]["seconds"],
                "denominator_guards": guard_seconds,
                "interval": interval_seconds,
            },
        }
        print(_encode_receipt(result))
        return 0 if result["criterion_passed"] else 1
    except REFUSALS as error:
        return _refuse(error)


if __name__ == "__main__":
    raise SystemExit(main())
