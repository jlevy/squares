"""Hold each packet's pinned scope to the source repository at its pin (review lane C).

Written for the 16 October review of T-185 to T-190. For each packet named on the command
line it reads the packet's acquisition record (``acquisition/sources.json``) and manifest
(``acquisition/upstream-subtree.sha256``) as data, and, from a blobless clone of the
source repository made over HTTPS (codeload tarballs are refused by this host's proxy):

- the pinned commit's tree must be the ``git_tree`` the record states;
- every manifest line's file, read as the Git blob at ``PIN:path``, must have the
  manifest's SHA-256, and every ``pinned_only`` entry its SHA-256 and byte count;
- every file the packet retains under its ``source/`` directory must be byte for byte the
  blob at the pin;
- every manifest path is written under ``OUT/PACKET/tree/`` so that the third route's
  ``--upstream PACKET DIR`` can read the source's files at the pin.

It runs no program of the source and writes nothing in the repository. Usage, from
``packing/`` with the project interpreter::

    python -I custody.py OUT PACKET...
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

WEB = Path.cwd() / "resources/web"
REPO = Path.cwd().parent


def git(clone: Path, *args: str, binary: bool = False) -> bytes | str:
    done = subprocess.run(
        ["git", "-C", str(clone), *args], capture_output=True, check=True, timeout=600
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
            timeout=1200,
        )
    return clone


def check(out: Path, packet_name: str) -> dict[str, object]:
    packet = WEB / packet_name
    record = json.loads((packet / "acquisition/sources.json").read_text(encoding="utf-8"))
    source = record["sources"][0]
    pin = source["source_commit"]
    clone = clone_of(out, source["source_url"])
    problems: list[str] = []
    tree = git(clone, "rev-parse", f"{pin}^{{tree}}")
    if tree != source["git_tree"]:
        problems.append(f"tree {tree} is not the recorded {source['git_tree']}")
    manifest = [
        line.split(None, 1)
        for line in (packet / "acquisition/upstream-subtree.sha256")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip()
    ]
    target = out / packet_name / "tree"
    # A sparse checkout of exactly the manifest's paths fetches their blobs in one batch;
    # the bytes compared are still each Git blob as `cat-file` prints it, no filter applied.
    paths = [raw.strip().removeprefix("./") for _digest, raw in manifest]
    git(clone, "sparse-checkout", "set", "--no-cone", *[f"/{path}" for path in paths])
    git(clone, "checkout", "-q", "--detach", pin)
    lines = 0
    for digest, raw_path in manifest:
        path = raw_path.strip().removeprefix("./")
        blob = git(clone, "cat-file", "blob", f"{pin}:{path}", binary=True)
        assert isinstance(blob, bytes)
        if hashlib.sha256(blob).hexdigest() != digest:
            problems.append(f"{path}: SHA-256 differs from the manifest")
        where = target / path
        where.parent.mkdir(parents=True, exist_ok=True)
        where.write_bytes(blob)
        lines += 1
    pinned = 0
    for item in source["pinned_only"]:
        blob = (target / item["path"]).read_bytes() if (target / item["path"]).is_file() else None
        if blob is None:
            problems.append(f"pinned_only {item['path']}: not in the manifest")
            continue
        if hashlib.sha256(blob).hexdigest() != item["sha256"]:
            problems.append(f"pinned_only {item['path']}: SHA-256 differs")
        if "bytes" in item and len(blob) != item["bytes"]:
            problems.append(f"pinned_only {item['path']}: size differs")
        pinned += 1
    retained = 0
    archived = REPO / source["archived_path"]
    for kept in sorted(p for p in archived.rglob("*") if p.is_file()):
        path = kept.relative_to(archived).as_posix()
        upstream = target / path
        if not upstream.is_file():
            problems.append(f"retained {path}: no manifest file at the pin")
            continue
        if upstream.read_bytes() != kept.read_bytes():
            problems.append(f"retained {path}: bytes differ from the pin")
        retained += 1
    return {
        "packet": packet_name,
        "source": source["source_url"],
        "pin": pin,
        "tree": tree,
        "manifest_lines": lines,
        "pinned_only": pinned,
        "retained": retained,
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
