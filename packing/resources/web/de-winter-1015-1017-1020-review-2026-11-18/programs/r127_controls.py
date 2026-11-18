"""Run the controls of programs/controls-plan.json on one certificate file.

Lane r127-1118.  Written for this review; imports only its own modules.

    python -I -B r127_controls.py FILE --tier first|twin --twin OTHER --claim DECIMAL
        [--checker real|always-accept|always-refuse] --out OUT.json

Every control writes a modified packing in the file's own form (or a modified text),
reads it back through the strict reader, decides it, and compares the result with the
outcome the plan states as a rule over the original's exact facts (method A's margins
and clearances, and the closed form of r127_frame), computed here before the modified
packing is decided.  Whole-packing controls are decided afresh by both methods; a
control that changes some squares or only the side re-decides what the change can
reach (r127_decide.decide_patch) and checks that the changed squares are exactly the
intended ones.  Pair-level controls (PALL) and square-level controls (WALL) decide the
moved pair or square by both methods.

With --checker always-accept or always-refuse, the decision is replaced by that
constant verdict (a reader refusal becomes the same constant), and each control is
judged on its verdict alone: the run shows which stated controls a checker that cannot
refuse, or cannot accept, would fail.  Such a run decides nothing about the file.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I drops the script dir

import argparse
import hashlib
import json
import time
from fractions import Fraction

import r127_area as B
import r127_axes as A
import r127_check as CK
import r127_decide as D
import r127_frame as F
import r127_read as R
import r127_twin as TW

DELTA = Fraction(1, 10**30)
WALLS = D.WALLS


class Ctx:
    def __init__(self, path: str, checker: str):
        self.path = path
        self.text = R.read_bytes(path).decode("utf-8")
        self.p = R.read_path(path)
        self.form = self.p.form
        self.n = self.p.n
        self.S = self.p.side
        self.d0 = D.decide_full(self.p)
        self.s0 = D.summarize(self.d0)
        self.cs, self.us = F.frames(self.p)
        self.checker = checker
        self.results: list[dict] = []

    # ------------------------------------------------------------- writing packings
    def emit(self, side, centres=None, dirs=None, corners=None) -> str:
        if self.form == "centre":
            return R.write_centre(self.n if centres is None else len(centres), side,
                                  centres if centres is not None else self.cs,
                                  dirs if dirs is not None else self.us)
        cs = corners if corners is not None else self.p.corners
        return R.write_witness(len(cs), side, cs, ids=None)

    def translated(self, i, t):
        """(centres, dirs, corners) with square i translated by t."""
        cs, us, cr = list(self.cs), list(self.us), [list(c) for c in self.p.corners]
        cs[i] = (cs[i][0] + t[0], cs[i][1] + t[1])
        cr[i] = [(x + t[0], y + t[1]) for x, y in cr[i]]
        return cs, us, cr

    def read_text(self, text):
        return R.read_centre(text) if self.form == "centre" else R.read_witness(text)

    # ------------------------------------------------------------- deciding
    def judge(self, text, changed=None, full=False):
        """Return (verdict, packing, decision, summary); verdict READER_REFUSES when the
        reader refuses.  A constant checker returns its constant."""
        if self.checker != "real":
            v = "ACCEPT" if self.checker == "always-accept" else "REFUSE"
            return v, None, None, None
        try:
            q = self.read_text(text)
        except R.ReadError as exc:
            return "READER_REFUSES", str(exc), None, None
        if full or q.n != self.n:
            d = D.decide_full(q)
        else:
            actual = [k for k in range(self.n) if q.corners[k] != self.p.corners[k]]
            if changed is not None and sorted(actual) != sorted(changed):
                return "CHANGED_SET_MISMATCH", q, None, {"actual": actual, "intended": changed}
            d = D.decide_patch(self.d0, q, actual)
        s = D.summarize(d)
        return s["verdict"], q, d, s

    def record(self, cid, stated, verdict_expected, verdict, ok, details=None):
        if self.checker != "real":
            ok = verdict == verdict_expected or (verdict_expected == "READ" and verdict == "ACCEPT")
            if verdict_expected == "READER_REFUSES":
                ok = verdict == "REFUSE"
        self.results.append({"id": cid, "stated": stated, "expected_verdict": verdict_expected,
                             "verdict": verdict, "as_stated": bool(ok), "details": details or {}})


# ---------------------------------------------------------------- reader controls

def reader_controls(c: Ctx):
    t = c.text
    S = c.S
    fs = D.fs
    muts = {}
    if c.form == "centre":
        obj = json.loads(t)
        o1 = dict(obj)
        o1["squares"] = obj["squares"][:-1]
        muts["R1"] = json.dumps(o1, indent=1)
        side2 = f"{2 * S.numerator}/{2 * S.denominator}"
        muts["R2"] = t.replace(f'"side": "{fs(S)}"', f'"side": "{side2}"', 1)
        first_row_end = t.index("]", t.index('"squares"') + 15)
        muts["R3"] = t[:first_row_end].rstrip() + ',\n   "0"\n  ' + t[first_row_end:]
        muts["R4"] = t.replace(f'"side": "{fs(S)}"', '"side": 11.8', 1)
        k = t.index('"', t.index("[", t.index('"squares"')) + 1)
        muts["R5"] = t[:k + 1] + "+" + t[k + 1:]
        muts["R6"] = t.replace('"n": ', f'"side": "{fs(S + 1)}",\n "n": ', 1)
        muts["R7"] = t.replace("(cos, sin) is the unit", "(sin, cos) is the unit", 1)
    else:
        lines = t.split("\n")
        last = max(i for i, ln in enumerate(lines) if ln.startswith("  - id: "))
        end = last + 1
        while end < len(lines) and (lines[end].startswith("    ") or lines[end].startswith("      ")):
            end += 1
        muts["R1"] = "\n".join(lines[:last] + lines[end:])
        side2 = f"{2 * S.numerator}/{2 * S.denominator}"
        side_line = [ln for ln in lines if ln.startswith("  side: ")][0]
        muts["R2"] = t.replace(side_line, f"  side: {side2}", 1)
        ids = [i for i, ln in enumerate(lines) if ln.startswith("  - id: ")]
        l2 = list(lines)
        l2[ids[1]] = lines[ids[0]]
        muts["R3"] = "\n".join(l2)
        muts["R4"] = t.replace(side_line, "  side: 11.8", 1)
        first = next(i for i, ln in enumerate(lines) if ln.startswith("    - - "))
        l5 = list(lines)
        val = l5[first][len("    - - "):]
        l5[first] = "    - - " + ("'+" + val[1:] if val.startswith("'") else "+" + val)
        muts["R5"] = "\n".join(l5)
        n_line = [ln for ln in lines if ln.startswith("  n: ")][0]
        muts["R6"] = t.replace(n_line, n_line + f"\n  side: {fs(S + 1)}", 1)
        muts["R7"] = t.replace("origin: lower-left", "origin: container-center", 1)
    for cid in ("R1", "R3", "R4", "R5", "R6", "R7"):
        changed = muts[cid] != t
        v, why, _, _ = c.judge(muts[cid], full=True)
        c.record(cid, "the reader refuses", "READER_REFUSES", v,
                 changed and v == "READER_REFUSES", {"text_changed": changed, "reason": why if isinstance(why, str) else None})
    # R2: read, equal values, only the side flagged
    if c.checker == "real":
        try:
            q = c.read_text(muts["R2"])
            ok = (q.side == S and q.corners == c.p.corners and q.not_lowest == ["side"] + c.p.not_lowest)
            c.record("R2", "read; values equal; only the side flagged out of lowest terms", "READ",
                     "READ", ok and muts["R2"] != t, {"flags": q.not_lowest[:3]})
        except R.ReadError as exc:
            c.record("R2", "read; values equal; only the side flagged", "READ", "READER_REFUSES", False,
                     {"reason": str(exc)})
    else:
        v, *_ = c.judge(muts["R2"])
        c.record("R2", "read; values equal; only the side flagged", "READ", v, False)


# ---------------------------------------------------------------- geometry controls

def side_rule(c: Ctx, cid, stated, delta, expect=None):
    """The side lowered by delta (raised if negative): L and B unchanged, R and T lowered
    by exactly delta, margins unchanged, crossings exactly the new negative clearances."""
    newS = c.S - delta
    text = c.emit(newS)
    want_cross = sorted((i + 1, WALLS[k]) for i in range(c.n) for k in (2, 3)
                        if c.d0.clearA[i][k] - delta < 0)
    want = "REFUSE" if want_cross else "ACCEPT"
    if expect is not None and expect != want:
        want = "CONTRADICTS_PLAN"
    v, q, d, s = c.judge(text, changed=[])
    ok = False
    details = {"delta": D.sci(delta), "crossings_expected": len(want_cross)}
    if d is not None:
        clear_ok = all(d.clearA[i][0] == c.d0.clearA[i][0] and d.clearA[i][1] == c.d0.clearA[i][1]
                       and d.clearA[i][2] == c.d0.clearA[i][2] - delta
                       and d.clearA[i][3] == c.d0.clearA[i][3] - delta for i in range(c.n))
        got_cross = sorted((i + 1, WALLS[k]) for i in range(c.n) for k in (2, 3)
                           if d.wallB[i][k] == "cross" and d.clearA[i][k] < 0)
        ok = (v == want and clear_ok and got_cross == want_cross and d.mA == c.d0.mA)
        details.update({"crossing_squares": got_cross[:12]})
    c.record(cid, stated, want if want != "CONTRADICTS_PLAN" else (expect or want), v, ok, details)


def transform_control(c: Ctx, cid, stated, fx, fu, perm):
    """A rigid symmetry of the box: margins identical, clearances permuted by perm."""
    cs = [fx(x, y) for x, y in c.cs]
    us = [fu(a, b) for a, b in c.us]
    cr = [[fx(x, y) for x, y in pts] for pts in c.p.corners]
    text = c.emit(c.S, cs, us, cr)
    v, q, d, s = c.judge(text, full=True)
    ok = False
    if d is not None:
        ok = (v == c.s0["verdict"] and d.mA == c.d0.mA
              and all(tuple(d.clearA[i]) == tuple(c.d0.clearA[i][k] for k in perm) for i in range(c.n)))
    c.record(cid, stated, c.s0["verdict"], v, ok)


def g_controls(c: Ctx):
    n, S = c.n, c.S
    # G1: square n given square 1's pose
    cs, us, cr = list(c.cs), list(c.us), [list(x) for x in c.p.corners]
    cs[n - 1], us[n - 1], cr[n - 1] = cs[0], us[0], list(cr[0])
    v, q, d, s = c.judge(c.emit(S, cs, us, cr), changed=[n - 1])
    ok = False
    if d is not None:
        over = sorted(k for k, m in d.mA.items() if m < 0)
        want_over = sorted([(0, n - 1)] + [(k, n - 1) for k in range(1, n - 1) if c.d0.mA[(0, k)] < 0])
        same = all(d.mA[(k, n - 1)] == c.d0.mA[(0, k)] for k in range(1, n - 1))
        ok = (v == "REFUSE" and over == want_over and d.mA[(0, n - 1)] == -1
              and d.cB[(0, n - 1)] == ("overlap", 1) and same)
    c.record("G1", "refused: overlapping exactly (1, n) at margin -1, B area 1; each (k, n) at the original (1, k)",
             "REFUSE", v, ok)
    # G2: square 1 translated by (S, 0)
    cs, us, cr = c.translated(0, (S, Fraction(0)))
    v, q, d, s = c.judge(c.emit(S, cs, us, cr), changed=[0])
    ok = False
    if d is not None:
        over = [k for k, m in d.mA.items() if m < 0]
        ok = (v == "REFUSE" and not over and d.clearA[0][2] == c.d0.clearA[0][2] - S
              and d.wallB[0][2] == "cross" and d.insideB[0] == 0
              and all(d.wallB[i][k] != "cross" for i in range(1, n) for k in range(4)))
    c.record("G2", "refused: the only crossing square 1 at the right wall, at R1 - S exactly; its area inside 0; no overlapping pair",
             "REFUSE", v, ok)
    # G3: square 1 off unit by 1e-30
    if c.form == "centre":
        us2 = list(c.us)
        us2[0] = (us2[0][0] + DELTA, us2[0][1])
        text = c.emit(S, c.cs, us2, None)
    else:
        cr = [list(x) for x in c.p.corners]
        cr[0][0] = (cr[0][0][0] + DELTA, cr[0][0][1])
        text = c.emit(S, None, None, cr)
    v, q, d, s = c.judge(text, changed=[0])
    ok = False
    if d is not None:
        ok = (v == "REFUSE" and not d.unitA[0] and not d.unitB[0] and all(d.unitA[1:]) and all(d.unitB[1:]))
    c.record("G3", "refused: square 1, and only square 1, not a unit square by A and by B", "REFUSE", v, ok)


def g_full_controls(c: Ctx):
    S = c.S
    transform_control(c, "G6", "transposed: the original's verdict; margins identical; clearances (L,B,R,T) -> (B,L,T,R)",
                      lambda x, y: (y, x), lambda a, b: (b, a), (1, 0, 3, 2))
    transform_control(c, "G7", "a quarter turn about the box centre: the original's verdict; margins identical; (L,B,R,T) -> (T,L,B,R)",
                      lambda x, y: (S - y, x), lambda a, b: (-b, a), (3, 0, 1, 2))
    transform_control(c, "G8", "mirrored x -> S - x: the original's verdict; margins identical; (L,B,R,T) -> (R,B,L,T)",
                      lambda x, y: (S - x, y), lambda a, b: (-a, b), (2, 1, 0, 3))
    # G9: every centre multiplied by 99/100 in the same box
    f = Fraction(99, 100)
    cs = [(f * x, f * y) for x, y in c.cs]
    cr = [[(x + (f - 1) * cc[0], y + (f - 1) * cc[1]) for x, y in pts] for pts, cc in zip(c.p.corners, c.cs, strict=True)]
    want_over = []
    cf = {}
    for (i, j) in c.d0.mA:
        dd = (c.cs[j][0] - c.cs[i][0], c.cs[j][1] - c.cs[i][1])
        m = f * F.M_of(c.us[i], c.us[j], dd) - F.T_of(c.us[i], c.us[j])
        cf[(i, j)] = m
        if m < 0:
            want_over.append((i, j))
    v, q, d, s = c.judge(c.emit(S, cs, c.us, cr), full=True)
    ok = False
    want = "REFUSE" if want_over else "ACCEPT"
    if d is not None:
        over = sorted(k for k, m in d.mA.items() if m < 0)
        ok = v == want and over == sorted(want_over) and all(d.mA[k] == cf[k] for k in cf)
    c.record("G9", "every centre times 99/100: margins equal the closed form's f M - T; overlapping exactly the pairs with T/M > 99/100",
             want, v, ok, {"overlapping_expected": len(want_over)})


def s_controls(c: Ctx, claim: Fraction):
    S = c.S
    W = min(min(cl[2], cl[3]) for cl in c.d0.clearA)
    side_rule(c, "S0", "the side lowered by 1: the side rule", Fraction(1), "REFUSE")
    side_rule(c, "S1a", "the side lowered by 1e-30: the side rule", DELTA)
    side_rule(c, "S1b", "the side lowered by 1/q, q the side's denominator: the side rule", Fraction(1, S.denominator))
    side_rule(c, "S1c", "the side lowered by W, the least right or top clearance: the side rule; accepted", W, "ACCEPT")
    side_rule(c, "S1d", "the side lowered by W + 1e-30: the side rule; refused", W + DELTA, "REFUSE")
    side_rule(c, "S1e", "the side set to the claim: the side rule with delta = S - C", S - claim)
    side_rule(c, "S1f", "the side set to the claim less 1e-12: the side rule", S - claim + Fraction(1, 10**12))
    return W


def s2_controls(c: Ctx):
    x0 = min(cl[0] for cl in c.d0.clearA)
    y0 = min(cl[1] for cl in c.d0.clearA)
    xs = max(c.S - cl[2] for cl in c.d0.clearA) - x0
    ys = max(c.S - cl[3] for cl in c.d0.clearA) - y0
    E = max(xs, ys)
    for cid, side, want in (("S2c", E, "ACCEPT"), ("S2p", E - DELTA, "REFUSE")):
        cs = [(x - x0, y - y0) for x, y in c.cs]
        cr = [[(x - x0, y - y0) for x, y in pts] for pts in c.p.corners]
        v, q, d, s = c.judge(c.emit(side, cs, c.us, cr), full=(x0 != 0 or y0 != 0))
        ok = False
        if d is not None:
            ok = v == want and d.mA == c.d0.mA
        c.record(cid, f"moved to the corner, the side set to the larger extent{' less 1e-30' if cid == 'S2p' else ''}: {want}; margins identical",
                 want, v, ok, {"moved": [D.sci(x0), D.sci(y0)], "extent": D.sci(E)})


def eligible_move(c: Ctx, j, ell, exclude):
    """Square j can move by at most ell (L1 bound) without touching anything but the pair."""
    for (a, b), m in c.d0.mA.items():
        if j in (a, b) and (a, b) != exclude and m <= ell:
            return False
    return all(cl > ell for cl in c.d0.clearA[j])


def p_controls(c: Ctx):
    touching = [k for k, m in c.d0.mA.items() if m == 0]
    if touching:
        i, j = touching[0]
        dd = (c.cs[j][0] - c.cs[i][0], c.cs[j][1] - c.cs[i][1])
        TT, M = F.T_of(c.us[i], c.us[j]), F.M_of(c.us[i], c.us[j], dd)
        tau = (-DELTA + TT) / M
        t = ((tau - 1) * dd[0], (tau - 1) * dd[1])
        cs, us, cr = c.translated(j, t)
        v, q, d, s = c.judge(c.emit(c.S, cs, us, cr), changed=[j])
        ok = d is not None and v == "REFUSE" and d.mA[(i, j)] == -DELTA
        c.record("P0p", "the first touching pair pushed 1e-30 past: refused, that pair at -1e-30", "REFUSE", v, ok)
    else:
        c.results.append({"id": "P0p", "stated": "the first touching pair pushed 1e-30 past", "verdict": "NO_SUBJECT",
                          "expected_verdict": "NO_SUBJECT", "as_stated": True, "details": {"touching_pairs": 0}})
    order = sorted((m, k) for k, m in c.d0.mA.items() if m > 0)
    chosen = None
    for m, (a, b) in order:
        for i, j in ((a, b), (b, a)):  # j is the square moved, toward i
            dd = (c.cs[j][0] - c.cs[i][0], c.cs[j][1] - c.cs[i][1])
            TT, M = F.T_of(c.us[i], c.us[j]), F.M_of(c.us[i], c.us[j], dd)
            tau = (-DELTA + TT) / M
            ell = (1 - tau) * (abs(dd[0]) + abs(dd[1]))
            if eligible_move(c, j, ell, (a, b)):
                chosen = (i, j, dd, TT, M)
                break
        if chosen is not None:
            break
    if chosen is None:
        c.results.append({"id": "P1", "stated": "the tightest eligible pair", "verdict": "NO_SUBJECT",
                          "expected_verdict": "NO_SUBJECT", "as_stated": False, "details": {}})
        return
    i, j, dd, TT, M = chosen
    key = (min(i, j), max(i, j))
    for cid, mstar, want in (("P1c", Fraction(0), "ACCEPT"), ("P1p", -DELTA, "REFUSE")):
        tau = (mstar + TT) / M
        t = ((tau - 1) * dd[0], (tau - 1) * dd[1])
        cs, us, cr = c.translated(j, t)
        v, q, d, s = c.judge(c.emit(c.S, cs, us, cr), changed=[j])
        ok = False
        if d is not None:
            over = sorted(k for k, m in d.mA.items() if m < 0)
            touch = sorted(k for k, m in d.mA.items() if m == 0)
            if mstar == 0:
                ok = (v == "ACCEPT" and d.mA[key] == 0 and d.cB[key][0] == "contact"
                      and touch == sorted(touching + [key]) and not over)
            else:
                ok = v == "REFUSE" and over == [key] and d.mA[key] == -DELTA and d.cB[key][0] == "overlap"
        c.record(cid, f"the tightest eligible pair closed along its centre line to {'exact contact' if mstar == 0 else '1e-30 past'}",
                 want, v, ok, {"pair": [key[0] + 1, key[1] + 1], "moved": j + 1, "margin": D.sci(c.d0.mA[key])})


def w_controls(c: Ctx):
    for k, wall in enumerate(WALLS):
        order = sorted((c.d0.clearA[i][k], i) for i in range(c.n))
        chosen = None
        for cl, i in order:
            # an axis move of cl + 1e-30 toward the wall changes every margin of the square
            # by at most that much and no other wall's clearance but the opposite one's
            if all(m > cl + DELTA for (a, b), m in c.d0.mA.items() if i in (a, b)):
                chosen = (cl, i)
                break
        if chosen is None:
            c.results.append({"id": f"W1-{wall}", "stated": "no eligible square", "verdict": "NO_SUBJECT",
                              "expected_verdict": "NO_SUBJECT", "as_stated": False, "details": {}})
            continue
        cl, i = chosen
        sign = {0: (-1, 0), 1: (0, -1), 2: (1, 0), 3: (0, 1)}[k]
        for cid, extra, want in ((f"W1c-{wall}", Fraction(0), "ACCEPT"), (f"W1p-{wall}", DELTA, "REFUSE")):
            mv = cl + extra
            cs, us, cr = c.translated(i, (sign[0] * mv, sign[1] * mv))
            v, q, d, s = c.judge(c.emit(c.S, cs, us, cr), changed=[i] if mv != 0 else [])
            ok = False
            if d is not None:
                opp = {0: 2, 1: 3, 2: 0, 3: 1}[k]
                crossing = [(a, kk) for a in range(c.n) for kk in range(4) if d.clearA[a][kk] < 0]
                ok = (v == want and d.clearA[i][k] == -extra and d.clearA[i][opp] == c.d0.clearA[i][opp] + mv
                      and (crossing == ([(i, k)] if extra else []))
                      and (d.wallB[i][k] == ("cross" if extra else "touch")))
            c.record(cid, f"square {i + 1}, nearest the {wall} wall, moved to it{' and 1e-30 further' if extra else ''}",
                     want, v, ok, {"square": i + 1, "clearance": D.sci(cl)})


def w2_controls(c: Ctx):
    for k, wall in enumerate(WALLS):
        least = min(cl[k] for cl in c.d0.clearA)
        sign = {0: (-1, 0), 1: (0, -1), 2: (1, 0), 3: (0, 1)}[k]
        for cid, extra, want in ((f"W2c-{wall}", Fraction(0), "ACCEPT"), (f"W2p-{wall}", DELTA, "REFUSE")):
            mv = least + extra
            t = (sign[0] * mv, sign[1] * mv)
            cs = [(x + t[0], y + t[1]) for x, y in c.cs]
            cr = [[(x + t[0], y + t[1]) for x, y in pts] for pts in c.p.corners]
            v, q, d, s = c.judge(c.emit(c.S, cs, c.us, cr), full=True)
            ok = False
            if d is not None:
                shift = {0: (-mv, 0, mv, 0), 1: (0, -mv, 0, mv), 2: (mv, 0, -mv, 0), 3: (0, mv, 0, -mv)}[k]
                want_cross = sorted(i for i in range(c.n) if c.d0.clearA[i][k] == least) if extra else []
                got_cross = sorted(i for i in range(c.n) if d.clearA[i][k] < 0)
                ok = (v == want and d.mA == c.d0.mA and got_cross == want_cross
                      and all(tuple(d.clearA[i]) == tuple(c.d0.clearA[i][kk] + shift[kk] for kk in range(4))
                              for i in range(c.n)))
            c.record(cid, f"the whole packing translated to the {wall} wall{' and 1e-30 further' if extra else ''}",
                     want, v, ok, {"move": D.sci(mv)})


def k_controls(c: Ctx):
    """K0: contracted by lambda* and boxed at L' (accepted, touching exactly the pairs
    with T/M = lambda*); K1: by lambda* - 1e-30 in the same box (refused, overlapping
    exactly the pairs with T/M > lambda* - 1e-30)."""
    lam_pair = {}
    for (i, j) in c.d0.mA:
        dd = (c.cs[j][0] - c.cs[i][0], c.cs[j][1] - c.cs[i][1])
        lam_pair[(i, j)] = F.T_of(c.us[i], c.us[j]) / F.M_of(c.us[i], c.us[j], dd)
    lam = max(lam_pair.values())
    ccs = [(lam * x, lam * y) for x, y in c.cs]
    x0, x1, y0, y1 = F.extents(ccs, c.us)
    Lp = max(x1 - x0, y1 - y0)
    for cid, f, want in (("K0", lam, "ACCEPT"), ("K1", lam - DELTA, "REFUSE")):
        cs = [(f * x - x0, f * y - y0) for x, y in c.cs]
        cr = [[(x + (f - 1) * cc[0] - x0, y + (f - 1) * cc[1] - y0) for x, y in pts]
              for pts, cc in zip(c.p.corners, c.cs, strict=True)]
        side = Lp
        v, q, d, s = c.judge(c.emit(side, cs, c.us, cr), full=True)
        ok = False
        if d is not None:
            touch = sorted(k for k, m in d.mA.items() if m == 0)
            over = sorted(k for k, m in d.mA.items() if m < 0)
            if cid == "K0":
                ok = v == "ACCEPT" and touch == sorted(k for k, lp in lam_pair.items() if lp == lam) and not over
            else:
                ok = v == "REFUSE" and over == sorted(k for k, lp in lam_pair.items() if lp > f)
        c.record(cid, "contracted by lambda* and boxed at L': accepted, touching exactly the binding pairs" if cid == "K0"
                 else "contracted by lambda* - 1e-30 in the box of side L': refused, overlapping exactly the pairs with T/M > lambda* - 1e-30",
                 want, v, ok, {"one_less_lambda": D.sci(1 - lam), "L_prime": D.sci(Lp)})


def pall(c: Ctx):
    if c.checker != "real":
        return
    bad = 0
    count = 0
    for (i, j) in c.d0.mA:
        dd = (c.cs[j][0] - c.cs[i][0], c.cs[j][1] - c.cs[i][1])
        TT, M = F.T_of(c.us[i], c.us[j]), F.M_of(c.us[i], c.us[j], dd)
        Pi = c.p.corners[i]
        for mstar in (Fraction(0), -DELTA):
            tau = (mstar + TT) / M
            t = ((tau - 1) * dd[0], (tau - 1) * dd[1])
            Pj = [(x + t[0], y + t[1]) for x, y in c.p.corners[j]]
            sa, sb = A.prepare(Pi), A.prepare(Pj)
            cj = (c.cs[j][0] + t[0], c.cs[j][1] + t[1])
            want = "contact" if mstar == 0 else "overlap"
            bi, bj = B.ccw(B.to_mpq(Pi)), B.ccw(B.to_mpq(Pj))
            ok = (A.margin(sa, sb) == mstar and A.margin(sb, sa) == mstar
                  and F.pair_margin(c.cs[i], c.us[i], cj, c.us[j]) == mstar
                  and B.pair_class(bi, bj)[0] == want and B.pair_class(bj, bi)[0] == want)
            count += 1
            bad += not ok
    c.results.append({"id": "PALL", "stated": "every pair closed along its centre line to exact contact and 1e-30 past: A both ways and the closed form exactly 0 and -1e-30; B contact and overlap both ways",
                      "expected_verdict": "PAIR-LEVEL", "verdict": "PAIR-LEVEL", "as_stated": bad == 0,
                      "details": {"closings": count, "not_as_stated": bad}})


def wall_all(c: Ctx):
    if c.checker != "real":
        return
    bad = 0
    count = 0
    Sq = B.mpq(c.S.numerator, c.S.denominator)
    for i in range(c.n):
        for k in range(4):
            cl = c.d0.clearA[i][k]
            sign = {0: (-1, 0), 1: (0, -1), 2: (1, 0), 3: (0, 1)}[k]
            for extra in (Fraction(0), DELTA):
                mv = cl + extra
                P = [(x + sign[0] * mv, y + sign[1] * mv) for x, y in c.p.corners[i]]
                ca = A.walls(A.prepare(P), c.S)[k]
                cls, inside = B.wall_classes(B.ccw(B.to_mpq(P)), Sq)
                ok = (ca == -extra and cls[k] == ("touch" if extra == 0 else "cross")
                      and ((inside == 1) == (extra == 0)))
                count += 1
                bad += not ok
    c.results.append({"id": "WALL", "stated": "every square moved to each wall and 1e-30 past: A clearance exactly 0 and -1e-30; B touch and cross; B area inside 1 and below 1",
                      "expected_verdict": "SQUARE-LEVEL", "verdict": "SQUARE-LEVEL", "as_stated": bad == 0,
                      "details": {"moves": count, "not_as_stated": bad}})


def c0(c: Ctx):
    if c.checker != "real":
        return
    bad = 0
    for (i, j), m in c.d0.mA.items():
        bad += F.pair_margin(c.cs[i], c.us[i], c.cs[j], c.us[j]) != m
    for i in range(c.n):
        bad += tuple(F.clearances(c.cs[i], c.us[i], c.S)) != tuple(c.d0.clearA[i])
    c.results.append({"id": "C0", "stated": "the closed form recomputes every margin and clearance equal to method A",
                      "expected_verdict": "EQUAL", "verdict": "EQUAL" if bad == 0 else "UNEQUAL",
                      "as_stated": bad == 0, "details": {"mismatches": bad}})


def t_controls(c: Ctx, twin_path):
    other = R.read_path(twin_path)
    if c.checker != "real":
        c.record("T0", "the report's other file: the same packing", "SAME_PACKING",
                 "SAME_PACKING" if c.checker == "always-accept" else "DIFFERENT", False)
        c.record("T1", "square 1 moved by (1e-30, 0), against the other file: different", "DIFFERENT",
                 "SAME_PACKING" if c.checker == "always-accept" else "DIFFERENT", False)
        return
    r0 = TW.compare(c.p, other)
    c.record("T0", "the report's other file: the same packing; n, the side and every square's corner set equal",
             "SAME_PACKING", r0["verdict"], r0["verdict"] == "SAME_PACKING", {"listing": r0["listing"]})
    cs, us, cr = c.translated(0, (DELTA, Fraction(0)))
    q = c.read_text(c.emit(c.S, cs, us, cr))
    r1 = TW.compare(q, other)
    c.record("T1", "square 1 moved by (1e-30, 0), against the other file: different, exactly square 1 unequal",
             "DIFFERENT", r1["verdict"], r1["verdict"] == "DIFFERENT" and r1["unequal_squares"] == [1])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--tier", choices=["first", "twin"], required=True)
    ap.add_argument("--twin", required=True)
    ap.add_argument("--claim", required=True)
    ap.add_argument("--checker", choices=["real", "always-accept", "always-refuse"], default="real")
    ap.add_argument("--plan", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "controls-plan.json"))
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    t0 = time.process_time()
    plan = json.load(open(a.plan))
    c = Ctx(a.file, a.checker)
    claim = CK.decimal_fraction(a.claim)
    reader_controls(c)
    g_controls(c)
    W = s_controls(c, claim)
    p_controls(c)
    w_controls(c)
    t_controls(c, a.twin)
    c0(c)
    if a.tier == "first":
        g_full_controls(c)
        s2_controls(c)
        w2_controls(c)
        k_controls(c)
        pall(c)
        wall_all(c)
    planned = {x["id"] for x in plan["controls"] if a.tier in x["tiers"]}
    ran = set()
    for r in c.results:
        base_id = r["id"].split("-")[0]
        ran.add(base_id)
    missing = sorted(planned - ran)
    unplanned = sorted(ran - planned)
    n_ok = sum(r["as_stated"] for r in c.results)
    verdict = ("EVERY_CONTROL_AS_STATED" if n_ok == len(c.results) and not missing and not unplanned
               else "SOME_CONTROL_NOT_AS_STATED")
    out = {"program": "r127_controls.py", "file": a.file,
           "sha256": hashlib.sha256(R.read_bytes(a.file)).hexdigest(),
           "plan_sha256": hashlib.sha256(open(a.plan, "rb").read()).hexdigest(),
           "tier": a.tier, "checker": a.checker, "original_verdict": c.s0["verdict"],
           "least_right_or_top_clearance_W": D.sci(W), "controls": len(c.results), "as_stated": n_ok,
           "not_as_stated": [r["id"] for r in c.results if not r["as_stated"]],
           "missing_from_run": missing, "unplanned": unplanned, "verdict": verdict,
           "results": c.results, "cpu_seconds": round(time.process_time() - t0, 1)}
    json.dump(out, open(a.out, "w"), indent=1, default=str)
    print(f"{a.file} [{a.tier}, {a.checker}]: {verdict} {n_ok}/{len(c.results)} "
          f"not_as_stated={out['not_as_stated'][:12]} missing={missing} cpu={out['cpu_seconds']}s")
    return 0 if verdict == "EVERY_CONTROL_AS_STATED" else 1


if __name__ == "__main__":
    sys.exit(main())
