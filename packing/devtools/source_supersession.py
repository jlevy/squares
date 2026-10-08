"""Keep historical import layers from replacing explicitly superseding source reports."""

from __future__ import annotations

import re
from collections.abc import Collection, Mapping
from copy import deepcopy
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml

from sqpack.yamlio import safe_load

COVERAGE = Path(__file__).resolve().parents[1] / "frontier/source-coverage.yaml"


def superseded_counts(coverage: Mapping[str, Any], source_ids: Collection[str]) -> set[int]:
    """Counts where the register explicitly assigns this source to a later selection."""
    selected = {row["n"]: row["source_id"] for row in coverage["selected_overrides"]}
    return {
        row["n"]
        for row in coverage["superseded_reports"]
        if row["source_id"] in source_ids
        and selected.get(row["n"]) == row["superseded_by"]
        and row["superseded_by"] not in source_ids
    }


def preserve_selected_case(n: int, text: str, source_ids: Collection[str]) -> bool:
    """Preserve an adopted later report, while still admitting earlier drafting inputs."""
    coverage = safe_load(COVERAGE.read_text())
    if n not in superseded_counts(coverage, source_ids):
        return False
    selected = next(row for row in coverage["selected_overrides"] if row["n"] == n)
    source = next(row for row in coverage["sources"] if row["id"] == selected["source_id"])
    case = safe_load(text.split("---\n", 2)[1])["packing"]
    return case["reported_upper_bound"]["source_key"] == source["source_key"]


