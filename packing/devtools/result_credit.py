"""Credit and lineage for a registered result, read from the record.

`frontier/RESULTS.md` (`devtools.render_results`) and the site's overview
(`devtools.overview_data`) print the same credit cell and group by the same
lineage, so both read them here and cannot credit a result differently. Both also
print a result's `regularizations` in one sentence each (`regularization_sentence`):
whose packing the certificate regularizes, and who regularized it.

Every credit names people, in one form (attribution.md, Credit Text and Lineage):
`X`, or `X after Y, Z` where X's result rests directly on Y's and Z's proof,
method or tool. A result by others takes its line from its sources in
`resources/bibliography.yaml`, the one home of that text. A result of this project is
credited to `PROJECT_AUTHOR`, and its `after` is the result's own `builds_on.credit`
in `frontier/results.yaml`, which `devtools.check_results` holds to the sources the
result's evidence cites. Nothing here restates either.
"""

from __future__ import annotations

import html
from collections.abc import Mapping
from typing import Any

from devtools.build_bound_citations import RECENT_SINCE
from devtools.contributor_credit import render_credit
from sqpack.contributor_occurrences import CreditOrigin

#: The groups results by others fall into, in reading order, by the lineage their
#: sources carry in the bibliography.
OTHERS = (
    ("builds-on-project", "Building on this project"),
    ("credits-project", "Crediting this project second-hand"),
    ("independent", "Independent of this project"),
    (None, "Published before this project began"),
)


#: The name this project's own results are credited under, the same surname form every
#: other author gets (the owner, 2026-10-01). It is also how other sources' credit lines
#: name this project: `Overbeck after Levy, Guzhou0806, Mira`.
PROJECT_AUTHOR = "Levy"

#: The generator-owned credit is reviewed as a literal source field, like a record's.
PROJECT_AUTHOR_ORIGIN = CreditOrigin(
    "packing/devtools/result_credit.py", "constants", "/PROJECT_AUTHOR"
)


def is_first_party(record: Mapping[str, Any]) -> bool:
    """Whether a result is this project's own, credited to `PROJECT_AUTHOR`: its entry
    names no `attribution`."""
    return not record.get("attribution")


def credit_sources(record: Mapping[str, Any]) -> tuple[str, ...]:
    """The bibliography keys whose credit a result prints, in the attribution's order.
    None for a result of this project, whose `after` names are its own entry's."""
    if is_first_party(record):
        return ()
    return tuple(record["attribution"]["source_keys"])


def credit_line(record: Mapping[str, Any], sources: Mapping[str, Mapping[str, Any]]) -> str:
    """Who a result is credited to. `RESULTS.md` and the site's overview print this cell.

    For a result by others: its sources' credit lines, each once, in the order the
    attribution names them. For a result of this project: `Levy`, or `Levy after …` with
    the names its `builds_on.credit` lists, in that order.
    """
    if is_first_party(record):
        after = (record.get("builds_on") or {}).get("credit") or []
        return PROJECT_AUTHOR + (f" after {', '.join(after)}" if after else "")
    lines = [
        sources[key].get("credit") or ", ".join(sources[key]["authors"])
        for key in credit_sources(record)
    ]
    return "; ".join(dict.fromkeys(lines)).replace("|", r"\|")


def result_credit_html(
    record: Mapping[str, Any], sources: Mapping[str, Mapping[str, Any]], *, prefix: str = ""
) -> str:
    """Compose source-addressed credits, retaining ambiguous deduplicated lines as text."""
    if is_first_party(record):
        author = render_credit(PROJECT_AUTHOR_ORIGIN, PROJECT_AUTHOR, prefix=prefix)
        after = (record.get("builds_on") or {}).get("credit") or []
        joined = ", ".join(
            render_credit(
                CreditOrigin(
                    "packing/frontier/results.yaml", record["id"], f"/builds_on/credit/{index}"
                ),
                name,
                prefix=prefix,
            )
            for index, name in enumerate(after)
        )
        return author + (f" after {joined}" if after else "")
    rendered: dict[str, str] = {}
    for key in credit_sources(record):
        source = sources[key]
        if source.get("credit"):
            text = source["credit"]
            markup = render_credit(
                CreditOrigin("packing/resources/bibliography.yaml", key, "/credit"),
                text,
                prefix=prefix,
            )
        else:
            text = ", ".join(source["authors"])
            markup = ", ".join(
                render_credit(
                    CreditOrigin(
                        "packing/resources/bibliography.yaml", key, f"/authors/{index}"
                    ),
                    name,
                    prefix=prefix,
                )
                for index, name in enumerate(source["authors"])
            )
        if text in rendered and rendered[text] != markup:
            # Plain-string deduplication cannot authorize one of conflicting identity joins.
            rendered[text] = html.escape(text)
        else:
            rendered.setdefault(text, markup)
    return "; ".join(rendered.values())


