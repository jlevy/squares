#!/usr/bin/env python3
# ruff: noqa: RUF001 -- this module writes register prose, whose typography uses curly
# apostrophes and the corpus's other non-ASCII marks.
"""Carry Evan Daniel's exact optima of 48 known-best packings into the Frontier records.

Issue #375 asked for 48 upper bounds to be registered: at each count, ``s(n) <= S'``, where
``S'`` is the side of an exact rational certificate of the register's own known-best
packing at its exact optimum, 3.5e-13 to 5.0e-11 below the side its finder prints
(``devtools.evand_exact_certificates`` decides the certificates). The packings are their
finders': Francisco Couzo's at 46 counts and Joost de Winter's at ``n = 126`` and ``211``.
Daniel's solver removes the slack of their binary64 poses.

Registered as T-098 (provisional), a result of its own, by the rule the T-088 and T-092
imports applied: a release that lowers a side is a new entry, the earlier ones keep their
claims, and the case records say which is current. At each of the 48 counts this tool
moves both upper lanes to ``S'``, written out in full (each ``S'`` is a terminating
decimal of 30 places) with its exact fraction on the verified lane; keeps the finder in
``found_by`` and adds Daniel to ``improved_by``, as the catalogue credits an optimizer;
drops the conflict and blocker that recorded the earlier verified ceiling trailing the
printed side, since ``S'`` lies below it; and in the body points the opening sentence at
``S'``, removes the ceiling section, writes a section on the exact optimum before the
packing section, and puts the earlier certificate's "the verified upper bound" in the
past. The known-best witness, which the atlas pictures, stays the finder's binary64 pose:
the certificate's pose lies within the displacement its section states, and its side
within 1e-8 of the witness's, the atlas's own tolerance.

In ``source-coverage.yaml`` it selects the packet's report at the 48 counts and names it
as what supersedes every report it displaces there.

It is a layer over the tools that wrote these records first, and composes with them:
``devtools.apply_upper_bound_packets`` applies it after its own intake, and
``devtools.generate_frontier_case`` after the catalogue certificates, so that each of
their ``--check`` modes still reads the record as written. Applied to its own output it
changes nothing.

Usage, from ``packing/``:
    uv run --frozen --all-extras --group dev python -m devtools.apply_exact_optima
    uv run --frozen --all-extras --group dev python -m devtools.apply_exact_optima --check
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Mapping, Sequence
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

import yaml
from strif import atomic_write_text

from devtools import evand_exact_certificates as certificates
from devtools.migrate_math import markdown_math
from devtools.retained_data import read_retained_text
from sqpack.assurance import bounds_agree_at_declared_precision
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
COVERAGE = FRONTIER / "source-coverage.yaml"

RESULT = "T-098"
INTAKE = "2026-10-05"
AUTHOR = "Evan Daniel"
SOURCE_KEY = "[evand exact optima 2026-10-05]"
COVERAGE_ID = "evand-square-packing-2026-10-05"
REPORT = "E-evand-exact-optima-2026-10-05-report"
EXACT_REPLAY = "E-evand-exact-optima-2026-10-05-exact-replay"
SOURCE_REPLAY = "E-evand-exact-optima-2026-10-05-source-replay"
EVIDENCE = (REPORT, EXACT_REPLAY, SOURCE_REPLAY)
ISSUE = "https://github.com/jlevy/squares/issues/375"
PACKET_LINK = "../resources/web/evand-square-packing-2026-10-05/README.md"
RESOURCE = {
    "key": SOURCE_KEY,
    "role": "upper-bound-report",
    "local": "web/evand-square-packing-2026-10-05",
    "url": "https://github.com/evand/square-packing",
    "retrieved": True,
}
#: The evidence of the upper bounds the 48 counts held before: the certified packets'
#: entries (devtools.apply_upper_bound_packets.REGISTRATIONS) and the catalogue's. A
#: conflict or blocker citing one is about the side this import replaces.
EARLIER_UPPER = frozenset(
    {
        "E-franciscouzo-2026-09-27-report",
        "E-franciscouzo-2026-09-27-exact-replay",
        "E-franciscouzo-2026-09-27-interval-replay",
        "E-franciscouzo-2026-10-03-report",
        "E-franciscouzo-2026-10-03-exact-replay",
        "E-franciscouzo-2026-10-03-interval-replay",
        "E-n211-de-winter-report",
        "E-n211-de-winter-exact-replay",
        "E-n211-de-winter-interval-replay",
        "E-kingbird-upper-register",
        "E-kingbird-grid-completeness",
    }
)
SECTION = "## The exact optimum"
CEILING_HEADING = "## The verified upper bound is a ceiling"
PACKING_HEADING = "## The packing"
#: What the source's own report says of its exact point, by its `status`.
KKT = (
    "The source reports the exact point as a KKT local minimum: multipliers that keep "
    "it in equilibrium, a reduced Hessian positive definite once its exact flat "
    "motions are set aside (its per-count report), and no "
    "first-order descent across corner-to-corner contacts, each computed numerically at "
    "that point; none of that is verified here, and it bears on this packing alone, not "
    "on `s({n})`."
)
BOUND_ONLY = (
    "The source reports the exact point as a certified bound only: its numerical checks "
    "do not show it to be a local minimum of the side."
)
#: The second-order report `KKT` restates, as the source's per-count `second` field
#: writes it at each of the 44 counts it reports as KKT local minima.
PD_MODULO_FLAT = re.compile(
    r"local minimum of S, strict modulo \d+ exact flat motions "
    r"\(PD on the rest of null\(J_A\)\)"
)
KKT_STATUS = "KKT local min"
AI_SENTENCE = (
    "On jlevy/squares#375 its author wrote that the solver, its checkers and the batch "
    "“were written with Claude (Anthropic) as a coding and research agent, directed and "
    "reviewed by me.”"
)


# --------------------------------------------------------------------------------------
# What the packet says
# --------------------------------------------------------------------------------------


@cache
def sides() -> dict[int, Fraction]:
    """Each improving count's certified side, read from its retained certificate."""
    return {
        n: certificates.parse(
            certificates.certificate_path(certificates.CERTS, n).read_text(encoding="utf-8"),
            expected_n=n,
        ).side
        for n in certificates.IMPROVING
    }


