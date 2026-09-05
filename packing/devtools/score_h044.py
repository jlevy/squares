"""Score H-044's registered criterion from the frozen chunk-partition atlas.

H-044 (registered 2026-08-26) claims at least 80 percent of standing-record poses at
``n <= 30`` with public full geometry are chunk-expressible at ``K <= 6`` with at most
two free squares under the declared adjacency bands. The partition atlas
(``atlas/known-best/chunk-partitions.json``) carries the per-record evaluation under
the frozen contract; its schema pins ``claim_status: calibration-no-verdict`` by
``const``, deliberately, so the atlas cannot quietly become evidence. This scorer is
the step that turns it into a registered measurement: it re-derives establishment per
record from the stored options rather than trusting the stored status, applies the
registered slice, and emits the exp-046 results record with a typed reason for every
miss.

The scoring never edits the atlas. A verdict lands in the experiment record; the
emitted ``verdict_note`` string is frozen with the byte-identical replay and records
the run-night hold. The 2026-08-31 verification review (session-060) resolved that
hold in the experiment record itself: the miss is determinate under both denominator
readings, and H-044 stays undisposed by its own calibration-only amendment; the two
frozen-contract decisions (singleton chunks inadmissible; sliding contact assemblies
outside the candidate universe) remain the priced reopen paths.

Usage, from ``packing/``:
    uv run --frozen python -m devtools.score_h044 --record <out.json>
    uv run --frozen python -m devtools.score_h044 --check <recorded.json>
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
ATLAS = ROOT / "atlas/known-best/chunk-partitions.json"

#: The registered criterion, quoted from campaign/hypotheses/H-044 (frozen 2026-08-26).
REGISTERED_THRESHOLD_NUMERATOR = 4
REGISTERED_THRESHOLD_DENOMINATOR = 5
REGISTERED_MAXIMUM_N = 30
REGISTERED_MAXIMUM_CHUNKS = 6
REGISTERED_MAXIMUM_FREE_SQUARES = 2
REGISTERED_MAXIMUM_OFF_FRAME_CHUNKS = 2


def _established(entry: dict[str, Any]) -> tuple[bool, str]:
    """Re-derive one record's establishment; return (established, typed reason).

    Trusting the stored ``status`` would make the score an echo of the generator, so
    the row is re-derived from the stored options: the selected option must exist, be
    partitioned, and meet every registered bound. Any disagreement with the stored
    status is a scoring failure, not a soft note.
    """
    options = entry.get("options", [])
    selected_free = entry.get("selected_free_square_count")
    if selected_free is None:
        limits = sorted({option["status"] for option in options} - {"partitioned"})
        reason = " and ".join(limits) if limits else "no options recorded"
        return False, f"typed-{reason}" if limits else reason
    matching = [
        option
        for option in options
        if option["free_square_count"] == selected_free and option["status"] == "partitioned"
    ]
    if len(matching) != 1:
        return False, "selected option missing from stored options"
    option = matching[0]
    if option["chunk_count"] > REGISTERED_MAXIMUM_CHUNKS:
        return False, f"outside registered chunk budget ({option['chunk_count']} > 6)"
    if selected_free > REGISTERED_MAXIMUM_FREE_SQUARES:
        return False, f"outside registered free budget ({selected_free} > 2)"
    if option["off_frame_chunk_count"] > REGISTERED_MAXIMUM_OFF_FRAME_CHUNKS:
        return False, "outside registered off-frame budget"
    return True, "established"


def score() -> dict[str, Any]:
    atlas = json.loads(ATLAS.read_text(encoding="utf-8"))["atlas"]
    bands = []
    for band in atlas["bands"]:
        rows = []
        for entry in band["entries"]:
            if entry["n"] > REGISTERED_MAXIMUM_N:
                continue
            established, reason = _established(entry)
            stored = entry["status"] == "established"
            if established != stored:
                raise SystemExit(
                    f"score disagrees with stored status at n={entry['n']} "
                    f"band={band['name']}: derived {established}, stored {entry['status']}"
                )
            rows.append(
                {
                    "n": entry["n"],
                    "witness_id": entry["witness_id"],
                    "source_kind": entry["source_kind"],
                    "established": established,
                    "reason": reason,
                    "selected_chunk_count": entry.get("selected_chunk_count"),
                    "selected_free_square_count": entry.get("selected_free_square_count"),
                    "limitation": None if established else entry.get("limitation"),
                }
            )
        rows.sort(key=lambda row: row["n"])

        def reading(rows_subset: list[dict[str, Any]]) -> dict[str, Any]:
            established_count = sum(row["established"] for row in rows_subset)
            return {
                "records": len(rows_subset),
                "established": established_count,
                "fraction": f"{established_count}/{len(rows_subset)}",
                "fraction_decimal_display_only": (
                    f"{established_count / len(rows_subset):.6f}" if rows_subset else "0"
                ),
                "criterion_met": (
                    established_count * REGISTERED_THRESHOLD_DENOMINATOR
                    >= len(rows_subset) * REGISTERED_THRESHOLD_NUMERATOR
                ),
            }

        bands.append(
            {
                "band": band["name"],
                "denominator_readings": {
                    "all_records": reading(rows),
                    "non_grid_sweep_records": reading(
                        [row for row in rows if row["source_kind"] != "exact-grid"]
                    ),
                },
                "rows": rows,
            }
        )
    return {
        "hypothesis": "H-044",
        "criterion": (
            "at least 4/5 of frozen-corpus records at n <= 30 admit a K <= 6 chunk "
            "decomposition with at most two free squares under the declared bands"
        ),
        "corpus": {
            "source": "atlas/known-best/chunk-partitions.json",
            "freeze": atlas["corpus"],
            "freeze_caveat": (
                "no machine-readable freeze date or content hash exists for the "
                "manifest; the nearest anchors are the 2026-08-26 retrieval dates "
                "and H-044's own registration date, and H-044's review amendment "
                "marks this corpus calibration-only"
            ),
            "denominator_readings": {
                "all_records": (
                    "every atlas record at n <= 30 (30: 20 exact-grid plus 10 "
                    "non-grid), per the claim text 'standing-record poses at "
                    "n <= 30 with public full geometry'"
                ),
                "non_grid_sweep_records": (
                    "the 10 non-grid records, which are exactly H-044's own sweep "
                    "points at n <= 30; the registered text supports both readings "
                    "and choosing between them is a preregistration-style decision "
                    "held for the owner"
                ),
            },
        },
        "contract_decisions_in_force": [
            "singleton chunks are inadmissible (candidate generation requires size >= 2)",
            (
                "sliding contact assemblies and angle-class splits are outside the "
                "candidate universe; their misses are typed, never H-044 refutations"
            ),
        ],
        "bands": bands,
        "verdict_note": (
            "held unresolved with needs_review per the run's unattended rules; the "
            "fraction sits near the registered threshold and both review questions "
            "are frozen-contract decisions, not tonight's"
        ),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--record", type=Path, help="write the scored record here")
    group.add_argument("--check", type=Path, help="recompute and compare to this record")
    options = parser.parse_args(argv)
    scored = score()
    if options.record is not None:
        options.record.parent.mkdir(parents=True, exist_ok=True)
        options.record.write_text(json.dumps(scored, indent=1) + "\n", encoding="utf-8")
        print(f"wrote {options.record}")
    else:
        recorded = json.loads(options.check.read_text(encoding="utf-8"))
        if recorded != scored:
            print("FAIL recorded H-044 score does not replay from the atlas", file=sys.stderr)
            return 1
        print("recorded H-044 score replays from the atlas")
    for band in scored["bands"]:
        for name, reading in band["denominator_readings"].items():
            met = "met" if reading["criterion_met"] else "missed"
            print(
                f"  {band['band']} / {name}: {reading['fraction']} established "
                f"({reading['fraction_decimal_display_only']}) -- criterion {met} as evaluated"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
