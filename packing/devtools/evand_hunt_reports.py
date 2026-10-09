"""Evan Daniel's #465 record-hunt certificates at e008180: custody, comparison, replay.

Issue #465 reports two exact rational certificates from the hunt1 record hunt in
evand/square-packing at e008180, at n = 132 and n = 155. The packet retains the
MIT-licensed source files at their upstream paths; ``devtools.acquire_source`` wrote it
and its ``check`` is the custody check here. ``read_facts`` admits the two certificates
only after that check passes, and only where each exact side equals the side the issue
prints.

``compare`` measures each certificate against the houses the record held when the issue
was read (main ``d3860c97a``, 9 October 2026), each rebuilt from its own retained
packet: Evan Daniel's T-098 certificate at 132 and the SQUISH update at 155. At 155 it
also compares the certificate with Francisco Couzo's issue451 certificate (T-128), whose
exact side is the same, square by square. ``acquisition/claims.json`` freezes that
comparison and ``check-claims`` rebuilds it, so a tampered prior or count is refused
however the case records later move.

Only the two rational certificates enter geometry decisions, through the maintained
two-route kernel of ``devtools.evand_arrangement_reports``: a positive, a duplicate-square
and an outside-container job for each count. No source program runs, and the KKT,
reduced-Hessian and jamming statements of the per-count reports are not replayed.

From ``packing/``, with the project interpreter::

    python -m devtools.evand_hunt_reports check-claims [--write]
    python -m devtools.evand_hunt_reports certify --jobs-dir SCRATCH/jobs --workers 2
    python -m devtools.evand_hunt_reports check [--replay]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import acquire_source
from devtools import couzo_refinement_reports as couzo451
from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools import squish_followup_packets as squish

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
PACKET = ROOT / "resources/web/evand-record-hunt-2026-10-09"
SOURCE = "https://github.com/evand/square-packing"
REVISION = "e0081804736a4613c2cf44c693ef1afe92518927"
ISSUE = "https://github.com/jlevy/squares/issues/465"
NUMBERS = (132, 155)
SOURCE_KEY = "[Daniel record hunt 2026-10-09]"
REPORT_EVIDENCE = "E-evand-465-record-hunt-report"
CLAIMS_FORMAT = "evand-465-record-hunt-claims-v1"
RECEIPT_FORMAT = "evand-465-record-hunt-exact-replay-v1"
WITNESS_PREFIX = "W-evand-465-n"
CLAIM_LIMITATIONS = (
    "Complete e008180 hunt1 rational centre/half-angle certificate converted exactly "
    "from the retained source. Finite construction feasibility only; no KKT, local "
    "minimum, rigidity, novelty, priority or global optimality claim."
)
#: The sides issue #465 prints, each the decimal expansion of its certificate's side.
OFFERED = {
    132: "11.987099332245063227179742877435",
    155: "12.952498944014007381965850566940",
}
#: When the issue was read, the case records cited these houses at each count.
READ_ON = "2026-10-09"
READ_AT_MAIN = "d3860c97a7037203701bcf262990ea0dee3a92dc"
HOUSES = {
    132: {
        "source_key": "[evand exact optima 2026-10-05]",
        "evidence": "E-evand-exact-optima-2026-10-05-exact-replay",
        "result": "T-098",
    },
    155: {
        "source_key": squish.SOURCE_KEY,
        "evidence": squish.EXACT_EVIDENCE,
        "result": "T-115",
    },
}
#: Couzo's issue451 certificate at 155, recorded as T-128 and pending adoption.
EQUAL_SIDE = {155: {"result": "T-128", "source_key": "[Couzo exact refinements 2026-10-08]"}}
DISPLAY_PLACES = 16
JOB_TIMEOUT = kernel.JOB_TIMEOUT
JOBS = kernel.JOBS
ROUTES = kernel.ROUTES
MAX_SOURCE_BYTES = 1_000_000


class ReportError(kernel.ReportError):
    """Refuse incomplete custody, a changed claim or an incomplete receipt."""


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """A JSON object with no repeated key."""
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ReportError("duplicate JSON key")
        result[key] = value
    return result


def ensure_private(path: Path) -> None:
    if path.is_symlink() or not path.resolve().is_relative_to(REPO.resolve()):
        raise ReportError(f"{path}: retained evidence must be a private repository file")


def certificate_path(n: int) -> str:
    if type(n) is not int or n not in NUMBERS:
        raise ReportError("count outside the two #465 certificates")
    return f"search/packer/candidates/hunt1_n{n}.cert"


def claims_path() -> Path:
    return PACKET / "acquisition/claims.json"


def receipt_path() -> Path:
    return PACKET / "receipts/exact-certification.json.xz"


def read_facts() -> dict[int, legacy.Certificate]:
    """Admit both certificates once the packet's custody check passes."""
    ensure_private(PACKET)
    if problems := acquire_source.check(PACKET, REPO):
        raise ReportError("packet custody: " + "; ".join(problems))
    certificates = {}
    for n in NUMBERS:
        path = PACKET / "source" / certificate_path(n)
        ensure_private(path)
        with path.open("rb") as stream:
            raw = stream.read(MAX_SOURCE_BYTES + 1)
        if len(raw) > MAX_SOURCE_BYTES:
            raise ReportError(f"n={n}: certificate exceeds its byte ceiling")
        certificate = legacy.parse(raw.decode("utf-8"), expected_n=n)
        if certificate.side != Fraction(Decimal(OFFERED[n])):
            raise ReportError(f"n={n}: certificate side differs from the side #465 prints")
        certificates[n] = certificate
    return certificates


