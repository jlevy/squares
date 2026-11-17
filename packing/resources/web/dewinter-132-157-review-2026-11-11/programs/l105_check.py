"""Lane L105's checker: decide de Winter's nNNN folder by two methods.

Usage: python -I -B l105_check.py SOURCE_DIR N OUT_JSON

Reads SOURCE_DIR/nN/nN_exact.json and SOURCE_DIR/nN/nN_witness.yaml through
`l105_reader`, decides whether they hold the same packing, and decides each file's
packing by method A (`l105_sat`, Fraction) and method B (`l105_clip`, mpq): every
square, every wall and every pair, with no distance filter.

The verdict is ACCEPT only when, for both files, both methods find every square a
unit square, every square inside its box (clearance >= 0, with equal exact
clearances from the two methods), every pair apart or touching, and the two
methods' classes equal on every wall and every pair.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import l105_clip as B  # noqa: E402
import l105_reader as R  # noqa: E402
import l105_sat as A  # noqa: E402

THRESHOLDS = (-60, -59, -58, -50, -40, -30, -20, -12, -9, -6, -3)
WALLS = ("left", "bottom", "right", "top")


def sci(v: Fraction, digits: int = 6) -> str:
    """Truncated scientific print of an exact rational, by integer arithmetic."""
    if v == 0:
        return "0"
    sign = "-" if v < 0 else ""
    v = abs(v)
    p, q = v.numerator, v.denominator
    e = len(str(p)) - len(str(q))
    if p * 10**max(0, -e) < q * 10**max(0, e):
        e -= 1
    # mantissa digits: floor(v * 10^(digits-1-e))
    sh = digits - 1 - e
    m = (p * 10**sh) // q if sh >= 0 else p // (q * 10 ** (-sh))
    ms = str(m)
    return f"{sign}{ms[0]}.{ms[1:]}e{e:+d}"


def frac_text(v: Fraction) -> str:
    return f"{v.numerator}/{v.denominator}" if v.denominator != 1 else str(v.numerator)


def decide(pk: dict[str, Any], label: str = "") -> dict[str, Any]:
    """Decide one read packing by both methods; returns the full record."""
    n = pk["n"]
    sideF = A.frac(pk["side"])
    sideQ = B.q(pk["side"])
    t0 = time.process_time()
    sa = [A.build(s) for s in pk["squares"]]
    unit_a = [q.unit for q in sa]
    clr_a = [A.clearances(q, sideF) for q in sa]
    margins: list[tuple[int, int, Fraction, int]] = []
    for i in range(n):
        for j in range(i + 1, n):
            m, ax = A.margin(sa[i], sa[j])
            margins.append((i + 1, j + 1, m, ax))
    ta = time.process_time() - t0
    t0 = time.process_time()
    pb = [B.corners(s) for s in pk["squares"]]
    unit_b = [B.is_unit_square(p) for p in pb]
    pccw = [B.ccw(p) for p in pb]
    walls_b = [B.wall_facts(p, sideQ) for p in pccw]
    cont_b = [B.contained(p, sideQ) for p in pccw]
    pair_b: list[tuple[str, Any]] = []
    for i in range(n):
        for j in range(i + 1, n):
            pair_b.append(B.pair_class(pccw[i], pccw[j]))
    tb = time.process_time() - t0

    # agreement
    wall_rows = []
    wall_disagree = 0
    clr_unequal = 0
    for k in range(n):
        for w in range(4):
            ca = clr_a[k][w]
            cls_a = A.wall_class(ca)
            cls_b, clr_b, _ar = walls_b[k][w]
            if cls_a != cls_b:
                wall_disagree += 1
            if Fraction(int(clr_b.numerator), int(clr_b.denominator)) != ca:
                clr_unequal += 1
            wall_rows.append((k + 1, WALLS[w], ca, cls_a, cls_b))
    pair_disagree = []
    classes = {"apart": 0, "contact": 0, "overlap": 0}
    contacts = []
    overlaps = []
    area_sum = 0
    for (i, j, m, ax), (cb, ar) in zip(margins, pair_b, strict=True):
        ca = A.classify(m)
        classes[ca] += 1
        if ca != cb:
            pair_disagree.append((i, j, ca, cb))
        if ca == "contact":
            contacts.append((i, j))
        if ca == "overlap":
            overlaps.append((i, j))
        area_sum += ar
    pos = [r for r in margins if r[2] > 0]
    least = min(margins, key=lambda r: r[2]) if margins else None
    least_pos = min(pos, key=lambda r: r[2]) if pos else None
    below = {}
    for e in THRESHOLDS:
        t = Fraction(1, 10 ** (-e))
        below[f"1e{e}"] = sum(1 for r in pos if r[2] < t)
    wall_contacts = [(k, w) for (k, w, c, ca, cb) in wall_rows if c == 0]
    wall_out = [(k, w) for (k, w, c, ca, cb) in wall_rows if c < 0]
    wpos = [r for r in wall_rows if r[2] > 0]
    wleast = min(wpos, key=lambda r: r[2]) if wpos else None
    wbelow = {}
    for e in THRESHOLDS:
        t = Fraction(1, 10 ** (-e))
        wbelow[f"1e{e}"] = sum(1 for r in wpos if r[2] < t)
    near = sorted((r for r in margins if r[2] < Fraction(1, 1000)), key=lambda r: r[2])
    margin_text = "\n".join(f"{i} {j} {frac_text(m)}" for i, j, m, _ in margins)
    accept = (
        all(unit_a)
        and all(unit_b)
        and all(cont_b)
        and not wall_out
        and wall_disagree == 0
        and clr_unequal == 0
        and not overlaps
        and not pair_disagree
    )
    return {
        "label": label,
        "n": n,
        "side": frac_text(sideF),
        "side_sci": sci(sideF, 20),
        "squares": n,
        "pairs": len(margins),
        "unit_squares_a": sum(unit_a),
        "unit_squares_b": sum(unit_b),
        "contained_b": sum(cont_b),
        "wall_class_disagreements": wall_disagree,
        "wall_clearances_unequal_a_b": clr_unequal,
        "wall_contacts": [{"square": k, "wall": w} for k, w in wall_contacts],
        "walls_outside": [{"square": k, "wall": w} for k, w in wall_out],
        "least_positive_wall_clearance": (
            {"square": wleast[0], "wall": wleast[1], "value": frac_text(wleast[2]), "sci": sci(wleast[2])}
            if wleast
            else None
        ),
        "positive_wall_clearances_below": wbelow,
        "pair_classes_a": classes,
        "pair_class_disagreements": [list(t) for t in pair_disagree[:50]],
        "pair_class_disagreement_count": len(pair_disagree),
        "touching_pairs": [list(t) for t in contacts],
        "overlapping_pairs": [list(t) for t in overlaps[:200]],
        "overlapping_pair_count": len(overlaps),
        "sum_clipped_pair_area_b_sci": sci(Fraction(int(area_sum.numerator), int(area_sum.denominator)))
        if area_sum
        else "0",
        "least_margin": (
            {"pair": [least[0], least[1]], "value": frac_text(least[2]), "sci": sci(least[2])} if least else None
        ),
        "least_positive_margin": (
            {"pair": [least_pos[0], least_pos[1]], "sci": sci(least_pos[2], 12)} if least_pos else None
        ),
        "positive_margins_below": below,
        "near_pairs_below_1e-3": [
            {"pair": [i, j], "sci": sci(m, 12), "axis": ax} for i, j, m, ax in near
        ],
        "margin_list_sha256": hashlib.sha256(margin_text.encode()).hexdigest(),
        "wall_clearances_sci": [
            {"square": k, "wall": w, "sci": sci(c, 8)} for (k, w, c, ca, cb) in wall_rows if c < Fraction(1, 1000)
        ],
        "cpu_seconds": {"method_a": round(ta, 1), "method_b": round(tb, 1)},
        "verdict": "ACCEPT" if accept else "REFUSE",
    }


def run(src: Path, n: int) -> dict[str, Any]:
    d = src / f"n{n}"
    jpath, ypath = d / f"n{n}_exact.json", d / f"n{n}_witness.yaml"
    out: dict[str, Any] = {
        "program": "l105_check.py",
        "python": sys.version.split()[0],
        "files": {},
    }
    for p in (jpath, ypath):
        out["files"][p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    js = R.read_json(jpath)
    ym = R.read_yaml(ypath)
    out["reading"] = {
        "json": {"n": js["n"], "scalars": js["scalars"], "lowest_terms": js["lowest_terms"]},
        "yaml": {
            "n": ym["n"],
            "id": ym["id"],
            "scalars": ym["scalars"],
            "lowest_terms": ym["lowest_terms"],
            "scalar_styles": ym["scalar_styles"],
        },
    }
    out["same_packing"] = R.compare(js, ym)
    out["n_matches_folder"] = js["n"] == n and ym["n"] == n
    out["json"] = decide(js, "json")
    out["yaml"] = decide(ym, "yaml")
    keys = ("verdict", "margin_list_sha256", "wall_contacts", "touching_pairs")
    out["json_yaml_decisions_equal"] = all(out["json"][k] == out["yaml"][k] for k in keys)
    ok = (
        out["n_matches_folder"]
        and out["json"]["verdict"] == "ACCEPT"
        and out["yaml"]["verdict"] == "ACCEPT"
        and out["same_packing"]["same_packing"]
    )
    out["verdict"] = "ACCEPT" if ok else "REFUSE"
    return out


def main() -> None:
    sys.set_int_max_str_digits(0)
    src, n, outp = Path(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3])
    me = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(HERE.glob("l105_*.py"))
        if p.name in ("l105_reader.py", "l105_sat.py", "l105_clip.py", "l105_check.py")
    }
    res = run(src, n)
    res["program_sha256"] = me
    outp.write_text(json.dumps(res, indent=1) + "\n")
    j = res["json"]
    print(
        f"n={n} {res['verdict']} same_packing={res['same_packing']['same_packing']} "
        f"pairs={j['pairs']} classes={j['pair_classes_a']} disagree={j['pair_class_disagreement_count']} "
        f"walls_contacts={len(j['wall_contacts'])} least={j['least_margin']} "
        f"cpu={j['cpu_seconds']} yaml_cpu={res['yaml']['cpu_seconds']}"
    )


if __name__ == "__main__":
    main()
