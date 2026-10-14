"""The source's own run and control logs, read as data and checked against the candidate.

Usage::

    python3 -I check_source_logs.py CANDIDATE.json RUN.jsonl.gz CONTROL.jsonl.gz \\
        RECEIPT.json PREPUBLICATION.json BUNDLE.json [TIGHTEST]

Prints, as JSON: whether the run log holds every direction of the declared net exactly
once, each verified at threshold one with a certified lower bound of at least one, with
the node total and the summary the receipt embeds; the summary's premises against the
candidate read here; the axis row's least vertex, at which the original's exact capture is
recomputed here and compared with the sweep's certified bound; the ``TIGHTEST`` (default
10) oblique directions of least certified bound, at whose least-bound leaf centres the
exact capture is recomputed here; and the control log's 32 refusals of the mass-scaled
mutant, each witness evaluated again here, exactly, on the scaled measure. It decides
only the poses it evaluates, and no direction.
"""

from __future__ import annotations

import gzip
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fine_net_exact as exact


def rows_of(path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        lines = [json.loads(line) for line in stream if line.strip()]
    rows = sorted((line for line in lines if "r" in line), key=lambda row: int(row["r"]))
    summary = next(
        (line for line in lines if line.get("kind") == "sqverify-fast-summary/v1"), {}
    )
    return rows, summary


def premises_agree(
    premises: dict[str, Any], measure: exact.Measure, data: bytes
) -> dict[str, bool]:
    return {
        "input_sha256_is_candidate": premises.get("input_sha256") == exact.sha256(data),
        "n": premises.get("n") == measure.n,
        "L": Fraction(str(premises.get("L"))) == measure.side,
        "B": Fraction(str(premises.get("B"))) == measure.core,
        "D": Fraction(str(premises.get("D"))) == measure.step,
        "angle_count": premises.get("angle_count") == measure.count,
        "mass_exact": Fraction(str(premises.get("mass_exact"))) == measure.total,
        "format_M_per_bin": (premises.get("format"), premises.get("centre_domain"))
        == ("M", "per-bin"),
        "expanded_rectangles": premises.get("expanded_rectangles") == len(measure.images),
        "source_rectangles": premises.get("source_rectangles") == len(measure.rows),
        "no_points_or_segments": (
            premises.get("expanded_points"),
            premises.get("expanded_segments"),
        )
        == (0, 0),
    }


def run_log(
    rows: list[dict[str, Any]], summary: dict[str, Any], measure: exact.Measure, tightest: int
) -> dict[str, Any]:
    indices = [int(row["r"]) for row in rows]
    axis = rows[0] if rows and int(rows[0]["r"]) == 0 else {}
    oblique = [row for row in rows if int(row["r"]) > 0]
    verdicts = {row.get("verdict") for row in rows}
    bounds = [
        row["min_certified_lower_bound"]
        for row in rows
        if row.get("min_certified_lower_bound") is not None
    ]
    nodes = sum(int(row.get("nodes") or 0) for row in oblique)
    argmin = [Fraction(value) for value in axis.get("argmin", [])]
    axis_capture = exact.capture(measure, argmin[0], argmin[1], 0) if argmin else None
    ranked = sorted(oblique, key=lambda row: (row["min_certified_lower_bound"], int(row["r"])))[
        :tightest
    ]
    points = []
    for row in ranked:
        box = row["least_bound_box"]
        x, y = Fraction(box["x"]), Fraction(box["y"])
        value = exact.capture(measure, x, y, int(row["r"]))
        low, high = exact.domain(measure.side, measure.step, int(row["r"]))
        points.append(
            {
                "r": int(row["r"]),
                "certified_lower_bound": row["min_certified_lower_bound"],
                "leaf_centre": [box["x"], box["y"]],
                "in_domain": low <= x <= high and low <= y <= high,
                "exact_capture": float(value),
                "at_least_1": value >= 1,
                "at_least_certified_bound": value >= Fraction(row["min_certified_lower_bound"]),
            }
        )
    return {
        "rows": len(rows),
        "indices_are_0_to_last_once": indices == list(range(measure.count)),
        "verdicts": sorted(verdicts),
        "thresholds": sorted({str(row.get("threshold")) for row in rows}),
        "methods": sorted({str(row.get("method")) for row in rows}),
        "least_certified_bound": min(bounds) if bounds else None,
        "least_certified_bound_at": min(rows, key=lambda row: row["min_certified_lower_bound"])[
            "r"
        ]
        if bounds
        else None,
        "all_bounds_at_least_1": all(bound >= 1 for bound in bounds),
        "oblique_nodes": nodes,
        "summary_nodes": summary.get("nodes"),
        "nodes_agree": nodes == summary.get("nodes"),
        "most_nodes_at": max(oblique, key=lambda row: int(row["nodes"]))["r"]
        if oblique
        else None,
        "direction_cpu_seconds": sum(float(row.get("cpu_seconds") or 0) for row in rows),
        "summary_status": summary.get("status"),
        "summary_refused": summary.get("refused_directions"),
        "summary_fault": summary.get("fault_injected_at_box"),
        "summary_build": summary.get("build"),
        "axis": {
            "x_events": axis.get("x_events"),
            "y_events": axis.get("y_events"),
            "certified_lower_bound": axis.get("min_certified_lower_bound"),
            "argmin": axis.get("argmin"),
            "argmin_in_domain": bool(argmin)
            and all(
                exact.domain(measure.side, measure.step, 0)[0]
                <= v
                <= exact.domain(measure.side, measure.step, 0)[1]
                for v in argmin
            ),
            "exact_capture": None if axis_capture is None else float(axis_capture),
            "exact_capture_rational": None if axis_capture is None else str(axis_capture),
            "exact_minus_certified": None
            if axis_capture is None
            else float(axis_capture - Fraction(axis["min_certified_lower_bound"])),
            "certified_is_a_lower_bound": axis_capture is not None
            and axis_capture >= Fraction(axis["min_certified_lower_bound"]),
        },
        "tightest_oblique_leaves": points,
    }


def control_log(
    rows: list[dict[str, Any]], summary: dict[str, Any], measure: exact.Measure
) -> dict[str, Any]:
    factor = Fraction(str(summary["premises"]["mass_exact"])) / measure.total
    witnessed = []
    for row in rows:
        r = int(row["r"])
        witness = row.get("witness") or {}
        pose = witness.get("exact_pose")
        if row.get("verdict") == "refused" and r == 0:
            pose = row.get("argmin")
        if not pose:
            witnessed.append({"r": r, "verdict": row.get("verdict"), "pose": None})
            continue
        x, y = Fraction(pose[0]), Fraction(pose[1])
        value = factor * exact.capture(measure, x, y, r)
        low, high = exact.domain(measure.side, measure.step, r)
        crate = witness.get("exact_coverage")
        witnessed.append(
            {
                "r": r,
                "verdict": row.get("verdict"),
                "method": row.get("method"),
                "in_domain": low <= x <= high and low <= y <= high,
                "scaled_capture": float(value),
                "below_1": value < 1,
                "equals_crate_exact_coverage": crate is not None and Fraction(crate) == value,
                "crate_exact_below_threshold": witness.get("exact_below_threshold"),
                "original_capture_at_pose_at_least_1": value / factor >= 1,
            }
        )
    return {
        "factor": str(factor),
        "rows": len(rows),
        "directions": [int(row["r"]) for row in rows],
        "verdicts": sorted({str(row.get("verdict")) for row in rows}),
        "summary_status": summary.get("status"),
        "summary_refused_count": len(summary.get("refused_directions") or []),
        "summary_input_sha256": (summary.get("premises") or {}).get("input_sha256"),
        "every_refusal_witnessed_below_1_in_domain": all(
            item.get("below_1")
            and item.get("in_domain")
            and item.get("verdict") in ("counterexample-candidate", "refused")
            for item in witnessed
        ),
        "every_oblique_witness_equals_crate": all(
            item.get("equals_crate_exact_coverage") for item in witnessed if item["r"] > 0
        ),
        "witnesses": witnessed,
    }


def main(argv: list[str]) -> int:
    candidate_path, run_path, control_path = Path(argv[1]), Path(argv[2]), Path(argv[3])
    receipt_path, prepublication_path, bundle_path = Path(argv[4]), Path(argv[5]), Path(argv[6])
    tightest = int(argv[7]) if len(argv) > 7 else 10
    data = candidate_path.read_bytes()
    measure = exact.read_measure(exact.load_json(data))
    digest = exact.semantic_digest(exact.load_json(data))
    run_rows, run_summary = rows_of(run_path)
    control_rows, control_summary = rows_of(control_path)
    # The receipts are read with their floats as floats, as the logs are, so that the
    # receipt's embedded summary compares with the log's line value by value.
    receipt = json.loads(receipt_path.read_bytes(), object_pairs_hook=exact.refuse_duplicates)
    prepublication = json.loads(
        prepublication_path.read_bytes(), object_pairs_hook=exact.refuse_duplicates
    )
    bundle = json.loads(bundle_path.read_bytes(), object_pairs_hook=exact.refuse_duplicates)
    report = {
        "candidate_sha256": exact.sha256(data),
        "semantic_digest": digest,
        "run_log": run_log(run_rows, run_summary, measure, tightest),
        "run_premises_agree": premises_agree(run_summary.get("premises") or {}, measure, data),
        "receipt": {
            "status": receipt.get("status"),
            "directions": receipt.get("directions"),
            "candidate_digest_is_ours": receipt.get("candidate_digest") == digest,
            "file_sha256_is_candidate": receipt.get("file_sha256") == exact.sha256(data),
            "embedded_summary_equals_log_summary": receipt.get("verifier_summary")
            == run_summary,
            "verifier_source_sha256": (receipt.get("verifier_summary") or {})
            .get("build", {})
            .get("source_sha256"),
            "binary_sha256": ((receipt.get("receipt") or {}).get("verifier") or {}).get(
                "binary_sha256"
            ),
            "threads": (receipt.get("receipt") or {}).get("threads"),
            "started_utc": (receipt.get("receipt") or {}).get("started_utc"),
        },
        "prepublication": {
            "status": prepublication.get("status"),
            "directions_verified": prepublication.get("directions_verified"),
            "seconds": prepublication.get("seconds"),
            "candidate_digest_is_ours": prepublication.get("candidate_digest") == digest,
            "input_sha256_is_candidate": prepublication.get("input_sha256")
            == exact.sha256(data),
            "source_sha256": (prepublication.get("build") or {}).get("source_sha256"),
            "same_build_as_check2": (prepublication.get("build") or {}).get("source_sha256")
            == (run_summary.get("build") or {}).get("source_sha256"),
            "control": prepublication.get("control"),
        },
        "bundle": {
            "candidate_digest_is_ours": bundle.get("candidate_digest") == digest,
            "candidate_sha256_is_candidate": bundle.get("candidate_sha256")
            == exact.sha256(data),
            "net_block_is_ours": all(
                Fraction(str(bundle["net"][name])) == value
                for name, value in exact.net_facts(
                    measure.core, measure.step, measure.count
                ).items()
                if name in bundle["net"]
            ),
            "receipt_sha256_is_receipt": bundle.get("receipt_sha256")
            == exact.sha256(receipt_path.read_bytes()),
        },
        "control_log": control_log(control_rows, control_summary, measure),
    }
    sys.stdout.write(json.dumps(report, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
