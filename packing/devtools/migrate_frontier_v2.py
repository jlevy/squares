#!/usr/bin/env python3
"""Migrate SquarePackingCase/v1 frontmatter to the assurance-separated v2 contract."""

from __future__ import annotations

import argparse
import math
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path

import yaml
from strif import atomic_output_file

from sqpack.assurance import bounds_agree_at_declared_precision
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
REVIEW_DATE = "2026-08-24"
COMMON_DOC_FOOTER = """<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
"""

METHODS = {
    "trivial_grid": "trivial-grid",
    "hand_construction": "hand-construction",
    "diagonal_strip": "diagonal-strip",
    "pattern_family": "pattern-family",
    "extension": "extension",
    "composition": "composition",
    "simulated_annealing": "simulated-annealing",
    "inflation_billiard": "inflation-billiard",
    "unknown": "unknown",
}

LOWER_KINDS = {
    "area": "area",
    "perfect_square": "perfect-square",
    "nagamochi": "nagamochi",
    "monotonicity": "monotonicity",
    "unavoidable_points": "unavoidable-points",
    "counting": "counting",
}

RESOURCE_ROLES = {
    "upper_bound": "upper-bound-report",
    "lower_bound": "lower-bound-proof",
    "record_catalogue": "record-catalogue",
    "survey": "survey",
    "exact_solution": "numerical-witness",
    "context": "context",
}

SPECIAL_LOWER_EVIDENCE = {
    2: "E-side2-center-lower",
    3: "E-side2-center-lower",
    5: "E-n005-gobel-proof",
    6: "E-n006-kearney-shiu-proof",
    10: "E-n010-stromquist-proof",
    11: "E-n011-repaired-lower",
    12: "E-n012-monotonicity-lower",
    13: "E-bentz-2010-proof",
    22: "E-bentz-2016-proof",
    33: "E-bentz-2016-proof",
    46: "E-bentz-2010-proof",
}


def _mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{label} must be an object")
    return value


def _literal(value: object) -> str:
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise TypeError(f"bound value must be a scalar, got {value!r}")
    return str(value)


