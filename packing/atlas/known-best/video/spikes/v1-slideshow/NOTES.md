# Slideshow candidate v1 — notes

Review candidate for the known-best atlas video, n = 1..324. Everything here is in this
directory; nothing under the repository worktree was touched.

## Revision 4

Two small changes after the revision 3 stills.
Regenerated `index.html` is **3,521,392 bytes** (78,178 fewer than revision 3, all of it
the two dropped faces); the timing is unchanged, 648 s. `test_candidate.py` passes in
about 38 s
(`ok: 3521392 bytes, 324 slides, 324 source URLs, 412 badges, 36 degree notes under a
side value, 5 faces, 648.0 s, sizes [28, 34, 44, 96], node=yes, survey=panel bottom 959
< footer 972 < bar 1008, lower line top 376, serif weights ['400']`), the harness’s 31
checks pass, and `render_review.py` over all 324 n reports `review: ok`. The revision 3
generator, test, review tool and notes are kept as `review/*.v3.*.bak`; the patch that
made revision 4 is `review/patch_r4.py`; the stills are `review/r4-n011.png`,
`r4-n028.png`, `r4-n147.png` (and `r4-fade-147-148.png`, which the review tool always
writes). The record’s contract string is `v1-candidate-r4`.

1. **The degree note sits under the value it annotates.** In revision 3 the five value
   slots were always side, exact, degree note, lower, lower’s note, so on the 36 n that
   have a degree but no printed exact form (n = 11 and 28 among them) `ALGEBRAIC DEGREE
   d` sat under an empty slot, directly above `s(n) ≥ …`, and read as that line’s label.
   Now, when there is no exact form, the note goes on the line directly under the side
   value and the empty exact slot follows it; with an exact form the order is as before.
   The slots keep their heights (50 + 58 + 30 px above the lower line in either order),
   so the lower line and everything below it do not move: the survey now records the
   `.line.lower` top for every n and finds the one value, 376, over all 324 (the test
   asserts it), and on the stills the lower line’s ink is rows 383–425 and its note
   432–450 at n = 11, 28 and 147 alike.
   The degree note’s ink is rows 294–312, directly under the side line’s 245–287, at n =
   11 and 28; at n = 147 the exact line (294–341) keeps its place and the note follows
   it (352–370). The survey also records which value line the note sits under and its
   distance from it (0, or the 5 px a nested radical’s line is lifted by) and checks
   both for every n: 68 notes under an exact form, 36 under the side value, the count
   the test derives from the record (degree ≥ 2 and no printed form).
   The intrusion check now covers every value line with a note beneath it, since the
   side line can have one; the worst is −2 px, clear.

2. **The PT Serif 700 faces are gone.** `FONT_FACES` lists five faces; the test pins
   them in its own list, `FACES` (no earlier revision of the test had one), and asserts
   no embedded face is weight 700 and no stage rule asks for a bold.
   The survey collects the computed family and weight of every text-bearing element on
   the stage over all n: `PT Serif 400` is the only serif pair (the sans resolves at
   400, 450 and 550), and `document.fonts` declares exactly the five faces, none at 700.
   The saving is 58,104 bytes raw, 77,472 as base64, plus the two `@font-face` wrappers.

## Revision 3

Applied after the owner’s second set of notes on the revision 1 stills.
Regenerated `index.html` is **3,599,570 bytes** (25,185 fewer than revision 2: shorter
labels, no polynomial rows); the timing is unchanged, 648 s. `test_candidate.py` passes
in about 43 s
(`ok: 3599570 bytes, 324 slides, 324 source URLs, 412 badges, 648.0 s, sizes [28, 34,
44, 96], node=yes, survey=panel bottom 959 < footer 972 < bar 1008`), the harness’s 31
checks pass, and `render_review.py` over all 324 n reports `review: ok`. The revision 2
generator, test and review tool are kept as `review/*.v2.*.bak`; the revision 2 stills
(`review/n*.png`, `fade-147-148.png`, `zoom-badges-and-bar.png`) are left for
comparison; the revision 3 stills are `review/r3-*.png` (n = 5, 11, 28, 54, 147, 268,
307, 323, 324, the 147 → 148 fade midpoint, and `r3-zoom-details.png`, a 2× crop of the
small things).

What changed, per note:

1. **`n =` on its own line above the numeral.** A `<p class="lead">` at 34 px — italic
   PT Serif `n`, upright `=` 0.24 em after it, in the notes’ grey `#47525f` — in a 36 px
   slot directly above the numeral’s slot, both flush left at x = 1080. The revision 2
   centring (the metric lifts) is gone.
   Measured on the stills: the `n =` ink ends at y = 139, the numeral’s ink begins at
   151–155 (a 12–16 px gap with nothing inked between, checked in the numeral’s
   columns), and the two blocks’ left edges coincide; the ink of the `n` and of the
   first digit differ by the digits’ own side bearings (3–9 px, the `1` widest).