def side_text(n: int) -> str:
    """``S'`` written out in full; every one of the 48 is a terminating decimal."""
    text = certificates.terminating_decimal(sides()[n])
    if text is None:
        raise ValueError(f"n={n}: the certified side does not terminate in decimal")
    return text


@cache
def comparison() -> dict[int, Mapping[str, Any]]:
    """The committed comparison with the earlier holders, by count."""
    receipt = json.loads(certificates.COMPARISON_RECEIPT.read_text(encoding="utf-8"))
    return {int(row["n"]): row for row in receipt["rows"]}


@cache
def reports() -> dict[int, tuple[str, str]]:
    """The source's own report of each improving count's exact point, from its retained
    results: its `status` and its second-order `second`. Rows at other counts are
    skipped by their `n` alone."""
    rows = json.loads(read_retained_text(certificates.RESULTS_JSON))
    improving = set(certificates.IMPROVING)
    return {
        int(row["n"]): (str(row.get("status", "")), str(row.get("second", "")))
        for row in rows
        if int(row["n"]) in improving
    }


def report_sentence(n: int, status: str, second: str) -> str:
    """What the record says of the source's report at `n`. The KKT sentence says the
    reduced Hessian is positive definite once the exact flat motions are set aside, so
    a count the source calls a KKT local minimum on any other second-order report is
    refused rather than described (fix check of T-098's review, FX-3)."""
    if status != KKT_STATUS:
        return BOUND_ONLY
    if not PD_MODULO_FLAT.match(second):
        raise ValueError(
            f"n={n}: reported as a KKT local minimum, but its second-order report is not "
            f"positive definite modulo exact flat motions: {second!r}"
        )
    return KKT.format(n=n)


# --------------------------------------------------------------------------------------
# Front matter
# --------------------------------------------------------------------------------------


def _set_block(front: str, name: str, value: object) -> str:
    from devtools.apply_upper_bound_packets import set_block  # noqa: PLC0415

    return set_block(front, name, value)


def _cites(item: Mapping[str, Any], evidence: frozenset[str]) -> bool:
    return bool(set(item.get("evidence") or []) & evidence)


