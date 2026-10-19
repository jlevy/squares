#!/usr/bin/env python3
"""What cfcheck shares with the producer's checker: files, crates and copied code.

wand125's README for ``indep-checker/`` says cfcheck was written from SPEC.md and the
published bundles only and shares no code with ``replay4d``, ``seam4d_core`` or
``validate_family.py``. That is a statement about how it was written, which no program
here can check. What can be checked is the code: this program compares the retained
cfcheck tree with the retained producer tree (``checker/`` and ``structure/`` of the
9a28a84 packet) and reports

- **files**: every file of one tree whose SHA-256 equals a file of the other;
- **crates**: cfcheck's path dependencies, and the crates the two ``Cargo.lock`` files
  both pin, each marked as a registry crate or a local one;
- **lines**: source lines of at least 40 non-blank characters, comments removed and
  whitespace collapsed, that occur in both trees;
- **token runs**: the longest runs of identical tokens (comments removed) that a cfcheck
  file shares with a producer file, found from shared 12-token windows, and the share of
  cfcheck's 25-token windows that occur anywhere in the producer; then the same with
  every identifier and literal replaced by a placeholder, which finds code copied and
  renamed;
- **names and comments**: the function names and the comment texts both trees use.

Two kinds of control calibrate the numbers. **Baselines**: the same token measures
between cfcheck and Rust checkers that share no author with it, Evan Daniel's ``zmx2``
and ``verify2`` and this repository's ``sqverify_exact``, and between the producer and
those, show how much two unrelated exact checkers share by convention. **A positive
control**: the producer's ``wmin`` from ``seam4d_core/src/lib.rs`` appended to a copy of
cfcheck's ``geom.rs``, verbatim and then renamed, must be found by the plain and the
renamed measure; the program fails if it is not.

Run from ``packing/`` with the project interpreter::

    uv run --frozen --all-extras --group dev python -I \\
        resources/web/wand125-closed-form-cfcheck-2026-10-14/comparison/shared_code.py \\
        --out \\
        resources/web/wand125-closed-form-cfcheck-2026-10-14/comparison/outputs/shared-code.json

It decides nothing about the certificate, and nothing about what cfcheck's authors read.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tomllib
from collections import defaultdict
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
WEB = PACKET.parent
PACKING = WEB.parents[1]
CFCHECK = PACKET / "square-packing/problems/closed-form/indep-checker"
PRODUCER_ROOT = WEB / "wand125-closed-form-2026-10-14/square-packing/problems/closed-form"
PRODUCER = (PRODUCER_ROOT / "checker", PRODUCER_ROOT / "structure")
BASELINES = {
    "evand-zmx2": WEB / "evand-zmx2-sym-atoms-2026-09-30/square-packing/s12/verify2/src",
    "evand-verify2": WEB / "evand-square-packing-2026-09-26/square-packing/s12/verify2/src",
    "sqverify_exact": PACKING / "sqverify_exact/src",
}
CONTROL_SOURCE = PRODUCER_ROOT / "checker/seam4d_core/src/lib.rs"
CONTROL_FUNCTION = "wmin"
CONTROL_HOST = CFCHECK / "src/geom.rs"

LINE_MIN = 40
WINDOW = 12
SHARE_WINDOW = 25
RUN_REPORT = 30
GENERIC = 50
KEYWORDS = frozenset(
    [
        *("as", "break", "const", "continue", "crate", "else", "enum", "extern", "false", "fn"),
        *(
            "for",
            "if",
            "impl",
            "in",
            "let",
            "loop",
            "match",
            "mod",
            "move",
            "mut",
            "pub",
            "ref",
        ),
        *("return", "self", "Self", "static", "struct", "super", "trait", "true", "type"),
        *("unsafe", "use", "where", "while", "dyn", "async", "await"),
    ]
)
TOKEN = re.compile(
    r"""r\#*"(?:[^"]|"(?!\#))*"\#*"""  # raw strings
    r"""|b?"(?:\\.|[^"\\])*\""""  # strings
    r"""|'(?:\\.|[^'\\])'"""  # chars
    r"""|[A-Za-z_][A-Za-z0-9_]*"""  # identifiers and keywords
    r"""|0x[0-9a-fA-F_]+"""
    r"""|\d[\d_]*(?:\.\d[\d_]*)?(?:[eE][+-]?\d+)?(?:[iu](?:8|16|32|64|128|size)|f32|f64)?"""
    r"""|::|->|=>|==|!=|<=|>=|&&|\|\||\.\.=?|[+\-*/%^&|]=|<<=?|>>=?"""
    r"""|\S"""
)
CHAR_LITERAL = re.compile(r"'(?:\\.[^']{0,8}|[^'\\])'")

