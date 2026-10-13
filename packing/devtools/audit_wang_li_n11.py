"""Compare the Wang and Li n11 certificate with Overbeck's, and refuse mutated copies of it.

Wang Ke and Li Can's certificate (Zenodo 23038546, retained in
``resources/web/wang-li-n11-2026-09-29/``) is Overbeck's ``global-certificate.json``
with thirteen threshold-charge orbit weights raised and the parent side ``A`` and every
row's core side ``B`` multiplied by one exact factor. ``diff`` derives that description
from the two files alone and checks the bound's arithmetic with exact fractions, and that
every premise the transfer theorem needs besides coverage is homogeneous in ``(A, B)``:
strict core containment, the parent-centre envelope and the angle cover.

``controls`` builds mutated certificates and runs each through source checkers in the
upstream interpreter, which has NumPy and Numba and none of this project's dependencies:
Overbeck's Python sweep (``exact_mixed.py``), the authors' separately written verifier
(``independent_scaled_fast.py``, which rebuilds the certificate from the source file, the
reweighting receipt and the factor, so its mutation is made there), and the BigInt
JavaScript sweep that Overbeck's ``prepare_secondary.py`` reconstructs. Every mutation
must be refused. `devtools.verify_n11_parent_core_native` runs the same mutations through
the native interval checker.

Usage, from ``packing/``::

    .venv/bin/python3 -m devtools.audit_wang_li_n11 diff --output OUT.json
    .venv/bin/python3 -m devtools.audit_wang_li_n11 scale-only --output CERT.json
    UPSTREAM/bin/python devtools/audit_wang_li_n11.py cliff --kleddamag-tree COPY \\
        --output OUT.json
    .venv/bin/python3 -m devtools.audit_wang_li_n11 controls --upstream-python PY \\
        --kleddamag-tree COPY --release-tree COPY --output OUT.json

The two trees are writable scratch copies: the source checkers write caches beside
themselves. The packet keeps the Zenodo archive zipped only, so the release tree is the
archive unzipped into scratch, and a path under `RELEASE` names the archive member at
that path.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib
import json
import os
import platform
import subprocess
import sys
import tempfile
import time
import zipfile
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
WEB = REPO / "packing/resources/web"
SOURCE = WEB / "external-square-certificates-2026-09-22/kleddamag-11/global-certificate.json"
PACKET = WEB / "wang-li-n11-2026-09-29"
#: Zenodo's archive, the bytes its published MD5 covers, kept in place of an extraction.
ARCHIVE = PACKET / "n11_wang_li_zenodo_release_2026-09-29_stage10_doi_23038546-1.zip"
#: The archive's top directory: a path under it names the member at that path.
RELEASE = PACKET / "n11_wang_li_zenodo_release_2026-09-29"
IMPROVED = RELEASE / "certificate/improved-global-certificate.json"
#: The bound, scaling factor and orbit changes the authors state, compared, not assumed.
STATED_BOUND = Fraction(3875000000, 999999999)
STATED_FACTOR = Fraction(999999999, 1000000000)
STATED_DELTAS = {
    3: 1, 27: 4, 43: 3, 51: 4384, 52: 7, 130: 34344, 131: 1,
    174: 3776, 206: 5, 207: 1, 218: 7, 232: 5, 259: 1,
}  # fmt: skip
#: Trump's 1979 packing of eleven unit squares fits a square of side 3.8770835900228...,
#: so no certificate may exclude side 3.877084.
KNOWN_PACKING_SIDE = Fraction(3877084, 1000000)
Certificate = dict[str, Any]


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key {key}")
        result[key] = value
    return result


def read_bytes(path: Path) -> bytes:
    """A file's bytes, or for a path under `RELEASE` the archive member it names."""
    if path.is_relative_to(RELEASE):
        with zipfile.ZipFile(ARCHIVE) as archive:
            return archive.read(path.relative_to(PACKET).as_posix())
    return path.read_bytes()


def load(path: Path) -> Certificate:
    """One certificate, refusing duplicate keys."""
    return json.loads(read_bytes(path), object_pairs_hook=_unique)


def text(value: Fraction) -> str:
    """A rational in the certificates' own string form."""
    return str(value.numerator) if value.denominator == 1 else str(value)


def _trig(t: Fraction) -> tuple[Fraction, Fraction]:
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def _orbit_size(x: int, y: int, span: int) -> int:
    return len({
        (a, b) for u, v in ((x, y), (y, x)) for a in (u, span - u) for b in (v, span - v)
    })  # fmt: skip


