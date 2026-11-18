"""The controls of ``controls-plan.json`` on one certificate (lane r127b-1118).

Usage:

    python -I -B rb127_controls.py pair LABEL EXACT.json WITNESS.yaml PLAN.json CLAIM OUT.json
    python -I -B rb127_controls.py house LABEL CANDIDATE.yaml PLAN.json CLAIM OUT.json

``CLAIM`` is the 12-place print the control S1e sets as the side (the issue's claim, or
for the house the ceiling of its side), written as a decimal.

Each control changes the certificate and states its outcome in advance as a rule over
the certificate's exact facts (its rows, its side, and method A's margins, clearances
and contact factors), since those facts were unknown when the plan was written. The
program evaluates each rule exactly and compares it with what both methods decide on
the changed packing; a decision in which the methods disagree fails its control.
Whole-file controls write the changed packing as the bytes of both forms with this
review's writer and read them back through the strict readers; reader controls change
the original bytes.

"Contact" is a margin or clearance of exactly 0, and "past" is 1e-40 beyond it.
A control that changes some squares decides again every pair and wall that holds one of
them; a pair or wall it does not decide again is unchanged, and a pair's decision is a
function of its two squares alone. Such a decision reads ``PARTIAL`` where all it
decided holds.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction as Fr
from itertools import combinations
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gmpy2 import mpq  # noqa: E402

import rb127_axes as A  # noqa: E402
import rb127_clip as B  # noqa: E402
import rb127_contract as K  # noqa: E402
import rb127_decide as D  # noqa: E402
import rb127_fmt as F  # noqa: E402
import rb127_read as R  # noqa: E402
import rb127_twin as T  # noqa: E402
import rb127_write as W  # noqa: E402

Q = tuple[int, int]
TINY = Fr(1, 10**40)
WALLS = ("left", "bottom", "right", "top")


def pq(f: Fr) -> Q:
    return f.numerator, f.denominator


def fr(v: Q) -> Fr:
    return Fr(v[0], v[1])


def dec_text(text: str) -> Fr:
    whole, _, frac = text.partition(".")
    return Fr(int(whole + frac), 10 ** len(frac))


class Cert:
    """One certificate's exact facts, by method A."""

    def __init__(self, rows: list[tuple[Q, Q, Q, Q]], corners: list[tuple[tuple[Q, Q], ...]], side: Q) -> None:
        self.rows = rows
        self.corners = corners
        self.side = side
        self.S = fr(side)
        self.n = len(rows)
        self.ip = [A.to_ipose(*r) for r in rows]
        self.margin: dict[tuple[int, int], Fr] = {}
        self.nums: dict[tuple[int, int], tuple[int, int, int]] = {}
        for i, j in combinations(range(self.n), 2):
            M, Hn, L = A.pair_numbers(self.ip[i], self.ip[j])
            self.nums[(i, j)] = (M, Hn, L)
            self.margin[(i, j)] = Fr(M - Hn, L)
        self.clear = [A.clearances(p, side) for p in self.ip]
        self.h = [A.half_extent(p) for p in self.ip]
        self.cen = [A.centre(p) for p in self.ip]

    def factor(self, i: int, j: int) -> Fr:
        M, Hn, _ = self.nums[(i, j)]
        return Fr(Hn, M)


def read_pair(jb: bytes, cb: bytes) -> tuple[dict, dict]:
    return R.read_form_j(jb), R.read_form_c(cb)


def write_read(n: int, side: Q, rows: list, corners: list | None = None) -> tuple[dict, dict]:
    corners = corners if corners is not None else [T.corners_pq(r) for r in rows]
    return read_pair(W.form_j(n, side, rows), W.form_c(n, side, corners))


def native(J: dict, C: dict, **kw: Any) -> dict:
    return D.decide(J["rows"], C["corners"], J["side"], **kw)


def c_alone(C: dict, **kw: Any) -> dict:
    return D.decide([T.pose_of_corners(c) for c in C["corners"]], C["corners"], C["side"], **kw)


