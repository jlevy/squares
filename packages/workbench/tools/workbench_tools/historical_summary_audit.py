"""Inventory retained annealing cells without upgrading summaries into trial evidence."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def _object(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise ValueError(f"{label} must be an object with string keys")
    return dict(value)


def _number(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{label} must be numeric")
    try:
        result = float(value)
    except OverflowError as error:
        raise ValueError(f"{label} must be finite") from error
    if not math.isfinite(result):
        raise ValueError(f"{label} must be finite")
    return result


def audit(value: object) -> dict[str, object]:
    """Retain file/cell identity and resolved flags; missing parameters stay missing."""
    files = _object(value, "summaries")
    cells: list[dict[str, object]] = []
    counts: list[int] = []
    for filename, contents in sorted(files.items()):
        for size, raw in sorted(
            _object(contents, filename).items(), key=lambda row: int(row[0])
        ):
            row = _object(raw, f"{filename}/{size}")
            n = int(size)
            if n < 1:
                raise ValueError("square counts must be positive")
            count = row.get("trials")
            if isinstance(count, bool) or not isinstance(count, int) or count < 0:
                raise ValueError("trial counts must be nonnegative integers")
            resolved = row.get("resolved")
            if not isinstance(resolved, bool):
                raise TypeError("resolved must be an explicit boolean")
            reference = _number(row.get("record"), "record")
            grid = _number(row.get("grid"), "grid")
            if reference <= 0 or grid <= 0:
                raise ValueError("reference and grid must be positive")
            closed = _number(row.get("closed_median"), "closed_median")
            absolute = (grid - reference) * (1 - closed)
            params = _object(row.get("params"), "params")
            for parameter, number in params.items():
                _number(number, parameter)
            best = _object(row.get("best_of"), "best_of")
            for prefix, number in best.items():
                if int(prefix) < 1 or int(prefix) > count:
                    raise ValueError("best-of prefix must fit the retained cell count")
                _number(number, prefix)
            cells.append(
                {
                    "artifact": filename,
                    "n": n,
                    "recorded_rows": count,
                    "resolved_flag": resolved,
                    "parameter_overrides": params,
                    "reference_side": reference,
                    "grid_side": grid,
                    "median_grid_gap_closed": closed,
                    "reconstructed_median_absolute_excess": absolute,
                    "reconstructed_median_relative_excess_pct": absolute / reference * 100,
                    "prefix_observations": best,
                }
            )
            counts.append(n)
    return {
        "schema": "squares.workbench.historical-summary-audit/v1",
        "evidence": "historical summaries; raw geometry and seed blocks unavailable",
        "count_semantics": "recorded rows per file, without a claim of unique trials",
        "reconstruction": "excess derived from rounded stored closed/reference/grid values",
        "file_count": len(files),
        "cell_count": len(cells),
        "largest_recorded_n": max(counts) if counts else None,
        "cells": cells,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("summaries", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    output = audit(json.loads(args.summaries.read_text(encoding="utf-8")))
    args.out.write_text(json.dumps(output, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
