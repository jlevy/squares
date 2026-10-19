"""Inventory every active owner-axis feature of the exact n17 endpoint.

This certifies first-order *inputs*, not a tangent-cone or stationarity verdict.
The H-255 root and H-256 packing receipts are mandatory prerequisites.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import argparse
import hashlib
import json
import time
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from typing import Any

import sympy as sp

from devtools.check_n17_contact_chart import ANCHORS, CONTACTS, SOURCE
from devtools.check_n17_endpoint_feasibility import (
    FROZEN_ROOT_REF,
    Box,
    _dot,
    _encode_receipt,
    _fraction_string,
    _layout,
    _object_unique,
    _read_limited,
    _support,
    _support_interval,
    require_retained_path,
    symbolic_identities,
)
from devtools.check_n17_root_certificate import CertificateError
from devtools.check_n17_root_certificate import check as check_root

EX, EY = "ex", "ey"
AXES = {
    "axis": (EX, EY),
    "theta": ("u", "v"),
    "beta": ("p", "q"),
}
WALLS = ("left", "right", "bottom", "top")
PARALLEL_PAIRS = frozenset(
    {(1, 2), (1, 3), (5, 7), (9, 10), (9, 11), (10, 12), (11, 12), (12, 14), (13, 14)}
)
ZERO_PAIRS = frozenset(tuple(sorted((left, right))) for left, right, _, _ in CONTACTS) | {
    (2, 3)
}
ANCHOR_SET = frozenset(ANCHORS)
EXPECTED_COUNTS = {
    "pairs": 21,
    "pair_options": 168,
    "pair_zero": 33,
    "pair_strict_negative": 135,
    "active_wall_incidences": 15,
    "wall_corners": 60,
    "wall_corner_zero": 29,
    "wall_corner_strict": 31,
    "parallel_pairs": 9,
}
FROZEN_ENDPOINT_REF = (
    "ad7a36ed0:packing/campaign/series/series-000-smoke-and-calibration/"
    "results/exp-238-n17-endpoint-feasibility/run-001/certificate.json"
)


def square_class(label: int) -> str:
    if label in {*range(1, 9), 15, 17}:
        return "axis"
    if 9 <= label <= 14:
        return "theta"
    if label == 16:
        return "beta"
    raise ValueError("square label outside 1..17")


def selected_directions() -> dict[tuple[int, int], tuple[tuple[str, int, str], ...]]:
    """Pair-order signs of the H-254 contacts and the extra 2/3 corner."""
    result: dict[tuple[int, int], tuple[tuple[str, int, str], ...]] = {}
    for index, (left, right, name, _) in enumerate(CONTACTS):
        pair = (min(left, right), max(left, right))
        axis = "v" if name == "w" else name
        sign = (-1 if name == "w" else 1) * (1 if left == pair[0] else -1)
        reason = "defining" if index < 17 else ("F1", "F2", "F3")[index - 17]
        result[pair] = ((axis, sign, reason),)
    result[2, 3] = ((EX, -1, "corner"), (EY, 1, "corner"))
    if len(result) != 21:
        raise ValueError("contact pair manifest is incomplete")
    return result


def option_manifest() -> tuple[dict[str, Any], ...]:
    selected = selected_directions()
    options: list[dict[str, Any]] = []
    for left, right in sorted(ZERO_PAIRS):
        wanted = {(axis, sign): reason for axis, sign, reason in selected[left, right]}
        for owner in (left, right):
            for axis in AXES[square_class(owner)]:
                for sign in (1, -1):
                    reason = wanted.get((axis, sign))
                    options.append(
                        {
                            "left": left,
                            "right": right,
                            "owner": owner,
                            "axis": axis,
                            "sign": sign,
                            "kind": "identity" if reason is not None else "strict_negative",
                            "reason": reason,
                        }
                    )
    if len(options) != 168 or sum(row["kind"] == "identity" for row in options) != 33:
        raise ValueError("unexpected owner-axis option roster")
    return tuple(options)


def active_wall_corners() -> tuple[dict[str, Any], ...]:
    """Four ordered corners per active incidence; never merge tied corners."""
    result: list[dict[str, Any]] = []
    for label, wall in ANCHORS:
        zeros = (
            {"left": (0, 3), "right": (1, 2), "bottom": (0, 1), "top": (2, 3)}[wall]
            if square_class(label) == "axis"
            else (3,)
        )
        result.extend(
            {
                "label": label,
                "wall": wall,
                "corner": corner,
                "kind": "identity" if corner in zeros else "strict_positive",
            }
            for corner in range(4)
        )
    if len(result) != 60 or sum(row["kind"] == "identity" for row in result) != 29:
        raise ValueError("unexpected active wall-corner roster")
    return tuple(result)


def _directed_gap(
    left: int,
    right: int,
    axis: str,
    sign: int,
    aux: dict[str, Any],
    *,
    centres: tuple[tuple[Any, Any], ...],
    symbolic: bool,
) -> Any:
    displacement = (
        centres[right - 1][0] - centres[left - 1][0],
        centres[right - 1][1] - centres[left - 1][1],
    )
    if symbolic:
        return (
            sign * _dot(aux[axis], displacement)
            - _support(left, axis, aux, sp.Rational(1, 2))
            - _support(right, axis, aux, sp.Rational(1, 2))
        )
    return (
        sign * _dot(aux[axis], displacement)
        - _support_interval(left, axis, aux)
        - _support_interval(right, axis, aux)
    )


def _corner(
    label: int, corner: int, aux: dict[str, Any], centres: tuple[tuple[Any, Any], ...]
) -> tuple[Any, Any]:
    axes = AXES[square_class(label)]
    first, second = aux[axes[0]], aux[axes[1]]
    signs = ((-1, -1), (1, -1), (1, 1), (-1, 1))
    a, b = signs[corner]
    x, y = centres[label - 1]
    half = Box.point(Q(1, 2)) if isinstance(x, Box) else sp.Rational(1, 2)
    return x + half * (a * first[0] + b * second[0]), y + half * (a * first[1] + b * second[1])


def _wall_corner_gap(
    label: int,
    wall: str,
    corner: int,
    side: Any,
    aux: dict[str, Any],
    *,
    centres: tuple[tuple[Any, Any], ...],
) -> Any:
    x, y = _corner(label, corner, aux, centres)
    return {"left": x, "right": side - x, "bottom": y, "top": side - y}[wall]


def _closing_functions(side: Any, aux: dict[str, Any]) -> dict[str, Any]:
    c, s, d, e = (aux[key] for key in ("c", "s", "d", "e"))
    return {
        "defining": 0,
        "corner": 0,
        "F1": c * (side - 3) + s * (side - 2) - 3,
        "F2": d * (side - aux["X"] - sp.Rational(3, 2))
        - e * (aux["Y"] - side + sp.Rational(3, 2))
        - 1,
        "F3": aux["alpha"] * (aux["A"] - sp.Rational(1, 2))
        + aux["gamma"] * (aux["B"] - sp.Rational(1, 2))
        - (c + 2 * s + 2),
    }


@lru_cache(maxsize=1)
def symbolic_zero_proofs() -> dict[str, Any]:
    """Replay every zero option and tied wall corner without a target sample."""
    foundation = symbolic_identities()
    t, b = sp.symbols("t b", real=True)
    side, aux, centres = _layout(t, b, sp.Rational(1, 2))
    closings = _closing_functions(side, aux)
    distinct: set[tuple[int, int, str, int]] = set()
    for row in option_manifest():
        if row["kind"] != "identity":
            continue
        key = row["left"], row["right"], row["axis"], row["sign"]
        if key in distinct:
            continue
        distinct.add(key)
        gap = _directed_gap(*key, aux, centres=centres, symbolic=True)
        if sp.cancel(gap - closings[row["reason"]]) != 0:
            raise ValueError(f"zero owner-axis identity failed: {key}")
    for row in active_wall_corners():
        if row["kind"] != "identity":
            continue
        gap = _wall_corner_gap(
            row["label"], row["wall"], row["corner"], side, aux, centres=centres
        )
        if sp.cancel(gap) != 0:
            raise ValueError(f"zero wall-corner identity failed: {row}")
    c, s = aux["c"], aux["s"]
    delta = c * (side - 3) - s - c * c
    offsets = {
        (1, 2): 0,
        (1, 3): 0,
        (5, 7): 0,
        (9, 10): delta,
        (9, 11): c * (1 - s),
        (10, 12): c * (1 - s),
        (11, 12): delta,
        (12, 14): c - s,
        (13, 14): delta + aux["T"] / 3,
    }
    if offsets.keys() != PARALLEL_PAIRS:
        raise ValueError("parallel offset manifest is incomplete")
    for (left, right), formula in offsets.items():
        tau = _tau({"left": left, "right": right}, aux, centres)
        if sp.cancel(tau - formula) != 0:
            raise ValueError(f"parallel tangential offset identity failed: {(left, right)}")
    return {
        "foundation": foundation,
        "pair_zero_options": 33,
        "pair_unique_identities": len(distinct),
        "wall_zero_corners": 29,
        "parallel_offset_identities": len(offsets),
    }


def _tau(row: dict[str, Any], aux: dict[str, Any], centres: tuple[tuple[Any, Any], ...]) -> Any:
    left, right = int(row["left"]), int(row["right"])
    axis, sign, _ = selected_directions()[left, right][0]
    normal = aux[axis]
    tangent = (-sign * normal[1], sign * normal[0])
    delta = (
        centres[right - 1][0] - centres[left - 1][0],
        centres[right - 1][1] - centres[left - 1][1],
    )
    return _dot(tangent, delta)


def validate_coverage(
    pair_options: list[dict[str, Any]], wall_corners: list[dict[str, Any]]
) -> None:
    expected_pairs = option_manifest()
    expected_walls = active_wall_corners()

    def pair_key(row: dict[str, Any]) -> tuple[Any, ...]:
        return row["left"], row["right"], row["owner"], row["axis"], row["sign"], row["kind"]

    def wall_key(row: dict[str, Any]) -> tuple[Any, ...]:
        return row["label"], row["wall"], row["corner"], row["kind"]

    for row in pair_options:
        if (
            any(type(row[key]) is not int for key in ("left", "right", "owner", "sign"))
            or type(row["axis"]) is not str
            or type(row["kind"]) is not str
        ):
            raise ValueError("malformed owner-axis coverage label")
    for row in wall_corners:
        if (
            type(row["label"]) is not int
            or type(row["corner"]) is not int
            or type(row["wall"]) is not str
            or type(row["kind"]) is not str
        ):
            raise ValueError("malformed wall-corner coverage label")

    if len(pair_options) != len(expected_pairs) or {pair_key(row) for row in pair_options} != {
        pair_key(row) for row in expected_pairs
    }:
        raise ValueError("incomplete or duplicate owner-axis coverage")
    if len(wall_corners) != len(expected_walls) or {wall_key(row) for row in wall_corners} != {
        wall_key(row) for row in expected_walls
    }:
        raise ValueError("incomplete or duplicate wall-corner coverage")


def interval_inventory(midpoint: tuple[Q, Q], radii: tuple[Q, Q]) -> dict[str, Any]:
    """Enclose strict features; identity rows rely on the caller's root proof."""
    if any(type(value) is not Q for value in (*midpoint, *radii)) or any(r <= 0 for r in radii):
        raise ValueError("invalid exact root enclosure")
    t, b = (
        Box(value - radius, value + radius)
        for value, radius in zip(midpoint, radii, strict=True)
    )
    side, aux, centres = _layout(t, b, Box.point(Q(1, 2)))
    for key in ("c", "s", "d", "e", "alpha", "gamma", "T"):
        if aux[key].lo <= 0:
            raise ValueError(f"unsupported sign branch: {key}")
    pair_rows: list[dict[str, Any]] = []
    failures: list[str] = []
    gap_cache: dict[tuple[int, int, str, int], Box] = {}
    for expected in option_manifest():
        row = expected.copy()
        key = row["left"], row["right"], row["axis"], row["sign"]
        if row["kind"] == "identity":
            row.update({"bound": ["0", "0"], "bound_scope": "certified_root", "passed": True})
        else:
            if key not in gap_cache:
                gap_cache[key] = _directed_gap(*key, aux, centres=centres, symbolic=False)
            gap = gap_cache[key]
            passed = gap.hi < 0
            row.update({"bound": gap.as_json(), "bound_scope": "whole_box", "passed": passed})
            if not passed:
                failures.append(f"pair.{key}")
        pair_rows.append(row)
    wall_rows: list[dict[str, Any]] = []
    for expected in active_wall_corners():
        row = expected.copy()
        if row["kind"] == "identity":
            row.update({"bound": ["0", "0"], "bound_scope": "certified_root", "passed": True})
        else:
            gap = _wall_corner_gap(
                row["label"], row["wall"], row["corner"], side, aux, centres=centres
            )
            passed = gap.lo > 0
            row.update({"bound": gap.as_json(), "bound_scope": "whole_box", "passed": passed})
            if not passed:
                failures.append(f"wall.{row['label']}.{row['wall']}.{row['corner']}")
        wall_rows.append(row)
    tau_rows: list[dict[str, Any]] = []
    for left, right in sorted(PARALLEL_PAIRS):
        tau = _tau({"left": left, "right": right}, aux, centres)
        passed = tau.lo > -1 and tau.hi < 1
        tau_rows.append(
            {
                "left": left,
                "right": right,
                "tau": tau.as_json(),
                "bound_scope": "whole_box",
                "passed": passed,
            }
        )
        if not passed:
            failures.append(f"parallel.{left}.{right}")
    validate_coverage(pair_rows, wall_rows)
    counts = {
        "pairs": len(ZERO_PAIRS),
        "pair_options": len(pair_rows),
        "pair_zero": sum(row["kind"] == "identity" for row in pair_rows),
        "pair_strict_negative": sum(row["kind"] == "strict_negative" for row in pair_rows),
        "active_wall_incidences": len(ANCHORS),
        "wall_corners": len(wall_rows),
        "wall_corner_zero": sum(row["kind"] == "identity" for row in wall_rows),
        "wall_corner_strict": sum(row["kind"] == "strict_positive" for row in wall_rows),
        "parallel_pairs": len(tau_rows),
    }
    if counts != EXPECTED_COUNTS:
        raise ValueError("feature count contract drifted")
    return {
        "schema": "n17-endpoint-features/v1",
        "box": {
            "midpoint": [_fraction_string(value) for value in midpoint],
            "inclusion_bounds": [_fraction_string(value) for value in radii],
        },
        "counts": counts,
        "pair_options": pair_rows,
        "wall_corners": wall_rows,
        "parallel_offsets": tau_rows,
        "feature_passed": not failures,
        "failures": failures,
    }


