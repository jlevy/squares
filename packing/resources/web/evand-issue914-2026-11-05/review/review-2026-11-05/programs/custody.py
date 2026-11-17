"""Custody: the 13 digests against issue #914, the packet against upstream bb4cc78, the licence.

Usage (from packing/, Python 3.14):
  python -I custody.py PACKET_SOURCE_DIR ISSUE_JSON UPSTREAM_DIR OUT.json

Reads, as data: the issue as GitHub's REST API returned it (ISSUE_JSON), the packet's
retained source tree, and UPSTREAM_DIR, which holds this review's own blobless fetch of
evand/square-packing at bb4cc78 (added-files.txt: `git diff --name-status` of the commit
against its parent; upstream-sha256.txt: SHA-256 of `git show bb4cc78:PATH` for every
added file, LICENSE, CREDITS.md and the two checkers; commit-log.txt). Decides nothing
about any bound.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import re
import sys
from pathlib import Path


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> None:
    src, issue_path, up, out = (Path(a) for a in sys.argv[1:5])
    issue = json.loads(issue_path.read_text())
    body = issue["body"]
    table = dict(re.findall(r"\|\s*`([^`]+\.cert)`\s*\|[^|]*\|\s*`([0-9a-f]{64})`\s*\|", body))
    res: dict = {
        "issue": {
            "number": issue["number"],
            "title": issue["title"],
            "user": issue["user"]["login"],
            "created_at": issue["created_at"],
            "updated_at": issue["updated_at"],
            "body_sha256": sha(body.encode()),
            "digests_printed": len(table),
        }
    }
    cand = src / "search/packer/candidates"
    rows = []
    for name, digest in sorted(table.items()):
        p = cand / name
        got = sha(p.read_bytes()) if p.exists() else None
        rows.append({"file": name, "issue": digest, "packet": got, "equal": got == digest})
    res["issue_digests_vs_packet"] = rows
    res["issue_digests_all_equal"] = all(r["equal"] for r in rows) and len(rows) == 13

    added = [line.split("\t") for line in (up / "added-files.txt").read_text().splitlines()]
    res["commit_adds"] = {"files": len(added), "all_added": all(s == "A" for s, _ in added),
                          "all_under_candidates": all(p.startswith("search/packer/candidates/") for _, p in added)}
    upstream = {}
    for line in (up / "upstream-sha256.txt").read_text().splitlines():
        h, p = line.split("  ", 1)
        upstream[p] = h
    cmp = {"equal": [], "equal_after_gunzip": [], "differ": [], "not_in_packet": []}
    for p, h in sorted(upstream.items()):
        f = src / p
        g = src / (p + ".gz")
        if f.exists():
            (cmp["equal"] if sha(f.read_bytes()) == h else cmp["differ"]).append(p)
        elif g.exists():
            (cmp["equal_after_gunzip"] if sha(gzip.decompress(g.read_bytes())) == h else cmp["differ"]).append(p)
        else:
            cmp["not_in_packet"].append(p)
    res["packet_vs_upstream_bb4cc78"] = {k: (len(v) if k != "not_in_packet" and k != "differ" else v) for k, v in cmp.items()}
    # the issue's digests against upstream too
    res["issue_digests_vs_upstream_all_equal"] = all(upstream.get("search/packer/candidates/" + r["file"]) == r["issue"] for r in rows)
    lic = (src / "LICENSE").read_text()
    res["licence"] = {
        "mit_header": lic.startswith("MIT License"),
        "copyright_line": next((ln for ln in lic.splitlines() if ln.startswith("Copyright")), None),
        "sha256": sha(lic.encode()),
        "equal_upstream": upstream.get("LICENSE") == sha((src / "LICENSE").read_bytes()),
    }
    cr = (src / "CREDITS.md").read_text()
    res["credits_md"] = {
        "mentions_Deotte": "Deotte" in cr,
        "mentions_composer": "composer" in cr.lower(),
        "provenance_sentence": next((ln for ln in cr.splitlines() if ln.startswith("Produced by")), None),
        "equal_upstream": upstream.get("CREDITS.md") == sha((src / "CREDITS.md").read_bytes()),
    }
    res["commit_log_head"] = (up / "commit-log.txt").read_text().splitlines()[:6]
    out.write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps({k: v for k, v in res.items() if k != "issue_digests_vs_packet"}, indent=1))


if __name__ == "__main__":
    main()
