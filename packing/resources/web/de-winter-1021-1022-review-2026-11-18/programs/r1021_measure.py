"""Measurements of lane r1021-1118: sides and prints, option D, identity, the house witnesses.

Usage, from this packet's programs/ directory:

    python -I -B r1021_measure.py SRC_DIR HOUSE268 HOUSE270 WIT268 WIT270 OUT.json

SRC_DIR holds the four de Winter files (n268_exact.json, n268_witness.yaml,
n270_exact.json, n270_witness.yaml); HOUSE268 and HOUSE270 are the houses'
certificates (T-289's and T-283's Witness/v2 corner files); WIT268 and WIT270 the
house witnesses on main (centre-basis), compared square for square with the houses'
certificates.  It decides each shrunk predecessor by both methods (r1021_check.decide)
and measures; every comparison of sides is exact.
"""

from __future__ import annotations

import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # this packet's programs/, run with -I

import json
import os
import sys
import time
from fractions import Fraction

import r1021_check as chk
import r1021_contract as con
import r1021_geom as geom
import r1021_identity as ident
import r1021_read as rd
from r1021_fmt import ceil_places, floor_places, frac_text, sci

ISSUE = {
    268: {"issue": 1021, "claim_print": "16.870013850405", "house_print": "16.87202984908445", "gain_print": "0.0020",
          "close_pairs": 620,
          "others": {"Polkovskyi #1009": "16.871868135", "Kaggle Thinking inside the box": "16.870013850412470"}},
    270: {"issue": 1022, "claim_print": "16.927314216352", "house_print": "16.928148603342855", "gain_print": "0.00083",
          "close_pairs": 642,
          "others": {"Panoras compilation": "16.92746606488242", "Malyshev #1012": "16.927469593519",
                     "Kaggle [NUP] Junie is all you need": "16.927314216351814"}},
}


def dec_fraction(text: str) -> Fraction:
    return Fraction(text)


def print_facts(side: Fraction) -> dict:
    return {"exact": frac_text(side), "floor_30": floor_places(side, 30), "ceil_12": ceil_places(side, 12),
            "ceil_16": ceil_places(side, 16), "floor_16": floor_places(side, 16)}


def contraction_facts(poses, side: Fraction, label: str) -> tuple[dict, dict]:
    t0 = time.process_time()
    c = con.contraction(poses, side)
    dec = chk.decide(c["shrunk_poses"], [geom.corners_of(p) for p in c["shrunk_poses"]], c["shrunk_side"])
    n = len(poses)
    pairs = geom.pair_index(n)
    touching = [pairs[k] for k, cl in enumerate(dec["a_classes"]) if cl == "contact"]
    facts = {
        "label": label,
        "lambda_exact": frac_text(c["lambda"]),
        "one_less_lambda": sci(c["one_less_lambda"], 8),
        "binding_pairs": [[i + 1, j + 1] for i, j in c["binding"]],
        "next_factor_below_lambda_by": sci(c["lambda"] - c["next_factor"], 4) if c["next_factor"] is not None else None,
        "shrunk_side_30": floor_places(c["shrunk_side"], 30),
        "shrunk_side_exact": frac_text(c["shrunk_side"]),
        "shrunk_width_less_height": sci(c["shrunk_width"] - c["shrunk_height"], 6),
        "margin": sci(c["margin"], 10),
        "margin_exact": frac_text(c["margin"]),
        "slack_side_less_extent": sci(c["slack"], 8),
        "closed_by_contraction": sci(c["closed_by_contraction"], 8),
        "shrunk_packing": {
            "accept_by_both": dec["accept"],
            "touching_pairs": [[i + 1, j + 1] for i, j in touching],
            "touching_equals_binding": touching == c["binding"],
            "a_overlaps": len(dec["a_overlap"]),
            "b_overlaps": len(dec["b_overlap"]),
            "disagreements": len(dec["pair_disagree"]) + len(dec["wall_disagree"]),
        },
        "cpu": round(time.process_time() - t0, 2),
    }
    return facts, c


def house_witness_compare(cert_poses, cert_side: Fraction, raw_witness: bytes) -> dict:
    w = rd.read_center_basis(raw_witness)
    same_side = w["side"] == cert_side
    centre_diff = []
    basis_diff = []
    for k, (p, q) in enumerate(zip(cert_poses, w["poses"], strict=True)):
        if (p[0], p[1]) != (q[0], q[1]):
            centre_diff.append(k + 1)
        dirs = {(p[2], p[3]), (-p[3], p[2]), (-p[2], -p[3]), (p[3], -p[2])}
        if (q[2], q[3]) not in dirs:
            basis_diff.append(k + 1)
    return {"sha256": w["sha256"], "n": w["n"], "same_side": same_side, "centres_differ": centre_diff[:20],
            "centres_differ_count": len(centre_diff), "basis_not_an_edge_direction": basis_diff[:20],
            "basis_differ_count": len(basis_diff)}


