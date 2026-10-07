"""Acquire issue 422's pinned nine-record report through the shared strict parser.

Only derived rational facts and custody metadata are retained. This revision has its
own identity; acquisition does not decide feasibility or run either source checker.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import re
import sys
import tempfile
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml
from strif import atomic_output_file

from devtools import squish_followup_packets as followup
from devtools import squish_upper_bound_packets as original
from sqpack.yamlio import safe_load

REPO = original.REPO
PACKET = REPO / "packing/resources/web/squish-422-second-update-2026-10-07"
REVISION = "e63e4e52b1728b6671b2f263c5e02a4aa79a39d3"
NUMBERS = (88, 108, 179, 180, 199, 207, 236, 263, 302)
NEW_NUMBERS = (88, 199, 207, 236, 302)
REPLACEMENTS = (108, 179, 180, 263)
SOURCE_KEY = "[SQUISH second update 2026-10-07]"
EVIDENCE_ID = "E-squish-second-update-2026-10-07-report"
SOURCE_ID = "squish-second-update-2026-10-07"
RETRIEVED = "2026-10-07"
HEADING = "## The second SQUISH update"
REPORT_END = "<!-- END second SQUISH update -->"
SOURCE_ROOT = (
    f"https://github.com/itsnaka/squish-certs/blob/{REVISION}/squish-submission-2026-10-07b"
)
SEEDS = {
    88: "Kingbird's s(41), grafted into n88's record",
    108: "SQUISH's own s(110), two squares removed, then nearby search",
    179: "Francisco Couzo's s(180), one square removed, then nearby search",
    180: "SQUISH's own s(182), two squares removed, then nearby search",
    199: "Kingbird's s(37), grafted into n199's record",
    207: "SQUISH's own s(88), grafted into n207's record",
    236: "SQUISH's own s(88), grafted into n236's record",
    263: (
        "Francisco Couzo's s(297), carved down to n263's record, then nearby search and squeeze"
    ),
    302: "SQUISH's own s(88), grafted into n302's record",
}


def source_url(n: int) -> str:
    """Pin this revision's zero-padded certificate path."""
    if type(n) is not int or n not in NUMBERS:
        raise original.PacketError("count absent from SQUISH second update")
    return f"{SOURCE_ROOT}/n{n:03d}/n{n:03d}.cert.json"


def fact_path(n: int) -> Path:
    """Keep reported geometry separate from either earlier packet."""
    source_url(n)
    return PACKET / "facts" / f"n-{n:03d}.json.gz"


def witness_id(n: int) -> str:
    """Reserve a revision-specific identity without asserting a checked witness."""
    source_url(n)
    return f"W-squish-422-n{n:03d}"


def save(path: Path, data: bytes) -> None:
    """Publish atomically only inside this packet owner's private checkout."""
    if not path.resolve().is_relative_to(REPO.resolve()):
        raise original.PacketError("second-update output escapes the private checkout")
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_bytes(data)


def read_fact(n: int) -> dict[str, Any]:
    """Re-admit bounded normalized facts without treating them as verification."""
    path = fact_path(n)
    if path.stat().st_size > original.MAX_SOURCE_BYTES:
        raise original.PacketError("compressed second-update facts exceed byte ceiling")
    with gzip.open(path, "rb") as stream:
        data = stream.read(original.MAX_SOURCE_BYTES + 1)
    if len(data) > original.MAX_SOURCE_BYTES:
        raise original.PacketError("second-update facts exceed byte ceiling")
    fact = json.loads(data, object_pairs_hook=original.unique_json_object)
    if type(fact) is not dict or set(fact) != {"n", "side", "printed_side", "squares"}:
        raise original.PacketError("invalid second-update fact schema")
    entries = fact["squares"]
    if type(entries) is not list or any(
        type(entry) is not dict or set(entry) != {"x", "y", "t"} for entry in entries
    ):
        raise original.PacketError("invalid second-update triple roster")
    source = {
        "n": fact["n"],
        "s_exact": fact["side"],
        "s_decimal": fact["printed_side"],
        "note": "Derived geometric facts; no producer prose retained.",
        "squares": [[entry[key] for key in ("x", "y", "t")] for entry in entries],
    }
    with tempfile.TemporaryDirectory() as directory:
        temporary = Path(directory) / "source.json"
        temporary.write_bytes(followup.json_bytes(source))
        normalized, _raw = original.parse_source(temporary, n)
    if normalized != fact:
        raise original.PacketError("second-update facts are not normalized")
    return normalized


