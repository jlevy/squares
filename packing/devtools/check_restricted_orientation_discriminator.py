"""Independent fixed-angle receipt/witness check; no exhaustive positive certificate."""

from __future__ import annotations

import argparse
import json
import math
import re
import signal
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

type Quadratic = tuple[Fraction, Fraction]
type Point = tuple[Quadratic, Quadratic]

NAMES = (
    "axis_ten_cover",
    "localization",
    "forced_A1",
    "forced_A2",
    "forced_A3",
    "twelve_cover_0",
    "twelve_cover_45",
)
BY_ANGLE = {0: (NAMES[0], NAMES[5]), 45: (*NAMES[1:5], NAMES[6])}
LIMIT = 262144
RATIONAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", re.ASCII)


def rational(value: int | str | Fraction) -> Quadratic:
    return Fraction(value), Fraction(0)


def add(x: Quadratic, y: Quadratic) -> Quadratic:
    return x[0] + y[0], x[1] + y[1]


def scale(x: Quadratic, factor: int | Fraction) -> Quadratic:
    return x[0] * factor, x[1] * factor


def subtract(x: Quadratic, y: Quadratic) -> Quadratic:
    return add(x, scale(y, -1))


def sign(value: Quadratic) -> int:
    """Exact sign of a+b sqrt(2), without numerical root isolation."""
    a, b = value
    if a == 0:
        return (b > 0) - (b < 0)
    if b == 0 or (a > 0) == (b > 0):
        return (a > 0) - (a < 0)
    difference = a * a - 2 * b * b
    result = (difference > 0) - (difference < 0)
    return result if a > 0 else -result


def between(value: Quadratic, low: Quadratic, high: Quadratic) -> bool:
    return sign(subtract(value, low)) >= 0 and sign(subtract(high, value)) >= 0


def coordinate(value: Any) -> Quadratic:
    if (
        type(value) is not str
        or len(value) > 520
        or not value.startswith("poly[")
        or not value.endswith("]")
    ):
        raise ValueError("coordinate requires bounded poly[a,b]")
    parts = value[5:-1].split(",")
    if len(parts) != 2:
        raise ValueError("coordinate requires two coefficients")
    values = []
    for part in parts:
        if len(part) > 256 or RATIONAL.fullmatch(part) is None:
            raise ValueError("coefficient must be a bounded ASCII rational")
        number = Fraction(part)
        if str(number) != part:
            raise ValueError("coefficient is not canonical")
        values.append(number)
    return values[0], values[1]


def point(value: Any) -> Point:
    if type(value) is not list or len(value) != 2:
        raise ValueError("point requires two coordinates")
    return coordinate(value[0]), coordinate(value[1])


def formulas(side: Quadratic) -> tuple[set[Point], tuple[Point, ...]]:
    """Independent transcription of the unchanged Theorem 3 formulas."""
    one, half = rational(1), scale(side, Fraction(1, 2))
    seeds = (
        (one, one),
        (half, one),
        (subtract(rational("3/2"), scale(side, Fraction(1, 4))), half),
        (add(rational("1/2"), scale(side, Fraction(1, 4))), half),
    )
    ten = {
        (subtract(side, x) if flip_x else x, subtract(side, y) if flip_y else y)
        for x, y in seeds
        for flip_x in (False, True)
        for flip_y in (False, True)
    }
    twelve = (
        (one, subtract(side, rational(3))),
        (half, subtract(side, rational(3))),
        (rational("3/2"), rational("13/10")),
        (subtract(side, one), one),
        (subtract(side, rational("4/5")), half),
        (subtract(side, one), subtract(side, one)),
        (half, subtract(side, rational("4/5"))),
        (one, subtract(side, one)),
        (rational("4/5"), subtract(side, rational(2))),
        (rational("17/10"), rational("11/5")),
        (rational("11/5"), rational("11/5")),
        (rational("11/5"), rational("17/10")),
    )
    return ten, twelve


