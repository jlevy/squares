"""A241 -- results/rows241.md: the extension table for the 16 protected classes + the 8 A55-killed k4
classes, each extension's window status, what can be rowed today and what waits on which frontier nodes.

    python rows241.py [--out results/rows241.md]

Sources, all read-only: the A56 scoreboard (the full-window rows), A241's results/param241.jsonl
(the window statements this attempt produced), A55 results/cap.json (the exact s0 kills and their
witnesses), and the k5 frontier's own closure ledgers for the three still-open k5 classes.
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
A241 = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(A241, "..", ".."))
ATT = os.path.join(ROOT, "attempts")
sys.path.insert(0, HERE)
import rowcascade241 as RC                                                      # noqa: E402

SB = RC.SCOREBOARD
CAP = os.path.join(ATT, "A55-k4-sweep", "results", "cap.json")
FULL = RC.FULL
TIER = ["trump5", "k4_03", "k4_05", "k4_06", "k4_08", "k4_11", "corners4",
        "k3_01", "k3_02", "k3_03", "k3_04", "k3_05", "k2_00", "k2_01", "k2_02", "k1_00",
        "k4_00", "k4_01", "k4_02", "k4_04", "k4_07", "k4_09", "k4_10", "k4_12", "k3_00"]
A55_KILLED = ("k4_00", "k4_01", "k4_02", "k4_04", "k4_07", "k4_09", "k4_10", "k4_12")
OPEN_K5 = ("trump5", "k5_11", "k5_16")
PROTECTED = ("k4_03", "k4_05", "k4_06", "k4_08", "k4_11", "k4_13", "corners4",
             "k3_01", "k3_02", "k3_03", "k3_04", "k3_05", "k2_00", "k2_01", "k2_02", "k1_00", "k0_00")


def frontier():
    """{open k5 class: alive frontier nodes still covering it}, from A57's PAUSED.md census (the same
    regex docs/shadows/status_gallery.py uses) -- i.e. the nodes A211/A209's frontier is working off."""
    import re
    out, f = {}, os.path.join(ATT, "A57-shadow-trees", "PAUSED.md")
    if not os.path.exists(f):
        return out
    txt = open(f, encoding="utf-8", errors="replace").read()
    m = re.search(r"([\d,]+)\s+alive A57/A60 records\s*\(([\d,]+)\s+distinct nodes:\s*"
                  r"k5_11\s*([\d,]+),\s*k5_16\s*([\d,]+),\s*trump5\s*([\d,]+)\)", txt)
    if m:
        out = {"k5_11": int(m.group(3).replace(",", "")), "k5_16": int(m.group(4).replace(",", "")),
               "trump5": int(m.group(5).replace(",", "")),
               "_total": int(m.group(2).replace(",", ""))}
    return out


def campaign():
    """A241's own window-statement campaign, one row per A55 kill."""
    out = []
    if os.path.exists(RC.PARAM_ROWS):
        for ln in open(RC.PARAM_ROWS, encoding="utf-8"):
            ln = ln.strip()
            if ln:
                out.append(json.loads(ln))
    return out


def status(name, sbrows):
    """the window status of an extension class, with its citation."""
    if name is None:
        return "never a class", "the pin set + this slot is not a census class"
    r = sbrows.get(name)
    if r and str(r.get("status", "")).startswith(FULL):
        src = (r.get("a241") or {}).get("route")
        cite = r.get("status")
        if src:
            cite += " [A241 %s]" % src
        return "FULL-WINDOW", cite
    if name in OPEN_K5:
        return "OPEN", "the k5 frontier: %s is not closed on the window" % name
    if name in A55_KILLED:
        return "s0 only", "A55 exact kill, no window statement yet (A241 campaign)"
    if name in PROTECTED:
        return "OPEN", "K1-protected: %s is a sub-skeleton of an open k5 class" % name
    return "no row", "no full-window scoreboard row"


def table():
    import load_cl241 as L
    CL = L.classes()
    sbrows = json.load(open(SB, encoding="utf-8"))["rows"]
    fr = frontier()
    out = []
    for c in TIER:
        try:
            cells = CL.forced_cells(c)
        except Exception as e:                                                  # noqa: BLE001
            out.append(dict(cls=c, error=repr(e)))
            continue
        exts = []
        for r in cells:
            st, cite = status(r["extension"], sbrows)
            exts.append(dict(cell=r["cell"], ext=r["extension"], status=st, cite=cite,
                             waits=fr.get(r["extension"] or "") if st == "OPEN" else None))
        own = sbrows.get(c)
        out.append(dict(cls=c, n=len(cells), usable=sum(1 for e in exts if e["status"] == "FULL-WINDOW"),
                        rowed=bool(own and str(own.get("status", "")).startswith(FULL)),
                        own_status=(own or {}).get("status"), exts=exts))
    return out


