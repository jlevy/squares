"""Pose file (centre x, centre y, turn in radians) -> exactsolve input: "n side", then "x y degrees" per square.

  python3 make-input.py ../n-127-decimal-pose.yaml n-127-input.txt
"""
import math
import sys

import yaml

w = yaml.safe_load(open(sys.argv[1]))["witness"]
with open(sys.argv[2], "w") as f:
    f.write(f"{w['n']} {w['side']}\n")
    for q in w["squares"]:
        f.write(f"{q['center'][0]} {q['center'][1]} {math.degrees(float(q['angle'])):.17g}\n")
