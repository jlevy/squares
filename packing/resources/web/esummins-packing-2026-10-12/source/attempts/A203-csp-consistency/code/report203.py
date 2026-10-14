"""A203 -- the table over the pages (results/csp203.jsonl vs A202's fast30.jsonl): per page and pad, A202's stage-0 /
stage-1 verdicts and A203's verdict with the CSP numbers (units alive, dead rows by rule, settle kills, ms per step).
    python report203.py            -> prints the markdown table (stdout) and writes results/report203.md"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def jl(p):
    out = []
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


def main():
    a202 = {}
    for d in jl(os.path.join(ROOT, "attempts", "A202-fast30", "results", "fast30.jsonl")):
        a202[(d.get("nid"), d.get("pad"), d.get("stage"))] = d
    a203 = {}
    for d in jl(os.path.join(HERE, "..", "results", "csp203.jsonl")):
        a203[(d.get("nid"), d.get("pad"))] = d
    nids = sorted({k[0] for k in a203})
    rows = ["| page | pad | A202 s0 / s1 | A203 (s) | H units -> alive | dead rows H / F | mutual clip | settle kills | count prunes mask / pair | CSP ms build / masks / settle | forced H |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
    kills = []
    for n in nids:
        for pad in ("g1", "zero"):
            d = a203.get((n, pad))
            if not d:
                continue
            s0 = (a202.get((n, pad, 0)) or {}).get("verdict", "-")
            s1 = (a202.get((n, pad, 1)) or {}).get("verdict", "-")
            csp = d.get("csp") or []
            c1 = csp[0] if csp else {}
            nH = sum(1 for r in csp for x in (r.get("dead_opts") or []) if x.get("rule") == "H")
            nF = sum(1 for r in csp for x in (r.get("dead_opts") or []) if x.get("rule") == "F")
            mc = {}
            for r in csp:
                for k, v in (r.get("dead_unit_count") or {}).items():
                    mc[k] = mc.get(k, 0) + v
            sk = {}
            for r in csp:
                for k, v in ((r.get("settle") or {}).get("kills") or {}).items():
                    sk[k] = sk.get(k, 0) + v
            ms = c1.get("ms") or {}
            prunes = {}
            last = None
            for r in (d.get("rounds") or []):
                last = r
            v = d.get("verdict")
            rows.append("| %s | %s | %s / %s | **%s** (%.0f) | %s -> %s | %d / %d | %s | %s | %s | %s / %s / %s | %s |" % (
                n.replace("_interior", ""), pad, s0, s1, v, float(d.get("seconds") or 0), c1.get("n_units", "-"), (csp[-1] if csp else {}).get("alive_units", "-"),
                nH, nF, ",".join("%s:%d" % (k.split(":")[1], v_) for k, v_ in sorted(mc.items())) or "-",
                ",".join("%s:%d" % (k, v_) for k, v_ in sorted(sk.items()) if v_) or "-",
                "-", ms.get("build", "-"), ms.get("masks", "-"), ms.get("settle", "-"), ",".join(d.get("forced_H") or []) or "-"))
            if v == "DEAD":
                kills.append((n, pad, (d.get("leaf") or "")[:200]))
    txt = "\n".join(rows) + "\n\nKILLS:\n" + "\n".join("- %s %s: %s" % k for k in kills) + "\n"
    print(txt)
    open(os.path.join(HERE, "..", "results", "report203.md"), "w", encoding="utf-8").write(txt)


if __name__ == "__main__":
    main()