HEAD = """# A241 -- the ROW cascade: the one-slot extensions of the protected tier and A55's k4 kills

A class gets a **full-window row** `%s` when, and only when, one of two things holds
(`code/rowcascade241.py` docstring carries the contract):

* **(A) a direct window certificate** -- a `parametric-kill-certificate-v1` 4D PASS over the window plus
  canary C2 at 191/50 / midpoint / s0.  `closed_disjoint_bridge.md` B.2 then instantiates `stratum_kill`
  at every m in the window.
* **(B) the Lemma K1(i) climb** -- `instratum_bridge.md` E.1(i): a class CONTAINING an already-rowed class
  inherits its row (slots_S(s) is a D4 image of a subset of slots_S'(s) at every side s).

**What is NOT a row, and the correction A241 has to make to its own brief.**  "Row C when every one-slot
EXTENSION of C is full-window closed" is unsound: K1 climbs UP containment, and a packing whose skeleton is
exactly C has no fifth simple square, so C's extensions never apply to it.  Closed extensions give Lemma
SLOT-CROWD (`slot_crowds.md` s.2) -- every such slot of C is met by >= 2 non-pin squares -- i.e. C's
FORCED CELLS, the toolkit's traction (A238), not C's emptiness.  Promoting "all slots doubly met" to
"C is empty" is the crowd certificate CS(S; ...) of `slot_crowds.md` s.4, and A94 measured that it does
NOT certify (runs B2-B4 FAIL, 30-32 exact holes).  So the CASCADE below is (A) + (B), and what it hands
the k <= 3 tier is forced cells, which is exactly the lever A238 asked for.

**Why A55's eight exact k4 kills were not already rows.**  They are certified AT s0.
`closed_disjoint_bridge.md` B.2: the corpus containment margin is rho ~ 1.0000009e-9 with A = 5/2, so
(H') reads s''/m - 1 < 4.0e-10 -- an s0-anchored PASS instantiates the kill at NO side of [3.82, s-hat]
whatsoever.  The window statement is therefore real work: A56's parametric layer, re-run on A55's base
certificates.  That campaign is `code/param241.py` (resumable, `code/param241.sh`).
""" % FULL


def md(rows):
    camp = campaign()
    fr = frontier()
    L = [HEAD, "## 1. The window-statement campaign (source (A)) -- A55's exact k <= 4 kills", "",
         "| class | base certificate | atoms | stage 0 at 191/50 (gap / nearest-wall / mid-band) |"
         " 4D over the window | C2 | ROW |", "|---|---|---|---|---|---|---|"]
    if not camp:
        L.append("| _(the campaign has not written a row yet)_ | | | | | | |")
    for r in camp:
        s0 = " / ".join("%s %s" % (s["anchoring"], s["result"]) for s in r.get("stage0", [])) or "-"
        four = " / ".join("%s rc=%s %ss" % (t["anchoring"], t["rc"], t["time_s"])
                          for t in r.get("anchoring_tried", [])) or "-"
        c2 = "/".join(c["result"] for c in (r.get("c2") or [])) or "-"
        L.append("| `%s` | %s | %s | %s | %s | %s | %s |" % (
            r["name"], r.get("base", ""), (r.get("param_stats") or {}).get("atoms", "-"),
            s0, four, c2, "**YES**" if r.get("result") == "TRANSFERRED" else r.get("result")))
    L += ["", "## 2. The extension table", "",
          "| class | own row | forced cells | USABLE | extension -> status |", "|---|---|---|---|---|"]
    for r in rows:
        if r.get("error"):
            L.append("| `%s` | - | - | - | (%s) |" % (r["cls"], r["error"][:60]))
            continue
        L.append("| `%s` | %s | %d | **%d** | %s |" % (
            r["cls"], ("**ROWED** " + (r["own_status"] or "")[:48]) if r["rowed"] else "--",
            r["n"], r["usable"],
            ", ".join("%s→%s [%s]" % (e["cell"], e["ext"], e["status"]) for e in r["exts"]) or "—"))
    L += ["", "## 3. Who can be rowed TODAY, and who waits on what", "",
          "* **TODAY, and on nothing but CPU:** `k3_00` and the eight A55-killed k4 classes",
          "  (`k4_00`, `k4_01`, `k4_02`, `k4_04`, `k4_07`, `k4_09`, `k4_10`, `k4_12`).  Each already has its",
          "  own A55 `case-measure-certificate-v1` PASS; the only missing step is the parametric re-expression",
          "  and the 4D run of section 1.  `k4_00` / `k4_01` / `k4_02` have a second route: each CONTAINS",
          "  `k3_00` (D4 `id`, A55 `cap.json` witness), so once `k3_00` rows they row by (B) for free.",
          "* **NEVER by certificate:** the six protected k4 classes `k4_03`, `k4_05`, `k4_06`, `k4_08`,",
          "  `k4_11`, `k4_13`=`corners4` and the ten open k <= 3 classes.  Lemma K1(ii) (`instratum_bridge.md`",
          "  E.1(ii)) forbids it: each is <= an open k5 class, so tau*(S) >= 11 - |S| and no certificate of this",
          "  kind can exist.  Their rows can only come from the P-TREE obligation O1 per class, i.e. AFTER the",
          "  k5 frontier closes -- they are not a bookkeeping item.",
          "* **Waiting on the frontier (for forced cells, not for rows):** the cells of the protected k4 tier",
          "  that extend into `trump5`, `k5_11`, `k5_16`.  Alive frontier nodes still covering each"] + \
         (["  (A57 `PAUSED.md` census, %d distinct alive nodes): `k5_11` %d, `k5_16` %d, `trump5` %d."
           % (fr.get("_total", 0), fr.get("k5_11", 0), fr.get("k5_16", 0), fr.get("trump5", 0))]
          if fr else ["  -- census not readable from A57 `PAUSED.md`."]) + \
         ["  `corners4` is the extreme case: all eight of its cells extend into `k5_16`, so it has 0 usable",
          "  forced cells until `k5_16` is closed on the whole window (A193 and A84 s.7.1 independently).", ""]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(A241, "results", "rows241.md"))
    a = ap.parse_args(argv)
    rows = table()
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    open(a.out, "w", encoding="utf-8").write(md(rows))
    json.dump(rows, open(os.path.join(A241, "results", "rows241.json"), "w", encoding="utf-8"), indent=1)
    for r in rows:
        print("%-9s usable %s / %s  %s" % (r["cls"], r.get("usable"), r.get("n"),
                                           "ROWED" if r.get("rowed") else ""))
    print("-> %s" % os.path.relpath(a.out, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
