"""Gains, contraction margins and identity for each step at 127 (lane r127b-1118).

Usage:

    python -I -B rb127_measure.py T305.yaml E1015.json E1017.json E1020.json \
        ISSUE1015.json ISSUE1017.json ISSUE1020.json OUT.json

For the owner's option D (think-b0w5): a re-certification of a standing packing is a
new result only if its side is below the predecessor's side once the predecessor is
shrunk until its squares first touch. For each step P -> Q this program gives, exactly:

- the gain ``S_P - S_Q``;
- P's contraction margin ``S_P - S_P*``, on P's own certificate (``rb127_contract``);
- whether ``S_Q < S_P*`` (option D's test), the excess ``S_P* - S_Q`` and the ratio of
  the gain to the margin;
- the 12-place prints of ``S_P``, ``S_P*`` and ``S_Q``;
- the identity measurement of Q against P (``rb127_identity``).

Every comparison is between exact fractions. It reads the certificates through the
strict readers and decides nothing about feasibility, which ``rb127_check`` decides; the
shrunk packings are themselves decided by the controls K1c and K1p.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rb127_contract as K  # noqa: E402
import rb127_fmt as F  # noqa: E402
import rb127_identity as ID  # noqa: E402
import rb127_issue as I  # noqa: E402
import rb127_read as R  # noqa: E402
import rb127_twin as T  # noqa: E402

STEPS = [
    ("T-305", "1015"),
    ("T-305", "1017"),
    ("T-305", "1020"),
    ("1015", "1017"),
    ("1017", "1020"),
    ("1015", "1020"),
]


def fr(v: tuple[int, int]) -> Fraction:
    return Fraction(v[0], v[1])


def dec(text: str) -> Fraction:
    whole, _, frac = text.partition(".")
    return Fraction(int(whole + frac), 10 ** len(frac))


def sig_print(f: Fraction, figures: int) -> str:
    """``f`` rounded half away from zero to ``figures`` significant figures, as a plain
    decimal, from the exact value."""
    s = F.sci(f, figures)
    mant, _, exp = s.partition("e")
    e = int(exp)
    digits = mant.replace(".", "").lstrip("-")
    if e < 0:
        return "0." + "0" * (-e - 1) + digits
    whole = digits[: e + 1].ljust(e + 1, "0")
    rest = digits[e + 1:]
    return whole + ("." + rest if rest else "")


def main(argv: list[str]) -> int:
    if len(argv) != 9:
        print(__doc__)
        return 2
    t0 = time.process_time()
    t305 = R.read_form_c(Path(argv[1]).read_bytes())
    certs: dict[str, dict[str, Any]] = {
        "T-305": {"rows": [T.pose_of_corners(c) for c in t305["corners"]], "side": t305["side"]},
    }
    for label, path in zip(("1015", "1017", "1020"), argv[2:5], strict=True):
        J = R.read_form_j(Path(path).read_bytes())
        certs[label] = {"rows": J["rows"], "side": J["side"]}
    issues = {label: I.read_issue(p) for label, p in zip(("1015", "1017", "1020"), argv[5:8], strict=True)}
    out: dict[str, Any] = {"program": "rb127_measure.py", "certificates": {}, "steps": [], "issue_numbers": {}}
    shrunk: dict[str, Fraction] = {}
    for label, c in certs.items():
        k = K.contraction(c["rows"], c["side"])
        S = fr(c["side"])
        shrunk[label] = k["_shrunk_side"]
        entry = {key: v for key, v in k.items() if not key.startswith("_")}
        entry["side_ceil_12"] = F.ceil_places(S, 12)
        entry["side_ceil_16"] = F.ceil_places(S, 16)
        entry["side_nearest_16"] = F.nearest_places(S, 16)
        entry["side_floor_25"] = F.floor_places(S, 25)
        entry["shrunk_side_floor_25"] = F.floor_places(k["_shrunk_side"], 25)
        out["certificates"][label] = entry
    for p, q in STEPS:
        Sp, Sq = fr(certs[p]["side"]), fr(certs[q]["side"])
        gain = Sp - Sq
        margin = Sp - shrunk[p]
        excess = shrunk[p] - Sq
        step: dict[str, Any] = {
            "step": f"{p} -> {q}",
            "gain": F.exact(gain),
            "gain_sci": F.sci(gain, 8),
            "predecessor_margin": F.exact(margin),
            "predecessor_margin_sci": F.sci(margin, 8),
            "successor_below_shrunk_predecessor": Sq < shrunk[p],
            "shrunk_predecessor_less_successor": F.exact(excess),
            "shrunk_predecessor_less_successor_sci": F.sci(excess, 8),
            "gain_over_margin": None if margin == 0 else F.sci(gain / margin, 8),
            "prints_ceil_12": {"predecessor": F.ceil_places(Sp, 12), "shrunk_predecessor": F.ceil_places(shrunk[p], 12),
                               "successor": F.ceil_places(Sq, 12)},
            "prints_floor_16": {"predecessor": F.floor_places(Sp, 16), "shrunk_predecessor": F.floor_places(shrunk[p], 16),
                                "successor": F.floor_places(Sq, 16)},
        }
        step["identity"] = ID.measure(certs[p]["rows"], certs[p]["side"], certs[q]["rows"], certs[q]["side"])
        out["steps"].append(step)
    S305 = fr(certs["T-305"]["side"])
    for label, iss in issues.items():
        S = fr(certs[label]["side"])
        nums: dict[str, Any] = {}
        if iss["house_print"] is not None:
            hp = dec(iss["house_print"])
            nums["house_print"] = iss["house_print"]
            nums["house_print_places"] = len(iss["house_print"].split(".")[1])
            k = nums["house_print_places"]
            nums["t305_side_ceil_at_those_places"] = F.ceil_places(S305, k)
            nums["t305_side_nearest_at_those_places"] = F.nearest_places(S305, k)
            nums["t305_side_floor_at_those_places"] = F.floor_places(S305, k)
            nums["house_print_less_t305_side_sci"] = F.sci(hp - S305, 6)
        if iss["gain_print"] is not None:
            g = S305 - S
            nums["gain_print"] = iss["gain_print"]
            nums["gain_exact_sci"] = F.sci(g, 8)
            nums["gain_two_figures"] = sig_print(g, 2)
            nums["gain_print_is_two_figures"] = iss["gain_print"] == sig_print(g, 2)
        if iss["kaggle_side"] is not None:
            kag = dec(iss["kaggle_side"])
            d = abs(kag - S)
            nums["kaggle_side"] = iss["kaggle_side"]
            nums["kaggle_below_this_packing"] = kag < S
            nums["kaggle_distance_sci"] = F.sci(d, 6)
            nums["kaggle_difference_print"] = iss["kaggle_difference_print"]
            nums["kaggle_difference_sense_stated"] = iss["kaggle_difference_sense"]
            for fig in (2, 3):
                nums[f"kaggle_distance_{fig}_figures"] = sig_print(d, fig)
                nums[f"kaggle_distance_{fig}_figures_sci"] = F.sci(d, fig)
        out["issue_numbers"][label] = nums
    out["cpu_seconds"] = round(time.process_time() - t0, 2)
    Path(argv[8]).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    for s in out["steps"]:
        print(s["step"], "gain", s["gain_sci"], "margin", s["predecessor_margin_sci"],
              "new by option D" if s["successor_below_shrunk_predecessor"] else "not below the shrunk predecessor")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
