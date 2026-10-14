"""Print `sources.yaml`'s structure: report coordinates, lane mappings and transcribed claims.

Long exact sides are abbreviated. From `packing/`, with the project interpreter::

    python campaign/issue-intake/upper-bounds-20261014/review/dump_sources.py
"""

from __future__ import annotations

from pathlib import Path

import yaml

#: The repository root: this file is packing/campaign/issue-intake/<directory>/review/.
REPO = Path(__file__).resolve().parents[5]
SOURCES = REPO / "packing/campaign/issue-intake/upper-bounds-20261014/sources.yaml"


def main() -> None:
    sources = yaml.safe_load(SOURCES.read_text(encoding="utf-8"))
    print("exceptions:", sources.get("exceptions"))
    print("other_items:", [item["issue"] for item in sources.get("other_items", [])])
    for report in sources["reports"]:
        print("==", {key: report[key] for key in report if key not in ("claims", "lanes")})
        for mapping in report.get("lanes", []):
            print("   lane:", mapping)
        for claim in report.get("claims", []):
            short = {
                key: value[:24] + "..."
                if key == "exact" and isinstance(value, str) and len(value) > 60
                else value
                for key, value in claim.items()
            }
            print("   claim:", short)


if __name__ == "__main__":
    main()
