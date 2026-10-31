"""Compare register claim sides, claims.json and ledger.json with certificate headers (think-ikku review)."""
import json, re, sys
from decimal import Decimal, getcontext
from fractions import Fraction as F
import yaml
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from rv_check import read_cert
getcontext().prec = 200
P = sys.argv[1]
R = P + "/resources/web/"
reg = yaml.safe_load(open(P + "/frontier/results.yaml"))
ents = {e["id"]: e for e in reg["results"]} if isinstance(reg, dict) and "results" in reg else None
if ents is None:
    for v in reg.values():
        if isinstance(v, list) and v and isinstance(v[0], dict) and "id" in v[0]:
            ents = {e["id"]: e for e in v}
            break
def tofrac(s):
    s = s.strip().rstrip(",.")
    return F(s) if "/" in s else F(Decimal(s))
for tid, pk, counts in (("T-253", "mishapolk-1023-refinements-2026-10-30", (154,155,183,211,227,236,237,241,271)),
                        ("T-259", "mishapolk-issue846-2026-10-30", (105,130,146,156,229,308))):
    e = ents[tid]
    claimed = {int(n): tofrac(v) for n, v in re.findall(r"s\((\d+)\) <= ([0-9./]+)", e["claim"])}
    cj = json.load(open(R + pk + "/acquisition/claims.json"))
    for n in counts:
        _, side, _ = read_cert(R + pk + f"/source/certificates/0000-0999/n{n}.cert")
        print(tid, n, "register==header", claimed.get(n) == side, "scope", n in e["scope"]["n_values"], e["verification"], e["confirmation"])
    print(tid, "claims.json keys", list(cj)[:8] if isinstance(cj, dict) else type(cj))
led = json.load(open(P + "/campaign/issue-intake/upper-bounds-843-846-20261031/ledger.json"))
print("ledger.json keys", list(led)[:10])