def prior_lanes() -> dict[int, dict[str, Any]]:
    """The complete earlier upper lanes, retained as semantic historical records."""
    data = original.read_json(PACKET / "acquisition/frontier-comparison.json")
    rows = data["cases"]
    if [row["n"] for row in rows] != list(NUMBERS):
        raise original.PacketError("second-update historical comparison roster mismatch")
    for row in rows:
        fact = read_fact(row["n"])
        prior = row["prior_reported"]
        verified = row["prior_verified"]
        if (
            row["new_exact_side"] != fact["side"]
            or row["new_safe_display"] != followup.display(fact["side"])
            or row["reported_seed"] != SEEDS[row["n"]]
            or not prior["source_key"]
            or not prior["found_by"]
            or not verified["evidence"]
            or original.verified_value(Fraction(verified["exact_form"]), verified["value"])
            != verified["value"]
            or Fraction(prior["value"]) <= Fraction(fact["side"])
            or Fraction(verified["value"]) <= Fraction(fact["side"])
        ):
            raise original.PacketError("second-update historical comparison mismatch")
    lower = rows[0].get("hand_authored_lower")
    fields = {"reported_lower_bound", "verified_lower_bound", "reported_status", "status"}
    if not isinstance(lower, dict) or set(lower) != fields:
        raise original.PacketError("second update needs the hand-authored n88 lower lanes")
    for field in ("reported_lower_bound", "verified_lower_bound"):
        lane = lower[field]
        if (
            not lane.get("evidence")
            or Fraction(lane["exact_form"]) != Fraction(lane["value"])
            or Fraction(lane["value"]) >= Fraction(read_fact(88)["side"])
        ):
            raise original.PacketError("second-update historical lower lane mismatch")
    return {row["n"]: row for row in rows}


def retain_prior_lanes() -> None:
    """Capture the earlier lanes once, before selecting this revision's reports."""
    path = PACKET / "acquisition/frontier-comparison.json"
    if path.exists():
        prior_lanes()
        return
    rows = []
    for n in NUMBERS:
        text = (REPO / f"packing/frontier/n-{n:03d}.md").read_text()
        case = safe_load(text.split("---\n", 2)[1])["packing"]
        if case["reported_upper_bound"]["source_key"] == SOURCE_KEY:
            raise original.PacketError("earlier lanes must be retained before adoption")
        fact = read_fact(n)
        rows.append(
            {
                "n": n,
                "prior_reported": case["reported_upper_bound"],
                "prior_verified": case["verified_upper_bound"],
                "prior_conjectured_optimum": case["conjectured_optimum"],
                "new_exact_side": fact["side"],
                "new_safe_display": followup.display(fact["side"]),
                "reported_seed": SEEDS[n],
            }
        )
        if n == 88:
            rows[-1]["hand_authored_lower"] = {
                field: copy.deepcopy(case[field])
                for field in (
                    "reported_lower_bound",
                    "verified_lower_bound",
                    "reported_status",
                    "status",
                )
            }
    save(path, followup.json_bytes({"cases": rows}))
    prior_lanes()


