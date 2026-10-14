"""A209 COPY of A207 tree207 (7db40795, unchanged). A207 -- A206's TreePage206 with the BASIN CLIP (clip207) applied to every non-pin role's pieces before every fixed point and
to every reach result (the anonymous option rows, the instantiated roles' reach at their slots), so that no pose inside the
basin B_F(p) of a FULL slot p ever enters the cascade.  A role left with no piece is DEAD: [C: extension certificate + Lemma
BASIN + library clip trace] naming the basin's certificate and radius.  Everything else is A206's (Rule NS, A205's clips, A204's
cascade); the tree is A206's Tree206 with this cascade."""
import time

import poly204 as P
import tree205b as TB
import tree206 as N6
import clip207 as C

FP = P.FP
_SAVE206, _RESTORE206 = N6.save_state, N6.restore_state       # the originals (install() rebinds N6's names to ours)


class TreePage207(N6.TreePage206):
    def __init__(self, *a, basins=None, **kw):
        N6.TreePage206.__init__(self, *a, **kw)
        self.basins = list(basins or [])
        self.basin_rep = []
        self.basin_reach = {}

    def basin_clip(self, label):
        """every non-pin role's pieces minus the basins; False when a role is emptied (DEAD)."""
        for k, pcs in list(self.pieces.items()):
            if k.startswith("P") or not pcs:
                continue
            new, rep = C.clip_pieces(pcs, self.basins)
            if rep:
                self.pieces[k] = new
                self.basin_rep.append(dict(label=label, role=k, removed=[(c, round(f, 6)) for c, f in rep], n_before=len(pcs), n_after=len(new)))
                self.T.test("BASIN-CLIP", role=k, label=label, removed=[(c, round(f, 6)) for c, f in rep], n_before=len(pcs), n_after=len(new))
                if not new:
                    b = max(self.basins, key=lambda d: d["rc"])
                    cells = sorted(set(c for c, _ in rep))
                    self.dead = ("BASIN(%s) at %s: every pose of %s lies in the basin of the simple pose of %s (Lemma BASIN: the extension certificate "
                                 "re-solved with the boxed slot square, r_c = %s, r_t = %.3f deg, window %s; %s)" % (
                                     k, label, k, cells, float(b["rc"]), float(b.get("r_t_deg") or 0), b.get("window"), b.get("cert")))
                    self.fix_rep = dict(dead=k, detail="basin", seconds=0.0)
                    self.T.test("BASIN-CLIP", role=k, label=label, verdict="DEAD", cells=cells)
                    return False
        return True

    def normalise(self, label):
        if self.basins and not self.basin_clip(label):
            self.T.step("normalise", 0.0, label=label, dead=self.fix_rep["dead"], detail="basin")
            return None
        return N6.TreePage206.normalise(self, label)

    def _clip_res(self, res, key):
        if not self.basins or not res[1] or key in self.basin_reach:
            return res
        new, rep = C.clip_pieces(res[1], self.basins)
        self.basin_reach[key] = rep
        if not rep:
            return res
        v0, v1 = P.vol(res[1]), P.vol(new)
        self.T.test("BASIN-REACH", key=str(key), removed=[(c, round(f, 6)) for c, f in rep], n_before=len(res[1]), n_after=len(new))
        return (float(res[0] * (v1 / v0)) if v0 else 0.0, new, res[2])

    def reach(self, ci, S):
        key = (ci, S)
        if key in self.reach_cache:
            return self.reach_cache[key]
        res = self._clip_res(N6.TreePage206.reach(self, ci, S), ("cell", ci, tuple(sorted(S))))
        self.reach_cache[key] = res
        return res

    def role_reach(self, role, S):
        key = (role, S)
        if key in self.reach_cache:
            return self.reach_cache[key]
        res = self._clip_res(N6.TreePage206.role_reach(self, role, S), (role, tuple(sorted(S))))
        self.reach_cache[key] = res
        return res


    def snapshot(self, rnd, label):
        """A204's snapshot, or -- when the basin clip killed the node BEFORE any fixed point (self.nd is None on a freshly loaded
        leaf) -- one built from the node's current pieces (no K'), so that the record carries what the panel IS."""
        if self.nd is not None:
            return N6.TreePage206.snapshot(self, rnd, label)
        roles = {}
        for k in self.roles:
            pcs = self.pieces.get(k) or []
            roles[k] = dict(box=[round(float(v), 6) for v in self.roles[k]], n_pieces=len(pcs), pieces=[P.piece6(b, r) for b, r in pcs][:600], kprime=[],
                            kept=None, corner=self.corners_now().get(k))
        snap = dict(pad=self.pad, round=rnd, label=label + " (basin clip before the fixed point)", roles=roles, forced_H=sorted(self.forced_H),
                    role_slots={k: list(v) for k, v in self.role_slots.items()}, t=round(self.T.now(), 1), fix=(self.fix_rep or {}), dead=self.dead)
        self.snapshots.append(snap)
        return snap


def save_state(pg):
    st = _SAVE206(pg)
    st["basin_rep"], st["basin_reach"] = list(pg.basin_rep), dict(pg.basin_reach)
    return st


def restore_state(pg, st):
    _RESTORE206(pg, st)
    pg.basin_rep, pg.basin_reach = list(st["basin_rep"]), dict(st["basin_reach"])


def cascade(pg, rounds, log=print):
    pg.basin_reach = {}
    clip, rnd = TB.cascade(pg, rounds, log=log)
    d = (pg.fix_rep or {}).get("detail")
    if pg.dead and d == "missclip":
        clip = "MISS-CLIP"
    if pg.dead and d == "basin":
        clip = "BASIN"
    return clip, rnd


def install():
    """route A206's tree through this cascade and state (the copies in this directory only)."""
    N6.cascade = cascade
    N6.save_state = save_state
    N6.restore_state = restore_state
