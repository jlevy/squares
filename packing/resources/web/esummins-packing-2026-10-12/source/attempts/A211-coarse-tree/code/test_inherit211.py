"""A211f -- REGRESSION TEST for the start-node loader: run inherit211's merge over EVERY page's certificates (both
pads) and check that every start node's replay steps are branch dicts the tree's own appliers accept.

The bug this pins (A211e, k5_11_interior_Y0036_D07 R.1.4.3.1.2 / R.1.4.3.2): a Lemma ROLE-SPLIT record writes
`branch_rows = ["t<=53.1301", "t>=53.1301"]` (printable labels, one string per branch), and inherit211.branches_of
read each label as a list of ROW INDICES -- `list("t<=53.1301")` -> ten one-character "rows" -- so startload211 sent
them to tree205b.apply_branch and died with TypeError('list indices must be integers or slices, not str'), leaving the
page ALIVE for a reason that has nothing to do with the geometry.

  python test_inherit211.py            # static check over every page and pad (fast)
  python test_inherit211.py --load     # ... and actually LOAD every start node (A211h: the loader must climb to
                                       #     the nearest COMPLETE ancestor rather than refuse a capped snapshot)
  python test_inherit211.py --load --rsplit-only   # ... only the start nodes carrying a role split (the A211f case)
"""
import argparse
import os
import sys
import re
import time
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ATT = os.path.join(ROOT, "attempts")
KINDS = ("row", "pair", "row-anon", "ns-meets", "ns-misses", "pocket", "rsplit", "inherited")
TAG = re.compile(r"_w\d+[a-z0-9]*$")


def pages():
    """every page id any campaign in the chain wrote a tree certificate for."""
    out = set()
    for d, pre in ((os.path.join(ATT, "A205-clip-tree", "certs"), "cliptree205_"),
                   (os.path.join(ATT, "A205-clip-tree", "certs", "extended"), "cliptree205_"),
                   (os.path.join(ATT, "A206-named-split", "certs"), "namedsplit206_"),
                   (os.path.join(ATT, "A209-k5-killer", "certs"), "k5killer209_"),
                   (os.path.join(ATT, "A211-coarse-tree", "certs"), "coarsetree211_")):
        for f in (sorted(os.listdir(d)) if os.path.isdir(d) else []):
            if f.startswith(pre) and f.endswith(".json"):        # A211h: an EXTENDED cert is <nid>_w<wall><variant>,
                out.add(TAG.sub("", f[len(pre):-5].split("__")[0]))   # not a page of its own (load_page would KeyError)
    return sorted(out)


