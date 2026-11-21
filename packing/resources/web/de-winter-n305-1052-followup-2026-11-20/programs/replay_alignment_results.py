"""Check retained n305 alignment receipts or replay one bounded first-party calculation.

The check action validates inputs and saved outcomes without rerunning geometry or
minimum-cover search. Replay actions compare fresh results, ignoring timings only.
No action proves the 34 local geometric exclusions or changes the accepted T-336.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import lzma
import signal
import sys
import time
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_sharp_controls as sharp
from devtools.evand_exact_certificates import Certificate, literal
from devtools.select_n11_field_minimum import Cover, minimum_covers
from devtools.upper_bound_reports import parse_certificate

comparison = importlib.import_module("replay_comparisons")
require = comparison.require
VARIANTS = {
    "31-aligned": "n305_31_quarter_turns.json",
    "37-aligned": "n305_37_aligned.json",
}
MOVED = [108, 140, 141, 142, 143, 150, 153, 164, 175]
LIMITATIONS = (
    "Exact same-side alignment variant of T-336. Finite feasibility only; "
    "no novelty, optimality, minimum-movement or drawing-selection claim."
)


def profile(variant: str) -> dict[str, str]:
    return {
        "witness_prefix": f"W-de-winter-1052-{variant}-n",
        "claim_limitations": LIMITATIONS,
    }


def read(packet: Path, name: str) -> Any:
    path = packet / "receipts" / name
    return kernel.read_xz(path) if path.suffix == ".xz" else json.loads(path.read_bytes())


def restored(original: Certificate, aligned: Certificate) -> Certificate:
    """Keep every 37-turn candidate value except square 43's original half-angle."""
    poses = list(aligned.poses)
    poses[42] = replace(poses[42], t=original.poses[42].t)
    return replace(aligned, poses=tuple(poses))


def cover(groups: list[list[int]]) -> Cover:
    centers = sorted({center for group in groups for center in group})
    sets = {
        str(center): frozenset(i for i, group in enumerate(groups) if center in group)
        for center in centers
    }
    return minimum_covers(frozenset(range(len(groups))), sets, max_nodes=300_000)


def check_sharp(
    record: dict[str, Any], candidate: Certificate, packet: Path, variant: str
) -> None:
    roster = [
        (control, where)
        for control in sharp.CONTROLS
        for where in (
            ("gross",) if control == sharp.DUPLICATE else ("at-contact", "past-contact")
        )
    ]
    require(
        record["format"] == sharp.FORMAT
        and record["n"] == 305
        and record["side"] == literal(candidate.side)
        and record["epsilon"] == literal(sharp.EPSILON)
        and record["routes"] == list(sharp.ROUTES)
        and record["certificate"]
        == f"packing/resources/web/{packet.name}/source/{VARIANTS[variant]}.gz",
        "Sharp input envelope differs",
    )
    require(
        [(row["control"], row["where"]) for row in record["controls"]] == roster,
        "Sharp control roster differs",
    )
    require(record["all_as_expected"] is True, "Sharp receipt reports a failure")
    for row in record["controls"]:
        require(row["as_expected"] is True, "Sharp control reports a failure")
        require(set(row["routes"]) == set(sharp.ROUTES), "Sharp route roster differs")
        for verdict in row["routes"].values():
            require(
                verdict["passed"] is (not row["expected_failures"])
                and verdict["failures"] == row["expected_failures"]
                and sharp.margin_met(
                    Fraction(verdict[row["margin"]]),
                    Fraction(row["expected_margin"]),
                    row["margin_rule"],
                    Fraction(row["detail"].get("edge", "1")),
                ),
                "Sharp verdict, failure category or exact margin differs",
            )


