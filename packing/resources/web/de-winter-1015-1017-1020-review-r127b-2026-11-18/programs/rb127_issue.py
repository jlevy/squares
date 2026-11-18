"""The numbers each issue states, read from its saved REST response (lane r127b-1118).

Decides nothing. Reads only the issue's title and body, never its comments. Each value
is the text as the issue prints it; the check program compares them with the files.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def _all(pattern: str, text: str) -> list[str]:
    return re.findall(pattern, text)


def _one(pattern: str, text: str) -> str | None:
    m = re.search(pattern, text)
    return m.group(1) if m else None


def read_issue(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    body = data["body"].replace("\r\n", "\n")
    title = data["title"]
    out: dict[str, Any] = {
        "number": data["number"],
        "title": title,
        "created_at": data["created_at"],
        "updated_at": data["updated_at"],
        "author": data["user"]["login"],
        "comments_count_at_fetch": data["comments"],
        "title_side_print": _one(r"\(side ([0-9]+\.[0-9]+)\)", title),
        "claim_print_rounded_up": _one(r"square of side ([0-9]+\.[0-9]+) \(rounded up at 12 places\)", body),
        "claim_exact": _one(r"side exactly ([0-9]+/[0-9]+) =", body),
        "claim_exact_decimal": _one(r"side exactly [0-9]+/[0-9]+ = ([0-9]+\.[0-9]+)", body),
        "house_print": _one(r"lists ([0-9]+\.[0-9]+) \(T-305", body),
        "gain_print": _one(r"The gain is ([0-9.]+)\.", body),
        "commit": _one(r"at commit ([0-9a-f]{40})", body),
        "close_pairs": [int(v) for v in _all(r"reports 127 squares and ([0-9]+) close pairs", body)],
        "kaggle_side": _one(r"Luka Cvetkovic reported ([0-9]+\.[0-9]+) for n = 127", body),
        "kaggle_difference_print": _one(r"([0-9.]+(?:e-[0-9]+)?) below (?:this packing|that value)", body),
        "kaggle_difference_sense": (
            "kaggle below this packing" if "below this packing" in body
            else "this packing below kaggle" if "below that value" in body else None
        ),
        "band_squares": _one(r"tilted central band of ([0-9]+) squares", body),
        "later_commits_unchanged_stated": "Later commits leave these files unchanged" in body,
        "files_named": sorted(set(_all(r"`(n127/[A-Za-z0-9_.]+)`", body))),
        "ai_statement": _one(r"\*\*AI assistance\.\*\* (.+)", body),
    }
    return out