def report_section(n: int, fact: dict[str, Any], verified: dict[str, Any]) -> str:
    """Generate the current report and explicitly separate its older verified ceiling."""
    value = followup.display(fact["side"])
    with localcontext() as context:
        context.prec = 40
        gap = Decimal(verified["value"]) - Decimal(value)
    return (
        f"{HEADING}\n\nNate Chaoweeraprasit, using SQUISH,\n"
        "[reports a tighter bound](https://github.com/jlevy/squares/issues/422):\n"
        f"$s({n}) \\le {value}$, with exact side ${fact['side']}$.\n"
        "This second update is a reported V0/C0 claim pending complete replay and new\n"
        "scoped review. Optimality and rigidity are not established. The author reports\n"
        f"the seed as {SEEDS[n]}.\n"
        "The [revision-specific packet]"
        "(../resources/web/squish-422-second-update-2026-10-07/README.md)\n"
        f"retains the source print ${fact['printed_side']}$ separately from its safe\n"
        "upward decimal ceiling. The original and first-update certificates, finder\n"
        "credit, evidence and reviews remain historical provenance.\n\n"
        "## The verified upper bound is a ceiling\n\n"
        f"The verified ceiling is $s({n}) \\le {verified['value']}$, while the reported\n"
        f"packing has side ${value}$, smaller by ${gap}$. The `verified_upper_bound`\n"
        "certifies a ceiling, not the value of $s(n)$; `reported_upper_bound` records\n"
        "the stronger source claim, whose independent exact replay remains pending.\n\n"
        f"{REPORT_END}\n\n"
    )


