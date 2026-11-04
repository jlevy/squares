"""Custody of the two retained packets against bare clones of their upstream repositories.

Usage: oz_custody.py S299.git S204.git PACKET299 PACKET204 OUT.json

For each upstream: the refs, the commit count, the pinned commit and its tree, its author,
committer and message; every blob's SHA-256 at the pin, against the packet's
upstream-subtree.sha256, against the retained file (gzip decompressed, and the gzip header
checked for name and time), and against the digests the issue states; licence files and
licence mentions in any text blob; and the sources.json fields that describe the clone.
git runs only read-only plumbing on the bare clones (rev-list, cat-file, ls-tree).
"""

from __future__ import annotations

import gzip
import hashlib
import json
import platform
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent

PINS = {
    "s299": {
        "commit": "6486ead9be5e3348f64ad39aecc1950f22910de4",
        "issue": 893,
        # Stated in issue #893's body and the source README.
        "stated": {"n-299-candidate.yaml": "2976d67f0b6da33434831a53d41c9af2a555e9d67daadb0e80ffc1a5cc6176e0",
                   "n299-refill2-t000173.json": "4fac4ed1b75eb0890935691045a0b395af2a762f8130bcd83cd4b3b83f0bb797"},
    },
    "s204": {
        "commit": "d4b8b05c45e3be464476c94712a4dbc063009875",
        "issue": 894,
        "stated": {"n-204-candidate.yaml": "e3c8c7ebf80819290efa023b0fa7f6cd046b9ee01979aac9cb8d76c1ec14eeb8",
                   "n204-witness.json": "613c0a668026a393f7eaebf796acdc2c8aafe6e7c9c66bc9ee68397ce13caf45"},
    },
}

LICENCE_NAME = re.compile(r"(^|/)(LICEN[CS]E|COPYING|NOTICE|UNLICENSE)(\.[A-Za-z0-9]+)?$", re.I)
LICENCE_WORD = re.compile(r"licen[cs]e|copyright|\bMIT\b|apache|\bGPL\b|creative commons|\bCC[- ]BY", re.I)


def git(repo, *args, binary=False):
    out = subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)
    return out.stdout if binary else out.stdout.decode("utf-8")