def _strings(value: object, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise TypeError(f"{label} must be a list of strings")
    return value


def _reported_value(bound: Mapping[str, object]) -> str:
    value_str = bound.get("value_str")
    return value_str if isinstance(value_str, str) else _literal(bound.get("value"))


def _ceil_sqrt(n: int) -> int:
    root = math.isqrt(n)
    return root if root * root == n else root + 1


def _nagamochi_identity(n: int) -> tuple[str, str]:
    side = _ceil_sqrt(n)
    if side * side - n <= 2:
        value = str(side)
        return value, value
    exact = f"sqrt({n} - 2*floor(sqrt({n})) + 1) + 1"
    floor_root = math.isqrt(n)
    display = format(math.sqrt(n - 2 * floor_root + 1) + 1, ".12g")
    return display, exact


def _reported_lower_evidence(n: int, kind: object) -> str:
    if n in SPECIAL_LOWER_EVIDENCE:
        return SPECIAL_LOWER_EVIDENCE[n]
    if kind == "nagamochi":
        return "E-nagamochi-lower"
    if kind in {"area", "perfect_square"}:
        return "E-basic-area-lower"
    return "E-migrated-lower-report"


def _verified_upper(n: int) -> dict[str, object]:
    if n == 5:
        return {
            "value": "2.70710678118654752440084436210485",
            "exact_form": "2 + (1/2)sqrt(2)",
            "evidence": ["E-n005-gobel-upper"],
        }
    if n == 10:
        return {
            "value": "3.70710678118654752440084436210485",
            "exact_form": "3 + (1/2)sqrt(2)",
            "evidence": ["E-n010-gobel-upper"],
        }
    if n == 11:
        return {
            "value": "3.87708359002281417730789706010096",
            "exact_form": "root(P_trump11, 3.87708359002281417730789706010096)",
            "evidence": ["E-n011-trump-upper"],
        }
    side = str(_ceil_sqrt(n))
    return {"value": side, "exact_form": side, "evidence": ["E-basic-grid-upper"]}


def _verified_lower(n: int) -> dict[str, object]:
    exact_audits = {
        2: ("2", "2", "E-side2-center-lower"),
        3: ("2", "2", "E-side2-center-lower"),
        5: (
            "2.70710678118654752440084436210485",
            "2 + (1/2)sqrt(2)",
            "E-n005-gobel-proof",
        ),
        6: ("3", "3", "E-n006-kearney-shiu-proof"),
        10: (
            "3.70710678118654752440084436210485",
            "3 + (1/2)sqrt(2)",
            "E-n010-stromquist-proof",
        ),
        13: ("4", "4", "E-bentz-2010-proof"),
        22: ("5", "5", "E-bentz-2016-proof"),
        33: ("6", "6", "E-bentz-2016-proof"),
        46: ("7", "7", "E-bentz-2010-proof"),
    }
    if n in exact_audits:
        value, exact, evidence = exact_audits[n]
        return {"value": value, "exact_form": exact, "evidence": [evidence]}
    if n == 11:
        return {
            "value": "3.788854381999831757127338934985",
            "exact_form": "2 + 4/sqrt(5)",
            "evidence": ["E-n011-repaired-lower"],
        }
    if n == 12:
        return {
            "value": "3.788854381999831757127338934985",
            "exact_form": "2 + 4/sqrt(5)",
            "evidence": ["E-n012-monotonicity-lower"],
        }
    if n >= 4:
        value, exact = _nagamochi_identity(n)
        return {"value": value, "exact_form": exact, "evidence": ["E-nagamochi-lower"]}
    value = format(math.sqrt(n), ".12g")
    return {
        "value": value,
        "exact_form": str(n) if n == 1 else f"sqrt({n})",
        "evidence": ["E-basic-area-lower"],
    }


def _migrate_resources(value: object) -> list[dict[str, object]]:
    if not isinstance(value, list):
        return []
    migrated: list[dict[str, object]] = []
    for raw in value:
        source = _mapping(raw, "resource")
        role = source.get("role")
        if not isinstance(role, str) or role not in RESOURCE_ROLES:
            raise ValueError(f"unsupported v1 resource role {role!r}")
        migrated.append(
            {
                "key": source.get("key"),
                "role": RESOURCE_ROLES[role],
                "local": source.get("local"),
                "url": source.get("url"),
                "retrieved": source.get("retrieved"),
            }
        )
    return migrated


def _bound_identity(bound: Mapping[str, object]) -> str | None:
    exact = bound.get("exact_form")
    if isinstance(exact, str) and exact:
        return exact
    value = bound.get("value")
    return value if isinstance(value, str) and value else None


def apply_assurance_audits(case: Mapping[str, object]) -> dict[str, object]:
    """Apply the reviewed exact constructions and complete proof records to v2 data."""
    audited = {2, 3, 5, 6, 10, 13, 22, 33, 46}
    n_value = case.get("n")
    if not isinstance(n_value, int):
        raise TypeError("case n must be an integer")
    result = deepcopy(dict(case))
    if n_value not in audited:
        return _remove_stale_upper_gap_blocker(result)

    result["verified_upper_bound"] = _verified_upper(n_value)
    result["verified_lower_bound"] = _verified_lower(n_value)
    reported_lower = dict(_mapping(result.get("reported_lower_bound"), "reported lower"))
    reported_lower["evidence"] = [_reported_lower_evidence(n_value, reported_lower.get("kind"))]
    result["reported_lower_bound"] = reported_lower
    reported_upper = dict(_mapping(result.get("reported_upper_bound"), "reported upper"))
    exact_upper_evidence = {
        5: "E-n005-gobel-upper",
        10: "E-n010-gobel-upper",
    }
    if n_value in exact_upper_evidence:
        reported_upper["evidence"] = list(
            dict.fromkeys(
                [
                    *_strings(reported_upper.get("evidence"), "reported upper evidence"),
                    exact_upper_evidence[n_value],
                ]
            )
        )
    result["reported_upper_bound"] = reported_upper

    verified_upper = _mapping(result["verified_upper_bound"], "verified upper")
    verified_lower = _mapping(result["verified_lower_bound"], "verified lower")
    refs = [
        *_strings(reported_upper.get("evidence"), "reported upper evidence"),
        *_strings(reported_lower.get("evidence"), "reported lower evidence"),
        *_strings(verified_upper.get("evidence"), "verified upper evidence"),
        *_strings(verified_lower.get("evidence"), "verified lower evidence"),
    ]
    retained = [
        ref
        for ref in _strings(result.get("evidence"), "case evidence")
        if ref != "E-migrated-lower-report"
    ]
    result["evidence"] = list(dict.fromkeys([*retained, *refs]))
    result["status"] = (
        "proved"
        if _bound_identity(verified_upper) == _bound_identity(verified_lower)
        else "open"
    )
    result["source_reviewed"] = "2026-08-25"
    if result["status"] == "proved":
        blockers = result.get("blockers")
        if isinstance(blockers, list):
            result["blockers"] = [
                blocker
                for blocker in blockers
                if not (
                    isinstance(blocker, Mapping)
                    and str(blocker.get("detail", "")).startswith(
                        "No formal certificate currently supports"
                    )
                )
            ]
    return _remove_stale_upper_gap_blocker(result)


def _remove_stale_upper_gap_blocker(case: dict[str, object]) -> dict[str, object]:
    """Drop the migration blocker when reported and formal lanes represent one bound."""
    if not bounds_agree_at_declared_precision(
        case.get("reported_upper_bound"), case.get("verified_upper_bound")
    ):
        return case
    blockers = case.get("blockers")
    if isinstance(blockers, list):
        case["blockers"] = [
            blocker
            for blocker in blockers
            if not (
                isinstance(blocker, Mapping)
                and str(blocker.get("detail", "")).startswith(
                    "No formal certificate currently supports"
                )
            )
        ]
    return case


def migrate_case(legacy: Mapping[str, object]) -> dict[str, object]:
    """Return a conservative v2 case without upgrading unsupported claims."""
    n_value = legacy.get("n")
    if not isinstance(n_value, int):
        raise TypeError("case n must be an integer")
    upper = _mapping(legacy.get("upper_bound"), "upper_bound")
    lower = _mapping(legacy.get("lower_bound"), "lower_bound")
    method = upper.get("method")
    kind = lower.get("kind")
    if not isinstance(method, str) or method not in METHODS:
        raise ValueError(f"unsupported v1 upper-bound method {method!r}")
    if not isinstance(kind, str) or kind not in LOWER_KINDS:
        raise ValueError(f"unsupported v1 lower-bound kind {kind!r}")

    upper_report_evidence = ["E-kingbird-upper-register"]
    if n_value in {5, 10}:
        upper_report_evidence.append(
            "E-n005-gobel-upper" if n_value == 5 else "E-n010-gobel-upper"
        )
    if n_value == 11:
        upper_report_evidence.append("E-n011-trump-upper")
    if n_value == 29:
        upper_report_evidence.append("E-n029-kingbird-report")
    lower_report_evidence = [_reported_lower_evidence(n_value, kind)]
    verified_upper = _verified_upper(n_value)
    verified_lower = _verified_lower(n_value)
    evidence = list(
        dict.fromkeys(
            upper_report_evidence
            + lower_report_evidence
            + _strings(verified_upper["evidence"], "verified upper evidence")
            + _strings(verified_lower["evidence"], "verified lower evidence")
        )
    )
    if n_value == 29:
        evidence.extend(["E-n029-kingbird-numerical", "E-n029-orientation-classes"])

    upper_identity = verified_upper["exact_form"] or verified_upper["value"]
    lower_identity = verified_lower["exact_form"] or verified_lower["value"]
    status = "proved" if upper_identity == lower_identity else "open"

    reported_upper = {
        "value": _reported_value(upper),
        "exact_form": upper.get("exact_form"),
        "algebraic_degree": upper.get("algebraic_degree"),
        "minimal_polynomial": upper.get("minimal_polynomial"),
        "analytically_optimized": upper.get("analytically_optimized"),
        # v1 carried a boolean `rigid` whose false and null both meant "the catalogue
        # did not annotate this packing"; only true was a transcribed statement. v2
        # says that in the source's own three-valued vocabulary, and keeps the
        # repository's own finding in the separate case-level `rigidity` field.
        "catalogue_rigid": "rigid" if upper.get("rigid") is True else "not-stated",
        "construction_method": METHODS[method],
        "tilt_angles_deg": upper.get("tilt_angles_deg"),
        "found_by": upper.get("found_by", []),
        "found_year": upper.get("found_year"),
        "improved_by": upper.get("improved_by", []),
        "catalogue_pictured": upper.get("catalogue_pictured", False),
        "source_key": "[Kingbird]",
        "source_date": None,
        "retrieved_date": "2026-08-22",
        "witnesses": ["W-n029-kingbird"] if n_value == 29 else [],
        "evidence": upper_report_evidence,
    }
    reported_lower = {
        "value": _literal(lower.get("value")),
        "exact_form": lower.get("exact_form"),
        "kind": LOWER_KINDS[kind],
        "proved_by": lower.get("proved_by", []),
        "proved_year": lower.get("proved_year"),
        "source_key": lower.get("source_key"),
        "note": lower.get("note"),
        "scope": None,
        "evidence": lower_report_evidence,
    }
    blockers: list[dict[str, object]] = []
    if not bounds_agree_at_declared_precision(reported_upper, verified_upper):
        blockers.append(
            {
                "kind": "mathematics",
                "detail": (
                    "No formal certificate currently supports the tighter reported upper bound."
                ),
                "evidence": upper_report_evidence,
            }
        )
    conflicts: list[dict[str, object]] = []
    if n_value == 29:
        conflicts.append(
            {
                "kind": "scope-ambiguity",
                "detail": (
                    "The source describes an exact analytic solution, but the public SVG "
                    "serializes a numerical FindRoot result and no formal certificate."
                ),
                "evidence": ["E-n029-kingbird-report", "E-n029-kingbird-numerical"],
            }
        )
    return {
        "n": n_value,
        "reported_status": legacy.get("status"),
        "status": status,
        "source_reviewed": REVIEW_DATE,
        "reported_upper_bound": reported_upper,
        "verified_upper_bound": verified_upper,
        "reported_lower_bound": reported_lower,
        "verified_lower_bound": verified_lower,
        # v1 had no first-party rigidity finding to carry forward, and null here means
        # exactly that: not assessed. It never means the packing can move.
        "rigidity": None,
        "conjectured_optimum": legacy.get("conjectured_optimum"),
        "priority_notes": legacy.get("priority_notes", []),
        "evidence": evidence,
        "conflicts": conflicts,
        "blockers": blockers,
        "resources": _migrate_resources(legacy.get("resources")),
    }


def _frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        raise ValueError("Markdown artifact has no YAML frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("Markdown artifact has unterminated YAML frontmatter")
    document = safe_load(parts[1])
    if not isinstance(document, dict):
        raise TypeError("frontmatter must be an object")
    return document, parts[2]


def migrate_path(path: Path, *, write: bool) -> bool:
    """Migrate one path and return whether its serialized content changes."""
    current = path.read_text(encoding="utf-8")
    document, body = _frontmatter(current)
    softschema = _mapping(document.get("softschema"), "softschema")
    contract = softschema.get("contract")
    if contract == "packing.squares:SquarePackingCase/v2":
        rendered = current
        if "This document follows common-doc-guidelines.md." not in current:
            rendered = current.rstrip() + "\n\n" + COMMON_DOC_FOOTER
        changed = rendered != current
        if changed and write:
            with atomic_output_file(path) as temporary:
                temporary.write_text(rendered, encoding="utf-8")
        return changed
    if contract != "packing.squares:SquarePackingCase/v1":
        raise ValueError(f"{path}: unsupported contract {contract!r}")
    migrated = {
        "title": document.get("title"),
        "softschema": {
            "contract": "packing.squares:SquarePackingCase/v2",
            "schema": "square-packing-case.schema.yaml",
            "envelope": "packing",
            "status": "enforced",
        },
        "packing": migrate_case(_mapping(document.get("packing"), "packing")),
    }
    body_with_footer = body
    if "This document follows common-doc-guidelines.md." not in body:
        body_with_footer = body.rstrip() + "\n\n" + COMMON_DOC_FOOTER
    rendered = (
        "---\n"
        + yaml.safe_dump(migrated, allow_unicode=True, sort_keys=False, width=96)
        + "---\n"
        + body_with_footer
    )
    changed = rendered != current
    if changed and write:
        with atomic_output_file(path) as temporary:
            temporary.write_text(rendered, encoding="utf-8")
    return changed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="rewrite v1 artifacts in place")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = sorted(FRONTIER.glob("n-*.md"))
    changed = [path for path in paths if migrate_path(path, write=args.write)]
    action = "migrated" if args.write else "would migrate"
    print(f"{action} {len(changed)} of {len(paths)} frontier cases")
    if changed and not args.write:
        print("re-run with --write after reviewing the contract and selftest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
