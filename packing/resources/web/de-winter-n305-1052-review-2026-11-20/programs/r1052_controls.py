"""Lane r1052's controls: each control of programs/controls-plan.json, evaluated as stated.

Usage: r1052_controls.py J_FILE C_FILE PLAN CLAIM OUT_JSON

The facts the rules are stated over are method A's margins and clearances of form J,
computed here. A whole-file control writes the modified packing with the writer, reads
it back through the reader and decides it by both methods with every pair and wall; a
control passes when every clause of its rule holds and the two methods agree everywhere.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction as F
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import r1052_check as check  # noqa: E402
import r1052_clip as clip  # noqa: E402
import r1052_decide as decide_mod  # noqa: E402
import r1052_geom as geom  # noqa: E402
import r1052_poses as poses_a  # noqa: E402
import r1052_reader as reader  # noqa: E402
import r1052_writer as writer  # noqa: E402

EPS = F(1, 10**30)
WALLS = decide_mod.WALLS
Pose = tuple[F, F, F, F]


def dec_j(side: F, poses: list[Pose]) -> tuple[dict[str, Any], dict[str, Any]]:
    got = reader.read_form_j(writer.form_j(side, poses))
    return got, decide_mod.decide(got["side"], poses=got["poses"], distance=False)


def dec_c(side: F, corners: list[Any], ids: list[str]) -> tuple[dict[str, Any], dict[str, Any]]:
    got = reader.read_form_c(writer.form_c(side, corners, ids=ids))
    return got, decide_mod.decide(got["side"], corners=got["corners"], distance=False)


def margins_of(res: dict[str, Any]) -> dict[tuple[int, int], F]:
    return {k: v[0] for k, v in res["pairs"].items()}


def clears_of(res: dict[str, Any]) -> list[tuple[F, ...] | None]:
    return [None if row is None else tuple(row["clearances"]) for row in res["walls"]]


def overlapping(res: dict[str, Any]) -> set[tuple[int, int]]:
    return {k for k, v in res["pairs"].items() if v[1] == "overlap"}


def crossings(res: dict[str, Any]) -> set[tuple[int, str]]:
    out = set()
    for k, row in enumerate(res["walls"]):
        if row is None:
            continue
        for w, name in enumerate(WALLS):
            if row["clearances"][w] < 0:
                out.add((k, name))
    return out


def refuses(fn: Any, data: bytes, needle: str) -> tuple[bool, str]:
    try:
        fn(data)
    except reader.Refused as exc:
        return needle in str(exc), f"refused: {exc}"
    return False, "read"


class Run:
    def __init__(self, plan: dict[str, Any]) -> None:
        self.stated = {c["id"]: c["stated"] for c in plan["controls"]}
        self.rows: list[dict[str, Any]] = []
        self.decisions = 0

    def record(self, cid: str, good: bool, detail: str) -> None:
        row = {"id": cid, "stated": self.stated.get(cid, ""), "outcome": "as stated" if good else "NOT as stated",
               "detail": detail}
        self.rows.append(row)
        print(f"{cid}: {row['outcome']} ({detail[:160]})", flush=True)


def main(argv: list[str]) -> int:
    j_path, c_path, plan_path, claim_text, out_path = argv[1:6]
    t0 = time.process_time()
    plan = json.loads(Path(plan_path).read_text())
    run = Run(plan)
    jj = reader.read_form_j(Path(j_path).read_bytes())
    cc = reader.read_form_c(Path(c_path).read_bytes())
    side: F = jj["side"]
    poses: list[Pose] = jj["poses"]
    corners = cc["corners"]
    ids = cc["ids"]
    n = len(poses)
    claim = F(claim_text)
    facts = poses_a.run(side, poses=poses)
    m: dict[tuple[int, int], F] = facts["margins"]
    cl: list[tuple[F, F, F, F]] = facts["walls"]
    base_j = decide_mod.decide(side, poses=poses, distance=False)
    base_c = decide_mod.decide(cc["side"], corners=corners, distance=False)
    run.decisions += 2
    base_ok = base_j["verdict"] == "ACCEPT"

    # C0: the third formulation against method A, everywhere.
    bad_m = sum(1 for (i, j), v in m.items() if geom.margin(poses[i], poses[j]) != v)
    bad_c = sum(1 for k in range(n) if geom.clearances(side, poses[k]) != cl[k])
    run.record("C0", bad_m == 0 and bad_c == 0 and len(m) == n * (n - 1) // 2,
               f"{bad_m} margin and {bad_c} clearance mismatches over {len(m)} pairs and {n} squares")

    # ------------------------------------------------------------------ reader, form J
    base_text = writer.form_j(side, poses)
    back = reader.read_form_j(base_text)
    run.record("R0J", back["n"] == n and back["side"] == side and back["poses"] == poses and not back["noncanonical"],
               f"{back['n']} rows; noncanonical {len(back['noncanonical'])}")
    obj = json.loads(base_text)

    def jtext(o: dict[str, Any]) -> bytes:
        return (json.dumps(o, indent=1) + "\n").encode()

    short = writer.form_j(side, poses[:-1]).replace(f'"n": {n - 1},'.encode(), f'"n": {n},'.encode(), 1)
    good, d = refuses(reader.read_form_j, short, f"{n} and {n - 1}")
    run.record("R1J", good, d)
    p, q = side.numerator, side.denominator
    t2 = base_text.replace(f'"side": "{side}"'.encode(), f'"side": "{2 * p}/{2 * q}"'.encode(), 1)
    r2 = reader.read_form_j(t2)
    run.record("R2J", r2["side"] == side and r2["noncanonical"] == ["side"], f"noncanonical {r2['noncanonical'][:3]}")
    t3 = base_text.replace(f'"side": "{side}",'.encode(), f'"side": "{side}",\n "side": "{side}",'.encode(), 1)
    good, d = refuses(reader.read_form_j, t3, "twice")
    run.record("R3J", good and t3 != base_text, d)
    t4 = base_text.replace(f'"side": "{side}"'.encode(), f'"side": {check.decimal(side, 40)}'.encode(), 1)
    good, d = refuses(reader.read_form_j, t4, "fraction or exponent")
    run.record("R4J", good, d)
    o5 = dict(obj)
    o5 = {"n": obj["n"], "origin": "lower-left", **{k: v for k, v in obj.items() if k != "n"}}
    good, d = refuses(reader.read_form_j, jtext(o5), "unexpected")
    run.record("R5J", good, d)
    o6 = json.loads(base_text)
    o6["squares"][0].append("0")
    good, d = refuses(reader.read_form_j, jtext(o6), "four scalars")
    run.record("R6J", good, d)
    o7 = json.loads(base_text)
    o7["squares"][0][0] = "+" + o7["squares"][0][0]
    good, d = refuses(reader.read_form_j, jtext(o7), "not an exact scalar")
    run.record("R7J", good, d)
    o8 = json.loads(base_text)
    o8["side"] = f"{p}/0"
    good, d = refuses(reader.read_form_j, jtext(o8), "not an exact scalar")
    run.record("R8J", good, d)
    o9 = json.loads(base_text)
    o9["square_size"] = "2"
    good, d = refuses(reader.read_form_j, jtext(o9), "square_size")
    run.record("R9J", good, d)

    # ------------------------------------------------------------------ reader, form C
    ctext = writer.form_c(cc["side"], corners, ids=ids).decode()
    backc = reader.read_form_c(ctext.encode())
    run.record("R0C", backc["n"] == n and backc["side"] == cc["side"] and backc["ids"] == ids
               and backc["corners"] == corners and not backc["noncanonical"],
               f"{backc['n']} squares; noncanonical {len(backc['noncanonical'])}")
    last = ctext.rfind("  - id: ")
    good, d = refuses(reader.read_form_c, ctext[:last].encode(), f"{n} and {n - 1}")
    run.record("R1C", good, d)
    sline = f"  side: {cc['side']}\n"
    cp, cq = cc["side"].numerator, cc["side"].denominator
    r2c = reader.read_form_c(ctext.replace(sline, f"  side: {2 * cp}/{2 * cq}\n", 1).encode())
    run.record("R2C", r2c["side"] == cc["side"] and r2c["noncanonical"] == ["witness.side"],
               f"noncanonical {r2c['noncanonical'][:3]}")
    t = ctext.replace(f"  - id: {ids[1]}\n", f"  - id: {ids[0]}\n", 1)
    good, d = refuses(reader.read_form_c, t.encode(), "twice")
    run.record("R3C", good, d)
    t = ctext.replace(sline, f"  side: {check.decimal(cc['side'], 40)}\n", 1)
    good, d = refuses(reader.read_form_c, t.encode(), "float")
    run.record("R4C", good, d)
    r5 = reader.read_form_c(ctext.replace(sline, f"  side: '{claim_text}'\n", 1).encode())
    run.record("R5C", r5["side"] == claim and r5["scalar_forms"].get("decimal") == 1,
               f"side {r5['side']}, forms {r5['scalar_forms']}")
    first_x = writer.text(corners[0][0][0])
    t = ctext.replace("    corners:\n", f"    corners:\n    - - {first_x}\n      - 0\n", 1)
    good, d = refuses(reader.read_form_c, t.encode(), "5 items")
    run.record("R6C", good, d)
    t = ctext.replace(sline, sline + sline, 1)
    good, d = refuses(reader.read_form_c, t.encode(), "twice")
    run.record("R7C", good, d)
    blocks = ctext.split("  - id: ")
    second = blocks[2]
    head, _, rest = second.partition("    corners:\n")
    tail_lines = rest.split("\n")
    second_new = head + "    corners: *c1\n" + "\n".join(tail_lines[8:])
    first_block = blocks[1].replace("    corners:\n", "    corners: &c1\n", 1)
    t = "  - id: ".join([blocks[0], first_block, second_new, *blocks[3:]])
    good, d = refuses(reader.read_form_c, t.encode(), "anchor")
    run.record("R8C", good, d)
    t = ctext.replace("representation: corners", "representation: center-angle", 1)
    good, d = refuses(reader.read_form_c, t.encode(), "representation")
    run.record("R9C", good, d)
    t = ctext.replace(f"    - - {first_x}\n", f"    - - +{first_x}\n", 1)
    good, d = refuses(reader.read_form_c, t.encode(), "not an exact scalar")
    run.record("R10C", good and t != ctext, d)
    t = ctext.replace("square_size: '1'", "square_size: '2'", 1)
    good, d = refuses(reader.read_form_c, t.encode(), "square_size")
    run.record("R11C", good, d)
    t = ctext.replace("kind: rational", "kind: decimal", 1)
    good, d = refuses(reader.read_form_c, t.encode(), "kind")
    run.record("R12C", good, d)
    r13 = reader.read_form_c(writer.form_c(cc["side"], corners, ids=ids, origin="container-center"))
    run.record("R13C", r13["corners"] == corners and r13["origin"] == "container-center", "corners equal")
    t = ctext.replace(sline, f"  side: {cp}/0\n", 1)
    good, d = refuses(reader.read_form_c, t.encode(), "not an exact scalar")
    run.record("R14C", good, d)
    t = ctext.replace(sline, f"  side: !!str {cc['side']}\n", 1)
    good, d = refuses(reader.read_form_c, t.encode(), "explicit tag")
    run.record("R15C", good, d)

    # ------------------------------------------------------------------ twin and form controls
    moved = [list(sq) for sq in corners]
    moved[0][0] = (moved[0][0][0] + EPS, moved[0][0][1])
    got, res = dec_c(cc["side"], moved, ids)
    run.decisions += 1
    tw = check.twin(poses, got["corners"])
    good = (tw == [1] and res["verdict"] == "REFUSE" and res["unit_a"] == [False] + [True] * (n - 1)
            and res["unit_b"] == [False] + [True] * (n - 1) and not res["disagreements"])
    run.record("T1", good, f"twin fails at {tw}; {res['problems'][:2]}")
    p2 = list(poses)
    p2[0] = (p2[0][0], p2[0][1], p2[0][2] + EPS, p2[0][3])
    got, res = dec_j(side, p2)
    run.decisions += 1
    tw = check.twin(got["poses"], corners)
    good = (tw == [1] and res["verdict"] == "REFUSE" and res["unit_a"] == [False] + [True] * (n - 1)
            and res["unit_b"] == [False] + [True] * (n - 1) and not res["disagreements"])
    run.record("T2", good, f"twin fails at {tw}; {res['problems'][:2]}")
    sw = [corners[1], corners[0], *corners[2:]]
    swid = [ids[1], ids[0], *ids[2:]]
    got, res = dec_c(cc["side"], sw, swid)
    run.decisions += 1
    tw = check.twin(poses, got["corners"])
    run.record("T3", tw == [1, 2] and res["verdict"] == base_c["verdict"] and not res["disagreements"],
               f"twin fails at {tw}; verdict {res['verdict']}")
    p4 = [(x, y, -b, a) for (x, y, a, b) in poses]
    got, res = dec_j(side, p4)
    run.decisions += 1
    tw = check.twin(got["poses"], corners)
    good = margins_of(res) == m and clears_of(res) == list(cl) and res["verdict"] == base_j["verdict"] and tw == []
    run.record("T4", good and not res["disagreements"], f"verdict {res['verdict']}; twin fails at {tw}")

    # ------------------------------------------------------------------ geometric controls
    g1 = [*poses[:-1], poses[0]]
    _, res = dec_j(side, g1)
    run.decisions += 1
    want = {k: v for k, v in m.items() if n - 1 not in k}
    for k in range(1, n - 1):
        want[(k, n - 1)] = m[(0, k)]
    want[(0, n - 1)] = F(-1)
    want_over = {(0, n - 1)} | {(k, n - 1) for k in range(1, n - 1) if m[(0, k)] < 0}
    good = (res["verdict"] == "REFUSE" and margins_of(res) == want and overlapping(res) == want_over
            and res["pairs"][(0, n - 1)][3] == 1 and clears_of(res)[n - 1] == cl[0] and not res["disagreements"])
    run.record("G1", good, f"overlapping {sorted(overlapping(res))[:4]}")
    g2 = list(poses)
    g2[0] = (poses[0][0] + side, poses[0][1], poses[0][2], poses[0][3])
    _, res = dec_j(side, g2)
    run.decisions += 1
    L, B, R, T = cl[0]
    want = dict(m)
    for k in range(1, n):
        want[(0, k)] = geom.margin(g2[0], poses[k])
    cls = clears_of(res)
    good = (res["verdict"] == "REFUSE" and cls[0] == (L + side, B, R - side, T) and cls[1:] == list(cl[1:])
            and crossings(res) == {(0, "right")} and res["walls"][0]["inside_area"] == 0
            and margins_of(res) == want and all(want[(0, k)] >= 0 for k in range(1, n)) and not res["disagreements"])
    run.record("G2", good, f"crossings {sorted(crossings(res))}; least margin of square 1 "
               f"{check.sci(min(want[(0, k)] for k in range(1, n)))}")
    rot = [sq[1:] + sq[:1] for sq in corners]
    _, res = dec_c(cc["side"], rot, ids)
    run.decisions += 1
    run.record("G3", res["verdict"] == base_c["verdict"] and margins_of(res) == margins_of(base_c)
               and clears_of(res) == clears_of(base_c) and not res["disagreements"], f"verdict {res['verdict']}")
    rev = [sq[::-1] for sq in corners]
    _, res = dec_c(cc["side"], rev, ids)
    run.decisions += 1
    run.record("G4", res["verdict"] == base_c["verdict"] and margins_of(res) == margins_of(base_c)
               and clears_of(res) == clears_of(base_c) and res["sense"] == [-s for s in base_c["sense"]]
               and not res["disagreements"], f"verdict {res['verdict']}")
    for cid, mapped, perm in (
        ("G5", [(y, x, b, a) for (x, y, a, b) in poses], lambda c: (c[1], c[0], c[3], c[2])),
        ("G6", [(side - y, x, -b, a) for (x, y, a, b) in poses], lambda c: (c[3], c[0], c[1], c[2])),
        ("G7", [(side - x, y, -a, b) for (x, y, a, b) in poses], lambda c: (c[2], c[1], c[0], c[3])),
    ):
        _, res = dec_j(side, mapped)
        run.decisions += 1
        good = (margins_of(res) == m and clears_of(res) == [perm(c) for c in cl]
                and res["verdict"] == base_j["verdict"] and not res["disagreements"])
        run.record(cid, good, f"verdict {res['verdict']}")
    g8 = [*poses, poses[0]]
    got, res = dec_j(side, g8)
    run.decisions += 1
    want = dict(m)
    for k in range(1, n):
        want[(k, n)] = m[(0, k)]
    want[(0, n)] = F(-1)
    want_over = {(0, n)} | {(k, n) for k in range(1, n) if m[(0, k)] < 0}
    good = (got["n"] == n + 1 and res["verdict"] == "REFUSE" and margins_of(res) == want
            and overlapping(res) == want_over and not res["disagreements"])
    run.record("G8", good, f"n {got['n']}; overlapping {sorted(overlapping(res))[:4]}")

    # ------------------------------------------------------------------ side controls
    w_least = min(min(c[2], c[3]) for c in cl)
    outcomes: dict[str, str] = {}
    for cid, delta in (
        ("S1a", EPS),
        ("S1b", F(1, side.denominator)),
        ("S1c", w_least),
        ("S1d", w_least + EPS),
        ("S1e", side - claim),
        ("S1f", side - claim + F(1, 10**12)),
    ):
        _, res = dec_j(side - delta, poses)
        run.decisions += 1
        want_cross = {(k, "right") for k in range(n) if cl[k][2] < delta} | {(k, "top") for k in range(n) if cl[k][3] < delta}
        want_cl = [(c[0], c[1], c[2] - delta, c[3] - delta) for c in cl]
        want_verdict = "ACCEPT" if (base_ok and not want_cross) else "REFUSE"
        short_sq = {k for k, _ in want_cross}
        inside_low = {k for k, row in enumerate(res["walls"]) if row is not None and row["inside_area"] < 1}
        good = (margins_of(res) == m and clears_of(res) == want_cl and crossings(res) == want_cross
                and res["verdict"] == want_verdict and inside_low == short_sq and not res["disagreements"])
        if cid == "S1c":
            good = good and res["verdict"] == base_j["verdict"]
        if cid == "S1d":
            good = good and res["verdict"] == "REFUSE"
        outcomes[cid] = res["verdict"]
        names = sorted({k + 1 for k, _ in want_cross})
        run.record(cid, good, f"delta {check.sci(delta)}; {res['verdict']}; {len(want_cross)} crossings, squares "
                   f"{names[:12]}{'...' if len(names) > 12 else ''}")

    # ------------------------------------------------------------------ pair controls
    (pi, pj), _ = min(m.items(), key=lambda kv: (kv[1], kv[0]))
    for cid, target in (("P1c", F(0)), ("P1p", -EPS)):
        new = geom.close_toward(poses[pi], poses[pj], target)
        moved_p = list(poses)
        moved_p[pj] = new
        _, res = dec_j(side, moved_p)
        run.decisions += 1
        want = {k: v for k, v in m.items() if pj not in k}
        for k in range(n):
            if k != pj:
                key = (min(k, pj), max(k, pj))
                want[key] = geom.margin(moved_p[key[0]], moved_p[key[1]])
        want_cl = list(cl)
        want_cl[pj] = geom.clearances(side, new)
        want_verdict = "ACCEPT" if (base_ok and min(want.values()) >= 0 and min(min(c) for c in want_cl) >= 0) else "REFUSE"
        good = (want[(pi, pj)] == target and margins_of(res) == want and clears_of(res) == want_cl
                and res["pairs"][(pi, pj)][1] == ("contact" if target == 0 else "overlap")
                and res["verdict"] == want_verdict and not res["disagreements"])
        if cid == "P1p":
            good = good and res["verdict"] == "REFUSE"
        run.record(cid, good, f"pair ({pi + 1}, {pj + 1}), square {pj + 1} moved from margin {check.sci(m[(pi, pj)])}; "
                   f"{res['verdict']}")

    # ------------------------------------------------------------------ wall controls
    for cid, beyond in (("W1c", F(0)), ("W1p", EPS)):
        parts = []
        all_good = True
        for w, name in enumerate(WALLS):
            k = min(range(n), key=lambda s, w=w: (cl[s][w], s))
            new = geom.to_wall(side, poses[k], w, beyond)
            moved_p = list(poses)
            moved_p[k] = new
            _, res = dec_j(side, moved_p)
            run.decisions += 1
            step = cl[k][w] + beyond
            opp = (w + 2) % 4
            want_c = list(cl[k])
            want_c[w] = -beyond
            want_c[opp] = cl[k][opp] + step
            want = {key: v for key, v in m.items() if k not in key}
            for s in range(n):
                if s != k:
                    key = (min(s, k), max(s, k))
                    want[key] = geom.margin(moved_p[key[0]], moved_p[key[1]])
            want_cl = list(cl)
            want_cl[k] = tuple(want_c)
            pred_ok = base_ok and min(want.values()) >= 0 and min(min(c) for c in want_cl) >= 0
            want_verdict = "ACCEPT" if pred_ok else "REFUSE"
            good = (geom.clearances(side, new) == tuple(want_c) and margins_of(res) == want
                    and clears_of(res) == want_cl and res["verdict"] == want_verdict and not res["disagreements"])
            if beyond:
                good = good and crossings(res) == {(k, name)} and res["verdict"] == "REFUSE"
            all_good = all_good and good
            parts.append(f"{name}: square {k + 1} moved {check.sci(step)}, {res['verdict']}")
        run.record(cid, all_good, "; ".join(parts))

    # ------------------------------------------------------------------ pair by pair, square by square
    bad = 0
    count = 0
    ints = [poses_a.integer_pose(*p) for p in poses]
    bcorn = [clip.corners_from_pose(*p) for p in poses]
    for (i, j) in m:
        for target, cls in ((F(0), "contact"), (-EPS, "overlap")):
            new = geom.close_toward(poses[i], poses[j], target)
            ma = poses_a.margin(ints[i], poses_a.integer_pose(*new))
            mg = geom.margin(poses[i], new)
            got_b = clip.pair(bcorn[i], clip.corners_from_pose(*new), distance=False)
            count += 1
            if not (ma == target and mg == target and got_b[0] == cls):
                bad += 1
    run.record("PALL", bad == 0 and count == 2 * len(m), f"{count} closings, {bad} not as stated")
    bad = 0
    count = 0
    s_q = clip.q(side)
    for k in range(n):
        w = min(range(4), key=lambda x, k=k: (cl[k][x], x))
        for beyond, cls in ((F(0), "contact"), (EPS, "crossing")):
            new = geom.to_wall(side, poses[k], w, beyond)
            ca = poses_a.clearances(side, poses_a.integer_pose(*new))[w]
            cg = geom.clearances(side, new)[w]
            wb = clip.walls(s_q, clip.corners_from_pose(*new))
            inside_one = clip.fr(wb["inside2"]) == 2
            count += 1
            if not (ca == -beyond and cg == -beyond and wb["classes"][WALLS[w]] == cls and inside_one == (beyond == 0)):
                bad += 1
    run.record("WALL", bad == 0 and count == 2 * n, f"{count} moves, {bad} not as stated")

    priors = {
        "accepted": base_j["verdict"] == "ACCEPT" and base_c["verdict"] == "ACCEPT",
        "twins": check.twin(poses, corners) == [],
        "claim_is_ceiling_12": claim == check.ceiling_at(side, 12),
        "S1e_accepted_S1f_refused": outcomes.get("S1e") == "ACCEPT" and outcomes.get("S1f") == "REFUSE",
    }
    stated = sum(1 for r in run.rows if r["outcome"] == "as stated")
    planned = [c["id"] for c in plan["controls"] if c["id"] != "side rule"]
    missing = [cid for cid in planned if cid not in {r["id"] for r in run.rows}]
    verdict = "EVERY_CONTROL_AS_STATED" if stated == len(run.rows) and not missing else "NOT_EVERY_CONTROL_AS_STATED"
    receipt = {
        "program": "r1052_controls.py",
        "verdict": verdict,
        "as_stated": stated,
        "controls": len(run.rows),
        "planned_not_run": missing,
        "whole_file_decisions": run.decisions,
        "priors": priors,
        "rows": run.rows,
        "cpu_seconds": round(time.process_time() - t0, 1),
        "python": sys.version.split()[0],
    }
    Path(out_path).write_text(json.dumps(receipt, indent=1) + "\n")
    print(f"{verdict} {stated} of {len(run.rows)}")
    return 0 if verdict == "EVERY_CONTROL_AS_STATED" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
