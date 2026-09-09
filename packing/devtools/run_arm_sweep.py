#!/usr/bin/env python3
"""Run several search *arms* over the same cells and seeds, at one declared budget.

    run_arm_sweep.py plan.yaml --out results/exp-130

An **arm** is one proposer: the control engine, or the control engine with one flag
group. The plan file names them, and it is the pre-registration -- it is written before
the sweep runs, it lives beside the archive the sweep produces, and nothing in this
tool reads a threshold or an accept rule, so the plan cannot be tuned to the result.

Three things this tool does that a shell loop does not, and each is why it exists rather
than a one-off script (OR-1):

* **One budget, in the campaign's own currency.** Arms whose per-move cost differs are
  not comparable at equal moves: a simultaneous perturbation scans every pair where a
  single-square move scans one square's. The budget here is `budget_pair_tests`, per
  chain, which is machine-independent -- so a loaded host changes the wall clock and
  changes nothing about what was compared.
* **The engine gate runs before any measurement,** and its result is recorded, not
  asserted.
* **Every archived pose is re-checked by `sqpack.verify` in a separate process,** via
  `packing-campaign verify-archive`. A side the engine printed is a claim by the thing
  under test; a side whose geometry an independent oracle re-derives is evidence. Any
  candidate below the standing best is flagged loudly and separately here rather than
  averaged into a median.

The output is an archive per arm plus `summary.json`, which carries the per-(arm, cell)
median, best, gap, hit rate and cost. The verdict is not this tool's business.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import platform
import statistics
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from sqpack.project import configured_project_root
from sqpack.yamlio import safe_load

ROOT = configured_project_root()
REPO = ROOT.parent


def shown(path: Path) -> str:
    """Repository-relative when it is inside the checkout, absolute otherwise."""
    try:
        return str(path.relative_to(REPO))
    except ValueError:
        return str(path)


# A gap under this counts as reaching the record's basin: the campaign's numerical proxy
# for "found the right combinatorial class", never evidence of it.
REACHED_BASIN = 1e-4
# The task's stricter reading of a hit: within 1e-6 of the standing best.
HIT = 1e-6


def frontier_best(n: int) -> tuple[float, str]:
    """The standing best for `n`, read from the frontier register and never retyped."""
    path = ROOT / "frontier" / f"n-{n:03d}.md"
    case = safe_load(path.read_text().split("---\n")[1])["packing"]
    bound = case.get("reported_upper_bound") or case["upper_bound"]
    who = ", ".join(bound.get("found_by") or ["unknown"])
    return float(bound["value"]), f"frontier/n-{n:03d}.md ({who} {bound.get('found_year', '')})"


def grid_side(n: int) -> float:
    """The trivial packing's side, which every chain starts from."""
    return float(math.ceil(math.sqrt(n)))


def run_selftest(engine: Path) -> dict[str, Any]:
    """Execute the engine's own gate. A failing gate stops the sweep."""
    started = time.time()
    done = subprocess.run(
        [str(engine), "--selftest"], capture_output=True, text=True, check=False
    )
    passed = done.returncode == 0 and "SELFTEST PASSED" in done.stdout
    return {
        "command": f"{engine} --selftest",
        "passed": passed,
        "seconds": round(time.time() - started, 3),
        "tail": done.stdout.strip().splitlines()[-1:] or [done.stderr.strip()[:200]],
    }


def run_one(
    engine: Path, plan: dict[str, Any], flags: list[str], n: int, seed: int
) -> list[str]:
    """One (arm, cell, seed) invocation. Returns its JSONL lines."""
    command = [
        str(engine),
        "--n", str(n),
        "--seed", str(seed),
        "--chains", str(plan["chains"]),
        "--threads", str(plan["threads"]),
        "--budget-moves", str(plan.get("budget_moves", 2**63)),
        "--budget-pair-tests", str(plan["budget_pair_tests"]),
        *flags,
    ]  # fmt: skip
    done = subprocess.run(command, capture_output=True, text=True, check=True)
    return [line for line in done.stdout.splitlines() if line.strip()]


