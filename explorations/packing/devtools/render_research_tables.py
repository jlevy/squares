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
from decimal import Decimal

import yaml
from strif import atomic_output_file

from sqpack.assurance import bounds_agree_at_declared_precision

ROOT = pathlib.Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
MAIN = ROOT / "docs/project/research/research-2026-08-22-packing-11-unit-squares.md"
STATUS = FRONTIER / "STATUS.md"

BEGIN = "<!-- BEGIN GENERATED: %s (devtools.render_research_tables) -->"
END = "<!-- END GENERATED: %s -->"


def load_cases() -> list[dict]:
    out = []
    for f in sorted(FRONTIER.glob("n-*.md")):
        fm = yaml.safe_load(f.read_text(encoding="utf-8").split("---\n")[1])
        out.append(fm["packing"])
    return out


def load_evidence() -> dict[str, dict]:
    document = yaml.safe_load((FRONTIER / "evidence.yaml").read_text(encoding="utf-8"))
    return {record["id"]: record for record in document["evidence"]}


def fmt(x: object, nd: int = 6) -> str:
    return f"{Decimal(str(x)):.{nd}f}".rstrip("0").rstrip(".")


def pretty(expr: str) -> str:
    """ASCII exact forms are the stored value; this is display only."""
    return re.sub(r"sqrt\((\d+)\)", r"√\1", expr)


LB_LABEL = {
    "area": "area `√n`",
    "perfect-square": "perfect square",
    "nagamochi": "Nagamochi",
    "monotonicity": "monotone",
    "unavoidable-points": "unavoidable points",
    "counting": "elementary",
}
UB_LABEL = {
    "trivial-grid": "grid",
    "hand-construction": "hand",
    "diagonal-strip": "strip",
    "pattern-family": "family",
    "extension": "extension",
    "composition": "composition",
    "simulated-annealing": "annealing",
    "inflation-billiard": "billiard",
    "unknown": "—",
}


def table_frontier(cases: list[dict]) -> list[str]:
    rows = [
        "| `n` | best reported `s(n)` | how | deg | reported lower bound | from | gap |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for c in cases:
        if c["reported_status"] != "open":
            continue
        ub, lb = c["reported_upper_bound"], c["reported_lower_bound"]
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
            f"| {c['n']} | {shown} | {UB_LABEL[ub['construction_method']]} | {deg} | "
            f"{fmt(lb['value'])} | {src} | "
            f"{fmt(Decimal(ub['value']) - Decimal(lb['value']), 4)} |"
        )
    return rows


def table_solved(cases: list[dict]) -> list[str]:
    rows = [
        "| `n` | reported `s(n)` | reported basis | source | formal lane |",
        "| --- | --- | --- | --- | --- |",
    ]
    for c in cases:
        if c["reported_status"] != "proved":
            continue
        ub, lb = c["reported_upper_bound"], c["reported_lower_bound"]
        val = pretty(ub["exact_form"]) if ub["exact_form"] else fmt(ub["value"], 8)
        who = ", ".join(lb["proved_by"]) if lb["proved_by"] else "classical"
        yr = f" ({lb['proved_year']})" if lb["proved_year"] else ""
        formal = "proved" if c["status"] == "proved" else "proof audit pending"
        rows.append(f"| {c['n']} | `{val}` | {LB_LABEL[lb['kind']]} | {who}{yr} | {formal} |")
    return rows


ORIGIN_LABEL = {
    "external": "external proof",
    "independently-external": "independent external",
    "replayed-here": "replayed here",
    "audited-here": "audited here",
}


def compact_bound(bound: dict) -> str:
    """Render one bound without discarding any declared decimal information."""
    exact = bound.get("exact_form")
    if isinstance(exact, str) and len(exact) <= 28:
        return f"`{pretty(exact)}`"
    return f"`{bound['value']}`"


