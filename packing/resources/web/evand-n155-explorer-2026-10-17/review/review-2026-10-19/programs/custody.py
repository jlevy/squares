"""Hold each packet's pinned scope to evand/square-packing at its pin (19 October review).

Written for the stage 4 review of Evan Daniel's 155, 229 (two), 236 and 271. For each
packet named on the command line it reads the packet's acquisition record
(``acquisition/sources.json``) and manifest (``acquisition/upstream-subtree.sha256``) as
data and, from one blobless clone of the source repository made over HTTPS:

- the pinned commit must exist and be an ancestor of the source's default branch, and
  its tree must be the ``git_tree`` the record states, its committer date the record's
  ``committed_utc``;
- every manifest line's file, read as the Git blob at ``PIN:path``, must have the
  manifest's SHA-256, and every ``pinned_only`` entry its SHA-256 and byte count (and,
  where it names an identical copy in another packet, that copy's bytes);
- every file the packet retains under ``source/`` must be byte for byte the blob at the
  pin, a stored ``.gz`` after decompression;
- the certificate the claim rests on must have the SHA-256 the issue prints
  (``ISSUE_DIGESTS``, copied by hand from the issues as fetched on 19 October); every
  commit of the default branch that touches its path is reported, with its date, and
  whether the default branch's head still holds the pinned blob there.

It writes every manifest file under ``OUT/PACKET/tree/`` for the other programs of this
review, runs no program of the source and writes nothing in the repository. Usage, from
``packing/`` with the project interpreter, network allowed for github.com::

    python -I custody.py OUT PACKET...
"""

from __future__ import annotations

import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path

WEB = Path.cwd() / "resources/web"
REPO = Path.cwd().parent

#: The SHA-256 each issue prints for the certificate its claim rests on, by packet.
ISSUE_DIGESTS = {
    "evand-n155-explorer-2026-10-17": {
        "search/packer/candidates/s155_ex2.cert": "a1a3b6e7c2ce4d7de79efc2e07fc0bf53616dc44b732a2849b4dc4d8f7e2c4cc",
        "search/packer/candidates/s155_ex2_regularized.cert": "ab3c0b93aa205a907da5387cc119df11164c0a6d63b49b81332d7ce77910a897",
    },
    "evand-n229-dilation-2026-10-17": {
        "search/packer/candidates/s229.cert": "0366e8178e37d7c5b4baf002d35f4c1088b4e20ab8f90283d418f634c8af204d",
        "search/packer/candidates/s229.input.txt": "7df8cd6fe3252fb8b015fea731229ef065130498014f1660aa0ccf435ee990fe",
    },
    "evand-n229-dilation-update-2026-10-18": {
        "search/packer/candidates/s229_v2.cert": "1a35a7806b6cc01b232d5c634efdbe789c7df979cec6ab28d6ab283ac2b47e23",
        "search/packer/candidates/s229_v2.input.txt": "7b2bf80771e8d96f11931e5080f18c0d623b3d4373b9693e4d338acbf4ffcf53",
    },
    "evand-n236-2026-10-16": {
        "search/packer/candidates/s236_bm3c.cert": "21dbf6792bec64b06ab5fc1d6ac56a17432f971431100fdbe63e92d23bc091c9",
        "search/packer/candidates/s236_bm3c_regularized.cert": "abae0c5240f986373a4c49f860004ba3b187495579b4f88d41bfec0d9015a546",
    },
    "evand-n271-2026-10-17": {
        "search/packer/candidates/s271_ex1.cert": "48abf7ca68909c42e0aaa5215d4d578f4cdba29d6188775012ae24636e02d680",
        "search/packer/candidates/s271_ex1_regularized.cert": "4d4d4e25604b2c492047b44144249e3d69be53db061ab51e26dab39e8fb12160",
    },
}


def git(clone: Path, *args: str, binary: bool = False) -> bytes | str:
    done = subprocess.run(
        ["git", "-C", str(clone), *args], capture_output=True, check=True, timeout=900
    )
    return done.stdout if binary else done.stdout.decode().strip()


