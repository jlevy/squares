"""Lane L163 check: decide a certificate and its strict variant by both methods.

Usage: l163_check.py LABEL MAIN.json TWIN.cert STRICT.cert STRICT.json OUT.json

MAIN.json is the certificate the claim rests on; TWIN.cert must hold exactly the same
tree. STRICT.cert (the variant whose digest the issue states) and STRICT.json must hold
the same tree as each other, and are decided too, with their exact relation to MAIN.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fractions import Fraction  # noqa: E402

import l163_clip as clip  # noqa: E402
import l163_geom as geom  # noqa: E402
from l163_decide import WALLS, Decision, decide  # noqa: E402
from l163_reader import Certificate, Refused, read_cert, read_json, same_tree  # noqa: E402

THRESHOLDS = [Fraction(1, 10**k) for k in (15, 12, 10, 9, 8, 6, 3)]


def sha(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def fr(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}"


def summary(d: Decision) -> dict[str, object]:
    pos = sorted((m, k) for k, m in d.margins.items() if m > 0)
    least = min(d.margins.values())
    least_pairs = sorted(k for k, m in d.margins.items() if m == least)
    pos_clear = sorted(
        (c, i + 1, WALLS[w]) for i, cl in enumerate(d.clear) for w, c in enumerate(cl) if c > 0
    )
    areas = [a for a in d.area_b.values()]
    return {
        "squares": d.n,
        "pairs": len(d.margins),
        "unit_a": sum(d.unit_a),
        "unit_b": sum(d.unit_b),
        "ccw_b": sum(d.ccw_b),
        "pairs_apart_touch_overlap_a": [
            sum(1 for c in d.class_a.values() if c == x) for x in ("apart", "touch", "overlap")
        ],
        "pairs_apart_touch_overlap_b": [
            sum(1 for c in d.class_b.values() if c == x) for x in ("apart", "touch", "overlap")
        ],
        "pair_classes_agree": d.pair_classes_agree(),
        "sum_overlap_area_b": str(sum(areas, start=clip.mpq(0))),
        "least_margin": fr(least),
        "least_margin_sci": geom.sci(least),
        "least_margin_pairs": [list(k) for k in least_pairs],
        "least_positive_margin_binding_normals": d.binding[least_pairs[0]],
        "positive_pairs_below": {geom.sci(t, 1): sum(1 for m, _ in pos if m < t) for t in THRESHOLDS},
        "least_positive_margins_20": [[list(k), geom.sci(m, 6)] for m, k in pos[:20]],
        "touching_pairs": [list(k) for k in d.touching()],
        "overlapping_pairs": [list(k) for k in d.overlapping()],
        "wall_classes_agree": d.wall_classes_agree(),
        "containment_agrees": d.containment_agrees(),
        "inside_by_area_b": sum(1 for a in d.inside_area_b if a == 1),
        "wall_contacts": [[i, w] for i, w in d.contacts()],
        "wall_contacts_by_wall": {w: sum(1 for _, x in d.contacts() if x == w) for w in WALLS},
        "wall_crossings": [[i, w] for i, w in d.crossings()],
        "least_positive_clearance": None
        if not pos_clear
        else {"value": fr(pos_clear[0][0]), "sci": geom.sci(pos_clear[0][0]), "square": pos_clear[0][1], "wall": pos_clear[0][2]},
        "least_clearance_by_wall": {
            w: (lambda c, i: {"value_sci": geom.sci(c), "square": i + 1, "exact": fr(c)})(
                *min((cl[k], i) for i, cl in enumerate(d.clear))
            )
            for k, w in enumerate(WALLS)
        },
        "positive_clearances_below": {geom.sci(t, 1): sum(1 for c, _, _ in pos_clear if c < t) for t in THRESHOLDS},
        "least_positive_clearances_10": [[i, w, geom.sci(c)] for c, i, w in pos_clear[:10]],
        "margin_list_sha256": d.margin_digest(),
        "clearance_multiset_sha256": d.clearance_multiset_digest(),
        "verdict": "ACCEPT" if d.accepted() else "REFUSE",
    }


def reading(c: Certificate) -> dict[str, object]:
    side = Fraction(*c.side)
    return {
        "n": c.n,
        "scalars": 1 + 3 * c.n,
        "side": fr(side),
        "side_digits_num_den": [len(str(side.numerator)), len(str(side.denominator))],
        "side_floor_30": geom.floor_places(side, 30),
        "t_zero": sum(1 for r in c.squares if r[4] == 0),
        "info": c.info,
    }


def main() -> None:
    label, main_json, twin_cert, strict_cert, strict_json, out = sys.argv[1:7]
    t0 = time.process_time()
    rec: dict[str, object] = {"label": label, "lane": "L163", "program": "l163_check.py"}
    rec["inputs"] = {
        p: {"sha256": sha(p), "bytes": os.path.getsize(p)} for p in (main_json, twin_cert, strict_cert, strict_json)
    }
    try:
        cm = read_json(main_json)
        ct = read_cert(twin_cert)
        cs = read_cert(strict_cert)
    except Refused as exc:
        rec["reader"] = f"REFUSED: {exc.reason}"
        rec["verdict"] = "REFUSE"
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(rec, fh, indent=1)
        print(label, "REFUSE", exc.reason)
        return
    lowest_strict_json = True
    try:
        cj = read_json(strict_json)
    except Refused as exc:
        rec["strict_json_lowest_terms"] = f"REFUSED: {exc.reason}"
        lowest_strict_json = False
        cj = read_json(strict_json, lowest=False)
    rec["reading"] = reading(cm)
    rec["twin_info"] = ct.info
    rec["strict_cert_info"] = cs.info
    rec["twin_equal"] = same_tree(cm, ct)
    if lowest_strict_json:
        rec["strict_twins_equal"] = same_tree(cs, cj)
    else:
        rec["strict_twins_equal_as_values"] = [
            (Fraction(*cs.side), [tuple(Fraction(r[k], r[k + 1]) for k in (0, 2, 4)) for r in cs.squares])
            == (Fraction(*cj.side), [tuple(Fraction(r[k], r[k + 1]) for k in (0, 2, 4)) for r in cj.squares])
        ]
    eps = Fraction(1, 10**15)
    rel = {
        "side_plus_2e-15": Fraction(*cs.side) == Fraction(*cm.side) + 2 * eps,
        "centres_plus_1e-15_each": all(
            Fraction(s[0], s[1]) == Fraction(m[0], m[1]) + eps and Fraction(s[2], s[3]) == Fraction(m[2], m[3]) + eps
            for s, m in zip(cs.squares, cm.squares, strict=True)
        ),
        "t_equal": all(s[4:] == m[4:] for s, m in zip(cs.squares, cm.squares, strict=True)),
    }
    rec["strict_relation"] = rel
    dm = decide(cm)
    rec["main"] = summary(dm)
    t1 = time.process_time()
    ds = decide(cs)
    rec["strict"] = summary(ds)
    rec["strict"]["margins_equal_main"] = ds.margins == dm.margins  # pyright: ignore[reportIndexIssue]
    rec["cpu_seconds"] = {"main": round(t1 - t0, 1), "strict": round(time.process_time() - t1, 1)}
    ok = (
        rec["twin_equal"] is True
        and rec["main"]["verdict"] == "ACCEPT"  # pyright: ignore[reportIndexIssue]
    )
    rec["verdict"] = "ACCEPT" if ok else "REFUSE"
    rec["versions"] = {"python": sys.version.split()[0], **clip.versions()}
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1)
    m = rec["main"]
    print(
        label,
        rec["verdict"],
        "pairs",
        m["pairs"],  # pyright: ignore[reportIndexIssue]
        "least",
        m["least_margin_sci"],  # pyright: ignore[reportIndexIssue]
        "contacts",
        m["wall_contacts_by_wall"],  # pyright: ignore[reportIndexIssue]
        "strict",
        rec["strict"]["verdict"],  # pyright: ignore[reportIndexIssue]
        "cpu",
        rec["cpu_seconds"],
    )


if __name__ == "__main__":
    main()
