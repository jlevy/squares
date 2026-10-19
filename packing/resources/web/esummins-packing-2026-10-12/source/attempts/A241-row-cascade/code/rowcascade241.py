"""A241 -- the ROW CASCADE.  Turn A241's verified window statements into A56 scoreboard rows, then
climb Lemma K1 until nothing moves; idempotent, with a log of what changed.

    python rowcascade241.py            # dry run: print the diff, touch nothing
    python rowcascade241.py --apply    # write the rows into the A56 scoreboard (backup first)
    python rowcascade241.py --apply --report   # + refresh results/rows241.md

WHAT MAY BE ROWED, AND WHY (the soundness contract -- read before adding a source)

A scoreboard row `FULL [191/50, 969271/250000]` for a class T is consumed by
`classes178.forced_cells` / Lemma SLOT-CROWD as: **no packing of eleven unit squares at ANY side
m in the window carries axis-aligned unit squares at all slots of T** (the MONOTONE class of T is
empty on the whole window).  Exactly two things produce one:

  (A) A DIRECT window certificate.  A `parametric-kill-certificate-v1` 4D PASS over
      [191/50, 969271/250000] plus canary C2 (the unmodified A53 verify_case.py at 191/50, the
      midpoint and s0).  `closed_disjoint_bridge.md` B.2 then instantiates the kill at every m in
      the window (rationals are dense in each s-cell; rho > 0 exact; nofams empty).  This is what
      `param241.py` produces from A55's base certificates and it is the ONLY new mathematics here.
  (B) The Lemma K1 CLIMB.  `instratum_bridge.md` E.1(i): if S <= S' (sub-diagram order, up to D4)
      and S is dead at side m, then S' is dead at m -- a packing carrying S's slots is carried by
      one carrying S''s.  So any class CONTAINING an already-rowed class inherits its row, with
      the SAME window.  The row cites the contained class and the D4 element.

**What is NOT a source, and the reason the brief's phrasing has to be sharpened.**  The tempting
rule "row C when every ONE-SLOT EXTENSION of C is full-window closed" is UNSOUND as an emptiness
statement.  K1 climbs UP containment, not down: a packing whose skeleton is exactly C has no fifth
simple square, so no extension class ever applies to it, and closed extensions say nothing about
C's own emptiness.  What closed extensions DO give is Lemma SLOT-CROWD -- every such slot of C is
met by >= 2 non-pin squares -- i.e. C's FORCED CELLS (Theorem FC), which is the traction A238
measured, not a row.  Turning "all slots doubly met" into "C is empty" needs the crowd-counting
certificate CS(S; ...) of `slot_crowds.md` s.4, and A94 measured that it does NOT certify
(runs B2-B4 FAIL with 30-32 exact holes).  So this script rows by (A) and (B) only, and the
cascade it runs is the K1 climb -- which is exactly what hands the k <= 3 classes their forced
cells, because their extensions are the k4 classes (A) and (B) close.

s0-only certificates are refused outright: B.2's corpus margin is rho ~ 1.0e-9 with A = 5/2, so
(H') reads s''/m - 1 < 4.0e-10 and an s0-anchored PASS kills at NO side of [3.82, s-hat].
"""
import argparse
import json
import os
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
A241 = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(A241, "..", ".."))
ATT = os.path.join(ROOT, "attempts")
SCOREBOARD = os.path.join(ATT, "A56-sparametric", "results", "scoreboard.json")
PARAM_ROWS = os.path.join(A241, "results", "param241.jsonl")
CHANGELOG = os.path.join(A241, "results", "cascade241.jsonl")
WINDOW = ["191/50", "969271/250000"]
FULL = "FULL [191/50, 969271/250000]"

N2S_FILES = [os.path.join(ATT, "A53-simple-strata", "results", "name_to_slots.json"),
             os.path.join(ATT, "A55-k4-sweep", "results", "name_to_slots.json")]
TIER84 = os.path.join(ATT, "A84-protected-trees", "results", "tier84_classes.json")
S0 = 969271 / 250000