def adopt_report(n: int, existing: str, generated: str | None = None) -> str:
    """Rebuild this reported lane while preserving the complete earlier verified lane."""
    from devtools import render_case_verifiers  # noqa: PLC0415
    from devtools.check_case_prose import sentence_spans  # noqa: PLC0415

    source_url(n)
    _, front, body = existing.split("---\n", 2)
    document = safe_load(front)
    case = document["packing"]
    if type(case["n"]) is not int or case["n"] != n:
        raise original.PacketError("case count differs from selected second update")
    if any(
        item.startswith("E-squish-second-update-") and item != EVIDENCE_ID
        for item in case["verified_upper_bound"]["evidence"]
    ):
        raise original.PacketError(
            "confirmed second update requires its own confirmation adapter"
        )
    fact = read_fact(n)
    prior = prior_lanes()[n]
    if any(
        evidence.startswith("E-squish-update-")
        and evidence not in prior["prior_verified"]["evidence"]
        for evidence in case["verified_upper_bound"]["evidence"]
    ):
        raise original.PacketError("unmapped confirmed SQUISH update evidence")
    report = case["reported_upper_bound"]
    report.update(
        value=followup.display(fact["side"]),
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
        source_key=SOURCE_KEY,
        source_date=RETRIEVED,
        retrieved_date=RETRIEVED,
        evidence=[EVIDENCE_ID],
    )
    case["verified_upper_bound"] = copy.deepcopy(prior["prior_verified"])
    case["rigidity"] = None
    case["source_reviewed"] = RETRIEVED
    if EVIDENCE_ID not in case["evidence"]:
        case["evidence"].append(EVIDENCE_ID)
    blocker = {
        "kind": "mathematics",
        "detail": (
            "The second SQUISH update is reported only; complete independent replay "
            "and new scoped review are pending under think-sfpz. The earlier verified "
            "bound remains the certified baseline; drawing checks do not promote "
            "this imported result."
        ),
        "evidence": [EVIDENCE_ID],
    }
    if not any(EVIDENCE_ID in row.get("evidence", []) for row in case["blockers"]):
        case["blockers"].append(blocker)
    resource = {
        "key": SOURCE_KEY,
        "role": "upper-bound-report",
        "local": PACKET.relative_to(REPO / "packing/resources").as_posix(),
        "url": SOURCE_ROOT.replace("/blob/", "/tree/"),
        "retrieved": True,
    }
    if not any(row["key"] == SOURCE_KEY for row in case["resources"]):
        case["resources"].insert(0, resource)
    history = (
        f"Prior reported s({n}) <= {prior['prior_reported']['value']} "
        f"from {prior['prior_reported']['source_key']}; its geometry, evidence and finder "
        "credit remain in the earlier packet and case history."
    )
    if not any(row["claim"] == history for row in case["priority_notes"]):
        case["priority_notes"].append(
            {
                "claim": history,
                "claimed_by": prior["prior_reported"]["found_by"],
                "published": None,
                "year": prior["prior_reported"]["found_year"],
            }
        )
    conjecture = prior["prior_conjectured_optimum"]
    if conjecture is not None:
        claim = (
            f"Earlier conjectured optimum s({n}) = {conjecture}; the smaller second-update "
            "report is pending confirmation, and no current optimum is conjectured."
        )
        if not any(row["claim"] == claim for row in case["priority_notes"]):
            case["priority_notes"].append(
                {
                    "claim": claim,
                    "claimed_by": prior["prior_reported"]["found_by"],
                    "published": None,
                    "year": prior["prior_reported"]["found_year"],
                }
            )
    case["conjectured_optimum"] = None
    if n == 88:
        # This range is hand-authored: its mixed-certificate lower intake is not
        # owned by the above-100 drafting tool. Preserve its complete prior lanes.
        for field, value in prior["hand_authored_lower"].items():
            case[field] = copy.deepcopy(value)
    if generated is not None and n != 88:
        _, draft_front, draft_body = generated.split("---\n", 2)
        draft = safe_load(draft_front)["packing"]
        for field in (
            "reported_lower_bound",
            "verified_lower_bound",
            "reported_status",
            "status",
        ):
            case[field] = draft[field]
        lower = re.search(
            r"\n## The lower bound\n.*?(?=\n<!-- BEGIN verification code)",
            draft_body,
            re.DOTALL,
        )
        if lower is None:
            raise original.PacketError("historical draft has no generated lower-bound section")
        body, count = re.subn(
            r"\n## The lower bound\n.*?(?=\n<!-- BEGIN verification code)",
            lambda _: lower.group(),
            body,
            flags=re.DOTALL,
        )
        if count != 1:
            raise original.PacketError("second update needs exactly one lower-bound section")
    if HEADING in body:
        pattern = rf"\n{HEADING}\n.*?{re.escape(REPORT_END)}\n+"
        body, count = re.subn(pattern, lambda _: "", body, flags=re.DOTALL)
        if count != 1:
            raise original.PacketError("second update needs exactly one current report section")
    else:
        body = body.replace("## The SQUISH Update", "## Earlier SQUISH update")
        body = body.replace(
            "## The verified upper bound is a ceiling", "## Earlier verified ceiling"
        )
        bound_pattern = re.compile(rf"s\({n}\)\s*\\le\s*([0-9]+\.[0-9]+)")
        for start, end in reversed(list(sentence_spans(body))):
            sentence = body[start:end]
            if (
                any(
                    Fraction(m.group(1)) > Fraction(report["value"])
                    for m in bound_pattern.finditer(sentence)
                )
                and re.search(
                    r"\b(previously|earlier|was|until|superseded)\b", sentence, re.IGNORECASE
                )
                is None
            ):
                heading = re.match(r"\s*(?:#{1,6} [^\n]*\n\s*)+", sentence)
                leading = heading.end() if heading else len(sentence) - len(sentence.lstrip())
                body = (
                    body[:start]
                    + sentence[:leading]
                    + "Previously, "
                    + sentence[leading:]
                    + body[end:]
                )
    # The superseded scientific declarations still describe their original geometry.
    # Restore them from their own immutable packet, never from the new report.
    if n in (108, 180):
        old_fact = original.read_fact(n)
        old_side = Fraction(old_fact["side"])
        old_verified = original.verified_value(old_side, old_fact["printed_side"])
        declarations = (
            (
                r"S_n = \\frac\{[0-9]+\}\{[0-9]+\}",
                f"S_n = \\frac{{{old_side.numerator}}}{{{old_side.denominator}}}",
            ),
            (
                r"The source[\u2019']s original finite decimal display is\s+\$[0-9.]+\$",
                (
                    "The source\u2019s original finite decimal display is "
                    f"${old_fact['printed_side']}$"
                ),
            ),
            (
                r"The verified display is\s+\$[0-9.]+\$",
                f"The verified display is ${old_verified}$",
            ),
        )
        for pattern, replacement in declarations:
            body, count = re.subn(pattern, lambda _, value=replacement: value, body)
            if count != 1:
                raise original.PacketError(
                    "second update needs exactly one earlier side/display declaration"
                )
    if n in (179, 263):
        old_fact = followup.read_fact(n)
        old_section = re.search(r"\n## Earlier SQUISH update\n.*?(?=\n## |\Z)", body, re.DOTALL)
        if old_section is None:
            raise original.PacketError("second update needs its earlier first-update section")
        text = old_section.group()
        for pattern, replacement in (
            (
                rf"\$s\({n}\) \\le [0-9.]+\$,\s+with exact side\s+\$[0-9]+(?:/[0-9]+)?\$",
                (
                    f"$s({n}) \\le {followup.display(old_fact['side'])}$, "
                    f"with exact side ${old_fact['side']}$"
                ),
            ),
            (r"source print\s+\$[0-9.]+\$", f"source print ${old_fact['printed_side']}$"),
        ):
            text, count = re.subn(pattern, lambda _, value=replacement: value, text)
            if count != 1:
                raise original.PacketError(
                    "second update needs exactly one earlier side/display declaration"
                )
        body = body[: old_section.start()] + text + body[old_section.end() :]
    title = re.search(r"(?m)^# [^\n]*\n", body)
    if title is None:
        raise original.PacketError("second update case has no publication title")
    first_section = title.end()
    body = (
        body[:first_section]
        + "\n"
        + report_section(n, fact, case["verified_upper_bound"])
        + body[first_section:].lstrip("\n")
    )
    return render_case_verifiers.refresh(
        "---\n"
        + yaml.safe_dump(document, sort_keys=False, allow_unicode=True, width=98)
        + "---\n"
        + body
    )


