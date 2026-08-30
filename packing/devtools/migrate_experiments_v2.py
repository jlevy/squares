#!/usr/bin/env python3
"""Migrate Experiment/v1 artifacts to explicit assurance and arithmetic fields."""

from __future__ import annotations

import argparse
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path

import yaml
from strif import atomic_output_file

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
CAMPAIGN = ROOT / "campaign"
MIGRATION_DATE = "2026-08-25"


def _mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{label} must be an object")
    return value


def _assurance_fields(experiment_id: str, old_precision: object) -> dict[str, object]:
    if old_precision == "exact":
        return {
            "assurance": "verified",
            "method": "exact-algebraic",
        }
    if experiment_id == "exp-012":
        if old_precision != "polished":
            raise ValueError("exp-012 must migrate from its historical polished label")
        return {
            "assurance": "numerically-checked",
            "method": "numerical-multiprecision",
            "precision": {"decimal_digits": 160, "rounding": "nearest"},
            "tolerance": "1e-80",
        }
    if old_precision in {"f64_screen", "polished"}:
        return {
            "assurance": "numerically-checked",
            "method": "numerical-f64",
            "precision": {"binary_bits": 53, "rounding": "nearest-even"},
            "tolerance": "unrecorded-historical",
            "migration_annotation": (
                f"{MIGRATION_DATE}: the v1 artifact identified float64 arithmetic but "
                "did not retain one experiment-wide acceptance tolerance."
            ),
        }
    raise ValueError(f"unsupported historical precision label {old_precision!r}")


def migrate_experiment(legacy: Mapping[str, object]) -> dict[str, object]:
    """Return an Experiment/v2 payload without inventing historical tolerance data."""
    experiment_id = legacy.get("id")
    if not isinstance(experiment_id, str):
        raise TypeError("experiment id must be a string")
    subject = _mapping(legacy.get("subject"), "subject")
    if "assurance" in subject:
        return deepcopy(dict(legacy))
    assurance = _assurance_fields(experiment_id, subject.get("precision"))
    migrated_subject: dict[str, object] = {}
    for key, value in subject.items():
        if key == "precision":
            migrated_subject.update(assurance)
        else:
            migrated_subject[key] = deepcopy(value)
    migrated = deepcopy(dict(legacy))
    migrated["subject"] = migrated_subject
    return migrated


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
    """Migrate one experiment path and return whether its content changes."""
    original = path.read_text(encoding="utf-8")
    document, body = _frontmatter(original)
    softschema = _mapping(document.get("softschema"), "softschema")
    contract = softschema.get("contract")
    if contract == "packing.squares:Experiment/v2":
        return False
    if contract != "packing.squares:Experiment/v1":
        raise ValueError(f"{path}: unsupported contract {contract!r}")
    migrated = {
        "title": document.get("title"),
        "softschema": {
            "contract": "packing.squares:Experiment/v2",
            "schema": softschema.get("schema"),
            "envelope": "experiment",
            "status": "enforced",
        },
        "experiment": migrate_experiment(_mapping(document.get("experiment"), "experiment")),
    }
    rendered = (
        "---\n"
        + yaml.safe_dump(migrated, allow_unicode=True, sort_keys=False, width=96)
        + "---\n"
        + body
    )
    changed = rendered != original
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
    paths = sorted(CAMPAIGN.glob("series/*/experiments/*.md"))
    changed = [path for path in paths if migrate_path(path, write=args.write)]
    action = "migrated" if args.write else "would migrate"
    print(f"{action} {len(changed)} of {len(paths)} experiment artifacts")
    if changed and not args.write:
        print("re-run with --write after reviewing the v2 contract and selftest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
