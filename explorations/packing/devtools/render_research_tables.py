#!/usr/bin/env python3
"""Render the research documents' data tables from the structured sources.

The tables are duplicated deliberately: a reader should get the whole picture
from the report alone, without opening the data. Duplication is only safe if it
cannot drift, so the Markdown between the GENERATED markers is written from
`frontier/` rather than by hand.

    uv run --frozen python -m devtools.render_research_tables
    uv run --frozen python -m devtools.render_research_tables --check

`--check` compares parsed cells, not bytes, so it is unaffected by the
Markdown formatter reflowing the surrounding prose.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

import yaml
from strif import atomic_output_file

ROOT = pathlib.Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
MAIN = ROOT / "docs/project/research/research-2026-08-22-packing-11-unit-squares.md"

BEGIN = "<!-- BEGIN GENERATED: %s (devtools.render_research_tables) -->"
END = "<!-- END GENERATED: %s -->"


def load_cases() -> list[dict]:
    out = []
    for f in sorted(FRONTIER.glob("n-*.md")):
        fm = yaml.safe_load(f.read_text(encoding="utf-8").split("---\n")[1])
        out.append(fm["packing"])
    return out


def fmt(x: float, nd: int = 6) -> str:
    return f"{x:.{nd}f}".rstrip("0").rstrip(".")


def pretty(expr: str) -> str:
    """ASCII exact forms are the stored value; this is display only."""
    return re.sub(r"sqrt\((\d+)\)", r"√\1", expr)


LB_LABEL = {
    "area": "area `√n`",
    "perfect_square": "perfect square",
    "nagamochi": "Nagamochi",
    "monotonicity": "monotone",
    "unavoidable_points": "unavoidable points",
    "counting": "elementary",
}
UB_LABEL = {
    "trivial_grid": "grid",
    "hand_construction": "hand",
    "diagonal_strip": "strip",
    "pattern_family": "family",
    "extension": "extension",
    "composition": "composition",
    "simulated_annealing": "annealing",
    "inflation_billiard": "billiard",
    "unknown": "—",
}


def table_frontier(cases: list[dict]) -> list[str]:
    rows = [
        "| `n` | best known `s(n)` | how | deg | best proved lower bound | from | gap |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for c in cases:
        if c["status"] != "open":
            continue
        ub, lb = c["upper_bound"], c["lower_bound"]
        val = (
            ub["exact_form"] if (ub["exact_form"] and not ub["exact_form"].isdigit()) else None
        )
        shown = f"`{pretty(val)}` = {fmt(ub['value'], 8)}" if val else fmt(ub["value"], 8)
        deg = str(ub["algebraic_degree"]) if ub["algebraic_degree"] else "—"
        src = LB_LABEL[lb["kind"]]
        if lb["kind"] == "monotonicity" and lb.get("note"):
            m = re.search(r"s\((\d+)\)", lb["note"])
            if m:
                src = f"monotone from `s({m.group(1)})`"
        rows.append(
            f"| {c['n']} | {shown} | {UB_LABEL[ub['method']]} | {deg} | "
            f"{fmt(lb['value'])} | {src} | {fmt(c['gap'], 4)} |"
        )
    return rows


def table_solved(cases: list[dict]) -> list[str]:
    rows = ["| `n` | `s(n)` | established by | source |", "| --- | --- | --- | --- |"]
    for c in cases:
        if c["status"] != "proved":
            continue
        ub, lb = c["upper_bound"], c["lower_bound"]
        val = pretty(ub["exact_form"]) if ub["exact_form"] else fmt(ub["value"], 8)
        who = ", ".join(lb["proved_by"]) if lb["proved_by"] else "classical"
        yr = f" ({lb['proved_year']})" if lb["proved_year"] else ""
        rows.append(f"| {c['n']} | `{val}` | {LB_LABEL[lb['kind']]} | {who}{yr} |")
    return rows


def table_strategies(kind: str) -> list[str]:
    d = yaml.safe_load((FRONTIER / f"{kind}-strategies.yaml").read_text(encoding="utf-8"))
    head = "Produced records?" if kind == "search" else "Used on this problem?"
    rows = [
        f"| # | Strategy | Family | Mechanism | {head} |",
        "| --- | --- | --- | --- | --- |",
    ]
    for s in d["strategies"]:
        fam = s["family"].replace("_", " ")
        rows.append(f"| {s['id']} | {s['name']} | {fam} | {s['mechanism']} | {s['note']} |")
    return rows


BLOCKER = {
    "unpublished": "unpublished",
    "print_only": "print only",
    "paywall": "paywall",
    "bot_blocked": "bot-blocked",
    "private_correspondence": "private correspondence",
    "obscure_periodical": "obscure periodical",
}


def table_unretrieved() -> list[str]:
    d = yaml.safe_load((FRONTIER / "source-availability.yaml").read_text(encoding="utf-8"))
    rows = [
        "| Source | Year | Where | Obstacle | What rests on it |",
        "| --- | --- | --- | --- | --- |",
    ]
    for s in sorted(d["unretrieved"], key=lambda x: (x["priority"], x["key"])):
        dep = " ".join(s["depends_on_it"].split())
        rows.append(
            f"| **{s['key']}** {s['title']} | {s['year']} | {s['venue']} | "
            f"{BLOCKER[s['blocker']]} | {dep} |"
        )
    return rows


def table_recovered() -> list[str]:
    d = yaml.safe_load((FRONTIER / "source-availability.yaml").read_text(encoding="utf-8"))
    rows = ["| Source | How it was recovered |", "| --- | --- |"]
    for s in d["recovered"]:
        rows.append(f"| **{s['key']}** {s['title']} | {' '.join(s['how'].split())} |")
    return rows


def splice(text: str, name: str, rows: list[str]) -> str:
    b, e = BEGIN % name, END % name
    i, j = text.index(b), text.index(e)
    return text[:i] + b + "\n\n" + "\n".join(rows) + "\n\n" + text[j:]


# The Markdown formatter normalizes typography in place (straight quotes to
# curly, -- to en dash, ... to an ellipsis). That rewrites generated cells, so
# --check compares *content*: both sides are folded back to ASCII punctuation
# first. Anything that actually changes what a cell says still fails.
_FOLD = str.maketrans(
    {
        "\u201c": '"',
        "\u201d": '"',
        "\u2018": "'",
        "\u2019": "'",
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
    }
)


def cells(block: str) -> list[list[str]]:
    out = []
    for line in block.splitlines():
        if not line.startswith("|"):
            continue
        c = [" ".join(x.translate(_FOLD).split()) for x in line.strip().strip("|").split("|")]
        if set("".join(c)) <= set("- "):
            continue
        out.append(c)
    return out


def extract(text: str, name: str) -> str:
    b, e = BEGIN % name, END % name
    return text[text.index(b) + len(b) : text.index(e)]


def tables(cases) -> dict[str, list[str]]:
    """The six generated tables, keyed by the marker name they are rendered between."""
    return {
        "frontier-open": table_frontier(cases),
        "frontier-solved": table_solved(cases),
        "search-strategies": table_strategies("search"),
        "proof-strategies": table_strategies("proof"),
        "sources-unretrieved": table_unretrieved(),
        "sources-recovered": table_recovered(),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    cases = load_cases()
    rendered = tables(cases)
    text = MAIN.read_text(encoding="utf-8")
    missing = [n for n in rendered if (BEGIN % n) not in text]
    if missing:
        print(f"missing generated markers for: {', '.join(missing)}", file=sys.stderr)
        return 2
    if args.check:
        stale = [
            n
            for n, rows in rendered.items()
            if cells(extract(text, n)) != cells("\n".join(rows))
        ]
        if stale:
            print(
                "STALE (re-run `python -m devtools.render_research_tables`): "
                + ", ".join(stale),
                file=sys.stderr,
            )
            return 1
        print(
            f"  {len(rendered)} generated tables match frontier/ "
            f"({sum(len(r) - 2 for r in rendered.values())} data rows)"
        )
        return 0
    for n, rows in rendered.items():
        text = splice(text, n, rows)
    with atomic_output_file(MAIN) as temporary:
        temporary.write_text(text, encoding="utf-8")
    print(f"rendered {len(rendered)} tables into {MAIN.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