def budget_units(certificate: Certificate) -> int:
    """The counting budget, recomputed from point orbits and charge orbits."""
    span = int(Fraction(certificate["L"]) * certificate["coordinate_denominator"])
    total = sum(_orbit_size(x, y, span) * w for x, y, w in certificate["point_orbits"])
    for orbit in certificate["charge_orbits"]:
        size, threshold = len(orbit["sets"][0]), orbit["threshold"]
        total += len(orbit["sets"]) * (size // threshold) * orbit["weight"]
    return total


def row_premises(parent: Fraction, row: list[str]) -> tuple[Fraction, Fraction, bool]:
    """Overbeck's per-row premise quantities: strict core margin, centre margin, envelope.

    The margin is ``A - B max(cos d + |sin d|)`` over the interval ends, the centre margin
    ``r = A min(cos u + sin u)/2``, and the envelope ``B (cos t + sin t)/2 <= r < L/2`` is
    checked by the caller against ``L``.
    """
    a, b, t, core = map(Fraction, row)
    cosine, sine = _trig(t)
    widths, reaches = [], []
    for u in (a, b):
        cu, su = _trig(u)
        dot, cross = cosine * cu + sine * su, abs(cosine * su - sine * cu)
        require(dot > 0 and dot >= cross, "relative angle outside [-pi/4, pi/4]")
        widths.append(dot + cross)
        reaches.append(cu + su)
    radius = parent * min(reaches) / 2
    return parent - core * max(widths), radius, core * (cosine + sine) / 2 <= radius


def diff(source: Certificate, improved: Certificate) -> dict[str, Any]:
    """Every difference between the two certificates, and the exact arithmetic of the bound."""
    keys = sorted(set(source) | set(improved))
    changed_keys = [key for key in keys if source.get(key) != improved.get(key)]
    require(source["point_orbits"] == improved["point_orbits"], "point orbits differ")
    require(
        len(source["charge_orbits"]) == len(improved["charge_orbits"]), "orbit count differs"
    )
    orbits: list[dict[str, Any]] = []
    for index, (old, new) in enumerate(
        zip(source["charge_orbits"], improved["charge_orbits"], strict=True)
    ):
        if old == new:
            continue
        require(
            {**old, "weight": new["weight"]} == new, f"orbit {index} differs beyond its weight"
        )
        size, threshold = len(old["sets"][0]), old["threshold"]
        delta = new["weight"] - old["weight"]
        orbits.append({
            "orbit": index,
            "feature": f"{threshold}-of-{size}",
            "features_in_orbit": len(old["sets"]),
            "budget_multiplier": len(old["sets"]) * (size // threshold),
            "weight_before": old["weight"],
            "weight_after": new["weight"],
            "delta": delta,
            "budget_delta": len(old["sets"]) * (size // threshold) * delta,
        })  # fmt: skip
    deltas = {orbit["orbit"]: orbit["delta"] for orbit in orbits}
    side = Fraction(source["L"])
    require(Fraction(improved["L"]) == side, "container side differs")
    parent, parent_after = Fraction(source["A"]), Fraction(improved["A"])
    factor = parent_after / parent
    require(len(source["entries"]) == len(improved["entries"]), "row count differs")
    margins: list[Fraction] = []
    margins_after: list[Fraction] = []
    for index, (old, new) in enumerate(
        zip(source["entries"], improved["entries"], strict=True)
    ):
        require(old[:3] == new[:3], f"row {index}: interval or core angle differs")
        core, core_after = Fraction(old[3]), Fraction(new[3])
        require(core_after == core * factor, f"row {index}: core side not scaled by A'/A")
        margin, radius, envelope = row_premises(parent, old)
        margin_after, radius_after, envelope_after = row_premises(parent_after, new)
        require(margin_after == margin * factor, f"row {index}: margin is not homogeneous")
        require(radius_after == radius * factor, f"row {index}: centre margin not homogeneous")
        require(margin_after > 0 and envelope and envelope_after, f"row {index}: premise fails")
        require(0 < radius_after < side / 2, f"row {index}: empty centre domain")
        margins.append(margin)
        margins_after.append(margin_after)
    final = Fraction(source["entries"][-1][1])
    budget, budget_after = budget_units(source), budget_units(improved)
    require(budget == source["budget_units"], "source budget disagrees")
    require(budget_after == improved["budget_units"], "improved budget disagrees")
    require(
        budget_after - budget == sum(orbit["budget_delta"] for orbit in orbits),
        "budget change is not the orbit changes",
    )
    gamma, gamma_after = source["minimum_units"], improved["minimum_units"]
    bound, bound_after = side / parent, side / parent_after
    require(Fraction(source["bound"]) == bound, "source declares another bound")
    require(Fraction(improved["bound"]) == bound_after, "improved declares another bound")
    return {
        "schema": "WangLiN11CertificateDiff/v1",
        "source": str(SOURCE.relative_to(REPO)),
        "improved": str(IMPROVED.relative_to(REPO)),
        "top_level_keys": keys,
        "changed_keys": changed_keys,
        "point_orbits_identical": True,
        "charge_orbits": len(source["charge_orbits"]),
        "changed_orbits": orbits,
        "changed_orbits_match_stated": deltas == STATED_DELTAS,
        "rows": len(source["entries"]),
        "row_intervals_and_core_angles_identical": True,
        "container_side": text(side),
        "parent_side_before": text(parent),
        "parent_side_after": text(parent_after),
        "factor": text(factor),
        "factor_matches_stated": factor == STATED_FACTOR,
        "every_core_side_scaled_by_factor": True,
        "budget_units_before": budget,
        "budget_units_after": budget_after,
        "minimum_units_before": gamma,
        "minimum_units_after": gamma_after,
        "surplus_units_before": 11 * gamma - budget,
        "surplus_units_after": 11 * gamma_after - budget_after,
        "declared_bound_before": source["bound"],
        "declared_bound_after": improved["bound"],
        "bound_before": text(bound),
        "bound_after": text(bound_after),
        "bound_after_matches_stated": bound_after == STATED_BOUND,
        "bound_after_equals_bound_before_over_factor": bound_after == bound / factor,
        "improvement": text(bound_after - bound),
        "improvement_decimal": f"{float(bound_after - bound):.6e}",
        "bound_after_decimal_30": _decimal(bound_after, 30),
        "premises": {
            "strict_core_margin_before": text(min(margins)),
            "strict_core_margin_after": text(min(margins_after)),
            "every_margin_and_centre_margin_scaled_by_factor": True,
            "envelope_holds_every_row_after": True,
            "final_half_tangent": text(final),
            "angle_cover_reaches_pi_over_4": final * final + 2 * final > 1,
        },
    }


def _decimal(value: Fraction, digits: int) -> str:
    whole, rest = divmod(value.numerator, value.denominator)
    return f"{whole}.{rest * 10**digits // value.denominator:0{digits}d}"


def _scale(certificate: Certificate, factor: Fraction) -> Certificate:
    mutated = copy.deepcopy(certificate)
    mutated["A"] = text(Fraction(certificate["A"]) * factor)
    for row in mutated["entries"]:
        row[3] = text(Fraction(row[3]) * factor)
    return mutated


def scale_only(source: Certificate, improved: Certificate) -> Certificate:
    """Overbeck's weights, budget and Gamma at the improved parent and core sides.

    A complete sweep of this certificate decides whether the reweighting is needed for
    the improved bound or only raises the counting surplus.
    """
    derived = _scale(source, Fraction(improved["A"]) / Fraction(source["A"]))
    require(derived["A"] == improved["A"], "scaled parent side differs")
    require(derived["entries"] == improved["entries"], "scaled rows differ")
    return {**derived, "bound": improved["bound"]}


def _gamma_plus_one(improved: Certificate, _source: Certificate) -> Certificate:
    return {**improved, "minimum_units": improved["minimum_units"] + 1}


def _gap_closed(improved: Certificate, _source: Certificate) -> Certificate:
    return {**improved, "minimum_units": improved["budget_units"] // 11}


def _orbit_130_reverted(improved: Certificate, source: Certificate) -> Certificate:
    mutated = copy.deepcopy(improved)
    mutated["charge_orbits"][130]["weight"] = source["charge_orbits"][130]["weight"]
    mutated["budget_units"] = budget_units(mutated)
    return mutated


def _one_step_further(improved: Certificate, source: Certificate) -> Certificate:
    factor = Fraction(improved["A"]) / Fraction(source["A"])
    return _scale(improved, (2 * factor - 1) / factor)


def _past_known_packing(improved: Certificate, _source: Certificate) -> Certificate:
    exact = Fraction(improved["L"]) / KNOWN_PACKING_SIDE / Fraction(improved["A"])
    return _scale(improved, Fraction(int(exact * 10**6), 10**6))


#: name -> (what changes, how a sound checker refuses it, rows that show it, builder).
MUTATIONS: dict[
    str, tuple[str, str, tuple[int, ...], Callable[[Certificate, Certificate], Certificate]]
] = {
    "gamma_plus_one": (
        "minimum charge Gamma raised by one unit (1e-9); budget unchanged",
        "coverage: every row's minimum is exactly Gamma",
        (0,),
        _gamma_plus_one,
    ),
    "counting_gap_closed": (
        "Gamma lowered to floor(M/11), so 11 Gamma <= M",
        "counting: no strict gap",
        (0,),
        _gap_closed,
    ),
    "orbit_130_reverted": (
        "orbit 130 (the largest change, +34344) back to its source weight, budget recomputed",
        "coverage: row 8844 falls below Gamma",
        (8844,),
        _orbit_130_reverted,
    ),
    "scaled_one_step_further": (
        "A and every B scaled by 1 - 2e-9 from the source instead of 1 - 1e-9",
        "coverage: row 615 opens a cell below Gamma",
        (615,),
        _one_step_further,
    ),
    "scaled_past_known_packing": (
        "A and every B scaled further until L/A exceeds 3.877084, a side Trump's packing fits",
        "coverage: a certificate for that bound would contradict a known packing",
        (0,),
        _past_known_packing,
    ),
}


# --- Upstream probes: run only under the upstream interpreter. --------------------------


def _probe_source_sweep(
    tree: Path, mutated: Certificate, rows: tuple[int, ...]
) -> dict[str, Any]:
    """Overbeck's ``exact_mixed.py``: premises, then each row's exact minimum."""
    if str(tree) not in sys.path:
        sys.path.insert(0, str(tree))
    source = importlib.import_module("exact_mixed")
    try:
        data, jobs, _ = source.validate(mutated)
    except ValueError as error:
        return {"refused": True, "by": "premises", "error": str(error)}
    minima = {
        str(row): int(source.accumulate(*source.geometry(*data, *jobs[row]))[0]) for row in rows
    }
    below = {row: z for row, z in minima.items() if z < mutated["minimum_units"]}
    return {"refused": bool(below), "by": "coverage" if below else None, "row_minima": minima}


def _probe_independent(
    tree: Path, improved: Certificate, mutated: Certificate, rows: tuple[int, ...]
) -> dict[str, Any]:
    """The authors' ``independent_scaled_fast.row_min_fast`` on a rebuilt mutation.

    The verifier never reads the improved file: it rebuilds the certificate at import
    from the source file, the receipt's weight deltas and the factor, and compares each
    row with a hard-coded target. The probe replaces that rebuilt certificate by the
    mutation and applies the release's own acceptance rule: every row at the target
    and ``11 * target > budget``.
    """
    verifier_dir = str(tree / "verifier/independent")
    if verifier_dir not in sys.path:
        sys.path.insert(0, verifier_dir)
    fast: Any = importlib.import_module("independent_scaled_fast")
    core: Any = importlib.import_module("independent_core")
    # The rebuilt copy keeps the source's declared bound, budget and Gamma; it reads none.
    declared = ("bound", "budget_units", "minimum_units")
    require(
        {k: v for k, v in fast.mod.items() if k not in declared}
        == {k: v for k, v in improved.items() if k not in declared},
        "the verifier's rebuilt certificate is not the improved file",
    )
    target = fast.TARGET
    if {k: v for k, v in mutated.items() if k not in declared} == {
        k: v for k, v in improved.items() if k not in declared
    }:
        return {
            "applicable": False,
            "reason": "the mutation changes only declared fields this verifier never reads; "
            f"it compares every row with its hard-coded target {target}",
        }
    fast.mod = mutated
    fast.pts, fast.pw, fast.signed, fast.budget, fast.D = core.expand_positive_and_signed(
        mutated
    )
    try:
        minima = {str(row): int(fast.row_min_fast(row)) for row in rows}
    finally:
        fast.mod = improved
        fast.pts, fast.pw, fast.signed, fast.budget, fast.D = core.expand_positive_and_signed(
            improved
        )
    below = {row: z for row, z in minima.items() if z != target}
    counting = 11 * target <= budget_units(mutated)
    return {
        "refused": bool(below) or counting,
        "by": "coverage" if below else "counting" if counting else None,
        "target_units": target,
        "row_minima": minima,
        "reads_minimum_units_from_certificate": False,
    }


def _probe_bigint(tree: Path, mutated: Certificate, rows: tuple[int, ...]) -> dict[str, Any]:
    """The reconstructed JavaScript sweep, one row range per row, on the mutated file."""
    if str(tree) not in sys.path:
        sys.path.insert(0, str(tree))
    script = importlib.import_module("prepare_secondary").ensure_secondary()
    results: dict[str, Any] = {}
    with tempfile.TemporaryDirectory(prefix="wang-li-control-") as scratch:
        path = Path(scratch) / "certificate.json"
        raw = json.dumps(mutated).encode()
        path.write_bytes(raw)
        # The script's interface requires the digest of the file it reads.
        digest = hashlib.sha256(raw).hexdigest()
        for row in rows:
            completed = subprocess.run(
                [
                    "node", str(script), "--certificate", str(path), "--expected-sha", digest,
                    "--A", mutated["A"], "--start", str(row), "--stop", str(row + 1),
                ],
                capture_output=True, text=True, check=False, timeout=600,
            )  # fmt: skip
            try:
                parsed = json.loads(completed.stdout)
                results[str(row)] = {
                    "exit": completed.returncode,
                    "status": parsed["status"],
                    "minimum_units": parsed["minimum_units"],
                    "budget_units": parsed["budget_units"],
                }
            except json.JSONDecodeError, KeyError:
                results[str(row)] = {
                    "exit": completed.returncode,
                    "error": completed.stderr.strip().splitlines()[-1:],
                }
    refused = any(result["exit"] != 0 for result in results.values())
    counting = 11 * mutated["minimum_units"] <= mutated["budget_units"]
    return {
        "refused": refused or counting,
        "by": "coverage" if refused else "counting (orchestrator)" if counting else None,
        "rows": results,
    }


def probe(kleddamag: Path, release: Path) -> dict[str, Any]:
    """Every mutation through the three source checkers; runs in the upstream interpreter."""
    sys.dont_write_bytecode = True
    source, improved = load(SOURCE), load(IMPROVED)
    results: dict[str, Any] = {}
    for name, (description, expected, rows, build) in MUTATIONS.items():
        mutated = build(improved, source)
        started = time.monotonic()
        checks = {
            "kleddamag_exact_mixed": _probe_source_sweep(kleddamag, mutated, rows),
            "authors_independent": _probe_independent(release, improved, mutated, rows),
            "kleddamag_bigint_javascript": _probe_bigint(kleddamag, mutated, rows),
        }
        results[name] = {
            "description": description,
            "expected_refusal": expected,
            "bound": text(Fraction(mutated["L"]) / Fraction(mutated["A"])),
            "minimum_units": mutated["minimum_units"],
            "budget_units": mutated["budget_units"],
            "rows": list(rows),
            "checks": checks,
            "refused_by_every_applicable_checker": all(
                check["refused"] for check in checks.values() if check.get("applicable", True)
            ),
            "seconds": time.monotonic() - started,
        }
    versions = importlib.import_module("importlib.metadata").version
    return {
        "mutations": results,
        "runtime": {
            "python": sys.version,
            "platform": platform.platform(),
            "packages": {name: versions(name) for name in ("numpy", "numba", "llvmlite")},
            "node": subprocess.run(
                ["node", "--version"], capture_output=True, text=True, check=True
            ).stdout.strip(),
        },
    }


#: The rows the preprint names for its failing control, lambda = 1 - 2e-7.
CLIFF_ROWS = (*range(543, 575), *range(615, 627))


def cliff(tree: Path, steps: tuple[int, ...], rows: tuple[int, ...]) -> dict[str, Any]:
    """The improved weights at ``lambda = 1 - k * 1e-9`` for each ``k``: rows below Gamma.

    Runs Overbeck's ``exact_mixed.py`` in the upstream interpreter. ``k = 1`` is the
    certificate itself.
    """
    sys.dont_write_bytecode = True
    source, improved = load(SOURCE), load(IMPROVED)
    factor = Fraction(improved["A"]) / Fraction(source["A"])
    results: dict[str, Any] = {}
    for step in steps:
        started = time.monotonic()
        mutated = _scale(improved, (1 - Fraction(step, 10**9)) / factor)
        require(step != 1 or mutated == improved, "k = 1 must be the certificate itself")
        checked = _probe_source_sweep(tree, mutated, rows)
        minima = checked.get("row_minima", {})
        results[str(step)] = {
            "factor": text(Fraction(mutated["A"]) / Fraction(source["A"])),
            "bound": text(Fraction(mutated["L"]) / Fraction(mutated["A"])),
            "rows_below_gamma": sorted(
                int(row) for row, z in minima.items() if z < improved["minimum_units"]
            ),
            "least_minimum": min(minima.values()) if minima else None,
            "refused_by": checked["by"],
            "seconds": time.monotonic() - started,
        }
    return {
        "schema": "WangLiN11ScalingCliff/v1",
        "improved": str(IMPROVED.relative_to(REPO)),
        "gamma": improved["minimum_units"],
        "rows": list(rows),
        "steps": results,
        "python": sys.version,
    }


def _run_probe(
    args: argparse.Namespace, environment: dict[str, str]
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            str(args.upstream_python), str(Path(__file__).resolve()), "probe",
            "--kleddamag-tree", str(args.kleddamag_tree.resolve()),
            "--release-tree", str(args.release_tree.resolve()),
        ],
        capture_output=True, text=True, check=True, env=environment, timeout=3600,
    )  # fmt: skip


def _write(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".partial")
    temporary.write_text(json.dumps(document, indent=2) + "\n")
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    diffing = commands.add_parser("diff", help="derive and check the certificate change")
    diffing.add_argument("--output", type=Path, required=True)
    controlling = commands.add_parser("controls", help="refuse mutated certificates")
    controlling.add_argument("--upstream-python", type=Path, required=True)
    controlling.add_argument("--kleddamag-tree", type=Path, required=True)
    controlling.add_argument("--release-tree", type=Path, required=True)
    controlling.add_argument("--output", type=Path, required=True)
    deriving = commands.add_parser("scale-only", help="write the unreweighted scaled copy")
    deriving.add_argument("--output", type=Path, required=True)
    edging = commands.add_parser("cliff", help="upstream interpreter: scale further")
    edging.add_argument("--kleddamag-tree", type=Path, required=True)
    edging.add_argument("--steps", type=int, nargs="+", default=[1, 2, 200])
    edging.add_argument("--output", type=Path, required=True)
    probing = commands.add_parser("probe", help=argparse.SUPPRESS)
    probing.add_argument("--kleddamag-tree", type=Path, required=True)
    probing.add_argument("--release-tree", type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    if args.command == "probe":
        print(json.dumps(probe(args.kleddamag_tree.resolve(), args.release_tree.resolve())))
        return 0
    if args.command == "cliff":
        result = cliff(args.kleddamag_tree.resolve(), tuple(args.steps), CLIFF_ROWS)
        result["seconds"] = time.monotonic() - started
        _write(args.output, result)
        print(json.dumps({k: v["rows_below_gamma"] for k, v in result["steps"].items()}))
        return 0
    if args.command == "scale-only":
        _write(args.output, scale_only(load(SOURCE), load(IMPROVED)))
        return 0
    if args.command == "diff":
        result = diff(load(SOURCE), load(IMPROVED))
        result["seconds"] = time.monotonic() - started
        _write(args.output, result)
        print(json.dumps({k: v for k, v in result.items() if k != "changed_orbits"}, indent=2))
        return 0
    with tempfile.TemporaryDirectory(prefix="wang-li-numba-") as cache:
        environment = dict(
            os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", NUMBA_CACHE_DIR=cache
        )
        completed = _run_probe(args, environment)
    probes = json.loads(completed.stdout)
    refused = all(
        m["refused_by_every_applicable_checker"] for m in probes["mutations"].values()
    )
    result = {
        "schema": "WangLiN11MutationControls/v1",
        "status": "PASS_EVERY_MUTATION_REFUSED" if refused else "FAIL_A_MUTATION_WAS_ACCEPTED",
        "improved": str(IMPROVED.relative_to(REPO)),
        **probes,
        "probe_stderr": completed.stderr,
        "seconds": time.monotonic() - started,
    }
    _write(args.output, result)
    print(json.dumps({"status": result["status"], "seconds": result["seconds"]}, indent=2))
    return 0 if refused else 1


if __name__ == "__main__":
    raise SystemExit(main())
