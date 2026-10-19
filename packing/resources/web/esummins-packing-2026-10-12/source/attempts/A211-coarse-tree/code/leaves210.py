"""A210 -- rule CC (Lemma CORNER-COVER, notes/corner_cover.md) applied to the NAMED NODES of A209's clip trees:
for every node of every k5killer209 certificate, in each corner slot c(0,0), take every non-pin role (H or an
instantiated F_j) whose pose classes (the snapshot's per-piece decomposition) sit at that corner, build CC1's band
of each class and test every candidate SECOND meeter of the slot -- the node's alive cells (anonymous) and the other
roles' boxes -- against CC'(b).  A node whose branch instantiated a meeter that cannot reach the band, or all of
whose corner pose classes leave no second meeter at all, is DEAD by Theorem FC
[C: closed-form trace; Lemma CORNER-COVER; no verifier clause], and its whole subtree with it (Lemma K1).
    python leaves210.py [--certs <dir>] [--out <jsonl>] [--nid <nid>]
Rows: results/cornercover210_leaves.jsonl (one per node the rule APPLIES to).  READ-ONLY on A209's files."""
import argparse
import glob
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
import cc210 as CC                                             # noqa: E402

S0 = 969271 / 250000.0
SQ2 = math.sqrt(2.0)
A209 = os.path.join(ROOT, "attempts", "A209-k5-killer", "certs")
OUT = os.path.join(HERE, "..", "results", "cornercover210_leaves.jsonl")


def corner_of(slot):
    return slot[:2]


def is_corner_slot(slot):
    return slot.endswith("(0,0)")


def wmax_of(box):
    """the largest axis width cos t + sin t over the box's tilt interval (concave, so the max is interior)."""
    t0, t1 = float(box[4]), float(box[5])
    lo, hi = min(t0, t1), max(t0, t1)
    if lo <= 45.0 <= hi:
        return SQ2
    return max(math.cos(math.radians(a)) + math.sin(math.radians(a)) for a in (lo, hi))


def role_pieces(node, name, box):
    """the role's alive pose classes at the node: A204/A205's per-piece decomposition from the snapshot when it is
    there (that is where the "near simple square" lives), else the hull box."""
    sn = ((node.get("snapshot") or {}).get("roles") or {}).get(name) or {}
    pcs = sn.get("pieces")
    if pcs:
        return [(tuple(float(v) for v in q[:4]), float(q[4]), float(q[5])) for q in pcs]
    return [(tuple(float(v) for v in box[:4]), float(box[4]), float(box[5]))]


