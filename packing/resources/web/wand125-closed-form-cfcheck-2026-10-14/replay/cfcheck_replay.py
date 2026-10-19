#!/usr/bin/env python3
"""Price, run and control wand125's cfcheck on intervals 1 and 34 of the closed form.

cfcheck is the source's second checker of the closed-form certificate, retained in this
packet at ``square-packing/problems/closed-form/indep-checker/``. This program does not
check anything about the certificate itself. It has four commands:

- ``plan`` reads one region record of a release asset and reports how many leaves, of
  which kinds, the first N roots hold, and what the source's own timings predict they
  cost: the stated sample is chosen by it before anything runs.
- ``price`` reads the source's two cfcheck receipts and ``intervals.json`` and prices a
  complete replay of intervals 1 and 34 in worker-hours, filling the leaves the source
  resumed from checkpoints (and so did not time) at the source's own per-kind rates. With
  ``--calibration`` it also reads run receipts written by ``run`` and scales the price to
  this host by the ratio of the time measured here to the source's time for the same
  leaves.
- ``run`` runs one cfcheck command from a working directory, measures its wall time and,
  through ``getrusage``, its CPU time, and writes a receipt with the binary's digest, the
  exit code, the final verdict line and a summary of cfcheck's JSON report, which it
  keeps beside the receipt byte for byte.
- ``mutate`` writes a mutated copy of one interval's asset directory and of
  ``intervals.json``, re-sealed: ``SHA256SUMS``, the interval's digests and its
  published counts are rewritten to match the mutation, so that only the check the
  mutation targets can refuse it. ``duplicate-root`` appends a copy of one root line to
  a record; ``relabel-leaf`` changes the named test of one leaf; ``scale-family``
  multiplies every mass and density of both families by 99/100.

Every path given to cfcheck is relative to the working directory, as cfcheck requires.
Run from ``packing/`` with the project interpreter; the packet README gives the commands.
"""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import os
import platform
import resource
import shutil
import subprocess
import sys
import time
from collections import Counter
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
WEB = PACKET.parent
CHECKER = PACKET / "square-packing/problems/closed-form/indep-checker"
SOURCE_RECEIPTS = {
    1: CHECKER / "receipts/interval_0_0.02.json",
    34: CHECKER / "receipts/interval_0.99_1.json",
}
FOLDER_9A28A84 = WEB / "wand125-closed-form-2026-10-14/square-packing/problems/closed-form"
INTERVALS_GZ = FOLDER_9A28A84 / "intervals.json.gz"
REPLAY4D_PUBLISHED = FOLDER_9A28A84 / "receipts/published_checker.json"
REPLAY4D_FULL = FOLDER_9A28A84 / "receipts/replay.json.gz"
ASSETS = {1: "interval_0_0.02.tar.gz", 34: "interval_0.99_1.tar.gz"}
COUNTS_TSV = WEB / "wand125-closed-form-2026-10-14/evaluation/outputs/counts.tsv"
INTERVALS_SHA256 = "a91b0b49988bc5bf8977d1e9f61e2930e2cb1be136bd4ff3140b5ee263591c0c"
REGIONS = ("straddle", "left", "top", "right")
HOUR = 3600.0

type Json = dict[str, Any]


def emit(line: str) -> None:
    sys.stdout.write(line + "\n")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> Json:
    data: Json = json.loads(path.read_text(encoding="utf-8"))
    return data


def load_intervals(path: Path | None) -> Json:
    """The certificate's intervals.json: the given file, or the retained gzip copy."""
    raw = path.read_bytes() if path is not None else gzip.decompress(INTERVALS_GZ.read_bytes())
    if hashlib.sha256(raw).hexdigest() != INTERVALS_SHA256:
        msg = "intervals.json is not the published bytes"
        raise SystemExit(msg)
    data: Json = json.loads(raw)
    return data


def interval_entry(intervals: Json, index: int) -> Json:
    entry: Json = intervals["intervals"][index - 1]
    if entry["index"] != index:
        msg = f"interval {index} is not at position {index}"
        raise SystemExit(msg)
    return entry


def now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


# ------------------------------------------------------------------------ source rates