type Json = dict[str, Any]


def emit(line: str) -> None:
    sys.stdout.write(line + "\n")


def files(roots: tuple[Path, ...] | list[Path]) -> list[Path]:
    found = (p for root in roots for p in root.rglob("*"))
    return sorted(p for p in found if p.is_file() and "__pycache__" not in p.parts)


def label(path: Path) -> str:
    return path.relative_to(PACKING.parent).as_posix()


def strip_comments(text: str, *, python: bool) -> tuple[str, list[str]]:
    """The code with comments removed (line structure kept), and the comment texts."""
    comments: list[str] = []
    out: list[str] = []
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        literal = CHAR_LITERAL.match(text, i) if not python and c == "'" else None
        quote = text[i : i + 3] if python and text[i : i + 3] in {'"""', "'''"} else None
        if literal:
            out.append(literal.group(0))
            i = literal.end()
        elif quote:
            j = text.find(quote, i + 3)
            j = n if j < 0 else j + 3
            out.append(text[i:j])
            i = j
        elif c == '"' or (python and c == "'"):
            j = i + 1
            while j < n and text[j] not in {c, "\n"}:
                j += 2 if text[j] == "\\" else 1
            out.append(text[i : j + 1])
            i = j + 1
        elif (python and c == "#") or (not python and text.startswith("//", i)):
            j = text.find("\n", i)
            j = n if j < 0 else j
            comments.append(text[i:j].lstrip("#/! ").strip())
            i = j
        elif not python and text.startswith("/*", i):
            j = text.find("*/", i + 2)
            j = n if j < 0 else j + 2
            comments.append(" ".join(text[i:j].strip("/*! ").split()))
            out.append("\n" * text.count("\n", i, j))
            i = j
        else:
            out.append(c)
            i += 1
    return "".join(out), [c for c in comments if c]


class Source:
    """One source file: its normalized lines, its tokens with line numbers, its names."""

    def __init__(self, path: Path, text: str | None = None) -> None:
        self.path = path
        raw = path.read_text(encoding="utf-8", errors="replace") if text is None else text
        self.rust = path.suffix == ".rs"
        code, self.comments = strip_comments(raw, python=path.suffix == ".py")
        self.lines = [" ".join(line.split()) for line in code.splitlines()]
        self.tokens: list[tuple[str, int]] = []
        for number, line in enumerate(code.splitlines(), start=1):
            self.tokens.extend((m.group(0), number) for m in TOKEN.finditer(line))
        self.functions = set(re.findall(r"\b(?:fn|def)\s+([A-Za-z_][A-Za-z0-9_]*)", code))

    def stream(self, *, renamed: bool) -> list[str]:
        if not renamed:
            return [t for t, _ in self.tokens]
        out: list[str] = []
        for t, _ in self.tokens:
            if t in KEYWORDS or not (t[0].isalnum() or t[0] in "_\"'"):
                out.append(t)
            else:
                out.append("ID" if t[0].isalpha() or t[0] == "_" else "LIT")
        return out


def longest_runs(a: Source, b: Source, *, renamed: bool) -> list[Json]:
    """Maximal runs of equal tokens between two files, longest first.

    Every pair of equal ``WINDOW``-token windows seeds a run, which is extended both ways
    along its diagonal (the offset between the two files) to its maximal length; a seed
    inside a run already found on its diagonal is skipped, so each run is reported once.
    A window that occurs more than ``GENERIC`` times in the other file seeds nothing, since
    it is boilerplate; a run through it is still found from any other window it holds.
    """
    sa, sb = a.stream(renamed=renamed), b.stream(renamed=renamed)
    seeds: dict[tuple[str, ...], list[int]] = defaultdict(list)
    for j in range(len(sb) - WINDOW + 1):
        seeds[tuple(sb[j : j + WINDOW])].append(j)
    found: dict[int, list[tuple[int, int]]] = defaultdict(list)
    runs: list[Json] = []
    for i in range(len(sa) - WINDOW + 1):
        matches = seeds.get(tuple(sa[i : i + WINDOW]), [])
        if len(matches) > GENERIC:
            continue
        for j in matches:
            if any(lo <= i < hi for lo, hi in found[i - j]):
                continue
            lo_i, lo_j = i, j
            while lo_i > 0 and lo_j > 0 and sa[lo_i - 1] == sb[lo_j - 1]:
                lo_i, lo_j = lo_i - 1, lo_j - 1
            hi_i, hi_j = i + WINDOW, j + WINDOW
            while hi_i < len(sa) and hi_j < len(sb) and sa[hi_i] == sb[hi_j]:
                hi_i, hi_j = hi_i + 1, hi_j + 1
            found[i - j].append((lo_i, hi_i))
            runs.append(
                {
                    "tokens": hi_i - lo_i,
                    "cfcheck_lines": f"{a.tokens[lo_i][1]}-{a.tokens[hi_i - 1][1]}",
                    "other_lines": f"{b.tokens[lo_j][1]}-{b.tokens[hi_j - 1][1]}",
                    "text": " ".join(t for t, _ in a.tokens[lo_i:hi_i])[:240],
                }
            )
    runs.sort(key=lambda r: -r["tokens"])
    return runs


