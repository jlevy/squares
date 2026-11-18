"""Run the frozen controls plan (controls-plan.json) on one certificate (lane r1021-1118).

Usage, from this packet's programs/ directory:

    python -I -B r1021_controls.py report LABEL FORM_J FORM_C OUT.json
    python -I -B r1021_controls.py house LABEL CORNERS OUT.json

Each control changes the certificate as the plan says, writes the changed packing as
the bytes of the file(s) it concerns in the source's own layout, reads them back
through the strict readers and decides them with r1021_check, then evaluates the
plan's stated outcome exactly over the original's exact facts.  PALL, WALL and C0
decide single pairs and squares and need no file.  KC replaces the checker's verdict
by a constant.  The receipt lists every control with "as_stated" and the facts its
rule compared.
"""

from __future__ import annotations

import os as _os
import sys as _sys

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # this packet's programs/, run with -I

import json
import time
from fractions import Fraction

import r1021_check as chk
import r1021_clip as clipmod
import r1021_contract as con
import r1021_geom as geom
import r1021_read as rd
from r1021_fmt import ceil_places, floor_places, frac_text, sci

EPS = Fraction(1, 10**40)
PLAN = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "controls-plan.json")


# ------------------------------------------------------------------ writers


def write_form_j(n: int, side_text: str, rows_text) -> bytes:
    obj = {"n": n, "side": side_text, "square_size": "1", "format": rd.FORMAT_SENTENCE, "squares": rows_text}
    return (json.dumps(obj, indent=1) + "\n").encode("ascii")


def rows_text(poses):
    return [[frac_text(v) for v in p] for p in poses]


class CornersLayout:
    """The header and trailer lines of a corners file, to write changed squares in its layout."""

    def __init__(self, raw: bytes, n: int, id_style: str):
        lines = raw.decode("ascii").split("\n")
        i = lines.index("  squares:")
        self.header = lines[: i + 1]
        self.trailer = lines[i + 1 + 10 * n:]
        self.id_style = id_style

    def write(self, side_text: str, squares, n: int | None = None) -> bytes:
        head = [f"  side: {side_text}" if ln.startswith("  side: ") else ln for ln in self.header]
        if n is not None:
            head = [f"  n: {n}" if ln.startswith("  n: ") else ln for ln in head]
        body = []
        for k, q in enumerate(squares, start=1):
            ident = f"square-{k}" if self.id_style == "square-k" else str(k)
            body += [f"  - id: {ident}", "    corners:"]
            for x, y in q:
                body += [f"    - - {frac_text(x)}", f"      - {frac_text(y)}"]
        return "\n".join(head + body + self.trailer).encode("ascii")


def listing_of(q, p):
    t = geom.twin_match(q, p)
    if t is None:
        raise ValueError("no listing")
    return t


def corners_in_listing(p, listing):
    e = geom.corners_of(p)
    o, sense = listing
    return tuple(e[(o + k) % 4] if sense == "ccw" else e[(o - k) % 4] for k in range(4))


# ------------------------------------------------------------------ the original


class Original:
    def __init__(self, kind: str, raws: dict):
        self.kind = kind
        self.raws = raws
        if kind == "report":
            res = chk.check_report(raws["J"], raws["C"])
            self.fj = rd.read_form_j(raws["J"])
            self.fc = rd.read_corners(raws["C"], "square-k", "form C")
            self.poses = self.fj["rows"]
            self.corners = self.fc["squares"]
            self.side = self.fj["side"]
            self.side_text = self.fj["side_text"]
            self.n = self.fj["n"]
            self.layout = CornersLayout(raws["C"], self.n, "square-k")
        else:
            res = chk.check_house(raws["H"])
            fh = rd.read_corners(raws["H"], "int", "house file")
            self.fc = fh
            self.corners = fh["squares"]
            self.poses = [geom.pose_of_corners(q)[1] for q in self.corners]
            self.side = fh["side"]
            self.side_text = fh["side_text"]
            self.n = fh["n"]
            self.layout = CornersLayout(raws["H"], self.n, "int")
        if res["verdict"] != "ACCEPT":
            raise SystemExit(f"the original is not accepted: {res.get('reason')}")
        self.result = res
        d = res["_decisions"][0]
        self.margins = d["a"]["margins"]
        self.clear = d["a"]["clearances"]
        self.listing = [listing_of(q, p) for q, p in zip(self.corners, self.poses, strict=True)]
        self.pairs = geom.pair_index(self.n)
        self.hsum = [half_sum(self.poses[i], self.poses[j]) for i, j in self.pairs]
        self.contr = con.contraction(self.poses, self.side)
        self.W = min(min(c[2], c[3]) for c in self.clear)

    def check(self, poses=None, corners=None, side=None, raw_j=None, raw_c=None):
        """Decide a changed packing written as file bytes; returns the check result."""
        side = self.side if side is None else side
        side_text = frac_text(side)
        if self.kind == "report":
            if raw_j is None:
                raw_j = write_form_j(self.n, side_text, rows_text(poses))
            if raw_c is None:
                if corners is None:
                    corners = [corners_in_listing(p, lst) for p, lst in zip(poses, self.listing, strict=True)]
                raw_c = self.layout.write(side_text, corners)
            return chk.check_report(raw_j, raw_c)
        if raw_c is None:
            if corners is None:
                corners = [corners_in_listing(p, lst) for p, lst in zip(poses, self.listing, strict=True)]
            raw_c = self.layout.write(side_text, corners)
        return chk.check_house(raw_c)


