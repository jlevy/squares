#!/usr/bin/env python3
"""Measure what a finer direction net buys the frozen *threshold* certificate.

This is `devtools.measure_net_refinement` for threshold certificates: the same three
measurements, run against `sqpack.fractional.threshold`'s charge instead of the point
route's covered mass, because a threshold atom ``(S, k, w)`` charges a core by the size
of its trace on ``S`` and so is more angle-sensitive than a point mass.

``Condition 4`` ties the shrink ``B`` to the net through the largest half-gap tangent
``D``: T-022's sharpened containment admits any ``B`` with ``B^2 (1 + D)^2 < 1 + D^2``,
so a finer net admits a larger ``B``, and the gain is realised by inverse dilation of
placements, which rules out every side below ``L sqrt(1 + D^2) / (B (1 + D))``. That
argument uses only Conditions 1 to 4, so it applies to a threshold certificate
unchanged. A finer net also adds directions at which ``Condition 5'`` must hold, which
can only lower the least charge. This holds the atoms fixed and measures both, net by
net:

- at the largest grid ``B`` the sharpened test admits, the least charge over every
  direction of the finer net;
- at the certificate's own ``B``, the least charge over the directions the finer net
  adds (the coarser directions are swept once and reused);
- the crossing shrink: the least grid ``B`` at which every direction of the finer net is
  charged above ``M / n``, by bisection between those two, and the dilation supremum it
  buys, as an exact surd.

Why ``M / n`` and not 1. A threshold certificate is stated normalised: ``Condition 5'``
asks for a least charge of at least 1 and ``Condition 2'`` for a total budget ``M``
below ``n``. Both conditions are homogeneous in the weights, so with ``m`` the least
charge of the *unscaled* atoms the rescaling ``w -> w / m`` produces a certificate at
the same ``(L, B, net)`` whose least charge is exactly 1 and whose budget is ``M / m``;
that certificate is admissible exactly when ``M / m < n``, i.e. when ``m > M / n``. So
the sweeps here are run on the unscaled atoms and read against ``M / n``, and the
rescaling by the rational ``1 / m`` is applied only when a record is written out.

Why the bisection is sound. At a fixed side and net the least charge is nondecreasing in
``B``: a larger concentric closed core contains a superset of the points of every atom
at every centre, each threshold atom's charge ``w [|trace| >= k]`` is monotone in the
trace, the point atoms' weights are nonnegative, and the admissible-centre square is a
subset. So a direction charged above the threshold at some ``B`` is charged above it at
every larger ``B``, a test sweeps only the directions not yet known to pass at its
``B``, and a failure is decided by the first failing direction.

The nets are nested (``t_k = T k / N`` with ``N`` doubling), so the directions of a
coarser net are directions of every finer one, and two further reuses follow. A least
charge decided at ``(t, B)`` is reused verbatim at every net containing ``t``. And a
``B`` at which the coarser net already fails is a failure for the finer net too, so the
coarser net's largest known failing shrink is a sound lower bracket for the finer net's
bisection.

Every decision here is in ``Fraction``s. Floats appear in the logs and in the printed
progress and nowhere else; no float proposes or decides a grid value.

Usage, from `packing/`:

    uv run --frozen --all-extras --group dev python \
        -m devtools.measure_threshold_net_refinement --nets 360 720 --workers 2
"""

from __future__ import annotations

import argparse
import json
import math
import os
import time
from collections.abc import Iterable, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from fractions import Fraction
from multiprocessing import get_context
from pathlib import Path
from typing import Any

from devtools.decide_threshold_certificate import load
from devtools.dilation_corollary import PositiveQuadraticSurd
from devtools.measure_net_refinement import (
    DENOM,
    half_gap_tangent,
    largest_coarse_side,
    largest_sharp_side,
    sharp_containment,
    uniform_net,
)
from sqpack.fractional.model import Direction
from sqpack.fractional.threshold import Point, ThresholdCertificate, minimum_charge

PACKING = Path(__file__).resolve().parents[1]
"""The build root, `packing/`; the frozen source is named relative to it, not to a cwd."""

