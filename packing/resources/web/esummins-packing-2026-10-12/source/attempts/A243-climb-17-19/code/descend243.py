"""A243 task 2b -- the DESCENT: close the census classes of one n level by level, k = k_max down to k_stop, each by
its own tree (run243.py in a child process), and write the window table results/verdicts243_n<N>.jsonl.

    python descend243.py N --worker W --of 2 [--wall 300] [--kmax 16] [--kstop 8] [--corners4] [--commit]

Per class S (Theorem FC + Lemma K1, n-general):
  * every candidate cell p of S (completable, unclipped) has an extension T = S + p of size k + 1, already decided;
  * the node run is the SPINE "S__spine": every candidate cell assumed met by two non-pin squares.  For a cell whose
    T is DEAD that is Theorem FC itself; for a cell whose T is not DEAD it is FC's first horn, the other horn being
    "the packing climbs to T" (the teleport of Lemma SLOT-CROWD);
  * verdict DEAD     : the spine tree closed and every assumed cell had a DEAD extension  -> S is closed (theorem);
            REDUCES  : the spine tree closed but some assumed cells have NOT-closed extensions T_1..T_r -> every
                       packing of S contains the pins of some T_j (S's survival is T_j's: the climb's k+1 branches);
            ALIVE    : the spine tree did not close within the wall (undecided; nothing claimed).
--corners4 restricts a level to the classes containing all four corner slots (the climb's nodes below k_rec).
Resumable: a class with a verdict in the table is skipped.  Workers split a level by index mod --of and wait at a
barrier for the whole level before going down (the next level's forced cells read this level's verdicts)."""
import argparse
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
A243 = os.path.abspath(os.path.join(HERE, ".."))
ROOT = os.path.abspath(os.path.join(A243, "..", ".."))
sys.path.insert(0, HERE)
import census243 as CEN                                         # noqa: E402
import classtab243 as CT                                        # noqa: E402

CORNER_LABELS = ("BL(0,0)", "BR(0,0)", "TR(0,0)", "TL(0,0)")


def level(tab, k, corners4):
    out = sorted(nm for nm, r in tab.rows.items() if r["k"] == k)
    if corners4:
        out = [nm for nm in out if all(c in tab.rows[nm]["labels"] for c in CORNER_LABELS)]
    return out


def last_row(n, nid):
    f = os.path.join(A243, "results", "rows243_n%d.jsonl" % n)
    row = None
    if os.path.exists(f):
        for ln in open(f, encoding="utf-8"):
            if ('"nid": "%s"' % nid) in ln:
                try:
                    row = json.loads(ln)
                except Exception:                                 # noqa: BLE001
                    pass
    return row


def run_class(n, cls, wall, log):
    """the class's spine node IN THIS PROCESS (run243.run_node; stdout to logs/n<N>/<nid>.log)."""
    import contextlib
    import traceback
    import run243
    nid = cls + "__spine"
    t0 = time.time()
    lf = os.path.join(A243, "logs", "n%d" % n, "%s.log" % nid)
    os.makedirs(os.path.dirname(lf), exist_ok=True)
    row = None
    with open(lf, "w", encoding="utf-8") as fo, contextlib.redirect_stdout(fo):
        try:
            row = run243.run_node(run243.node_args(n, nid, wall=wall, tag="descend"))
            print("ROW243 " + json.dumps(row, default=str), flush=True)
        except Exception:                                         # noqa: BLE001
            traceback.print_exc(file=fo)
    if row is None:
        return dict(cls=cls, k=None, verdict="ERROR", why="run243 raised (log %s)" % os.path.relpath(lf, ROOT).replace("\\", "/"),
                    seconds=round(time.time() - t0, 1), wall=wall)
    v = str(row.get("verdict") or "")
    tab = CT.table(n).reload()
    assumed_open = sorted({(row["forced_ext"].get(c) or "UNNAMED:" + c) for c in row["assumed"]
                           if not tab.dead(row["forced_ext"].get(c))})
    if v.startswith("DEAD"):
        verdict = "REDUCES" if assumed_open else "DEAD"
    else:
        verdict = "ALIVE"
    why = (row.get("stage0_leaf") if str(row.get("stage0_verdict")) == "DEAD" else row.get("leaf") or "; ".join(row.get("undecided") or []))[:240]
    return dict(cls=cls, k=row["k"], verdict=verdict, tree_verdict=v, targets=assumed_open, why=why,
                stage0=row.get("stage0_verdict"), kills_by_rule=row.get("kills_by_rule"), n_nodes=row.get("n_nodes"),
                max_depth=row.get("max_depth"), root_clip=row.get("root_clip"), seconds=round(time.time() - t0, 1),
                wall=wall, wall_hit=row.get("wall"), forced=row.get("forced"), cert=row.get("cert"),
                when=time.strftime("%Y-%m-%d %H:%M:%S"))


