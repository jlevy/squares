"""Corroborate polynomial identities and local reductions, not graph coverage."""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import math
import signal
import sys
import time
from collections import Counter
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path

Poly = tuple[int, ...]
C: Poly = (1, 0, -1)
S: Poly = (0, 2)
D: Poly = (1, 0, 1)
U: Poly = (1, 2, -1)


def trim(p: list[int] | Poly) -> Poly:
    result = list(p)
    while result and result[-1] == 0:
        result.pop()
    return tuple(result)


def plus(*terms: Poly) -> Poly:
    result = [0] * max((len(p) for p in terms), default=0)
    for p in terms:
        for degree, coefficient in enumerate(p):
            result[degree] += coefficient
    return trim(result)


def times(*terms: Poly) -> Poly:
    result: Poly = (1,)
    for p in terms:
        if not p or not result:
            return ()
        output = [0] * (len(result) + len(p) - 1)
        for i, a in enumerate(result):
            for j, b in enumerate(p):
                output[i + j] += a * b
        result = trim(output)
    return result


def scaled(p: Poly, n: int) -> Poly:
    return trim([n * a for a in p])


def nonnegative(p: Poly, *, strict: bool = False) -> bool:
    """Bernstein basis on [0, 1/24]; strict positivity excludes only t=0."""
    if not p:
        return not strict
    degree = len(p) - 1
    coefficients = [
        sum(
            (
                Fraction(p[k] * math.comb(j, k), 24**k * math.comb(degree, k))
                for k in range(j + 1)
            ),
            Fraction(),
        )
        for j in range(degree + 1)
    ]
    return all(a >= 0 for a in coefficients) and (not strict or coefficients[-1] > 0)


def constraint(rule: list[int | str]) -> tuple[dict[int, Poly], Poly]:
    """Rebuild necessary inequalities in variables X_i = 2(1+t²)² x_i."""
    kind, cell, *arguments = rule
    assert isinstance(cell, int)
    assert 0 <= cell < 25
    assert all(isinstance(v, int) for v in arguments)
    values = [int(v) for v in arguments]
    cd2 = times(C, D, D)
    cdu = times(C, D, U)
    displacement = times(U, plus(U, scaled(D, -1)))
    if kind in {"wall", "rank"}:
        axis, sign = values[:2]
        assert axis in {0, 1}
        assert sign in {-1, 1}
        lhs = {2 * cell + axis: scaled(C, sign)}
        if kind == "wall":
            assert len(values) == 2
            return lhs, plus(scaled(cd2, 10 if sign == 1 else 0), scaled(cdu, -1))
        assert len(values) == 3
        rank = values[2]
        assert rank == divmod(cell, 5)[axis]
        offset = 4 - rank if sign == 1 else rank
        return lhs, plus(
            scaled(cd2, sign * (2 * rank + 1)), scaled(times(C, displacement), 2 * offset)
        )
    assert kind in {"same", "mixdiag", "mixedstraight"}
    assert len(values) == 3
    other, axis, sign = values
    assert 0 <= other < 25
    assert axis in {0, 1}
    a, b = divmod(cell, 5), divmod(other, 5)
    assert b[axis] - a[axis] == 1
    transverse = b[1 - axis] - a[1 - axis]
    if kind == "same":
        assert sign in {-1, 1}
        cross = scaled(S, sign * (1 if axis == 0 else -1))
        rhs = scaled(times(D, D, D), -2)
    elif kind == "mixdiag":
        assert sign == transverse
        assert abs(sign) == 1
        cross = scaled(S, sign)
        rhs = scaled(cdu, -2)
    else:
        assert sign == transverse == 0
        cross = ()
        rhs = plus(scaled(cdu, -2), scaled(times(S, displacement), 8))
    return {
        2 * cell + axis: C,
        2 * other + axis: scaled(C, -1),
        2 * cell + 1 - axis: cross,
        2 * other + 1 - axis: scaled(cross, -1),
    }, rhs


def certificate(row: dict) -> None:
    rules, weights = row["rules"], row["multipliers"]
    assert len(rules) == len(weights) > 1
    assert len({tuple(rule) for rule in rules}) == len(rules)
    total: dict[int, Poly] = {}
    rhs: Poly = ()
    for rule, values in zip(rules, weights, strict=True):
        assert values
        assert all(type(v) is int for v in values)
        weight = trim(values)
        assert nonnegative(weight)
        lhs, bound = constraint(rule)
        for coordinate, polynomial in lhs.items():
            total[coordinate] = plus(total.get(coordinate, ()), times(weight, polynomial))
        rhs = plus(rhs, times(weight, bound))
    assert not any(total.values())
    margin = scaled(rhs, -1)
    assert margin == trim(row["margin"])
    assert nonnegative(margin, strict=True)


