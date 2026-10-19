"""Check fixed scalar premises; no packing, LP, compactness or rank theorem replay."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import re
import sys
import time
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

SCHEMA = "n17-global-contact-budget-scalars/v1"
DESCRIPTOR_SCHEMA = "n17-global-contact-budget-scalars-context/v1"
BYTE_LIMIT = 1 << 20
BIT_LIMIT = 4096
MAX_SECONDS = 10
RATIONAL = re.compile(r"(?:0|-?[1-9][0-9]*)(?:/[1-9][0-9]*)?", re.ASCII)
CONSTANTS = {
    "outer_U": "1169/250",
    "wall_strip_width": "1/4",
    "tangential_separation": "15/16",
    "wall_capacity": 4,
    "walls": 4,
    "squares": 17,
    "variables": 35,
}


class IncompleteError(ValueError):
    """The finite arithmetic check did not finish within its resource contract."""


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def tick(deadline: float) -> None:
    if time.monotonic() >= deadline:
        raise IncompleteError("scalar checker wall ceiling")


def rational(value: Any) -> Q:
    require(type(value) is str and RATIONAL.fullmatch(value) is not None, "rational grammar")
    if len(value) > 2600:
        raise IncompleteError("rational string ceiling")
    result = Q(value)
    if max(abs(result.numerator).bit_length(), result.denominator.bit_length()) > BIT_LIMIT:
        raise IncompleteError("rational bit ceiling")
    require(str(result) == value, "canonical rational required")
    return result


def scalar_packet(u: Q, strip: Q, separation: Q, capacity: int, n: int) -> dict[str, Any]:
    """Pure arithmetic helper; generic inputs are synthetic controls only."""
    checks = [
        ("support_radical_upper_bound", Q(2), "<", Q(3, 2) ** 2),
        ("disk_separation_squared", 1 - strip**2, ">", separation**2),
        ("five_wall_centres_span", u - 1, "<", capacity * separation),
        ("rank_count_subtraction", Q(2 * n + 1 - 4 * capacity), "==", Q(19)),
    ]
    return {
        name: {
            "left": str(left),
            "relation": relation,
            "right": str(right),
            "holds": left < right
            if relation == "<"
            else left > right
            if relation == ">"
            else left == right,
        }
        for name, left, relation, right in checks
    }


def star_packet() -> dict[str, Any]:
    """Finite identities and squared comparisons, not angular packing arguments."""
    x, c2 = Q(3, 4), Q(7, 8)
    coefficient = 16 * c2**2 - 20 * c2 + 5
    facts = {
        "triple_angle_polynomial_at_three_quarters": (4 * x**3 - 3 * x + Q(1, 2), Q(-1, 16)),
        "five_angle_reduced_coefficient": (coefficient, Q(-1, 4)),
        "five_angle_cosine_squared": (coefficient**2 * c2, Q(14, 256)),
    }
    identities = {
        name: {"left": str(left), "right": str(right), "holds": left == right}
        for name, (left, right) in facts.items()
    }
    comparisons = {
        "mixed_corner_squared_comparison": {
            "left": "4",
            "right": "9/2",
            "holds": Q(4) < Q(9, 2),
        },
        "wall_arc_squared_comparison": {
            "left": str(89**2),
            "right": str(2 * 64**2),
            "holds": 89**2 < 2 * 64**2,
        },
        "corner_arc_squared_comparison": {"left": "9", "right": "8", "holds": Q(9) > Q(8)},
    }
    return {"identities": identities, "squared_comparisons": comparisons}


def no_claims() -> dict[str, bool]:
    return {
        "hand_global_theorem_verified": False,
        "packing_geometry_checked": False,
        "global_exclusion_proved": False,
        "n17_exclusion_proved": False,
        "census_admission": False,
        "fixed_U_wall_filter_applied": False,
        "contact_pattern_realized": False,
    }


def generate(document: Any, *, deadline: float) -> dict[str, Any]:
    tick(deadline)
    require(
        type(document) is dict
        and set(document) == {"schema", "constants", "include_star_packet"},
        "descriptor fields differ",
    )
    require(document["schema"] == DESCRIPTOR_SCHEMA, "descriptor schema differs")
    require(
        type(document["constants"]) is dict and document["constants"] == CONSTANTS,
        "frozen constants differ",
    )
    constants = cast(dict[str, Any], document["constants"])
    for key in ("wall_capacity", "walls", "squares", "variables"):
        require(type(constants[key]) is int, "integer constant required")
    require(type(document["include_star_packet"]) is bool, "star selection must be boolean")
    u, strip, separation = (
        rational(constants[key])
        for key in ("outer_U", "wall_strip_width", "tangential_separation")
    )
    packet = scalar_packet(u, strip, separation, 4, 17)
    require(all(row["holds"] for row in packet.values()), "scalar inequality fails")
    stars = star_packet() if document["include_star_packet"] else None
    if stars is not None:
        require(
            all(row["holds"] for group in stars.values() for row in group.values()),
            "star arithmetic fails",
        )
    tick(deadline)
    return {
        "schema": SCHEMA,
        "status": "scalar_premises_verified",
        "arithmetic_packet_verified": True,
        "accepted_inputs": copy.deepcopy(document),
        "scalar_checks": packet,
        "optional_star_arithmetic": stars,
        "hand_implications_not_independently_verified": [
            "square support and open disk geometry",
            "sorted wall centre capacity argument",
            "area lower bound and inactive artificial side bounds",
            "complete fixed orientation SAT union",
            "compactness and global lexicographic normalization",
            "vertex active normal rank35 existence theorem",
            "active separating rows imply distinct physical contacts",
            "angular gap and contact degree arguments",
        ],
        **no_claims(),
    }


def payload(value: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in value.items()
        if key not in {"process_id", "verification_passed", "descriptor_sha256"}
    }


def check(document: Any, certificate: Any, *, deadline: float) -> dict[str, Any]:
    require(type(certificate) is dict, "certificate object required")
    result = generate(document, deadline=deadline)
    require(payload(result) == payload(certificate), "fresh arithmetic payload differs")
    return result | {"verification_passed": True}


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def reject_scalar(value: str) -> Any:
    raise ValueError("JSON floating/nonfinite scalar forbidden: " + value)


def read_json(path: Path, deadline: float) -> tuple[bytes, Any]:
    tick(deadline)
    with path.open("rb") as stream:
        raw = stream.read(BYTE_LIMIT + 1)
    if len(raw) > BYTE_LIMIT:
        raise IncompleteError("JSON byte ceiling")
    value = json.loads(
        raw,
        object_pairs_hook=unique_object,
        parse_float=reject_scalar,
        parse_constant=reject_scalar,
    )
    tick(deadline)
    return raw, value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--descriptor", type=Path, required=True)
    parser.add_argument("--certificate", type=Path)
    parser.add_argument("--max-seconds", type=float, default=MAX_SECONDS)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    require(
        math.isfinite(args.max_seconds) and 0 < args.max_seconds <= MAX_SECONDS,
        "phase wall must be finite and at most10 seconds",
    )
    deadline = time.monotonic() + args.max_seconds
    if args.output.exists() or args.output.resolve() in {
        args.descriptor.resolve(),
        args.certificate.resolve() if args.certificate else None,
    }:
        print("refused: output already exists or aliases input", file=sys.stderr)
        return 1
    try:
        raw, document = read_json(args.descriptor, deadline)
        held = {args.descriptor: raw}
        if args.certificate:
            saved, certificate = read_json(args.certificate, deadline)
            held[args.certificate] = saved
            require(
                type(certificate) is dict
                and certificate.get("descriptor_sha256") == hashlib.sha256(raw).hexdigest(),
                "certificate descriptor byte identity differs",
            )
            result = check(document, certificate, deadline=deadline)
        else:
            result = generate(document, deadline=deadline)
        for path, before in held.items():
            require(read_json(path, deadline)[0] == before, "retained input bytes changed")
        result["descriptor_sha256"] = hashlib.sha256(raw).hexdigest()
        result["process_id"] = os.getpid()
        tick(deadline)
        text = json.dumps(result, sort_keys=True, indent=2) + "\n"
        if len(text.encode()) > BYTE_LIMIT:
            raise IncompleteError("output byte ceiling")
        tick(deadline)
    except (ValueError, OSError, KeyError, TypeError, RecursionError) as exc:
        result = {
            "schema": SCHEMA,
            "status": "incomplete" if isinstance(exc, IncompleteError) else "refused",
            "arithmetic_packet_verified": False,
            "verification_passed": False,
            "error": str(exc),
            **no_claims(),
        }
        text = json.dumps(result, sort_keys=True, indent=2) + "\n"
    with args.output.open("x") as stream:
        stream.write(text)
    return 0 if result["status"] == "scalar_premises_verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