def pair_margins(dec: dict) -> dict[tuple[int, int], Fr]:
    return {(r["pair"][0] - 1, r["pair"][1] - 1): r["margin_a"] for r in dec["pairs"] if "margin_a" in r}


def classes_agree(dec: dict) -> bool:
    ok = all(r.get("class_a") == r.get("class_b") for r in dec["pairs"])
    ok = ok and all(r.get("classes_a") == r.get("classes_b") for r in dec["walls"])
    return ok


def wall_sets(dec: dict) -> tuple[dict[str, list[int]], dict[str, list[int]]]:
    touch: dict[str, list[int]] = {w: [] for w in WALLS}
    cross: dict[str, list[int]] = {w: [] for w in WALLS}
    for r in dec["walls"]:
        for w in range(4):
            c = r["clearances_a"][w]
            if c == 0:
                touch[WALLS[w]].append(r["square"])
            elif c < 0:
                cross[WALLS[w]].append(r["square"])
    return touch, cross


def refuses(fn, *args) -> tuple[bool, str]:
    try:
        fn(*args)
    except R.ReadError as exc:
        return True, str(exc)[:160]
    return False, "read"


class Runner:
    def __init__(self, label: str, mode: str, jb: bytes | None, cb: bytes, claim: str) -> None:
        self.label = label
        self.mode = mode
        self.jb = jb
        self.cb = cb
        self.jt = jb.decode("ascii") if jb is not None else None
        self.ct = cb.decode("ascii")
        self.C = R.read_form_c(cb)
        if mode == "pair":
            self.J = R.read_form_j(jb)
            rows = self.J["rows"]
        else:
            self.J = None
            rows = [T.pose_of_corners(c) for c in self.C["corners"]]
        self.cert = Cert(rows, self.C["corners"], self.C["side"])
        self.claim = claim
        self.results: list[dict[str, Any]] = []

    def record(self, cid: str, stated: str, ok: bool, outcome: Any) -> None:
        self.results.append({"control": cid, "stated": stated, "as_stated": bool(ok), "outcome": outcome})

    # -------------------------------------------------------------- whole-file decisions

    def decide_rows(self, rows: list, side: Q, **kw: Any) -> dict:
        """Write the rows as both forms (or form C alone for the house), read back, decide."""
        n = self.cert.n
        if self.mode == "pair":
            J, C = write_read(n, side, rows)
            dec = native(J, C, **kw)
            tw = T.twin(J["rows"], C["corners"])
            dec["twin_holds"] = tw["holds"]
            return dec
        C = R.read_form_c(W.form_c(n, side, [T.corners_pq(r) for r in rows]))
        dec = c_alone(C, **kw)
        dec["twin_holds"] = True
        return dec

    # -------------------------------------------------------------- reader controls

    def reader_controls(self) -> None:
        ct = self.ct
        # R1: the last square deleted.
        idx = ct.rfind("\n  - id: ")
        after = ct.find("\n  claim:", idx)
        mutated_c = ct[:idx] + ct[after:] if after != -1 else ct[: idx + 1]
        ok, why = refuses(R.read_form_c, mutated_c.encode())
        stated = "form C refused: the count stated exceeds the squares listed"
        self.record("R1-C", stated, mutated_c != ct and ok and "stated" in why, why)
        if self.jt is not None:
            jt = self.jt
            idx = jt.rfind(",\n  [\n")
            mutated = jt[:idx] + "\n ]\n}"
            applied = len(json.loads(mutated)["squares"]) == self.cert.n - 1
            ok, why = refuses(R.read_form_j, mutated.encode())
            self.record("R1-J", "form J refused: the count stated exceeds the squares listed", applied and ok and "stated" in why, why)
        # R2: the side as 2p/2q.
        p, q = self.cert.side
        side_text = f"{p}/{q}" if q != 1 else str(p)
        c2 = ct.replace(f"  side: {side_text}\n", f"  side: {2 * p}/{2 * q}\n", 1)
        C2 = R.read_form_c(c2.encode())
        ok = c2 != ct and fr(C2["side"]) == self.cert.S and C2["corners"] == self.C["corners"] and "side not in lowest terms" in C2["flags"]
        self.record("R2-C", "read; the same value and corners; the side flagged as not in lowest terms", ok, C2["flags"])
        if self.jt is not None:
            j2 = self.jt.replace(f' "side": "{side_text}",', f' "side": "{2 * p}/{2 * q}",', 1)
            J2 = R.read_form_j(j2.encode())
            ok = j2 != self.jt and fr(J2["side"]) == self.cert.S and J2["rows"] == self.J["rows"] and "side not in lowest terms" in J2["flags"]
            self.record("R2-J", "read; the same value and rows; the side flagged as not in lowest terms", ok, J2["flags"])
        # R3: ids of squares 1 and 2 exchanged in form C; rows 1 and 2 exchanged in form J.
        if self.C["id_style"] == "square-k":
            a, b = "  - id: square-1\n", "  - id: square-2\n"
        else:
            a, b = "  - id: 1\n", "  - id: 2\n"
        c3 = ct.replace(a, "\0", 1).replace(b, a, 1).replace("\0", b, 1)
        ok, why = refuses(R.read_form_c, c3.encode())
        self.record("R3-C", "form C refused: ids out of order", c3 != ct and ok and "out of order" in why, why)
        if self.jt is not None:
            jt = self.jt
            start = jt.index('"squares": [\n') + len('"squares": [\n')
            first_end = jt.index("\n  ],\n", start) + len("\n  ],\n")
            second_end = jt.index("\n  ],\n", first_end) + len("\n  ]")
            block1 = jt[start:first_end - 2]
            block2 = jt[first_end:second_end]
            j3 = jt[:start] + block2 + ",\n" + block1 + jt[second_end:]
            J3 = R.read_form_j(j3.encode())
            tw = T.twin(J3["rows"], self.C["corners"])
            ok = J3["rows"][0] == self.J["rows"][1] and J3["rows"][1] == self.J["rows"][0] and tw["failures"] == [1, 2]
            self.record("R3-J", "form J read; the twin fails at exactly squares 1 and 2", ok, tw["failures"][:10])
        # R4: the side as a 40-place decimal.
        d40 = F.ceil_places(self.cert.S, 40)
        for name, text, fn in (
            ("R4-C-quoted", ct.replace(f"  side: {side_text}\n", f"  side: '{d40}'\n", 1), R.read_form_c),
            ("R4-C-plain", ct.replace(f"  side: {side_text}\n", f"  side: {d40}\n", 1), R.read_form_c),
        ):
            ok, why = refuses(fn, text.encode())
            self.record(name, "refused: not a scalar p or p/q, or a YAML float", text != ct and ok, why)
        if self.jt is not None:
            j4 = self.jt.replace(f' "side": "{side_text}",', f' "side": "{d40}",', 1)
            ok, why = refuses(R.read_form_j, j4.encode())
            self.record("R4-J", "refused: not a scalar p or p/q", j4 != self.jt and ok, why)
        # R5: a leading plus sign on square 1's first coordinate; R6: a bare number there.
        x0 = self.C["corners"][0][0][0]
        x0t = f"{x0[0]}/{x0[1]}" if x0[1] != 1 else f"'{x0[0]}'"
        line = f"    - - {x0t}\n"
        c5 = ct.replace(line, f"    - - '+{x0t.strip(chr(39))}'\n", 1)
        ok, why = refuses(R.read_form_c, c5.encode())
        self.record("R5-C", "refused, naming the coordinate", c5 != ct and ok and "square 1" in why, why)
        c6 = ct.replace(line, "    - - 7\n", 1)
        ok, why = refuses(R.read_form_c, c6.encode())
        self.record("R6-C", "refused: a corner scalar that is not a string", c6 != ct and ok, why)
        if self.jt is not None:
            v = self.J["rows"][0][0]
            vt = f"{v[0]}/{v[1]}" if v[1] != 1 else str(v[0])
            j5 = self.jt.replace(f'  [\n   "{vt}",', f'  [\n   "+{vt}",', 1)
            ok, why = refuses(R.read_form_j, j5.encode())
            self.record("R5-J", "refused, naming the coordinate", j5 != self.jt and ok and "square 1" in why, why)
            j6 = self.jt.replace(f'  [\n   "{vt}",', "  [\n   7,", 1)
            ok, why = refuses(R.read_form_j, j6.encode())
            self.record("R6-J", "refused: a JSON number in place of a scalar string", j6 != self.jt and ok, why)

    # -------------------------------------------------------------- geometry controls

    def geometry_controls(self) -> None:
        c, n, S = self.cert, self.cert.n, self.cert.S
        # G1: square n given square 1's row.
        rows = list(c.rows)
        rows[n - 1] = rows[0]
        dec = self.decide_rows(rows, c.side, squares=[n - 1], pairs=[(k, n - 1) for k in range(n - 1)])
        m = pair_margins(dec)
        overl = sorted(k for k, v in m.items() if v < 0)
        pred = all(m[(k, n - 1)] == c.margin[(0, k)] for k in range(1, n - 1)) and m[(0, n - 1)] == -1
        b_area = [r.get("area_b") for r in dec["pairs"] if tuple(r["pair"]) == (1, n)]
        ok = dec["verdict"] == "REFUSE" and pred and overl == [(0, n - 1)] and b_area == [1] and classes_agree(dec)
        self.record("G1", "refused; (1, n) at margin -1 with B area 1 the only overlap; each (k, n) at the original (1, k)",
                    ok, {"verdict": dec["verdict"], "overlaps": [[i + 1, j + 1] for i, j in overl]})
        # G2: square 1 translated by (S, 0).
        rows = list(c.rows)
        x, y, cc, ss = rows[0]
        rows[0] = (pq(fr(x) + S), y, cc, ss)
        dec = self.decide_rows(rows, c.side, squares=[0], pairs=[(0, k) for k in range(1, n)])
        L, Bm, Rr, Tt = c.clear[0]
        w = dec["walls"][0]
        ok = (dec["verdict"] == "REFUSE" and w["clearances_a"] == (L + S, Bm, Rr - S, Tt) and w["inside_b"] == 0
              and all(v >= 0 for v in pair_margins(dec).values()) and classes_agree(dec))
        self.record("G2", "refused: square 1's clearances exactly (L+S, B, R-S, T), none of it inside, no pair overlapping",
                    ok, {"verdict": dec["verdict"], "inside_b": str(w["inside_b"])})
        # G3: square 1's first corner moved by 1e-40 in x, in form C.
        corners = list(c.corners)
        (cx0, cy0) = corners[0][0]
        corners[0] = ((pq(fr(cx0) + TINY), cy0),) + tuple(corners[0][1:])
        C3 = R.read_form_c(W.form_c(n, c.side, corners))
        dec = c_alone(C3, squares=[0], pairs=[])
        tw = T.twin(c.rows, C3["corners"])
        w = dec["walls"][0]
        ok = dec["verdict"] == "REFUSE" and not w["unit_a"] and not w["unit_b"] and tw["failures"] == [1]
        self.record("G3", "refused: square 1 not a unit square by A or B; the twin fails at square 1 only", ok,
                    {"verdict": dec["verdict"], "twin_failures": tw["failures"][:5]})
        # G4: form C with every square listed in reverse.
        corners = [tuple(reversed(cs)) for cs in c.corners]
        C4 = R.read_form_c(W.form_c(n, c.side, corners))
        dec = c_alone(C4)
        tw = T.twin(c.rows, C4["corners"])
        senses = {r["sense_b"] for r in dec["walls"]}
        same = pair_margins(dec) == c.margin
        ok = dec["verdict"] == "ACCEPT" and tw["holds"] and senses == {-1} and same and classes_agree(dec)
        self.record("G4", "accepted with every listing clockwise; margins identical; the twin holds", ok,
                    {"verdict": dec["verdict"], "senses": sorted(senses), "listings": tw["listings"]})
        # G5 to G7: transposed, quarter turn, mirrored.
        for cid, fn, perm, stated in (
            ("G5", lambda x, y, u, v: (y, x, v, u), (1, 0, 3, 2), "transposed: margins identical; (L,B,R,T) -> (B,L,T,R)"),
            ("G6", lambda x, y, u, v: (S - y, x, -v, u), (3, 0, 1, 2), "quarter turn: margins identical; (L,B,R,T) -> (T,L,B,R)"),
            ("G7", lambda x, y, u, v: (S - x, y, -u, v), (2, 1, 0, 3), "mirrored: margins identical; (L,B,R,T) -> (R,B,L,T)"),
        ):
            rows = []
            for r in c.rows:
                x, y, u, v = fn(fr(r[0]), fr(r[1]), fr(r[2]), fr(r[3]))
                rows.append((pq(x), pq(y), pq(u), pq(v)))
            dec = self.decide_rows(rows, c.side)
            same = pair_margins(dec) == c.margin
            walls_ok = all(
                tuple(r["clearances_a"]) == tuple(c.clear[r["square"] - 1][perm[k]] for k in range(4))
                for r in dec["walls"]
            )
            ok = dec["verdict"] == "ACCEPT" and same and walls_ok and classes_agree(dec) and dec["twin_holds"]
            self.record(cid, "accepted; " + stated, ok, {"verdict": dec["verdict"]})

    # -------------------------------------------------------------- side, extent, contraction

    def side_rule(self, cid: str, new_side: Fr, stated: str) -> None:
        c = self.cert
        delta = c.S - new_side
        side_pq = pq(new_side)
        dec = self.decide_rows(list(c.rows), side_pq, squares=list(range(c.n)), pairs=[])
        rows_ok = all(
            tuple(r["clearances_a"]) == (c.clear[k][0], c.clear[k][1], c.clear[k][2] - delta, c.clear[k][3] - delta)
            for k, r in enumerate(dec["walls"])
        )
        W_ = min(min(cl[2], cl[3]) for cl in c.clear)
        expect = "PARTIAL" if delta <= W_ else "REFUSE"
        touch, cross = wall_sets(dec)
        pt = sorted(k + 1 for k in range(c.n) if c.clear[k][2] - delta == 0 or c.clear[k][3] - delta == 0)
        px = sorted(k + 1 for k in range(c.n) if c.clear[k][2] - delta < 0 or c.clear[k][3] - delta < 0)
        got_t = sorted(set(touch["right"]) | set(touch["top"]))
        got_x = sorted(set(cross["right"]) | set(cross["top"]))
        ok = rows_ok and dec["verdict"] == expect and got_t == pt and got_x == px and classes_agree(dec)
        self.record(cid, stated + f"; by the side rule {'accepted' if expect == 'PARTIAL' else 'refused'}", ok,
                    {"delta_sci": F.sci(delta, 6), "verdict": dec["verdict"], "touching": len(got_t), "crossing": len(got_x)})

    def side_controls(self) -> None:
        c = self.cert
        W_ = min(min(cl[2], cl[3]) for cl in c.clear)
        self.side_rule("S1a", c.S - TINY, "the side lowered by 1e-40")
        self.side_rule("S1b", c.S - Fr(1, c.side[1]), "the side lowered by 1/q, q its denominator")
        self.side_rule("S1c", c.S - W_, "the side lowered by W, the least right-or-top clearance")
        self.side_rule("S1d", c.S - W_ - TINY, "the side lowered by W + 1e-40")
        claim = dec_text(self.claim)
        self.side_rule("S1e", claim, f"the side set to the claim {self.claim}")
        self.side_rule("S1f", claim - Fr(1, 10**12), "the side set to the claim less 1e-12")

    def extent_controls(self) -> None:
        c = self.cert
        Lmin = min(cl[0] for cl in c.clear)
        Bmin = min(cl[1] for cl in c.clear)
        width = max(c.cen[k][0] + c.h[k] for k in range(c.n)) - min(c.cen[k][0] - c.h[k] for k in range(c.n))
        height = max(c.cen[k][1] + c.h[k] for k in range(c.n)) - min(c.cen[k][1] - c.h[k] for k in range(c.n))
        X = max(width, height)
        rows = [(pq(fr(r[0]) - Lmin), pq(fr(r[1]) - Bmin), r[2], r[3]) for r in c.rows]
        dec = self.decide_rows(rows, pq(X))
        touch, cross = wall_sets(dec)
        want = {
            "left": sorted(k + 1 for k in range(c.n) if c.clear[k][0] == Lmin),
            "bottom": sorted(k + 1 for k in range(c.n) if c.clear[k][1] == Bmin),
            "right": sorted(k + 1 for k in range(c.n) if width == X and c.cen[k][0] + c.h[k] - (min(c.cen[j][0] - c.h[j] for j in range(c.n))) == X),
            "top": sorted(k + 1 for k in range(c.n) if height == X and c.cen[k][1] + c.h[k] - (min(c.cen[j][1] - c.h[j] for j in range(c.n))) == X),
        }
        same = pair_margins(dec) == c.margin
        ok = dec["verdict"] == "ACCEPT" and same and {w: sorted(v) for w, v in touch.items()} == want and classes_agree(dec)
        self.record("E1c", "every square moved by the least left and bottom clearances, the side its extent X: accepted; "
                    "margins identical; walls touched exactly by the squares at the least clearances and at the larger extent",
                    ok, {"verdict": dec["verdict"], "side_less_extent_sci": F.sci(c.S - X, 8),
                         "touching": {w: len(v) for w, v in touch.items()}, "width_equals_height": width == height})
        dec2 = self.decide_rows(rows, pq(X - TINY), squares=list(range(c.n)), pairs=[])
        _, cross2 = wall_sets(dec2)
        got = sorted(set(cross2["right"]) | set(cross2["top"]))
        ok = dec2["verdict"] == "REFUSE" and got == sorted(set(want["right"]) | set(want["top"])) and classes_agree(dec2)
        self.record("E1p", "the same with the side X - 1e-40: refused, exactly the squares at the larger extent crossing", ok,
                    {"verdict": dec2["verdict"], "crossing": len(got)})

    def contraction_controls(self) -> None:
        c = self.cert
        k = K.contraction(c.rows, c.side)
        lam = k["_lam"]
        binding = sorted((p[0] - 1, p[1] - 1) for p in k["binding_pairs"])
        rows, side = K.shrunk_rows(c.rows, lam)
        dec = self.decide_rows(rows, side)
        m = pair_margins(dec)
        pred = {ij: lam * Fr(M, L) - Fr(Hn, L) for ij, (M, Hn, L) in c.nums.items()}
        zeros = sorted(ij for ij, v in m.items() if v == 0)
        ok = dec["verdict"] == "ACCEPT" and m == pred and zeros == binding and classes_agree(dec) and fr(side) == k["_shrunk_side"]
        self.record("K1c", "centres scaled by lambda*, the first contact, in the box of the shrunk side: accepted; every margin "
                    "exactly lambda* M - H; the touching pairs exactly the binding pairs", ok,
                    {"verdict": dec["verdict"], "lambda_star": k["lambda_star"], "touching_pairs": [[i + 1, j + 1] for i, j in zeros],
                     "shrunk_side": k["shrunk_side"], "margin_sci": k["margin_sci"]})
        lam_p = lam * (1 - TINY)
        rows_p, side_p = K.shrunk_rows(c.rows, lam_p)
        dec = self.decide_rows(rows_p, side_p)
        m = pair_margins(dec)
        over = sorted(ij for ij, v in m.items() if v < 0)
        want = sorted(ij for ij in c.nums if c.factor(*ij) > lam_p)
        pred = {ij: lam_p * Fr(M, L) - Fr(Hn, L) for ij, (M, Hn, L) in c.nums.items()}
        _, cross = wall_sets(dec)
        ok = dec["verdict"] == "REFUSE" and over == want and m == pred and not any(cross.values()) and classes_agree(dec)
        self.record("K1p", "scaled by lambda*(1 - 1e-40) in its own extent: refused; the overlaps exactly the pairs whose factor "
                    "exceeds it; no wall crossed", ok, {"verdict": dec["verdict"], "overlaps": [[i + 1, j + 1] for i, j in over]})
        dec = self.decide_rows(rows, pq(fr(side) - TINY), squares=list(range(c.n)), pairs=[])
        _, cross = wall_sets(dec)
        ok = dec["verdict"] == "REFUSE" and bool(cross["right"] or cross["top"]) and not cross["left"] and not cross["bottom"]
        self.record("K1s", "K1c's packing in a box 1e-40 smaller: refused at the right or top wall only", ok,
                    {"verdict": dec["verdict"], "crossing": {w: len(v) for w, v in cross.items()}})

    # -------------------------------------------------------------- every pair, every square, C0, X1

    def all_pairs(self) -> None:
        c = self.cert
        bad = []
        done = 0
        orig = []
        for r in c.rows:
            p = B.to_points(T.corners_pq(r))
            okp, sp = B.unit_square(p)
            orig.append((okp, B.ccw(p, sp)))
        for (i, j), (M, Hn, L) in c.nums.items():
            xi, yi = c.cen[i]
            xj, yj = c.cen[j]
            for target in (Fr(0), -TINY):
                s = (target + Fr(Hn, L)) / Fr(M, L)
                nx, ny = xi + s * (xj - xi), yi + s * (yj - yi)
                rj = (pq(nx), pq(ny), c.rows[j][2], c.rows[j][3])
                m = A.margin(c.ip[i], A.to_ipose(*rj))
                oki, pi = orig[i]
                pj = B.to_points(T.corners_pq(rj))
                okj, sj = B.unit_square(pj)
                pj = B.ccw(pj, sj)
                cls, _, agree = B.pair(pi, pj)
                proj = B.projections_margin(pi, pj)
                want = "contact" if target == 0 else "overlap"
                if not (m == target and cls == want and agree and oki and okj and (target != 0 or proj == 0)):
                    bad.append([i + 1, j + 1, str(target)])
                done += 1
        self.record("PALL", "every pair closed along its line of centres to contact and 1e-40 past: A's margin exactly 0 and "
                    "-1e-40, the corner projections exactly 0 at contact, B touching and overlapping both ways round",
                    not bad, {"closings": done, "failures": bad[:20]})

    def all_walls(self) -> None:
        c = self.cert
        S_b = mpq(c.side[0], c.side[1])
        bad = []
        done = 0
        for k in range(c.n):
            cl = c.clear[k]
            w = min(range(4), key=lambda t: (cl[t], t))
            x, y = c.cen[k]
            for target in (Fr(0), -TINY):
                shift = cl[w] - target
                nx, ny = x, y
                if w == 0:
                    nx = x - shift
                elif w == 1:
                    ny = y - shift
                elif w == 2:
                    nx = x + shift
                else:
                    ny = y + shift
                rk = (pq(nx), pq(ny), c.rows[k][2], c.rows[k][3])
                a_cl = A.clearances(A.to_ipose(*rk), c.side)
                pts = B.to_points(T.corners_pq(rk))
                ok, sense = B.unit_square(pts)
                wc, inside = B.walls(B.ccw(pts, sense), S_b)
                want = "contact" if target == 0 else "overlap"
                if not (a_cl[w] == target and ok and wc[w][0] == want and ((inside == 1) == (target == 0))):
                    bad.append([k + 1, WALLS[w], str(target)])
                done += 1
        self.record("WALL", "every square moved to its nearest wall and 1e-40 past: A's clearance exactly 0 and -1e-40; B touching "
                    "and crossing; B's area inside 1 and below 1", not bad, {"moves": done, "failures": bad[:20]})

    def c0(self) -> None:
        c = self.cert
        pts = []
        for cs in c.corners:
            p = B.to_points(cs)
            ok, sense = B.unit_square(p)
            pts.append(B.ccw(p, sense))
        bad_pairs = []
        for (i, j), m in c.margin.items():
            proj = B.projections_margin(pts[i], pts[j])
            if Fr(int(proj.numerator), int(proj.denominator)) != m:
                bad_pairs.append([i + 1, j + 1])
        bad_walls = []
        for k, cs in enumerate(c.corners):
            xs = [fr(p[0]) for p in cs]
            ys = [fr(p[1]) for p in cs]
            cl = (min(xs), min(ys), c.S - max(xs), c.S - max(ys))
            if cl != tuple(c.clear[k]):
                bad_walls.append(k + 1)
        self.record("C0", "every margin from the form C corners' projections, and every clearance from their extremes, equal to "
                    "method A's from the poses", not bad_pairs and not bad_walls,
                    {"pairs": len(c.margin), "pair_mismatches": bad_pairs[:20], "wall_mismatches": bad_walls[:20]})

    def x1(self) -> None:
        c = self.cert
        rows = [(r[0], r[1], r[2], pq(-fr(r[3]))) for r in c.rows]
        tw = T.twin(rows, c.corners)
        tilted = [k + 1 for k, r in enumerate(c.rows) if fr(r[2]) * fr(r[3]) != 0]
        self.record("X1", "each direction (c, s) read as (c, -s): the twin fails at exactly the squares not upright", tw["failures"] == tilted,
                    {"twin_failures": len(tw["failures"]), "not_upright": len(tilted)})

    def run(self) -> dict[str, Any]:
        t0 = time.process_time()
        timings = {}
        for name, fn in (("reader", self.reader_controls), ("geometry", self.geometry_controls),
                         ("side", self.side_controls), ("extent", self.extent_controls),
                         ("contraction", self.contraction_controls), ("C0", self.c0), ("X1", self.x1),
                         ("WALL", self.all_walls), ("PALL", self.all_pairs)):
            t1 = time.process_time()
            fn()
            timings[name] = round(time.process_time() - t1, 2)
        every = all(r["as_stated"] for r in self.results)
        return {
            "program": "rb127_controls.py",
            "label": self.label,
            "mode": self.mode,
            "verdict": "EVERY_CONTROL_AS_STATED" if every else "SOME_CONTROL_NOT_AS_STATED",
            "controls": len(self.results),
            "not_as_stated": [r["control"] for r in self.results if not r["as_stated"]],
            "results": self.results,
            "cpu_seconds_by_group": timings,
            "cpu_seconds": round(time.process_time() - t0, 2),
        }


