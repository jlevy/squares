#!/usr/bin/env python3
"""Replay the certificate or run explicitly partial negative controls."""
import argparse
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CERT = ROOT / "certificate/s12_lower_3.9716.txt"
EXPECTED = "833b76a179a420a40775cc76305ec9ffb7f6ea27472e587958c234c4c4712cbd"


def clean_environment():
    return {k: v for k, v in os.environ.items()
            if not k.startswith(("VERIFY_", "TIGHT_"))}


def run(label, command, env, output, timeout):
    result = subprocess.run(command, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            timeout=timeout)
    (output / f"{label}.log").write_text(result.stdout)
    print(f"{label}: exit {result.returncode}", flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rust", type=Path,
                        default=ROOT / "build/verify/release/verify")
    parser.add_argument("--cpp", type=Path, default=ROOT / "build/indep_scan")
    parser.add_argument("--threads", type=int, default=10)
    parser.add_argument("--controls", action="store_true",
                        help="Only negative controls; partial bins are NOT full verification")
    parser.add_argument("--output", type=Path, default=ROOT / "replay-output")
    args = parser.parse_args()
    assert args.threads > 0
    assert hashlib.sha256(CERT.read_bytes()).hexdigest() == EXPECTED
    args.output.mkdir(parents=True, exist_ok=True)
    rust, cpp = str(args.rust.resolve()), str(args.cpp.resolve())
    if not args.controls:
        for label, command in [
            ("rust", [rust, str(CERT), "12", "96000", str(args.threads), "0"]),
            ("cpp", [cpp, str(CERT), "96000", "1000000000000000", "12"]),
        ]:
            env = clean_environment()
            if label == "rust":
                env["VERIFY_STATS"] = "1"
            result = run(label, command, env, args.output, timeout=None)
            assert result.returncode == 0, f"{label} did not accept"
            assert "VERIFIED:" in result.stdout and "NOT VERIFIED" not in result.stdout
        print("Both complete sweeps accepted.")
        return

    tokens = list(map(int, CERT.read_text().split()))
    assert len(tokens) == 5 + 3 * tokens[4]
    doubled = tokens.copy()
    doubled[3] *= 2
    report = {"scope": "negative controls only; bin 39531 for weight control",
              "certificateSha256": EXPECTED, "results": []}
    with tempfile.TemporaryDirectory() as temporary:
        for name, values in [("double-denominator", doubled),
                             ("truncated", tokens[:-3])]:
            mutant = Path(temporary) / f"{name}.txt"
            mutant.write_text(" ".join(map(str, values)) + "\n")
            for checker in ("rust", "cpp"):
                env = clean_environment()
                if checker == "rust":
                    env.update(VERIFY_FULLSWEEP="1", VERIFY_BINS="39531:39531")
                    command = [rust, str(mutant), "12", "96000", "1", "0"]
                else:
                    command = [cpp, str(mutant), "96000", "1000000000000000",
                               "12", "-1", "39532", "39531"]
                label = f"{name}-{checker}"
                result = run(label, command, env, args.output, timeout=60)
                item = {"control": name, "checker": checker,
                        "exitCode": result.returncode}
                if name == "truncated":
                    assert result.returncode == 2 and "ERROR:" in result.stdout
                else:
                    expected_exit = 4 if checker == "rust" else 1
                    assert result.returncode == expected_exit
                    match = re.search(r"min (?:covered|captured) weight[^=]*=\s*(\d+)/(\d+)", result.stdout)
                    assert match, "Missing exact minimum"
                    minimum = Fraction(int(match[1]), int(match[2]))
                    assert minimum == Fraction(1, 2)
                    assert "NOT VERIFIED" in result.stdout
                    item["minimumExact"] = str(minimum)
                    item["partial"] = True
                report["results"].append(item)
    (args.output / "controls.json").write_text(json.dumps(report, indent=2) + "\n")
    print("All four negative-control runs behaved as expected.")


if __name__ == "__main__":
    main()
