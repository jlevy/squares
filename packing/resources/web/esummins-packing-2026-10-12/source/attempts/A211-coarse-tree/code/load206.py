"""A209 COPY of A206 load206 (df5aebc9, unchanged; FP.load_page is A209's load209.load_page at run time). A206 -- load a node of an A205 clip tree from its certificate (the node's LAST snapshot: every role's pieces after that
node's last fixed point, rounded to 7 decimals / 4 tilt decimals in the certificate and padded OUTWARD here, so the loaded
node is a SUPERSET of the recorded one: sound), with its forced slots, role slots, pinned cells and corners; a snapshot
with more pieces than recorded (the 300-piece cap) is refused."""
import json
import os
from fractions import Fraction as Fr

import poly204 as P
import tree206 as N6

FP, MB = P.FP, P.MB
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
CERTS205 = os.path.join(ROOT, "attempts", "A205-clip-tree", "certs")
EPS_R = Fr(1, 10 ** 6)
EPS_D = 0.001


def cert_path(nid, src="standard", tag=""):
    if src == "extended":
        return os.path.join(CERTS205, "extended", "cliptree205_%s%s.json" % (nid, tag or "_w3600"))
    if src == "a206":                                             # a node of an A206 run (tag = the run key, e.g. g1_tree)
        return os.path.join(HERE, "..", "certs", "namedsplit206_%s.json" % nid)
    return os.path.join(CERTS205, "cliptree205_%s.json" % nid)


def pad_piece(p6):
    x0, x1, y0, y1, d0, d1 = p6
    rect = (Fr(x0) - EPS_R, Fr(x1) + EPS_R, Fr(y0) - EPS_R, Fr(y1) + EPS_R)
    return (MB.Bin(MB.t_lo(max(0.0, d0 - EPS_D)), MB.t_hi(min(90.0, d1 + EPS_D))), rect)


def find_node(doc, pad, leaf, src="standard", tag=""):
    d = doc["runs"][tag] if src == "a206" else doc["pads"][pad]
    for n in d.get("nodes") or []:
        if n.get("label") == leaf:
            return d, n
    raise KeyError("leaf %s not in %s pad %s" % (leaf, doc["nid"], pad))


def load_node(nid, pad, leaf, T, src="standard", tag=""):
    """-> (page, meta): a TreePage206 at the recorded node (before any cascade), and what was loaded."""
    f = cert_path(nid, src, tag)
    doc = json.load(open(f, encoding="utf-8"))
    d, node = find_node(doc, pad, leaf, src, tag)
    snap = node.get("snapshot")
    if not snap:
        raise ValueError("node %s has no snapshot" % leaf)
    start = P.load_start(nid, pad)
    rec, cls, row = FP.load_page(nid)
    pg = N6.TreePage206(rec, cls, nid, T, pad=pad, start=start)
    loaded = {}
    for k, v in snap["roles"].items():
        if k.startswith("P"):
            continue
        if v.get("n_pieces", 0) > len(v.get("pieces") or []):
            raise ValueError("role %s: snapshot holds %d of %d pieces (capped): cannot load soundly" % (k, len(v["pieces"]), v["n_pieces"]))
        pcs = [pad_piece(p6) for p6 in v["pieces"]]
        pg.pieces[k] = pcs
        pg.roles[k] = P.hull_box(pcs)
        pg.vol_record[k] = P.vol(pcs)
        loaded[k] = dict(n_pieces=len(pcs), box=FP.rect_f(pg.roles[k]), recorded_box=v.get("box"), kept_recorded=v.get("kept"))
    pg.forced_H = set(node.get("forced_H") or [])
    pg.role_slots = {k: tuple(v) for k, v in (node.get("role_slots") or {}).items()}
    pg.role_cell = {k: int(v) for k, v in (node.get("role_cell") or {}).items()}
    pg.cell_role = {ci: r for r, ci in pg.role_cell.items() if ci >= 0}
    pg.role_corner = {}
    for k, S in pg.role_slots.items():
        for p in S:
            if pg.item[p]["is_corner"]:
                pg.role_corner[k] = pg.item[p]["corner"]
    pg.miss = {k: frozenset(v) for k, v in (node.get("miss") or {}).items()}       # an A206 node: its Rule-NS miss hypotheses
    meta = dict(source=os.path.relpath(f, ROOT).replace("\\", "/"), pad=pad, leaf=leaf, snapshot_round=snap.get("round"), snapshot_label=snap.get("label"),
                recorded=dict(verdict=node.get("verdict"), reason=node.get("reason"), depth=node.get("depth"), seconds=node.get("seconds"),
                              roles=node.get("roles"), kept=node.get("kept"), alive_cells=node.get("alive_cells"), t=node.get("t")),
                path=[dict(label=n["label"], slot=n.get("slot"), rows=n.get("rows"), kind=n.get("kind")) for n in d["nodes"]
                      if n.get("rows") and (leaf == n["label"] or leaf.startswith(n["label"] + ".") or leaf.startswith(n["label"] + "u") or leaf.startswith(n["label"] + "s"))],
                loaded=loaded, forced_H=sorted(pg.forced_H), role_slots={k: list(v) for k, v in pg.role_slots.items()}, role_cell=dict(pg.role_cell),
                role_corner=dict(pg.role_corner), miss={k: sorted(v) for k, v in pg.miss.items()}, padding=dict(rect=float(EPS_R), tilt_deg=EPS_D), start=start,
                doc=dict(cells=doc.get("cells"), slots=doc.get("slots"), wbox_pad=doc.get("wbox_pad"), wbox=doc.get("wbox"), H_record=doc.get("H_record"), cls=doc.get("cls")))
    return pg, meta
