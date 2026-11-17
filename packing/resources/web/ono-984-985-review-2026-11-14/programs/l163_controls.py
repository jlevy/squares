"""Lane L163 controls: run every control of the stated plan by both methods or the reader.

Usage: l163_controls.py LABEL MAIN.json TWIN.cert PLAN.json FACTS.json CHECK.json OUT.json

Every whole-file control writes the modified certificate as JSON text and reads it back
through the reader before both methods decide every square, wall and pair; the classes
of the two methods must agree everywhere. S5 is decided pair by pair and S6 square by
square, by both methods.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fractions import Fraction as F  # noqa: E402
from math import gcd  # noqa: E402

import l163_clip as clip  # noqa: E402
import l163_geom as geom  # noqa: E402
import l163_sat as sat  # noqa: E402
from gmpy2 import mpq  # noqa: E402
from l163_decide import WALLS, Decision, decide  # noqa: E402
from l163_reader import Certificate, Refused, read_cert, read_cert_text, read_json, read_json_text, same_tree  # noqa: E402

NEAR = F(1, 10**6)


def fr(x: F) -> str:
    return f"{x.numerator}/{x.denominator}"


def to_json_text(c: Certificate) -> str:
    rows = [
        {"cx": f"{r[0]}/{r[1]}", "cy": f"{r[2]}/{r[3]}", "t": f"{r[4]}/{r[5]}"} for r in c.squares
    ]
    return json.dumps({"n": c.n, "side": f"{c.side[0]}/{c.side[1]}", "squares": rows})


def make(n: int, side: F, rows: list[geom.Row]) -> Certificate:
    """A certificate written as text and read back through the reader."""
    text = to_json_text(Certificate(n, (side.numerator, side.denominator), tuple(rows)))
    return read_json_text(text)


def digest(lines: list[str]) -> str:
    h = hashlib.sha256()
    for s in lines:
        h.update((s + "\n").encode())
    return h.hexdigest()


def judge(d: Decision, expect: dict) -> tuple[dict, bool]:  # pyright: ignore[reportMissingTypeArgument, reportUnknownParameterType]
    over = [list(k) for k in d.overlapping()]
    touch = [list(k) for k in d.touching()]
    came: dict[str, object] = {
        "verdict": "ACCEPT" if d.accepted() else "REFUSE",
        "pair_classes_agree": d.pair_classes_agree(),
        "wall_classes_agree": d.wall_classes_agree(),
        "containment_agrees": d.containment_agrees(),
        "overlapping_count": len(over),
        "touching": touch[:10],
        "crossings": sorted([i, w] for i, w in d.crossings()),
        "contacts": sorted([i, w] for i, w in d.contacts()),
    }
    ok = bool(came["pair_classes_agree"] and came["wall_classes_agree"] and came["containment_agrees"])
    ok = ok and all(d.unit_a) and all(d.unit_b) and all(d.ccw_b)
    if "verdict" in expect:
        ok = ok and came["verdict"] == expect["verdict"]
    if "overlapping" in expect:
        came["overlapping"] = over[:10]
        ok = ok and over == expect["overlapping"]
    if "overlapping_count" in expect:
        ok = ok and len(over) == expect["overlapping_count"]
    if "overlapping_sha256" in expect:
        came["overlapping_sha256"] = digest([f"{i} {j}" for i, j in over])
        ok = ok and came["overlapping_sha256"] == expect["overlapping_sha256"]
        came["least_margin"] = geom.sci(min(d.margins.values()))
    if "touching" in expect:
        ok = ok and touch == expect["touching"]
    if "crossings" in expect:
        ok = ok and came["crossings"] == expect["crossings"]
        for i, _ in d.crossings():
            ok = ok and d.inside_area_b[i - 1] != 1
    if "contacts" in expect:
        ok = ok and came["contacts"] == expect["contacts"]
    if "margin_of" in expect:
        pair = tuple(expect["margin_of"]["pair"])
        m = d.margins[pair]  # pyright: ignore[reportArgumentType]
        came["margin_of"] = {"pair": list(pair), "value": fr(m), "area_b": str(d.area_b[pair])}  # pyright: ignore[reportArgumentType]
        ok = ok and fr(m) == expect["margin_of"]["value"]
        if "area_b" in expect["margin_of"]:
            ok = ok and str(d.area_b[pair]) == expect["margin_of"]["area_b"]  # pyright: ignore[reportArgumentType]
    if "margin_list_sha256" in expect:
        came["margin_list_sha256"] = d.margin_digest()
        ok = ok and came["margin_list_sha256"] == expect["margin_list_sha256"]
    if "clearance_multiset_sha256" in expect:
        came["clearance_multiset_sha256"] = d.clearance_multiset_digest()
        ok = ok and came["clearance_multiset_sha256"] == expect["clearance_multiset_sha256"]
    if "clearances_of" in expect:
        k = expect["clearances_of"]["square"]
        vals = [fr(c) for c in d.clear[k - 1]]
        came["clearances_of_sci"] = [geom.sci(c) for c in d.clear[k - 1]]
        ok = ok and vals == expect["clearances_of"]["values"]
    return came, ok


def main() -> None:
    label, main_json, twin_cert, plan_path, facts_path, check_path, out = sys.argv[1:8]
    t0 = time.process_time()
    cert = read_json(main_json)
    with open(plan_path, encoding="utf-8") as fh:
        plan = json.load(fh)
    with open(facts_path, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(check_path, encoding="utf-8") as fh:
        check = json.load(fh)
    controls = plan["counts"][label]
    n = cert.n
    side = F(*cert.side)
    rows = list(cert.squares)
    results: list[dict[str, object]] = []
    base = decide(cert)
    for ctl in controls:
        cid, expect = ctl["id"], ctl["expect"]
        came: dict[str, object] = {}
        ok = False
        if cid == "G1":
            d = decide(make(n, side, rows[:-1] + [rows[0]]))
            came, ok = judge(d, expect)
        elif cid == "G2":
            d = decide(make(n, side, [geom.translate(rows[0], side, F(0))] + rows[1:]))
            came, ok = judge(d, expect)
        elif cid in ("G3", "G4"):
            if cid == "G3":
                text = to_json_text(Certificate(n, cert.side, tuple(rows[:-1])))
            else:
                p, q = cert.side
                text = to_json_text(cert).replace(f'"side": "{p}/{q}"', f'"side": "{2 * p}/{2 * q}"')
            try:
                read_json_text(text)
                came = {"reader": "accepted"}
            except Refused as exc:
                came = {"reader": "refused", "reason": exc.reason}
                ok = expect["reader_refuses_with"] in exc.reason
        elif cid in ("G5a", "G5b"):
            k = int(ctl["what"].split()[1]) - 1
            cx, cy, t = geom.parts(rows[k])
            sign = 1 if cid == "G5a" else -1
            new = list(rows)
            new[k] = geom.row(cx, cy, t + sign * F(1, 10**30))
            d = decide(make(n, side, new))
            came, ok = judge(d, expect)
        elif cid == "G6":
            new = [geom.row(*geom.parts(r)[:2], -geom.parts(r)[2]) for r in rows]
            d = decide(make(n, side, new))
            came, ok = judge(d, expect)
        elif cid == "G7":
            with open(twin_cert, encoding="utf-8") as fh:
                lines = fh.read().split("\n")
            h = next(i for i, s in enumerate(lines) if not s.startswith("#"))
            num, den = lines[h].split(" ")[1].split("/")
            last = int(num[-1])
            for step in range(1, 10):
                alt = num[:-1] + str((last + step) % 10)
                if gcd(int(alt), int(den)) == 1:
                    break
            lines[h] = f"{lines[h].split(' ')[0]} {alt}/{den}"  # pyright: ignore[reportPossiblyUnboundVariable]
            twin = read_cert_text("\n".join(lines))
            differs = not same_tree(cert, twin)
            came = {"twin_differs": differs, "twin_unaltered_equal": same_tree(cert, read_cert(twin_cert))}
            ok = differs and came["twin_unaltered_equal"] is True
        elif cid == "G8":
            new = [geom.row(geom.parts(r)[1], geom.parts(r)[0], -geom.parts(r)[2]) for r in rows]
            d = decide(make(n, side, new))
            came, ok = judge(d, expect)
        elif cid in ("G9", "G10"):
            new = []
            for r in rows:
                cx, cy, t = geom.parts(r)
                new.append(geom.row(cx, cy, (t + 1) / (1 - t) if cid == "G9" else (t - 1) / (1 + t)))
            d = decide(make(n, side, new))
            came, ok = judge(d, expect)
        elif cid == "G11":
            new = [geom.row(side - geom.parts(r)[1], geom.parts(r)[0], geom.parts(r)[2]) for r in rows]
            d = decide(make(n, side, new))
            came, ok = judge(d, expect)
        elif cid in ("S1a", "S1b", "S1c", "S1d"):
            new_side = {
                "S1a": side - F(1, side.denominator),
                "S1b": side - F(1, 10**30),
                "S1c": geom.floor_value(side, 12),
                "S1d": geom.ceil_value(side, 12),
            }[cid]
            d = decide(make(n, new_side, rows))
            came, ok = judge(d, expect)
            came["side"] = geom.floor_places(new_side, 15)
        elif cid in ("S4c", "S4p"):
            mv = expect["move"]
            i, j = mv["toward"] - 1, mv["moving"] - 1
            moved, _ = geom.close_pair(rows[i], rows[j], F(mv["delta"]))
            new = list(rows)
            new[j] = moved
            d = decide(make(n, side, new))
            came, ok = judge(d, expect)
        elif cid == "S5":
            near = sorted(k for k, m in base.margins.items() if 0 < m < NEAR)
            lines5: list[str] = []
            good = 0
            for i1, j1 in near:
                ri, rj = rows[i1 - 1], rows[j1 - 1]
                tc = geom.closing(ri, rj, F(0))[0]
                tp = geom.closing(ri, rj, F(1, 10**30))[0]
                lines5.append(f"{i1} {j1} {fr(tc)} {fr(tp)}")
                okp = True
                for delta, want in ((F(0), "touch"), (F(1, 10**30), "overlap")):
                    moved, _ = geom.close_pair(ri, rj, delta)
                    m = sat.margin(sat.prepare(ri), sat.prepare(moved))
                    cls, _ = clip.pair_class(clip.corners(ri), clip.corners(moved))
                    okp = okp and m == -delta and sat.classify(m) == want and cls == want
                good += okp
            came = {"pairs": len(near), "as_stated": good, "closing_times_sha256": digest(lines5)}
            ok = len(near) == expect["pairs"] and good == len(near) and came["closing_times_sha256"] == expect["closing_times_sha256"]
        elif cid == "S6":
            listed: list[str] = []
            good = 0
            for k, r in enumerate(rows):
                cl = base.clear[k]
                w = min(range(4), key=lambda x: (cl[x], x))
                listed.append(f"{k + 1} {WALLS[w]} {fr(cl[w])}")
                oks = True
                for delta, want in ((F(0), "contact"), (F(1, 10**30), "crossing")):
                    moved = geom.to_wall(r, w, side, delta)
                    ca = sat.clearances(sat.prepare(moved), cert.side)[w]
                    cls, inside = clip.wall_classes(clip.corners(moved), mpq(cert.side[0], cert.side[1]))
                    oks = oks and ca == -delta and sat.wall_class(ca) == want and cls[w] == want
                    oks = oks and ((inside == 1) == (delta == 0))
                good += oks
            came = {"squares": len(rows), "as_stated": good, "nearest_list_sha256": digest(listed)}
            ok = good == len(rows) == expect["squares"] and came["nearest_list_sha256"] == expect["nearest_list_sha256"]
        results.append({"id": cid, "stated": ctl["stated"], "came_out": came, "as_stated": bool(ok)})
        print(label, cid, "as stated" if ok else "NOT AS STATED", flush=True)
    every = all(r["as_stated"] for r in results)
    rec = {
        "label": label,
        "lane": "L163",
        "program": "l163_controls.py",
        "check_receipt_least_margin": check["main"]["least_margin_sci"],
        "facts_n": facts["n"],
        "controls": results,
        "summary": "EVERY_CONTROL_AS_STATED" if every else "SOME_CONTROL_NOT_AS_STATED",
        "as_stated": sum(1 for r in results if r["as_stated"]),
        "of": len(results),
        "cpu_seconds": round(time.process_time() - t0, 1),
    }
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1)
    print(label, rec["summary"], rec["as_stated"], "of", rec["of"], "cpu", rec["cpu_seconds"])


if __name__ == "__main__":
    main()
