#!/usr/bin/env python3
"""Replay the exact grid witnesses and basic bound instantiations in the frontier.

The grid replay is a machine check of a finite rational witness.  The lower-bound
checks only confirm that each case instantiates the exact expression named by its
evidence record; the mathematical force of Nagamochi's inequality still comes from the
scoped published proof recorded in ``frontier/evidence.yaml``.

The two halves run in different validation steps, on purpose.  ``check_case_basic_bounds``
compares declared expressions against their closed forms and costs nothing, so it stays
where the frontier records are read.  ``replay_grid_witness`` evaluates exact rational
predicates and belongs with the other exact geometry; running it inside a step called
``soft-schema validation`` is what made that step slow and what kept anyone from looking
(``D-370``).  Running this module directly does both, which is what the
``exact verification`` step invokes.

The replay half then split again on 2026-09-07, and by the same kind of measurement.  At
``n=1..324`` it was 34.81s of an 84.21s step in a ``checks`` job that had just run
189.09s against a 195s ceiling, so ``exact verification`` runs it with ``--sample`` and
``exact rational grid replay`` runs it whole on the deferred surface.  The bound
comparisons are not sampled: every case still has its declared bounds checked against
their closed forms, which is 0.14s of the whole run.
``benchmarks/gate-cost-at-324/`` retains the readings.

Usage:
    uv run --frozen python -m devtools.check_basic_bounds
    uv run --frozen python -m devtools.check_basic_bounds --sample
    uv run --frozen python -m devtools.check_basic_bounds --jobs 4
    uv run --frozen python -m devtools.check_basic_bounds --max-n 100
"""

from __future__ import annotations

import argparse
import math
from collections.abc import Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
from pathlib import Path

from sqpack.known_best import GRID_SAMPLE_STRIDE, sampled_sequence
from sqpack.verify import Report, verify_packing
from sqpack.workers import worker_count
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"


def _sign(value: Fraction) -> int:
    return (value > 0) - (value < 0)


