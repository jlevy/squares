"""Independent replay of `runToCheck table side shift S0 steps E` on one chunk file.

Re-implements CaptureTableFast.decodeEntries (11 integers per entry) and
CaptureRunFast.runToCheck (run every step with the HalfPlaneFast step semantics,
then require exact equality of the resulting state with the declared end state E),
using the checker functions in hpfast.py, which were lifted from the text of
Sq17Lean/HalfPlaneFast.lean.  Usage:
  python3 -I chunk_replay.py CHUNK_DATA.lean
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hpfast as H  # noqa: E402

path = Path(sys.argv[1])
text = path.read_text()
ns = re.search(r"^namespace (\S+)", text, re.M).group(1)
name = ".".join(ns.split(".")[-2:])

side = H.rat(re.search(r"def side : Rat := \((-?\d+/\d+) : Rat\)", text).group(1))
shift = H.rat(re.search(r"def shift : Rat := \((-?\d+/\d+) : Rat\)", text).group(1))
tableRaw = re.search(r'def tableRaw : String := "([^"]*)"', text).group(1)
initRaw = re.search(r'def initRaw : String := "([^"]*)"', text).group(1)
stepsRaw = re.search(r'def stepsRaw : String := "([^"]*)"', text).group(1)
finalRaw = re.search(r'def finalRaw : String := "([^"]*)"', text).group(1)
owners = int(re.search(r"List\.replicate (\d+) \[\]", text).group(1))


def decodeEntries(a):
    out = []
    p = 0
    while p + 11 <= len(a):
        out.append(dict(lo=H.F(a[p], a[p + 1]), hi=H.F(a[p + 2], a[p + 3]), C=a[p + 4], S=a[p + 5],
                        cd=a[p + 6], H=a[p + 7], hd=a[p + 8], span=H.F(a[p + 9], a[p + 10])))
        p += 11
    return out


T = decodeEntries(H.parseInts(tableRaw))
S0 = H.decodeInit(H.parseInts(initRaw), [[] for _ in range(owners)])
E = H.decodeInit(H.parseInts(finalRaw), [[] for _ in range(owners)])
steps = H.decodeSteps(H.parseInts(stepsRaw))
kinds = {}
for st in steps:
    kinds[st[0]] = kinds.get(st[0], 0) + 1
print(f"{name}: side-L? side={float(side):.17g} shift={float(shift):.3e} table {len(T)} entries, owners {owners}")
print(f"{name}: S0 rows {[len(r) for r in S0]}, E rows {[len(r) for r in E]}, steps {len(steps)} {kinds}")

S = S0
for n, st in enumerate(steps):
    S2 = H.run_step(T, side, shift, S, st)
    if S2 is None:
        print(f"{name}: step {n} ({st[0]}) REJECTED by the replayed checker -> runToCheck = False")
        sys.exit(1)
    S = S2
same = (S == E)
print(f"{name}: all {len(steps)} steps accepted; final rows {[len(r) for r in S]}; R == E exactly: {same}")
if not same:
    for i in range(owners):
        if S[i] != E[i]:
            print(f"  owner {i}: replay rows {len(S[i])} vs declared {len(E[i])}")
            break
print(f"runToCheck replayed = {same}")
