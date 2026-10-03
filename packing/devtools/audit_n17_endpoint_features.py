"""Independently audit the H257 endpoint-feature receipt.

This tool uses the earlier independent tuple-interval reconstruction, never the feature
producer. It checks all labeled owner options, active-wall corners and parallel offsets,
and recomputes every strict interval. The accepted H255 root, H256 packing, and reviewed
symbolic zero/normalization proofs remain explicit premises: this is not a standalone
root or symbolic-proof checker. Importing this module reads no target files.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path
from typing import Any, cast

from devtools import audit_n17_endpoint_receipt as exact

ENDPOINT_REF = f"ad7a36ed0:{exact.ENDPOINT_RUN}/certificate.json"
PARALLEL_PAIRS = {
    (1, 2),
    (1, 3),
    (5, 7),
    (9, 10),
    (9, 11),
    (10, 12),
    (11, 12),
    (12, 14),
    (13, 14),
}
COUNTS = {
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
SYMBOLIC_MANIFEST = {
    "foundation": {
        "wall_identities": 15,
        "pair_identities": 21,
        "normalizations": 3,
        "slider_identity": True,
    },
    "pair_zero_options": 33,
    "pair_unique_identities": 22,
    "wall_zero_corners": 29,
    "parallel_offset_identities": 9,
}


def basis_names(label: int) -> tuple[str, str]:
    exact.require(type(label) is int and 1 <= label <= 17, "invalid square label")
    if label == 16:
        return "p", "q"
    return ("u", "v") if 9 <= label <= 14 else ("ex", "ey")


def selected_normals() -> dict[tuple[int, int], list[tuple[str, int, str]]]:
    """Derive sorted-pair signs from the independently retained directed contacts."""
    result: dict[tuple[int, int], list[tuple[str, int, str]]] = {}
    for index, (start, end, direction) in enumerate(exact.CONTACTS):
        pair = min(start, end), max(start, end)
        axis = "v" if direction == "w" else direction
        sign = (-1 if direction == "w" else 1) * (1 if start < end else -1)
        reason = "defining" if index < 17 else ("F1", "F2", "F3")[index - 17]
        result[pair] = [(axis, sign, reason)]
    result[2, 3] = [("ex", -1, "corner"), ("ey", 1, "corner")]
    return result


def expected_options() -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for (left, right), normals in sorted(selected_normals().items()):
        identities = {(axis, sign): reason for axis, sign, reason in normals}
        for owner in (left, right):
            for axis, sign in itertools.product(basis_names(owner), (1, -1)):
                reason = identities.get((axis, sign))
                result.append(
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
    return result


def expected_corners() -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    # Corner order is (-,-), (+,-), (+,+), (-,+) in the square's own basis.
    edge_vertices = {"left": {0, 3}, "right": {1, 2}, "bottom": {0, 1}, "top": {2, 3}}
    for label, wall in sorted(exact.ANCHORS):
        touching = {3} if (label, wall) == (9, "left") else edge_vertices[wall]
        result.extend(
            {
                "label": label,
                "wall": wall,
                "corner": corner,
                "kind": "identity" if corner in touching else "strict_positive",
            }
            for corner in range(4)
        )
    return result


def corner_gap(layout: exact.Layout, label: int, wall: str, corner: int) -> exact.Interval:
    exact.require(type(corner) is int and corner in range(4), "invalid corner")
    first, second = (layout.axes[name] for name in basis_names(label))
    signs = ((-1, -1), (1, -1), (1, 1), (-1, 1))[corner]
    coordinates = tuple(
        exact.add(
            layout.centres[label][coordinate],
            exact.divide(
                exact.add(
                    exact.multiply(exact.point(signs[0]), first[coordinate]),
                    exact.multiply(exact.point(signs[1]), second[coordinate]),
                ),
                exact.point(2),
            ),
        )
        for coordinate in (0, 1)
    )
    exact.require(wall in ("left", "right", "bottom", "top"), "invalid wall")
    value = coordinates[0 if wall in ("left", "right") else 1]
    return exact.subtract(layout.side, value) if wall in ("right", "top") else value


def tangent_offset(layout: exact.Layout, left: int, right: int) -> exact.Interval:
    axis, sign, _ = selected_normals()[left, right][0]
    normal = layout.axes[axis]
    tangent = (
        exact.multiply(exact.point(-sign), normal[1]),
        exact.multiply(exact.point(sign), normal[0]),
    )
    return exact.dot(tangent, exact.difference(layout.centres[right], layout.centres[left]))


def pair_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return row["left"], row["right"], row["owner"], row["axis"], row["sign"]


def wall_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return row["label"], row["wall"], row["corner"]


def match_rows(
    rows: Any, expected: list[dict[str, Any]], *, pairs: bool
) -> list[dict[str, Any]]:
    exact.require(type(rows) is list and len(rows) == len(expected), "wrong feature row count")
    checked_rows = cast(list[dict[str, Any]], rows)
    key = pair_key if pairs else wall_key
    expected_by_key = {key(row): row for row in expected}
    seen: set[tuple[Any, ...]] = set()
    for row in checked_rows:
        exact.require(type(row) is dict, "feature row must be an object")
        item = key(row)
        exact.require(
            item in expected_by_key and item not in seen, "missing, extra or duplicate feature"
        )
        seen.add(item)
        wanted = expected_by_key[item]
        exact.require(
            set(row) == set(wanted) | {"bound", "bound_scope", "passed"}, "wrong feature fields"
        )
        exact.require(
            exact.exact_structure({name: row[name] for name in wanted}, wanted),
            "feature identity manifest differs",
        )
        identity = wanted["kind"] == "identity"
        exact.require(row["passed"] is True, "reported feature failed")
        exact.require(
            row["bound_scope"] == ("certified_root" if identity else "whole_box"),
            "wrong feature scope",
        )
        if identity:
            exact.require(row["bound"] == ["0", "0"], "identity bound differs")
    return checked_rows


def audit_inventory(inventory: dict[str, Any], layout: exact.Layout) -> dict[str, int]:
    exact.require(inventory["schema"] == "n17-endpoint-features/v1", "wrong feature schema")
    exact.require(
        inventory["feature_passed"] is True and inventory["failures"] == [],
        "feature inventory did not pass",
    )
    exact.require(exact.exact_structure(inventory["counts"], COUNTS), "feature counts differ")
    pairs = match_rows(inventory["pair_options"], expected_options(), pairs=True)
    corners = match_rows(inventory["wall_corners"], expected_corners(), pairs=False)
    cache: dict[tuple[int, int, str, int], exact.Interval] = {}
    for row in pairs:
        if row["kind"] == "identity":
            continue
        key = row["left"], row["right"], row["axis"], row["sign"]
        if key not in cache:
            cache[key] = layout.pair_gap(
                row["left"],
                row["right"],
                row["axis"],
                "forward" if row["sign"] == 1 else "reverse",
            )
        gap = cache[key]
        exact.match(gap, row["bound"], f"owner option {pair_key(row)}")
        exact.require(gap[1] < 0, "owner alternative is not strictly negative")
    for row in corners:
        if row["kind"] == "identity":
            continue
        gap = corner_gap(layout, row["label"], row["wall"], row["corner"])
        exact.match(gap, row["bound"], f"wall corner {wall_key(row)}", positive=True)
    raw_offsets = inventory["parallel_offsets"]
    exact.require(
        type(raw_offsets) is list and len(raw_offsets) == 9, "wrong parallel offset count"
    )
    offsets = cast(list[dict[str, Any]], raw_offsets)
    seen: set[tuple[int, int]] = set()
    for row in offsets:
        exact.require(
            set(row) == {"left", "right", "tau", "bound_scope", "passed"}, "wrong offset fields"
        )
        exact.require(
            type(row["left"]) is int and type(row["right"]) is int, "invalid parallel labels"
        )
        pair = row["left"], row["right"]
        exact.require(
            pair in PARALLEL_PAIRS and pair not in seen, "incomplete parallel coverage"
        )
        seen.add(pair)
        exact.require(
            row["passed"] is True and row["bound_scope"] == "whole_box",
            "wrong parallel scope or status",
        )
        tau = tangent_offset(layout, *pair)
        exact.match(tau, row["tau"], f"parallel offset {pair}")
        exact.require(-1 < tau[0] <= tau[1] < 1, "parallel face overlap is not strict")
    return {
        **COUNTS,
        "strict_interval_comparisons": 175,
        "distinct_negative_intervals_computed": len(cache),
    }


def audit(path: Path, repo: Path = exact.REPO) -> dict[str, Any]:
    started = time.monotonic()
    raw = exact.read_bytes(path)
    packet = exact.decode(raw)
    root_raw = exact.read_bytes(repo / exact.ROOT_RUN / "certificate.json")
    endpoint_raw = exact.read_bytes(repo / exact.ENDPOINT_RUN / "certificate.json")
    # The prerequisites are read from their retained paths and the packet must name
    # them by revision and path (below); their bytes are not compared with Git blobs.
    root, endpoint = exact.decode(root_raw), exact.decode(endpoint_raw)
    root_receipt = exact.decode(exact.read_bytes(repo / exact.ROOT_RUN / "checker.json"))
    exact.require(
        packet["schema"] == "n17-endpoint-feature-certificate/v1"
        and packet["criterion_passed"] is True,
        "feature certificate did not pass",
    )
    exact.require(
        packet["root_git_ref"] == exact.ROOT_REF and packet["endpoint_git_ref"] == ENDPOINT_REF,
        "wrong prerequisite references",
    )
    exact.require(
        packet["root_verification"] == root_receipt == endpoint["root_verification"],
        "root verification receipt differs",
    )
    exact.require(
        exact.exact_structure(packet["identities"], SYMBOLIC_MANIFEST),
        "reviewed symbolic completion manifest differs",
    )
    exact.require(
        endpoint["criterion_passed"] is True
        and exact.exact_structure(endpoint["geometry"]["counts"], exact.COUNTS),
        "accepted H256 prerequisite differs",
    )
    box = {"midpoint": root["box"]["midpoint"], "inclusion_bounds": root["inclusion_bounds"]}
    exact.require(
        packet["inventory"]["box"] == endpoint["geometry"]["box"] == box,
        "fixed root enclosure differs",
    )
    source = exact.read_bytes(repo / exact.SOURCE)
    # The one digest here that crosses a boundary: Kleddamag's downloaded release
    # against the value its review pinned (see `exact.SOURCE_SHA`).
    exact.require(
        hashlib.sha256(source).hexdigest()
        == packet["source_sha256"]
        == endpoint["source_sha256"]
        == root["source"]["sha256"]
        == exact.SOURCE_SHA,
        "source binding differs",
    )
    mid = [exact.rational(value) for value in box["midpoint"]]
    radii = [exact.rational(value) for value in box["inclusion_bounds"]]
    exact.require(
        len(mid) == len(radii) == 2 and all(radius > 0 for radius in radii),
        "invalid root enclosure",
    )
    t, b = [(m - radius, m + radius) for m, radius in zip(mid, radii, strict=True)]
    layout = exact.reconstruct(t, b)
    counts = audit_inventory(packet["inventory"], layout)
    return {
        "schema": "n17-endpoint-feature-audit/v1",
        "audit_passed": True,
        "counts": counts,
        "root_git_ref": exact.ROOT_REF,
        "endpoint_git_ref": ENDPOINT_REF,
        "audited_receipt_sha256": hashlib.sha256(raw).hexdigest(),
        "accepted_root_sha256": hashlib.sha256(root_raw).hexdigest(),
        "accepted_endpoint_sha256": hashlib.sha256(endpoint_raw).hexdigest(),
        "producer_imported_or_rerun": False,
        "trust_premises": [
            "accepted H255 root and H256 strict packing certificates",
            "reviewed symbolic zero, normalization and tangent-offset identities",
        ],
        "scope": (
            "all 175 strict interval records independently matched; "
            "symbolic identities audited as manifests, not reproved"
        ),
        "receipt_bytes": len(raw),
        "elapsed_seconds": time.monotonic() - started,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    try:
        result = audit(args.certificate)
    except (
        ValueError,
        OSError,
        KeyError,
        TypeError,
        IndexError,
        RecursionError,
    ) as error:
        print(json.dumps({"audit_passed": False, "error": str(error)}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
