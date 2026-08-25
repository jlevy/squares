#!/usr/bin/env python3
"""Behavior checks for the frontier assurance contract."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from cases.gobel5.verify_exact import verify as verify_gobel5
from cases.gobel10.verify_exact import verify as verify_gobel10
from devtools.check_basic_bounds import check_case_basic_bounds, verify_grid
from devtools.migrate_frontier_v2 import apply_assurance_audits, migrate_case
from devtools.render_research_tables import compact_bound, same_bound
from sqpack.assurance import (
    check_case_semantics,
    check_evidence_semantics,
    check_experiment_semantics,
)


def numerical_evidence() -> dict[str, object]:
    """Return one complete multiprecision numerical check."""
    return {
        "id": "E-n029-numerical",
        "claim": "witness-feasibility",
        "scope": {"n_values": [29]},
        "assurance": "numerically-checked",
        "method": "numerical-multiprecision",
        "performed_by": "repository",
        "relationship_to_generator": "independent-implementation",
        "source_key": "[Kingbird n=29 SVG]",
        "precision": {"decimal_digits": 160, "rounding": "nearest"},
        "tolerance": "1e-80",
        "replay": (
            "uv run --frozen python -m cases.kingbird29.verify_svg "
            "resources/papers/kingbird-square-29-provenance.svg"
        ),
        "replay_status": "passed",
        "limitations": "Does not certify exact feasibility or optimality.",
        "blocker": {"kind": "mathematics", "detail": "No formal existence certificate."},
        "source_reviewed": "2026-08-24",
    }


def verified_evidence() -> dict[str, object]:
    """Return one complete exact-algebraic replay record."""
    return {
        "id": "E-grid-exact",
        "claim": "exact-value",
        "scope": {"n_min": 1, "n_max": 100},
        "assurance": "verified",
        "method": "exact-algebraic",
        "performed_by": "repository",
        "relationship_to_generator": "independent-implementation",
        "origin": "replayed-here",
        "certificate": "frontier/n-029.md#verified-upper-bound",
        "replay": "uv run --frozen python -m devtools.check_basic_bounds",
        "replay_status": "passed",
        "limitations": "Establishes the grid fallback, not the reported record.",
        "source_reviewed": "2026-08-24",
    }


def valid_case() -> dict[str, object]:
    """Return a case whose verified bounds prove an exact value."""
    bound = {"value": "3", "exact_form": "3", "evidence": ["E-grid-exact"]}
    return {
        "n": 9,
        "reported_status": "proved",
        "status": "proved",
        "source_reviewed": "2026-08-24",
        "reported_upper_bound": {
            "value": "3",
            "exact_form": "3",
            "construction_method": "trivial-grid",
            "source_key": "[Kingbird]",
            "evidence": ["E-grid-exact"],
        },
        "verified_upper_bound": deepcopy(bound),
        "reported_lower_bound": {
            "value": "3",
            "exact_form": "3",
            "kind": "perfect-square",
            "source_key": None,
            "evidence": ["E-grid-exact"],
        },
        "verified_lower_bound": deepcopy(bound),
        "evidence": ["E-grid-exact"],
        "conflicts": [],
        "blockers": [],
        "resources": [],
    }


def valid_experiment() -> dict[str, object]:
    """Return the assurance-bearing fields used by experiment checks."""
    return {
        "subject": {
            "assurance": "numerically-checked",
            "method": "numerical-f64",
            "precision": {"binary_bits": 53, "rounding": "nearest-even"},
            "tolerance": "1e-10",
        },
        "results": [
            {
                "shape": "record",
                "beat_record": False,
            }
        ],
    }


def require_error(errors: list[str], fragment: str) -> None:
    """Require one diagnostic fragment without coupling tests to ordering."""
    assert any(fragment in error for error in errors), errors


def schema(name: str) -> Draft202012Validator:
    """Load one frontier schema through the same engine as the repository gate."""
    path = Path(__file__).resolve().parent.parent / "frontier" / name
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(document)
    return Draft202012Validator(document)


def main() -> int:
    numeric = numerical_evidence()
    exact = verified_evidence()
    assert check_evidence_semantics(numeric) == []
    assert check_evidence_semantics(exact) == []

    bad = deepcopy(numeric)
    bad["assurance"] = "verified"
    bad["origin"] = "replayed-here"
    require_error(check_evidence_semantics(bad), "numerical method cannot support verified")

    bad = deepcopy(exact)
    bad["certificate"] = None
    require_error(check_evidence_semantics(bad), "requires certificate and replay")

    historical = deepcopy(numeric)
    historical["precision"] = "unrecorded-historical"
    historical["tolerance"] = "unrecorded-historical"
    require_error(check_evidence_semantics(historical), "dated migration annotation")

    evidence = {"E-grid-exact": exact}
    case = valid_case()
    assert check_case_semantics(case, evidence) == []

    bad_case = deepcopy(case)
    bad_case["verified_lower_bound"] = {
        "value": "2.9",
        "exact_form": "29/10",
        "evidence": ["E-grid-exact"],
    }
    require_error(check_case_semantics(bad_case, evidence), "proved requires matching")

    bad_case = deepcopy(case)
    bad_case["evidence"] = ["E-does-not-exist"]
    require_error(check_case_semantics(bad_case, evidence), "unknown evidence")

    stale_blocker = deepcopy(case)
    stale_blocker["blockers"] = [
        {
            "kind": "mathematics",
            "detail": (
                "No formal certificate currently supports the tighter reported upper bound."
            ),
            "evidence": ["E-grid-exact"],
        }
    ]
    require_error(check_case_semantics(stale_blocker, evidence), "stale formal-upper-gap")

    unmarked_gap = deepcopy(case)
    unmarked_gap["reported_upper_bound"]["value"] = "2.9"  # type: ignore[index]
    unmarked_gap["reported_upper_bound"]["exact_form"] = None  # type: ignore[index]
    unmarked_gap["reported_upper_bound"]["evidence"] = []  # type: ignore[index]
    require_error(
        check_case_semantics(unmarked_gap, evidence),
        "formal upper trails report without a blocker",
    )

    shared_evidence_gap = deepcopy(case)
    shared_evidence_gap["reported_upper_bound"]["value"] = "2.9"  # type: ignore[index]
    shared_evidence_gap["reported_upper_bound"]["exact_form"] = None  # type: ignore[index]
    require_error(
        check_case_semantics(shared_evidence_gap, evidence),
        "formal upper trails report without a blocker",
    )

    experiment = valid_experiment()
    assert check_experiment_semantics(experiment) == []
    experiment["results"][0]["beat_record"] = True  # type: ignore[index]
    require_error(check_experiment_semantics(experiment), "beat_record requires verified")

    evidence_schema = schema("frontier-evidence.schema.yaml")
    evidence_schema.validate({"last_reviewed": "2026-08-24", "evidence": [numeric, exact]})
    case_schema = schema("square-packing-case.schema.yaml")
    case_schema.validate(case)
    malformed_case = deepcopy(case)
    malformed_case["verification_tier"] = "polished"
    malformed_serialized = yaml.safe_load(yaml.safe_dump(malformed_case))
    assert list(case_schema.iter_errors(malformed_serialized))

    legacy = {
        "n": 29,
        "status": "open",
        "upper_bound": {
            "value": 5.93383346267692,
            "value_str": "5.93383346267692",
            "exact_form": None,
            "method": "simulated_annealing",
            "found_by": ["Thomas Schadt"],
            "improved_by": ["David Ellsworth"],
            "catalogue_pictured": True,
        },
        "lower_bound": {
            "value": 5.472135955,
            "exact_form": None,
            "kind": "nagamochi",
            "source_key": "[Nagamochi 2005]",
        },
        "conjectured_optimum": "5.93383346267692",
        "priority_notes": [],
        "resources": [],
    }
    migrated = migrate_case(legacy)
    assert migrated["reported_upper_bound"]["value"] == "5.93383346267692"  # type: ignore[index]
    assert migrated["verified_upper_bound"]["exact_form"] == "6"  # type: ignore[index]
    assert migrated["verified_lower_bound"]["exact_form"] == (  # type: ignore[index]
        "sqrt(29 - 2*floor(sqrt(29)) + 1) + 1"
    )
    assert migrated["status"] == "open"

    audited_legacy = deepcopy(legacy)
    audited_legacy["n"] = 10
    audited_legacy["upper_bound"] = {
        **legacy["upper_bound"],
        "value": 3.70710678118654,
        "value_str": "3.70710678118654",
        "exact_form": "3 + (1/2)sqrt(2)",
    }
    audited_legacy["lower_bound"] = {
        **legacy["lower_bound"],
        "value": 3.707106781187,
        "exact_form": None,
        "kind": "unavoidable_points",
    }
    audited = apply_assurance_audits(migrate_case(audited_legacy))
    assert audited["status"] == "proved"
    assert audited["verified_upper_bound"]["evidence"] == [  # type: ignore[index]
        "E-n010-gobel-upper"
    ]

    assert verify_grid(5).valid
    assert verify_gobel5().valid
    assert verify_gobel10().valid
    basic_case = migrate_case(
        {
            **legacy,
            "n": 7,
            "upper_bound": {**legacy["upper_bound"], "value": 3, "value_str": "3"},
        }
    )
    assert check_case_basic_bounds(basic_case) == []
    malformed_bound = deepcopy(basic_case)
    malformed_bound["verified_upper_bound"]["exact_form"] = "2"  # type: ignore[index]
    require_error(check_case_basic_bounds(malformed_bound), "grid upper bound")

    # The reader-facing atlas preserves source precision and compares at the declared
    # scale. A longer exact rendering of the same value is not a conflict, while a
    # difference hidden by the old eight-decimal display remains visible.
    assert compact_bound({"value": "5.93383346267692", "exact_form": None}) == (
        "`5.93383346267692`"
    )
    assert (
        compact_bound(
            {
                "value": "5.472135955",
                "exact_form": "sqrt(29 - 2*floor(sqrt(29)) + 1) + 1",
            }
        )
        == "`1 + √20`"
    )
    assert (
        compact_bound(
            {
                "value": "5.93388579986236485799813026",
                "exact_form": ("296694289993118242899906513/50000000000000000000000000"),
            }
        )
        == "`296694289993118242899906513/50000000000000000000000000`"
    )
    assert same_bound(
        {"value": "3.87708359002281", "exact_form": None},
        {"value": "3.87708359002281417", "exact_form": "root(P, interval)"},
    )
    assert not same_bound(
        {"value": "5.93383346267692", "exact_form": None},
        {"value": "5.93388579986236485799813026", "exact_form": None},
    )
    assert not same_bound(
        {"value": "4.67553009360455", "exact_form": None},
        {"value": "5", "exact_form": "5"},
    )
    assert not same_bound(
        {"value": "1.000000001", "exact_form": None},
        {"value": "1.000000009", "exact_form": None},
    )

    print("frontier assurance contract selftest passed")
    return 0


def test_frontier_assurance_contract() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
