"""Compare two zmx2.rs versions item by item (top-level `fn` items).

Prints, for each top-level fn name, whether it is only in A, only in B, identical, or
changed (with the changed line count). Reads the two files named as arguments and
decides nothing about either; it locates what a reader has to read.

Usage: python3 -I zmx2_fn_diff.py A.rs B.rs [--show NAME ...]
"""

import difflib
import re
import sys

FN = re.compile(r"^(?:pub )?fn ([A-Za-z0-9_]+)")


def items(path: str) -> dict[str, list[str]]:
    lines = open(path, encoding="utf-8").read().splitlines()
    out: dict[str, list[str]] = {}
    name, buf = "<prelude>", []
    for line in lines:
        m = FN.match(line)
        if m:
            out.setdefault(name, []).extend(buf)
            name, buf = m.group(1), []
            while name in out:
                name += "#2"
        buf.append(line)
    out.setdefault(name, []).extend(buf)
    return out


def main() -> None:
    a, b = items(sys.argv[1]), items(sys.argv[2])
    show = sys.argv[sys.argv.index("--show") + 1 :] if "--show" in sys.argv else []
    if show:
        for name in show:
            for line in difflib.unified_diff(
                a.get(name, []), b.get(name, []), f"A:{name}", f"B:{name}", lineterm="", n=2
            ):
                print(line)
        return
    for name in sorted(set(a) | set(b), key=lambda n: (n not in a, n)):
        if name not in b:
            print(f"ONLY-A   {name}")
        elif name not in a:
            print(f"ONLY-B   {name} ({len(b[name])} lines)")
        elif a[name] == b[name]:
            print(f"SAME     {name}")
        else:
            d = [
                line
                for line in difflib.unified_diff(a[name], b[name], lineterm="", n=0)
                if line[:1] in "+-" and line[:3] not in ("+++", "---")
            ]
            print(f"CHANGED  {name} ({len(d)} diff lines)")


main()
