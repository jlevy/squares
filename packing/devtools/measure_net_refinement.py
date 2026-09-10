#!/usr/bin/env python3
"""Measure what a finer direction net buys the retained certificate.

Condition 4 ties the shrink to the net: with `D` the largest half-gap tangent, T-022's
sharpened containment admits any `B` with `B^2 (1 + D)^2 < 1 + D^2`, so a finer net
admits a larger `B`, and the gain is realised by uniform dilation, since a certificate
at `(L, B, net)` rules out every side below `L sqrt(1 + D^2) / (B (1 + D))`. A finer
net also adds directions at which Condition 5 must hold, which can only lower the least
covered mass. This holds the atoms fixed and measures both effects, net by net:

- at the largest grid `B` the sharpened test admits, the least mass over every
  direction (a certificate at the same side if it passes, with no dilation room left);
- at the certificate's own `B`, the least mass over the directions the finer net adds
  (the coarser directions are the control row, swept once and reused);
- the crossing shrink: the least grid `B` at which the finer net passes at the
  certificate's own side, by bisection between those two, and the dilation supremum
  `L sqrt(1 + D^2) / (B (1 + D))` it buys, as an exact surd in T-022's form.

The bisection is sound because the least covered mass is nondecreasing in `B` at a
fixed side and net: a larger concentric closed core covers a superset of the atoms at
every centre, and its admissible-centre square is a subset. So a direction that passes
at some `B` passes at every larger one, a test sweeps only the directions not yet known
to pass at its `B`, and a failure is decided by the first failing direction.

The decision is scale-invariant. With `M` the total mass and `m` the least covered
mass, the atoms certify at `(L, B, net)` iff `M / m < n`, the weights rescaled by
`1 / m`; the rescaled least mass is exactly 1, which Condition 5 allows. Every decision
here is in `Fraction`s. Floats propose the bisection's first grid value and nothing else.

Usage, from `packing/`:

    uv run --frozen python -m devtools.measure_net_refinement --nets 360 720 \\
        --output cases/n11_fractional_certificate/net-refinement-381-100.json
"""

from __future__ import annotations

import argparse
import json
import math
import time
from collections.abc import Sequence
from dataclasses import dataclass, field
from fractions import Fraction
from itertools import pairwise
from pathlib import Path

from strif import atomic_output_file

from devtools.decide_certificate import load_frozen_bytes, read_bounded
from sqpack.fractional.certificate import Certificate, sweep_direction_minimum

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
CASE = PACKING / "cases" / "n11_fractional_certificate"
DEFAULT_NETS = (360, 720, 1440)

# Shrinks are chosen on this grid: the largest multiple passing a containment test, and
# the crossing to within `--resolution` of it.
DENOM = 10**7


def half_gap_tangent(half_tangents: tuple[Fraction, ...]) -> Fraction:
    """`D`, as `Certificate.largest_half_gap_tangent` computes it."""
    return max((right - left) / (1 + left * right) for left, right in pairwise(half_tangents))


def sharp_containment(side: Fraction, gap: Fraction) -> bool:
    """T-022's sharpened test `B^2 (1 + D)^2 < 1 + D^2`."""
    return (side * (1 + gap)) ** 2 < 1 + gap * gap


def coarse_containment(side: Fraction, gap: Fraction) -> bool:
    """The retained theorem's Condition 4, `B (1 + D) < 1`."""
    return side * (1 + gap) < 1


