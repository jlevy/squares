"""Custody and licence of the five source repositories of issues 927 to 931 (lane L64).

Usage: python -I -B l64_custody.py STATEMENTS.json SRC_DIR OUT.json

Read-only git plumbing (`rev-parse`, `log`, `ls-tree`, `cat-file`) on the clones made
for this review; nothing in the clones is run. For each repository it records the
commit, tree, parents, author and dates, every file's blob and SHA-256, and checks:

- the commit is the issue's pin, and the only commit;
- the certificate's SHA-256 is the issue's, and the JSON twin's is the README's;
- the working-tree bytes are the committed blobs;
- `verifier/sqcheck.py`, `verifier/README.md` and `LICENSE.md` are one blob across all
  five (hashed only; the verifier is not read here);
- what `LICENSE.md` licenses, read as text.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from l64_util import Clock, environment, program_digests, write_receipt  # noqa: E402

HERE = Path(__file__).resolve().parent


def git(repo: Path, *args: str) -> bytes:
    return subprocess.run(  # noqa: S603 - fixed git plumbing, no shell
        ["git", "-C", str(repo), *args],  # noqa: S607
        check=True,
        capture_output=True,
    ).stdout


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(__doc__)
        return 2
    statements = json.loads(Path(argv[1]).read_text())["counts"]
    src, out = Path(argv[2]), argv[3]
    clock = Clock()
    rows = {}
    shared: dict[str, set[str]] = {"verifier/sqcheck.py": set(), "verifier/README.md": set(), "LICENSE.md": set()}
    for n_text, st in statements.items():
        repo = src / st["repo"]
        head = git(repo, "rev-parse", "HEAD").decode().strip()
        commits = git(repo, "rev-list", "--all").decode().split()
        meta = git(repo, "log", "-1", "--format=%T%n%P%n%an <%ae>%n%aI%n%cn <%ce>%n%cI%n%s", "HEAD").decode().splitlines()
        files = {}
        for line in git(repo, "ls-tree", "-r", "-l", "HEAD").decode().splitlines():
            info, path = line.split("\t", 1)
            mode, kind, blob, size = info.split()
            data = git(repo, "cat-file", "blob", blob)
            disk = (repo / path).read_bytes()
            files[path] = {
                "mode": mode,
                "blob": blob,
                "bytes": int(size),
                "sha256": hashlib.sha256(data).hexdigest(),
                "working_tree_equals_blob": disk == data,
            }
            if path in shared:
                shared[path].add(blob)
        readme = (repo / "README.md").read_text(encoding="utf-8")
        twin_digest = re.search(rf"`{re.escape(st['twin'])}` `([0-9a-f]{{64}})`", readme)
        cert_digest = re.search(rf"`{re.escape(st['certificate'])}` `([0-9a-f]{{64}})`", readme)
        rows[n_text] = {
            "repo": f"kenaznia-doga/{st['repo']}",
            "head": head,
            "head_is_issue_pin": head == st["commit"],
            "commits": len(commits),
            "tree": meta[0],
            "parents": meta[1],
            "author": meta[2],
            "authored": meta[3],
            "committer": meta[4],
            "committed": meta[5],
            "subject": meta[6],
            "files": files,
            "certificate_sha256_is_issue": files[st["certificate"]]["sha256"] == st["sha256"],
            "certificate_sha256_in_readme": bool(cert_digest) and cert_digest.group(1) == files[st["certificate"]]["sha256"],
            "twin_sha256_in_readme": twin_digest.group(1) if twin_digest else None,
            "twin_sha256_is_readme": bool(twin_digest) and twin_digest.group(1) == files[st["twin"]]["sha256"],
            "has_licence_file": "LICENSE.md" in files,
        }
    licence = (src / statements["232"]["repo"] / "LICENSE.md").read_text(encoding="utf-8")
    receipt = {
        "program": "l64_custody.py",
        "programs_sha256": program_digests([HERE / "l64_custody.py", HERE / "l64_util.py"]),
        "environment": environment(),
        "repositories": rows,
        "one_blob_across_five": {path: sorted(blobs) for path, blobs in shared.items()},
        "licence_text": licence,
        "licence_grants": {
            "cc_by_4_0_for_non_code": "Creative Commons Attribution 4.0" in licence
            and "Certificates, witnesses, receipts, data and write-ups" in licence,
            "mit_for_code": "MIT licence" in licence and "Source code" in licence,
            "copyright": next((ln for ln in licence.splitlines() if "Copyright" in ln), None),
        },
        "clock": clock.report(),
    }
    ok = all(
        r["head_is_issue_pin"]
        and r["commits"] == 1
        and r["parents"] == ""
        and r["certificate_sha256_is_issue"]
        and r["twin_sha256_is_readme"]
        and all(f["working_tree_equals_blob"] for f in r["files"].values())
        for r in rows.values()
    ) and all(len(b) == 1 for b in shared.values())
    receipt["verdict"] = "CUSTODY_HOLDS" if ok else "CUSTODY_QUESTIONS"
    write_receipt(out, receipt)
    print(receipt["verdict"])
    for n_text, r in rows.items():
        print(
            n_text,
            r["head"][:12],
            r["commits"],
            r["committed"],
            "cert",
            r["certificate_sha256_is_issue"],
            "twin",
            r["twin_sha256_is_readme"],
            r["subject"],
        )
    print("shared blobs:", receipt["one_blob_across_five"])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
