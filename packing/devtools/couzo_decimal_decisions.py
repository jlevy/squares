"""Decide Couzo's 8 October decimal reports at six counts exactly (think-rx26).

Francisco Couzo's report of 8 October 2026 (the ``couzo-extended-reports-2026-10-08``
packet) gives each count a decimal side and, per square, a decimal centre and an angle in
radians, each the rendering of a binary64 value. His exact certificates of 9 October
(``couzo-exact-certificates-2026-10-09``, at ``02f9690``) state the same packings at sides
about 1.8e-11 larger, with rational half-angle tangents, so the record holds the 8 October
row at 335 and has no exact side for it. The record asked whether the decimal poses pack
at their printed sides (D3 of think-f2io, think-rx26). Four readings decide that at 335,
336, 337, 341, 373 and 374 (`COUNTS`):

- **literal**: every printed centre and angle exactly as printed. Each angle's cosine
  and sine are enclosed by outward-rounded interval arithmetic at `DIGITS` digits, and
  `devtools.decimal_pose_margins.measurement` decides every wall and every pair whose
  centres lie within 2: a wall or pair proved negative makes the pose no packing.
- **near-axis read as 0**: the same, with each angle of magnitude below `NEAR_AXIS` that
  is not zero read as 0. The 9 October certificates set those angles to 0.
- **certificate rotations**: the printed centres and side with the 9 October
  certificate's rational rotations, square by square in the same order, decided by
  `devtools.couzo_678_replay`'s two exact routes over every wall and every pair whose
  centres are closer than sqrt 2. It applies only where every printed centre lies within
  `SAME_SQUARE` of the certificate's, so that the certificate is this packing: at 335,
  where it is the report dilated; at the other five the certificate is another packing,
  below the report's side.
- **certificate**: the 9 October certificate as published, decided the same way.

A reading that proves a wall or pair negative is not a packing; one that proves every wall
and pair nonnegative is a packing; anything else is undecided and reported as such. The
receipt keeps each reading's least wall clearance and least pair separation. It decides
nothing about optimality, and runs no code of the source.

From ``packing/``, with the project interpreter::

    python -m devtools.couzo_decimal_decisions decide [--write]
    python -m devtools.couzo_decimal_decisions check
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath as mp
from strif import atomic_output_file

from devtools import couzo_678_replay as base
from devtools import decimal_pose_margins as margins
from devtools import evand_exact_certificates as legacy
from devtools.retained_data import read_retained_text
from sqpack.promote.interval import decimal_string, from_endpoints, interval
from sqpack.retained_json import dumps as retained_dumps
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
WEB = ROOT / "resources/web"
REPORTS = WEB / "couzo-extended-reports-2026-10-08"
CERTIFICATES = WEB / "couzo-exact-certificates-2026-10-09"
#: The receipt, kept beside the release whose 335 supersedes the 8 October row there.
RECEIPT = WEB / "mishapolk-issue732-f1ceee4-2026-10-23/receipts/couzo-8-october-decisions.json"
FORMAT = "couzo-8-october-decimal-decisions-v1"
#: think-rx26's counts: 335, and the five where 02f9690 beat the row by under 1.2e-11.
COUNTS = (335, 336, 337, 341, 373, 374)
#: An angle below this in magnitude, and not zero, is read as 0 in the second reading. At
#: 335 these are the angles the 9 October certificate sets to 0: 193 binary64 roundings of
#: zero, none above 3.2e-15, and three near-axis angles, 1.1e-12, 9.0e-12 and 4.7e-11; the
#: next, 2.4e-10, it keeps. `decide_count` holds the reading to the certificate's zeros
#: wherever the certificate is the report's packing.
NEAR_AXIS = Fraction(1, 10**10)
#: Working digits of the interval arithmetic.
DIGITS = 60
#: How far a printed centre may lie from the certificate's, for the two to be one square.
SAME_SQUARE = Fraction(1, 10**6)


class DecisionError(ValueError):
    """An input this decision refuses."""


def _require(condition: object, message: str) -> None:
    if not condition:
        raise DecisionError(message)


def report(n: int) -> tuple[str, Fraction, list[tuple[Fraction, Fraction, Fraction]]]:
    """The 8 October report at ``n``: its printed side, verbatim and exact, and each
    square's printed centre and angle in radians, exactly."""
    document = safe_load(read_retained_text(REPORTS / f"facts/n-{n:03d}.yaml"))
    witness = document["witness"]
    _require(witness["n"] == n, f"n={n}: the facts state another count")
    _require(
        witness["coordinates"]["angle_unit"] == "radians"
        and witness["coordinates"]["origin"] == "lower-left",
        f"n={n}: not centres from the lower left and angles in radians",
    )
    squares = [
        (
            Fraction(str(square["center"][0])),
            Fraction(str(square["center"][1])),
            Fraction(str(square["angle"])),
        )
        for square in witness["squares"]
    ]
    _require(len(squares) == n, f"n={n}: {len(squares)} squares")
    return str(witness["side"]), Fraction(str(witness["side"])), squares


