#!/usr/bin/env python3
"""Checks 1 to 6 and 8 of the format T route review's section 5, for T-046's 46 rows.

Written for the stage 4 review of T-046 (bead think-buaj). Decides nothing about
coverage: it reads sqverify-fast's census rows, per-direction receipts and control
receipts for the 46 standing certificates, and the case records, and reports, per
certificate, every condition of
docs/project/reviews/review-2026-10-06-sqverify-fast-format-t-route.md section 5 that
holds or fails:

1. the case (status, exit, 201 directions, no refusal, threshold, least leaf clears it);
2. the receipts (directions 0..200 once, each verified at the threshold, one summary
   VERIFIED with no fault injected, its build and premises the row's, node total and least
   bound the row's);
3. the premises (format T, Tokoharu's domain, the standard net and core, the mass, no
   expanded point or segment, no declared net, metadata restating the standard net,
   net_origin, densities far below lemma F3's caps);
4. the candidate binding (candidate_sha256 = premises.input_sha256 = the stored file);
5. the build (row and control of reviewed source, release, rustc 1.98.0);
6. the control (CONTROLS_REFUSED at the threshold, the selection rule's fields, the three
   runs, the near-threshold factor);
8. the values (whether any count's verified lower bound would move).

It reports the mass condition separately, as the route's 6 October condition (n - 1/100)
and as the widened one this review reads (n - 1/100 or n - 1/1000), and lists every
retained format T census row whose mass is n - 1/1000, cited or not.

Usage, from packing/:
  .venv/bin/python3 -I PROGRAMS/route_t046.py --packing . --out OUT.json
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import re
import sys
from fractions import Fraction as Q
from pathlib import Path

CENSUS = "benchmarks/measure-verifier/census"
WEB = "resources/web"
THRESHOLD = "10001/10000"
NEAR = Q(1, 10**6)
DIRECTIONS = 201
#: The crate sources a soundness review accepted (the driver's REVIEWED_SOURCES), copied
#: here by digest rather than imported, so a change there shows as a difference.
REVIEWED = {
    "9985c465116631570c873ecc33af126adc6f14c7429a5ed44d922254d3c7f8a7": "4ddf37d9c",
    "7c49cf79f2408e745d5a0759caf85768d92c502bb574b95dbc12b81a36e50300": "e020eb1e2",
    "d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88": "910b6b12c",
}
DENSITY_CEILING = 2**32


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def receipt_rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in gzip.decompress(path.read_bytes()).splitlines()]


def candidate(packing: Path, packet: str, name: str) -> Path:
    return (
        packing / WEB / f"wand125-rectangle-certificates-{packet}"
        / "wand125-rectangles/certificates" / name / "certified_candidate.json.gz"
    )


def check(packing: Path, packet: str, name: str, row: dict) -> dict:
    out = packing / CENSUS / packet
    failed: list[str] = []

    def need(label: str, ok: bool) -> None:
        if not ok:
            failed.append(label)

    least = row["least_bound_leaf_exact"]
    premises = row["premises"]
    n = int(premises["n"])
    # 1. The case.
    need("1 status VERIFIED, exit 0", row["status"] == "VERIFIED" and row["returncode"] == 0)
    need("1 201 directions, none refused", row["directions_verified"] == DIRECTIONS and row["refused_directions"] == [])
    need("1 threshold 10001/10000", row["threshold"] == THRESHOLD)
    need("1 least leaf clears it", least["clears_threshold"] is True and Q(least["exact_coverage"]) >= Q(THRESHOLD))
    need("1 n and L the directory's", (n, Q(premises["L"])) == (row["n"], Q(row["L"])) and name == f"rect_n{n}_L{name.rsplit('_L', 1)[1]}")
    # 2. The receipts.
    rows = receipt_rows(out / f"{name}.jsonl.gz")
    directions = [item for item in rows if "r" in item]
    summaries = [item for item in rows if item.get("kind") == "sqverify-fast-summary/v1"]
    need("2 directions 0..200 once", sorted(int(item["r"]) for item in directions) == list(range(DIRECTIONS)))
    need("2 each verified", all(item["verdict"] == "verified" for item in directions))
    need("2 one summary", len(summaries) == 1 and rows[-1] is summaries[0])
    summary = summaries[0] if summaries else {}
    need("2 summary VERIFIED, no fault", summary.get("status") == "VERIFIED" and summary.get("fault_injected_at_box") is None)
    need("2 summary build and premises the row's", summary.get("build") == row["build"] and summary.get("premises") == premises)
    need("2 node total the row's", sum(int(item.get("nodes", 0)) for item in directions) == row["nodes"])
    need("2 least bound the receipts' minimum", min(item["min_certified_lower_bound"] for item in directions) == row["least_certified_bound"])
    thresholds = {str(item.get("threshold", THRESHOLD)) for item in directions}
    need("2 each at the threshold", thresholds == {THRESHOLD})
    # 3. The premises.
    raw = json.loads(gzip.decompress(candidate(packing, packet, name).read_bytes()))
    metadata = raw.get("certificate") or {}
    need("3 format T, Tokoharu's domain", premises["format"] == "T" and premises["centre_domain"] == "tokoharu")
    need("3 standard net and core", (premises["angle_count"], premises["D"], premises["B"]) == (DIRECTIONS, "83/40000", "9977/10000"))
    need("3 no expanded point or segment", premises["expanded_points"] == premises["expanded_segments"] == 0)
    need("3 no points, segments or declared net in the file", not {"points", "segments", "proof_net", "net"} & set(raw))
    need("3 metadata restates the standard net", Q(str(metadata.get("D", "83/40000"))) == Q(83, 40000) and int(metadata.get("angle_count", DIRECTIONS)) == DIRECTIONS)
    need("3 net_origin standard or metadata", premises.get("net_origin") in (None, "standard", "metadata"))
    densest = max(
        Q(str(weight)) / ((Q(str(x2)) - Q(str(x1))) * (Q(str(y2)) - Q(str(y1))))
        for (x1, y1, x2, y2), weight in zip(raw["rectangles"], raw["weights"], strict=True)
    )
    need("3 densities far below F3's caps", densest <= DENSITY_CEILING)
    gap = n - Q(premises["mass_exact"])
    mass_old = gap == Q(1, 100)
    mass_new = gap in (Q(1, 100), Q(1, 1000))
    need("3 mass n - 1/100 or n - 1/1000 (widened)", mass_new and Q(premises["mass_below_n"]) == gap)
    # 4. The candidate.
    stored = sha256(candidate(packing, packet, name))
    need("4 candidate binding", row["candidate_sha256"] == premises["input_sha256"] == stored)
    # 5. The build.
    control = json.loads((out / f"{name}.control.json").read_text(encoding="utf-8"))
    built, controlled = row["build"]["source_sha256"], (control.get("build") or {}).get("source_sha256")
    need("5 row of reviewed source", built in REVIEWED)
    need("5 release, rustc 1.98.0", (row["build"]["profile"], row["build"]["rustc"].split()[1]) == ("release", "1.98.0"))
    need("5 control of reviewed source", controlled in REVIEWED)
    # 6. The control.
    need("6 CONTROLS_REFUSED at the threshold", control["status"] == "CONTROLS_REFUSED" and control["threshold"] == THRESHOLD)
    need("6 v1 receipt", control["kind"] == "sqverify-fast-control/v1")
    need("6 selection rule", control["selection"] == "tightest least-bound leaf centre" and control["centres_weighed"] == DIRECTIONS - 1 and control["index"] >= 1)
    (chosen,) = [item for item in directions if int(item["r"]) == control["index"]]
    box = chosen["least_bound_box"]
    need("6 centre is that direction's least-bound box", control["centre"] == [box["x"], box["y"]])
    need("6 captures agree", control["captures_agree"] is True and control["exact_capture_crate"] == control["exact_capture_independent"])
    need("6 binding", control["candidate_sha256"] == stored and (control["packet"], control["n"], Q(control["L"])) == (packet, n, Q(row["L"])))
    runs = {run["name"]: run for run in control["runs"]}
    exact = Q(control["exact_capture_independent"])
    need("6 three runs", set(runs) == {"original", "scaled-99-100", "near-threshold"})
    need("6 original verified, exit 0", (runs["original"]["returncode"], runs["original"]["verdict"]) == (0, "verified"))
    below: dict[str, str] = {}
    for mutant in ("scaled-99-100", "near-threshold"):
        run = runs[mutant]
        mutation = run["mutation"]
        factor = Q(mutation["factor"])
        witness = mutation.get("capture_at_witness")
        at_centre = exact * factor < Q(THRESHOLD)
        at_witness = witness is not None and Q(witness) < Q(THRESHOLD)
        need(f"6 {mutant} refused on coverage, exit 1", run["returncode"] == 1 and run["verdict"] == "counterexample-candidate")
        need(f"6 {mutant} capture at centre is factor x capture", Q(mutation["capture_at_centre"]) == exact * factor)
        need(f"6 {mutant} exact capture below the threshold", at_centre or at_witness)
        below[mutant] = "centre" if at_centre else "witness" if at_witness else "none"
        if witness is not None:
            below[f"{mutant} witness below 1"] = str(Q(witness) < 1)
    need("6 99/100 factor", Q(runs["scaled-99-100"]["mutation"]["factor"]) == Q(99, 100))
    need("6 near-threshold factor", exact * Q(runs["near-threshold"]["mutation"]["factor"]) <= Q(THRESHOLD) * (1 - NEAR))
    return {
        "certificate": name,
        "packet": packet,
        "n": n,
        "L": row["L"],
        "mass_below_n": str(gap),
        "mass_condition_6_october": mass_old,
        "mass_condition_widened": mass_new,
        "row_source": REVIEWED.get(built, built[:8]),
        "control_source": REVIEWED.get(str(controlled), str(controlled)[:8]),
        "binary_sha256": row["binary_sha256"],
        "threads": row.get("threads"),
        "cpu_seconds": row.get("cpu_seconds"),
        "nodes": row["nodes"],
        "least_certified_bound": row["least_certified_bound"],
        "least_leaf_r": least["r"],
        "least_leaf_capture": float(Q(least["exact_coverage"])),
        "control_index": control["index"],
        "control_capture": float(exact),
        "mutants_below": below,
        "densest_log2": round(math.log2(densest), 2),
        "failed": failed,
    }


def verified_lower(packing: Path, n: int) -> Q | None:
    text = (packing / "frontier" / f"n-{n:03d}.md").read_text(encoding="utf-8")
    block = text.split("verified_lower_bound:", 1)
    if len(block) < 2:
        return None
    match = re.search(r"exact_form: ['\"]?([^'\"\n]+)", block[1])
    if match is None:
        return None
    form = match[1].strip()
    try:
        return Q(form)
    except ValueError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--packing", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    packing = args.packing.resolve()
    sys.path.insert(0, str(Path(__file__).parent))
    from certificates_t046 import BY_MASS, CLAIM, STANDING, write_report  # noqa: PLC0415

    census = json.loads((packing / CENSUS / "census.json").read_text(encoding="utf-8"))["cases"]
    results = [
        check(packing, packet, name, census[name])
        for packet, names in STANDING.items()
        for name in names
    ]
    thousandths = sorted(
        name for name, row in census.items()
        if row.get("premises", {}).get("format") == "T"
        and Q(row["premises"]["mass_below_n"]) == Q(1, 1000)
    )
    values: list[dict] = []
    for n, value in sorted(CLAIM.items()):
        held = verified_lower(packing, n)
        values.append({
            "n": n,
            "t046": value,
            "verified_lower_bound": str(held) if held is not None else None,
            "moves": held is None or Q(value) > held,
            "by_mass_from": BY_MASS.get(n),
        })
    report = {
        "kind": "t046-review-route/v1",
        "rows": results,
        "format_t_rows_at_n_minus_1_1000": thousandths,
        "needs_widening": [row["certificate"] for row in results if not row["mass_condition_6_october"]],
        "row_sources": {source: sum(row["row_source"] == source for row in results) for source in {row["row_source"] for row in results}},
        "control_sources": {source: sum(row["control_source"] == source for row in results) for source in {row["control_source"] for row in results}},
        "values": values,
        "moves": [item["n"] for item in values if item["moves"]],
        "failed": sum(len(row["failed"]) for row in results),
    }
    report["status"] = "PASS" if report["failed"] == 0 and not report["moves"] else "FAIL"
    write_report(args.out, report)
    print(
        f"{report['status']}: {len(results)} rows, {report['failed']} failed conditions; "
        f"needs widening {report['needs_widening']}; n - 1/1000 rows {thousandths}; "
        f"row sources {report['row_sources']}; control sources {report['control_sources']}; "
        f"verified bounds moved at {report['moves']}"
    )
    for row in results:
        for label in row["failed"]:
            print(f"  {row['certificate']}: {label}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