def front_matter(n: int, front: str) -> str:
    """The front matter with both upper lanes at the certified side."""
    payload = safe_load(front)["packing"]
    reviewed = max(str(payload.get("source_reviewed") or ""), INTAKE)
    front = re.sub(
        r"^  source_reviewed: .*$",
        f"  source_reviewed: '{reviewed}'",
        front,
        count=1,
        flags=re.MULTILINE,
    )
    current = payload["reported_upper_bound"]
    value = side_text(n)
    reported = {
        **current,
        "value": value,
        "exact_form": None,
        "algebraic_degree": None,
        "minimal_polynomial": None,
        # A catalogue's word, which this source does not use; the body says what it reports.
        "analytically_optimized": None,
        "catalogue_rigid": "not-stated",
        "improved_by": [AUTHOR],
        "source_key": SOURCE_KEY,
        "source_date": INTAKE,
        "retrieved_date": INTAKE,
        "evidence": [REPORT],
    }
    front = _set_block(front, "reported_upper_bound", reported)
    front = _set_block(
        front,
        "verified_upper_bound",
        {
            "value": value,
            "exact_form": certificates.literal(sides()[n]),
            "evidence": [EXACT_REPLAY, SOURCE_REPLAY],
        },
    )
    # The source conjectures no optimum, and a catalogue's conjecture above the certified
    # side would contradict the record (review finding EX-1, n = 126).
    front = _set_block(front, "conjectured_optimum", None)
    evidence = list(payload["evidence"])
    front = _set_block(
        front, "evidence", [item for item in EVIDENCE if item not in evidence] + evidence
    )
    front = _set_block(
        front,
        "conflicts",
        [item for item in payload["conflicts"] if not _cites(item, EARLIER_UPPER)],
    )
    front = _set_block(
        front,
        "blockers",
        [
            item
            for item in payload["blockers"]
            if not (item.get("kind") == "mathematics" and _cites(item, EARLIER_UPPER))
        ],
    )
    kept = [RESOURCE if item["key"] == SOURCE_KEY else item for item in payload["resources"]]
    if all(item["key"] != SOURCE_KEY for item in kept):
        kept.insert(0, RESOURCE)
    return _set_block(front, "resources", kept)


# --------------------------------------------------------------------------------------
# Body
# --------------------------------------------------------------------------------------


def _section_span(body: str, heading: str) -> tuple[int, int] | None:
    start = body.find(f"{heading}\n")
    if start < 0:
        return None
    end = body.find("\n## ", start + len(heading))
    return start, (len(body) if end < 0 else end + 1)


def _finder(payload: Mapping[str, Any]) -> str:
    found = list(payload["reported_upper_bound"].get("found_by") or [])
    if len(found) != 1:
        raise ValueError(f"n={payload['n']}: expected one finder, found {found}")
    return found[0]


def opener(body: str, n: int, finder: str, lower: str) -> str:
    """The opening sentence pointed at the certified side, in code or math form."""
    from devtools.generate_frontier_case import (  # noqa: PLC0415
        display_first_party_upper,
        display_gap,
    )

    shown = display_first_party_upper(side_text(n))
    who = f"{finder}’s at {AUTHOR}’s exact optimum ({RESULT})"
    body, count = re.subn(
        rf"The\s+best\s+known\s+(?:published\s+)?packing(?:,\s+[^`$]*?,)?\s+gives\s+"
        rf"(?:`s\({n}\)\s+≤\s+[^`]+`|\$s\({n}\)\s+\\le\s+[^$]+\$)",
        f"The best known published packing, {who}, gives `s({n}) ≤ {shown}`",
        body,
        count=1,
    )
    if count != 1:
        raise ValueError(f"n={n}: no opening sentence names the best known packing")
    return re.sub(
        r"leaving\s+a\s+gap\s+of\s+(?:`[0-9.]+`|\$[0-9.]+\$)",
        f"leaving a gap of `{display_gap(side_text(n), lower)}`",
        body,
        count=1,
    )


def _scientific(value: float) -> str:
    return f"{value:.1e}".replace("e-0", "e-")


def _bound(value: float) -> str:
    """An upper bound in two significant digits, rounded up so that it stays one."""
    return _scientific(certificates.round_up(float(value), 2))


