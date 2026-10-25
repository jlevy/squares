"""Read the credit statements the sources make at 268, 303 and 304, for the credit chains.

A program of the stage 4 mathematical review of T-241 and T-242 (bead think-vm3m). It
decides nothing about any bound: it prints, from the sources' own files, what each says
about who found the packings at 268, 303 and 304, and how Couzo's manifest uses its
provenance fields across all its entries. Every input is read as data and checked
against the SHA-256 the packets pin where they pin one.

Inputs: the issue-763 packet's manifest.json.gz and certified_bounds.json.gz (964ee2b);
the evand-kaggle-descents packet's CREDITS.md; and, from scratch copies of the two
watched clones (never the shared clones), the fa6237e manifest, the catalogue README at
fa6237e, 964ee2b and 1c17153, RECORD_PROVENANCE.md, and Daniel's Completed.md and
TODO.md at 659ee62, fetched there with `git cat-file -p BLOB > FILE`.

Run from packing/:
    python -I resources/web/evand-kaggle-descents-2026-10-24/review/review-2026-10-24/programs/t241_t242_credits.py \
        --scratch DIR --evand-clone CLONE --couzo-clone CLONE
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKING = HERE.parents[5]
COUZO_PACKET = PACKING / "resources/web/couzo-issue763-2026-10-23"
EVAND_PACKET = PACKING / "resources/web/evand-kaggle-descents-2026-10-24"

PINS = {
    "manifest-fa6237e.json": "31b0caef3c213b9390165520b6676d3003e8236f7c5cf35db1ed5be930f44f30",
    "manifest-964ee2b (packet, decompressed)": "d95f2bd6410abf07d568cbed937afb066de7ed6b01a35f74e6b461ac6a44c5ae",
    "catalogue-964ee2b.md": "59fe57183b78a892d614bc1e37c2d1935d07ebc127ee09c42f39d951aa2fa31d",
    "RECORD_PROVENANCE.md": "caa6050ec1a1ca3f902be0bb544d116bb0236affb54fa5d979bebd35e6e800c8",
}
COUNTS = ("268", "303", "304")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check(name: str, data: bytes) -> str:
    got = digest(data)
    pin = PINS.get(name)
    status = "no pin" if pin is None else ("matches the pin" if got == pin else "DOES NOT MATCH THE PIN")
    print(f"input {name}: sha256 {got} ({status})")
    return got


def summarise(entry: dict[str, object]) -> dict[str, object]:
    provenance = entry.get("provenance") or {}
    assert isinstance(provenance, dict)
    source = provenance.get("source_provenance") or {}
    previous = provenance.get("previous_source") or {}
    reference = provenance.get("previous_reference") or {}
    assert isinstance(source, dict) and isinstance(previous, dict) and isinstance(reference, dict)
    previous_prov = previous.get("provenance") or {}
    assert isinstance(previous_prov, dict)
    return {
        "certificate_sha256": str(entry.get("certificate_sha256", ""))[:16],
        "credit": entry.get("credit"),
        "category": provenance.get("category"),
        "source_provenance": {
            "category": source.get("category"),
            "lineage": [(step.get("submission"), step.get("source")) for step in source.get("lineage") or []],
            "seed_credit": source.get("seed_credit"),
            "notebook": source.get("notebook"),
            "notebook_version": source.get("notebook_version"),
            "source_notices": source.get("source_notices"),
            "original_credits": source.get("original_credits"),
            "witness_dilation": source.get("witness_dilation"),
        },
        "previous_source": {
            "certificate_sha256": str(previous.get("certificate_sha256", ""))[:16],
            "credit": previous.get("credit"),
            "category": previous_prov.get("category"),
            "construction_credit": previous_prov.get("construction_credit"),
        },
        "previous_reference": {
            "seed_credit": reference.get("seed_credit"),
            "source_certificate_sha256": str(reference.get("source_certificate_sha256", ""))[:16],
        },
    }


def census(witnesses: dict[str, dict[str, object]]) -> Counter[str]:
    """How previous_reference.seed_credit stands to the packing's own seed credit."""
    tally: Counter[str] = Counter()
    for entry in witnesses.values():
        provenance = entry.get("provenance") or {}
        if not isinstance(provenance, dict):
            continue
        source = provenance.get("source_provenance") or {}
        reference = provenance.get("previous_reference") or {}
        previous = provenance.get("previous_source") or {}
        if not isinstance(source, dict) or not isinstance(reference, dict) or not isinstance(previous, dict):
            continue
        if not reference:
            tally["no previous_reference"] += 1
            continue
        same_cert = reference.get("source_certificate_sha256") == previous.get("certificate_sha256")
        tally["previous_reference names the previous_source certificate" if same_cert else
              "previous_reference names another certificate"] += 1
        own_seed = source.get("seed_credit")
        if own_seed is None:
            tally["no seed_credit in source_provenance"] += 1
        elif own_seed == reference.get("seed_credit"):
            tally["source_provenance.seed_credit equals previous_reference.seed_credit"] += 1
        else:
            tally["source_provenance.seed_credit differs from previous_reference.seed_credit"] += 1
    return tally


