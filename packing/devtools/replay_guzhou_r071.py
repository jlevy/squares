"""Stage Guzhou0806's R071 package from the retained bytes, replay it, and run its controls.

Stage 4 of the result import process replays the source's own verification on the
retained bytes, in full (``campaign/result-import.md``). For R071 that is the package's
``run_public.js bound``: it checks the package against its ``MANIFEST.json``, compiles
Guzhou0806's C++ checker, and runs it beside Overbeck's Node BigInt checker over all
5,114 parent-angle intervals of the C027 certificate through the paired launcher
``replay.js`` at two partitions, then holds ``THEOREM.json`` to the claimed target,
minimum, budget, surplus and certificate digest.

The packet ``resources/web/n17-guzhou-r071-2026-09-30/`` retains the certificate, the
launchers and the package's documents, with its large files as deterministic gzip. It
pins the sixteen files under ``project/base/upstream/`` by digest only, because the R068
packet retains the same bytes, and it pins the C021 to C029 research files the bound does
not read by digest only too. This tool puts the package back together.

``stage --work DIR [--checkout CLONE]``
    Writes ``DIR/R071-C029/``: every file the packet's ``upstream-subtree.sha256`` lists
    under ``certificates/R071-C029/``, decompressed, the pinned-only checker files from
    the copy ``acquisition/sources.json`` names, and the pinned-only research files from
    ``CLONE``, a checkout of the source at ``8c11f696``. Each file's SHA-256 must equal
    the manifest's, so the staged package is the upstream package byte for byte. Without
    ``CLONE`` the research files are left out and listed; the package then holds every
    file the bound reads, but not every file ``check_package.js`` reads.
``run --work DIR [--cores 2,3] [--route public|paired]``
    The ``public`` route, the default, needs a complete package: it runs ``node
    check_package.js`` and then ``node run_public.js bound DIR/bound`` in the staged
    package, each under ``devtools.replay_receipt``, writing
    ``DIR/receipts/check_package.log`` and ``DIR/receipts/bound.log``. The ``paired``
    route runs what ``run_public.js bound`` runs without its package check, R068's
    commands: ``g++ -O3 -std=c++17`` on ``verify.cpp`` into ``DIR/bound/bin/verify``,
    and ``replay.js`` on the certificate into ``DIR/bound/global`` at two partitions,
    writing ``DIR/receipts/build.log`` and ``DIR/receipts/paired.log``. Either replay
    runs pinned to ``--cores`` with ``N17_TIMEOUT_MINUTES=600``, the launcher's
    documented per-process timeout, as R068's replay here did.
``control KIND --work DIR [--start I --count K]``
    Stage 4's negative control: writes a mutated copy of the certificate
    (``mutate``) and runs the built C++ checker and the BigInt checker on it over
    intervals ``I`` to ``I + K - 1``, each under ``devtools.replay_receipt``, writing
    ``DIR/receipts/control-KIND-cpp.log`` and ``control-KIND-bigint.log``. The
    receipt's ``cwd`` line names the mutated certificate's SHA-256 and the change, and
    each checker must refuse it, which ``tests/test_guzhou_r071_packet.py`` holds.
``retain --work DIR``
    Copies the run's records into the packet's ``receipts/r071/replay/``, compressing
    the partition records by the archive's rule, and the receipts into
    ``receipts/r071/``; prints the Compressed Files rows the README needs.

What a replay decides is read afterwards by ``devtools.audit_guzhou_r071 compare``.
This tool decides nothing about the certificate: it guarantees which bytes were run.

Usage (from ``packing/``)::

    .venv/bin/python3 -m devtools.replay_guzhou_r071 stage --work SCRATCH --checkout CLONE
    .venv/bin/python3 -m devtools.replay_guzhou_r071 run --work SCRATCH --cores 2,3
    .venv/bin/python3 -m devtools.replay_guzhou_r071 control over-claim --work SCRATCH
    .venv/bin/python3 -m devtools.replay_guzhou_r071 retain --work SCRATCH
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import replay_receipt
from devtools.retained_data import compress, describe, read_retained_bytes, retained_exists

REPO = Path(__file__).resolve().parents[2]
PACKET = REPO / "packing/resources/web/n17-guzhou-r071-2026-09-30"
SOURCE_ROOT = PACKET / "n17-square-packing"
SUBTREE = PACKET / "acquisition/upstream-subtree.sha256"
SOURCES = PACKET / "acquisition/sources.json"
PACKAGE = "certificates/R071-C029"
CERTIFICATE = "bounds/c027/certificate.json"
CERTIFICATE_SHA256 = "15b6bf6a936eba71338c9ea3e3b9966ae21db8116a6f5a92a8b5da5ccabed469"
VERIFY = "project/base/upstream/cpp/verify.cpp"
BIGINT = "project/base/upstream/cpp/reference/verify_global_variable.js"
RECEIPTS = PACKET / "receipts/r071"
#: The partition records ``replay.js`` writes at two partitions.
PARTITIONS = ("cpp-0", "cpp-1", "node-0", "node-1")
CWD_LABEL = (
    "{package}, the R071 package staged by devtools.replay_guzhou_r071 from the packet, "
    "byte-identical to certificates/R071-C029/ at 8c11f696"
)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def subtree_digests() -> dict[str, str]:
    """The SHA-256 of every upstream file under the package, by package-relative path."""
    prefix = f"./{PACKAGE}/"
    digests: dict[str, str] = {}
    for line in SUBTREE.read_text(encoding="utf-8").splitlines():
        digest, path = line.split("  ", 1)
        if path.startswith(prefix):
            digests[path.removeprefix(prefix)] = digest
    return digests


def pinned_copies() -> dict[str, Path]:
    """Where the packet says each pinned-only file of the package is retained."""
    record = json.loads(SOURCES.read_text(encoding="utf-8"))
    prefix = f"{PACKAGE}/"
    return {
        entry["path"].removeprefix(prefix): REPO / entry["identical_to"]
        for source in record["sources"]
        for entry in source["pinned_only"]
        if entry["path"].startswith(prefix) and "identical_to" in entry
    }


def stage(work: Path, checkout: Path | None = None) -> tuple[Path, list[str]]:
    """Write the package under ``work``; return it and the files left out.

    A file comes from the packet, from the retained copy the packet names, or from
    ``checkout``; any byte whose digest is not the manifest's is refused.
    """
    package = work / "R071-C029"
    _require(not package.exists(), f"{package} exists; stage into a fresh directory")
    pinned = pinned_copies()
    missing: list[str] = []
    for relative, digest in sorted(subtree_digests().items()):
        retained = SOURCE_ROOT / PACKAGE / relative
        if relative in pinned:
            data = read_retained_bytes(pinned[relative])
        elif retained_exists(retained):
            data = read_retained_bytes(retained)
        elif checkout is not None:
            data = (checkout / PACKAGE / relative).read_bytes()
        else:
            missing.append(relative)
            continue
        _require(_sha256(data) == digest, f"{relative} is not the pinned bytes")
        target = package / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return package, missing


def _bound_argv(work: Path, cores: str) -> list[str]:
    return [
        "env",
        "N17_TIMEOUT_MINUTES=600",
        "taskset",
        "-c",
        cores,
        "node",
        "run_public.js",
        "bound",
        str(work / "bound"),
    ]


def _receipt(argv: list[str], work: Path, name: str) -> dict[str, object]:
    package = work / "R071-C029"
    return replay_receipt.run(
        argv,
        receipt=work / "receipts" / f"{name}.log",
        cwd_label=CWD_LABEL.format(package=package),
        python_note="not used by this command",
        chdir=package,
    )


def run(work: Path, cores: str, route: str = "public") -> list[dict[str, object]]:
    """The complete paired replay by ``route``, each command under a receipt."""
    if route == "public":
        fields = [_receipt(["node", "check_package.js"], work, "check_package")]
        if fields[0]["exit"] == 0:
            fields.append(_receipt(_bound_argv(work, cores), work, "bound"))
        return fields
    _require(route == "paired", f"unknown route {route}")
    executable = work / "bound/bin/verify"
    executable.parent.mkdir(parents=True, exist_ok=False)
    build = ["g++", "-O3", "-std=c++17", VERIFY, "-o", str(executable)]
    fields = [_receipt(build, work, "build")]
    if fields[0]["exit"] == 0:
        replay = [
            *_bound_argv(work, cores)[:5],
            "node",
            "project/base/upstream/cpp/replay.js",
            CERTIFICATE,
            str(work / "bound/global"),
            str(executable),
            "2",
        ]
        fields.append(_receipt(replay, work, "paired"))
    return fields


def _threshold_budget(orbit: dict[str, Any]) -> int:
    """What one threshold orbit adds to the budget, as both checkers compute it."""
    sets = orbit["sets"]
    if orbit.get("winning_masks"):
        capacity = 1
    else:
        coefficients = orbit.get("coefficients") or [1] * len(sets[0])
        capacity = sum(int(c) for c in coefficients) // int(orbit["threshold"])
    return int(orbit["weight"]) * len(sets) * capacity


def _over_claim(cert: dict[str, Any]) -> str:
    """Claim 9321/2000 on the same cores: shrink the parent side, keep every interval."""
    target = Fraction(9321, 2000)
    side = Fraction(cert["L"]) / target
    cert["A"] = f"{side.numerator}/{side.denominator}"
    cert["normalized_target"] = f"{target.numerator}/{target.denominator}"
    return f"A {cert['A']} and normalized_target {cert['normalized_target']}, cores unchanged"


def _drop_rule(cert: dict[str, Any]) -> str:
    """Zero the heaviest rule orbit's weight and its budget share; keep the request."""
    orbits = cert["threshold_orbits"]
    index = max(range(len(orbits)), key=lambda i: (int(orbits[i]["weight"]), -i))
    removed = _threshold_budget(orbits[index])
    weight = int(orbits[index]["weight"])
    orbits[index]["weight"] = 0
    cert["budget_units"] = int(cert["budget_units"]) - removed
    return (
        f"rule orbit {index} of weight {weight} zeroed, budget_units {cert['budget_units']} "
        f"(minus {removed}), minimum_units {cert['minimum_units']} unchanged"
    )


