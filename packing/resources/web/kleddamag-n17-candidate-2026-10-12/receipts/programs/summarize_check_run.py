"""Summarize one check.py run into the packet's receipt, from its own outputs.

    python -I summarize_check_run.py K1_DIR CHECK_OUT_DIR PACKET_RECEIPT_DIR

Copies check.py's stdout and the run's environment and timing lines, keeps the three
small outputs check.py writes (equivalence.out, comparison_records.out and the
independent endpoint program's last lines), and summarizes each of the 31 runner receipts
(status, wall and CPU seconds, how many files it read, the SHA-256 of its receipt and
stdout). Nothing of the edition is copied.
"""

import hashlib
import json
import re
import shutil
import sys
from pathlib import Path


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    k1, run, dest = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    dest.mkdir(parents=True, exist_ok=True)
    src = k1 / "check-run"
    shutil.copyfile(src / "stdout.txt", dest / "stdout.txt")
    for name in ("equivalence.out", "comparison_records.out"):
        shutil.copyfile(run / name, dest / name)
    env = dict(
        line.split("=", 1) for line in (src / "env.txt").read_text().splitlines() if "=" in line
    )
    timing = dict(
        kv.split("=") for kv in (src / "time.txt").read_text().split() if "=" in kv
    )
    stdout = (src / "stdout.txt").read_text()
    last = stdout.rstrip("\n").split("\n")[-1]
    lines = [l for l in stdout.splitlines() if re.match(r"^L\d ", l)]
    status = {}
    for l in lines:
        level, word, name = l.split()[:3]
        status.setdefault(word, 0)
        status[word] += 1
    checks = []
    for receipt in sorted((run / "level2/public_runs").glob("*/receipt.json")):
        r = json.loads(receipt.read_text())
        checks.append(
            {
                "id": r["id"],
                "status": r["status"],
                "error": r["error"],
                "wall_seconds": round(r["wall_seconds"], 2),
                "cpu_seconds": round(r["cpu_seconds"], 2),
                "inputs_read": len(r["inputs_read"]),
                "script_sha256": r["script_sha256"],
                "python": r["python"].split()[0],
                "receipt_sha256": sha(receipt),
                "stdout_sha256": sha(receipt.parent / "stdout.txt"),
            }
        )
    ind = (run / "independent_endpoint.out").read_text().splitlines()
    ctl = (run / "independent_endpoint_control.out").read_text().splitlines()
    summary = {
        "schema": "k17-check-py-run/v1",
        "edition_commit": "653b9589d0f8a152f01adc56b1d48ba53d49abc3",
        "command": "env -i PATH=/opt/node22/bin:/usr/bin:/bin HOME=$HOME LANG=C.UTF-8 VENV/bin/python -I EDITION/check.py, run from a scratch directory outside the edition and this repository",
        "check_py_sha256": "c17240b5189821c9244b1e5568e7d6b73c3c4de0fae741ec4206f9852d86a7cb",
        "environment": env,
        "exit_code": int((src / "rc.txt").read_text().strip()),
        "wall_seconds": float(timing["real_s"]),
        "cpu_seconds_user_sys_with_children": round(float(timing["user_s"]) + float(timing["sys_s"]), 1),
        "last_line": last,
        "manifest_sha256_matches_release_notes": last.endswith(
            "9ecfa0db00fc9afaf98c6df8eeee920df8cb1e4737c88521ac3c64366ec7689e"
        ),
        "line_status_counts": status,
        "public_checks": checks,
        "independent_endpoint_last_line": [l for l in ind if l.strip()][-1],
        "independent_endpoint_control_last_line": [l for l in ctl if l.strip()][-1],
        "outputs_kept": ["stdout.txt", "equivalence.out", "comparison_records.out"],
        "outputs_not_kept": "the runner's per-check stdout and outputs folders and the independent endpoint program's full output, under _check_out/ in the scratch clone; their SHA-256 are above",
    }
    (dest / "run.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: summary[k] for k in ("exit_code", "wall_seconds", "cpu_seconds_user_sys_with_children", "last_line", "line_status_counts")}, indent=1))
    print(len(checks), "runner receipts;", sum(c["status"] == "PASS" for c in checks), "PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