def check_step(br):
    """-> [] when this replay step is a branch dict startload211.apply_step can apply, else the reasons it is not."""
    bad, kind = [], str(br.get("kind") or "")
    if kind not in KINDS:
        bad.append("unknown kind %r" % kind)
    if kind == "rsplit":                                          # rsplit211.apply_rsplit reads role / dim / side / m
        if not br.get("role"):
            bad.append("rsplit without a role")
        if br.get("dim") not in ("x", "y", "t"):
            bad.append("rsplit dim %r" % br.get("dim"))
        if br.get("side") not in ("lo", "hi"):
            bad.append("rsplit side %r" % br.get("side"))
        try:
            Fr(str(br.get("m")))
        except (ValueError, ZeroDivisionError, TypeError):
            bad.append("rsplit m %r is not a rational" % br.get("m"))
        if not (isinstance(br.get("rows"), list) and len(br["rows"]) == 1 and isinstance(br["rows"][0], str)):
            bad.append("rsplit rows %r (want one label)" % (br.get("rows"),))
    elif kind == "pocket":                                        # tree209.apply_pocket reads pocket / rows[0]
        pk = br.get("pocket")
        if not (isinstance(pk, (list, tuple)) and len(pk) >= 4 and all(isinstance(v, (int, float)) for v in pk)):
            bad.append("pocket %r" % (pk,))
        if not (isinstance(br.get("rows"), list) and br["rows"] and isinstance(br["rows"][0], int)):
            bad.append("pocket rows %r" % (br.get("rows"),))
    elif kind.startswith("ns-"):                                  # tree206.apply_ns reads role / slot
        if not br.get("role") or not br.get("slot"):
            bad.append("ns step without role / slot")
    else:                                                         # tree205b.apply_branch indexes pg.cells with rows
        if not br.get("slot"):
            bad.append("row step without a slot")
        rows = br.get("rows")
        if not (isinstance(rows, list) and rows and all(isinstance(r, int) and not isinstance(r, bool) for r in rows)):
            bad.append("row step rows %r are not cell indices" % (rows,))
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pads", default="zero,g1")
    ap.add_argument("--load", action="store_true", help="also run startload211 on every start node (A211h)")
    ap.add_argument("--rsplit-only", dest="rsplit_only", action="store_true",
                    help="--load only the start nodes that carry a role split (the A211f regression)")
    ap.add_argument("--nid", default=None)
    a = ap.parse_args()
    import inherit211 as INH
    quiet = lambda *_a, **_k: None                                # noqa: E731
    nids = [a.nid] if a.nid else pages()
    n_merge = n_start = n_step = n_rs = 0
    errs, loadable = [], []
    t0 = time.time()
    for nid in nids:
        for pad in a.pads.split(","):
            try:
                import stage209
                start = stage209.start_of(nid, pad)
            except Exception as e:                                # noqa: BLE001
                errs.append((nid, pad, "-", "stage209.start_of: %r" % (e,)))
                continue
            try:
                M = INH.merge(nid, pad, start.get("file"), log=quiet)
            except Exception as e:                                # noqa: BLE001
                errs.append((nid, pad, "-", "merge: %r" % (e,)))
                continue
            n_merge += 1
            if not M:
                continue
            for sn in M["starts"]:
                n_start += 1
                rs = False
                for br in sn["steps"]:
                    n_step += 1
                    rs = rs or br.get("kind") == "rsplit"
                    for why in check_step(br):
                        errs.append((nid, pad, sn["label"], why))
                n_rs += rs
                if rs or not a.rsplit_only:
                    loadable.append((nid, pad, sn, start))
    print("MERGE   %d pages x %d pads -> %d merges, %d start nodes, %d replay steps (%d start nodes carry a role split)"
          % (len(nids), len(a.pads.split(",")), n_merge, n_start, n_step, n_rs))
    print("ERRORS  %d" % len(errs))
    for e in errs[:40]:
        print("   %s pad %s start %s: %s" % e)
    if a.load:
        import load211
        load211.install()
        import poly204 as P
        import coarse211 as C11
        import startload211 as SL
        C11.install()
        n_ok, n_root, n_climb, refused = 0, 0, 0, []
        for nid, pad, sn, start in loadable:
            T = P.FP.Trace(wall=10 ** 9)
            rec, cls, _row = P.FP.load_page(nid)
            try:
                _pg, meta = SL.load(sn, rec, cls, nid, T, pad, start, [], rounds=1, log=quiet)
                lf = meta.get("loaded_from") or {}
                n_ok += 1
                n_root += lf.get("mode") == "a203_root"
                n_climb += bool(lf.get("climbed"))
            except Exception as e:                                # noqa: BLE001
                refused.append((nid, pad, sn["label"], repr(e)))
                errs.append((nid, pad, sn["label"], "load: %r" % (e,)))
                print("   LOAD FAIL %s pad %s %s: %r" % (nid, pad, sn["label"], e))
        print("LOAD    %d / %d start nodes loaded (%d climbed past a capped / missing snapshot, %d replayed from the "
              "A203 stage-0 root); %d REFUSED" % (n_ok, len(loadable), n_climb, n_root, len(refused)))
        for r in refused:
            print("   REFUSED %s pad %s %s: %s" % r)
    print("%s in %.1f s" % ("PASS" if not errs else "FAIL (%d)" % len(errs), time.time() - t0))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