2. **A lighter numeral.** PT Serif Regular (400) at 96 px, letter-spacing 0, in an 84 px
   slot: the lining digits’ ink is 67–73 px tall (the `5` overshoots), so the slot holds
   it, and it is the same slot for every n.

3. **Scarlet means new.** `#a3123f` is written once, in
   `.status li.star { color: #a3123f }`. The star polygon is `fill="currentColor"` and
   takes the row’s colour, as the poster draws its star in the same accent, so the star
   and its label are one colour and the literal is still one.
   The `--accent` variable, `.val.accent` and the `accent=` argument are gone: the lower
   bound’s digits are ink on every n, and `PROVED LOWER BOUND` is the notes’ grey small
   caps. The test counts `a3123f` in the page with the font data and the record excluded:
   exactly one.

4. **Short labels.** `O optimal`, `= exact`, `≈ numerical`, `R rigid`, muted `R rigid
   (catalogue)`, `★ new lower bound` (scarlet, weight 550 like the other rows).
   The open group’s rows are the short forms, `optimality`, `exact value`, `rigidity`,
   chosen because they parallel the one-word badge labels and read as a list under
   `OPEN`; the heading stays.
   The record’s `meaning` strings (“proved optimal”, “lower bound first proved here”)
   remain in the spoken `aria-live` mirror, which was not asked to change.

5. **Type scale 28 / 34 / 44 / 96.**
   - 28: the kicker, the degree and lower-bound notes, `OPEN`, the record block (labels
     and values), the source-URL line, the footer, the progress bar’s three numbers
     (these were 17–22).
   - 34: the `n =` line, the badge rows, the open rows (were 24).
   - 44: the side, exact and lower lines (were 56 / 42).
   - 96: the numeral (was 132).

   The numeral is 3.43 × the smallest.
   A stacked fraction’s digits are 28 px (they were 0.62 em, 26 px at 42, and would have
   been 21 at 34), inside the 44 px exact line; `#stage { font-size: 28px }` is the
   floor for anything unstyled.
   The scale is enforced twice: statically in the test (every stage rule’s `font-size`
   is an absolute px value from the scale; the review chrome’s rules are excluded by
   selector, `CHROME_SELECTORS`) and by computed style in the survey (every text-bearing
   element under `#stage`, over all 324 n, is one of {28, 34, 44, 96}). The small-caps
   notes keep their tracking (0.06 em; the kicker 0.14, `OPEN` and the record labels
   0.08).

   Leading, tightened to fit: kicker 30, lead 36, numeral 84, side 50, exact 58 (a 50 px
   strut), degree and note 30, lower 50, badge and open rows on a 36 px pitch, `OPEN`
   30, record 32. The panel’s deepest point is y = 959 (n = 132, 156, 182, 210, 241,
   273, 307: six record rows, one of which wraps) against the footer at 972 and the bar
   at 1008; the survey asserts both for every n and the test runs it.

   **What the record block dropped:** the minimal-polynomial row, for the 7 n where it
   printed in revision 2 — 11, 28, 39, 70, 153, 268, 302. (The revision 2 notes said 15;
   the shipped page printed 7, the count of polynomials at most 96 characters once
   normalised.) At 28 px the shortest of them (n = 302, 38 characters) takes two lines
   and the label `MINIMAL POLYNOMIAL` alone is 309 px, which would widen the label
   column on every n; the degree note under the exact line carries the degree.

   Also changed so the block fits: the source URL is its own line across both columns,
   last in the block (the longest, `…/squares_in_squares.html`, is 664 px, wider than
   the 514 px value column and narrower than the panel); Nagamochi’s bound is labelled
   `general bound` rather than `Nagamochi’s general bound` (289 of the 324 rows are his;
   “Hiroshi Nagamochi, 2005 (general bound)” is 485 px and fits the column, the old
   spelling was 643 and wrapped every one); and the footer’s right sentence lost the
   word “shade” (“darker, more full-side contacts”) so both sentences fit one line at 28
   px with a 95 px gap between them (the originals were 1,722 px in 1,740). Two rows
   still wrap, to two lines each: n = 11’s lower bound (“repository exact H-041
   certificate, 2026 (unavoidable points)”) and n = 307’s Found (three names).

   Progress bar: numbers at 28 px, the riding n on a line at y = 1008–1038, the track at
   1040, `1` and `324` centred on the track 18 px outside its ends.
   The riding n is now held inside the track at the ends (`render()` clamps its centre
   to [w/2, W − w/2]) so it never runs into the end labels — centred on the fill’s edge,
   the `324` had overlapped the `324` beside it; the tightest gap is now 18 px, at n = 1
   and 324. In the stub harness, which has no layout, the clamp falls back to the
   percentage.