def acquire(source: Path) -> None:
    """Admit all nine sources before saving attributed derived facts and claims."""
    parsed = [
        (n, *original.parse_source(source / f"n{n:03d}/n{n:03d}.cert.json", n)) for n in NUMBERS
    ]
    cases: list[dict[str, Any]] = []
    for n, fact, raw in parsed:
        metadata = json.loads(raw, object_pairs_hook=original.unique_json_object)
        save(fact_path(n), gzip.compress(followup.json_bytes(fact), mtime=0))
        cases.append(
            {
                "n": n,
                "exact_side": fact["side"],
                "side": fact["printed_side"],
                "safe_ceiling_16": followup.display(fact["side"]),
                "source_url": source_url(n),
                "source_file": f"n{n:03d}.cert.json",
                "source_sha256": hashlib.sha256(raw).hexdigest(),
                "source_bytes": len(raw),
                "facts": fact_path(n).relative_to(REPO).as_posix(),
                "raw_asset_retained": False,
                "reported_seed": SEEDS[n],
                "reported_metadata": {
                    key: metadata[key] for key in ("phase", "squeezed") if key in metadata
                },
            }
        )
    save(
        PACKET / "acquisition/sources.json",
        followup.json_bytes(
            {
                "format": "external-source-acquisition-v1",
                "retrieved": "2026-10-07",
                "source_commit": REVISION,
                "source_key": SOURCE_KEY,
                "source_issue": "https://github.com/jlevy/squares/issues/422",
                "raw_asset_retained": False,
                "producer_checker_replayed": False,
                "feasibility_checked": False,
                "sources": [
                    {
                        "source_url": "https://github.com/itsnaka/squish-certs",
                        "source_commit": REVISION,
                        "subtree_scope": [
                            f"squish-submission-2026-10-07b/n{n:03d}/n{n:03d}.cert.json"
                            for n in NUMBERS
                        ],
                    }
                ],
                "cases": cases,
            }
        ),
    )
    save(
        PACKET / "acquisition/update-claims.json",
        followup.json_bytes(
            {
                "results": [
                    {"n": row["n"], "offered_side": row["safe_ceiling_16"]} for row in cases
                ]
            }
        ),
    )