def _adopt_selected_update(n: int, existing: str, generated: str) -> str:
    """Rebuild the selected update while retaining the earlier certified lane."""
    from devtools import render_case_verifiers  # noqa: PLC0415
    from devtools import squish_followup_packets as update  # noqa: PLC0415
    from devtools import squish_upper_bound_packets as original  # noqa: PLC0415
    from devtools.check_case_prose import sentence_spans  # noqa: PLC0415

    if n not in update.NUMBERS or n == 153:
        raise ValueError("selected SQUISH update count is outside its result roster")
    _, front, body = existing.split("---\n", 2)
    _, draft_front, draft_body = generated.split("---\n", 2)
    document = safe_load(front)
    case = document["packing"]
    if case["reported_upper_bound"]["source_key"] != update.SOURCE_KEY:
        return generated
    declarations = case["verified_upper_bound"]["evidence"]
    if any(
        evidence.startswith("E-squish-update-") and evidence != update.EXACT_EVIDENCE
        for evidence in declarations
    ):
        raise ValueError("unmapped confirmed SQUISH update evidence")
    draft = safe_load(draft_front)["packing"]
    confirmed = update.EXACT_EVIDENCE in declarations
    bound = update.confirmed_bound(n) if confirmed else None
    fact = update.read_fact(n)
    report = case["reported_upper_bound"]
    report.update(
        value=update.display(fact["side"]),
        exact_form=fact["side"],
        algebraic_degree=1,
        minimal_polynomial=None,
        analytically_optimized=None,
        catalogue_rigid="not-stated",
        construction_method="unknown",
        tilt_angles_deg=None,
        found_by=[original.AUTHOR],
        found_year=2026,
        improved_by=[],
        catalogue_pictured=False,
        source_key=update.SOURCE_KEY,
        source_date=update.RETRIEVED,
        retrieved_date=update.RETRIEVED,
    )
    for field in ("reported_lower_bound", "verified_lower_bound", "reported_status", "status"):
        case[field] = draft[field]
    if bound is not None:
        case["verified_upper_bound"] = bound
    if n in update.REPLACEMENTS:
        prior = original.read_fact(n)
        prior_value = original.verified_value(Fraction(prior["side"]), prior["printed_side"])
        if not confirmed:
            case["verified_upper_bound"] = {
                "value": prior_value,
                "exact_form": prior["side"],
                "evidence": ["E-squish-ten-packings-2026-10-07-exact-replay"],
            }
        # These declarations belong to the earlier certified pose, never the update.
        side = Fraction(prior["side"])
        source_label = "The source" + chr(0x2019) + "s original finite decimal display is"
        declarations = (
            (
                r"S_n = \\frac\{[0-9]+\}\{[0-9]+\}",
                f"S_n = \\frac{{{side.numerator}}}{{{side.denominator}}}",
            ),
            (
                re.escape(source_label) + r"\s+\$[0-9.]+\$",
                f"{source_label} ${prior['printed_side']}$",
            ),
            (
                r"The verified display is\s+\$[0-9.]+\$",
                f"The verified display is ${prior_value}$",
            ),
        )
        for pattern, replacement in declarations:
            body, count = re.subn(pattern, lambda _match, value=replacement: value, body)
            if count != 1:
                raise ValueError(
                    "selected update needs exactly one earlier side/display declaration"
                )
    elif not confirmed:
        case["verified_upper_bound"] = draft["verified_upper_bound"]
    case["source_reviewed"] = update.RETRIEVED
    case["rigidity"] = None
    lower = re.search(
        r"\n## The lower bound\n.*?(?=\n<!-- BEGIN verification code)", draft_body, re.DOTALL
    )
    if lower is None:
        raise ValueError("historical draft has no independently generated lower-bound section")
    body, count = re.subn(
        r"\n## The lower bound\n.*?(?=\n<!-- BEGIN verification code)",
        lambda _match: lower.group(),
        body,
        flags=re.DOTALL,
    )
    if count != 1:
        raise ValueError("selected update needs exactly one generated lower-bound section")
    section = re.search(r"\n## The SQUISH Update\n.*?(?=\n## |\Z)", body, re.DOTALL)
    if section is None:
        raise ValueError("selected update needs its report section")
    text = section.group()
    if confirmed:
        for pattern, replacement in (
            (
                (
                    r"This\s+is a reported\s+V0/C0\s+claim pending complete replay "
                    r"and new scoped review\."
                ),
                (
                    "This update is confirmed at V3/C3 by the complete retained dual exact "
                    "replay and separately prompted scoped AI reviews. It establishes a "
                    "feasible upper bound; optimality and human oversight have not "
                    "been established."
                ),
            ),
            (
                (
                    r"The earlier certified bound and its retained evidence remain "
                    r"unchanged;\s+"
                    r"this reported\s+claim stays V0/C0\."
                ),
                (
                    "Earlier certified geometries, evidence and reviews remain retained as "
                    "historical provenance, separate from this update's confirmation."
                ),
            ),
        ):
            # Standard prose formatting uses a typographic apostrophe. Recognize
            # that same declaration after formatting without relaxing its count.
            occurrences = " ".join(text.split()).replace("\u2019", "'").count(replacement)
            if occurrences > 1:
                raise ValueError("confirmed update needs exactly one assurance declaration")
            if occurrences == 0:
                text, count = re.subn(pattern, lambda _match, value=replacement: value, text)
                if count != 1:
                    raise ValueError("confirmed update needs its current assurance declaration")
    declarations = (
        (
            rf"\$s\({n}\) \\le [0-9.]+\$,\s+with exact side\s+\$[0-9]+(?:/[0-9]+)?\$",
            f"$s({n}) \\le {report['value']}$, with exact side ${fact['side']}$",
        ),
        (r"source print\s+\$[0-9.]+\$", f"source print ${fact['printed_side']}$"),
    )
    for pattern, replacement in declarations:
        text, count = re.subn(pattern, lambda _match, value=replacement: value, text)
        if count != 1:
            raise ValueError(
                "selected update needs exactly one current side/display declaration"
            )
    body = body[: section.start()] + text + body[section.end() :]
    if confirmed:
        # Earlier exact certificates still prove their weaker bounds. Make that time
        # scope explicit in each sentence rather than silently relabelling their sides.
        bound_pattern = re.compile(rf"s\({n}\)\s*\\le\s*([0-9]+\.[0-9]+)")
        for start, end in reversed(list(sentence_spans(body))):
            sentence = body[start:end]
            if (
                any(
                    Decimal(match.group(1)) > Decimal(report["value"])
                    for match in bound_pattern.finditer(sentence)
                )
                and re.search(r"\b(previously|was|until|superseded)\b", sentence, re.IGNORECASE)
                is None
            ):
                leading = len(sentence) - len(sentence.lstrip())
                history = sentence[leading:]
                history = re.sub(
                    r"^(The|That|This)\b", lambda match: match.group().lower(), history
                )
                body = body[:start] + sentence[:leading] + "Previously, " + history + body[end:]
        body = body.replace(
            "`verified_upper_bound` for this case is", "The earlier certified ceiling was"
        ).replace(
            "the tighter, unconfirmed SQUISH update", "the tighter, confirmed SQUISH update"
        )
    heading = "## The verified upper bound is a ceiling"
    # An earlier catalogue audit is reviewed history, not this update's disclosure.
    history = re.search(rf"\n{heading}\n.*?(?=\n## )", body, re.DOTALL)
    if history is not None and "earlier catalogue print" in history.group():
        body = (
            body[: history.start()]
            + history.group().replace(heading, "## Earlier catalogue ceiling", 1)
            + body[history.end() :]
        )
    verified = case["verified_upper_bound"]["value"]
    with localcontext() as context:
        context.prec = 28
        gap = Decimal(verified) - Decimal(report["value"])
    ceiling = ""
    if gap > 0:
        ceiling = (
            f"\n{heading}\n\nThe verified ceiling is $s({n}) \\le {verified}$, "
            "while the reported packing has\n"
            f"side ${report['value']}$, smaller by ${gap}$. "
            "The `verified_upper_bound` certifies a\n"
            f"ceiling, not the value of $s({n})$; `reported_upper_bound` records the stronger\n"
            "source claim, whose independent exact replay remains pending in this record.\n"
        )
    body = re.sub(rf"\n{heading}\n.*?(?=\n## )", lambda _match: "", body, flags=re.DOTALL)
    body = body.replace("\n## The lower bound", ceiling + "\n## The lower bound", 1)
    rendered = (
        "---\n"
        + yaml.safe_dump(document, sort_keys=False, allow_unicode=True, width=98)
        + "---\n"
        + body
    )
    return render_case_verifiers.refresh(rendered)


