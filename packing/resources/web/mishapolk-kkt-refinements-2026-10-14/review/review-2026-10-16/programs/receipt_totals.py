"""Sum each packet receipt's jobs, pair decisions and wall, per count (reads only)."""
import sys
from devtools import upper_bound_reports as ubr

for name in sys.argv[1:]:
    packet = ubr.packet_path(name)
    paths = sorted((packet / "receipts").glob("exact-certification*.json.xz"))
    rows = []
    for p in paths:
        rows += ubr.kernel.read_xz(p)["cases"]
    s = ubr.receipt_summary({"cases": rows})
    per_n = {}
    for row in rows:
        per_n[row["n"]] = per_n.get(row["n"], 0.0) + row["wall_seconds"]
    print(name, len(paths), "files", s)
    print("   per-n wall:", {n: round(w, 1) for n, w in sorted(per_n.items())})
