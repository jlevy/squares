#!/usr/bin/env python3
"""Replay all included proof-code controls. No global n=11 enumeration is run."""
from pathlib import Path
import json
import subprocess
import sys

BASE = Path(__file__).resolve().parent


def run(folder, script, optimized=False):
    command = [sys.executable] + (["-O"] if optimized else []) + [script]
    result = subprocess.run(command, cwd=BASE / folder, text=True,
                            capture_output=True, check=True, timeout=120)
    return result.stdout, json.loads(result.stdout)


def main():
    try:
        support, sd = run("original_review/certificate", "check_support_ceiling.py")
        optimized, _ = run("original_review/certificate", "check_support_ceiling.py", True)
        if support != optimized:
            raise ValueError("fixed-support normal/optimized disagreement")
        old = json.loads((BASE/"original_review/certificate/support_exact_result.json").read_text())
        if sd != old:
            raise ValueError("fixed-support result differs from retained result")
        _, st = run("original_review/certificate", "test_support_ceiling.py")
        elementary, ed = run("enumeration", "enumeration_checks.py")
        optimized, _ = run("enumeration", "enumeration_checks.py", True)
        if elementary != optimized:
            raise ValueError("elementary normal/optimized disagreement")
        retained = json.loads((BASE/"enumeration/elementary_results.json").read_text())
        if ed != retained:
            raise ValueError("elementary result differs from retained result")
        _, et = run("enumeration", "test_enumeration.py")
        if st['status'] != 'PASS' or et['status'] != 'PASS':
            raise ValueError("a control suite did not pass")
        print(json.dumps({"status": "PASS", "fixed_support_upper_bound": sd['upper_bound'],
            "ordered_angle_profiles": ed['ordered_profiles'],
            "checks": ["fixed-support receipt reproduced", "both mutation suites pass",
                       "normal and optimized Python agree", "new elementary receipt reproduced"],
            "scope": "Same-code certificate/control replay; no historical 3.81 replay, full radius replay, or global enumeration",
            "new_global_bound": None}, indent=2))
    except (subprocess.SubprocessError, ValueError, OSError, KeyError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
