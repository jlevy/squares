"""Custody of the vitamoon files for the L70 review.

Inputs: the two extracted trees (SRC/ac14112, SRC/78eb9ea) and, as text, the outputs of
read-only git plumbing on a bare clone, saved beside them:
``git ls-tree -l <commit>`` for 78eb9ea, e4209f6, c10e094, 546928a and ac14112, and
``git log --format='%H|%T|%P|%an|%ae|%aI|%cn|%ce|%cI|%s' -8 ac14112``.

Checks: every extracted file's git blob id equals its tree entry; every SHA-256 the
source's SHA256SUMS and packing-certificates.json state equals the bytes; the text
copies equal their certificates; the eleven beyond-horizon blobs do not change from
78eb9ea to ac14112; and when each certificate blob first appears.

Usage: python -I l70_custody.py --src SRC --plumbing DIR --out custody.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import l70_check as C  # noqa: E402

COMMITS = ("78eb9ea", "e4209f6", "c10e094", "546928a", "ac14112")


def blob_id(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()  # noqa: S324 - git's object id


def ls_tree(path: Path) -> dict[str, tuple[str, int]]:
    out = {}
    for line in path.read_text().splitlines():
        meta, name = line.split("\t", 1)
        mode, typ, oid, size = meta.split()
        assert typ == "blob" and mode == "100644", line
        out[name] = (oid, int(size))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--plumbing", required=True)
    ap.add_argument("--out", required=True)
    ns = ap.parse_args()
    src = Path(ns.src)
    pl = Path(ns.plumbing)
    trees = {c: ls_tree(pl / f"lstree-{c}.txt") for c in COMMITS}
    log = []
    for line in (pl / "log-ac14112.txt").read_text().splitlines():
        h, t, p, an, ae, ad, cn, ce, cd, subj = line.split("|", 9)
        log.append({"commit": h, "tree": t, "parent": p, "author": f"{an} <{ae}>", "authored": ad, "committer": f"{cn} <{ce}>", "committed": cd, "subject": subj})
    problems: list[str] = []
    files: dict[str, Any] = {}
    for c in ("ac14112", "78eb9ea"):
        for name, (oid, size) in sorted(trees[c].items()):
            data = (src / c / name).read_bytes()
            ok = blob_id(data) == oid and len(data) == size
            if not ok:
                problems.append(f"{c}:{name} differs from its blob")
            files[f"{c}:{name}"] = {"blob": oid, "bytes": size, "sha256": hashlib.sha256(data).hexdigest(), "equals_blob": ok}
    # SHA256SUMS at both commits
    for c in ("ac14112", "78eb9ea"):
        for line in (src / c / "SHA256SUMS").read_text().splitlines():
            digest, name = line.split(None, 1)
            got = files.get(f"{c}:{name}", {}).get("sha256")
            if got != digest:
                problems.append(f"{c} SHA256SUMS {name}: {digest[:12]} vs {got}")
    # packing-certificates.json digests and pins
    meta = json.loads((src / "ac14112" / "packing-certificates.json").read_text())
    for cert in meta["certificates"]:
        got = files[f"ac14112:{cert['file']}"]["sha256"]
        if got != cert["sha256"]:
            problems.append(f"json sha256 for {cert['file']}")
        if cert.get("text_copy") and files[f"ac14112:{cert['text_copy']}"]["sha256"] != got:
            problems.append(f"text copy of {cert['file']} differs")
    prior = next(c for c in meta["certificates"] if c["n"] == 303)
    if files["78eb9ea:n303.cert"]["sha256"] != prior.get("prior_certificate_sha256"):
        problems.append("prior n303 digest")
    # first appearance and changes of each certificate blob across the commits
    history: dict[str, list[str]] = {}
    for c in COMMITS:
        for name, (oid, _size) in trees[c].items():
            if name.endswith(".cert"):
                seq = history.setdefault(name, [])
                if not seq or seq[-1].split(":")[1] != oid:
                    seq.append(f"{c}:{oid}")
    unchanged_bh = all(
        trees["78eb9ea"][f"n{n}.cert"][0] == trees["ac14112"][f"n{n}.cert"][0]
        for n in (553, 599, 600, 601, 602, 604, 645, 647, 648, 699, 700)
    )
    if not unchanged_bh:
        problems.append("a beyond-horizon blob changed")
    out = {
        "program": "l70_custody.py",
        "program_digests": C.file_digests(("l70_custody.py",)),
        "log": log,
        "files": files,
        "certificate_blob_history": history,
        "beyond_horizon_blobs_unchanged_78eb9ea_to_ac14112": unchanged_bh,
        "json_prior_certificate_commit": prior.get("prior_certificate_commit"),
        "problems": problems,
        "verdict": "CUSTODY_HOLDS" if not problems else "CUSTODY_PROBLEMS",
    }
    Path(ns.out).write_text(json.dumps(out, indent=1) + "\n")
    print(out["verdict"], problems)
    for k, v in history.items():
        print(k, v)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
