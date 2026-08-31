#!/usr/bin/env python3
"""Price X-003's chunk-level stage-1 label space before building the enumerator.

`BC-095` (agenda-010): the queue stopped `BC-092` on a figure that priced the wrong
object at the wrong route (D-405). This tool prices the object X-003 actually
proposed -- stratum labels over *chunks*, not squares -- at `n = 11` in counted LP
solves (D-126), with every factor labeled by its evidential standing:

- **counted**: exact combinatorics computed here (partitions, skeletons, angle-class
  assignments, pair contact states, wall subsets, and the per-partition symmetry
  group order for the orbit interval);
- **measured**: the local-realizability prefilter rate and per-candidate cost, run
  here on a declared sample of the size-five isomorph-free scaffold stream, beside
  the retained n = 4 exhaustive rate (26 of 124) from
  `atlas/known-best/contact-enumeration-pricing.json`;
- **assumed**: the transfer of that square-level prefilter rate to chunk-level
  strata, which nothing has measured -- named here so the go/no-go carries it
  explicitly instead of silently (the D-405 lesson, applied to ourselves).

The orbit count is reported as an interval: Burnside gives `orbits >= raw / |G|`
per stratum family, so the optimistic end divides by the full group (D4 times the
permutations of interchangeable chunks) and the pessimistic end is the raw count.
An exact orbit count is the enumerator's own job; pricing does not pretend to it.

Usage, from `packing/`:
    uv run --frozen python -m devtools.price_stage1_chunks [--sample-size N]
"""

from __future__ import annotations

import argparse
import math
import time
from fractions import Fraction
from itertools import islice

from sqpack.contact_assembly import enumerate_isomorph_free_scaffolds
from sqpack.contact_realization import realize_local_contact_scaffolds

N_SQUARES = 11
MAX_CHUNKS = 6
MAX_TILTED = 2
PAIR_STATES = 5  # absent, or one signed u/v normal, the scaffold grammar's pair states
WALL_SUBSETS = 16  # subsets of the four container walls per chunk
#: The retained T-2 measurement: one fixed-angle cell LP solve at n = 11.
LP_SECONDS = 0.00128
#: X-003's ranking rule: every surviving stratum gets a coarse angle sweep of this
#: many LP solves per tilted-class dimension before any triage.
SWEEP_SOLVES_PER_TILTED_DIM = 100
RETAINED_N4_FEASIBLE = (26, 124)


def partitions(total: int, largest: int, parts: int) -> list[tuple[int, ...]]:
    """Nonincreasing partitions of `total` into at most `parts` parts."""
    if total == 0:
        return [()]
    if parts == 0:
        return []
    return [
        (head, *tail)
        for head in range(min(total, largest), 0, -1)
        for tail in partitions(total - head, head, parts - 1)
    ]


def skeleton_count(size: int) -> int:
    """Distinct bar/rectangle/L lattice skeletons with `size` cells."""
    rectangles = sum(1 for a in range(1, size + 1) if size % a == 0 and a * a <= size)
    arms = 0
    if size >= 3:
        # L with arms a, b >= 2, a + b - 1 = size, unordered.
        arms = sum(1 for a in range(2, size) if (b := size + 1 - a) >= a and b >= 2)
    return rectangles + arms


def class_assignments(chunks: int) -> int:
    """Assignments of chunks to {frame, tilt-1, tilt-2}, at most MAX_TILTED tilted,
    counted up to swapping the two tilt-class names."""
    seen: set[tuple[int, ...]] = set()
    for encoded in range(3**chunks):
        digits = []
        remainder = encoded
        for _ in range(chunks):
            digits.append(remainder % 3)
            remainder //= 3
        if sum(1 for digit in digits if digit) > MAX_TILTED:
            continue
        swapped = tuple({0: 0, 1: 2, 2: 1}[digit] for digit in digits)
        seen.add(min(tuple(digits), swapped))
    return len(seen)


def priced_families(max_chunks: int, wall_subsets: int) -> tuple[int, Fraction, int]:
    """(raw label count, optimistic orbit floor, family count) over all partitions."""
    raw_total = 0
    floor_total = Fraction(0)
    families = 0
    for partition in partitions(N_SQUARES, N_SQUARES, max_chunks):
        chunks = len(partition)
        skeletons = math.prod(skeleton_count(size) for size in partition)
        labels = (
            skeletons
            * class_assignments(chunks)
            * PAIR_STATES ** math.comb(chunks, 2)
            * wall_subsets**chunks
        )
        counts = {size: partition.count(size) for size in partition}
        multiplicity = math.prod(math.factorial(count) for count in counts.values())
        raw_total += labels
        floor_total += Fraction(labels, 8 * multiplicity)
        families += 1
    return raw_total, floor_total, families


