#!/usr/bin/env python3
"""Render the synopsis document table from the validated document map."""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from pathlib import Path

from strif import atomic_output_file

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parents[1]
# The repository root. The reader-facing documents live there, not under packing/.
REPO = ROOT.parent
MAP = REPO / "docs" / "project" / "document-map.yaml"
SYNOPSIS = REPO / "SYNOPSIS.md"
BEGIN = "<!-- BEGIN GENERATED: document-map (devtools.render_document_map) -->"
END = "<!-- END GENERATED: document-map -->"

ROLE_LABELS = {
    "orientation": "reader orientation",
    "technical-synthesis": "current technical state and terminology",
    "tutorial": "first-principles tutorial",
    "conventions": "artifact and naming conventions",
    "epistemic-policy": "whole-result evidence classifications",
    "operating-rules": "how a session is conducted",
    "development-guide": "engineering and validation rules",
    "research-runbook": "W6 experiment mechanics",
    "documentation-runbook": "W8 documentation reconciliation",
    "remediation-runbook": "systematic defect and issue-backlog remediation",
    "oversight-runbook": "post-agenda disposition, document review, and replanning",
    "session-guide": "escalated session and recovery contract",
    "research-loop-logbook": "reader-facing research-run summaries",
    "series-guide": "series scope and comparability",
    "registry": "hand-maintained registry",
    "generated-view": "generated status view",
    "frontier-guide": "frontier semantics and contribution path",
    "source-index": "source retention and archive policy",
    "research-report": "research synthesis",
    "review": "dated review record",
    "plan": "implementation plan",
    "handoff": "dated handoff record",
    "postmortem": "failure analysis and lessons",
    "component-guide": "component scope and use",
    "frontier-case": "typed case claim register",
    "hypothesis-record": "typed hypothesis record",
    "experiment-record": "typed experiment record",
    "session-record": "typed session record",
    "research-loop-run-record": "typed research-run synopsis",
    "agenda": "mutable coordination agenda",
    "exploration-report": "typed idea provenance",
}


def load_map() -> dict:
    """Load the pure-YAML DocumentMap/v1 payload."""
    document = safe_load(MAP.read_text(encoding="utf-8"))
    return {key: value for key, value in document.items() if key != "softschema"}


def title(path: Path) -> str:
    """Use a document's own H1 rather than duplicating its title in the map."""
    match = re.search(r"^#\s+(.+)$", path.read_text(encoding="utf-8"), re.MULTILINE)
    return match.group(1) if match else path.name


def document_link(relative: str) -> str:
    return f"[{title(REPO / relative)}]({relative})"


def render_table(document_map: dict) -> str:
    """Render one compact reader view from the map's semantic fields."""
    rows = [
        "| Document or collection | Role | Authority | Lifecycle | Current replacement |",
        "| --- | --- | --- | --- | --- |",
    ]
    for document in document_map["documents"]:
        replacement = document.get("superseded_by")
        replacement_cell = document_link(replacement) if replacement else "—"
        rows.append(
            f"| {document_link(document['path'])} | {ROLE_LABELS[document['role']]} | "
            f"{document['authority']} | {document['lifecycle']} | {replacement_cell} |"
        )
    for collection in document_map["collections"]:
        replacement = collection.get("superseded_by")
        replacement_cell = document_link(replacement) if replacement else "—"
        rows.append(
            f"| `{collection['pattern']}` | {ROLE_LABELS[collection['role']]} | "
            f"{collection['authority']} | {collection['lifecycle']} | "
            f"{replacement_cell} |"
        )
    return "\n".join(rows)


def expected_synopsis(text: str, document_map: dict) -> str:
    """Replace the one generated block while preserving editorial prose around it."""
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise ValueError("SYNOPSIS.md needs exactly one ordered document-map marker pair")
    start = text.index(BEGIN)
    end = text.index(END, start) + len(END)
    block = f"{BEGIN}\n\n{render_table(document_map)}\n\n{END}"
    return text[:start] + block + text[end:]


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("--check", action="store_true", help="fail if SYNOPSIS.md is stale")
    return command


def main(argv: Sequence[str] | None = None) -> int:
    arguments = parser().parse_args(argv)
    current = SYNOPSIS.read_text(encoding="utf-8")
    expected = expected_synopsis(current, load_map())
    if arguments.check:
        if current != expected:
            print("SYNOPSIS.md document map is stale", file=sys.stderr)
            return 1
        print("  synopsis document map matches docs/project/document-map.yaml")
        return 0
    if current != expected:
        with atomic_output_file(SYNOPSIS) as temporary:
            temporary.write_text(expected, encoding="utf-8")
        print("rendered synopsis document map")
    else:
        print("synopsis document map already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