def adopt_selected_report(n: int, existing: str, generated: str) -> str:
    """Apply SQUISH's selected report to a genuine historical draft.

    Report geometry comes from the retained exact facts. Reviewed source-history prose,
    resources, evidence and blockers belong to the intake and remain editorial additions;
    ordinary lower lanes and their prose come from the generator. Rigidity is promoted
    afterwards by its existing owner. This is publication adaptation, not certification.
    """
    from devtools import render_case_verifiers  # noqa: PLC0415
    from devtools import squish_followup_packets as update  # noqa: PLC0415
    from devtools import squish_second_update_confirmation as confirmation  # noqa: PLC0415
    from devtools import squish_second_update_packets as second  # noqa: PLC0415
    from devtools import squish_upper_bound_packets as squish  # noqa: PLC0415

    coverage = safe_load(COVERAGE.read_text())
    selected = next((row for row in coverage["selected_overrides"] if row["n"] == n), None)
    if selected is None:
        return generated
    source = next(row for row in coverage["sources"] if row["id"] == selected["source_id"])
    if source["source_key"] == second.SOURCE_KEY:
        case = safe_load(existing.split("---\n", 2)[1])["packing"]
        adopter = (
            confirmation.adopt_verified
            if confirmation.EXACT_EVIDENCE in case["verified_upper_bound"]["evidence"]
            else second.adopt_report
        )
        return (
            adopter(n, existing, generated)
            if case["reported_upper_bound"]["source_key"] == second.SOURCE_KEY
            else generated
        )
    if source["source_key"] == update.SOURCE_KEY:
        return _adopt_selected_update(n, existing, generated)
    if n not in squish.NUMBERS or source["source_key"] != squish.source_key(n):
        return generated
    _, old_front, body = existing.split("---\n", 2)
    _, draft_front, draft_body = generated.split("---\n", 2)
    document = safe_load(old_front)
    case, draft = document["packing"], safe_load(draft_front)["packing"]
    if case["reported_upper_bound"]["source_key"] != source["source_key"]:
        return generated
    fact = squish.read_fact(n)
    confirmed = (
        f"E-{selected['source_id']}-exact-replay" in case["verified_upper_bound"]["evidence"]
    )
    report = deepcopy(case["reported_upper_bound"])
    report.update(
        value=(
            squish.verified_value(Fraction(fact["side"]), fact["printed_side"])
            if confirmed
            else fact["printed_side"]
        ),
        exact_form=fact["side"],
        algebraic_degree=1,
        minimal_polynomial=None,
        analytically_optimized=None,
        catalogue_rigid="not-stated",
        construction_method="unknown",
        tilt_angles_deg=None,
        found_by=[squish.AUTHOR],
        found_year=2026,
        improved_by=[],
        catalogue_pictured=False,
        source_key=squish.source_key(n),
        source_date=squish.RETRIEVED,
        retrieved_date=squish.RETRIEVED,
    )
    case["reported_upper_bound"] = report
    for field in ("reported_lower_bound", "verified_lower_bound", "reported_status", "status"):
        case[field] = draft[field]
    if confirmed:
        case["verified_upper_bound"].update(value=report["value"], exact_form=fact["side"])
    else:
        case["verified_upper_bound"] = draft["verified_upper_bound"]
    case["rigidity"] = None
    case["source_reviewed"] = squish.RETRIEVED
    lower = re.search(
        r"\n## The lower bound\n.*?(?=\n<!-- BEGIN verification code)", draft_body, re.DOTALL
    )
    if lower is None:
        raise ValueError("historical draft has no independently generated lower-bound section")
    body, replacements = re.subn(
        r"\n## The lower bound\n.*?(?=\n<!-- BEGIN verification code)",
        lambda _match: lower.group(),
        body,
        flags=re.DOTALL,
    )
    if replacements != 1:
        raise ValueError("selected SQUISH case needs exactly one generated lower-bound section")
    side = Fraction(fact["side"])
    numerator, denominator = side.numerator, side.denominator
    body, replacements = re.subn(
        r"S_n = \\frac\{[0-9]+\}\{[0-9]+\}",
        lambda _match: f"S_n = \\frac{{{numerator}}}{{{denominator}}}",
        body,
    )
    if replacements != 1:
        raise ValueError("selected SQUISH case needs exactly one rational-side declaration")
    label = (
        "The source" + chr(0x2019) + "s original finite decimal display is"
        if confirmed
        else "Its decimal display is"
    )
    body, replacements = re.subn(
        re.escape(label) + r"\s+\$[0-9.]+\$",
        lambda _match: f"{label} ${fact['printed_side']}$",
        body,
    )
    if replacements != 1:
        raise ValueError("selected SQUISH case needs exactly one source-display declaration")
    if confirmed:
        body, replacements = re.subn(
            r"The verified display is\s+\$[0-9.]+\$",
            lambda _match: f"The verified display is ${report['value']}$",
            body,
        )
        if replacements != 1:
            raise ValueError(
                "confirmed SQUISH case needs exactly one verified-display declaration"
            )
    heading = "## The verified upper bound is a ceiling"
    ceiling = ""
    verified = case["verified_upper_bound"]["value"]
    if not confirmed:
        with localcontext() as context:
            context.prec = 28
            gap = Decimal(verified) - Decimal(report["value"])
        ceiling = (
            f"\n{heading}\n\nThe verified ceiling is $s({n}) \\le {verified}$, "
            "while the reported packing has\n"
            f"side ${report['value']}$, smaller by ${gap}$. "
            "The `verified_upper_bound` certifies a\n"
            f"ceiling, not the value of $s({n})$; `reported_upper_bound` records the stronger\n"
            "source claim, whose independent exact replay remains pending in this record.\n"
        )
    body = re.sub(rf"\n{heading}\n.*?(?=\n## )", lambda _match: "", body, flags=re.DOTALL)
    body = body.replace("\n## The lower bound", ceiling + "\n## The lower bound", 1)
    rendered = (
        "---\n"
        + yaml.safe_dump(document, sort_keys=False, allow_unicode=True, width=98)
        + "---\n"
        + body
    )
    return render_case_verifiers.refresh(rendered)


