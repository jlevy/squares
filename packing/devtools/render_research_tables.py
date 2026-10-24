#!/usr/bin/env python3
"""Render the research documents' data tables from the structured sources.

The tables are duplicated deliberately: a reader should get the whole picture
from the report alone, without opening the data. Duplication is only safe if it
cannot drift, so the Markdown between the GENERATED markers is written from
`frontier/` rather than by hand.

    uv run --frozen python -m devtools.render_research_tables
    uv run --frozen python -m devtools.render_research_tables --check

`--check` compares parsed cells, not bytes, so it is unaffected by the
Markdown formatter reflowing the surrounding prose. Rendering answers to the
same comparison: a row that still says what the document says is written back
unchanged, so a run over an unchanged tree produces an empty diff.
"""

from __future__ import annotations

import argparse
import ast
import math
import pathlib
import re
import sys
from decimal import Decimal

from strif import atomic_output_file

from devtools.check_source_coverage import pending_intake_blocker
from sqpack.assurance import bounds_agree_at_declared_precision
from sqpack.yamlio import safe_load

ROOT = pathlib.Path(__file__).resolve().parent.parent
# The repository root. The reader-facing documents live there, not under packing/.
REPO = ROOT.parent
FRONTIER = ROOT / "frontier"
MAIN = REPO / "docs/project/research/research-2026-08-22-packing-11-unit-squares.md"
STATUS = FRONTIER / "STATUS.md"

BEGIN = "<!-- BEGIN GENERATED: %s (devtools.render_research_tables) -->"
END = "<!-- END GENERATED: %s -->"


def load_cases() -> list[dict]:
    out = []
    for f in sorted(FRONTIER.glob("n-*.md")):
        fm = safe_load(f.read_text(encoding="utf-8").split("---\n")[1])
        out.append(fm["packing"])
    return out


def load_evidence() -> dict[str, dict]:
    document = safe_load((FRONTIER / "evidence.yaml").read_text(encoding="utf-8"))
    return {record["id"]: record for record in document["evidence"]}


def fmt(x: object, nd: int = 6) -> str:
    return f"{Decimal(str(x)):.{nd}f}".rstrip("0").rstrip(".")


def nagamochi_radicand(expr: str) -> int | None:
    """The radicand `r` when `expr` is Nagamochi's `1 + √(n - 2⌊√n⌋ + 1)`, else `None`."""
    nagamochi = re.fullmatch(r"sqrt\((\d+) - 2\*floor\(sqrt\((\d+)\)\) \+ 1\) \+ 1", expr)
    if nagamochi is None or nagamochi.group(1) != nagamochi.group(2):
        return None
    n = int(nagamochi.group(1))
    return n - 2 * math.isqrt(n) + 1


def pretty(expr: str) -> str:
    """ASCII exact forms are the stored value; this is display only."""
    radicand = nagamochi_radicand(expr)
    if radicand is not None:
        return f"1 + √{radicand}"
    return re.sub(r"sqrt\((\d+)\)", r"√\1", expr)


#: A polynomial-root exact form, which has no closed form to show: `root(P_name, decimal)`,
#: a root of a named minimal polynomial, or `root(<polynomial in s>, <low>, <high>)`, the
#: one root in an interval, as `exact_sides.form` writes an algebraic house's side.
ROOT_FORM = re.compile(r"root\((?:\w+,\s*[0-9.]+|[0-9s^{}+\- ]+,\s*[0-9.]+,\s*[0-9.]+)\)")