Also fixed on the way: the exact line sat at three heights across n (288 / 289.3 /
289.9). With a 44 px line-height, the drawn radical’s inline-block (its padding-top) and
the stacked fraction each grew the line box above the baseline by 1.3–1.9 px and the
flex row’s baseline alignment dropped the `=` with them.
The line now has a 50 px strut, tall enough that neither box rises above it, so the
baseline is the strut’s for every form; the nested radical still rises 5 px above and is
lifted by 5 (it was 8 at 42 px).
Measured over all n, the equals sign’s top is 287.9–288.0, and the survey fails on a
spread over 1 px.

`render_review.py` is now importable (`survey`, `check`, `check_headline`), takes
`--prefix`, and also measures the computed font sizes, the footer’s overflow and the gap
between its sentences, the exact line’s baseline, the riding n’s distance from the end
labels, and the record block’s height and row count; the headline check looks for each
mark’s ink in its block’s rows, not its span’s box (a span’s box is the font’s content
area, and the 96 px numeral’s reaches up into the `n =` line).
`test_candidate.py` runs the survey whenever Playwright imports.

Left as is, and worth a decision: the two PT Serif 700 faces are still embedded (58 KB
raw, 78 KB as base64) though nothing uses them now that the numeral is Regular; the
brief listed the fonts as unchanged, so they stay, and dropping them is a one-line
saving.

## Revision 2

Applied after the owner’s browser review.
Regenerated `index.html` is 3,624,755 bytes; the default timing is now 1.5 s dwell + 0.5
s fade, so the whole run is 324 × 2.0 s = **648 s = 10 min 48.0 s** (19,440 frames at 30
fps). `test_candidate.py` passes
(`ok: 3624755 bytes, 324 slides, 324 source URLs, 412 badges, 648.0 s, node=yes`), and
the new `render_review.py` measured every n headless and wrote the screenshots in
`review/`. The v1 generator, harness and test are kept as `review/*.v1.*.bak`, and
`review/before-147*.png` are v1 captures for comparison.

What changed, per request:

1. **`n =` centred on the numeral.** The italic `n` and the `=` are lifted (by
   `position: relative`, so the numeral’s baseline and line box do not move) until each
   mark’s own ink centre sits on the digits’ cap centre.
   The lifts are computed from the embedded PT Serif faces’ ink metrics (digits 0..712,
   italic n −6..512, equals 237..450 font units) and emitted into the CSS;
   `render_review.py` checks the pixels: the `n` and the `=` centre at y = 169.0, the
   numeral at 170.0.
2. **Notes always below.** `ALGEBRAIC DEGREE d` and `PROVED LOWER BOUND` each have their
   own 24 px line directly under the value line they annotate, flush left with it, on
   every n; the slot is present (empty) when there is nothing to say.
   The skeleton is the same five lines for all 324: side, exact, exact-note, lower,
   lower-note. One consequence to be aware of: the 36 minimal-polynomial cases have a
   degree but no closed form, so their degree note sits under an empty exact line (n =
   11, 28). Moving it up under the side value for those n would vary the layout again,
   which is what was asked against.
3. **The poster’s badges.** Each status row now carries the poster’s badge as inline
   SVG: the 19-unit rounded box (`rx` 4.5, stroke 1.2, glyph at 15 units), scaled as a
   whole to 27 px; solid = `#5c6673` with a white glyph, muted = outlined; the star is
   `SUMMARY_STAR_POINTS` at the poster’s `0.92` span.
   Glyphs are paths, not text: `O`, `=`, `R`, `?` are extracted at build time from the
   embedded Source Sans 3 Variable instanced at weight 650 (the poster’s `font-weight`),
   and `≈` from KaTeX_Main, which the latin subsets lack, drawn at 13 units with a
   26-unit stroke so its regular-weight wave matches the 650 equals.
   The badge set is exactly `_case_badges`: the star from `lower.first_proved_here`,
   then `badges[].glyph/style` in record order, and the builder refuses any (glyph,
   style) pair it does not know.
   412 badges over the 324 cases.