def certificate(n: int) -> legacy.Certificate:
    """The 9 October certificate at ``n``, from its retained bytes."""
    return legacy.parse(
        read_retained_text(CERTIFICATES / f"source/certificates/n{n}.cert"), expected_n=n
    )


@dataclass(frozen=True)
class _Turned:
    """A square's rotation in radians, enclosed: its cosine, sine and half-width along the
    axes, ``(|cos| + |sin|)/2``."""

    cosine: Any
    sine: Any
    half_extent: Any


def _turned(theta: Fraction) -> _Turned:
    angle = margins.enclose(theta)
    cosine, sine = mp.iv.cos(angle), mp.iv.sin(angle)
    return _Turned(cosine, sine, (abs(cosine) + abs(sine)) / 2)


def _wall(square: margins.Pose, turned: _Turned, side: Fraction) -> Any:
    """The least clearance of a square's corners from the box of ``side`` centred at the
    origin, as `devtools.decimal_pose_margins.wall_clearance` reads it."""
    return margins.enclose(side / 2 - max(abs(square.x), abs(square.y))) - turned.half_extent


def _gap(first: margins.Pose, second: margins.Pose, one: _Turned, two: _Turned) -> Any:
    """The best separating-axis gap of two squares, as
    `devtools.decimal_pose_margins.pair_separation` reads it at no dilation: negative
    exactly when their interiors overlap."""
    dx = margins.enclose(second.x - first.x)
    dy = margins.enclose(second.y - first.y)
    projections = [abs(t.cosine * dx + t.sine * dy) for t in (one, two)] + [
        abs(t.cosine * dy - t.sine * dx) for t in (one, two)
    ]
    along = one.cosine * two.cosine + one.sine * two.sine
    across = one.sine * two.cosine - one.cosine * two.sine
    biggest = from_endpoints(
        max(mp.mpf(value.a) for value in projections),
        max(mp.mpf(value.b) for value in projections),
    )
    return biggest - interval("0.5") - (abs(along) + abs(across)) / 2


def _shown(value: Any) -> list[str]:
    """An enclosure's ends at eight significant digits, rounded outward."""
    return [
        decimal_string(mp.mpf(value.a), 8, upward=False),
        decimal_string(mp.mpf(value.b), 8, upward=True),
    ]


def interval_reading(
    side_text: str, side: Fraction, squares: list[tuple[Fraction, Fraction, Fraction]]
) -> dict[str, Any]:
    """Every wall and every pair whose centres lie within 2 (`decimal_pose_margins.near_pairs`)
    of the pose at its printed side, each rotation enclosed in radians at `DIGITS` digits,
    the walls and pairs read by `decimal_pose_margins`' formulas: a pose is a packing when
    every one is proved nonnegative and is not when one is proved negative."""
    poses = tuple(
        margins.Pose(index, x - side / 2, y - side / 2, Fraction(0))
        for index, (x, y, _) in enumerate(squares, start=1)
    )
    with margins.working_precision(DIGITS):
        turns = [_turned(theta) for _, _, theta in squares]
        walls = [
            (_wall(pose, turn, side), pose.label)
            for pose, turn in zip(poses, turns, strict=True)
        ]
        gaps = [
            (_gap(poses[i], poses[j], turns[i], turns[j]), poses[i].label, poses[j].label)
            for i, j in margins.near_pairs(poses)
        ]
        negative = [item for item in walls if mp.mpf(item[0].b) < 0]
        overlapping = [item for item in gaps if mp.mpf(item[0].b) < 0]
        unsure = sum(
            1 for value, *_ in [*walls, *gaps] if mp.mpf(value.a) < 0 <= mp.mpf(value.b)
        )
        least_wall = min(walls, key=lambda item: mp.mpf(item[0].a))
        least_gap = min(gaps, key=lambda item: mp.mpf(item[0].a))
        verdict = (
            "not-a-packing" if negative or overlapping else "undecided" if unsure else "packing"
        )
        return {
            "side": side_text,
            "verdict": verdict,
            "walls_outside": len(negative),
            "worst_walls": [
                {"square": label, "clearance": _shown(value)}
                for value, label in sorted(negative, key=lambda item: mp.mpf(item[0].a))[:10]
            ],
            "least_wall_clearance": _shown(least_wall[0]),
            "least_wall_square": least_wall[1],
            "pairs_overlapping": len(overlapping),
            "undecided": unsure,
            "least_pair_separation": _shown(least_gap[0]),
            "least_pair": [least_gap[1], least_gap[2]],
        }


def exact_reading(cert: legacy.Certificate) -> dict[str, Any]:
    """Both exact routes on a rational certificate, without the timings."""
    result = base.decide(base.geometry(cert))
    result.pop("cpu_seconds", None)
    return result


