"""A211 -- the DEAD leaves not yet audited (python audit_queue211.py [--nid <nid>]; logs/audit_done.txt): '<nid> <run key> <leaf>' per line (inherited and stage-0 kills excluded)."""
import glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DONE = os.path.join(HERE, "..", "logs", "audit_done.txt")
only = sys.argv[sys.argv.index("--nid") + 1] if "--nid" in sys.argv else None
done = set(l.strip() for l in open(DONE, encoding="utf-8")) if os.path.exists(DONE) else set()
for f in sorted(glob.glob(os.path.join(HERE, "..", "certs", "coarsetree211_%s.json" % (only or "*")))):
    try:
        c = json.load(open(f, encoding="utf-8"))
    except Exception:
        continue
    for key, d in (c.get("runs") or {}).items():
        if d.get("verdict") not in ("DEAD", "ALIVE"):
            continue
        for n in d.get("nodes") or []:
            if n.get("verdict") == "DEAD" and n.get("kind") != "inherited" and n.get("clip"):
                line = "%s %s %s" % (c["nid"], key, n["label"])
                if line not in done:
                    print(line)