4. **Open group.** Headed `OPEN` (rather than Unknown: it is the record’s own word,
   `optimality.status: open`, and it fits all three items as questions, whereas
   “optimality unknown” is wrong for a packing that may well be optimal).
   Rows, each with a `?` badge in the same box outlined in a lighter grey (`#9ca5ae`)
   and worded as the negation of a badge meaning: `optimality not proved` when
   `optimality.status` is `open`; `exact value not known` when `exactness.state` is
   neither `closed-form` nor `minimal-polynomial`; `rigidity not established` when
   `rigidity.state` is `not-established`. Nothing else is derived.
   The group is present with a fixed three-row height on every slide; the 19 cases with
   nothing open show a faint italic `nothing open` rather than a bare heading.
   Note n = 28 and 40 carry the muted “annotated rigid by the catalogue” badge and, per
   the record, still list rigidity as open.
   The old outlined “optimality open” row is gone.
5. **Faster.** Defaults 1.5 + 0.5 (still adjustable); readout and length line show the
   new total.
6. **Progress bar.** Inside the stage at the bottom: a 4 px track from x = 90 to 1830 at
   y = 1036, the fill in `#47525f`, `1` and `324` outside the ends, and the current n
   riding above the fill’s leading edge.
   Position = (n − 1 + fade progress) / 323, clamped, so it advances across each fade
   and rests through each dwell and is exactly 1 from the last slide’s dwell on;
   `barAt(t)` exposes it and `stateAt(t)` reports `bar` and `panel`. It is drawn once,
   outside the dissolving layers.
7. **No more ghosting.** The facts panel is now one element above both picture layers
   and cuts at the fade midpoint instead of dissolving: the panel shows n while
   `progress < 0.5` and n + 1 from 0.5 on.
   A cut was chosen over a sequential fade-out/fade-in because text at partial opacity
   is unreadable for the whole of the transition either way, and the cut keeps every
   frame’s text at full strength while the picture is what moves; the midpoint is also
   where the smoothstep dissolve tips from one picture to the other, so the panel always
   belongs to the dominant picture.
   The `aria-live` mirror already switched there.

Also fixed on the way, both v1 defects the review did not see:

- `render()` never set the base layer’s `visibility`, so after a seek that jumped from
  dwell to dwell the layer that had been hidden on top stayed hidden as base and the
  picture was blank (sequential play masked it, because a fade’s last frame had shown
  the layer). Now set on every render; the harness seeks dwell-to-dwell through all 324
  and checks.
- The stage footer was painted under the layers (no z-index) and had never been visible;
  it now sits above them, at y = 972, above the bar.
- Minimal polynomials longer than two record lines (21 of the 36, up to n = 108’s 18,506
  characters, which as one unbroken word ran the layer past the compositor’s limit) are
  no longer printed; the degree note carries what they would add.
  The 15 that fit are spaced for wrapping.

The panel had to fit the new rows in 880 px: the numeral is 132 px (was 144), the value
lines 56/42 px, the status rows 24 px on a 34 px pitch, the record 21 px on 27 px.
Measured over all n, the panel’s deepest point is y = 966 (n = 268, eight record lines)
against the footer at 972, and the nested radical `√(1 + √2)` (n = 54, 107, 178, 267) is
lifted by the 8 px its ascent would otherwise push the baseline down.

`render_review.py` (needs the venv’s Playwright) seeks every n, measures the panel’s
bottom and right edges and any intrusion of a value line into its note, checks the bar
never moves backwards and the cursor label is n, then writes the captures and measures
the headline’s ink. Run it after any layout change.

## What was built

- `build_candidate.py` — the generator.
  Reads `composite-figure.json`, `manifest.json`, the 324 frontier records and the 324
  per-n SVGs, embeds the seven font files, and writes `index.html`. Deterministic (no
  timestamps, no git, no randomness); three builds in this session were byte-identical.
  Runs in about 2.5 s. Flags: `--decimals
  1|2|3` (default 2), `--radical svg|text` (default `svg`), `--repo`, `--out`.
- `index.html` — the candidate, 3,599,570 bytes (revision 3), opens from `file://`. A
  Content-Security-Policy of `default-src 'none'` with `font-src data:` is the guarantee
  that it cannot reach the network even by accident.
- `test_candidate.py` — the smoke test (below).
  `timeline_harness.js` — a Node stub-DOM harness the test calls, which runs the page’s
  own script and exercises `window.atlasVideo` (31 checks, all passing).
  `render_review.py` — the headless layout measurement and screenshot tool (revision 2,
  extended in revision 3).