def source_rates(receipt: Json) -> dict[str, dict[str, tuple[int, float]]]:
    """Per region, per leaf kind: (timed leaves, summed seconds) from a cfcheck report."""
    out: dict[str, dict[str, tuple[int, float]]] = {}
    for name, region in receipt["details"]["regions"].items():
        out[name] = {
            kind: (int(row["leaves"]), float(row["seconds"]))
            for kind, row in region["leaf_timing"].items()
        }
    return out


def pooled(rates: dict[str, dict[str, tuple[int, float]]]) -> dict[str, float]:
    """Seconds per leaf of each kind, weighted across the regions that timed it."""
    total: dict[str, list[float]] = {}
    for region in rates.values():
        for kind, (leaves, seconds) in region.items():
            acc = total.setdefault(kind, [0.0, 0.0])
            acc[0] += leaves
            acc[1] += seconds
    return {kind: s / n for kind, (n, s) in total.items() if n}


def all_source_rates() -> tuple[
    dict[int, dict[str, dict[str, tuple[int, float]]]], dict[int, dict[str, float]]
]:
    per_region = {
        index: source_rates(load_json(path)) for index, path in SOURCE_RECEIPTS.items()
    }
    per_interval = {index: pooled(rates) for index, rates in per_region.items()}
    return per_region, per_interval


def rate_for(
    index: int,
    region: str,
    kind: str,
    per_region: dict[int, dict[str, dict[str, tuple[int, float]]]],
    per_interval: dict[int, dict[str, float]],
) -> tuple[float | None, str]:
    """The source's seconds per leaf for a kind, and where the rate came from."""
    timed = per_region[index].get(region, {}).get(kind)
    if timed and timed[0]:
        return timed[1] / timed[0], "this region"
    if kind in per_interval[index]:
        return per_interval[index][kind], "this interval, pooled"
    other = 1 if index == 34 else 34
    if kind in per_interval[other]:
        return per_interval[other][kind], f"interval {other}, pooled"
    return None, "unmeasured"


def receipt_custody(intervals: Json, index: int) -> Json:
    """Whether a source receipt names the published bytes and counts of its interval.

    Every input digest the report lists for a family, a record or intervals.json must be
    the published one, and its roots, leaves and leaf kinds the published totals.
    """
    entry = interval_entry(intervals, index)
    receipt = load_json(SOURCE_RECEIPTS[index])
    published = {
        "intervals.json": INTERVALS_SHA256,
        "family.json": entry["family_sha256"],
        "family_right.json": entry["family_right_sha256"],
    } | {f"{name}.rec": entry["regions"][name]["sha256"] for name in REGIONS}
    seen: dict[str, set[str]] = {}
    for item in receipt["inputs"]:
        name = Path(item["path"]).name
        if name in published:
            seen.setdefault(name, set()).add(item["sha256"])
    kinds: Counter[str] = Counter()
    for name in REGIONS:
        kinds.update(entry["regions"][name]["leaf_kinds"])
    return {
        "receipt_sha256": sha256(SOURCE_RECEIPTS[index]),
        "inputs_named": sorted(seen),
        "every_input_is_published": set(seen) == set(published)
        and all(digests == {published[n]} for n, digests in seen.items()),
        "roots_published": receipt["roots"]
        == sum(entry["regions"][n]["roots"] for n in REGIONS),
        "leaves_published": receipt["leaves"]
        == sum(entry["regions"][n]["leaves"] for n in REGIONS),
        "leaf_kinds_published": receipt["leaf_kinds"] == dict(kinds),
        "checked_leaf_kinds_equal_leaf_kinds": receipt["checked_leaf_kinds"]
        == receipt["leaf_kinds"],
        "ok_complete": receipt["ok"]
        and not receipt["partial"]
        and not receipt["incomplete"]
        and not receipt["refusals"]
        and not receipt["interruptions"],
        "resumed_roots": receipt["resumed_roots"],
    }


def replay4d_hours() -> dict[tuple[int, str], float]:
    """replay4d's CPU-hours per record of intervals 1 and 34, as the source recorded them."""
    runs: list[Json] = load_json(REPLAY4D_PUBLISHED)["runs"]
    by_asset = {asset: index for index, asset in ASSETS.items()}
    return {(by_asset[r["asset"]], r["region"]): float(r["cpu_hours"]) for r in runs}


# ------------------------------------------------------------------------------- counts


