"""What issue #1009 states, read from its saved REST response. Decides nothing.

Lane c-review-1009-1117, stage 4 blind review of issue #1009. Clean-room.

The issue's body holds three tables keyed by ``| **n** |`` rows: Part A and Part B give
each count's claimed side at 12 places, the standing bound it names and the gain; the
certificate table gives the two files' SHA-256, the least wall and pair margins and the
pair counts. This module returns them as text, exactly as written.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROW = re.compile(r"^\|\s*\*\*(\d+)\*\*\s*\|(.*)\|\s*$")
HEX64 = re.compile(r"[0-9a-f]{64}")
DECIMAL = re.compile(r"\d+\.\d{12}")


def _cells(rest: str) -> list[str]:
    return [cell.strip().strip("`").strip() for cell in rest.split("|")]


def read_issue(path: str) -> dict:
    """``{"claims": {n: {...}}, "files": {n: {...}}, "created_at": ..., "body_sha256": ...}``."""
    raw = Path(path).read_bytes()
    doc = json.loads(raw)
    body = doc["body"]
    claims: dict[int, dict] = {}
    files: dict[int, dict] = {}
    part = None
    for line in body.split("\n"):
        line = line.rstrip("\r")
        if line.startswith("### Part A"):
            part = "A"
        elif line.startswith("### Part B"):
            part = "B"
        match = ROW.match(line)
        if match is None:
            continue
        n = int(match.group(1))
        cells = _cells(match.group(2))
        if HEX64.fullmatch(cells[0]) and len(cells) >= 6:
            if n in files:
                msg = f"issue: two certificate rows for {n}"
                raise ValueError(msg)
            files[n] = {
                "cert_sha256": cells[0],
                "yaml_sha256": cells[1],
                "min_wall": cells[2],
                "min_pair": cells[3],
                "close_pairs": cells[4],
                "all_pairs": cells[5],
            }
        elif DECIMAL.fullmatch(cells[0]) and len(cells) >= 3:
            if n in claims:
                msg = f"issue: two claim rows for {n}"
                raise ValueError(msg)
            claims[n] = {
                "part": part,
                "claim": cells[0],
                "standing": cells[1],
                "gain": cells[2],
                "competing": cells[3] if len(cells) > 3 else None,
            }
        else:
            msg = f"issue: a row for {n} is of no known table"
            raise ValueError(msg)
    return {
        "number": doc["number"],
        "created_at": doc["created_at"],
        "updated_at": doc["updated_at"],
        "author": doc["user"]["login"],
        "claims": claims,
        "files": files,
    }
