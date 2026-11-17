"""Run the L77 self-test against mutated copies of the checker; every mutant must fail.

Each mutant is one deliberate error, chiefly in how an exact contact (gap 0) is classed.
A mutant fails when the self-test reports FAILED or stops with an error.

Run: python -I -B l77_mutants.py WORKDIR OUT.json
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MUTANTS = {
    "A-contact-as-overlap": ('return "overlap" if m < 0 else', 'return "overlap" if m <= 0 else'),
    "B-open-halfplanes": (
        "        if le >= 0:\n            if ls < 0:",
        "        if le > 0:\n            if ls <= 0:",
    ),
    "B-contact-as-overlap": (
        'return ("overlap" if area > 0 else "contact"), area',
        'return ("overlap" if area >= 0 else "contact"), area',
    ),
    "A-clockwise-not-accepted": (
        "        elif (fx, fy) == (uy, -ux):",
        "        elif (fx, fy) == (-uy, ux):",
    ),
    "A-only-own-axes": (
        "for k, (ax, ay) in enumerate(a.axes + b.axes):",
        "for k, (ax, ay) in enumerate(a.axes):",
    ),
    "B-no-area-check": ("        if a2 * sign != 2:", "        if False:"),
    "reader-accepts-non-lowest": ("    if gcd(abs(p), q) != 1:", "    if False:"),
}


def main() -> int:
    work, out = sys.argv[1], sys.argv[2]
    src = open(os.path.join(HERE, "l77_checker.py")).read()
    report = {}
    for name, (old, new) in MUTANTS.items():
        d = os.path.join(work, name)
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
        assert src.count(old) == 1, name
        with open(os.path.join(d, "l77_checker.py"), "w") as fh:
            fh.write(src.replace(old, new))
        shutil.copy(os.path.join(HERE, "l77_selftest.py"), d)
        rec = os.path.join(d, "selftest.json")
        p = subprocess.run(
            [sys.executable, "-I", "-B", os.path.join(d, "l77_selftest.py"), rec],
            capture_output=True,
            text=True,
        )
        if os.path.exists(rec):
            res = json.load(open(rec))
            report[name] = {
                "selftest": res["verdict"],
                "failed_cases": len(res["failed"]),
                "first_failed": [f["case"] for f in res["failed"][:3]],
            }
        else:
            report[name] = {"selftest": "STOPPED", "error": p.stderr.strip().splitlines()[-1][:200]}
    caught = all(r["selftest"] != "PASSED" for r in report.values())
    receipt = {
        "program": "l77_mutants.py",
        "program_sha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
        "checker_sha256": hashlib.sha256(src.encode()).hexdigest(),
        "verdict": "EVERY_MUTANT_CAUGHT" if caught else "A_MUTANT_PASSED",
        "mutants": report,
    }
    with open(out, "w") as fh:
        json.dump(receipt, fh, indent=1)
        fh.write("\n")
    print(receipt["verdict"], json.dumps({k: v["selftest"] for k, v in report.items()}))
    return 0 if caught else 1


if __name__ == "__main__":
    sys.exit(main())
