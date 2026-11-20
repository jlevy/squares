"""Write a mutated candidate for a control: the heaviest orbit of one kind removed.

Usage: r144_mutate.py --bundle BUNDLE_DIR --kind segment --out-dir DIR --out OUT.json

Reads candidate.json, removes the primitive of the given kind with the largest mass (the
first if several tie), lowers total_mass by its mass, and writes DIR/candidate.json in the
same layout, so that the frozen deciders, which read only candidate.json from the
directory they are given, can run on it unchanged. The receipt names the removed
primitive and both files' SHA-256. Written after the controls plan (a disclosed
addition, the second mutated certificate the runbook's replay conditions ask for);
imports nothing from jlevy/squares or the source.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from fractions import Fraction as F


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--kind", default="segment", choices=["point", "segment", "rectangle"])
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    raw = open(os.path.join(a.bundle, "candidate.json"), "rb").read()
    obj = json.loads(raw)
    prims = obj["primitives"]
    idx = max((i for i, p in enumerate(prims) if p["kind"] == a.kind), key=lambda i: F(prims[i]["mass"]))
    removed = prims[idx]
    m = F(removed["mass"])
    obj["primitives"] = prims[:idx] + prims[idx + 1 :]
    tot = F(obj["total_mass"]) - m
    obj["total_mass"] = f"{tot.numerator}/{tot.denominator}"
    os.makedirs(a.out_dir, exist_ok=True)
    data = (json.dumps(obj, indent=2) + "\n").encode()
    with open(os.path.join(a.out_dir, "candidate.json"), "wb") as f:
        f.write(data)
    res = {
        "program": "r144_mutate.py",
        "mutation": f"the heaviest {a.kind} orbit removed",
        "removed_index": idx,
        "removed": removed,
        "removed_mass": float(m),
        "removed_mass_per_image": float(m / 8),
        "total_mass_after": obj["total_mass"],
        "original_sha256": hashlib.sha256(raw).hexdigest(),
        "mutant_sha256": hashlib.sha256(data).hexdigest(),
    }
    with open(a.out, "w") as f:
        json.dump(res, f, indent=1)
        f.write("\n")
    print("MUTANT_WRITTEN", res["mutation"], f"index {idx}", f"mass {float(m):.6f} ({float(m / 8):.6f} per image)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
