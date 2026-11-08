"""Compact the complete sweep's per-bin JSON lines into a committed receipt.

Writes, from run_bins.py's shard files:
  OUT_TSV   one line per bin: bin, root core minimum minus W, decision nodes, decided
  OUT_JSON  the summary: bins present and missing, decided, least margin and where,
            the bins at margins 0 and 1 with their minimising centres, a histogram of
            the smallest margins, CPU seconds, and the SHA-256 of each shard file.

Usage: python -I compact_sweep.py W N_BINS OUT_TSV OUT_JSON SHARD.jsonl [SHARD.jsonl ...]
"""

import hashlib
import json
import sys
from collections import Counter


def main():
    w, n_bins = int(sys.argv[1]), int(sys.argv[2])
    out_tsv, out_json = sys.argv[3], sys.argv[4]
    shards = sys.argv[5:]
    recs = {}
    digests = {}
    for path in shards:
        raw = open(path, "rb").read()
        digests[path.rsplit("/", 1)[-1]] = hashlib.sha256(raw).hexdigest()
        for line in raw.decode().splitlines():
            if line.strip():
                r = json.loads(line)
                if r["bin"] in recs:
                    raise SystemExit(f"bin {r['bin']} appears twice")
                recs[r["bin"]] = r
    missing = [k for k in range(n_bins) if k not in recs]
    extra = sorted(k for k in recs if not 0 <= k < n_bins)
    with open(out_tsv, "w") as f:
        f.write("bin\troot_core_margin\tnodes\tdecided\n")
        for k in sorted(recs):
            r = recs[k]
            f.write(f"{k}\t{r['root_core_min'] - w}\t{r['nodes']}\t{int(r['decided'])}\n")
    margins = Counter(r["root_core_min"] - w for r in recs.values())
    least = min(recs.values(), key=lambda r: (r["min_over_leaves"], r["bin"]))
    tight = {
        str(k): {"margin": recs[k]["root_core_min"] - w, "centre": recs[k]["root_witness_centre"]}
        for k in sorted(recs) if recs[k]["root_core_min"] - w <= 1
    }
    out = {
        "W": w,
        "bins_expected": n_bins,
        "bins_present": len(recs),
        "bins_missing": missing,
        "bins_outside_range": extra,
        "decided": sum(1 for r in recs.values() if r["decided"]),
        "undecided": sorted(k for k, r in recs.items() if not r["decided"]),
        "subdivided_bins": sorted(k for k, r in recs.items() if r["nodes"] > 1),
        "least_min_over_leaves": least["min_over_leaves"],
        "least_margin": least["min_over_leaves"] - w,
        "least_at_bin": least["bin"],
        "bins_at_margin_0": sorted(k for k, r in recs.items() if r["root_core_min"] == w),
        "bins_at_margin_1": sorted(k for k, r in recs.items() if r["root_core_min"] == w + 1),
        "margin_histogram_smallest_20": dict(sorted(margins.items())[:20]),
        "bins_with_margin_below_1000": sum(v for m, v in margins.items() if m < 1000),
        "tight_bins": tight,
        "cpu_seconds": round(sum(r["cpu_s"] for r in recs.values()), 1),
        "shard_sha256": digests,
    }
    with open(out_json, "w") as f:
        json.dump(out, f, indent=1)
        f.write("\n")
    print(json.dumps({k: out[k] for k in (
        "bins_present", "bins_missing", "decided", "undecided", "subdivided_bins",
        "least_margin", "least_at_bin", "bins_at_margin_0", "bins_at_margin_1",
        "bins_with_margin_below_1000", "cpu_seconds")}, indent=1))


if __name__ == "__main__":
    main()