def clone_of(out: Path, url: str) -> Path:
    """One blobless clone per source repository, shared by the packets that pin it."""
    name = url.rstrip("/").removesuffix(".git").split("github.com/")[1].replace("/", "__")
    clone = out / "clones" / name
    if not clone.exists():
        clone.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", "-q", "--filter=blob:none", "--no-checkout", f"{url}.git", str(clone)],
            check=True,
            timeout=1800,
        )
    return clone


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check(out: Path, packet_name: str) -> dict[str, object]:
    packet = WEB / packet_name
    record = json.loads((packet / "acquisition/sources.json").read_text(encoding="utf-8"))
    (source,) = record["sources"]
    pin = source["source_commit"]
    clone = clone_of(out, source["source_url"])
    problems: list[str] = []
    head = str(git(clone, "rev-parse", "origin/HEAD"))
    ancestor = (
        subprocess.run(
            ["git", "-C", str(clone), "merge-base", "--is-ancestor", pin, head],
            capture_output=True,
            check=False,
        ).returncode
        == 0
    )
    if not ancestor:
        problems.append(f"pin {pin} is not an ancestor of the default branch {head}")
    tree = git(clone, "rev-parse", f"{pin}^{{tree}}")
    if tree != source["git_tree"]:
        problems.append(f"tree {tree} is not the recorded {source['git_tree']}")
    committed = str(git(clone, "show", "-s", "--format=%cI", pin))
    authored = str(git(clone, "show", "-s", "--format=%aI", pin))
    manifest = [
        line.split(None, 1)
        for line in (packet / "acquisition/upstream-subtree.sha256")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    target = out / packet_name / "tree"
    paths = [raw.strip().removeprefix("./") for _digest, raw in manifest]
    git(clone, "sparse-checkout", "set", "--no-cone", *[f"/{path}" for path in paths])
    git(clone, "checkout", "-q", "--detach", pin)
    lines = 0
    for digest, raw_path in manifest:
        path = raw_path.strip().removeprefix("./")
        blob = git(clone, "cat-file", "blob", f"{pin}:{path}", binary=True)
        assert isinstance(blob, bytes)
        if sha(blob) != digest:
            problems.append(f"{path}: SHA-256 differs from the manifest")
        where = target / path
        where.parent.mkdir(parents=True, exist_ok=True)
        where.write_bytes(blob)
        lines += 1
    if lines != source["subtree_file_count"]:
        problems.append(f"{lines} manifest lines, record says {source['subtree_file_count']}")
    total = sum((target / p).stat().st_size for p in paths)
    if total != source["subtree_total_bytes"]:
        problems.append(f"{total} manifest bytes, record says {source['subtree_total_bytes']}")
    pinned = 0
    for item in source["pinned_only"]:
        upstream = target / item["path"]
        if not upstream.is_file():
            problems.append(f"pinned_only {item['path']}: not in the manifest")
            continue
        blob = upstream.read_bytes()
        if sha(blob) != item["sha256"]:
            problems.append(f"pinned_only {item['path']}: SHA-256 differs")
        if "bytes" in item and len(blob) != item["bytes"]:
            problems.append(f"pinned_only {item['path']}: size differs")
        if "identical_to" in item and (REPO / item["identical_to"]).read_bytes() != blob:
            problems.append(f"pinned_only {item['path']}: differs from {item['identical_to']}")
        pinned += 1
    retained = 0
    retained_bytes = 0
    archived = REPO / source["archived_path"]
    for kept in sorted(p for p in archived.rglob("*") if p.is_file()):
        path = kept.relative_to(archived).as_posix()
        data = kept.read_bytes()
        if path.endswith(".gz"):
            path = path.removesuffix(".gz")
            data = gzip.decompress(data)
        upstream = target / path
        if not upstream.is_file():
            problems.append(f"retained {path}: no manifest file at the pin")
            continue
        if upstream.read_bytes() != data:
            problems.append(f"retained {path}: bytes differ from the pin")
        retained += 1
        retained_bytes += len(data)
    if retained != source["retained_file_count"]:
        problems.append(f"{retained} retained files, record says {source['retained_file_count']}")
    issue_digests: dict[str, object] = {}
    for path, printed in ISSUE_DIGESTS[packet_name].items():
        blob = (target / path).read_bytes()
        first = str(git(clone, "log", "--format=%H %cI", "--reverse", head, "--", path)).splitlines()
        at_head = str(git(clone, "rev-parse", f"{head}:{path}"))
        at_pin = str(git(clone, "rev-parse", f"{pin}:{path}"))
        issue_digests[path] = {
            "printed": printed,
            "equal": sha(blob) == printed,
            "commits_touching_path": first,
            "same_blob_at_default_branch_head": at_head == at_pin,
        }
        if sha(blob) != printed:
            problems.append(f"{path}: SHA-256 is not the one the issue prints")
    return {
        "packet": packet_name,
        "source": source["source_url"],
        "pin": pin,
        "pin_is_ancestor_of_default_branch": ancestor,
        "default_branch_head": head,
        "tree": tree,
        "committed": committed,
        "authored": authored,
        "recorded_committed_utc": source["committed_utc"],
        "manifest_lines": lines,
        "manifest_bytes": total,
        "pinned_only": pinned,
        "retained": retained,
        "retained_bytes_decompressed": retained_bytes,
        "issue_digests": issue_digests,
        "problems": problems,
    }


def main(argv: list[str]) -> int:
    out = Path(argv[0])
    results = [check(out, name) for name in argv[1:]]
    for result in results:
        print(json.dumps(result))
    (out / "custody.json").write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")
    return 1 if any(result["problems"] for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
