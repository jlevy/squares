#!/usr/bin/env python3
# ruff: noqa: RUF001 -- matching and writing the register's existing typography.
"""Audit DS7's reported lower bounds without promoting them to verified bounds.

The source claim is not verified by this program. The program proves only the
algebraic comparisons between its specialization and the exact identities named
by retained case records. It reads the working tree by default; explicit Git revisions
can reproduce an earlier source comparison without modifying the checkout.
The exact candidate envelope contains Green's Theorems 9 and 10, the usable exact
Table 2 entries, and the already indexed external n17 report. Table 2's three
decimal-only rows are retained as opaque metadata; its inconsistent n82 expression
is excluded in favor of Theorem 9. Neither operation recovers a missing source proof.

From packing/: uv run --frozen --group dev python -m devtools.audit_ds7_lower_bounds
"""

from __future__ import annotations

import argparse
import ast
import json
import math
import operator
import re
import subprocess
from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

import sympy as sp
import yaml

from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
MAX_N = 324
GREEN9 = "E-green-ds7-theorem9-reported-lower"
GREEN10 = "E-green-ds7-theorem10-reported-lower"
OPAQUE_TABLE = "E-friedman-ds7-table2-opaque-lower"
EXTERNAL17 = "E-n017-anabologyco-weighted-certificate"
REVIEW_DATE = "2026-09-07"


@dataclass(frozen=True)
class Candidate:
    """An exact source expression and the first case to which its report applies."""

    label: str
    base_n: int
    expression: sp.Expr
    evidence: str | None
    author: str
    theorem: int | None = None
    k: int | None = None


OPAQUE_ROWS = (
    (13, "3.8437", "Erich Friedman"),
    (21, "4.7438", "Erich Friedman"),
    (31, "5.6415", "Trevor Green"),
)


@cache
def exact_parse(source: str) -> sp.Expr:
    """Parse only arithmetic, square roots, integer floors/ceilings and min/max."""
    source = source.replace("^", "**")
    source = re.sub(r"(?<=[0-9)])(?=sqrt\()", "*", source)

    def visit(node: ast.AST) -> sp.Expr:
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            literal = ast.get_source_segment(source, node)
            assert literal is not None
            return sp.Rational(literal)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            value = visit(node.operand)
            return -value if isinstance(node.op, ast.USub) else value
        if isinstance(node, ast.BinOp):
            left, right = visit(node.left), visit(node.right)
            operations = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.Pow: operator.pow,
            }
            if type(node.op) in operations:
                return operations[type(node.op)](left, right)
        functions = {
            "sqrt": sp.sqrt,
            "floor": sp.floor,
            "ceil": sp.ceiling,
            "min": sp.Min,
            "max": sp.Max,
        }
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in functions
            and not node.keywords
        ):
            return functions[node.func.id](*(visit(arg) for arg in node.args))
        raise ValueError(f"unsupported exact expression: {source!r}")

    expression = sp.expand(visit(ast.parse(source, mode="eval").body))
    if (
        expression.free_symbols
        or expression.has(sp.Float)
        or expression.is_real is not True
        or expression.is_finite is not True
    ):
        raise ValueError(f"non-exact expression: {source!r}")
    return expression


def rational(value: sp.Rational) -> Fraction:
    return Fraction(int(value.p), int(value.q))