def half_sum(pi, pj) -> Fraction:
    """H = 1/2 + (|cos D| + |sin D|)/2, from the two directions (an independent formula)."""
    _x, _y, ci, si = pi
    _x, _y, cj, sj = pj
    return Fraction(1, 2) + (abs(ci * cj + si * sj) + abs(ci * sj - si * cj)) / 2


def decisions(res):
    return list(res.get("_decisions", ()))


def a_margins(res):
    return [d["a"]["margins"] for d in decisions(res)]


def a_clear(res):
    return [d["a"]["clearances"] for d in decisions(res)]


def verdict(res) -> str:
    return res["verdict"]


# ------------------------------------------------------------------ controls


def reader_controls(o: Original, plan_ids) -> list:
    out = []
    if o.kind == "report":
        rj = o.raws["J"]
        text_j = rj.decode("ascii")
        cut = text_j.index('"squares"')
        head_j, tail_j = text_j[:cut], text_j[cut:]

        def in_squares(a: str, b: str) -> bytes:
            """Replace the first a by b inside the squares block only."""
            return (head_j + tail_j.replace(a, b, 1)).encode()

        tj = text_j
        first_j = o.fj["rows"][0][0]
        first_j_text = frac_text(first_j)
        row_tok = f'"{first_j_text}"'

        def refused_j(raw):
            try:
                rd.read_form_j(raw)
            except rd.ReadError as exc:
                return True, str(exc)
            return False, ""

        def twin_fail(raw_j, raw_c):
            fj = rd.read_form_j(raw_j)
            fc = rd.read_corners(raw_c, "square-k", "form C")
            return [k + 1 for k in range(fj["n"]) if geom.twin_match(fc["squares"][k], fj["rows"][k]) is None]

        p, q = o.side.numerator, o.side.denominator
        cases = {
            "RJ1": write_form_j(o.n, o.side_text, rows_text(o.poses[:-1])),
            "RJ4": write_form_j(o.n, floor_places(o.side, 40), rows_text(o.poses)),
            "RJ5": in_squares(row_tok, f'"+{first_j_text}"') if not first_j_text.startswith("-") else None,
            "RJ6": in_squares(row_tok, "1"),
            "RJ7": tj.replace(f'"n": {o.n},', f'"n": {o.n},\n "n": {o.n},', 1).encode(),
            "RJ8": tj.replace(rd.FORMAT_SENTENCE, rd.FORMAT_SENTENCE.replace("edge", "edgf"), 1).encode(),
            "RJ9": in_squares(row_tok, '"-0"'),
            "RJ10": in_squares(row_tok, f'"0{first_j_text.lstrip("-")}"'),
        }
        for cid, raw in cases.items():
            if cid not in plan_ids:
                continue
            ok, why = refused_j(raw) if raw is not None else (False, "not applicable")
            out.append({"id": cid, "as_stated": ok, "stated_verdict": "REFUSE", "observed": why[:160]})
        if "RJ2" in plan_ids:
            raw = write_form_j(o.n, f"{2 * p}/{2 * q}", rows_text(o.poses))
            fj = rd.read_form_j(raw)
            ok = fj["side"] == o.side and [f for f in fj["flags"] if f not in o.fj["flags"]] == [["side", "not-lowest-terms"]]
            out.append({"id": "RJ2", "as_stated": ok, "stated_verdict": "ACCEPT", "observed": fj["flags"][:4]})
        if "RJ3" in plan_ids:
            rows = list(o.poses)
            rows[0], rows[1] = rows[1], rows[0]
            fails = twin_fail(write_form_j(o.n, o.side_text, rows_text(rows)), o.raws["C"])
            out.append({"id": "RJ3", "as_stated": fails == [1, 2], "stated_verdict": "ACCEPT", "observed": fails[:10]})
        if "X1" in plan_ids:
            rows = [(x, y, c, -s) for x, y, c, s in o.poses]
            fails = twin_fail(write_form_j(o.n, o.side_text, rows_text(rows)), o.raws["C"])
            turned = [k + 1 for k, p_ in enumerate(o.poses) if p_[2] != 0 and p_[3] != 0]
            out.append({"id": "X1", "as_stated": fails == turned, "stated_verdict": "ACCEPT",
                        "observed": {"twin_fails": len(fails), "not_upright": len(turned)}})
    # the corners file (form C or the house file)
    key = "C" if o.kind == "report" else "H"
    id_style = "square-k" if o.kind == "report" else "int"
    rc = o.raws[key]
    tc = rc.decode("ascii")
    first = frac_text(o.corners[0][0][0])
    line = f"    - - {first}\n"
    ident1 = "square-1" if id_style == "square-k" else "1"
    ident2 = "square-2" if id_style == "square-k" else "2"

    def refused_c(raw):
        try:
            rd.read_corners(raw, id_style, "corners file")
        except rd.ReadError as exc:
            return True, str(exc)
        return False, ""

    p, q = o.side.numerator, o.side.denominator
    cases = {
        "RC1": o.layout.write(o.side_text, o.corners[:-1]),
        "RC4": o.layout.write(floor_places(o.side, 40), o.corners),
        "RC5": tc.replace(line, f"    - - +{first}\n", 1).encode() if not first.startswith("-") else None,
        "RC6": tc.replace(line, f'    - - "{first}"\n', 1).encode(),
        "RC7": tc.replace(f"  n: {o.n}\n", f"  n: {o.n}\n  n: {o.n}\n", 1).encode(),
        "RC8": tc.replace(f"  n: {o.n}\n", f"  n: &a {o.n}\n", 1).encode(),
        "RC9": tc.replace(f"  n: {o.n}\n", f"  n:\t{o.n}\n", 1).encode(),
        "RC10": tc.replace(f"  - id: {ident1}\n", "  - id: XX\n", 1).replace(f"  - id: {ident2}\n", f"  - id: {ident1}\n", 1)
        .replace("  - id: XX\n", f"  - id: {ident2}\n", 1).encode(),
        "RC11": tc.replace(line, "    - - -0\n", 1).encode(),
        "RC12": tc.replace(line, f"    - - 0{first.lstrip('-')}\n", 1).encode(),
    }
    for cid, raw in cases.items():
        if cid not in plan_ids:
            continue
        ok, why = refused_c(raw) if raw is not None else (False, "not applicable")
        out.append({"id": cid, "as_stated": ok, "stated_verdict": "REFUSE", "observed": why[:160]})
    if "RC2" in plan_ids:
        raw = o.layout.write(f"{2 * p}/{2 * q}", o.corners)
        fc = rd.read_corners(raw, id_style, "corners file")
        ok = fc["side"] == o.side and [f for f in fc["flags"] if f not in o.fc["flags"]] == [["side", "not-lowest-terms"]]
        out.append({"id": "RC2", "as_stated": ok, "stated_verdict": "ACCEPT", "observed": fc["flags"][:4]})
    if "RC3" in plan_ids and o.kind == "report":
        sq = list(o.corners)
        sq[0], sq[1] = sq[1], sq[0]
        raw = o.layout.write(o.side_text, sq)
        fc = rd.read_corners(raw, "square-k", "form C")
        fails = [k + 1 for k in range(o.n) if geom.twin_match(fc["squares"][k], o.poses[k]) is None]
        out.append({"id": "RC3", "as_stated": fails == [1, 2], "stated_verdict": "ACCEPT", "observed": fails[:10]})
    return out