def house_side(n: int) -> Fraction:
    """The exact side of the house the case cited at ``n``, from its own retained packet."""
    if n == 132:
        path = legacy.certificate_path(legacy.CERTS, n)
        return legacy.parse(path.read_text(encoding="utf-8"), expected_n=n).side
    if n == 155:
        return Fraction(squish.read_fact(n)["side"])
    raise ReportError("count outside the two #465 certificates")


def pose_comparison(first: legacy.Certificate, second: legacy.Certificate) -> dict[str, Any]:
    """Which exact (x, y, t) poses two certificates share, and which they do not."""
    if first.n != second.n:
        raise ReportError("pose comparison needs two certificates of one count")
    left = [(p.x, p.y, p.t) for p in first.poses]
    right = [(p.x, p.y, p.t) for p in second.poses]
    if len(set(left)) != len(left) or len(set(right)) != len(right):
        raise ReportError("a certificate repeats a pose")
    shared = set(left) & set(right)
    return {
        "identical_poses": len(shared),
        "differing_here": [i for i, pose in enumerate(left) if pose not in shared],
        "differing_there": [i for i, pose in enumerate(right) if pose not in shared],
    }


def compare(certificates: dict[int, legacy.Certificate] | None = None) -> dict[str, Any]:
    """The frozen claim record, rebuilt from the certificates and the retained houses."""
    certificates = read_facts() if certificates is None else certificates
    rows = []
    for n in NUMBERS:
        side = certificates[n].side
        prior = house_side(n)
        if not side < prior:
            raise ReportError(f"n={n}: certificate side is not below the cited house")
        row: dict[str, Any] = {
            "n": n,
            "certificate": certificate_path(n),
            "offered_side": OFFERED[n],
            "exact_side": legacy.literal(side),
            "ceiling": legacy.ceiling_decimal(side, DISPLAY_PLACES),
            "house": {
                **HOUSES[n],
                "exact_side": legacy.literal(prior),
                "ceiling": legacy.ceiling_decimal(prior, DISPLAY_PLACES),
                "below_by": legacy.literal(prior - side),
            },
        }
        if n in EQUAL_SIDE:
            other = couzo451.read_facts()[n]
            if other.side != side:
                raise ReportError(f"n={n}: T-128's side no longer equals this certificate's")
            row["equal_side"] = {
                **EQUAL_SIDE[n],
                "exact_side": legacy.literal(other.side),
                **pose_comparison(certificates[n], other),
            }
        rows.append(row)
    return {
        "format": CLAIMS_FORMAT,
        "issue": ISSUE,
        "source": SOURCE,
        "revision": REVISION,
        "read_on": READ_ON,
        "read_at_main": READ_AT_MAIN,
        "results": rows,
    }