def run_tasks(worker, log):
    """logs/TASKS_w<W>.txt: one script per line ("script.py arg ..."), run IN THIS PROCESS (runpy) so that the agent's
    analyses never add a third python process; the file is renamed to .done afterwards."""
    import contextlib
    import runpy
    f = os.path.join(A243, "logs", "TASKS_w%d.txt" % worker)
    if not os.path.exists(f):
        return
    done = f[:-4] + "_%s.done" % time.strftime("%H%M%S")
    os.replace(f, done)
    for ln in open(done, encoding="utf-8"):
        args = ln.split()
        if not args or args[0].startswith("#"):
            continue
        out = os.path.join(A243, "logs", "task_%s.log" % os.path.splitext(args[0])[0])
        old = sys.argv
        sys.argv = list(args)
        with open(out, "a", encoding="utf-8") as fo, contextlib.redirect_stdout(fo):
            try:
                runpy.run_path(os.path.join(HERE, args[0]), run_name="__main__")
            except SystemExit:
                pass
            except Exception as e:                                # noqa: BLE001
                print("TASK FAILED %r" % (e,))
        sys.argv = old
        log("   task %s done (%s)" % (" ".join(args), os.path.basename(out)))


def git_commit(paths, msg, log):
    for k in range(6):
        try:
            subprocess.call(["git", "add", "--"] + paths, cwd=ROOT)
            rc = subprocess.call(["git", "commit", "-q", "-m", msg, "--"] + paths, cwd=ROOT)
            log("   git commit rc=%s: %s" % (rc, msg.splitlines()[0]))
            return rc
        except Exception as e:                                    # noqa: BLE001
            log("   git commit failed (%r), retry" % (e,))
            time.sleep(10 + 10 * k)
    return -1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("--worker", type=int, default=0)
    ap.add_argument("--of", type=int, default=1)
    ap.add_argument("--wall", type=float, default=90, help="tree wall for k >= k_rec (the census proper)")
    ap.add_argument("--wall-mid", dest="wall_mid", type=float, default=300, help="tree wall for 4 < k < k_rec (climb nodes)")
    ap.add_argument("--wall-root", dest="wall_root", type=float, default=1800, help="tree wall for k <= 4 (the roots)")
    ap.add_argument("--rewall", action="store_true", help="re-run ALIVE classes whose recorded wall is below this pass's")
    ap.add_argument("--kmax", type=int, default=16)
    ap.add_argument("--kstop", type=int, default=None)
    ap.add_argument("--corners4", action="store_true")
    ap.add_argument("--commit", action="store_true")
    ap.add_argument("--max-classes", dest="max_classes", type=int, default=40, help="exit after this many runs (the bash loop restarts: memory hygiene)")
    a = ap.parse_args()
    tab = CT.table(a.n)
    kstop = CEN.K_REC[a.n] if a.kstop is None else a.kstop
    logf = open(os.path.join(A243, "logs", "descend243_n%d_w%d.log" % (a.n, a.worker)), "a", encoding="utf-8")

    def log(s):
        logf.write(time.strftime("%H:%M:%S ") + s + "\n")
        logf.flush()
    log("== descend n=%d worker %d/%d walls %s/%s/%s k %d -> %d corners4 %s" % (a.n, a.worker, a.of, a.wall, a.wall_mid, a.wall_root, a.kmax, kstop, a.corners4))
    ran = 0
    for k in range(a.kmax, kstop - 1, -1):
        names = level(tab, k, a.corners4)
        wall = a.wall if k >= CEN.K_REC[a.n] else (a.wall_mid if k > 4 else a.wall_root)
        t0 = time.time()
        for idx, cls in enumerate(names):
            if idx % a.of != a.worker:
                continue
            v = tab.reload().verdicts.get(cls)
            if v and not (a.rewall and v.get("verdict") == "ALIVE" and float(v.get("wall") or 0) < wall):
                continue
            run_tasks(a.worker, log)
            if os.path.exists(os.path.join(A243, "logs", "STOP")):
                log("== logs/STOP present: exiting")
                return 0
            if ran >= a.max_classes:
                log("== max-classes %d reached: exiting for a restart" % a.max_classes)
                return 3
            r = run_class(a.n, cls, wall, log)
            ran += 1
            tab.record(r)
            log("   k=%d %s -> %s (%s; %s s; %s)" % (k, cls, r["verdict"], r.get("tree_verdict"), r.get("seconds"), (r.get("why") or "")[:90]))
        while any(not tab.reload().verdict(c) or (a.rewall and tab.verdict(c) == "ALIVE" and float(tab.verdicts[c].get("wall") or 0) < wall)
                  for c in names):     # the barrier: the next level reads this one
            time.sleep(20)
        cnt = {}
        for c in names:
            v = tab.verdict(c)
            cnt[v] = cnt.get(v, 0) + 1
        log("== level k=%d done: %d classes %s (%.0f s)" % (k, len(names), cnt, time.time() - t0))
        if a.commit and a.worker == 0:
            rel = lambda p: os.path.relpath(os.path.join(A243, p), ROOT).replace("\\", "/")
            git_commit([rel("results"), rel("certs/n%d" % a.n), rel("logs")],
                       "A243: n=%d census level k=%d%s -- %d classes %s (descend243, spine trees, pad window)\n\n"
                       "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" % (a.n, k, " (corners4)" if a.corners4 else "", len(names), cnt), log)
    log("== descend n=%d worker %d finished" % (a.n, a.worker))
    return 0


if __name__ == "__main__":
    sys.exit(main())
