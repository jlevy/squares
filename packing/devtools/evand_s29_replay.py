"""Replay Evan Daniel's five-step check of the s(29) minimal polynomial, with controls.

T-246 records Daniel's report that the side of the best known packing of 29 squares is a
root of an irreducible integer polynomial p of degree 7213.  His release
``exact-data-2026-10-12`` publishes p, the shape-lemma parametrization and the eliminated
system as ``s29-minpoly.tar.zst``, pinned here by digest in
``resources/web/evand-exact-data-2026-10-12/acquisition/release.json``; his scripts are
retained at ``ad86d42`` in ``resources/web/evand-exact-and-local-reports-2026-10-12``.

This module is the **same-implementation** route of ``result-import.md`` stage 4: it runs
the author's own five scripts, unchanged, as his archive README gives them, and records
what they print.  It proves nothing his code does not; what it adds is a reproduction on
another machine from the pinned bytes, fresh random seeds for the two Monte Carlo steps,
and negative controls that his run did not have:

- ``irred.py`` on ``p * (x + 1)``, which must not report irreducibility;
- ``link.py``, ``verify_mod.py`` and ``contacts_mod.py`` on ``p`` with one coefficient
  changed by one, each of which must fail.

The archive is untrusted data.  It is unpacked outside the repository by the caller, every
member is held to the digest the packet pins before anything runs, the scripts are copied
from the retained packet (Git holds them; they are not compared with its
``upstream-subtree.sha256``) to a fresh directory, and each runs
under the given interpreter (a separate virtual environment with the author's pinned
``python-flint`` and ``mpmath``) with ``-I``, an empty working directory and every path
passed as an argument.  Nothing here imports from the archive or the scripts.

The receipt is one small JSON file: commands, versions, digests, seeds, wall and CPU time
per step and the lines each step printed last.  The archive's bytes never enter it.

Run it from ``packing/``::

    uv run --frozen --all-extras --group dev python -m devtools.evand_s29_replay \
        --data UNPACKED/n29-minpoly --python VENV/bin/python --work SCRATCH \
        --out RECEIPTS/replay.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import shutil
import subprocess
import sys
import time
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PACKET = ROOT / "resources/web/evand-exact-data-2026-10-12"
SCRIPTS_PACKET = ROOT / "resources/web/evand-exact-and-local-reports-2026-10-12"
SCRIPTS_DIR = SCRIPTS_PACKET / "source/search/exact/homotopy"
SCRIPTS = ("irred.py", "krawczyk.py", "link.py", "verify_mod.py", "contacts_mod.py")
MEMBER_PREFIX = "n29-minpoly/"

#: The archive README's counts: 12 primes for irreducibility, 50 and 21 for the two
#: Monte Carlo steps, and the link's working precision in bits.
IRRED_PRIMES = 12
VERIFY_PRIMES = 50
CONTACT_PRIMES = 21
LINK_PREC = "220000"

#: The coefficient the perturbed-polynomial control changes, by one.
PERTURBED_INDEX = 3606

TAIL_LINES = 24


@dataclass
class Step:
    """One run of one of the author's scripts, and what it must print to pass."""

    name: str
    script: str
    args: list[str]
    expect: str
    env: dict[str, str] = field(default_factory=dict)
    expect_failure: bool = False
    seed: int | None = None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_members(data: Path) -> list[dict[str, object]]:
    """Hold every unpacked member to the digest and size the packet pins."""
    release = json.loads((DATA_PACKET / "acquisition/release.json").read_text())
    checked = []
    for member in release["s29_archive"]["members"]:
        name = str(member["path"]).removeprefix(MEMBER_PREFIX)
        path = data / name
        actual = sha256_file(path)
        if actual != member["sha256"] or path.stat().st_size != member["bytes"]:
            raise SystemExit(f"{name}: digest or size differs from the pinned record")
        checked.append({"member": name, "bytes": member["bytes"], "sha256": actual})
    return checked


def check_scripts(destination: Path) -> dict[str, str]:
    """Copy the retained scripts out, recording what ran.

    Git holds the retained copies (OR-16): the digests go to the receipt as a record of
    what ran, and nothing here compares them with the repository's own listing.
    """
    destination.mkdir(parents=True, exist_ok=False)
    digests = {}
    for script in SCRIPTS:
        source = SCRIPTS_DIR / script
        shutil.copyfile(source, destination / script)
        digests[script] = sha256_file(destination / script)
    return digests