def node_rows(nid, pad, lam, cells, slots, node):
    """the rule on one node: one row per (corner slot, role near that corner) it applies to."""
    roles = {k: v for k, v in (node.get("roles") or {}).items() if not k.startswith("P")}
    rslots = node.get("role_slots") or {}
    alive = node.get("alive_cells") or {}
    out = []
    for p in slots:
        if not is_corner_slot(p):
            continue
        corner = corner_of(p)
        for name, box in sorted(roles.items()):
            bands = CC.piece_bands(role_pieces(node, name, box), corner, S0, lam)
            if not bands:
                continue
            near = [(k, ws) for k, ws in bands if k[2] <= CC.NEAR and k[3] <= CC.NEAR]
            if not near:
                continue
            all_near = len(near) == len(bands)
            allb = [w for _, ws in bands for w in ws]
            if p not in alive:                                                  # the cert does not record the slot's
                continue                                                       # anonymous survivors: no claim
            cand_cells = {int(ci): tuple(float(v) for v in cells[int(ci)]) for ci in (alive.get(p) or [])}
            others = {k: (tuple(float(v) for v in b[:4]), wmax_of(b)) for k, b in roles.items() if k != name}
            dead_cells = [ci for ci, r in cand_cells.items() if not CC.reaches(r, SQ2, allb, lam)] if all_near else []
            dead_roles = [k for k, (r, w) in others.items() if not CC.reaches(r, w, allb, lam)] if all_near else []
            dead_classes = []
            for k, ws in near:
                if any(CC.reaches(r, SQ2, ws, lam) for r in cand_cells.values()):
                    continue
                if any(CC.reaches(r, w, ws, lam) for r, w in others.values()):
                    continue
                dead_classes.append(k)
            named_at_p = [r for r in rslots if p in (rslots.get(r) or []) and r != name]
            contra = [r for r in named_at_p if r in dead_roles]
            verdict, why = "ALIVE", None
            if contra:
                verdict = "DEAD"
                why = ("rule CC: %s is a corner square at %s (Lemma CORNER-COVER), so every other meeter of %s has an "
                       "interior point in the wall wedges; the branch's instantiated meeter(s) %s cannot reach them"
                       % (name, corner, p, contra))
            elif all_near and len(dead_classes) == len(near):
                verdict = "DEAD"
                why = ("rule CC: every pose class of %s at the %s corner (%d of %d) covers the slot cell except the "
                       "wall wedges, and no second non-pin meeter of %s can reach them (%d anonymous cell(s), %d other "
                       "role(s) excluded) -- Theorem FC demands 2" % (name, corner, len(dead_classes), len(bands), p,
                                                                     len(dead_cells), len(dead_roles)))
            out.append(dict(nid=nid, pad=pad, lam=lam, label=node.get("label"), depth=node.get("depth"),
                            node_verdict=node.get("verdict"), slot=p, corner=corner, role=name, all_near=all_near,
                            role_box=[round(float(v), 6) for v in box], n_classes=len(bands), n_near=len(near),
                            dead_classes=len(dead_classes), n_band=len(allb),
                            band=[[round(v, 6) for v in w] for w in allb[:24]],
                            cells_before=sorted(cand_cells), cells_killed=sorted(dead_cells),
                            cells_left=sorted(set(cand_cells) - set(dead_cells)), roles_excluded=sorted(dead_roles),
                            named_meeters=sorted(named_at_p), verdict=verdict, why=why,
                            verifier="[C: closed-form trace; Lemma CORNER-COVER (attempts/A210-corner-cover/notes/"
                                     "corner_cover.md)] -- no verifier clause exists yet"))
    return out


def run_cert(path, out_rows):
    d = json.load(open(path, encoding="utf-8"))
    nid = d["nid"]
    cells = d["cells"]
    slots = d["slots"]
    for run_key, run in sorted((d.get("runs") or {}).items()):
        pad = run.get("pad") or ("zero" if "zero" in run_key else "g1")
        lam = float(run.get("lam") or 1.0)
        if pad == "zero":
            lam = 1.0
        for node in run.get("nodes") or []:
            out_rows += node_rows(nid, pad, lam, cells, slots, node)
    return nid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--certs", default=A209)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--nid", default=None)
    a = ap.parse_args()
    files = sorted(glob.glob(os.path.join(a.certs, "k5killer209_*.json")))
    if a.nid:
        files = [f for f in files if a.nid in os.path.basename(f)]
    rows = []
    t0 = time.time()
    for f in files:
        try:
            run_cert(f, rows)
        except Exception as e:                                                 # a cert being rewritten by A209
            print("   skip %s: %r" % (os.path.basename(f), e), flush=True)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    when = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(a.out, "a", encoding="utf-8") as fh:
        for r in rows:
            r["when"] = when
            fh.write(json.dumps(r, default=str) + "\n")
    dead = [r for r in rows if r["verdict"] == "DEAD"]
    print("A210 leaves: %d cert(s), %d node/slot row(s) where a square is pushed into the corner, %d DEAD by rule CC, %.1f s"
          % (len(files), len(rows), len(dead), time.time() - t0), flush=True)
    for r in dead:
        print("   DEAD %s %s %s %s: %s" % (r["nid"], r["pad"], r["label"], r["slot"], r["why"]), flush=True)
    for r in rows:
        if r["verdict"] != "DEAD" and (r["cells_killed"] or r["dead_classes"] or r["roles_excluded"]):
            print("   clip %s %s %s %s [%s]: %d/%d pose classes dead, cells %s killed (%s left), roles excluded %s" % (
                r["nid"], r["pad"], r["label"], r["slot"], r["role"], r["dead_classes"], r["n_near"],
                r["cells_killed"], r["cells_left"], r["roles_excluded"]), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
