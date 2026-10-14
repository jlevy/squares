"""Dump the 98 class files compactly: symmetry, bound, classes (name, threshold, slots: polygon + gate).

Usage: python3 -I dump_classes.py CAP/statements [names...]
Long rationals are shortened to a float with 12 digits plus a marker.
"""
import json
import os
import sys
from fractions import Fraction as Fr

root = sys.argv[1]
names = sys.argv[2:] or sorted(os.listdir(root))

def short(s):
    f = Fr(s)
    if len(s) > 24:
        return "%.12g~" % float(f)
    return s

for n in names:
    p = os.path.join(root, n, "classes.json")
    if not os.path.exists(p):
        continue
    with open(p, "r", encoding="utf-8") as fh:
        d = json.load(fh)
    print("=" * 90)
    print("%s  symmetry=%s  bound=%s  centre=%s" % (n, d["symmetry"], d["bound"], d["frame"]["center"]))
    for c in d["classes"]:
        print("  class %-40s threshold=%s  slots=%d" % (c["name"], c["threshold"], len(c["slots"])))
        for s in c["slots"]:
            poly = s["centre"]["polygon"]
            print("     gate=[%s,%s] poly=%s" % (short(s["angle_tan_half"][0]), short(s["angle_tan_half"][1]),
                                              " ".join("(%s,%s)" % (short(x), short(y)) for x, y in poly)))