def section(n: int, finder: str) -> str:
    """The section on the exact optimum, placed before the packing section."""
    from devtools.generate_frontier_case import display_first_party_upper  # noqa: PLC0415

    row = comparison()[n]
    pose = row["pose"]
    shown = display_first_party_upper(side_text(n))
    printed = (
        f"the side the Kingbird catalogue prints for {finder}’s packing"
        if row["earlier_source_key"] == "[Kingbird]"
        else f"the side {finder} prints"
    )
    count, free = int(pose["moved_count"]), int(pose["moved_listed_free"])
    motion = (
        "Square for square, its pose lies within "
        f"`{_bound(pose['largest_centre_displacement'])}` of the binary64 pose the "
        "atlas pictures for this count."
    )
    if count:
        others = count - free
        nonfree = _bound(pose["nonfree_moved_largest_centre_displacement"])
        if not others:
            parts = "all of them squares the source lists as carrying no force"
        elif not free:
            parts = f"none of them listed by the source as free, each by at most `{nonfree}`"
        else:
            parts = (
                f"{free} of them squares the source lists as carrying no force and the "
                f"other {others} by at most `{nonfree}`"
            )
        motion += (
            f" {count} {'square moves' if count == 1 else 'squares move'} by more than "
            f"`1e-8`, {parts}; every other square moves by at most "
            f"`{_bound(pose['unmoved_largest_centre_displacement'])}`."
        )
    below = _scientific(float(row["below_printed_side_by"]))
    if row["earlier_result"] is None:
        trailing = (
            " No certificate of the packing was on record before, so the verified ceiling "
            f"here was the trivial grid bound `{row['earlier_verified_value']}` until this one."
        )
    elif bounds_agree_at_declared_precision(
        {"value": row["earlier_printed_side"], "exact_form": None},
        {"value": row["earlier_verified_value"], "exact_form": None},
    ):
        trailing = ""
    else:
        trailing = (
            " The certified ceiling this count held before, "
            f"`{row['earlier_verified_value']}`, lay above that printed side, which was not "
            "certified for its binary64 pose "
            f"({row['earlier_result']}); the exact optimum lies below both."
        )
    first = (
        f"{AUTHOR}’s [`square-packing`]({PACKET_LINK}) published on 5 October 2026 an exact "
        f"rational certificate of this packing at its exact optimum ({RESULT}): the same {n} "
        f"squares in a square of side `{shown}`, `{below}` below {printed}.{trailing} "
        f"{motion} The known-best witness this record lists is that binary64 pose, posed at "
        "its finder’s larger side; the side above is witnessed by the certificate itself. "
        f"{AUTHOR}’s solver moves the binary64 pose to a nearby exact KKT point of the "
        "problem of minimizing the side under non-overlap, computed at 80 digits, and "
        "rounds it outward to rationals, each square a rational centre and a rational "
        "`t = tan(θ/2)`."
    )
    second = (
        "This repository decides the certificate exactly. Converted without rounding, "
        "every pair and every wall is decided over `ℚ` twice, by `sqpack`’s exact "
        "separating-axis test and by an independent checker that shares no code with it, "
        "and the source’s own two checkers, run here as retained, accept it as well "
        f"([receipts]({PACKET_LINK}#replayed-here)). That proves `s({n}) ≤ {shown}`, the "
        "verified upper bound; it says nothing about optimality. "
        + report_sentence(n, *reports()[n])
        + f" {AI_SENTENCE}"
    )
    return f"{SECTION}\n\n{first}\n\n{second}\n\n"


#: The earlier certificate's paragraph names it the verified upper bound; after this
#: import that is history. Math form, as `markdown_math` leaves it, and code form.
_EARLIER_VERIFIED = re.compile(
    r"(That\s+proves\s+(?:\$s\(\d+\)\s+\\le\s+[^$]+\$|`s\(\d+\)\s+≤\s+[^`]+`)),\s+the\s+"
    r"verified\s+upper\s+bound;"
)
_EARLIER_SAME = re.compile(r"gives\s+the\s+same\s+verified\s+upper\s+bound")


def body_text(n: int, body: str, payload: Mapping[str, Any]) -> str:
    finder = _finder(payload)
    body = opener(body, n, finder, str(payload["verified_lower_bound"]["value"]))
    for heading in (CEILING_HEADING, SECTION):
        span = _section_span(body, heading)
        if span is not None:
            body = body[: span[0]] + body[span[1] :]
    # The earlier certificate's sentences are put in the past before the new section,
    # which says "the verified upper bound" of its own, goes in.
    body = _EARLIER_VERIFIED.sub(
        rf"\1, which was the verified upper bound until {AUTHOR}’s exact optimum "
        "above replaced it;",
        body,
    )
    body = _EARLIER_SAME.sub("gives the same bound", body)
    span = _section_span(body, PACKING_HEADING)
    if span is None:
        raise ValueError(f"n={n}: no packing section")
    return body[: span[0]] + section(n, finder) + body[span[0] :]


def apply_case(n: int, text: str) -> str:
    """One case record with the exact optimum written over it; others unchanged."""
    if n not in certificates.IMPROVING:
        return text
    from devtools.source_supersession import preserve_selected_case  # noqa: PLC0415

    if preserve_selected_case(n, text, {COVERAGE_ID}):
        return text
    _, front, body = text.split("---\n", 2)
    payload = safe_load(front)["packing"]
    written = markdown_math(body_text(n, body, payload))
    return f"---\n{front_matter(n, front)}---\n{written}"


# --------------------------------------------------------------------------------------
# Source coverage
# --------------------------------------------------------------------------------------


