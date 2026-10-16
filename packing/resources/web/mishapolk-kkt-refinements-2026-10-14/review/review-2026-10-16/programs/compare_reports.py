"""Compare two third-route JSON reports field by field, apart from this run's own times.

Written in the fix round of PR #648 to hold the kept driver's re-run to the report the
review lane wrote. It ignores only `wall_seconds`, `started_utc` and `finished_utc`,
wherever they occur (the run's and each certificate's times), and compares every other
field, the receipts' recorded seconds among them. It decides nothing. From ``packing/``::

    python -I PROGRAMS/compare_reports.py ORIGINAL.json RERUN.json
"""

from __future__ import annotations

import json
import sys

TIMES = frozenset({"wall_seconds", "started_utc", "finished_utc"})


def differences(a: object, b: object, path: str, out: list[str]) -> None:
    if type(a) is not type(b):
        out.append(f"{path}: {type(a).__name__} against {type(b).__name__}")
    elif isinstance(a, dict):
        assert isinstance(b, dict)
        for key in sorted(set(a) | set(b)):
            if key in TIMES:
                continue
            if key not in a or key not in b:
                out.append(f"{path}/{key}: in one report only")
            else:
                differences(a[key], b[key], f"{path}/{key}", out)
    elif isinstance(a, list):
        assert isinstance(b, list)
        if len(a) != len(b):
            out.append(f"{path}: {len(a)} items against {len(b)}")
            return
        for index, (x, y) in enumerate(zip(a, b, strict=True)):
            differences(x, y, f"{path}[{index}]", out)
    elif a != b:
        out.append(f"{path}: {str(a)[:60]} against {str(b)[:60]}")


def main(argv: list[str]) -> int:
    with open(argv[0], encoding="utf-8") as one, open(argv[1], encoding="utf-8") as two:
        original, rerun = json.load(one), json.load(two)
    found: list[str] = []
    differences(original, rerun, "", found)
    print(f"ignored: {', '.join(sorted(TIMES))}")
    print(f"certificates: {len(original['rows'])} and {len(rerun['rows'])}")
    print(f"wall seconds: {original['wall_seconds']} and {rerun['wall_seconds']}")
    print(f"differences in every other field: {len(found)}")
    for line in found[:50]:
        print(f"  {line}")
    return 1 if found else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
