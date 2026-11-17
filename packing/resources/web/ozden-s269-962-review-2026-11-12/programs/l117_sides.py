"""Lane L117, after the freeze: the claim's arithmetic. Decides nothing.

Reads the certificate (frozen reader), T-290's side from the case record's exact_form,
from the house witness and from the issue's printed fraction, T-174's side from the
identity receipt, and the issue as fetched; prints every quantity the issue states.

Usage: python -I -B l117_sides.py CERT.yaml TWIN.json N269_MD HOUSE.yaml IDENTITY.json ISSUE.json OUT.json
"""

from __future__ import annotations

import json
import os
import re
import sys
from fractions import Fraction as F

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l117_check as ck  # noqa: E402
import l117_reader as rd  # noqa: E402

FRAC = re.compile(r"\b(\d{100,})/(\d{100,})\b")


def places(x: F, k: int) -> dict[str, str]:
    return {"floor": ck.floor_places(x, k), "ceil": ck.ceil_places(x, k)}


def main(argv: list[str]) -> int:
    ypath, jpath, mdpath, housepath, idpath, issuepath, opath = argv[1:8]
    rec = rd.read_files(ypath, jpath)
    side = rec["side"]
    assert isinstance(side, tuple)
    S = F(side[0], side[1])
    with open(mdpath, encoding="utf-8") as fh:
        md = fh.read()
    front = yaml.safe_load(md.split("---")[1])
    T_md = F(front["packing"]["reported_upper_bound"]["exact_form"])
    T_ver = F(front["packing"]["verified_upper_bound"]["exact_form"])
    with open(housepath, encoding="utf-8") as fh:
        house = yaml.safe_load(fh)
    T_house = F(house["witness"]["side"])
    with open(idpath, encoding="utf-8") as fh:
        ident = json.load(fh)
    T174 = F(ident["inputs"]["T-174"]["side"])
    with open(issuepath, encoding="utf-8") as fh:
        issue = json.load(fh)
    body = issue["issue"]["body"]
    fracs = [F(int(p), int(q)) for p, q in FRAC.findall(body)]
    T_issue = fracs[0] if fracs else None
    T = T_md
    claim = F("16.899469075856")
    kaggle = F("16.889730079125")
    kirill = F("16.901513582205")
    gain = T - S
    out = {
        "program": "l117_sides.py",
        "side": {
            "floor_40": ck.floor_places(S, 40),
            "12": places(S, 12),
            "15": places(S, 15),
            "16": places(S, 16),
            "binary64": repr(float(S)),
        },
        "claim": {
            "value": "16.899469075856",
            "is_ceil_12": ck.ceil_places(S, 12) == "16.899469075856",
            "claim_less_side": ck.sci(claim - S, 6),
        },
        "T-290": {
            "case_record_equals_verified_exact_form": T_md == T_ver,
            "house_witness_side_equals_case_record": T_house == T_md,
            "issue_fraction_equals_case_record": T_issue == T_md,
            "floor_20": ck.floor_places(T, 20),
            "16": places(T, 16),
            "12": places(T, 12),
        },
        "gain_on_T-290": ck.sci(gain, 12),
        "relative_gain_on_T-290": ck.sci(gain / T, 6),
        "side_less_T-290_negative": S - T < 0,
        "claim_less_T-290_print": ck.sci(F("16.9009945799513249") - claim, 6),
        "T-174": {"floor_20": ck.floor_places(T174, 20), "T-290_less_T-174": ck.sci(T174 - T, 6),
                  "gain_on_T-174": ck.sci(T174 - S, 6)},
        "kaggle_side_only_16.889730079125": {
            "side_less": ck.sci(S - kaggle, 6),
            "claim_less": ck.sci(claim - kaggle, 6),
            "T-290_less": ck.sci(T - kaggle, 6),
        },
        "kirilltym_16.901513582205": {"less_side": ck.sci(kirill - S, 6), "less_T-174": ck.sci(kirill - T174, 6)},
        "quench_prints": {
            v: ck.sci(F(v) - S, 6) for v in ("16.899469084224", "16.899469075879", "16.899469075855")
        },
        "issue_prints": {
            "our exact side 16.8994690758550465": {
                "is_16_floor": ck.floor_places(S, 16) == "16.8994690758550465",
                "less_side": ck.sci(F("16.8994690758550465") - S, 6),
            },
            "sqcheck 16.899469075855047": {"is_15_ceil": ck.ceil_places(S, 15) == "16.899469075855047"},
            "README 16.899469075855046...": {"is_15_floor": ck.floor_places(S, 15) == "16.899469075855046"},
        },
        "pairs_269_choose_2": 269 * 268 // 2,
    }
    with open(opath, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
