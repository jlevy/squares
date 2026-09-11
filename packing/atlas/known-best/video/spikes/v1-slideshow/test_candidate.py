#!/usr/bin/env python3
"""Smoke test for the v1 slideshow candidate (revision 4).

Runs as a script (`python3 test_candidate.py`) or under pytest. It regenerates
index.html into two temporary directories and checks:

  1. the two runs are byte-identical (determinism);
  2. the page carries all 324 slides, each with n polygons and a facts template;
  3. no `http://` or `https://` occurs anywhere except the per-slide source-URL
     facts inside the embedded JSON record;
  4. the page performs no network fetch by construction (no `fetch(`, no
     external `src=`/`href=` beyond the in-document `#surd` and `#badge-*`
     references, a CSP that names no host);
  5. every slide carries one badge per entry in the poster's record (the star
     from `lower.first_proved_here`, then `badges[]`) with its short label and
     nothing else, an open group with its rows derived from the same record, both
     notes on their own line directly under the value they annotate (the degree
     note under the side value when there is no exact form, the empty exact slot
     after it), the `n =` line above the numeral, and a source-URL line closing
     the record block; no polynomial row;
  6. the type: the embedded faces are exactly the five in `FACES` (PT Serif at 400
     only, no 700), no stage rule asks for a bold face, and the numeral is PT Serif
     at weight 400; scarlet `#a3123f` is written once, on the star row, and the star
     is drawn in currentColor; every stage font-size is an absolute px value of at
     least 28 from a scale of at most four sizes whose largest is at most 4.5 x the
     smallest;
  7. the progress bar is in the stage markup and the default timing is 1.5 + 0.5;
  8. the embedded script parses and, in the stub-DOM harness, the timeline API
     behaves: the bar's width is monotone in time, the panel cuts at the fade
     midpoint, the base layer is visible at every seek (needs `node`, skipped
     otherwise);
  9. with Playwright importable, the headless survey of every n passes: the panel
     ends above the footer and the progress bar, inside the stage, no value line
     reaches its note, the browser's computed sizes obey the scale, no serif element
     resolves to a weight other than 400, the degree note sits directly under the
     value it annotates, and the lower-bound line is at the same y for every n.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import build_candidate  # noqa: E402

FIRST, LAST = build_candidate.FIRST_N, build_candidate.LAST_N

# The faces the page embeds, (family, style, weight) in @font-face order. PT Serif
# is embedded at 400 only: nothing on the stage is set bold in the serif, so the
# two 700 faces (78 KB as base64) are not carried.
FACES = (
    ("PT Serif", "normal", "400"),
    ("PT Serif", "italic", "400"),
    ("Source Sans 3 Variable", "normal", "200 900"),
    ("Source Sans 3 Variable", "italic", "200 900"),
    ("Atlas Symbols", "normal", "400"),
)


def _build_twice() -> tuple[bytes, bytes]:
    with tempfile.TemporaryDirectory() as tmp_a, tempfile.TemporaryDirectory() as tmp_b:
        build_candidate.build(build_candidate.DEFAULT_REPO, Path(tmp_a), 2, "svg")
        build_candidate.build(build_candidate.DEFAULT_REPO, Path(tmp_b), 2, "svg")
        a = (Path(tmp_a) / "index.html").read_bytes()
        b = (Path(tmp_b) / "index.html").read_bytes()
    return a, b


def _extract_json(page: str) -> dict:
    match = re.search(r'<script id="atlas-data" type="application/json">(.*?)</script>', page, re.DOTALL)
    assert match, "embedded record missing"
    return json.loads(match.group(1).replace("<\\/", "</"))


def _walk(node, path=()):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from _walk(value, path + (key,))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _walk(value, path + (index,))
    else:
        yield path, node


def _expected_badges(entry: dict) -> list[tuple[str, str]]:
    """(symbol id, label) per row, the star first."""
    rows = []
    if entry["lower"]["first_proved_here"]:
        rows.append((build_candidate.STAR_ID, build_candidate.STAR_LABEL))
    for badge in entry["badges"]:
        key = (badge["glyph"], badge["style"])
        rows.append((build_candidate.BADGE_IDS[key], build_candidate.BADGE_LABELS[key]))
    return rows


def _expected_open(entry: dict) -> list[str]:
    items = []
    if entry["optimality"]["status"] == "open":
        items.append(build_candidate.OPEN_LABELS[0])
    if entry["exactness"]["state"] not in ("closed-form", "minimal-polynomial"):
        items.append(build_candidate.OPEN_LABELS[1])
    if entry["rigidity"]["state"] == "not-established":
        items.append(build_candidate.OPEN_LABELS[2])
    return items


def _no_exact_form(entry: dict) -> bool:
    """True when the panel prints no exact line: no form, or a bare integer (which
    would duplicate the side line)."""
    form = entry["exactness"]["exact_form"]
    return form is None or build_candidate.parse_exact_form(form)[0] == "int"


def _stage_css(page: str) -> str:
    style = re.search(r"<style>\n(.*?)</style>", page, re.DOTALL).group(1)
    style = re.sub(r"@font-face \{[^}]*\}", "", style)
    return re.sub(r"/\*.*?\*/", "", style, flags=re.DOTALL)


def test_candidate() -> None:
    a, b = _build_twice()

    # 1. determinism, and the shipped file beside this test is that same build
    assert a == b, "two builds differ"
    shipped = HERE / "index.html"
    if shipped.exists():
        assert shipped.read_bytes() == a, "shipped index.html is stale: rerun build_candidate.py"

    page = a.decode("utf-8")

    # 2. all slides present
    data = _extract_json(page)
    slides = data["slides"]
    assert len(slides) == LAST - FIRST + 1 == 324
    for offset, slide in enumerate(slides):
        n = FIRST + offset
        assert slide["n"] == n
        assert len(slide["p"].split(";")) == n, f"n={n}: polygon count"
        assert len(slide["f"]) == n, f"n={n}: fill count"
        for polygon in slide["p"].split(";"):
            assert len(polygon.split(" ")) == 4, f"n={n}: corner count"
        assert slide["a"].startswith(f"n = {n}."), f"n={n}: aria text"
    templates = dict(re.findall(r'<template id="facts-(\d+)">(.*?)</template>', page, re.DOTALL))
    assert len(templates) == 324
    for n in range(FIRST, LAST + 1):
        assert str(n) in templates, f"n={n}: facts template"
        assert f'<span class="arg">({n})</span>' in templates[str(n)], f"n={n}: s(n) line"
    assert all(len(fill) == 7 and fill.startswith("#") for fill in data["palette"])

    # 3. the only http(s) strings are the source-URL facts in the record
    match = re.search(r'<script id="atlas-data" type="application/json">(.*?)</script>', page, re.DOTALL)
    outside = page[: match.start()] + page[match.end() :]
    assert "http://" not in outside and "https://" not in outside, "URL outside the record"
    url_paths = []
    for path, value in _walk(data):
        if isinstance(value, str) and ("http://" in value or "https://" in value):
            url_paths.append(path)
            assert path[0] == "slides" and path[2] == "src", f"URL at {path}"
    # Every case has one: 147 from the manifest (kingbird / unitsquare renderings),
    # 177 exact grids from the frontier's record-catalogue resource.
    assert len(url_paths) == 324, f"{len(url_paths)} source URLs"

    # 4. nothing that could reach the network
    assert "fetch(" not in page and "XMLHttpRequest" not in page and "import(" not in page
    assert "innerHTML" not in page and "eval(" not in page
    local_refs = {"#surd", f"#{build_candidate.STAR_ID}", f"#{build_candidate.OPEN_ID}"}
    local_refs.update(f"#{ident}" for ident in build_candidate.BADGE_IDS.values())
    for attr in re.findall(r'\b(?:src|href)="([^"]*)"', page):
        assert attr.startswith("data:") or attr in local_refs, f"external reference {attr[:60]!r}"
    csp = re.search(r'Content-Security-Policy" content="([^"]+)"', page).group(1)
    assert "default-src 'none'" in csp and "connect-src 'none'" in csp
    assert "Date.now" not in page and "Math.random" not in page and "setInterval" not in page

    # 5. badges and the open group come from the record, one row each, nothing invented
    for ident in list(build_candidate.BADGE_IDS.values()) + [build_candidate.STAR_ID, build_candidate.OPEN_ID]:
        assert page.count(f'<symbol id="{ident}">') == 1, f"symbol {ident}"
    composite = build_candidate.read_composite(build_candidate.DEFAULT_REPO)
    badge_tally = 0
    degree_under_side = 0
    for n in range(FIRST, LAST + 1):
        body = templates[str(n)]
        status = re.search(r'<ul class="status">(.*?)</ul>', body, re.DOTALL).group(1)
        rows = re.findall(r"<li[^>]*>(.*?)</li>", status, re.DOTALL)
        expected = _expected_badges(composite[n])
        assert len(rows) == len(expected), f"n={n}: badge rows {rows}"
        for row, (ident, label) in zip(rows, expected):
            assert f'<use href="#{ident}"' in row and row.endswith(label), f"n={n}: {row!r} vs {label!r}"
        badge_tally += len(rows)
        open_block = re.search(r'<div class="open"><p class="open-head">Open</p><ul>(.*?)</ul></div>', body, re.DOTALL)
        assert open_block, f"n={n}: open group missing"
        expected_open = _expected_open(composite[n])
        rows = re.findall(r"<li[^>]*>(.*?)</li>", open_block.group(1), re.DOTALL)
        if expected_open:
            assert len(rows) == len(expected_open), f"n={n}: open rows"
            for row, text in zip(rows, expected_open):
                assert f'<use href="#{build_candidate.OPEN_ID}"' in row and row.endswith(text), f"n={n}: {row!r}"
        else:
            assert rows == ["nothing open"], f"n={n}: empty open group {rows}"
        # Notes on their own line under the value: never inside a `.line`.
        for note in ("class=\"degree\"", "class=\"note\""):
            for line in re.findall(r'<p class="line[^"]*">(.*?)</p>', body, re.DOTALL):
                assert note not in line, f"n={n}: {note} inside a value line"
        # The five slots, in order. With an exact form: side, exact, degree note,
        # lower, the lower's note. Without one the degree note follows the side value
        # it annotates and the empty exact slot comes after it, so the note cannot
        # read as the lower bound's label; the slots are the same heights either way.
        lines = re.findall(r'<p class="(line[^"]*|sub[^"]*)">', body)
        kinds = [(c.split()[0],) if c.startswith("sub") else tuple(c.split()[:2]) for c in lines]
        exact_empty = '<p class="line exact empty"></p>' in body
        assert exact_empty == _no_exact_form(composite[n]), f"n={n}: exact slot"
        degree = composite[n]["exactness"]["degree"]
        degree_here = degree is not None and degree >= 2
        assert (f"algebraic degree {degree}" in body) == degree_here, f"n={n}: degree note"
        if exact_empty:
            expected_slots = [("line", "side"), ("sub",), ("line", "exact"), ("line", "lower"), ("sub",)]
            degree_slot = 1
        else:
            expected_slots = [("line", "side"), ("line", "exact"), ("sub",), ("line", "lower"), ("sub",)]
            degree_slot = 2
        assert kinds == expected_slots, f"n={n}: slots {lines}"
        assert (lines[degree_slot] == "sub") == degree_here, f"n={n}: degree slot {lines[degree_slot]!r}"
        if exact_empty and degree_here:
            degree_under_side += 1
        # The `n =` line is its own block directly above the numeral's.
        assert (
            '<p class="lead"><span class="var">n</span><span class="eq">=</span></p>'
            f'<p class="headline"><span class="nval">{n}</span></p>'
        ) in body, f"n={n}: headline"
        assert body.count('<div class="urlrow"><dd class="url">') == 1, f"n={n}: source URL line"
        assert body.endswith("</dl></div>"), f"n={n}: the URL line is not the last thing in the panel"
    assert badge_tally == sum(len(_expected_badges(entry)) for entry in composite.values())
    assert degree_under_side == sum(
        1
        for entry in composite.values()
        if _no_exact_form(entry) and (entry["exactness"]["degree"] or 0) >= 2
    )
    assert "Minimal polynomial" not in page and "<sup>" not in page

    # 6. the type: weight, the one scarlet, and the scale
    css = _stage_css(page)
    headline_rule = re.search(r"\n\.headline \{([^}]*)\}", css).group(1)
    assert "font-weight: 400" in headline_rule and f"font-size: {build_candidate.NUMERAL_SIZE}px" in headline_rule
    faces = re.findall(
        r'@font-face \{\n  font-family: "([^"]+)";\n  font-style: (\w+);\n  font-weight: ([^;]+);', page
    )
    assert tuple(faces) == FACES, f"embedded faces {faces}"
    assert not any(weight == "700" for _, _, weight in faces)
    assert "font-weight: 700" not in css and "bold" not in css, "a stage rule asks for a bold face"
    plain = re.sub(r"data:font/woff2;base64,[A-Za-z0-9+/=]+", "", outside)
    assert plain.lower().count("a3123f") == 1, f"scarlet written {plain.lower().count('a3123f')} times"
    star_rule = re.search(r"\.status li\.star \{([^}]*)\}", css).group(1)
    assert build_candidate.NEW_COLOR in star_rule, "scarlet is not on the star row"
    assert re.search(rf'<symbol id="{build_candidate.STAR_ID}"><polygon points="[^"]+" fill="currentColor"/>', page)
    assert "accent" not in css and "accent" not in "".join(templates.values())
    sizes: set[int] = set()
    for selectors, declarations in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        selector_list = [s.strip() for s in selectors.strip().split(",")]
        chrome = all(any(s.startswith(p) for p in build_candidate.CHROME_SELECTORS) for s in selector_list)
        for value in re.findall(r"font-size:\s*([^;]+);", declarations):
            if chrome:
                continue
            assert re.fullmatch(r"\d+px", value.strip()), f"stage font-size {value!r} in {selectors.strip()!r}"
            px = int(value.strip()[:-2])
            assert px >= 28, f"{px}px in {selectors.strip()!r}"
            sizes.add(px)
    assert sizes == set(build_candidate.TYPE_SCALE) and len(sizes) <= 4, sizes
    assert max(sizes) <= 4.5 * min(sizes)
    assert "font-size" not in build_candidate.JS
    assert not re.search(r'style="[^"]*font-size', page), "inline font-size in the markup"

    # 7. the progress bar and the timing
    assert page.count('<div id="progress" aria-hidden="true">') == 1
    assert '<span class="end lo">1</span>' in page and '<span class="end hi">324</span>' in page
    assert 'id="progress-fill"' in page and 'id="progress-cursor"' in page
    assert data["timing"] == {"dwell": 1.5, "fade": 0.5}
    assert page.count('<div id="facts" class="facts-host"></div>') == 1

    # 8. the script parses and its timeline API behaves (optional, needs node)
    node = shutil.which("node")
    scripts = re.findall(r"<script>(.*?)</script>", page, re.DOTALL)
    assert len(scripts) == 1
    if node:
        with tempfile.TemporaryDirectory() as tmp:
            script_path = Path(tmp) / "candidate.js"
            script_path.write_text(scripts[0])
            subprocess.run([node, "--check", str(script_path)], check=True)
            page_path = Path(tmp) / "index.html"
            page_path.write_bytes(a)
            subprocess.run(
                [node, str(HERE / "timeline_harness.js"), str(page_path)],
                check=True,
                stdout=subprocess.DEVNULL,
            )

    # 9. the headless survey of every n (optional, needs Playwright and its browser)
    survey_note = "skipped"
    try:
        import playwright.sync_api  # noqa: F401
        import render_review
    except ImportError:
        render_review = None
    if render_review is not None:
        with tempfile.TemporaryDirectory() as tmp:
            page_path = Path(tmp) / "index.html"
            page_path.write_bytes(a)
            result = render_review.survey(page_path.as_uri() + "?capture=1", [], 1, None, "")
        failures = render_review.check(result, verbose=False)
        assert not failures, failures
        bottom = max(m["bottom"] for m in result["measures"].values())
        footer = min(m["footerTop"] for m in result["measures"].values())
        bar = min(m["barTop"] for m in result["measures"].values())
        lower_tops = sorted({round(m["lowerTop"], 1) for m in result["measures"].values()})
        serif_weights = sorted({w for m in result["measures"].values() for w in m["serifWeights"]})
        assert len(lower_tops) == 1, f"the lower-bound line moves between n: {lower_tops}"
        assert serif_weights == ["400"], f"PT Serif elements resolve to weights {serif_weights}"
        survey_note = (
            f"panel bottom {bottom:.0f} < footer {footer:.0f} < bar {bar:.0f}, "
            f"lower line top {lower_tops[0]}, serif weights {serif_weights}"
        )

    duration = LAST * (data["timing"]["dwell"] + data["timing"]["fade"])
    print(
        f"ok: {len(a)} bytes, 324 slides, {len(url_paths)} source URLs, {badge_tally} badges, "
        f"{degree_under_side} degree notes under a side value, {len(faces)} faces, "
        f"{duration:.1f} s, sizes {sorted(sizes)}, node={'yes' if node else 'skipped'}, survey={survey_note}"
    )


if __name__ == "__main__":
    test_candidate()
