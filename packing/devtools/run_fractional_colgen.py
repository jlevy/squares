"""Run the dual-driven column generator at one setting and record what it cost.

The generator is a library call with a dozen parameters, and every run of it
in the record so far was made from a one-off script that was not kept. The
covering-values register carries the consequence in plain words: for the
`n = 12` rung at `99/25`, "the record names no site set and retains no site,
row or round count". This module is the driver, so the next run is a command
with its parameters on the line and a per-round table on its stdout.

It only drives. `generate_adaptive` makes every search decision, the
rationaliser makes the candidate, and nothing here decides a bound: freezing
is the last thing it does, and `devtools.decide_certificate` is what turns a
frozen candidate into a retained one.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from sqpack.fractional.certificate import Certificate, verify
from sqpack.fractional.colgen import AdaptiveLog, generate_adaptive, site_counts_for_side

# The net every retained fractional certificate carries, and the shrink they
# are all built at. Defaults rather than constants: a run that changes them is
# a different instrument and has to say so on the command line.
ANGLE_LIMIT = Fraction(207107, 500000)
DIRECTION_STEPS = 180
SHRINK = Fraction(9977, 10000)
SCALE = 200_000


@dataclass(frozen=True, slots=True)
class RunSettings:
    """Everything the run is, in the units the record quotes."""

    n: int
    outer_side: Fraction
    square_side: Fraction
    grid_counts: tuple[int, ...]
    inset: Fraction
    angle_limit: Fraction
    direction_steps: int
    scale: int
    column_rounds: int
    max_rounds: int
    rows_per_direction: int

    def as_dict(self) -> dict[str, object]:
        return {
            "n": self.n,
            "outer_side": str(self.outer_side),
            "square_side": str(self.square_side),
            "grid_counts": list(self.grid_counts),
            "inset": str(self.inset),
            "angle_limit": str(self.angle_limit),
            "direction_steps": self.direction_steps,
            "scale": self.scale,
            "column_rounds": self.column_rounds,
            "max_rounds": self.max_rounds,
            "rows_per_direction": self.rows_per_direction,
        }


def summary(
    settings: RunSettings,
    log: AdaptiveLog,
    candidate: Certificate | None,
    seconds: float,
    frozen: Path | None,
) -> dict[str, object]:
    return {
        "settings": settings.as_dict(),
        "seconds": seconds,
        "stopped": log.stopped,
        "converged": log.stopped.startswith("converged"),
        "objective": log.objective,
        "least_covered": log.least_covered,
        "rounds": [
            {
                "index": entry.index,
                "rows": entry.rows,
                "orbits": entry.orbits,
                "sites": entry.sites,
                "lp_rounds": entry.lp_rounds,
                "objective": entry.objective,
                "least_covered": entry.least_covered,
                "averaged_depth": entry.averaged_depth,
                "reduced_cost": entry.cost,
                "added": entry.added,
                "seconds": entry.seconds,
                "note": entry.note,
            }
            for entry in log.rounds
        ],
        "total_mass": str(log.total_mass) if log.total_mass is not None else None,
        "total_mass_float": float(log.total_mass) if log.total_mass is not None else None,
        "atoms": len(candidate.atoms) if candidate is not None else 0,
        "ceiling_proved": None if log.ceiling is None else log.ceiling.proved,
        "ceiling_detail": None if log.ceiling is None else log.ceiling.detail,
        "frozen": str(frozen) if frozen is not None else None,
    }


def run(
    settings: RunSettings,
    *,
    log_path: Path | None,
    freeze: Path | None,
    verify_serial: bool = False,
) -> dict[str, object]:
    started = time.perf_counter()
    candidate, log = generate_adaptive(
        settings.n,
        settings.outer_side,
        settings.square_side,
        grid_counts=settings.grid_counts,
        inset=settings.inset,
        angle_limit=settings.angle_limit,
        direction_steps=settings.direction_steps,
        scale=settings.scale,
        max_rounds=settings.max_rounds,
        column_rounds=settings.column_rounds,
        rows_per_direction=settings.rows_per_direction,
        log_path=log_path,
        # Never here. The retention boundary is freeze-then-decide, and an
        # in-memory verdict is not evidence about any file (D-433, D-441).
        decide=False,
    )
    seconds = time.perf_counter() - started
    frozen: Path | None = None
    least_cell_mass: str | None = None
    if candidate is not None and freeze is not None:
        if verify_serial:
            # One worker, never the pool: a lane holding one core must not
            # start a parallel sweep, and this only fills the declaration.
            least_cell_mass = str(verify(candidate, workers=1).minimum_cell_mass)
        freeze.parent.mkdir(parents=True, exist_ok=True)
        freeze.write_text(certificate_json(candidate, least_cell_mass))
        frozen = freeze
    result = summary(settings, log, candidate, seconds, frozen)
    result["least_cell_mass"] = least_cell_mass
    return result


def certificate_json(certificate: Certificate, least_cell_mass: str | None) -> str:
    """The retained on-disk shape, which `cases/*/replay.py` reads back.

    ``least_cell_mass`` is a declaration and not a decision: it is left null
    when nothing has computed it, so a frozen candidate never carries a number
    no run produced. `devtools.decide_certificate` is what decides the bytes.
    """

    record: dict[str, object] = {
        "id": f"C-n{certificate.n:03d}-fractional-"
        f"{certificate.outer_side.numerator}-{certificate.outer_side.denominator}",
        "n": certificate.n,
        "claim": f"s({certificate.n}) >= {certificate.bounded_side}",
        "outer_side": str(certificate.outer_side),
        "square_side": str(certificate.square_side),
        "angle_limit": str(certificate.half_tangents[-1]),
        "direction_steps": len(certificate.half_tangents) - 1,
        "total_mass": str(certificate.total_mass),
        "least_cell_mass": least_cell_mass,
        "symmetry": certificate.symmetry,
        "atoms": [[str(atom.x), str(atom.y), str(atom.weight)] for atom in certificate.atoms],
    }
    return json.dumps(record, indent=1) + "\n"


def counts_for(text: str, outer_side: Fraction, square_side: Fraction) -> tuple[int, ...]:
    """``auto`` holds BC-191's site density; anything else is an explicit tuple."""

    if text == "auto":
        return site_counts_for_side(outer_side, square_side)
    return tuple(int(part) for part in text.split(",") if part)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--side", type=Fraction, required=True, help="container side L")
    parser.add_argument("--shrink", type=Fraction, default=SHRINK, help="square side B")
    parser.add_argument(
        "--grid-counts",
        default="auto",
        help="comma-separated seed grid counts, or 'auto' for BC-191's site density",
    )
    parser.add_argument("--inset", type=Fraction, default=Fraction(1, 2))
    parser.add_argument("--angle-limit", type=Fraction, default=ANGLE_LIMIT)
    parser.add_argument("--direction-steps", type=int, default=DIRECTION_STEPS)
    parser.add_argument("--scale", type=int, default=SCALE)
    parser.add_argument("--column-rounds", type=int, default=8)
    parser.add_argument("--max-rounds", type=int, default=60)
    parser.add_argument("--rows-per-direction", type=int, default=3)
    parser.add_argument("--log", type=Path, default=None, help="append the round lines here")
    parser.add_argument("--freeze", type=Path, default=None, help="write the candidate here")
    parser.add_argument("--json", type=Path, default=None, help="write the run summary here")
    parser.add_argument(
        "--verify-serial",
        action="store_true",
        help="fill least_cell_mass with a one-worker sweep before freezing",
    )
    args = parser.parse_args(argv)

    settings = RunSettings(
        n=args.n,
        outer_side=args.side,
        square_side=args.shrink,
        grid_counts=counts_for(args.grid_counts, args.side, args.shrink),
        inset=args.inset,
        angle_limit=args.angle_limit,
        direction_steps=args.direction_steps,
        scale=args.scale,
        column_rounds=args.column_rounds,
        max_rounds=args.max_rounds,
        rows_per_direction=args.rows_per_direction,
    )
    print(json.dumps(settings.as_dict(), indent=1), flush=True)
    result = run(
        settings,
        log_path=args.log,
        freeze=args.freeze,
        verify_serial=args.verify_serial,
    )
    print(round_table_from(result), flush=True)
    print(
        f"stopped: {result['stopped']}\n"
        f"objective: {result['objective']}\n"
        f"least covered mass: {result['least_covered']}\n"
        f"total mass: {result['total_mass']} = {result['total_mass_float']}\n"
        f"least cell mass: {result.get('least_cell_mass')}\n"
        f"atoms: {result['atoms']}\n"
        f"frozen: {result['frozen']}\n"
        f"seconds: {result['seconds']:.1f}",
        flush=True,
    )
    if args.json is not None:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(result, indent=1) + "\n")
    return 0


def round_table_from(result: dict[str, object]) -> str:
    """The same table as `round_table`, from the summary a run returns."""

    header = (
        f"{'round':>5} {'rows':>7} {'orbits':>7} {'sites':>7} {'lp_rounds':>9} "
        f"{'objective':>13} {'least_covered':>13} {'depth':>10} {'seconds':>9}  note"
    )
    lines = [header, "-" * len(header)]
    rounds = result["rounds"]
    assert isinstance(rounds, list)
    lines.extend(
        f"{entry['index']:>5} {entry['rows']:>7} {entry['orbits']:>7} "
        f"{entry['sites']:>7} {entry['lp_rounds']:>9} {entry['objective']:>13.6f} "
        f"{entry['least_covered']:>13.6f} {entry['averaged_depth']:>10.6f} "
        f"{entry['seconds']:>9.1f}  {entry['note']}"
        for entry in rounds
    )
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
