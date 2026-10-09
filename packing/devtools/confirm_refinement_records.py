"""Publish only the accepted finite-feasibility confirmation for #425/#428.

Run after public complete recovery and the independent custody review. This record
writer reconciles retained executions; it never runs a geometric decision.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from devtools import refinement_custody as custody
from devtools import refinement_house_links as houses
from devtools import refinement_packets as packets
from devtools.register_refinement_reports import (
    DAY,
    FRONTIER,
    RETRIEVED,
    append_rows,
    dump,
    report_id,
    save,
)
from sqpack.yamlio import safe_load

REVIEW = "docs/project/reviews/review-2026-10-07-refinement-custody-closure.md"


def adopt_case(n: int, existing: str, generated: str) -> str:
    """Reconstruct a selected confirmed finite ceiling from admitted source facts.

    Historical prose and source credits remain editorial inputs. Ordinary lower lanes
    come from the draft; the separate rigidity owner assesses the resulting witness.
    This adapter admits retained executions and runs no geometric predicate.
    """
    from devtools import render_case_verifiers  # noqa: PLC0415

    source = next((item for item in packets.SOURCES.values() if n in item.numbers), None)
    if source is None:
        return generated
    _, front, body = existing.split("---\n", 2)
    document = safe_load(front)
    case = document["packing"]
    if case["n"] != n or case["reported_upper_bound"]["source_key"] != source.key:
        return generated
    confirming = f"E-{source.packet_name}-exact-replay"
    if case["verified_upper_bound"]["evidence"] != [confirming]:
        raise ValueError("selected refinement lacks its complete confirming evidence")
    custody.check_index(custody.read_index())
    houses.check_houses([n])
    fact = packets.read_fact(source, n)
    value = packets.exact_decimal(fact["side"])
    case["reported_upper_bound"].update(
        value=value,
        exact_form=fact["side"],
        algebraic_degree=1,
        minimal_polynomial=None,
        analytically_optimized=None,
        catalogue_rigid="not-stated",
        construction_method="unknown",
        tilt_angles_deg=None,
        found_by=["Francisco Couzo"],
        found_year=2026,
        improved_by=["Seth Rehwaldt"],
        catalogue_pictured=False,
        source_key=source.key,
        source_date=DAY,
        retrieved_date=RETRIEVED,
        witnesses=[f"W-known-best-n{n:03d}"],
        evidence=[report_id(source)],
    )
    case["verified_upper_bound"] = {
        "value": value,
        "exact_form": fact["side"],
        "evidence": [confirming],
    }
    draft = safe_load(generated.split("---\n", 2)[1])["packing"]
    for field in ("reported_lower_bound", "verified_lower_bound", "reported_status", "status"):
        case[field] = draft[field]
    case["rigidity"] = None
    case["source_reviewed"] = RETRIEVED
    body, count = re.subn(
        r"(at exact side\s+)\$[0-9]+/[0-9]+\$(,\s+whose complete terminating decimal is\s+)"
        r"\$[0-9.]+\$",
        lambda match: f"{match[1]}${fact['side']}${match[2]}${value}$",
        body,
    )
    if count != 1:
        raise ValueError("selected refinement needs one exact side and decimal declaration")
    draft_body = generated.split("---\n", 2)[2]
    lower_pattern = r"\n## The lower bound\n.*?(?=\n<!-- BEGIN verification code)"
    lower = re.search(lower_pattern, draft_body, re.DOTALL)
    if lower is None:
        raise ValueError("historical draft has no generated lower-bound section")
    body, count = re.subn(lower_pattern, lambda _match: lower.group(), body, flags=re.DOTALL)
    if count != 1:
        raise ValueError("selected refinement needs one generated lower-bound section")
    rendered = "---\n" + dump(document) + "---\n" + body
    return render_case_verifiers.refresh(rendered)


def replace_row(path: Path, field: str, row: dict[str, Any]) -> None:
    text = path.read_text()
    pattern = rf"(?m)^  - id: {re.escape(row['id'])}\n.*?(?=^  - id:|\Z)"
    found = re.search(pattern, text, re.DOTALL)
    if found is None:
        raise ValueError(f"{field}: expected existing {row['id']}")
    rendered = "".join("  " + line for line in dump([row]).splitlines(keepends=True))
    save(path, text[: found.start()] + rendered + text[found.end() :])


def confirm(recovered: Path) -> None:
    review = (packets.REPO / REVIEW).read_text()
    if "admission are accepted" not in review or "**R2, closed:**" not in review:
        raise ValueError("independent public-custody acceptance is required")
    expected = dict(custody.read_index())
    del expected["file_manifest_sha256"]
    if custody.compact(recovered) != expected:
        raise ValueError("recovered complete replay differs from admitted actual jobs")
    custody.check_index(custody.read_index())
    houses.check_houses()

    verifier_rows = []
    for name, (_function, digest) in packets.N68_PROGRAMS.items():
        retained = packets.N68.packet / "source" / (name + ".txt")
        packets.save(
            retained, (recovered / "n68-upstream" / packets.N68.prefix / name).read_bytes()
        )
        verifier_rows.append(
            {
                "id": "V-rehwaldt-n68-" + name.removesuffix(".py").replace("_", "-"),
                "program": name,
                "author": "Seth Rehwaldt",
                "provenance": "external",
                "language": ["Python"],
                "methods": ["exact-algebraic"],
                "role": "decides",
                "source": [retained.relative_to(packets.REPO).as_posix()],
                "versions": [{"sha256": digest, "note": packets.N68.revision}],
                "summary": "Decides all 68 rational unit squares, containment and 2278 "
                "unordered pairs.",
                "note": (
                    "Producer code reproduced here with Python Fraction and the rational "
                    "half-angle "
                    "map. The two programs use the same SAT theorem and arithmetic; their "
                    "distinct "
                    "code does not establish independence from the source producer. "
                    "Analytic root "
                    "and dual programs are outside this replay."
                ),
            }
        )
    verifier_rows.append(
        {
            "id": "V-refinement-custody",
            "program": "devtools.refinement_custody",
            "author": "Squares Project (Levy)",
            "provenance": "first-party",
            "language": ["Python"],
            "methods": ["exact-algebraic"],
            "role": "premises",
            "source": [
                "packing/devtools/refinement_custody.py",
                "packing/devtools/refinement_packets.py",
                "packing/devtools/refinement_house_links.py",
            ],
            "summary": (
                "Admits all 13 complete actual input/result jobs, immutable source conversion, "
                "process outcomes, full control coverage and three complete house witnesses."
            ),
            "note": "Offline admission reconciles retained executions and runs no geometric "
            "predicate.",
        }
    )
    append_rows(FRONTIER / "verifiers.yaml", "verifiers", verifier_rows, "id")

    for source, result_id in ((packets.COUZO, "T-117"), (packets.N68, "T-118")):
        confirming = f"E-{source.packet_name}-exact-replay"
        is425 = source.issue == 425
        deciders = (
            ["V-sqpack-verify", "V-check-rational-witness-independent"]
            if is425
            else [row["id"] for row in verifier_rows[:2]]
        )
        entry = {
            "id": confirming,
            "claim": "upper-bound",
            "scope": {"n_values": list(source.numbers)},
            "assurance": "verified",
            "method": "exact-algebraic",
            "performed_by": "repository",
            "relationship_to_generator": "independent-implementation"
            if is425
            else "same-implementation",
            "origin": "replayed-here",
            "novelty": "previously-published",
            "source_key": source.key,
            "certificate": f"packing/resources/web/{source.packet_name}/facts/",
            "replay": (
                "Recover the complete public evidence with python -m "
                "devtools.refinement_custody "
                "recover --destination /Volumes/spud-ext1/agent-scratch/refinement-recovery. "
                + (
                    "The retained unchanged couzo_replay.py replay-batch --root host-v3 "
                    "--reviews coordinator-accepted-reviews.json --execute-reviewed-replay "
                    "completed all ten jobs after the explicitly reviewed host relocation. "
                    "A different host requires a separately reviewed runtime relocation."
                    if is425
                    else (
                        "The completed command was python -m devtools.refinement_packets "
                        "replay-n68 "
                        "--source-root n68-upstream --output source-geometry.json.gz; "
                        "all three complete jobs ran both pinned source programs."
                    )
                )
            ),
            "replay_status": "passed",
            "verifiers": [*deciders, "V-refinement-custody"],
            "independence_record": REVIEW,
            "limitations": (
                (
                    "Ten full jobs cover 397 positive squares and 239730 pairs per route "
                    "across "
                    "positives and four controls per case, 479460 total. Both routes share "
                    "Fraction, "
                    "SAT, schema/YAML and serialized corner inputs; reviewed independent "
                    "matrix "
                    "derivation addresses the common conversion. All children exit 0 "
                    "without timeout; "
                    "full batch wall 453.85665345803136s."
                    if is425
                    else (
                        "Three full jobs cover 68 squares and 2278 pairs per job/route, "
                        "13668 total "
                        "across both source programs. Both accept the positive and reject "
                        "duplicate and outside controls; wall 7.843s. This reproduces "
                        "producer implementations and does not claim independence from them."
                    )
                )
                + (
                    " Complete source/runtime/review/actual receipt custody was publicly "
                    "recovered "
                    "byte-identically and independently reviewed. Canonical admission "
                    "executes no new decider. No analytic contact limit, lower bound, "
                    "optimality, rigidity, novel arrangement, formal proof or human oversight "
                    "is established."
                )
            ),
            "external_review": {
                "state": "informally-verified",
                "date": DAY,
                "reviewed_by": "GPT-6 Astra separately prompted refinement custody review",
                "note": "The retained closure review accepts complete finite-feasibility "
                "replay and public custody only.",
            },
            "source_reviewed": DAY,
        }
        append_rows(FRONTIER / "evidence.yaml", "evidence", [entry], "id")
        rows = safe_load((FRONTIER / "results.yaml").read_text())["results"]
        result = next(row for row in rows if row["id"] == result_id)
        result.update(verification="V3", confirmation="C3")
        result["claim"] = (
            f"Complete exact replay confirms the finite rational upper-bound refinement at n = "
            f"{', '.join(map(str, source.numbers))}. Only finite feasibility enters; no "
            f"optimality claim is registered."
        )
        if confirming not in result["evidence"]:
            result["evidence"].append(confirming)
        result["next_rung"] = (
            "C4 requires two distinct accepted confirming adversarial reviews and an actual "
            "human oversight record; neither publication nor input admission supplies them."
        )
        result["controls"] = [
            custody.INDEX.relative_to(packets.REPO).as_posix(),
            "packing/tests/test_refinement_custody.py",
        ]
        result["reviews"] = [
            {
                "path": REVIEW,
                "kind": "adversarial",
                "reviewer": "GPT-6 Astra refinement custody reviewer",
                "reviewer_kind": "ai",
                "relation": "project",
                "date": DAY,
                "scope": "Complete finite rational geometry, actual deciding "
                "inputs/results, controls, public recovery and worker custody.",
                "verdict": "accepted",
                "covers": [result_id],
            }
        ]
        replace_row(FRONTIER / "results.yaml", "results", result)
        for n in source.numbers:
            path = FRONTIER / f"n-{n:03d}.md"
            prefix, front, body = path.read_text().split("---\n", 2)
            document = safe_load(front)
            case = document["packing"]
            fact = packets.read_fact(source, n)
            case["verified_upper_bound"] = {
                "value": packets.exact_decimal(fact["side"]),
                "exact_form": fact["side"],
                "evidence": [confirming],
            }
            if confirming not in case["evidence"]:
                case["evidence"].append(confirming)
            case["blockers"] = [
                block
                for block in case["blockers"]
                if report_id(source) not in block["evidence"]
            ]
            body = body.replace(
                "This is a reported feasible ceiling, with local replay admission and "
                "scoped review\n"
                "pending. The earlier verified ceiling remains in the verified lane.",
                "The complete finite witness is now exact-replayed here at V3/C3 after scoped\n"
                "review and public recovery of all original scientific evidence. Earlier\n"
                "ceilings and verification remain historical evidence for their own "
                "geometries.",
            )
            save(path, prefix + "---\n" + dump(document) + "---\n" + body)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--recovered-root", type=Path, required=True)
    args = parser.parse_args()
    confirm(args.recovered_root)


if __name__ == "__main__":
    main()