def _strings(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _bound(case: Mapping[str, object], name: str) -> Mapping[str, object] | None:
    value = case.get(name)
    return value if isinstance(value, Mapping) else None


def build_grid(n: int) -> tuple[list[list[tuple[Fraction, Fraction]]], Fraction]:
    """Build the row-major rational grid fallback for one positive ``n``."""
    if n < 1:
        raise ValueError("n must be positive")
    root = math.isqrt(n)
    side = root if root * root == n else root + 1
    squares: list[list[tuple[Fraction, Fraction]]] = []
    for index in range(n):
        x = Fraction(index % side)
        y = Fraction(index // side)
        squares.append(
            [
                (x, y),
                (x + 1, y),
                (x + 1, y + 1),
                (x, y + 1),
            ]
        )
    return squares, Fraction(side)


def verify_grid(n: int) -> Report:
    """Verify one grid fallback with exact rational predicate evaluation.

    Bucketed, and the pruning is sound rather than convenient. `verify_packing` first
    establishes that every piece is a unit square, and two unit squares overlap only if
    their centres are within `sqrt(2)` of each other, so a bucket of side 2 with its
    eight neighbours contains every pair that could overlap. Nothing is skipped that a
    full sweep would have judged.

    The sweep it replaces is quadratic in `n` at each of 96 sizes: 166,650 exact pair
    tests to re-establish that unit squares on integer lattice points do not overlap,
    against 57,665 bucketed (D-370).
    """
    squares, side = build_grid(n)
    return verify_packing(squares, side, sign=_sign, bucket=True)


def _nagamochi_form(n: int) -> str:
    side = math.isqrt(n)
    if side * side < n:
        side += 1
    if side * side - n <= 2:
        return str(side)
    return f"sqrt({n} - 2*floor(sqrt({n})) + 1) + 1"


def check_case_basic_bounds(case: Mapping[str, object]) -> list[str]:
    """Check the parametric exact evidence referenced by one case."""
    n = case.get("n")
    if not isinstance(n, int):
        return ["case n is missing or malformed"]
    errors: list[str] = []
    upper = _bound(case, "verified_upper_bound")
    lower = _bound(case, "verified_lower_bound")

    if upper is not None and "E-basic-grid-upper" in _strings(upper.get("evidence")):
        expected = str(math.isqrt(n) if math.isqrt(n) ** 2 == n else math.isqrt(n) + 1)
        if upper.get("exact_form") != expected or upper.get("value") != expected:
            errors.append(
                f"n={n}: grid upper bound must have exact value {expected}, "
                f"got {upper.get('exact_form')!r}"
            )

    if lower is not None and "E-basic-area-lower" in _strings(lower.get("evidence")):
        expected = "1" if n == 1 else f"sqrt({n})"
        if lower.get("exact_form") != expected:
            errors.append(
                f"n={n}: area lower bound must have exact form {expected}, "
                f"got {lower.get('exact_form')!r}"
            )

    if lower is not None and "E-nagamochi-lower" in _strings(lower.get("evidence")):
        expected = _nagamochi_form(n)
        if lower.get("exact_form") != expected:
            errors.append(
                f"n={n}: Nagamochi bound must have exact form {expected}, "
                f"got {lower.get('exact_form')!r}"
            )

    if (
        lower is not None
        and "E-n012-monotonicity-lower" in _strings(lower.get("evidence"))
        and (n != 12 or lower.get("exact_form") != "2 + 4/sqrt(5)")
    ):
        errors.append("E-n012-monotonicity-lower must copy the verified n=11 bound")
    return errors


def claims_grid_witness(case: Mapping[str, object]) -> bool:
    """Whether this case's verified upper bound is the grid ceiling this module replays."""
    upper = _bound(case, "verified_upper_bound")
    return upper is not None and "E-basic-grid-upper" in _strings(upper.get("evidence"))


def replay_number(n: int) -> list[str]:
    """Replay the exact rational grid witness for one `n`, and say what failed.

    Addressed by `n` rather than by a case mapping so that `pool.map` can carry the work
    to a worker: `verify_grid` reads nothing but the size, and an `int` pickles where a
    frontier document's parsed frontmatter is both larger and needless.
    """
    report = verify_grid(n)
    if not report.valid or report.n != n:
        return [f"n={n}: exact grid witness replay failed: {report.failures}"]
    return []


def replay_grid_witness(case: Mapping[str, object]) -> list[str]:
    """Replay the exact rational grid witness for one case, if it claims one.

    Split out of `check_case_basic_bounds` so that exact geometry runs in the step named
    for exact geometry. It used to run inside `soft-schema validation`, where it was
    `3.58s` of the `15.5s` that step cost and where no reader would look for it
    (`D-370`). Nothing about the check changed in the move: the same cases are replayed,
    with the same predicate, to the same verdict.
    """
    n = case.get("n")
    if not isinstance(n, int):
        return ["case n is missing or malformed"]
    if not claims_grid_witness(case):
        return []
    return replay_number(n)


def replay_grid_witnesses(numbers: Sequence[int], workers: int) -> dict[int, list[str]]:
    """Every named grid witness replayed, serially or through a process pool.

    The per-case work is independent -- `verify_grid` builds its own grid from `n` and
    reads nothing else -- and it is the whole of this module's cost: measured on
    2026-09-07 at `n=1..324`, the replay was 34.72s of a 34.86s run, the remaining 0.14s
    being 324 frontmatter loads and the closed-form bound comparisons.

    `workers` is the pool size, and `1` runs in this process rather than through a pool,
    because a one-worker pool is a subprocess and a protocol for no concurrency at all.
    Who chooses the count matters more than the count: `main` asks
    `sqpack.workers.worker_count`, which reads the `PACK_JOBS` cap the gate exports to
    every step -- the same contract `screen_translation_escape`, `build_known_best_atlas`
    and `check_soundness_perimeter` use. The pull-request tiers set that cap to 1, so
    under them this stays exactly as serial as it was until a tier says otherwise.

    Returns the failures keyed by `n` rather than a flat list, so the caller can report
    them in frontier-document order whichever way they were computed. `pool.map` yields
    by submission index rather than by completion, so the mapping is the same object
    either way and a pooled run's output is byte-for-byte the serial run's.
    """
    count = max(1, min(workers, len(numbers)))
    if count == 1:
        replayed = [replay_number(n) for n in numbers]
    else:
        with ProcessPoolExecutor(max_workers=count) as pool:
            replayed = list(pool.map(replay_number, numbers))
    return dict(zip(numbers, replayed, strict=True))


def _load_case(path: Path) -> Mapping[str, object]:
    document = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])
    if not isinstance(document, Mapping) or not isinstance(document.get("packing"), Mapping):
        raise TypeError(f"{path}: malformed frontier frontmatter")
    return document["packing"]


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument(
        "--sample",
        action="store_true",
        help=(
            f"replay every {GRID_SAMPLE_STRIDE}th grid witness rather than all of them, "
            f"which is what the pull-request surface runs"
        ),
    )
    command.add_argument(
        "--max-n",
        type=int,
        metavar="N",
        default=None,
        help=(
            "replay only the grid witnesses at or below N. A diagnostic, not a gate "
            "setting: it is how the cost curve in benchmarks/gate-cost-at-324 was taken"
        ),
    )
    command.add_argument(
        "--jobs",
        type=int,
        metavar="N",
        default=None,
        help=(
            "processes to replay the witnesses with; the default follows the PACK_JOBS "
            "cap the gate exports, and the whole machine when there is no gate"
        ),
    )
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.sample and args.max_n is not None:
        raise SystemExit("--sample and --max-n are two different narrowings; pick one")
    if args.max_n is not None and args.max_n < 1:
        raise SystemExit("--max-n must be positive")
    if args.jobs is not None and args.jobs < 1:
        raise SystemExit("--jobs must be positive")

    paths = sorted(FRONTIER.glob("n-*.md"))
    cases = [(path, _load_case(path)) for path in paths]
    grid = [
        int(n)
        for _path, case in cases
        if claims_grid_witness(case) and isinstance(n := case.get("n"), int)
    ]
    if args.sample:
        selected = sampled_sequence(grid, GRID_SAMPLE_STRIDE)
        of_total = f" of {len(grid)}"
        narrowing = f" (every {GRID_SAMPLE_STRIDE}th grid case, from the first)"
    elif args.max_n is not None:
        selected = tuple(n for n in grid if n <= args.max_n)
        of_total = f" of {len(grid)}"
        narrowing = f" (n <= {args.max_n})"
    else:
        selected = tuple(grid)
        of_total = ""
        narrowing = ""
    # Resolved here and nowhere else, so an in-process caller of `replay_grid_witnesses`
    # never inherits a count taken from the machine behind the gate's back.
    workers = worker_count(len(selected)) if args.jobs is None else args.jobs

    failures = replay_grid_witnesses(selected, workers)
    errors: list[str] = []
    for path, case in cases:
        errors.extend(f"{path.name}: {error}" for error in check_case_basic_bounds(case))
        n = case.get("n")
        if isinstance(n, int):
            errors.extend(f"{path.name}: {error}" for error in failures.get(n, ()))
    if errors:
        print("\n".join(errors))
        return 1
    print(
        f"replayed {len(selected)}{of_total} exact rational grid witnesses{narrowing} "
        f"and checked basic bound instantiations for {len(paths)} cases"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
