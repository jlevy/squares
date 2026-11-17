"""Lane L169 controls: run the stated controls and compare each with its stated outcome.

Usage: l169_controls.py CERT PLAN_JSON PLAN_FACTS_JSON CHECK_JSON OUT_JSON

Every whole-file control is written as certificate text, read back through the reader,
and decided by both methods over every square, wall and pair (l169_decide.py). G3, G4 and
G7b stop at the reader. S5 decides each closed pair by both methods (pair-level), and S6
each moved square against its wall by both methods (square-level).
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves it off

import l169_clip as clipm
import l169_decide as dec
import l169_geom as geom
import l169_reader as rd
import l169_sat as sat

WALLS = ("left", "right", "bottom", "top")


def fs(f: F) -> str:
    return f"{f.numerator}/{f.denominator}"


def norm(x):
    return json.loads(json.dumps(x))


def to_reading(n: int, side: F, rows: list[tuple[F, F, F]]) -> dict:
    return {"n": n, "side": (side.numerator, side.denominator),
            "squares": [tuple((v.numerator, v.denominator) for v in r) for r in rows]}


def file_control(op: dict, raw: bytes, base: dict) -> tuple[bytes, dict | None]:
    """The modified text for a whole-file or reader control."""
    n = base["n"]
    S = F(*base["side"])
    rows = [tuple(F(*v) for v in sq) for sq in base["squares"]]
    name = op["name"]
    if name == "delete_last_row":
        lines = raw.split(b"\r\n")
        return b"\r\n".join(lines[:-2]) + b"\r\n", None
    if name == "side_doubled_text":
        p, q = base["side"]
        head, rest = raw.split(b"\r\n", 1)
        return f"{n} {2 * p}/{2 * q}".encode() + b"\r\n" + rest, None
    if name == "header_count":
        head, rest = raw.split(b"\r\n", 1)
        side_tok = head.split(b" ")[1]
        return f"{op['value']} ".encode() + side_tok + b"\r\n" + rest, None
    if name == "lf_text":
        return raw.replace(b"\r\n", b"\n"), None
    side = S
    if name == "copy_square":
        rows[op["to"] - 1] = rows[op["from"] - 1]
    elif name == "translate_square":
        x, y, t = rows[op["square"] - 1]
        rows[op["square"] - 1] = (x + F(op["dx"]), y + F(op["dy"]), t)
    elif name == "wall_then_turn":
        k = op["square"] - 1
        x, y, t = rows[k]
        q = geom.moved_to_wall((x, y, F(0), F(0)), op["wall"], F(op["by"]))
        rows[k] = (q[0], q[1], t + F(op["dt"]))
    elif name == "negate_t":
        rows = [(x, y, -t) for x, y, t in rows]
    elif name == "transpose":
        rows = [(y, x, -t) for x, y, t in rows]
    elif name == "rebase_plus":
        rows = [(x, y, (t + 1) / (1 - t)) for x, y, t in rows]
    elif name == "rebase_minus":
        rows = [(x, y, (t - 1) / (1 + t)) for x, y, t in rows]
    elif name == "quarter_turn":
        rows = [(S - y, x, t) for x, y, t in rows]
    elif name == "side_minus":
        side = S - F(op["by"]) - F(op.get("and", "0"))
    elif name == "fit_box":
        dx, dy = F(op["dx"]), F(op["dy"])
        rows = [(x + dx, y + dy, t) for x, y, t in rows]
        side = F(op["side"]) - F(op.get("and", "0"))
    elif name == "close_pair":
        m, tw = op["mover"] - 1, op["toward"] - 1
        tau = F(op["tau"])
        xm, ym, tm = rows[m]
        xt, yt, _ = rows[tw]
        rows[m] = (xm - tau * (xm - xt), ym - tau * (ym - yt), tm)
    else:
        raise ValueError(f"unknown op {name}")
    reading = to_reading(n, side, rows)
    return rd.write_text(reading), reading


def compare(expect: dict, res: dict) -> list[str]:
    bad = []
    for k, v in expect.items():
        if k == "pair":
            i, j = v["pair"]
            row = next(r for r in res["_pairs"] if r[0] == i and r[1] == j)
            got = {"A_margin": fs(row[2]), "B_class": row[4], "B_area": fs(F(int(row[5].numerator), int(row[5].denominator)))}
            for kk, vv in v.items():
                if kk != "pair" and got[kk] != vv:
                    bad.append(f"pair {i},{j} {kk}: {got[kk]} != {vv}")
        elif k == "clearance":
            row = next(r for r in res["_walls"] if r[0] == v["square"] and r[1] == v["wall"])
            if fs(row[2]) != v["value"]:
                bad.append(f"clearance {v['square']} {v['wall']}: {fs(row[2])} != {v['value']}")
        elif norm(res[k]) != norm(v):
            got = norm(res[k])
            bad.append(f"{k}: got {got if len(str(got)) < 300 else str(got)[:300]}")
    return bad


def run_s5(base: dict, pexp: dict) -> dict:
    rows = [tuple(F(*v) for v in sq) for sq in base["squares"]]
    qs = [geom.sq_of(*r) for r in rows]
    n = len(qs)
    eps = F(pexp["past"]["A_margin"])
    times = []
    bad = []
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            qi, qj = qs[i], qs[j]
            t0 = geom.close_time(qi, qj, F(0))
            t1 = geom.close_time(qi, qj, eps)
            times.append(f"{i + 1} {j + 1} {fs(t0)} {fs(t1)}\n")
            ri = (rows[i][0], rows[i][1], rows[i][2])
            for tag, tau in (("at_contact", t0), ("past", t1)):
                mj = geom.moved_toward(qi, qj, tau)
                pi = tuple((v.numerator, v.denominator) for v in ri)
                pj = tuple((v.numerator, v.denominator) for v in (mj[0], mj[1], rows[j][2]))
                m = sat.pair_margin(sat.Square(*pi), sat.Square(*pj))
                b1, b2 = clipm.corners(*pi), clipm.corners(*pj)
                kb, _ = clipm.pair_class(b1, b2)
                kb2, _ = clipm.pair_class(b2, b1)
                want = pexp[tag]
                if fs(m) != want["A_margin"] or kb != want["B_class"] or kb2 != want["B_class"]:
                    bad.append(f"pair {i + 1},{j + 1} {tag}: A {fs(m)} B {kb}/{kb2}")
            count += 1
    digest = hashlib.sha256("".join(times).encode()).hexdigest()
    if digest != pexp["closing_times_sha256"]:
        bad.append("closing times digest differs from the plan's")
    if count != pexp["pairs"]:
        bad.append(f"{count} pairs, not {pexp['pairs']}")
    return {"pairs_done": count, "as_stated_pairs": count - len({b.split(' ')[1] for b in bad if b.startswith('pair')}),
            "closing_times_sha256": digest, "failures": bad[:20]}


def run_s6(base: dict, sexp: dict) -> dict:
    side = base["side"]
    S = F(*side)
    rows = [tuple(F(*v) for v in sq) for sq in base["squares"]]
    eps = -F(sexp["past"]["A_clearance"])
    near = []
    bad = []
    for k, r in enumerate(rows):
        q = geom.sq_of(*r)
        c = geom.clearances(q, S)
        w = min(WALLS, key=lambda x: (c[x], WALLS.index(x)))
        near.append(f"{k + 1} {w} {fs(c[w])}\n")
        for tag, by in (("at_contact", c[w]), ("past", c[w] + eps)):
            m = geom.moved_to_wall(q, w, by)
            row = tuple((v.numerator, v.denominator) for v in (m[0], m[1], r[2]))
            ca = sat.clearances(sat.Square(*row), side)[w]
            corners = clipm.corners(*row)
            kb, _ = clipm.wall_class(corners, w, side)
            ain = clipm.area_in_box(corners, side)
            want = sexp[tag]
            ok = fs(ca) == want["A_clearance"] and kb == want["B_class"]
            ok = ok and ((ain == 1) if tag == "at_contact" else (ain < 1))
            if not ok:
                bad.append(f"square {k + 1} {w} {tag}: A {fs(ca)} B {kb} area {ain}")
    digest = hashlib.sha256("".join(near).encode()).hexdigest()
    if digest != sexp["list_sha256"]:
        bad.append("nearest-wall list digest differs from the plan's")
    return {"squares_done": len(rows), "list_sha256": digest, "failures": bad[:20],
            "as_stated_squares": len(rows) - len({b.split(' ')[1] for b in bad if b.startswith('square')})}


def main(argv: list[str]) -> int:
    t0 = time.process_time()
    cert, plan_path, _facts_path, check_path, out_path = argv[1:6]
    raw = open(cert, "rb").read()
    plan = json.load(open(plan_path))
    check = json.load(open(check_path))
    if hashlib.sha256(raw).hexdigest() != plan["certificate_sha256"] or check["sha256"] != plan["certificate_sha256"]:
        raise SystemExit("certificate digest differs from the plan's")
    base = rd.read_text(raw)
    results = []
    for c in plan["controls"]:
        exp = c["expect"]
        entry = {"id": c["id"], "what": c["what"]}
        if c["kind"] == "reader":
            text, _ = file_control(c["op"], raw, base)
            try:
                rd.read_text(text)
                entry["outcome"] = "reader accepted"
                entry["as_stated"] = False
            except rd.ReadError as e:
                entry["outcome"] = f"reader refused: {e}"
                entry["as_stated"] = exp["reader_refuses"] in str(e)
        elif c["kind"] == "file":
            text, _ = file_control(c["op"], raw, base)
            back = rd.read_text(text)
            res = dec.decide(back)
            bad = compare(exp, res)
            pub = dec.public(res)
            entry["outcome"] = {k: pub[k] for k in ("verdict", "overlapping_pairs", "touching_pairs", "wall_contacts",
                                                    "wall_crossings", "not_inside_by_B_area", "least_margin",
                                                    "margin_list_sha256", "clearance_list_sha256")}
            entry["mismatches"] = bad
            entry["as_stated"] = not bad
        elif c["kind"] == "pair-level":
            r = run_s5(base, exp)
            entry["outcome"] = r
            entry["as_stated"] = not r["failures"]
        else:
            r = run_s6(base, exp)
            entry["outcome"] = r
            entry["as_stated"] = not r["failures"]
        results.append(entry)
        print(f"{c['id']}: {'as stated' if entry['as_stated'] else 'NOT AS STATED'}")
        if not entry["as_stated"]:
            print("   ", entry.get("mismatches") or entry["outcome"])
    every = all(e["as_stated"] for e in results)
    out = {
        "program": "l169_controls.py",
        "plan_sha256": hashlib.sha256(open(plan_path, "rb").read()).hexdigest(),
        "status": "EVERY_CONTROL_AS_STATED" if every else "SOME_CONTROL_NOT_AS_STATED",
        "as_stated": sum(1 for e in results if e["as_stated"]),
        "controls": len(results),
        "results": results,
        "cpu_seconds": round(time.process_time() - t0, 2),
    }
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(f"{out['status']}: {out['as_stated']} of {out['controls']}; cpu {out['cpu_seconds']}s")
    return 0 if every else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
