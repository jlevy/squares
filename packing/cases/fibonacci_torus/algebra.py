"""
Replay the algebra behind the supplied Fibonacci-torus abstract.

The finite models below are reconstructed from the abstract, not extracted from
an available manuscript. In particular, their agreement does not verify that
the pictured packing has the asserted torus representation.

Run from ``packing/`` with ``python -m cases.fibonacci_torus.algebra``.
All decisions use integers or exact finite-field polynomial arithmetic.
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
from math import gcd
from typing import Any

import sympy as sp

type Matrix = tuple[tuple[int, int], tuple[int, int]]
type Pair = tuple[int, int]

Q: Matrix = ((0, 1), (1, 1))
IDENTITY: Matrix = ((1, 0), (0, 1))
SIDE_COEFFICIENTS = (1, -20, 178, -842, 1923, -496, -6754, 12420, -6865)
FACTOR_CERTIFICATES = {
    7: ((1, -1), (1, 2, -2, 3, 1, 2, 3, -2)),
    29: ((1, 9, 4, -1, 9, -3, 3, 8, 8),),
    73: ((1, 32), (1, -2, -32), (1, 23, 22, -22, -4, -35)),
}


def _require(condition: bool, message: str) -> None:  # noqa: FBT001 -- proposition, not an option
    if not condition:
        raise ValueError(message)


def _multiply(left: Matrix, right: Matrix) -> Matrix:
    a, b = left[0]
    c, d = left[1]
    e, f = right[0]
    g, h = right[1]
    return ((a * e + b * g, a * f + b * h), (c * e + d * g, c * f + d * h))


def _power(matrix: Matrix, exponent: int) -> Matrix:
    result = IDENTITY
    for _ in range(exponent):
        result = _multiply(result, matrix)
    return result


def _minus_identity(matrix: Matrix) -> Matrix:
    return ((matrix[0][0] - 1, matrix[0][1]), (matrix[1][0], matrix[1][1] - 1))


def _determinant(matrix: Matrix) -> int:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def _smith(matrix: Matrix) -> Pair:
    size = abs(_determinant(matrix))
    first = gcd(*matrix[0], *matrix[1])
    _require(size > 0, "Smith factors here require a finite quotient")
    return first, size // first


def _contains(matrix: Matrix, vector: Pair) -> bool:
    determinant = _determinant(matrix)
    a, b = matrix[0]
    c, d = matrix[1]
    x, y = vector
    return (d * x - b * y) % determinant == (-c * x + a * y) % determinant == 0


def _quotients() -> list[dict[str, Any]]:
    rows = []
    for index in range(3, 17):
        power = _power(Q, index)
        lattice = _minus_identity(power)
        size = abs(_determinant(lattice))
        lucas = power[0][0] + power[1][1]
        order = next(
            exponent
            for exponent in range(1, index + 1)
            if _contains(
                lattice,
                (_power(Q, exponent)[0][0] - 1, _power(Q, exponent)[1][0]),
            )
        )
        _require(size == lucas - 1 - (-1) ** index, "Lucas quotient-order identity")
        _require(order == index, "Multiplication by phi must have order m")
        rows.append(
            {
                "m": index,
                "size": size,
                "smith_factors": _smith(lattice),
                "phi_order": order,
                "affine_group_order": size * order,
                "pair_count": size * (size - 1) // 2,
                "cardinality_allows_regular_pair_action": size == 2 * index + 1,
            }
        )
    _require(
        [row["m"] for row in rows if row["cardinality_allows_regular_pair_action"]] == [5],
        "Finite sweep's necessary cardinality test",
    )
    return rows


def _pair(x: int, y: int, prime: int) -> Pair:
    return min(x % prime, y % prime), max(x % prime, y % prime)


def _return_orbit(alpha: int, beta: int, prime: int) -> Pair:
    return alpha % prime, min(beta % prime, -beta % prime)


def _affine_statistics(prime: int, slopes: set[int]) -> dict[str, Any]:
    pairs = set(combinations(range(prime), 2))
    transformations = [(slope, shift) for slope in sorted(slopes) for shift in range(prime)]
    remaining = pairs.copy()
    orbit_sizes = []
    while remaining:
        x, y = min(remaining)
        orbit = {
            _pair(slope * x + shift, slope * y + shift, prime)
            for slope, shift in transformations
        }
        remaining.difference_update(orbit)
        orbit_sizes.append(len(orbit))
    stabilizers = Counter(
        sum(
            _pair(slope * x + shift, slope * y + shift, prime) == (x, y)
            for slope, shift in transformations
        )
        for x, y in pairs
    )
    return {
        "prime": prime,
        "slopes": sorted(slopes),
        "group_order": len(transformations),
        "pair_count": len(pairs),
        "pair_orbit_sizes": sorted(orbit_sizes),
        "stabilizer_order_histogram": dict(sorted(stabilizers.items())),
        "regular": len(orbit_sizes) == 1 and set(stabilizers) == {1},
    }


def _reciprocal_pair(alpha: int, beta: int, prime: int) -> Pair:
    if beta % prime == 0:
        raise ValueError("The reciprocal pair is undefined at beta=0")
    inverse = pow(beta, -1, prime)
    return _pair(alpha + inverse, alpha - inverse, prime)


def _return_model() -> dict[str, Any]:
    prime = 11
    phi5 = _power(Q, 5)
    phi10 = _power(Q, 10)
    _require(
        _minus_identity(phi10)
        == ((11 * phi5[0][0], 11 * phi5[0][1]), (11 * phi5[1][0], 11 * phi5[1][1])),
        "phi^10 - 1 = 11 phi^5",
    )
    crt = {
        ((a + 4 * b) % prime, (a + 8 * b) % prime) for a in range(prime) for b in range(prime)
    }
    _require(len(crt) == 121, "CRT evaluation at 4 and 8 must be bijective")
    fixed = sum((alpha, beta) == (alpha, -beta % prime) for alpha, beta in crt)
    orbits = {_return_orbit(alpha, beta, prime) for alpha, beta in crt if beta}
    images = {_reciprocal_pair(alpha, beta, prime) for alpha, beta in orbits}
    _require(fixed == 11 and len(orbits) == 55, "The return involution's orbit census")
    _require(images == set(combinations(range(prime), 2)), "Reciprocity must give all pairs")
    _require(pow(4, 5, prime) == 1 and pow(8, 5, prime) == prime - 1, "CRT return multipliers")
    direct_beta_failures = 0
    for alpha, beta in orbits:
        x, y = _reciprocal_pair(alpha, beta, prime)
        _require(
            _reciprocal_pair(4 * alpha, 8 * beta, prime) == _pair(4 * x, 4 * y, prime),
            "Reciprocity must intertwine phi with the base slope 4",
        )
        _require(
            _reciprocal_pair(alpha + 1, beta, prime) == _pair(x + 1, y + 1, prime),
            "Reciprocity must intertwine the fixed-eigenspace translation",
        )
        direct_beta_failures += _pair(
            4 * alpha + 8 * beta, 4 * alpha - 8 * beta, prime
        ) != _pair(4 * (alpha + beta), 4 * (alpha - beta), prime)
    _require((2 + 8 * 4) % prime == 1 and (2 + 8 * 8) % prime == 0, "Translation idempotent")
    _require(direct_beta_failures == 55, "Omitting reciprocity must break slope equivariance")
    translation_failures = sum(
        _return_orbit(alpha + 1, beta + 1, prime) != _return_orbit(alpha + 1, -beta + 1, prime)
        for alpha, beta in crt
    )
    _require(
        translation_failures == 110, "Unit ring translation must fail to preserve return orbits"
    )
    try:
        _reciprocal_pair(0, 0, prime)
    except ValueError:
        zero_rejected = True
    else:
        zero_rejected = False
    _require(zero_rejected, "The fixed cells cannot enter the reciprocal map")
    return {
        "ring": "R_10 = Z[phi]/(11) = F_11 x F_11; not F_121",
        "crt_roots": [4, 8],
        "return": "phi^5: (alpha,beta) -> (alpha,-beta)",
        "fixed_cells": fixed,
        "two_cell_orbits": len(orbits),
        "distinct_reciprocal_pairs": len(images),
        "translation_lift_coefficients_1_phi": [2, 8],
        "controls": {
            "beta_zero_rejected": zero_rejected,
            "without_reciprocal_equivariance_failures": direct_beta_failures,
            "unit_ring_translation_orbit_preservation_failures": translation_failures,
        },
        "geometric_cover_identified": False,
    }


def _f17_obstructions() -> dict[str, Any]:
    residues = {a * a % 17 for a in range(1, 17)}
    roots = [a for a in range(17) if (a * a - a - 1) % 17 == 0]
    statistics = _affine_statistics(17, residues)
    _require(
        not roots and 5 not in residues, "The Fibonacci polynomial must be irreducible mod 17"
    )
    _require(
        statistics["pair_orbit_sizes"] == [68, 68], "The index-two affine group has two orbits"
    )
    _require(
        statistics["stabilizer_order_histogram"] == {2: 136},
        "The affine involution fixes pairs",
    )
    alternative: Matrix = ((-2, 5), (5, -13))
    _require(_determinant(alternative) == 1, "Alternative torus monodromy must be unimodular")
    _require(
        _smith(_minus_identity(alternative)) == (1, 17), "Alternative fixed-point quotient"
    )
    return {
        "fibonacci_polynomial_roots_mod_17": roots,
        "fibonacci_invariant_index_17_lattice_exists": False,
        "square_slope_affine_action": statistics,
        "regular_action_on_136_pairs_impossible": True,
        "proof": (
            "A group of order 136 has an involution; "
            "any nonidentity involution on 17 points fixes a pair."
        ),
        "alternative_monodromy": alternative,
        "alternative_determinant": 1,
        "alternative_trace": -15,
        "alternative_coker_A_minus_I": [1, 17],
        "alternative_has_packing_interpretation": False,
    }


def _bundle_and_geodesic() -> dict[str, Any]:
    q3 = _power(Q, 3)
    monodromy: Matrix = ((-q3[0][0], -q3[0][1]), (-q3[1][0], -q3[1][1]))
    conjugation: Matrix = ((1, 1), (0, -1))
    inverse_q3: Matrix = ((-q3[1][1], q3[0][1]), (q3[1][0], -q3[0][0]))
    _require(
        _multiply(_multiply(conjugation, monodromy), conjugation) == inverse_q3,
        "B conjugate to Q^-3",
    )
    covers = []
    for degree in range(1, 7):
        factors = _smith(_minus_identity(_power(monodromy, degree)))
        _require(
            factors == _smith(_minus_identity(_power(Q, 3 * degree))),
            "Cyclic-cover torsion is R_(3k)",
        )
        covers.append(
            {"cover_degree": degree, "R_index": 3 * degree, "torsion_smith_factors": factors}
        )
    _require(
        tuple((monodromy[0][i] + 8 * monodromy[1][i]) % 11 for i in range(2)) == (5, 7),
        "Fiber label a+8b must intertwine B with multiplier 5 mod 11",
    )
    _require(
        {pow(5, exponent, 11) for exponent in range(5)} == {1, 3, 4, 5, 9},
        "Bundle affine quotient",
    )
    w = sp.Symbol("w")
    numerator_x = 2 * w + w**2
    numerator_y = 1 + w - w**2
    denominator = 1 + w**2
    _require(
        sp.expand(numerator_x**2 - numerator_x * denominator + numerator_y**2 - denominator**2)
        == 0,
        "The assumed lattice I+wQ must lie on the golden geodesic",
    )
    q2 = _power(Q, 2)
    _require(
        _determinant(q2) == 1 and q2[0][0] + q2[1][1] == 3, "Smallest hyperbolic integral trace"
    )
    return {
        "monodromy": monodromy,
        "determinant": _determinant(monodromy),
        "mapping_torus_orientable": False,
        "cyclic_cover_homology": "Z direct_sum R_(3k) as abelian groups",
        "covers": covers,
        "affine_55_quotient": {"fiber_label": "a+8b mod 11", "base_multiplier": 5},
        "modular_geodesic": {
            "lattice_basis_period_matrix": q2,
            "upper_half_plane_period_matrix": ((2, 1), (1, 1)),
            "trace": 3,
            "length": "2 arccosh(3/2) = 4 log(phi)",
            "assumed_lattice_matrix": "I+wQ",
            "shape": "x=(2w+w^2)/(1+w^2), y=(1+w-w^2)/(1+w^2)",
            "axis_equation": "(x-1/2)^2+y^2=5/4",
            "manuscript_lattice_identified": False,
        },
    }


def _valid_factorization(
    coefficients: tuple[int, ...], prime: int, factors: tuple[tuple[int, ...], ...]
) -> bool:
    x = sp.Symbol("x")
    polynomial = sp.Poly.from_list(list(coefficients), x, modulus=prime)
    product = sp.Poly(1, x, modulus=prime)
    for coefficients_factor in factors:
        factor = sp.Poly.from_list(list(coefficients_factor), x, modulus=prime)
        if not factor.is_irreducible:
            return False
        product *= factor
    return product == polynomial and polynomial.gcd(polynomial.diff()).degree() == 0


def _side_field() -> dict[str, Any]:
    certificates = []
    for prime, factors in FACTOR_CERTIFICATES.items():
        _require(
            _valid_factorization(SIDE_COEFFICIENTS, prime, factors),
            f"Factor certificate mod {prime}",
        )
        certificates.append(
            {
                "prime": prime,
                "factor_degrees": [len(factor) - 1 for factor in factors],
                "factors": factors,
            }
        )
    mutant = (*SIDE_COEFFICIENTS[:-1], SIDE_COEFFICIENTS[-1] + 1)
    rejected = all(
        not _valid_factorization(mutant, prime, factors)
        for prime, factors in FACTOR_CERTIFICATES.items()
    )
    _require(rejected, "A changed side polynomial must fail the retained factor certificates")
    return {
        "coefficients_descending": SIDE_COEFFICIENTS,
        "degree": 8,
        "factor_certificates": certificates,
        "galois_group": "S_8",
        "proof": [
            "Irreducible mod 29 implies irreducible over Q and a transitive Galois action.",
            "The mod-7 cycle type (1,7) makes that transitive action 2-transitive.",
            "The fifth power of a mod-73 cycle of type (1,2,5) is a transposition.",
            "2-transitivity conjugates that transposition to every transposition, giving S_8.",
        ],
        "controls": {"constant_coefficient_mutant_rejected_at_all_three_primes": rejected},
    }


def audit() -> dict[str, Any]:
    """
    Return exact replay evidence; raise on any failed mathematical obligation.
    """
    affine = _affine_statistics(11, {pow(4, exponent, 11) for exponent in range(5)})
    _require(affine["regular"], "The order-55 affine group must be regular on pairs")
    enlarged = _affine_statistics(11, set(range(1, 11)))
    _require(
        enlarged["stabilizer_order_histogram"] == {2: 55}, "Adding slope -1 destroys freeness"
    )
    return {
        "schema_version": 1,
        "status": "verified-algebra-only",
        "quotients_m3_through_m16": _quotients(),
        "regular_affine_action_F11": affine,
        "enlarged_affine_group_control": enlarged,
        "R10_return_model": _return_model(),
        "F17_obstructions": _f17_obstructions(),
        "bundle_and_geodesic": _bundle_and_geodesic(),
        "side_field": _side_field(),
    }


def main() -> int:
    """
    Emit deterministic JSON suitable for a retained research receipt.
    """
    print(json.dumps(audit(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