def bridges() -> dict[int, int]:
    histogram: Counter[int] = Counter()
    for vacancy in permutations(range(5)):
        occupied = {(x, y) for x in range(5) for y in range(5) if vacancy[x] != y}
        count = 0
        for x in range(4):
            for y in range(5):
                for step in (-1, 1):
                    yy = y + step
                    if not 0 <= yy < 5:
                        continue
                    horizontal = {(k, y if k <= x else yy) for k in range(5)}
                    lo, hi = sorted(((x, y), (x + 1, yy)), key=lambda p: p[1])
                    vertical = {(lo[0] if k <= lo[1] else hi[0], k) for k in range(5)}
                    if horizontal <= occupied and vertical <= occupied:
                        count += 1
        histogram[count] += 1
    assert histogram == {4: 92, 5: 24, 6: 4}
    return dict(sorted(histogram.items()))


def one_diagonal_chains() -> int:
    count = 0
    displacement = times(U, plus(U, scaled(D, -1)))
    for position, row, step in product(range(4), range(5), (-1, 1)):
        if not 0 <= row + step < 5:
            continue
        ranks = [row] * (position + 1) + [row + step] * (4 - position)
        for signs in product((-1, 1), repeat=5):
            if all(sign == step for sign in signs):
                continue
            count += 1
            choices = []
            same = 0
            for i in range(4):
                h = ranks[i + 1] - ranks[i]
                if signs[i] == signs[i + 1]:
                    same += 1
                    choices.append((signs[i],))
                else:
                    choices.append((h,) if h else (-1, 1))
            for normals in product(*choices):
                hsum = sum(normals[i] * (ranks[i + 1] - ranks[i]) for i in range(4))
                coefficients = (
                    [-normals[0]]
                    + [normals[i - 1] - normals[i] for i in range(1, 4)]
                    + [normals[-1]]
                )
                ksum = sum(
                    w * (4 - r if w > 0 else -r)
                    for w, r in zip(coefficients, ranks, strict=True)
                )
                assert ksum >= 0
                gap = plus(
                    scaled(times(C, D, U), 5 - same),
                    scaled(times(D, D, D), same),
                    scaled(times(C, D, D), -5),
                    scaled(times(S, D, D), -hsum),
                    scaled(times(S, displacement), -ksum),
                )
                assert nonnegative(gap)
    assert count == 992
    return count


def run(packet: Path) -> dict:
    raw = (packet / "source/equal_tilt_through_24.json.gz").read_bytes()
    manifest = json.loads((packet / "acquisition/manifest.json").read_text())
    expected = next(
        row["sha256"]
        for row in manifest["retained_members"]
        if row["member"] == "proofs/equal_tilt_through_24.json.gz"
    )
    assert hashlib.sha256(raw).hexdigest() == expected
    bank = json.loads(gzip.decompress(raw))
    assert len(bank) == 117
    for row in bank:
        certificate(row)
    rejected = 0
    for mutation in ("margin", "negative_multiplier"):
        bad = copy.deepcopy(bank[0])
        if mutation == "margin":
            bad["margin"][0] += 1
        else:
            bad["multipliers"][0] = [-1]
        try:
            certificate(bad)
        except AssertionError:
            rejected += 1
        else:
            raise AssertionError(f"Failed mutation control: {mutation}")
    assert rejected == 2
    # theta = 2 atan(t) < 1/12 at t <= 1/24. Bound d <= e(1+e).
    e = Fraction(1, 12)
    d = e * (1 + e)
    assert 32 * d * d < 1  # same rank cell has center distance < 1
    assert (1 + 3 * d) * e + 4 * d < 1  # axial transverse normal cannot separate
    assert (1 - 5 * d) * (1 - e * e / 2) - (1 + 3 * d) * e > 0
    return {
        "format": "n20-bounded-corroboration-v1",
        "certificate_member_sha256": expected,
        "polynomial_certificates_checked": len(bank),
        "mutation_controls_rejected": rejected,
        "bridge_histogram": bridges(),
        "one_diagonal_chain_sign_cases": one_diagonal_chains(),
        "rank_domain": "0 < t <= 1/24",
        "rank_constants_verified": True,
        "scope": (
            "Local necessary inequalities and certificate arithmetic only; "
            "exhaustive sign/graph coverage and large-angle/common-orientation "
            "exclusions remain unverified."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assert __debug__, "Assertions must be enabled."
    signal.alarm(120)
    start = time.monotonic()
    result = run(Path(__file__).resolve().parents[1])
    result["elapsed_seconds"] = round(time.monotonic() - start, 6)
    with args.output.open("x") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    sys.stdout.write(json.dumps(result) + "\n")


if __name__ == "__main__":
    main()