def check(source: Path | None = None) -> None:
    """Bind all nine derived facts and acquisition declarations to their selected source."""
    data = original.read_json(PACKET / "acquisition/sources.json")
    if (
        data["format"] != "external-source-acquisition-v1"
        or data["source_commit"] != REVISION
        or data["source_key"] != SOURCE_KEY
        or data["source_issue"] != "https://github.com/jlevy/squares/issues/422"
        or data["retrieved"] != RETRIEVED
        or data["raw_asset_retained"] is not False
        or data["producer_checker_replayed"] is not False
        or data["feasibility_checked"] is not False
        or [row["n"] for row in data["cases"]] != list(NUMBERS)
    ):
        raise original.PacketError("second-update acquisition identity mismatch")
    for row in data["cases"]:
        n = row["n"]
        fact = read_fact(n)
        if (
            row["facts"] != fact_path(n).relative_to(REPO).as_posix()
            or row["exact_side"] != fact["side"]
            or row["side"] != fact["printed_side"]
            or row["safe_ceiling_16"] != followup.display(fact["side"])
            or row["source_url"] != source_url(n)
            or row["source_file"] != f"n{n:03d}.cert.json"
            or row["reported_seed"] != SEEDS[n]
            or row["raw_asset_retained"] is not False
            or type(row["source_bytes"]) is not int
            or not 1 <= row["source_bytes"] <= original.MAX_SOURCE_BYTES
            or re.fullmatch(r"[0-9a-f]{64}", row["source_sha256"]) is None
            or type(row["reported_metadata"]) is not dict
            or not set(row["reported_metadata"]) <= {"phase", "squeezed"}
        ):
            raise original.PacketError(f"n={n} second-update provenance/facts mismatch")
        metadata = row["reported_metadata"]
        if "phase" in metadata and (
            type(metadata["phase"]) is not int or not 1 <= metadata["phase"] <= 100
        ):
            raise original.PacketError("unsupported retained phase metadata")
        if "squeezed" in metadata and type(metadata["squeezed"]) is not bool:
            raise original.PacketError("unsupported retained squeezed metadata")
        if source is not None:
            parsed, raw = original.parse_source(source / f"n{n:03d}/n{n:03d}.cert.json", n)
            source_metadata = json.loads(raw, object_pairs_hook=original.unique_json_object)
            if (
                parsed != fact
                or len(raw) != row["source_bytes"]
                or hashlib.sha256(raw).hexdigest() != row["source_sha256"]
                or metadata
                != {
                    key: source_metadata[key]
                    for key in ("phase", "squeezed")
                    if key in source_metadata
                }
            ):
                raise original.PacketError(f"n={n} source bytes differ from pinned acquisition")
    claims = {
        "results": [
            {"n": row["n"], "offered_side": row["safe_ceiling_16"]} for row in data["cases"]
        ]
    }
    if original.read_json(PACKET / "acquisition/update-claims.json") != claims:
        raise original.PacketError("second-update claims mismatch")


def refresh_atlas(workers: int) -> None:
    """Rebuild these nine geometries while holding every other retained case unchanged."""
    from devtools import build_known_best_atlas as atlas  # noqa: PLC0415

    check()
    atlas.update_selected(NUMBERS, workers)


def main() -> int:
    """Acquire and check facts, or adopt reports without a feasibility promotion."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command", choices=("acquire", "check", "retain-prior", "record", "atlas")
    )
    parser.add_argument("--source", type=Path)
    parser.add_argument("--jobs", type=int, default=1)
    args = parser.parse_args()
    try:
        if args.command == "acquire":
            if args.source is None:
                parser.error("acquire requires --source")
            acquire(args.source)
        elif args.command == "check":
            check(args.source)
        elif args.command == "retain-prior":
            retain_prior_lanes()
        elif args.command == "atlas":
            if args.jobs < 1:
                parser.error("--jobs must be positive")
            refresh_atlas(args.jobs)
        else:
            check()
            prior_lanes()
            for n in NUMBERS:
                path = REPO / f"packing/frontier/n-{n:03d}.md"
                save(path, adopt_report(n, path.read_text()).encode())
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"SQUISH second update: {error}", file=sys.stderr)
        return 1
    print("SQUISH second update: reported facts checked; feasibility not decided")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
