"""Observe complete exact replay without changing its arithmetic or caches.

Use separate fresh processes for a matched uninstrumented run and a diagnostic run.
Callgraph timings include profiling overhead and are not speedup measurements. The
outer POSIX supervisor remains responsible for wall cleanup and sampled RSS limits.
"""

from __future__ import annotations

import argparse
import cProfile
import hashlib
import json
import math
import os
import platform
import re
import sys
import time
from collections import defaultdict
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, cast

from devtools import verify_n17_kernel_certificate as standing
from devtools.process_memory import current_memory_bytes, peak_memory_bytes
from devtools.provenance import provenance
from sqpack import retained_json

SCHEMA = "n17-exact-replay-profile/v1"
OUTPUT_LIMIT = 64 << 20
INPUT_LIMIT = 512 << 20
JSON_LIMIT = 10 << 20
ACCEPTED = {
    "PASS",
    "PASS_CLOSED",
    "PASS_STALL",
    "PASS_CONDITIONAL_CLOSED",
    "PASS_CONDITIONAL_STALL",
}


class IncompleteError(Exception):
    """A diagnostic lease or finite byte limit ended; no mathematical verdict."""


def require(condition: bool, message: str) -> None:  # noqa: FBT001
    if not condition:
        raise ValueError(message)


def bounded_size(path: Path, ceiling: int) -> None:
    if path.stat().st_size > ceiling:
        raise IncompleteError("profile input byte ceiling")


def tick(deadline: float) -> None:
    if time.monotonic() >= deadline:
        raise IncompleteError("exact replay profile wall ceiling")


def digest(path: Path, deadline: float, ceiling: int = INPUT_LIMIT) -> str:
    if path.stat().st_size > ceiling:
        raise IncompleteError("profile input byte ceiling")
    value = hashlib.sha256()
    consumed = 0
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            tick(deadline)
            consumed += len(block)
            if consumed > ceiling:
                raise IncompleteError("profile streamed input byte ceiling")
            value.update(block)
    tick(deadline)
    return value.hexdigest()


def cap_rational(token: str) -> Q:
    """Bound canonical integer/fraction syntax before allocating integers."""
    if (
        len(token) > 2500
        or re.fullmatch(r"(?:0|-?[1-9][0-9]*)(?:/[1-9][0-9]*)?", token) is None
    ):
        raise argparse.ArgumentTypeError("bounded canonical integer/fraction required")
    value = Q(token)
    if (
        max(abs(value.numerator).bit_length(), value.denominator.bit_length()) > 4096
        or str(value) != token
    ):
        raise argparse.ArgumentTypeError("canonical cap rational exceeds finite bound")
    return value


def result_payload(result: dict[str, Any]) -> dict[str, Any]:
    """Only timing, invocation and presentation provenance are omitted."""
    return {k: v for k, v in result.items() if k not in {"seconds", "provenance", "invocation"}}


def result_identity(result: dict[str, Any]) -> str:
    return hashlib.sha256(standing.canonical(result_payload(result))).hexdigest()


def memory_sample() -> dict[str, Any]:
    try:
        current = current_memory_bytes()
    except OSError as exc:
        return {"current_rss_bytes": None, "current_rss_error": str(exc)}
    return {"current_rss_bytes": current, "current_rss_error": None}


def memo_sizes(state: standing.State) -> dict[str, int]:
    covers = [r.cover for rows in state.rows.values() for r in rows if r.cover is not None]
    return {
        "facet_pairs": len(state.facets),
        "forbidden_pairs": len(state.forbidden),
        "admitted_row_covers": len(covers),
        "minimum_entries": sum(len(c.minima) for c in covers),
    }


