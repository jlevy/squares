"""A243 -- the CLASS TABLE at a new n: census243's classes (names, canonical slots) + the verdicts the descent has
proved so far (results/verdicts243_n<N>.jsonl, append-only; the LAST row per class wins, DEAD is final).

A class is DEAD on the window when its own tree (pad "window", Theorem FC with the cells whose extension classes
are DEAD) closed, or -- Lemma K1 -- when some DEAD class is contained in it up to D4 (`closed_by`).  This module is
the n-general stand-in for A53's name table + the A56 scoreboard that classes178 reads at n = 11."""
import json
import math
import os
from fractions import Fraction as Fr

import census243 as CEN

FULL_PREFIX = "FULL243"
_T = {}


class Table:
    def __init__(self, n):
        self.n = n
        d = CEN.load(n)
        self.s_lo, self.s_hi = Fr(d["s_lo"]), Fr(d["s_hi"])
        self.rows = {r["name"]: r for r in d["rows"]}
        self.canon = {}
        for r in d["rows"]:
            pts = tuple(sorted((Fr(x), Fr(y)) for x, y in r["slots"]))
            self.canon[CEN.canon(pts, self.s_hi)] = r["name"]
            r["_pts"] = pts
        self.verdicts = {}
        self.reload()

    def vpath(self):
        return os.path.join(CEN.A243, "results", "verdicts243_n%d.jsonl" % self.n)

    def reload(self):
        self.verdicts = {}
        f = self.vpath()
        if os.path.exists(f):
            for ln in open(f, encoding="utf-8"):
                try:
                    r = json.loads(ln)
                except Exception:                                 # noqa: BLE001
                    continue
                old = self.verdicts.get(r["cls"])
                if old is not None and old.get("verdict") == "DEAD":
                    continue                                      # DEAD is final
                self.verdicts[r["cls"]] = r
        return self

    def exact(self, p):
        """a float slot centre -> the exact lattice centre at s_hi (snap; the lattice is 1/2 + integers from a wall)."""
        out = []
        for v in p:
            a = Fr(round(float(v) - 0.5)) + Fr(1, 2)
            b = self.s_hi - Fr(round(float(self.s_hi) - 0.5 - float(v))) - Fr(1, 2)
            out.append(a if abs(float(a) - float(v)) < 1e-6 else b)
            assert abs(float(out[-1]) - float(v)) < 1e-6, "not a lattice slot: %r" % (p,)
        return tuple(out)

    def name_of(self, pts):
        if not pts:
            return "n%d_k00_0000" % self.n
        ex = tuple(sorted(self.exact(p) for p in pts))
        if len(set(ex)) != len(ex):
            return None
        return self.canon.get(CEN.canon(ex, self.s_hi))

    def pins_of(self, name):
        return [(float(x), float(y)) for x, y in self.rows[name]["_pts"]]

    def verdict(self, name):
        return (self.verdicts.get(name) or {}).get("verdict")

    def dead(self, name):
        return self.verdict(name) == "DEAD"

    def status(self, name):
        """classes178.scoreboard_status's shape: FULL iff the class is DEAD on the window."""
        if name is None or name not in self.rows:
            return None
        v = self.verdicts.get(name) or {}
        st = ("%s [%s, %s] %s" % (FULL_PREFIX, self.s_lo, self.s_hi, v.get("why", "")[:80])) if v.get("verdict") == "DEAD" else \
             ("OPEN243 %s" % (v.get("verdict") or "not yet run"))
        return dict(result=v.get("verdict"), status=st, full=v.get("verdict") == "DEAD")

    def subsets_dead(self, name):
        """Lemma K1: a DEAD class contained (as a slot set, any D4 image) in `name`, or None."""
        pts = self.rows[name]["_pts"]
        S = set(pts)
        for other, v in self.verdicts.items():
            if v.get("verdict") != "DEAD" or other == name:
                continue
            q = self.rows[other]["_pts"]
            if len(q) >= len(pts):
                continue
            for f in CEN.D4:
                if all(f(x, y, self.s_hi) in S for x, y in q):
                    return other
        return None

    def record(self, row):
        with open(self.vpath(), "a", encoding="utf-8") as f:
            f.write(json.dumps(row, default=str) + "\n")
        self.reload()


def table(n):
    if n not in _T:
        _T[n] = Table(n)
    return _T[n]


def forced_cells(tab, cls, s, max_off=None, extra=()):
    """classes178.forced_cells, n-general: every Young-completable, UNCLIPPED, non-pin cell (offsets <= floor(s) - 1),
    `usable` iff its extension class is DEAD in the table, or the cell is in `extra` (the climb's hypothesis "this cell
    is met by two non-pin squares", Theorem FC's other horn assumed).  Lemma SLOT-CROWD / Theorem FC are n-general:
    their proofs use only the teleport at side m and the dilation (forced_corners.md s.2)."""
    import classes178 as CL
    mo = (int(math.floor(float(s))) - 1) if max_off is None else max_off
    pins = tab.pins_of(cls)
    out = []
    for c in CL.CORNERS:
        for i in range(mo + 1):
            for j in range(mo + 1):
                pt = CL.slot_centre(c, i, j, s)
                if CL.is_pin(pins, pt):
                    continue
                if i >= 1 and not CL.is_pin(pins, CL.slot_centre(c, i - 1, j, s)):
                    continue
                if j >= 1 and not CL.is_pin(pins, CL.slot_centre(c, i, j - 1, s)):
                    continue
                if CL.clipped_by_pin(pins, c, i, j, s):
                    continue
                if pt[0] + 0.5 > float(s) + 1e-9 or pt[1] + 0.5 > float(s) + 1e-9 or min(pt) < 0.5 - 1e-9:
                    continue
                cell = "%s(%d,%d)" % (c, i, j)
                ext = tab.name_of(pins + [pt])
                st = tab.status(ext) if ext else None
                full = bool(st and st["full"])
                out.append(dict(cell=cell, corner=c, i=i, j=j, extension=ext, status=(st or {}).get("status"),
                                usable=full or cell in extra, assumed=(cell in extra and not full),
                                is_corner=(i == 0 and j == 0)))
    return out
