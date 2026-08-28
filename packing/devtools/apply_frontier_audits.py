#!/usr/bin/env python3
"""Apply reviewed proof and exact-construction evidence to migrated frontier cases."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml
from strif import atomic_output_file

from devtools.migrate_frontier_v2 import apply_assurance_audits

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"


def _frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        raise ValueError("Markdown artifact has no YAML frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("Markdown artifact has unterminated YAML frontmatter")
    document = yaml.safe_load(parts[1])
    if not isinstance(document, dict):
        raise TypeError("frontmatter must be an object")
    return document, parts[2]


def update_path(path: Path, *, write: bool) -> bool:
    """Update one v2 payload and preserve its reader-facing body."""
    original = path.read_text(encoding="utf-8")
    document, body = _frontmatter(original)
    payload = document.get("packing")
    if not isinstance(payload, dict):
        raise TypeError(f"{path}: packing payload must be an object")
    document["packing"] = apply_assurance_audits(payload)
    rendered = (
        "---\n"
        + yaml.safe_dump(document, allow_unicode=True, sort_keys=False, width=96)
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
    parser.add_argument("--write", action="store_true", help="rewrite audited cases")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = sorted(FRONTIER.glob("n-*.md"))
    changed = [path for path in paths if update_path(path, write=args.write)]
    action = "updated" if args.write else "would update"
    print(f"{action} {len(changed)} of {len(paths)} frontier cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