def _require_endpoint_accepted(
    document: dict[str, Any], root: dict[str, Any], source: bytes
) -> None:
    expected = {
        "walls": 68,
        "wall_identities": 15,
        "wall_strict": 53,
        "pairs": 136,
        "pair_identities": 21,
        "pair_strict": 115,
    }
    if (
        document.get("criterion_passed") is not True
        or document.get("geometry", {}).get("counts") != expected
        or document.get("root_certificate_git_ref") != FROZEN_ROOT_REF
        or document.get("source_sha256") != hashlib.sha256(source).hexdigest()
        or document.get("geometry", {}).get("box")
        != {
            "midpoint": root["box"]["midpoint"],
            "inclusion_bounds": root["inclusion_bounds"],
        }
    ):
        raise ValueError("frozen H-256 endpoint receipt is not accepted")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root_certificate", type=Path)
    parser.add_argument("endpoint_certificate", type=Path)
    parser.add_argument("--source", type=Path, default=SOURCE)
    args = parser.parse_args(argv)
    started = time.monotonic()
    try:
        # Both prerequisites are named by revision and path. The root's content is
        # decided by `check_root` and the endpoint receipt's by its acceptance check.
        require_retained_path(args.root_certificate, FROZEN_ROOT_REF)
        require_retained_path(args.endpoint_certificate, FROZEN_ENDPOINT_REF)
        source = _read_limited(args.source)
        root_raw = _read_limited(args.root_certificate)
        endpoint_raw = _read_limited(args.endpoint_certificate)
        root = json.loads(root_raw, object_pairs_hook=_object_unique)
        endpoint = json.loads(endpoint_raw, object_pairs_hook=_object_unique)
        root_receipt = check_root(root, source)
        _require_endpoint_accepted(endpoint, root, source)
        midpoint_values = root["box"]["midpoint"]
        inclusion_values = root["inclusion_bounds"]
        midpoint = (Q(midpoint_values[0]), Q(midpoint_values[1]))
        radii = (Q(inclusion_values[0]), Q(inclusion_values[1]))
        symbolic_started = time.monotonic()
        identities = symbolic_zero_proofs()
        symbolic_seconds = time.monotonic() - symbolic_started
        interval_started = time.monotonic()
        inventory = interval_inventory(midpoint, radii)
        interval_seconds = time.monotonic() - interval_started
        result = {
            "schema": "n17-endpoint-feature-certificate/v1",
            "root_git_ref": FROZEN_ROOT_REF,
            "endpoint_git_ref": FROZEN_ENDPOINT_REF,
            "source_sha256": hashlib.sha256(source).hexdigest(),
            "root_verification": root_receipt,
            "identities": identities,
            "inventory": inventory,
            "criterion_passed": inventory["feature_passed"],
            "timing_seconds": {
                "total": time.monotonic() - started,
                "symbolic": symbolic_seconds,
                "interval": interval_seconds,
            },
        }
        print(_encode_receipt(result))
        return 0 if result["criterion_passed"] else 1
    except (
        CertificateError,
        ValueError,
        OSError,
        KeyError,
        IndexError,
        TypeError,
        RecursionError,
    ) as error:
        print(
            json.dumps(
                {
                    "schema": "n17-endpoint-feature-certificate/v1",
                    "criterion_passed": False,
                    "error": str(error),
                },
                sort_keys=True,
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
