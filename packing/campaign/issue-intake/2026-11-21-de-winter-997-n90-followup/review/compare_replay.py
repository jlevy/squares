"""Compare a working replay with the frozen source-only mathematical result."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

TIMING_KEYS = {"elapsed_seconds", "started_at_utc", "finished_at_utc"}


def normalized(value: Any, *, top: bool = False) -> Any:
    if isinstance(value, dict):
        return {
            key: normalized(item)
            for key, item in value.items()
            if key not in TIMING_KEYS and not (top and key == "program_sha256")
        }
    if isinstance(value, list):
        return [normalized(item) for item in value]
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("frozen", type=Path)
    parser.add_argument("working", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    original = json.loads(args.frozen.read_text())
    replay = json.loads(args.working.read_text())
    original_normal = normalized(original, top=True)
    replay_normal = normalized(replay, top=True)
    altered = copy.deepcopy(replay)
    altered["candidate"]["feasible"] = not altered["candidate"]["feasible"]
    negative_control = normalized(altered, top=True) != replay_normal
    same = original_normal == replay_normal
    report = {
        "frozen_result_sha256": hashlib.sha256(args.frozen.read_bytes()).hexdigest(),
        "working_result_sha256": hashlib.sha256(args.working.read_bytes()).hexdigest(),
        "frozen_program_sha256": original["program_sha256"],
        "working_program_sha256": replay["program_sha256"],
        "program_identity_handling": (
            "Compared separately; the working program intentionally has different bytes."
        ),
        "excluded_timing_keys": sorted(TIMING_KEYS),
        "all_other_fields_match": same,
        "geometry_sources_controls_and_verdicts_match": same,
        "negative_control_changed_candidate_verdict_detected": negative_control,
        "compared_top_level_fields": sorted(original_normal),
        "mismatched_top_level_fields": [
            key
            for key in sorted(original_normal)
            if original_normal[key] != replay_normal.get(key)
        ],
        "pass": same and negative_control,
    }
    _ = args.out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