class Recorder:
    """Low-frequency observers; original functions are always restored."""

    def __init__(self, deadline: float) -> None:
        self.deadline = deadline
        self.steps: list[dict[str, Any]] = []
        self.evictions: list[dict[str, Any]] = []

    @contextmanager
    def installed(self) -> Iterator[None]:
        check, bound = standing.check_step, standing.bound_memos

        def check_step(
            state: standing.State,
            step: dict[str, Any],
            si: int,
            node_id: Any,
            full: set[int],
        ) -> Any:
            tick(self.deadline)
            before = dict(state.stats)
            start = time.perf_counter()
            outcome = check(state, step, si, node_id, full)
            elapsed = time.perf_counter() - start
            tick(self.deadline)
            self.steps.append(
                {
                    "step": si,
                    "owner": step["owner"],
                    "rows_requested_in_full": len(full),
                    "check_step_wall_seconds": elapsed,
                    "counter_delta": {k: v - before.get(k, 0) for k, v in state.stats.items()},
                    "memo_sizes_after_row_checks": memo_sizes(state),
                    **memory_sample(),
                }
            )
            return outcome

        def bound_memos(
            state: standing.State, owner: int, before: list[standing.Point]
        ) -> None:
            old = memo_sizes(state)
            bound(state, owner, before)
            new = memo_sizes(state)
            self.evictions.append(
                {
                    "owner": owner,
                    "before": old,
                    "after": new,
                    "facet_pairs_evicted": old["facet_pairs"] - new["facet_pairs"],
                    "forbidden_pairs_evicted": old["forbidden_pairs"] - new["forbidden_pairs"],
                }
            )
            tick(self.deadline)

        standing.check_step, standing.bound_memos = check_step, bound_memos
        try:
            yield
        finally:
            standing.check_step, standing.bound_memos = check, bound


def phase(code: Any) -> str:  # noqa: PLR0911 - explicit diagnostic category inventory
    name, filename = code.co_name, code.co_filename
    if "fractions.py" in filename:
        return "rational_arithmetic"
    if any(p in filename for p in ("/json/", "/gzip.py", "/codecs.py")):
        return "decode_and_compression"
    if name in {"load_object", "_fill", "_value", "read_json", "digest", "seed_decode"}:
        return "intake_and_decode"
    if name in {"prepare", "extract", "state_from", "check_frame", "check_seed"}:
        return "premise_and_initialization"
    if name in {"difference", "difference_facets", "directions"}:
        return "facets"
    if name in {"minimum", "support"}:
        return "support_minima"
    if name in {
        "covered_by_sweep",
        "degenerate_covered",
        "sweep_events",
        "section_covered",
        "compile_edges",
    }:
        return "coverage"
    if name in {
        "clip_closed",
        "intersect_convex",
        "intersect_walls",
        "intersection",
        "closed_planes",
    }:
        return "intersections"
    if name in {"check_partners", "admit_cover", "core_strict", "quad_min_positive"}:
        return "partner_admission"
    if name in {"compress", "owned", "check_final", "check_centered_final", "derive_closure"}:
        return "ownership_and_final"
    return "other"


def callgraph(profile: cProfile.Profile) -> dict[str, Any]:
    entries = {e.code: e for e in profile.getstats() if not isinstance(e.code, str)}

    def calls(function: Any) -> int:
        entry = entries.get(function.__code__)
        return 0 if entry is None else entry.callcount

    def edge(caller: Any, callee: Any) -> int:
        entry = entries.get(caller.__code__)
        return (
            sum(c.callcount for c in (entry.calls or []) if c.code == callee.__code__)
            if entry is not None
            else 0
        )

    counts = {}
    for name, caller, callee in (
        ("facets", standing.State.difference, standing.difference_facets),
        ("support_minima", standing.CoverRow.minimum, standing.support),
        ("forbidden_regions", standing.State.forbidden_region, standing.minkowski_diff),
    ):
        total, misses = calls(caller), edge(caller, callee)
        if not 0 <= misses <= total:
            raise ValueError("profile cache callgraph is inconsistent")
        counts[name] = {"lookups": total, "misses": misses, "hits": total - misses}
    exclusive: dict[str, float] = defaultdict(float)
    functions = []
    for code, e in entries.items():
        exclusive[phase(code)] += e.inlinetime
        functions.append(
            {
                "file": code.co_filename,
                "line": code.co_firstlineno,
                "function": code.co_qualname,
                "calls": e.callcount,
                "recursive_calls": e.reccallcount,
                "exclusive_wall_seconds": e.inlinetime,
                "inclusive_wall_seconds": e.totaltime,
            }
        )
    return {
        "cache_counts": counts,
        "exclusive_phase_wall_seconds": dict(sorted(exclusive.items())),
        "functions": sorted(
            functions, key=lambda x: (-x["inclusive_wall_seconds"], x["file"], x["line"])
        )[:80],
        "call_count_semantics": "Python profiler calls; generator resumptions count as calls",
        "phase_semantics": (
            "exclusive Python-function time is partitioned; inclusive functions overlap; "
            "C builtins are not separately traced"
        ),
        "partner_cover_admissions": edge(standing.check_partners, standing.admit_cover),
    }