def windows(sources: list[Source], *, renamed: bool) -> set[tuple[str, ...]]:
    out: set[tuple[str, ...]] = set()
    for s in sources:
        stream = s.stream(renamed=renamed)
        last = len(stream) - SHARE_WINDOW + 1
        out.update(tuple(stream[i : i + SHARE_WINDOW]) for i in range(last))
    return out


def token_measures(
    mine: list[Source], other: list[Source], *, renamed: bool, keep_runs: bool = True
) -> Json:
    theirs = windows(other, renamed=renamed)
    total = hits = 0
    for s in mine:
        stream = s.stream(renamed=renamed)
        for i in range(len(stream) - SHARE_WINDOW + 1):
            total += 1
            hits += tuple(stream[i : i + SHARE_WINDOW]) in theirs
    best = [
        {"cfcheck_file": label(a.path), "other_file": label(b.path), **run}
        for a in mine
        for b in other
        for run in longest_runs(a, b, renamed=renamed)[:3]
    ]
    best.sort(key=lambda r: -r["tokens"])
    return {
        "windows": total,
        "windows_found_in_other": hits,
        "share": round(hits / total, 5) if total else 0.0,
        "longest_run_tokens": best[0]["tokens"] if best else 0,
        "runs_at_least_report_length": sum(r["tokens"] >= RUN_REPORT for r in best),
        "longest_runs": (
            [r for r in best if r["tokens"] >= RUN_REPORT] or best[:3]
            if keep_runs
            else best[:1]
        ),
    }


def compare(mine: list[Source], other: list[Source]) -> Json:
    """Every measure between one set of sources and another."""

    def long_lines(sources: list[Source]) -> set[str]:
        return {x for s in sources for x in s.lines if len(x.replace(" ", "")) >= LINE_MIN}

    def long_comments(sources: list[Source]) -> set[str]:
        return {c for s in sources for c in s.comments if len(c) >= 20}

    names_mine: set[str] = set().union(*(s.functions for s in mine))
    names_other: set[str] = set().union(*(s.functions for s in other))
    return {
        "plain": token_measures(mine, other, renamed=False),
        "renamed": token_measures(mine, other, renamed=True),
        "shared_lines": sorted(long_lines(mine) & long_lines(other)),
        "shared_function_names": sorted(names_mine & names_other),
        "shared_comments": sorted(long_comments(mine) & long_comments(other)),
    }


def lock_crates(path: Path) -> dict[str, str]:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    packages: list[Json] = data.get("package", [])
    return {p["name"]: ("registry" if "source" in p else "local") for p in packages}


def control_texts() -> tuple[str, str]:
    """cfcheck's geom.rs with the producer's ``wmin`` appended, verbatim and renamed."""
    source = CONTROL_SOURCE.read_text(encoding="utf-8")
    start = source.index(f"pub fn {CONTROL_FUNCTION}(")
    depth, stop = 0, len(source)
    for k in range(source.index("{", start), len(source)):
        depth += {"{": 1, "}": -1}.get(source[k], 0)
        if depth == 0:
            stop = k + 1
            break
    function = source[start:stop]
    renamed = (
        function.replace(CONTROL_FUNCTION, "min_width_ctl")
        .replace("u0", "lo_ctl")
        .replace("u1", "hi_ctl")
    )
    host = CONTROL_HOST.read_text(encoding="utf-8")
    return f"{host}\n{function}\n", f"{host}\n{renamed}\n"