def measure_prefilter(sample_size: int) -> tuple[int, int, float]:
    """(feasible, solved, seconds per candidate) on the first `sample_size` size-5
    isomorph-free scaffolds, in their deterministic canonical order."""
    proposals = enumerate_isomorph_free_scaffolds(
        5, maximum_colorings=2_000_000, maximum_emitted_scaffolds=100_000
    )
    if proposals.status != "completed":
        raise RuntimeError(f"scaffold proposals hit {proposals.limit_kind}")
    sample = list(islice(proposals.scaffolds, sample_size))
    started = time.monotonic()
    batch = realize_local_contact_scaffolds(
        sample, minimum_overlap=0.25, maximum_lp_solves=sample_size
    )
    elapsed = time.monotonic() - started
    feasible = sum(1 for r in batch.receipts if r.outcome == "locally-feasible")
    return feasible, len(batch.receipts), elapsed / max(1, len(batch.receipts))


def main() -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--sample-size", type=int, default=300)
    arguments = parser.parse_args()

    raw, floor, families = priced_families(MAX_CHUNKS, WALL_SUBSETS)
    feasible, solved, per_candidate = measure_prefilter(arguments.sample_size)
    rate = feasible / solved if solved else 0.0
    n4_rate = RETAINED_N4_FEASIBLE[0] / RETAINED_N4_FEASIBLE[1]

    print(f"chunk-level stage-1 label space at n = {N_SQUARES}, K <= {MAX_CHUNKS}")
    print(f"{'factor':<46} {'value':>18}  standing")
    rows = [
        ("partition families (parts, unordered)", f"{families:,}", "counted"),
        ("raw stratum labels (pessimistic orbits)", f"{raw:,}", "counted"),
        ("orbit floor via Burnside, D4 x chunk perms", f"{float(floor):,.3e}", "counted bound"),
        (
            f"prefilter rate, size-5 sample of {solved}",
            f"{rate:.3f}",
            "measured here",
        ),
        ("prefilter rate, retained n = 4 exhaustive", f"{n4_rate:.3f}", "retained"),
        ("prefilter seconds per candidate", f"{per_candidate:.4f}", "measured here"),
        ("square-to-chunk rate transfer", "unmeasured", "ASSUMED"),
    ]
    for name, value, standing in rows:
        print(f"{name:<46} {value:>18}  {standing}")

    for label, strata in (("floor", float(floor)), ("ceiling", float(raw))):
        surviving = strata * rate
        solves = surviving * (1 + MAX_TILTED * SWEEP_SOLVES_PER_TILTED_DIM)
        hours = solves * LP_SECONDS / 3600
        print(
            f"{label}: {strata:,.3e} strata -> {surviving:,.3e} surviving at the "
            f"measured rate -> {solves:,.3e} LP solves "
            f"(~{hours:,.1f} h at the retained {LP_SECONDS * 1000:.2f} ms/solve)"
        )
    print()
    print("restricted slices (walls: 6 = X-008's measured seatings -- none, one of")
    print("four corner pairs, all four; 16 = free), same counted method:")
    print(f"{'slice':<34} {'raw labels':>16} {'orbit floor':>14} {'floor LP solves':>16}")
    for chunk_cap in (3, 4, 5, 6):
        for walls in (6, 16):
            sliced_raw, sliced_floor, _ = priced_families(chunk_cap, walls)
            solves = float(sliced_floor) * rate * (1 + MAX_TILTED * SWEEP_SOLVES_PER_TILTED_DIM)
            print(
                f"K <= {chunk_cap}, walls {walls:>2}{'':<18} {sliced_raw:>16,} "
                f"{float(sliced_floor):>14,.3e} {solves:>16,.3e}"
            )
    print()
    print(
        "go/no-go input, not a verdict: the interval spans the unknown exact orbit "
        "count, the rate transfer is assumed, and the omission control the enumerator "
        "must ship is the counted raw total above -- its emitted count per partition "
        "family must equal these closed forms exactly, with Trump's stratum as the "
        "known-answer inclusion."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