def check_plan(plan_path: str, mode: str, ran: list[str]) -> list[str]:
    plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    stated = [c["id"] for c in plan["controls"] if mode in c["applies_to"]]
    return sorted(set(stated) ^ set(ran))


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[1] == "pair" and len(argv) == 8:
        label, jp, cp, plan, claim, out = argv[2:8]
        runner = Runner(label, "pair", Path(jp).read_bytes(), Path(cp).read_bytes(), claim)
    elif len(argv) >= 2 and argv[1] == "house" and len(argv) == 7:
        label, cp, plan, claim, out = argv[2:7]
        runner = Runner(label, "house", None, Path(cp).read_bytes(), claim)
    else:
        print(__doc__)
        return 2
    rec = runner.run()
    diff = check_plan(plan, runner.mode, [r["control"] for r in runner.results])
    rec["plan_mismatch"] = diff
    if diff:
        rec["verdict"] = "SOME_CONTROL_NOT_AS_STATED"
    Path(out).write_text(json.dumps(rec, indent=1, default=str) + "\n", encoding="utf-8")
    print(f"{label}: {rec['verdict']} ({rec['controls']} controls; not as stated: {rec['not_as_stated']}; plan mismatch: {diff})")
    return 0 if rec["verdict"] == "EVERY_CONTROL_AS_STATED" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