def source_lineage(
    record: Mapping[str, Any], sources: Mapping[str, Mapping[str, Any]]
) -> str | None:
    """The group an attributed result reads under: its sources' lineage, if recent.

    Also the relation `render_recent_results.relation` names, read through this function.
    """
    attribution = record["attribution"]
    if attribution["published"] < RECENT_SINCE.isoformat():
        return None
    lineages = {sources[key].get("lineage") for key in attribution["source_keys"]}
    for lineage, _ in OTHERS:
        if lineage in lineages:
            return lineage
    return None


#: The typographic apostrophe the generated views use (`render_results.APOSTROPHE`).
_APOSTROPHE = "\u2019"
#: How a regularization's `side` reads: at the packing's own side, or after an exact solve.
_SIDES = {"same": "at its own side", "solved": "solved to its side"}
#: How the basis of a regularization's `identity` reads: whose the claim of identity is.
_BASES = {
    "source-claim": f"identity: the source{_APOSTROPHE}s claim",
    "measured": "identity: measured here",
}


def regularizer(by: str, sources: Mapping[str, Mapping[str, Any]]) -> str:
    """Who made a regularization, as a credit line names them: the names before `after`
    in its source's credit, or this project's author for its own (`project`)."""
    if by == "project":
        return PROJECT_AUTHOR
    source = sources[by]
    return str(source.get("credit") or ", ".join(source["authors"])).split(" after ")[0]


def _number(value: float) -> str:
    return format(value, "g")


def _plural(count: int, one: str, many: str) -> str:
    return f"{count} {one if count == 1 else many}"


def regularization_sentence(
    item: Mapping[str, Any], sources: Mapping[str, Mapping[str, Any]]
) -> str:
    """One item of a result's `regularizations` as a reader is told it: the count, whose
    packing it regularizes and who regularized it, then the method, this project's
    modifications to Evan Daniel's regularizer where the item names them and what of them
    it does not record, the side and the earlier result whose certificate first stated it
    where the item names one (`first_certified_in`), what the regularization changed, and
    what the identity rests on with what was measured here.
    `n = 70: a regularization of T-125's packing by Daniel (fewest; solved to its side;
    rotation groups merged by up to 0.93°; identity: the source's claim; ...).`"""
    parts = [str(item["method"])]
    if "modifications" in item:
        modifications = ", ".join(str(found) for found in item["modifications"])
        unrecorded = [str(found) for found in item.get("modifications_unrecorded") or []]
        if modifications:
            parts.append(f"the project{_APOSTROPHE}s modifications: {modifications}")
        elif unrecorded:
            parts.append(f"none of the project{_APOSTROPHE}s modifications established")
        else:
            parts.append("unmodified")
        if unrecorded:
            parts.append(f"{' and '.join(unrecorded)} not recorded")
    side = _SIDES[str(item["side"])]
    if item.get("first_certified_in"):
        side += f", first certified in {item['first_certified_in']}"
    parts.append(side)
    changes = item.get("changes")
    if changes:
        changed = []
        if changes.get("merged_rotation_groups_deg"):
            merged = _number(changes["merged_rotation_groups_deg"])
            changed.append(f"rotation groups merged by up to {merged}\u00b0")
        if changes.get("straightened"):
            changed.append(
                _plural(changes["straightened"], "free square", "free squares")
                + " straightened"
            )
        if changes.get("re_angled"):
            changed.append(
                _plural(changes["re_angled"], "free angle", "free angles") + " moved"
            )
        parts.append(", ".join(changed) or "no angle changed")
    identity = item["identity"]
    parts.append(_BASES[str(identity["basis"])])
    if "one_to_one" in identity:
        paired = "" if identity["one_to_one"] else "not "
        parts.append(f"nearest centres {paired}one to one")
    moved, largest = identity.get("moved"), identity.get("max_move")
    if moved is not None:
        squares = _plural(moved, "square", "squares") + " moved"
        parts.append(squares + (f", at most {_number(largest)}" if largest is not None else ""))
    elif largest is not None:
        parts.append(f"moves up to {_number(largest)}")
    if "max_turn_deg" in identity:
        turn = identity["max_turn_deg"]
        parts.append(f"turns up to {_number(turn)}\u00b0" if turn else "no square turned")
    return (
        f"n = {item['n']}: a regularization of {item['of']}{_APOSTROPHE}s packing by "
        f"{regularizer(str(item['by']), sources)} ({'; '.join(parts)})."
    )
