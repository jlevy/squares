"""Read Guzhou0806's R052 certificate for s(17) into the native parent-core route.

R052 (``s(17) > 231001/50000``) is an adaptive parent-core certificate in
Kleddamag's mixed-certificate schema: rows ``[a, b, t, B]``, D4 point orbits and
two families of threshold groups, ``threshold_orbits`` (two of three) and
``generic_trigger_orbits`` (``k`` of ``m``). Every piece maps onto
`ParentCoreCertificate` without source code: a point orbit becomes point atoms,
and a group of weight ``w`` becomes a `ThresholdAtom` whose budget is
``w floor(m / k)``, which is the source's own budget rule.

The loader never imports the source's Python. Site indexing follows the
source's definition, each orbit's integer D4 images sorted and concatenated, so
group indices name the same physical points; the tests check that order.

Two decisions are separate here. `validate_parent_core` discharges every exact
premise except centre coverage: D4 invariance of the weighted charges, the
strict counting gap ``budget < 17 Gamma``, a contiguous folded angle cover, and
strict core containment throughout each row, including interior minima. The
coverage decision is the frozen interval engine's, and that engine refuses this
certificate at its static allocation ceilings before any box is searched. The
receipt records the refusal with the dimensions and ceilings that caused it; a
refusal is not evidence about the certificate.

``--sizing`` prices what lifting those ceilings would buy. It raises them in this
process only, runs the selected rows serially through the unchanged search, and
labels the receipt ``SIZING_ONLY_RAISED_CEILINGS``: timing and row outcomes for
planning, never a coverage decision, because the configuration it ran is not the
reviewed one.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import platform
import re
import subprocess
import sys
import time
from dataclasses import asdict
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

import sqpack.fractional.interval as interval_module
import sqpack.fractional.threshold_interval as threshold_module
from sqpack.fractional.interval import (
    BATCH,
    MAX_BATCH_SITES,
    MAX_INTERVAL_ATOMS,
    IntervalInputError,
)
from sqpack.fractional.model import Atom
from sqpack.fractional.parent_core import (
    ParentCoreCertificate,
    ParentCoreRow,
    validate_parent_core,
)
from sqpack.fractional.parent_core_interval import verify_parent_core_rows
from sqpack.fractional.threshold import ThresholdAtom
from sqpack.fractional.threshold_interval import (
    MAX_BATCH_MEMBER_SLOTS,
    MAX_MEMBER_SLOTS,
    ThresholdAtomData,
)

REPO = Path(__file__).resolve().parents[2]
PACKAGE = (
    REPO
    / "packing/resources/web/n17-guzhou-r052-2026-09-25/n17-square-packing/certificates/R052"
)
SOURCE = PACKAGE / "certificate/R052_CERTIFICATE.json.gz"
SOURCE_URL = "https://github.com/Guzhou0806/n17-square-packing"
SOURCE_COMMIT = "3bf1095c68a28fb9b2750fb0bc99edd5c22b7a61"
#: SHA-256 of the decompressed certificate, as `SOURCE_PIN.json` and `verify.py` pin it.
REVIEWED_SHA256 = "d77743eadf7f4bf9c424549a37a4296ea3b23fceee4af8e3d774a5a07e62e825"
N = 17
OUTER_SIDE = Fraction(4613, 1000)
PARENT_SIDE = Fraction(230650, 231001)
#: First row, the two rows at the ledger minimum, and the last row.
PILOT_ROWS = (0, 15555, 15556, 15720)
MAX_COMPRESSED = 16 * 1024 * 1024
MAX_DECOMPRESSED = 64 * 1024 * 1024
_RATIONAL = re.compile(r"-?[0-9]+(?:/[1-9][0-9]*)?")
_GENERIC_KEYS = frozenset({"groups", "k", "weight", "label", "kind"})


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _exact(value: object, field: str) -> Fraction:
    _require(
        type(value) is str and len(value) <= 1024 and _RATIONAL.fullmatch(value) is not None,
        f"{field} must be an exact rational string",
    )
    assert isinstance(value, str)
    return Fraction(value)


def _integer(value: object, field: str, *, positive: bool = False) -> int:
    _require(
        type(value) is int and value >= int(positive),
        f"{field} must be a {'positive' if positive else 'nonnegative'} integer",
    )
    assert isinstance(value, int)
    return value


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        _require(key not in result, f"duplicate JSON key {key}")
        result[key] = value
    return result


def read_certificate_bytes(path: Path) -> bytes:
    """The decompressed certificate, bounded before and after decompression."""
    with path.open("rb") as stream:
        data = stream.read(MAX_COMPRESSED + 1)
    _require(len(data) <= MAX_COMPRESSED, "certificate file exceeds 16 MiB")
    if data[:2] == b"\x1f\x8b":
        with gzip.GzipFile(fileobj=io.BytesIO(data)) as stream:
            data = stream.read(MAX_DECOMPRESSED + 1)
        _require(len(data) <= MAX_DECOMPRESSED, "decompressed certificate exceeds 64 MiB")
    return data


def physical_sites(raw: dict[str, Any], outer: int) -> tuple[list[tuple[int, int]], list[int]]:
    """Integer sites on the coordinate grid in the source's index order, with owners.

    Each orbit contributes its distinct D4 images sorted lexicographically, and the
    orbits follow file order; ``owners[i]`` is the orbit that produced site ``i``.
    """
    orbits = raw["point_orbits"]
    _require(isinstance(orbits, list) and bool(orbits), "point_orbits must be a nonempty array")
    sites: list[tuple[int, int]] = []
    owners: list[int] = []
    for index, row in enumerate(orbits):
        _require(
            isinstance(row, list) and len(row) == 3, f"point orbit {index} must be [x,y,w]"
        )
        x, y, _ = (_integer(value, f"point orbit {index}") for value in row)
        _require(x <= outer and y <= outer, f"point orbit {index} lies outside the container")
        images = sorted(
            {
                (a, b)
                for u, v in ((x, y), (y, x))
                for a in (u, outer - u)
                for b in (v, outer - v)
            }
        )
        sites.extend(images)
        owners.extend([index] * len(images))
    _require(len(sites) == len(set(sites)), "duplicate physical sites")
    return sites, owners


def _groups(
    raw: dict[str, Any],
) -> list[tuple[str, int, int, list[list[int]]]]:
    """Every threshold orbit as ``(family, k, weight, groups)``, schema-checked."""
    result: list[tuple[str, int, int, list[list[int]]]] = []
    triples = raw["threshold_orbits"]
    _require(isinstance(triples, list), "threshold_orbits must be an array")
    for index, orbit in enumerate(triples):
        _require(
            isinstance(orbit, dict) and set(orbit) == {"triples", "weight"},
            f"threshold orbit {index} must hold exactly triples and weight",
        )
        groups = orbit["triples"]
        _require(
            isinstance(groups, list)
            and bool(groups)
            and all(isinstance(g, list) and len(g) == 3 for g in groups),
            f"threshold orbit {index} must list triples",
        )
        result.append(("threshold", 2, _integer(orbit["weight"], "weight"), groups))
    generic = raw["generic_trigger_orbits"]
    _require(isinstance(generic, list), "generic_trigger_orbits must be an array")
    for index, orbit in enumerate(generic):
        _require(
            isinstance(orbit, dict)
            and {"groups", "k", "weight"} <= set(orbit) <= _GENERIC_KEYS
            and orbit.get("kind", "k_of_m") == "k_of_m",
            f"generic orbit {index} has an unknown schema",
        )
        groups = orbit["groups"]
        _require(
            isinstance(groups, list)
            and bool(groups)
            and all(isinstance(g, list) for g in groups),
            f"generic orbit {index} must list groups",
        )
        size = len(groups[0])
        k = _integer(orbit["k"], "k", positive=True)
        _require(
            all(len(g) == size for g in groups) and k <= size,
            f"generic orbit {index} is not a k-of-m family",
        )
        result.append(("generic", k, _integer(orbit["weight"], "weight"), groups))
    return result


def parse_r052(raw: dict[str, Any]) -> ParentCoreCertificate:
    """Build native charges from parsed R052 data; zero weights index but never charge."""
    side = _exact(raw["L"], "L")
    parent = _exact(raw["A"], "A")
    _require(side == OUTER_SIDE and parent == PARENT_SIDE, "not the R052 container and parent")
    _require(_exact(raw["bound"], "bound") == side / parent, "bound is not L/A")
    denominator = _integer(
        raw["coordinate_denominator"], "coordinate denominator", positive=True
    )
    weights = _integer(raw["weight_denominator"], "weight denominator", positive=True)
    scaled = side * denominator
    _require(scaled.denominator == 1, "container is not integral on the coordinate grid")
    sites, owners = physical_sites(raw, int(scaled))
    points = [(Fraction(x, denominator), Fraction(y, denominator)) for x, y in sites]
    atoms = tuple(
        Atom(f"{owner}:{site}", x, y, Fraction(raw["point_orbits"][owner][2], weights))
        for site, (owner, (x, y)) in enumerate(zip(owners, points, strict=True))
        if raw["point_orbits"][owner][2]
    )
    features: list[ThresholdAtom] = []
    for family, k, weight, groups in _groups(raw):
        seen: set[tuple[int, ...]] = set()
        for group in groups:
            _require(
                all(type(i) is int and 0 <= i < len(sites) for i in group),
                f"{family} group names an invalid site",
            )
            key = tuple(sorted(group))
            _require(len(key) == len(set(key)) and key not in seen, f"repeated {family} group")
            seen.add(key)
            if weight:
                features.append(
                    ThresholdAtom(tuple(points[i] for i in group), k, Fraction(weight, weights))
                )
    entries = raw["entries"]
    _require(isinstance(entries, list), "entries must be an array")
    rows: list[ParentCoreRow] = []
    for index, row in enumerate(entries):
        _require(isinstance(row, list) and len(row) == 4, f"row {index} must have four values")
        rows.append(ParentCoreRow(*(_exact(value, f"row {index}") for value in row)))
    certificate = ParentCoreCertificate(
        N,
        side,
        parent,
        Fraction(_integer(raw["minimum_units"], "minimum units", positive=True), weights),
        atoms,
        tuple(features),
        tuple(rows),
    )
    declared = Fraction(_integer(raw["budget_units"], "budget units"), weights)
    _require(certificate.budget == declared, "incorrect declared counting budget")
    return certificate


def load_r052(
    path: Path = SOURCE, *, expected_sha256: str | None = REVIEWED_SHA256
) -> tuple[ParentCoreCertificate, dict[str, Any]]:
    """The native certificate and the parsed source, bound to the reviewed bytes."""
    data = read_certificate_bytes(path)
    if expected_sha256 is not None:
        _require(
            hashlib.sha256(data).hexdigest() == expected_sha256,
            "certificate bytes differ from the reviewed R052 release",
        )
    raw = json.loads(data, object_pairs_hook=_unique_object)
    _require(isinstance(raw, dict), "certificate must be a JSON object")
    return parse_r052(raw), raw


def source_counts(raw: dict[str, Any]) -> dict[str, int]:
    """The resource inventory the source's README states, counted from the file."""
    groups = _groups(raw)
    return {
        "point_orbits": len(raw["point_orbits"]),
        "threshold_orbits": len(raw["threshold_orbits"]),
        "generic_orbits": len(raw["generic_trigger_orbits"]),
        "resource_columns": len(raw["point_orbits"]) + len(groups),
        "physical_points": len(
            physical_sites(raw, int(_exact(raw["L"], "L") * raw["coordinate_denominator"]))[0]
        ),
        "physical_threshold_groups": sum(len(g) for *_, g in groups),
        "angular_rows": len(raw["entries"]),
    }


