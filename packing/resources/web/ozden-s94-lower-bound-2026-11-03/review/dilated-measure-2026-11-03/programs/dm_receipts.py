"""The census row, the control receipt and the author's receipts, against the candidate.

Usage: dm_receipts.py CERTIFICATE.json.gz AUTHOR_198.jsonl AUTHOR_193.jsonl CENSUS_CAPTURE.jsonl.gz
                      CENSUS_JSON CONTROL_RECEIPT.json PREMISES_OUT.json OUT.json

Holds the records to items 1 to 6 of the 6 October declared-net soundness review's
checklist ("For the Records Lane", (b)), with this review's own exact values from
`dm_premises.py`'s receipt (PREMISES_OUT.json) in place of the crate's:

- each of the three runs (the author's two receipts, this repository's census capture):
  the summary's status, premises and build, and indices exactly 0..599, each verified;
  per direction, the three runs' verdicts, least certified bounds and node counts equal;
- the census row's case, premises, candidate digest and build;
- the control receipt: its status and runs; then, apart from the crate and the census
  tool, every one of the 600 refusals of the 99/100 mutant is recomputed exactly
  (dmlib method 1): the original's capture at the recorded pose, times 99/100, must equal
  the recorded exact capture (or, at r = 0, lie at or above the vertex sweep's certified
  bound), lie below 1, and the pose must lie in the per-bin domain; and the
  near-threshold mutant's witness the same way.
"""

from __future__ import annotations

import gzip
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dmlib  # noqa: E402

TIMING = {"cpu_seconds", "seconds", "wall_seconds", "direction_cpu_seconds", "direction_seconds", "threads", "build"}


def jsonl(path: Path) -> list[dict]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def run_view(lines: list[dict], mine: dict, file_sha: str) -> tuple[dict, dict[int, dict]]:
    rows = [line for line in lines if "r" in line]
    summaries = [line for line in lines if line.get("kind") == "sqverify-fast-summary/v1"]
    by_index: dict[int, dict] = {}
    duplicates = 0
    for row in rows:
        if int(row["r"]) in by_index:
            duplicates += 1
        by_index[int(row["r"])] = row
    summary = summaries[-1] if summaries else {}
    premises = summary.get("premises", {})
    want = {
        "B": mine["file"]["B"],
        "D": mine["file"]["proof_net"]["step"],
        "L": mine["file"]["L"],
        "angle_count": mine["file"]["proof_net"]["count"],
        "centre_domain": "per-bin",
        "expanded_points": 0,
        "expanded_rectangles": mine["expansion"]["distinct_images"],
        "expanded_segments": 0,
        "format": "M",
        "input_sha256": file_sha,
        "mass_exact": mine["file"]["mass"],
        "mass_below_n": mine["file"]["n_minus_mass"],
        "n": mine["file"]["n"],
        "net_last_tangent": mine["premises"]["(c) t_max"],
        "net_origin": "proof_net",
        "shrink_bound": mine["premises"]["(b) B(1 + D)"],
        "source_rectangles": mine["file"]["rows"],
    }
    mismatched = sorted(key for key, value in want.items() if premises.get(key) != value)
    extra = sorted(set(premises) - set(want))
    view = {
        "summaries": len(summaries),
        "status": summary.get("status"),
        "refused_directions": summary.get("refused_directions"),
        "fault_injected_at_box": summary.get("fault_injected_at_box"),
        "threshold": summary.get("threshold"),
        "build": summary.get("build"),
        "nodes": summary.get("nodes"),
        "indices_exactly_0_to_last": sorted(by_index) == list(range(mine["file"]["proof_net"]["count"])) and not duplicates,
        "every_direction_verified": all(row.get("verdict") == "verified" for row in rows),
        "every_threshold_1": all(row.get("threshold") == "1" for row in rows),
        "premises_mismatched": mismatched,
        "premises_not_compared": extra,
        "least_bound": min((row["min_certified_lower_bound"], row["r"]) for row in rows),
    }
    return view, by_index


