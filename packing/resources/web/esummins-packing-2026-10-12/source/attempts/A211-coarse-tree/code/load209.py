"""A209 -- the page loader for BOTH populations, installed over A198's FP.load_page at run time (the library's Stage0 /
QPage / load206 all call FP.load_page(nid)):
  * a gallery page (docs/shadows/a57v4/review_a57v4.csv, A198's loader, unchanged);
  * an A57 tree record: nid = <id> for the G1 family, <id>__L1 for the L1 family (the same id is a DIFFERENT node in the
    two families -- A137 C.3), the record attempts/A57-shadow-trees/results/tree/<tree>/<id>.json in the record format
    geo178.load_record reads (hyp.boxes / hyp.cores: the class pins + H's box); an alive row with no record file on
    disk is rebuilt from its tree jsonl row (H = the row's `box`, the pins = the family's NO record's pins, which every
    node of the tree shares: the same hypothesis format, a synthesised record).
census(): the alive k5 frontier (A156 state156's rule: ALIVE / FAIL rows, the STRONGEST verdict per id, minus the ids a
supersession ledger or an ancestor's kill closes -- Lemma K1 -- and minus the gallery kills), deepest-first per tree."""
import collections
import csv
import glob
import json
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ATT = os.path.join(ROOT, "attempts")
A57 = os.path.join(ATT, "A57-shadow-trees", "results")
LEDGER = os.path.join(HERE, "..", "results", "superseded_by_k5killer_A209.jsonl")
for _p in (os.path.join(ATT, "A198-fastprop", "code"), os.path.join(ATT, "A178-gallery-geometry", "code")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import fastprop as FP                                          # noqa: E402  READ-ONLY (A198)
import geo178 as G                                             # noqa: E402  READ-ONLY (A178)

_ORIG = FP.load_page
CSV = os.path.join(ROOT, "docs", "shadows", "a57v4", "review_a57v4.csv")
RANK = {"PASS": 0, "logic kill": 1, "parent box": 2, "CANARY": 3, "skipped": 4, "ALIVE": 5, "FAIL": 6, "other": 7}
_TREES = None


def jl(p):
    out = []
    if os.path.exists(p):
        for ln in open(p, encoding="utf-8"):
            ln = ln.strip()
            if ln:
                try:
                    out.append(json.loads(ln))
                except Exception:
                    pass
    return out


def verdict_of(rec):
    c = str(rec.get("cert") or "")
    for pre, name in (("PASS", "PASS"), ("KILL-BY-LOGIC", "logic kill"), ("ALIVE", "ALIVE"), ("FAIL", "FAIL"),
                      ("UNSOUND", "parent box"), ("CANARY", "CANARY"), ("SKIPPED", "skipped")):
        if c.startswith(pre):
            return name
    return "other"


def trees():
    """tree key -> {id: (verdict, row)} over A57's k5 tree jsonls (strongest verdict per id)."""
    global _TREES
    if _TREES is None:
        T = collections.defaultdict(dict)
        for p in sorted(glob.glob(os.path.join(A57, "tree_k5_*.jsonl"))):
            key = os.path.basename(p)[5:].rsplit("_s", 1)[0].replace(".jsonl", "")
            for r in jl(p):
                if "id" not in r:
                    continue
                v = verdict_of(r)
                cur = T[key].get(r["id"])
                if cur is None or RANK[v] < RANK[cur[0]]:
                    T[key][r["id"]] = (v, r)
        _TREES = dict(T)
    return _TREES


def split_nid(nid):
    """-> (id, family): 'k5_11_interior_Y0041_D00' -> G1; 'k5_16_interior_Y0083__L1' -> L1."""
    fam = "G1"
    if "__" in nid:
        nid, fam = nid.split("__", 1)
    return nid, fam


def tree_key(nid):
    i, fam = split_nid(nid)
    cls = i.split("_interior")[0]
    return "%s_interior_%s" % (cls, fam) + "_D2" * i.count("_D"), i


def record_path(nid):
    key, i = tree_key(nid)
    return os.path.join(A57, "tree", key, i + ".json"), key, i


def pins_of_family(key):
    """the family's pins (from its NO record, hyp.boxes with th0 == th1): shared by every node of the tree."""
    fam = key.split("_D2")[0]
    cls = fam.split("_interior")[0]
    f = os.path.join(A57, "tree", fam, "%s_interior_NO.json" % cls)
    return G.load_record(os.path.relpath(f, ROOT))["pins"]


def synth_record(nid):
    """a record for an alive row without a file: H = the row's box, the pins = the family's."""
    key, i = tree_key(nid)
    v, row = trees()[key][i]
    b = row["box"]
    H = (float(b["x0"]), float(b["x1"]), float(b["y0"]), float(b["y1"]), float(b["th0"]), float(b["th1"]))
    return dict(pins=pins_of_family(key), H=[H], budget=row.get("budget"), s=float(Fr(str(row.get("side") or G.S0))), synthesised=True)


def load_page(nid, csv_path=None):
    """(rec, cls, row) for a gallery nid or a tree nid (see the module doc)."""
    try:
        if "__" not in nid:
            return _ORIG(nid, csv_path)
    except KeyError:
        pass
    path, key, i = record_path(nid)
    if os.path.exists(path):
        rec = G.load_record(os.path.relpath(path, ROOT))
        src = os.path.relpath(path, ROOT).replace("\\", "/")
    else:
        rec = synth_record(nid)
        src = "tree_%s.jsonl row (synthesised: box + the family's pins)" % key
    cls = G.class_of_record(rec)
    v, r = trees().get(key, {}).get(i, (None, {}))
    row = dict(node=nid, camp="A57", cls=cls, level=str(1 + i.count("_D")), family=r.get("family") or "", record=src, tree=key,
               tau=(r.get("tau") if r.get("tau") is not None else 0.0), budget=r.get("budget"), verdict=r.get("cert"), a57_verdict=v)
    return rec, cls, row


def install():
    FP.load_page = load_page


def gallery_nids():
    return [r["node"] for r in csv.DictReader(open(CSV, encoding="utf-8")) if r["node"].startswith("k5_")]


def dead_ids():
    """ids closed by a supersession ledger (A137 / A96 / A149 / A209's own) or by a killed gallery page."""
    dead = set()
    for f in glob.glob(os.path.join(A57, "superseded_by_*.jsonl")) + glob.glob(os.path.join(ATT, "A149-a57-reprice", "results", "superseded_by_*.jsonl")) + [LEDGER]:
        for r in jl(f):
            if "id" in r and not str(r.get("camp", "A57")).startswith("A60"):
                dead.add((r["id"], tuple(r.get("applies_to_tags") or [])))
    for f in glob.glob(os.path.join(ROOT, "docs", "shadows", "a57v4", "killed", "k5_*.svg")):
        dead.add((os.path.basename(f)[:-4], ()))
    return dead


def is_dead(i, key, dead):
    parts = i.split("_D")
    for n in range(len(parts), 0, -1):
        a = "_D".join(parts[:n])
        for d, tags in dead:
            if d == a and (not tags or key in tags):
                return True
    return False


def census():
    """the alive k5 frontier as [(nid, tree key, depth, a57 verdict, record on disk)], deepest-first within a tree."""
    dead = dead_ids()
    out = []
    for key, ids in trees().items():
        fam = "L1" if "_L1" in key else "G1"
        for i, (v, r) in ids.items():
            if v not in ("ALIVE", "FAIL") or is_dead(i, key, dead):
                continue
            nid = i if fam == "G1" else i + "__L1"
            out.append(dict(nid=nid, tree=key, depth=i.count("_D"), a57=v, cert=str(r.get("cert") or "")[:60],
                            on_disk=os.path.exists(os.path.join(A57, "tree", key, i + ".json"))))
    out.sort(key=lambda d: (d["tree"].split("_D2")[0], -d["depth"], d["nid"]))
    return out


if __name__ == "__main__":
    c = census()
    by = collections.Counter(d["tree"] for d in c)
    print("alive k5 frontier: %d nodes; %s" % (len(c), dict(by)))
    if len(sys.argv) > 1:
        rec, cls, row = load_page(sys.argv[1])
        print(cls, row, rec["H"], len(rec["pins"]))
