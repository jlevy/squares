"""Run the controls of controls-plan.json and compare each with its stated outcome.

Usage: python -I -B l101_controls.py WITNESS.yaml TWIN.json N PLAN.json FACTS.json OUT.json

Written after the plan was stated and hashed. Every geometric control is decided by both
frozen methods through l101_check.decide or directly by l101_sat and l101_clip; every
reader control by l101_reader on modified texts.
"""

from __future__ import annotations

import copy
import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
# The frozen l101_check.frac_str writes exact fractions; summed overlap areas in the
# reflected control (G6) run past CPython's default 4,300-digit limit on int-to-str.
# The limit is lifted for this process; no checker file is changed.
sys.set_int_max_str_digits(0)

from gmpy2 import mpq  # noqa: E402

import l101_clip as clip  # noqa: E402
import l101_geom as geom  # noqa: E402
import l101_reader as reader  # noqa: E402
import l101_sat as sat  # noqa: E402
from l101_check import decide, frac_str, program_digests, sci, sha256_file  # noqa: E402

D30 = F(1, 10**30)
OUTWARD = {"left": (-1, 0), "bottom": (0, -1), "right": (1, 0), "top": (0, 1)}


def pairs_of(i: int, n: int) -> list[tuple[int, int]]:
    return [(min(i, k), max(i, k)) for k in range(n) if k != i]


def brief(r: dict) -> dict:
    keys = ("verdict", "not_unit_A", "not_unit_B", "senses_agree", "wall_contacts", "wall_outside",
            "wall_disagreements", "pair_disagreements", "overlapping_pairs", "touching_pairs",
            "pair_classes_A", "pair_classes_B", "pairs_decided", "walls_decided", "margins_sha256",
            "inside_area_not_1")
    out = {k: r[k] for k in keys if k in r}
    shortened = []
    for o in out.get("overlapping_pairs", []):
        o = dict(o)
        for key in ("margin", "area"):
            if len(o[key]) > 200:
                num, den = (int(x) for x in o[key].split("/"))
                o[key] = "~" + sci(F(num, den))
        shortened.append(o)
    if "overlapping_pairs" in out:
        out["overlapping_pairs"] = shortened
    if len(out.get("overlapping_pairs", [])) > 12:
        out["overlapping_pairs_count"] = len(out["overlapping_pairs"])
        out["overlapping_pairs"] = out["overlapping_pairs"][:12]
    return out


def reader_refusal(ytext: str, jtext: str, n: int) -> str | None:
    try:
        reader.read_texts(ytext, jtext, n)
    except reader.ReadError as error:
        return str(error)
    return None


def pair_level(pa: list, pb: list) -> tuple[str, F, str, F]:
    a, b = sat.make_square(pa), sat.make_square(pb)
    qa, qb = clip.make_square(pa), clip.make_square(pb)
    assert not isinstance(a, str) and not isinstance(b, str)
    assert not isinstance(qa, str) and not isinstance(qb, str)
    m = sat.pair_margin(a, b)
    cb, area = clip.pair(qa, qb)
    return sat.classify(m), m, cb, F(int(area.numerator), int(area.denominator))


def wall_level(points: list, side: F, wall: str) -> tuple[str, str]:
    a, q = sat.make_square(points), clip.make_square(points)
    assert not isinstance(a, str) and not isinstance(q, str)
    ca = sat.wall_class(sat.wall_clearances(a, side)[wall])
    cb, _ = clip.wall(q, clip.outer_planes(mpq(side.numerator, side.denominator))[wall])
    return ca, cb


