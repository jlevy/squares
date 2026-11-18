"""Custody of the six certificate files in the source's history (lane r127b-1118).

Usage:

    python -I -B rb127_custody.py CLONE APIDIR ISSUE1015.json ISSUE1017.json ISSUE1020.json OUT.json

``CLONE`` is a clone of JoostdeWinter/square-packing; ``APIDIR`` holds the same files as
fetched at each pin through GitHub's contents API, as ``APIDIR/NNNN/n127_exact.json``
and ``APIDIR/NNNN/n127_witness.yaml``. Decides nothing about a packing. For each pin it
records the files' blob ids and SHA-256 by the two routes, the source's own
``n127/SHA256SUMS`` at the pin and at the next commit, every commit from the first that
holds ``n127/`` to the clone's head that changes either file, and whether the issue's
statement that later commits leave the files unchanged holds now and held when the
issue was opened. Runs ``git`` read-only on the clone.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

FILES = ("n127_exact.json", "n127_witness.yaml")


def git(clone: str, *args: str) -> str:
    return subprocess.run(["git", "-C", clone, *args], check=True, capture_output=True, text=True).stdout


def git_bytes(clone: str, *args: str) -> bytes:
    return subprocess.run(["git", "-C", clone, *args], check=True, capture_output=True).stdout


def main(argv: list[str]) -> int:
    if len(argv) != 7:
        print(__doc__)
        return 2
    clone, apidir = argv[1], Path(argv[2])
    issues = {}
    for p in argv[3:6]:
        d = json.loads(Path(p).read_text(encoding="utf-8"))
        issues[str(d["number"])] = d
    import re

    pins = {k: re.search(r"at commit ([0-9a-f]{40})", d["body"]).group(1) for k, d in issues.items()}
    head = git(clone, "rev-parse", "HEAD").strip()
    chain = git(clone, "rev-list", "--reverse", "--topo-order", "HEAD", "--", "n127/").split()
    log = {}
    for c in git(clone, "rev-list", "--reverse", "HEAD").split():
        info = git(clone, "show", "-s", "--format=%H%x00%cI%x00%P%x00%s", c).strip().split("\x00")
        log[c] = {"committed": info[1], "parents": info[2].split(), "subject": info[3]}
    out = {"program": "rb127_custody.py", "clone_head": head, "linear_history": all(len(v["parents"]) <= 1 for v in log.values()),
           "pins": {}, "file_history": {}}
    order = list(log)
    for label, pin in pins.items():
        rec = {"pin": pin, "is_commit": git(clone, "cat-file", "-t", pin).strip() == "commit",
               "committed": log[pin]["committed"], "subject": log[pin]["subject"],
               "issue_created": issues[label]["created_at"], "files": {}}
        nxt = order[order.index(pin) + 1] if order.index(pin) + 1 < len(order) else None
        sums_pin = git(clone, "show", f"{pin}:n127/SHA256SUMS")
        sums_next = git(clone, "show", f"{nxt}:n127/SHA256SUMS") if nxt else ""
        for f in FILES:
            blob = git(clone, "rev-parse", f"{pin}:n127/{f}").strip()
            data = git_bytes(clone, "show", f"{pin}:n127/{f}")
            sha_git = hashlib.sha256(data).hexdigest()
            api = (apidir / label / f).read_bytes()
            sha_api = hashlib.sha256(api).hexdigest()
            listed_pin = [ln.split()[0] for ln in sums_pin.splitlines() if ln.endswith(f"  {f}")]
            listed_next = [ln.split()[0] for ln in sums_next.splitlines() if ln.endswith(f"  {f}")]
            later = []
            for c in order[order.index(pin) + 1:]:
                try:
                    b = git(clone, "rev-parse", f"{c}:n127/{f}").strip()
                except subprocess.CalledProcessError:
                    b = None
                if b != blob:
                    later.append({"commit": c, "committed": log[c]["committed"], "blob": b})
                    break
            rec["files"][f] = {
                "blob": blob, "bytes": len(data), "sha256_git": sha_git, "sha256_contents_api": sha_api,
                "routes_agree": sha_git == sha_api,
                "sha256sums_at_pin_lists": listed_pin, "sha256sums_at_pin_matches": listed_pin == [sha_git],
                "next_commit": nxt, "sha256sums_at_next_commit_matches": listed_next == [sha_git],
                "first_later_change": later[0] if later else None,
            }
        stated = "Later commits leave these files unchanged" in issues[label]["body"]
        changes = [v["first_later_change"] for v in rec["files"].values() if v["first_later_change"]]
        created = datetime.fromisoformat(issues[label]["created_at"].replace("Z", "+00:00"))
        rec["later_commits_unchanged_stated"] = stated
        rec["later_commits_unchanged_now"] = not changes
        rec["later_commits_unchanged_when_opened"] = all(
            datetime.fromisoformat(ch["committed"]) > created for ch in changes
        ) if changes else True
        out["pins"][label] = rec
    for f in FILES:
        hist = []
        prev = None
        for c in chain:
            try:
                b = git(clone, "rev-parse", f"{c}:n127/{f}").strip()
            except subprocess.CalledProcessError:
                b = None
            if b != prev:
                hist.append({"commit": c, "committed": log[c]["committed"], "blob": b, "subject": log[c]["subject"]})
                prev = b
        out["file_history"][f] = hist
    ordered = [pins[k] for k in sorted(pins)]
    out["pins_in_order_of_history"] = [order.index(p) for p in ordered] == sorted(order.index(p) for p in ordered)
    Path(argv[6]).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    for label, rec in out["pins"].items():
        print(label, rec["pin"][:9], {f: (v["routes_agree"], v["sha256sums_at_pin_matches"]) for f, v in rec["files"].items()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