def command_counts(args: argparse.Namespace) -> int:
    """The counts whose a(N) is attained on the given intervals, from counts.tsv.

    At a count N the bound s(N) >= a(N) rests on the interval where a(N) is attained: the
    supremum is approached by deltas in that interval alone (or is its closed right end,
    where a(N) is the cap k + d1), so a complete check of that interval's family and four
    records completes the computational part of the bound at N. The interval at each
    count is the one the 9a28a84 packet's evaluation recorded (evaluation/outputs).
    """
    wanted = set(args.intervals)
    with COUNTS_TSV.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    chosen = [r for r in rows if int(r["interval"]) in wanted]
    relations: dict[str, Counter[str]] = {
        lane: Counter(r[f"rel_{lane}"] for r in chosen)
        for lane in ("reported_lb", "verified_lb", "verified_ub")
    }
    out = {
        "schema": "cfcheck-interval-counts/v1",
        "source": COUNTS_TSV.relative_to(WEB.parents[2]).as_posix(),
        "intervals": sorted(wanted),
        "counts": [
            {
                "n": int(r["n"]),
                "interval": int(r["interval"]),
                "form": r["form"],
                "a_floor_15": r["a_floor_15"],
                "rel_reported_lb": r["rel_reported_lb"],
                "rel_verified_lb": r["rel_verified_lb"],
                "case_status": r["case_status"],
            }
            for r in chosen
        ],
        "relations": {lane: dict(sorted(c.items())) for lane, c in relations.items()},
        "of_counts": len(rows),
    }
    text = json.dumps(out, indent=1)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    emit(text)
    return 0


# --------------------------------------------------------------------------------- plan


def first_roots(record: Path, count: int) -> tuple[int, Counter[str]]:
    roots, kinds = 0, Counter[str]()
    with record.open("rb") as handle:
        for line in handle:
            if roots == count:
                break
            row: Json = json.loads(line)
            if "header" in row:
                continue
            roots += 1
            kinds.update(kind for _, kind in row["leaves"])
    return roots, kinds


def command_plan(args: argparse.Namespace) -> int:
    per_region, per_interval = all_source_rates()
    roots, kinds = first_roots(args.record, args.roots)
    predicted = 0.0
    unmeasured: list[str] = []
    rows: list[Json] = []
    for kind, n in sorted(kinds.items()):
        rate, origin = rate_for(args.index, args.region, kind, per_region, per_interval)
        if rate is None:
            unmeasured.append(kind)
        else:
            predicted += n * rate
        rows.append(
            {"kind": kind, "leaves": n, "source_seconds_per_leaf": rate, "rate_from": origin}
        )
    plan = {
        "schema": "cfcheck-sample-plan/v1",
        "record": args.record.name,
        "interval": args.index,
        "region": args.region,
        "first_roots": roots,
        "leaves": sum(kinds.values()),
        "kinds": rows,
        "predicted_worker_seconds_at_source_rates": round(predicted, 3),
        "unmeasured_kinds": unmeasured,
    }
    text = json.dumps(plan, indent=1)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    emit(text)
    return 0


# -------------------------------------------------------------------------------- price


def region_timings(run: Json, path: Path) -> dict[str, dict[str, Json]]:
    """Per region, per kind, the leaf timing of a run, read from its kept cfcheck report."""
    report = load_json(path.with_name(run["report"]))
    details: Json = report["details"]
    if report["command"] == "interval":
        return {name: r["leaf_timing"] for name, r in details["regions"].items()}
    return {run["sample"]["region"]: details["leaf_timing"]}