D4 = (lambda x, y: (x, y), lambda x, y: (S0 - x, y), lambda x, y: (x, S0 - y),
      lambda x, y: (S0 - x, S0 - y), lambda x, y: (y, x), lambda x, y: (S0 - y, x),
      lambda x, y: (y, S0 - x), lambda x, y: (S0 - y, S0 - x))
D4_NAME = ("id", "mx", "my", "r180", "transpose", "r90", "r270", "antitranspose")


def slots():
    """the MERGED census: A53 (k5/k6/trump5/corners4) + A55 (k3_00, k4_*) + A84's protected tier."""
    out = {}
    for f in N2S_FILES:
        if os.path.exists(f):
            for k, v in json.load(open(f, encoding="utf-8")).items():
                out.setdefault(k, [(round(float(a), 5), round(float(b), 5)) for a, b in v])
    if os.path.exists(TIER84):
        from fractions import Fraction as Fr
        for k, d in json.load(open(TIER84, encoding="utf-8")).items():
            pts = [(round(float(Fr(a)), 5), round(float(Fr(b)), 5)) for a, b in (d.get("pins") or [])]
            old = out.get(k)
            if old is not None:
                assert sorted(old) == sorted(pts), "A241: tier84 disagrees with name_to_slots on %s" % k
            out[k] = pts
    return out


def contains(big, small):
    """(g, True) when some D4 image of `small`'s slots is a subset of `big`'s: Lemma K1(i)'s hypothesis."""
    B = set((round(x, 5), round(y, 5)) for x, y in big)
    for f, nm in zip(D4, D4_NAME):
        if all((round(a, 5), round(b, 5)) in B for a, b in (f(x, y) for x, y in small)):
            return nm
    return None


def transferred():
    """A241's verified window statements: {name: row}, TRANSFERRED only."""
    out = {}
    if os.path.exists(PARAM_ROWS):
        for ln in open(PARAM_ROWS, encoding="utf-8"):
            ln = ln.strip()
            if not ln:
                continue
            r = json.loads(ln)
            if r.get("result") == "TRANSFERRED":
                out[r["name"]] = r
    return out


def direct_row(r):
    """source (A): the scoreboard row of a class with its own 4D PASS + C2 3/3."""
    return {
        "name": r["name"], "k": int(r["name"][1]),
        "result": "TRANSFERRED", "status": FULL + " -- A241 window statement of A55's exact kill",
        "s_range": list(WINDOW), "s_ranges": [list(WINDOW)], "window_coverage": 1.0,
        "single_corner": False, "open_band": [], "margin": None,
        "anchoring": r.get("anchoring"), "param_result": "PASS", "param_time_s": r.get("param_time_s"),
        "param_stats": r.get("param_stats"), "c2": r.get("c2"),
        "source": "A241 (A)", "a241": {
            "route": "direct window certificate",
            "base_certificate": r.get("base"), "provenance": r.get("provenance"),
            "parametric_cert": r.get("parametric_cert"),
            "bridge": "closed_disjoint_bridge.md B.2: parametric PASS on s-cells covering the window "
                      "+ rho > 0 exact + nofams empty ==> stratum_kill at every m in [191/50, 969271/250000]",
            "k1": "not used (this row is its own certificate)"},
        "certs": {"original_s0_cert": r.get("base"), "parametric_cert": r.get("parametric_cert"),
                  "carries_the_window_claim": r.get("parametric_cert"),
                  "note": "A55's base case-measure-certificate-v1 re-expressed with s-affine atom and core "
                          "positions (A56 C1 identity), 4D-verified over the window, C2 at 191/50 / mid / s0"},
    }


