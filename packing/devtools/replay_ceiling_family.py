"""Replay a retained depth-scaled family from its bytes through the ceiling verifier.

A cutting run retains its best family as a record ``CeilingCertificate.from_record``
reads: ``--freeze`` writes one, and a state file carries one under ``best_family``.
The floor the run reported, total weight over exact maximum depth, is only as good
as the depth the separation screen found at the time, and D-476 and D-477 are two
ways that screen was wrong. This command re-decides the depth from the bytes on disk
with the final verifier, whose vertices are enumerated independently of the search,
and prints what it found beside what the record says.

Run from ``packing/``, with ``uv run --frozen --all-extras --group dev`` in front::

    python -m devtools.replay_ceiling_family FAMILY.json
    python -m devtools.replay_ceiling_family --check FAMILY.json STATE.json

``--check`` fails unless the replay reproduces the record: a frozen family's own
``provenance.verify_ceiling`` vertex count and maximum depth, or a state file's
``best_scaled_total``. A retained floor is then confirmed by a command rather than
by reading a log. A large family takes minutes: the retained n=11 families have
about 2.5 million vertices each.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from sqpack.fractional.ceiling import CeilingCertificate, CeilingVerdict, verify_ceiling


@dataclass(frozen=True)
class Expectation:
    """What the record itself says the replay should reproduce."""

    vertices: int | None = None
    max_depth: Fraction | None = None
    scaled_total: Fraction | None = None

    @property
    def empty(self) -> bool:
        return self.vertices is None and self.max_depth is None and self.scaled_total is None


def load_family(path: Path) -> tuple[CeilingCertificate, Expectation]:
    """The family a frozen record or a state file carries, and what it claims."""
    data = json.loads(path.read_text())
    if "best_family" in data:
        record = data["best_family"]
        total = data.get("best_scaled_total")
        expectation = Expectation(scaled_total=None if total is None else _rational(total))
    else:
        record = data
        recorded = data.get("provenance", {}).get("verify_ceiling", {})
        expectation = Expectation(
            vertices=None if "vertices" not in recorded else int(recorded["vertices"]),
            max_depth=None if "max_depth" not in recorded else _rational(recorded["max_depth"]),
        )
    return CeilingCertificate.from_record(record), expectation


def _rational(value: Any) -> Fraction:
    """A recorded number, exact when the record wrote a rational or a decimal string."""
    if isinstance(value, float):
        return Fraction(repr(value))
    return Fraction(str(value))


def scaled_total(verdict: CeilingVerdict) -> Fraction:
    """The floor the family certifies: its total once scaled to unit depth."""
    if verdict.max_depth <= 1:
        return verdict.total_weight
    return verdict.total_weight / verdict.max_depth


def compare(verdict: CeilingVerdict, expectation: Expectation) -> list[str]:
    """Every way the replay disagrees with what the record claims."""
    found = {
        "vertices": (verdict.vertices, expectation.vertices),
        "max_depth": (verdict.max_depth, expectation.max_depth),
        "scaled_total": (scaled_total(verdict), expectation.scaled_total),
    }
    return [
        f"{name}: replayed {replayed}, recorded {recorded}"
        for name, (replayed, recorded) in found.items()
        if recorded is not None and replayed != recorded
    ]


def report(
    path: Path,
    certificate: CeilingCertificate,
    verdict: CeilingVerdict,
    expectation: Expectation,
    seconds: float,
) -> dict[str, Any]:
    """One JSON line: what the replay found beside what the record claims."""
    return {
        "path": str(path),
        "placements": len(certificate.placements),
        "total_weight": str(verdict.total_weight),
        "total_weight_float": float(verdict.total_weight),
        "vertices": verdict.vertices,
        "decided_exactly": verdict.decided_exactly,
        "max_depth": str(verdict.max_depth),
        "max_depth_float": float(verdict.max_depth),
        "scaled_total": str(scaled_total(verdict)),
        "scaled_total_float": float(scaled_total(verdict)),
        "proved": verdict.proved,
        "failures": list(verdict.failures),
        "recorded": {
            "vertices": expectation.vertices,
            "max_depth": None if expectation.max_depth is None else str(expectation.max_depth),
            "scaled_total": (
                None if expectation.scaled_total is None else str(expectation.scaled_total)
            ),
        },
        "seconds": round(seconds, 1),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail unless the replay reproduces what each record claims",
    )
    arguments = parser.parse_args(argv)
    failed = False
    for path in arguments.paths:
        certificate, expectation = load_family(path)
        started = time.perf_counter()
        verdict = verify_ceiling(certificate)
        line = report(path, certificate, verdict, expectation, time.perf_counter() - started)
        if arguments.check:
            problems = compare(verdict, expectation)
            if expectation.empty:
                problems.append("the record carries nothing to check against")
            line["check"] = problems or "reproduced"
            failed = failed or bool(problems)
        print(json.dumps(line))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