@cache
def enclosure(expression: sp.Expr, digits: int) -> tuple[Fraction, Fraction]:
    """Exact rational enclosure, using integer square-root division only."""
    if isinstance(expression, sp.Rational):
        value = rational(expression)
        return value, value
    if isinstance(expression, sp.Add):
        terms = [enclosure(term, digits) for term in expression.args]
        return sum((lo for lo, _ in terms), Fraction()), sum(
            (hi for _, hi in terms), Fraction()
        )
    if isinstance(expression, sp.Mul):
        lo = hi = Fraction(1)
        for term in expression.args:
            a, b = enclosure(term, digits)
            products = (lo * a, lo * b, hi * a, hi * b)
            lo, hi = min(products), max(products)
        return lo, hi
    if isinstance(expression, sp.Pow) and expression.exp == sp.Rational(1, 2):
        if not isinstance(expression.base, sp.Rational) or expression.base < 0:
            raise ValueError(f"unsupported radical: {expression}")
        radicand = rational(expression.base)
        scale = 10**digits
        floor = math.isqrt(radicand.numerator * scale**2 // radicand.denominator)
        lo = Fraction(floor, scale)
        if lo * lo == radicand:
            return lo, lo
        hi = Fraction(floor + 1, scale)
        assert lo * lo < radicand < hi * hi
        return lo, hi
    raise ValueError(f"unsupported exact enclosure expression: {expression}")


def compare(left: sp.Expr, right: sp.Expr) -> dict[str, Any]:
    difference = sp.expand(left - right)
    if difference == 0:
        return {"sign": 0, "difference_interval": ["0", "0"], "digits": 0}
    for digits in (8, 16, 32, 64, 128):
        lo, hi = enclosure(difference, digits)
        if lo > 0 or hi < 0:
            return {
                "sign": 1 if lo > 0 else -1,
                "difference_interval": [str(lo), str(hi)],
                "digits": digits,
            }
    raise ValueError(f"exact sign not separated: {difference}")


def green(k: int) -> sp.Expr:
    if k < 1:
        raise ValueError("The theorem's packing-count parameter must be positive")
    return sp.expand(
        2 * sp.sqrt(2) - 1 + (k * (k - 1) ** 2 + (k - 1) * sp.sqrt(2 * k)) / (k * k + 1)
    )


def green_ten(k: int) -> sp.Expr:
    if k < 1:
        raise ValueError("The theorem's packing-count parameter must be positive")
    return sp.expand(2 * sp.sqrt(2) + 2 * (k - 2) / sp.sqrt(5))


@cache
def candidates(max_n: int = MAX_N) -> tuple[Candidate, ...]:
    """All exact source candidates in the audited horizon, including dominated ones."""
    found: list[Candidate] = []
    for k in range(1, math.isqrt(max_n - 1) + 1):
        found.append(
            Candidate(f"Theorem 9, k={k}", k * k + 1, green(k), GREEN9, "Trevor Green", 9, k)
        )
        n0 = k * k + k // 2 + 1
        if n0 <= max_n:
            found.append(
                Candidate(
                    f"Theorem 10, k={k}", n0, green_ten(k), GREEN10, "Trevor Green", 10, k
                )
            )
    # Table intervals name the same bound at their first n; monotonicity extends it.
    # The n82 row is deliberately absent: the printed expression contradicts both
    # its own decimal and the elementary ten-by-ten grid upper bound.
    table = (
        (2, "2", "Frits Göbel"),
        (5, "2+1/sqrt(2)", "Frits Göbel"),
        (6, "3", "Michael Kearney and Peter Shiu"),
        (7, "3", "Erich Friedman"),
        (8, "3", "Erich Friedman"),
        (10, "3+1/sqrt(2)", "Walter Stromquist"),
        (11, "2+4/sqrt(5)", "Walter Stromquist"),
        (14, "4", "Erich Friedman"),
        (15, "4", "Erich Friedman"),
        (17, "(40sqrt(2)+19)/17", "Trevor Green"),
        (19, "6sqrt(2)-4", "Erich Friedman"),
        (22, "2sqrt(2)+2", "Trevor Green"),
        (23, "5", "Hiroshi Nagamochi"),
        (24, "5", "Erich Friedman"),
        (26, "2sqrt(2)+(27+2sqrt(10))/13", "Trevor Green"),
        (28, "2sqrt(2)+6/sqrt(5)", "Trevor Green"),
        (34, "6", "Hiroshi Nagamochi"),
        (35, "6", "Erich Friedman"),
        (37, "2sqrt(2)+(113+10sqrt(3))/37", "Trevor Green"),
        (40, "2sqrt(2)+8/sqrt(5)", "Trevor Green"),
        (47, "7", "Hiroshi Nagamochi"),
        (50, "2sqrt(2)+(101+3sqrt(14))/25", "Trevor Green"),
        (62, "8", "Hiroshi Nagamochi"),
        (65, "2sqrt(2)+71/13", "Trevor Green"),
        (79, "9", "Hiroshi Nagamochi"),
    )
    found.extend(
        Candidate(f"Table 2, n={n}", n, exact_parse(form), None, author)
        for n, form, author in table
        if n <= max_n
    )
    # Retained in the pre-existing source inventory. It is stronger than MacIver
    # and Green at n17, and monotonicity also makes it relevant at n18 and n19.
    if max_n >= 17:
        found.append(
            Candidate(
                "anabologyco-maker v0.2.0",
                17,
                sp.Rational(9141, 2000),
                EXTERNAL17,
                "anabologyco-maker",
            )
        )
    return tuple(found)


@cache
def best_candidate(n: int) -> Candidate | None:
    if not 1 <= n <= MAX_N:
        raise ValueError(f"n={n} lies outside the audited range 1..{MAX_N}")
    applicable = [candidate for candidate in candidates() if candidate.base_n <= n]
    if not applicable:
        return None
    best = applicable[0]
    for candidate in applicable[1:]:
        if compare(candidate.expression, best.expression)["sign"] > 0:
            best = candidate
    return best


def reported_payload(candidate: Candidate, n: int) -> dict[str, Any]:
    """Source-only payload; the caller is responsible for preserving stronger bounds."""
    if candidate.evidence is None:
        raise ValueError(f"no adoption evidence is declared for {candidate.label}")
    exact = str(candidate.expression).replace("**", "^")
    value = str(sp.N(candidate.expression, 13))
    external = candidate.evidence == EXTERNAL17
    note = (
        "The indexed external v0.2.0 report states s(17) >= 9141/2000 = 4.5705; "
        "the source checker has not been replayed completely here."
        if external
        else f"Friedman's DS7 survey, {candidate.label}, reports this bound at "
        f"n={candidate.base_n}; reference [8] is Green's private communication (2000). "
        "The source proof has not been recovered."
    )
    if n != candidate.base_n:
        note += f" Inherited at n={n} by monotonicity."
    if candidate.theorem == 10 and candidate.k == 4:
        note += (
            " This is the literal specialization of the printed general theorem; "
            "Table 2 lists the weaker 6*sqrt(2)-4 at n=19-20. "
            "The source does not explain that tension."
        )
    return {
        "value": "4.5705" if external else value,
        "exact_form": "9141/2000" if external else exact,
        "kind": "monotonicity" if n != candidate.base_n else "unavoidable-points",
        "proved_by": [candidate.author],
        "proved_year": 2026 if external else 2000,
        "source_key": "[GitHub n17 certificates 2026]" if external else "[Friedman DS7]",
        "note": note,
        "scope": "Source-reported only; no verification promotion.",
        "evidence": [candidate.evidence],
    }


def opaque_payload(n: int) -> dict[str, Any]:
    row = next((row for row in OPAQUE_ROWS if row[0] == n), None)
    if row is None:
        raise ValueError(f"n={n} is not an opaque Table 2 row")
    _, value, author = row
    return {
        "value": value,
        "exact_form": None,
        "kind": "unavoidable-points",
        "proved_by": [author],
        "proved_year": None,
        "source_key": "[Friedman DS7]",
        "note": "Table 2 prints this decimal without an exact identity or a rounding "
        "guarantee. It is opaque reported metadata, not an exact rational theorem.",
        "scope": "Source-reported decimal only; no exact comparison or proof certification.",
        "evidence": [OPAQUE_TABLE],
    }


def nagamochi(n: int) -> sp.Expr:
    k = math.isqrt(n)
    return sp.Min(k if k * k == n else k + 1, 1 + sp.sqrt(n - 2 * k + 1))


def field_expression(case: Mapping[str, Any], lane: str) -> tuple[sp.Expr, str]:
    bound = case[lane]
    if bound.get("exact_form"):
        return exact_parse(str(bound["exact_form"])), "record exact_form"
    if bound.get("kind") == "nagamochi":
        return nagamochi(case["n"]), "Nagamochi theorem identity for this n"
    shown = sp.Rational(str(bound["value"]))
    if isinstance(shown, sp.Rational) and shown.q == 1:
        return shown, "record integer value"
    source_identities = {5: "2+1/sqrt(2)", 10: "3+1/sqrt(2)"}
    if lane == "reported_lower_bound" and case["n"] in source_identities:
        expression = exact_parse(source_identities[case["n"]])
        verified = case["verified_lower_bound"]
        if (
            case.get("status") == "proved"
            and bound.get("evidence")
            and verified.get("evidence")
            and verified.get("exact_form")
            and compare(expression, exact_parse(str(verified["exact_form"])))["sign"] == 0
        ):
            return (
                expression,
                "DS7 Table 2 exact identity, agreeing with the established proved-case bound",
            )
    raise ValueError(f"n={case['n']}: {lane} lacks a usable exact identity: {bound}")


def read_case(repo: Path, revision: str | None, n: int) -> dict[str, Any]:
    path = f"packing/frontier/n-{n:03d}.md"
    source = (
        (repo / path).read_text()
        if revision is None
        else subprocess.run(
            ["git", "show", f"{revision}:{path}"],
            cwd=repo,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    )
    return load_yaml(source.split("---", 2)[1])["packing"]


def opaque_needs_update(case: Mapping[str, Any], value: str) -> bool:
    """Rank displayed metadata, while protecting a known stronger exact identity.

    Using the literal display as a preservation threshold gives it no theorem or
    rounding guarantee. It only prevents a less precise report from replacing an
    already stronger exact identity.
    """
    current = case["reported_lower_bound"]
    if (
        current.get("exact_form")
        and compare(exact_parse(str(current["exact_form"])), sp.Rational(value))["sign"] >= 0
    ):
        return False
    return Decimal(str(current["value"])) < Decimal(value)


def select_update(case: Mapping[str, Any]) -> dict[str, Any] | None:
    """Raise only the reported lane within this explicitly named candidate set."""
    n = int(case["n"])
    if n == 21:
        # This comparison is of displayed source metadata only. It never enters
        # the verified lane or a theorem as the rational number 23719/5000.
        # A known stronger exact identity must survive a coarser displayed value.
        return opaque_payload(n) if opaque_needs_update(case, "4.7438") else None
    candidate = best_candidate(n)
    if candidate is None or candidate.evidence is None:
        return None
    expression, _ = field_expression(case, "reported_lower_bound")
    if compare(candidate.expression, expression)["sign"] <= 0:
        return None
    return reported_payload(candidate, n)


def source_paragraph(n: int, case: Mapping[str, Any]) -> str:
    reported = case["reported_lower_bound"]
    verified = case["verified_lower_bound"]["value"]
    exact = reported.get("exact_form")
    claim = (
        f"the lower-bound expression `{exact}` for `s({n})` "
        f"(approximately `{reported['value']}`)"
        if exact
        else (f"the decimal `{reported['value']}` for `s({n})`")
    )
    return (
        f"The selected external report, {reported['source_key']}, gives {claim}. "
        f"{reported['note']} This changes the reported source field only; "
        f"the independently verified lower bound remains `{verified}`. "
        "The [source audit](../devtools/audit_ds7_lower_bounds.py) compares the exact "
        "theorem expressions separately from opaque table decimals."
    )


def update_records(repo: Path, first_n: int = 1, last_n: int = MAX_N) -> list[int]:
    """Apply the reviewed source corrections while retaining every verified field."""
    from flowmark import reformat_text  # noqa: PLC0415

    from devtools.generate_frontier_case import (  # noqa: PLC0415
        NAGAMOCHI_DEFAULT_COUNTED,
        NAGAMOCHI_DEFAULT_UNCOUNTED,
        nagamochi_lower_section,
    )

    changed_bounds = []
    old_counted = (
        "This is the default across almost the whole open frontier — 58 of the 65 open cases "
        "at `n ≤ 100` are governed by it, and outside this repository’s own displacements it "
        "has not been improved since 2005."
    )
    old_uncounted = (
        "This is the default across almost the whole open frontier, and outside this "
        "repository’s own displacements it has not been improved since 2005."
    )
    for path in sorted((repo / "packing" / "frontier").glob("n-*.md")):
        original = path.read_text()
        _, front, body = original.split("---", 2)
        document = load_yaml(front)
        case = document["packing"]
        n = int(case["n"])
        if not first_n <= n <= last_n:
            continue
        protected = ("verified_lower_bound", "reported_upper_bound", "verified_upper_bound")
        before = deepcopy(tuple(case[key] for key in protected))
        selected = select_update(case)
        if selected is not None:
            changed_bounds.append(n)
            case["reported_lower_bound"] = selected
            case["source_reviewed"] = REVIEW_DATE
            for evidence in selected["evidence"]:
                if evidence not in case["evidence"]:
                    case["evidence"].append(evidence)
            if not any(
                set(block.get("evidence", [])) & set(selected["evidence"])
                for block in case["blockers"]
            ):
                case["blockers"].append(
                    {
                        "kind": "source-evidence",
                        "detail": (
                            "The complete source checker has not been independently "
                            "replayed here."
                            if EXTERNAL17 in selected["evidence"]
                            else "The exact identity and rounding meaning of this "
                            "reported decimal are not supplied."
                            if OPAQUE_TABLE in selected["evidence"]
                            else "Green's reported lower-bound proof, cited as private "
                            "communication "
                            "by Friedman, has not been recovered or independently replayed."
                        ),
                        "evidence": list(selected["evidence"]),
                    }
                )
            if selected["source_key"] == "[GitHub n17 certificates 2026]" and not any(
                resource["key"] == selected["source_key"] for resource in case["resources"]
            ):
                case["resources"].append(
                    {
                        "key": selected["source_key"],
                        "role": "lower-bound-proof",
                        "local": "packing/resources/web/n17-github-certificates-2026/README.md",
                        "url": "https://github.com/anabologyco-maker/square17-lower-bound/tree/396da6f7c112f49b50b5f4563ad2486ef38ac909",
                        "retrieved": True,
                    }
                )
            if n <= 100:
                paragraph = source_paragraph(n, case)
                marker = "## The lower bound\n"
                if marker in body:
                    body = body.replace(marker, marker + "\n" + paragraph + "\n", 1)
                else:
                    body = body.replace(
                        "<!-- This document follows",
                        "## Reported Lower Bound\n\n"
                        + paragraph
                        + "\n\n<!-- This document follows",
                        1,
                    )
        # The former blanket claims were not source audits. Removing them does not
        # remove a bound; every actual reported improvement is adopted above.
        body = body.replace("Nothing specific to this `n` has ever been proved.\n", "")
        body = re.sub(
            r"the\s+best\s+proved\s+lower\s+bound\s+is",
            "the strongest lower bound independently verified here is",
            body,
        )
        if selected is None and case["reported_lower_bound"].get("exact_form"):
            reported = case["reported_lower_bound"]
            if set(reported["evidence"]) & {GREEN9, GREEN10, EXTERNAL17}:
                body = body.replace(
                    f"`s({n}) ≥ {reported['exact_form']}`",
                    f"the lower-bound expression `{reported['exact_form']}` for `s({n})`",
                )
        body = re.sub(
            r"The bound is Nagamochi’s general closed form, which applies to every `N ≥ 4`:",
            "The strongest lower bound independently verified in this record is "
            "Nagamochi’s general closed form, which applies to every `N ≥ 4`:",
            body,
        )
        for old, new in (
            (old_counted, NAGAMOCHI_DEFAULT_COUNTED),
            (old_uncounted, NAGAMOCHI_DEFAULT_UNCOUNTED),
        ):
            body = re.sub(r"\s+".join(re.escape(word) for word in old.split()), new, body)
        if (n > 100 or n == 50) and math.isqrt(n) ** 2 != n:
            replacement = (
                "## The lower bound\n\n" + "\n".join(nagamochi_lower_section(n, case)) + "\n\n"
            )
            body = re.sub(
                r"## The lower bound\n.*?(?=<!-- This document follows)",
                replacement,
                body,
                flags=re.DOTALL,
            )
        assert tuple(case[key] for key in protected) == before
        # Preserve frontmatter bytes on prose-only changes, including source anchors.
        if selected is not None or n > 100 or n == 50:
            front = (
                "\n"
                + yaml.safe_dump(
                    document, sort_keys=False, allow_unicode=True, width=96
                ).rstrip()
                + "\n"
            )
        updated = reformat_text("---" + front + "---" + body, semantic=True, cleanups=True)
        if updated != original:
            path.write_text(updated)
    return changed_bounds


def audit(
    repo: Path, base_ref: str | None, extension_ref: str | None, max_n: int
) -> dict[str, Any]:
    if not 2 <= max_n <= MAX_N:
        raise ValueError(f"max_n must lie in 2..{MAX_N}")
    seeds = [(k, k * k + 1, green(k)) for k in range(1, math.isqrt(max_n - 1) + 1)]
    rows = []
    seed_rows = []
    no_candidate_cases = []
    for k, n0, value in seeds:
        seed_rows.append(
            {
                "k": k,
                "base_n": n0,
                "exact": str(value),
                "display_decimal": str(sp.N(value, 24)),
                "rational_interval": [str(v) for v in enclosure(value, 24)],
            }
        )
    for n in range(1, max_n + 1):
        revision = base_ref if n <= 100 else extension_ref
        case = read_case(repo, revision, n)
        best_source = best_candidate(n)
        if best_source is None:
            # n1 has no applicable DS7 candidate, but its fields are still read.
            field_expression(case, "reported_lower_bound")
            field_expression(case, "verified_lower_bound")
            no_candidate_cases.append(n)
            continue
        best = best_source.expression
        comparisons = {}
        for lane in ("reported_lower_bound", "verified_lower_bound"):
            if (
                lane == "reported_lower_bound"
                and OPAQUE_TABLE in case[lane]["evidence"]
                and not case[lane].get("exact_form")
            ):
                comparisons[lane] = {
                    "current_record_value": str(case[lane]["value"]),
                    "current_exact": None,
                    "exact_identity_basis": "opaque source decimal",
                    "comparison": {"sign": None, "difference_interval": None, "digits": None},
                }
                continue
            current, basis = field_expression(case, lane)
            comparisons[lane] = {
                "current_record_value": str(case[lane]["value"]),
                "current_exact": str(current),
                "exact_identity_basis": basis,
                "comparison": compare(best, current),
            }
        rows.append(
            {
                "n": n,
                "case_revision": revision,
                "k": best_source.k,
                "base_n": best_source.base_n,
                "selected_source": best_source.label,
                "monotonicity_transfer": n != best_source.base_n,
                "candidate_exact": str(best),
                **comparisons,
            }
        )
    opaque = []
    for n, value, author in OPAQUE_ROWS:
        if n > max_n:
            continue
        case = read_case(repo, base_ref if n <= 100 else extension_ref, n)
        opaque.append(
            {
                "n": n,
                "source_value": value,
                "author": author,
                "source_status": "opaque decimal; no exact identity or rounding guarantee",
                "reported_display_comparison": (
                    Decimal(value) > Decimal(case["reported_lower_bound"]["value"])
                )
                - (Decimal(value) < Decimal(case["reported_lower_bound"]["value"])),
                "verified_record_value": str(case["verified_lower_bound"]["value"]),
                "needs_reported_update": opaque_needs_update(case, value),
                "disposition": "reported decimal retained; verified bound unchanged"
                if n == 21
                else "display value is below current source and verified records; not selected",
            }
        )
    malformed = exact_parse("2sqrt(2)+(288+12sqrt(3))/41")
    return {
        "source": {
            "url": "https://erich-friedman.github.io/papers/squares/squares.html",
            "local": (
                "packing/resources/papers/friedman-ds7-packing-unit-squares-in-squares.pdf"
            ),
            "theorems": [9, 10],
            "theorem_pdf_page": 23,
            "table_pdf_pages": [25, 26],
            "reference": "[8], Trevor Green, private communication (2000)",
            "status": "source-reported; proof not independently verified",
            "limitations": [
                (
                    "Exact comparison validates formula specialization and ordering only; "
                    "the missing geometric proofs have not been recovered."
                ),
                (
                    "This is the named candidate envelope, not a complete DS7 or world "
                    "literature audit. Opaque table decimals have no exact interpretation."
                ),
            ],
        },
        "scope": {
            "base_ref_through_100": base_ref,
            "extension_ref_above_100": extension_ref,
            "max_n": max_n,
            "case_records_checked": max_n,
            "cases_without_applicable_exact_candidate": no_candidate_cases,
        },
        "candidate_counts": {
            "theorem9": sum(c.theorem == 9 for c in candidates(max_n)),
            "theorem10": sum(c.theorem == 10 for c in candidates(max_n)),
            "usable_exact_table2_entries": sum(c.evidence is None for c in candidates(max_n)),
            "indexed_external_n17_report": int(max_n >= 17),
            "opaque_table2_entries": len(opaque),
            "excluded_malformed_table2_entries": 1,
        },
        "exact_candidates": [
            {
                "label": c.label,
                "base_n": c.base_n,
                "exact": str(c.expression),
                "evidence": c.evidence,
                "author": c.author,
            }
            for c in candidates(max_n)
        ],
        "theorem9_seeds": seed_rows,
        "theorem10_seeds": [
            {"k": c.k, "base_n": c.base_n, "exact": str(c.expression)}
            for c in candidates(max_n)
            if c.theorem == 10
        ],
        "opaque_table_rows": opaque,
        "theorem10_table2_tension": {
            "cases": [19, 20],
            "theorem10_k4_base_n": 19,
            "literal_general_theorem": str(green_ten(4)),
            "table2_expression": str(exact_parse("6sqrt(2)-4")),
            "theorem_exceeds_table": compare(green_ten(4), exact_parse("6sqrt(2)-4")),
            "disposition": (
                "Select the literal general-theorem specialization as reported only. "
                "The source supplies no restriction explaining its weaker Table 2 row; "
                "this is not evidence that the historical table accepted the specialization."
            ),
        },
        "table82_defect": {
            "printed_expression": str(malformed),
            "printed_decimal": "9.2667",
            "theorem9_k9": str(green(9)),
            "printed_expression_exceeds_exact_grid_upper_10": compare(
                malformed, sp.Integer(10)
            ),
            "disposition": (
                "exclude malformed table expression; select the independent "
                "Theorem 9 specialization"
            ),
        },
        "rows": rows,
        "greater_than_reported": [
            r["n"] for r in rows if r["reported_lower_bound"]["comparison"]["sign"] == 1
        ],
        "equal_to_reported": [
            r["n"] for r in rows if r["reported_lower_bound"]["comparison"]["sign"] == 0
        ],
        "greater_than_verified": [
            r["n"] for r in rows if r["verified_lower_bound"]["comparison"]["sign"] > 0
        ],
        "equal_to_verified": [
            r["n"] for r in rows if r["verified_lower_bound"]["comparison"]["sign"] == 0
        ],
    }


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=ROOT.parent)
    parser.add_argument(
        "--base-ref", help="optional Git revision for n<=100; default reads the worktree"
    )
    parser.add_argument(
        "--extension-ref", help="optional Git revision for n>100; default reads the worktree"
    )
    parser.add_argument("--max-n", type=int, default=324)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if an audited candidate still dominates a reported field",
    )
    parser.add_argument(
        "--update",
        action="store_true",
        help="apply source corrections to case records, preserving verified fields",
    )
    parser.add_argument("--update-min-n", type=int, default=1)
    parser.add_argument("--update-max-n", type=int, default=MAX_N)
    args = parser.parse_args(argv)
    if not 2 <= args.max_n <= MAX_N:
        parser.error(f"--max-n must lie in 2..{MAX_N}")
    if args.update:
        if args.base_ref or args.extension_ref:
            parser.error("--update cannot target historical Git revisions")
        if not 1 <= args.update_min_n <= args.update_max_n <= MAX_N:
            parser.error("update interval must lie in 1..324")
        changed = update_records(args.repo, args.update_min_n, args.update_max_n)
        print(f"updated reported lower fields: {changed}")
    result = audit(args.repo, args.base_ref, args.extension_ref, args.max_n)
    if args.output:
        result["scope"]["worktree_git_head"] = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=args.repo,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        result["scope"]["git_basis_note"] = (
            "The Git HEAD identifies the worktree's parent commit, not a claim that "
            "the corrected record bytes are already committed. Explicit revision "
            "arguments, when present, identify the record inputs instead."
        )
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "scope",
                    "greater_than_reported",
                    "equal_to_reported",
                    "greater_than_verified",
                    "equal_to_verified",
                )
            },
            indent=2,
        )
    )
    opaque_dominated = [
        row["n"] for row in result["opaque_table_rows"] if row["needs_reported_update"]
    ]
    if args.check and (result["greater_than_reported"] or opaque_dominated):
        raise SystemExit(
            "audited reports still dominate case fields: "
            f"exact={result['greater_than_reported']}, opaque={opaque_dominated}"
        )


if __name__ == "__main__":
    main()
