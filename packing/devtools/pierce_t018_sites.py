#!/usr/bin/env python3
"""M3 kill-test: integral piercing of the T-018 sites at side 19/5.

Default is encode-ready, not a search. ``--search`` runs a HiGHS set-cover MIP
with integrality on site indicators. A coarse-net optimum ≥ 12 is
``killed_coarse_net``; a feasible 11-set is ``eleven_candidate``. Timeout and
non-infeasible solver failures are unresolved. The float LP relaxation is never
solved and is not a verdict.

``--check`` loads T-018, reports the unique site count, and writes nothing.
``--certify`` (off by default) may call ``cases.green17.interval_audit.certify``
on an 11-or-fewer incumbent; that path is optional because it can be slow and
because some T-018 coordinates are not exact at the audit's pose scale.

Usage, from ``packing/``:

    uv run --frozen --all-extras --group dev python -m devtools.pierce_t018_sites --check
    uv run --frozen --all-extras --group dev python -m devtools.pierce_t018_sites \\
        --side 19/5 --direction-steps 36 --time-limit-s 30 --output-dir DIR
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
import time
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from cases.green17.interval_audit import IntervalAuditError, certify
from sqpack.fractional.integral_piercing import (
    CANDIDATE_CARDINALITY,
    DEFAULT_ANGLE_LIMIT,
    DEFAULT_DIRECTION_STEPS,
    DEFAULT_SIDE,
    DEFAULT_SQUARE_SIDE,
    CoverEncodingTimeoutError,
    M3Verdict,
    PiercingError,
    Point,
    SearchStatus,
    encode_event_cell_covers,
    geometry_fields,
    load_unique_sites,
    m3_verdict_for,
    sites_inside_container,
    solve_integral_set_cover,
    t018_certificate_path,
)
from sqpack.project import require_project_root

RECEIPT_NAME = "pierce-t018-receipt.json"
SELFTEST_DIRECTION_STEPS = 4
SELFTEST_TIME_LIMIT_S = 20.0


def _point_strings(points: Sequence[Point]) -> list[list[str]]:
    return [[str(x), str(y)] for x, y in points]


def _certificate_field(certificate: Path) -> str:
    """Repository-relative when the file sits in this checkout; otherwise the given path."""

    resolved = certificate.resolve()
    packing = require_project_root().resolve()
    for root in (packing.parent, packing):
        try:
            relative = resolved.relative_to(root).as_posix()
        except ValueError:
            continue
        if root == packing:
            return f"packing/{relative}"
        return relative
    return certificate.as_posix()


def _write_receipt(path: Path, record: dict[str, Any]) -> None:
    protected = t018_certificate_path().resolve()
    if path.resolve() == protected:
        raise PiercingError("receipt output may not overwrite the T-018 certificate")
    atomic_write_text(path, json.dumps(record, indent=2) + "\n", make_parents=True)


def _maybe_certify(points: Sequence[Point], side: Fraction, *, enabled: bool) -> dict[str, Any]:
    if not enabled:
        return {"ran": False, "certified": None, "error": None}
    try:
        stats = certify(side=side, points=list(points))
    except (IntervalAuditError, ValueError) as error:
        return {"ran": True, "certified": False, "error": str(error)}
    return {
        "ran": True,
        "certified": True,
        "error": None,
        "boxes": stats.boxes,
        "max_depth": stats.max_depth,
    }


def check_sites(certificate: Path) -> tuple[int, tuple[Point, ...]]:
    sites = load_unique_sites(certificate)
    return len(sites), sites


def build_receipt(
    *,
    certificate: Path,
    side: Fraction,
    square_side: Fraction,
    angle_limit: Fraction,
    direction_steps: int,
    time_limit_s: float,
    search: bool,
    certify: bool,
) -> dict[str, Any]:
    all_sites = load_unique_sites(certificate)
    sites = sites_inside_container(all_sites, side)
    record: dict[str, Any] = {
        "kind": "t018_integral_piercing_receipt",
        "schema": "packing.squares:T018IntegralPiercing/v1",
        "side": str(side),
        **geometry_fields(square_side),
        "angle_limit": str(angle_limit),
        "direction_steps": direction_steps,
        "direction_count": direction_steps + 1,
        "unique_sites": len(all_sites),
        "sites_in_container": len(sites),
        "certificate": _certificate_field(certificate),
        "optimizer_ran": False,
        "search_status": SearchStatus.encoding_ready.value,
        "piercing": None,
        "m3_verdict": M3Verdict.unresolved.value,
        "selected_sites": None,
        "reachable_cells": None,
        "cover_rows": None,
        "truncated_rows": False,
        "float_lp_used": False,
        "time_limit_s": time_limit_s,
        "interval_audit": {"ran": False, "certified": None, "error": None},
        "scope": (
            "A coarse-net IP optimum is a kill-test measurement, not a verified "
            "s(11) movement. A float LP relaxation is not a verdict."
        ),
        "message": "search not requested; receipt is encoding-ready",
    }
    if not search:
        return record
    if not sites:
        raise PiercingError("no T-018 sites lie in the container")
    deadline = time.monotonic() + time_limit_s
    try:
        encoding = encode_event_cell_covers(
            sites,
            outer_side=side,
            square_side=square_side,
            angle_limit=angle_limit,
            direction_steps=direction_steps,
            deadline_monotonic=deadline,
        )
    except CoverEncodingTimeoutError:
        record["search_status"] = SearchStatus.timeout.value
        record["m3_verdict"] = M3Verdict.unresolved.value
        record["message"] = "event-cell encoding hit the time limit; timeout is unresolved"
        return record
    record["reachable_cells"] = encoding.reachable_cells
    record["cover_rows"] = int(encoding.rows.shape[0])
    record["truncated_rows"] = encoding.truncated
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        record["search_status"] = SearchStatus.timeout.value
        record["m3_verdict"] = M3Verdict.unresolved.value
        record["optimizer_ran"] = False
        record["message"] = "encoding consumed the wall; timeout is unresolved"
        return record
    outcome = solve_integral_set_cover(encoding.rows, time_limit_s=remaining)
    verdict = m3_verdict_for(
        outcome.search_status, outcome.piercing, truncated=encoding.truncated
    )
    selected: list[list[str]] | None = None
    if outcome.selected is not None:
        selected = _point_strings([sites[index] for index in outcome.selected])
    record.update(
        {
            "optimizer_ran": outcome.optimizer_ran,
            "search_status": outcome.search_status.value,
            "piercing": outcome.piercing,
            "m3_verdict": verdict.value,
            "selected_sites": selected,
            "reachable_cells": encoding.reachable_cells,
            "cover_rows": int(encoding.rows.shape[0]),
            "truncated_rows": encoding.truncated,
            "message": outcome.message,
        }
    )
    if (
        certify
        and verdict is M3Verdict.eleven_candidate
        and outcome.selected is not None
        and outcome.piercing is not None
        and outcome.piercing <= CANDIDATE_CARDINALITY
    ):
        points = tuple(sites[index] for index in outcome.selected)
        record["interval_audit"] = _maybe_certify(points, side, enabled=True)
    return record


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        allow_abbrev=False,
    )
    command.add_argument(
        "--check",
        action="store_true",
        help="load T-018 sites, report the unique count, write nothing",
    )
    command.add_argument(
        "--search",
        action="store_true",
        help="run the integral set-cover MIP; default is off",
    )
    command.add_argument(
        "--certify",
        action="store_true",
        help="call interval_audit.certify on an 11-candidate (default off)",
    )
    command.add_argument(
        "--selftest",
        action="store_true",
        help="load T-018 and run a 5-direction, 20s coarse-net search",
    )
    command.add_argument("--side", type=Fraction, default=DEFAULT_SIDE)
    command.add_argument("--square-side", type=Fraction, default=DEFAULT_SQUARE_SIDE)
    command.add_argument("--angle-limit", type=Fraction, default=DEFAULT_ANGLE_LIMIT)
    command.add_argument(
        "--direction-steps",
        type=int,
        default=DEFAULT_DIRECTION_STEPS,
        help="steps up to the angle limit; N steps is an (N+1)-direction net",
    )
    command.add_argument("--time-limit-s", type=float, default=30.0)
    command.add_argument("--output-dir", type=Path, default=None)
    command.add_argument(
        "--certificate",
        type=Path,
        default=None,
        help="atom JSON; default is the frozen T-018 certificate",
    )
    return command


def _run(args: argparse.Namespace) -> int:
    certificate = (
        args.certificate.resolve() if args.certificate is not None else t018_certificate_path()
    )
    if args.check and not args.selftest:
        count, _sites = check_sites(certificate)
        print(f"T-018 unique sites: {count}")
        return 0
    direction_steps = args.direction_steps
    time_limit_s = args.time_limit_s
    search = args.search
    output_dir = args.output_dir
    if args.selftest:
        search = True
        direction_steps = SELFTEST_DIRECTION_STEPS
        time_limit_s = SELFTEST_TIME_LIMIT_S
        count, _sites = check_sites(certificate)
        print(f"T-018 unique sites: {count}")
        print(
            f"selftest coarse net: {direction_steps + 1} directions, time-limit {time_limit_s}s"
        )
        if output_dir is None:
            output_dir = Path(tempfile.mkdtemp(prefix="pierce-t018-selftest-"))
    if output_dir is None:
        parser().error("--output-dir is required unless --check")
    record = build_receipt(
        certificate=certificate,
        side=args.side,
        square_side=args.square_side,
        angle_limit=args.angle_limit,
        direction_steps=direction_steps,
        time_limit_s=time_limit_s,
        search=search,
        certify=args.certify,
    )
    path = output_dir / RECEIPT_NAME
    _write_receipt(path, record)
    print(
        f"{path}: piercing={record['piercing']} "
        f"status={record['search_status']} verdict={record['m3_verdict']}"
    )
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    try:
        return _run(parser().parse_args(argv))
    except (PiercingError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