def calibration(receipts: list[Path]) -> Json:
    """Time measured here against the source's per-kind rates for the same kinds.

    The ratio is the time cfcheck took here on the leaves it checked, over the time the
    source's average rate for each leaf's kind in the same region predicts for them. It
    mixes two things: this host's speed against the source's machines, and how the
    checked leaves differ from the average leaf of their kind (a selection by the first
    leaves of each kind is not a random one). Its spread over regions says how far it
    can be trusted.
    """
    per_region, per_interval = all_source_rates()
    rows: list[Json] = []
    unmeasured: dict[str, list[float]] = {}
    here_total = source_total = cpu_total = 0.0
    for path in receipts:
        run = load_json(path)
        index = run["sample"]["interval"]
        run_here = 0.0
        for region, timing in region_timings(run, path).items():
            here = expected = 0.0
            leaves = 0
            for kind, row in timing.items():
                rate, _ = rate_for(index, region, kind, per_region, per_interval)
                if rate is None:
                    acc = unmeasured.setdefault(kind, [0, 0.0])
                    acc[0] += int(row["leaves"])
                    acc[1] += float(row["seconds"])
                    continue
                here += float(row["seconds"])
                expected += int(row["leaves"]) * rate
                leaves += int(row["leaves"])
            rows.append(
                {
                    "receipt": path.name,
                    "interval": index,
                    "region": region,
                    "leaves": sum(int(row["leaves"]) for row in timing.values()),
                    "leaf_seconds_here": round(here, 3),
                    "leaf_seconds_at_source_rates": round(expected, 3),
                    "ratio": round(here / expected, 3) if expected else None,
                }
            )
            run_here += here
            here_total += here
            source_total += expected
        cpu = float(run["cpu_seconds"]["user"]) + float(run["cpu_seconds"]["system"])
        cpu_total += cpu
        rows.append(
            {
                "receipt": path.name,
                "process_cpu_seconds": round(cpu, 3),
                "leaf_seconds_here": round(run_here, 3),
                "cpu_to_leaf_seconds": round(cpu / run_here, 4) if run_here else None,
            }
        )
    ratios = [r["ratio"] for r in rows if r.get("ratio") is not None]
    return {
        "rows": rows,
        "ratio_here_to_source": round(here_total / source_total, 4),
        "ratio_range_over_regions": [min(ratios), max(ratios)],
        "cpu_to_leaf_seconds": round(cpu_total / here_total, 4),
        "kinds_the_source_did_not_time": {
            kind: {"leaves": int(n), "seconds_per_leaf_here": round(s / n, 5)}
            for kind, (n, s) in sorted(unmeasured.items())
        },
    }