def verify(archive: Path) -> dict[str, Any]:
    """Hand the archive to the independent pose oracle, in its own process."""
    done = subprocess.run(
        [sys.executable, "-m", "sqpack.campaign.runner", "verify-archive", str(archive)],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )  # fmt: skip
    lines = [line for line in done.stdout.splitlines() if line.strip()]
    if not lines:
        return {"verified": False, "failures": [done.stderr.strip()[:400]], "poses_checked": 0}
    report = json.loads(lines[-1])
    # The per-pose detail is large and already summarised by the fields beside it.
    report.pop("poses", None)
    return report


def summarise(rows: list[dict[str, Any]], n: int) -> dict[str, Any]:
    """Per-(arm, cell) statistics. Median and range together, or it is not a result."""
    best_by_seed = sorted(row["seed_best"] for row in rows)
    record, source = frontier_best(n)
    gaps = [side - record for side in best_by_seed]
    return {
        "n": n,
        "seeds": len(best_by_seed),
        "median_side": statistics.median(best_by_seed),
        "best_side": best_by_seed[0],
        "worst_side": best_by_seed[-1],
        "median_gap": statistics.median(gaps),
        "best_gap": min(gaps),
        "record": record,
        "record_source": source,
        "grid": grid_side(n),
        "beat_grid_runs": sum(1 for side in best_by_seed if side < grid_side(n) - 1e-12),
        "basin_runs": sum(1 for gap in gaps if gap < REACHED_BASIN),
        "hit_runs": sum(1 for gap in gaps if gap < HIT),
        "below_record_runs": sum(1 for gap in gaps if gap < -1e-12),
        "pair_tests": sum(row["pair_tests"] for row in rows),
        "moves": sum(row["moves"] for row in rows),
        "seconds": sum(row["seconds"] for row in rows),
    }


def rows_from_archive(archive: Path) -> list[dict[str, Any]]:
    """Rebuild a sweep's per-(cell, seed) rows from an archive alone.

    The recovery path, and the reason a sweep that dies three hours in is not a loss:
    every number the summary needs is already in the archive, so an interrupted round
    can be summarised from what it wrote. Wall seconds come from the engine's own
    summary line rather than from the harness clock, which no longer exists.
    """
    best: dict[tuple[int, int], dict[str, float]] = {}
    for line in archive.read_text().splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if "best_side" not in rec:
            continue
        key = (int(rec["n"]), int(rec["seed"]))
        row = best.setdefault(
            key, {"n": key[0], "seed": key[1], "seed_best": math.inf,
                  "pair_tests": 0, "moves": 0, "seconds": 0.0}
        )  # fmt: skip
        row["seed_best"] = min(row["seed_best"], float(rec["best_side"]))
        if rec.get("kind") == "summary":
            row["pair_tests"] += int(rec["pair_tests"])
            row["moves"] += int(rec["moves"])
            row["seconds"] += float(rec.get("seconds", 0.0))
    return [best[key] for key in sorted(best)]


def rebuild(plan_path: Path, out: Path) -> dict[str, Any]:
    """Summarise whatever archives a sweep left behind, complete or not."""
    plan = safe_load(plan_path.read_text())
    summary: dict[str, Any] = {
        "plan": str(plan_path),
        "label": plan["label"] + " (rebuilt from archives)",
        "engine": plan["engine"],
        "gate": {"passed": True, "command": "rebuilt: the gate ran when the sweep ran"},
        "host": {
            "platform": platform.platform(),
            "cpu_count": os.cpu_count(),
            "loadavg_before": os.getloadavg(),
            "loadavg_after": os.getloadavg(),
        },
        "budget_pair_tests_per_chain": plan["budget_pair_tests"],
        "chains": plan["chains"],
        "threads": plan["threads"],
        "cells": plan["cells"],
        "seeds": plan["seeds"],
        "arms": {},
    }
    for arm, flags in plan["arms"].items():
        archive = out / f"{arm}.jsonl"
        if not archive.exists():
            continue
        rows = rows_from_archive(archive)
        cells = {
            str(n): summarise([r for r in rows if r["n"] == n], n)
            for n in plan["cells"]
            if any(r["n"] == n for r in rows)
        }
        if not cells:
            continue
        summary["arms"][arm] = {
            "flags": list(flags),
            "archive": shown(archive),
            "verification": verify(archive),
            "runs": rows,
            "cells": cells,
        }
    return summary


