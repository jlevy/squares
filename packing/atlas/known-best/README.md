# Known-Best Packing Atlas, `n = 1..324`

This atlas retains one complete geometry record for every frontier case from $n = 1$
through $n = 324$, the witness of the count’s
[house best packing](../../../SYNOPSIS.md#the-measurements), and renders every record
with the repository’s deterministic house renderer.
The machine-readable discovery layer is [`manifest.json`](manifest.json).
The range widened from 100 on 2026-09-07 under
[the expansion plan](../../../docs/project/specs/active/plan-2026-09-07-atlas-expansion-to-324.md).
Two composites are drawn from it: the published figure of the first hundred, with its
10-by-10 layout, and a poster of the whole corpus beside it.
Each tile of both, like every drawing of a count on the site, shows the count’s default
picture: its [regularized view](#the-regularized-views) where that view improves on the
packing as published, and the house rendering of its witness everywhere else
([the default picture](#the-default-picture)). The calibration annotations further down
stay pinned to the first hundred by design.

The geometry records, drawings and exports in this directory are generated.
[`credit-attributions.json`](credit-attributions.json) is the curated input for
lower-bound and optimality-proof acknowledgments; it retains names, roles, source
references and evidenced dates without changing any scientific result.
[figure-playbook.md](figure-playbook.md) is the playbook for both: how to rebuild them,
where each fact on them comes from, what a third would take, and how the poster’s byte
budget was measured.

## The figure, `n = 1..100`

[![The complete known-best atlas from n equals one through one hundred.](known-best-1-100.svg)](known-best-1-100.svg)

The composite is a native 10-by-10 SVG, not a screenshot montage.
Its 5,050 square polygons come from the same normalized witnesses as the individual
figures under [`rendering/`](rendering/) and the regularized views under
[`regularized/`](regularized/index.json).
The title and plain black “The Squares Project · github.com/jlevy/squares” line sit
above the grid; its problem description, legend, construction, lower-bound and
optimality-proof credits, regularization credits and dated diagram credit occupy a
footer.

Both composites share the same two-line problem description, two-column legend and
construction credits.
Each counted legend item names the count and number of cases in that composite, such as
“proved optimal (45 of 100)” or “proved optimal (77 of 324)”. Titles, problem
descriptions and all ordinary text use black; case numbers remain gray.
Changed numerical values and the angle/contact swatches keep their semantic colors.
A bundled bold sans-serif face supplies the print text and its layout measurements.
The gap between information blocks is three body-text ems, measured between their ink
bounds; the lines within a block share 1.50 leading and weight 700. All three credit
paragraphs use the width of the balanced three-line construction paragraph, with
complete names and role clauses kept together.
A fourth paragraph uses the owner’s approved two-line credit on both posters:

```text
Drawn packings are regularized for cleaner display using Squares Project rules,
based on Daniel’s regularizer
```

The paragraph’s SVG group retains the depicted regularized cases in
`data-regularized-cases` and the generators’ complete section 7 credits in
`data-generator-credits`. These structured values preserve the counts and attribution;
they are not printed in the compact credit.

The composite ships in four forms, all drawn from that one SVG in one build:

| File | Size | For |
| --- | --- | --- |
| [`known-best-1-100.svg`](known-best-1-100.svg) | 2150 × 3898 units | the source; scales to anything |
| [`known-best-1-100.png`](known-best-1-100.png) | 2150 × 3898 px | the GitHub-facing raster preview |
| [`known-best-1-100@2x.png`](known-best-1-100@2x.png) | 4300 × 7796 px | attaching, or downscaling for social media |
| [`square-packings-100-20261008.pdf`](square-packings-100-20261008.pdf) | 22.40 × 40.60 in | printing; vector, so text stays selectable |

Each export carries the SHA-256 of its source SVG, so `--check` rejects any one of them
that has fallen behind the drawing.
The 2x raster is scaled by a whole number rather than to a round pixel width: a
fractional scale lands every edge on a fractional pixel boundary, and the antialiasing
shades the rasteriser then invents cost more bytes than the extra pixels do.

## The poster, `n = 1..324`

[![The complete known-best atlas from n equals one through three hundred twenty-four.](known-best-1-324.png)](known-best-1-324.svg)

Every case the register holds, at the figure’s card scale, arranged in a triangle: row
$k$ holds $n = (k-1)^2 + 1$ through $k^2$. All eighteen rows are complete and
right-aligned; the final row has thirty-five cards.
The packing drawings and card scale remain unchanged.
A $k×k$ grid label marks each row’s first retained regular axis-aligned grid packing;
the dimensions and `GRID` form one line rotated 90 degrees beside the grid segment, and
the card retains its ordinary count.
Its distance from the first grid outline matches the ordinary horizontal gap between
boxes. Where irregular packings precede it, an extra gap of half a drawing width (79
units) separates the groups horizontally.
Both PDFs use the same 287-unit row pitch and 203-unit column pitch.
Compared with the 214-unit column and 307-unit row pitches, visible horizontal box gaps
are about 20% tighter, and the annotation-to-next-row clearance is about 25% tighter.
Rows that are all grid receive no added horizontal gap.
The poster draws 52,650 square polygons from the same witnesses.
Its title, complete legend, explanation, construction credits and closing project
details form one block in the upper-left whitespace, leaving the bottom for the final
row of packings. Title and documentation are left-aligned; the legend has two
left-aligned columns, four status rows beside four recency, color and degree rows.
The last right-column item reads “deg is the algebraic degree of that side length,”
without a badge. The first two tilt-color swatches carry black $90^\circ$ and $45^\circ$
labels.
The information starts at the left edge of the first drawing in the final row; at
least 120 units of outside clearance keep the grid labels inside the page margins.
One dark $R$ means known rigid; its verification status, dates and sources remain in the
structured metadata.
The two-line definition uses 66-unit type; the following legend, credits and closing use
48-unit type in the shared bundled body font at weight 700. The definition and all body
lines use normalized leading 1.50, giving the 48-unit lines a uniform 72-unit baseline
pitch. The packing drawings and card captions keep their original scale.
The triangle’s bound captions use five decimal places, one fewer than the figure,
leaving room for the algebraic degree; a longer degree label can shorten the adjacent
side caption to four places.
Upper bounds round upward and lower bounds downward; stored bounds retain their full
precision. Three paragraphs credit best packings, lower bounds and optimality proofs.
Each uses complete canonical names once, ordered from oldest to newest by the earliest
supported result or contribution date.
Year-only dates retain their precision; ties follow alphabetical order.
Acquisition and snapshot dates do not establish priority.
The construction paragraph names all recorded finders and improvers.
The lower-bound paragraph names current bound-source authors; its metadata also retains
method, prerequisite and historical contributions.
The proof paragraph names mathematical proof authors, then everyone who worked on a
formalization or its verification infrastructure in one “formalization by” clause.
Both PDFs use the same acknowledgments for the full $n = 1..324$ corpus; their diagram
counts and depicted ranges remain specific to each figure.
Names wrap intact into balanced lines without bracketed citations or final periods.
Complete source citations, roles and case associations remain in the SVG metadata and
curated credit input.
A section gap separates the credits from the diagram credit, followed by the data date,
a middle dot and the generated edition stamp.
A blank line precedes exactly “The Squares Project” and “github.com/jlevy/squares”.
Both lines use the same 48-unit body font, weight and leading as the legend and credits.
They are plain black text without a hyperlink or PDF annotation, and start flush with
the information block’s left edge.
The black two-line definition appears above the legend: “The square packing problem asks
for the side $s(n)$ of the smallest square that can hold $n$ unit squares, where the
squares are free to rotate but cannot overlap”.
The first line ends after “can”.
The definition and credit paragraphs omit a final period.
Both composites apply the recent accent independently to the numeric value of a new
upper or lower bound.
Case numbers remain gray; relation signs and optimality badges keep their usual styling.
The image above is the raster; the vector it was drawn from is one click away, and the
PDF is a 78.09-by-55.84-inch page.

| File | Size | For |
| --- | --- | --- |
| [`known-best-1-324.svg`](known-best-1-324.svg) | 7497 × 5361 units | the source; scales to anything |
| [`known-best-1-324.png`](known-best-1-324.png) | 7497 × 5361 px | the raster embedded above |
| [`square-packings-324-20261008.pdf`](square-packings-324-20261008.pdf) | 78.09 × 55.84 in | printing; vector, so text stays selectable |

The poster publishes one raster and a vector PDF. The rectangular poster’s 2x raster
measured 5,055,264 bytes for 83 megapixels; the poster publishes a single preview, while
the PDF preserves every square at any zoom.
The link-preview card is one page’s unfurl, which the figure above supplies.

The poster also draws a square more cheaply than the figure does, because ten times as
many of them will not fit in a file anyone should clone.
The poster drops the per-square `data-*` facts, states the stroke once per card instead
of once per polygon, and rounds coordinates to three decimals.
Measured on the rectangular poster, those choices reduced the house encoding’s 490 bytes
a square to 117.7. The triangle uses the same encoding.
All three departures are recorded in the drawing’s own metadata, the facts they drop are
still carried per case by [`rendering/`](rendering/) and
[`composite-figure.json`](composite-figure.json), and each was measured before it was
chosen:

```bash
uv run --frozen --all-extras --group dev python -m devtools.build_known_best_atlas --report
```

[The playbook](figure-playbook.md#the-two-composites) has the measurements and what each
one bought.

## The regularized views

The [regularization policy](../../../docs/project/policies/regularization-policy.md)
governs every view here: what admits a view, what goes to manual review, and what is a
register result instead.

[`regularized/`](regularized/index.json) holds the exact derived views the atlas draws,
one index entry a record under the contract `packing.squares:RegularizedAtlasIndex/v2`
([schema](regularized-atlas-index.schema.yaml)). Each entry names the generator that
decided it:

- **`regularize_axis_components/2`**, this project’s tool, run over every record by
  `python -m devtools.regularize_axis_components --update-atlas`. It straightens
  near-axis squares and slides axis-aligned ones into exact contact at the certified
  side.
- **Evan Daniel’s regularizer**, vendored under `vendor/evand-regularize/` and driven by
  `devtools.regularize_evand`, which brings each view to the record’s own side over the
  rationals where it can.
- **The grid-slack generator**, `devtools.regularize_grid_slack`, a port of his
  coincidence placement that starts from the witness’s exact frame and closes free grid
  slack.

A view from either of the last two enters only where the policy’s decision table admits
it (row 10), by `python -m devtools.regularize_evand layer --select admitted` (a
grid-slack run’s views by adding `--grid-run DIR --grid-counts N ...`, which draws that
run’s view at those counts in place of Evan Daniel’s), and only where it is worse on no
goal of the improvement rule than the picture drawn at that count today: the layer’s
view where the rule draws it, else the house drawing
(`regularize_evand.worse_than_drawn`). A tie is admitted; refusing one is the
selection’s. The axis tool’s own record of that count stays beside it as `reference`.
Such a view carries the credit line *Regularized by the Squares Project with Evan
Daniel’s regularizer (evand/square-packing, MIT)*, in the index, in the view and in its
drawing. The
[regularization process](../../../docs/project/guides/regularization-process.md) gives
the steps from a run to a merged view: generate, select with
`python -m devtools.regularize_select`, admit, render, record and validate.

On 13 October 2026 the index draws 90 views: 20 by the axis tool, 48 by Evan Daniel’s
regularizer (29 at the witness’s side and 19 at the verified upper bound) and 22 by the
grid-slack generator (2 by its version 0 and 20 by its version 1), with 181 records
unchanged and 53 refused.
At sixteen counts Evan Daniel’s views lay below the earlier ceilings and were held; they
were admitted once T-155 registered their exact sides and the runs were decided again
against the case records as they stand (`python -m devtools.regularize_evand reclassify
--refresh-bounds`); at 227 the grid-slack view is drawn instead.
At the 42 counts jlevy/squares#518 re-housed, both generators ran again on the new
witnesses. 14 of Evan Daniel’s views are drawn, each worse on no measure of the drawing
and better on at least one, and 10 grid-slack views where his regularizer admitted none
and the grid view draws better with nothing worse.
16 keep the axis tool’s view: 232’s grid view awaits review; at 236 his view turned two
squares 0.000537 degrees off their group and drew one more angle class; at 180 and 207
his views tied the axis tool’s on all seven measures at the same side, which the owner’s
rule of 13 October 2026 does not draw (“better on one or drawn at a smaller side”); the
three were withdrawn on 13 October; and at the rest neither generator draws better.
At 270 and 305, which jlevy/squares#553 re-housed again after those runs, the views
lapsed with the witnesses they were made from, and the axis tool’s views of the new
witnesses were drawn.
On 13 October 2026 the owner set what a drawn view must be: exactly verified at a side
no larger than the verified upper bound, and better or equal on the drawing, its pose
free to change
([the policy’s section 9](../../../docs/project/policies/regularization-policy.md#9-owner-decisions),
questions 13 to 15). Nineteen counts were drawn again under that rule.
At eight (87, 106, 152, 172, 182, 206, 268 and 301) the drawing sat above the bound, at
a decimal witness’s side, and Evan Daniel’s exact view at the bound is drawn instead.
At eleven a grid-slack view straightened at up to 1 or 5 degrees, or a new half-degree
view, draws better: 146, 176, 181, 199, 238, 239, 267, 270, 271, 305 and 306. Over the
nineteen, light / uneven / near-axis squares go from 78 / 232 / 113 to 39 / 117 / 1, and
house sides from 10,764 to 11,560; light squares under the house rule fall atlas-wide
from 5,455 to 5,381. Seven drawn views stay above the bound, each an exception question
13 names: at 18, 26, 66 and 85 Evan Daniel’s views sit about $10^{-30}$ above a
closed-form optimum (question 4), and at 110, 241 and 297 the drawing is at Francisco
Couzo’s decimal side, $3 \times 10^{-12}$ to $1.3 \times 10^{-11}$ above Evan Daniel’s
exact optimum, where the view at the bound draws fewer shared sides (110 and 241) or
awaits the owner’s review (297). `--check-atlas` and
`packing/tests/test_regularize_select.py` fail on a view above the bound at any other
count, both reading the one list, the axis tool’s `ABOVE_U`.

On 16 October 2026 both generators ran again on the nine witnesses jlevy/squares#614
adopted in `60aa1d39e`, whose strong views had lapsed to the axis tool’s (think-la7h):
Evan Daniel’s regularizer (`evand-regularize-3a-1016`) and grid-slack at 0.5, 1 and 5
degrees (`grid-slack-3a-deg05-1016`, `grid-slack-3a-deg1-1016` and
`grid-slack-3a-deg5-1016`), 6,188 CPU-seconds in all by the producing session’s notes.
The index records the first two, from which views are drawn (3,559.68 and 915.99
CPU-seconds); the runs at 1 and 5 degrees, about 1,712 CPU-seconds, left no block,
receipt or report in this repository.
At 176, where the axis tool’s view drew more uneven squares than the house and the raw
house was drawn, his same-side view is drawn: light / uneven / near-axis squares go from
70 / 71 / 52 to 11 / 24 / 0, angle classes from 83 to 6, and house sides from 33 to 457.
His views are drawn at 129, 146, 156 and 271 too, and grid-slack’s half-degree view at
105, where his view is refused at row 7. Over the six, light / uneven / near-axis
squares go from 88 / 110 / 63 to 26 / 45 / 0, and house sides from 2,017 to 2,553. At
three counts neither generator draws better, and the axis tool’s view stays: at 204 and
303 grid-slack’s view ties it on every goal at all three thresholds, while his view is
refused at row 7 at 204 and held at row 4 at 303, solved above $U$; at 272 grid-slack’s
view is refused at row 7 at every threshold (stage sides fall from 732 to 730), and his
is held at row 4. At 272 and 303 there is no same-side view of his to decide: the
same-side re-solve was refused (`same-side-refused: literal-too-large`: its exact
coordinates are too long for Python to write as text), and the solved view draws fewer
shared sides, at 303 than the witness (house sides 758 to 708, stage sides 798 to 724)
and at 272 than the drawn picture (stage sides 732 to 724). A same-side view of either
arrangement would most likely be refused at row 7 too, though none exists to measure, so
neither settlement rests on how little the solved side exceeds $U$
($2.6 \times 10^{-31}$ at 303, $1.7 \times 10^{-19}$ at 272). The producer’s run
directories stayed on the host that ran them and could not be recovered, so the same
generators ran again from main `e2e018f32`, the revision their selection ran on, and
that evidence is retained in
[`cases/regularized_drawings/think-la7h-2026-10-16/`](../../cases/regularized_drawings/think-la7h-2026-10-16/):
`regularize_select`’s reports (`selection-3a.json` and `selection-3a-d1.json`, every
candidate’s decision and reasons, each beside its Markdown table), each run’s per-count
`report.json`, gzip-compressed, a `run.json` for each grid-slack run (the block
`regularize_grid_slack.run_block` computes from its reports), and each driver run’s
`receipt.json`. Grid-slack ran on all nine counts at all three thresholds
(`grid-slack-3a-rerun-deg05-1016`, `-deg1-1016` and `-deg5-1016`; a container restart
killed 105 and 176 at five degrees, which ran again as
`grid-slack-3a-rerun-deg5b-1016`). The driver ran 105, 129 and 146
(`evand-regularize-3a-rerun-1016`, stopped there for time, so it has no receipt), 204
and 272 (`evand-regularize-3a-rerun-s-1016`), 303 alone
(`evand-regularize-3a-rerun-303-1016`), and 156, 176 and 271
(`evand-regularize-evand-addr644-1016`, 916.52 CPU-seconds, review D1 of #644).
`devtools.default_drawings.SETTLED` records the three settlements as decided on the two
recorded originals and on the reproductions that cover them.
`--check-state` fails on a run it names that the retained evidence does not hold, or
whose record shows it did not run that count.
The layer’s index drops a run’s block once no entry draws from it, so
`default_drawings --retain-runs` copied the two originals’ blocks, and the five others
the settlements of 15 October rest on, into `cases/regularized_drawings/settled-runs/`
(review F1 of #644; the last two copies went on 17 October 2026, when 272 was settled
again on its new witness and no settlement named them).
Every outcome reproduces, and every drawn view byte for byte.
At 129, 146, 156, 176 and 271 `regularize_evand rungs --check` found his admitted view
the drawn view’s text exactly, with the same retry rungs (none), regularizer level (2)
and groups, contact histograms and regularization record.
That comparison ran on the runs’ scratch directories, whose views are not retained.
Each retained `report.json.gz` keeps the rungs, level, groups, contacts and
regularization record the check compares, and the view’s Git blob only as provenance.
Run on the retained evidence, `rungs --check` reads those reports and finds all five in
agreement and none differing: 156, 176 and 271 in `evand-addr644-1016`, and 129 and 146
in `3a-rerun-1016` (review F2 of #644). At 105 grid-slack’s half-degree view is the
drawn view, and so are its views at 1 and 5 degrees (reviews D and E of #644 compared
the bytes).
His same-side views at 105 and 204 are refused at row 7, and his solved views
at 204, 272 and 303 are held at row 4, above $U$; at 204 and 303 grid-slack’s view ties
the drawn picture on every goal at all three thresholds, and at 272 it is refused at row
7 at all three (stage sides 732 to 730). `selection-3a.json` was made before the driver
ran 156, 176 and 271, and without his views there it chose grid-slack’s at 156 and 271,
which the drawn views dominate, and none at 176, where grid-slack’s view goes to review
(row 7); `selection-3a-d1.json`, over his new run and grid-slack’s runs at those three
counts on main’s tree, chooses his view at each, with the drawn views’ measures.
After this batch the index draws 92 views: 28 by the axis tool, 49 by Evan Daniel’s
regularizer (30 at the witness’s side and 19 at the verified upper bound) and 15 by the
grid-slack generator (1 by its version 0 and 14 by its version 1), with 181 records
unchanged and 51 refused.

The same day both generators ran on the eight witnesses jlevy/squares#614 adopted in
`3b9fab84a` at 153, 154, 207, 211, 237, 241, 302 and 304 (think-kpm3): Evan Daniel’s
regularizer (`evand-regularize-3b-1016`) and grid-slack at 0.5, 1 and 5 degrees
(`grid-slack-3b-deg05-1016`, `grid-slack-3b-deg1-1016` and `grid-slack-3b-deg5-1016`),
3,916 CPU-seconds in all.
His views at the witness’s side are drawn at 153, 207, 211, 237, 241 and 302: the
same-side re-solve’s at the first four, and at 241 and 302, where the re-solve was
refused (an overlap, an unmatched rotation), his solve itself, unmodified, which closed
to that side. Grid-slack’s five-degree view is drawn at 154, where his view goes to the
owner at row 7 (eight squares lose a contact while no total falls).
Over the seven, light / uneven / near-axis squares go from 51 / 133 / 34 to 10 / 26 / 3,
and house sides from 3,957 to 4,341. At 304 every view draws two or four light squares
where the axis tool’s view draws none, so that view stays: grid-slack’s at all three
thresholds, and his, held at row 4, solved $8.9 \times 10^{-31}$ above $U$.
`devtools.default_drawings.SETTLED` records it as decided on these four runs.
At 153 and 207 his solved views lie below $U$, by $1.6 \times 10^{-14}$ and
$2.4 \times 10^{-12}$; they are register candidates for the owner and are not drawn.
The evidence for these choices and for 304 is retained in
[`cases/regularized_drawings/think-kpm3-2026-10-16/`](../../cases/regularized_drawings/think-kpm3-2026-10-16/):
`regularize_select`’s report (`selection-3b.json`, every candidate’s decision and
reasons, and `selection-3b.md`), the driver’s `receipt.json`, and each run’s per-count
`report.json`, gzip-compressed.
Grid-slack keeps no receipt of its own, so each of its three runs has a `run.json`, the
block `regularize_grid_slack.run_block` computes from its reports; the index records
only the five-degree run, which supplied a view, and that block is the same as the
index’s. Its cost is the per-count seconds the reports record, which are wall seconds
under load. The views themselves are not retained beyond the seven the layer draws.

Last that day both generators ran on the three witnesses jlevy/squares#598 adopted in
`8a4d26fea` at 175, 232 and 264 (think-3zi3): Evan Daniel’s regularizer
(`evand-regularize-3c-1016`) and grid-slack at 0.5, 1 and 5 degrees
(`grid-slack-3c-deg05-1016`, `grid-slack-3c-deg1-1016` and `grid-slack-3c-deg5-1016`),
2,050 CPU-seconds in all.
His same-side views are drawn at 175 and 232, and grid-slack’s half-degree view at 264,
where his regularizer gave no view (its certificate overlapped by $2.1 \times 10^{-14}$
and upstream’s checker refused it).
Over the three, light / uneven / near-axis squares go from 19 / 64 / 0 to 13 / 57 / 0,
and house sides from 1,859 to 1,963. No count is pending any more:
`devtools.default_drawings.PENDING_ALLOWED` is empty.
The evidence is retained in
[`cases/regularized_drawings/think-3zi3-2026-10-16/`](../../cases/regularized_drawings/think-3zi3-2026-10-16/),
in the same layout as think-kpm3’s: `selection-3c.json` and `selection-3c.md`, the
driver’s `receipt.json`, each run’s per-count `report.json`, gzip-compressed, and a
`run.json` for each grid-slack run; the index records only the half-degree run, which
supplied a view, and that block is the same as the index’s.

The same day both generators ran again at the ten counts recorded as decided on 15
October whose decision still owed runs or a per-count outcome (think-0ut1), and at 270
and 305, whose witnesses jlevy/squares#553 adopted after Evan Daniel’s regularizer last
ran there (think-zjmt): his regularizer (`evand-regularize-leftovers-1016`, 2,917
CPU-seconds) and grid-slack at 0.5, 1 and 5 degrees (`grid-slack-leftovers-deg05-1016`,
`grid-slack-leftovers-deg1-1016` and `grid-slack-leftovers-deg5-1016`, 1,613
CPU-seconds), which also ran at 301 (think-co6o). None draws better than the picture
drawn today, so nothing was admitted.
At 102, 258, 263 and 269, Evan Daniel’s own regularized lists (`T-146`), both generators
draw no change at every threshold; at 236 his view draws one more angle class and hue
than the house, and grid-slack draws no change.
Of the five counts drawn by the axis tool’s view, at 180 every view of both generators
ties it on every goal; at 123 grid-slack’s view ties it and his is refused at row 7
(house sides fall from 329 to 314); at 155 grid-slack’s view draws one more light and
one more uneven square at every threshold, and his is held at row 4, solved about
$10^{-30}$ above $U$; at 179 both are refused at row 7, a stage total falling from 535
to 533 and 531; and at 110, drawn at Francisco Couzo’s decimal side above $U$, his exact
view at the bound and grid-slack’s views are refused at row 7, drawing fewer shared
sides. At 270 his view is held at row 4, solved $1.7 \times 10^{-19}$ above $U$, and at
305 it is refused at row 7, a total of shared sides falling; grid-slack’s views there
tie the drawn ones or draw worse.
At 301 grid-slack’s 1- and 5-degree views, which draw no light, uneven or near-axis
square, sit at the decimal witness’s side, $4.6 \times 10^{-12}$ above $U$, and draw 14
angle classes, where Evan Daniel’s view at the bound, drawn since 13 October, draws 8.
`devtools.default_drawings.SETTLED` records the ten as decided on these four runs, each
with its outcome, and none owes a run any longer.
No settlement names any longer the five earlier runs whose blocks `settled-runs/` kept
for those decisions (`evand-regularize-full`, `evand-regularize-refreshed-adopt518-v2`,
`evand-regularize-adopt518-v2-rerun-2026-10-13`, `evand-regularize-bound-1013` and
`grid-slack-on518`), so the five copies are deleted, and `--check-state` fails on a copy
no settlement names (review G2 of #644). The runs’ receipts and per-count reports, and
the selection’s report, are kept in
[`cases/regularized_drawings/think-0ut1-2026-10-16/`](../../cases/regularized_drawings/think-0ut1-2026-10-16/),
without the views.
The same directory keeps the audit probe at 307, grid-slack at 1 and 5
degrees (`leftovers-audit-deg1-1016` and `leftovers-audit-deg5-1016`), which
straightened nothing and drew the drawn view’s measures, so nothing was admitted, and
`grid-slack-timing.tsv`, each grid-slack invocation’s measured wall, user and system
seconds. On 17 October 2026 an adoption under the house rule moved 29 to PR #622’s
certificate (T-195), PingYou Ltd’s tighter certificate of Thomas Schadt’s packing as
David Ellsworth improved it (think-30n2). Both generators had run on that witness the
day before, on a trial branch that wrote it byte for byte as the adoption does: Evan
Daniel’s regularizer (`evand-regularize-adopt-2026-10-16-n29-evand`) and grid-slack at
0.5, 1 and 5 degrees (`grid-slack-adopt-2026-10-16-n29-grid-0.5`, `-grid-1` and
`-grid-5`), about 2.5 CPU-minutes in all.
Grid-slack changes no square and ties the house drawing on every goal, and his view,
$5.93 \times 10^{-20}$ above the certificate’s side, is held at row 4, so 29 is decided
with no better view (`devtools.default_drawings.SETTLED`) and draws its house.
The evidence is retained in
[`cases/regularized_drawings/think-30n2-2026-10-16/`](../../cases/regularized_drawings/think-30n2-2026-10-16/),
in the same layout: `selection-n29.json` and `selection-n29.md`, the driver’s
`receipt.json`, each run’s `report.json`, gzip-compressed, and a `run.json` for each
grid-slack run, the block `regularize_grid_slack.run_block` computes.

Every drawn view carries its regularization in the register’s terms (`by: project`, the
method, the side and the identity measured here), and `results.yaml`’s
`regularized_drawings` records each one whose packing a registered result holds,
generated by `python -m devtools.regularized_drawings`. The same tool writes a
`regularization` note into the case record of every drawn count: who regularized the
drawing, with which of this project’s modifications to Evan Daniel’s regularizer, at
which side and of which result’s packing, and that it is a pure regularization, which
proves no new bound and is not a result, or, at the fifteen counts where `T-155`
registered the drawn regularization’s exact side as an upper bound, that its side is
registered as that result
([the policy’s question 16](../../../docs/project/policies/regularization-policy.md#9-owner-decisions)).
Where the house is itself a regularization its source published, as at the thirteen
counts drawn from `T-146`’s certificates, the note credits the source first.
The 44 counts where `T-155` registered this project’s regularization but the layer draws
another view or none carry the note as well, crediting the Squares Project and naming
`T-155`. At 33 of `T-155`’s 59 counts, eight drawn and 25 not, its side is the side of
Evan Daniel’s earlier certificate (`T-101`), so the note says that `T-155` registers it,
that his certificate first certified it, naming `T-101`, and that it proves no new
bound. No view changes a side, a frontier value, an evidence tier or a credit, and none
replaces a witness. The modifications are read from each entry’s `run` and `method`: the
retry rungs the solve climbed (`run.rungs`), or before the retry ladder of 12 October
the one retry’s arguments (`run.retried_with`). The 23 vendored views admitted after the
ladder had no rungs recorded; on 13 October 2026
`python -m devtools.regularize_evand rungs` recorded them from their runs’ retained
reports at eight counts and, at the fifteen then drawn from the run on
jlevy/squares#518’s witnesses, from a fresh run of those counts,
`evand-regularize-adopt518-v2-rerun-2026-10-13` (917 s of wall, 2,097 CPU seconds at
three workers), whose views came out byte for byte the drawn ones.
Thirteen of the fifteen are drawn now, so 21 entries carry the rungs: Evan Daniel’s
views at 180 and 207 were withdrawn the same day, and their entries with them.
Each entry names the run that supplied its rungs as `run.rungs_from`, and the index’s
`runs` records the fresh run beside the runs whose views it draws.
A run’s receipt records no id, and the driver names a run by its directory,
`evand-regularize-<run directory>`; the fresh run’s directory was also `adopt518-v2`, so
that convention gives it the id of the 12 October run of 37 counts in
`runs/adopt518-v2`, whose reports `evand-regularize-refreshed-adopt518-v2` decided
again. Its id was therefore assigned afterwards, on 13 October 2026, by
`python -m devtools.regularize_evand rename-run`, and its block’s `id_note` says so.
The tool never writes over rungs or a retry an entry already records.
Only 152 climbed a rung (`force-kkt`); with 18’s earlier `dps-100`, those are the two
vendored views drawn with a retry, and none used a replica patch.
Exploration
[X-049](../../campaign/explorations/X-049-families-shading-and-the-large-n-limit.md#exact-regularization)
explains why the layer exists and what the axis tool changes.

Later that day the adoption of the 16 October review (think-z7wn) moved the houses at
129, 146, 154, 156, 175, 176, 204, 211, 232, 237, 264, 271, 302, 303 and 304, so the
views the stack had drawn there lapsed to the axis tool’s view of each new witness.
Both generators ran on the fifteen new witnesses: Evan Daniel’s regularizer
(`evand-regularize-z7wn-a-1016` and `evand-regularize-z7wn-b-1016`, 4,817 CPU-seconds)
and grid-slack at 0.5, 1 and 5 degrees (`grid-slack-z7wn-{a,b}-deg05-1016`, `-deg1-1016`
and `-deg5-1016`, 3,487 CPU-seconds).
The selection of the counts 129 to 211 draws his same-side views at 129, 146, 175 and
204, grid-slack’s half-degree view at 156 and its five-degree view at 154; at 176
grid-slack’s views draw more uneven squares than the axis tool’s and his is held at row
4, so 176 is decided no better, as the owner settled it on 16 October (“Adopt as
settled”). At 211 every view of both generators goes to review at row 7 (a square’s
contact count falls while no total does), though his same-side view betters the drawn
axis view on every measure; the owner admitted it the same day, as recommended (“Admit
it (Recommended)”), by the layer’s first review record, in
[`regularized/reviews.yaml`](regularized/reviews.yaml).
The selection of 232, 237, 264, 271, 302, 303 and 304, which did not finish by that
pass’s stop time, ran the same day on the same runs (think-r3cl, 28 minutes of wall at
two workers): it draws grid-slack’s half-degree views at 232, 264 and 271 and its
five-degree view at 302, which draws no light, uneven or near-axis square.
At 237 every view, admitted at row 10, draws one more light and one more uneven square
than the axis tool’s view of the new witness (6 / 10 against 5 / 9); at 303 grid-slack’s
views tie it on every goal and his solved view is held at row 4; at 304 every view draws
light squares where it draws none, and his solved view is held at row 4. So those three
are decided no better, and his same-side re-solve at 303 and 304 was refused, its
literal too large. The evidence is retained in
[`cases/regularized_drawings/think-z7wn-2026-10-16/`](../../cases/regularized_drawings/think-z7wn-2026-10-16/)
in think-kpm3’s layout, with `selection-z7wn-a.json` and `selection-z7wn-a.md` for the
counts 129 to 211 and `selection-r3cl.json` and `selection-r3cl.md` for the rest.
After it, with 211, the index draws 92 views: 19 by the axis tool, 52 by Evan Daniel’s
regularizer and 21 by the grid-slack generator (1 by its version 0 and 20 by its version
1).

On 17 October 2026 the adoption under the owner’s house rule (think-3mry) moved 37
houses to PingYou Ltd’s certificates of PR #574 (T-174), 1.7e-99 to 1.8e-19 below the
earlier ones: 68, 84, 86, 103, 105, 108, 110, 127, 130 to 132, 155, 172, 179 to 182,
206, 208 to 210, 228, 238 to 240, 261, 263, 268 to 270, 272, 273, 297 and 305 to 308.
Every earlier view there was drawn at the earlier house’s side, now above $U$, so 28
strong views lapsed to the axis tool’s view of each new witness.
Both generators ran on the 35 counts that read pending, Evan Daniel’s regularizer
(`evand-regularize-adopt174-1017`, 6,947 CPU-seconds, and at 206, where it timed out,
`evand-regularize-adopt174-b-1017` with a 1,800-second limit, which timed out too) and
grid-slack at 0.5, 1 and 5 degrees (`grid-slack-adopt174-deg05-1017`, `-deg1-1017` and
`-deg5-1017`, 13,313 CPU-seconds), and in runs of their own (`adopt174-c-*`) on 103 and
261, which read regular as published.
His solved views lie about $10^{-19}$ above $U$ at nearly every count and are held at
row 4. The selections draw his same-side view at 172, grid-slack’s half-degree views at
105, 131, 181, 206, 239, 261, 270 and 307 and its five-degree views at 238 and 305; 103
stays regular as published, and the other 25 are decided no better
(`devtools.default_drawings.SETTLED`, each with what the runs found).
No view went to the review queue: the row-7 views, at 110, 272 and 273, are refusals, a
total of shared sides falling.
At 206, 239 and 306 the drawing now drawn is worse than the strong view it replaces on
shared sides (and at 206 on angle classes and hues, at 239 on light squares), since no
view of the new witness draws as well; by the house rule that is no reason to keep the
larger house.
110 and 297, drawn at Francisco Couzo’s decimal sides above $U$ until then,
leave the exceptions question 13 names.
The evidence is retained in
[`cases/regularized_drawings/think-3mry-2026-10-17/`](../../cases/regularized_drawings/think-3mry-2026-10-17/)
in think-kpm3’s layout, with `selection-adopt174.json.gz` and `selection-adopt174.md`
for the 35 and `selection-adopt174-c.json.gz` and `selection-adopt174-c.md` for 103 and
261\. After it the index draws 92 views: 36 by the axis tool, 36 by Evan Daniel’s
regularizer and 20 by the grid-slack generator’s version 1.

On 19 October 2026 the adoption of Evan Daniel’s certificates (think-ip1p) moved four
houses: 155 to T-197, 229 to T-199, 236 to T-218 and 271 to T-219, $4.46 \times 10^{-5}$
to $6.69 \times 10^{-3}$ below the earlier ones.
Both generators ran on all four, Evan Daniel’s regularizer
(`evand-regularize-adopt-2026-10-19-n155-271-evand`, 1,199 CPU-seconds) and grid-slack
at 0.5, 1 and 5 degrees (`grid-slack-adopt-2026-10-19-n155-271-grid-deg05`, `-grid-deg1`
and `-grid-deg5`, 2,758 CPU-seconds).
The selection draws grid-slack’s half-degree view at 155 and his same-side views at 236
and 271. At 229 his driver draws no view, and grid-slack’s views, better than the axis
tool’s on every goal, go to the owner’s review at row 7 (two squares’ contact counts
fall while no total does), so 229 is decided no better on the axis tool’s view until a
review record admits one; the catalogue’s packing it replaces was regular as published.
At 271 the view drawn now has two more uneven squares than the strong view of the
earlier house; by the house rule that is no reason to keep the larger house.
The evidence is retained in
[`cases/regularized_drawings/think-ip1p-2026-10-19/`](../../cases/regularized_drawings/think-ip1p-2026-10-19/README.md).
After it the index draws 93 views: 36 by the axis tool, 37 by Evan Daniel’s regularizer
and 20 by the grid-slack generator’s version 1.

The same day the adoption of Evan Daniel’s original n183 certificate (T-220, think-jh4w)
moved 183 from the trivial $14 \times 14$ grid to a house $4.20 \times 10^{-4}$ below
it, whose house drawing has 21 light, 51 uneven and no near-axis squares.
The axis tool’s view of the new witness was drawn first, and the count read pending.
Both generators then ran on it, on a shared host at a load average of about fifteen:
Evan Daniel’s regularizer (`evand-regularize-adopt-2026-10-19-n183-evand`, 345
CPU-seconds, 892 seconds of wall at two workers) and grid-slack at 0.5, 1 and 5 degrees
(`grid-slack-adopt-2026-10-19-n183-grid-0.5`, `-grid-1` and `-grid-5`, 388, 375 and 352
seconds, the per-count seconds their reports record).
Every view is admitted at row 10 at the witness’s own side.
The three grid-slack runs drew one view, which ties his same-side view on light, uneven
and near-axis squares and on house sides, and draws one more angle class, one more hue
and two fewer stage sides.
So the selection draws his same-side view: light / uneven / near-axis squares 2 / 8 / 0,
as the axis tool’s view draws them, against the house drawing’s 21 / 51 / 0; 18 angle
classes and hues against 19; and 426 / 446 house and stage sides against the axis view’s
410 / 438 and the house drawing’s 327 / 390. It moves 24 squares, by at most 0.358, and
turns none by more than 6.23 degrees.
The evidence is retained in
[`cases/regularized_drawings/think-jh4w-2026-10-19/`](../../cases/regularized_drawings/think-jh4w-2026-10-19/)
in think-kpm3’s layout, with `selection-n183.json` and `selection-n183.md`. After both
the index draws 94 views: 36 by the axis tool, 38 by Evan Daniel’s regularizer and 20 by
the grid-slack generator’s version 1.

On 20 October 2026 the adoption of Evan Daniel’s certificates of #694 and #689
(think-115j, think-h8jm) moved the house best packing at two counts: 154 to T-222,
$1.06 \times 10^{-4}$ below T-186, and 308 to T-221, $1.12 \times 10^{-3}$ below T-174.
The axis tool’s views of the new witnesses were drawn first, and both counts read
pending. Both generators then ran on both, niced, on a shared four-core host: Evan
Daniel’s regularizer (`evand-regularize-adopt-2026-10-20-n154-308-evand`, 275
CPU-seconds, 239 seconds of wall at two workers) and grid-slack at 0.5, 1 and 5 degrees
(`grid-slack-adopt-2026-10-20-n154-308-grid-deg05`, `-grid-deg1` and `-grid-deg5`, 186,
187 and 142 seconds, the per-count seconds their reports record).
The grid runs ran in directories named `-grid-0.5`, `-grid-1` and `-grid-5`, the names
`adopt_houses` prints, and were renamed before the selection read them, since a run’s id
takes no dot. The selection, 68 seconds of wall at two workers, admits a view at both
counts at row 10, at the witness’s own side.
At 154 it draws his same-side view: light / uneven / near-axis squares 5 / 12 / 0
against the axis view’s 5 / 15 / 3, 10 angle classes and hues against 19, and 421 / 421
house and stage sides against 394 / 408; it moves 60 squares, by at most 0.078. The
strong view of the earlier house best packing it replaces, grid-slack’s of T-186, had 9
uneven squares and 419 stage sides; by the house rule that is no reason to keep the
larger house best packing.
At 308 his solved view goes to the owner’s review at row 7 (32 squares’ contact counts
fall while no total does) and his same-side re-solve refuses the certificate’s literal
as too large, so the selection draws grid-slack’s half-degree view, which ties the axis
tool’s view on light, uneven and near-axis squares (9 / 20 / 0), classes (34) and hues
(19) and adds house and stage sides, 770 / 840 against 750 / 834. The earlier house best
packing was decided no better on the axis tool’s view of T-174, and its settlement goes
with the witness it was made on.
The evidence is retained in
[`cases/regularized_drawings/think-h8jm-2026-10-20/`](../../cases/regularized_drawings/think-h8jm-2026-10-20/)
in think-kpm3’s layout, with `selection-adopt-2026-10-20-n154-308.json` and `.md`. After
it the index draws 94 views: 35 by the axis tool, 39 by Evan Daniel’s regularizer and 20
by the grid-slack generator’s version 1.

On 20 October 2026 the adoption of Joost de Winter’s certificates of issue 668 (T-196,
think-qdcc) moved 227 and 260 from the Kingbird catalogue’s packings to house best
packings $7.27 \times 10^{-3}$ and $1.11 \times 10^{-2}$ below them.
At 227 the grid-slack view of the earlier witness lapsed; at 260 the earlier house
drawing was regular as published, and the axis tool made a view of the new witness.
Both generators then ran on both counts, on a shared host at a load average of about
thirteen: Evan Daniel’s regularizer (`evand-regularize-adopt-2026-10-20-n227-260-evand`,
243 CPU-seconds and 535 seconds of wall at two workers by its receipt) and grid-slack at
0.5, 1 and 5 degrees (`grid-slack-adopt-2026-10-20-n227-260-grid-deg05`, `-grid-deg1`
and `-grid-deg5`, 30, 29 and 31 seconds, the per-count seconds their reports record,
retained under those names though they ran as `-grid-0.5`, `-grid-1` and `-grid-5`); the
selection took 139 seconds of wall at two workers.
Every same-side view is admitted at row 10 at the witness’s own side, and the selection
draws his same-side view at both counts.
At 227 it has no uneven and no near-axis square, 5 angle classes and hues and 676 / 684
house and stage sides, against the new house drawing’s 4 uneven and 3 near-axis squares,
11 classes and 650 / 678 sides, and grid-slack’s 8 classes and 674 / 680 sides; it is
worse than the lapsed view of the catalogue’s packing (2 classes, 809 sides), which by
the house rule is no reason to keep the larger packing.
At 260 it has no light and no uneven square against the house drawing’s 3 and 20, and
778 sides against 754 and grid-slack’s 774. His driver’s solved views at both counts are
below the new sides, by $1.66 \times
10^{-8}$ and $1.81 \times 10^{-8}$: register candidates (policy row 3), listed in the
selection and not admitted here.
The evidence is retained in
[`cases/regularized_drawings/think-qdcc-2026-10-20/`](../../cases/regularized_drawings/think-qdcc-2026-10-20/),
with `selection-n227-n260.json` and `selection-n227-n260.md`. After both adoptions of
the day the index draws 95 views: 35 by the axis tool, 41 by Evan Daniel’s regularizer
and 19 by the grid-slack generator’s version 1.

On 21 October 2026 the adoption of Evan Daniel’s certificate of #703 (think-a9jp) moved
the house best packing at 270 to T-224, $3.47 \times 10^{-5}$ below T-174: another
arrangement of the design of Nate Chaoweeraprasit’s #500 packing, which T-174 refines.
The axis tool’s view of the new witness was drawn first (light / uneven / near-axis
squares 5 / 10 / 1, 22 angle classes, 735 / 746 house and stage sides), and the count
read pending. Both generators then ran on it, niced, on a shared four-core host:
grid-slack at 0.5, 1 and 5 degrees (`grid-slack-adopt-2026-10-21-n270-grid-deg05`,
`-grid-deg1` and `-grid-deg5`, 58.6, 59.0 and 50.5 seconds by their reports, the first
two side by side) and Evan Daniel’s regularizer
(`evand-regularize-adopt-2026-10-21-n270-evand`, 233 CPU-seconds, 237 seconds of wall at
two workers).
The selection, 33 seconds of wall at two workers, admits his solved view at
row 10, at the witness’s own side, since his same-side re-solve was refused for an
overlap: 5 / 10 / 0, 21 classes and 19 hues, and 743 / 753 sides; it moves 24 squares
beyond $10^{-3}$, by at most 0.130, and turns one square upright from 0.2175 degrees.
Grid-slack’s three views were admissible too, but none dominates it (743 / 749 sides).
The strong view of the earlier house best packing, grid-slack’s half-degree view of
T-174, had 4 light and 9 uneven squares against this view’s 5 and 10; by
[the house rule](../../campaign/result-import.md#the-house-rule) that is no reason to
keep the larger packing.
The evidence is retained in
[`cases/regularized_drawings/think-a9jp-2026-10-21/`](../../cases/regularized_drawings/think-a9jp-2026-10-21/)
in think-kpm3’s layout, with `selection-adopt-2026-10-21-n270.json` and `.md`. After it
the index draws 94 views: 35 by the axis tool, 40 by Evan Daniel’s regularizer and 19 by
the grid-slack generator’s version 1. With the adoption at 227 and 260 merged beside it,
the index draws 95 views: 35 by the axis tool, 42 by Evan Daniel’s regularizer and 18 by
the grid-slack generator’s version 1.

On 20 October 2026 the adoption of Francisco Couzo’s issue-678 certificates (T-223,
think-xu4d) moved the house best packing at 204 from T-186, $2.04 \times 10^{-5}$ below
it, and on 21 October 2026, once #704’s adoption had landed, at 260 from Joost de
Winter’s T-196, $2.56 \times 10^{-5}$ below it.
Both generators ran on T-223’s witnesses at both counts, Evan Daniel’s regularizer
(`evand-regularize-adopt-2026-10-20-n204-260-evand`, 222 CPU-seconds) and grid-slack at
0.5, 1 and 5 degrees (`grid-slack-adopt-2026-10-20-n204-260-grid-deg05`, `-grid-deg1`
and `-grid-deg5`, 173 CPU-seconds).
The selection draws grid-slack’s half-degree view at 204, where his view of the earlier
witness lapsed. At 260 every strong view goes to the owner’s review at row 7 (some
squares’ contact counts fall while no total does), so 260 is decided no better on the
axis tool’s view until a review record admits one (think-fltj); his view of T-196, which
#704 drew there, lapses with its witness.
At both counts his solved view lies below the witness’s side, by $1.39 \times 10^{-9}$
and $2.51 \times 10^{-11}$: register candidates (think-ql4v), not drawn.
The evidence is retained in
[`cases/regularized_drawings/think-xu4d-2026-10-20/`](../../cases/regularized_drawings/think-xu4d-2026-10-20/README.md).
After it the index draws 95 views: 36 by the axis tool, 40 by Evan Daniel’s regularizer
and 19 by the grid-slack generator’s version 1.

### The default picture

On 13 October 2026 the owner made the regularized view the default picture, with the
house drawing kept as published
([the policy’s section 12](../../../docs/project/policies/regularization-policy.md#12-the-default-picture)).
A count’s tile on both composites, its atlas tile and frontier-survey thumbnail on the
site and the drawing that heads its case page are its regularized view where the view is
exactly verified on both routes, at a side no larger than the verified upper bound or
one of the exceptions question 13 names, and improves on the house drawing under the
policy’s
[improvement rule](../../../docs/project/policies/regularization-policy.md#11-the-improvement-rule):
worse on none of its goals and better on at least one, exactness included.
The case page keeps the house drawing one click away, under *As published*, with its
source’s credit; everywhere else the house drawing is the picture.

[`default-drawings.json`](default-drawings.json)
([schema](default-drawings.schema.yaml)), written by
`python -m devtools.default_drawings --update`, records each drawn view’s default, its
reason, and both drawings’ measures.
Its `totals` say how many views are defaults; its entries say which, and why each of the
others keeps the house: a view that replaces a numerically checked witness with an
exactly verified one may tie it on every measure, and a view that ties an exactly
verified house at its own side on every goal is no improvement, so the house stays its
picture and its case page says so.
The records-tier step `default pictures improve on their house drawings` measures every
view and its house drawing again on each pull request, fails on a stale record or a
regularized default the rule refuses, and lists the counts that keep the house; this
file states no count of its own, so it cannot fall behind the record.
It reads the exceptions above the bound from `devtools.default_drawings.ABOVE_U`, which
`packing/tests/test_regularize_select.py` holds to the layer.

The same file’s `states` says, for every count n = 1..324, whether the picture it draws
is regularized: `regularized` where a view of Evan Daniel’s regularizer or the
grid-slack generator is drawn, `regular-as-published` where the house drawing has no
uneven and no near-axis square, `decided-no-better` where the strong generators ran on
that very witness and drew nothing better, `exempt` with the bead that owns it, and
`pending` otherwise.
Each state carries the drawn picture’s measures, the witness’s id, its source’s key,
path and revision, and its side, and the runs that decided it.
The index’s `status: regularized` means only that the layer holds a view: at n = 176 it
held the axis tool’s view while the raw house was drawn.
A view that lapses with its witness is now recorded on the axis tool’s record (`lapsed`)
rather than only printed.
The records-tier step
`every drawn picture is regularized, regular as published, decided or exempt` fails on a
pending count that `devtools.default_drawings.PENDING_ALLOWED` does not name with its
bead, and on a named count that is no longer pending; `bead tree` holds each bead the
list names open.

`--check-atlas` runs in the records tier on every pull request: it holds the index to
the manifest, the witnesses and the views by digest, and reads each other generator’s
view against its entry (label, generator, credit, side and regularization).
It also holds every drawn view’s exact side to the witness’s own side $s_W$, which is
what `same` means, and to the case record’s verified upper bound $U$, decided exactly
for a closed-form $U$ as well: no view below $U$, a `bound` view exactly at it, and no
view above it at a count the tool’s `ABOVE_U` list does not name with its reason.
Seven views sit above $U$ at this layer, each a rounding above it and each an exception
question 13 names: four of Evan Daniel’s about $10^{-30}$ above a closed-form optimum,
and three at Francisco Couzo’s decimal side, $3 \times 10^{-12}$ to
$1.3 \times 10^{-11}$ above Evan Daniel’s exact optimum.
`--verify-atlas` is the deferred step `regularized atlas views re-derive exactly`, on a
`regularized-views` runner of its own in both the deep gate and the post-merge
checkpoint
([development.md](../../../development.md#the-deep-gate-the-deferred-surface-before-the-merge)):
it re-derives every axis-tool record, the references included, and decides each other
generator’s view again on both maintained exact routes, with its square count, its
identity against the witness and its shades measured again.

**The axis tool still refuses 71 Kingbird-derived records.** Their 36-digit poses
overlap by a rounding sliver at centre dilation 1, the only factor the tool uses; Evan
Daniel’s regularizer, re-solved at that promotion’s side, now draws three of them
($n = 18$, $66$ and $85$), and the rest stay refused here.
The index refuses one more record, $n = 51$, whose witness is exact over
$\mathbb{Q}(\sqrt{2})$, because the layer has no field arithmetic.
`promote_rational` would try wider ones: it scales every centre about the container’s
centre by $1 + 10^{-p}$, $p = 31, 29, \ldots, 3$, and keeps the first exact packing
within $10^{-9}$ of the printed side.
The tool’s `--smallest-dilation` flag runs that ladder.
On 2026-10-02 it was run over the 89 records refused at that time, and the census’s
`--witness` mode shaded each source and view.
The later SQUISH import replaces two of those source poses with exactly feasible
rational packings; the historical census below describes the earlier poses:

| Smallest verifying dilation | Records | Views below the register’s verified bound | Light green, house rule | Light green, stage rule |
| --- | ---: | ---: | --- | --- |
| $1 + 10^{-31}$ | 53 | 49 | 1,355 → 1,353 | 1,355 → 1,353 |
| $1 + 10^{-29}$ | 33 | 23 | 731 → 731 | 731 → 731 |
| $1 + 10^{-27}$ | 3 | 3 | 93 → 93 | 93 → 93 |
| All | 89 | 75 | 2,179 → 2,177 | 2,179 → 2,177 |

Every view passed both exact verifiers, and none made a square lighter or needed a hold.
The views still fail the claim boundary, for two reasons:

- **Most would promote a tier.** On 2026-10-02, for 73 of the 89 the register’s verified
  upper bound was the grid ceiling, because the Kingbird catalogue was reported evidence
  that had never been replayed.
  An exactly verified view there was a rational packing 0.05 to 0.46 below that bound,
  and a drawing would have carried a certificate the register did not.
  At $n = 17$ and $n = 29$ the view lay $10^{-22}$ and $5 \times 10^{-20}$ below the
  certified endpoint the register held, which is the same promotion at smaller scale.
  The grid-ceiling count no longer holds: T-101 (registered 2026-10-06) made Evan
  Daniel’s exact certificates the verified upper bound at 74 Kingbird counts, and on 11
  October none of the 74 records the layer then refused had the grid ceiling as its
  verified bound. The 72 it refuses now are among those 74
  ([the assessment, section 3.2](../../../docs/project/research/research-2026-10-11-evand-regularization-assessment.md#32-the-side-relation-same-or-solved)).
- **The rest would change the side.** For the other 14 the register already verifies the
  reported bound, but a dilated view’s container is $2.9 \times 10^{-31}$ to
  $8.8 \times 10^{-29}$ larger than the printed side and lies above the verified bound,
  and every centre has moved.
  That is not the author’s packing at the certified side.

What it would buy is two squares.
The views’ remaining light faces are structural: 3,873 face a tilted neighbour, 132 face
a hole, and 129 face an offset row, with no slack.
Only one square at $n = 85$ and one at $n = 227$ compact, by 0.37 and 0.29. Every other
move snaps shut a gap the dilation itself opened.
The flag stays in the tool as the instrument that measured this.
A view framed by it is a scratch artifact and never part of the layer.

## What the drawings are drawn from

The pipeline has four separate layers:

1. exact canonical grids, attributed Kingbird-derived numerical facts, source packets’
   derived facts, or retained UnitSquare SVG renderings;
2. normalized [`Witness/v2`](../../witnesses/witness.schema.yaml) geometry;
3. numerical or exact feasibility receipts at the assurance the source supports; and
4. deterministic SVGs under [`rendering/`](rendering/).

Chunk decompositions do not belong in the source witness.
They live in separate, regenerable annotation artifacts with their detector version,
deterministic objective, tolerances, and limitations.
The current annotations are explicitly calibration-only because the 1–100 corpus was
inspected during their design.
This prevents a taxonomy invented from the corpus from being counted as independent
confirmation on the same corpus.

[`chunk-components.json`](chunk-components.json) is the exploratory layer that tests the
assembly intuition without crossing that boundary.
At the registered `1e-6`-radian angle and `1e-3` contact tolerances, 1,782 of 1,860
squares in the 36 non-grid records belong to a multi-square same-angle contact
component.
Twenty-five of those 36 records use no more than six such components and three
singletons. This is strong evidence for a broad **contact-assembly** description.
It is not yet evidence that every component is one of the enumerator’s narrower bar, L,
or rectangle skeletons.

The 36 non-grid records contain 169 multi-square components: 55 contact chains and 114
cyclic patches. Contact-normal equalities alone leave 859 internal slide degrees before
overlap intervals or wall contacts are applied, and 792 squares are wall-seated at the
registered contact tolerance.
A connected contact assembly is therefore not automatically a rigid chunk; the next
grammar must retain and price those slides.

The retained maximal-lattice detector establishes that stricter decomposition directly
for only 21 of 100 records.
Its other 79 results are recorded as `not-established`, not as failures: a maximal
polyomino may split into two allowed chunks.

[`chunk-partitions.json`](chunk-partitions.json) performs that split with a bounded,
deterministic exact-cover search over contiguous bars, filled rectangles, and corner Ls.
It certifies all 64 grid-derived records and 3 of 36 non-grid records inside the
six-chunk/two-free budget.
Two non-grid cases are conclusively outside that budget, 23 have no partition in this
candidate universe, and eight are search-capped and therefore indeterminate after the
declared 10,000-state limit.
The broad contact result and the narrow partition result therefore point in the same
direction: same-angle assembly is common, but rigid integer-lattice chunks are too
narrow as the only grammar for the interesting records.

The partition atlas evaluates every allowed exact free-square count, prefers an
in-budget certificate when one exists, then minimizes free squares before chunk count.
If an earlier free-count slice is capped, a later in-budget certificate still proves
existence, but the retained selection marks its free-square and chunk minimality as
indeterminate. A later out-of-budget certificate leaves both budget membership and
`F`/`C` minimality indeterminate; likewise, any later capped slice leaves an earlier
out-of-budget certificate indeterminate.
The atlas reports exact and near bands separately and types state-cap and
candidate-universe limitations.
It is calibration evidence only and emits no H-044 verdict.
The contrast is useful rather than embarrassing.
It says the corpus supports the chunk intuition while the current grammar and detector
do not yet support the proposed coverage claim.

[`chunk-evidence-profile.json`](chunk-evidence-profile.json) condenses the full non-grid
census into 36 source-stratified rows.
Its [`house-rendered overview`](evidence/non-grid-chunk-evidence-profile.svg) shows
contact coverage, component count, free squares, largest component, internal slide
degrees, the narrow partition disposition, and the broad-budget flag for every case.
Ten cases are fully covered, 27 cover at least 90 percent, 33 cover at least 75 percent,
and 35 cover at least half; $n = 5$ is the lone zero-contact outlier.
Orange row outlines identify the only registered-to-regularized changes ($n = 68$, $69$,
and $71$) instead of hiding tolerance sensitivity in an aggregate.

[`contact-assembly-grammar.yaml`](contact-assembly-grammar.yaml) records the proposed
revision as a versioned, schema-checked draft.
It keeps rigid lattice chunks as a strict subgrammar and adds contact scaffolds whose
tangential slides remain LP variables.
Its complexity tuple charges free squares, assemblies, internal slide degrees, angle
classes, mandatory contacts, and largest assembly size.
No scalar budget is frozen yet.

[`contact-enumeration-pricing.json`](contact-enumeration-pricing.json) prices the first
target-free implementation without reading atlas geometry.
Exact connected labeled counts grow from 15,104 at size 4 to 9,684,224 at size 5. The
exhaustive size-4 control reduces to 124 canonical labels and local LP solves; 26 pass
the local equations, which accept one fitted-angle class only and still omit walls,
non-edge separation, and container fit.
Mixed angle classes fail before an LP solve.
The isomorph-free size-5 path reduces 1,533,696 topology colorings to 11,013 exact
orbits. Those abstract representatives are retained without geometry or local LP
outcomes; the earlier 9,296,855,040-image raw path remains only a differential oracle.

[`contact-full-cell-control.json`](contact-full-cell-control.json) is a separate
literal, source-free structural control for CG-010. Its three-square axis-aligned L has
eight available non-edge axis-and-order branches; the retained fixture selects one raw
cell, checks all 48 D4-by-relabeling images, emits one canonical label, and performs
zero LP solves. The artifact validates representation, canonicalization, typed caps, and
work accounting only.
It contains no centres, side, geometry, container-fit result, packing feasibility claim,
or optimality claim.

[`contact-overlays.json`](contact-overlays.json) indexes five deterministic visual
strata from the registered descriptive census: $n = 11$, $28$, $40$, $68$, and $89$.
Every SVG under [`contact-overlays/`](contact-overlays/) uses the same house renderer as
the base atlas. Dashed orange lines join square centres or a centre to a seated wall;
they show tolerance-qualified graph incidence, not exact physical contact loci or
rigidity. The numerical overlay feature is deliberately distinct from the renderer’s
certified exact-contact feature, and the gallery remains calibration-only.

## Coverage Policy

Exact integer records use a canonical row-major subset of the corresponding grid.
Noninteger catalogue records use attributed Kingbird-derived numerical center and angle
facts retained in Witness/v2; the upstream SVGs are not retained in this source
inventory because the review located no express redistribution terms.
This is a conservative retention policy, not a legal conclusion.
The newer public UnitSquare renderings superseded the older Kingbird geometry at
$n = 68, 69, 103, 105, 110$ and $131$; their six-decimal polygon coordinates are
explicitly recorded as rendering-derived numerical evidence, not as the unavailable
interval boxes named in their metadata.
None draws one now: Couzo’s packings supersede five of them, and $n = 69$ moved on
2026-10-05 to the catalogue’s later side for the same packing, David Ellsworth’s
optimization (T-088).

At $n = 69, 83$ and $87$ the catalogue facts are not read from the SVG itself, which the
session that took in their September 2026 sides could not fetch, but from Evan Daniel’s
binary64 parse of it, pinned at a commit of `evand/square-packing`; each witness names
that file in `source.revision` and says so in its limitations.
`devtools.derive_kingbird_facts --compare-parse` measures that parse against this
repository’s own: at the 90 counts whose witnesses were read from their own pictures,
every side agrees and every pose agrees to one binary64 ulp.
Before the three were taken in it also compared $n = 83$ and $87$, whose retained
witnesses still described the pictures the catalogue had replaced, and those two were
the only ones that differed.

At 50 counts the drawing is a parallel project’s packing, read from its source packet’s
derived facts: Francisco Couzo’s at 49 counts from $n = 68$ to $307$ (T-056), seven of
them, $n = 208, 209, 228, 263, 272, 303$ and $306$, from his revision of 3 October 2026
(T-092), and Joost de Winter’s at $n = 211$ (T-057), the first drawing of 211 squares
that is not the grid.
Neither source publishes a licence, so the packets keep the centres and angles and the
upstream digests, never the files, as for Kingbird.
Each of these packings is also certified exactly here, which the case record carries in
its verified lane; the atlas witness itself stays the numerical one.

Every witness limits its claim to feasibility of the retained construction.
The phrase “known best” comes from the frontier register and never turns a numerical
witness into an optimality proof.

## Rebuild

From `packing`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.build_known_best_atlas --check
uv run --frozen --all-extras --group dev python -m devtools.census_known_best_chunks --check
uv run --frozen python -m devtools.render_known_best_contact_overlays --check
uv run --frozen python -m devtools.profile_known_best_chunks --check
uv run --frozen python -m devtools.price_contact_enumeration --check
```

Source acquisition is an explicit network operation and is not part of CI:

```bash
uv run --frozen --all-extras --group dev python -m devtools.build_known_best_atlas --fetch
uv run --frozen --all-extras --group dev python -m devtools.build_known_best_atlas --update
```

The first command acquires only missing UnitSquare assets unless `--refresh` is
requested; Kingbird live audits are ephemeral and write no geometry.
The second rebuilds witnesses, individual house renderings, the manifest, and frontier
witness links from retained inputs.
For a layout change, `--update-composite-records` refreshes only the composite geometry
in the manifest and figure record, refusing changes to case facts or legend totals.
Commit those data records and re-pin the release before redrawing the composites.
The two composites and their exports are drawn apart, by `--update-composites`, at a
version bump or on demand; each states the data commit it was drawn from, and
`--check-composites` holds it to that statement without rebuilding anything
([the figure playbook](figure-playbook.md#rebuild-it)). `--report` measures what those
exports cost — bytes, square polygons, bytes per square, and how each composite encodes
a square — without rebuilding anything.
Rasters are drawn by cairosvg, the same renderer that draws the PDFs, so every export of
one drawing agrees; check mode reads the embedded source-SVG receipt without invoking a
renderer at all. Git remains the integrity boundary for co-committed outputs.
Upstream asset integrity uses only hashes declared independently by a source; the PNG’s
local source-SVG receipt tracks derivation and is not source evidence.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