def command_price(args: argparse.Namespace) -> int:
    intervals = load_intervals(args.intervals)
    per_region, per_interval = all_source_rates()
    rows: list[Json] = []
    totals = {"recorded": 0.0, "estimated_untimed": 0.0, "unmeasured_leaves": 0}
    for index in (1, 34):
        entry = interval_entry(intervals, index)
        receipt = load_json(SOURCE_RECEIPTS[index])
        for region in REGIONS:
            published: dict[str, int] = entry["regions"][region]["leaf_kinds"]
            timed = per_region[index].get(region, {})
            recorded = sum(seconds for _, seconds in timed.values())
            untimed_seconds = 0.0
            untimed_leaves = 0
            unmeasured = 0
            for kind, n in published.items():
                missing = n - timed.get(kind, (0, 0.0))[0]
                if missing < 0:
                    msg = f"interval {index} {region}: more {kind} leaves timed than published"
                    raise SystemExit(msg)
                if not missing:
                    continue
                untimed_leaves += missing
                rate, _ = rate_for(index, region, kind, per_region, per_interval)
                if rate is None:
                    unmeasured += missing
                else:
                    untimed_seconds += missing * rate
            region_report = receipt["details"]["regions"][region]
            rows.append(
                {
                    "interval": index,
                    "region": region,
                    "roots": entry["regions"][region]["roots"],
                    "leaves": entry["regions"][region]["leaves"],
                    "roots_resumed_by_source": region_report["resumed_roots"],
                    "leaves_timed_by_source": sum(n for n, _ in timed.values()),
                    "recorded_worker_hours": round(recorded / HOUR, 3),
                    "untimed_leaves": untimed_leaves,
                    "estimated_untimed_worker_hours": round(untimed_seconds / HOUR, 3),
                    "unmeasured_leaves": unmeasured,
                }
            )
            totals["recorded"] += recorded
            totals["estimated_untimed"] += untimed_seconds
            totals["unmeasured_leaves"] += unmeasured
    source_hours = (totals["recorded"] + totals["estimated_untimed"]) / HOUR
    custody = {str(index): receipt_custody(intervals, index) for index in (1, 34)}
    replay4d = replay4d_hours()
    for row in rows:
        row["replay4d_cpu_hours"] = replay4d[row["interval"], row["region"]]
    replay4d_two = sum(replay4d.values())
    full: float = json.loads(gzip.decompress(REPLAY4D_FULL.read_bytes()))["cpu_hours_total"]
    per_interval_ratio = {
        index: sum(
            r["recorded_worker_hours"] + r["estimated_untimed_worker_hours"]
            for r in rows
            if r["interval"] == index
        )
        / sum(r["replay4d_cpu_hours"] for r in rows if r["interval"] == index)
        for index in (1, 34)
    }
    price: Json = {
        "schema": "cfcheck-price/v1",
        "basis": (
            "The source's cfcheck receipts, details.regions.*.leaf_timing: per-leaf elapsed "
            "seconds summed on worker threads, which the source calls an approximation to "
            "CPU cost. Leaves the source resumed from earlier checkpoints carry no timing "
            "and are priced at the source's rate for their kind in the same region, or "
            "pooled over the interval, or over the other interval."
        ),
        "regions": rows,
        "source_recorded_worker_hours": round(totals["recorded"] / HOUR, 2),
        "source_estimated_untimed_worker_hours": round(totals["estimated_untimed"] / HOUR, 2),
        "source_total_worker_hours": round(source_hours, 2),
        "unmeasured_leaves": totals["unmeasured_leaves"],
        "source_receipt_custody": custody,
        "replay4d": {
            "basis": (
                "The source's receipts of replay4d, receipts/published_checker.json for "
                "the eight records of intervals 1 and 34 (cpu_hours per record) and "
                "receipts/replay.json for one replay of all 136 records (cpu_hours_total)."
            ),
            "intervals_1_and_34_cpu_hours": round(replay4d_two, 2),
            "all_136_records_cpu_hours": full,
            "cfcheck_to_replay4d": {str(k): round(v, 3) for k, v in per_interval_ratio.items()},
            "cfcheck_to_replay4d_both": round(source_hours / replay4d_two, 3),
            "extrapolated_all_records_worker_hours": {
                "at_both_intervals_ratio": round(full * source_hours / replay4d_two),
                "low": round(full * min(per_interval_ratio.values())),
                "high": round(full * max(per_interval_ratio.values())),
            },
        },
    }
    if args.calibration:
        cal = calibration(args.calibration)
        factor = cal["cpu_to_leaf_seconds"]
        here = source_hours * cal["ratio_here_to_source"] * factor
        low, high = (source_hours * r * factor for r in cal["ratio_range_over_regions"])
        price["calibration"] = cal
        price["here_cpu_hours"] = round(here, 1)
        price["here_cpu_hours_over_region_ratios"] = [round(low, 1), round(high, 1)]
        price["here_wall_hours_at_threads"] = {str(t): round(here / t, 1) for t in (2, 4)}
    text = json.dumps(price, indent=1)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    emit(text)
    return 0


# ---------------------------------------------------------------------------------- run


def summarise(report: Json) -> Json:
    keys = (
        "ok",
        "command",
        "partial",
        "incomplete",
        "roots",
        "leaves",
        "resumed_roots",
        "seconds",
    )
    summary: Json = {key: report.get(key) for key in keys}
    summary["leaf_kinds"] = report.get("leaf_kinds")
    summary["checked_leaf_kinds"] = report.get("checked_leaf_kinds")
    refusals: list[Json] = report.get("refusals") or []
    summary["refusal_count"] = len(refusals)
    summary["refusals"] = refusals[:10]
    summary["interruptions"] = len(report.get("interruptions") or [])
    details: Json = report.get("details") or {}
    regions: Json = (
        details.get("regions") if report.get("command") == "interval" else {"region": details}
    )
    timing: dict[str, Json] = {}
    per_region: Json = {}
    for name, region in (regions or {}).items():
        if not isinstance(region, dict) or "leaf_timing" not in region:
            continue
        per_region[name] = {
            k: region.get(k) for k in ("checked_roots", "accepted_roots", "resumed_roots")
        }
        for kind, row in region["leaf_timing"].items():
            acc = timing.setdefault(kind, {"leaves": 0, "seconds": 0.0})
            acc["leaves"] += int(row["leaves"])
            acc["seconds"] += float(row["seconds"])
    summary["regions"] = per_region
    summary["leaf_timing"] = timing
    return summary


