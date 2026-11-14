"""Lane L153 controls: run every control of the hashed plan and compare its outcome.

Clean-room: written for this review, importing nothing from this repository or the
source, and reusing no code of any earlier review. Written after `controls-plan.json`
was stated and hashed (`frozen/controls-plan-digest.txt`).

Each whole-file control builds the modified certificate as JSON text, reads it back
through the frozen reader and decides it with the frozen checker's `decide`, by both
methods over every square, wall and pair. The reader controls hand modified files (and,
for 297, a modified twin) to the reader. S5 and S6 decide the moved pair or square by
both methods.

Usage: l153_controls.py LABEL CERT.json [TWIN.yaml] PLAN.json FACTS.json CHECK.json OUT.json
"""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l153_clip as B  # noqa: E402
import l153_geom as G  # noqa: E402
import l153_reader as reader  # noqa: E402
import l153_sat as A  # noqa: E402
from gmpy2 import mpq  # noqa: E402
from l153_check import decide, sci, sha256_file  # noqa: E402

PAST = Fraction(1, 10**90)
WALL_ORDER = ("left", "right", "bottom", "top")


def sort_walls(items) -> list[list]:
    return sorted(([k, w] for k, w in items), key=lambda x: (x[0], WALL_ORDER.index(x[1])))


def sort_pairs(items) -> list[list[int]]:
    return sorted([min(p[0], p[1]), max(p[0], p[1])] for p in items)


def json_text(n: int, side: Fraction, squares: list[G.FSquare], fmt: str) -> str:
    rows = [[str(v) for v in sq] for sq in squares]
    return json.dumps(
        {"n": n, "side": str(side), "square_size": "1", "format": fmt, "squares": rows}
    )


def decide_text(text: str) -> dict:
    _, side_pair, squares, _ = reader.parse_json_text(text)
    return decide(side_pair, squares)


def compare(outcome: dict, result: dict, extra: dict) -> tuple[bool, dict]:
    """Each stated field against what came out; and the methods must agree."""
    came: dict = {"verdict": result.get("verdict")}
    ok = True

    def check(key: str, value) -> None:
        nonlocal ok
        came[key] = value
        if key in outcome and outcome[key] != value:
            ok = False

    if result.get("not_unit"):
        check("verdict", result["verdict"])
        check("not_unit", result["not_unit"])
        check("unit_disagree", result["unit_disagree"])
        if result["unit_disagree"]:
            ok = False
        return ok, came
    pairs, walls = result["pairs"], result["walls"]
    check("verdict", result["verdict"])
    overlaps = sort_pairs(pairs["overlaps"])
    check("overlaps", overlaps)
    came["overlap_count"] = len(overlaps)
    if "overlaps_nonempty" in outcome:
        check("overlaps_nonempty", bool(overlaps))
    if "overlap_margin" in outcome or "overlap_area" in outcome:
        if len(pairs["overlaps"]) == 1:
            check("overlap_margin", pairs["overlaps"][0][2])
            check("overlap_area", pairs["overlaps"][0][3])
        else:
            ok = False
    check("contacts", sort_pairs(pairs["contacts"]))
    check("wall_contacts", sort_walls(walls["contacts"]))
    crossing_a = sort_walls([x[0], x[1]] for x in walls["crossing_a"])
    crossing_b = sort_walls(walls["crossing_b"])
    check("crossing", crossing_a)
    if crossing_a != crossing_b:
        ok = False
    came["crossing_b_equals_a"] = crossing_a == crossing_b
    check("not_inside_b", walls["not_inside_b"])
    check("margin_list_sha256", pairs["margin_list_sha256"])
    check("clearance_list_sha256", walls["clearance_list_sha256"])
    if pairs["disagree"] or walls["disagree"] or result["unit_disagree"]:
        ok = False
    came["classes_agree"] = not (pairs["disagree"] or walls["disagree"] or result["unit_disagree"])
    came["least_positive_margin"] = pairs["least_positive"] and pairs["least_positive"]["approx"]
    if overlaps:
        came["least_margin"] = sci(min(Fraction(x[2]) for x in pairs["overlaps"]), 6)
    for key, value in extra.items():
        check(key, value)
    # Keep the receipt small: long lists are stored by count and digest.
    for key in ("contacts", "wall_contacts", "crossing", "overlaps"):
        value = came.get(key)
        if isinstance(value, list) and len(value) > 12:
            came[key] = {
                "count": len(value),
                "sha256": hashlib.sha256(json.dumps(value).encode()).hexdigest(),
            }
    return ok, came


