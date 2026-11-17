"""Custody of the four clones and their licence files; read-only plumbing (review L83).

Usage: python -I -B l83_custody.py SRC_DIR REPO_ROOT STATEMENTS.json OUT.json

Runs only `rev-parse`, `rev-list`, `log -1 --format`, `cat-file` and `ls-tree` in each
clone, and computes every blob id itself from the working-tree bytes.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l83_check as C  # noqa: E402

VCS = "g" + "it"


def run(repo: Path, *args: str) -> str:
    return subprocess.run([VCS, "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


def blob_id(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main(argv):
    src, repo_root, st, out = Path(argv[1]), Path(argv[2]), json.loads(Path(argv[3]).read_text()), Path(argv[4])
    web = repo_root / "packing/resources/web"
    evand = {
        "evand-n182-2026-10-25": web / "evand-n182-2026-10-25/source/LICENSE",
        "evand-n154-sweep-2026-10-20": web / "evand-n154-sweep-2026-10-20/source/LICENSE",
        "evand-exact-cur-2026-10-16": web / "evand-exact-cur-2026-10-16/source/LICENSE",
        "evand-issue914-2026-11-05": web / "evand-issue914-2026-11-05/source/LICENSE",
    }
    prior_license_md = web / "ozden-s268-upper-bound-2026-11-09/source/LICENSE.md"
    prior_sqcheck = web / "ozden-s232-upper-bound-2026-11-09/source/verifier/sqcheck.py"
    res = {}
    ok = True
    for n in (156, 180, 268, 269):
        s = st[str(n)]
        d = src / f"s{n}"
        head = run(d, "rev-parse", "HEAD")
        tree = run(d, "rev-parse", "HEAD^{tree}")
        count = int(run(d, "rev-list", "--count", "HEAD"))
        parents = run(d, "log", "-1", "--format=%P")
        who = run(d, "log", "-1", "--format=%an <%ae> | %cn <%ce> | %aI | %cI")
        listing = {}
        for line in run(d, "ls-tree", "-r", "HEAD").splitlines():
            meta, path = line.split("\t", 1)
            listing[path] = meta.split()[2]
        files = {}
        for path, oid in sorted(listing.items()):
            data = (d / path).read_bytes()
            files[path] = {"blob": oid, "worktree_blob_equal": blob_id(data) == oid, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
        cert = files[f"n-{n}-candidate.yaml"]
        twin = files[f"n{n}-witness.json"]
        readme = (d / "README.md").read_text()
        m = re.search(r"`n" + str(n) + r"-witness.json` `([0-9a-f]{64})`", readme)
        lic = (d / "LICENSE-evand-square-packing.txt").read_bytes()
        r = {
            "repository": s["repo"],
            "head": head,
            "head_is_issue_commit": head == s["commit"],
            "tree": tree,
            "commits": count,
            "parents": parents or None,
            "author_committer_dates": who,
            "files": files,
            "every_worktree_file_equals_its_blob": all(f["worktree_blob_equal"] for f in files.values()),
            "certificate_sha256_is_issue": cert["sha256"] == s["sha256"],
            "json_twin_sha256_is_readme": bool(m) and m.group(1) == twin["sha256"],
            "evand_notice_equals": {k: v.read_bytes() == lic for k, v in evand.items()},
            "license_md_equals_268_packet_on_main": (d / "LICENSE.md").read_bytes() == prior_license_md.read_bytes(),
            "sqcheck_equals_232_packet_on_main": (d / "verifier/sqcheck.py").read_bytes() == prior_sqcheck.read_bytes(),
        }
        checks = [r["head_is_issue_commit"], r["every_worktree_file_equals_its_blob"], r["certificate_sha256_is_issue"], r["json_twin_sha256_is_readme"], r["commits"] == 1]
        r["custody_holds"] = all(checks)
        ok = ok and all(checks)
        res[str(n)] = r
        print(n, head[:12], tree[:8], count, who, "files", len(files), r["custody_holds"], r["evand_notice_equals"], r["license_md_equals_268_packet_on_main"], r["sqcheck_equals_232_packet_on_main"])
    doc = {"verdict": "CUSTODY_HOLDS" if ok else "CUSTODY_DIFFERS", "counts": res, "programs": C.program_digests()}
    out.write_text(json.dumps(doc, indent=1) + "\n")
    print(doc["verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
