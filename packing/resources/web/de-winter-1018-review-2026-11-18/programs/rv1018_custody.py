"""Custody of #1018's files: digests, and what the bundle shares byte for byte with jlevy/squares.

Lane r108-1118, blind review of jlevy/squares#1018. Decides nothing about the bound. It
records the SHA-256 of every file of the source's `lower_n108/` at the pin, compares the
bundled `sqverify_fast/` files, `evidence/SOUNDNESS.md` and the licence with this
repository's files at stated commits (read with `git show`, as bytes), compares the
source's copy of T-216's measure with the retained one, lists the files the README names
that the folder lacks, and lists what the repository's crate holds that the bundle does
not. It reads no code: files are compared as bytes.

Usage: python -I rv1018_custody.py --source DIR/lower_n108 --repo REPO --commit C [...]
         --retained-base PATH --out OUT.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

CRATE = "packing/sqverify_fast"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_bytes(repo: Path, commit: str, path: str) -> bytes | None:
    res = subprocess.run(
        ["git", "-C", str(repo), "show", f"{commit}:{path}"], capture_output=True, check=False
    )
    return res.stdout if res.returncode == 0 else None


def git_list(repo: Path, commit: str, path: str) -> list[str]:
    res = subprocess.run(
        ["git", "-C", str(repo), "ls-tree", "-r", "--name-only", commit, path],
        capture_output=True,
        text=True,
        check=True,
    )
    return [p[len(path) + 1 :] for p in res.stdout.split()]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--commit", action="append", required=True)
    ap.add_argument("--retained-base", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    src, repo = Path(args.source), Path(args.repo)
    files = sorted(p for p in src.rglob("*") if p.is_file())
    digests = {str(p.relative_to(src)): sha(p.read_bytes()) for p in files}
    bundle = sorted(
        str(p.relative_to(src / "sqverify_fast")) for p in (src / "sqverify_fast").rglob("*")
        if p.is_file()
    )
    crate_cmp = {}
    for commit in args.commit:
        rows = {}
        for rel in bundle:
            mine = (src / "sqverify_fast" / rel).read_bytes()
            theirs = git_bytes(repo, commit, f"{CRATE}/{rel}")
            rows[rel] = "identical" if theirs == mine else (
                "absent" if theirs is None else "differs"
            )
        repo_files = git_list(repo, commit, CRATE)
        crate_cmp[commit] = {
            "bundle_files": rows,
            "all_bundled_crate_sources_identical": all(
                v == "identical" for k, v in rows.items() if k != "LICENSE"
            ),
            "in_repository_not_in_bundle": sorted(set(repo_files) - set(bundle)),
        }
    docs = {}
    for commit in args.commit:
        sound = git_bytes(repo, commit, f"{CRATE}/SOUNDNESS.md")
        lic = git_bytes(repo, commit, "LICENSE")
        docs[commit] = {
            "evidence/SOUNDNESS.md": sound == (src / "evidence/SOUNDNESS.md").read_bytes(),
            "evidence/squares-project-license.txt": lic
            == (src / "evidence/squares-project-license.txt").read_bytes(),
            "sqverify_fast/LICENSE": lic == (src / "sqverify_fast/LICENSE").read_bytes(),
        }
    base_raw = Path(args.retained_base).read_bytes()
    copy_raw = (src / "evidence/Hosono_n108.json.gz").read_bytes()
    readme = (src / "README.md").read_text()
    named = sorted(set(re.findall(r"`([A-Za-z0-9_./-]+\.[A-Za-z0-9]+|SHA256SUMS)`", readme)))
    missing = [n for n in named if not (src / n).exists() and not list(src.rglob(Path(n).name))]
    out = {
        "program": "rv1018_custody.py",
        "source_files": digests,
        "file_count": len(digests),
        "crate_comparison": crate_cmp,
        "documents": docs,
        "hosono_copy_sha256": sha(copy_raw),
        "retained_T216_sha256": sha(base_raw),
        "hosono_copy_is_retained_T216": sha(copy_raw) == sha(base_raw),
        "readme_names": named,
        "readme_names_missing_from_folder": missing,
    }
    Path(args.out).write_text(json.dumps(out, indent=1) + "\n")
    print(
        "crate identical:",
        {c: v["all_bundled_crate_sources_identical"] for c, v in crate_cmp.items()},
        "T216 copy identical:",
        out["hosono_copy_is_retained_T216"],
        "missing:",
        missing,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