def audit(
    repo: Path, packet: Path
) -> tuple[dict[str, Certificate], Certificate, dict[str, Any]]:
    _, data = comparison.custody(repo, packet)
    manifest = json.loads((packet / "acquisition/completed-replays.json").read_bytes())
    for row in manifest["records"]:
        body = (packet / row["path"]).read_bytes()
        if row["storage"] == "xz":
            body = lzma.decompress(body)
        require(
            len(body) == row["bytes"] and hashlib.sha256(body).hexdigest() == row["sha256"],
            f"Completed receipt differs: {row['path']}",
        )
    original = parse_certificate(data["n305_exact.json"], 305, "center-direction-json")
    candidates = {
        key: parse_certificate(data[name], 305, "center-direction-json")
        for key, name in VARIANTS.items()
    }
    positives = {}
    for variant, candidate in candidates.items():
        require(candidate.side == original.side, "Variant side differs from T-336")
        positives[variant] = kernel.validate_receipt(
            read(packet, f"feasibility-{variant}.json.xz"),
            {305: candidate},
            receipt_format=f"de-winter-n305-{variant}-replay-v1",
            **profile(variant),
        )[305]
        check_sharp(read(packet, f"sharp-controls-{variant}.json"), candidate, packet, variant)
    kept = restored(original, candidates["37-aligned"])
    saved = read(packet, "square43-kept.json.xz")
    pairs = list(zip(original.poses, kept.poses, strict=True))
    moved = [i for i, (a, b) in enumerate(pairs, 1) if (a.x, a.y) != (b.x, b.y)]
    turns = [i for i, (a, b) in enumerate(pairs, 1) if a.basis != b.basis]
    extent = max(max(abs(a.x - b.x), abs(a.y - b.y)) for a, b in pairs)
    require(
        moved == saved["moved_center_ids"] == MOVED, "Restored witness moved centers differ"
    )
    require(
        turns == saved["changed_orientation_ids"] and len(turns) == 36 and 43 not in turns,
        "Restored witness changed directions differ",
    )
    require(
        str(extent) == saved["maximum_move"] and extent <= Fraction(2, 10**11),
        "Restored witness exceeds coordinate bound",
    )
    require(
        all(kept.poses[i - 1].basis[0] * kept.poses[i - 1].basis[1] == 0 for i in turns),
        "A restored witness changed direction is not aligned",
    )
    require(saved["both_routes_passed"] is True, "Restored witness reports a failure")
    kernel.validate_job(
        saved["native_positive_job"], kept, "positive", witness_prefix="W-issue1052-keep43-n"
    )
    hitting = read(packet, "hitting-set.json.xz")
    groups = [row["fixed"] for row in json.loads(data["local-move-conflicts.json"])]
    require(
        hitting["source_sha256"]
        == hashlib.sha256(data["local-move-conflicts.json"]).hexdigest()
        and hitting["groups"] == groups
        and len(groups) == 17,
        "Conflict groups differ",
    )
    minimizers = {tuple(row) for row in hitting["minimizers"]}
    require(
        len(minimizers) == len(hitting["minimizers"]) == 1581
        and hitting["minimum_cardinality"] == 9
        and hitting["nodes"] == 10991,
        "Recorded hitting-set result differs",
    )
    require(
        all(
            len(set(choice)) == 9 and all(set(choice).intersection(group) for group in groups)
            for choice in minimizers
        ),
        "A retained minimizer does not cover all groups",
    )
    require(
        all(set(MOVED).intersection(group) for group in groups),
        "Nine-center candidate misses a group",
    )
    summary = {
        "scope": (
            "Saved-receipt integrity and input correspondence; "
            "no geometry or cover search rerun."
        ),
        "side_exact": literal(original.side),
        "feasibility_jobs": 6,
        "feasibility_route_outcomes": 12,
        "sharp_cases": 22,
        "sharp_route_outcomes": 44,
        "square43_restored_positive_routes": 2,
        "pairs_per_positive_route": 46360,
        "minimum_hitting_set_recorded": 9,
        "minimum_hitting_set_minimizers": 1581,
        "minimum_hitting_set_nodes": 10991,
        "local_geometric_exclusions": "34 unverified; no geometric minimum-nine conclusion",
        "positive_margins": {
            name: {
                key: job["exact_verify"][key]
                for key in ("id", "minimum_containment_clearance", "minimum_best_pair_gap")
            }
            for name, job in {
                **positives,
                "36-aligned-keep43": saved["native_positive_job"],
            }.items()
        },
    }
    return candidates, kept, summary


def untimed(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{key: value for key, value in row.items() if key != "cpu_seconds"} for row in rows]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action", choices=("check", "feasibility", "sharp", "square43", "hitting-set")
    )
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--packet", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--variant", choices=tuple(VARIANTS))
    parser.add_argument("--control", choices=kernel.JOBS, default="positive")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--startup-delay", type=float, default=0)
    args = parser.parse_args()
    require(
        0 <= args.startup_delay <= 30, "Startup delay must be between zero and thirty seconds"
    )
    signal.alarm(930)
    time.sleep(args.startup_delay)
    packet = args.packet.resolve()
    candidates, kept, summary = audit(args.repo.resolve(), packet)
    if args.action == "check":
        sys.stdout.write(json.dumps(summary, indent=2) + "\n")
        return
    require(args.out is not None, "A replay needs a fresh --out path in external scratch")
    require(
        not args.out.exists() and not args.out.resolve().is_relative_to(packet),
        "Replay output must be new and outside the retained packet",
    )
    signal.alarm(
        900 if args.action == "sharp" else 600 if args.action == "feasibility" else 120
    )
    if args.action in {"feasibility", "sharp"}:
        require(args.variant is not None, "Variant replay needs --variant")
        candidate = candidates[args.variant]
        if args.action == "feasibility":
            fresh = kernel.run_case(candidate, args.control, **profile(args.variant))
            saved = read(packet, f"feasibility-{args.variant}.json.xz")["cases"]
            expected = next(row for row in saved if row["control"] == args.control)
            require(
                kernel.stable_row(fresh) == kernel.stable_row(expected),
                "Feasibility replay differs",
            )
        else:
            rows = sharp.control_rows(candidate, profile(args.variant))
            saved = read(packet, f"sharp-controls-{args.variant}.json")["controls"]
            require(untimed(rows) == untimed(saved), "Sharp replay differs")
            fresh = {"variant": args.variant, "controls": rows}
    elif args.action == "square43":
        fresh = kernel.run_case(kept, "positive", witness_prefix="W-issue1052-keep43-n")
        expected = read(packet, "square43-kept.json.xz")["native_positive_job"]
        require(
            kernel.stable_row(fresh) == kernel.stable_row(expected),
            "Restored-square replay differs",
        )
    else:
        single, disjoint = cover([[1, 2], [2, 3]]), cover([[1, 2], [3, 4]])
        require(
            (single.size, single.selections, disjoint.size, len(disjoint.selections))
            == (1, (frozenset({"2"}),), 2, 4),
            "Small cover controls differ",
        )
        saved = read(packet, "hitting-set.json.xz")
        found = cover(saved["groups"])
        choices = {frozenset(map(int, choice)) for choice in found.selections}
        require(
            found.size == saved["minimum_cardinality"]
            and found.nodes == saved["nodes"]
            and choices == {frozenset(choice) for choice in saved["minimizers"]},
            "Hitting-set replay differs",
        )
        fresh = {
            "minimum_cardinality": found.size,
            "minimizers": len(choices),
            "nodes": found.nodes,
            "scope": "Combinatorial result; geometric exclusions remain unverified.",
        }
    atomic_write_text(args.out, json.dumps(fresh, indent=2) + "\n")
    sys.stdout.write(f"PASS {args.action}: fresh result agrees with retained evidence\n")


if __name__ == "__main__":
    main()