def _latex_node(node: ast.expr) -> str:
    """One node of a parsed exact form, as LaTeX."""
    match node:
        case ast.Constant(value=int() as value):
            shown = str(value)
        case ast.UnaryOp(op=ast.USub(), operand=operand):
            shown = f"-{_latex_node(operand)}"
        case ast.Call(func=ast.Name(id="sqrt"), args=[argument]):
            shown = rf"\sqrt{{{_latex_node(argument)}}}"
        case ast.Call(func=ast.Name(id="floor"), args=[argument]):
            shown = rf"\lfloor {_latex_node(argument)} \rfloor"
        case ast.BinOp(left=left, op=ast.Div(), right=right):
            shown = rf"\frac{{{_latex_node(left)}}}{{{_latex_node(right)}}}"
        case ast.BinOp(left=left, op=ast.Mult(), right=right):
            joined = isinstance(right, ast.Call) or (
                isinstance(right, ast.BinOp) and isinstance(right.op, ast.Div)
            )
            shown = _latex_node(left) + ("" if joined else r" \cdot ") + _latex_node(right)
        case ast.BinOp(left=left, op=ast.Add(), right=right):
            shown = f"{_latex_node(left)} + {_latex_node(right)}"
        case ast.BinOp(left=left, op=ast.Sub(), right=right):
            subtracted = _latex_node(right)
            if isinstance(right, ast.BinOp) and isinstance(right.op, ast.Add | ast.Sub):
                subtracted = rf"\left({subtracted}\right)"
            shown = f"{_latex_node(left)} - {subtracted}"
        case _:
            raise ValueError(f"no LaTeX form for {ast.dump(node)}")
    return shown


def polynomial_latex(polynomial: str) -> str:
    """A recorded minimal polynomial as LaTeX: its radicals typeset, the rest as written.

    The record writes `s^{12}` and `s^8 - 20s^7 + … = 0` as TeX already reads them; only
    the `sqrt(2)` in a coefficient and an explicit `*` need translating.
    """
    tex = re.sub(r"sqrt\((\d+)\)", r"\\sqrt{\1}", polynomial).replace("*", "")
    if not re.fullmatch(r"[0-9s^{}+\-=() ]*", tex.replace(r"\sqrt", "")):
        raise ValueError(f"no LaTeX form for the polynomial {polynomial!r}")
    return tex


def latex(expr: str) -> str:
    """An ASCII exact form as LaTeX, for pages that render math; display only, like `pretty`.

    `31/8` becomes `\\frac{31}{8}`, `2 + (1/2)sqrt(2)` becomes `2 + \\frac{1}{2}\\sqrt{2}`,
    and Nagamochi's bound reads `1 + \\sqrt{r}` as `pretty` shows it. A `root(P, x)` form
    has no closed form to show and is refused: its reader wants the decimal and the
    minimal polynomial instead. Anything else the record could hold is refused too, so a
    new shape fails the render rather than printing ASCII.
    """
    if ROOT_FORM.fullmatch(expr):
        raise ValueError(f"{expr!r} is a polynomial root, not a closed form")
    radicand = nagamochi_radicand(expr)
    if radicand is not None:
        return rf"1 + \sqrt{{{radicand}}}"
    # The record writes implicit products, `(1/2)sqrt(2)` and `2 sqrt(2)`.
    explicit = re.sub(r"(\)|\d)\s*(?=sqrt\()", r"\1*", expr)
    return _latex_node(ast.parse(explicit, mode="eval").body)


