"""Triage diagnostic for #594: re-read the zm_mixed sub-root records and the zmx2 failing
roots, with exact fractions, independently of the author's check_coverage.py.

Checks: every record file has one header naming the pinned checker digests, the cover digest
and the D4 certificate-mode settings; each sub-root is a 1/20 x 1/20 x 1/32 cell aligned to
that grid (so distinct cells are interior-disjoint); the cells inside each failing zmx2 root
are exactly its 16 grid cells; the record root equals the header's region and jobs.txt;
UNCERT 0 and empty unc everywhere; totals of boxes, max depth and CPU.

usage: python -I zm_records.py RECORDS_DIR FAILING_ROOTS JOBS
"""

import json
import sys
from fractions import Fraction as F
from pathlib import Path

rec_dir, failing_path, jobs_path = (Path(a) for a in sys.argv[1:4])
PINS = {
    "zm_mixed.py": "ee3e2915349b8795128417bca6414b205d526db9f01f88cd4cd32c32e8d760ac",
    "mixed_cover.py": "bb89de15ecf5821dd7e1a36ebab8a50d792a406b7fb0f5cb38059f99ef74aae5",
    "zeromargin.py": "640fe453c1a32f4aa580ca2b1261c6406923a4d7c131f65604a432c7fc2086ab",
    "input": "b6a1214b99f00e5dd136d74c8d87bccd178df38a1063b2c7be90517eb2b862b2",
}
WANT = {"mode": "D4", "depth": 24, "pitch": "1/20", "ubins": 16, "chain": True,
        "chain_from": 0, "cert_mode": True, "split": True}
PX, PU = F(1, 20), F(1, 32)

jobs = {}
for line in jobs_path.read_text().splitlines():
    if line.strip():
        i, *vals = line.split()
        jobs[i] = tuple(F(v) for v in vals)
failing = [tuple(F(v) for v in ln.strip().split(",")) for ln in failing_path.read_text().splitlines() if ln.strip()]

cells = {}
boxes = maxdepth = 0
cpu = 0.0
problems = []
for path in sorted(rec_dir.glob("j*.jsonl")):
    lines = [json.loads(x) for x in path.read_text().splitlines() if x.strip()]
    headers = [d for d in lines if d.get("kind") == "zm_mixed cert header"]
    roots = [d for d in lines if "st" in d]
    if len(headers) != 1 or len(roots) != 1 or len(lines) != 2:
        problems.append(f"{path.name}: {len(headers)} headers, {len(roots)} roots, {len(lines)} lines")
        continue
    h, r = headers[0], roots[0]
    if h["sha256"] != PINS:
        problems.append(f"{path.name}: digests {h['sha256']}")
    s = h["settings"]
    for k, v in WANT.items():
        if s.get(k) != v:
            problems.append(f"{path.name}: setting {k}={s.get(k)!r}")
    reg = s["region"]
    region = tuple(F(reg[k]) for k in ("cx_lo", "cx_hi", "cy_lo", "cy_hi", "u_lo", "u_hi"))
    root = tuple(F(v) for v in r["root"])
    job = jobs.get(path.stem[1:])
    if root != region or root != job:
        problems.append(f"{path.name}: root {root} region {region} job {job}")
    if r["st"]["UNCERT"] != 0 or r["unc"]:
        problems.append(f"{path.name}: uncertified")
    x0, x1, y0, y1, u0, u1 = root
    if (x1 - x0, y1 - y0, u1 - u0) != (PX, PX, PU) or any(
        (v / p).denominator != 1 for v, p in ((x0, PX), (y0, PX), (u0, PU))
    ):
        problems.append(f"{path.name}: not a grid cell {root}")
    if root in cells:
        problems.append(f"{path.name}: duplicate cell")
    cells[root] = path.name
    boxes += r["st"]["boxes"]
    maxdepth = max(maxdepth, r["st"]["maxdepth"])
    cpu += r["st"]["cpu"]

for fr in failing:
    x0, x1, y0, y1, u0, u1 = fr
    want = {
        (x0 + i * PX, x0 + (i + 1) * PX, y0 + j * PX, y0 + (j + 1) * PX, u0 + k * PU, u0 + (k + 1) * PU)
        for i in range(int((x1 - x0) / PX)) for j in range(int((y1 - y0) / PX)) for k in range(int((u1 - u0) / PU))
    }
    missing = want - set(cells)
    if missing:
        problems.append(f"failing root {fr}: {len(missing)} cells missing")
inside = {c for c in cells if any(f[0] <= c[0] and c[1] <= f[1] and f[2] <= c[2] and c[3] <= f[3] and f[4] <= c[4] and c[5] <= f[5] for f in failing)}
if inside != set(cells):
    problems.append(f"{len(set(cells) - inside)} cells outside the failing roots")
print(json.dumps({"record_files": len(cells), "failing_roots": len(failing), "boxes": boxes,
                  "max_depth": maxdepth, "cpu_s": round(cpu, 1), "problems": problems}, indent=1))
sys.exit(1 if problems else 0)
