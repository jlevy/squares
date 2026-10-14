"""A243 -- dump nparam243's rebinding report and the remaining-literal scan of the LIVE process (run as a worker task,
so the report is the one the running descent actually uses) -> results/nparam243_n<N>.json."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import nparam243 as NP                                          # noqa: E402

if not NP.CFG["done"]:
    NP.setup(int(sys.argv[1]) if len(sys.argv) > 1 else 17)
R = NP.report()
kinds = {}
for r in R:
    kinds[r[0]] = kinds.get(r[0], 0) + 1
out = dict(n=NP.CFG["n"], s_hi=str(NP.CFG["s_hi"]), s_lo=str(NP.CFG["s_lo"]), counts=kinds, rebindings=R, scan=NP.scan())
json.dump(out, open(os.path.join(HERE, "..", "results", "nparam243_n%d.json" % NP.CFG["n"]), "w", encoding="utf-8"), indent=0)
print(json.dumps(kinds))
