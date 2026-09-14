"""Measure bounded threshold expansion without relaxing its production resource caps.

Run from packing/: ``uv run --frozen python -m devtools.measure_threshold_expansion``.
Use ``--tokens 64 --threshold 62 --atoms 125`` for a near-cap aggregate fixture.
Each atom has one coincident token site, so every subset survives intersection. Timings
describe this fixture, not a bound on arbitrary exact-coordinate arithmetic or grids.
Run each measurement in a fresh process if comparing process peak RSS.
"""

from __future__ import annotations

import argparse
import json
import platform
import resource
import sys
import time
from fractions import Fraction
from math import comb

from sqpack.fractional.model import rotation_from_half_tangent
from sqpack.fractional.threshold import (
    MAX_EXPANSION_SUBSETS,
    ThresholdAtom,
    preflight_expansion,
    rectangle_terms,
)


def measure(tokens: int, threshold: int, atoms: int) -> dict[str, object]:
    """Return fixture counts and measured costs, refusing before any token expansion."""
    # Every nonzero atom emits at least one subset. Bound the fixture tuple itself before
    # constructing it, then let the same guard as production bound its combinatorial work.
    if not 1 <= atoms <= MAX_EXPANSION_SUBSETS:
        raise ValueError(f"atoms must be in 1..{MAX_EXPANSION_SUBSETS}")
    atom = ThresholdAtom(((Fraction(3, 2), Fraction(3, 2)),), threshold, Fraction(1), (tokens,))
    family = (atom,) * atoms
    started = time.perf_counter()
    subsets = preflight_expansion(family)
    preflight_seconds = time.perf_counter() - started
    token_slots = atoms * sum(j * comb(tokens, j) for j in range(threshold, tokens + 1))
    started = time.perf_counter()
    terms = rectangle_terms(
        (),
        family,
        rotation_from_half_tangent("0", Fraction(0)),
        Fraction(3),
        Fraction(9, 10),
        scale=1,
    )
    elapsed = time.perf_counter() - started
    peak_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return {
        "tokens_per_atom": tokens,
        "threshold": threshold,
        "atoms": atoms,
        "subsets": subsets,
        "token_slots": token_slots,
        "emitted_terms": int(terms.weight.size),
        "preflight_seconds": preflight_seconds,
        "expansion_seconds": elapsed,
        "process_peak_rss_bytes": peak_rss if sys.platform == "darwin" else peak_rss * 1024,
        "python": platform.python_version(),
        "platform": platform.platform(),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tokens", type=int, default=7)
    parser.add_argument("--threshold", type=int, default=4)
    parser.add_argument("--atoms", type=int, default=1)
    args = parser.parse_args(argv)
    try:
        result = measure(args.tokens, args.threshold, args.atoms)
    except (TypeError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
