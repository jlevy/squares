"""Independent replay of `CaptureTableFast.freshCheck 44 table previousEntryIds.size freshBounds`.

Reads a chunk Data file (tableRaw, previousEntryIds) and its Checks file (freshBoundsRaw),
decodes both as CaptureTableFast.decodeEntries / decodeBounds do (11 and 16 integers per
item), and re-evaluates entryCheck at degree 44 with exact Fractions, following the text of
Sq17Lean/CaptureTableFast.lean (read, not executed).
  python3 -I table_check.py CHUNK_DATA.lean CHUNK_CHECKS.lean
"""
import re
import sys
from fractions import Fraction as F
from math import factorial
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hpfast as H  # noqa: E402

data = Path(sys.argv[1]).read_text()
checks = Path(sys.argv[2]).read_text()
name = re.search(r"^namespace (\S+)", data, re.M).group(1).split(".")[-1]
tableRaw = re.search(r'def tableRaw : String := "([^"]*)"', data).group(1)
prev = re.search(r"def previousEntryIds : Array Nat := #\[([^\]]*)\]", data).group(1)
offset = len([t for t in prev.split(",") if t.strip()])
freshRaw = re.search(r'def freshBoundsRaw : String := "([^"]*)"', checks).group(1)


def decodeEntries(a):
    out = []
    p = 0
    while p + 11 <= len(a):
        out.append(dict(lo=F(a[p], a[p + 1]), hi=F(a[p + 2], a[p + 3]), C=a[p + 4], S=a[p + 5],
                        cd=a[p + 6], H=a[p + 7], hd=a[p + 8], span=F(a[p + 9], a[p + 10])))
        p += 11
    return out


def boundsAt(a, p):
    return dict(cosLo=F(a[p], a[p + 1]), cosHi=F(a[p + 2], a[p + 3]),
                sinLo=F(a[p + 4], a[p + 5]), sinHi=F(a[p + 6], a[p + 7]))


def decodeBounds(a):
    out = []
    p = 0
    while p + 16 <= len(a):
        out.append((boundsAt(a, p), boundsAt(a, p + 8)))
        p += 16
    return out


N = 44


def taylor(x):
    c = s = F(0)
    for k in range(N + 1):
        term = x ** k / factorial(k)
        if k % 4 == 0:
            c += term
        elif k % 4 == 1:
            s += term
        elif k % 4 == 2:
            c -= term
        else:
            s -= term
    return c, s


def remainder(x):
    return abs(x) ** (N + 1) / factorial(N + 1)


def trigCheck(x, b):
    c, s = taylor(x)
    r = remainder(x)
    return b["cosLo"] <= c - r and c + r <= b["cosHi"] and b["sinLo"] <= s - r and s + r <= b["sinHi"]


def endpoint(c, s, b):
    dLo = min(c * b["cosLo"], c * b["cosHi"]) + min(s * b["sinLo"], s * b["sinHi"])
    dHi = max(c * b["cosLo"], c * b["cosHi"]) + max(s * b["sinLo"], s * b["sinHi"])
    xLo = min(c * b["sinLo"], c * b["sinHi"]) + min(-s * b["cosLo"], -s * b["cosHi"])
    xHi = max(c * b["sinLo"], c * b["sinHi"]) + max(-s * b["cosLo"], -s * b["cosHi"])
    return dLo, dHi, xLo, xHi


def endpointCheck(h, ep):
    dLo, dHi, xLo, xHi = ep
    mx = max(abs(xLo), abs(xHi))
    return h >= 0 and dLo > 0 and dLo <= dHi and xLo <= xHi and mx <= dLo and h * (dHi + mx) <= 1


def entryCheck(e, b):
    b1, b2 = b
    c = F(e["C"], e["cd"]); s = F(e["S"], e["cd"]); h = F(e["H"], e["hd"])
    d = (F(1), F(1)) if e["lo"] >= 0 else ((F(1), F(-1)) if e["hi"] <= 0 else (F(0), F(0)))
    ok = trigCheck(e["lo"], b1) and trigCheck(e["hi"], b2)
    ok = ok and 0 <= e["hi"] - e["lo"] <= 1
    ok = ok and endpointCheck(h, endpoint(c, s, b1)) and endpointCheck(h, endpoint(c, s, b2))
    ok = ok and abs(d[0]) <= 1 and abs(d[1]) <= 1 and e["span"] >= 0 and e["lo"] <= e["hi"] and e["hi"] - e["lo"] <= 1
    ok = ok and e["span"] <= endpoint(d[0], d[1], b1)[0] and e["span"] <= endpoint(d[0], d[1], b2)[0]
    return ok


T = decodeEntries(H.parseInts(tableRaw))
B = decodeBounds(H.parseInts(freshRaw))
fresh = T[offset:]
print(f"{name}: table {len(T)} entries, previousEntryIds.size = {offset}, fresh {len(fresh)}, bounds {len(B)}")
if offset > len(T):
    print("freshCheck replayed = False (offset > size)")
    sys.exit(1)
bad = []
for j, e in enumerate(fresh):
    if j >= len(B) or not entryCheck(e, B[j]):
        bad.append(offset + j)
ok = len(bad) == 0
print(f"{name}: failing fresh entries: {bad[:8]}")
print(f"{name}: angle range [{float(min(e['lo'] for e in T)):.9f}, {float(max(e['hi'] for e in T)):.9f}], "
      f"max width {float(max(e['hi']-e['lo'] for e in T)):.3e}, min core h {float(min(F(e['H'],e['hd']) for e in T)):.6f}, "
      f"min span {float(min(e['span'] for e in T)):.6f}")
print(f"freshCheck 44 replayed = {ok}")
