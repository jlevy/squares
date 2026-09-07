#!/usr/bin/env python3
"""Exact elementary controls accompanying the n=11 enumeration addendum.

Standard library, Python 3.10+. This is NOT an eleven-square packing solver.
It enumerates discrete angle descriptors, checks explicit geometric/arithmetic
controls, and implements a small rational robust-Farkas bound. The supplied
Stromquist restricted-orientation theorem is an input premise, not re-proved.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import combinations
import json
from math import comb
from pathlib import Path
from typing import Iterator, Sequence


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def positive_compositions(n: int, k: int) -> Iterator[tuple[int, ...]]:
    """Ordered multiplicities for k nonempty orientation classes."""
    require(type(n) is int and type(k) is int and 1 <= k <= n,
            "require integers 1 <= k <= n")
    if k == 1:
        yield (n,)
        return
    for first in range(1, n - k + 2):
        for rest in positive_compositions(n - first, k - 1):
            yield (first,) + rest


def weak_compositions(n: int, k: int) -> Iterator[tuple[int, ...]]:
    """Occupancy counts in k named bins, with zero counts allowed."""
    require(type(n) is int and type(k) is int and n >= 0 and k >= 1,
            "require integers n >= 0 and k >= 1")
    if k == 1:
        yield (n,)
        return
    for first in range(n + 1):
        for rest in weak_compositions(n - first, k - 1):
            yield (first,) + rest


def profiles_by_cuts(n: int) -> set[tuple[int, ...]]:
    """Independent enumeration: cuts in the n-1 spaces between n objects."""
    require(type(n) is int and n >= 1, "n must be a positive integer")
    profiles: set[tuple[int, ...]] = set()
    for mask in range(1 << (n - 1)):
        cuts = [0] + [j for j in range(1, n) if mask & (1 << (j - 1))] + [n]
        profiles.add(tuple(b - a for a, b in zip(cuts, cuts[1:])))
    return profiles


def validate_profiles(profiles: Sequence[Sequence[int]], n: int = 11) -> None:
    values = [tuple(p) for p in profiles]
    require(all(all(type(a) is int and a > 0 for a in p) and sum(p) == n
                for p in values), "invalid multiplicity profile")
    require(len(values) == len(set(values)), "duplicate profile")
    require(set(values) == profiles_by_cuts(n), "missing or extraneous profile")


def disk_centers() -> list[tuple[F, F]]:
    """Twelve diameter-one disks fit in a square of side 18/5."""
    return [(F(1, 2) + col + F(row % 2, 2), F(1, 2) + F(13 * row, 15))
            for row in range(4) for col in range(3)]


def check_disks(points: Sequence[tuple[F, F]], side: F = F(18, 5)) -> F:
    require(type(side) in (int, F) and all(type(v) in (int, F) for p in points for v in p),
            "disk control requires exact rational inputs")
    require(len(points) == 12, "expected the twelve-disk control")
    require(all(F(1, 2) <= v <= side - F(1, 2) for p in points for v in p),
            "a disk crosses a wall")
    distances = [(p[0] - q[0])**2 + (p[1] - q[1])**2
                 for p, q in combinations(points, 2)]
    require(min(distances) >= 1, "disk interiors overlap")
    return min(distances)


def trump_side_upper() -> F:
    """Prove an upper enclosure for U from the supplied polynomial/root definition."""
    coefficients = (5, -10, -2, 14, 12, -6, 2, 2, -1)
    derivative = (40, -70, -12, 70, 48, -18, 4, 2)
    def poly(cs, x):
        out = F(0)
        for a in cs:
            out = out*x + a
        return out
    lo, hi = F(36, 100), F(37, 100)
    derivative_lower = sum(a * (lo if a >= 0 else hi)**(7-j)
                           for j, a in enumerate(derivative))
    require(derivative_lower > 0, "root uniqueness not established")
    require(poly(coefficients, lo) < 0 < poly(coefficients, hi), "root existence not established")
    for _ in range(80):
        mid = (lo+hi)/2
        if poly(coefficients, mid) < 0:
            lo = mid
        else:
            hi = mid
    denominator_lower = 1+2*lo-hi*hi
    require(denominator_lower > 0, "side denominator not positive")
    return (6*hi+4)/denominator_lower


def angular_arithmetic() -> dict:
    """Arithmetic for two conditional occupancy cuts, with rational premises.

    The bound U < q = 3.8771 is checked from the supplied root definition.
    The remaining source premise is that every 0/45-degree packing requires side >= 2 + 4 sqrt(2)/3.
    The analytic proof cos(delta)+sin(delta) <= 1+delta is in the addendum.
    """
    q, delta, root2_lower = F(38771, 10000), F(1, 500), F(1414213, 1000000)
    require(trump_side_upper() < q, "U < q was not proved")
    require(root2_lower > 0 and root2_lower**2 < 2, "invalid sqrt(2) lower bound")
    restricted_lower = 2 + F(4, 3) * root2_lower
    required_side_upper = q * (1 + delta)
    margin = restricted_lower - required_side_upper
    require(margin > 0, "cannot exclude the two narrow angle neighborhoods")
    axis_margin = 4 - required_side_upper
    require(axis_margin > 0, "nine-point near-axis cut not justified")
    return {"side_upper_q": str(q), "delta_radians": str(delta),
            "sqrt2_lower": str(root2_lower),
            "restricted_bound_rational_lower": str(restricted_lower),
            "rounded_packing_side_upper": str(required_side_upper),
            "obliquity_margin": str(margin), "near_axis_grid_margin": str(axis_margin),
            "U_less_than_q_checked_from_root_definition": True,
            "premises": ["Supplied defining polynomial and intended root for U",
                         "Stromquist exact 0/45-degree lower bound"],
            "scope": "Arithmetic supporting deductions in the addendum; not a new s(11) bound"}


def dot(a: tuple[F, F], b: tuple[F, F]) -> F:
    return a[0] * b[0] + a[1] * b[1]


def angle_controls() -> dict:
    """Show why independently folding angles or rotating at fixed side is unsafe."""
    t = F(1, 10)
    c, s = (1 - t*t) / (1 + t*t), 2*t / (1 + t*t)
    require(c*c + s*s == 1, "rotation is not exact")
    require((c+s)/2 > F(1, 2), "rotated unit-square wall fixture failed")
    # A and B originally have common axes u,v and center difference u. They touch.
    u, v = (c, s), (-s, c)
    require(dot(u, u) == 1 and dot(v, u) == 0, "initial pair separation failed")
    # Reflect only A's orientation from theta to -theta, without moving either center.
    # A point 0.51 u from A's center lies strictly in the reflected A and in B.
    p = (F(51, 100)*c, F(51, 100)*s)
    reflected_axes = ((c, -s), (s, c))
    require(all(abs(dot(a, p)) < F(1, 2) for a in reflected_axes),
            "reflected A interior witness failed")
    pb = (p[0]-u[0], p[1]-u[1])
    require(all(abs(dot(a, pb)) < F(1, 2) for a in (u, v)),
            "B interior witness failed")
    # Translate both centers by (1,1); both before/after squares fit in C_3.
    h = (c+s)/2
    centers = ((F(1), F(1)), (1+c, 1+s))
    require(all(h <= w <= 3-h for center in centers for w in center),
            "pair-control containment failed")
    # Exact uniform-angle-core formula, tested at several rational half-tangents.
    for a in (F(1, 1000), F(1, 10), F(1, 3)):
        cc, ss = (1-a*a)/(1+a*a), 2*a/(1+a*a)
        gamma = cc+ss
        require(gamma > 1 and (1/gamma)*gamma == 1, "core transfer control")
    return {"half_tangent": str(t), "cos": str(c), "sin": str(s),
            "fixed_side_rotation_violates_wall": True,
            "independent_reflection_turns_touching_pair_into_strict_overlap": True,
            "strict_overlap_witness_relative_to_A": [str(x) for x in p],
            "scope": "Exact counterexamples to invalid simplifications, not packing exclusions"}


Interval = tuple[F, F]


def robust_farkas_gap(A: Sequence[Sequence[Interval]], b: Sequence[Interval],
                      multipliers: Sequence[F], bounds: Sequence[Interval]) -> F:
    """Return certified lower(r.z) - upper(y.b) for Az<=b, z in bounds.

    A,b must already enclose the SAME branch over the ENTIRE parameter box.
    A positive return proves infeasibility. A nonpositive return is undecided.
    No geometric enclosure-generation or global completeness is implemented here.
    """
    m, n = len(A), len(bounds)
    require(m >= 1 and n >= 1 and len(b) == m and len(multipliers) == m,
            "dimension mismatch")
    require(all(len(row) == n for row in A), "ragged coefficient matrix")
    require(all(y >= 0 for y in multipliers), "negative multiplier")
    all_intervals = [x for row in A for x in row] + list(b) + list(bounds)
    require(all(len(x) == 2 and x[0] <= x[1] for x in all_intervals),
            "invalid interval")
    require(all(type(v) in (int, F) for pair in all_intervals for v in pair)
            and all(type(y) in (int, F) for y in multipliers),
            "Farkas checker requires exact rational inputs")
    rhs_upper = sum(y * bi[1] for y, bi in zip(multipliers, b))
    lhs_lower = F(0)
    for j, (lo, hi) in enumerate(bounds):
        rlo = sum(y * A[i][j][0] for i, y in enumerate(multipliers))
        rhi = sum(y * A[i][j][1] for i, y in enumerate(multipliers))
        lhs_lower += min(rlo*lo, rlo*hi, rhi*lo, rhi*hi)
    return lhs_lower - rhs_upper


def catalogue() -> dict:
    groups = {str(k): list(positive_compositions(11, k)) for k in range(1, 12)}
    profiles = [p for rows in groups.values() for p in rows]
    validate_profiles(profiles)
    unordered = sorted({tuple(sorted(p, reverse=True)) for p in profiles})
    require(len(unordered) == 56, "partition count")
    hist = list(weak_compositions(11, 3))
    # Named bins: near-axis, strict-middle, near-45. Geometric proof is in addendum.
    survivors = [p for p in hist if p[0] <= 9 and p[1] >= 1]
    require(len(hist) == 78 and len(survivors) == 65, "histogram counts")
    return {
        "scope": "Complete DISCRETE descriptor catalogues only; continuous packing cases unsolved",
        "n": 11, "exact_angle_class_count_definition": "distinct orientations modulo pi/2, NOT folded angles",
        "ordered_multiplicities_by_k": groups,
        "profile_count_by_k": {str(k): comb(10, k-1) for k in range(1, 12)},
        "total_ordered_profiles": len(profiles),
        "unordered_multiplicity_partitions": unordered,
        "unordered_partitions_are_not_an_ordered_angle_case_cover_by_themselves": True,
        "three_bins": ["near_axis", "strict_middle", "near_45"],
        "delta_radians": "1/500", "side_upper_q": "38771/10000",
        "three_bin_profiles_before_cuts": hist,
        "three_bin_profiles_after_elementary_cuts": survivors,
        "remaining_continuous_cases_status": "ALL UNRESOLVED BY THIS CATALOGUE",
        "chirality_lifts_required_for_configuration_geometry": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", type=Path, help="write catalogue and control receipts here")
    args = parser.parse_args()
    data = catalogue()
    receipt = {
        "status": "PASS: elementary controls only",
        "ordered_profiles": data["total_ordered_profiles"],
        "unordered_partitions": len(data["unordered_multiplicity_partitions"]),
        "histogram_counts": {"before": 78, "after_elementary_cuts": 65},
        "twelve_disk_control": {"container_side": "18/5", "minimum_distance_squared": str(check_disks(disk_centers())),
            "nearest_adjacent_row_distance_squared": "901/900",
            "conclusion": "The unrestricted diameter-one disk relaxation fits 11 (indeed 12) disks by side 3.6"},
        "angular_arithmetic": angular_arithmetic(), "angle_controls": angle_controls(),
        "new_global_square_packing_bound": None,
    }
    if args.write:
        args.write.mkdir(parents=True, exist_ok=True)
        (args.write / "profile_catalogue.json").write_text(json.dumps(data, indent=2)+"\n")
        (args.write / "elementary_results.json").write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