def git(clone: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(clone), *args], check=True, capture_output=True, text=True).stdout


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--scratch", type=Path, required=True, help="directory holding the fetched source files")
    parser.add_argument("--evand-clone", type=Path, required=True, help="scratch copy of evand/square-packing")
    parser.add_argument("--couzo-clone", type=Path, required=True, help="scratch copy of franciscouzo/square-packing")
    args = parser.parse_args()

    raw = (args.scratch / "manifest-fa6237e.json").read_bytes()
    check("manifest-fa6237e.json", raw)
    manifest_a = json.loads(raw)
    raw = gzip.decompress((COUZO_PACKET / "source/certificates/best/manifest.json.gz").read_bytes())
    check("manifest-964ee2b (packet, decompressed)", raw)
    manifest_b = json.loads(raw)
    print(f"first_checker fa6237e: {manifest_a.get('first_checker')}")
    print(f"first_checker 964ee2b: {manifest_b.get('first_checker')}")
    for count in COUNTS:
        for tag, manifest in (("fa6237e", manifest_a), ("964ee2b", manifest_b)):
            print(f"\nmanifest {tag} witnesses/{count}:")
            print(json.dumps(summarise(manifest["witnesses"][count]), indent=1))
        print(f"witnesses/{count} identical at fa6237e and 964ee2b: "
              f"{manifest_a['witnesses'][count] == manifest_b['witnesses'][count]}")
    for tag, manifest in (("fa6237e", manifest_a), ("964ee2b", manifest_b)):
        print(f"\ncensus of the {tag} manifest's {len(manifest['witnesses'])} witnesses:")
        for key, value in sorted(census(manifest["witnesses"]).items()):
            print(f"  {value:5d}  {key}")

    raw = gzip.decompress((COUZO_PACKET / "source/certified_bounds.json.gz").read_bytes())
    print(f"\ninput certified_bounds.json (964ee2b, packet): sha256 {digest(raw)}")
    entries = json.loads(raw)["entries"]
    for count in COUNTS:
        row = entries[count]
        verification = row.get("verification") or {}
        keep = {
            "certificate": row.get("certificate"),
            "certificate_sha256": str(row.get("certificate_sha256"))[:16],
            "credit": row.get("credit"),
            "rounded_up": row.get("rounded_up"),
            "valid": verification.get("valid"),
            "pairs_tested": verification.get("pairs_tested"),
            "arithmetic_backend": verification.get("arithmetic_backend"),
        }
        print(f"certified_bounds {count}: {json.dumps(keep)}")

    for tag in ("fa6237e", "964ee2b", "1c17153"):
        data = (args.scratch / f"catalogue-{tag}.md").read_bytes()
        check(f"catalogue-{tag}.md", data)
        for line in data.decode().splitlines():
            if re.match(r"^\| \[(268|303|304)\]\(", line):
                print(f"  catalogue {tag}: {line}")

    data = (args.scratch / "RECORD_PROVENANCE.md").read_bytes()
    check("RECORD_PROVENANCE.md", data)
    for line in data.decode().splitlines():
        if "70a033f" in line and "304" in line:
            print(f"  RECORD_PROVENANCE.md: {line}")

    notices = git(args.couzo_clone, "log", "--all", "--format=%h %s", "--", "*SOURCE_NOTICES*").strip()
    print(f"\ncommits on any ref of the Couzo clone touching a SOURCE_NOTICES file: {notices or 'none'}")
    for commit in ("fa6237e", "964ee2b", "43f666c"):
        message = git(args.couzo_clone, "log", "-1", "--format=%H %cI%n%B", commit)
        for line in message.splitlines():
            if re.search(r"\b(268|303|304)\b|notebook|Kaggle", line):
                print(f"  couzo {commit}: {line.strip()}")

    print()
    message = git(args.evand_clone, "log", "-1", "--format=%H %aI %cI%n%B", "8a8879a2972c32cbd2d906049228cc9f0762b02a")
    print("evand 8a8879a commit message:\n" + message)
    for name in ("Completed.md", "TODO.md"):
        data = (args.scratch / f"evand-659ee62-{name}").read_bytes()
        print(f"input evand 659ee62 {name}: sha256 {digest(data)}")
        for line in data.decode().splitlines():
            if re.search(r"8a8879a|lightningv08|kozykappa|kirilltym|268 / 303|finder", line):
                print(f"  {name}: {line.strip()}")
    data = (EVAND_PACKET / "source/CREDITS.md").read_bytes()
    print(f"input evand CREDITS.md (packet): sha256 {digest(data)}")
    hits = [line.strip() for line in data.decode().splitlines() if re.search(r"Kaggle|Lavrentev|kozykappa|Tymchishin|Couzo|Produced by|jlevy", line)]
    for line in hits:
        print(f"  CREDITS.md: {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
