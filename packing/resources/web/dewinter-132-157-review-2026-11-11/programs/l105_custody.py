"""Lane L105, after the freeze: custody, licence and dating. Decides no packing.

Usage: python -I -B l105_custody.py SOURCE_CLONE SEED_CLONE REPO_DIR OUT_JSON

Runs read-only Git plumbing (`rev-parse`, `log -1`, `ls-tree`, `diff --name-status`,
`cat-file`) on the clone of JoostdeWinter/square-packing made for this review, on the
clone of Samanyu-dev/squares_in_squares at the seed's commit, and reads this
repository's retained copies of the author's LICENSE. It computes every blob id and
SHA-256 itself and holds each folder's files to its SHA256SUMS.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


def blob_id(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def commit_info(repo: Path, rev: str) -> dict[str, Any]:
    fmt = "%H%n%P%n%T%n%an%n%aI%n%cn%n%cI%n%s"  # names only: no e-mail addresses in the receipt
    h, parents, tree, author, adate, committer, cdate, subject = git(repo, "log", "-1", f"--format={fmt}", rev).split("\n")
    return {"commit": h, "parents": parents.split(), "tree": tree, "author": author, "authored": adate, "committer": committer, "committed": cdate, "subject": subject}


def main() -> None:
    src, seed, repo, outp = (Path(a) for a in sys.argv[1:5])
    out: dict[str, Any] = {"program": "l105_custody.py"}
    head = git(src, "rev-parse", "HEAD")
    out["source_head"] = head
    out["working_tree_clean"] = git(src, "status", "--porcelain") == ""
    out["commits"] = {r: commit_info(src, r) for r in ("6617869", "a491dad")}
    out["a491dad_to_6617869"] = git(src, "diff", "--name-status", "a491dad", "6617869").splitlines()
    out["first_commit_of_each_file"] = {}
    folders = {}
    for folder in ("n132", "n157"):
        sums = {}
        for line in (src / folder / "SHA256SUMS").read_text().splitlines():
            digest, name = line.split()
            sums[name] = digest
        files = {}
        for line in git(src, "ls-tree", "HEAD", f"{folder}/").splitlines():
            meta, path = line.split("\t")
            _, _, oid = meta.split()
            data = (src / path).read_bytes()
            name = Path(path).name
            files[name] = {
                "blob": oid,
                "blob_computed_equal": blob_id(data) == oid,
                "sha256": hashlib.sha256(data).hexdigest(),
                "sha256sums_line_equal": sums.get(name) == hashlib.sha256(data).hexdigest() if name != "SHA256SUMS" else None,
                "bytes": len(data),
            }
            first = git(src, "log", "--diff-filter=A", "--format=%h %cI", "--", path).splitlines()
            out["first_commit_of_each_file"][path] = first[-1] if first else None
        folders[folder] = {"files": files, "sha256sums_entries": len(sums), "all_listed_equal": all(v["sha256sums_line_equal"] for k, v in files.items() if k != "SHA256SUMS")}
    out["folders"] = folders
    out["verify_exact_identical"] = folders["n132"]["files"]["verify_exact.py"]["sha256"] == folders["n157"]["files"]["verify_exact.py"]["sha256"]
    lic = (src / "LICENSE").read_bytes()
    readme = (src / "README.md").read_text()
    retained = {}
    for p in sorted((repo / "packing" / "resources" / "web").glob("de-winter-*/**/LICENSE")):
        retained[str(p.relative_to(repo))] = hashlib.sha256(p.read_bytes()).hexdigest()
    out["licence"] = {
        "LICENSE_blob": git(src, "rev-parse", "HEAD:LICENSE"),
        "LICENSE_sha256": hashlib.sha256(lic).hexdigest(),
        "LICENSE_first_line": lic.decode().splitlines()[0],
        "LICENSE_copyright": next((ln for ln in lic.decode().splitlines() if ln.startswith("Copyright")), None),
        "LICENSE_first_commit": git(src, "log", "--diff-filter=A", "--format=%h %cI", "--", "LICENSE").splitlines()[-1],
        "root_readme_licence_line": next((ln for ln in readme.splitlines() if "licence" in ln.lower()), None),
        "root_readme_rows": [ln for ln in readme.splitlines() if ln.startswith("| [132]") or ln.startswith("| [157]")],
        "retained_copies_here": retained,
        "equals_every_retained_copy": all(v == hashlib.sha256(lic).hexdigest() for v in retained.values()) and bool(retained),
    }
    # The seed
    csv_path = seed / "best_fit_101_500.csv"
    data = csv_path.read_bytes()
    out["seed"] = {
        "head": git(seed, "rev-parse", "HEAD"),
        "commit": commit_info(seed, "HEAD"),
        "csv_blob": git(seed, "rev-parse", "HEAD:best_fit_101_500.csv"),
        "csv_blob_computed_equal": blob_id(data) == git(seed, "rev-parse", "HEAD:best_fit_101_500.csv"),
        "csv_sha256": hashlib.sha256(data).hexdigest(),
        "licence_files_at_root": [ln.split("\t")[1] for ln in git(seed, "ls-tree", "HEAD").splitlines() if ln.split("\t")[1].upper().startswith(("LICENSE", "LICENCE", "COPYING"))],
        "readme_licence_line": next((ln for ln in (seed / "README.md").read_text().splitlines() if ln.startswith("Our own code is MIT")), None),
        "summary_row_109": next((ln for ln in (seed / "best_fit_summary.csv").read_text().splitlines() if ln.startswith("109,")), None),
    }
    out["dating"] = {
        "first_commit": "a491dad",
        "first_commit_committed": out["commits"]["a491dad"]["committed"],
        "push_time": "not read: the GitHub API refused the source repository in this session (HTTP 403)",
    }
    outp.write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: out[k] for k in ("source_head", "working_tree_clean", "a491dad_to_6617869", "verify_exact_identical")}))
    print(json.dumps({f: v["all_listed_equal"] for f, v in folders.items()}), json.dumps(out["licence"], indent=None)[:600])
    print(json.dumps(out["seed"])[:700])
    print(json.dumps(out["commits"]))


if __name__ == "__main__":
    main()
