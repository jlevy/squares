#!/usr/bin/env python3
"""Why each layer-plus-one mutant of the sampled rows is refused, mutant by mutant
(stage 4 review of the filled-end lemma, PR #870).

`fe_independent.py`'s sample receipt keeps, per row, only the union of its layer
mutants' reasons. This program decides the same mutants again with `fe_independent`'s
geometry and records each one's own reasons: which band rows the new square overlaps and
whether it crosses a wall. Standard library only, through `fe_independent`.

    python -I fe_layer_reasons.py PACKET OUT.json N...
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fe_independent as fe  # noqa: E402


def main() -> int:
    packet = Path(sys.argv[1])
    out = Path(sys.argv[2])
    counts = [int(a) for a in sys.argv[3:]]
    text, digest = fe.deposit_text(packet, "2")
    rows = {row["n"]: row for row in fe.read_rows(text)}
    started = time.process_time()
    mutants = []
    for n in counts:
        row = rows[n]
        side, polys, v, h = fe.construction(row)
        base = fe.Verdict(polys, side)
        for item in fe.layer_mutants(row, base, v, h):
            mutants.append(
                {
                    "n": n,
                    "end": item["end"],
                    "level": item["level"],
                    "held": item["held"],
                    "refused": item["refused"],
                    "overlaps_a_row": any(why.startswith("overlaps") for why in item["why"]),
                    "crosses_a_wall": "crosses a wall" in item["why"],
                    "why": item["why"],
                }
            )
    kinds = Counter(
        ("overlaps a row" if m["overlaps_a_row"] else "no row")
        + (" and crosses a wall" if m["crosses_a_wall"] else "")
        for m in mutants
    )
    receipt = {
        "program": "fe_layer_reasons.py",
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "uses_sha256": hashlib.sha256(Path(fe.__file__).read_bytes()).hexdigest(),
        "table_sha256": digest,
        "environment": {"python": platform.python_version(), "machine": platform.machine()},
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "cpu_seconds": round(time.process_time() - started, 1),
        "rows": counts,
        "mutants_total": len(mutants),
        "all_refused": all(m["refused"] for m in mutants),
        "kinds": dict(sorted(kinds.items())),
        "wall_crossings": [
            {key: m[key] for key in ("n", "end", "level", "held", "why")}
            for m in mutants
            if m["crosses_a_wall"]
        ],
        "mutants": mutants,
    }
    fe.write_json_lines(out, receipt, "mutants")
    print(json.dumps({key: receipt[key] for key in ("mutants_total", "all_refused", "kinds")}))
    return 0 if receipt["all_refused"] else 1


if __name__ == "__main__":
    sys.exit(main())