The page: a 1920×1080 stage scaled to fit the window, paper white.
The packing sits in an 880 px box at (90, 80); the facts panel is a 750 px column at x =
1080\. Two picture layers cross-dissolve: the outgoing layer stays opaque underneath and
the incoming one fades in on top, so the white paper never shows through mid-fade.
The facts panel, the footer and the progress bar sit above both layers; the panel cuts
at the fade midpoint.
Below the stage, the review controls; `?capture=1` in the URL or the “capture preview”
checkbox hides them and shows the stage alone at 16:9.

## Sizes and the per-square encoding

| Part | Bytes |
| --- | --- |
| geometry (points + fills, 52,650 squares) | 2,688,572 |
| facts templates (324 `<template>` blocks) | 492,477 |
| fonts as base64 `@font-face` CSS | 281,977 (209,660 raw) |
| behaviour script | 11,043 |
| radical path and the seven badge symbols | 4,845 |
| markup, CSS, JSON framing | the rest, about 120 KB |
| **index.html** | **3,599,570** |

Per square the generator keeps the fill polygon’s four corners, re-based from the
960×680 canvas to the packing’s own 536×536 box, rounded to 2 decimals with trailing
zeros stripped (`0,198 198,198 198,0 0,0`), and the fill as one base-36 digit into a
sorted 34-colour palette.
Polygons are joined by `;` per n. The outline polygons are dropped; a single `stroke` on
the group draws every edge, and the container is one `<rect>` above the squares, as the
poster does. All 324 container rects were asserted at (36, 36) 536×536 while extracting.

Precision: 0.01 of 536 units is 1.9×10⁻⁵ of the container side, 0.016 px at the 880 px
picture and 0.033 px at a 4K capture.
Adjacent squares share input values, so shared edges round together and stay coincident.
Measured alternatives: 3 decimals gives 3,938,704 bytes, 1 decimal 3,245,791. The full
range ships at 2 decimals; nothing is subset.

## Fonts embedded

From `vendor/kpress/src/kpress/format/static/fonts/` and `.../katex/fonts/`:

| Face | File | Bytes |
| --- | --- | --- |
| PT Serif 400 | pt-serif-latin-400-normal.woff2 | 33,116 |
| PT Serif 400 italic | pt-serif-latin-400-italic.woff2 | 34,896 |
| PT Serif 700 (revisions 1–3; dropped in revision 4) | pt-serif-latin-700-normal.woff2 | 29,588 |
| PT Serif 700 italic (revisions 1–3; dropped in revision 4) | pt-serif-latin-700-italic.woff2 | 28,516 |
| Source Sans 3 Variable (wght 200–900) | source-sans-3-latin-wght-normal.woff2 | 28,740 |
| Source Sans 3 Variable italic | source-sans-3-latin-wght-italic.woff2 | 28,532 |
| “Atlas Symbols” = KaTeX_Main-Regular | KaTeX_Main-Regular.woff2 | 26,272 |

The latin subsets carry neither ≤, ≥, √ nor ≈ (checked with fontTools: 216 glyphs in PT
Serif, 231 in Source Sans; U+2212 minus and × are present).
KaTeX_Main-Regular has them.
It is declared as a seventh family restricted by `unicode-range` to
`U+2208, U+221A, U+2248, U+2264-2265, U+2308-230B` and placed after PT Serif and Source
Sans in both stacks, with `size-adjust: 102.5%` — the value kpress measured for the
Main-Regular slot of its composite math text face.
This is the same composition `katex-text-face.css` uses: the reading face claims Latin,
the KaTeX face follows in the stack for what it does not claim.

The split: PT Serif carries the headline numeral (400 since revision 3), the `s(n)`
lines, the exact form and the lower bound; Source Sans 3 (weight 550, the kpress medium)
carries the kicker, the degree and lower-bound notes, the status labels, the record
block, the stage footer and the controls.
The `s` in `s(n)` is PT Serif italic followed by a 0.055 em kern
(`.fn i { margin-right: 0.055em }`), the poster’s `SUMMARY_ITALIC_KERN` and the
math-text-face plan’s `\mkern1mu` in CSS form.

Radicals are drawn, not typed: each `√` is KaTeX’s `sqrtMain` path (resolved from the
vendored `katex.min.js` with its default parameters) in a `preserveAspectRatio="xMinYMin
slice"` SVG behind the radicand, so the vinculum is part of the surd and cannot
misalign. The paddings (0.03 em top, 0.16 em bottom, 0.92 em radicand offset, a `tall`
variant for the four nested `√(1 + √2)` forms) were computed from PT Serif’s metrics
(ascent 1039, descent 286, cap height 700), not checked by eye.
`--radical text` produces the plain `7 + 4√2` / `√(1 + √2)` notation if the drawn
radical does not read well.
Fractions are stacked (`.frac`, 0.62 em, `vertical-align: middle`).