def geometry_controls(o: Original, plan_ids) -> list:
    out = []
    n, S = o.n, o.side
    m0 = o.margins
    cl0 = o.clear
    idx = {pr: k for k, pr in enumerate(o.pairs)}

    def rec(cid, res, ok, stated, facts):
        out.append({"id": cid, "as_stated": bool(ok), "stated_verdict": stated, "verdict": verdict(res), "facts": facts,
                    "cpu": res.get("cpu_total")})

    if "G1" in plan_ids:
        poses = list(o.poses)
        poses[-1] = poses[0]
        corners = list(o.corners)
        corners[-1] = corners[0]
        res = o.check(poses=poses, corners=corners)
        oks = []
        for d in decisions(res):
            ms = d["a"]["margins"]
            ov_a = d["a_overlap"]
            ov_b = d["b_overlap"]
            bp = d["b"]["pairs"][idx[(0, n - 1)]]
            same = all(ms[idx[(k, n - 1)]] == m0[idx[(0, k)]] for k in range(1, n - 1))
            oks.append(ov_a == [(0, n - 1)] and ov_b == [(0, n - 1)] and ms[idx[(0, n - 1)]] == -1
                       and bp[0] == bp[2] == "overlap" and bp[1] == bp[3] == 1 and same)
        rec("G1", res, verdict(res) == "REFUSE" and oks and all(oks), "REFUSE", {"per_decision": oks})
    if "G2" in plan_ids:
        p0 = o.poses[0]
        poses = [(p0[0] + S, p0[1], p0[2], p0[3])] + list(o.poses[1:])
        q0 = tuple((x + S, y) for x, y in o.corners[0])
        corners = [q0] + list(o.corners[1:])
        res = o.check(poses=poses, corners=corners)
        L, B, R, T = cl0[0]
        oks = []
        for d in decisions(res):
            c = d["a"]["clearances"][0]
            oks.append(c == (L + S, B, R - S, T) and d["b"]["inside_area"][0] == 0 and not d["a_overlap"] and not d["b_overlap"])
        rec("G2", res, verdict(res) == "REFUSE" and oks and all(oks), "REFUSE", {"per_decision": oks})
    if "G3" in plan_ids:
        q0 = list(o.corners[0])
        q0[0] = (q0[0][0] + EPS, q0[0][1])
        corners = [tuple(q0)] + list(o.corners[1:])
        side_text = frac_text(S)
        raw_c = o.layout.write(side_text, corners)
        if o.kind == "report":
            res = o.check(raw_j=o.raws["J"], raw_c=raw_c)
            dj, dc = decisions(res)
            facts = {"twin_fail": res["twin"]["fail"], "form_c_corner_sets_not_unit": res["form_c"]["corner_sets_not_unit"],
                     "form_c_b_not_unit": res["form_c"]["b_not_unit"], "form_j_accept": dj["accept"]}
            ok = (verdict(res) == "REFUSE" and res["twin"]["fail"] == [1] and res["form_c"]["corner_sets_not_unit"] == [1]
                  and res["form_c"]["b_not_unit"] == [1] and dj["accept"])
        else:
            res = o.check(raw_c=raw_c)
            facts = {"corner_sets_not_unit": res["house"]["corner_sets_not_unit"], "b_not_unit": res["house"]["b_not_unit"]}
            ok = verdict(res) == "REFUSE" and res["house"]["corner_sets_not_unit"] == [1] and res["house"]["b_not_unit"] == [1]
        rec("G3", res, ok, "REFUSE", facts)
    if "G4" in plan_ids:
        corners = [tuple(reversed(q)) for q in o.corners]
        raw_c = o.layout.write(frac_text(S), corners)
        res = o.check(raw_j=o.raws.get("J"), raw_c=raw_c) if o.kind == "report" else o.check(raw_c=raw_c)
        ms = a_margins(res)
        cls = a_clear(res)
        ok = verdict(res) == "ACCEPT" and all(m == m0 for m in ms) and all(c == cl0 for c in cls)
        facts = {}
        if o.kind == "report":
            flipped = all(geom.twin_match(tuple(reversed(q)), p)[1] != lst[1]
                          for q, p, lst in zip(o.corners, o.poses, o.listing, strict=True))
            ok = ok and flipped
            facts["sense_reversed_everywhere"] = flipped
        rec("G4", res, ok, "ACCEPT", facts)
    sym = {
        "G5": (lambda x, y, c, s: (y, x, s, c), lambda x, y: (y, x), lambda L, B, R, T: (B, L, T, R)),
        "G6": (lambda x, y, c, s: (S - y, x, -s, c), lambda x, y: (S - y, x), lambda L, B, R, T: (T, L, B, R)),
        "G7": (lambda x, y, c, s: (S - x, y, -c, s), lambda x, y: (S - x, y), lambda L, B, R, T: (R, B, L, T)),
    }
    for cid, (fp, fpt, fcl) in sym.items():
        if cid not in plan_ids:
            continue
        poses = [fp(*p) for p in o.poses]
        corners = [tuple(fpt(x, y) for x, y in q) for q in o.corners]
        res = o.check(poses=poses, corners=corners)
        ok = verdict(res) == "ACCEPT" and all(m == m0 for m in a_margins(res)) and all(
            c == [fcl(*c0) for c0 in cl0] for c in a_clear(res))
        rec(cid, res, ok, "ACCEPT", {})
    # the side rule
    c12 = Fraction(ceil_places(S, 12))
    deltas = {"S1a": EPS, "S1b": Fraction(1, S.denominator), "S1c": o.W, "S1d": o.W + EPS, "S1e": S - c12,
              "S1f": S - (c12 - Fraction(1, 10**12))}
    for cid, delta in deltas.items():
        if cid not in plan_ids:
            continue
        res = o.check(poses=list(o.poses), corners=list(o.corners), side=S - delta)
        pred = [(L, B, R - delta, T - delta) for L, B, R, T in cl0]
        stated = "ACCEPT" if delta <= o.W else "REFUSE"
        oks = []
        for d in decisions(res):
            cr_pred = sorted({k for k, c in enumerate(pred) if min(c) < 0})
            touch_pred = [[k for k, c in enumerate(pred) if c[w] == 0] for w in range(4)]
            touch_a = [[k for k, cl in enumerate(d["a_walls"]) if cl[w] == "touching"] for w in range(4)]
            touch_b = [[k for k, cl in enumerate(d["b_walls"]) if cl[w] == "touching"] for w in range(4)]
            oks.append(d["a"]["margins"] == m0 and d["a"]["clearances"] == pred and d["a_cross"] == cr_pred
                       and d["b_cross"] == cr_pred and touch_a == touch_pred and touch_b == touch_pred)
        rec(cid, res, verdict(res) == stated and oks and all(oks), stated,
            {"delta": sci(delta, 6), "W": sci(o.W, 6), "crossing": len(sorted({k for k, c in enumerate(pred) if min(c) < 0}))})
    # the extent
    lmin = min(c[0] for c in cl0)
    bmin = min(c[1] for c in cl0)
    e = [geom.half_extent(p) for p in o.poses]
    width = max(p[0] + h for p, h in zip(o.poses, e, strict=True)) - min(p[0] - h for p, h in zip(o.poses, e, strict=True))
    height = max(p[1] + h for p, h in zip(o.poses, e, strict=True)) - min(p[1] - h for p, h in zip(o.poses, e, strict=True))
    X = max(width, height)
    moved = [(x - lmin, y - bmin, c, s) for x, y, c, s in o.poses]
    moved_c = [tuple((x - lmin, y - bmin) for x, y in q) for q in o.corners]
    pred_e = [(L - lmin, B - bmin, R - (S - X - lmin), T - (S - X - bmin)) for L, B, R, T in cl0]
    if "E1c" in plan_ids:
        res = o.check(poses=moved, corners=moved_c, side=X)
        oks = []
        for d in decisions(res):
            touch_pred = [[k for k, c in enumerate(pred_e) if c[w] == 0] for w in range(4)]
            touch_a = [[k for k, cl in enumerate(d["a_walls"]) if cl[w] == "touching"] for w in range(4)]
            oks.append(d["a"]["margins"] == m0 and d["a"]["clearances"] == pred_e and touch_a == touch_pred)
        rec("E1c", res, verdict(res) == "ACCEPT" and oks and all(oks), "ACCEPT",
            {"extent": floor_places(X, 30), "side_less_extent": sci(S - X, 6)})
    if "E1p" in plan_ids:
        res = o.check(poses=moved, corners=moved_c, side=X - EPS)
        cr_pred = sorted({k for k, c in enumerate(pred_e) if min(c[2], c[3]) < EPS})
        oks = [d["a_cross"] == cr_pred and d["b_cross"] == cr_pred for d in decisions(res)]
        rec("E1p", res, verdict(res) == "REFUSE" and oks and all(oks), "REFUSE", {"crossing": len(cr_pred)})
    # the contraction
    lam = o.contr["lambda"]
    fac = o.contr["factors"]

    def scaled(lmb):
        ps = [(lmb * x, lmb * y, c, s) for x, y, c, s in o.poses]
        xl = min(p[0] - h for p, h in zip(ps, e, strict=True))
        yl = min(p[1] - h for p, h in zip(ps, e, strict=True))
        ps = [(x - xl, y - yl, c, s) for x, y, c, s in ps]
        ext = max(max(p[0] + h for p, h in zip(ps, e, strict=True)), max(p[1] + h for p, h in zip(ps, e, strict=True)))
        return ps, ext

    k_poses, k_side = scaled(lam)
    pred_k = [lam * (m + h) - h for m, h in zip(m0, o.hsum, strict=True)]
    binding = [o.pairs[k] for k, f in enumerate(fac) if Fraction(f[0], f[1]) == lam]
    if "K1c" in plan_ids:
        res = o.check(poses=k_poses, side=k_side)
        oks = []
        for d in decisions(res):
            touching = [o.pairs[k] for k, c in enumerate(d["a_classes"]) if c == "contact"]
            oks.append(d["a"]["margins"] == pred_k and touching == binding and k_side == o.contr["shrunk_side"])
        rec("K1c", res, verdict(res) == "ACCEPT" and oks and all(oks), "ACCEPT",
            {"binding": [[i + 1, j + 1] for i, j in binding][:12], "shrunk_side_30": floor_places(k_side, 30)})
    if "K1p" in plan_ids:
        lp = lam * (1 - EPS)
        p_poses, p_side = scaled(lp)
        res = o.check(poses=p_poses, side=p_side)
        pred_p = [lp * (m + h) - h for m, h in zip(m0, o.hsum, strict=True)]
        over_pred = [o.pairs[k] for k, f in enumerate(fac) if Fraction(f[0], f[1]) > lp]
        oks = [d["a"]["margins"] == pred_p and d["a_overlap"] == over_pred and d["b_overlap"] == over_pred for d in decisions(res)]
        rec("K1p", res, verdict(res) == "REFUSE" and oks and all(oks), "REFUSE", {"overlapping": len(over_pred)})
    if "K1s" in plan_ids:
        res = o.check(poses=k_poses, side=k_side - EPS)
        kc = [geom.clearances(p, k_side) for p in k_poses]
        cr_pred = sorted({k for k, c in enumerate(kc) if min(c[2], c[3]) < EPS})
        oks = [d["a"]["margins"] == pred_k and d["a_cross"] == cr_pred and d["b_cross"] == cr_pred for d in decisions(res)]
        rec("K1s", res, verdict(res) == "REFUSE" and oks and all(oks), "REFUSE", {"crossing": len(cr_pred)})
    return out


