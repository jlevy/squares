#!/usr/bin/env python3
"""Negative-control harness: prove a check fails when it should.

A check nobody has watched fail is not a check. Every guard in this directory was
negative-controlled by hand at least once -- corrupt a field, run the gate, confirm it
complains, put the field back -- and every one of those controls was then thrown away,
so the next person has only a claim that it was done.

This runs them from a file instead, so they are checked in, repeatable, and part of the
suite. It also removes the way the hand version goes wrong: restoring with
`git checkout` reverts to HEAD, which silently discards uncommitted work in the same
file. This restores the exact bytes it saved.

Control file format (YAML):

    controls:
    - name: outstanding defect without a bead
      file: defects.yaml
      replace: ["  bead: think-lksm\\n", ""]     # literal, must appear exactly once
      run: python3 tools/validate_schemas.py
      expect: "outstanding without a bead"

Usage:
    python3 tools/negctl.py tools/controls.yaml          # run them all
    python3 tools/negctl.py tools/controls.yaml -k bead  # only matching names
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def run_one(c: dict) -> tuple[bool, str]:
    """Apply the mutation, run the command, restore. Returns (passed, detail)."""
    target = ROOT / c["file"]
    original = target.read_bytes()
    old, new = c["replace"]
    try:
        text = original.decode("utf-8")
        if text.count(old) != 1:
            return False, f"anchor appears {text.count(old)} times, expected exactly 1"
        target.write_text(text.replace(old, new, 1), encoding="utf-8")
        # check=False deliberately: a non-zero exit is the EXPECTED outcome here, and
        # inspecting it is this function's whole job.
        proc = subprocess.run(
            c["run"], shell=True, cwd=ROOT, capture_output=True, text=True, check=False
        )
        output = proc.stdout + proc.stderr
        if proc.returncode == 0:
            return False, "command SUCCEEDED; the check did not fire"
        if c["expect"] not in output:
            return False, f"failed, but not with the expected message: {output.strip()[:120]}"
        return True, ""
    finally:
        # Always, on every path: the bytes we saved, not whatever git thinks they were.
        target.write_bytes(original)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    spec = yaml.safe_load((ROOT / sys.argv[1]).read_text(encoding="utf-8"))
    only = sys.argv[sys.argv.index("-k") + 1] if "-k" in sys.argv else None
    controls = [c for c in spec["controls"] if not only or only in c["name"]]

    failures = 0
    for c in controls:
        passed, detail = run_one(c)
        if not passed:
            failures += 1
            print(f"  CONTROL FAILED  {c['name']}: {detail}", file=sys.stderr)
    if failures:
        print(f"{failures} of {len(controls)} negative controls did not fire", file=sys.stderr)
        return 1
    print(f"  {len(controls)} negative controls fire as expected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