def _json_text(value: Any) -> str:
    return json.dumps(value, indent=2, allow_nan=False) + "\n"


def write_claims() -> None:
    ensure_private(claims_path())
    with atomic_output_file(claims_path()) as temporary:
        temporary.write_text(_json_text(compare()), encoding="utf-8")


def check_claims(certificates: dict[int, legacy.Certificate] | None = None) -> dict[str, Any]:
    ensure_private(claims_path())
    stored = json.loads(
        claims_path().read_text(encoding="utf-8"), object_pairs_hook=unique_object
    )
    rebuilt = compare(certificates)
    if stored != rebuilt:
        raise ReportError("frozen claim record differs from its rebuild")
    return rebuilt


def validate_certification(value: Any, facts: dict[int, legacy.Certificate]) -> dict[int, Any]:
    if (
        type(value) is not dict
        or set(value) != {"format", "routes", "cases"}
        or value["format"] != RECEIPT_FORMAT
        or value["routes"] != list(ROUTES)
        or type(value["cases"]) is not list
        or len(value["cases"]) != len(NUMBERS) * len(JOBS)
        or list(facts) != list(NUMBERS)
    ):
        raise ReportError("incomplete six-job exact receipt envelope")
    positives = {}
    jobs = ((n, control) for n in NUMBERS for control in JOBS)
    for (n, control), row in zip(jobs, value["cases"], strict=True):
        kernel.validate_job(
            row,
            facts[n],
            control,
            witness_prefix=WITNESS_PREFIX,
            claim_limitations=CLAIM_LIMITATIONS,
        )
        if control == "positive":
            positives[n] = row
    return positives


def _stable(row: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in row.items() if k not in {"cpu_seconds", "wall_seconds"}}


def check_certification(
    numbers: list[int] | None = None, *, replay: bool = False
) -> dict[int, Any]:
    """Admit the retained receipt; with ``replay``, decide the selected counts again."""
    selected = list(NUMBERS) if numbers is None else numbers
    if (
        not selected
        or any(type(n) is not int for n in selected)
        or len(set(selected)) != len(selected)
        or set(selected) - set(NUMBERS)
    ):
        raise ReportError("empty, repeated or unknown replay selection")
    facts = read_facts()
    ensure_private(receipt_path())
    record = kernel.read_xz(receipt_path())
    positives = validate_certification(record, facts)
    if replay:
        jobs = ((n, control) for n in NUMBERS for control in JOBS)
        for (n, control), row in zip(jobs, record["cases"], strict=True):
            if n not in selected:
                continue
            fresh = kernel.run_case(
                facts[n],
                control,
                witness_prefix=WITNESS_PREFIX,
                claim_limitations=CLAIM_LIMITATIONS,
            )
            if _stable(fresh) != _stable(row):
                raise ReportError(f"n={n} {control}: fresh replay differs from the receipt")
    return positives


