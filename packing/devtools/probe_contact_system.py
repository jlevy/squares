#!/usr/bin/env python3
"""Report what an assembled contact system determines, and walk what it does not.

This is the tool that found [D-361](../defects.md), and it exists because that finding
was first made in a throwaway script.  A measurement that overturns a claim in the record
has to be replayable by the next reader, so it lives here rather than in a transcript.

**What it reports.**  For each retained case: the contact typing, the assembled equation
count against the unknowns, the Jacobian's rank and the gap the rank verdict rests on,
the residual at the pose the structure came from, `side_leak`, and what `close` does.

**What `--walk` adds, and why it is the interesting half.**  A rank shortfall says the
contacts do not pin the pose.  It does not say *why*, and the difference between "a
stationarity condition is missing" and "an equation is wrong" is invisible to it.
Walking the null direction that most changes the side separates them by the *order* of
the violation it produces:

- `O(t^2)` is an ordinary second-order obstruction.  The contacts hold to first order and
  curvature is what forbids the motion.  Nothing is missing.
- `O(t)` means an active constraint is being violated *linearly* along a direction where
  its own equation has zero derivative -- so that equation is not the constraint, and
  something is wrong with the assembly rather than with the packing.

At `n = 11` with `edge-edge` written as one equation, the descent direction gave `O(t)`
on three declared contacts.  That is the whole of D-361, and it is one command.

Usage:

    python -m devtools.probe_contact_system                 # every case
    python -m devtools.probe_contact_system --case trump11 --walk
    python -m devtools.probe_contact_system --json
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

import mpmath as mp

from cases.gobel5 import packing as gobel5
from cases.kingbird29.verify_svg import materialise_svg
from cases.kingbird29.verify_svg import sign as kingbird_sign
from cases.trump11 import packing as trump11
from sqpack.promote.contacts import extract_contacts, require_decided
from sqpack.promote.system import (
    CORNER_OFFSETS,
    ContactSystem,
    SystemAssemblyError,
    assemble,
    close,
    contact_jacobian,
    jacobian_rank,
    pose_values,
    residual_at,
)

ROOT = Path(__file__).resolve().parent.parent
PROVENANCE = ROOT / "resources/papers/kingbird-square-29-provenance.svg"

#: Working precision for the exact cases. The Kingbird case needs far more and says so.
EXACT_DIGITS = 50
KINGBIRD_DIGITS = 160
KINGBIRD_FLOOR = "1e-80"
AMBIGUITY_RATIO = "1e10"

#: Steps for `--walk`, an order of magnitude apart so the violation's order in `t` is
#: read off the ratios rather than asserted.
WALK_STEPS = ("1e-3", "1e-4", "1e-5")


def _exact_case(build: Callable, digits: int) -> tuple[list, Any, Any, list, float]:
    """Field elements for the extraction, floats for the pose.

    They cannot be the same objects.  Extraction decides signs, and an exact case decides
    them with `field.sign`, which is defined on field elements and not on floats; the
    pose that goes into the Jacobian is numeric.  Handing the extractor floats is how the
    first version of this tool crashed.
    """
    squares, side, field = build()
    field.refine_to(digits)
    numbers = [
        [(float(field.decimal(x, 30)), float(field.decimal(y, 30))) for x, y in square]
        for square in squares
    ]
    return squares, side, field.sign, numbers, float(field.decimal(side, 30))


def _kingbird_case() -> tuple[list, float, Callable, list, float]:
    mp.mp.dps = KINGBIRD_DIGITS
    _raw, _entities, side, squares = materialise_svg(PROVENANCE)
    return squares, side, kingbird_sign, squares, side


#: Name -> (loader, working digits, extraction keywords).
#:
#: The digits are pinned per case rather than inherited, and that is not decoration. The
#: rank verdict is a judgement about a gap between singular values, and the gap this tool
#: can *see* is bounded by the precision the SVD runs at: at mpmath's ambient default of
#: 15, Göbel's discarded singular value reads `2.3e-16` against a counted `0.511`, where
#: pinned it is around `1e-51`. Same verdict, a gap four decades narrower than the truth,
#: and a reader would have no way to tell the difference from the output.
CASES: dict[str, tuple[Callable, int, dict]] = {
    "gobel5": (lambda: _exact_case(gobel5.build, EXACT_DIGITS), EXACT_DIGITS, {}),
    "trump11": (lambda: _exact_case(trump11.build, EXACT_DIGITS), EXACT_DIGITS, {}),
    "kingbird29": (
        _kingbird_case,
        KINGBIRD_DIGITS,
        {"floor": KINGBIRD_FLOOR, "ambiguity_ratio": AMBIGUITY_RATIO},
    ),
}


def _corners_at(values: Sequence[float], count: int, chirality: Sequence[int]) -> list:
    """The packing at a pose, inverting `sqpack.promote.system._corner` numerically."""
    squares = []
    for index in range(count):
        centre_x, centre_y = values[index], values[count + index]
        angle = values[2 * count + index]
        cosine, sine = math.cos(angle), math.sin(angle)
        corners = []
        for offset_x, offset_y in CORNER_OFFSETS:
            local_x = 0.5 * offset_x * chirality[index]
            local_y = 0.5 * offset_y
            corners.append(
                (
                    centre_x + cosine * local_x - sine * local_y,
                    centre_y + sine * local_x + cosine * local_y,
                )
            )
        squares.append(corners)
    return squares


def _separation(first: Sequence, second: Sequence) -> float:
    """The widest separating-axis gap, negative when the squares overlap."""
    best = None
    for square in (first, second):
        for index in range(4):
            edge_x = square[(index + 1) % 4][0] - square[index][0]
            edge_y = square[(index + 1) % 4][1] - square[index][1]
            length = math.hypot(edge_x, edge_y)
            axis = (-edge_y / length, edge_x / length)
            left = [x * axis[0] + y * axis[1] for x, y in first]
            right = [x * axis[0] + y * axis[1] for x, y in second]
            gap = max(min(right) - max(left), min(left) - max(right))
            best = gap if best is None else max(best, gap)
    return float(best if best is not None else 0.0)


def _null_direction(system: ContactSystem, values: Sequence[float]) -> list[float] | None:
    """The unit null-space direction that changes the side the most, or None if there is none.

    Built from the projection of the side's unit vector onto the null space, so it is the
    steepest side-changing motion the contacts permit rather than an arbitrary basis
    vector -- which a null space does not have.
    """
    _left, singular, right = mp.svd_r(contact_jacobian(system, values))
    ordered = [float(singular[i]) for i in range(singular.rows)]
    rank = sum(1 for value in ordered if value > 1e-9 * ordered[0])
    if rank >= right.rows:
        return None
    side_index = list(system.unknowns).index("s")
    weights = [float(right[k, side_index]) for k in range(rank, right.rows)]
    norm = math.sqrt(sum(w * w for w in weights))
    if norm < 1e-14:
        return None
    return [
        sum(weights[k - rank] * float(right[k, j]) for k in range(rank, right.rows)) / norm
        for j in range(right.cols)
    ]


def walk(system: ContactSystem, values: Sequence[float], contacts: set) -> dict:
    """Step along the side-changing null direction and report the violation's order in `t`.

    Both signs are walked because they answer different questions.  The `+` direction
    grows the container and is expected to obstruct at second order; the `-` direction
    shrinks it, and a first-order violation there is the signature of an equation that
    does not describe its constraint.
    """
    direction = _null_direction(system, values)
    if direction is None:
        return {
            "walkable": False,
            "reason": (
                "the null space contains no direction that changes the side, so there is "
                "nothing here to walk -- which is what a determined system looks like"
            ),
        }
    count = system.n
    side_index = list(system.unknowns).index("s")
    rows: list[dict] = []
    for sign in (1, -1):
        for text in WALK_STEPS:
            step = sign * float(text)
            moved = [values[j] + step * direction[j] for j in range(len(values))]
            squares = _corners_at(moved, count, system.chirality)
            worst = None
            offenders: list[tuple[float, int, int]] = []
            for i in range(count):
                for j in range(i + 1, count):
                    gap = _separation(squares[i], squares[j])
                    if gap < 0:
                        offenders.append((gap, i, j))
                    worst = gap if worst is None else min(worst, gap)
            offenders.sort()
            rows.append(
                {
                    "step": step,
                    "side": moved[side_index],
                    "worst_separation": worst,
                    "overlapping_pairs": len(offenders),
                    "worst_three": [
                        {
                            "pair": [i, j],
                            "separation": gap,
                            "declared_contact": (i, j) in contacts,
                        }
                        for gap, i, j in offenders[:3]
                    ],
                }
            )
    return {"walkable": True, "steps": rows, "order": _order(rows)}


def _order(rows: Sequence[dict]) -> dict:
    """Read the violation's order in `t` off consecutive decades, per sign."""
    verdicts: dict[str, str] = {}
    for label, sign in (("grow", 1), ("shrink", -1)):
        series = [row for row in rows if (row["step"] > 0) == (sign > 0)]
        series = [row for row in series if row["worst_separation"] is not None]
        if len(series) < 2:
            verdicts[label] = "not enough steps"
            continue
        ratios = []
        for earlier, later in itertools.pairwise(series):
            if later["worst_separation"] == 0:
                continue
            ratios.append(abs(earlier["worst_separation"] / later["worst_separation"]))
        if not ratios:
            verdicts[label] = "no violation at any step"
            continue
        typical = sum(ratios) / len(ratios)
        # A decade of `t` per step: ~10x is linear, ~100x is quadratic.
        if typical < 30:
            verdicts[label] = f"O(t), ratio {typical:.1f} per decade -- an equation is wrong"
        elif typical < 300:
            verdicts[label] = (
                f"O(t^2), ratio {typical:.1f} per decade -- a second-order obstruction"
            )
        else:
            verdicts[label] = f"steeper than quadratic, ratio {typical:.1f} per decade"
    return verdicts


