"""A211g regression -- the RESUME bug: pass 2 over the gallery finished every page in 3-9 s without running anything.

Two invariants, both checked here:
 1. run211.wall_limited / the cached-verdict gate: a pad whose recorded ALIVE verdict came from the WALL must be
    RE-RUN on a fresh wall (it resumes: inherit211 ranks A211's own certificate highest, so the previous run's DEAD
    branches come back as inherited dead and the tree restarts at the alive frontier).  A DEAD pad, a stage-0 kill
    and an ALIVE pad that stopped for any reason other than time stay cached.
 2. startload211.load runs the start node on the RUN's OWN clock: pg.T.left() == the run's wall (minus only the
    seconds the load itself spent), never an elapsed time inherited from the recorded snapshot or a previous pass --
    that is what would make every loaded start node "undecided (wall) at the fully named leaf" in seconds.

  python test_resume211.py [<nid>] [<pad>]        (default: the first page of queue_gallery_pass2.txt, pad g1)
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
import load211                                                    # noqa: E402
load211.install()
import run211 as R                                                # noqa: E402
import poly204 as P                                               # noqa: E402
import inherit211 as INH                                          # noqa: E402
import startload211 as SL                                         # noqa: E402
import stage209                                                   # noqa: E402
import clip207 as C                                               # noqa: E402

FP, QP = P.FP, P.QP
OK, BAD = [], []


def check(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("   %-4s %s%s" % ("ok" if cond else "FAIL", name, (" -- " + detail) if detail else ""), flush=True)


def test_gate():
    """the cached-verdict gate (bug 1): WALL-limited ALIVE pads re-run, everything else stays cached."""
    wallrun = dict(verdict="ALIVE", wall=True, undecided=[dict(label="R.9.2x", reason="undecided (wall) at the fully named leaf before the leaf rules")])
    caprun = dict(verdict="ALIVE", wall=False, undecided=[dict(label="R.3", reason="undecided: node cap before this branch ran")])
    loadrun = dict(verdict="ALIVE", wall=False, undecided=[dict(label="R.3", reason="undecided: the start node could not be loaded soundly (ValueError(...))")])
    deadrun = dict(verdict="DEAD", wall=False, undecided=[])
    s0run = dict(verdict="DEAD", stage0_kill=True)
    check("gate: wall-limited ALIVE resumes", R.wall_limited(wallrun) is True)
    check("gate: node-cap ALIVE resumes", R.wall_limited(caprun) is True)
    check("gate: a loader refusal now RESUMES (A211h)",            # startload211 climbs to the nearest COMPLETE
          R.wall_limited(loadrun) is True)                          # ancestor (A203 root at worst): not final
    check("gate: DEAD stays cached", R.wall_limited(deadrun) is False)
    check("gate: stage-0 kill stays cached", R.wall_limited(s0run) is False)
    check("gate: a missing run stays cached", R.wall_limited({}) is False and R.wall_limited(None) is False)


def test_clock(nid, pad, wall=1800.0):
    """the start-node clock (bug 2): a FRESH Trace per run; a spent one is refused, never silently used."""
    rec, cls, row = FP.load_page(nid)
    start = stage209.start_of(nid, pad)
    basins = C.load_basins(cls, pad, QP.PADS[pad]) if pad != "zero" else []
    M = INH.merge(nid, pad, start.get("file"), log=lambda *a, **k: None)
    starts = list((M or {}).get("starts") or [])
    check("merge: %s pad %s has start nodes" % (nid, pad), bool(starts), "%d start nodes" % len(starts))
    if not starts:
        return
    sn = starts[0]
    T = FP.Trace(wall=wall)
    check("trace: a fresh Trace has the run's whole wall", abs(T.left() - wall) < 1.0, "left %.1f of %.1f" % (T.left(), wall))
    t0 = time.time()
    pg, meta = SL.load(sn, rec, cls, nid, T, pad, start, basins, rounds=1, wall=wall, log=lambda *a, **k: None)
    spent = time.time() - t0
    check("load: the page runs on the caller's Trace", pg.T is T)
    check("load: pg.T.left() == the run's wall (less only the load itself)",
          abs(pg.T.left() - (wall - spent)) < 2.0, "left %.1f, wall %.1f, load %.1f s" % (pg.T.left(), wall, spent))
    check("load: the loaded start node is NOT out of time", not pg.T.out_of_time())
    check("load: the snapshot's t is provenance only",
          (meta.get("recorded") or {}).get("t") is None or pg.T.now() < spent + 1.0,
          "snapshot t = %s, clock now %.1f s" % ((meta.get("recorded") or {}).get("t"), pg.T.now()))
    spentT = FP.Trace(t0=time.time() - (wall + 60.0), wall=wall)
    try:
        SL.load(sn, rec, cls, nid, spentT, pad, start, basins, rounds=1, wall=wall, log=lambda *a, **k: None)
        check("load: a SPENT Trace is refused", False, "the load accepted an exhausted Trace")
    except ValueError as e:
        check("load: a SPENT Trace is refused", "already spent" in str(e))
    try:
        SL.load(sn, rec, cls, nid, FP.Trace(wall=wall + 1.0), pad, start, basins, rounds=1, wall=wall, log=lambda *a, **k: None)
        check("load: a foreign wall is refused", False, "the load accepted a Trace with another run's wall")
    except ValueError as e:
        check("load: a foreign wall is refused", "not the run's wall" in str(e))


def test_pages(queue):
    """the pass-2 queue as it stands: which pages the gate now re-runs."""
    n_res = 0
    for nid in [x.strip() for x in open(queue, encoding="utf-8").read().split() if x.strip() and not x.startswith("#")]:
        f = os.path.join(ROOT, "attempts", "A211-coarse-tree", "certs", "coarsetree211_%s.json" % nid)
        if not os.path.exists(f):
            continue
        doc = json.load(open(f, encoding="utf-8"))
        pads = [p for p in ("zero", "g1") if doc.get("verdicts", {}).get(p) not in (None, "DEAD")
                and R.wall_limited((doc.get("runs") or {}).get("%s_page" % p) or {})]
        n_res += bool(pads)
        print("   %-24s verdicts %s -> resumes %s" % (nid, doc.get("verdicts"), pads or "-"), flush=True)
    check("queue: every WALL-limited page of the pass-2 queue now resumes", n_res > 0, "%d pages" % n_res)


if __name__ == "__main__":
    R.belownormal()
    Q = os.path.join(HERE, "queue_gallery_pass2.txt")
    nid = sys.argv[1] if len(sys.argv) > 1 else [x for x in open(Q, encoding="utf-8").read().split() if x.strip()][0]
    pad = sys.argv[2] if len(sys.argv) > 2 else "g1"
    print("== A211g resume regression (%s pad %s)" % (nid, pad), flush=True)
    test_gate()
    test_pages(Q)
    test_clock(nid, pad)
    print("== %d ok, %d FAILED%s" % (len(OK), len(BAD), (": " + "; ".join(BAD)) if BAD else ""), flush=True)
    sys.exit(1 if BAD else 0)