def tool_version(name: str) -> str:
    try:
        return subprocess.run(
            [name, "--version"], capture_output=True, text=True, check=True
        ).stdout.strip()
    except OSError, subprocess.CalledProcessError:
        return "unavailable"


def command_run(args: argparse.Namespace) -> int:
    cfargs: list[str] = args.cfcheck
    if cfargs and cfargs[0] == "--":
        cfargs = cfargs[1:]
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    load_before = os.getloadavg()
    started = now()
    clock = time.monotonic()
    proc = subprocess.run(
        [str(args.binary), *cfargs], cwd=args.cwd, capture_output=True, check=False
    )
    wall = time.monotonic() - clock
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    lines = proc.stdout.decode().splitlines()
    report: Json = json.loads(lines[0]) if lines else {}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    report_path = args.out.with_name(args.out.stem + ".report.json")
    report_path.write_bytes(lines[0].encode() + b"\n" if lines else b"")
    receipt: Json = {
        "schema": "cfcheck-run/v1",
        "label": args.label,
        "binary_sha256": sha256(args.binary),
        "toolchain": {"rustc": tool_version("rustc"), "cargo": tool_version("cargo")},
        "command": ["cfcheck", *cfargs],
        "cwd": (
            "the run directory: intervals.json and assets/<asset>/ unpacked from the release"
        ),
        "started": started,
        "finished": now(),
        "wall_seconds": round(wall, 3),
        "cpu_seconds": {
            "user": round(after.ru_utime - before.ru_utime, 3),
            "system": round(after.ru_stime - before.ru_stime, 3),
        },
        "max_rss_kib": after.ru_maxrss,
        "host": {
            "cpus": os.cpu_count(),
            "load_average_before": [round(x, 2) for x in load_before],
            "load_average_after": [round(x, 2) for x in os.getloadavg()],
            "platform": platform.platform(),
        },
        "exit_code": proc.returncode,
        "verdict": lines[-1] if lines else "",
        "stderr_tail": proc.stderr.decode()[-2000:],
        "report": report_path.name,
        "report_sha256": sha256(report_path),
        "sample": {"interval": args.interval, "region": args.region, "note": args.note},
        "summary": summarise(report),
    }
    args.out.write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    emit(
        json.dumps(
            {
                k: receipt[k]
                for k in ("label", "exit_code", "verdict", "wall_seconds", "cpu_seconds")
            }
        )
    )
    return 0


# ------------------------------------------------------------------------------- mutate


def scaled(value: str, factor: Fraction) -> str:
    q = Fraction(value) * factor
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def count_record(path: Path) -> tuple[int, int, dict[str, int]]:
    roots, leaves, kinds = 0, 0, Counter[str]()
    with path.open("rb") as handle:
        for line in handle:
            row: Json = json.loads(line)
            if "header" in row:
                continue
            roots += 1
            leaves += len(row["leaves"])
            kinds.update(kind for _, kind in row["leaves"])
    return roots, leaves, dict(sorted(kinds.items()))