def probe(name: str, *, with_walk: bool = False) -> dict:
    """Assemble one case and report what its system determines."""
    loader, digits, keywords = CASES[name]
    saved = mp.mp.dps
    mp.mp.dps = digits
    try:
        squares, side, sign, numbers, side_value = loader()
        structure = require_decided(extract_contacts(squares, side, sign=sign, **keywords))
        system = assemble(structure)
        values = pose_values(system, numbers, side_value)
        residuals = residual_at(system, values)
        info = jacobian_rank(system, values)
        try:
            closure = len(close(system, values).closure)
            closure_note = f"{closure} conditions"
        except SystemAssemblyError as error:
            closure_note = f"refuses: {error.kind}"
        walked = None
        if with_walk:
            contacts = {(i.left, int(i.right)) for i in structure.pair_contacts}
            walked = walk(system, values, contacts)
    finally:
        mp.mp.dps = saved

    report: dict[str, Any] = {
        "case": name,
        "working_digits": digits,
        "n": structure.n,
        "contact_types": dict(Counter(i.contact for i in structure.pair_contacts)),
        "wall_contacts": len(structure.wall_contacts),
        "chirality_reflected": sum(1 for s in structure.chirality if s < 0),
        "equations": len(system.equations),
        "unknowns": info["unknowns"],
        "rank": info["rank"],
        "shortfall": info["shortfall"],
        "side_leak": info["side_leak"],
        "residual": max(abs(v) for v in residuals),
        "smallest_counted": info["smallest_counted"],
        "largest_discarded": info["largest_discarded"],
        "closure": closure_note,
    }
    if walked is not None:
        report["walk"] = walked
    return report