def one(name, repo, packet) -> dict:
    pin = PINS[name]
    refs = git(repo, "for-each-ref", "--format=%(refname) %(objectname)").split("\n")
    refs = [r for r in refs if r]
    commits = git(repo, "rev-list", "--all").split()
    meta = git(repo, "log", "-1", "--format=%H%n%T%n%an <%ae>%n%aI%n%cn <%ce>%n%cI%n%s", pin["commit"]).split("\n")
    tree = git(repo, "ls-tree", "-r", "-l", pin["commit"]).split("\n")
    blobs = {}
    for ln in tree:
        if not ln:
            continue
        mode_type_obj, path = ln.split("\t", 1)
        mode, typ, obj, size = mode_type_obj.split()
        data = git(repo, "cat-file", "blob", obj, binary=True)
        blobs[path] = {"blob": obj, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "data": data}
    manifest = {}
    for ln in (packet / "acquisition" / "upstream-subtree.sha256").read_text().split("\n"):
        if ln.strip():
            dig, p = ln.split(None, 1)
            manifest[p.removeprefix("./")] = dig
    sources = json.loads((packet / "acquisition" / "sources.json").read_text())
    src = sources["sources"][0]
    pinned_only = {p["path"]: p for p in src.get("pinned_only", [])}
    rows = []
    for path, b in sorted(blobs.items()):
        retained = packet / "source" / path
        gz = packet / "source" / (path + ".gz")
        row = {"path": path, "blob": b["blob"], "bytes": b["bytes"], "sha256": b["sha256"],
               "manifest_matches": manifest.get(path) == b["sha256"]}
        if retained.exists():
            row["retained"] = "plain"
            row["retained_matches"] = hashlib.sha256(retained.read_bytes()).hexdigest() == b["sha256"]
        elif gz.exists():
            raw = gz.read_bytes()
            row["retained"] = "gzip"
            row["retained_matches"] = hashlib.sha256(gzip.decompress(raw)).hexdigest() == b["sha256"]
            flags = raw[3]
            mtime = int.from_bytes(raw[4:8], "little")
            row["gzip_header"] = {"magic_ok": raw[:3] == b"\x1f\x8b\x08", "flags": flags, "mtime": mtime,
                                  "no_name_no_time": flags == 0 and mtime == 0}
        elif path in pinned_only:
            po = pinned_only[path]
            row["retained"] = "pinned-only"
            row["pinned_digest_matches"] = po.get("sha256") == b["sha256"] and po.get("bytes") == b["bytes"]
            ident = po.get("identical_to")
            if ident:
                other = Path(str(packet).split("packing/resources/web/")[0]) / ident
                row["identical_to"] = ident
                row["identical_to_matches"] = other.exists() and hashlib.sha256(other.read_bytes()).hexdigest() == b["sha256"]
        else:
            row["retained"] = "MISSING"
        if path in pin["stated"]:
            row["issue_stated_sha256_matches"] = pin["stated"][path] == b["sha256"]
        rows.append(row)
    extra_in_packet = sorted(
        str(p.relative_to(packet / "source")) for p in (packet / "source").rglob("*")
        if p.is_file() and str(p.relative_to(packet / "source")).removesuffix(".gz") not in blobs)
    licence_files = [p for p in blobs if LICENCE_NAME.search(p)]
    mentions = {}
    for p, b in blobs.items():
        try:
            text = b["data"].decode("utf-8")
        except UnicodeDecodeError:
            continue
        hits = sorted({m.group(0).lower() for m in LICENCE_WORD.finditer(text)})
        if hits:
            lines = [ln.strip()[:160] for ln in text.split("\n") if LICENCE_WORD.search(ln)]
            mentions[p] = {"words": hits, "lines": lines[:6]}
    return {
        "name": name,
        "issue": pin["issue"],
        "refs": refs,
        "commit_count": len(commits),
        "pinned_commit": meta[0],
        "pinned_commit_is_only_commit": commits == [pin["commit"]],
        "tree": meta[1],
        "sources_json_tree_matches": src.get("git_tree") == meta[1],
        "author": meta[2], "authored": meta[3], "committer": meta[4], "committed": meta[5], "subject": meta[6],
        "sources_json_committed_utc": src.get("committed_utc"),
        "files": rows,
        "file_count": len(blobs),
        "sources_json_file_count_matches": src.get("subtree_file_count") == len(blobs),
        "total_bytes": sum(b["bytes"] for b in blobs.values()),
        "sources_json_total_bytes_matches": src.get("subtree_total_bytes") == sum(b["bytes"] for b in blobs.values()),
        "manifest_paths_equal_tree": sorted(manifest) == sorted(blobs),
        "files_in_packet_source_not_upstream": extra_in_packet,
        "licence_files": licence_files,
        "licence_mentions": mentions,
        "sources_json_license": src.get("license"),
    }


def main() -> int:
    r299, r204, p299, p204, out_p = sys.argv[1:6]
    t0 = time.process_time()
    rows = [one("s299", Path(r299), Path(p299)), one("s204", Path(r204), Path(p204))]
    ok = all(
        r["pinned_commit_is_only_commit"] and r["sources_json_tree_matches"] and r["manifest_paths_equal_tree"]
        and all(f["manifest_matches"] for f in r["files"])
        and all(f.get("retained_matches", True) and f.get("pinned_digest_matches", True)
                and f.get("identical_to_matches", True) and f.get("issue_stated_sha256_matches", True)
                and f["retained"] != "MISSING" for f in r["files"])
        for r in rows)
    receipt = {
        "program": "oz_custody.py",
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python": platform.python_version(),
        "git": subprocess.run(["git", "--version"], capture_output=True, text=True).stdout.strip(),
        "argv": sys.argv[1:],
        "results": rows,
        "verdict": "CUSTODY_HOLDS" if ok else "CUSTODY_GAP",
        "cpu_seconds": round(time.process_time() - t0, 3),
    }
    Path(out_p).write_text(json.dumps(receipt, indent=1) + "\n")
    print(receipt["verdict"])
    for r in rows:
        print(f"{r['name']}: commits {r['commit_count']}, only pin {r['pinned_commit_is_only_commit']}, tree ok "
              f"{r['sources_json_tree_matches']}, files {r['file_count']}, licence files {r['licence_files']}, "
              f"mentions {list(r['licence_mentions'])}")
        for f in r["files"]:
            print("   ", {k: v for k, v in f.items() if k not in ('blob',)})
    return 0


if __name__ == "__main__":
    sys.exit(main())
