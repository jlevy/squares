#!/usr/bin/env python3
"""Extract what the source's manifests say about the four certificates; decides nothing.

Reads franciscouzo/square-packing's `certificates/best/manifest.json` at the three pins
(fetched through the GitHub API, read as data), checks each file's SHA-256 against the
digest its packet pins in `acquisition/upstream-subtree.sha256`, and writes the fields
this review cites: the checkers the manifest names, and for each certificate its credit,
provenance, and the source checker's strict verdict and pair counts.

Usage: python -I manifest_extract_0nse.py REPO FETCHED_DIR OUT.json
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

PINS = {
    "couzo-issue670-2026-10-17": ("manifest-23aff0c6.json", "23aff0c6f992271e1ad13a148d44f392c4b386c0", ["204"]),
    "couzo-issue672-2026-10-17": ("manifest-af8cb795.json", "af8cb7959aead318c0cf5e9f873de3caa763f77a", ["227", "229"]),
    "couzo-issue675-2026-10-18": ("manifest-c6da0fc7.json", "c6da0fc7524d667bf3d224559724ba9b60762e60", ["204"]),
}


def main(argv: list[str]) -> int:
    repo, fetched, out = Path(argv[1]), Path(argv[2]), Path(argv[3])
    report = {}
    for packet, (name, pin, counts) in PINS.items():
        data = (fetched / name).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        pinned = next(
            line.split()[0]
            for line in (repo / "packing/resources/web" / packet / "acquisition/upstream-subtree.sha256").read_text().splitlines()
            if line.endswith("./certificates/best/manifest.json")
        )
        manifest = json.loads(data)
        entry = {
            "pin": pin,
            "sha256": digest,
            "equals_packet_pinned_digest": digest == pinned,
            "generated": manifest.get("generated"),
            "first_checker": manifest.get("first_checker"),
            "second_checker": manifest.get("second_checker"),
            "second_checker_sha256": manifest.get("second_checker_sha256"),
            "witnesses": {},
        }
        for n in counts:
            w = manifest["witnesses"][n]
            entry["witnesses"][n] = {
                "certificate": w.get("certificate"),
                "certificate_sha256": w.get("certificate_sha256"),
                "bound": w.get("bound"),
                "credit": w.get("credit"),
                "provenance": w.get("provenance"),
                "strict_verification": w.get("strict_verification"),
            }
        report[packet] = entry
        print(packet, pin[:8], "digest equal" if entry["equals_packet_pinned_digest"] else "DIGEST DIFFERS", entry["first_checker"])
        for n, w in entry["witnesses"].items():
            s = w["strict_verification"] or {}
            print(f"  {n}: credit={w['credit']!r}; category={w['provenance'].get('category')!r}; strict valid={s.get('valid')} closed_valid={s.get('closed_valid')} near_pairs={s.get('near_pairs')}")
    out.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    return 0 if all(e["equals_packet_pinned_digest"] for e in report.values()) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
