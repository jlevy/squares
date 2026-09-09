# Plan: A Video of Every Known-Best Packing, `n = 1..324`

**Date:** 2026-09-07

**Author:** Joshua Levy, with Claude Fable 5.1 assistance

**Status:** Draft, owner-directed; the open questions below await the owner.
Epic `think-hsdj` is created by this plan.
It runs beside the atlas expansion (`think-0juv`,
[session-099](../../../../packing/campaign/agent-sessions/session-099-atlas-expansion-to-324.md),
PR 111), whose poster and per-`n` renderings it consumes, and it does not preempt the
research selection in the [current handoff](../../../../SYNOPSIS.md#current-handoff).
Two spikes ran under the `coding-spike` shortcut as Phase 0; their findings are folded
into this document below.

**Workflow:** W7 pipeline-improvement throughout, with a W8 documentation pass closing
the last phase.

**Owns:** The design of the two videos, the player that draws them, the frame and
transition records the player reads, the capture tool, the receipts the captures carry,
their validation, and where the videos are published.

**Does not own:** The per-`n` renderings and the poster, which the
[expansion plan](plan-2026-09-07-atlas-expansion-to-324.md) and the
[figure playbook](../../../../packing/atlas/known-best/FIGURE-PLAYBOOK.md) own; the
colour contract, which `sqpack/render/color.py` and its tests own; the safe SVG profile,
which the
[rendering toolkit plan](plan-2026-08-24-deterministic-svg-rendering-toolkit.md) owns;
the page’s design system, which the vendored kpress owns; any claim about a packing,
which stays with the frontier register; and, from 2026-09-08, the solver workbench Phase
0 grew — the force law, the relationship graph, growth, the annealing dial, hand editing
and the unbuilt Calibrate mode — which belongs to
[`X-025`](../../../../packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md).

## Overview

The atlas holds a house rendering and a typed record for every known-best packing from
`n = 1` to `324`, and the poster shows all of them at once.
What it does not have is a way to watch them in sequence.

This plan builds that in two versions from one player.
**Version 1** is a slideshow: each packing at full size with its card facts set as
readable text, fading to the next.
**Version 2** animates the step from `n` to `n + 1`: the squares that stay slide and
turn to their new poses, the one that arrives fades in, and fills cross-fade as
orientations change.
Both are HTML documents whose every frame is a pure function of a virtual clock, so a
headless browser can be asked for the frame at any instant and a video encoder can be
handed the frames in order.
The video files are not committed; they are captured from the committed player under a
receipt and published beside the poster.

Two rules from elsewhere in the repository govern the design.
The figure playbook’s rule that a figure reports what is known about the packing, never
how the repository stores it, decides what the facts panel may say.
The rendering toolkit’s rule that animation does not grant validity to intermediate
frames decides how Version 2 labels itself: a tween between two packings is a picture of
neither, and the player and the video say so.

## Goals

- A self-contained, byte-reproducible player under `packing/atlas/known-best/video/`
  that draws all 324 packings from the same records the poster reads, in a slideshow
  mode and a transition mode, with a deterministic `seek` clock.
- A frame record and a transition record with schemas, built by devtools from the
  witnesses, the renderings, and `composite-figure.json`, and checked on the
  pull-request surface.
- A capture tool that renders frames through the pinned Playwright headless shell and
  encodes them with ffmpeg, writes a receipt naming everything the frames depended on,
  and records its own per-frame cost.
- The first Version 1 video and the first Version 2 video, published as release assets
  and linked from the atlas README and the site, with receipts.
- Validation that stays fast: regeneration checks, schema checks, a bijection test over
  every consecutive pair, a stand-in capture of a few frames, and a size budget on the
  pull-request surface; the full capture off it, under OR-13.

## Non-Goals

- No change to the publication renderer, the safe SVG profile, or `validate_safe_tree`.
  The player is an HTML profile beside the renderer, as the motion lab is.
- No claim that any intermediate frame of Version 2 is a packing.
  The tween is illustrative and labelled as such; no feasibility check runs on it and
  none is implied.
- No new colour contract for the atlas.
  Whatever the video does between frames, the frame at each integer `n` carries the
  fills the retained rendering carries.
- No committed video bytes.
  The repository already refuses to serve a 1.2 MiB raster for resolution nothing
  displays; a multi-megabyte MP4 in Git is the same mistake with a larger number.
- No audio, no interactive editing, no scrubbing of packings that are not in the record,
  and nothing above `n = 324`.
- No third top-level tree.
  Code under `packing/src` and `packing/devtools`, records and the player under
  `packing/atlas/known-best/video/`, prose at the root.

## Background

### What exists

| Layer | What is there | Where |
| --- | --- | --- |
| Per-`n` renderings | 324 SVGs, `960 × 680`, the packing in a `536 × 536` box at `(36, 36)`; two `<polygon>` per square with explicit corners, `fill`, `data-square`, `data-hue-index`, `data-shade-index`, `data-orientation-radians`, `data-angle-class`, `data-contact-sides`; one caption in `system-ui`; 51 MB in total, 330 KB for `n = 324` | `packing/atlas/known-best/rendering/n-NNN.svg` |
| Card facts | one entry per `n`: `side`, `lower`, `badges`, `exactness`, `optimality`, `rigidity`, each with provenance; the poster draws only from this record | `packing/atlas/known-best/composite-figure.json` |
| Geometry | `Witness/v2`: 141 `center-angle` records (centre and angle in degrees as decimal strings, up to 100 digits) and 183 `corners` records (177 exact grids, 6 UnitSquare) with no angle field; ids `1..n` positional; witness `k` is `square-{k:03d}` in the rendering | `packing/witnesses/known-best/` |
| Poster | `known-best-1-324.svg`, 6,198,351 bytes at 117.7 bytes per square after three measured levers; Helvetica; PNG and PDF with source-digest receipts | `packing/atlas/known-best/` |
| Motion precedent | the `n = 5` motion lab: a generator in `devtools/`, shared assets under `src/sqpack/motion_lab/assets/`, a retained self-contained HTML under `atlas/rendering/` with a strict CSP, `requestAnimationFrame` driving a range input, byte-checked by `--check` and a Node-executed model test | `packing/devtools/render_packing_motion_lab.py` |
| Browser | `playwright==1.62.0`, whose wheel pins Chromium revision 1234 (`151.0.7922.34`) and the headless shell the PDF exporter launches; `chromium_headless_shell-1234` is in the host cache and the pages workflow installs it with `--only-shell` | `packing/pyproject.toml`, `.github/workflows/pages.yml` |
| Encoders | host `ffmpeg` 7.1.1 at `/opt/homebrew/bin/ffmpeg` with `libx264`, `libvpx-vp9`, `libaom-av1`; Playwright’s bundled `ffmpeg-1011` (`n7.0.1`) carries `libvpx` VP8 only | host; `~/Library/Caches/ms-playwright/ffmpeg-1011` |
| Fonts | PT Serif in four faces and Source Sans 3 in two variable faces, 183 KB of woff2 together, inlined as data URIs by `render_explainer.kpress_css`; the math text face with the italic `s` and the function-name kern from the [math text face plan](plan-2026-09-07-math-text-face.md) | `vendor/kpress/src/kpress/format/static/fonts/` |
| Site | `packing/site/` is gitignored, built by `render_explainer`, deployed by `pages.yml`; the poster’s SVG, PNG and PDF are served beside the page; the `@2x` raster is deliberately not | `packing/devtools/render_explainer.py`, `COMPOSITE_ASSETS` |
| Receipts | every PNG and PDF carries the sha256 of the one SVG it was drawn from; the PDF uses a receipt rather than a byte comparison because cairo’s font-subset tags differ per process | playbook, “Staleness cannot pass quietly” |

### What a video needs that the renderings do not give

The renderings cannot simply be concatenated into one page: 51 MB of SVG in a document
that must stay self-contained is out of the question, and the poster already found the
encoding that fits, at under 200 bytes per square with three-decimal coordinates and no
per-square data attributes.
The player therefore reads a compact per-square pose record built for it, and the record
declares the precision it was rounded to, as the poster’s profile block does.

The per-`n` caption reads `n=147 known best: side ~ 12.65685425 (numerically checked)`
in `system-ui`. The poster’s card reads `147`, a badge row, `s(147) ≤ 12.656854`,
`deg 2`, and `s(147) ≥ 12.135528`, in Helvetica at 14 to 29 units.
The owner asked for the same information in a more readable fashion, which means the
poster’s facts set at a size a viewer can read from a video, with the badges spelled
out.

### The correspondence problem

Square ids are positional and mean nothing across `n`. Over the 323 consecutive pairs,
measured from the witness pose tuples:

| Relation between `n` and `n + 1` | Pairs |
| --- | ---: |
| `n`’s poses are an exact prefix of `n + 1`’s (every grid-to-grid pair) | 160 |
| `n`’s poses are `n + 1`’s with one square removed (the five shared-picture pairs: 147→148, 232→233, 264→265, 290→291, 295→296) | 5 |
| no pose in common; a correspondence has to be chosen | 158 |

Grid cases are numbered row-major from the lower left, so appending square `n + 1`
extends the prefix. A shared-picture case is the catalogue’s own rule that a smaller
count is the pictured packing with any square removed;
`derive_kingbird_facts.subpacking_poses` drops the square whose centre sorts last, and
the retained `n = 147` is exactly `n = 148` with index 21 removed.
The remaining 158 pairs are the interesting ones: the packings are different
constructions, and any correspondence between them is a choice the record has to state.

### Colour is not a function of angle

Hue comes from the angle class, and classes take hues by descending size from slot 2
upward, wrapping modulo 18 once a frame has more than twenty classes (`n = 273` has
106). Right angles are pinned to teal and 45-degree tilts to citron; everything else can
change hue between `n` and `n + 1` without moving, because the size ordering changed.
Shade comes from the count of full-side contacts.
So “the square changes colour as it rotates” is not what the house rule says; the house
rule says the square’s class changed.
A video that wants a continuous colour in angle has to invent one, and a video that
keeps the house fills has to accept that some squares cross-fade to a new hue while
standing still. `AngleHueRegistry` in `color.py` already keeps hues stable across the
panels of one comparison render and could do the same across the sequence, at the cost
of making the integer frames differ from the retained renderings.

### The honesty rule already held

The rendering toolkit plan refuses to draw rotation as translation, does not invent
frames, and requires an `illustrative` interpolation to say in visible text and metadata
that intermediate poses are unverified and may overlap; its testing section adds that
animation does not grant validity to intermediate frames.
The motion lab plan labels any frame that is not a retained solver evaluation an
`illustrative tween`. Version 2 inherits both.

### What the toolkit offers a relaxed tween

The owner asked whether a physics-like model could carry a step through a relaxed
intermediate, and whether the repository’s own research says which optimisation models
work best below 100. The record answers both.

- There is no physics integrator in the repository.
  The quench in `sqpack.research.quench` is a fixed-angle linear programme inside a
  separation cell with a golden-section search over merged angle classes, a polisher
  within the basin a configuration is already in, and the synopsis says that is all it
  does; the Rust `sqsearch` annealer minimises the required side plus a linear overlap
  penalty under a cooling schedule, in floating point, and may not claim a record.
  The interactive free-quench lab drives that quench for at most twenty squares from a
  seeded random start and has no witness import.
  *Overtaken 2026-09-08:* there is an integrator now, and Phase 0 wrote it.
  The Version 2 prototype carries a fixed-timestep contact solver with an editable force
  law, and it is a solver workbench rather than a video component; the section below on
  what Phase 0 became records the split, and what the integrator measured is why `D11`
  no longer investigates a relaxed intermediate.
- No packing in the corpus has container slack: the translation-escape screen’s
  `min_container_slack` is zero or below in all 318 screened records, and what play
  exists is tangential sliding of 5,323 squares in 296 records.
  A relaxed state therefore has to be constructed, by inflation, not found.
- A float feasibility check is meaningful only with positive gaps:
  `verify_packing(corners_from_poses(x, y, theta), side, float_sign(1e-9))` in
  `sqpack.verify` is the call the motion lab’s tests already make, and its own docstring
  says why it cannot decide a tight packing.
  `promote/relax.py` makes the same argument from the other side, opening every contact
  by `eps` to certify an upper bound.
- Two registered hypotheses describe the idea and are unbuilt: `H-013`, a fixed-side
  projection family from an inflated container toward the target side, which notes the
  side-minimising quench is not that operator; and `H-004`, seeding `n ± 1` from a
  neighbour’s packing.
  `H-018` measured that perturbing Trump’s `n = 11` by `1e-3` returned to it in zero of
  forty trials, so a tween that relied on a refiner finding the endpoint would not work;
  the tween has both endpoints and needs no refiner.
- Below 100 the records are 52 trivial grids, 25 hand constructions, 10 simulated
  annealing, 6 diagonal strips, 3 extensions and 4 unrecorded; above 100, 113 grids, 30
  annealing, 27 extensions, 10 strips, 8 hand, 3 compositions and 33 unrecorded.
  The algorithms research records that the dominant mode at large `n` is construct, then
  locally optimise, that annealing credits are all for `n` between 28 and 307, and that
  general-purpose global optimisation at `n = 27` returns a much worse arrangement.
  For the video this means the physics-like model is a path between two given packings,
  never a search, and it must not be presented as one.

### Spike findings

Both spikes ran on 2026-09-07 under the `coding-spike` shortcut, each in a directory of
the session scratchpad outside the repository, and neither touched the worktree.
Those directories do not outlive the session, so the dispositions below name what Phase
1 and Phase 3 re-implement rather than what they copy.
The coordinator measured the Version 1 candidate independently with the repository’s
pinned Playwright (`playwright==1.62.0`, `chromium_headless_shell-1234`, Chromium
151.0.7922.34); those figures are marked as the coordinator’s.

#### Version 1: the slideshow (`think-5oba`)

**Built.** A deterministic generator (about 2.5 s to run; three builds in one session
byte-identical) reads `composite-figure.json`, `manifest.json`, the 324 frontier records
and the 324 renderings and writes one self-contained page under a
`default-src 'none'; font-src data:` policy.
Its smoke test builds twice into temporary directories and asserts byte identity with
the shipped page, checks 324 slides each with `n` four-corner polygons and `n` fill
digits, finds no `http` outside the record’s 324 source URLs and none of `fetch(`,
`XMLHttpRequest`, `import(`, `innerHTML`, `eval(`, `Date.now`, `Math.random` or
`setInterval`, and runs the page’s own script through a Node stub-DOM harness of 20
timeline checks. The spike opened no browser.

**Bytes.** 3,594,925 bytes for 52,650 squares, about 68 bytes per square: 2,688,572 of
geometry, 441,318 of facts templates (324 `<template>` blocks), 281,977 of base64 font
CSS (209,660 raw), 9,642 of script, and about 173 KB of markup and JSON framing.
Each square is its fill polygon’s four corners re-based from the `960 × 680` canvas to
the 536-unit box at two decimals with trailing zeros stripped, and its fill as one
base-36 digit into a sorted 34-fill palette; the outlines are one `stroke` on the group
and the container one `<rect>`, as the poster does, and all 324 container rects were
asserted at `(36, 36)`, `536 × 536`. Three decimals cost 3,938,704 bytes, one decimal
3,245,791. Two decimals of 536 units are 0.016 px on the spike’s 880 px picture and
0.033 px at 4K.

**Fonts.** The PT Serif and Source Sans 3 latin subsets carry none of ≤, ≥, √ or ≈ (216
and 231 glyphs by fontTools; minus and × are present).
The spike declared `KaTeX_Main-Regular.woff2` (26,272 bytes) as a seventh family
restricted by `unicode-range` to `U+2208, U+221A, U+2248, U+2264-2265, U+2308-230B`,
placed after PT Serif and Source Sans in both stacks with `size-adjust: 102.5%`, the
value kpress measured for that slot of its math text face; the composition is the one
`katex-text-face.css` already uses.
Radicals are drawn, not typed: KaTeX’s `sqrtMain` path in an SVG behind the radicand,
with paddings computed from PT Serif’s metrics and a tall variant for the four nested
`√(1 + √2)` forms; `--radical text` prints `7 + 4√2` instead.
The italic `s` carries a 0.055 em kern in CSS, the poster’s `SUMMARY_ITALIC_KERN`. None
of the typography was judged by eye.

**Panel.** Fixed slots so the layout does not jump between `n`: kicker, the numeral
`n = 147`, three line slots (side, exact form, lower bound) kept even when empty, a
four-row status block, then a record block last.
From `composite-figure.json`, entry by entry: `side.display` and `side.relation`;
`exactness.exact_form` parsed by a small grammar and evaluated against `side.value` to
`1e-9` as a build assertion, with the minimal polynomial instead for the 36 cases that
have no closed form; the degree when at least 2; `lower.display` when shown, in the
accent when `first_proved_here`; each badge’s `meaning` and `style` as a filled or
outlined mark. Two additions the card does not make: “optimality open” and a “proved
lower bound” note. Beyond the card the spike read a record block straight from the
frontier records and the manifest: construction method, found by and year (114 cases),
improved by (20), the lower bound’s prover, year and kind for open cases, and the source
key and URL. That is the second reader of the register that `D3` and `D4` rule out, and
it showed why the route through the composite builder matters: `n = 11`’s `proved_by` is
the string “repository exact H-041 certificate”, which the row prints literally.

**Timeline and API.** Slot = dwell + fade; slide `k` owns `[k · slot, (k + 1) · slot)`;
the first slide appears at `t = 0` and the last fades to paper, with no cards.
At the spike’s default 2.0 s dwell and 0.6 s fade the run is `324 × 2.6 s = 842.4 s`.
The dissolve is smoothstep in opacity with the outgoing layer opaque underneath, so the
paper never shows through; a 2 % scale settle with a cubic ease-out is applied to the
incoming picture, on by default with a toggle, and the spike recorded its own
reservation that a 2 % breath on the one element stable across 323 transitions may read
as a pulse. `window.atlasVideo` exposes `seek`, `frameAt(index, fps)`, `duration`,
`setTiming`, `stateAt(t)` returning `{n, next, progress, phase}`, and `ready`; nothing
reads `Date.now` or `Math.random`, and the harness seeks `100 → 5 → 500 → 100` and
checks the two layers’ contents match.
The current facts are mirrored into an `aria-live` region past each fade’s midpoint.

**The coordinator’s measurements** on the candidate: page load 0.18 s;
`atlasVideo.duration()` 842.4 s. A `seek` plus PNG screenshot at `1920 × 1080` and
device scale factor 1 costs about 42 ms for a dwell frame and 53 ms mid-fade, 139,871
bytes per frame; at device scale factor 2 (`3840 × 2160`) about 145 ms and 167 ms,
297,175 bytes. Six captures of the same instant were byte-identical at both sizes, and
two instants inside one dwell produced identical bytes, which is what the `stateKey`
deduplication in `D8` relies on.
At 30 fps the default timing indexes 25,272 frames; deduplication leaves one screenshot
per dwell and 18 per fade, 6,138 in all, about 320 s of capture at 1080p and about 1,020
s at 4K in one process at the measured rates, against about 1,140 s for all 25,272 at
1080p without it.

**Defect.** The facts panel cross-dissolves as a whole with the picture, so mid-fade the
numerals 147 and 148 overlap and ghost, and the lower-bound digits smear.
The picture’s own dissolve reads well.
The panel text has to cut at the fade midpoint or fade out and then in, never overlap;
`D4` now says so and Phase 1 carries it.

**Disposition.** Phase 1 re-implements, as the spec’s devtools and tests: the
deterministic generator with its byte-identity, self-containment and CSP checks; the
seven-face composition with the `unicode-range` subset (`D5`); the fixed-slot panel from
`composite-figure.json` with the exact-form build assertion; the drawn radicals, if the
owner keeps the exact-form line; the `seek`, `frameAt`, `duration` and `setTiming` API,
`stateAt` as the seed of `stateKey`, and the Node harness as the model test.
Kept as reference and not promoted: the four-corner encoding (the pose record of `D3` is
about half the bytes, and it is what Version 2 needs); the record block read from the
frontier (the `discovery` block goes through `build_composite_figure_data` with
provenance or not at all, the owner’s call under `D4`); the settle, which the design
does not include, unless the owner asks for it after seeing the plain dissolve; and the
whole-panel dissolve.
Questions the spike asked that the spec already answers: opening and closing cards
(`D4`), reduced motion (`D7`), and hue flips between similar packings on consecutive
dissolves, which the non-goals settle by keeping the retained fills at every integer
frame.

#### Version 2: the transitions (`think-l78w`)

**Built.** A deterministic generator (about 7 s to run; two runs identical) reads the
324 witnesses and renderings, classifies and matches all 323 pairs, and writes a 24-pair
review page of 327,176 bytes, an all-pairs page of 2,077,600 bytes,
`transition-stats.json` with every correspondence map, and `stats-summary.md`. Its test
checks byte-identical regeneration, the bijection of every correspondence, recognition
of the 5 shared-picture pairs and all 160 grid pairs, and no network reference.
The all-pairs page carries each of the 52,650 squares as `[x, y, angle, fill, contacts]`
at 6/6/4 decimals with three PT Serif faces and one Source Sans 3 face inlined (169,013
bytes), about 36 bytes per square of geometry, which is the frame record’s estimate; it
loads in 0.13 s in the headless shell and keeps one pair’s DOM at a time (at most 325
`<g><rect>`), so render cost does not depend on how many pairs are embedded.
Each square is a unit `<rect>` under `translate(x y) rotate(deg)` in a world group
flipped by `scale(1 -1)`, so the witnesses’ y-up coordinates are used as they are; the
container rect and the viewBox interpolate with the squares’ own ease-in-out, the
viewBox always `s × 1.09` centred on the container, so the container holds a constant
screen size as in the atlas.
The panel sets `s(n)` in PT Serif with the italic `s`.

**Correspondence.** As `D10` specifies: exact prefix for the 160 grid-to-grid pairs (the
first `n` poses of `n + 1` are byte-identical to `n`’s), the manifest’s recorded removal
for the 5 shared-picture pairs (checked to be `n + 1` with exactly one square removed,
order preserved), and `scipy.optimize.linear_sum_assignment` (scipy 1.17.1) on an
`n × (n + 1)` matrix for the 158, with the leftover column as the new square.
The cost is the squared centre distance in coordinates normalised by the larger of the
pair’s two sides, plus `ANGLE_WEIGHT × (Δθ / 45°)² / side²` for the shortest turn modulo
90°. The spike’s first cut used weight 0.25, which is what this document’s earlier read
of `stats-summary.md` reported; its final page uses weight 1.0, on the sweep below.

Statistics at weight 1, from `transition-stats.json`, displacement in unit-square units
in the witnesses’ own coordinates so that a square which keeps its pose while the
container grows has displacement 0:

| Kind | Pairs | Mean of the maximum displacement | Largest maximum | Pairs with any rotation | Pairs with a close pass |
| --- | ---: | ---: | ---: | ---: | ---: |
| prefix | 160 | 0 | 0 | 0 | 0 |
| shared-picture | 5 | 0 | 0 | 0 | 0 |
| assignment | 158 | 0.998 | 1.657 | 156 | 5 |

Over all 323 pairs the maximum displacement is exactly 0 in 165, in `(0, 0.5)` in 3, in
`[0.5, 1)` in 81 and in `[1, 2)` in 74; none reaches 2. Over the 158 assigned pairs the
median mean displacement is 0.35 units, the median maximum 0.98, and the median fraction
of squares that turn (by more than 0.05°) is 37 %. The largest single displacement is
65→66 at 1.66 units; the largest rotation count is 260→261, where 159 of 260 squares
turn. A close pass is two squares, at least one moving, whose linearly interpolated
centres come within 0.7 units at one of 21 sampled instants; five pairs have one each
(65→66, 82→83, 145→146, 149→150, 261→262, at 0.61 to 0.69 units) and the rest have none,
since the straight-line trajectories of a squared-distance assignment never collide
unless the angle term breaks them.

The angle-weight sweep over the 158 assigned pairs:

| Weight | Mean of max displacement | Largest maximum | Squares moving over 1 unit | Squares turning | Total turn, degrees | Pairs with a close pass | 4→5 keeps its corners |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 0.956 | 1.422 | 282 | 9,162 | 255,084 | 0 | no |
| 0.25 | 0.956 | 1.422 | 277 | 9,143 | 254,004 | 0 | no |
| 0.5 | 0.964 | 1.422 | 273 | 9,128 | 253,116 | 0 | no |
| 1 | 0.998 | 1.657 | 277 | 9,078 | 250,304 | 5 | yes |
| 2 | 1.075 | 1.832 | 339 | 9,010 | 246,032 | 21 | yes |
| 4 | 1.206 | 2.335 | 540 | 8,890 | 238,757 | 48 | yes |
| 8 | 1.602 | 3.705 | 1,231 | 8,636 | 222,327 | 72 | yes |

Rotation is forced by the change in tilt census between frames, not chosen by the
weight: at weight 8 the total turn falls by 13 %. The weight decides marginal cases, and
the first is the one that matters: below 1 the matching sends a corner square of the
`2 × 2` to the centre of `n = 5` and lets the new square appear in a corner.
Weight 1 keeps the corners as corners at the cost of the five close passes; above 1 the
slides lengthen and the close passes multiply.

**What the motion looks like.** No transition is a long-range rearrangement; what
differs between pairs is how many squares are involved and how much they turn.
The 158 assigned pairs fall into three kinds.
Local settle, 126 pairs: mean displacement mostly under 0.45, nothing beyond about 1.2
units, a third of the squares turning a few degrees (129→130 at maximum 0.48 and mean
0.05; 272→273 is the rotation-only extreme, mean 0.06 with 101 squares turning up to
28°). Block rotation, the 16 grid-to-derived pairs that leave a perfect square (4→5,
9→10, 16→17, 25→26, 36→37, 49→50, 64→65, 81→82, 100→101, 121→122, 144→145, 169→170,
196→197, 225→226, 256→257, 289→290): the grid holds and a central block turns 45° as a
unit while the container grows by 0.54 to 0.71; 100→101 turns 25 squares and moves 67 by
more than half a unit but none by more than 0.97; these read well.
Collapse into the grid, the 16 derived-to-grid pairs that land on an integer side (5→6,
11→12, 19→20, 29→30, 41→42, 55→56, 71→72, 89→90, 110→111, 132→133, 156→157, 182→183,
210→211, 241→242, 273→274, 307→308): from 110→111 on, mean displacement about 0.6, 9 to
23 squares moving more than a unit and 46 to 105 turning at once.
The pair that reads worst is 110→111, a derived packing collapsing into the `11 × 11`
grid with 46 rotations and 12 squares moving more than a unit, where the assignment
turns the tilted rows into a conveyor of one-unit hops rather than a block turning back;
307→308 moves 23. The spike’s proposed fixes, in its order: cluster-level matching
(cluster each frame by angle class and full-side-contact adjacency, both of which the
atlas already computes; match clusters by centroid and size, then squares within matched
clusters, so a block rotates rigidly about its centroid); two-stage moves, rotate-first
or slide-first, which its page already offers beside simultaneous; a 2-opt swap of the
two assignments of any crossing pair when the swap barely raises the cost; staggered
start times; and a narrative rule for which square is new, since the leftover column is
decided by cost residue.
An exact 45° tie is resolved counter-clockwise, and a block whose members are matched to
`+44.9°` and `−45°` spins in both directions, which cluster matching would also cure.

**Colour.** Both rules are built and the spike shipped the continuous-angle rule as its
default. Under the house fills (cross-faded in OkLab during the move, where `D11` says
OkLCh) the assignment is class-based and re-ranked per frame, and at 260→261 a
sub-degree turn moves the central block from the pinned citron to a ranked hue: it
cross-fades from citron to salmon while barely moving, and across a sequence that reads
as flicker without a geometric cause.
The continuous rule makes fill a function of tilt modulo 90° and the frame’s full-side
contact count: a piecewise-linear OkLCh hue path, teal (house slot 0, hue 174.6°) at 0°,
citron (slot 1, hue 109.4°) at 45°, then the long way round the hue circle from 45° back
to teal at 90°, with lightness and chroma along the house’s own shade ramps and chroma
clipped to sRGB by bisection; at 0° and 45° the fills are exactly the house families, so
every grid frame looks as it does in the atlas.
Its cost is that two classes at nearby angles (20° and 22°) are no longer
distinguishable, which the house rule guarantees, and that mirror tilts (20° and 70°)
get different colours on the long arc.
`D11` carries the evidence and keeps the owner’s question.

**Timing.** Dwell 1.2 s, move 1.6 s, settle 0.5 s per pair; 323 × 3.3 s plus a closing
dwell is 1,067.1 s, 17.8 minutes, at uniform timing.
165 of the 323 pairs are static appends whose 1.6 s move changes nothing except, for
1→2, the container; giving those 0.5 s dwell and 0.4 s settle with no move brings the
run to `158 × 3.3 + 165 × 0.9 + 1.2 = 671 s`, 11.2 minutes.
The new square scales up from 0.35 and fades in over the first 0.45 s of the settle, at
the instant the panel rolls to `n + 1`, where `D11` had it fading in during the last
third of the move; Phase 3 judges the two by eye.
The spike’s questions on the panel’s status line and on showing the source kind are
answered by `D4`, and its question on labelling the tween by `D12`.

**Capture.** The prototype ran first time on what the host already holds: the pinned
Playwright’s `chromium_headless_shell-1234` and `/opt/homebrew/bin/ffmpeg` 7.1.1. It
loads the all-pairs page by `file://` at `1920 × 1080` and device scale factor 1, waits
on `document.fonts.ready`, hides the review chrome, and for each pair seeks `k / fps`
and screenshots. 100 frames of 100→101 took 7.4 s, 74 ms per frame on a page with more
DOM per square than Version 1’s polygons; `libx264 -crf 18 -pix_fmt yuv420p` encoded
them in 3.5 s to a 522 KB MP4 of 3.33 s; the same frame from two independent browser
launches was byte-identical.
Nothing yet compares a host frame with a runner frame, so the pixel standing in `D14` is
unchanged. The full run at 30 fps is 32,013 indexed frames; deduplication collapses only
the dwells, to about 20,700 screenshots, so a transition capture in one process is about
1,530 s at the measured rate plus about 35 ms per frame to encode, and 60 fps doubles
both. The spike captured pair by pair, which maps onto the segments `schedule` lists in
`D7`; frame index to time is a pure function, so ranges split across processes and the
segments join with ffmpeg’s concat demuxer.

**Disposition.** Phase 3 re-implements: the three-method classifier and the bijection
and census tests; the assignment at weight 1 with the sweep kept as a `--review` output;
the statistics per pair in the transition record; the unit-rect transform drawing in a
y-up world group with the interpolated container and viewBox; shortest-arc angles with
the counter-clockwise tie; the continuous-angle rule behind a record flag with its own
label; the motion phase (simultaneous, rotate-first, slide-first) as a timeline
parameter; and the per-pair capture loop as a walk over `schedule`. Phase 3 takes
110→111 as the pair on which two-stage moves and then cluster-level matching are judged
(`D10`). Kept as reference: the 24-pair review page, the correspondence overlay, the
pair selector and auto-advance.
Not promoted: a per-pair clock (`select(i)` then `seek`), since `D7` has one clock over
the whole run; the OkLab cross-fade; and a narrative rule for the new square, which the
record does not need to state and no measurement supports yet.

**Where the spikes and this document disagreed.** The statistics table this document
carried before the notes arrived was the weight-0.25 run (mean of maximum 0.956, largest
1.422 at 110→111, no close pass); the final page is weight 1 and the table above
replaces it. The all-pairs page was reported at 2,076,281 bytes from the first build and
is 2,077,600 in the notes.
Version 1 counts “the trivial grids” as 165 of 324 where the witnesses hold 177 exact
grids; the 165 are the static-append steps (160 prefix and 5 shared-picture), and this
document uses that name.

#### What Phase 0 became, and where its parts now live (2026-09-08)

Phase 0 asked for two spikes and got one spike and one instrument.
The Version 1 candidate stopped where its brief did.
The Version 2 candidate did not: across thirteen revisions it became a solver workbench,
and this plan should name the drift rather than let “the transitions spike” keep
standing for it.

What it grew that no video needs: a contact force law with four editable parameters and
a force-against-gap plot whose control points drag; a relationship graph that masks the
attraction, over every pair, over the blocks, or over the retained packing’s own contact
graph, which can also be drawn by hand on the stage; growth from a reduced starting size
up to unit squares; open-ended optimisation with squares draggable mid-run; an annealing
dial; and three named modes.

Those modes are the shape of the split.
**Pack** is one `n` with a person in the loop.
**Animate** is a range rendered at speed with nobody intervening, and that is this
video. **Calibrate**, unbuilt, sweeps the strategy over cases whose records are known.
The middle mode was called Sweep until 2026-09-08 and is renamed Animate, because
Calibrate is the mode that sweeps — over parameters — and two modes called sweep would
be permanently ambiguous.
[`X-025`](../../../../packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md)
sets out the three axes a mode is a choice on.

**Ownership splits here.** This plan keeps the video artefacts and nothing else: the
frame record and the player (Phase 1), the capture pipeline (Phase 2), the transition
record and the tween (Phase 3), publication (Phase 4). The solver is not one of them.
The force law, the relationship graph, growth, the annealing dial, the hand, Calibrate,
and every research question they raised belong to `X-025` and to the beads under it.
The prototype is one page today and the two owners share it; where they pull apart, the
video’s needs decide what the retained player does and the workbench’s needs decide what
the prototype does.

**Three of Phase 0’s findings are negative, and they are worth keeping.** The research
is recorded in `X-025`; what bears on this plan is folded into `D11` and `D16` below.
Aimed straight at a known answer with the final snap disabled, the settle still rests
one to 1.7 units away per square and 0.1 to 1.1 per cent wide, and run blind it loses
every genuinely packed case, by up to 6.8 per cent at `307 → 308`. So no physics-driven
tween replaces the interpolated one, and the plan’s rule that the frame at every integer
`n` is the retained rendering’s geometry is what keeps Version 2 honest rather than a
convenience.

**And one is positive: the page is not slow.** Measured headless on the prototype, 120
frames per second at both `n = 17` and `n = 272`, worst frame 10 ms, 358 DOM nodes, 10.7
MB heap, and every API call under 2 ms.
Apparent sluggishness during the session coincided with a five-minute load average of
116 caused by another session, not with the page.
Nothing in `D8`’s capture budget or the player’s byte budget needs to be reopened for
draw cost; the capture’s cost is the screenshot, as `D8` already measures it.

## Design

### Decisions

Each decision states the default this plan builds and the alternative it rejects.
`D4`, `D8`, `D11` and `D14` carry the owner’s open questions.

**D1: one player, two modes, one clock.** A single generated HTML document draws both
versions. `mode` selects slideshow or transitions; both read the same frame record, and
the transition mode additionally reads the transition record.
Every visual state is a function of `(mode, t)`. *Rejected:* two generators, which would
duplicate the stage, the panel, the fonts and the clock, and let the two versions drift
in what they say about a packing.

**D2: homes follow the motion lab and the atlas.** Shared code under
`packing/src/sqpack/known_best_video/`: `record.py` builds the frame record,
`transitions.py` the correspondence, `assets/` holds `player.css`, `player.js` and
`tween.js`. Three devtools: `build_known_best_video_data.py` writes the record,
`render_known_best_video.py` inlines record, assets and fonts into the player, and
`capture_known_best_video.py` turns the player into frames and files.
Generated artefacts under `packing/atlas/known-best/video/`: `known-best-video.json`
with its schema and `known-best-1-324-video.html`, both committed and byte-checked.
Captures land in `packing/atlas/known-best/video/captures/`, gitignored like
`packing/site/`. *Rejected:* `packing/atlas/rendering/`, the motion lab’s home, because
the video is an atlas product drawn from the known-best record, not a renderer gallery
entry; and a `video/` directory at the repository root, which AGENTS.md forbids.

**D3: three records, joined positionally, nothing re-derived.** Facts come from
`composite-figure.json`, embedded entry by entry as the poster’s `_figure_entries()`
reads them, so the video and the poster cannot disagree.
Poses come from the witnesses in world units (unit squares, container side `s`): centre
and angle from a `center-angle` record, centre and folded angle from a `corners` record,
rounded to a declared `pose_decimals` (default 6) that the record states, against
`D-359`. Fills, hue index, shade index, angle class and contact count come from the
rendering’s `square-fill` polygons.
The builder joins on the positional id (`witness k` is `square-{k:03d}`), and refuses
any `n` where the counts differ or where the witness angle and the rendering’s
`data-orientation-radians` disagree by more than `1e-9`, so a stale rendering fails the
build rather than colouring the wrong square.
*Rejected:* re-projecting corners and re-running `assign_square_colors` in the builder,
which is a second implementation of the drawing that can drift from the retained one;
and un-projecting the rendering’s canvas coordinates, which needs the side from a fourth
place.

**D4: the panel says what the poster’s card says, with the poster’s own icons.** The
headline is `n =` as a small line above the numeral, and the numeral is set at regular
weight and about 96 px on the 1080 stage, well under the Version 1 candidate’s first
bold 144 px cut; the type scale is compressed for video, with nothing on the stage under
28 px and at most four sizes; the side line `s(n) ≤ 12.656854` or `s(n) = 10` as
`side.display` gives it; the lower-bound line when `lower.shown`; the degree when known.
Every small note such as the degree sits on its own line directly below the value it
annotates, never beside it, so the layout is the same for every `n`. The status row
draws the poster’s badge glyphs as the poster draws them (the rounded rect with `O`,
`=`, `≈`, `R`, muted `R`, and the star polygon, solid or muted), each followed by a
short label: optimal, exact, numerical, rigid, rigid (catalogue), new lower bound.
Below it a quieter grey group headed “open” lists, each with a `?` badge in the same
style, what the record leaves open for this `n`: optimality, the exact value, rigidity;
it keeps a fixed height when empty.
The scarlet accent `#a3123f` means new and nothing else: the first-proved-here star and
its label here, the arriving square in Version 2; it is never used for proved or
optimal. These are the owner’s decisions from the review of the Version 1 candidate on
2026-09-07. A progress bar along the bottom of the stage runs from `1` to `324`, its
fill a function of the clock, with the current `n` riding its leading edge.
Opening and closing cards carry the poster’s title, release, repository and credit lines
and its two legend rows, so the video is attributed as the poster is.
Record-only frontier facts (`construction_method`, `found_by`, `found_year`,
`source_key`) are facts about the packing and its discovery and may be added, but only
by extending `composite-figure.json` with a `discovery` block through
`build_composite_figure_data`, with provenance, shown only when known; the poster simply
does not draw it. Whether to add it is the owner’s call.
Witness-layer facts (`coordinate_provenance`, `retrieved_date`, `raw_asset_retained`,
the caption’s “numerically checked”) are about the repository’s records and stay off the
panel, as they are off the card.
The panel keeps fixed slots, as the Version 1 spike built it, so an empty line does not
shift the lines below it between `n`; and it never shows two values of one fact at once.
Across a cut or a cross-fade the panel text changes at the fade midpoint, or fades out
and then in, while the picture dissolves; the Version 1 candidate cross-dissolved the
panel with the picture, and mid-fade the numerals 147 and 148 overlapped and ghosted
while the lower-bound digits smeared.
*Rejected:* reading the frontier records directly from the player’s builder, which would
put a second reader of the register beside the one the poster already has.

**D5: the kpress faces, inlined.** The numeral and the two `s(n)` lines are set in PT
Serif with the italic `s` and the function-name kern the math text face plan records;
badges, the progress line and the legend in Source Sans 3 at the site’s weights.
The six woff2 files are inlined as data URIs through the explainer’s `kpress_static`,
`kpress_css` and `inline_font_urls`, moved into a shared `devtools/kpress_assets.py`
that both renderers import.
The latin subsets carry none of ≤, ≥, √ or ≈ (the Version 1 spike’s finding), so a
seventh file, `KaTeX_Main-Regular.woff2`, is inlined with them, restricted by
`unicode-range` to those code points and placed after the reading faces with the
`size-adjust` kpress measured, the composition `katex-text-face.css` already uses.
The reason is determinism before taste: the poster sets Helvetica because cairo
rasterises it from the host, and the per-`n` captions set `system-ui`; a headless shell
on a Linux runner has neither, so a frame captured there and a frame captured on the Mac
would differ in every glyph.
With the faces inlined the frames depend on the browser revision alone.
*Rejected:* Helvetica for continuity with the poster; `system-ui` for continuity with
the captions.

**D6: the container fills a fixed square stage.** The stage is the per-`n` rendering’s
convention: the container always fills the same box, so the poster’s card and the video
agree on what a packing looks like, and the change of scale between `n` and `n + 1` is
`s(n) / s(n + 1)`, never more than a few per cent past the first few `n`. The player
holds poses in world units and applies `stage / s(t)` at draw time; in transition mode
`s(t)` is interpolated with the poses, so the container edge and the squares move
together. The frame is landscape: the square stage on the left, the panel on the right,
the way the rendering leaves its right third empty.
Both spikes built this stage.
Version 1 puts the packing in an 880 px box at `(90, 80)` of a `1920 × 1080` stage and
the panel in a 750 px column from `x = 1080`, which is the starting layout; Version 2
keeps the container at a constant screen size by interpolating the viewBox, `s × 1.09`
centred on the container, with the squares’ own easing.
The coordinator’s mid-fade frame of Version 1 shows the picture’s dissolve reading well
on this stage; two decimals of the 536-unit box are 0.016 px on that picture and 0.033
px at 4K, so the record’s six decimals in world units are past any raster.
*Rejected:* a fixed world scale with the container growing from 1 to 18, which draws
`n = 1` at an eighteenth of the stage’s width; and a square frame, which leaves no room
for a readable panel beside a square stage.

**D7: a virtual clock with a seek API, and nothing else moves.** The player exposes
`window.atlasVideo = {version, mode, setMode, duration, schedule, seek, stateKey}`.
`seek(t)` sets the DOM to the state at `t` seconds and returns; `stateKey(t)` is a
string that changes exactly when the drawn state changes; `schedule` lists the segment
boundaries so a capture can name the frame at which `n` begins.
No CSS transition or animation, no SMIL, no `Date.now`, no `Math.random`, no network:
the state is the function.
In a browser, Play runs a `requestAnimationFrame` loop that calls `seek` with elapsed
time, starts paused, and honours reduced motion by offering the scrubber alone, all as
the motion lab does.
*Rejected:* CSS transitions, which cannot be seeked; and Playwright’s built-in video
recording, which is real-time and non-deterministic.

**D8: frames from screenshots at `seek(k / fps)`, deduplicated, then ffmpeg.** The
capture launches the headless shell the PDF exporter launches, honouring the same
`SQPACK_CHROMIUM` override, at a fixed viewport and device scale factor 1, loads the
player by `file://` URI, waits on `document.fonts.ready` and the player’s own ready
marker, then for each frame index calls `seek`, compares `stateKey` with the previous
frame’s, and screenshots only when it changed, recording a duration for the repeated
frame in an ffmpeg concat list.
In slideshow mode that turns most of the dwell into one frame.
Defaults: `1920 × 1080` at 30 frames per second.
The per-frame cost is measured, by the coordinator on the Version 1 candidate in the
pinned headless shell: about 42 ms per dwell frame and 53 ms mid-fade at 1080p, 139,871
bytes per PNG; about 145 ms and 167 ms at `3840 × 2160` through device scale factor 2,
297,175 bytes; and 74 ms per frame in the Version 2 spike’s own capture at 1080p, whose
DOM is heavier per square.
Six captures of one instant were byte-identical at both sizes, the Version 2 spike found
the same across two browser launches, and two instants inside one dwell gave identical
bytes, so the deduplication rests on measurement: the slideshow’s 25,272 indexed frames
at the spike’s timing fall to 6,138 screenshots, one per dwell and 18 per fade, while a
transition capture keeps about two thirds of its 32,013. 4K costs about 3.4 times 1080p
per frame and 2.1 times the bytes; it is enabled when the owner chooses, and Phase 2
records both sizes in the timings file so the choice is re-read from a file.
Frame index to time is a pure function, so a capture splits by frame range across
processes and joins with ffmpeg’s concat demuxer, as both spikes proposed.
Encoding: H.264 in MP4 (`libx264`, `yuv420p`, a pinned CRF and preset, `+faststart`; the
spikes used `-crf 16` and `-crf 18`, and Phase 2 pins one) for players, and VP9 in WebM
for the web; both need the host or runner ffmpeg, since the bundled `ffmpeg-1011`
encodes VP8 only. The frames are the deterministic layer; the encode is receipted, not
byte-reproducible, the same standing the composite PDF has.
*Rejected:* screenshotting every frame of every dwell; and committing to 4K before the
cost is measured.

**D9: receipts, metadata and timings.** Beside every capture: `<stem>.receipt.json`
naming the player’s sha256 and path, the commit, the mode, the timeline parameters, the
viewport and scale factor, the Playwright version and browser revision and executable
kind, the ffmpeg version and arguments, the frame counts (indexed, captured, repeated),
and for transition mode the statement `intermediate_frames: illustrative-tween`. The
same statement and the player digest go into the container metadata
(`-metadata comment=`, `-metadata title=`). `<stem>.timings.json` records per-frame
screenshot milliseconds, encode wall, worker count and host shape, so the 4K decision
and any later regression read from a file rather than a memory.
Under OR-16 the digest names a real boundary: a video downloaded from a release is
checked against the player at the tagged commit, and the failure it detects is a video
captured from a player the commit does not hold.
No per-frame digest list; a second capture in one browser is the determinism check.
*Rejected:* embedding the receipt in the video stream, which no player exposes; and a
sidecar without the browser revision, which is the input most likely to move.

**D10: squares have identity across the sequence, and blocks move as blocks.** On
watching the fourth revision of the Version 2 candidate the owner ruled out a fresh
cheapest matching per pair, which reads as random motion: each step is to be seen as one
square added and the others moving coherently, because the squares have an identity.
So the record carries an identity chain: identity `k` is born as the new square of step
`n = k` and persists through every later pair by composing the maps, and the player keys
each square’s element by that identity, created once and never re-keyed.
The correspondence for the 158 assigned pairs is found at the block level first
(clusters by angle class and full-side-contact adjacency, matched by centroid, size and
orientation, each matched block carrying one rigid transform) and only then square by
square inside the remainder, so a tilted block turns back into rows as a body rather
than as a conveyor of one-unit hops; and the new square is a choice under a stated rule
(the square whose removal leaves the most coherent match, then the fewest contacts),
never the assignment’s leftover.
The fifth spike revision builds this and measures it; its numbers replace the per-square
statistics below where they differ.
For each consecutive pair the transition record states `method`, the assignment `pairs`
from `n`’s ids to `n + 1`’s, the `new_square` id and the rule that chose it, the
identity map, the block statistics, and the displacement and turn statistics.
`prefix`: the builder checks that `n`’s poses equal the first `n` of `n + 1`’s at the
record’s precision; the map is the identity and the new square is `n + 1`.
`shared-picture`: the builder finds the one index whose removal makes the tuples equal,
and refuses if there is not exactly one.
`assignment`: `scipy.optimize.linear_sum_assignment` on the `n × (n + 1)` cost of
squared centre displacement in world units plus a weighted squared shortest-arc turn
modulo a quarter turn; the unassigned column is the new square.
Ties are broken by id so the record is reproducible.
The turn is weighted at one square-width squared per 45-degree turn, weight 1 in the
Version 2 spike’s terms, and the record states the weight.
The spike matched in coordinates normalised by the larger of the pair’s two sides, with
the turn term divided by the same side squared; one normaliser per pair scales the whole
cost matrix, so its assignment is the world-unit assignment at that weight up to ties,
and there is nothing for Phase 3 to compare.
The weight is the whole choice, and the spike’s sweep over the 158 pairs decides it:
below 1 the matching sends a corner of the `2 × 2` to the centre of `n = 5` and lets the
new square appear in a corner; at 1 the corners stay corners at the cost of five pairs
with one close pass each; above 1 the slides lengthen and the close passes multiply (21
pairs at 2, 72 at 8) while the total turn barely moves, since the tilt census forces it.
What the assignment gets wrong is measured at 110→111, a derived packing collapsing into
the `11 × 11` grid with 46 rotations and 12 squares moving more than a unit, where the
tilted rows become a conveyor of one-unit hops instead of a block turning back (307→308
moves 23). Phase 3 first captures that pair under the three motion phases of `D11`; if
it still reads as a shiver, a fourth method, `cluster-assignment`, clusters each frame
by angle class and full-side-contact adjacency, matches clusters by centroid and size
and then squares within matched clusters, so a block turns rigidly about its centroid
and its members turn one way; the record names the method per pair either way.
The new square stays the unassigned column; a narrative rule for it is the spike’s
suggestion and nothing yet measures it.
*Rejected:* a hand-written Hungarian, since scipy is already a runtime dependency; and
matching in stage units, which would let the change of scale masquerade as motion.

**D11: add, reshuffle at a fixed scale, then scale down; linear centres, shortest-arc
angles, and cross-faded house fills.** The owner’s direction for the step is “add the
new square, then reshuffle without scaling, then scale down”, with the scaling as its
own animation whenever the container gets bigger.
So a step has three beats, each its own timeline segment: the arriving square appears at
its final pose with the scarlet mark; the existing squares then move as blocks while the
world-to-stage scale is held at `n`’s, so the container visibly grows on the stage and
no square changes size while it moves; and the whole picture then scales down to fit the
new side back into the stage box (`scale_seconds`, skipped when the side is unchanged).
The stage reserves a margin around the box for that growth; the early pairs whose growth
exceeds it are the cases the fifth and sixth spike revisions count and report.
The reverse of the first two beats, make room and then arrive, is kept as a selectable
mode so the owner can compare the two on the pairs where the arriving square would
overlap squares that have not yet moved, which the spike counts.
*Under investigation, the owner’s idea:* a relaxed intermediate.
Loosen `n` by inflating the container to `(1 + δ) s_n` and scaling every centre about
the container’s centre, which opens each contact by about `δ` times the pair’s
separation; add the new square; move the blocks in that relaxed space with a per-frame
overlap-resolution step, a push-apart along the separating axis the way the motion lab’s
`pair_gap` measures it; then tighten by the inverse contraction to `s_{n+1}`. The corpus
offers no slack of its own: the escape screen’s `min_container_slack` is zero or below
in every one of its 318 screened records, so the relaxed state has to be constructed.
In that state a float check is meaningful, which it is not at a tight packing, so every
relaxed frame is run through
`verify_packing(corners_from_poses(x, y, theta), side, float_sign(1e-9))` and the tween
labels the frames that pass as overlap-free and the rest as illustrative.
This is the animation form of the registered but unbuilt `H-013` δ-continuation family
and of `H-004`’s neighbour-transfer premise, and it never claims to search: both
endpoints are given, and the model between them is a path, not a proposal.
*Measured 2026-09-08, and the investigation closes.* The prototype built a crude
instance of exactly this loop: the container opens to 1.12 times the record’s side,
holds while the arriving square inflates, then contracts toward the record’s side,
pausing whenever two full-size squares overlap by more than 0.08. It loses.
Run blind it ends worse than the record on every genuinely packed case, by up to 6.8 per
cent at `307 → 308`; aimed at the known answer with the snap off, the settle still rests
one to 1.7 units per square away.
That is a result about constants chosen to look right in a video and never swept, not
about the mechanism, and the prototype’s notes say so themselves.
It is enough for this plan: Phase 3 does not ship a relaxed intermediate as a
`tween_model` option, and the block tween of `D10` is what Version 2 draws.
The mechanism keeps its research standing under `X-025`, as candidate `C6` against
`H-013`, where the instrument and the kill condition live.
Between `n` and `n + 1` each matched square’s centre moves linearly, its angle turns
along the shorter arc modulo 90 degrees (at most 45 degrees, an exact tie resolved
counter-clockwise as the spike did), the container side interpolates linearly, and the
new square fades in at its final pose during the last third of the transition (the spike
scaled it up from 0.35 over the first 0.45 s of its settle instead; Phase 3 judges the
two by eye). The motion phase is a timeline parameter: `simultaneous`, the default, or
`rotate-first` or `slide-first`, the two-stage moves the spike’s page already offers,
judged on 110→111 with `D10`’s cluster matching behind them.
Fills cross-fade from the retained fill at `n` to the retained fill at `n + 1`, mixed in
OkLCh, so a square that turns from a right angle to a diagonal passes from teal to
citron and a square whose class was renumbered changes hue without moving, both of which
are what the record says.
The frame at every integer `n` is the retained rendering’s geometry and colours.
The Version 2 spike built both rules and shipped the continuous ramp as its default, on
this evidence: under the house fills a sub-degree turn at 260→261 re-ranks the unpinned
classes and the central block cross-fades from citron to salmon while it barely moves,
which across a sequence reads as a colour change with no geometric cause; under the ramp
a square changes colour only when it turns, and the grid frames at 0° and 45° are the
house families exactly.
The evidence leans toward the ramp for the moving frames.
Against it stand the two costs the default was chosen to avoid: integer frames at other
tilts depart from the poster, and classes at nearby angles (20° and 22°) become one
colour, with mirror tilts differing on the spike’s long arc.
The default therefore stays with the house fills and the question stays the owner’s;
Phase 3 builds the ramp behind a record flag with its own label, so the owner judges
260→261 under both from the same player, as the spike did.
*Rejected as the default, offered to the owner:* a continuous OkLCh angle ramp through
the house teal and citron, which makes colour a function of angle at the price of
integer frames that no longer match the poster and a rule the record does not hold; and
an `AngleHueRegistry` carried across the sequence, which stabilises hues but changes the
fills the retained renderings carry.

**D12: the tween says what it is.** In transition mode the panel shows a persistent
line, “illustrative transition, not a packing”, from the first moving frame to the last,
and the record, the player’s metadata block, the receipt and the container metadata
carry `intermediate_frames: illustrative-tween`. The slideshow’s cross-fade is a
dissolve between two retained pictures and draws no new pose, so it carries no such
label.
*Rejected:* a label only in the metadata, which the toolkit plan already rules out
for illustrative interpolation.

**D13: an HTML profile beside the renderer.** The player is an HTML document with the
motion lab’s CSP plus `font-src data:`, no `fetch`, no `eval`, no `innerHTML`, no
external URL, and the generator refuses any of them.
`validate_safe_tree` is not widened and no per-`n` SVG changes.
The generator is deterministic: `--check` regenerates and compares bytes, as the motion
lab’s does. *Rejected:* an animated SVG in the safe profile, which forbids scripts and
rotation; and an external stylesheet or font, which would make the frames a function of
the network.

**D14: every fast check on the pull-request surface; the capture off it.** On the
surface: both `--check` regenerations as steps on the `checks` tier with budget entries;
the record and transition schemas; a test that every one of the 323 correspondences is a
bijection from `n`’s ids onto all but one of `n + 1`’s and that the prefix and
shared-picture methods hold where the data says they should; the JS model run in Node
against the Python record at segment boundaries and at a mid-transition; the player’s
byte budget; and a `--stand-in` capture of three frames (the first, a mid-transition,
the last) in `video.yml` on pull requests that touch its declared inputs, checked by
self-agreement, two captures in one browser byte for byte, the rule the PDF exporter
already uses. Off the surface: the full capture, run by `video.yml` on
`workflow_dispatch`, which attaches the MP4, WebM, receipt and timings to a GitHub
release; the atlas README and the site link the asset.
Frames are compared by receipt and by DOM state, not by pixels, unless the spike shows
pixels are stable across the host and the runner.
*Rejected as the default, offered to the owner:* copying the captures into
`packing/site/video/` at deploy, which puts a slow step and tens of megabytes in front
of the page deploy on every push that touches its inputs.

**D15: workflows.** Phase 0 is the two spikes under the `coding-spike` shortcut.
Phases 1 to 4 are W7 pipeline-improvement; Phase 4 closes with a W8 documentation pass
and a handoff entry.

**D16: snapping is production correctness for Animate, and evidence of nothing.** Added
2026-09-08, after Phase 0 built a solver and the two readings of its endpoint had to be
told apart. The prototype can end a move by blending the physics onto the retained poses
over the last fraction of the transition and finishing on them exactly.
For this plan that is not a flourish, it is the requirement: a run across all 324
records has to land each frame on what is actually known, which is the rule `D3` and
`D11` already state as “the frame at every integer `n` is the retained rendering’s
geometry and colours”.
So the retained player snaps, always, and the snap is not a switch a capture can leave
off.
What the snap is not is evidence about the physics, because the physics did not find
the endpoint; the prototype’s notes say so, and this session confirmed it from the other
side — with the snap off and the run aimed straight at the known answer, the settle
still rests one to 1.7 units per square away and 0.1 to 1.1 per cent wide.
No capture, receipt or caption may present a settled frame as a solver result, and the
`illustrative-tween` statement of `D12` covers a physics-settled frame exactly as it
covers an interpolated one.
The research use of the physics runs the other way, harvesting what the records’ contact
structures are rather than trying to reach them, and that direction is `X-025`’s.
*Rejected:* offering the snap as a switch in the retained player, which would let a
capture drift off the record; and reading a snapped run as a check on the tween model.

### Components

| Surface | Change |
| --- | --- |
| `src/sqpack/known_best_video/` (new) | `record.py` (frame record from witnesses, renderings, composite record; refusals), `transitions.py` (three correspondence methods, statistics), `assets/` (`player.css`, `player.js`, `tween.js`) |
| `devtools/build_known_best_video_data.py` (new) | writes `atlas/known-best/video/known-best-video.json`; `--update`, `--check`, `--review` printing bytes per square and the pair-method census |
| `devtools/render_known_best_video.py` (new) | inlines the record, the assets and the faces into `known-best-1-324-video.html`; `--output`, `--check`; refuses external references |
| `devtools/capture_known_best_video.py` (new) | frames at `seek`, deduplication, encode, receipt, timings; `--mode`, `--fps`, `--width`, `--height`, `--codec`, `--ffmpeg`, `--stand-in`, `--check` (self-agreement) |
| `devtools/kpress_assets.py` (new) | `kpress_static`, `kpress_css`, `inline_font_urls`, `data_uri` moved out of `render_explainer.py`, which imports them |
| `atlas/known-best/video/` (new) | the record, its schema, the player, a README; `captures/` gitignored |
| `atlas/known-best/known-best-atlas.schema.yaml`, `manifest.json` | a `video` block naming the record and the player |
| `.github/workflows/video.yml` (new) | stand-in capture on pull requests touching `CAPTURE_INPUTS`; full capture and release upload on dispatch; the browser cache keyed on `uv.lock` as `pages.yml` does |
| `sqpack/cli/validate.py`, `devtools/gate-budgets.yaml` | the two regeneration steps on the `checks` tier, measured |
| `tests/test_known_best_video.py` (new) | record shape, refusals, bijection over 323 pairs, method census `(160, 5, 158)`, Node-executed model, byte budget, CSP and self-containment, the workflow filter against `CAPTURE_INPUTS` |
| `.gitignore` | `packing/atlas/known-best/video/captures/` |
| README, `packing/atlas/README.md`, `packing/atlas/known-best/README.md`, the playbook, `SYNOPSIS.md` | a video section; “The two composites” gains a line on the third artefact; the handoff |

### The frame record

`packing.squares:KnownBestVideo/v1`, one document:

```yaml
contract: packing.squares:KnownBestVideo/v1
generated_by: python -m devtools.build_known_best_video_data
range: {first_n: 1, last_n: 324, count: 324}
sources:
  facts: atlas/known-best/composite-figure.json
  poses: witnesses/known-best/
  fills: atlas/known-best/rendering/
pose_decimals: 6
palette: [...]                 # the 100 fills the renderings use, indexed
frames:
  - n: 147
    side: "12.65685424949238"  # composite-figure side.value, verbatim
    squares: [[x, y, angle_deg, fill_index, angle_class], ...]   # world units
    facts: {...}               # the composite-figure entry, verbatim
transitions:                   # Phase 3
  - from_n: 147
    to_n: 148
    method: shared-picture     # prefix | shared-picture | assignment
    pairs: [[1, 1], [2, 2], ...]
    new_square: 22
    displacement: {max: "0", mean: "0"}
    turn_degrees: {max: "0"}
intermediate_frames: illustrative-tween
```

At 324 frames and 52,650 squares the pose array is about 35 bytes per square, so the
record is about two megabytes before the facts and the transitions.
The Version 2 spike’s all-pairs page confirms the estimate at about 36 bytes per square
of geometry, 2,077,600 bytes with four faces inlined, where the Version 1 candidate’s
four-corner encoding is 68 per square, 3,594,925 bytes with seven faces.
The player adds about 282 KB of inlined faces as base64 CSS (209,660 raw bytes across
the seven files) and the assets.
The budget is set from the measurement in Phase 1, the way the poster’s was, with the
spikes’ figures as the first ceiling.

### The timeline

The player’s `schedule` is computed from the parameters embedded in the record’s
`timeline` block: `dwell_seconds`, `fade_seconds` (slideshow), `move_seconds`,
`settle_seconds` and `motion_phase` (transitions), the two card durations, and a dwell
schedule: an override per pair kind (`prefix`, `shared-picture`, `assignment`) and an
override per named `n`, so that the owner’s answer to the dwell question is a record
edit and not a code change.
Slideshow: card, then for each `n` a dwell followed by a cross-fade to `n + 1`, then
card.
Transitions: card, then for each `n` a dwell followed by the tween to `n + 1`, then
card. The slideshow defaults are 1.5 s dwell and 0.5 s fade, the pace the owner chose on
review after the Version 1 spike’s 2.0 s and 0.6 s (842.4 s) read as too slow; that is
`324 × 1.5 s` of dwell and `323 × 0.5 s` of fades, 648 s before the cards.
For transitions the defaults are 1.0 s dwell, 1.4 s move and 0.4 s settle, tightened
from the Version 2 spike’s 1.2 s, 1.6 s and 0.5 s, which the spike measured at 1,067.1 s
over the corpus at uniform timing; with 0.5 s dwell, 0.4 s settle and no move for the
165 static appends the spike’s timing runs 671 s, which is what the per-kind override is
for. Everything downstream reads `schedule`, so a change to the defaults is one line in
the record and a rebuild.

### Version 2 in one pass

For a pair `(n, n + 1)` with assignment `pairs` and progress `u ∈ [0, 1]`, eased:

- `s(u) = (1 − u) s_n + u s_{n+1}`; the stage scale is `stage / s(u)`.
- Matched square `(i, j)`: centre `(1 − u) c_i + u c_j`; angle `θ_i + u Δ`, where `Δ` is
  the shortest arc from `θ_i` to `θ_j` modulo 90 degrees; fill `mix(fill_i, fill_j, u)`
  in OkLCh.
- New square `j*`: drawn at its final pose with opacity rising from 0 at `u = 2/3` to 1
  at `u = 1`.
- The label of `D12` is visible for `0 < u < 1`.

The 160 prefix pairs reduce to a single square fading in, and the 5 shared-picture pairs
to the same with the container fixed; the 158 assigned pairs are where the motion is,
and the spike’s displacement statistics say how much.

## Implementation Plan

Beads are linked to this spec; the epic orders them.
Each phase closes on its own validation command and a commit by the coordinator.

### Phase 0: Spikes (done)

- [x] Version 1 spike: single-file slideshow, deterministic `seek`, kpress faces, the
  card facts as text; notes record the player bytes and whether one frame captured twice
  in one browser agrees byte for byte.
- [x] Version 2 spike: correspondence for all 323 pairs by the three rules, translate
  and rotate per square, both colour rules, displacement statistics over the corpus.
- [x] Fold both notes into “Spike findings”; confirm or revise `D6`, `D8`, `D10`, `D11`;
  decide for each spike whether its code is promoted into Phase 1 or kept as reference;
  close the spike beads with a reason.

Closed 2026-09-07: both NOTES.md files read and cited in “Spike findings” with the
coordinator’s own measurements; `D4`, `D5`, `D6`, `D8`, `D10` and `D11` revised; each
spike’s code dispositioned there; `think-5oba` and `think-l78w` closed.

Reopened and re-closed 2026-09-08, because the closure was premature on one side.
The Version 2 candidate kept going after its bead closed and became a solver workbench;
“What Phase 0 became” records the drift and the split of ownership, `D11` records what
its physics measured and closes the relaxed-intermediate investigation, and `D16`
records what its snap does and does not establish.
The solver, its modes and its research questions leave this plan for `X-025` at this
point; the video artefacts stay here and Phases 1 to 4 are unchanged in scope.

### Phase 1: The record and the Version 1 player

- [ ] `known_best_video/record.py` and `build_known_best_video_data.py` with the schema;
  refusals for count and angle mismatches; `--review` prints bytes per square.
- [ ] `devtools/kpress_assets.py` extracted from `render_explainer.py`, with the KaTeX
  symbol subset of `D5` beside the six kpress faces; the explainer’s `--check` still
  passes byte for byte.
- [ ] `render_known_best_video.py` and the assets: stage, panel, cards, slideshow mode,
  `window.atlasVideo`, the CSP, the ready marker, the browser controls.
- [ ] The panel text cuts at the fade midpoint or fades out and then in, never
  overlapping (the mid-fade ghosting of 147 and 148 on the Version 1 candidate); the
  panel keeps its fixed slots; the Node model asserts one value per fact at every
  instant of a fade.
- [ ] The `timeline` block’s dwell schedule: the per-kind and per-`n` overrides read by
  `schedule`, tested against the two spike totals (842.4 s at 2.0 s and 0.6 s; 1,067.1 s
  and 671 s for the transition defaults with and without the static-append override).
- [ ] Tests: record shape and refusals, Node-executed model at segment boundaries, byte
  budget from the measurement, self-containment, determinism.
- [ ] Both `--check` steps on the `checks` tier with budget entries; the manifest and
  schema gain the `video` block; `.gitignore` gains `captures/`.

Closes on: `packing-validate --checks` green with the new steps measured, and
`render_known_best_video --check` byte-identical in two fresh processes.

### Phase 2: The capture tool and the first Version 1 video

- [ ] `capture_known_best_video.py`: browser launch as the PDF exporter’s, `seek` loop,
  `stateKey` deduplication, concat list, H.264 and VP9 encodes, receipt, timings,
  `--stand-in`, `--check`.
- [ ] Measure per-frame cost at `1920 × 1080` and `3840 × 2160` on the host with the
  stand-in; record both in the timings file and here.
- [ ] `video.yml`: stand-in on pull requests under `CAPTURE_INPUTS`, with the test that
  compares the filter to the declaration; full capture and release upload on dispatch.
- [ ] The first full slideshow capture on the host; its receipt and timings kept in the
  session record; the owner reviews it.

Closes on: `capture_known_best_video --stand-in --check` self-agreeing locally and in
`video.yml`, and one full Version 1 capture with a receipt.

### Phase 3: The transition record and the Version 2 player

- [ ] `known_best_video/transitions.py`: the three methods, the statistics, tie-breaking
  by id; the builder writes `transitions` and the `intermediate_frames` statement.
- [ ] The bijection test over all 323 pairs and the method census `(160, 5, 158)`.
- [ ] `tween.js` and transition mode: interpolation per the design, OkLCh mixing, the
  new square’s fade, the `D12` label; the Node model test at a mid-transition.
- [ ] `motion_phase` as a timeline parameter (`simultaneous`, `rotate-first`,
  `slide-first`) and the per-kind timing for the 165 static appends; 110→111 captured
  under each phase and judged.
- [ ] Block-level matching as the method for the 158 assigned pairs, per `D10`: clusters
  by angle class and full-side-contact adjacency, matched by centroid, size and
  orientation, one rigid transform per matched block, then squares within the remainder;
  the record names the method per pair, the block statistics and the residuals, and the
  bijection test covers it.
- [ ] The identity chain: each square’s global identity born at its step and composed
  through every later map; the player keys elements by it; a test composes all 323 maps
  and asserts every identity born at step `k` appears exactly once in every frame from
  `k` to 324.
- [ ] The new-square rule of `D10` recorded per pair, with a census of how often it
  differs from the assignment’s leftover.
- [ ] The add-then-make-room staging of `D11` as the default `motion_phase`, with the
  reverse order selectable and the arrival-overlap census recorded; the scale-down beat
  as its own segment with `scale_seconds`, the stage margin it needs, and the census of
  early pairs whose growth exceeds the margin.
- [x] Spike: the relaxed intermediate of `D11`. Dropped 2026-09-08, not deferred.
  Phase 0’s prototype ran the loop at `δ = 0.12` with a contraction that pauses on
  overlap and lost every genuinely packed case, by up to 6.8 per cent; `D11` records the
  measurement and the reasoning.
  Phase 4 ships no `tween_model` option, the block tween of `D10` is what Version 2
  draws, and the sweep over `δ` with the per-frame `verify_packing` census moves to
  `X-025` as candidate `C6`, where `H-013` owns the kill condition.
- [ ] The continuous-angle rule behind a record flag with its own label, so the owner
  judges 260→261 under both rules from the same player.

Closes on: `packing-validate --checks` green, the bijection test in the quick lane, and
the stand-in capture of a mid-transition frame self-agreeing.

### Phase 4: The Version 2 video, publication and documents

- [ ] The first full transition capture; receipt and timings kept.
- [ ] Release with both videos and their sidecars via `video.yml`; the atlas README, the
  root README and the site link them; `check_published_site` learns the link if the site
  serves anything.
- [ ] The playbook gains a section on the video (what it reads, what it declares, how to
  rebuild and recapture); “The two composites” names the third artefact.
- [ ] W8 pass over the touched documents; the handoff entry; beads closed.

Closes on: the full checkpoint green, and both release assets downloadable with receipts
that name the player at the tagged commit.

## Testing Strategy

- The two generators are byte-deterministic and `--check` regenerates in a fresh
  process, the motion lab’s rule; the retained files are the goldens.
- The record’s refusals are tested with a deliberately shifted witness and a rendering
  whose angle disagrees, so a stale rendering cannot pass silently.
- The correspondence test is exhaustive over the corpus and cheap: 323 pairs of arrays
  no longer than 324, checked for bijectivity, the method census, and for the prefix and
  shared-picture cases that the data supports the method.
- The JS model runs in Node with the same wheel the motion lab tests use, evaluated at
  every segment boundary and at chosen interior instants, against poses computed in
  Python from the record.
- Frames are checked by self-agreement in one browser and by reading the DOM at
  `seek(t)`, not by pixels; a pixel golden waits for the spike to show stability across
  the host and the runner, the standing the toolkit plan already gives raster goldens.
- The stand-in capture is the pull-request surface’s proof that the pipeline runs end to
  end; the full capture earns its exit from the surface by its measured cost, recorded
  in the timings file.
- Every new step has a budget entry, and the quick lane’s 12 s ceiling applies to every
  new test.

## Rollout Plan

One pull request per phase from a branch off `main`, each opened with the generated cost
block first (OR-9), Phase 1 refreshed rather than reopened if Phase 2 lands before
review. The videos ship as release assets after Phase 2 and Phase 4; the site links them
once the owner has chosen the channel.
Nothing about the poster or the per-`n` renderings changes at any phase.

## Open Questions

- Aspect ratio and resolution: landscape `16:9` at `1920 × 1080` as `D6` and `D8`
  default, or `3840 × 2160` now that the per-frame cost is measured at about 3.4 times
  1080p’s (145 to 167 ms against 42 to 53 ms per frame, 297 KB against 140 KB per PNG),
  or a square frame with the panel below the stage?
- Dwell and length: 3 s per packing with 0.5 s fades puts the slideshow near nineteen
  minutes and the Version 1 spike’s 2.0 s and 0.6 s at 842.4 s; uniform transition
  timing puts Version 2 at 1,067.1 s (17.8 minutes), and a 0.9 s beat with no move for
  the 165 static appends at 671 s (11.2 minutes).
  On review the owner asked for a faster switch, and the revised candidates run at 1.5 s
  dwell with 0.5 s fades (648 s, about eleven minutes) and 1.0 s dwell, 1.4 s move and
  0.4 s settle; those become the defaults.
  Still open: the shorter beat for the 165 steps where one square appears and nothing
  else moves, and a schedule that holds longer on the cases the Version 1 spike names
  (5, 11, 12, 17 to 21, 29, 54, and the first-party lower bounds).
  The `timeline` block takes any of these.
- The panel: the icons, the short labels, the open group, the scarlet rule and the
  progress bar are decided (`D4`). Still open: whether the exact form is drawn with its
  radicals and the minimal polynomial shown for the 36 cases with no closed form, as the
  Version 1 spike does; and whether the `discovery` block (`construction method`, `found
  by`, `found year`, source key) is added to `composite-figure.json` and shown when
  known.
- Version 2 colour: cross-faded house fills (`D11`), or the continuous angle ramp the
  Version 2 spike shipped as its default after 260→261 flickered under the house fills,
  with the integer frames departing from the poster?
  If the ramp, the revised candidate uses the symmetric teal-to-citron sweep rather than
  the long arc through red and blue, because the owner reserved scarlet for “new” and
  the long arc painted 58° to 65° tilts in salmon beside the scarlet mark in 16 frames;
  mirror tilts then share a colour, which is the trade the sweep makes.
  A third answer arrived with the prototype’s revision 12 and is now on the table:
  colour by the persistent identity `D10` already requires, so a square keeps its colour
  for the whole run and a viewer can follow one square from `n = 5` to `n = 324`. It has
  a measured ceiling this plan would hit and the workbench does not: the prototype’s
  green band holds 42 distinguishable entries, which repeats 7.7 times over 324 squares,
  so identity colouring stops being an identity at large `n` unless a second channel
  carries it. The bead for that ceiling is under `X-025`.
- Publication: release assets linked from the site (`D14`), or the captures copied into
  the site deploy?
- Frame rate: 30 frames per second, or 60 for the transition version, which doubles its
  capture and its encode?

## References

- [`packing/atlas/known-best/FIGURE-PLAYBOOK.md`](../../../../packing/atlas/known-best/FIGURE-PLAYBOOK.md),
  “The rule that matters”, “Staleness cannot pass quietly”, “Fonts”, “The two
  composites”
- [Atlas expansion to 324](plan-2026-09-07-atlas-expansion-to-324.md), `D5` on the
  poster’s encoding levers
- [Deterministic SVG rendering toolkit](plan-2026-08-24-deterministic-svg-rendering-toolkit.md),
  “Animation Semantics” and the testing section’s line on intermediate frames
- [Generalized motion lab](plan-2026-08-25-generalized-motion-lab.md), the
  `illustrative tween` label
- [The `n = 5` motion lab spike](spike-2026-08-25-n5-motion-lab.md), the HTML profile
  and its disposition
- [Math text face integration](plan-2026-09-07-math-text-face.md), the italic `s` and
  the function-name kern
- [`packing/atlas/rendering/README.md`](../../../../packing/atlas/rendering/README.md),
  the motion lab’s home and the raster-golden standing
- [`X-025`](../../../../packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md),
  which owns the solver workbench Phase 0 grew, the three-axis decomposition of its
  modes, and the research candidates its measurements bear on
- [`packing/atlas/known-best/video/spikes/v2-transitions/NOTES.md`](../../../../packing/atlas/known-best/video/spikes/v2-transitions/NOTES.md),
  revisions 6 to 13, the source for every workbench measurement quoted here
- [`operating-rules.md`](../../../../operating-rules.md), OR-1, OR-9, OR-13, OR-14,
  OR-16
- Beads: epic `think-hsdj` under `think-wfz1`; spikes `think-5oba` (Version 1) and
  `think-l78w` (Version 2); phases `think-4ew6`, `think-007q`, `think-krtt`,
  `think-gpfg`; `think-0juv` (the atlas expansion); `think-vb0v` (the motion lab spike);
  defect `D-359`. The workbench beads are not here: they hang off `X-025`’s own epic,
  which is the point of the split.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
