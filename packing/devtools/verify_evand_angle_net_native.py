"""Decide evand's angle-net certificates by the native parent-core interval route.

evand/square-packing proves ``s(12) >= 15680/3951`` and ``s(21) >= 5000/1001`` with
weighted closed covers checked by its own Rust arrangement sweep, ``verify/``, over the
net ``theta_k = 2 arctan(k/N)``, ``N = 6000``. For bin ``k`` it tests the concentric
square of side ``sigma_k``, ``1/(cos d + sin d)`` for the bin's gap ``d`` rounded down
to a multiple of ``10^-6``, at ``theta_k``, over the centres where a unit square at some
angle of the bin fits. That is, row for row, this repository's adaptive parent-core
theorem (`sqpack.fractional.parent_core`) with parent side ``A = 1``: the row
``[k/N, (k+1)/N]`` of parent half-tangents, core half-tangent ``k/N`` and core side
``sigma_k``, minimum charge ``1``, and the point atoms as the source lists them.

So this reader builds that `ParentCoreCertificate` from the source's integer text file
(stored in the packet as deterministic gzip and read back as the upstream bytes by
`devtools.retained_data.read_retained_bytes`), without importing any source code, and
hands it to two separately reviewed pieces: `validate_parent_core`, which discharges the
exact premises (D4 invariance of the weighted points, the strict counting gap
``weight < n``, a contiguous half-tangent cover reaching ``tan(pi/8)``, and strict
containment of each core in every parent of its row), and `verify_parent_core_rows`, the
directed-rounding branch and bound over centre boxes that decides coverage. The coverage
decision shares nothing with the source's arrangement sweep, which is what makes a
complete pass a method-distinct confirmation.

The native theorem proves the strict ``s(n) > L``; the claim recorded is the source's
``s(n) >= L``.

The reader is not tied to one source or one net. ``s12-rescaled`` is squarepacker's
certificate of jlevy/squares#309, Daniel's ``s12`` file with every coordinate and the
container multiplied by ``7902/7901``, which its producer's checkers refuse at
``N = 6000`` and ``12000`` and accept at ``N = 24000``; its case therefore carries the net
``N = 24000``, and every row is the same construction at that net. ``s12-v11`` is
squarepacker's v1.1 certificate of jlevy/squares#363, Daniel's points dilated to the
container ``7943/2000`` with new weights, which its producer's checkers accept at
``N = 96000``, the net its case carries. ``s12-unnir`` is unnir's certificate of
jlevy/squares#924, 4,996 new points over the container ``9929/2500``, which its
producer's checkers accept at ``N = 96000`` with least captured weight exactly one at
bin ``39531``. ``--certificate`` and
``--certificate-sha256`` run a case's net and count on another file of the same format,
pinned by its digest on the command line, which is how a mutated control is decided.

Usage (from ``packing/``)::

    uv run --frozen --all-extras --group dev python -m devtools.verify_evand_angle_net_native \\
        --case s12 --pilot --output OUT.json
    ... --case s12 --all --workers 2 --output OUT.json
    ... --case s12-rescaled --rows 0 --certificate CONTROL.txt \\
        --certificate-sha256 HEX --output OUT.json

``--all`` writes an append-only row journal beside the receipt (``OUT.rows.jsonl``), and
``--resume JOURNAL`` skips the rows a previous journal of the same case and settings
already certified; a resumed receipt still requires every row certified before it says
``PASS_COMPLETE``.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import platform
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, TextIO

from strif import atomic_output_file

from devtools.retained_data import read_retained_bytes
from sqpack.fractional.model import Atom
from sqpack.fractional.parent_core import (
    ParentCoreCertificate,
    ParentCoreRow,
    validate_parent_core,
)
from sqpack.fractional.parent_core_interval import verify_parent_core_rows

REPO = Path(__file__).resolve().parents[2]
PACKET = REPO / "packing/resources/web/evand-square-packing-2026-09-26/square-packing/s12"
SOURCE_URL = "https://github.com/evand/square-packing"
SOURCE_COMMIT = "167d842cd27ba1451cb2833773ea930c80b9e65b"
RESCALED = (
    REPO / "packing/resources/web/squarepacker-s12-lower-bound-2026-10-02/s12-lower-bound"
)
V11 = REPO / "packing/resources/web/squarepacker-s12-lower-bound-2026-10-05/s12-lower-bound"
UNNIR = REPO / "packing/resources/web/unnir-s12-lower-bound-2026-11-08/s12-lower-bound-3.9716"
#: The source's net and its sigma rounding, as `verify/src/main.rs` `bin_geometry` has them.
NET = 6000
SIGMA_SCALE = 1_000_000
MAX_BYTES = 4 * 1024 * 1024


@dataclass(frozen=True, slots=True)
class Case:
    n: int
    path: Path
    sha256: str
    #: The source's recorded least captured weight and bin at the case's net.
    source_minimum: str
    source_bin: int
    net: int = NET
    source_url: str = SOURCE_URL
    source_commit: str = SOURCE_COMMIT


CASES = {
    "s12": Case(
        12,
        PACKET / "certificates/s12_lower_3.9686.txt",
        "75f1cc891a8b8739b92b50c7ddbd85a493efa58cf2e921d58ce4ac7c2dcabe78",
        "10000056/10000000",
        0,
    ),
    "s21": Case(
        21,
        PACKET / "certificates/s21/s21_lower_4.9950.txt",
        "c8e8f878205f2da9c213e4a87c06f17c5a759dce7e695e676dd5c50e0994f2ef",
        "10000083/10000000",
        684,
    ),
    "s12-rescaled": Case(
        12,
        RESCALED / "s12_lower_3.969118.txt",
        "6ad9b0e8257166687f4e861b97f024f4993d7b2125897173b2f5e9f6e2167578",
        "10000056/10000000",
        0,
        24000,
        "https://github.com/squarepacker/s12-lower-bound",
        "8c53049025b94bb589ed25a90203f0a34c2945e4",
    ),
    "s12-v11": Case(
        12,
        V11 / "s12_lower_3.9715.txt",
        "e2f326b28142cf22402f88357f4c7fe4680a08a32ae785b493adac335bcc2685",
        "10000050/10000000",
        0,
        96000,
        "https://github.com/squarepacker/s12-lower-bound",
        "7a96bec36bc6811c3715ef581598f22ff9b7ba3a",
    ),
    "s12-unnir": Case(
        12,
        UNNIR / "certificate/s12_lower_3.9716.txt",
        "833b76a179a420a40775cc76305ec9ffb7f6ea27472e587958c234c4c4712cbd",
        "9985226/9985226",
        39531,
        96000,
        "https://github.com/unnir/s12-lower-bound-3.9716",
        "064c2955670765321aaf1c0a2d5c778949daab6b",
    ),
}


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_source(path: Path, expected_sha256: str | None) -> tuple[bytes, list[int]]:
    """The reviewed bytes and their integers, refusing anything else."""
    data = read_retained_bytes(path)
    _require(len(data) <= MAX_BYTES, "certificate file exceeds 4 MiB")
    if expected_sha256 is not None:
        _require(
            hashlib.sha256(data).hexdigest() == expected_sha256,
            "certificate bytes differ from the reviewed evand release",
        )
    tokens = data.split()
    _require(
        all(t.isdigit() for t in tokens), "the text format holds nonnegative integers only"
    )
    return data, [int(t) for t in tokens]


def sigma(k: int, net: int = NET) -> Fraction:
    """``1/(cos d + sin d)`` for bin ``k``'s gap, rounded down to ``1/SIGMA_SCALE``."""
    c0, s0, g0 = net * net - k * k, 2 * k * net, net * net + k * k
    k1 = k + 1
    c1, s1, g1 = net * net - k1 * k1, 2 * k1 * net, net * net + k1 * k1
    cd, sd = c0 * c1 + s0 * s1, c0 * s1 - s0 * c1
    return Fraction((g0 * g1 * SIGMA_SCALE) // (cd + sd), SIGMA_SCALE)


def net_rows(net: int = NET) -> tuple[ParentCoreRow, ...]:
    """The bins ``[k/N, (k+1)/N]`` up to the first right end reaching ``tan(pi/8)``."""
    rows: list[ParentCoreRow] = []
    k = 0
    while True:
        right = Fraction(k + 1, net)
        rows.append(ParentCoreRow(Fraction(k, net), right, Fraction(k, net), sigma(k, net)))
        if right * right + 2 * right >= 1:
            return tuple(rows)
        k += 1


def parse_certificate(n: int, values: list[int], net: int = NET) -> ParentCoreCertificate:
    """Build the native certificate from the source's ``s_num s_den D W m (X Y w)^m``."""
    _require(len(values) >= 5, "truncated header")
    s_num, s_den, denominator, weight_scale, count = values[:5]
    _require(min(s_num, s_den, denominator, weight_scale, count) > 0, "nonpositive header")
    _require(len(values) == 5 + 3 * count, "point count does not match the file")
    side = Fraction(s_num, s_den)
    _require((side * denominator).denominator == 1, "container is off the coordinate grid")
    atoms: list[Atom] = []
    for index in range(count):
        x, y, w = values[5 + 3 * index : 8 + 3 * index]
        point = Fraction(x, denominator), Fraction(y, denominator)
        _require(point[0] <= side and point[1] <= side, f"point {index} outside the container")
        if w:
            atoms.append(Atom(str(index), *point, Fraction(w, weight_scale)))
    return ParentCoreCertificate(
        n, side, Fraction(1), Fraction(1), tuple(atoms), (), net_rows(net)
    )


def resolve_case(name: str, certificate: Path | None = None, sha256: str | None = None) -> Case:
    """The named case, or its net and count on another file pinned by ``sha256``."""
    case = CASES[name]
    if certificate is None:
        return case
    _require(sha256 is not None, "--certificate needs --certificate-sha256")
    return dataclasses.replace(case, path=certificate.resolve(), sha256=sha256)


def load_case(case: Case) -> ParentCoreCertificate:
    _, values = read_source(case.path, case.sha256)
    return parse_certificate(case.n, values, case.net)


def file_case(path: Path, n: int, net: int) -> str:
    """Register a certificate file in the source's format as a case of its own.

    For certificates derived from the source's, such as a rescaled or re-weighted s(12)
    file, decided over the net ``net``. The digest is the file's own, so a journal or
    receipt names exactly the bytes it decided; there is no recorded source minimum.
    """
    data, _ = read_source(path, None)
    name = f"file:{path.name}:{net}"
    CASES[name] = Case(n, path, hashlib.sha256(data).hexdigest(), "", -1, net)
    return name


def _shown(path: Path) -> str:
    return str(path.relative_to(REPO)) if path.is_relative_to(REPO) else str(path)


def _git(*arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments], cwd=REPO, check=True, capture_output=True, text=True
    ).stdout.strip()


