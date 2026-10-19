"""Independent replay of `CaptureSummary.summaryCheck Chunk0164.table Chunk0164.E summaryTargets`.

Follows the text of Sq17Lean/CaptureSummaryFast.lean and HalfPlaneCoverFast.impliedOK:
for every owner i < 17 and every live row r of E[i] whose entry index is in the table,
require target_i.lo <= e.lo, e.hi <= target_i.hi, and every target half-plane c to be
implied by r.cons, i.e. findUpper r.cons c.a c.b = some (N, d) with N <= c.q * d.
  python3 -I summary_check.py CHUNK0164_DATA.lean CaptureSummaryTargetsFast.lean [--perturb]
"""
import re
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hpfast as H  # noqa: E402

data = Path(sys.argv[1]).read_text()
tt = Path(sys.argv[2]).read_text()
perturb = "--perturb" in sys.argv


def decodeEntries(a):
    out = []
    p = 0
    while p + 11 <= len(a):
        out.append(dict(lo=F(a[p], a[p + 1]), hi=F(a[p + 2], a[p + 3]), C=a[p + 4], S=a[p + 5],
                        cd=a[p + 6], H=a[p + 7], hd=a[p + 8], span=F(a[p + 9], a[p + 10])))
        p += 11
    return out


T = decodeEntries(H.parseInts(re.search(r'def tableRaw : String := "([^"]*)"', data).group(1)))
E = H.decodeInit(H.parseInts(re.search(r'def finalRaw : String := "([^"]*)"', data).group(1)), [[] for _ in range(17)])

targets = []
for i in range(17):
    m = re.search(rf"def target{i} : Target := ⟨\(?(-?\d+(?:/\d+)?)\)?,\(?(-?\d+(?:/\d+)?)\)?,\[(.*?)\]⟩", tt)
    lo, hi, cons = H.rat(m.group(1)), H.rat(m.group(2)), []
    for c in re.finditer(r"⟨\(?(-?\d+)\)?,\(?(-?\d+)\)?,\(?(-?\d+)\)?⟩", m.group(3)):
        cons.append((int(c.group(1)), int(c.group(2)), int(c.group(3))))
    targets.append((lo, hi, cons))
order = re.search(r"def summaryTargets : Array Target := #\[(.*?)\]", tt, re.S)
print("summaryTargets order:", order.group(1).replace("\n", " ").strip()[:120] if order else "NOT FOUND")

if perturb:
    lo, hi, cons = targets[3]
    targets[3] = (lo, hi - F(1, 10**12), cons)  # shrink one angle target by 1e-12
    print("perturbation: target3.hi lowered by 1e-12")


def impliedOK(cons, c):
    r = H.findUpper(cons, c[0], c[1])
    return r is not None and r[0] <= c[2] * r[1]


def rowCheck(target, r):
    if r[2] >= len(T):
        return True
    e = T[r[2]]
    lo, hi, cons = target
    return lo <= e["lo"] and e["hi"] <= hi and all(impliedOK(r[0], c) for c in cons)


ok = len(E) == 17 and len(targets) == 17
fails = []
for i in range(17):
    for k, r in enumerate(H.rowsOf(E, i)):
        if not rowCheck(targets[i], r):
            fails.append((i, k))
ok = ok and not fails
print(f"table {len(T)} entries; E rows per owner {[len(r) for r in E]}; targets {len(targets)}, "
      f"half-planes per target {[len(t[2]) for t in targets]}")
print(f"failing (owner,row): {fails[:6]}")
print(f"summaryCheck replayed = {ok}")