def run_child(job: tuple[int, str], directory: Path, timeout: int) -> dict[str, Any]:
    n, control = job
    if type(n) is not int or n not in NUMBERS or control not in JOBS:
        raise ReportError("job outside the complete certificate/control roster")
    if type(timeout) is not int or not 1 <= timeout <= JOB_TIMEOUT:
        raise ReportError("invalid bounded deadline")
    path = directory / f"n{n}-{control}.json"
    if path.exists():
        raise ReportError("refusing to overwrite a deciding job")
    command = [
        sys.executable,
        "-m",
        "devtools.evand_hunt_reports",
        "decide-job",
        "--n",
        str(n),
        "--control",
        control,
        "--output",
        str(path),
    ]
    try:
        completed = subprocess.run(command, capture_output=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as error:
        path.with_suffix(".stdout.log").write_bytes(error.stdout or b"")
        path.with_suffix(".stderr.log").write_bytes(error.stderr or b"")
        raise ReportError(f"native job {n}/{control} exceeded {timeout}s") from error
    path.with_suffix(".stdout.log").write_bytes(completed.stdout)
    path.with_suffix(".stderr.log").write_bytes(completed.stderr)
    if completed.returncode:
        raise ReportError(f"native job {n}/{control} exited {completed.returncode}")
    with path.open("rb") as stream:
        raw = stream.read(kernel.MAX_BYTES + 1)
    if len(raw) > kernel.MAX_BYTES:
        raise ReportError("native job exceeds the existing receipt ceiling")
    try:
        value = json.loads(raw, object_pairs_hook=unique_object)
    except ValueError as error:
        raise ReportError(f"native job {n}/{control} is not strict JSON") from error
    if type(value) is not dict:
        raise ReportError("complete native job object required")
    return value


def certify(directory: Path, *, workers: int = 2, timeout: int = JOB_TIMEOUT) -> None:
    if (
        type(workers) is not int
        or not 1 <= workers <= 2
        or type(timeout) is not int
        or not 1 <= timeout <= JOB_TIMEOUT
    ):
        raise ReportError("invalid bounded worker/deadline selection")
    ensure_private(receipt_path())
    facts = read_facts()
    if directory.exists():
        raise ReportError("native job directory must be a fresh attempt")
    directory.mkdir(parents=True)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        cases = list(
            pool.map(
                lambda job: run_child(job, directory, timeout),
                ((n, control) for n in NUMBERS for control in JOBS),
            )
        )
    value = {"format": RECEIPT_FORMAT, "routes": list(ROUTES), "cases": cases}
    validate_certification(value, facts)
    kernel.save_xz(receipt_path(), value)


def margins(positives: dict[int, Any]) -> dict[int, dict[str, str]]:
    """The least wall and pair clearance each route found in each positive job."""
    return {
        n: {
            f"{route}_{field}": row[route][f"minimum_{field}"]
            for route in ROUTES
            for field in ("containment_clearance", "best_pair_gap")
        }
        for n, row in positives.items()
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    claims = sub.add_parser("check-claims")
    claims.add_argument("--write", action="store_true")
    campaign = sub.add_parser("certify")
    campaign.add_argument("--jobs-dir", type=Path, required=True)
    campaign.add_argument("--workers", type=int, default=2)
    campaign.add_argument("--timeout", type=int, default=JOB_TIMEOUT)
    check = sub.add_parser("check")
    check.add_argument("--n", type=int, nargs="+")
    check.add_argument("--replay", action="store_true")
    job = sub.add_parser("decide-job")
    job.add_argument("--n", type=int, choices=NUMBERS, required=True)
    job.add_argument("--control", choices=JOBS, required=True)
    job.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.action == "check-claims":
        if args.write:
            write_claims()
        print(json.dumps(check_claims(), indent=2))
    elif args.action == "certify":
        certify(args.jobs_dir, workers=args.workers, timeout=args.timeout)
    elif args.action == "check":
        positives = check_certification(args.n, replay=args.replay)
        print(json.dumps(margins(positives), indent=2))
        print(f"both certificates and all {len(NUMBERS) * len(JOBS)} full jobs admitted")
    else:
        certificate = read_facts()[args.n]
        row = kernel.run_case(
            certificate,
            args.control,
            witness_prefix=WITNESS_PREFIX,
            claim_limitations=CLAIM_LIMITATIONS,
        )
        kernel.validate_job(
            row,
            certificate,
            args.control,
            witness_prefix=WITNESS_PREFIX,
            claim_limitations=CLAIM_LIMITATIONS,
        )
        if args.output.exists():
            raise ReportError("refusing to overwrite an actual deciding job")
        with atomic_output_file(args.output) as temporary:
            temporary.write_text(json.dumps(row, separators=(",", ":"), allow_nan=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