def pair_controls(o: Original, plan_ids) -> list:
    out = []
    if "PALL" in plan_ids:
        t0 = time.process_time()
        bad = []
        ints = [geom.int_pose(p) for p in o.poses]
        for k, (i, j) in enumerate(o.pairs):
            pi, pj = o.poses[i], o.poses[j]
            p, hn, den = geom.pair_terms(ints[i], ints[j])
            dx, dy = pj[0] - pi[0], pj[1] - pi[1]
            for t, want in ((Fraction(hn, 2 * p), Fraction(0)), (Fraction(hn - den * EPS, 2 * p), -EPS)):
                pj2 = (pi[0] + t * dx, pi[1] + t * dy, pj[2], pj[3])
                ma = geom.margin(geom.int_pose(pi), geom.int_pose(pj2))
                c1, a1, c2, a2 = clipmod.decide_pair(geom.corners_of(pi), geom.corners_of(pj2))
                if want == 0:
                    good = ma == 0 and c1 == c2 == "contact"
                else:
                    good = ma == want and c1 == c2 == "overlap" and a1 == a2 and a1 > 0
                if not good:
                    bad.append([i + 1, j + 1, "contact" if want == 0 else "past"])
        out.append({"id": "PALL", "as_stated": not bad, "facts": {"closings": 2 * len(o.pairs), "not_as_stated": bad[:10]},
                    "cpu": round(time.process_time() - t0, 2)})
    if "WALL" in plan_ids:
        t0 = time.process_time()
        bad = []
        S = o.side
        for k, p in enumerate(o.poses):
            c = o.clear[k]
            w = min(range(4), key=lambda m: (c[m], m))
            for extra, want_a, want_b in ((Fraction(0), Fraction(0), "contact"), (EPS, -EPS, "overlap")):
                shift = c[w] + extra
                x, y = p[0], p[1]
                if w == 0:
                    x -= shift
                elif w == 1:
                    y -= shift
                elif w == 2:
                    x += shift
                else:
                    y += shift
                p2 = (x, y, p[2], p[3])
                ca = geom.clearances(p2, S)[w]
                bd = clipmod.decide_corners([geom.corners_of(p2)], S)
                area = bd["inside_area"][0]
                good = ca == want_a and bd["walls"][0][w] == want_b and (area == 1 if want_b == "contact" else area < 1)
                if not good:
                    bad.append([k + 1, w, "contact" if extra == 0 else "past"])
        out.append({"id": "WALL", "as_stated": not bad, "facts": {"moves": 2 * o.n, "not_as_stated": bad[:10]},
                    "cpu": round(time.process_time() - t0, 2)})
    if "C0" in plan_ids:
        t0 = time.process_time()
        mism = 0
        for k, (i, j) in enumerate(o.pairs):
            mc = clipmod.margin_from_corners(o.corners[i], o.corners[j])
            if mc != o.margins[k]:
                mism += 1
        cmis = 0
        for k, q in enumerate(o.corners):
            xs = [x for x, _y in q]
            ys = [y for _x, y in q]
            if (min(xs), min(ys), o.side - max(xs), o.side - max(ys)) != o.clear[k]:
                cmis += 1
        out.append({"id": "C0", "as_stated": mism == 0 and cmis == 0,
                    "facts": {"pairs": len(o.pairs), "margin_mismatches": mism, "squares": o.n, "clearance_mismatches": cmis},
                    "cpu": round(time.process_time() - t0, 2)})
    return out