def render(summary: dict[str, Any]) -> str:
    """The arm-by-cell table, lifted from the summary and never retyped into prose."""
    present = {n for body in summary["arms"].values() for n in body["cells"]}
    cells = [str(n) for n in summary["cells"] if str(n) in present]
    header = (
        f"Budget {summary['budget_pair_tests_per_chain']:.3g} pair tests per chain, "
        f"{summary['chains']} chains, {summary['threads']} threads, "
        f"seeds {summary['seeds']}. "
        f"Engine gate: {'passed' if summary['gate']['passed'] else 'FAILED'}. "
        f"Load {summary['host']['loadavg_before'][0]:.1f} -> "
        f"{summary['host']['loadavg_after'][0]:.1f} on "
        f"{summary['host']['cpu_count']} cores."
    )
    lines = [
        header,
        "",
        "| arm | " + " | ".join(f"n={n}" for n in cells) + " |",
        "| --- | " + " | ".join("---" for _ in cells) + " |",
    ]

    def cell_of(n: str) -> dict[str, Any] | None:
        """Any arm's view of this cell, for the record and grid rows."""
        for body in summary["arms"].values():
            if n in body["cells"]:
                return body["cells"][n]
        return None

    lines.append(
        "| **record** | "
        + " | ".join(f"`{(cell_of(n) or {}).get('record', 0):.6f}`" for n in cells)
        + " |"
    )
    lines.append(
        "| **grid** | "
        + " | ".join(f"`{(cell_of(n) or {}).get('grid', 0):.0f}`" for n in cells)
        + " |"
    )
    for arm, body in summary["arms"].items():
        row = []
        for n in cells:
            c = body["cells"].get(n)
            if c is None:
                row.append("--")
                continue
            row.append(
                f"`{c['median_side']:.6f}`<br>`{c['best_side']:.6f}`<br>{c['median_gap']:+.2e}"
                + ("" if c["seeds"] == len(summary["seeds"]) else f"<br>({c['seeds']} seeds)")
            )
        lines.append(f"| {arm} | " + " | ".join(row) + " |")
    lines.append("")
    lines.append(
        "| arm | verified poses | beat grid | basin (1e-4) | hits (1e-6) | below record |"
    )
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")

    for arm, body in summary["arms"].items():
        totals = [body["cells"][n] for n in cells if n in body["cells"]]
        checked = body["verification"]["poses_checked"]
        verdict = "ok" if body["verification"]["verified"] else "REFUSED"
        lines.append(
            f"| {arm} | {checked} {verdict}"
            f" | {sum(c['beat_grid_runs'] for c in totals)}"
            f"/{sum(c['seeds'] for c in totals)}"
            f" | {sum(c['basin_runs'] for c in totals)}"
            f" | {sum(c['hit_runs'] for c in totals)}"
            f" | {sum(c['below_record_runs'] for c in totals)} |"
        )
    return "\n".join(lines)