## What the facts panel shows and where each fact comes from

Fixed slots (the panel does not jump between n): kicker, the `n =` line, the numeral,
five line slots (side; exact form and its degree note, the note first and the empty
exact slot after it when there is no form, since revision 4; lower bound and its note —
empty slots are kept), three badge rows, the `OPEN` heading and three rows, then a
record block that varies in row count but sits last.

From `packing/atlas/known-best/composite-figure.json`, the poster card’s own record,
nothing re-derived:

| On screen | Field |
| --- | --- |
| `s(n) = 12.656854` or `s(n) ≤ …` | `side.display`, `side.relation` (asserted consistent) |
| `= 7 + 4√2` | `exactness.exact_form`, parsed by a small grammar (`INT`, `(p/q)`, `sqrt(...)`, juxtaposition, `+`/`-`) and evaluated against `side.value` to 10⁻⁹ as a build assertion; bare integers are not repeated |
| `ALGEBRAIC DEGREE 2` | `exactness.degree`, shown when ≥ 2 as on the card |
| `s(n) ≥ 12.135528` + “proved lower bound” | `lower.display` when `lower.shown`; the digits are ink on every n (revision 3) |
| status badges | `badges[].glyph` and `style`, drawn as the poster draws them, the star from `lower.first_proved_here` first; labelled `optimal`, `exact`, `numerical`, `rigid`, `rigid (catalogue)`, `new lower bound` (`BADGE_LABELS`), the record’s `meaning` kept for the spoken mirror |
| `OPEN` rows | `optimality.status`, `exactness.state`, `rigidity.state`, as listed under Revision 2, worded `optimality`, `exact value`, `rigidity` since Revision 3 |

From the frontier records `packing/frontier/n-NNN.md` (`reported_upper_bound` and
`reported_lower_bound` blocks) and the manifest:

| Row | Field |
| --- | --- |
| Construction | `construction_method` (`unknown` → “not recorded”) |
| Found | `found_by`, `found_year` (114 cases carry them; the row is omitted otherwise) |
| Improved | `improved_by` (20 cases) |
| Lower bound | `reported_lower_bound.proved_by`, `proved_year`, `kind` (open cases only; the `nagamochi` kind prints as “general bound”) |
| Source | `source_key` spelled out, `catalogue_pictured` as “pictured”; then, as the block’s last line, the URL: `manifest.json` `source.url` for the 147 kingbird/unitsquare renderings, else the frontier’s `record-catalogue` resource URL for the 177 exact grids; the scheme is stripped on screen, the full URL is in the embedded record as `src` |

Two additions beyond the card, both from the record: the `OPEN` group (the card shows
optimality, exactness and rigidity only by the presence of a badge; text needs the
absence spelled), and the “proved lower bound” note under the `≥` line.

Not surfaced, and why: `tilt_angles_deg` (only 7 records carry a non-trivial list; the
picture shows it); `analytically_optimized` (174 nulls); `rigidity.method`, `scope`,
`certificate`, `replay` and the composite’s rigidity `evidence` prose (long paragraphs;
the label carries the result); `verified_upper_bound` (a ceiling, which the record’s own
body text warns is not the side); `conjectured_optimum` (equals the reported side where
present); `witnesses`, `retrieved_date`, `source_date`, `source_reviewed` (how the
repository stores the case, which the playbook keeps off the figure); `priority_notes`,
`blockers`, `conflicts`. Degree 1 is not shown, as on the card.
The minimal polynomial is not shown at all since revision 3 (it was shown for 7 cases in
revision 2); the degree note carries the degree.

One rendering quirk to decide on: n = 11’s `reported_lower_bound.proved_by` is the
string “repository exact H-041 certificate”, which the Lower bound row prints literally
("repository exact H-041 certificate, 2026 (unavoidable points)").

## Timeline and the capture API

Slot = dwell + fade; slide k (n = k + 1) owns [k·slot, (k+1)·slot): dwell, then a fade
into slide k + 1. The last slide fades to paper; the first appears at t = 0 without a
lead-in. Total = 324 × slot = **648 s = 10 min 48.0 s** at the default 1.5 + 0.5
(revision 2; it was 842.4 s at 2.0 + 0.6). The picture dissolve is smoothstep in
opacity; the panel cuts at the fade midpoint; the settle is `scale(0.98 → 1)` with a
cubic ease-out on the incoming picture only.

