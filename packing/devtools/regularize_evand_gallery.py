"""Build the owner's review gallery for a regularization run.

`devtools.regularize_evand render` writes one comparison drawing per count and a
`summary.json`; this page puts them in front of the reviewer the regularization policy
names (`docs/project/policies/regularization-policy.md`, section 5): a summary table, then
one card per count grouped by its reported decision (section 4), each with its measures and
the three-panel drawing, then the run's measured cost. The page is static HTML and CSS with
no script, so it can be published as it is.

Review prose is not generated. An optional YAML file supplies it, keyed by count::

    title: Regularization spikes at 15 counts
    lede: One paragraph saying what was run.
    pilot: [10, 26, 70]
    decisions:
      - Do the three admitted views look right?
    effort: The full n = 1..324 pass is estimated at 5 to 7 CPU-hours.
    notes:
      26: Slides the one free square onto the grid.

Usage, from `packing/`::

    python -m devtools.regularize_evand_gallery --render RUN_DIR/render \\
        [--notes NOTES.yaml] --out gallery.html
"""

from __future__ import annotations

import argparse
import html
import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from sqpack.yamlio import load_yaml

TEMPLATE = Path(__file__).resolve().parent / "templates" / "regularize-evand-gallery.html"
POLICY = "docs/project/policies/regularization-policy.md"
DASH = "\N{EN DASH}"  # an empty cell

#: Reported decisions in the order the page shows them, with the policy's own reading.
GROUPS: tuple[tuple[str, str, str, str], ...] = (
    (
        "admitted",
        "Admitted",
        "ok",
        (
            "The view changes the drawing, passes every exact check at the witness's own "
            "side, pairs one to one with the witness and loses no contact."
        ),
    ),
    (
        "review",
        "Review",
        "hold",
        "The view passes every check the policy automates and waits for a person.",
    ),
    (
        "alternate",
        "Alternate",
        "hold",
        "An arrangement at the record's side that is not drawn as the credited packing.",
    ),
    (
        "held",
        "Held",
        "hold",
        (
            "The view changes the drawing and passes every exact check, but waits on the "
            "record: a side below the verified bound goes to the register first."
        ),
    ),
    (
        "refused",
        "Refused",
        "bad",
        "The view would change the drawing and fails an obligation.",
    ),
    (
        "no change",
        "No change",
        "flat",
        "Nothing visible would be drawn differently; the witness or the current view stands.",
    ),
    ("no view", "No view", "none", "The generator produced nothing to judge."),
)
CHIP = {report: chip for report, _, chip, _ in GROUPS}
STAGE_LABELS = (
    ("exact_solve", "Exact solve (80 digits)"),
    ("regularize", "Regularize"),
    ("import", "Import: exact routes, same-side re-solve, identity, contacts"),
)


def _number(value: float | None) -> str:
    if value is None:
        return DASH
    if value == 0:
        return "0"
    if abs(value) < 1e-3:
        return f"{value:.1e}"
    return f"{value:.2f}"


def facts(row: Mapping[str, Any], variant: str = "conservative") -> dict[str, str]:
    """The measures a card and the summary table show for one count."""
    record = row["variants"].get(variant) or {}
    policy = record.get("policy") or {}
    identity = record.get("identity") or {}
    house = (record.get("shades") or {}).get("house") or {}
    same = (record.get("same_side") or {}).get("status")
    one_to_one = identity.get("one_to_one")
    return {
        "kind": row["scalar_kind"].replace("algebraic-number-field", "number field"),
        "layer": row["project_layer"]["status"],
        "report": policy.get("report", "no view"),
        "row": str(policy.get("row", DASH)),
        "register": "yes" if policy.get("register_candidate") else "no",
        "same": {"same": "holds", "refused": "refused"}.get(same or "", DASH),
        "one_to_one": DASH if one_to_one is None else ("yes" if one_to_one else "no"),
        "move": _number(identity.get("max_move")),
        "turn": _number(identity.get("max_turn_degrees")),
        "light": (
            f"{house['light_before']} → {house['light_after']}"
            if "light_before" in house
            else DASH
        ),
    }


def _chip(report: str) -> str:
    return f'<span class="chip {CHIP.get(report, "flat")}">{html.escape(report)}</span>'


def _drawing(render: Path, n: int) -> str:
    path = render / f"n-{n:03d}-compare.svg"
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    # The drawing's fixed pixel size is dropped so it scales with its card.
    text = re.sub(r'(<svg[^>]*?) width="[\d.]+" height="[\d.]+"', r"\1", text, count=1)
    return f'<div class="plate">{text}</div>'


def _effort(rows: Sequence[Mapping[str, Any]], note: str = "") -> str:
    totals = {stage: 0.0 for stage, _ in STAGE_LABELS}
    for row in rows:
        for stage, seconds in row.get("timings", {}).items():
            if not seconds:
                continue  # a stage the count never reached
            for key in totals:
                if stage == key or stage.startswith(f"{key}_"):
                    totals[key] += float(seconds.get("wall") or 0)
    body = "".join(
        f'<tr><td>{label}</td><td class="num">{totals[stage]:.0f} s</td></tr>'
        for stage, label in STAGE_LABELS
    )
    total = sum(totals.values())
    return (
        '<section class="panel effort" id="effort"><h2>Measured cost</h2>'
        f"<p>Wall seconds over the {len(rows)} counts of this run, summed per stage.</p>"
        '<div class="scroll"><table><thead><tr><th>Stage</th><th>Wall</th></tr></thead>'
        f'<tbody>{body}<tr><td><b>Total</b></td><td class="num"><b>{total:.0f} s</b></td>'
        "</tr></tbody></table></div>"
        + (f"<p>{html.escape(note)}</p>" if note else "")
        + "</section>"
    )