def reader_refuses(json_str: str, yaml_str: str | None, needle: str) -> tuple[bool, dict]:
    with tempfile.TemporaryDirectory() as tmp:
        jp = Path(tmp) / "c.json"
        jp.write_text(json_str)
        yp = None
        if yaml_str is not None:
            yp = Path(tmp) / "c.yaml"
            yp.write_text(yaml_str)
        try:
            reader.read(str(jp), None if yp is None else str(yp))
        except reader.ReadError as error:
            return needle in str(error), {"reader": "refuses", "reason": str(error)[:120]}
    return False, {"reader": "accepts"}


def yaml_drop_last(text: str, n: int) -> str:
    lines = text.split("\n")
    start = lines.index(f"  - id: {n}")
    end = start + 1
    while end < len(lines) and lines[end].startswith("    "):
        end += 1
    return "\n".join(lines[:start] + lines[end:])


def main(argv: list[str]) -> int:
    label = argv[1]
    cert = argv[2]
    twin = argv[3] if len(argv) == 8 else None
    plan_path, facts_path, check_path, out_path = argv[-4:]
    t_start = time.process_time()
    plan = json.loads(Path(plan_path).read_text())
    entry = plan["files"][label]
    if entry["check_receipt_sha256"] != sha256_file(check_path):
        raise SystemExit("check receipt differs from the plan's")
    if entry["plan_facts_sha256"] != sha256_file(facts_path):
        raise SystemExit("plan facts differ from the plan's")
    facts = json.loads(Path(facts_path).read_text())
    data = reader.read(cert, twin)
    n = data["n"]
    fmt = data["format"]
    side = Fraction(*data["side"])
    squares = [G.decode(s) for s in data["squares"]]
    json_raw = Path(cert).read_text()
    yaml_raw = Path(twin).read_text() if twin else None
    results = []
    for control in entry["controls"]:
        cid = control["id"]
        outcome = control["outcome"]
        t0 = time.process_time()
        extra: dict = {}
        ok: bool
        came: dict
        if cid in ("G3", "G4", "G7"):
            tree = json.loads(json_raw)
            y = yaml_raw
            side_text = tree["side"]
            if cid == "G3":
                tree["squares"] = tree["squares"][:-1]
                if y is not None:
                    y = yaml_drop_last(y, n)
            elif cid == "G4":
                p, q = side_text.split("/")
                doubled = f"{2 * int(p)}/{2 * int(q)}"
                tree["side"] = doubled
                if y is not None:
                    old = f"\n  side: {side_text}\n"
                    if y.count(old) != 1:
                        raise SystemExit("twin side line not found once")
                    y = y.replace(old, f"\n  side: {doubled}\n")
            else:
                old = f"\n  side: {side_text}\n"
                p, q = side_text.split("/")
                if y is None or y.count(old) != 1 or not p.endswith("3"):
                    raise SystemExit("G7 cannot be built as stated")
                y = y.replace(old, f"\n  side: {p[:-1]}1/{q}\n")
            ok, came = reader_refuses(json.dumps(tree), y, outcome["reader_refuses"])
        elif cid in ("S5", "S6"):
            ok, came = pair_or_square_level(cid, outcome, facts, squares, side)
        else:
            sq = list(squares)
            s = side
            if cid == "G1":
                sq[n - 1] = sq[0]
            elif cid == "G2":
                cx, cy, c, sn = sq[0]
                sq[0] = (cx + side, cy, c, sn)
            elif cid == "G5":
                cx, cy, c, sn = sq[0]
                sq[0] = (cx, cy, c, sn + Fraction(1, 10**30))
            elif cid == "G6":
                sq = [(cx, cy, c, -sn) for cx, cy, c, sn in sq]
            elif cid == "G8":
                sq = [(cy, cx, sn, c) for cx, cy, c, sn in sq]
            elif cid == "G9":
                sq = [(cx, cy, -sn, c) for cx, cy, c, sn in sq]
            elif cid == "G10":
                sq = [(cx, cy, -c, -sn) for cx, cy, c, sn in sq]
            elif cid == "G11":
                sq = [(side - cy, cx, -sn, c) for cx, cy, c, sn in sq]
            elif cid == "S1a":
                s = side - Fraction(1, side.denominator)
            elif cid == "S1b":
                s = side - PAST
            elif cid == "S1c":
                s = Fraction(side.numerator * 10**12 // side.denominator, 10**12)
            elif cid == "S1d":
                s = Fraction(-((-side.numerator * 10**12) // side.denominator), 10**12)
            elif cid in ("S4c", "S4p"):
                s4 = facts["S4"]
                mover, toward = s4["mover"], s4["toward"]
                t = Fraction(s4["t_contact"] if cid == "S4c" else s4["t_past"])
                sq[mover - 1] = G.moved(sq[mover - 1], sq[toward - 1], t)
                if cid == "S4c":
                    i, j = s4["pair"]
                    m = A.margin(A.prepare(G.encode(sq[i - 1])), A.prepare(G.encode(sq[j - 1])))
                    extra["pair_margin"] = {"pair": [i, j], "value": str(m)}
            else:
                raise SystemExit(f"unknown control {cid}")
            result = decide_text(json_text(n, s, sq, fmt))
            ok, came = compare(outcome, result, extra)
        results.append(
            {
                "id": cid,
                "what": control["what"],
                "as_stated": ok,
                "came_out": came,
                "cpu_seconds": round(time.process_time() - t0, 1),
            }
        )
        print(label, cid, "as stated" if ok else "NOT AS STATED", round(time.process_time() - t0, 1), flush=True)
    every = all(r["as_stated"] for r in results)
    receipt = {
        "program": "l153_controls.py",
        "label": label,
        "plan_sha256": sha256_file(plan_path),
        "verdict": "EVERY_CONTROL_AS_STATED" if every else "SOME_CONTROL_NOT_AS_STATED",
        "as_stated": sum(r["as_stated"] for r in results),
        "controls": results,
        "cpu_seconds_total": round(time.process_time() - t_start, 1),
    }
    Path(out_path).write_text(json.dumps(receipt, indent=1) + "\n")
    print(label, receipt["verdict"], receipt["as_stated"], "of", len(results))
    return 0 if every else 1


def pair_or_square_level(cid: str, outcome: dict, facts: dict, squares, side) -> tuple[bool, dict]:
    ok = True
    if cid == "S5":
        digest = hashlib.sha256()
        at_ok = past_ok = 0
        count = 0
        exact_minus = 0
        for i, j, _, _ in facts["S5"]["list"]:
            count += 1
            info = G.closing(squares[i - 1], squares[j - 1])
            slow = min(info["rates"][b] for b in info["binding"])
            tau = PAST / slow
            want = max(g - tau * info["rates"][lab] for lab, g in info["gaps_at"].items())
            digest.update(f"{i} {j} {info['t']} {info['t'] + tau} {want}\n".encode())
            exact_minus += want == -PAST
            fixed = G.encode(squares[i - 1])
            pa, pb = A.prepare(fixed), B.corners(fixed)
            for t, expect_m, expect_b, kind in (
                (info["t"], Fraction(0), "contact", "at"),
                (info["t"] + tau, want, "overlap", "past"),
            ):
                enc = G.encode(G.moved(squares[j - 1], squares[i - 1], t))
                m = A.margin(pa, A.prepare(enc))
                cls_b, _ = B.pair(pb, B.corners(enc))
                good = m == expect_m and A.classify(m) == expect_b and cls_b == expect_b
                if kind == "at":
                    at_ok += good
                else:
                    past_ok += good
        came = {
            "pairs": count,
            "at_contact_as_stated": at_ok,
            "past_as_stated": past_ok,
            "digest_times_and_past_margins": digest.hexdigest(),
            "past_margin_minus_1e90_exactly": exact_minus,
        }
        ok = (
            count == outcome["pairs"]
            and at_ok == count
            and past_ok == count
            and came["digest_times_and_past_margins"] == outcome["digest_times_and_past_margins"]
            and exact_minus == outcome["past_margin_minus_1e90_exactly"]
        )
        return ok, came
    # S6
    side_q = mpq(side.numerator, side.denominator)
    at_ok = past_ok = 0
    by_wall = dict.fromkeys(WALL_ORDER, 0)
    for k, wall, _ in facts["S6"]["list"]:
        cx, cy, c, sn = squares[k - 1]
        clear = A.clearances(A.prepare(G.encode(squares[k - 1])), side)
        nearest = min((clear[w], idx, w) for idx, w in enumerate(WALL_ORDER))[2]
        if nearest != wall:
            ok = False
        by_wall[wall] += 1
        for extra, expect_a, expect_b, kind in (
            (Fraction(0), Fraction(0), "contact", "at"),
            (PAST, -PAST, "crossing", "past"),
        ):
            step = clear[wall] + extra
            if wall == "left":
                moved = (cx - step, cy, c, sn)
            elif wall == "right":
                moved = (cx + step, cy, c, sn)
            elif wall == "bottom":
                moved = (cx, cy - step, c, sn)
            else:
                moved = (cx, cy + step, c, sn)
            enc = G.encode(moved)
            value = A.clearances(A.prepare(enc), side)[wall]
            cls_b, _ = B.wall(B.corners(enc), wall, side_q)
            good = value == expect_a and cls_b == expect_b
            if kind == "at":
                at_ok += good
            else:
                past_ok += good
    n = len(facts["S6"]["list"])
    came = {"squares": n, "at_as_stated": at_ok, "past_as_stated": past_ok, "by_wall": by_wall}
    ok = ok and n == outcome["squares"] and at_ok == n and past_ok == n and by_wall == outcome["by_wall"]
    return ok, came


if __name__ == "__main__":
    sys.exit(main(sys.argv))