def profile_call(
    invoke: Callable[[], dict[str, Any]],
    *,
    instrumentation: str,
    deadline: float,
) -> dict[str, Any]:
    if instrumentation not in {"none", "phases", "callgraph"}:
        raise ValueError("unknown instrumentation")
    if sys.getprofile() is not None:
        raise ValueError("an existing profiler is active")
    observer = Recorder(deadline)
    profiler = cProfile.Profile(builtins=False)
    before = memory_sample()
    start, cpu = time.perf_counter(), time.process_time()
    if instrumentation == "callgraph":
        profiler.enable()
    result: dict[str, Any] | None = None
    incomplete = None
    try:
        if instrumentation == "none":
            result = invoke()
        else:
            with observer.installed():
                result = invoke()
        tick(deadline)
    except IncompleteError as exc:
        incomplete = str(exc)
    finally:
        profiler.disable()
    elapsed, cpu_elapsed = time.perf_counter() - start, time.process_time() - cpu
    graph = callgraph(profiler) if instrumentation == "callgraph" else None
    if graph is not None and result is not None and result.get("status") in ACCEPTED:
        lookups = result.get("counts", {}).get("partner_rows")
        if lookups is not None:
            misses = graph["partner_cover_admissions"]
            require(0 <= misses <= lookups, "partner cover cache counters differ")
            graph["cache_counts"]["partner_row_covers"] = {
                "lookups": lookups,
                "misses": misses,
                "hits": lookups - misses,
            }
    return {
        "schema": SCHEMA,
        "status": "INCOMPLETE"
        if incomplete
        else "COMPLETE"
        if result is not None
        and result.get("status") in ACCEPTED
        and result.get("mode") == "full"
        else "REFUSED",
        "error": incomplete,
        "instrumentation": instrumentation,
        "replay_wall_seconds": elapsed,
        "replay_cpu_seconds": cpu_elapsed,
        "verification_result": result,
        "mathematical_result_sha256": None if result is None else result_identity(result),
        "current_rss_start": before,
        "current_rss_end": memory_sample(),
        "process_lifetime_peak_rss_bytes": peak_memory_bytes(),
        "steps": observer.steps,
        "memo_evictions": observer.evictions,
        "callgraph": graph,
        "profile_overhead_is_not_gain": True,
        "scientific_admission_proved": False,
        "resource_assurance": (
            "boundary samples and cooperative deadlines; "
            "external owned-group wall/RSS supervisor required"
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--directory", type=Path)
    source.add_argument("--conditional-descriptor", type=Path)
    parser.add_argument("--cells", type=Path)
    parser.add_argument("--cells-sha256")
    parser.add_argument("--centered-inner-cap", type=cap_rational)
    parser.add_argument(
        "--instrumentation", choices=("none", "phases", "callgraph"), default="callgraph"
    )
    parser.add_argument("--max-seconds", type=float, default=300)
    parser.add_argument(
        "--compare", type=Path, help="previous fresh-process uninstrumented profile receipt"
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0:
        parser.error("max-seconds must be finite and positive")
    deadline = time.monotonic() + args.max_seconds
    total_start = time.perf_counter()
    try:
        paths = []
        if args.directory is not None:
            require(
                args.cells is not None and bool(args.cells_sha256),
                "explicit independently bound cells required",
            )
            cells_path = cast(Path, args.cells)
            bounded_size(cells_path, JSON_LIMIT)
            cells = standing.file_cells(cells_path, args.cells_sha256)
            container = (
                None
                if args.centered_inner_cap is None
                else standing.CenteredContainer(cells.cap, args.centered_inner_cap)
            )
            paths = [
                *args.directory.glob("seed-*.json.gz"),
                *args.directory.glob("node-*.json.gz"),
                cells_path,
            ]

            def invoke() -> dict[str, Any]:
                return standing.verify(args.directory, cells, container=container, sample=None)
        else:
            from devtools import (  # noqa: PLC0415 - conditional mode only
                verify_n17_conditional_owned_hull as conditional,
            )

            _, document = conditional.read_json(args.conditional_descriptor)
            paths = [args.conditional_descriptor]

            def invoke() -> dict[str, Any]:
                try:
                    return conditional.consume(document, deadline=deadline)
                except conditional.IncompleteError as exc:
                    raise IncompleteError(str(exc)) from exc

        inputs = {str(p): digest(p, deadline) for p in paths}
        pre_replay = time.perf_counter() - total_start
        report = profile_call(invoke, instrumentation=args.instrumentation, deadline=deadline)
        post_start = time.perf_counter()
        if report["status"] != "INCOMPLETE":
            require(
                inputs == {str(p): digest(p, deadline) for p in paths},
                "profile inputs changed during replay",
            )
            report["post_replay_input_recheck_complete"] = True
        else:
            report["post_replay_input_recheck_complete"] = False
        report["input_compressed_or_file_sha256"] = inputs
        report["pre_replay_intake_wall_seconds"] = pre_replay
        report["post_replay_custody_wall_seconds"] = time.perf_counter() - post_start
        if args.compare is not None:
            bounded_size(args.compare, OUTPUT_LIMIT)
            baseline = json.loads(args.compare.read_bytes())
            matched = (
                baseline["schema"] == SCHEMA
                and baseline["status"] == report["status"] == "COMPLETE"
                and baseline["instrumentation"] == "none"
                and baseline["input_compressed_or_file_sha256"] == inputs
                and baseline["mathematical_result_sha256"]
                == result_identity(baseline["verification_result"])
                == report["mathematical_result_sha256"]
            )
            report["matched_uninstrumented_baseline"] = matched
            if not matched:
                report["status"] = "REFUSED"
        report["provenance"] = provenance(Path(__file__), Path(standing.__file__))
        report["invocation"] = {
            "argv": list(sys.argv if argv is None else argv),
            "interpreter": sys.executable,
        }
        report["runtime"] = {
            "python": sys.version,
            "platform": platform.platform(),
            "pid": os.getpid(),
            "logical_cpus": os.cpu_count(),
            "load_average": list(os.getloadavg()) if hasattr(os, "getloadavg") else None,
            "single_worker": True,
        }
        report["total_wall_seconds_before_serialization"] = time.perf_counter() - total_start
        tick(deadline)
    except IncompleteError as exc:
        report = {
            "schema": SCHEMA,
            "status": "INCOMPLETE",
            "error": str(exc),
            "scientific_admission_proved": False,
        }
    except (
        OSError,
        EOFError,
        ValueError,
        KeyError,
        TypeError,
        standing.VerificationError,
    ) as exc:
        report = {
            "schema": SCHEMA,
            "status": "REFUSED",
            "error": str(exc),
            "scientific_admission_proved": False,
        }
    encoded = retained_json.dumps(report) + "\n"
    if time.monotonic() >= deadline or len(encoded.encode()) > OUTPUT_LIMIT:
        report = {
            "schema": SCHEMA,
            "status": "INCOMPLETE",
            "error": "profile final wall or output byte ceiling",
            "scientific_admission_proved": False,
        }
        encoded = retained_json.dumps(report) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(encoded)
    print(json.dumps({k: report.get(k) for k in ("schema", "status", "error")}))
    return 0 if report["status"] == "COMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
