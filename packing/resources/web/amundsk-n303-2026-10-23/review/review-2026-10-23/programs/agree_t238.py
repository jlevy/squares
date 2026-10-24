#!/usr/bin/env python3
"""Every number the review's checker shares with the maintained routes and the records lane.

Written for the stage 4 review of T-238 (bead think-jdz0). Decides nothing: it compares
receipts. It reads:

- the certificate, through `review_t238_check.py`'s reader;
- that checker's two receipts (`outputs/check-route-z.json`, `outputs/check-route-e.json`);
- this lane's run of the maintained routes (`outputs/maintained/`), whose rows keep the
  kernel's `checker_input`;
- the records lane's replay receipt, `receipts/exact-certification.json.xz`, and its
  derived fact, `facts/n-303.yaml.gz`, from the records branch;
- `outputs/sharp-controls.json`.

It checks that the side and all 303 poses read alike everywhere (the fact's
`center-basis` against the cosine and sine of each tangent), and that each least wall
clearance, least pair gap, pair count and control margin is equal as a rational.

Usage:
  python3 -I agree_t238.py CERT --checker review_t238_check.py --outputs OUTPUTS \
      --receipt exact-certification.json.xz --fact n-303.yaml.gz --out OUT.json
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import json
import lzma
import sys
from fractions import Fraction as Q
from pathlib import Path

import yaml


def load_checker(path: str):
    spec = importlib.util.spec_from_file_location("review_t238_check", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def lit(q: Q) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("--checker", required=True)
    ap.add_argument("--outputs", required=True)
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--fact", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    checker = load_checker(args.checker)
    outputs = Path(args.outputs)
    cert = checker.read_certificate(Path(args.cert).read_bytes())
    side = Q(*cert["side"])
    poses = [[Q(*x), Q(*y), Q(*t)] for x, y, t in cert["rows"]]
    mine_input = {"n": 303, "side": lit(side), "poses": [[lit(v) for v in p] for p in poses]}

    z = json.loads((outputs / "check-route-z.json").read_text())["result"]
    e = json.loads((outputs / "check-route-e.json").read_text())["result"]
    maintained = json.loads((outputs / "maintained/maintained-routes.json").read_text())
    rows = {
        control: json.loads(lzma.decompress((outputs / f"maintained/n303-{control}.json.xz").read_bytes()))
        for control in ("positive", "duplicate-square-overlap", "square-translated-outside-container")
    }
    lane = json.loads(lzma.decompress(Path(args.receipt).read_bytes()))
    lane_rows = {row["control"]: row for row in lane["cases"]}
    fact = yaml.safe_load(gzip.decompress(Path(args.fact).read_bytes()))["witness"]
    controls = json.loads((outputs / "sharp-controls.json").read_text())
    by_name = {m["name"]: m for m in controls["mutants"]}

    checks = []

    def check(name, a, b):
        checks.append({"check": name, "equal": a == b, "left": str(a)[:120], "right": str(b)[:120]})

    # reading
    check("checker_input: this review's reader = this lane's maintained run (positive)", mine_input, rows["positive"]["checker_input"])
    check("checker_input: this review's reader = the records lane's receipt (positive, from its fact)", mine_input, lane_rows["positive"]["checker_input"])
    check("fact side = certificate side", Q(str(fact["side"])), side)
    fact_ok = len(fact["squares"]) == 303
    for p, sq in zip(poses, fact["squares"]):
        t = p[2]
        c, s = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
        if [Q(str(v)) for v in sq["center"]] != p[:2] or [Q(str(v)) for v in sq["basis"]] != [c, s]:
            fact_ok = False
    check("fact: 303 centres and bases equal the certificate's centres and the cosine and sine of its tangents", fact_ok, True)
    # positive margins
    least_wall_z = min(Q(v["clearance"]) for v in z["least_wall"].values())
    least_wall_e = min(Q(v["clearance"]) for v in e["least_wall"].values())
    check("least wall clearance: route Z = route E", least_wall_z, least_wall_e)
    for source, row in (("this lane's maintained run", rows["positive"]), ("the records lane's receipt", lane_rows["positive"])):
        for route in ("exact_verify", "independent"):
            check(f"least wall clearance: route Z = {route}, {source}", least_wall_z, Q(row[route]["minimum_containment_clearance"]))
            check(f"least pair gap: route Z = {route}, {source}", Q(z["least_gap"]["gap"]), Q(row[route]["minimum_best_pair_gap"]))
            check(f"pairs decided: route Z = {route}, {source}", z["pairs_decided"], row[route]["pairs_tested"])
            check(f"verdict: accepted = {route}, {source}", True, row[route]["verification_passed"])
    check("least pair gap: route Z = route E's least Euclidean distance", Q(z["least_gap"]["gap"]) ** 2, Q(e["least_distance_squared"]["distance_squared"]))
    check("pairs decided: route Z = route E", z["pairs_decided"], e["pairs_decided"])
    check("per-square wall clearances: route Z = route E (digest)", z["per_square_wall_digest"], e["per_square_wall_digest"])
    check("per-pair gaps: route Z = route E (digest)", z["per_pair_gap_digest"], e["per_pair_gap_digest"])
    # gross controls
    g1, g2 = by_name["G1"], by_name["G2"]
    for source, rws in (("this lane's maintained run", rows), ("the records lane's receipt", lane_rows)):
        for route in ("exact_verify", "independent"):
            check(
                f"duplicate-square control gap: route Z (G1) = {route}, {source}",
                Q(g1["review_routes"]["Z"]["least_gap"]),
                Q(rws["duplicate-square-overlap"][route]["minimum_best_pair_gap"]),
            )
            check(
                f"outside-container control wall: route Z (G2) = {route}, {source}",
                Q(g2["review_routes"]["Z"]["least_wall"]),
                Q(rws["square-translated-outside-container"][route]["minimum_containment_clearance"]),
            )
    # the kernel's sharp controls against this review's
    sharp = maintained["sharp"]
    check("kernel's tightest pair = route Z's first least-gap pair", [maintained["tightest_pair"]["left"], maintained["tightest_pair"]["right"]], [z["least_gap"]["pairs"][0]["i"], z["least_gap"]["pairs"][0]["j"]])
    check("kernel's tightest gap = route Z's least gap", Q(maintained["tightest_pair"]["gap"]), Q(z["least_gap"]["gap"]))
    top_right = min(Q(z["least_wall"]["right"]["clearance"]), Q(z["least_wall"]["top"]["clearance"]))
    check("kernel's top clearance = route Z's least top-or-right clearance", Q(maintained["top_clearance"]), top_right)
    for key, mutant in (("side-lowered-past-wall-contact", "F"), ("tightest-pair-closed-past-contact", "P")):
        for state, suffix in (("contact", "0"), ("past", "1")):
            for route in ("exact_verify", "independent"):
                k = f"{key}:{state}"
                mine_verdict = by_name[mutant + suffix]["verdicts"]["Z"] == "accept"
                check(f"{k}: {route} verdict = route Z on {mutant}{suffix}", sharp[k][route]["passed"], mine_verdict)
                if mutant == "F":
                    check(f"{k}: {route} wall = route Z on {mutant}{suffix}", Q(sharp[k][route]["wall"]), Q(by_name[mutant + suffix]["review_routes"]["Z"]["least_wall"]))
                else:
                    check(f"{k}: {route} gap = route Z on {mutant}{suffix}", Q(sharp[k][route]["gap"]), Q(by_name[mutant + suffix]["review_routes"]["Z"]["least_gap"]))
    # the sixteen paired mutants: maintained margins against route Z's
    for m in controls["mutants"]:
        if m["name"][0] in "FNBPQTUD" and m["name"][1] in "01":
            for route in ("exact_verify", "independent"):
                check(f"{m['name']}: {route} least wall = route Z", Q(m["maintained_routes"][route]["least_wall"]), Q(m["review_routes"]["Z"]["least_wall"]))
                check(f"{m['name']}: {route} least gap = route Z", Q(m["maintained_routes"][route]["least_gap"]), Q(m["review_routes"]["Z"]["least_gap"]))
    result = {
        "program": "agree_t238.py",
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "checks": len(checks),
        "equal": sum(1 for c in checks if c["equal"]),
        "unequal": [c for c in checks if not c["equal"]],
        "all": checks,
    }
    Path(args.out).write_text(json.dumps(result, indent=2) + "\n")
    print(f"{result['equal']} of {result['checks']} checks equal")
    for c in result["unequal"]:
        print("UNEQUAL:", c["check"], c["left"], c["right"])
    return 0 if not result["unequal"] else 1


if __name__ == "__main__":
    sys.exit(main())
