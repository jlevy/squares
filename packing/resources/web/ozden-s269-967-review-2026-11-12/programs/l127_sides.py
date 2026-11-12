"""The claim's arithmetic, exactly. Written and run after the findings were frozen.

Lane L127, clean room; decides nothing about the certificate. Usage:

    python -I -B l127_sides.py CERT.yaml TWIN.json MAIN_RESULTS.yaml BRANCH_RESULTS.yaml \
        MAIN_HOUSE.yaml BRANCH_HOUSE.yaml CERT_962.yaml POSE.yaml ISSUE.json \
        CONTRACTION_NEW.json OUT.json

MAIN_RESULTS is packing/frontier/results.yaml on main (T-290); BRANCH_RESULTS the
same file on PR #966's branch (#962's entry). The house witnesses and #962's certificate are
read only for their sides, to check them against the register's fractions.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l127_reader as rd  # noqa: E402


def floor_dec(x: F, places: int) -> str:
    q = x.numerator * 10**places // x.denominator
    s = str(q).rjust(places + 1, "0")
    return f"{s[:-places]}.{s[-places:]}"


def ceil_dec(x: F, places: int) -> str:
    q = -((-x.numerator * 10**places) // x.denominator)
    s = str(q).rjust(places + 1, "0")
    return f"{s[:-places]}.{s[-places:]}"


def sci(x: F, sig: int = 6) -> str:
    return f"{float(x):.{sig - 1}e}"


def register_side(text: str, tid: str) -> F:
    m = re.search(rf"- id: {tid}\n.*?proves s\(269\) <=\s+([0-9]+/[0-9]+)\.", text, re.S)
    assert m is not None, tid
    return F(m.group(1))


def witness_side(text: str) -> F:
    m = re.search(r"^  side: '?([0-9]+(?:[./][0-9]+)?)'?$", text, re.M)
    assert m is not None
    return F(m.group(1))


def rounds_to(printed: str, x: F) -> dict[str, Any]:
    """Whether a printed decimal (plain or e-notation) is x rounded to its own digits."""
    p = printed.strip()
    if "e" in p:
        mant, exp = p.split("e")
        digits = len(mant.replace(".", "").replace("-", "").lstrip("0"))
        e = int(exp)
        # x rounded to `digits` significant figures at exponent e
        scale = F(10) ** (e - (digits - 1))
        r = round(x / scale) * scale
        return {"printed": p, "value": sci(x, 8), "rounds_to_nearest": F(p) == r}
    places = len(p.split(".")[1]) if "." in p else 0
    return {
        "printed": p,
        "floor": floor_dec(x, places) == p,
        "ceil": ceil_dec(x, places) == p,
        "nearest": floor_dec(x + F(1, 2 * 10**places), places) == p,
    }


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main(argv: list[str]) -> int:
    paths = [Path(a) for a in argv[1:12]]
    cert, twin, mres, bres, mhouse, bhouse, c962, pose, issue, cnew, out = paths
    doc = rd.read_certificate(cert.read_text(encoding="utf-8"), twin.read_text(encoding="utf-8"))
    s = F(*doc["side"])
    mtext = mres.read_text(encoding="utf-8")
    btext = bres.read_text(encoding="utf-8")
    t290 = register_side(mtext, "T-290")
    t962 = register_side(btext, "T-296")  # the register id PR #966 gives #962
    house_main = witness_side(mhouse.read_text(encoding="utf-8"))
    house_branch = witness_side(bhouse.read_text(encoding="utf-8"))
    side962 = witness_side(c962.read_text(encoding="utf-8"))
    pose_side = witness_side(pose.read_text(encoding="utf-8"))
    iss = json.loads(issue.read_text(encoding="utf-8"))
    body = iss["issue"]["body"]
    m = re.search(r"≤ ([0-9.]+)", iss["issue"]["title"])
    assert m is not None
    claim = F(m.group(1))
    m290 = re.search(r"The record holds `([0-9]+/[0-9]+) = ", body)
    assert m290 is not None
    issue_t290 = F(m290.group(1))
    kaggle = F("16.889730079125")
    kirill = F("16.901513582205")
    cloud = F("16.88973007359575")
    quench1 = F("16.890507465412")
    kick1 = F("16.889734433328")
    parent = F("16.890507620785")
    cn = json.loads(cnew.read_text(encoding="utf-8"))
    contracted = F(cn["contracted_side"])

    out_d: dict[str, Any] = {
        "program": "l127_sides.py",
        "inputs": {p.name: sha(p) for p in paths[:-1]},
        "side_floor_40": floor_dec(s, 40),
        "side_floor_12": floor_dec(s, 12),
        "side_ceil_12": ceil_dec(s, 12),
        "claim": str(claim),
        "claim_is_ceil_12": ceil_dec(s, 12) == m.group(1),
        "claim_minus_side": sci(claim - s),
        "t290": {
            "floor_20": floor_dec(t290, 20),
            "register_equals_main_house_witness": t290 == house_main,
            "register_equals_issue_fraction": t290 == issue_t290,
            "print_16_ceil": ceil_dec(t290, 16),
            "gain": sci(t290 - s, 12),
            "relative_to_t290": sci((t290 - s) / t290, 6),
            "relative_to_side": sci((t290 - s) / s, 6),
        },
        "t962": {
            "floor_20": floor_dec(t962, 20),
            "register_equals_branch_house_witness": t962 == house_branch,
            "register_equals_962_source_certificate": t962 == side962,
            "print_16_ceil": ceil_dec(t962, 16),
            "print_16_floor": floor_dec(t962, 16),
            "print_12_ceil": ceil_dec(t962, 12),
            "gain": sci(t962 - s, 12),
            "relative_to_t962": sci((t962 - s) / t962, 6),
        },
        "kaggle": {
            "value": "16.889730079125",
            "kaggle_minus_side": sci(kaggle - s, 8),
            "kaggle_minus_claim": sci(kaggle - claim, 8),
            "side_below": s < kaggle,
            "claim_below": claim < kaggle,
            "kaggle_minus_half_unit_minus_claim": sci(kaggle - F(5, 10**13) - claim, 8),
        },
        "kirilltym_minus_side": sci(kirill - s, 8),
        "pose": {
            "pose_side": str(pose_side),
            "pose_minus_side": sci(pose_side - s, 6),
            "pose_minus_cloud": sci(pose_side - cloud, 6),
            "side_minus_cloud": sci(s - cloud, 6),
            "claim_minus_cloud": sci(claim - cloud, 6),
            "quench_minus_side": sci(quench1 - s, 6),
            "kick_minus_side": sci(kick1 - s, 6),
            "parent_minus_quench": sci(parent - quench1, 6),
        },
        "contracted_side_floor_16": floor_dec(contracted, 16),
        "contracted_below_side": sci(s - contracted, 6),
        "prints": {
            "issue exact side 16.889730073595636": rounds_to("16.889730073595636", s),
            "sqcheck 16.889730073595637": rounds_to("16.889730073595637", s),
            "claim 16.889730073596": rounds_to("16.889730073596", s),
            "#962 as 16.8994690758550465": rounds_to("16.8994690758550465", t962),
            "#962 as 16.899469075856": rounds_to("16.899469075856", t962),
            "T-290 as 16.9009945799513249": rounds_to("16.9009945799513249", t290),
            "gain on T-290 1.126e-02": rounds_to("1.126e-02", t290 - s),
            "gain on T-290 1.1265e-2": rounds_to("1.1265e-2", t290 - s),
            "gain on T-290 1.13e-2": rounds_to("1.13e-2", t290 - s),
            "relative 6.66e-04 (of T-290)": rounds_to("6.66e-04", (t290 - s) / t290),
            "gain on #962 9.74e-3": rounds_to("9.74e-3", t962 - s),
            "below Kaggle 5.53e-9": rounds_to("5.53e-9", kaggle - s),
            "below Kaggle 5.5e-9": rounds_to("5.5e-9", kaggle - s),
            "below kirilltym 1.18e-2": rounds_to("1.18e-2", kirill - s),
            "comment: below #947's side by 9.74e-3": rounds_to("9.74e-3", t290 - s),
        },
    }
    out.write_text(json.dumps(out_d, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out_d, indent=1)[:4000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