def constant_checkers(results: list) -> dict:
    stated = [r for r in results if r.get("stated_verdict") in ("ACCEPT", "REFUSE")]
    acc_fails = [r["id"] for r in stated if r["stated_verdict"] == "REFUSE"]
    ref_fails = [r["id"] for r in stated if r["stated_verdict"] == "ACCEPT"]
    return {"id": "KC", "as_stated": bool(acc_fails) and bool(ref_fails),
            "facts": {"controls_with_a_stated_verdict": len(stated), "constant_ACCEPT_fails": len(acc_fails),
                      "constant_REFUSE_fails": len(ref_fails), "constant_ACCEPT_fails_ids": acc_fails,
                      "constant_REFUSE_fails_ids": ref_fails}}


def main(argv: list[str]) -> int:
    if len(argv) == 5 and argv[0] == "report":
        _, label, pj, pc, out = argv
        raws = {"J": open(pj, "rb").read(), "C": open(pc, "rb").read()}
        kind = "report"
    elif len(argv) == 4 and argv[0] == "house":
        _, label, ph, out = argv
        raws = {"H": open(ph, "rb").read()}
        kind = "house"
    else:
        print(__doc__)
        return 2
    t_all = time.process_time()
    plan = json.load(open(PLAN))
    plan_ids = {c["id"] for c in plan["controls"] if kind in c["applies"]}
    o = Original(kind, raws)
    results = reader_controls(o, plan_ids)
    results += geometry_controls(o, plan_ids)
    results += pair_controls(o, plan_ids)
    if "KC" in plan_ids:
        results.append(constant_checkers(results))
    ran = {r["id"] for r in results}
    missing = sorted(plan_ids - ran)
    summary = {"label": label, "kind": kind, "planned": len(plan_ids), "ran": len(results),
               "as_stated": sum(1 for r in results if r["as_stated"]),
               "not_as_stated": [r["id"] for r in results if not r["as_stated"]], "not_run": missing,
               "cpu_total": round(time.process_time() - t_all, 1)}
    with open(out, "w") as f:
        json.dump({"summary": summary, "controls": results}, f, indent=1)
        f.write("\n")
    print(json.dumps(summary))
    return 0 if not summary["not_as_stated"] and not missing else 1


if __name__ == "__main__":
    _sys.exit(main(_sys.argv[1:]))