LB_LABEL = {
    "area": "area `√n`",
    "perfect-square": "perfect square",
    "nagamochi": "Nagamochi",
    "monotonicity": "monotone",
    "unavoidable-points": "unavoidable points",
    "counting": "counting",
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
    """Render the authoritative exact form when one is available."""
    exact = bound.get("exact_form")
    if isinstance(exact, str) and exact:
        return f"`{pretty(exact)}`"
    return f"`{bound['value']}`"


#: What a read here of an external argument found, as an external entry's label carries
#: it (the evidence schema's `external_review.state`). An external proof with no read on
#: file is "not read here": it proves its claim whether or not it was read, and the label
#: says only what this repository has examined.
REVIEW_LABEL = {
    "not-reviewed": "not read here",
    "informally-verified": "read here",
    "defect-found": "read here, defect recorded",
}
UNREAD = "not-reviewed"
DEFECT_FOUND = "defect-found"
#: The two lanes a case's verified bounds sit in, as the labels name them.
VERIFIED_LANES = (("upper", "verified_upper_bound"), ("lower", "verified_lower_bound"))


def origin_label(entry: dict) -> str | None:
    """Who did the work behind one evidence entry, and for an external argument whether it
    was read here: `replayed here`, or `external proof (not read here)`."""
    label = ORIGIN_LABEL.get(str(entry.get("origin")))
    if label is None:
        return None
    if entry.get("origin") == "external":
        state = (entry.get("external_review") or {}).get("state")
        if state in REVIEW_LABEL:
            label = f"{label} ({REVIEW_LABEL[state]})"
    return label


def lane_origins(bound: dict, evidence: dict[str, dict]) -> str:
    """The labels of the evidence one bound cites, once each, or `—`."""
    labels = [origin_label(evidence[ref]) for ref in bound.get("evidence") or []]
    return ", ".join(dict.fromkeys(label for label in labels if label)) or "—"


def verification_origins(case: dict, evidence: dict[str, dict]) -> str:
    """Who verified each of a case's two verified bounds, lane by lane: `upper: replayed
    here; lower: external proof (not read here)`. Until 2026-10-06 the two lanes were
    merged into one list, so a row whose upper bound was replayed and whose lower bound
    was a published proof nobody here had read said `replayed here, external proof`
    without saying which lane was which, or that the proof was unread."""
    return "; ".join(
        f"{name}: {lane_origins(case[field], evidence)}" for name, field in VERIFIED_LANES
    )


def unread_external_proof(entry: dict) -> bool:
    """Whether an evidence entry is a published proof by others that nobody here has
    read: `origin: external`, `method: published-proof`, `external_review.state:
    not-reviewed`."""
    return (
        entry.get("origin") == "external"
        and entry.get("method") == "published-proof"
        and (entry.get("external_review") or {}).get("state") == UNREAD
    )


def rests_on_unread_proof(bound: dict, evidence: dict[str, dict]) -> bool:
    """Whether every entry a bound cites is a published proof nobody here has read, so
    that nothing here has examined the argument the bound stands on."""
    refs = bound.get("evidence") or []
    return bool(refs) and all(unread_external_proof(evidence[ref]) for ref in refs)


def reported_defect(reported: dict, verified: dict, evidence: dict[str, dict]) -> bool:
    """Whether a reported bound stands on evidence whose read here found a defect while
    no verified bound holds its value: Nagamochi's closed form above the verified floor
    since 2026-10-02 (T-007), or a value of Green's DS7 Theorem 9, whose illustrated
    argument leaves a square empty. Where the verified bound equals the reported one, the
    defect moves no value on the row and is not marked."""
    found = any(
        (evidence[ref].get("external_review") or {}).get("state") == DEFECT_FOUND
        for ref in reported.get("evidence") or []
    )
    return found and not bounds_agree_at_declared_precision(reported, verified)


def same_bound(left: dict, right: dict) -> bool:
    """Delegate the shared assurance-level representation comparison."""
    return bounds_agree_at_declared_precision(left, right)


def case_disposition(case: dict, evidence: dict[str, dict]) -> str:
    """The row's notes: where a verified bound differs from the reported one, where a
    reported bound stands on a read that found a defect (`reported_defect`), a pending
    audit, a conflict, or a catalogue side the record waits to take."""
    notes = []
    if not same_bound(case["reported_upper_bound"], case["verified_upper_bound"]):
        notes.append("formal upper trails report")
    if reported_defect(case["reported_upper_bound"], case["verified_upper_bound"], evidence):
        notes.append("reported upper: defect recorded")
    if not same_bound(case["reported_lower_bound"], case["verified_lower_bound"]):
        notes.append("formal lower differs from report")
    if reported_defect(case["reported_lower_bound"], case["verified_lower_bound"], evidence):
        notes.append("reported lower: defect recorded")
    if case["reported_status"] != case["status"]:
        notes.append("proof audit pending")
    if case["conflicts"]:
        notes.append(f"{len(case['conflicts'])} conflict")
    if pending_intake_blocker(case) is not None:
        # The catalogue prints a smaller side the record waits to take: say so here, so
        # the table does not present the older side as the best known one.
        notes.append("catalogue ahead, intake pending")
    return "; ".join(notes) or "—"


def render_status(cases: list[dict], evidence: dict[str, dict]) -> str:
    last_n = max(case["n"] for case in cases)
    rows = [
        (
            "<!-- GENERATED by devtools.render_research_tables from frontier/n-*.md and "
            "evidence.yaml. Do not edit by hand. -->"
        ),
        "",
        "# Current Square-Packing Frontier",
        "",
        (
            f"This is the reader-first view of every tracked case through `n = {last_n}`. "
            "Reported columns preserve what the declared public sources say. Verified "
            "columns contain only exact formal bounds: a complete proof, an exact "
            "algebraic replay, or a rigorous certificate. A finite-precision result is "
            "*numerically checked* and does not enter a verified column, even at "
            "extremely small tolerance."
        ),
        "",
        (
            "The verification origin says, lane by lane, who did the work behind each "
            "verified bound, and for a published proof by others whether anyone here has "
            "read it: a published proof counts whether or not it was read, and *not read "
            "here* says only that this repository has not examined it. *Defect recorded* "
            "marks a reported bound that stands on a proof whose reading here found a "
            "defect, where no verified bound reaches its value."
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
            f"{verification_origins(case, evidence)} | {case_disposition(case, evidence)} | "
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
    d = safe_load((FRONTIER / f"{kind}-strategies.yaml").read_text(encoding="utf-8"))
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
    d = safe_load((FRONTIER / "source-availability.yaml").read_text(encoding="utf-8"))
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
    d = safe_load((FRONTIER / "source-availability.yaml").read_text(encoding="utf-8"))
    rows = ["| Source | How it was recovered |", "| --- | --- |"]
    for s in d["recovered"]:
        rows.append(f"| **{s['key']}** {s['title']} | {' '.join(s['how'].split())} |")
    return rows


# The Markdown formatter normalizes typography in place (straight quotes to
# curly, -- to en dash, ... to an ellipsis). That rewrites generated cells, so
# both directions compare *content*: sides are folded back to ASCII punctuation
# first, by --check before it reports staleness and by the writer before it
# decides a row needs rewriting. Anything that changes what a cell says still
# reads as changed.
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


def fold(line: str) -> str:
    """What a generated line *says*, with formatter-owned typography folded away."""
    return " ".join(line.translate(_FOLD).split())


def keep_document_typography(previous: str, rows: list[str]) -> list[str]:
    """Rewrite only the rows whose content actually changed.

    The formatter owns typography everywhere, including inside these generated
    blocks: it curls the straight quotes this module renders from the ASCII in
    `frontier/`. Splicing freshly rendered rows in flattens them back, on every
    run, in lines nobody edited -- and `--check` folds typography away, so it
    never reports the damage. So a rendered row that says exactly what the
    document already says is written back byte for byte, and only a row whose
    content moved is replaced with the newly rendered text.
    """
    available: dict[str, list[str]] = {}
    for line in previous.splitlines():
        if line.strip():
            available.setdefault(fold(line), []).append(line)
    kept = []
    for row in rows:
        unchanged = available.get(fold(row))
        kept.append(unchanged.pop(0) if unchanged else row)
    return kept


def splice(text: str, name: str, rows: list[str]) -> str:
    b, e = BEGIN % name, END % name
    i, j = text.index(b), text.index(e)
    rows = keep_document_typography(text[i + len(b) : j], rows)
    return text[:i] + b + "\n\n" + "\n".join(rows) + "\n\n" + text[j:]


def cells(block: str) -> list[list[str]]:
    out = []
    for line in block.splitlines():
        if not line.startswith("|"):
            continue
        c = [fold(x) for x in line.strip().strip("|").split("|")]
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
    raise SystemExit(main())
