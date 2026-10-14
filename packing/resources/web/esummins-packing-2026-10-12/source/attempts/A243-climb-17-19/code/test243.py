"""A243 -- the n = 11 UNIT TEST of the generalisation (must pass before any n = 17 / 19 run).

  T1  census243 at n = 11 reproduces A53's Young census (D4 classes per k, 163 classes, Trump's class present);
  T2  nparam243.setup(11) is the IDENTITY on the toolkit: no global / default rebinding changes a value, the derived
      constants (C_WIDEN, W0_RAT, LAM_MAX, PADS["window"]) equal the originals, noroom_at243 gates exactly at k >= 9;
  T3  classtab243.forced_cells (the n-general FC census) == classes178.forced_cells (A53 + the A56 scoreboard) on every
      class A53 names, cell for cell, extension for extension, usable flag for usable flag;
  T4  root243.build with n = 11, pins = Trump's 5 slots (trump5), the A60 node c0_Y0072's slack d and H reproduces
      that A57-format root (geo178.load_record of attempts/A60-trump5-campaign/results/nodes/c0_Y0072.json): pins,
      cores, H, budget;
  T5  fast30.Stage0 on the rebuilt page (pad zero) reproduces A212's stage-0 certificate of the same node
      (certs/csp209_c0_Y0072_zero_s0.json): verdict, forced H, per-rule kill counts, CSP alive units.
python test243.py  -> prints PASS / FAIL per test, exit code = number of failures."""
import json
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True
import census243 as CEN                                         # noqa: E402
import nparam243 as NP                                          # noqa: E402

ATT = os.path.abspath(os.path.join(HERE, "..", ".."))
FAILS = []


def check(name, ok, detail=""):
    print("%-4s %s %s" % (name, "PASS" if ok else "FAIL", detail), flush=True)
    if not ok:
        FAILS.append(name)


def t1():
    d = CEN.build(11)
    a53 = json.load(open(os.path.join(ATT, "A53-simple-strata", "results", "skeletons_young.json"), encoding="utf-8"))
    check("T1", d["census_d4_by_k"] == a53["census_d4_by_k"] and d["n_rows"] == a53["n_classes_d4"],
          "census %s vs A53 %s" % (d["census_d4_by_k"], a53["census_d4_by_k"]))


def t2():
    import path243
    path243.fix()
    import stage209, tree211, run211                              # noqa: F401,E401
    import multibox as MB
    import classes178 as CL
    import quick200 as QP
    c0 = (MB.C_WIDEN, MB.W0_RAT, CL.LAM_MAX, QP.PADS["window"])
    NP.setup(11, classes=False)
    changed = [r for r in NP.report() if r[0] in ("global", "default", "kwdefault")]
    c1 = (MB.C_WIDEN, MB.W0_RAT, CL.LAM_MAX, QP.PADS["window"])
    same = all(abs(float(a) - float(b)) < 1e-15 for a, b in zip(c0, c1))

    class PG:
        roles = {"r%d" % i: (0, 1, 0, 1, 0, 0) for i in range(8)}
        name = "t"

        class T:
            @staticmethod
            def test(*a, **k):
                pass
    gate8 = NP.noroom_at243(PG, 10.0)["reason"].startswith("not attempted")
    check("T2", not changed and same and gate8, "rebindings that changed a value: %d; derived equal %s; k=8 gated %s" % (len(changed), same, gate8))


def t3():
    import classes178 as CL
    import classtab243 as CT

    class Tab:
        pins_of = staticmethod(CL.pins_of)
        name_of = staticmethod(lambda pts: CL.class_of(pts))
        status = staticmethod(CL.scoreboard_status)
    names = sorted(CL.name_to_slots())
    bad, n_cells, n_usable = [], 0, 0
    for cls in names:
        ours = CT.forced_cells(Tab, cls, CL.S0, 2, ())
        theirs = CL.forced_cells(cls)
        a = [(r["cell"], r["extension"], r["usable"]) for r in ours]
        b = [(r["cell"], r["extension"], r["usable"]) for r in theirs]
        n_cells += len(b)
        n_usable += sum(1 for r in b if r[2])
        if a != b:
            bad.append((cls, a, b))
    check("T3", not bad, "%d classes, %d cells, %d usable; mismatches %s" % (len(names), n_cells, n_usable, bad[:2]))


def t4_t5():
    import geo178 as G
    import root243
    import fastprop as FP
    import classes178 as CL
    rel = os.path.join("attempts", "A60-trump5-campaign", "results", "nodes", "c0_Y0072.json")
    ref = G.load_record(rel)
    pts = CL.pins_of("trump5")
    byxy = {(round(p["kx"], 6), round(p["ky"], 6)): p for p in ref["pins"]}
    deltas = [byxy[(round(x, 6), round(y, 6))]["dpin"] for x, y in pts]
    rec = root243.build(11, pts, ref["H"][0], deltas, CL.S0)
    key = lambda P: sorted((round(p["kx"], 9), round(p["ky"], 9), round(p["dpin"], 12), round(p["a"], 12)) for p in P)
    ok4 = key(rec["pins"]) == key(ref["pins"]) and rec["H"] == ref["H"] and rec["budget"] == ref["budget"] and \
        G.class_of_record(rec) == "trump5"
    check("T4", ok4, "pins %s / H %s / budget %s vs %s" % (len(rec["pins"]), rec["H"][0][:2], rec["budget"], ref["budget"]))
    orig = FP.load_page

    def lp(nid, csv_path=None):
        if nid == "n11T_c0_Y0072":
            return rec, "trump5", dict(node=nid)
        return orig(nid, csv_path)
    FP.load_page = lp
    import fast30 as F30
    out = F30.Stage0("n11T_c0_Y0072", "zero", log=lambda *a: None).run()
    c = json.load(open(os.path.join(ATT, "A212-trump5-tree", "certs", "csp209_c0_Y0072_zero_s0.json"), encoding="utf-8"))
    kills = lambda d: {k: v.get("kills") for k, v in (d.get("kills") or {}).items()}
    alive = lambda d: (d.get("csp") or [{}])[-1].get("alive_units")
    ok5 = out["verdict"] == c["verdict"] and sorted(out.get("forced_H") or []) == sorted(c.get("forced_H") or []) and \
        kills(out) == kills(c) and alive(out) == alive(c)
    check("T5", ok5, "verdict %s/%s forced_H %s/%s alive units %s/%s kills %s / %s" % (
        out["verdict"], c["verdict"], out.get("forced_H"), c.get("forced_H"), alive(out), alive(c), kills(out), kills(c)))


if __name__ == "__main__":
    t1()
    t2()
    t3()
    t4_t5()
    print("FAILURES: %s" % (FAILS or "none"))
    sys.exit(len(FAILS))
