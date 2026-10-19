"""Account for every native_decide fact of sq19's final theorem, by where its module lives.

Reads expected/axioms.txt.gz, the retained Lean sources, and the JSON outputs of
scan_archives.py for the five release archives, and reports how many of the 4,320
native facts are proved in the Git tree, how many only in the archives, how many in
both (tracked files the archives also carry), whether any is found nowhere, and which
native theorems are in the build but not in the final axiom set.

    python -I count_native.py SQ19_DIR SCAN_JSON... [--json OUT]

Standard library only.
"""

import argparse
import glob
import gzip
import json
import re
import sys

THEOREM = re.compile(r"(?m)^(?:private\s+)?theorem\s+(\S+)")
NAMESPACE = re.compile(r"(?m)^(namespace|end)[ \t]+(\S+)")


def strip_comments(text):
    text = re.sub(r"/-.*?-/", "", text, flags=re.S)
    return re.sub(r"--[^\n]*", "", text)


def native_theorems(text):
    out, ns = [], []
    events = sorted([(m.start(), "ns", m) for m in NAMESPACE.finditer(text)]
                    + [(m.start(), "thm", m) for m in THEOREM.finditer(text)], key=lambda e: e[0])
    starts = [e[0] for e in events] + [len(text)]
    for k, (pos, kind, m) in enumerate(events):
        if kind == "ns":
            if m.group(1) == "namespace":
                ns.append(m.group(2))
            elif ns:
                ns.pop()
        elif "native_decide" in text[pos:starts[k + 1]]:
            out.append(".".join([*ns, m.group(1)]))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("sq19")
    ap.add_argument("scans", nargs="+")
    ap.add_argument("--json")
    a = ap.parse_args()
    ax = {x.split("._native")[0] for x in gzip.open(a.sq19 + "/expected/axioms.txt.gz", "rt", encoding="utf-8").read().split()
          if "native_decide" in x}
    tree = set()
    for p in glob.glob(a.sq19 + "/Sq19Lean/**/*.lean", recursive=True) + glob.glob(a.sq19 + "/s19/**/*.lean", recursive=True):
        tree.update(native_theorems(strip_comments(open(p, encoding="utf-8").read())))
    archived = set()
    for s in a.scans:
        archived.update(json.load(open(s, encoding="utf-8"))["native_names"])
    in_tree = ax & tree
    in_archives = (ax & archived) - tree
    missing = ax - tree - archived
    res = {"native_facts": len(ax), "in_git_tree": len(in_tree), "in_archives_only": len(in_archives),
           "found_nowhere": sorted(missing), "both_tree_and_archive": len(ax & tree & archived),
           "native_theorems_not_in_axioms": sorted((tree | archived) - ax)}
    print(f"{len(ax)} native facts: {len(in_tree)} in the Git tree, {len(in_archives)} only in the archives, "
          f"{len(missing)} found nowhere; {res['both_tree_and_archive']} in both (tracked files the archives also carry)")
    print(f"native theorems in the build but not in the final axioms: {res['native_theorems_not_in_axioms']}")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=1)
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