def largest_sharp_side(gap: Fraction, denom: int = DENOM) -> Fraction:
    """The largest `b / denom` passing the sharpened test; `isqrt` proposes, Fractions decide.

    A float never decides: the integer square root of the floored target is the start
    of two exact loops that settle the grid value either side of it.
    """
    scaled = (1 + gap * gap) / (1 + gap) ** 2 * denom * denom
    b = math.isqrt(scaled.numerator // scaled.denominator)
    while not sharp_containment(Fraction(b, denom), gap):
        b -= 1
    while sharp_containment(Fraction(b + 1, denom), gap):
        b += 1
    return Fraction(b, denom)


def largest_coarse_side(gap: Fraction, denom: int = DENOM) -> Fraction:
    """The largest `b / denom` passing the coarse test."""
    ratio = Fraction(denom) / (1 + gap)
    b = ratio.numerator // ratio.denominator
    while not coarse_containment(Fraction(b, denom), gap):
        b -= 1
    while coarse_containment(Fraction(b + 1, denom), gap):
        b += 1
    return Fraction(b, denom)


def dilation_supremum(
    outer_side: Fraction, side: Fraction, gap: Fraction
) -> tuple[Fraction, str]:
    """`L sqrt(1 + D^2) / (B (1 + D))`: its exact square, and it as `p*sqrt(A)/q`."""
    num, den = gap.numerator, gap.denominator
    radicand = den * den + num * num
    coefficient = outer_side / (side * (den + num))
    squared = coefficient * coefficient * radicand
    return squared, f"{coefficient.numerator}*sqrt({radicand})/{coefficient.denominator}"


def uniform_net(limit: Fraction, steps: int) -> tuple[Fraction, ...]:
    """`generate.net_half_tangents`: `steps` equal half-tangent steps up to `limit`."""
    return tuple(limit * k / steps for k in range(steps + 1))


@dataclass
class Knowledge:
    """What the sweeps so far say about each direction, keyed by its half-tangent.

    `passing_at[t]` is the least `B` at which direction `t` is known to cover mass above
    the threshold; by monotonicity it passes at every larger `B`. `minima[t, B]` is every
    exact least covered mass a sweep decided, so a direction is never swept twice at one
    `B`.
    """

    threshold: Fraction
    passing_at: dict[Fraction, Fraction] = field(default_factory=dict)
    minima: dict[tuple[Fraction, Fraction], Fraction] = field(default_factory=dict)

    def record(self, tangent: Fraction, side: Fraction, minimum: Fraction) -> None:
        self.minima[tangent, side] = minimum
        if minimum > self.threshold:
            known = self.passing_at.get(tangent)
            if known is None or side < known:
                self.passing_at[tangent] = side

    def known_to_pass(self, tangent: Fraction, side: Fraction) -> bool:
        known = self.passing_at.get(tangent)
        return known is not None and known <= side


@dataclass(frozen=True)
class Sweep:
    """One pass over a list of directions: the least mass, where, and how many ran."""

    least: Fraction | None
    argmin: int | None
    swept: int
    seconds: float


def sweep(
    certificate: Certificate,
    indices: Sequence[int],
    knowledge: Knowledge,
    *,
    stop_on_failure: bool,
) -> Sweep:
    """Sweep the listed directions at the certificate's `B`, recording each minimum.

    With `stop_on_failure` the pass returns at the first direction at or below the
    threshold: a failure is one direction's, a pass is every direction's.
    """
    started = time.monotonic()
    least: Fraction | None = None
    argmin: int | None = None
    swept = 0
    for k in indices:
        minimum, _witness = sweep_direction_minimum(certificate, certificate.directions[k])
        knowledge.record(certificate.half_tangents[k], certificate.square_side, minimum)
        swept += 1
        if least is None or minimum < least:
            least, argmin = minimum, k
        if stop_on_failure and minimum <= knowledge.threshold:
            break
    return Sweep(least, argmin, swept, time.monotonic() - started)


def at(
    certificate: Certificate, half_tangents: tuple[Fraction, ...], side: Fraction
) -> Certificate:
    return Certificate(
        n=certificate.n,
        outer_side=certificate.outer_side,
        square_side=side,
        atoms=certificate.atoms,
        half_tangents=half_tangents,
        symmetry=certificate.symmetry,
    )


def fraction_field(value: Fraction | None) -> dict[str, object] | None:
    return None if value is None else {"exact": str(value), "float": float(value)}


def crossing(
    certificate: Certificate,
    half_tangents: tuple[Fraction, ...],
    lower: Fraction,
    upper: Fraction,
    *,
    knowledge: Knowledge,
    resolution: Fraction,
) -> tuple[Fraction, Fraction, list[dict[str, object]]]:
    """Bisect `(lower, upper]` on the grid to the least passing `B` within `resolution`.

    `lower` must be a known failure and `upper` a known pass. Each test sweeps only the
    directions not known to pass at its `B`, the last failing direction first.
    """
    lo, hi = int(lower * DENOM), int(upper * DENOM)
    if Fraction(lo, DENOM) != lower or Fraction(hi, DENOM) != upper:
        raise ValueError("the bracket must sit on the shrink grid")
    first: int | None = None
    tests: list[dict[str, object]] = []
    while Fraction(hi - lo, DENOM) > resolution:
        mid = (lo + hi) // 2
        side = Fraction(mid, DENOM)
        candidate = at(certificate, half_tangents, side)
        indices = [
            k for k, t in enumerate(half_tangents) if not knowledge.known_to_pass(t, side)
        ]
        if first is not None and first in indices:
            indices.remove(first)
            indices.insert(0, first)
        result = sweep(candidate, indices, knowledge, stop_on_failure=True)
        passes = result.least is None or result.least > knowledge.threshold
        tests.append(
            {
                "B": str(side),
                "least_over_swept": fraction_field(result.least),
                "argmin": result.argmin,
                "directions_unknown": len(indices),
                "swept": result.swept,
                "passes": passes,
                "seconds": round(result.seconds, 1),
            }
        )
        print(
            f"    B={float(side):.7f}  {'PASS' if passes else 'FAIL'}  "
            f"({result.swept}/{len(indices)} directions, {result.seconds:.1f}s)",
            flush=True,
        )
        if passes:
            hi = mid
        else:
            lo = mid
            first = result.argmin
    return Fraction(lo, DENOM), Fraction(hi, DENOM), tests


def measure(
    certificate: Certificate,
    record: dict[str, object],
    nets: tuple[int, ...],
    resolution: Fraction,
) -> list[dict[str, object]]:
    limit = Fraction(str(record["angle_limit"]))
    base = int(str(record["direction_steps"]))
    threshold = certificate.total_mass / certificate.n
    knowledge = Knowledge(threshold)
    own = certificate.square_side
    rows: list[dict[str, object]] = []
    for steps in (base, *nets):
        half_tangents = uniform_net(limit, steps)
        gap = half_gap_tangent(half_tangents)
        sharp, coarse = largest_sharp_side(gap), largest_coarse_side(gap)
        started = time.monotonic()

        # The certificate's own B: the base net is the control, swept in full; a finer
        # net sweeps only the directions it adds, the rest being reused exactly.
        candidate = at(certificate, half_tangents, own)
        new = [k for k, t in enumerate(half_tangents) if (t, own) not in knowledge.minima]
        sweep(candidate, new, knowledge, stop_on_failure=False)
        own_minima = [knowledge.minima[t, own] for t in half_tangents]
        least_own = min(own_minima)
        argmin_own = own_minima.index(least_own)
        passes_own = least_own > threshold

        # The sharpened-test limit, every direction.
        sharp_candidate = at(certificate, half_tangents, sharp)
        sharp_result = sweep(
            sharp_candidate, range(steps + 1), knowledge, stop_on_failure=False
        )
        if sharp_result.least is None:
            raise ValueError("a net must have at least one direction")
        passes_sharp = sharp_result.least > threshold

        row: dict[str, object] = {
            "K": steps,
            "control": steps == base,
            "D": fraction_field(gap),
            "B_own": str(own),
            "B_sharp": str(sharp),
            "B_coarse": str(coarse),
            "least_at_B_own": fraction_field(least_own),
            "argmin_at_B_own": argmin_own,
            "passes_at_B_own": passes_own,
            "directions_added": len(new),
            "least_at_B_sharp": fraction_field(sharp_result.least),
            "argmin_at_B_sharp": sharp_result.argmin,
            "passes_at_B_sharp": passes_sharp,
        }
        for label, side, passes in (("own", own, passes_own), ("sharp", sharp, passes_sharp)):
            squared, surd = dilation_supremum(certificate.outer_side, side, gap)
            row[f"dilation_supremum_at_B_{label}"] = {
                "certified": passes,
                "squared": str(squared),
                "surd": surd,
                "float": math.sqrt(squared.numerator / squared.denominator),
            }
        if steps != base:
            if passes_own:
                lo_b, hi_b, tests = own, own, []
            elif passes_sharp:
                lo_b, hi_b, tests = crossing(
                    certificate,
                    half_tangents,
                    own,
                    sharp,
                    knowledge=knowledge,
                    resolution=resolution,
                )
            else:
                lo_b, hi_b, tests = sharp, None, []
            row["crossing"] = {
                "B_fail": str(lo_b),
                "B_pass": None if hi_b is None else str(hi_b),
                "tests": tests,
            }
            if hi_b is not None:
                squared, surd = dilation_supremum(certificate.outer_side, hi_b, gap)
                row["dilation_supremum_at_B_pass"] = {
                    "certified": True,
                    "squared": str(squared),
                    "surd": surd,
                    "float": math.sqrt(squared.numerator / squared.denominator),
                }
        row["seconds"] = round(time.monotonic() - started, 1)
        rows.append(row)
        print(
            f"K={steps:5d}  D={float(gap):.7f}  own B: least={float(least_own):.6f} "
            f"{'PASS' if passes_own else 'FAIL'}  sharp B={float(sharp):.7f}: "
            f"least={float(sharp_result.least):.6f} {'PASS' if passes_sharp else 'FAIL'}  "
            f"({row['seconds']}s)",
            flush=True,
        )
    return rows


def repository_relative(path: Path, role: str) -> str:
    """The path as the record states it; a path outside the repository is refused
    before any sweep runs, since the record cannot name it."""
    try:
        return path.relative_to(REPO).as_posix()
    except ValueError:
        raise SystemExit(f"the {role} {path} is not inside the repository") from None


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=CASE / "certificate.json")
    parser.add_argument("--output", type=Path, help="where to write the rows")
    parser.add_argument("--nets", type=int, nargs="+", default=list(DEFAULT_NETS))
    parser.add_argument(
        "--resolution",
        type=Fraction,
        default=Fraction(1, 10**6),
        help="stop bisecting the crossing shrink once the bracket is this narrow",
    )
    args = parser.parse_args(argv)

    certificate_path = args.certificate.resolve()
    certificate, record = load_frozen_bytes(read_bounded(certificate_path))
    side = certificate.outer_side
    output = (
        args.output.resolve()
        if args.output
        else CASE / f"net-refinement-{side.numerator}-{side.denominator}.json"
    )
    payload: dict[str, object] = {
        "certificate": repository_relative(certificate_path, "certificate"),
        "certificate_id": record["id"],
        "threshold_M_over_n": str(certificate.total_mass / certificate.n),
        "shrink_grid_denominator": DENOM,
        "resolution": str(args.resolution),
    }
    output_label = repository_relative(output, "output")
    payload["rows"] = measure(certificate, record, tuple(args.nets), args.resolution)
    with atomic_output_file(output) as temporary:
        temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output_label}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
