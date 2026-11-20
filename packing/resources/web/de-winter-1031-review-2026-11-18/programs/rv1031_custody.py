"""Custody of the certificate of jlevy/squares#1031 (decides nothing).

Written for this review after the checker's freeze; imports nothing from this repository
or the source.

    python -I -B rv1031_custody.py --route raw=DIR --route api=DIR \
        --inputs out/custody-inputs --out custody.json

For each fetched copy of ``n299_exact.json`` and ``n299_witness.yaml`` (one directory per
route: raw.githubusercontent.com at the pin, and the GitHub git-blob API by the blob ids
the pin's tree lists), it gives the SHA-256 and the git blob id, and compares them with
the tree listings at the pin and at the source's head and with the source's own
``SHA256SUMS`` (added in the pin's child commit).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os

FILES = ("n299_exact.json", "n299_witness.yaml")


def blob_id(raw: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--route", action="append", default=[])
    ap.add_argument("--inputs", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    with open(os.path.join(args.inputs, "n299-listing-pin.json")) as fh:
        pin = {e["name"]: e for e in json.load(fh)}
    with open(os.path.join(args.inputs, "n299-listing-head.json")) as fh:
        head = {e["name"]: e for e in json.load(fh)}
    sums = {}
    with open(os.path.join(args.inputs, "SHA256SUMS-at-3293038d")) as fh:
        for line in fh:
            d, name = line.split()
            sums[name] = d
    with open(os.path.join(args.inputs, "pin-commit.json")) as fh:
        commit = json.load(fh)
    rec: dict = {
        "program": "rv1031_custody.py",
        "pin": commit["sha"],
        "pin_committed": commit["commit"]["committer"]["date"],
        "pin_files_changed": [f["filename"] for f in commit.get("files", [])],
        "routes": {},
    }
    digests: dict[str, set[str]] = {f: set() for f in FILES}
    ok = True
    for spec in args.route:
        name, d = spec.split("=", 1)
        r = {}
        for f in FILES:
            with open(os.path.join(d, f), "rb") as fh:
                raw = fh.read()
            sha, bid = hashlib.sha256(raw).hexdigest(), blob_id(raw)
            digests[f].add(sha)
            r[f] = {
                "bytes": len(raw), "sha256": sha, "git_blob": bid,
                "blob_as_listed_at_pin": bid == pin[f]["sha"], "blob_as_listed_at_head": bid == head[f]["sha"],
                "sha256_as_in_source_SHA256SUMS": sha == sums.get(f),
            }
            ok = ok and r[f]["blob_as_listed_at_pin"] and r[f]["blob_as_listed_at_head"] and r[f]["sha256_as_in_source_SHA256SUMS"]
        rec["routes"][name] = r
    rec["routes_agree"] = all(len(v) == 1 for v in digests.values())
    rec["head_listing_names"] = sorted(head)
    rec["pin_listing_names"] = sorted(pin)
    rec["added_after_pin"] = sorted(set(head) - set(pin))
    rec["verdict"] = "CUSTODY_HOLDS" if ok and rec["routes_agree"] else "CUSTODY_DIFFERS"
    with open(args.out, "w") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(rec["verdict"], {f: sorted(v) for f, v in digests.items()}, rec["added_after_pin"])
    return 0 if rec["verdict"] == "CUSTODY_HOLDS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
