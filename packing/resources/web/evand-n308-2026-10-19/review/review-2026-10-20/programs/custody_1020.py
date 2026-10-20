"""Hold the two packets' retained files and pins to the source repository.

Written for the stage 4 review of 20 October 2026. It checks premises and decides no
geometry. Given a blobless clone of evand/square-packing (made outside the repository
and read as data), it checks for each packet:

- the pinned commit's tree and committer date against ``acquisition/sources.json``;
- every line of the manifest ``acquisition/upstream-subtree.sha256`` against the blob at
  the pin, by SHA-256;
- every retained file under ``source/`` byte for byte against its upstream blob, a
  ``.gz``-stored file after decompression;
- every ``pinned_only`` entry's digest and byte count, and that each ``identical_to``
  copy in another packet equals it byte for byte;
- the digests the issue prints for the certificate and the view;
- on the default branch, which commits touch each certificate path and whether the head
  still holds the pinned blob.

Usage, from ``packing/``::

    python -I custody_1020.py --clone CLONE --json OUT.json PACKET [PACKET ...]
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path

WEB = Path("resources/web")
REPO = Path("..").resolve()
#: Digests the issues print, by packet: path -> sha256.
ISSUE_DIGESTS = {
    "evand-n308-2026-10-19": {
        "search/packer/candidates/s308_d308.cert": "6a9c03318ee5a703313b5dcab02febbe6b520133ffea0a21ea2ecf0741c42a91",
        "search/packer/candidates/s308_d308_regularized.cert": "5e5af5a4833656743ae84c66dcaa6b2cd3d65d9e8308ff1323240f33520c2f03",
    },
    "evand-n154-sweep-2026-10-20": {
        "search/packer/candidates/s154_sw.cert": "c2242dcda1ae3d4c9d580af14ed9adf425780320d94846c3c96f5c3ee486d78d",
        "search/packer/candidates/s154_sw_regularized.cert": "7fb7f288a864e9d3190e7b1b01f2491e7ce97f5e2e9e7de9b1dae3768580d2bd",
    },
}


def git(clone: Path, *args: str) -> bytes:
    return subprocess.run(["git", "-C", str(clone), *args], check=True, capture_output=True).stdout


def blob(clone: Path, commit: str, path: str) -> bytes:
    return git(clone, "cat-file", "-p", f"{commit}:{path}")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check_packet(clone: Path, name: str) -> dict[str, object]:
    packet = WEB / name
    record = json.loads((packet / "acquisition/sources.json").read_text("utf-8"))["sources"][0]
    pin = record["source_commit"]
    out: dict[str, object] = {"pin": pin, "problems": []}
    problems: list[str] = out["problems"]  # type: ignore[assignment]
    tree = git(clone, "rev-parse", f"{pin}^{{tree}}").decode().strip()
    date = git(clone, "log", "-1", "--format=%cI", pin).decode().strip()
    out["tree"] = tree
    out["committed"] = date
    if tree != record["git_tree"]:
        problems.append(f"tree {tree} != recorded {record['git_tree']}")
    # The committer date is recorded in UTC.
    recorded = record["committed_utc"]
    date_utc = git(clone, "log", "-1", "--date=format-local:%Y-%m-%dT%H:%M:%SZ", "--format=%cd", pin).decode().strip()
    out["committed_utc"] = date_utc
    if date_utc != recorded:
        problems.append(f"committed {date_utc} != recorded {recorded}")
    head = git(clone, "rev-parse", "HEAD").decode().strip()
    out["head"] = head
    out["pin_is_ancestor_of_head"] = subprocess.run(["git", "-C", str(clone), "merge-base", "--is-ancestor", pin, "HEAD"]).returncode == 0
    # Manifest.
    manifest = (packet / "acquisition/upstream-subtree.sha256").read_text("utf-8").splitlines()
    checked = 0
    total_bytes = 0
    for line in manifest:
        if not line.strip():
            continue
        digest, path = line.split(None, 1)
        path = path.strip()
        if path.startswith("./"):
            path = path[2:]
        data = blob(clone, pin, path)
        total_bytes += len(data)
        if sha(data) != digest:
            problems.append(f"manifest: {path} upstream digest {sha(data)} != {digest}")
        checked += 1
    out["manifest_lines"] = checked
    out["manifest_bytes"] = total_bytes
    if checked != record["subtree_file_count"] or total_bytes != record["subtree_total_bytes"]:
        problems.append(f"manifest count/bytes {checked}/{total_bytes} != recorded {record['subtree_file_count']}/{record['subtree_total_bytes']}")
    # Retained files.
    source = packet / "source"
    retained = 0
    retained_bytes = 0
    compressed = set(record.get("compressed", []))
    for file in sorted(p for p in source.rglob("*") if p.is_file()):
        rel = file.relative_to(packet).as_posix()
        upstream_path = file.relative_to(source).as_posix()
        data = file.read_bytes()
        if rel in compressed:
            assert upstream_path.endswith(".gz")
            upstream_path = upstream_path[:-3]
            data = gzip.decompress(data)
        try:
            up = blob(clone, pin, upstream_path)
        except subprocess.CalledProcessError:
            problems.append(f"retained {rel}: no blob {upstream_path} at the pin")
            continue
        retained += 1
        retained_bytes += len(data)
        if up != data:
            problems.append(f"retained {rel} differs from upstream {upstream_path}")
    out["retained_files"] = retained
    out["retained_bytes"] = retained_bytes
    if retained != record["retained_file_count"] or retained_bytes != record["retained_total_bytes"]:
        problems.append(f"retained count/bytes {retained}/{retained_bytes} != recorded {record['retained_file_count']}/{record['retained_total_bytes']}")
    # pinned_only.
    pinned = 0
    identical = 0
    for entry in record["pinned_only"]:
        data = blob(clone, pin, entry["path"])
        pinned += 1
        if sha(data) != entry["sha256"] or len(data) != entry["bytes"]:
            problems.append(f"pinned_only {entry['path']}: digest or bytes differ")
        other = entry.get("identical_to")
        if other:
            copy = (REPO / other).read_bytes()
            identical += 1
            if copy != data:
                problems.append(f"pinned_only {entry['path']}: identical_to {other} differs")
    out["pinned_only"] = pinned
    out["identical_copies_checked"] = identical
    # Issue digests.
    for path, digest in ISSUE_DIGESTS[name].items():
        data = (source / path).read_bytes()
        if sha(data) != digest:
            problems.append(f"issue digest: {path} is {sha(data)} not {digest}")
    out["issue_digests_checked"] = len(ISSUE_DIGESTS[name])
    # Default-branch history of each certificate path.
    history: dict[str, object] = {}
    for path in ISSUE_DIGESTS[name]:
        commits = git(clone, "log", "--format=%H", "HEAD", "--", path).decode().split()
        head_blob = git(clone, "rev-parse", f"HEAD:{path}").decode().strip()
        pin_blob = git(clone, "rev-parse", f"{pin}:{path}").decode().strip()
        history[path] = {"commits_touching": commits, "head_holds_pinned_blob": head_blob == pin_blob, "blob": pin_blob}
        if commits != [pin] or head_blob != pin_blob:
            problems.append(f"history: {path} touched by {commits}, head holds pinned blob: {head_blob == pin_blob}")
    out["history"] = history
    return out


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("packets", nargs="+")
    parser.add_argument("--clone", type=Path, required=True)
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args(argv)
    report = {name: check_packet(args.clone, name) for name in args.packets}
    args.json.write_text(json.dumps(report, indent=1) + "\n", "utf-8")
    bad = 0
    for name, row in report.items():
        problems = row["problems"]
        assert isinstance(problems, list)
        bad += len(problems)
        print(
            f"{name}: pin {row['pin'][:7]} tree ok={row['tree']==json.loads((WEB/name/'acquisition/sources.json').read_text())['sources'][0]['git_tree']} "
            f"manifest {row['manifest_lines']} lines {row['manifest_bytes']} B; retained {row['retained_files']} files {row['retained_bytes']} B; "
            f"pinned_only {row['pinned_only']} ({row['identical_copies_checked']} copies); issue digests {row['issue_digests_checked']}; "
            f"ancestor of head {row['head'][:7]}: {row['pin_is_ancestor_of_head']}; problems: {len(problems)}"
        )
        for problem in problems:
            print("  PROBLEM", problem)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
