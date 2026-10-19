"""A243 -- the ROOT BUILDER: (n, window, pin set) -> a page in geo178.load_record's format, which run211 / stage209 /
fast30 / the coarse tree consume unchanged (nparam243 has rebound them to n and the window).

    pins  = the class's slots (classtab243.pins_of: the census frame), each an UPRIGHT box of half-width d_i at the
            slot with exact core a = 1/2 - d_i, d_i = (lambda_max - 1) * max(u, v) rounded up, (u, v) the slot centre's
            corner-frame coordinates: the dilate Delta_lambda of a packing at side m in [s_lo, s_hi] (lambda = s_hi/m)
            moves a slot square's centre by (lambda - 1) u per coordinate (forced_corners.md s.2 Step 2, n-general);
    H     = ONE non-pin square anywhere: the whole centre range [1/2, s - 1/2]^2 x [0, 90] (VACUOUS: n - k >= 1);
    budget = n - k - 1 anonymous squares.
A nid is the census class name ("n17_k08_0012"); the suffix "__spine" puts EVERY candidate forced cell into Theorem
FC's first horn ("met by two non-pin squares", nparam243.set_extra) -- a DEAD spine says the class's packings all
climb to its NOT-closed extensions (the climb's k+1 branches); without the suffix only cells whose extension is DEAD
on the table are forced (Theorem FC proper).  "n11T_<a60 tag>" is the unit test's A60 trump5 node rebuilt here.

HYPOTHESIS on every page (carried on the certificate):  P is a packing of n unit squares in [0, m]^2, m in
[s_lo, s_hi], containing an axis-aligned unit square centred at every slot of class S (side-m slots), and -- for a
spine page -- every assumed cell is met by two non-pin squares of the dilate.  DEAD = no such packing."""
import math
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import nparam243 as NP                                          # noqa: E402

HYP = ("A243 page (attempts/A243-climb-17-19/code/root243.py): P is a packing of %d unit squares in [0, m]^2, m in "
       "[%s, %s], containing an axis-aligned unit square at every slot of class %s (%s); after the dilation to side %s "
       "the pins lie in boxes of half-width (lambda_max - 1) max(u, v) about the slots (cores a = 1/2 - d).  %s  "
       "A DEAD verdict is `stratum_kill` for %s on the window (Lemma K1 / Theorem FC, n-general).")


def split(nid):
    spine = nid.endswith("__spine")
    return (nid[:-len("__spine")] if spine else nid), spine


def frame(x, s):
    """the slot's own corner-frame coordinate: i + 1/2 from the wall it is measured from (s is not an integer)."""
    return x if abs((x - 0.5) - round(x - 0.5)) < 1e-6 else float(s) - x


def delta_of(x, y, s, lam):
    u, v = frame(x, s), frame(y, s)
    d = (float(lam) - 1.0) * max(u, v)
    return math.ceil(d * 1e9 + 1) / 1e9 if d > 0 else 1e-9


def spine_cells(cls):
    """every candidate cell of the class (completable, unclipped, inside) -- Theorem FC's first horn at all of them."""
    import classtab243 as CT
    import classes178 as CL
    tab = NP.CFG["tab"]
    return [r["cell"] for r in CT.forced_cells(tab, cls, CL.S0, None, ())]


def build(n, pts, H, deltas, s):
    """the page record from slot centres, the conditioned box H and the per-pin slack d (core a = 1/2 - d)."""
    pins = [dict(kx=float(x), ky=float(y), dpin=float(d), a=float(Fr(1, 2) - Fr(str(d)))) for (x, y), d in zip(pts, deltas)]
    return dict(pins=pins, H=[tuple(float(v) for v in H)], budget=n - len(pins) - 1, s=float(s))


def record(nid):
    cls, spine = split(nid)
    tab = NP.CFG["tab"]
    n, s, lam = NP.CFG["n"], NP.CFG["s_hi"], NP.CFG["lam"]
    pts = tab.pins_of(cls)
    sf = float(s)
    rec = build(n, pts, (0.5, sf - 0.5, 0.5, sf - 0.5, 0.0, 90.0), [delta_of(x, y, s, lam) for x, y in pts], s)
    extra = spine_cells(cls) if spine else []
    NP.set_extra(extra)
    hyp = HYP % (n, NP.CFG["s_lo"], s, cls, ",".join(tab.rows[cls]["labels"]), s,
                 ("SPINE: every candidate cell %s is ASSUMED met by two non-pin squares (Theorem FC's first horn)." % extra) if spine else
                 "Forced cells: exactly those whose extension class is DEAD on this n's table (Theorem FC).", cls)
    rec.update(a243=True, cls=cls, spine=spine, assumed=extra, hypothesis=hyp)
    return rec


def load_page(nid, csv_path=None):
    if not nid.startswith("n%d_k" % NP.CFG["n"]):
        return _ORIG[0](nid, csv_path)
    rec = record(nid)
    row = dict(node=nid, camp="A243", cls=rec["cls"], level=str(len(rec["pins"])), family="n%d" % NP.CFG["n"],
               record="attempts/A243-climb-17-19/code/root243.py (synthesised)", tree="%s_window" % rec["cls"], tau=0.0,
               budget=rec["budget"], verdict=None, hypothesis=rec["hypothesis"])
    return rec, rec["cls"], row


_ORIG = [None]


def install(n):
    NP.setup(n)
    import fastprop as FP
    if _ORIG[0] is None:
        _ORIG[0] = FP.load_page
    FP.load_page = load_page
    return FP


if __name__ == "__main__":
    n = int(sys.argv[1])
    FP = install(n)
    for nid in sys.argv[2:]:
        rec, cls, row = FP.load_page(nid)
        import geo178 as G
        its = G.forced_items(cls, rec)
        print(nid, cls, "pins", [(round(p["kx"], 4), round(p["ky"], 4), p["dpin"]) for p in rec["pins"]], "budget", rec["budget"])
        print("   forced:", [(it["cell"], it.get("extension"), "ASSUMED" if it.get("assumed") else "closed") for it in its])
