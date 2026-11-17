"""Mutant covers for the controls (review of issue #973, lane L144).  Written here; reads the board as text.

usage: python -I make_mutants.py BOARD OUTDIR
writes:
  scale0999.txt   every segment weight * 999/1000, floored (the source's x0.999 control, rebuilt here)
  scale0993.txt   every segment weight * 993/1000, floored (the source's x0.993 control, rebuilt here)
  m1_leb.txt      M-1: the Lebesgue square's weight * (1 - 10^-6); segments unchanged
  m2_minus1.txt   M-2: every segment weight lowered by one unit of the weight denominator
"""
import os
import sys

src, outd = sys.argv[1:3]
L = open(src).read().split("\n")
i = 0
while not L[i].split() or L[i].startswith("#") or L[i].startswith("mixed"):
    i += 1
n = int(L[i + 4])


def emit(name, seg_fn, poly_fn, note):
    o = L[:i] + [f"# CONTROL (L144 review): {note}"] + L[i:i + 5]
    for j in range(n):
        t = L[i + 5 + j].split()
        t[4] = str(seg_fn(int(t[4])))
        o.append(" ".join(t))
    rest = L[i + 5 + n:]
    k = 0
    while not rest[k].strip():
        k += 1
    npoly = int(rest[k])
    out_rest = rest[:k + 1]
    for j in range(npoly):
        t = rest[k + 1 + j].split()
        t[1] = str(poly_fn(int(t[1])))
        out_rest.append(" ".join(t))
    out_rest += rest[k + 1 + npoly:]
    open(os.path.join(outd, name), "w").write("\n".join(o + out_rest))


emit("scale0999.txt", lambda w: w * 999 // 1000, lambda w: w, "every segment mass scaled by 999/1000 (floor); Lebesgue square unchanged")
emit("scale0993.txt", lambda w: w * 993 // 1000, lambda w: w, "every segment mass scaled by 993/1000 (floor); Lebesgue square unchanged")
emit("m1_leb.txt", lambda w: w, lambda w: w - w // 10 ** 6, "Lebesgue weight times (1 - 10^-6); segments unchanged")
emit("m2_minus1.txt", lambda w: w - 1, lambda w: w, "every segment weight lowered by 1/(2*10^12); Lebesgue unchanged")
print("ok")
