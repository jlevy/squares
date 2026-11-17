"""Lane L105, after the freeze and after L104's branch appeared: the lane against the review.

Usage: python -I -B l105_compare_lane.py REPO_DIR LANE_COMMIT PACKET_DIR OUT_JSON

Decides nothing. Reads lane L104's files at LANE_COMMIT through `git show` (its two
packets' claim records, exact-certification receipts, sharp controls, contraction and
identity receipts, its register entries' prints and its ledger) and holds each to this
review's receipts in PACKET_DIR/out. Prints LANE_EQUALS_REVIEW when every comparison
holds, else the comparisons that do not.
"""

from __future__ import annotations

import hashlib
import json
import lzma
import re
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any

import yaml


def show(repo: Path, commit: str, path: str) -> bytes:
    return subprocess.run(["git", "-C", str(repo), "show", f"{commit}:{path}"], check=True, capture_output=True).stdout


def fr(t: str) -> F:
    return F(t)


def ceil_places(v: F, k: int) -> F:
    return F(-((-v.numerator * 10**k) // v.denominator), 10**k)


def main() -> None:
    sys.set_int_max_str_digits(0)
    repo, commit, pkt, outp = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
    out_dir = pkt / "out"
    rows: list[dict[str, Any]] = []

    def cmp(name: str, lane: Any, review: Any, ok: bool) -> None:
        rows.append({"comparison": name, "lane": lane, "review": review, "equal": bool(ok)})

    sides = json.loads((out_dir / "sides.json").read_text())["counts"]
    construct = json.loads((out_dir / "construct.json").read_text())["counts"]
    custody = json.loads((out_dir / "custody.json").read_text())
    ledger = yaml.safe_load(show(repo, commit, "packing/campaign/issue-intake/upper-bounds-de-winter-132-157-20261111/ledger.yaml"))
    for n in (132, 157):
        base = f"packing/resources/web/de-winter-s{n}-upper-bound-2026-11-11"
        mine = json.loads((out_dir / f"check-n{n}.json").read_text())
        my_side = fr(mine["json"]["side"])
        my_least = fr(mine["json"]["least_margin"]["value"])
        my_pair = sorted(mine["json"]["least_margin"]["pair"])
        claims = json.loads(show(repo, commit, f"{base}/acquisition/claims.json"))["results"][0]
        cmp(f"{n}: exact side", claims["exact_side"][:24] + "…", mine["json"]["side"][:24] + "…", fr(claims["exact_side"]) == my_side)
        cmp(f"{n}: offered side is the 12-place ceiling", claims["offered_side"], sides[str(n)]["ceil12"], F(claims["offered_side"]) == ceil_places(my_side, 12))
        ec = json.loads(lzma.decompress(show(repo, commit, f"{base}/receipts/exact-certification.json.xz")))
        pos = [c for c in ec["cases"] if c["control"] == "positive"]
        ctl = [c for c in ec["cases"] if c["control"] != "positive"]
        for route in ("exact_verify", "independent"):
            r = pos[0][route]
            cmp(f"{n}: {route} accepts", r["verification_passed"], mine["verdict"], r["verification_passed"] and mine["verdict"] == "ACCEPT")
            cmp(f"{n}: {route} least pair gap equals the review's least margin", r["minimum_best_pair_gap"][:20] + "…", mine["json"]["least_margin"]["value"][:20] + "…", fr(r["minimum_best_pair_gap"]) == my_least)
            cmp(f"{n}: {route} least containment clearance", r["minimum_containment_clearance"], "0 (wall contacts)", fr(r["minimum_containment_clearance"]) == 0 and len(mine["json"]["wall_contacts"]) > 0)
            cmp(f"{n}: {route} pairs tested", r["pairs_tested"], mine["json"]["pairs"], r["pairs_tested"] == mine["json"]["pairs"])
            cmp(f"{n}: {route} side", "exact", "exact", fr(r["side"]) == my_side)
        cmp(f"{n}: both controls refused on both routes", [c["control"] for c in ctl], "G1 and G2 refused here", all(not c[rt]["verification_passed"] for c in ctl for rt in ("exact_verify", "independent")) and len(ctl) == 2)
        sharp = show(repo, commit, f"{base}/receipts/sharp-controls.json").decode()
        tight = re.findall(r'"square": (\d+)', sharp)
        cmp(f"{n}: the sharp controls' tightest pair contains the review's least pair's square", tight[0], my_pair, int(tight[0]) in my_pair)
        own = json.loads(show(repo, commit, f"{base}/measure/contraction-n{n}-own.json"))
        model = construct[str(n)]["side_above_scaled_back_configuration"]["side_above_solution_sci"]
        cmp(f"{n}: own contraction margin against the review's scaled-back side", own["margin_float"], model, abs(float(own["margin_float"]) - float(model)) / float(model) < 1e-5)
        cmp(f"{n}: one minus lambda star is the review's epsilon", own["one_minus_lambda_star"], "1e-60", abs(float(own["one_minus_lambda_star"]) - 1e-60) < 1e-66)
        # retained source files against the review's custody digests
        for name in (f"n{n}_exact.json", f"n{n}_witness.yaml", "verify_exact.py", "SHA256SUMS", "README.md"):
            path = f"{base}/source/n{n}/{name}"
            try:
                data = show(repo, commit, path)
            except subprocess.CalledProcessError:
                continue
            cmp(f"{n}: retained {name}", hashlib.sha256(data).hexdigest()[:16], custody["folders"][f"n{n}"]["files"][name]["sha256"][:16], hashlib.sha256(data).hexdigest() == custody["folders"][f"n{n}"]["files"][name]["sha256"])
        # ledger dating
        led = [c for r in ledger["reports"] for c in r["claims"] if c["n"] == n]
        cmp(f"{n}: ledger first commit is a491dad's", led[0].get("first_committed"), custody["commits"]["a491dad"]["committed"], led[0].get("first_committed") == "2026-11-11T20:49:44Z")
    # identity at 132
    ident = json.loads(show(repo, commit, "packing/resources/web/de-winter-s132-upper-bound-2026-11-11/measure/identity.json"))
    mine_id = json.loads((out_dir / "identity-n132.json").read_text())
    lane_rows = [p for p in ident["pairs"] if p.get("against") == "T-174"]
    a = lane_rows[0]["assignment"]
    cmp("132: identity against T-174, beyond 0.1 and largest move", [a["moved_beyond"]["1e-1"], a["largest_move"]], [mine_id["best"]["beyond_0.1"], mine_id["best"]["largest_move"]], a["moved_beyond"]["1e-1"] == mine_id["best"]["beyond_0.1"] and abs(float(a["largest_move"]) - mine_id["best"]["largest_move"]) < 1e-3)
    cmp("132: no symmetry one to one", lane_rows[0]["nearest_centre"]["one_to_one"], mine_id["one_to_one_anywhere"], lane_rows[0]["nearest_centre"]["one_to_one"] is False and mine_id["one_to_one_anywhere"] is False)
    # the register's 16-place prints
    text = show(repo, commit, "packing/frontier/results.yaml").decode()
    for n, tid in ((132, "T-292"), (157, "T-293")):
        blk = text[text.index(f"  - id: {tid}\n"):]
        m = re.search(r"That side is ([0-9.]+) rounded up at 16 places and ([0-9.]+) at 12", blk)
        mine = json.loads((out_dir / f"check-n{n}.json").read_text())
        S = fr(mine["json"]["side"])
        cmp(f"{n}: the entry's 16-place print is the ceiling", m.group(1), "ceil16", F(m.group(1)) == ceil_places(S, 16))
        cmp(f"{n}: the entry's 12-place print is the ceiling", m.group(2), sides[str(n)]["ceil12"], F(m.group(2)) == ceil_places(S, 12))
        sc = re.search(r"significance:\n      score: (\d)", blk)
        cmp(f"{n}: draft significance", f"S{sc.group(1)}", "S3", sc.group(1) == "3")
    bad = [r["comparison"] for r in rows if not r["equal"]]
    out = {"program": "l105_compare_lane.py", "lane_commit": commit, "comparisons": rows, "status": "LANE_EQUALS_REVIEW" if not bad else "DIFFERS", "differing": bad}
    outp.write_text(json.dumps(out, indent=1, default=str) + "\n")
    print(out["status"], len(rows), "comparisons", bad)


if __name__ == "__main__":
    main()