def with_rotations(
    n: int, side: Fraction, squares: list[tuple[Fraction, Fraction, Fraction]]
) -> tuple[legacy.Certificate | None, str]:
    """The printed centres and side with the 9 October certificate's rotations, square by
    square, and the largest distance between a printed centre and the certificate's; None
    where some square's lies `SAME_SQUARE` or more away, so the certificate states another
    packing and has no rotations of this one."""
    published = certificate(n)
    largest = max(
        max(abs(x - pose.x), abs(y - pose.y))
        for (x, y, _), pose in zip(squares, published.poses, strict=True)
    )
    if largest >= SAME_SQUARE:
        return None, f"{float(largest):.3e}"
    poses = tuple(
        legacy.Pose(x, y, pose.t)
        for (x, y, _), pose in zip(squares, published.poses, strict=True)
    )
    return legacy.Certificate(n, side, poses), f"{float(largest):.3e}"


def _summary(result: dict[str, Any]) -> dict[str, Any]:
    """An exact reading's verdict, least wall clearance and least pair gap."""
    second = result["independent"]
    return {
        "verdict": "packing" if result["passed"] else "not-a-packing",
        "sqpack_passed": result["sqpack"]["passed"],
        "independent_passed": second["passed"],
        "candidate_pairs": result["candidate_pairs"],
        "touching_pairs": result["sqpack"]["touching_pairs"],
        "least_wall_clearance": second["least_wall_clearance"],
        "least_pair_gap": second["least_pair_gap"],
        "failures": second["failures"][:5] + result["sqpack"]["failures"][:5],
    }


def decide_count(n: int) -> dict[str, Any]:
    """The four readings at ``n``."""
    side_text, side, squares = report(n)
    near = [
        index
        for index, (_, _, theta) in enumerate(squares, start=1)
        if theta != 0 and abs(theta) < NEAR_AXIS
    ]
    zeroed = [
        (x, y, Fraction(0) if index in near else theta)
        for index, (x, y, theta) in enumerate(squares, start=1)
    ]
    rotated, distance = with_rotations(n, side, squares)
    published = certificate(n)
    if rotated is not None:
        _require(
            [index for index, pose in enumerate(rotated.poses, start=1) if pose.t == 0]
            == [index for index, (_, _, theta) in enumerate(zeroed, start=1) if theta == 0],
            f"n={n}: the near-axis reading zeroes other angles than the certificate does",
        )
    return {
        "n": n,
        "printed_side": side_text,
        "near_axis_squares": near,
        "near_axis_angles": [str(squares[index - 1][2]) for index in near],
        "literal": interval_reading(side_text, side, squares),
        "near_axis_read_as_zero": interval_reading(side_text, side, zeroed),
        "certificate_rotations": (
            {
                "largest_centre_difference": distance,
                "zero_rotations": sum(1 for pose in rotated.poses if pose.t == 0),
                **_summary(exact_reading(rotated)),
            }
            if rotated is not None
            else {
                "largest_centre_difference": distance,
                "verdict": "not-applicable",
                "reason": (
                    "the certificate's squares lie this far from the printed ones, square by "
                    "square: it states another packing, with no rotations of this one"
                ),
            }
        ),
        "certificate": {
            "side": legacy.literal(published.side),
            "above_printed_side": f"{float(published.side - side):.3e}",
            **_summary(exact_reading(published)),
        },
    }


def decide(counts: tuple[int, ...] = COUNTS) -> dict[str, Any]:
    """Every count's readings, as the receipt records them."""
    started = time.process_time()
    rows = [decide_count(n) for n in counts]
    return {
        "format": FORMAT,
        "reports": REPORTS.relative_to(REPO).as_posix(),
        "certificates": CERTIFICATES.relative_to(REPO).as_posix(),
        "program": "packing/devtools/couzo_decimal_decisions.py",
        "interval_digits": DIGITS,
        "near_axis": str(NEAR_AXIS),
        "rows": rows,
        "cpu_seconds": round(time.process_time() - started, 1),
    }


def _stable(record: dict[str, Any]) -> dict[str, Any]:
    copy = json.loads(json.dumps(record))
    copy.pop("cpu_seconds", None)
    return copy


def check() -> list[str]:
    """Where the retained receipt differs from a fresh decision, apart from its timing."""
    kept = json.loads(RECEIPT.read_text(encoding="utf-8"))
    fresh = decide(tuple(row["n"] for row in kept["rows"]))
    return (
        []
        if _stable(kept) == _stable(fresh)
        else [f"{RECEIPT.name}: differs from a fresh decision"]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n", 1)[0])
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("decide")
    run.add_argument("--write", action="store_true")
    commands.add_parser("check")
    args = parser.parse_args(argv)
    if args.command == "check":
        problems = check()
        for problem in problems:
            print(problem)
        print("FAILED" if problems else "OK: the receipt is a fresh decision")
        return 1 if problems else 0
    record = decide()
    if args.write:
        RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        with atomic_output_file(RECEIPT) as temporary:
            Path(temporary).write_text(retained_dumps(record, sort_keys=True), encoding="utf-8")
    for row in record["rows"]:
        print(
            row["n"],
            "literal:",
            row["literal"]["verdict"],
            row["literal"]["least_wall_clearance"],
            "| near-axis 0:",
            row["near_axis_read_as_zero"]["verdict"],
            "| certificate rotations:",
            row["certificate_rotations"]["verdict"],
            "| certificate:",
            row["certificate"]["verdict"],
        )
    print(f"cpu {record['cpu_seconds']} s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