def coverage_readiness(certificate: ParentCoreCertificate, batch_size: int) -> dict[str, Any]:
    """Dimensions against the frozen interval engine's ceilings, and its own verdict."""
    width = max((atom.token_count for atom in certificate.threshold_atoms), default=1)
    rows = len(certificate.atoms) + len(certificate.threshold_atoms)
    sites = {(atom.x, atom.y) for atom in certificate.atoms}
    for atom in certificate.threshold_atoms:
        sites.update(atom.points)
    report: dict[str, Any] = {
        "batch_size": batch_size,
        "point_atoms": len(certificate.atoms),
        "threshold_atoms": len(certificate.threshold_atoms),
        "atom_rows": rows,
        "distinct_sites": len(sites),
        "member_width": width,
        "member_slots": rows * width,
        "ragged_member_slots": len(certificate.atoms)
        + sum(atom.token_count for atom in certificate.threshold_atoms),
        "ceiling_atom_rows": min(MAX_BATCH_SITES, MAX_INTERVAL_ATOMS * BATCH // batch_size),
        "ceiling_distinct_sites": min(
            MAX_BATCH_SITES, MAX_INTERVAL_ATOMS * BATCH // batch_size
        ),
        "ceiling_member_slots": min(
            MAX_BATCH_MEMBER_SLOTS, MAX_MEMBER_SLOTS * BATCH // batch_size
        ),
    }
    try:
        ThresholdAtomData.of(certificate, batch_size=batch_size)
    except IntervalInputError as refusal:
        report.update(admitted=False, refusal=str(refusal))
    else:
        report.update(admitted=True, refusal=None)
    return report


#: In-process ceilings for a sizing run. They keep the 16 MiB site mask at batch 1024
#: (9,261 sites x 1024 boxes) and admit the padded member table. Not the reviewed
#: configuration: a sizing receipt is never a decision, whatever its rows report.
SIZING_CEILINGS = {
    "MAX_BATCH_SITES": 16384,
    "MAX_MEMBER_SLOTS": 16384,
    "MAX_BATCH_MEMBER_SLOTS": 65536,
}
SIZING_BATCH = 1024


def raise_ceilings_for_sizing() -> dict[str, dict[str, int]]:
    """Lift the frozen engine's allocation guards in this process only.

    Spawned workers re-import the frozen values, so a sizing run is serial.
    """
    changed: dict[str, dict[str, int]] = {}
    for module in (interval_module, threshold_module):
        for name, value in SIZING_CEILINGS.items():
            if hasattr(module, name):
                changed[f"{module.__name__}.{name}"] = {
                    "frozen": getattr(module, name),
                    "sizing": value,
                }
                setattr(module, name, value)
    return changed


def _git(*arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments], cwd=REPO, check=True, capture_output=True, text=True
    ).stdout.strip()


