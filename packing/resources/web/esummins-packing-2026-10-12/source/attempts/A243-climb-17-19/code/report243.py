"""A243 -- results/climb243.md from the window tables (verdicts243_n*.jsonl), the climb trees (climb243.py) and the
rigidity measurements (rigid243.py).  Safe to run at any time (the chain runs it at every phase end).
    python report243.py"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
A243 = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import climb243 as CL                                           # noqa: E402

SRC = {17: "s_lo = 116511/25000 (T-043; T-093 raises it to 18641771/4000000), s_hi = 4675531/10^6 >= T-065's 4.67553009360455...",
       19: "s_lo = 193/40 (T-103, superseding T-020's 24/5), s_hi = 4885619/10^6 >= the best known 3 + 4 sqrt2/3 = 4.88561808..."}


def block(n):
    s = CL.summary(n)
    L = ["## n = %d" % n, "", "Window [%s, %s]: %s." % (s["window"][0], s["window"][1], SRC[n]), "",
         "Census (A53's Young slot-set classes, D4-reduced, window-stable) and the descent's verdicts per k "
         "(spine trees, pad window, no LP; `root dead` = closed at stage 0 or at the tree's root node):", "",
         "| k | classes | corners4 | DEAD | REDUCES | ALIVE | pending | root dead | stage-0 dead | CPU-s |", "|---|---|---|---|---|---|---|---|---|---|"]
    for k, d in s["census_by_k"].items():
        L.append("| %s | %d | %d | %d | %d | %d | %d | %d | %d | %.0f |" % (k, d["classes"], d["corners4"], d.get("DEAD", 0), d.get("REDUCES", 0),
                                                                        d.get("ALIVE", 0), d["pending"], d["root_dead"], d["stage0_dead"], d["seconds"]))
    L += ["", "Decided %d classes in %.2f CPU-h.  Kills by rule (tree leaves; STAGE0 = classes closed by the closed-form "
          "stage 0 + CSP): %s." % (s["n_done"], s["cpu_h"], json.dumps(s["rules"], sort_keys=True)), ""]
    c = s["climb"]
    L += ["**Record class** %s: %s%s.  **Soundness canary** (no class contained in the record's may be DEAD -- the record "
          "realises it inside the window): %s." % (s["record"], s["record_verdict"] or "PENDING",
                                                 (" -> " + ", ".join(s["record_targets"] or [])) if s["record_targets"] else "",
                                                 "OK" if not s["canary_dead_in_record"] else "VIOLATED %s" % s["canary_dead_in_record"]), "",
          "**The climb** from the four-corner root %s (task 2; nodes = classes on root-to-leaf paths, depth capped at the "
          "record's k): %d path nodes over %d classes, depth %d, leaves %s, reaches the record class: %s." % (
              s["root"], c["n_nodes"], c["n_classes"], c["max_depth"], c["leaves"], c["reaches_record"]), ""]
    if c["alive_leaves"]:
        L += ["Open leaves (ALIVE, or REDUCES at the record's k):", ""]
        L += ["- `%s` (k %d%s)" % (a["path"], a["k"], ", the record" if a["record"] else (", inside the record's class" if a["in_record"] else ""))
              for a in c["alive_leaves"][:20]]
        L.append("")
    f = os.path.join(A243, "results", "rigid243_n%d.json" % n)
    if os.path.exists(f):
        r = json.load(open(f, encoding="utf-8"))
        lp = r.get("lp") or {}
        L += ["**Rigidity of the record [M]** (rigid243.py, first-order, side fixed): %d contacts, rank %d of %d, rattlers %s; "
              "first-order motion LP max |v|_1 = %s over squares %s -> %s." % (
                  r["n_contacts"], r["rank"], 3 * r["n_squares"], r["rattlers"] or "none", lp.get("max_l1"), lp.get("moving"),
                  "infinitesimally RIGID" if r.get("rigid_first_order") else "NOT first-order rigid (a tube must be a band, not a point)"), ""]
    return L, s


def main():
    L = ["# A243 -- the simple-square climb at n = 17 and n = 19 (corners pinned; FC run forward as a slot-set tree)", "",
         "Generated %s by code/report243.py from results/verdicts243_n*.jsonl (the descend243 / chain243 runs are "
         "resumable and may still be running: `pending` rows are not yet run).  Method and soundness: notes/climb243.md." % time.strftime("%Y-%m-%d %H:%M"), ""]
    S = {}
    for n in (17, 19):
        b, s = block(n)
        L += b
        S[n] = s
    open(os.path.join(A243, "results", "climb243.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    json.dump(S, open(os.path.join(A243, "results", "climb243_summary.json"), "w", encoding="utf-8"), indent=1)
    print("\n".join(L))


if __name__ == "__main__":
    main()
