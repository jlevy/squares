"""One finite LP outer relaxation; only exact rational objective evidence is emitted.

The scientific factory is lazy. This module never claims a continuum kernel or a
packing bound. A separately declared supervisor must cap the WHOLE child at 60s;
the 30s HiGHS limit covers the solver only, not construction or rational checking.
Stdout is a live certificate stream, not a file-publication API.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections.abc import Iterable, Sequence, Sized
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
from numbers import Real
from typing import Any, TypedDict

from scipy.optimize import linprog

FORMAT = "bc264-axis-objective/v1"
SCIENTIFIC_SOURCE = "five-tight-axis-grids-v1"
SYNTHETIC_SOURCE = "synthetic-axis-poses-v1"
MAX_POSES = 45
MAX_PAIRS = 990
MAX_ROWS = MAX_POSES + MAX_PAIRS + 23
MAX_INPUT_BITS = 128
MAX_EXACT_BITS = 4096
MAX_PACKET_BYTES = 2 * 1024 * 1024
MAX_SOLVER_SECONDS = 30.0
MAX_SOLVER_ITERATIONS = 10_000
MAX_DENOMINATOR = 1_000_000
MAX_DUAL_MAGNITUDE = 2**32
PARAMETERS = 16

type Pose = tuple[Fraction, Fraction]
type Vector = tuple[Fraction, ...]
type Matrix = list[list[Fraction]]
type PairWeight = tuple[int, int, Fraction]


class GuardError(ValueError):
    """A malformed or resource-exceeding input cannot enter the finite problem."""


class BetaEntry(TypedDict):
    i: int
    j: int
    weight: str


class Certificate(TypedDict):
    format: str
    source: str
    side: str
    poses: list[list[str]]
    alpha: list[str]
    beta: list[BetaEntry]
    bound: str


@dataclass(frozen=True)
class Problem:
    side: Fraction
    poses: tuple[Pose, ...]
    source: str
    pairs: tuple[tuple[int, int], ...]
    rows: tuple[Vector, ...]
    rhs: Vector


@dataclass(frozen=True)
class Outcome:
    packet: Certificate | None
    reason: str
    solver_status: int | None


def bounded(value: object, bits: int = MAX_EXACT_BITS) -> Fraction:
    if not isinstance(value, Fraction):
        raise GuardError("exact Fraction input required; floats and strings are refused")
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > bits:
        raise GuardError("rational exceeds the declared bit limit")
    return value


def bounded_sum(values: Iterable[Fraction]) -> Fraction:
    """Refuse denominator growth during accumulation, not only after the final sum."""
    total = Fraction(0)
    for value in values:
        total = bounded(total + bounded(value))
    return total


def validate_poses(side: Fraction, poses: tuple[Pose, ...], source: str) -> None:
    bounded(side, MAX_INPUT_BITS)
    if not 1 <= side <= 16:
        raise GuardError("side must lie in [1,16]")
    if not isinstance(poses, tuple) or not 1 <= len(poses) <= MAX_POSES:
        raise GuardError("one to forty-five poses are required")
    for pose in poses:
        if not isinstance(pose, tuple) or len(pose) != 2:
            raise GuardError("each pose is an exact coordinate pair")
        for coordinate in pose:
            bounded(coordinate, MAX_INPUT_BITS)
            if not Fraction(1, 2) <= coordinate <= side - Fraction(1, 2):
                raise GuardError("axis-aligned square is not contained")
    if poses != tuple(sorted(set(poses))):
        raise GuardError("poses must be sorted and distinct")
    if source == SCIENTIFIC_SOURCE:
        # Screen the side first so a foreign one never reaches the factory, then admit
        # the roster only through it. A control that forbids the factory then refuses
        # every scientific construction structurally, not by its choice of test data.
        if side != Fraction(96, 25) or poses != scientific_source()[1]:
            raise GuardError("scientific source must be the full fixed five-grid roster")
    elif source != SYNTHETIC_SOURCE:
        raise GuardError("unknown source identity")


def five_grid_poses(side: Fraction) -> tuple[Pose, ...]:
    """Construct the declared grid rule at a caller-supplied exact side, lazily."""
    bounded(side, MAX_INPUT_BITS)
    if not 3 <= side <= 16:
        raise GuardError("five tight grids require side in [3,16]")
    offsets = (Fraction(1, 2), side - Fraction(5, 2))
    poses = {
        (a + i, b + j)
        for a, b in product(offsets, repeat=2)
        for i, j in product(range(3), repeat=2)
    }
    poses.update((side / 2 + i, side / 2 + j) for i, j in product((-1, 0, 1), repeat=2))
    return tuple(sorted(poses))


def scientific_source() -> tuple[Fraction, tuple[Pose, ...]]:
    """The sole scientific factory; never called by source-free controls."""
    side = Fraction(96, 25)
    return side, five_grid_poses(side)


def axis_features(side: Fraction, pose: Pose) -> Vector:
    """Restrict (z4,s,d,w,V0,V1) to angle zero: cos(4theta)=1, sin=0."""
    bounded(side, MAX_INPUT_BITS)
    for coordinate in pose:
        bounded(coordinate, MAX_INPUT_BITS)
    u, v = pose[0] - side / 2, pose[1] - side / 2
    return tuple(
        bounded(value)
        for value in (
            Fraction(1),
            u * u + v * v,
            u * u * v * v,
            Fraction(1),
            Fraction(0),
            u * u - v * v,
            u * v,
            u,
            v,
            u * v * v,
            u * u * v,
        )
    )


def pair_coefficients(left: Vector, right: Vector) -> Vector:
    """Coefficients of A-upper10, B-upper3, a_s/a_d/a_w in K-1."""
    if len(left) != 11 or len(right) != 11:
        raise GuardError("eleven features are required")
    for value in (*left, *right):
        bounded(value)
    coefficients = [
        left[i] * right[j] + (left[j] * right[i] if i != j else 0)
        for i in range(4)
        for j in range(i, 4)
    ]
    coefficients.extend(
        (
            left[7] * right[7] + left[8] * right[8],
            left[7] * right[9] + left[8] * right[10] + left[9] * right[7] + left[10] * right[8],
            left[9] * right[9] + left[10] * right[10],
            left[4] * right[4],
            left[5] * right[5],
            left[6] * right[6],
        )
    )
    return tuple(bounded(value) for value in coefficients)


def psd_directions() -> tuple[Vector, ...]:
    """The fixed 23 linear PSD necessities, with no adaptive cuts."""
    rows: list[Vector] = []
    for size, offset in ((4, 0), (2, 10)):
        vectors = [tuple(Fraction(i == j) for i in range(size)) for j in range(size)]
        for i, j in combinations(range(size), 2):
            vectors.extend(
                tuple(Fraction((k == i) + sign * (k == j)) for k in range(size))
                for sign in (-1, 1)
            )
        for vector in vectors:
            row = [Fraction(0)] * PARAMETERS
            packed = [
                vector[i] * vector[j] * (1 if i == j else 2)
                for i in range(size)
                for j in range(i, size)
            ]
            row[offset : offset + len(packed)] = packed
            rows.append(tuple(row))
    rows.extend(
        tuple(Fraction(i == index) for i in range(PARAMETERS)) for index in (13, 14, 15)
    )
    return tuple(rows)


def compatible(left: Pose, right: Pose) -> bool:
    """Interior-disjoint axis squares include exact edge and corner contacts."""
    return abs(left[0] - right[0]) >= 1 or abs(left[1] - right[1]) >= 1


def build_problem(
    side: Fraction, poses: tuple[Pose, ...], *, source: str = SYNTHETIC_SOURCE
) -> Problem:
    validate_poses(side, poses, source)
    features = tuple(axis_features(side, pose) for pose in poses)
    pairs = tuple(
        (i, j) for i, j in combinations(range(len(poses)), 2) if compatible(poses[i], poses[j])
    )
    rows = [(-Fraction(1), *pair_coefficients(feature, feature)) for feature in features]
    rows.extend((Fraction(0), *pair_coefficients(features[i], features[j])) for i, j in pairs)
    rhs = [-Fraction(1)] * len(rows)
    directions = psd_directions()
    rows.extend((Fraction(0), *(-value for value in direction)) for direction in directions)
    rhs.extend([Fraction(0)] * len(directions))
    return Problem(side, poses, source, pairs, tuple(rows), tuple(rhs))


def projected_blocks(coefficients: Vector) -> tuple[Matrix, Matrix, Vector]:
    """Convert parameter coefficients to the exact trace-dual matrices."""
    if len(coefficients) != PARAMETERS:
        raise GuardError("sixteen parameter coefficients are required")
    for value in coefficients:
        bounded(value)
    matrices: list[Matrix] = []
    for size, offset in ((4, 0), (2, 10)):
        matrix = [[Fraction(0)] * size for _ in range(size)]
        entries = [(i, j) for i in range(size) for j in range(i, size)]
        for index, (i, j) in enumerate(entries):
            value = coefficients[offset + index] / (1 if i == j else 2)
            matrix[i][j] = matrix[j][i] = bounded(value)
        matrices.append(matrix)
    return matrices[0], matrices[1], coefficients[13:]


def is_psd(matrix: Matrix) -> bool:
    """Exact Schur complements; a zero pivot must have a zero residual row."""
    size = len(matrix)
    if size not in (2, 4) or any(len(row) != size for row in matrix):
        raise GuardError("only the fixed 4x4 and 2x2 blocks are admitted")
    work = [[bounded(value) for value in row] for row in matrix]
    if any(work[i][j] != work[j][i] for i in range(size) for j in range(size)):
        raise GuardError("PSD matrix is not symmetric")
    for pivot in range(size):
        diagonal = work[pivot][pivot]
        if diagonal < 0:
            return False
        if diagonal == 0:
            if any(work[pivot][j] != 0 for j in range(pivot + 1, size)):
                return False
            continue
        for i in range(pivot + 1, size):
            for j in range(i, size):
                value = bounded(work[i][j] - work[i][pivot] * work[pivot][j] / diagonal)
                work[i][j] = work[j][i] = value
    return True


def make_certificate(
    side: Fraction,
    poses: tuple[Pose, ...],
    alpha: Sequence[Fraction],
    beta: Sequence[PairWeight],
    *,
    source: str = SYNTHETIC_SOURCE,
) -> Certificate:
    """Emit only a normalized, exact projected-PSD objective certificate."""
    validate_poses(side, poses, source)
    if len(alpha) != len(poses) or len(beta) > MAX_PAIRS:
        raise GuardError("objective weight inventory exceeds its fixed bounds")
    if any(bounded(weight) < 0 for weight in alpha) or bounded_sum(alpha) != 1:
        raise GuardError("alpha must be nonnegative and sum exactly to one")
    keys: list[tuple[int, int]] = []
    for i, j, weight in beta:
        if type(i) is not int or type(j) is not int or not 0 <= i < j < len(poses):
            raise GuardError("beta indices must be distinct ordered pose indices")
        if bounded(weight) <= 0 or not compatible(poses[i], poses[j]):
            raise GuardError("beta must positively weight a compatible pair")
        keys.append((i, j))
    if keys != sorted(set(keys)):
        raise GuardError("beta must be sorted without duplicate pairs")
    features = [axis_features(side, pose) for pose in poses]
    terms = [
        (weight, pair_coefficients(feature, feature))
        for weight, feature in zip(alpha, features, strict=True)
    ]
    terms.extend((weight, pair_coefficients(features[i], features[j])) for i, j, weight in beta)
    total = tuple(
        bounded_sum(weight * row[k] for weight, row in terms) for k in range(PARAMETERS)
    )
    matrix_a, matrix_b, scalars = projected_blocks(total)
    if not is_psd(matrix_a) or not is_psd(matrix_b) or any(value < 0 for value in scalars):
        raise GuardError("objective combination is not exactly projected PSD")
    bound = bounded(1 + bounded_sum(weight for _, _, weight in beta))
    packet: Certificate = {
        "format": FORMAT,
        "source": source,
        "side": str(side),
        "poses": [[str(x), str(y)] for x, y in poses],
        "alpha": [str(weight) for weight in alpha],
        "beta": [{"i": i, "j": j, "weight": str(weight)} for i, j, weight in beta],
        "bound": str(bound),
    }
    if len(json.dumps(packet).encode("ascii")) > MAX_PACKET_BYTES:
        raise GuardError("certificate exceeds the 2 MiB output cap")
    return packet


def reconstruct(problem: Problem, raw_marginals: object) -> Certificate:
    """One bounded rationalization and normalization; no residual tolerance."""
    if (
        not 1 <= len(problem.rows) <= MAX_ROWS
        or not isinstance(raw_marginals, Iterable)
        or not isinstance(raw_marginals, Sized)
        or len(raw_marginals) != len(problem.rows)
    ):
        raise GuardError("solver dual inventory is incomplete")
    values: list[Fraction] = []
    for index, raw in enumerate(raw_marginals):
        if index >= len(problem.rows):
            raise GuardError("solver dual yielded more values than its declared inventory")
        if not isinstance(raw, Real) or isinstance(raw, bool):
            raise GuardError("solver dual must contain real numeric values")
        value = -float(raw)
        if not math.isfinite(value) or abs(value) > MAX_DUAL_MAGNITUDE:
            raise GuardError("solver dual is not a bounded finite number")
        rational = Fraction(value).limit_denominator(MAX_DENOMINATOR)
        if rational < 0:
            raise GuardError("solver dual has a negative rationalized weight")
        values.append(rational)
    if len(values) != len(problem.rows):
        raise GuardError("solver dual yielded fewer values than its declared inventory")
    count = len(problem.poses)
    normalization = bounded_sum(values[:count])
    if normalization <= 0:
        raise GuardError("solver dual has no positive diagonal normalization")
    alpha = [bounded(value / normalization) for value in values[:count]]
    beta = [
        (i, j, bounded(values[count + index] / normalization))
        for index, (i, j) in enumerate(problem.pairs)
        if values[count + index] != 0
    ]
    return make_certificate(problem.side, problem.poses, alpha, beta, source=problem.source)


def propose(
    side: Fraction, poses: tuple[Pose, ...], *, source: str = SYNTHETIC_SOURCE
) -> Outcome:
    """Exactly one HiGHS invocation; every numerical/reconstruction failure is inconclusive."""
    problem = build_problem(side, poses, source=source)
    try:
        result: Any = linprog(
            c=[1.0] + [0.0] * PARAMETERS,
            A_ub=[[float(value) for value in row] for row in problem.rows],
            b_ub=[float(value) for value in problem.rhs],
            bounds=[(None, None)] * (PARAMETERS + 1),
            method="highs",
            options={"time_limit": MAX_SOLVER_SECONDS, "maxiter": MAX_SOLVER_ITERATIONS},
        )
    except (ValueError, ArithmeticError, RuntimeError) as error:
        return Outcome(None, f"solver error: {error}", None)
    try:
        status = int(result.status)
        success = result.success
    except (ValueError, TypeError, AttributeError) as error:
        return Outcome(None, f"solver receipt inconclusive: {error}", None)
    if not success or status != 0:
        return Outcome(None, f"solver inconclusive: status {status}", status)
    try:
        packet = reconstruct(problem, result.ineqlin.marginals)
    except (ValueError, ArithmeticError, TypeError, AttributeError) as error:
        return Outcome(None, f"exact reconstruction inconclusive: {error}", status)
    return Outcome(packet, "exact objective certificate", status)


def propose_scientific() -> Outcome:
    side, poses = scientific_source()
    return propose(side, poses, source=SCIENTIFIC_SOURCE)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target-five-grids", action="store_true", required=True)
    parser.parse_args(argv)
    try:
        outcome = propose_scientific()
    except (GuardError, ArithmeticError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    if outcome.packet is None:
        print(f"inconclusive: {outcome.reason}", file=sys.stderr)
        return 1
    print(json.dumps(outcome.packet, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
