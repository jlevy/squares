"""The certificate's records, manifest and completion audit, read as data and cross-checked.

Usage::

    python3 -I check_linear_records.py CANDIDATE.json CERTIFICATE.json MANIFEST.json \\
        COMPLETION_AUDIT.json PROOF_BUNDLE.tar.gz RETAINED_CHECKER.cpp

Prints, as JSON: the 201 records (one per net angle, each replayed, with distinct input
digests and their node total), the manifest's and the certificate's net block against the
facts recomputed here, every digest the three documents state against the files they name
(the candidate, the certificate itself, the proof bundle and the retained checker), and
the source's own comparison fields. It decides no coverage.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import linear_exact as exact


def main(argv: list[str]) -> int:
    candidate_path, certificate_path, manifest_path = (
        Path(argv[1]),
        Path(argv[2]),
        Path(argv[3]),
    )
    audit_path, bundle_path, checker_path = Path(argv[4]), Path(argv[5]), Path(argv[6])
    candidate_bytes = candidate_path.read_bytes()
    certificate_bytes = certificate_path.read_bytes()
    candidate = exact.load_json(candidate_bytes)
    measure = exact.read_measure(candidate)
    digest = exact.semantic_digest(candidate)
    certificate = exact.load_json(certificate_bytes)
    manifest = exact.load_json(manifest_path.read_bytes())
    audit = exact.load_json(audit_path.read_bytes())
    checker = exact.sha256(checker_path.read_bytes())
    facts = exact.net_facts(measure.core, measure.step, measure.last + 1)
    results = certificate["results"]
    indices = sorted(int(key) for key in results)
    records = [results[str(index)] for index in indices]
    nodes = [int(record["nodes"]) for record in records]
    inputs = [record["input_sha256"] for record in records]

    def net_block_is_ours(block: dict[str, object]) -> bool:
        return all(
            Fraction(str(block[name])) == value
            for name, value in facts.items()
            if name in block
        )

    report = {
        "candidate_sha256": exact.sha256(candidate_bytes),
        "certificate_sha256": exact.sha256(certificate_bytes),
        "bundle_sha256": exact.sha256(bundle_path.read_bytes()),
        "retained_checker_sha256": checker,
        "semantic_digest": digest,
        "certificate": {
            "status": certificate["status"],
            "claim_fields_are_ours": (
                certificate["n"] == measure.n
                and Fraction(certificate["L"]) == measure.side
                and Fraction(certificate["B"]) == measure.core
                and Fraction(certificate["total_mass"]) == measure.total
                and Fraction(certificate["budget_gap"]) == exact.GAP
                and certificate["candidate_digest"] == digest
                and certificate["angle_count"] == measure.last + 1
            ),
            "net_block_is_ours": net_block_is_ours(certificate["net"]),
            "source_sha256_is_retained_checker": certificate["source_sha256"] == checker,
            "records": len(records),
            "indices_are_0_to_last_once": indices == list(range(measure.last + 1))
            and all(
                int(record["index"]) == index
                for index, record in zip(indices, records, strict=True)
            ),
            "statuses": sorted({str(record["status"]) for record in records}),
            "input_digests_distinct": len(set(inputs)) == len(inputs),
            "nodes_total": sum(nodes),
            "nodes_most": max(nodes),
            "nodes_most_at": indices[nodes.index(max(nodes))],
            "nodes_least": min(nodes),
            "nodes_least_at": indices[nodes.index(min(nodes))],
            "theorem": certificate.get("theorem"),
            "replay_scope": certificate.get("replay_scope"),
        },
        "manifest": {
            "claim_fields_are_ours": (
                manifest["n"] == measure.n
                and Fraction(manifest["L"]) == measure.side
                and Fraction(manifest["B"]) == measure.core
                and Fraction(manifest["mass"]) == measure.total
                and manifest["candidate_digest"] == digest
                and manifest["angle_count"] == measure.last + 1
            ),
            "net_block_is_ours": net_block_is_ours(manifest["net"]),
            "source_sha256_is_retained_checker": manifest["source_sha256"] == checker,
            "node_limit": manifest["node_limit"],
            "node_limit_exceeds_every_record": int(manifest["node_limit"]) > max(nodes),
            "workers": manifest.get("workers"),
        },
        "completion_audit": {
            "status": audit["status"],
            "claim_fields_are_ours": (
                audit["n"] == measure.n
                and Fraction(audit["L"]) == measure.side
                and Fraction(audit["total_mass"]) == measure.total
                and audit["candidate_digest"] == digest
                and audit["all_angles"] == measure.last + 1
            ),
            "certificate_sha256_is_certificate": audit["certificate_sha256"]
            == exact.sha256(certificate_bytes),
            "archive_sha256_is_bundle": audit["archive_sha256"]
            == exact.sha256(bundle_path.read_bytes()),
            "verifier_source_sha256_is_retained_checker": audit["verifier_source_sha256"]
            == checker,
            "side_minus_compared_with_equals_improvement_lower": measure.side
            - Fraction(audit["compared_with"])
            == Fraction(audit["improvement_lower"]),
            "compared_note": audit.get("compared_note"),
            "replay_scope": audit.get("replay_scope"),
        },
    }
    sys.stdout.write(json.dumps(report, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
