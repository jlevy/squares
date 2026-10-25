"""Which files of the source's adapted verifier equal this repository's crate (premises).

The source's nested archive, check2/src/sqverify-proof-net-fe12e036c.tar.gz, is pinned by
digest and not retained, and this review did not open it. The 8 October facts packet's
source-manifest.json records the SHA-256 of each of its 20 files. This program hashes
this repository's packing/sqverify_fast files at a named commit (by `git show`, from the
repository root) and reports which archive files are byte-identical to them, and the sizes
of those that are not. It reads no code: it compares digests.

    python3 -I crate_identity.py --manifest FACTS/source-manifest.json --repo REPO \
        --commit e020eb1e2 --out outputs/crate-identity.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def blob(repo: Path, commit: str, path: str) -> bytes | None:
    out = subprocess.run(
        ["git", "-C", str(repo), "show", f"{commit}:packing/sqverify_fast/{path}"],
        capture_output=True,
        check=False,
    )
    return out.stdout if out.returncode == 0 else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--commit", action="append", required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    manifest = json.loads(args.manifest.read_text())
    source = manifest["common_verifier_source"]
    files = {f["path"].removeprefix("sqverify_fast/"): f for f in source["files"]}
    report: dict[str, object] = {
        "kind": "t233-review-crate-identity/v1",
        "archive": {k: source[k] for k in ("archive_path", "sha256", "declared_commit")},
        "upstream_commit_text": source.get("inner_bundle_upstream_commit", {}).get("text"),
        "commits": {},
    }
    for commit in args.commit:
        rows = []
        for path, f in files.items():
            here = blob(args.repo, commit, path)
            rows.append({
                "path": path,
                "archive_bytes": f["bytes"],
                "here_bytes": None if here is None else len(here),
                "identical": here is not None and hashlib.sha256(here).hexdigest() == f["sha256"],
            })
        same = [r["path"] for r in rows if r["identical"]]
        differ = [r for r in rows if not r["identical"]]
        report["commits"][commit] = {"identical": same, "differ": differ}
        print(commit, f"{len(same)} of {len(rows)} identical; differ:",
              ", ".join(f"{r['path']} ({r['here_bytes']} here, {r['archive_bytes']} archived)"
                        for r in differ))
    args.out.write_text(json.dumps(report, indent=1, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