def main(argv: list[str]) -> int:
    if len(argv) != 6:
        print(__doc__)
        return 2
    src, h268, h270, w268, w270, out = argv
    t_all = time.process_time()
    result: dict = {"counts": {}}
    for n, hpath, wpath, house_id in ((268, h268, w268, "T-289"), (270, h270, w270, "T-283")):
        with open(os.path.join(src, f"n{n}_exact.json"), "rb") as f:
            fj = rd.read_form_j(f.read())
        with open(os.path.join(src, f"n{n}_witness.yaml"), "rb") as f:
            fc = rd.read_corners(f.read(), "square-k", "form C")
        with open(hpath, "rb") as f:
            fh = rd.read_corners(f.read(), "int", "house file")
        with open(wpath, "rb") as f:
            raw_w = f.read()
        succ = fj["rows"]
        succ_c = [geom.pose_of_corners(q)[1] for q in fc["squares"]]
        house = [geom.pose_of_corners(q)[1] for q in fh["squares"]]
        s_succ, s_house = fj["side"], fh["side"]
        info = ISSUE[n]
        entry: dict = {"issue": info["issue"], "house": house_id}
        entry["sides"] = {"successor": print_facts(s_succ), "house": print_facts(s_house)}
        claim = Fraction(info["claim_print"])
        entry["claim"] = {
            "print": info["claim_print"],
            "is_ceil_12_of_side": ceil_places(s_succ, 12) == info["claim_print"],
            "claim_less_side": sci(claim - s_succ, 8),
            "claim_at_least_side": claim >= s_succ,
            "side_text_same_in_both_files": fj["side_text"] == fc["side_text"],
        }
        hp = Fraction(info["house_print"])
        places = len(info["house_print"].split(".")[1])
        entry["house_print"] = {
            "print": info["house_print"],
            "print_less_house_side": sci(hp - s_house, 6),
            "is_ceil_at_its_places": ceil_places(s_house, places) == info["house_print"],
            "is_floor_at_its_places": floor_places(s_house, places) == info["house_print"],
        }
        gain = s_house - s_succ
        entry["gain"] = {"exact": frac_text(gain), "sci": sci(gain, 10), "issue_print": info["gain_print"]}
        others = {}
        for name, text in info["others"].items():
            others[name] = {"value": text, "value_less_successor": sci(Fraction(text) - s_succ, 6)}
        entry["others_printed"] = others
        f_succ, c_succ = contraction_facts(succ, s_succ, f"#{info['issue']}")
        f_succ_c, c_succ_c = contraction_facts(succ_c, s_succ, f"#{info['issue']} from form C")
        f_house, c_house = contraction_facts(house, s_house, house_id)
        entry["contraction"] = {"successor": f_succ, "house": f_house,
                                "successor_form_c_equal": (c_succ["lambda"] == c_succ_c["lambda"]
                                                           and c_succ["shrunk_side"] == c_succ_c["shrunk_side"]
                                                           and c_succ["binding"] == c_succ_c["binding"])}
        od = con.option_d(s_house, c_house, s_succ)
        entry["option_d"] = {
            "step": f"{house_id} -> #{info['issue']}",
            "gain": sci(od["gain"], 10),
            "predecessor_margin": sci(od["predecessor_margin"], 10),
            "gain_over_margin": sci(od["gain_over_margin"], 8) if od["gain_over_margin"] is not None else None,
            "successor_below_shrunk_predecessor_by": sci(od["successor_below_shrunk_predecessor_by"], 10),
            "new_under_option_d": od["new_under_option_d"],
            "prints_12": [ceil_places(s_house, 12), ceil_places(c_house["shrunk_side"], 12), ceil_places(s_succ, 12)],
            "floors_16": [floor_places(s_house, 16), floor_places(c_house["shrunk_side"], 16), floor_places(s_succ, 16)],
        }
        t0 = time.process_time()
        entry["identity"] = ident.measure(house, s_house, succ, s_succ)
        entry["identity"]["cpu"] = round(time.process_time() - t0, 2)
        entry["house_witness_on_main"] = house_witness_compare(house, s_house, raw_w)
        result["counts"][str(n)] = entry
        print(n, "gain", entry["option_d"]["gain"], "margin", entry["option_d"]["predecessor_margin"],
              "new", entry["option_d"]["new_under_option_d"], "nearest", entry["identity"]["nearest_symmetry"],
              "one-to-one", entry["identity"]["one_to_one_under"])
    result["cpu_total"] = round(time.process_time() - t_all, 2)
    with open(out, "w") as f:
        json.dump(result, f, indent=1)
        f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
