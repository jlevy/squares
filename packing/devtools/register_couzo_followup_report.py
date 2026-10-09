"""Register Couzo's five 2d32a6e follow-up claims without changing selected cases.

The derived exact facts and the complete fifteen-job native receipt are admitted before
any record is planned. Every proposed record is checked against its enforced schema
before the first write, so a late refusal writes nothing. Independent review,
historical source-house integration and confirmation remain required before adoption;
this registration states the claim as reported, at V0/C0.

From ``packing/``: ``python -m devtools.register_couzo_followup_report``.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from devtools import couzo_followup_reports as reports
from devtools.register_couzo_refinement_report import append, validate
from devtools.register_refinement_reports import FOOTER, dump, save
from sqpack.yamlio import safe_load

REPO = reports.REPO
DAY = "2026-10-09"
PUBLISHED = "2026-10-08"
RESULT = "T-130"
REPORT = reports.REPORT_EVIDENCE
BEAD = "think-88r0"
ISSUE = 451
REQUEST_KEY = "five-follow-up-refinements-2d32a6e"
PACKET_PATH = reports.PACKET.relative_to(REPO).as_posix()
WATCH_URL = reports.SOURCE
DISCLOSURE = (
    "The source author reports passes from Evan Daniel's verify_cert.py and a copy of "
    "this repository's sqpack verifier, so the exact_verify route overlaps that source "
    "checker. The second maintained rational-geometry route is a separate deciding "
    "implementation; both routes share certificate parsing, half-angle conversion, "
    "Fraction arithmetic and the separating-axis method. No two independent methods, "
    "human oversight or optimality is claimed."
)
REPLAY = (
    "A separate complete repository replay is retained: five positives and ten "
    "duplicate-square and outside-container controls passed their required outcomes on "
    "both routes, 384846 pair decisions in 79.55 seconds wall with two workers and "
    "unchanged kernel limits."
)
CLAIM = (
    "Five complete rational source certificates report finite upper-bound improvements "
    "at 84,86,105,175,270. Complete native feasibility outcomes are retained separately; "
    "selected standing cases are unchanged pending independent review, historical "
    "source-house integration and record review."
)


def rows() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    scope = {"n_values": list(reports.NUMBERS)}
    evidence = {
        "id": REPORT,
        "claim": "upper-bound",
        "scope": scope,
        "assurance": "reported",
        "reported_method": "exact-algebraic",
        "performed_by": "source-author",
        "relationship_to_generator": "same-implementation",
        "origin": "external",
        "novelty": "previously-published",
        "source_key": reports.SOURCE_KEY,
        "certificate": PACKET_PATH + "/facts/",
        "replay_status": "not-attempted",
        "verifiers": [],
        "source_reviewed": DAY,
        "limitations": (
            "This atom records the source author's report of five exact rational "
            "certificates at 2d32a6e. The packet keeps derived exact facts that rebuild "
            "each pinned certificate blob, not the source bytes. "
            + REPLAY
            + " Independent review, historical source-house integration and confirmation "
            "remain pending. Author KKT and no-descent statements are not checked. "
            + DISCLOSURE
        ),
    }
    result = {
        "id": RESULT,
        "kind": "upper-bound",
        "registered": DAY,
        "headline": "Five follow-up rational refinements from Francisco Couzo",
        "claim": CLAIM,
        "scope": scope,
        "verification": "V0",
        "confirmation": "C0",
        "significance": {
            "score": 3,
            "rationale": "Five smaller finite construction sides; no lower bound or optimum.",
            "scored": DAY,
            "by": "think-88r0 Couzo follow-up import",
        },
        "novelty": "previously-published",
        "attribution": {"source_keys": [reports.SOURCE_KEY], "published": PUBLISHED},
        "evidence": [REPORT],
        "artifacts": [
            PACKET_PATH + "/README.md",
            PACKET_PATH + "/acquisition/sources.json",
            *(reports.fact_path(n).relative_to(REPO).as_posix() for n in reports.NUMBERS),
            PACKET_PATH + "/receipts/exact-certification.json.xz",
            "packing/devtools/couzo_followup_reports.py",
        ],
        "controls": ["packing/tests/test_couzo_followup_reports.py"],
        "notes": (
            "All five complete certificates are kept as derived exact facts that rebuild "
            "each pinned blob; no upstream byte is retained. "
            + REPLAY
            + "\n\nThe earlier issue451 n105 certificate (T-128) stays retained with its own "
            "replay outcomes; the new n105 side is smaller by exactly "
            "262896871797134956129927589/200000000000000000000000000000. Ryan Xu's T-125 "
            "certificates at 84, 86, 105 and 175 and Evan Daniel's T-119 certificate at 270 "
            "remain the selected and verified ceilings. The source seeds 84, 86, 105 and "
            "175 from Ryan Xu's #432 packings and 270 from Evan Daniel's #399 packing, "
            "refined by Couzo's basin hopping and, at 175, David Ellsworth's "
            "refine_packing and Evan Daniel's fq; Daniel's exact contact solver wrote the "
            "certificates.\n\n" + DISCLOSURE
        ),
        "next_rung": (
            "Independently review the retained replay, preserve each complete historical "
            "source house (Ryan Xu at 84, 86, 105 and 175; Evan Daniel at 270) before any "
            "selected-house replacement, then record source-specific adoption and "
            "confirming evidence. Final exact-head CI remains required."
        ),
    }
    source = {
        "id": reports.SOURCE_ID,
        "title": "Francisco Couzo's five follow-up rational refinements at 2d32a6e",
        "role": "source-repository",
        "url": reports.SOURCE + "/tree/" + reports.REVISION,
        "local": reports.PACKET.relative_to(REPO / "packing").as_posix(),
        "source_key": reports.SOURCE_KEY,
        "scope": scope,
        "reviewed": DAY,
        "source_date": PUBLISHED,
        "disposition": "current-report",
        "replay_disposition": "case-specific",
        "represented_by": [
            "frontier/results.yaml",
            reports.sources_path().relative_to(REPO / "packing").as_posix(),
        ],
        "evidence": [REPORT],
        "notes": (
            "All five complete claims and their exact sides are kept as derived exact facts "
            "with the complete pinned tree; no upstream byte is retained. T-130 records the "
            "aggregate source report. All fifteen native jobs have full outcomes. No "
            "selected override or superseded claim is created at this source-only stage; "
            "current cases and earlier source ownership remain unchanged. The seven other "
            "certificates at this commit are byte-identical to the issue451 originals."
        ),
    }
    request = {
        "key": REQUEST_KEY,
        "claim": CLAIM,
        "source": reports.COMMENT,
        "register": [RESULT],
    }
    return evidence, result, source, request


def bibliography_row() -> dict[str, Any]:
    return {
        "key": reports.SOURCE_KEY,
        "authors": ["Couzo"],
        "year": 2026,
        "venue": "GitHub",
        "dated": PUBLISHED,
        "lineage": "builds-on-project",
        "credit": "Couzo after Xu, Daniel, Ellsworth, Levy",
        "short_credit": "Couzo after Xu et al.",
        "note": (
            "Five complete exact certificates at " + reports.REVISION + ", refined from "
            "Xu's #432 and Daniel's #399 packings with Ellsworth's refine_packing and "
            "Daniel's fq, and written by Daniel's exact contact solver. The source checks "
            "with Squares Project (Levy) verification code; this project lineage is not "
            "independent. Derived exact facts only; no upstream byte is retained. "
            "No optimizer/local/global claims."
        ),
    }


def _issue_block(text: str, number: int) -> tuple[int, int]:
    start = text.index(f"\n  - number: {number}\n") + 1
    following = re.search(r"^  - number: \d+$|^\S", text[start + 1 :], re.MULTILINE)
    end = len(text) if following is None else start + 1 + following.start()
    return start, end


def _list_end(block: str, field: str) -> int:
    """The offset just past the last item of a four-space-indented list field."""
    match = re.search(rf"^    {field}:\n", block, re.MULTILINE)
    if match is None:
        raise ValueError(f"issue entry lacks {field}")
    if not block[match.end() :].startswith("    - "):
        raise ValueError(f"issue entry {field} is not a block list")
    following = re.search(r"^    [A-Za-z_]", block[match.end() :], re.MULTILINE)
    if following is None:
        raise ValueError(f"issue entry field {field} is not followed by another field")
    return match.end() + following.start()


def request_text(text: str, request: dict[str, Any]) -> str:
    """Add one result and the import bead to the existing issue entry, nothing else."""
    before = safe_load(text)
    entry = next(item for item in before["issues"] if item["number"] == ISSUE)
    if any(row["key"] == REQUEST_KEY for row in entry["results"]):
        return text
    start, end = _issue_block(text, ISSUE)
    block = text[start:end]
    at = _list_end(block, "results")
    addition = "".join(
        "    " + line if line.strip() else line
        for line in dump([request]).splitlines(keepends=True)
    )
    block = block[:at] + addition + block[at:]
    if BEAD not in entry["beads"]:
        at = _list_end(block, "beads")
        block = block[:at] + f"    - {BEAD}\n" + block[at:]
    updated = text[:start] + block + text[end:]
    after = safe_load(updated)
    expected = {
        **entry,
        "results": [*entry["results"], request],
        "beads": [*entry["beads"], *([] if BEAD in entry["beads"] else [BEAD])],
    }
    changed = next(item for item in after["issues"] if item["number"] == ISSUE)
    others = [item for item in after["issues"] if item["number"] != ISSUE]
    if (
        changed != expected
        or others != [item for item in before["issues"] if item["number"] != ISSUE]
        or {k: v for k, v in after.items() if k != "issues"}
        != {k: v for k, v in before.items() if k != "issues"}
    ):
        raise ValueError("request edit changed more than the one result and bead")
    return updated


WATCH_NOTE = (
    "Read 2d32a6e (parent ffd900d) on 2026-10-09. Its five changed in-horizon\n"
    "      certificates at n84/86/105/175/270 are kept as derived exact facts by the\n"
    "      couzo-followup-refinements packet (T-130), whose fifteen-job native replay is\n"
    "      retained; the seven other certificates and their decimal poses are byte-identical\n"
    "      to the issue451 originals. README, decimal-pose and SVG changes are context held\n"
    "      by identity only. The n375 and n378 TXT/SVG updates are outside the 1..324\n"
    "      corpus, recorded by identity and printed side only, and stay with think-1545,\n"
    "      which also keeps the outside-corpus reader work. The eight issue451 certificates\n"
    "      and their native and custody receipts keep their own scope; their historical\n"
    "      current-house adoption and confirmation remain pending.\n"
    "      Earlier reads: complete changed-path manifests and README context for b10ad36,\n"
    "      74f7e8b and ffd900df are covered by the strict seventy-three-role custody check;\n"
    "      twenty outside-horizon reports retain derived decimal facts without a result row\n"
    "      or geometry credit, and the fourteen removed constructions remain historical\n"
    "      source roles. Raw upstream TXT/SVG/prose remain outside Git under the existing\n"
    "      retention policy; no transferred verification or all-path source retention is\n"
    "      asserted.\n"
)


def watch_text(text: str) -> str:
    """Move the franciscouzo read to the pinned commit, keeping its open owner."""
    before = safe_load(text)
    start = text.index(f"  - url: {WATCH_URL}\n")
    following = re.search(r"^\n  - url: |^  # ", text[start + 1 :], re.MULTILINE)
    end = len(text) if following is None else start + 1 + following.start()
    entry = (
        f"  - url: {WATCH_URL}\n"
        f"    read_through: {reports.REVISION}\n"
        f"    read_on: '{DAY}'\n"
        "    bead: think-1545\n"
        "    note: >-\n"
        "      " + WATCH_NOTE
    )
    updated = text[:start] + entry + text[end:]
    after = safe_load(updated)
    old = [row for row in before["repositories"] if row["url"] != WATCH_URL]
    new = [row for row in after["repositories"] if row["url"] != WATCH_URL]
    read = next(row for row in after["repositories"] if row["url"] == WATCH_URL)
    if (
        old != new
        or read["read_through"] != reports.REVISION
        or read["bead"] != "think-1545"
        or len(after["repositories"]) != len(before["repositories"])
    ):
        raise ValueError("watch edit changed more than the franciscouzo read")
    return updated


def resources_text(text: str) -> str:
    marker = "**" + reports.SOURCE_KEY + "**"
    if marker in text:
        return text
    if text.count(FOOTER) != 1:
        raise ValueError("one resources guideline footer required")
    entry = (
        "- " + marker + " — Francisco Couzo's five follow-up exact rational certificates "
        "at 84, 86, 105, 175 and 270, pinned at 2d32a6e and kept as derived exact facts "
        "with the complete pinned tree; no upstream byte is retained. [Derived packet]"
        "(web/couzo-followup-refinements-2026-10-08/README.md). T-130 remains V0/C0: all "
        "five positives and ten controls passed both maintained exact routes, while "
        "independent review, historical source-house integration and confirmation remain "
        "pending. Ryan Xu, Evan Daniel and David Ellsworth receive the source's seed and "
        "refinement credits; no optimality is asserted.\n\n"
    )
    return text.replace(FOOTER, entry + FOOTER)


def reviewed_text(text: str) -> str:
    """Move the register's review date to this registration's, never backwards."""
    match = re.search(r"^last_reviewed: '(\d{4}-\d{2}-\d{2})'$", text, re.MULTILINE)
    if match is None:
        raise ValueError("register review date missing")
    if match.group(1) >= DAY:
        return text
    return text[: match.start(1)] + DAY + text[match.end(1) :]


def plan() -> list[tuple[Path, str]]:
    """Admit complete inputs and every proposed record before the first write."""
    reports.check_certification()
    evidence, result, source, request = rows()
    items = []
    for relative, field, row, key in (
        ("packing/frontier/evidence.yaml", "evidence", evidence, "id"),
        ("packing/frontier/results.yaml", "results", result, "id"),
        ("packing/frontier/source-coverage.yaml", "sources", source, "id"),
        ("packing/resources/bibliography.yaml", "sources", bibliography_row(), "key"),
    ):
        path = REPO / relative
        reports.ensure_private(path)
        text = append(path.read_text(), field, row, key)
        if field == "results":
            text = reviewed_text(text)
        validate(path, text)
        items.append((path, text))
    path = REPO / "packing/campaign/result-requests.yaml"
    reports.ensure_private(path)
    text = request_text(path.read_text(), request)
    validate(path, text)
    items.append((path, text))
    path = REPO / "packing/campaign/intake-watch.yaml"
    reports.ensure_private(path)
    text = watch_text(path.read_text())
    validate(path, text)
    items.append((path, text))
    index = REPO / "packing/resources/README.md"
    reports.ensure_private(index)
    items.append((index, resources_text(index.read_text())))
    return items


def register() -> None:
    proposed = plan()
    for path, text in proposed:
        if path.read_text() != text:
            save(path, text)


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    register()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