def _render(report: dict) -> None:
    print(f"== {report['case']} (n = {report['n']}) ==")
    types = ", ".join(f"{k} x{v}" for k, v in sorted(report["contact_types"].items()))
    print(f"  contacts: {types}; {report['wall_contacts']} wall")
    if report["chirality_reflected"]:
        print(f"  reflected squares: {report['chirality_reflected']}")
    print(
        f"  {report['equations']} equations, {report['unknowns']} unknowns, "
        f"rank {report['rank']} -- shortfall {report['shortfall']}"
    )
    print(f"  residual at the retained pose: {report['residual']:.3e}")
    print(f"  side_leak: {report['side_leak']:.3e}")
    discarded = report["largest_discarded"]
    gap = "nothing discarded" if discarded is None else f"{discarded:.3e}"
    print(
        f"  rank gap at {report['working_digits']} digits: "
        f"smallest counted {report['smallest_counted']:.3e} vs {gap}"
    )
    print(f"  close(): {report['closure']}")
    if "walk" in report:
        result = report["walk"]
        if not result["walkable"]:
            print(f"  walk: {result['reason']}")
            return
        print("  walk along the steepest side-changing null direction:")
        print(f"    {'step':>10} {'side':>20} {'worst sep':>14} {'overlaps':>9}")
        for row in result["steps"]:
            print(
                f"    {row['step']:>10.0e} {row['side']:>20.12f} "
                f"{row['worst_separation']:>14.3e} {row['overlapping_pairs']:>9d}"
            )
        for label, verdict in result["order"].items():
            print(f"    {label}: {verdict}")
        offenders = [
            entry for row in result["steps"] if row["step"] < 0 for entry in row["worst_three"]
        ]
        if offenders:
            declared = sum(1 for entry in offenders if entry["declared_contact"])
            print(
                f"    worst offenders on the shrink side: {declared} of {len(offenders)} "
                "are declared contacts"
            )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--case",
        choices=[*CASES, "all"],
        default="all",
        help="which retained case to probe (default: all)",
    )
    parser.add_argument(
        "--walk",
        action="store_true",
        help="also step along the side-changing null direction and report its order in t",
    )
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    arguments = parser.parse_args(argv)

    names = list(CASES) if arguments.case == "all" else [arguments.case]
    reports = [probe(name, with_walk=arguments.walk) for name in names]
    if arguments.json:
        print(json.dumps(reports, indent=2, sort_keys=True))
        return 0
    for report in reports:
        _render(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
