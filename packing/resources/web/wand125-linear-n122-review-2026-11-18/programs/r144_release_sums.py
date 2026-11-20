"""Does the release's SHA256SUMS list the asset? A custody receipt.

Usage: r144_release_sums.py --sums SHA256SUMS --api-sha256 HEX --api-updated ISO
                            --asset-name NAME --asset-sha256 HEX --out OUT.json

SHA256SUMS is the release asset as downloaded; --api-sha256 and --api-updated are the
release API's digest and update time for it, taken by `gh api` at the same time. The
receipt says whether the file is the one the API names, how many entries it has, and
whether any entry names the asset or its digest. Written after the review's controls
plan (a disclosed addition); imports nothing from jlevy/squares or the source.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys


def main():
    ap = argparse.ArgumentParser()
    for k in ("--sums", "--api-sha256", "--api-updated", "--asset-name", "--asset-sha256", "--out"):
        ap.add_argument(k, required=True)
    a = ap.parse_args()
    data = open(a.sums, "rb").read()
    lines = [ln for ln in data.decode("utf-8").splitlines() if ln.strip()]
    entries = [ln.split(None, 1) for ln in lines]
    names = {e[1].strip() for e in entries if len(e) == 2}
    digests = {e[0] for e in entries if len(e) == 2}
    res = {
        "program": "r144_release_sums.py",
        "sums_sha256": hashlib.sha256(data).hexdigest(),
        "equals_api_digest": hashlib.sha256(data).hexdigest() == a.api_sha256,
        "api_updated_at": a.api_updated,
        "entries": len(entries),
        "lists_asset_name": a.asset_name in names,
        "lists_asset_digest": a.asset_sha256 in digests,
        "sibling_mixed_entries": sorted(n for n in names if n.startswith("certificates__mixed_n"))[:40],
    }
    with open(a.out, "w") as f:
        json.dump(res, f, indent=1)
        f.write("\n")
    print("SUMS_LIST_ASSET" if res["lists_asset_name"] or res["lists_asset_digest"] else "SUMS_DO_NOT_LIST_ASSET", f"{res['entries']} entries, file equals API digest: {res['equals_api_digest']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
