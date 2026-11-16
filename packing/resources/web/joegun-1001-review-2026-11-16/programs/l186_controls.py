"""Lane L186: run the stated controls on one certificate.

Usage: python -I -B l186_controls.py CERT.yaml PLAN.json COUNT OUT.json

Every expected outcome is computed from the plan's rule and the original's
exact facts (method A's margins and clearances), then compared exactly with
what both methods decide on the modified packing. Whole-file controls write the
modified packing as Witness/v2 text and read it back through the reader first.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from fractions import Fraction
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l186_clip as mb  # noqa: E402
import l186_geom as geo  # noqa: E402
import l186_sat as ma  # noqa: E402
from l186_decide import WALLS, decide, decimal_text, ftext, sci  # noqa: E402
from l186_reader import (  # noqa: E402
    ReadError,
    Square,
    Witness,
    dump_witness_text,
    read_witness_file,
    read_witness_text,
)

Clear = list[str]


def pidx(n: int, i: int, j: int) -> int:
    return i * n - i * (i + 1) // 2 + (j - i - 1)


def written(w: Witness, side: Fraction, squares: list[Square]) -> dict[str, Any]:
    tmp = Witness(n=len(squares), side=side, side_text="", squares=squares, sha256="", witness_id=w.witness_id)
    back = read_witness_text(dump_witness_text(tmp))
    assert back.side == side and back.squares == squares
    return decide(back.side, back.squares, keep_lists=True)


def sgn(v: Fraction) -> int:
    return (v > 0) - (v < 0)


class Runner:
    def __init__(self, path: str, plan: dict[str, Any], count: str) -> None:
        self.path = path
        self.plan = plan
        self.cfg = plan["counts"][count]
        self.eps = Fraction(plan["eps"])
        self.w = read_witness_file(path)
        with open(path, encoding="utf-8") as fh:
            self.text = fh.read()
        self.n = self.w.n
        self.S = self.w.side
        self.sq = self.w.squares
        self.base = decide(self.S, self.sq, keep_lists=True)
        self.M0: list[str] = self.base["_margins"]
        self.C0: list[Clear] = self.base["_clearances"]
        self.M0f = [Fraction(m) for m in self.M0]
        self.C0f = [[Fraction(c) for c in row] for row in self.C0]
        self.results: list[dict[str, Any]] = []
        self.stated = {c["id"]: c for c in plan["controls"]}

    # ---------------------------------------------------------------- helpers
    def record(self, cid: str, ok: bool, observed: dict[str, Any], stated_id: str | None = None) -> None:
        c = self.stated.get(stated_id or cid, {})
        self.results.append(
            {
                "id": cid,
                "text": c.get("text", ""),
                "stated": c.get("expect", ""),
                "observed": observed,
                "outcome": "AS_STATED" if ok else "NOT_AS_STATED",
            }
        )
        print(cid, "AS_STATED" if ok else "NOT_AS_STATED", flush=True)

    def summary(self, r: dict[str, Any]) -> dict[str, Any]:
        return {
            "verdict": r["verdict"],
            "reasons": r["reasons"][:5],
            "disagreement_count": r["disagreement_count"],
            "wall_contacts": r["walls"]["contact_count"],
            "crossing": r["walls"]["crossing"][:10],
            "touching_pairs": len(r["pairs"]["touching"]),
            "overlapping": r["pairs"]["overlapping"][:5],
            "overlapping_count": r["pairs"]["overlapping_count"],
            "least_margin_sci": r["pairs"]["least_margin_sci"],
            "digests": r["digests"],
        }

    def margins_without(self, r: dict[str, Any], skip: int) -> bool:
        n = self.n
        mm = r["_margins"]
        for i in range(n):
            for j in range(i + 1, n):
                if i == skip or j == skip:
                    continue
                k = pidx(n, i, j)
                if mm[k] != self.M0[k]:
                    return False
        return True

    def classes_kept(self, r: dict[str, Any], m: int, except_pair: tuple[int, int] | None) -> bool:
        n = self.n
        mm = r["_margins"]
        for k in range(n):
            if k == m:
                continue
            i, j = min(k, m), max(k, m)
            if except_pair is not None and (i, j) == except_pair:
                continue
            idx = pidx(n, i, j)
            if sgn(Fraction(mm[idx])) != sgn(self.M0f[idx]):
                return False
        cl = [Fraction(c) for c in r["_clearances"][m]]
        return all(sgn(a) == sgn(b) for a, b in zip(cl, self.C0f[m], strict=True))

    def clear_others_same(self, r: dict[str, Any], m: int) -> bool:
        return all(r["_clearances"][k] == self.C0[k] for k in range(self.n) if k != m)

    # ---------------------------------------------------------------- C0
    def c0(self) -> None:
        n = self.n
        bad_m = bad_c = 0
        for i in range(n):
            for j in range(i + 1, n):
                if geo.margin(self.sq[i], self.sq[j]) != self.M0f[pidx(n, i, j)]:
                    bad_m += 1
            if list(geo.clearances(self.sq[i], self.S)) != self.C0f[i]:
                bad_c += 1
        self.record("C0", bad_m == 0 and bad_c == 0, {"pair_mismatches": bad_m, "square_clearance_mismatches": bad_c, "pairs": n * (n - 1) // 2})

    # ---------------------------------------------------------------- R
    def reader_refuses(self, text: str) -> tuple[bool, str]:
        try:
            read_witness_text(text)
            return False, "read"
        except ReadError as exc:
            return True, str(exc)[:200]

    def side_line(self) -> tuple[int, int]:
        a = self.text.index("\n  side: ") + 1
        b = self.text.index("\n", a)
        return a, b

    def r_controls(self) -> None:
        n = self.n
        t = self.text
        p1 = t.index(f"\n  - id: {n}\n")
        p2 = t.index("\n  claim:\n")
        ok, msg = self.reader_refuses(t[:p1] + t[p2:])
        self.record("R1", ok and "squares listed" in msg, {"reader": msg})
        a, b = self.side_line()
        num, den = self.S.numerator, self.S.denominator
        t2 = t[:a] + f"  side: {2 * num}/{2 * den}" + t[b:]
        try:
            w2 = read_witness_text(t2)
            ok2 = (
                t2 != t
                and w2.side == self.S
                and w2.squares == self.sq
                and set(w2.noncanonical) == set(self.w.noncanonical) | {"side"}
            )
            obs2: dict[str, Any] = {"reader": "read", "noncanonical": w2.noncanonical[:5]}
        except ReadError as exc:
            ok2, obs2 = False, {"reader": str(exc)}
        self.record("R2", ok2, obs2)
        t3 = t.replace("\n  - id: 1\n", "\n  - id: @@\n", 1).replace("\n  - id: 2\n", "\n  - id: 1\n", 1).replace("\n  - id: @@\n", "\n  - id: 2\n", 1)
        ok, msg = self.reader_refuses(t3)
        self.record("R3", t3 != t and ok and "id" in msg, {"reader": msg})
        t4 = t[:a] + f"  side: {decimal_text(self.S, 40)}" + t[b:]
        ok, msg = self.reader_refuses(t4)
        self.record("R4", ok, {"reader": msg})
        key = "\n  - id: 1\n    corners:\n    - - "
        q = t.index(key) + len(key)
        t5 = t[:q] + "+" + t[q:]
        ok, msg = self.reader_refuses(t5)
        self.record("R5", ok, {"reader": msg})

    # ---------------------------------------------------------------- G
    def g_controls(self) -> None:
        n, S, sq = self.n, self.S, self.sq
        base_v = self.base["verdict"]
        senses = self.base["senses"]
        # G1
        s1 = sq[:-1] + [sq[0]]
        r = written(self.w, S, s1)
        exp_m = []
        for i in range(n):
            for j in range(i + 1, n):
                if j == n - 1:
                    exp_m.append("-1" if i == 0 else self.M0[pidx(n, 0, i)])
                else:
                    exp_m.append(self.M0[pidx(n, i, j)])
        exp_c = self.C0[:-1] + [self.C0[0]]
        ok = (
            r["verdict"] == "REFUSE"
            and r["_margins"] == exp_m
            and r["_clearances"] == exp_c
            and r["pairs"]["overlapping_count"] == 1
            and r["pairs"]["overlapping"][0] == [1, n, "-1", "1"]
        )
        self.record("G1", ok, self.summary(r))
        # G2
        s2 = [geo.translate(sq[0], S, Fraction(0))] + sq[1:]
        r = written(self.w, S, s2)
        L, B, R, T = self.C0f[0]
        exp0 = [ftext(L + S), ftext(B), ftext(R - S), ftext(T)]
        no_overlap = all(Fraction(r["_margins"][pidx(n, 0, k)]) >= 0 for k in range(1, n))
        ok = (
            r["verdict"] == "REFUSE"
            and r["_clearances"][0] == exp0
            and self.clear_others_same(r, 0)
            and r["walls"]["crossing"] == [[1, "right", ftext(R - S)]]
            and (L < 0 or r["walls"]["not_contained_B"] == [1])
            and r["pairs"]["overlapping_count"] == 0
            and no_overlap
            and self.margins_without(r, 0)
        )
        self.record("G2", ok, self.summary(r))
        # G3
        p = list(sq[0])
        p[0] = (p[0][0] + self.eps, p[0][1])
        s3 = [(p[0], p[1], p[2], p[3])] + sq[1:]
        r = written(self.w, S, s3)
        ok = r["verdict"] == "REFUSE" and r["non_unit_A"] == [1] and r["non_unit_B"] == [1]
        self.record("G3", ok, {**self.summary(r), "non_unit_A": r["non_unit_A"], "non_unit_B": r["non_unit_B"]})

        def transformed(cid: str, f: Any, perm: list[int] | None, flip: bool) -> None:
            ss = [f(x) for x in sq]
            rr = written(self.w, S, ss)
            if perm is None:
                exp_cl = self.C0
            else:
                exp_cl = [[row[k] for k in perm] for row in self.C0]
            exp_s = (
                {"ccw": senses["cw"], "cw": senses["ccw"], "none": senses["none"]}
                if flip
                else senses
            )
            okk = (
                rr["verdict"] == base_v
                and rr["_margins"] == self.M0
                and rr["_clearances"] == exp_cl
                and rr["senses"] == exp_s
            )
            self.record(cid, okk, {**self.summary(rr), "senses": rr["senses"]})

        def rev(x: Square) -> Square:
            return (x[3], x[2], x[1], x[0])

        def cyc(x: Square) -> Square:
            return (x[1], x[2], x[3], x[0])

        def tr(x: Square) -> Square:
            p = [(b, a) for a, b in x]
            return (p[0], p[1], p[2], p[3])

        def qt(x: Square) -> Square:
            p = [(S - b, a) for a, b in x]
            return (p[0], p[1], p[2], p[3])

        def mi(x: Square) -> Square:
            p = [(S - a, b) for a, b in x]
            return (p[0], p[1], p[2], p[3])

        transformed("G4", rev, None, True)
        transformed("G5", cyc, None, False)
        transformed("G6", tr, [1, 0, 3, 2], True)
        transformed("G7", qt, [3, 0, 1, 2], False)
        transformed("G8", mi, [2, 1, 0, 3], True)

    # ---------------------------------------------------------------- S
    def side_rule(self, cid: str, delta: Fraction) -> dict[str, Any]:
        S2 = self.S - delta
        r = written(self.w, S2, self.sq)
        exp_cl: list[Clear] = []
        crossing: list[list[Any]] = []
        contacts: list[list[Any]] = []
        for i, row in enumerate(self.C0f):
            new = [row[0], row[1], row[2] - delta, row[3] - delta]
            exp_cl.append([ftext(v) for v in new])
            for wi, v in enumerate(new):
                if v < 0:
                    crossing.append([i + 1, WALLS[wi], ftext(v)])
                elif v == 0:
                    contacts.append([i + 1, WALLS[wi]])
        exp_v = "REFUSE" if crossing else self.base["verdict"]
        ok = (
            r["verdict"] == exp_v
            and r["_clearances"] == exp_cl
            and r["_margins"] == self.M0
            and r["walls"]["crossing"] == crossing
            and r["walls"]["contacts"] == contacts
        )
        obs = {
            **self.summary(r),
            "delta": ftext(delta),
            "delta_sci": sci(delta),
            "new_side_decimal_30": decimal_text(S2, 30),
            "expected_verdict": exp_v,
            "expected_crossings": len(crossing),
            "expected_contacts": len(contacts),
        }
        self.record(cid, ok, obs)
        return r

    def s_controls(self) -> dict[str, str]:
        eps = self.eps
        rt = [min(row[2], row[3]) for row in self.C0f]
        W = min(rt)
        claim = Fraction(self.cfg["claim"])
        self.side_rule("S1a", eps)
        self.side_rule("S1b", Fraction(1, self.S.denominator))
        self.side_rule("S1c", W)
        self.side_rule("S1d", W + eps)
        re_ = self.side_rule("S1e", self.S - claim)
        rf = self.side_rule("S1f", self.S - claim + Fraction(1, 10**12))
        return {"S1e": re_["verdict"], "S1f": rf["verdict"], "W": ftext(W), "W_sci": sci(W)}

    # ---------------------------------------------------------------- P1
    def choose_pair(self) -> tuple[int, int, int, int] | None:
        n = self.n
        order: list[tuple[Fraction, int, int]] = []
        for i in range(n):
            for j in range(i + 1, n):
                m = self.M0f[pidx(n, i, j)]
                if m > 0:
                    order.append((m, i, j))
        order.sort()
        for _, i, j in order:
            for moved, other in ((j, i), (i, j)):
                _, len2 = geo.close_pair(self.sq[other], self.sq[moved], -self.eps)
                good = True
                for k in range(n):
                    if k in (i, j):
                        continue
                    mk = self.M0f[pidx(n, min(k, moved), max(k, moved))]
                    if mk <= 0 or mk * mk <= len2:
                        good = False
                        break
                if good:
                    for c in self.C0f[moved]:
                        if c <= 0 or c * c <= len2:
                            good = False
                            break
                if good:
                    return i, j, moved, other
        return None

    def p_controls(self) -> None:
        pick = self.choose_pair()
        if pick is None:
            self.record("P1c", False, {"note": "no eligible pair"})
            self.record("P1p", False, {"note": "no eligible pair"})
            return
        i, j, moved, other = pick
        n = self.n
        info = {"pair": [i + 1, j + 1], "moved": moved + 1, "pair_margin_sci": sci(self.M0f[pidx(n, i, j)])}
        for cid, target in (("P1c", Fraction(0)), ("P1p", -self.eps)):
            new_sq, len2 = geo.close_pair(self.sq[other], self.sq[moved], target)
            ss = list(self.sq)
            ss[moved] = new_sq
            r = written(self.w, self.S, ss)
            m_pair = Fraction(r["_margins"][pidx(n, i, j)])
            base_ok = (
                m_pair == target
                and self.margins_without(r, moved)
                and self.classes_kept(r, moved, (i, j))
                and self.clear_others_same(r, moved)
            )
            if cid == "P1c":
                exp_touch = sorted(self.base["pairs"]["touching"] + [[i + 1, j + 1]])
                ok = base_ok and r["verdict"] == self.base["verdict"] and sorted(r["pairs"]["touching"]) == exp_touch
            else:
                ok = (
                    base_ok
                    and r["verdict"] == "REFUSE"
                    and r["pairs"]["overlapping_count"] == 1
                    and r["pairs"]["overlapping"][0][:3] == [i + 1, j + 1, ftext(-self.eps)]
                )
            move = sci(Fraction(len2))
            self.record(cid, ok, {**self.summary(r), **info, "move_squared_sci": move})

    # ---------------------------------------------------------------- W1
    def w_controls(self) -> None:
        n = self.n
        for wi, wall in enumerate(WALLS):
            order = sorted(range(n), key=lambda k: (self.C0f[k][wi], k))
            pick = None
            for m in order:
                c = self.C0f[m][wi]
                mv = c + self.eps
                good = True
                for k in range(n):
                    if k == m:
                        continue
                    mk = self.M0f[pidx(n, min(k, m), max(k, m))]
                    if mk <= 0 or mk <= mv:
                        good = False
                        break
                if good:
                    pick = m
                    break
            if pick is None:
                self.translate_rule(wi, wall)
                continue
            m = pick
            c = self.C0f[m][wi]
            opp = (wi + 2) % 4
            for cid, extra in ((f"W1c-{wall}", Fraction(0)), (f"W1p-{wall}", self.eps)):
                ss = list(self.sq)
                ss[m] = geo.to_wall(self.sq[m], wall, c + extra)
                r = written(self.w, self.S, ss)
                exp_row = list(self.C0f[m])
                exp_row[wi] = -extra
                exp_row[opp] = self.C0f[m][opp] + c + extra
                base_ok = (
                    r["_clearances"][m] == [ftext(v) for v in exp_row]
                    and self.clear_others_same(r, m)
                    and self.margins_without(r, m)
                    and self.classes_kept_pairs(r, m)
                )
                if extra == 0:
                    ok = base_ok and r["verdict"] == self.base["verdict"]
                else:
                    ok = base_ok and r["verdict"] == "REFUSE" and r["walls"]["crossing"] == [[m + 1, wall, ftext(-extra)]]
                stated = "W1c-<wall>" if extra == 0 else "W1p-<wall>"
                self.record(cid, ok, {**self.summary(r), "square": m + 1, "clearance_sci": sci(c)}, stated)

    def translate_rule(self, wi: int, wall: str) -> None:
        """No square is eligible: the whole packing moved toward the wall instead."""
        c = min(row[wi] for row in self.C0f)
        opp = (wi + 2) % 4
        for cid, extra in ((f"W1c-{wall}", Fraction(0)), (f"W1p-{wall}", self.eps)):
            mv = c + extra
            ss = [geo.to_wall(x, wall, mv) for x in self.sq]
            r = written(self.w, self.S, ss)
            exp_cl: list[Clear] = []
            crossing: list[list[Any]] = []
            contacts: list[list[Any]] = []
            for i, row in enumerate(self.C0f):
                new = list(row)
                new[wi] = row[wi] - mv
                new[opp] = row[opp] + mv
                exp_cl.append([ftext(v) for v in new])
                for k, v in enumerate(new):
                    if v < 0:
                        crossing.append([i + 1, WALLS[k], ftext(v)])
                    elif v == 0:
                        contacts.append([i + 1, WALLS[k]])
            exp_v = "REFUSE" if crossing else self.base["verdict"]
            ok = (
                r["verdict"] == exp_v
                and r["_margins"] == self.M0
                and r["_clearances"] == exp_cl
                and r["walls"]["crossing"] == crossing
                and r["walls"]["contacts"] == contacts
                and (extra == 0 or len(crossing) > 0)
            )
            stated = "W1c-<wall>" if extra == 0 else "W1p-<wall>"
            obs = {
                **self.summary(r),
                "fallback": "whole packing translated",
                "move_sci": sci(mv),
                "squares_at_least_clearance": [i + 1 for i, row in enumerate(self.C0f) if row[wi] == c][:40],
            }
            self.record(cid, ok, obs, stated)

    def classes_kept_pairs(self, r: dict[str, Any], m: int) -> bool:
        n = self.n
        mm = r["_margins"]
        for k in range(n):
            if k == m:
                continue
            idx = pidx(n, min(k, m), max(k, m))
            if sgn(Fraction(mm[idx])) != sgn(self.M0f[idx]):
                return False
        return True

    # ---------------------------------------------------------------- PALL, WALL
    def pall(self) -> None:
        n, sq = self.n, self.sq
        fails: list[Any] = []
        h = hashlib.sha256()
        done = 0
        pa = [ma.prepare(x) for x in sq]
        pb = [mb.ccw(mb.to_mpq(x)) for x in sq]
        for i in range(n):
            for j in range(i + 1, n):
                for target in (Fraction(0), -self.eps):
                    try:
                        t = geo.closing_time(sq[i], sq[j], target)
                    except ValueError:
                        fails.append([i + 1, j + 1, "coincident centres"])
                        continue
                    h.update(ftext(t).encode() + b"\n")
                    ci, cj = geo.centre(sq[i]), geo.centre(sq[j])
                    moved = geo.translate(sq[j], -t * (cj[0] - ci[0]), -t * (cj[1] - ci[1]))
                    m_a = ma.pair_margin(pa[i], ma.prepare(moved))
                    m_c = geo.margin(sq[i], moved)
                    cls, _, agree = mb.pair_class(pb[i], mb.ccw(mb.to_mpq(moved)))
                    if not (m_a == target and m_c == target and cls == ma.sign_class(target) and agree):
                        fails.append([i + 1, j + 1, ftext(target), ftext(m_a), cls])
                    done += 1
        self.record("PALL", not fails, {"closings": done, "pairs": n * (n - 1) // 2, "failures": fails[:20], "failure_count": len(fails), "closing_times_sha256": h.hexdigest()})

    def wall_all(self) -> None:
        fails: list[Any] = []
        done = 0
        sb = mb.mpq(self.S.numerator, self.S.denominator)
        for i in range(self.n):
            row = self.C0f[i]
            wi = min(range(4), key=lambda k: (row[k], k))
            for extra in (Fraction(0), self.eps):
                moved = geo.to_wall(self.sq[i], WALLS[wi], row[wi] + extra)
                a = ma.wall_clearances(ma.prepare(moved), self.S)[wi]
                classes, area_in = mb.wall_classes(mb.ccw(mb.to_mpq(moved)), sb)
                exp_cls = "touch" if extra == 0 else "cross"
                if not (a == -extra and classes[wi] == exp_cls and (area_in == 1) == (extra == 0)):
                    fails.append([i + 1, WALLS[wi], ftext(extra)])
                done += 1
        self.record("WALL", not fails, {"moves": done, "squares": self.n, "failures": fails[:20], "failure_count": len(fails)})


def main() -> None:
    path, plan_path, count, out_path = sys.argv[1:5]
    t0 = time.process_time()
    with open(plan_path) as fh:
        plan = json.load(fh)
    run = Runner(path, plan, count)
    base_summary = run.summary(run.base)
    run.c0()
    run.r_controls()
    run.g_controls()
    s_info = run.s_controls()
    run.p_controls()
    run.w_controls()
    run.wall_all()
    run.pall()
    all_ok = all(r["outcome"] == "AS_STATED" for r in run.results)
    priors = {
        "P0_accept": run.base["verdict"] == "ACCEPT",
        "P2_S1e_accepted": s_info["S1e"] == "ACCEPT",
        "P2_S1f_refused": s_info["S1f"] == "REFUSE",
    }
    rec = {
        "count": count,
        "file": os.path.basename(path),
        "sha256": run.w.sha256,
        "sha256_matches_plan": run.w.sha256 == run.cfg["sha256"],
        "original": base_summary,
        "least_right_or_top_clearance": {"value": s_info["W"], "sci": s_info["W_sci"]},
        "status": "EVERY_CONTROL_AS_STATED" if all_ok else "SOME_CONTROL_NOT_AS_STATED",
        "as_stated": sum(r["outcome"] == "AS_STATED" for r in run.results),
        "controls_run": len(run.results),
        "priors": priors,
        "controls": run.results,
        "cpu_seconds": round(time.process_time() - t0, 1),
    }
    with open(out_path, "w") as fh:
        json.dump(rec, fh, indent=1)
        fh.write("\n")
    print(count, rec["status"], rec["as_stated"], "of", rec["controls_run"], "priors", priors)


if __name__ == "__main__":
    main()
