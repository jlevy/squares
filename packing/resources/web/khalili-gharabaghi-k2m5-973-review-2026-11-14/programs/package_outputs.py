"""Copy this lane's small outputs into the packet; reduce bulk zmx2 dumps to their census and a digest
(review of #973, L144).

usage: python -I package_outputs.py WORKDIR PACKET
  WORKDIR  the scratch work folder (out/, zmx2/, qx2/, qx2c/, tt/, b1/, cov_m4 is not copied)
For every zmx2 output: the lines that are not UNCERT lines, the number of UNCERT lines, and the SHA-256 of the
sorted, newline-joined exact box strings "root,pass,box" (so a later run can be compared without the bulk).
Tight-leaf dumps are reduced to their line count and SHA-256.  Everything else is copied as is (all small).
"""
import glob
import hashlib
import json
import os
import re
import shutil
import sys

work, packet = sys.argv[1:3]
out = os.path.join(packet, "outputs")
os.makedirs(out, exist_ok=True)
pat = re.compile(r"^UNCERT (\d+) pass (\d+) box (\S+) ")


def sha_file(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


summary = {}
# clean-room JSON outputs
for f in sorted(glob.glob(os.path.join(work, "out", "*.json"))):
    name = os.path.basename(f)
    if name == "samples.json":       # the drawn samples: large, regenerable by draw_samples.py
        summary[name] = dict(bytes=os.path.getsize(f), sha256=sha_file(f), kept=False)
        continue
    shutil.copy(f, os.path.join(out, name))
for f in glob.glob(os.path.join(work, "out", "*.log")):
    shutil.copy(f, os.path.join(out, os.path.basename(f)))
# zmx2 runs
zo = os.path.join(out, "zmx2")
os.makedirs(zo, exist_ok=True)
for f in sorted(glob.glob(os.path.join(work, "zmx2", "*.out"))):
    name = os.path.basename(f)
    keep, boxes = [], []
    for ln in open(f):
        m = pat.match(ln)
        if m:
            boxes.append(f"{m.group(1)},{m.group(2)},{m.group(3)}")
        elif not ln.startswith("progress "):
            keep.append(ln.rstrip("\n"))
    digest = hashlib.sha256("\n".join(sorted(boxes)).encode()).hexdigest()
    keep.append(f"# L144 packaging: {len(boxes)} UNCERT lines removed; sha256 of their sorted box strings {digest}")
    open(os.path.join(zo, name), "w").write("\n".join(keep) + "\n")
    t = f[:-4] + ".time"
    if os.path.exists(t):
        shutil.copy(t, os.path.join(zo, name[:-4] + ".time"))
for f in sorted(glob.glob(os.path.join(work, "zmx2", "*.tight"))):
    summary["tight/" + os.path.basename(f)] = dict(lines=sum(1 for _ in open(f)), sha256=sha_file(f), kept=False)
shutil.copy(os.path.join(work, "zmx2", "runner.log"), os.path.join(zo, "runner.log"))
shutil.copy(os.path.join(work, "zmx2", "jobs.txt"), os.path.join(zo, "jobs.txt"))
# qx2 runs (small)
for sub in ("qx2", "qx2c"):
    d = os.path.join(work, sub)
    if os.path.isdir(d):
        os.makedirs(os.path.join(out, sub), exist_ok=True)
        for f in glob.glob(os.path.join(d, "*")):
            if f.endswith(".txt") and "c9632" in f:
                continue                   # the source's input covers, not ours
            shutil.copy(f, os.path.join(out, sub, os.path.basename(f)))
# Tight-Tile runs (small)
to = os.path.join(out, "tt")
os.makedirs(to, exist_ok=True)
for f in glob.glob(os.path.join(work, "tt", "*")):
    shutil.copy(f, os.path.join(to, os.path.basename(f)))
# the source's fast checks run here
bo = os.path.join(out, "source_fast_checks")
os.makedirs(bo, exist_ok=True)
for f in glob.glob(os.path.join(work, "b1", "*.out")):
    shutil.copy(f, os.path.join(bo, os.path.basename(f)))
json.dump(summary, open(os.path.join(out, "bulk_not_kept.json"), "w"), indent=1, sort_keys=True)
print("packaged", sum(len(fs) for _, _, fs in os.walk(out)), "files")