def verification_origins(case: dict, evidence: dict[str, dict]) -> str:
    refs = [
        *case["verified_upper_bound"]["evidence"],
        *case["verified_lower_bound"]["evidence"],
    ]
    origins = [evidence[ref].get("origin") for ref in refs]
    labels = [ORIGIN_LABEL[origin] for origin in origins if origin in ORIGIN_LABEL]
    return ", ".join(dict.fromkeys(labels)) or "—"


def same_bound(left: dict, right: dict) -> bool:
    """Delegate the shared assurance-level representation comparison."""
    return bounds_agree_at_declared_precision(left, right)


def case_disposition(case: dict) -> str:
    notes = []
    if not same_bound(case["reported_upper_bound"], case["verified_upper_bound"]):
        notes.append("formal upper trails report")
    if not same_bound(case["reported_lower_bound"], case["verified_lower_bound"]):
        notes.append("formal lower differs from report")
    if case["reported_status"] != case["status"]:
        notes.append("proof audit pending")
    if case["conflicts"]:
        notes.append(f"{len(case['conflicts'])} conflict")
    return "; ".join(notes) or "—"


def render_status(cases: list[dict], evidence: dict[str, dict]) -> str:
    rows = [
        (
            "<!-- GENERATED by devtools.render_research_tables from frontier/n-*.md and "
            "evidence.yaml. Do not edit by hand. -->"
        ),
        "",
        "# Current Square-Packing Frontier",
        "",
        (
            "This is the reader-first view of every tracked case through `n = 100`. "
            "Reported columns preserve what the declared public sources say. Verified "
            "columns contain only exact formal bounds: a complete proof, an exact "
            "algebraic replay, or a rigorous certificate. A finite-precision result is "
            "*numerically checked* and does not enter a verified column, even at "
            "extremely small tolerance."
        ),
        "",
        (
            "Follow the `n` link for full provenance, numerical evidence, conflicts, "
            "and blockers. See [the frontier guide](README.md) for the contract and "
            "[`evidence.yaml`](evidence.yaml) for the typed evidence register."
        ),
        "",
        (
            "| `n` | reported upper | verified upper | reported lower | verified lower | "
            "formal status | verification origin | gap or conflict | reviewed |"
        ),
        "| ---: | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for case in cases:
        n = case["n"]
        rows.append(
            f"| [`{n}`](n-{n:03d}.md) | {compact_bound(case['reported_upper_bound'])} | "
            f"{compact_bound(case['verified_upper_bound'])} | "
            f"{compact_bound(case['reported_lower_bound'])} | "
            f"{compact_bound(case['verified_lower_bound'])} | {case['status']} | "
            f"{verification_origins(case, evidence)} | {case_disposition(case)} | "
            f"{case['source_reviewed']} |"
        )
    rows.extend(
        [
            "",
            "<!-- This document follows common-doc-guidelines.md.",
            "See github.com/jlevy/practical-prose and review guidelines before editing.",
            "-->",
            "",
        ]
    )
    return "\n".join(rows)


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
    evidence = load_evidence()
    rendered = tables(cases)
    status = render_status(cases, evidence)
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
        if not STATUS.exists() or STATUS.read_text(encoding="utf-8") != status:
            print(
                "STALE (re-run `python -m devtools.render_research_tables`): "
                "frontier/STATUS.md",
                file=sys.stderr,
            )
            return 1
        print(
            f"  {len(rendered)} generated report tables and frontier/STATUS.md match "
            f"frontier/ "
            f"({sum(len(r) - 2 for r in rendered.values())} data rows)"
        )
        return 0
    for n, rows in rendered.items():
        text = splice(text, n, rows)
    with atomic_output_file(MAIN) as temporary:
        temporary.write_text(text, encoding="utf-8")
    with atomic_output_file(STATUS) as temporary:
        temporary.write_text(status, encoding="utf-8")
    print(f"rendered {len(rendered)} report tables and {STATUS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