def climb_row(name, src, g, srcrow):
    """source (B): Lemma K1(i), instratum_bridge.md E.1(i) -- `name` contains `src`, which is rowed."""
    return {
        "name": name, "k": int(name[1]), "result": "K1", "status": FULL + " by Lemma K1(i) climb from " + src,
        "s_range": list(WINDOW), "s_ranges": [list(WINDOW)], "window_coverage": 1.0,
        "single_corner": False, "open_band": [], "margin": None, "source": "A241 (B)",
        "a241": {"route": "Lemma K1(i) climb", "contains": src, "d4": g,
                 "k1": "instratum_bridge.md E.1(i): slots_%s(s) is a D4(%s) image of a SUBSET of slots_%s(s) at "
                       "every side s, so any packing carrying %s's slots carries %s's; %s is dead on the whole "
                       "window, hence so is %s" % (name, g, name, name, src, src, name),
                 "cited_row": srcrow.get("status")},
        "certs": {"carries_the_window_claim": (srcrow.get("certs") or {}).get("carries_the_window_claim"),
                  "note": "no certificate of its own: the window claim is %s's, climbed by Lemma K1(i)" % src},
    }


def plan():
    """-> (rows_to_add, notes).  Idempotent: a class already FULL in the scoreboard is never touched."""
    sb = json.load(open(SCOREBOARD, encoding="utf-8"))
    have = dict(sb["rows"])
    S, tr, add, notes = slots(), transferred(), {}, []
    for name, r in sorted(tr.items()):
        if name in have:
            notes.append("%s: already on the scoreboard (%s)" % (name, have[name].get("status", "")[:40]))
            continue
        add[name] = direct_row(r)
        notes.append("%s: ROW (A) direct window certificate, anchoring %s, %ss"
                     % (name, r.get("anchoring"), r.get("param_time_s")))
    changed = True
    while changed:                                                              # the K1 climb to a fixed point
        changed = False
        rowed = dict(have)
        rowed.update(add)
        for name, pts in sorted(S.items()):
            if name in rowed or not pts:
                continue
            for src, srcrow in sorted(rowed.items()):
                sp = S.get(src)
                if not sp or len(sp) > len(pts):
                    continue
                g = contains(pts, sp)
                if g:
                    add[name] = climb_row(name, src, g, srcrow)
                    notes.append("%s: ROW (B) Lemma K1(i) climb from %s (D4 %s)" % (name, src, g))
                    changed = True
                    break
    return sb, add, notes


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args(argv)
    sb, add, notes = plan()
    for n in notes:
        print("  " + n)
    print("cascade: %d new row(s): %s" % (len(add), ", ".join(sorted(add)) or "-"))
    if add and a.apply:
        bak = SCOREBOARD + ".bak_pre_a241"
        if not os.path.exists(bak):
            shutil.copy2(SCOREBOARD, bak)
        sb = json.load(open(SCOREBOARD, encoding="utf-8"))       # A114's rule: never a stale copy
        add = {k: v for k, v in add.items() if k not in sb["rows"]}
        if not add:
            print("nothing to add after re-read")
            return 0
        sb["rows"].update(add)
        sb.setdefault("a241", {})
        sb["a241"] = {"attempt": "A241-row-cascade",
                      "when": time.strftime("%Y-%m-%dT%H:%M:%S"),
                      "rows": sorted(add),
                      "what": "window statements for A55's exact k <= 4 kills (A56's parametric layer re-run on "
                              "A55's base certificates) plus the Lemma K1(i) climb; sources (A)/(B) of "
                              "attempts/A241-row-cascade/code/rowcascade241.py",
                      "previous_row_count": sum(1 for k in sb["rows"] if k not in add)}
        sm = sb.setdefault("summary", {})
        sm["total"] = len(sb["rows"])
        sm["full_window_rows"] = sum(1 for r in sb["rows"].values()
                                     if str(r.get("status", "")).startswith(FULL))
        tmp = SCOREBOARD + ".a241.tmp"                           # A114's rule: tmp + atomic replace
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(sb, fh, indent=1)
        os.replace(tmp, SCOREBOARD)
        with open(CHANGELOG, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"when": time.strftime("%Y-%m-%dT%H:%M:%S"),
                                 "added": sorted(add), "notes": notes}, sort_keys=True) + "\n")
        print("-> %s (%d rows, backup %s)" % (os.path.relpath(SCOREBOARD, ROOT), len(sb["rows"]),
                                              os.path.basename(bak)))
    if a.report:
        sys.path.insert(0, HERE)
        import rows241                                                          # noqa: E402
        rows241.main([])
    return 0


if __name__ == "__main__":
    sys.exit(main())