def coverage_entries(name: str, entries: Sequence[Mapping[str, Any]]) -> str:
    """A top-level list of the coverage record, laid out as the packet intake lays it."""
    if not entries:
        return f"{name}: []\n"
    lines = [f"{name}:\n"]
    for entry in entries:
        dumped = yaml.safe_dump(dict(entry), allow_unicode=True, sort_keys=False, width=88)
        for index, line in enumerate(dumped.splitlines()):
            lines.append(("  - " if index == 0 else "    ") + line + "\n")
    return "".join(lines)


def coverage_text(text: str) -> str:
    """The coverage record with the packet's report selected at the 48 counts."""
    original = text
    coverage = safe_load(text)
    from devtools.source_supersession import (  # noqa: PLC0415
        preserve_other_coverage,
        superseded_counts,
    )

    counts = set(certificates.IMPROVING) - superseded_counts(coverage, {COVERAGE_ID})
    previous = {
        entry["n"]: entry
        for entry in coverage["selected_overrides"]
        if entry["n"] in counts and entry["source_id"] != COVERAGE_ID
    }
    overrides = [entry for entry in coverage["selected_overrides"] if entry["n"] not in counts]
    for n in sorted(counts):
        row = comparison()[n]
        earlier = (
            "the Kingbird catalogue's side for Joost de Winter's packing"
            if row["earlier_source_key"] == "[Kingbird]"
            else f"{row['earlier_author']}'s printed side ({row['earlier_result']})"
        )
        overrides.append(
            {
                "n": n,
                "source_id": COVERAGE_ID,
                "value": side_text(n),
                "evidence": REPORT,
                "reason": (
                    f"The exact optimum of the same packing, certified here ({RESULT}), "
                    f"below {earlier}."
                ),
            }
        )
    overrides.sort(key=lambda entry: entry["n"])
    superseded = []
    for entry in coverage.get("superseded_reports") or []:
        if entry["n"] in counts and entry["superseded_by"] != COVERAGE_ID:
            superseded.append(
                {
                    **entry,
                    "superseded_by": COVERAGE_ID,
                    "reason": (
                        f"{entry['reason'].rstrip('.')}; since {INTAKE} the selected report "
                        f"is {AUTHOR}'s exact optimum of that packing ({RESULT})."
                    ),
                }
            )
        else:
            superseded.append(entry)
    for n, entry in sorted(previous.items()):
        superseded.append(
            {
                "n": n,
                "source_id": entry["source_id"],
                "value": entry["value"],
                "superseded_by": COVERAGE_ID,
                "reason": (
                    f"Superseded on {INTAKE} by {AUTHOR}'s exact optimum of the same "
                    f"packing, certified here ({RESULT})."
                ),
            }
        )
    superseded.sort(key=lambda entry: (entry["n"], entry["source_id"]))
    text = re.sub(
        r"^selected_overrides:.*\n(?:(?:  |    ).*\n)*",
        lambda _match: coverage_entries("selected_overrides", overrides),
        text,
        count=1,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^superseded_reports:.*\n(?:(?:  |    ).*\n)*",
        lambda _match: coverage_entries("superseded_reports", superseded),
        text,
        count=1,
        flags=re.MULTILINE,
    )
    return preserve_other_coverage(original, text, counts)


# --------------------------------------------------------------------------------------
# Command line
# --------------------------------------------------------------------------------------


def _normalized(text: str) -> str:
    from devtools.apply_upper_bound_packets import normalized  # noqa: PLC0415

    return normalized(text)


def main(argv: Sequence[str] | None = None) -> int:
    from devtools import render_case_verifiers  # noqa: PLC0415

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report drift without writing")
    args = parser.parse_args(argv)
    drift: list[Path] = []
    for n in certificates.IMPROVING:
        path = FRONTIER / f"n-{n:03d}.md"
        text = path.read_text(encoding="utf-8")
        rendered = render_case_verifiers.refresh(apply_case(n, text))
        if _normalized(rendered) != _normalized(text):
            drift.append(path)
            if not args.check:
                atomic_write_text(path, rendered)
    text = COVERAGE.read_text(encoding="utf-8")
    updated = coverage_text(text)
    if updated != text:
        drift.append(COVERAGE)
        if not args.check:
            atomic_write_text(COVERAGE, updated)
    for path in drift:
        print(("drift: " if args.check else "wrote: ") + str(path.relative_to(ROOT)))
    if not drift:
        print(f"the {len(certificates.IMPROVING)} records and the coverage record are current")
    return 1 if args.check and drift else 0


if __name__ == "__main__":
    sys.exit(main())
