"""Custody and licence of the two source repositories (lane L72, bead think-qqyg).

Usage: python -I -B l72_custody.py STATEMENTS.json SRC REPO_ROOT OUT.json

Read-only git plumbing (rev-parse, rev-list, cat-file, ls-tree) on clones of the two
repositories, git blob ids of the working files computed here, SHA-256s against the issues'
and READMEs' statements, and the licence files against the copies this repository retains.
Runs nothing from the clones. Decides no bound.
"""

import hashlib
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l72_util as util  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SAFE_ENV = {"PATH": "/usr/bin:/bin", "GIT_CONFIG_NOSYSTEM": "1", "HOME": "/nonexistent", "LC_ALL": "C"}


def git(repo, *args):
    out = subprocess.run(
        ["git", "-C", repo, "-c", "core.hooksPath=/dev/null", *args],
        capture_output=True,
        check=True,
        env=SAFE_ENV,
    )
    return out.stdout.decode("utf-8")


def blob_id(path):
    with open(path, "rb") as fh:
        data = fh.read()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main(argv):
    statements = json.load(open(argv[1]))
    src, repo_root, out = argv[2], argv[3], argv[4]
    report = {"program": "l72_custody.py", "lane": "L72", "bead": "think-qqyg", "environment": util.environment()}
    report["program_digests"] = util.program_digests([os.path.join(HERE, "l72_custody.py"), os.path.join(HERE, "l72_util.py"), argv[1]])
    problems = []
    blobs_by_path = {}
    for count in ("172", "270"):
        st = statements[count]
        name = st["repository"].split("/")[1]
        repo = os.path.join(src, name)
        head = git(repo, "rev-parse", "HEAD").strip()
        tree = git(repo, "rev-parse", "HEAD^{tree}").strip()
        commits = git(repo, "rev-list", "--all").split()
        raw_commit = git(repo, "cat-file", "-p", head)
        header, _, message = raw_commit.partition("\n\n")
        fields = {}
        parents = []
        for line in header.split("\n"):
            key, _, value = line.partition(" ")
            if key == "parent":
                parents.append(value)
            else:
                fields[key] = value
        entries = []
        for line in git(repo, "ls-tree", "-r", "-l", "HEAD").strip().split("\n"):
            meta, path = line.split("\t", 1)
            mode, typ, obj, size = meta.split()
            work = os.path.join(repo, path)
            entries.append(
                {
                    "path": path,
                    "mode": mode,
                    "blob": obj,
                    "size": int(size),
                    "working_file_equals_blob": os.path.exists(work) and blob_id(work) == obj,
                    "sha256": util.sha256_file(work),
                }
            )
            blobs_by_path.setdefault(path.replace(count, "NNN"), {})[count] = obj
        by_path = {e["path"]: e for e in entries}
        cert = by_path[st["certificate"]]
        twin = by_path[st["json_twin"]]
        row = {
            "repository": st["repository"],
            "pin_stated": st["pin"],
            "head": head,
            "tree": tree,
            "commits_reachable": len(commits),
            "parents": parents,
            "author": fields.get("author"),
            "committer": fields.get("committer"),
            "message": message.strip(),
            "files": entries,
            "certificate_sha256_equals_issue": cert["sha256"] == st["certificate_sha256"],
            "twin_sha256_equals_readme": twin["sha256"] == st["json_twin_sha256_readme"],
            "every_working_file_equals_its_blob": all(e["working_file_equals_blob"] for e in entries),
        }
        if head != st["pin"]:
            problems.append(f"{count}: HEAD {head} is not the pin")
        if len(commits) != 1 or parents:
            problems.append(f"{count}: history is not one parentless commit")
        if not row["certificate_sha256_equals_issue"]:
            problems.append(f"{count}: certificate digest differs from the issue's")
        if not row["twin_sha256_equals_readme"]:
            problems.append(f"{count}: twin digest differs from the README's")
        if not row["every_working_file_equals_its_blob"]:
            problems.append(f"{count}: a working file differs from its blob")
        report[count] = row
    # identity across the two repositories
    shared = {p: v for p, v in blobs_by_path.items() if len(v) == 2}
    report["same_blob_in_both"] = sorted(p for p, v in shared.items() if v["172"] == v["270"])
    report["different_blob"] = sorted(p for p, v in shared.items() if v["172"] != v["270"])
    # against copies this repository retains (blob ids computed from the files on disk)
    retained = {
        "LICENSE-evand-square-packing.txt": [
            "packing/resources/web/evand-issue845-2026-10-29/source/LICENSE",
            "packing/resources/web/evand-n270-sweep-2026-10-20/source/LICENSE",
        ],
        "LICENSE.md": ["packing/resources/web/ozden-s232-upper-bound-2026-11-09/source/LICENSE.md"],
        "verifier/sqcheck.py": ["packing/resources/web/ozden-s232-upper-bound-2026-11-09/source/verifier/sqcheck.py"],
    }
    comparisons = []
    for path, copies in retained.items():
        mine = shared.get(path, {}).get("172")
        for c in copies:
            full = os.path.join(repo_root, c)
            theirs = blob_id(full) if os.path.exists(full) else None
            comparisons.append({"source_path": path, "retained_copy": c, "source_blob": mine, "retained_blob": theirs, "equal": mine == theirs})
    report["retained_copies"] = comparisons
    report["problems"] = problems
    report["verdict"] = "CUSTODY_HOLDS" if not problems else "CUSTODY_PROBLEMS"
    util.write_receipt(out, report)
    print(report["verdict"], problems)
    for c in comparisons:
        print(c["source_path"], "==", c["retained_copy"], c["equal"])
    print("same blob in both:", report["same_blob_in_both"])
    print("different:", report["different_blob"])
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
