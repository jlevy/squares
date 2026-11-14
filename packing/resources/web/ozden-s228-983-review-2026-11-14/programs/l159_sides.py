"""Lane L159's arithmetic of the claim: decides nothing about feasibility.

Written after the findings were frozen, for the stage 4 review of issue #983. It reads
the certificate through the reader and compares its exact side, exactly, with the claim,
the house at 228 (T-174) and the record's earlier exact side (T-128), the issue's and
README's prints, the side-only and Kaggle values the issue quotes, the decimal pose's
side, the search side, the promotion and interval reports, and the certificate's own
contraction.

Usage: l159_sides.py CERT.yaml TWIN.json N228.md HOUSE.yaml T128.cert.gz POSE.yaml
       HIT.json PROMOTE.json INTERVAL.json ISSUE.json CONTRACTION_NEW.json
       CONTRACTION_T174.json OUT.json
"""

from __future__ import annotations

import gzip
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml  # noqa: E402

from l159_geom import ceil_places, floor_places, sci  # noqa: E402
from l159_reader import read_paths  # noqa: E402


def frac(text: str) -> Fraction:
    return Fraction(text.strip())


def main(argv: list[str]) -> int:
    (cert, twin, case_md, house, t128, pose, hit, promote, interval, issue_path, cnew, ct174, out_path) = (
        Path(a) for a in argv[1:14]
    )
    w = read_paths(cert, twin)
    s = Fraction(*w.side)
    out: dict[str, object] = {"program": "l159_sides.py"}
    out["side_floor_45"] = floor_places(s, 45)
    out["side_floor_12"] = floor_places(s, 12)
    out["side_ceil_12"] = ceil_places(s, 12)
    out["side_floor_15"] = floor_places(s, 15)
    out["side_ceil_15"] = ceil_places(s, 15)
    out["side_floor_16"] = floor_places(s, 16)
    out["side_ceil_16"] = ceil_places(s, 16)
    issue = json.loads(issue_path.read_text(encoding="utf-8"))
    body = issue["body"]
    claim = Fraction("15.600801734812")
    out["claim_less_side"] = sci(claim - s, 8)
    out["claim_is_ceil_12"] = ceil_places(s, 12) == "15.600801734812"

    # The issue's exact-side digits.
    m = re.search(r"exact side, specified in the witness, is (15\.[0-9]+)", body)
    printed = m.group(1) if m else ""
    out["issue_exact_side_digits"] = printed
    out["issue_exact_side_digits_are_floor"] = bool(printed) and floor_places(s, len(printed) - 3) == printed

    # The house (T-174) and T-128.
    case_text = case_md.read_text(encoding="utf-8")
    front = yaml.safe_load(case_text.split("---")[1])
    rub = front["packing"]["reported_upper_bound"]
    vub = front["packing"]["verified_upper_bound"]
    h = frac(vub["exact_form"])
    out["house_reported_equals_verified"] = frac(rub["exact_form"]) == h
    out["house_value_print"] = vub["value"]
    out["house_print_is_ceil_17"] = ceil_places(h, 17) == vub["value"]
    hw = yaml.load(house.read_text(encoding="utf-8"), Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))
    out["house_witness_side_equals_case"] = frac(str(hw["witness"]["side"])) == h
    out["house_floor_20"] = floor_places(h, 20)
    gain = h - s
    out["gain_on_house"] = sci(gain, 15)
    out["gain_on_house_floor_17"] = floor_places(gain, 17)
    out["gain_relative_to_house"] = sci(gain / h, 6)
    out["gain_relative_to_side"] = sci(gain / s, 6)
    issue_gain = Fraction("0.00379974091792048")
    out["issue_gain_less_exact_gain"] = sci(issue_gain - gain, 6)
    out["issue_gain_is_floor_17"] = floor_places(gain, 17) == "0.00379974091792048"
    out["issue_gain_is_round_17"] = abs(issue_gain - gain) <= Fraction(1, 2 * 10**17)
    t128_text = gzip.decompress(t128.read_bytes()).decode()
    t128_side = Fraction([line for line in t128_text.splitlines() if not line.startswith("#")][0].split()[1])
    out["t128_side_floor_30"] = floor_places(t128_side, 30)
    out["t128_less_house"] = sci(t128_side - h, 6)
    out["gain_on_t128"] = sci(t128_side - s, 15)

    # The side-only entry and Kaggle.
    k1 = Fraction("15.596043116646")
    k2 = Fraction("15.604601475744")
    out["side_minus_side_only"] = sci(s - k1, 12)
    out["claim_minus_side_only"] = sci(claim - k1, 12)
    out["issue_side_only_gap_0.004758618166"] = {
        "exact_gap_floor_12": floor_places(s - k1, 12),
        "exact_gap_round_12_matches": abs(Fraction("0.004758618166") - (s - k1)) <= Fraction(1, 2 * 10**12),
    }
    out["kaggle_minus_side"] = sci(k2 - s, 12)
    out["kaggle_minus_claim"] = sci(k2 - claim, 12)
    out["kaggle_minus_house"] = sci(k2 - h, 8)
    out["readme_kaggle_gap_0.003799740932"] = abs(Fraction("0.003799740932") - (k2 - s)) <= Fraction(1, 2 * 10**12)
    hitj = json.loads(hit.read_text(encoding="utf-8"))
    out["hit_record"] = hitj.get("record")
    out["hit_lb"] = hitj.get("lb")
    out["hit_lb_less_side_only"] = sci(Fraction(str(hitj["lb"])) - k1, 6)

    # The decimal pose, the search side and the reports.
    pw = yaml.safe_load(pose.read_text(encoding="utf-8"))
    pose_side = Fraction(pw["witness"]["side"])
    out["pose_side"] = pw["witness"]["side"]
    out["pose_side_less_side"] = sci(pose_side - s, 8)
    search = Fraction("15.60080173481195764")
    out["search_side_less_side"] = sci(search - s, 8)
    out["search_side_less_pose_side"] = sci(search - pose_side, 6)
    pj = json.loads(promote.read_text(encoding="utf-8"))
    out["promote_side_equals_certificate"] = Fraction(pj["side"]) == s
    out["promote_side_increase"] = sci(Fraction(pj["side_increase"]), 8)
    out["promote_side_increase_is_side_less_pose_side"] = Fraction(pj["side_increase"]) == s - pose_side
    out["promote_ids"] = {"promoted_witness": pj.get("promoted_witness"), "source_witness": pj.get("source_witness")}
    ij = json.loads(interval.read_text(encoding="utf-8"))
    out["interval_certified_side_exact_equals_pose_side"] = Fraction(ij["certified_side_exact"]) == pose_side
    out["interval_min_wall_margin"] = ij["min_wall_margin"]
    out["interval_min_pair_margin"] = ij["min_pair_margin"]

    # Contractions (devtools.contraction_margin receipts).
    cn = json.loads(cnew.read_text(encoding="utf-8"))
    out["new_one_minus_lambda_star"] = str(1 - Fraction(cn["lambda_star"]))
    out["new_contracted_side_floor_20"] = floor_places(Fraction(cn["contracted_side"]), 20)
    out["new_margin"] = sci(Fraction(cn["margin"]), 8)
    out["new_margin_is_side_less_contracted_side"] = Fraction(cn["margin"]) == s - Fraction(cn["contracted_side"])
    ch = json.loads(ct174.read_text(encoding="utf-8"))
    out["house_lambda_star"] = ch["lambda_star"]
    out["house_margin"] = ch["margin"]
    out["house_binding_pair"] = ch["binding_pair"]
    out["house_routes_accept"] = ch["routes_accept"]
    out["gain_equals_contraction_receipt"] = Fraction(ch["against"]["gain"]) == gain
    out_path.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    for key in ("side_floor_45", "claim_less_side", "gain_on_house", "gain_relative_to_house", "issue_gain_is_floor_17", "side_minus_side_only", "kaggle_minus_side", "kaggle_minus_house", "pose_side_less_side"):
        print(key, out[key])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
