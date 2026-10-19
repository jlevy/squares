"""A202 report: the per-page table (stage 0 ms / stage 1 s per pad, verdicts, kill leaf) from results/fast30.jsonl and
the certificates; per-rule kill counts and milliseconds per page.  `python report202.py [md]`."""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results", "fast30.jsonl")
CERTS = os.path.join(HERE, "..", "certs")


def load():
    rows = {}
    for line in open(RES, encoding="utf-8"):
        try:
            d = json.loads(line)
        except Exception:
            continue
        if d.get("pad") in ("g1", "zero") and "stage" in d:
            rows[(d["nid"], d["pad"], int(d["stage"]))] = d
    return rows


def table(rows, md=True):
    nids = sorted({k[0] for k in rows})
    out = []
    hdr = "| page | s0 g1 (ms) | s0 pad0 (ms) | s1 g1 (s) | s1 pad0 (s) | verdict | leaf |"
    out.append(hdr)
    out.append("|---|---|---|---|---|---|---|")
    n_dead = 0
    for nid in nids:
        cells = []
        for pad, stage in (("g1", 0), ("zero", 0), ("g1", 1), ("zero", 1)):
            d = rows.get((nid, pad, stage))
            if d is None:
                cells.append("-")
            else:
                v = "%.0f" % (1000 * float(d["seconds"])) if stage == 0 else "%.0f" % float(d["seconds"])
                cells.append(v + (" DEAD" if d["verdict"] == "DEAD" else ""))
        dead = [(k, d) for k, d in rows.items() if k[0] == nid and d["verdict"] == "DEAD"]
        dead.sort(key=lambda kd: (kd[0][1] != "g1", kd[0][2]))
        if dead:
            n_dead += 1
            k, d = dead[0]
            verdict = "DEAD (stage %d, %s pad%s)" % (k[2], k[1], "; s0-only WINDOW-PENDING" if k[1] == "zero" else "")
            leaf = (d.get("leaf") or "")[:110]
        else:
            verdict, leaf = "ALIVE", ""
        out.append("| %s | %s | %s |" % (nid.replace("_interior", ""), " | ".join(cells), verdict + " | " + leaf))
    out.append("")
    out.append("pages %d, dead %d" % (len(nids), n_dead))
    return "\n".join(out)


def rules(nid, pad="g1"):
    f = os.path.join(CERTS, "f30_%s_%s_s0.json" % (nid, pad))
    if not os.path.exists(f):
        return None
    c = json.load(open(f, encoding="utf-8"))
    return c.get("kills"), c.get("seconds"), c.get("caps"), c.get("forced_H")


if __name__ == "__main__":
    rows = load()
    print(table(rows))
    for nid in ("k5_16_interior_Y0044", "k5_16_interior_Y0054", "k5_16_interior_Y0491", "k5_11_interior_Y1110"):
        for pad in ("g1", "zero"):
            r = rules(nid, pad)
            if r:
                print(nid, pad, "%.0f ms" % (1000 * r[1]), " ".join("%s:%d/%.0fms" % (k, v["kills"], v["ms"]) for k, v in r[0].items()), "caps", r[2], "forced", r[3])
