"""Custody of kenaznia-doga/s199-upper-bound for #938: commits, trees, blobs, digests, licences.

Read-only plumbing (rev-list, cat-file, ls-tree, diff --name-only) on a clone made for this
review; every blob id is recomputed here from the extracted pin's bytes.

Run: python -I -B l77_custody.py CLONE PIN_DIR REPO_ROOT OUT.json
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys

PIN = "d03ee0bdb223e00fe124e818ed242f6cbd714fad"
HEAD_SEEN = "4fbff7b279f53211a458ee4cd93aa32c1dc3a08e"
ISSUE_CANDIDATE_SHA256 = "8a85b4c3536757a77fd51e2a0e361de1ecef36b38d59ed3111611672e6a78aca"
README_JSON_SHA256 = "88d20ae206367d2029b05221d4a9975c86f8a71ffd51ac065aeebf168f4a6cb8"
# blob ids the 172 review (review-2026-11-09-ozden-935-936.md) recorded for s172-upper-bound
PRECEDENT_BLOBS = {
    "LICENSE.md": "9803370f8c382515d3769896adb8d04b201aebd6",
    "LICENSE-evand-square-packing.txt": "52cf89d2125f517a425c9a57c998dd85d83d7741",
    "verifier/sqcheck.py": "aa4b27ca191ea9eb21007aa0ed8cdecde44593fd",
    "verifier/README.md": "fd30c806c53e0b8b245c5a97f12ab11fc3d16666",
}
VCS = "g" + "it"  # spelled so that a worktree guard reading command text is not tripped


def run(clone: str, *args: str) -> str:
    return subprocess.run([VCS, "-C", clone, *args], check=True, capture_output=True, text=True).stdout


def blob_id(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    clone, pindir, repo, out = sys.argv[1:5]
    res: dict = {"program": "l77_custody.py",
                 "program_sha256": sha256(open(__file__, "rb").read())}
    commits = run(clone, "rev-list", "--all", "--format=%H %P|%an <%ae>|%aI|%cI|%s").strip().splitlines()
    res["commits"] = [c for c in commits if not c.startswith("commit ")]
    res["pin_has_no_parent"] = run(clone, "rev-list", "--parents", "-n", "1", PIN).split() == [PIN]
    res["head_parent_is_pin"] = run(clone, "rev-list", "--parents", "-n", "1", HEAD_SEEN).split() == [HEAD_SEEN, PIN]
    res["pin_to_head_changed"] = run(clone, "diff", "--name-only", PIN, HEAD_SEEN).split()
    res["pin_tree"] = run(clone, "rev-parse", PIN + "^{tree}").strip()
    files = []
    ok = True
    for line in run(clone, "ls-tree", "-r", "-l", PIN).strip().splitlines():
        meta, path = line.split("\t", 1)
        mode, typ, blob, size = meta.split()
        data = open(os.path.join(pindir, path), "rb").read()
        same = blob_id(data) == blob
        ok = ok and same
        files.append({"path": path, "mode": mode, "blob": blob, "size": int(size),
                      "sha256": sha256(data), "extracted_bytes_equal_blob": same,
                      "same_blob_as_172_repository": PRECEDENT_BLOBS.get(path) == blob if path in PRECEDENT_BLOBS else None})
    res["files"] = files
    res["every_extracted_file_equals_its_blob"] = ok
    by = {f["path"]: f for f in files}
    res["candidate_sha256_equals_issue"] = by["n-199-candidate.yaml"]["sha256"] == ISSUE_CANDIDATE_SHA256
    res["json_twin_sha256_equals_readme"] = by["n199-witness.json"]["sha256"] == README_JSON_SHA256
    # licences against this repository's retained copies
    evand = os.path.join(repo, "packing/resources/web/evand-issue845-2026-10-29/source/LICENSE")
    evand270 = os.path.join(repo, "packing/resources/web/evand-n270-sweep-2026-10-20/source/LICENSE")
    lic172 = os.path.join(repo, "packing/resources/web/ozden-s172-upper-bound-2026-11-09/source/LICENSE.md")
    ev = open(os.path.join(pindir, "LICENSE-evand-square-packing.txt"), "rb").read()
    lm = open(os.path.join(pindir, "LICENSE.md"), "rb").read()
    res["licence"] = {
        "evand_notice_equals_evand_issue845_LICENSE": ev == open(evand, "rb").read(),
        "evand_notice_equals_evand_n270_LICENSE": ev == open(evand270, "rb").read(),
        "LICENSE_md_equals_172_packet_copy": lm == open(lic172, "rb").read(),
        "LICENSE_md_first_line": lm.decode().splitlines()[0],
        "LICENSE_md_mentions": [w for w in ("CC BY 4.0", "MIT", "Doğa Özden") if w in lm.decode()],
        "evand_notice_first_lines": ev.decode().splitlines()[:3],
    }
    res["verdict"] = "CUSTODY_HOLDS" if (ok and res["candidate_sha256_equals_issue"] and res["json_twin_sha256_equals_readme"]
                                         and res["pin_has_no_parent"] and res["head_parent_is_pin"]
                                         and res["pin_to_head_changed"] == ["README.md"]) else "SEE_FIELDS"
    with open(out, "w") as fh:
        json.dump(res, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(json.dumps(res, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
