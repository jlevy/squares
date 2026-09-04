#!/usr/bin/env python3
"""The whole check in one command, with whatever python3 is on PATH.

    python3 check.py

Any CPython 3.8 or later, nothing installed, no project environment. Exits
non-zero if the control data does not match its published constants, either
positive certificate is refused, or the negative control is accepted. Expect
about half a minute on an idle core, and up to a minute on a contended one.

Four steps, and the second one is not the interesting one. Step 1 rebuilds the
n = 17 control from the constants printed in Massaccesi's own source and checks
it against the copy shipped here, so the control is not merely asserted. Step 2
decides the claim. Step 3 decides Massaccesi's published bound with the same
verifier, unchanged -- if that fails, the verifier is wrong and step 2 means
nothing, which is the point of running it. Step 4 makes one weight negative and
requires a labelled refusal at the theorem preconditions.
"""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = (
    (
        "rebuild and compare the control data",
        ["build_n17_control.py", "--check", "control-n17-massaccesi.json"],
    ),
    ("decide the claim: s(11) >= 19/5", ["verify.py", "certificate.json"]),
    (
        "decide Massaccesi's published s(17) >= 4.5058 with the same verifier",
        ["control-n17-massaccesi.json"],
    ),
    (
        "require a labelled refusal for a negative weight",
        ["falsify.py", "--quick", "certificate.json"],
    ),
)


def main() -> int:
    for label, argv in STEPS:
        script = argv[0] if argv[0].endswith(".py") else "verify.py"
        rest = argv[1:] if argv[0].endswith(".py") else argv
        print(f"\n=== {label} ===", flush=True)
        completed = subprocess.run([sys.executable, str(HERE / script), *rest], cwd=HERE, check=False)
        if completed.returncode != 0:
            print(f"check.py: FAILED at: {label}", file=sys.stderr)
            return completed.returncode
    print("\ncheck.py: all four steps passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