def journal_certified(
    path: Path, name: str, case: Case, batch_size: int
) -> dict[int, dict[str, Any]]:
    """Rows a previous journal of this case and batch size recorded as certified."""
    lines = path.read_text(encoding="utf-8").splitlines()
    _require(bool(lines), "empty journal")
    head = json.loads(lines[0])
    _require(
        head.get("schema") == "EvandNativeRowJournal/v1"
        and head.get("case") == name
        and head.get("batch_size") == batch_size
        and head.get("certificate_sha256") == case.sha256,
        "journal is for another case, certificate or batch size",
    )
    certified: dict[int, dict[str, Any]] = {}
    for line in lines[1:]:
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue  # a torn last line from an interrupted run: that row is redone
        if row.get("status") == "certified" and not row.get("stalled"):
            certified[int(row["index"])] = row
    return certified


def run(
    name: str,
    case: Case,
    rows: tuple[int, ...] | None,
    *,
    batch_size: int,
    workers: int,
    journal: TextIO | None,
    resumed: dict[int, dict[str, Any]],
    source_state: tuple[str, bool],
) -> dict[str, Any]:
    started = time.monotonic()
    certificate = load_case(case)
    premises = validate_parent_core(certificate)
    catalogue = len(certificate.rows)
    selected = tuple(range(catalogue)) if rows is None else rows
    todo = tuple(index for index in selected if index not in resumed)
    provenance = {
        "git_commit": source_state[0],
        "dirty": source_state[1],
        "python": sys.version,
        "platform": platform.platform(),
        "command": sys.argv,
        "source_url": case.source_url,
        "source_commit": case.source_commit,
        "certificate": _shown(case.path),
        "certificate_sha256": case.sha256,
    }
    if journal is not None:
        header = {
            "schema": "EvandNativeRowJournal/v1",
            "case": name,
            "batch_size": batch_size,
            "certificate_sha256": case.sha256,
            "provenance": provenance,
            "resumed_rows": len(resumed),
        }
        journal.write(json.dumps(header) + "\n")
        for index in sorted(set(selected) & set(resumed)):
            journal.write(json.dumps(dict(resumed[index], resumed=True)) + "\n")
        journal.flush()
    outcomes: dict[int, dict[str, Any]] = {
        index: resumed[index] for index in selected if index in resumed
    }

    def progress(index: int, outcome: Any, elapsed: float) -> None:
        record = dict(asdict(outcome), index=index, seconds=elapsed)
        outcomes[index] = record
        if journal is not None:
            journal.write(json.dumps(record, default=str) + "\n")
            journal.flush()
        if outcome.status != "certified" or outcome.stalled or index % 100 == 0:
            print(
                f"row {index}: {outcome.status}, {outcome.boxes} boxes, "
                f"{outcome.stalled} stalled, {elapsed:.2f}s",
                flush=True,
            )

    threshold_units = scale = None
    refutations: list[Any] = []
    if todo:
        verdict = verify_parent_core_rows(
            certificate, todo, batch_size=batch_size, workers=workers, progress=progress
        )
        threshold_units, scale = verdict.threshold_units, verdict.scale
        refutations = [asdict(witness) for witness in verdict.refutations]
    records = [outcomes[index] for index in selected]
    covered = all(
        r["status"] == "certified"
        and not r["budget_exhausted"]
        and r["stalled"] == 0
        and r["lower"] is not None
        and (threshold_units is None or int(r["lower"]) >= threshold_units)
        for r in records
    )
    complete = sorted(selected) == list(range(catalogue))
    least = (
        min(records, key=lambda r: -1 if r["lower"] is None else int(r["lower"]))
        if records
        else None
    )
    return {
        "schema": "EvandNativeParentCoreReceipt/v1",
        "status": "PASS_COMPLETE"
        if covered and complete and not refutations
        else "PASS_PARTIAL"
        if covered and not refutations
        else "UNRESOLVED",
        "method": "directed-rounding box branch-and-bound over parent-core rows",
        "case": name,
        "provenance": provenance,
        "claim": f"s({case.n}) >= {certificate.outer_side}",
        "native_bound": f"s({case.n}) > {certificate.outer_side / certificate.parent_side}",
        "net": case.net,
        "sigma_scale": SIGMA_SCALE,
        "points": len(certificate.atoms),
        "budget": str(certificate.budget),
        "counting_gap": str(case.n * certificate.minimum_charge - certificate.budget),
        "premises": {
            "budget": str(premises.budget),
            "minimum_containment_numerator": str(premises.minimum_containment_numerator),
            "final_half_tangent": str(premises.final_half_tangent),
            "rows": premises.rows,
        },
        "catalogue_rows": catalogue,
        "selected_rows": len(selected),
        "resumed_rows": len(set(selected) & set(resumed)),
        "complete": complete,
        "batch_size": batch_size,
        "workers": workers,
        "scale": scale,
        "threshold_units": threshold_units,
        "boxes": sum(int(r["boxes"]) for r in records),
        "row_cpu_seconds": sum(float(r["seconds"]) for r in records),
        "least_lower": None
        if least is None
        else {"row": least["index"], "units": least["lower"]},
        "source_minimum": {"weight": case.source_minimum, "bin": case.source_bin},
        "refutations": refutations,
        "seconds": time.monotonic() - started,
        "rows": records if rows is not None and len(records) <= 64 else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--case",
        choices=sorted(CASES),
        help="a pinned case; without it, --certificate is a case of its own (--n, --net)",
    )
    select = parser.add_mutually_exclusive_group(required=True)
    select.add_argument("--rows", nargs="+", type=int)
    select.add_argument("--pilot", action="store_true", help="first, source-minimum, last row")
    select.add_argument("--premises", action="store_true", help="exact premises only")
    select.add_argument("--all", action="store_true")
    parser.add_argument("--batch-size", type=int, default=2048)
    parser.add_argument("--workers", type=int, choices=(1, 2), default=1)
    parser.add_argument("--resume", type=Path, help="a previous row journal of this case")
    parser.add_argument(
        "--certificate", type=Path, help="decide this file at the case's net, e.g. a control"
    )
    parser.add_argument(
        "--certificate-sha256", help="with --case, the digest --certificate must have"
    )
    parser.add_argument("--n", type=int, default=12, help="with --certificate and no --case")
    parser.add_argument("--net", type=int, default=NET, help="with --certificate and no --case")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.case is None:
        if args.certificate is None:
            parser.error("give --case, --certificate, or both")
        # A file decided as a case of its own, at the net it names, pinned by its own
        # digest; with --case, a file is decided at that case's net and pinned digest.
        args.case = file_case(args.certificate.resolve(), args.n, args.net)
        args.certificate = None
    source_state = _git("rev-parse", "HEAD"), bool(_git("status", "--porcelain"))
    case = resolve_case(args.case, args.certificate, args.certificate_sha256)
    if args.premises:
        certificate = load_case(case)
        premises = validate_parent_core(certificate)
        result: dict[str, Any] = {
            "schema": "EvandNativeParentCoreReceipt/v1",
            "status": "PREMISES_VERIFIED_COVERAGE_NOT_REQUESTED",
            "case": args.case,
            "certificate_sha256": case.sha256,
            "points": len(certificate.atoms),
            "premises": {k: str(v) for k, v in asdict(premises).items()},
        }
    else:
        rows: tuple[int, ...] | None
        if args.all:
            rows = None
        elif args.pilot:
            last = len(net_rows(case.net)) - 1
            rows = tuple(sorted({0, case.source_bin, last} - {-1}))
        else:
            rows = tuple(args.rows)
        resumed = (
            journal_certified(args.resume, args.case, case, args.batch_size)
            if args.resume
            else {}
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        journal_path = args.output.with_suffix(".rows.jsonl")
        with journal_path.open("x", encoding="utf-8") as journal:
            result = run(
                args.case,
                case,
                rows,
                batch_size=args.batch_size,
                workers=args.workers,
                journal=journal,
                resumed=resumed,
                source_state=source_state,
            )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(args.output) as handle:
        handle.write_text(json.dumps(result, indent=2, default=str) + "\n")
    print(f"{result['status']}: {args.output}")
    return 0 if result["status"] != "UNRESOLVED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
