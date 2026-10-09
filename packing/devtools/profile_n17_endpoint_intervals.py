"""Compare two existing interval types on four selected, byte-heavy expressions.

From packing/: python -m devtools.profile_n17_endpoint_intervals --out OUTPUT.json
The fixed AB/BA experiment is descriptive, not a full endpoint certificate or a
representative speedup. Box, Dyadic and the production geometry remain unchanged.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import argparse
import json
import time
from collections.abc import Callable
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from devtools.bounded_diagnostics import check_budget, write_json
from devtools.check_n17_contact_chart import SOURCE
from devtools.check_n17_core_stress import Dyadic
from devtools.check_n17_endpoint_feasibility import (
    FROZEN_ROOT_REF,
    Box,
    _directed_gap_interval,
    _fraction_string,
    _layout,
    _object_unique,
    _read_limited,
    _wall_gap_interval,
    require_retained_path,
)
from devtools.check_n17_root_certificate import check as check_root
from devtools.process_memory import peak_memory_bytes
from sqpack.hull_kernel.geometry import Budget, IncompleteError, require

ROOT = Path(__file__).resolve().parents[2]
ROOT_CERTIFICATE = ROOT / FROZEN_ROOT_REF.split(":", 1)[1]
FIXTURE = ("wall.9.right", "wall.16.top", "pair.9.16.ex.forward", "pair.13.16.ey.forward")
ORDER = ("exact", "dyadic", "dyadic", "exact")
SECONDS = 30
SCHEMA = "n17-selected-interval-profile/v1"


def disposition(value: Box) -> str:
    """A sign straddle is unresolved, never a rejected or proved inequality."""
    if value.lo > 0:
        return "positive"
    return "negative" if value.hi < 0 else "unresolved"


def check_enclosure(exact: Box, candidate: Box) -> None:
    require(candidate.lo <= exact.lo <= exact.hi <= candidate.hi, "interval was narrowed")
    require(disposition(exact) == disposition(candidate), "strict sign was lost")


def build_layout(backend: str, midpoint: tuple[Q, Q], radii: tuple[Q, Q]) -> tuple[Any, ...]:
    require(backend in ("exact", "dyadic"), "unknown backend")
    values = [
        Box(point - radius, point + radius)
        if backend == "exact"
        else Dyadic.enclose(point - radius, point + radius)
        for point, radius in zip(midpoint, radii, strict=True)
    ]
    half = Box.point(Q(1, 2)) if backend == "exact" else Dyadic.point(Q(1, 2))
    return _layout(values[0], values[1], half)


def query_layout(layout: tuple[Any, ...]) -> tuple[Box, ...]:
    side, aux, centres = layout
    return (
        _wall_gap_interval(9, "right", side, aux, centres),
        _wall_gap_interval(16, "top", side, aux, centres),
        _directed_gap_interval(9, 16, "ex", aux, centres, direction=1),
        _directed_gap_interval(13, 16, "ey", aux, centres, direction=1),
    )


def interval_stats(value: Any) -> dict[str, Any]:
    """Observe returned objects; this cannot inspect every internal intermediate."""
    intervals: list[Box] = []

    def visit(item: Any) -> None:
        if isinstance(item, Box):
            intervals.append(item)
        elif isinstance(item, dict):
            for entry in item.values():
                visit(entry)
        elif isinstance(item, (tuple, list)):
            for entry in item:
                visit(entry)

    visit(value)
    require(bool(intervals), "no returned interval objects")
    return {
        "interval_count": len(intervals),
        "types": sorted({type(item).__name__ for item in intervals}),
        "off_grid_endpoints": sum(
            (endpoint * 2**256).denominator != 1
            for item in intervals
            for endpoint in (item.lo, item.hi)
        ),
        "max_numerator_bits": max(
            abs(v).numerator.bit_length() for item in intervals for v in (item.lo, item.hi)
        ),
        "max_denominator_bits": max(
            v.denominator.bit_length() for item in intervals for v in (item.lo, item.hi)
        ),
    }


def timed[T](budget: Budget, operation: Callable[[], T]) -> tuple[T, float]:
    check_budget(budget, wall_message="selected interval profile time limit")
    started = time.perf_counter()
    result = operation()
    elapsed = time.perf_counter() - started
    check_budget(budget, wall_message="selected interval profile time limit")
    return result, elapsed


def run_pass(
    backend: str, midpoint: tuple[Q, Q], radii: tuple[Q, Q], budget: Budget
) -> tuple[dict[str, Any], tuple[Box, ...]]:
    layout, construction = timed(budget, lambda: build_layout(backend, midpoint, radii))
    values, query = timed(budget, lambda: query_layout(layout))
    expected_type = Box if backend == "exact" else Dyadic
    require(
        all(type(value) is expected_type for value in values), "unexpected support output type"
    )
    stats = interval_stats((layout, values))
    if backend == "dyadic":
        require(
            stats["types"] == ["Dyadic"] and stats["off_grid_endpoints"] == 0,
            "returned dyadic layout escaped its grid",
        )
        require(
            stats["max_denominator_bits"] <= 257, "returned dyadic denominator exceeded grid"
        )

    def serialize() -> list[dict[str, Any]]:
        return [
            {"ref": ref, "bound": [_fraction_string(value.lo), _fraction_string(value.hi)]}
            for ref, value in zip(FIXTURE, values, strict=True)
        ]

    def serialized_rows() -> tuple[list[dict[str, Any]], bytes]:
        rows = serialize()
        return rows, json.dumps(rows, sort_keys=True, separators=(",", ":")).encode("utf-8")

    (rows, raw), serialization = timed(budget, serialized_rows)
    return {
        "backend": backend,
        "seconds": {
            "construction": construction,
            "query": query,
            "serialization": serialization,
            "fresh_fixture_total": construction + query + serialization,
        },
        "serialized_bytes": len(raw),
        "rows": rows,
        "returned_objects": stats,
    }, values


def pair_gate(exact_seconds: float, dyadic_seconds: float) -> bool:
    return dyadic_seconds <= 0.8 * exact_seconds and exact_seconds - dyadic_seconds >= 0.1


def profile(
    midpoint: tuple[Q, Q],
    radii: tuple[Q, Q],
    budget: Budget,
    completed_passes: list[dict[str, Any]] | None = None,
    checkpoint: Path | None = None,
) -> dict[str, Any]:
    passes = [] if completed_passes is None else completed_passes
    values = []
    for backend in ORDER:
        receipt, outputs = run_pass(backend, midpoint, radii, budget)
        passes.append(receipt)
        values.append(outputs)
        if checkpoint is not None:
            write_json(
                checkpoint,
                {
                    "schema": SCHEMA,
                    "status": "IN_PROGRESS_UNACCEPTED",
                    "completed_passes": passes,
                    "partial_evidence_accepted": False,
                    "selected_fixture_adoption_interest": False,
                },
            )
    gates = []
    for exact_index, dyadic_index in ((0, 1), (3, 2)):
        for exact, dyadic in zip(values[exact_index], values[dyadic_index], strict=True):
            check_enclosure(exact, dyadic)
            require(
                disposition(exact) == "positive", "fixed fixture lost its strict positive sign"
            )
        gates.append(
            pair_gate(
                passes[exact_index]["seconds"]["fresh_fixture_total"],
                passes[dyadic_index]["seconds"]["fresh_fixture_total"],
            )
        )
    require(
        passes[0]["rows"] == passes[3]["rows"] and passes[1]["rows"] == passes[2]["rows"],
        "fresh pass bounds differ",
    )
    check_budget(budget, wall_message="selected interval profile time limit")
    return {
        "schema": SCHEMA,
        "status": "PASS_SELECTED_ENCLOSURE_AND_SIGNS",
        "fixture": list(FIXTURE),
        "order": list(ORDER),
        "passes": passes,
        "first_use_indices": [0, 1],
        "pair_performance_gates": gates,
        "selected_fixture_adoption_interest": all(gates),
        "timing_scope": (
            "Fresh-object construction/query/compact-bound serialization only; guards, "
            "object inspection and inclusion checks are separate. Only passes 0/1 "
            "are first-use. Common imports precede the in-process timer; Job wall includes them"
        ),
        "scope": (
            "Four deliberately byte-heavy expressions; not a representative/full "
            "endpoint result or production adoption"
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root-certificate", type=Path, default=ROOT_CERTIFICATE)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.out.exists():
        parser.error("output must not exist; retained evidence is never overwritten")
    started = time.monotonic()
    budget = Budget(started + SECONDS, 0)
    completed_passes: list[dict[str, Any]] = []
    try:

        def inputs() -> tuple[dict[str, Any], dict[str, Any]]:
            require_retained_path(args.root_certificate, FROZEN_ROOT_REF)
            root = json.loads(
                _read_limited(args.root_certificate), object_pairs_hook=_object_unique
            )
            return root, check_root(root, _read_limited(args.source))

        (root, root_check), loading = timed(budget, inputs)
        midpoint = tuple(Q(value) for value in root["box"]["midpoint"])
        radii = tuple(Q(value) for value in root["inclusion_bounds"])
        require(len(midpoint) == len(radii) == 2, "invalid root box dimension")
        packet = profile(
            (midpoint[0], midpoint[1]), (radii[0], radii[1]), budget, completed_passes, args.out
        )
        packet.update(
            {
                "common_loading_root_seconds": loading,
                "root_verification": root_check,
                "wall_seconds": time.monotonic() - started,
                "lifetime_peak_bytes": peak_memory_bytes(),
                "limits": {
                    "protocol_seconds": SECONDS,
                    "worker_current_rss_bytes": 512 * 1024**2,
                },
                "input_paths": {"root": str(args.root_certificate), "source": str(args.source)},
            }
        )
        write_json(args.out, packet)
    except (IncompleteError, ValueError, OSError) as error:
        write_json(
            args.out,
            {
                "schema": SCHEMA,
                "status": "INCOMPLETE_OR_REFUSED",
                "error": str(error),
                "completed_passes": completed_passes,
                "partial_evidence_accepted": False,
                "selected_fixture_adoption_interest": False,
            },
        )
        print(f"INCOMPLETE_OR_REFUSED: {error}")
        return 2
    print(
        f"{packet['status']}; selected fixture "
        f"interest={packet['selected_fixture_adoption_interest']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