#: Each mutation edits the parsed certificate in place and says what it changed.
MUTATIONS: dict[str, Callable[[dict[str, Any]], str]] = {
    "over-claim": _over_claim,
    "drop-rule": _drop_rule,
}


def mutate(kind: str, original: bytes) -> tuple[bytes, str]:
    """The mutated certificate's bytes and a one-line description of the change."""
    _require(_sha256(original) == CERTIFICATE_SHA256, "not the C027 certificate")
    cert = json.loads(original)
    change = MUTATIONS[kind](cert)
    return (json.dumps(cert, separators=(",", ":")) + "\n").encode(), change


def control(kind: str, work: Path, start: int, count: int) -> list[dict[str, object]]:
    """Run both checkers on the ``kind`` mutation over ``count`` intervals from ``start``."""
    package = work / "R071-C029"
    executable = work / "bound/bin/verify"
    _require(executable.is_file(), f"{executable} is missing; run the replay first")
    data, change = mutate(kind, (package / CERTIFICATE).read_bytes())
    directory = work / "controls" / kind
    directory.mkdir(parents=True, exist_ok=False)
    mutated = directory / "certificate.json"
    mutated.write_bytes(data)
    label = (
        f"{package}, the staged R071 package; certificate {_sha256(data)}, the {kind} "
        f"mutation of {CERTIFICATE_SHA256} ({CERTIFICATE}): {change}; "
        f"intervals {start} to {start + count - 1}; C++ executable "
        f"{_sha256(executable.read_bytes())}"
    )
    commands = {
        "cpp": [
            str(executable),
            str(mutated),
            str(directory / "cpp.json"),
            "--range",
            str(start),
            str(count),
        ],
        "bigint": [
            "node",
            BIGINT,
            str(mutated),
            str(directory / "node.json"),
            str(start),
            str(count),
        ],
    }
    return [
        replay_receipt.run(
            argv,
            receipt=work / "receipts" / f"control-{kind}-{checker}.log",
            cwd_label=label,
            python_note="not used by this command",
            chdir=package,
        )
        for checker, argv in commands.items()
    ]


