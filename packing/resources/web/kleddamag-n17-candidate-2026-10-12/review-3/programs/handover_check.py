"""Own check of the hand-overs of section 8 (P092-P095): JG tube = G20S window; G20S tube cut by xi_(2,1) <= 0 lies
in the HW window; HW tube cut by xi_(2,1) <= 0 lies in the sixteen-square entry (core 1/200, angles 1/400,
a in [0,8/25], b in [-1/20,1/5], z in [-1/5,3/40]); and the stored acceptance reports of G20S and HW record
exactly the EXPECT windows and tubes.
Usage: python3 -I handover_check.py SRC_ROOT
"""
import json
import os
import sys
from fractions import Fraction as Fr

SRC = sys.argv[1]
W = os.path.join(SRC, "research/window-extension-20261008")
LABELS16 = [i for i in range(1, 18) if i != 4]
fails = []


def check(cond, text):
    print(("OK   " if cond else "FAIL ") + text)
    if not cond:
        fails.append(text)


def expect_region(e):
    core = Fr(e["core"])
    out = {}
    for i in LABELS16:
        iv = [(-core, core), (-core, core)]
        ov = e.get("box", {}).get(str(i), {})
        for k in ("1", "2"):
            if k in ov:
                iv[int(k) - 1] = (Fr(ov[k][0]), Fr(ov[k][1]))
        al = Fr(e["alpha"].get(str(i), e["alpha"]["default"]))
        out[i] = (iv[0], iv[1], al)
    return out


def inside(A, B, cut21=None):
    """region A (with xi_(2,1) additionally cut from above by cut21) lies in region B"""
    ok = True
    for i in LABELS16:
        a1, a2, al = A[i]
        if i == 2 and cut21 is not None:
            a1 = (a1[0], min(a1[1], cut21))
        b1, b2, bl = B[i]
        ok &= b1[0] <= a1[0] and a1[1] <= b1[1] and b2[0] <= a2[0] and a2[1] <= b2[1] and al <= bl
    return ok


G = json.load(open(os.path.join(W, "acceptance/EXPECT_G20S.json")))
H = json.load(open(os.path.join(W, "acceptance/EXPECT_HW.json")))
check(G["labels"] == 16 and H["labels"] == 16 and Fr(G["S_floor"]) == 4 and Fr(H["S_floor"]) == 4, "G20S and HW: sixteen labels, S_floor = 4")
Gw, Gt = expect_region(G["window"]), expect_region(G["tube"])
Hw, Ht = expect_region(H["window"]), expect_region(H["tube"])
# JG tube (terminal of JG_exact_v2.json) versus the G20S window
JG = json.load(open(os.path.join(W, "bigbox/join/JG_exact_v2.json")))
jg = {}
for i in LABELS16:
    b = JG["terminal"]["box"][str(i)]
    jg[i] = ((Fr(b[0][0]), Fr(b[0][1])), (Fr(b[1][0]), Fr(b[1][1])), Fr(JG["terminal"]["alpha"][str(i)]))
check("centre" not in JG["terminal"], "JG tube has no centre map (identity centres, as the G20S window)")
check(all(jg[i] == Gw[i] for i in LABELS16), "JG tube (sixteen labels) equals the G20S window exactly (P092)")
print("   G20S window: core", G["window"]["core"], "alpha", G["window"]["alpha"], "box", G["window"]["box"])
# G20S tube -> HW window with the retained cut xi_(2,1) <= 0
check(inside(Gt, Hw, cut21=Fr(0)), "G20S tube T1 cut by xi_(2,1) <= 0 lies in the HW window (P094)")
check(not inside(Gt, Hw), "without the cut, T1 does not lie in HW (xi_(2,1) up to 1/100): the cut is needed")
# HW tube -> entry
entry = {}
for i in LABELS16:
    entry[i] = ((Fr(-1, 200), Fr(1, 200)), (Fr(-1, 200), Fr(1, 200)), Fr(1, 400))
entry[2] = ((Fr(-8, 25), Fr(0)), (Fr(-1, 200), Fr(1, 200)), Fr(1, 400))          # a = -xi_(2,1) in [0, 8/25]
entry[11] = ((Fr(-1, 200), Fr(1, 200)), (Fr(-1, 5), Fr(1, 20)), Fr(1, 400))       # b = -xi_(11,2) in [-1/20, 1/5]
entry[13] = ((Fr(-1, 200), Fr(1, 200)), (Fr(-1, 5), Fr(3, 40)), Fr(1, 400))       # z = xi_(13,2) in [-1/5, 3/40]
check(inside(Ht, entry, cut21=Fr(0)), "HW tube T2 cut by xi_(2,1) <= 0 lies in the sixteen-square entry (P095)")
check(not inside(Ht, entry), "without the cut, T2 does not lie in the entry (xi_(2,1) up to 1/250): the cut is needed")
print("   HW tube:", H["tube"])
# the stored acceptance reports: what window and tube did the executed trees have?
for name, E in (("G20S", G), ("HW", H)):
    for c in ("C1", "C2"):
        pth = os.path.join(SRC, "local-research/claude-20261002/review/public-edition/path-neutral-20261012/files/research/window-extension-20261008/acceptance/%s_v30_%s.json" % (name, c))
        rep = json.load(open(pth))
        keys = sorted(rep.keys())
        print("   %s %s report keys: %s" % (name, c, keys[:40]))
        hw = rep.get("window") or rep.get("header", {}).get("window")
        if hw is not None:
            print("      report window keys", list(hw.keys()) if isinstance(hw, dict) else type(hw))
        for k in ("result", "status", "verdict", "labels", "S_floor", "schema", "nodes", "terminal_leaves", "root"):
            if k in rep:
                print("      %s = %s" % (k, str(rep[k])[:120]))
print()
print("FAILURES:", len(fails))
for f in fails:
    print("  -", f)