def main() -> None:
    args = [Path(a) for a in sys.argv[1:9]]
    cert_path, author98, author93, capture_path, census_path, control_path, premises_path, out_path = args
    started = time.process_time()
    mine = json.loads(premises_path.read_text())
    file_sha = dmlib.sha256_file(cert_path)
    failures: list[str] = []
    runs = {}
    indexed = {}
    for name, path in (("author-rustc1.98", author98), ("author-rustc1.93", author93), ("census-capture", capture_path)):
        view, by_index = run_view(jsonl(path), mine, file_sha)
        view["file_sha256"] = dmlib.sha256_file(path)
        runs[name] = view
        indexed[name] = by_index
        if not (view["status"] == "VERIFIED" and view["indices_exactly_0_to_last"] and view["every_direction_verified"]):
            failures.append(f"{name}: not verified at every index")
        if view["premises_mismatched"] or view["fault_injected_at_box"] is not None:
            failures.append(f"{name}: premises {view['premises_mismatched']}")
    differing = []
    for index in range(mine["file"]["proof_net"]["count"]):
        keys = ("verdict", "min_certified_lower_bound", "nodes", "leaves", "least_bound_box", "argmin", "vertices")
        views = [{k: indexed[name][index].get(k) for k in keys} for name in indexed]
        if any(v != views[0] for v in views[1:]):
            differing.append(index)
    agreement = {"directions_where_the_three_runs_differ": differing, "fields_compared": list(keys)}

    # census row
    census = json.loads(census_path.read_text())["cases"]["mixed_n94_L9965"]
    row_checks = {
        "n": census.get("n") == 94,
        "L": census.get("L") == mine["file"]["L"],
        "status VERIFIED": census.get("status") == "VERIFIED",
        "returncode 0": census.get("returncode") == 0,
        "refused_directions empty": census.get("refused_directions") == [],
        "directions_verified = last + 1": census.get("directions_verified") == mine["file"]["proof_net"]["count"],
        "threshold 1": census.get("threshold") == "1",
        "least_bound_leaf_exact.clears_threshold": (census.get("least_bound_leaf_exact") or {}).get("clears_threshold") is True,
        "candidate_sha256 is the retained file's": census.get("candidate_sha256") == file_sha,
        "build source d97758bb, release, rustc 1.98.0": (census.get("build") or {}).get("source_sha256", "").startswith("d97758bb")
        and census["build"].get("profile") == "release"
        and census["build"].get("rustc", "").startswith("rustc 1.98.0"),
        "premises equal the summary's": census.get("premises") == next(
            line for line in jsonl(capture_path) if line.get("kind") == "sqverify-fast-summary/v1"
        ).get("premises"),
    }
    for key, ok in row_checks.items():
        if not ok:
            failures.append(f"census row: {key}")

    # control receipt
    control = json.loads(control_path.read_text())
    cert = dmlib.certificate(dmlib.read_gzip_json(cert_path).data)
    exact = dmlib.ExactMeasure.of(cert, dmlib.expand(cert))
    runs_by_name = {run["name"]: run for run in control["runs"]}
    scaled = runs_by_name["scaled-99-100"]
    factor = Fraction(scaled["mutation"]["factor"])
    recomputed = []
    worst = None
    original_least = None
    for item in scaled["sweep"]["refused"]:
        index = int(item["r"])
        x, y = (Fraction(str(v)) if isinstance(v, str) else Fraction(v) for v in item["pose"])
        original = dmlib.fraction_of(dmlib.capture_exact(exact, index, dmlib.q(x), dmlib.q(y))[0])
        mutant = factor * original
        low, high = dmlib.domain(cert, index)
        in_domain = low <= x <= high and low <= y <= high
        recorded = Fraction(item["capture"])
        if index == 0:
            bound = Fraction(item["crate_lower_bound"])
            agrees = bound <= mutant
            gap = float(mutant - bound)
        else:
            agrees = mutant == recorded
            gap = None
        ok = agrees and mutant < 1 and in_domain and original >= 1 and mutant == recorded
        if not ok:
            failures.append(f"control refusal at r {index} does not hold")
        if worst is None or mutant > worst[0]:
            worst = (mutant, index)
        if original_least is None or original < original_least[0]:
            original_least = (original, index, item["pose"])
        if index == 0 or index % 100 == 0 or index == 599:
            recomputed.append({"r": index, "original": float(original), "mutant": float(mutant), "equals_recorded": mutant == recorded, "in_domain": in_domain, "axis_bound_gap": gap})
    near = runs_by_name["near-threshold"]
    witness = near["witness"]
    near_factor = Fraction(near["mutation"]["factor"])
    wx, wy = witness["exact_pose"]
    near_original = dmlib.fraction_of(dmlib.capture_exact(exact, int(control["index"]), dmlib.exact_of_float(wx), dmlib.exact_of_float(wy))[0])
    near_mutant = near_factor * near_original
    low, high = dmlib.domain(cert, int(control["index"]))
    control_view = {
        "status": control["status"],
        "captures_agree": control["captures_agree"],
        "original": {k: runs_by_name["original"].get(k) for k in ("verdict", "returncode", "min_certified_lower_bound")},
        "scaled_99_100": {
            "refused_directions": len(scaled["sweep"]["refused"]),
            "summary_status": scaled["sweep"].get("summary_status"),
            "returncode": scaled["sweep"].get("returncode"),
            "recomputed_here_exactly": len(scaled["sweep"]["refused"]),
            "every_refusal_holds_here": all(f"control refusal at r {i}" not in " ".join(failures) for i in range(600)),
            "largest_mutant_capture_at_a_witness": [float(worst[0]), worst[1]] if worst else None,
            "least_original_capture_at_a_witness": [str(original_least[0]), float(original_least[0]), original_least[1], original_least[2]] if original_least else None,
            "sampled_rows": recomputed,
        },
        "near_threshold": {
            "factor": str(near_factor),
            "r": int(control["index"]),
            "pose": [wx, wy],
            "mutant_capture_here": float(near_mutant),
            "equals_recorded": near_mutant == Fraction(witness["exact_coverage"]),
            "below_1": near_mutant < 1,
            "in_domain": all(low <= Fraction(v) <= high for v in (wx, wy)),
            "returncode": near.get("returncode"),
        },
    }
    if not (control_view["near_threshold"]["equals_recorded"] and near_mutant < 1):
        failures.append("near-threshold witness does not hold")

    report = {
        "program": "dm_receipts.py",
        "program_sha256": dmlib.sha256_file(Path(__file__)),
        "dmlib_sha256": dmlib.sha256_file(Path(dmlib.__file__)),
        "certificate_file_sha256": file_sha,
        "runs": runs,
        "per_direction_agreement": agreement,
        "census_row": row_checks,
        "control": control_view,
        "failures": failures,
        "status": "RECORDS_HOLD" if not failures else "RECORDS_DIFFER",
        "cpu_seconds": round(time.process_time() - started, 1),
    }
    out_path.write_text(dmlib.dumps(report, 3) + "\n")
    print(json.dumps({"status": report["status"], "failures": failures[:20], "control_status": control["status"], "cpu_seconds": report["cpu_seconds"]}, indent=1))


if __name__ == "__main__":
    main()