def _copy(source: Path, target: Path, work: Path) -> None:
    """Copy one record, writing the scratch directory as ``WORK`` in a text receipt."""
    data = source.read_bytes()
    if source.suffix == ".log" or source.name == "REPLAY.json":
        data = data.replace(str(work).encode(), b"WORK")
    target.write_bytes(data)


def retain(work: Path) -> list[str]:
    """Copy the run's records and receipts into the packet; return the table rows.

    The replay's records go to ``receipts/r071/replay/``, its receipts to
    ``receipts/r071/``, and each control's receipts and checker outputs to
    ``receipts/r071/controls/``; the mutated certificates are not kept, since
    `mutate` re-derives them from the retained one. The scratch directory is written
    ``WORK`` in the logs and ``REPLAY.json``, as R068's replay record writes it; the
    partition records, ``THEOREM.json`` and ``INPUTS.json`` name no path and are kept
    byte for byte.
    """
    run_dir = work / "bound"
    replay = RECEIPTS / "replay"
    controls = RECEIPTS / "controls"
    replay.mkdir(parents=True, exist_ok=False)
    controls.mkdir(exist_ok=False)
    rows: list[str] = []
    for name in PARTITIONS:
        target = replay / f"{name}.json"
        shutil.copyfile(run_dir / "global" / f"{name}.json", target)
        rows.append(describe(PACKET, compress(target), "receipt").markdown())
        _copy(run_dir / "global" / f"{name}.log", replay / f"{name}.log", work)
    for name in ("THEOREM.json", "INPUTS.json"):
        shutil.copyfile(run_dir / "global" / name, replay / name)
    if (run_dir / "REPLAY.json").is_file():
        _copy(run_dir / "REPLAY.json", replay / "REPLAY.json", work)
    for log in sorted((work / "receipts").glob("*.log")):
        folder = controls if log.name.startswith("control-") else RECEIPTS
        _copy(log, folder / log.name, work)
    for kind in sorted(MUTATIONS):
        for output, checker in (("cpp.json", "cpp"), ("node.json", "bigint")):
            source = work / "controls" / kind / output
            if source.is_file():
                shutil.copyfile(source, controls / f"control-{kind}-{checker}.json")
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("stage", "run", "control", "retain"):
        sub = commands.add_parser(name)
        sub.add_argument("--work", type=Path, required=True)
        if name == "stage":
            sub.add_argument("--checkout", type=Path, help="a clone of the source at 8c11f696")
        if name == "run":
            sub.add_argument("--cores", default="2,3", help="taskset CPU list for the replay")
            sub.add_argument("--route", choices=("public", "paired"), default="public")
        if name == "control":
            sub.add_argument("kind", choices=sorted(MUTATIONS))
            sub.add_argument("--start", type=int, default=0)
            sub.add_argument("--count", type=int, default=1)
    args = parser.parse_args()
    work = args.work.resolve()
    if args.command == "stage":
        package, missing = stage(work, args.checkout)
        print(package)
        if missing:
            print(f"left out {len(missing)} pinned-only research files", file=sys.stderr)
        return 0
    if args.command == "retain":
        for row in retain(work):
            print(row)
        return 0
    if args.command == "run":
        fields = run(work, args.cores, args.route)
        print(json.dumps(fields, indent=2))
        return max(int(str(f["exit"])) for f in fields)
    fields = control(args.kind, work, args.start, args.count)
    print(json.dumps(fields, indent=2))
    return 0 if all(f["exit"] != 0 for f in fields) else 1


if __name__ == "__main__":
    raise SystemExit(main())