def preserve_other_coverage(original: str, rendered: str, owned_counts: Collection[int]) -> str:
    """Update owned counts without reordering or rewriting another import's entries."""
    old, new = safe_load(original), safe_load(rendered)
    for name in ("selected_overrides", "superseded_reports"):
        replacement = {(row["n"], row["source_id"]): row for row in new[name]}
        rows = []
        for row in old[name]:
            key = row["n"], row["source_id"]
            if row["n"] not in owned_counts:
                rows.append(row)
                replacement.pop(key, None)
            elif key in replacement:
                rows.append(replacement.pop(key))
        rows.extend(row for row in replacement.values() if row["n"] in owned_counts)
        pattern = re.compile(rf"^{name}:.*\n(?:(?:  |    ).*\n)*", re.MULTILINE)
        if rows == old[name]:
            match = pattern.search(original)
            if match is None:
                raise ValueError(f"missing coverage list {name}")
            block = match.group()
        else:
            lines = [f"{name}:\n"]
            for row in rows:
                dumped = yaml.safe_dump(row, sort_keys=False, allow_unicode=True, width=88)
                lines.extend(
                    ("  - " if i == 0 else "    ") + line + "\n"
                    for i, line in enumerate(dumped.splitlines())
                )
            block = "".join(lines) if rows else f"{name}: []\n"
        rendered = pattern.sub(lambda _match, replacement=block: replacement, rendered, count=1)
    return rendered