DEFAULT_CERTIFICATE = PACKING / "cases" / "n11_threshold_certificate" / "certificate.json"
DEFAULT_NETS = (360, 720, 1440)


def grid_label(side: Fraction) -> str:
    """The shrink as its integer numerator on the ``1 / DENOM`` grid, for a filename."""

    scaled = side * DENOM
    if scaled.denominator != 1:
        raise ValueError(f"shrink {side} is not on the 1/{DENOM} grid")
    return str(scaled.numerator)


def decimal_places(squared: Fraction, places: int) -> str:
    """``sqrt(squared)`` truncated to ``places`` decimals, by integer square root."""

    scale = 10**places
    scaled = math.isqrt(squared.numerator * scale * scale // squared.denominator)
    whole, rest = divmod(scaled, scale)
    return f"{whole}.{rest:0{places}d}"


def dilation_supremum(
    outer_side: Fraction, side: Fraction, gap: Fraction
) -> PositiveQuadraticSurd:
    """``L sqrt(1 + D^2) / (B (1 + D))`` in T-022's form, exactly.

    With ``D = num / den`` this is ``L sqrt(den^2 + num^2) / (B (den + num))``: the
    same coefficient and radicand `devtools.dilation_corollary.sharp_dilation_ceiling`
    builds, scaled by ``L``.
    """

    num, den = gap.numerator, gap.denominator
    coefficient = outer_side / (side * (den + num))
    return PositiveQuadraticSurd(coefficient, den * den + num * num)


def surd_field(surd: PositiveQuadraticSurd) -> dict[str, Any]:
    return {
        "surd": surd.exact,
        "squared": str(surd.squared),
        "decimal_20": decimal_places(surd.squared, 20),
        "float": math.sqrt(surd.squared.numerator / surd.squared.denominator),
    }


def fraction_field(value: Fraction | None) -> dict[str, Any] | None:
    return None if value is None else {"exact": str(value), "float": float(value)}


def at(
    certificate: ThresholdCertificate, half_tangents: tuple[Fraction, ...], side: Fraction
) -> ThresholdCertificate:
    """The same atoms at another net and another shrink."""

    return ThresholdCertificate(
        n=certificate.n,
        outer_side=certificate.outer_side,
        square_side=side,
        atoms=certificate.atoms,
        threshold_atoms=certificate.threshold_atoms,
        half_tangents=half_tangents,
        symmetry=certificate.symmetry,
    )


@dataclass
class Shared:
    """What a forked worker reads: set before the pool is built, never after.

    The certificate carries 584 point atoms and 320 threshold atoms of very long
    rationals, so it is inherited across the fork rather than pickled per task; the
    tasks themselves are direction indices.
    """

    certificate: ThresholdCertificate | None = None
    directions: tuple[Direction, ...] = ()


SHARED = Shared()


def minimum_at(index: int) -> tuple[int, Fraction, Point]:
    """The least charge and its witness at one direction of the shared certificate."""

    certificate = SHARED.certificate
    if certificate is None:
        raise RuntimeError("the shared certificate was not set before the sweep")
    return (
        index,
        *minimum_charge(
            certificate.atoms,
            certificate.threshold_atoms,
            SHARED.directions[index],
            certificate.outer_side,
            certificate.square_side,
        ),
    )


@dataclass
class Knowledge:
    """What the sweeps so far say about each direction, keyed by its half-tangent.

    ``passing_at[t]`` is the least ``B`` at which direction ``t`` is known to be charged
    above the threshold; by monotonicity it passes at every larger ``B``.
    ``minima[t, B]`` is every exact least charge a sweep decided, with its witness, so a
    direction is never swept twice at one shrink and the nested nets share their rows.
    """

    threshold: Fraction
    passing_at: dict[Fraction, Fraction] = field(default_factory=dict)
    minima: dict[tuple[Fraction, Fraction], tuple[Fraction, Point]] = field(
        default_factory=dict
    )

    def record(
        self, tangent: Fraction, side: Fraction, charge: Fraction, witness: Point
    ) -> None:
        self.minima[tangent, side] = (charge, witness)
        if charge > self.threshold:
            known = self.passing_at.get(tangent)
            if known is None or side < known:
                self.passing_at[tangent] = side

    def known_to_pass(self, tangent: Fraction, side: Fraction) -> bool:
        known = self.passing_at.get(tangent)
        return known is not None and known <= side


@dataclass(frozen=True)
class Sweep:
    """One pass over a list of directions: the least charge, where, and how many ran."""

    least: Fraction | None
    argmin: int | None
    swept: int
    seconds: float


def sweep(
    certificate: ThresholdCertificate,
    indices: Sequence[int],
    knowledge: Knowledge,
    log: Path,
    *,
    workers: int,
    stop_on_failure: bool,
) -> Sweep:
    """Sweep the listed directions at the certificate's ``B``, recording each minimum.

    With ``stop_on_failure`` the pass returns at the first direction at or below the
    threshold: a failure is one direction's, a pass is every direction's.
    """

    started = time.monotonic()
    SHARED.certificate = certificate
    SHARED.directions = certificate.directions
    least: Fraction | None = None
    argmin: int | None = None
    swept = 0
    stopped = False
    block = max(1, 4 * workers)
    with log.open("a", encoding="utf-8") as sink:

        def consume(results: Iterable[tuple[int, Fraction, Point]]) -> bool:
            """Record and log one block; report whether a failure ended the pass."""
            nonlocal least, argmin, swept
            hit = False
            for index, charge, witness in results:
                knowledge.record(
                    certificate.half_tangents[index], certificate.square_side, charge, witness
                )
                swept += 1
                if least is None or charge < least:
                    least, argmin = charge, index
                sink.write(
                    json.dumps(
                        {
                            "direction": index,
                            "half_tangent": str(certificate.half_tangents[index]),
                            "B": str(certificate.square_side),
                            "charge": str(charge),
                            "charge_float": float(charge),
                            "above_threshold": charge > knowledge.threshold,
                            "witness": [str(witness[0]), str(witness[1])],
                        }
                    )
                    + "\n"
                )
                if stop_on_failure and charge <= knowledge.threshold:
                    hit = True
                    break
            sink.flush()
            return hit

        if workers <= 1:
            stopped = consume(minimum_at(k) for k in indices)
        else:
            with ProcessPoolExecutor(
                max_workers=workers, mp_context=get_context("fork")
            ) as pool:
                for start in range(0, len(indices), block):
                    if stopped:
                        break
                    stopped = consume(pool.map(minimum_at, indices[start : start + block]))
    return Sweep(least, argmin, swept, time.monotonic() - started)


def replay(
    knowledge: Knowledge,
    half_tangents: tuple[Fraction, ...],
    side: Fraction,
    log: Path,
) -> None:
    """Write the rows a finer net inherits from a coarser one at the same shrink."""

    with log.open("a", encoding="utf-8") as sink:
        for index, tangent in enumerate(half_tangents):
            found = knowledge.minima.get((tangent, side))
            if found is None:
                continue
            charge, witness = found
            sink.write(
                json.dumps(
                    {
                        "direction": index,
                        "half_tangent": str(tangent),
                        "B": str(side),
                        "charge": str(charge),
                        "charge_float": float(charge),
                        "above_threshold": charge > knowledge.threshold,
                        "witness": [str(witness[0]), str(witness[1])],
                        "reused": True,
                    }
                )
                + "\n"
            )


def log_path(work: Path, steps: int, side: Fraction) -> Path:
    return work / f"dirmin-N{steps}-B{grid_label(side)}.jsonl"


def full_sweep(
    certificate: ThresholdCertificate,
    half_tangents: tuple[Fraction, ...],
    side: Fraction,
    *,
    knowledge: Knowledge,
    work: Path,
    steps: int,
    workers: int,
) -> tuple[Fraction, int, int]:
    """Every direction at ``side``, sweeping only what is not already decided there."""

    candidate = at(certificate, half_tangents, side)
    fresh = [k for k, t in enumerate(half_tangents) if (t, side) not in knowledge.minima]
    log = log_path(work, steps, side)
    replay(knowledge, half_tangents, side, log)
    if fresh:
        sweep(candidate, fresh, knowledge, log, workers=workers, stop_on_failure=False)
    charges = [knowledge.minima[t, side][0] for t in half_tangents]
    least = min(charges)
    return least, charges.index(least), len(fresh)


def crossing(
    certificate: ThresholdCertificate,
    half_tangents: tuple[Fraction, ...],
    lower: Fraction,
    upper: Fraction,
    *,
    steps: int,
    knowledge: Knowledge,
    work: Path,
    workers: int,
    resolution: Fraction,
) -> tuple[Fraction, Fraction, list[dict[str, Any]]]:
    """Bisect ``(lower, upper]`` on the grid to the least passing ``B``.

    ``lower`` must be a known failure and ``upper`` a known pass. Each test sweeps only
    the directions not known to pass at its ``B``, the last failing direction first.
    """

    lo, hi = lower * DENOM, upper * DENOM
    if lo.denominator != 1 or hi.denominator != 1:
        raise ValueError("the bracket must sit on the shrink grid")
    low, high = lo.numerator, hi.numerator
    first: int | None = None
    tests: list[dict[str, Any]] = []
    while Fraction(high - low, DENOM) > resolution:
        mid = (low + high) // 2
        side = Fraction(mid, DENOM)
        candidate = at(certificate, half_tangents, side)
        indices = [
            k for k, t in enumerate(half_tangents) if not knowledge.known_to_pass(t, side)
        ]
        if first is not None and first in indices:
            indices.remove(first)
            indices.insert(0, first)
        log = log_path(work, steps, side)
        result = sweep(
            candidate, indices, knowledge, log, workers=workers, stop_on_failure=True
        )
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
            high = mid
        else:
            low = mid
            first = result.argmin
    return Fraction(low, DENOM), Fraction(high, DENOM), tests


def rescaled_record(
    record: dict[str, Any], steps: int, side: Fraction, factor: Fraction
) -> dict[str, Any]:
    """The frozen record's own layout, at a new net and shrink, weights times ``factor``.

    Key order and atom order are the input's; only the declared numbers move. The
    identifier is suffixed with the net so the rescaled record is never mistaken for
    T-025's bytes, and the provenance object keeps its own entries and gains the
    derivation.
    """

    out: dict[str, Any] = {}
    point_mass = Fraction(0)
    threshold_budget = Fraction(0)
    for key, value in record.items():
        if key == "id":
            out[key] = f"{value}-net{steps}"
        elif key == "square_side":
            out[key] = str(side)
        elif key == "direction_steps":
            out[key] = steps
        elif key == "atoms":
            atoms: list[list[str]] = []
            for x, y, w in value:
                weight = Fraction(w) * factor
                point_mass += weight
                atoms.append([x, y, str(weight)])
            out[key] = atoms
        elif key == "threshold_atoms":
            entries: list[dict[str, Any]] = []
            for entry in value:
                if any(
                    key in entry for key in ("variant", "multiplicities", "weighted_points")
                ):
                    raise ValueError(
                        "net refinement accepts unweighted threshold records only; "
                        "weighted coverage has not been admitted"
                    )
                weight = Fraction(entry["weight"]) * factor
                threshold_budget += weight * (len(entry["points"]) // entry["threshold"])
                entries.append(
                    {
                        key2: (str(weight) if key2 == "weight" else value2)
                        for key2, value2 in entry.items()
                    }
                )
            out[key] = entries
        elif key == "provenance":
            out[key] = dict(value) | {
                "derived_from": "cases/n11_threshold_certificate/certificate.json",
                "derivation": (
                    f"net refined to {steps} steps, shrink raised to {side}, "
                    f"every weight multiplied by {factor}"
                ),
            }
        else:
            out[key] = value
    if "point_mass" in out:
        out["point_mass"] = str(point_mass)
    if "threshold_budget" in out:
        out["threshold_budget"] = str(threshold_budget)
    if "total_budget" in out:
        out["total_budget"] = str(point_mass + threshold_budget)
    if "least_cell_charge" in out:
        out["least_cell_charge"] = "1"
    return out


def measure_net(
    certificate: ThresholdCertificate,
    record: dict[str, Any],
    *,
    steps: int,
    knowledge: Knowledge,
    work: Path,
    lower_bracket: Fraction,
    workers: int,
    resolution: Fraction,
) -> dict[str, Any]:
    """One net: the two full sweeps, the crossing shrink, and the dilation it buys."""

    limit = Fraction(str(record["angle_limit"]))
    own = certificate.square_side
    half_tangents = uniform_net(limit, steps)
    gap = half_gap_tangent(half_tangents)
    sharp = largest_sharp_side(gap)
    coarse = largest_coarse_side(gap)
    started = time.monotonic()

    least_own, argmin_own, added = full_sweep(
        certificate,
        half_tangents,
        own,
        knowledge=knowledge,
        work=work,
        steps=steps,
        workers=workers,
    )
    passes_own = least_own > knowledge.threshold
    print(
        f"K={steps:5d}  D={float(gap):.9f}  own B={float(own):.7f}: "
        f"least={float(least_own):.9f} {'PASS' if passes_own else 'FAIL'} "
        f"(+{added} directions)",
        flush=True,
    )

    least_sharp, argmin_sharp, _ = full_sweep(
        certificate,
        half_tangents,
        sharp,
        knowledge=knowledge,
        work=work,
        steps=steps,
        workers=workers,
    )
    passes_sharp = least_sharp > knowledge.threshold
    print(
        f"K={steps:5d}  sharp B={float(sharp):.7f}: least={float(least_sharp):.9f} "
        f"{'PASS' if passes_sharp else 'FAIL'}",
        flush=True,
    )

    row: dict[str, Any] = {
        "K": steps,
        "D": fraction_field(gap),
        "B_own": str(own),
        "B_sharp": str(sharp),
        "B_coarse": str(coarse),
        "threshold_M_over_n": str(knowledge.threshold),
        "least_at_B_own": fraction_field(least_own),
        "argmin_at_B_own": argmin_own,
        "passes_at_B_own": passes_own,
        "directions_added_at_B_own": added,
        "least_at_B_sharp": fraction_field(least_sharp),
        "argmin_at_B_sharp": argmin_sharp,
        "passes_at_B_sharp": passes_sharp,
        "lower_bracket": str(lower_bracket),
    }

    if passes_own:
        fail_at, pass_at, tests = lower_bracket, own, []
    elif passes_sharp:
        fail_at, pass_at, tests = crossing(
            certificate,
            half_tangents,
            max(lower_bracket, own),
            sharp,
            steps=steps,
            knowledge=knowledge,
            work=work,
            workers=workers,
            resolution=resolution,
        )
    else:
        fail_at, pass_at, tests = sharp, None, []
    row["crossing"] = {
        "B_fail": str(fail_at),
        "B_pass": None if pass_at is None else str(pass_at),
        "tests": tests,
    }
    if pass_at is not None:
        # The bisection's passing test skips directions monotonicity already settles, so
        # it knows the crossing shrink passes and not by how much. The rescaling needs
        # the exact least charge over the whole net, so it is swept in full here.
        least_cross, argmin_cross, _ = full_sweep(
            certificate,
            half_tangents,
            pass_at,
            knowledge=knowledge,
            work=work,
            steps=steps,
            workers=workers,
        )
        if least_cross <= knowledge.threshold:
            raise ValueError(f"the crossing shrink {pass_at} does not pass after all")
        row["least_at_B_pass"] = fraction_field(least_cross)
        row["argmin_at_B_pass"] = argmin_cross
        row["binding_directions_at_B_pass"] = [
            {
                "direction": k,
                "half_tangent": str(t),
                "charge": str(knowledge.minima[t, pass_at][0]),
                "witness": [str(w) for w in knowledge.minima[t, pass_at][1]],
            }
            for k, t in enumerate(half_tangents)
            if knowledge.minima[t, pass_at][0] == least_cross
        ]
        row["rescale_factor"] = str(1 / least_cross)
        row["rescaled_total_budget"] = fraction_field(certificate.total_budget / least_cross)
        row["condition_4_coarse_holds"] = pass_at * (1 + gap) < 1
        row["condition_4_sharp_holds"] = sharp_containment(pass_at, gap)
        row["dilation_supremum_at_B_pass"] = surd_field(
            dilation_supremum(certificate.outer_side, pass_at, gap)
        )
    for label, side in (("own", own), ("sharp", sharp)):
        row[f"dilation_supremum_at_B_{label}"] = surd_field(
            dilation_supremum(certificate.outer_side, side, gap)
        )
    row["seconds"] = round(time.monotonic() - started, 1)
    return row


def run(
    certificate: ThresholdCertificate,
    record: dict[str, Any],
    nets: tuple[int, ...],
    work: Path,
    *,
    workers: int,
    resolution: Fraction,
) -> None:
    """Every net in turn, writing each summary and each candidate record as it lands."""

    threshold = certificate.total_budget / certificate.n
    knowledge = Knowledge(threshold)
    limit = Fraction(str(record["angle_limit"]))
    base = int(str(record["direction_steps"]))
    print(f"threshold M/n = {threshold} = {float(threshold):.12f}", flush=True)

    base_least, base_argmin, _ = full_sweep(
        certificate,
        uniform_net(limit, base),
        certificate.square_side,
        knowledge=knowledge,
        work=work,
        steps=base,
        workers=workers,
    )
    (work / f"summary-N{base}.json").write_text(
        json.dumps(
            {
                "K": base,
                "control": True,
                "B_own": str(certificate.square_side),
                "least_at_B_own": fraction_field(base_least),
                "argmin_at_B_own": base_argmin,
                "threshold_M_over_n": str(threshold),
                "passes_at_B_own": base_least > threshold,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        f"K={base:5d}  control: least={float(base_least):.9f} at direction {base_argmin}",
        flush=True,
    )

    bracket = certificate.square_side
    for steps in nets:
        row = measure_net(
            certificate,
            record,
            steps=steps,
            knowledge=knowledge,
            work=work,
            lower_bracket=bracket,
            workers=workers,
            resolution=resolution,
        )
        (work / f"summary-N{steps}.json").write_text(
            json.dumps(row, indent=2) + "\n", encoding="utf-8"
        )
        crossing_row: dict[str, Any] = row["crossing"]
        bracket = max(bracket, Fraction(str(crossing_row["B_fail"])))
        passing = crossing_row["B_pass"]
        if passing is not None:
            side = Fraction(str(passing))
            least = Fraction(str(row["least_at_B_pass"]["exact"]))
            out = work / (
                f"threshold-certificate-{certificate.outer_side.numerator}-"
                f"{certificate.outer_side.denominator}-net{steps}.json"
            )
            out.write_text(
                json.dumps(rescaled_record(record, steps, side, 1 / least), indent=1) + "\n",
                encoding="utf-8",
            )
            print(f"  wrote {out}", flush=True)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--nets", type=int, nargs="+", default=list(DEFAULT_NETS))
    parser.add_argument("--workers", type=int, default=int(os.environ.get("PACK_JOBS", "1")))
    parser.add_argument("--resolution", type=Fraction, default=Fraction(1, 10**7))
    args = parser.parse_args(argv)

    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=True)
    certificate, record = load(args.certificate.resolve().read_bytes())
    run(
        certificate,
        record,
        tuple(args.nets),
        work,
        workers=max(1, args.workers),
        resolution=args.resolution,
    )
    return 0


__all__ = [
    "Knowledge",
    "at",
    "crossing",
    "decimal_places",
    "dilation_supremum",
    "full_sweep",
    "measure_net",
    "rescaled_record",
    "sweep",
]

if __name__ == "__main__":
    raise SystemExit(main())