def run(
    path: Path,
    rows: tuple[int, ...] | None,
    *,
    coverage: bool,
    batch_size: int,
    workers: int,
    source_state: tuple[str, bool],
    sizing: bool = False,
) -> dict[str, Any]:
    """Exact premises always; coverage only when requested and admitted.

    A sizing run first records the frozen engine's refusal, then lifts its ceilings
    in-process and times the selected rows serially. Its status says so, and it
    never reports a complete or accepted decision.
    """
    _require(not sizing or (coverage and workers == 1), "a sizing run is serial coverage")
    started = time.monotonic()
    certificate, raw = load_r052(path)
    loaded = time.monotonic()
    premises = validate_parent_core(certificate)
    validated = time.monotonic()
    gap = N * certificate.minimum_charge - certificate.budget
    final = premises.final_half_tangent
    readiness = coverage_readiness(certificate, batch_size)
    raised: dict[str, dict[str, int]] | None = None
    if sizing:
        raised = raise_ceilings_for_sizing()
        try:
            ThresholdAtomData.of(certificate, batch_size=batch_size)
        except IntervalInputError as refusal:
            raise ValueError(f"sizing ceilings still refuse: {refusal}") from refusal
    receipt: dict[str, Any] = {
        "schema": "NativeParentCoreR052Receipt/v1",
        "provenance": {
            "git_commit": source_state[0],
            "dirty": source_state[1],
            "python": sys.version,
            "platform": platform.platform(),
            "command": sys.argv,
            "source_url": SOURCE_URL,
            "source_commit": SOURCE_COMMIT,
            "certificate_sha256": REVIEWED_SHA256,
        },
        "bound": str(certificate.outer_side / certificate.parent_side),
        "outer_side": str(certificate.outer_side),
        "parent_side": str(certificate.parent_side),
        "minimum_charge": str(certificate.minimum_charge),
        "budget": str(certificate.budget),
        "counting_gap": str(gap),
        "counting_gap_units": int(gap * raw["weight_denominator"]),
        "final_endpoint_excess": str(final * final + 2 * final - 1),
        "source_counts": source_counts(raw),
        "premises": {
            "budget": str(premises.budget),
            "minimum_containment_numerator": str(premises.minimum_containment_numerator),
            "final_half_tangent": str(final),
            "rows": premises.rows,
            "containment_quadratics": 4 * premises.rows,
        },
        "coverage_readiness": readiness,
        "sizing_raised_ceilings": raised,
        "timings": {"load": loaded - started, "premises": validated - loaded},
    }
    if not coverage:
        receipt["status"] = "PREMISES_VERIFIED_COVERAGE_NOT_REQUESTED"
    elif not readiness["admitted"] and not sizing:
        receipt["status"] = "PREMISES_VERIFIED_COVERAGE_REFUSED"
    else:
        verdict = verify_parent_core_rows(
            certificate, rows, batch_size=batch_size, workers=workers
        )
        receipt["status"] = (
            "SIZING_ONLY_RAISED_CEILINGS"
            if sizing
            else "PASS_COMPLETE"
            if verdict.accepted
            else "PASS_PARTIAL"
            if verdict.covered
            else "UNRESOLVED"
        )
        receipt["rows_covered"] = verdict.covered
        receipt["threshold_units"] = verdict.threshold_units
        receipt["rows"] = [
            dict(asdict(outcome), index=index, seconds=seconds)
            for index, outcome, seconds in zip(
                verdict.indices, verdict.directions, verdict.row_seconds, strict=True
            )
        ]
    receipt["seconds"] = time.monotonic() - started
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=SOURCE)
    select = parser.add_mutually_exclusive_group()
    select.add_argument("--rows", nargs="+", type=int)
    select.add_argument("--pilot", action="store_true")
    select.add_argument("--all", action="store_true")
    parser.add_argument("--batch-size", type=int)
    parser.add_argument("--workers", type=int, choices=(1, 2), default=1)
    parser.add_argument(
        "--sizing",
        action="store_true",
        help="time rows with the engine's ceilings lifted in-process; never a decision",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    coverage = bool(args.rows or args.pilot or args.all)
    rows = None if args.all else PILOT_ROWS if args.pilot else tuple(args.rows or ())
    batch_size = args.batch_size or (SIZING_BATCH if args.sizing else 2048)
    source_state = _git("rev-parse", "HEAD"), bool(_git("status", "--porcelain"))
    result = run(
        args.certificate,
        rows,
        coverage=coverage,
        batch_size=batch_size,
        workers=args.workers,
        source_state=source_state,
        sizing=args.sizing,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(args.output) as handle:
        handle.write_text(json.dumps(result, indent=2, default=str) + "\n")
    print(f"{result['status']}: {args.output}")
    return (
        0
        if result["status"]
        in (
            "PREMISES_VERIFIED_COVERAGE_NOT_REQUESTED",
            "PASS_COMPLETE",
            "PASS_PARTIAL",
            "SIZING_ONLY_RAISED_CEILINGS",
        )
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