def main() -> int:
    ypath, jpath, n_text, plan_path, facts_path, out_path = sys.argv[1:7]
    start = time.process_time()
    n = int(n_text)
    ytext = Path(ypath).read_text(encoding="utf-8")
    jtext = Path(jpath).read_text(encoding="utf-8")
    w = reader.read_texts(ytext, jtext, n)
    plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    facts = json.loads(Path(facts_path).read_text(encoding="utf-8"))
    stated = {c["id"]: c["stated"] for c in plan["controls"]}
    side = F(*w.side)
    base = [list(s) for s in w.squares]
    results = []

    def record(cid: str, observed: dict, ok: bool) -> None:
        results.append({"id": cid, "stated": stated[cid], "observed": observed, "as_stated": bool(ok)})
        print(cid, "as stated" if ok else "NOT AS STATED", flush=True)

    # G1
    s = copy.deepcopy(base)
    s[n - 1] = s[0]
    r = decide(w.side, s, pair_list=pairs_of(n - 1, n), wall_squares=[n - 1])
    ov = r["overlapping_pairs"]
    record("G1", brief(r), r["verdict"] == "REFUSE" and [o["pair"] for o in ov] == [[1, n]]
           and ov[0]["margin"] == "-1" and ov[0]["area"] == "1" and r["touching_pairs"] == []
           and r["wall_outside"] == [] and not r["pair_disagreements"])

    # G2
    s = copy.deepcopy(base)
    s[0] = geom.translate(s[0], side, F(0))
    r = decide(w.side, s, pair_list=pairs_of(0, n), wall_squares=[0])
    record("G2", brief(r), r["verdict"] == "REFUSE" and r["wall_outside"] == [[1, "right"]]
           and r["overlapping_pairs"] == [] and r["touching_pairs"] == []
           and not r["wall_disagreements"] and not r["pair_disagreements"])

    # G3, G4, G7, G9: the reader
    lines = ytext.split("\n")
    last = lines.index(f"  - id: {n}")
    claim = lines.index("  claim:")
    jtree = json.loads(jtext)
    t3 = copy.deepcopy(jtree)
    t3["witness"]["squares"].pop()
    why = reader_refusal("\n".join(lines[:last] + lines[claim:]), json.dumps(t3), n)
    record("G3", {"reader": why}, why is not None and stated["G3"]["reason_contains"] in why)
    t4 = copy.deepcopy(jtree)
    t4["witness"]["squares"][-1]["id"] = 1
    l4 = list(lines)
    l4[last] = "  - id: 1"
    why = reader_refusal("\n".join(l4), json.dumps(t4), n)
    record("G4", {"reader": why}, why is not None and stated["G4"]["reason_contains"] in why)
    t7 = copy.deepcopy(jtree)
    side_text = t7["witness"]["side"]
    t7["witness"]["side"] = side_text[:-1] + ("1" if side_text[-1] != "1" else "3")
    why = reader_refusal(ytext, json.dumps(t7), n)
    record("G7", {"reader": why}, why is not None and stated["G7"]["reason_contains"] in why)
    p, q = w.side
    doubled = f"{2 * p}/{2 * q}"
    side_line = [k for k, line in enumerate(lines) if line.startswith("  side: ")]
    l9 = list(lines)
    l9[side_line[0]] = f"  side: {doubled}"
    t9 = copy.deepcopy(jtree)
    t9["witness"]["side"] = doubled
    why = reader_refusal("\n".join(l9), json.dumps(t9), n)
    record("G9", {"reader": why, "side_lines": len(side_line)},
           len(side_line) == 1 and why is not None and stated["G9"]["reason_contains"] in why)

    # G5
    s = copy.deepcopy(base)
    pts = geom.to_fracs(s[0])
    pts[2] = (pts[2][0] + D30, pts[2][1])
    s[0] = geom.to_ints(pts)
    r = decide(w.side, s, pair_list=pairs_of(0, n), wall_squares=[0])
    record("G5", brief(r), r["verdict"] == "REFUSE" and [x[0] for x in r["not_unit_A"]] == [1]
           and [x[0] for x in r["not_unit_B"]] == [1])

    # G6
    s = [geom.reflect_horizontal(x) for x in base]
    r = decide(w.side, s)
    st = stated["G6"]
    record("G6", brief(r), r["verdict"] == "REFUSE" and len(r["overlapping_pairs"]) > 0
           and not r["not_unit_A"] and not r["not_unit_B"]
           and sorted(r["wall_contacts"]) == st["wall_contacts"] and r["wall_outside"] == []
           and not r["wall_disagreements"] and not r["pair_disagreements"])

    # G8
    s = [geom.transpose(x) for x in base]
    r = decide(w.side, s)
    st = stated["G8"]
    record("G8", brief(r), r["verdict"] == "ACCEPT" and sorted(r["wall_contacts"]) == st["wall_contacts"]
           and r["margins_sha256"] == st["margins_sha256"]
           and not r["wall_disagreements"] and not r["pair_disagreements"])

    # S1a to S1d: the side
    def side_control(cid: str, new_side: F) -> dict:
        return decide((new_side.numerator, new_side.denominator), base, pair_list=[])

    r = side_control("S1a", F(p - 1, q))
    record("S1a", brief(r), r["verdict"] == "REFUSE" and r["wall_outside"] == stated["S1a"]["wall_outside"]
           and not r["wall_disagreements"])
    r = side_control("S1b", side - D30)
    record("S1b", brief(r), r["verdict"] == "REFUSE" and r["wall_outside"] == stated["S1b"]["wall_outside"]
           and not r["wall_disagreements"])
    floor12 = F(*(int(x) for x in facts["floor12"].split("/")))
    r = side_control("S1c", floor12)
    outside_squares = sorted({x[0] for x in r["wall_outside"]})
    obs = brief(r)
    obs["squares_outside"] = outside_squares
    record("S1c", obs, r["verdict"] == "REFUSE" and outside_squares == stated["S1c"]["squares_outside"]
           and all(x[1] in {"right", "top"} for x in r["wall_outside"]) and not r["wall_disagreements"])
    ceil12 = F(*(int(x) for x in facts["ceil12"].split("/")))
    r = side_control("S1d", ceil12)
    record("S1d", brief(r), r["verdict"] == "ACCEPT"
           and sorted(r["wall_contacts"]) == sorted(stated["S1d"]["wall_contacts"])
           and r["wall_outside"] == [] and not r["wall_disagreements"])

    # S4c, S4p: the least pair
    lp = facts["least_pair"]
    fi, mi = lp["fixed"] - 1, lp["moved"] - 1
    info = geom.closing(base[fi], base[mi])
    same_t = frac_str(info["t_contact"]) == lp["t_contact"] and frac_str(info["t_past"]) == lp["t_past"]
    pair_id = sorted([fi + 1, mi + 1])
    for cid, t in (("S4c", info["t_contact"]), ("S4p", info["t_past"])):
        s = copy.deepcopy(base)
        s[mi] = geom.moved(base[mi], info["w"], t)
        r = decide(w.side, s, pair_list=pairs_of(mi, n), wall_squares=[mi])
        obs = brief(r)
        obs["t_matches_plan"] = same_t
        if cid == "S4c":
            ok = (r["verdict"] == "ACCEPT" and r["touching_pairs"] == [pair_id] and r["overlapping_pairs"] == []
                  and r["wall_outside"] == [] and r["wall_contacts"] == [])
        else:
            ov = r["overlapping_pairs"]
            ok = (r["verdict"] == "REFUSE" and [o["pair"] for o in ov] == [pair_id]
                  and ov[0]["margin"] == frac_str(-D30) and r["touching_pairs"] == [] and r["wall_outside"] == [])
        record(cid, obs, ok and same_t and not r["pair_disagreements"] and not r["wall_disagreements"])

    # S5: every near pair, pair by pair
    near = facts["near_pairs"]
    good = 0
    bad = []
    for entry in near:
        a, b = (k - 1 for k in entry["pair"])
        c = geom.closing(base[a], base[b])
        at = pair_level(base[a], geom.moved(base[b], c["w"], c["t_contact"]))
        past = pair_level(base[a], geom.moved(base[b], c["w"], c["t_past"]))
        ok = (at[0] == "contact" and at[2] == "contact" and at[1] == 0 and at[3] == 0
              and past[0] == "overlap" and past[2] == "overlap" and past[1] == -D30 and past[3] > 0
              and frac_str(c["t_contact"]) == entry["t_contact"])
        good += ok
        if not ok:
            bad.append(entry["pair"])
    record("S5", {"pairs": len(near), "as_stated": good, "not_as_stated": bad},
           good == len(near) == stated["S5"]["pairs"])

    # S6: every square to its nearest wall
    good = 0
    bad = []
    for row in facts["nearest_walls"]:
        i = row["square"] - 1
        wall = row["wall"]
        c = F(*(int(x) for x in row["clearance"].split("/"))) if "/" in row["clearance"] else F(int(row["clearance"]))
        dx, dy = OUTWARD[wall]
        at = wall_level(geom.translate(base[i], c * dx, c * dy), side, wall)
        past = wall_level(geom.translate(base[i], (c + D30) * dx, (c + D30) * dy), side, wall)
        ok = at == ("contact", "contact") and past == ("outside", "outside")
        good += ok
        if not ok:
            bad.append([row["square"], wall, at, past])
    record("S6", {"squares": len(facts["nearest_walls"]), "as_stated": good, "not_as_stated": bad},
           good == n == stated["S6"]["squares"])

    every = all(x["as_stated"] for x in results)
    receipt = {
        "program": "l101_controls.py",
        "programs_sha256": {**program_digests(),
                            "l101_geom.py": sha256_file(Path(__file__).resolve().parent / "l101_geom.py"),
                            "l101_controls.py": sha256_file(Path(__file__).resolve())},
        "plan_sha256": sha256_file(Path(plan_path)),
        "facts_sha256": sha256_file(Path(facts_path)),
        "input_yaml_sha256": sha256_file(Path(ypath)),
        "controls": results,
        "verdict": "EVERY_CONTROL_AS_STATED" if every else "SOME_CONTROL_NOT_AS_STATED",
        "cpu_seconds": round(time.process_time() - start, 1),
    }
    Path(out_path).write_text(json.dumps(receipt, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(receipt["verdict"], receipt["cpu_seconds"], "s")
    return 0 if every else 1


if __name__ == "__main__":
    raise SystemExit(main())