def merged(paths: list[Path]) -> dict[str, Any]:
    """Fold several summaries of one sweep into one table.

    A sweep split across concurrent processes is still one measurement: sqsearch is
    deterministic in (n, seed, chain, params), so which process ran an arm changes
    nothing about its numbers. Merging is refused when the parts do not agree about the
    budget, the cells or the seeds, because then they are not one measurement.
    """
    parts = [json.loads(path.read_text()) for path in paths]
    head = parts[0]
    for part in parts[1:]:
        for field in ("budget_pair_tests_per_chain", "chains", "cells", "seeds"):
            if part[field] != head[field]:
                message = f"summaries disagree about {field}; they are not one sweep"
                raise SystemExit(message)
    out = dict(head)
    out["arms"] = {arm: body for part in parts for arm, body in part["arms"].items()}
    out["host"] = dict(head["host"])
    out["host"]["loadavg_after"] = max(
        (part["host"]["loadavg_after"] for part in parts), key=lambda load: load[0]
    )
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "plan", type=Path, help="the plan, written before the sweep runs (or a summary.json)"
    )
    parser.add_argument(
        "extra", type=Path, nargs="*", help="further summary.json parts, with --report"
    )
    parser.add_argument("--out", type=Path, help="archive directory")
    parser.add_argument(
        "--only-arm", action="append", default=[], help="restrict to these arms"
    )
    parser.add_argument(
        "--report", action="store_true", help="render an existing summary.json and stop"
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="rebuild summary.json from the archives an interrupted sweep left in --out",
    )
    options = parser.parse_args(argv)

    if options.rebuild:
        if options.out is None:
            parser.error("--rebuild needs --out")
        target = options.out if options.out.is_absolute() else ROOT / options.out
        summary = rebuild(options.plan, target)
        # Never `summary.json`: a rebuild may run against a sweep that is still writing,
        # and clobbering the live summary would destroy the thing being recovered.
        (target / "summary-rebuilt.json").write_text(
            json.dumps(summary, indent=2, sort_keys=True) + "\n"
        )
        print(render(summary))
        return 0
    if options.report:
        print(render(merged([options.plan, *options.extra])))
        return 0
    if options.out is None:
        parser.error("--out is required unless --report is given")

    plan = safe_load(options.plan.read_text())
    engine = (ROOT / plan["engine"]).resolve()
    out = options.out if options.out.is_absolute() else ROOT / options.out
    out.mkdir(parents=True, exist_ok=True)

    gate = run_selftest(engine)
    if not gate["passed"]:
        print(json.dumps({"refused": "engine selftest failed", "gate": gate}), file=sys.stderr)
        return 1

    arms = {
        name: flags
        for name, flags in plan["arms"].items()
        if not options.only_arm or name in options.only_arm
    }
    summary: dict[str, Any] = {
        "plan": str(options.plan),
        "label": plan["label"],
        "engine": shown(engine),
        "gate": gate,
        "host": {
            "platform": platform.platform(),
            "cpu_count": os.cpu_count(),
            "loadavg_before": os.getloadavg(),
        },
        "budget_pair_tests_per_chain": plan["budget_pair_tests"],
        "chains": plan["chains"],
        "threads": plan["threads"],
        "cells": plan["cells"],
        "seeds": plan["seeds"],
        "arms": {},
    }

    for arm, flags in arms.items():
        archive = out / f"{arm}.jsonl"
        rows: list[dict[str, Any]] = []
        with archive.open("w", encoding="utf-8") as handle:
            for n in plan["cells"]:
                for seed in plan["seeds"]:
                    started = time.time()
                    lines = run_one(engine, plan, list(flags), n, seed)
                    elapsed = time.time() - started
                    records = [json.loads(line) for line in lines]
                    scored = [r for r in records if "best_side" in r]
                    handle.write("\n".join(lines) + "\n")
                    # Flushed per run, not per buffer: the archive is the recovery path
                    # for an interrupted sweep, and a buffered archive recovers nothing.
                    handle.flush()
                    summaries = [r for r in records if r.get("kind") == "summary"]
                    rows.append(
                        {
                            "n": n,
                            "seed": seed,
                            # The seed's result is the MINIMUM over its own lines, so
                            # nothing has to agree about which line is the summary.
                            "seed_best": min(float(r["best_side"]) for r in scored),
                            "pair_tests": sum(int(r["pair_tests"]) for r in summaries),
                            "moves": sum(int(r["moves"]) for r in summaries),
                            "seconds": elapsed,
                        }
                    )
                    print(
                        f"{arm} n={n} seed={seed} best={rows[-1]['seed_best']:.12f} "
                        f"{elapsed:.1f}s",
                        file=sys.stderr,
                    )
        summary["arms"][arm] = {
            "flags": list(flags),
            "archive": shown(archive),
            "verification": verify(archive),
            "runs": rows,
            "cells": {
                str(n): summarise([r for r in rows if r["n"] == n], n) for n in plan["cells"]
            },
        }

    summary["host"]["loadavg_after"] = os.getloadavg()
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"wrote": str((out / "summary.json").relative_to(REPO))}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