def write_controls(data: Path, work: Path) -> dict[str, object]:
    """Write the two control polynomials: p with one coefficient changed, and p * (x+1)."""
    sys.set_int_max_str_digits(0)
    coefficients = [
        int(c) for c in json.loads((data / "n29_poly_q4.json").read_text())["coeffs_ascending"]
    ]
    perturbed = list(coefficients)
    perturbed[PERTURBED_INDEX] += 1
    reducible = [0] * (len(coefficients) + 1)
    for index, value in enumerate(coefficients):
        reducible[index] += value
        reducible[index + 1] += value
    for name, values in (("perturbed.json", perturbed), ("reducible.json", reducible)):
        (work / name).write_text(json.dumps({"coeffs_ascending": [str(v) for v in values]}))
    return {
        "perturbed": f"coefficient of x^{PERTURBED_INDEX} increased by one",
        "reducible": "p * (x + 1), degree 7214",
    }


def interpreter_versions(python: str) -> dict[str, str]:
    probe = (
        "import json, sys, flint, sympy, mpmath; print(json.dumps({"
        "'python': sys.version.split()[0], 'python-flint': flint.__version__, "
        "'sympy': sympy.__version__, 'mpmath': mpmath.__version__}))"
    )
    result = subprocess.run(
        [python, "-I", "-c", probe], capture_output=True, text=True, check=True
    )
    return json.loads(result.stdout)


def run_step(step: Step, python: str, scripts: Path, work: Path) -> dict[str, object]:
    """Run one step with -I in an empty directory, measuring its own CPU time."""
    cwd = work / f"cwd-{step.name}"
    cwd.mkdir()
    env = {
        "PATH": "/usr/bin:/bin",
        "HOME": str(cwd),
        "OPENBLAS_NUM_THREADS": "1",
        "OMP_NUM_THREADS": "1",
        **step.env,
    }
    log = work / f"{step.name}.log"
    started = datetime.now(UTC)
    wall = time.monotonic()
    with log.open("w") as handle:
        process = subprocess.Popen(
            [python, "-I", str(scripts / step.script), *step.args],
            cwd=cwd,
            env=env,
            stdout=handle,
            stderr=subprocess.STDOUT,
        )
        _, status, usage = os.wait4(process.pid, 0)
        process.returncode = os.waitstatus_to_exitcode(status)
    wall_seconds = time.monotonic() - wall
    lines = log.read_text(errors="replace").splitlines()
    printed = "\n".join(lines)
    found = step.expect in printed
    # A control passes when the script prints its failure verdict (two of them then exit
    # nonzero); a replay step passes only on its success line and a clean exit.
    passed = found if step.expect_failure else found and process.returncode == 0
    return {
        "name": step.name,
        "script": step.script,
        "args": [arg.replace(str(work), "WORK") for arg in step.args],
        "env": step.env,
        "seed": step.seed,
        "started_utc": started.isoformat(timespec="seconds"),
        "wall_seconds": round(wall_seconds, 1),
        "cpu_seconds": round(usage.ru_utime + usage.ru_stime, 1),
        "max_rss_mb": round(usage.ru_maxrss / 1024, 1),
        "exit_code": process.returncode,
        "expect": step.expect,
        "expect_failure": step.expect_failure,
        "passed": passed,
        "tail": [line.replace(str(work), "WORK") for line in lines[-TAIL_LINES:]],
    }