`window.atlasVideo`: `seek(seconds)`, `frameAt(index, fps)`, `duration()`, `play()`,
`pause()`, `setTiming({dwell, fade})` (keeps the current slide and its phase), plus
`stateAt(seconds)` → `{n, next, progress, phase, panel, bar}` (`panel` is the n the
facts panel shows, `bar` the progress-bar fraction), `barAt(seconds)`,
`setSettle(bool)`, `setCapture(bool)`, `timing()`, `count`, and `ready` (the
`document.fonts.ready` promise).
`seek` and `frameAt` return the state they rendered.

Rendering is a pure function of the virtual clock: no `Date.now`, no `Math.random`, no
`setInterval`; `requestAnimationFrame` deltas advance the clock only while playing.
Slides are built from the record on first use and cached as DOM nodes; both layers are
assigned by time alone (the harness seeks 100 → 5 → 500 → 100 and checks the layer
contents match).

Review controls: play/pause (space), previous/next (arrow keys), Home/End, a scrubber, a
go-to-n field, a readout (`n 147 → 148 (fade 43%) · 04:53.7 / 10:48.0`), dwell and fade
inputs, the settle toggle, and the capture-preview toggle.
The current facts are mirrored into an `aria-live="polite"` region on each slide change
(past the fade’s midpoint).

On the settle: implemented at 2 % as asked and left on by default, with a toggle so it
can be judged against the plain dissolve.
My reservation, unverified because no browser was opened: the container frame is the one
stable element across 323 transitions, and a 2 % breath on it every 2.6 s may read as a
pulse rather than a settle.
If so, drop it (`setSettle(false)` or the checkbox) — it is one line.

## What the smoke test checks (passed)

`test_candidate.py`, run with `packing/.venv/bin/python3`: builds twice into temp
directories and asserts byte identity, and that the shipped `index.html` is that same
build; 324 slides, each with n polygons of 4 corners, n fill digits, a facts template
and an `s(n)` line; no `http://`/`https://` anywhere outside the record, and inside it
only at `slides[i].src` (324 of them); no `fetch(`, `XMLHttpRequest`, `import(`,
`innerHTML`, `eval(`, external `src`/`href` (only `#surd` and the `#badge-*` symbols),
`Date.now`, `Math.random`, `setInterval`; the CSP names no host; for every n, the badge
rows are exactly the record’s (star, then `badges[]`) with their short labels, the
`OPEN` group is present with the rows the record implies, the notes are on their own
lines, the five value slots are in order, the `n =` line is the block before the
numeral’s, and the source-URL line closes the panel; no polynomial row; the numeral’s
rule is weight 400 at 96 px; `a3123f` occurs once outside the fonts and the record, on
the star row, and the star is `currentColor`; every stage `font-size` is an absolute px
value ≥ 28 from a scale of at most four sizes with the largest ≤ 4.5 × the smallest; the
progress bar markup and the 1.5 + 0.5 timing are there; then, with the Node on PATH,
`node --check` on the script and the timeline harness (bar width monotone over 6,481
seeks, panel cut at the midpoint, base layer visible at every seek); then, with
Playwright importable, the survey of every n (panel bottom above the footer and the bar,
inside x = 1830, no value line into its note, the exact line’s baseline within 1 px, the
computed sizes on the scale, the riding n clear of the end labels).
Result: `ok: 3599570 bytes, 324 slides, 324 source URLs, 412 badges, 648.0 s, sizes [28,
34, 44, 96], node=yes, survey=panel bottom 959 < footer 972 < bar 1008`, about 43 s (10
s without the survey).

Visual verification (revision 2): `render_review.py` with the venv’s Playwright and the
pinned headless shell, offline; the captures are in `review/`, looked at and corrected
twice (the blank-layer defect above, then the radical and fraction lines clearing their
notes). Revision 3: the `r3-*.png` stills, looked at and corrected twice (the riding n
against the `324`, then the exact line’s three baselines).

## What a capture pipeline would look like

What is already on this Mac and in the repository:

- `playwright==1.62.0` is pinned in `packing/pyproject.toml` (dev group) and importable
  from the venv; `~/Library/Caches/ms-playwright` holds `chromium_headless_shell-1223`,
  `chromium_headless_shell-1234`, `chromium-1223` and Playwright’s own `ffmpeg-1011`.
  `render_explainer_pdf.py` already has the `SQPACK_CHROMIUM` override pattern for
  pointing at an installed Chrome.
- `ffmpeg` is on PATH at `/opt/homebrew/bin/ffmpeg`. Nothing was installed.

Sketch (`devtools/capture_atlas_video.py`, not written):