def command_mutate(args: argparse.Namespace) -> int:
    intervals = load_intervals(args.intervals)
    entry = interval_entry(intervals, args.index)
    source = args.assets
    target: Path = args.out_dir / source.name
    if target.exists():
        msg = f"{target} exists"
        raise SystemExit(msg)
    shutil.copytree(source, target)
    note: Json = {"mutation": args.mutation, "interval": args.index, "from": source.name}
    changed: list[str] = []
    if args.mutation in {"duplicate-root", "relabel-leaf"}:
        record = target / f"{args.region}.rec"
        lines = record.read_bytes().splitlines(keepends=True)
        line = lines[args.line - 1]
        if args.mutation == "duplicate-root":
            lines.append(line)
            note |= {
                "region": args.region,
                "line": args.line,
                "appended_copy_of_line": args.line,
            }
        else:
            row: Json = json.loads(line)
            old = row["leaves"][args.leaf - 1][1]
            row["leaves"][args.leaf - 1][1] = args.to
            lines[args.line - 1] = (json.dumps(row, separators=(", ", ": ")) + "\n").encode()
            note |= {
                "region": args.region,
                "line": args.line,
                "leaf": args.leaf,
                "kind_from": old,
                "kind_to": args.to,
            }
        record.write_bytes(b"".join(lines))
        roots, leaves, kinds = count_record(record)
        region = entry["regions"][args.region]
        region |= {
            "sha256": sha256(record),
            "bytes": record.stat().st_size,
            "roots": roots,
            "leaves": leaves,
            "leaf_kinds": kinds,
        }
        changed.append(record.name)
    else:
        factor = Fraction(99, 100)
        for name, key in (
            ("family.json", "family_sha256"),
            ("family_right.json", "family_right_sha256"),
        ):
            path = target / name
            family: Json = json.loads(path.read_text(encoding="utf-8"))
            for group in ("F", "T"):
                for row in family.get(group, []):
                    row[4] = scaled(row[4], factor)
            for row in family.get("V", []):
                row[2] = scaled(row[2], factor)
            path.write_text(json.dumps(family), encoding="utf-8")
            entry[key] = sha256(path)
            changed.append(name)
        note |= {
            "factor": "99/100",
            "scaled": "every F and T mass and every V density of both families",
        }
    sums = target / "SHA256SUMS"
    rows = [
        line.split() for line in sums.read_text(encoding="utf-8").splitlines() if line.strip()
    ]
    resealed = {
        name: sha256(target / name.lstrip("*")) if name.lstrip("*") in changed else digest
        for digest, name in rows
    }
    sums.write_text(
        "".join(f"{digest}  {name}\n" for name, digest in resealed.items()),
        encoding="utf-8",
    )
    out_intervals = args.out_dir / "intervals.json"
    out_intervals.write_text(json.dumps(intervals, indent=1) + "\n", encoding="utf-8")
    note["resealed"] = [*changed, "SHA256SUMS", "intervals.json (digests and published counts)"]
    (args.out_dir / f"{source.name}.mutation.json").write_text(
        json.dumps(note, indent=1) + "\n", encoding="utf-8"
    )
    emit(json.dumps(note))
    return 0


# --------------------------------------------------------------------------------- main


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="command", required=True)

    plan = sub.add_parser(
        "plan", help="leaves and predicted cost of the first N roots of a record"
    )
    plan.add_argument("--record", type=Path, required=True)
    plan.add_argument("--index", type=int, required=True)
    plan.add_argument("--region", choices=REGIONS, required=True)
    plan.add_argument("--roots", type=int, required=True)
    plan.add_argument("--out", type=Path)

    counts = sub.add_parser("counts", help="the counts whose a(N) is attained on intervals")
    counts.add_argument("--intervals", type=int, nargs="+", default=[1, 34])
    counts.add_argument("--out", type=Path)

    price = sub.add_parser("price", help="price a complete replay of intervals 1 and 34")
    price.add_argument(
        "--intervals", type=Path, help="intervals.json; default: the retained gzip copy"
    )
    price.add_argument("--calibration", type=Path, nargs="*", default=[])
    price.add_argument("--out", type=Path)

    run = sub.add_parser("run", help="run one cfcheck command and write its receipt")
    run.add_argument("--binary", type=Path, required=True)
    run.add_argument("--cwd", type=Path, required=True)
    run.add_argument("--label", required=True)
    run.add_argument("--out", type=Path, required=True)
    run.add_argument("--interval", type=int)
    run.add_argument("--region")
    run.add_argument("--note", default="")
    run.add_argument("cfcheck", nargs=argparse.REMAINDER)

    mutate = sub.add_parser(
        "mutate", help="write a mutated, re-sealed copy of one interval's assets"
    )
    mutate.add_argument("--assets", type=Path, required=True)
    mutate.add_argument("--intervals", type=Path, required=True)
    mutate.add_argument("--index", type=int, required=True)
    mutate.add_argument("--out-dir", type=Path, required=True)
    mutate.add_argument(
        "--mutation", choices=("duplicate-root", "relabel-leaf", "scale-family"), required=True
    )
    mutate.add_argument("--region", choices=REGIONS, default="top")
    mutate.add_argument("--line", type=int, default=1)
    mutate.add_argument("--leaf", type=int, default=1)
    mutate.add_argument("--to", default="EMPTY")

    args = parser.parse_args(argv)
    commands = {
        "counts": command_counts,
        "plan": command_plan,
        "price": command_price,
        "run": command_run,
        "mutate": command_mutate,
    }
    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
