"""Run the controls plan of the review of jlevy/squares#1031 (``controls-plan.json``).

Written for this review; imports nothing from this repository or the source.

    python -I -B rv1031_controls.py --json n299_exact.json --witness n299_witness.yaml \
        --claim 17.793636991744 --plan controls-plan.json --out controls.json

Each control changes the certificate (its bytes, or its squares in both forms, or its
side), decides the changed packing by both methods, and compares what they decide with
the outcome the plan states, evaluated here exactly from the original's facts.  A control
whose two methods disagree anywhere fails.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # this packet's own modules, under python -I

import rv1031_axes as A
import rv1031_clip as B
import rv1031_contract as K
import rv1031_decide as D
import rv1031_reader as R

EPS = F(1, 10**40)
HALF = F(1, 2)
WALLS = D.WALLS


def parse_decimal(text: str) -> F:
    a, b = text.split(".")
    return F(int(a + b), 10 ** len(b))


class Ctx:
    def __init__(self, json_path: str, witness_path: str, claim_text: str) -> None:
        with open(json_path, "rb") as fh:
            self.raw_j = fh.read()
        with open(witness_path, "rb") as fh:
            self.raw_c = fh.read()
        self.dj = R.read_json_bytes(self.raw_j)
        self.dc = R.read_witness_bytes(self.raw_c)
        self.n = self.dj["n"]
        self.side = self.dj["side"]
        self.poses = self.dj["poses"]
        self.corners = self.dc["corners"]
        self.claim = parse_decimal(claim_text)
        t0 = time.process_time()
        self.terms = {}
        for i in range(self.n):
            for j in range(i + 1, self.n):
                self.terms[(i, j)] = A.pair_terms(self.poses[i], self.poses[j])
        self.margins = {k: m - h for k, (m, h, _) in self.terms.items()}
        self.clear = A.all_clearances(self.poses, self.side)
        self.db = D.decide_b(self.corners, self.side)
        self.ext = D.extent(self.poses)
        self.cpu_setup = time.process_time() - t0


def translate(cs: list[tuple[F, F]], dx: F, dy: F) -> list[tuple[F, F]]:
    return [(x + dx, y + dy) for x, y in cs]


def centre_of(cs: list[tuple[F, F]]) -> tuple[F, F]:
    return (cs[0][0] + cs[2][0]) * HALF, (cs[0][1] + cs[2][1]) * HALF


def evaluate(ctx: Ctx, poses: list, corners: list, side: F, changed: set[int] | None) -> dict:
    """Both methods on a changed packing of n squares; ``changed`` None decides every pair,
    a set decides the pairs holding those squares and checks the rest read back unchanged."""
    n = len(poses)
    out: dict = {}
    if changed is None:
        pairs = None
        out["unchanged_read_back"] = None
    else:
        pairs = sorted({(min(i, k), max(i, k)) for i in changed for k in range(n) if k != i})
        out["unchanged_read_back"] = all(poses[k] == ctx.poses[k] and corners[k] == ctx.corners[k] for k in range(n) if k not in changed)
    da = D.decide_a(poses, side, pairs)
    db = D.decide_b(corners, side, pairs)
    if db.get("unit_failures"):
        out["unit_failures"] = [k + 1 for k in db["unit_failures"]]
        return out
    if changed is not None:
        margins = dict(ctx.margins)
        margins.update(da["margins"])
        classes = dict(ctx.db["classes"])
        classes.update(db["classes"])
        da = {"margins": margins, "clearances": da["clearances"]}
        db = {**db, "classes": classes}
    cmp_ = D.compare(da, db)
    sa = D.summarize_a(da, side, list_limit=10**6)
    out.update(
        da=da, db=db, compare=cmp_, summary=sa,
        methods_agree=not (cmp_["pair_mismatches"] or cmp_["wall_mismatches"] or cmp_["inside_not_one"]),
        accepted=D.verdict_ok(sa, cmp_),
        overlaps=sorted((i - 1, j - 1) for i, j, _ in sa["overlap_pairs"]),
        crossings=sorted((k - 1, w) for k, c in enumerate(da["clearances"], start=1) for w in range(4) if c[w] < 0),
    )
    return out


def brief(ev: dict) -> dict:
    if "unit_failures" in ev:
        return {"unit_failures": ev["unit_failures"]}
    return {
        "accepted": ev["accepted"],
        "methods_agree": ev["methods_agree"],
        "unchanged_read_back": ev["unchanged_read_back"],
        "classes": ev["summary"]["classes"],
        "overlaps": [[i + 1, j + 1] for i, j in ev["overlaps"][:20]],
        "overlap_count": len(ev["overlaps"]),
        "crossings": [[k + 1, WALLS[w]] for k, w in ev["crossings"][:20]],
        "crossing_count": len(ev["crossings"]),
        "wall_contacts": len(ev["summary"]["wall_contacts"]),
    }


def refused_by_reader(raw: bytes, form: str) -> tuple[bool, str]:
    try:
        if form == "J":
            R.read_json_bytes(raw)
        else:
            R.read_witness_bytes(raw)
    except R.ReadError as exc:
        return True, str(exc)[:160]
    return False, ""


ROW_RE = re.compile(rb'\n  \[\n(?:   "[^"]*",?\n){4}  \]')


def j_rows(raw: bytes) -> list[tuple[int, int]]:
    return [(m.start(), m.end()) for m in ROW_RE.finditer(raw)]


# ------------------------------------------------------------------------- the controls


def c_C0(ctx: Ctx) -> dict:
    mism = sum(1 for (i, j), m in ctx.margins.items() if A.corner_projection_margin(ctx.corners[i], ctx.corners[j]) != m)
    wm = 0
    for k, cs in enumerate(ctx.corners):
        xs = [x for x, _ in cs]
        ys = [y for _, y in cs]
        if (min(xs), min(ys), ctx.side - max(xs), ctx.side - max(ys)) != ctx.clear[k]:
            wm += 1
    return {"as_stated": mism == 0 and wm == 0, "pair_mismatches": mism, "wall_mismatches": wm, "pairs": len(ctx.margins), "squares": ctx.n}


def c_R1(ctx: Ctx) -> dict:
    rows = j_rows(ctx.raw_j)
    s, e = rows[-1]
    assert ctx.raw_j[s - 1:s] == b","
    raw_j = ctx.raw_j[: s - 1] + ctx.raw_j[e:]
    pos = ctx.raw_c.rfind(b"\n  - id: square-")
    raw_c = ctx.raw_c[: pos + 1]
    rj, mj = refused_by_reader(raw_j, "J")
    rc, mc = refused_by_reader(raw_c, "C")
    applied = len(j_rows(raw_j)) == ctx.n - 1 and raw_c.count(b"  - id: square-") == ctx.n - 1
    ok = applied and rj and rc and "listed" in mj and "listed" in mc
    return {"as_stated": ok, "applied": applied, "J": mj, "C": mc}


def side_text_c(ctx: Ctx) -> bytes:
    t = ctx.dc["facts"]["side_text"].encode()
    for form in (b"  side: " + t + b"\n", b"  side: '" + t + b"'\n"):
        if form in ctx.raw_c:
            return form
    raise AssertionError("side line not found in form C")


def c_R2(ctx: Ctx) -> dict:
    p, q = ctx.side.numerator, ctx.side.denominator
    new = f"{2 * p}/{2 * q}".encode()
    t = ctx.dj["facts"]["side_text"].encode()
    raw_j = ctx.raw_j.replace(b'"side": "' + t + b'"', b'"side": "' + new + b'"', 1)
    line = side_text_c(ctx)
    raw_c = ctx.raw_c.replace(line, line.replace(t, new), 1)
    dj = R.read_json_bytes(raw_j)
    dc = R.read_witness_bytes(raw_c)
    flagged = any("side: not in lowest terms" in x for x in dj["facts"]["notes"]) and any("side: not in lowest terms" in x for x in dc["facts"]["notes"])
    same = dj["side"] == ctx.side and dc["side"] == ctx.side and dj["poses"] == ctx.poses and dc["corners"] == ctx.corners
    applied = raw_j != ctx.raw_j and raw_c != ctx.raw_c
    return {"as_stated": applied and flagged and same, "applied": applied, "flagged": flagged, "values_equal": same, "verdict": "the original's (no value changed)"}


def c_R3(ctx: Ctx) -> dict:
    rows = j_rows(ctx.raw_j)
    (s1, e1), (s2, e2) = rows[0], rows[1]
    raw_j = ctx.raw_j[:s1] + ctx.raw_j[s2:e2] + ctx.raw_j[e1:s2] + ctx.raw_j[s1:e1] + ctx.raw_j[e2:]
    dj = R.read_json_bytes(raw_j)
    fails = [k + 1 for k in range(ctx.n) if R.twin_match(R.pose_corners(dj["poses"][k]), ctx.corners[k]) is None]
    raw_c = ctx.raw_c.replace(b"id: square-1\n", b"id: square-X\n", 1).replace(b"id: square-2\n", b"id: square-1\n", 1).replace(b"id: square-X\n", b"id: square-2\n", 1)
    rc, mc = refused_by_reader(raw_c, "C")
    ok = fails == [1, 2] and rc and "out of order" in mc
    return {"as_stated": ok, "J_twin_fails_at": fails, "C": mc}


def c_R4(ctx: Ctx) -> dict:
    v = ctx.side
    dec = str(v.numerator * 10**40 // v.denominator)
    dec = dec[:-40] + "." + dec[-40:]
    t = ctx.dj["facts"]["side_text"].encode()
    raw_j = ctx.raw_j.replace(b'"side": "' + t + b'"', b'"side": "' + dec.encode() + b'"', 1)
    line = side_text_c(ctx)
    raw_cq = ctx.raw_c.replace(line, b"  side: '" + dec.encode() + b"'\n", 1)
    raw_cu = ctx.raw_c.replace(line, b"  side: " + dec.encode() + b"\n", 1)
    out = {}
    ok = True
    for name, raw, form in (("J", raw_j, "J"), ("C quoted", raw_cq, "C"), ("C unquoted", raw_cu, "C")):
        r, m = refused_by_reader(raw, form)
        out[name] = m
        ok = ok and r and raw != (ctx.raw_j if form == "J" else ctx.raw_c)
    ok = ok and "not a scalar" in out["J"] and "not a scalar" in out["C quoted"] and "not a string" in out["C unquoted"]
    return {"as_stated": ok, **out}


def c_R5(ctx: Ctx) -> dict:
    raw_j = ctx.raw_j.replace(b'"squares": [\n  [\n   "', b'"squares": [\n  [\n   "+', 1)
    pos = ctx.raw_c.find(b"    - - ") + len(b"    - - ")
    quote = ctx.raw_c[pos:pos + 1] == b"'"
    ins = pos + 1 if quote else pos
    raw_c = ctx.raw_c[:ins] + b"+" + ctx.raw_c[ins:]
    rj, mj = refused_by_reader(raw_j, "J")
    rc, mc = refused_by_reader(raw_c, "C")
    applied = raw_j != ctx.raw_j and raw_c != ctx.raw_c
    return {"as_stated": applied and rj and rc, "J": mj, "C": mc}


def c_R6(ctx: Ctx) -> dict:
    nn = str(ctx.n).encode()
    raw_j = ctx.raw_j.replace(b'"n": ' + nn + b",", b'"n": ' + nn + b',\n "n": ' + nn + b",", 1)
    raw_c = ctx.raw_c.replace(b"  n: " + nn + b"\n", b"  n: " + nn + b"\n  n: " + nn + b"\n", 1)
    rj, mj = refused_by_reader(raw_j, "J")
    rc, mc = refused_by_reader(raw_c, "C")
    applied = raw_j != ctx.raw_j and raw_c != ctx.raw_c
    return {"as_stated": applied and rj and rc and "duplicate" in mj and "duplicate" in mc, "J": mj, "C": mc}


def c_R7(ctx: Ctx) -> dict:
    k = next(i for i, p in enumerate(ctx.poses) if p[3] != 0)
    rows = j_rows(ctx.raw_j)
    s, e = rows[k]
    block = ctx.raw_j[s:e]
    vals = re.findall(rb'"([^"]*)"', block)
    cos_t = vals[2]
    c = ctx.poses[k][2]
    new = f"{c.numerator * 10**40 + c.denominator}/{c.denominator * 10**40}".encode()
    nb = block.replace(b'"' + cos_t + b'"', b'"' + new + b'"', 1)
    raw_j = ctx.raw_j[:s] + nb + ctx.raw_j[e:]
    r, m = refused_by_reader(raw_j, "J")
    return {"as_stated": nb != block and r and "unit" in m, "square": k + 1, "J": m}


def c_G1(ctx: Ctx) -> dict:
    n = ctx.n
    poses = list(ctx.poses)
    corners = list(ctx.corners)
    poses[n - 1] = ctx.poses[0]
    corners[n - 1] = ctx.corners[0]
    ev = evaluate(ctx, poses, corners, ctx.side, {n - 1})
    m = ev["da"]["margins"]
    pred = m[(0, n - 1)] == -1 and all(m[(k, n - 1)] == ctx.margins[(0, k)] for k in range(1, n - 1))
    area = ev["db"]["classes"][(0, n - 1)][1]
    ok = pred and ev["overlaps"] == [(0, n - 1)] and area == 1 and not ev["accepted"] and ev["methods_agree"] and ev["unchanged_read_back"]
    return {"as_stated": ok, "margins_predicted": pred, "b_area": str(area), **brief(ev)}


def c_G2(ctx: Ctx) -> dict:
    s = ctx.side
    poses = list(ctx.poses)
    corners = list(ctx.corners)
    cx, cy, ux, uy = poses[0]
    poses[0] = (cx + s, cy, ux, uy)
    corners[0] = translate(ctx.corners[0], s, F(0))
    ev = evaluate(ctx, poses, corners, s, {0})
    L, Bc, Rc, T = ctx.clear[0]
    pred = ev["da"]["clearances"][0] == (L + s, Bc, Rc - s, T)
    inside0 = ev["db"]["inside"][0] == 0
    no_pair = not any(0 in key for key in ev["overlaps"])
    ok = pred and inside0 and no_pair and not ev["accepted"] and ev["methods_agree"] and ev["unchanged_read_back"]
    return {"as_stated": ok, "clearances_predicted": pred, "area_inside_zero": inside0, **brief(ev)}


def c_G3(ctx: Ctx) -> dict:
    corners = list(ctx.corners)
    c0 = list(ctx.corners[0])
    c0[0] = (c0[0][0] + EPS, c0[0][1])
    corners[0] = c0
    bad_b = [k + 1 for k, cs in enumerate(corners) if B.unit_square_sense(B.to_mpq(cs)) is None]
    no_pose = [k + 1 for k, cs in enumerate(corners) if R.corners_pose(cs) is None]
    twin = [k + 1 for k in range(ctx.n) if R.twin_match(R.pose_corners(ctx.poses[k]), corners[k]) is None]
    ok = bad_b == [1] and no_pose == [1] and twin == [1]
    return {"as_stated": ok, "b_not_unit": bad_b, "no_pose": no_pose, "twin_fails": twin, "verdict": "refused" if bad_b else "?"}


def whole(ctx: Ctx, poses: list, corners: list, side: F, perm: tuple[int, int, int, int] | None, sense: str | None, twin_off: int | None, extra_pred=None, b_same_required: bool = True) -> dict:
    ev = evaluate(ctx, poses, corners, side, None)
    b_same = all(ev["db"]["classes"][k] == v for k, v in ctx.db["classes"].items()) if "db" in ev else False
    m = ev["da"]["margins"]
    same_m = m == ctx.margins if extra_pred is None else extra_pred(ev)
    if perm is not None:
        clear_ok = all(ev["da"]["clearances"][k] == tuple(ctx.clear[k][perm[w]] for w in range(4)) for k in range(ctx.n))
    else:
        clear_ok = True
    senses = ev["db"]["senses"]
    sense_ok = True if sense is None else all(s_ == sense for s_ in senses)
    twin_ok = True
    if twin_off is not None:
        twin_ok = all(R.twin_match(R.pose_corners(poses[k]), corners[k]) is not None for k in range(ctx.n))
    orig_ok = D.verdict_ok(D.summarize_a({"margins": ctx.margins, "clearances": ctx.clear}, ctx.side), D.compare({"margins": ctx.margins, "clearances": ctx.clear}, ctx.db))
    ok = same_m and clear_ok and sense_ok and twin_ok and ev["methods_agree"] and ev["accepted"] == orig_ok and (b_same or not b_same_required)
    return {"as_stated": ok, "margins_as_predicted": same_m, "clearances_permuted": clear_ok, "b_classes_and_areas_as_original": b_same, "senses": {"ccw": senses.count("ccw"), "cw": senses.count("cw")}, "twin_holds": twin_ok, **brief(ev)}


def c_G4(ctx: Ctx) -> dict:
    corners = [list(reversed(cs)) for cs in ctx.corners]
    poses = [R.corners_pose(cs) for cs in corners]
    r = whole(ctx, poses, corners, ctx.side, (0, 1, 2, 3), "cw", 0)
    offs = {R.twin_match(R.pose_corners(ctx.poses[k]), corners[k]) for k in range(ctx.n)}
    r["twin_listings"] = sorted(f"{o} {s}" for o, s in offs if o is not None)
    return r


def c_G5(ctx: Ctx) -> dict:
    corners = [cs[1:] + cs[:1] for cs in ctx.corners]
    poses = [R.corners_pose(cs) for cs in corners]
    orig = {R.twin_match(R.pose_corners(ctx.poses[k]), ctx.corners[k]) for k in range(ctx.n)}
    new = {R.twin_match(R.pose_corners(ctx.poses[k]), corners[k]) for k in range(ctx.n)}
    shifted = {(o + 1) % 4 if s == "ccw" else (o - 1) % 4 for o, s in orig} == {o for o, _ in new} and {s for _, s in orig} == {s for _, s in new}
    r = whole(ctx, poses, corners, ctx.side, (0, 1, 2, 3), None, 0)
    senses_same = r["senses"] == {"ccw": [s for s in ctx.db["senses"]].count("ccw"), "cw": [s for s in ctx.db["senses"]].count("cw")}
    r["twin_offsets_moved_by_one"] = shifted
    r["as_stated"] = r["as_stated"] and shifted and senses_same
    return r


def c_G6(ctx: Ctx) -> dict:
    poses = [(cy, cx, uy, ux) for cx, cy, ux, uy in ctx.poses]
    corners = [[(y, x) for x, y in cs] for cs in ctx.corners]
    return whole(ctx, poses, corners, ctx.side, (1, 0, 3, 2), None, 0)


def c_G7(ctx: Ctx) -> dict:
    s = ctx.side
    poses = [(s - cy, cx, -uy, ux) for cx, cy, ux, uy in ctx.poses]
    corners = [[(s - y, x) for x, y in cs] for cs in ctx.corners]
    return whole(ctx, poses, corners, s, (3, 0, 1, 2), None, 0)


def c_G8(ctx: Ctx) -> dict:
    s = ctx.side
    poses = [(s - cx, cy, -ux, uy) for cx, cy, ux, uy in ctx.poses]
    corners = [[(s - x, y) for x, y in cs] for cs in ctx.corners]
    return whole(ctx, poses, corners, s, (2, 1, 0, 3), None, 0)


def side_rule(ctx: Ctx, delta: F) -> dict:
    side = ctx.side - delta
    ca = A.all_clearances(ctx.poses, side)
    db = D.decide_b(ctx.corners, side, pairs=[])
    pred = all(ca[k] == (c[0], c[1], c[2] - delta, c[3] - delta) for k, c in enumerate(ctx.clear))
    b_eq = all(tuple(B.mpq_to_fraction(x) for x in db["walls"][k]) == ca[k] for k in range(ctx.n))
    cross = sorted((k, w) for k, c in enumerate(ctx.clear) for w in (2, 3) if c[w] < delta)
    cross_got = sorted((k, w) for k, c in enumerate(ca) for w in range(4) if c[w] < 0)
    contact_exp = sorted({(k, w) for k, c in enumerate(ctx.clear) for w in (2, 3) if c[w] == delta} | {(k, w) for k, c in enumerate(ctx.clear) for w in (0, 1) if c[w] == 0})
    contact_got = sorted((k, w) for k, c in enumerate(ca) for w in range(4) if c[w] == 0)
    inside_ok = all((db["inside"][k] == 1) == (min(ca[k]) >= 0) for k in range(ctx.n))
    ok = pred and b_eq and cross == cross_got and contact_exp == contact_got and inside_ok
    return {
        "as_stated": ok, "delta": D.short(delta), "side": D.short(side, 20), "accepted": not cross_got,
        "crossings": len(cross_got), "contacts_right_top": len([1 for k, w in contact_got if w in (2, 3)]),
        "rule_holds": pred, "b_equal": b_eq,
    }


def least_rt(ctx: Ctx) -> F:
    return min(min(c[2], c[3]) for c in ctx.clear)


def c_S1a(ctx: Ctx) -> dict:
    return side_rule(ctx, EPS)


def c_S1b(ctx: Ctx) -> dict:
    return side_rule(ctx, F(1, ctx.side.denominator))


def c_S1c(ctx: Ctx) -> dict:
    r = side_rule(ctx, least_rt(ctx))
    r["as_stated"] = r["as_stated"] and r["accepted"]
    r["W"] = D.fstr(least_rt(ctx))
    return r


def c_S1d(ctx: Ctx) -> dict:
    r = side_rule(ctx, least_rt(ctx) + EPS)
    w = least_rt(ctx)
    att = sum(1 for c in ctx.clear for x in (c[2], c[3]) if x == w)
    r["as_stated"] = r["as_stated"] and not r["accepted"] and r["crossings"] == att
    return r


def c_S1e(ctx: Ctx) -> dict:
    return side_rule(ctx, ctx.side - ctx.claim)


def c_S1f(ctx: Ctx) -> dict:
    return side_rule(ctx, ctx.side - ctx.claim + F(1, 10**12))


def extent_case(ctx: Ctx, past: bool) -> dict:
    e = ctx.ext
    xmin, ymin = e["xmin"], e["ymin"]
    X = max(e["width"], e["height"])
    side = X - EPS if past else X
    poses = [(cx - xmin, cy - ymin, ux, uy) for cx, cy, ux, uy in ctx.poses]
    corners = [translate(cs, -xmin, -ymin) for cs in ctx.corners]
    ev = evaluate(ctx, poses, corners, side, None)
    pred_clear = [A.clearances(p, side) for p in poses]
    ok_clear = ev["da"]["clearances"] == pred_clear
    same_m = ev["da"]["margins"] == ctx.margins
    exp_contacts = set()
    for k, (cx, cy, ux, uy) in enumerate(ctx.poses):
        h = A.half_extent(ctx.poses[k])
        if cx - h == xmin:
            exp_contacts.add((k, 0))
        if cy - h == ymin:
            exp_contacts.add((k, 1))
        if not past and e["width"] == X and cx + h == e["xmax"]:
            exp_contacts.add((k, 2))
        if not past and e["height"] == X and cy + h == e["ymax"]:
            exp_contacts.add((k, 3))
    got_contacts = {(k - 1, WALLS.index(w)) for k, w in ev["summary"]["wall_contacts"]}
    exp_cross = set()
    if past:
        for k, (cx, cy, ux, uy) in enumerate(ctx.poses):
            h = A.half_extent(ctx.poses[k])
            if e["width"] == X and cx + h == e["xmax"]:
                exp_cross.add((k, 2))
            if e["height"] == X and cy + h == e["ymax"]:
                exp_cross.add((k, 3))
    got_cross = set(ev["crossings"])
    ok = ok_clear and same_m and got_contacts == exp_contacts and got_cross == exp_cross and ev["methods_agree"] and ev["accepted"] == (not past)
    return {"as_stated": ok, "X": D.fstr(X), "width_equals_height": e["width"] == e["height"], "translation": [D.short(-xmin), D.short(-ymin)], "contacts": len(got_contacts), **brief(ev)}


def c_E1c(ctx: Ctx) -> dict:
    return extent_case(ctx, False)


def c_E1p(ctx: Ctx) -> dict:
    return extent_case(ctx, True)


def c_K1c(ctx: Ctx) -> dict:
    g = 1 + EPS
    s = ctx.side
    poses = [(g * cx, g * cy, ux, uy) for cx, cy, ux, uy in ctx.poses]
    corners = []
    for cs in ctx.corners:
        ccx, ccy = centre_of(cs)
        corners.append(translate(cs, EPS * ccx, EPS * ccy))

    def pred(ev: dict) -> bool:
        m = ev["da"]["margins"]
        return all(m[k] == g * mm - h for k, (mm, h, _) in ctx.terms.items())

    r = whole(ctx, poses, corners, g * s, None, None, 0, extra_pred=pred, b_same_required=False)
    exp_clear = all(
        A.clearances(poses[k], g * s) == (c[0] + EPS * ctx.poses[k][0], c[1] + EPS * ctx.poses[k][1], c[2] + EPS * (s - ctx.poses[k][0]), c[3] + EPS * (s - ctx.poses[k][1]))
        for k, c in enumerate(ctx.clear)
    )
    r["clearances_predicted"] = exp_clear
    r["as_stated"] = r["as_stated"] and exp_clear and r["accepted"] and r["classes"]["contact"] == 0 and r["wall_contacts"] == 0
    return r


def c_K1p(ctx: Ctx) -> dict:
    g = 1 - EPS
    s = ctx.side
    mid = s * HALF
    poses = [(mid + g * (cx - mid), mid + g * (cy - mid), ux, uy) for cx, cy, ux, uy in ctx.poses]
    corners = []
    for cs in ctx.corners:
        ccx, ccy = centre_of(cs)
        corners.append(translate(cs, -EPS * (ccx - mid), -EPS * (ccy - mid)))

    def pred(ev: dict) -> bool:
        m = ev["da"]["margins"]
        return all(m[k] == g * mm - h for k, (mm, h, _) in ctx.terms.items())

    ev = evaluate(ctx, poses, corners, s, None)
    margins_ok = pred(ev)
    exp_over = sorted(k for k, (mm, h, _) in ctx.terms.items() if g * mm < h)
    exp_clear = all(
        ev["da"]["clearances"][k] == (c[0] + EPS * (mid - ctx.poses[k][0]), c[1] + EPS * (mid - ctx.poses[k][1]), c[2] + EPS * (ctx.poses[k][0] - mid), c[3] + EPS * (ctx.poses[k][1] - mid))
        for k, c in enumerate(ctx.clear)
    )
    ok = margins_ok and ev["overlaps"] == exp_over and exp_clear and not ev["crossings"] and ev["methods_agree"]
    return {"as_stated": ok, "margins_predicted": margins_ok, "clearances_predicted": exp_clear, "expected_overlaps": len(exp_over), **brief(ev)}


def moved_square(ctx: Ctx, k: int, cx: F, cy: F) -> tuple[list, list]:
    poses = list(ctx.poses)
    corners = list(ctx.corners)
    ox, oy, ux, uy = ctx.poses[k]
    poses[k] = (cx, cy, ux, uy)
    corners[k] = translate(ctx.corners[k], cx - ox, cy - oy)
    return poses, corners


def closing(ctx: Ctx, i: int, j: int, mover: int, target: F) -> tuple[F, F]:
    mm, h, _ = ctx.terms[(i, j)]
    s = (target + h) / mm
    pi, pj = ctx.poses[i], ctx.poses[j]
    dx, dy = pj[0] - pi[0], pj[1] - pi[1]
    if mover == j:
        return pi[0] + s * dx, pi[1] + s * dy
    return pj[0] - s * dx, pj[1] - s * dy


def eligible_move(ctx: Ctx, k: int, cx: F, cy: F, skip: int | None, allow_cross_wall: int | None = None) -> bool:
    p = (cx, cy, ctx.poses[k][2], ctx.poses[k][3])
    for o in range(ctx.n):
        if o == k or o == skip:
            continue
        key = (min(k, o), max(k, o))
        if A.klass(A.pair_margin(p, ctx.poses[o])) != A.klass(ctx.margins[key]):
            return False
    c = A.clearances(p, ctx.side)
    return all(c[w] >= 0 for w in range(4) if w != allow_cross_wall)


def c_P1(ctx: Ctx) -> tuple[dict, dict]:
    pos = sorted((m, key) for key, m in ctx.margins.items() if m > 0)
    tried = 0
    for m, (i, j) in pos[:300]:
        for mover in (j, i):
            tried += 1
            other = i if mover == j else j
            c0 = closing(ctx, i, j, mover, F(0))
            c1 = closing(ctx, i, j, mover, -EPS)
            if not (eligible_move(ctx, mover, *c0, skip=other) and eligible_move(ctx, mover, *c1, skip=other)):
                continue
            out = []
            for target, cc in ((F(0), c0), (-EPS, c1)):
                poses, corners = moved_square(ctx, mover, *cc)
                ev = evaluate(ctx, poses, corners, ctx.side, {mover})
                mij = ev["da"]["margins"][(i, j)]
                kb = ev["db"]["classes"][(i, j)][0]
                others_same = all(
                    A.klass(ev["da"]["margins"][(min(mover, o), max(mover, o))]) == A.klass(ctx.margins[(min(mover, o), max(mover, o))])
                    for o in range(ctx.n) if o not in (i, j)
                )
                if target == 0:
                    ok = mij == 0 and kb == "contact" and others_same and ev["accepted"] and ev["methods_agree"] and ev["unchanged_read_back"]
                else:
                    ok = mij == -EPS and kb == "overlap" and ev["overlaps"] == [(i, j)] and not ev["accepted"] and ev["methods_agree"] and ev["unchanged_read_back"]
                out.append({"as_stated": ok, "pair": [i + 1, j + 1], "moved": mover + 1, "original_margin": D.short(m), "margin": D.short(mij) if mij else "0", "b_class": kb, "candidates_tried": tried, **brief(ev)})
            return out[0], out[1]
    none = {"as_stated": False, "note": f"no eligible pair among the first {tried} candidates"}
    return none, none


def c_P0p(ctx: Ctx) -> dict:
    contacts = sorted(k for k, m in ctx.margins.items() if m == 0)
    if not contacts:
        return {"as_stated": True, "note": "no pair in contact: not applicable"}
    i, j = contacts[0]
    cc = closing(ctx, i, j, j, -EPS)
    poses, corners = moved_square(ctx, j, *cc)
    ev = evaluate(ctx, poses, corners, ctx.side, {j})
    p = poses[j]
    exp = sorted((min(j, o), max(j, o)) for o in range(ctx.n) if o != j and A.pair_margin(p, ctx.poses[o]) < 0)
    got = sorted(key for key in ev["overlaps"] if j in key)
    mij = ev["da"]["margins"][(i, j)]
    ok = mij == -EPS and got == exp and (i, j) in got and not ev["accepted"] and ev["methods_agree"] and ev["unchanged_read_back"]
    return {"as_stated": ok, "pair": [i + 1, j + 1], "moved": j + 1, "margin_exact_minus_eps": mij == -EPS, "overlapping_pairs_of_moved": [[a + 1, b + 1] for a, b in got], **brief(ev)}


WALL_DIR = {0: (-1, 0), 1: (0, -1), 2: (1, 0), 3: (0, 1)}


def wall_move(ctx: Ctx, k: int, w: int, dist: F) -> tuple[F, F]:
    dx, dy = WALL_DIR[w]
    return ctx.poses[k][0] + dx * dist, ctx.poses[k][1] + dy * dist


def c_W1(ctx: Ctx) -> tuple[dict, dict, dict]:
    res_c, res_p, res_0 = {}, {}, {}
    for w in range(4):
        cands = sorted((c[w], k) for k, c in enumerate(ctx.clear) if c[w] > 0)
        done = False
        for cl, k in cands[:200]:
            at = wall_move(ctx, k, w, cl)
            past = wall_move(ctx, k, w, cl + EPS)
            if not (eligible_move(ctx, k, *at, skip=None) and eligible_move(ctx, k, *past, skip=None, allow_cross_wall=w)):
                continue
            for tgt, cc, store in ((F(0), at, res_c), (-EPS, past, res_p)):
                poses, corners = moved_square(ctx, k, *cc)
                ev = evaluate(ctx, poses, corners, ctx.side, {k})
                c_new = ev["da"]["clearances"][k]
                opp = {0: 2, 1: 3, 2: 0, 3: 1}[w]
                raised = c_new[opp] == ctx.clear[k][opp] + cl + (EPS if tgt else 0)
                if tgt == 0:
                    ok = c_new[w] == 0 and raised and ev["accepted"] and ev["methods_agree"] and ev["unchanged_read_back"]
                else:
                    ok = c_new[w] == -EPS and ev["crossings"] == [(k, w)] and not ev["overlaps"] and not ev["accepted"] and ev["methods_agree"] and ev["unchanged_read_back"]
                store[WALLS[w]] = {"as_stated": ok, "square": k + 1, "clearance": D.short(cl), "opposite_raised": raised, **brief(ev)}
            done = True
            break
        if not done:
            res_c[WALLS[w]] = res_p[WALLS[w]] = {"as_stated": True, "note": "no eligible square with a positive clearance at this wall among the 200 nearest: not applicable"}
        zero = [k for k, c in enumerate(ctx.clear) if c[w] == 0]
        res_0[WALLS[w]] = {"as_stated": True, "note": "no square in contact with this wall: not applicable"}
        for k in zero:
            past = wall_move(ctx, k, w, EPS)
            p = (past[0], past[1], ctx.poses[k][2], ctx.poses[k][3])
            if any(A.pair_margin(p, ctx.poses[o]) < 0 for o in range(ctx.n) if o != k):
                continue
            poses, corners = moved_square(ctx, k, *past)
            ev = evaluate(ctx, poses, corners, ctx.side, {k})
            ok = ev["da"]["clearances"][k][w] == -EPS and ev["crossings"] == [(k, w)] and not ev["overlaps"] and not ev["accepted"] and ev["methods_agree"] and ev["unchanged_read_back"]
            res_0[WALLS[w]] = {"as_stated": ok, "square": k + 1, "squares_in_contact": len(zero), **brief(ev)}
            break
    agg = lambda d: {"as_stated": all(v["as_stated"] for v in d.values()), "walls": d}  # noqa: E731
    return agg(res_c), agg(res_p), agg(res_0)


def c_WALL(ctx: Ctx) -> dict:
    bad = 0
    moves = 0
    side_q = B.mpq(ctx.side.numerator, ctx.side.denominator)
    for k, c in enumerate(ctx.clear):
        w = min(range(4), key=lambda x: (c[x], x))
        for tgt in (F(0), -EPS):
            cc = wall_move(ctx, k, w, c[w] - tgt)
            p = (cc[0], cc[1], ctx.poses[k][2], ctx.poses[k][3])
            ca = A.clearances(p, ctx.side)[w]
            cs = B.ccw(B.to_mpq(translate(ctx.corners[k], cc[0] - ctx.poses[k][0], cc[1] - ctx.poses[k][1])))
            cb = B.mpq_to_fraction(B.wall_terms(cs, side_q)[w])
            inside = B.area_inside(cs, side_q)
            ok = ca == tgt and cb == tgt and ((inside == 1) if tgt == 0 else (inside < 1))
            moves += 1
            bad += 0 if ok else 1
    return {"as_stated": bad == 0, "squares": ctx.n, "moves": moves, "failures": bad}


def c_PALL(ctx: Ctx) -> dict:
    bad = []
    closings = 0
    for (i, j), (mm, h, _) in ctx.terms.items():
        ci = ctx.corners[i]
        cqi = B.ccw(B.to_mpq(ci))
        for tgt in (F(0), -EPS):
            cx, cy = closing(ctx, i, j, j, tgt)
            pj = (cx, cy, ctx.poses[j][2], ctx.poses[j][3])
            ma = A.pair_margin(ctx.poses[i], pj)
            cj = translate(ctx.corners[j], cx - ctx.poses[j][0], cy - ctx.poses[j][1])
            mc = A.corner_projection_margin(ci, cj)
            kb, area = B.pair_class(cqi, B.ccw(B.to_mpq(cj)))
            want = "contact" if tgt == 0 else "overlap"
            closings += 1
            if not (ma == tgt and mc == tgt and kb == want and (area == 0 if tgt == 0 else area > 0)):
                bad.append([i + 1, j + 1, D.short(tgt)])
    return {"as_stated": not bad, "pairs": len(ctx.terms), "closings": closings, "failures": bad[:20], "failure_count": len(bad)}


def c_X1(ctx: Ctx) -> dict:
    poses = [(cx, cy, ux, -uy) for cx, cy, ux, uy in ctx.poses]
    exp = sorted(k + 1 for k, p in enumerate(ctx.poses) if p[2] * p[3] != 0 and abs(p[2]) != abs(p[3]))
    got = sorted(k + 1 for k in range(ctx.n) if R.twin_match(R.pose_corners(poses[k]), ctx.corners[k]) is None)
    corners = [R.pose_corners(p) for p in poses]
    ev = evaluate(ctx, poses, corners, ctx.side, None)
    ok = exp == got and ev["methods_agree"]
    return {"as_stated": ok, "twin_fails_at_count": len(got), "expected_count": len(exp), **brief(ev)}


def c_T1(ctx: Ctx) -> dict:
    X = max(ctx.ext["width"], ctx.ext["height"])
    has_contact = any(m == 0 for m in ctx.margins.values())
    r0 = K.contraction(ctx.poses, ctx.side, verify=True)
    ok0 = r0["verdict"] == "MEASURED" and (F(r0["g_star"]) == 1) == has_contact and (not has_contact or F(r0["contraction_margin"]) == ctx.side - X)
    g = 1 + EPS
    dil = [(g * cx, g * cy, ux, uy) for cx, cy, ux, uy in ctx.poses]
    r1 = K.contraction(dil, g * ctx.side, verify=True)
    ok1 = r1["verdict"] == "MEASURED" and (F(r1["g_star"]) == 1 / g) == has_contact and (not has_contact or F(r1["contraction_margin"]) == g * ctx.side - X)
    return {
        "as_stated": ok0 and ok1, "has_contact": has_contact,
        "original": {k: r0.get(k) for k in ("verdict", "one_less_g_star_short", "contraction_margin_short", "verify")},
        "dilation": {k: r1.get(k) for k in ("verdict", "one_less_g_star_short", "contraction_margin_short", "verify")},
    }


ORDER = ["C0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8",
         "S1a", "S1b", "S1c", "S1d", "S1e", "S1f", "E1c", "E1p", "K1c", "K1p", "P1", "P0p", "W1", "WALL", "PALL", "X1", "T1"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--witness", required=True)
    ap.add_argument("--claim", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--only", default="")
    ap.add_argument("--mutant", default="", help="run under a broken copy: always-accept, always-refuse, or a name in rv1031_selftest.PATCHES")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    with open(args.plan, "rb") as fh:
        plan_raw = fh.read()
    plan = json.loads(plan_raw)
    stated = {c["id"]: c["stated"] for c in plan["controls"]}
    t0 = time.process_time()
    patches: list = []
    if args.mutant:
        import rv1031_selftest as S

        if args.mutant == "always-accept":
            patches = [(D, "verdict_ok", lambda sa, c: True)]
        elif args.mutant == "always-refuse":
            patches = [(D, "verdict_ok", lambda sa, c: False)]
        else:
            patches = S.PATCHES[args.mutant]
        S.patched(patches).__enter__()
    try:
        ctx = Ctx(args.json, args.witness, args.claim)
    except Exception as exc:  # a broken copy may refuse the original itself
        rec0 = {"program": "rv1031_controls.py", "mutant": args.mutant, "verdict": "SETUP_FAILED", "error": str(exc)[:200]}
        with open(args.out, "w") as fh:
            json.dump(rec0, fh, indent=1, sort_keys=True)
            fh.write("\n")
        print(rec0["verdict"], rec0["error"])
        return 1
    rec: dict = {"program": "rv1031_controls.py", "python": sys.version.split()[0], "arith": B.version(), "plan_sha256": hashlib.sha256(plan_raw).hexdigest(), "setup_cpu_s": round(ctx.cpu_setup, 1), "mutant": args.mutant, "controls": {}}
    only = set(args.only.split(",")) if args.only else None
    for cid in ORDER:
        if only and cid not in only:
            continue
        t1 = time.process_time()
        if cid == "P1":
            a, b = c_P1(ctx)
            results = {"P1c": a, "P1p": b}
        elif cid == "W1":
            a, b, c = c_W1(ctx)
            results = {"W1c": a, "W1p": b, "W0p": c}
        else:
            try:
                results = {cid: globals()[f"c_{cid}"](ctx)}
            except Exception as exc:  # under a broken copy a control may crash: it is then not as stated
                if not args.mutant:
                    raise
                results = {cid: {"as_stated": False, "error": f"{type(exc).__name__}: {str(exc)[:160]}"}}
        dt = round(time.process_time() - t1, 1)
        for k, v in results.items():
            v["stated"] = stated.get(k, "")
            v["cpu_s"] = dt
            rec["controls"][k] = v
            print(k, "AS_STATED" if v["as_stated"] else "NOT_AS_STATED", dt, flush=True)
    failed = [k for k, v in rec["controls"].items() if not v["as_stated"]]
    rec["failed"] = failed
    rec["verdict"] = "EVERY_CONTROL_AS_STATED" if not failed else "CONTROLS_NOT_AS_STATED"
    rec["cpu_s_total"] = round(time.process_time() - t0, 1)
    with open(args.out, "w") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True, default=str)
        fh.write("\n")
    print(rec["verdict"], failed)
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
