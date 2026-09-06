"""Replay a smaller core on frozen atoms, normalize its mass, and emit a candidate.

The decision is m(b) > M/n, not m(b) >= 1. A passing in-memory sweep constructs
fresh candidate bytes; the ordinary production and standalone verifiers must still
decide those bytes before the candidate can be retained as a mathematical result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import time
from dataclasses import replace
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path

from strif import atomic_output_file

from devtools.decide_certificate import load_frozen_bytes, read_bounded
from sqpack.fractional.certificate import (
    Certificate,
    closed_form_conditions,
    sweep_direction_minimum,
    verify,
)

REPO = Path(__file__).resolve().parents[2]


def _witness_details(
    certificate: Certificate, direction_index: int, center_uv: tuple[Fraction, Fraction]
) -> dict[str, object]:
    direction = certificate.directions[direction_index]
    u, v = center_uv
    cosine, sine = direction.ux, direction.uy
    x, y = cosine * u - sine * v, sine * u + cosine * v
    events: dict[Fraction, Fraction] = {}
    for atom in certificate.atoms:
        inclusion = 2 * max(
            abs(cosine * atom.x + sine * atom.y - u),
            abs(-sine * atom.x + cosine * atom.y - v),
        )
        events[inclusion] = events.get(inclusion, Fraction(0)) + atom.weight
    mass = sum(
        (weight for side, weight in events.items() if side <= certificate.square_side),
        start=Fraction(0),
    )
    admissible_up_to = 2 * min(x, y, certificate.outer_side - x, certificate.outer_side - y)
    admissible_up_to /= cosine + sine
    return {
        "witness_center_uv": [str(u), str(v)],
        "witness_center_xy": [str(x), str(y)],
        "witness_closed_mass": str(mass),
        "witness_admissible_up_to_side": str(admissible_up_to),
        "witness_inclusion_events": [
            {"side": str(side), "added_mass": str(weight)}
            for side, weight in sorted(events.items())
        ],
    }


def evaluate(
    source: bytes, *, square_side: Fraction, factor: Fraction, workers: int = 1
) -> tuple[dict[str, object], dict[str, object] | None]:
    """Decide a fixed core shrink; the exact bytes hashed are the bytes parsed.

    Replays the source and candidate rather than accepting a detached Verdict.
    The returned candidate has not crossed the file-based retention boundary.
    """
    certificate, record = load_frozen_bytes(source)
    if not 0 < square_side < certificate.square_side:
        raise ValueError("the new core side must be positive and strictly smaller")
    if not 0 < Fraction(str(record["angle_limit"])) < 1:
        raise ValueError("the source net must satisfy 0 < angle_limit < 1")
    gap = certificate.largest_half_gap_tangent
    containment_slack = 1 - factor * square_side * (1 + gap)
    if factor <= 0 or containment_slack <= 0:
        raise ValueError("the proposed dilation fails strict ordinary containment")
    old_limit_squared = certificate.outer_side**2 * (1 + gap**2)
    old_limit_squared /= certificate.square_side**2 * (1 + gap) ** 2
    new_side = factor * certificate.outer_side
    gain_squared = new_side**2 - old_limit_squared
    if gain_squared <= 0:
        raise ValueError("the proposed side does not exceed the source refined limit")
    started = time.perf_counter()
    baseline = verify(certificate, workers=workers)
    source_seconds = time.perf_counter() - started
    if not baseline.accepted or baseline.minimum_cell_mass is None:
        raise ValueError(f"the source replay failed: {baseline.failures}")
    if Fraction(str(record["total_mass"])) != baseline.total_mass or (
        "least_cell_mass" in record
        and Fraction(str(record["least_cell_mass"])) != baseline.minimum_cell_mass
    ):
        raise ValueError("a source declaration disagrees with its exact replay")
    smaller = replace(certificate, square_side=square_side)
    candidate_started = time.perf_counter()
    verdict = verify(smaller, workers=workers)
    if verdict.minimum_cell_mass is None or verdict.worst_direction is None:
        raise ValueError("the candidate replay decided no covered mass")
    minimum = verdict.minimum_cell_mass
    direction_index = int(verdict.worst_direction)
    repeated, center = sweep_direction_minimum(smaller, smaller.directions[direction_index])
    witness = _witness_details(smaller, direction_index, center)
    if repeated != minimum or Fraction(str(witness["witness_closed_mass"])) != minimum:
        raise ValueError("the candidate witness disagrees with its minimum")
    if square_side > Fraction(str(witness["witness_admissible_up_to_side"])):
        raise ValueError("the candidate witness is outside its admissible center domain")
    threshold = certificate.total_mass / certificate.n
    result: dict[str, object] = {
        "source_sha256": hashlib.sha256(source).hexdigest(),
        "source_id": record["id"],
        "n": certificate.n,
        "outer_side": str(certificate.outer_side),
        "source_core_side": str(certificate.square_side),
        "source_minimum_mass": str(baseline.minimum_cell_mass),
        "total_mass": str(certificate.total_mass),
        "core_side": str(square_side),
        "factor": str(factor),
        "threshold_mass": str(threshold),
        "minimum_mass": str(minimum),
        "criterion_slack": str(minimum - threshold),
        "worst_direction": verdict.worst_direction,
        "direction_count": len(smaller.directions),
        "ordinary_containment_slack": str(containment_slack),
        "proposed_side": str(new_side),
        "source_refined_limit_squared": str(old_limit_squared),
        "squared_bound_gain": str(gain_squared),
        "source_replay_seconds": source_seconds,
        "candidate_replay_seconds": time.perf_counter() - candidate_started,
        "outcome": "criterion_missed",
        "retention_status": "no candidate",
        **witness,
    }
    if minimum <= threshold:
        return result, None
    transformed = replace(
        smaller,
        outer_side=new_side,
        square_side=factor * square_side,
        atoms=tuple(
            replace(atom, x=factor * atom.x, y=factor * atom.y, weight=atom.weight / minimum)
            for atom in smaller.atoms
        ),
    )
    if not all(condition.holds for condition in closed_form_conditions(transformed)):
        raise ValueError("the transformed candidate failed a closed-form condition")
    candidate = {
        **record,
        "id": f"{record['id']}-core-shrink-{new_side}",
        "claim": f"s({certificate.n}) >= {new_side}",
        "outer_side": str(transformed.outer_side),
        "square_side": str(transformed.square_side),
        "total_mass": str(transformed.total_mass),
        "least_cell_mass": "1",
        "atoms": [[str(atom.x), str(atom.y), str(atom.weight)] for atom in transformed.atoms],
    }
    result["outcome"] = "candidate_constructed"
    result["retention_status"] = "requires production and standalone decisions"
    result["normalized_total_mass"] = str(transformed.total_mass)
    return result, candidate


def publish(
    destination: Path, result: dict[str, object], candidate: dict[str, object] | None
) -> None:
    """Reserve a new directory; atomically publish the receipt after the candidate.

    An existing directory is refused. Interruption can leave that reserved directory
    without a receipt, but cannot present a partial receipt or replace an old result.
    """
    destination.mkdir(parents=True, exist_ok=False)
    if candidate is not None:
        encoded = json.dumps(candidate, indent=1) + "\n"
        result = {**result, "candidate_sha256": hashlib.sha256(encoded.encode()).hexdigest()}
        with atomic_output_file(destination / "candidate.json") as temporary:
            temporary.write_text(encoded)
    with atomic_output_file(destination / "result.json") as temporary:
        temporary.write_text(json.dumps(result, indent=2) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--square-side", type=Fraction, required=True)
    parser.add_argument("--factor", type=Fraction, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=1)
    args = parser.parse_args(argv)
    if args.output_dir.exists():
        parser.error("the output directory must be fresh")
    source = read_bounded(args.source)
    provenance = {
        "started_utc": datetime.now(UTC).isoformat(),
        "command": sys.argv if argv is None else ["core_shrink", *argv],
        "source_path": args.source.resolve().relative_to(REPO).as_posix(),
        "git_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO, text=True
        ).strip(),
        "git_dirty": bool(
            subprocess.check_output(
                ["git", "status", "--porcelain"], cwd=REPO, text=True
            ).strip()
        ),
        "tool_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "workers_requested": args.workers,
    }
    print(f"Exact source and core-side {args.square_side} replays starting", flush=True)
    result, candidate = evaluate(
        source, square_side=args.square_side, factor=args.factor, workers=args.workers
    )
    result.update(provenance)
    result["finished_utc"] = datetime.now(UTC).isoformat()
    publish(args.output_dir, result, candidate)
    print(
        f"{result['outcome']}: m = {result['minimum_mass']}, "
        f"required > {result['threshold_mass']}; {result['retention_status']}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
