"""Does the Lean hypothesis Valid11 speak about the board file?  (review of #973, L144)

usage: python -I lean_data_link.py BOARD INSTDATA_LEAN
Parses `boxSegs`, `boxPolyVerts` and `boxPolyW` out of InstData.lean as text and compares them, in file order, with
the board's segment lines, polygon vertices and polygon weight.  Also scans every K2m5 Lean file next to InstData
for kernel-escape tokens.
"""
import glob
import json
import os
import re
import sys

board, inst = sys.argv[1:3]
L = open(board).read().split("\n")
i = 0
while not L[i].split() or L[i].startswith("#") or L[i].startswith("mixed"):
    i += 1
n = int(L[i + 4])
segs = [tuple(map(int, L[i + 5 + j].split())) for j in range(n)]
rest = [ln for ln in L[i + 5 + n:] if ln.strip()]
poly = list(map(int, rest[1].split()))
txt = open(inst).read()
m = re.search(r"def boxSegs : List \(Nat × Nat × Nat × Nat × Nat\) := \[(.*?)\]\n", txt, re.S)
lean_segs = [tuple(map(int, t)) for t in re.findall(r"\((\d+), (\d+), (\d+), (\d+), (\d+)\)", m.group(1))]
mv = re.search(r"def boxPolyVerts : List \(Nat × Nat\) := \[(.*?)\]", txt)
verts = [tuple(map(int, t)) for t in re.findall(r"\((\d+), (\d+)\)", mv.group(1))]
pw = int(re.search(r"def boxPolyW : Nat := (\d+)", txt).group(1))
tokens = ("sorry", "native_decide", "implemented_by", "extern", "unsafe", "axiom ", "admit", "decide := true", "ofReduceBool")
hits = {}
for f in sorted(glob.glob(os.path.join(os.path.dirname(inst), "*.lean"))):
    t = open(f).read()
    for tok in tokens:
        if tok in t:
            hits.setdefault(os.path.basename(f), []).append(tok)
res = dict(board_segments=len(segs), lean_segments=len(lean_segs), segments_equal_in_order=segs == lean_segs,
           poly_verts_equal=verts == [tuple(poly[2 + 2 * k: 4 + 2 * k]) for k in range(4)], poly_weight_equal=pw == poly[1],
           kernel_escape_tokens=hits)
print(json.dumps(res))