def membership(center: Point, points: tuple[Point, ...], angle: int) -> int:
    bound = rational("1/2") if angle == 0 else (Fraction(0), Fraction(1, 2))
    mask = 0
    for index, (px, py) in enumerate(points):
        dx, dy = subtract(px, center[0]), subtract(py, center[1])
        values = (dx, dy) if angle == 0 else (add(dx, dy), subtract(dy, dx))
        if all(between(value, scale(bound, -1), bound) for value in values):
            mask |= 1 << index
    return mask


def check_escape(
    side: Quadratic, ten: tuple[Point, ...], twelve: tuple[Point, ...], row: Any
) -> str:
    if type(row) is not dict:
        raise TypeError("escape must be an object")
    angle, name = row.get("angle_degrees"), row.get("obligation")
    if (
        type(angle) is not int
        or angle not in BY_ANGLE
        or not isinstance(name, str)
        or name not in BY_ANGLE[angle]
    ):
        raise ValueError("escape angle and obligation disagree")
    if row.get("square_side") != "1" or row.get("square_semantics") != "closed":
        raise ValueError("escape must be a closed unit square")
    if row.get("strict_box_counterexample_established") is not False:
        raise ValueError("escape is not a strict-box counterexample")
    center = point(row.get("center_power_basis"))
    extent = rational("1/2") if angle == 0 else (Fraction(0), Fraction(1, 2))
    if not all(between(value, extent, subtract(side, extent)) for value in center):
        raise ValueError("escape fails closed containment")
    ten_mask, twelve_mask = membership(center, ten, angle), membership(center, twelve, angle)
    for key, actual in (
        ("ten_membership_mask", ten_mask),
        ("twelve_membership_mask", twelve_mask),
    ):
        if type(row.get(key)) is not int or row[key] != actual:
            raise ValueError("escape membership mask disagrees")
    x, y = center
    one = rational(1)
    localized = between(x, one, subtract(side, one)) and (
        sign(subtract(y, one)) <= 0 or sign(subtract(y, subtract(side, one))) >= 0
    )
    canonical = between(x, one, scale(side, Fraction(1, 2))) and between(y, rational(0), one)
    if name.startswith("twelve_cover_"):
        failed = twelve_mask == 0
    elif name == "axis_ten_cover":
        failed = ten_mask == 0
    elif name == "localization":
        failed = ten_mask == 0 and not localized
    else:
        index = int(name[-1]) - 1
        failed = ten_mask == 0 and canonical and not twelve_mask & (1 << index)
    if not failed:
        raise ValueError("square does not falsify the named clause")
    return name