def plan(data: Path, work: Path, shards: int, counts: dict[str, int]) -> list[Step]:
    system = str(data / "n29_system.jl")
    poly = str(data / "n29_poly_q4.json")
    box = str(data / "n29_krawczyk.json")
    s0 = str(data / "n29_S0.txt")
    params = [str(data / f"n29_param_t{i}.json") for i in range(1, 6)]
    perturbed, reducible = str(work / "perturbed.json"), str(work / "reducible.json")
    steps = [
        Step(
            "krawczyk",
            "krawczyk.py",
            [system, "1e-50", str(work / "krawczyk-out.json")],
            "UNIQUE ZERO of F in X",
        ),
        Step(
            "link",
            "link.py",
            [system, poly, box, s0, *params],
            "LINKED: S(t*) is a root of p",
            {"PREC": LINK_PREC},
        ),
        Step("irred", "irred.py", [poly, str(counts["irred"])], "IRREDUCIBLE over Q"),
    ]
    contact_seed = secrets.randbits(32)
    steps.append(
        Step(
            "contacts_mod",
            "contacts_mod.py",
            [system, poly, *params, str(counts["contacts"]), str(contact_seed)],
            "contact system consistent with S = x",
            seed=contact_seed,
        )
    )
    control_seed = secrets.randbits(32)
    steps += [
        Step(
            "control-link-perturbed",
            "link.py",
            [system, perturbed, box, s0, *params],
            "NOT LINKED",
            {"PREC": LINK_PREC},
            expect_failure=True,
        ),
        Step(
            "control-verify-perturbed",
            "verify_mod.py",
            [system, perturbed, *params, "1", str(control_seed)],
            "IDENTITY FAILS mod q",
            expect_failure=True,
            seed=control_seed,
        ),
        Step(
            "control-contacts-perturbed",
            "contacts_mod.py",
            [system, perturbed, *params, "1", str(control_seed)],
            "CONTACT CHECK FAILS mod q",
            expect_failure=True,
            seed=control_seed,
        ),
        Step(
            "control-irred-reducible",
            "irred.py",
            [reducible, "3"],
            "not proven",
            expect_failure=True,
        ),
    ]
    total = counts["verify"]
    per_shard = [total // shards + (1 if i < total % shards else 0) for i in range(shards)]
    for index, count in enumerate(per_shard):
        seed = secrets.randbits(32)
        steps.append(
            Step(
                f"verify_mod-{index + 1}",
                "verify_mod.py",
                [system, poly, *params, str(count), str(seed)],
                f"all identities hold modulo {count} random 62-bit primes",
                seed=seed,
            )
        )
    return steps


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument(
        "--data", type=Path, required=True, help="the unpacked n29-minpoly directory"
    )
    parser.add_argument(
        "--python", required=True, help="interpreter of the author's pinned environment"
    )
    parser.add_argument(
        "--work",
        type=Path,
        required=True,
        help="an empty scratch directory outside the repository",
    )
    parser.add_argument("--out", type=Path, required=True, help="the receipt JSON to write")
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument(
        "--shards",
        type=int,
        default=2,
        help="verify_mod.py processes, primes split between them",
    )
    parser.add_argument("--only", nargs="*", default=None, help="run only these step names")
    parser.add_argument("--irred-primes", type=int, default=IRRED_PRIMES)
    parser.add_argument("--contact-primes", type=int, default=CONTACT_PRIMES)
    parser.add_argument(
        "--verify-primes",
        type=int,
        default=VERIFY_PRIMES,
        help="the README uses 50; fewer when a compute cap requires it",
    )
    args = parser.parse_args(argv)

    data, work = args.data.resolve(), args.work.resolve()
    if work.exists() and any(work.iterdir()):
        raise SystemExit(f"{work} is not empty")
    work.mkdir(parents=True, exist_ok=True)
    started = datetime.now(UTC)
    members = check_members(data)
    scripts = work / "scripts"
    digests = check_scripts(scripts)
    controls = write_controls(data, work)
    counts = {
        "irred": args.irred_primes,
        "contacts": args.contact_primes,
        "verify": args.verify_primes,
    }
    steps = plan(data, work, args.shards, counts)
    if args.only:
        steps = [step for step in steps if step.name in set(args.only)]
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(lambda step: run_step(step, args.python, scripts, work), steps))
    fresh = (
        json.loads((work / "krawczyk-out.json").read_text())
        if (work / "krawczyk-out.json").exists()
        else None
    )
    archived = json.loads((data / "n29_krawczyk.json").read_text())
    receipt = {
        "format": "evand-s29-replay/1",
        "route": "same-implementation",
        "started_utc": started.isoformat(timespec="seconds"),
        "finished_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "archive": {
            "asset": "s29-minpoly.tar.zst",
            "sha256": "708e1b8b45894667f90a0d18b55bb35ed6079b84d33f9656976fd5cfa6f3729c",
            "members_checked": len(members),
            "members_match_pinned_record": True,
        },
        "scripts": {"retained_at": "ad86d42", "sha256": digests},
        "environment": {
            **interpreter_versions(args.python),
            "flags": "-I, empty working directory, paths as arguments",
            "machine": {"cpus": os.cpu_count(), "jobs": args.jobs},
        },
        "controls": controls,
        "prime_counts": {
            **counts,
            "readme": {
                "irred": IRRED_PRIMES,
                "contacts": CONTACT_PRIMES,
                "verify": VERIFY_PRIMES,
            },
        },
        "krawczyk_output_matches_archive": None
        if fresh is None
        else all(
            fresh[key] == archived[key] for key in ("certified", "radius", "tstar", "S_mid")
        ),
        "steps": results,
        "all_passed": all(result["passed"] for result in results),
        "cpu_seconds_total": round(sum(float(str(r["cpu_seconds"])) for r in results), 1),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2) + "\n")
    for result in results:
        print(
            f"{result['name']}: passed={result['passed']} "
            f"cpu={result['cpu_seconds']}s wall={result['wall_seconds']}s"
        )
    print(
        f"all_passed={receipt['all_passed']} cpu_seconds_total={receipt['cpu_seconds_total']}"
    )
    return 0 if receipt["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
