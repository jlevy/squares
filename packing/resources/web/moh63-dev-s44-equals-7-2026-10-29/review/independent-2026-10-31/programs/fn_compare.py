"""Compare two Rust files function by function (reviewer scratch tool, bold-ritchie-rev3).

Extracts every `fn NAME(` item with its body by brace matching (string/char literals and
comments are skipped crudely but adequately for this code), and reports for each name in
OLD whether NEW has a byte-identical body, a changed body, or none.

Usage: python -I fn_compare.py OLD.rs NEW.rs
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

FN = re.compile(r"^\s*(?:pub\s+)?fn\s+([A-Za-z_][A-Za-z0-9_]*)", re.M)


def functions(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for m in FN.finditer(text):
        name = m.group(1)
        i = text.index("{", m.end())
        depth, j = 0, i
        while True:
            c = text[j]
            if c == "/" and text[j + 1] == "/":
                j = text.index("\n", j)
                continue
            if c == '"':
                j += 1
                while text[j] != '"':
                    j += 2 if text[j] == "\\" else 1
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        key = name
        k = 2
        while key in out:
            key = f"{name}#{k}"
            k += 1
        out[key] = text[m.start() : j + 1]
    return out


def main(old: Path, new: Path) -> int:
    a, b = functions(old.read_text()), functions(new.read_text())
    same = [n for n in a if n in b and a[n] == b[n]]
    changed = [n for n in a if n in b and a[n] != b[n]]
    gone = [n for n in a if n not in b]
    added = [n for n in b if n not in a]
    print(f"old {len(a)} fns, new {len(b)} fns: identical {len(same)}, changed {len(changed)}, removed {len(gone)}, added {len(added)}")
    print("changed:", ", ".join(changed))
    print("removed:", ", ".join(gone))
    print("added:", ", ".join(added))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2])))