def check_packet(packet: Any, mode: str, producer_exit_code: int) -> dict[str, Any]:
    if mode not in ("source-control", "target-fixed-side") or type(packet) is not dict:
        raise ValueError("invalid packet or mode")
    if (
        packet.get("mode") != mode
        or packet.get("kind") != "restricted-orientation-auxiliary-discriminator"
    ):
        raise ValueError("packet mode or kind mismatch")
    if (
        packet.get("h036_outcome") != "unresolved"
        or packet.get("theorem_acceptance") is not False
        or packet.get("perturbed_angles_evaluated") is not False
    ):
        raise ValueError("packet exceeds the auxiliary scope")
    complete = packet.get("complete")
    if (
        type(complete) is not bool
        or (complete and producer_exit_code != 0)
        or (not complete and producer_exit_code == 0)
    ):
        raise ValueError("completion and producer exit disagree")
    outcomes = packet.get("obligations")
    if (
        type(outcomes) is not dict
        or set(outcomes) != set(NAMES)
        or any(value is not None and type(value) is not bool for value in outcomes.values())
    ):
        raise ValueError("seven Boolean-or-null outcomes required")
    for key, expected in (
        ("checked_obligations", [name for name in NAMES if outcomes[name] is not None]),
        ("unchecked_obligations", [name for name in NAMES if outcomes[name] is None]),
    ):
        if packet.get(key) != expected:
            raise ValueError("checked/unchecked inventory disagrees")
    cases = packet.get("cases")
    if type(cases) is not list or len(cases) > 2:
        raise ValueError("invalid completed case inventory")
    angles = []
    for case in cases:
        if type(case) is not dict or type(case.get("angle_degrees")) is not int:
            raise ValueError("invalid angle case")
        angles.append(case["angle_degrees"])
        counts = case.get("reachable_event_strata_by_dimension")
        if (
            type(counts) is not list
            or len(counts) != 3
            or any(type(n) is not int or n < 0 for n in counts)
            or sum(counts) == 0
        ):
            raise ValueError("invalid or empty stratum counts")
    if angles not in ([], [0], [0, 45]) or (complete and angles != [0, 45]):
        raise ValueError("completed angles must be a prefix of 0,45")
    expected_checked = {name for angle in angles for name in BY_ANGLE[angle]}
    if expected_checked != set(packet["checked_obligations"]):
        raise ValueError("angle completion and outcomes disagree")
    escapes = packet.get("obstructions")
    if type(escapes) is not list or len(escapes) > 7:
        raise ValueError("invalid escape inventory")
    inputs = packet.get("inputs")
    verified: list[str] = []
    if inputs is None:
        if cases or escapes or complete:
            raise ValueError("checked work requires exact inputs")
    else:
        if type(inputs) is not dict or inputs.get("mode") != mode:
            raise ValueError("input mode mismatch")
        if (
            inputs.get("kind") != "input"
            or inputs.get("field") != "Q(sqrt(2)), positive root in (1,2)"
        ):
            raise ValueError("input field or receipt kind mismatch")
        # The target value is constructed only after explicit target dispatch.
        side = (
            (Fraction(2), Fraction(4, 3)) if mode == "source-control" else rational("1939/500")
        )
        if coordinate(inputs.get("container_side_power_basis")) != side:
            raise ValueError("wrong fixed side")
        expected_ten, expected_twelve = formulas(side)
        actual_points = []
        for key, count in (("ten_points_power_basis", 10), ("twelve_points_power_basis", 12)):
            values = inputs.get(key)
            if type(values) is not list or len(values) != count:
                raise ValueError("wrong point inventory")
            parsed = tuple(point(value) for value in values)
            if len(set(parsed)) != count:
                raise ValueError("duplicate point")
            actual_points.append(parsed)
        ten, twelve = actual_points
        if set(ten) != expected_ten or twelve != expected_twelve:
            raise ValueError("point formulas or A labels disagree")
        verified = [check_escape(side, ten, twelve, row) for row in escapes]
    if len(set(verified)) != len(verified) or set(verified) != {
        name for name in NAMES if outcomes[name] is False
    }:
        raise ValueError("each failed clause requires one verified escape")
    decision = "rejected" if verified else "accepted" if complete else "unresolved"
    return {
        "decision": decision,
        "mode": mode,
        "verified_escapes": verified,
        "h036_outcome": "unresolved",
        "standalone_exhaustive_certificate": False,
        "positive_assurance": "reviewed algorithm plus independent input/receipt checks",
    }


def _pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _float(value: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError("nonfinite JSON number")
    return number


def load_packet(path: Path) -> Any:
    with path.open("rb") as stream:
        data = stream.read(LIMIT + 1)
    if len(data) > LIMIT:
        raise ValueError("packet exceeds byte limit")
    return json.loads(data, object_pairs_hook=_pairs, parse_float=_float, parse_constant=_float)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--source-control", action="store_true")
    modes.add_argument("--target-fixed-side", action="store_true")
    parser.add_argument("--producer-exit-code", type=int, required=True)
    args = parser.parse_args()

    def expired(_signal: int, _frame: Any) -> None:
        raise TimeoutError("independent replay exceeded ten seconds")

    previous = signal.signal(signal.SIGALRM, expired)
    signal.alarm(10)
    try:
        mode = "source-control" if args.source_control else "target-fixed-side"
        result = check_packet(load_packet(args.packet), mode, args.producer_exit_code)
        print(json.dumps(result, sort_keys=True))
        return 1 if result["decision"] == "unresolved" else 0
    except TimeoutError as error:
        print(json.dumps({"decision": "unresolved", "reason": str(error)}))
        return 1
    except (OSError, ValueError, TypeError, KeyError, RecursionError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)


if __name__ == "__main__":
    raise SystemExit(main())
