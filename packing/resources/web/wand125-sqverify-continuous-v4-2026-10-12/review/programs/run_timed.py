"""Run one command and write a JSON receipt of what ran and what it cost.

The receipt records the command line, the working directory, the exit status, the
wall seconds and the child process's CPU seconds (user and system, from
``resource.getrusage(RUSAGE_CHILDREN)``), the SHA-256 of every file named with
``--digest``, and the first and last lines of standard output and standard error.
Standard output and standard error are also saved whole beside the receipt when
``--keep`` names a directory.

It decides nothing: it is the clock and the custody record for the review's runs of
the verifier (its build, its tests and its smoke and control runs).

Usage::

    python -I run_timed.py RECEIPT.json [--cwd DIR] [--keep DIR] [--digest PATH]... \
        -- COMMAND [ARG]...
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import resource
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--cwd", type=Path, default=None)
    parser.add_argument("--keep", type=Path, default=None)
    parser.add_argument("--digest", type=Path, action="append", default=[])
    argv = sys.argv[1:]
    if "--" not in argv:
        parser.error("give the command after --")
    split = argv.index("--")
    args = parser.parse_args(argv[:split])
    command = argv[split + 1 :]
    if not command:
        parser.error("no command given")
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    started = datetime.now(UTC)
    clock = time.monotonic()
    done = subprocess.run(command, cwd=args.cwd, capture_output=True, check=False)
    wall = time.monotonic() - clock
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    out = done.stdout.decode("utf-8", "replace").splitlines()
    err = done.stderr.decode("utf-8", "replace").splitlines()
    if args.keep is not None:
        args.keep.mkdir(parents=True, exist_ok=True)
        stem = args.receipt.stem
        (args.keep / f"{stem}.stdout").write_bytes(done.stdout)
        (args.keep / f"{stem}.stderr").write_bytes(done.stderr)
    receipt = {
        "command": command,
        "cwd": str(args.cwd) if args.cwd is not None else os.getcwd(),
        "started_utc": started.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "exit_status": done.returncode,
        "wall_seconds": round(wall, 3),
        "cpu_user_seconds": round(after.ru_utime - before.ru_utime, 3),
        "cpu_system_seconds": round(after.ru_stime - before.ru_stime, 3),
        "max_rss_kib": after.ru_maxrss,
        "load_average": list(os.getloadavg()),
        "digests": {str(p): sha256(p) for p in args.digest if p.is_file()},
        "stdout_lines": len(out),
        "stdout_head": out[:3],
        "stdout_tail": out[-3:],
        "stderr_lines": len(err),
        "stderr_tail": err[-5:],
    }
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({k: receipt[k] for k in ("exit_status", "wall_seconds", "cpu_user_seconds")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
