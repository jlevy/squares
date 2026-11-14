"""Write receipts/freeze.sha256: the frozen verdicts and the SHA-256 of every program and output of the packet,
and of the review draft, before the lane reads the record's own material (review of #973, L144).

usage: python -I freeze.py PACKET REVIEW VERDICTS_TEXT_FILE
"""
import datetime
import hashlib
import os
import sys

packet, review, verdicts = sys.argv[1:4]
lines = [f"# L144 freeze, {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
         "# Verdicts frozen before step 5 (the record's T-064, T-081, T-252, T-066, T-184 and k^2 - 5 material at n = 76 to 95):"]
lines += ["# " + ln for ln in open(verdicts).read().strip().split("\n")]
lines.append("# SHA-256 of every file below, relative to the packet; then the review draft")
for root, _, files in sorted(os.walk(packet)):
    for f in sorted(files):
        p = os.path.join(root, f)
        rel = os.path.relpath(p, packet)
        if rel.startswith("receipts/freeze"):
            continue
        lines.append(f"{hashlib.sha256(open(p, 'rb').read()).hexdigest()}  {rel}")
lines.append(f"{hashlib.sha256(open(review, 'rb').read()).hexdigest()}  {os.path.basename(review)} (draft at freeze)")
open(os.path.join(packet, "receipts", "freeze.sha256"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines[:40]))
print("...", len(lines), "lines")
