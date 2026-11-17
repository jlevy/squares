#!/usr/bin/env python3
"""Custody of n260.cert: read-only git plumbing on a bare clone of vitamoon/vitamoon.

A premise check for the review; it decides nothing about the bound. It records the
clone's head, every commit with its author and the files it changes, the blob and
SHA-256 of n260.cert at each commit that has it, and compares them with the packet's
retained copy and manifest. It also records the blob and SHA-256 of this repository's
devtools/check_rational_witness_independent.py at e6e8d577 (the commit the author says
he ran) and at the checkout's HEAD, read with git, not run.

Usage (from the repository root):
  python -I custody.py --clone VITAMOON.git --packet PACKET_DIR --repo . --out RECEIPT.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import resource
import subprocess
import sys
import time
from pathlib import Path

AUTHOR_CHECK_COMMIT = "e6e8d57726db80cd0e6a1523166a96c5d36a3119"
CHECKER = "packing/devtools/check_rational_witness_independent.py"


def git(repo, *args, text=True):
    out = subprocess.run(["git", "--git-dir" if repo.endswith(".git") else "-C", repo, *args],
                         check=True, capture_output=True)
    return out.stdout.decode() if text else out.stdout


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clone", required=True)
    ap.add_argument("--packet", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    t0 = time.time()
    clone = str(Path(args.clone).resolve())
    head = git(clone, "rev-parse", "main").strip()
    log = git(clone, "log", "--format=%H%x09%cI%x09%an%x09%ae%x09%s", "main").strip().splitlines()
    commits = []
    for line in log:
        sha, when, name, email, subject = line.split("\t")
        changed = git(clone, "diff-tree", "--no-commit-id", "--name-status", "-r", "--root", sha).strip().splitlines()
        rec = {"commit": sha, "committed": when, "author": name, "email": email, "subject": subject,
               "changes": changed}
        tree = git(clone, "ls-tree", sha).strip().splitlines()
        for entry in tree:
            meta, path = entry.split("\t")
            if path == "n260.cert":
                blob = meta.split()[2]
                data = git(clone, "cat-file", "blob", blob, text=False)
                rec["n260_cert"] = {"blob": blob, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
        commits.append(rec)
        if sha.startswith("e7cab3a"):
            break
    retained = Path(args.packet) / "source" / "n260.cert"
    data = retained.read_bytes()
    manifest = (Path(args.packet) / "acquisition" / "upstream-subtree.sha256").read_text().split()
    sources = json.loads((Path(args.packet) / "acquisition" / "sources.json").read_text())
    retained_sha = hashlib.sha256(data).hexdigest()
    with_file = [c for c in commits if "n260_cert" in c]
    checker = {}
    for ref in (AUTHOR_CHECK_COMMIT, "HEAD"):
        blob = git(args.repo, "rev-parse", f"{ref}:{CHECKER}").strip()
        body = git(args.repo, "cat-file", "blob", blob, text=False)
        checker[ref] = {"blob": blob, "sha256": hashlib.sha256(body).hexdigest()}
    out = {
        "program": "custody.py", "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python": platform.python_version(), "clone_head_main": head,
        "pinned_commit": sources["sources"][0]["source_commit"],
        "head_is_pin": head == sources["sources"][0]["source_commit"],
        "commits_from_pin_back_to_first_with_file": commits,
        "n260_cert_identical_at_every_commit": len({c["n260_cert"]["sha256"] for c in with_file}) == 1,
        "retained": {"sha256": retained_sha, "bytes": len(data)},
        "retained_matches_clone": all(c["n260_cert"]["sha256"] == retained_sha for c in with_file),
        "retained_matches_manifest": manifest[0] == retained_sha,
        "authors": sorted({(c["author"], c["email"]) for c in commits}),
        "author_check_program": checker,
        "author_check_program_unchanged_at_head": checker[AUTHOR_CHECK_COMMIT]["blob"] == checker["HEAD"]["blob"],
        "custody_holds": head == sources["sources"][0]["source_commit"]
        and all(c["n260_cert"]["sha256"] == retained_sha for c in with_file) and manifest[0] == retained_sha,
    }
    usage = resource.getrusage(resource.RUSAGE_SELF)
    out["cpu_seconds_total"] = round(usage.ru_utime + usage.ru_stime, 3)
    out["wall_seconds"] = round(time.time() - t0, 3)
    Path(args.out).write_text(json.dumps(out, indent=1, default=list) + "\n")
    print(json.dumps({k: out[k] for k in ("clone_head_main", "head_is_pin", "n260_cert_identical_at_every_commit",
                                           "retained_matches_clone", "retained_matches_manifest", "authors",
                                           "author_check_program_unchanged_at_head", "custody_holds")}, default=list))
    for c in commits:
        print(c["commit"][:9], c["committed"], c["email"], c["subject"], c["changes"], c.get("n260_cert", {}).get("blob"))
    return 0 if out["custody_holds"] else 1


if __name__ == "__main__":
    sys.exit(main())
