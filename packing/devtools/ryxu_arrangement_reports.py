"""Import issue432's complete rational source packings with full native exact replay.

All25 source configurations are retained, including those superseded by later
bounds. The independently decidable rational certificates are separate from the
source's undilated n51 radical claim. Producer code is never executed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
PACKET = ROOT / "resources/web/ry-xu-new-packings-2026-10-08"
SOURCE = "https://github.com/ry-xu/square_packing"
REVISION = "8dc415296f697f5140caea27c7a0193d52deb4e6"
NUMBERS = (
    51,
    70,
    84,
    86,
    88,
    102,
    103,
    105,
    108,
    123,
    126,
    127,
    129,
    130,
    131,
    146,
    153,
    175,
    179,
    236,
    258,
    261,
    263,
    267,
    295,
)
SOURCE_KEY = "ry-xu-new-packings-2026-10-08"
EXACT_EVIDENCE = "E-ryxu-432-rational-feasibility"
PREFIX = "W-ryxu-432-n"
LIMITATIONS = (
    "Issue432 source rational centre/half-angle construction converted exactly, "
    "without additional dilation. Feasibility only, not global optimality, rigidity "
    "or an identity with the separate undilated n51 radical construction."
)
FACT_FORMAT = "ryxu-432-complete-source-facts-v1"
RECEIPT_FORMAT = "ryxu-432-complete-exact-replay-v1"
JOBS = kernel.JOBS
ROUTES = kernel.ROUTES
MAX_BYTES = 4_000_000
JOB_TIMEOUT = 600
SOURCE_SHA256: dict[int, str] = {
    51: "98ea45e1a053a66d0aec66b83c19735a1df7bad66885987b4c2c9b3baf9df9a0",
    70: "c63b0d6d1a7cb0b6f1a2ed69b642d02a4e229581b778233a4233cfdff334c610",
    84: "be40c8ea9c52bff7754af502f29393df41dbc246a550e43a3c1b84c758296c3b",
    86: "00f6a5df981b1ccbc5194b755052b6d598ff1d596ec0146f6b63fbd22de87d58",
    88: "c01ae153fa5511e992a9831256a4b4192f62272dca9d7b770684c5457d0e4050",
    102: "b8d35393f14ce57230ee524f2d5b99082e659871fca337b4acad570d057eafb2",
    103: "4e12ee37bc9f1f20149b6a2e0955569a1bd213d50d81dfc16026d1b9c9eb9ceb",
    105: "b251c331b00b5e6e4041b4253c4e46e2afcaa55c291ee6962b890d3c0947f02a",
    108: "852f580f762df5845bc46cd6c41c02010dbbf3616d090175d7dbe12eeedc98df",
    123: "30f740f1fda4ab5f19ff3a9cf45b3643b7befad83d9a1b48ddf3c9ca2e04f290",
    126: "f30d11d1666d84951cc2661e834dae14ef8164406812213fc0506fc98b265cbd",
    127: "196d22b40ce485484df9345c19fea648c14da9a32ff8c407ea9686fa4588aa0f",
    129: "67ed26af2ffdfa506465ec32f1045b663765283f9b842e29bc154a627ca73271",
    130: "fd8968e04d9ba80804d84ee21975d1e89b0f8ef56fa00ee8aa68a820f149d696",
    131: "34c7eb6ab4c66386f6e2333771da366b689ce0f1e4f409631c74eff1fd1101f1",
    146: "67b8411e2e7f8d000e6352cd3344c7376ea10916d53e02a323f33af10de930cd",
    153: "2ac0df81630e4e9405200503e0e57d1da824860e2b1a9082a1e037b9d9d01512",
    175: "ac04b40defa2a5b179418681da0f6e96db0cf378438e47605125783fd06c9ff2",
    179: "c26d6252756b5ac4849a617ab0540b72d3fda6be96737be4690e829da9415567",
    236: "1334bc1d110ebbd7e1f26ac6d5e90c5326c26b222ca5131359892dded0efab28",
    258: "2ff87a46bee713d75b6fdff0a805304dc2992963614cc5091d12d1a293f508ed",
    261: "5e0192f12ecb70f3a5e8c6c3b0d39b0f29832e0179f98907fbf062d7c7a1d88b",
    263: "a38a2427ab791b5f4448ecf4a8eb28db5ce361c807d2f596f7f0f7d25ef43bee",
    267: "f226635e43bae7017b95dad7e7140c3c9051c516e6b7c8d55ad7c244eeffa88d",
    295: "30255a2929b380007428863b9ee68c44db487981721c12dc9bb76ff17eba482f",
}


def source_path(n: int) -> str:
    if type(n) is not int or n not in NUMBERS:
        raise ValueError("count outside the complete issue432 roster")
    return f"certificates/n{n:03d}/n{n:03d}.cert.json"


def fact_path() -> Path:
    return PACKET / "facts/complete-certificates.json.xz"


def receipt_path() -> Path:
    return PACKET / "receipts/exact-certification.json.xz"


def canonical_json(value: Any) -> bytes:
    return (
        json.dumps(value, separators=(",", ":"), sort_keys=True, allow_nan=False) + "\n"
    ).encode()


def unique_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate source JSON key")
        result[key] = value
    return result


def _rational(value: object) -> Fraction:
    if (
        type(value) is not str
        or len(value) > 1024
        or re.fullmatch(r"-?[0-9]+(?:/[1-9][0-9]*)?", value) is None
    ):
        raise ValueError("exact source scalar must be a bounded rational string")
    return Fraction(value)


def parse(text: str, n: int) -> legacy.Certificate:
    """Validate the complete source syntax; source precision labels decide nothing."""
    source_path(n)
    row = json.loads(text, object_pairs_hook=unique_json_keys)
    expected = {"n", "s_exact", "s_decimal_ceiling", "dilation_eps", "angle_param", "squares"}
    if (
        type(row) is not dict
        or set(row) != expected
        or type(row["n"]) is not int
        or row["n"] != n
    ):
        raise ValueError("source certificate namespace or count mismatch")
    if (
        row["dilation_eps"] != "1/10^12"
        or row["angle_param"] != "t = tan(theta/2); cos = (1-t^2)/(1+t^2), sin = 2t/(1+t^2)"
        or type(row["s_decimal_ceiling"]) is not str
        or re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", row["s_decimal_ceiling"]) is None
        or len(row["s_decimal_ceiling"]) > 128
    ):
        raise ValueError("unsupported source precision or angle metadata")
    side = _rational(row["s_exact"])
    poses = row["squares"]
    if side <= 0 or type(poses) is not list or len(poses) != n:
        raise ValueError("positive side and complete source roster required")
    result = []
    for pose in poses:
        if type(pose) is not dict or set(pose) != {"x", "y", "t"}:
            raise ValueError("square must contain exactly x, y and t")
        result.append(legacy.Pose(*(_rational(pose[key]) for key in ("x", "y", "t"))))
    return legacy.Certificate(n=n, side=side, poses=tuple(result))


def ensure_private(path: Path) -> None:
    if not path.resolve().is_relative_to(REPO.resolve()):
        raise ValueError(
            "source facts and deciding receipts must remain private to this checkout"
        )


def save(path: Path, value: Any) -> None:
    ensure_private(path)
    data = canonical_json(value)
    if len(data) > MAX_BYTES:
        raise ValueError("complete evidence exceeds the unchanged receipt ceiling")
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_bytes(lzma.compress(data, preset=6))


def acquire(directory: Path) -> None:
    """Bind all original factual certificate bytes to the immutable upstream download."""
    cases = []
    for n in NUMBERS:
        path = directory / source_path(n)
        with path.open("rb") as stream:
            data = stream.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES or hashlib.sha256(data).hexdigest() != SOURCE_SHA256[n]:
            raise ValueError("source acquisition differs from the frozen upstream certificate")
        text = data.decode()
        parse(text, n)
        cases.append({"n": n, "source_path": source_path(n), "source_certificate": text})
    save(
        fact_path(),
        {"format": FACT_FORMAT, "source": SOURCE, "revision": REVISION, "cases": cases},
    )


def read_facts() -> dict[int, legacy.Certificate]:
    ensure_private(fact_path())
    record = kernel.read_xz(fact_path())
    if type(record) is not dict or set(record) != {"format", "source", "revision", "cases"}:
        raise ValueError("invalid complete source fact envelope")
    if (record["format"], record["source"], record["revision"]) != (
        FACT_FORMAT,
        SOURCE,
        REVISION,
    ):
        raise ValueError("wrong issue432 source namespace")
    if type(record["cases"]) is not list or len(record["cases"]) != len(NUMBERS):
        raise ValueError("incomplete issue432 source roster")
    result = {}
    for n, row in zip(NUMBERS, record["cases"], strict=True):
        if type(row) is not dict or set(row) != {"n", "source_path", "source_certificate"}:
            raise ValueError("invalid complete source case")
        if (
            type(row["n"]) is not int
            or row["n"] != n
            or row["source_path"] != source_path(n)
            or type(row["source_certificate"]) is not str
        ):
            raise ValueError("source case identity mismatch")
        if hashlib.sha256(row["source_certificate"].encode()).hexdigest() != SOURCE_SHA256[n]:
            raise ValueError("retained complete source differs from acquired certificate")
        result[n] = parse(row["source_certificate"], n)
    return result


def read_fact(n: int) -> legacy.Certificate:
    source_path(n)
    return read_facts()[n]


def to_witness(certificate: legacy.Certificate) -> dict[str, Any]:
    return kernel.to_witness(certificate, witness_prefix=PREFIX, claim_limitations=LIMITATIONS)


def run_case(certificate: legacy.Certificate, control: str) -> dict[str, Any]:
    return kernel.run_case(
        certificate, control, witness_prefix=PREFIX, claim_limitations=LIMITATIONS
    )


def validate_job(row: Any, certificate: legacy.Certificate, control: str) -> None:
    kernel.validate_job(row, certificate, control, witness_prefix=PREFIX)


def _stable(row: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value for key, value in row.items() if key not in {"cpu_seconds", "wall_seconds"}
    }


def check_certification(
    numbers: list[int] | None = None, *, replay: bool = False
) -> dict[int, Any]:
    selected = list(NUMBERS) if numbers is None else numbers
    if not selected or len(set(selected)) != len(selected):
        raise ValueError("empty or repeated confirmation selection")
    for n in selected:
        source_path(n)
    facts = read_facts()
    ensure_private(receipt_path())
    record = kernel.read_xz(receipt_path())
    if (
        type(record) is not dict
        or set(record) != {"format", "routes", "cases", "batch_wall_seconds"}
        or record["format"] != RECEIPT_FORMAT
        or record["routes"] != list(ROUTES)
    ):
        raise ValueError("invalid issue432 exact certification namespace")
    if type(record["cases"]) is not list or len(record["cases"]) != len(NUMBERS) * len(JOBS):
        raise ValueError("incomplete 75-job deciding receipt")
    elapsed = record["batch_wall_seconds"]
    if type(elapsed) not in (float, int) or elapsed < 0 or not float(elapsed) < float("inf"):
        raise ValueError("invalid actual batch wall measurement")
    result = {}
    for (n, control), row in zip(
        [(n, control) for n in NUMBERS for control in JOBS], record["cases"], strict=True
    ):
        validate_job(row, facts[n], control)
        if replay and n in selected and _stable(run_case(facts[n], control)) != _stable(row):
            raise ValueError("fresh native result differs from retained actual outcome")
        if control == "positive":
            result[n] = row
    return result


def confirmed_bound(n: int) -> dict[str, Any]:
    source_path(n)
    row = check_certification([n])[n]
    return {
        "value": legacy.ceiling_decimal(Fraction(row["checker_input"]["side"]), 16),
        "exact_form": row["checker_input"]["side"],
        "evidence": [EXACT_EVIDENCE],
    }


def run_child(job: tuple[int, str], directory: Path) -> dict[str, Any]:
    n, control = job
    path = directory / f"n{n}-{control}.json"
    command = [
        sys.executable,
        "-m",
        "devtools.ryxu_arrangement_reports",
        "decide-job",
        "--n",
        str(n),
        "--control",
        control,
        "--output",
        str(path),
    ]
    try:
        completed = subprocess.run(
            command, capture_output=True, timeout=JOB_TIMEOUT, check=False
        )
    except subprocess.TimeoutExpired as error:
        path.with_suffix(".stdout.log").write_bytes(error.stdout or b"")
        path.with_suffix(".stderr.log").write_bytes(error.stderr or b"")
        raise ValueError(f"n={n} {control}: child exceeded {JOB_TIMEOUT}s") from error
    path.with_suffix(".stdout.log").write_bytes(completed.stdout)
    path.with_suffix(".stderr.log").write_bytes(completed.stderr)
    path.with_suffix(".exit.json").write_bytes(
        canonical_json({"returncode": completed.returncode})
    )
    if completed.returncode != 0:
        raise ValueError(f"n={n} {control}: deciding child exited {completed.returncode}")
    return json.loads(path.read_text(), object_pairs_hook=unique_json_keys)


def certify(directory: Path, *, workers: int = 2) -> None:
    if type(workers) is not int or not 1 <= workers <= 3:
        raise ValueError("invalid bounded exact replay allocation")
    read_facts()
    directory.mkdir(parents=True, exist_ok=True)
    jobs = [(n, control) for n in NUMBERS for control in JOBS]
    started = time.monotonic()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(lambda job: run_child(job, directory), jobs))
    elapsed = time.monotonic() - started
    facts = read_facts()
    for (n, control), row in zip(jobs, rows, strict=True):
        validate_job(row, facts[n], control)
    save(
        receipt_path(),
        {
            "format": RECEIPT_FORMAT,
            "routes": list(ROUTES),
            "cases": rows,
            "batch_wall_seconds": elapsed,
        },
    )
    check_certification()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    acquisition = commands.add_parser("acquire")
    acquisition.add_argument("--source-dir", type=Path, required=True)
    certification = commands.add_parser("certify")
    certification.add_argument("--jobs-dir", type=Path, required=True)
    certification.add_argument("--workers", type=int, default=2)
    check = commands.add_parser("check")
    check.add_argument("--n", type=int, nargs="+")
    check.add_argument("--replay", action="store_true")
    child = commands.add_parser("decide-job")
    child.add_argument("--n", type=int, required=True)
    child.add_argument("--control", choices=JOBS, required=True)
    child.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "acquire":
        acquire(args.source_dir)
    elif args.command == "certify":
        certify(args.jobs_dir, workers=args.workers)
    elif args.command == "check":
        check_certification(args.n, replay=args.replay)
        print("issue432: 25 full positives and 50 complete-roster controls admitted")
    else:
        certificate = read_fact(args.n)
        row = run_case(certificate, args.control)
        validate_job(row, certificate, args.control)
        with atomic_output_file(args.output) as temporary:
            temporary.write_bytes(canonical_json(row))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