def summary_line(name: str, base: Json) -> str:
    cf, pr = base["cfcheck_vs_baseline"], base["producer_vs_baseline"]
    return (
        f"baseline {name}: cfcheck longest runs plain {cf['plain']['longest_run_tokens']},"
        f" renamed {cf['renamed']['longest_run_tokens']}; producer plain"
        f" {pr['plain']['longest_run_tokens']}, renamed {pr['renamed']['longest_run_tokens']}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)

    cf_files = files([CFCHECK])
    producer_files = files(PRODUCER)
    digest = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in cf_files + producer_files}
    producer_by_digest = {digest[p]: p for p in producer_files}
    identical = [
        {"cfcheck": label(p), "producer": label(producer_by_digest[digest[p]])}
        for p in cf_files
        if digest[p] in producer_by_digest
    ]
    manifest = tomllib.loads((CFCHECK / "Cargo.toml").read_text(encoding="utf-8"))
    deps: dict[str, Any] = manifest.get("dependencies", {})
    path_deps = sorted(
        n for n, spec in deps.items() if isinstance(spec, dict) and "path" in spec
    )
    ours = lock_crates(CFCHECK / "Cargo.lock")
    theirs = lock_crates(PRODUCER_ROOT / "checker/Cargo.lock")
    shared_crates = {name: ours[name] for name in sorted(set(ours) & set(theirs))}

    cf_sources = [Source(p) for p in cf_files if p.suffix == ".rs"]
    producer_sources = [Source(p) for p in producer_files if p.suffix in {".rs", ".py"}]
    producer_rust = [s for s in producer_sources if s.rust]
    against = compare(cf_sources, producer_sources)
    baselines: Json = {}
    for name, root in BASELINES.items():
        base = [Source(p) for p in files([root]) if p.suffix == ".rs"]
        baselines[name] = {
            "files": [label(s.path) for s in base],
            "cfcheck_vs_baseline": {
                "plain": token_measures(cf_sources, base, renamed=False, keep_runs=False),
                "renamed": token_measures(cf_sources, base, renamed=True, keep_runs=False),
            },
            "producer_vs_baseline": {
                "plain": token_measures(producer_rust, base, renamed=False, keep_runs=False),
                "renamed": token_measures(producer_rust, base, renamed=True, keep_runs=False),
            },
        }
    verbatim, renamed = control_texts()
    plain_hit = token_measures([Source(CONTROL_HOST, verbatim)], producer_rust, renamed=False)
    renamed_hit = token_measures([Source(CONTROL_HOST, renamed)], producer_rust, renamed=True)
    control = {
        "pasted": (
            f"{label(CONTROL_SOURCE)}: pub fn {CONTROL_FUNCTION}, appended to a copy of"
            f" {label(CONTROL_HOST)}; renamed: wmin, u0 and u1 replaced"
        ),
        "verbatim_longest_run": plain_hit["longest_runs"][0],
        "renamed_longest_run": renamed_hit["longest_runs"][0],
        "found": min(plain_hit["longest_run_tokens"], renamed_hit["longest_run_tokens"])
        >= RUN_REPORT,
    }
    verdict = {
        "identical_files": len(identical),
        "path_dependencies": len(path_deps),
        "shared_local_crates": [n for n, kind in shared_crates.items() if kind == "local"],
        "longest_plain_run_tokens": against["plain"]["longest_run_tokens"],
        "longest_renamed_run_tokens": against["renamed"]["longest_run_tokens"],
        "plain_window_share": against["plain"]["share"],
        "renamed_window_share": against["renamed"]["share"],
        "shared_lines": len(against["shared_lines"]),
        "shared_comments": len(against["shared_comments"]),
        "positive_control_found": control["found"],
    }
    result: Json = {
        "schema": "cfcheck-shared-code/v1",
        "cfcheck": label(CFCHECK),
        "producer": [label(p) for p in PRODUCER],
        "cfcheck_files": len(cf_files),
        "producer_files": len(producer_files),
        "parameters": {
            "line_min_chars": LINE_MIN,
            "seed_window_tokens": WINDOW,
            "share_window_tokens": SHARE_WINDOW,
            "generic_window_occurrences": GENERIC,
        },
        "verdict": verdict,
        "identical_files": identical,
        "cfcheck_path_dependencies": path_deps,
        "cfcheck_dependencies": sorted(deps),
        "producer_lock_crates": sorted(theirs),
        "shared_lock_crates": shared_crates,
        "against_producer": against,
        "baselines": baselines,
        "positive_control": control,
    }
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    for key, value in verdict.items():
        emit(f"{key}: {value}")
    for name, base in baselines.items():
        emit(summary_line(name, base))
    if not control["found"]:
        emit("POSITIVE CONTROL NOT FOUND")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