1. `page = browser.new_page(viewport={"width": 1920, "height": 1080},
   device_scale_factor=1)`; `page.goto("file:///…/index.html?capture=1")`;
   `page.evaluate("atlasVideo.ready")`.
2. For `i in range(ceil(duration × fps))`: `page.evaluate("atlasVideo.frameAt(%d, %d)")`
   then `page.screenshot(type="png")`, piped to
   `ffmpeg -f image2pipe -framerate 30 -i - -c:v libx264 -pix_fmt yuv420p -crf 16
   -movflags +faststart out.mp4`, or written as PNGs and encoded afterwards.
3. Because frame index → time is a pure function, the run splits across processes by
   frame range and the segments concatenate with `ffmpeg -f concat`.

At 30 fps the default timing is 19,440 frames (revision 2). A headless screenshot of
this page should run 40–80 ms, so a single process is on the order of twenty minutes;
four processes, about five.
Recommendation for v1: 1920×1080 at 30 fps (a 0.5 s fade is 15 frames, enough for a
smooth dissolve).
The source is vector, so a 4K master costs nothing but capture time via
`device_scale_factor=2`; keep the stage layout at 1920×1080 CSS pixels either way.
Use `yuv420p` for players, and expect the 4:2:0 subsampling to soften one-pixel coloured
edges slightly; `-crf 16` keeps the flat fills clean.

## Open questions for the spec

1. Lead-in and end: a title card before n = 1 and a closing card, or the present hard
   start and fade to paper.
   Both change the total length formula.
2. Constant dwell or a schedule: 2.0 s for every n, or longer for the named cases (5,
   11, 12, 17–21, 29, 54, the first-party lower bounds) and shorter for the trivial
   grids, which are 165 of the 324.
3. Colour continuity: hue is assigned per frame by tilt-class size, so the same tilt can
   change hue between n and n + 1 (the inventory’s note).
   Consecutive dissolves will show hue flips on otherwise similar packings.
   The spec should say whether the video wants a stable hue policy or accepts the per-n
   colouring as the atlas’s own.
4. The settle: keep, drop, or apply only on cuts between dissimilar packings.
5. Which record facts belong on screen at all, and the wording of the `OPEN` rows (the
   badges themselves are now the poster’s; the open group is the one addition).
6. The vocabulary of `proved_by` (n = 11 above) if the Lower bound row stays.
7. Reduced-motion: deliberately ignored so rendering depends on nothing but time; a
   viewer-facing web version would want it.
8. Radical typography and the PT Serif/KaTeX pairing: computed from metrics, to be
   judged by eye; `--radical text` is the fallback.
9. Frame rate and master resolution, per the recommendation above.

## Repository files read

Under
`/Users/levy/wrk/github/squares/.claude/worktrees/squares-viz-explanations-4ae624/`:

- `packing/atlas/known-best/rendering/n-005.svg` (in full), and all 324
  `n-001.svg … n-324.svg` by regex in the generator and the corpus check
- `packing/atlas/known-best/composite-figure.json`
- `packing/atlas/known-best/manifest.json`
- `packing/frontier/n-147.md` (in full), and the YAML frontmatter of all 324
  `n-001.md … n-324.md`
- `vendor/kpress/src/kpress/format/static/css/style-tokens.css` (lines 50–97, 555–640)
- `vendor/kpress/src/kpress/format/static/fonts/` — the six woff2 files (metrics and
  cmaps via fontTools, bytes embedded)
- `vendor/kpress/src/kpress/format/static/katex/fonts/` — listing;
  `KaTeX_Main-Regular.woff2` (embedded), `KaTeX_Math-Italic.woff2`,
  `KaTeX_Size1-Regular.woff2` (cmaps only)
- `vendor/kpress/src/kpress/format/static/katex/katex-text-face.css`
- `vendor/kpress/src/kpress/format/static/katex/katex.min.js` (the `sqrtMain` path
  function only)
- `docs/project/specs/active/plan-2026-09-07-math-text-face.md` (lines 22–100)
- `packing/devtools/build_known_best_atlas.py` (lines 1190–1240, `_append_function_text`
  and `SUMMARY_ITALIC_KERN`)
- `packing/src/sqpack/known_best.py` (lines 405–445, the poster’s `CompositeSpec`)
- `packing/pyproject.toml` (lines 62–76 and a grep for playwright/cairosvg)
- `packing/devtools/render_explainer_pdf.py` (grep for `SQPACK_CHROMIUM`)

Outside the repository: the inventory report `explore-A-rendering-and-data.md` in the
scratchpad; `which ffmpeg`, `~/Library/Caches/ms-playwright`, `/Applications/Google
Chrome.app`, and the Node on PATH.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
