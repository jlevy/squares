"""Run this repository's two maintained exact routes on the n = 204 certificate (T-231).

The routes are the ones ``devtools.upper_bound_reports certify`` runs for a packet row of
format ``evand-cert``: the row's bytes go through that module's ``evand_cert`` adapter
into the kernel ``devtools.evand_arrangement_reports``, whose ``run_case`` decides a job
on route ``exact_verify`` (``sqpack.witness.exact_verify`` on the centre-basis witness)
and route ``independent`` (``devtools.check_rational_witness_independent.check_squares``
on exact corners), and whose ``validate_job`` admits the row. Each job runs here in a
process of its own, as ``certify``'s child does, from a certificate file rather than from
a packet, since the packet is being built while this review runs.

``--job`` runs one job (``positive`` and the kernel's two gross controls); ``--sharp`` runs
the kernel's ``run_sharp`` at contact and ``1e-30`` past it, for both of its sharp
controls. This program decides nothing of its own: the verdicts are the routes'.

From ``packing/`` of the reference checkout, with the project interpreter::

    python -I maintained_routes_t231.py --packing . CERT --job positive --out ROW.json
    python -I maintained_routes_t231.py --packing . CERT --sharp --out SHARP.json
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

PROGRAM = Path(__file__).resolve()
WITNESS_PREFIX = "W-mishapolk-n204-n"
CLAIM_LIMITATIONS = (
    "Complete 12fc466 rational centre/half-angle certificate certificates/n204.cert in "
    "Evan Daniel's format, centres in [0, S]^2, decided by the stage 4 review lane from "
    "its own blobless clone at the pin. Finite construction feasibility only; no KKT, "
    "local minimum, rigidity, novelty, priority or global optimality claim."
)


def text_of(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--packing", type=Path, required=True)
    parser.add_argument("--job", choices=("positive", "duplicate-square-overlap", "square-translated-outside-container"))
    parser.add_argument("--sharp", action="store_true")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    packing = args.packing.resolve()
    sys.path.insert(0, str(packing))
    reports = importlib.import_module("devtools.upper_bound_reports")
    kernel = importlib.import_module("devtools.evand_arrangement_reports")
    raw = args.certificate.read_bytes()
    certificate = reports.evand_cert(raw, 204, {})
    profile = {"witness_prefix": WITNESS_PREFIX, "claim_limitations": CLAIM_LIMITATIONS}
    started = time.process_time()
    record: dict[str, Any] = {
        "program": PROGRAM.name,
        "program_sha256": hashlib.sha256(PROGRAM.read_bytes()).hexdigest(),
        "python": sys.version,
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "maintained_modules": {
            name: hashlib.sha256((packing / path).read_bytes()).hexdigest()
            for name, path in (
                ("devtools/upper_bound_reports.py", "devtools/upper_bound_reports.py"),
                ("devtools/evand_arrangement_reports.py", "devtools/evand_arrangement_reports.py"),
                ("devtools/evand_exact_certificates.py", "devtools/evand_exact_certificates.py"),
                (
                    "devtools/check_rational_witness_independent.py",
                    "devtools/check_rational_witness_independent.py",
                ),
                ("src/sqpack/witness.py", "src/sqpack/witness.py"),
                ("src/sqpack/verify.py", "src/sqpack/verify.py"),
            )
        },
    }
    if args.job is not None:
        row = kernel.run_case(certificate, args.job, **profile)
        try:
            kernel.validate_job(row, certificate, args.job, **profile)
        except kernel.ReportError as error:
            record["validate_job"] = f"refused: {error}"
        else:
            record["validate_job"] = "passed"
        record["job"] = args.job
        record["row"] = row
        record["summary"] = {
            route: {
                "passed": row[route]["verification_passed"],
                "pairs_tested": row[route]["pairs_tested"],
                "minimum_containment_clearance": row[route]["minimum_containment_clearance"],
                "minimum_best_pair_gap": row[route]["minimum_best_pair_gap"],
                "failures": len(row[route]["failures"]),
                "cpu_seconds": row["cpu_seconds"][route],
            }
            for route in kernel.ROUTES
        }
    if args.sharp:
        sharp: dict[str, Any] = {}
        for control in kernel.SHARP_CONTROLS:
            for past in (False, True):
                verdicts = kernel.run_sharp(certificate, control, past=past, **profile)
                sharp[f"{control}{'' if past else ' (at contact)'}"] = {
                    route: {
                        "passed": verdict["passed"],
                        "wall": text_of(verdict["wall"]),
                        "gap": text_of(verdict["gap"]),
                    }
                    for route, verdict in verdicts.items()
                }
        legacy = importlib.import_module("devtools.evand_exact_certificates")
        left, right, gap, direction = legacy.tightest_pair(certificate)
        record["tightest_pair"] = {
            "pair_0_based": [left, right],
            "gap": text_of(gap),
            "direction": [text_of(direction[0]), text_of(direction[1])],
        }
        record["top_clearance"] = text_of(legacy.top_clearance(certificate))
        record["sharp"] = sharp
    record["cpu_seconds"] = round(time.process_time() - started, 3)
    args.out.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    brief = record.get("summary") or record.get("sharp")
    sys.stdout.write(json.dumps({"job": args.job, "validate_job": record.get("validate_job"), "result": brief, "cpu_seconds": record["cpu_seconds"]}) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