def build(summary: Mapping[str, Any], render: Path, notes: Mapping[str, Any]) -> str:
    """The gallery page for one run's summary, its drawings and the reviewer's notes."""
    rows = sorted(summary["rows"], key=lambda row: row["n"])
    by_report: dict[str, list[Mapping[str, Any]]] = {}
    for row in rows:
        by_report.setdefault(facts(row)["report"], []).append(row)
    pilot = {int(n) for n in notes.get("pilot", [])}
    remarks = {int(n): str(text) for n, text in (notes.get("notes") or {}).items()}

    def tag(n: int) -> str:
        return '<span class="pilot">pilot</span>' if n in pilot else ""

    table: list[str] = []
    sections: list[str] = []
    ordered = [group for group in GROUPS if group[0] in by_report]
    ordered += [(report, report, "flat", "") for report in by_report if report not in CHIP]
    for report, title, _, blurb in ordered:
        cards: list[str] = []
        for row in by_report[report]:
            n, f = row["n"], facts(row)
            table.append(
                f'<tr><td><a href="#n{n}">{n}</a>{tag(n)}</td><td>{_chip(f["report"])}</td>'
                f'<td class="num">{f["row"]}</td><td>{f["kind"]}</td><td>{f["layer"]}</td>'
                f"<td>{f['same']}</td><td>{f['one_to_one']}</td>"
                f'<td class="num">{f["move"]}</td><td class="num">{f["turn"]}</td>'
                f'<td class="num">{f["light"]}</td><td>{f["register"]}</td></tr>'
            )
            note = f'<p class="note">{html.escape(remarks[n])}</p>' if n in remarks else ""
            measures = (
                ("witness", f["kind"]),
                ("project layer today", f["layer"]),
                ("same-side re-solve", f["same"]),
                ("one to one", f["one_to_one"]),
                ("largest move", f["move"]),
                ("largest turn (deg)", f["turn"]),
                ("light contacts", f["light"]),
                ("register candidate", f["register"]),
            )
            dl = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in measures)
            cards.append(
                f'<article class="count" id="n{n}"><header><h3>n = {n}</h3>'
                f'{_chip(f["report"])}<span class="row">policy row {f["row"]}</span>{tag(n)}'
                f'</header>{note}<dl class="facts">{dl}</dl>{_drawing(render, n)}</article>'
            )
        sections.append(
            f'<section class="group" id="{report.replace(" ", "-")}"><h2>{title} '
            f'<span class="count-n">{len(cards)}</span></h2><p class="blurb">{blurb}</p>'
            f"{''.join(cards)}</section>"
        )

    tally = "".join(
        f"<span><b>{len(by_report.get(report, []))}</b> {report}</span>"
        for report, *_ in GROUPS
        if report in by_report
    )
    decisions = notes.get("decisions") or []
    decided = (
        '<section class="panel decisions"><h2>What this run needs from you</h2><ol>'
        + "".join(f"<li>{html.escape(str(item))}</li>" for item in decisions)
        + "</ol></section>"
        if decisions
        else ""
    )
    title = str(notes.get("title") or f"Regularization review: {len(rows)} counts")
    pin = summary.get("pin") or {}
    commit = pin.get("revision") if isinstance(pin, Mapping) else pin
    meta = (
        f"Generator {html.escape(str(summary.get('tool', 'devtools.regularize_evand')))} · "
        f"upstream pin {html.escape(str(commit or 'unrecorded'))} · "
        "nothing here is committed to the record or drawn on the site."
    )
    footer = (
        f"<p>Decisions follow <code>{POLICY}</code>, section 4. Regularized views are "
        "drawings, not witnesses: they change no side, frontier value or evidence tier. "
        "Evan Daniel's method is credited as evand/square-packing (MIT).</p>"
    )
    replacements = {
        "TITLE": html.escape(title),
        "HEADING": html.escape(title),
        "LEDE": html.escape(str(notes.get("lede") or "")),
        "META": meta,
        "TALLY": tally,
        "DECISIONS": decided,
        "TABLE": "\n".join(table),
        "SECTIONS": "\n".join(sections),
        "EFFORT": _effort(rows, str(notes.get("effort") or "")),
        "FOOTER": footer,
    }
    page = TEMPLATE.read_text(encoding="utf-8")
    for key, value in replacements.items():
        page = page.replace("{{" + key + "}}", value)
    return page


def main(argv: Sequence[str] | None = None) -> int:
    command = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    command.add_argument("--render", type=Path, required=True, help="a run's render directory")
    command.add_argument("--notes", type=Path, default=None, help="reviewer notes (YAML)")
    command.add_argument("--out", type=Path, required=True, help="the HTML page to write")
    args = command.parse_args(argv)
    summary = json.loads((args.render / "summary.json").read_text(encoding="utf-8"))
    notes = load_yaml(args.notes.read_text(encoding="utf-8")) if args.notes else {}
    page = build(summary, args.render, notes or {})
    args.out.write_text(page, encoding="utf-8")
    print(f"{args.out}: {len(summary['rows'])} counts, {len(page)} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
