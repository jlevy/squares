"""Lane rR2: build a synthetic folder with the source's layout and run the drivers on it.

Decides nothing. It exists so that rr2_strips.py and rr2_envelope.py were run end to end
before checker freeze 1, on data this lane made up: a periodic measure on [0, 9]^2 (three
central strips), strip claims at d = -1, 1, 2, one corner modification and three region
claims. The 161 follow-up's paths are created too, with the synthetic anchor, so that its
hypotheses are evaluated (and fail, since its side does not fit a board of side 9).

Usage: python -I rr2_plumbing.py --scratch DIR [--out FILE]
"""

from __future__ import annotations

import argparse
import gzip
import json
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from rr2_measure import Measure  # noqa: E402
from rr2_selftest import periodic_prims  # noqa: E402
from rr2_strips import strip_masses  # noqa: E402


def measure_json(side: F, prims: list) -> bytes:
    rects = [{"rectangle": [str(v) for v in p[:4]], "mass": str(p[4])} for p in prims]
    tot = sum((p[4] for p in prims), F(0))
    data = {"n": 0, "L": str(side), "points": [], "total_mass": str(tot), "fixed_mass": str(tot),
            "rectangles": rects}
    return gzip.compress(json.dumps(data).encode())


def build(root: Path) -> None:
    side = F(9)
    prims = periodic_prims()
    prims.append((F(1, 10), F(2, 10), F(6, 10), F(4, 10), F(1, 3)))  # a corner primitive
    blob = measure_json(side, prims)
    tmp = root / "tmp.json.gz"
    tmp.write_bytes(blob)
    m = Measure.from_file(tmp)
    sm = strip_masses(m.images(), m.S, 3)
    M, b, c = m.total(), sm["bx"], sm["c"]
    # the drivers name this folder in their controls and cross-check, so the synthetic
    # anchor takes its name; nothing here is the source's data
    folder = "162--719881-12.881-100-uniform_finish"
    rep = root / "followup/repeated" / folder
    (rep / "proof").mkdir(parents=True, exist_ok=True)
    for k in ("k100", "k300"):
        (rep / "proof" / f"{k}.json.gz").write_bytes(blob)
    claims = []
    for d in (-1, 1, 2):
        Md = M + 2 * d * b + d * d * c
        n = int(Md) + 1
        claims.append({"n": n, "offset": d, "mass": str(Md), "side": str(side + d),
                       "previous_upper_endpoint": "0", "previous_source": "synthetic",
                       "anchor": 0, "anchor_side": str(side), "folder": folder})
    (root / "followup/repeated/claims.json").write_text(json.dumps(claims))
    family = {"periods": 3, "side": str(side), "anchor_n": 0, "base_mass": str(M),
              "strip_mass": str(b), "cell_mass": str(c),
              "claims": [{k: v for k, v in cl.items() if k in ("n", "offset", "mass", "side")}
                         for cl in claims]}
    (rep / "family.json").write_text(json.dumps(family))
    a161 = root / "followup/repeated/161--749858-12.858-100-uniform/proof"
    a161.mkdir(parents=True, exist_ok=True)
    (a161 / "k100.json.gz").write_bytes(blob)
    ct = root / "followup/corner_trim" / folder
    (ct / "proof").mkdir(parents=True, exist_ok=True)
    (ct / "proof/k100.json.gz").write_bytes(blob)
    corner_index = len(prims) - 1
    mult = {str(corner_index): "1/2"}
    phi = F(1)
    removed = prims[corner_index][4] * (1 - F(1, 2) * phi)
    old = M + 4 * b + 4 * c
    new = old - removed
    claim = {"n": int(new) + 1, "side": str(side + 2), "anchor_side": str(side), "offset": 2,
             "periods": 3, "corner": "1", "factor": str(phi), "removed_mass": str(removed),
             "old_mass": str(old), "new_mass": str(new)}
    (ct / "claim.json").write_text(json.dumps(claim))
    (ct / "multipliers.json").write_text(json.dumps(mult))
    (root / "followup/corner_trim/claims.json").write_text(json.dumps([
        {"n": claim["n"], "offset": 2, "side": claim["side"], "mass": str(new),
         "previous_upper_endpoint": "0", "previous_source": "synthetic", "anchor": 0,
         "folder": folder}]))
    env = root / "followup/envelopes" / folder
    (env / "proof").mkdir(parents=True, exist_ok=True)
    (env / "proof/k100.json.gz").write_bytes(blob)
    eclaims = [
        {"n": 1000, "side": "8", "mass": "1", "folder": folder},
        {"n": 1001, "side": "80001/10000", "mass": "1", "round_steps": 8, "folder": folder},
        {"n": 1, "side": "9001/1000", "mass": "1", "round_steps": 8, "folder": folder},
    ]
    (root / "followup/envelopes/claims.json").write_text(json.dumps(eclaims))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True, type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    root = args.scratch / "plumbing-source"
    root.mkdir(parents=True, exist_ok=True)
    build(root)
    runs = {}
    for prog, extra in (("rr2_strips.py", ["--controls"]),
                        ("rr2_envelope.py", ["--scratch", str(args.scratch), "--controls"])):
        if prog == "rr2_strips.py":
            extra = ["--controls"]
        out = args.scratch / f"plumbing-{prog}.json"
        proc = subprocess.run(
            [sys.executable, "-I", str(HERE / prog), "--source", str(root), "--out", str(out),
             *extra],
            capture_output=True, text=True, check=False,
        )
        runs[prog] = {"returncode": proc.returncode, "stdout": proc.stdout[-2000:],
                      "stderr": proc.stderr[-2000:]}
    text = json.dumps(runs, indent=1)
    if args.out:
        args.out.write_text(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
